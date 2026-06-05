# Implicit Requirement Inference Guide

Use this guide to discover requirements that are not explicitly stated but are necessary consequences or dependencies of stated requirements.

## Core idea

If the user says A and B, but A and B cannot work safely without C, identify C as an inferred requirement.

Example:

```text
Explicit:
A: users can invite teammates
B: invited teammates can join a workspace

Inferred:
C1: the system needs invitation tokens
C2: invitations need expiration and revocation
C3: only authorized roles may invite teammates
C4: acceptance should create membership
C5: duplicate invitation handling is needed
C6: invite events should be auditable
```

## Inference lenses

Check each explicit requirement through these lenses:

1. Prerequisites
2. Dependencies
3. Consequences
4. States and lifecycle
5. Permissions and security
6. Data ownership and retention
7. Failure and recovery
8. Observability and audit
9. Notifications
10. Compatibility and migration
11. Non-functional qualities
12. Abuse and edge cases

## Output pattern

```text
IR-001:
Derived from:
Type:
Reasoning:
Confidence:
Needs confirmation:
Acceptance criteria:
```

## Confidence guidance

High:
- almost certainly required for the explicit requirement to work safely

Medium:
- likely required, but product choice may vary

Low:
- plausible implication, but should be confirmed before implementation

## Do not

- hide inferred requirements inside confirmed requirements
- overfit to implementation details
- infer expensive scope without marking it as optional or needing confirmation
- skip security, permissions, failure states, or migration consequences
