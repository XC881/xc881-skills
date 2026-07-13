# Sources

Principle: survey/benchmark paper → original paper → standard/RFC → official docs.

Implementation: official docs → changelog → standard → maintainer GitHub issue/PR → benchmark/demo → forum → blog.

Security: vendor advisory → CVE/NVD/GHSA/OSV → CWE/OWASP → maintainer note.

Rules: primary source first; match version/context; cite only sources used; rank conflicts by authority+recency.

Tool budget: search broadly only to identify candidates, then open the smallest
authoritative set that answers the RQ. Keep claims and citations, not raw result
pages or repeated excerpts. Bound each tool output and batch independent lookups.

Requirement-delegated research: when handoff includes a req-process Artifact,
write bounded findings to `<artifact>/evidence/RQ-NNN-<slug>.md`; cite each
non-obvious claim and return path + affected RQ/decision to the same requirement
run. Do not duplicate the evidence in chat or another research artifact.

Other large research: write a bounded Markdown artifact in the repo/dev-notes
location already used by the project. Chat reports path + decision impact only.
