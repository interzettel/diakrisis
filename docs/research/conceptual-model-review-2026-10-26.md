# Conceptual model review: source review before implementation

**Observed:** 2026-10-26. **Scope:** Ontology, taxonomy and conceptual type consistency. **Gate:** pre-implementation design only; model testing explicitly deferred by owner. **Source policy:** inspect linked primary materials where public; do not claim access to paid standards or validation from cited material.

## Checked external sources

- [W3C OWL 2 Primer](https://www.w3.org/TR/owl-primer/): distinguishes classes, individuals, properties and formally interpreted relations. This is **ontology modeling**, not an oracle for domain truth.
- [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/): validates RDF data graphs against declared shapes and emits reports; normative 2017 recommendation. [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) was a **working draft on 25 October 2026**, not a replacement Recommendation.
- [W3C SKOS](https://www.w3.org/TR/skos-reference/): concept schemes and labels are different from formal subclass axiom entailments.

## Comparison with repo research and donors

[Diakrisis Foundation](../FOUNDATION.md) separates types, instances, states, events, relations and measurements. [terminology-review](../../.agents/skills/terminology-review/SKILL.md) handles designation/definition drift; this skill instead checks *modeled kinds and dependencies*. Native domain schemas, OWL/SHACL validators are preferred for deterministic checks when the project actually provides machine-readable ontology/constraints. **No RDF mandatory:** Markdown conceptual models and bounded diagrams are valid inputs. No upstream code imported; licensing/security import review deferred.

## Decisions

- Review existing authoritative domain model before hypothesizing types. **No universal ontology**; a review-event could legitimately be treated differently in different bounded models.
- Separate subtype (is-a), part-whole, instance-of, state-of, transition, produces, depends-on and measures relations; do not interpret temporal state as subtype without rule.
- OWL may use open-world reasoning; missing triples don't prove negation. SHACL violation requires actual shapes + graph and a real validator; do not hallucinate formal output.
- Flag contradictory cardinalities/disjointness only when constraints are explicit. Reconcile conflicts and record uncertainty.

## Challenge cases and handoff

Positive: `Waiting for review` asserted subtype of review activity when the accepted model defines it as task state. Negative: a correctly defined `ReviewEvent` has its own class. Unknown: unfamiliar but internally consistent ontology with no external governing semantics → suggest/abstain, never impose common taxonomy. Hand off term spelling to terminology, unsupported causal claims to argument, empirical operationalization to method. **No baseline/model run was executed.**
