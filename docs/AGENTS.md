# AGENTS.md

## Project purpose

This repository is a senior-level backend portfolio project that simulates a post-trade settlement platform.

The goal is to demonstrate:
- REST API design
- asynchronous messaging
- idempotent write handling
- retry policies
- dead-letter queue handling
- clean architecture
- operational thinking
- strong automated testing
- production-minded documentation

This is a simulation for portfolio purposes, not a real trading or settlement system.

---

## Working style for Codex

When working in this repository, always:

1. Read the existing docs before making major changes.
2. Prefer a thin vertical slice over broad unfinished scaffolding.
3. Keep code modular, explicit, and easy to explain in a senior engineer interview.
4. Avoid overengineering.
5. Update documentation only when implementation actually changes behavior or setup.
6. Preserve consistency with the architecture and domain language already defined in `docs/`.

For non-trivial work:
- summarize the plan first
- then implement
- then run relevant tests
- then summarize what changed, how it was verified, and what remains

---

## Repository priorities

Optimize for:
- correctness
- clarity
- maintainability
- testability
- resilience
- observability

Do not optimize for:
- clever abstractions
- premature generic frameworks
- unnecessary microservices
- finance-domain complexity beyond the agreed simulator scope

---

## Repository structure

Expected structure:

- `README.md` — project overview and setup
- `AGENTS.md` — durable instructions for Codex
- `docs/` — architecture, domain, API, messaging, tasks, runbooks, scenarios
- `src/` or `backend/` — application source code
- `tests/` — automated tests
- `infra/` — docker, local infrastructure, deployment-related files

If the structure differs slightly in implementation, preserve the same separation of concerns:
- API layer
- application layer
- domain layer
- infrastructure layer
- tests

---

## Files to read first

