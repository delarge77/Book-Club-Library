PRAGMA foreign_keys = ON;

CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    publication_year INTEGER,
    CHECK (
        publication_year IS NULL
        OR publication_year > 0
    )
);

CREATE TABLE book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,

    PRIMARY KEY (book_id, author_id),

    FOREIGN KEY (book_id)
        REFERENCES books(book_id)
        ON DELETE CASCADE,

    FOREIGN KEY (author_id)
        REFERENCES authors(author_id)
        ON DELETE CASCADE
);

CREATE TABLE members (
    member_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
);

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,

    CHECK (due_date >= loan_date),
    CHECK (
        return_date IS NULL
        OR return_date >= loan_date
    ),

    FOREIGN KEY (book_id)
        REFERENCES books(book_id)
        ON DELETE RESTRICT,

    FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE RESTRICT
);

CREATE UNIQUE INDEX idx_one_active_loan_per_book
ON loans (book_id)
WHERE return_date IS NULL;

CREATE INDEX idx_book_authors_author_id
ON book_authors (author_id);

CREATE INDEX idx_loans_member_id
ON loans (member_id);