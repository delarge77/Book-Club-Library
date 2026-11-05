
import requests


FRIENDLY_MESSAGES = {
    "name": "Name must be at least 5 characters",
    "email": "Email must look like name@example.com",
    "password": "Password must be at least 3 characters",
}


def show_errors(data):
    """Print validation errors (422) as short readable messages."""

    print("Please fix:")

    for error in data.get("detail", []):
        field = error.get("loc", ["unknown"])[-1]
        message = FRIENDLY_MESSAGES.get(field, error.get("msg", "Invalid value"))
        print(f"- {message}")


def request_json(method, url, params=None, headers=None,
                  timeout=5, status_messages=None, query_params=False):
    """Handle HTTP requests, responses and common API errors."""

    try:
        request_data = {
            "headers": headers,
            "timeout": timeout
        }

        if method.upper() != "DELETE":
            if query_params:
                request_data["params"] = params
            else:
                request_data["json"] = params

        response = requests.request(
            method,
            url,
            **request_data
        )

        # Handle expected HTTP errors
        if response.status_code in (401, 403, 404, 409, 422):

            if response.status_code == 422:
                show_errors(response.json())
            else:
                messages = status_messages or {}
                print(messages.get(
                    response.status_code,
                    f"Request failed: {response.status_code}"
                ))

            return None

        response.raise_for_status()

        # Handle empty responses (e.g. HTTP 204)
        if not response.content:
            return {}

        return response.json()

    except requests.exceptions.ConnectionError:
        print("Cannot reach the server. Is the API running?")

    except requests.exceptions.Timeout:
        print("The server is too slow to answer. Try again later.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")

        if error.response is not None:
            print(f"Details: {error.response.text}")

    except requests.exceptions.JSONDecodeError:
        print("The answer was not JSON.")

    except requests.exceptions.RequestException as error:
        print(f"Something else went wrong: {type(error).__name__}")

    return None


# Public HTTP helper functions

def get_json(url, params=None, headers=None, timeout=5):
    """Send a GET request."""

    return request_json(
        "GET", url, params, headers, timeout,
        query_params=True
    )


def post_json(url, params=None, headers=None, timeout=5, status_messages=None):
    """Send a POST request."""

    return request_json(
        "POST", url, params, headers, timeout, status_messages
    )


def put_json(url, params=None, headers=None, timeout=5, status_messages=None):
    """Send a PUT request."""

    return request_json(
        "PUT", url, params, headers, timeout, status_messages
    )


def patch_json(url, params=None, headers=None, timeout=5, status_messages=None):
    """Send a PATCH request."""

    return request_json(
        "PATCH", url, params, headers, timeout, status_messages
    )


def delete_request(url, headers=None, timeout=5, status_messages=None):
    """Send a DELETE request."""

    return request_json(
        "DELETE", url, headers=headers, timeout=timeout,
        status_messages=status_messages
    )
