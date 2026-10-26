# 📚 Book Club Library

A Python-based library management system for a small community library run by volunteers.

## 📖 Project Overview

Book Club Library is a collaborative software development project designed to help a small community library transition from manually recording book loans in a notebook to a digital management system.

The application will allow volunteers to manage books, authors, members, and loans while reducing manual data entry through integration with the Open Library API.

The project will be developed using Python and SQLite, following Agile/Scrum practices.

**Project Status:** Planning and initial setup — development has not yet started.

## 🎯 Project Goals

- Replace the paper-based loan tracking system with a digital solution.
- Simplify the management of books, authors, and library members.
- Track borrowed books, due dates, and returns.
- Reduce manual book registration using the Open Library API.
- Provide a simple and user-friendly system for library volunteers.

## ✨ Planned Features

### Book Management
- Add, view, update, and remove books.
- Search books by title, author, or ISBN.
- Retrieve book information automatically using the Open Library API.

### Author Management
- Store and manage author information.
- Associate multiple authors with a book.
- Allow authors to be associated with multiple books.

### Member Management
- Register new library members.
- View and update member information.
- Track books borrowed by each member.

### Loan Management
- Register new book loans.
- Record loan dates and due dates.
- Register book returns and return dates.
- Track active and completed loans.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| SQLite | Relational database |
| SQL | Database queries and relationships |
| Open Library API | Automatic book information retrieval |
| Git | Version control |
| GitHub | Team collaboration and pull requests |
| Scrum | Agile project management |

## 🗂️ Project Structure

The initial repository structure is:

```text
Book-Club-Library/
├── docs/              # Project documentation
├── client.py          # Application interaction logic
├── database.py        # SQLite database operations
├── external_api       # Open Library API integration (planned)
├── main.py            # Application entry point
├── models.py          # Data models
├── schema.sql         # Database schema
├── seed.py            # Initial/sample data
├── requirements.txt   # Python dependencies
├── README.md          # Project overview
├── CONTRIBUTING.md    # Team coding standards
├── .env.example       # Environment variable template
└── .gitignore         # Git ignored files
```

The structure may evolve as development progresses.

## 🗄️ Database Design

The database will contain four main entities:

**Books**
- Book ID
- Title
- ISBN
- Publication information

**Authors**
- Author ID
- Name

**Members**
- Member ID
- Name
- Contact information

**Loans**
- Loan ID
- Book ID
- Member ID
- Loan date
- Due date
- Return date

### Relationships

- **Books ↔ Authors:** Many-to-many. A book can have multiple authors, and an author can write multiple books.
- **Members → Loans:** One-to-many. A member can have multiple loans.
- **Books → Loans:** One-to-many. A book can appear in multiple loan records over time.

A junction table, such as `book_authors`, will manage the many-to-many relationship between books and authors.

The final database schema will be defined during development.

## 🌐 External API

The application will integrate with the [Open Library API](https://openlibrary.org/developers/api) to retrieve book information.

The goal is to allow volunteers to enter an ISBN and automatically retrieve available book metadata, such as title, authors, and publication details, reducing manual data entry.

## 🚀 Getting Started

Development is currently in the planning stage. These are the intended setup steps for contributors.

### 1. Clone the repository

```bash
git clone https://github.com/delarge77/Book-Club-Library.git
cd Book-Club-Library
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Configure environment variables

If environment variables are required, create a local `.env` file using `.env.example` as a template.

Never commit API keys, passwords, or other secrets to GitHub.

### 5. Run the application

Once the application has been implemented, the intended entry point is:

```bash
python3 main.py
```

Database initialization and complete execution instructions will be documented as development progresses.

## 🔄 Development Workflow

The team follows Agile/Scrum practices and uses GitHub for collaboration.

### Branch Naming

- `feature/` — New functionality
- `fix/` — Bug fixes
- `docs/` — Documentation changes
- `test/` — Tests

Example: `feature/add-book-search`

### Pull Requests

1. Create a new branch from `main`.
2. Implement the assigned task.
3. Test the changes locally.
4. Push the branch to GitHub.
5. Open a pull request.
6. Request a code review from another team member.
7. Merge after approval and all required checks pass.

Direct commits to `main` are not part of the team's intended workflow.

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, Definition of Done, and review guidelines.

## 📋 Project Management

The project follows the Scrum framework.

Work will be organized into a Product Backlog containing user stories and tasks. The team will plan and prioritize work during Sprint Planning and review progress throughout development.

GitHub Issues will be used to track tasks, bugs, and improvements.

## 🚧 Project Status

**Current Phase: Planning / Repository Setup**

- [x] Create GitHub repository
- [x] Define initial project structure
- [x] Create contribution guidelines
- [x] Configure `.gitignore`
- [ ] Finalize Product Backlog
- [ ] Design SQLite database schema
- [ ] Implement book and author management
- [ ] Integrate Open Library API
- [ ] Implement member management
- [ ] Implement loan management
- [ ] Add automated tests
- [ ] Complete documentation

## 👥 Contributors

This project is being developed collaboratively by a team of software development students.

All contributors are expected to follow the guidelines described in [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

No license has been selected yet.

