# Architecture

## Overview

The system simulates post-trade settlement using a combination of synchronous REST APIs and asynchronous messaging.

The design intentionally separates command handling from background processing to reflect real enterprise settlement systems.

## High-level components

1. **API Service**
   - accepts client requests
   - validates payloads
   - enforces idempotency
   - persists trade and command records
   - publishes domain events

2. **Message Broker**
   - transports domain events and commands
   - supports retry routing
   - supports dead-lettering

3. **Settlement Worker**
   - consumes events
   - performs settlement steps
   - updates trade state
   - emits follow-up events
   - applies retry policy on transient failures

4. **Persistence Layer**
   - stores trades, settlement attempts, idempotency keys, outbox records, audit records

5. **Observability Layer**
   - structured logs
   - correlation IDs
   - message IDs
   - metrics and tracing hooks

## Architectural style

- Clean Architecture
- Domain-driven design principles
- Event-driven workflow
- Outbox pattern for reliable event publishing
- Idempotent command handling

## Core design principles

- API operations must be safe to retry
- Messaging must tolerate transient failures
- Processing must be observable and auditable
- Domain state transitions must be explicit
- Failures must be classifiable as transient or terminal
- Poison messages must not block the system

## Conceptual flow

```text
Client
  -> REST API
      -> Validate Request
      -> Check Idempotency
      -> Persist Trade + Outbox Event
      -> Return 202/201

Outbox Publisher
  -> Message Broker

Settlement Worker
  -> Consume Event
  -> Process Settlement
  -> Success: update status + publish next event
  -> Transient Failure: retry
  -> Terminal Failure: route to DLQ