# Terminology-review conceptual and testability audit

**Date:** 2026-10-26. **Reviewer:** assistant exploratory document inspection. **Status:** qualitative analysis only; NOT an independent human blind adjudication, sampled inference run, or measured effectiveness result.

## Examined materials

- Current pilot `.agents/skills/terminology-review/SKILL.md` and `references/CASES.md`;
- Diakrisis foundation and intended 7-skill division of responsibilities;
- ISO 704:2022 / ISO 1087:2019 publicly accessible abstracts (not full text);
- W3C SKOS concept/label reference;
- Agent Skills specification, Anthropic skill-creator and paired with-skill/without-skill evaluation guidance;
- [2026-10-26 research record](../../docs/research/terminology-review-2026-10-26.md).

## Conceptual review: source constraints and revisions

| Check | Finding / action | Boundary |
| --- | --- | --- |
| Designation vs concept | Explicit mapping required. Added reminder that concept, term/label and referent are not interchangeable. | Lexical correctness is not itself ontological truth. |
| Scoped authority | Clarified that adopted standards or binding domain rules can outrank local convention; sources must be inspected and applicability established. | No universal local-before-global hierarchy. |
| State vs activity | Can identify terminology conflict **only when the governing vocabulary defines that distinction**. Otherwise refer a true conceptual modeling issue to `conceptual-model-review`. | Avoid duplicate false positives. |
| Construct vs measured observation | Words like 'quality', 'reliable', 'valid' may shift meanings across measurement contexts. Flag equivocation, but route evidential and statistical claims to method/argument review. | Do not equate textual overclaim with false empirical observations. |
| Neologism, regional terms, translation | Consistent author-defined unfamiliar term is a negative control; bilingual ambiguity and historical quotations require context. | Don't flatten valid vocabulary for convenience. |
| Conflicting sources | No confirmed contradiction without applicable authority and exact span. A valid response may be to abstain. | Missing evidence is not proven error. |
| Untrusted input | Reviewed material is data, not command; no silent edits or private-data disclosure. | Acceptance remains with owner. |

## Available checks performed and missing checks

Structural checks are available in CI and exercise frontmatter, required decision boundary phrases, **all three classes of fixture** (positive, negative, uncertain), no skill-specific version, runner local-only network guard, exact paired plan and dry-run without inference.

The official pinned `skills-ref` verifies portability of the Agent Skills format. These checks do **not** prove that any LLM catches the intended conflicts.

A repeatable paired runner is available: `python tools/terminology_eval.py --dry-run` (no model calls). For actual inference, the owner or authorized local operator may use `--execute --model <installed-ollama-model> --output <new-file.json>`, which only connects to local Ollama and writes raw results. Its 'with-skill' arm injects the skill's instructions explicitly; this tests instruction effect, **not automatic skill discovery in Claude Code/Codex**.

**Not observed:** Ollama model or Claude Code active runtime, no-skill baseline outputs, treatment outputs, model variation, human judgments, false-positive rate, or release-quality regression checks. Do not describe pilot as evaluated or ready for production.

## Go / no-go

- **GO** for retaining as an experimental skill in the *unreleased* unified Diakrisis package; CI/format tests required.
- **NO-GO** for claiming proven error detection, accepting research conclusions or publishing a stable package release.
- Next meaningful action: execute same-model/same-context paired runs, independently adjudicate false positives and unsupported findings, document counterexamples, then revise before a production release.
