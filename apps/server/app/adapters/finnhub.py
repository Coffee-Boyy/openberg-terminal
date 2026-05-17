"""Finnhub data adapter — sync HTTP via requests."""

import os
import logging
from typing import Any, Optional

import requests

from .base import BaseAdapter, AdapterError

logger = logging.getLogger(__name__)

# Finnhub API base URL
_API_BASE = "https://finnhub.io/api/v1"

# Default timeout for all HTTP calls (seconds)
_DEFAULT_TIMEOUT = 10


class FinnhubAdapter(BaseAdapter):
    """Finnhub adapter for market data.

    Uses synchronous ``requests`` calls — no asyncio event loop needed.
    All methods are sync and safe to call from FastAPI sync endpoints.
    """

    @property
    def name(self) -> str:
        return "finnhub"

    def is_available(self) -> bool:
        return bool(os.environ.get("FINNHUB_API_KEY"))

    # ── HTTP helpers ──────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        return {"X-Api-Key": os.environ["FINNHUB_API_KEY"]}

    def _get(self, path: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Synchronous GET to a Finnhub REST endpoint."""
        url = f"{_API_BASE}/{path}"
        resp = requests.get(url, headers=self._headers(), params=params, timeout=_DEFAULT_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    # ── BaseAdapter interface ─────────────────────────────────────

    def search_securities(self, query: str) -> list[dict[str, Any]]:
        """Search securities by ticker symbol or company name.

        Uses the Finnhub search endpoint which returns a list of
        matching securities with exchange, type, and description.
        """
        if not query:
            return []
        try:
            result = self._get(
                "search/query",
                {"q": query, "exchange": "US"},
            )
        except Exception as e:
            logger.warning(f"Finnhub search failed for '{query}': {e}")
            return []

        hits = result.get("result", [])
        return [
            {
                "ticker": h["symbol"],
                "name": h.get("description", ""),
                "exchange": h.get("exchange", {}).get("displayCode", h.get("exchange", "UNKNOWN")),
                "currency": h.get("currency", "USD"),
                "sector": "",
                "industry": "",
                "type": "equity",
                "status": "active",
            }
            for h in hits
            if h.get("type") == "Common Stock"
        ]

    def get_security(self, ticker: str) -> dict[str, Any]:
        try:
            profile = self._get("stock/profile2", {"symbol": ticker})
        except Exception as e:
            raise AdapterError(f"Finnhub profile failed for {ticker}: {e}") from e

        return {
            "ticker": ticker,
            "name": profile.get("name", ticker),
            "exchange": profile.get("exchange", "UNKNOWN"),
            "currency": profile.get("currencyCode", "USD"),
            "sector": profile.get("finnhubIndustry", ""),
            "industry": profile.get("finnhubIndustry", ""),
            "type": "equity",
            "status": "active",
            "marketCap": profile.get("marketCapitalization"),
            "peRatio": profile.get("pe"),
            "eps": profile.get("eps"),
            "beta": profile.get("beta"),
        }

    def get_quotes(self, tickers: list[str]) -> list[dict[str, Any]]:
        if not tickers:
            return []
        quotes: list[dict[str, Any]] = []
        for t in tickers:
            try:
                quote = self._get("quote", {"symbol": t})
                quotes.append({
                    "ticker": t,
                    "exchange": "UNKNOWN",
                    "currency": "USD",
                    "bid": quote.get("high", 0) - 0.01,
                    "ask": quote.get("high", 0) + 0.01,
                    "last": quote.get("c", 0),
                    "change": quote.get("d", 0),
                    "changePercent": quote.get("dp", 0),
                    "volume": 0,
                    "marketCap": None,
                    "timestamp": "",
                })
            except Exception as e:
                logger.warning(f"Finnhub quote failed for {t}: {e}")
        return quotes

    def get_price_history(
        self, ticker: str, interval: str = "1d", count: int = 200
    ) -> list[dict[str, Any]]:
        from datetime import datetime

        resolution_map = {
            "1m": "1", "5m": "5", "15m": "15",
            "1h": "60", "4h": "240", "1d": "D",
        }
        resolution = resolution_map.get(interval, "D")

        try:
            result = self._get(
                "stock/candle",
                {
                    "symbol": ticker,
                    "resolution": resolution,
                    "from": 0,
                    "to": 0,
                    "limit": count,
                },
            )
        except Exception as e:
            logger.warning(f"Finnhub candles failed for {ticker}: {e}")
            return []

        if result.get("s") != "ok":
            return []

        return [
            {
                "time": datetime.fromtimestamp(ts).isoformat(),
                "open": row[0],
                "high": row[1],
                "low": row[2],
                "close": row[3],
                "volume": row[4],
            }
            for ts, row in zip(result["t"], result["c"])
        ]

    def get_news(
        self, ticker: Optional[str] = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Fetch news. If *ticker* is provided, use company-specific news;
        otherwise fetch general market news."""
        try:
            if ticker:
                result = self._get(
                    "companyNews",
                    {"symbol": ticker, "from": "2020-01-01"},
                )
            else:
                result = self._get(
                    "news",
                    {"category": "general"},
                )
        except Exception as e:
            logger.warning(f"Finnhub news failed: {e}")
            return []

        return [
            {
                "id": str(n.get("id", "")),
                "headline": n.get("headline", ""),
                "summary": n.get("summary", ""),
                "source": n.get("source", ""),
                "published": str(n.get("datetime", "")),
                "sentiment": "neutral",
                "tickers": n.get("related", "").split(",") if n.get("related") else [],
                "categories": [],
            }
            for n in result[:limit]
        ]

    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        """Return an empty list — Finnhub does not provide a dividend history
        endpoint. Their deprecated 'stock/stock-financials' tool had partial
        dividend data but is no longer available in the current API.

        For dividend data, prefer the Yahoo adapter.
        """
        return []
