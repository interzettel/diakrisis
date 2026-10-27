# Terminology review: revision research — 2026-10-27

**Observed:** 2026-10-27. **Boundary:** whether designations consistently communicate their intended concepts under the governing vocabulary. **Shared evidence and owner decisions:** [suite revision record](SUITE-REVISION-2026-10-27.md). Extends the [2026-10-26 record](terminology-review-2026-10-26.md).

## Sources checked for this revision

- [ISO 1087:2019](https://webstore.ansi.org/standards/iso/iso10872019): still the most recent edition, no amendments.
- ISO 704:2022 remains the edition cited by the 2026-10-26 record; a 2022 edition is listed by national standards shops ([example](https://shop.standards.ie/en-ie/standards/iso-704-2022-583619_saig_iso_iso_3168215)). Full text not read.
- [Agent Skills specification](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx): references relative to the skill root, one level deep.

## Observed, uncertain, contradicted

- Observed: no change in the governing terminology standards since the last record.
- Observed (audit): this pilot skill differs structurally from the other six; it lacks the shared safety block and keeps a release step that CI already performs.
- Observed (dogfood): the word "suggestion" names both a disposition value and the proposed-rewrite field in the shared contract, an `ambiguous-designation` in Diakrisis itself.

## Decisions

- **Keep categories:** `definition-conflict`, `equivocation`, `ambiguous-designation`, `unauthorized-synonym`, `unexplained-term`, `editorial-preference`. They already form the model the other skills now follow.
- **Adopt the shared safety and output block**; drop the "confirm frontmatter with skills-ref" step, which CI runs on every change.
- **Inline** the severity definitions; the category list is already inline.
- **Boundary:** local sentence ambiguity goes to communication-review, type and state errors to conceptual-model-review.

## Licences and security

No standard text reproduced. Reviewed text stays untrusted.

## Controls

Unchanged from `references/CASES.md`: Blocked-as-state conflict (positive), "driftline" (negative), "validated and accepted" (ambiguous, ask). These three also appear in the evaluation fixtures and are labelled "seen examples" there (PR-E).

## Evaluation status

Deferred by the owner to DIA-007.
