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

**Status:** checked-in native ledger/manifest are present and the official v0.4.1 check and disposable installation passed in GitHub Actions. Working scope now records **1/10 required leaves** (DIA-001 merged and verified). Milestone acceptance, local runner discovery, official release checksums, branding, and any hosted tracker remain pending. Owner's direction to proceed authorizes development, not acceptance of outputs.