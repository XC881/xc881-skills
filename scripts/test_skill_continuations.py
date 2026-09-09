#!/usr/bin/env python3
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from audit_skill_continuations import (
    USAGE_KEYS, attach_usage, compare_runs, efficiency_conclusion, host_compaction,
    instruction_reads, load_events, load_report, main, usage_from_events,
    validate_executable_cases,
)
from audit_skill_loads import validate_continuations
from run_skill_continuations import local_path, main as run_main, retained_event

ROOT = Path(__file__).resolve().parents[1]


def token_event(turn_id, total, last=None):
    def block(value):
        if isinstance(value, dict):
            return {key: value.get(key, 0) for key in USAGE_KEYS}
        return {key: value for key in USAGE_KEYS}
    return {"method": "thread/tokenUsage/updated", "params": {
        "turnId": turn_id,
        "tokenUsage": {"total": block(total), "last": block(total if last is None else last)},
    }}


def complete(turn_id, status="completed"):
    return {"method": "turn/completed", "params": {"turn": {"id": turn_id, "status": status}}}


class ContinuationAuditTests(unittest.TestCase):
    def test_usage_is_cumulative_delta_not_sum_of_last(self):
        events = [
            token_event("t1", 100, last=100),
            token_event("t1", 250, last=150),
            complete("t1"),
            token_event("t2", 250, last=150),
            token_event("t2", 300, last=50),
            complete("t2"),
        ]
        usage = usage_from_events(events)
        self.assertEqual(usage["method"], "cumulative_total_delta")
        self.assertTrue(usage["observed"])
        self.assertEqual(usage["thread"]["totalTokens"], 300)
        self.assertEqual([turn["usage"]["totalTokens"] for turn in usage["turns"]], [250, 50])
        summed_last = 100 + 150 + 150 + 50
        self.assertNotEqual(usage["thread"]["totalTokens"], summed_last)

    def test_repeated_total_and_zeroed_last_do_not_add_usage(self):
        events = [
            token_event("t1", {"totalTokens": 120679, "inputTokens": 119360, "cachedInputTokens": 93184,
                               "cacheWriteInputTokens": 0, "outputTokens": 1319, "reasoningOutputTokens": 0}),
            complete("t1"),
            token_event("t2", {"totalTokens": 120679, "inputTokens": 119360, "cachedInputTokens": 93184,
                               "cacheWriteInputTokens": 0, "outputTokens": 1319, "reasoningOutputTokens": 0}),
            token_event("t2", {"totalTokens": 128535, "inputTokens": 126384, "cachedInputTokens": 93184,
                               "cacheWriteInputTokens": 0, "outputTokens": 2151, "reasoningOutputTokens": 0},
                        last={"totalTokens": 7856, "inputTokens": 7024, "cachedInputTokens": 0,
                              "cacheWriteInputTokens": 0, "outputTokens": 832, "reasoningOutputTokens": 0}),
            token_event("t2", {"totalTokens": 128535, "inputTokens": 126384, "cachedInputTokens": 93184,
                               "cacheWriteInputTokens": 0, "outputTokens": 2151, "reasoningOutputTokens": 0},
                        last={"totalTokens": 1253, "inputTokens": 0, "cachedInputTokens": 0,
                              "cacheWriteInputTokens": 0, "outputTokens": 0, "reasoningOutputTokens": 0}),
            complete("t2"),
        ]
        usage = usage_from_events(events)
        self.assertEqual(usage["turns"][1]["usage"]["totalTokens"], 7856)
        self.assertEqual(usage["thread"]["totalTokens"], 128535)

    def test_failed_and_missing_usage_cannot_claim_savings(self):
        failed = attach_usage({"status": "incomplete", "effective_skill": "/tmp/skill"}, [])
        self.assertIsNone(failed["usage_claim"])
        self.assertEqual(failed["usage_reason"], "incomplete")
        missing = attach_usage({"status": "executed", "effective_skill": "/tmp/skill"}, [complete("t1")])
        self.assertEqual(missing["usage_reason"], "missing_usage")
        self.assertIsNone(efficiency_conclusion(
            {"status": "executed", "model": "m", "client_version": "1", "case_sha256": "x",
             "usage": missing["usage"]},
            {"status": "incomplete", "model": "m", "client_version": "1", "case_sha256": "x",
             "usage": failed["usage"]},
        )["claim"])

    def test_condition_mismatch_and_character_counts_are_rejected(self):
        observed = {"status": "executed", "model": "m", "client_version": "1", "case_sha256": "x",
                    "usage": {"observed": True, "thread": {"totalTokens": 100}}, "instruction_reads": []}
        other = dict(observed, model="other")
        self.assertEqual(efficiency_conclusion(observed, other)["reason"], "condition_mismatch:model")
        with_chars = dict(observed, chars=4000)
        self.assertEqual(efficiency_conclusion(observed, with_chars)["reason"], "character_counts_are_not_usage")

    def test_instruction_reads_ignore_writes_and_project_files(self):
        skill = "/tmp/eval/skill"
        commands = [
            f"/bin/bash -lc 'rtk read {skill}/SKILL.md'",
            f"/bin/bash -lc 'rtk read {skill}/references/requirement-artifact-execution.md'",
            "/bin/bash -lc 'rtk read dev-notes/req-process/labels/current.md'",
            f"/bin/bash -lc \"rtk proxy apply_patch <<'PATCH'\\n*** Update File: {skill}/SKILL.md\\nPATCH\"",
        ]
        self.assertEqual(instruction_reads(commands, skill), [
            "SKILL.md", "references/requirement-artifact-execution.md",
        ])

    def test_observed_only_conclusion_lists_unobserved_boundaries(self):
        run = {
            "status": "executed", "model": "gpt-6-astra", "client_version": "codex-cli 0.153.4",
            "case_sha256": "abc", "instruction_reads": ["SKILL.md"],
            "usage": {"observed": True, "thread": {"totalTokens": 128535}},
        }
        conclusion = efficiency_conclusion(run, dict(run, instruction_reads=["SKILL.md", "SKILL.md"]))
        self.assertEqual(conclusion["claim"], "observed_only")
        self.assertIn("provider_request_bodies", conclusion["unobserved"])
        self.assertNotIn("saved_tokens", conclusion)

    def test_cli_and_declared_continuations(self):
        scenarios = validate_executable_cases(ROOT)
        ids = {item["id"] for item in scenarios}
        self.assertTrue({
            "supplied-body-three-turns", "path-only-activation", "explicit-repeat-invocation",
            "new-and-returning-concern", "known-instruction-change", "missing-after-compaction",
            "retained-after-compaction", "fresh-context-loaded-marker",
            "host-compaction-queue-resume", "requested-reread",
        }.issubset(ids))
        self.assertEqual(len(validate_continuations(ROOT)), len(scenarios))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "run.json").write_text(json.dumps({
                "case": "probe", "status": "executed", "model": "m",
                "usage_scope": "this thread; no claim about unobserved provider payloads or child usage",
                "effective_skill": "/tmp/skill",
            }), encoding="utf-8")
            (path / "events.jsonl").write_text(json.dumps(token_event("t1", 9)) + "\n" + json.dumps(complete("t1")) + "\n", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main([str(path)]), 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["usage"]["thread"]["totalTokens"], 9)
            self.assertFalse(payload["host_compaction"])
            self.assertEqual(load_events(path / "events.jsonl")[0]["method"], "thread/tokenUsage/updated")

    def test_host_compaction_is_not_inferred_from_simulation(self):
        compact = {"method": "item/completed", "params": {"item": {"type": "contextCompaction", "id": "c1"}}}
        self.assertTrue(host_compaction([compact]))
        self.assertTrue(host_compaction([{"method": "thread/compacted"}]))
        self.assertFalse(host_compaction([complete("t1")]))
        self.assertIsNotNone(retained_event(compact))
        self.assertIsNone(retained_event({"method": "noise"}))
        with self.assertRaises(ValueError):
            local_path(Path("/tmp/eval"), "../etc/passwd")

    def test_compare_cli_rejects_unexecuted_and_accepts_matched_usage(self):
        def write_run(path, status, total, compact=False, model="m"):
            events = [json.dumps(token_event("t1", total)), json.dumps(complete("t1"))]
            if compact:
                events.insert(1, json.dumps({"method": "item/completed", "params": {"item": {"type": "contextCompaction"}}}))
            path.mkdir()
            (path / "run.json").write_text(json.dumps({
                "case": "queue-block-compact-resume", "status": status, "model": model,
                "client_version": "codex-cli 0.153.4", "case_sha256": "abc",
                "effective_skill": "/tmp/skill",
            }), encoding="utf-8")
            (path / "events.jsonl").write_text("\n".join(events) + "\n", encoding="utf-8")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_run(root / "base", "executed", 200, compact=True)
            write_run(root / "cand", "executed", 180, compact=True)
            write_run(root / "dead", "incomplete", 180)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(main(["--compare", str(root / "base"), str(root / "cand")]), 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["claim"], "observed_only")
            self.assertEqual(payload["baseline_thread_tokens"], 200)
            self.assertEqual(payload["candidate_thread_tokens"], 180)
            self.assertTrue(payload["candidate_host_compaction"])
            self.assertNotIn("saved_tokens", payload)
            self.assertIsNone(compare_runs(load_report(root / "base"), load_report(root / "dead"))["claim"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--compare", str(root / "base"), str(root / "dead")]), 1)

    def test_runner_requires_execute_flag(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as ctx:
                run_main([
                    str(ROOT / "evals/queue-execution/block-compact-resume.json"),
                    "--skill-root", str(ROOT / "skills"),
                    "--out-dir", str(ROOT / "no-such-out"),
                ])
        self.assertNotEqual(ctx.exception.code, 0)
        self.assertIn("--execute", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
