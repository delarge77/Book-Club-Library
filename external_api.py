import requests
from models import Book

OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


def search_books(query):
    """Search Open Library and return the results as Book objects."""

    if not query.strip():
        print("Please type something to search for.")
        return None

    params = {
        "q": query,
        "limit": 5,
        "fields": "title,author_name,first_publish_year"
    }
    try:
        response = requests.get(OPEN_LIBRARY_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Open Library took too long. Try again later.")
        return None
    except requests.exceptions.ConnectionError:
        print("Could not connect to Open Library. Check your Internet.")
        return None
    except requests.exceptions.HTTPError:
        print("Open Library had a problem. Try again later.")
        return None
    data = response.json()

    books = []
    for item in data["docs"]:
        book = Book(
            title=item["title"],
            author_name=item.get("author_name", ["Unknown"]),
            first_publish_year=item.get("first_publish_year")
        )
        books.append(book)

    if not books:
        print(f"No books found for '{query}'.")
    else:
        print(f"Found {len(books)} books.")
    return books
