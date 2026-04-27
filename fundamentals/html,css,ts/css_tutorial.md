# CSS Exercises

CSS (Cascading Style Sheets) controls how HTML looks — colours, fonts, spacing, layout. HTML describes structure; CSS describes presentation. They are always separate files.

Work through each section in order. Every exercise shows immediate visual change in your browser.

**This is a continuation of the HTML tutorial.** Use the `index.html` you built in the HTML final exercise. If you do not have it, create a minimal `index.html` with a heading, a paragraph, a form, and a few task cards.

The CSS tutorial connects forward to the React tutorial — Tailwind CSS is a collection of utility classes that map one-to-one to regular CSS properties. Once you understand the CSS property, the Tailwind class is obvious.

## 0. Setup

### 0.1

Create `style.css` in the same folder as `index.html`. Link it from the `<head>`:

```html
<head>
  <meta charset="UTF-8" />
  <title>Task Manager</title>
  <link rel="stylesheet" href="style.css" />
</head>
```

Add a rule to confirm the link works:

```css
body {
  background-color: #f9fafb;
}
```

Save and refresh. The page background should turn light gray. Open browser dev tools (`F12`) → Elements panel → select `<body>` → check the Styles panel on the right. You will see the rule listed. This is the main debugging tool for CSS.

### 0.2

CSS rules have two parts: a **selector** (what to target) and **declarations** (what to change). Each declaration is a property–value pair:

```css
selector {
  property: value;
  another-property: value;
}
```

Add a rule for all headings:

```css
h1 {
  color: #111827;
  font-size: 2rem;
}
```

`rem` is a relative unit — `1rem` equals the browser's base font size (usually 16px). Using `rem` instead of `px` respects a user's font-size preference.

## 1. Selectors

### 1.1

There are three fundamental selector types:

```css
/* Element selector — targets every <p> */
p {
  color: #374151;
}

/* Class selector — targets every element with class="task-card" */
.task-card {
  background-color: #ffffff;
}

/* ID selector — targets the one element with id="main-heading" */
#main-heading {
  font-size: 2.5rem;
}
```

Add `class="task-card"` to each task `<article>` in your HTML. Then write a `.task-card` rule that gives them a white background and adds `padding: 1rem`.

### 1.2

Selectors can be combined:

```css
/* Descendant — <p> inside .task-card */
.task-card p {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Multiple selectors — same rule for h2 and h3 */
h2, h3 {
  font-weight: 600;
}
```

Write a rule that targets only `<strong>` elements inside `.task-card` and makes them a dark color.

### 1.3

**Pseudo-classes** target elements in a specific state:

```css
a:hover {
  color: #2563eb;
  text-decoration: underline;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

Add these rules to `style.css`. Hover over links, focus inputs by clicking them, and observe the state changes. The `outline` on `:focus` is important for keyboard accessibility — never remove it without providing a visible alternative.

### 1.4 — Challenge

Use the `:nth-child` pseudo-class to stripe alternate list items:

```css
li:nth-child(odd) {
  background-color: #f3f4f6;
}
li:nth-child(even) {
  background-color: #ffffff;
}
```

Apply padding to the `<li>` elements so the stripes are visible. Then remove the rule and instead use `:hover` to highlight the row the user is mousing over.

## 2. The Box Model

Every HTML element is a rectangular box. The box model describes how the browser calculates its size:

```
┌────────────────────────────────┐
│            margin              │   space outside the border
│  ┌──────────────────────────┐  │
│  │         border           │  │   the visible edge
│  │  ┌────────────────────┐  │  │
│  │  │      padding       │  │  │
│  │  │  ┌──────────────┐  │  │  │
│  │  │  │   content    │  │  │  │
│  │  │  └──────────────┘  │  │  │
│  │  └────────────────────┘  │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
```

### 2.1

Add these rules to `.task-card`:

```css
.task-card {
  background-color: #ffffff;
  padding: 1rem;          /* space inside the border */
  margin-bottom: 1rem;    /* space below each card */
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;  /* rounded corners */
}
```

Open dev tools → select a `.task-card` → look at the box model diagram in the Styles/Computed panel. You will see the exact pixel values for each layer.

### 2.2

By default, `width` and `height` only set the content area — padding and border are added on top, making the total larger than expected. Fix this with `box-sizing`:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Put this at the top of `style.css`. It applies to every element. Now `width: 300px` means the total box is 300px — padding and border are included inside that width. This is how every modern CSS framework (including Tailwind) works.

### 2.3

Control size explicitly:

```css
.task-card {
  width: 100%;
  max-width: 400px;
}

input, textarea, select {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
}
```

`max-width` sets an upper limit — the element shrinks on smaller screens but does not grow past `400px`. Verify by resizing the browser window.

### 2.4 — Challenge

Use margin shorthand. The four values correspond to top, right, bottom, left (clockwise from the top):

```css
margin: 0 auto;        /* 0 top/bottom, auto left/right → centres the block */
padding: 1rem 2rem;    /* 1rem top/bottom, 2rem left/right */
```

Centre the task form section horizontally using `margin: 0 auto` and `max-width`. Confirm it stays centred when you resize the window.

## 3. Typography and Colour

### 3.1

Set a base font for the page:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 1rem;
  line-height: 1.5;
  color: #111827;
  background-color: #f9fafb;
}
```

`font-family` lists fonts in priority order — the browser uses the first one it finds. The list above uses system fonts so no external font needs to be downloaded. `line-height: 1.5` (150% of the font size) is the recommended minimum for readability.

### 3.2

CSS colours can be written in several formats — they all produce the same result:

```css
color: red;               /* named colour */
color: #111827;           /* hex — most common */
color: rgb(17, 24, 39);   /* RGB */
color: hsl(222, 47%, 11%);/* hue, saturation, lightness */
```

Style the page typography:

```css
h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
}

h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

p {
  color: #6b7280;
}
```

### 3.3

Style the submit button:

```css
button[type="submit"] {
  background-color: #2563eb;
  color: #ffffff;
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
}

button[type="submit"]:hover {
  background-color: #1d4ed8;
}
```

`button[type="submit"]` is an **attribute selector** — it targets buttons with a specific attribute value. `cursor: pointer` changes the cursor to a hand on hover, signalling the element is clickable.

### 3.4 — Challenge

Add a priority badge using the class you added in the HTML tutorial. Create three colour variants:

```css
.priority-high {
  background-color: #fee2e2;
  color: #991b1b;
  padding: 0.125rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.priority-medium {
  background-color: #fef9c3;
  color: #854d0e;
  /* same padding, border-radius, font-size, font-weight */
}

.priority-low {
  background-color: #dcfce7;
  color: #166534;
}
```

Add `class="priority-high"` (or `medium` / `low`) to the priority text in each task card. Then extract the shared properties into a single `.priority-badge` class and use two classes on each element: `class="priority-badge priority-high"`.

## 4. Layout with Flexbox

Flexbox is a layout model for arranging elements in a row or column. It is the basis for most modern UI layouts — and every Tailwind layout utility (`flex`, `items-center`, `justify-between`, `gap-4`) maps directly to a Flexbox property.

### 4.1

Make the nav bar a horizontal row:

```css
nav {
  display: flex;
  gap: 1.5rem;          /* space between each link */
  align-items: center;  /* centre links vertically */
}
```

By default, elements stack vertically. `display: flex` switches the container to Flexbox mode and its direct children (`<a>` elements) become **flex items** arranged in a row.

### 4.2

Style the page header:

```css
header {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;  /* push children to opposite ends */
  align-items: center;
}
```

`justify-content` controls alignment along the **main axis** (horizontal by default). `space-between` pushes the first child to the left and the last to the right. Common values:

| Value | Behaviour |
|---|---|
| `flex-start` | pack to the start (default) |
| `flex-end` | pack to the end |
| `center` | centre all items |
| `space-between` | first at start, last at end, even gaps between |
| `space-around` | equal space on each side of each item |

### 4.3

Arrange the task cards in a grid of columns using Flexbox:

```css
.task-list {
  display: flex;
  flex-wrap: wrap;   /* allow items to wrap onto a new row */
  gap: 1rem;
}

.task-card {
  flex: 1 1 280px;   /* grow, shrink, base width of 280px */
}
```

`flex-wrap: wrap` lets items flow onto a second row rather than overflowing. `flex: 1 1 280px` means each card starts at 280px wide, can grow to fill space, and can shrink below 280px if needed. Resize the window — the number of columns adjusts automatically.

### 4.4

Arrange labels and inputs vertically inside a form:

```css
form {
  display: flex;
  flex-direction: column;  /* stack children vertically */
  gap: 0.75rem;
  max-width: 400px;
}

label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}
```

`flex-direction: column` changes the main axis to vertical. `gap` works the same way — it adds space between each form element.

### 4.5 — Challenge

Use `align-items` (the cross-axis property) to vertically centre content inside a card:

```css
.task-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}
```

Add a `<div class="task-card-footer">` to each task card containing a priority badge on the left and a Delete button on the right. The badge and button should be vertically centred relative to each other.

## 5. Putting It Together

### Final Exercise

Style the complete Task Manager page. By the end it should be clean and functional — not polished, but readable and well-structured.

**Requirements:**

**Global**
- `box-sizing: border-box` on everything
- System font stack on `body`
- Light gray page background

**Header**
- White background, bottom border
- Title on the left, nav links on the right (Flexbox)
- Nav links change colour on hover

**Form section**
- White card with padding, border, and rounded corners
- Inputs and textarea are full-width with padding and a border
- Input border changes colour on `:focus`
- Submit button is blue, lightens on hover

**Task cards**
- Arrange in a flex row that wraps
- Each card has a white background, border, rounded corners, and padding
- Task title is bold
- Priority badge uses colour variants from section 3.4
- Delete button is outlined (no fill), red on hover

**Verification:**
1. Open `index.html` in the browser
2. Open dev tools and select a `.task-card` — confirm the box model shows padding and border
3. Resize the window to a narrow width — confirm the cards wrap to a single column and the form stays readable
4. Focus an input with the keyboard (`Tab` key) — confirm the focus outline is visible
5. Hover over a nav link and the submit button — confirm the colour transitions work

This page is the starting point for the React tutorial — you will rebuild the same layout in React with Tailwind, and recognise every property because you wrote it here first.

## Checklist

- [ ] Can link a CSS file to an HTML document with `<link>`
- [ ] Can write rules using element, class, and id selectors
- [ ] Can combine selectors: descendant (`.parent .child`), group (`h2, h3`)
- [ ] Can use `:hover`, `:focus`, and `:nth-child` pseudo-classes
- [ ] Understand the box model: content, padding, border, margin
- [ ] Know why `box-sizing: border-box` is set globally
- [ ] Can use `width`, `max-width`, and `margin: 0 auto` to constrain and centre a block
- [ ] Can set a system font stack and control `font-size`, `font-weight`, `line-height`, `color`
- [ ] Can use `display: flex` to arrange items in a row or column
- [ ] Know what `justify-content` and `align-items` do and their common values
- [ ] Can use `flex-wrap` and `gap` to create a responsive card grid
- [ ] Can use `flex-direction: column` to stack form elements with even spacing
