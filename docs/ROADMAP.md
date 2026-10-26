# Roadmap and work packages

**Recorded:** 2026-10-26. **Status:** ten-package working scope approved for development on 2026-10-26; one foundation leaf (DIA-001) completed through merged PR #11. This does not establish any milestone acceptance. Native PRS v0.2.0 ledger validated separately.

The project follows [Project Record Standard v0.4.1](https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1), contract 0.2.0, for terminology, stable IDs, separate completion and acceptance, evidence, and scope changes. Its installer preview/apply and official ledger check succeeded in isolated GitHub Actions CI on 2026-10-26; Windows/Claude/Codex runtime discovery, owner scope acceptance, and hosted tracker remain unverified.

**Prerequisite for any additional reviewer:** complete the [research gate](RESEARCH-GATE.md) before skill implementation or material revision; source-refresh and matched baseline/treatment evaluation are independent gates.\n\n## Sequencing and gates

| Order | Package | Priority | Completion gate | Depends on |
| --- | --- | --- | --- | --- |
| 0 | **DIA-001 Persist foundation** | P0 | Research, README, scope, provenance and unresolved decisions versioned | — |
| 1 | **DIA-002 Establish project records** | P0 | PRS pinned, installation preview/check, manifest, ledger, named milestone gates, verification receipts | DIA-001 |
| 2 | **DIA-003 Audit upstream skill standards and donors** | P0 | Agent Skills spec reviewed; Superpowers, Anthropic skill-creator, scientific skills inventoried with licenses/revisions | DIA-001 |
| 3 | **DIA-004 Integrate authoring toolchains** | P1 | Verified source/pin and secure install of Superpowers + skill-creator into a supported runtime; do not overwrite other skills | DIA-003 |
| 4 | **DIA-005 Define common finding contract** | P1 | Versioned schema and authority rules with validation, examples and negative controls | DIA-002, DIA-003 |
| 5 | **DIA-006 Implement three pilot reviewer skills** | P1 | Terminology, conceptual-model, argument reviews conform to spec; baseline and post-skill evals; independent adjudication | DIA-004, DIA-005 |
| 6 | **DIA-007 End-to-end research and writing pilots** | P1 | Tests on copies of real project documents; source spans, abstentions and false-positive metrics audited | DIA-006 |
| 7 | **DIA-008 Expand remaining skills and coordination** | P2 | Method, communication, consistency, coordinator; conflict-resolution tests | DIA-007 |
| 8 | **DIA-009 Cross-repo adoption** | P2 | Optional bounded PRs with consumer authority, integration tests, rollback | DIA-007 |
| 9 | **DIA-010 Release, update and drift policy** | P2 | Versioned release, pinned adoption, compatibility matrix, upstream watch policy | DIA-008, DIA-009 |

**Priority rules:** P0 = blocks trustworthy bootstrap; P1 = next required work; P2 = subsequent scoped work; P3 = investigation/deferred. Proposed priority is not a declaration of issue-state completion.

## Milestone proposals

- **M0: Documented basis** — DIA-001 evidence reviewed, scope proposed and open questions visible.
- **M1: Reproducible foundation** — DIA-002 through DIA-005; verified standard and toolchain, authoritative record and evaluation contract.
- **M2: Tested minimum viable reviewers** — DIA-006 and DIA-007; positive and negative controls; human adjudication.
- **M3: Portable system** — DIA-008 through DIA-010; cross-repository integration, maintainability, releases.

Milestones are **acceptance gates**, not tasks or percentages. No milestone is accepted by the existence of this plan.

## Decisions to resolve

- Whether the initial scope of ten packages and three pilot reviewers is accepted.
- Which local runtime(s) are the first installation targets (Claude Code, Codex, or both).
- How findings are adjudicated when project definitions and external standards disagree.
- Which validation thresholds are release-blocking; avoid invented reliability metrics.
- Public/private boundary for experimental documents, source quotations and agent telemetry.

## Immediate next move

Finish source verification and install/validate Project Record Standard in a **clean staging checkout**. Inspect changes, then create the authoritative manifest/ledger. After that, integrate upstream authoring tools and run *baseline* tests before shipping skills. GitHub issues can record delivery discussions; they must not become a competing authoritative completion ledger.
## Owner-approved build-first sequencing — 2026-10-26

All seven specialist/coordinator skill modules were authored and merged in [PR #17](https://github.com/interzettel/diakrisis/pull/17) on 2026-10-26, before any further model test infrastructure or behavioral evaluation. Each module has a dated pre-implementation web-source record in `docs/research/`. Structural packaging checks remain in CI. No DIA-006, DIA-007, or DIA-008 completion or milestone acceptance is inferred from authored instructions or the merge; comparative evaluations and integrated behavioral checks remain **deferred until the owner-directed final test phase**, at the owner's direction. Suite SemVer applies to the **whole package only**, not individual modules.
