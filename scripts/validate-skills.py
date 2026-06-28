#!/usr/bin/env python3
"""Validate the skill collection without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills.manifest.json"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._/-]+")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated YAML frontmatter")

    raw = text[4:end]
    data: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_value
        if current_key is not None:
            data[current_key] = "\n".join(current_value).strip()
        current_key = None
        current_value = []

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            if current_key is None:
                raise ValueError(f"frontmatter continuation without key: {line!r}")
            current_value.append(line.strip())
            continue
        flush()
        if ":" not in line:
            raise ValueError(f"frontmatter line is not key/value: {line!r}")
        key, value = line.split(":", 1)
        current_key = key.strip()
        current_value = [value.strip()]
    flush()
    return data, text[end + 5 :]


def load_manifest() -> dict:
    if not MANIFEST.exists():
        raise ValueError("skills.manifest.json is missing")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def validate_openai_yaml(skill_dir: Path, name: str) -> list[str]:
    errors: list[str] = []
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [f"{skill_dir.name}: missing agents/openai.yaml"]
    text = path.read_text(encoding="utf-8")
    required = [
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"{skill_dir.name}: agents/openai.yaml missing {marker}")
    if f"${name}" not in text:
        errors.append(f"{skill_dir.name}: default_prompt must mention ${name}")
    return errors


def validate_skill(skill_dir: Path, manifest_entry: dict | None) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    try:
        frontmatter, body = parse_frontmatter(skill_md)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    extra_keys = sorted(set(frontmatter) - {"name", "description"})

    if not name:
        errors.append(f"{skill_dir.name}: frontmatter missing name")
    elif not NAME_RE.match(name):
        errors.append(f"{skill_dir.name}: invalid skill name {name!r}")
    elif name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name {name!r} must match directory name")

    if not description:
        errors.append(f"{skill_dir.name}: frontmatter missing description")
    if extra_keys:
        errors.append(f"{skill_dir.name}: unsupported frontmatter keys: {', '.join(extra_keys)}")
    if not body.strip():
        errors.append(f"{skill_dir.name}: SKILL.md body is empty")

    if (skill_dir / "README.md").exists():
        errors.append(f"{skill_dir.name}: do not put README.md inside a skill directory")

    for reference in sorted(set(REFERENCE_RE.findall(body))):
        reference_path = skill_dir / reference
        if not reference_path.exists():
            errors.append(f"{skill_dir.name}: referenced file is missing: {reference}")

    if manifest_entry is None:
        errors.append(f"{skill_dir.name}: missing from skills.manifest.json")
    else:
        if manifest_entry.get("name") != name:
            errors.append(f"{skill_dir.name}: manifest name must be {name!r}")
        if manifest_entry.get("path") != skill_dir.name:
            errors.append(f"{skill_dir.name}: manifest path must be {skill_dir.name!r}")
        if not manifest_entry.get("description"):
            errors.append(f"{skill_dir.name}: manifest description is empty")
        apps = manifest_entry.get("apps", {})
        if not apps.get("codex"):
            errors.append(f"{skill_dir.name}: manifest apps.codex must be true")

    if name:
        errors.extend(validate_openai_yaml(skill_dir, name))
    return errors


def find_skill_dirs() -> list[Path]:
    return sorted(path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skills in this repository.")
    parser.add_argument("--list", action="store_true", help="List manifest skills without full validation")
    args = parser.parse_args()

    try:
        manifest = load_manifest()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    manifest_skills = manifest.get("skills", [])
    manifest_by_path = {entry.get("path"): entry for entry in manifest_skills}

    if args.list:
        for entry in manifest_skills:
            print(f"{entry.get('name')}	{entry.get('path')}")
        return 0

    errors: list[str] = []
    skill_dirs = find_skill_dirs()
    if not skill_dirs:
        errors.append("no skill directories found")

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir, manifest_by_path.get(skill_dir.name)))

    actual_paths = {path.name for path in skill_dirs}
    for entry in manifest_skills:
        path = entry.get("path")
        if path not in actual_paths:
            errors.append(f"manifest path does not contain a skill: {path}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
