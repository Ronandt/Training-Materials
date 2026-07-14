# React Frontend Exercises — Part 1: Setup, Styling & Routing

React is a JavaScript library for building user interfaces. This is part 1 of 2 for a Task Manager-style frontend — it gets a real, navigable, styled app running before you ever call an API. Part 2 (`react_api_tutorial.md`) picks up the same project and wires it to [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free public fake REST API — no backend of your own required.

**Slides:** [`why-react-slides.pdf`](why-react-slides.pdf) — read this first if you haven't touched React before. It picks up right where the DOM tutorial left off: why manual DOM code gets unwieldy, and what problem components/state/JSX actually solve.

**This part's stack:**
- **Vite** — build tool and dev server
- **React** — UI component model
- **Tailwind CSS** — utility-first styling
- **shadcn/ui** — pre-built accessible components
- **React Router** — client-side routing

Work through each section in order. Every exercise has something visible in your browser. Each section builds on the previous one.

**Prerequisite:** Node.js 18 or later. Check: `node --version`.

**References:**
- [Vite docs](https://vitejs.dev)
- [React docs](https://react.dev)
- [Tailwind CSS docs](https://tailwindcss.com/docs)
- [shadcn/ui docs](https://ui.shadcn.com)
- [React Router docs](https://reactrouter.com)

## 0. Setup

### 0.1

Scaffold a new Vite project with the React TypeScript template:

```bash
npm create vite@latest task-ui -- --template react-ts
cd task-ui
npm install
```

Start the dev server:

```bash
npm run dev
```

Open `http://localhost:5173`. You will see Vite's default React starter page. The server hot-reloads on every file save — leave it running throughout this tutorial.

### 0.2

Open the `task-ui` folder. The important files:

```
task-ui/
├── index.html          ← entry point — Vite injects the JS bundle here
├── vite.config.ts      ← build and plugin configuration
├── tsconfig.json       ← TypeScript configuration
├── src/
│   ├── main.tsx        ← mounts the React app into index.html
│   ├── App.tsx         ← root component (you will replace this)
│   └── index.css       ← global styles
└── public/             ← static files served as-is
```

In React, the entire UI is composed of **components** — TypeScript functions that return JSX (HTML-like syntax embedded in TypeScript). `App.tsx` is the root; everything else renders inside it.

Open `src/App.tsx` and replace the contents with:

```tsx
function App() {
  return <h1>Task Manager</h1>
}

export default App
```

Save. The browser updates instantly.

### 0.3

Install the routing dependency you'll use in section 3:

```bash
npm install react-router-dom
npm install -D @types/node
```

- `react-router-dom` — client-side routing
- `@types/node` — Node.js types needed for the path alias in section 2

You do not need to restart the dev server — Vite picks up new packages automatically after install. (You'll install `axios` and `@tanstack/react-query` at the start of part 2.)

## 1. Tailwind CSS

Tailwind is a utility-first CSS framework. Instead of writing CSS rules, you compose styles by combining small utility classes directly in your JSX: `className="flex items-center gap-4 p-6 text-gray-800"`. Each class maps to exactly one CSS rule.

### 1.1

Install Tailwind and its Vite plugin:

```bash
npm install tailwindcss @tailwindcss/vite
```

Open `vite.config.ts` and add the plugin:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
    react(),
  ],
})
```

Replace the entire contents of `src/index.css` with a single import:

```css
@import "tailwindcss";
```

Restart the dev server:

```bash
npm run dev
```

### 1.2

Replace `src/App.tsx` with a page that uses Tailwind classes:

```tsx
function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900">Task Manager</h1>
      <p className="mt-2 text-gray-500">Manage your tasks and users.</p>
    </div>
  )
}

export default App
```

`p-8` → `padding: 2rem`, `text-gray-900` → dark gray, `font-bold` → `font-weight: 700`. Look up any unfamiliar class in the [Tailwind docs](https://tailwindcss.com/docs) — the search is fast.

### 1.3

Tailwind exposes CSS Flexbox and Grid as utilities. Build a two-column card layout:

```tsx
function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Task Manager</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800">Users</h2>
          <p className="mt-1 text-gray-500">Manage team members.</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800">Tasks</h2>
          <p className="mt-1 text-gray-500">Track work items.</p>
        </div>
      </div>
    </div>
  )
}
```

`grid-cols-1 md:grid-cols-2` means: one column on small screens, two columns on `md` (768px) and wider. Resize the browser window to see the responsive breakpoint switch.



## 2. shadcn/ui

shadcn/ui is a collection of accessible, composable components built on Radix UI and Tailwind. Unlike most component libraries it copies component source directly into your project — you own the code and can modify it freely.

### 2.1

shadcn requires a `@/` path alias pointing to `src/`. Add it to `vite.config.ts`:

```typescript
import path from 'path'

