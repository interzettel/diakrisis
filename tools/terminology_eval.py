#!/usr/bin/env python3
"""Paired local Ollama terminology evaluations: baseline vs explicit skill instructions.

Never contacts a hosted model: only loopback Ollama is accepted. This tests an
instruction intervention, NOT automatic Agent Skills discovery. Test-case gold
labels are never sent to the model. Writes raw data for human adjudication.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "terminology-review" / "cases.json"
SKILL = ROOT / ".agents" / "skills" / "terminology-review" / "SKILL.md"
BASELINE_SYSTEM = ("You are a careful writing reviewer. Do not invent source "
                   "authority or modify text. Identify terminology problems "
                   "and uncertainties from the supplied context.")
USER_TEMPLATE = (
    "Review the passage for terminology, concept naming and definition "
    "consistency in the supplied domain. Cite applicable text and evidence; "
    "avoid false-positive criticism of legitimate alternate or quoted terms. "
    "Do not change the original.\n\nCONTEXT:\n{context}\n\nPASSAGE:\n{text}"
)


def local_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return (parsed.scheme == "http" and parsed.hostname in ("127.0.0.1", "localhost", "::1")
            and parsed.username is None and parsed.password is None
            and parsed.path == "/api/chat" and not parsed.query and not parsed.fragment)


def load_cases() -> list[dict]:
    payload = json.loads(CASES.read_text(encoding="utf-8"))
    cases = payload["cases"]
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case ID")
    for c in cases:
        if not all(c.get(k) for k in ("id", "kind", "context", "text", "expected")):
            raise ValueError(f"missing case detail: {c.get('id')}")
    return cases


def plan(cases: list[dict], seed: int) -> list[tuple[str, str]]:
    """Randomize paired run order with reproducible seed, not answer labels."""
    tasks = [(c["id"], arm) for c in cases for arm in ("baseline", "with_skill")]
    random.Random(seed).shuffle(tasks)
    return tasks


def generate(url: str, model: str, system: str, user: str, timeout: int) -> str:
    data = json.dumps({
        "model": model, "stream": False, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ], "options": {"temperature": 0}
    }).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        record = json.loads(response.read().decode("utf-8"))
    if not isinstance(record.get("message", {}).get("content"), str):
        raise ValueError("local Ollama response has no text message")
    return record["message"]["content"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Print plan without contacting any model")
    p.add_argument("--execute", action="store_true", help="Run paired trials against LOCAL Ollama only")
    p.add_argument("--model", help="Installed local Ollama model identifier")
    p.add_argument("--url", default="http://127.0.0.1:11434/api/chat")
    p.add_argument("--seed", type=int, default=1042)
    p.add_argument("--timeout", type=int, default=180, help="Per request timeout in seconds")
    p.add_argument("--output", type=Path, help="New JSON results file; never overwrite")
    args = p.parse_args()
    if args.execute == args.dry_run:
        p.error("Select exactly one of --dry-run or --execute")
    if not local_url(args.url):
        p.error("Only loopback Ollama /api/chat is allowed (no hosted inference)")
    cases = load_cases()
    tasks = plan(cases, args.seed)
    if args.dry_run:
        print(json.dumps({"kind":"dry-run-no-model", "case_count":len(cases),
                          "arms":["baseline","with_skill"],"total_runs":len(tasks),
                          "tasks":tasks,"model":args.model or "not selected"}, indent=2))
        return 0
    if not args.model or not args.output:
        p.error("--execute requires --model and --output")
    out = args.output.resolve()
    if out.exists():
        p.error("output already exists; results must not be overwritten")
    if out.suffix.lower() != ".json":
        p.error("output path must end with .json")
    source = SKILL.read_bytes()
    instructions = source.decode("utf-8").split("---",2)[2]
    case_by_id = {c["id"]:c for c in cases}
    results = []
    start = datetime.now(timezone.utc).isoformat()
    for case_id, arm in tasks:
        case = case_by_id[case_id]
        system = BASELINE_SYSTEM if arm == "baseline" else BASELINE_SYSTEM + "\n\nAdditional skill procedure:\n" + instructions
        prompt = USER_TEMPLATE.format(context=case["context"], text=case["text"])
        try:
            answer = generate(args.url, args.model, system, prompt, args.timeout)
            result = {"status":"completed", "response":answer}
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            result = {"status":"error", "error":str(exc)}
        results.append({"caseId":case_id, "arm":arm, **result})
        print(f"{case_id} {arm}: {result['status']}", flush=True)
    payload = {
        "kind":"actual-local-instruction-intervention-not-skill-discovery",
        "model":args.model,"endpoint":"localhost Ollama (address omitted)","seed":args.seed,
        "skillSha256":hashlib.sha256(source).hexdigest(), "startedAt":start,
        "endedAt":datetime.now(timezone.utc).isoformat(),
        "caseIds":[c["id"] for c in cases],
        "results":results,"adjudication":"pending human independent review; no accuracy claim"
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n", encoding="utf-8")
    return 0 if all(r["status"]=="completed" for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())
