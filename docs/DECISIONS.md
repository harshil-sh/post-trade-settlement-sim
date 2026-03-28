# Architecture Decision Log

## ADR-001: Use REST + asynchronous messaging
**Status:** Accepted

### Context
Trade submission is synchronous from the client perspective, but settlement processing is naturally asynchronous and failure-prone.

### Decision
Use REST for command submission and asynchronous messaging for background settlement workflow.

### Consequences
- improves realism
- allows retry and DLQ modeling
- introduces eventual consistency complexity

---

## ADR-002: Enforce idempotency on trade submission
**Status:** Accepted

### Context
Clients may retry requests due to timeouts or network issues.

### Decision
Require/support `Idempotency-Key` on trade submission endpoints.

### Consequences
- safer client integration
- prevents duplicate trades
- requires request fingerprint storage

---

## ADR-003: Use outbox pattern for reliable event publishing
**Status:** Accepted

### Context
Writing to DB and publishing to broker in separate non-atomic steps risks inconsistency.

### Decision
Persist domain events in an outbox table and publish asynchronously.

### Consequences
- stronger delivery reliability
- slightly more implementation complexity

---

## ADR-004: Separate transient and terminal failures
**Status:** Accepted

### Context
Not every processing failure should be retried.

### Decision
Introduce explicit failure classification and DLQ routing.

### Consequences
- better operational behavior
- requires careful exception taxonomy

---

## ADR-005: Keep financial domain simplified
**Status:** Accepted

### Context
This is a portfolio simulator, not a production clearing system.

### Decision
Use a simplified trade and settlement model focused on engineering concerns.

### Consequences
- keeps MVP achievable
- still demonstrates senior design ability