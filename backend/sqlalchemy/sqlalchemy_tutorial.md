# SQLAlchemy Exercises

SQLAlchemy is Python's most widely used database toolkit. It has two layers: Core (raw SQL expression language) and ORM (maps Python classes to database tables). This tutorial covers the ORM — which is what you will use with FastAPI.

Work through each section in order. Every exercise has something to run in your terminal.

**This is a continuation of the FastAPI tutorial.** The FastAPI tutorial stored data in an in-memory Python list. This tutorial replaces that with a real database. By the end, you will swap out the in-memory store in `main.py` for SQLAlchemy — everything else in the API stays the same.

**Track order:**
- **FastAPI tutorial:** Build a working in-memory API ✓
- **Pydantic tutorial:** Production-quality schemas ✓ (recommended before this)
- **SQLAlchemy (this file):** Add a real database

**Prerequisite:** The Pydantic tutorial must be complete. Your `schemas.py` file must exist — you will import from it in the final exercise.

**Reference:** [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/en/20/)

## 0. Setup

Continue in your `task-api` folder with the same venv active:

```bash
pip install sqlalchemy
```

SQLite is built into Python so no database server is needed for these exercises. You will use the same ORM code with PostgreSQL in a real project — virtually nothing changes.

Verify:

```bash
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

The version should be 2.x. If it is 1.x, upgrade: `pip install --upgrade sqlalchemy`.

## 1. Engine and Session

The **engine** manages the connection pool to the database. The **session** is the unit of work — you use it to run queries and commit changes. Think of the session like a shopping basket: you stage changes inside it, then commit them all at once.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///tasks.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
```

`echo=True` prints every SQL statement SQLAlchemy generates — leave it on while learning.

### 1.1

Create `database.py` in your `task-api` folder with the engine and session factory:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
```

Run it:

```bash
python database.py
```

No visible output yet, but the engine is ready. Add `print("Engine created")` at the bottom to confirm.

### 1.2

A session is how you interact with the database. Use it as a context manager so it is always closed, even if an exception occurs:

```python
with SessionLocal() as session:
    print("Session open")
# session is automatically closed here
```

Add this block to `database.py` and run it. With `echo=True` you will see SQLAlchemy open and close the connection.

### 1.3

Replace `get_session` with a proper FastAPI dependency. A **dependency** is a function FastAPI calls for you before each request — and cleans up after. The key is `yield`: code before it runs before the request, code in `finally` runs after the response, even if an exception occurred.

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    pass  # will create tables once models are defined
```

In a route handler, `Depends(get_db)` tells FastAPI to call `get_db()` and pass the session in:

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

FastAPI handles calling `get_db()`, injecting `db`, and closing the session — you never call `get_db()` yourself.

Add `get_db` and `init_db` to `database.py`. You do not need to call `get_db()` directly yet — that comes in the final exercise.

## 2. Defining ORM Models

An ORM model is a Python class that maps to a database table. In SQLAlchemy you define columns with `Column()` — the first argument is the SQLAlchemy type, and keyword arguments control options like `primary_key`, `unique`, and `nullable`.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
```

- `Column(Integer)` — an integer column
- `Column(String(100))` — a varchar column with max length 100
- `nullable=False` — the column cannot be NULL (defaults to `True` if omitted)
- `primary_key=True` — marks the column as the primary key; SQLite auto-increments it

### 2.1

Create `models.py` in `task-api`. Define the `Base` class and a `User` model:

- `id`: integer primary key (`Column(Integer, primary_key=True)`)
- `name`: string, max 100 chars, not nullable
- `email`: string, max 255 chars, unique, not nullable

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r})"
```

Run `python models.py` — no errors means the class definition is valid.

### 2.2

Add a `Task` model to `models.py`:

- `id`: integer primary key
- `title`: string, max 200 chars, not nullable
- `description`: string, nullable — use `nullable=True`
- `priority`: string, max 20 chars, not nullable, default `"medium"`
- `status`: string, max 20 chars, not nullable, default `"todo"`
- `owner_id`: integer, not nullable (foreign key comes in section 5)

```python
from sqlalchemy import Column, Integer, String, Text

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), nullable=False, default="medium")
    status = Column(String(20), nullable=False, default="todo")
    owner_id = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
```

### 2.3 — Challenge

Add a `created_at` column to `Task`. Use `server_default` so the database sets the timestamp automatically rather than Python:

```python
from sqlalchemy import Column, DateTime, func

class Task(Base):
    ...
    created_at = Column(DateTime, server_default=func.now())
```

