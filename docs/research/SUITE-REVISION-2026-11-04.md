# Suite revision 2026-11-04: lessons from DIA-007 round 3

**Date:** 2026-11-04.

**Scope:** a material revision of all seven skills, made under the [research gate](../RESEARCH-GATE.md). It changes the shared contract block, the hand-off sections of five specialists, one procedure step in argument-review and method-review, and one workflow step in the coordinator. It changes no schema, no category or severity vocabulary, and no contract revision.

**What was tested.** Round 3 tested the skills at the 2026-10-28 revision against a no-skill baseline, each on the owner's PDF and on its extracted text (24 runs, private material). These revised skills are untested until a new round runs them; round 3 results are not credited to them. Round 3 counts are in [DIA-007-ROUND-3-2026-11-04.md](DIA-007-ROUND-3-2026-11-04.md).

## Evidence that motivates each change

The source is two blind graders' per-finding verdicts (ChatGPT and a project-informed Claude), frozen before the arm key opened, mapped to arms afterwards. No owner document content is reproduced here.

| # | Observed in round 3 | Arm(s) | Change |
| --- | --- | --- | --- |
| L8 | A public record that describes less than the owner's account (a narrower role, one year for two events, fewer details) was still reported as a conflict, although the round 1 rule said such statements conflict only if both cannot be true. The same point recurred across versions. | Both | The shared block says outright that a record which says less is compatible with a fuller account and is not a finding; at most a coverage note. |
| L9 | Findings said a cited paper did not support, or was unclear about, a sentence; graders who read the full texts found the support in the body (methods, a discussion subsection, a future-work section). The reviewers had judged from titles or abstracts. | Skill | Argument-review and method-review require the relevant full-text passage before any support finding; an unopened full text is `not inspected` and gets no support finding. |
| L10 | Within one version, several specialists spent findings on the same problem. The largest family was one mislabelled question number, reported by terminology, conceptual-model, communication and consistency reviews in every version. Most repeats paired terminology with another review, or argument with method. | Both | Shared block: **one problem, one home**; a problem owned by another review is listed in coverage as `handed off to <review>` instead of using a finding slot. Terminology is named the home for labels that name two things or point to the wrong item. Argument-review hands design defects to method-review and keeps only the overclaim. |
| L11 | The coordinator's problem families grouped every within-version pair the graders marked as duplicates, with a few extra merges. Duplicates are a cost of the raw specialist output, not of the merged report. | Skill (coordinator run on both arms) | The coordinator keeps families and now also reads hand-off lines, so a handed-off problem no specialist reported becomes its own family instead of being lost. |

**Input format (no change).** PDF and extracted-text inputs performed about the same in round 3. The only findings graders tagged as extraction problems came from text runs that quoted a word as the extractor had joined it. No skill text changes for format; `tools/check_spans.py` gained a `found-dehyphenated` status (PR #57).

Graders' verdicts are a reason to revise, not ground truth; both graders are project-informed and one shares the reviewers' model family.

## External sources checked on 2026-11-04

- **Compatible versus conflicting statements (L8).** Stanford Encyclopedia of Philosophy, "The Traditional Square of Opposition", substantive revision 19 May 2025 (https://plato.stanford.edu/entries/square/): contraries cannot both be true; subcontraries can both be true. A narrower description and a fuller one can both be true, so neither contradicts the other. {fact: definitions; the application is expert inference}
- **Absence of evidence (L8).** Altman and Bland (1995), *BMJ* 311:485 (https://www.bmj.com/content/311/7003/485), as in the 2026-10-28 record. {fact}
- **Abstracts misstate bodies (L9).** Pitkin, Branagan and Burmeister (1999), "Accuracy of data in abstracts of published research articles", *JAMA* 281(12):1110 to 1111 (https://pubmed.ncbi.nlm.nih.gov/10188662/): 18% to 68% of abstracts across six general medical journals had data inconsistent with or absent from the body. {fact}
- **Quotation errors (L9).** Jergas and Baethge (2015), "Quotation accuracy in medical journal articles: a systematic review and meta-analysis", *PeerJ* 3:e1364 (https://peerj.com/articles/1364): total quotation error rate 25.4% (95% CI 19.5 to 32.4), major errors 11.9%; the authors advise checking statements against original papers. {fact: medical literature; transfer to other fields is expert inference}
- **Division of labour between agents (L10).** Anthropic, "How we built our multi-agent research system", 13 June 2025 (https://www.anthropic.com/engineering/multi-agent-research-system): "Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information"; each subagent needs "clear task boundaries". {fact: one practitioner report, not a controlled study}

## Decisions

- **Adopted:** L8 to L11 as narrow instructions above.
- **Rejected:** telling specialists to drop out-of-scope problems silently. A hand-off line keeps the observation visible when a skill runs alone.
- **Rejected:** restricting the suite to PDF input. Round 3 shows no format effect large enough to justify it.
- **Deferred:** a schema field for hand-offs. `limitations` carries them for now; a field would need a contract revision.

## Controls

- **Positive:** a label that points to the wrong numbered question is reported once, by terminology-review; other reviews list it as handed off.
- **Negative:** a public page listing a narrower role than the owner's account produces no finding.
- **Abstention:** a cited paper whose full text cannot be opened is `not inspected`, with no support finding.

**Behavioural status:** untested until a new round.
