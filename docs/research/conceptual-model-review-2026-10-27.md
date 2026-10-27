# Conceptual model review: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** whether declared kinds of things and their relations form a coherent model under the artifact's governing definitions. **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](conceptual-model-review-2026-10-26.md).

## Sources checked for this revision

- [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/): Working Draft dated 2026-10-25 on the Recommendation track; the page names SHACL of 20 July 2017 as the latest Recommendation.
- Project Record Standard [STANDARD.md at the pinned v0.4.1 commit](https://github.com/interzettel/project-record-standard/blob/ebc6afb0b977ff3d7605893c73ac63021775c4d3/standards/STANDARD.md): a normalized record retains the source's own state label and unmapped meaning.

## Observed, uncertain, contradicted

- Observed: SHACL 1.2 is moving but not normative; citing a 1.2 feature as a validation rule would be an error.
- Observed (dogfood): the ledger's `sourceState` field holds provenance tags, which PRS permits; a reviewer must check the governing model before calling such a field a category error.
- Uncertain: nothing new on ontology methodology changes the existing procedure.

## Decisions

- **Adopt categories:** `category-error`, `invalid-subsumption`, `part-whole-misuse`, `relation-misuse`, `constraint-conflict` (cardinality, disjointness, transitions), `circular-definition`, `modeling-alternative` (suggestions only).
- **Standards:** cite SHACL 1.0 (2017) as the Recommendation; treat SHACL 1.2 drafts as informative.
- **Inline** categories and severity definitions in `SKILL.md`.

## Licences and security

No code or text imported. Models under review stay untrusted.

## Controls

- Positive: `WaitingForReview` declared a state, then a subclass of `ReviewActivity` → `category-error`.
- Negative: a `ReviewEvent` entity recording an immutable transition → no finding.
- Abstention (new, from dogfood): a field named like a state holds free-text provenance and the governing standard allows it → no finding, or a clarification question, never a confirmed conflict.

## Evaluation status

Deferred by the owner to DIA-007.