Look up the difference between `default` (Python sets the value before INSERT) and `server_default` (the database sets it during INSERT). Write a comment explaining when you would use each.

## 3. Creating Tables

`Base.metadata.create_all(engine)` inspects all classes that inherit from `Base` and creates their tables if they do not already exist. It is idempotent — safe to call multiple times.

### 3.1

Update `database.py` to import `Base` from `models` and fill in `init_db`:

```python
from models import Base

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Tables created.")
```

Run it:

```bash
python database.py
```

With `echo=True` you will see `CREATE TABLE` SQL. A file called `tasks.db` appears in your folder. Confirm the tables exist:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
print(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())
"
```

### 3.2

During development you will often change your models and need to reset the database. Add a `reset_db` function that drops and recreates all tables:

```python
def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
```

Run it and read the `echo=True` output — you will see `DROP TABLE` followed by `CREATE TABLE`.

> In production, never drop tables — use database migrations (Alembic) instead. `reset_db` is development-only.

### 3.3

Wire `init_db()` into FastAPI so tables are created automatically when the server starts. Open `main.py` and add a startup event:

```python
from fastapi import FastAPI
from database import init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()
```

`@app.on_event("startup")` runs the decorated function once when Uvicorn starts the server — before any request is handled. This means the tables will always exist by the time a route runs, even on a fresh machine with no `tasks.db` file.

Start the server:

```bash
uvicorn main:app --reload
```

With `echo=True` still set in `database.py` you will see the `CREATE TABLE IF NOT EXISTS` statements in the terminal on startup. Delete `tasks.db` and restart — the tables are recreated automatically.

> `@app.on_event("startup")` is the current stable API. FastAPI also supports `lifespan` context managers as a more modern alternative — you will see both in real codebases, but `on_event` is simpler to read at this stage.

## 4. Basic CRUD

All database operations go through a session.

### 4.1

**Create** — instantiate a model, add it to the session, and commit:

```python
from database import SessionLocal
from models import User

with SessionLocal() as session:
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)  # reload from DB to get the auto-generated id
    print(user.id)         # 1
```

`session.refresh()` updates the in-memory object with values the database set (like the auto-increment id). Without it, `user.id` might still be `None`.

Create a script `seed.py` that creates two users and prints their ids after committing.

### 4.2

**Read** — use `select()` to query:

```python
from sqlalchemy import select
from models import User

with SessionLocal() as session:
    # Get all users
    users = session.execute(select(User)).scalars().all()
    for u in users:
        print(u.name, u.email)

    # Get one by primary key
    user = session.get(User, 1)
    print(user.name)
```

- `.scalars().all()` — returns a list of model instances
- `session.get(Model, pk)` — fastest way to fetch by primary key; returns `None` if not found

Add queries to `seed.py` to read back the users you created.

### 4.3

**Filter** — add `.where()` clauses to narrow results:

```python
from sqlalchemy import select
from models import User

with SessionLocal() as session:
    stmt = select(User).where(User.email == "alice@example.com")
    user = session.execute(stmt).scalar_one_or_none()
    if user:
        print(f"Found: {user.name}")
    else:
        print("Not found")
```

- `.scalar_one()` — expects exactly one result; raises if zero or multiple
- `.scalar_one_or_none()` — returns `None` if no result; raises if multiple
- `.scalars().all()` — returns a list (possibly empty)

Write a query that fetches all users whose name contains the letter `"a"` (use `User.name.ilike("%a%")`).

### 4.4

**Update** — load the object, modify it, and commit. SQLAlchemy detects what changed:

```python
with SessionLocal() as session:
    user = session.get(User, 1)
    if user:
        user.name = "Alice Smith"
        session.commit()
```

Update the name of one user. Read it back in a new `with` block to confirm the change persisted.

### 4.5

**Delete** — load the object and call `session.delete()`:

```python
with SessionLocal() as session:
    user = session.get(User, 1)
    if user:
        session.delete(user)
        session.commit()
```

Delete one user. Confirm the row is gone by reading all users in a new session.

### 4.6 — Challenge

Write a function `get_or_create(session, model_class, **kwargs)` that:
- Looks for an existing record where all `kwargs` match
- Returns it if found
- Creates, commits, and returns a new one if not found

Call it twice with the same email address. Confirm only one user is created.

## 5. Relationships

Tables are related through foreign keys. SQLAlchemy models this with `ForeignKey` on the column and `relationship()` on the model, giving you Python-level navigation between related objects.

```python
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"
    ...
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = "users"
    ...
    tasks = relationship("Task", back_populates="owner")
