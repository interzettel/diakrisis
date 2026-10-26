# Authority, sense boundaries and challenge examples

Read only when auditing competing definitions or preparing a disputed finding.

## Authority selection

1. **Applicable agreed source** — canonical project glossary, accepted ADR or a frozen study protocol that actually governs this artifact.
2. **Governing external standard** — when the target explicitly adopts it or the domain requires it; cite the specific accessible edition and provision. A title or abstract alone may establish scope, not detailed requirements.
3. **Local usage within the artifact** — explicitly defined construct or operational usage. Internal contradiction between definition and subsequent usage can be flagged without an external standard.
4. **Broad conventional usage** — useful for reader confusion, but generally a suggestion, not a normative correction.

When two applicable authorities disagree and no precedence rule exists, abstain; ask the author to resolve the conflict. Newer does not automatically supersede a frozen, purpose-specific research protocol.

## Meaning checks

- *Designation*: a word, phrase, abbreviation, symbol or name representing a concept in context.
- *Concept*: domain notion the author intends to identify; one concept may have multiple designations.
- *Definition*: statement constraining the concept's intended meaning.
- *Scope*: domain, audience, language, version and section in which a definition applies.

Informative examples, not quotations from ISO or W3C.

### Positive: local normative conflict

Authority: Project Record Standard explicitly treats `Blocked` as a flag, not one of its mutually exclusive workflow states.

Passage: "The task enters the Blocked execution state."

Expected review: identify that the use of `Blocked` as a state conflicts **with this project's** state model; propose "The task is Ready, but has a blocked flag..." only if it preserves actual state. Avoid suggesting that every task manager must adopt this convention.

### Negative: novel but coherent vocabulary

Authority: author explicitly defines *driftline* as the computed dividing boundary in a spatial algorithm.

Passage: "We extract the driftline from each resulting mesh."

Expected review: no terminology error solely because the term is unusual; ask for definition only if the actual audience/scope has not received one.

### Ambiguous: polysemy across domains

Passage: "Model X is validated and accepted."

Without a governing contract this may refer to experimental validity, input/schema validation, reviewer approval or stakeholder acceptance. Ask which; do not claim which meaning is universally correct.

### Negative: quotations or historical language

Quoted old terminology may be deliberately preserved while a current preferred term appears in editorial narration. Distinguish quotation from author-endorsed vocabulary before suggesting updates.

### Context note: W3C SKOS

SKOS represents a *concept* separately from its preferred and alternative lexical labels. This is useful inspiration for a registry, but a prose document does not require RDF, and a SKOS alternative label is not evidence two concepts are logically identical.

## Primary references

- ISO 704:2022: https://www.iso.org/standard/79077.html
- ISO 1087:2019: https://www.iso.org/standard/62330.html
- W3C SKOS Recommendation: https://www.w3.org/TR/skos-reference/
- Pre-implementation research: docs/research/terminology-review-2026-10-26.md at repository root.
