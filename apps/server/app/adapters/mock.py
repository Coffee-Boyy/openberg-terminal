"""Mock data adapter — works without any API keys."""

import math
import random
from datetime import datetime, timedelta
from typing import Any, Optional

from .base import BaseAdapter

# Deterministic seed-based data
SECURITIES = {
    "AAPL": {"name": "Apple Inc.", "exchange": "NASDAQ", "sector": "Technology", "industry": "Consumer Electronics", "currency": "USD", "marketCap": 3_050_000_000_000, "peRatio": 31.2, "eps": 6.13, "dividendYield": 0.5, "beta": 1.18, "price": 198.2},
    "GOOG": {"name": "Alphabet Inc.", "exchange": "NASDAQ", "sector": "Technology", "industry": "Internet Content & Services", "currency": "USD", "marketCap": 2_100_000_000_000, "peRatio": 27.5, "eps": 6.05, "dividendYield": 0, "beta": 1.06, "price": 172.5},
    "MSFT": {"name": "Microsoft Corp.", "exchange": "NASDAQ", "sector": "Technology", "industry": "Systems Software", "currency": "USD", "marketCap": 3_200_000_000_000, "peRatio": 36.8, "eps": 11.05, "dividendYield": 0.7, "beta": 0.92, "price": 389.1},
    "AMZN": {"name": "Amazon.com Inc.", "exchange": "NASDAQ", "sector": "Consumer Discretionary", "industry": "Internet Retail", "currency": "USD", "marketCap": 2_200_000_000_000, "peRatio": 60.1, "eps": 3.01, "dividendYield": 0, "beta": 1.18, "price": 180.7},
    "TSLA": {"name": "Tesla Inc.", "exchange": "NASDAQ", "sector": "Consumer Discretionary", "industry": "Auto Manufacturers", "currency": "USD", "marketCap": 560_000_000_000, "peRatio": 95.4, "eps": 3.75, "dividendYield": 0, "beta": 2.27, "price": 177.4},
    "NVDA": {"name": "NVIDIA Corp.", "exchange": "NASDAQ", "sector": "Technology", "industry": "Semiconductors", "currency": "USD", "marketCap": 2_800_000_000_000, "peRatio": 64.8, "eps": 13.4, "dividendYield": 0.02, "beta": 1.68, "price": 875.3},
    "META": {"name": "Meta Platforms Inc.", "exchange": "NASDAQ", "sector": "Technology", "industry": "Internet Content & Services", "currency": "USD", "marketCap": 1_500_000_000_000, "peRatio": 28.3, "eps": 19.72, "dividendYield": 0.3, "beta": 1.18, "price": 502.8},
    "JPM": {"name": "JPMorgan Chase & Co.", "exchange": "NYSE", "sector": "Financials", "industry": "Banks", "currency": "USD", "marketCap": 620_000_000_000, "peRatio": 12.1, "eps": 17.37, "dividendYield": 2.2, "beta": 1.12, "price": 210.3},
    "V": {"name": "Visa Inc.", "exchange": "NYSE", "sector": "Financials", "industry": "Data Processing Services", "currency": "USD", "marketCap": 520_000_000_000, "peRatio": 31.0, "eps": 8.88, "dividendYield": 0.7, "beta": 0.94, "price": 283.5},
    "WMT": {"name": "Walmart Inc.", "exchange": "NYSE", "sector": "Consumer Staples", "industry": "Discount Stores", "currency": "USD", "marketCap": 480_000_000_000, "peRatio": 29.5, "eps": 6.29, "dividendYield": 1.2, "beta": 0.52, "price": 185.6},
    "SPY": {"name": "SPDR S&P 500 ETF Trust", "exchange": "NYSE Arca", "sector": "Index", "industry": "Broad Market", "currency": "USD", "marketCap": 500_000_000_000, "peRatio": 0, "eps": 0, "dividendYield": 0.85, "beta": 1.0, "price": 520.4},
    "BTC": {"name": "Bitcoin USD", "exchange": "CRYPTO", "sector": "Crypto", "industry": "Currency", "currency": "USD", "marketCap": 1_900_000_000_000, "peRatio": 0, "eps": 0, "beta": 0, "price": 67_500},
    "EURUSD": {"name": "EUR/USD", "exchange": "FOREX", "sector": "Forex", "industry": "Currency", "currency": "USD", "peRatio": 0, "eps": 0, "beta": 0, "price": 1.085},
}


