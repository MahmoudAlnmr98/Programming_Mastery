# TypeScript — Complete Reference Guide (Zero to Advanced)

> This guide assumes you have read the JavaScript guide. It builds on that foundation and explains every TypeScript concept from WHY it exists, to HOW it works internally, to real-world production patterns. Nothing is skipped.

---

## Table of Contents

1. [What is TypeScript and Why Does it Exist?](#1-what-is-typescript-and-why-does-it-exist)
2. [How TypeScript Works — The Compiler](#2-how-typescript-works--the-compiler)
3. [Basic Types — Complete Coverage](#3-basic-types--complete-coverage)
4. [Type Inference — How TypeScript Guesses Types](#4-type-inference--how-typescript-guesses-types)
5. [Interfaces — Full Guide](#5-interfaces--full-guide)
6. [Type Aliases — Full Guide](#6-type-aliases--full-guide)
7. [Union & Intersection Types](#7-union--intersection-types)
8. [Literal Types & Narrowing](#8-literal-types--narrowing)
9. [Type Guards — Complete Coverage](#9-type-guards--complete-coverage)
10. [Functions in TypeScript](#10-functions-in-typescript)
11. [Classes in TypeScript](#11-classes-in-typescript)
12. [Generics — Complete Guide](#12-generics--complete-guide)
13. [Advanced Types — Every Pattern](#13-advanced-types--every-pattern)
14. [Utility Types — Complete Reference](#14-utility-types--complete-reference)
15. [Mapped Types — Deep Dive](#15-mapped-types--deep-dive)
16. [Conditional Types — Deep Dive](#16-conditional-types--deep-dive)
17. [Template Literal Types](#17-template-literal-types)
18. [Decorators & Metadata](#18-decorators--metadata)
19. [Modules, Namespaces & Declaration Files](#19-modules-namespaces--declaration-files)
20. [The TypeScript Compiler & tsconfig.json](#20-the-typescript-compiler--tsconfigjson)
21. [Structural Typing & Type Compatibility](#21-structural-typing--type-compatibility)
22. [Declaration Merging & Module Augmentation](#22-declaration-merging--module-augmentation)
23. [Enums — Full Coverage](#23-enums--full-coverage)
24. [Symbols & Unique Symbols](#24-symbols--unique-symbols)
25. [Variance — Covariance, Contravariance & Invariance](#25-variance--covariance-contravariance--invariance)
26. [Error Handling Patterns in TypeScript](#26-error-handling-patterns-in-typescript)
27. [TypeScript with Async/Await & Promises](#27-typescript-with-asyncawait--promises)
28. [Production Patterns for Full-Stack TypeScript](#28-production-patterns-for-full-stack-typescript)
29. [TypeScript Configuration for Monorepos](#29-typescript-configuration-for-monorepos)
30. [Common Pitfalls & How to Avoid Them](#30-common-pitfalls--how-to-avoid-them)

---

## 1. What is TypeScript and Why Does it Exist?

### The Problem JavaScript Has at Scale

JavaScript was originally designed for small scripts that added interactivity to web pages. As applications grew to hundreds of thousands of lines and dozens of engineers, several problems emerged:

**Problem 1: Silent property access errors**
```javascript
// JavaScript
function processUser(user) {
  return user.profle.name; // typo: "profle" instead of "profile"
  // This crashes at RUNTIME — you only discover it when it runs
}
```

**Problem 2: Refactoring is terrifying**
```javascript
// You rename a function parameter in JavaScript
// There is NO way to know which other files use it
// You have to search manually and hope you find everything
```

**Problem 3: No documentation about what functions expect**
```javascript
// What does this function expect? A string? An object? Which fields?
function createOrder(userId, items, discount) { ... }
// You have to READ THE BODY to understand — and it might be 200 lines
```

**Problem 4: No autocomplete on custom objects**
```javascript
// IDE can't suggest what properties exist on 'user'
// because it doesn't know the shape at the time you're writing code
user.  // IDE suggests nothing useful
```

### What TypeScript Adds

TypeScript is a **programming language** that:
- Is a **strict superset of JavaScript** — all valid JavaScript is valid TypeScript
- Adds a **type system** that is checked at compile time, not runtime
- **Compiles to plain JavaScript** — browsers and Node.js never see TypeScript
- **Erases all type information** at runtime — zero performance overhead
- Is **structurally typed** (explained in depth later)
- Provides **language server features** — autocomplete, go-to-definition, find-all-references, rename-refactor

```
TypeScript → TypeScript Compiler (tsc) → JavaScript → Browser/Node.js runs
           ↑ Type checking happens here    ↑ Types are gone here
```

### TypeScript is NOT

- Not a different runtime (V8 still runs the code)
- Not slower than JavaScript at runtime
- Not optional "annotations on top of JS" — the type system is deeply integrated
- Not a complete type system like Haskell — it has intentional escape hatches

---

## 2. How TypeScript Works — The Compiler

### The TypeScript Compiler (tsc)

The compiler does three things:
1. **Parses** your TypeScript source into an AST (Abstract Syntax Tree)
2. **Type-checks** the AST, reporting errors
3. **Emits** JavaScript (and optionally declaration files `.d.ts`)

```bash
# Install TypeScript globally
npm install -g typescript

# Compile a file
tsc app.ts

# Watch mode — recompile on changes
tsc --watch

# Use tsconfig.json (project-wide configuration)
tsc

# Type-check only, don't emit JavaScript
tsc --noEmit

# See what TypeScript infers about a specific file
tsc --declaration --emitDeclarationOnly
```

### What Happens to Types at Runtime

```typescript
// TypeScript source
interface User {
  id: number;
  name: string;
}

function greet(user: User): string {
  return `Hello, ${user.name}`;
}

const alice: User = { id: 1, name: "Alice" };
```

```javascript
// Compiled JavaScript output (types COMPLETELY ERASED)
function greet(user) {
  return `Hello, ${user.name}`;
}

const alice = { id: 1, name: "Alice" };
```

The interface `User` and all type annotations are gone. This means:
- You **cannot use types for runtime validation** — use Zod, io-ts, or manual checks
- TypeScript errors are **compile-time only** — they don't prevent code from running if you ignore them
- You can have TypeScript errors and still produce working JavaScript

### Declaration Files (`.d.ts`)

When you want to distribute a TypeScript library (or use an untyped JS library), you use `.d.ts` files — they contain ONLY type information, no JavaScript code.

```typescript
// math.d.ts — pure type information
declare function add(a: number, b: number): number;
declare function subtract(a: number, b: number): number;
declare const PI: number;
```

The `@types/*` packages (like `@types/node`, `@types/react`) are just large collections of `.d.ts` files for popular JavaScript libraries.

---

## 3. Basic Types — Complete Coverage

### Primitive Types

```typescript
// string — text
let firstName: string = "Alice";
let greeting: string = `Hello, ${firstName}`; // template literals work
let empty: string = "";

// number — all numbers (integer, float, hex, octal, binary, NaN, Infinity)
let integer: number = 42;
let float: number = 3.14;
let hex: number = 0xFF;       // 255
let octal: number = 0o377;    // 255
let binary: number = 0b11111111; // 255
let notANumber: number = NaN;
let infinite: number = Infinity;

// boolean
let isActive: boolean = true;
let isDeleted: boolean = false;

// bigint — large integers
let big: bigint = 9007199254740992n;
let alsoBig: bigint = BigInt("9007199254740992");

// symbol
let sym: symbol = Symbol("description");
let unique: unique symbol = Symbol(); // more restrictive, explained later

// null and undefined — type AND value
let nothing: null = null;
let undef: undefined = undefined;
// By default (with strictNullChecks on), null and undefined are their OWN types
// they cannot be assigned to string, number, etc.
```

### `any` — The Escape Hatch

```typescript
// any disables ALL type checking for that variable
let dangerous: any = "hello";
dangerous = 42;           // OK
dangerous = { x: 1 };     // OK
dangerous.anything();      // OK — TypeScript doesn't check this!
dangerous.x.y.z.deep;      // OK — will crash at runtime, TS doesn't care

// When any spreads:
let a: any = "hello";
let b = a.toUpperCase(); // b is ALSO any — the "any cancer"
let c = b.split(",");    // c is ALSO any

// You get any from:
// - Explicit annotation: let x: any
// - Untyped JS libraries (if noImplicitAny is off)
// - JSON.parse() — returns any
// - Functions without return type in some configs
```

### `unknown` — The Safe Alternative to `any`

```typescript
// unknown is like any — accepts any value
// BUT you cannot use it without first narrowing the type
let input: unknown = fetchDataFromSomewhere();

// These would all be ERRORS with unknown:
input.toUpperCase();        // Error: Object is of type 'unknown'
const x = input + 1;        // Error
const y = input as number;  // Allowed but unsafe (type assertion)

// You MUST narrow before using:
if (typeof input === "string") {
  input.toUpperCase();   // OK — now TypeScript knows it's a string
}

if (typeof input === "number") {
  input.toFixed(2);      // OK
}

if (input instanceof Date) {
  input.toISOString();   // OK
}

if (Array.isArray(input)) {
  input.forEach(item => console.log(item)); // OK
}

// unknown is the right type for:
// - JSON.parse() results you haven't validated yet
// - Error catch clauses (catch(e: unknown))
// - Data from external sources (API responses, user input)
// - Generic code that needs to accept any value but be type-safe
```

### `never` — The Bottom Type

```typescript
// never represents a value that NEVER occurs
// It is the "empty type" — no value can ever be of type never

// Function that never returns (throws or infinite loops)
function throwError(message: string): never {
  throw new Error(message);
  // Cannot have any code after throw — the function NEVER returns
}

function infiniteLoop(): never {
  while (true) {
    // never terminates
  }
}

// never in exhaustiveness checking
type Direction = "North" | "South" | "East" | "West";

function handleDirection(d: Direction): string {
  switch (d) {
    case "North": return "Going north";
    case "South": return "Going south";
    case "East":  return "Going east";
    case "West":  return "Going west";
    default:
      // If you added a new direction to the union but forgot to handle it,
      // d would NOT be 'never' here, causing a type error
      const exhaustiveCheck: never = d; // This line catches missing cases!
      throw new Error(`Unhandled direction: ${exhaustiveCheck}`);
  }
}

// never in conditional types (explained later)
// never is the "nothing" result when a condition matches nothing

// never is a SUBTYPE of every type
// This means:
let n: never;
let s: string = n; // OK — never is assignable to anything
// But nothing is assignable TO never (except never itself)
```

### `void` — The "I Don't Care About the Return Value" Type

```typescript
// void means the function returns nothing useful
// (returns undefined or nothing)
function logMessage(msg: string): void {
  console.log(msg);
  // implicitly returns undefined
}

// void vs never:
// void = function CAN return (it returns undefined)
// never = function CANNOT return (throws or loops forever)

// void in callbacks — common pattern
const arr = [1, 2, 3];
arr.forEach((item: number): void => {
  console.log(item); // return value ignored
});

// Interesting: a function typed as () => void CAN return a value
// TypeScript just ignores the return value
type Callback = () => void;
const cb: Callback = () => "hello"; // OK — return value is discarded
```

### Arrays and Tuples

```typescript
// Array types — two equivalent syntaxes
let nums: number[] = [1, 2, 3];
let strs: Array<string> = ["a", "b", "c"];
let matrix: number[][] = [[1, 2], [3, 4]]; // 2D array
let mixed: (string | number)[] = [1, "two", 3]; // union element type

// Readonly arrays — cannot be mutated
let readonlyArr: readonly number[] = [1, 2, 3];
// readonlyArr.push(4); // Error: Property 'push' does not exist on type 'readonly number[]'
let alsoReadonly: ReadonlyArray<number> = [1, 2, 3]; // same

// Tuple — fixed-length array with SPECIFIC TYPES at EACH POSITION
let point: [number, number] = [3, 4];
let rgb: [number, number, number] = [255, 128, 0];
let entry: [string, number, boolean] = ["Alice", 30, true];

// Accessing tuple elements — TypeScript knows the exact type at each index
let x = point[0]; // type: number
let y = point[1]; // type: number
// let z = point[2]; // Error: Tuple type '[number, number]' has no element at index 2

// Named tuples (TypeScript 4.0+) — for documentation
let coordinate: [latitude: number, longitude: number] = [48.8566, 2.3522];
let range: [start: number, end: number] = [0, 100];
// Names are ONLY for documentation — they don't change behavior

// Optional tuple elements
let optionalTuple: [string, number?] = ["hello"]; // second is optional
let alsoOptional: [string, number?] = ["hello", 42]; // or with value

// Rest elements in tuples
type StringsAndNumber = [...string[], number]; // any strings, then a number
const valid: StringsAndNumber = ["a", "b", "c", 42]; // OK
const alsoValid: StringsAndNumber = [42]; // OK
// const invalid: StringsAndNumber = [42, "a"]; // Error

// Readonly tuple
let immutablePoint: readonly [number, number] = [3, 4];
// immutablePoint[0] = 5; // Error
```

### Object Types

```typescript
// Inline object type annotation
let user: { name: string; age: number; email?: string } = {
  name: "Alice",
  age: 30
  // email is optional
};

// Object type with methods
let calculator: {
  add: (a: number, b: number) => number;
  subtract(a: number, b: number): number; // alternative syntax
} = {
  add: (a, b) => a + b,
  subtract: (a, b) => a - b
};

// Readonly properties in object type
let config: { readonly host: string; readonly port: number } = {
  host: "localhost",
  port: 3000
};
// config.host = "other"; // Error: Cannot assign to 'host' because it is a read-only property

// Index signatures — for objects with dynamic keys
type StringMap = { [key: string]: string };
const headers: StringMap = {
  "Content-Type": "application/json",
  "Authorization": "Bearer token"
};

type NumberMap = { [key: string]: number };
const scores: NumberMap = { alice: 95, bob: 87 };
```

---

## 4. Type Inference — How TypeScript Guesses Types

TypeScript can infer types without you explicitly writing them. Understanding inference reduces annotation noise.

### Variable Inference

```typescript
// TypeScript infers the type from the initial value
let name = "Alice";      // inferred: string
let count = 42;           // inferred: number
let active = true;         // inferred: boolean
let nothing = null;        // inferred: null (with strict mode)
let items = [1, 2, 3];    // inferred: number[]
let mixed = [1, "two"];   // inferred: (string | number)[]
let obj = { x: 1, y: 2 }; // inferred: { x: number; y: number }

// const creates NARROWER (literal) types
const pi = 3.14159;        // inferred: 3.14159 (literal type), NOT number
const status = "active";   // inferred: "active" (literal type), NOT string
const point = { x: 1, y: 2 }; // inferred: { x: number; y: number }
// Note: object properties are NOT inferred as literals — they can be changed
// To get literal types on object properties, use 'as const':
const frozenPoint = { x: 1, y: 2 } as const;
// frozenPoint: { readonly x: 1; readonly y: 2 }
```

### Function Return Type Inference

```typescript
// TypeScript infers return types from the function body
function add(a: number, b: number) {
  return a + b; // inferred return: number
}

function greet(name: string) {
  return `Hello, ${name}`; // inferred return: string
}

function getUser(id: number) {
  if (id === 1) return { name: "Alice", id: 1 }; // inferred return
  return null; // inferred return: { name: string; id: number } | null
}

// When to annotate return types explicitly:
// 1. Complex functions where you want to document the contract
// 2. When you want TypeScript to catch if you accidentally return the wrong type
// 3. Recursive functions (inference can't handle them)
// 4. Public API functions (clarity for consumers)
function calculateTax(income: number, rate: number): number { // explicit
  return income * rate;
}
```

### Contextual Typing

TypeScript can infer types from context — the position a value appears in.

```typescript
// TypeScript knows the array is number[] from context
[1, 2, 3].forEach((item) => {
  // TypeScript infers 'item' is number from the array type
  item.toFixed(2); // OK — TypeScript knows item is number
});

// Event handlers — TypeScript knows the event type from context
const button = document.querySelector("button")!;
button.addEventListener("click", (event) => {
  // TypeScript infers event is MouseEvent from context
  console.log(event.clientX); // OK
  console.log(event.clientY); // OK
});

// Callbacks in typed functions
interface DataProcessor {
  process: (data: string) => number;
}
const processor: DataProcessor = {
  process: (data) => data.length // TypeScript knows data is string, return is number
};
```

### Type Widening and Narrowing

```typescript
// Widening — TypeScript makes types less specific for mutation
let x = "hello"; // widened to: string (not "hello"), because let can be reassigned
const y = "hello"; // stays as: "hello" (literal), because const can't be reassigned

// Control widening with 'as const'
let colors = ["red", "green", "blue"] as const;
// Type: readonly ["red", "green", "blue"] — tuple, not string[]

// Widening through union inference
let value = Math.random() > 0.5 ? "hello" : 42;
// TypeScript infers: string | number

// Object widening
function getUserConfig() {
  return {
    theme: "dark",  // string (widened from "dark")
    fontSize: 16    // number (widened from 16)
  };
}
// Return type: { theme: string; fontSize: number }

// Prevent widening with as const
function getUserConfigConst() {
  return {
    theme: "dark",
    fontSize: 16
  } as const;
}
// Return type: { readonly theme: "dark"; readonly fontSize: 16 }
```

---

## 5. Interfaces — Full Guide

An `interface` in TypeScript is a named contract that describes the shape of an object.

### Defining Interfaces

```typescript
// Basic interface
interface User {
  id: number;
  name: string;
  email: string;
}

// Optional properties — use ?
interface CreateUserRequest {
  name: string;
  email: string;
  role?: "admin" | "user"; // optional — may be absent
  age?: number;
}

// Readonly properties — cannot be changed after creation
interface DatabaseConfig {
  readonly host: string;
  readonly port: number;
  readonly database: string;
  maxConnections?: number; // mutable, optional
}

// Using the interface
const config: DatabaseConfig = {
  host: "localhost",
  port: 5432,
  database: "mydb"
};
// config.host = "other"; // Error: Cannot assign to 'host' — it's readonly

// Method signatures in interfaces
interface Calculator {
  // Method signature syntax
  add(a: number, b: number): number;
  // Function property syntax (equivalent)
  subtract: (a: number, b: number) => number;
  // Optional method
  multiply?(a: number, b: number): number;
}

// Call signature — for callable objects
interface Formatter {
  (value: number): string; // this interface describes a function
  prefix: string;          // that also has properties
  version: number;
}

// Construct signature — for classes/constructors
interface StringConstructor {
  new(value: string): String;
}

// Index signatures
interface StringDictionary {
  [key: string]: string; // any string key maps to a string value
  length: number;        // also has a specific 'length' property
  // BUT: all specific properties must be compatible with the index signature
  // (length: number is NOT compatible with [key: string]: string — Error!)
}

// Correct way to mix index signatures and specific properties
interface Mixed {
  [key: string]: string | number; // index signature allows string OR number
  count: number;    // OK — number is assignable to string | number
  name: string;     // OK — string is assignable to string | number
}
```

### Extending Interfaces

```typescript
interface Animal {
  name: string;
  age: number;
}

interface Pet extends Animal {
  owner: string;
}

// Multiple inheritance in interfaces
interface Shape {
  color: string;
}

interface Position {
  x: number;
  y: number;
}

interface ColoredShape extends Shape, Position {
  area(): number;
}

// Using it
const circle: ColoredShape = {
  color: "red",
  x: 0,
  y: 0,
  area: () => Math.PI * 5 ** 2
};

// Extending with modifications
interface BaseResponse {
  success: boolean;
  timestamp: Date;
}

interface UserResponse extends BaseResponse {
  data: {
    user: User;
  };
}

interface ErrorResponse extends BaseResponse {
  success: false; // narrowed from boolean to the literal false
  error: {
    code: string;
    message: string;
  };
}
```

### Declaration Merging with Interfaces

This is a unique feature of `interface` — multiple declarations with the same name are MERGED.

```typescript
// This is intentional and useful for extending third-party types
interface Window {
  myPlugin: { initialize(): void };
}

// Now TypeScript knows window.myPlugin exists
window.myPlugin.initialize(); // OK

// Merging in the same file
interface User {
  id: number;
  name: string;
}

interface User {
  email: string;
}

// Result: User has id, name, AND email
const user: User = { id: 1, name: "Alice", email: "alice@example.com" }; // OK

// This is how @types packages add to existing types
// e.g., Express:
// declare namespace Express {
//   interface Request {
//     user?: AuthenticatedUser;
//   }
// }
```

---

## 6. Type Aliases — Full Guide

A `type alias` gives a name to any type — not just object shapes.

### What Type Aliases Can Do That Interfaces Can't

```typescript
// Primitive type alias
type UserId = number;
type UserName = string;
type IsActive = boolean;

// Union type — impossible with interface
type StringOrNumber = string | number;
type Status = "pending" | "active" | "cancelled" | "completed";
type NullableString = string | null;
type ApiResult<T> = T | null | undefined;

// Intersection type
type WithTimestamps = {
  createdAt: Date;
  updatedAt: Date;
};
type UserWithTimestamps = User & WithTimestamps;

// Tuple type
type Point = [x: number, y: number];
type RGB = [red: number, green: number, blue: number];
type PagedResponse<T> = [data: T[], total: number, page: number];

// Function type
type EventHandler = (event: Event) => void;
type AsyncOperation<T> = (input: string) => Promise<T>;
type Comparator<T> = (a: T, b: T) => number;

// Mapped type
type Optional<T> = { [K in keyof T]?: T[K] };

// Conditional type
type IsString<T> = T extends string ? true : false;

// Template literal type
type EventName = `on${Capitalize<string>}`;

// Recursive type
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// None of these are possible with interface!
```

### When to Use `type` vs `interface`

```
Use interface when:
  - Defining the shape of an object or class contract
  - You expect the type to be extended (either by you or by consumers)
  - You want declaration merging (adding to existing types, module augmentation)
  - Defining public API shapes in a library

Use type when:
  - Union types: type Result = Success | Failure
  - Intersection types: type FullUser = User & Admin
  - Tuple types: type Point = [number, number]
  - Function types: type Handler = (e: Event) => void
  - Utility type transformations: type Optional<T> = { [K in keyof T]?: T[K] }
  - Conditional types
  - Mapped types
  - Template literal types
  - Recursive types
  - Any type that's not purely an object shape
```

---

## 7. Union & Intersection Types

### Union Types (`|`)

A union type says "this value can be ONE of these types." Think of it as OR.

```typescript
// Basic union
type StringOrNumber = string | number;
let value: StringOrNumber;
value = "hello"; // OK
value = 42;       // OK
// value = true; // Error

// Union with null (nullable types)
type NullableUser = User | null;
type MaybeString = string | null | undefined;

// Literal union — extremely useful
type Direction = "North" | "South" | "East" | "West";
type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
type LogLevel = "debug" | "info" | "warn" | "error";

function log(level: LogLevel, message: string): void {
  console.log(`[${level.toUpperCase()}] ${message}`);
}
log("info", "Server started");   // OK
// log("verbose", "Detail"); // Error: "verbose" is not assignable to LogLevel

// Working with union types — you can only use what's COMMON to all members
type StringOrArray = string | number[];

function processValue(val: StringOrArray): number {
  // val.length — OK: both string and array have .length
  return val.length; // Wait — string has length, array has length — both have it!
}

// To use type-specific methods, you must narrow:
function processValue2(val: string | number): string {
  if (typeof val === "string") {
    return val.toUpperCase(); // string method — OK
  }
  return val.toFixed(2); // number method — OK
}
```

### Discriminated Unions (Tagged Unions)

This is one of the most important patterns in TypeScript. Each member has a common literal property (the "discriminant") that uniquely identifies it.

```typescript
// Without discriminated union — hard to work with
type Shape =
  | { radius: number }
  | { width: number; height: number }
  | { base: number; height: number };

// What kind of shape is this? Ambiguous!

// WITH discriminated union — type-safe and clear
type Shape =
  | { kind: "circle";    radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle";  base: number; height: number };

function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      // TypeScript KNOWS shape is { kind: "circle"; radius: number }
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      // TypeScript KNOWS shape is { kind: "rectangle"; width: number; height: number }
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    // TypeScript warns if you don't handle all cases (with noImplicitReturns)
  }
}

// Real-world example: API response states
type ApiState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T; timestamp: Date }
  | { status: "error";   error: Error; retryCount: number };

function renderUserState(state: ApiState<User>) {
  switch (state.status) {
    case "idle":
      return "Click to load";
    case "loading":
      return "Loading...";
    case "success":
      return `Hello, ${state.data.name}`; // state.data is User — typed!
    case "error":
      return `Error: ${state.error.message} (tried ${state.retryCount} times)`;
  }
}

// Exhaustiveness checking — ensure all cases are handled
function assertNever(value: never): never {
  throw new Error(`Unhandled value: ${JSON.stringify(value)}`);
}

function renderUserStateWithExhaustiveness(state: ApiState<User>): string {
  switch (state.status) {
    case "idle":    return "Click to load";
    case "loading": return "Loading...";
    case "success": return `Hello, ${state.data.name}`;
    case "error":   return `Error: ${state.error.message}`;
    default:
      return assertNever(state); // If you forget a case, TypeScript errors here!
  }
}
```

### Intersection Types (`&`)

An intersection combines multiple types into one. Think of it as AND — the result has ALL properties of ALL types.

```typescript
interface HasId {
  id: string;
}

interface HasTimestamps {
  createdAt: Date;
  updatedAt: Date;
}

interface HasSoftDelete {
  deletedAt: Date | null;
}

// Combine all of them
type DatabaseEntity = HasId & HasTimestamps & HasSoftDelete;
// Result has: id, createdAt, updatedAt, deletedAt

type User = DatabaseEntity & {
  name: string;
  email: string;
  role: "admin" | "user";
};

// Intersection with function types
type Logger = {
  log(message: string): void;
};
type Serializable = {
  serialize(): string;
};
type LoggableService = Logger & Serializable; // has both log() and serialize()

// Intersection of primitives — can create impossible types
type Impossible = string & number; // never — a value can't be both
// This is useful in some advanced patterns

// Conflict resolution in intersections
type A = { x: number };
type B = { x: string }; // x is string in B
type AB = A & B;         // x: number & string = never
// AB.x is never — impossible to satisfy both
```

---

## 8. Literal Types & Narrowing

### Literal Types

A literal type is a type that represents exactly ONE specific value.

```typescript
// String literals
type Yes = "yes";
type No = "no";
type YesOrNo = "yes" | "no";

// Number literals
type One = 1;
type HttpOk = 200;
type HttpNotFound = 404;

// Boolean literals
type AlwaysTrue = true;
type AlwaysFalse = false;

// Real-world use: status codes
type HttpStatus = 200 | 201 | 400 | 401 | 403 | 404 | 500;

function handleResponse(status: HttpStatus): string {
  if (status === 200) return "OK";
  if (status === 201) return "Created";
  if (status === 400) return "Bad Request";
  // ...
  return "Unknown";
}

// Literal types enable very precise function contracts
function setAlignment(align: "left" | "center" | "right"): void {
  // ...
}
setAlignment("left");   // OK
setAlignment("center"); // OK
// setAlignment("justify"); // Error — not in the type!

// Template literal types (TypeScript 4.1+)
type EventName = `on${Capitalize<string>}`;
// Valid values: "onClick", "onChange", "onSubmit", etc.

// Literal type inference with 'as const'
const config = {
  host: "localhost",
  port: 3000,
  ssl: false
} as const;
// config.host: "localhost" (literal, not string)
// config.port: 3000 (literal, not number)
// config.ssl: false (literal, not boolean)
// All properties are readonly
```

### Type Narrowing — The Full Picture

Narrowing is how TypeScript refines a broad type to a more specific type within a block of code.

```typescript
function padLeft(padding: number | string, input: string): string {
  // At this point, padding is number | string

  if (typeof padding === "number") {
    // Here, padding is number — narrowed!
    return " ".repeat(padding) + input;
  }

  // Here, padding is string — TypeScript eliminated number
  return padding + input;
}
```

**All Narrowing Techniques:**

#### 1. `typeof` Guards

```typescript
function process(value: string | number | boolean): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // string methods OK
  }
  if (typeof value === "number") {
    return value.toFixed(2);    // number methods OK
  }
  // At this point TypeScript knows: value must be boolean
  return String(value);         // boolean
}

// typeof is useful for: string, number, boolean, bigint, symbol, undefined, function
// NOT useful for: null (returns "object"), arrays (returns "object")
```

#### 2. `instanceof` Guards

```typescript
class HttpError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
  }
}

class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
  }
}

function handleError(error: unknown): string {
  if (error instanceof HttpError) {
    return `HTTP ${error.statusCode}: ${error.message}`;
  }
  if (error instanceof ValidationError) {
    return `Validation error on '${error.field}': ${error.message}`;
  }
  if (error instanceof Error) {
    return `Error: ${error.message}`;
  }
  return "Unknown error";
}
```

#### 3. Truthiness Narrowing

```typescript
function greet(name: string | null | undefined): string {
  if (name) {
    // name is string here (null and undefined are falsy)
    return `Hello, ${name.toUpperCase()}`;
  }
  return "Hello, stranger";
}

// Careful with truthiness — empty string is also falsy!
function process(value: string | null): void {
  if (value) {
    // value is string, BUT "" would be excluded!
    // This might be a bug if "" is a valid value
  }
}

// Better: check specifically for null/undefined
function processSafe(value: string | null): void {
  if (value !== null) {
    // value is string (including "")
  }
}
```

#### 4. Equality Narrowing

```typescript
function compare(a: string | number, b: string | boolean): void {
  if (a === b) {
    // Both a and b must be string (the only type in common that can be ===)
    a.toUpperCase(); // OK
    b.toUpperCase(); // OK
  }
}

// Narrowing with switch
type Status = "loading" | "success" | "error";
function handleStatus(status: Status): void {
  switch (status) {
    case "loading":
      // status is "loading" here
      break;
    case "success":
      // status is "success" here
      break;
    case "error":
      // status is "error" here
      break;
  }
}
```

#### 5. `in` Operator Narrowing

```typescript
interface Cat {
  meow(): void;
  paws: number;
}

interface Dog {
  bark(): void;
  paws: number;
}

function makeSound(animal: Cat | Dog): void {
  if ("meow" in animal) {
    animal.meow(); // TypeScript knows it's Cat
  } else {
    animal.bark(); // TypeScript knows it's Dog
  }
}

// Very useful for discriminated unions
type Message =
  | { type: "text";  content: string }
  | { type: "image"; url: string; alt: string };

function displayMessage(msg: Message): void {
  if ("content" in msg) {
    console.log(msg.content); // text message
  } else {
    console.log(`<img src="${msg.url}" alt="${msg.alt}">`);
  }
}
```

#### 6. Assignment Narrowing

```typescript
type StringOrNumber = string | number;

let x: StringOrNumber;

x = "hello";
console.log(x.toUpperCase()); // x is string here — TypeScript narrows based on assignment

x = 42;
console.log(x.toFixed(2)); // x is number here
```

#### 7. Control Flow Analysis

TypeScript tracks every possible path through your code:

```typescript
function processInput(input: string | null | undefined): string {
  // TypeScript knows: input is string | null | undefined

  if (input === null) {
    return "null value";
    // After this if, input CANNOT be null (it would have returned)
  }

  if (input === undefined) {
    return "undefined value";
    // After this if, input CANNOT be undefined either
  }

  // TypeScript knows: input must be string at this point
  return input.toUpperCase(); // OK — no error
}

// Another example
function getLength(value: string | number[]): number {
  if (typeof value === "string") {
    return value.length;
  }
  // TypeScript knows: must be number[] here
  return value.reduce((sum, n) => sum + n, 0);
}
```

---

## 9. Type Guards — Complete Coverage

A **type guard** is a runtime check that narrows a type in a way TypeScript understands.

### Built-in Type Guards

Already covered: `typeof`, `instanceof`, `in`, truthiness, equality.

### Custom Type Guard Functions (User-Defined Type Guards)

```typescript
// A type predicate function: "param is Type"
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as any).id === "number" &&
    typeof (value as any).name === "string" &&
    typeof (value as any).email === "string"
  );
}

// Using the type guard
function processInput(input: unknown): void {
  if (isString(input)) {
    input.toUpperCase(); // TypeScript knows: input is string
  }

  if (isUser(input)) {
    console.log(input.name); // TypeScript knows: input is User
  }
}

// Type guard for array of specific type
function isStringArray(arr: unknown): arr is string[] {
  return Array.isArray(arr) && arr.every(item => typeof item === "string");
}

// Type guard with generics
function isArrayOf<T>(arr: unknown, guard: (item: unknown) => item is T): arr is T[] {
  return Array.isArray(arr) && arr.every(guard);
}

const isNumberGuard = (x: unknown): x is number => typeof x === "number";
const nums: unknown = [1, 2, 3];
if (isArrayOf(nums, isNumberGuard)) {
  nums.reduce((sum, n) => sum + n, 0); // nums is number[]
}
```

### Assertion Functions

TypeScript 3.7+ supports "assertion functions" — functions that throw if a condition isn't met.

```typescript
// Assertion function — asserts that the value is NOT null/undefined
function assertDefined<T>(val: T | null | undefined, message: string): asserts val is T {
  if (val === null || val === undefined) {
    throw new Error(message);
  }
}

function processUser(userId: string): void {
  const user = findUser(userId); // returns User | null
  assertDefined(user, `User ${userId} not found`);
  // After this line, TypeScript knows: user is User (not null)
  console.log(user.name); // OK — no error!
}

// Assertion function that checks a condition
function assert(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

function processNumber(n: unknown): void {
  assert(typeof n === "number", "Expected a number");
  // TypeScript knows: n is number after the assertion
  console.log(n.toFixed(2)); // OK
}
```

### Discriminant Narrowing — Deep Pattern

```typescript
// Full discriminated union pattern for robust state management
type AsyncState<T, E = Error> =
  | { readonly status: "idle" }
  | { readonly status: "loading"; readonly startedAt: Date }
  | { readonly status: "success"; readonly data: T; readonly completedAt: Date }
  | { readonly status: "error"; readonly error: E; readonly failedAt: Date };

// Type guards for each state
function isIdle<T>(state: AsyncState<T>): state is Extract<AsyncState<T>, { status: "idle" }> {
  return state.status === "idle";
}

function isLoading<T>(state: AsyncState<T>): state is Extract<AsyncState<T>, { status: "loading" }> {
  return state.status === "loading";
}

function isSuccess<T>(state: AsyncState<T>): state is Extract<AsyncState<T>, { status: "success" }> {
  return state.status === "success";
}

function isError<T>(state: AsyncState<T>): state is Extract<AsyncState<T>, { status: "error" }> {
  return state.status === "error";
}

// Usage
function renderState<T>(state: AsyncState<T>, render: (data: T) => string): string {
  if (isIdle(state)) return "Ready";
  if (isLoading(state)) return `Loading... (started ${state.startedAt.toISOString()})`;
  if (isSuccess(state)) return render(state.data);
  if (isError(state)) return `Error: ${state.error.message}`;
  return assertNever(state); // exhaustiveness check
}
```

---

## 10. Functions in TypeScript

### Function Type Annotations

```typescript
// Named function
function add(a: number, b: number): number {
  return a + b;
}

// Function expression
const multiply = function(a: number, b: number): number {
  return a * b;
};

// Arrow function
const divide = (a: number, b: number): number => a / b;

// Function type variable
let operation: (a: number, b: number) => number;
operation = add;       // OK
operation = multiply;  // OK
// operation = (x: string) => x.length; // Error — wrong signature

// Type alias for function types
type BinaryOperation = (a: number, b: number) => number;
type AsyncFetcher<T> = (id: string) => Promise<T>;
type EventHandler<E extends Event = Event> = (event: E) => void;
type Predicate<T> = (value: T) => boolean;
type Transformer<In, Out> = (input: In) => Out;
```

### Optional, Default, and Rest Parameters

```typescript
// Optional parameters — must come AFTER required ones
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}!`;
}
greet("Alice");          // "Hello, Alice!"
greet("Alice", "Hi");    // "Hi, Alice!"

// Default parameters — also make the param optional
function createUser(
  name: string,
  role: "admin" | "user" = "user",
  active: boolean = true
): User {
  return { name, role, active, id: generateId() };
}
createUser("Alice");             // role="user", active=true
createUser("Alice", "admin");    // role="admin", active=true
createUser("Alice", "user", false); // explicitly false

// Default from expression
function timestamp(date: Date = new Date()): string {
  return date.toISOString();
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((total, n) => total + n, 0);
}
sum(1, 2, 3, 4, 5); // 15

// Typed rest parameters
function buildUrl(base: string, ...segments: string[]): string {
  return [base, ...segments].join("/");
}
buildUrl("https://api.example.com", "users", "42", "posts"); // "https://api.example.com/users/42/posts"
```

### Function Overloads

TypeScript lets you define multiple signatures for one function — each signature describes a valid way to call it.

```typescript
// Overload signatures (declarations only — no body)
function process(input: string): string;
function process(input: number): number;
function process(input: string[]): string[];

// Implementation signature (must be compatible with ALL overloads)
function process(input: string | number | string[]): string | number | string[] {
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  if (typeof input === "number") {
    return input * 2;
  }
  return input.map(s => s.toUpperCase());
}

// Callers see the overload signatures, not the implementation
let a = process("hello");    // return type: string
let b = process(42);          // return type: number
let c = process(["a", "b"]);  // return type: string[]
// let d = process(true);     // Error — no matching overload

// Real-world example: createElement with overloads
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "input"): HTMLInputElement;
function createElement(tag: "canvas"): HTMLCanvasElement;
function createElement(tag: string): HTMLElement;
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div = createElement("div");     // HTMLDivElement
const input = createElement("input"); // HTMLInputElement
const span = createElement("span");   // HTMLElement (fallback)
```

### `this` Parameter

```typescript
// TypeScript lets you type 'this' as the first parameter
// (it's erased at compile time — it's not a real parameter)
interface User {
  name: string;
  greet(this: User): string;
}

const user: User = {
  name: "Alice",
  greet() {
    return `Hello, I'm ${this.name}`;
  }
};

// Using this parameter to prevent misuse
function fetchUser(this: void, id: number): Promise<User> {
  // 'this: void' means: this function cannot be called as a method
  // (with a 'this' context) — must be called as a standalone function
  return fetch(`/api/users/${id}`).then(r => r.json());
}

// Class-based 'this' typing
class EventEmitter {
  private listeners = new Map<string, Array<(event: any) => void>>();

  on(event: string, callback: (this: this, data: any) => void): this {
    // The return type 'this' enables fluent/chaining API
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
    return this; // returns the instance for chaining
  }
}
```

---

## 11. Classes in TypeScript

TypeScript enhances JavaScript classes with access modifiers, abstract classes, and more.

### Access Modifiers

```typescript
class BankAccount {
  // public — accessible from anywhere (default)
  public id: string;

  // private — only accessible within THIS class
  private balance: number;

  // protected — accessible within this class AND subclasses
  protected owner: string;

  // readonly — can only be set in constructor (or at declaration)
  readonly accountNumber: string;

  // private shorthand: declare AND initialize a property in constructor
  constructor(
    public readonly id: string,      // public + readonly
    private balance: number,         // private
    protected owner: string,         // protected
    public accountType: string       // public
  ) {
    this.accountNumber = generateAccountNumber();
  }

  getBalance(): number {
    return this.balance; // OK — same class
  }

  deposit(amount: number): void {
    if (amount <= 0) throw new Error("Amount must be positive");
    this.balance += amount;
  }
}

class SavingsAccount extends BankAccount {
  constructor(
    id: string,
    balance: number,
    owner: string,
    private interestRate: number
  ) {
    super(id, balance, owner, "savings");
  }

  applyInterest(): void {
    const interest = this.getBalance() * this.interestRate;
    this.deposit(interest); // OK — deposit is public
    // this.balance += interest; // Error — balance is private (only in BankAccount)
    // this.owner is OK — protected is accessible in subclass
  }
}

const account = new BankAccount("acc1", 1000, "Alice", "checking");
account.id;          // OK — public
account.accountType; // OK — public
account.getBalance(); // OK — public
// account.balance;  // Error — private
// account.owner;    // Error — protected (only within class hierarchy)
```

### Abstract Classes

An abstract class cannot be instantiated directly — it's a template for subclasses.

```typescript
abstract class Animal {
  constructor(protected readonly name: string) {}

  // Abstract method — must be implemented by subclasses
  abstract makeSound(): string;

  // Concrete method — shared by all subclasses
  move(distance: number): void {
    console.log(`${this.name} moved ${distance}m`);
  }

  // Abstract getter
  abstract get description(): string;
}

class Dog extends Animal {
  constructor(name: string, private breed: string) {
    super(name);
  }

  makeSound(): string {
    return "Woof!";
  }

  get description(): string {
    return `${this.name} is a ${this.breed}`;
  }
}

class Cat extends Animal {
  makeSound(): string {
    return "Meow!";
  }

  get description(): string {
    return `${this.name} is a cat`;
  }
}

// const animal = new Animal("any"); // Error — cannot instantiate abstract class
const dog = new Dog("Rex", "Labrador"); // OK
dog.makeSound(); // "Woof!"
dog.move(10);    // "Rex moved 10m"
```

### Interfaces and Classes — `implements`

```typescript
interface Serializable {
  serialize(): string;
  deserialize(data: string): void;
}

interface Comparable<T> {
  compareTo(other: T): number; // negative, zero, or positive
}

interface HasId {
  readonly id: string;
}

// A class can implement multiple interfaces
class Product implements Serializable, Comparable<Product>, HasId {
  constructor(
    public readonly id: string,
    public name: string,
    public price: number
  ) {}

  serialize(): string {
    return JSON.stringify({ id: this.id, name: this.name, price: this.price });
  }

  deserialize(data: string): void {
    const parsed = JSON.parse(data);
    this.name = parsed.name;
    this.price = parsed.price;
  }

  compareTo(other: Product): number {
    return this.price - other.price; // compare by price
  }
}

// Interfaces are structural — TypeScript only cares about the shape
// A class doesn't need to explicitly declare 'implements' to be used as that interface
// (though declaring it catches missing implementations at authoring time)
```

### Static Members

```typescript
class UserRepository {
  private static instance: UserRepository | null = null;
  private static instanceCount = 0;

  // Static factory method (Singleton pattern)
  static getInstance(): UserRepository {
    if (!UserRepository.instance) {
      UserRepository.instance = new UserRepository();
    }
    return UserRepository.instance;
  }

  // Static utility method
  static validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  private users: Map<string, User> = new Map();

  private constructor() {
    UserRepository.instanceCount++;
  }

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user);
    return user;
  }
}

// Usage
const repo1 = UserRepository.getInstance();
const repo2 = UserRepository.getInstance();
// repo1 === repo2 — same instance
// new UserRepository(); // Error — constructor is private
```

### Private Class Fields (ES2022 + TypeScript)

```typescript
class SecureStorage<T> {
  // Native private fields — truly private, even at JS runtime
  #data: Map<string, T> = new Map();
  #maxSize: number;
  #accessLog: string[] = [];

  constructor(maxSize: number = 100) {
    this.#maxSize = maxSize;
  }

  set(key: string, value: T): void {
    if (this.#data.size >= this.#maxSize) {
      throw new Error("Storage is full");
    }
    this.#data.set(key, value);
    this.#accessLog.push(`SET ${key} at ${new Date().toISOString()}`);
  }

  get(key: string): T | undefined {
    this.#accessLog.push(`GET ${key} at ${new Date().toISOString()}`);
    return this.#data.get(key);
  }

  // TypeScript private vs ES private (#):
  // TypeScript private: removed at compile time, accessible in JS
  // ES # private: runtime enforcement, truly inaccessible
  private internalMethod(): void {} // only TypeScript enforcement
  #trulyPrivate(): void {} // runtime enforcement
}

const storage = new SecureStorage<string>(10);
storage.set("key1", "value1");
// storage.#data; // SyntaxError at runtime — truly private!
```

---

## 12. Generics — Complete Guide

Generics let you write code that works with multiple types while remaining type-safe. Think of generics as "type parameters" — placeholder types filled in when the code is used.

### Why Generics?

```typescript
// Without generics — duplicate code or lose type safety
function getFirstItemOfArray(arr: number[]): number {
  return arr[0];
}
function getFirstItemOfStrings(arr: string[]): string {
  return arr[0];
}
// Have to write this for EVERY type!

// With any — type safety lost
function getFirst(arr: any[]): any {
  return arr[0]; // returns any — no type info preserved
}
const first = getFirst([1, 2, 3]);
first.toFixed(2); // TypeScript doesn't catch if this is wrong!

// WITH GENERICS — type-safe and reusable
function getFirst<T>(arr: T[]): T {
  return arr[0];
  // T is filled in at the call site, preserving type information
}

const numFirst = getFirst([1, 2, 3]);       // T is inferred as number
numFirst.toFixed(2);                         // OK — it's a number!
const strFirst = getFirst(["a", "b", "c"]); // T is inferred as string
strFirst.toUpperCase();                       // OK — it's a string!
```

### Generic Functions

```typescript
// Single type parameter
function identity<T>(value: T): T {
  return value;
}
identity(42);        // T inferred as number
identity("hello");   // T inferred as string
identity<boolean>(true); // T explicitly set

// Multiple type parameters
function pair<A, B>(first: A, second: B): [A, B] {
  return [first, second];
}
pair("hello", 42);       // [string, number]
pair(true, { x: 1 });    // [boolean, { x: number }]

// Generic with array operations
function map<T, U>(arr: T[], transform: (item: T) => U): U[] {
  return arr.map(transform);
}
map([1, 2, 3], x => x.toString());  // string[]
map(["a", "b"], s => s.length);      // number[]

// Generic filter
function filter<T>(arr: T[], predicate: (item: T) => boolean): T[] {
  return arr.filter(predicate);
}

// Generic zip
function zip<A, B>(arrA: A[], arrB: B[]): Array<[A, B]> {
  const len = Math.min(arrA.length, arrB.length);
  return Array.from({ length: len }, (_, i) => [arrA[i], arrB[i]]);
}
zip([1, 2, 3], ["a", "b", "c"]); // Array<[number, string]>
```

### Generic Constraints

You can constrain a type parameter to only accept types with certain properties.

```typescript
// Constraint with extends
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Alice", email: "alice@example.com" };
getProperty(user, "name");   // OK — returns string
getProperty(user, "id");     // OK — returns number
// getProperty(user, "missing"); // Error — "missing" is not keyof typeof user

// Constraint with interface
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T): void {
  console.log(item.length);
}
logLength("hello");        // OK — string has length
logLength([1, 2, 3]);      // OK — array has length
// logLength(42);           // Error — number has no length

// Constraint with multiple types
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
merge({ name: "Alice" }, { age: 30 }); // { name: string; age: number }

// Defaulting type parameters (TypeScript 2.3+)
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message: string;
}
// ApiResponse — T defaults to unknown
// ApiResponse<User> — T is User
```

### Generic Interfaces and Classes

```typescript
// Generic interface
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(item: T): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic class implementing generic interface
class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private items = new Map<string, T>();

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null;
  }

  async findAll(): Promise<T[]> {
    return Array.from(this.items.values());
  }

  async save(item: T): Promise<T> {
    this.items.set(item.id, item);
    return item;
  }

  async delete(id: string): Promise<void> {
    this.items.delete(id);
  }
}

// Use with specific types
const userRepo = new InMemoryRepository<User>();
const productRepo = new InMemoryRepository<Product>();
```

### Generic Type Inference in Practice

```typescript
// TypeScript infers generic types from usage
function createState<T>(initial: T) {
  let value = initial;
  return {
    get(): T { return value; },
    set(newValue: T): void { value = newValue; }
  };
}

const nameState = createState("Alice");
nameState.get(); // string
nameState.set("Bob"); // OK
// nameState.set(42); // Error — T was inferred as string

const countState = createState(0);
countState.set(1); // OK
// countState.set("1"); // Error — T was inferred as number

// Inference with callbacks
function useEffect<T>(
  fetcher: () => Promise<T>,
  onSuccess: (data: T) => void
): void {
  fetcher().then(onSuccess);
}

useEffect(
  () => fetch("/api/user").then(r => r.json() as Promise<User>),
  (user) => {
    // TypeScript infers user is User — from the fetcher's return type
    console.log(user.name); // OK
  }
);
```

### Conditional Types in Generics

```typescript
// Unwrap Promise<T> to T
type Awaited<T> = T extends Promise<infer U> ? U : T;
type Result1 = Awaited<Promise<string>>;  // string
type Result2 = Awaited<Promise<number>>;  // number
type Result3 = Awaited<string>;           // string (not a Promise)

// Extract the element type from an array
type ElementOf<T> = T extends (infer U)[] ? U : never;
type StrElement = ElementOf<string[]>; // string
type NumElement = ElementOf<number[]>; // number
type Never = ElementOf<string>;         // never (not an array)

// Infer function return type
type ReturnType<T extends (...args: any) => any> =
  T extends (...args: any) => infer R ? R : never;

function getUser(): User { return { id: 1, name: "Alice", email: "" }; }
type GetUserReturn = ReturnType<typeof getUser>; // User

// Infer function parameter types
type Parameters<T extends (...args: any) => any> =
  T extends (...args: infer P) => any ? P : never;
type GetUserParams = Parameters<typeof getUser>; // []
```

---

## 13. Advanced Types — Every Pattern

### Indexed Access Types

```typescript
type User = {
  id: number;
  name: string;
  address: {
    street: string;
    city: string;
    zip: string;
  };
  tags: string[];
};

// Access the type of a property
type UserId = User["id"];       // number
type UserName = User["name"];   // string
type UserAddress = User["address"]; // { street: string; city: string; zip: string }
type UserStreet = User["address"]["city"]; // string — chain access
type TagsArray = User["tags"];  // string[]
type TagElement = User["tags"][number]; // string — access array element type

// Dynamic key access
type Keys = keyof User; // "id" | "name" | "address" | "tags"
type Values = User[keyof User]; // number | string | { ... } | string[]

// Generic indexed access
function getField<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
// T[K] — the TYPE of the value at key K in object T

// Indexed access with union keys
type NameOrId = User["id" | "name"]; // number | string
```

### `keyof` and `typeof`

```typescript
// keyof — gets union of all keys of a type
interface Config {
  host: string;
  port: number;
  ssl: boolean;
  timeout: number;
}

type ConfigKey = keyof Config; // "host" | "port" | "ssl" | "timeout"

// Useful for type-safe object access
function getConfigValue(config: Config, key: keyof Config): Config[typeof key] {
  return config[key];
}

// typeof — get the TypeScript type of a VALUE
const defaultConfig = {
  host: "localhost",
  port: 3000,
  ssl: false,
  timeout: 30000
};

type DefaultConfigType = typeof defaultConfig;
// { host: string; port: number; ssl: boolean; timeout: number }

// typeof with functions
function add(a: number, b: number): number { return a + b; }
type AddFunction = typeof add; // (a: number, b: number) => number

// Combining keyof and typeof
function pick<T, K extends keyof T>(obj: T, ...keys: K[]): Pick<T, K> {
  return keys.reduce((acc, key) => {
    acc[key] = obj[key];
    return acc;
  }, {} as Pick<T, K>);
}

const config = { host: "localhost", port: 3000, ssl: false };
pick(config, "host", "port"); // { host: string; port: number }
```

### Lookup Types and Indexed Types in Depth

```typescript
// Building type-safe event systems
interface EventMap {
  "user:created": { userId: string; email: string };
  "user:deleted": { userId: string };
  "order:placed": { orderId: string; total: number };
  "payment:processed": { paymentId: string; amount: number; success: boolean };
}

type EventName = keyof EventMap; // "user:created" | "user:deleted" | ...
type EventPayload<E extends EventName> = EventMap[E];

// Type-safe event emitter
class TypedEventEmitter {
  private listeners = new Map<string, Function[]>();

  on<E extends EventName>(
    event: E,
    listener: (payload: EventPayload<E>) => void
  ): void {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event)!.push(listener);
  }

  emit<E extends EventName>(event: E, payload: EventPayload<E>): void {
    this.listeners.get(event)?.forEach(listener => listener(payload));
  }
}

const emitter = new TypedEventEmitter();

emitter.on("user:created", (payload) => {
  // payload is { userId: string; email: string } — fully typed!
  console.log(payload.userId, payload.email);
});

emitter.emit("user:created", { userId: "123", email: "test@example.com" }); // OK
// emitter.emit("user:created", { wrong: "fields" }); // Error!
```

### `infer` — Type Inference in Conditional Types

`infer` lets you "capture" a part of a type inside a conditional type.

```typescript
// Basic infer
type GetReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type GetParams<T> = T extends (...args: infer P) => any ? P : never;

// Unwrap nested types
type Flatten<T> = T extends Array<infer Item> ? Item : T;
type FlattenNested<T> = T extends Array<infer Item>
  ? Item extends Array<infer Nested>
    ? Nested
    : Item
  : T;

type StrArray = Flatten<string[]>; // string
type NumArray = Flatten<number[]>; // number
type NotArray = Flatten<boolean>;  // boolean (passthrough)

// Infer from Promise
type UnwrapPromise<T> = T extends Promise<infer U> ? UnwrapPromise<U> : T;
type Result = UnwrapPromise<Promise<Promise<string>>>; // string — recursively unwrapped

// Infer first and last elements of tuple
type First<T extends any[]> = T extends [infer Head, ...any[]] ? Head : never;
type Last<T extends any[]> = T extends [...any[], infer Tail] ? Tail : never;

type F = First<[string, number, boolean]>; // string
type L = Last<[string, number, boolean]>;  // boolean

// Infer constructor parameter types
type ConstructorParams<T extends new (...args: any) => any> =
  T extends new (...args: infer P) => any ? P : never;

class Service {
  constructor(public name: string, public port: number) {}
}
type ServiceParams = ConstructorParams<typeof Service>; // [string, number]
```

---

## 14. Utility Types — Complete Reference

TypeScript ships with built-in utility types. These are VERY commonly used and asked about in interviews.

### Object Property Modifiers

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
  lastLogin: Date;
}

// Partial<T> — makes ALL properties optional
type PartialUser = Partial<User>;
// { id?: number; name?: string; email?: string; role?: ...; lastLogin?: Date }

// Required<T> — makes ALL properties required (removes ?)
interface Config {
  host?: string;
  port?: number;
}
type RequiredConfig = Required<Config>;
// { host: string; port: number } — both required now

// Readonly<T> — makes ALL properties readonly
type ReadonlyUser = Readonly<User>;
// { readonly id: number; readonly name: string; ... }
// Cannot modify any property after creation

// Custom deep versions:
type DeepPartial<T> = T extends object ? {
  [K in keyof T]?: DeepPartial<T[K]>;
} : T;

type DeepReadonly<T> = T extends object ? {
  readonly [K in keyof T]: DeepReadonly<T[K]>;
} : T;

type DeepRequired<T> = T extends object ? {
  [K in keyof T]-?: DeepRequired<T[K]>; // -? removes optionality
} : T;
```

### Picking and Omitting

```typescript
// Pick<T, K> — keep ONLY the specified keys
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

type LoginFields = Pick<User, "email" | "role">;
// { email: string; role: "admin" | "user" }

// Omit<T, K> — keep everything EXCEPT the specified keys
type CreateUserDTO = Omit<User, "id" | "lastLogin">;
// { name: string; email: string; role: "admin" | "user" }

type PublicUser = Omit<User, "email" | "lastLogin">;
// { id: number; name: string; role: "admin" | "user" }

// Pick vs Omit — when to use which:
// Pick: when you want FEW fields from a type with many fields
// Omit: when you want MOST fields, removing just a few

// Common pattern: DTO types
interface UserEntity {
  id: string;
  name: string;
  email: string;
  passwordHash: string; // sensitive — don't expose!
  createdAt: Date;
  updatedAt: Date;
}

type CreateUserDto = Omit<UserEntity, "id" | "createdAt" | "updatedAt">;
type UpdateUserDto = Partial<Omit<UserEntity, "id" | "createdAt" | "updatedAt" | "passwordHash">>;
type UserResponseDto = Omit<UserEntity, "passwordHash">; // safe to send
```

### Set Operations

```typescript
type A = "a" | "b" | "c" | "d";
type B = "c" | "d" | "e" | "f";

// Extract<T, U> — keep members of T that ARE assignable to U (intersection)
type Common = Extract<A, B>; // "c" | "d"
type Strings = Extract<string | number | boolean, string>; // string
type Arrays = Extract<string[] | number[] | boolean, any[]>; // string[] | number[]

// Exclude<T, U> — keep members of T that are NOT assignable to U (set difference)
type OnlyInA = Exclude<A, B>; // "a" | "b"
type NonString = Exclude<string | number | boolean, string>; // number | boolean

// NonNullable<T> — remove null and undefined
type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>; // string
```

### Function-Related Utilities

```typescript
// ReturnType<T> — extracts return type of a function type
function fetchUser(): Promise<User> { ... }
type FetchResult = ReturnType<typeof fetchUser>; // Promise<User>

function add(a: number, b: number): number { return a + b; }
type AddResult = ReturnType<typeof add>; // number

// Parameters<T> — extracts parameter types as a tuple
type FetchParams = Parameters<typeof fetchUser>; // []
type AddParams = Parameters<typeof add>; // [a: number, b: number]

// ConstructorParameters<T> — like Parameters but for constructors
class HttpClient {
  constructor(public baseUrl: string, public timeout: number = 5000) {}
}
type HttpClientParams = ConstructorParameters<typeof HttpClient>;
// [baseUrl: string, timeout?: number]

// InstanceType<T> — extracts the instance type of a constructor
type HttpClientInstance = InstanceType<typeof HttpClient>; // HttpClient

// Useful pattern
type ServiceInstance<T extends new (...args: any) => any> = InstanceType<T>;
```

### String Manipulation Utilities

```typescript
// Uppercase<S>, Lowercase<S>, Capitalize<S>, Uncapitalize<S>
type Upper = Uppercase<"hello world">; // "HELLO WORLD"
type Lower = Lowercase<"HELLO WORLD">; // "hello world"
type Cap = Capitalize<"hello">; // "Hello"
type Uncap = Uncapitalize<"Hello">; // "hello"

// Used in template literal types
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"
type ChangeEvent = EventName<"change">; // "onChange"

// Building getter type names
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  id: number;
  name: string;
  email: string;
}

type UserGetters = Getters<User>;
// {
//   getId: () => number;
//   getName: () => string;
//   getEmail: () => string;
// }
```

### Awaited

```typescript
// Awaited<T> — recursively unwraps Promise types (TypeScript 4.5+)
type T1 = Awaited<string>;                    // string
type T2 = Awaited<Promise<string>>;            // string
type T3 = Awaited<Promise<Promise<string>>>;   // string — recursive!
type T4 = Awaited<Promise<string | number>>;   // string | number

async function fetchAll(): Promise<User[]> { ... }
type FetchAllResult = Awaited<ReturnType<typeof fetchAll>>; // User[]
```

---

## 15. Mapped Types — Deep Dive

Mapped types create new types by transforming each property of an existing type.

### Basic Mapped Type

```typescript
// The syntax: { [K in UnionType]: SomeType }
// "For each K in the union UnionType, create a property of type SomeType"

type BooleanFlags = {
  [K in "a" | "b" | "c"]: boolean;
};
// { a: boolean; b: boolean; c: boolean }

// Using keyof to iterate over existing type's keys
type StringVersion<T> = {
  [K in keyof T]: string; // every property becomes string
};

type User = { id: number; name: string; active: boolean };
type StringUser = StringVersion<User>;
// { id: string; name: string; active: string }

// How Partial<T> is implemented:
type MyPartial<T> = {
  [K in keyof T]?: T[K]; // '?' makes it optional
};

// How Readonly<T> is implemented:
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K]; // 'readonly' modifier
};

// How Required<T> is implemented:
type MyRequired<T> = {
  [K in keyof T]-?: T[K]; // '-?' REMOVES optional modifier
};

// Removing readonly:
type Mutable<T> = {
  -readonly [K in keyof T]: T[K]; // '-readonly' removes readonly
};
```

### Mapped Types with Key Remapping (`as`)

TypeScript 4.1 added key remapping — you can change the key names in a mapped type.

```typescript
// Rename keys using 'as'
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  id: number;
  name: string;
  email: string;
}

type UserGetters = Getters<User>;
// { getId: () => number; getName: () => string; getEmail: () => string }

// Filter properties using 'as never' to exclude
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

type StringFields = OnlyStrings<User>;
// { name: string; email: string } — id (number) is filtered out

// Create event handler types
type EventHandlers<T> = {
  [K in keyof T as `on${Capitalize<string & K>}Changed`]?: (
    newValue: T[K],
    oldValue: T[K]
  ) => void;
};

type UserEventHandlers = EventHandlers<User>;
// {
//   onIdChanged?: (newValue: number, oldValue: number) => void;
//   onNameChanged?: (newValue: string, oldValue: string) => void;
//   onEmailChanged?: (newValue: string, oldValue: string) => void;
// }
```

### Practical Mapped Type Patterns

```typescript
// Make all functions in an interface async
type AsyncVersion<T> = {
  [K in keyof T]: T[K] extends (...args: infer A) => infer R
    ? (...args: A) => Promise<R>
    : T[K];
};

interface SyncRepository {
  findById(id: string): User | null;
  save(user: User): User;
  delete(id: string): void;
}

type AsyncRepository = AsyncVersion<SyncRepository>;
// findById(id: string): Promise<User | null>
// save(user: User): Promise<User>
// delete(id: string): Promise<void>

// Nullable version of a type
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

// Record-like type with specific value types
type FeatureFlags = Record<string, boolean>;
// Equivalent to: { [key: string]: boolean }

// Type-safe Record
type HttpStatusMessages = Record<200 | 201 | 400 | 401 | 404 | 500, string>;
const messages: HttpStatusMessages = {
  200: "OK",
  201: "Created",
  400: "Bad Request",
  401: "Unauthorized",
  404: "Not Found",
  500: "Internal Server Error"
};

// Flatten an object type (make all values one level)
type FlattenObject<T> = {
  [K in keyof T]: T[K] extends object ? keyof T[K] : K;
};
```

---

## 16. Conditional Types — Deep Dive

A conditional type is like an if-statement at the type level.

### Syntax

```typescript
// T extends Condition ? TypeIfTrue : TypeIfFalse
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false
type C = IsString<"hello">; // true ("hello" extends string)
```

### Distributive Conditional Types

When a conditional type is applied to a union, it distributes over each member:

```typescript
type ToArray<T> = T extends any ? T[] : never;

type A = ToArray<string | number>;
// This distributes: ToArray<string> | ToArray<number>
// Result: string[] | number[]

// Compare with a non-distributive version:
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
// The [T] wrapping prevents distribution
type B = ToArrayNonDist<string | number>; // (string | number)[]

// Filtering union types using distribution
type Strings<T> = T extends string ? T : never;
type Numbers<T> = T extends number ? T : never;

type Mixed = string | number | boolean | null;
type OnlyStrings = Strings<Mixed>; // string
type OnlyNumbers = Numbers<Mixed>; // number

// This is how Extract and Exclude are implemented:
type MyExtract<T, U> = T extends U ? T : never;
type MyExclude<T, U> = T extends U ? never : T;
```

### Complex Conditional Types

```typescript
// Recursive conditional types
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

// Conditional return type based on input
type Stringify<T> =
  T extends string   ? T :
  T extends number   ? `${T}` :
  T extends boolean  ? "true" | "false" :
  T extends null     ? "null" :
  T extends undefined ? "undefined" :
  string;

// Type-safe parser
type Parse<T extends string> =
  T extends "true"    ? true :
  T extends "false"   ? false :
  T extends "null"    ? null :
  T extends `${infer N extends number}` ? N : // parse number
  T; // keep as string

type Parsed1 = Parse<"42">;    // 42 (number!)
type Parsed2 = Parse<"true">;  // true (boolean!)
type Parsed3 = Parse<"hello">; // "hello" (string)

// Checking if a type is a specific kind
type IsArray<T> = T extends any[] ? true : false;
type IsFunction<T> = T extends Function ? true : false;
type IsPromise<T> = T extends Promise<any> ? true : false;
type IsNullable<T> = null extends T ? true : false;

// Getting the "inner" type
type Unbox<T> =
  T extends Array<infer Item>   ? Item :
  T extends Promise<infer Value> ? Value :
  T extends Set<infer Element>   ? Element :
  T extends Map<any, infer V>    ? V :
  T;

type A = Unbox<string[]>;           // string
type B = Unbox<Promise<number>>;    // number
type C = Unbox<Set<boolean>>;       // boolean
type D = Unbox<Map<string, Date>>;  // Date
type E = Unbox<string>;             // string (passthrough)
```

---

## 17. Template Literal Types

Template literal types (TypeScript 4.1+) let you build types from string combinations.

```typescript
// Basic template literal type
type Greeting = `Hello, ${string}`;
// Any string starting with "Hello, "

// With literal union
type Color = "red" | "green" | "blue";
type Size = "sm" | "md" | "lg";
type ClassName = `btn-${Color}-${Size}`;
// "btn-red-sm" | "btn-red-md" | "btn-red-lg" | "btn-green-sm" | ...
// Automatically generates ALL combinations!

// Event names
type EventBase = "click" | "change" | "submit" | "focus" | "blur";
type EventHandlerName = `on${Capitalize<EventBase>}`;
// "onClick" | "onChange" | "onSubmit" | "onFocus" | "onBlur"

// CSS property names to camelCase
type CssProperties = "background-color" | "font-size" | "margin-top";
type CamelCase<S extends string> =
  S extends `${infer Head}-${infer Tail}`
    ? `${Head}${Capitalize<CamelCase<Tail>>}`
    : S;

type CC = CamelCase<"background-color">; // "backgroundColor"
type CC2 = CamelCase<"margin-top">;       // "marginTop"

// Deep path types (for accessing nested properties)
type DotPath<T extends object, K extends keyof T = keyof T> =
  K extends string
    ? T[K] extends object
      ? `${K}` | `${K}.${DotPath<T[K]>}`
      : `${K}`
    : never;

interface Config {
  server: {
    host: string;
    port: number;
  };
  database: {
    url: string;
    name: string;
  };
}

type ConfigPath = DotPath<Config>;
// "server" | "database" | "server.host" | "server.port" | "database.url" | "database.name"

// SQL-like query builder types
type TableName = "users" | "orders" | "products";
type SelectQuery<T extends TableName> = `SELECT * FROM ${T}`;
type InsertQuery<T extends TableName> = `INSERT INTO ${T}`;

type UserSelect = SelectQuery<"users">; // "SELECT * FROM users"
```

---

## 18. Decorators & Metadata

Decorators are a stage-3 ECMAScript proposal. TypeScript supports them (with experimental flags).

```typescript
// Enable in tsconfig.json:
// "experimentalDecorators": true
// "emitDecoratorMetadata": true

// Class decorator — receives the class constructor
function Singleton<T extends new (...args: any[]) => any>(Base: T) {
  let instance: InstanceType<T>;
  return class extends Base {
    constructor(...args: any[]) {
      if (instance) return instance;
      super(...args);
      instance = this as any;
    }
  };
}

@Singleton
class Database {
  connection: string;
  constructor(url: string) {
    this.connection = url;
  }
}

// Method decorator
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
): PropertyDescriptor {
  const original = descriptor.value;
  descriptor.value = function(...args: any[]) {
    console.log(`Calling ${propertyKey} with:`, args);
    const result = original.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };
  return descriptor;
}

class Calculator {
  @Log
  add(a: number, b: number): number {
    return a + b;
  }
}

// Property decorator
function Required(target: any, propertyKey: string): void {
  // Metadata about the property
  Reflect.defineMetadata("required", true, target, propertyKey);
}

// Parameter decorator
function Validate(target: any, method: string, index: number): void {
  // Mark parameter at index as requiring validation
}

// Decorator factory (decorator with configuration)
function Throttle(milliseconds: number) {
  return function(target: any, key: string, descriptor: PropertyDescriptor) {
    let lastCalled = 0;
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
      const now = Date.now();
      if (now - lastCalled >= milliseconds) {
        lastCalled = now;
        return original.apply(this, args);
      }
    };
    return descriptor;
  };
}

class SearchService {
  @Throttle(300) // Only call every 300ms
  search(query: string): void {
    console.log("Searching:", query);
  }
}

// Validation decorator system (like class-validator)
function IsString(target: any, key: string): void {
  let value: string;
  const getter = () => value;
  const setter = (newValue: any) => {
    if (typeof newValue !== "string") {
      throw new TypeError(`${key} must be a string, got ${typeof newValue}`);
    }
    value = newValue;
  };
  Object.defineProperty(target, key, { get: getter, set: setter });
}

function MinLength(min: number) {
  return function(target: any, key: string): void {
    let value: string;
    const setter = (newValue: string) => {
      if (newValue.length < min) {
        throw new Error(`${key} must be at least ${min} characters`);
      }
      value = newValue;
    };
    Object.defineProperty(target, key, {
      get: () => value,
      set: setter
    });
  };
}

class CreateUserDto {
  @IsString
  @MinLength(2)
  name: string = "";

  @IsString
  email: string = "";
}
```

---

## 19. Modules, Namespaces & Declaration Files

### ES Modules in TypeScript

```typescript
// Exporting
export const PI = 3.14159;

export interface User {
  id: number;
  name: string;
}

export function add(a: number, b: number): number {
  return a + b;
}

export default class UserService {
  findUser(id: number): User | null { ... }
}

// Importing
import UserService from "./UserService";          // default
import { User, add } from "./types";              // named
import { User as UserType } from "./types";       // renamed
import * as MathUtils from "./math";              // namespace import
import type { User } from "./types";              // TYPE-only import (erased at runtime)
import UserService, { User } from "./module";     // both

// 'import type' is important:
// - Makes it clear the import is only for types
// - TypeScript can erase it without running the module
// - Required in some configurations to avoid circular deps

// Re-exporting
export { add } from "./math";
export type { User } from "./types"; // type-only re-export
export * from "./utils";
export * as Validators from "./validators"; // namespace re-export
```

### Module Resolution

```typescript
// TypeScript looks for modules in this order:
// 1. Relative imports: "./module", "../module"
//    - ./module.ts
//    - ./module.tsx
//    - ./module.d.ts
//    - ./module/index.ts
//    - ./module/index.tsx

// 2. Non-relative imports: "lodash", "react", "@company/utils"
//    - node_modules lookup
//    - tsconfig "paths" mapping

// tsconfig.json paths mapping
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@components/*": ["./components/*"],
      "@lib/*": ["./lib/*"]
    }
  }
}

// Now you can use:
import { Button } from "@components/Button";
import { formatDate } from "@lib/utils";
```

### Declaration Files

```typescript
// For third-party JS libraries without types, you write .d.ts files

// Declaring a module
declare module "untyped-library" {
  export function doSomething(value: string): number;
  export class UnknownClass {
    constructor(options: object);
    method(): void;
  }
  export default function(config: object): void;
}

// Ambient declarations — for globally available things
declare const __DEV__: boolean;
declare const __VERSION__: string;

// Extending existing types (module augmentation)
declare module "express" {
  interface Request {
    user?: AuthenticatedUser;
    requestId: string;
  }
}

// Declaring global variables
declare global {
  interface Window {
    analytics: AnalyticsClient;
    featureFlags: Record<string, boolean>;
  }

  // Extend Array prototype (use with caution)
  interface Array<T> {
    last(): T | undefined;
  }
}

// This makes TypeScript know about your window.analytics
window.analytics.track("pageview"); // OK
```

---

## 20. The TypeScript Compiler & tsconfig.json

### Essential tsconfig Settings

```json
{
  "compilerOptions": {
    // Target JavaScript version
    "target": "ES2022",
    // What module system to emit
    "module": "NodeNext",   // or "ESNext", "CommonJS"
    // Module resolution strategy
    "moduleResolution": "NodeNext",

    // === STRICT MODE (always enable these) ===
    "strict": true,
    // This enables all of the below:
    "strictNullChecks": true,       // null/undefined must be handled
    "strictFunctionTypes": true,    // stricter function type checking
    "strictBindCallApply": true,    // strict checking of call/bind/apply
    "strictPropertyInitialization": true, // class properties must be initialized
    "noImplicitAny": true,          // error on implicit any
    "noImplicitThis": true,         // error on implicit any for 'this'
    "alwaysStrict": true,           // emit "use strict" in all files

    // === ADDITIONAL CHECKS ===
    "noUnusedLocals": true,         // error on unused variables
    "noUnusedParameters": true,     // error on unused parameters
    "noImplicitReturns": true,      // all code paths must return
    "noFallthroughCasesInSwitch": true, // no fallthrough in switch
    "exactOptionalPropertyTypes": true, // undefined !== missing property
    "noUncheckedIndexedAccess": true,   // index access includes undefined

    // === OUTPUT ===
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,            // emit .d.ts files
    "declarationMap": true,         // source maps for .d.ts
    "sourceMap": true,              // source maps for .js
    "removeComments": false,        // keep comments in output

    // === PATHS ===
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"]
    },

    // === LIBRARIES ===
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    // ES2022: Array.at, Object.hasOwn, Error.cause, etc.
    // DOM: browser APIs (window, document, fetch, etc.)

    // === EXPERIMENTAL ===
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,

    // === INTEROP ===
    "esModuleInterop": true,        // allows default import of CJS modules
    "allowSyntheticDefaultImports": true, // same effect without modifying emit
    "resolveJsonModule": true,      // allow importing .json files
    "skipLibCheck": true            // skip type checking of .d.ts files (faster builds)
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Understanding `strictNullChecks`

```typescript
// WITH strictNullChecks: false (dangerous, avoid)
let name: string = null;     // OK — null is assignable to everything
let user: User = undefined;  // OK

// WITH strictNullChecks: true (recommended)
let name: string = null;     // Error! null is NOT assignable to string
let user: User = undefined;  // Error!

// Now you must explicitly include null/undefined in unions:
let nullableName: string | null = null; // OK
let optionalUser: User | undefined = undefined; // OK

// And you must check before using:
function greet(name: string | null): string {
  // name.toUpperCase(); // Error — might be null!
  return name?.toUpperCase() ?? "Hello, stranger";
}
```

### The `noUncheckedIndexedAccess` Setting

```typescript
// With noUncheckedIndexedAccess: true
const arr = [1, 2, 3];
const first = arr[0]; // type: number | undefined (index might be out of bounds)
// first.toFixed(2); // Error — might be undefined!

// You must check:
if (first !== undefined) {
  first.toFixed(2); // OK
}

const map: Record<string, number> = {};
const val = map["key"]; // type: number | undefined
```

---

## 21. Structural Typing & Type Compatibility

### Structural Typing

TypeScript uses **structural typing** (duck typing) — a type is compatible with another if it has the **required shape**, regardless of name.

```typescript
interface Point2D {
  x: number;
  y: number;
}

interface Named {
  x: number;
  y: number;
  name: string; // extra property
}

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

const point: Named = { x: 1, y: 2, name: "origin" };
printPoint(point); // OK! Named has x and y — it satisfies Point2D
// TypeScript only checks that the required properties are present
// Extra properties are allowed (they're just ignored)

// But with object literals, TypeScript does "excess property checking"
printPoint({ x: 1, y: 2, name: "origin" }); // Error! Excess property 'name'
// This is a special check only on DIRECT object literals — prevents typos
// When you assign through a variable, the check is bypassed (as above)
```

### Assignability Rules

```typescript
// Subtypes are assignable to supertypes
// A type A is a subtype of B if A has all properties of B (and possibly more)

interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}

let animal: Animal;
let dog: Dog = { name: "Rex", breed: "Lab" };

animal = dog;   // OK — Dog has everything Animal has
// dog = animal; // Error — Animal might not have 'breed'

// Function assignability
// Function with FEWER parameters is assignable to function with MORE parameters
type Handler = (event: Event, id: number) => void;

const simpleHandler = (event: Event) => {}; // only handles event, ignores id
const handler: Handler = simpleHandler; // OK! This is common in JavaScript callbacks

// Return type: more specific is assignable to less specific
type GetAnimal = () => Animal;
const getDog: () => Dog = () => ({ name: "Rex", breed: "Lab" });
const getAnimal: GetAnimal = getDog; // OK — Dog is assignable to Animal
```

### Branded Types (Nominal Typing Simulation)

When structural typing is too permissive, branded types add nominal-like behavior:

```typescript
// Problem: all these are just 'number' — easy to mix them up
function transfer(from: number, to: number, amount: number): void {
  // ... is 'from' an accountId? userId? What if we swap arguments?
}

// Solution: branded types
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<number, "UserId">;
type AccountId = Brand<number, "AccountId">;
type Amount = Brand<number, "Amount">;

// Factory functions create the branded values
function toUserId(id: number): UserId {
  return id as UserId;
}
function toAccountId(id: number): AccountId {
  return id as AccountId;
}
function toAmount(amount: number): Amount {
  if (amount < 0) throw new Error("Amount cannot be negative");
  return amount as Amount;
}

// Now functions are type-safe
function transfer(from: AccountId, to: AccountId, amount: Amount): void {
  // ...
}

const userId = toUserId(1);
const accountId = toAccountId(100);
const amount = toAmount(50);

transfer(accountId, toAccountId(200), amount); // OK
// transfer(userId, accountId, amount); // Error — userId is UserId, not AccountId!
// transfer(accountId, accountId, 50); // Error — 50 is number, not Amount!
```

---

## 22. Declaration Merging & Module Augmentation

### Declaration Merging

```typescript
// Interfaces with the same name merge automatically
interface User {
  id: number;
  name: string;
}

interface User {
  email: string;
  role: "admin" | "user";
}

// Result: User has id, name, email, AND role
const user: User = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  role: "admin"
};

// This is how typing for third-party libs works
// @types/express adds to the existing express types
```

### Module Augmentation

```typescript
// Extend types from external packages
import express from "express";

// Augment the express namespace
declare module "express" {
  interface Request {
    user?: {
      id: string;
      email: string;
      roles: string[];
    };
    requestId: string;
    startTime: number;
  }
}

// Now in your middleware:
app.use((req, res, next) => {
  req.requestId = crypto.randomUUID(); // TypeScript knows this field exists
  req.startTime = Date.now();
  next();
});

// And in your routes:
app.get("/profile", (req, res) => {
  if (!req.user) { // TypeScript knows req.user might be undefined
    return res.status(401).json({ error: "Unauthorized" });
  }
  res.json(req.user); // TypeScript knows req.user shape
});
```

### Namespace Merging

```typescript
// A function and namespace with the same name merge
function validate(input: string): boolean {
  return input.length > 0;
}

namespace validate {
  export function email(input: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input);
  }

  export function url(input: string): boolean {
    try { new URL(input); return true; }
    catch { return false; }
  }
}

validate("hello");        // calls the function
validate.email("a@b.com"); // calls the namespace method
```

---

## 23. Enums — Full Coverage

```typescript
// Numeric enum (auto-increments from 0)
enum Direction {
  North,   // 0
  South,   // 1
  East,    // 2
  West     // 3
}

let dir: Direction = Direction.North;
Direction[0]; // "North" — reverse mapping (only numeric enums)
Direction.North; // 0

// Numeric enum with custom start
enum HttpStatus {
  OK = 200,
  Created = 201,
  BadRequest = 400,
  Unauthorized = 401,
  NotFound = 404,
  InternalError = 500
}

// String enum — most useful in practice
enum LogLevel {
  Debug = "DEBUG",
  Info = "INFO",
  Warn = "WARN",
  Error = "ERROR"
}

// String enums are NOT auto-incremented
// String enum values are included in JavaScript output (unlike const enum)
let level: LogLevel = LogLevel.Info;
// level = "INFO"; // Error — must use LogLevel.Info

// Const enum — inlined at compile time, zero runtime overhead
const enum Direction2 {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT"
}

const move = Direction2.Up;
// Compiles to: const move = "UP"; — the enum is completely inlined!

// Heterogeneous enum (avoid — confusing)
enum Mixed {
  No = 0,
  Yes = "YES" // mixing number and string
}

// Enum pitfalls — why many prefer union types
enum Status {
  Active = "active",
  Inactive = "inactive"
}

// Problem: enums add runtime code (except const enums)
// Problem: enums are nominal — Status.Active !== "active" type-wise
// Problem: numeric enums allow any number

// Alternative: string literal union (often preferred)
type Status = "active" | "inactive";
// - No runtime code
// - Compatible with string values
// - Autocomplete works
// - Can use directly in JSON/API responses

// Enum as flags (bitwise)
enum Permissions {
  None   = 0,
  Read   = 1 << 0,  // 1
  Write  = 1 << 1,  // 2
  Delete = 1 << 2,  // 4
  Admin  = Read | Write | Delete // 7
}

function canRead(perms: Permissions): boolean {
  return (perms & Permissions.Read) !== 0;
}
const userPerms = Permissions.Read | Permissions.Write;
canRead(userPerms); // true
```

---

## 24. Symbols & Unique Symbols

```typescript
// symbol — a symbol value
let sym: symbol = Symbol("description");

// unique symbol — a specific symbol value
// only const variables and readonly class properties can be unique symbol
const id: unique symbol = Symbol("id");
const id2: unique symbol = Symbol("id");

// They are different types even with the same description:
// typeof id !== typeof id2

// Symbols as object keys (avoid class in Object.keys/JSON.stringify)
const SECRET_KEY = Symbol("secretKey");

interface WithSecret {
  [SECRET_KEY]: string;
  public: string;
}

const obj: WithSecret = {
  [SECRET_KEY]: "secret value",
  public: "visible"
};

Object.keys(obj); // ["public"] — symbol key is hidden
JSON.stringify(obj); // {"public":"visible"} — symbol key excluded

// Well-known symbols for customizing behavior
class Range {
  constructor(public from: number, public to: number) {}

  [Symbol.iterator]() {
    let current = this.from;
    const end = this.to;
    return {
      next(): IteratorResult<number> {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { value: undefined as any, done: true };
      }
    };
  }
}

// Now Range works with for...of, spread, destructuring
for (const n of new Range(1, 5)) {
  console.log(n); // 1, 2, 3, 4, 5
}
[...new Range(1, 3)]; // [1, 2, 3]
```

---

## 25. Variance — Covariance, Contravariance & Invariance

Understanding variance is important for understanding why TypeScript allows or rejects certain assignments.

### What is Variance?

Variance describes how type parameters relate to each other in terms of subtype relationships.

```typescript
// Setup
interface Animal { name: string }
interface Dog extends Animal { breed: string }
// Dog is a subtype of Animal (Dog extends Animal)
// So: Dog is assignable to Animal

// COVARIANCE — the container follows the same direction
// If Dog is a subtype of Animal, then ReadonlyArray<Dog> is a subtype of ReadonlyArray<Animal>
const dogs: ReadonlyArray<Dog> = [{ name: "Rex", breed: "Lab" }];
const animals: ReadonlyArray<Animal> = dogs; // OK — covariant
// This is safe because we can only READ from ReadonlyArray

// CONTRAVARIANCE — the container goes the opposite direction
// If Dog is a subtype of Animal, then a function expecting Animal is a supertype of a function expecting Dog
// (Consumer<Animal> is a subtype of Consumer<Dog>)
type Consumer<T> = (arg: T) => void;
const consumeAnimal: Consumer<Animal> = (a) => console.log(a.name);
const consumeDog: Consumer<Dog> = consumeAnimal; // OK — contravariant
// This is safe because: consumeAnimal can handle ANY animal, including dogs

// INVARIANCE — no relationship either way
// Mutable arrays in TypeScript are treated as covariant (despite being technically unsound)
// This is a design decision for practicality
const mutableDogs: Dog[] = [];
// const mutableAnimals: Animal[] = mutableDogs; // Allowed in TS but technically unsound
// mutableAnimals.push({ name: "Cat" }); // Would add a non-Dog to dogs array!

// TypeScript's function parameter bivariance (strictFunctionTypes: false)
// vs strictFunctionTypes: true
// With strict: parameters are contravariant (the correct behavior)
```

### Variance Annotations (TypeScript 4.7+)

```typescript
// Explicit variance annotations
type CovariantContainer<out T> = {
  get(): T;
  // set(value: T): void; // Error — cannot have out-position and in-position
};

type ContravariantContainer<in T> = {
  process(value: T): void;
  // get(): T; // Error — cannot have in-position and out-position
};

// This makes TypeScript faster (no inference needed) and more precise
type ReadonlyBox<out T> = {
  readonly value: T;
};

type WriteBox<in T> = {
  setValue(newValue: T): void;
};

const dogBox: ReadonlyBox<Dog> = { value: { name: "Rex", breed: "Lab" } };
const animalBox: ReadonlyBox<Animal> = dogBox; // OK — out parameter is covariant
```

---

## 26. Error Handling Patterns in TypeScript

### The Problem with `throw`

```typescript
// TypeScript cannot type thrown values
// catch(e: unknown) — e could be anything
function parse(json: string) {
  return JSON.parse(json); // might throw SyntaxError
}

try {
  const data = parse("invalid");
} catch (e) {
  // e is 'unknown' — you must narrow it
  if (e instanceof SyntaxError) {
    console.log("Syntax error:", e.message);
  } else if (e instanceof Error) {
    console.log("Error:", e.message);
  } else {
    console.log("Unknown error:", String(e));
  }
}
```

### Result / Either Pattern

```typescript
// Define success and error cases as types
type Success<T> = { readonly ok: true; readonly data: T };
type Failure<E extends Error = Error> = { readonly ok: false; readonly error: E };
type Result<T, E extends Error = Error> = Success<T> | Failure<E>;

// Constructor functions
function ok<T>(data: T): Success<T> {
  return { ok: true, data };
}
function err<E extends Error>(error: E): Failure<E> {
  return { ok: false, error };
}

// Using Result
async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      return err(new Error(`HTTP ${response.status}: ${response.statusText}`));
    }
    const user = await response.json() as User;
    return ok(user);
  } catch (e) {
    return err(e instanceof Error ? e : new Error("Unknown error"));
  }
}

// Consuming Results — explicit, no hidden throws
async function displayUser(id: string): Promise<void> {
  const result = await fetchUser(id);

  if (!result.ok) {
    console.error("Failed to fetch user:", result.error.message);
    return;
  }

  // result.data is User — TypeScript knows this is the success case
  console.log(`Hello, ${result.data.name}`);
}

// Chaining results
function mapResult<T, U, E extends Error>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  if (!result.ok) return result;
  return ok(fn(result.data));
}

function chainResult<T, U, E extends Error>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  if (!result.ok) return result;
  return fn(result.data);
}
```

### Custom Error Hierarchy

```typescript
// Base application error
class AppError extends Error {
  public readonly code: string;
  public readonly statusCode: number;
  public readonly isOperational: boolean;

  constructor(
    message: string,
    code: string,
    statusCode: number = 500,
    isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    // Fix prototype chain — critical for instanceof to work after transpilation
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

class ValidationError extends AppError {
  public readonly fields: Record<string, string[]>;

  constructor(fields: Record<string, string[]>) {
    super("Validation failed", "VALIDATION_ERROR", 400);
    this.fields = fields;
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`, "NOT_FOUND", 404);
  }
}

class UnauthorizedError extends AppError {
  constructor(reason: string = "Unauthorized") {
    super(reason, "UNAUTHORIZED", 401);
  }
}

class ConflictError extends AppError {
  constructor(message: string) {
    super(message, "CONFLICT", 409);
  }
}

// Error type union for explicit error handling
type ServiceError = ValidationError | NotFoundError | UnauthorizedError | ConflictError;

// Type-safe error handler
function handleServiceError(error: ServiceError): Response {
  if (error instanceof ValidationError) {
    return Response.json({ code: error.code, fields: error.fields }, { status: error.statusCode });
  }
  if (error instanceof NotFoundError) {
    return Response.json({ code: error.code, message: error.message }, { status: error.statusCode });
  }
  return Response.json({ code: error.code, message: error.message }, { status: error.statusCode });
}
```

---

## 27. TypeScript with Async/Await & Promises

```typescript
// Typing async functions
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as Promise<User>; // explicit cast from any
}

// Generic async function
async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as Promise<T>;
}

const user = await fetchJson<User>("/api/user/1"); // Promise<User>
user.name; // OK — TypeScript knows it's User

// Type-safe Promise.all
async function fetchUserAndPosts(userId: string): Promise<[User, Post[]]> {
  return Promise.all([
    fetchJson<User>(`/api/users/${userId}`),
    fetchJson<Post[]>(`/api/users/${userId}/posts`)
  ]);
}

const [user, posts] = await fetchUserAndPosts("1");
user.name;         // User
posts[0].title;    // Post

// AbortController with types
async function fetchWithTimeout<T>(
  url: string,
  timeoutMs: number
): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response.json() as Promise<T>;
  } finally {
    clearTimeout(timeout);
  }
}

// Async generators
async function* paginate<T>(
  fetcher: (page: number, size: number) => Promise<{ data: T[]; hasMore: boolean }>,
  pageSize: number = 20
): AsyncGenerator<T[], void, unknown> {
  let page = 0;
  let hasMore = true;

  while (hasMore) {
    const result = await fetcher(page, pageSize);
    yield result.data;
    hasMore = result.hasMore;
    page++;
  }
}

// Usage
for await (const batch of paginate(fetchUserBatch, 50)) {
  await processUsers(batch);
}
```

---

## 28. Production Patterns for Full-Stack TypeScript

### Type-Safe API Client

```typescript
// Define your API schema as types
interface ApiRoutes {
  "/users": {
    GET: { response: User[] };
    POST: { body: CreateUserDto; response: User };
  };
  "/users/:id": {
    GET: { params: { id: string }; response: User };
    PUT: { params: { id: string }; body: UpdateUserDto; response: User };
    DELETE: { params: { id: string }; response: void };
  };
  "/auth/login": {
    POST: { body: LoginDto; response: { token: string; user: User } };
  };
}

// Generic API client
class ApiClient {
  constructor(private baseUrl: string) {}

  async get<Path extends keyof ApiRoutes>(
    path: Path
  ): Promise<"GET" extends keyof ApiRoutes[Path]
    ? "response" extends keyof ApiRoutes[Path]["GET"]
      ? ApiRoutes[Path]["GET"]["response"]
      : never
    : never> {
    const response = await fetch(`${this.baseUrl}${path}`);
    return response.json();
  }
}
```

### Zod Integration for Runtime Validation

```typescript
import { z } from "zod";

// Define schema (Zod)
const UserSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "user"]),
  createdAt: z.string().datetime()
});

// Infer TypeScript type FROM the schema — single source of truth!
type User = z.infer<typeof UserSchema>;
// { id: number; name: string; email: string; role: "admin" | "user"; createdAt: string }

// Parsing and validation at runtime
function parseUser(input: unknown): User {
  return UserSchema.parse(input); // throws ZodError if invalid
}

function tryParseUser(input: unknown): Result<User> {
  const result = UserSchema.safeParse(input);
  if (result.success) return ok(result.data);
  return err(new ValidationError(
    Object.fromEntries(
      result.error.errors.map(e => [e.path.join("."), [e.message]])
    )
  ));
}

// Request validation middleware
const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });
type CreateUserDto = z.infer<typeof CreateUserSchema>;

// API route with runtime + compile-time safety
app.post("/users", async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.errors });
  }
  const dto: CreateUserDto = result.data; // FULLY TYPED
  const user = await userService.create(dto);
  res.status(201).json(user);
});
```

### Type-Safe Environment Variables

```typescript
import { z } from "zod";

const EnvSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32, "JWT secret must be at least 32 characters"),
  REDIS_URL: z.string().url().optional(),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  CORS_ORIGIN: z.string().default("*"),
  MAX_REQUEST_SIZE: z.coerce.number().default(10 * 1024 * 1024), // 10MB
});

type Env = z.infer<typeof EnvSchema>;

function loadEnv(): Env {
  const result = EnvSchema.safeParse(process.env);
  if (!result.success) {
    console.error("❌ Invalid environment variables:");
    result.error.errors.forEach(err => {
      console.error(`  ${err.path.join(".")}: ${err.message}`);
    });
    process.exit(1);
  }
  return result.data;
}

export const env = loadEnv();
// env.PORT — number (not string!)
// env.NODE_ENV — "development" | "test" | "production"
```

### Dependency Injection with TypeScript

```typescript
// Interface-driven DI
interface ILogger {
  info(message: string, context?: Record<string, unknown>): void;
  error(message: string, error?: Error): void;
  warn(message: string): void;
  debug(message: string): void;
}

interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

interface IPasswordHasher {
  hash(password: string): Promise<string>;
  verify(password: string, hash: string): Promise<boolean>;
}

interface IEventPublisher {
  publish<T>(event: string, payload: T): Promise<void>;
}

// Service class with constructor injection
class UserService {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly hasher: IPasswordHasher,
    private readonly events: IEventPublisher,
    private readonly logger: ILogger
  ) {}

  async createUser(dto: CreateUserDto): Promise<Result<User, ValidationError | ConflictError>> {
    this.logger.info("Creating user", { email: dto.email });

    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      return err(new ConflictError(`User with email ${dto.email} already exists`));
    }

    const passwordHash = await this.hasher.hash(dto.password);
    const user = await this.userRepo.save({
      id: crypto.randomUUID(),
      name: dto.name,
      email: dto.email,
      passwordHash,
      role: dto.role ?? "user",
      createdAt: new Date()
    });

    await this.events.publish("user.created", {
      userId: user.id,
      email: user.email
    });

    this.logger.info("User created successfully", { userId: user.id });
    return ok(user);
  }
}
```

### TypeScript for Message Queue Types (RabbitMQ-style)

```typescript
// Typed message definitions
interface BaseMessage {
  readonly messageId: string;
  readonly timestamp: number;
  readonly version: "1.0" | "2.0";
  readonly correlationId?: string;
}

// Define all message types
type AppMessages = {
  "user.created": BaseMessage & {
    payload: { userId: string; email: string; name: string };
  };
  "user.deleted": BaseMessage & {
    payload: { userId: string; deletedBy: string };
  };
  "order.placed": BaseMessage & {
    payload: {
      orderId: string;
      userId: string;
      items: Array<{ productId: string; quantity: number; price: number }>;
      total: number;
    };
  };
  "payment.processed": BaseMessage & {
    payload: { paymentId: string; orderId: string; success: boolean; amount: number };
  };
};

type MessageType = keyof AppMessages;
type MessagePayload<T extends MessageType> = AppMessages[T];

// Type-safe message publisher
interface IMessagePublisher {
  publish<T extends MessageType>(
    type: T,
    message: Omit<MessagePayload<T>, "messageId" | "timestamp">
  ): Promise<void>;
}

// Type-safe message handler
type MessageHandler<T extends MessageType> = (
  message: MessagePayload<T>
) => Promise<void>;

interface IMessageConsumer {
  subscribe<T extends MessageType>(
    type: T,
    handler: MessageHandler<T>
  ): Promise<void>;
}

// Usage
const publisher: IMessagePublisher = createPublisher();

publisher.publish("user.created", {
  version: "1.0",
  correlationId: "req-123",
  payload: {
    userId: "user-456",
    email: "alice@example.com",
    name: "Alice"
  }
  // messageId and timestamp are added automatically
}); // Fully typed — payload must match AppMessages["user.created"].payload
```

---

## 29. TypeScript Configuration for Monorepos

```json
// tsconfig.base.json — shared settings
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": true
  }
}

// packages/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "lib": ["ES2022"]
  },
  "references": [
    { "path": "../shared" },
    { "path": "../database" }
  ]
}

// packages/web/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx"
  },
  "references": [
    { "path": "../shared" }
  ]
}
```

### Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@components/*": ["./components/*"],
      "@lib/*": ["./lib/*"],
      "@types/*": ["./types/*"]
    }
  }
}
```

```typescript
// Now you can import like this:
import { Button } from "@components/ui/Button";
import { formatDate } from "@lib/utils/date";
import type { User } from "@types/domain";
// Instead of:
import { Button } from "../../../../components/ui/Button";
```

---

## 30. Common Pitfalls & How to Avoid Them

### 1. The `any` Trap

```typescript
// BAD — using any everywhere
function processData(data: any): any {
  return data.map((item: any) => item.value); // no type safety
}

// GOOD — use generics or proper types
function processData<T extends { value: unknown }>(data: T[]): T["value"][] {
  return data.map(item => item.value);
}
```

### 2. Type Assertion Overuse

```typescript
// BAD — forcing TypeScript to accept wrong types
const user = fetchUser() as User; // dangerous if fetchUser can return other things

// GOOD — validate before asserting
const rawData = await fetchUser();
if (!isUser(rawData)) throw new Error("Invalid user data");
const user = rawData; // properly narrowed
```

### 3. Object Index Signature Pitfalls

```typescript
// BAD — all specific properties must match the index signature
interface Config {
  [key: string]: string;
  count: number; // Error! number is not assignable to string
}

// GOOD — use union type in index signature
interface Config {
  [key: string]: string | number;
  count: number; // OK now
  name: string;  // OK
}
```

### 4. Forgetting to Handle `undefined` in Index Access

```typescript
// With noUncheckedIndexedAccess: true
const arr = [1, 2, 3];
const item = arr[10]; // type: number | undefined

// BAD
arr[10].toFixed(2); // Might be undefined!

// GOOD
const item = arr[10];
if (item !== undefined) {
  item.toFixed(2);
}
// Or:
arr[10]?.toFixed(2);
```

### 5. Mutating `Readonly` Arrays

```typescript
// Readonly prevents direct mutation but...
const readonlyArr: readonly number[] = [1, 2, 3];
// readonlyArr.push(4); // Error!

// But you can still spread and create mutable copies
const mutable = [...readonlyArr]; // number[] — now mutable
mutable.push(4); // OK
```

### 6. `strictPropertyInitialization` vs `!` operator

```typescript
class Service {
  // BAD — using ! to silence TypeScript
  private connection!: DatabaseConnection; // "trust me" — but we might forget to initialize

  // GOOD — initialize in constructor
  private connection: DatabaseConnection;

  constructor(config: Config) {
    this.connection = new DatabaseConnection(config);
  }
}

// When ! IS appropriate: when you know initialization happens elsewhere
// (e.g., in a @BeforeEach test hook, or lazy initialization)
class LazyService {
  private _connection: DatabaseConnection | undefined;

  get connection(): DatabaseConnection {
    if (!this._connection) {
      this._connection = new DatabaseConnection();
    }
    return this._connection; // always DatabaseConnection after this
  }
}
```

### 7. `never` for Exhaustive Unions

```typescript
type Status = "active" | "inactive" | "pending";

// BAD — missing "pending" and TypeScript doesn't warn
function handleStatus(status: Status): string {
  if (status === "active") return "Active";
  if (status === "inactive") return "Inactive";
  return "Unknown"; // silently returns "Unknown" for "pending"
}

// GOOD — exhaustive check
function handleStatus(status: Status): string {
  switch (status) {
    case "active": return "Active";
    case "inactive": return "Inactive";
    case "pending": return "Pending";
    default:
      const _exhaustive: never = status; // Error if new status is added!
      return _exhaustive; // never reached
  }
}
```

---

## Quick Reference: TypeScript Cheat Sheet

```typescript
// === TYPES ===
string, number, boolean, null, undefined, bigint, symbol
any, unknown, never, void
object, Object

// === TYPE ANNOTATIONS ===
let x: string = "hello";
function fn(a: string, b?: number): void {}
const arr: string[] = [];
const tuple: [string, number] = ["hello", 42];

// === INTERFACE vs TYPE ===
interface User { id: number; name: string }   // extensible, mergeable
type User = { id: number; name: string }      // more flexible

// === GENERICS ===
function id<T>(x: T): T { return x; }
interface Box<T> { value: T }
class Stack<T> { items: T[] = [] }

// === UTILITY TYPES ===
Partial<T>        // all optional
Required<T>       // all required
Readonly<T>       // all readonly
Pick<T, K>        // keep only K
Omit<T, K>        // remove K
Record<K, V>      // { [key in K]: V }
Extract<T, U>     // T & U (union intersection)
Exclude<T, U>     // T - U (set difference)
NonNullable<T>    // remove null | undefined
ReturnType<T>     // return type of function
Parameters<T>     // parameter types of function
Awaited<T>        // unwrap Promise<T>

// === TYPE OPERATORS ===
keyof T           // union of keys
typeof x          // type of value
T[K]              // indexed access
T extends U ? A : B  // conditional type
infer R           // type inference in conditional types
T & U             // intersection
T | U             // union

// === MODIFIERS ===
readonly          // cannot reassign
?                 // optional
-?                // remove optional
-readonly         // remove readonly
!                 // non-null assertion

// === NARROWING ===
typeof, instanceof, in, truthy/falsy, ==, switch
type guards: value is Type
assertion functions: asserts condition

// === MAPPED TYPES ===
{ [K in keyof T]: T[K] }
{ [K in keyof T as NewKey]: T[K] }
{ readonly [K in keyof T]?: T[K] }
```

---

*This guide covers every TypeScript feature needed for a TypeScript-first full-stack role. The next file covers React & Next.js.*
