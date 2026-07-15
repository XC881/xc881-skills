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
for ref in ['english-spec-first-policy.md', 'implicit-requirement-inference.md', 'existing-project-feature-analysis.md', 'issue-tracker-triage.md', 'requirement-process-artifact.md', 'requirement-output-contract.md', 'requirement-quality-rubric.md']:
    if not (root/"references"/ref).exists(): die(f"missing {ref}")
artifact_validator = root/"scripts/validate_req_process.py"
if not artifact_validator.exists(): die("missing validate_req_process.py")
subprocess.run([sys.executable, str(artifact_validator), "--self-test"], check=True)
candidate_finder = root/"scripts/find_req_process_candidates.py"
if not candidate_finder.exists(): die("missing find_req_process_candidates.py")
subprocess.run([sys.executable, str(candidate_finder), "--self-test"], check=True)
for a in ["openai.yaml","claude.yaml"]:
    t = (root/"agents"/a).read_text(encoding="utf-8")
    for k in ["interface:","display_name:","short_description:","default_prompt:","policy:",'allow_implicit_invocation: true']:
        if k not in t: die(f"{a} missing {k}")
ev = json.loads((root/"evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev): die("need positive eval")
if not any(not e["should_trigger"] for e in ev): die("need negative eval")
if "Intent-routed" not in text:
    die("missing intent-routing rule")
for rule in ["perform a simple exact/local/low-risk read here", "delegate a complex/tracked `read` to `$xc881-coding-skills`", "hand every write and selected complex/tracked read", "per-item “continue”", "no second invocation"]:
    if rule not in text: die(f"missing Coding handoff rule: {rule}")
artifact_text = (root/"references/requirement-process-artifact.md").read_text(encoding="utf-8")
for section in ["## Goal", "## Contract", "## Targets", "## Constraints", "## Verification"]:
    if section not in artifact_text: die(f"artifact contract missing {section}")
if "Requirement reads it by default" not in artifact_text:
    die("artifact contract must define Requirement's default index.md read")
if "Coding does not read `index.md`" not in artifact_text:
    die("artifact contract must keep index.md out of normal Coding continuation")
for rule in ["Reuse Before Gate", "one semantic match", "Coding never"]:
    if rule not in artifact_text: die(f"artifact contract missing reuse rule: {rule}")
if "chat-only lightweight analysis does not scan" not in artifact_text:
    die("artifact contract must keep lightweight chat-only work out of candidate search")
output_text = (root/"references/requirement-output-contract.md").read_text(encoding="utf-8")
for heading in ["需求结论", "这次会做", "完成标准", "下一步", "开发记录"]:
    if heading not in output_text: die(f"human output missing {heading}")
contract = json.loads((root/"evals/behavior-contract.json").read_text(encoding="utf-8"))
if contract.get("required_sections") != ["需求结论", "这次会做", "完成标准", "下一步", "开发记录"]:
    die("behavior contract must validate human-facing requirement output")
if len(text.splitlines()) > 95: die("SKILL.md too long")
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 65:
        die(f"{ref.name} too long")
for bad in ["skill-indexing-troubleshooting.md","real-compatibility.md","research-basis.md"]:
    if (root/"references"/bad).exists(): die(f"{bad} belongs in docs/")
print(root.name + " OK")
