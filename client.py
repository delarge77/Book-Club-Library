import os
import requests
from dotenv import load_dotenv
from books_menu import logged_in_menu
from api_client import post_json

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY")


def show_menu():
    """Print the main menu."""
    print("\n--- Book Club Library ---")
    print("1. Register Member")
    print("2. Login")
    print("0. Exit")



def register():
    """Ask for member details and register them through the API."""
    name = input("Member Name : ").strip()
    email = input("Email : ").strip()
    phone = input("Phone : ").strip() or None
    password = input("Password : ").strip()

        
    response = post_json(f"{BASE_URL}/members/register",
                           {"name":name,"email":email,"phone":phone,"password":password},
                           {"X-API-Key": API_KEY},
                           5,
                           status_messages={409: "Email already exists."}
                        )
        
    if response is None:
        print("Registration failed. Please try again.")
        return
    
    print("Registration successful")
    print(f"Welcome {response['name']}! Your member id is {response['member_id']}")
    


def login():
    """Log in through the API and return the access token, or None."""

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    response = post_json(
        f"{BASE_URL}/members/login",
        {"email": email, "password": password},
        {"X-API-Key": API_KEY},
        5,
        status_messages={401: "Invalid email or password."}
    )

    if response is None:
        return None

    access_token = response.get("access_token")

    if access_token:
        print("Login successful!")
        return access_token

    print("Login failed. No access token received.")
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
