#!/usr/bin/env python3
"""Offline UI/UX Pro Max CLI with bounded results and exact record expansion."""

import argparse
import csv
import json
from pathlib import Path
import re
import sys


sys.dont_write_bytecode = True
VENDOR = Path(__file__).resolve().parents[1] / "vendor/ui-ux-pro-max"
OUTPUT_LIMIT = 4200
FIELDS = {
    "style": ("Style ID", "Style Category", "Preferred Mode", "Best For", "Accessibility", "Performance"),
    "color": ("Product Type", "Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent", "Background", "Foreground", "Card", "Card Foreground", "Muted", "Muted Foreground", "Border", "Destructive", "On Destructive", "Ring", "Notes"),
    "chart": ("Data Type", "Best Chart Type", "When to Use", "When NOT to Use", "Accessibility Notes", "A11y Fallback"),
    "landing": ("Pattern ID", "Pattern Name", "Section Order", "Primary CTA Placement"),
    "product": ("Product Type", "Primary Style Recommendation", "Dashboard Style (if applicable)", "Color Palette Focus"),
    "typography": ("Font Pairing Name", "Heading Font", "Body Font", "Best For"),
    "icons": ("Icon Name", "Library", "Semantic Role", "Allowed Contexts"),
    "google-fonts": ("Family", "Category", "Subsets", "Styles"),
    "gsap": ("Category", "Intensity Tier", "Trigger", "Do", "Don't", "Performance Notes"),
    "stack": ("Guideline", "Category", "Do", "Don't", "Severity", "Status", "Applies To", "Verified At", "Docs URL"),
}
GUIDELINE_FIELDS = ("Issue", "Category", "Platform", "Do", "Don't", "Severity")
SECTIONS = ("style", "colors", "typography", "layout", "constraints", "anti_patterns",
            "spacing_scale", "motion_snippet", "source_identities", "source_derivations",
            "decision_rules", "activated_rules", "key_effects", "severity", "dials",
            "reasoning_default", "project_name", "category", "request")


