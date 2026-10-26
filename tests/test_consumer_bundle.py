"""DIA-010 package-builder deterministic offline structural tests; no model calls."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("diakrisis_bundle", ROOT / "tools/build_consumer_bundle.py")
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)


class ConsumerBundleTests(unittest.TestCase):
    def test_two_builds_are_byte_identical_and_source_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            one = Path(tmp) / "one"
            two = Path(tmp) / "two"
            bundle.build(one)
            bundle.build(two)
            archives = sorted(one.glob("*.zip"))
            self.assertEqual(len(archives), 1)
            self.assertEqual(archives[0].read_bytes(), (two / archives[0].name).read_bytes())
            self.assertEqual((one / "SHA256SUMS").read_bytes(),
                             (two / "SHA256SUMS").read_bytes())
            manifest = bundle.verify(one / "bundle")
            self.assertEqual(len(manifest["files"]), 19)
            self.assertEqual(manifest["suite_version"], "0.1.0-dev.0")
            self.assertEqual(manifest["source_revision"], bundle.commit_sha())

    def test_integrity_checker_rejects_modified_review_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            target = out / "bundle/.agents/skills/argument-review/SKILL.md"
            target.write_text(target.read_text(encoding="utf-8") + "\nModified!\n",
                              encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "local file drift"):
                bundle.verify(out / "bundle")

    def test_refuse_nonempty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "existing"
            out.mkdir()
            (out / "do-not-touch").write_text("original", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not empty"):
                bundle.build(out)
            self.assertEqual((out / "do-not-touch").read_text(), "original")


if __name__ == "__main__":
    unittest.main()
