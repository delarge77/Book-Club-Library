# Contributing to Book-Club-Library

Thank you for contributing to Book-Club-Library! This document defines our coding standards, Definition of Done, branching strategy, and code review process.

## 1. Definition of Done (DoD)

A task or user story is considered Done when all the following criteria are met:

- [ ] The implementation meets the agreed requirements and acceptance criteria.
- [ ] The code follows our coding standards and PEP 8 guidelines.
- [ ] Appropriate tests have been written and all tests pass.
- [ ] No known critical bugs or errors remain.
- [ ] The code has been reviewed and approved by at least one other team member.
- [ ] The code has been merged into the `main` branch through a pull request.
- [ ] Relevant documentation has been updated, if necessary.
- [ ] No API keys, passwords, or other secrets are included in the committed code.
- [ ] The application continues to work without breaking existing functionality.

## 2. Coding Standards

### 2.1 Naming Conventions

We follow standard Python naming conventions:

- **Variables and functions:** `snake_case`, for example, `book_title` and `get_book_by_id()`.
- **Classes:** `PascalCase`, for example, `Book`, `Library` and `DatabaseManager`.
- **Constants:** `UPPER_SNAKE_CASE`, for example, `MAX_BOOKS`.
- **Modules and Python files:** lowercase, using underscores when needed, for example, `book_service.py`.
- **Private attributes and methods:** prefix with a single underscore, for example, `_connection`.

Names should be descriptive and meaningful. Avoid unclear abbreviations and single-letter names, except where they are conventional, such as loop counters.

### 2.2 PEP 8

All Python code should follow PEP 8, the official Python style guide.

- Use four spaces for indentation; do not use tabs.
- Keep lines to a reasonable length, preferably no more than 79 characters.
- Use blank lines to separate functions and classes.
- Use spaces around operators, for example, `total = price + tax`.
- Use imports at the beginning of the file.
- Remove unused imports and unnecessary code.
- Use consistent formatting throughout the project.

### 2.3 Docstrings and Comments

- All public classes and functions should have docstrings explaining their purpose.
- Use triple double quotes (`"""`) for docstrings.
- Document parameters, return values, and exceptions when relevant.
- Add comments to explain complex logic or important decisions.
- Avoid comments that simply repeat what the code already says.

Example:

```python
def get_book_by_id(book_id: int) -> dict | None:
    """Return a book by its ID, or None if it is not found."""
    # Implementation goes here
```

### 2.4 Error Handling

- Handle expected errors explicitly using appropriate exceptions.
- Avoid silently ignoring errors.
- Provide clear and useful error messages.
- Do not expose API keys, passwords, or sensitive information in error messages or logs.

### 2.5 Environment Variables and Secrets

- Store local configuration and API keys in a `.env` file.
- Never commit `.env` or other files containing secrets.
- Keep `.env` in `.gitignore`.
- Use `.env.example` to document required environment variables with placeholder values only.

## 3. Branch Naming

We use descriptive branch names with a prefix indicating the type of work.

- `feature/` — new functionality, for example, `feature/add-book-search`
- `fix/` — bug fixes, for example, `fix/handle-missing-book`
- `docs/` — documentation changes, for example, `docs/update-readme`
- `test/` — adding or improving tests, for example, `test/book-search`

Use lowercase letters and hyphens. Keep branch names short and descriptive.

The `main` branch must always contain stable, reviewed code. Contributors should not commit directly to `main`.

## 4. Code Review Process

All changes must be submitted through a pull request (PR).

1. Create a branch from the latest `main`.
2. Implement the change and test it locally.
3. Commit your changes using clear, descriptive commit messages.
4. Push your branch to GitHub and open a pull request against `main`.
5. Explain what changed and why. Link any related issue or task when applicable.
6. Ask at least one other team member to review the PR.
7. Address review comments and make any required changes.
8. Merge the PR only after approval and successful tests.

### Review Checklist

Reviewers should verify that:

- The code meets the requirements and acceptance criteria.
- Naming, formatting, and documentation follow our standards.
- The implementation is understandable and maintainable.
- Tests cover the new functionality and relevant edge cases.
- No secrets, unrelated changes, or unnecessary files are included.
- Existing functionality has not been broken.

Review feedback should be constructive, respectful, and focused on improving the code.

## 5. Commit Messages

Write short, descriptive commit messages using the imperative mood.

Examples:

- `Add book search functionality`
- `Fix database connection handling`
- `Update contributing guidelines`
- `Add tests for book lookup`

## 6. General Guidelines

- Keep changes focused on one task whenever possible.
- Communicate with the team when requirements are unclear.
- Update documentation when functionality or setup instructions change.
- Ask for help if you are unsure about a technical decision.

Our goal is to keep Book-Club-Library reliable, readable, secure, and easy for every team member to maintain.
