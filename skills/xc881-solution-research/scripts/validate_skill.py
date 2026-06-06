#!/usr/bin/env python3
from pathlib import Path
import json, re
root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
fm = text.split("---", 2)[1]
name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not name or name.group(1) != root.name:
    raise SystemExit("name must match folder")
for token in ["description:", "when_to_use:", "display_name:", "version:", "category:", "tags:", "aliases:"]:
    if token not in fm:
        raise SystemExit(f"missing {token}")
if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M):
    raise SystemExit("tags must be a non-empty YAML list")
for required in ["Explicit-only", "Do not auto-trigger", "Explicit invocation only", "Do not implement code"]:
    if required not in text:
        raise SystemExit(f"missing explicit-only or analysis-only rule: {required}")
for ref in ["english-spec-and-research-questions.md","source-priority-policy.md","paper-first-policy.md","tech-stack-feasibility-policy.md","solution-output-contract.md"]:
    if not (root / "references" / ref).exists():
        raise SystemExit(f"missing {ref}")
for agent in ["openai.yaml", "claude.yaml"]:
    t = (root / "agents" / agent).read_text(encoding="utf-8")
    for token in ["interface:", "display_name:", "short_description:", "default_prompt:", "policy:", "allow_implicit_invocation: false"]:
        if token not in t:
            raise SystemExit(f"{agent} missing {token}")
ev = json.loads((root / "evals" / "trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev) or not any(not e["should_trigger"] for e in ev):
    raise SystemExit("evals need positive and negative examples")
if not all("explicit" in e["workflow"] for e in ev if e["should_trigger"]):
    raise SystemExit("positive evals must be explicit invocation cases")
print("xc881-solution-research explicit-only structure looks OK")
