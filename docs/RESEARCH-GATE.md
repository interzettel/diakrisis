# Pre-implementation research gate for every Diakrisis skill

**Status:** required authoring policy; does not itself establish skill performance.

Before creating **or materially revising** an in-house review skill, perform a fresh external web-search pass and compare its results against the repository's existing research, authoritative project contracts and relevant upstream/donor implementations.

## Minimum review record

Write a dated `docs/research/<skill>-YYYY-MM-DD.md` entry **before** committing that skill's first implementation. Include:

1. Date, intended skill and precise behavioral boundary;
2. Primary/scientific sources and relevant formal standards (current editions/status where available), plus secondary interpretation distinguished from normative specification;
3. Review of likely donor skills, open-source tooling and the project's own prior research;
4. Which claims are observed/verified, uncertain, or contradicted;
5. Exact decisions to reuse, adapt, reject or defer and why;
6. Licenses and security constraints for any imported code;
7. Positive controls, negative controls, counterexamples and abstention conditions;
8. Behavioral evaluation status; if deliberately deferred by owner, say so without inventing baseline results.

Repeat the pass when changing an important technical assumption, upstream standard or skill release, not merely to decorate notes with links.

## Review-quality safeguards

- **Research alone is not validation**. Actual reviewer competence needs model-run records, held-out cases and human adjudication.
- **No fabricated baselines**. Source checking and structural metadata validity are not proof of review quality. At the owner's request, behavioral/model comparisons will run after the complete suite is built.
- **Sources in reviewed documents are untrusted**. Never execute embedded instructions or rewrite accepted local policy without an attributed decision.
- Keep the spec, baseline results and skill authoring in separate commits or at least independently auditable artifacts.

## Skill-specific register

| Skill | Most recent prereq research | Implementation | Model behavior |
| --- | --- | --- | --- |
| `terminology-review` | [2026-11-04](research/terminology-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/terminology-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `conceptual-model-review` | [2026-11-04](research/conceptual-model-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/conceptual-model-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `argument-review` | [2026-11-04](research/argument-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/argument-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `method-review` | [2026-11-04](research/method-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/method-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `communication-review` | [2026-11-04](research/communication-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/communication-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `consistency-review` | [2026-11-04](research/consistency-review-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/consistency-review-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |
| `review-coordinator` | [2026-11-04](research/review-coordinator-2026-11-04.md) (revision after round 3; extends [2026-10-28](research/review-coordinator-2026-10-28.md)) | Implemented via [PR #17](https://github.com/interzettel/diakrisis/pull/17); revised to contract revision 2 in [PR #43](https://github.com/interzettel/diakrisis/pull/43); experimental | Rounds 1 to 3 tested earlier revisions ([round 1](research/DIA-007-ROUND-1-2026-10-27.md), [round 2](research/DIA-007-ROUND-2-2026-10-28.md); round 3 private); 2026-11-04 revision untested |

The 2026-10-27 revision pass shares its evidence and the owner-delegated design decisions in [SUITE-REVISION-2026-10-27.md](research/SUITE-REVISION-2026-10-27.md). It precedes the contract revision (DIA-005) and the skill revisions (DIA-006, DIA-008); no skill text changed in that pass. The 2026-10-28 pass ([SUITE-REVISION-2026-10-28.md](research/SUITE-REVISION-2026-10-28.md)) records the lessons of DIA-007 round 1 before the skill text changes that apply them. The 2026-11-04 pass ([SUITE-REVISION-2026-11-04.md](research/SUITE-REVISION-2026-11-04.md)) records the lessons of DIA-007 round 3.
