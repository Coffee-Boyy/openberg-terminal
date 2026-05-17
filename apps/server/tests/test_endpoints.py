"""Integration tests for FastAPI endpoints using Starlette TestClient.

Every test gets a fresh database via the ``_test_client`` fixture,
which patches ``app.database.DB_PATH`` to a temp file, creates the
TestClient (lifespan runs once per test), and cleans up after.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

import app.database as db_mod
from app.main import app


# ===================================================================
# Fixture: one temp DB + TestClient per test
# ===================================================================


@pytest.fixture
def test_client():
    """Create a TestClient pointing at a fresh temp DB.

    The lifespan (init_db) fires when the client is created, so we
    patch DB_PATH *before* instantiating the client.  The DB file
    is cleaned up in the fixture teardown.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    temp_path = Path(tmp.name)

    db_mod.DB_PATH = temp_path

    from starlette.testclient import TestClient

    with TestClient(app) as client:
        yield client

    # Cleanup
    for ext in [".db", ".db-wal", ".db-shm"]:
        temp_path.with_suffix(ext).unlink(missing_ok=True)


# ===================================================================
# Health
# ===================================================================


class TestHealth:
    def test_health_ok(self, test_client):
        r = test_client.get("/api/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert body["version"] == "0.1.0"


# ===================================================================
# Securities search
# ===================================================================


class TestSearchSecurities:
    def test_search_all(self, test_client):
        r = test_client.get("/api/securities")
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 10
        for item in data:
            assert "ticker" in item
            assert "name" in item

    def test_search_filter(self, test_client):
        r = test_client.get("/api/securities", params={"q": "aapl"})
        assert r.status_code == 200
        data = r.json()
        assert any(s["ticker"] == "AAPL" for s in data)


# ===================================================================
# Security detail
# ===================================================================


class TestGetSecurity:
    def test_known_security(self, test_client):
        r = test_client.get("/api/securities/AAPL")
        assert r.status_code == 200
        sec = r.json()
        assert sec["ticker"] == "AAPL"
        assert sec["name"] == "Apple Inc."

    def test_unknown_security(self, test_client):
        r = test_client.get("/api/securities/NOPE")
        assert r.status_code == 200
        sec = r.json()
        assert sec["ticker"] == "NOPE"


# ===================================================================
# Quotes
# ===================================================================


class TestQuotes:
    def test_single_quote(self, test_client):
        r = test_client.get("/api/quotes", params={"tickers": "AAPL"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        q = data[0]
        assert q["ticker"] == "AAPL"
        assert q["last"] is not None

    def test_multiple_quotes(self, test_client):
        r = test_client.get("/api/quotes", params={"tickers": "AAPL,MSFT"})
        assert r.status_code == 200
        data = r.json()
        tickers = {q["ticker"] for q in data}
        assert tickers == {"AAPL", "MSFT"}


# ===================================================================
# Historical prices
# ===================================================================


class TestPrices:
    def test_historical(self, test_client):
        r = test_client.get("/api/prices/AAPL", params={"count": 10})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 10
        for bar in data:
            assert "time" in bar
            assert bar["open"] is not None
            assert bar["close"] is not None

    def test_interval(self, test_client):
        r = test_client.get(
            "/api/prices/AAPL",
            params={"interval": "1h", "count": 5},
        )
        assert r.status_code == 200
        assert len(r.json()) == 5


# ===================================================================
# News
# ===================================================================


class TestNews:
    def test_general_news(self, test_client):
        r = test_client.get("/api/news", params={"limit": 3})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        for a in data:
            assert "headline" in a
            assert "id" in a

    def test_ticker_news(self, test_client):
        r = test_client.get("/api/news", params={"ticker": "AAPL"})
        assert r.status_code == 200
        data = r.json()
        for a in data:
            assert "AAPL" in a["tickers"]


# ===================================================================
# Dividends
# ===================================================================


class TestDividends:
    def test_dividend_paying(self, test_client):
        r = test_client.get("/api/dividends/AAPL")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 8
        for d in data:
            assert "date" in d
            assert d["amount"] is not None

    def test_no_dividend(self, test_client):
        r = test_client.get("/api/dividends/TSLA")
        assert r.status_code == 200
        data = r.json()
        assert data == []


# ===================================================================
# Watchlist endpoints
# ===================================================================


class TestWatchlistEndpoints:
    def test_add_and_list(self, test_client):
        r = test_client.post(
            "/api/watchlist",
            json={"ticker": "AAPL", "name": "Apple"},
        )
        assert r.status_code == 201
        body = r.json()
        assert body["ticker"] == "AAPL"
        assert body["name"] == "Apple"
        assert "id" in body
        assert "added_at" in body

        r = test_client.get("/api/watchlist")
        assert r.status_code == 200
        items = r.json()
        assert any(i["ticker"] == "AAPL" for i in items)

    def test_add_duplicate_409(self, test_client):
        test_client.post("/api/watchlist", json={"ticker": "AAPL"})
        r = test_client.post("/api/watchlist", json={"ticker": "AAPL"})
        assert r.status_code == 409

    def test_remove(self, test_client):
        test_client.post("/api/watchlist", json={"ticker": "AAPL"})
        r = test_client.delete("/api/watchlist", params={"ticker": "AAPL"})
        assert r.status_code == 204
        items = test_client.get("/api/watchlist").json()
        assert not any(i["ticker"] == "AAPL" for i in items)

    def test_remove_missing_404(self, test_client):
        r = test_client.delete("/api/watchlist", params={"ticker": "NOPE"})
        assert r.status_code == 404


# ===================================================================
# Portfolio endpoints
# ===================================================================


class TestPortfolioEndpoints:
    def test_add_position(self, test_client):
        r = test_client.post(
            "/api/portfolio",
            json={"ticker": "AAPL", "shares": 10, "cost": 150.0},
        )
        assert r.status_code == 201
        body = r.json()
        assert body["ticker"] == "AAPL"
        assert body["shares"] == 10
        assert body["avg_cost"] == 150.0

    def test_list_portfolio(self, test_client):
        test_client.post(
            "/api/portfolio",
            json={"ticker": "AAPL", "shares": 10, "cost": 150.0},
        )
        r = test_client.get("/api/portfolio")
        assert r.status_code == 200
        positions = r.json()
        assert any(p["ticker"] == "AAPL" for p in positions)

    def test_summary(self, test_client):
        test_client.post(
            "/api/portfolio",
            json={"ticker": "AAPL", "shares": 10, "cost": 150.0},
        )
        r = test_client.get("/api/portfolio/summary")
        assert r.status_code == 200
        body = r.json()
        assert body["position_count"] >= 1
        assert body["total_cost"] > 0
        assert "total_pnl" in body
        assert "pnl_percent" in body

    def test_update_price(self, test_client):
        test_client.post(
            "/api/portfolio",
            json={"ticker": "AAPL", "shares": 10, "cost": 150.0},
        )
        r = test_client.patch(
            "/api/portfolio/AAPL/price",
            json={"price": 155.0},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["current_price"] == 155.0

    def test_remove_position(self, test_client):
        test_client.post(
            "/api/portfolio",
            json={"ticker": "AAPL", "shares": 10, "cost": 150.0},
        )
        r = test_client.delete("/api/portfolio", params={"ticker": "AAPL"})
        assert r.status_code == 204

    def test_remove_missing_404(self, test_client):
        r = test_client.delete("/api/portfolio", params={"ticker": "NOPE"})
        assert r.status_code == 404


# ===================================================================
# Alerts endpoints
# ===================================================================


class TestAlertEndpoints:
    def test_create(self, test_client):
        r = test_client.post(
            "/api/alerts",
            json={
                "ticker": "AAPL",
                "alert_type": "price_above",
                "threshold": 200.0,
            },
        )
        assert r.status_code == 201
        body = r.json()
        assert body["ticker"] == "AAPL"
        assert body["alert_type"] == "price_above"
        assert body["threshold"] == 200.0
        assert body["triggered"] == 0

    def test_list(self, test_client):
        test_client.post(
            "/api/alerts",
            json={
                "ticker": "AAPL",
                "alert_type": "price_above",
                "threshold": 200.0,
            },
        )
        r = test_client.get("/api/alerts")
        assert r.status_code == 200
        alerts = r.json()
        assert any(a["ticker"] == "AAPL" for a in alerts)

    def test_remove(self, test_client):
        r = test_client.post(
            "/api/alerts",
            json={
                "ticker": "AAPL",
                "alert_type": "price_above",
                "threshold": 200.0,
            },
        )
        alert = r.json()
        alert_id = alert["id"]
        r = test_client.delete("/api/alerts", params={"alert_id": alert_id})
        assert r.status_code == 204

    def test_remove_missing_404(self, test_client):
        r = test_client.delete("/api/alerts", params={"alert_id": 99999})
        assert r.status_code == 404
