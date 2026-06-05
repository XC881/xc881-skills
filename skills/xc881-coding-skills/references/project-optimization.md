# Project Optimization

New project engineering happens after `$xc881-requirement-analysis`.

Legacy optimization:
1. inspect current behavior and entry points
2. find high-change/high-risk files
3. identify coupling, duplicated rules, framework/SDK leakage
4. rank P0/P1/P2/P3
5. add/identify behavior tests
6. extract pure logic
7. isolate side effects
8. introduce interfaces only where they reduce coupling
9. keep each step reversible and verifiable
