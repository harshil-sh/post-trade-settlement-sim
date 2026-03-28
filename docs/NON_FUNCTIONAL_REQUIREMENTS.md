# Non-Functional Requirements

## Purpose

Define the quality attributes expected from the system.

## Reliability

- API writes must support safe client retries
- async processing must tolerate transient failures
- poison messages must not block healthy message processing
- all failures must be diagnosable

## Availability

For portfolio MVP:
- local environment should remain easy to recover
- services should restart cleanly
- transient dependency failures should be handled gracefully

## Performance

Portfolio targets only, not production SLAs.

Initial targets:
- submit trade API responds under 300 ms in normal local conditions
- background worker handles small bursts without message loss
- status lookup under 200 ms in local environment

## Scalability

System should be structured so that:
- API layer can scale independently
- workers can scale horizontally
- broker decouples ingress from processing

## Consistency

- API layer uses strong consistency for trade and idempotency records
- async settlement is eventually consistent
- trade status endpoints must clearly reflect current known state

## Auditability

The system must record:
- who/what submitted a trade
- when it was accepted
- each settlement attempt
- each retry
- DLQ entry and replay actions

## Security

For MVP:
- basic secure defaults
- secrets not stored in source control
- input validation on all external payloads
- admin endpoints clearly separated

## Observability

Must support:
- structured logging
- correlation IDs
- basic metrics
- health checks
- clear failure diagnostics

## Maintainability

- clean architecture boundaries
- explicit domain language
- small, testable components
- documentation kept close to implementation

## Testability

- deterministic unit tests
- integration tests with real infrastructure where reasonable
- repeatable local setup
- seeded sample scenarios

## Portability

- local environment should run via Docker Compose
- no hard dependency on cloud-specific services in MVP