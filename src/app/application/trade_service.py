import hashlib
import json
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.api.schemas import TradeCreateRequest, TradeResponse
from app.domain.models import IdempotencyRecord, Trade


@dataclass
class SubmissionResult:
    response: TradeResponse


class TradeService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def submit_trade(self, payload: TradeCreateRequest, idempotency_key: str, correlation_id: str) -> TradeResponse:
        payload_dict = payload.model_dump(by_alias=True, mode="json")
        payload_hash = hashlib.sha256(json.dumps(payload_dict, sort_keys=True).encode("utf-8")).hexdigest()

        existing = (
            self.db.query(IdempotencyRecord)
            .filter(IdempotencyRecord.idempotency_key == idempotency_key)
            .one_or_none()
        )

        if existing:
            if existing.payload_hash != payload_hash:
                raise ValueError("Idempotency key already used with a different payload")
            return TradeResponse.model_validate_json(existing.response_body)

        trade = Trade(
            client_trade_id=payload.client_trade_id,
            instrument_id=payload.instrument_id,
            quantity=payload.quantity,
            price=payload.price,
            currency=payload.currency,
            buyer_account=payload.buyer_account,
            seller_account=payload.seller_account,
            trade_date=payload.trade_date,
            settlement_date=payload.settlement_date,
            status="ACCEPTED",
        )
        self.db.add(trade)
        self.db.flush()

        response = TradeResponse(
            tradeId=trade.id,
            clientTradeId=trade.client_trade_id,
            status=trade.status,
            createdAt=trade.created_at,
        )
        record = IdempotencyRecord(
            idempotency_key=idempotency_key,
            payload_hash=payload_hash,
            correlation_id=correlation_id,
            response_status_code=201,
            response_body=response.model_dump_json(by_alias=True),
            trade_id=trade.id,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(trade)
        return response
