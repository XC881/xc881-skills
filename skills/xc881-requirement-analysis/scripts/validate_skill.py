#!/usr/bin/env python3
from pathlib import Path
import json, re
root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
fm = text.split("---", 2)[1]
name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not name or name.group(1) != root.name:
    raise SystemExit("name must match folder")
for token in ["description:", "when_to_use:"]:
    if token not in fm:
        raise SystemExit(f"missing {token}")

for token in ["tags:", "category:", "aliases:"]:
    if token not in fm:
        raise SystemExit(f"missing {token}")
if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M):
    raise SystemExit("tags must be a non-empty YAML list")
for ref in ["english-spec-first-policy.md","implicit-requirement-inference.md","existing-project-feature-analysis.md","requirement-output-contract.md","requirement-quality-rubric.md"]:
    if not (root / "references" / ref).exists():
        raise SystemExit(f"missing {ref}")
for agent in ["openai.yaml","claude.yaml"]:
    t = (root / "agents" / agent).read_text(encoding="utf-8")
    for token in ["interface:","display_name:","short_description:","default_prompt:","policy:","allow_implicit_invocation: true"]:
        if token not in t:
            raise SystemExit(f"{agent} missing {token}")
ev = json.loads((root / "evals" / "trigger-queries.json").read_text(encoding="utf-8"))
workflows = {e["workflow"] for e in ev if e["should_trigger"]}
for workflow in ["new project","english spec first","existing project feature","implicit requirements"]:
    if workflow not in workflows:
        raise SystemExit(f"missing eval workflow {workflow}")

for forbidden in [  "research-basis.md"]:
    if (root / "references" / forbidden).exists():
        raise SystemExit(f"{forbidden} belongs in root docs/ or README, not per-skill references")

print("xc881-requirement-analysis optimized structure looks OK")
