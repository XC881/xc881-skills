#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys
import tempfile


TASK_STATES = {"draft", "ready", "in-progress", "blocked", "done", "cancelled", "superseded"}
ITEM_STATES = {"pending", "ready", "blocked", "done", "skipped"}
TERMINAL_STATES = {"done", "cancelled", "superseded"}
INDEX_CHAR_LIMIT = 10000
CURRENT_CHAR_LIMIT = 1200
ACTIVE_ITEM_CHAR_LIMIT = 3500
REQUIRED_EXECUTION_SECTIONS = (
    "Goal",
    "Contract",
    "Targets",
    "Constraints",
    "Verification",
)


class ValidationError(Exception):
    pass


def validate_size(path, text, limit):
    size = len(text)
    if size > limit:
        raise ValidationError(f"{path}: {size} chars exceeds limit {limit}")


def field(text, name):
    match = re.search(rf"^{re.escape(name)}:\s*`?([^`\n]+?)`?\s*$", text, re.M)
    if not match:
        raise ValidationError(f"missing field {name}")
    return match.group(1).strip()


def values(raw):
    if raw.lower() == "none":
        return []
    return [value.strip().strip("`") for value in raw.split(",") if value.strip()]


def has_section(text, name):
    return bool(re.search(rf"^## {re.escape(name)}\s*$", text, re.M))


def section_body(text, name):
    match = re.search(
        rf"^(?:## )?{re.escape(name)}:?\s*$\n(.*?)"
        rf"(?=^(?:## )?(?:Progress|Last completed|Next action):?\s*$|\Z)",
        text,
        re.M | re.S,
    )
    return match.group(1).strip() if match else ""


def parse_items(queue_dir):
    items = {}
    paths = {}
    for path in sorted(queue_dir.glob("Q-*.md")):
        text = path.read_text(encoding="utf-8")
        item_id = field(text, "ID")
        if not re.fullmatch(r"Q-\d{3}", item_id):
            raise ValidationError(f"{path.name}: invalid ID {item_id}")
        if not path.name.startswith(item_id + "-"):
            raise ValidationError(f"{path.name}: filename/ID mismatch")
        if item_id in items:
            raise ValidationError(f"duplicate ID {item_id}")
        status = field(text, "Status")
        if status not in ITEM_STATES:
            raise ValidationError(f"{item_id}: invalid status {status}")
        items[item_id] = {
            "status": status,
            "previous": field(text, "Previous"),
            "next": field(text, "Next"),
            "blocked_by": values(field(text, "Blocked by")),
            "text": text,
        }
        paths[item_id] = path
    if not items:
        raise ValidationError("queue must contain at least one item")
    return items, paths


def validate_links(items):
    heads = [item_id for item_id, item in items.items() if item["previous"] == "none"]
    tails = [item_id for item_id, item in items.items() if item["next"] == "none"]
    if len(heads) != 1 or len(tails) != 1:
        raise ValidationError("queue must have exactly one head and one tail")
    for item_id, item in items.items():
        previous = item["previous"]
        next_id = item["next"]
        if previous != "none":
            if previous not in items:
                raise ValidationError(f"{item_id}: missing previous {previous}")
            if items[previous]["next"] != item_id:
                raise ValidationError(f"{item_id}: broken previous/next link")
        if next_id != "none":
            if next_id not in items:
                raise ValidationError(f"{item_id}: missing next {next_id}")
            if items[next_id]["previous"] != item_id:
                raise ValidationError(f"{item_id}: broken next/previous link")
    visited = []
    current = heads[0]
    while current != "none":
        if current in visited:
            raise ValidationError("queue link cycle")
        visited.append(current)
        current = items[current]["next"]
    if set(visited) != set(items):
        raise ValidationError("queue contains disconnected items")


def validate_dependencies(items):
    for item_id, item in items.items():
        for dependency in item["blocked_by"]:
            if dependency not in items:
                raise ValidationError(f"{item_id}: missing dependency {dependency}")
            if dependency == item_id:
                raise ValidationError(f"{item_id}: self dependency")
    visiting = set()
    visited = set()

    def visit(item_id):
        if item_id in visiting:
            raise ValidationError("dependency cycle")
        if item_id in visited:
            return
        visiting.add(item_id)
        for dependency in items[item_id]["blocked_by"]:
            visit(dependency)
        visiting.remove(item_id)
        visited.add(item_id)

    for item_id in items:
        visit(item_id)
    for item_id, item in items.items():
        unresolved = [
            dependency
            for dependency in item["blocked_by"]
            if items[dependency]["status"] not in {"done", "skipped"}
        ]
        if item["status"] == "ready" and unresolved:
            raise ValidationError(f"{item_id}: ready with unresolved dependencies")


def validate_execution_contracts(items):
    for item_id, item in items.items():
        if item["status"] in {"done", "skipped"}:
            continue
        missing = [
            section
            for section in REQUIRED_EXECUTION_SECTIONS
            if not has_section(item["text"], section)
        ]
        if missing:
            raise ValidationError(
                f"{item_id}: missing execution sections {', '.join(missing)}"
            )


