# Implementation Brief: Refine Long-Task Workflow

## Requested Change

Refine Agentikit's long-task execution workflow so it uses one authoritative progress tracker, composes cleanly with `AGENTS.md` and planner-generated briefs, survives interruptions safely, distinguishes ordinary execution variance from material plan drift, verifies the final worktree in the correct order, and hands off partial work without ambiguity. Align the skill trigger and planner contract across the copyable guidance, remove the default commit-message overlap with `$commit-report`, add concise tool-neutral coordination guidance for parallel work, and strengthen the package verifier with stable contract checks.

The expected impact is a more reliable long-task workflow without adding a new state-file convention, dependency, framework, or tool-specific orchestration API.

## Existing Context Found

- `AGENTS.md` is always loaded and already owns general planning, confirmation, surgical implementation, simplification, verification, uncertainty, final-report minimums, and skill routing.
- `.agents/skills/long-task-workflow/SKILL.md` currently owns phased execution, checkpoints, handoffs, and a compact final format, but it creates a plan and a duplicate checklist, incompletely restates root planning and confirmation rules, and advertises multi-session work without a resume/reconciliation protocol.
- The current long-task example performs implementation before test updates and places verification before regression review and simplification, so later edits can make earlier checks stale.
- The current context-record ranking treats code, reports, commit messages, ADRs, and checklists as interchangeable alternatives even though they serve different purposes.
- The current final-report contract both delegates suggested commit messages to `$commit-report` only on request and includes a default `Suggested commit message` section.
- `.agents/skills/repo-change-planner/SKILL.md` makes a generated plan's `## Execution Checklist` the persistent source of truth and normally freezes plan details, but it does not define a controlled response when implementation evidence materially invalidates those details.
- `.agents/skills/commit-report/SKILL.md` already owns explicit diff summaries, commit-message rules, and commit-style reports. Its workflow does not need to change for this request.
- `AGENTS.md`, `.agents/skills/long-task-workflow/SKILL.md`, `.agents/skills/repo-change-planner/SKILL.md`, and `README.md` currently repeat broad file-count, phase-count, command-count, and report-format triggers that can route ordinary or report-only work into the long-task workflow.
- `scripts/verify_package.py` checks required paths, skill metadata, and selected stable guidance phrases, but it does not guard the long-task tracker, resume, drift, trigger-alignment, or commit-report ownership contracts.
- `README.md` is a human-facing source-repository overview. Operational details must remain in the copyable `AGENTS.md` and skill files, with README containing only an aligned skill summary.
- Existing files under `docs/plans/` are completed repository-specific working artifacts and should not be rewritten to match the refined future workflow.
- The available repository checks are `python scripts/verify_package.py` and `git diff --check`; this source repository intentionally has no package-manager test, lint, typecheck, build, or format command.
- `git status --short` was clean before this plan file was created.

## Assumptions

None.

## Plan File Use

This plan is a working artifact, not durable project documentation. During normal execution, update only checklist state and brief notes beneath the relevant checklist item; do not rewrite requested change, context, scope, epics, acceptance criteria, files, risks, verification, or handoff wording.

Mark an epic complete only after all of its acceptance criteria are met. If implementation evidence materially invalidates this brief, stop before divergent edits, leave affected items incomplete with a concise evidence note, and ask the user whether to authorize a focused revision or a superseding plan.

## Execution Checklist

- [x] Epic 1 acceptance criteria met.
- [x] Epic 2 acceptance criteria met.
- [x] Verification plan completed.
- [x] ADR need considered after completion.

## Out of Scope

- Do not rewrite the general planning, confirmation, implementation, simplification, verification, or documentation policies already owned by `AGENTS.md`.
- Do not change `.agents/skills/commit-report/SKILL.md`, its Conventional Commit rules, or its report format.
- Do not introduce a default repository state file, `context-notes.md`, tracker dependency, plugin, framework, or tool-specific plan API.
- Do not make persistent plan files mandatory for long tasks that were not supplied with one and whose user did not request one.
- Do not add Codex-specific multi-agent commands; keep any parallel-work guidance conditional and tool-neutral.
- Do not retroactively edit completed files under `docs/plans/` or the existing repository ADR.
- Do not redesign unrelated `repo-change-planner` behavior, broaden its 1-to-5-epic planning scope, or turn it into an implementation skill.
- Do not build a semantic Markdown linter, snapshot entire prose sections, add a test framework, or make the verifier enforce subjective workflow judgment.
- Do not create a new ADR unless implementation reveals a durable architectural decision beyond the existing Agentikit guidance-ownership contract.

## Implementation Epics