```

`back_populates` links both sides of the relationship — changing one side updates the other in the same session.

### 5.1

Update `models.py` to add the foreign key and relationship:

- `Task.owner_id` → `Column(Integer, ForeignKey("users.id"), nullable=False)`
- `Task.owner` → relationship to `User`
- `User.tasks` → relationship to `list[Task]`

Call `reset_db()` to apply the schema change. Then re-run `seed.py` to repopulate.

### 5.2

Create a user and several tasks owned by that user. Navigate the relationship in both directions:

```python
with SessionLocal() as session:
    user = session.get(User, 1)
    print(user.tasks)         # list of Task objects

    task = session.get(Task, 1)
    print(task.owner.name)    # User name via relationship
```

### 5.3

Add tasks to a user by appending to the relationship list — SQLAlchemy handles the foreign key automatically:

```python
with SessionLocal() as session:
    user = session.get(User, 1)
    new_task = Task(title="Write tests", priority="high")
    user.tasks.append(new_task)
    session.commit()
```

Notice you did not set `owner_id` manually. Confirm it was set correctly by reading the task back.

### 5.4 — Challenge

By default SQLAlchemy lazily loads relationships — it runs a separate query the first time you access `user.tasks`. Querying 10 users and accessing their tasks triggers 11 queries total. This is the **N+1 problem**.

Fix it with eager loading using `joinedload`:

```python
from sqlalchemy.orm import joinedload

stmt = select(User).options(joinedload(User.tasks))
users = session.execute(stmt).unique().scalars().all()
```

Run both versions with `echo=True` and count the number of SQL queries each produces.

## 6. Putting It Together

### Final Exercise

Create `crud.py` in `task-api`. This module provides the database functions that the FastAPI tutorial will call directly — do not rename or move it.

Import `UserCreate`, `TaskCreate`, and `TaskUpdate` from `schemas.py`.

**User functions:**

```python
from sqlalchemy.orm import Session
from schemas import UserCreate, TaskCreate, TaskUpdate
from models import User, Task

def create_user(session: Session, user: UserCreate) -> User:
    ...

def get_user(session: Session, user_id: int) -> User | None:
    ...

def get_user_by_email(session: Session, email: str) -> User | None:
    ...

def list_users(session: Session) -> list[User]:
    ...
```

**Task functions:**

```python
def create_task(session: Session, task: TaskCreate) -> Task:
    ...

def get_task(session: Session, task_id: int) -> Task | None:
    ...

def list_tasks(session: Session, status: str | None = None) -> list[Task]:
    ...

def update_task(session: Session, task_id: int, updates: TaskUpdate) -> Task | None:
    ...

def delete_task(session: Session, task_id: int) -> bool:
    ...
```

Requirements:
- `create_task` must verify `owner_id` refers to a real user — raise `ValueError` if not
- `list_tasks` must filter by `status` when provided
- `update_task` must apply only non-`None` fields from `TaskUpdate` — use `model_dump(exclude_none=True)` and `setattr` in a loop
- `delete_task` returns `True` if deleted, `False` if the task was not found

Write `test_crud.py` that calls every function and prints the results. Run it against a fresh database until all functions work.

Once `crud.py` works, wire it into `main.py` using `Depends(get_db)`. Replace the in-memory store endpoints with real database calls:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
import crud
from schemas import UserCreate, UserResponse, TaskCreate, TaskResponse, TaskUpdate

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_tasks(db, status=status)

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db, task)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

Notice that each route receives `db: Session = Depends(get_db)` and passes it straight to `crud` — the route itself does no database work. This keeps the database logic in one place and makes the routes easy to test independently.

## Checklist

- [ ] Can create a SQLAlchemy engine and session factory
- [ ] Can define an ORM model with `Column` and SQLAlchemy types
- [ ] Understand `nullable=False` vs `nullable=True` on columns
- [ ] Can create tables with `Base.metadata.create_all()`
- [ ] Can create, read, update, and delete records through a session
- [ ] Know when to use `session.get()` vs `select().where()`
- [ ] Know the difference between `.scalar_one()`, `.scalar_one_or_none()`, and `.scalars().all()`
- [ ] Can define a foreign key and two-way relationship with `back_populates`
- [ ] Understand lazy loading and the N+1 problem; can fix it with `joinedload`
- [ ] `crud.py` is complete and all functions pass `test_crud.py`
- [ ] Can write a `get_db()` dependency and inject it into routes with `Depends(get_db)`
- [ ] Understand why `yield` + `finally` guarantees session cleanup
