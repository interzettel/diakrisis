"""DIA-002 README tracker generator: evidence links and stale-date guard. Offline."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("diakrisis_sync_readme", ROOT / "tools/sync_readme.py")
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


def work(evidence, criterion="Criterion text"):
    return {"evidence": evidence, "criterion": criterion}


class EvidenceLinkTests(unittest.TestCase):
    def test_first_pull_request_wins_whatever_its_label(self):
        cell = sync.evidence_cell(work([
            {"kind": "coordinator-implementation-pr",
             "source": "https://github.com/interzettel/diakrisis/pull/27"},
            {"kind": "merged-pr", "source": "https://github.com/interzettel/diakrisis/pull/17"},
        ]))
        self.assertEqual(cell, "[PR #27](https://github.com/interzettel/diakrisis/pull/27)")

    def test_pull_request_after_non_pr_evidence_is_found(self):
        cell = sync.evidence_cell(work([
            {"kind": "published-release-metadata",
             "source": "https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1"},
            {"kind": "schema-implementation", "source": "https://github.com/interzettel/diakrisis/pull/24"},
        ]))
        self.assertEqual(cell, "[PR #24](https://github.com/interzettel/diakrisis/pull/24)")

    def test_pull_request_in_another_repository_names_it(self):
        cell = sync.evidence_cell(work([
            {"kind": "consumer-merged-implementation",
             "source": "https://github.com/yigit-denktas/writing-kitchen/pull/24"},
        ]))
        self.assertEqual(cell, "[writing-kitchen PR #24](https://github.com/yigit-denktas/writing-kitchen/pull/24)")

    def test_no_pull_request_falls_back_to_criterion(self):
        cell = sync.evidence_cell(work([
            {"kind": "ci-verification", "source": "https://github.com/interzettel/diakrisis/actions/runs/1"},
        ], criterion="Verified | escaped"))
        self.assertEqual(cell, r"Verified \| escaped")


class StaleDateGuardTests(unittest.TestCase):
    def ledger(self, note="", warning="", next_action=""):
        return {"items": [{"note": note}], "warnings": [warning],
                "milestones": [{"nextAction": next_action}]}

    def test_newer_date_in_ledger_than_manifest_is_reported(self):
        ledger = self.ledger(warning="2026-10-27: runner incident recorded")
        self.assertEqual(sync.stale_update_date(ledger, "2026-10-26"), "2026-10-27")

    def test_dates_in_notes_and_next_actions_are_scanned(self):
        self.assertEqual(sync.stale_update_date(self.ledger(note="checked 2026-11-02"), "2026-10-27"),
                         "2026-11-02")
        self.assertEqual(sync.stale_update_date(self.ledger(next_action="retry after 2026-11-01"),
                                                "2026-10-27"), "2026-11-01")

    def test_current_manifest_date_passes(self):
        ledger = self.ledger(note="investigated 2026-10-27", warning="2026-10-26: older")
        self.assertIsNone(sync.stale_update_date(ledger, "2026-10-27"))

    def test_repository_records_are_currently_consistent(self):
        import json
        ledger = json.loads((ROOT / "progress/ledger.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "progress/project-record.json").read_text(encoding="utf-8"))
        updated = manifest["projects"][0]["source"]["updatedOn"]
        self.assertIsNone(sync.stale_update_date(ledger, updated))


if __name__ == "__main__":
    unittest.main()
