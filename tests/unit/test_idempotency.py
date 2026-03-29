from sqlalchemy.orm import Session

from app.api.schemas import TradeCreateRequest
from app.application.trade_service import TradeService


def _payload(price: str = "125.50") -> TradeCreateRequest:
    return TradeCreateRequest(
        clientTradeId="CT-10001",
        instrumentId="IBM",
        quantity=100,
        price=price,
        currency="USD",
        buyerAccount="ACC-BUY-001",
        sellerAccount="ACC-SELL-001",
        tradeDate="2026-03-28",
        settlementDate="2026-03-30",
    )


def test_same_key_same_payload_returns_original_response(db_session: Session) -> None:
    service = TradeService(db_session)
    first = service.submit_trade(_payload(), "key-1", "corr-1")
    second = service.submit_trade(_payload(), "key-1", "corr-2")
    assert first.trade_id == second.trade_id


def test_same_key_different_payload_raises_conflict(db_session: Session) -> None:
    service = TradeService(db_session)
    service.submit_trade(_payload(), "key-2", "corr-1")

    try:
        service.submit_trade(_payload(price="126.00"), "key-2", "corr-2")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "different payload" in str(exc)