### Epic 1: Make Long-Task Execution State Reliable

#### Goal

Make `.agents/skills/long-task-workflow/SKILL.md` the concise owner of long-task execution state, phase checkpoints, interruption recovery, plan-drift handling, fresh verification, partial handoffs, and implementation final reports while relying on applicable `AGENTS.md` files for general policy.

#### Tasks

- Tighten the skill frontmatter and `When to Use This` section around execution that has meaningful coordination or continuity risk, such as dependent phases, cross-layer changes, unsafe partial states, migrations or refactors, or likely interruption. State that file count, command count, planning-only work, report-only work, and simple mechanical changes are not sufficient triggers by themselves.
- Change `Read first` to cover every applicable `AGENTS.md` file for the areas being touched.
- Replace the skill's incomplete plan schema and separate checklist with one tracked execution plan derived from the 2-to-5-step plan required by `AGENTS.md`. Add only long-task-specific phase dependencies, exit criteria, risks, safe pause points, and verification mapping.
- Define one authoritative progress tracker per task:
  - When a supplied `docs/plans/*` brief contains `## Execution Checklist`, update it first as the persistent source of progress truth; any chat summary may mirror it but must not compete with it.
  - Otherwise maintain exactly one native or in-chat tracker and do not create a repository tracker unless the user asks.
  - Clarify that the tracker records declared progress while the worktree, diff, and verification output remain the supporting evidence.
- Add a concise resume/reconciliation gate for work continuing after interruption. Require rereading applicable instructions, the request, active brief, checklist, and notes; inspecting status, diff, and available check evidence; separating pre-existing and task-owned changes where possible; marking affected checks stale after later edits; correcting unsupported checklist state with a brief note; and selecting the first safe incomplete step before editing.
- Record the relevant initial working-tree and verification baseline for long tasks so later handoffs and final reports do not silently claim unrelated changes or pre-existing failures.
- Require phase exit criteria and tracker synchronization after meaningful phases and before planned pauses, handoffs, or final responses. A completed item must have its intended outcome and required verification satisfied; implemented-but-unverified work remains incomplete.
- Require phases to leave the repository in a coherent state where practical. When temporary breakage is unavoidable, keep the affected item incomplete and record the exact state and next safe action.
- Replace the local narrow confirmation list with the applicable `AGENTS.md` confirmation boundaries. Distinguish non-material execution variance from material plan drift:
  - Sequencing changes, implementation details, newly discovered likely files, or equivalent verification substitutions may continue with a tracker note only when requested outcome, scope, acceptance criteria, public behavior and contracts, risk, and verification strength remain intact.
  - Drift is material when the plan cannot be followed accurately, assumptions, scope, acceptance criteria, or out-of-scope boundaries must change, verification would weaken, or `AGENTS.md` requires confirmation.
  - For material drift, stop before divergent edits, leave affected state incomplete, explain evidence, affected sections, options, tradeoffs, and a recommendation, then require explicit approval to revise or supersede the plan.
- Replace the example's verification order with: inspect and capture a baseline or reproduction when applicable; implement each phase with focused checks; review regression and product or UI fit; simplify and perform the comment-preservation review; then rerun affected focused checks and final relevant broader checks against the final worktree. Mark earlier checks stale when later edits can invalidate them.
- Replace the ordered `durable records` list with purpose-based ownership: code and tests capture behavior and evidence; the execution tracker captures temporary progress; handoff and final reports communicate execution state; documentation and ADRs capture qualifying durable rationale under `AGENTS.md`; `$commit-report` owns explicitly requested diff and commit-message reporting.
- Expand the handoff trigger and compact template to cover a pause, blocker, user transfer, session boundary, or still-running long command. Include the authoritative tracker or plan path, completed and active or remaining items, reason for stopping, task-owned versus pre-existing changes when known, exact check states including passed, failed, running, stale, and not run, known issues, and the next safe action.
- Make final completion conditional on all required checklist outcomes and verification being satisfied; otherwise use the partial handoff contract. Separate `Checks run` from `Not verified`, retain regression and fit review plus simplification results, and report remaining risk honestly.
- Remove the default suggested commit-message bullet and template section. Say that an explicitly requested commit message, diff summary, or commit-style report is a separate final read-only phase owned by `$commit-report`.
- Add a short conditional parallel-work rule: partition only independent work, assign non-overlapping ownership and interface expectations, keep one coordinator as the tracker writer, reconcile the combined worktree and evidence rather than trusting delegated completion claims, and run integrated verification before final completion.
- Perform a simplification pass on the revised skill so the new state mechanics do not restate root policy or turn routine checkpoints into ceremony.

