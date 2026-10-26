# DIA-003 — Agent Skills specification and upstream donor audit

**Observed:** 2026-10-26 · **Accounting leaf:** [DIA-003 / issue #3](https://github.com/interzettel/diakrisis/issues/3) · **PRS milestone:** DIA-M1 · **Priority:** P0.  
**Decision scope:** Research, provenance, license, threat boundary, fit and *reuse / adapt / reference / reject* choices. **No new skills, installation changes, runtime checks, behavioral benchmarks or model spending.**

## Executive decision

**Keep the seven authored Diakrisis skills as one independent `0.1.0-dev.0` package.** Adopt the *format* from Agent Skills, reuse the already pinned authoring *methods* from Superpowers and Anthropic skill-creator, and leave Project Record Standard as the canonical source of project-governance meaning. Selectively **reference** scientific-domain donors; do **not** wholesale import their libraries, scripts, APIs, licenses, or model-performance claims.

Three noteworthy findings:

1. **KalarisLabs is substantially downstream of K-Dense**, not a second independent validation of shared practices. Kalaris [third-party notices](https://github.com/KalarisLabs/research-agent-skills/blob/b0ee35abfd7e26428846fbd84f282114560a5fbd/THIRD_PARTY_NOTICES.md) identify 159 adapted skills from a K-Dense revision. Compare specific source files and notices before using either; avoid counting their overlap as corroboration.
2. **The root license is not enough for skill-level reuse.** K-Dense explicitly warns of per-skill licenses. Anthropic distributes `skill-creator` with its own Apache-2.0 `LICENSE.txt` and broader third-party notices. Kalaris has MIT plus third-party/source notices. Source access does not imply rights to relicense bundled scripts/templates. **No third-party skill content was copied into the Diakrisis seven review skills for this audit.**
3. **Project Record Standard v0.4.1 has an unresolved distribution-license question.** Its pinned public tree has no root `LICENSE` file and repository metadata did not declare an SPDX license in the observed API response; `pyproject.toml` does not declare a license. Do **not** infer MIT from Diakrisis's license or from public GitHub availability. Continue to treat the existing pinned submodule as a separate dependency; confirm rights/notice treatment with its owner *before new redistribution/bundling*. This is a licensing *gap*, not evidence of malicious code or an assertion that its current use is prohibited.

## Method and limits

Reviewed public GitHub default-branch revision metadata, canonical upstream files (including representative skill instructions), license notices, installation/security documentation and primary standards; compared them with the [existing source inventory](../SOURCES.md), [Agent Skills conformance rules](../AGENT-SKILLS-STANDARD.md), [Diakrisis foundation](../FOUNDATION.md) and the seven modules already on `main`.

**Review level:** documentary/manual spot-check, **not** full source-tree security audit, transitive dependency audit, execution, antivirus check, legal advice, assertion of cryptographic verification, or model evaluation. GitHub-reported default-branch SHA is an **observation**, not a release pin, and may change after 2026-10-26. A public specification link is not a software package. The existing three authoring-toolkit submodules and official format validator are pinned in Diakrisis; their actual interactive agent activation remains unobserved. CI checking only establishes its tested boundary.

### Exact source and licensing matrix

| Upstream | Observed revision / specification | License evidence and portability | Decision |
| --- | --- | --- | --- |
| **Agent Skills** | [agentskills/agentskills @ `69ef37e9424c0a7ea9dd2293b559e43ec8176379`](https://github.com/agentskills/agentskills/tree/69ef37e9424c0a7ea9dd2293b559e43ec8176379) (observed `main`; pinned submodule in Diakrisis) | Root [Apache-2.0](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/LICENSE). `SKILL.md` requires `name` and `description`; `metadata.version` **not required**. `skills-ref` is demonstration tooling, not runtime-quality certification. | **ADOPT format; REFERENCE validator**. One **suite** SemVer; no individual skill versions. |
| **Anthropic skill-creator** | [anthropics/skills @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44`](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator) (observed `main`; pinned) | `skills/skill-creator/LICENSE.txt` is **Apache-2.0**; broader [THIRD_PARTY_NOTICES.md](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/THIRD_PARTY_NOTICES.md) includes differing licenses for bundled dependencies (including GPL notices). Contains Python scripts/evaluation viewer; runner/model/tool requirements are not cross-platform guarantees. | **REUSE authoring workflow as pinned external tool**, not inside Diakrisis's review-skill text; do not vendor unrelated Anthropic skills or execute evaluator scripts without review. |
| **Superpowers** | [obra/superpowers @ `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) (observed `main`; pinned) | [MIT](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/LICENSE). Portable skill folders **do not** imply a functional Claude plugin; [session-start hooks](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/hooks/hooks.json) launch commands. Upstream documents optional visual companion telemetry and an opt-out; ensure privacy rules. | **REUSE methods / reference `writing-skills`**; don't automatically activate hooks or global plugins. Keep TDD model trials deferred at owner's direction. |
| **Project Record Standard** | [v0.4.1, source `ebc6afb0b977ff3d7605893c73ac63021775c4d3`](https://github.com/interzettel/project-record-standard/tree/ebc6afb0b977ff3d7605893c73ac63021775c4d3) (pinned) | **No root `LICENSE` or project license in observed pinned tree / `pyproject.toml`**; permission for redistribution not inferred. Python CLI >=3.10, no declared runtime Python dependencies in pyproject; shell/CI/browser portions have additional environments. Upstream [release](https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1) reports archive SHA-256 `a46cdcea938eb987b936497a22db8eab07106aad7dd12a8cfe10b4ad41f74607` (not independently recomputed here). | **REUSE as separate pinned governance standard**; maintain existing tracked dependency, **HOLD further code redistribution until license terms clarified**; preserve owner authority. |
| **K-Dense Scientific Agent Skills** | [K-Dense-AI/scientific-agent-skills @ `5f2bc0341354fd5590aef76a533ada1e1e5b4e62`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62) (observed `main`, **not** installed/pinned in Diakrisis) | Root [MIT](https://github.com/K-Dense-AI/scientific-agent-skills/blob/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/LICENSE.md), **but per-skill licenses can differ**. Representative `scientific-writing`, `peer-review`, `ontology-term-resolution` state MIT. Some helpers call external scientific APIs; repo tooling calls for Python 3.13+/uv/WSL2, while individual skill needs differ. Security policy reports periodic scans but claims aren't independently reproduced here. | **REFERENCE selective skill designs**, not bulk install. Possible future **ADAPT** ideas (source-linked peer review, controlled vocabulary ID resolution) only on scoped request, exact per-file license check, no network without authorization. |
| **KalarisLabs Research Agent Skills** | [KalarisLabs/research-agent-skills @ `b0ee35abfd7e26428846fbd84f282114560a5fbd`](https://github.com/KalarisLabs/research-agent-skills/tree/b0ee35abfd7e26428846fbd84f282114560a5fbd) (observed `main`, **not** installed/pinned) | Root [MIT](https://github.com/KalarisLabs/research-agent-skills/blob/b0ee35abfd7e26428846fbd84f282114560a5fbd/LICENSE) **with third-party notices** and [adapted-source manifest](https://github.com/KalarisLabs/research-agent-skills/blob/b0ee35abfd7e26428846fbd84f282114560a5fbd/third_party/upstream-manifest.json). Its `citation-verification` (MIT) explicitly calls Crossref/OpenAlex/arXiv; `unslop-academic-writing` has a local script and must preserve voice/claims. CLI/installer and downloads introduce supply-chain scope; security policy lists checks but not independently reproduced. | **REFERENCE citation and prose workflows**; don't import everything or claim independent replication of K-Dense. Potential domain-specific donor only after selecting exact skill and checking notices, network permissions and privacy. |
| **Vale** | [vale-cli/vale `v3` @ `8b9bfb97700a707140fff9f444048439df5bc9b1`](https://github.com/vale-cli/vale/tree/8b9bfb97700a707140fff9f444048439df5bc9b1); older `errata-ai/vale` path redirects | [MIT](https://github.com/vale-cli/vale/blob/8b9bfb97700a707140fff9f444048439df5bc9b1/LICENSE), Go executable with configuration and user-selected YAML rule packs; **rule packs may have independent licenses**. Local lint can work offline once binary/rules exist; `vale sync` fetches packages. Pattern substitutions are not contextual semantic or ontological truth. | **ADAPT as optional deterministic terminology/style checker** *if a consumer wants it*; not a dependency or required service for Diakrisis. No external style packs auto-applied. |

**Licensing decision detail:** No `LICENSE` found in PRS pinned source is a documented inspection result, **not a legal determination**. Do not assume the absence confers MIT rights. Similarly, a repository-wide MIT declaration does not negate explicitly different notices for nested donor material.

### Formal standards: what they are—and are not

| Primary reference | Status verified 2026-10-26 | Role in Diakrisis | Decision |
| --- | --- | --- | --- |
| [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/) | **W3C Recommendation, 18 August 2009**; separate concepts from preferred/alternative lexical labels and concept schemes | `terminology-review`, `conceptual-model-review` | **REFERENCE** normative descriptions. Don't copy whole specs or require RDF. |
| [W3C SHACL](https://www.w3.org/TR/shacl/) | **W3C Recommendation (2017)** | RDF graph constraint validity *when real data+shapes+validator available* | **REFERENCE** as optional deterministic tool boundary; no fake validation output. |
| [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) | **Working Draft, 25 October 2026**, not a Recommendation | Monitor only; do not silently present draft features as normative stable rules | **REFERENCE / DEFER** adoption pending specification maturity and consumer need. |
| [OWL 2 Primer, Second Edition](https://www.w3.org/TR/owl2-primer/) | **W3C Recommendation, 11 December 2012** | Classes, individuals, properties and open-world ontology interpretation | **REFERENCE**; no mandatory RDF/OWL ontology for narrative reviews. |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | **W3C Recommendation, 30 April 2013** | Provenance entities, activities and agents; provenance ≠ truth, authority or acceptance | **REFERENCE**, use only if formal provenance needed. |

W3C technical reports carry their own [W3C document-use terms](https://www.w3.org/copyright/document-license-2015/). **Citing publicly accessible normative definitions is not a decision to copy their normative text into an MIT codebase.**

## Distinct responsibilities and duplication risks

| Diakrisis responsibility | Useful donor insight | What we should *not* clone |
| --- | --- | --- |
| `terminology-review` | SKOS concept/label separation; K-Dense `ontology-term-resolution` verifies biomedical identifiers | External biomedical ontology-ID lookup as a compulsory writing check; text similarity mistaken for equivalent concepts |
| `conceptual-model-review` | OWL/SKOS/SHACL categorical and logical distinctions | Universal ontology, incorrect closed-world inference or imaginary SHACL validation |
| `argument-review` | K-Dense scientific-writing/peer-review source-evidence discipline; Kalaris citation verification | Automatically fetching confidential manuscripts or treating DOI existence as proof of claim |
| `method-review` | K-Dense peer-review and scientific methods workflows | Discipline-blind checklists, mandatory randomization or assuming preregistration |
| `communication-review` | Vale custom vocabulary; Kalaris `unslop-academic-writing` clarity-before-style | Mandatory stock “AI-slop scores,” one English style, flattening an author's voice |
| `consistency-review` | PROV-O source lineage; PRS ledger and project-record parity | A second project database or independent completion accounting |
| `review-coordinator` | Agent Skills modular activation; Superpowers skill authoring discipline | Autonomous background loops, bulk models, fictional cross-reviewer independence |

Kalaris credits K-Dense as one source for a large shared collection, so an overlap between their skills **cannot count as independent evidence** supporting Diakrisis's conclusions. Reuse a canonical origin when two donor copies address the same workflow, and preserve attribution if selected later.

## Threat and compatibility register

- **Untrusted skill instructions / prompt injection:** a repository may contain commands, URLs and references that an agent treats as authoritative. **Read/check exact scoped source before executing**. No instructions in a donor skill grant new user permissions.
- **Remote installers and global paths:** `curl | sh`, `irm | iex`, unpinned `npx`, `--global` and plugin hooks can mutate broader runner environments. **No such command executed in this audit.** Diakrisis's existing installer is separate and dry-run by default.
- **Exfiltration / research confidentiality:** tools that call Crossref, OpenAlex, OLS, ZOOMA or model/cloud APIs may disclose identifiers, metadata or private text. A local Python helper alone does not make a hosted reviewing agent local. Separate explicit user and institutional authorization remains necessary.
- **Supply chain:** pin exact source revision *after selection*, inspect scripts/dependencies/license, record checksums and rollback. **A current default-branch SHA is not a verified release checksum**.
- **Windows portability:** Agent Skills Markdown generally travels, while Bash hooks, executable file paths, `uv`, WSL2, binary installers and optional API calls are host dependent. Don't infer that Windows 11 and Claude Code/Codex both activate the same hooks.
- **False assurance:** scanner/readme claims, YAML validators, source references, a collection of two overlapping donor libraries and CI smoke runs are not behavioral evidence or scientific acceptance.

### Current installation boundary

- **Pinned existing submodules:** Agent Skills reference `69ef37e…`, Anthropic `dbd4588…`, Superpowers `2ce8aa1…`, Project Record Standard v0.4.1 `ebc6afb…`.
- **Observed execution:** earlier isolated GitHub Actions copied project-scoped authoring skills and validated Project Record Standard files; Diakrisis CI validated structural format. No interactive Windows/Claude/Codex discovery, no live model A/B tests and no scientifically adjudicated performance observed.
- **Not installed into Diakrisis:** K-Dense, KalarisLabs, Vale (only externally consulted for this audit). No W3C parser/validator added as a new runtime dependency.
- **Package version:** still single `0.1.0-dev.0`, unreleased. Donor revisions do not impose per-skill versioning.

## Decision record and unresolved follow-up (not new scope)

**DIA-003 scope complete when this audit is reviewed and committed** with source links and explicit uncertainty. No donor code was imported. This work meets the documentation criterion without falsely claiming third-party security certification, performance or installation.

The following matters belong to **existing** issues, not new side quests:

- **DIA-002 / #2, P0, DIA-M1:** clarify redistribution/license terms for PRS with its owner before copying it into distributable Diakrisis packages; compare against original v0.4.1 release materials. This is distinct from later local checksum/runtime receipts, already deferred.
- **DIA-004 / #4, P1, DIA-M1:** actual selected-runner activation, local installation and rollback verification (deferred until user-directed final test stage).
- **DIA-005 / #5, P1, DIA-M1:** decide if contextual source/authority schema needs any formal SKOS/SHACL adapter; do not introduce one without validated need.
- **DIA-007 / #7 and DIA-008 / #8:** behavior, false-positive and composition testing deferred by owner; no benchmark or evaluator added under DIA-003.
- **DIA-010 / #10:** one package release and pinned adoption; this report is not publication evidence.

**Progress discipline:** update `DIA-003` only for its documentation deliverable. DIA-M1 acceptance remains unknown; do not count another leaf as Done. At handoff, select the next eligible issue from actual dependencies and blockers—not from donor novelty.

## Primary source registry

- Agent Skills spec: https://agentskills.io/specification ; pinned source/validator above.
- Anthropic skill-creator and per-skill Apache license: https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator
- Superpowers methods + hooks: https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
- PRS release: https://github.com/interzettel/project-record-standard/releases/tag/v0.4.1
- K-Dense library and skill licensing: https://github.com/K-Dense-AI/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62
- Kalaris provenance and citation verifier: https://github.com/KalarisLabs/research-agent-skills/tree/b0ee35abfd7e26428846fbd84f282114560a5fbd
- Vale v3 linter: https://github.com/vale-cli/vale/tree/8b9bfb97700a707140fff9f444048439df5bc9b1
- W3C specs and statuses: https://www.w3.org/TR/skos-reference/ · https://www.w3.org/TR/shacl/ · https://www.w3.org/TR/shacl12-core/ · https://www.w3.org/TR/owl2-primer/ · https://www.w3.org/TR/prov-o/

## Post-audit source-owner licensing resolution — 2026-10-26

**This is a subsequent event, not a correction of what the original audit observed.** The audit correctly recorded no `LICENSE` in the frozen v0.4.1 tag. The repository owner later expressly approved MIT with the proposed attribution for rights-controlled original Project Record Standard source, **including original material in v0.4.1**. The approval is now documented in [PRS licensing decision](https://github.com/interzettel/project-record-standard/blob/9fab17ddae8c2488eff63670d8f1a28d5c763a1f/standards/LICENSING-DECISION.md) and [merged PR #5](https://github.com/interzettel/project-record-standard/pull/5). The old tag/ZIP and digests remain unchanged; third-party materials retain their own terms. Supersedes the audit's former *unresolved owner-permission* action only. No live runtime/model tests, new imports, or repository release have occurred.
