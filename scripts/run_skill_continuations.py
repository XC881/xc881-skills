#!/usr/bin/env python3
"""Opt-in real Codex app-server turns in a fresh isolated evaluation workspace."""

import argparse
import hashlib
import json
from pathlib import Path
import queue
import re
import shutil
from string import Template
import subprocess
import tempfile
import threading
import time

from audit_queue_execution import snapshot
from audit_skill_continuations import attach_usage, load_events


def local_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"expected a contained relative path: {relative}")
    resolved = (root / path).resolve()
    if root.resolve() not in resolved.parents:
        raise ValueError(f"path escapes evaluation root: {relative}")
    return resolved


def retained_event(event):
    method = event.get("method")
    if method in {"turn/started", "turn/completed"}:
        params = event["params"]
        turn = params["turn"]
        return {"method": method, "params": {"threadId": params["threadId"], "turn": {
            key: turn.get(key) for key in ("id", "status", "error", "startedAt", "completedAt", "durationMs")
        }}}
    if method == "thread/tokenUsage/updated":
        return event
    if method == "item/completed":
        item = event["params"].get("item", {})
        if item.get("type") in {"agentMessage", "commandExecution", "fileChange", "contextCompaction", "collabAgentToolCall"}:
            return event
    if method in {"error", "thread/compacted"}:
        return event
    return None


class AppServer:
    def __init__(self, cwd, record):
        self.record = record
        self.inbox = queue.Queue()
        self.sequence = 0
        self.stderr = tempfile.TemporaryFile()
        self.process = subprocess.Popen(
            ["codex", "app-server", "--listen", "stdio://"], cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr,
            text=True, encoding="utf-8",
        )
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        for line in self.process.stdout:
            try:
                self.inbox.put(json.loads(line))
            except json.JSONDecodeError:
                self.inbox.put({"protocol_error": "non-JSON app-server stdout"})
        self.inbox.put({"protocol_error": "app-server stream closed"})

    def notify(self, method, params=None):
        message = {"method": method}
        if params is not None:
            message["params"] = params
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params, timeout=60):
        self.sequence += 1
        message = {"id": self.sequence, "method": method, "params": params}
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()
        response = self.wait(lambda event: event.get("id") == self.sequence, timeout)
        if "error" in response:
            raise RuntimeError(f"{method}: {response['error']}")
        return response["result"]

    def wait(self, predicate, timeout):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                event = self.inbox.get(timeout=min(30, deadline - time.monotonic()))
            except queue.Empty:
                print(f"waiting for the same live app-server pid={self.process.pid}", flush=True)
                if self.process.poll() is not None:
                    raise RuntimeError("app server exited before completion")
                continue
            if "protocol_error" in event:
                raise RuntimeError(event["protocol_error"])
            if "method" in event and "id" in event:
                # A test never grants a new permission or fabricates missing user input.
                self.process.stdin.write(json.dumps({"id": event["id"], "error": {
                    "code": -32000, "message": "Unattended evaluation cannot grant approval or answer input requests",
                }}) + "\n")
                self.process.stdin.flush()
                self.record({"method": "evaluation/unansweredRequest", "params": {"method": event["method"]}})
            selected = retained_event(event)
            if selected:
                self.record(selected)
            if predicate(event):
                return event
        raise TimeoutError("evaluation deadline reached; do not restart this turn as a successful retry")

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        self.reader.join(timeout=2)
        self.process.stdin.close()
        self.process.stdout.close()
        self.stderr.close()


