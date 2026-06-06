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
for required in [
    "Explicit-only",
    "Do not auto-trigger",
    "Do not write implementation code",
    "Do not edit code",
    "Do not claim tests or verification were run",
]:
    if required not in text:
        raise SystemExit(f"missing explicit-only or analysis-only rule: {required}")
for ref in [
    "web-research-policy.md",
    "bugfix-forensics-workflow.md",
    "vulnerability-triage-policy.md",
    "reproducer-verification-plan.md",
    "bugfix-output-contract.md",
]:
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
positive = [e for e in ev if e["should_trigger"]]
negative = [e for e in ev if not e["should_trigger"]]
if not all("explicit" in e["workflow"] for e in positive):
    raise SystemExit("positive evals must be explicit invocation cases")
if not any(e["workflow"] == "ordinary bug mention" for e in negative):
    raise SystemExit("missing ordinary bug negative trigger")
for forbidden in ["real-compatibility.md", "research-basis.md", "skill-indexing-troubleshooting.md"]:
    if (root / "references" / forbidden).exists():
        raise SystemExit(f"{forbidden} belongs in root docs/ or README, not per-skill references")
print("xc881-bugfix-research explicit-only structure looks OK")
