# Implementation Brief: Prefer Project-Fitting Ecosystem Solutions

## Requested Change

Revise Agentikit's implementation guidance so agents choose the best proportionate solution for the project rather than minimizing imports, dependencies, API calls, or local diff size. Agents should freely use APIs from declared project dependencies and may add a focused, established dependency—even for a single call site—when it materially improves correctness, reliability, security, interoperability, clarity, or long-term maintenance and its broader purpose and capability fit the project's responsibilities, constraints, and direction.

Keep the policy anti-bloat rather than dependency-averse: prefer language, platform, and standard-library capabilities for straightforward native logic; reject domain-mismatched packages and disproportionate heavyweight frameworks or libraries for narrow work; and retain explicit discussion or approval for changes that materially affect architecture, toolchains, runtimes, deployment, security boundaries, or public contracts.

## Existing Context Found

- `AGENTS.md` is the primary copyable instruction source and is read by every included skill. Its combination of "smallest correct implementation," "do not add a new pattern," and "match existing style" can make agents optimize for a small diff unless "smallest" is defined in terms of total unnecessary complexity rather than lines, imports, or packages.
- `AGENTS.md` currently prohibits "new dependencies when a small local implementation or existing dependency is enough." This directly encodes a local-first tie-breaker and conflicts with the clarified preference for a well-fitting, established package when it avoids bespoke ownership or provides meaningful broader value.
- `AGENTS.md` asks agents to identify an unrequested "framework" they are rejecting without distinguishing framework adoption or replacement from ordinary use of the project's selected stack.
- `docs/agent/architecture-boundaries.md` says "Do not add dependencies by default" and asks agents to "Explain why a local implementation is worse." These rules place an asymmetric burden on dependencies rather than comparing the lifecycle benefits and costs of both options.
- The same dependency section correctly checks maintenance, license, install size, runtime cost, security, and platform compatibility. Those safeguards should remain and be expanded to include purpose and project fit, project direction, transitive footprint, bundle or startup impact, and operational burden.
- `docs/agent/architecture-boundaries.md` requires explicit approval for broad categories such as frameworks, code generation, state managers, queues, ORMs, and build tools. The useful boundary is material architectural or operational impact: ordinary focused libraries should not require blanket design approval solely because a manifest or lockfile changes, while architecture-scale adoption should still be surfaced and approved.
- `.agents/skills/long-task-workflow/SKILL.md` repeats "add the smallest behavior change" close to implementation time. It should refer to the smallest complete, project-fitting change so it does not reinforce import or dependency minimization.
- `.agents/skills/repo-change-planner/SKILL.md` says stack and framework decisions are already made. In context this prevents speculative stack reselection; it does not prohibit adding a library or using more of the selected framework. `.agents/skills/commit-report/SKILL.md` contains no dependency-selection policy. Neither needs duplicated guidance.
- `README.md` describes the kit's philosophy as surgical and anti-speculative. It should briefly state that surgical scope means proportionate total complexity, not automatic preference for hand-written code.
- `scripts/verify_package.py` checks structure and selected copy-contract wording but does not guard the intended dependency decision policy.
- The earlier version of this plan addressed installed framework imports but still preserved blanket scrutiny or approval for package additions. This revision supersedes that narrower approach in response to the user's clarified initiative.

## Assumptions

- The user has confirmed that a focused, established new dependency may be preferable to bespoke code—even when used at only one call site—if it provides meaningful benefits and its broader purpose fits the project.
- Call-site length and local implementation length are not reliable measures of complexity. The comparison should include behavior and edge cases the dependency owns, future maintenance, ecosystem conventions, and the dependency's full lifecycle footprint.
- Simple logic already expressed clearly and correctly by the language, platform, or standard library should remain native; a package that merely wraps trivial built-ins is bloat rather than an industry-standard improvement.
- "Industry standard" is favorable evidence, not an automatic reason to add a package. Maintenance health, security posture, licensing, compatibility, footprint, and project fit still matter.
- Project direction must be evidenced by the current stack, repository documentation or roadmap, established nearby architecture, or an explicit user statement. Agents should not invent future framework needs to justify a heavy dependency.
- Using an API from an existing declared direct dependency is ordinary implementation. A package that happens to be present only transitively should not be imported silently; it should be evaluated and declared directly if selected.
- Ordinary, proportionate package additions may proceed as part of an authorized implementation without separate design approval solely because they update a manifest or lockfile. Separate environment, network, or tool-execution permissions still apply.
- Adopting or replacing a major framework, or adding something that materially changes architecture, the toolchain, runtime, deployment model, security boundary, or public contract, remains approval-worthy even when it is a legitimate recommendation.
- The reusable rules should be framework-neutral. Astro, Tailwind, Kubernetes, React, Vue, Angular, Lodash, and jQuery are useful review scenarios, not names that need to appear in the final policy.

