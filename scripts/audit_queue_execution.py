#!/usr/bin/env python3
"""Opt-in maintenance audit of queue checkpoints and tool activity."""

import argparse
import json
from pathlib import Path
import re

ITEM_STATES = frozenset({"pending", "ready", "blocked", "done", "skipped"})
TASK_STATES = frozenset({"draft", "ready", "in-progress", "blocked", "done", "cancelled", "superseded"})
STATE_TEXT = "|".join(sorted(ITEM_STATES))
TASK_TEXT = "|".join(sorted(TASK_STATES))
ITEM_EDGE_RE = re.compile(r"\b(Q-\d+):\s*(" + STATE_TEXT + r")\s*->\s*(" + STATE_TEXT + r")\b")
ITEM_IN_PROGRESS_RE = re.compile(r"\b(Q-\d+):\s*(?:in-progress\b|(?:" + STATE_TEXT + r")\s*->\s*in-progress\b)")
TASK_EDGE_RE = re.compile(r"\btask(?:\s+state)?\s*:?\s*(" + TASK_TEXT + r")\s*->\s*(" + TASK_TEXT + r")\b", re.IGNORECASE)
TASK_MARKER_RE = re.compile(r"\btask(?:\s+state)?\s*:?\s*(" + TASK_TEXT + r")\b", re.IGNORECASE)
CURRENT_RE = re.compile(r"\bcurrent\s*:?\s*(Q-\d+|none)\b", re.IGNORECASE)
VALIDATOR_RE = re.compile(r"(?:validate_req_process|validate_cross_process)\.py")


def field(text, name):
    matches = re.findall(
        r"^" + re.escape(name) + r"(?:\s*[（(][^()（）]*[)）])?:\s*(?:`([^`\n]+)`|([^\n]+))\s*$",
        text,
        re.MULTILINE,
    )
    if len(matches) != 1:
        return None
    return (matches[0][0] or matches[0][1]).strip()


def snapshot(artifact):
    artifact = Path(artifact)
    return {
        "current": (artifact / "current.md").read_text(encoding="utf-8"),
        "history": (artifact / "history.md").read_text(encoding="utf-8"),
        "items": {
            str(path.relative_to(artifact)): path.read_text(encoding="utf-8")
            for path in sorted((artifact / "queue").glob("Q-*.md"))
        },
    }


def _item_ids(items):
    ids = {}
    violations = []
    for path, text in items.items():
        item_id, status = field(text, "ID"), field(text, "Status")
        if not item_id or not re.fullmatch(r"Q-\d+", item_id) or item_id in ids:
            violations.append(f"invalid_item_id:{path}")
        else:
            ids[item_id] = path
        if status not in ITEM_STATES:
            violations.append(f"invalid_item_state:{path}")
    return ids, violations


def _history_lines(history):
    return [line.replace("`", "") for line in history.splitlines() if line.strip()]


def _parse_history(history):
    rows = []
    for line in _history_lines(history):
        item_edges = list(ITEM_EDGE_RE.finditer(line))
        task_edges = list(TASK_EDGE_RE.finditer(line))
        task_markers = list(TASK_MARKER_RE.finditer(line))
        current = list(CURRENT_RE.finditer(line))
        rows.append({
            "line": line,
            "item_edges": [(match.group(1), match.group(2), match.group(3)) for match in item_edges],
            "task_edges": [(match.group(1).lower(), match.group(2).lower()) for match in task_edges],
            "task_status": (task_edges[-1].group(2).lower() if task_edges else
                            task_markers[-1].group(1).lower() if task_markers else None),
            "current": current[-1].group(1).upper() if current else None,
        })
    return rows


def _history_task_transition(rows, old_state, new_state):
    state = old_state
    edges = []
    violations = []
    for row in rows:
        for old, new in row["task_edges"]:
            edges.append((old, new))
            if old == new or old != state:
                violations.append("history_task_state_discontinuity")
            state = new
    if old_state != new_state and not edges:
        violations.append("missing_task_state_history_transition")
    elif state != new_state:
        violations.append("missing_task_state_history_transition")
    return state, edges, violations


