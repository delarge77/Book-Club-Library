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


def get_member_by_id(member_id: int) -> dict | None:
    """Return member by member_id, or None if not found"""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT member_id FROM members WHERE member_id = ?""",
            (member_id,),
        ).fetchone()

    return dict(row) if row is not None else None
