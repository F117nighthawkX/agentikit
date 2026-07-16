---
name: coordinate-change-execution
description: Execute substantial repository changes that need explicit progress state, phased verification, interruption recovery, partial handoff, or coordinated integration. Use when execution has coordination or continuity risk, such as dependent or cross-layer phases, unsafe intermediate states, migrations, refactors, likely interruption, or verification that later edits can make stale. Do not use for planning-only, report-only, or simple mechanical changes.
---

# Coordinate Change Execution Skill

Read first:

- Every applicable `AGENTS.md` file for the areas being touched.

## Activation Check

Planning-only, report-only, and simple mechanical work should follow applicable `AGENTS.md` files without this workflow. File count, command count, and report format alone do not trigger it.

## Establish or Reconcile State

At the start of work and after any interruption, read or reread the request, applicable instructions, active plan and notes, and latest handoff before editing. Identify the progress authority before creating or updating tracker state:

- If a supplied `docs/plans/*` brief contains an `## Execution Checklist`, identify it as the persistent source of truth for declared progress.
- Otherwise, identify and reuse any existing built-in or in-chat tracker. If none exists, leave tracker state uninitialized until after inspection. Do not create a repository tracker unless the user asks.

Inspect and reconcile the baseline before establishing or changing progress state:

- Inspect version-control status and the relevant diff; distinguish task-owned, pre-existing, and unrelated changes where possible.
- Capture current behavior, reproduction, or characterization evidence when applicable.
- Inspect check results plus running-command, process, and log evidence. Record known pre-existing failures.

After inspecting and reconciling that evidence:

- For a persistent checklist, reopen unsupported items with a brief note, then map conceptual execution phases onto its items. Record permitted notes beneath the active item rather than create another status plan. A native or in-chat mirror may show only the same item identities and statuses and must not make independent completion claims. Update the persistent checklist before its mirror.
- For an existing built-in or in-chat tracker, reopen unsupported items with a brief note and mark affected checks stale.
- If no tracker exists, make the 2-to-5-step plan required by `AGENTS.md` the sole status-bearing execution tracker in the built-in plan facility or chat. Add only needed dependencies, exit criteria, risks, safe pause points, and verification mapping.

The tracker declares progress; worktree, diff, behavior, and verification determine validity. Identify the first safe incomplete item and synchronize it.

Scale reconciliation to the interruption and diff. Do not redo completed work or trust unsupported boxes.

## Execute the Phase Loop

For each meaningful phase:

- Use its intended outcome, exit criteria, and mapped focused verification.
- Keep the repository coherent where practical. If temporary breakage is unavoidable, leave the item incomplete and record the exact state and next safe action.
- Mark the item complete only after its outcome and required verification are satisfied. Implemented-but-unverified work remains incomplete.
- If a required check fails, do not advance unless evidence establishes that the failure is pre-existing or irrelevant and continuing is safe.
- After evidence supports a status change, synchronize the tracker before checkpointing what changed, what was verified, what remains, and any new risk, blocker, or scope change.

For a check likely to outlive the turn or a planned pause, record its command, purpose, expected evidence, and process or log location. On resume, inspect that state before launching another run.

Synchronize before every planned pause, handoff, or final response. Later edits that invalidate verification reopen it.

## Plan Variance and Material Drift

Note and continue only when variance affects sequencing, implementation details, newly discovered files, or equivalent verification while preserving the requested outcome, scope, acceptance criteria, public contracts, risk, and verification strength.

Treat drift as material when the plan becomes inaccurate, an assumption, scope boundary, acceptance criterion, or out-of-scope rule must change, verification would weaken, or an `AGENTS.md` confirmation boundary is triggered.

For material drift:

- Stop before divergent edits.
- Leave affected items incomplete and record the evidence briefly.
- Explain the affected plan sections, meaningful options and tradeoffs, and a recommendation.
- Require explicit user approval to revise or supersede the plan.

For a persistent brief, follow its approved-revision or supersession rules; never edit frozen details silently. For a native or in-chat tracker, update the confirmed plan before continuing. If approval is denied, continue only when the original remains viable; otherwise hand off partial or blocked work.

## Parallel Work

When parallel execution is available and useful:

- Delegate independently completable work with explicit interfaces. Read-only investigations may overlap; mutating work should have non-overlapping write ownership.
- Keep one coordinator as the sole writer of the authoritative tracker.
- Require each workstream to return findings, assumptions, exact verification evidence, and changed paths when applicable.
- Reinspect the combined worktree and evidence; do not trust delegated completion claims.
- Complete integrated verification before reporting the overall task done.

## Final Worktree Gate

Complete every outcome below. A stronger project-specific sequence may reorder or add steps but must not omit or weaken these outcomes:

1. Review the combined diff against the request, scope boundaries, and pre-existing or unrelated changes.
2. Review regression preservation and product or UI fit across the combined change.
3. Perform the simplification and comment-preservation pass required by `AGENTS.md`.
4. Rerun affected focused checks and final relevant broader checks against the final worktree.

Record exact commands or manual checks, results, and scope. Classify failures as introduced, pre-existing, or unknown only with supporting evidence. Never treat a stale or unrun check as passing.

Do not create an ad hoc `context-notes.md` or equivalent by default. Code and tests capture behavior and evidence; the tracker captures temporary progress; reports communicate state; and documentation or ADRs capture qualifying durable rationale.

## Handoff or Completion

Use a handoff whenever stopping with incomplete, blocked, failed, stale, or running state, or at a permission, transfer, session, or command boundary. Synchronize the tracker first, then report:

```md
Current state:
- Goal and scope:
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

Keep partial, blocked, stale, failed, running, or unverified work out of completed items. Make the handoff self-contained for a new agent or session; omit only inapplicable fields.

Use a final report only when every required outcome is complete and verification is fresh. Include the `AGENTS.md` report requirements, final tracker state, task-owned versus unrelated changes when relevant, regression or product-fit review, and remaining risk.

Use `$commit-report` only when explicitly requested for a current diff summary, suggested commit message, or commit-style report. Treat it as a separate final read-only reporting phase.
