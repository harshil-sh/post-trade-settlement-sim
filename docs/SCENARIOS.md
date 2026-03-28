# Demo Scenarios

## Scenario 1: Happy path

### Goal
Show standard trade submission and successful settlement.

### Steps
1. Submit valid trade
2. Receive accepted response
3. Show broker event
4. Show worker processing
5. Fetch trade status
6. Show `SETTLED`

## Scenario 2: Duplicate submission handled safely

### Goal
Show idempotent API behavior.

### Steps
1. Submit trade with `Idempotency-Key`
2. Retry exact same request with same key
3. Show same response returned
4. Show only one trade created

## Scenario 3: Conflict on reused key with changed payload

### Goal
Show protection against accidental misuse of idempotency key.

### Steps
1. Submit trade with key
2. Resubmit with same key but different payload
3. Show `409 Conflict`

## Scenario 4: Transient failure with retry

### Goal
Show resilience.

### Steps
1. Inject simulated timeout in worker
2. Show retry count increasing
3. Show eventual success after retry
4. Show final `SETTLED`

## Scenario 5: DLQ path

### Goal
Show poison message handling.

### Steps
1. Inject terminal failure
2. Show retries skipped or exhausted
3. Show message moved to DLQ
4. Show trade marked for review

## Scenario 6: Replay from DLQ

### Goal
Show supportability and recovery workflow.

### Steps
1. Fix cause of failure
2. Replay DLQ message
3. Show settlement completes successfully