## Open Questions

No blocking open questions. The user's clarification supplies the missing dependency preference, and the impact-based approval boundary preserves the kit's safety posture without reinstating a default-deny package policy.

## Plan File Use

This user-requested revision supersedes the earlier version of the working brief. Once implementation begins, update only checklist state and concise notes beneath the relevant checklist item; do not rewrite the plan's detail sections unless the user explicitly requests another planning revision. Mark an epic complete only when its acceptance criteria are met.

## Execution Checklist

- [x] User confirmed assumptions are valid.
- [x] Open questions are resolved or explicitly accepted as non-blocking at implementation start.
  - Implementation began with the plan's stated assumptions confirmed and no blocking questions.
- [x] Epic 1 acceptance criteria met.
  - `AGENTS.md` now defines minimum unnecessary total complexity, permits project-fitting declared APIs and new dependencies, and retains native, redundancy, fit, and material-approval safeguards.
- [x] Epic 2 acceptance criteria met.
  - `docs/agent/architecture-boundaries.md` now compares lifecycle value and cost proportionately, covers purpose, health, footprint, declared/transitive use, and reserves approval for material impact.
- [x] Epic 3 acceptance criteria met.
  - The workflow and README now reinforce the root policy concisely; the verifier detects eight missing or restored dependency-policy contracts in mutation checks.
- [x] Verification plan completed.
  - The package check, tracked and plan whitespace checks, scoped consistency search, old-rule absence check, eight mutation checks, and ten-scenario manual matrix passed.
- [x] ADR need considered after completion.
  - No ADR is needed: this refines reusable implementation policy without changing Agentikit's architecture or copyable-kit structure.

## Out of Scope

- Making third-party packages the default for trivial logic already handled cleanly by the language, platform, or standard library.
- Treating every popular or "industry-standard" package as appropriate without evaluating health, security, footprint, and project fit.
- Adding domain-mismatched packages for incidental utilities or using speculative future needs to justify current bloat.
- Removing discussion or approval requirements for major framework adoption or replacement, architecture changes, toolchain changes, runtime or deployment changes, security-sensitive dependencies, or public-contract changes.
- Creating framework-specific allowlists, denylists, package-size thresholds, or a numeric dependency scoring system.
- Adding, removing, upgrading, or consolidating actual project dependencies; this plan changes Agentikit's reusable instructions only.
- Refactoring unrelated guidance, redesigning the kit's documentation structure, or duplicating the full dependency policy across every skill.

## Implementation Epics

### Epic 1: Define Proportionate Solutions in the Root Rules

#### Goal

Make `AGENTS.md` unambiguous that agents should minimize unnecessary total complexity, not dependency count, import count, API-call count, line count, or diff size.

#### Tasks

- Amend the planning language so an unrequested "framework" clearly means adopting or replacing a framework or making another material architecture choice, not normal use of the selected stack.
- Define the "smallest correct implementation" as the least unnecessary total complexity that fully solves the request. Include both locally owned code and dependency, transitive, build, runtime, and operational costs in that concept.
- Replace the local-first prohibition on new dependencies with a balanced rule:
  - use native or standard-library capabilities for straightforward logic they handle cleanly;
  - use supported APIs from declared project dependencies normally;
  - prefer a focused, established, project-fitting dependency over bespoke code when its meaningful benefits and avoided ownership outweigh its footprint, even if the local helper would be short or the dependency is used once;
  - avoid domain-mismatched or disproportionate dependencies.
- State that agents should not recreate established ecosystem functionality merely to keep the dependency list or diff smaller.
- Clarify that existing patterns are evidence and a consistency default, not a veto against a better framework-native or ecosystem-standard approach. Preserve the requirement to investigate surprising structure and explain material tradeoffs.
- Keep the root wording compact and principle-based; put the detailed evaluation checklist in `docs/agent/architecture-boundaries.md`.

#### Acceptance Criteria

