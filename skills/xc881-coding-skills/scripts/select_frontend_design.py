#!/usr/bin/env python3
import argparse
import json
import re


CATALOG = {
    "product": [
        ("regulated-trust", "health healthcare medical finance fintech banking insurance government public compliance", "trust-first hierarchy, restrained density, explicit recovery and predictable actions", "unverified claims, decorative risk signals, or casual interaction patterns"),
        ("operational-density", "ops operations admin dashboard monitoring analytics devtool internal b2b", "scan and comparison first, persistent context, compact controls, and meaningful empty states", "marketing composition, nested cards, or decorative telemetry"),
        ("transactional-service", "booking reservation checkout ecommerce marketplace store delivery order appointment", "clear task flow, one primary action, truthful product evidence, and recovery feedback", "fake social proof, hidden fees, or ambiguous next actions"),
        ("editorial-brand", "portfolio editorial story campaign culture magazine agency creator", "content-led hierarchy, intentional type, relevant media, and one justified signature", "generic equal feature grids or copied identity assets"),
        ("balanced-product", "product app tool service workflow", "clear task hierarchy, semantic tokens, and a restrained system that can scale", "style changes without a product or user reason"),
    ],
    "type-color": [
        ("trust-readable", "health finance banking insurance government public compliance", "semantic roles, high contrast, stable type scale, and limited emphasis", "decorative urgency colors or low-contrast text"),
        ("dense-data", "dashboard analytics monitoring ops admin table comparison", "tabular numerals, compact hierarchy, neutral surfaces, and one semantic accent", "rainbow status systems or weak data contrast"),
        ("brand-expression", "portfolio editorial campaign culture luxury creative consumer", "one content-derived color world, distinct display/body roles, and disciplined accents", "a generic palette or decorative font pairing"),
        ("system-neutral", "app product tool service workflow", "existing semantic tokens, readable body type, and role-based color before raw hex values", "adding a font or palette without evidence"),
    ],
    "data": [
        ("time-series", "trend timeline time over daily weekly monthly history growth decline", "line or area with a clear time scale, comparison baseline, and accessible summary", "a decorative chart with no time question"),
        ("comparison", "compare comparison ranking rank category categories region team product", "sorted bars or a compact comparison table with direct labels", "pie charts for many comparable categories"),
        ("composition", "composition share percent percentage breakdown mix allocation", "stacked bars for change over time or a labeled part-to-whole view for few parts", "a donut with too many slices or color-only meaning"),
        ("distribution", "distribution spread range percentile histogram outlier variance", "histogram, box plot, or ordered distribution summary with outlier context", "averages that hide spread"),
        ("relationship", "relationship correlation scatter x y variable variables", "scatter or paired values with labeled axes and trend context", "implying causation from visual proximity"),
        ("status", "status alert health sla incident queue backlog", "status list, metric, threshold, and actionable drill-in before a chart", "a chart when the user needs an operational action"),
    ],
    "mobile": [
        ("ios-native", "ios iphone ipad apple", "iOS-native navigation, safe areas, readable type, and system-consistent feedback", "web-shaped controls inside a phone flow"),
        ("android-native", "android material compose", "Material navigation, touch targets, predictable back behavior, and system state feedback", "copying iOS navigation without product evidence"),
        ("touch-neutral", "mobile phone touch handheld responsive", "safe areas, reachable actions, visible alternatives to gestures, and narrow-screen priority", "desktop layout squeezed into a phone viewport"),
    ],
    "ux": [
        ("form-recovery", "form input validation checkout submit field error", "visible labels, local recovery, accessible errors, and clear submit feedback", "placeholder-only labels or error messages without a next action"),
        ("navigation-state", "navigation tab filter pagination route deep link back", "clear hierarchy, predictable return paths, and shareable state where relevant", "modal-based primary navigation or disappearing context"),
        ("async-feedback", "loading pending async retry timeout empty", "structure-matched loading, clear progress/retry, and an actionable empty state", "indefinite spinners or silent failures"),
        ("destructive-safety", "delete remove archive cancel destructive undo", "clear consequence, confirmation or undo, and separate danger treatment", "immediate irreversible action"),
        ("accessibility-detail", "keyboard focus screen reader aria contrast motion", "semantic controls, visible focus, meaningful labels, and reduced-motion behavior", "visual-only feedback or removed focus outlines"),
    ],
}
ALIASES = {"visual": "product", "data-display": "data", "platform": "mobile", "qa": "ux"}


def words(value):
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def select(concern, terms, limit):
    concern = ALIASES.get(concern, concern)
    if concern not in CATALOG:
        raise ValueError(f"unknown concern: {concern}")
    query = words(terms)
    ranked = []
    for key, keywords, decision, avoid in CATALOG[concern]:
        matched = sorted(query & words(keywords))
        ranked.append((len(matched), key, matched, decision, avoid))
    ranked.sort(key=lambda row: (-row[0], row[1]))
    matched = [row for row in ranked if row[0]]
    selected = (matched or ranked[:1])[:limit]
    return {
        "concern": concern,
        "candidates": [
            {
                "id": key,
                "matched_terms": terms_matched,
                "decision": decision,
                "avoid": avoid,
            }
            for _, key, terms_matched, decision, avoid in selected
        ],
    }


def self_test():
    assert select("product", "healthcare scheduling trust", 3)["candidates"][0]["id"] == "regulated-trust"
    assert select("data-display", "orders trend monthly", 3)["candidates"][0]["id"] == "time-series"
    assert select("platform", "ios settings", 3)["candidates"][0]["id"] == "ios-native"
    assert select("ux", "checkout form validation", 3)["candidates"][0]["id"] == "form-recovery"
    assert len(select("data", "comparison composition trend", 3)["candidates"]) <= 3


def main():
    parser = argparse.ArgumentParser(description="Return bounded frontend design candidates.")
    parser.add_argument("concern", nargs="?", help="product, type-color, data, mobile, or ux")
    parser.add_argument("terms", nargs="?", help="current concern terms")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("frontend design selector self-test OK")
        return
    if not args.concern or not args.terms:
        parser.error("concern and terms are required")
    if not 1 <= args.limit <= 3:
        parser.error("--limit must be between 1 and 3")
    try:
        result = select(args.concern, args.terms, args.limit)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
