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
for ref in ['xc881-code-quality-standard.md', 'high-constraint-coding-policy.md', 'no-code-comments-policy.md', 'git-checkpoint-policy.md', 'engineering-quality-rubric.md', 'project-optimization.md', 'adaptive-read-routing.md', 'requirement-artifact-execution.md', 'execution-checkpoint-and-tool-policy.md']:
    if not (root/"references"/ref).exists(): die(f"missing {ref}")
for a in ["openai.yaml","claude.yaml"]:
    t = (root/"agents"/a).read_text(encoding="utf-8")
    for k in ["interface:","display_name:","short_description:","default_prompt:","policy:",'allow_implicit_invocation: true']:
        if k not in t: die(f"{a} missing {k}")
ev = json.loads((root/"evals/trigger-queries.json").read_text(encoding="utf-8"))
if not any(e["should_trigger"] for e in ev): die("need positive eval")
if not any(not e["should_trigger"] for e in ev): die("need negative eval")
for rule in ["Read gate: explicit Coding invocation", "every write", "task/project complexity trigger", "Ordinary simple reads stay direct", "before opening project files or execution artifacts", "`read` or `change`", "Queue loop:", "After context compaction", "Never ask the user to say continue", "task terminal", "explicit stepwise/pause intent", "Do not scan `dev-notes`", "Do not read `index.md` by default", "current queue item only", "Do not load previous/next", "stop and return to Requirement", "Run only the needed branch"]:
    if rule not in text: die(f"missing task-mode rule: {rule}")
for workflow in ["instant read-only", "queue read-only", "instant change", "requirements then coding", "bugfix then coding"]:
    if not any(e["should_trigger"] and workflow in e["workflow"] for e in ev):
        die(f"need positive coding eval: {workflow}")
if not any(e["should_trigger"] and "known-cause coding" in e["workflow"] for e in ev):
    die("need positive known-cause coding eval")
if not any(not e["should_trigger"] and "simple direct read" in e["workflow"] for e in ev):
    die("need negative simple direct read eval")
if not any(e["should_trigger"] and "complex project read" in e["workflow"] for e in ev):
    die("need positive complex project read eval")
if text.index("before opening project files or execution artifacts") > text.index("Classify action independently"):
    die("persistence mode must be classified before read/change action")
rubric_text = (root/"evals/behavior-rubric.json").read_text(encoding="utf-8")
for case in ["三个可运行队列项", "每完成一个队列项先停下来", "生产环境权限"]:
    if case not in rubric_text: die(f"missing continuous-run rubric: {case}")
if len(text.splitlines()) > 170: die("SKILL.md too long")
for ref in (root/"references").glob("*.md"):
    if len(ref.read_text(encoding="utf-8").splitlines()) > 160:
        die(f"{ref.name} too long")
for bad in ["skill-indexing-troubleshooting.md","real-compatibility.md","research-basis.md"]:
    if (root/"references"/bad).exists(): die(f"{bad} belongs in docs/")
print(root.name + " OK")
