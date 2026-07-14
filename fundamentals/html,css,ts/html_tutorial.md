# HTML Exercises

HTML (HyperText Markup Language) is the structure of every web page. It describes what content exists and what it means — headings, paragraphs, links, images, forms — without saying anything about how it looks. Browsers read HTML and render it into a visual page.

Work through each section in order. Every exercise opens in your browser — no build tools or installs needed.

**This tutorial is standalone.** All you need is a text editor and a browser.

Continuation tutorials build on this one:
- **CSS tutorial:** Style the pages you build here
- **DOM tutorial:** Make the pages you build here interactive with TypeScript
- **React tutorial:** JSX is HTML-like syntax — understanding HTML makes it intuitive

## 0. Setup

### 0.1

Create a folder called `html-exercises`. Inside it, create a file called `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My Page</title>
  </head>
  <body>
    <h1>Hello, world</h1>
  </body>
</html>
```

Open the file in your browser: right-click it in your file explorer → **Open with** → your browser. You will see the heading.

The `<!DOCTYPE html>` declaration tells the browser to use modern HTML. `<head>` contains metadata the browser reads but does not display. `<body>` contains everything the user sees.

### 0.2

Change the `<title>` text to `Task Manager`. Switch to the browser and notice the tab title updated. The `<title>` is one of the few head elements that is visible — in the tab, not in the page body.

Every time you save `index.html` and refresh the browser (`F5` or `Cmd+R`), you see the updated page.

## 1. Text and Structure

HTML elements are written as **tags**: an opening tag `<p>`, content, and a closing tag `</p>`. Some elements are **self-closing** and have no content: `<br />`, `<img />`, `<input />`.

### 1.1

Add these heading levels to `<body>`:

```html
<h1>Task Manager</h1>
<h2>Today's Tasks</h2>
<h3>High Priority</h3>
```

There are six heading levels: `<h1>` through `<h6>`. `<h1>` is the main page heading — use it once per page. Headings convey hierarchy, not just size; do not use `<h3>` unless there is a parent `<h2>`.

### 1.2

Add a paragraph and a line break:

```html
<p>Track your work and stay organised. Add tasks, set priorities, and mark them done.</p>
<p>Today is <strong>Monday</strong>. You have <em>3 tasks</em> remaining.</p>
```

- `<p>` — paragraph, adds vertical space above and below
- `<strong>` — bold, indicates importance
- `<em>` — italic, indicates emphasis

### 1.3

Add both types of list:

```html
<h2>Unordered list</h2>
<ul>
  <li>Write tests</li>
  <li>Review PR</li>
  <li>Update docs</li>
</ul>

<h2>Ordered list</h2>
<ol>
  <li>Read the brief</li>
  <li>Plan the work</li>
  <li>Implement</li>
  <li>Ship</li>
</ol>
```

`<ul>` renders bullet points. `<ol>` renders numbered items. `<li>` is a list item — it must appear inside `<ul>` or `<ol>`.

### 1.4 — Challenge

Add an HTML comment — text that appears in the source but not in the browser:

```html
<!-- This section will be replaced with dynamic content later -->
```

Open your browser's developer tools (`F12`) and look at the Elements panel. You can see the full HTML including comments. Get used to having the dev tools open — you will use them constantly.

## 2. Links and Images

### 2.1

Add a link:

```html
<a href="https://developer.mozilla.org">MDN Web Docs</a>
```

`<a>` is the anchor element. `href` (hypertext reference) is the destination. Without `href`, the element is not a link. Click it — you navigate to MDN.

Add a link to another page in the same folder. First create `tasks.html` (a minimal HTML file with a heading). Then link to it:

```html
<a href="tasks.html">Go to Tasks</a>
```

Relative paths (no `https://`) navigate within the same site.

### 2.2

Add an image:

```html
<img src="https://placehold.co/200x100" alt="A placeholder image" />
```

- `src` — the image URL or relative path
- `alt` — description shown if the image fails to load; read by screen readers; required for accessibility

`<img />` is self-closing — no content, no closing tag. Download any small image into your folder and reference it by filename in `src`.

### 2.3 — Challenge

Wrap an image in a link so clicking the image navigates somewhere:

```html
<a href="tasks.html">
  <img src="https://placehold.co/200x100" alt="Go to tasks" />
</a>
```

Elements can be nested inside one another. The rule is that **block elements** (like `<p>`, `<div>`) cannot be nested inside **inline elements** (like `<a>`, `<span>`), but inline elements can nest inside block elements. A link wrapping an image is valid.

## 3. Forms

Forms are how users send data to a server — or in React apps, to JavaScript event handlers. Understanding form elements is essential for building any interactive UI.

### 3.1

Create a basic form in `index.html`:

```html
<form>
  <label for="task-title">Task title</label>
  <input type="text" id="task-title" name="title" placeholder="Enter a task..." />
  <button type="submit">Add Task</button>
</form>
```

- `<form>` — wraps a group of inputs
- `<label>` — text label for an input; the `for` attribute matches the input's `id`, so clicking the label focuses the input
- `<input>` — a single-line text field; `type="text"` is the default
- `<button type="submit">` — submits the form

