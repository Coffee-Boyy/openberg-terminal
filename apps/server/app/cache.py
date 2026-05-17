"""In-memory LRU cache with per-key TTL and a service-method decorator."""

from __future__ import annotations

import datetime
import threading
from collections import OrderedDict
from functools import wraps
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# Cache TTL defaults (seconds) keyed by data category
# ---------------------------------------------------------------------------

CACHE_TTL: dict[str, int] = {
    "quote": 10,
    "price": 60,
    "news": 60,
    "security": 300,
    "dividend": 300,
}


# ---------------------------------------------------------------------------
# TTLCache — thread-safe LRU cache with per-key TTL
# ---------------------------------------------------------------------------


class TTLCache:
    """Thread-safe, maxsize-bounded LRU cache with per-key TTL expiry."""

    def __init__(self, maxsize: int = 512, default_ttl: Optional[int] = None) -> None:
        self._maxsize = maxsize
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, Any] = OrderedDict()
        self._expiry: dict[str, datetime.datetime] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Any:
        """Return the cached value for *key* if present and not expired."""
        with self._lock:
            if key not in self._store:
                return None
            if self._is_expired(key):
                self._remove(key)
                return None
            value = self._store[key]
            self._store.move_to_end(key)
            return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store *value* under *key*, evicting the LRU entry if at capacity."""
        effective_ttl = ttl if ttl is not None else self._default_ttl
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            else:
                while len(self._store) >= self._maxsize:
                    self._store.popitem(last=False)
            self._store[key] = value
            if effective_ttl is not None:
                self._expiry[key] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=effective_ttl)

    def invalidate(self, key: str) -> None:
        """Remove *key* from the cache."""
        with self._lock:
            self._remove(key)

    def clear(self) -> None:
        """Evict all entries."""
        with self._lock:
            self._store.clear()
            self._expiry.clear()

    # -- internal helpers ---------------------------------------------------

    def _is_expired(self, key: str) -> bool:
        """Check whether *key* has passed its TTL (must hold lock)."""
        if key not in self._expiry:
            return False
        return datetime.datetime.now(datetime.timezone.utc) > self._expiry[key]

    def _remove(self, key: str) -> None:
        """Remove *key* from store and expiry tracking (must hold lock)."""
        self._store.pop(key, None)
        self._expiry.pop(key, None)


# ---------------------------------------------------------------------------
# cached_service decorator
# ---------------------------------------------------------------------------


def _make_cache_key(method_name: str, args: tuple, kwargs: dict) -> str:
    """Build a deterministic cache key from positional and keyword arguments."""

    def _serialize(val: Any) -> str:
        if isinstance(val, dict):
            parts = ",".join(f"{k}={_serialize(v)}" for k, v in sorted(val.items()))
            return f"{{{parts}}}"
        if isinstance(val, (list, tuple)):
            return "[" + ",".join(_serialize(item) for item in val) + "]"
        return str(val)

    positional = ",".join(_serialize(a) for a in args)
    kw = ",".join(f"{k}={_serialize(v)}" for k, v in sorted(kwargs.items()))
    parts = ",".join(filter(None, [positional, kw]))
    return f"{method_name}({parts})"


def cached_service(method_name: str, ttl: int) -> Callable:
    """Return a decorator that wraps a service method with cache lookup/miss logic."""

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache = get_cache()
            key = _make_cache_key(method_name, args, kwargs)
            cached = cache.get(key)
            if cached is not None:
                return cached
            result = fn(*args, **kwargs)
            cache.set(key, result, ttl=ttl)
            return result

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Singleton cache instance
# ---------------------------------------------------------------------------

_cache_instance: Optional[TTLCache] = None


def get_cache() -> TTLCache:
    """Return the shared cache instance (lazy singleton)."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = TTLCache()
    return _cache_instance


def reset_cache() -> None:
    """Reset the singleton cache (useful for tests)."""
    global _cache_instance
    _cache_instance = None
