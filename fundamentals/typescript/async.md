# Async and Promises

JavaScript runs on a single thread. That means if you wait for something — a network request, a file read, a database query — you block everything else. Promises (and `async`/`await` on top of them) are how JavaScript handles waiting without blocking.

## What is async, and why do we need it?

"Async" means code that keeps running instead of stopping to wait for something slow. The alternative — **synchronous** code — executes one line at a time, in order, and each line has to finish before the next one starts.

That's fine for fast, in-memory work like adding two numbers. It falls apart for anything that takes real time: fetching data over the network, reading a file from disk, querying a database. Those operations can take milliseconds to seconds — an eternity for a CPU. If JavaScript blocked on every one of them, a browser tab would freeze mid-request and a server would be unable to handle any other user's request until the first one finished.

Because JavaScript only has one thread to run code on, it can't just spin up a second thread to wait on your behalf the way some other languages do. Instead, it hands the slow operation off (to the browser or Node's runtime, outside your JS code), keeps executing everything else, and comes back to run your code again once the result is ready. That "come back to it later" mechanism is what `async` code, Promises, and `async`/`await` are all built around.

**Analogy:** think of a single waiter running a restaurant. A synchronous waiter takes one table's order, walks it to the kitchen, and then just stands there staring at the pass until the food is ready before doing anything else — every other table sits ignored the whole time. An async waiter takes the order, hands it to the kitchen, and immediately goes to take the next table's order, refill water, and clear plates. When the kitchen rings a bell for a finished dish, the waiter goes and delivers it, then goes right back to whatever they were doing. One waiter (thread), but nobody sits around blocked waiting on the kitchen (the slow operation).

## Video

[Mastering async code with Typescript and Javascript](https://www.youtube.com/watch?v=VcOMq3LQtBU&t=390s)

## Resources

- [javascript.info — Promises](https://javascript.info/promise-basics) — how Promises work
- [javascript.info — async/await](https://javascript.info/async-await) — the syntax you'll actually write day to day

## Supplementary Notes

**Promises**

A Promise represents a value that doesn't exist yet — it will either resolve (success) or reject (failure):

```ts
const p = new Promise<string>((resolve, reject) => {
  // call resolve(value) when done, reject(error) if something went wrong
});

p.then((value) => console.log(value))
 .catch((err) => console.error(err))
 .finally(() => console.log("request complete"));
```

`.then()` handles the resolved value, `.catch()` handles errors, `.finally()` runs either way.

**async/await**

`async`/`await` is syntax built on top of Promises. An `async` function always returns a Promise. Inside one, `await` pauses execution until a Promise resolves — without blocking the thread.

```ts
async function getOrderDetails(): Promise<string> {
  try {
    const user = await getUser(1);
    const orders = await getOrders(user.id);
    const detail = await getOrderDetails(orders[0]);
    return detail;
  } catch (err) {
    console.error(err);
    throw err;
  }
}
```

`try`/`catch` is the `async`/`await` equivalent of `.catch()` on a Promise chain.

**Running things in parallel**

`await`ing calls one after another runs them sequentially, even when they don't depend on each other. `Promise.all` runs them in parallel:

```ts
const sequential = [];
for (const id of orderIds) {
  sequential.push(await getOrderDetails(id)); // waits for each one before starting the next
}

const parallel = await Promise.all(orderIds.map(getOrderDetails)); // all start immediately
```

**fetch**

`fetch` is the built-in API for HTTP requests and returns a Promise. Node.js 18+ includes it natively.

```ts
interface Todo {
  userId: number;
  id: number;
  title: string;
  completed: boolean;
}

async function getTodo(id: number): Promise<Todo> {
  const response = await fetch(`https://jsonplaceholder.typicode.com/todos/${id}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}
```

Two things that trip people up:
- `response.json()` is also a Promise — it needs its own `await`.
- `fetch` only rejects on network failure. A 404 or 500 still *resolves* — check `response.ok` to catch it.

**Common mistakes**

- *Forgetting `await`.* Without it, you get the `Promise` object itself, not its resolved value.
- *`await` inside `.forEach()`.* `forEach` doesn't wait for async callbacks — it fires them all and moves on immediately, so logging happens out of order. Use a `for...of` loop for sequential awaits, or `Promise.all` for parallel ones.
- *Unhandled rejections.* If an async function throws and nothing catches it, Node.js warns about an unhandled rejection. Always wrap awaited calls in `try`/`catch`, or attach `.catch()`.
