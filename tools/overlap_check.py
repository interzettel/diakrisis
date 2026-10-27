#!/usr/bin/env python3
"""DIA-007: check that evaluation material is held out from the skills' own text.

Counts word n-grams (default 8) shared between each candidate file and the
reference set (by default every skill file and every evaluation fixture).
Zero shared n-grams supports "held out" for verbatim reuse only; it cannot
detect a reused scenario in new words, which is why fixtures also carry a
hand-checked exposure label (evals/README.md).

python tools/overlap_check.py FILE... [--n 8] [--reference GLOB ...] [--fail-on-overlap]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = (".agents/skills/**/*.md", "evals/**/*.json", "evals/**/*.md")


def shingles(text: str, n: int) -> set[str]:
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def reference_set(patterns, n: int) -> tuple[set[str], int]:
    shared, count = set(), 0
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file():
                shared |= shingles(path.read_text(encoding="utf-8"), n)
                count += 1
    return shared, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--reference", nargs="*", default=list(DEFAULT_REFERENCE))
    parser.add_argument("--fail-on-overlap", action="store_true")
    args = parser.parse_args()
    if args.n < 3:
        print("DIA-007 overlap check refused: --n below 3 matches ordinary phrases", file=sys.stderr)
        return 2
    reference, count = reference_set(args.reference, args.n)
    results = {}
    for path in args.files:
        try:
            candidate = shingles(path.read_text(encoding="utf-8"), args.n)
        except (OSError, UnicodeDecodeError) as error:
            print(f"DIA-007 overlap check refused: {path}: {error}", file=sys.stderr)
            return 2
        hits = sorted(candidate & reference)
        results[str(path)] = {"ngrams": len(candidate), "shared": len(hits), "examples": hits[:5]}
    print(json.dumps({"n": args.n, "reference_files": count, "results": results}, indent=1, ensure_ascii=False))
    return 1 if args.fail_on_overlap and any(r["shared"] for r in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
