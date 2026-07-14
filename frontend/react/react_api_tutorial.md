# React Frontend Exercises — Part 2: Connecting to a Public API

This is part 2 of 2. Part 1 (`react_styling_tutorial.md`) got you a navigable, styled `task-ui` app with placeholder pages. This part wires that same app up to [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — a free, fake REST API with no auth and no setup, widely used for exactly this kind of practice — using Axios and TanStack Query.

**This part's stack:**
- **Axios** — HTTP client for API calls
- **TanStack Query** — server state management

**One important quirk of JSONPlaceholder:** it accepts `POST`/`PATCH`/`DELETE` requests and returns a plausible response, but it doesn't actually persist anything server-side. Refresh the page and the data is back to its original state. This isn't a bug in your code — it's how the fake API works, and it's a good excuse to see clearly what TanStack Query's cache is doing for you: your UI updates instantly and correctly *within the session* because the cache is updated locally, even though the "server" never really remembers the write.

**A structural note:** it's tempting to write a page component that fetches data, manages form state, and renders everything itself — section 1 starts that way on purpose, so you feel the problem. From section 2 onward, every exercise builds in one of three places, and pages stop growing:

```
src/
  hooks/       ← data: useQuery / useMutation calls, nothing else
  components/  ← presentation: props in, JSX out, no data fetching
  pages/       ← composition: calls a hook, passes the result to a component
```

**References:**
- [Axios docs](https://axios-http.com)
- [TanStack Query docs](https://tanstack.com/query/latest)
- [JSONPlaceholder docs](https://jsonplaceholder.typicode.com/)

## 0. Setup

Install the two dependencies this part needs, in your existing `task-ui` project:

```bash
npm install axios @tanstack/react-query
```

## 1. Axios

Axios is an HTTP client for making API requests from the browser. It handles JSON serialisation, status code errors, and request configuration in one place.

### 1.1

Create a central API client at `src/lib/api.ts`. All requests go through this instance — base URL and headers are configured once:

```typescript
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
```

JSONPlaceholder already allows cross-origin requests from any page, so — unlike a self-hosted API — there's no CORS configuration step needed here.

### 1.2

Create `src/types/api.ts` to define the shapes this API returns. JSONPlaceholder's `/users` and `/todos` endpoints give you exactly two types to model:

```typescript
export interface User {
  id: number
  name: string
  email: string
}

export interface Todo {
  id: number
  userId: number
  title: string
  completed: boolean
}
```

For creating a new one, TypeScript's built-in `Omit<Todo, 'id'>` gives you exactly the "no id yet" shape without a hand-written `TodoCreate` interface — the server assigns the id. For partial updates, `Partial<Todo>` makes every field optional, covering what a hand-written `TodoUpdate` interface would otherwise do.

### 1.3

React's `useEffect` hook runs side effects — like API calls — after a component renders. The pattern for fetching data on mount, written directly inside a page component for now:

```tsx
// src/pages/UsersPage.tsx
import { useEffect, useState } from 'react'
import api from '@/lib/api'
import { User } from '@/types/api'

export default function UsersPage() {
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

Navigate to `/users` — you should see JSONPlaceholder's ten sample users.

Sit with this for a second: three `useState` calls and a `useEffect` just to display a list. Section 2 replaces all four with one line — that's the motivation for what's coming, not a mistake to fix yet.

### 1.4

Sending data uses `api.post()`. Still inline, for now — build a create-todo form directly in the page:

```tsx
import { useState } from 'react'
import api from '@/lib/api'
import { Todo } from '@/types/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

function CreateTodoForm({ onCreated }: { onCreated: (todo: Todo) => void }) {
  const [title, setTitle] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSubmitting(true)
    try {
      const res = await api.post<Todo>('/todos', { title, completed: false, userId: 1 })
      onCreated(res.data)
      setTitle('')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-sm">
      <Input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} required />
      <Button type="submit" disabled={submitting}>
        {submitting ? 'Creating...' : 'Create Todo'}
      </Button>
    </form>
  )
}
```

`e.preventDefault()` stops the browser from doing a full-page form submission. `onCreated` is a callback prop — the parent component decides what to do with the new todo (typically: append it to the list). Add this form to `TasksPage.tsx` and test it: create a todo and confirm the response comes back with a fake `id` (JSONPlaceholder always returns `id: 201` for a new todo — that's expected, and won't actually be retrievable afterwards).

### 1.5 — Challenge

Add a `PATCH /todos/:id` call using `api.patch()`. Write a standalone `updateTodoStatus` function in a new file `src/lib/todos.ts`, typed with `Partial<Todo>`:

```typescript
import api from './api'
import { Todo } from '@/types/api'

export async function updateTodoStatus(id: number, completed: boolean): Promise<Todo> {
  const res = await api.patch<Todo>(`/todos/${id}`, { completed } satisfies Partial<Todo>)
  return res.data
}
```

Import and call it from `TaskDetailPage.tsx` (you will use it fully in section 2). Confirm the call succeeds and returns the object you sent — then refresh the page and notice the change is gone, since JSONPlaceholder didn't really save it.

## 2. TanStack Query

TanStack Query manages **server state** — data that lives in your API rather than in your component. It replaces the `useEffect` + `useState` fetching pattern from section 1 with a cache that handles loading, errors, background refetching, and cache invalidation automatically.

The key shift in thinking: instead of asking "how do I fetch data and store it locally?", you ask "what data do I need, and what is its cache key?" — and because the query itself becomes a one-line function call, it can live in its own file instead of bloating a page. From here on, every query and mutation you write goes in `src/hooks/`, not inside a page component.

### 2.1

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

### 2.2

`useQuery` fetches data and manages loading and error state automatically. Instead of writing it inside `UsersPage.tsx`, put it in its own hook file:

```typescript
// src/hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { User } from '@/types/api'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.get<User[]>('/users').then(res => res.data),
  })
}
```

- `queryKey` — a unique identifier for this query in the cache; `['users']` means "the list of all users"
- `queryFn` — an async function that returns the data; if it throws, `isError` becomes `true`

Now `UsersPage.tsx` shrinks to:

```tsx
import { useUsers } from '@/hooks/useUsers'

