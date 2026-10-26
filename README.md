# diakrisis

**Distinguish before you judge.**

A local-first, evidence-aware collection of portable Agent Skills for reviewing conceptual structures, terminology, reasoning, research methods, and written communication.

**Status: bootstrap / research and planning.** Official Project Record Standard validation and isolated skill installation have passed in GitHub Actions; no local Claude/Codex activation or skill-efficacy evaluation is yet verified. This repository is not yet a validated scientific-review product. No skill output is automatically authoritative; no review grants an agent permission to publish, merge, or alter another repository.

## Project tracker

<!-- project-record:start -->
![Diakrisis · current required scope](./assets/progress.svg)

| Measure | Completion | Meaning |
| --- | ---: | --- |
| Required work | 1/10 · 10.0% | Completed leaf items in the named required scope. |
| Accepted milestones | 0/4 · Not measured | Milestones whose declared outcome gates passed. |

Interactive route not connected. · Source file: `progress/ledger.json` (content-addressed file snapshot).

Observed 2026-10-26 against `ffd8002b`.

#### Milestone roadmap

| Milestone | Horizon | Supporting required work | Outcome acceptance | Next gate |
| --- | --- | ---: | --- | --- |
| **DIA-M0 — Documented basis** | Now | 1/1 · 100.0% | Unknown / not assessed | Owner acceptance and verified gate evidence pending |
| **DIA-M1 — Reproducible foundation** | Now | 0/4 · 0.0% | Unknown / not assessed | Owner acceptance and verified gate evidence pending |
| **DIA-M2 — Evaluated reviewers** | Next | 0/2 · 0.0% | Unknown / not assessed | Owner acceptance and verified gate evidence pending |
| **DIA-M3 — Portable system** | Later | 0/3 · 0.0% | Unknown / not assessed | Owner acceptance and verified gate evidence pending |

#### Work packages

States represent recorded implementation progress; a closed issue, passing test or accepted milestone is not automatically interchangeable.

