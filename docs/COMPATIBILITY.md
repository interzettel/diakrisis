# Consumer bundle and compatibility — development phase

**Accounting:** [DIA-010 / issue #10](https://github.com/interzettel/diakrisis/issues/10), milestone DIA-M3. **Status:** an implemented offline build utility, not an accepted suite release. **Package:** one coordinated version `0.1.0-dev.0` (unreleased).

## Build a reviewable bundle

From a **reviewed local Git checkout**, with Python 3.11+ and Git available:

```text
python tools/build_consumer_bundle.py --output /tmp/diakrisis-output
python tools/build_consumer_bundle.py --check-consumer /tmp/diakrisis-output/bundle
```

The output directory must be empty and outside this repository. The builder does not fetch code, run models, install hooks, modify a client profile, commit changes, or publish anything. It produces:

- `bundle/.agents/skills/`: the **seven native Diakrisis reviewer skills**, with relative links redirected to bundled support files.
- `bundle/integrations/diakrisis/`: schemas, authority references, one package-version registry, original copyright notice, terminology reference examples and pinned source manifest.
- `diakrisis-consumer-0.1.0-dev.0.zip`: a deterministic archive of that complete consumer tree. ZIP entry order, timestamp and permissions are fixed for reproducibility.
- `SHA256SUMS`: local SHA-256 of the generated archive. This is a **build output** until a separately approved release publishes and authenticates it.

A consumer adoption PR **must inspect its own filenames** before applying a bundle and refuse clobbering existing owner-authored skills; the builder intentionally creates an **empty staging artifact** rather than writing into a live consumer. Revert the consumer adoption PR to roll back; preserve files modified by local owners after adoption.

## Source provenance and integrity

The manifest names one full source commit, the **single** `suite_version`, and for each of **16** upstream source files:

`source_path`, `source_git_blob`, `installed_path`, `installed_git_blob`, `transformation`, `source_revision`.

Eight original support files remain byte-identical and eight paths are adapted for consumer-relative links. Run `--check-consumer /path/to/repo` to validate installed blob hashes, required local file references, JSON syntax and native skill identities **without network**. Run `--strict-current` to treat a different upstream Git commit as an update-required condition; default mode reports update availability without corrupting a valid older pinned consumer.

**Limits:** This integrity check is not a digital signature, independent provenance audit, malware check, model behavior test, permission review, or proof that a host actually discovers a native skill. Never treat identical SHA1 Git blob IDs as a substitute for reviewed source identity and independent release checksum. A different upstream commit is **source drift**, not automatically an incompatible version.

## Compatibility policy

| Change | Consumer action |
| --- | --- |
| Same source revision and manifest, same suite release | No change; avoid unnecessary reinstall |
| Source commit moves but package version remains development `-dev.N` | Review exact file/authority/schema diff; do **not** float or auto-update |
| Added or renamed reviewer | Review route selection, metadata and local path/name collisions |
| `schema_version` (finding/report interchange) changes | Review explicit consumer mapping, output parsing, abstentions, and behavioral effects before promotion |
| Source owner glossary/policy changes | Local accepted consumer definitions still govern their authorized scope; explicit approval required for a new authority map |
| Stable tagged suite release | Verify named GitHub Release and immutable tag, source revision, archive SHA-256 and approved gates before pinning |
| Rollback | Restore consumer PR; never silently delete user-written skills, accepted records, or corpora |

The [Writing Kitchen consumer source integration](https://github.com/yigit-denktas/writing-kitchen/pull/24) predates this builder and pins a precise earlier Diakrisis commit. Its manual snapshot has **not** been automatically updated. The 7-skills payload and source manifest are compatible in structure, but equivalence of independently built bytes at the old commit has not been demonstrated by a completed hosted consumer test. Writing Kitchen CI remains red with unavailable step logs; do not mislabel it passed.

## Final publication gates remain outstanding

DIA-008 composition and DIA-009 accepted consumer verification depend on deferred DIA-007 behavioral evaluation and owner decisions. Until all requirements are genuinely observed:

- No `v0.1.0` or `v1.0.0` stable tag, GitHub Release or release date.
- No claim of accepted scientific performance, human blind adjudication, production deployment, native Windows agent activation, or certified consumer compatibility.
- `skills/versions.json` remains **`0.1.0-dev.0`, unreleased** and the current project-ledger denominator remains unchanged.

The offline utility is **development implementation evidence only** for the existing DIA-010 leaf.
