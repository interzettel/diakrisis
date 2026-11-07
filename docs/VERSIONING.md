# Versioning the Diakrisis skill package

**Decision (2026-10-26): one version for the complete skill suite.** No separate SemVer numbers, tags or publication channels for individual reviewer skills.

The reviewers are designed to work together and share one finding contract. Simpler accounting is preferable until independent releases become a demonstrated need.

**Superseded proposal:** [issue #14](https://github.com/interzettel/diakrisis/issues/14) (*Specify versioning and compatibility for individual Agent Skills*) was closed as "completed" after [PR #15](https://github.com/interzettel/diakrisis/pull/15) shipped an initial version registry. The owner then requested simplification, and [PR #16](https://github.com/interzettel/diakrisis/pull/16) replaced per-skill versions with this single-suite policy. Read #14 as historical context, not as a per-skill versioning decision.

## Single version source

`skills/versions.json` owns the version of the **whole Diakrisis package** (`suite.version`). It also lists which skills are actually included in that package and which are merely draft proposals. These lists contain skill *names and status*, not individual versions.

- `0.1.0-dev.0` is a development version, **not a published release**.
- `SKILL.md` frontmatter follows the [Agent Skills specification](https://agentskills.io/specification). `name` and `description` are required; individual `metadata.version` is **not needed**.
- A draft PR may supply an experimental skill but does not make it included in `main` or publish the package.
- When reviewer skills or their shared contracts change, the next **package** version is proposed, tested and released as one consistent collection.

## Release policy

| Change | Impact on suite version |
| --- | --- |
| Incompatible finding/authority contract or behavioral API | Major |
| New compatible reviewer, workflow or capability | Minor |
| Compatible correction of review guidance or schemas | Patch |
| Work in progress | `-dev.N` / `-rc.N`, without implying publication |

Before `1.0.0`, document potentially breaking changes explicitly. A release is a GitHub Release with a reviewed immutable `vX.Y.Z` tag, source revision and artifact digests. A Git merge, change log, successful unit test or an author's approval is **not** by itself release evidence.

Consumers pin an exact suite tag/commit/checksum and can upgrade the complete package together. Version compatibility and experimental quality are documented at the **suite level**; skill-specific behavioral tests remain independently inspectable but do not create individual release versions.

## Quality gates before any suite release

1. Metadata/Agent Skills format validation of each included skill.
2. Shared findings contract validation and deterministic tests.
3. Matched with-skill/without-skill agent evaluation on realistic, positive, negative and unfamiliar cases, including human adjudication and honest limitations.
4. Composition tests where multiple included skills operate together.
5. Approved source/privacy boundaries and a reversible consumer installation procedure.
6. Publication and checksum receipts.

A skill can be **experimental** while included in development builds; released suite descriptions must state which behaviors were actually evaluated. Never invent accuracy or run receipts.

## Current package

**`0.1.0`, released 2026-11-07, experimental.** The first GitHub Release of the suite: tag `v0.1.0`, the seven skills, contract revision 2, and a consumer bundle with SHA-256 digests attached to the release.

**Gates (owner decision, 2026-11-07).** Gates 1, 2, 4 and 6 are met by the repository checks and the release receipts. Gate 5 is met for the documented consumer procedure. **Gate 3 is waived by the owner:** with-skill and no-skill runs were compared on the owner's real documents in three blinded rounds ([EVALUATION.md](EVALUATION.md)), but graded by agent graders, not by a person; recall against an owner problem list was not measured; the 2026-11-04 revision included in this release has not been evaluated. Nothing in this release claims validated review quality.

**Version choice.** `0.1.0` is the first public number after `0.1.0-dev.0`; the contract moved to revision 2 during development, so there is no earlier release to be incompatible with.

**Before `0.1.0`:** `0.1.0-dev.0` was the unreleased development version that consumers pinned by commit. Pinned consumers keep working until they choose to move to the tag.

There is no GitHub Pages deployment for Diakrisis. The repository README tracker is a projection of governed project records, not a release channel. This is a deliberate small-project tailoring of the [Project Record Standard](https://github.com/interzettel/project-record-standard).
