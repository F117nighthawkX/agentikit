"""Verify the Agentikit copyable-kit contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "LICENSE",
    ".agents/skills/commit-report/SKILL.md",
    ".agents/skills/long-task-workflow/SKILL.md",
    "docs/agent/architecture-boundaries.md",
    "docs/agent/adr-template.md",
    "docs/agent/llm-runtime-guidance.md",
    "docs/adr/.gitkeep",
    "scripts/verify_package.py",
]

README_COPY_PATHS = [
    "AGENTS.md",
    ".agents/skills/",
    "docs/agent/",
    "docs/adr/",
]

SKILL_NAMES = {
    ".agents/skills/commit-report/SKILL.md": "commit-report",
    ".agents/skills/long-task-workflow/SKILL.md": "long-task-workflow",
}


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def has_frontmatter_field(text: str, field: str, value: str | None = None) -> bool:
    pattern = rf"^{re.escape(field)}:\s*(.+)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return False
    return value is None or match.group(1).strip() == value


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            errors.append(f"Missing required file: {path}")

    for path in ["docs/adr", ".agents/skills", "docs/agent"]:
        if not (ROOT / path).is_dir():
            errors.append(f"Missing required directory: {path}")

    if errors:
        return report(errors)

    readme = read_text("README.md")
    for path in README_COPY_PATHS:
        if path not in readme:
            errors.append(f"README is missing copy path: {path}")
    for phrase in ["hidden", "merge", "python scripts/verify_package.py"]:
        if phrase not in readme:
            errors.append(f"README is missing maintainer/copy guidance: {phrase}")

    agents = read_text("AGENTS.md")
    for command in ["Install", "Test", "Lint", "Typecheck", "Build", "Format"]:
        if f"- {command}: `TODO`" not in agents:
            errors.append(f"AGENTS.md is missing template command: {command}")

    for path, name in SKILL_NAMES.items():
        skill = read_text(path)
        if not skill.startswith("---\n"):
            errors.append(f"{path} is missing YAML frontmatter")
        if not has_frontmatter_field(skill, "name", name):
            errors.append(f"{path} has missing or incorrect skill name")
        if not has_frontmatter_field(skill, "description"):
            errors.append(f"{path} is missing skill description")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print("Agentikit package verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agentikit package verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
