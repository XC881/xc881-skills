# Git Checkpoint Push Policy

Use only when explicitly requested.

Preflight:
- git status --short
- branch
- remotes
- upstream/divergence when relevant

Rules:
- stage relevant files only
- no unrelated user changes
- no secrets
- verify when practical
- Conventional Commits
- no force push unless explicitly requested
- report commit, branch, push result, verification, remaining changes
