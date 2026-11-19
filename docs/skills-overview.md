# Skills

```text
$xc881-analysis              request/symptom/question -> Requirement|Bugfix|Solution branch -> evidence/AC/cause -> optional Coding chain
$xc881-coding-skills         readiness check -> instant|queue -> read|change -> evidence or patch/verify
$xc881-source-article-style  source evidence -> article outline/prose (+ Coding/Analysis for gaps)
$xc881-porting-orchestration classify goal -> boundary/plan -> optional port -> behavioral equivalence
```

`xc881-analysis` owns every analysis deliverable and pre-coding readiness gap
through three internal branches: Requirement (scope/AC/tracker), Bugfix
(diagnosis) and Solution (external evidence). Branch switches stay internal and
never create a delegation.

Routing combines user intent with actual task readiness: concrete edits/reads
enter Coding directly, while underspecified builds, unconfirmed bugs, or
cross-language ports run Analysis or Porting first and chain into Coding
automatically. Generic Q&A and simple exact/local/low-risk reads use no skill.

Reference routes load only missing guidance for the current concern. Coding
includes the full offline frontend engine/data behind conditional, bounded CLI output.
