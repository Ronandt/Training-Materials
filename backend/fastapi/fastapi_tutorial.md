# FastAPI Exercises

FastAPI is a Python web framework for building REST APIs. It validates request and response data automatically using Pydantic, and generates interactive API documentation with no extra work.

Work through each section in order. Every exercise has something to run in your terminal.

**This tutorial is standalone — no database required.** You will use an in-memory Python list as a data store. The data resets every time you restart the server, but that is fine for learning the framework.

Two continuation tutorials build on this one:
- **Pydantic (continuation):** Deeper validation, nested models, serialization patterns
- **SQLAlchemy (continuation):** Replace the in-memory store with a real database

**Reference:** [FastAPI docs](https://fastapi.tiangolo.com)

## 0. Setup

Create a project folder and virtual environment:

```bash
mkdir task-api
cd task-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate.bat
```

Install FastAPI and Uvicorn:

```bash
pip install fastapi "uvicorn[standard]"
```

`uvicorn[standard]` includes optional extras for better performance. Verify:

```bash
uvicorn --version
```

## 1. Your First API

A FastAPI app is a Python object. Routes are functions decorated with HTTP method decorators — `@app.get`, `@app.post`, etc. Whatever the function returns is serialised to JSON automatically.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, world"}
```

Save this as `main.py` and start the server:

```bash
uvicorn main:app --reload
```

- `main` — the filename without `.py`
- `app` — the FastAPI instance
- `--reload` — restarts the server automatically on every file save

Open `http://localhost:8000` in your browser. You will see the JSON response.

### 1.1

FastAPI generates interactive API documentation automatically. Open:

- `http://localhost:8000/docs` — Swagger UI (try requests directly in the browser)
- `http://localhost:8000/redoc` — ReDoc (clean readable format)

Find your `/` endpoint in the Swagger UI. Click it, then click **Try it out** and **Execute**. You will see the request and response without writing any test code.

### 1.2

Add two more endpoints to `main.py`:

- `GET /health` — returns `{"status": "ok"}`
- `GET /version` — returns `{"version": "0.1.0"}`

Save the file. Uvicorn reloads automatically. Verify both in the browser and in the Swagger UI.

### 1.3

Functions can be `async`. For now, everything is synchronous — but FastAPI supports both:

```python
@app.get("/ping")
async def ping():
    return {"ping": "pong"}
```

Add an async `GET /ping` endpoint. It behaves identically to a sync function here. You will use `async` more in the SQLAlchemy continuation when working with async database drivers.

## 2. Path and Query Parameters

### 2.1

There are two ways to pass data to an endpoint through the URL. Understanding the difference matters because they communicate different things about how the resource is identified.

**Path parameters** identify a specific resource. They are part of the URL structure itself:

```
GET /tasks/42        ← 42 is the path parameter: which task?
GET /users/7/tasks   ← 7 identifies the user; tasks is the sub-resource
```

**Query parameters** filter, sort, or configure how a resource is returned. They appear after `?` and are optional by convention:

```
GET /tasks?status=todo          ← filter tasks by status
GET /tasks?limit=10&offset=20   ← pagination
GET /tasks?sort=priority        ← sorting
```

The rule of thumb: if removing the parameter would make the URL meaningless or point to a different resource, it is a path parameter. If removing it just changes what you get back from the same collection, it is a query parameter.

| | Path parameter | Query parameter |
|---|---|---|
| Position | Inside the URL path | After `?` |
| Purpose | Identify a resource | Filter or configure the response |
| Required | Always | Usually optional |
| Example | `/tasks/42` | `/tasks?status=todo` |

In FastAPI, path parameters are declared with `{name}` in the route and as typed function parameters. FastAPI validates and converts the type automatically:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

Any function parameter **not** in the path string is treated as a query parameter:

```python
@app.get("/tasks")
def list_tasks(status: str | None = None, limit: int = 10):
    return {"status": status, "limit": limit}
```

Add both endpoints. Test:
- `http://localhost:8000/tasks/5` → path parameter, returns the specific task id
- `http://localhost:8000/tasks/abc` → FastAPI rejects it with 422 before your function runs
- `http://localhost:8000/tasks?status=todo&limit=5` → query parameters, filters the list

Open the Swagger UI and compare how the two endpoints look in the docs — path parameters appear in the URL template, query parameters appear as a separate inputs panel below it.

### 2.2

Add a `GET /users/{user_id}` endpoint alongside the task endpoints from 2.1. Then experiment with required vs optional parameters — add a `GET /search` endpoint that has a **required** `q` query parameter (no default):

```python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

Call `/search` without `?q=` — FastAPI returns 422 automatically. Call it with `?q=hello` — it works. This is the same mechanism as path parameters: both enforce their type and presence before your function runs.

### 2.3

Add validation constraints to query parameters using `Annotated` and `Query`:

```python
from typing import Annotated
from fastapi import Query

@app.get("/tasks")
def list_tasks(
    status: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return {"status": status, "limit": limit, "offset": offset}
```

Update your endpoint to include `offset` for pagination. Test that `?limit=0` and `?limit=200` both return 422 errors.

### 2.4 — Challenge

Add a `GET /users/{user_id}/tasks` endpoint with an optional `?priority=` query parameter. For now, return a hardcoded list. The point is to combine a path parameter and a query parameter in the same endpoint — confirm both appear correctly in the Swagger docs.

## 3. Request Bodies and Pydantic Models (Basic)

POST and PATCH endpoints receive data in the request body. Declare the body type as a Pydantic model — FastAPI validates it automatically and shows the schema in the docs.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return item
```

FastAPI detects that `item` is a Pydantic model (not a path or query parameter) and reads it from the request body.

**Common mistake:** on a POST or PUT endpoint, a plain primitive like `user_id: int` is still a query parameter — not a body field. Only Pydantic model parameters are read from the body. If you need an integer in the body, put it inside a model.

```python
# user_id here is a query param (?user_id=5), not in the body
@app.post("/tasks")
def create_task(task: TaskCreate, user_id: int):
    ...

# to receive user_id in the body, add it to the model instead
class TaskCreate(BaseModel):
    title: str
    user_id: int
```

### 3.1

Define these two models in `main.py`:

```python
from pydantic import BaseModel
from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: str

class TaskCreate(BaseModel):
    title: str
    priority: Literal["low", "medium", "high"] = "medium"
    owner_id: int
```

Add a `POST /users` endpoint that accepts a `UserCreate` body and returns it. Open the Swagger UI — the expected request shape appears automatically. Click **Try it out** and submit a valid body, then try submitting one with a missing field.

### 3.2

Add response models. `response_model` tells FastAPI which Pydantic model to use for the output — it filters out extra fields and validates the response:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}
```

Update `POST /users` to use `response_model=UserResponse` and return a hardcoded `id`. Notice the response schema now appears in the docs alongside the request schema.

### 3.3

Define `TaskResponse` and add a `POST /tasks` endpoint:

```python
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["todo", "in-progress", "done"]
    owner_id: int
```

The endpoint should accept `TaskCreate` and return `TaskResponse`. Hardcode `status="todo"` and `id=1` for now. Verify the schemas in the Swagger docs.

### 3.4 — Challenge

Add an optional `description: str | None = None` field to both `TaskCreate` and `TaskResponse`. Confirm that the field is optional in requests (the Swagger UI marks it accordingly) and that it appears in responses when provided.

## 4. HTTP Errors and Status Codes

### 4.1

Raise `HTTPException` to return an error response:

```python
from fastapi import HTTPException

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id > 100:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "title": "Example task"}
```

Update your `GET /tasks/{task_id}` endpoint to raise a 404 for ids above 100 (a placeholder — you will replace this with real lookups in section 5). Test it in the browser and the Swagger UI.

### 4.2

Use named status code constants from FastAPI instead of raw integers:

```python
from fastapi import status

raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
```

Update all your error responses to use named constants. Add 409 handling to `POST /users` if the email is `"taken@example.com"` (a temporary hardcoded check).

### 4.3

Override the default success status code. Creations should return `201 Created`, not `200 OK`:

```python
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    ...
```

Update both `POST /users` and `POST /tasks` to return 201. Verify with curl:

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
# should print: 201
```

### 4.4 — Challenge

Add a `DELETE /tasks/{task_id}` endpoint. A successful delete returns `204 No Content` — no body. Use `Response` to return an empty 204:

```python
from fastapi import Response

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id > 100:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

Test that a valid id returns 204 with no body, and an invalid id returns 404.

## 5. In-Memory CRUD

Replace the hardcoded responses with a real (in-memory) data store. Use Python lists and a simple counter for ids. The data lives only as long as the server is running — that is fine.

```python
# at the top of main.py, outside any function
users_db: list[dict] = []
tasks_db: list[dict] = []
next_user_id = 1
next_task_id = 1
```

### 5.1

Rewrite `POST /users` to store the new user in `users_db`:

```python
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global next_user_id
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    new_user = {"id": next_user_id, **user.model_dump()}
    users_db.append(new_user)
    next_user_id += 1
    return new_user
```

Test it by creating two users with different emails, then try the same email twice — confirm the 409.

### 5.2

Rewrite `GET /users` and `GET /users/{user_id}` to read from `users_db`:

```python
@app.get("/users", response_model=list[UserResponse])
def list_users():
    return users_db

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
```

Create a few users, then list them and fetch individual ones by id.

### 5.3

Rewrite `POST /tasks` to store tasks. Validate that `owner_id` refers to a real user:

```python
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_task_id
    owner = next((u for u in users_db if u["id"] == task.owner_id), None)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Owner not found")
    new_task = {"id": next_task_id, "status": "todo", **task.model_dump()}
    tasks_db.append(new_task)
    next_task_id += 1
    return new_task
```

### 5.4

Add a `PATCH /tasks/{task_id}` endpoint. Define a `TaskUpdate` model where every field is optional:

```python
class TaskUpdate(BaseModel):
    title: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    status: Literal["todo", "in-progress", "done"] | None = None
    description: str | None = None
```

The endpoint should apply only the fields the caller provided:

```python
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    for field, value in updates.model_dump(exclude_none=True).items():
        task[field] = value
    return task
```

Test by patching only the `status` field — confirm `title` and `priority` are unchanged.

### 5.5 — Challenge

Rewrite `GET /tasks` to filter by `status` and `priority` when provided, and apply `limit` and `offset` for pagination:

```python
@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    ...
```

Test with several tasks of different statuses and priorities. Confirm filtering and pagination work correctly.

## 6. Putting It Together

### Final Exercise

Complete `main.py` as a working in-memory Task Manager API. No hardcoded responses — every endpoint reads from or writes to `users_db` and `tasks_db`.

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

## Checklist

- [ ] Can create a FastAPI app and run it with uvicorn
- [ ] Know where to find the auto-generated docs and how to use them
- [ ] Can declare path parameters with types and understand the automatic validation
- [ ] Can declare optional and required query parameters
- [ ] Can add constraints to query parameters with `Query()`
- [ ] Can define a Pydantic model and use it as a request body
- [ ] Can set `response_model` and understand what it enforces on the output
- [ ] Can set custom HTTP status codes for success responses
- [ ] Can raise `HTTPException` with the correct status code and detail
- [ ] Can use named status code constants from `fastapi.status`
- [ ] Can implement all four CRUD operations using an in-memory store
- [ ] All 8 endpoints in the final exercise work correctly end-to-end
