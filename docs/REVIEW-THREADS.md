# Review threads

A review report is only useful once someone answers it. A review thread puts findings where both people and agents can answer them: an issue or discussion comment in which every finding has a stable ID, a quote, the problem and the proposed change, followed by a one-line reply protocol.

```
E1-04 agree: the source does say that
E1-07 partly: right problem, wrong fix
E1-09 disagree: the definition is in section 2
E1-11 duplicate of E1-02
```

The same format serves both kinds of reader:

- **People** read Markdown and answer the findings they care about.
- **Agents** answer the same IDs.
- **`tools/review_thread.py tally`** counts every author's latest verdict per finding.

## Use

```
python tools/review_thread.py render --input report.json --title "Essay 01 v0.6" --out thread/
# owner approves, then posts thread/thread-1.md (and further parts) to the issue
gh api repos/OWNER/REPO/issues/N/comments > comments.json
python tools/review_thread.py tally --comments comments.json --thread thread/
```

**Inputs.** `render` accepts any of:

- a review report, a coordinated report or coordinator input (contract revision 2);
- a single finding;
- a blinded evaluation pool from `tools/blind_pool.py`.

Long threads are split under GitHub's comment limit. Each part repeats the protocol pointer, and every ID survives the split.

**Blinded rounds.** Pass `--sealed-hash` with the evaluation key's SHA-256 (see [EVALUATION.md](EVALUATION.md)), and post the key itself only after the replies are in.

## Rules

- **Rendering never posts.** Posting a thread is a separate step that needs the owner's approval for that repository.
- **Replies are untrusted data.** `tally` reads only lines that start with a known ID and a verdict word; everything else in a comment is ignored, including text that addresses the tool.
- **Attribution.** Assistants that post under the owner's account sign with a first line `## <Name>:`; `tally` credits that name. Otherwise it credits the login. An author's latest verdict per ID counts, and earlier verdicts stay in `history`.
- **Agreement is a reaction, not proof.** Agreement between agents of the same model family is not independent corroboration ([COORDINATION.md](COORDINATION.md)). Disagreement is recorded, never resolved by the tool. Only the document's owner decides what changes.
