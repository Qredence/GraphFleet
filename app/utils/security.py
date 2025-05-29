import re

def sanitize_search_query(query: str) -> str:
    """
    Sanitizes a search query by removing potentially harmful characters.
    Allows alphanumeric characters, spaces, periods, hyphens, and underscores.
    """
    if query is None:
        return ""
    # Use the compiled regex pattern to remove unwanted characters
    sanitized_query = SANITIZE_PATTERN.sub('', query)
    return sanitized_query
