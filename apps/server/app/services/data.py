"""Data aggregation service — multi-adapter fallback chain."""

import logging
from typing import Optional

from ..adapters.base import BaseAdapter, AdapterError

logger = logging.getLogger(__name__)


def get_adapter() -> BaseAdapter:
    """Resolve the first available adapter."""
    from ..adapters.yahoo import YahooAdapter
    from ..adapters.finnhub import FinnhubAdapter

    # Try adapters in priority order
    adapters = [YahooAdapter(), FinnhubAdapter()]
    for adapter in adapters:
        if adapter.is_available():
            return adapter
    # Fallback to mock data
    from ..adapters.mock import MockAdapter
    return MockAdapter()


class SecurityService:
    """Security master operations."""

    @staticmethod
    def search(query: str = []):
        try:
            adapter = get_adapter()
            return adapter.search_securities(query or "")
        except AdapterError as e:
            logger.warning(f"Security search failed: {e}")
            return MockAdapter().search_securities(query or "")

    @staticmethod
    def get(ticker: str):
        try:
            adapter = get_adapter()
            return adapter.get_security(ticker)
        except AdapterError as e:
            logger.warning(f"Security lookup failed: {e}")
            return MockAdapter().get_security(ticker)


class QuoteService:
    """Real-time quote operations."""

    @staticmethod
    def get_batch(tickers: list = []):
        try:
            adapter = get_adapter()
            return adapter.get_quotes(tickers)
        except AdapterError as e:
            logger.warning(f"Quote fetch failed: {e}")
            return MockAdapter().get_quotes(tickers)


class PriceService:
    """Historical price operations."""

    @staticmethod
    def get_history(ticker: str, interval: str = "1d", count: int = 200):
        try:
            adapter = get_adapter()
            return adapter.get_price_history(ticker, interval, count)
        except AdapterError as e:
            logger.warning(f"Price history fetch failed: {e}")
            return MockAdapter().get_price_history(ticker, interval, count)


class NewsService:
    """News feed operations."""

    @staticmethod
    def get_feed(ticker: Optional[str] = None, limit: int = 50):
        try:
            adapter = get_adapter()
            return adapter.get_news(ticker, limit)
        except AdapterError as e:
            logger.warning(f"News fetch failed: {e}")
            return MockAdapter().get_news(ticker, limit)


class DividendService:
    """Dividend operations."""

    @staticmethod
    def get_history(ticker: str):
        try:
            adapter = get_adapter()
            return adapter.get_dividends(ticker)
        except AdapterError as e:
            logger.warning(f"Dividend fetch failed: {e}")
            return MockAdapter().get_dividends(ticker)
