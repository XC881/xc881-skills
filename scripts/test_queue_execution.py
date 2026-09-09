#!/usr/bin/env python3
import copy
import json
import unittest

from pathlib import Path

from audit_queue_execution import (
    audit_checkpoint, audit_snapshots, audit_tool_activity, commands_from_events,
)

ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "skills/xc881-coding-skills"


def item(item_id, status, following="none"):
    return f"ID: `{item_id}`\nStatus: `{status}`\nNext: `{following}`\n"


def current(state="ready", active="queue/Q-010-one.md", following="queue/Q-020-two.md", done=0, previous="none"):
    return f"Task: `RP-EVAL`\nState: `{state}`\nPrevious: `{previous}`\nCurrent: `{active}`\nNext: `{following}`\n- Implementation queue: done {done} / total 2\n"


def initial():
    return {"current": current(), "history": "# History\n\n- created\n", "items": {
        "queue/Q-010-one.md": item("Q-010", "ready", "Q-020"),
        "queue/Q-020-two.md": item("Q-020", "pending"),
    }}


def completed():
    data = initial()
    data["current"] = current("done", "none", "none", 2, "queue/Q-020-two.md")
    data["items"]["queue/Q-010-one.md"] = item("Q-010", "done", "Q-020")
    data["items"]["queue/Q-020-two.md"] = item("Q-020", "done")
    data["history"] += "- Q-010: ready -> done; current Q-020; task in-progress\n- Q-020: pending -> done; current none; task done\n"
    return data


