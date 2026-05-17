"""Finnhub data adapter."""

import os
import aiohttp
import logging
from typing import Any, Optional

from .base import BaseAdapter, AdapterError

logger = logging.getLogger(__name__)


class FinnhubAdapter(BaseAdapter):
    """Finnhub adapter for market data."""

    @property
    def name(self) -> str:
        return "finnhub"

    def is_available(self) -> bool:
        return bool(os.environ.get("FINNHUB_API_KEY"))

    def _headers(self) -> dict[str, str]:
        return {"X-Api-Key": os.environ["FINNHUB_API_KEY"]}

    async def _get(self, path: str, params: Optional[dict] = None) -> Any:
        url = f"https://finnhub.io/api/v1/{path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers(), params=params) as resp:
                return await resp.json()

    def search_securities(self, query: str) -> list[dict[str, Any]]:
        if not query:
            return []
        # Finnhub search is async — use sync fallback
        return []

    def get_security(self, ticker: str) -> dict[str, Any]:
        profile = self._run(self._get("stock/profile2", {"symbol": ticker}))
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
        quotes = []
        for t in tickers:
            try:
                quote = self._run(self._get("quote", {"symbol": t}))
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
        resolution_map = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1d": "D"}
        resolution = resolution_map.get(interval, "D")
        result = self._run(self._get(
            "stock/candle",
            {"symbol": ticker, "resolution": resolution, "from": 0, "to": 0, "limit": count},
        ))
        if result.get("s") != "ok":
            return []
        return [
            {
                "time": __import__("datetime").datetime.fromtimestamp(ts).isoformat(),
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
        token = os.environ.get("FINNHUB_API_KEY", "")
        if ticker:
            return []
        # General news
        result = self._run(self._get(
            "news",
            {"category": "general"},
        ))
        return [
            {
                "id": str(n.get("id", "")),
                "headline": n.get("headline", ""),
                "summary": n.get("summary", ""),
                "source": n.get("source", ""),
                "published": str(n.get("datetime", "")),
                "sentiment": "neutral",
                "tickers": n.get("related", "").split(","),
                "categories": [],
            }
            for n in result[:limit]
        ]

    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        # Finnhub doesn't have dividend endpoint
        return []

    # Helper to run async
    def _run(self, coro):
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(coro)
        except RuntimeError:
            return asyncio.run(coro)
