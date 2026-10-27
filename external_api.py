import requests

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def search_books(query):
    """Search Open Library for books by title, author or ISBN."""
    params = {
        "q": query,
        "limit": 5,
        "fields": "title,author_name,first_publish_year"
    }
    response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=5)
    response.raise_for_status()
    return response.json()
