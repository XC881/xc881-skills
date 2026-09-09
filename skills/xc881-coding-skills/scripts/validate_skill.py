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
    "xc881-code-quality-standard.md", "high-constraint-coding-policy.md",
    "no-code-comments-policy.md", "git-checkpoint-policy.md",
    "engineering-quality-rubric.md", "project-optimization.md",
    "adaptive-read-routing.md", "requirement-artifact-execution.md",
    "execution-checkpoint-and-tool-policy.md", "frontend-routing-and-design-read.md",
    "frontend-design-intelligence.md",
    "frontend-implementation-standard.md", "frontend-image-reference-workflow.md",
    "frontend-redesign-and-visual-qa.md", "frontend-pattern-catalog.md",
    "frontend-layout-and-platform.md", "frontend-visual-system-and-content.md",
    "frontend-states-and-accessibility.md", "frontend-motion-and-performance.md",
]
frontend_refs = [
    "frontend-routing-and-design-read.md", "frontend-design-intelligence.md",
    "frontend-implementation-standard.md",
    "frontend-image-reference-workflow.md", "frontend-redesign-and-visual-qa.md",
    "frontend-pattern-catalog.md",
]
for ref in required_refs:
    if not (root/"references"/ref).exists(): die(f"missing {ref}")
selector = root/"scripts/select_frontend_design.py"
if not selector.exists(): die("missing compact frontend design selector")
subprocess.run([sys.executable, str(selector), "--self-test"], check=True)
routing_text = (root/"references"/frontend_refs[0]).read_text(encoding="utf-8")
if "Just-In-Time Escalation" not in routing_text:
    die("frontend routing lacks just-in-time escalation")
if "automatically load the next reference" not in routing_text.lower():
    die("frontend routing must automatically load the next reference")
if "do not wait for another user request or handoff" not in routing_text.lower():
    die("frontend routing must not wait for a user handoff")
for ref in frontend_refs[1:]:
    if ref not in routing_text: die(f"frontend routing missing {ref}")
    if not re.search(r"automatically\s+load", (root/"references"/ref).read_text(encoding="utf-8"), re.I):
        die(f"{ref} must automatically escalate when its concern is reached")
implementation = (root/"references/frontend-implementation-standard.md").read_text(encoding="utf-8")
for ref in ["frontend-layout-and-platform.md", "frontend-visual-system-and-content.md",
            "frontend-states-and-accessibility.md", "frontend-motion-and-performance.md"]:
    if f"./references/{ref}" not in implementation:
        die(f"implementation route missing {ref}")
for a in ["openai.yaml","claude.yaml"]:
    t = (root/"agents"/a).read_text(encoding="utf-8")
    for k in ["interface:","display_name:","short_description:","default_prompt:","policy:",'allow_implicit_invocation: true']:
        if k not in t: die(f"{a} missing {k}")
    if "Auto-load the next-needed frontend ref" not in t:
        die(f"{a} must require automatic frontend reference escalation")
ev = json.loads((root/"evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev): die("need positive eval")
if not any(not e["should_trigger"] for e in ev): die("need negative eval")
required_rules = [
    "Read gate: explicit Coding invocation", "every write",
    "task/project complexity trigger", "Ordinary simple reads stay direct",
    "before opening project files or execution artifacts", "`read` or `change`",
    "Frontend design starts with routing", "Automatically load each relevant next ref", "only when its concern is reached", "substantial", "history line",
    "After compaction", "Never ask the user to say continue",
    "never `in-progress`", "Resume a blocked item as `ready`",
    "advance until terminal", "explicit stepwise/pause intent", "Do not scan `dev-notes`",
    "Do not read `index.md` by default", "its current item only",
    "Do not load previous/next", "stop and return to Requirement",
    "run only needed branches",
]
for rule in required_rules:
    if rule.lower() not in text.lower(): die(f"missing task-mode rule: {rule}")
if "use the write-first exact handoff; do not validate normally" not in text:
    die("queue mode must not run a normal process validator")
execution_text = (root/"references/requirement-artifact-execution.md").read_text(encoding="utf-8")
for rule in ["do not run a process validator in", "one coherent patch", "history.md", "old -> new",
             "Item `Status` is only `pending | ready | blocked | done | skipped`, never"]:
    if rule not in execution_text:
        die(f"requirement execution missing write-first rule: {rule}")
checkpoint_text = (root/"references/execution-checkpoint-and-tool-policy.md").read_text(encoding="utf-8")
if "never `in-progress`" not in checkpoint_text or "resume blocked items as `ready`" not in checkpoint_text:
    die("recovery checkpoint must keep in-progress as task-only")
design_text = (root/"references/frontend-design-intelligence.md").read_text(encoding="utf-8")
for rule in ["at most three candidates", "frontend_design.py", "full pinned upstream data",
             "Ordinary lookups never write files", "Do not retry with synonyms", "candidate-with-fallback"]:
    if rule not in design_text:
        die(f"design intelligence missing bounded selector rule: {rule}")
for workflow in ["instant read-only", "queue read-only", "instant change", "requirements then coding", "bugfix then coding"]:
    if not any(e["should_trigger"] and workflow in e["workflow"] for e in ev):
        die(f"need positive coding eval: {workflow}")
if not any(e["should_trigger"] and "known-cause coding" in e["workflow"] for e in ev):
    die("need positive known-cause coding eval")
if not any(not e["should_trigger"] and "simple direct read" in e["workflow"] for e in ev):
    die("need negative simple direct read eval")
if not any(e["should_trigger"] and "complex project read" in e["workflow"] for e in ev):
    die("need positive complex project read eval")
for workflow in ["frontend automatic just-in-time redesign", "image-to-code frontend automatic just-in-time", "frontend automatic just-in-time visual review", "frontend automatic implementation just-in-time", "frontend automatic design intelligence", "nonvisual UI behavior", "backend coding without frontend pack"]:
    if not any(e["should_trigger"] and workflow in e["workflow"] for e in ev):
        die(f"need positive coding eval: {workflow}")
if not any(not e["should_trigger"] and "image generation only" in e["workflow"] for e in ev):
    die("need negative image-only eval")
if text.lower().index("before opening project files or execution artifacts") > text.index("Classify action independently"):
    die("persistence mode must be classified before read/change action")
rubric_text = (root/"evals/behavior-rubric.json").read_text(encoding="utf-8")
for case in ["三个可运行队列项", "每完成一个队列项先停下来", "生产环境权限", "视觉重设计", "设计参考图", "文字溢出", "外观保持", "Node API", "React 表单", "跨页面医疗预约", "订单趋势"]:
    if case not in rubric_text: die(f"missing continuous-run rubric: {case}")
for assertion in ["automatically loads routing", "another user reference request"]:
    if assertion not in rubric_text: die(f"missing automatic frontend escalation rubric: {assertion}")
if len(text.splitlines()) > 170: die("SKILL.md too long")
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 160:
        die(f"{ref.name} too long")
for bad in ["skill-indexing-troubleshooting.md","real-compatibility.md","research-basis.md"]:
    if (root/"references"/bad).exists(): die(f"{bad} belongs in docs/")
print(root.name + " OK")
