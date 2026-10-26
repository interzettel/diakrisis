# Terminology-review pre-implementation literature and tool pass

**Date:** 2026-10-26  
**Scope:** terminology-review (first Diakrisis skill only).  
**Status:** source-grounded architecture decision; not a behavioral evaluation or certification.  
**Method:** web search, primary specification inspection and comparison with the already recorded Diakrisis foundations and consumer repository contracts.

## Sources independently checked

| Source | Finding relevant to the skill | Use and limit |
| --- | --- | --- |
| [ISO 704:2022](https://www.iso.org/standard/79077.html) (primary ISO page) | Terminology work explicitly relates objects, concepts, definitions and designations, with procedures for developing terminology. | Concept-first reviews; ISO abstract is public, full paid text not licensed or copied. Do not claim whole standard audited. |
| [ISO 1087:2019](https://www.iso.org/standard/62330.html) (primary ISO page; confirmed 2025) | Standard vocabulary for terminology work and science. | Vocabulary reference; avoid inventing verbatim definitions or claiming full-text examination. |
| [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/) (W3C Recommendation) | Concept schemes distinguish concepts, preferred labels, alternative labels and documentation notes. | Candidate structured glossary representation, not a requirement to adopt RDF on day one. |
| [W3C SKOS Primer](https://www.w3.org/TR/skos-primer) (informative) | Explains preferred/alternative labels, concept schemes and contextual scope. | Design inspiration; primer is not the normative standard. |
| [Agent Skills specification](https://agentskills.io/specification) | Portable `SKILL.md` format requires frontmatter name and description and supports referenced resources. | Packaging and metadata validation; not proof the reviewer catches errors. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Workflow calls for comparing skill behavior with baselines, cases and improvement cycles. | Use a qualified eval harness before releasing. |
| [Superpowers / writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills) | Advocates baseline-first RED/GREEN/REFACTOR evaluation of process skills. | No pretending an absent model run occurred; deterministic RED check is distinct from behavioral baseline. |
| [Vale](https://vale.sh/) | Configurable deterministic prose linting exists. | Reuse/consider for known vocabulary/style policies; avoid replacing contextual reasoning with regex. |
| [Skill review example](https://github.com/tomzx/agents/blob/main/skills/review-skills/SKILL.md) | Audits skill libraries for duplicate functionality and composability. | Adjacent donor, not a substitute for term/concept review; not imported. |

## Comparison to foundations and existing owned projects

- [Foundation](../FOUNDATION.md): terminology names concepts; lexicology concerns usage; semantics concerns intended meaning. A reviewer should identify **definitions and designation relations** before rejecting expression.
- [Project Record Standard / STANDARD.md](https://github.com/interzettel/project-record-standard/blob/main/standards/STANDARD.md): `Blocked` is a flag with reason/next action, **not** a mutually exclusive execution state. This is local source authority; conflicting general usage is not a universal language error.
- [Spatial Laboratory / evidence-audit](https://github.com/yigit-denktas/spatial-laboratory/blob/main/.agents/skills/evidence-audit/SKILL.md): evidence reconciliation exists; don't duplicate its verification responsibility.
- [Writing Kitchen](https://github.com/yigit-denktas/writing-kitchen): preserve author vocabulary, style and deliberate neologisms, not a homogenizing global glossary.

## Adopted distinctions and reviewer boundary

1. **Concept** is not equivalent to its **designation**; alternate labels can denote one concept, and identical strings can denote different concepts depending on domain.
2. A **term-definition conflict** needs a verifiable authority, exact span, contextual scope and reason.
3. An **unexplained term** is a possible clarification request, not proof the term is wrong.
4. A **neologism** or alternative usage may be valid when defined coherently; do not treat usage frequency as authority.
5. Quotes, code, citations and historical usage require explicit context or should be excluded from unconditional term enforcement.
6. Reviewer must **abstain** when authority is inaccessible or contradictory; do not auto-rewrite normative terms.
7. Out of scope: adjudicating ontology consistency beyond term implications, factual source verification, methodology validity, proofreading and automatic mutation.

## Test-first acceptance path

- Confirm test suite reports RED for absent `terminology-review` artifact before adding the skill.
- Author portable skill and focused references; validate frontmatter, trigger examples, deterministic fixtures and no automatic edits.
- Execute genuine without-skill/with-skill agent runs in the **same model/harness configuration** once one is available; evaluate false positives and correctly scoped conflicts. **No such behavior run has yet happened in this session.**
- Keep reviewer in pilot status until held-out human adjudication.

## Open questions

- Whether term references will initially be project-local Markdown or a structured concept registry; start with existing canonical documents.
- Triggering and instruction coverage in local Windows Claude Code/Codex remain unverified.
- No commercial/paid source text copied to this repository.

## Additional cross-check (26 October 2026, independent pass before revised draft)

- [Agent Skills primary specification](https://agentskills.io/specification) requires skill identity and description but does **not** require individual version metadata. Diakrisis therefore uses one `0.1.0-dev.0` suite version, no skill-specific SemVer.
- [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) explicitly compares skill-on versus no-skill on the same inputs, retaining failures.
- [Microsoft SkillGen](https://www.microsoft.com/en-us/research/publication/skillgen-verified-inference-time-agent-skill-synthesis/) compares repair against regression on paired tasks: positive gains alone are insufficient if valid inputs are newly mishandled.
- [NVIDIA SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) provides optional live evaluations and deterministic checks; considered as a potential donor, **not imported** without licensing/security review.

The existing skill remains an experimental candidate. This source pass is not evidence of model efficacy.
