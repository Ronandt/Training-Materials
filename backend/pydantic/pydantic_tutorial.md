# Pydantic Exercises

Pydantic is a data validation library. You define data shapes as Python classes — Pydantic validates incoming data against those shapes, converts types where possible, and raises clear errors when data doesn't fit. FastAPI uses Pydantic for all request and response validation, so learning it here pays off immediately in the next tutorial.

Work through each section in order. Every exercise has something to run in your terminal.

**This is a continuation of the FastAPI tutorial.** The FastAPI tutorial used simple inline Pydantic models. This tutorial goes deeper — validators, nested models, serialization patterns, and the full schema design you will carry into the SQLAlchemy tutorial.

**Track order:**
- **FastAPI tutorial:** Build a working in-memory API ✓
- **Pydantic (this file):** Deepen your Pydantic knowledge and build production-quality schemas
- **SQLAlchemy (continuation):** Replace the in-memory store with a real database

**Reference:** [Pydantic docs](https://docs.pydantic.dev/latest/)

## 0. Setup

Create a folder for the project you will build across all three tutorials:

```bash
mkdir task-api
cd task-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate.bat
```

Install Pydantic:

```bash
pip install pydantic
```

Verify the version (these exercises use v2):

```bash
python -c "import pydantic; print(pydantic.__version__)"
```

If the version starts with `1`, upgrade: `pip install --upgrade pydantic`.

Create a file called `schemas.py` inside `task-api`. You will build this file up across the whole tutorial — it will be imported directly by the SQLAlchemy and FastAPI tutorials.

## 1. Basic Models

A Pydantic model is a class that inherits from `BaseModel`. Each field is a class attribute with a type annotation. When you instantiate the model, Pydantic validates the data automatically.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

user = User(id=1, name="Alice", email="alice@example.com")
print(user.id)    # 1
print(user.name)  # Alice
```

### 1.1

In `schemas.py`, define a `User` model with `id: int`, `name: str`, and `email: str`. Create an instance and print each field. Run the file:

```bash
python schemas.py
```

### 1.2

Pydantic coerces compatible types automatically:

```python
user = User(id="42", name="Alice", email="alice@example.com")
print(user.id)        # 42  (int, not "42")
print(type(user.id))  # <class 'int'>
```

Try creating a `User` where `id` is the string `"42"`. Confirm Pydantic converts it to an integer. Then try passing a string that cannot be converted, like `"abc"`. Read the `ValidationError`.

### 1.3

When validation fails, Pydantic raises a `ValidationError` with information about every field that failed:

```python
from pydantic import ValidationError

try:
    user = User(id="not-a-number", name="Alice", email="alice@example.com")
except ValidationError as e:
    print(e)
```

Run this. The output shows the field name, the value that failed, and why. Deliberately trigger two validation errors at once by passing bad values for two different fields.

### 1.4

Define a `Task` model in `schemas.py` with these fields:

- `id: int`
- `title: str`
- `priority: str`
- `status: str`
- `owner_id: int`

Create two `Task` instances with different values and print them. You will extend this model throughout the tutorial.

## 2. Field Constraints

`Field()` lets you add constraints to individual fields.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)           # greater than 0
    quantity: int = Field(ge=0, le=999)  # 0 <= quantity <= 999
```

Constraints: `gt` (greater than), `ge` (≥), `lt` (less than), `le` (≤), `min_length`, `max_length`, `pattern` (regex).

### 2.1

Update `Task` in `schemas.py` to add constraints:

- `title`: minimum 1 character, maximum 200 characters
- `priority`: must be one of `"low"`, `"medium"`, `"high"` — use `Literal` from `typing`
- `status`: must be one of `"todo"`, `"in-progress"`, `"done"` — also `Literal`

```python
from typing import Literal

class Task(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    priority: Literal["low", "medium", "high"]
    status: Literal["todo", "in-progress", "done"]
    owner_id: int
```

Try creating a `Task` with `priority="urgent"`. Read the validation error.

### 2.2

Update `User` to validate the email address properly. Install the optional email validator first:

```bash
pip install "pydantic[email]"
```

Then use `EmailStr`:

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
```

Try passing `"not-an-email"` and read the error.

### 2.3 — Challenge

Define a `Comment` model (practice only — not part of the project). A comment has:

- `body`: string, 1–1000 characters
- `rating`: integer, 1–5 inclusive
- `author_email`: valid email
- `url`: optional URL — look up `AnyHttpUrl` from Pydantic

Write code that creates a valid comment, then another that triggers at least three different field errors in a single attempt.

## 3. Optional Fields and Defaults

Not every field is required. Optional fields use `| None` with a default of `None`. Regular defaults are assigned with `=`.

```python
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None  # optional, defaults to None
    priority: str = "medium"        # has a default but is still typed
```

### 3.1

Add `description: str | None = None` to `Task`. Create one task with a description and one without. Confirm the field exists and is `None` in the second case.

### 3.2

`default_factory` is for mutable or dynamic defaults — a callable that is called each time a new instance is created. Use it for lists and timestamps:

```python
from datetime import datetime
from pydantic import Field

class Task(BaseModel):
    ...
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)
```

Add `created_at` and `tags` to `Task` with `default_factory`. Create two tasks without supplying these fields — confirm each gets its own independent `created_at`.

### 3.3

In real APIs you need separate models for creating vs reading data:

- **Create model**: no `id` (the database assigns it), no `created_at`
- **Response model**: includes `id`, `created_at`, and everything else

Add `TaskCreate` to `schemas.py` — same fields as `Task` but without `id` and `created_at`. Then rename `Task` to `TaskResponse`. You will use `TaskCreate` for POST request bodies and `TaskResponse` for what the API returns.

Update any test code that used the old name.

### 3.4 — Challenge

Add `UserCreate` (no `id`) and `UserResponse` (with `id`) to `schemas.py`. Then write a function `make_user_response(create: UserCreate, generated_id: int) -> UserResponse` that constructs a `UserResponse` from a `UserCreate` plus a generated id. Use `model_dump()` to help convert between them:

```python
def make_user_response(create: UserCreate, generated_id: int) -> UserResponse:
    data = create.model_dump()
    data["id"] = generated_id
    return UserResponse(**data)
