"""Data aggregation service — multi-adapter fallback chain with caching."""

import logging
from typing import Optional

from ..adapters.base import BaseAdapter, AdapterError
from ..cache import cached_service

logger = logging.getLogger(__name__)


def get_adapter() -> BaseAdapter:
    """Resolve the first available adapter."""
    from ..adapters.yahoo import YahooAdapter
    from ..adapters.finnhub import FinnhubAdapter

    adapters = [YahooAdapter(), FinnhubAdapter()]
    for adapter in adapters:
        if adapter.is_available():
            return adapter
    from ..adapters.mock import MockAdapter
    return MockAdapter()


class SecurityService:
    """Security master operations."""

    @staticmethod
    @cached_service("SecurityService.search", 300)
    def search(query: str = ""):
        try:
            adapter = get_adapter()
            return adapter.search_securities(query or "")
        except AdapterError as e:
            logger.warning(f"Security search failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().search_securities(query or "")

    @staticmethod
    @cached_service("SecurityService.get", 300)
    def get(ticker: str):
        try:
            adapter = get_adapter()
            return adapter.get_security(ticker)
        except AdapterError as e:
            logger.warning(f"Security lookup failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().get_security(ticker)


class QuoteService:
    """Real-time quote operations."""

    @staticmethod
    @cached_service("QuoteService.get_batch", 10)
    def get_batch(tickers: list[str] = []):
        try:
            adapter = get_adapter()
            return adapter.get_quotes(list(tickers))
        except AdapterError as e:
            logger.warning(f"Quote fetch failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().get_quotes(list(tickers))


class PriceService:
    """Historical price operations."""

    @staticmethod
    @cached_service("PriceService.get_history", 60)
    def get_history(ticker: str, interval: str = "1d", count: int = 200):
        try:
            adapter = get_adapter()
            return adapter.get_price_history(ticker, interval, count)
        except AdapterError as e:
            logger.warning(f"Price history fetch failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().get_price_history(ticker, interval, count)


class NewsService:
    """News feed operations."""

    @staticmethod
    @cached_service("NewsService.get_feed", 60)
    def get_feed(ticker: Optional[str] = None, limit: int = 50):
        try:
            adapter = get_adapter()
            return adapter.get_news(ticker, limit)
        except AdapterError as e:
            logger.warning(f"News fetch failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().get_news(ticker, limit)


class DividendService:
    """Dividend operations."""

    @staticmethod
    @cached_service("DividendService.get_history", 300)
    def get_history(ticker: str):
        try:
            adapter = get_adapter()
            return adapter.get_dividends(ticker)
        except AdapterError as e:
            logger.warning(f"Dividend fetch failed: {e}")
            from ..adapters.mock import MockAdapter
            return MockAdapter().get_dividends(ticker)
