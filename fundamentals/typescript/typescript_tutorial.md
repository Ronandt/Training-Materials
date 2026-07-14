# TypeScript Reference

You know Python. TypeScript is JavaScript with types bolted on. The syntax looks different but the concepts are the same — variables, loops, functions, data structures. The main adjustment is that types are explicit and the compiler will reject your code if something doesn't add up.

## Video

[TypeScript Tutorial for Beginners](https://www.youtube.com/watch?v=d56mG7DezGs)

## Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Playground](https://www.typescriptlang.org/play) — run code in the browser, no setup needed
- [Array methods on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)

## Supplementary Notes

### Variables and Types

`let` allows reassignment; `const` doesn't. TypeScript infers a type from the initial value, or you can annotate it explicitly with `name: type`:

```ts
let greeting = "hello";      // inferred as string
const pi = 3.14;             // cannot be reassigned
let username: string = "alice"; // explicit annotation
```

Python's `None` splits into two concepts: `null` (explicitly nothing) and `undefined` (never assigned). A value that might be absent uses a union type with `|`:

```ts
let email: string | null = null;
```

`typeof` returns a value's runtime type as a string (`"number"`, `"string"`, `"boolean"`, `"undefined"` — notably `typeof null` is `"object"`, a long-standing JS quirk). Checking `typeof` inside an `if` **narrows** a union type, so the compiler knows exactly which branch you're in:

```ts
function double(value: number | string): string {
  if (typeof value === "number") {
    return String(value * 2); // narrowed to number here
  }
  return value + value; // narrowed to string here
}
```

`??` (nullish coalescing) falls back only on `null`/`undefined` — unlike `||`, it doesn't treat `0`, `""`, or `false` as missing. `?.` (optional chaining) safely accesses a property that might not exist, returning `undefined` instead of throwing:

```ts
console.log(score ?? 100);              // 0 stays 0; || would give 100
console.log(user?.address?.city ?? "Unknown");
```

### Control Flow

`if`/`else if`/`else` use `{}` blocks instead of indentation. `===` checks value and type with no coercion — always prefer it over `==`:

```ts
console.log(1 == "1");   // true  — == coerces
console.log(1 === "1");  // false — === does not
```

Ternary and `switch` work as in most C-like languages:

```ts
const label = x > 0 ? "positive" : "non-positive";

switch (status) {
  case "active":   console.log("User is active"); break;
  case "inactive": console.log("User is inactive"); break;
  default:         console.log("Unknown status");
}
```

Each `case` needs a `break`, or execution falls through into the next one.

### Loops

```ts
for (let i = 0; i < nums.length; i++) { ... }   // C-style, index variable

for (const fruit of fruits) { ... }             // values — Python's `for x in list`
for (const i in fruits) { ... }                 // keys/indices as strings — rarely what you want on an array

while (count > 0) { ... }                       // condition-based, use break to exit early
```

There's no `enumerate()` — use the C-style loop, or `.entries()`:

```ts
for (const [i, fruit] of fruits.entries()) {
  console.log(`${i}: ${fruit}`);
}
```

### Functions

Two ways to write one — the `function` keyword, or an arrow function (used heavily in modern code):

```ts
function add(a: number, b: number): number {
  return a + b;
}

const add = (a: number, b: number): number => a + b; // shorthand, no `return` needed
```

Template literals replace f-strings: `` `Hello ${name}, you are ${age}` ``.

A `?` marks an optional parameter (`undefined` if omitted); `=` sets a default used when the argument is omitted:

```ts
function formatName(first: string, last?: string): string { ... }
function repeat(text: string, times: number = 3): string { ... }
```

A function can return a union type, and callers must handle every case:

```ts
function divide(a: number, b: number): number | null {
  if (b === 0) return null;
  return a / b;
}
```

### Arrays and Array Methods

These replace Python list comprehensions and are used constantly in React:

```ts
const doubled = prices.map(p => p * 2);              // transform every item
const expensive = prices.filter(p => p > 15);         // keep matching items
const total = prices.reduce((sum, p) => sum + p, 0);  // collapse to one value

names.find(n => n.length > 4);       // first match, or undefined
names.findIndex(n => n.length > 4);  // its index, or -1
names.some(n => n.startsWith("z"));  // true if any match
names.every(n => n === n.toLowerCase()); // true if all match
```

Array destructuring unpacks by position: `const [lat, lng, altitude] = coords;`

### Objects and Interfaces

Python dicts are flexible; TypeScript objects have a fixed shape defined by an `interface`, enforced by the compiler:

```ts
interface Product {
  id: number;
  name: string;
  price: number;
  inStock: boolean;
  discount?: number;       // optional field
  supplier: Supplier;      // interfaces can nest other interfaces
}
```

Object destructuring: `const { name, role } = user;`

The spread operator copies an object while overriding specific fields — Python's `{**base, "price": 14.99}`:

```ts
const discounted = { ...base, price: 14.99 };
```

`Record<Keys, Type>` builds an object type where every key is `Keys` and every value is `Type` — useful both as a lookup map and as an exhaustive mapping over a union:

```ts
type Role = "admin" | "editor" | "viewer";

const permissions: Record<Role, string[]> = {
  admin:  ["read", "write", "delete"],
  editor: ["read", "write"],
  viewer: ["read"],
}; // omitting a key here is a compiler error
```

### Classes and OOP

The shape matches Python's `__init__(self, name)` / `self.name` — TypeScript just requires properties to be declared:

```ts
class Animal {
  constructor(public name: string, private sound: string) {} // shorthand: declares + assigns

  speak(): string {
    return `${this.name} says ${this.sound}.`;
  }
}
```

Access modifiers (`public` default, `private` class-only, `protected` class + subclasses) are enforced at **compile time** — unlike Python's `_underscore` convention, which is only a hint.

`extends` inherits from a parent class; `super(...)` calls its constructor and `super.method()` calls its method:

```ts
class Dog extends Animal {
  constructor(name: string) { super(name, "woof"); }
  speak(): string { return `${super.speak()} (dog)`; }
}
```

`implements` makes the compiler enforce that a class has everything an interface requires:

```ts
interface Shape { area(): number; perimeter(): number; }

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
  perimeter(): number { return 2 * (this.width + this.height); }
}
```

`readonly` properties can be set in the constructor but never after. `static` members belong to the class itself, not an instance (`Config.MAX_RETRIES`, not `instance.MAX_RETRIES`).

Getters/setters run logic on property access while looking like a plain field:

```ts
class Temperature {
  constructor(private _celsius: number) {}
  get fahrenheit(): number { return this._celsius * 9 / 5 + 32; }
  set celsius(value: number) { this._celsius = value; }
}
```

An `abstract class` defines methods subclasses must implement and can't be instantiated directly:

```ts
abstract class Notification {
  abstract message(): string;
  send(): void { console.log(`Sending: ${this.message()}`); }
}
```

### Generics

Python 3.12's `TypeVar` does the same job: write one function or class that works across many types without losing type safety.

```ts
function identity<T>(value: T): T {
  return value; // return type == input type, tracked by the compiler
}
```

Constrain what can be passed with `extends`:

```ts
function getLength<T extends { length: number }>(value: T): number {
  return value.length; // works for string, array — not number
}
```

Interfaces and classes can be generic too:

```ts
interface ApiResponse<T> { data: T; status: number; message: string; }

class Stack<T> {
  private items: T[] = [];
  push(item: T): void { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
}
```

Several built-ins you already use are generic under the hood: `Array<T>` (same as `T[]`), `Map<K, V>`, `Set<T>`. `keyof T` represents any valid key of `T` — you'll see it constantly (e.g. `groupBy<T>(items: T[], key: keyof T)`).

A common pattern for functions that can fail is a discriminated union `Result<T>` (like Rust's `Result`, or Python's `(value, error)` tuple convention):

```ts
type Result<T> = { ok: true; value: T } | { ok: false; error: string };
```

### Modules and Imports/Exports

Named exports let importers take only what they need:

```ts
// maths.ts
export function add(a: number, b: number): number { return a + b; }
export const PI = 3.14159;

// main.ts
import { add, PI } from "./maths";
```

A default export is the one main thing a file exports (at most one per file), and is imported without braces:

```ts
export default function greet(name: string): string { return `Hello, ${name}!`; }
import greet from "./greeter"; // any local name works
```

Rename an import with `as`, or import everything as a namespace:

```ts
import { add as sum } from "./maths";
import * as Maths from "./maths"; // Maths.add(), Maths.PI
```

A **barrel file** (`index.ts`) re-exports everything from a folder so consumers import from one place:

```ts
// utils/index.ts
export { add, subtract, PI } from "./maths";
export { capitalise, truncate } from "./strings";
```

`import type` is erased entirely from the compiled output — use it when you only need a type at compile time, not a runtime value:

```ts
import type { User } from "./types";
```

### Error Handling

Same shape as Python's `try` / `except`, with `try` / `catch` / `finally` (`finally` always runs, even after an error):

```ts
try {
  const data = JSON.parse(input);
} catch (err) {
  console.log("Something went wrong");
} finally {
  console.log("Runs either way");
}
```

The caught value's type is `unknown`, not `Error` — anything can be thrown (`throw "oops"`), so you must narrow before accessing properties:

```ts
catch (err) {
  if (err instanceof Error) {
    console.log(err.message); // safe, narrowed
  } else {
    console.log("Unknown error:", err);
  }
}
```

Custom error classes extend `Error`, letting callers distinguish failure types with `instanceof`:

```ts
class NotFoundError extends Error {
  constructor(public readonly id: number) {
    super(`Resource ${id} not found`);
    this.name = "NotFoundError";
  }
}
```

Combining this with the `Result<T>` pattern above gives a `tryCatch` wrapper so callers never write `try`/`catch` themselves:

```ts
function tryCatch<T>(fn: () => T): Result<T> {
  try {
    return { ok: true, value: fn() };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : String(err) };
  }
}
```
