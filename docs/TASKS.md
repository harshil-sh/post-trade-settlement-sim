# TASKS.md

## Purpose

This file defines the implementation order for the post-trade settlement simulator.

It is optimized for Codex execution:
- small, reviewable slices
- each task has a narrow scope
- each task has explicit acceptance criteria
- each task can usually be completed in one Codex run
- later tasks depend on earlier verified foundations

This project is a senior backend portfolio project. The goal is not maximum feature count. The goal is to demonstrate strong engineering quality, clear architecture, resilience patterns, and production-minded execution.

---

## Execution rules

When working from this file:

1. Complete only the first unchecked task unless explicitly told otherwise.
2. Do not begin a later task if the current task is incomplete.
3. Keep changes minimal and aligned to the task scope.
4. Run relevant tests before marking a task complete.
5. Update docs only if behavior or setup changed.
6. If blocked, leave a clear note under the task instead of silently skipping ahead.

---

## Status markers

- `[ ]` not started
- `[-]` in progress
- `[x]` completed
- `[!]` blocked

---

# Phase 1 — Repo foundation

## Task 1 — Create production-grade backend skeleton
- [ ] Create the backend project structure with clear separation for:
  - API layer
  - application layer
  - domain layer
  - infrastructure layer
  - tests
- [ ] Add placeholder modules/files only where needed to support the first slice
- [ ] Keep the structure simple and extensible

### Acceptance criteria
- backend structure exists and is coherent
- imports are clean and runnable
- no unnecessary scaffolding beyond immediate need

### Notes
- This task is about structure, not feature completeness.

---

## Task 2 — Set up FastAPI application entrypoint
- [ ] Create the FastAPI app entrypoint
- [ ] Add router registration
- [ ] Add a basic `/health` endpoint
- [ ] Ensure the app starts locally

### Acceptance criteria
- application boots without errors
- `GET /health` returns `200 OK`
- local startup command is documented in README if needed

---

## Task 3 — Add environment and config management
- [ ] Introduce centralized settings/config handling
- [ ] Support local environment variables for:
  - app environment
  - database connection
  - redis connection
  - broker connection
- [ ] Keep configuration loading simple and testable

### Acceptance criteria
- application reads config from environment
- config usage is centralized
- no secrets hardcoded in source

---

## Task 4 — Add structured logging and correlation ID support
- [ ] Add structured logging foundation
- [ ] Support correlation ID extraction or generation per request
- [ ] Include correlation ID in request lifecycle logs

### Acceptance criteria
- logs are structured and readable
- each request can be traced with a correlation ID
- no excessive noisy logging

---

# Phase 2 — Persistence foundation

## Task 5 — Add database setup and persistence base
- [ ] Set up PostgreSQL integration
- [ ] Add DB session/connection management
- [ ] Add migration tooling or schema bootstrapping approach
- [ ] Ensure local developer workflow is clear

### Acceptance criteria
- app can connect to PostgreSQL
- schema creation/migration path is defined
- DB wiring is testable and not mixed into route handlers

---

## Task 6 — Create initial persistence models
- [ ] Create persistence models/tables for:
  - trades
  - idempotency records
- [ ] Include timestamps and primary identifiers
- [ ] Keep schema names explicit and interview-friendly

### Acceptance criteria
- trade and idempotency persistence models exist
- schema supports the first submission slice
- migrations/schema creation works locally

---

# Phase 3 — First vertical slice: trade submission

## Task 7 — Add trade submission request/response contracts
- [ ] Define API request schema for trade submission
- [ ] Define response schema for accepted trade submission
- [ ] Define error response contract
- [ ] Validate required business fields

### Acceptance criteria
- request contract is explicit
- invalid payloads return clean validation errors
- response shape is stable and documented in code

---

## Task 8 — Implement domain model for Trade
- [ ] Create core trade domain model/value objects needed for first slice
- [ ] Add core invariants such as:
  - quantity > 0
  - price > 0
  - buyer and seller differ
  - settlement date not before trade date
- [ ] Keep domain logic independent of FastAPI and ORM concerns

### Acceptance criteria
- domain rules are explicit and testable
- trade invariants are not embedded only in route handlers
- code is easy to explain in interview discussion

---

## Task 9 — Implement `POST /api/v1/trades`
- [ ] Add trade submission endpoint
- [ ] Route request through application/service layer
- [ ] Persist trade record
- [ ] Return accepted response with trade identifier and status

### Acceptance criteria
- valid request creates trade successfully
- endpoint is thin and delegates business logic
- API behavior matches docs for implemented scope

---

## Task 10 — Implement idempotency key handling
- [ ] Support `Idempotency-Key` header on trade submission
- [ ] Store request fingerprint/hash
- [ ] Store original response snapshot or equivalent replayable result
- [ ] Return original response for same key + same payload
- [ ] Return conflict for same key + different payload

### Acceptance criteria
- duplicate identical submission does not create a second trade
- mismatched payload with reused key returns conflict
- idempotency logic is deterministic and tested

---

## Task 11 — Add `GET /api/v1/trades/{tradeId}`
- [ ] Implement trade lookup endpoint
- [ ] Return core trade details and current processing status
- [ ] Handle not found with clear error contract

