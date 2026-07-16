---
name: long-task-workflow
description: Use when executing substantial repository changes with coordination or continuity risk, such as dependent phases, cross-layer work, unsafe partial states, migrations, refactors, or likely interruption.
---

# Long Task Workflow Skill

Use this skill to execute substantial repository changes that need explicit progress state, phased verification, interruption recovery, or partial handoff.

The goal is enough structure to keep scope, progress, and verification clear without creating busywork.

Read first:

- Every applicable `AGENTS.md` file for the areas being touched.

## When to Use This

Use this workflow when execution has meaningful coordination or continuity risk, for example:

- Dependent phases or cross-layer changes must stay aligned.
- A migration, refactor, or other intermediate state could leave the repository incoherent.
- Work is likely to pause, transfer to another agent, or continue after an interruption.
- Several verification stages must remain fresh through later edits.

File count, command count, or a desired report format is not sufficient by itself. Skip this skill for planning-only work, report-only work, or simple mechanical changes; follow root `AGENTS.md` instead.

## Start and Progress Tracker

After the initial inspection required by `AGENTS.md` and before editing, turn its 2-to-5-step plan into one status-tracked execution plan. Add only long-task-specific phase dependencies, exit criteria, risks, safe pause points, and verification mapping.

Use one authoritative tracker:

- If the task supplies a `docs/plans/*` brief with an `## Execution Checklist`, that checklist is the persistent source of truth for declared progress. Update it first; an in-chat summary may mirror it but must not compete with it.
- Otherwise, maintain one native or in-chat tracker. Do not create a repository tracker unless the user asks.
- Treat the worktree, diff, and verification output as the evidence for tracker state. Reconcile unsupported tracker claims instead of trusting them.

Capture a relevant baseline before implementation:

- Current version-control status and relevant diff, including pre-existing changes when they can be identified.
- Current behavior, reproduction, or characterization evidence when applicable.
- Checks already run, their results, and any known pre-existing failures.

Example:

```md
Execution plan:
- [ ] Inspect current behavior and baseline. Complete when ownership, constraints, and known failures are identified.
- [ ] Implement the first coherent phase. Complete when its outcome and focused verification pass.
- [ ] Implement remaining dependent phases. Complete when their outcomes and focused verification pass.
- [ ] Review regression and product fit, simplify, then rerun affected and final checks on the final worktree.
- [ ] Reconcile the tracker and produce the appropriate handoff or final report.
```

## Resume and Reconcile

At the start of work and after any interruption, reconcile state before editing:

- Reread applicable `AGENTS.md` files, the request, the active plan, its checklist and notes, and the latest handoff.
- Inspect current version-control status and diff plus available verification, running-command, process, and log evidence.
- Distinguish task-owned changes from pre-existing or unrelated changes where possible.
- Reopen checked items that evidence no longer supports, retaining a concise note about why.
- Mark checks stale when later edits could invalidate them.
- Identify the first safe incomplete item and synchronize the authoritative tracker.

Scale this reconciliation to the interruption and diff. Do not blindly redo completed work or blindly trust checked boxes.

## During Work

After each meaningful phase:

- Mark an item complete only when its intended outcome and required verification are satisfied. Implemented-but-unverified work remains incomplete.
- Synchronize the authoritative tracker before publishing an in-chat checkpoint.
- State what changed, what was verified, what remains, and any new risk, blocker, or scope change.
- Leave the repository coherent where practical. If temporary breakage is unavoidable, keep the item incomplete and record the exact state and next safe action.

Before starting a long-running check, record its command, purpose, and expected evidence. If work pauses while it runs, record its process or log location when available; on resume, inspect that state instead of launching a duplicate blindly.

Synchronize the tracker before every planned pause, handoff, or final response. Later edits that can invalidate a completed check reopen that verification requirement.

## Plan Variance and Material Drift

Non-material execution variance may continue with a tracker note when it changes only sequencing, implementation details, newly discovered likely files, or an equivalent verification method, while preserving the requested outcome, scope, acceptance criteria, public behavior and contracts, risk, and verification strength.