def validate_current(root, task_id, items, paths):
    text = (root / "current.md").read_text(encoding="utf-8")
    if field(text, "Task") != task_id:
        raise ValidationError("current task ID mismatch")
    state = field(text, "State")
    if state not in TASK_STATES:
        raise ValidationError(f"invalid task state {state}")
    pointers = {}
    for name in ("Previous", "Current", "Next"):
        value = field(text, name)
        if value == "none":
            pointers[name.lower()] = None
            continue
        path = root / value
        if not path.is_file():
            raise ValidationError(f"missing current target {value}")
        pointers[name.lower()] = field(path.read_text(encoding="utf-8"), "ID")
    current_id = pointers["current"]
    if state in TERMINAL_STATES:
        if current_id is not None:
            raise ValidationError("terminal task must not have a current item")
        if pointers["next"] is not None:
            raise ValidationError("terminal task must not have a next item")
        if state == "done" and any(
            item["status"] not in {"done", "skipped"} for item in items.values()
        ):
            raise ValidationError("done task contains unfinished items")
        return
    if current_id is None:
        raise ValidationError("active task must have a current item")
    for section in ("Last completed", "Next action"):
        if not section_body(text, section):
            raise ValidationError(f"current.md missing resume summary: {section}")
    if current_id not in items or paths[current_id] != root / field(text, "Current"):
        raise ValidationError("current pointer is not a queue item")
    if items[current_id]["status"] in {"done", "skipped"}:
        raise ValidationError("current item cannot be done or skipped")
    if state == "blocked" and items[current_id]["status"] != "blocked":
        raise ValidationError("blocked task must point to a blocked item")
    if state != "blocked" and items[current_id]["status"] == "blocked":
        raise ValidationError("blocked current item requires blocked task state")
    expected_previous = None if items[current_id]["previous"] == "none" else items[current_id]["previous"]
    expected_next = None if items[current_id]["next"] == "none" else items[current_id]["next"]
    if pointers["previous"] != expected_previous or pointers["next"] != expected_next:
        raise ValidationError("current window does not match queue links")


def validate(root):
    root = Path(root).resolve()
    if "req-process" not in root.parts:
        raise ValidationError("artifact must live under dev-notes/req-process")
    for name in ("index.md", "current.md", "history.md"):
        if not (root / name).is_file():
            raise ValidationError(f"missing {name}")
    if not (root / "queue").is_dir():
        raise ValidationError("missing queue directory")
    index_path = root / "index.md"
    index_text = index_path.read_text(encoding="utf-8")
    validate_size(index_path, index_text, INDEX_CHAR_LIMIT)
    if re.search(r"^State:\s*", index_text, re.M):
        raise ValidationError(
            "index.md must not duplicate mutable State; current.md is authoritative"
        )
    current_path = root / "current.md"
    validate_size(
        current_path, current_path.read_text(encoding="utf-8"), CURRENT_CHAR_LIMIT
    )
    task_id = field(index_text, "ID")
    items, paths = parse_items(root / "queue")
    validate_links(items)
    validate_dependencies(items)
    validate_execution_contracts(items)
    for item_id, item in items.items():
        if item["status"] not in {"done", "skipped"}:
            validate_size(paths[item_id], item["text"], ACTIVE_ITEM_CHAR_LIMIT)
    validate_current(root, task_id, items, paths)
    if not (root / "history.md").read_text(encoding="utf-8").strip():
        raise ValidationError("history.md must not be empty")
    return len(items)


def write_fixture(root):
    (root / "queue").mkdir(parents=True)
    (root / "index.md").write_text("ID: `RP-TEST-001`\n", encoding="utf-8")
    (root / "history.md").write_text("# History\n\n- created\n", encoding="utf-8")
    (root / "current.md").write_text(
        "Task: `RP-TEST-001`\nState: `ready`\nPrevious: `queue/Q-010-first.md`\n"
        "Current: `queue/Q-020-second.md`\nNext: `none`\n\n"
        "## Last completed\nQ-010 completed\n\n"
        "## Next action\nexecute second slice\n",
        encoding="utf-8",
    )
    (root / "queue/Q-010-first.md").write_text(
        "ID: `Q-010`\nStatus: `done`\nPrevious: `none`\nNext: `Q-020`\n"
        "Blocked by: `none`\n",
        encoding="utf-8",
    )
    (root / "queue/Q-020-second.md").write_text(
        "ID: `Q-020`\nStatus: `ready`\nPrevious: `Q-010`\nNext: `none`\n"
        "Blocked by: `none`\n\n## Goal\nsecond slice\n\n## Contract\nAC-2\n"
        "\n## Targets\nmodule-b\n\n## Constraints\nno unrelated work\n"
        "\n## Verification\ncheck-b\n",
        encoding="utf-8",
    )


def write_terminal_fixture(root):
    (root / "queue").mkdir(parents=True)
    (root / "index.md").write_text("ID: `RP-TEST-002`\n", encoding="utf-8")
    (root / "history.md").write_text("# History\n\n- task done\n", encoding="utf-8")
    (root / "current.md").write_text(
        "Task: `RP-TEST-002`\nState: `done`\nPrevious: `queue/Q-010-first.md`\n"
        "Current: `none`\nNext: `none`\n",
        encoding="utf-8",
    )
    (root / "queue/Q-010-first.md").write_text(
        "ID: `Q-010`\nStatus: `done`\nPrevious: `none`\nNext: `none`\n"
        "Blocked by: `none`\n",
        encoding="utf-8",
    )


