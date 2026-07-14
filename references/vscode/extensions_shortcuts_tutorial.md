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

### 2.6 - Challenge

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

