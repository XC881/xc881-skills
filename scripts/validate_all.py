#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
root = Path(__file__).resolve().parents[1]
m = json.loads((root/"skills-manifest.json").read_text(encoding="utf-8"))["skills"]
folders = {p.name for p in (root/"skills").iterdir() if p.is_dir()}
names = {s["name"] for s in m}
if names != folders: raise SystemExit(f"manifest mismatch: {names} != {folders}")
for s in m:
    p = root/"skills"/s["name"]
    subprocess.run([sys.executable, str(p/"scripts/validate_skill.py")], cwd=root, check=True)
    need = "false" if s["trigger"] == "explicit-only" else "true"
    for a in ["openai.yaml","claude.yaml"]:
        t = (p/"agents"/a).read_text(encoding="utf-8")
        if f"allow_implicit_invocation: {need}" not in t:
            raise SystemExit(f"{s['name']}/{a}: bad trigger policy")
print("xc881-skills OK")
