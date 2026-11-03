import os
import requests
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
    print("3. Add new book")
    print("4. Delete book")
    print("5. Update book")
    print("6. Show my member info")
    print("7. Update my contact info")
    print("8. Show most borrowed books")
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


def add_new_book(headers):
    """Ask for book details to add new book."""

    title = input("Book title : ").strip()
    author_name = input("Author Name : ").strip()
    publication_year = input("Publication year : ").strip() or None
    if publication_year is not None:
        publication_year = int(publication_year)

    try:
        response = requests.post(
            f"{BASE_URL}/books/add_new_book",
            json={
                "title": title,
                "author_name": author_name,
                "publication_year": publication_year,
            },
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")
        return
    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")
        return

    data = response.json()
    if response.status_code == 201:
        print("Book added!")
        if publication_year is not None:
            success_message = f"{title} by {author_name} from {publication_year} with id: {data['book_id']}"
        else:
            success_message = f"{title} by {author_name} with id: {data['book_id']}"
        print(success_message)
    elif response.status_code == 409:
        print("Book already exists")
    elif response.status_code == 422:
        print("Please check title and author")
    else:
        print("Error:", response.status_code, data["detail"])


# delete book
def delete_book(headers):
    """delete book using book_id"""
    print("Delete book")
    while True:
        try:
            book_id = int(input("Book ID: : ").strip())
        except ValueError:
            print("Please type a number.")
        else:
            break
    book = get_json(f"{BASE_URL}/books/{book_id}")
    if book is None:
        return
    confirm = input(f"Delete {book['title']}? y/n ").strip().lower()
    if confirm != "y":
        print("Cancelled")
        return

    try:
        response = requests.delete(
            f"{BASE_URL}/books/{book_id}",
            headers=headers,
            timeout=5,
        )

    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")
        return
    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")

        return
    if response.status_code == 204:
        print("Book deleted")
    elif response.status_code == 404:
        print("Book cant be found")
    elif response.status_code == 409:
        print("Book has loans and can not be deleted")
    else:
        print("Error:", response.status_code)


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
        elif choice == "3":
            add_new_book(headers)
        elif choice == "4":
            delete_book(headers)
        elif choice == "0":
            print("Logging out. Bye!")
            break
        else:
            print("Please choose a number from the menu")


if __name__ == "__main__":
    logged_in_menu("test")
