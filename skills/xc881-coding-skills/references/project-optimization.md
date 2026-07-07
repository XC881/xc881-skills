# Project Optimization

Legacy:

```text
inspect → find risk/coupling → rank P0-P3 → tests → extract pure logic → isolate side effects → verify
```

New project:

```text
change axes → domain/usecase/boundary → minimal contracts → verification
```

No broad rewrite unless requested.

Deepening:

- find shallow modules, leakage across seams, duplicated rules, and hard-to-test clusters
- prefer replacing shallow layers with one deeper interface over adding another layer
- when interface shape is uncertain, compare 2-3 designs on depth, locality, seam placement
- prototype only to answer one UI/logic question; keep the answer, delete or absorb the throwaway shell
