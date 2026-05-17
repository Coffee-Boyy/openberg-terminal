"""Base data adapter interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class AdapterError(Exception):
    """Raised when a data adapter operation fails."""
    pass


class BaseAdapter(ABC):
    """Abstract interface for data provider adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Adapter identifier."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if adapter can be used (API key, network, etc.)."""
        ...

    @abstractmethod
    def search_securities(self, query: str) -> list[dict[str, Any]]:
        """Search securities by ticker or name."""
        ...

    @abstractmethod
    def get_security(self, ticker: str) -> dict[str, Any]:
        """Get security description."""
        ...

    @abstractmethod
    def get_quotes(self, tickers: list[str]) -> list[dict[str, Any]]:
        """Get real-time quotes."""
        ...

    @abstractmethod
    def get_price_history(
        self, ticker: str, interval: str = "1d", count: int = 200
    ) -> list[dict[str, Any]]:
        """Get historical price bars."""
        ...

    @abstractmethod
    def get_news(
        self, ticker: Optional[str] = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get news feed."""
        ...

    @abstractmethod
    def get_dividends(self, ticker: str) -> list[dict[str, Any]]:
        """Get dividend history."""
        ...
