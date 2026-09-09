#!/usr/bin/env python3
"""Offline parser for Grok session files. No model calls, no OTEL."""

import json
from pathlib import Path

INJECTION_CLASSES = ("system", "skills", "rules")
INJECTION_SURFACE = "chat_history.jsonl"
SKILLS_MARKERS = (
    "Available Skills",
    "The following skills are available for use",
)
INJECTION_NOTE = (
    "Appended chat_history.jsonl system/user records only. A retained "
    "system/skills/rules line does not prove resent. HTTP request bytes "
    "unknown. No token savings."
)

USAGE_KEYS = (
    "inputTokens", "outputTokens", "cachedReadTokens", "cacheCreationTokens",
    "reasoningTokens", "totalTokens", "modelCalls",
)
USAGE_ALIASES = {
    "output_tokens": "outputTokens",
    "cachedReadTokens": "cachedReadTokens",
    "cacheCreationTokens": "cacheCreationTokens",
    "reasoning_tokens": "reasoningTokens",
    "total_tokens": "totalTokens",
    "model_calls": "modelCalls",
    "inputTokens": "inputTokens",
    "outputTokens": "outputTokens",
    "reasoningTokens": "reasoningTokens",
    "totalTokens": "totalTokens",
    "modelCalls": "modelCalls",
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def text_of(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return content.get("text") or content.get("content") or ""
    if isinstance(content, list):
        return "\n".join(text_of(part) for part in content if text_of(part))
    return str(content)


def parse_chat_history(path):
    records = []
    for row in load_jsonl(path):
        if not isinstance(row, dict):
            continue
        records.append({
            "type": row.get("type") or row.get("role") or "unknown",
            "text": text_of(row.get("content")),
        })
    return records


def _int(value):
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def normalize_usage(block):
    if not isinstance(block, dict):
        return {key: 0 for key in USAGE_KEYS}
    buckets = {key: 0 for key in USAGE_KEYS}
    for src, dest in USAGE_ALIASES.items():
        if src in block:
            buckets[dest] = _int(block.get(src))
    return buckets


def usage_completeness(block):
    if not isinstance(block, dict):
        return "missing"
    if block.get("usageIsIncomplete") or block.get("usage_is_incomplete"):
        return "incomplete"
    buckets = normalize_usage(block)
    token_keys = [key for key in USAGE_KEYS if key != "modelCalls"]
    if all(buckets[key] == 0 for key in token_keys):
        return "unknown"
    return "complete"


def empty_usage(status):
    return {"status": status, "session": None, "turns": [], "modelUsage": {}}


def parse_model_usage(block):
    raw = block.get("modelUsage") if isinstance(block, dict) else None
    if not isinstance(raw, dict):
        return {}
    models = {}
    for name, usage in raw.items():
        if not isinstance(usage, dict):
            models[str(name)] = empty_usage("unknown")
            continue
        models[str(name)] = {
            "status": usage_completeness(usage),
            "buckets": normalize_usage(usage),
        }
    return models


def parse_usage(path_or_obj):
    if path_or_obj is None:
        return empty_usage("missing")
    data = load_json(path_or_obj) if not isinstance(path_or_obj, dict) else path_or_obj
    session_block = data.get("session") if isinstance(data.get("session"), dict) else data
    turns = []
    for turn in data.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        turns.append({
            "turnNumber": turn.get("turnNumber") or turn.get("turn_number"),
            "status": usage_completeness(turn),
            "buckets": normalize_usage(turn),
        })
    return {
        "status": usage_completeness(session_block),
        "session": normalize_usage(session_block) if isinstance(session_block, dict) else None,
        "turns": turns,
        "modelUsage": parse_model_usage(session_block),
    }


def parse_signals(path):
    data = load_json(path)
    return {
        "compactionCount": _int(data.get("compactionCount")),
        "contextTokensUsed": _int(data.get("contextTokensUsed")),
        "toolCallCount": _int(data.get("toolCallCount")),
    }


def parse_compaction_checkpoints(directory):
    directory = Path(directory)
    if not directory.is_dir():
        return []
    checkpoints = []
    for path in sorted(directory.glob("*.json")):
        data = load_json(path)
        history = data.get("compacted_history") or []
        checkpoints.append({
            "checkpoint_id": data.get("checkpoint_id") or path.stem,
            "prompt_index_at_compaction": data.get("prompt_index_at_compaction"),
            "history_records": len(history) if isinstance(history, list) else 0,
        })
    return checkpoints


def child_session_dir(parent_dir, child_id):
    if not child_id:
        return None
    sibling = Path(parent_dir).parent / child_id
    return sibling if sibling.is_dir() else None


def parse_subagents(parent_dir):
    parent_dir = Path(parent_dir)
    root = parent_dir / "subagents"
    children = []
    if not root.is_dir():
        return children
    for meta_path in sorted(root.glob("*/meta.json")):
        meta = load_json(meta_path)
        child_id = meta.get("child_session_id") or meta.get("subagent_id")
        child_dir = child_session_dir(parent_dir, child_id)
        usage_path = (child_dir / "usage.json") if child_dir else None
        signals_path = (child_dir / "signals.json") if child_dir else None
        if child_dir is None or usage_path is None or not usage_path.is_file():
            usage = empty_usage("missing")
            attribution = "missing"
        else:
            usage = parse_usage(usage_path)
            attribution = usage["status"]
        children.append({
            "child_session_id": child_id,
            "subagent_type": meta.get("subagent_type"),
            "session_found": child_dir is not None,
            "attribution": attribution,
            "usage": usage,
            "signals": parse_signals(signals_path) if signals_path and signals_path.is_file() else None,
        })
    return children


def host_compaction(session_dir):
    session_dir = Path(session_dir)
    signals_path = session_dir / "signals.json"
    count = parse_signals(signals_path)["compactionCount"] if signals_path.is_file() else 0
    checkpoints = parse_compaction_checkpoints(session_dir / "compaction_checkpoints")
    return count > 0 or bool(checkpoints)


def unknown_injection_compare():
    return {
        "surface": INJECTION_SURFACE,
        "http_wire": "unknown",
        "classes": {name: "unknown" for name in INJECTION_CLASSES},
        "note": INJECTION_NOTE,
    }


def record_injection_classes(record):
    found = []
    text = record.get("text") or ""
    if record.get("type") == "system":
        found.append("system")
    if any(marker in text for marker in SKILLS_MARKERS):
        found.append("skills")
    if "<rules>" in text or "always_applied_workspace_rules" in text:
        found.append("rules")
    return found


def compare_chat_histories(before, after):
    result = unknown_injection_compare()
    if not isinstance(before, list) or not isinstance(after, list):
        return result
    if len(after) < len(before) or after[:len(before)] != before:
        return result
    seen = {name: False for name in INJECTION_CLASSES}
    for record in after[len(before):]:
        if record.get("type") not in ("system", "user"):
            continue
        for name in record_injection_classes(record):
            seen[name] = True
    result["classes"] = {
        name: "repeat" if seen[name] else "absent" for name in INJECTION_CLASSES
    }
    return result


def compare_session_dirs(before_dir, after_dir):
    before_path = Path(before_dir) / INJECTION_SURFACE
    after_path = Path(after_dir) / INJECTION_SURFACE
    if not before_path.is_file() or not after_path.is_file():
        return unknown_injection_compare()
    return compare_chat_histories(
        parse_chat_history(before_path), parse_chat_history(after_path)
    )


def rollup_injection_classes(class_maps):
    rolled = {}
    for name in INJECTION_CLASSES:
        states = [item.get(name) for item in class_maps]
        if "unknown" in states:
            rolled[name] = "unknown"
        elif "repeat" in states:
            rolled[name] = "repeat"
        elif states and all(state == "absent" for state in states):
            rolled[name] = "absent"
        else:
            rolled[name] = "unknown"
    return rolled


def compare_snapshots(dirs):
    existing = [Path(path) for path in dirs if Path(path).is_dir()]
    if len(existing) < 2:
        report = unknown_injection_compare()
        report["pairs"] = []
        return report
    pairs = []
    for index in range(len(existing) - 1):
        row = compare_session_dirs(existing[index], existing[index + 1])
        row["before"] = existing[index].name
        row["after"] = existing[index + 1].name
        pairs.append(row)
    return {
        "surface": INJECTION_SURFACE,
        "http_wire": "unknown",
        "classes": rollup_injection_classes([row["classes"] for row in pairs]),
        "pairs": pairs,
        "note": INJECTION_NOTE,
    }


def parse_session(session_dir):
    session_dir = Path(session_dir)
    history_path = session_dir / "chat_history.jsonl"
    usage_path = session_dir / "usage.json"
    signals_path = session_dir / "signals.json"
    return {
        "chat_history": parse_chat_history(history_path) if history_path.is_file() else [],
        "usage": parse_usage(usage_path) if usage_path.is_file() else parse_usage(None),
        "signals": parse_signals(signals_path) if signals_path.is_file() else {
            "compactionCount": 0, "contextTokensUsed": 0, "toolCallCount": 0,
        },
        "compaction_checkpoints": parse_compaction_checkpoints(
            session_dir / "compaction_checkpoints"
        ),
        "subagents": parse_subagents(session_dir),
        "host_compaction": host_compaction(session_dir),
        "http_wire": "unknown",
    }
