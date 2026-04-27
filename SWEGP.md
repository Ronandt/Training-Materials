# SWEGP — Software Engineering General Practice Assignment

## Overview

This assignment asks you to build a working full-stack web application of your own choosing. You decide what to build — the only constraint is that your project must demonstrate a meaningful selection of the concepts covered in the training track.

You may use the `task-api` backend and `task-ui` frontend from the tutorials as a **starting template**. You can extend them with new features, or start a fresh project using the same stack. Either approach is valid.

---

## What to Build

Choose any application that interests you. It should be something you would plausibly use or show to someone. Ideas to get you started — but do not feel limited to these:

| Idea | Description |
|---|---|
| Budget tracker | Track income and expenses by category; show a monthly summary |
| Recipe manager | Store recipes with ingredients and steps; filter by cuisine or dietary tag |
| Habit tracker | Log daily habits; show streaks and completion history |
| Event board | Create events with dates and attendees; RSVP management |
| Inventory system | Track stock items with quantities; alert when below threshold |
| Link collection | Save and tag URLs; search and filter saved links |
| Simple blog | Create posts with a title, body, and tags; view by tag |
| Job application tracker | Log applications with company, role, status, and notes |

The subject matter is not graded — the implementation is.

---

## Requirements

### Backend (FastAPI + SQLAlchemy + Alembic)

You must implement **all four** of the following:

- [ ] **At least two database models** with a relationship between them (foreign key + `relationship()`)
- [ ] **A complete set of CRUD routes** for at least one resource (list, get by id, create, update, delete)
- [ ] **Pydantic schemas** that separate request shapes from response shapes — no returning ORM objects directly from routes
- [ ] **At least one Alembic migration** — the schema must be managed by migrations, not `create_all()`

You must implement **at least two** of the following:

- [ ] Query filtering via query parameters (e.g. `GET /items?status=active`)
- [ ] A validation rule enforced in Pydantic (e.g. a field must match a pattern, be within a range, or reference a valid foreign key)
- [ ] A route that aggregates data (e.g. counts, totals, groupings) rather than just returning rows
- [ ] `server_default` or `default` used appropriately on at least one column

### Frontend (React + Tailwind + shadcn + TanStack Query)

You must implement **all four** of the following:

- [ ] **At least three routes** using React Router, including at least one dynamic route (`/items/:id`)
- [ ] **A layout component** with navigation that uses `NavLink` for active highlighting
- [ ] **`useQuery`** for all data fetching — no raw `useEffect` + `useState` for server data
- [ ] **`useMutation`** for at least one write operation (create, update, or delete), with `invalidateQueries` or `setQueryData` after success

You must implement **at least two** of the following:

- [ ] A filter or search control that changes the `queryKey` and triggers a re-fetch
- [ ] Error handling shown to the user — not just console errors
- [ ] A loading state shown while a query is in flight
- [ ] An optimistic update using `onMutate` + `onError` rollback

### General

- [ ] The backend and frontend are connected — the frontend calls real API endpoints, not hardcoded data
- [ ] CORS is configured correctly so the frontend can reach the backend
- [ ] The application works end-to-end: a user can perform at least one complete flow (create something, view it, update it, delete it) without the app breaking

---

## What You Are Free to Decide

Everything not listed above is your choice:

- **Subject matter** — build whatever interests you
- **Visual design** — use any shadcn components, Tailwind classes, and layout you like
- **Extra features** — add pagination, sorting, charts, authentication, or anything else you want; it will not count against you
- **Project structure** — organise files however makes sense for your app
- **Naming** — models, routes, and components can be named to suit your domain

---

## Deliverables

Submit a single zip file or repository link containing:

1. **`backend/`** — the FastAPI project with `models.py`, `schemas.py`, `crud.py`, `main.py`, `database.py`, and an `alembic/` directory with at least one migration
2. **`frontend/`** — the Vite + React project
3. **`README.md`** — in the root, containing:
   - What your app does (2–3 sentences)
   - How to run the backend (`pip install`, `alembic upgrade head`, `uvicorn ...`)
   - How to run the frontend (`npm install`, `npm run dev`)
   - A list of which required items from the checklist above you implemented

The README does not need to be long. It just needs to be complete enough for someone else to run your project.

---

## Marking Criteria

| Area | What is assessed |
|---|---|
| **Models and relationships** | Are the models well-structured? Does the foreign key relationship make sense for the domain? |
| **API correctness** | Do routes return appropriate status codes? Are errors handled (404, 409, 422)? |
| **Schema separation** | Are Pydantic request and response schemas distinct and purposeful? |
| **Migration** | Is the schema managed through Alembic? Does `alembic upgrade head` run cleanly on a fresh database? |
| **Data fetching** | Is TanStack Query used correctly — right query keys, correct invalidation after mutations? |
| **UI usability** | Can a user complete the core flow without confusion or broken states? |
| **Code clarity** | Is the code readable? Are names descriptive? Is logic in the right layer (database work in `crud.py`, not in routes)? |

There is no marks for visual polish. A plain but working app scores the same as a visually impressive one.

---

## Using the Template

If you start from the `task-api` / `task-ui` tutorial projects, you must do more than rename things. The new domain, models, and features must be genuinely yours.

Starting from the template is encouraged — it means you already have the project structure, database setup, and CORS configured. The tutorial code gives you a foundation; the assignment asks you to build something real on top of it.

---

## Tips

- **Start with the data model.** Decide what your two (or more) models are and how they relate before writing any routes or frontend code.
- **Get the backend working first.** Test your routes in the FastAPI Swagger UI (`/docs`) before touching the frontend.
- **Run `alembic upgrade head` on a fresh database** before submitting — this is how your work will be tested.
- **Use the Swagger UI to verify status codes.** A route that returns 200 when it should return 201 or 404 is a bug.
- **Commit regularly.** Use descriptive commit messages. The git history is part of the submission.
