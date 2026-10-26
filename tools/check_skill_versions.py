#!/usr/bin/env python3
"""Fail if skill package/release metadata drift from authored Skill files."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills" / "versions.json"
SEMVER = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def error(message):
    raise ValueError(message)


def check():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("project") != "diakrisis":
        error("wrong package project")
    suite = data["suite"]
    if not SEMVER.fullmatch(suite["version"]):
        error("suite version is not SemVer")
    if suite["status"] not in {"unreleased", "candidate", "published", "superseded"}:
        error("invalid suite status")
    if suite["status"] != "published" and (suite.get("releaseTag") or suite.get("releaseDate")):
        error("unreleased suite must not report publication")
    if suite["status"] == "published" and not all(suite.get(k) for k in ("releaseTag", "releaseDate")):
        error("published suite missing release evidence")
    known = set()
    for field, released in (("skills", True), ("candidates", False)):
        for item in data[field]:
            name = item["name"]
            if name in known or not NAME.fullmatch(name):
                error(f"duplicate or invalid skill identity: {name}")
            known.add(name)
            version = item["version"] if released else item["proposedVersion"]
            if not SEMVER.fullmatch(version):
                error(f"invalid version: {name} {version}")
            path = ROOT / ".agents" / "skills" / name / "SKILL.md"
            if released:
                if not path.exists() or not item.get("releaseTag") or not item.get("sourceCommit"):
                    error(f"released skill missing bytes and provenance: {name}")
                front = path.read_text(encoding="utf-8").split("---", 2)[1]
                match = re.search(r'^  version:\s*["\']?([^"\'\n]+)', front, re.M)
                if not match or match.group(1).strip() != version:
                    error(f"version mismatch with SKILL.md: {name}")
            else:
                if item.get("released") is not False or not item.get("pullRequest"):
                    error(f"unreleased candidate has inconsistent release status: {name}")
    for skill in (ROOT / ".agents" / "skills").glob("*/SKILL.md"):
        if skill.parent.name not in known:
            error(f"unregistered authored skill: {skill.parent.name}")
    print(f"PASS: suite {suite['version']}, {len(data['skills'])} released skill(s), {len(data['candidates'])} draft candidate(s)")


if __name__ == "__main__":
    try:
        check()
    except (OSError, ValueError, KeyError, IndexError) as e:
        print("FAILED VERSION POLICY:", e, file=sys.stderr)
        sys.exit(1)
