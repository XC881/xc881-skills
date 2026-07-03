#!/usr/bin/env python3
"""Offline behavior-data collector.

Walks local Codex rollout sessions, extracts real skill outputs (assistant
messages carrying a skill's output-contract), runs the structural-layer check
reused from skill_validation, and reports per-skill sample counts + structural
pass rate. Read-only over sessions; writes only under data/ (gitignored).

No network, no model. This produces the real denominator: how often each skill
actually emitted a structurally-complete output in genuine tasks.
"""
from pathlib import Path
import json
import sys

from skill_validation import check_structural_output

ROOT = Path(__file__).resolve().parents[1]
SESSIONS_DIR = Path.home() / ".codex" / "sessions"
OUT_DIR = ROOT / "data"

# Distinctive first-line anchor that marks an assistant message as an attempt to
# emit a given skill's output contract. Analysis anchors are highly distinctive;
# coding uses its final-response header.
ANCHORS = {
    "xc881-solution-research": "xc881 Solution:",
    "xc881-requirement-analysis": "xc881 Req:",
    "xc881-bugfix-research": "xc881 BugFix:",
    "xc881-coding-skills": "完成内容",
    "xc881-source-article-style": "本章结论",
}

# A message must show at least this many required sections to count as an output
# attempt at all; below it, the anchor is almost certainly a quote/meta-mention,
# not a real output. Kept explicit so the pass-rate denominator is defensible.
MIN_SECTIONS_TO_COUNT = 2

INJECTION_PREFIXES = (
    "<", "# AGENTS.md", "# codebase", "@/home", "<!--",
)

# A genuine skill product leads with its own contract. Session
# continuation/compaction turns instead lead with a handoff/objective recap that
# merely quotes contract section names; counting those inflates the denominator
# with non-outputs. Skip a message whose first non-empty line is such a recap.
CONTINUATION_MARKERS = (
    "handoff summary",
    "goal/current objective",
    "current objective:",
    "continue working toward",
    "continue the active",
    "continue the long-running",
    "continue long-running",
)


def is_continuation_artifact(text):
    for line in text.splitlines():
        stripped = line.strip().lower()
        if not stripped:
            continue
        return stripped.startswith(CONTINUATION_MARKERS)
    return False


def load_contracts():
    contracts = {}
    for skill in ANCHORS:
        path = ROOT / "skills" / skill / "evals" / "behavior-contract.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        contracts[skill] = {
            "required": data["required_sections"],
            "forbid": data.get("forbid_impl_code", False),
        }
    return contracts


def message_text(item):
    if item.get("type") != "message":
        return None, None
    role = item.get("role")
    parts = item.get("content")
    if role not in ("user", "assistant") or not isinstance(parts, list):
        return role, None
    chunks = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        if part.get("type") in ("input_text", "output_text"):
            text = part.get("text")
            if isinstance(text, str) and text.strip():
                chunks.append(text)
    return role, "\n".join(chunks) if chunks else None


def clean_user_query(text):
    """Keep the last meaningful user line, dropping injected context blocks."""
    if not text:
        return ""
    kept = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith(INJECTION_PREFIXES)
    ]
    joined = " ".join(kept).strip()
    return joined[:300]


def present_section_count(text, required):
    violations = check_structural_output(text, required, False)
    missing = sum(1 for v in violations if v.startswith("missing_section:"))
    return len(required) - missing


def classify(text, contracts):
    """Return (skill, violations) for the best-matching skill, or (None, None)."""
    best = None
    for skill, anchor in ANCHORS.items():
        if anchor not in text:
            continue
        required = contracts[skill]["required"]
        if present_section_count(text, required) < MIN_SECTIONS_TO_COUNT:
            continue
        violations = check_structural_output(
            text, required, contracts[skill]["forbid"]
        )
        # Prefer the skill this message most completely satisfies.
        score = len(violations)
        if best is None or score < best[2]:
            best = (skill, violations, score)
    if best is None:
        return None, None
    return best[0], best[1]


def iter_sessions():
    if not SESSIONS_DIR.exists():
        return
    yield from sorted(SESSIONS_DIR.rglob("rollout-*.jsonl"))


def main():
    contracts = load_contracts()
    OUT_DIR.mkdir(exist_ok=True)

    samples = []
    files = 0
    for path in iter_sessions():
        files += 1
        pending_query = ""
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for raw in lines:
            raw = raw.strip()
            if not raw:
                continue
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "response_item":
                continue
            role, text = message_text(rec.get("payload", {}))
            if text is None:
                continue
            if role == "user":
                q = clean_user_query(text)
                if q:
                    pending_query = q
                continue
            # assistant
            if is_continuation_artifact(text):
                continue
            skill, violations = classify(text, contracts)
            if skill is None:
                continue
            samples.append(
                {
                    "session": path.name,
                    "skill": skill,
                    "query": pending_query,
                    "output_excerpt": text[:500],
                    "violations": violations,
                    "structural_clean": not violations,
                }
            )

    samples_path = OUT_DIR / "behavior-samples.jsonl"
    with samples_path.open("w", encoding="utf-8") as fh:
        for s in samples:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")

    summary = {}
    for s in samples:
        row = summary.setdefault(s["skill"], {"candidates": 0, "clean": 0})
        row["candidates"] += 1
        if s["structural_clean"]:
            row["clean"] += 1
    for row in summary.values():
        c = row["candidates"]
        row["structural_pass_rate"] = round(row["clean"] / c, 3) if c else None

    report = {
        "sessions_scanned": files,
        "total_candidates": len(samples),
        "min_sections_to_count": MIN_SECTIONS_TO_COUNT,
        "note": (
            "candidate = assistant message with a skill's contract anchor and "
            "at least MIN_SECTIONS_TO_COUNT required sections present. "
            "structural_pass_rate measures form only (all sections present + "
            "non-empty, no forbidden impl code); it does NOT measure semantic "
            "correctness. Candidates may still include meta/quoted outputs."
        ),
        "by_skill": summary,
    }
    report_path = OUT_DIR / "behavior-report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"sessions scanned: {files}")
    print(f"samples written : {samples_path}")
    print(f"report written  : {report_path}")
    print("--- structural pass by skill ---")
    for skill in ANCHORS:
        row = summary.get(skill)
        if not row:
            print(f"  {skill}: 0 candidates")
            continue
        print(
            f"  {skill}: {row['clean']}/{row['candidates']} clean "
            f"({row['structural_pass_rate']})"
        )


if __name__ == "__main__":
    sys.exit(main())
