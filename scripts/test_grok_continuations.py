#!/usr/bin/env python3
import contextlib
import io
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

from run_grok_continuations import (
    HOST_COMPACTION,
    classify_coverage,
    coverage_plan,
    create_args,
    encoded_cwd,
    load_continuations,
    main,
    resume_args,
    run_case,
    session_dir,
)

ROOT = Path(__file__).resolve().parents[1]


class GrokRunnerTests(unittest.TestCase):
    def test_execute_flag_required_and_does_not_spawn_grok(self):
        stderr = io.StringIO()
        with mock.patch("run_grok_continuations.subprocess.run") as grok_run:
            with mock.patch("run_grok_continuations.subprocess.check_output") as version:
                with contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as ctx:
                        main([
                            str(ROOT / "evals/continuations/path-only-activation.json"),
                            "--skill-root", str(ROOT / "skills"),
                            "--out-dir", str(ROOT / "no-such-grok-out"),
                        ])
        self.assertNotEqual(ctx.exception.code, 0)
        self.assertIn("--execute", stderr.getvalue())
        grok_run.assert_not_called()
        version.assert_not_called()

    def test_create_uses_uuid_session_id_not_resume(self):
        session_id = str(uuid.uuid4())
        args = create_args("hello", "/tmp/ws", session_id)
        self.assertEqual(args[0], "grok")
        self.assertIn("-p", args)
        self.assertIn("-s", args)
        self.assertEqual(args[args.index("-s") + 1], session_id)
        self.assertNotIn("-r", args)
        self.assertNotIn("--resume", args)
        self.assertIn("--always-approve", args)
        self.assertIn("--no-auto-update", args)
        self.assertIn("--output-format", args)
        self.assertEqual(args[args.index("--output-format") + 1], "json")
        with self.assertRaises(ValueError):
            create_args("hello", "/tmp/ws", "not-a-uuid")

    def test_resume_does_not_pass_create_flag(self):
        session_id = str(uuid.uuid4())
        args = resume_args("/compact", "/tmp/ws", session_id)
        self.assertIn("-r", args)
        self.assertEqual(args[args.index("-r") + 1], session_id)
        self.assertNotIn("-s", args)
        self.assertNotIn("--session-id", args)

    def test_session_dir_urlencodes_cwd(self):
        cwd = Path("/tmp/eval workspace")
        session_id = str(uuid.uuid4())
        path = session_dir(cwd, session_id, grok_home="/tmp/grok-home")
        self.assertEqual(path.parent.name, encoded_cwd(cwd))
        self.assertEqual(path.name, session_id)
        self.assertIn("%20", path.parent.name)

    def test_run_case_snapshots_each_turn_for_injection_compare(self):
        case = json.loads((ROOT / "evals/continuations/path-only-activation.json").read_text(encoding="utf-8"))

        def fake_run(args, cwd, env, capture_output, text, timeout):
            session_id = args[args.index("-s") + 1] if "-s" in args else args[args.index("-r") + 1]
            captured = session_dir(cwd, session_id, grok_home)
            captured.mkdir(parents=True, exist_ok=True)
            history = captured / "chat_history.jsonl"
            prefix = (
                '{"type":"system","content":"You are Grok 4.6"}\n'
                '{"type":"user","content":"Available Skills\\n<rules>\\nhello"}\n'
                '{"type":"assistant","content":"ok"}\n'
            )
            if "-s" in args:
                history.write_text(prefix, encoding="utf-8")
            else:
                history.write_text(
                    prefix
                    + '{"type":"user","content":"<user_query>again</user_query>"}\n'
                    + '{"type":"assistant","content":"ok2"}\n',
                    encoding="utf-8",
                )
            return mock.Mock(returncode=0, stdout="{}", stderr="")

        with tempfile.TemporaryDirectory(prefix="grok-home-") as home:
            grok_home = Path(home)
            with tempfile.TemporaryDirectory(prefix="grok-out-") as parent:
                out = Path(parent) / "run"
                with mock.patch("run_grok_continuations.subprocess.check_output", return_value="1.0.24\n"):
                    report = run_case(
                        case, ROOT / "skills", out, timeout=5, grok_home=grok_home, grok_run=fake_run,
                    )
                self.assertEqual(report["status"], "executed")
                self.assertTrue((out / "session-000").is_dir())
                self.assertTrue((out / "session-001").is_dir())
                compare = report["injection_compare"]
                self.assertEqual(compare["surface"], "chat_history.jsonl")
                self.assertEqual(compare["http_wire"], "unknown")
                self.assertEqual(
                    compare["classes"],
                    {"system": "absent", "skills": "absent", "rules": "absent"},
                )
                self.assertIn("No token savings", compare["note"])

    def test_coverage_plan_runs_compact_twice_and_every_executable(self):
        continuations = load_continuations(ROOT)
        plan = coverage_plan(continuations)
        ids = [case_id for case_id, _run in plan]
        executable_ids = [scenario["id"] for scenario in continuations if scenario.get("executable")]
        self.assertEqual(set(executable_ids), set(ids))
        self.assertEqual(ids.count(HOST_COMPACTION), 2)
        self.assertEqual(len(plan), len(executable_ids) + 1)
        self.assertEqual(
            classify_coverage(HOST_COMPACTION, {"status": "executed", "session": {"host_compaction": False}}),
            ("failed", "host_compaction_not_observed"),
        )
        self.assertEqual(
            classify_coverage(HOST_COMPACTION, {"status": "executed", "session": {"host_compaction": True}}),
            ("executed", None),
        )
        self.assertEqual(
            classify_coverage("path-only-activation", {"status": "incomplete", "error": "grok version: missing"}),
            ("unexecuted", "grok version: missing"),
        )

    def test_all_flag_still_requires_execute(self):
        stderr = io.StringIO()
        with mock.patch("run_grok_continuations.subprocess.run") as grok_run:
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as ctx:
                    main([
                        "--all",
                        "--skill-root", str(ROOT / "skills"),
                        "--out-dir", str(ROOT / "no-such-grok-coverage"),
                    ])
        self.assertNotEqual(ctx.exception.code, 0)
        self.assertIn("--execute", stderr.getvalue())
        grok_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
