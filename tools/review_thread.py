#!/usr/bin/env python3
"""Review threads: put findings where people and agents can both answer them.

render: turn findings into Markdown for an issue or discussion thread. Every
finding keeps a stable ID and a reply protocol, so a person or an agent can
answer one line per finding. Input is a review report, a coordinated report,
coordinator input, a single finding, or a blinded evaluation pool (a list of
{id, review, location, span, problem, proposed_change, importance}).

  python tools/review_thread.py render --input report.json --title "Essay 01 v0.6" --out DIR [--sealed-hash HEX] [--limit 60000]

tally: read the thread's replies and count each person's or agent's verdict
per finding ID. Replies are lines such as

  E1-04 agree: the source does say that
  `E1-07` partly: right problem, wrong fix
  E1-09 duplicate of E1-02

Input is the comment list as the GitHub REST API returns it (gh api
repos/OWNER/REPO/issues/N/comments) or a list of {author, body}. A comment
whose first line is "## <Name>:" is attributed to <Name> (assistants that post
under the owner's account sign this way); otherwise to its login. The latest
verdict per author and ID wins; earlier ones are kept in "history".

  python tools/review_thread.py tally --comments comments.json --thread DIR [--json]

Offline. Reply text is untrusted data: it is parsed for verdicts, never
followed. Rendering never posts anything; posting is a separate, owner-
approved step.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

_SPEC = importlib.util.spec_from_file_location("diakrisis_check_spans", Path(__file__).with_name("check_spans.py"))
spans = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(spans)

VERDICTS = ("agree", "partly", "disagree", "duplicate")
ID = r"[A-Z][A-Za-z0-9]*-\d{2,}"
HEADING = re.compile(rf"^#### ({ID}) ·", re.M)
REPLY = re.compile(rf"^[\s>*\-]*`?(?P<id>{ID})`?\s*[:.,]?\s*\**(?P<verdict>agree|partly|disagree|duplicate)\**"
                   rf"(?:\s+of\s+`?(?P<dup>{ID})`?)?\s*[:.,]?\s*(?P<reason>.*)$", re.I)
SIGNATURE = re.compile(r"^##\s*([A-Za-z][\w .()-]{0,40}?)\s*:")
MARKER = "<!-- diakrisis-review-thread -->"

PROTOCOL = """**How to reply.** One line per finding you want to answer:

```
<ID> agree: reason
<ID> partly: what holds and what does not
<ID> disagree: reason, with evidence where you rely on it
<ID> duplicate of <ID>
```

