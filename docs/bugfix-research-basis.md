# Bugfix Research Basis

Repository-level background, not runtime reference.

The Bugfix branch of `xc881-analysis` is analysis-only and activates both for
standalone diagnosis requests and before Coding when a bug/regression/vulnerability
fix request has an unconfirmed root cause.

Reason:

- incidental error words do not trigger diagnosis when cause and patch are already concrete;
- unconfirmed bugs/vulnerabilities need tight reproducers, falsifiable hypotheses, and bounded version/advisory checks before patching;
- once root cause and minimal repair are supported and a fix was intended, Analysis chains into `xc881-coding-skills` automatically; diagnosis-only requests stop at the plan.

Flow:

```text
diagnosis intent OR unconfirmed fix request
-> tight reproducer + bounded repository/advisory evidence
-> falsifiable hypotheses -> supported cause + confidence
-> minimal repair + verification plan
-> automatic chain to xc881-coding-skills when a fix was intended (else 下一步: 仅诊断)
```
