# Async and Promises

JavaScript runs on a single thread. That means if you wait for something — a network request, a file read, a database query — you block everything else. Promises are how JavaScript handles waiting without blocking.

This tutorial builds from the problem up: why callbacks exist, why they're painful, why Promises fix them, and why `async/await` is the syntax you'll actually use every day.

Work through each section in order. You need Node.js 18+ for the `fetch` exercises — run `node --version` to check.

## Before you start

Read these first — they're short and will make the exercises click faster:

- [javascript.info — Introduction: callbacks](https://javascript.info/callbacks) — why async code exists and what the problem looks like
- [javascript.info — Promises](https://javascript.info/promise-basics) — how Promises work and why they're better than callbacks
- [javascript.info — async/await](https://javascript.info/async-await) — the syntax you'll actually write day to day
- [MDN — Using Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) — good to keep open while working through the exercises

You don't need to understand everything before starting. Read enough to have a mental model, then come back when something doesn't make sense.

## 0. The problem

JavaScript can only do one thing at a time. If it had to wait for a network request to finish before moving on, the entire page (or server) would freeze until the response came back.

The solution: instead of waiting, you hand JavaScript a callback — a function to call *when the work is done* — and move on. JavaScript will circle back to it later.

This is what makes JavaScript async. Everything in this tutorial is built on that idea.

## 1. Callbacks

You've already used callbacks without knowing it. `.map()`, `.filter()`, and `.forEach()` all take callbacks. Async callbacks work the same way — except they run later, not immediately.

### 1.1

`setTimeout` schedules a callback to run after a delay. It doesn't block — execution continues immediately and the callback runs later.

```ts
console.log("start");

setTimeout(() => {
  console.log("inside timeout");
}, 1000);

console.log("end");
```

Run this. Before you do, write down what order you expect the three lines to print. Then check if you were right.

### 1.2

Here are three functions that simulate async operations using `setTimeout`:

```ts
function getUser(id: number, callback: (user: { id: number; name: string }) => void) {
  setTimeout(() => callback({ id, name: "Alice" }), 300);
}

function getOrders(userId: number, callback: (orders: string[]) => void) {
  setTimeout(() => callback(["order-1", "order-2"]), 300);
}

function getOrderDetails(orderId: string, callback: (detail: string) => void) {
  setTimeout(() => callback(`Details for ${orderId}`), 300);
}
```

Call all three in sequence — pass the result of each into the next — and log the final detail. You'll need to nest the calls.

Read the shape of what you wrote. This nesting is called **callback hell**. Promises were invented to solve it.

## 2. Promises

A Promise represents a value that doesn't exist yet — it will either resolve (success) or reject (failure). You construct one like this:

```ts
const p = new Promise<string>((resolve, reject) => {
  // call resolve(value) when done, reject(error) if something went wrong
});
```

Chain `.then()` to handle the resolved value, `.catch()` for errors, `.finally()` for cleanup that runs either way.

### 2.1

Create a Promise that resolves with the string `"done"` after 500ms. Chain `.then()` to log the result.

Then create a second version that rejects with an `Error` instead. Add `.catch()` to handle it. Confirm that without `.catch()`, Node.js prints an unhandled rejection warning.

### 2.2

Rewrite the three functions from section 1.2 to return Promises instead of taking callbacks. The signatures should look like:

```ts
function getUser(id: number): Promise<{ id: number; name: string }>
function getOrders(userId: number): Promise<string[]>
function getOrderDetails(orderId: string): Promise<string>
```

Chain them with `.then()` to reproduce the same result as 1.2. Add a single `.catch()` at the end.

Compare the shape of this code to your nested callbacks. Note the difference.

### 2.3

Add `.finally()` to your chain from 2.2 to log `"request complete"` whether it succeeded or failed.

Then deliberately make `getOrders` reject — confirm `.catch()` catches it and `.finally()` still runs.

## 3. async/await

`async/await` is syntax built on top of Promises. An `async` function always returns a Promise. Inside one, `await` pauses execution until a Promise resolves — without blocking the thread. Under the hood it's still Promises.

```ts
async function example() {
  const result = await somePromise();
  console.log(result);
}
```

### 3.1

Rewrite your chain from 2.2 as an `async` function using `await`. It should read like synchronous code — no `.then()` calls.

### 3.2

Add error handling to your async function. `async/await` uses `try/catch` — look up how it maps to `.catch()` on a Promise chain.

Make `getOrders` reject and confirm your `catch` block handles it.

### 3.3

Write two functions that both use the three helpers from section 1.2 (the Promise versions):

- `fetchSequential` — fetches order details for each order one at a time, returns all details as a `string[]`
- `fetchParallel` — fetches all order details at the same time using `Promise.all`

Measure how long each takes with `Date.now()`. The difference should be clear.

> `Promise.all` takes an array of Promises and resolves when all of them resolve.

## 4. fetch

`fetch` is the built-in API for HTTP requests. It returns a Promise. Node.js 18+ includes it natively.

Two things to know before the exercises:

1. `fetch` gives you back a `Response` object. To get the body as JSON, call `response.json()` — that's also a Promise, so you need a second `await`.
2. `fetch` only rejects on network failure. A 404 or 500 still resolves — `response.ok` tells you whether the status was 2xx. Always check it.

### 4.1

Write an async function that fetches a single todo from `https://jsonplaceholder.typicode.com/todos/1` and logs the result. You'll need two `await` calls — one for the response, one for the JSON body.

### 4.2

Update your function to check `response.ok` before parsing the body. If the request failed, throw an `Error` with the status code in the message. Test it works by changing the URL to a bad endpoint.

### 4.3

Define a `Todo` interface that matches the shape of the response:

```ts
interface Todo {
  userId: number;
  id: number;
  title: string;
  completed: boolean;
}
```

Wrap your fetch logic in a typed function `getTodo(id: number): Promise<Todo>`. Use it to fetch todo 5 and log the title and completed status in a formatted string.

### 4.4

Use `getTodo` and `Promise.all` to fetch todos 1 through 5 in parallel. Log each title when they all resolve.

### 4.5 — Challenge

Write a function `searchTodos(query: string): Promise<Todo[]>` that:

1. Fetches all todos from `https://jsonplaceholder.typicode.com/todos`
2. Returns only the completed ones whose title contains the query (case-insensitive)

Print the count and titles of the results.

Then handle the failure case — if the fetch fails, print a user-friendly message instead of crashing.

## 5. Common mistakes

### 5.1

Forgetting `await` is the most common error. Run this:

```ts
async function run() {
  const response = fetch("https://jsonplaceholder.typicode.com/todos/1");
  console.log(response);
}

run();
```

What does `response` contain? Why? Fix it.

### 5.2

`await` inside `.forEach()` doesn't work the way you'd expect:

```ts
async function run() {
  const ids = [1, 2, 3];

  ids.forEach(async (id) => {
    const todo = await getTodo(id);
    console.log(todo.title);
  });

  console.log("done");
}
```

Run it. Notice the order of output. `forEach` doesn't wait for async callbacks — it fires them all and moves on.

Figure out two ways to fix this: one that processes items sequentially, one that processes them in parallel.

### 5.3

If an async function throws and nothing catches it, Node.js will warn about an unhandled rejection. Write an async function that throws, call it without `.catch()`, and read the warning. Then fix it.

## Checklist

- [ ] Understand why JavaScript needs async — single-threaded, can't block
- [ ] Can read and write callback-style async code
- [ ] Can create a Promise manually with `resolve` and `reject`
- [ ] Can chain `.then()`, `.catch()`, and `.finally()`
- [ ] Can rewrite a Promise chain using `async/await`
- [ ] Know how to handle errors with `try/catch` in async functions
- [ ] Can use `Promise.all` to run multiple async operations in parallel
- [ ] Can fetch data from an API using `fetch`, check `response.ok`, and type the result
- [ ] Know why `await` inside `.forEach()` doesn't work and what to use instead
