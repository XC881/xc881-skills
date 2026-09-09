#!/usr/bin/env python3
"""Compatibility entry; new callers use frontend_design.py's domain/stack CLI."""

import argparse
import json
import sys

sys.dont_write_bytecode = True
from frontend_design import lookup


ALIASES = {"visual": "product", "data-display": "data", "platform": "mobile", "qa": "ux"}


def select(concern, terms, limit):
    concern = ALIASES.get(concern, concern)
    if not 1 <= limit <= 3:
        raise ValueError("limit must be between 1 and 3")
    if concern == "mobile":
        stack = "swiftui" if "ios" in terms.lower() else "jetpack-compose" if "android" in terms.lower() else None
        return lookup(terms, None if stack else "ux", stack, limit)
    domains = {"product": "product", "type-color": "color", "data": "chart", "ux": "ux"}
    if concern not in domains:
        raise ValueError(f"unknown concern: {concern}")
    return lookup(terms, domain=domains[concern], limit=limit)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("concern", nargs="?")
    parser.add_argument("terms", nargs="?")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = select("data", "time series trend", 1)
        assert result["count"] == 1 and result["candidates"][0]["record"].startswith("charts.csv#")
        assert select("ux", "zzzxqvplm", 1)["count"] == 0
        print("frontend design compatibility test OK")
        return
    if not args.concern or not args.terms:
        parser.error("concern and terms are required")
    try:
        print(json.dumps(select(args.concern, args.terms, args.limit), separators=(",", ":")))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
