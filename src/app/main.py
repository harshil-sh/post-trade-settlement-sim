from fastapi import FastAPI

from app.api.middleware import CorrelationIdMiddleware
from app.api.routes import health, trades
from app.infrastructure.db import initialize_database
from app.infrastructure.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Post-Trade Settlement Simulator", version="0.1.0")
    app.add_middleware(CorrelationIdMiddleware)
    app.include_router(health.router)
    app.include_router(trades.router, prefix="/api/v1")

    @app.on_event("startup")
    def _startup() -> None:
        initialize_database()

    return app


app = create_app()
