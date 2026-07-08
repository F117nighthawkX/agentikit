---
name: repo-change-planner
description: Use for planning focused follow-up changes in an existing repo. Writes a scoped implementation brief with 1 to 5 epics, acceptance criteria, likely files, risks, verification notes, and a handoff prompt to docs/plans/<plan-title>.md, or explains why the request is too broad and suggests ways to split it.
---

# Repo Change Planner Skill

Use this skill to turn a focused implementation request for an existing repository into a clean implementation brief.

This skill plans only. It may create a new plan file under `docs/plans/`, but it must not implement the requested code change and must not produce a completion report.

The output should be something the user can feed to Codex or another coding agent.

Read first:

- `AGENTS.md` for repository-specific commands, safety, scope, verification, and communication guidance.

## When to Use This

Use this skill when:

- The repository already exists.
- Stack, framework, structure, and setup decisions are already made.
- The user has a focused follow-up request.
- The request is larger than a simple one-line fix.
- The request can probably be described in 1 to 5 implementation epics, or is close enough that the planner should explain why it should be split before implementation.
- The user wants a plan before giving the work to an implementation agent.

Good examples:

- Plan a new route and related navigation changes.
- Plan a focused UI update across existing components.
- Plan changes to an existing workflow.
- Plan a small data model change with matching UI behavior.
- Plan a focused test addition.
- Plan a feature refinement without changing the larger architecture.

Do not use this skill for:

- New app planning.
- Full product discovery.
- Stack selection from scratch.
- Large roadmap generation.
- Direct implementation.
- Large staged execution.
- Migrations or refactors that already need `$long-task-workflow`.

## Relationship to Other Skills

Use `$repo-change-planner` to create the implementation brief.

Use `$long-task-workflow` later if one of the planned epics is large, risky, multi-phase, or touches several layers.

Use `$commit-report` only after implementation, when the user asks for a current diff summary, suggested commit message, or commit-style completion report.

## Planning Rules

- Inspect enough repo context to avoid guessing.
- Do not implement the requested code change.
- Do not run full product discovery.
- Do not revisit stack decisions unless the request requires it.
- Do not add speculative features.
- Include relevant regression-preservation and product-fit criteria: existing nearby behavior should remain intact unless explicitly changed, and UI work should fit surrounding layout, spacing, alignment, animation, placement, interaction flow, and style.
- Match the repo's existing structure and patterns in the plan.
- Keep the plan scoped to the user's request.
- Do not force-fit broad work into 5 epics. If the request needs more than 5 coherent epics, requires product discovery, mixes unrelated goals, or depends on unresolved architecture decisions, use the "Request Too Broad" output instead of an implementation brief.
- Separate known facts, assumptions, and open questions.
- Mark anything that needs user confirmation before implementation.
- Write acceptance criteria that can be tested.
- Write the full plan to a new file under `docs/plans/` instead of printing the full plan in chat.
- Use a filesystem-safe slug derived from the implementation brief title for the plan filename, such as `docs/plans/add-settings-route.md`.
- If `docs/plans/` does not exist, create it before writing the plan file.
- If the target plan filename already exists, ask before overwriting it. Do not overwrite an existing plan file silently.

## Repo Context to Inspect

Look for:

- Routes
- Pages
- Components
- Data structures
- Shared constants
- Styling patterns
- Animation patterns
- Tests
- Package scripts
- Build, lint, typecheck, and test commands

Do not guess file names. If repo access is incomplete, state what could not be inspected.

## Plan File Rules

The plan file is a working artifact for coordinating implementation. It is not durable project documentation and must not be treated as the source of truth for project decisions or implementation details.

Plans can become stale as the user, contributors, or other agents make changes beyond the scope of a particular plan. Agents and users should follow `AGENTS.md` section `7. Documentation and Decisions` for durable documentation, and create an ADR only when applicable after the relevant epic or plan has been completed.

After writing a plan file:

- Do not update plan detail sections such as requested change, assumptions, open questions, out of scope, epics, acceptance criteria, likely files, risks, verification plan, or handoff prompt.
- Only update checklist state and brief notes under the relevant checklist item.
- If a problem arises during execution, such as command access, implementation issues, or test failures, add a concise note below the checklist item in question.
- Mark an epic checklist item complete only after that epic's acceptance criteria have been met.

Every normal implementation brief plan file must include a checklist before the implementation epics:

```md
## Execution Checklist

- [ ] User confirmed assumptions are valid.
- [ ] Open questions are resolved or explicitly accepted as non-blocking.
- [ ] Epic 1 acceptance criteria met.
- [ ] Epic 2 acceptance criteria met.
- [ ] Epic 3 acceptance criteria met.
- [ ] Verification plan completed.
- [ ] ADR need considered after completion, following `AGENTS.md` section `7. Documentation and Decisions`.
```

Adjust the number of epic checklist items to match the plan. If there are no open questions, keep the open-question checklist item and mark it complete only when implementation begins with that fact still true.

## Required Output

If the request is too broad to plan responsibly in 1 to 5 epics, do not produce the normal implementation brief. Produce a "Request Too Broad" response in chat using this structure:

# Request Too Broad: [Short Task Name]

## Why This Should Be Split

Explain the concrete scope problem. Name whether the issue is too many unrelated outcomes, too many layers, missing product decisions, unresolved architecture choices, migration risk, unclear acceptance criteria, or another specific blocker.

## What Can Be Planned Now

List any coherent subset that can be planned safely with the current repo context.

If no subset can be planned safely, state that and explain what information is missing.

## Recommended Split Options

Suggest 2 to 5 viable ways to break the request into focused follow-up prompts.

For each option, include:

- Suggested prompt
- Expected scope
- Why this split is safer
- Whether `$repo-change-planner` or `$long-task-workflow` should be used next

## Questions Before Planning

List the decisions or missing information that would make the next planning request focused enough.

Only write a normal implementation brief file when the request fits in 1 to 5 coherent epics.

---

For a normal implementation brief, write the full plan to `docs/plans/<plan-title>.md` using this structure:

# Implementation Brief: [Short Task Name]

## Requested Change

Restate the user's request in your own words.

## Existing Context Found

List the relevant files, components, routes, data structures, styles, tests, or commands found in the repo.

## Assumptions

List only assumptions that affect implementation.

Mark assumptions that need confirmation before coding.

## Open Questions

List questions that block implementation or could change user-facing behavior, routing, data shape, animation behavior, persistence, or public APIs.

If there are no blocking questions, state that.

## Plan File Use

State that this plan is a working artifact, not a durable source of truth.

State that plan details must not be updated after the file is written. Only checklist state and brief notes under checklist items may be updated.

State that users and agents should follow `AGENTS.md` section `7. Documentation and Decisions` for durable documentation, and create an ADR only when applicable after the relevant epic or plan has been completed.

## Execution Checklist

Include the checklist described in "Plan File Rules."

## Out of Scope

List nearby work that should not be changed.

Include tempting cleanup, unrelated refactors, unrelated styling updates, and future-version behavior.

## Implementation Epics

Create 1 to 5 epics.

For each epic, use:

### Epic [number]: [name]

#### Goal

#### Tasks

#### Acceptance Criteria

Use testable criteria.

Prefer:

- Given [state], when [action], then [result].
- Verify [behavior] by [test, build, or manual check].
- The implementation must not [forbidden behavior].
- Existing [nearby behavior] remains intact, or [new UI] follows surrounding [layout, spacing, placement, interaction, or style] conventions.

#### Likely Files or Areas

List expected files or areas.

#### Risks

List implementation risks.

#### Recommended Execution Skill

Use one:

- Root `AGENTS.md` only
- `$long-task-workflow`

Choose `$long-task-workflow` if the epic touches several files or layers, has multiple phases, has real tradeoffs or unknowns, needs more than one verification command or manual check, or would be risky if partially implemented.

## Verification Plan

List the narrowest checks that would prove the full request works.

Include available commands when known:

- Format
- Lint
- Typecheck
- Unit tests
- UI tests
- Build
- Manual browser or device checks

Do not claim these checks were run unless they were actually run while planning.

## Suggested Handoff Prompt

Write a concise prompt the user can paste into an implementation agent.

The handoff prompt should include:

- The plan file path
- The requested change
- The selected epic or epics
- The relevant assumptions
- The acceptance criteria
- The verification plan
- Whether to use `$long-task-workflow`

After writing the plan file, respond in chat with only an abridged version:

````md
Created plan file: `docs/plans/<plan-title>.md`

## Requested Change

<brief restatement>

## Assumptions

- <assumption>

## Open Questions

- <question, or "No blocking open questions.">

## Epics

- Epic 1: <title> - <goal>
- Epic 2: <title> - <goal>

## Handoff Prompt

```text
<copyable handoff prompt that references docs/plans/<plan-title>.md>
```
````

Do not print the full plan in chat.
