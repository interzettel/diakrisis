# Source inventory and reuse assessment

**Observed:** 2026-10-26. **Detailed and source-linked decision matrix:** [DIA-003 upstream donor audit](research/DONOR-AUDIT.md). The audit is a documentary/manual inspection, **not a full code-security review, license opinion or behavioral evaluation**.

## Main decisions

| Source | Exact observed revision | Decision | Critical qualification |
| --- | --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | `agentskills/agentskills` `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | **Adopt** open skill format; reference pinned `skills-ref` | Apache-2.0 source; format conformance not reviewer efficacy |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator) | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | **Reuse** as separate pinned authoring dependency | Per-skill Apache-2.0; wider third-party notices vary |
| [Superpowers](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | **Reuse** authoring methods, not global hooks | MIT, hook execution and optional visual telemetry need runtime/privacy consideration |
| [Project Record Standard v0.4.1](https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1) | `ebc6afb0b977ff3d7605893c73ac63021775c4d3` | **Reuse** source authority through existing pinned submodule | No root license or declared SPDX in inspected pinned source; owner decision open at [PRS #4](https://github.com/interzettel/project-record-standard/issues/4), MIT **proposed only** in [draft PR #5](https://github.com/interzettel/project-record-standard/pull/5); resolve before redistribution |
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62) | `5f2bc0341354fd5590aef76a533ada1e1e5b4e62` | **Reference**, selectively adapt only if needed | Root MIT; skill-level licensing may differ; many optional external services |
| [KalarisLabs research-agent-skills](https://github.com/KalarisLabs/research-agent-skills/tree/b0ee35abfd7e26428846fbd84f282114560a5fbd) | `b0ee35abfd7e26428846fbd84f282114560a5fbd` | **Reference** selective citation/academic-writing guidance | MIT + third-party notices; 159 attributed upstream K-Dense skills are *not* independent evidence |
| [Vale prose linter](https://github.com/vale-cli/vale/tree/8b9bfb97700a707140fff9f444048439df5bc9b1) | `vale-cli/vale` `v3` at `8b9bfb97700a707140fff9f444048439df5bc9b1` | **Optional adapt**, not core dependency | MIT engine; downloaded rule packs and source-specific terminology policy must be separately reviewed |
| [W3C SKOS](https://www.w3.org/TR/skos-reference/), [SHACL](https://www.w3.org/TR/shacl/), [OWL 2](https://www.w3.org/TR/owl2-primer/), [PROV-O](https://www.w3.org/TR/prov-o/) | Stable W3C Recommendations with dates in [audit](research/DONOR-AUDIT.md) | **Reference** formal concept, validation and provenance semantics | Normative documentation is not imported software; SHACL **1.2 Core remains a 2026 Working Draft** |

A *source SHA* identifies observed repository bytes, not a certified binary, downloaded asset digest, local installation receipt or validated review outcome.

## Existing owned repositories (initially inspected 2026-10-26)

- `yigit-denktas/spatial-laboratory`: 16 previously observed `.agents/skills/` directories, including `evidence-audit`, `lab-research-contract`, `spatial-research-method-selection`, and `first-principles-exposition`. Treat domain-specific methods and evidence procedures as consumer-owned.
- `interzettel/project-record-standard`: 11 workflow skills and canonical progress semantics. `Blocked` is a flag, not an execution state.
- `interzettel/personal-agent-stack`: authorization/delegation boundaries and ADRs are authoritative in their own repository.
- `yigit-denktas/writing-kitchen`: personal author-voice system, concept graph and typed judges proposed in its README; it retains final writing authority.

These are integration targets, not complete cross-repository migrations or evidence that all local copies were freshly inspected in this DIA-003 audit.

## Observed installation and testing boundaries

The authenticated GitHub connector can inspect repository files and create reviewed commits. CI has checked out the four pinned submodules and exercised the existing project-local install and format checks in disposable Actions environments. **No actual Windows Claude Code or Codex client activation is verified.** The model-behavior testing phase is explicitly deferred by owner; no tests were run for donor effectiveness in this audit.

**Pinned upstreams in the repository:** Agent Skills reference validator, Anthropic skill-creator source, Superpowers source and PRS v0.4.1 source. **Not installed:** K-Dense, KalarisLabs, Vale or any W3C runtime validator.

## Import/security rules

Inspect source, exact skill-level license and bundled notices before importing; scripts may touch the network, files, environment or host hooks. Never execute unreviewed remote `curl | sh`, `irm | iex`, global install or plugin automation. A plain Markdown skill doesn't authorize new file access or publication rights. Default to project-scoped pinned installs, source-linked changes, explicit permission and rollback. **Do not redistribute Project Record Standard code under an assumed MIT license** until its source owner clarifies the missing license terms. The full rationale and remaining gates are recorded in [the DIA-003 audit](research/DONOR-AUDIT.md).
