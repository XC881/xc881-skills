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
required_refs = [
    # requirement branch
    "english-spec-first-policy.md", "implicit-requirement-inference.md",
    "existing-project-feature-analysis.md", "issue-tracker-triage.md",
    "requirement-process-artifact.md", "design-system-artifact.md",
    "requirement-output-contract.md", "requirement-quality-rubric.md",
    # bugfix branch
    "bugfix-forensics-workflow.md", "reproducer-verification-plan.md",
    "web-research-policy.md", "vulnerability-triage-policy.md",
    "bugfix-output-contract.md",
    # solution branch
    "english-spec-and-research-questions.md", "source-priority-policy.md",
    "paper-first-policy.md", "tech-stack-feasibility-policy.md",
    "solution-output-contract.md",
]
for ref in required_refs:
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
for rule in ["perform a simple exact/local/low-risk read here", "delegate a complex/tracked `read` to `$xc881-coding-skills`", "hand every write and selected complex/tracked read", "per-item “continue”", "no second invocation", "implementation intent is", "Diagnosis-only stops", "do not invent options", "decision-only;\nomit them for a single-fact check".replace("\n", " "), "per-branch dispatch"]:
    if rule not in text: die(f"missing workflow rule: {rule}")
if not re.search(r"one contract.*?never a second\s+contract", text, re.S):
    die("missing combined-deliverable contract rule")
ref_all = "\n".join(p.read_text(encoding="utf-8") for p in (root/"references").glob("*.md"))
if re.search(r"[Dd]elegate[^.\n]*\bbranch", ref_all):
    die("branch switches are not delegation; refs must not say 'delegate ... branch'")
spec_blocks = re.findall(r"```text\n(.*?)```", (root/"references/english-spec-first-policy.md").read_text(encoding="utf-8"), re.S)
rq_text = (root/"references/english-spec-and-research-questions.md").read_text(encoding="utf-8")
if not spec_blocks or "Unknowns:" not in spec_blocks[0] or "english-spec-first-policy.md" not in rq_text:
    die("english-spec-and-research-questions.md must defer Spec shape to english-spec-first-policy.md")
if "source-priority-policy.md" not in (root/"references/web-research-policy.md").read_text(encoding="utf-8"):
    die("web-research-policy must defer source ordering to source-priority-policy.md")
artifact_text = (root/"references/requirement-process-artifact.md").read_text(encoding="utf-8")
for section in ["## Goal", "## Contract", "## Targets", "## Constraints", "## Verification"]:
    if section not in artifact_text: die(f"artifact contract missing {section}")
if "Requirement reads it by default" not in artifact_text:
    die("artifact contract must define Requirement's default index.md read")
if "Coding does not read `index.md`" not in artifact_text:
    die("artifact contract must keep index.md out of normal Coding continuation")
for rule in ["Reuse Before Gate", "one semantic match", "never scan and guess"]:
    if rule not in artifact_text: die(f"artifact contract missing reuse rule: {rule}")
if "chat-only lightweight analysis does not scan" not in artifact_text:
    die("artifact contract must keep lightweight chat-only work out of candidate search")
for rule in ["never use Python to discover ordinary omissions", "explicit audit, observed-corruption repair, or repository/CI maintenance"]:
    if rule not in artifact_text:
        die(f"artifact contract missing write-first rule: {rule}")
if not re.search(r"derive the complete\s+linked write.*?one coherent patch", text, re.S):
    die("requirement workflow must construct one coherent process write")
if not re.search(r"not normal authoring or\s+handoff loops", text):
    die("requirement workflow must keep validators out of normal handoffs")
design_text = (root/"references/design-system-artifact.md").read_text(encoding="utf-8")
for rule in ["dev-notes/design-system", "MASTER.md", "Coding never scans", "One-surface work"]:
    if rule not in design_text:
        die(f"design-system contract missing rule: {rule}")
for banner in ["需求结论: <", "xc881 诊断: <", "xc881 调研: <", "single user-facing contract", "product-visible values"]:
    if banner not in text: die(f"SKILL.md output skeleton must include inline hint: {banner}")
for field_token in ["ID: <task-id>", "Task:", "Blocked by:"]:
    if field_token not in artifact_text: die(f"artifact contract missing machine field: {field_token}")
output_text = (root/"references/requirement-output-contract.md").read_text(encoding="utf-8")
for heading in ["需求结论", "这次会做", "完成标准", "下一步", "开发记录"]:
    if heading not in output_text: die(f"human output missing {heading}")
bugfix_text = (root/"references/bugfix-output-contract.md").read_text(encoding="utf-8")
for heading in ["xc881 诊断", "结论", "依据", "验证", "需要注意", "下一步"]:
    if heading not in bugfix_text: die(f"bugfix output missing {heading}")
solution_text = (root/"references/solution-output-contract.md").read_text(encoding="utf-8")
for heading in ["xc881 调研", "结论", "查证点", "依据", "需要注意", "下一步"]:
    if heading not in solution_text: die(f"solution output missing {heading}")
contract = json.loads((root/"evals/behavior-contract.json").read_text(encoding="utf-8"))
if contract.get("required_sections") != ["需求结论", "这次会做", "完成标准", "下一步", "开发记录"]:
    die("behavior contract must validate human-facing requirement output")
for mode in ["bugfix", "solution", "decision", "chat-only"]:
    if mode not in contract.get("modes", {}): die(f"behavior contract missing mode {mode}")
if not contract.get("anchor_modes"): die("behavior contract must map anchors to branch modes")
if contract["anchor_modes"].get("xc881 诊断") != "bugfix" or contract["anchor_modes"].get("xc881 调研") != "solution":
    die("behavior contract must anchor 诊断/调研 banners to their modes")
if not any(e["should_trigger"] and "single-fact solution research" in e["workflow"] for e in ev):
    die("need positive single-fact research eval")
if not any(e["should_trigger"] and "diagnosis only" in e["workflow"] for e in ev):
    die("need positive diagnosis-only eval")
if not any(not e["should_trigger"] and "known-cause coding" in e["workflow"] for e in ev):
    die("need negative known-cause coding eval")
if len(text.splitlines()) > 160: die("SKILL.md too long")
ref_line_overrides = {"requirement-process-artifact.md": 78}  # core protocol doc
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > ref_line_overrides.get(ref.name, 65):
        die(f"{ref.name} too long")
for bad in ["skill-indexing-troubleshooting.md","real-compatibility.md","research-basis.md"]:
    if (root/"references"/bad).exists(): die(f"{bad} belongs in docs/")
print(root.name + " OK")
