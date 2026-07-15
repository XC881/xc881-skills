#!/usr/bin/env python3
from pathlib import Path
import json, re, subprocess, sys
root = Path(__file__).resolve().parents[1]
text = (root/"SKILL.md").read_text(encoding="utf-8")
fm = text.split("---",2)[1] if text.startswith("---") else ""
def die(x): raise SystemExit(x)
m = re.search(r"^name:\s*([a-z0-9-]+)\s*$", fm, re.M)
if not m or m.group(1) != root.name: die("name must match folder")
for k in ["description:","when_to_use:","display_name:","version:","category:","tags:","aliases:"]:
    if k not in fm: die(f"missing {k}")
if not re.search(r"^tags:\n(?:  - .+\n)+", fm, re.M): die("tags must be non-empty")
for ref in ['goal-boundary-contract.md', 'cross-language-understanding.md', 'equivalence-and-idiomatic-porting.md', 'porting-output-contract.md', 'cross-process-plan.md']:
    if not (root/"references"/ref).exists(): die(f"missing {ref}")
cross_validator = root/"scripts/validate_cross_process.py"
if not cross_validator.exists(): die("missing validate_cross_process.py")
subprocess.run([sys.executable, str(cross_validator), "--self-test"], check=True)
for a in ["openai.yaml","claude.yaml"]:
    t = (root/"agents"/a).read_text(encoding="utf-8")
    for k in ["interface:","display_name:","short_description:","default_prompt:","policy:",'allow_implicit_invocation: true']:
        if k not in t: die(f"{a} missing {k}")
ev = json.loads((root/"evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev): die("need positive eval")
if not any(not e["should_trigger"] for e in ev): die("need negative eval")
if "Intent-routed" not in text: die("missing intent-routing rule")
cross_text = (root/"references/cross-process-plan.md").read_text(encoding="utf-8")
for rule in ["Never scan `cross-process/`", "req-process `current.md`", "Do not read req-process `index.md`"]:
    if rule not in cross_text: die(f"missing current-window rule: {rule}")
for rule in ["continue automatically", "task terminal", "explicit stepwise/pause intent"]:
    if rule not in text + cross_text: die(f"missing continuous-run rule: {rule}")
for rule in ["supplied or cheap evidence", "Small non-goal planning stays", "Planning/boundary-only intent stops"]:
    if rule not in text: die(f"missing minimum porting branch: {rule}")
if not any(e["should_trigger"] and "porting boundary only" in e["workflow"] for e in ev):
    die("need positive boundary-only eval")
output_text = (root/"references/porting-output-contract.md").read_text(encoding="utf-8")
human_sections = ["迁移结论", "本次迁移", "如何确认成功", "当前进度", "下一步", "开发记录"]
for heading in human_sections:
    if heading not in output_text: die(f"human output missing {heading}")
contract = json.loads((root/"evals/behavior-contract.json").read_text(encoding="utf-8"))
if contract.get("required_sections") != human_sections:
    die("behavior contract must validate human-facing porting output")
if len(text.splitlines()) > 120: die("SKILL.md too long")
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 55:
        die(f"{ref.name} too long")
print(root.name + " OK")