def _history_item_transitions(before, after, rows, ids):
    states = {field(text, "ID"): field(text, "Status") for text in before["items"].values()}
    after_states = {field(text, "ID"): field(text, "Status") for text in after["items"].values()}
    violations = []
    edges = []
    for row in rows:
        for match in ITEM_IN_PROGRESS_RE.finditer(row["line"]):
            violations.append(f"item_in_progress_history:{match.group(1)}")
        for item_id, old, new in row["item_edges"]:
            edges.append((item_id, old, new))
            expected = states.get(item_id, "pending")
            if item_id not in ids or old == new or expected != old:
                violations.append(f"history_state_discontinuity:{item_id}")
            states[item_id] = new
    for item_id, status in after_states.items():
        if item_id not in states:
            # A newly appended item has no prior state and needs no artificial
            # pending -> ready history entry.
            states[item_id] = status
        elif states[item_id] != status:
            old = next((field(text, "Status") for text in before["items"].values()
                        if field(text, "ID") == item_id), states[item_id])
            violations.append(f"missing_history_transition:{item_id}:{old}->{status}")
    for item_id in set(states) - set(after_states):
        violations.append(f"item_removed:{item_id}")
    return edges, violations


def _checkpoint_marker(rows, task_state, current_id):
    current_id = current_id.upper()
    if not rows:
        return False
    row = rows[-1]
    return row["current"] == current_id and row["task_status"] == task_state


def _validate_shape(state):
    violations = []
    current = state["current"]
    task_state = field(current, "State")
    task_id = field(current, "Task")
    ids, item_violations = _item_ids(state["items"])
    violations.extend(item_violations)
    if task_state not in TASK_STATES:
        violations.append("invalid_task_state")
    if not task_id:
        violations.append("task_identity_changed_or_missing")
    pointers = {name: field(current, name) for name in ("Previous", "Current", "Next")}
    for name, pointer in pointers.items():
        if pointer != "none" and pointer not in state["items"]:
            violations.append(f"invalid_pointer:{name}")
    for path, text in state["items"].items():
        item_id = field(text, "ID")
        previous = field(text, "Previous")
        following = field(text, "Next")
        if previous not in (None, "none") and previous not in ids:
            violations.append(f"invalid_item_previous:{path}")
        if following not in (None, "none") and following not in ids:
            violations.append(f"invalid_item_next:{path}")
        if previous in ids and field(state["items"][ids[previous]], "Next") not in (None, item_id):
            violations.append(f"broken_item_previous_link:{path}")
        if following in ids and field(state["items"][ids[following]], "Previous") not in (None, item_id):
            violations.append(f"broken_item_next_link:{path}")
    active, following = pointers["Current"], pointers["Next"]
    if task_state not in {"done", "cancelled", "superseded"} and active not in state["items"]:
        violations.append("active_task_without_current")
    if active in state["items"]:
        status = field(state["items"][active], "Status")
        if status in {"done", "skipped"}:
            violations.append("current_item_already_terminal")
        if task_state == "blocked" and status != "blocked":
            violations.append("blocked_task_item_disagree")
        if task_state in {"ready", "in-progress"} and status == "blocked":
            violations.append("runnable_task_has_blocked_current")
        expected_next = field(state["items"][active], "Next")
        if expected_next not in (None, "none") and expected_next not in ids:
            violations.append("current_item_next_missing")
        expected_path = "none" if expected_next in (None, "none") else ids.get(expected_next)
        if following != expected_path:
            violations.append("next_pointer_disagrees_with_current_item")
    if task_state in {"done", "cancelled", "superseded"} and (active != "none" or following != "none"):
        violations.append("terminal_task_has_active_pointer")
    if task_state == "done" and (active != "none" or following != "none" or any(
        field(text, "Status") not in {"done", "skipped"} for text in state["items"].values()
    )):
        violations.append("premature_task_done")
    counts = re.findall(r"^- Implementation queue: done (\d+) / total (\d+)\s*$", current, re.MULTILINE)
    completed = sum(field(text, "Status") in {"done", "skipped"} for text in state["items"].values())
    if len(counts) != 1 or tuple(map(int, counts[0])) != (completed, len(state["items"])):
        violations.append("implementation_counts_disagree")
    return violations, ids, task_state, pointers


