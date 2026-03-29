def test_submit_trade_success(client) -> None:
    response = client.post(
        "/api/v1/trades",
        headers={"Idempotency-Key": "integration-key-1", "X-Correlation-Id": "corr-int-1"},
        json={
            "clientTradeId": "CT-10001",
            "instrumentId": "IBM",
            "quantity": 100,
            "price": "125.50",
            "currency": "USD",
            "buyerAccount": "ACC-BUY-001",
            "sellerAccount": "ACC-SELL-001",
            "tradeDate": "2026-03-28",
            "settlementDate": "2026-03-30",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["clientTradeId"] == "CT-10001"
    assert body["status"] == "ACCEPTED"
    assert response.headers["x-correlation-id"] == "corr-int-1"
