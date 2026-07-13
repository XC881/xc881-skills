#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import tempfile


CHAR_LIMIT = 3000
REQUIRED_FIELDS = (
    "Requirement artifact",
    "Magnitude",
    "Equivalence method",
    "Items",
    "Progress",
    "Open risks",
)


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
            present = re.search(r"^Items:\s*(?:.+|\n\s+-\s+.+)", text, re.M)
        else:
            present = re.search(rf"^{re.escape(name)}:\s*.+$", text, re.M)
        if not present:
            raise ValidationError(f"missing field {name}")
    return size


def write_fixture(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Requirement artifact: dev-notes/req-process/test/\n"
        "Magnitude: module\nEquivalence method: ported tests\n"
        "Items: module-a in-progress\nProgress: 0 of 1\nOpen risks: none\n",
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
