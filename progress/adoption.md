# Project Record Standard adoption plan

**Profile:** cold — newly created repository with LICENSE only (observed main on 2026-10-26). **Reference:** Project Record Standard v0.4.1 / contract 0.2.0, release commit `ebc6afb0b977ff3d7605893c73ac63021775c4d3`.

## Authority map

| Fact | Authoritative source (proposed) |
| --- | --- |
| Vision, scope and acceptance | `progress/overview.md`, accepted PR/decision records |
| Work definition and milestones | Future validated Project Record Standard ledger/manifest under `progress/` |
| Issue discussion, assignees, closure | GitHub issues |
| Skills and versioned contracts | `.agents/skills/`, `schemas/` in this repository |
| Experiments and evaluation evidence | Future versioned `evals/` fixtures and results |
| Release/publication | GitHub release and digest-backed artifact records |
| Consumer repository definitions | Consumer repo's canonical standards and ADRs, **never overridden by Diakrisis** |

## Adoption steps

1. Pin and inspect the v0.4.1 source kit and its license/digests.
2. Preview skill installation in a clean checkout; review changes to AGENTS and skill namespace, then apply without overwriting authored files.
3. Initialize new tracking records in empty staging directory using official CLI and merge only validated scaffold; keep first scope *unapproved*.
4. Reconcile GitHub issues and proposed work package IDs without double-counting.
5. Validate naming, denominators, milestones and changes with official CLI and CI.
6. Add optional branded view only after correct ledger, permissions and accessible presentation are proven.

**Rollback:** remove only files introduced by the reviewed PR/installer receipt; never run `init` over authored records or delete source history. Source of truth stays in this repo, project issue labels are projections/discussion.

**Status:** checked-in native ledger/manifest are present and the official v0.4.1 check and disposable installation passed in GitHub Actions. Required working scope has 1/10 completed leaves as of the recorded observation. Milestone acceptance, local runner discovery and release evidence remain pending. README-only presentation is selected; Pages and interactive site routes are not required.
## 2026-10-26 issue/ledger milestone reconciliation

All ten accounted GitHub issues (#1–#10) were re-read and given an explicit canonical `DIA-###`, PRS milestone `DIA-M#`, state, priority, prerequisites, and next evidence requirement. In the inspected GitHub issue metadata, **none has a native milestone assignment**. The API listing native milestone *objects* was unavailable; the PRS ledger remains authoritative for milestone mapping, not GitHub's issue milestone field. Owner-authorized issue-first workflow is now in `AGENTS.md`; cross-project template improvement tracked in [PRS #3](https://github.com/interzettel/project-record-standard/issues/3). `DIA-003 / issue #3 / DIA-M1` is the selected next available P0 package; `DIA-002` carries a Blocked flag with a specific final-verification dependency.

## 2026-10-26 PRS licensing clarification handoff

[DIA-002 / issue #2](https://github.com/interzettel/diakrisis/issues/2) now links the upstream [PRS license-decision issue #4](https://github.com/interzettel/project-record-standard/issues/4) and [unmerged MIT proposal PR #5](https://github.com/interzettel/project-record-standard/pull/5). **No permission or v0.4.1 coverage is yet confirmed.** The source-owner decision is separate from local Windows/Claude/Codex activation and independent archive digest verification, both deferred until the owner-directed final test phase. Required work stays **2/10**; DIA-M1 acceptance is still unknown.

## 2026-10-26 source-license approval reconciled

The repository owner expressly approved the MIT license and attribution for rights-controlled original Project Record Standard material, covering original source at the pinned historical `v0.4.1` revision. Upstream [PR #5](https://github.com/interzettel/project-record-standard/pull/5) merged; the licensing decision is available [here](https://github.com/interzettel/project-record-standard/blob/main/standards/LICENSING-DECISION.md). This **supersedes the earlier unapproved draft proposal** but does not change frozen v0.4.1 assets or third-party rights. DIA-002 remains active+blocked solely for owner-deferred independent archive verification and local Windows/Claude/Codex runtime checks. DIA-M1 not accepted; accounting remains 2/10.