def engine():
    sys.path.insert(0, str(VENDOR / "scripts"))
    import core
    return core


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def rows(relative):
    allowed = json.loads((VENDOR / "upstream.json").read_text(encoding="utf-8"))["files"]
    if f"data/{relative}" not in allowed or not relative.endswith(".csv"):
        raise ValueError("record must name a bundled CSV file, not an arbitrary path")
    with (VENDOR / "data" / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def detail(record, fields=None):
    try:
        relative, ordinal = record.rsplit("#", 1)
        number = int(ordinal)
    except ValueError as error:
        raise ValueError("record format is relative.csv#N (1-based CSV record, not line)") from error
    records = rows(relative)
    if number < 1 or number > len(records):
        raise ValueError("record number outside dataset")
    row = records[number - 1]
    if fields:
        unknown = set(fields) - row.keys()
        if unknown:
            raise ValueError(f"unknown fields: {sorted(unknown)}; available: {list(row)}")
        row = {field: row[field] for field in fields}
    return {"record": record, "fields": row}


def lookup(query, domain=None, stack=None, limit=1):
    core = engine()
    result = (core.search_stack(query, stack, limit, diagnostics=True) if stack
              else core.search(query, domain, limit, diagnostics=True))
    if result.get("error"):
        raise ValueError(result["error"])
    output = {key: result[key] for key in ("domain", "stack", "file", "count", "redirect") if key in result}
    output["candidates"] = []
    output["reason"] = result.get("diagnostics", {}).get("reason", "ranked")
    if not result["count"]:
        output["status"] = "no-match"
        return output
    raw_rows = rows(result["file"])
    columns = FIELDS.get(result["domain"], GUIDELINE_FIELDS)
    for row in result["results"]:
        matches = [i for i, raw in enumerate(raw_rows, 1)
                   if all(raw.get(key) == value for key, value in row.items())]
        if not matches:
            raise ValueError("upstream result cannot be traced to a CSV record")
        selected = {field: row[field] for field in columns if row.get(field)}
        output["candidates"].append({
            "record": f"{result['file']}#{matches[0]}",
            "fields": selected,
            "more": [field for field in raw_rows[matches[0] - 1] if field not in selected],
        })
    output["detail"] = "Use --record ID [--fields FIELD ...] for complete values; expand omitted constraints before acting."
    # Omit whole fields with a locator, never truncate executable snippets or rules.
    while len(encode(output)) > OUTPUT_LIMIT - 160:
        options = [(len(encode(value)), candidate, key)
                   for candidate in output["candidates"]
                   for key, value in list(candidate["fields"].items())[1:]]
        if not options:
            raise ValueError("result metadata exceeds output budget; use a smaller --limit")
        _, candidate, key = max(options, key=lambda item: item[0])
        del candidate["fields"][key]
        candidate["more"].append(key)
        output["status"] = "needs-detail"
    return output


def design_system(query, project=None, surface="app", variance=None, motion=None, density=None):
    engine()
    from design_system import DesignSystemGenerator
    generated = DesignSystemGenerator().generate(query, project, variance, motion, density)
    if surface == "landing":
        generated["layout"] = {"surface": surface, **generated.pop("pattern")}
    else:
        generated.pop("pattern", None)
        generated["source_identities"].pop("landing", None)
        generated["layout"] = {"surface": surface, "rule": "Derive navigation and work area from the real task; no inferred marketing sections."}
    generated["fallback_fields"] = [key for key, value in generated["source_identities"].items() if not value]
    generated["status"] = "candidate-with-fallback" if generated["fallback_fields"] else "candidate"
    generated["authority"] = "Reconcile with user, brand, existing code and accessibility; not proof of fitness or compliance."
    generated["request"] = {"query": query, "surface": surface, "variance": variance,
                            "motion": motion, "density": density}
    return generated


def system_summary(generated):
    output = {key: generated[key] for key in
              ("status", "project_name", "category", "authority", "layout", "constraints", "fallback_fields", "source_identities")}
    output["style"] = {key: generated["style"][key] for key in ("id", "name", "accessibility")}
    output["colors"] = {key: value for key, value in generated["colors"].items()
                        if key not in {"notes", "cta", "text", "on_cta"}}
    output["typography"] = {key: generated["typography"][key] for key in ("heading", "body")}
    output["anti_patterns"] = generated["anti_patterns"]
    output["source_derivations"] = generated["source_derivations"]
    output["detail"] = "Reuse the same query/dials with --section NAME for full values."
    output["sections"] = list(SECTIONS)
    if len(encode(output)) > OUTPUT_LIMIT - 160:
        for key in ("anti_patterns", "constraints", "layout"):
            if len(encode(output)) <= OUTPUT_LIMIT - 160:
                break
            output[key] = {"required_detail": f"--section {key}"}
    if len(encode(output)) > OUTPUT_LIMIT - 160:
        raise ValueError("design summary exceeds budget; request one --section")
    return output


def persist_candidate(generated, project_root, slug):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 64:
        raise ValueError("slug must be lowercase kebab-case, at most 64 characters")
    root = project_root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project root must be an existing directory")
    target = root / "dev-notes/design-system" / slug / "MASTER.md"
    for part in (root / "dev-notes", target.parent.parent, target.parent, target):
        if part.is_symlink():
            raise ValueError("design-system path must not traverse symlinks")
    data = system_summary(generated)
    lines = ["# Design-System Candidate", "", "Status: proposal (Requirement reconciles before acceptance)",
             "Source revision: " + json.loads((VENDOR / "upstream.json").read_text(encoding="utf-8"))["revision"],
             "", "## Authority", generated["authority"], "", "## Decisions"]
    lines.append(f"- request: {encode(generated['request'])}")
    for key in ("project_name", "category", "layout", "style", "colors", "typography", "constraints", "anti_patterns", "fallback_fields", "source_identities", "source_derivations"):
        lines.append(f"- {key}: {encode(data.get(key))}")
    lines.extend(["", "## Boundaries", "No package installation or existing-token replacement is authorized.",
                  "Requirement supplies project-specific component, state, responsive and asset rules.", ""])
    content = "\n".join(lines)
    if len(content) > 3000:
        raise ValueError("candidate exceeds master budget; reconcile a bounded contract in Requirement before writing")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(content)
    return str(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", help="English task terms inferred by the agent; preserve named versions")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--domain", "-d")
    mode.add_argument("--stack", "-s")
    mode.add_argument("--design-system", action="store_true")
    mode.add_argument("--record", help="exact result locator: relative.csv#N")
    mode.add_argument("--catalog", action="store_true")
    parser.add_argument("--limit", "--max-results", type=int, choices=range(1, 4), default=1)
    parser.add_argument("--fields", nargs="+", help="complete fields from one --record")
    parser.add_argument("--section", choices=SECTIONS)
    parser.add_argument("--surface", choices=("app", "landing", "mobile"))
    parser.add_argument("--project-name", "-p")
    for dial in ("variance", "motion", "density"):
        parser.add_argument(f"--{dial}", type=int, choices=range(1, 11))
    parser.add_argument("--persist", action="store_true", help="explicitly create a candidate under dev-notes; never overwrite")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--slug")
    args = parser.parse_args()
    if args.fields and not args.record:
        parser.error("--fields requires --record")
    if any((args.section, args.surface, args.project_name, args.variance, args.motion,
            args.density, args.persist, args.project_root, args.slug)) and not args.design_system:
        parser.error("design-system options require --design-system")
    if args.persist and (not args.project_root or not args.slug):
        parser.error("--persist requires --project-root and --slug")
    if not args.persist and (args.project_root or args.slug):
        parser.error("--project-root/--slug require --persist")
    if args.section and args.persist:
        parser.error("select detail or persistence, not both")
    if (args.catalog or args.record) and args.query:
        parser.error("--catalog/--record do not accept a search query")
    if not args.catalog and not args.record and (not args.query or len(args.query) > 500):
        parser.error("provide a non-empty query of at most 500 characters")
    try:
        if args.catalog:
            core = engine()
            counts = json.loads((VENDOR / "data/catalog-summary.json").read_text(encoding="utf-8"))["counts"]
            result = {"domains": list(core.CSV_CONFIG), "stacks": core.AVAILABLE_STACKS, "counts": counts}
        elif args.record:
            result = detail(args.record, args.fields)
        elif args.design_system:
            generated = design_system(args.query, args.project_name, args.surface or "app",
                                      args.variance, args.motion, args.density)
            if args.persist:
                result = {"status": "proposal-written", "path": persist_candidate(generated, args.project_root, args.slug)}
            elif args.section:
                result = {"section": args.section, "value": generated[args.section]}
            else:
                result = system_summary(generated)
        else:
            core = engine()
            if args.domain and args.domain not in core.CSV_CONFIG:
                parser.error("unknown --domain; use --catalog")
            if args.stack and args.stack not in core.AVAILABLE_STACKS:
                parser.error("unknown --stack; use --catalog")
            result = lookup(args.query, args.domain, args.stack, args.limit)
        result["revision"] = json.loads((VENDOR / "upstream.json").read_text(encoding="utf-8"))["revision"]
        print(encode(result))
    except (ValueError, OSError, csv.Error, ImportError) as error:
        print(encode({"error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
