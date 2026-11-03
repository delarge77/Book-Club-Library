import os
import requests
from dotenv import load_dotenv
from books_menu import logged_in_menu

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY")


FRIENDLY_MESSAGES = {
    "name": "Name must be at least 5 characters",
    "email": "Email must look like name@example.com",
    "password": "Password must be at least 3 characters",
}


def show_menu():
    """Print the main menu."""
    print("\n--- Book Club Library ---")
    print("1. Register Member")
    print("2. Login")
    print("0. Exit")


def show_errors(data):
    """Print validation errors (422) as short readable messages."""
    print("Please fix:")
    for error in data["detail"]:
        field = error["loc"][-1]
        message = FRIENDLY_MESSAGES.get(field, error["msg"])
        print(f"- {message}")


def register():
    """Ask for member details and register them through the API."""
    name = input("Member Name : ").strip()
    email = input("Email : ").strip()
    phone = input("Phone : ").strip() or None
    password = input("Password : ").strip()

    try:
        response = requests.post(
            f"{BASE_URL}/members/register",
            json={
                "name": name,
                "email": email,
                "phone": phone,
                "password": password,
            },
            headers={"X-API-Key": API_KEY},
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
        print("Registration successful")
        print(f"Welcome {data['name']}! Your member id is {data['member_id']}")
    elif response.status_code == 409:
        print("Email already exists")
    elif response.status_code == 422:
        show_errors(data)
    else:
        print("Error:", response.status_code, data["detail"])


def login():
    """Log in through the API and return the access token, or None."""
    email = input("Email : ").strip()
    password = input("Password : ").strip()

    try:
        response = requests.post(
            f"{BASE_URL}/members/login",
            json={"email": email, "password": password},
            headers={"X-API-Key": API_KEY},
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")
        return None
    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")
        return None

    data = response.json()
    if response.status_code == 200:
        print("Login successful")
        return data["access_token"]
    elif response.status_code == 401:
        print("Wrong email or password")
    elif response.status_code == 422:
        show_errors(data)
    else:
        print("Error:", response.status_code, data["detail"])
    return None


def main():
    """Show the menu until the user chooses Exit."""
    token = None
    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            token = login()
            if token is not None:
                logged_in_menu(token)
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Please choose 1, 2 or 0")


if __name__ == "__main__":
    main()
