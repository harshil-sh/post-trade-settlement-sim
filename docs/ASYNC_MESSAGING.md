
# Async Messaging Design

## Goal

Model a realistic asynchronous workflow with:
- durable event publishing
- retries
- DLQ handling
- replay support
- correlation across services

## Message broker role

The broker decouples:
- API submission
- background settlement processing

This allows:
- resilience
- scalability
- workload smoothing
- failure isolation

## Candidate queues / topics

### Main queue
- `trade.accepted`

### Retry queue
- `trade.accepted.retry`

### Dead-letter queue
- `trade.accepted.dlq`

### Optional support queues
- `settlement.completed`
- `settlement.failed`
- `audit.events`

## Message envelope

Each message should include metadata separate from payload.

### Envelope example
```json
{
  "messageId": "msg_001",
  "messageType": "TradeAccepted",
  "occurredAt": "2026-03-28T10:15:31Z",
  "correlationId": "corr_001",
  "causationId": "cmd_001",
  "retryCount": 0,
  "payload": {
    "tradeId": "trd_8cdb8d5e",
    "clientTradeId": "CT-10001"
  }
}