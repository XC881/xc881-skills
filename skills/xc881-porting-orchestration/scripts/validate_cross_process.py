#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import tempfile


CHAR_LIMIT = 4500
REQUIRED_FIELDS = (
    "Requirement artifact",
    "Magnitude",
    "Equivalence method",
    "Items",
    "Progress",
    "Open risks",
)


# Models naturally annotate field names with qualifiers (`Items (ledger):`,
# `Open risks（audit）:`); the canonical name stays the anchor.
_QUAL = r"(?:\s*[（(][^()（）]*[)）])?"


class ValidationError(Exception):
    pass


def validate(path):
    path = Path(path).resolve()
    if "cross-process" not in path.parts:
        raise ValidationError("ledger must live under dev-notes/cross-process")
    if not path.is_file():
        raise ValidationError(f"missing ledger {path}")
    text = path.read_text(encoding="utf-8")
    size = len(text)
    if size > CHAR_LIMIT:
        raise ValidationError(f"{path}: {size} chars exceeds limit {CHAR_LIMIT}")
    for name in REQUIRED_FIELDS:
        if name == "Items":
            present = re.search(rf"^Items{_QUAL}:\s*(?:.+|\n\s+-\s+.+)", text, re.M)
        else:
            present = re.search(rf"^{re.escape(name)}{_QUAL}:\s*.+$", text, re.M)
        if not present:
            raise ValidationError(f"missing field {name}")
    items_block = re.search(rf"^Items{_QUAL}:(.*?)(?=^[A-Z][A-Za-z ]*(?:\s*[（(][^()（）]*[)）])?:|\Z)", text, re.M | re.S)
    if items_block and re.search(r"\bin-progress\b", items_block.group(1)):
        raise ValidationError("Items must not use in-progress; linked current.md is authoritative")
    req_match = re.search(rf"^Requirement artifact{_QUAL}:\s*`?([^`\n]+?)`?\s*$", text, re.M)
    req_rel = req_match.group(1).strip().rstrip("/")
    if ".." in Path(req_rel).parts or not req_rel.startswith("dev-notes/req-process/"):
        raise ValidationError("Requirement artifact must point under dev-notes/req-process/<task>")
    idx = path.parts.index("cross-process")
    if idx >= 1 and path.parts[idx - 1] == "dev-notes":
        workspace = Path(*path.parts[: idx - 1])
        if (workspace / "dev-notes/req-process").exists():
            req_dir = workspace / req_rel
            for required in ("index.md", "current.md"):
                if not (req_dir / required).is_file():
                    raise ValidationError(f"broken Requirement artifact link: missing {req_rel}/{required}")
    return size


def write_fixture(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    req_dir = path.parents[2] / "dev-notes/req-process/test"
    req_dir.mkdir(parents=True, exist_ok=True)
    (req_dir / "index.md").write_text("ID: `RP-PORT-001`\n", encoding="utf-8")
    (req_dir / "current.md").write_text("Task: `RP-PORT-001`\nState: `ready`\n", encoding="utf-8")
    path.write_text(
        "Requirement artifact: dev-notes/req-process/test/\n"
        "Magnitude: module\nEquivalence method: ported tests\n"
        "Items: module-a ready\nProgress: 0 of 1\nOpen risks: none\n",
        encoding="utf-8",
    )


def expect_failure(path, label):
    try:
        validate(path)
    except ValidationError:
        return
    raise ValidationError(f"self-test did not detect {label}")


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "dev-notes/cross-process/test.md"
        write_fixture(path)
        validate(path)
        path.write_text(
            path.read_text(encoding="utf-8").replace("Progress: 0 of 1\n", ""),
            encoding="utf-8",
        )
        expect_failure(path, "missing field")
        write_fixture(path)
        path.write_text(
            path.read_text(encoding="utf-8") + "x" * CHAR_LIMIT,
            encoding="utf-8",
        )
        expect_failure(path, "oversized ledger")
        write_fixture(path)
        path.write_text(
            path.read_text(encoding="utf-8").replace("module-a ready", "module-a in-progress"),
            encoding="utf-8",
        )
        expect_failure(path, "item in-progress")
        write_fixture(path)
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "dev-notes/req-process/test/", "dev-notes/req-process/missing/"
            ),
            encoding="utf-8",
        )
        expect_failure(path, "broken Requirement artifact link")
        write_fixture(path)
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Open risks: none", "Open risks (semantic trap audit): none"
            ),
            encoding="utf-8",
        )
        validate(path)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        print("cross-process validator self-test OK")
        return
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_cross_process.py <ledger> | --self-test")
    try:
        size = validate(sys.argv[1])
    except ValidationError as error:
        raise SystemExit(f"cross-process invalid: {error}") from error
    print(f"cross-process OK: {size} chars")


if __name__ == "__main__":
    main()
