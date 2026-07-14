# The DOM

A static HTML page displays content but does nothing when you interact with it. JavaScript is what makes a page interactive, and it does that through the **DOM** — the browser's live, in-memory representation of the page, which your code can read and change.

## Videos

1. [The JavaScript DOM explained in 5 minutes!](https://www.youtube.com/watch?v=NO5kUNxGIu0) — what the DOM actually is and why it exists.
2. [Learn DOM Manipulation In 18 Minutes](https://www.youtube.com/watch?v=y17RuWkWdn8) — selecting elements, changing them, and responding to events.

## Supplementary Notes

Reference for wiring a script into an HTML page and driving the DOM from it.

**Linking a script**

```html
  ...
  <script src="main.js"></script>
</body>
```

Placed at the bottom of `<body>` so the HTML above it exists before the script runs.

**Selecting elements**

`document` exposes the whole page. You can grab any element by id or CSS selector:

```javascript
const heading = document.getElementById("task-1");
const input = document.querySelector("#task-title");
```

In Python terms, `document.getElementById` is a dictionary lookup on a global registry of every element on the page.

**Event listeners**

```javascript
const button = document.querySelector("#my-btn");

button.addEventListener("click", (event) => {
  console.log("clicked!");
});
```

`console.log` output shows up in dev tools (`F12`) → Console.

**Handling form submission**

The browser's default form behavior is a full page reload. `event.preventDefault()` stops that:

```javascript
form.addEventListener("submit", (event) => {
  event.preventDefault();

  const title = titleInput.value.trim();
  if (title.length === 0) return;

  console.log("New task:", title);
  titleInput.value = "";
});
```

**Creating elements dynamically**

```javascript
function createTaskCard(title) {
  const article = document.createElement("article");
  article.className = "task-card";

  const heading = document.createElement("h3");
  heading.textContent = title;

  const deleteBtn = document.createElement("button");
  deleteBtn.type = "button";
  deleteBtn.textContent = "Delete";
  deleteBtn.addEventListener("click", () => article.remove());

  article.appendChild(heading);
  article.appendChild(deleteBtn);
  return article;
}
```

This is the core DOM pattern: create elements, set their properties, wire up events, attach them to the page.
