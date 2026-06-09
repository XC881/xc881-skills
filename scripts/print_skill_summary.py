#!/usr/bin/env python3
from pathlib import Path
import json
root = Path(__file__).resolve().parents[1]
for s in json.loads((root/"skills-manifest.json").read_text(encoding="utf-8"))["skills"]:
    print(f"{s['name']}: {s['trigger']} | {s['mode']} | handoff={','.join(s['handoff']) or '-'}")
