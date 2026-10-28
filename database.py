from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "library.db"


def get_connection() -> sqlite3.Connection:
    """Create and configure a new SQLite connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def get_all_catalogued_books() -> list[dict]:
    """Return all catalogued books."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                book_id,
                title,
                publication_year
            FROM books
            ORDER BY title
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_catalogued_book_by_id(book_id: int) -> dict | None:
    """Return a catalogued book by ID, or None if not found."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                book_id,
                title,
                publication_year
            FROM books
            WHERE book_id = ?
            """,
            (book_id,),
        ).fetchone()

    return dict(row) if row is not None else None


def get_never_borrowed_books() -> list[dict]:
    """Return books that have never been borrowed."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                books.book_id,
                books.title,
                books.publication_year
            FROM books
            LEFT JOIN loans
                ON loans.book_id = books.book_id
            WHERE loans.loan_id IS NULL
            ORDER BY books.title
            """
        ).fetchall()

    return [dict(row) for row in rows]
