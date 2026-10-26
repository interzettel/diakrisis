#!/usr/bin/env python3
"""Generate or verify Diakrisis' README-only tracker from PRS v0.4.1 records.

No network, no Pages, no issues-to-ledger synchronization, no silent README edits.
The marker region and SVG are generated projections; ledger is authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLKIT = ROOT / "tools" / "upstream" / "project-record-standard"
sys.path.insert(0, str(TOOLKIT / "src"))

from project_record.adapters import load_config
from project_record.build import render_readme
from project_record.core import summarize
from project_record.readme import START, END

README = ROOT / "README.md"
GRAPHIC = ROOT / "assets" / "progress.svg"
CONFIG = ROOT / "progress" / "project-record.json"
VERSIONS = ROOT / "skills" / "versions.json"
THEME = ROOT / "progress" / "theme.json"


def safe(text: object) -> str:
    """Escape Markdown table delimiters and line breaks in source-owned strings."""
    return str(text if text is not None else "—").replace("|", r"\|").replace("\r", "").replace("\n", " ").strip()


def fraction(progress: dict) -> str:
    value = progress["percent"]
    return f"{progress['done']}/{progress['total']} · {value:.1f}%" if value is not None else f"{progress['done']}/{progress['total']} · Not measured"


def render() -> tuple[str, str]:
    (record,) = load_config(CONFIG)
    record = summarize(record)
    theme = json.loads(THEME.read_text(encoding="utf-8"))
    versions = json.loads(VERSIONS.read_text(encoding="utf-8"))
    svg, module = render_readme(record, theme)
    # The host has deliberately chosen README-only presentation; no missing-site warning.
    module = module.replace("Interactive route not connected. · ", "")
    source = record["source"]
    milestones = record["milestones"]
    items = record["items"]
    metrics = record["metrics"]
    breakdown = [
        "",
        "#### Milestone roadmap",
        "",
        "| Milestone | Horizon | Supporting required work | Outcome acceptance | Next gate |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for milestone in milestones:
        status = "Accepted" if milestone["accepted"] is True else ("Not accepted" if milestone["accepted"] is False else "Unknown / not assessed")
        breakdown.append(
            f"| **{safe(milestone['id'])} — {safe(milestone['title'])}**"
            f" | {safe(milestone['horizon'])} | {fraction(milestone['progress'])}"
            f" | {status} | {safe(milestone.get('nextAction') or milestone.get('goal'))} |"
        )
    breakdown.extend([
        "",
        "#### Work packages",
        "",
        "States represent recorded implementation progress; a closed issue, passing test or accepted milestone is not automatically interchangeable.",
        "",
        "| ID / issue | Work package | State | Priority | Dependencies | Evidence or next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    state_labels = {"done": "Done", "active": "In progress", "review": "In review", "ready": "Ready",
                    "backlog": "Planned", "cancelled": "Cancelled", "unknown": "Unknown"}
    for work in items:
        link = f"[{safe(work['id'])}]({work['issueUrl']})" if work.get("issueUrl") else f"`{safe(work['id'])}`"
        deps = ", ".join(work.get("dependsOn", [])) or "—"
        proof = next((e.get("source") for e in work.get("evidence", []) if e.get("kind") == "merged-pr"), None)
        proof = f"[Evidence]({proof})" if proof and proof.startswith("https://") else safe(work.get("criterion") or "Check work criterion")
        if not work["required"]:
            proof += " · deferred from required scope"
        if work.get("blocked"):
            proof += " · Blocked flag (reason in source)"
        breakdown.append(
            f"| {link} | {safe(work['title'])} | {state_labels.get(work['state'], safe(work['state']))}"
            f" | {safe(work.get('priority'))} | {safe(deps)} | {proof} |"
        )
    candidates = versions.get("candidates", [])
    draft = ", ".join(
        f"`{safe(c['name'])}` {safe(c['proposedVersion'])} (draft, [PR #{str(c['pullRequest']).rstrip('/').split('/')[-1]}]({c['pullRequest']}))"
        for c in candidates
    ) or "None"
    breakdown.extend([
        "",
        f"**Versioning:** Suite `{safe(versions['suite']['version'])}` — **{safe(versions['suite']['status'])}**; released skills: **{len(versions['skills'])}**. "
        f"Draft candidates: {draft}. [Per-skill version and release policy](docs/VERSIONING.md).",
        "",
        f"**Source coverage:** observed **{source['observedOn']}**, authoritative "
        "[ledger](progress/ledger.json), [manifest](progress/project-record.json), "
        "[scope history](progress/history/2026-10-26-unapproved.json). "
        "Regeneration does not fetch newer issues or change the observation date.",
        "",
        f"**Counts:** required work **{fraction(metrics['work'])}**; retained work "
        f"**{fraction(metrics['ledger'])}**; accepted milestones "
        f"**{'Unknown' if metrics['milestones']['percent'] is None else str(metrics['milestones']['percent']) + '%'}** "
        f"({metrics['milestones']['known']} of {metrics['milestones']['total']} determinate).",
        "",
    ])
    if module.count(START) != 1 or module.count(END) != 1:
        raise ValueError("Upstream README module lost its markers")
    module = module.replace(END, "\n".join(breakdown) + "\n" + END)
    original = README.read_text(encoding="utf-8")
    if original.count(START) != 1 or original.count(END) != 1 or original.index(START) > original.index(END):
        raise ValueError("README must have exactly one valid project-record marker pair")
    transformed = (original[:original.index(START)] + module[module.index(START):module.index(END) + len(END)]
                   + original[original.index(END) + len(END):])
    return transformed, svg + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="Fail if README/SVG are stale")
    modes.add_argument("--write", action="store_true", help="Update the generated region and SVG")
    modes.add_argument("--emit-hex", action="store_true", help="Emit generated content for controlled GitHub bootstrap")
    args = parser.parse_args()
    readme, svg = render()
    if args.emit_hex:
        print("DIA_README_HEX_START" + readme.encode("utf-8").hex() + "DIA_README_HEX_END")
        print("DIA_SVG_HEX_START" + svg.encode("utf-8").hex() + "DIA_SVG_HEX_END")
        return 0
    if args.write:
        README.write_text(readme, encoding="utf-8")
        GRAPHIC.parent.mkdir(parents=True, exist_ok=True)
        GRAPHIC.write_text(svg, encoding="utf-8")
        print("Generated README marker and assets/progress.svg from approved source records")
        return 0
    checks = [
        ("README.md", README.is_file() and README.read_text(encoding="utf-8") == readme),
        ("assets/progress.svg", GRAPHIC.is_file() and GRAPHIC.read_text(encoding="utf-8") == svg)
    ]
    for filename, passed in checks:
        print(("OK " if passed else "STALE ") + filename)
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
