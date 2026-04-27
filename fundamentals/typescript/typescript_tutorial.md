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

TypeScript has two keywords for declaring variables: `let` and `const`.

```ts
let greeting = "hello";
greeting = "world"; // fine — let allows reassignment
console.log(greeting);
```

Declare a variable using `let`. Assign it a string, then reassign it a different string. Print both values.

### 1.2

`const` declares a variable that cannot be reassigned after its initial value:

```ts
const pi = 3.14;
pi = 3; // error: cannot assign to 'pi' because it is a constant
```

Declare a variable using `const`. Try to reassign it and read the error.

Figure out: when would you use `let` vs `const`? Write your conclusion as a comment.

### 1.3

TypeScript infers the type of a variable from its initial value. You do not have to write the type yourself — the compiler figures it out:

```ts
let score = 100;   // TypeScript infers: number
score = "high";    // error: type 'string' is not assignable to type 'number'
```

Declare a variable and assign it a number. Then try to reassign it a string. Read the compiler error — it caught a type mismatch without you writing a single annotation.

### 1.4

You can also write the type explicitly. The syntax is `variableName: type`:

```ts
let username: string = "alice";
let age: number = 30;
let isActive: boolean = true;
```

Declare three variables using explicit annotations — one `string`, one `number`, one `boolean`. Then try assigning the wrong type to each and confirm the compiler rejects all three.

### 1.5

Python has `None`. TypeScript has two things: `null` (explicitly nothing) and `undefined` (never assigned). They are different.

A variable that might hold a string or nothing is typed with `|`, which means "or":

```ts
let email: string | null = null;  // starts as nothing
email = "alice@example.com";      // now it's a string
console.log(email);
```

Declare a variable typed as `string | null`. Assign `null` to it, print it, then assign a real string and print it again.

> `|` is the union operator. You will see it constantly — `string | null`, `number | undefined`, `"active" | "inactive"` are all union types.

### 1.6

`typeof` returns the runtime type of a value as a string. It is similar to Python's `type()` but returns different things:

```ts
console.log(typeof 42);        // "number"
console.log(typeof "hello");   // "string"
console.log(typeof true);      // "boolean"
console.log(typeof undefined); // "undefined"
// Python's type(42) returns <class 'int'>, not a string
```

Declare five variables — at least one of each type (`string`, `number`, `boolean`). Do not write any type annotations. Use `console.log(typeof x)` on each one.

What does `typeof null` return? Look it up, then write a comment explaining why it is considered a historic bug in JavaScript.

### 1.7

Knowing the type of a value at runtime lets you **narrow** a union type — convincing the compiler that inside a branch, the value can only be one specific type:

```ts
function double(value: number | string): string {
  if (typeof value === "number") {
    // inside this block, TypeScript knows value is number
    return String(value * 2);
  }
  // here, TypeScript knows value must be string
  return value + value;
}
```

Without the `typeof` check, trying to use `value * 2` would be a compiler error because `*` doesn't work on strings.

Implement this function:

```ts
function padLeft(padding: number | string, input: string): string {
  // if padding is a number, prepend that many spaces to input
  // if padding is a string, prepend it directly
}
```

Then call it with both cases and confirm the output is correct. Try removing the `typeof` check and read the compiler error — it will tell you exactly why narrowing is necessary.

### 1.8

The **nullish coalescing operator** `??` returns the right-hand side when the left is `null` or `undefined` — and only those two values:

```ts
const username: string | null = null;

console.log(username ?? "Guest");   // "Guest" — left is null
console.log(username || "Guest");   // "Guest" — same result here...

const score: number = 0;
console.log(score ?? 100);   // 0   — 0 is not null/undefined
console.log(score || 100);   // 100 — || treats 0 as falsy, so this is wrong
```

`||` short-circuits on any falsy value (`0`, `""`, `false`, `null`, `undefined`). `??` only short-circuits on `null` or `undefined`. For optional values, `??` is almost always what you want.

