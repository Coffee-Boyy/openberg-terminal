"""Tests for adapter implementations."""

import pytest

from app.adapters.base import BaseAdapter
from app.adapters.mock import MockAdapter


# ===================================================================
# MockAdapter — all six methods return correct shapes
# ===================================================================

class TestMockAdapterSearch:
    """MockAdapter.search_securities."""

    def test_returns_all_when_empty_query(self):
        adapter = MockAdapter()
        results = adapter.search_securities()
        assert len(results) >= 10
        for r in results:
            assert "ticker" in r
            assert "name" in r
            assert "exchange" in r

    def test_filters_by_ticker(self):
        adapter = MockAdapter()
        results = adapter.search_securities("Aapl")
        assert any(r["ticker"] == "AAPL" for r in results)
        assert not any(r["ticker"] == "GOOG" for r in results)

    def test_filters_by_name(self):
        adapter = MockAdapter()
        results = adapter.search_securities("Apple")
        assert any(r["ticker"] == "AAPL" for r in results)

    def test_case_insensitive(self):
        adapter = MockAdapter()
        results = adapter.search_securities("aapl")
        assert any(r["ticker"] == "AAPL" for r in results)


class TestMockAdapterGetSecurity:
    """MockAdapter.get_security."""

    def test_known_ticker(self):
        adapter = MockAdapter()
        sec = adapter.get_security("AAPL")
        assert sec["ticker"] == "AAPL"
        assert sec["name"] == "Apple Inc."
        assert sec["exchange"] == "NASDAQ"
        assert sec["sector"] == "Technology"

    def test_unknown_ticker(self):
        adapter = MockAdapter()
        sec = adapter.get_security("NONEXISTENT")
        assert sec["ticker"] == "NONEXISTENT"
        assert sec["exchange"] == "UNKNOWN"

    def test_lower_case_input(self):
        adapter = MockAdapter()
        sec = adapter.get_security("aapl")
        assert sec["name"] == "Apple Inc."


class TestMockAdapterGetQuotes:
    """MockAdapter.get_quotes."""

    def test_known_tickers(self):
        adapter = MockAdapter()
        quotes = adapter.get_quotes(["AAPL", "MSFT"])
        tickers = {q["ticker"] for q in quotes}
        assert tickers == {"AAPL", "MSFT"}
        for q in quotes:
            assert q["last"] is not None
            assert q["bid"] is not None
            assert q["ask"] is not None
            assert q["change"] is not None
            assert q["changePercent"] is not None
            assert q["volume"] is not None
            assert q["timestamp"] is not None

    def test_unknown_ticker_skipped(self):
        adapter = MockAdapter()
        quotes = adapter.get_quotes(["FAKE"])
        assert quotes == []

    def test_empty_list(self):
        adapter = MockAdapter()
        quotes = adapter.get_quotes([])
        assert quotes == []


class TestMockAdapterGetPriceHistory:
    """MockAdapter.get_price_history."""

    def test_returns_bars(self):
        adapter = MockAdapter()
        bars = adapter.get_price_history("AAPL", count=10)
        assert len(bars) == 10
        for b in bars:
            assert "time" in b
            assert b["open"] is not None
            assert b["high"] is not None
            assert b["low"] is not None
            assert b["close"] is not None
            assert b["volume"] is not None

    def test_unknown_ticker(self):
        adapter = MockAdapter()
        bars = adapter.get_price_history("NONEXIST", count=5)
        # Should still produce bars (base price = 100)
        assert len(bars) == 5

    def test_interval(self):
        adapter = MockAdapter()
        bars = adapter.get_price_history("AAPL", interval="1h", count=5)
        assert len(bars) == 5


class TestMockAdapterGetNews:
    """MockAdapter.get_news."""

    def test_general_news(self):
        adapter = MockAdapter()
        articles = adapter.get_news(limit=3)
        assert len(articles) == 3
        for a in articles:
            assert "id" in a
            assert "headline" in a
            assert "source" in a
            assert "published" in a
            assert "sentiment" in a
            assert "tickers" in a

    def test_ticker_filter(self):
        adapter = MockAdapter()
        articles = adapter.get_news(ticker="AAPL")
        for a in articles:
            assert "AAPL" in a["tickers"]

    def test_limit(self):
        adapter = MockAdapter()
        articles = adapter.get_news(limit=2)
        assert len(articles) == 2


class TestMockAdapterGetDividends:
    """MockAdapter.get_dividends."""

    def test_dividend_paying_stock(self):
        adapter = MockAdapter()
        divs = adapter.get_dividends("AAPL")
        assert len(divs) == 8
        for d in divs:
            assert "date" in d
            assert d["amount"] is not None

    def test_no_dividend_stock(self):
        adapter = MockAdapter()
        divs = adapter.get_dividends("TSLA")
        assert divs == []


# ===================================================================
# BaseAdapter — abstract interface
# ===================================================================

class TestBaseAdapterInterface:
    """Verify BaseAdapter defines the adapter interface via ABC."""

    def test_is_abstract(self):
        with pytest.raises(TypeError):
            BaseAdapter()

    def test_abstract_name(self):
        @property
        def name(self):
            return "fake"
        assert hasattr(BaseAdapter, "name")
        assert isinstance(BaseAdapter.__dict__["name"], property)

    def test_abstract_methods_exist(self):
        required = {
            "is_available",
            "search_securities",
            "get_security",
            "get_quotes",
            "get_price_history",
            "get_news",
            "get_dividends",
        }
        for method in required:
            assert hasattr(BaseAdapter, method), f"BaseAdapter missing {method}"

    def test_mock_implements_all(self):
        adapter = MockAdapter()
        assert adapter.name == "mock"
        assert adapter.is_available() is True
        # Call every method to confirm no NotImplementedError
        adapter.search_securities("AAPL")
        adapter.get_security("AAPL")
        adapter.get_quotes(["AAPL"])
        adapter.get_price_history("AAPL")
        adapter.get_news("AAPL")
        adapter.get_dividends("AAPL")
