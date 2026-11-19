#!/usr/bin/env python3
from pathlib import Path
import argparse
import tempfile


def find_candidates(root, terms, limit):
    root = Path(root)
    needles = {term.casefold().strip() for term in terms if term.strip()}
    if not root.is_dir() or not needles:
        return []
    ranked = []
    for index in sorted(root.glob("*/index.md")):
        name = index.parent.name.casefold()
        text = index.read_text(encoding="utf-8", errors="replace").casefold()
        matched = {term for term in needles if term in name or term in text}
        if not matched:
            continue
        score = len(matched) + sum(1 for term in matched if term in name)
        ranked.append((-score, str(index.parent)))
    ranked.sort()
    return [path for _, path in ranked[:limit]]


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "dev-notes/req-process"
        for name, goal in (("login-flow", "Login session protocol"), ("payment", "Payment retry")):
            task = root / name
            task.mkdir(parents=True)
            (task / "index.md").write_text(f"# {goal}\n", encoding="utf-8")
        found = find_candidates(root, ["login", "session"], 5)
        assert found == [str(root / "login-flow")]
        assert find_candidates(root, ["missing"], 5) == []


def main():
    parser = argparse.ArgumentParser(
        description="Return bounded req-process candidate paths; semantic matching is external."
    )
    parser.add_argument("root", nargs="?")
    parser.add_argument("terms", nargs="*")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("req-process candidate finder self-test OK")
        return
    if not args.root or not args.terms or not 1 <= args.limit <= 20:
        parser.error("provide <req-root> <identity terms> and --limit 1..20")
    for path in find_candidates(args.root, args.terms, args.limit):
        print(path)


if __name__ == "__main__":
    main()
