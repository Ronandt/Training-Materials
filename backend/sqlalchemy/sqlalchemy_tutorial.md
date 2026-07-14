# SQLAlchemy Reference

SQLAlchemy is Python's most widely used database toolkit. It has two layers: Core (raw SQL expression language) and ORM (maps Python classes to database tables). This covers the ORM — what you'll use with FastAPI.

**This is a continuation of the FastAPI tutorial.** The FastAPI tutorial stored data in an in-memory Python list. This replaces that with a real database — everything else in the API stays the same.

**Prerequisite:** The Pydantic tutorial must be complete. Your `schemas.py` must exist, exporting exactly `User` and `Task` — you will import from it in the final project.

**A naming note before you start:** `schemas.py` exports `User` and `Task` (Pydantic). This tutorial's ORM classes model the same two entities — so if they were also named `User` and `Task`, importing both into the same file (as `crud.py` will) would collide. This tutorial names the ORM classes `UserModel` and `TaskModel` instead.

## Video

[FastAPI for Beginners — Python Web Framework](https://www.youtube.com/watch?v=Lu8lXXlstvM) (Telusko) — this single course covers Pydantic, FastAPI, and SQLAlchemy.

## Resources

- [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/en/20/)

## Setup

```bash
pip install sqlalchemy
```

SQLite is built into Python, so no database server is needed here — the same ORM code works against PostgreSQL in a real project with virtually no changes.

## Reference

**Engine and session.** The engine manages the connection pool; the session is the unit of work — stage changes, then commit them all at once, like a shopping basket:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///tasks.db", echo=True)  # echo=True prints every SQL statement
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    ...
# session is automatically closed here
```

For FastAPI, wrap the session in a **dependency** — a function FastAPI calls before each request and cleans up after via `yield`/`finally`:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()
```

**ORM models.** A class that inherits from a declarative `Base`, mapping to a table via `Column()`:

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    tasks = relationship("TaskModel", back_populates="owner")

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), nullable=False, default="medium")
    status = Column(String(20), nullable=False, default="todo")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("UserModel", back_populates="tasks")
```

`nullable=False` means the column can't be NULL (defaults to `True` if omitted). `ForeignKey` + `relationship(..., back_populates=...)` links both sides — the string passed to `relationship()` is the *ORM class name*, not the table name, and changing one side updates the other in the same session.

**Creating tables.** `Base.metadata.create_all(engine)` inspects every `Base` subclass and creates its table if missing — idempotent, safe to call repeatedly. `drop_all` + `create_all` resets everything (development only — never in production; use Alembic migrations there instead):

```python
def init_db():
    Base.metadata.create_all(engine)

def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
```

Wire `init_db()` into FastAPI's startup so tables always exist before a route runs:

```python
@app.on_event("startup")
def startup():
    init_db()
```

**CRUD.** Create by instantiating, adding, committing, then `refresh()` to pull back DB-assigned values like the id:

```python
with SessionLocal() as session:
    user = UserModel(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    print(user.id)
```

Read with `select()`; `.scalars().all()` for a list, `session.get(Model, pk)` for a fast primary-key lookup, `.where()` to filter:

```python
from sqlalchemy import select

session.execute(select(UserModel)).scalars().all()
session.get(UserModel, 1)
session.execute(select(UserModel).where(UserModel.email == "alice@example.com")).scalar_one_or_none()
```

`.scalar_one()` expects exactly one result (raises otherwise); `.scalar_one_or_none()` allows zero. Update by mutating a loaded object and committing; delete with `session.delete(obj)` + commit — SQLAlchemy tracks what changed automatically.

**Relationships.** Once `relationship()` is defined, navigate in Python without writing joins, and append to the collection side to set the foreign key automatically:

```python
user = session.get(UserModel, 1)
print(user.tasks)          # list of TaskModel

user.tasks.append(TaskModel(title="Write tests", priority="high"))
session.commit()  # owner_id set automatically — no manual assignment needed
```

Relationships lazy-load by default — accessing `user.tasks` fires a separate query the first time. Querying 10 users and reading each one's `.tasks` is 11 queries (the **N+1 problem**). Fix it with eager loading:

```python
from sqlalchemy.orm import joinedload

stmt = select(UserModel).options(joinedload(UserModel.tasks))
users = session.execute(stmt).unique().scalars().all()
```

## Final Project

Create `crud.py` in `task-api`. Import `User`/`Task` from `schemas.py` (what routes receive and return) and `UserModel`/`TaskModel` from `models.py` (what actually talks to the database):

```python
from sqlalchemy.orm import Session
from schemas import User, Task
from models import UserModel, TaskModel

def create_user(session: Session, user: User) -> UserModel:
    db_user = UserModel(**user.model_dump(exclude={"id"}))  # id is DB-assigned, never client-supplied
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session: Session, user_id: int) -> UserModel | None: ...
def get_user_by_email(session: Session, email: str) -> UserModel | None: ...
def list_users(session: Session) -> list[UserModel]: ...

def create_task(session: Session, task: Task) -> TaskModel: ...
def get_task(session: Session, task_id: int) -> TaskModel | None: ...
def list_tasks(session: Session, status: str | None = None) -> list[TaskModel]: ...

def update_task(session: Session, task_id: int, updates: dict) -> TaskModel | None:
    task = session.get(TaskModel, task_id)
    if task is None:
        return None
    for field, value in updates.items():
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: int) -> bool: ...
```

Requirements:
- `create_task` must verify `owner_id` refers to a real user — raise `ValueError` if not
- `list_tasks` must filter by `status` when provided
- `update_task` takes a plain `dict` (matching the FastAPI PATCH endpoint, which has no dedicated update schema) and applies each field with `setattr` in a loop
- `delete_task` returns `True` if deleted, `False` if the task was not found

Write `test_crud.py` that calls every function and prints the results, run against a fresh database until all functions work.

Then wire `crud.py` into `main.py` using `Depends(get_db)`, replacing the in-memory store endpoints with real database calls:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
import crud
from schemas import User, Task

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/users", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@app.post("/users", response_model=User, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db, user)

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db, task)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updates: dict, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

Each route receives `db: Session = Depends(get_db)` and passes it straight to `crud` — the route itself does no database work. `response_model=User`/`Task` validates the returned ORM object against the Pydantic schema automatically; Pydantic reads attributes off any object, not just dicts, so no extra conversion code is needed.
