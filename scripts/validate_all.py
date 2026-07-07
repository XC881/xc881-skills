#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
from skill_validation import (
    validate_behavior_contracts,
    validate_routing_matrix,
    validate_skill_frontmatter,
)
root = Path(__file__).resolve().parents[1]
m = json.loads((root/"skills-manifest.json").read_text(encoding="utf-8"))["skills"]
folders = {p.name for p in (root/"skills").iterdir() if p.is_dir()}
names = {s["name"] for s in m}
if names != folders: raise SystemExit(f"manifest mismatch: {names} != {folders}")
for s in m:
    p = root/"skills"/s["name"]
    validate_skill_frontmatter(p)
    subprocess.run([sys.executable, str(p/"scripts/validate_skill.py")], cwd=root, check=True)
    if s["trigger"] != "implicit-allowed":
        raise SystemExit(f"{s['name']}: trigger must be implicit-allowed")
    need = "true"
    for a in ["openai.yaml","claude.yaml"]:
        t = (p/"agents"/a).read_text(encoding="utf-8")
        if f"allow_implicit_invocation: {need}" not in t:
            raise SystemExit(f"{s['name']}/{a}: bad trigger policy")
validate_routing_matrix(root, m)
validate_behavior_contracts(root, m)
print("xc881-skills OK")