The **optional chaining operator** `?.` safely accesses a property or calls a method on a value that might be `null` or `undefined`, returning `undefined` instead of throwing:

```ts
const user: { address?: { city: string } } | null = null;

console.log(user?.address?.city);      // undefined — no error
console.log(user?.address?.city ?? "Unknown");  // "Unknown"
```

The two operators compose naturally: `?.` to safely navigate, `??` to provide a fallback.

Declare a `user` object with an optional `nickname?: string` field. Write a function `displayName(user: { name: string; nickname?: string }): string` that returns the nickname if it exists, falling back to the name — using `??`. Then call it with and without a nickname set.

## 2. Control Flow

> `if`, `else`, comparisons. Same idea as Python, different syntax.

### 2.1

TypeScript `if/else` uses `{}` to delimit blocks instead of indentation. Python's `elif` becomes `else if`:

```ts
// Python:            # TypeScript:
# if x > 0:          if (x > 0) {
#     print("+")        console.log("+");
# elif x < 0:        } else if (x < 0) {
#     print("-")        console.log("-");
# else:              } else {
#     print("0")        console.log("0");
                     }
```

Write an `if/else if/else` that checks whether a number is positive, negative, or zero and prints a message for each case.

### 2.2

Python uses `==` for equality. TypeScript has two operators, and they behave very differently:

```ts
console.log(1 == "1");   // true  — == coerces types before comparing
console.log(1 === "1");  // false — === checks value AND type, no coercion
console.log(0 == false); // true
console.log(0 === false);// false
```

Always use `===` in TypeScript. Write two examples that show a case where `==` returns `true` but `===` returns `false`. Add a comment explaining why `===` is safer.

### 2.3

The **ternary operator** is a one-line if/else. Python and TypeScript both have it, but the syntax differs:

```ts
// Python: "positive" if x > 0 else "non-positive"
// TypeScript:
const label = x > 0 ? "positive" : "non-positive";
//                   ^             ^
//               if true       if false
```

Rewrite your exercise 2.1 solution as a single ternary expression assigned to a variable. Print the result.

### 2.4

The `switch` statement matches a value against a list of cases. Each case needs a `break` to stop — without it, execution falls through into the next case:

```ts
switch (status) {
  case "active":
    console.log("User is active");
    break;
  case "inactive":
    console.log("User is inactive");
    break;
  default:
    console.log("Unknown status");
}
```

Write a `switch` for a `status` variable that can be `"active"`, `"inactive"`, or `"banned"`, with a different message for each. Then deliberately remove one `break` and observe what falls through.

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

The classic C-style `for` loop uses an index variable. Python doesn't have this — it's new syntax:

```ts
const nums = [10, 20, 30, 40, 50];

for (let i = 0; i < nums.length; i++) {
  console.log(nums[i]);
}
// three parts: initialise; condition (keep going while true); step after each iteration
```

Declare an array of five numbers. Write a `for` loop using an index variable to print each one.

### 3.2

`for...of` is the TypeScript equivalent of Python's `for x in list` — it gives you the values directly:

```ts
for (const fruit of ["apple", "banana", "cherry"]) {
  console.log(fruit); // "apple", "banana", "cherry"
}
```

`for...in` looks similar but gives you the **keys** (indices as strings), not the values:

```ts
for (const i in ["apple", "banana", "cherry"]) {
  console.log(i); // "0", "1", "2"  — strings, not numbers
}
```

Write both loops on the same array. Add a comment explaining when you would use each — and why `for...in` on an array is almost never what you want.

### 3.3

`while` runs as long as a condition is true. Use `break` to exit early:

```ts
let count = 10;
while (count > 0) {
  console.log(count);
  count--; // count-- is shorthand for count = count - 1
}
```

Write a `while` loop that counts down from 10 to 1. Then add a `break` that stops it early when the count reaches 5. Confirm only 10–6 prints.

### 3.4

Recreate this Python snippet in TypeScript:

```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

TypeScript doesn't have `enumerate`. Figure out how to get both the index and the value — you can use the C-style for loop from 3.1, or look up the `.entries()` array method.

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

TypeScript has two ways to write a function. The `function` keyword is the classic form. Arrow functions are a shorter syntax used heavily in modern code:

```ts
// function keyword — Python's "def" equivalent
function add(a: number, b: number): number {
  return a + b;
}

// arrow function — assigned to a const
const add = (a: number, b: number): number => {
  return a + b;
};

// arrow function shorthand — single expression, no return keyword needed
const add = (a: number, b: number): number => a + b;
```

Write a function using the `function` keyword that takes an array of numbers and returns their product. Then rewrite it as an arrow function using `.reduce()`. Both should produce the same output when called.

### 4.2

Template literals are TypeScript's equivalent of Python f-strings. They use backticks and `${}` for interpolation:

```ts
const name = "Alice";
const age = 30;

// Python: f"Hello {name}, you are {age} years old"
const message = `Hello ${name}, you are ${age} years old`;
```

Write a function `greet(name: string): string` that returns a personalised greeting using a template literal. The parameter type goes after a colon; the return type goes after the closing parenthesis:

```ts
function greet(name: string): string {
  // your code here
}
```

### 4.3

A parameter marked with `?` is optional — the caller can omit it, in which case it will be `undefined` inside the function:

```ts
function formatName(first: string, last?: string): string {
  if (last) {
    return `${first} ${last}`;
  }
  return first;
}

formatName("Alice");          // "Alice"
formatName("Alice", "Smith"); // "Alice Smith"
```

Write a function `buildEmail(username: string, domain?: string): string` that returns `username@domain` if a domain is provided, or just `username` if not.

### 4.4

Default parameters are set in the function signature. If the caller omits the argument, the default is used:

```ts
function repeat(text: string, times: number = 3): string {
  return text.repeat(times);
}

repeat("ha");    // "hahaha"
repeat("ha", 5); // "hahahahaha"
```

Write a function `padStart(text: string, width: number = 10, char: string = " "): string` that pads the string on the left to reach the given width. Call it with one, two, and three arguments to confirm all three defaults work.

### 4.5

Functions can return different types using a union return type. The calling code must handle both possibilities:

```ts
function divide(a: number, b: number): number | null {
  if (b === 0) return null;
  return a / b;
}

const result = divide(10, 2);
if (result === null) {
  console.log("Cannot divide by zero");
} else {
  console.log(result);
}
```

Write a function `findFirst(arr: string[], target: string): number | null` that returns the index of the first match, or `null` if not found. Write calling code that handles both cases.

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

### 6.7

`Record<Keys, Type>` constructs an object type where every key is `Keys` and every value is `Type`. It is cleaner than writing an index signature by hand and gives you autocomplete on the keys when they are a union:

```ts
type Role = "admin" | "editor" | "viewer";

const permissions: Record<Role, string[]> = {
  admin:  ["read", "write", "delete"],
  editor: ["read", "write"],
  viewer: ["read"],
};
// Forgetting a key ("viewer") is a compiler error — Record enforces all keys are present
```

It also works as a plain lookup map when the keys are not known upfront:

```ts
const wordCount: Record<string, number> = {};
wordCount["hello"] = 1;
```

Write a `Record<string, number>` that maps HTTP status codes (as strings) to their descriptions. Then write a function `describe(code: string): string` that looks up the code and returns `"Unknown status"` if it is not in the map.

Then define a union type `Direction = "north" | "south" | "east" | "west"` and create a `Record<Direction, [number, number]>` that maps each direction to an `[x, y]` coordinate delta. Try adding a key that is not in the union — confirm the compiler rejects it.

### 6.8 — Challenge

Define interfaces for a simple order system:

- `Customer`: id, name, email
- `OrderItem`: productId, productName, quantity, unitPrice
- `Order`: id, customer, items (array of OrderItem), status (`"pending" | "shipped" | "delivered"`)

Write a function `orderTotal(order: Order): number` that returns the total cost across all items.

Write another function `orderSummary(order: Order): string` that returns a formatted summary including the customer name, item count, total, and status.

## 7. Classes and OOP

> Python has classes too, so the concepts are familiar. The differences are mostly syntax and the fact that TypeScript enforces access control at compile time — Python only has naming conventions for it.

**Reference:** [Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html)

### 7.1

Write a basic class with a constructor and a method:

```ts
class Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  speak(): string {
    return `${this.name} makes a sound.`;
  }
}

