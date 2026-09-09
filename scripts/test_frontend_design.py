#!/usr/bin/env python3

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/xc881-coding-skills/scripts/frontend_design.py"
spec = importlib.util.spec_from_file_location("xc881_frontend_design", CLI)
design = importlib.util.module_from_spec(spec)
spec.loader.exec_module(design)


class FrontendDesignTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None, ok=True):
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)], cwd=cwd,
                                capture_output=True, text=True, timeout=20)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_catalog_and_all_domain_paths(self):
        catalog = self.run_cli("--catalog")
        core = design.engine()
        self.assertEqual(set(catalog["domains"]), set(core.CSV_CONFIG))
        self.assertEqual(catalog["counts"]["stacks"], len(core.AVAILABLE_STACKS))
        identity = {"style": "Style ID", "color": "Product Type", "chart": "Data Type",
                    "landing": "Pattern ID", "product": "Product Type", "ux": "Issue",
                    "typography": "Font Pairing Name", "icons": "Icon Name", "gsap": "Category",
                    "react": "Issue", "web": "Issue", "google-fonts": "Family"}
        for domain, config in core.CSV_CONFIG.items():
            with self.subTest(domain=domain):
                query = design.rows(config["file"])[0][identity[domain]]
                if domain == "icons":
                    query = "navigation home icon"
                output = self.run_cli(query, "--domain", domain)
                self.assertGreater(output["count"], 0)
                self.assertLessEqual(len(design.encode(output)), design.OUTPUT_LIMIT)
                self.assertTrue(output["candidates"][0]["record"].startswith(config["file"] + "#"))

    def test_all_stack_paths_and_full_code(self):
        core = design.engine()
        for stack in core.AVAILABLE_STACKS:
            with self.subTest(stack=stack):
                relative = core.STACK_CONFIG[stack]["file"]
                rows = design.rows(relative)
                row = next(row for row in rows if row.get("Status", "active") == "active") if stack != "uwp" else rows[0]
                output = self.run_cli(row["Guideline"], "--stack", stack)
                self.assertGreater(output["count"], 0)
                record = output["candidates"][0]["record"]
                detail = self.run_cli("--record", record, "--fields", "Code Good", "Do", "Don't")
                original = design.detail(record)["fields"]
                self.assertEqual(detail["fields"]["Code Good"], original["Code Good"])
                self.assertEqual(detail["fields"]["Don't"], original["Don't"])
                self.assertLessEqual(len(design.encode(output)), design.OUTPUT_LIMIT)

    def test_no_match_does_not_invent_profile(self):
        result = self.run_cli("zzzxqvplm", "--domain", "ux")
        self.assertEqual(result["status"], "no-match")
        self.assertEqual(result["candidates"], [])
        generated = self.run_cli("zzzxqvplm", "--design-system")
        self.assertEqual(generated["status"], "candidate-with-fallback")
        self.assertIn("product", generated["fallback_fields"])

    def test_deterministic_and_bounded(self):
        result = self.run_cli("dashboard analytics", "--domain", "style", "--limit", 3)
        self.assertEqual(result, self.run_cli("dashboard analytics", "--domain", "style", "--limit", 3))
        self.assertLessEqual(result["count"], 3)
        self.assertLessEqual(len(design.encode(result)), design.OUTPUT_LIMIT)

    def test_surface_and_exact_system_sections(self):
        app = self.run_cli("healthcare dashboard", "--design-system", "--surface", "app")
        self.assertEqual(app["layout"]["surface"], "app")
        self.assertNotIn("pattern", app)
        self.assertNotIn("landing", app["source_identities"])
        self.assertTrue(app["style"]["accessibility"])
        self.assertLessEqual(len(design.encode(app)), design.OUTPUT_LIMIT)
        section = self.run_cli("healthcare dashboard", "--design-system", "--section", "colors")
        for key, value in app["colors"].items():
            self.assertEqual(section["value"][key], value)
        landing = self.run_cli("portfolio landing", "--design-system", "--surface", "landing")
        self.assertEqual(landing["layout"]["surface"], "landing")
        self.assertIn("sections", landing["layout"])

    def test_dials_reach_real_generator(self):
        output = self.run_cli("analytics dashboard", "--design-system", "--density", 9,
                              "--section", "spacing_scale")
        self.assertEqual(output["value"]["md"], "8px")
        motion = self.run_cli("button interaction", "--design-system", "--motion", 2,
                              "--section", "motion_snippet")
        self.assertIn("GSAP Snippet", motion["value"])
        generated = design.design_system("healthcare dashboard", "Clinic", "app", density=9)
        for section in design.SECTIONS:
            with self.subTest(section=section):
                self.assertIn(section, generated)
        summary = design.system_summary(generated)
        self.assertEqual(summary["project_name"], "Clinic")

    def test_default_commands_are_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            before = {p.relative_to(design.VENDOR) for p in design.VENDOR.rglob("*")}
            self.run_cli("time series", "--domain", "chart", cwd=directory)
            self.run_cli("healthcare dashboard", "--design-system", cwd=directory)
            self.assertEqual(list(Path(directory).iterdir()), [])
            self.assertEqual(before, {p.relative_to(design.VENDOR) for p in design.VENDOR.rglob("*")})

    def test_installer_distributes_relocatable_complete_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, HOME=directory)
            subprocess.run(["bash", str(ROOT / "scripts/install.sh"), "codex"],
                           env=env, check=True, capture_output=True, timeout=20)
            target = Path(directory) / ".codex/skills"
            subprocess.run([sys.executable, str(ROOT / "scripts/validate_installed_skills.py"), str(target)],
                           check=True, capture_output=True, timeout=20)
            installed_cli = target / "xc881-coding-skills/scripts/frontend_design.py"
            result = subprocess.run([sys.executable, str(installed_cli), "time series", "--domain", "chart"],
                                    cwd=directory, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreater(json.loads(result.stdout)["count"], 0)

    def test_persist_is_explicit_bounded_and_non_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ("healthcare dashboard", "--design-system", "--persist", "--project-root", directory, "--slug", "clinic")
            result = self.run_cli(*args)
            target = Path(result["path"])
            self.assertEqual(target, Path(directory) / "dev-notes/design-system/clinic/MASTER.md")
            content = target.read_text(encoding="utf-8")
            self.assertLessEqual(len(content), 3000)
            self.assertIn("Status: proposal", content)
            self.run_cli(*args, ok=False)
            self.assertEqual(target.read_text(encoding="utf-8"), content)
            self.assertFalse((Path(directory) / "design-system").exists())
            self.run_cli("healthcare", "--design-system", "--persist", "--project-root", directory,
                         "--slug", "../../outside", ok=False)

    def test_symlink_notes_are_not_followed(self):
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as outside:
            (Path(project) / "dev-notes").symlink_to(outside, target_is_directory=True)
            self.run_cli("healthcare dashboard", "--design-system", "--persist", "--project-root", project,
                         "--slug", "clinic", ok=False)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_invalid_modes_and_arbitrary_file_access(self):
        for args in [("test", "--domain", "unknown"), ("test", "--stack", "unknown"),
                     ("test", "--limit", 20), ("test", "--section", "colors"),
                     ("test", "--fields", "Do"), ("--record", "../LICENSE#1"),
                     ("--record", "ux-guidelines.csv#0"), ("--record", "ux-guidelines.csv#99999"),
                     ("--record", "ux-guidelines.csv#1", "--fields", "not-a-column"),
                     ("test", "--design-system", "--persist"), ("test", "--catalog")]:
            with self.subTest(args=args):
                self.run_cli(*args, ok=False)


if __name__ == "__main__":
    unittest.main()
