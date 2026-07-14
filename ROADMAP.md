# Learning Roadmap

Work through the materials in the order listed below. Each phase builds on the previous one — do not skip ahead, except where noted that a phase is independent.

---

## Quick Reference

| Phase | Topic | File |
|---|---|---|
| 0 | Environment setup | [`fundamentals/setup.md`](fundamentals/setup.md) |
| 1 | Python — pip and venv | [`fundamentals/python/pip_venv_tutorial.md`](fundamentals/python/pip_venv_tutorial.md) |
| 2 | Python — type hints | [`fundamentals/python/type_hinting_tutorial.md`](fundamentals/python/type_hinting_tutorial.md) |
| 3 | HTML | [`fundamentals/html,css,ts/html_tutorial.md`](fundamentals/html,css,ts/html_tutorial.md) |
| 4 | CSS | [`fundamentals/html,css,ts/css_tutorial.md`](fundamentals/html,css,ts/css_tutorial.md) |
| 5 | The DOM | [`fundamentals/html,css,ts/dom_tutorial.md`](fundamentals/html,css,ts/dom_tutorial.md) |
| 6 | TypeScript | [`fundamentals/typescript/typescript_tutorial.md`](fundamentals/typescript/typescript_tutorial.md) |
| 7 | Async / Promises | [`fundamentals/typescript/async.md`](fundamentals/typescript/async.md) |
| 8 | FastAPI | [`backend/fastapi/fastapi_tutorial.md`](backend/fastapi/fastapi_tutorial.md) |
| 9 | Pydantic | [`backend/pydantic/pydantic_tutorial.md`](backend/pydantic/pydantic_tutorial.md) |
| 10 | SQLAlchemy | [`backend/sqlalchemy/sqlalchemy_tutorial.md`](backend/sqlalchemy/sqlalchemy_tutorial.md) |
| 11 | React — setup, styling & routing | [`frontend/react/react_styling_tutorial.md`](frontend/react/react_styling_tutorial.md) |
| 12 | React — connecting to a public API | [`frontend/react/react_api_tutorial.md`](frontend/react/react_api_tutorial.md) |
| 13 | Architecture report assignment | [`integration & architecture (good luck)/report_assignment.md`](integration%20&%20architecture%20(good%20luck)/report_assignment.md) |
| 14 | SWEGP final project | [`SWEGP.md`](SWEGP.md) |

**Reference material (not sequential phases — dip into these alongside the phase noted):**

| Use alongside | Topic | File |
|---|---|---|
| Phase 0 | VS Code shortcuts and extensions | [`references/vscode/extensions_shortcuts_tutorial.md`](references/vscode/extensions_shortcuts_tutorial.md) |
| Phase 6 | TypeScript — advanced types | [`fundamentals/typescript/typescript_reference_advanced.md`](fundamentals/typescript/typescript_reference_advanced.md) |
| Phase 10 | Alembic — database migrations | [`references/alembic/alembic_tutorial.md`](references/alembic/alembic_tutorial.md) |

