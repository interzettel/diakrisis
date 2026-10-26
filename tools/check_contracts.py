#!/usr/bin/env python3
"""Dependency-free checks for the authored Diakrisis bootstrap records."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "docs/FOUNDATION.md",
    "docs/ROADMAP.md", "docs/SOURCES.md",
    "docs/AGENT-SKILLS-STANDARD.md", "docs/INSTALLATION.md",
    "progress/overview.md", "progress/discovery.json", "progress/adoption.md",
    "progress/project-record.json", "progress/ledger.json", "progress/theme.json",
    "docs/REVIEW-CONTRACT.md", "docs/RESEARCH-GATE.md", "schemas/finding.schema.json", "evals/pilot-cases.json",
    "tools/bootstrap_skills.py",
]
PINS = {
    "superpowers": "2ce8aa15d05bd57213e6f746f953aafb7ded7a8b",
    "anthropic-skills": "dbd4588f9e1033efb41dad4bef2f7947c8993d44",
    "project-record-standard": "ebc6afb0b977ff3d7605893c73ac63021775c4d3",
}


def check():
    errors = []
    for p in REQUIRED:
        if not (ROOT / p).is_file():
            errors.append("missing " + p)
    try:
        data = json.loads((ROOT / "progress/discovery.json").read_text(encoding="utf-8"))
        assert data.get("repository") == "interzettel/diakrisis"
        assert data.get("coverage")
    except (ValueError, OSError, AssertionError) as e:
        errors.append(f"invalid discovery record: {e}")
    try:
        fixture = json.loads((ROOT / "evals/pilot-cases.json").read_text(encoding="utf-8"))
        examples = fixture["cases"]
        ids = [x["id"] for x in examples]
        if len(ids) != len(set(ids)):
            errors.append("duplicate evaluation fixture IDs")
        for reviewer in ["terminology-review", "conceptual-model-review", "argument-review"]:
            selected = [c for c in examples if c["reviewer"] == reviewer]
            if {c["class"] for c in selected} != {"positive", "negative-control"}:
                errors.append(f"missing positive/negative-control pair for {reviewer}")
        schema = json.loads((ROOT / "schemas/finding.schema.json").read_text(encoding="utf-8"))
        if not schema.get("required") or schema.get("additionalProperties") is not False:
            errors.append("review schema lacks required/closed fields")
    except (ValueError, OSError, KeyError, TypeError) as e:
        errors.append(f"invalid pilot fixtures/review schema: {e}")
    for skillfile in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
        name = skillfile.parent.name
        content = skillfile.read_text(encoding="utf-8")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"illegal skill name: {name}")
        if not content.startswith("---\n") or not re.search(r"^name: " + re.escape(name) + r"$", content, re.M):
            errors.append(f"invalid skill metadata: {skillfile}")
        research = sorted((ROOT / "docs" / "research").glob(f"{name}-????-??-??.md"))
        if not research:
            errors.append(f"missing dated external-source research gate: {name}")
        elif not ("https://" in research[-1].read_text(encoding="utf-8")
                  and "## " in research[-1].read_text(encoding="utf-8")):
            errors.append(f"research gate missing external references or decisions: {name}")
    bootstrap = (ROOT / "tools/bootstrap_skills.py").read_text(encoding="utf-8") if (ROOT / "tools/bootstrap_skills.py").exists() else ""
    for name, pin in PINS.items():
        if pin not in bootstrap:
            errors.append(f"unrecorded bootstrap pin: {name}")
    return errors


if __name__ == "__main__":
    failures = check()
    if failures:
        for f in failures:
            print("FAIL:", f)
        sys.exit(1)
    print("PASS: bootstrap record structure and current skill header checks")
