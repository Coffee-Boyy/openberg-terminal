"""OpenBerg Terminal — FastAPI backend entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


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


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/securities")
async def search_securities(q: str = ""):
    """Search securities by ticker or name."""
    # Returns list of Security models
    from app.services.data import SecurityService
    return SecurityService.search(q)


@app.get("/api/securities/{ticker}")
async def get_security(ticker: str):
    """Get security description."""
    from app.services.data import SecurityService
    return SecurityService.get(ticker.upper())


@app.get("/api/quotes")
async def get_quotes(tickers: str = ""):
    """Get real-time quotes for comma-separated tickers."""
    from app.services.data import QuoteService
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    return QuoteService.get_batch(ticker_list)


@app.get("/api/prices/{ticker}")
async def get_historical_prices(
    ticker: str,
    interval: str = "1d",
    count: int = 200,
):
    """Get historical price bars."""
    from app.services.data import PriceService
    return PriceService.get_history(ticker.upper(), interval, count)


@app.get("/api/news")
async def get_news(ticker: str = "", limit: int = 50):
    """Get news feed, optionally filtered by ticker."""
    from app.services.data import NewsService
    return NewsService.get_feed(ticker.upper() if ticker else None, limit)


@app.get("/api/dividends/{ticker}")
async def get_dividends(ticker: str):
    """Get dividend history."""
    from app.services.data import DividendService
    return DividendService.get_history(ticker.upper())


@app.get("/api/calendar")
async def get_earnings_calendar():
    """Get earnings calendar."""
    # TODO: Wire up earnings data source
    return []
