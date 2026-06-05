# Git Checkpoint Push Policy

Use only when explicitly requested.

## Preflight

Inspect:

- `git status --short`
- current branch
- remotes
- upstream and divergence when remote exists
- GitHub-specific constraints when visible or relevant

## Staging

- Stage only relevant files.
- Avoid `git add .` unless the worktree contains only relevant changes.
- Do not include unrelated user changes.
- Do not commit secrets, credentials, `.env` secrets, local auth files, private keys, or generated secrets.

## Verification

Before committing, run the most appropriate lightweight check when practical:

- targeted tests
- build
- typecheck
- lint
- manual reproduction

If verification fails, do not push unless the user explicitly asks for the failing checkpoint to be saved.

## Commit message

Use Conventional Commits:

```text
type(optional-scope): imperative summary
```

Examples:

```text
feat(auth): add refresh token rotation
fix(api): handle missing workspace id
refactor(web): split dashboard data flow
test(auth): cover expired session behavior
```

## Push

- Do not force push unless explicitly requested.
- Do not bypass repository rules, branch protection, required reviews, signed commits, required checks, or secret scanning.
- Prefer feature branches when a protected default branch or PR workflow is likely.
- If remote rejects the push, report the exact blocker.

## Report

```text
Checkpoint:
- Commit:
- Branch:
- Push:
- Verification:
- Remaining changes:
```
