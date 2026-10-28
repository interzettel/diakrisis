# Suite revision 2026-10-28: lessons from DIA-007 round 1

**Date:** 2026-10-28.

**Scope:** a material revision of all seven skills, made under the [research gate](../RESEARCH-GATE.md). It changes the shared contract block and one procedure step in each of five specialists and the coordinator. It changes no schema, no category or severity vocabulary, and no contract revision.

**What was tested.** [Round 1](DIA-007-ROUND-1-2026-10-27.md) tested the skills at `654f5ee`. These revised skills are untested until a new round runs them; round 1 results are not credited to them.

## Evidence that motivates each change

The source is the blind graders' per-finding verdicts and their written feedback in round 1, mapped to arms after unblinding. No owner document content is reproduced here.

| # | Observed in round 1 | Arm(s) | Change |
| --- | --- | --- | --- |
| L1 | A correct diagnosis came with a remedy that would create a new problem. One fix replaced the author's construct with an easier count; another excluded participants who had been interviewed, which creates selection; another demanded an extra experimental arm without its identification assumptions. | Both | The shared block adds a **remedy check**. Method-review and conceptual-model-review name construct substitution and post-treatment selection explicitly. |
| L2 | A public role description was read as contradicting the owner's confirmed account. The two descriptions were compatible. | Both (one finding each) | The shared block states the **evidence hierarchy**: what the owner has confirmed outranks a public record's silence or different wording, and two statements conflict only if both cannot be true. Consistency-review repeats the test at its comparison step. |
| L3 | Evidence the reviewer could not open was treated as missing from the record. | Baseline | The shared block now requires `not inspected` plus a bounded verification request. This extends the existing "coverage gap" rule. |
| L4 | A documented historical mechanism was asked for a controlled comparison. | Baseline | Argument-review matches the required evidence to the claim type: description, causal estimate, normative argument or recollection. |
| L5 | A counterexample from a different kind of programme was used as a direct test. | Baseline | Argument-review counts a counterexample only when it is comparable or a link is shown. |
| L6 | A reflective essay was pushed toward a research report's repeated thesis, and a clarity rewrite would have turned an illustrative calculation into an observed result. | Both | Communication-review protects genre. A clarity edit must not change the status of a claim. |
| L7 | Overlapping findings inflated the apparent number of distinct problems. | Both (expected, since the arms overlap by design and the coordinator was not run) | Review-coordinator presents **problem families**: one entry per underlying problem, listing every contributing finding ID, and counts families, not findings. |

Graders were project-informed AI assistants: the essays' editor, and ChatGPT for the proposal. Their feedback is a reason to revise, not ground truth. Each change below is a narrow instruction aimed at a behaviour both a grader and the arm mapping identified.

## External sources checked on 2026-10-28

- **Post-treatment selection (L1).** Montgomery, Nyhan and Torres (2018), "How conditioning on posttreatment variables can ruin your experiment and what to do about it", *American Journal of Political Science* 62(3), 760 to 775 ([IDEAS record](https://ideas.repec.org/a/wly/amposc/v62y2018i3p760-775.html)). Excluding units because of something that happened after assignment, such as being interviewed, can bias a randomised comparison. {fact: published result; its application to a given design is expert inference}
- **Construct substitution (L1).** Shadish, Cook and Campbell (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*: construct validity concerns whether the operations represent the intended construct. A count that is easier to collect can under-represent it. {fact: standard reference; checked as a catalogue record, not reread in full}
- **Absence of evidence (L3).** Altman and Bland (1995), "Absence of evidence is not evidence of absence", *BMJ* 311:485 ([BMJ](https://www.bmj.com/content/311/7003/485)). {fact}
- **Comparability of counterexamples (L5).** Pearl and Bareinboim (2014), "External validity: from do-calculus to transportability across populations", *Statistical Science* 29(4) ([doi:10.1214/14-STS486](https://doi.org/10.1214/14-STS486)). Results transfer between settings only under stated assumptions about how the settings differ. {fact: published framework; its use here is an informal analogy}
- **Remedies can make things worse (L1, L6).** Huang et al. (2024), "Large Language Models Cannot Self-Correct Reasoning Yet", ICLR 2024 ([arXiv:2310.01798](https://arxiv.org/abs/2310.01798)): unprompted model "corrections" can degrade correct answers. This supports checking a proposed change rather than trusting it. {expert inference: an analogy from reasoning tasks to editorial remedies}

## Decisions

- **Adopt L1 to L7** as instructions in skill text. They come from round 1 behaviour, are each limited to one or two sentences, and do not change the schema.
- **Reject** adding new categories (for example `unsafe-remedy`). An unsafe remedy is a property of a finding's proposed change, not a separate defect in the text. A category would also need contract revision 3.
- **Defer** a schema field recording the remedy check. Prose first; a field only if round 2 shows the instruction is followed but invisible.
- **Defer** owner-document examples in skill text. Owner material stays private, so the examples stay generic.

## Controls for round 2

**Positive controls.** A diagnosis the graders agreed with should still be reported, with a remedy that preserves the construct and the commitments.

**Negative controls.** These should produce no finding, or a question instead:

- a compatible role description;
- a public record that is merely silent;
- a historical account without a controlled comparison;
- a reflective essay that reaches its thesis late.

**Abstention.** Where no safe remedy exists, ask a question.

**Round 2 status.** A fresh paired round on a cleaner manuscript (the owner's v7.6 proposal) is registered separately, before it runs.
