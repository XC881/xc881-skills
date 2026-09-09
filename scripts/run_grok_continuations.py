#!/usr/bin/env python3
"""Opt-in Grok headless continuation runner. No CI model calls."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import uuid
from pathlib import Path
from string import Template
from urllib.parse import quote

from audit_grok_sessions import compare_snapshots, parse_session
from run_skill_continuations import local_path

HOST_COMPACTION = "host-compaction-queue-resume"


def require_uuid(value):
    return str(uuid.UUID(str(value)))


def encoded_cwd(cwd):
    return quote(str(Path(cwd).resolve()), safe="")


def session_dir(cwd, session_id, grok_home=None):
    home = Path(grok_home) if grok_home else Path.home() / ".grok"
    return home / "sessions" / encoded_cwd(cwd) / require_uuid(session_id)


def create_args(prompt, cwd, session_id, max_turns=20):
    session_id = require_uuid(session_id)
    args = [
        "grok", "-p", prompt, "-s", session_id, "--cwd", str(cwd),
        "--output-format", "json", "--always-approve", "--no-auto-update",
        "--max-turns", str(max_turns),
    ]
    if "-r" in args or "--resume" in args:
        raise ValueError("-s creates a UUID session and must not resume")
    return args


def resume_args(prompt, cwd, session_id, max_turns=20):
    session_id = require_uuid(session_id)
    args = [
        "grok", "-p", prompt, "-r", session_id, "--cwd", str(cwd),
        "--output-format", "json", "--always-approve", "--no-auto-update",
        "--max-turns", str(max_turns),
    ]
    if "-s" in args or "--session-id" in args:
        raise ValueError("-r resumes; do not pass -s (not an upsert)")
    return args


def grok_env():
    env = os.environ.copy()
    env["GROK_DISABLE_AUTOUPDATER"] = "1"
    return env


def copy_session(src, dest):
    dest = Path(dest)
    if dest.exists():
        shutil.rmtree(dest)
    if Path(src).is_dir():
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("*.lock", "*.tmp"))


def run_case(case, skill_root, out, timeout, grok_home=None, grok_run=None):
    owner = case["owner"]
    source_skill = local_path(skill_root, owner)
    if not (source_skill / "SKILL.md").is_file():
        raise ValueError(f"missing skill entry: {source_skill}")
    out.mkdir(parents=True, exist_ok=False)
    skill = out / "skill"
    shutil.copytree(source_skill, skill)
    entry = skill / "SKILL.md"
    workspace = out / "workspace"
    workspace.mkdir()
    variables = {"skill": str(skill), "entry": str(entry), "workspace": str(workspace), "owner": owner}

    def expand(text):
        return Template(text).substitute(variables)

    def write_files(files):
        for relative, content in files.items():
            target = local_path(workspace, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expand(content), encoding="utf-8")

    write_files(case.get("files", {}))
    session_id = str(uuid.uuid4())
    captured = session_dir(workspace, session_id, grok_home)
    if captured.exists():
        raise ValueError("session id already exists; -s does not resume")
    report = {
        "case": case["id"], "owner": owner, "host": "grok",
        "effective_skill": str(skill),
        "case_sha256": hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest(),
        "session_id": session_id, "status": "incomplete", "turns": [],
        "usage_scope": "grok session files; HTTP wire unknown",
        "http_wire": "unknown",
    }
    try:
        report["client_version"] = subprocess.check_output(
            ["grok", "--version"], text=True, env=grok_env()
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        report["error"] = f"grok version: {exc}"
        (out / "run.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return report
    runner = grok_run or subprocess.run
    try:
        for index, turn in enumerate(case["turns"]):
            write_files(turn.get("write_files", {}))
            prompt = "/compact" if turn.get("compact") else expand(turn["request"])
            if index == 0 and not turn.get("compact"):
                prompt = f"Use {owner} from {entry} for this task.\n\n{prompt}"
            args = (
                create_args(prompt, workspace, session_id)
                if index == 0 else resume_args(prompt, workspace, session_id)
            )
            row = {"index": index, "kind": "compact" if turn.get("compact") else "request", "argv_mode": args[3]}
            completed = runner(args, cwd=str(workspace), env=grok_env(), capture_output=True, text=True, timeout=timeout)
            (out / f"turn-{index:03d}.json").write_text(completed.stdout or "", encoding="utf-8")
            row["returncode"] = completed.returncode
            report["turns"].append(row)
            copy_session(captured, out / "session")
            copy_session(captured, out / f"session-{index:03d}")
            if completed.returncode != 0:
                row["stderr"] = (completed.stderr or "")[-2000:]
                raise RuntimeError(f"grok turn {index} failed")
        report["status"] = "executed"
        if (out / "session").is_dir():
            report["session"] = parse_session(out / "session")
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, KeyError) as exc:
        report["error"] = str(exc)
    snapshots = [
        out / f"session-{index:03d}"
        for index in range(len(report["turns"]))
        if (out / f"session-{index:03d}").is_dir()
    ]
    report["injection_compare"] = compare_snapshots(snapshots)
    (out / "run.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def load_continuations(root):
    data = json.loads((Path(root) / "evals/skill-load-paths.json").read_text(encoding="utf-8"))
    return data["continuations"]


def coverage_plan(continuations):
    plan = []
    for scenario in continuations:
        if not scenario.get("executable"):
            continue
        plan.append((scenario["id"], "run-1"))
        if scenario["id"] == HOST_COMPACTION:
            plan.append((scenario["id"], "run-2"))
    return plan


def classify_coverage(scenario_id, report):
    error = report.get("error")
    if report.get("status") == "executed":
        if scenario_id == HOST_COMPACTION and not (report.get("session") or {}).get("host_compaction"):
            return "failed", "host_compaction_not_observed"
        return "executed", None
    if error and str(error).startswith("grok version"):
        return "unexecuted", str(error)
    return "failed", str(error or "incomplete")


def run_coverage(root, skill_root, out_root, timeout, grok_home=None, grok_run=None):
    root = Path(root)
    out_root = Path(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    continuations = load_continuations(root)
    by_id = {scenario["id"]: scenario for scenario in continuations}
    rows = []
    for case_id, run_name in coverage_plan(continuations):
        scenario = by_id[case_id]
        executable = root / scenario["executable"]
        out = out_root / case_id / run_name
        row = {
            "id": case_id,
            "run": run_name,
            "executable": scenario["executable"],
            "status": "unexecuted",
            "reason": None,
            "http_wire": "unknown",
        }
        try:
            case = json.loads(executable.read_text(encoding="utf-8"))
            report = run_case(
                case, skill_root, out, timeout, grok_home=grok_home, grok_run=grok_run,
            )
            row["status"], row["reason"] = classify_coverage(case_id, report)
            session = report.get("session") or {}
            row["host_compaction"] = bool(session.get("host_compaction"))
            row["usage_status"] = (session.get("usage") or {}).get("status")
        except (OSError, ValueError, KeyError, json.JSONDecodeError, FileExistsError) as exc:
            row["status"] = "failed"
            row["reason"] = str(exc)
        rows.append(row)
        print(f"coverage {case_id}/{run_name}: {row['status']}", flush=True)
    coverage = {
        "host": "grok",
        "http_wire": "unknown",
        "note": "No general reliability claim from n=1. No token savings.",
        "rows": rows,
    }
    (out_root / "coverage.json").write_text(
        json.dumps(coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return coverage


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?", type=Path)
    parser.add_argument("--all", action="store_true", help="run every executable continuation")
    parser.add_argument("--skill-root", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--execute", action="store_true", help="explicitly permit paid grok turns")
    parser.add_argument("--turn-timeout", type=int, default=600)
    parser.add_argument("--grok-home", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    if not args.execute:
        parser.error("real model calls require --execute; offline CI must not invoke this runner")
    if args.turn_timeout <= 0:
        parser.error("turn timeout must be positive")
    if args.all == bool(args.task):
        parser.error("provide a case path or --all")
    try:
        if args.all:
            coverage = run_coverage(
                args.repo_root.resolve(), args.skill_root.resolve(), args.out_dir.resolve(),
                args.turn_timeout, grok_home=args.grok_home,
            )
            print(f"coverage evidence: {args.out_dir / 'coverage.json'}", flush=True)
            return 0 if all(row["status"] == "executed" for row in coverage["rows"]) else 1
        case = json.loads(args.task.read_text(encoding="utf-8"))
        report = run_case(
            case, args.skill_root.resolve(), args.out_dir.resolve(),
            args.turn_timeout, grok_home=args.grok_home,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(f"run status: {report['status']}; evidence: {args.out_dir / 'run.json'}", flush=True)
    return 0 if report["status"] == "executed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