- Given an API from a declared project dependency, when it is the clearest project-fitting solution, then the root rules permit normal import and use without treating it as a dependency or framework change.
- Given a focused, maintained package that materially improves correctness, reliability, standards compliance, interoperability, security, clarity, or maintenance over bespoke code, when its purpose, capability, and footprint fit the project, then the root rules permit and may prefer adding it even for a single call site or short helper.
- Given a declared dependency that already provides a comparably clear, reliable, and maintainable solution, when a new package has no material advantage, then the root rules favor the declared dependency and avoid redundant ecosystem overlap.
- Given straightforward logic that the language or standard library handles cleanly, when an external wrapper offers no meaningful additional value, then the root rules favor the native implementation.
- Given a domain-mismatched package or a heavyweight framework for a narrow lightweight tool, when no evidenced project direction supports it, then the root rules reject it as disproportionate.
- Given a major framework, toolchain, runtime, deployment, security-boundary, or public-contract change, when it could be beneficial, then the agent presents it as a legitimate option and seeks the required approval instead of silently adopting or reflexively dismissing it.
- The rules explicitly reject imports, packages, lines, call sites, and diff size as standalone optimization targets while retaining limits on unrelated scope and unnecessary complexity.
- A single-use dependency is not classified as bloat solely because it has one call site, and a one-line library call is not accepted solely because it is short.

#### Likely Files or Areas

- `AGENTS.md` sections 1 through 3

#### Risks

- Overcorrecting from local-first to dependency-first could cause micro-package proliferation.
- "Best" and "project fit" can become vague; the root rule must point to concrete benefits and costs without becoming a long rubric.
- Agents may confuse a transitively installed package with a declared project dependency.

#### Recommended Execution Skill

Root `AGENTS.md` only

### Epic 2: Replace the Default-Deny Dependency Policy

#### Goal

Turn `docs/agent/architecture-boundaries.md` into a symmetric, impact-based dependency decision guide that supports valuable industry-standard packages while screening out bloat and architecture-scale surprises.

#### Tasks

- Rewrite the `Dependencies` section rather than merely defining "dependency."
- Remove "Do not add dependencies by default" and replace it with an instruction not to add or reject a dependency reflexively.
- Replace "Explain why a local implementation is worse" with a fair comparison of total lifecycle value and cost for the local and package options.
- Organize the comparison around:
  - capability: whether the language, platform, standard library, an existing declared dependency, or a new package handles the behavior correctly;
  - benefit: correctness and edge cases, security, standards compliance, interoperability, clarity, testability, maintenance ownership, and ecosystem conventions;
  - fit: whether the capability is relevant and proportionate; whether the dependency's broader purpose is congruent with the project's responsibilities and constraints; and whether it fits the current stack, established architecture, and evidenced direction. General-purpose ecosystem libraries may fit without being specific to the application's business domain;
  - cost: maintenance health, API stability, license, security and supply-chain exposure, direct and transitive footprint, install or bundle size, startup and runtime cost, platform compatibility, build impact, and operational burden.
- Scale the depth of evaluation and explanation to the dependency's risk and impact. A routine, well-known, low-footprint library should not require an architectural essay or user interruption, while an unfamiliar, security-sensitive, heavyweight, or operationally significant dependency deserves deeper review.
- State that short local code is not automatically cheaper, a one-line package call is not automatically better, and single use is not automatically bloat.
- Prefer focused, official or established packages over obscure or overly broad packages when a dependency is justified.
- Require directly declaring a selected package rather than relying on its incidental transitive presence.
- Preserve coordinated updates to manifests, lockfiles, documentation, build configuration, and verification when applicable.
- Replace the category-wide approval sentence with an impact-based boundary: ask before adopting or replacing a major framework or introducing a dependency that materially changes architecture, code generation, state ownership, persistence, messaging, toolchains, runtimes, deployment, security boundaries, or public contracts. Do not require blanket design approval for an ordinary proportionate library addition.

#### Acceptance Criteria

