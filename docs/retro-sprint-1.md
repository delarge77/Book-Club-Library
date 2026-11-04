# Sprint 1: Review and Retrospective
 
**Sprint:** 27–29 Oct 2026 · **Review + Retro:** Fri 30 Oct (afternoon)
 
## Roles in sprint 1
- Product Owner: Christian
- Scrum Master: Alessandro
- Developers: Marcus, Krithika, Alessandro, Christian
## Sprint Goal
?  <!-- the one sentence you wrote at Sprint Planning 1 on 26 Oct -->
 
## Sprint Review 1 (5-minute demo for the class)
 
**Increment: what was merged to main**
 
| Area | What works | PRs | Who |
|---|---|---|---|
| Setup | Repo, .gitignore, .env, CONTRIBUTING.md, README | #16 | Alessandro |
| Database | schema.sql, seed.py, local library.db, DB design | #34, #36 | Christian |
| Books | GET /books, GET /books/{book_id} | #35 | Marcus |
| Books | Open Library search, GET /books/search | #37, #55 | Krithika |
| Books | Add (#60) and update (#72) a book, search fix (#66) | #60, #66, #72 | Alessandro |
| Books | Remove a book, never-borrowed, most borrowed | #59, #61, #71 | Krithika |
| Books | Filter GET /books by author | #84 | Krithika |
| Members | Register (#31), login with JWT (#57), update member info (#82) | #31, #57, #82 | Alessandro |
| Members | List and search members | #70, #74 | Marcus |
| Members | Remove a member | #73, #77 | Christian |
| Loans | Lend (#58) and return (#62) a book, token auth on loans (#64) | #58, #62, #64 | Marcus |
| Loans | Member's current loans, overdue loans | #75, #76 | Alessandro, Krithika |
| Client | api_client.py with get_json() | #29 | Alessandro |
 
**Not done in sprint 1 (moved to sprint 2):** client.py menu (register/login, books, members), import from Open Library into the DB, API key on all write routes.
 
**Feedback from the review:**
- ?
## Retrospective 1
 
**What went well**
- Many small PRs, each closing one issue. About 35 PRs merged in sprint 1.
- Every PR was reviewed before merging.
  
**What we can do better**
- Merge conflicts in main.py and database.py, mostly in the import lines, because many PRs touched the same files.
- A new push removed the approval, so PRs needed another review ("stale review").
- requirements.txt was not kept up to date.
- Review PRs faster before continuing other tasks to keep the codebase up to date.
- Calls started without warning and pulled in people who weren't needed.
- It wasn't clear who was reviewing which PR, and PR descriptions varied.
  
**The one change we try in sprint 2: a shared Way of Working** (written by Krithika after the retro)

*Daily standup (09:00)*
- What I worked on yesterday, what I will do today, any blockers.
- If a blocker needs a meeting, we decide at standup when, based on how urgent it is, and who joins (one or two people, or the whole team).

*Calls and meetings during the day*
- Post in the team chat first and say what you need help with.
- If a call is needed, agree on a time in the chat before starting it.
- Only the people needed join. Check with someone before adding them.
- If something is urgent, say so in the chat, and whoever is free can help.

*Pull requests*
- The PR says what changed, how to test it (when the acceptance criteria are not enough), and `Closes #issue-number`.
- After opening a PR, post it in the channel. Whoever picks it up replies "I'm reviewing it".
- The person who opened the PR fixes comments, resolves conflicts and merges.
- Everyone pulls main after a merge.
