# Implementation Brief: Align README with the Copyable Kit

## Requested Change

Align Agentikit's human-facing README, copyable agent guidance, package verifier, and durable decision records so the README is clearly a source-repository overview rather than an agent instruction dependency. Ensure every operational rule an agent may need in a consuming repository is present in `AGENTS.md`, `.agents/skills/`, or `docs/agent/`. Keep `docs/adr/` and `docs/plans/` as reusable directory conventions while making clear that the records inside them are repository-specific and should not be copied into another project.

## Existing Context Found

- `README.md` describes the project history, package layout, installation, skill catalog, optional references, maintainer check, cross-agent compatibility, and guidance ownership.
- Most behavioral statements in `README.md` already have an agent-visible owner:
  - The core work principles and skill/doc routing are in `AGENTS.md`.
  - Plan files as working artifacts and ADRs as durable records are defined in `.agents/skills/repo-change-planner/SKILL.md`, `.agents/skills/long-task-workflow/SKILL.md`, `AGENTS.md`, and `docs/agent/adr-template.md`.
  - Skill triggers and workflows are defined in each skill's `SKILL.md` and routed from `AGENTS.md`.
- The README-only cross-agent fallback—keep canonical skill files and add a tool-specific pointer instead of duplicating them—is operational guidance that a consuming agent may need but cannot currently discover from the copyable files.
- The broader ownership rule—human-facing README content must not be the exclusive source of agent-operational instructions—is stated by repository intent but is not encoded in the copyable guidance.
- `README.md` currently tells users to copy the whole `docs/plans/` path even though `docs/plans/` contains repository-specific plan Markdown that should not be distributed. Its contents tree also shows only `.gitkeep` under `docs/plans/`, so it does not accurately distinguish source-repository contents from the empty target scaffold.
- `docs/adr/` currently contains only `.gitkeep`. The user has clarified that Agentikit may store its own ADRs there, following the same distribution model as `docs/plans/`: the directory convention is reusable, but each contained record belongs to the repository that created it.
- The documentation-authority and distribution boundary qualifies for an ADR under `docs/agent/adr-template.md`: it chooses between real alternatives, captures a non-obvious constraint in a self-modifying kit, and must remain visible to future maintainers.
- `scripts/verify_package.py` verifies required source files, broad README copy-path strings, skill metadata, and selected guidance phrases. It does not verify that README and scripts are source-only, that repository-specific plans and ADRs are excluded from copy instructions, that the Agentikit ADR recording this contract remains present, or that README-only operational guidance has an agent-visible owner.
- `git status --short` was clean before this plan file was created.

## Assumptions

- "Material to the kit's functionality" means rules, routing, or workflows an agent may need while operating in a consuming repository. Project history, attribution, human installation steps, and source-repository maintenance commands may remain README-only.
- Consumers may copy any useful subset of `AGENTS.md`, `.agents/skills/`, and `docs/agent/`. They may also copy or recreate the `docs/adr/` and `docs/plans/` directory conventions without copying the source repository's records.
- Files under `docs/adr/` and `docs/plans/` are repository-specific working or decision records. They are not reusable kit content even though the directory names, `.gitkeep` placeholders, and supporting templates or workflows are reusable.
- Existing repository-specific files in `docs/plans/` remain in place and are not modified or deleted by this work. A new Agentikit-specific ADR may be added under `docs/adr/`.
- `README.md` and `scripts/verify_package.py` remain source-repository files and are not part of the kit copied into consuming repositories.
- The new guidance should still allow agents to read a project's README for project context; it should only prohibit relying on README as the sole location for agent-operational instructions.

## Open Questions

No blocking open questions. The user has confirmed that the decision should be recorded in `docs/adr/` and that ADR contents, like plan contents, are specific to the repository that created them. The recommended default filename is `docs/adr/0001-keep-agent-guidance-in-copyable-files.md`.

## Plan File Use

