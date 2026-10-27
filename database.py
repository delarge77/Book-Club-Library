import sqlite3

DB_NAME = "library.db"


def connect():
    """Open a connection to the library database with foreign keys on."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_all_catalogued_books():
    """Get all catalogued books from db"""
    conn = connect()
    cursor = conn.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books
