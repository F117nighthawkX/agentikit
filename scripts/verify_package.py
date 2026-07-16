"""Verify the Agentikit copyable-kit contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CHANGE_EXECUTION_SKILL_NAME = "coordinate-change-execution"
CHANGE_EXECUTION_SKILL_PATH = (
    f".agents/skills/{CHANGE_EXECUTION_SKILL_NAME}/SKILL.md"
)
LEGACY_CHANGE_EXECUTION_SKILL_NAME = "long-task-workflow"
LEGACY_CHANGE_EXECUTION_SKILL_PATH = (
    f".agents/skills/{LEGACY_CHANGE_EXECUTION_SKILL_NAME}"
)

SOURCE_REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "LICENSE",
    ".agents/skills/commit-report/SKILL.md",
    CHANGE_EXECUTION_SKILL_PATH,
    ".agents/skills/repo-change-planner/SKILL.md",
    "docs/agent/architecture-boundaries.md",
    "docs/agent/adr-template.md",
    "docs/agent/llm-runtime-guidance.md",
    "docs/adr/.gitkeep",
    "docs/adr/0001-keep-agent-guidance-in-copyable-files.md",
    "docs/plans/.gitkeep",
    "scripts/verify_package.py",
]

SOURCE_FORBIDDEN_PATHS = [
    LEGACY_CHANGE_EXECUTION_SKILL_PATH,
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

README_COMMIT_REPORT_ROUTE_PREFIX = "- `$commit-report`:"

README_COMMIT_REPORT_ROUTE_PHRASES = {
    "explicitly requested": (
        "README does not restrict commit-report routing to explicit requests"
    ),
}

README_FORBIDDEN_COMMIT_REPORT_ROUTE_PHRASES = {
    "or final reports based on repository changes": (
        "README still routes ordinary final reports to commit-report"
    ),
}

SKILL_NAMES = {
    ".agents/skills/commit-report/SKILL.md": "commit-report",
    CHANGE_EXECUTION_SKILL_PATH: CHANGE_EXECUTION_SKILL_NAME,
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
    CHANGE_EXECUTION_SKILL_PATH,
    ".agents/skills/repo-change-planner/SKILL.md",
]

CHANGE_EXECUTION_ROUTE_PATHS = [
    "AGENTS.md",
    "README.md",
    ".agents/skills/repo-change-planner/SKILL.md",
]

COORDINATE_CHANGE_EXECUTION_DISCOVERY_PHRASES = {
    WORKFLOW_ACTIVATION_ANCHOR: (
        "Coordinate-change-execution frontmatter is missing its positive discovery trigger"
    ),
    "planning-only": (
        "Coordinate-change-execution frontmatter is missing the planning-only exclusion"
    ),
    "report-only": (
        "Coordinate-change-execution frontmatter is missing the report-only exclusion"
    ),
    "simple mechanical": (
        "Coordinate-change-execution frontmatter is missing the mechanical-work exclusion"
    ),
    "verification that later edits can make stale": (
        "Coordinate-change-execution frontmatter is missing the verification-freshness trigger"
    ),
}

TRACKER_COMPOSITION_PHRASES = {
    "conceptual execution phases onto": (
        "Workflow is missing planner-checklist phase mapping"
    ),
    "same item identities and statuses": (
        "Workflow is missing mirror identity and status alignment"
    ),
    "independent completion claims": (
        "Workflow allows a mirror to become a competing tracker"
    ),
}

COORDINATE_CHANGE_EXECUTION_WORKFLOW_PHRASES = {
    "persistent source of truth": (
        "Coordinate-change-execution is missing the authoritative tracker contract"
    ),
    "after any interruption": (
        "Coordinate-change-execution is missing the interruption-resume contract"
    ),
    "revise or supersede": (
        "Coordinate-change-execution is missing the material-drift contract"
    ),
    "Not verified:": (
        "Coordinate-change-execution is missing the unverified-work reporting contract"
    ),
    "Use `$commit-report` only when explicitly requested": (
        "Coordinate-change-execution is missing explicit commit-report delegation"
    ),
    "sole status-bearing execution tracker": (
        "Coordinate-change-execution is missing the single-tracker fallback"
    ),
    "Identify the progress authority before creating or updating tracker state": (
        "Coordinate-change-execution is missing authority-before-state ordering"
    ),
    "may reorder or add steps but must not omit or weaken these outcomes": (
        "Coordinate-change-execution allows project checks to replace the final gate"
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
    "Every applicable `AGENTS.md` file": (
        "Planner workflow does not require all applicable scoped instructions"
    ),
}

PLANNER_HANDOFF_DIRECTIVE_ANCHOR = (
    "Include this directive verbatim in the handoff prompt, "
    "replacing the placeholder path:"
)

COMMIT_REPORT_WORKFLOW_PHRASES = {
    "This skill owns commit-message rules, report structure, and commit-style completion reports.": (
        "Commit-report workflow is missing its reporting-ownership contract"
    ),
}

FORBIDDEN_COORDINATE_CHANGE_EXECUTION_WORKFLOW_PHRASES = {
    "Then create an in-chat checklist.": (
        "Coordinate-change-execution restored the duplicate in-chat checklist instruction"
    ),
    "Prefer durable records in this order:": (
        "Coordinate-change-execution restored the ranked-records instruction"
    ),
    "Suggested commit message when useful.": (
        "Coordinate-change-execution restored default commit-message guidance"
    ),
}

FRONTMATTER_PATTERN = re.compile(
    r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)",
    flags=re.DOTALL,
)


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> str | None:
    match = FRONTMATTER_PATTERN.match(text)
    return match.group("body") if match else None


def frontmatter_field_value(frontmatter: str, field: str) -> str | None:
    match = re.search(
        rf"^{re.escape(field)}:[ \t]*(.+)$",
        frontmatter,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def extract_fenced_text_block_after(text: str, anchor: str) -> str | None:
    position = text.find(anchor)
    if position < 0:
        return None

    match = re.match(
        r"\s*```text\n(?P<body>.*?)\n```",
        text[position + len(anchor) :],
        flags=re.DOTALL,
    )
    return match.group("body") if match else None


def main() -> int:
    errors: list[str] = []

    for path in SOURCE_REQUIRED_FILES:
        if not (ROOT / path).is_file():
            errors.append(f"Missing required file: {path}")

    for path in SOURCE_FORBIDDEN_PATHS:
        if (ROOT / path).exists():
            errors.append(f"Obsolete source path remains after skill rename: {path}")

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

    commit_report_route = next(
        (
            line
            for line in readme.splitlines()
            if line.startswith(README_COMMIT_REPORT_ROUTE_PREFIX)
        ),
        None,
    )
    if commit_report_route is None:
        errors.append("README is missing the `$commit-report` skill route")
    else:
        for phrase, error in README_COMMIT_REPORT_ROUTE_PHRASES.items():
            if phrase not in commit_report_route:
                errors.append(error)
        for phrase, error in README_FORBIDDEN_COMMIT_REPORT_ROUTE_PHRASES.items():
            if phrase in commit_report_route:
                errors.append(error)

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

    skill_texts = {path: read_text(path) for path in SKILL_NAMES}
    skill_frontmatter: dict[str, str] = {}
    for path, name in SKILL_NAMES.items():
        frontmatter = extract_frontmatter(skill_texts[path])
        if frontmatter is None:
            errors.append(f"{path} is missing bounded YAML frontmatter")
            continue

        skill_frontmatter[path] = frontmatter
        if frontmatter_field_value(frontmatter, "name") != name:
            errors.append(f"{path} has missing or incorrect skill name")
        if not frontmatter_field_value(frontmatter, "description"):
            errors.append(f"{path} is missing skill description")

    change_execution_frontmatter = skill_frontmatter.get(CHANGE_EXECUTION_SKILL_PATH)
    if change_execution_frontmatter is not None:
        change_execution_description = frontmatter_field_value(
            change_execution_frontmatter,
            "description",
        )
        if change_execution_description:
            for phrase, error in (
                COORDINATE_CHANGE_EXECUTION_DISCOVERY_PHRASES.items()
            ):
                if phrase not in change_execution_description:
                    errors.append(
                        f"{CHANGE_EXECUTION_SKILL_PATH}: "
                        f"{error}: {phrase}"
                    )

    workflow_texts = {
        "AGENTS.md": agents,
        "README.md": readme,
        CHANGE_EXECUTION_SKILL_PATH: skill_texts[CHANGE_EXECUTION_SKILL_PATH],
        ".agents/skills/repo-change-planner/SKILL.md": skill_texts[
            ".agents/skills/repo-change-planner/SKILL.md"
        ],
    }
    for path in WORKFLOW_ACTIVATION_PATHS:
        if WORKFLOW_ACTIVATION_ANCHOR not in workflow_texts[path]:
            errors.append(
                f"{path} is missing workflow activation anchor: "
                f"{WORKFLOW_ACTIVATION_ANCHOR}"
            )

    route_anchor = f"`${CHANGE_EXECUTION_SKILL_NAME}`"
    for path in CHANGE_EXECUTION_ROUTE_PATHS:
        if route_anchor not in workflow_texts[path]:
            errors.append(
                f"{path} is missing change-execution skill route: {route_anchor}"
            )
        if LEGACY_CHANGE_EXECUTION_SKILL_NAME in workflow_texts[path]:
            errors.append(
                f"{path} still routes to the renamed skill: "
                f"{LEGACY_CHANGE_EXECUTION_SKILL_NAME}"
            )

    change_execution = workflow_texts[CHANGE_EXECUTION_SKILL_PATH]
    for phrase, error in COORDINATE_CHANGE_EXECUTION_WORKFLOW_PHRASES.items():
        if phrase not in change_execution:
            errors.append(
                f"{CHANGE_EXECUTION_SKILL_PATH}: "
                f"{error}: {phrase}"
            )
    for phrase, error in TRACKER_COMPOSITION_PHRASES.items():
        if phrase not in change_execution:
            errors.append(
                f"{CHANGE_EXECUTION_SKILL_PATH}: "
                f"{error}: {phrase}"
            )
    for phrase, error in (
        FORBIDDEN_COORDINATE_CHANGE_EXECUTION_WORKFLOW_PHRASES.items()
    ):
        if phrase in change_execution:
            errors.append(
                f"{CHANGE_EXECUTION_SKILL_PATH}: "
                f"{error}: {phrase}"
            )
    if re.search(
        r"^Suggested commit message:$",
        change_execution,
        flags=re.MULTILINE,
    ):
        errors.append(
            f"{CHANGE_EXECUTION_SKILL_PATH} restored the standalone "
            "Suggested commit message: template heading"
        )

    planner = workflow_texts[".agents/skills/repo-change-planner/SKILL.md"]
    for phrase, error in PLANNER_WORKFLOW_PHRASES.items():
        if phrase not in planner:
            errors.append(
                f".agents/skills/repo-change-planner/SKILL.md: {error}: {phrase}"
            )

    planner_directive = extract_fenced_text_block_after(
        planner,
        PLANNER_HANDOFF_DIRECTIVE_ANCHOR,
    )
    if planner_directive is None:
        errors.append(
            ".agents/skills/repo-change-planner/SKILL.md is missing its "
            "required handoff directive block"
        )
    else:
        for phrase, error in TRACKER_COMPOSITION_PHRASES.items():
            if phrase not in planner_directive:
                errors.append(
                    ".agents/skills/repo-change-planner/SKILL.md: "
                    f"{error} in the generated handoff directive: {phrase}"
                )

    commit_report = skill_texts[".agents/skills/commit-report/SKILL.md"]
    for phrase, error in COMMIT_REPORT_WORKFLOW_PHRASES.items():
        if phrase not in commit_report:
            errors.append(
                f".agents/skills/commit-report/SKILL.md: {error}: {phrase}"
            )

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