export default function UsersPage() {
  const { data: users = [], isLoading, isError } = useUsers()

  if (isLoading) return <p className="text-gray-500">Loading...</p>
  if (isError) return <p className="text-red-500">Failed to load users.</p>
  return (
    <ul className="space-y-1">
      {users.map(u => (
        <li key={u.id} className="text-gray-700">{u.name} — {u.email}</li>
      ))}
    </ul>
  )
}
```

Compare this to 1.3: the three `useState` calls and the `useEffect` are gone, replaced by one hook call. Delete the old inline version and confirm `/users` still works.

### 2.3

Query keys with variables give each combination its own cache entry. When the variable changes, TanStack Query automatically runs a new fetch — you no longer need a `useEffect` dependency array. JSONPlaceholder supports `?userId=` filtering on `/todos`, so use that as the variable:

```typescript
// src/hooks/useTodos.ts
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Todo } from '@/types/api'

export function useTodos(userId: number | 'all') {
  return useQuery({
    queryKey: ['todos', userId],
    queryFn: () => {
      const params = userId !== 'all' ? { userId } : {}
      return api.get<Todo[]>('/todos', { params }).then(res => res.data)
    },
  })
}
```

- `['todos', 'all']`, `['todos', 1]`, `['todos', 2]` are separate cache entries
- Switching users hits a cached result instantly if you've viewed that user before — no spinner on the second visit

Also add a single-todo hook for the detail page:

```typescript
// src/hooks/useTodo.ts
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Todo } from '@/types/api'

export function useTodo(id: string) {
  return useQuery({
    queryKey: ['todos', id],
    queryFn: () => api.get<Todo>(`/todos/${id}`).then(res => res.data),
    retry: (failureCount, error: any) => error?.response?.status !== 404,
  })
}
```

`retry` is configured to not retry on 404 — by default TanStack Query retries failed queries three times, which would show a spinner for 3× the delay before a "not found" message could appear. JSONPlaceholder only has todos with ids 1–200, so anything outside that range is a real 404 to test against.

### 2.4

`useMutation` handles writes — POST, PATCH, DELETE. Each one gets its own hook file too. After a successful mutation, call `invalidateQueries` to mark cached data as stale so it re-fetches:

```typescript
// src/hooks/useCreateTodo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Todo } from '@/types/api'

export function useCreateTodo() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: Omit<Todo, 'id'>) =>
      api.post<Todo>('/todos', data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}
