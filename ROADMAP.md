# Learning Roadmap

Work through the materials in the order listed below. Each phase builds on the previous one — do not skip ahead.

---

## Quick Reference

| Phase | Topic | File |
|---|---|---|
| 0 | Environment setup | [`fundamentals/setup.md`](fundamentals/setup.md) |
| 1 | VS Code shortcuts and extensions | [`fundamentals/vscode/extensions_shortcuts_tutorial.md`](fundamentals/vscode/extensions_shortcuts_tutorial.md) |
| 2 | Python — pip and venv | [`fundamentals/python/pip_venv_tutorial.md`](fundamentals/python/pip_venv_tutorial.md) |
| 3 | Python — type hints | [`fundamentals/python/type_hinting_tutorial.md`](fundamentals/python/type_hinting_tutorial.md) |
| 4 | HTML | [`fundamentals/html,css,ts/html_tutorial.md`](fundamentals/html,css,ts/html_tutorial.md) |
| 5 | CSS | [`fundamentals/html,css,ts/css_tutorial.md`](fundamentals/html,css,ts/css_tutorial.md) |
| 6 | TypeScript | [`fundamentals/typescript/typescript_tutorial.md`](fundamentals/typescript/typescript_tutorial.md) |
| 7 | Async / Promises | [`fundamentals/typescript/async.md`](fundamentals/typescript/async.md) |
| 8 | FastAPI | [`backend/fastapi/fastapi_tutorial.md`](backend/fastapi/fastapi_tutorial.md) |
| 9 | Pydantic | [`backend/pydantic/pydantic_tutorial.md`](backend/pydantic/pydantic_tutorial.md) |
| 10 | SQLAlchemy | [`backend/sqlalchemy/sqlalchemy_tutorial.md`](backend/sqlalchemy/sqlalchemy_tutorial.md) |
| 11 | Alembic | [`backend/alembic/alembic_tutorial.md`](backend/alembic/alembic_tutorial.md) |
| 12 | React (full frontend stack) | [`frontend/react/react_tutorial.md`](frontend/react/react_tutorial.md) |
| 13 | Architecture report assignment | [`integration & architecture (good luck)/report_assignment.md`](integration%20&%20architecture%20(good%20luck)/report_assignment.md) |
| 14 | SWEGP final project | [`SWEGP.md`](SWEGP.md) |

**Reference (use alongside phases 6–7, not as a sequential read):**
[`fundamentals/typescript/typescript_reference_advanced.md`](fundamentals/typescript/typescript_reference_advanced.md)

---

## Phase 0 — Environment Setup

**[`fundamentals/setup.md`](fundamentals/setup.md)**

Install everything before writing a single line of code. This guide covers VS Code, Git, GitHub Desktop, Python, and Node.js — verified with terminal commands at each step.

> Complete this first. Nothing else works without it.

---

## Phase 1 — Tooling

**[`fundamentals/vscode/extensions_shortcuts_tutorial.md`](fundamentals/vscode/extensions_shortcuts_tutorial.md)**

Learn the editor you will use for everything. Keyboard shortcuts, the integrated terminal, multi-cursor editing, and the extensions that make Python and TypeScript development fast. Time spent here pays back on every task that follows.

---

## Phase 2 — Python Package Management

**[`fundamentals/python/pip_venv_tutorial.md`](fundamentals/python/pip_venv_tutorial.md)**

Learn how Python projects manage dependencies. Creating virtual environments, installing and pinning packages, and understanding `requirements.txt`. The FastAPI and SQLAlchemy tutorials run inside a venv — this is the prerequisite.

---

## Phase 3 — Python Type Hints

**[`fundamentals/python/type_hinting_tutorial.md`](fundamentals/python/type_hinting_tutorial.md)**

Python is dynamically typed, but modern Python code uses type annotations everywhere — especially in FastAPI and Pydantic, where types drive automatic validation. This tutorial covers the annotation syntax you will see constantly in the backend track.

---

## Phase 4 — HTML

**[`fundamentals/html,css,ts/html_tutorial.md`](fundamentals/html,css,ts/html_tutorial.md)**

Learn how a web page is structured. Elements, attributes, forms, semantic HTML. JSX in React is HTML-like — understanding real HTML makes React components intuitive. No tools needed: just a text file and a browser.

---

## Phase 5 — CSS

**[`fundamentals/html,css,ts/css_tutorial.md`](fundamentals/html,css,ts/css_tutorial.md)**

Learn how a web page is styled. Selectors, the box model, typography, and Flexbox layout. Every Tailwind CSS utility class in the React tutorial maps to a regular CSS property — understanding CSS first makes Tailwind obvious rather than magic.

> Do phases 4 and 5 before the React tutorial, not during it.

---

## Phase 6 — TypeScript

**[`fundamentals/typescript/typescript_tutorial.md`](fundamentals/typescript/typescript_tutorial.md)**

TypeScript is JavaScript with types. The tutorial explains it by analogy to Python — variables, control flow, functions, arrays, and objects. By the end you will have built a typed task manager. All frontend code in this track is TypeScript.

