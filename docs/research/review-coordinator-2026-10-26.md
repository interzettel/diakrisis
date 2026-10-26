# Review coordinator: source review before implementation

**Observed:** 2026-10-26. **Scope:** Skill selection, cross-review synthesis and owner-aware handoffs. **Gate:** pre-implementation design only; model testing explicitly deferred by owner. **Source policy:** inspect linked primary materials where public; do not claim access to paid standards or validation from cited material.

## Checked external sources

- [Agent Skills format](https://agentskills.io/specification): each skill has concrete scope and trigger description; loading a collection does not automatically execute all its members.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): preserve provenance linking each finding to its agent activity and source document; provenance is not proof.
- [NIST AI RMF generative-AI profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence): generative confabulation and consequential misinterpretation require transparent limitations and human risk governance.
- [Nature (2026) evaluation incentives](https://www.nature.com/articles/s41586-026-10549-w): more model-generated answers or confident consensus do not establish reliability.

## Comparison with repo and donors

[Review contract](../REVIEW-CONTRACT.md) already specifies findings, basis, uncertainty and owner decision. Shared agents and work authority belong to Qurultai/Personal Agent Stack, not this skill. This coordinator should choose **which specialist review is relevant** and assemble findings, not plan autonomous multi-agent background loops, run commands on untrusted documents, modify other repositories or claim agent independence.

## Decisions

- Route request based on artifact and claim: term/definition → terminology, entities/relations → conceptual model, warrants/evidence → argument, study design → method, readability/pragmatics → communication, cross-artifact conflicts → consistency.
- Use smallest sufficient set; don't invoke all seven by default. Never treat two identical model opinions as independent corroboration.
- Standardize finding shape, deduplicate overlap by same underlying passage+claim+basis, preserve genuine disagreements and abstentions; no invented confidence arithmetic.
- Show coverage and unresolved sources; only user/authorized workflow decides acceptance, rewrite, merge or release. Coordinator is **not** an agent runtime or scheduling harness.

## Challenge cases and handoff

Positive: review project README and state contract, run terminology + consistency, avoid irrelevant methodology review. Negative: single proofread request routes only communication. Unknown: inaccessible shared policy causes abstention, not arbitrary majority vote. **No behavior baseline or activation check yet.**
