# Sprint 2: Review and Retrospective
 
**Sprint:** 2–4 Nov 2026 (planning 2 Nov) · **Retro 2:** Thu 5 Nov, after the 12:00 feature freeze
 
## Roles in sprint 2
- Product Owner: Krithika
- Scrum Master: Marcus
- Developers: Marcus, Krithika, Alessandro, Christian
## Product Goal
To help 'Book Club Library' volunteers manage books, members, and loans efficiently while reducing manual work by importing external data.
 
## Sprint Goal
Volunteers can manage books from a terminal menu, import books from Open Library, and every route that changes data is protected with an API key.
 
## Increment: what was merged to main
 
| Area | What works | PRs | Who |
|---|---|---|---|
| Loans | Default loan_date, loans use PUT | #94, #95 | Christian, Alessandro |
| Members | Anonymous user on delete, my profile lists loans | #98, #97 | Alessandro, Christian |
| API | X-API-Key on all write routes | #100 | Krithika |
| Books | Import from Open Library search result | #99 | Christian |
| Client | Register + login menu | #96 | Krithika |
| Client | Books menu: list, show, add, update, delete | #104, #107 | Marcus |
| Client | Import from Open Library in the menu | #108 | Krithika |
| Client | My member info, update contact, most borrowed | #110 | Marcus |
| Client | Consistent output layout (CONTRIBUTING 2.6), menu numbers 10-16 | #118 | Marcus |
| Client | Borrow a book, return a book | #120, #119 | Christian, Krithika |
| Client | My current loans | #121 | Marcus |
| Client | Overdue loans, never-borrowed books | #122 | Christian |
| Client | List and search members | #123 | Marcus |
| Client | Refactoring + POST helper in api_client.py | #131 | Alessandro |
| Setup | requirements.txt updated | #106 | Christian |
| Docs | ER diagram, daily notes, sprint retros | #109, #111, #127 | Christian, Marcus |
 
## Retrospective 2

**What went well**
- The Way of Working from Retro 1 worked: every PR was posted in the channel, someone replied "I'm reviewing it", and PR texts had "How to test" and `Closes #`.
- The communication rules worked: we asked in the chat first and agreed on a time before starting a call, with only the people needed.
- Breaking stories into smaller sub-issues (decided at Sprint Review 1) gave small PRs that were quick to review.

**What we can do better**
- Several PRs touched `books_menu.py` at the same time, which caused merge conflicts in the menu. Reserving menu numbers early (#118) helped.
- Branches were sometimes behind main when tested, so reviewers saw old code. Merge main into your branch before asking for review.

**What we would change next time**
- Keep the "Way of Working" and the "sub-issue split".
- Agree on shared files and formats (menu numbers, output style) at sprint planning, before coding starts.
