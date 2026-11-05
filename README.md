# Book Club Library

Book Club Library is a Python application for a small community library run by volunteers. It replaces notebook-based loan tracking with a REST API, a SQLite database, an Open Library integration, and a terminal client.

## Project status

The project is in its final stage and the application is functional in its current form. The implemented system supports:

- member registration and login;
- API-key protection for routes that change data;
- JWT bearer authentication for member operations;
- book catalogue management;
- title-based Open Library search and import;
- borrowing and returning books;
- current, overdue, most-borrowed, and never-borrowed views;
- member profiles with loan history;
- member deletion or anonymisation depending on loan history;
- a terminal-based client menu; and
- interactive API documentation through FastAPI Swagger UI.

The application is intended as a local educational project, not a production library service.

## Technology stack

- Python 3.10 or later
- FastAPI
- SQLite
- Pydantic
- Requests
- Open Library Search API
- PyJWT
- pwdlib with Argon2
- python-dotenv

## Project structure

```text
Book-Club-Library/
├── api_client.py       # Shared GET helper used by the terminal client
├── books_menu.py       # Logged-in terminal menu and library operations
├── client.py           # Registration, login, and client entry point
├── database.py         # SQLite queries and database operations
├── external_api.py     # Open Library search integration
├── main.py             # FastAPI application, authentication, and routes
├── models.py           # Pydantic request and response models
├── schema.sql          # Database schema, constraints, and indexes
├── seed.py             # Recreates and populates the development database
├── start.sh            # Starts the FastAPI development server
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── CONTRIBUTING.md     # Team standards and Definition of Done
├── docs/
│   ├── daily.md
│   ├── library_ER_Diagram.png
│   ├── retro-sprint-1.md
│   └── retro-sprint-2.md
├── .env.example        # Environment-variable template
└── .gitignore          # Files excluded from Git
```

The local `.env`, virtual environment, cache files, access tokens, and `library.db` should not be committed.

## Database design

The SQLite database contains five tables:

- `authors`: unique author records;
- `books`: title, display-form author name, and publication year;
- `book_authors`: many-to-many links between books and authors;
- `members`: contact information, active status, and password hash; and
- `loans`: member, book, loan date, due date, and optional return date.

### Relationships

- A book can have several authors.
- An author can be connected to several books.
- A member can have many loans.
- A book can occur in many historical loan records, but only one active loan is allowed at a time.

