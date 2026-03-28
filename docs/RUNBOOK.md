# Runbook

## Purpose

Operational guide for local development and demo support.

## Common startup flow

1. Start infrastructure services
2. Start API service
3. Start worker service
4. Verify health endpoints
5. Submit sample trade
6. Inspect logs and final status

## Basic checks

### API health
- call health endpoint
- verify DB connectivity if included in readiness check

### Broker health
- verify queue exists
- verify publisher and consumer can connect

### Worker health
- verify consumer loop active
- verify logs show subscription to main queue

## Common incidents

## Incident: duplicate trade submissions
### Symptoms
- multiple client retries
- concern around duplicate trades

### Expected system behavior
- same idempotency key and same request returns original result
- same key with changed payload returns conflict

## Incident: transient settlement failure
### Symptoms
- timeout in worker
- settlement not completed immediately

### Expected behavior
- retry according to policy
- logs show retry count
- trade remains non-terminal until retry limit reached

## Incident: message in DLQ
### Symptoms
- trade stuck in failed/manual review state
- DLQ contains message

### Operator action
- inspect failure reason
- fix root cause if appropriate
- replay message manually for demo/support use

## Incident: outbox backlog
### Symptoms
- trades persist but events not reaching broker

### Checks
- outbox publisher running
- DB outbox rows pending
- broker connectivity healthy

## Demo guidance

For portfolio demos, prepare three scenarios:
1. happy path settlement
2. transient failure with successful retry
3. terminal failure sent to DLQ and replayed