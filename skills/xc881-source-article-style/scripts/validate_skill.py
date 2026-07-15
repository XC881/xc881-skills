#!/usr/bin/env python3
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
fm = text.split("---", 2)[1] if text.startswith("---") else ""


def die(message):
    raise SystemExit(message)


m = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not m or m.group(1) != root.name:
    die("name must match folder")

for key in [
    "description:",
    "when_to_use:",
    "display_name:",
    "version:",
    "category:",
    "tags:",
    "aliases:",
]:
    if key not in fm:
        die(f"missing {key}")

if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M):
    die("tags must be non-empty")

refs = [
    "function-level-source-article.md",
    "evidence-and-style-rules.md",
    "article-output-contract.md",
]
for ref in refs:
    if not (root / "references" / ref).exists():
        die(f"missing {ref}")

for agent in ["openai.yaml", "claude.yaml"]:
    content = (root / "agents" / agent).read_text(encoding="utf-8")
    for key in [
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        "policy:",
        "allow_implicit_invocation: true",
    ]:
        if key not in content:
            die(f"{agent} missing {key}")

evals = json.loads((root / "evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in evals):
    die("need positive eval")
if not any(not e["should_trigger"] for e in evals):
    die("need negative eval")
if "Intent-routed" not in text:
    die("missing intent-routing rule")
for rule in ["Reuse supplied evidence", "Inspect only missing simple exact/local/low-risk facts", "delegate missing complex/tracked evidence to `$xc881-coding-skills`", "Do not bypass Coding for complex/tracked source inspection"]:
    if rule not in text:
        die(f"missing Coding read delegation: {rule}")

if len(text.splitlines()) > 110:
    die("SKILL.md too long")
for ref in (root / "references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 65:
        die(f"{ref.name} too long")

print(root.name + " OK")
