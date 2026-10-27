"""DIA-005 quote checker: deterministic structural checks on quoted spans. No model."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/check_spans.py"
SPEC = importlib.util.spec_from_file_location("diakrisis_check_spans", TOOL)
spans = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(spans)

HEAD = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                      text=True, check=True).stdout.strip()
REAL = "Distinguish before you judge."  # README.md tagline, present at HEAD


def finding(span, path="README.md", revision=HEAD, basis=()):
    return {"schema_version": 2, "id": "F-1", "reviewer": "communication-review",
            "artifact": {"path": path, "revision": revision, "span": span},
            "category": "referential-ambiguity", "claim": "c", "basis": list(basis),
            "evidence_status": "observed", "disposition": "suggestion",
            "severity": "minor", "confidence_reason": "r", "requires_owner_decision": False}


def statuses(record):
    return [r["status"] for r in spans.check(record, ROOT)]


class QuoteCheckerTests(unittest.TestCase):
    def test_real_span_at_stated_revision_is_found(self):
        self.assertEqual(statuses(finding(REAL)), ["found"])

    def test_whitespace_altered_span_is_flagged_as_normalised_match(self):
        self.assertEqual(statuses(finding("Distinguish  before\nyou judge.")), ["found-normalized"])

    def test_invented_span_is_missing(self):
        self.assertEqual(statuses(finding("Distinguish after you judge.")), ["missing"])

    def test_missing_file_is_a_failure(self):
        self.assertEqual(statuses(finding(REAL, path="docs/NO-SUCH-FILE.md")), ["file-not-found"])

    def test_unavailable_revision_is_not_checkable(self):
        self.assertEqual(statuses(finding(REAL, revision="0" * 40)), ["not-checkable"])

    def test_remote_location_and_escaping_paths_are_not_checkable(self):
        self.assertEqual(statuses(finding(REAL, path="https://example.org/doc")), ["not-checkable"])
        self.assertEqual(statuses(finding("line 42")), ["not-checkable"])
        self.assertEqual(statuses(finding(REAL, path="../outside.md")), ["not-checkable"])
        self.assertEqual(statuses(finding(REAL, path="/etc/hostname")), ["not-checkable"])

    def test_working_tree_used_when_no_revision(self):
        self.assertEqual(statuses(finding(REAL, revision=None)), ["found"])

    def test_basis_spans_are_checked_too(self):
        basis = [{"source": "README.md", "revision": HEAD, "span": "no such sentence here",
                  "reason": "r", "verification": "inspected", "applicability": "applicable"},
                 {"source": "https://example.org", "reason": "r",
                  "verification": "not-inspected", "applicability": "uncertain"}]
        self.assertEqual(statuses(finding(REAL, basis=basis)), ["found", "missing"])

    def test_reports_coordinated_reports_and_coordinator_inputs_are_read(self):
        report = {"schema_version": 2, "review_id": "R", "status": "issues-identified",
                  "coverage": {"examined": [{"source": "README.md", "scope": "all"}], "not_examined": []},
                  "findings": [finding(REAL)], "limitations": []}
        self.assertEqual(statuses(report), ["found"])
        self.assertEqual(statuses({"report": report, "sources": []}), ["found"])
        self.assertEqual(statuses({"inputs": [{"input_id": "i", "report": report}]}), ["found"])

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            bad = Path(tmp) / "bad.json"
            good.write_text(json.dumps(finding(REAL)), encoding="utf-8")
            bad.write_text(json.dumps(finding("Distinguish after you judge.")), encoding="utf-8")
            run = lambda p, *extra: subprocess.run(
                [sys.executable, str(TOOL), "--input", str(p), "--root", str(ROOT), *extra],
                capture_output=True, text=True)
            self.assertEqual(run(good).returncode, 0)
            self.assertEqual(run(bad).returncode, 1)
            loose = Path(tmp) / "loose.json"
            loose.write_text(json.dumps(finding("Distinguish  before you judge.")), encoding="utf-8")
            self.assertEqual(run(loose).returncode, 0)
            self.assertEqual(run(loose, "--strict").returncode, 1)


if __name__ == "__main__":
    unittest.main()
