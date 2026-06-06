# Web Research Policy

Use only after `xc881-bugfix-research` has been explicitly invoked and external information may explain a bug or vulnerability.

## Source priority

1. Official project documentation
2. Official release notes/changelog
3. Official security advisory
4. CVE/NVD, GHSA, OSV, vendor advisory
5. CWE/OWASP class guidance
6. Maintainer issue/PR/discussion
7. Trusted forum answer with matching version/context
8. Blog posts only as supporting evidence

## Rules

- Match package/framework/runtime version.
- Prefer primary sources.
- Compare at least two sources for security-critical claims when practical.
- Separate sourced facts from hypotheses.
- Cite sources in the final response when web was used.
- Do not copy untrusted patch code.
- Do not use stale workaround if official fix exists.
- Note if advisory data is incomplete, delayed, or inconsistent.

## Compact output

```text
Web intel:
- fact:
- source:
- version match:
- relevance:
```
