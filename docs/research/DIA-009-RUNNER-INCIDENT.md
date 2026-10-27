# DIA-009 — private-consumer Actions runner startup incident

**Observed:** 2026-10-27 (UTC data from GitHub API). **Owning item:** [DIA-009 / issue #9](https://github.com/interzettel/diakrisis/issues/9); **PRS ledger milestone:** DIA-M3.  
**Scope:** Writing Kitchen and Spatial Laboratory, both private repositories owned by `yigit-denktas`. **Conclusion:** GitHub Actions jobs failed **before any runner allocation or executable step**. The underlying GitHub account/dispatcher reason is not exposed through the available connector; the precise billing or policy cause is therefore **not confirmed**.

## Inspectable failure evidence

| Repository / run | When | Jobs | Runner allocation | Executed steps | Outcome |
| --- | --- | --- | --- | --- | --- |
| [Writing Kitchen, before Diakrisis, run 39126910180](https://github.com/yigit-denktas/writing-kitchen/actions/runs/39126910180) | 2026-10-18 12:21 UTC | `pytest` | `runner_id: 0` | `steps: []` | Failed within ~2 seconds |
| [Writing Kitchen, after Diakrisis, run 40409275568](https://github.com/yigit-denktas/writing-kitchen/actions/runs/40409275568) | 2026-10-26 22:02 UTC | `pytest`; `Pinned Diakrisis source integrity` | Both `runner_id: 0`, `runner_name: ""` | Both `steps: []` | Both failed within ~2–3 seconds |
| [Spatial Laboratory, before Diakrisis, run 40119623438](https://github.com/yigit-denktas/spatial-laboratory/actions/runs/40119623438) | 2026-10-24 18:12 UTC | `telemetry` | `runner_id: 0` | `steps: []` | Failed within ~2 seconds |
| [Spatial Laboratory, PR #18, run 40412642089](https://github.com/yigit-denktas/spatial-laboratory/actions/runs/40412642089) | 2026-10-26 22:28 UTC | `telemetry` | `runner_id: 0`, `runner_name: ""` | `steps: []` | Failed within ~1 second |
| [Public Diakrisis, run 40417865197](https://github.com/interzettel/diakrisis/actions/runs/40417865197) | 2026-10-26 23:10 UTC | `basic` | `runner_id: 1000010652` | 14 steps | Success |

The API evidence is from the latest job collection with exact attempts, e.g.:

- `GET /repos/yigit-denktas/writing-kitchen/actions/runs/40409275568/attempts/1/jobs`
- `GET /repos/yigit-denktas/spatial-laboratory/actions/runs/40412642089/attempts/1/jobs`
- `GET /repos/interzettel/diakrisis/actions/runs/40417865197/attempts/1/jobs`

Both consumer workflows request standard `runs-on: ubuntu-latest`. Spatial Laboratory uses `actions/checkout@v4`; Writing Kitchen's isolated source-integrity job also uses `actions/checkout@v4`. Their check-run records have two annotations each, but the connected GitHub API cannot read their annotation texts (or actual billing and repo Actions policy). Log download yields unavailable log blobs because no steps were executed.

**Established:** This failure cannot be attributed to Python application tests, checkout, review skills, SDKs, `pytest`, or the N02 integration being *executed and failing*. None of those commands ran. The symptom existed before the Diakrisis changes in both private repositories.

**Hypothesis (not confirmed):** GitHub-hosted runner dispatch is blocked by the account's private Actions billing/usage budget, quota, failed payment/hold, repository Actions permissions, or another backend allocation condition. GitHub documents private-repo minute limits and billing restrictions in [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions). Similar cases are described in [GitHub community discussion #183940](https://github.com/orgs/community/discussions/183940), but this is **not** direct evidence of this owner's billing state.

**Owner confirmation (2026-10-27):** The owner confirmed that the account's **monthly private GitHub Actions usage is exhausted** and does **not** wish to add spending. This is now the recorded explanation for `runner_id: 0`, `steps: []`. It rests on the owner's statement; GitHub billing pages were not independently inspected by an agent. Consequently, steps 1–2 of the repair path below are settled by owner decision: wait for the quota to renew, and use offline/local checks meanwhile. Do not ask the owner to pay, raise budgets, change repository visibility or modify workflows to bypass the limit.

## Correct repair path

1. Repository owner checks **GitHub account Settings → Billing & licensing (or Billing & plans) → Actions usage / Budgets and alerts** for the owner account, including free-minute balance, any `$0` budget limit, payment notices, and whether Actions are enabled for private repos.
2. If GitHub displays a budget/spending/payment restriction, the owner decides whether to adjust it. **Do not automatically raise spending limits, add payment methods, or change repository visibility.** If the UI shows no restriction, supply these run IDs and `runner_id: 0`, `steps: []` to GitHub Support and ask for runner-dispatch diagnosis.
3. Once runner allocation resumes, **rerun** Writing Kitchen's full `Test suite` and Spatial Laboratory PR #18's `Research observatory offline validation`. Confirm a nonzero runner ID and actual executed checkout/test steps, inspect real failures and repair only verified source defects.
4. If runnable, verify Writing Kitchen's pinned 16-file snapshot and its original application suite; verify Spatial Laboratory's N02 bridge synthetic controls. **The latter PR remains unmerged pending required explicit owner approval**, even if CI later turns green.
5. Reconcile [Writing Kitchen #21](https://github.com/yigit-denktas/writing-kitchen/issues/21), [Spatial Laboratory PR #18](https://github.com/yigit-denktas/spatial-laboratory/pull/18) and Diakrisis DIA-009 with exact check receipts; then honor deferred DIA-007 behavior, authorization and consumer acceptance gates.

## Non-actions and acceptance boundary

No workflow YAML, runner labels, repository visibility, owner account budget or client runtime was changed during this investigation. Replacing workflow steps or rerunning unchanged jobs while the dispatcher refuses to allocate a runner cannot validate the tests. GitHub public Diakrisis's successful CI is **not** proof that the private consumer installations behave correctly. This incident diagnosis is repository/runner **verification evidence only**; implementation can remain merged, but DIA-009 is **not Done**, DIA-M3 acceptance is unknown, and required completion remains **2/10**.