#### Acceptance Criteria

- Given a planner-generated implementation brief, when `$long-task-workflow` starts, then the plan's `## Execution Checklist` is the sole authoritative progress tracker, an in-chat view is only a mirror, and no competing checklist is created.
- Given no persistent brief, when the workflow starts, then exactly one native or in-chat tracker is maintained and no repository state file is created by default.
- Given an initial or resumed long task, when work begins, then the tracker is reconciled against applicable instructions, the request, repository state, ownership evidence, acceptance evidence, and verification freshness before edits continue.
- Given a checked item that is no longer supported by the worktree or fresh verification, when reconciliation occurs, then it is reopened with a concise note rather than trusted or reported complete.
- Given a non-material execution variance, when outcome, scope, contracts, risk, criteria, and verification strength remain intact, then the agent may note the variance and continue without editing frozen plan details.
- Given material drift, when the current plan is no longer accurate, then no divergent code or plan-detail edit occurs before the user receives the evidence, options, tradeoffs, and recommendation and explicitly approves revision or supersession.
- Given later implementation or simplification edits, when they can invalidate earlier checks, then those checks are treated as stale and rerun before final completion.
- Given partially implemented, blocked, running, stale, failed, or unverified work, when execution pauses, then the handoff distinguishes those states and identifies the next safe action without placing them under completed work.
- Given final completion, when the report is produced, then it describes the final worktree, separates checks actually run from work not verified, includes regression or product-fit and simplification results, and contains no default suggested commit message.
- Given parallel delegation is used, when delegated work returns, then a single coordinator reconciles non-overlapping ownership, combined changes, and integrated verification before marking progress complete.
- Existing restraint against ad hoc context-note files, surgical scope, phase checkpointing, UI or product-fit review, comment preservation, and compact reporting remain intact.

#### Likely Files or Areas

- `.agents/skills/long-task-workflow/SKILL.md`

#### Risks

- Resume and handoff requirements can become busywork if they are not scaled to the size of the interruption and current diff.
- Calling a checklist the source of truth can imply that it outranks repository evidence; wording must scope it to declared progress and require reconciliation.
- An overly broad definition of material drift can cause unnecessary user pauses, while a narrow definition can permit silent scope or acceptance changes.
- Parallel-work guidance can become tool-specific or disproportionately long unless kept conditional and outcome-focused.
- This is a self-hosted workflow change, so the implementation agent must obey the existing plan directive while editing the skill that will define future behavior.

#### Recommended Execution Skill

`$long-task-workflow`

### Epic 2: Align and Guard the Workflow Contract

#### Goal

Make Agentikit's routing, planner handoff semantics, human-facing summary, and package checks agree with the refined long-task workflow without duplicating its operational detail or changing unrelated skill behavior.

#### Tasks

- Choose one concise canonical activation concept centered on `coordination or continuity risk` and align it across:
  - The `$long-task-workflow` route in `AGENTS.md`.
  - The planner's relationship and recommended-execution-skill guidance.
  - The human-facing skill summary in `README.md`.
  - The long-task frontmatter and body completed in Epic 1.
- Keep routing phase-based: `$repo-change-planner` creates or revises a user-requested persistent implementation brief, `$long-task-workflow` executes substantial work that needs coordination or continuity state, and `$commit-report` performs explicitly requested read-only diff or commit-style reporting.
- Update `.agents/skills/repo-change-planner/SKILL.md` so future plans and handoff prompts use the same authoritative-checklist, resume, stale-check, synchronization, and material-drift vocabulary as the long-task workflow.
- Replace absolute plan immutability with a normal-execution freeze plus a controlled revision exception:
  - Normal implementation may update only checklist state and brief notes.
  - Material drift stops execution before divergent edits and requires explicit user approval.
  - After approval, revise the existing brief in place only when it remains the same focused 1-to-5-epic request; update every affected plan section and handoff atomically, add a compact approved-revision note, preserve unaffected evidence, and reset affected epic and verification state.
  - If the approved work becomes broader, different, or no longer fits the planner, create a superseding brief or split the request, designate the new authority, and leave the old brief read-only apart from a concise superseded checklist note.
  - If approval is denied, continue against the original plan only when it remains viable; otherwise report a blocked or partial state.
