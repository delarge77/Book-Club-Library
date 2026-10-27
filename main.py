from fastapi import FastAPI, HTTPException

from database import get_all_catalogued_books, get_catalogued_book_by_id

app = FastAPI()


@app.get("/books")
def list_catalogued_books():
    """Return all books in the library catalogue."""
    return get_all_catalogued_books()


@app.get("/books/{book_id}")
def list_catalogued_book(book_id: int):
    """Return one book using book_id"""
    book = get_catalogued_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
