#!/usr/bin/env python3
"""DIA-007: pool, shuffle and blind paired review runs for adjudication.

Each run file is named <document>-<review>-<arm>.json and holds the common
evaluation shape (docs/EVALUATION.md):

  {"findings": [{"location", "span", "problem", "proposed_change", "importance"}],
   "coverage_note": "..."}

The config names the corpus (a git repository), its frozen revision and the
file behind each document key:

  {"root": "/path/to/corpus", "revision": "<40-hex>",
   "documents": {"P": "proposal.txt", "E1": "essay-01.md"}}

Output: pool.json (what graders see: no arm, no run, no rank), key.json (the
sealed arm key, with each finding's quote-check status) and the key's SHA-256
on stdout. Publish the hash before grading; open the key after.

python tools/blind_pool.py --runs DIR --config cells.json --out DIR [--seed N] [--cap 6]

Offline. No model calls. Run files are untrusted data and are only copied.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import secrets
import sys

FIELDS = ("location", "span", "problem", "proposed_change", "importance")
RUN_NAME = re.compile(r"^(?P<doc>[A-Za-z0-9]+)-(?P<review>[A-Za-z0-9]+)-(?P<arm>[A-Za-z0-9]+)$")
_SPEC = importlib.util.spec_from_file_location("diakrisis_check_spans", Path(__file__).with_name("check_spans.py"))
spans = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(spans)


def load_runs(runs: Path, documents: dict, cap: int) -> list[dict]:
    rows = []
    for path in sorted(runs.glob("*.json")):
        if path.name.endswith(".contract.json"):
            continue
        match = RUN_NAME.match(path.stem)
        if not match:
            raise ValueError(f"run file name is not <document>-<review>-<arm>.json: {path.name}")
        if match["doc"] not in documents:
            raise ValueError(f"run {path.name} names a document missing from the config")
        data = json.loads(path.read_text(encoding="utf-8"))
        findings = data.get("findings") if isinstance(data, dict) else None
        if not isinstance(findings, list):
            raise ValueError(f"run {path.name} has no findings list")
        for rank, item in enumerate(findings[:cap], 1):
            if not isinstance(item, dict):
                raise ValueError(f"run {path.name} finding {rank} is not an object")
            row = {k: str(item.get(k, "")) for k in FIELDS}
            row["importance"] = row["importance"].lower()
            row.update(doc=match["doc"], review=match["review"], arm=match["arm"], rank=rank)
            rows.append(row)
    return rows


def quote_check(rows: list[dict], config: dict) -> None:
    document = {"findings": [{"id": str(i), "basis": [],
                              "artifact": {"path": config["documents"][r["doc"]],
                                           "revision": config.get("revision"), "span": r["span"]}}
                             for i, r in enumerate(rows)]}
    for result in spans.check(document, Path(config["root"]).resolve()):
        rows[int(result["finding"])]["quote_check"] = result["status"]


def blind(rows: list[dict], documents: dict, seed: int) -> tuple[list[dict], dict]:
    rng = random.Random(seed)
    pool, key = [], {"seed": seed, "entries": {}}
    for doc in documents:
        items = [r for r in rows if r["doc"] == doc]
        rng.shuffle(items)
        for n, r in enumerate(items, 1):
            fid = f"{doc}-{n:02d}"
            pool.append({"id": fid, "document": documents[doc], "review": r["review"],
                         **{k: r[k] for k in FIELDS}})
            key["entries"][fid] = {"arm": r["arm"], "rank": r["rank"], "quote_check": r.get("quote_check")}
    return pool, key


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--seed", type=int, help="fixed shuffle seed (tests only; default is random and recorded in the key)")
    parser.add_argument("--cap", type=int, default=6, help="findings kept per run, in the run's own order")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        rows = load_runs(args.runs, config["documents"], args.cap)
        quote_check(rows, config)
        seed = args.seed if args.seed is not None else secrets.randbits(64)
        pool, key = blind(rows, config["documents"], seed)
        key["corpus_revision"] = config.get("revision")
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "pool.json").write_text(json.dumps(pool, indent=1, ensure_ascii=False), encoding="utf-8")
        sealed = json.dumps(key, indent=1, sort_keys=True).encode("utf-8")
        with open(args.out / "key.json", "xb") as handle:  # never overwrite a sealed key
            handle.write(sealed)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"DIA-007 blind pooling refused: {error}", file=sys.stderr)
        return 2
    print(f"findings: {len(pool)}  key sha256: {hashlib.sha256(sealed).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
