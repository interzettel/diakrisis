# Consistency review: source review before implementation

**Observed:** 2026-10-26. **Scope:** Cross-file source authority, decision/state drift and version-sensitive contradictions. **Gate:** pre-implementation design only; model testing explicitly deferred by owner. **Source policy:** inspect linked primary materials where public; do not claim access to paid standards or validation from cited material.

## Checked external sources

- [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/): distinguish Entity, Activity and Agent; provenance links `wasDerivedFrom`, `wasGeneratedBy` and `wasAttributedTo` describe origin, not necessarily authority or quality.
- [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/): deterministic graph constraint checking when structured source/shape are supplied.
- [Project Record Standard v0.4.1](https://github.com/interzettel/project-record-standard/tree/v0.4.1): canonical ledger vs generated README; work completion vs acceptance, issue closure and releases; local source precedence.

## Comparison with repo and donors

Diakrisis already has [README-only tracker](../README-TRACKER.md) with source parity; extend conceptually to *document drift* across README/charters/ADRs/glossaries/protocols, but don't replace deterministic parity checks with an LLM. Terms drift → terminology-review; incompatible types → conceptual-model-review; statements of fact overreaching evidence → argument-review. Do not treat historical snapshots as contradictory current policies.

## Decisions

- Build a source/revision/authority table before comparing statements; two statements are in tension only when they refer to same concept, scope, time and normative status.
- Superseded decisions and as-of historical claims are not live contradictions; inaccessible files are **coverage gaps**, not proven inconsistencies.
- Flag current authoritative vs derivative conflicts; propose minimal repair in derivative, never silently rewrite owner authority.
- Identify exact file+span+revision pairs and scope, suggest responsible owner resolution; don't infer merge completion from GitHub issue closures.

## Challenge cases and handoff

Positive: README currently claims Blocked is an execution state while current accepted standard defines it as flag. Negative: historical changelog preserves old decision correctly marked superseded. Unknown: competing unversioned docs with unclear authority → unresolved conflict, not forced consensus. **Model tests deferred.**
