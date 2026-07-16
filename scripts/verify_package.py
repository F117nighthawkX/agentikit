"""Verify the Agentikit copyable-kit contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "LICENSE",
    ".agents/skills/commit-report/SKILL.md",
    ".agents/skills/long-task-workflow/SKILL.md",
    ".agents/skills/repo-change-planner/SKILL.md",
    "docs/agent/architecture-boundaries.md",
    "docs/agent/adr-template.md",
    "docs/agent/llm-runtime-guidance.md",
    "docs/adr/.gitkeep",
    "docs/adr/0001-keep-agent-guidance-in-copyable-files.md",
    "docs/plans/.gitkeep",
    "scripts/verify_package.py",
]

README_REUSABLE_PATHS = [
    "AGENTS.md",
    ".agents/skills/",
    "docs/agent/",
    "docs/adr/",
    "docs/plans/",
]

README_DISTRIBUTION_PHRASES = {
    "Choose any of these reusable components": (
        "README does not describe the kit paths as selectable components"
    ),
    "This README and the `scripts/` directory are source-repository files and should not be copied": (
        "README does not exclude its source-only overview and maintenance scripts"
    ),
    "The `docs/adr/` directory convention, recreated empty or copied with only `.gitkeep`": (
        "README does not define the reusable ADR directory convention"
    ),
    "The `docs/plans/` directory convention, recreated empty or copied with only `.gitkeep`": (
        "README does not define the reusable plan directory convention"
    ),
    "Files under `docs/adr/*.md` and `docs/plans/*.md` are repository-specific records and should not be copied.": (
        "README does not exclude repository-specific ADR and plan records"
    ),
}

SKILL_NAMES = {
    ".agents/skills/commit-report/SKILL.md": "commit-report",
    ".agents/skills/long-task-workflow/SKILL.md": "long-task-workflow",
    ".agents/skills/repo-change-planner/SKILL.md": "repo-change-planner",
}

AGENT_GUIDANCE_PHRASES = {
    "Do not optimize for the fewest imports, dependencies, API calls, lines, or the smallest diff.": (
        "AGENTS.md is missing the total-complexity rule"
    ),
    "A new import from one is not a new dependency.": (
        "AGENTS.md is missing the declared-dependency import distinction"
    ),
    "Prefer a focused, established, project-fitting dependency": (
        "AGENTS.md is missing the project-fitting dependency allowance"
    ),
    "Use language, platform, or standard-library capabilities": (
        "AGENTS.md is missing the native and standard-library safeguard"
    ),
    "Treat an ordinary, proportionate library addition as normal implementation.": (
        "AGENTS.md is missing the impact-based dependency approval boundary"
    ),
    "Keep broadly applicable agent rules in `AGENTS.md`, repeatable workflows in `.agents/skills/`, and longer task-specific guidance in `docs/agent/`.": (
        "AGENTS.md is missing the portable guidance ownership rule"
    ),
    "Agent-operational guidance must not exist only in a README.": (
        "AGENTS.md allows operational guidance to depend only on README"
    ),
    "Files under `docs/adr/` and `docs/plans/` are repository-specific records.": (
        "AGENTS.md is missing the repository-specific record boundary"
    ),
    "add a small tool-specific pointer to the canonical skill files": (
        "AGENTS.md is missing the cross-agent skill discovery fallback"
    ),
}

ADR_DECISION_PHRASES = {
    "Status: Accepted": "Agentikit's package-contract ADR is not accepted",
    "Agent-operational guidance must have an authoritative home": (
        "Agentikit's ADR is missing the agent-guidance authority decision"
    ),
    "`docs/adr/` and `docs/plans/` are reusable directory conventions": (
        "Agentikit's ADR is missing the directory and record distribution decision"
    ),
    "It will not attempt to determine semantic equivalence across documentation.": (
        "Agentikit's ADR is missing the verifier boundary"
    ),
}

ARCHITECTURE_GUIDANCE_PHRASES = {
    "Do not add or reject a dependency reflexively.": (
        "Architecture guidance is missing the balanced dependency rule"
    ),
    "A package present only transitively is not a declared project dependency": (
        "Architecture guidance is missing the transitive-dependency distinction"
    ),
    "An ordinary, proportionate library addition does not require separate design approval": (
        "Architecture guidance is missing the impact-based approval boundary"
    ),
    "Ask before adopting or replacing a major framework": (
        "Architecture guidance is missing the architecture-scale approval safeguard"
    ),
}

FORBIDDEN_DEPENDENCY_PHRASES = {
    "Do not add dependencies by default.": (
        "Architecture guidance restored the default-deny dependency rule"
    ),
    "New dependencies when a small local implementation or existing dependency is enough.": (
        "AGENTS.md restored the local-first dependency rule"
    ),
}

WORKFLOW_ACTIVATION_ANCHOR = "coordination or continuity risk"

WORKFLOW_ACTIVATION_PATHS = [
    "AGENTS.md",
    "README.md",
    ".agents/skills/long-task-workflow/SKILL.md",
    ".agents/skills/repo-change-planner/SKILL.md",
]

LONG_TASK_WORKFLOW_PHRASES = {
    "persistent source of truth": (
        "Long-task workflow is missing the authoritative tracker contract"
    ),
    "after any interruption": (
        "Long-task workflow is missing the interruption-resume contract"
    ),
    "revise or supersede": (
        "Long-task workflow is missing the material-drift contract"
    ),
    "Not verified:": (
        "Long-task workflow is missing the unverified-work reporting contract"
    ),
    "Use `$commit-report` only when explicitly requested": (
        "Long-task workflow is missing explicit commit-report delegation"
    ),
}

PLANNER_WORKFLOW_PHRASES = {
    "persistent source of truth": (
        "Planner workflow is missing the authoritative tracker contract"
    ),
    "after any interruption": (
        "Planner workflow is missing the interruption-resume contract"
    ),
    "revise or supersede": (
        "Planner workflow is missing the material-drift contract"
    ),
}

COMMIT_REPORT_WORKFLOW_PHRASES = {
    "This skill owns commit-message rules, report structure, and commit-style completion reports.": (
        "Commit-report workflow is missing its reporting-ownership contract"
    ),
}

FORBIDDEN_LONG_TASK_WORKFLOW_PHRASES = {
    "Then create an in-chat checklist.": (
        "Long-task workflow restored the duplicate in-chat checklist instruction"
    ),
    "Prefer durable records in this order:": (
        "Long-task workflow restored the ranked-records instruction"
    ),
    "Suggested commit message when useful.": (
        "Long-task workflow restored default commit-message guidance"
    ),
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

    for path in SOURCE_REQUIRED_FILES:
        if not (ROOT / path).is_file():
            errors.append(f"Missing required file: {path}")

    for path in ["docs/adr", "docs/plans", ".agents/skills", "docs/agent"]:
        if not (ROOT / path).is_dir():
            errors.append(f"Missing required directory: {path}")

    if errors:
        return report(errors)

    readme = read_text("README.md")
    for path in README_REUSABLE_PATHS:
        if path not in readme:
            errors.append(f"README is missing reusable path: {path}")
    for phrase, error in README_DISTRIBUTION_PHRASES.items():
        if phrase not in readme:
            errors.append(error)
    for phrase in [
        "hidden",
        "merge",
        "python scripts/verify_package.py",
        "docs/plans/*.md",
        "!docs/plans/.gitkeep",
    ]:
        if phrase not in readme:
            errors.append(f"README is missing maintainer/copy guidance: {phrase}")

    agents = read_text("AGENTS.md")
    for command in ["Install", "Test", "Lint", "Typecheck", "Build", "Format"]:
        if f"- {command}: `TODO`" not in agents:
            errors.append(f"AGENTS.md is missing template command: {command}")

    for phrase, error in AGENT_GUIDANCE_PHRASES.items():
        if phrase not in agents:
            errors.append(error)

    adr = read_text("docs/adr/0001-keep-agent-guidance-in-copyable-files.md")
    for phrase, error in ADR_DECISION_PHRASES.items():
        if phrase not in adr:
            errors.append(error)

    architecture = read_text("docs/agent/architecture-boundaries.md")
    for phrase, error in ARCHITECTURE_GUIDANCE_PHRASES.items():
        if phrase not in architecture:
            errors.append(error)

    dependency_guidance = agents + architecture
    for phrase, error in FORBIDDEN_DEPENDENCY_PHRASES.items():
        if phrase in dependency_guidance:
            errors.append(error)

    workflow_texts = {
        "AGENTS.md": agents,
        "README.md": readme,
        ".agents/skills/long-task-workflow/SKILL.md": read_text(
            ".agents/skills/long-task-workflow/SKILL.md"
        ),
        ".agents/skills/repo-change-planner/SKILL.md": read_text(
            ".agents/skills/repo-change-planner/SKILL.md"
        ),
    }
    for path in WORKFLOW_ACTIVATION_PATHS:
        if WORKFLOW_ACTIVATION_ANCHOR not in workflow_texts[path]:
            errors.append(
                f"{path} is missing workflow activation anchor: "
                f"{WORKFLOW_ACTIVATION_ANCHOR}"
            )

    long_task = workflow_texts[".agents/skills/long-task-workflow/SKILL.md"]
    for phrase, error in LONG_TASK_WORKFLOW_PHRASES.items():
        if phrase not in long_task:
            errors.append(
                f".agents/skills/long-task-workflow/SKILL.md: {error}: {phrase}"
            )
    for phrase, error in FORBIDDEN_LONG_TASK_WORKFLOW_PHRASES.items():
        if phrase in long_task:
            errors.append(
                f".agents/skills/long-task-workflow/SKILL.md: {error}: {phrase}"
            )
    if re.search(r"^Suggested commit message:$", long_task, flags=re.MULTILINE):
        errors.append(
            ".agents/skills/long-task-workflow/SKILL.md restored the standalone "
            "Suggested commit message: template heading"
        )

    planner = workflow_texts[".agents/skills/repo-change-planner/SKILL.md"]
    for phrase, error in PLANNER_WORKFLOW_PHRASES.items():
        if phrase not in planner:
            errors.append(
                f".agents/skills/repo-change-planner/SKILL.md: {error}: {phrase}"
            )

    commit_report = read_text(".agents/skills/commit-report/SKILL.md")
    for phrase, error in COMMIT_REPORT_WORKFLOW_PHRASES.items():
        if phrase not in commit_report:
            errors.append(
                f".agents/skills/commit-report/SKILL.md: {error}: {phrase}"
            )

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
