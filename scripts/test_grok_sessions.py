#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

from audit_grok_sessions import (
    compare_chat_histories,
    compare_session_dirs,
    compare_snapshots,
    host_compaction,
    parse_session,
    parse_usage,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals/grok-sessions"


class GrokSessionParserTests(unittest.TestCase):
    def test_chat_history_accepts_string_and_list_content(self):
        report = parse_session(FIXTURES / "parent-complete")
        types = [row["type"] for row in report["chat_history"]]
        self.assertEqual(types, ["system", "user", "user", "assistant"])
        self.assertIn("Available Skills", report["chat_history"][1]["text"])
        self.assertIn("<user_query>hello</user_query>", report["chat_history"][2]["text"])
        self.assertEqual(report["http_wire"], "unknown")

    def test_complete_usage_and_child_attribution(self):
        report = parse_session(FIXTURES / "parent-complete")
        self.assertEqual(report["usage"]["status"], "complete")
        self.assertEqual(report["usage"]["session"]["totalTokens"], 165)
        self.assertEqual(report["usage"]["modelUsage"]["grok-4.6"]["status"], "complete")
        self.assertEqual(report["usage"]["modelUsage"]["grok-4.6"]["buckets"]["totalTokens"], 165)
        self.assertEqual(len(report["subagents"]), 1)
        child = report["subagents"][0]
        self.assertEqual(child["child_session_id"], "child-a")
        self.assertTrue(child["session_found"])
        self.assertEqual(child["attribution"], "complete")
        self.assertEqual(child["usage"]["status"], "complete")
        self.assertEqual(child["usage"]["session"]["totalTokens"], 38)
        self.assertEqual(child["signals"]["toolCallCount"], 1)

    def test_incomplete_usage_is_not_complete(self):
        report = parse_usage(FIXTURES / "incomplete/usage.json")
        self.assertEqual(report["status"], "incomplete")
        self.assertNotEqual(report["status"], "complete")

    def test_all_zero_usage_is_unknown_not_free(self):
        report = parse_usage(FIXTURES / "zero-unknown/usage.json")
        self.assertEqual(report["status"], "unknown")
        self.assertEqual(report["session"]["totalTokens"], 0)

    def test_missing_child_usage_is_unknown_not_zero(self):
        report = parse_session(FIXTURES / "missing-child")
        self.assertEqual(len(report["subagents"]), 1)
        child = report["subagents"][0]
        self.assertFalse(child["session_found"])
        self.assertEqual(child["attribution"], "missing")
        self.assertEqual(child["usage"]["status"], "missing")
        self.assertIsNone(child["usage"]["session"])
        self.assertIsNone(child["signals"])

    def test_child_dir_without_usage_json_is_missing_not_zero(self):
        report = parse_session(FIXTURES / "parent-child-missing-usage")
        self.assertEqual(report["usage"]["modelUsage"]["grok-4.6"]["buckets"]["totalTokens"], 12)
        child = report["subagents"][0]
        self.assertTrue(child["session_found"])
        self.assertEqual(child["attribution"], "missing")
        self.assertEqual(child["usage"]["status"], "missing")
        self.assertIsNone(child["usage"]["session"])
        self.assertNotEqual(child["usage"]["status"], "complete")
        self.assertEqual(child["signals"]["toolCallCount"], 2)

    def test_host_compaction_ignores_tui_events(self):
        compact = parse_session(FIXTURES / "parent-complete")
        self.assertTrue(compact["host_compaction"])
        self.assertEqual(compact["signals"]["compactionCount"], 1)
        self.assertEqual(compact["compaction_checkpoints"][0]["checkpoint_id"], "cp-1")
        self.assertFalse(host_compaction(FIXTURES / "no-compact"))
        noisy = parse_session(FIXTURES / "no-compact")
        self.assertFalse(noisy["host_compaction"])

    def test_appended_injections_are_repeat_absent_or_unknown(self):
        base = FIXTURES / "injection-compare"
        retained = compare_session_dirs(base / "turn-000", base / "turn-001-absent")
        self.assertEqual(retained["surface"], "chat_history.jsonl")
        self.assertEqual(retained["http_wire"], "unknown")
        self.assertEqual(
            retained["classes"],
            {"system": "absent", "skills": "absent", "rules": "absent"},
        )
        self.assertIn("No token savings", retained["note"])
        self.assertNotIn("chars", json.dumps(retained))
        repeated = compare_session_dirs(base / "turn-000", base / "turn-001-repeat")
        self.assertEqual(
            repeated["classes"],
            {"system": "repeat", "skills": "repeat", "rules": "repeat"},
        )
        rewritten = compare_session_dirs(base / "turn-000", base / "turn-001-rewrite")
        self.assertEqual(
            rewritten["classes"],
            {"system": "unknown", "skills": "unknown", "rules": "unknown"},
        )
        rolled = compare_snapshots([base / "turn-000", base / "turn-001-absent"])
        self.assertEqual(rolled["pairs"][0]["before"], "turn-000")
        self.assertEqual(
            rolled["classes"],
            {"system": "absent", "skills": "absent", "rules": "absent"},
        )
        missing = compare_snapshots([base / "turn-000"])
        self.assertEqual(
            missing["classes"],
            {"system": "unknown", "skills": "unknown", "rules": "unknown"},
        )
        self.assertEqual(missing["http_wire"], "unknown")

    def test_grok_headless_skills_phrase_counts_as_skills(self):
        before = [{"type": "system", "text": "You are Grok 4.6"}]
        after = before + [{
            "type": "user",
            "text": "The following skills are available for use:\n- xc881-coding-skills",
        }]
        result = compare_chat_histories(before, after)
        self.assertEqual(result["classes"]["skills"], "repeat")
        self.assertEqual(result["classes"]["system"], "absent")
        self.assertEqual(result["http_wire"], "unknown")


if __name__ == "__main__":
    unittest.main()
