# Implementation Brief: Simplify Agent Guidance

## Requested Change

Inspect `AGENTS.md`, the accompanying repository documentation, and the optional docs and skills named in `AGENTS.md` section `Optional Reading and Skills`. Plan a simplification/refactor that reduces repeated wording and context load without losing the intent of the current guidance. The implementation should combine overlapping concepts where useful, simplify wording and ordering, and consider whether repeated concepts deserve extraction into optional docs or skills.

## Existing Context Found

- `AGENTS.md` is the always-loaded root instruction file. It currently covers clarification, reading before writing, simplicity, surgical edits, verification, communication, documentation decisions, and optional reading/skill triggers.
- `README.md` describes Agentikit as a compact `AGENTS.md` plus optional docs and reusable skills, and documents copy paths, generated plan behavior, skill descriptions, and maintainer checks.
- `docs/agent/architecture-boundaries.md` contains architecture, public contract, dependency, data, auth/security, error/logging, endpoint, UI boundary, and ADR-trigger guidance.
- `docs/agent/adr-template.md` contains durable ADR trigger guidance, file naming, template, update rules, and an example that repeats the root/optional-doc split rationale.
- `docs/agent/llm-runtime-guidance.md` contains LLM boundary guidance and is relatively self-contained.
- `.agents/skills/commit-report/SKILL.md` contains current-diff inspection, commit-message rules, report structure, and safety rules about not staging or committing.
- `.agents/skills/long-task-workflow/SKILL.md` contains multi-phase task triggers, starting checklist, progress updates, handoff notes, final report structure, simplification-pass reporting, and commit-report delegation.
- `.agents/skills/repo-change-planner/SKILL.md` contains planning-only scope, broad-request handling, plan-file rules, required plan template, checklist rules, and handoff prompt rules.
- `scripts/verify_package.py` verifies required package paths, README copy guidance, `AGENTS.md` project-command placeholders, and skill frontmatter.
- `docs/plans/` exists and currently contains only `.gitkeep`; no existing plan file was overwritten.
- `PLAN.md` was referenced in the IDE context but does not exist in this workspace.

## Assumptions

- The implementation should preserve Agentikit's current product shape: a compact root `AGENTS.md`, optional docs under `docs/agent/`, reusable skills under `.agents/skills/`, ADRs under `docs/adr/`, and generated implementation plans under `docs/plans/`.
- The main optimization target is reducing duplicated instruction text and loaded context, not changing the behavioral standard for coding agents.
- Any new optional doc should be added only if it replaces enough repeated text across `AGENTS.md` and skills to reduce total maintained wording and keep routing clear. This should be confirmed before coding if the implementer finds the extraction is marginal.
- Skill metadata names should remain stable unless the user explicitly requests a breaking rename.
- Because this repository is a copyable kit, any new copied path or required file should be reflected in `README.md` and `scripts/verify_package.py`.

## Open Questions

- Non-blocking: Should the implementation optimize for the shortest possible `AGENTS.md`, or for the fewest total files? Recommended default: keep `AGENTS.md` compact but do not create a new optional doc unless it clearly removes repeated guidance from at least two other places.
- Non-blocking: Should README origin/attribution prose be simplified as part of this pass? Recommended default: leave origin/attribution mostly alone unless a wording change is needed to keep the new structure accurate.

## Plan File Use

This plan is a working artifact for coordinating implementation, not a durable source of truth.

Plan details must not be updated after the file is written. Only checklist state and brief notes under checklist items may be updated.

Users and agents should follow `AGENTS.md` section `7. Documentation and Decisions` for durable documentation, and create an ADR only when applicable after the relevant epic or plan has been completed.

## Execution Checklist

- [x] User confirmed assumptions are valid.
- [x] Open questions are resolved or explicitly accepted as non-blocking.
- [x] Epic 1 acceptance criteria met.
- [x] Epic 2 acceptance criteria met.
- [x] Epic 3 acceptance criteria met.
- [x] Epic 4 acceptance criteria met.
- [x] Verification plan completed.
- [x] ADR need considered after completion, following `AGENTS.md` section `7. Documentation and Decisions`.

