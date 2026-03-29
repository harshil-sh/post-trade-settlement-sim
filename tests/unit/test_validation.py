import pytest
from pydantic import ValidationError

from app.api.schemas import TradeCreateRequest


def test_validation_rejects_negative_quantity() -> None:
    with pytest.raises(ValidationError):
        TradeCreateRequest(
            clientTradeId="CT-1",
            instrumentId="IBM",
            quantity=-1,
            price="125.50",
            currency="usd",
            buyerAccount="BUY-1",
            sellerAccount="SELL-1",
            tradeDate="2026-03-28",
            settlementDate="2026-03-30",
        )


def test_validation_rejects_settlement_before_trade() -> None:
    with pytest.raises(ValidationError):
        TradeCreateRequest(
            clientTradeId="CT-1",
            instrumentId="IBM",
            quantity=10,
            price="125.50",
            currency="USD",
            buyerAccount="BUY-1",
            sellerAccount="SELL-1",
            tradeDate="2026-03-30",
            settlementDate="2026-03-28",
        )
