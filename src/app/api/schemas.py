from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TradeCreateRequest(BaseModel):
    client_trade_id: str = Field(min_length=1, max_length=64, alias="clientTradeId")
    instrument_id: str = Field(min_length=1, max_length=32, alias="instrumentId")
    quantity: int = Field(gt=0)
    price: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    buyer_account: str = Field(min_length=1, max_length=64, alias="buyerAccount")
    seller_account: str = Field(min_length=1, max_length=64, alias="sellerAccount")
    trade_date: date = Field(alias="tradeDate")
    settlement_date: date = Field(alias="settlementDate")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()

    @field_validator("settlement_date")
    @classmethod
    def settlement_on_or_after_trade_date(cls, settlement_date: date, info):
        trade_date = info.data.get("trade_date")
        if trade_date and settlement_date < trade_date:
            raise ValueError("settlementDate must be on or after tradeDate")
        return settlement_date


class TradeResponse(BaseModel):
    trade_id: UUID = Field(alias="tradeId")
    client_trade_id: str = Field(alias="clientTradeId")
    status: str
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ErrorResponse(BaseModel):
    detail: str
