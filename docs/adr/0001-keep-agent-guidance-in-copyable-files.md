# ADR 0001: Keep Agent Guidance in Copyable Files

Date: 2026-07-10
Status: Accepted

## Context

Agentikit is both a source repository and a kit used to modify itself. Consumers may copy `AGENTS.md`, skills, optional agent guidance, and the `docs/adr/` and `docs/plans/` directory conventions into other repositories. They are not expected to copy this source repository's README, maintenance scripts, plans, or decision records.

If an operational rule exists only in Agentikit's README, an agent using the kit elsewhere may never receive it. The same mistake can recur during future Agentikit changes because the source README is easy to treat as authoritative even though it is not part of the reusable kit.

The repository also needs a clear distinction between reusable directory conventions and the records stored in them. Plans and ADRs describe the repository that created them; copying Agentikit's records into another project would give that project's agents irrelevant or misleading context.

## Decision

Agent-operational guidance must have an authoritative home in the files intended to travel with the kit:

- `AGENTS.md` owns broadly applicable rules and routes agents to deeper guidance.
- `.agents/skills/` owns repeatable task workflows.
- `docs/agent/` owns longer task-specific reference material.

`README.md` remains a human-facing overview for Agentikit's history, contents, installation, and source maintenance. It may summarize operational behavior, but it must not be the only place an agent can learn a rule required while working in a consuming repository. `README.md` and `scripts/` are source-repository files and are not copied as kit content.

`docs/adr/` and `docs/plans/` are reusable directory conventions. Markdown records inside them belong to the repository that created them and are not reusable kit content. A consuming repository should start those directories empty, apart from an optional placeholder, and create its own ADRs and plans.

The package verifier will enforce objective parts of this contract, such as required source files and explicit distribution guidance. It will not attempt to determine semantic equivalence across documentation.

## Alternatives Considered

### Allow README to own operational guidance

Rejected because README is not copied with the kit and is not guaranteed to be available to an agent in a consuming repository.

### Copy all source documentation

Rejected because Agentikit's plans and ADRs describe this repository. Distributing them as reusable guidance would mix source history with the target repository's own working and decision records.

### Store Agentikit ADRs in a maintainer-only directory

Rejected because `docs/adr/` is already the established location for repository decisions. Treating its directory convention as reusable while treating its records as repository-specific is consistent with `docs/plans/` and avoids a second decision-record system.

## Consequences

Agents using a copied kit can discover every required operational rule without Agentikit's README. Maintainers must place new rules in an agent-visible owner before summarizing them in README.

Consumers must selectively copy or recreate `docs/adr/` and `docs/plans/` rather than copying their Markdown contents wholesale. README copy guidance must make that boundary explicit.

The verifier provides regression protection for structural and explicit wording contracts, but maintainers still need to review whether new README guidance is materially operational. Exact verification phrases may need coordinated updates when equivalent wording changes.

## Verification

Confirm `AGENTS.md` states the guidance ownership and cross-agent discovery rules. Confirm README identifies itself and `scripts/` as source-only, and distinguishes reusable directory conventions from repository-specific ADR and plan records.

Run `python scripts/verify_package.py` and `git diff --check`. Review future README changes for operational guidance that lacks an authoritative copyable owner.
