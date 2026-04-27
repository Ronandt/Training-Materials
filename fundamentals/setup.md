# Dev Environment Setup

Before writing any code, you need the right tools installed. This guide walks you through every tool used in the fundamentals track, in the order you should install them.

Work through each section in order. Every step has a verification command — run it before moving on.

## 1. Visual Studio Code

VS Code is the code editor you'll use for everything. It's free, fast, and has extensions for every language.

### 1.1

Download and install VS Code from [https://code.visualstudio.com](https://code.visualstudio.com). Choose the installer for your OS.

During installation on Windows, check both of these options when they appear:
- **Add "Open with Code" action to Windows Explorer file context menu**
- **Add to PATH**

On Mac, after opening the app, open the Command Palette (`Cmd+Shift+P`), type `shell command`, and select **Shell Command: Install 'code' command in PATH**.

### 1.2

Verify VS Code is on your PATH:

```bash
code --version
```

You should see a version number. If the command is not found, restart your terminal and try again.

### 1.3

Install these extensions — open VS Code, go to the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`), and search for each:

- **Python** (by Microsoft) — Python language support
- **Pylance** (by Microsoft) — Python type checking and autocomplete
- **ESLint** (by Microsoft) — JavaScript/TypeScript linting

You'll add more extensions as you move into frontend and backend work. These cover the fundamentals track.

## 2. Git

Git is the version control system. Every project uses it. GitHub Desktop (next section) is a graphical interface on top of Git, but Git itself must be installed first.

### 2.1

**Windows:** Download from [https://git-scm.com/download/win](https://git-scm.com/download/win) and run the installer. Accept all defaults. When asked which editor Git should use by default, select VS Code.

**Mac:** Git comes with Xcode Command Line Tools. Run:

```bash
xcode-select --install
```

A dialog will appear — click Install. If you already have it, the command will tell you.

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install git
```

### 2.2

Verify the installation:

```bash
git --version
```

### 2.3

Configure Git with your name and email. These appear on every commit you make:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the same email address you'll use for your GitHub account.

Verify it saved:

```bash
git config --global --list
```

You should see `user.name` and `user.email` in the output.

## 3. GitHub Desktop

GitHub Desktop gives you a visual interface for Git operations — committing, pushing, branching, and reviewing changes. You'll use it alongside the terminal.

### 3.1

Download from [https://desktop.github.com](https://desktop.github.com) and install.

### 3.2

Open GitHub Desktop and sign in with your GitHub account. If you don't have one, create a free account at [https://github.com](https://github.com) first.

### 3.3

In GitHub Desktop, go to **File → Options** (Windows) or **GitHub Desktop → Settings** (Mac) and confirm your Git config (name and email) matches what you set in section 2.3.

**Verify:** Clone a repository using GitHub Desktop (File → Clone Repository). You can use any public repository. The point is to confirm the tool works end-to-end — cloning, and seeing the files appear locally.

## 4. Python

Python is needed for the Python fundamentals exercises (pip, venv) and any backend work later.

### 4.1

**Windows:** Download the latest stable release from [https://www.python.org/downloads](https://www.python.org/downloads). Run the installer and **check the box that says "Add Python to PATH"** before clicking Install Now. This is easy to miss and causes problems if skipped.

**Mac:** Use Homebrew. If you don't have Homebrew yet:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Python:

```bash
brew install python
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install python3 python3-pip
```

### 4.2

Verify Python is installed and on your PATH:

```bash
python --version
```

On Mac/Linux this may be `python3 --version` instead. Both are fine — just note which command works for you, as you'll use it throughout the exercises.

### 4.3

Verify pip is available:

```bash
pip --version
```

Again, may be `pip3` on Mac/Linux. If pip is missing on Linux, install it:

```bash
sudo apt install python3-pip
```

## 5. Node.js

Node.js is the JavaScript/TypeScript runtime. It comes with npm (the Node package manager). You need it for the TypeScript exercises and all frontend and backend JavaScript work.

### 5.1

Download the **LTS** (Long Term Support) release from [https://nodejs.org](https://nodejs.org). LTS is the stable version — avoid Current unless you have a specific reason.

**Mac alternative (recommended):** Use Homebrew:

```bash
brew install node
```

**Linux (Ubuntu/Debian):**

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs
```

### 5.2

Verify both Node.js and npm are installed:

```bash
node --version
npm --version
```

Both should print version numbers.

### 5.3

Install `tsx` globally. This lets you run TypeScript files directly without a separate compile step — you'll use it throughout the TypeScript exercises:

```bash
npm install -g tsx
```

Verify:

```bash
tsx --version
```

### 5.4

Create a file called `hello.ts` anywhere, write one line:

```ts
console.log("TypeScript is working");
```

Run it:

```bash
tsx hello.ts
```

If you see the output, your Node/TypeScript setup is complete. Delete the file.

## Checklist

- [ ] VS Code is installed and `code --version` works in the terminal
- [ ] Python and ESLint extensions are installed in VS Code
- [ ] Git is installed and `git --version` works
- [ ] Git is configured with your name and email (`git config --global --list`)
- [ ] GitHub Desktop is installed and signed into your GitHub account
- [ ] Python is installed and `python --version` (or `python3 --version`) works
- [ ] pip is available (`pip --version` or `pip3 --version`)
- [ ] Node.js and npm are installed (`node --version` and `npm --version`)
- [ ] `tsx` is installed globally and `tsx --version` works
- [ ] You ran a `.ts` file with `tsx` and saw output