**Reference:** [`fundamentals/typescript/typescript_reference_advanced.md`](fundamentals/typescript/typescript_reference_advanced.md) — a lookup document for advanced type features. Bookmark it; return to it when you encounter unfamiliar syntax in the later tutorials.

---

## Phase 7 — Async / Promises

**[`fundamentals/typescript/async.md`](fundamentals/typescript/async.md)**

JavaScript is single-threaded. Promises and `async/await` are how it handles waiting for network requests without freezing. Every API call in the React tutorial uses `async/await` — this tutorial explains why it works the way it does.

> Complete phases 6 and 7 before starting the backend or frontend tracks.

---

## Phase 8 — FastAPI

**[`backend/fastapi/fastapi_tutorial.md`](backend/fastapi/fastapi_tutorial.md)**

Build a REST API in Python. Routes, path and query parameters, request bodies, HTTP status codes, and in-memory CRUD. The API you build here — the Task Manager — is the project you will carry through the remaining backend tutorials and connect to the frontend.

---

## Phase 9 — Pydantic

**[`backend/pydantic/pydantic_tutorial.md`](backend/pydantic/pydantic_tutorial.md)**

Pydantic validates data using Python type annotations. This tutorial goes deeper than the basic models in the FastAPI tutorial: validators, nested models, serialisation, and the production-quality schemas (`UserCreate`, `TaskResponse`, etc.) you will import in the SQLAlchemy tutorial.

> This deepens the FastAPI tutorial — complete phase 8 first.

---

## Phase 10 — SQLAlchemy

**[`backend/sqlalchemy/sqlalchemy_tutorial.md`](backend/sqlalchemy/sqlalchemy_tutorial.md)**

Replace the in-memory store with a real database. ORM models, sessions, CRUD through SQLAlchemy, and table relationships. By the end, the Task Manager API reads and writes to SQLite. The same ORM code works with PostgreSQL in production.

> Requires: FastAPI tutorial (phase 8), Pydantic tutorial (phase 9).

---

## Phase 11 — Alembic

**[`backend/alembic/alembic_tutorial.md`](backend/alembic/alembic_tutorial.md)**

Manage schema changes safely. Alembic generates versioned migration scripts from your SQLAlchemy models — the correct replacement for `create_all()` and `reset_db()` in any real project. Covers autogenerate, upgrade/downgrade, data migrations, and the three-step pattern for adding a `NOT NULL` column safely.

> Requires: SQLAlchemy tutorial (phase 10). This is the final piece of the backend track.

---

## Phase 12 — React (Full Frontend Stack)

**[`frontend/react/react_tutorial.md`](frontend/react/react_tutorial.md)**

Build the frontend that connects to the backend you built in phases 8–11. One tutorial, one project, seven technologies introduced in sequence:

| Introduced | Purpose |
|---|---|
| Vite | Build tool and dev server |
| React | Component model and UI |
| Tailwind CSS | Utility-first styling |
| shadcn/ui | Accessible pre-built components |
| React Router | Client-side routing |
| Axios | HTTP client |
| TanStack Query | Server state management (replaces raw `useEffect` for data fetching) |

Each section of the tutorial adds one technology to the same project, so by the end everything is wired together into a working Task Manager UI.

> Requires: HTML (phase 4), CSS (phase 5), TypeScript + async (phases 6–7), and a running backend (phases 8–11).

---

## Phase 13 — Architecture Report Assignment

**[`integration & architecture (good luck)/report_assignment.md`](integration%20&%20architecture%20(good%20luck)/report_assignment.md)**

Read and explore the Architecture Sample App — a production-style template that adds authentication, role-based access control, and a more complex backend structure. The assignment asks you to understand unfamiliar code, run it locally, and present how it works. This is deliberate practice at the skill of reading existing systems.

Setup guides:
- [`integration & architecture (good luck)/template_setup_backend.md`](integration%20&%20architecture%20(good%20luck)/template_setup_backend.md)
- [`integration & architecture (good luck)/template_setup_frontend.md`](integration%20&%20architecture%20(good%20luck)/template_setup_frontend.md)

> Do this after completing the full backend and frontend tracks.

---

## Phase 14 — SWEGP Final Project

**[`SWEGP.md`](SWEGP.md)**

Build a full-stack application of your own choosing. You choose the subject; the assignment specifies which concepts from the track you must demonstrate. You may use the Task Manager as a starting template or begin from scratch.

> This is the capstone. Complete all prior phases before starting.

---

## Dependency Map

```
setup.md
    └── vscode tutorial
            ├── pip/venv tutorial
            │       └── type hints tutorial
            │               ├── FastAPI tutorial
            │               │       └── Pydantic tutorial
            │               │               └── SQLAlchemy tutorial
            │               │                       └── Alembic tutorial ──────┐
            │               └── (backend complete)                              │
            └── html tutorial                                                   │
                    └── css tutorial                                            │
                            └── TypeScript tutorial                            │
                                    └── async tutorial                         │
                                            └── React tutorial ────────────────┘
                                                    └── Architecture report
                                                            └── SWEGP project
```
