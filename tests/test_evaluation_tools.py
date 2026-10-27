"""DIA-007 evaluation tooling: exposure labels, blind pooling, overlap check. No model."""
import glob
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BLIND = ROOT / "tools/blind_pool.py"
OVERLAP = ROOT / "tools/overlap_check.py"
FIXTURES = {"evals/pilot-cases.json": "passage", "evals/terminology-review/cases.json": "text"}
STATUSES = {"held-out", "seen-same-skill", "seen-other-skill"}


def shingles(text, n=6):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def cases():
    for path, field in FIXTURES.items():
        for case in json.loads((ROOT / path).read_text(encoding="utf-8"))["cases"]:
            yield case, field


class ExposureLabelTests(unittest.TestCase):
    def test_every_case_has_a_checked_exposure_label(self):
        for case, _ in cases():
            with self.subTest(case=case["id"]):
                exposure = case["exposure"]
                self.assertIn(exposure["status"], STATUSES)
                self.assertTrue(exposure["basis"])
                if exposure["status"] != "held-out":
                    self.assertTrue((ROOT / exposure["source"]).is_file())

    def test_readme_table_matches_labels(self):
        readme = (ROOT / "evals/README.md").read_text(encoding="utf-8")
        for status in STATUSES:
            row = re.search(rf"^\| `{status}` \|[^|]*\| (.+) \|$", readme, re.M)
            listed = set(row.group(1).split(", "))
            labelled = {c["id"] for c, _ in cases() if c["exposure"]["status"] == status}
            self.assertEqual(listed, labelled, status)

    def test_no_case_reuses_skill_wording(self):
        skill_text = set()
        for path in glob.glob(str(ROOT / ".agents/skills/**/*.md"), recursive=True):
            skill_text |= shingles(Path(path).read_text(encoding="utf-8"))
        for case, field in cases():
            with self.subTest(case=case["id"]):
                self.assertFalse(shingles(case[field] + " " + case["context"]) & skill_text)


class BlindPoolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.corpus = base / "corpus"
        self.corpus.mkdir()
        (self.corpus / "doc.md").write_text("The pavilion opens at dawn. Visitors adjust the panels.\n", encoding="utf-8")
        git = lambda *a: subprocess.run(["git", *a], cwd=self.corpus, check=True, capture_output=True, text=True)
        git("init", "-q")
        git("add", "doc.md")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "corpus")
        revision = git("rev-parse", "HEAD").stdout.strip()
        self.runs = base / "runs"
        self.runs.mkdir()
        finding = lambda span: {"location": "p1", "span": span, "problem": "p", "proposed_change": "c", "importance": "High"}
        (self.runs / "D-arg-S.json").write_text(json.dumps({"findings": [finding("opens at dawn")]}), encoding="utf-8")
        (self.runs / "D-arg-B.json").write_text(json.dumps({"findings": [finding("closes at dusk"), finding("adjust the panels")]}), encoding="utf-8")
        (self.runs / "D-arg-S.contract.json").write_text("{}", encoding="utf-8")
        self.config = base / "cells.json"
        self.config.write_text(json.dumps({"root": str(self.corpus), "revision": revision, "documents": {"D": "doc.md"}}), encoding="utf-8")
        self.out = base / "out"

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *extra):
        return subprocess.run([sys.executable, str(BLIND), "--runs", str(self.runs), "--config", str(self.config),
                               "--out", str(self.out), *extra], capture_output=True, text=True)

    def test_pool_hides_arm_and_key_hash_is_printed(self):
        result = self.run_tool("--seed", "7")
        self.assertEqual(result.returncode, 0, result.stderr)
        pool = json.loads((self.out / "pool.json").read_text(encoding="utf-8"))
        self.assertEqual([f["id"] for f in pool], ["D-01", "D-02", "D-03"])
        for finding in pool:
            self.assertFalse({"arm", "rank", "quote_check"} & set(finding))
            self.assertEqual(finding["importance"], "high")
        key_bytes = (self.out / "key.json").read_bytes()
        self.assertIn(hashlib.sha256(key_bytes).hexdigest(), result.stdout)
        key = json.loads(key_bytes)
        self.assertEqual(sorted(e["arm"] for e in key["entries"].values()), ["B", "B", "S"])
        statuses = sorted(e["quote_check"] for e in key["entries"].values())
        self.assertEqual(statuses, ["found", "found", "missing"])

    def test_same_seed_same_order_and_key_is_never_overwritten(self):
        self.assertEqual(self.run_tool("--seed", "7").returncode, 0)
        first = (self.out / "pool.json").read_text(encoding="utf-8")
        self.assertEqual(self.run_tool("--seed", "7").returncode, 2)  # sealed key exists
        (self.out / "key.json").unlink()
        self.assertEqual(self.run_tool("--seed", "7").returncode, 0)
        self.assertEqual((self.out / "pool.json").read_text(encoding="utf-8"), first)

    def test_badly_named_run_is_refused(self):
        (self.runs / "notes.json").write_text("{}", encoding="utf-8")
        self.assertEqual(self.run_tool().returncode, 2)


class OverlapCheckTests(unittest.TestCase):
    def test_reused_skill_sentence_is_counted_and_fresh_text_is_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            reused = Path(tmp) / "reused.md"
            fresh = Path(tmp) / "fresh.md"
            skill = (ROOT / ".agents/skills/argument-review/SKILL.md").read_text(encoding="utf-8")
            reused.write_text(skill[:400], encoding="utf-8")
            fresh.write_text("Pneumatic enclosures were hosted in a municipal park for six weeks.", encoding="utf-8")
            run = lambda *a: subprocess.run([sys.executable, str(OVERLAP), *a], capture_output=True, text=True)
            self.assertEqual(run(str(fresh), "--fail-on-overlap").returncode, 0)
            result = run(str(reused), "--fail-on-overlap")
            self.assertEqual(result.returncode, 1)
            self.assertGreater(json.loads(result.stdout)["results"][str(reused)]["shared"], 0)
            self.assertEqual(run(str(fresh), "--n", "2").returncode, 2)


if __name__ == "__main__":
    unittest.main()