```

- `Omit<Todo, 'id'>` — the input shape for creating a todo: everything except `id`, which the caller shouldn't need to think about
- `onSuccess` — runs after `mutationFn` resolves; invalidating `['todos']` causes every component using `useTodos(...)` to re-fetch. Since JSONPlaceholder doesn't really store the new todo, that re-fetch will bring back the original 200 todos — the newly created one won't be in it. You'll fix the *appearance* of this with `setQueryData` in 2.5, which is the more realistic pattern anyway (the server already told you what it "created" in the response — no need to re-fetch to find out).
- `mutation.isPending` — `true` while the request is in flight
- `mutation.error` — the thrown error, if any

Write the equivalent `useCreateUser` hook in `src/hooks/useCreateUser.ts`, using `Omit<User, 'id'>` and invalidating `['users']`.

### 2.5 — Challenge

Add hooks for updating and deleting a todo, using `setQueryData` to write the result directly into the cache instead of relying on `invalidateQueries` to re-fetch data the fake API won't actually have:

```typescript
// src/hooks/useUpdateTodo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Todo } from '@/types/api'

export function useUpdateTodo(id: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (completed: boolean) =>
      api.patch<Todo>(`/todos/${id}`, { completed } satisfies Partial<Todo>).then(res => res.data),
    onSuccess: (updatedTodo) => {
      queryClient.setQueryData(['todos', id], updatedTodo)
    },
  })
}
```

Write `useDeleteTodo(id)` in `src/hooks/useDeleteTodo.ts` similarly, calling `api.delete` — since there's no real list to re-fetch from, you'll handle removing it from the UI directly in the component in section 3.

Compare the size of `TaskDetailPage.tsx` once it just calls `useTodo`, `useUpdateTodo`, and `useDeleteTodo`, versus writing all three inline — you'll build the page itself in section 3.

## 3. Putting It Together

Now build the **presentational components** — pure, props-in-JSX-out, no data fetching — and compose them with the hooks from section 2 into complete pages. This is the payoff for the split: each file stays small and has one job.

### 3.1 — User components and page

Build `src/components/UserCard.tsx` — display only:

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { User } from '@/types/api'

export function UserCard({ user }: { user: User }) {
  return (
    <Card>
      <CardHeader><CardTitle className="text-base">{user.name}</CardTitle></CardHeader>
      <CardContent>
        <p className="text-sm text-gray-500">{user.email}</p>
      </CardContent>
    </Card>
  )
}
```

`src/pages/UsersPage.tsx` is composition only — it owns no fetch logic:

```tsx
import { useUsers } from '@/hooks/useUsers'
import { UserCard } from '@/components/UserCard'

export default function UsersPage() {
  const { data: users = [], isLoading } = useUsers()

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Users</h1>
      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {users.map(user => <UserCard key={user.id} user={user} />)}
        </div>
      )}
    </div>
  )
}
```

JSONPlaceholder's ten users are fixed sample data (read-only in practice, since creates don't persist), so this page is display-only — the create-a-user form from section 1 was for learning the POST pattern, not something you need to keep wired into the final page.

### 3.2 — Todo components and page

Build `src/components/TaskCard.tsx` — named for the page it lives on, backed by the `Todo` type:

```tsx
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { StatusBadge } from '@/components/StatusBadge'
import { Todo } from '@/types/api'

export function TaskCard({ todo }: { todo: Todo }) {
  return (
    <Link to={`/tasks/${todo.id}`}>
      <Card className="hover:shadow-md transition-shadow cursor-pointer h-full">
        <CardHeader>
          <CardTitle className="text-base">{todo.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <StatusBadge completed={todo.completed} />
        </CardContent>
      </Card>
    </Link>
  )
}
```

And `src/components/TaskForm.tsx`:

```tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { User } from '@/types/api'

interface TaskFormProps {
  users: User[]
  onSubmit: (data: { title: string; userId: number }) => void
  submitting: boolean
}

export function TaskForm({ users, onSubmit, submitting }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [userId, setUserId] = useState<number | null>(null)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!userId) return
    onSubmit({ title, userId })
    setTitle('')
    setUserId(null)
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <Input placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} required />
      <Select value={userId ? String(userId) : ''} onValueChange={v => setUserId(Number(v))}>
        <SelectTrigger>
          <SelectValue placeholder="Assign to..." />
        </SelectTrigger>
        <SelectContent>
          {users.map(u => (
            <SelectItem key={u.id} value={String(u.id)}>{u.name}</SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Button type="submit" disabled={submitting || !userId}>
        {submitting ? 'Creating...' : 'Create Task'}
      </Button>
    </form>
  )
}
```

