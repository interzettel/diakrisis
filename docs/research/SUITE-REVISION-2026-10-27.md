# Suite revision research and decisions — 2026-10-27

**Scope:** shared evidence for the contract revision (DIA-005, fix plan PR-D), the skill revisions (DIA-006 and DIA-008, PR-F) and the evaluation design ahead of DIA-007 (PR-E), following the 2026-10-27 audit (its first fixes landed in PRs #35–#38). **Gate:** this is the fresh public-source pass that [RESEARCH-GATE.md](../RESEARCH-GATE.md) requires before a material revision. The per-skill records dated 2026-10-27 apply it to each skill. **No model was run**; behavioural evaluation stays deferred by the owner.

**Verification policy for this pass:** every standard's status and every quantitative claim below was checked online on 2026-10-27 against the source named, not taken from training data. Where a page could only be partly read, the limit is stated.

## Owner decisions

On 2026-10-27 the owner merged the Phase 1 fixes and delegated the open design decisions to the maintaining agent ("I trust you", in chat). The recommendations from the fix plan are therefore adopted:

| # | Decision | Adopted |
| --- | --- | --- |
| D1 | Versioning of the contract tightening | Wire `schema_version` 2 with a migration note; consumers keep their pinned revision-1 copies |
| D2 | Two meanings of "suggestion" | Keep the field name; define both senses in the contract and fix the skill wording |
| D3 | Category and severity vocabularies | Documented lists in the contract and in each skill; schema `category` stays free text; a test warns on categories outside the list |
| D4 | Default reviewers for scientific writing | `argument-review`, `method-review`, `terminology-review` (USAGE.md), with the coordinator aligned to it |
| D5 | Source of held-out evaluation cases | Safe copies of real documents plus owner-written cases; agent-written cases only as a labelled supplement (decided in PR-E) |
| D6 | Deterministic quote checker | Yes, repository-only, under DIA-005 |
| D8 | Grouping duplicates that quote different passages | Deferred until DIA-007 data exists |

D7 (whether Studio Zettlerei and interzettel are one owner or two roles) is a fact only the owner can state; it stays open.

## Verified sources

| Source | Status checked 2026-10-27 | Used for |
| --- | --- | --- |
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx) | Pinned commit `69ef37e` equals upstream `main` (last change 2026-08-09); no format change since the 2026-10-26 records. The agentskills.io site itself could not be opened from this session. | Frontmatter limits; progressive disclosure; references relative to the skill root, one level deep |
| [IEEE 1044-1993](https://standards.ieee.org/ieee/1044/1526) and 1044-2009 | 1993 edition superseded by 2009; 2009 listed as inactive-reserved by IEEE catalogue pages | No current general anomaly-severity standard to adopt |
| [ISO/IEC 20246:2017](https://www.iso.org/standard/67407.html) | Published, edition 1, last confirmed 2022, still current | Review process framing only; its full text (paywalled) was not read, so no severity scale is attributed to it |
| [Herr, Baumgartner, Gross (CHI 2016)](https://cml.hci.uni-bamberg.de/~gross/publ/chi16_herr_et_al_severity_rating_scales__proceedings.pdf) | Read | Severity ratings vary widely between evaluators; Nielsen's 0–4 scale produced higher ratings than other scales (preliminary, 103 participants) |
| [Sjøberg & Bergersen (EASE 2023)](https://arxiv.org/abs/2306.05336) | Read | Construct-validity threats (inadequate definition, under-representation, representation bias) versus internal, external and statistical-conclusion validity |
| [Bean et al., NeurIPS 2025](https://arxiv.org/abs/2511.04703v1) | Abstract read | 29 reviewers, 445 LLM benchmarks: weak construct validity is common |
| [Calvo Figueras & Agerri, critical questions benchmark (2025)](https://arxiv.org/html/2505.11341v3) | Read | No LLM above ~57% useful critical questions zero-shot; generic and templated questions; LLM judges without references agree poorly with humans (κ < 0.1) |
| [Li et al., LLM-as-a-Reviewer (2026)](https://arxiv.org/pdf/2605.25415) | Read | 12 LLMs, 898 papers: inflated ratings and confidence; under-flag clarity, over-flag reproducibility; hidden-instruction injection raised scores for 67–76% of low-scoring papers in weaker models |
| [Merits and defects of LLM review generation (2025)](https://arxiv.org/pdf/2509.19326) | Read | One model produced 59% fewer weakness entities than humans; weakness counts barely tracked paper quality (5.7% versus 50% for humans) |
| [CoCoReviewBench (ICML 2026)](https://arxiv.org/pdf/2605.07905) | First 100k characters read | Two-level aspect taxonomy (5 categories, 23 subcategories); AI reviews clearer but less correct and thorough |
| [Awuni et al., family-conditioned judge preference (2026)](https://arxiv.org/pdf/2609.17857) | Read | Same-family preference in LLM judges (score 0.067; 3.4–8.4 point lifts); 55% of AB/BA pairs reverse winners |
| [Zhao et al., non-existent citations (2026)](https://arxiv.org/pdf/2605.07723) | Read | 0.21–1.91% of references non-existent by August 2025, rising since 2023; existence checks scale, but checking whether a real source supports a claim remains hard |
| [van der Lee et al., INLG 2019](https://aclanthology.org/W19-8643.pdf) | Read | Randomise order, separate criteria, report agreement with confidence intervals. It does **not** explicitly recommend hiding system identity |
| [CONSORT 2025, Hopewell et al., BMJ 388:e081123](https://www.ideal-collaboration.net/wp-content/uploads/2025/12/CONSORT_2025_editable_checklist.pdf) | Checklist read | Item 20a: report who was blinded, including outcome assessors |
| [ISO 1087:2019](https://webstore.ansi.org/standards/iso/iso10872019) | Most recent edition, no amendments | Terminology vocabulary (unchanged) |
| [ISO 24495-1:2023](https://committee.iso.org/standard/78907.html), principles via [IPLF](https://www.iplfederation.org/the-iso-plain-language-standard-part1-and-part2) | Published 2023-06-20; further parts in development | Four principles: relevant, findable, understandable, usable |
| [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) | Working Draft dated 2026-10-25; SHACL 1.0 (2017) remains the Recommendation | Conceptual-model review must not treat 1.2 drafts as normative |
| Kalai et al., Nature 2026 (cited by the 2026-10-26 records) | Existence confirmed via a mirror of the same article number; content not re-read in this pass | Unchanged use |

## Findings that change the design

1. **Skills reference files outside their own folder.** The specification asks for references relative to the skill root, one level deep. All seven skills link three levels up to the shared contract, so a skill copied alone loses its definitions. Adding `references/` files would fix that but change the 19-file roster that the Spatial Laboratory bridge enforces. **Decision:** carry the short category list and the severity definitions inline in each `SKILL.md`; the contract stays authoritative; a test checks that the inline copies match the contract.
2. **No adoptable severity standard exists, and severity ratings are unreliable between raters.** **Decision:** keep the four schema levels, define each by its consequence for the reader's decision, require one clause naming that consequence, and keep severity separate from evidence status and confidence.
3. **The argument/method boundary has a published basis.** Construct-validity threats concern how a concept is defined and measured; internal, external and statistical-conclusion validity concern design and analysis. **Decision:** method-review owns defects in how a study was designed or measured; argument-review owns conclusions that go beyond what the reported design supports. When both apply, they are two findings with different causes, related but not grouped.
4. **LLM reviewers are lenient, generic and injectable.** They under-produce weaknesses, barely track quality, template their questions, and follow hidden instructions. **Decision:** keep the untrusted-data rule; add that instruction-like text addressed to a reviewer inside the material is reported as a finding, never followed; require every finding to name what the cited passage specifically fails to do, which rules out generic critiques.
5. **Same-family agreement is not corroboration.** **Decision:** unchanged coordinator rule, now with evidence; DIA-007 should use cross-family or human graders, judge both orders, and report reversal rates.
6. **Existence of a source is not support.** Fabricated references are rising and support mismatches are harder to detect. **Decision:** argument-review distinguishes `source-support-gap` from `unverifiable-source`; the quote checker (D6) verifies local quoted spans deterministically.
7. **Blinded grading needs its own authority.** The NLG guidance does not require hiding system identity; CONSORT 2025 item 20a treats blinding of outcome assessors as a reportable design property. **Decision:** PR-E cites CONSORT for blinding and van der Lee for randomisation, separate criteria and agreement reporting.

## Drafted shared vocabularies (to be finalised in PR-D)

**Severity**, by consequence:

- `informational`: no change is needed to keep the meaning or validity; context, a question, or an abstention.
- `minor`: a reader may be slowed or briefly misled, but the main claim, definition, method or decision survives as written.
- `major`: a main claim, definition, method step or decision is unsupported, contradicted or likely misread as written; fixing it changes what the text asserts.
- `blocking-candidate`: a result or decision that others rely on is invalid under the governing authority; the reviewer proposes resolving it before acceptance. This is never the Project Record Standard `Blocked` flag.

**Categories** per reviewer are drafted in each skill's 2026-10-27 record and collected in the contract by PR-D.

## Evaluation design implications (PR-E)

- Keep the eight cases that restate skill examples as a labelled "seen-example" subset; add held-out cases per D5.
- Graders blinded to which arm produced an output (CONSORT 2025 item 20a), order randomised, separate criteria, agreement with confidence intervals (van der Lee 2019).
- LLM graders only with reference answers, from a different model family, both orders judged, reversal rate reported (Calvo Figueras & Agerri 2025; Awuni et al. 2026).

## Limits of this pass

Paywalled standards were checked through catalogue pages only. The agentskills.io site was not reachable; the specification was read at its source repository. Two long papers were read partly (stated above). Nothing here is evidence that any Diakrisis skill performs well; it only grounds design choices.
