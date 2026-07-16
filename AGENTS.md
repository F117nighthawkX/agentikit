# AGENTS.md

Project instructions for Codex. These rules apply unless a more specific `AGENTS.md` overrides them.

Bias: careful, verified work over speed on non-trivial tasks. For trivial typo fixes or obvious one-line edits, keep the same intent without extra ceremony.

## Project Commands

Fill these in for each repository:
- Install: `TODO`
- Test: `TODO`
- Lint: `TODO`
- Typecheck: `TODO`
- Build: `TODO`
- Format: `TODO`

If a command is missing, search the repo for scripts, task files, CI config, package manifests, Makefiles, or docs before asking.

## 1. Scope and Plan

Do not assume. Do not hide confusion. Surface tradeoffs and recommend clearly.

Before non-trivial coding, inspect enough context to state:
- Intended outcome, assumptions, constraints, success criteria, and expected impact.
- Files, modules, behavior, and nearby areas expected to remain untouched.
- A 2 to 5 step plan with verification for each step.
- Any unrequested abstraction, framework adoption or replacement, compatibility layer, or speculative feature you are rejecting.

Ask before editing when:
- The request has multiple plausible meanings.
- The change touches sensitive data, security, auth, billing, persistence, migrations, public APIs, or external contracts.
- The expected behavior is not defined by nearby code, tests, docs, or the user's request.
- The request conflicts with existing code, prior requirements, or itself.
- A decision could cause data loss or broad refactoring.

Proceed without asking when the task is narrow, reversible, and the expected outcome is clear from context.

When multiple interpretations or approaches exist:
- Present the meaningful options with rough costs and tradeoffs.
- Mark your recommended option.
- Explain why it fits the current codebase, constraints, and goal.
- Defer to the user if they choose a different option.

## 2. Read Before Writing

Before adding or changing code, understand the local context. Read the target file, immediate callers and callees, exports, public interfaces, schemas, type definitions, shared utilities, nearby tests, and existing patterns as needed.

Before changing existing behavior, identify what nearby behavior must remain intact. Treat unchanged behavior as part of the task even when it is not named in acceptance criteria; preserve it unless the user asked to change it or you surface and confirm the tradeoff.

For UI work, inspect the surrounding flow and visual system before implementing. Layout, spacing, alignment, animation, placement, affordances, and state behavior should feel like a natural extension of the project. Ask whether someone using the project could tell the new work was added later; if yes, adjust within scope or report the mismatch.

Check for an existing pattern before adding a new one. Treat existing patterns as evidence and a consistency default, not a veto: use a better framework-native or ecosystem-standard approach when it materially improves correctness, maintainability, or project fit, and explain meaningful tradeoffs.

If code seems oddly structured, assume there may be a reason. Ask or investigate before replacing it.

## 3. Implement Surgically

Use the smallest correct implementation: minimize unnecessary total complexity across locally owned code and dependency, transitive, build, runtime, and operational costs. Do not optimize for the fewest imports, dependencies, API calls, lines, or the smallest diff. Touch only what the task requires. Clean up only your own mess.

Do not add:
- Features beyond what was requested.
- Abstractions for single-use code.
- Configurability that was not requested.
- Error handling for impossible states.
- Compatibility layers without a current need.

When choosing implementation tools:
- Use language, platform, or standard-library capabilities for straightforward logic they handle cleanly.
- Use supported APIs from declared project dependencies normally. A new import from one is not a new dependency.
- Prefer a focused, established, project-fitting dependency over bespoke code when meaningful correctness, reliability, security, standards, interoperability, clarity, or maintenance benefits and avoided ownership outweigh its footprint, even for a single call site or short helper.
- Avoid redundant dependencies when a declared dependency offers a comparably clear, reliable, and maintainable solution. Avoid purpose-mismatched or disproportionate dependencies, but do not recreate established ecosystem functionality merely to keep the dependency list smaller.
- Treat an ordinary, proportionate library addition as normal implementation. Ask before adopting or replacing a major framework or adding a dependency that materially changes architecture, the toolchain, runtime, deployment, security boundaries, or public contracts; separate environment, network, and tool-execution permissions still apply.

Do preserve:
- Established patterns that improve long-term maintainability or testability.
- Security boundaries and necessary validation.
- Clear naming and direct control flow.
- Existing public contracts unless the task explicitly changes them.

When editing existing code:
- Do not improve adjacent code, comments, formatting, or names unless required.
- Do not refactor unrelated code.
- Match existing style even if you disagree with it.
- If an existing convention is harmful, mention it and ask before changing direction.
- If you notice unrelated dead code or bugs, report them instead of fixing them silently.

