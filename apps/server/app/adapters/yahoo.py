"""Yahoo Finance data adapter."""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError as FuturesTimeoutError
from typing import Any, Optional

from .base import BaseAdapter, AdapterError

logger = logging.getLogger(__name__)

# Timeout for individual yfinance calls (seconds)
# yfinance can hang on stale tickers; this keeps the batch from blocking.
_CALL_TIMEOUT = 15


class YahooAdapter(BaseAdapter):
    """Yahoo Finance adapter for market data."""

    @property
    def name(self) -> str:
        return "yahoo"

    def is_available(self) -> bool:
        try:
            import yfinance as yf
            return yf is not None
        except ImportError:
            return False

    # ── Helpers ───────────────────────────────────────────────────

    def _call_with_timeout(self, func, *args, **kwargs):
        """Run *func* in a daemon thread with a timeout so a single yfinance
        call cannot hang the entire request.  Returns the result on success,
        raises ``TimeoutError`` if the call takes too long."""
        result: list = []
        exc: list = []

        def _target():
            try:
                result.append(func(*args, **kwargs))
            except Exception as e:
                exc.append(e)

        t = threading.Thread(target=_target, daemon=True)
        t.start()
        t.join(timeout=_CALL_TIMEOUT)
        if t.is_alive():
            raise TimeoutError(
                f"yfinance call timed out after {_CALL_TIMEOUT}s"
            )
        if exc:
            raise exc[0]
        return result[0]

    # ── BaseAdapter interface ─────────────────────────────────────

    def search_securities(self, query: str) -> list[dict[str, Any]]:
        if not query:
            return []
        import yfinance as yf

        try:
            ticker = self._call_with_timeout(lambda: yf.Ticker(query))
            info = self._call_with_timeout(lambda: ticker.info)
        except Exception as e:
            logger.warning(f"Yahoo search failed for '{query}': {e}")
            return []

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

        t = self._call_with_timeout(lambda: yf.Ticker(ticker))
        info = self._call_with_timeout(lambda: t.info)
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
        """Fetch quotes for each ticker with per-call isolation.

        Each ticker is fetched in its own thread with a timeout so that a
        single slow or broken symbol cannot delay the entire batch.  Failed
        tickers are logged and skipped — they never corrupt successful results.
        """
        if not tickers:
            return []
        import yfinance as yf

        def _fetch_one(t: str) -> Optional[dict[str, Any]]:
            """Fetch a single quote. Returns None on failure."""
            try:
                yt = yf.Ticker(t)
                info = yt.info
                if not info:
                    return None
                return {
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
                }
            except Exception as e:
                logger.warning(f"Yahoo quote failed for {t}: {e}")
                return None

        quotes: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=min(8, len(tickers))) as pool:
            futures: list[Future] = [
                pool.submit(_fetch_one, t) for t in tickers
            ]
            for fut in futures:
                try:
                    quote = fut.result(timeout=_CALL_TIMEOUT + 2)
                    if quote is not None:
                        quotes.append(quote)
                except FuturesTimeoutError:
                    logger.warning("Quote fetch timed out for a ticker")
                except Exception as e:
                    logger.warning(f"Quote thread raised: {e}")
        return quotes

    def get_price_history(
        self, ticker: str, interval: str = "1d", count: int = 200
    ) -> list[dict[str, Any]]:
        import yfinance as yf

        t = self._call_with_timeout(lambda: yf.Ticker(ticker))
        period = "max" if count > 1000 else "1y"

        def _fetch():
            return t.history(period=period, interval=interval)

        hist = self._call_with_timeout(_fetch)
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

            yt = self._call_with_timeout(lambda: yf.Ticker(ticker))
            news = getattr(yt, "news", [])
            return [
                {
                    "id": str(n.get("uuid", "")),
                    "headline": n.get("title", ""),
                    "summary": n.get("summary", ""),
                    "source": n.get("source", ""),
                    "published": n.get("providerPublishTime", ""),
                    "sentiment": "neutral",
                    "tickers": [ticker],
                    "categories": [],
                }
                for n in news[:limit]
            ]
        # Yahoo doesn't offer general market news
        return []

    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        import yfinance as yf

        t = self._call_with_timeout(lambda: yf.Ticker(ticker))
        div = self._call_with_timeout(lambda: t.dividends)
        if div.empty:
            return []
        return [
            {
                "date": date.isoformat(),
                "amount": float(amount),
            }
            for date, amount in div.items()
        ]
