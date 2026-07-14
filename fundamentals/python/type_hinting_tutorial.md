# Python Type Hinting

Python is dynamically typed - variables don't have declared types and the interpreter figures it out at runtime. Type hints are optional annotations you can add to tell the type checker (and other developers) what type a variable or function is expected to hold. They don't change how your code runs - they're checked separately by a tool called `mypy`, the same way TypeScript's compiler checks `.ts` files.

## Video

[Python Typing - Type Hints & Annotations](https://www.youtube.com/watch?v=QORvB-_mbZ0)

Covers annotating variables and functions, typing collections (`list`, `dict`, `tuple`, `set`), `Optional`/`Union` types, and the basics of catching type errors with a type checker.

## Supplementary Notes

Quick reference for the syntax and gotchas that come up most often.

**Basic types**

```python
username: str = "alice"
age: int = 30

def add(a: int, b: int) -> int:
    return a + b

def log_message(message: str) -> None:  # None = no return value
    print(f"[LOG] {message}")
```

**Collections** - annotate the contents, not just the container:

```python
names: list[str] = ["alice", "bob"]
scores: dict[str, int] = {"alice": 95, "bob": 88}
point: tuple[int, int] = (10, 20)          # fixed length, each position typed
sizes: tuple[int, ...] = (1, 2, 3)         # variable length, all same type
tags: set[str] = {"python", "typing"}
```

> Python 3.8 and earlier: use `List`, `Dict`, `Tuple`, `Set` from `typing` instead of the lowercase built-ins.

**Optional and union types**

```python
def find_user(user_id: int) -> str | None:   # might return None
    ...

def process(value: int | str) -> str:        # one of several types
    ...
```

> Python 3.9 and earlier: use `Optional[str]` and `Union[int, str]` from `typing` instead of `|`. Same meaning.

If a parameter defaults to `None`, its type should almost always include `| None`:

```python
def greet(name: str, title: str | None = None) -> str: ...
```

**Structured data** - `TypedDict` for a dict with a known shape, `dataclass` for an actual class:

```python
from typing import TypedDict
from dataclasses import dataclass

class User(TypedDict):
    name: str
    age: int

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True   # dataclass gives you __init__ and __repr__ for free
```

Use `TypedDict` when you're stuck with dict-shaped data (e.g. parsed JSON). Use `dataclass` for anything you construct yourself - it's a real object with methods.

**Checking your annotations with mypy**

```bash
pip install mypy
mypy your_file.py          # normal mode
mypy --strict your_file.py # flags missing annotations and untyped code too
```

Type hints are never enforced at runtime - Python will happily run a function whose return type annotation is wrong. mypy is the tool that actually catches the mismatch, which is why it's worth running in CI, not just locally.

**Reference:** [Python typing module docs](https://docs.python.org/3/library/typing.html) · [mypy documentation](https://mypy.readthedocs.io)