Click the button. The page reloads (the form's default behaviour). In JavaScript and React you will call `e.preventDefault()` to stop this.

### 3.2

Add more input types to the form:

```html
<label for="priority">Priority</label>
<select id="priority" name="priority">
  <option value="low">Low</option>
  <option value="medium" selected>Medium</option>
  <option value="high">High</option>
</select>

<label for="description">Description</label>
<textarea id="description" name="description" rows="3" placeholder="Optional details..."></textarea>

<label>
  <input type="checkbox" name="urgent" value="yes" />
  Mark as urgent
</label>
```

- `<select>` + `<option>` — a dropdown; `selected` pre-selects an option
- `<textarea>` — multi-line text input; `rows` sets the visible height
- `<input type="checkbox">` — a checkbox; wrapping it in `<label>` makes the label text clickable

### 3.3

Add a radio group — a set of options where only one can be selected:

```html
<fieldset>
  <legend>Status</legend>
  <label><input type="radio" name="status" value="todo" checked /> Todo</label>
  <label><input type="radio" name="status" value="in-progress" /> In Progress</label>
  <label><input type="radio" name="status" value="done" /> Done</label>
</fieldset>
```

All radio inputs in a group share the same `name`. The `checked` attribute pre-selects one option. `<fieldset>` groups related inputs; `<legend>` labels the group — this matters for screen readers.

### 3.4 — Challenge

Add validation attributes to the task title input:

```html
<input
  type="text"
  id="task-title"
  name="title"
  placeholder="Enter a task..."
  required
  minlength="3"
  maxlength="200"
/>
```

Try submitting the form with an empty title — the browser shows a validation error without any JavaScript. Try `type="email"` on a new input and submit an invalid email. Browser-native validation is a baseline; you will add more thorough validation with Pydantic (backend) and React state (frontend).

## 4. Semantic HTML

HTML has two categories of elements: **generic containers** (`<div>`, `<span>`) and **semantic elements** that describe what their content means (`<nav>`, `<main>`, `<article>`, `<header>`, `<footer>`). Using semantic elements makes your HTML more readable and accessible.

### 4.1

Replace the body of `index.html` with a structured layout using semantic elements:

```html
<body>
  <header>
    <h1>Task Manager</h1>
    <nav>
      <a href="index.html">Home</a>
      <a href="tasks.html">Tasks</a>
    </nav>
  </header>

  <main>
    <section>
      <h2>Add a Task</h2>
      <!-- your form goes here -->
    </section>

    <section>
      <h2>Recent Tasks</h2>
      <ul>
        <li>Write tests</li>
        <li>Review PR</li>
      </ul>
    </section>
  </main>

  <footer>
    <p>Task Manager &copy; 2026</p>
  </footer>
</body>
```

- `<header>` — introductory content for the page or a section
- `<nav>` — a block of navigation links
- `<main>` — the primary content of the page; use it once
- `<section>` — a thematic grouping of content; should have a heading
- `<footer>` — closing content (credits, links, copyright)

The page looks identical to using `<div>` everywhere — the semantic meaning is for screen readers, search engines, and other developers reading the code.

### 4.2

Use `<article>` for self-contained pieces of content that make sense on their own (a task card, a blog post, a comment):

```html
<section>
  <h2>Recent Tasks</h2>
  <article>
    <h3>Write tests</h3>
    <p>Priority: <strong>High</strong></p>
  </article>
  <article>
    <h3>Review PR</h3>
    <p>Priority: <strong>Medium</strong></p>
  </article>
</section>
```

Use `<div>` only when no semantic element fits — for example, a wrapper you need purely for CSS layout.

### 4.3 — Challenge

Add `id` and `class` attributes to your elements:

```html
<article id="task-1" class="task-card">
  <h3 class="task-title">Write tests</h3>
  <p class="task-priority">Priority: <strong>High</strong></p>
</article>
```

- `id` — unique identifier; only one element per page should have a given id
- `class` — reusable label; multiple elements can share a class; one element can have multiple classes separated by spaces

These attributes do nothing by themselves — they are hooks for CSS (`.task-card { ... }`) and JavaScript (`document.getElementById("task-1")`). In the CSS tutorial you will use them to apply styles.

## 5. Putting It Together

### Final Exercise

Build a complete `index.html` for the Task Manager. No CSS yet — focus on correct structure and semantics.

**Requirements:**

```
<header>
  ├── Site title as <h1>
  └── <nav> with links to Home and Tasks pages

<main>
  ├── <section> "Add a Task"
  │    └── <form> with:
  │         ├── Text input for title (required, minlength="3")
  │         ├── <select> for priority (low / medium / high)
  │         ├── <textarea> for description (optional)
  │         ├── Radio group for status (todo / in-progress / done)
  │         └── Submit button
  │
  └── <section> "Tasks"
       └── Three <article> task cards, each with:
            ├── Task title as <h3>
            ├── Priority paragraph
            ├── Status paragraph
            └── A "Delete" button (type="button")

<footer>
  └── Copyright line
```

Open the finished page in the browser. Open dev tools (`F12`) → Elements panel. Expand the tree and verify the nesting matches the structure above. Use the Accessibility tab if available — confirm heading levels are in order and all inputs have labels.

## Checklist

- [ ] Understand the role of `<!DOCTYPE html>`, `<head>`, and `<body>`
- [ ] Can use heading levels `<h1>`–`<h3>` with correct hierarchy
- [ ] Can write paragraphs, bold text, and emphasised text
- [ ] Can create ordered and unordered lists
- [ ] Can add links with `<a href="">` (absolute and relative)
- [ ] Can add images with `<img src="" alt="" />`
- [ ] Can build a form with `<input>`, `<select>`, `<textarea>`, checkbox, and radio inputs
- [ ] Know why `<label for="">` matters
- [ ] Can add browser-native validation with `required`, `minlength`, `type="email"`
- [ ] Know when to use `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- [ ] Know the difference between `id` (unique) and `class` (reusable)
- [ ] Know when to use `<div>` vs a semantic element
