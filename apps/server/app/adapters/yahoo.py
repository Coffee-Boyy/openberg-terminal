"""Yahoo Finance data adapter."""

import os
import logging
from typing import Any, Optional

from .base import BaseAdapter, AdapterError

logger = logging.getLogger(__name__)


class YahooAdapter(BaseAdapter):
    """Yahoo Finance adapter for market data."""

    @property
    def name(self) -> str:
        return "yahoo"

    def is_available(self) -> bool:
        # Check if yfinance is installed and API key is set if needed
        try:
            import yfinance as yf
            return yf is not None
        except ImportError:
            return False

    def search_securities(self, query: str) -> list[dict[str, Any]]:
        if not query:
            return []
        # Use yfinance search
        import yfinance as yf
        ticker = yf.Ticker(query)
        info = ticker.info
        if not info:
            return []
        return [{
            "ticker": ticker.ticker,
            "name": info.get("longName", ticker.ticker),
            "exchange": info.get("exchange", "UNKNOWN"),
            "currency": info.get("currency", "USD"),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "type": "equity",
            "status": "active",
            "marketCap": info.get("marketCap"),
            "peRatio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "beta": info.get("beta"),
        }]

    def get_security(self, ticker: str) -> dict[str, Any]:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.info
        return {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "exchange": info.get("exchange", "UNKNOWN"),
            "currency": info.get("currency", "USD"),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
            "type": "equity",
            "status": "active",
            "marketCap": info.get("marketCap"),
            "peRatio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "dividendYield": info.get("dividendYield"),
            "beta": info.get("beta"),
        }

    def get_quotes(self, tickers: list[str]) -> list[dict[str, Any]]:
        if not tickers:
            return []
        import yfinance as yf
        quotes = []
        for t in tickers:
            try:
                ticker = yf.Ticker(t)
                info = ticker.info
                quotes.append({
                    "ticker": t,
                    "exchange": info.get("exchange", "UNKNOWN"),
                    "currency": info.get("currency", "USD"),
                    "bid": info.get("bid", 0),
                    "ask": info.get("ask", 0),
                    "last": info.get("currentPrice", 0),
                    "change": info.get("regularMarketChange", 0),
                    "changePercent": info.get("regularMarketChangePercent", 0),
                    "volume": info.get("volume", 0),
                    "marketCap": info.get("marketCap"),
                    "timestamp": info.get("currentPriceTime", ""),
                })
            except Exception as e:
                logger.warning(f"Yahoo quote failed for {t}: {e}")
        return quotes

    def get_price_history(
        self, ticker: str, interval: str = "1d", count: int = 200
    ) -> list[dict[str, Any]]:
        import yfinance as yf
        t = yf.Ticker(ticker)
        period = "max" if count > 1000 else "1y"
        hist = t.history(period=period, interval="1d")
        if hist.empty:
            return []
        result = []
        for date, row in hist.iterrows():
            result.append({
                "time": date.isoformat(),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            })
        return result[-count:]

    def get_news(
        self, ticker: Optional[str] = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        if ticker:
            import yfinance as yf
            t = yf.Ticker(ticker)
            news = t.news if hasattr(t, "news") else []
            return [
                {
                    "id": str(n.get("uuid", "")),
                    "headline": n.get("title", ""),
                    "summary": n.get("summary", ""),
                    "source": n.get("source", ""),
                    "published": n.get("providerPublishTime", ""),
                    "sentiment": "neutral",
                    "tickers": [ticker] if ticker else [],
                    "categories": [],
                }
                for n in news[:limit]
            ]
        # No general news from Yahoo, use mock
        return []

    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        import yfinance as yf
        t = yf.Ticker(ticker)
        div = t.dividends
        if div.empty:
            return []
        return [
            {
                "date": date.isoformat(),
                "amount": float(amount),
            }
            for date, amount in div.items()
        ]
