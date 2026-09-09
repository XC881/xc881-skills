#!/usr/bin/env python3
"""Opt-in parser for recorded continuation runs. No model calls."""

import argparse
import json
from pathlib import Path
import re

from audit_queue_execution import commands_from_events
from audit_skill_loads import validate_continuations

USAGE_KEYS = (
    "totalTokens", "inputTokens", "cachedInputTokens", "cacheWriteInputTokens",
    "outputTokens", "reasoningOutputTokens",
)
UNOBSERVED = ("provider_request_bodies", "host_injection_dedup", "child_agent_usage")
INSTRUCTION_RE = re.compile(r"(SKILL\.md|references/[^/\s'\"]+\.md)")
HOST_COMPACTION = "host-compaction-queue-resume"


def _zero_usage():
    return {key: 0 for key in USAGE_KEYS}


def _parse_usage(block):
    if not isinstance(block, dict):
        return None, ["token_usage_total_missing"]
    parsed = {}
    violations = []
    for key in USAGE_KEYS:
        if key not in block:
            if key == "cacheWriteInputTokens":
                parsed[key] = 0
                continue
            violations.append(f"token_usage_missing:{key}")
            parsed[key] = 0
            continue
        value = block[key]
        if isinstance(value, bool) or not isinstance(value, int):
            violations.append(f"token_usage_invalid:{key}")
            parsed[key] = 0
            continue
        if value < 0:
            violations.append(f"token_usage_negative:{key}")
        parsed[key] = value
    return parsed, violations


def _usage(block):
    parsed, _ = _parse_usage(block)
    return parsed or _zero_usage()


def _sub(left, right):
    return {key: left[key] - right[key] for key in USAGE_KEYS}


def _decreased(current, previous):
    return any(current[key] < previous[key] for key in USAGE_KEYS)


def usage_from_events(events, expected_thread_id=None):
    last_total = _zero_usage()
    previous_total = None
    observed = False
    duplicate_total_notifications = 0
    diagnostics = []
    updates_by_turn = {}
    completion_order = []
    completion_status = {}

    def belongs(params, event_kind):
        if expected_thread_id is None:
            return True
        actual = params.get("threadId")
        if actual != expected_thread_id:
            diagnostics.append(f"{event_kind}_thread_mismatch")
            return False
        return True

    for event in events:
        if not isinstance(event, dict):
            diagnostics.append("malformed_event")
            continue
        method = event.get("method")
        if method == "thread/tokenUsage/updated":
            params = event.get("params") or {}
            observed = True
            if not belongs(params, "token_usage"):
                continue
            turn_id = params.get("turnId")
            if not isinstance(turn_id, str) or not turn_id:
                diagnostics.append("token_usage_missing_turn_id")
                turn_id = None
            usage = params.get("tokenUsage") or {}
            total, errors = _parse_usage(usage.get("total"))
            diagnostics.extend(errors)
            if total is None:
                continue
            if previous_total is not None:
                if _decreased(total, previous_total):
                    diagnostics.append("cumulative_total_regressed")
                if total == previous_total:
                    duplicate_total_notifications += 1
            previous_total = total
            last_total = total
            if turn_id is not None:
                updates_by_turn.setdefault(turn_id, []).append(total)
        elif method == "turn/completed":
            params = event.get("params") or {}
            if not belongs(params, "turn_completed"):
                continue
            turn = params.get("turn") or {}
            turn_id = turn.get("id")
            if not isinstance(turn_id, str) or not turn_id:
                diagnostics.append("turn_completed_missing_turn_id")
                continue
            if turn_id in completion_status:
                diagnostics.append(f"duplicate_turn_completed:{turn_id}")
                continue
            completion_order.append(turn_id)
            completion_status[turn_id] = turn.get("status")

    turns = []
    previous_turn_total = _zero_usage()
    for turn_id in completion_order:
        totals = updates_by_turn.get(turn_id, [])
        if not totals:
            diagnostics.append(f"missing_usage_for_turn:{turn_id}")
            total = previous_turn_total
        else:
            total = totals[-1]
        delta = _sub(total, previous_turn_total)
        if any(value < 0 for value in delta.values()):
            diagnostics.append(f"turn_usage_regressed:{turn_id}")
        turns.append({
            "turn_id": turn_id,
            "status": completion_status[turn_id],
            "usage": delta,
        })
        previous_turn_total = total

    for turn_id in updates_by_turn:
        if turn_id not in completion_status:
            diagnostics.append(f"usage_for_uncompleted_turn:{turn_id}")
    return {
        "method": "cumulative_total_delta", "observed": observed,
        "thread": last_total, "turns": turns,
        "valid": not diagnostics,
        "diagnostics": sorted(set(diagnostics)),
        "duplicate_total_notifications": duplicate_total_notifications,
    }


