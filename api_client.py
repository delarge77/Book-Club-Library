import requests

FRIENDLY_MESSAGES = {
    "name": "Name must be at least 5 characters",
    "email": "Email must look like name@example.com",
    "password": "Password must be at least 3 characters",
}

def get_json(url, params=None, headers=None, timeout=5):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("The request took too long")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server")
    except requests.exceptions.HTTPError as error:
        if error.response is not None:
             print(f"The server said no: {error.response.status_code}")
        else:
            print("An HTTP error occurred.")
    except requests.exceptions.JSONDecodeError:
        print("The answer was not JSON")
    except requests.exceptions.RequestException as error:
        print(f"Something else went wrong: {type(error).__name__}")
    return None

def post_json(url, params=None, headers=None, timeout=5):
    try:
        response = requests.post(url, json=params, headers=headers, timeout=timeout)

        # Handle specific HTTP status codes
        if response.status_code == 401:
            print("Wrong email or password")
            return None
        
        if response.status_code == 409:
            print("Email already exists")
            return None

        if response.status_code == 422:
            show_errors(response.json())
            return None

        # Raise exceptions for other unsuccessful responses
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")
        return
    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")
        return
    except requests.exceptions.HTTPError as error:
        if error.response is not None:
            print(f"The server said no: {error.response.status_code}")
            print(f"Details: {error.response.text}")
        else:
            print("An HTTP error occurred.")

    except requests.exceptions.JSONDecodeError:
        print("The answer was not JSON")

    except requests.exceptions.RequestException as error:
        print(f"Something else went wrong: {type(error).__name__}")

    return None


def show_errors(data):
    """Print validation errors (422) as short readable messages."""
    print("Please fix:")
    for error in data["detail"]:
        field = error["loc"][-1]
        message = FRIENDLY_MESSAGES.get(field, error["msg"])
        print(f"- {message}")