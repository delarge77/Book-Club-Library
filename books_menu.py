import os
import requests
from dotenv import load_dotenv
from api_client import get_json

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
    # Reserved for the backlog stories (uncomment when the option is added):
    # print("12. Show my current loans")
    print("13. Show overdue loans")
    print("14. Show never-borrowed books")
    # print("15. List members")
    # print("16. Search members")
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
    """Ask for book details to add new book."""
    print("\n--- Add new book ---")

    title = input("Book Title : ").strip()
    author_name = input("Author Name : ").strip()
    publication_year = ask_year()
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
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])
        return

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error:", response.status_code)
        return
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

    try:
        response = requests.post(
            f"{BASE_URL}/books/import",
            json=book,
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])
        return

    if response.status_code == 201:
        data = response.json()
        print(f"Imported! '{data['title']}' has book_id {data['book_id']}")
    elif response.status_code == 409:
        print("This book is already in the library.")
    elif response.status_code == 401:
        print(STATUS_MESSAGES[401])
    else:
        print("Error:", response.status_code)


def delete_book(headers):
    """Delete a book using book_id."""
    print("\n--- Delete book ---")
    book_id = ask_book_id()
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
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])

        return
    if response.status_code == 204:
        print("Book deleted")
    elif response.status_code == 404:
        print("Book can't be found")
    elif response.status_code == 409:
        print("Book has loans and cannot be deleted")
    else:
        print("Error:", response.status_code)


def update_book(headers):
    """Update a book using book_id."""
    print("\n--- Update book ---")

    book_id = ask_book_id()
    book = get_json(f"{BASE_URL}/books/{book_id}")
    if book is None:
        return
    print(BOOK_INFO.format_map(book))
    book_updates = {}
    title = input("New title (Enter to keep): ").strip()
    if title != "":
        book_updates["title"] = title
    author = input("New Author name (Enter to keep): ").strip()
    if author != "":
        book_updates["author_name"] = author
    publication_year = ask_year()
    if publication_year is not None:
        book_updates["publication_year"] = publication_year
    if not book_updates:
        print("No changes made")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/books/update/{book_id}",
            json=book_updates,
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])
        return

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error:", response.status_code)
        return
    if response.status_code == 200:
        print("Book updated!")
        print(BOOK_INFO.format_map(data))
    elif response.status_code == 409:
        print("Could not update the book (data conflict)")
    elif response.status_code == 422:
        print("Please check input")
    elif response.status_code == 401:
        print(STATUS_MESSAGES[401])
    else:
        print("Error:", response.status_code, data["detail"])


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

    member_info = get_json(f"{BASE_URL}/members/me", headers=headers)
    if member_info is None:
        return
    profile = member_info["profile"]
    email = input(f"New email ({profile['email']}): ").strip() or profile["email"]
    phone = (
        input(f"New phone number ({profile['phone']}): ").strip() or profile["phone"]
    )
    try:
        response = requests.patch(
            f"{BASE_URL}/members/update_contact/{profile['member_id']}",
            json={"email": email, "phone": phone},
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])
        return

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error:", response.status_code)
        return
    if response.status_code == 200:
        print("Contact updated!")
        print(MEMBER_INFO.format_map(data))
    elif response.status_code == 409:
        print("Could not update email (data conflict)")
    elif response.status_code == 422:
        print("Please check input")
    elif response.status_code == 401:
        print(STATUS_MESSAGES[401])
    else:
        print("Error:", response.status_code, data["detail"])


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

    books = get_json(
        f"{BASE_URL}/books/never-borrowed"
    )

    if books is None:
        return

    if not books:
        print("Every book has been borrowed at least once.")
        return

    for number, book in enumerate(books, start=1):
        print(
            f"{number}. "
            + BOOK_INFO.format_map(book)
        )


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


def borrow_book(headers):
    """Borrow a book using its book_id."""

    print("Borrow a book")
    book_id = ask_book_id()

    confirm = input(f"Borrow book with ID {book_id}? y/n: ").strip().lower()
    if confirm != "y":
        print("Cancelled")
        return

    try:
        response = requests.post(
            f"{BASE_URL}/loans",
            json={"book_id": book_id},
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")
        return
    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")
        return

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error:", response.status_code)
        return

    if response.status_code == 201:
        print("Book borrowed!")
        print(f"Loan ID: {data['loan_id']}")
    elif response.status_code == 404:
        print("Book not found")
    elif response.status_code == 409:
        print("This book is already on loan")
    elif response.status_code == 401:
        print(
            "Not logged in, the API key is invalid, "
            "or your session has expired."
        )
    elif response.status_code == 422:
        print("Please enter a valid positive book ID")
    else:
        print(
            "Error:",
            response.status_code,
            data.get("detail", "Unknown error"),
        )


def return_book(headers):
    """Return a borrowed book using loan_id."""
    print("\n--- Return a book ---")

    loan_id = ask_loan_id()
    try:
        response = requests.put(
            f"{BASE_URL}/loans/{loan_id}/return",
            headers=headers,
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print(STATUS_MESSAGES["connection"])
        return
    except requests.exceptions.Timeout:
        print(STATUS_MESSAGES["timeout"])
        return

    if response.status_code == 200:
        print(f"Book returned! (loan_id {loan_id})")
    elif response.status_code == 404:
        print("Loan not found.")
    elif response.status_code == 409:
        print("This book is already returned.")
    elif response.status_code == 401:
        print(STATUS_MESSAGES[401])
    else:
        print("Error:", response.status_code)


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
        

        elif choice == "13":
            show_overdue_loans(headers)
        elif choice == "14":
            show_never_borrowed_books()
        elif choice == "0":
            print("Logging out. Bye!")
            break
        else:
            print("Please choose a number from the menu")


if __name__ == "__main__":
    logged_in_menu("test")