This plan is a working artifact, not durable documentation. The user explicitly authorized this revision to add the ADR decision and distribution model. After this revision, do not rewrite its requested change, assumptions, open questions, scope, epics, acceptance criteria, risks, verification plan, or handoff prompt unless the user explicitly authorizes another update. During implementation, update only checklist state and add brief notes beneath the relevant checklist item.

## Execution Checklist

- [x] User confirmed assumptions are valid.
- [x] Open questions are resolved or explicitly accepted as non-blocking.
- [x] Epic 1 acceptance criteria met.
- [x] Epic 2 acceptance criteria met.
- [x] Epic 3 acceptance criteria met.
- [x] Epic 4 acceptance criteria met.
- [x] Verification plan completed.
- [x] ADR recorded and checked for consistency with the implemented contract.

## Out of Scope

- Do not copy, move, delete, or rewrite the existing repository-specific files under `docs/plans/`.
- Do not treat the new Agentikit ADR as a reusable template or copy it into consuming repositories.
- Do not rewrite project history, attribution, licensing, or the substantive coding standards.
- Do not redesign the skills, rename skill metadata, or alter their task workflows.
- Do not add package-manager tooling, a documentation framework, or generalized README-content linting.
- Do not instruct agents to ignore project READMEs; they may remain valuable sources of project context and human-facing setup information.

## Implementation Epics

### Epic 1: Put Portable Guidance in Agent-Visible Files

#### Goal

Give consuming agents a concise, copyable source of truth for guidance placement and cross-agent skill discovery without duplicating README prose.

#### Tasks

- Add a compact guidance-ownership rule to `AGENTS.md`: broadly applicable agent rules belong in `AGENTS.md`, repeatable workflows belong in `.agents/skills/`, and longer task-specific references belong in `docs/agent/`.
- State that operational instructions required by an agent must not exist only in a human-facing README, while preserving README as a valid source of project context.
- Move or restate the README-only cross-agent fallback in `AGENTS.md`: when a tool does not discover `.agents/skills/`, use a small tool-specific pointer to the canonical skill rather than maintaining duplicate skill copies unless duplication is required.
- Keep the addition short enough to preserve the root file's compact, always-loaded role and avoid repeating existing skill triggers or optional-doc descriptions.

#### Acceptance Criteria

- Given a consuming repository without this source README, when an agent reads `AGENTS.md`, then it can determine where always-loaded rules, repeatable workflows, and optional reference guidance belong.
- Given an agent tool that does not auto-discover `.agents/skills/`, when the copied guidance is available, then the agent is told to point the tool to the canonical skill files and avoid unnecessary duplicate copies.
- The guidance must not tell agents to ignore README content or prevent them from using README as project context.
- No skill workflow, core coding rule, or optional-reference trigger is duplicated in full.

#### Likely Files or Areas

- `AGENTS.md`

#### Risks

- An overly broad README warning could discourage agents from reading legitimate project setup or architecture context.
- Too much packaging guidance in `AGENTS.md` would increase the always-loaded context for every consuming repository.

#### Recommended Execution Skill

Root `AGENTS.md` only

### Epic 2: Correct README Scope and Copy Instructions

#### Goal

Make the human-facing README accurately distinguish reusable directory conventions from repository-specific records and prevent consumers from copying Agentikit's plans or ADRs into another project.

#### Tasks

- State near the usage guidance that `README.md` is a human-facing source-repository overview, is not intended to be copied, and must not be the sole owner of agent-operational guidance.
- Describe the reusable paths as independently selectable components rather than implying every path is mandatory.
- Explain that users may copy or recreate the `docs/adr/` and `docs/plans/` directory conventions, but should not copy the Markdown records currently stored inside either directory.
- Make the source contents tree and recommended target tree clearly distinguish actual repository-specific ADR and plan files from target `.gitkeep` placeholders, without turning the README into a complete record index.
- Keep source-only information—history, attribution, human copy mechanics, ignore-file suggestions, and the maintenance verification command—in the README.
- Shorten or remove duplicated operational prose after its canonical rule exists in `AGENTS.md`, replacing it with a pointer where useful.

