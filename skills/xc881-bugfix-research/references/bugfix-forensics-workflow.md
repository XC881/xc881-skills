# Forensics

For regressions, include the relevant recent change in the evidence.

Rank plausible explanations by evidence fit and a falsifiable prediction; use as
many as needed to distinguish cause, not a fixed quota. For each live alternative,
name the observation that would reject it. Choose the smallest discriminating
read/repro before requesting instrumentation from Coding.

A hypothesis predicts the symptom. A supported cause also has a causal path or
controlled observation connecting trigger to failure and evidence distinguishing
the live alternatives. A stack location or successful speculative patch alone
does not establish cause. Report confidence, supporting anchors and remaining gaps;
use `unconfirmed` when the discriminating check has not happened.

Temporary debug output is Coding-owned, prediction-specific, and must be removed
in its handoff. If blocked, return the exact missing observation.
