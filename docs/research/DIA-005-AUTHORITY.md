# DIA-005 authority decision examples

**Date:** 2026-10-26 · **Purpose:** Bounded cross-specialist authority-resolution examples for [issue #5](https://github.com/interzettel/diakrisis/issues/5). **Status:** authored design controls, *not* observed model behavior or independent human adjudication.

| Case | Target passage | Governing evidence | Expected advisory treatment |
| --- | --- | --- | --- |
| A1 — Valid conflict | “Blocked is now a workflow state.” | Accepted PRS project policy at a known revision says blocked is an independent flag | `confirmed-conflict` only after checking target and exact governing rule at same scope; propose minimal terminology/model repair |
| A2 — Valid neologism | “A driftline encloses each region.” | Author explicitly defines *driftline* earlier and uses it consistently | No finding; unfamiliar vocabulary alone is not an issue |
| A3 — Equal-authority source collision | “Review means X” versus “Review means Y” in two live unversioned policies | Both authoritative status and supersession unknown | `needs-clarification` or `abstain`, with source coverage gap and owner precedence decision; no confirmed verdict |
| A4 — Inspected historical exception | 2025 archive says “Review is an execution state”; current project says Review is an activity | 2025 text is marked superseded; current contract is live | No active contradiction; retain historical record |
| A5 — Inaccessible source | A paper cites a closed publication as definitive proof of a specific use | Reviewer cannot inspect full claim | `abstain` with `evidence_status=unknown`; don't paraphrase inaccessible source |
| A6 — External obligations | Local wiki approves terms that conflict with a binding regulatory term for the covered document | Regulator's current applicability and source passage verified | Document binding scope and conflict; no absolute rule that all local usages lose priority |
| A7 — Two specialist views, one cause | Reviewer A says *Blocked* is misnamed, reviewer B says it's mistyped as a state | Same exact state/flag category error in same artifact | Coordinator links/merges underlying issue only after matching revision/cause; preserve both bases, no double progress |
| A8 — Two causes, one sentence | “Three trials prove it is universally safer.” | Logical overreach plus separate syntactic scope ambiguity | Keep independent argument and communication observations; sharing a span isn't sufficient to deduplicate |
| A9 — Valid empty review | Two explicitly scoped paragraphs reviewed, no detected issues | Both paragraphs accessible; chapter 3 unexamined | `no-issues-detected` with `findings=[]`, explicit `not_examined`; **not** acceptance or certification |
| A10 — Uncertain ontology | New domain defines “state” as a first-class entity | No contradictory adopted schema or external binding requirement | Suggest clarification or abstain; don't impose a universal ontology |

These rows are **human-authored case intentions**. Structured synthetic fixtures in [`evals/finding-contract/cases.json`](../../evals/finding-contract/cases.json) confirm only schema shape and conditional fields. Real LLM performance and false positives will be evaluated in the later owner-directed test phase.

## Source and limits

- [JSON Schema 2020-12](https://json-schema.org/specification): supported conditional constraints, not proof that source assertions are accurate.
- [W3C SKOS](https://www.w3.org/TR/skos-reference/): concept, lexical label and document scheme distinctions.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): provenance of entity/activity/agent, not epistemic authority.
- [Project Record Standard v0.4.1](https://github.com/interzettel/project-record-standard/tree/v0.4.1): status vs blocked flag, scope and acceptance boundaries.
- [Diakrisis foundation](../FOUNDATION.md) and [review contract](../REVIEW-CONTRACT.md): owner authority and minimally invasive correction.

External sources may evolve; the cited editions and their applicability must be checked for the actual future review artifact.
