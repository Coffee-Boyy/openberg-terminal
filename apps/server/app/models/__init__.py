"""Pydantic v2 response models for the OpenBerg Terminal API."""

from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Security / Quote
# ---------------------------------------------------------------------------

class SecuritySchema(BaseModel):
    """Full description of a security."""

    ticker: str
    name: str
    exchange: Optional[str] = None
    currency: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    marketCap: Optional[float] = Field(None, alias="marketCap")
    peRatio: Optional[float] = Field(None, alias="peRatio")
    eps: Optional[float] = None
    dividendYield: Optional[float] = Field(None, alias="dividendYield")
    beta: Optional[float] = None


class QuoteSchema(BaseModel):
    """Real-time quote snapshot."""

    ticker: str
    exchange: Optional[str] = None
    currency: Optional[str] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    change: Optional[float] = None
    changePercent: Optional[float] = Field(None, alias="changePercent")
    volume: Optional[int] = None
    marketCap: Optional[float] = Field(None, alias="marketCap")
    timestamp: Optional[str] = None


class PriceBarSchema(BaseModel):
    """A single historical price bar."""

    time: str
    open: Optional[float] = Field(None, alias="open")
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None


class NewsSchema(BaseModel):
    """A news article."""

    id: str
    headline: str
    summary: Optional[str] = None
    source: Optional[str] = None
    published: Optional[str] = None
    sentiment: Optional[str] = None
    tickers: Optional[list[str]] = None
    categories: Optional[list[str]] = None


class DividendSchema(BaseModel):
    """A single dividend payment."""

    date: str
    amount: Optional[float] = None


# ---------------------------------------------------------------------------
# Error / Meta
# ---------------------------------------------------------------------------

class ErrorResponse(BaseModel):
    """Standard error response body."""

    detail: str
    error_code: str
    timestamp: Optional[str] = None


class HealthResponse(BaseModel):
    """Health-check response."""

    status: str
    version: str
    adapters: list[str] = []