#### Acceptance Criteria

- Given a user following `README.md`, when they assemble a target kit, then they do not copy `README.md`, `scripts/verify_package.py`, existing `docs/plans/*.md`, or any source ADR records.
- Given a user wants only part of the kit, when they read the copy instructions, then they understand the listed components may be selected individually.
- Given `docs/adr/` and `docs/plans/` are included, when established in a target repository, then each starts empty apart from an optional placeholder and later contains only that target repository's own records.
- The README continues to explain hidden `.agents/` handling, merging an existing `AGENTS.md`, filling project commands, optional generated-plan ignores, and running the source maintenance check.
- No material agent workflow or rule remains exclusively in the README after comparison with `AGENTS.md`, `.agents/skills/`, and `docs/agent/`.

#### Likely Files or Areas

- `README.md`

#### Risks

- Listing source-repository plans or ADRs in the package tree could accidentally advertise them as reusable.
- Over-condensing the README could make the human installation path less clear even if the agent guidance is correctly owned.

#### Recommended Execution Skill

Root `AGENTS.md` only

### Epic 3: Enforce the Distribution Contract

#### Goal

Update the maintenance verifier so future edits cannot silently reintroduce ambiguous copy instructions or source-only content into the advertised kit.

#### Tasks

- Refactor verifier names or groupings as needed to distinguish required source-repository files from paths advertised as copyable kit components.
- Replace broad `docs/adr/` and `docs/plans/` README substring checks with assertions that distinguish reusable directory conventions from repository-specific records.
- Add the Agentikit ADR created in Epic 4 to the required source-repository contract without advertising it as a copyable file.
- Require concise README language that excludes source-specific ADR and plan Markdown, README, and the maintenance script from the target kit.
- Require the copyable guidance to contain the portable ownership and cross-agent fallback rules added in Epic 1.
- Keep checks structural and phrase-focused; do not attempt semantic equivalence analysis or build a general documentation linter.

#### Acceptance Criteria

- Given the aligned repository, when `python scripts/verify_package.py` runs, then it passes.
- Given the Agentikit ADR is removed or no longer recognized as a required source record, when the verifier runs, then it fails with a focused source-contract error.
- Given README copy guidance again advertises the whole source contents of `docs/adr/` or `docs/plans/`, or omits the source-only exclusions, when the verifier runs, then it fails with a clear copy-contract error.
- Given the agent-visible ownership or cross-agent fallback rule is removed from `AGENTS.md`, when the verifier runs, then it fails with a focused guidance error.
- Existing required-file, project-command, dependency-guidance, forbidden-phrase, and skill-frontmatter checks remain intact.

#### Likely Files or Areas

- `scripts/verify_package.py`
- `README.md`
- `AGENTS.md`

#### Risks

- Exact prose checks can become brittle if they enforce a sentence rather than a stable invariant.
- Filesystem and README checks must distinguish the intentionally non-empty source `docs/adr/` and `docs/plans/` directories from the empty starting directories recommended for a target repository.

#### Recommended Execution Skill

`$long-task-workflow`

### Epic 4: Record the Durable Package Decision

#### Goal

Preserve the documentation-authority and distribution decision for future Agentikit maintainers without turning the decision record itself into reusable kit content.

#### Tasks

- Create `docs/adr/0001-keep-agent-guidance-in-copyable-files.md` using `docs/agent/adr-template.md` and mark it accepted.
- Explain the self-modifying context: Agentikit uses its own copied rules and workflows, so README-only behavior can disappear when the kit is used elsewhere and can be accidentally reintroduced during future edits.
- Record the decision that agent-operational guidance must have an authoritative home in `AGENTS.md`, `.agents/skills/`, or `docs/agent/`; README remains a human-facing, source-only overview.
- Record that `docs/adr/` and `docs/plans/` are reusable directory conventions, while their Markdown contents are specific to the repository that created them and should not be copied as kit material.
- Record the verifier's role as a guardrail for objective distribution invariants, not as a semantic documentation linter.
- Include the meaningful alternatives: allowing README to own operational guidance, copying all source documentation wholesale, or placing Agentikit's ADRs in a separate maintainer-only directory.

