"""DIA-005: offline JSON Schema 2020-12 structural controls, not model evaluation."""
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
FINDING = json.loads((ROOT / "schemas/finding.schema.json").read_text(encoding="utf-8"))
REPORT = json.loads((ROOT / "schemas/review-report.schema.json").read_text(encoding="utf-8"))
CASES = json.loads((ROOT / "evals/finding-contract/cases.json").read_text(encoding="utf-8"))

# Register local source in memory: JSON Schema must never fetch our public repo
# or the internet at validation time.
REGISTRY = Registry().with_resource(FINDING["$id"], Resource.from_contents(FINDING))
FINDING_CHECK = Draft202012Validator(FINDING, registry=REGISTRY)
REPORT_CHECK = Draft202012Validator(REPORT, registry=REGISTRY)


class FindingContractTests(unittest.TestCase):
    def test_schemas_are_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(FINDING)
        Draft202012Validator.check_schema(REPORT)
        self.assertEqual(CASES["contract_revision"], 1)
        self.assertIn("finding.schema.json", REPORT["properties"]["findings"]["items"]["$ref"])

    def test_accepted_findings(self):
        self.assertGreaterEqual(len(CASES["valid_findings"]), 3)
        for record in CASES["valid_findings"]:
            with self.subTest(id=record["id"]):
                FINDING_CHECK.validate(record)

    def test_rejected_findings(self):
        self.assertGreaterEqual(len(CASES["invalid_findings"]), 10)
        for case in CASES["invalid_findings"]:
            with self.subTest(reason=case["reason"]):
                self.assertTrue(list(FINDING_CHECK.iter_errors(case["record"])),
                                "An invalid finding was accepted: " + case["reason"])

    def test_accepted_reports_and_no_findings_control(self):
        for record in CASES["valid_reports"]:
            with self.subTest(id=record["review_id"]):
                REPORT_CHECK.validate(record)
        no_findings = [r for r in CASES["valid_reports"]
                       if r["status"] == "no-issues-detected"]
        self.assertTrue(no_findings)
        self.assertTrue(all(not r["findings"] for r in no_findings))
        self.assertTrue(all(r["coverage"]["examined"] for r in no_findings))

    def test_rejected_reports(self):
        for case in CASES["invalid_reports"]:
            with self.subTest(reason=case["reason"]):
                self.assertTrue(list(REPORT_CHECK.iter_errors(case["record"])),
                                "An invalid report was accepted: " + case["reason"])

    def test_contract_bounds_no_fabricated_efficacy(self):
        self.assertNotIn("accuracy", FINDING["properties"])
        self.assertNotIn("autonomous_approval", REPORT["properties"])
        self.assertNotIn("review-coordinator",
                         FINDING["properties"]["reviewer"]["enum"])


if __name__ == "__main__":
    unittest.main()
