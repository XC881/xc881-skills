#!/usr/bin/env python3
from pathlib import Path
import json, re
root = Path(__file__).resolve().parents[1]
text = (root/"SKILL.md").read_text(encoding="utf-8")
fm = text.split("---",2)[1] if text.startswith("---") else ""
def die(x): raise SystemExit(x)
m = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not m or m.group(1) != root.name: die("name must match folder")
for k in ["description:","when_to_use:","display_name:","version:","category:","tags:","aliases:"]:
    if k not in fm: die(f"missing {k}")
if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M): die("tags must be non-empty")
for ref in ['english-spec-and-research-questions.md', 'source-priority-policy.md', 'paper-first-policy.md', 'tech-stack-feasibility-policy.md', 'solution-output-contract.md']:
    if not (root/"references"/ref).exists(): die(f"missing {ref}")
for a in ["openai.yaml","claude.yaml"]:
    t = (root/"agents"/a).read_text(encoding="utf-8")
    for k in ["interface:","display_name:","short_description:","default_prompt:","policy:",'allow_implicit_invocation: false']:
        if k not in t: die(f"{a} missing {k}")
ev = json.loads((root/"evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev): die("need positive eval")
if not any(not e["should_trigger"] for e in ev): die("need negative eval")
if True:
    if (
        "Explicit only." not in text
        and "Explicit xc881-prefixed intent only." not in text
        and "Explicit xc881-scoped intent only." not in text
    ):
        die("missing explicit rule")
    if not all("explicit" in e["workflow"] for e in ev if e["should_trigger"]): die("positive evals must be explicit")
if len(text.splitlines()) > 90: die("SKILL.md too long")
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 50:
        die(f"{ref.name} too long")
for bad in ["skill-indexing-troubleshooting.md","real-compatibility.md","research-basis.md"]:
    if (root/"references"/bad).exists(): die(f"{bad} belongs in docs/")
print(root.name + " OK")
