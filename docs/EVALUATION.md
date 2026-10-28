# Evaluation protocol (DIA-006, DIA-007)

How Diakrisis skills are compared with a no-skill baseline on real documents, and how the results are kept honest. This is a protocol, not a result: no behaviour claim follows from this file.

It serves two ledger criteria:

- **DIA-006:** "matched no-skill/with-skill runs and human-adjudicated behavior results".
- **DIA-007:** "evidence-linked evaluation on safe copies of real research/project documents, including false-positive and preservation checks".

## 1. Register before running

Before any review run, write the protocol for that round and record its SHA-256. The record names:

- the documents (as a frozen copy in a git repository, with its commit);
- the Diakrisis revision whose skills are tested;
- the cells (document × review type);
- the arms;
- the finding cap;
- the tool access;
- the grading scale;
- the outcomes.

Anything that later departs from it is a **deviation** and is reported as one, with its reason (CONSORT 2025 item 10).

## 2. Held out, checked two ways

Material the skills have already seen cannot show that a skill generalises.

- **Verbatim reuse:** `python tools/overlap_check.py <files>` counts 8-word sequences shared with every skill file and fixture. Zero is required for owner-supplied material.
- **Reused scenario in new words:** the n-gram check cannot see this, so every fixture carries a hand-checked `exposure` label (`held-out`, `seen-same-skill` or `seen-other-skill`) with the skill file and the example it matches. Report results on `held-out` cases separately from seen ones; a skill reproducing its own example is not evidence.

## 3. Arms and runs

- **Skill arm:** a fresh agent reads the specialist `SKILL.md` and the contract files it links, and nothing else in this repository.
- **Baseline arm:** a fresh agent with the same task line, the same documents, the same tool access and the same output shape, and no Diakrisis files.
- One agent per cell and arm, on the same model. Each run reports at most the cap (default 6) of findings, most important first, in the common shape:

```json
{"findings": [{"location": "", "span": "exact quote", "problem": "", "proposed_change": "", "importance": "low|medium|high"}],
 "coverage_note": "what was checked and what could not be"}
```

- The skill arm also writes its full contract revision 2 report. Its schema validity is a secondary outcome. The common-shape file is its projection: `informational` and `minor` map to `low`, `major` to `medium`, `blocking-candidate` to `high`.
- Both arms are told to write `problem` and `proposed_change` in plain sentences without framework labels, so that category names do not reveal the arm.

## 4. Blinding (CONSORT 2025 items 20a and 20b)

**Who is blind (20a):** every grader, meaning the document owner and any agent asked to agree or disagree. The person running the evaluation is not blind and therefore never grades.

**How (20b):**

1. `python tools/blind_pool.py --runs DIR --config cells.json --out DIR` drops arm, run and rank from every finding.
2. It pools each document's findings, shuffles them and assigns new IDs (`<document>-<nn>`).
3. It writes the arm key to a separate file, refusing to overwrite an existing key, and prints the key's SHA-256.
4. Publish that hash where the graders work **before** grading starts. Open the key only when grading is finished. Anyone can then check the opened key against the hash.

**Residual risks.** These are reported, not hidden:

- writing style can still differ between arms;
- the skill arm may use contract vocabulary despite the instruction not to;
- agent graders from the same model family are not independent of the reviewers. Their agreement is a reaction, not corroboration (see `COORDINATION.md`).

## 5. Grading

Each pooled finding gets exactly one grade:

| Grade | Meaning |
| --- | --- |
| Useful | Correct, and the owner would act on it or answer it |
| Valid but trivial | Correct, but not worth the owner's time |
| Wrong or unsupported | Misreads the text, invents a problem or relies on something that is not there |
| Duplicate | Same point as an earlier finding in the same document |

**False positives (DIA-007).** "Wrong or unsupported" findings are the false positives.

**Preservation check.** Is a proposed change one that would alter what the author meant? A finding can be correct in substance and still fail preservation; graders note this.

**Recall.** Before seeing any output, the owner writes a private list of problems they already know about in each document. Afterwards each finding is matched to list items, by the owner or by an agent that has not seen the arm key.

A grader who cannot finish every finding may grade a random sample drawn by the evaluator. The sample and its size are recorded as a deviation.

## 6. Outcomes

**Primary, per arm:**

- useful findings;
- the useful share of all findings;
- owner-listed problems caught.

**Secondary:**

- quote-check failures (`tools/check_spans.py`, run by `blind_pool.py` on every span);
- importance agreement with the owner;
- findings outside the review type's scope;
- contract-report schema validity (skill arm);
- agreement or disagreement from agent graders.

With one run per cell, results show a direction, not a measured effect. Report counts, not percentages dressed as rates, and never call a skill validated on one round.

## 7. Privacy

Owner material is reviewed in a private workspace and never committed here. The public repository receives:

- this protocol;
- the tools;
- the exposure labels;
- aggregate counts, and only when the owner approves them.

Quotes from owner documents, findings, grades and keys stay with the owner.

## Rounds

| Date | Material | Status |
| --- | --- | --- |
| 2026-10-27 | Owner-supplied research proposal, two essay drafts and their status ledgers (private) | Adjudicated and unblinded 28 Oct; aggregate counts published with owner approval in [DIA-007-ROUND-1-2026-10-27.md](research/DIA-007-ROUND-1-2026-10-27.md) |
| 2026-10-28 | Owner's revised research proposal (v7.6, private), six review types | Round 2: revised skills (`28067ca`) vs baseline, 12 runs, 70 findings posted blind (key SHA-256 `c7bc3027…`, protocol SHA-256 `956975dd…`); adjudication pending; no result reported here |
