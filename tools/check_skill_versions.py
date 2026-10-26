#!/usr/bin/env python3
"""Validate one-version Diakrisis suite registry; no per-skill release scheme."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills" / "versions.json"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def check():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 2 or data.get("project") != "diakrisis":
        raise ValueError("expected Diakrisis one-version manifest, schema v2")
    suite = data["suite"]
    if not SEMVER.fullmatch(suite["version"]):
        raise ValueError("package version must be SemVer")
    if suite["status"] not in {"unreleased", "candidate", "published", "superseded"}:
        raise ValueError("invalid suite publication status")
    if suite["status"] != "published" and (suite.get("releaseTag") or suite.get("releaseDate")):
        raise ValueError("unpublished suite cannot report a publication tag/date")
    if suite["status"] == "published" and not (suite.get("releaseTag") and suite.get("releaseDate")):
        raise ValueError("published package lacks release provenance")

    included = data["skills"]
    proposed = data["candidates"]
    all_names = []
    for name in included:
        if not isinstance(name, str):
            raise ValueError("included skills must be name strings, not individually versioned objects")
        all_names.append(name)
        path = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not path.is_file():
            raise ValueError("listed included skill missing from package: " + name)
        front = path.read_text(encoding="utf-8").split("---", 2)[1]
        if re.search(r"(?m)^\s*version\s*:", front):
            raise ValueError("remove per-skill version metadata: " + name)
    for candidate in proposed:
        if set(candidate) - {"name", "status", "pullRequest"}:
            raise ValueError("draft entry must not contain per-skill version/release fields")
        name = candidate["name"]
        if not candidate.get("pullRequest") or candidate.get("status") != "experimental":
            raise ValueError("candidate needs experimental status and PR link")
        all_names.append(name)
    if len(all_names) != len(set(all_names)) or any(not NAME.fullmatch(n) for n in all_names):
        raise ValueError("duplicate or invalid skill name")
    unlisted = {p.parent.name for p in (ROOT / ".agents" / "skills").glob("*/SKILL.md")} - set(included)
    if unlisted:
        raise ValueError("authored skills not listed as included: " + ", ".join(sorted(unlisted)))
    print(f"PASS: Diakrisis package {suite['version']} ({suite['status']}), "
          f"{len(included)} included skill(s), {len(proposed)} draft(s)")


if __name__ == "__main__":
    try:
        check()
    except (ValueError, KeyError, IndexError, OSError, TypeError) as exc:
        print("FAILED PACKAGE VERSION POLICY:", exc, file=sys.stderr)
        sys.exit(1)
