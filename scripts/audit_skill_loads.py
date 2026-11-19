#!/usr/bin/env python3
"""Report skill entry and declared branch sizes."""

import argparse
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def validate_instruction_paths(root, owner, reads):
    if not isinstance(reads, list) or not all(isinstance(item, str) for item in reads):
        raise ValueError("instruction reads must be a list of paths")
    if len(set(reads)) != len(reads):
        raise ValueError(f"duplicate instruction read: {owner}")
    for relative in reads:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or not (
                relative == "SKILL.md" or relative.startswith("references/")):
            raise ValueError(f"runtime scenario loads non-instruction payload: {relative}")
        if not (root / "skills" / owner / path).is_file():
            raise ValueError(f"missing load path: {owner}/{relative}")


def validate_continuations(root=ROOT):
    scenarios = json.loads((root / "evals/skill-load-paths.json").read_text(encoding="utf-8"))["continuations"]
    owners = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    seen = set()
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("continuation scenarios must be a non-empty list")
    for scenario in scenarios:
        for field in ("id", "precondition", "quality"):
            if not isinstance(scenario.get(field), str) or not scenario[field].strip():
                raise ValueError(f"continuation scenario needs {field}")
        if scenario["id"] in seen or scenario["owner"] not in owners:
            raise ValueError(f"duplicate continuation or unknown owner: {scenario['id']}")
        seen.add(scenario["id"])
        if "executable" in scenario:
            raise ValueError(f"continuation must not include executable: {scenario['id']}")
        if not isinstance(scenario.get("turns"), list) or not scenario["turns"]:
            raise ValueError(f"continuation has no turns: {scenario['id']}")
        for turn in scenario["turns"]:
            if not isinstance(turn.get("request"), str) or not turn["request"].strip():
                raise ValueError(f"continuation turn needs a request: {scenario['id']}")
            validate_instruction_paths(root, scenario["owner"], turn["reads"])
    if {scenario["owner"] for scenario in scenarios} != owners:
        raise ValueError("continuation scenarios must cover every skill")
    return scenarios


def validate_cases(root=ROOT):
    cases = json.loads((root / "evals/skill-load-paths.json").read_text(encoding="utf-8"))["cases"]
    owners = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    seen = set()
    for case in cases:
        if case["id"] in seen:
            raise ValueError(f"duplicate load case: {case['id']}")
        seen.add(case["id"])
        owner, reads = case["owner"], case["reads"]
        if owner is None:
            if reads:
                raise ValueError("no-skill case must not read a skill")
            continue
        if owner not in owners or not reads or reads[0] != "SKILL.md":
            raise ValueError(f"invalid entry path: {case['id']}")
        validate_instruction_paths(root, owner, reads)
    if {case["owner"] for case in cases if case["owner"]} != owners:
        raise ValueError("load scenarios must cover every skill")
    validate_continuations(root)
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", help="Git revision for entry and declared-path comparison")
    parser.add_argument("--encoding", help="optional installed tiktoken encoding; no dependency installation")
    args = parser.parse_args()
    measure = len
    unit = "chars"
    if args.encoding:
        try:
            import tiktoken
        except ImportError:
            parser.error("tiktoken is not installed; omit --encoding for character counts")
        encoding = tiktoken.get_encoding(args.encoding)
        measure = lambda text: len(encoding.encode(text, disallowed_special=()))
        unit = f"tokens ({args.encoding})"
    print(f"Entry sizes [{unit}]")
    current_total = before_total = 0
    previous = {}

    def baseline_size(relative):
        if relative not in previous:
            result = subprocess.run(["git", "-C", str(ROOT), "show", f"{args.baseline}:{relative}"],
                                    capture_output=True, text=True)
            previous[relative] = measure(result.stdout) if result.returncode == 0 else None
        return previous[relative]

    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        current = measure(path.read_text(encoding="utf-8"))
        current_total += current
        before = None
        if args.baseline:
            before = baseline_size(str(path.relative_to(ROOT)))
            if before is not None:
                before_total += before
        comparison = f"{before:5d} -> " if before is not None else ("  new -> " if args.baseline else "")
        print(f"{comparison}{current:5d} {path.parent.name}")
    print(f"total: {before_total if args.baseline else '-'} -> {current_total} {unit}")
    print("Declared cold instruction paths; project/artifact reads excluded:")
    for case in validate_cases():
        size = sum(measure((ROOT / "skills" / case["owner"] / relative).read_text(encoding="utf-8"))
                   for relative in case["reads"])
        output = case.get("tool_output_max_chars")
        suffix = f"; tool output <= {output} chars separately" if output else ""
        comparison = ""
        if args.baseline:
            base_sizes = [baseline_size(f"skills/{case['owner']}/{relative}")
                          for relative in case.get("baseline_reads", case["reads"])]
            comparison = f"{sum(base_sizes):5d} -> " if all(s is not None for s in base_sizes) else "  new -> "
        print(f"{comparison}{size:5d} {case['id']}{suffix}")
    print("Declared continuation tool reads under fixture preconditions:")
    for scenario in validate_continuations():
        counts = " -> ".join(str(len(turn["reads"])) for turn in scenario["turns"])
        print(f"{scenario['id']}: {counts}")


if __name__ == "__main__":
    main()
