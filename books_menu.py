import os
from dotenv import load_dotenv
from api_client import get_json

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "http://127.0.0.1:8000"
BOOK_INFO = "book_id: {book_id} | name: {title} | year: {publication_year}"


def show_user_menu():
    """Print the user menu."""
    print("\n--- Book Club Library ---")
    print("\n------- User Menu -------")
    print(" ")
    print("1. List books")
    print("2. Show one book")
    print("0. Log out")
    print(" ")


def list_books():
    """list all catalogued books"""
    books = get_json(f"{BASE_URL}/books")
    if books is None:
        return
    for book in books:
        print(BOOK_INFO.format_map(book))


def show_book():
    """Print one book using book_id"""

    while True:
        try:
            user_input = int(input("book id:"))
        except ValueError:
            print("Please type a number.")
        else:
            break
    book = get_json(f"{BASE_URL}/books/{(user_input)}")
    if book is None:
        return
    print(BOOK_INFO.format_map(book))


# add book


def add_book():
    """add book to catalogue"""
    books = get_json(f"{BASE_URL}/books/add_new/book")


# delete book
# show member information
# show atleast one memberstatistics endpoint
# errors from the api with clear message


def logged_in_menu(token):
    """Show logged-in menu"""
    headers = {"X-API-Key": API_KEY, "Authorization": f"Bearer {token}"}

    while True:
        show_user_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            list_books()
        elif choice == "2":
            show_book()
        elif choice == "0":
            print("Logging out. Bye!")
            break
        else:
            print("Please choose 1, 2 or 0")


if __name__ == "__main__":
    logged_in_menu("test")
