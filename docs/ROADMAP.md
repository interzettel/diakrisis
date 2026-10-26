# Diakrisis roadmap — issue- and milestone-linked

**Working scope authorized:** 2026-10-26. **Reference:** [Project Record Standard v0.4.1](https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1) (record contract `0.2.0`). **Source of truth:** [ledger](../progress/ledger.json) and [manifest](../progress/project-record.json), not this prose or issue closure.

**Observation:** 2026-10-26 after [seven-skill merge PR #17](https://github.com/interzettel/diakrisis/pull/17) and [README reconciliation PR #18](https://github.com/interzettel/diakrisis/pull/18). All seven skill instructions are on `main` as a single experimental, unreleased `0.1.0-dev.0` package. **DIA-001** and **DIA-003** meet their scoped completion criteria; **required work 2/10 (20.0%)**. [DIA-003 donor audit](research/DONOR-AUDIT.md) was merged in [PR #20](https://github.com/interzettel/diakrisis/pull/20). All four milestone acceptance gates remain **unknown**, not failed or accepted. Owner explicitly deferred interactive model testing until end of build.

## Current authorized queue

**DIA-002 / GitHub #2 — licensing decision resolved.** The [Project Record Standard source owner approved MIT](https://github.com/interzettel/project-record-standard/blob/main/standards/LICENSING-DECISION.md) for their rights-controlled original material including historical v0.4.1; [PRS PR #5](https://github.com/interzettel/project-record-standard/pull/5) is **merged**. That historical tag, archive and SHA-256 are unchanged. Third-party rights retain their own terms. **DIA-002 remains In progress + Blocked solely on owner-deferred local installation/activation and independent archive verification.**

**Eligibility qualification:** DIA-002 is **In progress + Blocked flag** for independently checked archive/download and real Claude/Codex activation, both postponed by owner until the final test phase. DIA-004 is likewise deferred. **DIA-005 / issue #5 contract revision 1 is now implemented** under the owner's build-first exception in [PR #24](https://github.com/interzettel/diakrisis/pull/24) with positive/negative/abstention structural controls. Its dependency on unfinished DIA-002 still prevents calling it Done or accepting DIA-M1. DIA-006–DIA-010 require later gate evidence. There is no currently eligible unblocked completion item; do not invent unrelated work or override deferral.

## Accounted work and dependencies

These ten records alone constitute the current required-work denominator. GitHub issues provide delivery/discussion; each has one canonical ledger milestone. **None of the ten tracked GitHub issues had a native milestone assigned in the 2026-10-26 inspection**, so these DIA-M IDs are *ledger checkpoints*, not GitHub milestone objects.

| ID / issue | Ledger milestone | Priority | State | Dependencies | Remaining criterion |
| --- | --- | --- | --- | --- | --- |
| [DIA-001 / #1](https://github.com/interzettel/diakrisis/issues/1) | DIA-M0 | P0 | Done | — | Foundation preserved (met); M0 acceptance separately pending |
| [DIA-002 / #2](https://github.com/interzettel/diakrisis/issues/2) | DIA-M1 | P0 | In progress, **Blocked** | DIA-001 | Owner-approved MIT documented in upstream merged PR #5; independent archive and runtime evidence deferred by owner. |
| [DIA-003 / #3](https://github.com/interzettel/diakrisis/issues/3) | DIA-M1 | P0 | **Done** | DIA-001 | Donor audit merged in [PR #20](https://github.com/interzettel/diakrisis/pull/20); M1 acceptance separate |
| [DIA-004 / #4](https://github.com/interzettel/diakrisis/issues/4) | DIA-M1 | P1 | Planned | DIA-003 | Verified interactive Claude/Codex authoring toolchain activation and rollback; deferred to final test phase |
| [DIA-005 / #5](https://github.com/interzettel/diakrisis/issues/5) | DIA-M1 | P1 | In progress (schema implemented) | DIA-002, DIA-003 | [PR #24](https://github.com/interzettel/diakrisis/pull/24): contract and deterministic examples checked; deferred dependency and final behavior evidence outstanding |
| [DIA-006 / #6](https://github.com/interzettel/diakrisis/issues/6) | DIA-M2 | P1 | In progress (authored early by owner direction) | DIA-004, DIA-005 | Empirical review quality and independent adjudication postponed |
| [DIA-007 / #7](https://github.com/interzettel/diakrisis/issues/7) | DIA-M2 | P1 | Planned | DIA-006 | Actual real-document evaluation/negative control evidence postponed |
| [DIA-008 / #8](https://github.com/interzettel/diakrisis/issues/8) | DIA-M3 | P2 | In progress (authored early by owner direction) | DIA-007 | Cross-skill composition and coordinator behavior assessment postponed |
| [DIA-009 / #9](https://github.com/interzettel/diakrisis/issues/9) | DIA-M3 | P2 | Planned | DIA-007 | Reviewed, reversible consumer integration PRs |
| [DIA-010 / #10](https://github.com/interzettel/diakrisis/issues/10) | DIA-M3 | P2 | Planned | DIA-008, DIA-009 | **One package version**, publication receipts, pinned consumers and drift policy |

The owner instructed **build all seven instructions before behavioral testing**. That explains out-of-sequence drafting of #6/#8 but does **not** remove prerequisites from completion and acceptance.

## Milestones and exit criteria

| Ledger checkpoint | Required leaves | Outcome gate | Acceptance |
| --- | --- | --- | --- |
| **DIA-M0 — Documented basis** | DIA-001 | Owner reviews source-bound foundation and scope | Unknown; 1/1 supporting work Done |
| **DIA-M1 — Reproducible foundation** | DIA-002–DIA-005 | Source/licensing audit, local runtime activation, approved findings contract | Unknown; 1/4 supporting work Done |
| **DIA-M2 — Evaluated reviewers** | DIA-006–DIA-007 | Source-backed paired reviewer studies including legitimate negatives | Unknown; 0/2 supporting work Done |
| **DIA-M3 — Portable system** | DIA-008–DIA-010 | Skill composition, reversible consumer adoption and one suite release | Unknown; 0/3 supporting work Done |

No milestone can be accepted merely because an issue closes, a prompt exists, or CI validates metadata. No Pages deployment is requested; the [README graphic](../README.md#project-tracker) is the view.

## Mandatory work selection and update

The [AGENTS operating protocol](../AGENTS.md) governs selection: re-read the **actual** issues and PRs, canonical work records, dependency and blocker states; announce exact **ID + issue + milestone + expected deliverable**; stay within authorized scope. For unclear criteria, **announce a bounded detailing pass first**, preserve IDs and denominator, and ask for approval only when scope/authority changes.

At completion or blocker change: preserve prior evidence, update the ledger and linked issue, inspect the milestone, regenerate `README.md` and `assets/progress.svg`, run the native PRS validator and parity CI, then name the **next exact eligible issue**. GitHub issue/PR closure does not itself write or refresh these authoritative records.

Shared-system improvement: [Project Record Standard #3](https://github.com/interzettel/project-record-standard/issues/3).
