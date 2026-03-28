# Test Strategy

## Goal

Demonstrate that the system is correct, resilient, and production-minded.

## Test layers

## 1. Unit tests
Focus on:
- domain rules
- state transitions
- idempotency logic
- retry classification
- error mapping

Examples:
- duplicate idempotency key with same payload returns stored result
- duplicate idempotency key with different payload returns conflict
- settlement cannot move from SETTLED back to IN_PROGRESS
- transient exceptions are retryable
- terminal exceptions are sent to DLQ

## 2. Integration tests
Focus on:
- API to database persistence
- outbox to broker publishing
- worker consumption
- retry behavior
- DLQ routing

Examples:
- POST trade persists trade and outbox record
- worker consumes event and updates settlement status
- transient failure causes retry
- repeated transient failure moves message to DLQ

## 3. Contract tests
Focus on:
- API payload shapes
- schema compatibility
- event envelope format

## 4. End-to-end tests
Focus on full scenario:
- submit trade
- process asynchronously
- inspect final state
- verify retries / DLQ where applicable

## 5. Failure-mode tests
Focus on:
- broker unavailable during publish
- worker crash during processing
- malformed message payload
- duplicate message delivery
- out-of-order message delivery

## Key test scenarios

### Idempotency
- same key + same body => same result
- same key + different body => 409
- missing key => reject or handle per design

### Settlement
- valid trade settles successfully
- transient dependency failure retries then succeeds
- terminal error moves to DLQ
- replay from DLQ reprocesses successfully

### Observability
- correlation ID appears in logs
- retry count increments correctly
- failure codes are preserved

## Tooling

Suggested:
- pytest
- httpx test client
- testcontainers or docker-compose-based integration tests
- fixture-based seeded data

## CI gates

Recommended minimum:
- unit tests
- integration tests
- linting
- type checks
- coverage threshold on core domain logic