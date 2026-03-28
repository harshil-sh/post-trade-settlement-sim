# Domain Model

## Purpose

This document describes the simplified business domain being simulated.

This is not a full financial settlement model. It is a realistic engineering simulation designed to showcase distributed systems and backend architecture skills.

## Core concepts

### Trade
A trade submitted into the platform for settlement processing.

Example fields:
- trade_id
- client_trade_id
- instrument_id
- quantity
- price
- buyer_account
- seller_account
- trade_date
- settlement_date
- currency
- status

### Settlement
The process of completing obligations arising from a trade.

Simplified stages:
- PENDING
- VALIDATED
- MATCHED
- INSTRUCTED
- SETTLED
- FAILED

### Idempotency key
A client-supplied key used to ensure duplicate submissions do not create duplicate trades.

### Settlement attempt
A single processing attempt by the worker.

### Dead-letter message
A message moved aside because it failed processing repeatedly or failed in a non-recoverable way.

## Trade lifecycle

```text
RECEIVED
-> VALIDATED
-> ACCEPTED
-> MATCHED
-> SETTLEMENT_INSTRUCTED
-> SETTLED

Failure paths:
-> REJECTED
-> SETTLEMENT_FAILED
-> DLQ_PENDING_INVESTIGATION