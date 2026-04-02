# TypeScript Exercises

You know Python. TypeScript is JavaScript with types bolted on. The syntax looks different but the concepts are the same — variables, loops, functions, data structures. The main adjustment is that types are explicit and the compiler will reject your code if something doesn't add up.

Work through each section in order. Every section ends harder than it starts.

**Reference:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) · [TypeScript Playground](https://www.typescriptlang.org/play) (run code in the browser, no setup needed)

## 0. Setup

Install [Node.js](https://nodejs.org/en/download) if you haven't already, then:

```bash
npm install -g tsx
```

`tsx` lets you run a `.ts` file directly without a separate compile step:

```bash
tsx hello.ts
```

Create a folder called `ts-exercises` and do all your work in there. One file per section is fine.

**Verify:** Create `hello.ts`, write a line that prints something, and run it. If you see output, you're ready.

## 1. Variables and Types

> Python uses `x = 5`. TypeScript has two ways to declare a variable, and you can optionally tell it the type.

**Reference:** [Variable Declarations](https://www.typescriptlang.org/docs/handbook/variable-declarations.html)

### 1.1

Declare a variable using `let`. Assign it a string, then reassign it a different string. Print both values.

### 1.2

Declare a variable using `const`. Try to reassign it. Read the error.

Figure out: when would you use `let` vs `const`? Write your conclusion as a comment.

### 1.3

TypeScript can infer types automatically. Declare a variable and assign it a number. Then try to reassign it a string. Read the compiler error — it caught a bug without you writing a single type annotation.

### 1.4

Now write explicit type annotations. Declare:

- A `string` variable for a username
- A `number` variable for an age
- A `boolean` variable for whether the account is active

Then try assigning the wrong type to each. Confirm the compiler rejects all three.

### 1.5

Python has `None`. TypeScript has two things: `null` and `undefined`. They are different.

Declare a variable explicitly typed as `string | null` and assign `null` to it. Then assign it a real string. Print both.

> You'll need to look up what `|` means here. It will come up constantly in the codebase.

### 1.6

Declare five variables — at least one of each type (`string`, `number`, `boolean`). Do not write any type annotations. Use `console.log(typeof x)` on each one.

What does `typeof` return? Is it the same as Python's `type()`? Write the difference as a comment.

## 2. Control Flow

> `if`, `else`, comparisons. Same idea as Python, different syntax.

### 2.1

Write an `if/else` that checks whether a number is positive, negative, or zero. Print a message for each case.

Note: blocks use `{}`, not indentation. There is no `elif` — look up what to use instead.

### 2.2

In Python you use `==` for comparison. In TypeScript (and JavaScript) there are two equality operators: `==` and `===`. They behave differently.

Research the difference. Then write a short example that demonstrates it. Add a comment explaining which one you should always use and why.

### 2.3

The **ternary operator** is a one-line if/else. Look up the syntax and rewrite your Exercise 2.1 solution as a single expression.

> Python has this too but the syntax is different. You'll use ternary expressions a lot in React.

### 2.4

Look up the `switch` statement. Write one that takes a `status` variable (which could be `"active"`, `"inactive"`, or `"banned"`) and prints a different message for each.

What happens if you forget the `break` keyword? Try removing one and see.

### 2.5

Write a function `classify(n: number): string` that returns:

- `"fizz"` if divisible by 3
- `"buzz"` if divisible by 5
- `"fizzbuzz"` if divisible by both
- the number as a string otherwise

No hints on how to check divisibility — figure it out from your Python knowledge.

## 3. Loops

> Python has `for x in list`. TypeScript has several loop types. They are not all the same.

### 3.1

Declare an array of five numbers. Write a classic `for` loop using an index variable to print each one.

```
for (let i = ...) { ... }
```

> This is the C-style for loop Python doesn't have. Look up the syntax.

### 3.2

Write the same loop using `for...of`. This is the TypeScript equivalent of Python's `for x in list`.

What is the difference between `for...of` and `for...in`? Write a comment explaining it — and demonstrate `for...in` on the same array. The output might surprise you.

### 3.3

Write a `while` loop that counts down from 10 to 1 and prints each number. Then make it stop early if the number is 5. Look up how to break out of a loop.

### 3.4

Recreate this Python snippet in TypeScript:

```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

TypeScript doesn't have `enumerate`. Figure out how to get both the index and the value.

### 3.5

Write a loop (any kind) that builds a new array containing only the even numbers from this list:

```ts
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
```

Do it with a loop first. Then look up the `.filter()` array method and do it in one line without a loop.

### 3.6 — Challenge

Write a loop that prints a multiplication table from 1×1 to 10×10. Each row should be formatted neatly. Use nested loops.

## 4. Functions

> Python uses `def`. TypeScript has two syntaxes. You need to know both.

**Reference:** [Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

### 4.1

Write a function using the `function` keyword that takes two numbers and returns their sum. Call it and print the result.

Then rewrite the exact same function as an **arrow function** assigned to a `const`. Both should behave identically.

### 4.2

Add type annotations to a function: typed parameters and a typed return value. Write a function `greet(name: string): string` that returns a greeting string using a **template literal**.

> Template literals are TypeScript's equivalent of Python f-strings. Look up the syntax — it uses backticks.

### 4.3

Write a function with an **optional parameter**. The function `formatName(first: string, last?: string): string` should return just the first name if no last name is given, or the full name if both are provided.

Handle the case where `last` might be undefined.

### 4.4

Write a function with a **default parameter** value. `repeat(text: string, times: number = 3): string` should return the text repeated that many times.

### 4.5

Functions can return different types. Write a function `divide(a: number, b: number): number | null` that returns `null` if the divisor is zero, otherwise the result.

Write the calling code that handles both cases.

### 4.6 — Challenge

Write a function `pipe` that takes a starting number and an array of functions (each `(n: number) => number`), applies them in sequence, and returns the final result.

```ts
const result = pipe(5, [
  x => x * 2,
  x => x + 3,
  x => x ** 2,
]);
// (5 * 2 + 3)^2 = 169
```

You'll need to look up how to type an array of functions.

## 5. Arrays and Array Methods

> Python lists → TypeScript arrays. But TypeScript arrays have methods that replace list comprehensions. You'll use these constantly in React.

**Reference:** [Array methods on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)

### 5.1

Declare a typed array of strings. Add items using `.push()`. Remove the last item with `.pop()`. Print the array after each operation.

### 5.2

Python has list comprehensions: `[x * 2 for x in numbers]`. TypeScript uses `.map()`.

Given:
```ts
const prices = [10, 25, 8, 42, 17];
```

Use `.map()` to produce a new array where every price has 20% added. Do not modify the original.

### 5.3

Use `.filter()` to get only prices above 15 from the same array.

Then chain `.map()` and `.filter()` in a single expression to get the discounted price of every item that was originally above 15.

### 5.4

`.reduce()` collapses an array into a single value. Look up the syntax — it's used everywhere.

Use it to:
1. Sum all the prices
2. Find the maximum price (without using `Math.max`)

### 5.5

Given an array of names: `["alice", "bob", "charlie", "diana"]`

Use `.find()` to get the first name longer than 4 characters. Use `.findIndex()` to get its position. Use `.some()` to check if any name starts with "z". Use `.every()` to check if all names are lowercase.

Print all four results.

### 5.6

Look up array **destructuring**. Given:

```ts
const coords = [51.5, -0.1, 10];
```

Unpack it into three named variables `lat`, `lng`, `altitude` in a single line. No index access.

### 5.7 — Challenge

Given this array:

```ts
const words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"];
```

Without using any loops — only array methods — produce an object where each key is a unique word and each value is how many times it appears. The result should be:

```ts
{ the: 2, quick: 1, brown: 1, ... }
```

## 6. Objects and Interfaces

> Python dicts are flexible. TypeScript objects have a fixed shape defined by an interface, and the compiler enforces it.

### 6.1

Create an object literal with at least four properties of different types. Access each property using dot notation. Try accessing a property that doesn't exist — read the compiler error.

### 6.2

Look up object **destructuring**. Given:

```ts
const user = { id: 1, name: "alice", email: "alice@example.com", role: "admin" };
```

Unpack `name` and `role` into separate variables in a single line.

### 6.3

Define an `interface` for a `Product`:

- `id`: number
- `name`: string
- `price`: number
- `inStock`: boolean
- `category`: string

Write a function `formatProduct(product: Product): string` that returns a one-line summary. Create two Product objects and call it on both.

**Verify:** Try removing a required field from one of your objects. The compiler should reject it.

### 6.4

Add an optional field `discount?: number` to your `Product` interface. Update `formatProduct` to include the discounted price when a discount exists.

**Verify:** Existing objects without `discount` should still compile fine.

### 6.5

Interfaces can reference other interfaces. Create a `Supplier` interface with `id`, `name`, and `contactEmail`. Add a `supplier: Supplier` field to `Product`.

Update your Product objects and `formatProduct` to use the nested supplier. Try passing a supplier object that's missing `contactEmail` — confirm the compiler catches it.

### 6.6

Look up the **spread operator** (`...`) for objects. Given:

```ts
const base = { id: 1, name: "Widget", price: 9.99, inStock: true, category: "misc" };
```

Create a new Product object that is identical to `base` except the price is 14.99. Do it in one line without repeating every field.

> Python equivalent: `{**base, "price": 14.99}`

### 6.7 — Challenge

Define interfaces for a simple order system:

- `Customer`: id, name, email
- `OrderItem`: productId, productName, quantity, unitPrice
- `Order`: id, customer, items (array of OrderItem), status (`"pending" | "shipped" | "delivered"`)

Write a function `orderTotal(order: Order): number` that returns the total cost across all items.

Write another function `orderSummary(order: Order): string` that returns a formatted summary including the customer name, item count, total, and status.

## 7. Putting It Together

No section reference. No hints. Read the spec, model it, make it work.

### Final Exercise — Task Manager

Build a typed task manager. Requirements:

**Data model**

- A `User` has an `id` (number), `name` (string), and `email` (string)
- A `Task` has an `id`, `title`, `description` (optional), `priority` (`"low" | "medium" | "high"`), `status` (`"todo" | "in-progress" | "done"`), `assignee` (a `User`), and `createdAt` (string)

**Functions — all must be fully typed, no `any`**

- `createTask(title, priority, assignee)` — returns a new Task with status `"todo"` and a generated id
- `assignTask(task, user)` — returns a new task (do not mutate the original) with the updated assignee
- `completeTask(task)` — returns a new task with status `"done"`
- `filterByStatus(tasks, status)` — returns only tasks matching the given status
- `filterByPriority(tasks, priority)` — returns only tasks matching the given priority
- `getAssigneeTasks(tasks, userId)` — returns all tasks assigned to a specific user
- `summarise(tasks)` — prints a breakdown: how many tasks per status, how many per priority

**Demonstrate it works** by creating at least three users and five tasks, running them through several of the functions, and printing meaningful output.

## Checklist

- [ ] Can declare variables with `let` and `const` and explain the difference
- [ ] Understand when TypeScript infers a type vs when you must write it explicitly
- [ ] Can write both regular functions and arrow functions with full type annotations
- [ ] Know the difference between `for...of` and `for...in`
- [ ] Can use `.map()`, `.filter()`, and `.reduce()` without looking them up
- [ ] Can define an interface and use it across multiple functions
- [ ] Understand optional properties and union types
- [ ] Completed the final exercise with no `any` types