## Out of Scope

- Do not change the repository into a different documentation system or introduce a new framework for skills.
- Do not change the core safety posture: careful context gathering, reversible scope, surgical edits, explicit verification, and honest uncertainty should remain intact.
- Do not rewrite attribution, license, or project positioning beyond what is needed to keep structure descriptions accurate.
- Do not add generated plan files to the copyable kit contract; generated plans should remain working artifacts.
- Do not implement new coding-agent behaviors that are not already implied by the existing docs.
- Do not add package-manager tooling or unrelated checks.

## Implementation Epics

### Epic 1: Map Guidance Ownership

#### Goal

Create an explicit ownership map before editing so repeated concepts are either kept once in the right place or intentionally repeated only as short routing reminders.

#### Tasks

- Compare `AGENTS.md`, `README.md`, optional docs, and skill files for repeated concepts around clarification, reading context, scope control, simplification, verification, final reporting, ADR triggers, plan-file rules, and skill routing.
- Decide which file should own each concept:
  - Root `AGENTS.md` should own always-loaded coding-agent behavior and routing triggers.
  - Optional docs should own deeper reference guidance for architecture, ADRs, LLM runtime behavior, or any newly justified shared reference.
  - Skills should own task-specific workflow, output formats, and trigger-specific constraints.
  - README should own package usage and maintainer-facing copy guidance.
- Identify wording that can become a shorter pointer instead of a repeated rule.
- Identify any repeated concept that is not worth extracting because it must stay self-contained in a skill.

#### Acceptance Criteria

- Given the existing docs and skills, when a repeated concept appears in multiple files, then the implementation notes a single intended owner before editing.
- Given ADR guidance appears in `AGENTS.md`, `architecture-boundaries.md`, `adr-template.md`, and skill files, when refactoring begins, then the implementer has chosen whether `adr-template.md` or `architecture-boundaries.md` owns the detailed trigger wording.
- Given reporting and verification rules appear in `AGENTS.md`, `long-task-workflow`, and `commit-report`, when refactoring begins, then the implementer has separated general verification obligations from task-specific report formats.
- Existing copyable-kit structure remains intact.

#### Likely Files or Areas

- `AGENTS.md`
- `README.md`
- `docs/agent/architecture-boundaries.md`
- `docs/agent/adr-template.md`
- `docs/agent/llm-runtime-guidance.md`
- `.agents/skills/commit-report/SKILL.md`
- `.agents/skills/long-task-workflow/SKILL.md`
- `.agents/skills/repo-change-planner/SKILL.md`

#### Risks

- Over-extracting core rules from `AGENTS.md` could make agents miss behavior that should always be loaded.
- Keeping skills too self-contained can preserve too much duplication.
- Removing repeated safety wording may reduce fidelity if the remaining pointer is too vague.

#### Recommended Execution Skill

`$long-task-workflow`

### Epic 2: Reorder and Condense Root Guidance

#### Goal

Make `AGENTS.md` shorter and more effective by ordering it around the actual work loop and turning detailed repeated guidance into precise pointers where safe.

#### Tasks

- Reorder root guidance into an execution sequence that is easier to follow: commands and discovery, clarify/scope, read context, plan when needed, implement surgically, simplify, verify, report uncertainty, document durable decisions, and route to optional docs/skills.
- Combine overlapping wording between sections `Clarify, Plan, Recommend`, `Read Before Writing`, `Simplicity and Maintainability`, `Surgical Changes`, `Verification Contract`, and `Communication and Uncertainty` where the same instruction is stated more than once.
- Preserve explicit ask-before-editing rules for ambiguity, security/auth/billing/persistence/public contracts, data loss, broad refactors, and undefined expected behavior.
- Preserve comment-handling rules unless a shorter equivalent keeps all existing intent.
- Keep optional doc and skill triggers specific enough that agents know when to load each file.
- Correct small wording issues found during the pass, such as `simplfied` in user-facing copied text only if that typo exists in repository docs.

