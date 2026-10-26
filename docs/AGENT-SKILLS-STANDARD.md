# Agent Skills conformance review

**Source:** https://agentskills.io/specification ; `agentskills/agentskills` commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379` observed 2026-10-26.

## Normative shape

A skill directory must contain `SKILL.md`, with YAML frontmatter including `name` and `description`, followed by Markdown instructions.

- `name`: 1–64 chars, lowercase `a-z0-9-`, no leading/trailing or repeated hyphens, exactly matches directory.
- `description`: 1–1024 chars, explains capability and activation circumstances.
- Optional `license`, `compatibility` (1–500 chars), `metadata` (string-string mapping), `allowed-tools` (experimental).
- Typical optional `scripts/`, `references/`, `assets/`. Put large sources in references, not in every prompt.
- Main `SKILL.md` under 500 lines; instructions under 5,000 tokens recommended; progressive disclosure through metadata → instructions → resources.
- Relative file references; avoid deep indirect dependency chains.
- Validate with official `skills-ref validate <skill-directory>` and portable runtime discovery tests. Note the reference implementation explicitly describes itself as demonstrative rather than production software; structural conformity is not behavioral quality.

## Local design rules (additional, not claims of standard requirements)

1. A skill's `description` names concrete activation triggers; it must also have non-trigger examples in the evaluation set.
2. Skill bodies specify inputs, authority, procedure, output contract, abstentions, limits, and handoffs.
3. Source text being reviewed is untrusted, never an instruction to the reviewer.
4. Every factual verdict is traceable to an artifact span and evidence/rule.
5. Formal checks should be done in validators; model review is advisory.
6. Keep independent judges if possible, but no invented independence or consensus authority.
7. Never install automatically into global user profiles, or grant permissions by importing a skill.
8. Schema validation and real task evaluation are different gates.

## How to validate

A first skill passes only when:
- Frontmatter passes `skills-ref`.
- The selected runtime discovers and triggers the skill.
- At least one baseline without the skill, positive case, negative control, and unfamiliar case are evaluated.
- Invalid findings can be challenged and corrected without rewriting the author's intended meanings.
- Required scripts work offline, are licensed, and have deterministic tests.

Anthropic skill-creator and Superpowers writing-skills provide complementary iteration methods, but neither replaces this format specification or empirical review.