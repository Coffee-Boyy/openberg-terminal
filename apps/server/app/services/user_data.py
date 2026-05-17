"""CRUD service layer for user-managed data (watchlist, portfolio, alerts)."""

from __future__ import annotations

import sqlite3
from typing import Optional

from ..database import get_db


class DuplicateError(Exception):
    """Raised when a unique constraint conflict is detected."""

    pass


# ---------------------------------------------------------------------------
# Watchlist
# ---------------------------------------------------------------------------

class WatchlistService:
    """User watchlist operations."""

    @staticmethod
    def add(ticker: str, name: Optional[str] = None) -> dict:
        ticker = ticker.upper()
        conn = get_db()
        try:
            row = conn.execute(
                "INSERT INTO watchlist (ticker, name) VALUES (?, ?) RETURNING *",
                (ticker, name),
            ).fetchone()
            conn.commit()
            return dict(row)
        except sqlite3.IntegrityError:
            raise DuplicateError(f"Ticker {ticker} already exists in watchlist")
        finally:
            conn.close()

    @staticmethod
    def remove(ticker: str) -> bool:
        ticker = ticker.upper()
        conn = get_db()
        try:
            cur = conn.execute(
                "DELETE FROM watchlist WHERE ticker = ?",
                (ticker,),
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def get_all() -> list[dict]:
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT id, ticker, name, added_at FROM watchlist ORDER BY ticker"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def search(query: str) -> list[dict]:
        query = query.upper().strip()
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT id, ticker, name, added_at FROM watchlist WHERE ticker LIKE ?",
                (f"%{query}%",),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------

class PortfolioService:
    """User portfolio operations."""

    @staticmethod
    def add_position(ticker: str, shares: float, cost: float) -> dict:
        ticker = ticker.upper()
        conn = get_db()
        try:
            row = conn.execute(
                """INSERT INTO portfolio (ticker, shares, avg_cost, current_price)
                   VALUES (?, ?, ?, 0)
                   RETURNING *""",
                (ticker, shares, cost),
            ).fetchone()
            conn.commit()
            return dict(row)
        except sqlite3.IntegrityError:
            # Merge: update existing position
            existing = conn.execute(
                "SELECT id, ticker, shares, avg_cost, current_price, added_at, updated_at "
                "FROM portfolio WHERE ticker = ?",
                (ticker,),
            ).fetchone()
            if existing:
                new_avg = (existing["shares"] * existing["avg_cost"] + shares * cost) / (
                    existing["shares"] + shares
                )
                conn.execute(
                    """UPDATE portfolio SET shares = shares + ?,
                       avg_cost = ?, updated_at = datetime('now')
                       WHERE ticker = ?""",
                    (shares, new_avg, ticker),
                )
                conn.commit()
                updated = conn.execute(
                    "SELECT id, ticker, shares, avg_cost, current_price, added_at, updated_at "
                    "FROM portfolio WHERE ticker = ?",
                    (ticker,),
                ).fetchone()
                return dict(updated)
            raise
        finally:
            conn.close()

    @staticmethod
    def update_price(ticker: str, price: float) -> Optional[dict]:
        ticker = ticker.upper()
        conn = get_db()
        try:
            cur = conn.execute(
                """UPDATE portfolio SET current_price = ?,
                       updated_at = datetime('now')
                   WHERE ticker = ?""",
                (price, ticker),
            )
            conn.commit()
            if cur.rowcount:
                return dict(
                    conn.execute(
                        "SELECT id, ticker, shares, avg_cost, current_price, added_at, updated_at "
                        "FROM portfolio WHERE ticker = ?",
                        (ticker,),
                    ).fetchone()
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all() -> list[dict]:
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT id, ticker, shares, avg_cost, current_price, added_at, updated_at "
                "FROM portfolio ORDER BY ticker"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def remove(ticker: str) -> bool:
        ticker = ticker.upper()
        conn = get_db()
        try:
            cur = conn.execute("DELETE FROM portfolio WHERE ticker = ?", (ticker,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def get_summary() -> dict:
        conn = get_db()
        try:
            row = conn.execute(
                """SELECT
                       COALESCE(SUM(shares * avg_cost), 0)    AS total_cost,
                       COALESCE(SUM(shares * current_price), 0) AS total_value,
                       COUNT(*)                                  AS position_count
                   FROM portfolio"""
            ).fetchone()
            total_cost = row["total_cost"]
            total_value = row["total_value"]
            total_pnl = total_value - total_cost
            pnl_percent = (total_pnl / total_cost * 100) if total_cost else 0.0
            return {
                "total_value": total_value,
                "total_cost": total_cost,
                "total_pnl": total_pnl,
                "pnl_percent": round(pnl_percent, 2),
                "position_count": row["position_count"],
            }
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

class AlertsService:
    """Price / volume alert operations."""

    @staticmethod
    def create(ticker: str, alert_type: str, threshold: float) -> dict:
        ticker = ticker.upper()
        conn = get_db()
        try:
            row = conn.execute(
                "INSERT INTO alerts (ticker, alert_type, threshold) VALUES (?, ?, ?)",
                (ticker, alert_type, threshold),
            )
            conn.commit()
            return dict(
                conn.execute(
                    "SELECT id, ticker, alert_type, threshold, triggered, created_at, resolved_at "
                    "FROM alerts WHERE id = ?",
                    (row.lastrowid,),
                ).fetchone()
            )
        finally:
            conn.close()

    @staticmethod
    def get_active() -> list[dict]:
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT id, ticker, alert_type, threshold, triggered, created_at, resolved_at "
                "FROM alerts WHERE triggered = 0 ORDER BY created_at"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_all() -> list[dict]:
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT id, ticker, alert_type, threshold, triggered, created_at, resolved_at "
                "FROM alerts ORDER BY created_at"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def mark_triggered(alert_id: int) -> Optional[dict]:
        conn = get_db()
        try:
            cur = conn.execute(
                """UPDATE alerts SET triggered = 1,
                       resolved_at = datetime('now')
                   WHERE id = ?""",
                (alert_id,),
            )
            conn.commit()
            if cur.rowcount:
                return dict(
                    conn.execute(
                        "SELECT id, ticker, alert_type, threshold, triggered, created_at, resolved_at "
                        "FROM alerts WHERE id = ?",
                        (alert_id,),
                    ).fetchone()
                )
            return None
        finally:
            conn.close()

    @staticmethod
    def remove(alert_id: int) -> bool:
        conn = get_db()
        try:
            cur = conn.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()
