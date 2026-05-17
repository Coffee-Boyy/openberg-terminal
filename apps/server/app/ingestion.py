"""Scheduled data ingestion — snapshot quotes into SQLite."""

import asyncio
import logging

import aiosqlite

from .database import DB_PATH
from .services.data import QuoteService

logger = logging.getLogger(__name__)


class IngestionService:
    """Persist quote snapshots for offline / historical use."""

    @staticmethod
    async def snapshot(tickers: list[str]) -> int:
        """Fetch quotes and store each in market_history. Returns rows written."""
        quotes = QuoteService.get_batch(tickers) or []
        if not quotes:
            return 0

        conn = await aiosqlite.connect(str(DB_PATH))
        try:
            for q in quotes:
                await conn.execute(
                    "INSERT OR REPLACE INTO market_history "
                    "(ticker, price, change, change_percent, volume, timestamp) "
                    "VALUES (?, ?, ?, ?, ?, datetime('now'))",
                    (
                        q.get("ticker", ""),
                        q.get("last", 0),
                        q.get("change", 0),
                        q.get("changePercent", 0),
                        q.get("volume", 0),
                    ),
                )
            await conn.commit()
            return len(quotes)
        finally:
            await conn.close()

    @staticmethod
    async def history(ticker: str, days: int = 30) -> list[dict]:
        """Retrieve historical snapshots for a ticker."""
        conn = await aiosqlite.connect(str(DB_PATH))
        try:
            cursor = await conn.execute(
                "SELECT ticker, price, change, change_percent, volume, timestamp "
                "FROM market_history "
                "WHERE ticker = ? AND timestamp >= datetime('now', ?) "
                "ORDER BY timestamp",
                (ticker.upper(), f"-{days} days"),
            )
            rows = await cursor.fetchall()
            return [
                dict(zip(["ticker", "price", "change", "change_percent", "volume", "timestamp"], r))
                for r in rows
            ]
        finally:
            await conn.close()

    @staticmethod
    async def latest(tickers: list[str]) -> list[dict]:
        """Get the most recent snapshot per ticker."""
        if not tickers:
            return []
        conn = await aiosqlite.connect(str(DB_PATH))
        try:
            placeholders = ",".join(["?"] * len(tickers))
            sql = (
                "SELECT mh.* FROM market_history mh "
                f"INNER JOIN (SELECT ticker, MAX(timestamp) AS ts FROM market_history "
                f"WHERE ticker IN ({placeholders}) GROUP BY ticker) latest "
                "ON mh.ticker = latest.ticker AND mh.timestamp = latest.ts "
                "ORDER BY mh.ticker"
            )
            cursor = await conn.execute(sql, [t.upper() for t in tickers])
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            await conn.close()


async def run_loop():
    """Background loop: snapshot quotes every 60 seconds."""
    default_tickers = [
        "AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NVDA",
        "META", "JPM", "V", "WMT", "SPY", "BTC", "EURUSD",
    ]
    logger.info("Ingestion loop started")
    while True:
        try:
            count = await IngestionService.snapshot(default_tickers)
            logger.debug("Snapshot: %d quotes stored", count)
        except Exception as e:
            logger.error("Ingestion snapshot failed: %s", e)
        await asyncio.sleep(60)
