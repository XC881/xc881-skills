from pathlib import Path
import re


REQUIRED_FRONTMATTER = [
    "name",
    "description",
    "when_to_use",
    "display_name",
    "version",
    "category",
    "tags",
    "aliases",
]

SCALAR_FIELDS = [
    "name",
    "description",
    "when_to_use",
    "display_name",
    "version",
    "category",
]

LIST_FIELDS = ["tags", "aliases"]


def die(skill, message):
    raise SystemExit(f"{skill}: {message}")


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _frontmatter(text, skill):
    if not text.startswith("---\n"):
        die(skill, "SKILL.md must start with YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        die(skill, "SKILL.md missing closing frontmatter delimiter")
    return frontmatter.strip("\n")


def parse_frontmatter(text, skill):
    data = {}
    current_list = None
    for line_no, raw_line in enumerate(_frontmatter(text, skill).splitlines(), 1):
        if not raw_line.strip():
            continue
        if raw_line.startswith("  - "):
            if current_list is None:
                die(skill, f"line {line_no}: list item without list key")
            value = _unquote(raw_line[4:].strip())
            if not value:
                die(skill, f"line {line_no}: empty list item")
            data[current_list].append(value)
            continue
        if raw_line.startswith(" "):
            die(skill, f"line {line_no}: unsupported indentation")
        if ":" not in raw_line:
            die(skill, f"line {line_no}: expected key/value pair")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            die(skill, f"line {line_no}: empty key")
        if key in data:
            die(skill, f"line {line_no}: duplicate key {key}")
        if not value:
            data[key] = []
            current_list = key
        else:
            data[key] = _unquote(value)
            current_list = None
    return data


def validate_skill_frontmatter(skill_dir):
    skill_dir = Path(skill_dir)
    skill = skill_dir.name
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    data = parse_frontmatter(text, skill)
    for key in REQUIRED_FRONTMATTER:
        if key not in data:
            die(skill, f"missing frontmatter key {key}")
    for key in SCALAR_FIELDS:
        if not isinstance(data[key], str) or not data[key].strip():
            die(skill, f"{key} must be a non-empty scalar")
    for key in LIST_FIELDS:
        if not isinstance(data[key], list) or not data[key]:
            die(skill, f"{key} must be a non-empty list")
        if not all(isinstance(item, str) and item.strip() for item in data[key]):
            die(skill, f"{key} must contain only non-empty strings")
    if data["name"] != skill:
        die(skill, "frontmatter name must match folder")
    if not re.fullmatch(r"[a-z0-9-]+", data["name"]):
        die(skill, "frontmatter name must be lowercase kebab-case")
    return data


_LANG_HINT = (
    "py python js javascript ts typescript java go golang rust rs c cpp "
    "cs csharp rb ruby php bash sh shell sql kotlin swift scala"
).split()
_IMPL_CODE_RE = re.compile(
    r"^[ \t]*(?:`{3,}|~{3,})[ \t]*(" + "|".join(re.escape(lang) for lang in _LANG_HINT) + r")\b",
    re.IGNORECASE | re.MULTILINE,
)


# Real agent output wraps section labels in markdown: bold (**risk:**), list
# markers (- risk:), backticks, or a full-width colon (：). Normalize those away
# so header detection matches emitted headers, not just the plain fixture form.
def _norm_header(line):
    header = line.strip().lstrip("#-*` \t").rstrip("*` ")
    header = re.sub(r"(\*\*|__|`)", "", header)
    return header.replace("：", ":").strip()


def _is_header_of(line, section):
    header = _norm_header(line)
    if header == section:
        return True
    if header.startswith(section):
        return header[len(section) : len(section) + 1] == ":"
    return False


def _is_any_header(line, sections):
    return any(_is_header_of(line, section) for section in sections)


# Section boundaries are detected purely from required-section labels: a line is
# a header only if it equals a label or is that label followed by ":". Bodies run
# until the next such header. Fixture samples must not start body lines with a
# label, or those lines would be misread as headers.
def output_lines(text):
    """Keep fenced/quoted evidence as content, never as contract headings."""
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        is_fence = marker is not None
        if marker:
            run, suffix = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not suffix.strip():
                fence = None
        yield line, not is_fence and fence is None and not (
            line.lstrip().startswith(">") or line.startswith(("    ", "\t"))
        )


def _section_body(text, section, sections):
    lines = list(output_lines(text))
    for index, (line, heading_allowed) in enumerate(lines):
        if heading_allowed and _is_header_of(line, section):
            inline = _norm_header(line)[len(section) :].lstrip(": ").strip()
            body = [inline] if inline else []
            for follow, allowed in lines[index + 1 :]:
                if allowed and _is_any_header(follow, sections):
                    break
                if follow.strip():
                    body.append(follow.strip())
            return True, "\n".join(body).strip()
    return False, ""


def _delete_section(text, section, sections):
    lines = list(output_lines(text))
    kept = []
    index = 0
    while index < len(lines):
        if lines[index][1] and _is_header_of(lines[index][0], section):
            index += 1
            while index < len(lines) and not (
                lines[index][1] and _is_any_header(lines[index][0], sections)
            ):
                index += 1
        else:
            kept.append(lines[index][0])
            index += 1
    return "\n".join(kept)


def check_structural_output(text, required_sections, forbid_impl_code, optional_sections=()):
    violations = []
    sections = [*required_sections, *optional_sections]
    for section in sections:
        present, body = _section_body(text, section, sections)
        if not present and section in required_sections:
            violations.append(f"missing_section:{section}")
        elif present and not body:
            violations.append(f"empty_section:{section}")
        if sum(allowed and _is_header_of(line, section) for line, allowed in output_lines(text)) > 1:
            violations.append(f"duplicate_section:{section}")
    if forbid_impl_code and _IMPL_CODE_RE.search(text):
        violations.append("no_impl_code")
    return violations


def output_contract_mode(contract, mode="full"):
    if mode == "full":
        return contract
    if mode == "prose":
        return None
    if mode not in contract.get("modes", {}):
        raise ValueError(f"unknown output mode: {contract['skill']}/{mode}")
    return {**contract, **contract["modes"][mode]}


def evaluate_output(text, contract, mode="full"):
    selected = output_contract_mode(contract, mode)
    if selected is None:
        return {"status": "unscored", "reason": "no_fixed_structure", "violations": []}
    violations = check_structural_output(
        text, selected["required_sections"], selected.get("forbid_impl_code", False),
        selected.get("optional_sections", []),
    )
    return {"status": "fail" if violations else "pass", "violations": violations}


def validate_output_contract(contract):
    def labels(value, field, nonempty=False):
        if not isinstance(value, list) or (nonempty and not value) or not all(
            isinstance(s, str) and s.strip() == s and s for s in value
        ) or len(set(value)) != len(value):
            raise ValueError(f"{field} must be unique non-empty strings")

    if contract.get("layer") != "structural":
        raise ValueError("behavior-contract layer must be structural")
    labels(contract.get("anchors"), "anchors", True)
    modes = contract.get("modes", {})
    if not isinstance(modes, dict) or any(
        not isinstance(mode, str) or not mode.strip() or mode in {"full", "prose"}
        or not isinstance(body, dict) for mode, body in modes.items()
    ):
        raise ValueError("invalid output modes")
    for mode in ["full", *modes]:
        selected = output_contract_mode(contract, mode)
        required, optional = selected.get("required_sections"), selected.get("optional_sections", [])
        labels(required, "required_sections", True)
        labels(optional, "optional_sections")
        if set(required) & set(optional):
            raise ValueError("required/optional sections overlap")
        forbid = selected.get("forbid_impl_code", False)
        if not isinstance(forbid, bool):
            raise ValueError("forbid_impl_code must be boolean")
        sample = selected.get("pass_sample")
        if not isinstance(sample, str) or not sample.strip():
            raise ValueError("pass_sample must be non-empty")
        residual = evaluate_output(sample, contract, mode)["violations"]
        if residual:
            raise ValueError(f"{mode} pass_sample violates its contract: {residual}")
        sections = [*required, *optional]
        for section in required:
            mutated = _delete_section(sample, section, sections)
            if f"missing_section:{section}" not in evaluate_output(mutated, contract, mode)["violations"]:
                raise ValueError(f"deletion of {section} not detected")
        if forbid and "no_impl_code" not in evaluate_output(sample + "\n```python\nx = 1\n```\n", contract, mode)["violations"]:
            raise ValueError("impl-code injection not detected")


def validate_behavior_contracts(root, skills):
    import json

    for skill in skills:
        name = skill["name"]
        evals_dir = Path(root) / "skills" / name / "evals"
        contract_path = evals_dir / "behavior-contract.json"
        if not contract_path.exists():
            die("xc881-skills", f"{name} missing evals/behavior-contract.json")
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        if contract.get("skill") != name:
            die("xc881-skills", f"{name} behavior-contract skill mismatch")
        try:
            validate_output_contract(contract)
        except ValueError as exc:
            die("xc881-skills", f"{name}: {exc}")

        rubric_path = evals_dir / "behavior-rubric.json"
        if not rubric_path.exists():
            continue
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        if rubric.get("skill") != name:
            die("xc881-skills", f"{name} behavior-rubric skill mismatch")
        if rubric.get("layer") != "semantic":
            die("xc881-skills", f"{name} behavior-rubric layer must be 'semantic'")
        if rubric.get("ci") is not False:
            die("xc881-skills", f"{name} behavior-rubric ci must be false")
        cases = rubric.get("cases")
        if not isinstance(cases, list) or not cases:
            die("xc881-skills", f"{name} behavior-rubric cases must be non-empty")
        for case in cases:
            query = case.get("query")
            if not isinstance(query, str) or not query.strip():
                die("xc881-skills", f"{name} rubric case query must be non-empty")
            checklist = case.get("checklist")
            if not isinstance(checklist, list) or not checklist or not all(
                isinstance(item, str) and item.strip() for item in checklist
            ):
                die("xc881-skills", f"{name} rubric checklist must be non-empty strings")


def validate_routing_matrix(root, skills):
    matrix_path = Path(root) / "evals" / "cross-skill-routing.json"
    if not matrix_path.exists():
        die("xc881-skills", "missing evals/cross-skill-routing.json")
    import json

    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    skill_names = {skill["name"] for skill in skills}
    if not isinstance(matrix, list) or not matrix:
        die("xc881-skills", "routing matrix must be a non-empty list")

    evals_by_skill = {}
    for skill_name in skill_names:
        eval_path = Path(root) / "skills" / skill_name / "evals" / "trigger-queries.json"
        evals_by_skill[skill_name] = {
            item["query"]: item["should_trigger"]
            for item in json.loads(eval_path.read_text(encoding="utf-8"))
        }

    for idx, case in enumerate(matrix, 1):
        query = case.get("query")
        expected = set(case.get("expected_skills", []))
        if not isinstance(query, str) or not query.strip():
            die("xc881-skills", f"routing case {idx}: query must be non-empty")
        if not expected <= skill_names:
            unknown = ", ".join(sorted(expected - skill_names))
            die("xc881-skills", f"routing case {idx}: unknown skill {unknown}")
        for skill_name in skill_names:
            actual = evals_by_skill[skill_name].get(query)
            if actual is None:
                die("xc881-skills", f"{skill_name} missing routing eval: {query}")
            wanted = skill_name in expected
            if actual is not wanted:
                die("xc881-skills", f"{skill_name} bad routing eval for {query}")
