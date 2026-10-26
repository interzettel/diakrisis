"""Contract tests for candidate terminology-review Agent Skill (structural RED/GREEN only)."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "terminology-review" / "SKILL.md"
EVALS = ROOT / "evals" / "pilot-cases.json"

class TerminologySkillContract(unittest.TestCase):
    def test_skill_exists(self):
        self.assertTrue(SKILL.is_file(), "RED: terminology-review SKILL.md is absent")

    def test_portable_metadata(self):
        body = SKILL.read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\n"))
        front = body.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^name: terminology-review$")
        self.assertRegex(front, r"(?m)^description: .{30,1024}$")
        self.assertLess(len(body.splitlines()), 500, "Move large references outside SKILL.md")

    def test_scope_and_safety(self):
        body = SKILL.read_text(encoding="utf-8").lower()
        for required in ["concept", "designation", "authority", "abstain", "source", "do not edit"]:
            self.assertIn(required, body)

    def test_positive_and_negative_fixtures(self):
        cases = json.loads(EVALS.read_text(encoding="utf-8"))["cases"]
        selected = [x for x in cases if x["reviewer"] == "terminology-review"]
        self.assertTrue(any(x["class"] == "positive" for x in selected))
        self.assertTrue(any(x["class"] == "negative-control" for x in selected))
        for case in selected:
            self.assertTrue(case.get("expected_interpretation"))

if __name__ == "__main__":
    unittest.main()
