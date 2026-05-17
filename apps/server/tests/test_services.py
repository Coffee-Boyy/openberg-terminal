"""Tests for service-layer fallback behaviour."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from app.adapters.base import AdapterError


def _make_error_adapter():
    """Create an adapter mock whose every method raises AdapterError."""
    adapter = MagicMock()
    adapter.search_securities.side_effect = AdapterError("boom")
    adapter.get_security.side_effect = AdapterError("boom")
    adapter.get_quotes.side_effect = AdapterError("boom")
    adapter.get_price_history.side_effect = AdapterError("boom")
    adapter.get_news.side_effect = AdapterError("boom")
    adapter.get_dividends.side_effect = AdapterError("boom")
    return adapter


def _reload_data_module():
    """Force-reload the data module so @patch starts fresh, and clear cache."""
    from app.cache import reset_cache

    # Remove cached modules so patch applies cleanly
    for mod in list(sys.modules):
        if mod.startswith("app.services.data"):
            del sys.modules[mod]

    # Clear the in-memory service cache so stale results don't leak
    # across tests (the @cached_service decorator caches on service method
    # name + args).
    reset_cache()


# ===================================================================
# SecurityService
# ===================================================================


class TestSecurityServiceSearch:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.search_securities.return_value = [{"ticker": "AAPL", "name": "Apple"}]
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import SecurityService
            result = SecurityService.search("aapl")
            assert len(result) == 1
            assert result[0]["ticker"] == "AAPL"

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import SecurityService
            result = SecurityService.search("AAPL")
            assert len(result) == 1
            assert result[0]["ticker"] == "AAPL"

    def test_empty_query_returns_all(self):
        _reload_data_module()
        from app.services.data import SecurityService
        result = SecurityService.search("")
        assert len(result) >= 10


class TestSecurityServiceGet:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.get_security.return_value = {"ticker": "AAPL", "name": "Apple Inc."}
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import SecurityService
            result = SecurityService.get("AAPL")
            assert result["ticker"] == "AAPL"

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import SecurityService
            result = SecurityService.get("AAPL")
            assert result["ticker"] == "AAPL"
            assert result["name"] == "Apple Inc."


# ===================================================================
# QuoteService
# ===================================================================


class TestQuoteService:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.get_quotes.return_value = [{"ticker": "AAPL", "last": 198.0}]
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import QuoteService
            result = QuoteService.get_batch(["AAPL"])
            assert result[0]["ticker"] == "AAPL"

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import QuoteService
            result = QuoteService.get_batch(["AAPL"])
            assert any(q["ticker"] == "AAPL" for q in result)


# ===================================================================
# PriceService
# ===================================================================


class TestPriceService:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.get_price_history.return_value = [
            {"time": "2024-01-01", "close": 100.0}
        ]
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import PriceService
            result = PriceService.get_history("AAPL")
            assert result[0]["close"] == 100.0

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import PriceService
            result = PriceService.get_history("AAPL", count=5)
            assert len(result) == 5


# ===================================================================
# NewsService
# ===================================================================


class TestNewsService:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.get_news.return_value = [{"id": "1", "headline": "Breaking"}]
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import NewsService
            result = NewsService.get_feed(limit=1)
            assert result[0]["id"] == "1"

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import NewsService
            result = NewsService.get_feed(limit=2)
            assert len(result) == 2


# ===================================================================
# DividendService
# ===================================================================


class TestDividendService:
    def test_calls_first_available(self):
        _reload_data_module()
        adapter = MagicMock()
        adapter.get_dividends.return_value = [{"date": "2024-01-01", "amount": 0.24}]
        with patch("app.services.data.get_adapter", return_value=adapter):
            from app.services.data import DividendService
            result = DividendService.get_history("AAPL")
            assert result[0]["amount"] == 0.24

    def test_falls_back_to_mock_on_error(self):
        _reload_data_module()
        err_adapter = _make_error_adapter()
        with patch("app.services.data.get_adapter", return_value=err_adapter):
            from app.services.data import DividendService
            result = DividendService.get_history("AAPL")
            assert len(result) == 8
