# React Frontend Exercises

React is a JavaScript library for building user interfaces. This tutorial builds a frontend for the Task Manager API from the backend tutorials — a working web app with user management, task tracking, and live API calls.

The stack you will assemble in a single project:
- **Vite** — build tool and dev server
- **React** — UI component model
- **Tailwind CSS** — utility-first styling
- **shadcn/ui** — pre-built accessible components
- **React Router** — client-side routing
- **Axios** — HTTP client for API calls
- **TanStack Query** — server state management

Work through each section in order. Every exercise has something visible in your browser. Each section builds on the previous one — by the end everything is wired together.

**This tutorial connects to the backend track.** Your FastAPI + SQLAlchemy API must be running on `http://localhost:8000`. Start it before section 4.

**Track order:**
- **FastAPI tutorial:** Task Manager API ✓
- **Pydantic tutorial:** Production-quality schemas ✓
- **SQLAlchemy tutorial:** Real database ✓
- **React (this file):** Frontend UI

**Prerequisite:** Node.js 18 or later. Check: `node --version`.

**References:**
- [Vite docs](https://vitejs.dev)
- [React docs](https://react.dev)
- [Tailwind CSS docs](https://tailwindcss.com/docs)
- [shadcn/ui docs](https://ui.shadcn.com)
- [React Router docs](https://reactrouter.com)
- [Axios docs](https://axios-http.com)
- [TanStack Query docs](https://tanstack.com/query/latest)

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

Install the remaining dependencies you will use across this tutorial:

```bash
npm install react-router-dom axios @tanstack/react-query
npm install -D @types/node
```

- `react-router-dom` — client-side routing
- `axios` — HTTP client
- `@tanstack/react-query` — server state management
- `@types/node` — Node.js types needed for the path alias in section 2

You do not need to restart the dev server — Vite picks up new packages automatically after install.

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

### 1.4 — Challenge

Build a `StatusBadge` component that shows different colours for different task statuses. Dynamic class names must use the full string — Tailwind cannot detect `text-${colour}-700` at build time and will not include those classes in the output:

```tsx
function StatusBadge({ status }: { status: string }) {
  const colours: Record<string, string> = {
    todo: "bg-gray-100 text-gray-700",
    "in-progress": "bg-blue-100 text-blue-700",
    done: "bg-green-100 text-green-700",
  }
  return (
    <span className={`inline-block rounded-full px-3 py-1 text-sm font-medium ${colours[status] ?? "bg-gray-100 text-gray-700"}`}>
      {status}
    </span>
  )
}
```

Render three instances with statuses `"todo"`, `"in-progress"`, and `"done"` in `App.tsx` and confirm each has a different colour.

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

Install the components you will use throughout this tutorial:

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

## 4. Axios

Axios is an HTTP client for making API requests from the browser. It handles JSON serialisation, status code errors, and request configuration in one place.

### 4.1

Create a central API client at `src/lib/api.ts`. All requests go through this instance — base URL and headers are configured once:

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
```

### 4.2

Create `src/types/api.ts` to define the shapes your backend returns. These mirror the Pydantic response models in your FastAPI backend:

```typescript
export interface User {
  id: number
  name: string
  email: string
}

export interface Task {
  id: number
  title: string
  description: string | null
  priority: string
  status: string
  owner_id: number
}

export interface UserCreate {
  name: string
  email: string
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: string
  owner_id: number
}

export interface TaskUpdate {
  title?: string
  status?: string
  priority?: string
  description?: string
}
```

### 4.3

Requests from `localhost:5173` to `localhost:8000` are cross-origin — the browser blocks them unless the API explicitly allows it. Add CORS middleware to your FastAPI `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Add this immediately after `app = FastAPI()`. Restart the FastAPI server.

### 4.4

React's `useEffect` hook runs side effects — like API calls — after a component renders. The pattern for fetching data on mount:

```tsx
import { useEffect, useState } from 'react'
import api from '@/lib/api'
import { User } from '@/types/api'

function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.get<User[]>('/users')
      .then(res => setUsers(res.data))
      .catch(() => setError('Failed to load users'))
      .finally(() => setLoading(false))
  }, []) // empty array → run once when the component mounts

  if (loading) return <p className="text-gray-500">Loading...</p>
  if (error) return <p className="text-red-500">{error}</p>
  return (
    <ul className="space-y-1">
      {users.map(u => (
        <li key={u.id} className="text-gray-700">{u.name} — {u.email}</li>
      ))}
    </ul>
  )
}
```

Add `UserList` to `UsersPage.tsx` and navigate to `/users`. Make sure the FastAPI server is running — you should see your existing users or an empty list.

### 4.5

Sending data uses `api.post()`. Build a create-user form:

```tsx
import { useState } from 'react'
import { AxiosError } from 'axios'
import api from '@/lib/api'
import { User } from '@/types/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

function CreateUserForm({ onCreated }: { onCreated: (user: User) => void }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const res = await api.post<User>('/users', { name, email })
      onCreated(res.data)
      setName('')
      setEmail('')
    } catch (err) {
      const axiosErr = err as AxiosError<{ detail: string }>
      if (axiosErr.response?.status === 409) {
        setError('That email is already registered.')
      } else {
        setError('Something went wrong. Please try again.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-sm">
      <Input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
      <Input placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
      {error && <p className="text-sm text-red-500">{error}</p>}
      <Button type="submit" disabled={submitting}>
        {submitting ? 'Creating...' : 'Create User'}
      </Button>
    </form>
  )
}
```

`e.preventDefault()` stops the browser from doing a full-page form submission. `onCreated` is a callback prop — the parent component decides what to do with the new user (typically: append it to the list). Add this form to `UsersPage.tsx` and test it: create a user, then try the same email twice.

### 4.6 — Challenge

Add a `PATCH /tasks/:id` call using `api.patch()`. Write a standalone `updateTaskStatus` function in a new file `src/lib/tasks.ts`:

```typescript
import api from './api'
import { Task, TaskUpdate } from '@/types/api'

export async function updateTaskStatus(id: number, status: string): Promise<Task> {
  const res = await api.patch<Task>(`/tasks/${id}`, { status } satisfies TaskUpdate)
  return res.data
}
```

Import and call it from `TaskDetailPage.tsx` (you will use it fully in section 5). Confirm the call succeeds by checking the FastAPI terminal for the PATCH log line.

## 5. TanStack Query

TanStack Query manages **server state** — data that lives in your API rather than in your component. It replaces the `useEffect` + `useState` fetching pattern from section 4 with a cache that handles loading, errors, background refetching, and cache invalidation automatically.

The key shift in thinking: instead of asking "how do I fetch data and store it locally?", you ask "what data do I need, and what is its cache key?"

### 5.1

Wrap your app in `QueryClientProvider` in `src/main.tsx`. The `QueryClient` holds the shared cache — all components in the tree read from and write to the same cache:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.tsx'

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
)
```

### 5.2

`useQuery` fetches data and manages loading and error state automatically. Compare the two approaches for the user list:

**Before (section 4.4) — manual state:**
```tsx
const [users, setUsers] = useState<User[]>([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)

useEffect(() => {
  api.get<User[]>('/users')
    .then(res => setUsers(res.data))
    .catch(() => setError('Failed to load users'))
    .finally(() => setLoading(false))
}, [])
```

**After — useQuery:**
```tsx
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { User } from '@/types/api'

const { data: users = [], isLoading, isError } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.get<User[]>('/users').then(res => res.data),
})
```

- `queryKey` — a unique identifier for this query in the cache; `['users']` means "the list of all users"
- `queryFn` — an async function that returns the data; if it throws, `isError` becomes `true`
- `data`, `isLoading`, `isError` — derived automatically; no `useState` needed
- `= []` default — the type of `data` is `User[] | undefined` until the first fetch resolves; the default prevents null checks in the render

Update `UsersPage.tsx` to use `useQuery` for the user list. Remove the three manual state variables and the `useEffect`, and replace with the single `useQuery` call.

### 5.3

Query keys with variables give each combination its own cache entry. When the variable changes, TanStack Query automatically runs a new fetch — you no longer need a `useEffect` dependency array:

```tsx
const { data: tasks = [], isLoading } = useQuery({
  queryKey: ['tasks', statusFilter],
  queryFn: () => {
    const params = statusFilter !== 'all' ? { status: statusFilter } : {}
    return api.get<Task[]>('/tasks', { params }).then(res => res.data)
  },
})
```

- `['tasks', 'all']`, `['tasks', 'in-progress']`, `['tasks', 'done']` are three separate cache entries
- Switching the filter hits a cached result instantly if you have visited that filter before — no spinner on the second visit
- The cache entries stay fresh for 5 minutes by default (`staleTime` is configurable)

Update `TasksPage.tsx` to use this pattern. Remove both `useEffect` calls and the `loading` / `tasks` / `users` `useState` calls — replace them with two `useQuery` calls.

### 5.4

`useMutation` handles writes — POST, PATCH, DELETE. After a successful mutation, call `invalidateQueries` to mark cached data as stale so it re-fetches:

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { AxiosError } from 'axios'

const queryClient = useQueryClient()

const createUser = useMutation({
  mutationFn: (data: { name: string; email: string }) =>
    api.post<User>('/users', data).then(res => res.data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] })
  },
})

// In the form submit handler:
async function handleCreate(e: React.FormEvent) {
  e.preventDefault()
  try {
    await createUser.mutateAsync({ name, email })
    setName('')
    setEmail('')
  } catch (err) {
    // createUser.error holds the thrown value
  }
}
```

- `onSuccess` — runs after `mutationFn` resolves; invalidating `['users']` causes every component using `useQuery({ queryKey: ['users'] })` to re-fetch
- `createUser.isPending` — `true` while the request is in flight; replaces the manual `submitting` state
- `createUser.error` — the thrown error, if any; cast it to `AxiosError` to check the status code
- `mutateAsync` — returns a promise; use `await` inside a try/catch to handle errors inline

Rewrite the create-user form submission in `UsersPage.tsx` to use `useMutation`. Replace the `submitting` state with `createUser.isPending`.

### 5.5 — Challenge

`setQueryData` updates a cache entry directly without making a network request — useful when the API already returns the full updated object:

```tsx
const updateStatus = useMutation({
  mutationFn: (status: string) =>
    api.patch<Task>(`/tasks/${id}`, { status }).then(res => res.data),
  onSuccess: (updatedTask) => {
    // write the updated task directly into the ['tasks', id] cache entry
    queryClient.setQueryData(['tasks', id], updatedTask)
    // also invalidate the list so it reflects the change next time it loads
    queryClient.invalidateQueries({ queryKey: ['tasks'] })
  },
})
```

Rewrite `TaskDetailPage.tsx` to use:
- `useQuery({ queryKey: ['tasks', id] })` for the initial fetch
- `useMutation` with `setQueryData` for the status update
- `useMutation` with `invalidateQueries` + `navigate` for delete

Compare the line count to the `useEffect` version from section 5.3 — the component has far less manual state management.

## 6. Putting It Together

Now connect all five layers — Tailwind layout, shadcn components, React Router pages, Axios, and TanStack Query — into complete, working pages.

### 6.1

Replace `src/pages/UsersPage.tsx` with a full implementation using TanStack Query:

```tsx
import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { AxiosError } from 'axios'
import api from '@/lib/api'
import { User } from '@/types/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function UsersPage() {
  const queryClient = useQueryClient()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [formError, setFormError] = useState<string | null>(null)

  const { data: users = [], isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.get<User[]>('/users').then(res => res.data),
  })

  const createUser = useMutation({
    mutationFn: (data: { name: string; email: string }) =>
      api.post<User>('/users', data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    setFormError(null)
    try {
      await createUser.mutateAsync({ name, email })
      setName('')
      setEmail('')
    } catch (err) {
      const axiosErr = err as AxiosError<{ detail: string }>
      setFormError(
        axiosErr.response?.status === 409
          ? 'Email already registered.'
          : 'Failed to create user.'
      )
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Users</h1>

      <Card className="max-w-sm">
        <CardHeader><CardTitle>New User</CardTitle></CardHeader>
        <CardContent>
          <form onSubmit={handleCreate} className="flex flex-col gap-3">
            <Input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
            <Input placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
            {formError && <p className="text-sm text-red-500">{formError}</p>}
            <Button type="submit" disabled={createUser.isPending}>
              {createUser.isPending ? 'Creating...' : 'Create User'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {users.map(user => (
            <Card key={user.id}>
              <CardHeader><CardTitle className="text-base">{user.name}</CardTitle></CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500">{user.email}</p>
              </CardContent>
            </Card>
          ))}
          {users.length === 0 && (
            <p className="text-gray-500">No users yet.</p>
          )}
        </div>
      )}
    </div>
  )
}
```

Create two users. After `mutateAsync` resolves, `invalidateQueries` marks the `['users']` cache as stale — TanStack Query re-fetches in the background and the grid updates automatically. No manual `setUsers` needed.

### 6.2

Replace `src/pages/TasksPage.tsx`. Two `useQuery` calls replace the two `useEffect` calls — one for users, one for tasks with the filter baked into the key:

```tsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Task, User, TaskCreate } from '@/types/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select'

export default function TasksPage() {
  const queryClient = useQueryClient()
  const [statusFilter, setStatusFilter] = useState('all')
  const [form, setForm] = useState<TaskCreate>({ title: '', owner_id: 0 })

  const { data: users = [] } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.get<User[]>('/users').then(res => res.data),
  })

  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ['tasks', statusFilter],
    queryFn: () => {
      const params = statusFilter !== 'all' ? { status: statusFilter } : {}
      return api.get<Task[]>('/tasks', { params }).then(res => res.data)
    },
  })

  const createTask = useMutation({
    mutationFn: (data: TaskCreate) => api.post<Task>('/tasks', data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    await createTask.mutateAsync(form)
    setForm({ title: '', owner_id: 0 })
  }

  const badgeVariant = (status: string) =>
    ({ todo: 'secondary', 'in-progress': 'default', done: 'outline' } as Record<string, any>)[status] ?? 'secondary'

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="todo">Todo</SelectItem>
            <SelectItem value="in-progress">In Progress</SelectItem>
            <SelectItem value="done">Done</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Card className="max-w-sm">
        <CardHeader><CardTitle>New Task</CardTitle></CardHeader>
        <CardContent>
          <form onSubmit={handleCreate} className="flex flex-col gap-3">
            <Input
              placeholder="Title"
              value={form.title}
              onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
              required
            />
            <Select
              value={form.owner_id ? String(form.owner_id) : ''}
              onValueChange={v => setForm(f => ({ ...f, owner_id: Number(v) }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Assign to..." />
              </SelectTrigger>
              <SelectContent>
                {users.map(u => (
                  <SelectItem key={u.id} value={String(u.id)}>{u.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button type="submit" disabled={createTask.isPending || !form.owner_id}>
              {createTask.isPending ? 'Creating...' : 'Create Task'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tasks.map(task => (
            <Link to={`/tasks/${task.id}`} key={task.id}>
              <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
                <CardHeader>
                  <CardTitle className="text-base">{task.title}</CardTitle>
                </CardHeader>
                <CardContent className="flex items-center gap-2">
                  <Badge variant={badgeVariant(task.status)}>{task.status}</Badge>
                  <span className="text-sm text-gray-500">{task.priority}</span>
                </CardContent>
              </Card>
            </Link>
          ))}
          {tasks.length === 0 && (
            <p className="text-gray-500 col-span-3">No tasks found.</p>
          )}
        </div>
      )}
    </div>
  )
}
```

When `statusFilter` changes, TanStack Query looks for `['tasks', 'in-progress']` in the cache. If it exists (you have visited that filter before), the cached data renders instantly — no spinner — while a background refetch runs silently.

### 6.3

Replace `src/pages/TaskDetailPage.tsx`. `useQuery` fetches the task; two `useMutation` calls handle the status update and delete:

```tsx
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Task } from '@/types/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select'

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: task, isLoading, isError } = useQuery({
    queryKey: ['tasks', id],
    queryFn: () => api.get<Task>(`/tasks/${id}`).then(res => res.data),
    retry: (failureCount, error: any) => error?.response?.status !== 404,
  })

  const updateStatus = useMutation({
    mutationFn: (status: string) =>
      api.patch<Task>(`/tasks/${id}`, { status }).then(res => res.data),
    onSuccess: (updated) => {
      queryClient.setQueryData(['tasks', id], updated)
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteTask = useMutation({
    mutationFn: () => api.delete(`/tasks/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      navigate('/tasks')
    },
  })

  if (isLoading) return <p className="text-gray-500">Loading...</p>
  if (isError) return <p className="text-red-500">Task not found.</p>
  if (!task) return null

  return (
    <div className="max-w-lg space-y-4">
      <Button variant="outline" onClick={() => navigate('/tasks')}>← Back</Button>

      <Card>
        <CardHeader>
          <CardTitle>{task.title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {task.description && (
            <p className="text-gray-600">{task.description}</p>
          )}

          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-gray-700">Status:</span>
            <Select value={task.status} onValueChange={s => updateStatus.mutate(s)} disabled={updateStatus.isPending}>
              <SelectTrigger className="w-36">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="todo">Todo</SelectItem>
                <SelectItem value="in-progress">In Progress</SelectItem>
                <SelectItem value="done">Done</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">Priority:</span>
            <Badge variant="outline">{task.priority}</Badge>
          </div>

          <Button
            variant="destructive"
            onClick={() => deleteTask.mutate()}
            disabled={deleteTask.isPending}
            className="w-full"
          >
            {deleteTask.isPending ? 'Deleting...' : 'Delete Task'}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
```

`retry` is configured to not retry on 404 — by default TanStack Query retries failed queries three times, which would show a spinner for 3 × delay before the "Task not found" message appeared. `setQueryData` writes the patched task directly into the `['tasks', id]` cache entry so the status Select updates instantly, while `invalidateQueries` on the list key means the tasks page will re-fetch next time it mounts.

### 6.4

Update `src/pages/HomePage.tsx`. Two `useQuery` calls run in parallel — TanStack Query fires both requests simultaneously without needing `Promise.all`:

```tsx
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { User, Task } from '@/types/api'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function HomePage() {
  const { data: users = [] } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.get<User[]>('/users').then(res => res.data),
  })

  const { data: tasks = [], isLoading } = useQuery({
    queryKey: ['tasks', 'all'],
    queryFn: () => api.get<Task[]>('/tasks').then(res => res.data),
  })

  const byStatus = (status: string) => tasks.filter(t => t.status === status).length

  if (isLoading) return <p className="text-gray-500">Loading...</p>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Link to="/users">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader><CardTitle className="text-sm text-gray-500">Users</CardTitle></CardHeader>
            <CardContent><p className="text-3xl font-bold">{users.length}</p></CardContent>
          </Card>
        </Link>
        <Link to="/tasks">
          <Card className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader><CardTitle className="text-sm text-gray-500">Total Tasks</CardTitle></CardHeader>
            <CardContent><p className="text-3xl font-bold">{tasks.length}</p></CardContent>
          </Card>
        </Link>
        <Card>
          <CardHeader><CardTitle className="text-sm text-gray-500">In Progress</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-blue-600">{byStatus('in-progress')}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm text-gray-500">Done</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-green-600">{byStatus('done')}</p></CardContent>
        </Card>
      </div>
    </div>
  )
}
```

Because `['users']` is the same key used in `UsersPage`, navigating to the dashboard after visiting Users shows the count instantly from cache — no second network request. Navigate to `/` — you should see live counts. Click the Users or Tasks card to navigate to that page.

### 6.5 — Challenge

Add **optimistic updates** to the task delete. TanStack Query has first-class support for optimistic updates — cancel any in-flight refetch, snapshot the current cache, remove the item immediately, and roll back if the request fails:

```typescript
const deleteTask = useMutation({
  mutationFn: () => api.delete(`/tasks/${id}`),
  onMutate: async () => {
    // cancel in-flight refetches so they don't overwrite the optimistic removal
    await queryClient.cancelQueries({ queryKey: ['tasks'] })
    // snapshot current list for rollback
    const previous = queryClient.getQueryData<Task[]>(['tasks', 'all'])
    // remove the task from the list cache immediately
    queryClient.setQueryData<Task[]>(['tasks', 'all'], old =>
      old?.filter(t => t.id !== Number(id)) ?? []
    )
    return { previous }
  },
  onError: (_err, _vars, context) => {
    // something went wrong — put the old list back
    if (context?.previous) {
      queryClient.setQueryData(['tasks', 'all'], context.previous)
    }
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks'] })
    navigate('/tasks')
  },
})
```

`onMutate` runs synchronously before the network request. `onError` receives the snapshot from `onMutate`'s return value via `context`. `onSettled` runs whether the mutation succeeded or failed — a safe place to re-sync with the server.

## 7. Putting It Together

### Final Exercise

Complete `task-ui` as a fully working frontend for the Task Manager API.

**Requirements:**

**Users page** (`/users`):
- Lists all users in a card grid
- Create form with name and email fields
- Shows a 409 error message if the email is already taken
- New user appears in the grid immediately on creation

**Tasks page** (`/tasks`):
- Lists tasks as clickable cards
- Status filter dropdown re-fetches from the API when changed
- Create form with title and owner selector (populated from `/users`)
- New task appears in the grid immediately on creation

**Task detail page** (`/tasks/:id`):
- Loads the task by id
- Status dropdown saves to the API immediately on change
- Delete button removes the task and redirects to `/tasks`
- Shows "Task not found." for non-existent ids

**Navigation:**
- Persistent nav bar with active link highlighting
- Back button on the task detail page
- 404 page for unknown routes

**Verification — run through this in your browser:**

1. Open the home page — confirm the dashboard counts are accurate
2. Create two users — confirm both appear in the grid immediately
3. Try creating a duplicate email — confirm the error message
4. Create three tasks with different statuses and owners
5. On the tasks page, filter by `in-progress` — confirm only matching tasks show
6. Click a task card — confirm the detail page loads correctly
7. Change the status on the detail page — refresh the page and confirm the change persisted
8. Delete a task — confirm redirect to `/tasks` and the task is gone
9. Visit `/tasks/99999` — confirm "Task not found." appears
10. Visit `/doesnotexist` — confirm the 404 page appears

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
- [ ] Can use `useNavigate` for programmatic navigation
- [ ] Can create an Axios instance with a base URL
- [ ] Understand what CORS is and how to enable it in FastAPI
- [ ] Can fetch data in `useEffect` and store it with `useState`
- [ ] Understand the `useEffect` dependency array and how it controls re-runs
- [ ] Can send POST and PATCH requests and update local state with the response
- [ ] Can handle Axios errors and show user-facing messages for specific status codes
- [ ] Can set up `QueryClient` and `QueryClientProvider` in `main.tsx`
- [ ] Can replace a `useEffect` fetch with `useQuery`, understanding `queryKey`, `queryFn`, `data`, `isLoading`, `isError`
- [ ] Understand how variable query keys (`['tasks', statusFilter]`) give each value its own cache entry
- [ ] Can use `useMutation` with `mutationFn`, `onSuccess`, and `isPending`
- [ ] Know the difference between `invalidateQueries` (re-fetch from server) and `setQueryData` (write to cache directly)
- [ ] Can configure `retry` to skip retries on specific HTTP status codes
- [ ] Understand the optimistic update pattern: `onMutate` snapshot → optimistic write → `onError` rollback
- [ ] All pages in the final exercise work end-to-end against the FastAPI backend
