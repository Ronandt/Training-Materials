# pip and venv Exercises

Python ships with a package manager (pip) and a virtual environment tool (venv). You need both for any real project. This tutorial walks you through them hands-on.

Work through each section in order. Every exercise has something to run in your terminal.

## 0. What problem are we solving?

When you install a package globally with `pip install requests`, it lands in your system Python. That's fine until two projects need different versions of the same library. Virtual environments fix this by giving each project its own isolated Python installation.

The rule is simple: one project, one venv, always activated before you work.

## 1. Creating and Activating a venv

### 1.1

Create a new folder called `pip-exercises` and navigate into it. Then create a virtual environment:

```bash
python -m venv .venv
```

This creates a `.venv` folder. Look inside it — you'll see a copy of Python and a `lib` directory where packages will live.

### 1.2

Activate the environment:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Your terminal prompt should now show `(.venv)` at the start. That's how you know it's active.

**Verify:** Run `which python` (Mac/Linux) or `where python` (Windows). The path should point inside your `.venv` folder, not your system Python.

### 1.3

Check what's currently installed in your fresh environment:

```bash
pip list
```

You should see almost nothing — just `pip` itself and maybe `setuptools`. That's the point. A clean slate for every project.

### 1.4

Deactivate the environment and run `pip list` again. Notice the difference.

```bash
deactivate
pip list
```

Now reactivate before continuing.

## 2. Installing Packages

### 2.1

Install the `requests` library:

```bash
pip install requests
```

Run `pip list` again. It should now appear. Then open a Python shell and confirm it works:

```python
import requests
print(requests.__version__)
```

### 2.2

Install a specific version of a package. The syntax is `package==version`:

```bash
pip install "requests==2.28.0"
```

Check the version again. pip will downgrade if needed.

### 2.3

Install multiple packages at once:

```bash
pip install httpx rich
```

These are common in real projects. `httpx` is a modern HTTP client, `rich` is for pretty terminal output. You don't need to know them — just get comfortable with installing.

### 2.4

Uninstall a package:

```bash
pip uninstall httpx
```

pip will ask for confirmation. Confirm it, then verify it's gone with `pip list`.

## 3. Requirements Files

This is how you share dependencies with your team or deploy to a server.

### 3.1

Freeze your current environment into a `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Open the file. Every installed package is listed with its exact version. This is what gets committed to git.

### 3.2

Create a new virtual environment in a separate folder to simulate a fresh machine:

```bash
mkdir fresh-install
cd fresh-install
python -m venv .venv
source .venv/bin/activate   # or the Windows equivalent
```

Install everything from the requirements file:

```bash
pip install -r ../requirements.txt
```

Run `pip list`. It should match your original environment exactly.

Deactivate and go back to your `pip-exercises` folder.

### 3.3

Most projects separate dev dependencies (linters, test runners) from production dependencies. By convention you'd have two files:

- `requirements.txt` — what the app needs to run
- `requirements-dev.txt` — what developers additionally need

Create `requirements-dev.txt` manually and add:

```
pytest
```

Install it:

```bash
pip install -r requirements-dev.txt
```

The idea: when deploying to production, you only install `requirements.txt`. Locally you install both.

## 4. pip show and pip check

### 4.1

Get detailed info about an installed package:

```bash
pip show requests
```

This tells you the version, where it's installed, its dependencies, and its homepage. Useful when something breaks.

### 4.2

Check for dependency conflicts in your environment:

```bash
pip check
```

If everything is consistent, you'll see "No broken requirements." This is worth running after installing or upgrading anything significant.

### 4.3

List outdated packages:

```bash
pip list --outdated
```

Try upgrading one:

```bash
pip install --upgrade rich
```

Then run `pip freeze > requirements.txt` again to save the updated version.

## 5. Common Mistakes

### 5.1

Run this without activating your venv first:

```bash
deactivate
pip install cowsay
```

Now activate your venv and try to import it:

```python
import cowsay
```

It will fail. This is the most common mistake beginners make — installing without the venv active means the package goes to the wrong place.

Activate your venv and install it again properly.

### 5.2

Try importing a package that isn't installed:

```python
import pandas
```

Read the error. `ModuleNotFoundError` means either the package isn't installed, or you're in the wrong environment. When you see this error on a real project, the first thing to check is whether your venv is active.

### 5.3

What happens when you delete your venv folder and try to run your code?

```bash
deactivate
rm -rf .venv   # Windows: rmdir /s /q .venv
python -c "import requests"
```

Nothing is permanently lost — you still have `requirements.txt`. Recreate the environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This is the point of `requirements.txt`. The venv is disposable; the file is what matters.

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
