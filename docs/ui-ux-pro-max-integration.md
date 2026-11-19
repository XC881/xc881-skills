# UI/UX Pro Max Integration

The complete open-source dataset and actual search/design generator are vendored
inside Coding. They are executable resources, not prompt text or a separate skill.
The former small hardcoded selector is replaced by a compatibility forwarder.

## Source And Inventory

- Official repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Pinned revision: `4aad0584d92131626b16d4ff4d77f0455385013c` (2026-09-06).
- Location: `skills/xc881-coding-skills/vendor/ui-ux-pro-max/`.
- MIT license is retained verbatim in `LICENSE`; `upstream.json` records every
  imported file's SHA-256 and revision. Vendor code/data is not edited locally.
- `.gitattributes` preserves vendor bytes across Git line-ending settings.
- The full `src/ui-ux-pro-max/data/` snapshot includes 192 products, palettes and
  reasoning profiles; 79 searchable styles (88 including deprecated rows), 74
  font pairings, 1,934 Google Font records, 105 curated icons, 1,512 upstream icon
  records, 119 UX guidelines, 25 chart types, 17 motion presets and 22 stacks.
- Full runtime modules: `core.py`, `search.py`, `design_system.py`,
  `reasoning_contract.py`; `validate_data.py` is retained for maintenance.
- Font licenses, catalog summary and data provenance are retained. Font metadata
  and icon records are not bundled font/image binaries or permission to copy brands.
- Upstream's premium/proprietary features are not part of its public repository.

## CLI Integration

Use `<coding-skill>/scripts/frontend_design.py`. Requires Python 3.9+, standard
library only. Resolve the installed skill path instead of guessing from project
cwd. No network, dependency installation or filesystem write occurs by default.

```bash
python skills/xc881-coding-skills/scripts/frontend_design.py "time series trend" --domain chart
python skills/xc881-coding-skills/scripts/frontend_design.py "form accessibility react 18" --stack react
python skills/xc881-coding-skills/scripts/frontend_design.py --record 'stacks/react.csv#46' --fields 'Code Good' "Don't"
python skills/xc881-coding-skills/scripts/frontend_design.py "healthcare scheduling dashboard" --design-system --surface app
python skills/xc881-coding-skills/scripts/frontend_design.py "healthcare scheduling dashboard" --design-system --section colors
```

Record numbers are 1-based parsed CSV records, not physical lines; always use the
ID from the actual result. All upstream domains/stacks remain supported. The CLI
returns one result by default, up to three for comparison. Default search/system
JSON is <=4,200 characters. Exact record/field or system-section requests return
complete content; never cut code in the middle to meet an output limit.
Omitted fields are named and `needs-detail` marks budget-driven omission.
Results name the upstream revision. `no-match` stays empty; generated fallbacks
name missing source identities. The agent translates terms internally and avoids
synonym retry loops. A demonstrated wrong domain/language/version permits one
correction; an actual external gap may delegate bounded Solution research.

Generator queries use short positive product/workflow terms, not the whole brief.
Keep negations and implementation/framework instructions in reconciliation;
perform a versioned stack lookup only for an actual API/pattern decision. Once a
baseline fits, use targeted domain queries for remaining font/color/rule gaps.

The upstream npm `uipro` CLI installs/updates a separate skill. It is not the
search/generation engine. xc881 retains the original Python search CLI and wraps
its engine with xc881's bounded command interface; `scripts/install.sh` distributes
the complete embedded resources. No global npm install or competing skill is needed.
The raw upstream CLI is kept for provenance/explicit maintenance, not routine agent
execution, because its persistence/output defaults do not implement xc881 ownership.

## Default System And Authority

Substantial new/reworked UI without a reusable system automatically generates a
project-specific candidate. This is not a universal palette, a mandatory new
document on every UI change, or permission to replace existing branding.

App/mobile surfaces suppress upstream landing-page sections; only an actual
landing surface receives those patterns. Reconcile task fit, localization/font
coverage, accessibility, contrast, dependencies and version applicability before
using a result. Upstream rankings can be unsuitable: even a high-ranking style
may carry high accessibility risk. Industry constraints are proposals, not proof
of an obligation or compliance. Existing project/user evidence wins.

Default generator output is ephemeral. Requirement owns accepted reusable
contracts under `dev-notes/design-system/<slug>/MASTER.md` (<=3,000 chars) with
optional `surfaces/<surface>.md` overrides (<=1,200). Coding consumes exact paths.
Normal authoring derives the accepted contract once, not a generation/validation
rewrite cycle. Evidence-complete single-surface work needs no persisted master.

For an explicit draft export, the CLI supports:

```bash
python <coding-skill>/scripts/frontend_design.py "product audience task" --design-system --persist --project-root <project> --slug <name>
```

It creates a bounded `Status: proposal` only, refuses existing files, unsafe slugs
and symlinked note paths. Requirement must reconcile a proposal before execution.
Oversized candidates fail before writing. No project-root `design-system/` is used.

## Updates And Verification

Import only an explicitly reviewed local upstream Git revision:

```bash
python scripts/sync_frontend_vendor.py <upstream-checkout> --revision <full-commit>
python scripts/validate_frontend_vendor.py
python -B skills/xc881-coding-skills/vendor/ui-ux-pro-max/scripts/validate_data.py
python scripts/test_frontend_design.py
python scripts/validate_all.py
```

The import reads Git objects, not uncommitted checkout content, and refuses locally
modified vendor files or removals requiring review. It does not fetch/upgrade at
skill activation. Hash checks protect the snapshot; they do not certify advice.
Upstream code is excluded from xc881 prompt-language lint, not from integrity or
behavior testing. Refer to the upstream search/generator tests when changing pins.

## Reading-Cost Model

Metadata selects one owner; SKILL routes the concern; a selected reference invokes
the engine; only a bounded result enters the model's context. The full multi-MB
dataset stays on disk. Runtime code, data, maintenance docs and all other refs are
not preloaded. This restores ability without making every activation a data dump.

Agent Skills primary guidance:

- https://agentskills.io/skill-creation/best-practices.md
- https://agentskills.io/skill-creation/using-scripts.md
- https://agentskills.io/skill-creation/evaluating-skills.md

These support conditional references, executable resources and behavior-based
iteration; they do not establish a measured token-saving percentage for xc881.
