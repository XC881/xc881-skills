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
    r"```[ \t]*(" + "|".join(re.escape(lang) for lang in _LANG_HINT) + r")\b",
    re.IGNORECASE,
)


# Real agent output wraps section labels in markdown: bold (**risk:**), list
# markers (- risk:), backticks, or a full-width colon (：). Normalize those away
# so header detection matches emitted headers, not just the plain fixture form.
def _norm_header(line):
    header = line.strip().lstrip("#->*` \t").rstrip("*` ")
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
def _section_body(text, section, sections):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if _is_header_of(line, section):
            inline = _norm_header(line)[len(section) :].lstrip(": ").strip()
            body = [inline] if inline else []
            for follow in lines[index + 1 :]:
                if _is_any_header(follow, sections):
                    break
                if follow.strip():
                    body.append(follow.strip())
            return True, "\n".join(body).strip()
    return False, ""


def _delete_section(text, section, sections):
    lines = text.splitlines()
    kept = []
    index = 0
    while index < len(lines):
        if _is_header_of(lines[index], section):
            index += 1
            while index < len(lines) and not _is_any_header(lines[index], sections):
                index += 1
        else:
            kept.append(lines[index])
            index += 1
    return "\n".join(kept)


def check_structural_output(text, required_sections, forbid_impl_code):
    violations = []
    for section in required_sections:
        present, body = _section_body(text, section, required_sections)
        if not present:
            violations.append(f"missing_section:{section}")
        elif not body:
            violations.append(f"empty_section:{section}")
    if forbid_impl_code and _IMPL_CODE_RE.search(text):
        violations.append("no_impl_code")
    return violations


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
        required = contract.get("required_sections")
        if not isinstance(required, list) or not required or not all(
            isinstance(s, str) and s.strip() for s in required
        ):
            die("xc881-skills", f"{name} required_sections must be non-empty strings")
        forbid = contract.get("forbid_impl_code", False)
        if not isinstance(forbid, bool):
            die("xc881-skills", f"{name} forbid_impl_code must be boolean")
        sample = contract.get("pass_sample")
        if not isinstance(sample, str) or not sample.strip():
            die("xc881-skills", f"{name} pass_sample must be non-empty")

        residual = check_structural_output(sample, required, forbid)
        if residual:
            die("xc881-skills", f"{name} pass_sample must satisfy contract, got {residual}")
        for section in required:
            mutated = _delete_section(sample, section, required)
            if f"missing_section:{section}" not in check_structural_output(
                mutated, required, forbid
            ):
                die("xc881-skills", f"{name} deletion of {section} not detected")
        if forbid:
            injected = sample + "\n```python\nx = 1\n```\n"
            if "no_impl_code" not in check_structural_output(injected, required, forbid):
                die("xc881-skills", f"{name} impl-code injection not detected")

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
