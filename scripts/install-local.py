#!/usr/bin/env python3
"""Install skills from this checkout into a local Codex skills directory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills.manifest.json"


def default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def load_skills() -> dict[str, dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {entry["name"]: entry for entry in manifest["skills"]}


def install_skill(entry: dict, dest_root: Path, replace: bool) -> str:
    source = ROOT / entry["path"]
    target = dest_root / entry["name"]
    if not source.exists():
        raise FileNotFoundError(f"source skill not found: {source}")
    if target.exists():
        if not replace:
            raise FileExistsError(f"{target} already exists; pass --replace to overwrite")
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return str(target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install local skills from this checkout.")
    parser.add_argument("skills", nargs="*", help="Skill names to install. Defaults to all manifest skills.")
    parser.add_argument("--dest", default=str(default_dest()), help="Destination skills directory.")
    parser.add_argument("--replace", action="store_true", help="Replace existing destination skill directories.")
    args = parser.parse_args()

    skills = load_skills()
    names = args.skills or list(skills)
    unknown = [name for name in names if name not in skills]
    if unknown:
        print(f"ERROR: unknown skills: {', '.join(unknown)}", file=sys.stderr)
        return 1

    dest_root = Path(args.dest).expanduser()
    dest_root.mkdir(parents=True, exist_ok=True)

    for name in names:
        try:
            target = install_skill(skills[name], dest_root, args.replace)
        except Exception as exc:
            print(f"ERROR: {name}: {exc}", file=sys.stderr)
            return 1
        print(f"Installed {name} -> {target}")

    print("Restart Codex to pick up newly installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
