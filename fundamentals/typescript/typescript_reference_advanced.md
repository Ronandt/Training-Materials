# TypeScript Advanced Reference

Quick reference for TypeScript features beyond the tutorial. Each entry shows what it does, the syntax, and a real example. This is for lookup, not step-by-step learning.

**Official docs:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) · [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)

---

## Utility Types

Utility types are built into TypeScript — no imports needed. They transform existing types into new ones.

---

### `Partial<Type>`
*Added: 2.1*

Makes every property in `Type` optional. Useful when you want to accept a subset of a type, e.g. update payloads.

```ts
interface User {
  id: number;
  name: string;
  email: string;
}

function updateUser(id: number, changes: Partial<User>): void {
  // changes can have any combination of User's fields
}

updateUser(1, { name: "Alice" });          // fine
updateUser(1, { name: "Alice", email: "a@b.com" }); // fine
```

---

### `Required<Type>`
*Added: 2.8*

The opposite of `Partial` — makes every property required, even ones originally marked optional.

```ts
interface Config {
  host?: string;
  port?: number;
  debug?: boolean;
}

type StrictConfig = Required<Config>;
// { host: string; port: number; debug: boolean }

const cfg: StrictConfig = { host: "localhost", port: 3000, debug: false };
```

---

### `Readonly<Type>`
*Added: 2.1*

Makes every property read-only. Assignments after construction are a compiler error.

```ts
interface Point {
  x: number;
  y: number;
}

const origin: Readonly<Point> = { x: 0, y: 0 };
origin.x = 1; // error: cannot assign to 'x' because it is a read-only property
```

Useful for configuration objects and constants you want to protect from accidental mutation.

---

### `Pick<Type, Keys>`
*Added: 2.1*

Constructs a new type with only the specified keys from `Type`.

```ts
interface Todo {
  title: string;
  description: string;
  completed: boolean;
  createdAt: number;
}

type TodoPreview = Pick<Todo, "title" | "completed">;
// { title: string; completed: boolean }

const preview: TodoPreview = { title: "Clean room", completed: false };
```

---

### `Omit<Type, Keys>`
*Added: 3.5*

The opposite of `Pick` — constructs a type with all properties from `Type` **except** the specified keys.

```ts
interface Todo {
  title: string;
  description: string;
  completed: boolean;
  createdAt: number;
}

type TodoPreview = Omit<Todo, "description">;
// { title: string; completed: boolean; createdAt: number }

type TodoInfo = Omit<Todo, "completed" | "createdAt">;
// { title: string; description: string }
```

Use `Omit` when a type is mostly right but has one or two fields you don't want to expose (e.g. stripping `id` or `createdAt` from a creation payload).

---

### `Exclude<UnionType, ExcludedMembers>`
*Added: 2.8*

Removes specific members from a union type.

```ts
type Status = "active" | "inactive" | "banned" | "deleted";

type VisibleStatus = Exclude<Status, "deleted">;
// "active" | "inactive" | "banned"

type T = Exclude<string | number | boolean, boolean>;
// string | number
```

---

### `Extract<Type, Union>`
*Added: 2.8*

The opposite of `Exclude` — keeps only the members of `Type` that are assignable to `Union`.

```ts
type Mixed = string | number | boolean | null;

type StringOrNumber = Extract<Mixed, string | number>;
// string | number
```

---

### `NonNullable<Type>`
*Added: 2.8*

Removes `null` and `undefined` from a type.

```ts
type MaybeString = string | null | undefined;

type DefiniteString = NonNullable<MaybeString>;
// string

function process(value: string | null | undefined): void {
  const safe: NonNullable<typeof value> = value!; // after a null check
}
```

---

### `ReturnType<Type>`
*Added: 2.8*

Extracts the return type of a function type.

```ts
function fetchUser() {
  return { id: 1, name: "Alice", email: "alice@example.com" };
}

type User = ReturnType<typeof fetchUser>;
// { id: number; name: string; email: string }
```

Useful when you don't control the function's type definition (e.g. a library function) and you need its return type for annotations elsewhere.

---

### `Parameters<Type>`
*Added: 3.1*

Extracts the parameter types of a function as a tuple.

```ts
function createUser(name: string, age: number, admin: boolean): void {}

type CreateUserArgs = Parameters<typeof createUser>;
// [name: string, age: number, admin: boolean]

const args: CreateUserArgs = ["Alice", 30, false];
createUser(...args);
```

---

### `InstanceType<Type>`
*Added: 2.8*

Extracts the instance type of a constructor function (i.e. what `new MyClass()` returns).

```ts
class HttpClient {
  get(url: string) { /* ... */ }
}

type Client = InstanceType<typeof HttpClient>;
// HttpClient

function useClient(client: Client) { /* ... */ }
```

---

## Type Operators

### `keyof`

Produces a union of all keys of a type.

```ts
interface User {
  id: number;
  name: string;
  email: string;
}

type UserKey = keyof User;
// "id" | "name" | "email"

function getField<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
const name = getField(user, "name");  // type: string
const id   = getField(user, "id");    // type: number
```

