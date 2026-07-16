---
name: repo-change-planner
description: Use for planning focused follow-up changes in an existing repo. Resolves material assumptions and questions before writing a scoped implementation brief with 1 to 5 epics, acceptance criteria, likely files, risks, verification notes, and a handoff prompt to docs/plans/<plan-title>.md, or explains why the request is too broad and suggests ways to split it.
---

# Repo Change Planner Skill

Use this skill to turn a focused implementation request for an existing repository into a clean implementation brief.

This skill plans only. It may create a new plan file under `docs/plans/`, but it must not implement the requested change or produce a completion report.

The output should be something the user can feed to Codex or another coding agent.

Read first:

- Every applicable `AGENTS.md` file for the areas being planned, including repository-specific commands, safety, scope, verification, and communication guidance.

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
- Direct implementation, including large staged execution. This skill may still plan a focused request that will later use `$coordinate-change-execution`.

## Relationship to Other Skills

- Use `$repo-change-planner` to create the implementation brief.
- Use `$coordinate-change-execution` later when implementation has coordination or continuity risk, such as dependent phases, cross-layer work, unsafe partial states, migrations, refactors, or likely interruption.
- Use `$commit-report` only after implementation, when the user asks for a current diff summary, suggested commit message, or commit-style completion report.

## Planning Rules

- Inspect enough repo context to avoid guessing.
- Do not implement the requested code change.
- Do not run full product discovery.
- Do not revisit stack decisions unless the request requires it.
- Do not add speculative features.
- Include relevant regression-preservation and product-fit criteria.
- Match the repo's existing structure and patterns in the plan.
- Keep the plan scoped to the user's request.
- Choose the smallest number of coherent epics that accurately represents the work, from 1 to 5. Use one epic when the request is one cohesive implementation outcome, and add another only when it represents a meaningfully distinct outcome or workstream.
- Do not default to 3 epics, pad the plan to reach a preferred count, or split setup, implementation, verification, documentation, or cleanup into separate epics unless they are independently meaningful parts of the requested change.
- Do not force-fit broad work into 5 epics. If the request needs more than 5 coherent epics, requires product discovery, mixes unrelated goals, or depends on unresolved architecture decisions, use the "Request Too Broad" output instead of an implementation brief.
- Separate known facts, assumptions, and questions while drafting.
- Resolve every question and any material assumption needing confirmation before finalizing the plan.
- Write acceptance criteria that can be tested.
- Write the full plan to a new file under `docs/plans/` instead of printing the full plan in chat. Use a filesystem-safe slug derived from the title, such as `docs/plans/add-settings-route.md`.
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

## Pre-Finalization Follow-up

After inspecting repository context, identify candidate assumptions and questions before writing the plan file or final handoff prompt.

If an answer could materially change scope, user-facing behavior, routing, data shape, persistence, public APIs, acceptance criteria, verification, or the selected epics:

1. Ask the user a concise, numbered set of direct questions in chat.
2. Include a candidate assumption for confirmation only when confirming or correcting it could change the plan.
3. Do not create the plan file or present a handoff prompt yet.
4. Wait for the user's answers. The user may answer inline without following a special form.

Use this chat structure, omitting an empty subsection:

```md
## Planning Follow-up

### Assumptions to Confirm

1. <assumption to confirm or correct>

### Questions

1. <direct question>
```

If no material follow-up is needed, proceed directly to the normal implementation brief.

After the user answers, perform a focused refinement pass across the entire plan and handoff prompt. Integrate each answer into every affected section, including requested change, assumptions, out of scope, epics, acceptance criteria, risks, verification, and handoff wording. Do not append an answer log or preserve stale draft wording.

Retain only assumptions the implementation agent still needs and that are not already expressed clearly elsewhere in the plan. Remove assumptions that the user's answers converted into requirements or that became redundant. Resolve and remove every planning question. If any question remains, ask another follow-up instead of finalizing the normal implementation brief.

## Plan File Rules

The plan file is a working artifact, not durable project documentation. Durable decisions belong in `docs/adr/` only when `AGENTS.md` and `docs/agent/adr-template.md` call for an ADR.

During normal execution after writing a plan file:

- Do not update plan detail sections such as requested change, assumptions, out of scope, epics, acceptance criteria, likely files, risks, verification plan, or handoff prompt.
- Only update checklist state and brief notes under the relevant checklist item.
- If command access, implementation issues, or test failures arise during execution, add a concise note below the checklist item in question.
- Mark an epic checklist item complete only after that epic's acceptance criteria have been met.

When `$coordinate-change-execution` executes the brief, map its conceptual 2-to-5 execution phases onto these checklist items instead of creating another status-bearing tracker. A native or in-chat view may mirror only the same item identities and statuses and must not make independent completion claims.

### Material Plan Drift and Approved Revisions

Plan drift is material when implementation evidence means the brief can no longer be followed accurately, an assumption, scope boundary, acceptance criterion, or out-of-scope rule must change, verification would be weakened, or an applicable `AGENTS.md` confirmation boundary is triggered.

When material drift occurs during execution:

1. Stop before divergent code or plan-detail edits.
2. Leave affected checklist items incomplete and add a concise evidence note.
3. Explain the affected sections, meaningful options and tradeoffs, and a recommendation.
4. Require explicit user approval to revise or supersede the brief. A generic instruction to continue is not approval unless it clearly accepts the proposed change.

After explicit approval:

