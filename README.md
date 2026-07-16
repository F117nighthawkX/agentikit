# Agentikit

Agentikit is a reusable, copyable rules and workflow kit for coding agents.

It provides a compact `AGENTS.md`, optional agent guidance docs, and reusable skills for common repository workflows like change planning, coordinated change execution, and commit-style reporting. The package is designed to stay small at the root while letting agents load deeper guidance only when the task calls for it.

## Origins

Agentikit started as a personal attempt to turn coding-agent advice into a reusable project setup.

The first version was based on ideas from [`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills), a Karpathy-inspired ruleset for reducing common LLM coding mistakes: unchecked assumptions, hidden confusion, overcomplicated implementations, unrelated edits, and weak verification loops.

From there, I reviewed several proposed changes and pull requests against that project, selected the parts that seemed broadly useful, and narrowed the guidance into a smaller, tool-neutral structure. The goal was not to copy every rule. It was to keep the pieces that improve coding-agent behavior, remove rules that felt too tool-specific or too heavy for normal work, and split longer workflows into optional docs or skills.

Agentikit keeps the same general spirit: agents should clarify before guessing, make surgical changes, preserve existing behavior, fit surrounding product patterns, avoid speculative abstractions, verify their work, and report uncertainty honestly. Here, surgical means minimizing unnecessary total complexity, not imports or dependency count: established, project-fitting dependencies are welcome when their benefits justify their footprint, while straightforward native logic should stay with the language, platform, or standard library. Agentikit adapts those ideas for `AGENTS.md`, reusable skills, and project guidance that can be shared across repositories.

This project is not affiliated with Andrej Karpathy, Multica, or the original `andrej-karpathy-skills` repository.

## Source Repository Contents

```text
AGENTS.md
README.md
docs/
  agent/
    architecture-boundaries.md
    adr-template.md
    llm-runtime-guidance.md
  adr/
    .gitkeep
    0001-keep-agent-guidance-in-copyable-files.md
  plans/
    .gitkeep
    *.md (repository-specific plans)
.agents/
  skills/
    commit-report/
      SKILL.md
    coordinate-change-execution/
      SKILL.md
    repo-change-planner/
      SKILL.md
scripts/
  verify_package.py
```

## How to Use

This README and the `scripts/` directory are source-repository files and should not be copied into a target repository. Agent-operational guidance has an authoritative home in the reusable files, so an agent using the kit does not depend on this README.

Choose any of these reusable components for the root of a target repository:

- `AGENTS.md`
- `.agents/skills/`
- `docs/agent/`
- The `docs/adr/` directory convention, recreated empty or copied with only `.gitkeep`
- The `docs/plans/` directory convention, recreated empty or copied with only `.gitkeep`

Files under `docs/adr/*.md` and `docs/plans/*.md` are repository-specific records and should not be copied. A target repository should create its own ADRs and plans in those directories.

The `.agents/` directory is hidden on some systems, so make sure your copy command includes hidden paths.

If the target repository already has an `AGENTS.md`, merge the relevant Agentikit guidance into the existing file instead of overwriting project-specific instructions.

Then update the `Project Commands` section in `AGENTS.md`:

```md
- Install: `TODO`
- Test: `TODO`
- Lint: `TODO`
- Typecheck: `TODO`
- Build: `TODO`
- Format: `TODO`
```

Keep `AGENTS.md` short and durable. Put repeatable task workflows into `.agents/skills/`, and put longer reference material in `docs/agent/`.

Generated plan files under `docs/plans/` are working artifacts, not durable documentation. In consuming repositories, consider ignoring generated plan markdown while keeping the placeholder tracked:

```gitignore
docs/plans/*.md
!docs/plans/.gitkeep
```

Use `docs/adr/` for durable architectural decisions belonging to the target repository after the relevant work is complete.

The `scripts/` directory is for maintaining this source repository only.

## Skills

Codex can discover repo-scoped skills from `.agents/skills/`.

Included skills:

- `$commit-report`: use only when explicitly requested for a current diff summary, suggested commit message, or commit-style report.
- `$coordinate-change-execution`: use for substantial repository changes with coordination or continuity risk, such as dependent phases, cross-layer work, unsafe partial states, migrations, refactors, or likely interruption.
- `$repo-change-planner`: use for focused follow-up planning that writes scoped epics, acceptance criteria, likely files, risks, verification notes, and a handoff prompt to `docs/plans/`.

Each skill is instruction-only and has a required `SKILL.md` with `name` and `description` metadata.

## Optional Reference Docs

Optional docs are not meant to be loaded every time. `AGENTS.md` points agents to them when the task calls for them:

- `docs/agent/architecture-boundaries.md`
- `docs/agent/adr-template.md`
- `docs/agent/llm-runtime-guidance.md`

## Recommended Placement

Use the package like this:

```text
repo-root/
  AGENTS.md
  .agents/
    skills/
      commit-report/
        SKILL.md
      coordinate-change-execution/
        SKILL.md
      repo-change-planner/
        SKILL.md
  docs/
    agent/
      architecture-boundaries.md
      adr-template.md
      llm-runtime-guidance.md
    adr/
      .gitkeep
    plans/
      .gitkeep
```

## Maintainer Checks

This repository intentionally does not use package-manager tooling. To verify the copyable kit structure after edits, run:

```bash
python scripts/verify_package.py
```

That check verifies required source paths, skill metadata, agent-visible ownership rules, README distribution instructions, and the Agentikit decision record for this contract.

## Cross-Agent Notes

Agentikit is centered on `AGENTS.md` and `.agents/skills/` because those paths are useful for Codex and can also serve as a tool-neutral convention for other coding agents.

The portable fallback for tools that do not automatically discover `.agents/skills/` is defined in `AGENTS.md`, so it travels with the kit.

## Attribution

Agentikit was influenced by `multica-ai/andrej-karpathy-skills` and the broader discussion around Andrej Karpathy's observations on LLM coding behavior. The structure and wording in this repository were adapted, condensed, and reorganized for tool-neutral `AGENTS.md` usage, reusable skills, and cross-repository workflows.

## Notes

- `AGENTS.md` should contain rules agents should apply broadly.
- Skills should contain repeatable workflows with clear triggers.
- Optional docs should contain longer guidance that is only relevant for some tasks.
- ADRs and plans should be created for the repository using the kit, not copied from another repository.
