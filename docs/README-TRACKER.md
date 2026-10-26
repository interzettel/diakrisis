# README-only project tracking

**Host:** GitHub repository README. **Dedicated website / GitHub Pages:** not required and not configured.  
**Standard:** pinned Project Record Standard v0.4.1, record contract 0.2.0.

## Authority and presentation

- `progress/ledger.json` owns bounded work items, states, evidence, priorities, dependencies and milestone gates.
- `progress/project-record.json` owns project identity, source observation and selected `host` renderer.
- `progress/history/` retains source snapshots and scope changes; changing the denominator is not hidden.
- `skills/versions.json` owns suite/package version status, distinct from project progress.
- `README.md` generated marker and `assets/progress.svg` are **derived views**; neither becomes another authoritative completion ledger.
- Issues own discussion and closure, not work accounting; PRs and CI receipts supply evidence, not automatic milestone acceptance.

## Read the view

At the top of the README, the scoped graphic shows named fractions/percentages from the official Project Record Standard calculator, not an estimate. Below it are exact milestone work fractions, acceptance states (including **unknown**), every accounting leaf, stable issue links, dependencies, next gates and draft skill versions. All data appears as Markdown for readers who cannot view the SVG.

The graphic is the original Project Record Standard README renderer, using Diakrisis-specific colours and typography. The added table is a local small-project view; **no JavaScript, Pages route, or hosted website is necessary**.

The source observation date is *not* the generation time. Re-running CI does not imply external GitHub issue reconciliation or advance the observation timestamp.

## Regenerate after a scoped change

In a checkout with the pinned submodules:

```sh
git submodule update --init --recursive
python tools/sync_readme.py --write
PYTHONPATH=tools/upstream/project-record-standard/src python -m project_record check --config progress/project-record.json
python tools/sync_readme.py --check
python tools/check_skill_versions.py
```

Review the resulting README/SVG diff together with the ledger and source history, commit them **in the same PR**, and let CI verify byte-for-byte parity. `--check` fails when generated files are stale and does not change source files. Outside the managed markers, the README is author-owned and preserved.

A failing parity gate does not authorize automated changes to the ledger, issue closure or source state. No recurring workflow polls GitHub; user instructions or explicit bounded updates change the canonical records.

## What keeps this current

Every PR runs official Project Record Standard ledger validation, scope-history checks, package version integrity, and `sync_readme.py --check`. A PR modifying ledger/manifest/versions without updating README and SVG will fail the parity gate. This prevents *known source-to-view drift after a merge*, but cannot promise the record itself is live with GitHub or silently fetch new issue states.

## Publication / versioning

GitHub `main` README is a source-controlled status view, **not a release or deployment channel**. No Pages workflow, URL, site or web runtime is installed. Reusable skills are released independently under [per-skill versioning](VERSIONING.md) after separate behavioral evaluation and review.
