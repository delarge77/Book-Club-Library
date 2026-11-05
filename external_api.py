from api_client import get_json
from models import ExternalBook

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
    
    response = get_json(OPEN_LIBRARY_URL, params=params, timeout=5)

    if response is None:
            return None
    
    books = []
    for item in response["docs"]:
        book = ExternalBook( 
            title=item["title"], 
            #This handles both a missing field and a None value.
            author_name=item.get("author_name") or ["Unknown"],
            first_publish_year=item.get("first_publish_year"))
        books.append(book)

    if not books:
        print(f"No books found for '{query}'.")
    else:
        print(f"Found {len(books)} books.")
    return books
