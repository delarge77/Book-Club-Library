from pathlib import Path

from database import DATABASE_PATH, get_connection


BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


AUTHORS = [
    ("Jane Austen",),
    ("George Orwell",),
    ("Mary Shelley",),
    ("Neil Gaiman",),
    ("Terry Pratchett",),
]

BOOKS = [
    ("Pride and Prejudice", "author_name_1", 1813),
    ("Nineteen Eighty-Four", "author_name_2", 1949),
    ("Frankenstein", "author_name_3", 1818),
    ("Good Omens", "author_name_4", 1990),
]

MEMBERS = [
    (
        "Alex Andersson",
        "alex@example.com",
        "0701112233",
        "$argon2id$v=19$m=65536,t=3,p=4$3Hq9BXYaN3JsnkmcltfWHA$paZBNkRUUq1EjcVbEo/qlp/aLKh47T/UEFJ0CzfU5fU",
    ),
    (
        "Sam Berg",
        "sam@example.com",
        None,
        "$argon2id$v=19$m=65536,t=3,p=4$7DejaYqYc3VGNL+Loxq8WA$hYVOc2TdaMj6MNouniDqIfLHeMen6Y1TL6z/+OkXqEE",
    ),
    (
        "Robin Carlsson",
        "robin@example.com",
        "0704445566",
        "$argon2id$v=19$m=65536,t=3,p=4$lHGI+nuMnCUE+MkLW1JLYg$6w2khIuj85cim88Nhi3FzUqz3I7c35akMnznK4Gz/xo",
    ),
]


def recreate_database() -> None:
    """Delete the old database and create a new empty database."""
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
        print(f"Deleted existing database: {DATABASE_PATH.name}")

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.executescript(schema)

    print(f"Created database schema: {DATABASE_PATH.name}")


def seed_authors(connection) -> None:
    """Insert sample authors."""
    connection.executemany(
        """
        INSERT INTO authors (name)
        VALUES (?)
        """,
        AUTHORS,
    )


def seed_books(connection) -> None:
    """Insert sample books."""
    connection.executemany(
        """
        INSERT INTO books (title, author_name, publication_year)
        VALUES (?, ?, ?)
        """,
        BOOKS,
    )


def seed_book_authors(connection) -> None:
    """Connect sample books with their authors."""
    book_authors = [
        (1, 1),  # Pride and Prejudice — Jane Austen
        (2, 2),  # Nineteen Eighty-Four — George Orwell
        (3, 3),  # Frankenstein — Mary Shelley
        (4, 4),  # Good Omens — Neil Gaiman
        (4, 5),  # Good Omens — Terry Pratchett
    ]

    connection.executemany(
        """
        INSERT INTO book_authors (book_id, author_id)
        VALUES (?, ?)
        """,
        book_authors,
    )


def seed_members(connection) -> None:
    """Insert sample library members."""
    connection.executemany(
        """
        INSERT INTO members (name, email, phone, password_hash)
        VALUES (?, ?, ?,?)
        """,
        MEMBERS,
    )


def seed_loans(connection) -> None:
    """Insert historical and active sample loans."""
    loans = [
        (
            1,
            1,
            "2026-09-01",
            "2026-09-15",
            "2026-09-12",
        ),
        (
            2,
            2,
            "2026-10-10",
            "2026-10-24",
            None,
        ),
        (
            3,
            1,
            "2026-10-20",
            "2026-11-03",
            None,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO loans (
            book_id,
            member_id,
            loan_date,
            due_date,
            return_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        loans,
    )


def seed_database() -> None:
    """Populate the database with representative test data."""
    with get_connection() as connection:
        seed_authors(connection)
        seed_books(connection)
        seed_book_authors(connection)
        seed_members(connection)
        seed_loans(connection)

    print("Inserted sample authors, books, members, and loans.")


def verify_database() -> None:
    """Display row counts to verify the seed operation."""
    tables = [
        "authors",
        "books",
        "book_authors",
        "members",
        "loans",
    ]

    with get_connection() as connection:
        for table in tables:
            result = connection.execute(
                f"SELECT COUNT(*) AS count FROM {table}"
            ).fetchone()

            print(f"{table}: {result['count']} rows")


def main() -> None:
    """Rebuild and seed the development database."""
    recreate_database()
    seed_database()
    verify_database()
    print("Database setup completed successfully.")


if __name__ == "__main__":
    main()