def audit_checkpoint(before, after):
    """Audit one coherent before/after checkpoint, including history replay."""
    violations, ids, task_state, pointers = _validate_shape(after)
    if field(before["current"], "Task") != field(after["current"], "Task"):
        violations.append("task_identity_changed_or_missing")

    old_history, new_history = before["history"], after["history"]
    if not new_history.startswith(old_history):
        violations.append("history_not_append_only")
        added = []
    else:
        added = _parse_history(new_history[len(old_history):])

    item_edges, item_violations = _history_item_transitions(before, after, added, ids)
    violations.extend(item_violations)
    old_task, new_task = field(before["current"], "State"), task_state
    _, task_edges, task_violations = _history_task_transition(added, old_task, new_task)
    violations.extend(task_violations)

    changed_items = []
    before_by_id = {field(text, "ID"): field(text, "Status") for text in before["items"].values()}
    after_by_id = {field(text, "ID"): field(text, "Status") for text in after["items"].values()}
    for item_id, old in before_by_id.items():
        new = after_by_id.get(item_id)
        if new != old:
            changed_items.append(item_id)
        if item_id in after_by_id and not any(edge[0] == item_id for edge in item_edges) and new != old:
            violations.append(f"missing_history_transition:{item_id}:{old}->{new}")

    state_changed = field(before["current"], "State") != new_task
    pointer_changed = state_changed or any(
        field(before["current"], name) != pointers[name]
        for name in ("Current", "Next", "Previous")
    )
    if changed_items or pointer_changed or item_edges or task_edges:
        active_path = pointers["Current"]
        active_id = field(after["items"][active_path], "ID") if active_path in after["items"] else "none"
        if not _checkpoint_marker(added, new_task, active_id):
            violations.append("missing_history_current_or_task_state")
    if not changed_items and not pointer_changed and not item_edges and not task_edges and added:
        violations.append("history_without_state_transition")
    return violations


def audit_snapshots(snapshots):
    if not snapshots:
        return ["empty_snapshots"]
    violations = []
    for index, state in enumerate(snapshots):
        shape, _, _, _ = _validate_shape(state)
        violations.extend(f"snapshot:{index}:{item}" for item in shape)
        if index:
            violations.extend(f"snapshot:{index}:{item}" for item in audit_checkpoint(snapshots[index - 1], state))
    return violations


def commands_from_events(events):
    return [record["command"] for record in command_records_from_events(events)]


def command_records_from_events(events):
    records = []
    for event in events:
        if event.get("method") != "item/completed":
            continue
        params = event.get("params") or {}
        item = params.get("item") or {}
        if item.get("type") == "commandExecution" and isinstance(item.get("command"), str):
            records.append({"turn_id": params.get("turnId"), "command": item["command"], "status": item.get("status")})
    return records


def _is_write(command):
    return "apply_patch" in command or "*** Update File:" in command or "*** Add File:" in command


def _contains_path(command, path):
    return re.search(
        r"(?<![A-Za-z0-9_.-])" + re.escape(path) + r"(?![A-Za-z0-9_.-])",
        command,
    ) is not None


def audit_tool_activity(commands, artifact, required_reads=()):
    """Check read/write discipline against the current window."""
    violations = []
    normalized = []
    for item in commands:
        command = item.get("command") if isinstance(item, dict) else item
        if not isinstance(command, str):
            violations.append("malformed_command_record")
            continue
        normalized.append(command)
    artifact = artifact.rstrip("/")
    for command in normalized:
        if _contains_path(command, f"{artifact}/index.md") and not _is_write(command):
            violations.append("index_scan")
        if VALIDATOR_RE.search(command) and not _is_write(command):
            violations.append("process_validator_call")
        if _contains_path(command, f"{artifact}/history.md") and not _is_write(command) and not re.search(
            r"\b(?:tail|sed)\b[^\n;]*" + re.escape(artifact) + r"/history\.md", command
        ):
            violations.append("history_body_read")
    joined = "\n".join(normalized)
    for relative in required_reads:
        if not _contains_path(joined, relative):
            violations.append(f"missing_required_read:{relative}")
    return sorted(set(violations))


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
