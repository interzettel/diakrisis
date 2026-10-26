#!/usr/bin/env python3
"""Preview or install pinned, project-scoped Agent Skills. No global profile writes.

Usage:
    git submodule update --init --recursive
    python tools/bootstrap_skills.py --target .            # dry run
    python tools/bootstrap_skills.py --target . --apply    # explicit project-scoped install

Superpowers' Claude Code plugin hooks require its official runner-specific plugin
installation separately. Copying skill directories is not the same as activating
those hooks. Uses only standard-library Python and project-local paths.
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "superpowers": "2ce8aa15d05bd57213e6f746f953aafb7ded7a8b",
    "anthropic-skills": "dbd4588f9e1033efb41dad4bef2f7947c8993d44",
    "project-record-standard": "ebc6afb0b977ff3d7605893c73ac63021775c4d3",
}
UPSTREAM = ROOT / "tools" / "upstream"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def require_pin(name: str) -> Path:
    path = UPSTREAM / name
    if not (path / ".git").exists() and not path.is_dir():
        raise RuntimeError(f"Uninitialized submodule: {path}. Run git submodule update --init --recursive")
    p = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True, capture_output=True, check=True,
    )
    actual = p.stdout.strip()
    if actual != PINS[name]:
        raise RuntimeError(f"{name} unexpected commit {actual}; expected {PINS[name]}")
    return path


def paths_in_tree(src: Path) -> list[Path]:
    paths = []
    for candidate in src.rglob("*"):
        if candidate.is_symlink():
            raise RuntimeError(f"Refuse to install source symlink: {candidate}")
        if candidate.is_file():
            paths.append(candidate.relative_to(src))
    return sorted(paths)


def plan_skill(src: Path, target_dir: Path) -> list[tuple[Path, Path, str]]:
    header = src / "SKILL.md"
    if not header.is_file():
        raise RuntimeError(f"Missing SKILL.md: {src}")
    name = src.name
    if not NAME_PATTERN.fullmatch(name):
        raise RuntimeError(f"Invalid skill directory name: {name}")
    text = header.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise RuntimeError(f"Missing skill YAML frontmatter: {header}")
    if not re.search(r"^name: " + re.escape(name) + r"$", text, re.M):
        raise RuntimeError(f"Skill name differs from directory: {src}")
    destination = target_dir / name
    if destination.is_symlink():
        raise RuntimeError(f"Refusing symlink destination: {destination}")
    result = []
    for relative in paths_in_tree(src):
        to = destination / relative
        if to.is_symlink():
            raise RuntimeError(f"Refusing symlink target: {to}")
        before = src / relative
        if to.exists():
            if not to.is_file() or not filecmp.cmp(before, to, shallow=False):
                raise RuntimeError(f"Existing file conflict, no overwrite: {to}")
            action = "identical"
        else:
            action = "create"
        result.append((before, to, action))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=ROOT,
                        help="project root receiving .agents/skills; defaults to Diakrisis")
    parser.add_argument("--apply", action="store_true", help="write files (default: preview only)")
    parser.add_argument("--skip-project-records", action="store_true",
                        help="skip native Project Record Standard installer")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists() or not target.is_dir():
        parser.error(f"target must be an existing directory: {target}")
    if target.is_symlink():
        parser.error("target may not be a symlink")

    try:
        sp = require_pin("superpowers")
        an = require_pin("anthropic-skills")
        prs = require_pin("project-record-standard")
        sources = [an / "skills" / "skill-creator"] + sorted(
            p for p in (sp / "skills").iterdir() if p.is_dir()
        )
        operations = []
        for src in sources:
            operations.extend(plan_skill(src, target / ".agents" / "skills"))
        pending = [item for item in operations if item[2] == "create"]
        print(json.dumps({
            "mode": "apply" if args.apply else "preview",
            "target": str(target),
            "source_commits": PINS,
            "skills_to_install": [s.name for s in sources],
            "new_files": len(pending),
            "unchanged_files": len(operations) - len(pending),
            "conflicts": 0,
            "plugin_hooks_installed": False,
        }, indent=2))
        # Preview the authoritative PRS installer before making changes.
        if not args.skip_project_records:
            env = dict(os.environ)
            env["PYTHONPATH"] = str(prs / "src")
            cmd = [sys.executable, "-m", "project_record", "install-skills",
                   "--toolkit", str(prs), "--target", str(target)]
            subprocess.run(cmd, env=env, cwd=str(prs), check=True)
        if not args.apply:
            print("Dry run. No files written. Use --apply to install project-scoped skills.")
            return 0
        for before, to, action in operations:
            if action == "create":
                to.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(before, to)
        if not args.skip_project_records:
            subprocess.run(cmd + ["--apply"], env=env, cwd=str(prs), check=True)
        receipt = target / ".agents" / "diakrisis-upstreams.json"
        if receipt.exists() and receipt.is_symlink():
            raise RuntimeError("Refusing symlink receipt")
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps({
            "source_commits": PINS,
            "scope": "project",
            "superpowers_harness_plugin_active": False,
            "note": "Skills copied; Claude Code plugin hooks require official runner-specific installation.",
        }, indent=2) + "\n", encoding="utf-8")
        print("Installed project-scoped skills. Verify discovery in your runner separately.")
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"BOOTSTRAP ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
