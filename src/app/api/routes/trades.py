from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.schemas import ErrorResponse, TradeCreateRequest, TradeResponse
from app.application.trade_service import TradeService

router = APIRouter(tags=["trades"])


@router.post(
    "/trades",
    response_model=TradeResponse,
    responses={409: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
def submit_trade(
    payload: TradeCreateRequest,
    request: Request,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> TradeResponse:
    if not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required",
        )

    service = TradeService(db)
    try:
        result = service.submit_trade(
            payload=payload,
            idempotency_key=idempotency_key,
            correlation_id=request.state.correlation_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return result
