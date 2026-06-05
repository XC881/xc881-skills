#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
skill = root / "SKILL.md"
text = skill.read_text(encoding="utf-8")

if not text.startswith("---"):
    raise SystemExit("SKILL.md must start with frontmatter")

parts = text.split("---", 2)
if len(parts) < 3:
    raise SystemExit("Frontmatter must be closed")

frontmatter = parts[1]

name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.M)
if not name:
    raise SystemExit("Missing valid name")
if name.group(1) != root.name:
    raise SystemExit(f"Skill name {name.group(1)!r} must match folder {root.name!r}")

for key in ["description:", "when_to_use:"]:
    if key not in frontmatter:
        raise SystemExit(f"Missing {key}")

for d in ["references", "agents", "evals", "scripts"]:
    if not (root / d).exists():
        raise SystemExit(f"Missing {d}")

for agent_file in ["openai.yaml", "claude.yaml"]:
    path = root / "agents" / agent_file
    if not path.exists():
        raise SystemExit(f"Missing agents/{agent_file}")
    content = path.read_text(encoding="utf-8")
    for token in ["interface:", "display_name:", "short_description:", "default_prompt:", "policy:", "allow_implicit_invocation: true"]:
        if token not in content:
            raise SystemExit(f"agents/{agent_file} missing {token}")

required_refs = [
    "english-spec-first-policy.md",
    "high-constraint-coding-policy.md",
    "no-code-comments-policy.md",
    "git-checkpoint-policy.md",
    "quality-bar.md",
    "low-quality-code-rubric.md",
    "project-optimization.md",
    "real-compatibility.md",
]
for ref in required_refs:
    if not (root / "references" / ref).exists():
        raise SystemExit(f"Missing reference {ref}")

triggers = json.loads((root / "evals" / "trigger-queries.json").read_text(encoding="utf-8"))
if not any(t["should_trigger"] for t in triggers):
    raise SystemExit("Missing positive trigger cases")
if not any(not t["should_trigger"] for t in triggers):
    raise SystemExit("Missing negative trigger cases")

workflows = {t.get("workflow") for t in triggers if t.get("should_trigger")}
for workflow in ["english spec first", "high constraint coding", "no code comments", "git checkpoint push", "xc881"]:
    if workflow not in workflows:
        raise SystemExit(f"Missing trigger coverage for {workflow}")

print("xc881 repo skill structure looks OK")
