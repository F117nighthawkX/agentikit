# Agentikit

Agentikit is a reusable, copyable rules and workflow kit for coding agents.

It provides a compact `AGENTS.md`, optional agent guidance docs, and reusable skills for common repository workflows like change planning, long-task execution, and commit-style reporting. The package is designed to stay small at the root while letting agents load deeper guidance only when the task calls for it.

## Origins

Agentikit started as a personal attempt to turn coding-agent advice into a reusable project setup.

The first version was based on ideas from [`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills), a Karpathy-inspired ruleset for reducing common LLM coding mistakes: unchecked assumptions, hidden confusion, overcomplicated implementations, unrelated edits, and weak verification loops.

From there, I reviewed several proposed changes and pull requests against that project, selected the parts that seemed broadly useful, and narrowed the guidance into a smaller, tool-neutral structure. The goal was not to copy every rule. It was to keep the pieces that improve coding-agent behavior, remove rules that felt too tool-specific or too heavy for normal work, and split longer workflows into optional docs or skills.

Agentikit keeps the same general spirit: agents should clarify before guessing, make surgical changes, preserve existing behavior, fit surrounding product patterns, avoid speculative abstractions, verify their work, and report uncertainty honestly. It adapts those ideas for `AGENTS.md`, reusable skills, and project guidance that can be shared across repositories.

This project is not affiliated with Andrej Karpathy, Multica, or the original `andrej-karpathy-skills` repository.

## Contents

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
.agents/
  skills/
    commit-report/
      SKILL.md
    long-task-workflow/
      SKILL.md
    repo-change-planner/
      SKILL.md
scripts/
  verify_package.py
```

## How to Use

Copy these paths into the root of a repository:

- `AGENTS.md`
- `.agents/skills/`
- `docs/agent/`
- `docs/adr/`

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

The `scripts/` directory is for maintaining this source repository. It does not need to be copied into target repositories.

## Skills

Codex can discover repo-scoped skills from `.agents/skills/`.

Included skills:

- `$commit-report`: use for current diff summaries, suggested commit messages, commit-style completion reports, or final reports based on repository changes.
- `$long-task-workflow`: use for large multi-file tasks, staged implementations, refactors, migrations, checklists, phased verification, handoff notes, or structured final reports.
- `$repo-change-planner`: use for focused follow-up planning with scoped epics, acceptance criteria, likely files, risks, and verification notes.

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
      long-task-workflow/
        SKILL.md
      repo-change-planner/
        SKILL.md
  docs/
    agent/
      architecture-boundaries.md
      adr-template.md
      llm-runtime-guidance.md
    adr/
```

## Maintainer Checks

This repository intentionally does not use package-manager tooling. To verify the copyable kit structure after edits, run:

```bash
python scripts/verify_package.py
```

That check verifies the expected paths, skill metadata, README copy instructions, and tracked ADR placeholder.

## Cross-Agent Notes

Agentikit is centered on `AGENTS.md` and `.agents/skills/` because those paths are useful for Codex and can also serve as a tool-neutral convention for other coding agents.

If another agent does not automatically discover `.agents/skills/`, keep the source files here and add a small tool-specific pointer rather than forking the rules. Avoid maintaining duplicate skill copies unless the tool requires it.

## Attribution

Agentikit was influenced by `multica-ai/andrej-karpathy-skills` and the broader discussion around Andrej Karpathy's observations on LLM coding behavior. The structure and wording in this repository were adapted, condensed, and reorganized for tool-neutral `AGENTS.md` usage, reusable skills, and cross-repository workflows.

## Notes

- `AGENTS.md` should contain rules agents should apply broadly.
- Skills should contain repeatable workflows with clear triggers.
- Optional docs should contain longer guidance that is only relevant for some tasks.
- ADRs should be added under `docs/adr/` only when a durable technical decision needs to be recorded.
