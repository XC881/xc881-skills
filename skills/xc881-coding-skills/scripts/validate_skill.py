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
if "English Spec First" in text or "english-spec-first-policy.md" in text:
    raise SystemExit("English Spec First must not be in coding skill")
for agent_file in ["openai.yaml", "claude.yaml"]:
    content = (root / "agents" / agent_file).read_text(encoding="utf-8")
    for token in ["interface:", "display_name:", "short_description:", "default_prompt:", "policy:", "allow_implicit_invocation: true"]:
        if token not in content:
            raise SystemExit(f"agents/{agent_file} missing {token}")
print("xc881-coding-skills structure looks OK")
