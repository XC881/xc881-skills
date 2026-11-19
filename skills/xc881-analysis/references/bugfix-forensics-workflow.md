# Forensics

For regressions, include the relevant recent change in the evidence.

Rank plausible explanations by evidence fit and a falsifiable prediction; use as
many as needed to distinguish cause, not a fixed quota. For each live alternative,
name the observation that would reject it. Choose the smallest discriminating
read/repro before requesting instrumentation from Coding.

A hypothesis predicts the symptom. A supported cause also has a causal path or
controlled observation connecting trigger to failure and evidence distinguishing
the live alternatives. Separate the upstream invariant-violation site (producer
of bad state) from the downstream crash/symptom site (consumer): do not propose
silent defensive masking (`or {}` / broad catch) at the consumer when an upstream
contract is broken, and only relax the consumer when optional/null input is
legitimate domain data. A stack location or successful speculative patch alone
does not establish cause. Report confidence, supporting anchors, adjacent failure
hazards on the same path (in `需要注意`), and remaining gaps; use `unconfirmed`
when the discriminating check has not happened.

Temporary debug output is Coding-owned, prediction-specific, and must be removed
in its handoff. If blocked, return the exact missing observation.
