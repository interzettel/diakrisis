# Method review: source review before implementation

**Observed:** 2026-10-26. **Scope:** Scientific constructs, operationalization, study design and inference limits. **Gate:** pre-implementation design only; model testing explicitly deferred by owner. **Source policy:** inspect linked primary materials where public; do not claim access to paid standards or validation from cited material.

## Checked external sources

- [OSF official registrations guide](https://help.osf.io/article/330-welcome-to-registrations): distinguish pre-specified plans, actual decisions and deviations; record hypotheses, variables, tests and contingencies.
- [EQUATOR reporting-guideline finder](https://equator-network.org/reporting-guidelines/index.html): reporting completeness guidance depends on study type; **reporting guidelines are not study-design or quality-appraisal tools**.
- [EQUATOR STROBE](https://equator-network.org/reporting-guidelines/strobe/index.html): observational-study reporting, not a general requirement for experimental spatial design.
- [Cochrane bias taxonomy excerpt](https://www.ncbi.nlm.nih.gov/sites/books/NBK91433/table/cerguidebias.t2/): consider selection, confounding and other named bias mechanisms, conditional on study design.

## Comparison with repo and donors

[FOUNDATION](../FOUNDATION.md) distinguishes construct, conceptual definition, operational definition, measurement, evidence, and claim; preserve the distinctions. Spatial Lab `lab-research-contract`, `spatial-research-method-selection` and reproducible-experiment skills are potential delegated domain aids. This is an *audit* of a proposed or reported design, not a tool to run experiments or rewrite preregistration after the fact. No imported code.

## Decisions

- Identify study type and target of inference before offering advice. Check units, instruments, comparison groups, data grain, analysis plan, sample selection, independence, leakage, stopping/exclusion rules and confounders *when applicable*.
- Don't treat qualitative/exploratory designs as failed RCTs; pre-registration applies to confirmatory work when appropriate, not every creative investigation.
- Keep **planned**, **actually conducted** and **reported** as separate records. Unreported detail → cannot assess, not proof it was missing from the actual experiment.
- Compare measurement to construct and avoid overgeneralizing proxy outcomes; mark certainty.

## Challenge cases and handoff

Positive: spatial-design “quality” operationalized solely as number of constraint violations while the claim includes user satisfaction. Negative: exploratory qualitative interview study with explicit reflexivity but no randomized control. Unknown: no sample-design documentation → ask for protocol, don't infer that sampling was invalid. Abstract argument wording routes to argument review. **Behavior tests deferred.**