---

### `typeof` (in type position)

In a type annotation, `typeof` extracts the type of a variable or expression. Different from the runtime `typeof` used in expressions.

```ts
const config = { host: "localhost", port: 3000 };

type Config = typeof config;
// { host: string; port: number }

function applyConfig(cfg: typeof config): void { /* ... */ }
```

---

### Indexed Access Types (`Type[Key]`)

Look up the type of a specific property.

```ts
interface User {
  id: number;
  address: {
    city: string;
    postcode: string;
  };
}

type AddressType = User["address"];
// { city: string; postcode: string }

type CityType = User["address"]["city"];
// string

type UserValues = User[keyof User];
// number | { city: string; postcode: string }
```

---

## Intersection Types

Combines multiple types into one. The result must satisfy all of them. Written with `&`.

```ts
interface HasId   { id: number }
interface HasName { name: string }

type Entity = HasId & HasName;
// { id: number; name: string }

function printEntity(e: Entity): void {
  console.log(e.id, e.name);
}
```

Useful for composing types from smaller pieces, or for mixing a base type with extra fields:

```ts
type AdminUser = User & { permissions: string[] };
```

---

## Mapped Types

Transform every property in a type using a loop-like syntax.

```ts
// Make every property optional (same as Partial<T> — shown for illustration)
type Optional<T> = {
  [K in keyof T]?: T[K];
};

// Make every property nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Make every value a string (same as Record<keyof T, string>)
type Stringify<T> = {
  [K in keyof T]: string;
};
```

The `?` and `readonly` modifiers can be added or removed with `+` / `-`:

```ts
// Remove readonly from every property
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

// Remove optional from every property (same as Required<T>)
type Concrete<T> = {
  [K in keyof T]-?: T[K];
};
```

---

## Template Literal Types

Build string literal types using the same syntax as template literals.

```ts
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"
```

```ts
type HttpMethod = "get" | "post" | "put" | "delete";
type Endpoint   = "/users" | "/posts" | "/comments";
type Route = `${Uppercase<HttpMethod>} ${Endpoint}`;
// "GET /users" | "GET /posts" | ... (12 combinations)
```

Built-in string manipulation types: `Uppercase<S>`, `Lowercase<S>`, `Capitalize<S>`, `Uncapitalize<S>`.

---

## Conditional Types

A type that resolves to one of two options based on a condition. Syntax: `T extends U ? TrueType : FalseType`.

```ts
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false
```

Commonly used with generics:

```ts
type Flatten<T> = T extends Array<infer Item> ? Item : T;

type Str = Flatten<string[]>;  // string
type Num = Flatten<number>;    // number (not an array, passes through)
```

### `infer`

`infer` declares a type variable inside a conditional type that TypeScript fills in from the actual type:

```ts
type UnpackPromise<T> = T extends Promise<infer Value> ? Value : T;

type A = UnpackPromise<Promise<string>>;  // string
type B = UnpackPromise<number>;           // number
```

```ts
type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

type F = FirstArg<(x: string, y: number) => void>;
// string
```

---

## The `satisfies` Operator
*Added: 4.9*

Validates that a value matches a type without widening the inferred type. Lets you get both type checking and precise inference.

```ts
type Palette = Record<string, [number, number, number] | string>;

// Without satisfies — colors is typed as Palette, so colors.red is string | [number, number, number]
const colors: Palette = { red: [255, 0, 0], blue: "#0000ff" };

// With satisfies — TypeScript checks the shape but infers the precise type
const colors = {
  red:  [255, 0, 0],
  blue: "#0000ff",
} satisfies Palette;

colors.red.at(0);   // fine — TypeScript knows red is a tuple, not a string
colors.blue.toUpperCase(); // fine — TypeScript knows blue is a string
```

---

## Type Assertions

Tell the compiler to treat a value as a specific type. Use sparingly — you are overriding the type checker.

```ts
const input = document.getElementById("username") as HTMLInputElement;
input.value; // fine — compiler knows it's an HTMLInputElement, not just HTMLElement | null
```

The non-null assertion `!` asserts that a value is not `null` or `undefined`:

```ts
const el = document.getElementById("app")!; // you are asserting it exists
```

Only use assertions when you know more than the compiler does. If you find yourself using them to silence errors you don't understand, that's a bug.

---

## Declaration Merging

TypeScript merges multiple declarations of the same name. Most commonly used with interfaces (unlike `type`, interfaces can be extended after the fact):

```ts
interface Window {
  analytics: AnalyticsClient;
}

// Now window.analytics is typed everywhere without touching the original lib
```

---

## Discriminated Unions

A union where each member has a shared literal property (the discriminant) that TypeScript uses to narrow:

```ts
type Shape =
  | { kind: "circle";    radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle";  base: number;  height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":    return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    case "triangle":  return 0.5 * shape.base * shape.height;
  }
}
```

If you add a new member to the union and forget to handle it in the switch, the compiler will catch it if your function has an explicit return type.
