# Post-Trade Settlement Simulator

A production-style portfolio project that simulates a post-trade settlement platform using REST APIs and asynchronous messaging.

This project is designed to demonstrate senior-level backend engineering skills through:

- idempotent REST endpoints
- asynchronous event-driven workflows
- retry policies and dead-letter queues
- failure handling and recovery design
- clean architecture and domain-driven design
- observability, resilience, and testability
- realistic trade lifecycle and settlement scenarios

## Why this project

Many portfolio projects show CRUD. Fewer show real-world distributed systems concerns.

This project focuses on the kind of engineering problems seen in capital markets, clearing, settlement, and high-reliability enterprise systems:

- duplicate request protection
- eventual consistency
- out-of-order events
- poison messages
- retry backoff
- settlement state transitions
- reconciliation and auditability

## Portfolio value

This project is intended to position me as a Senior/Lead backend engineer by showing:

- strong API design
- system design thinking
- resilient async processing
- operational awareness
- realistic failure-mode handling
- production-ready documentation and testing strategy

## Core capabilities

- Submit trades through REST
- Validate and persist trades
- Publish domain events to a message broker
- Process settlement asynchronously
- Support retries for transient failures
- Route poison/unrecoverable messages to a dead-letter queue
- Expose status and reconciliation endpoints
- Guarantee idempotent API behavior for safe retries by clients
- Provide structured logs, metrics, and tracing hooks

## Example lifecycle

1. Client submits a trade with an idempotency key
2. API validates request and stores trade
3. System publishes `TradeAccepted`
4. Settlement worker consumes event
5. Worker performs enrichment / matching / settlement simulation
6. On success, trade reaches `SETTLED`
7. On transient failure, message is retried
8. On repeated failure, message lands in DLQ for investigation

## Proposed tech stack

The exact stack may evolve, but the current target is:

- Backend API: Python + FastAPI
- Async messaging: RabbitMQ or Azure Service Bus simulation layer
- Persistence: PostgreSQL
- Cache / idempotency support: Redis
- Background workers: Python worker service
- Containerization: Docker Compose
- Observability: OpenTelemetry-ready logging and metrics
- Tests: pytest + integration and contract tests

## Repository structure

```text
.
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DOMAIN.md
│   ├── API_SPEC.md
│   ├── ASYNC_MESSAGING.md
│   ├── NON_FUNCTIONAL_REQUIREMENTS.md
│   ├── TEST_STRATEGY.md
│   ├── TASKS.md
│   ├── DECISIONS.md
│   ├── RUNBOOK.md
│   ├── SCENARIOS.md
│   └── INTERVIEW_NOTES.md
├── src/
├── tests/
└── infra/
## Current implementation status (Slice 1)

Implemented in this slice:
- FastAPI app skeleton using clean layering (`api`, `application`, `domain`, `infrastructure`)
- `GET /health`
- `POST /api/v1/trades` with request validation
- idempotency behavior using `Idempotency-Key`
  - same key + same payload returns original response
  - same key + different payload returns `409`
- PostgreSQL-ready persistence for `trades` and `idempotency_records`
- JSON structured logging with correlation ID middleware
- unit tests for validation + idempotency logic
- one integration test for successful trade submission

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Run tests

```bash
pytest
```