def host_compaction(events):
    for event in events:
        if event.get("method") == "thread/compacted":
            return True
        item = (event.get("params") or {}).get("item") or {}
        if event.get("method") == "item/completed" and item.get("type") == "contextCompaction":
            return True
    return False


def instruction_reads(commands, skill_dir):
    marker = str(skill_dir or "").rstrip("/")
    reads = []
    for command in commands:
        if "apply_patch" in command or "*** Update File:" in command:
            continue
        if marker and marker in command:
            reads.extend(INSTRUCTION_RE.findall(command.split(marker, 1)[1]))
        else:
            reads.extend(INSTRUCTION_RE.findall(command))
    return reads


def efficiency_conclusion(baseline, candidate):
    unobserved = list(UNOBSERVED)
    if baseline.get("status") != "executed" or candidate.get("status") != "executed":
        return {"claim": None, "reason": "unexecuted_or_failed", "unobserved": unobserved}
    for key in ("model", "client_version", "case_sha256"):
        if baseline.get(key) != candidate.get(key):
            return {"claim": None, "reason": f"condition_mismatch:{key}", "unobserved": unobserved}
        if not baseline.get(key) or not candidate.get(key):
            return {"claim": None, "reason": f"missing_comparison_metadata:{key}", "unobserved": unobserved}
    for key in ("case", "owner", "model_provider"):
        if key in baseline or key in candidate:
            if baseline.get(key) != candidate.get(key):
                return {"claim": None, "reason": f"condition_mismatch:{key}", "unobserved": unobserved}

    baseline_turns = baseline.get("turns")
    candidate_turns = candidate.get("turns")
    if baseline_turns is not None or candidate_turns is not None:
        if not isinstance(baseline_turns, list) or not isinstance(candidate_turns, list):
            return {"claim": None, "reason": "condition_mismatch:turns", "unobserved": unobserved}
        baseline_signature = [
            (turn.get("kind"), turn.get("status"))
            for turn in baseline_turns
        ]
        candidate_signature = [
            (turn.get("kind"), turn.get("status"))
            for turn in candidate_turns
        ]
        if baseline_signature != candidate_signature:
            return {"claim": None, "reason": "condition_mismatch:turn_plan", "unobserved": unobserved}

    if "host_compaction" in baseline or "host_compaction" in candidate:
        if bool(baseline.get("host_compaction")) != bool(candidate.get("host_compaction")):
            return {"claim": None, "reason": "condition_mismatch:host_compaction", "unobserved": unobserved}

    base_usage = baseline.get("usage") or {}
    cand_usage = candidate.get("usage") or {}
    if not base_usage.get("observed") or not cand_usage.get("observed"):
        return {"claim": None, "reason": "missing_usage", "unobserved": unobserved}
    if base_usage.get("valid", True) is False or cand_usage.get("valid", True) is False:
        return {"claim": None, "reason": "invalid_usage", "unobserved": unobserved}
    base_thread = base_usage.get("thread")
    cand_thread = cand_usage.get("thread")
    if not isinstance(base_thread, dict) or not isinstance(cand_thread, dict):
        return {"claim": None, "reason": "malformed_usage", "unobserved": unobserved}
    if type(base_thread.get("totalTokens")) is not int or type(cand_thread.get("totalTokens")) is not int:
        return {"claim": None, "reason": "malformed_usage", "unobserved": unobserved}
    if "chars" in baseline or "chars" in candidate:
        return {"claim": None, "reason": "character_counts_are_not_usage", "unobserved": unobserved}
    return {
        "claim": "observed_only",
        "baseline_thread_tokens": base_thread["totalTokens"],
        "candidate_thread_tokens": cand_thread["totalTokens"],
        "baseline_instruction_reads": list(baseline.get("instruction_reads") or []),
        "candidate_instruction_reads": list(candidate.get("instruction_reads") or []),
        "baseline_host_compaction": bool(baseline.get("host_compaction")),
        "candidate_host_compaction": bool(candidate.get("host_compaction")),
        "unobserved": unobserved,
        "note": "Thread-visible provider totals and tool file reads only. No request-body dedup or session-wide savings.",
    }