### Acceptance criteria
- existing trade can be retrieved
- unknown trade returns `404`
- response is stable and clear

---

# Phase 4 — Tests for first slice

## Task 12 — Add unit tests for trade validation
- [ ] Add unit tests for domain invariants
- [ ] Cover valid and invalid trade cases
- [ ] Keep tests fast and deterministic

### Acceptance criteria
- core trade rules are covered by unit tests
- failing cases are explicit and readable

---

## Task 13 — Add unit tests for idempotency logic
- [ ] Test same key + same payload
- [ ] Test same key + different payload
- [ ] Test first-time submission flow

### Acceptance criteria
- idempotency behavior is covered by focused tests
- tests are not coupled to HTTP layer unnecessarily

---

## Task 14 — Add integration test for successful trade submission
- [ ] Add integration test covering:
  - API request
  - DB persistence
  - successful response
- [ ] Use realistic local test setup

### Acceptance criteria
- integration test passes locally
- first vertical slice is proven end-to-end

---

# Phase 5 — Messaging foundation

## Task 15 — Add broker wiring and local infrastructure support
- [ ] Add RabbitMQ connection/config foundation
- [ ] Add local infrastructure configuration for broker
- [ ] Keep implementation minimal until outbox is in place

### Acceptance criteria
- broker can be reached in local dev setup
- no business messaging logic is prematurely scattered

---

## Task 16 — Create outbox persistence model
- [ ] Add outbox table/model
- [ ] Define event record shape
- [ ] Include status/dispatch metadata needed for reliable publishing

### Acceptance criteria
- outbox can persist pending domain events
- schema is simple and reliable

---

## Task 17 — Persist `TradeAccepted` outbox event during submission
- [ ] Update trade submission flow to save outbox event in same unit of work
- [ ] Keep DB write semantics consistent
- [ ] Do not publish directly from route handler

### Acceptance criteria
- trade + outbox record are created together
- no broker publish required yet to complete task

---

## Task 18 — Build outbox publisher process
- [ ] Add process/service that reads pending outbox events
- [ ] Publish to broker
- [ ] Mark outbox records as dispatched on success
- [ ] Preserve correlation metadata

### Acceptance criteria
- pending outbox events are published successfully
- outbox records reflect dispatch state
- failure behavior is safe and observable

---

# Phase 6 — Settlement worker

## Task 19 — Create message envelope standard
- [ ] Define message envelope with:
  - message ID
  - message type
  - correlation ID
  - causation ID if used
  - retry count
  - payload
- [ ] Apply consistently to published events

### Acceptance criteria
- envelope is explicit and reusable
- logs and consumers can trace message lineage

---

## Task 20 — Build settlement worker skeleton
- [ ] Create worker application/process
- [ ] Subscribe to the trade accepted queue/topic
- [ ] Add message handling boundary
- [ ] Add basic logging and failure capture

### Acceptance criteria
- worker starts locally
- worker receives and parses messages
- worker structure is ready for settlement logic

---

## Task 21 — Implement settlement workflow state transitions
- [ ] Add settlement-related status model/state machine
- [ ] Implement initial transition flow for:
  - pending
  - in progress
  - settled
  - failed
- [ ] Guard invalid transitions

### Acceptance criteria
- settlement transitions are explicit
- invalid transitions are rejected safely
- logic is testable outside transport layer

---

## Task 22 — Record settlement attempts
- [ ] Add settlement attempt persistence model
- [ ] Record each worker processing attempt
- [ ] Include timestamps and outcome status

### Acceptance criteria
- each processing attempt is auditable
- success/failure is visible historically

---

# Phase 7 — Retry and DLQ

## Task 23 — Implement transient vs terminal failure classification
- [ ] Introduce exception/failure classification
- [ ] Distinguish retryable vs non-retryable failures
- [ ] Keep rules explicit and easy to review

### Acceptance criteria
- classification logic exists in one clear place
- worker behavior can branch correctly on failure type

---

## Task 24 — Implement retry policy
- [ ] Add bounded retry handling
- [ ] Increment retry count metadata
- [ ] Apply configurable backoff policy
- [ ] Preserve correlation/message IDs across retries

### Acceptance criteria
- retryable failures are retried deterministically
- retries are bounded
- retry metadata is observable

---

## Task 25 — Add DLQ routing
- [ ] Route terminal failures to dead-letter queue
- [ ] Route exhausted retries to dead-letter queue
- [ ] Preserve original payload and failure reason

### Acceptance criteria
- poison/unrecoverable messages do not loop forever
- DLQ records are diagnosable

---

## Task 26 — Persist DLQ diagnostics
- [ ] Store DLQ failure diagnostics for later inspection
- [ ] Capture:
  - message ID
  - trade ID if available
  - retry count
  - failure reason
  - timestamps
- [ ] Keep structure operator-friendly

### Acceptance criteria
- DLQ diagnostics are queryable
- failures can be reviewed without reading raw logs only

---

# Phase 8 — Replay and supportability

