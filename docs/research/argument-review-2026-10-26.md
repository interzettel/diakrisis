# Argument review: source review before implementation

**Observed:** 2026-10-26. **Scope:** Claim–grounds–warrant reasoning and epistemic restraint. **Gate:** pre-implementation design only; model testing explicitly deferred by owner. **Source policy:** inspect linked primary materials where public; do not claim access to paid standards or validation from cited material.

## Checked external sources

- [Hitchcock (2006), Good Reasoning on the Toulmin Model](https://doi.org/10.1007/s10503-005-4422-y): justified grounds, adequate warrants and defeaters are distinct questions.
- [Schemes, Critical Questions, and Complete Argument Evaluation](https://link.springer.com/article/10.1007/s10503-020-09512-4): claim, data, warrant, backing, qualifier, rebuttal structure; evaluation is field-sensitive.
- [Gough (2021), Appraising Evidence Claims](https://doi.org/10.3102/0091732X20985072): technical quality, relevance, synthesis and alternative explanations matter for interpreting evidence claims.
- [Kalai et al. (2026), Nature](https://www.nature.com/articles/s41586-026-10549-w): accuracy-oriented evaluation can incentivize guessing; uncertainty/abstention need explicit handling.

## Comparison with repo and donors

[Diakrisis review contract](../REVIEW-CONTRACT.md) requires source-linked claims, non-pseudo-precise confidence, and owner-controlled decisions. Spatial Laboratory's `evidence-audit` already addresses source retrieval; **do not duplicate or pretend to have retrieved references**. The argument reviewer tests whether *claims are supported by premises*, not whether a paper's study design is methodologically sound (method-review), or whether a concept's classification is coherent (conceptual review). No donor code imported.

## Decisions

- Decompose conclusion/grounds/warrant and qualifier; distinguish empirical reports, hypotheses, definitions, normative prescriptions, cause-effect inferences and predictions.
- A source existing ≠ a source supporting the specific claim; cite the actual observed passage or abstain.
- Explain alternative explanations and defeaters without treating every possible caveat as a proven flaw; evidence absence = not justified in examined material, **not proven false**.
- No invented quotations, citations or statistical significance. Use a minimal counterstatement preserving measured outcome.

## Challenge cases and handoff

Positive: “fewer geometric violations ⇒ better architecture” when only geometric constraints were assessed. Negative: “we hypothesize independent review may help; this remains untested.” Unknown: citation behind inaccessible paywall → request verification instead of asserting fabricated content. Leave measurement validity to method review. **Model baselines deferred by owner.**
