#!/usr/bin/env python3
"""DIA-010: deterministic, offline, nonpublishing Diakrisis consumer bundle.

Build: python tools/build_consumer_bundle.py --output /tmp/dia-build
Check: python tools/build_consumer_bundle.py --check-consumer /tmp/dia-build/bundle
All source paths are local. This script never installs globally or calls models.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZipFile, ZipInfo, ZIP_STORED

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("argument-review", "communication-review", "conceptual-model-review",
         "consistency-review", "method-review", "review-coordinator",
         "terminology-review")
SKILLS = tuple(".agents/skills/" + n + "/SKILL.md" for n in NAMES)
SUPPORT = (".agents/skills/terminology-review/references/CASES.md",
           "LICENSE", "docs/FOUNDATION.md", "docs/REVIEW-CONTRACT.md",
           "docs/COORDINATION.md",
           "docs/research/DIA-005-AUTHORITY.md", "evals/finding-contract/cases.json",
           "schemas/finding.schema.json", "schemas/review-report.schema.json",
           "schemas/coordinated-report.schema.json", "tools/coordinate_reviews.py",
           "skills/versions.json")
INPUTS = SKILLS + SUPPORT
# DIA-008 added these three files; consumers pinned before it (e.g. Writing
# Kitchen at a72b28e) carry the 16-file roster that PR #26 first shipped.
COORDINATOR_SUPPORT = ("docs/COORDINATION.md", "schemas/coordinated-report.schema.json",
                       "tools/coordinate_reviews.py")
LEGACY_INPUTS = tuple(p for p in INPUTS if p not in COORDINATOR_SUPPORT)
ROSTERS = {"current-19": frozenset(INPUTS), "legacy-16": frozenset(LEGACY_INPUTS)}
MANIFEST = "integrations/diakrisis/source-manifest.json"
LINKS = re.compile(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def blob(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode() + data).hexdigest()


def commit_sha():
    x = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                       capture_output=True, text=True, check=True).stdout.strip()
    if not re.fullmatch("[0-9a-f]{40}", x):
        raise ValueError("checkout revision is not full git commit")
    return x


def dest_of(src):
    return src if src.startswith(".agents/skills/") else "integrations/diakrisis/" + src


def transform(src, data, sha):
    if src in SKILLS:
        t = data.decode("utf-8")
        t = t.replace("../../../schemas/finding.schema.json",
                      "../../../integrations/diakrisis/schemas/finding.schema.json")
        t = t.replace("../../../docs/REVIEW-CONTRACT.md",
                      "../../../integrations/diakrisis/docs/REVIEW-CONTRACT.md")
        t = t.replace("../../../docs/COORDINATION.md",
                      "../../../integrations/diakrisis/docs/COORDINATION.md")
        t = t.replace("../../../schemas/coordinated-report.schema.json",
                      "../../../integrations/diakrisis/schemas/coordinated-report.schema.json")
        return t.encode("utf-8"), "consumer-path-rewrites-v1"
    if src == "docs/FOUNDATION.md":
        t = data.decode("utf-8").replace(
            "../evals/pilot-cases.json",
            "https://github.com/interzettel/diakrisis/blob/" + sha + "/evals/pilot-cases.json"
        ).replace(
            "(USAGE.md)",
            "(https://github.com/interzettel/diakrisis/blob/" + sha + "/docs/USAGE.md)"
        )
        return t.encode("utf-8"), "pin-nonbundled-document-links"
    if src == "docs/COORDINATION.md":
        t = data.decode("utf-8").replace(
            "../tests/test_coordinator_composition.py",
            "https://github.com/interzettel/diakrisis/blob/" + sha + "/tests/test_coordinator_composition.py"
        ).replace(
            "(research/review-coordinator-2026-10-26.md)",
            "(https://github.com/interzettel/diakrisis/blob/" + sha + "/docs/research/review-coordinator-2026-10-26.md)"
        )
        return t.encode("utf-8"), "pin-nonbundled-document-links"
    return data, "byte-identical"


def within(root, rel, reject_symlinks=False):
    part = Path(rel)
    if part.is_absolute() or ".." in part.parts:
        raise ValueError("unsafe path: " + rel)
    if reject_symlinks:
        # Inspect each component BEFORE resolving: resolve() follows links, so a
        # symlink check on the resolved path can never fire.
        current = root
        for name in part.parts:
            current = current / name
            if current.is_symlink():
                raise ValueError("symlink in consumer path: " + rel)
    target = (root / part).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("path escaped checkout: " + rel)
    return target


def upstream_blobs(revision, paths):
    """Git blob IDs of `paths` at `revision` in this checkout, or None when the
    revision is not available here (shallow clone, other machine, no git)."""
    try:
        present = subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"], cwd=ROOT,
                                 capture_output=True, text=True, check=False)
    except OSError:
        return None
    if present.returncode != 0:
        return None
    blobs = {}
    for path in paths:
        found = subprocess.run(["git", "rev-parse", revision + ":" + path], cwd=ROOT,
                               capture_output=True, text=True, check=False)
        if found.returncode != 0:
            raise ValueError("file not present in upstream revision: " + path)
        blobs[path] = found.stdout.strip()
    return blobs


def verify(consumer):
    return verify_report(consumer)["manifest"]


def verify_report(consumer):
    """Check a consumer bundle; report its roster and whether the recorded
    source blobs could be compared with upstream git in this checkout."""
    consumer = consumer.resolve()
    manifest = json.loads((consumer / MANIFEST).read_text(encoding="utf-8"))
    reg = json.loads((consumer / "integrations/diakrisis/skills/versions.json").read_text(encoding="utf-8"))
    if manifest["suite_version"] != reg["suite"]["version"] or set(reg["skills"]) != set(NAMES):
        raise ValueError("package version or skill registry differs")
    if manifest["source_repository"] != "interzettel/diakrisis":
        raise ValueError("different upstream")
    # Untrusted input reaches git arguments below: allow only a full commit ID.
    if not re.fullmatch("[0-9a-f]{40}", str(manifest["source_revision"])):
        raise ValueError("source revision is not a full git commit ID")
    sources = [f["source_path"] for f in manifest["files"]]
    if len(sources) != len(set(sources)):
        raise ValueError("duplicate source path in manifest")
    roster = next((name for name, paths in ROSTERS.items() if set(sources) == paths), None)
    if roster is None:
        raise ValueError("file set matches neither the legacy 16-file nor the current "
                         "19-file roster (partial, extra or mixed bundle)")
    names = set()
    seen = set()
    for f in manifest["files"]:
        rel = f["installed_path"]
        if rel != dest_of(f["source_path"]):
            raise ValueError("unexpected installed path: " + rel)
        if rel in seen:
            raise ValueError("duplicate path: " + rel)
        seen.add(rel)
        p = within(consumer, rel, reject_symlinks=True)
        if not p.is_file():
            raise ValueError("missing file: " + rel)
        data = p.read_bytes()
        if blob(data) != f["installed_git_blob"]:
            raise ValueError("local file drift: " + rel)
        if f["transformation"] == "byte-identical" and blob(data) != f["source_git_blob"]:
            raise ValueError("installed file differs from its recorded source blob: " + rel)
        if f["source_revision"] != manifest["source_revision"]:
            raise ValueError("mixed source revisions")
        if p.name == "SKILL.md":
            name = p.parent.name
            names.add(name)
            if ("name: " + name) not in data.decode("utf-8").split("---", 2)[1]:
                raise ValueError("skill metadata mismatch: " + rel)
        if p.suffix == ".json":
            json.loads(data)
        if p.suffix == ".md":
            for link in LINKS.findall(data.decode("utf-8")):
                link = link.split("#", 1)[0]
                if not link or ":" in link or link.startswith("/"):
                    continue
                target = (p.parent / link).resolve()
                if not target.is_relative_to(consumer.resolve()) or not target.is_file():
                    raise ValueError("broken local reference in " + rel + ": " + link)
    if names != set(NAMES):
        raise ValueError("missing reviewer")
    blobs = upstream_blobs(manifest["source_revision"], sources)
    if blobs is None:
        upstream = "not-verifiable-here"
    else:
        for f in manifest["files"]:
            if blobs[f["source_path"]] != f["source_git_blob"]:
                raise ValueError("recorded source blob differs from upstream git: " + f["source_path"])
        upstream = "verified"
    return {"manifest": manifest, "roster": roster, "upstream": upstream}


def build(output):
    output = output.resolve()
    if output.is_relative_to(ROOT) or ROOT == output:
        raise ValueError("output must be outside source tree")
    if output.exists() and any(output.iterdir()):
        raise ValueError("output directory not empty")
    output.mkdir(parents=True, exist_ok=True)
    sha = commit_sha()
    reg = json.loads((ROOT / "skills/versions.json").read_text())
    if set(reg["skills"]) != set(NAMES) or reg["suite"]["status"] != "unreleased":
        raise ValueError("unsupported package roster or release status")
    version = reg["suite"]["version"]
    consumer = output / "bundle"
    consumer.mkdir()
    files = []
    for src in INPUTS:
        original = (ROOT / src).read_bytes()
        content, method = transform(src, original, sha)
        dst = dest_of(src)
        path = within(consumer, dst)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        files.append(dict(source_path=src, source_git_blob=blob(original),
                          installed_path=dst, installed_git_blob=blob(content),
                          transformation=method, source_revision=sha))
    manifest = dict(schema_version=1, owner_record="DIA-010 / DIA-M3",
                    source_repository="interzettel/diakrisis", source_revision=sha,
                    suite_version=version, suite_status="unreleased-experimental",
                    files=files)
    out = consumer / MANIFEST
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    verify(consumer)
    archive = output / ("diakrisis-consumer-" + version + ".zip")
    with ZipFile(archive, "w", compression=ZIP_STORED) as z:
        for path in sorted(consumer.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(consumer).as_posix()
            zi = ZipInfo(rel, (1980, 1, 1, 0, 0, 0))
            zi.compress_type = ZIP_STORED
            zi.external_attr = 0o100644 << 16
            z.writestr(zi, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(digest + "  " + archive.name + "\n")
    print("Prepared only (NOT PUBLISHED):", archive.name, digest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--check-consumer", type=Path)
    parser.add_argument("--strict-current", action="store_true")
    args = parser.parse_args()
    if args.output:
        build(args.output)
    else:
        report = verify_report(args.check_consumer.resolve())
        item = report["manifest"]
        print("PASS:", len(item["files"]), "pinned source files")
        print("Roster:", report["roster"])
        if report["upstream"] == "verified":
            print("Upstream: recorded source blobs match git at", item["source_revision"])
        else:
            print("Upstream: source revision", item["source_revision"],
                  "is not in this checkout; recorded source blobs not verified here")
        if commit_sha() != item["source_revision"]:
            print("Source update available (no automatic upgrade)")
            if args.strict_current:
                return 3
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("DIA-010 packaging failure:", e, file=sys.stderr)
        sys.exit(1)