#### Acceptance Criteria

- Given a non-trivial coding task, when an agent reads `AGENTS.md`, then the expected sequence is clear: inspect context before editing, plan when needed, make surgical changes, simplify, verify, and report truthfully.
- Given a sensitive or ambiguous task, when an agent reads `AGENTS.md`, then it still knows when to ask before editing.
- Given optional docs and skills, when an agent reads `AGENTS.md`, then routing triggers remain discoverable and no skill trigger becomes broader than its `SKILL.md` description.
- The implementation must not remove the `Project Commands` TODO template required by `scripts/verify_package.py`.
- The implementation must not remove comment-preservation or verification-reporting intent.

#### Likely Files or Areas

- `AGENTS.md`
- Possibly `README.md` if structural descriptions need adjustment.

#### Risks

- A shorter root file may become too abstract unless examples or concrete triggers are retained.
- Reordering can accidentally imply that planning should happen before reading local context; the new order should make "read before writing" explicit.

#### Recommended Execution Skill

`$long-task-workflow`

### Epic 3: Deduplicate Skill Workflows

#### Goal

Reduce repeated workflow text in the three skills while keeping each skill usable when loaded on its own.

#### Tasks

- In `.agents/skills/long-task-workflow/SKILL.md`, keep the multi-phase checklist, progress checkpointing, handoff, and final report formats, but shorten restatements already owned by `AGENTS.md`.
- In `.agents/skills/repo-change-planner/SKILL.md`, remove duplicated plan-file immutability and ADR-routing wording where it appears both in planning rules and required template instructions, while preserving the required output structure.
- In `.agents/skills/commit-report/SKILL.md`, keep commit-message and report-format rules as authoritative, but avoid restating general scope, verification, and prohibited-action guidance already covered by `AGENTS.md` except where the safety rule is task-critical.
- Preserve the clear relationship between the three skills:
  - `repo-change-planner` plans only.
  - `long-task-workflow` executes large or risky work.
  - `commit-report` summarizes current diffs and commit-style reports only.
- Consider whether a small shared optional doc for "execution/reporting contract" is justified. Add it only if it replaces meaningful duplicated text from at least `AGENTS.md` and `long-task-workflow` without making simple task routing harder.

#### Acceptance Criteria

- Given a request for a plan, when `repo-change-planner` is loaded, then it still instructs the agent to write a plan file under `docs/plans/`, include 1 to 5 epics or a "Request Too Broad" response, and avoid implementing.
- Given a large implementation request, when `long-task-workflow` is loaded, then it still instructs the agent to create an in-chat checklist, checkpoint progress, provide handoff notes if incomplete, and provide a structured final report.
- Given a commit-style report request, when `commit-report` is loaded, then it still forbids staging, unstaging, committing, amending, resetting, or pushing unless explicitly asked.
- The skills remain self-contained enough that loading a skill plus `AGENTS.md` is sufficient to execute the workflow.
- Any new optional doc is referenced from `AGENTS.md`, `README.md`, and `scripts/verify_package.py` if it becomes part of the copyable kit.

#### Likely Files or Areas

- `.agents/skills/long-task-workflow/SKILL.md`
- `.agents/skills/repo-change-planner/SKILL.md`
- `.agents/skills/commit-report/SKILL.md`
- Possibly `docs/agent/<new-shared-reference>.md`
- Possibly `README.md`
- Possibly `scripts/verify_package.py`

#### Risks

- Shortening `repo-change-planner` too much could make generated plan files inconsistent.
- Moving report guidance out of skills could make final reports less predictable.
- Adding a new optional doc can increase routing complexity if it is not clearly justified.

#### Recommended Execution Skill

`$long-task-workflow`

### Epic 4: Align Optional Docs, README, and Package Checks

