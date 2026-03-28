# TASKS

## Phase 1 - Foundations

- [ ] Task 1: Create repository structure for `src`, `tests`, `docs`, and `infra`
- [ ] Task 2: Set up FastAPI application skeleton with health endpoint
- [ ] Task 3: Add project configuration management for environment variables
- [ ] Task 4: Set up PostgreSQL connection and migration tooling
- [ ] Task 5: Create initial Docker Compose for API, worker, PostgreSQL, Redis, and broker
- [ ] Task 6: Add structured logging with correlation ID support
- [ ] Task 7: Create base domain models for Trade, SettlementAttempt, and IdempotencyRecord

## Phase 2 - Trade submission API

- [ ] Task 8: Implement `POST /api/v1/trades`
- [ ] Task 9: Add request validation and error contract
- [ ] Task 10: Implement idempotency key storage and request fingerprinting
- [ ] Task 11: Return stored response for duplicate idempotent submissions
- [ ] Task 12: Reject same idempotency key with different payload
- [ ] Task 13: Implement `GET /api/v1/trades/{tradeId}`
- [ ] Task 14: Implement `GET /api/v1/trades/{tradeId}/settlement`

## Phase 3 - Reliable messaging

- [ ] Task 15: Add outbox table and domain event persistence
- [ ] Task 16: Build outbox publisher process
- [ ] Task 17: Publish `TradeAccepted` messages to broker
- [ ] Task 18: Define message envelope with correlation metadata
- [ ] Task 19: Create processed-message deduplication strategy for consumers

## Phase 4 - Settlement worker

- [ ] Task 20: Build settlement worker consumer
- [ ] Task 21: Implement settlement workflow state transitions
- [ ] Task 22: Record settlement attempts
- [ ] Task 23: Implement transient vs terminal failure classification
- [ ] Task 24: Add retry policy with capped retries and backoff
- [ ] Task 25: Route exhausted/terminal failures to dead-letter queue
- [ ] Task 26: Persist DLQ diagnostics and failure reason

## Phase 5 - Operations and replay

- [ ] Task 27: Implement admin endpoint or command for DLQ replay
- [ ] Task 28: Add audit trail for replay activity
- [ ] Task 29: Add health checks for API, database, and broker dependencies
- [ ] Task 30: Add metrics/logging for retries, failures, and settlements

## Phase 6 - Testing

- [ ] Task 31: Add unit tests for trade validation rules
- [ ] Task 32: Add unit tests for idempotency logic
- [ ] Task 33: Add unit tests for settlement state transitions
- [ ] Task 34: Add integration test for trade submission flow
- [ ] Task 35: Add integration test for outbox publish flow
- [ ] Task 36: Add integration test for worker success path
- [ ] Task 37: Add integration test for retry path
- [ ] Task 38: Add integration test for DLQ path
- [ ] Task 39: Add end-to-end test for replay scenario

## Phase 7 - Portfolio polish

- [ ] Task 40: Add sequence diagrams to architecture docs
- [ ] Task 41: Add sample payloads and demo scenarios
- [ ] Task 42: Add interview notes explaining design trade-offs
- [ ] Task 43: Add README walkthrough with local setup and demo steps
- [ ] Task 44: Add CI pipeline for tests and linting
- [ ] Task 45: Record short demo script for recruiters/hiring managers