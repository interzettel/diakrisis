# Terminology-review behavior evaluation (unexecuted plan)

**Status:** NOT EXECUTED. No baseline model run, skill-on run, independent judgment or effect estimate has been recorded. CI structure and prompt-metadata serialization do **not** establish competence.

## Purpose

Measure whether `terminology-review` improves source-grounded terminology critique, particularly false-positive avoidance, compared with the **same model and tools** performing the task without the skill.

## Runtime preflight

1. Open a reviewed checkout of draft PR #17 in a supported agent runtime (Claude Code and/or Codex). Use a clean branch/worktree and no private data.
2. Verify that `.agents/skills/terminology-review/SKILL.md` appears through the host's real skill discovery/activation mechanism. Separately verify whether Superpowers is active as a plugin; a copied directory is not a plugin hook.
3. Record exact model/build, temperature/thinking where available, prompt versions, allowed tools, source revision, skill revision, system instruction baseline, time and user approvals.
4. If using two different models or harnesses, treat results as distinct experiments, not matched pairs.

## Locally runnable paired evaluation (no hosted inference)

On a Windows checkout with Python and an intentionally installed local Ollama model:

```powershell
python tools/terminology_eval.py --dry-run
python tools/terminology_eval.py --execute --model <your-installed-model> --output evals/terminology-review/runs/first-pair.json
```

The tool refuses non-loopback endpoints, redirects and proxy egress; raw outputs remain locally gitignored until privacy and quality review. Do not claim this executes on a user's machine merely because commands exist. The with-skill arm explicitly injects the procedure; test actual automatic skill discovery separately in Claude Code/Codex.

## Same-input comparisons

Use [pilot-cases](../pilot-cases.json) as proposed prompts and reference interpretations, not established gold labels. For each case:

**Control:** without the Diakrisis skill. Present the input and available canonical references as ordinary task context. Do not add rule hints from the skill.

**Treatment:** with `terminology-review` discovered and used. Present the same input and references; record if the runtime actually loaded the skill. Don't silently upgrade to an independent external verifier in only one arm.

Ask both:
> Review this passage for terminology consistency and definition conflicts in the provided domain. Identify relevant errors, uncertainties and any legitimate unusual usage. Cite the applicable source/passage. Do not modify the original.

Do not expose expected interpretations to either model. Make a run record for every invocation, including failures and abstentions.

## Review metrics

Per case, human adjudicators examine:
- **Detection:** correct identification of confirmed source-defined conflict.
- **Specificity:** valid unusual labels, quotation and scope-dependent terms are not wrongly flagged.
- **Evidence:** accurate supporting source, scope, exact quoted passage and applicability.
- **Restraint:** admitted uncertainty when authority cannot be inspected.
- **Minimal intervention:** the proposed change preserves authorial intent.

Count confirmed/false-positive/false-negative/uncertain outcomes with a rubric that explains borderline judgments. Do **not** interpret a tiny sample or a higher raw finding count as statistically demonstrated improvement.

## Recommended additional held-out cases

- The same designation denotes distinct concepts in two explicitly named domains.
- Bilingual glossary has preferred labels in multiple languages and legitimate translation variants.
- A term appears in a quoted historical passage and current editorial narration.
- Local and external authorities conflict without a precedence rule.
- An abbreviation is defined twice with incompatible expansions.
- A canonical glossary is inaccessible; safe abstention expected.

## Artifacts to save (private if source demands)

- `runs/<run-id>/manifest.json`: model, tool/harness, skill checksum, revision, date, case IDs and executed command.
- `runs/<run-id>/baseline/`: actual outputs and logs with skill absent.
- `runs/<run-id>/treatment/`: actual outputs and host evidence of skill activation.
- `runs/<run-id>/adjudication.json`: independent labels, rationale, unresolved conflicts.
- `runs/<run-id>/summary.md`: measured rates, limitations and next change.

Only update this document or issue DIA-006 to *completed* once real runs exist, tests and acceptance gates pass, and owner/reviewer evaluation is recorded.

## Security / spending

External model use, paid inference, sharing private repository text or invoking a private device requires the existing operator's authorization. This file grants none. Use synthetic fixtures until privacy is reviewed.
