"""WebSocket endpoint for live quote streaming."""

import asyncio
import logging

from fastapi import WebSocket, Query

from app.models import QuoteSchema

logger = logging.getLogger(__name__)

# Interval (seconds) between quote pushes
QUOTE_INTERVAL = 30


def get_available_adapters() -> list[str]:
    """Return names of all adapters that report themselves available."""
    from app.adapters.yahoo import YahooAdapter
    from app.adapters.finnhub import FinnhubAdapter
    from app.adapters.mock import MockAdapter

    available: list[str] = []
    for cls in (YahooAdapter, FinnhubAdapter):
        instance = cls()
        if instance.is_available():
            available.append(instance.name)
    # MockAdapter is always available as the final fallback
    available.append(MockAdapter().name)
    return available


async def ws_quotes(
    websocket: WebSocket,
    tickers: str = Query(default="", description="Comma-separated ticker list"),
):
    """Stream live quotes to the client every *QUOTE_INTERVAL* seconds."""

    await websocket.accept()

    # Parse ticker list
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if not ticker_list:
        await websocket.send_json({
            "type": "quotes",
            "quotes": [],
            "detail": "No tickers provided; send ?tickers=AAPL,MSFT",
        })
        await websocket.close()
        return

    disconnect_event = asyncio.Event()

    async def _send_loop():
        """Background loop that fetches and pushes quotes until disconnect."""
        from app.services.data import QuoteService

        while True:
            try:
                raw = QuoteService.get_batch(ticker_list)
                quotes = [
                    QuoteSchema.model_validate(q).model_dump(mode="json")
                    for q in (raw or [])
                ]
                await websocket.send_json({
                    "type": "quotes",
                    "quotes": quotes,
                })
            except Exception:
                # Any send error (closed socket, etc.) breaks the loop
                logger.debug("WebSocket quote push failed — exiting loop")
                break
            else:
                # Wait for the next interval or early-cancel from disconnect
                try:
                    await asyncio.wait_for(
                        disconnect_event.wait(),
                        timeout=QUOTE_INTERVAL,
                    )
                    # Event was set — client disconnected
                    return
                except asyncio.TimeoutError:
                    # Normal interval elapsed — continue looping
                    pass

    task = asyncio.create_task(_send_loop())

    try:
        # Wait for a client-sent close message; FastAPI closes the WS
        # automatically when this coroutine returns.
        while True:
            msg = await websocket.receive_text()
            logger.debug(f"Received client message: {msg!r}")
    except Exception:
        pass  # Client disconnected
    finally:
        disconnect_event.set()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