- Given a well-maintained, project-fitting standards-oriented package that avoids owning subtle parsing, protocol, security, or compatibility behavior, when its meaningful benefits outweigh its footprint, then the guidance can recommend it over a bespoke implementation even if the call site is one line.
- Given built-in path, collection, string, or other straightforward native behavior, when it fully meets the requirement, then the guidance does not justify an external package merely for syntactic convenience.
- Given a package whose broader purpose or surface is incongruent with the project's responsibilities and only an incidental helper is attractive, then the guidance rejects it unless a separately evidenced project need justifies the package. General-purpose validation, parsing, HTTP, CLI, and similar libraries are not disqualified merely because they are not business-domain-specific.
- Given a monolithic UI framework or heavy general-purpose library proposed for a basic CLI or standalone script, when the project has no established direction toward it, then the guidance treats it as disproportionate and requires rejection or explicit architectural discussion.
- Given the same substantial dependency when the repository or user explicitly establishes it as project direction, then the guidance treats that direction as favorable evidence while still evaluating costs and seeking approval for material adoption.
- Given a popular package with poor maintenance, unacceptable licensing, security concerns, or excessive transitive, install, bundle, startup, runtime, or operational cost, then "industry standard" status alone does not justify adoption.
- Given direct use of a transitively present package, then the guidance requires evaluating and declaring it as a direct dependency rather than relying on accidental installation.
- Ordinary, scoped package additions are distinguished from architecture-scale changes and are not subject to blanket design approval solely because dependency metadata changes.
- A routine, low-impact dependency receives proportionate due diligence and concise reasoning rather than a process burden that indirectly restores default dependency aversion.

#### Likely Files or Areas

- `docs/agent/architecture-boundaries.md`, especially `Boundary First` and `Dependencies`

#### Risks

- "Broader purpose fits" can be interpreted subjectively; the guidance should require evidence from the project's responsibilities, constraints, stack, architecture, or stated direction without requiring a business-domain-specific package.
- A small API surface can conceal a large transitive tree, supply-chain exposure, or runtime burden.
- Agents may treat popularity as a substitute for maintenance and security evaluation.
- Agents may speculate about future framework needs instead of relying on repository or user evidence.
- Agents may confuse repository policy permission with separate network, install-command, or environment approval requirements.
- An exhaustive checklist applied mechanically to every small library could recreate dependency aversion through procedural cost.

#### Recommended Execution Skill

Root `AGENTS.md` only

### Epic 3: Align Workflows, Philosophy, and Contract Verification

#### Goal

Make the nearby workflow language and maintainer checks reinforce the balanced dependency policy without duplicating the detailed rubric throughout the kit.

#### Tasks

- Change the "smallest behavior change" example in `.agents/skills/long-task-workflow/SKILL.md` to a focused, complete, project-fitting behavior change and rely on `AGENTS.md` for the selection principle.
- Add a concise README philosophy note: surgical work minimizes unnecessary total complexity, not imports or packages; project-fitting established dependencies are welcome when their benefits justify their footprint; native facilities remain preferable for simple native logic.
- Leave `.agents/skills/repo-change-planner/SKILL.md` and `.agents/skills/commit-report/SKILL.md` unchanged unless implementation review finds a direct contradiction. They already inherit `AGENTS.md`, and repeating the dependency rubric would undermine the kit's simplification goal.
- Extend `scripts/verify_package.py` with stable, focused instruction-contract checks that protect:
  - permission to choose a meaningful project-fitting new dependency;
  - preference for native or standard-library facilities for simple logic;
  - the distinction between importing a declared dependency and adding one;
  - scrutiny or approval for disproportionate or architecture-changing adoption.
- Add a targeted check that the old unqualified default-deny phrases are absent. Use short semantic anchors rather than full-paragraph equality.
- Keep the verifier structural and fast; use the scenario review in the verification plan for interpretive behavior.

#### Acceptance Criteria

- The long-task example cannot reasonably be read as minimizing dependencies, imports, calls, or diff size at the expense of the better project-fitting solution.
- README communicates "avoid bloat, not dependencies" without becoming a second authoritative copy of the detailed evaluation rubric.
- `repo-change-planner` and `commit-report` remain free of duplicated selection policy unless a concrete contradiction is found.
- Given removal of the positive allowance for a meaningful, project-fitting new dependency, when `python scripts/verify_package.py` runs, then it reports a targeted failure.
- Given removal of the native or standard-library safeguard, the declared-dependency import distinction, or the architecture-scale approval boundary, when the verifier runs, then it reports a targeted failure.
- Given restoration of "Do not add dependencies by default" or the local-first prohibition, when the verifier runs, then it reports a targeted failure.
- Existing file, directory, metadata, README-copy, and placeholder checks remain intact.

#### Likely Files or Areas

