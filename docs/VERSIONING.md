# Skill package and suite versioning

**Initial policy:** 2026-10-26. **Status:** chosen release policy; releases and agent-behavior certification remain pending.

Diakrisis uses the Agent Skills open format but does **not** assume all skill modules share one version. Project Record Standard v0.4.1 / contract v0.2.0 supplies the governance distinction between work acceptance, version plan, published release and observed downstream installation.

## What is versioned

| Unit | Canonical version source | Release convention |
| --- | --- | --- |
| Each Diakrisis skill | `metadata.version` in its `SKILL.md`; mirrored by a checked `skills/versions.json` entry when the skill is on `main` | Independent semantic versions (`MAJOR.MINOR.PATCH`, optional prerelease) |
| Diakrisis suite | `skills/versions.json:suite.version` | `vX.Y.Z` release tag only after acceptance; pre-releases use `-dev.N`, `-rc.N` |
| Shared finding contract | JSON Schema `$id` and explicit schema version | Version independently when consumer-visible fields or meanings change |
| Agent Skills runtime format | Pinned upstream source plus validated metadata | External compatibility requirement; not an invented internal API version |
| Downstream installation | Consumer's pinned source/release commit/digest | Never silently follow `main` or a mutable branch |

## Version rules

1. Before a release, skills may carry versions like `0.1.0-draft`, and metadata `maturity: experimental`; these are **not published releases**. Record draft PR and its actual source ref in `candidates`.
2. On the first accepted release of a skill, move it to `skills` with version equal to `SKILL.md` `metadata.version`, a path on `main`, and versioned evidence/compatibility. A passing frontmatter linter is not an effectiveness certification.
3. Bump **major** when changing reviewer authority, outputs, semantics, or incompatible schemas; **minor** for backward-compatible new capabilities; **patch** for corrections preserving interfaces. Before 1.0, explicitly document compatibility instead of assuming stable APIs.
4. Record required Agent Skills spec source, tested client runtimes/models and result limitations for each release. Individual skill versions can differ; suite version captures a tested compatible collection.
5. Author a change fragment for meaningful behavior/contract changes. Update a human-readable changelog as a derived publication history; distinguish merged change, accepted functionality, tagged release and observed downstream installation.
6. Tag releases at immutable commits (suggested `skill/<name>/vX.Y.Z` for individual packages; `vX.Y.Z` for suite). Published ZIPs should include license, source revision and file digests.
7. Consumer repositories choose when to upgrade. Record exact version and checksum; regression checks and reversible migrations are required.
8. A project with no shipped skill must report **zero released skills**, not an invented v1.

## CI obligations

`tools/check_skill_versions.py` verifies structured manifest fields and confirms that any `skills` entries actually exist on `main`, have corresponding `SKILL.md` metadata and unique names. Proposed `candidates` cannot be mistaken for releases.

Diakrisis has **no GitHub Pages deployment**; README-only progress is a tailored presentation choice and not a release channel. CI artifacts are verification evidence, not publication.

## Current candidates

- `terminology-review`: prototype `0.1.0-draft`, draft PR #12, structural CI only, behavioral evidence pending.
- Remaining specialist skills: not yet authored and therefore no artificial package versions.

This structure is tailored to a small modular skills toolkit. Project Record Standard governs *meaning, evidence, and source authority*, not one directory hierarchy imposed across all repos.