class MockAdapter(BaseAdapter):
    """Mock data adapter — returns realistic demo data."""

    @property
    def name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return True

    def _rng(self, ticker: str) -> random.Random:
        """Deterministic RNG for a ticker."""
        h = hash(ticker)
        return random.Random(h)

    def search_securities(self, query: str = "") -> list[dict[str, Any]]:
        if not query:
            return list(SECURITIES.items())
        q = query.lower()
        return [
            (ticker, info)
            for ticker, info in SECURITIES.items()
            if q in ticker.lower() or q in info["name"].lower()
        ]

    def get_security(self, ticker: str) -> dict[str, Any]:
        info = SECURITIES.get(ticker.upper())
        if not info:
            return {
                "ticker": ticker,
                "name": ticker,
                "exchange": "UNKNOWN",
                "currency": "USD",
                "sector": "",
                "industry": "",
                "type": "equity",
                "status": "active",
                "marketCap": None,
                "peRatio": None,
                "eps": None,
                "dividendYield": None,
                "beta": None,
            }
        return {
            "ticker": ticker,
            "name": info["name"],
            "exchange": info["exchange"],
            "currency": info["currency"],
            "sector": info["sector"],
            "industry": info["industry"],
            "type": "equity",
            "status": "active",
            "marketCap": info["marketCap"],
            "peRatio": info["peRatio"],
            "eps": info["eps"],
            "dividendYield": info["dividendYield"],
            "beta": info["beta"],
        }

    def get_quotes(self, tickers: list[str]) -> list[dict[str, Any]]:
        results = []
        for t in tickers:
            info = SECURITIES.get(t.upper())
            if not info:
                continue
            rng = self._rng(t)
            price = info["price"] * (1 + rng.uniform(-0.02, 0.02))
            change_pct = rng.uniform(-2, 2)
            results.append({
                "ticker": t.upper(),
                "exchange": info["exchange"],
                "currency": info["currency"],
                "bid": price - 0.05,
                "ask": price + 0.05,
                "last": price,
                "change": price * change_pct / 100,
                "changePercent": change_pct,
                "volume": rng.randint(100_000, 50_000_000),
                "marketCap": info["marketCap"],
                "timestamp": datetime.now().isoformat(),
            })
        return results

    def get_price_history(
        self, ticker: str, interval: str = "1d", count: int = 200
    ) -> list[dict[str, Any]]:
        info = SECURITIES.get(ticker.upper())
        base = info["price"] if info else 100
        rng = self._rng(ticker + interval)
        volatility = base * 0.005 if base > 100 else 0.01
        price = base * 0.85
        results = []
        now = datetime.now()
        for i in range(count):
            change = rng.gauss(0, volatility)
            close = price + change
            high = max(price, close) + rng.uniform(0, volatility)
            low = min(price, close) - rng.uniform(0, volatility)
            results.append({
                "time": (now - timedelta(days=count - i)).isoformat(),
                "open": round(price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close, 2),
                "volume": rng.randint(10_000, 1_000_000),
            })
            price = close
        return results

    def get_news(
        self, ticker: Optional[str] = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        headlines = [
            ("Apple Beats Q4 Earnings Expectations", ["AAPL"], "positive"),
            ("Fed Holds Rates Steady at 5.25%", ["SPY", "JPM"], "neutral"),
            ("NVIDIA Surpasses $3T Market Cap", ["NVDA"], "positive"),
            ("Tesla Delivery Numbers Miss Estimates", ["TSLA"], "negative"),
            ("Meta Announces $500B Buyback", ["META"], "positive"),
            ("JPMorgan Raises 2026 Growth Forecast", ["JPM", "SPY"], "positive"),
            ("Amazon Web Services Launches AI Chip", ["AMZN", "NVDA"], "positive"),
            ("Bitcoin Surges Past $67K", ["BTC"], "positive"),
            ("EUR/USD Slips on ECB Dovish Outlook", ["EURUSD"], "negative"),
            ("Microsoft Cloud Revenue Grows 24%", ["MSFT"], "positive"),
            ("Google Faces EU Antitrust Probe", ["GOOG"], "negative"),
            ("Visa Processes Record Volume", ["V"], "positive"),
            ("Walmart Expands Same-Day Delivery", ["WMT"], "positive"),
        ]
        results = []
        now = datetime.now()
        for i, (headline, tickers, sentiment) in enumerate(headlines):
            if ticker and ticker not in tickers:
                continue
            results.append({
                "id": f"mock-{i}",
                "headline": headline,
                "summary": "",
                "source": "OpenBerg Demo",
                "published": (now - timedelta(minutes=i * 30)).isoformat(),
                "sentiment": sentiment,
                "tickers": tickers,
                "categories": ["markets"],
            })
            if len(results) >= limit:
                break
        return results

    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        info = SECURITIES.get(ticker.upper())
        if not info or not info.get("dividendYield"):
            return []
        price = info["price"]
        annual = price * info["dividendYield"]
        quarterly = annual / 4
        results = []
        for i in range(8):
            results.append({
                "date": (datetime.now() - timedelta(months=3 * (7 - i))).isoformat(),
                "amount": round(quarterly, 4),
            })
        return results
