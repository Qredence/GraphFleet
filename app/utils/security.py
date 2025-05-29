import re

def sanitize_search_query(query: str) -> str:
    """
    Sanitizes a search query by removing potentially harmful characters.
    Allows alphanumeric characters, spaces, periods, hyphens, and underscores.
    """
    if query is None:
        return ""
    # Remove characters that are not alphanumeric, space, period, hyphen, or underscore
    sanitized_query = re.sub(r'[^a-zA-Z0-9 ._-]', '', query)
    return sanitized_query
