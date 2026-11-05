import os
import requests
from dotenv import load_dotenv
from api_client import get_json, post_json, put_json, patch_json, delete_request
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "http://127.0.0.1:8000"
BOOK_INFO = "{title} ({publication_year}), book_id {book_id}"
MEMBER_INFO = "{name}, {email}, {phone} (member_id {member_id})"

STATUS_MESSAGES = {
    401: "Please log in again.",
    "connection": "Cannot reach the server. Is the API running?",
    "timeout": "The server is too slow to answer. Try again later.",
}


def ask_book_id():
    """Ask for a book_id."""
    while True:
        try:
            return int(input("Book ID : ").strip())
        except ValueError:
            print("Please type a number.")


def ask_year():
    """Ask for a publication year. Enter skips and returns None."""
    while True:
        year = input("Publication Year : ").strip()
        if year == "":
            return None
        try:
            return int(year)
        except ValueError:
            print("Please type a number, or press Enter to skip.")


def ask_loan_id():
    """Ask for a loan_id."""
    while True:
        try:
            return int(input("Loan ID : ").strip())
        except ValueError:
            print("Please type a number.")


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
    print("9. Import from Open Library")
    print("10. Borrow a book")
    print("11. Return a book")
    print("12. Show my current loans")
    print("13. Show overdue loans")
    print("14. Show never-borrowed books")
    print("15. List members")
    print("16. Search members")
    print("0. Log out")
    print(" ")


def list_books():
    """List all catalogued books."""
    print("\n--- Books ---")

    books = get_json(f"{BASE_URL}/books")
    if books is None:
        return
    for number, book in enumerate(books, start=1):
        print(f"{number}. " + BOOK_INFO.format_map(book))


def show_book():
    """Print one book using book_id."""
    print("\n--- Show one book ---")

    book_id = ask_book_id()
    book = get_json(f"{BASE_URL}/books/{book_id}")
    if book is None:
        return
    print(BOOK_INFO.format_map(book))



def add_new_book(headers):
    """Ask for book details to add a new book."""

    print("\n--- Add new book ---")

    title = input("Book Title: ").strip()
    author_name = input("Author Name: ").strip()
    publication_year = ask_year()

    response = post_json(
        f"{BASE_URL}/books/add_new_book",
        params={
            "title": title,
            "author_name": author_name,
            "publication_year": publication_year
        },
        headers=headers,
        timeout=5,
        status_messages={
            401: "Your session has expired. Please log in again.",
            409: "Book already exists."
        }
    )

    if response is None:
        return

    print("Book added!")

    if publication_year is not None:
        success_message = (
            f"{title} by {author_name} from {publication_year} "
            f"with ID: {response['book_id']}"
        )
    else:
        success_message = (
            f"{title} by {author_name} "
            f"with ID: {response['book_id']}"
        )

    print(success_message)


def search_open_library():
    """Search Open Library and print the results as a numbered list."""
    query = input("Search Open Library: ").strip()
    if not query:
        print("Please type something to search for.")
        return None

    books = get_json(f"{BASE_URL}/books/search", params={"q": query}, timeout=10)
    if not books:
        print("No books found.")
        return None

    for number, book in enumerate(books, start=1):
        authors = ", ".join(book["author_name"])
        print(f"{number}. {book['title']} by {authors} ({book['first_publish_year']})")
    return books


def choose_book(books):
    """Ask for a number and return that book, or None to cancel."""
    while True:
        choice = input("Pick a number to import (Enter to cancel): ").strip()
        if choice == "":
            return None
        try:
            number = int(choice)
        except ValueError:
            print("Please type a number.")
            continue
        if 1 <= number <= len(books):
            return books[number - 1]
        print(f"Please choose 1 to {len(books)}.")



def import_book(headers):
    """Search Open Library, pick a book and import it."""

    print("\n--- Import from Open Library ---")

    books = search_open_library()

    if not books:
        return

    book = choose_book(books)

    if book is None:
        print("Import cancelled.")
        return

    response = post_json(
        f"{BASE_URL}/books/import",
        params=book,
        headers=headers,
        timeout=5,
        status_messages={
            401: "Your session has expired. Please log in again.",
            409: "This book is already in the library."
        }
    )

    if response is None:
        return

    print(
        f"Imported! '{response['title']}' "
        f"has book_id {response['book_id']}"
    )

