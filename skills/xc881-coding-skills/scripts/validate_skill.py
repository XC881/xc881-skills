#!/usr/bin/env python3
from pathlib import Path
import json, re
root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
fm = text.split("---", 2)[1]
name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not name or name.group(1) != root.name:
    raise SystemExit("name must match folder")
for token in ["description:", "when_to_use:", "tags:", "category:", "aliases:"]:
    if token not in fm:
        raise SystemExit(f"missing {token}")
if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M):
    raise SystemExit("tags must be a non-empty YAML list")
if "English Spec First" in text or "english-spec-first-policy.md" in text:
    raise SystemExit("English Spec First belongs to requirement-analysis")
for ref in [
    "xc881-code-quality-standard.md",
    "high-constraint-coding-policy.md",
    "no-code-comments-policy.md",
    "git-checkpoint-policy.md",
    "engineering-quality-rubric.md",
    "project-optimization.md",
]:
    if not (root / "references" / ref).exists():
        raise SystemExit(f"missing {ref}")
for agent in ["openai.yaml", "claude.yaml"]:
    t = (root / "agents" / agent).read_text(encoding="utf-8")
    for token in ["interface:", "display_name:", "short_description:", "default_prompt:", "policy:", "allow_implicit_invocation: true"]:
        if token not in t:
            raise SystemExit(f"{agent} missing {token}")
ev = json.loads((root / "evals" / "trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev) or not any(not e["should_trigger"] for e in ev):
    raise SystemExit("evals need positive and negative examples")
workflows = {e["workflow"] for e in ev if e["should_trigger"]}
for workflow in ["code quality", "performance mode", "high constraint coding", "comments policy", "git checkpoint push"]:
    if workflow not in workflows:
        raise SystemExit(f"missing eval workflow {workflow}")
for forbidden in ["skill-indexing-troubleshooting.md", "real-compatibility.md", "research-basis.md"]:
    if (root / "references" / forbidden).exists():
        raise SystemExit(f"{forbidden} belongs in root docs/ or README, not per-skill references")
print("xc881-coding-skills optimized structure looks OK")
