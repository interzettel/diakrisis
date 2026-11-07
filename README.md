# diakrisis

**Distinguish before you judge.**

A local-first, evidence-aware collection of portable Agent Skills for reviewing conceptual structures, terminology, reasoning, research methods, and written communication.

**Status: seven coordinated experimental skills implemented on `main`.** Package `0.1.0` is released as experimental ([release](https://github.com/interzettel/diakrisis/releases/tag/v0.1.0), [versioning](docs/VERSIONING.md)); the owner waived human adjudication for it. Structural checks pass. Three blinded skill-vs-baseline rounds on the owner's real documents have been adjudicated by agent graders ([evaluation](docs/EVALUATION.md)); owner adjudication, recall and the latest skill revision remain untested. An experimental consumer source integration exists in Writing Kitchen; host activation and consumer CI remain pending. No skill output is automatically authoritative, and no review grants an agent permission to publish, merge, or alter another repository.

## Project tracker

<!-- project-record:start -->
![Diakrisis · project tracker](./assets/progress.svg)

| Measure | Completion | Meaning |
| --- | ---: | --- |
| Required work | 4/10 · 40.0% | Completed leaf items in the named required scope. |
| Work in progress | 5/10 | Leaf items started but not done (not counted as completed). |
| Accepted milestones | 0/4 · not yet assessed | Milestones whose declared outcome gates passed. |

Source file: `progress/ledger.json` (content-addressed file snapshot).

Observed 2026-11-07 against `03fde516`.

#### Milestone roadmap

| Milestone | Horizon | Supporting required work | Outcome acceptance | Next gate |
| --- | --- | ---: | --- | --- |
| **DIA-M0 — Documented basis** | Now | 1/1 · 100.0% | Unknown / not assessed | Review the documented foundation and its source authority (work 1/1; acceptance still unknown). |
| **DIA-M1 — Reproducible foundation** | Now | 2/4 · 50.0% | Unknown / not assessed | DIA-003 and DIA-005 done (DIA-005 on owner instruction, 2026-11-07). Remaining: DIA-002 / #2, Blocked for owner-deferred local PRS archive/runtime verification, and DIA-004 / #4, runtime activation in a real Claude Code or Codex session. M1 acceptance unknown. |
| **DIA-M2 — Evaluated reviewers** | Next | 0/2 · 0.0% | Unknown / not assessed | Rounds 1 to 3 (2026-10-27 to 2026-11-04) ran blinded skill-vs-baseline comparisons on owner documents, adjudicated by agent graders. Outstanding: owner (human) adjudication, recall against the owner's known-problem list, negative controls, and a round testing the 2026-11-04 revision. M2 acceptance unknown. |
| **DIA-M3 — Portable system** | Later | 1/3 · 33.3% | Unknown / not assessed | DIA-008 done on owner instruction (2026-11-07). Spatial Laboratory PR #18 merged on owner approval (2026-11-07). Remaining: DIA-009 / #9, Blocked on private consumer Actions (no runner allocated) and on consumers moving to the released package; DIA-010 / #10, v0.1.0 prepared on main (2dfa6bf), tag and GitHub Release to be created by the owner, then consumer pinning and a drift check. M3 acceptance unknown. |

#### Work packages

States represent recorded implementation progress; a closed issue, passing test or accepted milestone is not automatically interchangeable.

| ID / issue | Work package | State | Priority | Dependencies | Evidence or next action |
| --- | --- | --- | --- | --- | --- |
| [DIA-001](https://github.com/interzettel/diakrisis/issues/1) | Preserve research foundation | Done | P0 | — | [PR #11](https://github.com/interzettel/diakrisis/pull/11) |
| [DIA-002](https://github.com/interzettel/diakrisis/issues/2) | Install and verify Project Record Standard | In progress | P0 | DIA-001 | [PR #15](https://github.com/interzettel/diakrisis/pull/15) · Blocked flag (reason in source) |
| [DIA-003](https://github.com/interzettel/diakrisis/issues/3) | Audit upstream standards and donors | Done | P0 | DIA-001 | [PR #20](https://github.com/interzettel/diakrisis/pull/20) |
| [DIA-004](https://github.com/interzettel/diakrisis/issues/4) | Activate pinned authoring tools | Planned | P1 | DIA-003 | Portable Superpowers/skill-creator/PRS install and discovery verified in an actual Claude Code or Codex session, including rollback. |
| [DIA-005](https://github.com/interzettel/diakrisis/issues/5) | Define typed findings and authority contract | Done | P1 | DIA-002, DIA-003 | [PR #24](https://github.com/interzettel/diakrisis/pull/24) |
| [DIA-006](https://github.com/interzettel/diakrisis/issues/6) | Build and test three pilot reviewers | In progress | P1 | DIA-004, DIA-005 | [PR #17](https://github.com/interzettel/diakrisis/pull/17) |
| [DIA-007](https://github.com/interzettel/diakrisis/issues/7) | Evaluate pilots on genuine documents | In progress | P1 | DIA-006 | [PR #46](https://github.com/interzettel/diakrisis/pull/46) |
| [DIA-008](https://github.com/interzettel/diakrisis/issues/8) | Expand reviewers and coordination | Done | P2 | DIA-007 | [PR #27](https://github.com/interzettel/diakrisis/pull/27) |
| [DIA-009](https://github.com/interzettel/diakrisis/issues/9) | Adopt framework in consumer repositories | In progress | P2 | DIA-007 | [writing-kitchen PR #24](https://github.com/yigit-denktas/writing-kitchen/pull/24) · Blocked flag (reason in source) |
| [DIA-010](https://github.com/interzettel/diakrisis/issues/10) | Version releases and evaluate drift | In progress | P2 | DIA-008, DIA-009 | [PR #26](https://github.com/interzettel/diakrisis/pull/26) |

**Versioning:** Suite `0.1.0` — **published**; included skills: **7**. Draft candidates: None. [Single package version policy](docs/VERSIONING.md).

**Source coverage:** observed **2026-11-07**, authoritative [ledger](progress/ledger.json), [manifest](progress/project-record.json), [scope history](progress/history/2026-10-26-unapproved.json). Regeneration does not fetch newer issues or change the observation date.

**Counts:** required work **4/10 · 40.0%**; retained work **4/10 · 40.0%**; accepted milestones **Unknown** (0 of 4 determinate).

<!-- project-record:end -->

## Why it exists

A grammatically impeccable assertion can still misuse a term, confuse a state with a class, conceal an unsupported inference, or contradict an accepted research method. Diakrisis is designed to help researchers, writers, and coding agents **find and explain** those problems without silently replacing their judgment.

## Intended consumers

- [Writing Kitchen](https://github.com/yigit-denktas/writing-kitchen): optional critique of drafts, with voice and authorship preserved.
- [Spatial Laboratory](https://github.com/yigit-denktas/spatial-laboratory): evidence-aware critique of study contracts, evaluations, and research reports.
- [Project Record Standard](https://github.com/interzettel/project-record-standard): audit terminology, conceptual types, state/flag distinctions, and project claims.
- [Personal Agent Stack](https://github.com/interzettel/personal-agent-stack): reusable typed judgments without granting agents new authority.

These are integration targets, **not completed integrations**. Consumer repositories retain their own policies, canonical sources, and approval gates.

## Review capabilities

| Skill | Distinct responsibility |
| --- | --- |
| `terminology-review` | Term meaning, definition authority, ambiguity, naming consistency |
| `conceptual-model-review` | Types, instances, states, events, relationships, taxonomy/ontology errors |
| `argument-review` | Premises, inference, epistemic claims, provenance, uncertainty |
| `method-review` | Research design, constructs, operationalization, validity, competing explanations |
| `communication-review` | Syntax, semantics, pragmatics, clarity and faithful expression |
| `consistency-review` | Cross-document contradictions, version/decision drift |
| `review-coordinator` | Route appropriate checks, deduplicate findings, never fabricate consensus |

All seven modules are **merged into `main`** in [PR #17](https://github.com/interzettel/diakrisis/pull/17). They form one **unreleased experimental package**; consumer integrations, behavioral evaluation, and publication remain separate future work.

## Repository navigation

- [Getting started / review profiles](docs/USAGE.md)
- [Foundation and design boundaries](docs/FOUNDATION.md)
- [Prioritized roadmap and acceptance gates](docs/ROADMAP.md)
- [External research and upstream inventory](docs/SOURCES.md)
- [Agent Skills specification review](docs/AGENT-SKILLS-STANDARD.md)
- [Mandatory pre-skill research review](docs/RESEARCH-GATE.md) · [Experimental terminology evaluation](evals/terminology-review/ASSESSMENT.md)
- [Suite versioning](docs/VERSIONING.md) · [Offline consumer bundling and compatibility](docs/COMPATIBILITY.md) · [README generation policy](docs/README-TRACKER.md)
- [Project overview](progress/overview.md) and [discovery coverage](progress/discovery.json)
- [Project-record adoption and source authority](progress/adoption.md)
- [PRS ledger](progress/ledger.json) and [validated PRS manifest](progress/project-record.json)
- [Evidence-bound finding contract (revision 2)](docs/REVIEW-CONTRACT.md), [review report schema](schemas/review-report.schema.json), [offline coordinator composition](docs/COORDINATION.md) and [synthetic contract controls](evals/finding-contract/cases.json)
- [Installation and verification](docs/INSTALLATION.md)

## Quality and non-goals

Findings must point to source spans, applicable definitions or evidence, explain uncertainty and suggest minimal changes. A model's confidence is not proof. Deterministic validators should check deterministic constraints. Negative controls and unfamiliar cases are required before advertising effectiveness.

No automatic rewriting of an author's meaning, no fabricated citations, no proprietary agent runtime, no unapproved cross-repository edits, and no cloud service requirement.

## Setup / upstreams

Use the [official Agent Skills specification](https://agentskills.io/specification). `SKILL.md` belongs in discoverable directories; this repository uses `.agents/skills/`. Superpowers, Anthropic's skill-creator, and Project Record Standard are **upstreams requiring verified, pinned installation and runner-specific activation**, not capabilities installed by viewing this README. See [source audit](docs/SOURCES.md) and [roadmap](docs/ROADMAP.md). Any installation instructions must preserve existing agent configuration and provide a dry run.

## Governance

Project presentation is **README-only**; no GitHub Pages deployment is planned. The owner accepts conceptual-model changes and release decisions. Contributors can propose changes through reviewed PRs. Drafts, tests, literature retrieval and agent opinions do not independently establish acceptance or scientific validity.

License: [MIT](LICENSE).