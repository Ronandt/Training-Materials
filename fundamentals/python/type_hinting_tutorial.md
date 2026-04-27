# Python Type Hinting Exercises

Python is dynamically typed - variables don't have declared types and the interpreter figures it out at runtime. Type hints are optional annotations you can add to tell the type checker (and other developers) what type a variable or function is expected to hold.

They don't change how your code runs. They're checked separately by a tool called `mypy`. The payoff is that mypy will catch bugs before you run your code - the same way TypeScript's compiler does.

Work through each section in order. Every exercise has something to run in your terminal.

**Reference:** [Python typing module docs](https://docs.python.org/3/library/typing.html) · [mypy documentation](https://mypy.readthedocs.io)

## 0. What problem are we solving?

Without type hints, this function has a hidden assumption:

```python
def greet(name):
    return "Hello, " + name
```

Call it with a number and Python crashes at runtime. With type hints:

```python
def greet(name: str) -> str:
    return "Hello, " + name
```

Now a type checker can tell you about the mistake before you ever run the code. In a large codebase, this is the difference between catching bugs immediately and debugging them in production.

## 1. Annotating Variables and Functions

### 1.1

Create a file called `hints.py`. Annotate some variables with their types:

```python
username: str = "alice"
age: int = 30
score: float = 9.5
is_active: bool = True
```

Run the file to confirm it works:

```bash
python hints.py
```

Type hints on variables are optional but useful for documenting intent. The interpreter ignores them entirely.

### 1.2

Write a function with annotated parameters and a return type:

```python
def add(a: int, b: int) -> int:
    return a + b
```

The syntax is `parameter: type` for inputs and `-> type` before the colon for the return value.

Add a call to the function and print the result. Run it.

### 1.3

The return type `None` is used for functions that don't return a value:

```python
def log_message(message: str) -> None:
    print(f"[LOG] {message}")
```

Write two more functions:
- One that takes a `float` and returns a `str`
- One that takes two `str` values and returns a `bool`

You decide what they do. Run the file.

### 1.4

Write a function that deliberately has the wrong return type annotation - the annotation says `str` but the function returns an `int`. Run it with Python. It will run fine. Python does not enforce annotations at runtime.

Keep this in mind: type hints are for your tools and your teammates, not for the interpreter.

## 2. Collection Types

### 2.1

For lists, dicts, tuples, and sets, you annotate the contents too.

```python
names: list[str] = ["alice", "bob"]
scores: dict[str, int] = {"alice": 95, "bob": 88}
point: tuple[int, int] = (10, 20)
tags: set[str] = {"python", "typing"}
```

> If you're on Python 3.8 or earlier, use `List`, `Dict`, `Tuple`, `Set` from `typing` instead. On 3.9+ the lowercase versions work directly.

Add these to `hints.py` and run it.

### 2.2

Annotate the parameters and return types of functions that work with collections:

```python
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def first_value(data: dict[str, int]) -> int:
    return next(iter(data.values()))
```

Call both functions and print the results.

### 2.3

A `tuple` with a fixed number of elements annotates each position separately:

```python
def min_max(numbers: list[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)
```

For a tuple of variable length where all elements are the same type, use `tuple[int, ...]` (with ellipsis).

Write a function that takes a list of strings and returns a `tuple[int, str]` containing the length of the longest string and the longest string itself.

## 3. Optional and Union Types

### 3.1

`None` is its own type in Python's type system. A variable that might be a string or `None` is typed as `str | None`:

```python
def find_user(user_id: int) -> str | None:
    users = {1: "alice", 2: "bob"}
    return users.get(user_id)
```

> On Python 3.9 and earlier, use `Optional[str]` from the `typing` module instead of `str | None`. They mean the same thing.

Write this function and call it with both a valid and an invalid user ID. Print the results.

### 3.2

`|` lets you express that a value can be one of several types:

```python
def process(value: int | str) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    return f"String: {value}"
```

This is the same `|` you used for union types in TypeScript. Call `process` with both an int and a string.

### 3.3

When a function parameter has a default of `None`, you almost always want `X | None` as its type:

```python
def greet(name: str, title: str | None = None) -> str:
    if title:
        return f"Hello, {title} {name}"
    return f"Hello, {name}"
```

Write a function with at least two parameters where one is optional (defaults to `None`). Annotate it correctly and call it both ways.

## 4. TypedDict and dataclasses

### 4.1

A plain `dict` is awkward to annotate when the keys and value types are known upfront. `TypedDict` gives a dict a fixed structure:

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int
    email: str

def print_user(user: User) -> None:
    print(f"{user['name']} ({user['age']}) - {user['email']}")

alice: User = {"name": "Alice", "age": 30, "email": "alice@example.com"}
print_user(alice)
```

Create this in a new file `structured.py` and run it.

### 4.2

`dataclass` is similar but gives you an actual class with attributes, not a dict. It also generates `__init__`, `__repr__`, and other methods automatically:

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True

item = Product(name="Keyboard", price=79.99)
print(item)
print(item.name)
```

Add this to `structured.py` and run it. Notice the `__repr__` - you get a readable print for free.

### 4.3

Add a method to your `Product` dataclass:

```python
def discounted_price(self, percent: float) -> float:
    return self.price * (1 - percent / 100)
```

Annotate the method parameters and return type. Call it and print the result.

### 4.4 - Challenge

Rewrite one of your functions from earlier sections that accepts a plain `dict` to accept a `TypedDict` instead. Then rewrite the same function to use a `dataclass`. Compare the two approaches - when would you choose one over the other? Write your conclusion as a comment.

## 5. Type Checking with mypy

### 5.1

Install mypy:

```bash
pip install mypy
```

Run it on your `hints.py` file:

```bash
mypy hints.py
```

If your annotations are consistent, you'll see `Success: no issues found`. If mypy finds a problem, it will tell you the line number and what's wrong.

### 5.2

Introduce a type error deliberately. In `hints.py`, add:

```python
def double(n: int) -> int:
    return n * 2

result: str = double(5)
```

Run mypy again. It will flag the assignment - `double` returns `int` but you annotated `result` as `str`.

Fix the annotation and confirm mypy is happy again.

### 5.3

mypy is stricter by default in some areas than others. Run it with `--strict` to enable all checks:

```bash
mypy --strict hints.py
```

You will likely see new errors about missing return types or unannotated function parameters. Fix each one until `--strict` passes.

### 5.4

Create a `mypy.ini` file to save your mypy configuration so you don't have to pass flags every time:

```ini
[mypy]
strict = true
```

Now just running `mypy hints.py` will apply strict mode automatically.

### 5.5 - Challenge

Run mypy on `structured.py` in strict mode. Fix any errors it finds. Then add a deliberate mistake - pass the wrong type to a `TypedDict` key or a `dataclass` field - and confirm mypy catches it before you run the code.

## 6. Putting It Together

### Final Exercise

Build a small typed contact book.

1. Create a new file `contacts.py`
2. Define a `Contact` dataclass with fields: `name: str`, `email: str`, `phone: str | None`
3. Write these functions, fully annotated:
   - `add_contact(book: list[Contact], contact: Contact) -> None`
   - `find_by_name(book: list[Contact], name: str) -> Contact | None`
   - `list_contacts(book: list[Contact]) -> None` - prints each contact
   - `count_with_phone(book: list[Contact]) -> int` - returns how many contacts have a phone number
4. Create a list of at least four contacts (some with phone numbers, some without)
5. Call all four functions and print results
6. Run mypy with `--strict` and fix every error until it passes

**The goal:** a fully annotated file that mypy approves in strict mode, with zero uses of `Any`.

## Checklist

- [ ] Can annotate variables and function parameters with basic types (`str`, `int`, `float`, `bool`)
- [ ] Can annotate functions that return `None`
- [ ] Can annotate `list`, `dict`, `tuple`, and `set` with their content types
- [ ] Understand why `str | None` is different from `str`, and when to use it
- [ ] Can write a `TypedDict` to give a fixed structure to a dict
- [ ] Can write a `dataclass` and understand what it generates automatically
- [ ] Can run mypy and read its output
- [ ] Can fix type errors mypy reports
- [ ] Can configure mypy with `mypy.ini`
- [ ] Completed the final exercise with mypy strict mode passing
