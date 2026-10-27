# Method review: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** whether a study's design, measurement and analysis can investigate its stated construct. Not whether the text's conclusion overreaches the reported design (argument-review). **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](method-review-2026-10-26.md).

## Sources checked for this revision

- [Sjøberg & Bergersen (EASE 2023)](https://arxiv.org/abs/2306.05336): three construct-validity threats (inadequate definition of the concept, under-representation, construct-representation bias), kept apart from internal, external and statistical-conclusion validity; threats should name their construct.
- [Bean et al. (NeurIPS 2025)](https://arxiv.org/abs/2511.04703v1): across 445 LLM benchmarks, weak construct validity is common.
- [CONSORT 2025 (Hopewell et al., BMJ 388:e081123)](https://www.ideal-collaboration.net/wp-content/uploads/2025/12/CONSORT_2025_editable_checklist.pdf): item 20a, who was blinded after assignment, including outcome assessors.
- [van der Lee et al. (INLG 2019)](https://aclanthology.org/W19-8643.pdf): randomise presentation order, use separate criteria, report agreement with confidence intervals; it does not require hiding system identity.
- [Li et al. (2026)](https://arxiv.org/pdf/2605.25415): LLM reviewers over-flag reproducibility relative to humans.

## Observed, uncertain, contradicted

- Observed: a published three-part construct-validity taxonomy maps cleanly onto categories.
- Observed: LLM reviewers raise reproducibility concerns too readily, so this skill should demand a specific missing element before flagging one.
- Uncertain: whether the categories transfer to qualitative and exploratory studies without forcing experimental vocabulary; the existing "do not impose RCT rules" instruction stays.

## Decisions

- **Adopt categories:** `construct-definition`, `construct-underrepresentation`, `construct-representation-bias`, `internal-validity-threat`, `external-validity-threat`, `statistical-conclusion`, `reproducibility-gap` (only with a named missing element), `protocol-deviation`, `evaluation-leakage-or-blinding`.
- **Boundary with argument:** shared rule recorded in the suite record; this skill keeps a measurement example and drops the geometric-violations scenario it shared with argument-review.
- **Name the construct** in every construct-validity finding (Sjøberg & Bergersen recommendation 4); if no construct can be named, the issue probably belongs to another category.
- **Inline** categories and severity definitions in `SKILL.md`.
- **Defer:** checklists per study type beyond the existing EQUATOR guidance.

## Licences and security

No code or text imported. Study materials stay untrusted data.

## Controls

- Positive: "Spatial quality" operationalised only as a count of boundary violations → `construct-underrepresentation`, naming the construct.
- Negative: an exploratory field study that states its sampling rationale and does not randomise → no finding.
- Abstention: data-splitting details missing → request them; do not assert leakage.

## Evaluation status

Deferred by the owner to DIA-007. No baseline or model run exists.