```

Call it and print the result.

## 4. Nested Models

A Pydantic model can contain another model as a field. Validation is recursive — all nested models are validated too.

```python
class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address

# Pydantic accepts a dict or an Address instance
person = Person(name="Alice", address={"street": "123 Main St", "city": "London"})
print(person.address.city)  # London
```

### 4.1

Add `owner: UserResponse` to `TaskResponse`. Update your test code to embed a full `UserResponse` inside a `TaskResponse`. Access `task.owner.name` and print it.

### 4.2

Models can contain lists of other models:

```python
class ProjectResponse(BaseModel):
    id: int
    name: str
    tasks: list[TaskResponse]
```

Define `ProjectResponse` and create an instance with three tasks. Print the title of each task using a loop.

### 4.3 — Challenge

Validation errors in nested models report the full path to the failing field:

```python
try:
    ProjectResponse(id=1, name="x", tasks=[{"id": 1, "title": "", ...}])
except ValidationError as e:
    print(e)
# error location will show: tasks -> 0 -> title
```

Deliberately trigger validation errors at two levels of nesting — one on the project itself and one inside a task in its list. Read the output and understand the location format.

## 5. Validators and Serialization

### 5.1

`@field_validator` runs custom validation logic on a field after the standard type check. Return the (possibly transformed) value, or raise `ValueError`:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        if v != v.lower():
            raise ValueError("email must be lowercase")
        return v
```

Add a validator to `UserCreate` that strips whitespace from `name`. Confirm that `name="  Alice  "` is stored as `"Alice"`.

### 5.2

`model_dump()` serializes a model to a plain Python dict. `model_dump_json()` serializes to a JSON string:

```python
task = TaskResponse(...)
print(task.model_dump())
print(task.model_dump_json())

# Exclude specific fields
print(task.model_dump(exclude={"id", "created_at"}))
```

Create a `TaskResponse` and print its dict and JSON forms. Then print it again excluding `id` and `created_at`.

### 5.3

`model_validate()` reconstructs a model from a dict. This is how you rebuild a model from a database row or an incoming API payload:

```python
data = task.model_dump()
data["title"] = "Updated title"
updated = TaskResponse.model_validate(data)
print(updated.title)
```

Take the dict from `model_dump()`, change a field, and reconstruct a new `TaskResponse` using `model_validate()`. Confirm the change took effect.

### 5.4 — Challenge

`model_config` controls model-wide behaviour:

```python
from pydantic import ConfigDict

class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ...
```

Add `str_strip_whitespace=True` to `TaskCreate`. Confirm that a title with surrounding spaces is automatically trimmed without a manual validator.

Then try adding `frozen=True` to any model and attempt to reassign a field — read the error. Frozen models behave like immutable dataclasses.

## 6. Putting It Together

Finalize `schemas.py`. This file will be imported directly by the SQLAlchemy and FastAPI tutorials — do not rename or move it.

### Final Exercise

Your `schemas.py` must export these five models, all fully constrained:

**User models**

- `UserCreate`: `name` (1–100 chars, whitespace stripped), `email` (valid email) — no `id`
- `UserResponse`: all `UserCreate` fields plus `id: int`

**Task models**

- `TaskCreate`: `title` (1–200 chars), `description` (optional `str | None`), `priority` (low/medium/high, default `"medium"`), `owner_id: int` — no `id`, `status`, or `created_at`
- `TaskUpdate`: every field optional (`str | None = None` for all) — used for PATCH requests where the caller sends only what they want to change
- `TaskResponse`: `id: int`, `title`, `description`, `priority`, `status` (default `"todo"`), `created_at: datetime`, `owner: UserResponse`

Requirements:
- `str_strip_whitespace = True` on all models via `model_config`
- A `@field_validator` on `UserCreate.name` that raises `ValueError` if the name is purely digits
- All five models must round-trip: `Model.model_validate(instance.model_dump())` must succeed

Test by instantiating one of each model and printing its JSON. Fix any errors until all five pass.

## Checklist

- [ ] Can define a `BaseModel` with typed fields and create instances
- [ ] Understand how Pydantic coerces types and when it raises `ValidationError`
- [ ] Can use `Field()` to add constraints (length, numeric bounds)
- [ ] Can use `Literal` to restrict a field to a fixed set of values
- [ ] Can use `EmailStr` and install Pydantic optional extras
- [ ] Know the difference between `str | None = None` and a required field
- [ ] Can use `default_factory` for mutable or dynamic defaults
- [ ] Can nest models and access nested fields
- [ ] Can write a `@field_validator` that transforms or rejects a value
- [ ] Can serialize with `model_dump()` and `model_dump_json()`
- [ ] Can deserialize from a dict with `model_validate()`
- [ ] `schemas.py` is complete with all five models and passes all round-trip tests
