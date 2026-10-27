"""DIA-010 package-builder deterministic offline structural tests; no model calls."""
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("diakrisis_bundle", ROOT / "tools/build_consumer_bundle.py")
bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bundle)

MANIFEST = "integrations/diakrisis/source-manifest.json"
COORDINATOR_FILES = {"docs/COORDINATION.md", "schemas/coordinated-report.schema.json",
                     "tools/coordinate_reviews.py"}
UNKNOWN_REVISION = "0" * 40  # a revision no local checkout contains


def _manifest(consumer):
    return json.loads((consumer / MANIFEST).read_text(encoding="utf-8"))


def _save(consumer, manifest):
    (consumer / MANIFEST).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _rehash(manifest, rel, data):
    for entry in manifest["files"]:
        if entry["installed_path"] == rel:
            entry["installed_git_blob"] = bundle.blob(data)
            if entry["transformation"] == "byte-identical":
                entry["source_git_blob"] = bundle.blob(data)


def make_legacy(consumer):
    """Synthetic stand-in for a pre-DIA-008 consumer such as Writing Kitchen's
    16-file snapshot: no coordinator files, no links to them, and a pinned
    source revision this checkout does not contain."""
    manifest = _manifest(consumer)
    kept = []
    for entry in manifest["files"]:
        if entry["source_path"] in COORDINATOR_FILES:
            (consumer / entry["installed_path"]).unlink()
        else:
            kept.append(entry)
    manifest["files"] = kept
    link = re.compile(r"\[([^\]]+)\]\([^)]*(?:COORDINATION\.md|coordinated-report\.schema\.json"
                      r"|coordinate_reviews\.py)[^)]*\)")
    for entry in kept:
        path = consumer / entry["installed_path"]
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        stripped = link.sub(r"\1", text)
        if stripped != text:
            path.write_text(stripped, encoding="utf-8")
            _rehash(manifest, entry["installed_path"], stripped.encode("utf-8"))
    manifest["source_revision"] = UNKNOWN_REVISION
    for entry in kept:
        entry["source_revision"] = UNKNOWN_REVISION
    _save(consumer, manifest)
    return manifest


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

    def test_packaged_coordinator_runs_against_local_schemas(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            script = out / "bundle/integrations/diakrisis/tools/coordinate_reviews.py"
            example = ROOT / "evals/coordinator/example.json"
            result_path = Path(tmp) / "combined.json"
            run = subprocess.run(
                [sys.executable, str(script), "--input", str(example),
                 "--output", str(result_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            report = __import__("json").loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(len(report["report"]["findings"]), 2)
            self.assertEqual(len(report["groups"]), 1)

    def test_legacy_16_file_consumer_is_accepted_not_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            make_legacy(out / "bundle")
            report = bundle.verify_report(out / "bundle")
            self.assertEqual(report["roster"], "legacy-16")
            self.assertEqual(len(report["manifest"]["files"]), 16)
            self.assertEqual(report["upstream"], "not-verifiable-here")

    def test_current_bundle_reports_current_roster_and_verified_upstream(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            report = bundle.verify_report(out / "bundle")
            self.assertEqual(report["roster"], "current-19")
            self.assertEqual(report["upstream"], "verified")

    def test_partial_extra_or_swapped_rosters_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            consumer = out / "bundle"
            original = _manifest(consumer)
            # 18 files: one coordinator file missing.
            partial = json.loads(json.dumps(original))
            partial["files"] = [f for f in partial["files"]
                                if f["source_path"] != "tools/coordinate_reviews.py"]
            _save(consumer, partial)
            with self.assertRaisesRegex(ValueError, "roster"):
                bundle.verify(consumer)
            # 19 entries, but one known file swapped for an unknown path.
            swapped = json.loads(json.dumps(original))
            entry = next(f for f in swapped["files"] if f["source_path"] == "LICENSE")
            entry["source_path"] = "docs/NOT-IN-ANY-ROSTER.md"
            _save(consumer, swapped)
            with self.assertRaisesRegex(ValueError, "roster"):
                bundle.verify(consumer)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlinked_file_inside_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            consumer = out / "bundle"
            target = consumer / "integrations/diakrisis/LICENSE"
            alias = consumer / ".license-copy"
            target.rename(alias)
            try:
                target.symlink_to(Path("../..") / alias.name)
            except OSError as exc:  # e.g. Windows without symlink privilege
                self.skipTest(f"cannot create symlink: {exc}")
            with self.assertRaisesRegex(ValueError, "symlink"):
                bundle.verify(consumer)

    def test_recorded_source_blob_is_checked_against_upstream_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pkg"
            bundle.build(out)
            consumer = out / "bundle"
            manifest = _manifest(consumer)
            entry = next(f for f in manifest["files"]
                         if f["source_path"].endswith("argument-review/SKILL.md"))
            entry["source_git_blob"] = "f" * 40
            _save(consumer, manifest)
            with self.assertRaisesRegex(ValueError, "upstream git"):
                bundle.verify(consumer)

    def test_refuse_nonempty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "existing"
            out.mkdir()
            (out / "do-not-touch").write_text("original", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not empty"):
                bundle.build(out)
            self.assertEqual((out / "do-not-touch").read_text(), "original")


class UncommittedFilesTests(unittest.TestCase):
    def test_modified_and_untracked_bundled_files_are_listed(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git = lambda *a: subprocess.run(["git", *a], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            (root / "a.md").write_text("a\n", encoding="utf-8")
            (root / "other.md").write_text("o\n", encoding="utf-8")
            git("add", ".")
            git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c")
            self.assertEqual(bundle.uncommitted(["a.md", "b.md"], root), [])
            (root / "a.md").write_text("changed\n", encoding="utf-8")
            (root / "b.md").write_text("new\n", encoding="utf-8")
            (root / "other.md").write_text("not bundled\n", encoding="utf-8")
            self.assertEqual(bundle.uncommitted(["a.md", "b.md"], root), ["a.md", "b.md"])


if __name__ == "__main__":
    unittest.main()
