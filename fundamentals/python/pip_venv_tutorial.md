# pip and venv Exercises

Python ships with a package manager (pip) and a virtual environment tool (venv). You need both for any real project. This tutorial walks you through them hands-on.

**Video:** [How To Setup A Virtual Environment For Python In Visual Studio Code](https://www.youtube.com/watch?v=GZbeL5AcTgw) — watch this first if you'd rather see venv setup done visually before typing the commands yourself.

Work through each section in order. Every exercise has something to run in your terminal.

## 0. What problem are we solving?

When you install a package globally with `pip install requests`, it lands in your system Python. That's fine until two projects need different versions of the same library. Virtual environments fix this by giving each project its own isolated Python installation.

The rule is simple: one project, one venv, always activated before you work.

## 1. Creating and Activating a venv

### 1.1

Create a folder `pip-exercises`, `cd` into it, and create a venv:

```bash
python -m venv .venv
```

### 1.2

Activate it:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Your prompt should show `(.venv)`. **Verify:** run `which python` (Mac/Linux) or `where python` (Windows) — the path should point inside `.venv`, not your system Python.

### 1.3

Run `pip list` — you should see almost nothing, just `pip` itself. That's a clean slate for every project.

Now `deactivate` and run `pip list` again. Notice the difference, then reactivate before continuing.

## 2. Installing Packages

### 2.1

Install `requests`, confirm it shows up in `pip list`, then confirm it actually works:

```bash
pip install requests
```

```python
import requests
print(requests.__version__)
```

### 2.2

Install a specific version with `package==version`, and check the version again — pip will downgrade if needed:

```bash
pip install "requests==2.28.0"
```

### 2.3

Uninstall it:

```bash
pip uninstall requests
```

Confirm it with `pip list`, then reinstall the latest version for the next section.

## 3. Requirements Files

This is how you share dependencies with your team or deploy to a server.

### 3.1

Freeze your environment into a file — this is what gets committed to git:

```bash
pip freeze > requirements.txt
```

Open it. Every installed package is pinned to its exact version.

### 3.2

Simulate a fresh machine: create a new venv in a separate folder and install from the file.

```bash
mkdir fresh-install && cd fresh-install
python -m venv .venv
source .venv/bin/activate   # or the Windows equivalent
pip install -r ../requirements.txt
```

Run `pip list` — it should match your original environment exactly. Deactivate and go back to `pip-exercises`.

### 3.3

Most projects split production deps from dev-only deps (linters, test runners) into `requirements.txt` and `requirements-dev.txt`. Create `requirements-dev.txt` by hand with `pytest` in it, then install it:

```bash
pip install -r requirements-dev.txt
```

In production you'd install only `requirements.txt`; locally you install both.

## 4. pip show and pip check

### 4.1

`pip show requests` gives you the version, location, dependencies, and homepage — useful when something breaks.

### 4.2

`pip check` reports dependency conflicts in your environment. Run it now; you should see "No broken requirements."

### 4.3

`pip list --outdated` lists what's behind. Upgrade one (`pip install --upgrade requests`), then re-run `pip freeze > requirements.txt` to save the new version.

## 5. Common Mistakes

### 5.1

Deactivate your venv, then install something:

```bash
deactivate
pip install cowsay
```

Reactivate and try `import cowsay` in Python — it fails, because the package went to your system Python, not the venv. This is the most common beginner mistake. Reinstall it properly with the venv active.

`ModuleNotFoundError` almost always means one of these two things: the package isn't installed, or your venv isn't active. Check the venv first.

### 5.2

Delete your venv folder entirely and try to run your code:

```bash
deactivate
rm -rf .venv   # Windows: rmdir /s /q .venv
python -c "import requests"
```

Nothing is permanently lost — `requirements.txt` still describes the environment. Recreate it:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The venv is disposable; the requirements file is what matters.

## 6. Putting It Together

### Final Exercise

Set up the dependency environment for a small project from scratch.

1. Create a new folder `my-project` with a venv inside it
2. Activate the venv
3. Install these packages: `requests`, `rich`, `pytest`
4. Write a `requirements.txt` (production deps: `requests`, `rich`) and a `requirements-dev.txt` (dev deps: `pytest`) by hand — not with `pip freeze`
5. Write a Python script `main.py` that imports `requests` and prints the status code of a GET request to `https://httpbin.org/get`
6. Run it and confirm it works
7. Deactivate, delete your venv, recreate it from your requirements files, and confirm the script still runs

**The goal:** a project that anyone can clone, run `pip install -r requirements.txt`, and have a working environment — without any manual setup steps.

## Checklist

- [ ] Know how to create and activate a venv on your OS
- [ ] Can install, upgrade, and uninstall packages with pip
- [ ] Understand what `pip freeze` produces and why it's useful
- [ ] Know the difference between `requirements.txt` and `requirements-dev.txt`
- [ ] Can recreate an environment from a requirements file
- [ ] Understand why "ModuleNotFoundError" usually means the venv isn't active
- [ ] Completed the final exercise end-to-end
