# Architecture Boundaries

Read this before changing module boundaries, public APIs, database schemas, service layers, dependencies, auth, logging, error handling, or cross-cutting infrastructure.

## Boundary First

Before editing architecture-level code, identify:
- The layer or module that owns the behavior.
- The public contract that callers rely on.
- The nearest existing pattern for similar behavior.
- The smallest boundary that can contain the change.
- The verification that proves callers still work.

Do not move behavior across layers just because the current location feels imperfect. If ownership is unclear, name the ambiguity and recommend a path.

## Public Contracts

Treat these as public contracts unless the repository shows otherwise:
- Exported functions, classes, hooks, components, commands, endpoints, schemas, events, messages, and migration formats.
- Database tables, columns, indexes, constraints, and serialized data.
- CLI flags, environment variables, config keys, URLs, status codes, and error shapes.

Before changing a public contract:
- Search for every caller or consumer.
- Check tests, generated clients, docs, examples, and CI usage.
- State whether the change is backward compatible.
- Add migration, adapter, or compatibility handling only when a real caller needs it.

## Layer Discipline

Keep responsibilities separated:
- UI should render state and collect user intent. It should not own business rules that belong in services or domain code.
- Domain or service code should own business decisions. It should not depend on UI details.
- Data access code should isolate persistence details. It should not leak query mechanics into unrelated layers.
- Infrastructure code should wrap external systems behind clear interfaces.
- Tests should verify behavior at the right layer instead of mocking through every layer by default.

If the repository intentionally uses a different pattern, follow the repository.

## Dependencies

Do not add or reject a dependency reflexively. Compare the total lifecycle value and cost of the local and package options, and scale the depth of the evaluation to the dependency's risk and impact. A routine, well-known, low-footprint library should not require an architecture essay or user interruption; an unfamiliar, security-sensitive, heavyweight, or operationally significant dependency deserves deeper review.

First check whether the language, platform, standard library, or a declared project dependency already solves the problem cleanly. When a declared dependency offers a comparably clear, reliable, and maintainable solution, prefer it over an overlapping package. A package present only transitively is not a declared project dependency; evaluate and declare it directly before importing it.

A focused, established dependency may be better than bespoke code—even for a single call site or short helper—when meaningful correctness, reliability, security, standards compliance, interoperability, clarity, testability, or maintenance benefits and avoided ownership outweigh its footprint. Short local code is not automatically cheaper, a one-line package call is not automatically better, and single use is not automatically bloat.

Before adding one, consider:
- Capability: whether each option handles the behavior and edge cases correctly.
- Fit: whether the capability is relevant and proportionate, the dependency's broader purpose fits the project's responsibilities and constraints, and the choice aligns with the current stack, established architecture, and evidenced direction. General-purpose ecosystem libraries may fit without being specific to the application's business domain.
- Health: maintenance, API stability, license, security posture, supply-chain exposure, and platform compatibility.
- Footprint: direct and transitive dependencies, install or bundle size, startup and runtime cost, build impact, and operational burden.

Prefer focused, official or established libraries over obscure or overly broad packages when a dependency is justified. Reject packages whose broader purpose or surface is incongruent with the project when only an incidental helper is attractive. Update manifests, lockfiles, docs, build config, and verification together when applicable.

Ask before adopting or replacing a major framework or introducing a dependency that materially changes architecture, code generation, state ownership, persistence, messaging, toolchains, runtimes, deployment, security boundaries, or public contracts. An ordinary, proportionate library addition does not require separate design approval solely because it changes a manifest or lockfile; environment, network, and tool-execution permissions still apply.

## Data and Migrations

Database and persistence changes are high risk.

Before editing schemas or migrations:
- Inspect existing migration style and naming.
- Check whether migrations are forward-only, reversible, or environment-specific.
- Preserve existing data unless the user explicitly asks to delete or rewrite it.
- Plan rollout, backfill, and rollback when applicable.
- Verify both schema shape and application behavior.

Never silently change persisted formats, enum values, external IDs, timestamps, or units.

## Auth, Security, and Privacy

Security can justify necessary complexity.

Before changing auth, permissions, secrets, encryption, input validation, or data exposure:
- Identify the trust boundary.
- Identify who can call the path and what data they can reach.
- Preserve deny-by-default behavior when present.
- Avoid logging secrets, tokens, private user data, credentials, or full request bodies.
- Prefer centralized validation and authorization over scattered checks.
- Run or add focused tests for allowed and denied cases.

Do not weaken security for simpler code.

## Errors and Logging

Follow existing error and logging conventions.

Good errors:
- Tell the caller what failed.
- Preserve enough context for debugging.
- Avoid exposing secrets or internal-only details to users.
- Use existing error types, status codes, and response shapes.

Good logs:
- Help diagnose production failures.
- Include stable identifiers when safe.
- Avoid noisy success logs.
- Avoid sensitive data.

## API and Endpoint Checklist

Before editing an endpoint, command, event handler, or message consumer:
- Confirm request and response shape.
- Confirm validation behavior.
- Confirm auth and permission checks.
- Confirm idempotency requirements.
- Confirm retry behavior and duplicate handling.
- Confirm error shape and status code.
- Confirm tests cover success and failure paths.

## UI Boundary Checklist

Before editing UI structure or state:
- Check existing component boundaries and naming.
- Keep rendering, state derivation, and side effects separated where the repo already does so.
- Preserve accessibility behavior, loading states, empty states, and error states.
- Avoid broad restyling unless requested.
- Verify the user-visible path manually or with the narrowest useful test.

## Architecture Decision Trigger

If an architecture change creates a durable decision, use `docs/agent/adr-template.md` for ADR criteria and format.