- Update the planner's required handoff directive and plan-file-use instructions so they remain internally consistent with the controlled revision exception and still prevent ordinary implementers from silently rewriting plan details.
- Keep `.agents/skills/commit-report/SKILL.md` unchanged and manually confirm the revised long-task and routing text preserve its explicit ownership.
- Extend `scripts/verify_package.py` with a small set of stable workflow-contract checks:
  - Require the canonical activation anchor in each routing surface that must stay aligned, with path-specific failure messages.
  - Require short authoritative-tracker, interruption-resume, material-drift, and explicit commit-report delegation anchors in the owning skills.
  - Require a distinct `Not verified` reporting anchor if retained as a stable final-template contract.
  - Forbid the exact stale long-task instructions that mandate a second in-chat checklist, rank unrelated records, invite a commit message by default, or restore a full-line `Suggested commit message:` template heading.
  - Anchor forbidden template checks to full lines where needed so explanatory prose can still mention intentionally absent sections.
- Keep verifier assertions structural and phrase-focused. Do not snapshot full sections, require paragraph order, parse subjective semantics, or claim to prove runtime workflow behavior.
- Perform a cross-file simplification and ownership audit so `AGENTS.md` and README contain only routing summaries, the planner owns persistent-plan lifecycle, the long-task skill owns execution lifecycle, and commit-report ownership remains unambiguous.

#### Acceptance Criteria

- Given a planning-only, report-only, or simple mechanical request, when Agentikit routing is read, then file count, command count, or desired report format alone does not select `$long-task-workflow`.
- Given substantial execution with dependent phases, cross-layer coordination, unsafe partial state, migration or refactor risk, or likely interruption, when Agentikit routing is read, then the long-task workflow is discoverable through the same canonical activation concept in `AGENTS.md`, the planner, the skill, and README.
- `AGENTS.md` remains the owner of universal planning, confirmation, implementation, simplification, verification, and report-minimum rules; the long-task skill adds only execution-lifecycle mechanics.
- Planner-generated handoffs and the long-task workflow agree on tracker precedence, interruption reconciliation, stale verification, synchronization before pauses and final responses, and material plan drift.
- During normal execution, plan details remain frozen; an in-place revision cannot occur without explicit approval and must update all affected sections, reset affected state, and retain a single authoritative brief.
- Broader or different approved work is split or moved to a clearly designated superseding brief rather than silently expanding the original plan.
- Explicit commit-message and commit-style report ownership remains in `.agents/skills/commit-report/SKILL.md`, which is unchanged by this work.
- README contains an aligned human-facing summary and no new operational rule that lacks an authoritative copyable owner.
- Given the completed guidance, when `python scripts/verify_package.py` runs, then it passes without weakening existing required-file, project-command, dependency-guidance, ADR, README-distribution, or skill-frontmatter checks.
- Given one guarded activation, tracker or resume, material-drift, or commit-ownership anchor is removed, or one forbidden stale template line is restored, when the focused negative verifier check runs, then it fails with a clear path-specific contract error.
- No new dependency, test framework, semantic documentation linter, package structure, skill name, public workflow artifact, or unrelated behavior is introduced.

#### Likely Files or Areas

- `AGENTS.md`
- `.agents/skills/repo-change-planner/SKILL.md`
- `README.md`
- `scripts/verify_package.py`
- `.agents/skills/long-task-workflow/SKILL.md` for cross-file consistency review after Epic 1
- `.agents/skills/commit-report/SKILL.md` for reference-only ownership review

#### Risks

- Repeating a trigger across several routing surfaces can drift again unless the canonical anchor is concise and guarded.
- Exact phrase checks can become brittle if they enforce prose rather than a stable contract anchor.
- Controlled in-place plan revision can obscure original intent unless the approval and revision note are explicit and affected checklist state is reset.
- Existing generated plans retain legacy frozen-plan wording; they should not be rewritten retroactively, so future guidance must explain rather than conceal that boundary.
- Updating the planner's required handoff directive is high leverage because every future generated plan will copy it verbatim.

#### Recommended Execution Skill

`$long-task-workflow`

## Verification Plan

- Run `python scripts/verify_package.py` and require it to pass after all edits.
- Run `git diff --check` and require it to pass after all edits and again after any temporary negative-test mutations are restored.
- Run `git status --short` before final reporting and confirm only the implementation plan and intended workflow-contract files are changed; distinguish any newly observed unrelated changes rather than modifying them.
- Exercise one focused negative case for each verifier-check class using reversible temporary edits or a copied temporary workspace, restoring the source tree before the final pass:
  - Remove the canonical activation anchor from one routing surface and confirm a path-specific alignment failure.
  - Remove one required authoritative-tracker or interruption-resume anchor and confirm a focused workflow-contract failure.
  - Restore a full-line `Suggested commit message:` heading in the long-task final template and confirm the stale-text guard fails.
