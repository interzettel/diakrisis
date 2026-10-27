#!/usr/bin/env python3
"""DIA-005: check that quoted spans in Diakrisis findings exist in their files.

Reads one JSON file holding a finding, a review report, a coordinated report or
coordinator input. For every artifact span and every basis span that names a
local file, it looks for the quoted text in that file at the stated revision
(read through git when the revision is a commit) or in the working tree when
no revision is given.

Statuses: found · found-normalized (matches only after collapsing whitespace) ·
missing · file-not-found · not-checkable (remote source, location rather than
quote, path outside the root, revision not available here, unreadable file).

It proves a quote exists, never that it supports the claim. Offline, read-only;
inputs are untrusted data.

python tools/check_spans.py --input findings.json [--root DIR] [--strict] [--json]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

COMMIT = re.compile(r"^[0-9a-f]{7,40}$")
LOCATION = re.compile(r"^\s*(?:lines?|l\.|§|section|sect\.|para(?:graph)?|page|p\.|row|cell|L)\s*\d", re.I)
FAILURES = {"missing", "file-not-found"}


def findings_in(document: object) -> list[dict]:
    """Findings from a finding, review report, coordinated report or coordinator input."""
    if not isinstance(document, dict):
        raise ValueError("expected a JSON object")
    if "artifact" in document and "basis" in document:
        return [document]
    if isinstance(document.get("findings"), list):
        return [f for f in document["findings"] if isinstance(f, dict)]
    if isinstance(document.get("report"), dict):
        return findings_in(document["report"])
    if isinstance(document.get("inputs"), list):
        collected = []
        for entry in document["inputs"]:
            if isinstance(entry, dict) and isinstance(entry.get("report"), dict):
                collected.extend(findings_in(entry["report"]))
        return collected
    raise ValueError("no findings found: expected a finding, report, coordinated report or coordinator input")


def _normalise(text: str) -> str:
    return " ".join(text.split())


def _read(root: Path, path: str, revision: object) -> tuple[str | None, str]:
    """Return (text, reason). text is None when the file cannot be checked or found."""
    if "://" in path or path.startswith("mailto:"):
        return None, "not-checkable:remote source"
    relative = PurePosixPath(path.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts or not relative.parts or path.startswith("-"):
        return None, "not-checkable:path outside the root"
    if revision not in (None, ""):
        revision = str(revision)
        if not COMMIT.match(revision):
            return None, "not-checkable:revision is not a commit ID"
        present = subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"], cwd=root,
                                 capture_output=True, check=False)
        if present.returncode != 0:
            return None, "not-checkable:revision not available here"
        shown = subprocess.run(["git", "show", f"{revision}:{relative.as_posix()}"], cwd=root,
                               capture_output=True, check=False)
        if shown.returncode != 0:
            return None, "file-not-found:not present at that revision"
        data = shown.stdout
    else:
        current = root
        for name in relative.parts:
            current = current / name
            if current.is_symlink():
                return None, "not-checkable:symlink in path"
        if not current.is_file():
            return None, "file-not-found:not in the working tree"
        data = current.read_bytes()
    try:
        return data.decode("utf-8"), "ok"
    except UnicodeDecodeError:
        return None, "not-checkable:not UTF-8 text"


def _check_one(root: Path, finding_id: str, where: str, path: object, revision: object,
               span: object) -> dict:
    result = {"finding": finding_id, "where": where, "path": path, "revision": revision, "span": span}
    if not isinstance(path, str) or not isinstance(span, str) or not span:
        result.update(status="not-checkable", reason="no path or span")
        return result
    text, reason = _read(root, path, revision)
    if text is None:
        status, _, detail = reason.partition(":")
        result.update(status=status, reason=detail)
        return result
    if span in text:
        result.update(status="found", reason="exact match")
    elif _normalise(span) and _normalise(span) in _normalise(text):
        result.update(status="found-normalized", reason="matches only after collapsing whitespace")
    elif LOCATION.match(span):
        result.update(status="not-checkable", reason="span gives a location, not a quote")
    else:
        result.update(status="missing", reason="quoted text not in the file")
    return result


def check(document: object, root: Path) -> list[dict]:
    results = []
    for finding in findings_in(document):
        fid = str(finding.get("id", "?"))
        artifact = finding.get("artifact") or {}
        results.append(_check_one(root, fid, "artifact", artifact.get("path"),
                                  artifact.get("revision"), artifact.get("span")))
        for index, basis in enumerate(finding.get("basis") or []):
            if isinstance(basis, dict) and "span" in basis:
                results.append(_check_one(root, fid, f"basis[{index}]", basis.get("source"),
                                          basis.get("revision"), basis.get("span")))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository the artifact paths are relative to (default: current directory)")
    parser.add_argument("--strict", action="store_true", help="treat found-normalized as a failure")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args()
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        results = check(document, args.root.resolve())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"DIA-005 quote check refused: {error}", file=sys.stderr)
        return 2
    failing = FAILURES | ({"found-normalized"} if args.strict else set())
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"{r['status']:<17} {r['finding']} {r['where']}: {r['path']} — {r['reason']}")
        counts = {}
        for r in results:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print("Summary:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "no spans")
    return 1 if any(r["status"] in failing for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
