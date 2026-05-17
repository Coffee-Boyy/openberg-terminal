"""Tests for user-data services (watchlist, portfolio, alerts) against SQLite.

Each test gets its own isolated database via the ``_fresh`` autouse fixture
which patches ``app.database.DB_PATH`` to a unique temp file.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

import app.database as db_mod

from app.services.user_data import DuplicateError


# ===================================================================
# Autouse fixture: every test in this module gets a fresh database
# ===================================================================


@pytest.fixture(autouse=True)
def _fresh(tmp_path):
    """Patch DB_PATH to a per-test temp file and initialise tables."""
    db_path = tmp_path / "test.db"
    db_mod.DB_PATH = db_path
    db_mod.init_db()
    yield db_path


# ===================================================================
# WatchlistService CRUD
# ===================================================================


class TestWatchlistService:
    def test_add(self):
        from app.services.user_data import WatchlistService

        row = WatchlistService.add("AAPL", "Apple Inc.")
        assert row["ticker"] == "AAPL"
        assert row["name"] == "Apple Inc."
        assert row["id"] is not None
        assert row["added_at"] is not None

    def test_add_uppercase_normalization(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("aapl", "Apple")
        items = WatchlistService.get_all()
        assert items[0]["ticker"] == "AAPL"

    def test_add_duplicate_raises(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("AAPL")
        with pytest.raises(DuplicateError, match="already exists"):
            WatchlistService.add("AAPL")

    def test_get_all_empty(self):
        from app.services.user_data import WatchlistService

        assert WatchlistService.get_all() == []

    def test_get_all(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("AAPL")
        WatchlistService.add("MSFT")
        items = WatchlistService.get_all()
        assert len(items) == 2
        tickers = {i["ticker"] for i in items}
        assert tickers == {"AAPL", "MSFT"}

    def test_remove_existing(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("AAPL")
        assert WatchlistService.remove("AAPL") is True
        assert WatchlistService.get_all() == []

    def test_remove_nonexistent(self):
        from app.services.user_data import WatchlistService

        assert WatchlistService.remove("NOPE") is False

    def test_search_match(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("AAPL")
        WatchlistService.add("MSFT")
        WatchlistService.add("GOOG")
        results = WatchlistService.search("AAPL")
        assert len(results) == 1
        assert results[0]["ticker"] == "AAPL"

    def test_search_case_insensitive(self):
        from app.services.user_data import WatchlistService

        WatchlistService.add("AAPL")
        results = WatchlistService.search("aapl")
        assert len(results) == 1


# ===================================================================
# PortfolioService CRUD
# ===================================================================


class TestPortfolioService:
    def test_add_position(self):
        from app.services.user_data import PortfolioService

        pos = PortfolioService.add_position("AAPL", 10.0, 150.0)
        assert pos["ticker"] == "AAPL"
        assert pos["shares"] == 10.0
        assert pos["avg_cost"] == 150.0
        assert pos["current_price"] == 0

    def test_add_merge_same_ticker(self):
        """Adding an existing ticker merges shares and averages cost."""
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 10.0, 150.0)
        pos = PortfolioService.add_position("AAPL", 10.0, 160.0)
        assert pos["shares"] == 20.0
        # Weighted avg: (10*150 + 10*160) / 20 = 155.0
        assert pos["avg_cost"] == pytest.approx(155.0)

    def test_add_merge_different_costs(self):
        """Merge with unequal shares and costs."""
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 100.0, 100.0)
        pos = PortfolioService.add_position("AAPL", 100.0, 120.0)
        assert pos["shares"] == 200.0
        # (100*100 + 100*120) / 200 = 110.0
        assert pos["avg_cost"] == pytest.approx(110.0)

    def test_get_all_empty(self):
        from app.services.user_data import PortfolioService

        assert PortfolioService.get_all() == []

    def test_get_all(self):
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 10.0, 150.0)
        PortfolioService.add_position("MSFT", 5.0, 300.0)
        positions = PortfolioService.get_all()
        assert len(positions) == 2

    def test_remove_existing(self):
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 10.0, 150.0)
        assert PortfolioService.remove("AAPL") is True
        assert PortfolioService.get_all() == []

    def test_remove_nonexistent(self):
        from app.services.user_data import PortfolioService

        assert PortfolioService.remove("NOPE") is False

    def test_update_price_existing(self):
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 10.0, 150.0)
        pos = PortfolioService.update_price("AAPL", 155.0)
        assert pos is not None
        assert pos["current_price"] == 155.0

    def test_update_price_nonexistent(self):
        from app.services.user_data import PortfolioService

        result = PortfolioService.update_price("NOPE", 100.0)
        assert result is None

    def test_summary_empty(self):
        from app.services.user_data import PortfolioService

        summary = PortfolioService.get_summary()
        assert summary["total_cost"] == 0
        assert summary["total_value"] == 0
        assert summary["total_pnl"] == 0
        assert summary["pnl_percent"] == 0.0
        assert summary["position_count"] == 0

    def test_summary(self):
        from app.services.user_data import PortfolioService

        PortfolioService.add_position("AAPL", 10.0, 150.0)
        PortfolioService.update_price("AAPL", 155.0)
        summary = PortfolioService.get_summary()
        assert summary["position_count"] == 1
        assert summary["total_cost"] == 1500.0
        assert summary["total_value"] == 1550.0
        assert summary["total_pnl"] == 50.0
        assert summary["pnl_percent"] == pytest.approx(3.33, rel=0.01)


# ===================================================================
# AlertsService CRUD
# ===================================================================


class TestAlertsService:
    def test_create(self):
        from app.services.user_data import AlertsService

        alert = AlertsService.create("AAPL", "price_above", 200.0)
        assert alert["ticker"] == "AAPL"
        assert alert["alert_type"] == "price_above"
        assert alert["threshold"] == 200.0
        assert alert["triggered"] == 0
        assert alert["id"] is not None

    def test_get_active(self):
        from app.services.user_data import AlertsService

        AlertsService.create("AAPL", "price_above", 200.0)
        AlertsService.create("MSFT", "price_below", 250.0)
        active = AlertsService.get_active()
        assert len(active) == 2
        for a in active:
            assert a["triggered"] == 0

    def test_get_all(self):
        from app.services.user_data import AlertsService

        AlertsService.create("AAPL", "price_above", 200.0)
        all_alerts = AlertsService.get_all()
        assert len(all_alerts) == 1

    def test_mark_triggered(self):
        from app.services.user_data import AlertsService

        alert = AlertsService.create("AAPL", "price_above", 200.0)
        updated = AlertsService.mark_triggered(alert["id"])
        assert updated is not None
        assert updated["triggered"] == 1
        assert updated["resolved_at"] is not None

    def test_mark_triggered_nonexistent(self):
        from app.services.user_data import AlertsService

        result = AlertsService.mark_triggered(99999)
        assert result is None

    def test_remove_existing(self):
        from app.services.user_data import AlertsService

        alert = AlertsService.create("AAPL", "price_above", 200.0)
        assert AlertsService.remove(alert["id"]) is True

    def test_remove_nonexistent(self):
        from app.services.user_data import AlertsService

        assert AlertsService.remove(99999) is False

    def test_triggered_not_in_active(self):
        """Marked alerts should not appear in get_active()."""
        from app.services.user_data import AlertsService

        alert = AlertsService.create("AAPL", "price_above", 200.0)
        AlertsService.mark_triggered(alert["id"])
        active = AlertsService.get_active()
        assert len(active) == 0

    def test_create_uppercase_ticker(self):
        from app.services.user_data import AlertsService

        alert = AlertsService.create("aapl", "price_above", 200.0)
        assert alert["ticker"] == "AAPL"
