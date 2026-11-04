#!/usr/bin/env python3
"""Generate or verify Diakrisis' README-only tracker from PRS v0.4.1 records.

No network, no Pages, no issues-to-ledger synchronization, no silent README edits.
The marker region and SVG are generated projections; ledger is authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
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


PULL = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)$")
ISO_DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def evidence_cell(work: dict) -> str:
    """Link the first pull request among a work item's evidence, whatever its
    `kind` label; fall back to the completion criterion."""
    for entry in work.get("evidence", []):
        match = PULL.match(str(entry.get("source", "")))
        if match:
            owner, repo, number = match.groups()
            label = f"PR #{number}" if (owner, repo) == ("interzettel", "diakrisis") else f"{repo} PR #{number}"
            return f"[{label}]({entry['source']})"
    return safe(work.get("criterion") or "Check work criterion")


def stale_update_date(ledger: dict, updated_on: str) -> str | None:
    """Newest ISO date written in ledger narrative (notes, warnings, milestone
    next actions) when it is later than the manifest's updatedOn, else None."""
    texts = [item.get("note") or "" for item in ledger.get("items", [])]
    texts += [w or "" for w in ledger.get("warnings", [])]
    texts += [m.get("nextAction") or "" for m in ledger.get("milestones", [])]
    dates = [d for text in texts for d in ISO_DATE.findall(text)]
    newest = max(dates, default=None)
    return newest if newest and newest > updated_on else None


def fraction(progress: dict) -> str:
    value = progress["percent"]
    return f"{progress['done']}/{progress['total']} · {value:.1f}%" if value is not None else f"{progress['done']}/{progress['total']} · not yet assessed"


def progress_svg(items: list[dict], milestones: list[dict], source: dict, theme: dict) -> str:
    """The README graphic: every required work package by state, and milestone acceptance.

    Drawn here rather than by the upstream renderer, whose layout let long values
    overlap their neighbours. Each value sits on its own line, so no two texts share
    a row, and the bar shows in-progress work beside completed work.
    """
    from html import escape
    c = theme["light"]
    required = [w for w in items if w["required"]]
    done = sum(w["state"] == "done" for w in required)
    active = sum(w["state"] in ("active", "review", "ready") for w in required)
    planned = len(required) - done - active
    blocked = sum(bool(w.get("blocked")) for w in required)
    total = len(required) or 1
    accepted = sum(m["accepted"] is True for m in milestones)
    assessed = sum(m["accepted"] is not None for m in milestones)
    width, bar = 350, []
    x = 28.0
    for count, fill in ((done, c["accent"]), (active, "#7FAF9F")):
        w = width * count / total
        if w:
            bar.append(f'<rect x="{x:.2f}" y="146" width="{w:.2f}" height="10" fill="{fill}"/>')
        x += w
    t = lambda x, y, size, text, weight="400", fill=c["text"]: (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(text)}</text>')
    detail = f"{active} in progress · {planned} planned" + (f" · {blocked} flagged blocked" if blocked else "")
    m_detail = (f"{assessed} of {len(milestones)} assessed by the owner" if assessed
                else "Acceptance not yet assessed by the owner")
    legend = []
    for n, (label, fill) in enumerate((("Done", c["accent"]), ("In progress", "#7FAF9F"), ("Planned", c["border"]))):
        lx = 28 + n * 110
        legend.append(f'<rect x="{lx}" y="170" width="10" height="10" rx="2" fill="{fill}"/>' + t(lx + 16, 179, 12, label, fill=c["muted"]))
    desc = (f"Required work: {done} of {len(required)} work packages done, {active} in progress, {planned} planned. "
            f"Milestones: {accepted} of {len(milestones)} accepted. Observed {source['observedOn']}.")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 840 226">',
        '<title id="title">Diakrisis · project tracker</title>', f'<desc id="desc">{escape(desc)}</desc>',
        f'<rect width="840" height="226" rx="10" fill="{c["background"]}"/>',
        f'<g font-family="{escape(theme["font"])}">',
        t(28, 37, 18, "Diakrisis · project tracker", "700"),
        t(28, 72, 14, "Required work packages"), t(28, 108, 28, f"{done} / {len(required)} done", "700"),
        t(28, 132, 13, detail, fill=c["muted"]),
        f'<rect x="28" y="146" width="{width}" height="10" fill="{c["border"]}"/>', *bar,
        t(445, 72, 14, "Milestones"), t(445, 108, 28, f"{accepted} / {len(milestones)} accepted", "700"),
        t(445, 132, 13, m_detail, fill=c["muted"]),
        f'<rect x="445" y="146" width="{width}" height="10" fill="{c["border"]}"/>',
        *([f'<rect x="445" y="146" width="{width * accepted / len(milestones):.2f}" height="10" fill="{c["accent"]}"/>']
          if accepted else []),
        *legend,
        t(28, 208, 12, f"Observed {source['observedOn']} · from progress/ledger.json", fill=c["muted"]),
        "</g></svg>",
    ]
    return "".join(parts)


def render() -> tuple[str, str]:
    manifest = json.loads(CONFIG.read_text(encoding="utf-8"))
    ledger = json.loads((CONFIG.parent / manifest["projects"][0]["sourceFile"]).read_text(encoding="utf-8"))
    updated_on = manifest["projects"][0]["source"]["updatedOn"]
    newer = stale_update_date(ledger, updated_on)
    if newer:
        raise ValueError(f"ledger mentions {newer} but progress/project-record.json updatedOn is "
                         f"{updated_on}; update observedOn/updatedOn after reconciling, then regenerate")
    (record,) = load_config(CONFIG)
    record = summarize(record)
    theme = json.loads(THEME.read_text(encoding="utf-8"))
    versions = json.loads(VERSIONS.read_text(encoding="utf-8"))
    _, module = render_readme(record, theme)
    # The host has deliberately chosen README-only presentation; no missing-site warning.
    module = module.replace("Interactive route not connected. · ", "")
    source = record["source"]
    milestones = record["milestones"]
    items = record["items"]
    metrics = record["metrics"]
    svg = progress_svg(items, milestones, source, theme)
    module = module.replace("Not measured", "not yet assessed").replace("![Diakrisis · current required scope]", "![Diakrisis · project tracker]", 1)
    required = [w for w in items if w["required"]]
    in_progress = sum(w["state"] in ("active", "review", "ready") for w in required)
    row = "| Required work |"
    if module.count(row) == 1:
        start = module.index(row)
        end = module.index("\n", start)
        module = (module[:end + 1] + f"| Work in progress | {in_progress}/{len(required)} | Leaf items started but not done (not counted as completed). |\n"
                  + module[end + 1:])
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
        proof = evidence_cell(work)
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
        f"`{safe(c['name'])}` (draft, [PR #{str(c['pullRequest']).rstrip('/').split('/')[-1]}]({c['pullRequest']}))"
        for c in candidates
    ) or "None"
    breakdown.extend([
        "",
        f"**Versioning:** Suite `{safe(versions['suite']['version'])}` — **{safe(versions['suite']['status'])}**; included skills: **{len(versions['skills'])}**. "
        f"Draft candidates: {draft}. [Single package version policy](docs/VERSIONING.md).",
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
    try:
        readme, svg = render()
    except ValueError as error:
        print("STALE source dates:", error)
        return 1
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