def delete_book(headers):
    """Delete a book using book_id."""

    print("\n--- Delete book ---")

    book_id = ask_book_id()

    book = get_json(
        f"{BASE_URL}/books/{book_id}"
    )

    if book is None:
        return

    confirm = input(
        f"Delete {book['title']}? y/n: "
    ).strip().lower()

    if confirm != "y":
        print("Cancelled")
        return

    response = delete_request(
        f"{BASE_URL}/books/{book_id}",
        headers=headers,
        timeout=5,
        status_messages={
            401: "Your session has expired. Please log in again.",
            404: "Book can't be found.",
            409: "Book has loans and cannot be deleted."
        }
    )

    if response is None:
        return

    print("Book deleted successfully!")




def update_book(headers):
    """Update a book using book_id."""

    print("\n--- Update book ---")

    book_id = ask_book_id()

    book = get_json(
        f"{BASE_URL}/books/{book_id}",
        headers=headers
    )

    if book is None:
        return

    print(BOOK_INFO.format_map(book))

    book_updates = {}

    title = input("New title (Enter to keep): ").strip()
    if title:
        book_updates["title"] = title

    author = input("New author name (Enter to keep): ").strip()
    if author:
        book_updates["author_name"] = author

    publication_year = ask_year()
    if publication_year is not None:
        book_updates["publication_year"] = publication_year

    if not book_updates:
        print("No changes made.")
        return

    response = patch_json(
        f"{BASE_URL}/books/update/{book_id}",
        params=book_updates,
        headers=headers,
        timeout=5,
        status_messages={
            401: "Your session has expired. Please log in again.",
            404: "Book not found.",
            409: "Could not update the book (data conflict)."
        }
    )

    if response is None:
        return

    print("Book updated!")
    print(BOOK_INFO.format_map(response))



def show_my_info(headers):
    """Show the logged-in member's info."""
    print("\n--- My member info ---")

    member_info = get_json(f"{BASE_URL}/members/me", headers=headers)
    if member_info is None:
        return
    profile = member_info["profile"]
    print(MEMBER_INFO.format_map(profile))



def update_my_contact(headers):
    """Update the logged-in member's email and phone."""

    print("\n--- Update my contact info ---")

    member_info = get_json(
        f"{BASE_URL}/members/me",
        headers=headers
    )

    if member_info is None:
        return

    profile = member_info["profile"]

    email = (
        input(f"New email ({profile['email']}): ").strip()
        or profile["email"]
    )

    phone = (
        input(f"New phone number ({profile['phone']}): ").strip()
        or profile["phone"]
    )

    response = patch_json(
        f"{BASE_URL}/members/update_contact/{profile['member_id']}",
        params={
            "email": email,
            "phone": phone
        },
        headers=headers,
        timeout=5,
        status_messages={
            401: "Your session has expired. Please log in again.",
            404: "Member not found.",
            409: "Could not update email. Email already exists."
        }
    )

    if response is None:
        return

    print("Contact updated!")
    print(MEMBER_INFO.format_map(response))



def show_overdue_loans(headers):
    """Show active loans whose due date has passed."""

    print("\n--- Overdue loans ---")

    loans = get_json(
        f"{BASE_URL}/loans/overdue",
        headers=headers,
    )

    if loans is None:
        return

    if not loans:
        print("There are no overdue loans.")
        return

    for number, loan in enumerate(loans, start=1):
        print(
            f"{number}. {loan['title']} borrowed by "
            f"{loan['name']} | due {loan['due_date']} "
            f"| loan_id {loan['loan_id']}"
        )


def show_never_borrowed_books():
    """Show books that have never been borrowed."""

    print("\n--- Never-borrowed books ---")

    books = get_json(f"{BASE_URL}/books/never-borrowed")

    if books is None:
        return

    if not books:
        print("Every book has been borrowed at least once.")
        return

    for number, book in enumerate(books, start=1):
        print(f"{number}. " + BOOK_INFO.format_map(book))