## Task 27 — Implement DLQ replay path
- [ ] Add admin replay endpoint or support command
- [ ] Requeue dead-lettered messages intentionally
- [ ] Preserve auditability of replay action

### Acceptance criteria
- replay is explicit, not automatic
- replay activity is recorded
- successful replay path can be demonstrated

---

## Task 28 — Add audit trail for key lifecycle events
- [ ] Record important state changes and support actions
- [ ] Include:
  - trade created
  - settlement started
  - settlement completed
  - settlement failed
  - DLQ routed
  - replay requested
- [ ] Keep records simple and consistent

### Acceptance criteria
- key lifecycle events are auditable
- timeline reconstruction is possible

---

# Phase 9 — Observability and operations

## Task 29 — Add health/readiness checks
- [ ] Expand health checks for:
  - API
  - database
  - broker
- [ ] Separate shallow health from deeper readiness if useful

### Acceptance criteria
- local operators can quickly see system status
- checks are useful and not misleading

---

## Task 30 — Add operational metrics/logging improvements
- [ ] Add metrics or counters for:
  - submitted trades
  - retries
  - settlements completed
  - settlements failed
  - DLQ routed
- [ ] Improve logs where needed for traceability

### Acceptance criteria
- major operational flows are observable
- logs/metrics support demo and interview discussion

---

# Phase 10 — Testing for async and resilience

## Task 31 — Add unit tests for settlement state transitions
- [ ] Cover valid transitions
- [ ] Cover invalid transitions
- [ ] Cover duplicate processing protection where relevant

### Acceptance criteria
- settlement transition logic is well covered

---

## Task 32 — Add integration test for outbox publishing
- [ ] Verify trade submission creates pending outbox event
- [ ] Verify publisher dispatches event successfully

### Acceptance criteria
- outbox flow is proven in integration tests

---

## Task 33 — Add integration test for worker success path
- [ ] Verify published trade event is consumed
- [ ] Verify settlement reaches successful final state

### Acceptance criteria
- happy-path async flow works end-to-end

---

## Task 34 — Add integration test for retry path
- [ ] Simulate transient worker failure
- [ ] Verify retry count increments
- [ ] Verify eventual success or bounded behavior

### Acceptance criteria
- retry flow is deterministic and proven

---

## Task 35 — Add integration test for DLQ path
- [ ] Simulate terminal or exhausted failure
- [ ] Verify message lands in DLQ
- [ ] Verify trade state reflects failure/manual review

### Acceptance criteria
- DLQ path is proven end-to-end

---

## Task 36 — Add integration test for replay path
- [ ] Trigger replay for dead-lettered message
- [ ] Verify message is reprocessed
- [ ] Verify final trade state updates correctly

### Acceptance criteria
- replay scenario is demonstrated and testable

---

# Phase 11 — Portfolio polish

## Task 37 — Add Docker Compose for full local stack
- [ ] Finalize local stack for:
  - API
  - worker
  - PostgreSQL
  - Redis if used
  - RabbitMQ
- [ ] Ensure startup flow is repeatable

### Acceptance criteria
- local stack starts reliably
- project is demoable on one machine

---

## Task 38 — Add sample seed/demo scenarios
- [ ] Add sample requests or seeded scenarios for:
  - happy path
  - duplicate idempotent request
  - retry
  - DLQ
  - replay
- [ ] Make demos easy to run

### Acceptance criteria
- recruiter/interviewer demo flow is easy to execute

---

## Task 39 — Add architecture diagrams and final doc alignment
- [ ] Add sequence/flow diagrams where useful
- [ ] Align docs with actual implementation
- [ ] Remove stale assumptions from docs

### Acceptance criteria
- docs reflect reality
- architecture is easy to explain visually

---

## Task 40 — Add CI pipeline
- [ ] Add CI workflow for linting and tests
- [ ] Keep CI focused and reliable
- [ ] Avoid overcomplicating the pipeline

### Acceptance criteria
- repo has automated quality gate
- core checks run consistently

---

## Task 41 — Prepare recruiter-friendly walkthrough
- [ ] Add final README walkthrough
- [ ] Add “what this project demonstrates” section
- [ ] Add “trade-offs and future improvements” section
- [ ] Add concise run/demo instructions

### Acceptance criteria
- repo clearly signals senior engineering value
- a reviewer can understand the project quickly

---

# Current recommended stopping points

Use these as natural checkpoints for Codex sessions:

## Checkpoint A
Complete through Task 14.
This gives a strong first vertical slice:
- API
- persistence
- idempotency
- tests

## Checkpoint B
Complete through Task 18.
This adds:
- outbox
- broker publishing foundation

## Checkpoint C
Complete through Task 26.
This adds:
- worker
- retries
- DLQ

## Checkpoint D
Complete through Task 36.
This adds:
- replay
- resilience scenarios
- full async proof

## Checkpoint E
Complete through Task 41.
This adds:
- portfolio polish
- CI
- recruiter-ready presentation

---

# Notes for Codex

Unless explicitly instructed otherwise:
- work only on the first unchecked task
- do not skip ahead
- do not mix multiple major tasks in one run
- keep commits focused
- keep the repo runnable after each task