- `.agents/skills/long-task-workflow/SKILL.md`, `Start` example
- `README.md`, `Origins` or `Notes`
- `scripts/verify_package.py`

#### Risks

- Repeating detailed policy in README or a skill would add context cost and create competing sources of truth.
- Exact prose matching can make the verifier brittle; anchors should be intentionally stable and failure messages should name the missing concept.
- Automated presence checks cannot prove agent interpretation, so the manual scenario matrix remains essential.

#### Recommended Execution Skill

`$long-task-workflow`

## Verification Plan

- Review the final guidance against this decision matrix:
  - Existing declared Astro API: use or import it when it is idiomatic and provides the best scoped solution.
  - New focused package for a short helper or single call: prefer it over bespoke ownership when meaningful cleanliness, correctness, reliability, interoperability, standards, or maintenance benefits outweigh its footprint and its broader purpose fits the project.
  - Existing capability overlap: use a declared dependency when it offers a comparably good solution and the new package has no material advantage; allow the new package when its benefits justify the overlap.
  - Straightforward language or standard-library behavior: implement natively rather than adding a wrapper package with no meaningful benefit.
  - Domain mismatch: reject a game-oriented dependency used only for an incidental helper in a Kubernetes health CLI.
  - Disproportionate weight: reject or escalate a monolithic UI framework or heavy general-purpose library for a lightweight CLI or standalone script with no relevant direction.
  - Evidenced direction: consider the same substantial framework legitimately when the repository or user explicitly establishes that direction, while preserving approval for the material adoption.
  - Unhealthy dependency: reject a popular package when maintenance, security, licensing, compatibility, or transitive and runtime costs are unacceptable.
  - Transitive-only availability: evaluate and declare the package directly before importing it.
  - Permission boundary: allow an ordinary focused package addition under normal implementation authority, while keeping separate install/network permissions and approval for architecture-scale changes.
- Search the operative copied guidance in `AGENTS.md`, `docs/agent/`, `.agents/skills/`, and `README.md` for `smallest`, `new pattern`, `dependency`, `framework`, `import`, `standard library`, `domain`, `transitive`, `heavy`, `approval`, and `existing` to confirm no nearby sentence directly contradicts the revised policy. Exclude working artifacts under `docs/plans/`, which quote the old language for implementation context.
- Specifically confirm that the unqualified phrases "Do not add dependencies by default" and "New dependencies when a small local implementation or existing dependency is enough" no longer remain in `AGENTS.md` or `docs/agent/architecture-boundaries.md`.
- Run `python scripts/verify_package.py` and confirm it passes.
- Run `git diff --check` and confirm no whitespace errors.
- Manually confirm that, apart from checklist notes in this plan, only `AGENTS.md`, the directly relevant architecture/workflow/README guidance, and the verifier changed; no unrelated documentation was reformatted.
- No package-manager lint, typecheck, test, or build commands exist for this instruction-only repository.
- Do not claim that documentation checks prove model behavior; report the scenario review as the manual interpretive verification performed.

## Suggested Handoff Prompt

Use `$long-task-workflow` to implement all three epics in `docs/plans/prefer-framework-native-solutions.md`.

Revise Agentikit so agents choose proportionate, project-fitting solutions instead of minimizing imports, dependencies, API calls, lines, or diff size. Permit and sometimes prefer a focused, established new dependency—even for a single call site or short helper—when it materially improves correctness, reliability, security, interoperability, clarity, standards compliance, or maintenance and its broader purpose and capability fit the project's responsibilities, constraints, and evidenced direction. Prefer language, platform, or standard-library facilities for straightforward native logic; avoid redundant packages when a declared dependency is comparably good; reject purpose-mismatched packages and disproportionate heavy frameworks or libraries; and reserve explicit approval for material architecture, framework, toolchain, runtime, deployment, security-boundary, or public-contract changes rather than ordinary scoped package additions.

Keep `AGENTS.md` authoritative, rewrite the asymmetric dependency policy in `docs/agent/architecture-boundaries.md`, make only concise aligning edits in `.agents/skills/long-task-workflow/SKILL.md` and `README.md`, and add stable contract checks to `scripts/verify_package.py`. Leave the other skills unchanged unless they directly contradict the policy. Validate the result with the full scenario matrix, `python scripts/verify_package.py`, `git diff --check`, and the scoped consistency review in the plan. Report any separate install or network permission constraints without treating them as reasons to reject an otherwise appropriate dependency.