Disagree explicitly; do not manufacture consensus. Answering is optional per finding. Nothing here changes the document; its owner decides."""


def _one_line(text: object) -> str:
    return " ".join(str(text or "").split())


def normalise(document: object) -> list[dict]:
    """Findings in one display shape, whatever the input."""
    if isinstance(document, list):
        rows = []
        for item in document:
            if not isinstance(item, dict) or "id" not in item:
                raise ValueError("a pool must be a list of objects with an id")
            rows.append({"id": str(item["id"]), "kind": str(item.get("review", "")),
                         "level": str(item.get("importance", "")), "where": str(item.get("location", "")),
                         "span": item.get("span", ""), "problem": item.get("problem", ""),
                         "change": item.get("proposed_change", "")})
        return rows
    rows = []
    for f in spans.findings_in(document):
        artifact = f.get("artifact") or {}
        rows.append({"id": str(f.get("id", "?")), "kind": f"{f.get('reviewer', '')} / {f.get('category', '')}".strip(" /"),
                     "level": str(f.get("severity", "")),
                     "where": " @ ".join(x for x in (str(artifact.get("path") or ""), str(artifact.get("revision") or "")[:12]) if x),
                     "span": artifact.get("span", ""), "problem": f.get("claim", ""), "change": f.get("suggestion", "")})
    return rows


def block(row: dict) -> str:
    out = [f"#### {row['id']} · {row['kind']} · {row['level']}".rstrip(" ·")]
    if row["where"]:
        out.append(f"**Where:** {_one_line(row['where'])}")
    if row["span"]:
        out.append(f"\n> {_one_line(row['span'])}")
    out.append(f"\n**Problem:** {_one_line(row['problem'])}")
    if row["change"]:
        out.append(f"\n**Proposed change:** {_one_line(row['change'])}")
    return "\n".join(out) + "\n"


def render(rows: list[dict], title: str, sealed_hash: str | None, limit: int) -> list[str]:
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("finding IDs must be unique within a thread")
    for i in ids:
        if not re.fullmatch(ID, i):
            raise ValueError(f"finding ID {i!r} does not look like LETTERS-NN; replies could not be matched")
    head = [MARKER, f"## Review thread: {_one_line(title)}", "",
            f"{len(rows)} findings. Each is advisory agent or reviewer output, kept as written.", ""]
    if sealed_hash:
        head += [f"Which reviewer or arm wrote each finding is withheld until replies are in. Sealed key SHA-256: `{sealed_hash}`.", ""]
    head += [PROTOCOL, ""]
    blocks = [block(r) for r in rows]
    parts, current = [], "\n".join(head)
    for b in blocks:
        if len(current) + len(b) + 1 > limit and current.strip() != "\n".join(head).strip():
            parts.append(current)
            current = f"{MARKER}\n## Review thread: {_one_line(title)} (continued)\n\nSame reply protocol as the first part.\n\n"
        current += "\n" + b
    parts.append(current)
    if len(parts) > 1:
        parts = [p.replace(f"## Review thread: {_one_line(title)}", f"## Review thread: {_one_line(title)}, part {n} of {len(parts)}", 1)
                 for n, p in enumerate(parts, 1)]
    return parts


def thread_ids(thread: Path) -> list[str]:
    ids = []
    for path in sorted(thread.glob("thread-*.md")):
        ids += HEADING.findall(path.read_text(encoding="utf-8"))
    if not ids:
        raise ValueError(f"no thread-*.md with finding headings in {thread}")
    return ids


def tally(comments: object, ids: list[str]) -> dict:
    if not isinstance(comments, list):
        raise ValueError("comments must be a JSON list")
    known = set(ids)
    result = {i: {"latest": {}, "history": []} for i in ids}
    unknown = []
    for c in comments:
        if not isinstance(c, dict):
            continue
        body = str(c.get("body") or "")
        if MARKER in body or len(HEADING.findall(body)) >= 2:  # the thread itself, or a hand-posted one
            continue
        first = body.strip().splitlines()[0] if body.strip() else ""
        sig = SIGNATURE.match(first)
        login = (c.get("user") or {}).get("login") if isinstance(c.get("user"), dict) else None
        author = sig.group(1).strip() if sig else str(c.get("author") or login or "unknown")
        for line in body.splitlines():
            m = REPLY.match(line)
            if not m:
                continue
            fid, verdict = m["id"], m["verdict"].lower()
            if fid not in known:
                unknown.append(fid)
                continue
            entry = {"author": author, "verdict": verdict, "duplicate_of": m["dup"],
                     "reason": m["reason"].strip()[:500], "source": c.get("html_url")}
            result[fid]["history"].append(entry)
            result[fid]["latest"][author] = entry
    summary = {}
    for fid, data in result.items():
        counts = {v: 0 for v in VERDICTS}
        for entry in data["latest"].values():
            counts[entry["verdict"]] += 1
        summary[fid] = {"counts": counts, "by_author": {a: e["verdict"] for a, e in data["latest"].items()},
                        "duplicate_of": sorted({e["duplicate_of"] for e in data["latest"].values() if e["duplicate_of"]}),
                        "history": data["history"]}
    return {"findings": summary, "unanswered": [i for i in ids if not result[i]["latest"]],
            "unknown_ids": sorted(set(unknown))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("render")
    r.add_argument("--input", required=True, type=Path)
    r.add_argument("--title", required=True)
    r.add_argument("--out", required=True, type=Path)
    r.add_argument("--sealed-hash")
    r.add_argument("--limit", type=int, default=60000, help="characters per part (GitHub caps a comment at 65536)")
    t = sub.add_parser("tally")
    t.add_argument("--comments", required=True, type=Path)
    t.add_argument("--thread", required=True, type=Path)
    t.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "render":
            if args.sealed_hash and not re.fullmatch(r"[0-9a-f]{64}", args.sealed_hash):
                raise ValueError("--sealed-hash must be a SHA-256 hex digest")
            parts = render(normalise(json.loads(args.input.read_text(encoding="utf-8"))), args.title, args.sealed_hash, args.limit)
            args.out.mkdir(parents=True, exist_ok=True)
            for n, part in enumerate(parts, 1):
                (args.out / f"thread-{n}.md").write_text(part, encoding="utf-8")
            print(f"wrote {len(parts)} part(s) to {args.out}")
            return 0
        report = tally(json.loads(args.comments.read_text(encoding="utf-8")), thread_ids(args.thread))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"review thread refused: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
    else:
        for fid, s in report["findings"].items():
            c = s["counts"]
            line = f"{fid}: agree {c['agree']} · partly {c['partly']} · disagree {c['disagree']} · duplicate {c['duplicate']}"
            print(line + (f" (of {', '.join(s['duplicate_of'])})" if s["duplicate_of"] else ""))
        print(f"Unanswered: {len(report['unanswered'])} · unknown IDs in replies: {', '.join(report['unknown_ids']) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