#### Acceptance Criteria

- Given a future maintainer asks why README cannot be authoritative for agent behavior, when they read the ADR, then the self-hosting and portability rationale is explicit.
- Given a consumer sees `docs/adr/` or `docs/plans/` in the recommended layout, when they read the ADR and README, then they can distinguish reusable directory conventions from non-reusable repository records.
- The ADR follows the numbering, status, context, decision, alternatives, consequences, and verification format in `docs/agent/adr-template.md`.
- The ADR describes durable policy and rationale rather than duplicating exact verifier phrases or implementation details.
- `README.md`, `AGENTS.md`, `scripts/verify_package.py`, and the ADR do not contradict one another.

#### Likely Files or Areas

- `docs/adr/0001-keep-agent-guidance-in-copyable-files.md`
- `docs/agent/adr-template.md` for format reference only

#### Risks

- An overly implementation-specific ADR would become stale when verifier wording changes.
- Storing the ADR under the reusable directory name could confuse consumers unless README copy guidance clearly excludes repository-specific records.

#### Recommended Execution Skill

Root `AGENTS.md` only

## Verification Plan

- Run `python scripts/verify_package.py` and require it to pass.
- Run `git diff --check` and require it to pass.
- Manually inventory all operational statements in `README.md` and map each to `AGENTS.md`, a skill, or an optional agent reference; classify history, attribution, installation mechanics, and source maintenance as non-operational human content.
- Manually confirm the README distinguishes:
  - Source-only `README.md` and `scripts/verify_package.py`.
  - Selectable copyable guidance paths.
  - Reusable directory conventions and empty target starting points for `docs/adr/` and `docs/plans/`.
  - Repository-specific `docs/adr/*.md` and `docs/plans/*.md` files that must not be copied.
- Review `docs/adr/0001-keep-agent-guidance-in-copyable-files.md` against `docs/agent/adr-template.md` and confirm its decision matches `README.md`, `AGENTS.md`, and verifier behavior.
- Exercise new verifier failure paths with temporary, reversible test edits or a focused test harness, restoring the workspace after each check:
  - Temporarily make the required Agentikit ADR unavailable and confirm a focused source-contract failure.
  - Temporarily remove the README exclusion for either ADR or plan records and confirm a focused copy-contract failure.
  - Temporarily remove each new required contract phrase and confirm a focused failure.
- Re-run `python scripts/verify_package.py` and `git diff --check` after restoring all temporary test changes.
- Do not claim runtime or cross-agent integration testing; this work changes documentation and structural verification only.

## Suggested Handoff Prompt

```text
Implement all epics in `docs/plans/align-readme-with-copyable-kit.md`.

Align Agentikit so README remains a human-facing, source-only overview and no agent-operational instruction depends on it. Add only the concise portable ownership and cross-agent discovery rules needed in `AGENTS.md`; correct README copy guidance so components are selectable and the `docs/adr/` and `docs/plans/` directory conventions are reusable without their repository-specific records; strengthen `scripts/verify_package.py` to enforce those objective distribution invariants; and create the accepted Agentikit ADR specified in Epic 4.

Preserve existing repository-specific plans, substantive coding guidance, skill workflows, source history, attribution, human setup guidance, and current verifier checks. Treat Agentikit's ADR and plan Markdown as source-repository records that should not be copied into consuming projects. Do not tell agents to ignore project READMEs, and do not add a general documentation linter.

Use `$long-task-workflow` for the full four-epic implementation. Run `python scripts/verify_package.py`, `git diff --check`, the focused negative verifier checks described in the plan, the ADR consistency review, and the final manual README-to-copyable-guidance ownership audit. Report changed files, simplification result, passed and skipped verification, remaining risk, and ADR consistency.
```
