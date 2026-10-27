import requests
from models import Book

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def search_books(query):
    """Search Open Library and return the results as Book objects."""
    params = {
        "q": query,
        "limit": 5,
        "fields": "title,author_name,first_publish_year"
    }
    response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    books = []
    for item in data["docs"]:
        book = Book(
            title=item["title"],
            author_name=item.get("author_name", ["Unknown"]),
            first_publish_year=item.get("first_publish_year")
        )
        books.append(book)
    return books
