# Sources

Principle: original paper/standard for the claim; survey for discovery, benchmark for applicability.

Implementation: official docs → changelog → standard → maintainer GitHub issue/PR → benchmark/demo → forum → blog.

Security: vendor advisory → CVE/NVD/GHSA/OSV → CWE/OWASP → maintainer note.

Resolve conflicts by scope/version fit before authority/recency: newer general
guidance does not settle a version-specific claim. Pin cited claims to the exact
library/runtime/protocol version (or mark version-unverified) and preserve
unresolved conflict and impact.

Start at a known primary source; broaden only to locate missing evidence. Stop
when blocking RQs are supported, not after a source-count quota. Keep used claims,
citations and limits, not result pages; bound outputs and batch independent lookups.

Research serving a Requirement run: when it carries a req-process Artifact,
write bounded findings to `<artifact>/evidence/RQ-NNN-<slug>.md`; reuse an exact
supplied evidence path for the same RQ. Cite non-obvious claims; return path,
affected decision, uncertainty and next action to the same Requirement run.
Do not duplicate evidence in chat or another artifact; do not store verification logs.

Other large research: write a bounded Markdown artifact in the repo/dev-notes
location already used by the project. Chat reports path + decision impact only.