Comment handling:
- Preserve existing comments by default, including inline comments, block comments, doc comments, and TODOs.
- If you change code that a nearby comment describes, update only the parts of the comment needed to keep it accurate.
- Do not remove a comment merely because it feels obvious, verbose, stylistically different, or not how you would write it.
- Remove a pre-existing comment only when it is blatantly wrong, outdated, misleading, or attached to code that the requested change removes.
- If you remove or materially rewrite a non-trivial existing comment, mention why in the final report.

When your change creates orphans:
- Remove imports, variables, functions, files, or tests made unused by your change.
- Do not remove pre-existing dead code unless asked.

Every changed line should trace back to the user's request or to verification required by that request.

## 4. Simplify Before Handoff

After code changes, perform a simplification pass:
- Remove abstraction, wrappers, dead code, or flexibility introduced by your change that is not needed.
- Check for duplication introduced by your change.
- Confirm the code still follows repo conventions and these instructions.
- Preserve comments according to Section 3.
- Mention what was simplified, or state that no meaningful simplification was needed.

Ask: would a senior engineer say this is overcomplicated? If yes, simplify.

## 5. Verify

Define success criteria and loop until verified.

Turn vague tasks into testable goals:
- "Add validation" means test invalid inputs, then make them pass.
- "Fix the bug" means reproduce it with a test or focused check, then make it pass.
- "Refactor" means preserve behavior and run relevant tests before and after when practical.

Prefer the narrowest verification that proves the change: focused tests, typecheck, lint, formatter, build, or manual check when automated coverage is unavailable.

Tests should verify intent, not only implementation details. A test that still passes when the business rule is broken is weak.

Never claim verification you did not run. Final reports must state:
- What changed.
- What was simplified.
- What verification ran and passed.
- What was not verified.
- Any remaining risk.

If verification fails, report the failure clearly and explain the likely cause if known.

## 6. Communicate Uncertainty

Say what is known, what is inferred, and what is unknown.

When confidence is low:
- Use clear uncertainty language near the claim, not only at the end.
- Name the missing visibility or assumption.
- Flag claims that need external verification before the user acts on them.
- Do not use confident tone to cover incomplete knowledge.

For multi-step tasks:
- Checkpoint after meaningful phases.
- Summarize what is done, what is verified, and what remains.
- If you lose track, stop and restate the current state before continuing.

Fail loud:
- "Done" is wrong if required work was skipped silently.
- "Tests pass" is wrong if tests were skipped, filtered unexpectedly, or not run.
- Report blocked work, partial completion, and skipped steps.

## 7. Documentation and Decisions

Code shows what changed. Docs should explain durable decisions.

Update docs when a decision was made between real alternatives, a non-obvious constraint was discovered, or project structure, commands, conventions, or setup changed.

Do not document obvious implementation details, duplicate git history, or add docs just in case.

Use `docs/adr/` only for durable architectural decisions. See `docs/agent/adr-template.md`.

Keep broadly applicable agent rules in `AGENTS.md`, repeatable workflows in `.agents/skills/`, and longer task-specific guidance in `docs/agent/`.

Agent-operational guidance must not exist only in a README. A README can still provide useful project context and human-facing setup or usage information.

Files under `docs/adr/` and `docs/plans/` are repository-specific records. Reuse the directory conventions across projects, not the records they contain.

If a tool does not discover `.agents/skills/`, add a small tool-specific pointer to the canonical skill files instead of maintaining duplicate copies unless the tool requires them.

## Optional Reading and Skills

Read optional docs only when the task calls for them:
- `docs/agent/architecture-boundaries.md`: before changing module boundaries, public APIs, database schemas, service layers, dependencies, logging, auth, or cross-cutting infrastructure.
- `docs/agent/adr-template.md`: when a durable technical decision should be recorded.
- `docs/agent/llm-runtime-guidance.md`: when implementing code that calls LLMs, agents, classifiers, extractors, routers, retry loops, or deterministic transforms.

Use available skills when the task matches them:
- `$commit-report`: use for explicit current diff summaries, suggested commit messages, or commit-style completion reports.
- `$repo-change-planner`: use before implementation when a focused follow-up request should become a scoped plan under `docs/plans/`, or when the request should be split before planning. This skill plans only.
- `$long-task-workflow`: use for executing substantial repository changes with coordination or continuity risk, such as dependent phases, cross-layer work, unsafe partial states, migrations, refactors, or likely interruption.
