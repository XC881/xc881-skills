# Frontend Design Intelligence

Automatically load this reference when substantial new/reworked UI has no reusable
design system, or an active visual/UX decision remains unresolved after the Design
Read. Reuse adequate user, brand, frame, token and component evidence first.

## Default Baseline

For eligible new/reworked UI, generate one project-specific candidate by default:

```bash
python <coding-skill>/scripts/frontend_design.py "appointment scheduling operations dashboard accessible" --design-system --surface app
```

Resolve `<coding-skill>` from this skill's installed directory, not the project
working directory. Use `landing` only for an actual landing page, `mobile` for a
mobile surface; app work must not inherit marketing sections. Translate a short
product/workflow phrase internally, not the entire brief. Keep negations, framework
versions and implementation instructions out of the generator query; reconcile
them against the result. Preserve versions in a version-dependent stack lookup.
Do not ask the user to translate or manually invoke a skill/tool.

The CLI uses the full pinned upstream data and generator locally. Python 3.9+ is
needed only for lookup/generation; if unavailable, report the lookup limit and use
project evidence without installing anything or pretending a database match.
Existing-system work and narrow evidence-complete changes skip generation.

## Concern Lookup

For one remaining gap, query its domain or relevant stack. A named framework alone
is not a gap: query it only for a specific API/pattern compatibility decision.
After a usable baseline, resolve a font/color/rule gap by its domain, not another
whole-system generation. Start with one result;
use `--limit 2` or `3` only for a real comparison (at most three candidates).

```bash
python <coding-skill>/scripts/frontend_design.py "time series trend" --domain chart
python <coding-skill>/scripts/frontend_design.py "form accessibility react 18" --stack react
python <coding-skill>/scripts/frontend_design.py --record 'stacks/react.csv#46' --fields 'Code Good' "Don't"
```

Use the record ID returned by the actual query, not the illustrative ID above.
Supported domains: `product`, `style`, `color`, `typography`, `google-fonts`,
`chart`, `icons`, `landing`, `ux`, `web`, `react`, `gsap`. Use `--catalog` only
when the needed domain/stack name is unknown, not at every activation.
Existing icon/motion libraries win; the icon dataset is Phosphor, not Lucide,
and `gsap` examples do not authorize adding that package.

## Bounded Reads

Run the CLI; never read its Python source, CSVs, full inventory, or vendor docs for
a normal lookup. Default JSON is <=4,200 characters; omitted fields retain exact
record locators, never chopped code. Expand only the fields needed to apply a
rule/snippet safely, especially omitted constraints and applicability.
For generator detail, repeat the same query/options with `--section colors`,
`style`, `typography`, `constraints`, `spacing_scale`, or another returned section.
Reuse the result while its inputs remain valid; do not regenerate at each page.

`no-match` means no evidence, and `candidate-with-fallback` names missing sources.
Do not retry with synonyms in a loop. Correct a demonstrated language/domain/version
error once; otherwise use local evidence or bounded `$xc881-analysis` (Solution branch) research for a
blocking external fact. Never label fallback as a catalog recommendation.

## Reconcile Before Applying

Check surface/task fit, existing design authority, locale/font coverage,
accessibility risks, semantic contrast, dependency availability and version
applicability. Catalog constraints are proposals, not verified obligations or
compliance. Reject incompatible choices, not the project constraint; a high-risk
style is not justified by its recommendation rank. Report only the resulting
decision and a material conflict, not the full generator output.

When reusable decisions need a durable contract, automatically delegate bounded
evidence to `$xc881-analysis` (Requirement branch). It reconciles and writes the accepted master under
`dev-notes/design-system/<slug>/MASTER.md`, with named surface overrides only.
Coding consumes exact handoff paths, never scans for masters or creates a second
authority. Ordinary lookups never write files. The optional CLI `--persist`
creates a proposal only, requires explicit project root/slug, and never overwrites;
Analysis's accepted write-first contract remains the execution authority.

Automatically load implementation, image, redesign/QA, or pattern refs only as
their concern is reached; continue without another user invocation. The legacy
`scripts/select_frontend_design.py` forwards to the real engine, not a fixed map.
