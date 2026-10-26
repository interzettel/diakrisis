# Reproducible toolchain installation

This repository declares three pinned skill-toolkit submodules plus the pinned Agent Skills specification/reference validator submodule; their availability in GitHub does not install them on your Windows PC or load them into an agent. For first setup use a **reviewed local checkout**; do not pipe network responses directly into a shell.

## 1. Clone source at reviewed revisions

On Windows 11 PowerShell with Git and Python 3.10+:

```powershell
git clone --recurse-submodules https://github.com/interzettel/diakrisis.git
cd diakrisis
git submodule status
python tools/bootstrap_skills.py --target .
```

Confirm that the preview shows the exact pinned commits from `docs/SOURCES.md`. No skill installs on preview.

## 2. Install project-local portable skills

```powershell
python tools/bootstrap_skills.py --target . --apply
```

The installer copies **all 15 Superpowers skill directories** and Anthropic's full `skill-creator` directory, including its bundled evaluator scripts and Apache-2.0 license, to `.agents/skills/`; it then calls the **upstream Project Record Standard's own installer** for its 11 skills. It previews both parts first. It refuses conflicts rather than overwriting existing files. The script never mutates a global `~/.claude` or `~/.codex` folder.

Run the preview before subsequent upgrades. Pinned revisions are fixed until a reviewed change updates them. Avoid editing third-party installed copies; replace through reinstallation with a reviewed pin and preserve local authors' skills.

## 3. Activate the full Superpowers harness support

Portable skill directory installation **does not automatically activate Superpowers plugin hooks**. On Claude Code, use the maintained official plugin marketplace and explicitly install:

```text
/plugin install superpowers@claude-plugins-official
```

Restart the agent session and verify automatic skill triggering. See upstream [installation documentation](https://github.com/obra/superpowers#installation). Codex App uses its official Superpowers plugin marketplace; other runtimes follow their documented procedures. Do not claim hook activation from a checked-in skill directory.

Anthropic's `skill-creator` is now project-local in a compatible runner that discovers `.agents/skills/`; verify it is discoverable through your runtime's native skill listing. Follow its evaluation process, and test before deploying reviewers.

## 4. Establish Project Record Standard

The installer copies the v0.4.1 project-record skills, but does not itself author accepted scope, run the project-record ledger CLI, authorize decisions, create a GitHub Project, or deploy a website.

Follow the [adoption plan](../progress/adoption.md), starting with the official `establish-project-tracking` skill and a new empty staging directory. Use its native CLI to validate the project manifest. Do not claim a completion percentage before scoped ledger and authoritative evidence exist.

## 5. Verification and rollback

Run `python tools/check_contracts.py` and the source kit's official tests. Test one new Claude/Codex session: skill discovery, appropriate trigger, negative trigger, and inability to silently edit accepted project definitions. GitHub Actions tests should be treated as separate evidence once a workflow actually executes.

For rollback, reverse the reviewed commit/PR or remove only file paths recorded as introduced by the installation receipt; preserve pre-existing skills and `AGENTS.md`. Project-scoped plugin uninstall is runner-specific.

**Limitations of this bootstrap session:** The connector could pin upstream Git objects but did not run git clone, skill CLI or Claude/Codex in the user's workstation. No local runtime activation has been observed.