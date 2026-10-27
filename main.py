from fastapi import FastAPI
from database import get_all_catalogued_books

app = FastAPI()


@app.get("/books")
def list_catalogued_books():
    """Return all books in the library catalogue."""
    return get_all_catalogued_books()
