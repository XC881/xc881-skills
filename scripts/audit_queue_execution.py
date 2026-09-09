#!/usr/bin/env python3
"""Opt-in maintenance audit of before/after queue fixtures, never a runtime gate."""

import argparse
import json
from pathlib import Path
import re

ITEM_STATES = {"pending", "ready", "blocked", "done", "skipped"}
TASK_STATES = {"draft", "ready", "in-progress", "blocked", "done", "cancelled", "superseded"}
ITEM_PROGRESS = re.compile(
    r"\b(Q-\d+):\s*(?:in-progress\b|(?:pending|ready|blocked|done|skipped)\s*->\s*in-progress\b)"
)
VALIDATOR_RE = re.compile(r"validate_(?:req|cross)_process\.py")


def field(text, name):
    matches = re.findall(r"^" + re.escape(name) + r":\s*`([^`\n]+)`\s*$", text, re.MULTILINE)
    return matches[0] if len(matches) == 1 else None


def snapshot(artifact):
    return {
        "current": (artifact / "current.md").read_text(encoding="utf-8"),
        "history": (artifact / "history.md").read_text(encoding="utf-8"),
        "items": {str(path.relative_to(artifact)): path.read_text(encoding="utf-8")
                  for path in sorted((artifact / "queue").glob("Q-*.md"))},
    }


def audit_checkpoint(before, after):
    violations = []
    current = after["current"]
    state = field(current, "State")
    if state not in TASK_STATES:
        violations.append("invalid_task_state")
    if not field(current, "Task") or field(before["current"], "Task") != field(current, "Task"):
        violations.append("task_identity_changed_or_missing")
    items = after["items"]
    ids = {}
    for path, text in items.items():
        item_id, status = field(text, "ID"), field(text, "Status")
        if not item_id or not re.fullmatch(r"Q-\d+", item_id) or item_id in ids:
            violations.append(f"invalid_item_id:{path}")
        ids[item_id] = path
        if status not in ITEM_STATES:
            violations.append(f"invalid_item_state:{path}")
    for name in ("Previous", "Current", "Next"):
        pointer = field(current, name)
        if pointer != "none" and pointer not in items:
            violations.append(f"invalid_pointer:{name}")
    active, following = field(current, "Current"), field(current, "Next")
    if state in {"ready", "in-progress", "blocked"} and active not in items:
        violations.append("active_task_without_current")
    if active in items:
        status = field(items[active], "Status")
        if status in {"done", "skipped"}:
            violations.append("current_item_already_terminal")
        if state == "blocked" and status != "blocked":
            violations.append("blocked_task_item_disagree")
        if state in {"ready", "in-progress"} and status == "blocked":
            violations.append("runnable_task_has_blocked_current")
        expected_next = field(items[active], "Next")
        if following != ("none" if expected_next == "none" else ids.get(expected_next)):
            violations.append("next_pointer_disagrees_with_current_item")
    if state == "done" and (active != "none" or following != "none" or any(
        field(text, "Status") not in {"done", "skipped"} for text in items.values()
    )):
        violations.append("premature_task_done")
    counts = re.findall(r"^- Implementation queue: done (\d+) / total (\d+)\s*$", current, re.MULTILINE)
    expected_counts = (sum(field(text, "Status") == "done" for text in items.values()), len(items))
    if len(counts) != 1 or tuple(map(int, counts[0])) != expected_counts:
        violations.append("implementation_counts_disagree")

    old_history, history = before["history"], after["history"]
    if not history.startswith(old_history):
        violations.append("history_not_append_only")
        added = ""
    else:
        added = history[len(old_history):]
    lines = [line.replace("`", "") for line in added.splitlines() if line.strip()]
    replay = {field(text, "ID"): field(text, "Status") for text in before["items"].values()}
    edges = []
    item_states = "|".join(sorted(ITEM_STATES))
    edge_pattern = re.compile(r"\b(Q-\d+):\s*(" + item_states + r")\s*->\s*(" + item_states + r")\b")
    for line in lines:
        for match in ITEM_PROGRESS.finditer(line):
            violations.append(f"item_in_progress_history:{match.group(1)}")
        for match in edge_pattern.finditer(line):
            item_id, old, new = match.groups()
            edges.append((item_id, old, new))
            if item_id not in ids or old == new or (item_id in replay and replay[item_id] != old):
                violations.append(f"history_state_discontinuity:{item_id}")
            replay[item_id] = new
    changed = []
    for path, old_text in before["items"].items():
        if path not in items:
            violations.append(f"item_removed:{path}")
            continue
        old, new = field(old_text, "Status"), field(items[path], "Status")
        item_id = field(old_text, "ID")
        if old != new:
            changed.append(item_id)
        if replay.get(item_id) != new:
            violations.append(f"missing_history_transition:{item_id}:{old}->{new}")
    pointers_changed = any(field(before["current"], name) != field(current, name)
                           for name in ("State", "Current", "Next", "Previous"))
    if (changed or pointers_changed) and not lines:
        violations.append("missing_checkpoint_history")
    old_state = field(before["current"], "State")
    if not edges and old_state != state:
        task_name = re.escape(str(field(current, "Task")))
        task_edge = r"(?:\btask(?:\s+state)?|" + task_name + r")\s*:?\s*" + re.escape(str(old_state)) + r"\s*->\s*" + re.escape(str(state)) + r"\b"
        if not any(re.search(task_edge, line, re.IGNORECASE) for line in lines):
            violations.append("missing_task_state_history_transition")
    if changed or pointers_changed or edges:
        active_id = field(items[active], "ID") if active in items else "none"
        states = "|".join(sorted(TASK_STATES))
        task_pattern = re.compile(r"\btask(?:\s+state)?\s*[:=]?\s*(?:((?:" + states + r"))\s*->\s*)?(" + states + r")\b", re.IGNORECASE)
        pointer_pattern = re.compile(r"\bcurrent\s*[:=]?\s*(?:(?:Q-\d+|none)\s*->\s*)?(Q-\d+|none)\b", re.IGNORECASE)
        task_matches = [match for line in lines for match in task_pattern.finditer(line)]
        pointer_matches = [match for line in lines for match in pointer_pattern.finditer(line)]
        if not task_matches or task_matches[-1][2] != state or not pointer_matches or pointer_matches[-1][1] != active_id:
            violations.append("missing_history_current_or_task_state")
    if not changed and not pointers_changed and not edges and added.strip():
        violations.append("history_without_state_transition")
    return violations


