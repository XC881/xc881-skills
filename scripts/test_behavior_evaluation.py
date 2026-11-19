#!/usr/bin/env python3
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import collect_behavior_data as collector
from skill_validation import check_structural_output, evaluate_output, validate_output_contract

CODING = "xc881-coding-skills"
ANALYSIS = "xc881-analysis"


class StructuralOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = collector.load_contracts()

    def test_current_owners_are_recognized(self):
        self.assertEqual(len(self.contracts), 4)
        for owner, contract in self.contracts.items():
            with self.subTest(owner=owner):
                self.assertEqual(collector.classify(contract["pass_sample"], self.contracts), (owner, None))
                self.assertEqual(evaluate_output(contract["pass_sample"], contract)["status"], "pass")

    def test_coding_omits_irrelevant_fields(self):
        for text in ("完成内容: 已检查所选调用链。", "完成内容: 已修正标签。\n验证: 已执行指定检查。"):
            self.assertEqual(evaluate_output(text, self.contracts[CODING])["status"], "pass")

    def test_required_omission_is_not_optional(self):
        self.assertEqual(evaluate_output("验证: 已执行检查。", self.contracts[CODING])["violations"], ["missing_section:完成内容"])

    def test_optional_body_does_not_fill_empty_required_section(self):
        self.assertEqual(check_structural_output("完成内容:\n验证: 已执行。", ["完成内容"], False, ["验证"]), ["empty_section:完成内容"])

    def test_present_optional_section_must_not_be_empty(self):
        self.assertEqual(check_structural_output("完成内容: 已完成。\n验证:", ["完成内容"], False, ["验证"]), ["empty_section:验证"])

    def test_optional_sections_are_separate_from_each_other(self):
        self.assertEqual(check_structural_output("完成内容: 已完成。\n验证:\n需要注意: 待确认环境。", ["完成内容"], False, ["验证", "需要注意"]), ["empty_section:验证"])

    def test_duplicate_header_is_reported(self):
        self.assertIn("duplicate_section:完成内容", check_structural_output("完成内容: A\n完成内容: B", ["完成内容"], False))

    def test_markdown_and_chinese_colon(self):
        for heading in ("**完成内容：**", "- **完成内容:**", "## 完成内容", "`完成内容:`", "完成内容（最小改动）:"):
            with self.subTest(heading=heading):
                self.assertEqual(check_structural_output(heading + "\n已完成。", ["完成内容"], False), [])

    def test_quoted_and_code_headers_do_not_satisfy_contract(self):
        for text in ("> 完成内容: 示例", "    完成内容: 示例", "\t完成内容: 示例", "```text\n完成内容: 示例\n```", "~~~text\n完成内容: 示例\n~~~"):
            with self.subTest(text=text):
                self.assertEqual(check_structural_output(text, ["完成内容"], False), ["missing_section:完成内容"])
                self.assertIsNone(collector.classify(text, self.contracts)[0])

    def test_code_and_quote_can_be_real_evidence(self):
        text = "依据:\n```text\n结论: a literal from the log\n```\n结论: still unconfirmed"
        self.assertEqual(check_structural_output(text, ["依据", "结论"], False), [])
        self.assertEqual(check_structural_output("依据:\n> observed failure", ["依据"], False), [])

    def test_short_inner_fence_does_not_close_outer_fence(self):
        text = "````text\n```\n完成内容: 示例\n````"
        self.assertEqual(check_structural_output(text, ["完成内容"], False), ["missing_section:完成内容"])

    def test_forbidden_code_fence_variants(self):
        for fence in ("```python", "~~~SQL", "````js"):
            self.assertIn("no_impl_code", check_structural_output("Evidence: source\n" + fence + "\nx = 1", ["Evidence"], True))
        self.assertEqual(check_structural_output("Evidence: the text mentions ```python inline", ["Evidence"], True), [])

    def test_truncated_recognized_output_counts_as_failure(self):
        owner, reason = collector.classify("需求结论:", self.contracts)
        self.assertEqual(owner, ANALYSIS)
        self.assertIsNone(reason)
        self.assertEqual(evaluate_output("需求结论:", self.contracts[owner])["status"], "fail")

    def test_mode_is_supplied_by_task_not_chosen_for_fewest_errors(self):
        text = "需求结论: 筛选列表\n这次会做: 名称过滤\n完成标准: 只保留匹配项\n下一步: 实现"
        self.assertEqual(evaluate_output(text, self.contracts[ANALYSIS], "chat-only")["status"], "pass")
        self.assertEqual(evaluate_output(text, self.contracts[ANALYSIS], "full")["violations"], ["missing_section:开发记录"])
        self.assertEqual(collector.classify(text, self.contracts)[0], ANALYSIS)

    def test_anchor_modes_select_branch_contract(self):
        bugfix = "xc881 诊断: 登录 500\n结论: unconfirmed，疑似冷启动缺少初始化\n背景: 部署后首次请求 500\n依据: 堆栈显示 null token\n修复: bootstrap 初始化\n验证: 冷启动返回 200\n需要注意: 风险低\n下一步: 交给 Coding 修复"
        contract = self.contracts[ANALYSIS]
        self.assertEqual(collector.resolve_mode(bugfix, contract), "bugfix")
        self.assertEqual(evaluate_output(bugfix, contract, collector.resolve_mode(bugfix, contract))["status"], "pass")
        self.assertEqual(evaluate_output(bugfix, contract, "full")["status"], "fail")
        coding_read = "代码结论: 并发刷新缺少单飞保护\n依据: auth/session.ts 未合并并发请求\n需要注意: 仅静态确认"
        self.assertEqual(collector.classify(coding_read, self.contracts), (CODING, None))
        self.assertEqual(collector.resolve_mode(coding_read, self.contracts[CODING]), "read")
        self.assertEqual(evaluate_output(coding_read, self.contracts[CODING], "read")["status"], "pass")

    def test_decision_mode_requires_both_options_and_pick(self):
        contract = self.contracts[ANALYSIS]
        fact = contract["modes"]["solution"]["pass_sample"]
        self.assertEqual(evaluate_output(fact, contract, "solution")["status"], "pass")
        self.assertEqual(evaluate_output(fact, contract, "decision")["violations"], ["missing_section:对比", "missing_section:推荐"])

    def test_free_prose_is_not_structurally_clean(self):
        for contract in self.contracts.values():
            self.assertEqual(evaluate_output("这段只回答当前问题。", contract, "prose")["status"], "unscored")

    def test_unknown_modes_are_errors(self):
        with self.assertRaises(ValueError):
            evaluate_output("text", self.contracts[CODING], "ful")

    def test_meta_preamble_and_ambiguous_anchor_are_unscored(self):
        self.assertIsNone(collector.classify("格式示例：\n完成内容: 已完成", self.contracts)[0])
        conflicting = copy.deepcopy(self.contracts)
        conflicting[ANALYSIS]["anchors"].append("完成内容")
        self.assertEqual(collector.classify("完成内容: 已完成", conflicting), (None, "ambiguous_contract"))

    def test_article_title_before_contract(self):
        owner = "xc881-source-article-style"
        text = "# 请求处理流程\n\n" + self.contracts[owner]["pass_sample"]
        self.assertEqual(collector.classify(text, self.contracts)[0], owner)

    def test_h1_contract_heading_is_not_discarded_as_title(self):
        self.assertEqual(collector.classify("# 完成内容\n已经完成。", self.contracts)[0], CODING)

    def test_invalid_contracts_are_rejected(self):
        mutations = (
            {"anchors": []}, {"required_sections": []}, {"optional_sections": ["完成内容"]},
            {"required_sections": ["完成内容", "完成内容"]}, {"forbid_impl_code": "false"},
            {"pass_sample": "完成内容:"}, {"modes": {"prose": {}}}, {"layer": "semantic"},
            {"modes": {"bad": {"required_sections": ["Missing"]}}},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_output_contract({**self.contracts[CODING], **mutation})


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.contracts = collector.load_contracts()

    def write_jsonl(self, texts, filename="outputs.jsonl"):
        path = self.root / filename
        path.write_text("".join(json.dumps({"text": text}) + "\n" for text in texts), encoding="utf-8")
        return path

    def test_explicit_files_only_and_no_raw_content_persisted(self):
        path = self.write_jsonl(["完成内容: selected-private-marker"])
        self.write_jsonl(["完成内容: unrelated"], "extra.jsonl")
        samples, excluded = collector.collect([path], self.contracts)
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]["status"], "pass")
        self.assertNotIn("selected-private-marker", json.dumps(samples))
        self.assertEqual(excluded, {})

    def test_scored_unscored_and_excluded_denominators(self):
        path = self.write_jsonl(["完成内容: done", "完成内容:", "简短回答"])
        samples, excluded = collector.collect([path], self.contracts)
        report = collector.summarize(samples, excluded)
        self.assertEqual(report["eligible_messages"], 3)
        self.assertEqual(report["by_skill"][CODING]["structural_pass_rate"], 0.5)
        self.assertIsNone(report["by_skill"]["unattributed"]["structural_pass_rate"])
        self.assertEqual(excluded, {})

    def test_explicit_prose_attribution_stays_unscored(self):
        path = self.write_jsonl(["当前判断还缺少复现证据。"])
        samples, _ = collector.collect([path], self.contracts, CODING, "prose")
        self.assertEqual(samples[0]["skill"], CODING)
        self.assertEqual(samples[0]["status"], "unscored")

    def test_malformed_json_marks_incomplete_collection(self):
        path = self.write_jsonl([])
        path.write_text("{broken\n", encoding="utf-8")
        samples, excluded = collector.collect([path], self.contracts)
        self.assertEqual(excluded, {"malformed_json": 1})
        self.assertFalse(collector.summarize(samples, excluded)["collection_complete"])

    def test_non_text_records_are_malformed(self):
        path = self.root / "outputs.jsonl"
        path.write_text(
            "\n".join(
                json.dumps(record)
                for record in ({"payload": "完成内容: done"}, {"text": ""}, {"text": 1})
            )
            + "\n",
            encoding="utf-8",
        )
        samples, excluded = collector.collect([path], self.contracts)
        self.assertEqual(samples, [])
        self.assertEqual(excluded, {"malformed_record": 3})
        self.assertFalse(collector.summarize(samples, excluded)["collection_complete"])

    def test_cli_deduplicates_inputs_and_writes_bounded_report(self):
        path = self.write_jsonl(["完成内容: done"])
        out = self.root / "out"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(collector.main([str(path), str(path), "--out-dir", str(out)]), 0)
        report = json.loads((out / "behavior-report.json").read_text())
        self.assertEqual(report["input_files"], 1)
        self.assertEqual(report["eligible_messages"], 1)

    def test_cli_rejects_unsafe_arguments(self):
        path = self.write_jsonl([], "behavior-samples.jsonl")
        cases = ([], [str(self.root)], [str(path), "--mode", "prose"],
                 [str(path), "--skill", "missing"], [str(path), "--skill", CODING, "--mode", "typo"],
                 [str(path), "--out-dir", str(self.root)])
        for argv in cases:
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                collector.main(argv)


if __name__ == "__main__":
    unittest.main()