| ID / issue | Work package | State | Priority | Dependencies | Evidence or next action |
| --- | --- | --- | --- | --- | --- |
| [DIA-001](https://github.com/interzettel/diakrisis/issues/1) | Preserve research foundation | Done | P0 | — | [Evidence](https://github.com/interzettel/diakrisis/pull/11) |
| [DIA-002](https://github.com/interzettel/diakrisis/issues/2) | Install and verify Project Record Standard | In progress | P0 | DIA-001 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-003](https://github.com/interzettel/diakrisis/issues/3) | Audit upstream standards and donors | In progress | P0 | DIA-001 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-004](https://github.com/interzettel/diakrisis/issues/4) | Activate pinned authoring tools | Planned | P1 | DIA-003 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-005](https://github.com/interzettel/diakrisis/issues/5) | Define typed findings and authority contract | In progress | P1 | DIA-002, DIA-003 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-006](https://github.com/interzettel/diakrisis/issues/6) | Build and test three pilot reviewers | In progress | P1 | DIA-004, DIA-005 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-007](https://github.com/interzettel/diakrisis/issues/7) | Evaluate pilots on genuine documents | Planned | P1 | DIA-006 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-008](https://github.com/interzettel/diakrisis/issues/8) | Expand reviewers and coordination | Planned | P2 | DIA-007 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-009](https://github.com/interzettel/diakrisis/issues/9) | Adopt framework in consumer repositories | Planned | P2 | DIA-007 | See issue and docs/ROADMAP.md for acceptance criteria |
| [DIA-010](https://github.com/interzettel/diakrisis/issues/10) | Version releases and evaluate drift | Planned | P2 | DIA-008, DIA-009 | See issue and docs/ROADMAP.md for acceptance criteria |

**Versioning:** Suite `0.1.0-dev.0` — **unreleased**; released skills: **0**. Draft candidates: `terminology-review` 0.1.0-draft (draft, [PR #12](https://github.com/interzettel/diakrisis/pull/12)). [Per-skill version and release policy](docs/VERSIONING.md).

**Source coverage:** observed **2026-10-26**, authoritative [ledger](progress/ledger.json), [manifest](progress/project-record.json), [scope history](progress/history/2026-10-26-unapproved.json). Regeneration does not fetch newer issues or change the observation date.

**Counts:** required work **1/10 · 10.0%**; retained work **1/10 · 10.0%**; accepted milestones **Unknown** (0 of 4 determinate).

<!-- project-record:end -->

## Why it exists

A grammatically impeccable assertion can still misuse a term, confuse a state with a class, conceal an unsupported inference, or contradict an accepted research method. Diakrisis helps researchers, writers, and coding agents **find and explain** those problems without silently replacing their judgment.

## Intended consumers

- [Writing Kitchen](https://github.com/yigit-denktas/writing-kitchen): optional critique of drafts, with voice and authorship preserved.
- [Spatial Laboratory](https://github.com/yigit-denktas/spatial-laboratory): evidence-aware critique of study contracts, evaluations, and research reports.
- [Project Record Standard](https://github.com/interzettel/project-record-standard): audit terminology, conceptual types, state/flag distinctions, and project claims.
- [Personal Agent Stack](https://github.com/interzettel/personal-agent-stack): reusable typed judgments without granting agents new authority.

These are integration targets, **not completed integrations**. Consumer repositories retain their own policies, canonical sources, and approval gates.

## Proposed review capabilities

| Skill | Distinct responsibility |
| --- | --- |
| `terminology-review` | Term meaning, definition authority, ambiguity, naming consistency |
| `conceptual-model-review` | Types, instances, states, events, relationships, taxonomy/ontology errors |
| `argument-review` | Premises, inference, epistemic claims, provenance, uncertainty |
| `method-review` | Research design, constructs, operationalization, validity, competing explanations |
| `communication-review` | Syntax, semantics, pragmatics, clarity and faithful expression |
| `consistency-review` | Cross-document contradictions, version/decision drift |
| `review-coordinator` | Route appropriate checks, deduplicate findings, never fabricate consensus |

These are **planned modules** rather than a list of shipped capabilities. The initial slice is terminology, conceptual modeling and arguments.

**Tracking:** Required approved work: **0/0 — Not measured**. Proposed retained work: **0/10 completed**. Milestone acceptance: **unknown**. These are separate measures; see [ledger](progress/ledger.json).

## Repository navigation

- [Foundation and design boundaries](docs/FOUNDATION.md)
- [Prioritized roadmap and acceptance gates](docs/ROADMAP.md)
- [External research and upstream inventory](docs/SOURCES.md)
- [Agent Skills specification review](docs/AGENT-SKILLS-STANDARD.md)
- [Per-skill versioning](docs/VERSIONING.md) · [README generation policy](docs/README-TRACKER.md)\n- [Project overview](progress/overview.md) and [discovery coverage](progress/discovery.json)
- [Project-record adoption and source authority](progress/adoption.md)
- [Proposed PRS ledger](progress/ledger.json) and [validated PRS manifest](progress/project-record.json)
- [Provisional review finding contract](docs/REVIEW-CONTRACT.md) and [RED-phase test cases](evals/README.md)
- [Installation and verification](docs/INSTALLATION.md)

## Quality and non-goals

Findings must point to source spans, applicable definitions or evidence, explain uncertainty and suggest minimal changes. A model's confidence is not proof. Deterministic validators should check deterministic constraints. Negative controls and unfamiliar cases are required before advertising effectiveness.

No automatic rewriting of an author's meaning, no fabricated citations, no proprietary agent runtime, no unapproved cross-repository edits, and no cloud service requirement.

## Setup / upstreams

Use the [official Agent Skills specification](https://agentskills.io/specification). `SKILL.md` belongs in discoverable directories (planned `.agents/skills/`). Superpowers, Anthropic's skill-creator, and Project Record Standard are **upstreams requiring verified, pinned installation and runner-specific activation**, not capabilities installed by viewing this README. See [source audit](docs/SOURCES.md) and [roadmap](docs/ROADMAP.md). Any installation instructions must preserve existing agent configuration and provide a dry run.

## Governance

Project presentation is **README-only**; no GitHub Pages deployment is planned. The owner accepts conceptual-model changes and release decisions. Contributors can propose changes through reviewed PRs. Drafts, tests, literature retrieval and agent opinions do not independently establish acceptance or scientific validity.

License: [MIT](LICENSE).