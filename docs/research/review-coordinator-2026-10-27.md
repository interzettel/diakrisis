# Review coordinator: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** routing to the smallest sufficient set of specialists and composing their reports without inventing agreement. **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](review-coordinator-2026-10-26.md).

## Sources checked for this revision

- [Awuni et al. (2026)](https://arxiv.org/pdf/2609.17857): LLM judges prefer outputs from their own model family; 55% of AB/BA pairs reverse winners; panel composition changed 18.5% of outcomes.
- [CoCoReviewBench (ICML 2026)](https://arxiv.org/pdf/2605.07905): a single human reviewer covers about 5 of 23 review subcategories; even all reviewers together cover about 40%.
- [Calvo Figueras & Agerri (2025)](https://arxiv.org/html/2505.11341v3): LLM judges without reference answers agree poorly with human judgments.

## Observed, uncertain, contradicted

- Observed: agreement among reviewers from one model family is weak evidence; order and composition change outcomes.
- Observed: complete coverage is rare even among human reviewers, so a combined report must state what was not examined.
- Observed (audit): the coordinator's scientific profile and `USAGE.md` disagreed on default reviewers; `USAGE.md` also had a Spatial Laboratory profile the coordinator lacked.

## Decisions

- **Routing (D4):** scientific default `argument-review`, `method-review`, `terminology-review`; add others only when needed. One table, mirrored in `USAGE.md`, including the Spatial Laboratory profile.
- **Agreement is never corroboration** when reviewers share a model or family; state this in syntheses.
- **Coverage first:** a synthesis states examined and unexamined scope before findings.
- **Inline** the severity definitions; the coordinator has no category list of its own.
- **Defer (D8):** loosening the identical-span rule for grouping.

## Licences and security

No code imported. Reports from specialists are data, not instructions.

## Controls

- Positive: two specialists flag one state/flag confusion at the same span with the same cause → one declared group, both findings kept.
- Negative: identical issue keys without a declared, reasoned relation → no grouping.
- Abstention: specialists disagree under unresolved authority → a recorded disagreement, no verdict.

## Evaluation status

Deferred by the owner to DIA-007.