def reopen_fixture(root):
    first = root / "queue/Q-010-first.md"
    first.write_text(
        first.read_text(encoding="utf-8").replace("Next: `none`", "Next: `Q-020`"),
        encoding="utf-8",
    )
    (root / "queue/Q-020-second.md").write_text(
        "ID: `Q-020`\nStatus: `ready`\nPrevious: `Q-010`\nNext: `none`\n"
        "Blocked by: `Q-010`\n\n## Goal\nnew work\n\n## Contract\nAC-2\n"
        "\n## Targets\nmodule-b\n\n## Constraints\nkeep history\n"
        "\n## Verification\ncheck-b\n",
        encoding="utf-8",
    )
    (root / "current.md").write_text(
        "Task: `RP-TEST-002`\nState: `ready`\nPrevious: `queue/Q-010-first.md`\n"
        "Current: `queue/Q-020-second.md`\nNext: `none`\n\n"
        "## Last completed\nQ-010 completed\n\n## Next action\nexecute appended slice\n",
        encoding="utf-8",
    )


def expect_failure(root, label):
    try:
        validate(root)
    except ValidationError:
        return
    raise ValidationError(f"self-test did not detect {label}")


def self_test():
    mutations = {
        "missing current target": lambda root: (root / "current.md").write_text(
            (root / "current.md").read_text(encoding="utf-8").replace(
                "queue/Q-020-second.md", "queue/Q-999-missing.md"
            ),
            encoding="utf-8",
        ),
        "broken links": lambda root: (root / "queue/Q-020-second.md").write_text(
            (root / "queue/Q-020-second.md").read_text(encoding="utf-8").replace(
                "Previous: `Q-010`", "Previous: `none`"
            ),
            encoding="utf-8",
        ),
        "invalid state": lambda root: (root / "current.md").write_text(
            (root / "current.md").read_text(encoding="utf-8").replace(
                "State: `ready`", "State: `unknown`"
            ),
            encoding="utf-8",
        ),
        "dependency cycle": lambda root: [
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Blocked by: `none`", f"Blocked by: `{dependency}`"
                ),
                encoding="utf-8",
            )
            for path, dependency in (
                (root / "queue/Q-010-first.md", "Q-020"),
                (root / "queue/Q-020-second.md", "Q-010"),
            )
        ],
        "missing execution contract": lambda root: (root / "queue/Q-020-second.md").write_text(
            (root / "queue/Q-020-second.md").read_text(encoding="utf-8").replace(
                "## Contract\nAC-2\n\n", ""
            ),
            encoding="utf-8",
        ),
        "missing resume summary": lambda root: (root / "current.md").write_text(
            (root / "current.md").read_text(encoding="utf-8").replace(
                "## Next action\nexecute second slice\n", ""
            ),
            encoding="utf-8",
        ),
        "oversized current": lambda root: (root / "current.md").write_text(
            (root / "current.md").read_text(encoding="utf-8")
            + "x" * CURRENT_CHAR_LIMIT,
            encoding="utf-8",
        ),
        "oversized active item": lambda root: (root / "queue/Q-020-second.md").write_text(
            (root / "queue/Q-020-second.md").read_text(encoding="utf-8")
            + "x" * ACTIVE_ITEM_CHAR_LIMIT,
            encoding="utf-8",
        ),
        "oversized index": lambda root: (root / "index.md").write_text(
            (root / "index.md").read_text(encoding="utf-8")
            + "x" * INDEX_CHAR_LIMIT,
            encoding="utf-8",
        ),
        "duplicate index state": lambda root: (root / "index.md").write_text(
            (root / "index.md").read_text(encoding="utf-8")
            + "State: `ready`\n",
            encoding="utf-8",
        ),
    }
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "dev-notes/req-process/test"
        write_fixture(base)
        validate(base)
        for label, mutate in mutations.items():
            shutil.rmtree(base)
            write_fixture(base)
            mutate(base)
            expect_failure(base, label)
        shutil.rmtree(base)
        write_fixture(base)
        duplicate = base / "queue/Q-020-duplicate.md"
        duplicate.write_text(
            "ID: `Q-020`\nStatus: `pending`\nPrevious: `Q-020`\nNext: `none`\n"
            "Blocked by: `none`\n",
            encoding="utf-8",
        )
        expect_failure(base, "duplicate ID")
        shutil.rmtree(base)
        write_terminal_fixture(base)
        validate(base)
        reopen_fixture(base)
        validate(base)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        print("req-process validator self-test OK")
        return
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_req_process.py <task-dir> | --self-test")
    try:
        count = validate(sys.argv[1])
    except ValidationError as error:
        raise SystemExit(f"req-process invalid: {error}") from error
    print(f"req-process OK: {count} queue items")


if __name__ == "__main__":
    main()
