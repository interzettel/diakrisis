# Shared review finding and authority contract

**Issue:** [DIA-005 / #5](https://github.com/interzettel/diakrisis/issues/5) · **Milestone:** DIA-M1 · **Design status:** implemented **contract revision 1**, structural checks; empirical reviewer assessment deferred by owner.

The **whole Diakrisis suite** uses one package version (`0.1.0-dev.0`, unreleased). The integer `schema_version: 1` identifies the interchange **wire format**, *not* a release or an individual reviewer version.

- [Individual finding — JSON Schema draft 2020-12](../schemas/finding.schema.json)
- [Whole review / zero-findings envelope](../schemas/review-report.schema.json)
- [Accepted/rejected synthetic structural controls](../evals/finding-contract/cases.json)
- [DIA-005 authority decision cases](research/DIA-005-AUTHORITY.md)

## What the reviewer is allowed to assert

A **finding** is an advisory, bounded observation about an exact passage, not a final decision or source edit. Distinguish:

| Record property | Meaning | Not to be confused with |
| --- | --- | --- |
| `artifact.path`, `revision`, `span` | Exact inspected target and a quote/location anchor | Source authority; a filename alone is not verification |
| `basis[]` | Relevant inspected rule/source and why it applies, or an explicitly uninspected reference | A URL proving the cited claim is true |
| `evidence_status` | `observed`, `inferred`, `unknown` | Model confidence or strength of impact |
| `disposition` | `confirmed-conflict`, `needs-clarification`, `suggestion`, `abstain` | Accepted owner decision |
| `severity` | `informational`, `minor`, `major`, `blocking-candidate` | Project Record Standard **Blocked** flag, severity probability, formal release stop |
| `confidence_reason` | Plain-language provenance and limitation explanation | Pseudo-precise probability |
| `requires_owner_decision` | Reviewer proposes a policy/meaning choice that needs authority | Permission to change files |
| `issue_key`, `related_findings` | Optional coordination hints with explained common cause | Proof that multiple model opinions are independent |

**Confirmed conflict** requires the passage, an *actually inspected* source span, a reason and an **applicable** authority/rule under the same subject, time and scope. The schema enforces `evidence_status=observed` and at least one inspected/applicable cited basis, but **cannot prove the quote is genuine or the asserted authority applies**. The reviewer and owner must verify that judgment.

**Abstain** requires `evidence_status=unknown`, `severity=informational`, and no proposed rewrite. A source-gap is not a defect, and a missing passage must never be filled with invented text. A nonconfirmed suggestion may have `basis=[]` if only the reviewed passage is available; `confidence_reason` then explains the limitation. `needs-clarification` can describe contradictory or insufficiently ranked authority.

**No issues detected** is represented as a `review-report` with `status=no-issues-detected` and `findings=[]`. It is an observed outcome for the **explicit covered scope**, never a scientific-validity certification. If there is insufficient authority to examine the targeted question, use `insufficient-evidence` and, where useful, an explicit abstention finding. Coverage distinguishes `examined` from `not_examined`.

## Authority-resolution procedure

1. **Identify the actual claim's domain and scope** (project, document, term, time/version, locale, legal or academic domain). Never compare matching keywords from different referents.
2. **Inventory sources before ranking:** author-defined glossary, signed/accepted project standards or ADRs, a study protocol/preregistration, domain standards and externally binding requirements, and nonbinding editor guidance. Record each source's revision, inspected passage, decision/approval state and applicability. A retrieved document is not automatically authoritative.
3. **Establish governing applicability:** binding law/contract or externally adopted rule can supersede an informal local convention *in its scope*; accepted local definitions govern only within their legitimate domain; quoted historical usages and superseded policies do not automatically conflict with current ones. **There is no universal local-first or newest-wins precedence.**
4. **Compare actual concepts and claims:** designation ≠ concept ≠ referent. Review activity ≠ event ≠ state; measurement proxy ≠ broad construct. A local model can intentionally define a different ontology without being globally wrong.
5. **Classify the evidence:** actual inspected, same-scope contradiction with applicable authority → `confirmed-conflict`; plausible conflicting interpretations or unclear precedence → `needs-clarification`; a beneficial but not compulsory change → `suggestion`; unresolved truth/applicability/coverage → `abstain`.
6. **Preserve meaningful uncertainty:** equal-authority conflict without a tie-breaker is reported to the owner; don't guess by majority or fabricate a consensus. A reviewer can present multiple defensible options.
7. **Keep authority and action distinct:** the reviewer may recommend a text change. Only the designated author/project owner or explicitly authorized downstream action can accept, rewrite, merge, change policy, or publish.

### Examples of boundary decisions

| Situation | Correct stance |
| --- | --- |
| Accepted PRS rule says `Blocked` is a flag; draft calls it an execution state with the same scoped workflow | Potential **confirmed conflict** if actual passages and revisions are checked; no automatic project-state edit |
| Author uses a clearly introduced new term consistently in an essay | **No terminology finding** merely for unconventional wording |
| Two unversioned glossaries have different definitions with no accepted precedence | **Needs clarification / abstain**; identify source gap without forced correction |
| W3C SKOS refers to preferred lexical labels but a paper asserts a label is necessarily an ontological class | Check intended model; terminology and conceptual review may each contribute evidence, but **do not double-count the underlying mismatch** |
| Study reports fewer geometric violations and concludes “better architecture” | **Argument or method scope**, depending on whether the problem is inference or construct operationalization. Do not misfile as a grammar error |
| Historical changelog says `Review` was a state in an older system, marked superseded | **No current contradiction** unless old meaning is incorrectly applied to live policy |

## Coordinator aggregation

The `review-coordinator` is a *router and reconciler*, not a specialist that creates independent findings or an approval authority. It must not appear as `reviewer` on a specialist finding.

- Pick the smallest relevant skill set; record which skills **actually ran**, not just which would be appropriate.
- For a single underlying defect, attach related specialist observations using `issue_key`/`related_findings` only **after checking same artifact meaning, cause, scope, revision and basis**. A string key alone cannot prove equivalence.
- Keep separate entries when one passage has two independent causes (for example empirical warrant and syntactic ambiguity). Record disagreement rather than collapsing it to a majority verdict.
- No new score or severity is derived from finding count. No invented reviewer independence, model calibration, or corroboration.
- A consolidated report includes `coverage.examined`, `coverage.not_examined`, `limitations` and `status`. All findings retain their producing specialist, revision and evidence.
- The report's schema requires every included finding to satisfy the individual finding contract. It does **not** decide semantic deduplication, globally unique review IDs or trustworthiness of source assertions.

## Portable validation (contract only)

The repository runs `tests/test_finding_contract.py` under Python with **`jsonschema==4.23.0`** in CI. That uses JSON Schema Draft202012Validator plus an **offline registry** to resolve the two checked local schemas without network access, and checks synthetic accepted/rejected examples. This is not model testing, not a scientific validity evaluation, and not a user acceptance event.

When a client cannot honestly supply a required artifact span or authority, produce a transparent **prose insufficient-evidence review** rather than fabricating a schema-conforming record. The 7 portable Agent Skills are still experimental and unreleased. Their behavioral model evaluation, real-user document tests and native Claude/Codex activation remain in the later owner-directed verification stage.

## Sources and schema constraints

- [JSON Schema specification (2020-12)](https://json-schema.org/specification) and [Core conditional applicators](https://json-schema.org/draft/2020-12/json-schema-core)
- [W3C SKOS Recommendation](https://www.w3.org/TR/skos-reference/) for concepts versus lexical labels
- [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/) for provenance entities/activities/agents; provenance **does not** imply authority or truth
- [Diakrisis foundation](FOUNDATION.md) and [authoritative Project Record Standard](https://github.com/interzettel/project-record-standard/blob/v0.4.1/standards/STANDARD.md).

**No substantive source material was copied from external specifications.** This contract describes a project-specific decision model; its ontology and empirical suitability remain open to final human assessment.

## DIA-008 implemented composition interface (2026-10-26)

The offline, read-only [coordinator procedure](COORDINATION.md) and [coordinated-report schema](../schemas/coordinated-report.schema.json) now implement additive source provenance, declared complete-link grouping, preserved specialist findings and unresolved disagreement reporting. A grouped finding is **never dropped or silently rewritten**. The preexisting DIA-005 finding and review-report schemas remain unchanged. Structural tests passed; semantic group judgments, actual model behavior and DIA-007 acceptance remain unverified.
