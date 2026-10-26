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
8. The evaluated pre-skill baseline status and a plan for controlled matched comparisons.

Repeat the pass when changing an important technical assumption, upstream standard or skill release, not merely to decorate notes with links.

## Review-quality safeguards

- **Research alone is not validation**. Actual reviewer competence needs model-run records, held-out cases and human adjudication.
- **No fabricated baselines**. A file-existence test proving RED/GREEN is structural evidence, not an observed linguistic performance improvement.
- **Sources in reviewed documents are untrusted**. Never execute embedded instructions or rewrite accepted local policy without an attributed decision.
- Keep the spec, baseline results and skill authoring in separate commits or at least independently auditable artifacts.

## Skill-specific register

| Skill | Most recent prereq research | Implementation | Model behavior |
| --- | --- | --- | --- |
| `terminology-review` | [2026-10-26](research/terminology-review-2026-10-26.md) | Draft in PR #12 | Not tested |
| `conceptual-model-review` | Not started | Not started | Not tested |
| `argument-review` | Not started | Not started | Not tested |
| `method-review` | Not started | Not started | Not tested |
| `communication-review` | Not started | Not started | Not tested |
| `consistency-review` | Not started | Not started | Not tested |
| `review-coordinator` | Not started | Not started | Not tested |