const a = new Animal("Cat");
console.log(a.speak());
```

Compare to Python's `__init__(self, name)` and `self.name`. The shape is the same — TypeScript just requires you to declare properties before the constructor.

Create two more instances and call the method on each.

### 7.2

TypeScript has **access modifiers**: `public`, `private`, and `protected`.

- `public` — accessible from anywhere (the default)
- `private` — only accessible inside the class
- `protected` — accessible inside the class and subclasses

Add a private property `#sound` to `Animal` and a public method that uses it:

```ts
class Animal {
  name: string;
  private sound: string;

  constructor(name: string, sound: string) {
    this.name = name;
    this.sound = sound;
  }

  speak(): string {
    return `${this.name} says ${this.sound}.`;
  }
}
```

Try accessing `a.sound` directly from outside the class. Read the compiler error. This is enforced at compile time — Python's `_underscore` convention is just a hint.

### 7.3

TypeScript has a shorthand for declaring and assigning constructor parameters at the same time. These two are identical:

```ts
// Long form
class Point {
  x: number;
  y: number;
  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

// Shorthand — put the modifier in the constructor parameter
class Point {
  constructor(public x: number, public y: number) {}
}
```

Rewrite `Animal` using the shorthand. Then confirm everything still works.

### 7.4

Classes can **extend** other classes. The subclass inherits all public and protected members and can override methods.

```ts
class Dog extends Animal {
  breed: string;

  constructor(name: string, breed: string) {
    super(name, "woof");
    this.breed = breed;
  }

  speak(): string {
    return `${super.speak()} (${this.breed})`;
  }
}
```

- `super(...)` calls the parent constructor — required before you can use `this` in a subclass
- `super.speak()` calls the parent method

Create a `Dog` and a `Cat` class that both extend `Animal`. Give each a different override of `speak()`. Create instances of both and call `speak()`.

### 7.5

A class can **implement** an interface. This means the compiler enforces that the class has all the required properties and methods.

```ts
interface Shape {
  area(): number;
  perimeter(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}

  area(): number {
    return this.width * this.height;
  }

  perimeter(): number {
    return 2 * (this.width + this.height);
  }
}
```

Create a `Circle` class that also implements `Shape`. Then write a function `describeShape(shape: Shape): void` that prints the area and perimeter. Call it with both a `Rectangle` and a `Circle` — the function doesn't need to know which one it is.

### 7.6

**Readonly** properties can be set in the constructor but not changed afterwards. **Static** members belong to the class itself, not instances.

```ts
class Config {
  static readonly MAX_RETRIES = 3;
  readonly createdAt: string;

  constructor() {
    this.createdAt = new Date().toISOString();
  }
}

console.log(Config.MAX_RETRIES); // accessed on the class, not an instance
```

Try reassigning `createdAt` after construction. Confirm the compiler rejects it.

Add a static method `Config.default()` that returns a `new Config()`. Call it without constructing a `Config` manually.

### 7.7

**Getters and setters** let you run logic when a property is read or written, while keeping the interface looking like a plain property access:

```ts
class Temperature {
  private _celsius: number;

  constructor(celsius: number) {
    this._celsius = celsius;
  }

  get fahrenheit(): number {
    return this._celsius * 9 / 5 + 32;
  }

  set celsius(value: number) {
    if (value < -273.15) throw new Error("Below absolute zero");
    this._celsius = value;
  }
}

const t = new Temperature(100);
console.log(t.fahrenheit); // called like a property, not t.fahrenheit()
t.celsius = 0;
```

