# VS Code Extensions and Shortcuts

VS Code ships with a lot - but its real power comes from extensions and keyboard shortcuts. Extensions add language support, linting, Git tools, and formatting. Shortcuts let you navigate and edit without touching the mouse. Together, they cut the friction out of your daily workflow.

Work through each section in order. Every section ends harder than it starts.

**Reference:** [VS Code Extension Marketplace](https://marketplace.visualstudio.com) · [VS Code Keyboard Shortcuts (Windows)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf) · [VS Code Keyboard Shortcuts (Mac)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)

---

## 1. The Extensions Panel

The Extensions panel is where you find, install, manage, and remove extensions.

### 1.1

Open the Extensions panel:

- **Windows/Linux:** `Ctrl+Shift+X`
- **Mac:** `Cmd+Shift+X`

You can also click the square icon in the left Activity Bar.

In the search box, type `Python`. You will see the **Python** extension by Microsoft at or near the top. If it's already installed, it will say **Installed**.

### 1.2

Find an extension you have installed (try **Python** or **ESLint**). Click on it to open its detail page. Explore what is there:

- **Changelog** tab - what changed in recent versions
- **Feature Contributions** - commands, settings, and keybindings the extension adds
- The gear icon next to the **Disable** button - options to disable globally or for the current workspace only

Disable the extension, then re-enable it. Notice that some extensions require a reload - VS Code will show a **Reload Required** button when they do.

### 1.3

Search for and install **Prettier - Code formatter** (by Prettier). This is the standard formatter for JavaScript, TypeScript, JSON, and CSS.

After it installs, open its detail page and read the **Feature Contributions → Settings** section. You will see which settings it adds to VS Code.

### 1.4

Search for and install **Error Lens** (by Alexander). This extension shows error and warning messages inline, next to the line that caused them, instead of requiring you to hover.

Open any `.py` or `.ts` file, deliberately introduce a type error or syntax mistake, and observe the difference from how errors appeared before.

### 1.5 - Challenge

Find two extensions you did not already know about by browsing the Marketplace (sort by **Most Popular** or explore the **Programming Languages** and **Linters** categories). Install one. Write a one-line comment at the top of a scratch file explaining what it does and why you might want it. You do not need to keep it installed.

---

## 2. Format on Save and Extension Settings

Extensions expose their own settings. Some of the most useful ones are about automation - things that happen when you save a file.

### 2.1

Open VS Code settings:

- **Windows/Linux:** `Ctrl+,`
- **Mac:** `Cmd+,`

Search for `format on save`. Enable the **Editor: Format On Save** checkbox. This tells VS Code to run the configured formatter every time you save a file.

### 2.2

Create a file called `messy.ts` and paste in something deliberately poorly formatted:

```ts
const x=1
const   y =    2
function add(a:number,b:number){return a+b}
console.log(add(x,y))
```

Save the file (`Ctrl+S` / `Cmd+S`). If Prettier is installed and format on save is on, it will clean it up automatically.

If nothing happened, open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`), type `Format Document`, and run it. If VS Code prompts you to select a formatter, choose **Prettier**.

### 2.3

Open settings again and search for `default formatter`. Set **Editor: Default Formatter** to `Prettier - Code formatter`. This is the setting that controls which formatter runs on `Format Document`.

### 2.4

Settings come in two scopes:

- **User settings** - apply everywhere across all projects
- **Workspace settings** - stored in `.vscode/settings.json` in the project folder, override user settings for that project, and can be committed to version control

Open the Command Palette, type `Open Workspace Settings (JSON)`, and run it. VS Code will create `.vscode/settings.json` if it doesn't exist.

Add this to the file:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

This locks the formatter for everyone who opens this project in VS Code.

### 2.5

When a teammate clones your project and opens it in VS Code, they have none of your extensions. You can fix this by committing a list of recommended extensions alongside your code. VS Code reads it and prompts them to install everything in one click.

Create `.vscode/extensions.json` in your project folder:

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "usernamehw.errorlens"
  ]
}
```

Each string is an extension's **identifier** — not its display name. To find an identifier: open the extension's detail page in VS Code and look for the ID under the extension name, or find it in the Marketplace URL.

Add a `recommendations` entry for at least three extensions relevant to this project. Commit the file.

**Verify:** Open the Extensions panel and type `@recommended` in the search box. VS Code will show your list separated into workspace recommendations and other recommendations.

### 2.6

Prettier handles JavaScript and TypeScript. Python has its own formatter: **Black**. Black is opinionated — it makes almost all decisions for you, so there is no bikeshedding over style.

Install Black into your active virtual environment:

```bash
pip install black
```

Then install the **Black Formatter** extension in VS Code (search for `Black Formatter` by Microsoft).

Create a file called `messy.py` and paste in something poorly formatted:

```python
x=1
y =   2
def add( a,b ):
    return a+b
print(  add(x,y)  )
```

Open the Command Palette, run **Format Document**, and select **Black Formatter** when prompted. Confirm it reformats the file.

### 2.7

Black is configured via `pyproject.toml`. This file lives at the root of your project and can hold configuration for multiple Python tools at once.

Create `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ["py311"]
```

- `line-length` — Black's default is 88. Some teams use 79 (PEP 8) or 100.
- `target-version` — tells Black which Python syntax it can use. Match this to the Python version your project runs on.

Save the file, then reformat `messy.py` again. Try changing `line-length` to something very short (e.g. 40) and reformat. Watch how Black aggressively wraps lines to stay within the limit.

To see every option Black supports, run:

```bash
black --help
```

### 2.8

When a project has both Python and TypeScript files, you want Prettier for `.ts` files and Black for `.py` files. VS Code lets you set the default formatter **per language** in `settings.json`.

Open `.vscode/settings.json` and update it to this:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

The `[python]` block overrides the global default for Python files only. The outer `editor.defaultFormatter` still applies to TypeScript, JSON, and everything else.

**Verify:** Open `messy.py` and save — Black runs. Open `messy.ts` and save — Prettier runs. They should not interfere with each other.

### 2.9 - Challenge

Research how to configure Prettier's formatting rules using a `.prettierrc` file (JSON format). Create one in any folder with at least two custom rules (e.g. `tabWidth`, `singleQuote`, `semi`). Verify it takes effect by saving a file that violates one of your rules.

---

## 3. Core Keyboard Shortcuts

Learning shortcuts removes the constant hand-reach for the mouse. These are the ones you will use every single day.

### 3.1

**The Command Palette** - the single most important shortcut in VS Code:

- **Windows/Linux:** `Ctrl+Shift+P`
- **Mac:** `Cmd+Shift+P`

The Command Palette gives you access to every command in VS Code and every installed extension. Any time you cannot remember a shortcut, open this and type what you want to do.

Open it now and type `toggle terminal`. Select **Terminal: Toggle Integrated Terminal**. Close the terminal the same way.

### 3.2

**Quick Open** - jump to any file by name without using the Explorer:

- **Windows/Linux:** `Ctrl+P`
- **Mac:** `Cmd+P`

Type part of a filename. VS Code fuzzy-matches - you don't need to type the full name or path. Practice opening three different files this way without touching the mouse.

### 3.3

**Go to Line** - jump to a specific line number in the current file:

- **Windows/Linux:** `Ctrl+G`
- **Mac:** `Ctrl+G`

Open any file that is more than 30 lines long, press `Ctrl+G`, and type `30`. Press Enter. Confirm the cursor is on line 30.

### 3.4

**Find in current file** and **Find and Replace**:

| Action | Windows/Linux | Mac |
|---|---|---|
| Find | `Ctrl+F` | `Cmd+F` |
| Find and Replace | `Ctrl+H` | `Cmd+H` |
| Find in all files | `Ctrl+Shift+F` | `Cmd+Shift+F` |

Open any file. Press `Ctrl+F` and search for a word that appears multiple times. Press `Enter` or `F3` to cycle through matches. Press `Escape` to close the search bar.

### 3.5

**Move and duplicate lines** - rearranging code without cut-paste:

| Action | Windows/Linux | Mac |
|---|---|---|
| Move line up | `Alt+Up` | `Option+Up` |
| Move line down | `Alt+Down` | `Option+Down` |
| Duplicate line down | `Shift+Alt+Down` | `Shift+Option+Down` |

Write three lines of text in a scratch file. Reorder them using only the move shortcuts.

### 3.6

**Multi-cursor editing** - editing multiple places at once:

| Action | Windows/Linux | Mac |
|---|---|---|
| Add cursor above | `Ctrl+Alt+Up` | `Ctrl+Opt+Up` |
| Add cursor below | `Ctrl+Alt+Down` | `Ctrl+Opt+Down` |
| Add cursor at click | `Alt+Click` | `Opt+Click` |
| Select all occurrences of word | `Ctrl+Shift+L` | `Cmd+Shift+L` |

Write a block like this in a scratch file:

```
firstName: "",
lastName: "",
email: "",
```

Place your cursor on the first `""`. Use `Ctrl+Alt+Down` (or `Ctrl+Opt+Down`) to add cursors on the next two lines. All three cursors should be active. Type something - it will appear in all three places at once. Press `Escape` to return to a single cursor.

### 3.7 - Challenge

Open any file in this repo. Using only keyboard shortcuts (no mouse):

1. Open the file with **Quick Open**
2. Jump to line 20
3. Find all occurrences of a word that appears multiple times
4. Rename all occurrences at once using multi-cursor
5. Undo your changes

Complete all five steps without reaching for the mouse.

---

## 4. Editor Navigation Shortcuts

These shortcuts move you around the editor quickly - between files, panels, and splits.

### 4.1

**Sidebar and panel toggles:**

| Action | Windows/Linux | Mac |
|---|---|---|
| Toggle sidebar | `Ctrl+B` | `Cmd+B` |
| Toggle integrated terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| Toggle Explorer | `Ctrl+Shift+E` | `Cmd+Shift+E` |
| Toggle Source Control | `Ctrl+Shift+G` | `Cmd+Shift+G` |

Toggle each panel open and closed using its shortcut. Note that `Ctrl+B` (`Cmd+B`) closes whichever sidebar panel is currently open.

### 4.2

**Switching between open files (tabs):**

| Action | Windows/Linux | Mac |
|---|---|---|
| Next tab | `Ctrl+Tab` | `Ctrl+Tab` |
| Previous tab | `Ctrl+Shift+Tab` | `Ctrl+Shift+Tab` |
| Close current tab | `Ctrl+W` | `Cmd+W` |
| Reopen closed tab | `Ctrl+Shift+T` | `Cmd+Shift+T` |

Open four or five files, then navigate between them using `Ctrl+Tab` only.

### 4.3

**Split editor** - view two files side by side:

- **Windows/Linux:** `Ctrl+\`
- **Mac:** `Cmd+\`

Split the editor. Open a different file in the new pane. Switch focus between panes using `Ctrl+1` and `Ctrl+2` (same on Mac). Close the split with `Ctrl+W` while focused in the extra pane.

### 4.4

**Go to Definition** - jump to where a function, variable, or type is defined:

- `F12`
- Or right-click → **Go to Definition**

Open the TypeScript tutorial file. Place your cursor on any built-in TypeScript type (e.g. `number`, `string`) and press `F12`. VS Code will open the type definition from the TypeScript standard library. Press `Alt+Left` (`Ctrl+-` on Mac) to navigate back.

### 4.5 - Challenge

You have been given a codebase to explore. Without using the mouse or the Explorer panel:

1. Open the Command Palette and use **Go to Symbol in Workspace** (`Ctrl+T` / `Cmd+T`) to jump to a function by name
2. Open a second file in a split
3. Jump back and forth between the two panes using `Ctrl+1` / `Ctrl+2`
4. Close both splits and return to a single editor

---

## 5. Customizing Shortcuts

VS Code's shortcuts can be changed. Any command can be assigned a new key, and keys can be reassigned if they conflict with habits from other editors.

### 5.1

Open the Keyboard Shortcuts editor:

- **Windows/Linux:** `Ctrl+K Ctrl+S` (press `Ctrl+K`, then `Ctrl+S` while still holding `Ctrl`)
- **Mac:** `Cmd+K Cmd+S`

Or open the Command Palette and search for **Preferences: Open Keyboard Shortcuts**.

### 5.2

In the Keyboard Shortcuts editor, search for `format document`. You will see the current binding. Click the pencil icon on the left to reassign it. Press the key combination you want to use. Press `Enter` to confirm.

> Note: If the key combination is already used by another command, VS Code will warn you. Read the conflict and decide whether to override or pick a different key.

### 5.3

Keyboard shortcuts are stored in `keybindings.json`. Click the **Open Keyboard Shortcuts (JSON)** button in the top right corner of the Keyboard Shortcuts editor (the document icon).

Each entry looks like this:

```json
{
  "key": "ctrl+shift+d",
  "command": "editor.action.copyLinesDownAction",
  "when": "editorTextFocus"
}
```

- `key` - the key combination
- `command` - the VS Code command ID
- `when` - a condition for when the shortcut is active (optional but common)

Add a custom entry manually. Pick any command you use frequently (find it in the Keyboard Shortcuts UI, note its command ID), assign it a key you prefer, and save the file.

### 5.4 - Challenge

Look up how to create a **chord shortcut** in VS Code - a two-step shortcut where you press one key combo, then a second one (similar to how `Ctrl+K Ctrl+S` opens the Keyboard Shortcuts editor). Create one for a command of your choice and test it.

---

## Checklist

- [ ] Can open and search the Extensions panel without a mouse
- [ ] Installed Prettier and Error Lens
- [ ] Format on Save is enabled; saving a messy TypeScript file cleans it up
- [ ] Know the difference between User settings and Workspace settings
- [ ] Can create a `.vscode/settings.json` and explain why you would commit it
- [ ] Can create a `.vscode/extensions.json` with extension recommendations and verify it with `@recommended`
- [ ] Can install Black and format a Python file with it from inside VS Code
- [ ] Can configure Black's line length and target Python version via `pyproject.toml`
- [ ] Can set per-language formatters in `.vscode/settings.json` so Black handles `.py` and Prettier handles `.ts`
- [ ] Can open any file by name using Quick Open without typing the full path
- [ ] Can jump to a specific line number in a file
- [ ] Can use multi-cursor editing to edit multiple lines simultaneously
- [ ] Can split the editor and navigate between panes with keyboard shortcuts
- [ ] Can use Go to Definition and navigate back
- [ ] Can open the Keyboard Shortcuts editor and reassign a shortcut
- [ ] Can edit `keybindings.json` directly to add a custom binding
