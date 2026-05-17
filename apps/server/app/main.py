"""OpenBerg Terminal — FastAPI backend entry point."""

import asyncio
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, List

from fastapi import FastAPI, HTTPException, Request, WebSocket, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.adapters.base import AdapterError, APIError
from app.models import (
    MarketHistorySchema,
    DividendSchema,
    ErrorResponse,
    HealthResponse,
    NewsSchema,
    PriceBarSchema,
    QuoteSchema,
    SecuritySchema,
)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — ensure SQLite tables exist
    from app.database import init_db
    init_db()

    # Start background ingestion loop
    from app.ingestion import run_loop
    task = asyncio.create_task(run_loop())
    yield
    # Shutdown — cancel ingestion task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="OpenBerg Terminal API",
    description="Open-source financial terminal backend",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(APIError)
async def handle_api_error(request: Request, exc: APIError) -> JSONResponse:
    """Convert application errors into structured ErrorResponse bodies."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=str(exc) or exc.error_code,
            error_code=exc.error_code,
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(mode="json"),
    )


@app.exception_handler(AdapterError)
async def handle_adapter_error(request: Request, exc: AdapterError) -> JSONResponse:
    """Catch upstream adapter failures and return 502 Bad Gateway."""
    return JSONResponse(
        status_code=502,
        content=ErrorResponse(
            detail=str(exc) or "Upstream data adapter failed",
            error_code="UPSTREAM_ERROR",
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(mode="json"),
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Format FastAPI / Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail=str(exc.errors()),
            error_code="VALIDATION_ERROR",
            timestamp=datetime.now(timezone.utc).isoformat(),
        ).model_dump(mode="json"),
    )


# ---------------------------------------------------------------------------
# Pydantic models for user data
# ---------------------------------------------------------------------------

class WatchlistItemIn(BaseModel):
    ticker: str = Field(min_length=1)
    name: str | None = None


class WatchlistItemOut(BaseModel):
    id: int
    ticker: str
    name: str | None
    added_at: str


class PortfolioPositionIn(BaseModel):
    ticker: str = Field(min_length=1)
    shares: float = Field(gt=0)
    cost: float = Field(ge=0)


class PortfolioPositionOut(BaseModel):
    id: int
    ticker: str
    shares: float
    avg_cost: float
    current_price: float
    added_at: str
    updated_at: str


class PortfolioPriceUpdate(BaseModel):
    price: float = Field(gt=0)


class PortfolioSummaryOut(BaseModel):
    total_value: float
    total_cost: float
    total_pnl: float
    pnl_percent: float
    position_count: int


class AlertCreateIn(BaseModel):
    ticker: str = Field(min_length=1)
    alert_type: str = Field(pattern=r"^(price_above|price_below|percent_change|volume)$")
    threshold: float


class AlertOut(BaseModel):
    id: int
    ticker: str
    alert_type: str
    threshold: float
    triggered: int
    created_at: str
    resolved_at: str | None


# ---------------------------------------------------------------------------
# Routes — market data
# ---------------------------------------------------------------------------

@app.get(
    "/api/health",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    from app.websocket import get_available_adapters
    return HealthResponse(
        status="ok",
        version="0.1.0",
        adapters=get_available_adapters(),
    )


@app.get(
    "/api/securities",
    response_model=List[SecuritySchema],
)
async def search_securities(q: str = "") -> List[SecuritySchema]:
    """Search securities by ticker or name."""
    from app.services.data import SecurityService
    raw = SecurityService.search(q)
    return [SecuritySchema.model_validate(s) for s in (raw or [])]


@app.get(
    "/api/securities/{ticker}",
    response_model=SecuritySchema,
)
async def get_security(ticker: str) -> SecuritySchema:
    """Get security description."""
    from app.services.data import SecurityService
    result = SecurityService.get(ticker.upper())
    return SecuritySchema.model_validate(result)


@app.get(
    "/api/quotes",
    response_model=List[QuoteSchema],
)
async def get_quotes(tickers: str = "") -> List[QuoteSchema]:
    """Get real-time quotes for comma-separated tickers."""
    from app.services.data import QuoteService
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    raw = QuoteService.get_batch(ticker_list)
    return [QuoteSchema.model_validate(q) for q in (raw or [])]


@app.get(
    "/api/prices/{ticker}",
    response_model=List[PriceBarSchema],
)
async def get_historical_prices(
    ticker: str,
    interval: str = "1d",
    count: int = 200,
) -> List[PriceBarSchema]:
    """Get historical price bars."""
    from app.services.data import PriceService
    raw = PriceService.get_history(ticker.upper(), interval, count)
    return [PriceBarSchema.model_validate(b) for b in (raw or [])]


@app.get(
    "/api/news",
    response_model=List[NewsSchema],
)
async def get_news(ticker: str = "", limit: int = 50) -> List[NewsSchema]:
    """Get news feed, optionally filtered by ticker."""
    from app.services.data import NewsService
    raw = NewsService.get_feed(ticker.upper() if ticker else None, limit)
    return [NewsSchema.model_validate(n) for n in (raw or [])]


@app.get(
    "/api/dividends/{ticker}",
    response_model=List[DividendSchema],
)
async def get_dividends(ticker: str) -> List[DividendSchema]:
    """Get dividend history."""
    from app.services.data import DividendService
    raw = DividendService.get_history(ticker.upper())
    return [DividendSchema.model_validate(d) for d in (raw or [])]


@app.get(
    "/api/history/{ticker}",
    response_model=List[MarketHistorySchema],
)
async def get_history(ticker: str, days: int = 30) -> List[MarketHistorySchema]:
    """Get stored market history from ingestion snapshots."""
    from app.ingestion import IngestionService
    from app.models import MarketHistorySchema
    raw = await IngestionService.history(ticker.upper(), days)
    return [MarketHistorySchema.model_validate(r) for r in raw]


@app.get("/api/latest", response_model=List[MarketHistorySchema])
async def get_latest(tickers: str = "") -> List[MarketHistorySchema]:
    """Get latest stored snapshots from ingestion."""
    from app.ingestion import IngestionService
    from app.models import MarketHistorySchema
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    raw = await IngestionService.latest(ticker_list)
    return [MarketHistorySchema.model_validate(r) for r in raw]


@app.get(
    "/api/calendar",
    response_model=List[Any],
)
async def get_earnings_calendar() -> List[Any]:
    """Get earnings calendar."""
    # TODO: Wire up earnings data source
    return []


# ---------------------------------------------------------------------------
# Routes — watchlist
# ---------------------------------------------------------------------------

@app.get("/api/watchlist", response_model=list[WatchlistItemOut])
async def list_watchlist():
    """Return the full user watchlist."""
    from app.services.user_data import WatchlistService
    return WatchlistService.get_all()


@app.post(
    "/api/watchlist",
    response_model=WatchlistItemOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_watchlist(item: WatchlistItemIn):
    """Add a ticker to the watchlist."""
    from app.services.user_data import DuplicateError, WatchlistService
    try:
        return WatchlistService.add(item.ticker, item.name)
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.delete(
    "/api/watchlist",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_watchlist(ticker: str):
    """Remove a ticker from the watchlist."""
    from app.services.user_data import WatchlistService
    if not WatchlistService.remove(ticker):
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found in watchlist")
    return None


# ---------------------------------------------------------------------------
# Routes — portfolio
# ---------------------------------------------------------------------------

@app.get("/api/portfolio", response_model=list[PortfolioPositionOut])
async def list_portfolio():
    """Return all portfolio positions."""
    from app.services.user_data import PortfolioService
    return PortfolioService.get_all()


@app.get("/api/portfolio/summary", response_model=PortfolioSummaryOut)
async def portfolio_summary():
    """Return portfolio summary (total value, cost, PnL)."""
    from app.services.user_data import PortfolioService
    return PortfolioService.get_summary()


@app.post(
    "/api/portfolio",
    response_model=PortfolioPositionOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_portfolio(item: PortfolioPositionIn):
    """Add or merge a portfolio position."""
    from app.services.user_data import PortfolioService
    return PortfolioService.add_position(item.ticker, item.shares, item.cost)


@app.patch("/api/portfolio/{ticker}/price", response_model=PortfolioPositionOut)
async def update_portfolio_price(ticker: str, body: PortfolioPriceUpdate):
    """Update the current price for a portfolio position."""
    from app.services.user_data import PortfolioService
    result = PortfolioService.update_price(ticker, body.price)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Position {ticker} not found")
    return result


@app.delete(
    "/api/portfolio",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_portfolio(ticker: str):
    """Remove a position from the portfolio."""
    from app.services.user_data import PortfolioService
    if not PortfolioService.remove(ticker):
        raise HTTPException(status_code=404, detail=f"Position {ticker} not found")
    return None


# ---------------------------------------------------------------------------
# Routes — alerts
# ---------------------------------------------------------------------------

@app.get("/api/alerts", response_model=list[AlertOut])
async def list_alerts():
    """Return active alerts."""
    from app.services.user_data import AlertsService
    return AlertsService.get_active()


@app.post(
    "/api/alerts",
    response_model=AlertOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_alert(item: AlertCreateIn):
    """Create a new alert."""
    from app.services.user_data import AlertsService
    return AlertsService.create(item.ticker, item.alert_type, item.threshold)


@app.delete(
    "/api/alerts",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_alert(alert_id: int):
    """Remove an alert by ID."""
    from app.services.user_data import AlertsService
    if not AlertsService.remove(alert_id):
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    return None


# ---------------------------------------------------------------------------
# WebSocket — live quotes
# ---------------------------------------------------------------------------

@app.websocket("/ws/quotes")
async def websocket_quotes(websocket: WebSocket, tickers: str = ""):
    """WebSocket endpoint for streaming live quotes."""
    from app.websocket import ws_quotes
    await ws_quotes(websocket, tickers)
