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


def _usage(block):
    if not isinstance(block, dict):
        return {key: 0 for key in USAGE_KEYS}
    return {key: int(block.get(key) or 0) for key in USAGE_KEYS}


def _sub(left, right):
    return {key: left[key] - right[key] for key in USAGE_KEYS}


def usage_from_events(events):
    thread = {key: 0 for key in USAGE_KEYS}
    last_total = dict(thread)
    observed = False
    turns = []
    for event in events:
        method = event.get("method")
        if method == "thread/tokenUsage/updated":
            params = event.get("params") or {}
            usage = params.get("tokenUsage") or {}
            last_total = _usage(usage.get("total"))
            observed = True
        elif method == "turn/completed":
            turn = (event.get("params") or {}).get("turn") or {}
            turns.append({
                "turn_id": turn.get("id"), "status": turn.get("status"),
                "usage": _sub(last_total, thread),
            })
            thread = dict(last_total)
    return {
        "method": "cumulative_total_delta", "observed": observed,
        "thread": last_total, "turns": turns,
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
    base_usage = (baseline.get("usage") or {}).get("thread")
    cand_usage = (candidate.get("usage") or {}).get("thread")
    if not (baseline.get("usage") or {}).get("observed") or not (candidate.get("usage") or {}).get("observed"):
        return {"claim": None, "reason": "missing_usage", "unobserved": unobserved}
    if "chars" in baseline or "chars" in candidate:
        return {"claim": None, "reason": "character_counts_are_not_usage", "unobserved": unobserved}
    return {
        "claim": "observed_only",
        "baseline_thread_tokens": base_usage["totalTokens"],
        "candidate_thread_tokens": cand_usage["totalTokens"],
        "baseline_instruction_reads": list(baseline.get("instruction_reads") or []),
        "candidate_instruction_reads": list(candidate.get("instruction_reads") or []),
        "baseline_host_compaction": bool(baseline.get("host_compaction")),
        "candidate_host_compaction": bool(candidate.get("host_compaction")),
        "unobserved": unobserved,
        "note": "Thread-visible provider totals and tool file reads only. No request-body dedup or session-wide savings.",
    }


def attach_usage(report, events):
    usage = usage_from_events(events)
    attached = {
        "usage": usage,
        "instruction_reads": instruction_reads(
            commands_from_events(events), report.get("effective_skill", "")
        ),
        "host_compaction": host_compaction(events),
    }
    if report.get("status") != "executed" or not usage["observed"]:
        attached["usage_claim"] = None
        attached["usage_reason"] = report.get("status") if report.get("status") != "executed" else "missing_usage"
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