- Re-run `python scripts/verify_package.py`, `git diff --check`, and `git status --short` after restoring every negative mutation.
- Manually walk the following scenarios against the final instructions:
  - A fresh long task with no plan file uses one native or in-chat tracker and creates no repository tracker by default.
  - A planner-generated brief makes its `## Execution Checklist` authoritative and any chat status a non-competing mirror.
  - Interrupted work with a dirty tree reconciles request, applicable instructions, plan state, diff, pre-existing versus task-owned changes, acceptance evidence, running checks, and stale verification before editing.
  - A minor sequencing or equivalent-verification change continues with a note, while material scope, acceptance, risk, contract, or verification drift stops for explicit approval.
  - An approved in-scope plan revision updates every affected section and resets impacted state; broader approved work receives a superseding or split brief.
  - Verification proceeds from baseline or reproduction through focused phase checks, regression and product-fit review, simplification, then fresh final checks on the final worktree.
  - Incomplete work uses the handoff contract, while final completion has no unchecked required outcome or stale required check.
  - A normal final report contains no suggested commit message, while an explicit commit-message request routes to `$commit-report`.
  - Conditional parallel work has non-overlapping ownership, one checklist coordinator, combined-diff reconciliation, and integrated final verification.
- Manually cross-read `AGENTS.md`, all three skill files, and README to confirm phase ownership, trigger wording, tracker precedence, drift handling, handoff semantics, final-report minimums, and commit-report delegation do not contradict one another.
- Confirm `.agents/skills/commit-report/SKILL.md`, completed files under `docs/plans/`, and existing files under `docs/adr/` were not changed.
- Do not claim runtime agent, cross-session, or multi-agent integration testing; this work changes instruction contracts and their structural verifier only.

## Suggested Handoff Prompt

```text
Use `$long-task-workflow` to implement all epics in `docs/plans/refine-long-task-workflow.md`.

Requested change: refine Agentikit's long-task execution workflow so it has one authoritative tracker, interruption-safe resume and handoff behavior, controlled material plan drift, fresh final-worktree verification, clear artifact ownership, no default commit-message overlap, concise tool-neutral parallel-work guidance, aligned routing, and focused package-contract guards.

Assumptions: none. Preserve Agentikit's existing skill names, copyable-kit structure, applicable `AGENTS.md` authority, compact workflow style, and current commit-report behavior.

Epic 1: update `.agents/skills/long-task-workflow/SKILL.md` to own the execution lifecycle without duplicating root policy. Implement the activation boundary, single-tracker precedence, resume reconciliation, baseline and phase state, non-material variance versus material drift, verification freshness and ordering, purpose-based artifact routing, resumable handoffs, final-report corrections, and conditional multi-agent coordination specified in the plan.

Epic 2: align `AGENTS.md`, `.agents/skills/repo-change-planner/SKILL.md`, README, and `scripts/verify_package.py`. Use one coordination-or-continuity-risk trigger, add the planner's explicit approved-revision or supersession protocol, preserve `$commit-report` as the unchanged owner of explicit commit reporting, and guard only stable workflow anchors and exact stale fragments.

Acceptance criteria: planner-driven execution uses the plan checklist as its sole authoritative progress tracker; unplanned long-task execution uses exactly one native or in-chat tracker; resume reconciles progress with repository and verification evidence; stale checks and unsupported completion state are reopened; material drift cannot change code or plan details before explicit approval; final checks run after regression review and simplification; partial work produces a resumable handoff; normal final reports contain no suggested commit message; all routing surfaces and future planner handoffs agree; and no unrelated workflow, dependency, package structure, or completed record changes.

Out of scope: do not redesign general `AGENTS.md` policy, edit `.agents/skills/commit-report/SKILL.md`, create a mandatory state file or new ADR, retroactively update completed plans, add tool-specific orchestration commands, or build a semantic documentation linter.

Verification: run `python scripts/verify_package.py`, `git diff --check`, the three focused reversible negative verifier checks, the manual scenario matrix, and the cross-file ownership audit described in the plan. Restore every temporary mutation, inspect `git status --short`, and report any verification that remains unrun.

Treat the `## Execution Checklist` in `docs/plans/refine-long-task-workflow.md` as the persistent source of truth for implementation progress. At the start of work and after any interruption, read and reconcile it before proceeding. Update it in the plan file as soon as each checklist condition is satisfied and after each epic or verification phase, and sync it before any pause, handoff, or final response. An in-chat checklist may mirror the plan, but it does not replace updating the plan file. Mark an item complete only after its stated criteria are met. For partial work, blockers, command-access issues, or test failures, leave the item unchecked and add a brief note beneath it. Do not edit other plan sections.
```
