# Interview Notes

## Elevator pitch

This project simulates a post-trade settlement platform using REST and asynchronous messaging. I built it specifically to demonstrate senior-level backend engineering concerns such as idempotency, reliable event publishing, retries, dead-letter queues, observability, and failure recovery.

## Why this project stands out

Most portfolio projects stop at CRUD and basic APIs.

This one demonstrates:
- distributed systems thinking
- enterprise integration patterns
- reliability engineering
- operational diagnostics
- realistic failure handling

## Key design decisions to talk through

### Idempotency
Clients often retry due to network uncertainty. I implemented idempotent submission so the API is safe to retry without creating duplicate trades.

### Outbox pattern
I used an outbox approach to avoid database/broker inconsistency when persisting trades and publishing events.

### Retry and DLQ
I separated transient and terminal failures so the worker can retry only what is likely recoverable and route poison messages to DLQ for support workflows.

### Eventual consistency
I intentionally modeled settlement as asynchronous to reflect real systems where command acceptance and business completion are separate steps.

## Senior engineering signals

- architecture documentation before coding
- failure-mode-driven design
- explicit trade-offs captured as ADRs
- operational runbook and replay workflow
- test strategy beyond unit tests

## Trade-offs

### Why not make everything synchronous?
Because settlement is naturally workflow-driven, failure-prone, and operationally better decoupled from client request/response latency.

### Why simplify the finance domain?
The goal is to focus on engineering depth, not to recreate the full complexity of real clearing systems in an MVP.

### Why Python/FastAPI?
Fast iteration speed, strong testability, and clear API modeling for a portfolio project.

## What to improve next
- authentication and authorization
- event versioning
- reconciliation service
- load testing
- chaos testing
- dashboard for failed trades and DLQ replay