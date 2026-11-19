#!/usr/bin/env python3
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts/install.sh"


def run_install(target, home, extra=None):
    env = dict(os.environ, HOME=str(home))
    if extra:
        env.update(extra)
    return subprocess.run(
        ["bash", str(INSTALL), target],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )


def run_copy(dest, home):
    command = "source {install} && copy {dest}".format(
        install=shlex.quote(str(INSTALL)),
        dest=shlex.quote(dest),
    )
    return subprocess.run(
        ["bash", "-c", command],
        env=dict(os.environ, HOME=str(home)),
        capture_output=True,
        text=True,
        timeout=20,
    )


class InstallTests(unittest.TestCase):
    def test_cli_installs_codex_and_grok_under_fake_home(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for target in ("codex", "grok"):
                result = run_install(target, home)
                self.assertEqual(result.returncode, 0, result.stderr)
            expected = sorted(
                path.name for path in (ROOT / "skills").glob("xc881-*") if path.is_dir()
            )
            for dest in (home / ".codex/skills", home / ".grok/skills"):
                names = sorted(path.name for path in dest.glob("xc881-*") if path.is_dir())
                self.assertEqual(names, expected)
                self.assertTrue((dest / "xc881-coding-skills/SKILL.md").is_file())
            self.assertFalse((home / ".claude/skills").exists())

    def test_copy_refuses_empty_slash_and_home(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for dest in ("", "/", str(home)):
                result = run_copy(dest, home)
                self.assertNotEqual(result.returncode, 0, dest)
                self.assertIn("refusing dest root", result.stderr)
            self.assertEqual(list(home.iterdir()), [])

    def test_copy_refuses_existing_dest_without_skill_md(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest_root = home / "skills"
            blocked = dest_root / "xc881-coding-skills"
            blocked.mkdir(parents=True)
            marker = blocked / "notes.txt"
            marker.write_text("keep", encoding="utf-8")
            result = run_copy(str(dest_root), home)
            self.assertNotEqual(result.returncode, 0, result.stderr)
            self.assertIn("refusing to replace", result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertFalse((blocked / "SKILL.md").exists())

    def test_copy_replaces_existing_skill_dir_and_leaves_unrelated(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest_root = home / "skills"
            skill = dest_root / "xc881-coding-skills"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("old", encoding="utf-8")
            (skill / "stale.txt").write_text("remove", encoding="utf-8")
            unrelated = dest_root / "other-tool"
            unrelated.mkdir()
            (unrelated / "keep.txt").write_text("ok", encoding="utf-8")
            result = run_copy(str(dest_root), home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual((skill / "SKILL.md").read_text(encoding="utf-8"), "old")
            self.assertFalse((skill / "stale.txt").exists())
            self.assertEqual((unrelated / "keep.txt").read_text(encoding="utf-8"), "ok")

    def test_copy_prunes_retired_skill_dirs_safely_and_validates_parity(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest_root = home / "skills"
            for retired in ("xc881-requirement-analysis", "xc881-bugfix-research", "xc881-solution-research"):
                stale = dest_root / retired
                stale.mkdir(parents=True)
                (stale / "SKILL.md").write_text("retired", encoding="utf-8")
            result = run_copy(str(dest_root), home)
            self.assertEqual(result.returncode, 0, result.stderr)
            for retired in ("xc881-requirement-analysis", "xc881-bugfix-research", "xc881-solution-research"):
                self.assertFalse((dest_root / retired).exists())
            parity = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_installed_skills.py"), str(dest_root)],
                capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(parity.returncode, 0, parity.stderr)

            rogue = dest_root / "xc881-requirement-analysis"
            rogue.mkdir()
            (rogue / "notes.txt").write_text("keep", encoding="utf-8")
            refused = run_copy(str(dest_root), home)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("refusing to prune", refused.stderr)
            self.assertEqual((rogue / "notes.txt").read_text(encoding="utf-8"), "keep")
            stale_parity = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_installed_skills.py"), str(dest_root)],
                capture_output=True, text=True, timeout=20,
            )
            self.assertNotEqual(stale_parity.returncode, 0)


if __name__ == "__main__":
    unittest.main()
