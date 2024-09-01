from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(question: str, method: str) -> str:
    # Implement caching logic here
    pass