# Alembic Exercises

Alembic is the migration tool for SQLAlchemy. When your database schema changes — a new column, a renamed table, a dropped index — Alembic generates a versioned migration script that applies the change in a controlled, reproducible way. Unlike `create_all()`, migrations are reversible and safe to run in production.

Work through each section in order. Every exercise has something to run in your terminal.

**This is a continuation of the SQLAlchemy tutorial.** The SQLAlchemy tutorial used `Base.metadata.create_all()` and `reset_db()` to manage the schema during development. This tutorial replaces both of those with Alembic — the tool you will use in any real project.

**Track order:**
- **FastAPI tutorial:** Build a working in-memory API ✓
- **Pydantic tutorial:** Production-quality schemas ✓
- **SQLAlchemy tutorial:** Add a real database ✓
- **Alembic (this file):** Manage schema changes safely

**Prerequisite:** The SQLAlchemy tutorial must be complete. Your `task-api` folder must contain `models.py`, `database.py`, and `crud.py`.

**Reference:** [Alembic docs](https://alembic.sqlalchemy.org/en/latest/)

## 0. Setup

Continue in your `task-api` folder with the same venv active:

```bash
pip install alembic
```

Verify:

```bash
alembic --version
```

You should see `alembic 1.x.x`. Before continuing, delete `tasks.db` if it exists — Alembic will create the schema from scratch:

```bash
# Mac/Linux
rm -f tasks.db

# Windows
del tasks.db
```

This forces you to start clean. In a real project you would never delete the database — you would run the migrations against the existing schema instead.

## 1. Initialising Alembic

`alembic init` scaffolds the configuration and directory structure Alembic needs. You run it once per project.

```bash
alembic init migrations
```

This creates:

```
task-api/
├── alembic.ini          ← main configuration file
└── migrations/
    ├── env.py           ← how Alembic connects to your database and finds your models
    ├── script.py.mako   ← template used when generating new migration files
    └── versions/        ← one file per migration (starts empty)
```

### 1.1

Run `alembic init migrations` from your `task-api` folder. Open `alembic.ini` and find the `sqlalchemy.url` line:

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

Replace it with your SQLite URL:

```ini
sqlalchemy.url = sqlite:///tasks.db
```

### 1.2

Open `migrations/env.py`. Near the top you will see:

```python
target_metadata = None
```

Alembic needs your models' metadata so it can compare the current database schema against your Python models and generate migrations automatically. Replace `target_metadata = None` with an import and assignment:

```python
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import Base
from models import User, Task  # importing models registers them on Base.metadata

target_metadata = Base.metadata
```

The `sys.path.insert` line makes sure Python can find your modules even when Alembic runs from a different working directory.

Run `alembic current` to confirm the configuration is valid:

```bash
alembic current
```

No error means Alembic can connect to the database and read your metadata. You will see no output yet — there is no migration history.

### 1.3 — Challenge

Read through `migrations/env.py` and answer these questions in comments at the top of the file:

1. What does `run_migrations_offline()` do and when would it be used?
2. What is the difference between `run_migrations_online()` and `run_migrations_offline()`?
3. Where is the database URL read from in `run_migrations_online()`?

Look at how `connectable` is constructed — trace it back to `alembic.ini`. This is the configuration chain you will modify when you switch to PostgreSQL.

## 2. Your First Migration

Alembic's autogenerate feature compares your SQLAlchemy models against the current database schema and writes the migration for you. The result is a plain Python file with two functions: `upgrade()` applies the change, and `downgrade()` reverses it.

### 2.1

Generate the initial migration — this creates the `users` and `tasks` tables:

```bash
alembic revision --autogenerate -m "create users and tasks tables"
```

A file appears in `migrations/versions/` with a name like `a1b2c3d4e5f6_create_users_and_tasks_tables.py`. Open it.

The file contains:
- **`revision`** — a unique hex identifier for this migration
- **`down_revision`** — the revision this one builds on (`None` for the first migration)
- **`upgrade()`** — SQL to apply the change
- **`downgrade()`** — SQL to undo the change

Read through `upgrade()`. You will see `op.create_table()` calls for `users` and `tasks`. The column definitions should match your `models.py` exactly.

### 2.2

Run the migration:

```bash
alembic upgrade head
```

- `head` means "apply all pending migrations up to the latest one"

Confirm the tables exist:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
print(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())
"
```

You should see `users`, `tasks`, and `alembic_version`. The `alembic_version` table is how Alembic tracks which migrations have been applied.

### 2.3

Check the current state of the database:

```bash
alembic current
```

You will see the revision id followed by `(head)` — meaning the database is fully up to date.

Check the migration history:

```bash
alembic history
```

One entry. As you add more migrations this list grows into a full audit trail.

### 2.4 — Challenge

Look at the `alembic_version` table directly:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
print(conn.execute('SELECT * FROM alembic_version').fetchall())
"
```

The value stored is the revision id of the latest applied migration. Explain in a comment in your `env.py` why Alembic stores this in the database itself rather than in a local file.

## 3. Running Migrations

Every Alembic command revolves around moving the database between revision states. `upgrade` moves forward; `downgrade` moves backward.

### 3.1

Downgrade one step back to the empty state:

```bash
alembic downgrade -1
```

- `-1` means "go back one revision from the current state"

Confirm the tables are gone:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
print(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())
"
```

Only `alembic_version` remains — Alembic always keeps its own table. Run `alembic current` — it reports `<current revision> (base)` showing you are at the starting point with no schema applied.

### 3.2

Upgrade back to head:

```bash
alembic upgrade head
```

Confirm the tables are recreated. Check `alembic current` again — you should be back at `(head)`.

### 3.3

You can also target a specific revision by its id. Run `alembic history` to get the revision id, then upgrade or downgrade to it by id:

```bash
alembic upgrade <revision_id>
alembic downgrade <revision_id>
```

Try downgrading to the specific revision id shown in `alembic history`, then upgrade back to `head`.

### 3.4 — Challenge

Generate the SQL Alembic would run without actually running it. This is the `--sql` flag — useful for reviewing what will be executed before touching a production database:

```bash
alembic upgrade head --sql
```

The output is raw SQL. Redirect it to a file and read it:

```bash
# Mac/Linux
alembic upgrade head --sql > migration_preview.sql

# Windows
alembic upgrade head --sql | Out-File migration_preview.sql
```

In production you might pipe this to a DBA for review before running the real upgrade.

## 4. Modifying the Schema

This is where Alembic earns its place. Every schema change in production must go through a migration. The autogenerate command reads your models, compares them to the current database, and writes only the diff.

### 4.1

Add a `completed` boolean column to `Task` in `models.py`:

```python
from sqlalchemy import Column, Boolean

class Task(Base):
    __tablename__ = "tasks"
    ...
    completed = Column(Boolean, nullable=False, server_default="0")
```

`server_default="0"` means the database sets `completed = false` for all existing rows automatically when the column is added. This is important — adding a `NOT NULL` column without a default would fail on a table that already has rows.

Generate the migration:

```bash
alembic revision --autogenerate -m "add completed column to tasks"
```

Open the new file in `migrations/versions/`. Confirm `upgrade()` contains `op.add_column("tasks", sa.Column("completed", ...))` and `downgrade()` contains `op.drop_column("tasks", "completed")`.

Run it:

```bash
alembic upgrade head
```

### 4.2

Read the new column back:

```python
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
cursor = conn.execute('PRAGMA table_info(tasks)')
for row in cursor.fetchall():
    print(row)
"
```

The `completed` column should appear with a default value.

### 4.3

Rename a column using `op.alter_column()`. Add a `due_date` column first:

```python
from sqlalchemy import Column, Date

class Task(Base):
    __tablename__ = "tasks"
    ...
    due_date = Column(Date, nullable=True)
```

Generate and run the migration:

```bash
alembic revision --autogenerate -m "add due_date to tasks"
alembic upgrade head
```

SQLite has limited `ALTER TABLE` support — Alembic works around this by recreating the table. Watch the SQL output when you run with `echo=True` or use `--sql` to see how it handles this.

### 4.4 — Challenge

Add an `is_archived` boolean column to `User` with `server_default="0"`. Before generating the migration, write down what you expect the migration to contain. Then generate it and compare.

Now downgrade one step — what does `downgrade()` do to a column that already has data in it? Consider the risk of an irreversible downgrade and write a comment in the migration file explaining this.

## 5. Data Migrations

Schema migrations change the structure of the database. Data migrations change the content. Alembic handles both — in the same migration file if needed.

### 5.1

A data migration executes SQL inside `upgrade()` alongside `op` calls. Create a new migration that seeds default data — not using autogenerate, but written manually:

```bash
alembic revision -m "seed default task status values"
```

Notice there is no `--autogenerate` flag. This creates an empty migration template with blank `upgrade()` and `downgrade()` functions. Fill it in:

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

def upgrade() -> None:
    tasks_table = table(
        "tasks",
        column("id", sa.Integer),
        column("status", sa.String),
    )
    op.execute(
        tasks_table.update()
        .where(tasks_table.c.status == None)
        .values(status="todo")
    )

def downgrade() -> None:
    pass  # data migrations are rarely reversible
```

Run it:

```bash
alembic upgrade head
```

### 5.2

A common pattern is a three-step migration for adding a `NOT NULL` column to a table that already has rows:

1. Add the column as `nullable=True` (no risk to existing rows)
2. Backfill existing rows with a sensible value
3. Alter the column to `nullable=False`

All three steps can go in one migration file. Create a migration manually that adds a `notes` column to `User`:

```python
def upgrade() -> None:
    # Step 1: add nullable column
    op.add_column("users", sa.Column("notes", sa.Text, nullable=True))

    # Step 2: backfill existing rows
    op.execute("UPDATE users SET notes = '' WHERE notes IS NULL")

    # Step 3: tighten to NOT NULL
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("notes", nullable=False)

def downgrade() -> None:
    op.drop_column("users", "notes")
```

Run it with `alembic upgrade head`. Then update `models.py` to match:

```python
class User(Base):
    __tablename__ = "users"
    ...
    notes = Column(Text, nullable=False, default="")
```

Run `alembic revision --autogenerate -m "sync notes column"` and confirm the generated file is empty — autogenerate sees no diff because the model and the database now match.

### 5.3 — Challenge

Write a data migration that normalises the `status` column on `tasks` — converting any value that is not one of `"todo"`, `"in-progress"`, or `"done"` to `"todo"`. Run it and then query the table to verify.

Write a `downgrade()` that is a no-op and add a comment explaining why rolling back a data normalisation is not generally safe.

## 6. Putting It Together

### Final Exercise

You have been asked to add a new feature to the task API: **task priorities must be stored as integers** (1 = low, 2 = medium, 3 = high) instead of strings, for easier sorting.

This is a breaking change — the column type changes and all existing data must be converted.

Complete the following steps in order:

**Step 1 — Write the migration.**

Create a new manual migration (no `--autogenerate`):

```bash
alembic revision -m "convert priority to integer"
```

In `upgrade()`:
1. Add a new `priority_int` column to `tasks` as `Integer, nullable=True`
2. Backfill: `"low"` → `1`, `"medium"` → `2`, `"high"` → `3`
3. Drop the old `priority` column
4. Use `batch_alter_table` to rename `priority_int` to `priority`

In `downgrade()`:
1. Add `priority` back as `String(20), nullable=True`
2. Backfill: `1` → `"low"`, `2` → `"medium"`, `3` → `"high"`
3. Drop the integer column

**Step 2 — Run the migration forward.**

```bash
alembic upgrade head
```

Confirm the `priority` column is now integer type:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('tasks.db')
cursor = conn.execute('PRAGMA table_info(tasks)')
for row in cursor.fetchall():
    print(row)
"
```

**Step 3 — Update the model.**

In `models.py`, change `priority` from `Column(String(20), ...)` to `Column(Integer, ...)`. Run autogenerate to confirm the model and database now agree:

```bash
alembic revision --autogenerate -m "verify priority int sync"
```

Open the generated file. If `upgrade()` is empty, the model and schema are in sync. Delete the empty migration file and remove it from the versions history.

**Step 4 — Update the schemas and routes.**

Update `schemas.py` to use `int` instead of `Literal["low", "medium", "high"]` for the `priority` field. Update the FastAPI routes and CRUD functions to reflect the new type. Start the server and verify everything works via the Swagger UI.

**Step 5 — Rollback test.**

```bash
alembic downgrade -1
```

Confirm the original string `priority` column is restored. Upgrade back to head:

```bash
alembic upgrade head
```

Completing both directions confirms your migration is safe for production.

## Checklist

- [ ] Can initialise Alembic with `alembic init` and configure `env.py` to point at your models
- [ ] Understand what `target_metadata` does and why model imports are required
- [ ] Can generate an initial migration with `alembic revision --autogenerate`
- [ ] Understand the structure of a migration file: `revision`, `down_revision`, `upgrade()`, `downgrade()`
- [ ] Can apply migrations with `alembic upgrade head` and roll back with `alembic downgrade -1`
- [ ] Can target a specific revision by id
- [ ] Can preview SQL without running it using `--sql`
- [ ] Know why `server_default` is required when adding a `NOT NULL` column to an existing table
- [ ] Can write a manual (non-autogenerate) migration for data changes
- [ ] Know the three-step pattern for safely adding a `NOT NULL` column with backfill
- [ ] Can write `downgrade()` and understand when it is and is not reversible
- [ ] Completed the final exercise: type-change migration applied and rolled back successfully