def attach_usage(report, events):
    usage = usage_from_events(events, report.get("thread_id"))
    expected_turns = [
        turn for turn in report.get("turns", []) if turn.get("kind") != "compact"
    ]
    expected_turn_ids = [turn.get("turn_id") for turn in expected_turns if turn.get("turn_id")]
    actual_turn_ids = [turn["turn_id"] for turn in usage["turns"]]
    report_turn_missing_id = len(expected_turn_ids) != len(expected_turns)
    if report_turn_missing_id or (expected_turn_ids and actual_turn_ids != expected_turn_ids):
        usage = dict(usage)
        usage["valid"] = False
        usage["diagnostics"] = sorted(set(
            [*usage.get("diagnostics", []), "turn_completion_mapping_mismatch"]
        ))
    attached = {
        "usage": usage,
        "instruction_reads": instruction_reads(
            commands_from_events(events), report.get("effective_skill", "")
        ),
        "host_compaction": host_compaction(events),
    }
    if report.get("status") != "executed":
        attached["usage_claim"] = None
        attached["usage_reason"] = report.get("status")
    elif not usage["observed"]:
        attached["usage_claim"] = None
        attached["usage_reason"] = "missing_usage"
    elif not usage.get("valid", True):
        attached["usage_claim"] = None
        attached["usage_reason"] = "invalid_usage"
    return attached


def load_events(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def load_report(run_dir):
    run_dir = Path(run_dir)
    run_path, events_path = run_dir / "run.json", run_dir / "events.jsonl"
    if not run_path.is_file() or not events_path.is_file():
        raise FileNotFoundError("run directory must contain run.json and events.jsonl")
    report = json.loads(run_path.read_text(encoding="utf-8"))
    report.update(attach_usage(report, load_events(events_path)))
    return report


def compare_runs(baseline, candidate):
    return efficiency_conclusion(baseline, candidate)


def validate_executable_cases(root=None):
    root = Path(root or Path(__file__).resolve().parents[1])
    scenarios = validate_continuations(root)
    seen = set()
    for scenario in scenarios:
        rel = scenario["executable"]
        if rel in seen:
            raise ValueError(f"duplicate executable mapping: {rel}")
        seen.add(rel)
        case = json.loads((root / rel).read_text(encoding="utf-8"))
        if case.get("owner") != scenario["owner"]:
            raise ValueError(f"owner mismatch: {scenario['id']}")
        if not isinstance(case.get("turns"), list) or not case["turns"]:
            raise ValueError(f"executable case has no turns: {scenario['id']}")
        compact = any(isinstance(turn, dict) and turn.get("compact") for turn in case["turns"])
        if scenario["id"] == HOST_COMPACTION:
            if not compact:
                raise ValueError("host-compaction-queue-resume must use real thread/compact")
        elif compact:
            raise ValueError(f"non-host continuation must not set compact: {scenario['id']}")
        blob = json.dumps(case)
        if "expected read" in blob.lower() or "intended answer" in blob.lower():
            raise ValueError(f"executable case leaks evaluation keys: {scenario['id']}")
    return scenarios


def _public(report):
    return {
        "case": report.get("case"), "status": report.get("status"),
        "model": report.get("model"), "usage": report.get("usage"),
        "instruction_reads": report.get("instruction_reads"),
        "host_compaction": report.get("host_compaction"),
        "usage_claim": report.get("usage_claim"), "usage_reason": report.get("usage_reason"),
        "usage_scope": report.get("usage_scope"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", nargs="?", type=Path, help="directory with run.json and events.jsonl")
    parser.add_argument("--compare", nargs=2, type=Path, metavar=("BASELINE", "CANDIDATE"))
    args = parser.parse_args(argv)
    if bool(args.run_dir) == bool(args.compare):
        parser.error("provide a run directory or --compare BASELINE CANDIDATE")
    try:
        if args.compare:
            conclusion = compare_runs(load_report(args.compare[0]), load_report(args.compare[1]))
            print(json.dumps(conclusion, indent=2, ensure_ascii=False))
            return 0 if conclusion.get("claim") == "observed_only" else 1
        report = load_report(args.run_dir)
    except (OSError, UnicodeError, json.JSONDecodeError, FileNotFoundError) as exc:
        parser.error(str(exc))
    print(json.dumps(_public(report), indent=2, ensure_ascii=False))
    return 0 if report.get("status") == "executed" and report.get("usage", {}).get("observed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