class QueueAuditTests(unittest.TestCase):
    def test_completed_queue(self):
        self.assertEqual(audit_checkpoint(initial(), completed()), [])

    def test_old_missing_history_defect(self):
        after = completed()
        after["history"] = initial()["history"]
        failures = audit_checkpoint(initial(), after)
        self.assertIn("missing_history_transition:Q-010:ready->done", failures)
        self.assertIn("missing_history_transition:Q-020:pending->done", failures)

    def test_sequential_advancement_and_task_start(self):
        started = initial()
        started["current"] = current("in-progress")
        started["history"] += "- task ready -> in-progress; current Q-010\n"
        self.assertEqual(audit_checkpoint(initial(), started), [])
        advanced = copy.deepcopy(started)
        advanced["current"] = current("in-progress", "queue/Q-020-two.md", "none", 1, "queue/Q-010-one.md")
        advanced["items"]["queue/Q-010-one.md"] = item("Q-010", "done", "Q-020")
        advanced["history"] += "- Q-010: ready -> done; current Q-020; task in-progress\n"
        self.assertEqual(audit_checkpoint(started, advanced), [])

    def test_task_start_needs_a_transition_not_just_an_end_state(self):
        after = initial()
        after["current"] = current("in-progress")
        after["history"] += "- current Q-010; task in-progress\n"
        self.assertIn("missing_task_state_history_transition", audit_checkpoint(initial(), after))

    def test_block_and_resume(self):
        blocked = initial()
        blocked["current"] = current("blocked")
        blocked["items"]["queue/Q-010-one.md"] = item("Q-010", "blocked", "Q-020")
        blocked["history"] += "- Q-010: ready -> blocked; current Q-010; task blocked; needs user decision\n"
        self.assertEqual(audit_checkpoint(initial(), blocked), [])
        resumed = copy.deepcopy(blocked)
        resumed["current"] = current("in-progress")
        resumed["items"]["queue/Q-010-one.md"] = item("Q-010", "ready", "Q-020")
        resumed["history"] += "- Q-010: blocked -> ready; current Q-010; task in-progress\n"
        self.assertEqual(audit_checkpoint(blocked, resumed), [])

    def test_reopen_preserves_completed_items(self):
        before = completed()
        after = copy.deepcopy(before)
        after["items"]["queue/Q-030-three.md"] = item("Q-030", "ready")
        after["current"] = current("ready", "queue/Q-030-three.md", "none", 2, "queue/Q-020-two.md").replace("total 2", "total 3")
        after["history"] += "- task done -> ready; current Q-030; reopened accepted follow-up\n"
        self.assertEqual(audit_checkpoint(before, after), [])

    def test_complete_history_replays_intermediate_block_and_resume(self):
        after = completed()
        after["history"] = after["history"].replace(
            "- Q-020: pending -> done; current none; task done",
            "- Q-020: pending -> blocked; current Q-020; task blocked\n"
            "- Q-020: blocked -> ready; current Q-020; task in-progress\n"
            "- Q-020: ready -> done; current none; task done",
        )
        self.assertEqual(audit_checkpoint(initial(), after), [])

    def test_net_unchanged_state_can_have_real_intermediate_edges(self):
        before = initial()
        after = copy.deepcopy(before)
        after["history"] += "- Q-010: ready -> blocked; current Q-010; task blocked\n- Q-010: blocked -> ready; current Q-010; task ready\n"
        self.assertEqual(audit_checkpoint(before, after), [])

    def test_nontransition_does_not_append_duplicate_history(self):
        self.assertEqual(audit_checkpoint(completed(), completed()), [])
        after = completed()
        after["history"] += "- Q-020: pending -> done; current none; task done\n"
        self.assertIn("history_state_discontinuity:Q-020", audit_checkpoint(completed(), after))

    def test_negative_mutations(self):
        mutations = {
            "counts": lambda data: data.update(current=data["current"].replace("done 2", "done 1")),
            "history_rewrite": lambda data: data.update(history=data["history"].replace("- created", "- rewritten")),
            "pointer": lambda data: data.update(current=data["current"].replace("Current: `none`", "Current: `../../elsewhere`")),
            "unfinished_item": lambda data: data["items"].update({"queue/Q-020-two.md": item("Q-020", "ready")}),
            "removed_item": lambda data: data["items"].pop("queue/Q-020-two.md"),
            "missing_task": lambda data: data.update(current=data["current"].replace("Task: `RP-EVAL`", "")),
            "missing_history_pointer": lambda data: data.update(history=data["history"].replace("current none", "current Q-020")),
            "duplicate_edge": lambda data: data.update(history=data["history"] + "- Q-020: pending -> done; current none; task done\n"),
            "duplicate_id": lambda data: data["items"].update({"queue/Q-020-two.md": item("Q-010", "done")}),
            "broken_edge_chain": lambda data: data.update(history=data["history"].replace("pending -> done", "blocked -> done")),
            "stale_task_state": lambda data: data.update(history=data["history"].replace("task done", "task done -> in-progress")),
        }
        for name, mutate in mutations.items():
            data = completed()
            mutate(data)
            with self.subTest(name=name):
                self.assertTrue(audit_checkpoint(initial(), data))

    def test_item_status_cannot_be_in_progress(self):
        after = initial()
        after["current"] = current("in-progress", "queue/Q-020-two.md", "none", 1, "queue/Q-010-one.md")
        after["items"]["queue/Q-010-one.md"] = item("Q-010", "done", "Q-020")
        after["items"]["queue/Q-020-two.md"] = item("Q-020", "in-progress")
        after["history"] += (
            "- Q-010: ready -> done; current Q-020; task in-progress\n"
            "- Q-020: pending -> in-progress; current Q-020; task in-progress\n"
        )
        failures = audit_checkpoint(initial(), after)
        self.assertIn("invalid_item_state:queue/Q-020-two.md", failures)
        self.assertIn("item_in_progress_history:Q-020", failures)

    def test_final_done_does_not_hide_item_in_progress(self):
        blocked = initial()
        blocked["current"] = current("blocked", "queue/Q-020-two.md", "none", 1, "queue/Q-010-one.md")
        blocked["items"]["queue/Q-010-one.md"] = item("Q-010", "done", "Q-020")
        blocked["items"]["queue/Q-020-two.md"] = item("Q-020", "blocked")
        blocked["history"] += (
            "- Q-010: ready -> done; current Q-020; task in-progress\n"
            "- Q-020: pending -> blocked; current Q-020; task blocked\n"
        )
        self.assertEqual(audit_checkpoint(initial(), blocked), [])
        resumed = copy.deepcopy(blocked)
        resumed["current"] = current("in-progress", "queue/Q-020-two.md", "none", 1, "queue/Q-010-one.md")
        resumed["items"]["queue/Q-020-two.md"] = item("Q-020", "in-progress")
        resumed["history"] += "- Q-020: blocked -> in-progress; current Q-020; task in-progress\n"
        finished = copy.deepcopy(resumed)
        finished["current"] = current("done", "none", "none", 2, "queue/Q-020-two.md")
        finished["items"]["queue/Q-020-two.md"] = item("Q-020", "done")
        finished["history"] += "- Q-020: in-progress -> done; current none; task done\n"
        failures = audit_snapshots([initial(), blocked, resumed, finished])
        self.assertTrue(any("invalid_item_state:queue/Q-020-two.md" in item for item in failures))
        self.assertTrue(any("item_in_progress_history:Q-020" in item for item in failures))
        correct = copy.deepcopy(blocked)
        correct["current"] = current("in-progress", "queue/Q-020-two.md", "none", 1, "queue/Q-010-one.md")
        correct["items"]["queue/Q-020-two.md"] = item("Q-020", "ready")
        correct["history"] += "- Q-020: blocked -> ready; current Q-020; task in-progress\n"
        done = copy.deepcopy(correct)
        done["current"] = current("done", "none", "none", 2, "queue/Q-020-two.md")
        done["items"]["queue/Q-020-two.md"] = item("Q-020", "done")
        done["history"] += "- Q-020: ready -> done; current none; task done\n"
        self.assertEqual(audit_snapshots([initial(), blocked, correct, done]), [])

    def test_tool_activity_requires_current_window_and_rejects_scans(self):
        artifact = "dev-notes/req-process/labels"
        current_item = "queue/Q-010-trim.md"
        allowed = [
            "/bin/bash -lc 'rtk read dev-notes/req-process/labels/current.md'",
            "/bin/bash -lc 'rtk read dev-notes/req-process/labels/queue/Q-010-trim.md'",
            "/bin/bash -lc 'rtk proxy tail -n 5 dev-notes/req-process/labels/history.md'",
            "/bin/bash -lc \"rtk proxy apply_patch <<'PATCH'\\n*** Update File: "
            "dev-notes/req-process/labels/history.md\\n@@\\n+line\\nPATCH\"",
        ]
        self.assertEqual(audit_tool_activity(
            allowed, artifact, required_reads=("current.md", current_item)), [])
        events = [
            {"method": "item/completed", "params": {"item": {
                "type": "commandExecution",
                "command": "/bin/bash -lc 'rtk read dev-notes/req-process/labels/index.md'",
            }}},
            {"method": "item/completed", "params": {"item": {
                "type": "commandExecution",
                "command": "/bin/bash -lc 'rtk read skills/xc881-requirement-analysis/scripts/validate_req_process.py'",
            }}},
            {"method": "item/completed", "params": {"item": {
                "type": "commandExecution",
                "command": "/bin/bash -lc 'rtk read dev-notes/req-process/labels/history.md'",
            }}},
        ]
        failures = audit_tool_activity(commands_from_events(events), artifact, required_reads=("current.md",))
        self.assertEqual(set(failures), {
            "index_scan", "process_validator_call", "history_body_read", "missing_required_read:current.md",
        })

    def test_entry_and_eval_fixture_forbid_item_in_progress(self):
        skill = (CODING / "SKILL.md").read_text(encoding="utf-8")
        checkpoint = (CODING / "references/execution-checkpoint-and-tool-policy.md").read_text(encoding="utf-8")
        execution = (CODING / "references/requirement-artifact-execution.md").read_text(encoding="utf-8")
        self.assertIn("never `in-progress`", skill)
        self.assertIn("never `in-progress`", checkpoint)
        self.assertIn("Item `Status` is only `pending | ready | blocked | done | skipped`, never", execution)
        case = json.loads((ROOT / "evals/queue-execution/block-compact-resume.json").read_text(encoding="utf-8"))
        continuous = json.loads((ROOT / "evals/queue-execution/two-item-continuous.json").read_text(encoding="utf-8"))
        self.assertEqual(case["id"], "queue-block-compact-resume")
        self.assertEqual(case["owner"], "xc881-coding-skills")
        self.assertTrue(any(turn.get("compact") for turn in case["turns"]))
        self.assertEqual(continuous["id"], "queue-two-item-continuous")
        q020 = case["files"]["dev-notes/req-process/labels/queue/Q-020-empty.md"]
        self.assertIn("Status: `pending`", q020)
        self.assertNotIn("Status: `in-progress`", q020)


if __name__ == "__main__":
    unittest.main()