Write a `BankAccount` class with:
- A private `_balance: number` property
- A getter `balance` that returns it
- A `deposit(amount: number)` method that adds to the balance
- A `withdraw(amount: number)` method that throws if the balance would go negative

### 7.8 — Challenge

An **abstract class** defines methods that subclasses must implement, but cannot be instantiated directly.

```ts
abstract class Notification {
  abstract message(): string;

  send(): void {
    console.log(`Sending: ${this.message()}`);
  }
}
```

Design an abstract class `Report` with:
- An abstract method `generate(): string`
- A concrete method `export(format: "json" | "csv"): void` that calls `generate()` and wraps the output appropriately

Create two concrete subclasses — `SalesReport` and `InventoryReport` — each with their own `generate()` implementation. Call `export()` on instances of both.

## 8. Generics

> Python 3.12 has `TypeVar` for this. TypeScript generics do the same job: write one function or class that works across many types, without losing type safety.

**Reference:** [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)

### 8.1

A generic function uses a **type parameter** — a placeholder that gets filled in at the call site.

```ts
function identity<T>(value: T): T {
  return value;
}

const a = identity(42);       // T is inferred as number
const b = identity("hello");  // T is inferred as string
```

Without generics you'd have to write `identity(value: any)` and lose all type information. With generics, the return type is the same as the input type — the compiler knows that.

Write a generic function `firstItem<T>(arr: T[]): T | null` that returns the first element of an array, or `null` if the array is empty. Call it with a `string[]` and a `number[]`.

### 8.2

Type parameters can be **constrained** with `extends`. This restricts which types can be passed in.

```ts
function getLength<T extends { length: number }>(value: T): number {
  return value.length;
}

getLength("hello");    // string has .length
getLength([1, 2, 3]);  // array has .length
getLength(42);         // error — number has no .length
```

Write a function `maxValue<T extends number | string>(a: T, b: T): T` that returns whichever argument is larger. The constraint ensures only comparable types can be passed.

### 8.3

Interfaces can be generic too.

```ts
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}
```

Use this to type two different responses without duplicating the wrapper fields:

- `ApiResponse<User>` — where `User` has `id` and `name`
- `ApiResponse<Product[]>` — where `Product` has `id`, `name`, and `price`

Write a function `unwrap<T>(response: ApiResponse<T>): T` that returns `response.data`. Call it on both response types.

### 8.4

Classes can also take type parameters.

```ts
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  get size(): number {
    return this.items.length;
  }
}

const stack = new Stack<number>();
stack.push(1);
stack.push(2);
console.log(stack.pop()); // 2
```

Create a `Stack<string>` and a `Stack<number>`. Try pushing the wrong type into each — confirm the compiler rejects it.

### 8.5

Several types you have already used are generic under the hood:

```ts
const nums: Array<number> = [1, 2, 3];    // same as number[]
const map = new Map<string, number>();
map.set("a", 1);

const set = new Set<string>();
set.add("hello");
```

Write a function `groupBy<T>(items: T[], key: keyof T): Map<T[keyof T], T[]>` that groups an array of objects by a given key. Test it by grouping an array of `{ name: string; role: string }` objects by `"role"`.

> `keyof T` is a type that represents any valid key of `T`. You will see this pattern constantly in real codebases.

### 8.6 — Challenge

Write a generic `Result<T>` type that represents either a success value or an error — similar to Rust's `Result` or Python's pattern of returning `(value, error)` tuples.

Model it as a discriminated union:

```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };
```

Write these utilities:
- `ok<T>(value: T): Result<T>` — wraps a success value
- `err<T>(message: string): Result<T>` — wraps an error
- `map<T, U>(result: Result<T>, fn: (value: T) => U): Result<U>` — applies a function to the value if it succeeded, passes the error through if it failed

Test all three by simulating a function that might fail (e.g. parsing a number from a string).

## 9. Modules and Imports/Exports

> Python uses `import module` and `from module import name`. TypeScript has the same idea but with two distinct export styles — named and default — and a few extra tools for working with types specifically.

