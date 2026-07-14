# Pydantic Reference

Pydantic is a data validation library. You define data shapes as Python classes — Pydantic validates incoming data against those shapes, converts types where possible, and raises clear errors when data doesn't fit. FastAPI uses Pydantic for all request and response validation, so learning it here pays off immediately in the next tutorial.

**This is a continuation of the FastAPI tutorial.** This project keeps to exactly **two models: `User` and `Task`** — no separate Create/Response/Update variants. Each model has an `id: int | None = None` field: `None` when the client is creating something, filled in once the server assigns one. That one pattern does the job a Create/Response split would otherwise do, with half the classes to maintain.

**Track order:**
- **FastAPI tutorial:** Build a working in-memory API ✓
- **Pydantic (this file):** Deepen your Pydantic knowledge on the same two models
- **SQLAlchemy (continuation):** Replace the in-memory store with a real database

## Video

[FastAPI for Beginners — Python Web Framework](https://www.youtube.com/watch?v=Lu8lXXlstvM&t=4954s) (Telusko) — this single course covers Pydantic, FastAPI, and SQLAlchemy; the timestamp lands on the Pydantic section.

## Resources

- [Pydantic docs](https://docs.pydantic.dev/latest/)

## Reference

**Basic models.** A model is a class that inherits from `BaseModel`. Each field is a class attribute with a type annotation, validated automatically on instantiation:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    name: str
    email: str

user = User(name="Alice", email="alice@example.com")
print(user.id)  # None — nothing has assigned one yet
```

`id: int | None = None` is the pattern that replaces a Create/Response pair: the same class represents a user *being created* (no `id` yet) and one *already stored* (an `id` supplied by whatever created it).

Pydantic coerces compatible types automatically (`id="1"` becomes `1`), and raises `ValidationError` — listing every failed field, what value it got, and why — when a value can't be converted:

```python
from pydantic import ValidationError

try:
    User(id="not-a-number", name="Alice", email="alice@example.com")
except ValidationError as e:
    print(e)
```

**Field constraints.** `Field()` adds constraints to individual fields: `gt`/`ge`/`lt`/`le` for numbers, `min_length`/`max_length` for strings, `pattern` for regex. `Literal` restricts a field to a fixed set of values:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class Task(BaseModel):
    id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["todo", "in-progress", "done"] = "todo"
    owner_id: int

class User(BaseModel):
    id: int | None = None
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr  # needs: pip install "pydantic[email]"
```

**Optional fields and defaults.** `| None = None` marks a field optional; `= value` gives a plain default. `default_factory` is for mutable or dynamic defaults — a callable invoked fresh for each instance, used for lists and timestamps:

```python
from datetime import datetime

class Task(BaseModel):
    ...
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)
```

**`model_copy` — why one model is enough.** `model_copy(update=...)` returns a new instance with specific fields overridden, leaving the original untouched:

```python
draft = Task(title="Write tests", priority="high", owner_id=1)
print(draft.id)  # None — this is what a client POSTs

saved = draft.model_copy(update={"id": 7})
print(saved.id)   # 7 — this is what the server returns
print(draft.id)   # still None — model_copy doesn't mutate the original
```

A client sends a `Task` with no `id`; the server assigns one with `model_copy(update={"id": new_id})` and returns the same `Task` type back. This is what the FastAPI tutorial uses instead of separate `TaskCreate`/`TaskResponse` classes — and it's also how partial updates work, by merging only the changed fields.

**Validators.** `@field_validator` runs custom logic after the standard type check — return the (possibly transformed) value, or raise `ValueError`:

```python
from pydantic import field_validator

class User(BaseModel):
    ...
    @field_validator("name")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()
```

**Serialization.** `model_dump()` → plain dict, `model_dump_json()` → JSON string, `model_validate()` reconstructs a model from a dict (e.g. a database row or API payload):

```python
task = Task(id=1, title="Write tests", priority="high", status="todo", owner_id=1)
task.model_dump(exclude={"id", "created_at"})  # dict, minus some fields
task.model_dump_json()                          # JSON string

data = task.model_dump()
data["title"] = "Updated title"
Task.model_validate(data)  # rebuilt with the change applied
```

**`model_config`** controls model-wide behaviour — `str_strip_whitespace=True` trims every string field automatically; `frozen=True` makes a model immutable (which is exactly why `model_copy` — not direct assignment — is the normal way to change a field):

```python
from pydantic import ConfigDict

class Task(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ...
```

> Pydantic models can nest other models as fields (validation is recursive), but this project doesn't need that — `Task.owner_id` stays a plain int, and the FastAPI tutorial fetches the owner separately rather than embedding a full `User` inside every `Task`. Two flat models is the whole project.

## Final Project

Build `schemas.py` in your `task-api` folder. It will be imported directly by the SQLAlchemy and FastAPI tutorials — do not rename or move it, and do not add more models to it.

Your `schemas.py` must export exactly these two models:

- **`User`**: `id: int | None = None`, `name` (1–100 chars, whitespace stripped, via `str_strip_whitespace`), `email: EmailStr`, plus a `@field_validator` on `name` that raises `ValueError` if the name is purely digits
- **`Task`**: `id: int | None = None`, `title` (1–200 chars), `description: str | None = None`, `priority` (`Literal["low", "medium", "high"]`, default `"medium"`), `status` (`Literal["todo", "in-progress", "done"]`, default `"todo"`), `owner_id: int`, `created_at: datetime` (via `default_factory`)

Requirements:
- `str_strip_whitespace = True` on both models via `model_config`
- Both models must round-trip: `Model.model_validate(instance.model_dump())` must succeed
- Demonstrate the create-then-assign-id pattern: build a `Task` with no `id`, then produce a "saved" version with `model_copy(update={"id": ...})`

Test by instantiating one of each model and printing its JSON. Fix any errors until both pass.