def run_case(case, skill_root, out, timeout):
    owner = case["owner"]
    if not re.fullmatch(r"xc881-[a-z0-9-]+", owner):
        raise ValueError("invalid skill owner")
    source_skill = local_path(skill_root, owner)
    if not (source_skill / "SKILL.md").is_file():
        raise ValueError(f"missing skill entry: {source_skill}")
    if any(path.is_symlink() for path in source_skill.rglob("*")):
        raise ValueError("skill snapshot must not contain symlinks")
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
    artifact = local_path(workspace, case["queue_artifact"]) if case.get("queue_artifact") else None
    state_snapshots = []

    def checkpoint():
        if artifact:
            state = snapshot(artifact)
            if not state_snapshots or state != state_snapshots[-1]:
                state_snapshots.append(state)
                (out / f"state-{len(state_snapshots) - 1:03d}.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checkpoint()
    instructions = {str(path.relative_to(skill)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in [entry, *sorted((skill / "references").glob("*.md"))]}
    supplied = []
    for relative in case.get("supplied", []):
        path = local_path(skill, relative)
        if relative not in instructions:
            raise ValueError(f"not an instruction path: {relative}")
        supplied.append(f"Instructions supplied from {path}:\n{path.read_text(encoding='utf-8')}")
    report = {
        "case": case["id"], "owner": owner, "skill_root": str(skill_root),
        "effective_skill": str(skill),
        "instruction_sha256": instructions, "case_sha256": hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest(),
        "client_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "sandbox": "danger-full-access", "approval_policy": "never", "turns": [],
        "status": "incomplete", "usage_scope": "this thread; no claim about unobserved provider payloads or child usage",
    }
    events_path = out / "events.jsonl"
    server = None
    thread_id = None
    with events_path.open("x", encoding="utf-8") as stream:
        def record(event):
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
            stream.flush()
            if event.get("method") == "item/completed":
                item = event["params"].get("item", {})
                if item.get("type") == "fileChange" or (item.get("type") == "commandExecution" and "apply_patch" in item.get("command", "")):
                    checkpoint()

        try:
            server = AppServer(workspace, record)
            initialization = server.request("initialize", {"clientInfo": {"name": "xc881_skill_eval", "version": "1"}, "capabilities": {"experimentalApi": True}})
            report["client_user_agent"] = initialization.get("userAgent")
            server.notify("initialized")
            started = server.request("thread/start", {
                "cwd": str(workspace), "approvalPolicy": "never", "sandbox": "danger-full-access",
                "ephemeral": True,
                "developerInstructions": f"This is a bounded skill evaluation. Project reads/writes are permitted only in {workspace}; selected instructions are in {skill}. Do not inspect other projects, user sessions, credentials or sibling evaluation files. Do not install dependencies, modify git, provider or client configuration. Prefix shell commands with rtk and use apply_patch for manual edits.",
            })
            thread_id = started["thread"]["id"]
            report.update(thread_id=thread_id, model=started.get("model"), model_provider=started.get("modelProvider"))
            for index, turn in enumerate(case["turns"]):
                write_files(turn.get("write_files", {}))
                changed_instructions = {}
                for relative, addition in turn.get("append_instructions", {}).items():
                    if relative not in instructions:
                        raise ValueError(f"not an instruction path: {relative}")
                    path = local_path(skill, relative)
                    path.write_text(path.read_text(encoding="utf-8") + expand(addition), encoding="utf-8")
                    changed_instructions[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
                row = {"index": index, "kind": "compact" if turn.get("compact") else "request", "status": "incomplete"}
                if changed_instructions:
                    row["changed_instruction_sha256"] = changed_instructions
                report["turns"].append(row)
                if turn.get("compact"):
                    server.request("thread/compact/start", {"threadId": thread_id})
                    turn_id = None
                else:
                    text = expand(turn["request"])
                    if index == 0:
                        text = f"Use {owner} from {entry} for this task.\n\n" + "\n\n".join(supplied) + "\n\n" + text
                    inputs = [{"type": "text", "text": text}]
                    if turn.get("invoke"):
                        inputs.append({"type": "skill", "name": owner, "path": str(entry)})
                    started_turn = server.request("turn/start", {"threadId": thread_id, "input": inputs})
                    turn_id = started_turn["turn"]["id"]
                    row["turn_id"] = turn_id
                terminal = server.wait(lambda event: event.get("method") == "turn/completed"
                                       and event["params"]["threadId"] == thread_id
                                       and (turn_id is None or event["params"]["turn"]["id"] == turn_id), timeout)
                finished = terminal["params"]["turn"]
                row.update(turn_id=finished["id"], status=finished["status"], error=finished.get("error"))
                checkpoint()
                print(f"{case['id']} turn {index + 1}: {row['status']} ({row['kind']})", flush=True)
                if row["status"] != "completed":
                    raise RuntimeError("model turn did not complete successfully")
            report["status"] = "executed"
        except (OSError, ValueError, RuntimeError, TimeoutError, KeyError) as exc:
            report["error"] = str(exc)
            if isinstance(exc, TimeoutError) and server and thread_id:
                try:
                    server.request("turn/interrupt", {"threadId": thread_id, "turnId": report["turns"][-1].get("turn_id")}, 10)
                except (OSError, RuntimeError, TimeoutError):
                    pass
        finally:
            if server:
                server.close()
            report["state_snapshots"] = len(state_snapshots)
            if events_path.is_file():
                report.update(attach_usage(report, load_events(events_path)))
            (out / "run.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("--skill-root", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--execute", action="store_true", help="explicitly permit paid model turns using existing Codex authentication")
    parser.add_argument("--turn-timeout", type=int, default=600)
    args = parser.parse_args(argv)
    if not args.execute:
        parser.error("real model calls require --execute; offline CI must not invoke this runner")
    if args.turn_timeout <= 0:
        parser.error("turn timeout must be positive")
    try:
        case = json.loads(args.task.read_text(encoding="utf-8"))
        report = run_case(case, args.skill_root.resolve(), args.out_dir.resolve(), args.turn_timeout)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(f"run status: {report['status']}; evidence: {args.out_dir / 'run.json'}", flush=True)
    return 0 if report["status"] == "executed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
