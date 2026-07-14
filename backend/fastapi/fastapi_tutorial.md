# FastAPI Reference

FastAPI is a Python web framework for building REST APIs. It validates request and response data automatically using Pydantic, and generates interactive API documentation with no extra work.

**This tutorial is standalone — no database required.** You will use an in-memory Python list as a data store. The data resets every time you restart the server, but that is fine for learning the framework.

Two continuation tutorials build on this one:
- **Pydantic (continuation):** Deeper validation, defaults, nested models, serialization
- **SQLAlchemy (continuation):** Replace the in-memory store with a real database

## Video

[FastAPI for Beginners — Python Web Framework](https://www.youtube.com/watch?v=Lu8lXXlstvM) (Telusko) — this single course covers Pydantic, FastAPI, and SQLAlchemy.

## Resources

- [FastAPI docs](https://fastapi.tiangolo.com)

## Setup

```bash
mkdir task-api
cd task-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate.bat

pip install fastapi "uvicorn[standard]"
```

## Reference

**Your first API.** A FastAPI app is a Python object; routes are functions decorated with HTTP method decorators. Whatever the function returns is serialised to JSON automatically:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, world"}
```

```bash
uvicorn main:app --reload
```

Interactive docs are generated automatically at `/docs` (Swagger UI, lets you try requests in the browser) and `/redoc`. Functions can be `async def` — FastAPI supports both sync and async handlers identically at this level; async matters once you're awaiting a database driver.

**Path vs query parameters.** Path parameters identify a specific resource and live inside the URL (`/tasks/{task_id}`); query parameters filter or configure the response and come after `?` (`/tasks?status=todo`). Any function parameter that appears in the path string is a path parameter — everything else becomes a query parameter, optional if it has a default:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}

@app.get("/tasks")
def list_tasks(status: str | None = None, limit: int = 10):
    return {"status": status, "limit": limit}
```

FastAPI validates and converts the type before your function runs — `/tasks/abc` against `task_id: int` returns 422 automatically. Add constraints to query parameters with `Annotated` and `Query`:

```python
from typing import Annotated
from fastapi import Query

@app.get("/tasks")
def list_tasks(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    ...
```

**Request bodies.** POST/PATCH endpoints read a Pydantic model from the body — FastAPI detects the model parameter and reads it from JSON, not the query string. A plain primitive like `user_id: int` on a POST is still a query parameter; only Pydantic model parameters come from the body:

```python
from pydantic import BaseModel
from typing import Literal

class User(BaseModel):
    id: int | None = None
    name: str
    email: str

class Task(BaseModel):
    id: int | None = None
    title: str
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["todo", "in-progress", "done"] = "todo"
    owner_id: int

@app.post("/users", response_model=User)
def create_user(user: User):
    return user.model_copy(update={"id": 1})
```

This project keeps to **two models total** (see the Pydantic tutorial) — `id: int | None = None` plus `model_copy(update=...)` does the job a separate response model would otherwise do, since request and response share the same shape.

**Errors and status codes.** Raise `HTTPException` for error responses, using named constants from `fastapi.status` instead of raw integers. Override the default 200 with `status_code` for correct success codes (`201` for creation, `204` for a body-less delete):

```python
from fastapi import HTTPException, status, Response

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    ...

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    ...
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

**In-memory CRUD.** Store model instances directly in a list, with a counter standing in for auto-increment ids:

```python
users_db: list[User] = []
tasks_db: list[Task] = []
next_user_id = 1
next_task_id = 1

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    global next_user_id
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    new_user = user.model_copy(update={"id": next_user_id})
    users_db.append(new_user)
    next_user_id += 1
    return new_user
```

For partial updates (`PATCH`), since there's no dedicated update schema, accept a plain `dict` body and merge it with `model_copy`:

```python
@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updates: dict):
    index = next((i for i, t in enumerate(tasks_db) if t.id == task_id), None)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated = tasks_db[index].model_copy(update=updates)
    tasks_db[index] = updated
    return updated
```

The tradeoff: a raw `dict` body isn't field-validated before the merge, so a typo'd key is silently ignored rather than rejected with a 422. Worth it here to avoid a third model; a larger project might add one back.

## Final Project

Build `main.py` in your `task-api` folder as a working in-memory Task Manager API. Every endpoint reads from or writes to `users_db` and `tasks_db` — no hardcoded responses.

**Full API contract:**

| Method  | Path               | Success | Errors                           |
|---------|--------------------|---------|----------------------------------|
| `GET`   | `/users`           | 200     |                                  |
| `POST`  | `/users`           | 201     | 409 duplicate email              |
| `GET`   | `/users/{id}`      | 200     | 404 not found                    |
| `GET`   | `/tasks`           | 200     | 422 invalid query params         |
| `POST`  | `/tasks`           | 201     | 422 if owner not found           |
| `GET`   | `/tasks/{id}`      | 200     | 404 not found                    |
| `PATCH` | `/tasks/{id}`      | 200     | 404 not found                    |
| `DELETE`| `/tasks/{id}`      | 204     | 404 not found                    |

`GET /tasks` also supports `?status=`, `?priority=` filtering and `?limit=`/`?offset=` pagination (`limit` 1–100, `offset` ≥ 0).

**Verification** — run through this sequence in the Swagger UI at `http://localhost:8000/docs`:

1. Create two users with different emails
2. Try creating a duplicate email — confirm 409
3. List all users — confirm both appear
4. Create three tasks assigned to different users, with different priorities
5. Try creating a task with a non-existent `owner_id` — confirm 422
6. List all tasks, then filter by `?status=todo`, then by `?priority=high`
7. Fetch a specific task by id
8. Patch a task's status to `"in-progress"` — confirm only that field changed
9. Delete a task — confirm 204 with no body
10. Try deleting the same task again — confirm 404