- Revise the existing brief in place only when it remains the same focused 1-to-5-epic request. Return to this planning workflow, update every affected section and the handoff prompt atomically, add a concise approved-revision note under `Plan File Use`, preserve unaffected evidence, and reset affected epic and verification checklist state.
- If the work becomes broader, different, or no longer fits this planner, split it or create a new plan file. Designate the new brief as the persistent source of truth and leave the old brief read-only apart from a concise checklist note linking to its successor.
- If approval is denied, follow the original brief only when it remains viable; otherwise report a blocked or partial state.

After revising a brief, apply the normal pre-finalization and output rules again, including the verbatim handoff-prompt comparison.

Every normal implementation brief plan file must include a checklist before the implementation epics:

```md
## Execution Checklist

- [ ] Remaining assumptions reviewed and still applicable.
- [ ] Epic <number> acceptance criteria met.
- [ ] Verification plan completed.
- [ ] ADR need considered after completion.
```

Replace the epic placeholder with exactly one checklist item per planned epic. Do not infer a default count from the template. If the finalized plan has no remaining assumptions, omit the assumption checklist item.

## Required Output

If the request is too broad to plan responsibly in 1 to 5 epics, do not produce the normal implementation brief. Produce a "Request Too Broad" response in chat using this structure:

# Request Too Broad: [Short Task Name]

## Why This Should Be Split

Explain the concrete scope problem: unrelated outcomes, too many layers, missing product decisions, unresolved architecture choices, migration risk, unclear acceptance criteria, or another specific blocker.

## What Can Be Planned Now

List any coherent subset that can be planned safely with the current repo context.

If no subset can be planned safely, state that and explain what information is missing.

## Recommended Split Options

Suggest 2 to 5 viable ways to break the request into focused follow-up prompts.

For each option, include:

- Suggested prompt
- Expected scope
- Why this split is safer
- Whether `$repo-change-planner` or `$coordinate-change-execution` should be used next

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

List only remaining implementation-relevant assumptions that were not converted into requirements or expressed clearly elsewhere in the plan.

If no assumptions remain, state `None.` Do not include an `Open Questions` section in a finalized normal implementation brief. If a question remains, return to "Pre-Finalization Follow-up" instead of writing the plan file.

## Plan File Use

State the plan-file rules from "Plan File Rules" concisely.

## Execution Checklist

Include the checklist described in "Plan File Rules."

## Out of Scope

List nearby work that should not be changed.

Include tempting cleanup, unrelated refactors, unrelated styling updates, and future-version behavior.

## Implementation Epics

Create 1 to 5 epics, following the smallest-coherent-count rules above. For each epic, use:

### Epic [number]: [name]

#### Goal

#### Tasks

#### Acceptance Criteria

Use testable criteria. Prefer:

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
- `$coordinate-change-execution`

Choose `$coordinate-change-execution` when implementation has coordination or continuity risk, such as dependent phases, cross-layer work, unsafe partial states, migrations, refactors, or likely interruption. File count, command count, and report format are not sufficient by themselves.

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

Format the prompt for reliable copy and paste:

- Use plain text inside a fenced `text` code block.
- Do not hard-wrap prose. Keep each paragraph or list item on one logical line and use blank lines only between intentional paragraphs or sections.
- Do not indent the code fence or prefix its contents with list markers, blockquote markers, or other Markdown syntax.

The handoff prompt should include:

- The plan file path
- The requested change
- The selected epic or epics
- The relevant assumptions
- The acceptance criteria
- The verification plan
- Whether to use `$coordinate-change-execution`
- The checklist-maintenance directive below, with the actual plan file path substituted

Do not include planning questions or a question-and-answer history in the handoff prompt. Reflect the resolved answers directly in its requested change, assumptions, scope, acceptance criteria, and verification wording.

Include this directive verbatim in the handoff prompt, replacing the placeholder path:

```text
Treat the `## Execution Checklist` in `docs/plans/<plan-title>.md` as the persistent source of truth for declared progress. At the start of work and after any interruption, reconcile it with the request, current worktree and diff, acceptance evidence, and verification freshness before proceeding. Map conceptual execution phases onto these checklist items rather than creating another status-bearing tracker. Any native or in-chat view may mirror only the same item identities and statuses and must not make independent completion claims. Update the checklist in the plan file as soon as each condition is satisfied and after each epic or verification phase, and sync it before any pause, handoff, or final response. Reopen unsupported items with a concise note, and treat later edits as making affected checks stale. Mark an item complete only after its stated criteria and required verification are met. For partial work, blockers, command-access issues, or test failures, leave the item unchecked and add a brief note beneath it. Do not edit other plan sections during normal execution. If evidence materially invalidates the brief, stop before divergent edits and ask for explicit approval to revise or supersede it under `Material Plan Drift and Approved Revisions`.
```

After writing the plan file, respond in chat with only an abridged version, except for the handoff prompt. Copy the complete contents of the plan's `Suggested Handoff Prompt` code block into the chat response verbatim. Do not summarize, rewrite, reflow, or otherwise abbreviate that prompt. Before responding, compare the two code blocks and confirm their contents are identical, including paragraph breaks and list items.

In the abridged response's `Epics` section, include exactly one summary line per planned epic.

````md
Created plan file: `docs/plans/<plan-title>.md`

## Requested Change

<brief restatement>

## Assumptions

- <assumption, or "None.">

## Epics

- Epic <number>: <title> - <goal>

## Handoff Prompt

```text
<verbatim contents of the plan's Suggested Handoff Prompt code block>
```
````

Do not print any other part of the full plan in chat.
