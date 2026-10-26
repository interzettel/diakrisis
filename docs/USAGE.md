# Using the Diakrisis skill suite

**Package:** `0.1.0-dev.0` — seven *experimental* modules, versioned and shipped together. **No production release, hosted service, Pages deployment or demonstrated model-effectiveness claim.**

The open [Agent Skills format](https://agentskills.io/specification) makes these skills portable instructions. A host agent must **discover and invoke** them; merely committing the folders doesn't ensure activation in every runtime. Use the repository's [project-scoped installation process](INSTALLATION.md) and inspect the runner's available skills before relying on automatic triggering.

## Profiles (routing guidance)

| Use case | Default set | Add only if needed |
| --- | --- | --- |
| **Scientific writing / research agents** | `argument-review`, `method-review`, `terminology-review` | `conceptual-model-review` for conceptual schemas, `communication-review` for clarity, `consistency-review` across files |
| **Personal / creative writing** | `communication-review` | `terminology-review` for deliberate concept systems; other reviews only by request |
| **Project charters / agentic stack** | `consistency-review`, `conceptual-model-review`, `terminology-review` | `argument-review` for justified decisions and `communication-review` for readership |
| **Spatial Laboratory studies** | `method-review`, `argument-review` | `conceptual-model-review` for spatial semantics and `consistency-review` against preregistration |

**The coordinator chooses the minimum relevant set**; it doesn't automatically launch seven isolated models or treat a single model's multiple opinions as independent evidence.

## Example requests

For a scientific manuscript:

> Use Diakrisis `review-coordinator` to inspect the provided draft for claim/evidence alignment, operationalization, and terminology. Cite exact source passages, mark unknowns, and suggest changes without modifying the draft.

For a project charter:

> Compare the current README, charter and governing ADRs. Use Diakrisis conceptual-model and consistency reviews; identify only genuinely concurrent contradictions, distinguishing task state from flags and source authority from derivative summaries.

For personal writing:

> Use Diakrisis communication-review, preserve my voice and purposeful unconventional phrasing, and offer only edits that make the intended audience's reading clearer.

For a very narrow question, invoke a named reviewer directly rather than the coordinator.

## A good review request supplies

- Artifact(s), exact available revision, and an explicit accessible scope; protect confidential material.
- Intended domain/audience/language and author-preferred style.
- Local canonical definitions, ADRs, protocols, glossary and precedence rules.
- Desired output: compact prose findings or source-linked records conforming to `schemas/finding.schema.json` where honest.
- What the review **must not do**, especially automated edits, commits or publication.

## How findings work together

1. The coordinator identifies relevant specialists and the governing sources.
2. Each specialist names exact affected spans, the supported or uncertain claim, the relevant evidence and the least intrusive suggestion.
3. Findings about the **same underlying defect** are deduplicated; their differing reasons remain visible.
4. Unresolved authority conflicts and inaccessible sources remain explicitly undecided.
5. Only the human owner or authorized downstream workflow decides to accept, apply, publish or release a change.

The suite never changes a manuscript or project repository simply because a critique was generated. `findings` being empty is *not a certification*.

## Integration boundary

- [Writing Kitchen](https://github.com/yigit-denktas/writing-kitchen) retains authorship, its concept graph and typed judges. Diakrisis supplies optional critiques.
- [Spatial Laboratory](https://github.com/yigit-denktas/spatial-laboratory) retains preregistration, raw experiment records and research acceptance.
- [Project Record Standard](https://github.com/interzettel/project-record-standard) retains source authority for ledger counts, acceptance and status flags; Diakrisis can flag contradictory wording.
- [Personal Agent Stack](https://github.com/interzettel/personal-agent-stack) retains action authorization, secrets and runtime capabilities.

No cross-repository integration has yet been installed or tested. Use reviewed independent PRs later; do not copy private fixtures into this public repo.

## Deferred verification

At the user's request, live model comparisons, test infrastructure expansion and client-activation verification will be handled **after** the cohesive package is implemented. Existing CI can still catch broken metadata, invalid project records and stale README projections. Current skills are development quality only; there are no reported accuracy metrics.

See [foundation](FOUNDATION.md), [review finding contract](REVIEW-CONTRACT.md), [single package versioning](VERSIONING.md) and [source records](research/).
