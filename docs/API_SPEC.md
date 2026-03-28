# API Specification

## Design goals

- resource-oriented REST design
- idempotent write semantics for client retries
- explicit correlation and traceability
- clear error contracts

## Headers

### Required / supported headers

- `Content-Type: application/json`
- `Idempotency-Key: <unique-key>` for POST endpoints
- `X-Correlation-Id: <optional-client-correlation-id>`

## Endpoints

## 1. Submit trade

`POST /api/v1/trades`

Creates a trade submission and starts async settlement workflow.

### Request
```json
{
  "clientTradeId": "CT-10001",
  "instrumentId": "IBM",
  "quantity": 100,
  "price": 125.50,
  "currency": "USD",
  "buyerAccount": "ACC-BUY-001",
  "sellerAccount": "ACC-SELL-001",
  "tradeDate": "2026-03-28",
  "settlementDate": "2026-03-30"
}