`src/pages/TasksPage.tsx` composes hooks and components, and owns only the filter state (that's genuinely page-level UI state, not server state):

```tsx
import { useState } from 'react'
import { useUsers } from '@/hooks/useUsers'
import { useTodos } from '@/hooks/useTodos'
import { useCreateTodo } from '@/hooks/useCreateTodo'
import { TaskCard } from '@/components/TaskCard'
import { TaskForm } from '@/components/TaskForm'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

export default function TasksPage() {
  const [userFilter, setUserFilter] = useState<number | 'all'>('all')
  const { data: users = [] } = useUsers()
  const { data: todos = [], isLoading } = useTodos(userFilter)
  const createTodo = useCreateTodo()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
        <Select value={String(userFilter)} onValueChange={v => setUserFilter(v === 'all' ? 'all' : Number(v))}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filter by user" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All users</SelectItem>
            {users.map(u => (
              <SelectItem key={u.id} value={String(u.id)}>{u.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Card className="max-w-sm">
        <CardHeader><CardTitle>New Task</CardTitle></CardHeader>
        <CardContent>
          <TaskForm
            users={users}
            onSubmit={data => createTodo.mutate({ ...data, completed: false })}
            submitting={createTodo.isPending}
          />
        </CardContent>
      </Card>

      {isLoading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {todos.slice(0, 20).map(todo => <TaskCard key={todo.id} todo={todo} />)}
        </div>
      )}
    </div>
  )
}
```

JSONPlaceholder returns up to 200 todos for `/todos` and up to 20 per user — `.slice(0, 20)` keeps the grid from getting overwhelming; feel free to add real pagination as a stretch goal. When `userFilter` changes, `useTodos` looks for `['todos', 2]` (say) in the cache — if it exists, the cached data renders instantly while a background refetch runs silently.

### 3.3 — Task detail page

```tsx
// src/pages/TaskDetailPage.tsx
import { useParams, useNavigate } from 'react-router-dom'
import { useTodo } from '@/hooks/useTodo'
import { useUpdateTodo } from '@/hooks/useUpdateTodo'
import { useDeleteTodo } from '@/hooks/useDeleteTodo'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { StatusBadge } from '@/components/StatusBadge'

export default function TaskDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: todo, isLoading, isError } = useTodo(id!)
  const updateTodo = useUpdateTodo(id!)
  const deleteTodo = useDeleteTodo(id!)

  if (isLoading) return <p className="text-gray-500">Loading...</p>
  if (isError) return <p className="text-red-500">Task not found.</p>
  if (!todo) return null

  return (
    <div className="max-w-lg space-y-4">
      <Button variant="outline" onClick={() => navigate('/tasks')}>← Back</Button>

      <Card>
        <CardHeader>
          <CardTitle>{todo.title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-3">
            <StatusBadge completed={todo.completed} />
            <Button
              variant="outline"
              size="sm"
              onClick={() => updateTodo.mutate(!todo.completed)}
              disabled={updateTodo.isPending}
            >
              {todo.completed ? 'Mark pending' : 'Mark done'}
            </Button>
          </div>

          <Button
            variant="destructive"
            onClick={() => deleteTodo.mutate(undefined, { onSuccess: () => navigate('/tasks') })}
            disabled={deleteTodo.isPending}
            className="w-full"
          >
            {deleteTodo.isPending ? 'Deleting...' : 'Delete Task'}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
```

Every hook call here is one line. All the fetch/cache/mutation logic lives in `src/hooks/`; this file only decides what to render and when to call what. Toggle the status, then refresh the page — the toggle reverts, because JSONPlaceholder never really saved it. That's expected, and worth confirming for yourself once.

### 3.4 — Home page

```tsx
// src/pages/HomePage.tsx
import { Link } from 'react-router-dom'
import { useUsers } from '@/hooks/useUsers'
import { useTodos } from '@/hooks/useTodos'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function HomePage() {
  const { data: users = [] } = useUsers()
  const { data: todos = [], isLoading } = useTodos('all')

  const completedCount = todos.filter(t => t.completed).length

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
            <CardContent><p className="text-3xl font-bold">{todos.length}</p></CardContent>
          </Card>
        </Link>
        <Card>
          <CardHeader><CardTitle className="text-sm text-gray-500">Done</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-green-600">{completedCount}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm text-gray-500">Pending</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-gray-600">{todos.length - completedCount}</p></CardContent>
        </Card>
      </div>
    </div>
  )
}
```

Because `useUsers()` and `useTodos('all')` use the same keys everywhere, navigating here after visiting Users or Tasks shows the counts instantly from cache.

### 3.5 — Challenge: remove-from-list on delete

Since JSONPlaceholder won't actually remove the todo from future `/todos` fetches, make the delete feel real within the session by removing it from every relevant cache entry directly, instead of relying on `invalidateQueries`:

```typescript
// src/hooks/useDeleteTodo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { Todo } from '@/types/api'

export function useDeleteTodo(id: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => api.delete(`/todos/${id}`),
    onSuccess: () => {
      queryClient.setQueriesData<Todo[]>({ queryKey: ['todos'] }, (old) =>
        old?.filter(t => t.id !== Number(id))
      )
    },
  })
}
```

`setQueriesData` (plural) updates every cache entry whose key starts with `['todos']` — `['todos', 'all']`, `['todos', 1]`, `['todos', 2]`, etc. — in one call, so the deleted task disappears from whichever filtered view you're on.

## 4. Final Exercise

Complete `task-ui` as a fully working frontend against JSONPlaceholder, using the file layout from this tutorial:

```
src/
  hooks/       useUsers, useTodos, useTodo, useCreateUser, useCreateTodo,
               useUpdateTodo, useDeleteTodo
  components/  Layout, StatusBadge, UserCard, TaskCard, TaskForm,
               ui/ (shadcn)
  pages/       HomePage, UsersPage, TasksPage, TaskDetailPage, NotFoundPage
```

**Requirements:**

**Users page** (`/users`):
- Lists all users in a card grid

**Tasks page** (`/tasks`):
- Lists tasks as clickable cards
- User filter dropdown re-fetches from the API when changed
- Create form with title and owner selector (populated from `useUsers`)
- New task appears in the grid immediately on creation (via the cache — not necessarily via a real re-fetch)

**Task detail page** (`/tasks/:id`):
- Loads the task by id
- A button toggles completed/pending and saves immediately
- Delete button removes the task from the grid and redirects to `/tasks`
- Shows "Task not found." for ids above 200

**Navigation:**
- Persistent nav bar with active link highlighting (from part 1)
- Back button on the task detail page
- 404 page for unknown routes (from part 1)

**No page component should contain a `useQuery` or `useMutation` call directly** — every data operation goes through a hook in `src/hooks/`.

**Verification — run through this in your browser:**

1. Open the home page — confirm the dashboard counts are accurate
2. Open the users page — confirm all ten JSONPlaceholder users appear
3. Create a task and confirm it appears in the grid immediately
4. Filter tasks by a specific user — confirm only their tasks show
5. Click a task card — confirm the detail page loads correctly
6. Toggle a task's status — confirm the badge updates without a page reload
7. Refresh the detail page and confirm the status reverts — and that you understand why (JSONPlaceholder doesn't persist writes)
8. Delete a task — confirm redirect to `/tasks` and the task is gone from the grid
9. Visit `/tasks/99999` — confirm "Task not found." appears
10. Visit `/doesnotexist` — confirm the 404 page appears

## Checklist

- [ ] Can create an Axios instance with a base URL
- [ ] Understand why `Omit<T, 'id'>` and `Partial<T>` cover create/update shapes without hand-written interfaces
- [ ] Felt the `useEffect` + triple-`useState` pattern firsthand before replacing it
- [ ] Can set up `QueryClient` and `QueryClientProvider` in `main.tsx`
- [ ] Can write a `useQuery`-based hook in its own file and explain `queryKey`, `queryFn`, `data`, `isLoading`, `isError`
- [ ] Understand how variable query keys (`['todos', userId]`) give each value its own cache entry
- [ ] Can write a `useMutation`-based hook with `mutationFn`, `onSuccess`, and `isPending`
- [ ] Understand why `setQueryData`/`setQueriesData` matter more than usual against an API that doesn't persist writes
- [ ] Can separate a page (composition) from a component (presentation, no fetching) from a hook (fetching, no JSX)
- [ ] Can explain, in your own words, why a refreshed page reverts a change you just made
- [ ] All pages in the final exercise work end-to-end against JSONPlaceholder, with no `useQuery`/`useMutation` calls inside page files
