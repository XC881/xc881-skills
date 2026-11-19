#!/usr/bin/env python3
"""Score selected outputs against structural contracts."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from skill_validation import (
    _is_header_of, evaluate_output, output_contract_mode, output_lines,
    validate_output_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def load_contracts(root=ROOT):
    manifest = json.loads((root / "skills-manifest.json").read_text(encoding="utf-8"))
    contracts = {}
    for skill in manifest["skills"]:
        name = skill["name"]
        contract = json.loads((root / "skills" / name / "evals/behavior-contract.json").read_text(encoding="utf-8"))
        if contract.get("skill") != name:
            raise ValueError(f"output contract owner mismatch: {name}")
        validate_output_contract(contract)
        contracts[name] = contract
    return contracts


def classify(text, contracts):
    """Recognize a leading contract, not a quote or a completeness-selected mode."""
    lines = [(line, allowed) for line, allowed in output_lines(text) if line.strip()]
    if lines and lines[0][1] and lines[0][0].startswith("# ") and not any(
        _is_header_of(lines[0][0], anchor)
        for contract in contracts.values() for anchor in contract["anchors"]
    ):
        # A full article may have its own title before the first contract heading.
        lines = lines[1:]
    if not lines or not lines[0][1]:
        return None, "no_leading_contract"
    first = lines[0][0]
    matches = [name for name, contract in contracts.items()
               if any(_is_header_of(first, anchor) for anchor in contract["anchors"])]
    if len(matches) != 1:
        return None, "ambiguous_contract" if matches else "no_leading_contract"
    return matches[0], None


def resolve_mode(text, contract):
    """Pick the contract mode from the leading anchor, else full."""
    anchor_modes = contract.get("anchor_modes")
    if not anchor_modes:
        return "full"
    lines = [(line, allowed) for line, allowed in output_lines(text) if line.strip()]
    if lines and lines[0][1] and lines[0][0].startswith("# ") and not any(
        _is_header_of(lines[0][0], anchor) for anchor in anchor_modes
    ):
        lines = lines[1:]
    if lines and lines[0][1]:
        for anchor in anchor_modes:
            if _is_header_of(lines[0][0], anchor):
                return anchor_modes[anchor]
    return "full"


def collect(paths, contracts, skill=None, mode=None):
    samples, excluded = [], Counter()
    for path in paths:
        with path.open(encoding="utf-8") as source:
            for number, raw in enumerate(source, 1):
                if not raw.strip():
                    continue
                try:
                    record = json.loads(raw)
                except json.JSONDecodeError:
                    excluded["malformed_json"] += 1
                    continue
                text = record.get("text") if isinstance(record, dict) else None
                if not isinstance(text, str) or not text:
                    excluded["malformed_record"] += 1
                    continue
                owner, reason = (skill, None) if skill else classify(text, contracts)
                selected_mode = mode or (resolve_mode(text, contracts[owner]) if owner else None)
                result = evaluate_output(text, contracts[owner], selected_mode) if owner else {
                    "status": "unscored", "reason": reason, "violations": [],
                }
                samples.append({
                    "source": str(path.resolve()), "line": number, "skill": owner,
                    "mode": selected_mode,
                    "attribution": "explicit" if skill else "leading_contract",
                    "output_sha256": hashlib.sha256(text.encode()).hexdigest(), **result,
                })
    return samples, dict(excluded)


def summarize(samples, excluded):
    by_skill = {}
    for sample in samples:
        row = by_skill.setdefault(sample["skill"] or "unattributed", {"pass": 0, "fail": 0, "unscored": 0})
        row[sample["status"]] += 1
    for row in by_skill.values():
        row["scored"] = row["pass"] + row["fail"]
        row["structural_pass_rate"] = round(row["pass"] / row["scored"], 3) if row["scored"] else None
    return {
        "eligible_messages": len(samples), "by_skill": by_skill, "excluded": excluded,
        "collection_complete": not any(excluded.get(reason) for reason in ("malformed_json", "malformed_record")),
        "note": "Structural form against the output contract. The denominator is scored records in the given files. Prose and unknown modes are unscored. Auto-attributed mode is full; use --skill/--mode for lightweight or decision outputs. Samples store locations, hashes and violations.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, nargs="+", help="explicit JSONL files")
    parser.add_argument("--skill", help="known owner of these test outputs; do not mix owners in one run")
    parser.add_argument("--mode", help="known response mode: full, prose, or a contract-defined mode")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args(argv)
    try:
        contracts = load_contracts()
        if args.mode and not args.skill:
            parser.error("--mode requires task-known --skill")
        if args.skill:
            if args.skill not in contracts:
                parser.error(f"unknown skill: {args.skill}")
            output_contract_mode(contracts[args.skill], args.mode or "full")
        paths = list(dict.fromkeys(path.resolve() for path in args.inputs))
        if any(not path.is_file() for path in paths):
            parser.error("every input must be an existing file")
        outputs = [args.out_dir / name for name in ("behavior-samples.jsonl", "behavior-report.json")]
        if any(output.resolve() in paths for output in outputs):
            parser.error("output must not overwrite an input file")
        samples, excluded = collect(paths, contracts, args.skill, args.mode)
        report = {"input_files": len(paths), **summarize(samples, excluded)}
        args.out_dir.mkdir(parents=True, exist_ok=True)
        outputs[0].write_text("".join(json.dumps(sample, ensure_ascii=False) + "\n" for sample in samples), encoding="utf-8")
        outputs[1].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["collection_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