Before changing code, read these if present:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DOMAIN.md`
- `docs/API_SPEC.md`
- `docs/ASYNC_MESSAGING.md`
- `docs/NON_FUNCTIONAL_REQUIREMENTS.md`
- `docs/TEST_STRATEGY.md`
- `docs/TASKS.md`
- `docs/DECISIONS.md`

If a requested change conflicts with these documents:
- follow implementation reality plus the most recent documented intent
- update docs if needed
- explicitly call out the mismatch in the final summary

---

## Domain language

Use consistent terms across code and docs:

- Trade
- Settlement
- SettlementAttempt
- IdempotencyKey / IdempotencyRecord
- OutboxEvent
- DeadLetterMessage / DLQ
- CorrelationId
- RetryPolicy
- TransientFailure
- TerminalFailure

Do not introduce multiple names for the same concept unless there is a strong reason.

---

## Architecture rules

Follow these rules unless the repo already establishes a stronger pattern:

1. Keep route handlers thin.
2. Put business rules in application/domain services, not in FastAPI endpoints.
3. Keep infrastructure concerns out of domain entities.
4. Make state transitions explicit.
5. Keep async workflow boundaries clear.
6. Prefer composition over deep inheritance.
7. Prefer small focused classes/functions over god objects.
8. Keep side effects easy to locate.

Recommended directional dependency flow:

API -> Application -> Domain  
Infrastructure -> supports Application/Domain through interfaces

Domain should not depend on FastAPI, broker SDKs, or ORM-specific details.

---

## API rules

For REST endpoints:

- Use explicit request and response models.
- Validate inputs clearly.
- Return stable error contracts.
- Keep endpoint behavior predictable.
- Use versioned routes such as `/api/v1/...`.

For write endpoints that create or submit trades:

- support idempotency explicitly
- same idempotency key + same request payload must return the original response
- same idempotency key + different payload must return conflict
- document or preserve the response status behavior consistently

Do not hide idempotency behavior inside vague helper logic.

---

## Messaging rules

The async part of this system exists to showcase real backend reliability concerns.

Where messaging is implemented:

- use explicit message envelopes
- include message ID and correlation ID
- preserve retry count metadata
- separate transient vs terminal failures
- keep retry behavior deterministic and testable
- route poison/unrecoverable messages to DLQ
- preserve auditability for replay

Consumers must be safe against:
- duplicate delivery
- out-of-order delivery where relevant
- repeated retries
- already-completed state transitions

---

## Reliability patterns

Prefer these patterns where applicable:

- idempotent command handling
- outbox pattern for reliable event publishing
- consumer deduplication
- retry with bounded attempts
- dead-letter queue on unrecoverable or exhausted failures
- explicit audit trail for important state changes

Do not pretend distributed operations are atomic when they are not.

Make consistency boundaries explicit.

---

## Persistence rules

Database design should support:
- trades
- idempotency records
- settlement attempts
- outbox events
- audit history
- optionally processed message tracking

Persistence rules:
- keep schema names understandable
- use timestamps consistently
- prefer immutable audit/event records where reasonable
- avoid mixing transport DTOs directly with persistence models unless intentionally simple

---

## Logging and observability

Every meaningful backend change should preserve or improve observability.

Use:
- structured logging
- correlation IDs
- message IDs where applicable
- clear failure reason codes where possible

At minimum, logs should make it easy to trace:
- request received
- idempotency decision
- trade persisted
- event published
- message consumed
- retry attempted
- DLQ routed
- replay triggered

Do not add noisy logs that reduce signal.

Do not log secrets.

---

## Testing expectations

Testing is mandatory for meaningful backend changes.

Prefer this test mix:

- unit tests for domain logic and validation
- unit tests for idempotency behavior
- integration tests for API + persistence
- integration tests for messaging, retries, and DLQ once implemented
- end-to-end tests for representative scenarios when practical

When changing behavior:
- add or update tests for that behavior
- keep tests deterministic
- avoid brittle timing-based tests where possible

If a change touches critical flow and no test is added, explain why in the final summary.

---

## Code quality standards

Write code that is:
- explicit
- typed where practical
- cohesive
- easy to review
- easy to extend

Prefer:
- clear names
- small functions
- focused modules
- straightforward control flow
- narrow exception handling

Avoid:
- speculative abstractions
- deeply nested logic
- hidden side effects
- giant files with mixed responsibilities

---

## Dependency rules

Be conservative with new dependencies.

Before adding a new production dependency:
- check whether the standard library or an existing dependency is enough
- prefer widely used, stable libraries
- keep the stack aligned with the architecture docs

Do not add dependencies just to save a small amount of code.

If you add one:
- use it consistently
- update setup docs if needed
- keep the change minimal

---

## Documentation rules

Docs are part of the portfolio quality signal.

Update docs when:
- setup steps change
- architecture meaningfully changes
- API contract changes
- a new operational concept is introduced
- task tracking needs to reflect newly completed work

Do not rewrite all docs unnecessarily.

Keep docs aligned with reality.

---

## Delivery strategy

When asked to implement work, prefer this order:

1. understand current repo state
2. identify the smallest valuable slice
3. implement only that slice
4. add tests
5. verify locally where possible
6. update only necessary docs
7. summarize clearly

For large tasks:
- do not try to complete the entire platform in one pass
- deliver in vertical slices
- leave the repo in a working state

---

## Definition of done

A task is done only when all of the following are true:

1. The requested scope is implemented.
2. The code is consistent with the repository architecture.
3. Relevant tests pass, or the limitation is clearly explained.
4. Docs are updated if behavior or setup changed.
5. No unrelated refactors were mixed in without strong justification.
6. Final summary includes:
   - what changed
   - files created/updated
   - how it was verified
   - remaining next steps

---

## What not to do

Do not:
- build frontend code unless explicitly requested
- introduce authentication unless explicitly requested
- add cloud-specific infrastructure unless explicitly requested
- widen project scope beyond the current slice
- replace working patterns with large framework rewrites
- silently change documented API behavior
- mark tasks complete unless they are truly complete

---

## Preferred implementation order for this repo

Default development order should be:

1. project skeleton
2. health endpoint
3. trade submission endpoint
4. idempotency support
5. persistence
6. outbox pattern
7. event publishing
8. worker consumer
9. retry policy
10. dead-letter queue
11. replay flow
12. observability hardening
13. broader integration and scenario testing

Unless the user explicitly asks otherwise, stay on the earliest unfinished slice.

---

## If uncertain

If repo intent is unclear:
- inspect docs and current code first
- choose the smallest safe interpretation
- make minimal, reversible changes
- note assumptions in the final summary

Do not invent hidden requirements.

---

## Final response format

At the end of each task, provide:

1. Plan
2. Changes made
3. Files updated
4. Verification performed
5. Next recommended step

Keep the final summary concise but concrete.