def audit_snapshots(snapshots):
    if not snapshots:
        return ["empty_snapshots"]
    violations = []
    for index, state in enumerate(snapshots):
        for path, text in state["items"].items():
            if field(text, "Status") not in ITEM_STATES:
                violations.append(f"invalid_item_state:{path}:snapshot:{index}")
        if index:
            violations.extend(f"snapshot:{index}:{item}" for item in audit_checkpoint(snapshots[index - 1], state))
    return violations


def commands_from_events(events):
    commands = []
    for event in events:
        item = event.get("params", {}).get("item") if event.get("method") == "item/completed" else None
        if isinstance(item, dict) and item.get("type") == "commandExecution" and isinstance(item.get("command"), str):
            commands.append(item["command"])
    return commands


def _is_write(command):
    return "apply_patch" in command or "*** Update File:" in command or "*** Add File:" in command


def audit_tool_activity(commands, artifact, required_reads=()):
    violations = []
    joined = "\n".join(commands)
    artifact = artifact.rstrip("/")
    if any(f"{artifact}/index.md" in command and not _is_write(command) for command in commands):
        violations.append("index_scan")
    if any(VALIDATOR_RE.search(command) for command in commands):
        violations.append("process_validator_call")
    if any("history.md" in command and not _is_write(command) and not re.search(r"\btail\b", command)
           for command in commands):
        violations.append("history_body_read")
    for relative in required_reads:
        if relative not in joined:
            violations.append(f"missing_required_read:{relative}")
    return violations


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="explicit pristine fixture artifact")
    parser.add_argument("after", type=Path, help="explicit executed fixture artifact")
    args = parser.parse_args(argv)
    try:
        violations = audit_checkpoint(snapshot(args.before), snapshot(args.after))
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps({"status": "fail" if violations else "pass", "violations": violations}, indent=2))
    return int(bool(violations))


if __name__ == "__main__":
    raise SystemExit(main())