export default defineConfig({
  plugins: [tailwindcss(), react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

Add the same alias to `tsconfig.json` under `compilerOptions`:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Restart the dev server after making these changes.

### 2.2

Run the shadcn initialiser:

```bash
npx shadcn@latest init
```

Accept the defaults when prompted. It writes `components.json` and `src/lib/utils.ts`. Open `utils.ts` — it exports a `cn()` helper that merges Tailwind classes correctly, handling conflicts like `p-2 p-4` resolving to `p-4`.

### 2.3

Install the components you will use throughout this project:

```bash
npx shadcn@latest add button card input badge select
```

Each component is copied into `src/components/ui/`. Open any one — it is plain TypeScript and Tailwind that you can read and edit.

Use `Button` in `App.tsx`:

```tsx
import { Button } from "@/components/ui/button"

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Task Manager</h1>
      <div className="flex gap-3">
        <Button>Default</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="destructive">Delete</Button>
      </div>
    </div>
  )
}
```

### 2.4

Replace the hand-rolled cards from section 1 with shadcn `Card` components:

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <Card>
    <CardHeader>
      <CardTitle>Users</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-gray-500">Manage team members.</p>
    </CardContent>
  </Card>
  <Card>
    <CardHeader>
      <CardTitle>Tasks</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-gray-500">Track work items.</p>
    </CardContent>
  </Card>
</div>
```

The shadcn card gives consistent spacing and border radius — the utility classes you wrote manually are now encapsulated inside the component.

### 2.5 — Challenge

Wire a shadcn `Input` to local state. React's `useState` hook stores component state — each call returns the current value and a setter function:

```tsx
import { useState } from "react"
import { Input } from "@/components/ui/input"

function SearchBox() {
  const [query, setQuery] = useState("")
  return (
    <div className="flex flex-col gap-2 max-w-sm">
      <Input
        placeholder="Search tasks..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <p className="text-sm text-gray-500">You typed: {query}</p>
    </div>
  )
}
```

`value` + `onChange` together make this a **controlled input** — React owns the value; the DOM only displays it. Render `SearchBox` in `App.tsx` and type into it.

## 3. React Router

React Router handles client-side navigation — users move between pages without a full browser reload, and the URL stays in sync with what is on screen.

### 3.1

Wrap your app in `BrowserRouter` in `src/main.tsx`:

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

### 3.2

Create a `src/pages/` folder with three placeholder page components:

```tsx
// src/pages/HomePage.tsx
export default function HomePage() {
  return <h2 className="text-2xl font-bold">Home</h2>
}
```

```tsx
// src/pages/UsersPage.tsx
export default function UsersPage() {
  return <h2 className="text-2xl font-bold">Users</h2>
}
```

```tsx
// src/pages/TasksPage.tsx
export default function TasksPage() {
  return <h2 className="text-2xl font-bold">Tasks</h2>
}
```

Replace `src/App.tsx` with route declarations:

```tsx
import { Routes, Route } from 'react-router-dom'
import HomePage from '@/pages/HomePage'
import UsersPage from '@/pages/UsersPage'
import TasksPage from '@/pages/TasksPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/tasks" element={<TasksPage />} />
    </Routes>
  )
}

export default App
```

Visit `http://localhost:5173/users` directly — you should see the Users heading. React Router matched the URL and rendered the right component.

### 3.3

A **layout route** wraps all pages with a shared header and navigation. Create `src/components/Layout.tsx`:

```tsx
import { NavLink, Outlet } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-6">
        <span className="font-bold text-lg text-gray-900">Task Manager</span>
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? "text-gray-900 font-semibold" : "text-gray-500 hover:text-gray-900 transition-colors"
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/users"
          className={({ isActive }) =>
            isActive ? "text-gray-900 font-semibold" : "text-gray-500 hover:text-gray-900 transition-colors"
          }
        >
          Users
        </NavLink>
        <NavLink
          to="/tasks"
          className={({ isActive }) =>
            isActive ? "text-gray-900 font-semibold" : "text-gray-500 hover:text-gray-900 transition-colors"
          }
        >
          Tasks
        </NavLink>
      </nav>
      <main className="p-8">
        <Outlet />
      </main>
    </div>
  )
}
```

`<Outlet />` is where child routes render. `<NavLink>` automatically receives `isActive` — use it to highlight the current page. The `end` prop on the Home link prevents it matching every route that starts with `/`.

Update `App.tsx` to nest all pages inside the layout:

```tsx
import { Routes, Route } from 'react-router-dom'
import Layout from '@/components/Layout'
import HomePage from '@/pages/HomePage'
import UsersPage from '@/pages/UsersPage'
import TasksPage from '@/pages/TasksPage'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/tasks" element={<TasksPage />} />
      </Route>
    </Routes>
  )
}

export default App
```

Navigate between pages using the nav links. The URL changes but there is no page flash — React Router handles it client-side.

### 3.4

Add a task detail page with a dynamic route. Create `src/pages/TaskDetailPage.tsx`:

```tsx
import { useParams } from 'react-router-dom'

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>()
  return <h2 className="text-2xl font-bold">Task #{id}</h2>
}
```

Register it in `App.tsx` inside the layout:

```tsx
import TaskDetailPage from '@/pages/TaskDetailPage'

<Route path="/tasks/:id" element={<TaskDetailPage />} />
```

Visit `http://localhost:5173/tasks/42` — the page shows `Task #42`. The `:id` segment is dynamic; `useParams` captures it.

### 3.5 — Challenge

Add a 404 page. React Router's catch-all route uses `path="*"`:

```tsx
// src/pages/NotFoundPage.tsx
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center gap-4 mt-16">
      <h2 className="text-2xl font-bold text-gray-900">Page not found</h2>
      <Button asChild variant="outline">
        <Link to="/">Go home</Link>
      </Button>
    </div>
  )
}
```

Add `<Route path="*" element={<NotFoundPage />} />` inside the layout in `App.tsx`. Visit any unknown URL — confirm the 404 page appears with working navigation.

## Checklist

- [ ] Can scaffold a Vite + React + TypeScript project and run the dev server
- [ ] Can install and configure Tailwind CSS using `@tailwindcss/vite`
- [ ] Can use utility classes for layout, spacing, colour, and responsive breakpoints
- [ ] Understand why dynamic Tailwind class names must be full strings
- [ ] Can initialise shadcn/ui and add components to the project
- [ ] Understand that shadcn copies source into your project — you own the code
- [ ] Can set up `BrowserRouter`, `Routes`, and `Route` in React Router
- [ ] Can create a layout route with `<Outlet />` for shared navigation
- [ ] Can use `<NavLink>` with `isActive` for active link highlighting
- [ ] Can use `useParams` to read dynamic route segments
- [ ] Have a navigable, styled app with placeholder pages — ready to connect to a real API in part 2

**Next:** `react_api_tutorial.md` picks up this exact project and connects it to a public API.
