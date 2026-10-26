#!/usr/bin/env python3
"""DIA-008: deterministic, read-only composition of submitted specialist reports.

Inputs are untrusted data. No model invocation, fetching, AI judging, source edits,
automatic relation inference, majority voting, or source-authority decisions.

python tools/coordinate_reviews.py --input evals/coordinator/example.json --output /tmp/coordinated.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "schemas"


def canonical(item: object) -> bytes:
    return json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def validator(name: str) -> Draft202012Validator:
    schema_by_name = {}
    registry = Registry()
    for filename in ("finding.schema.json", "review-report.schema.json",
                     "coordinated-report.schema.json"):
        doc = json.loads((DIR / filename).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(doc)
        schema_by_name[filename] = doc
        registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))
    return Draft202012Validator(schema_by_name[name], registry=registry)


def validate(check: Draft202012Validator, obj: object, label: str) -> None:
    failures = sorted(check.iter_errors(obj), key=lambda e: (str(e.json_path), e.message))
    if failures:
        e = failures[0]
        raise ValueError(f"{label}: {e.json_path}: {e.message}")


def compose(payload: dict) -> dict:
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version", "coordination_id", "inputs", "relations"
    } or payload["schema_version"] != 1:
        raise ValueError("unsupported coordinator input format")
    coord_id = payload["coordination_id"]
    if not isinstance(coord_id, str) or not coord_id:
        raise ValueError("missing coordination ID")
    inputs = payload["inputs"]
    if not isinstance(inputs, list) or not inputs:
        raise ValueError("at least one submitted specialist review is required")
    relations = payload["relations"]
    if not isinstance(relations, list):
        raise ValueError("relations must be an array")

    report_schema = validator("review-report.schema.json")
    output_schema = validator("coordinated-report.schema.json")
    all_findings = {}
    source_reports = []
    examined = {}
    not_examined = set()
    limitations = {"This report is deterministic assembly of submitted reviewer claims, not a second independent review or approval."}
    source_ids = set()
    review_ids = set()
    statuses = []
    for incoming in inputs:
        if not isinstance(incoming, dict) or set(incoming) != {"input_id", "report"}:
            raise ValueError("each input must supply input_id and an unchanged report")
        source_id = incoming["input_id"]
        report = incoming["report"]
        if not isinstance(source_id, str) or not source_id or source_id in source_ids:
            raise ValueError("duplicate or missing input ID")
        source_ids.add(source_id)
        validate(report_schema, report, "input " + source_id)
        review_id = report["review_id"]
        if review_id in review_ids:
            raise ValueError("duplicate upstream review ID")
        review_ids.add(review_id)
        statuses.append(report["status"])
        source_reports.append({
            "input_id": source_id,
            "review_id": review_id,
            "review_status": report["status"],
            "sha256": hashlib.sha256(canonical(report)).hexdigest(),
        })
        for finding in report["findings"]:
            fid = finding["id"]
            if fid in all_findings:
                raise ValueError("finding IDs must be unique across submitted reviews: " + fid)
            all_findings[fid] = finding
        for item in report["coverage"]["examined"]:
            examined[canonical(item)] = item
        not_examined.update(report["coverage"]["not_examined"])
        limitations.update(f"{source_id}: {note}" for note in report["limitations"])

    pairs = set()
    groups_pairs = set()
    declared = []
    disagreements = []
    for relation in relations:
        if (not isinstance(relation, dict) or
                set(relation) != {"left", "right", "kind", "reason", "authority_source"}):
            raise ValueError("relation requires left/right/kind/reason/authority_source")
        left, right = relation["left"], relation["right"]
        if (not isinstance(left, str) or not isinstance(right, str) or
                left == right or left not in all_findings or right not in all_findings):
            raise ValueError("relation has missing, duplicate or unknown finding ID")
        pair = tuple(sorted((left, right)))
        if pair in pairs:
            raise ValueError("conflicting or repeated relation for same pair")
        pairs.add(pair)
        kind = relation["kind"]
        reason = relation["reason"]
        authority_source = relation["authority_source"]
        if kind not in ("shared-cause", "disagreement"):
            raise ValueError("unsupported relation kind")
        if not isinstance(reason, str) or len(reason.strip()) < 12:
            raise ValueError("explicit relationship needs a substantive reason")
        if not isinstance(authority_source, str) or not authority_source.strip():
            raise ValueError("relationship must name its declared authority/source")
        a, b = all_findings[left], all_findings[right]
        if kind == "shared-cause":
            if (not a.get("issue_key") or a["issue_key"] != b.get("issue_key") or
                    a["artifact"] != b["artifact"] or
                    a["reviewer"] == b["reviewer"] or
                    a["disposition"] != b["disposition"] or
                    a["disposition"] == "abstain"):
                raise ValueError("shared cause needs matching scoped issue, artifact, distinct reviewers and non-abstention disposition")
            groups_pairs.add(pair)
            declared.append((pair, reason))
        else:
            if (a["artifact"].get("path") != b["artifact"].get("path") or
                    a["artifact"].get("revision") != b["artifact"].get("revision")):
                raise ValueError("disagreement needs a shared artifact and revision")
            disagreements.append({
                "left": pair[0], "right": pair[1],
                "reason": reason, "authority_source": authority_source
            })

    # Explicit complete-link clusters only: transitivity cannot infer an
    # undeclared semantic equivalence from two separate pairs.
    linked = sorted(set(f for pair in groups_pairs for f in pair))
    adjacency = {fid: set() for fid in linked}
    for a, b in groups_pairs:
        adjacency[a].add(b)
        adjacency[b].add(a)
    groups = []
    while adjacency:
        first = min(adjacency)
        component = {first}
        frontier = [first]
        while frontier:
            node = frontier.pop()
            for neighbor in adjacency[node] - component:
                component.add(neighbor)
                frontier.append(neighbor)
        members = sorted(component)
        expected_pairs = {(members[i], members[j]) for i in range(len(members))
                          for j in range(i + 1, len(members))}
        if not expected_pairs.issubset(groups_pairs):
            raise ValueError("incomplete relation clique; no automatic transitive grouping")
        reasons = sorted({reason for pair, reason in declared if pair in expected_pairs})
        identifier = hashlib.sha256(canonical(members)).hexdigest()[:12]
        groups.append({"group_id": "G-" + identifier,
                       "finding_ids": members, "declared_reasons": reasons})
        for member in members:
            adjacency.pop(member)

    findings = [all_findings[x] for x in sorted(all_findings)]
    if not findings:
        status = ("no-issues-detected" if statuses and all(
            x == "no-issues-detected" for x in statuses) and examined
                  else "insufficient-evidence")
    elif all(x["disposition"] == "abstain" for x in findings):
        status = "insufficient-evidence"
    else:
        status = "issues-identified"
    result = {
        "schema_version": 1,
        "coordination_id": coord_id,
        "report": {
            "schema_version": 1,
            "review_id": coord_id,
            "status": status,
            "coverage": {
                "examined": [examined[k] for k in sorted(examined)],
                "not_examined": sorted(not_examined),
            },
            "findings": findings,
            "limitations": sorted(limitations),
        },
        "sources": sorted(source_reports, key=lambda r: r["input_id"]),
        "groups": sorted(groups, key=lambda g: g["group_id"]),
        "disagreements": sorted(disagreements, key=lambda d: (d["left"], d["right"])),
        "relationship_policy": "declared-links-only-not-independent-adjudication",
    }
    validate(output_schema, result, "coordinated report")
    # Preserve every submitted finding without rewriting or dropping any entry.
    assert {f["id"]: canonical(f) for f in result["report"]["findings"]} == {
        k: canonical(v) for k, v in all_findings.items()
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        src = args.input.resolve(strict=True)
        dest = args.output.resolve()
        if not src.is_file() or src.is_symlink() or dest == src or dest.exists():
            raise ValueError("input must be a real file; output must not exist or overwrite input")
        payload = json.loads(src.read_text(encoding="utf-8"))
        output = compose(payload)
        dest.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"DIA-008: {len(output['report']['findings'])} preserved findings, "
              f"{len(output['groups'])} declared groups; no source files modified")
        return 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"DIA-008 input refused: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