def show_most_borrowed_books():
    """Show the most borrowed books."""
    print("\n--- Most borrowed books ---")
    books = get_json(f"{BASE_URL}/books/most-borrowed")
    if books is None:
        return
    if not books:
        print("No loans yet.")
        return
    for number, book in enumerate(books, start=1):
        print(
            f"{number}. {book['title']} ({book['loan_count']} loans), book_id {book['book_id']}"
        )


def show_my_current_loans(headers):
    """Show the logged-in member's current loans."""
    print("\n--- My current loans ---")

    member_info = get_json(f"{BASE_URL}/members/me", headers=headers)
    if member_info is None:
        return
    member_id = member_info["profile"]["member_id"]
    loans = get_json(f"{BASE_URL}/members/{member_id}/loans/current", headers=headers)
    if loans is None:
        return
    if not loans:
        print("No current loans.")
        return
    for number, loan in enumerate(loans, start=1):
        print(
            f"{number}. {loan['title']}, due {loan['due_date']}, loan_id {loan['loan_id']}"
        )



def borrow_book(headers):
    """Borrow a book using its book_id."""

    print("\n--- Borrow a book ---")

    book_id = ask_book_id()

    confirm = input(
        f"Borrow book with ID {book_id}? y/n: "
    ).strip().lower()

    if confirm != "y":
        print("Cancelled")
        return

    response = post_json(
        f"{BASE_URL}/loans",
        params={"book_id": book_id},
        headers=headers,
        timeout=5,
        status_messages={
            401: "Not logged in or your session has expired.",
            404: "Book not found.",
            409: "This book is already on loan."
        }
    )

    if response is None:
        return

    print("Book borrowed successfully!")
    print(f"Loan ID: {response['loan_id']}")



def return_book(headers):
    """Return a borrowed book using loan_id."""
    print("\n--- Return a book ---")
    loan_id = ask_loan_id()

    response = put_json(
        f"{BASE_URL}/loans/{loan_id}/return",
        headers=headers,
        timeout=5,
        status_messages={
            401: "You are not authorized. Please log in again.",
            404: "Loan not found.",
            409: "This book is already returned."
        }
    )

    if response is None:
        return

    print(f"Book returned successfully! (loan_id {loan_id})")



def show_members(headers):
    """List all registered members."""
    print("\n--- Members ---")
    members = get_json(f"{BASE_URL}/members", headers=headers)
    if members is None:
        return
    if not members:
        print("No members yet.")
        return
    for number, member in enumerate(members, start=1):
        print(f"{number}. " + MEMBER_INFO.format_map(member))


def find_member(headers):
    """Show members by name or email."""
    print("\n--- Search members ---")
    query = input("Search member by Name or Email : ").strip()
    members = get_json(
        f"{BASE_URL}/members/search", params={"q": query}, headers=headers
    )
    if members is None:
        return
    if not members:
        print("No members found.")
        return
    for number, member in enumerate(members, start=1):
        print(f"{number}. " + MEMBER_INFO.format_map(member))


def logged_in_menu(token):
    """Show the logged-in menu."""
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
        elif choice == "5":
            update_book(headers)
        elif choice == "6":
            show_my_info(headers)
        elif choice == "7":
            update_my_contact(headers)
        elif choice == "8":
            show_most_borrowed_books()
        elif choice == "9":
            import_book(headers)
        elif choice == "10":
            borrow_book(headers)
        elif choice == "11":
            return_book(headers)
        elif choice == "12":
            show_my_current_loans(headers)
        elif choice == "13":
            show_overdue_loans(headers)
        elif choice == "14":
            show_never_borrowed_books()
        elif choice == "15":
            show_members(headers)
        elif choice == "16":
            find_member(headers)
        elif choice == "0":
            print("Logging out. Bye!")
            break
        else:
            print("Please choose a number from the menu")


if __name__ == "__main__":
    logged_in_menu("test")