Plan drift is material when the plan can no longer be followed accurately, an assumption, scope boundary, acceptance criterion, or out-of-scope rule must change, verification would be weakened, or an applicable `AGENTS.md` confirmation boundary is triggered.

For material drift:

- Stop before making divergent edits.
- Leave affected items incomplete and record the evidence briefly.
- Explain the affected plan sections, meaningful options and tradeoffs, and a recommendation.
- Require explicit user approval to revise or supersede the plan.

For a persistent brief, follow its approved-revision or supersession rules; do not silently edit frozen details. For a native or in-chat tracker, update the confirmed plan before continuing. If approval is denied, continue with the original plan only when it remains viable; otherwise provide a partial or blocked handoff.

## Parallel Work

When parallel execution is available and useful:

- Delegate only independent work with non-overlapping file or module ownership and explicit interface expectations.
- Keep one coordinator as the sole writer of the authoritative tracker.
- Require each workstream to return changed paths, assumptions, and exact verification evidence.
- Reinspect the combined worktree and integrate the evidence instead of accepting delegated completion claims at face value.
- Complete integrated verification before reporting the overall task done.

## Verification Order

Use this order unless the task provides a stronger project-specific sequence:

1. Establish the baseline or reproduction when applicable.
2. Run focused verification after each implementation phase.
3. Review regression preservation and product or UI fit across the combined change.
4. Perform the simplification and comment-preservation pass required by `AGENTS.md`.
5. Rerun affected focused checks and final relevant broader checks against the final worktree.

Record exact commands or manual checks, results, and scope. Distinguish failures as introduced, pre-existing, or unknown when evidence supports that classification. Never treat a stale or unrun check as passing.

## Execution Records

Do not create an ad hoc `context-notes.md` or equivalent progress file by default. Use existing repository conventions or create a persistent task artifact only when the user asks.

Use artifacts by purpose:

- Code and tests capture behavior and verification evidence.
- The execution tracker captures temporary progress state.
- Handoff and final reports communicate execution status.
- Documentation and ADRs capture qualifying durable rationale under `AGENTS.md`.
- `$commit-report` owns explicitly requested current-diff, commit-message, and commit-style reporting.

## Handoff Notes

Use a handoff when stopping before completion because of a pause, blocker, permission boundary, user transfer, session boundary, or still-running command.

Synchronize the authoritative tracker first, then report:

```md
Current state:
- Tracker or plan:
- Completed:
- In progress:
- Remaining:
- Reason for stopping:
- Task-owned changes:
- Pre-existing or unrelated changes:
- Checks run: <command or manual check, result, and whether fresh or stale>
- Not verified:
- Known issues:
- Running processes or logs:
- Next safe action:
```

Do not place partial, blocked, stale, failed, running, or unverified work under completed items.

## Final Report

Use the final report only when every required tracker outcome is complete and required verification is fresh. Otherwise use the handoff contract.

End a completed large task with:

- Summary of behavior changed.
- Files changed, distinguishing unrelated work when necessary.
- Checks actually run and their results.
- Work not verified.
- Regression and product or UI fit review.
- Simplification pass result, including any non-trivial existing comment removal or rewrite.
- Follow-up steps, if any.
- Remaining risk.

Use `$commit-report` only when explicitly requested for a current diff summary, suggested commit message, or commit-style report. Treat it as a separate final read-only reporting phase.

Suggested compact implementation report:

```text
Summary:
- <behavior or outcome changed>

Files changed:
- `<path-or-file-name>`

Checks run:
- `<command-or-manual-check>` - passed or failed.

Not verified:
- <unrun or stale verification, or none>

Regression and fit review:
- <existing behavior preserved and UI/product fit checked where relevant, or not applicable>

Simplification pass:
- <what was simplified, or no meaningful simplification needed; mention any non-trivial existing comment removal or rewrite>

Follow-up steps:
- <guidance for anything the user should do next, or none>

Risks:
- <remaining risk, or none>
```