**Note on structure:** most tutorials below are now a short video plus a condensed reference doc (concepts and syntax to look up), each ending in one concrete hands-on build rather than many small guided exercises. Phases 8–10 (FastAPI/Pydantic/SQLAlchemy) share a single video and build one continuous project (`task-api`) across all three. Phases 11–12 (React) are a separate two-part project and — importantly — **no longer depend on the backend track**: part 2 connects to [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a public fake REST API, not to the API you build in phases 8–10.

---

## Phase 0 — Environment Setup

**[`fundamentals/setup.md`](fundamentals/setup.md)**

Install everything before writing a single line of code. This guide covers VS Code, Git, GitHub Desktop, Python, and Node.js — verified with terminal commands at each step.

> Complete this first. Nothing else works without it.

**Reference:** [`references/vscode/extensions_shortcuts_tutorial.md`](references/vscode/extensions_shortcuts_tutorial.md) — keyboard shortcuts, the integrated terminal, and the extensions that make Python and TypeScript development fast (Prettier and its formatter settings, in particular). Not a blocking step — dip into it whenever your editor is slowing you down.

---

## Phase 1 — Python Package Management

**[`fundamentals/python/pip_venv_tutorial.md`](fundamentals/python/pip_venv_tutorial.md)**

Learn how Python projects manage dependencies. Creating virtual environments, installing and pinning packages, and understanding `requirements.txt`. The FastAPI and SQLAlchemy tutorials run inside a venv — this is the prerequisite. Includes a companion video on setting up a venv in VS Code.

---

## Phase 2 — Python Type Hints

**[`fundamentals/python/type_hinting_tutorial.md`](fundamentals/python/type_hinting_tutorial.md)**

Python is dynamically typed, but modern Python code uses type annotations everywhere — especially in FastAPI and Pydantic, where types drive automatic validation. This is a video + reference doc: watch the video, then use the syntax reference (basics, collections, `Optional`/`Union`, `TypedDict`/`dataclass`, mypy) as a lookup while working through the backend track.

---

## Phase 3 — HTML

**[`fundamentals/html,css,ts/html_tutorial.md`](fundamentals/html,css,ts/html_tutorial.md)**

Learn how a web page is structured. Elements, attributes, forms, semantic HTML. JSX in React is HTML-like — understanding real HTML makes React components intuitive. No tools needed: just a text file and a browser.

---

## Phase 4 — CSS

**[`fundamentals/html,css,ts/css_tutorial.md`](fundamentals/html,css,ts/css_tutorial.md)**

Learn how a web page is styled. Selectors, the box model, typography, and Flexbox layout. Every Tailwind CSS utility class in the React tutorial maps to a regular CSS property — understanding CSS first makes Tailwind obvious rather than magic.

> Do phases 3 and 4 before the React tutorial, not during it.

---

## Phase 5 — The DOM

**[`fundamentals/html,css,ts/dom_tutorial.md`](fundamentals/html,css,ts/dom_tutorial.md)**

A static page displays content but does nothing when you interact with it — the DOM is the browser's live, in-memory model of the page that JavaScript reads and changes. Video + reference notes on selecting elements, event listeners, handling form submission, and creating elements dynamically. Plain JavaScript, no TypeScript or build tooling — this is what React abstracts away later.

---

## Phase 6 — TypeScript

**[`fundamentals/typescript/typescript_tutorial.md`](fundamentals/typescript/typescript_tutorial.md)**

TypeScript is JavaScript with types. Video + a condensed syntax reference organised by topic — variables, control flow, functions, arrays, objects/interfaces, classes, generics, modules, error handling — explained by analogy to Python throughout. Use it as a lookup while writing the React tutorial, rather than reading it end to end first.

**Reference:** [`fundamentals/typescript/typescript_reference_advanced.md`](fundamentals/typescript/typescript_reference_advanced.md) — a lookup document for advanced type features. Bookmark it; return to it when you encounter unfamiliar syntax in the later tutorials.

---

## Phase 7 — Async / Promises

**[`fundamentals/typescript/async.md`](fundamentals/typescript/async.md)**

JavaScript is single-threaded. Promises and `async/await` are how it handles waiting for network requests without freezing — covered here with a plain-language explanation, a restaurant-waiter analogy, a video, and reference notes (Promises, async/await, running things in parallel, `fetch`, common mistakes). Every API call in the React tutorial uses `async/await`.

> Complete phases 6 and 7 before starting the backend or frontend tracks.

---

## Phase 8 — FastAPI

**[`backend/fastapi/fastapi_tutorial.md`](backend/fastapi/fastapi_tutorial.md)**

Build a REST API in Python. Video + reference notes on routes, path/query parameters, request bodies, HTTP status codes, and in-memory CRUD, followed by one Final Project: build `main.py` for the Task Manager API — the project you carry through the remaining backend tutorials. Standalone — no database required yet.

---

## Phase 9 — Pydantic

**[`backend/pydantic/pydantic_tutorial.md`](backend/pydantic/pydantic_tutorial.md)**

Pydantic validates data using Python type annotations. This project deliberately keeps to **two models — `User` and `Task`** — instead of a separate Create/Response pair per entity; an `id: int | None = None` field plus `model_copy(update=...)` does that job instead. Reference notes cover constraints, defaults, that `id` pattern, validators, and serialization, ending in one Final Project: build `schemas.py`, imported directly by the SQLAlchemy tutorial.

> Same video as phase 8 (it covers Pydantic, FastAPI, and SQLAlchemy together) — jump to the Pydantic section.

---

## Phase 10 — SQLAlchemy

**[`backend/sqlalchemy/sqlalchemy_tutorial.md`](backend/sqlalchemy/sqlalchemy_tutorial.md)**

Replace the in-memory store with a real database. Reference notes cover the engine/session, ORM models, table creation, CRUD, and relationships, ending in one Final Project: build `crud.py` and wire it into `main.py`. The ORM classes are named `UserModel`/`TaskModel` (not `User`/`Task`) specifically to avoid colliding with the Pydantic schemas of the same name once both are imported into `crud.py`. By the end, the Task Manager API reads and writes to SQLite — the same ORM code works with PostgreSQL in production. This is the final piece of the backend track.

> Requires: FastAPI tutorial (phase 8), Pydantic tutorial (phase 9) — `schemas.py` must already exist.

**Reference:** [`references/alembic/alembic_tutorial.md`](references/alembic/alembic_tutorial.md) — once you're comfortable with the ORM models above, this covers managing schema changes safely with versioned migrations (the correct replacement for `create_all()`/`reset_db()` in a real project). Optional deep-dive, not required to move on to React.

---

## Phase 11 — React, Part 1: Setup, Styling & Routing

**[`frontend/react/react_styling_tutorial.md`](frontend/react/react_styling_tutorial.md)**

Get a real, navigable, styled app running before ever calling an API:

| Introduced | Purpose |
|---|---|
| Vite | Build tool and dev server |
| React | Component model and UI |
| Tailwind CSS | Utility-first styling |
| shadcn/ui | Accessible pre-built components |
| React Router | Client-side routing |

Ends with a styled `task-ui` project with placeholder pages and working navigation — part 2 continues the exact same project.

> Requires: HTML (phase 3), CSS (phase 4), TypeScript (phase 6), async (phase 7). The DOM tutorial (phase 5) isn't a hard prerequisite but explains what React is abstracting away.

---

## Phase 12 — React, Part 2: Connecting to a Public API

**[`frontend/react/react_api_tutorial.md`](frontend/react/react_api_tutorial.md)**

Wire the same project up to [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — a free public fake REST API — using Axios and TanStack Query:

| Introduced | Purpose |
|---|---|
| Axios | HTTP client |
| TanStack Query | Server state management (replaces raw `useEffect` for data fetching) |

Every hook lives in its own file (`src/hooks/`), every presentational piece is a separate component with no data-fetching in it (`src/components/`), and pages (`src/pages/`) only compose the two — the final exercise requires no `useQuery`/`useMutation` calls inside a page file. JSONPlaceholder doesn't persist writes, which the tutorial uses deliberately to demonstrate what the TanStack Query cache is actually doing for you.

> Requires: React Part 1 (phase 11) only. **Does not require the backend track** — this is intentionally decoupled from phases 8–10, so it can be done independently of them.

---

## Phase 13 — Architecture Report Assignment

**[`integration & architecture (good luck)/report_assignment.md`](integration%20&%20architecture%20(good%20luck)/report_assignment.md)**

Read and explore the Architecture Sample App — a production-style template that adds authentication, role-based access control, and a more complex backend structure. The assignment asks you to understand unfamiliar code, run it locally, and present how it works. This is deliberate practice at the skill of reading existing systems.

Setup guides:
- [`integration & architecture (good luck)/template_setup_backend.md`](integration%20&%20architecture%20(good%20luck)/template_setup_backend.md)
- [`integration & architecture (good luck)/template_setup_frontend.md`](integration%20&%20architecture%20(good%20luck)/template_setup_frontend.md)

> Do this after completing both the backend track (phases 8–10) and the frontend track (phases 11–12) — even though phase 12 itself didn't require the backend, this assignment does, since it's a real connected full-stack app.

---

## Phase 14 — SWEGP Final Project

**[`SWEGP.md`](SWEGP.md)**

Build a full-stack application of your own choosing. You choose the subject; the assignment specifies which concepts from the track you must demonstrate. You may use the Task Manager as a starting template or begin from scratch.

> This is the capstone. Complete all prior phases before starting.

---

## Dependency Map

```
setup.md
    ├── pip/venv tutorial
    │       └── type hints tutorial
    │               └── FastAPI tutorial
    │                       └── Pydantic tutorial
    │                               └── SQLAlchemy tutorial
    │                                       (backend track complete) ───┐
    └── html tutorial                                                    │
            └── css tutorial                                             │
                    └── DOM tutorial                                     │
                            └── TypeScript tutorial                      │
                                    └── async tutorial                   │
                                            └── React (styling)          │
                                                    └── React (API — standalone) │
                                                       (frontend track complete) │
                                                               │                 │
                                                               └────────┬────────┘
                                                                        └── Architecture report
                                                                                └── SWEGP project
```

Reference docs (VS Code shortcuts, advanced TypeScript, Alembic) sit outside this chain — dip into them at the phase noted above, but nothing downstream is blocked on them.

Note the frontend track (phases 3–7, 11–12) no longer merges into the backend track partway through — React connects to a public API on its own, and the two tracks only come together at the Architecture report, which is the first place a real connected full-stack app matters.
