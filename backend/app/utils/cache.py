from functools import lru_cache
from app.utils.context_builder import create_context_builder

@lru_cache(maxsize=1)
def get_context_builder():
    return create_context_builder()