The database enforces foreign keys, positive publication years when supplied, valid loan-date order, and a unique partial index that prevents two active loans for the same book.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/delarge77/Book-Club-Library.git
cd Book-Club-Library
```

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### macOS, Linux, or Git Bash

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root:

```dotenv
API_KEY=replace-with-a-local-api-key
JWT_SECRET_KEY=replace-with-a-random-secret
```

A development JWT secret can be generated with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Never commit `.env`, passwords, password hashes, API keys, JWT secrets, or access tokens. Use placeholder values only in `.env.example`.

### 5. Create and seed the database

```bash
python seed.py
```

This command deletes an existing local `library.db`, recreates the schema, inserts sample authors, books, members, and loans, and prints row counts. Do not run it when local data must be preserved.

### 6. Start the API

```bash
fastapi dev main.py
```

Open:

- API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative documentation: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

The included `start.sh` is a local zsh helper that activates `~/.venv`. If the virtual environment is stored in the repository as `.venv`, use the command above or adjust the script for the local machine.

## Running the terminal client

Start the API in one terminal. Activate the virtual environment in a second terminal and run:

```bash
python client.py
```

Before login, the client allows a user to:

1. register a member; and
2. log in.

After login, the client provides these options:

1. list books;
2. show one book;
3. add a book manually;
4. delete a book;
5. update a book;
6. show the authenticated member's information;
7. update contact information;
8. show the most borrowed books;
9. search and import from Open Library;
10. borrow a book;
11. return a book;
12. show the authenticated member's current loans;
13. show overdue loans;
14. show never-borrowed books;
15. list members; and
16. search members.

## Authentication and API key

The application uses two forms of access control:

- `X-API-Key` is required by routes that change data.
- JWT bearer tokens identify logged-in members and expire after 15 minutes.

Registration and login require the API key. After successful login, the client stores the returned token in memory and sends it with authenticated requests. The terminal client reads `API_KEY` from `.env`.

In Swagger UI:

1. call `POST /members/login` with the API key;
2. copy the returned `access_token`;
3. select **Authorize** and enter the token; and
4. supply `X-API-Key` for protected write routes.

## Open Library integration

The application searches the Open Library Search API and requests up to five results containing:

- title;
- author names; and
- first publication year.

### Terminal workflow

1. Log in through `client.py`.
2. Choose **Import from Open Library**.
3. Enter a search term.
4. Select one numbered result.
5. The selected book is imported into the local database.

The import operation:

- maps `first_publish_year` to `publication_year`;
- stores a comma-separated display value in `books.author_name`;
- creates or reuses records in `authors`;
- creates the corresponding `book_authors` relationships; and
- rejects the same title, author display, and publication year when it is imported again.

Books can also be added manually when Open Library data is not used.

## Loan rules

- A loan is created for the authenticated member.
- The normal loan period is 14 days.
- One member can have many loans.
- The same book cannot have two active loans simultaneously.
- Returning a loan records the current date.
- Overdue loans are active loans whose due date has passed.
- A book is “never borrowed” only when it has no loan record at all.

## Member profile and removal

`GET /members/me` returns the authenticated member's profile together with current and returned loan history. Password hashes are not part of this response.

Member removal follows these rules:

- a member with an active loan cannot be removed;
- a member without loan history is permanently deleted; and
- a member with returned-loan history is anonymised and marked inactive so the historical loan records remain connected.

An inactive member cannot log in and is omitted from the general active-member list.

## API overview

### Members

- `POST /members/register` - register a member.
- `POST /members/login` - authenticate and receive a JWT token.
- `GET /members/me` - show the authenticated profile and loan history.
- `GET /members` - list active members.
- `GET /members/search` - search members by name or email.
- `GET /members/{member_id}/loans/current` - show a member's active loans.
- `PATCH /members/update_contact/{member_id}` - update email and phone.
- `DELETE /members/{member_id}` - delete or anonymise a member.

### Books

- `GET /books` - list books or filter by `author_name`.
- `GET /books/{book_id}` - show one local book.
- `POST /books/add_new_book` - add a book manually.
- `GET /books/search` - search Open Library.
- `POST /books/import` - import a selected Open Library result.
- `PATCH /books/update/{book_id}` - update a book.
- `DELETE /books/{book_id}` - delete a book without loan references.
- `GET /books/never-borrowed` - show books with no loan history.
- `GET /books/most-borrowed` - show up to ten books ordered by loan count.

### Loans

- `POST /loans` - borrow a book.
- `PUT /loans/{loan_id}/return` - return a loan.
- `GET /loans/overdue` - show overdue active loans.

Swagger UI is the authoritative interactive description of request bodies, parameters, and responses in the running application.

## Sample data

Running `seed.py` creates:

- five authors;
- four books;
- three members; and
- three loan records.

The seeded `books.author_name` values currently contain placeholder text such as `author_name_1`. The correct author relationships are still inserted into `authors` and `book_authors`. This is sample-data behavior, not the expected display quality for newly imported books.

## Known issues and limitations

The application works for its intended local demonstration, but the following limitations are known:

- There are no member roles or librarian role. Any logged-in member can access member lists, member searches, overdue-loan information, and member-specific loan routes.
- The contact-update route accepts a member ID in the URL, so a logged-in member can update another member's contact information if that ID is known.
- Member deletion currently requires the API key but not a bearer token.
- Anonymisation replaces the member's name, email, and phone and marks the record inactive, but the existing password hash remains stored.
- Anonymised members are excluded from the general active-member list, but the member-search query does not filter on `is_active`.
- Contact update requires both email and phone. A member whose phone is `NULL` can receive a validation error when the client resends that value.
- Manual book addition writes only to `books`; it does not create `authors` or `book_authors` records. Therefore, manually added books may not appear in the author filter.
- Duplicate detection is implemented for Open Library import, but not for the manual add-book path.
- Manual book creation can turn some validation/database conflicts into a generic or misleading conflict response.
- The API key is distributed to the terminal client through `.env`. It acts as a shared deployment guard, not individual user authentication.
- A `401` response in the logged-in menu prints a message but does not automatically return the user to the login screen.
- The application uses synchronous `sqlite3` and `requests` calls and regular `def` routes. This is intentional for the current implementation.
- Automated tests are not included in the submitted project files; verification is primarily manual through Swagger UI and the terminal client.
- `requirements.txt` lists direct dependencies without pinned versions.
- `start.sh` assumes zsh and a virtual environment at `~/.venv`, so it may need adjustment on another machine.

These items are documented for transparency and are outside the final feature work unless the team explicitly chooses to address them.

## Development workflow

The team used Scrum, GitHub Issues, feature branches, pull requests, and code review across two sprints.

Recommended branch prefixes:

- `feature/` for new functionality;
- `fix/` for bug fixes;
- `docs/` for documentation; and
- `test/` for tests.

The project Definition of Done and coding standards are documented in `CONTRIBUTING.md`. Daily Scrum notes and sprint reviews/retrospectives are stored under `docs/`.

## Contributors

- Marcus
- Krithika
- Alessandro
- Christian

Sprint roles changed between the two sprints and are documented in the retrospective files.

## External resources

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Open Library API documentation](https://openlibrary.org/developers/api)

## License

No license has been selected.
