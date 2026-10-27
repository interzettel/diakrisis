# DIA-008 — Deterministic review composition

**Issue:** [DIA-008 / #8](https://github.com/interzettel/diakrisis/issues/8) · **Milestone:** DIA-M3 · **Status:** implementation under owner-directed build-first exception; DIA-007 empirical testing/acceptance is deferred. **Single suite version:** `0.1.0-dev.0` (unreleased).

A read-only offline companion to [DIA-005 finding and review schemas](REVIEW-CONTRACT.md). The coordinator routes the smallest relevant set of reviewers. **It is not a specialist, model runner or adjudicating judge.** A combined report retains every specialist finding, its producer, exact local passage and cited sources.

## Input and output

Run from a checked-out Diakrisis repository with the CI-pinned `jsonschema==4.23.0` dependency:

```bash
python tools/coordinate_reviews.py --input evals/coordinator/example.json --output /tmp/dia-coordinated.json
```

The output must **not exist**. Nothing is fetched, no reviewed documents are changed, no background agents or model calls are launched. Input JSON:

```json
{
  "schema_version": 2,
  "coordination_id": "user-provided-review-id",
  "inputs": [
    {"input_id": "specialist-run-1", "report": {"...": "one complete validated DIA-005 review-report"}}
  ],
  "relations": [
    {
      "left": "F-001", "right": "F-002",
      "kind": "shared-cause",
      "reason": "Exact inspected passage has one common state/flag misconception",
      "authority_source": "docs/contract.md @ source revision"
    }
  ]
}
```

Every input report must follow [review-report.schema.json](../schemas/review-report.schema.json), and each embedded finding must follow [finding.schema.json](../schemas/finding.schema.json). Specialist reports must have unique `review_id` and globally unique finding `id`, and the `coordination_id` must differ from every input `review_id` (it becomes the combined report's own ID). A coordinator **cannot invent, silently repair or reclassify missing findings** to make malformed input pass.

The additive [coordinated-report.schema.json](../schemas/coordinated-report.schema.json) wraps the existing, unchanged `report` format with `sources` (origin review IDs and deterministic SHA-256 of each submitted report's canonical JSON), `groups`, `disagreements` and an explicit relationship policy. **This does not change the existing finding/review wire revision** or give any reviewer a separate version.

## Deduplication and disagreement policy

**Grouping is an annotation, never deletion.** Group membership requires an explicit, reasoned `shared-cause` relation between two findings; the code rejects mismatched `issue_key`, different artifact path/revision/span, different dispositions, repeated or self-referential pairs, abstentions and single-reviewer self-corroboration. Each source author must establish that the underlying cause truly matches. Related words or a shared issue key **alone never cause a merge**.

For three or more findings, **every pair** must be explicitly related to form a single grouping. The coordinator rejects incomplete chains; it never assumes transitivity from A–B and B–C to A–C. Group metadata includes declared reasons; every original specialist record stays in the output, without summed severity, pseudo-confidence or a consensus vote.

A `disagreement` relation is explicit, cites an authority/source and requires the same document path and revision. It does **not** resolve the difference: conflicting positions, uncertainty and abstentions remain visible; only an authorized owner can decide governing meaning or amendments.

A relation's `reason` and `authority_source` are **declarations supplied by the operator**, not independently fact-checked by this algorithm. The validation proves input consistency, not a genuine semantic relationship or scientific validity. Unrelated findings remain separate.

## Coverage, provenance and honest negatives

The combined `report` is valid against DIA-005's original schema. It unions exact examined source/scope/revision entries, unions excluded scopes and source-provided limitations, and adds an explicit synthesis limitation. Source report statuses and canonical digests are recorded even when a report contributes no findings. Submitted sources can remain uninspected/unknown; the coordinator does not pretend otherwise.

- At least one non-abstention finding → `issues-identified`.
- Only abstentions or missing authority → `insufficient-evidence`.
- Zero findings **and** every included source reports `no-issues-detected` **and every included source lists at least one explicit examined scope** → `no-issues-detected`, *not* certification. A source that claims no issues but examined nothing makes the whole result `insufficient-evidence`; it cannot borrow another source's coverage.
- Zero findings without that coverage → `insufficient-evidence`.

This is **deterministic composition/structural evaluation**, not paired human-rated LLM behavior, independent reviewers, secure private-data handling, genuine external-source verification, or owner acceptance. The deferred DIA-007 evaluation and DIA-M3 gate remain outstanding.

## Safety and boundary

The CLI reads one explicitly authorized local JSON file and creates one new local output file. It refuses an input that is a symlink and any output path that already exists, including a dangling symlink, and creates the output with an exclusive open so it never writes through a link; no network access, automatic repairs, publishing, execution of text from reviewed artifacts, API credentials, global installs or repository mutation is performed. As with other Diakrisis tools, **do not feed confidential manuscripts or unapproved personal records** into public CI fixtures. Use synthetic examples only in this repository.

The companion test cases in [tests/test_coordinator_composition.py](../tests/test_coordinator_composition.py) test structural outcomes, source preservation, disagreement and non-transitivity refusal. Tests cannot attest reviewer epistemic reliability.

## Research grounding

This design implements the bounded decisions in [the review coordinator's dated research gate](research/review-coordinator-2026-10-26.md), [DIA-005 authority examples](research/DIA-005-AUTHORITY.md), [W3C PROV-O](https://www.w3.org/TR/prov-o/), and [JSON Schema 2020-12](https://json-schema.org/specification). Provenance **does not confer truth**, and valid schema constraints do not establish source authority.
