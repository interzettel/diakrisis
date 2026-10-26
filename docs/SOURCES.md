# Source inventory and reuse assessment

**Observed:** 2026-10-26. This is an initial evidence ledger, not a complete security/code-quality audit. Source tags and commits are noted where verified through GitHub.

## Core upstreams

| Source | Observed source identity | Reuse decision | Follow-up |
| --- | --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | `agentskills/agentskills` main at `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | Adopt format, validate with `skills-ref` | Test cross-client discovery/activation |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | `anthropics/skills` main at `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Review and install into selected agent runtime | License per file, scripts, sandbox; check update policy |
| [Superpowers](https://github.com/obra/superpowers) | `obra/superpowers` main at `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | Install via supported runner/plugin; use writing-skills, TDD | Avoid unsafe manual hook copies; verify activation |
| [Project Record Standard](https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1) | v0.4.1 points to commit `ebc6afb0b977ff3d7605893c73ac63021775c4d3`; contract 0.2.0 | Source of shared project terminology, ledger model, skills installation | Verify published zip checksums and local dry-run |
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | candidate, revision not yet pinned | Compare scientific writing, peer review and citations | Verify per-skill license, behavior and tests |
| [KalarisLabs research-agent-skills](https://github.com/KalarisLabs/research-agent-skills) | candidate, revision not yet pinned | Compare citation verification and research workflows | Independently evaluate security and claims |
| [Vale](https://vale.sh/) | candidate deterministic prose linter | Evaluate for style and terminology | Verify rules and language coverage |
| [W3C SKOS](https://www.w3.org/TR/skos-reference/) / [SHACL](https://www.w3.org/TR/shacl/) / [PROV-O](https://www.w3.org/TR/prov-o/) | normative specifications | Possible taxonomic, constraint and provenance instruments | Use when complexity justifies formal representation |

A Git commit pin identifies source bytes, not necessarily a trusted release or a verified installation. Nothing above is assumed installed merely because a URL or pin was recorded.

## Existing owned repositories (observed main branch)

- `yigit-denktas/spatial-laboratory`: 16 directories in `.agents/skills/` observed; including `evidence-audit`, `lab-research-contract`, `spatial-research-method-selection`, `first-principles-exposition`. Reuse domain-specific evidence and method criteria rather than copying unexamined text.
- `interzettel/project-record-standard`: 11 source skills and canonical vocabulary. `Blocked` is a flag, not a mutually exclusive execution state.
- `interzettel/personal-agent-stack`: authorization/delegation boundaries and prior ADRs. Consumer retains authority.
- `yigit-denktas/writing-kitchen`: personal writing system with concept graph, typed judges and provenance proposed in its README. Consumer integration is not implemented here.

## Known capability gap

Available workspace cannot fetch GitHub with ordinary `git clone` (DNS resolution unavailable), but the authenticated GitHub connector reads/writes repository data. We staged pinned sources via the connector; GitHub Actions successfully installed all three skill toolkits in an isolated disposable checkout and passed the official Project Record Standard ledger check on 2026-10-26. This does **not** demonstrate activation on the user's Windows/Claude/Codex environment. Verified local installs and test receipts are independent gates.

## Security and license rules

Inspect provenance and license **before** importing upstream code. Run no remote installer via pipe-to-shell. Use pinned, reviewed downloads and checksums; scope scripts to the repository workspace; avoid hidden hooks and mutation of global agent profiles without an explicitly chosen harness. Test activation and uninstall/rollback.