**Reference:** [Modules](https://www.typescriptlang.org/docs/handbook/2/modules.html)

### 9.1

Create two files in your `ts-exercises` folder: `maths.ts` and `main.ts`.

In `maths.ts`, use **named exports**:

```ts
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export const PI = 3.14159;
```

In `main.ts`, import them by name:

```ts
import { add, subtract, PI } from "./maths";

console.log(add(2, 3));
console.log(PI);
```

Run with `tsx main.ts`. You can import only what you need — if you only import `add`, `subtract` and `PI` are not included.

### 9.2

A **default export** is the one main thing a file exports. A file can have at most one.

Create `greeter.ts`:

```ts
export default function greet(name: string): string {
  return `Hello, ${name}!`;
}
```

Import it in `main.ts`:

```ts
import greet from "./greeter";

console.log(greet("Alice"));
```

Default imports have no curly braces, and you can name them whatever you like on the import side. Named imports must match exactly (or be renamed — see next exercise).

### 9.3

You can rename any import using `as`:

```ts
import { add as sum } from "./maths";
import greet as sayHello from "./greeter"; // default import, renamed

console.log(sum(1, 2));
```

This is useful when two modules export something with the same name, or when the exported name conflicts with a local variable.

You can also import everything from a module into a namespace object:

```ts
import * as Maths from "./maths";

console.log(Maths.add(1, 2));
console.log(Maths.PI);
```

Try both patterns in `main.ts`.

### 9.4

As projects grow, you'll have many modules. A **barrel file** (`index.ts`) re-exports everything from a folder so consumers import from one place instead of many:

```
utils/
  index.ts
  maths.ts
  strings.ts
```

In `utils/index.ts`:

```ts
export { add, subtract, PI } from "./maths";
export { capitalise, truncate } from "./strings";
```

In `main.ts`:

```ts
import { add, capitalise } from "./utils";
```

Create a `utils/` folder with at least two utility files. Write a barrel `index.ts` that re-exports from both. Import from `"./utils"` in `main.ts` — confirm it works.

### 9.5

When you only need a type at compile time (not at runtime), use `import type`. This guarantees the import is erased entirely from the compiled output and avoids circular dependency issues.

```ts
import type { User } from "./types";

function greetUser(user: User): string {
  return `Hello, ${user.name}`;
}
```

Create a `types.ts` file with interface definitions only. Import them with `import type` wherever you use them as type annotations. Import them with a regular `import` in a file that actually constructs instances — observe that both work but serve different purposes.

### 9.6 — Challenge

Take your task manager from the final exercise (or any multi-function file you have written) and split it across modules:

```
task-manager/
  types.ts       — interfaces and type aliases only
  tasks.ts       — functions that operate on tasks
  users.ts       — functions that operate on users
  index.ts       — barrel that re-exports everything
  main.ts        — demo script, imports from ./index
```

Rules:
- `types.ts` must use only `export type` / `export interface` — no runtime values
- `main.ts` must only import from `"./index"`, not from the individual modules
- No `any`

Run `tsx main.ts` and confirm the output is identical to the original single-file version.

## 10. Error Handling

> Python uses `try / except`. TypeScript uses `try / catch / finally`. The concepts are the same — the main TypeScript-specific twist is that the caught value is typed as `unknown`, not `Error`, so you have to narrow it before using it.

**Reference:** [Error Handling](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)

### 10.1

Basic `try / catch / finally`:

```ts
try {
  const data = JSON.parse('{ bad json }');
} catch (err) {
  console.log("Something went wrong");
} finally {
  console.log("This always runs, even if there was no error");
}
```

- `catch` runs only if an error is thrown inside `try`
- `finally` always runs — use it for cleanup (closing files, releasing locks)

Write a function `parseNumber(input: string): number` that uses `parseInt`, detects when the result is `NaN`, throws an `Error` with a descriptive message, and is called inside a `try / catch` that prints the error message on failure.

### 10.2

In TypeScript, the value caught in a `catch` block is typed as `unknown` — not `Error`. This is intentional: anything can be thrown (`throw "oops"`, `throw 42`), so the compiler can't assume you have an `Error` object.

You must narrow it before accessing properties:

```ts
try {
  throw new Error("something failed");
} catch (err) {
  if (err instanceof Error) {
    console.log(err.message); // safe — narrowed to Error
    console.log(err.stack);
  } else {
    console.log("Unknown error:", err);
  }
}
```

Update the `catch` from exercise 10.1 to use `instanceof Error` narrowing. Then add a second call that throws a plain string instead of an `Error` — confirm the `else` branch handles it.

### 10.3

You can create custom error classes by extending `Error`. This lets callers distinguish between different failure types using `instanceof`:

```ts
class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field: string
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

class NotFoundError extends Error {
  constructor(public readonly id: number) {
    super(`Resource ${id} not found`);
    this.name = "NotFoundError";
  }
}
```

Write a function `findUser(id: number): { id: number; name: string }` that throws a `NotFoundError` for unknown ids. Call it inside a `try / catch` that handles `NotFoundError` and generic `Error` separately, printing a different message for each.

### 10.4

`finally` is useful for cleanup that must happen regardless of success or failure:

```ts
function riskyOperation(): void {
  console.log("acquiring resource");
  try {
    throw new Error("something went wrong mid-operation");
  } finally {
    console.log("releasing resource"); // runs even though an error was thrown
  }
}

try {
  riskyOperation();
} catch (err) {
  console.log("caught:", err instanceof Error ? err.message : err);
}
```

Run this and read the output order carefully. Notice that `finally` runs before the `catch` in the outer block sees the error.

Write your own example: a function that "opens a connection" (just a `console.log`), does something that might throw, and always "closes the connection" in `finally`.

### 10.5 — Challenge

Combine error handling with the `Result<T>` type from section 8.6. Write a wrapper function `tryCatch<T>(fn: () => T): Result<T>` that runs `fn` inside a `try / catch` and returns either `ok(value)` or `err(message)` — so callers never have to write `try / catch` themselves:

```ts
const result = tryCatch(() => JSON.parse(userInput));

if (result.ok) {
  console.log("Parsed:", result.value);
} else {
  console.log("Failed:", result.error);
}
```

Then write a version `tryCatchAsync<T>(fn: () => Promise<T>): Promise<Result<T>>` that handles async functions. You will need to look up how `async / await` interacts with `try / catch`.

## 11. Putting It Together

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
- [ ] Can use `??` and `?.` and explain why `??` is safer than `||` for optional values
- [ ] Can write both regular functions and arrow functions with full type annotations
- [ ] Know the difference between `for...of` and `for...in`
- [ ] Can use `.map()`, `.filter()`, and `.reduce()` without looking them up
- [ ] Can define an interface and use it across multiple functions
- [ ] Can use `Record<Keys, Type>` for lookup maps and union-keyed objects
- [ ] Understand optional properties and union types
- [ ] Can write a class with a constructor, typed properties, and methods
- [ ] Understand `public`, `private`, and `protected` and how they differ from Python conventions
- [ ] Can extend a class and call `super()` correctly
- [ ] Can implement an interface in a class and write functions that accept the interface type
- [ ] Know when to use `readonly` and `static`
- [ ] Can write getters and setters
- [ ] Can write a generic function with a type parameter and explain why it is better than `any`
- [ ] Can constrain a type parameter with `extends`
- [ ] Can write a generic interface and a generic class
- [ ] Know the difference between named exports and default exports
- [ ] Can rename imports with `as` and import an entire module as a namespace
- [ ] Can create a barrel `index.ts` that re-exports from multiple modules
- [ ] Know when to use `import type` instead of `import`
- [ ] Can split a multi-function file into a properly structured module folder
- [ ] Can write `try / catch / finally` and explain what each block does
- [ ] Understand why caught errors are typed `unknown` and can narrow them with `instanceof`
- [ ] Can create a custom error class by extending `Error`
- [ ] Completed the final exercise with no `any` types
