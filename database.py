import sqlite3
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "library.db"

LOAN_PERIOD_DAYS = 14


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

def get_all_members() -> list[dict]:
    """Return all members."""
    with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    member_id,
                    name,
                    email,
                    phone
                FROM members
                """
            ).fetchall()

    return [dict(row) for row in rows]

def search_members(q: str) -> list[dict]:
    """Return members whose name or email contains q."""
    search = f"%{q}%"
    with get_connection() as connection:
        rows = connection.execute(
            """
                SELECT
                    member_id,
                    name,
                    email,
                    phone
                FROM members
                WHERE name LIKE ? OR email LIKE ?
                """,
            (search, search),
        ).fetchall()

    return [dict(row) for row in rows]


def add_member( name: str, email: str, phone: str | None, password_hash: str) -> int:
    """Insert a new member and return their ID."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO members (name, email, phone, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, phone, password_hash),
        )

        return cursor.lastrowid

def get_member_by_email(email: str) -> dict | None:
    """Return a member by name, including their password hash."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT member_id, name, email, phone, password_hash
            FROM members
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    return dict(row) if row else None

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


def get_most_borrowed_books() -> list[dict]:
    """Return the books that have been borrowed the most."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                books.book_id,
                books.title,
                COUNT(loans.loan_id) AS loan_count
            FROM books
            JOIN loans
                ON loans.book_id = books.book_id
            GROUP BY books.book_id, books.title
            ORDER BY loan_count DESC, books.title
            LIMIT 10
            """
        ).fetchall()

    return [dict(row) for row in rows]


def create_loan(book_id: int, member_id: int):
    """Create loan entry using book ID and member ID"""
    loan_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=LOAN_PERIOD_DAYS)).isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO loans (book_id, member_id, loan_date, due_date)
            VALUES (?,?,?,?)
            """,
            (book_id, member_id, loan_date, due_date),
        )
    return cursor.lastrowid


def return_loan(loan_id: int):
    """return loaned book by loan_id, set return date to todays date"""
    return_date = date.today().isoformat()
    with get_connection() as connection:
        connection.execute(
            """
        UPDATE loans SET return_date = ? WHERE loan_id = ?
        """,
            (return_date, loan_id),
        )


def get_loan_by_id(loan_id: int) -> dict | None:
    """Return loan by loan_id, or None if not found"""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT loan_id, return_date FROM loans WHERE loan_id = ?""",
            (loan_id,),
        ).fetchone()
    return dict(row) if row is not None else None


def get_member_by_id(member_id: int) -> dict | None:
    """Return member by member_id, or None if not found"""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT member_id FROM members WHERE member_id = ?""",
            (member_id,),
        ).fetchone()

    return dict(row) if row is not None else None


def add_book(title: str, author_name: str, publication_year: int ) -> int:
    """Insert a new bookd and return their ID."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO books (title, author_name, publication_year)
            VALUES (?, ?, ?)
            """,
            (title, author_name, publication_year),
        )

        return cursor.lastrowid


def delete_book(book_id: int) -> bool:
    """Delete a book by ID. Return True if deleted, False if not found."""
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM books
            WHERE book_id = ?
            """,
            (book_id,),
        )
    return cursor.rowcount > 0

def update_book_by_id(book_id: int, update_data: dict) -> dict | None:

    allowed_fields = {
        "title",
        "author_name",
        "publication_year",
    }

    update_data = {
        key: value
        for key, value in update_data.items()
        if key in allowed_fields
    }

    if not update_data:
        return None

    with get_connection() as connection:
        # Check whether the book exists.
        existing_book = connection.execute(
            "SELECT book_id FROM books WHERE book_id = ?",
            (book_id,)
        ).fetchone()

        if existing_book is None:
            return None

        # Update only the supplied fields.
        fields = ", ".join(
            f"{field} = ?" for field in update_data
        )
        values = list(update_data.values()) + [book_id]

        connection.execute(
            f"UPDATE books SET {fields} WHERE book_id = ?",
            values
        )

        row = connection.execute(
            "SELECT * FROM books WHERE book_id = ?",
            (book_id,)
        ).fetchone()

        return dict(row)
