"""Cache utilities for GraphFleet."""
import asyncio
from typing import Any, Optional
import json
from pathlib import Path
import time

class Cache:
    """Simple file-based cache implementation."""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache = {}
        self._lock = asyncio.Lock()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a key."""
        return self.cache_dir / f"{hash(key)}.json"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        async with self._lock:
            # Check memory cache first
            if key in self._cache:
                value, expiry = self._cache[key]
                if expiry > time.time():
                    return value
                del self._cache[key]
            
            # Check file cache
            cache_path = self._get_cache_path(key)
            if cache_path.exists():
                try:
                    data = json.loads(cache_path.read_text())
                    if data["expiry"] > time.time():
                        self._cache[key] = (data["value"], data["expiry"])
                        return data["value"]
                    cache_path.unlink()
                except (json.JSONDecodeError, KeyError):
                    if cache_path.exists():
                        cache_path.unlink()
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set a value in the cache with TTL in seconds."""
        async with self._lock:
            expiry = time.time() + ttl
            # Update memory cache
            self._cache[key] = (value, expiry)
            
            # Update file cache
            cache_path = self._get_cache_path(key)
            try:
                cache_data = {
                    "value": value,
                    "expiry": expiry
                }
                cache_path.write_text(json.dumps(cache_data))
            except (TypeError, OSError) as e:
                print(f"Failed to write to cache: {e}")
    
    async def clear(self) -> None:
        """Clear all cached data."""
        async with self._lock:
            self._cache.clear()
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_file.unlink()
                except OSError:
                    pass

# Global cache instance
_cache = Cache()

async def get_cache(key: str) -> Optional[Any]:
    """Get a value from the global cache."""
    return await _cache.get(key)

async def set_cache(key: str, value: Any, ttl: int = 3600) -> None:
    """Set a value in the global cache."""
    await _cache.set(key, value, ttl)

async def clear_cache() -> None:
    """Clear the global cache."""
    await _cache.clear() 