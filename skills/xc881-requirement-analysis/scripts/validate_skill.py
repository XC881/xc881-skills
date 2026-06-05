#!/usr/bin/env python3
from pathlib import Path
import json
import re
root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
frontmatter = text.split("---", 2)[1]
name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.M)
if not name or name.group(1) != root.name:
    raise SystemExit("Skill name must match folder name")
for required in ["Existing project feature", "Implicit requirement inference", "Inferred / Derived Requirements"]:
    if required not in text:
        raise SystemExit(f"Missing required section: {required}")
for ref in ["english-spec-first-policy.md", "implicit-requirement-inference.md", "existing-project-feature-analysis.md", "requirement-quality-rubric.md", "prd-template.md", "research-basis.md"]:
    if not (root / "references" / ref).exists():
        raise SystemExit(f"Missing reference {ref}")
triggers = json.loads((root / "evals" / "trigger-queries.json").read_text(encoding="utf-8"))
workflows = {t["workflow"] for t in triggers if t["should_trigger"]}
for workflow in ["english spec first", "existing project feature", "implicit requirements", "new project"]:
    if workflow not in workflows:
        raise SystemExit(f"Missing trigger coverage: {workflow}")
print("xc881-requirement-analysis structure looks OK")
