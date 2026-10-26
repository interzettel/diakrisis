"""Structural and safety tests, not a language-model efficacy score."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "terminology-review" / "SKILL.md"
CASES = ROOT / "evals" / "terminology-review" / "cases.json"
RUNNER = ROOT / "tools" / "terminology_eval.py"

spec = importlib.util.spec_from_file_location("terminology_eval", RUNNER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TerminologySkillContract(unittest.TestCase):
    def test_skill_exists(self):
        self.assertTrue(SKILL.is_file(), "missing experimental terminology reviewer")

    def test_frontmatter_is_spec_portable_and_unversioned(self):
        body = SKILL.read_text(encoding="utf-8")
        self.assertTrue(body.startswith("---\n"))
        front = body.split("---", 2)[1]
        self.assertRegex(front, r"(?m)^name: terminology-review$")
        self.assertRegex(front, r"(?m)^description: .{30,1024}$")
        self.assertNotRegex(front, r"(?m)^\s*version:")
        self.assertLess(len(body.splitlines()), 500)

    def test_epistemic_and_safety_boundary(self):
        body = SKILL.read_text(encoding="utf-8").lower()
        for required in ["concept", "designation", "authority", "abstain", "source", "do not edit"]:
            self.assertIn(required, body)
        self.assertIn("not automatically", body)

    def test_cases_cover_misses_and_regressions(self):
        cases = mod.load_cases()
        self.assertGreaterEqual(len(cases), 10)
        classes = {c["kind"] for c in cases}
        self.assertEqual(classes, {"positive", "negative-control", "uncertain"})
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        pairs = mod.plan(cases, 1042)
        self.assertEqual(len(pairs), len(cases)*2)
        self.assertEqual(pairs, mod.plan(cases, 1042))
        self.assertEqual({a for _,a in pairs},{"baseline","with_skill"})

    def test_local_only_guard(self):
        self.assertTrue(mod.local_url("http://127.0.0.1:11434/api/chat"))
        self.assertTrue(mod.local_url("http://localhost:11434/api/chat"))
        for value in ["https://api.openai.com/api/chat","https://example.com/api/chat",
                      "http://example.com/api/chat","http://localhost:11434/v1/chat/completions",
                      "http://username@localhost:11434/api/chat","http://localhost:11434/api/chat?q=1"]:
            self.assertFalse(mod.local_url(value), value)

    def test_dry_run_does_not_call_model(self):
        r = subprocess.run([sys.executable,str(RUNNER),"--dry-run"],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        p = json.loads(r.stdout)
        self.assertEqual(p["kind"],"dry-run-no-model")
        self.assertEqual(p["total_runs"],20)


if __name__ == "__main__":
    unittest.main()
