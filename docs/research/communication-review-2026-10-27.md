# Communication review: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** whether the intended audience can recover the author's intended message. Not whether claims are true or justified (argument-review), not term definitions (terminology-review). **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](communication-review-2026-10-26.md).

## Sources checked for this revision

- [ISO 24495-1:2023](https://committee.iso.org/standard/78907.html), published 2023-06-20, edition 1; its four governing principles as summarised by the [International Plain Language Federation](https://www.iplfederation.org/the-iso-plain-language-standard-part1-and-part2): readers get what they need, can find it, can understand it, and can use it. Further parts (legal, science writing, design) are in development.
- [Li et al. (2026)](https://arxiv.org/pdf/2605.25415): LLM reviewers under-flag clarity relative to human reviewers.

## Observed, uncertain, contradicted

- Observed: a current international standard gives four reader-centred principles usable as categories without imposing a house style.
- Observed: LLM reviewers miss clarity problems more than they overstate them, so the skill should not be tuned towards fewer findings.
- Uncertain: how the principles apply to creative and mixed-language writing; voice-preservation rules stay in force and take precedence.

## Decisions

- **Adopt categories:** `syntactic-ambiguity`, `referential-ambiguity`, `scope-ambiguity`, `relevance`, `findability`, `understandability`, `usability`, `register-or-audience-mismatch`.
- **Boundary with argument:** whether confidence matches the evidence belongs to argument-review; this skill flags only phrasing that leaves the author's actual confidence unclear to the reader.
- **ISO 24495-1 is a reference, not a mandate:** it applies only when the author or project adopts plain-language goals; otherwise findings are suggestions.
- **Inline** categories and severity definitions in `SKILL.md`.

## Licences and security

No text from the standard is reproduced; only the principle names as published by the federation. Reviewed text stays untrusted.

## Controls

- Positive: "The agents reviewed the designs that were blocked yesterday" → `scope-ambiguity`.
- Negative: an essay's deliberate fragments with clear meaning → no finding.
- Abstention: a regional idiom with unknown audience → ask for the audience.

## Evaluation status

Deferred by the owner to DIA-007. No baseline or model run exists.
