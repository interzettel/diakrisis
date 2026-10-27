"""DIA-008 synthetic structural composition controls, NOT LLM behavior evaluation."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools.coordinate_reviews import compose, validator, main

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evals/finding-contract/cases.json").read_text(encoding="utf-8"))
BASE = CASES["valid_findings"][0]
ABSTAIN = CASES["valid_findings"][1]


def finding(name, reviewer="terminology-review", disposition=None, **kwargs):
    f = deepcopy(BASE)
    f["id"] = name
    f["reviewer"] = reviewer
    if disposition is not None:
        f["disposition"] = disposition
    f.update(kwargs)
    return f


def report(identifier, findings, status=None):
    if status is None:
        status = "issues-identified" if findings else "no-issues-detected"
    return {
        "schema_version": 2,
        "review_id": identifier,
        "status": status,
        "coverage": {
            "examined": [{"source": "draft.md", "scope": "bounded terms", "revision": "a1"}],
            "not_examined": ["other chapters"],
        },
        "findings": findings,
        "limitations": ["Only supplied passages reviewed."],
    }


def bundle(*reviews, relations=None):
    return {"schema_version": 2, "coordination_id": "coord-001",
            "inputs": [{"input_id": "I-" + r["review_id"], "report": r}
                       for r in reviews], "relations": relations or []}


def relation(left, right, kind, reason="Same semantic state/flag distinction in the cited paragraph."):
    return {"left": left, "right": right, "kind": kind,
            "reason": reason, "authority_source": "standards/STANDARD.md @ v0.4.1"}


class CoordinatorTests(unittest.TestCase):
    def test_schemas_and_two_reviewer_group_preserve_originals(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="conceptual-model-review")
        inputs = bundle(report("R-a", [a]), report("R-b", [b]),
                        relations=[relation("F-a", "F-b", "shared-cause")])
        result = compose(inputs)
        validator("coordinated-report.schema.json").validate(result)
        self.assertEqual(len(result["report"]["findings"]), 2)
        self.assertEqual([g["finding_ids"] for g in result["groups"]], [["F-a", "F-b"]])
        self.assertEqual(result["report"]["findings"], [a, b])
        self.assertEqual(len(result["sources"]), 2)
        self.assertEqual(result["report"]["status"], "issues-identified")
        self.assertIn("other chapters", result["report"]["coverage"]["not_examined"])

    def test_does_not_group_by_key_without_declared_relation(self):
        result = compose(bundle(report("R-a", [finding("F-a")]),
                                report("R-b", [finding("F-b", reviewer="method-review")])))
        self.assertEqual(result["groups"], [])
        self.assertEqual(len(result["report"]["findings"]), 2)

    def test_declared_disagreement_keeps_both_claims(self):
        a = finding("F-a")
        b = deepcopy(ABSTAIN)
        b["id"] = "F-b"
        b["reviewer"] = "method-review"
        b["artifact"] = deepcopy(a["artifact"])
        result = compose(bundle(report("R-a", [a]),
                                report("R-b", [b], status="insufficient-evidence"),
                                relations=[relation("F-a", "F-b", "disagreement")]))
        self.assertEqual(len(result["disagreements"]), 1)
        self.assertEqual(len(result["report"]["findings"]), 2)
        self.assertFalse(result["groups"])
        self.assertEqual(result["report"]["findings"][1]["disposition"], "abstain")

    def test_cannot_group_different_artifact_or_issue_key(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="method-review")
        b["artifact"]["span"] = "different paragraph"
        with self.assertRaisesRegex(ValueError, "shared cause"):
            compose(bundle(report("R-a", [a]), report("R-b", [b]),
                           relations=[relation("F-a", "F-b", "shared-cause")]))
        b = finding("F-b", reviewer="method-review", issue_key="other")
        with self.assertRaisesRegex(ValueError, "shared cause"):
            compose(bundle(report("R-a", [a]), report("R-b", [b]),
                           relations=[relation("F-a", "F-b", "shared-cause")]))

    def test_transitive_inference_refused_without_all_pairs(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="conceptual-model-review")
        c = finding("F-c", reviewer="method-review")
        with self.assertRaisesRegex(ValueError, "clique"):
            compose(bundle(report("R-a", [a]), report("R-b", [b]), report("R-c", [c]),
                           relations=[relation("F-a", "F-b", "shared-cause"),
                                      relation("F-b", "F-c", "shared-cause")]))
        ok = compose(bundle(report("R-a", [a]), report("R-b", [b]), report("R-c", [c]),
                            relations=[relation("F-a", "F-b", "shared-cause"),
                                       relation("F-b", "F-c", "shared-cause"),
                                       relation("F-a", "F-c", "shared-cause")]))
        self.assertEqual(len(ok["groups"]), 1)
        self.assertEqual(len(ok["report"]["findings"]), 3)

    def test_duplicate_findings_or_uninspected_source_rejected(self):
        a = finding("F-a")
        with self.assertRaisesRegex(ValueError, "unique"):
            compose(bundle(report("R-a", [a]), report("R-b", [deepcopy(a)])))
        b = finding("F-b")
        b["basis"][0]["verification"] = "not-inspected"
        with self.assertRaisesRegex(ValueError, "input"):
            compose(bundle(report("R-a", [b])))

    def test_zero_findings_scoped_and_abstentions(self):
        empty = compose(bundle(report("R-a", []), report("R-b", [])))
        self.assertEqual(empty["report"]["status"], "no-issues-detected")
        self.assertEqual(empty["report"]["findings"], [])
        inconclusive = compose(bundle(report("R-a", [], status="insufficient-evidence")))
        self.assertEqual(inconclusive["report"]["status"], "insufficient-evidence")
        abstain = deepcopy(ABSTAIN)
        abstain["id"] = "F-unknown"
        no_authority = compose(bundle(report("R-c", [abstain], status="insufficient-evidence")))
        self.assertEqual(no_authority["report"]["status"], "insufficient-evidence")

    def test_reorders_inputs_deterministically(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="communication-review", issue_key="different")
        x = bundle(report("R-b", [b]), report("R-a", [a]))
        y = deepcopy(x)
        y["inputs"].reverse()
        self.assertEqual(compose(x), compose(y))

    def test_disagreement_must_refer_to_same_revision(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="method-review")
        b["artifact"]["revision"] = "later"
        with self.assertRaisesRegex(ValueError, "shared artifact"):
            compose(bundle(report("R-a", [a]), report("R-b", [b]),
                           relations=[relation("F-a", "F-b", "disagreement")]))

    def test_duplicate_relation_and_unknown_finding_refused(self):
        a = finding("F-a")
        b = finding("F-b", reviewer="method-review")
        source = bundle(report("R-a", [a]), report("R-b", [b]),
                        relations=[relation("F-a", "F-b", "shared-cause")] * 2)
        with self.assertRaisesRegex(ValueError, "repeated relation"):
            compose(source)
        source["relations"] = [relation("F-a", "missing", "shared-cause")]
        with self.assertRaisesRegex(ValueError, "unknown finding"):
            compose(source)

    def test_cli_never_overwrites_existing_result(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.json"
            result = root / "output.json"
            source.write_text(json.dumps(bundle(report("R-a", []))), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "tools/coordinate_reviews.py"),
                   "--input", str(source), "--output", str(result)]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = result.read_bytes()
            second = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(result.read_bytes(), original)

    def test_clean_source_that_examined_nothing_cannot_make_aggregate_clean(self):
        # Contract revision 2 rejects such a report at input validation; the
        # per-source status rule stays as a second line of defence.
        blind = report("R-blind", [])
        blind["coverage"]["examined"] = []
        with self.assertRaisesRegex(ValueError, "input"):
            compose(bundle(blind, report("R-seen", [])))

    def test_revision_1_input_is_refused_with_migration_hint(self):
        old = bundle(report("R-a", []))
        old["schema_version"] = 1
        with self.assertRaisesRegex(ValueError, "revision 1"):
            compose(old)

    def test_coordination_id_must_not_reuse_an_input_review_id(self):
        with self.assertRaisesRegex(ValueError, "coordination ID"):
            compose(bundle(report("coord-001", [])))

    def _run_cli(self, source, result):
        import subprocess
        import sys
        return subprocess.run([sys.executable, str(ROOT / "tools/coordinate_reviews.py"),
                               "--input", str(source), "--output", str(result)],
                              capture_output=True, text=True)

    def test_cli_refuses_symlinked_input(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            real = root / "source.json"
            real.write_text(json.dumps(bundle(report("R-a", []))), encoding="utf-8")
            alias = root / "alias.json"
            try:
                alias.symlink_to(real)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"cannot create symlink: {exc}")
            run = self._run_cli(alias, root / "out.json")
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse((root / "out.json").exists())

    def test_cli_refuses_output_that_is_a_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source.json"
            source.write_text(json.dumps(bundle(report("R-a", []))), encoding="utf-8")
            elsewhere = root / "elsewhere.json"
            output = root / "out.json"
            try:
                output.symlink_to(elsewhere)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"cannot create symlink: {exc}")
            run = self._run_cli(source, output)
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse(elsewhere.exists())


if __name__ == "__main__":
    unittest.main()
