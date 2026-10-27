# Reviewer evaluation fixtures

These are **proposed test inputs**, not completed baseline runs or accepted gold labels.

Run baseline tests **without** loading the new skill before writing or optimizing its instructions, following Superpowers' skill TDD guidance. Run equivalent skill-on tests in the same harness and record model/build, prompt, source revision, settings, tool access, answer, adjudicator and disputed labels. Keep negative controls and unfamiliar alternative models.

The first fixtures are in [pilot-cases.json](pilot-cases.json). Intended outcomes have `expected_interpretation` but are not validated judge outputs. No skill release may claim tested behavior on the basis of this fixture file alone.

Never send private research source documents to an unapproved API. Synthetic samples are intentionally short.

## Exposure labels

Every case in `pilot-cases.json` and `terminology-review/cases.json` carries an `exposure` record, checked by hand on 2026-10-27 against the skill files:

| Status | Meaning | Cases |
| --- | --- | --- |
| `seen-same-skill` | The skill under test contains the same scenario as an example | TERM-001, TERM-002, ONTO-001, ONTO-002, ARG-002, TERM-A1, TERM-A2, TERM-A6, TERM-A9 |
| `seen-other-skill` | Another skill contains it; the skill under test does not load that file | TERM-A4 |
| `held-out` | No matching example found | ARG-001, TERM-A3, TERM-A5, TERM-A7, TERM-A8, TERM-A10 |

A skill that reproduces its own example shows nothing about generalisation, so report seen and held-out cases separately. No case passage or context shares a 6-word sequence with any skill file (checked in `tests/test_evaluation_tools.py`), so all reuse is reuse of the scenario, not the wording. The protocol for paired, blinded runs is in [docs/EVALUATION.md](../docs/EVALUATION.md).