#### Goal

Make the surrounding docs and verification script match the simplified structure after root and skill changes.

#### Tasks

- In `docs/agent/architecture-boundaries.md`, keep detailed architecture and public-contract guidance, but replace duplicated ADR trigger wording with a short pointer if `adr-template.md` owns detailed ADR criteria.
- In `docs/agent/adr-template.md`, keep durable ADR trigger, naming, template, update rules, and example. If root guidance is simplified, ensure the example still matches the intended root/optional-doc split.
- In `docs/agent/llm-runtime-guidance.md`, leave content mostly intact unless wording can be tightened without reducing the deterministic-code-vs-LLM-judgment rule.
- Update `README.md` only where the file list, skill descriptions, optional docs, or maintainer checks change.
- If a new optional doc is added, update `scripts/verify_package.py` `REQUIRED_FILES` and README copy/optional-doc references as needed.
- Run a simplification pass on the changed docs: remove only new duplication introduced by the refactor, preserve meaningful existing comments and examples, and avoid broad stylistic rewrites.

#### Acceptance Criteria

- Given the final file set, when `README.md` describes package contents and copy paths, then those descriptions match the repository.
- Given the final optional doc list, when `AGENTS.md` routes agents to optional docs, then each referenced path exists.
- Given the final skill list, when `scripts/verify_package.py` checks skill metadata, then all skill names and descriptions remain valid.
- The implementation must not introduce stale references to removed or renamed files.
- Existing generated-plan guidance remains clear that `docs/plans/*.md` are working artifacts, not durable documentation.

#### Likely Files or Areas

- `docs/agent/architecture-boundaries.md`
- `docs/agent/adr-template.md`
- `docs/agent/llm-runtime-guidance.md`
- `README.md`
- `scripts/verify_package.py`

#### Risks

- Updating the package check incorrectly could make future structural changes look valid when required files are missing.
- Simplifying README too aggressively could remove important copy instructions for hidden `.agents/` paths or generated plan ignores.

#### Recommended Execution Skill

`$long-task-workflow`

## Verification Plan

- Run `python scripts/verify_package.py` after changes and require it to pass.
- Run `git diff --check` after changes and require it to pass.
- Manually review every path referenced from `AGENTS.md`, `README.md`, and skill files to ensure the referenced files exist.
- Manually compare old and new trigger coverage for:
  - Ask-before-editing cases.
  - Read-before-writing expectations.
  - Simplification pass and comment-preservation expectations.
  - Verification and final-report expectations.
  - ADR creation/update triggers.
  - Skill routing for `$commit-report`, `$repo-change-planner`, and `$long-task-workflow`.
- If a new optional doc is added, verify it is included in `README.md` and `scripts/verify_package.py`.
- Do not claim behavioral verification beyond docs/package checks; this is a documentation and instruction refactor.

## Suggested Handoff Prompt

```text
Use `$long-task-workflow` to implement `docs/plans/simplify-agent-guidance.md`.

Requested change: simplify and refactor Agentikit's root instructions, optional docs, and local skills to reduce overlap and context usage without losing fidelity or intent.

Implement all epics in the plan. Preserve the current copyable-kit structure and the core safety posture: read before writing, ask on ambiguity/sensitive changes, make surgical edits, simplify, verify, report uncertainty, and use ADRs only for durable decisions. Treat the open questions as non-blocking unless the extraction of a new optional doc is marginal; in that case, prefer no new file.

Acceptance criteria: root guidance follows a clearer work-loop order; repeated skill workflow text is shortened without losing task-specific output formats; optional docs and README match the final structure; any new optional doc is reflected in `README.md` and `scripts/verify_package.py`; generated plan guidance remains a working-artifact convention.

Verification: run `python scripts/verify_package.py`, run `git diff --check`, and manually review all references and trigger coverage listed in the plan. Report what changed, what was simplified, verification results, unverified areas, remaining risk, and whether an ADR is needed.
```
