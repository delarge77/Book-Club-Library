# Team Reflection

**Project:** Book Club Library · **Group 4** · Module 6, 26 Oct – 6 Nov 2026

## Roles

| Sprint | Product Owner | Scrum Master | Developers |
|---|---|---|---|
| Sprint 1 (27–30 Oct) | Christian | Alessandro | Marcus, Krithika, Alessandro, Christian |
| Sprint 2 (2–5 Nov) | Krithika | Marcus | Marcus, Krithika, Alessandro, Christian |

## What each person mainly built

### Alessandro
Scrum Master in sprint 1, Developer in both sprints.

**Setup**
- Created the GitHub repository and the project structure (API, database, client) (#16, #29)

**API and database**
- Register a new member (#31) and login with password hashing and JWT tokens (#57)
- Add a book (#60), update a book (#72), improved book search (#66)
- A member's current loans (#75), update contact info (#82)
- Return a loan with PUT instead of PATCH (#95)
- Delete a member, or anonymise them if they have loan history (#98)

**Client**
- First API client helper (#29) and register in `client.py` (#31)
- Refactored `api_client.py` with POST/PUT/PATCH/DELETE helpers, used in all menus (#131)

**Reviews:** #32, #34, #35, #36, #55, #58, #59, #62, #64, #70, #71, #73, #74, #77, #84, #94, #97, #109, #120, #133

### Christian
Product Owner in sprint 1, Developer in both sprints.

**Database and data model**
- SQLite scaffolding: schema, seed and database helpers (#34)
- Database design diagram for books, authors, members and loans (#36)
- Default value for `loan_date` (#94), fixed an import for current loans (#77)
- ER diagram of the database (#109)

**Members and personal data**
- Remove a member without loan history (#73)
- `GET /members/me` also shows current and returned loans (#97)

**Open Library and books**
- Import a chosen Open Library result into our database, linked to new or existing authors through `book_authors` (#99)

**Client**
- Menu option 10, borrow a book (#120)
- Menu options 13 and 14, overdue loans and never-borrowed books (#122)

**Setup and documentation**
- Updated `requirements.txt` (#106)
- Rewrote `README.md` for the finished app (#132)

**Reviews:** #35, #37, #57, #59, #60, #72, #74, #75, #76, #82, #100, #107, #108, #110, #111, #119, #121, #123, #127, #131, #133

### Krithika
Developer in both sprints, Product Owner in sprint 2.

**API and database**
- Open Library search: `external_api.py` with a timeout, and `GET /books/search`, which answers 503 with a clear message when Open Library is down (#37, #55)
- `GET /books/never-borrowed`: LEFT JOIN ... IS NULL (#59)
- `GET /books/most-borrowed`: GROUP BY + COUNT (#71)
- `GET /loans/overdue`: JOIN of loans, members and books (#76)
- Author filter on `GET /books?author_name=...` (#84)
- `DELETE /books/{book_id}` (#61)
- X-API-Key on all routes that change data (#100)

**Client**
- Start menu in `client.py`: register and login (#96)
- Import a book from Open Library in the menu (#108)
- Return a book in the menu (#119)
- Solved the merge conflict in `books_menu.py` when borrow (#120) and return (#119) were added at the same time

**Documentation and Scrum**
- Wrote our shared "Way of Working" after Retro 1 (in `retro-sprint-1.md`)
- Put together the team reflection, `docs/reflection.md`

**Reviews:** #31, #57, #58, #60, #66, #70, #73, #74, #95, #98, #99, #104, #106, #118, #132, #133

### Marcus
Developer in both sprints, Scrum Master in sprint 2.

**API and database**
- `GET /books` and `GET /books/{book_id}`, with 404 when the book does not exist (#35)
- Lend a book with `POST /loans`: 14-day due date, 404 for unknown book or member, 409 when the book is already on loan (#58)
- Return a book: 404 for unknown loan, 409 when already returned (#62)
- Loans require a logged-in member (token auth) (#64)
- `GET /members` and `GET /members/search` by name or email (#70, #74)

**Client**
- Books menu: list, show, add, update and delete a book, with the API key and token in the headers (#104, #107)
- My member info, update my contact info and most borrowed books (#110)
- One output style for the whole client (CONTRIBUTING 2.6), and reserved menu numbers 10–16 (#118)
- Show my current loans (#121), list and search members (#123)
- Solved the menu merge conflicts in `books_menu.py` in his branch (#121) after borrow (#120) and return (#119) were merged

**Scrum and documentation**
- Daily notes and both sprint reviews and retrospectives (#111, #127)

**Reviews:** #16, #29, #31, #34, #57, #60, #61, #73, #76, #82, #96, #109, #120, #122

## One review that changed something

- **PR:** #82, update member contact info (built by Alessandro, reviewed by Marcus)
- **What the reviewer found:** when a member updated their email or phone, the answer from the API also showed their `password_hash`. Marcus tested it and pasted the response in the PR as proof.
- **What we changed:** the route now sends back only safe fields (member_id, name, email, phone), so the password hash never leaves the server.
- **What we learned:** test what the API *sends back*, not only what it saves. Marcus also noticed that you must send both email and phone to update only one of them. We discussed it and kept it as it is.

## One problem that was hard, and how we solved it

- **Problem:** In sprint 2, three of us added new options to the same client menu in `books_menu.py` at the same time (return #119, borrow #120, my loans #121, overdue and never-borrowed #122, members #123, all on 4 Nov). Each time one PR was merged, the next branches got merge conflicts, because they had changed the same lines: the menu text and the `if choice == ...` list.
- **How we solved it:** We got on a call and solved the conflicts together, one PR at a time. Before merging, each person merged main into their own branch, kept both people's code, and tested the menu again. It helped that we had already reserved menu numbers 10–16 for the remaining stories (#118), so nobody took the same number.
- **What we learned:** Agree early on shared files (menu numbers, output style), merge small PRs often, and merge main into your branch before asking for review.

## Our Scrum process

**What worked well**
- Our "Way of Working" from Retro 1: every PR posted in the channel, someone replied "I'm reviewing it", and calls were agreed in the chat first. Details in [retro-sprint-1.md](retro-sprint-1.md) and [retro-sprint-2.md](retro-sprint-2.md).

**One thing we would do differently next time**
- Agree on shared files (menu numbers, output style) at sprint planning, before coding starts, to avoid merge conflicts.
