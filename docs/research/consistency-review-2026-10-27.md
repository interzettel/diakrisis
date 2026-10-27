# Consistency review: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** contradictions between concurrently applicable artifacts about the same referent, time and scope. **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](consistency-review-2026-10-26.md).

## Sources checked for this revision

- Project Record Standard [STANDARD.md at the pinned v0.4.1 commit](https://github.com/interzettel/project-record-standard/blob/ebc6afb0b977ff3d7605893c73ac63021775c4d3/standards/STANDARD.md): a regenerated projection cannot make an old observation fresh; missing, unknown and zero are distinct.
- The 2026-10-27 audit of this repository, as a worked case: a documentation promise contradicted by code (checker roster), stale derived README dates, and status claims left behind after state changes.

## Observed, uncertain, contradicted

- Observed: the most consequential inconsistency found in Diakrisis was documentation versus implementation, a kind the current skill does not name explicitly.
- Observed: stale projections and dated observations embedded in standing rules recur; both are distinct from contradictions between canonical records.

## Decisions

- **Adopt categories:** `concurrent-contradiction`, `stale-derived-projection`, `status-drift`, `version-drift`, `documented-behavior-vs-implementation`, `authority-unresolved`.
- **Name implementation drift explicitly:** when a document states how code behaves, the code is an inspectable artifact; a contradiction can be confirmed by reading or running it.
- **Inline** categories and severity definitions in `SKILL.md`.

## Licences and security

No external code imported. Cross-repository reads still require authorization.

## Controls

- Positive: `COMPATIBILITY.md` promised older consumers would be reported as updatable while the checker rejected them → `documented-behavior-vs-implementation`, confirmed by reproduction.
- Negative: a changelog preserving a superseded label → no finding.
- Abstention: two undated policies, no designated authority → `authority-unresolved`, `needs-clarification`.

## Evaluation status

Deferred by the owner to DIA-007.
