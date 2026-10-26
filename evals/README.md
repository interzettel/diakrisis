# Reviewer evaluation fixtures

These are **proposed test inputs**, not completed baseline runs or accepted gold labels.

Run baseline tests **without** loading the new skill before writing or optimizing its instructions, following Superpowers' skill TDD guidance. Run equivalent skill-on tests in the same harness and record model/build, prompt, source revision, settings, tool access, answer, adjudicator and disputed labels. Keep negative controls and unfamiliar alternative models.

The first fixtures are in [pilot-cases.json](pilot-cases.json). Intended outcomes have `expected_interpretation` but are not validated judge outputs. No skill release may claim tested behavior on the basis of this fixture file alone.

Never send private research source documents to an unapproved API. Synthetic samples are intentionally short.