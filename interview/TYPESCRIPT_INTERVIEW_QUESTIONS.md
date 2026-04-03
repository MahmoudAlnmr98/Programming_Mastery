# TypeScript — Interview Questions & Answers (Complete Reference)
> 120 questions. Full code answers. Easy → Medium → Hard. Covers type system internals, generics, advanced patterns, compiler, and real-world usage.

---

## Table of Contents
- [Easy Questions (Q1–Q35)](#easy-questions)
- [Medium Questions (Q36–Q75)](#medium-questions)
- [Hard Questions (Q76–Q120)](#hard-questions)

---

## EASY QUESTIONS

---

**Q1. What is TypeScript and why use it over JavaScript?**

TypeScript is a statically typed superset of JavaScript developed by Microsoft. It compiles to plain JavaScript and adds optional static typing, interfaces, generics, enums, and richer IDE tooling.

Key benefits:
- **Catch bugs at compile time** before they hit production
- **Autocomplete and IntelliSense** — IDE knows what methods exist on every value
- **Self-documenting code** — types replace many comments
- **Safer refactoring** — the compiler catches every broken reference
- **Latest JS features** — TypeScript compiles modern syntax down to any target

All valid JavaScript is valid TypeScript — TypeScript is a strict superset.

---

**Q2. What are the basic types in TypeScript?**

```typescript
// Primitives:
let name: string = "Alice";
let age: number = 30;
let active: boolean = true;
let nothing: null = null;
let missing: undefined = undefined;
let id: symbol = Symbol("id");
let big: bigint = 9007199254740991n;

// Special / top types:
let anything: any = "bypass the type system — avoid!";
let safe: unknown = "must narrow before use";

// Bottom type:
function fail(msg: string): never { throw new Error(msg); }

// Void:
function log(msg: string): void { console.log(msg); }

// Arrays:
let nums: number[] = [1, 2, 3];
let strs: Array<string> = ["a", "b"];

// Tuple — fixed-length, typed positions:
let pair: [string, number] = ["Alice", 30];
let triple: [string, number, boolean] = ["x", 1, true];

// Object literal type:
let user: { name: string; age: number; role?: string } = { name: "Alice", age: 30 };
```

---

**Q3. What is the difference between `interface` and `type`?**

```typescript
// INTERFACE — designed for object shapes, supports extension and declaration merging
interface User {
  id: number;
  name: string;
  email?: string; // optional
  readonly createdAt: Date; // readonly
}

interface Admin extends User {
  role: "admin";
  permissions: string[];
}

// Declaration merging — only interfaces support this:
interface Window { myPlugin: Plugin; }
interface Window { analytics: Analytics; } // merged with the first Window!

// TYPE ALIAS — more flexible, works for any type
type ID = string | number;                 // union — can't do with interface
type Point = { x: number; y: number };
type Callback = (err: Error | null) => void;
type Grid = Point[][];                     // nested

// Intersection (similar to extends):
type AdminUser = User & { role: string; permissions: string[] };

// PRACTICAL RULE:
// Use `interface` for: public APIs of libraries, class contracts, object shapes
// Use `type` for: unions, intersections, tuples, mapped types, utility type results
// In most codebases: either works for objects — pick one and be consistent
```

---

**Q4. What are union and intersection types?**

```typescript
// UNION (A | B) — value is type A OR type B
type StringOrNumber = string | number;
type Status = "pending" | "active" | "inactive"; // string literal union

function format(value: string | number): string {
  if (typeof value === "string") return value.toUpperCase(); // narrowed
  return value.toFixed(2);                                   // narrowed
}

// INTERSECTION (A & B) — value satisfies BOTH A and B
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged; // { name: string; age: number }

const p: Person = { name: "Alice", age: 30 }; // must satisfy both

// Discriminated union — union with a shared literal field:
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle":  return Math.PI * s.radius ** 2;
    case "square":  return s.side ** 2;
    case "rect":    return s.w * s.h;
  }
}
```

---

**Q5. What are generics?**

```typescript
// Generics — parameterize types, reuse logic across many types

// Generic function:
function identity<T>(value: T): T { return value; }
identity<string>("hello"); // T = string, explicit
identity(42);              // T = number, inferred

// Generic constraint:
function getLength<T extends { length: number }>(val: T): number {
  return val.length;
}
getLength("hello"); getLength([1,2,3]); // OK
getLength(42);      // Error — number has no .length

// Generic interface:
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic class:
class Stack<T> {
  #items: T[] = [];
  push(item: T)   { this.#items.push(item); }
  pop(): T | undefined { return this.#items.pop(); }
  peek(): T | undefined { return this.#items.at(-1); }
  get isEmpty() { return this.#items.length === 0; }
}

const stack = new Stack<number>();
stack.push(1);
stack.push("x"); // Error! string not assignable to number

// Multiple type parameters:
function zip<A, B>(as: A[], bs: B[]): [A, B][] {
  return as.map((a, i) => [a, bs[i]]);
}
zip([1, 2], ["a", "b"]); // [[1,"a"],[2,"b"]]
```

---

**Q6. What are the built-in utility types?**

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
  createdAt: Date;
}

// Partial<T> — all properties optional
type Draft = Partial<User>;
// { id?: number; name?: string; ... }

// Required<T> — all properties required
type FullUser = Required<Draft>;

// Readonly<T> — all properties readonly
type Frozen = Readonly<User>;
const u: Frozen = { id:1, name:"Alice", email:"", role:"user", createdAt: new Date() };
u.name = "Bob"; // Error!

// Pick<T, K> — keep only listed keys
type Preview = Pick<User, "id" | "name">;

// Omit<T, K> — exclude listed keys
type PublicUser = Omit<User, "email">;

// Record<K, V> — object with keys K and values V
type Roles = Record<"admin" | "user", string[]>;

// Exclude<T, U> — remove from union
type NonString = Exclude<string | number | boolean, string>; // number | boolean

// Extract<T, U> — keep only assignable to U
type Strings = Extract<string | number | boolean, string | symbol>; // string

// NonNullable<T>
type Safe = NonNullable<string | null | undefined>; // string

// ReturnType<T>
type FetchRet = ReturnType<typeof fetch>; // Promise<Response>

// Parameters<T>
type FetchArgs = Parameters<typeof fetch>; // [input: RequestInfo | URL, init?: RequestInit]

// InstanceType<T>
type Client = InstanceType<typeof Map>; // Map<any, any>

// Awaited<T> — unwrap promise
type Data = Awaited<Promise<string>>; // string
```

---

**Q7. What is type narrowing?**

```typescript
function process(input: string | number | null | Date) {
  // typeof guard:
  if (typeof input === "string") {
    input.toUpperCase(); // string
  } else if (typeof input === "number") {
    input.toFixed(2);    // number

  // instanceof guard:
  } else if (input instanceof Date) {
    input.toISOString(); // Date

  // equality / truthiness:
  } else {
    input; // null — only remaining type
  }

  // Truthiness narrowing:
  if (input) {
    input; // string | number | Date (null removed)
  }

  // in operator:
  if (input && typeof input === "object" && "getTime" in input) {
    input.getTime(); // Date narrowed
  }
}

// Discriminated union narrowing:
type Result<T> =
  | { ok: true;  data: T }
  | { ok: false; error: string };

function handle<T>(r: Result<T>) {
  if (r.ok) {
    r.data;  // T — narrowed by `ok: true`
  } else {
    r.error; // string — narrowed by `ok: false`
  }
}

// Array narrowing with Array.isArray:
function logAll(value: string | string[]) {
  const arr = Array.isArray(value) ? value : [value];
  arr.forEach(s => console.log(s.toUpperCase()));
}
```

---

**Q8. What are type guards?**

```typescript
// User-defined type guard — return type `value is Type`
interface Cat { meow(): void; legs: number; }
interface Dog { bark(): void; legs: number; }

function isCat(animal: Cat | Dog): animal is Cat {
  return "meow" in animal; // runtime check
}

function makeSound(animal: Cat | Dog) {
  if (isCat(animal)) {
    animal.meow(); // TypeScript knows Cat here
  } else {
    animal.bark(); // TypeScript knows Dog here
  }
}

// Generic type guard:
function isArrayOf<T>(
  arr: unknown[],
  guard: (x: unknown) => x is T
): arr is T[] {
  return arr.every(guard);
}

function isString(x: unknown): x is string {
  return typeof x === "string";
}

const mixed: unknown[] = ["a", "b", "c"];
if (isArrayOf(mixed, isString)) {
  mixed.map(s => s.toUpperCase()); // safe — all strings
}

// Assertion functions (throws instead of returning bool):
function assertDefined<T>(val: T): asserts val is NonNullable<T> {
  if (val == null) throw new Error("Expected defined value");
}

function processUser(user: User | null) {
  assertDefined(user);
  user.name; // TypeScript knows non-null after assertion
}
```

---

**Q9. What is `unknown` vs `any` vs `never`?**

```typescript
// ANY — opts out of type checking completely
let a: any = "hello";
a.toUpperCase(); // OK
a.nonExistent(); // OK — no error, potential runtime crash
a = 42;          // OK

// UNKNOWN — type-safe top type (safer alternative to any)
let u: unknown = "hello";
u.toUpperCase(); // Error! Must narrow first
u = 42;          // OK — can assign anything

if (typeof u === "string") u.toUpperCase(); // OK — narrowed

// Use unknown for:
// - Values from external sources (JSON.parse, fetch responses)
// - Error objects in catch (default in strict mode)
try {} catch (e: unknown) {
  if (e instanceof Error) e.message; // safe
}

// NEVER — represents impossible / bottom type
// 1. Functions that never return:
function crash(msg: string): never { throw new Error(msg); }

// 2. Exhaustive checks:
type Color = "red" | "green" | "blue";
function getHex(c: Color): string {
  switch (c) {
    case "red":   return "#ff0000";
    case "green": return "#00ff00";
    case "blue":  return "#0000ff";
    default:
      const _: never = c; // if we miss a case, error here
      return crash(`Unknown color: ${c}`);
  }
}

// 3. Impossible intersections:
type Impossible = string & number; // never
```

---

**Q10. What are enums and when should you avoid them?**

```typescript
// Numeric enum — auto-increments, has REVERSE MAPPING:
enum Direction { Up = 0, Down, Left, Right }
Direction.Up;    // 0
Direction[0];    // "Up" — reverse mapping exists at runtime!

// String enum — no reverse mapping, more debuggable:
enum Status {
  Pending = "PENDING",
  Active  = "ACTIVE",
  Done    = "DONE",
}

// Const enum — inlined at compile time (no runtime object):
const enum Color { Red, Green, Blue }
const c = Color.Red; // compiles to: const c = 0

// WHY TO AVOID ENUMS:
// 1. Numeric enums accept ANY number — not type-safe!
const move = (d: Direction) => {};
move(999); // No error! Bug.

// 2. Const enums break with isolatedModules (Vite, esbuild, Babel)
// 3. Emit extra runtime code (unless const)
// 4. Confusing reverse mapping

// PREFERRED ALTERNATIVE — object + as const:
const StatusConst = {
  Pending: "PENDING",
  Active:  "ACTIVE",
  Done:    "DONE",
} as const;

type Status = typeof StatusConst[keyof typeof StatusConst];
// "PENDING" | "ACTIVE" | "DONE" — fully type-safe, no magic

// Or just string literal union:
type Dir = "up" | "down" | "left" | "right";
```

---

**Q11. What are mapped types?**

```typescript
// Mapped types transform every property of a type

// Building Readonly from scratch:
type MyReadonly<T> = { readonly [K in keyof T]: T[K] };

// Building Partial from scratch:
type MyPartial<T> = { [K in keyof T]?: T[K] };

// Remove modifiers with -readonly and -?:
type Mutable<T>   = { -readonly [K in keyof T]: T[K] };
type Complete<T>  = { [K in keyof T]-?: T[K] };

// Transform values:
type Nullable<T>  = { [K in keyof T]: T[K] | null };
type Stringify<T> = { [K in keyof T]: string };

// Filter properties using `as` (TypeScript 4.1+):
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K]
};

interface User { id: number; name: string; age: number; active: boolean }
type NumberProps = PickByValue<User, number>; // { id: number; age: number }

// Remap keys:
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};
type UserGetters = Getters<{ name: string; age: number }>;
// { getName: () => string; getAge: () => number }
```

---

**Q12. What are conditional types?**

```typescript
// T extends U ? X : Y

// Basic:
type IsString<T> = T extends string ? true : false;
type A = IsString<string>; // true
type B = IsString<number>; // false

// Infer — extract type within conditional:
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type Resolved = UnwrapPromise<Promise<string>>; // string
type Plain    = UnwrapPromise<number>;           // number

// Recursive unwrapping:
type DeepAwaited<T> =
  T extends Promise<infer U> ? DeepAwaited<U> : T;

type Deep = DeepAwaited<Promise<Promise<string>>>; // string

// Extract tuple head and tail:
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;
type Tail<T extends any[]> = T extends [any, ...infer R]   ? R : never;
type H = Head<[string, number, boolean]>; // string
type R = Tail<[string, number, boolean]>; // [number, boolean]

// Distributive conditional — distributes over union:
type Wrap<T> = T extends any ? T[] : never;
type Wrapped = Wrap<string | number>; // string[] | number[]

// Prevent distribution with tuple:
type WrapAll<T> = [T] extends [any] ? T[] : never;
type WrappedAll = WrapAll<string | number>; // (string | number)[]
```

---

**Q13. What are template literal types?**

```typescript
// String types built from combinations of literal types

type Color = "red" | "green" | "blue";
type Size  = "sm" | "md" | "lg";

type ColorSize = `${Color}-${Size}`;
// "red-sm" | "red-md" | ... (9 total)

// CSS helper:
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;
const width: CSSValue = "100px"; // OK
const bad: CSSValue   = "100pt"; // Error

// Event naming:
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

// Generate getter/setter API from type:
type Getters<T extends Record<string, unknown>> = {
  [K in string & keyof T as `get${Capitalize<K>}`]: () => T[K]
};
type Setters<T extends Record<string, unknown>> = {
  [K in string & keyof T as `set${Capitalize<K>}`]: (v: T[K]) => void
};

// Intrinsic string types:
type U = Uppercase<"hello">;   // "HELLO"
type L = Lowercase<"WORLD">;   // "world"
type C = Capitalize<"hello">;  // "Hello"
type D = Uncapitalize<"Hello">;// "hello"

// Route parameters:
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"
```

---

**Q14. What is the `satisfies` operator?**

```typescript
// Problem: type annotation widens and loses specific information
const palette: Record<string, string | number[]> = {
  red: [255, 0, 0],
  green: "#00ff00",
};
palette.red.map(v => v * 2); // Error! TS thinks it's string | number[]

// satisfies — validates type WITHOUT widening
const palette2 = {
  red:   [255, 0, 0],
  green: "#00ff00",
} satisfies Record<string, string | number[]>;

palette2.red.map(v => v * 2);   // OK — TS knows it's number[]
palette2.green.toUpperCase();   // OK — TS knows it's string

// Another example: config validation
type Config = { port: number; host: string; debug?: boolean };

const config = {
  port: 3000,
  host: "localhost",
  debug: false,
} satisfies Config; // validates shape

config.port.toFixed(); // OK — TS knows port is number, not number | undefined

// Works great with `as const`:
const ROUTES = {
  home:    "/",
  users:   "/users",
  profile: "/users/:id",
} as const satisfies Record<string, string>;
// Each value keeps its literal type AND is validated as string
```

---

**Q15. What are declaration files and module augmentation?**

```typescript
// Declaration files (.d.ts) — type-only, no implementation

// Describing a JS library (no built-in types):
// math.d.ts
export declare function add(a: number, b: number): number;
export declare const PI: number;

// Global variable:
declare global {
  var __DEV__: boolean;
  var __VERSION__: string;
}

// MODULE AUGMENTATION — add types to existing modules:
// In Express, add `user` to Request:
declare module "express-serve-static-core" {
  interface Request {
    user?: { id: string; role: "admin" | "user" };
    requestId: string;
  }
}

// Usage in route handler:
app.get("/profile", (req, res) => {
  req.user?.id;     // TypeScript accepts this now
  req.requestId;    // TypeScript accepts this now
});

// Augment built-in Array:
declare global {
  interface Array<T> {
    last(): T | undefined;
    groupBy<K extends string>(fn: (item: T) => K): Record<K, T[]>;
  }
}

Array.prototype.last = function() { return this[this.length - 1]; };
[1, 2, 3].last(); // OK — TypeScript knows about .last()
```

---

**Q16. What are decorators in TypeScript?**

```typescript
// Enable: "experimentalDecorators": true in tsconfig (legacy/stage 2)
// Stage 3 decorators are landing without the flag

// Class decorator:
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class BugReport {
  type = "report";
  title: string;
  constructor(t: string) { this.title = t; }
}

// Factory decorator (returns decorator):
function Route(path: string, method = "GET") {
  return function(target: any, key: string, descriptor: PropertyDescriptor) {
    Reflect.defineMetadata("route", { path, method }, target, key);
    return descriptor;
  };
}

class UserController {
  @Route("/users", "GET")
  list() {}

  @Route("/users/:id", "GET")
  findOne() {}

  @Route("/users", "POST")
  create() {}
}

// Method decorator — logging:
function log(target: any, key: string, desc: PropertyDescriptor) {
  const orig = desc.value;
  desc.value = function(...args: any[]) {
    console.log(`▶ ${key}(${args.join(", ")})`);
    const result = orig.apply(this, args);
    console.log(`◀ ${key} → ${result}`);
    return result;
  };
}

class MathService {
  @log
  add(a: number, b: number) { return a + b; }
}
new MathService().add(2, 3);
// ▶ add(2, 3)
// ◀ add → 5
```

---

**Q17. What is `readonly` and `as const`?**

```typescript
// readonly on individual property:
interface Config {
  readonly port: number;
  readonly host: string;
}
const c: Config = { port: 3000, host: "localhost" };
c.port = 8080; // Error!

// readonly arrays:
function process(items: readonly number[]) {
  items.push(4);  // Error — readonly
  items.map(x => x * 2); // OK — non-mutating
}

// as const — freeze literals AND narrow types:
const directions = ["up", "down", "left", "right"] as const;
// type: readonly ["up", "down", "left", "right"]
// NOT: string[]

type Direction = typeof directions[number];
// "up" | "down" | "left" | "right"

const config = {
  port: 3000,        // type: 3000 (literal), not number
  host: "localhost", // type: "localhost", not string
  features: ["auth", "rate-limit"] as const,
} as const;

config.port = 8080;            // Error!
config.features.push("extra"); // Error — readonly tuple

// Combining: satisfies + as const
const STATUS = {
  Pending:  "PENDING",
  Active:   "ACTIVE",
  Inactive: "INACTIVE",
} as const satisfies Record<string, string>;

type Status = typeof STATUS[keyof typeof STATUS];
// "PENDING" | "ACTIVE" | "INACTIVE"
```

---

**Q18. What is `keyof` and indexed access types?**

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}

// keyof — union of all keys
type UserKeys = keyof User; // "id" | "name" | "email" | "role"

// Indexed access — lookup type of a property
type NameType = User["name"];          // string
type RoleType = User["role"];          // "admin" | "user"
type IdOrName = User["id" | "name"];   // number | string

// keyof + indexed access — safe property access:
function pluck<T, K extends keyof T>(obj: T, keys: K[]): T[K][] {
  return keys.map(k => obj[k]);
}

const user: User = { id:1, name:"Alice", email:"a@b.com", role:"user" };
pluck(user, ["name", "email"]); // string[]  ✅
pluck(user, ["id", "name"]);    // (number | string)[] ✅
pluck(user, ["age"]);           // Error! "age" not in keyof User

// Nested indexed access:
type Address = { city: string; zip: { code: string; plus4?: string } };
type ZipCode = Address["zip"]["code"]; // string

// From value to type:
const routes = { home: "/", users: "/users" } as const;
type RouteKey = keyof typeof routes;   // "home" | "users"
type RoutePath = typeof routes[RouteKey]; // "/" | "/users"

// Array element type:
const fruits = ["apple", "banana", "cherry"] as const;
type Fruit = typeof fruits[number]; // "apple" | "banana" | "cherry"
```

---

**Q19. What is structural typing and excess property checking?**

```typescript
// TypeScript uses STRUCTURAL typing — shape matters, not name
interface Named { name: string }

class Dog { name = "Rex"; bark() {} }
class Cat { name = "Whiskers"; meow() {} }

// Both compatible with Named — structurally match
function greet(n: Named) { console.log(n.name); }
greet(new Dog()); // OK
greet(new Cat()); // OK
greet({ name: "Frank", age: 30 }); // OK — has at least .name

// This differs from Java (nominal) where Dog must explicitly implement Named

// EXCESS PROPERTY CHECKING — only on direct object literals:
interface User { name: string; age: number }

const u: User = { name: "Alice", age: 30, extra: true }; // Error! 'extra' unexpected

// But via variable: no excess property check
const obj = { name: "Alice", age: 30, extra: true };
const u2: User = obj; // OK — structurally compatible

// {} type — means "any non-null value" (not empty object!):
const s: {} = "hello"; // OK — string satisfies {}
const n: {} = 42;      // OK — number satisfies {}

// Use Record<string, never> or object for truly "no properties":
const empty: Record<string, never> = {};
empty.x = 1; // Error!
```

---

**Q20. What is TypeScript's `strict` mode and its options?**

```typescript
// "strict": true in tsconfig.json enables ALL these:

// 1. strictNullChecks — null/undefined are separate types
let name: string = null; // Error! Must be: string | null

// 2. noImplicitAny — all params must be typed
function bad(x) { return x; } // Error — x implicitly any
function good(x: unknown) { return x; } // OK

// 3. strictFunctionTypes — proper function type variance
type Handler = (a: Animal) => void;
const dogHandler: (a: Dog) => void = (a: Animal) => {}; // OK — contravariant
const wrong: (a: Animal) => void = (a: Dog) => a.bark(); // Error — not sound

// 4. strictPropertyInitialization — class properties must be initialized
class Foo {
  x: number;     // Error! Not initialized
  y = 0;         // OK
  z!: number;    // OK — non-null assertion: "I'll handle this"
}

// 5. noImplicitThis — `this` must have explicit type
function bad2() { return this.name; } // Error — `this` is implicit any

// 6. useUnknownInCatchVariables — errors are unknown
try {} catch(e) {
  e.message;                    // Error — e is unknown
  if (e instanceof Error) e.message; // OK
}

// 7. exactOptionalPropertyTypes — stricter optional handling
interface Opts { debug?: boolean }
const o: Opts = { debug: undefined }; // Error with exactOptionalPropertyTypes!
// undefined is not the same as "property absent"
```

---

**Q21. What is the difference between `abstract class` and `interface`?**

```typescript
// INTERFACE — pure contract, no implementation, no runtime code
interface Flyable {
  fly(): void;
  readonly maxAltitude: number;
}
interface Swimmable {
  swim(): void;
}
// A class can implement multiple interfaces:
class Duck implements Flyable, Swimmable {
  maxAltitude = 1000;
  fly()  { console.log("flying"); }
  swim() { console.log("swimming"); }
}

// ABSTRACT CLASS — can have implementation + abstract members
// Can only extend ONE abstract class
abstract class Animal {
  abstract makeSound(): string; // must implement
  abstract name: string;        // must implement

  // Concrete shared implementation:
  move(meters: number): string {
    return `${this.name} moved ${meters}m`;
  }
  describe(): string {
    return `${this.name} says: ${this.makeSound()}`;
  }
}

// Cannot instantiate:
new Animal(); // Error!

class Dog extends Animal {
  name = "Dog";
  makeSound() { return "Woof!"; }
  // move() inherited from Animal
}

// WHEN TO USE EACH:
// Interface: defining a contract for unrelated classes (Serializable, Comparable)
// Abstract class: sharing implementation among related classes (Animal → Dog/Cat)
```

---

**Q22. What are function overloads in TypeScript?**

```typescript
// Multiple call signatures + one implementation:

// Overload signatures (no body):
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "input"): HTMLInputElement;
function createElement(tag: "canvas"): HTMLCanvasElement;
function createElement(tag: string): HTMLElement;

// Implementation (handles all cases):
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

const div    = createElement("div");    // HTMLDivElement  ✅
const input  = createElement("input"); // HTMLInputElement ✅
const el     = createElement("p");     // HTMLElement     ✅

// Class method overloads:
class Formatter {
  format(value: string): string;
  format(value: number, decimals?: number): string;
  format(value: string | number, decimals = 2): string {
    if (typeof value === "string") return value.trim();
    return value.toFixed(decimals);
  }
}

// Interface overloads (call signatures):
interface Transform {
  (input: string): string;
  (input: number): number;
  (input: boolean): string;
}

// Overloads + generics:
function first<T>(arr: [T, ...any[]]): T;
function first<T>(arr: T[]): T | undefined;
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

---

**Q23. What are TypeScript's `Exclude`, `Extract`, and `NonNullable`?**

```typescript
// All built from conditional types

type T = string | number | boolean | null | undefined | symbol;

// Exclude<T, U> — remove from T members assignable to U
type A = Exclude<T, null | undefined>;   // string | number | boolean | symbol
type B = Exclude<T, string | symbol>;    // number | boolean | null | undefined

// Extract<T, U> — keep only members assignable to U
type C = Extract<T, string | number>;    // string | number
type D = Extract<T, null | undefined>;   // null | undefined

// NonNullable<T> — Exclude<T, null | undefined>
type E = NonNullable<string | null | undefined>; // string

// Building them from scratch:
type MyExclude<T, U> = T extends U ? never : T;
type MyExtract<T, U> = T extends U ? T : never;
type MyNonNullable<T> = T extends null | undefined ? never : T;

// Practical usage:
type EventMap = {
  click: MouseEvent;
  keydown: KeyboardEvent;
  focus: FocusEvent;
  wheel: WheelEvent;
};

type MouseEventNames = Extract<keyof EventMap, "click" | "wheel" | "nonExistent">;
// "click" | "wheel" — only existing keys

type NonMouseEvents = Exclude<keyof EventMap, "click" | "wheel">;
// "keydown" | "focus"
```

---

**Q24. What is `ReturnType`, `Parameters`, and `InstanceType`?**

```typescript
// ReturnType<T> — type of what function returns
function fetchUser(id: string) {
  return { id, name: "Alice", createdAt: new Date() };
}
type User = ReturnType<typeof fetchUser>;
// { id: string; name: string; createdAt: Date }

// Works with generics too:
async function loadData<T>(url: string): Promise<T> {
  const res = await fetch(url);
  return res.json();
}
type LoadDataReturn = ReturnType<typeof loadData>; // Promise<unknown>

// Parameters<T> — tuple of parameter types
type FetchParams = Parameters<typeof fetch>;
// [input: RequestInfo | URL, init?: RequestInit]

// Use to forward parameters:
function withLogging<T extends (...args: any[]) => any>(fn: T) {
  return function(...args: Parameters<T>): ReturnType<T> {
    console.log("calling with", args);
    return fn(...args);
  };
}

// InstanceType<T> — type of class instance
class Connection {
  query(sql: string): Promise<unknown[]> { return Promise.resolve([]); }
  close(): void {}
}
type ConnInstance = InstanceType<typeof Connection>;
// Connection — same as just using Connection type, but useful with generics:

function createInstance<T extends new (...args: any) => any>(
  Ctor: T,
  ...args: ConstructorParameters<T>
): InstanceType<T> {
  return new Ctor(...args);
}
```

---

**Q25. What is `namespace` in TypeScript?**

```typescript
// Namespaces — TypeScript's way to organize code in the global scope
// Mostly used in declaration files today; prefer ESM modules in application code

namespace Validation {
  export interface StringValidator {
    isAcceptable(s: string): boolean;
  }

  const lettersRegexp = /^[A-Za-z]+$/;
  const numberRegexp = /^[0-9]+$/;

  export class LettersOnlyValidator implements StringValidator {
    isAcceptable(s: string) { return lettersRegexp.test(s); }
  }

  export class ZipCodeValidator implements StringValidator {
    isAcceptable(s: string) {
      return s.length === 5 && numberRegexp.test(s);
    }
  }
}

const validator: Validation.StringValidator = new Validation.LettersOnlyValidator();

// Namespace merging:
namespace Animals {
  export class Dog { bark() {} }
}
namespace Animals {
  export class Cat { meow() {} }
}
// Now Animals has both Dog and Cat

// Namespace + class (companion namespace pattern):
class Order { id: string = ""; }
namespace Order {
  export function create(id: string): Order {
    const o = new Order(); o.id = id; return o;
  }
  export type Status = "pending" | "shipped" | "delivered";
}
```

---

**Q26. What is `Omit` vs `Pick` vs `Partial` and when to use each?**

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  stock: number;
  createdAt: Date;
  updatedAt: Date;
}

// Pick — I know exactly which fields I want:
type ProductPreview = Pick<Product, "id" | "name" | "price">;
// Use for: DTOs, API responses with fewer fields, view models

// Omit — I want everything EXCEPT certain fields:
type CreateProductInput = Omit<Product, "id" | "createdAt" | "updatedAt">;
// { name: string; price: number; stock: number }
// Use for: create/update DTOs (remove auto-generated fields)

// Partial — all fields optional:
type UpdateProductInput = Partial<Omit<Product, "id" | "createdAt" | "updatedAt">>;
// { name?: string; price?: number; stock?: number; updatedAt?: Date }
// Use for: PATCH endpoints, update inputs

// Required — ensure all fields are present:
type CompleteProduct = Required<Product>;
// Use for: after validation, all fields must exist

// Combining:
type PatchProduct = Pick<Partial<Product>, "name" | "price" | "stock">;
// Only these three, all optional

// Real-world CRUD types:
type CreateInput  = Omit<Product, "id" | "createdAt" | "updatedAt">;
type UpdateInput  = Partial<CreateInput> & { id: string };
type ReadResponse = Product;
type ListItem     = Pick<Product, "id" | "name" | "price">;
```

---

**Q27. How does TypeScript handle `this` in classes and arrow functions?**

```typescript
class EventHandler {
  name = "handler";
  private count = 0;

  // Regular method — `this` depends on HOW it's called:
  regularMethod() {
    return this.name; // works if called as obj.regularMethod()
  }

  // Arrow field — `this` is always the instance (bound at creation):
  arrowMethod = () => {
    return this.name; // always correct, even when extracted
  };

  // `this` parameter (type annotation, stripped at runtime):
  typedMethod(this: EventHandler) {
    return this.name;
  }
}

const handler = new EventHandler();
const regular = handler.regularMethod;
const arrow   = handler.arrowMethod;

regular(); // undefined — `this` is lost!
arrow();   // "handler" — `this` is bound ✅

// Fluent builder with `this` return type:
class Builder {
  protected data: Record<string, unknown> = {};

  set(key: string, value: unknown): this { // `this` = subclass type
    this.data[key] = value;
    return this; // returns actual subclass, not just Builder
  }

  build() { return this.data; }
}

class QueryBuilder extends Builder {
  where(condition: string): this {
    this.data.where = condition;
    return this;
  }
}

new QueryBuilder()
  .set("table", "users")
  .where("age > 18")
  .build(); // QueryBuilder throughout the chain
```

---

**Q28. What are index signatures and their limitations?**

```typescript
// Index signature — object with dynamic keys
interface StringMap {
  [key: string]: string;
}
const m: StringMap = { a: "1", b: "2" };

// Known properties must match index signature type:
interface MixedMap {
  name: string;          // OK — string matches [key: string]: string
  count: number;         // Error! number not assignable to string
  [key: string]: string;
}

// Fix: broaden index signature:
interface FlexMap {
  name: string;
  count: number;
  [key: string]: string | number; // union covers both
}

// noUncheckedIndexedAccess (strict option):
// With this option, index access returns T | undefined:
const map: StringMap = { a: "hello" };
const val = map["b"]; // string | undefined (with noUncheckedIndexedAccess)
val.toUpperCase();     // Error! might be undefined

// Template literal index:
interface EventHandlers {
  [key: `on${Capitalize<string>}`]: (...args: any[]) => void;
}
const h: EventHandlers = {
  onClick: () => {},
  onHover: () => {},
  name: () => {}, // Error! doesn't match `on${Capitalize<string>}`
};

// Record<K, V> is preferred over index signature when keys are known:
type FixedMap = Record<"a" | "b" | "c", number>;
// { a: number; b: number; c: number }
```

---

**Q29. What is `Awaited<T>` and how to type async operations correctly?**

```typescript
// Awaited<T> — unwrap promise types (built-in since TS 4.5)
type A = Awaited<Promise<string>>;            // string
type B = Awaited<Promise<Promise<number>>>;   // number — recursive!
type C = Awaited<string | Promise<number>>;  // string | number

// Typing async functions:
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json() as Promise<User>;
}

// Infer resolved type:
type UserType = Awaited<ReturnType<typeof fetchUser>>; // User

// Type-safe Result pattern for error handling:
type Ok<T>  = { success: true;  data: T };
type Err<E> = { success: false; error: E };
type Result<T, E = Error> = Ok<T> | Err<E>;

async function safeAsync<T>(
  fn: () => Promise<T>
): Promise<Result<T>> {
  try {
    return { success: true, data: await fn() };
  } catch (e) {
    return { success: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

const result = await safeAsync(() => fetchUser("1"));
if (result.success) {
  result.data.name; // User — fully typed
} else {
  result.error.message; // Error — fully typed
}
```

---

**Q30. What is TypeScript's module resolution?**

```typescript
// Module resolution — how TypeScript finds the file for an import

// "moduleResolution": "NodeNext" (recommended for Node.js):
// Requires explicit file extensions:
import { foo } from "./foo.js"; // even though file is .ts!

// "moduleResolution": "Bundler" (for Vite/webpack/esbuild):
// No extension required — bundler handles it:
import { foo } from "./foo";

// "paths" — path aliases:
// tsconfig.json:
// "baseUrl": ".",
// "paths": { "@/*": ["./src/*"], "@utils/*": ["./src/utils/*"] }
import { formatDate } from "@/utils/date";

// "types" — which @types packages to include:
// "types": ["node", "jest"] — only include these

// Type-only imports (stripped entirely at runtime):
import type { User } from "./types";
import { type User, createUser } from "./user"; // mixed

// ESM vs CJS in .d.ts:
// .d.mts — for ESM-only declaration files
// .d.cts — for CJS-only declaration files
// .d.ts  — ambient (matches host module system)

// package.json "exports" field with types:
// {
//   "exports": {
//     ".": {
//       "types": "./dist/index.d.ts",
//       "import": "./dist/index.mjs",
//       "require": "./dist/index.cjs"
//     }
//   }
// }
```

---

**Q31. What is `Pick` with conditional filtering?**

```typescript
// Filter object properties by value type

type FilterByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K]
};

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  active: boolean;
  createdAt: Date;
}

type StringFields  = FilterByValue<User, string>;
// { name: string; email: string }

type NumberFields  = FilterByValue<User, number>;
// { id: number; age: number }

type PrimitiveFields = FilterByValue<User, string | number | boolean>;
// { id, name, email, age, active }

// Inverse — exclude by value type:
type NonPrimitiveFields<T> = {
  [K in keyof T as T[K] extends string | number | boolean | null | undefined
    ? never
    : K]: T[K]
};

type ObjectFields = NonPrimitiveFields<User>;
// { createdAt: Date }

// Deep partial only for nested objects:
type DeepPartialObjects<T> = {
  [K in keyof T]: T[K] extends object ? Partial<T[K]> : T[K]
};
```

---

**Q32. How does TypeScript's `infer` work with function overloads?**

```typescript
// When inferring from overloaded functions, TypeScript uses the LAST overload

function parse(input: string): number;
function parse(input: number): string;
function parse(input: string | number): number | string {
  if (typeof input === "string") return parseInt(input);
  return String(input);
}

// ReturnType uses last overload:
type ParseReturn = ReturnType<typeof parse>; // number | string (last overload)

// To get specific overload return type — use conditional inference:
type StringOverloadReturn =
  typeof parse extends (input: string) => infer R ? R : never;
// number ✅

// Overload union inference:
type AllReturns<T extends (...args: any) => any> =
  T extends { (...args: any): infer R1; (...args: any): infer R2 }
    ? R1 | R2
    : ReturnType<T>;

// Practical: higher-order function preserving overloads
function withCache<T extends (...args: any) => any>(fn: T): T {
  const cache = new Map();
  return function(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);
    if (!cache.has(key)) cache.set(key, fn(...args));
    return cache.get(key);
  } as T; // assertion needed to preserve overloads
}
```

---

**Q33. What is the `Extract` pattern for discriminated unions?**

```typescript
// Extract specific members from a discriminated union

type ApiEvent =
  | { type: "user.created"; userId: string; name: string }
  | { type: "user.deleted"; userId: string }
  | { type: "order.created"; orderId: string; total: number }
  | { type: "order.shipped"; orderId: string; trackingId: string }
  | { type: "payment.received"; amount: number; currency: string };

// Extract specific event type:
type UserCreated = Extract<ApiEvent, { type: "user.created" }>;
// { type: "user.created"; userId: string; name: string }

// Extract all user events:
type UserEvents = Extract<ApiEvent, { type: `user.${string}` }>;
// { type: "user.created"; ... } | { type: "user.deleted"; ... }

// Extract all order events:
type OrderEvents = Extract<ApiEvent, { type: `order.${string}` }>;

// Type-safe handler map:
type HandlerMap = {
  [E in ApiEvent["type"]]: (
    event: Extract<ApiEvent, { type: E }>
  ) => void;
};

const handlers: HandlerMap = {
  "user.created":     (e) => { e.userId; e.name; },        // typed correctly!
  "user.deleted":     (e) => { e.userId; },
  "order.created":    (e) => { e.orderId; e.total; },
  "order.shipped":    (e) => { e.orderId; e.trackingId; },
  "payment.received": (e) => { e.amount; e.currency; },
};
```

---

**Q34. What is TypeScript's `asserts` in assertion functions?**

```typescript
// Assertion function — throws if condition fails, narrows type if passes

// Basic assertion:
function assert(condition: unknown, msg?: string): asserts condition {
  if (!condition) throw new Error(msg ?? "Assertion failed");
}

function processAge(age: number | null) {
  assert(age !== null, "Age must not be null");
  age; // number — narrowed after assertion
  age.toFixed(); // OK ✅
}

// Type assertion — asserts value is of specific type:
function assertIsString(val: unknown): asserts val is string {
  if (typeof val !== "string") {
    throw new TypeError(`Expected string, got ${typeof val}`);
  }
}

function processInput(val: unknown) {
  assertIsString(val);
  val.toUpperCase(); // OK — narrowed to string
}

// Assertion + generic:
function assertDefined<T>(
  val: T,
  msg?: string
): asserts val is NonNullable<T> {
  if (val == null) throw new Error(msg ?? `Expected defined value, got ${val}`);
}

const user: User | null = getUser();
assertDefined(user, "User not found");
user.name; // User — non-null narrowed ✅

// Works in test setup:
function setup(): asserts this is { db: Database } {
  if (!this.db) throw new Error("DB not initialized");
}
```

---

**Q35. What is the `using` declaration and `Symbol.dispose`?**

```typescript
// Explicit Resource Management — TypeScript 5.2+ / ES2025

// Symbol.dispose — synchronous disposal
class DatabaseConnection {
  #closed = false;

  query(sql: string) {
    if (this.#closed) throw new Error("Connection closed");
    return [];
  }

  [Symbol.dispose]() {
    this.#closed = true;
    console.log("Connection closed");
  }
}

// Automatic cleanup with `using`:
function processData() {
  using conn = new DatabaseConnection();
  // conn is automatically disposed when scope exits
  const data = conn.query("SELECT * FROM users");
  return data;
} // [Symbol.dispose]() called here — even if an error is thrown!

// Symbol.asyncDispose — asynchronous disposal:
class FileStream {
  async [Symbol.asyncDispose]() {
    await this.flush();
    await this.close();
  }
}

async function writeFile() {
  await using stream = new FileStream();
  await stream.write("data");
} // asyncDispose() called automatically

// DisposableStack — collect multiple disposables:
function openResources() {
  using stack = new DisposableStack();
  const conn  = stack.use(new DatabaseConnection());
  stack.defer(() => cleanupTemp());
  return processAll(conn);
  // Disposed in LIFO order on scope exit
}
```

---

## MEDIUM QUESTIONS

---

**Q36. How do you implement a type-safe event emitter?**

```typescript
type EventMap = Record<string, any>;

class TypedEmitter<Events extends EventMap> {
  private listeners = new Map<keyof Events, Set<Function>>();

  on<K extends keyof Events>(
    event: K,
    handler: (payload: Events[K]) => void
  ): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);
    return () => this.off(event, handler);
  }

  once<K extends keyof Events>(
    event: K,
    handler: (payload: Events[K]) => void
  ): void {
    const wrapper = (payload: Events[K]) => {
      handler(payload);
      this.off(event, wrapper);
    };
    this.on(event, wrapper);
  }

  off<K extends keyof Events>(event: K, handler: Function): void {
    this.listeners.get(event)?.delete(handler);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.listeners.get(event)?.forEach(h => h(payload));
  }
}

// Define your event types:
interface AppEvents {
  "user:created": { id: string; name: string; email: string };
  "user:deleted": { id: string };
  "order:placed": { orderId: string; total: number; userId: string };
  "error":        Error;
}

const emitter = new TypedEmitter<AppEvents>();

emitter.on("user:created", (payload) => {
  payload.id;    // string ✅
  payload.name;  // string ✅
  payload.total; // Error! not in user:created ✅
});

emitter.emit("user:created", { id:"1", name:"Alice", email:"a@b.com" }); // ✅
emitter.emit("user:created", { id:"1" }); // Error! missing name & email ✅
emitter.on("unknown", () => {}); // Error! not in AppEvents ✅
```

---

**Q37. How do you create deeply nested readonly types?**

```typescript
// Built-in Readonly<T> is only one level deep:
const shallow: Readonly<{ a: { b: number } }> = { a: { b: 1 } };
shallow.a = {};   // Error ✅
shallow.a.b = 2;  // No error ❌ — not deep!

// Deep Readonly:
type DeepReadonly<T> =
  T extends (...args: any[]) => any  ? T                     : // functions unchanged
  T extends (infer U)[]              ? ReadonlyArray<DeepReadonly<U>> :
  T extends ReadonlyArray<infer U>   ? ReadonlyArray<DeepReadonly<U>> :
  T extends Map<infer K, infer V>    ? ReadonlyMap<DeepReadonly<K>, DeepReadonly<V>> :
  T extends Set<infer U>             ? ReadonlySet<DeepReadonly<U>> :
  T extends object                   ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;

interface AppConfig {
  server: { host: string; port: number; ssl: { cert: string; key: string } };
  database: { url: string; pool: { min: number; max: number } };
  features: string[];
}

type FrozenConfig = DeepReadonly<AppConfig>;

const config: FrozenConfig = {
  server: { host:"localhost", port:3000, ssl: { cert:"", key:"" } },
  database: { url:"postgres://...", pool: { min:1, max:10 } },
  features: ["auth"],
};

config.server.host = "prod";       // Error ✅
config.server.ssl.cert = "x";     // Error ✅ — deeply readonly!
config.database.pool.max = 100;   // Error ✅
config.features.push("logging");  // Error ✅ — ReadonlyArray
```

---

**Q38. How do you implement a type-safe builder pattern?**

```typescript
// Builder that tracks which fields are set at TYPE level

type IsSet<T, K extends keyof T> = K extends keyof T ? true : false;

// Phase-based builder:
class UserBuilder<
  Set extends Partial<Record<keyof User, true>> = {}
> {
  private data: Partial<User> = {};

  setId(id: string): UserBuilder<Set & { id: true }> {
    this.data.id = id;
    return this as any;
  }

  setName(name: string): UserBuilder<Set & { name: true }> {
    this.data.name = name;
    return this as any;
  }

  setEmail(email: string): UserBuilder<Set & { email: true }> {
    this.data.email = email;
    return this as any;
  }

  setRole(role: User["role"]): UserBuilder<Set & { role: true }> {
    this.data.role = role;
    return this as any;
  }

  // build() only available when id, name, email are all set:
  build(
    this: UserBuilder<Set & { id: true; name: true; email: true }>
  ): User {
    return this.data as User;
  }
}

interface User { id: string; name: string; email: string; role?: string }

// Correct usage:
const user = new UserBuilder()
  .setId("1")
  .setName("Alice")
  .setEmail("alice@example.com")
  .build(); // ✅

// Error cases:
new UserBuilder().setId("1").setName("Alice").build(); // Error — email not set ✅
new UserBuilder().build(); // Error — nothing set ✅
```

---

**Q39. What is variance in TypeScript's type system?**

```typescript
// COVARIANCE — if Dog extends Animal, then T<Dog> extends T<Animal>
// Safe for output positions (return types, readonly fields)

class Animal { breathe() {} }
class Dog extends Animal { bark() {} }

// Array is covariant (but unsound!):
const dogs: Dog[] = [new Dog()];
const animals: Animal[] = dogs; // OK — covariant assignment
animals.push(new Animal());     // Runtime bug! dogs[1] is Animal, not Dog

// Functions: CONTRAVARIANT in parameter, COVARIANT in return
type AnimalFn = (a: Animal) => Animal;
type DogFn    = (d: Dog)    => Dog;

// Is DogFn assignable to AnimalFn? NO (parameter is contravariant)
const dogFn: DogFn = (d) => { d.bark(); return d; };
const animalFn: AnimalFn = dogFn; // Error with strictFunctionTypes

// Why? If we call animalFn(new Animal()), dogFn receives Animal but tries to .bark()!

// Is AnimalFn assignable to DogFn? YES (return is covariant)
const makeAnimal: AnimalFn = () => new Dog(); // OK — Dog is-a Animal

// TypeScript 4.7 — explicit variance markers:
type Provider<out T>  = () => T;   // covariant — T only produced
type Consumer<in T>   = (x: T) => void; // contravariant — T only consumed
type Both<in out T>   = { get(): T; set(x: T): void }; // invariant

// out T — TypeScript verifies T only appears in output positions
// in T  — TypeScript verifies T only appears in input positions
```

---

**Q40. How do you implement recursive types?**

```typescript
// Recursive types reference themselves

// JSON type:
type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };

const data: JSONValue = {
  users: [
    { id: 1, name: "Alice", metadata: { nested: { deep: true } } }
  ],
  count: 1,
};

// Recursive tree:
interface TreeNode<T> {
  value: T;
  children: TreeNode<T>[];
}

// Recursive tuple to union:
type TupleToUnion<T extends readonly unknown[]> =
  T extends readonly [infer H, ...infer Rest]
    ? H | TupleToUnion<Rest>
    : never;

type UnionFromTuple = TupleToUnion<[string, number, boolean]>;
// string | number | boolean

// Deep partial (only recurse into objects):
type DeepPartial<T> =
  T extends object
    ? { [K in keyof T]?: DeepPartial<T[K]> }
    : T;

// Deep required:
type DeepRequired<T> =
  T extends object
    ? { [K in keyof T]-?: DeepRequired<T[K]> }
    : T;

// Path type (dot-notation string paths):
type Paths<T, Prefix extends string = ""> =
  T extends object
    ? { [K in string & keyof T]:
          | `${Prefix}${K}`
          | Paths<T[K], `${Prefix}${K}.`>
      }[string & keyof T]
    : never;

interface Config { server: { port: number; host: string }; debug: boolean }
type ConfigPaths = Paths<Config>; // "server" | "server.port" | "server.host" | "debug"
```

---

**Q41. How do you implement a type-safe `pipe` function?**

```typescript
// pipe(value, fn1, fn2, fn3) — each fn's output is next fn's input

// Variadic overloads:
function pipe<A>(value: A): A;
function pipe<A, B>(value: A, fn1: (a: A) => B): B;
function pipe<A, B, C>(value: A, fn1: (a: A) => B, fn2: (b: B) => C): C;
function pipe<A, B, C, D>(
  value: A,
  fn1: (a: A) => B,
  fn2: (b: B) => C,
  fn3: (c: C) => D
): D;
// ... add more overloads as needed

function pipe(value: any, ...fns: Function[]) {
  return fns.reduce((acc, fn) => fn(acc), value);
}

// Usage:
const result = pipe(
  "  hello world  ",
  (s: string) => s.trim(),       // string
  (s: string) => s.split(" "),   // string[]
  (a: string[]) => a.map(s => s.toUpperCase()), // string[]
  (a: string[]) => a.join("-"),  // string
);
// "HELLO-WORLD"

// More advanced: Variadic tuple inference (TS 4.0+)
type PipeReturn<
  Fns extends ReadonlyArray<(arg: any) => any>,
  First
> = Fns extends []
  ? First
  : Fns extends [infer Head extends (arg: any) => any, ...infer Tail extends ReadonlyArray<(arg: any) => any>]
    ? PipeReturn<Tail, ReturnType<Head>>
    : never;
```

---

**Q42. What are TypeScript's `infer` patterns for extracting nested types?**

```typescript
// Extract type from nested structures

// From nested promise:
type UnwrapAll<T> =
  T extends Promise<infer U> ? UnwrapAll<U> :
  T extends Array<infer U>   ? UnwrapAll<U>[] :
  T;

type A = UnwrapAll<Promise<Promise<string>>>; // string
type B = UnwrapAll<Promise<string[]>>;        // string[]

// Extract event handler param type:
type HandlerParam<T> =
  T extends (event: infer E) => any ? E : never;

type ClickParam = HandlerParam<(e: MouseEvent) => void>; // MouseEvent

// From function tuple (first param of each fn):
type FirstParams<T extends ((...args: any) => any)[]> = {
  [K in keyof T]: T[K] extends (first: infer P, ...rest: any) => any ? P : never
};

type Params = FirstParams<
  [(s: string) => void, (n: number) => void, (b: boolean) => void]
>; // [string, number, boolean]

// Extract promise value and error:
type PromiseResult<T extends Promise<any>> =
  T extends Promise<infer Success>
    ? { data: Success; error: null } | { data: null; error: Error }
    : never;

// Constructor argument extractor:
type CtorArgs<T> =
  T extends new (...args: infer A) => any ? A : never;

type MapArgs = CtorArgs<typeof Map>; // [entries?: readonly [unknown, unknown][]]
```

---

**Q43. How do you build a type-safe query builder?**

```typescript
type WhereClause<T> = {
  [K in keyof T]?: T[K] | { eq: T[K] } | { ne: T[K] } |
    (T[K] extends number ? { gt: number; lt?: number } : never);
};

type OrderDirection = "ASC" | "DESC";
type OrderClause<T> = Partial<Record<keyof T & string, OrderDirection>>;

class Query<T extends Record<string, any>> {
  private wheres: WhereClause<T>[] = [];
  private orders: OrderClause<T>[] = [];
  private limitVal?: number;
  private offsetVal?: number;
  private selectedFields?: Array<keyof T>;

  select<K extends keyof T>(...fields: K[]): Query<Pick<T, K>> {
    this.selectedFields = fields;
    return this as any;
  }

  where(clause: WhereClause<T>): this {
    this.wheres.push(clause);
    return this;
  }

  orderBy(clause: OrderClause<T>): this {
    this.orders.push(clause);
    return this;
  }

  limit(n: number): this { this.limitVal = n; return this; }
  offset(n: number): this { this.offsetVal = n; return this; }

  build(): string {
    // Build SQL from accumulated state
    const fields = this.selectedFields?.join(", ") ?? "*";
    const where = this.wheres.map(w => Object.entries(w)
      .map(([k, v]) => `${k} = '${v}'`).join(" AND ")
    ).join(" AND ");
    return `SELECT ${fields}${where ? ` WHERE ${where}` : ""}`;
  }
}

interface User { id: number; name: string; email: string; age: number }

const query = new Query<User>()
  .where({ age: { gt: 18 } })
  .where({ name: "Alice" })
  .orderBy({ name: "ASC" })
  .limit(10)
  .select("id", "name")
  .build();
```

---

**Q44. What is the difference between `typeof` and `keyof` at the type level?**

```typescript
// `typeof` at TYPE level — get the type of a VALUE
const config = {
  port: 3000,
  host: "localhost",
  features: ["auth", "log"] as const,
};

type Config = typeof config;
// { port: number; host: string; features: readonly ["auth", "log"] }

// With function:
function add(a: number, b: number): number { return a + b; }
type AddFn = typeof add; // (a: number, b: number) => number

// With class (gets constructor type):
class User { id: string = ""; }
type UserConstructor = typeof User; // typeof User = constructor
type UserInstance = InstanceType<typeof User>; // User instance type

// `keyof` at TYPE level — get union of keys
type ConfigKeys = keyof Config; // "port" | "host" | "features"
type ConfigKeys2 = keyof typeof config; // same — typeof first, then keyof

// Combining:
function getConfig<K extends keyof typeof config>(key: K): typeof config[K] {
  return config[key];
}

getConfig("port");    // returns number
getConfig("host");    // returns string
getConfig("missing"); // Error! Not a key

// keyof on union:
type A = { x: string; y: number };
type B = { y: number; z: boolean };
type KeysOfBoth = keyof (A & B); // "x" | "y" | "z" — intersection
type KeysOfEither = keyof (A | B); // "y" — only common keys
```

---

**Q45. How do you type React components properly in TypeScript?**

```typescript
import React, { useState, useEffect, useRef, ComponentProps } from "react";

// Functional component with props:
interface ButtonProps {
  label: string;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "danger";
  children?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = "primary",
  children,
}) => (
  <button
    className={`btn btn-${variant}`}
    onClick={onClick}
    disabled={disabled}
  >
    {children ?? label}
  </button>
);

// Extending HTML element props:
interface InputProps extends ComponentProps<"input"> {
  label: string;
  error?: string;
  helperText?: string;
}

const Input: React.FC<InputProps> = ({ label, error, helperText, ...inputProps }) => (
  <div>
    <label>{label}</label>
    <input {...inputProps} />
    {error && <span className="error">{error}</span>}
  </div>
);

// Generic component:
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage = "No items" }: ListProps<T>) {
  if (items.length === 0) return <p>{emptyMessage}</p>;
  return <ul>{items.map((item, i) => <li key={keyExtractor(item)}>{renderItem(item, i)}</li>)}</ul>;
}

// Hooks with generics:
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url)
      .then(r => r.json() as Promise<T>)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

---

**Q46. How do you implement discriminated union exhaustive switch?**

```typescript
// The `never` trick for compile-time exhaustiveness

type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" }
  | { type: "SET"; value: number };

function assertNever(x: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(x)}`);
}

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT": return state + action.amount;
    case "DECREMENT": return state - action.amount;
    case "RESET":     return 0;
    case "SET":       return action.value;
    default:
      // If we add a new action type and forget to handle it,
      // TypeScript errors here (action would be `never`)
      return assertNever(action);
  }
}

// Alternative: object dispatch (also exhaustive with mapped type):
type Handler<A extends Action> = (state: number, action: A) => number;

type Handlers = {
  [K in Action["type"]]: Handler<Extract<Action, { type: K }>>
};

const handlers: Handlers = {
  INCREMENT: (s, a) => s + a.amount,
  DECREMENT: (s, a) => s - a.amount,
  RESET:     (s)    => 0,
  SET:       (s, a) => a.value,
  // If action type added, TypeScript requires adding it here too!
};

function dispatch(state: number, action: Action): number {
  return (handlers[action.type] as Handler<typeof action>)(state, action);
}
```

---

**Q47. What is TypeScript's `NoInfer<T>` utility type?**

```typescript
// NoInfer<T> — prevents TypeScript from using a specific position for inference
// (TypeScript 5.4+)

// Problem: inference from multiple positions can pick the wrong one
function createPair<T>(a: T, b: T): [T, T] { return [a, b]; }

createPair("hello", 42); // Error — T inferred as string | number from both args
// Sometimes we want inference from ONLY the first arg:

function withDefault<T>(value: T, defaultValue: NoInfer<T>): T {
  return value ?? defaultValue;
}

withDefault("hello", 42);    // Error! T = string, 42 not string ✅
withDefault("hello", "world"); // OK ✅
withDefault(true, false);      // OK ✅

// Another use case: React's createContext pattern
function createContext<T>(
  defaultValue: T
): [React.Provider<T>, () => T] {
  const ctx = React.createContext(defaultValue);
  const useCtx = () => React.useContext(ctx);
  return [ctx.Provider, useCtx];
}

// Event system with constrained payload:
function on<T extends EventMap, K extends keyof T>(
  emitter: TypedEmitter<T>,
  event: K,
  handler: (payload: NoInfer<T[K]>) => void  // no inference from handler
): void {
  emitter.on(event, handler);
}
```

---

**Q48. How do you create fully type-safe REST API clients?**

```typescript
// Type-safe API client with inferred response types

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface Endpoint<
  Method extends HttpMethod,
  Path extends string,
  Body,
  Response
> {
  method: Method;
  path: Path;
  body?: Body;
  response: Response;
}

// Define your API contract:
type ApiRoutes = {
  "GET /users":          Endpoint<"GET",    "/users",          never,       User[]>;
  "POST /users":         Endpoint<"POST",   "/users",          CreateUser,  User>;
  "GET /users/:id":      Endpoint<"GET",    "/users/:id",      never,       User>;
  "PATCH /users/:id":    Endpoint<"PATCH",  "/users/:id",      Partial<User>, User>;
  "DELETE /users/:id":   Endpoint<"DELETE", "/users/:id",      never,       void>;
};

type Route = keyof ApiRoutes;
type RouteResponse<R extends Route> = ApiRoutes[R]["response"];
type RouteBody<R extends Route> = ApiRoutes[R]["body"];

class ApiClient {
  constructor(private baseUrl: string) {}

  async request<R extends Route>(
    route: R,
    ...args: RouteBody<R> extends never
      ? [params?: Record<string, string>]
      : [body: RouteBody<R>, params?: Record<string, string>]
  ): Promise<RouteResponse<R>> {
    const [method, path] = (route as string).split(" ");
    const body = typeof args[0] === "object" && !(args[0] instanceof URLSearchParams)
      ? args[0] : undefined;

    const res = await fetch(`${this.baseUrl}${path}`, {
      method,
      body: body ? JSON.stringify(body) : undefined,
      headers: { "Content-Type": "application/json" },
    });
    return res.json();
  }
}

const api = new ApiClient("https://api.example.com");
const users = await api.request("GET /users");     // type: User[] ✅
const user  = await api.request("POST /users", { name: "Alice", email: "a@b.com" }); // User ✅
```

---

**Q49. What is TypeScript's `Awaited` in recursive contexts?**

```typescript
// The built-in Awaited handles recursive Promise unwrapping

type A = Awaited<Promise<string>>;                      // string
type B = Awaited<Promise<Promise<Promise<number>>>>;    // number
type C = Awaited<string | Promise<number>>;            // string | number

// Building Awaited from scratch (educational):
type MyAwaited<T> =
  T extends null | undefined ? T :
  T extends object & { then(onfulfilled: infer F, ...args: any): any }
    ? F extends ((value: infer V, ...args: any) => any)
      ? MyAwaited<V>
      : never
    : T;

// Practical: unwrap nested async function chains
type ChainedResult<Fns extends ((...args: any) => any)[]> =
  Fns extends []
    ? unknown
    : Fns extends [...any[], infer Last extends (...args: any) => any]
      ? Awaited<ReturnType<Last>>
      : never;

// Type-safe async pipeline with correct return types:
async function pipeline<A, B, C>(
  value: A,
  fn1: (a: A) => Promise<B>,
  fn2: (b: B) => Promise<C>,
): Promise<C> {
  return fn2(await fn1(value));
}

const result = await pipeline(
  "user@example.com",
  async (email) => fetchUserByEmail(email),   // Promise<User>
  async (user) => fetchUserPosts(user.id),     // Promise<Post[]>
);
// result: Post[] ✅
```

---

**Q50. How do you type Express middleware in TypeScript?**

```typescript
import express, { Request, Response, NextFunction, RequestHandler } from "express";

// Augment Request with custom fields:
declare global {
  namespace Express {
    interface Request {
      user?: AuthUser;
      requestId: string;
      startTime: number;
    }
  }
}

// Typed middleware:
const authMiddleware: RequestHandler = (req, res, next) => {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) return res.status(401).json({ error: "Unauthorized" });

  try {
    req.user = verifyToken(token); // Request is augmented
    next();
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
};

// Generic error handler:
class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public details?: unknown
  ) { super(message); }
}

const errorHandler: express.ErrorRequestHandler = (err, req, res, next) => {
  if (err instanceof ApiError) {
    return res.status(err.statusCode).json({
      error: err.message,
      details: err.details,
    });
  }
  res.status(500).json({ error: "Internal Server Error" });
};

// Route with typed params/body:
interface UserParams { id: string }
interface UpdateBody { name?: string; email?: string }

app.patch<UserParams, User, UpdateBody>(
  "/users/:id",
  authMiddleware,
  async (req, res, next) => {
    try {
      req.params.id;   // string ✅
      req.body.name;   // string | undefined ✅
      req.user?.id;    // string | undefined ✅
      const user = await updateUser(req.params.id, req.body);
      res.json(user);
    } catch (err) {
      next(err);
    }
  }
);
```

---

**Q51. What is `ConstructorParameters` and how to use it?**

```typescript
// ConstructorParameters<T> — tuple of constructor parameter types

class UserService {
  constructor(
    private db: Database,
    private cache: CacheService,
    private logger: Logger,
    private config: { timeout: number; retries: number }
  ) {}
}

type ServiceArgs = ConstructorParameters<typeof UserService>;
// [db: Database, cache: CacheService, logger: Logger, config: { timeout: number; retries: number }]

// Use to forward constructor args:
function createService<T extends new (...args: any) => any>(
  ServiceClass: T,
  ...args: ConstructorParameters<T>
): InstanceType<T> {
  return new ServiceClass(...args);
}

const service = createService(UserService, db, cache, logger, { timeout: 5000, retries: 3 });
// Fully typed, no `any`!

// Factory with partial args:
function createFactory<T extends new (...args: any) => any>(
  ServiceClass: T,
  defaults: Partial<ConstructorParameters<T>[0]> // partial first arg
) {
  return (...args: ConstructorParameters<T>) => new ServiceClass(...args);
}

// Test helper — create instance with mocked deps:
type Mocked<T> = { [K in keyof T]: jest.Mock };

function createMockedService<T extends new (...args: any) => any>(
  ServiceClass: T,
  mocks: { [K in keyof ConstructorParameters<T>]?: any }
): InstanceType<T> {
  const args = Object.values(mocks) as ConstructorParameters<T>;
  return new ServiceClass(...args);
}
```

---

**Q52. How do you implement type-safe environment variables?**

```typescript
// Validate and type env vars at startup

type EnvSchema = {
  [key: string]: {
    type: "string" | "number" | "boolean" | "url" | "email";
    required?: boolean;
    default?: string;
  };
};

type EnvResult<Schema extends EnvSchema> = {
  [K in keyof Schema]:
    Schema[K]["type"] extends "number"  ? number  :
    Schema[K]["type"] extends "boolean" ? boolean :
    string;
};

function validateEnv<Schema extends EnvSchema>(
  schema: Schema
): EnvResult<Schema> {
  const result: Record<string, unknown> = {};

  for (const [key, config] of Object.entries(schema)) {
    const raw = process.env[key] ?? config.default;

    if (raw === undefined) {
      if (config.required !== false) {
        throw new Error(`Missing required env var: ${key}`);
      }
      continue;
    }

    switch (config.type) {
      case "number": {
        const n = Number(raw);
        if (isNaN(n)) throw new Error(`${key} must be a number`);
        result[key] = n;
        break;
      }
      case "boolean":
        result[key] = raw === "true" || raw === "1";
        break;
      case "url":
        try { new URL(raw); result[key] = raw; }
        catch { throw new Error(`${key} must be a valid URL`); }
        break;
      default:
        result[key] = raw;
    }
  }

  return result as EnvResult<Schema>;
}

const env = validateEnv({
  PORT:         { type: "number", default: "3000" },
  NODE_ENV:     { type: "string", required: false, default: "development" },
  DATABASE_URL: { type: "url" },
  JWT_SECRET:   { type: "string" },
  DEBUG:        { type: "boolean", default: "false" },
} as const);

env.PORT;         // number ✅
env.DATABASE_URL; // string ✅
env.DEBUG;        // boolean ✅
```

---

**Q53. What is module augmentation for third-party libraries?**

```typescript
// Add types that a third-party library is missing

// 1. Augmenting 'express' to add custom request properties:
declare module "express-serve-static-core" {
  interface Request {
    user?:      { id: string; role: "admin" | "user"; permissions: string[] };
    tenantId?:  string;
    requestId:  string;
    logger:     Logger;
  }
}

// 2. Augmenting 'knex' to add table row types:
declare module "knex/types/tables" {
  interface Tables {
    users:  UserRow;
    posts:  PostRow;
    comments: CommentRow;
  }
}

// Now knex gives correct types:
const user = await knex("users").where("id", 1).first();
// user: UserRow | undefined ✅

// 3. Augmenting 'process.env':
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      readonly NODE_ENV: "development" | "test" | "production";
      readonly PORT: string;
      readonly DATABASE_URL: string;
      readonly JWT_SECRET: string;
    }
  }
}
process.env.NODE_ENV; // "development" | "test" | "production" ✅
process.env.RANDOM;   // Error! Not in ProcessEnv ✅

// 4. Augmenting window:
declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION__?: () => any;
    analytics: {
      track(event: string, props?: Record<string, unknown>): void;
      identify(userId: string, traits?: Record<string, unknown>): void;
    };
  }
}
window.analytics.track("Page View"); // ✅
```

---

**Q54. How do you make TypeScript `switch` statements exhaustive?**

```typescript
// Pattern 1: assertNever in default
function assertNever(x: never, msg = `Unhandled: ${JSON.stringify(x)}`): never {
  throw new Error(msg);
}

type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.r ** 2;
    case "square": return shape.s ** 2;
    default: return assertNever(shape); // error if case missed
  }
}

// Pattern 2: Object dispatch (no switch at all):
const areaCalculators: { [K in Shape["kind"]]: (s: Extract<Shape, { kind: K }>) => number } = {
  circle: (s) => Math.PI * s.r ** 2,
  square: (s) => s.s ** 2,
  // TypeScript errors if a case is missing!
};

function area2(shape: Shape): number {
  return (areaCalculators[shape.kind] as (s: typeof shape) => number)(shape);
}

// Pattern 3: Match function utility
function match<T extends { kind: string }, R>(
  value: T,
  handlers: { [K in T["kind"]]: (v: Extract<T, { kind: K }>) => R }
): R {
  return (handlers[value.kind as T["kind"]] as any)(value);
}

const result = match(shape, {
  circle: (s) => `circle r=${s.r}`,
  square: (s) => `square s=${s.s}`,
});
```

---

**Q55. What are TypeScript's `using` and `await using` declarations?**

Already covered in Q35. Extension: common patterns.

```typescript
// Pattern: scope-based resource management

// Database transaction:
class Transaction {
  #committed = false;

  async commit() { this.#committed = true; }

  async [Symbol.asyncDispose]() {
    if (!this.#committed) {
      await this.rollback(); // auto-rollback on error!
    }
  }

  private async rollback() { console.log("Rolling back"); }
}

async function transferFunds(from: string, to: string, amount: number) {
  await using tx = await db.beginTransaction();

  await tx.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", [amount, from]);
  await tx.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", [amount, to]);

  await tx.commit(); // only commits if no error
} // tx.asyncDispose() called — rolls back if commit wasn't called

// HTTP request scope:
class RequestContext {
  private cleanups: (() => void)[] = [];

  register(cleanup: () => void) { this.cleanups.push(cleanup); }

  [Symbol.dispose]() {
    this.cleanups.reverse().forEach(fn => fn());
    console.log("Request context cleaned up");
  }
}

function handleRequest(req: Request) {
  using ctx = new RequestContext();
  ctx.register(() => releaseDbConnection());
  ctx.register(() => flushLogs());
  return processRequest(req, ctx);
} // All cleanups called automatically
```

---

**Q56. How do you handle TypeScript with JSON parsing safely?**

```typescript
// JSON.parse returns `any` — unsafe!

// Pattern 1: Schema validation with Zod
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().max(150),
  role: z.enum(["admin", "user"]),
  createdAt: z.string().datetime().transform(s => new Date(s)),
});

type User = z.infer<typeof UserSchema>; // type derived from schema!

function parseUser(json: string): User {
  const data = JSON.parse(json);        // any
  return UserSchema.parse(data);         // throws ZodError if invalid
}

// Safe parse (returns Result):
function safeParseUser(json: string): { success: true; data: User } | { success: false; error: string } {
  try {
    const result = UserSchema.safeParse(JSON.parse(json));
    if (result.success) return { success: true, data: result.data };
    return { success: false, error: result.error.message };
  } catch (e) {
    return { success: false, error: "Invalid JSON" };
  }
}

// Pattern 2: Manual type guard
function isUser(x: unknown): x is User {
  return (
    typeof x === "object" && x !== null &&
    "id" in x && typeof (x as any).id === "string" &&
    "name" in x && typeof (x as any).name === "string"
  );
}

const raw: unknown = JSON.parse(jsonString);
if (isUser(raw)) {
  raw.name; // User — safe!
}
```

---

**Q57. What is type-level programming with recursive conditional types?**

```typescript
// TypeScript's type system is Turing-complete!

// Fibonacci at type level:
type Fib<N extends number, A extends any[] = [], B extends any[] = [any]> =
  A["length"] extends N ? A["length"] :
  Fib<N, B, [...A, ...B]>;

type Fib10 = Fib<10>; // 55

// Type-level addition:
type Add<A extends number, B extends number> =
  [...BuildTuple<A>, ...BuildTuple<B>]["length"];

type BuildTuple<N extends number, T extends any[] = []> =
  T["length"] extends N ? T : BuildTuple<N, [...T, any]>;

type Sum = Add<3, 4>; // 7

// String type operations:
type Split<S extends string, Sep extends string> =
  S extends `${infer Head}${Sep}${infer Tail}`
    ? [Head, ...Split<Tail, Sep>]
    : [S];

type Parts = Split<"a,b,c,d", ",">; // ["a", "b", "c", "d"]

// Join:
type Join<Parts extends string[], Sep extends string> =
  Parts extends [infer H extends string]
    ? H
    : Parts extends [infer H extends string, ...infer Rest extends string[]]
      ? `${H}${Sep}${Join<Rest, Sep>}`
      : "";

type Joined = Join<["a", "b", "c"], "-">; // "a-b-c"

// Replace all occurrences:
type Replace<
  S extends string,
  From extends string,
  To extends string
> = S extends `${infer L}${From}${infer R}`
  ? `${L}${To}${Replace<R, From, To>}`
  : S;

type Replaced = Replace<"hello world world", "world", "TypeScript">;
// "hello TypeScript TypeScript"
```

---

**Q58. How do you implement conditional required fields?**

```typescript
// Some fields required only when another field has a specific value

// Union approach (cleaner):
type BaseForm = { title: string };
type WithFile = BaseForm & { type: "file"; fileUrl: string; mimeType: string };
type WithLink = BaseForm & { type: "link"; href: string; target?: "_blank" | "_self" };
type WithText = BaseForm & { type: "text"; content: string; maxLength?: number };

type Form = WithFile | WithLink | WithText;

const f1: Form = { type: "file", title: "Doc", fileUrl: "/file.pdf", mimeType: "application/pdf" }; // ✅
const f2: Form = { type: "file", title: "Doc" }; // Error! fileUrl required for type "file" ✅

// Conditional required via generic helper:
type RequiredIf<
  T,
  Condition extends Partial<T>,
  RequiredKeys extends keyof T
> =
  | (T & Condition & Required<Pick<T, RequiredKeys>>)
  | (T & { [K in keyof Condition]?: undefined });

// Fields required only for premium users:
type UserForm = RequiredIf<
  { name: string; email: string; tier: "free" | "premium"; paymentMethod?: string; billingAddress?: string },
  { tier: "premium" },
  "paymentMethod" | "billingAddress"
>;

const free: UserForm    = { name:"Alice", email:"a@b.com", tier:"free" }; // ✅
const premium: UserForm = { name:"Bob", email:"b@b.com", tier:"premium", paymentMethod:"card", billingAddress:"123 Main" }; // ✅
const invalid: UserForm = { name:"Carol", email:"c@b.com", tier:"premium" }; // Error! ✅
```

---

**Q59. What is TypeScript's `Flatten` and `FlatMap` type?**

```typescript
// Built-in Awaited is TypeScript's official "flatten promises"
// For other types, we build our own:

// Flatten array one level:
type Flatten<T> = T extends ReadonlyArray<infer U> ? U : T;
type F1 = Flatten<number[][]>; // number[]  (one level)
type F2 = Flatten<string[]>;   // string

// Deep flatten:
type DeepFlatten<T> =
  T extends ReadonlyArray<infer U>
    ? DeepFlatten<U>
    : T;

type F3 = DeepFlatten<number[][][]>; // number

// FlatMap at type level:
type FlatMap<T extends any[], F extends (x: any) => any[]> =
  T extends [infer H, ...infer R]
    ? [...ReturnType<F extends (x: H) => any[] ? F : never>, ...FlatMap<R, F>]
    : [];

// Flatten union:
type FlatUnion<T> =
  T extends T ? T : never; // identity (for distributive behavior)

// Flatten intersection to object:
type Simplify<T> = { [K in keyof T]: T[K] } & {};
type Merged = Simplify<{ a: string } & { b: number } & { c: boolean }>;
// { a: string; b: number; c: boolean }

// Practical: flatten nested error types
type FlattenErrors<T> =
  T extends Record<string, unknown>
    ? { [K in keyof T]: T[K] extends object ? FlattenErrors<T[K]> : string }
    : string;
```

---

**Q60. What is the full TypeScript compilation pipeline?**

```
TypeScript Compilation Pipeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SCANNING (Lexer)
   Source code → Token stream
   Identifies: keywords, identifiers, operators, literals

2. PARSING
   Token stream → Abstract Syntax Tree (AST)
   AST nodes: SourceFile → Statements → Expressions

3. BINDING
   AST → Symbol Table
   Creates symbols for declarations
   Builds scope chain
   Detects: duplicate identifiers, unreachable code

4. TYPE CHECKING
   Symbol Table → Type information
   Resolves types for every expression
   Validates assignments, function calls, property access
   Reports type errors (tsc errors)
   Does NOT generate any output

5. EMIT
   AST + Types → JavaScript output
   Strips type annotations
   Transforms: decorators, enums, namespaces
   Generates: .js, .d.ts, .js.map, .d.ts.map

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key design decisions:
- Types are ERASED at runtime (no runtime type info by default)
- Type checking happens per PROJECT, not per file
- transpileModule (used by Babel/esbuild) skips binding+checking — only emits
  (This is why "isolatedModules" is needed — ensures safe single-file transform)
- Language Server (tsserver) = incremental compilation for IDE
```

```typescript
// Checking compilation impact:

// This works at compile time:
type IsString<T> = T extends string ? "yes" : "no";
const result: IsString<string> = "yes"; // TS checks this

// But at RUNTIME — all types are gone:
// JavaScript output: const result = "yes"; — no type info!

// To have runtime type info: use class (has instanceof) or discriminants
function isString(val: unknown): val is string {
  return typeof val === "string"; // actual runtime check
}
```

---

## HARD QUESTIONS

---

**Q76. Implement a type-safe ORM query builder with full type inference.**

```typescript
// Mimics Prisma-style API with full type safety

type FieldType = "string" | "number" | "boolean" | "date";

type TypescriptType<F extends FieldType> =
  F extends "string"  ? string  :
  F extends "number"  ? number  :
  F extends "boolean" ? boolean :
  F extends "date"    ? Date    :
  never;

type SchemaDefinition = Record<string, FieldType>;

type Model<Schema extends SchemaDefinition> = {
  [K in keyof Schema]: TypescriptType<Schema[K]>
};

type WhereInput<Schema extends SchemaDefinition> = {
  [K in keyof Schema]?: TypescriptType<Schema[K]> | {
    equals?:  TypescriptType<Schema[K]>;
    not?:     TypescriptType<Schema[K]>;
    in?:      TypescriptType<Schema[K]>[];
    notIn?:   TypescriptType<Schema[K]>[];
    lt?:      Schema[K] extends "number" ? number : never;
    gt?:      Schema[K] extends "number" ? number : never;
    contains?: Schema[K] extends "string" ? string : never;
  };
};

type OrderByInput<Schema extends SchemaDefinition> = {
  [K in keyof Schema]?: "asc" | "desc";
};

class ModelQuery<Schema extends SchemaDefinition, Selected extends keyof Schema = keyof Schema> {
  private wheres: WhereInput<Schema>[] = [];
  private orders: OrderByInput<Schema>[] = [];
  private limitVal?: number;
  private fields?: (keyof Schema)[];

  constructor(private schema: Schema, private tableName: string) {}

  where(condition: WhereInput<Schema>): this {
    this.wheres.push(condition);
    return this;
  }

  orderBy(order: OrderByInput<Schema>): this {
    this.orders.push(order);
    return this;
  }

  limit(n: number): this { this.limitVal = n; return this; }

  select<K extends keyof Schema>(...fields: K[]): ModelQuery<Schema, K> {
    const q = new ModelQuery<Schema, K>(this.schema, this.tableName);
    q.fields = fields;
    return q;
  }

  async findMany(): Promise<Pick<Model<Schema>, Selected>[]> {
    // Execute SQL
    return [] as any;
  }

  async findFirst(): Promise<Pick<Model<Schema>, Selected> | null> {
    return null as any;
  }

  async count(): Promise<number> { return 0; }
}

// Schema definition:
const userSchema = {
  id:        "number",
  name:      "string",
  email:     "string",
  age:       "number",
  active:    "boolean",
  createdAt: "date",
} as const;

const query = new ModelQuery(userSchema, "users");

const users = await query
  .where({ age: { gt: 18 } })
  .where({ active: true })
  .orderBy({ name: "asc" })
  .limit(10)
  .select("id", "name", "email")
  .findMany();

users[0].id;    // number ✅
users[0].name;  // string ✅
users[0].age;   // Error! not selected ✅
```

---

**Q77. Implement a fully type-safe Finite State Machine.**

```typescript
// State machine with compile-time transition validation

type StateMachine<
  States extends string,
  Events extends string,
  Transitions extends Partial<Record<States, Partial<Record<Events, States>>>>
> = {
  current: States;
  send<
    State extends States,
    Event extends keyof Transitions[State] & Events
  >(
    this: { current: State },
    event: Event
  ): StateMachine<States, Events, Transitions> & {
    current: Transitions[State][Event] extends States
      ? Transitions[State][Event]
      : never
  };
};

// Traffic light state machine:
type TrafficState = "red" | "yellow" | "green";
type TrafficEvent = "timer" | "emergency";

type TrafficTransitions = {
  red:    { timer: "green" };
  yellow: { timer: "red" };
  green:  { timer: "yellow"; emergency: "red" };
};

// Simpler practical implementation:
function createMachine<
  State extends string,
  Event extends string
>(config: {
  initial: State;
  transitions: Partial<Record<State, Partial<Record<Event, State>>>>;
  onEnter?: Partial<Record<State, () => void>>;
  onExit?:  Partial<Record<State, () => void>>;
}) {
  let current = config.initial;

  return {
    get state(): State { return current; },

    send(event: Event): boolean {
      const nextState = config.transitions[current]?.[event];
      if (!nextState) {
        console.warn(`No transition from ${current} on ${event}`);
        return false;
      }
      config.onExit?.[current]?.();
      current = nextState;
      config.onEnter?.[current]?.();
      return true;
    },

    can(event: Event): boolean {
      return !!(config.transitions[current]?.[event]);
    },

    matches(state: State): boolean { return current === state; },
  };
}

const traffic = createMachine<TrafficState, TrafficEvent>({
  initial: "red",
  transitions: {
    red:    { timer: "green" },
    yellow: { timer: "red" },
    green:  { timer: "yellow", emergency: "red" },
  },
  onEnter: {
    red: () => console.log("🔴 STOP"),
    yellow: () => console.log("🟡 WAIT"),
    green: () => console.log("🟢 GO"),
  },
});

traffic.send("timer");     // red → green
traffic.send("emergency"); // green → red
traffic.state;             // "red"
traffic.can("timer");      // true
```

---

**Q78. How do you implement phantom types in TypeScript?**

```typescript
// Phantom types — add compile-time safety without runtime overhead
// The type parameter exists only at compile time

// Brand type helper:
type Brand<T, B extends string> = T & { readonly __brand: B };

// Create branded types:
type UserId    = Brand<string, "UserId">;
type OrderId   = Brand<string, "OrderId">;
type ProductId = Brand<string, "ProductId">;
type Email     = Brand<string, "Email">;
type Dollars   = Brand<number, "Dollars">;
type Cents     = Brand<number, "Cents">;

// Smart constructors — the only way to create branded values:
function createUserId(id: string): UserId {
  if (!id.match(/^usr_[a-z0-9]+$/)) throw new Error("Invalid user ID format");
  return id as UserId;
}

function createEmail(email: string): Email {
  if (!email.includes("@")) throw new Error("Invalid email");
  return email as Email;
}

function dollarsToCents(d: Dollars): Cents {
  return Math.round(d * 100) as Cents;
}

// Functions require correct brand — mixing up IDs is a compile-time error:
function fetchUser(id: UserId): Promise<User> { return fetch(`/users/${id}`) as any; }
function fetchOrder(id: OrderId): Promise<Order> { return fetch(`/orders/${id}`) as any; }

const userId  = createUserId("usr_abc123");
const orderId = "ord_xyz789" as OrderId; // manual cast if needed

fetchUser(userId);  // ✅
fetchUser(orderId); // Error! OrderId not assignable to UserId ✅
fetchUser("usr_abc123"); // Error! plain string not UserId ✅

// Phantom state types — track state at compile time
type Validated    = { __state: "validated" };
type Unvalidated  = { __state: "unvalidated" };

type FormData<State> = { data: Record<string, string> } & State;

function validate(form: FormData<Unvalidated>): FormData<Validated> {
  // ... perform validation
  return form as unknown as FormData<Validated>;
}

function submit(form: FormData<Validated>): Promise<void> {
  return Promise.resolve(); // only accepts validated forms!
}

const raw = { data: { name: "Alice" }, __state: "unvalidated" as const };
submit(raw as any);            // only works with cast
const valid = validate(raw as any);
submit(valid);                  // ✅ — passes type check
```

---

**Q79. How do you implement co-recursive types and mutual recursion?**

```typescript
// Mutually recursive types reference each other

// AST example — expression and statement reference each other:
type Expression =
  | { kind: "literal";   value: number | string | boolean }
  | { kind: "variable";  name: string }
  | { kind: "binary";    op: "+" | "-" | "*" | "/"; left: Expression; right: Expression }
  | { kind: "call";      fn: Expression; args: Expression[] }
  | { kind: "block";     statements: Statement[]; result?: Expression }
  | { kind: "if";        condition: Expression; then: Expression; else?: Expression }
  | { kind: "lambda";    params: string[]; body: Expression };

type Statement =
  | { kind: "let";     name: string; value: Expression }
  | { kind: "return";  value: Expression }
  | { kind: "if";      condition: Expression; then: Block; else?: Block }
  | { kind: "while";   condition: Expression; body: Block }
  | { kind: "expr";    expression: Expression };

type Block = Statement[];

// Type-safe AST builder:
const ast: Expression = {
  kind: "block",
  statements: [
    { kind: "let", name: "x", value: { kind: "literal", value: 42 } },
    { kind: "let", name: "y", value: { kind: "literal", value: 10 } },
    {
      kind: "if",
      condition: { kind: "binary", op: ">", left: { kind: "variable", name: "x" }, right: { kind: "variable", name: "y" } } as any,
      then: {
        kind: "expr",
        expression: { kind: "call", fn: { kind: "variable", name: "console.log" }, args: [{ kind: "variable", name: "x" }] }
      },
    }
  ],
  result: { kind: "variable", name: "x" },
};

// Evaluator (mutually recursive):
function evalExpr(expr: Expression, env: Map<string, unknown>): unknown {
  switch (expr.kind) {
    case "literal":  return expr.value;
    case "variable": return env.get(expr.name);
    case "binary": {
      const l = evalExpr(expr.left, env) as number;
      const r = evalExpr(expr.right, env) as number;
      return { "+": l+r, "-": l-r, "*": l*r, "/": l/r }[expr.op];
    }
    case "block": {
      const blockEnv = new Map(env);
      for (const stmt of expr.statements) evalStmt(stmt, blockEnv);
      return expr.result ? evalExpr(expr.result, blockEnv) : undefined;
    }
  }
}

function evalStmt(stmt: Statement, env: Map<string, unknown>): void {
  switch (stmt.kind) {
    case "let": env.set(stmt.name, evalExpr(stmt.value, env)); break;
    case "expr": evalExpr(stmt.expression, env); break;
  }
}
```

---

**Q80. What is type-level string parsing in TypeScript?**

```typescript
// Parse URL template into parameter names:
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractRouteParams<`/${Rest}`>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type Params = ExtractRouteParams<"/users/:userId/posts/:postId/comments/:commentId">;
// { userId: string; postId: string; commentId: string }

// Type-safe router:
function createRoute<T extends string>(
  pattern: T,
  handler: (params: ExtractRouteParams<T>, req: Request) => Response
) {
  return { pattern, handler };
}

const route = createRoute(
  "/users/:userId/posts/:postId",
  (params, req) => {
    params.userId;  // string ✅
    params.postId;  // string ✅
    params.missing; // Error! ✅
    return new Response();
  }
);

// Parse CSS class names:
type ParseClasses<T extends string> =
  T extends `${infer Head} ${infer Tail}`
    ? Head | ParseClasses<Tail>
    : T;

type Classes = ParseClasses<"flex items-center justify-between gap-4">;
// "flex" | "items-center" | "justify-between" | "gap-4"

// Parse format strings:
type ParseFormat<T extends string> =
  T extends `${string}%{${infer Param}}${infer Rest}`
    ? { [K in Param | keyof ParseFormat<Rest>]: unknown }
    : {};

type FormatParams = ParseFormat<"Hello %{name}, you have %{count} messages">;
// { name: unknown; count: unknown }
```

---

**Q81–Q120: Advanced Pattern questions**

**Q81. What are higher-kinded types and how TypeScript approximates them?**

```typescript
// True HKTs (Haskell): type constructors as type parameters
// TypeScript lacks true HKTs — but we approximate via defunctionalization

// The problem — you can't express "any container" generically:
// interface Functor<F<_>> { map<A, B>(fa: F<A>, f: (a: A) => B): F<B>; }
// F<A> is not valid TypeScript syntax

// APPROXIMATION using URI strings:

// 1. Register type constructors:
interface URItoKind<A> {
  Array:  A[];
  Option: Option<A>;
  Task:   Task<A>;
}

type URIS = keyof URItoKind<any>;
type Kind<F extends URIS, A> = URItoKind<A>[F];

// 2. Define Functor with URI:
interface Functor<F extends URIS> {
  map<A, B>(fa: Kind<F, A>, f: (a: A) => B): Kind<F, B>;
}

// 3. Implement for Array:
const arrayFunctor: Functor<"Array"> = {
  map: (fa, f) => fa.map(f),
};

// 4. Generic function over any Functor:
function lift<F extends URIS>(
  F: Functor<F>
) {
  return function<A, B>(f: (a: A) => B) {
    return (fa: Kind<F, A>): Kind<F, B> => F.map(fa, f);
  };
}

const double = (n: number) => n * 2;
const liftedDouble = lift(arrayFunctor)(double);
liftedDouble([1, 2, 3]); // [2, 4, 6] — fully typed!

// This is how fp-ts works internally
```

---

**Q82. Implement a type-safe dependency injection container.**

```typescript
// Container that tracks registered types and validates dependencies at compile time

type Token<T> = { readonly __type: T };

function token<T>(name: string): Token<T> {
  return { __type: undefined as any };
}

// Tokens:
const DB_TOKEN     = token<Database>("Database");
const CACHE_TOKEN  = token<Cache>("Cache");
const LOGGER_TOKEN = token<Logger>("Logger");

class Container {
  private registry = new Map<Token<any>, any>();

  register<T>(token: Token<T>, value: T): void {
    this.registry.set(token, value);
  }

  registerFactory<T>(token: Token<T>, factory: (c: Container) => T): void {
    this.registry.set(token, factory(this));
  }

  resolve<T>(token: Token<T>): T {
    if (!this.registry.has(token)) {
      throw new Error(`No registration for token: ${JSON.stringify(token)}`);
    }
    return this.registry.get(token) as T;
  }
}

// Usage:
const container = new Container();
container.register(DB_TOKEN, new Database());
container.register(CACHE_TOKEN, new Cache());
container.registerFactory(LOGGER_TOKEN, c => new Logger(c.resolve(DB_TOKEN)));

const db     = container.resolve(DB_TOKEN);     // Database ✅
const cache  = container.resolve(CACHE_TOKEN);   // Cache ✅
const logger = container.resolve(LOGGER_TOKEN);  // Logger ✅

// Typed factory injection:
function inject<Tokens extends Token<any>[]>(
  tokens: [...Tokens],
  factory: (...deps: { [K in keyof Tokens]: Tokens[K] extends Token<infer T> ? T : never }) => any
) {
  return { tokens, factory };
}
```

---

**Q83. What are TypeScript's compiler API use cases?**

```typescript
// TypeScript exposes its compiler API via the `typescript` package

import * as ts from "typescript";

// 1. Parse source file into AST:
const source = `
  const greeting: string = "Hello, World!";
  function add(a: number, b: number): number { return a + b; }
`;

const sourceFile = ts.createSourceFile(
  "example.ts",
  source,
  ts.ScriptTarget.Latest,
  true // setParentNodes
);

// 2. Walk the AST:
function visit(node: ts.Node) {
  if (ts.isFunctionDeclaration(node)) {
    const name = node.name?.text;
    const params = node.parameters.map(p => ({
      name: (p.name as ts.Identifier).text,
      type: p.type?.getText(sourceFile),
    }));
    console.log(`Function: ${name}`, params);
  }
  ts.forEachChild(node, visit);
}
visit(sourceFile);

// 3. Type checking:
const program = ts.createProgram(["example.ts"], {
  strict: true,
  noEmit: true,
});

const checker = program.getTypeChecker();
const diagnostics = ts.getPreEmitDiagnostics(program);
diagnostics.forEach(d => console.error(ts.formatDiagnostic(d, ts.createCompilerHost({}))));

// 4. Code transformation (custom transform):
function addLogTransformer(ctx: ts.TransformationContext): ts.Transformer<ts.SourceFile> {
  return (source) => {
    function visitor(node: ts.Node): ts.Node {
      if (ts.isFunctionDeclaration(node) && node.name) {
        // Add console.log at the start of every function
        const logStmt = ctx.factory.createExpressionStatement(
          ctx.factory.createCallExpression(
            ctx.factory.createPropertyAccessExpression(
              ctx.factory.createIdentifier("console"),
              "log"
            ),
            undefined,
            [ctx.factory.createStringLiteral(`Calling ${node.name.text}`)]
          )
        );
        // ... add to function body
      }
      return ts.visitEachChild(node, visitor, ctx);
    }
    return ts.visitNode(source, visitor) as ts.SourceFile;
  };
}

// Use cases for compiler API:
// - Custom linting rules (eslint typescript plugin)
// - Code generation (generate types from GraphQL schema)
// - Codemod scripts (automated refactoring)
// - Documentation generation
// - API compatibility checking
```

---

**Q84. What are TypeScript's `satisfies` operator advanced patterns?**

```typescript
// satisfies validates type without losing literal types or causing widening

// Pattern 1: Validate config object
type LogLevel = "debug" | "info" | "warn" | "error";
type AppConfig = {
  logLevel: LogLevel;
  port: number;
  database: { url: string; pool: number };
};

const config = {
  logLevel: "info",  // validated as LogLevel, but type is "info" not LogLevel
  port: 3000,        // type is 3000 not number
  database: { url: "postgres://...", pool: 5 },
} satisfies AppConfig;

config.logLevel.toUpperCase(); // OK — TypeScript knows it's string
config.port.toFixed();         // OK — TypeScript knows it's number

// Pattern 2: Exhaustive record with literal value types
type Color = "red" | "green" | "blue";
const hexCodes = {
  red:   "#ff0000",
  green: "#00ff00",
  blue:  "#0000ff",
} satisfies Record<Color, string>;

hexCodes.red.startsWith("#"); // OK — TypeScript knows it's string
// hexCodes.purple; — Error! not in Color ✅

// Pattern 3: Component props validation
type ButtonVariant = "primary" | "secondary" | "danger";
const buttonStyles = {
  primary:   { bg: "blue-500",   text: "white" },
  secondary: { bg: "gray-200",   text: "gray-800" },
  danger:    { bg: "red-500",    text: "white" },
} satisfies Record<ButtonVariant, { bg: string; text: string }>;

// Each value keeps its specific shape:
buttonStyles.primary.bg; // "blue-500" (literal) not string

// Pattern 4: Type-safe factory methods
class Logger {
  static levels = {
    debug: 0,
    info:  1,
    warn:  2,
    error: 3,
  } satisfies Record<LogLevel, number>;
}

Logger.levels.debug; // 0 (literal), not number
```

---

**Q85. What is TypeScript's type widening and narrowing in depth?**

```typescript
// WIDENING — TypeScript widens literal types to their base types in certain contexts

// Variables without annotation are widened:
let x = "hello"; // type: string (widened from "hello")
const y = "hello"; // type: "hello" (literal — const can't change)

// Arrays widen element types:
const arr = ["a", "b", "c"]; // string[] (widened)
const tuple = ["a", "b", "c"] as const; // readonly ["a", "b", "c"]

// Object values widen:
const obj = { kind: "circle", radius: 5 }; // { kind: string; radius: number }
const frozenObj = { kind: "circle", radius: 5 } as const; // literal types!

// FRESHNESS — object literal type checking is stricter initially:
function f(p: { a: number }) {}
f({ a: 1, b: 2 }); // Error! excess property check on fresh object
const o = { a: 1, b: 2 };
f(o); // OK — widened through variable

// NARROWING flows:
// TypeScript tracks narrowing through control flow, not just conditionals

function example(val: string | number | null) {
  if (val === null) return; // null excluded after this

  // val: string | number here

  if (typeof val === "string") {
    val; // string
    return; // early return
  }
  // TypeScript knows: if we reach here, val is NOT string AND NOT null
  val; // number ✅ — correctly narrowed!
}

// Narrowing through assignment:
let value: string | number = "hello";
value; // string | number — not yet narrowed

value = 42;
value; // number — narrowed by assignment!

value = Math.random() > 0.5 ? "hi" : 10;
value; // string | number — widened back by union assignment
```

---

**Q86. What are TypeScript's recursive mapped types?**

```typescript
// Mapped types can reference themselves for deep transformations

// Deep Partial:
type DeepPartial<T> =
  T extends Function ? T :
  T extends object   ? { [K in keyof T]?: DeepPartial<T[K]> } :
  T;

// Deep Required:
type DeepRequired<T> =
  T extends Function ? T :
  T extends object   ? { [K in keyof T]-?: DeepRequired<T[K]> } :
  T;

// Deep Readonly:
type DeepReadonly<T> =
  T extends Function ? T :
  T extends object   ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;

// Deep Mutable (remove all readonly):
type DeepMutable<T> =
  T extends Function ? T :
  T extends object   ? { -readonly [K in keyof T]: DeepMutable<T[K]> } :
  T;

// Deep NonNullable:
type DeepNonNullable<T> =
  T extends null | undefined ? never :
  T extends object ? { [K in keyof T]: DeepNonNullable<T[K]> } :
  T;

// Deep Replace — replace all values of type A with type B:
type DeepReplace<T, From, To> =
  T extends From ? To :
  T extends object ? { [K in keyof T]: DeepReplace<T[K], From, To> } :
  T;

// Replace all Date with string (for JSON serialization):
type Serialized<T> = DeepReplace<T, Date, string>;

interface User { name: string; createdAt: Date; address: { city: string; since: Date } }
type SerializedUser = Serialized<User>;
// { name: string; createdAt: string; address: { city: string; since: string } }
```

---

**Q87. How do you implement type-safe database query types with joins?**

```typescript
// Type-level SQL JOIN type inference

type Tables = {
  users:  { id: number; name: string; email: string; departmentId: number };
  departments: { id: number; name: string; budget: number };
  posts:  { id: number; title: string; userId: number; publishedAt: Date };
};

type TableName = keyof Tables;
type Row<T extends TableName> = Tables[T];

// Aliased table:
type AliasedRow<T extends TableName, Alias extends string> = {
  [K in keyof Row<T> as `${Alias}.${string & K}`]: Row<T>[K]
};

// JOIN two tables:
type Join<
  Left extends TableName,
  LeftAlias extends string,
  Right extends TableName,
  RightAlias extends string,
> = AliasedRow<Left, LeftAlias> & AliasedRow<Right, RightAlias>;

// SELECT specific columns:
type Select<
  T extends Record<string, unknown>,
  Keys extends keyof T
> = Pick<T, Keys>;

// Example: users JOIN departments
type UserWithDept = Join<"users", "u", "departments", "d">;
// { "u.id": number; "u.name": string; ... "d.id": number; "d.name": string; ... }

type UserDeptResult = Select<UserWithDept, "u.name" | "u.email" | "d.name">;
// { "u.name": string; "u.email": string; "d.name": string }

// Full type-safe query:
function query<
  T extends TableName,
  J extends TableName,
  Selected extends keyof Join<T, "t1", J, "t2">
>(params: {
  from: T;
  join: { table: J; on: string };
  select: Selected[];
}): Promise<Pick<Join<T, "t1", J, "t2">, Selected>[]> {
  return Promise.resolve([]) as any;
}
```

---

**Q88. What are TypeScript error messages and how to write better generic constraints for clearer errors?**

```typescript
// Poor error messages come from overly generic constraints

// BAD — unhelpful error message:
function process<T>(value: T): T { return value; }
process(42 as never); // Error message is confusing

// BETTER — specific constraint with helpful message:

// Custom error type using conditional types:
type TypeError<Msg extends string> = { __error: Msg };

type ValidInput<T> =
  T extends string | number ? T :
  TypeError<"Input must be string or number">;

// The error isn't shown in the type itself, but:
function processTyped<T>(
  value: T & (T extends string | number ? unknown : TypeError<"Must be string or number">)
): T { return value; }

// Better pattern using branded errors:
type AssertExtends<T, Expected, ErrorMsg extends string = `${string} expected`> =
  [T] extends [Expected] ? T : never & { __error: ErrorMsg };

// Template literal error messages:
function createArray<T, N extends number>(
  fill: T,
  length: AssertExtends<N, number, `Length must be a numeric literal, got ${string & N}`>
): T[] {
  return Array(Number(length)).fill(fill);
}

// Improving error messages with overloads + descriptive types:
function divide(numerator: number, denominator: number): number;
function divide(numerator: number, denominator: 0): never; // clear: division by 0 = never
function divide(numerator: number, denominator: number): number {
  if (denominator === 0) throw new Error("Division by zero");
  return numerator / denominator;
}

const result = divide(10, 0); // Type: never — clear indicator something is wrong
```

---

**Q89. Implement a type-safe middleware pipeline.**

```typescript
// Express-like middleware but fully typed

type Next = (error?: Error) => void;
type Handler<Ctx> = (ctx: Ctx, next: Next) => void | Promise<void>;

// Middleware that augments context:
type Middleware<InCtx, OutCtx extends InCtx = InCtx> = (
  ctx: InCtx,
  next: (ctx: OutCtx) => Promise<void>
) => Promise<void>;

class Pipeline<Ctx extends Record<string, unknown>> {
  private handlers: Handler<Ctx>[] = [];

  use<ExtCtx extends Ctx>(
    middleware: Middleware<Ctx, ExtCtx>
  ): Pipeline<ExtCtx> {
    this.handlers.push(middleware as any);
    return this as unknown as Pipeline<ExtCtx>;
  }

  async run(initialCtx: Ctx): Promise<Ctx> {
    let ctx = initialCtx;

    const runMiddleware = async (index: number): Promise<void> => {
      if (index >= this.handlers.length) return;
      const handler = this.handlers[index];
      await new Promise<void>((resolve, reject) => {
        const next = async (nextCtx?: Ctx) => {
          if (nextCtx) ctx = nextCtx;
          try { await runMiddleware(index + 1); resolve(); }
          catch (e) { reject(e); }
        };
        Promise.resolve(handler(ctx, next as any)).catch(reject);
      });
    };

    await runMiddleware(0);
    return ctx;
  }
}

// Usage with growing context:
type BaseCtx   = { requestId: string };
type AuthCtx   = BaseCtx   & { user: { id: string; role: string } };
type LoggedCtx = AuthCtx   & { startTime: number };

const pipeline = new Pipeline<BaseCtx>()
  .use<LoggedCtx>(async (ctx, next) => {
    await next({ ...ctx, startTime: Date.now() });
  })
  .use<AuthCtx & LoggedCtx>(async (ctx, next) => {
    await next({ ...ctx, user: { id: "1", role: "admin" } });
  });

// Each middleware receives the enriched context type
```

---

**Q90. What are TypeScript's upcoming features in TypeScript 5.x?**

```typescript
// TypeScript 5.0:
// - const type parameters — preserve literal types in generics
function identity<const T>(value: T): T { return value; }
const x = identity(["a", "b", "c"]); // type: readonly ["a", "b", "c"] not string[]

// - Multiple config file extends
// tsconfig.json:
// { "extends": ["./base.json", "./strict.json", "./paths.json"] }

// TypeScript 5.1:
// - Unrelated types for setters and getters
class Foo {
  #value = 0;
  get value(): number { return this.#value; }
  set value(v: number | string) {
    this.#value = typeof v === "string" ? parseInt(v) : v;
    // Getter and setter can have different (but related) types now
  }
}

// TypeScript 5.2:
// - using declarations (already covered in Q35)
// - Explicit Resource Management

// TypeScript 5.3:
// - import attributes: import data from "./data.json" with { type: "json" };
// - switch(true) narrowing improvements

// TypeScript 5.4:
// - NoInfer<T> utility type (already covered)
// - Preserved narrowing through closures (in some cases)

// TypeScript 5.5:
// - Inferred type predicates
function isString(x: string | number): boolean {
  return typeof x === "string"; // TypeScript now INFERS: x is string!
}
// No need to write: x is string return type annotation

// - Array filtering infers type:
const arr = [1, "hello", 2, "world", null];
const strings = arr.filter(x => typeof x === "string"); // string[] inferred!

// TypeScript 5.6+:
// - Iterator methods (.map, .filter on iterators)
// - Strict built-in iterator types
```

---

**Q91–Q120 are topic questions — answering key ones:**

**Q91. What is the difference between `infer` in covariant vs contravariant position?**

```typescript
// Position determines how infer collects types in unions

// COVARIANT position (output/return) — multiple infers → UNION
type Covariant<T> =
  T extends { a: infer U; b: infer U } ? U : never;

type A = Covariant<{ a: string; b: number }>;
// string | number — covariant: union

// CONTRAVARIANT position (input/parameter) — multiple infers → INTERSECTION
type Contravariant<T> =
  T extends { a: (x: infer U) => void; b: (x: infer U) => void } ? U : never;

type B = Contravariant<{ a: (x: string) => void; b: (x: number) => void }>;
// string & number = never — contravariant: intersection

// Why intersection for contravariant?
// If both a and b accept U, then U must satisfy BOTH — hence intersection
// If a accepts string and b accepts number, no U works → never

// Practical: union of parameter types
type UnionParams<T extends (...args: any) => any> =
  T extends (arg: infer U) => any ? U : never;

type HandlerUnion = UnionParams<
  ((s: string) => void) | ((n: number) => void)
>;
// string | number — because distributive over union
```

---

**Q92. How do you implement a type-safe `curry` function?**

```typescript
// Fully typed curry — one argument at a time

type Curry<F extends (...args: any) => any> =
  Parameters<F> extends [infer Head, ...infer Tail]
    ? Tail extends []
      ? F
      : (arg: Head) => Curry<(...args: Tail) => ReturnType<F>>
    : ReturnType<F>;

function curry<F extends (...args: any[]) => any>(fn: F): Curry<F> {
  const curried = (...args: any[]) => {
    if (args.length >= fn.length) return fn(...args);
    return (...more: any[]) => curried(...args, ...more);
  };
  return curried as Curry<F>;
}

const add = curry((a: number, b: number, c: number) => a + b + c);
const add1   = add(1);       // (arg: number) => (arg: number) => number
const add1_2 = add(1)(2);    // (arg: number) => number
const result = add(1)(2)(3); // number = 6

// Type-safe partial application:
type PartialApply<F extends (...args: any) => any, Applied extends any[]> =
  Parameters<F> extends [...Applied, ...infer Rest]
    ? Rest extends []
      ? ReturnType<F>
      : (...args: Rest) => ReturnType<F>
    : never;

function partial<F extends (...args: any) => any, Args extends Partial<Parameters<F>>>(
  fn: F,
  ...args: Args
): PartialApply<F, Args> {
  return ((...rest: any[]) => fn(...args, ...rest)) as any;
}

function greet(greeting: string, name: string, punctuation: string): string {
  return `${greeting}, ${name}${punctuation}`;
}

const sayHello = partial(greet, "Hello");
sayHello("Alice", "!"); // "Hello, Alice!" ✅
sayHello(42); // Error! 42 not string ✅
```

---

*This file contains 92+ TypeScript interview questions with complete code answers. Q1–Q35 Easy, Q36–Q75 Medium, Q76–Q120 Hard. Covers type system fundamentals through advanced type-level programming, compiler internals, and production patterns.*

---

## COMPLETING HARD QUESTIONS (Q93–Q120)

---

**Q93. How do you implement a type-safe `Result` monad in TypeScript?**

```typescript
// Result<T, E> — represents success or failure without exceptions

type Ok<T>  = { readonly _tag: "Ok";  readonly value: T };
type Err<E> = { readonly _tag: "Err"; readonly error: E };
type Result<T, E = Error> = Ok<T> | Err<E>;

// Constructors:
const ok  = <T>(value: T): Ok<T>   => ({ _tag: "Ok",  value });
const err = <E>(error: E): Err<E>  => ({ _tag: "Err", error });

// Type guards:
const isOk  = <T, E>(r: Result<T, E>): r is Ok<T>  => r._tag === "Ok";
const isErr = <T, E>(r: Result<T, E>): r is Err<E> => r._tag === "Err";

// Combinators:
function map<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
  return isOk(result) ? ok(fn(result.value)) : result;
}

function flatMap<T, U, E>(result: Result<T, E>, fn: (value: T) => Result<U, E>): Result<U, E> {
  return isOk(result) ? fn(result.value) : result;
}

function mapErr<T, E, F>(result: Result<T, E>, fn: (error: E) => F): Result<T, F> {
  return isErr(result) ? err(fn(result.error)) : result;
}

function getOrElse<T, E>(result: Result<T, E>, defaultValue: T): T {
  return isOk(result) ? result.value : defaultValue;
}

// Try/catch wrapper:
function tryCatch<T>(fn: () => T): Result<T, Error> {
  try { return ok(fn()); }
  catch (e) { return err(e instanceof Error ? e : new Error(String(e))); }
}

async function tryCatchAsync<T>(fn: () => Promise<T>): Promise<Result<T, Error>> {
  try { return ok(await fn()); }
  catch (e) { return err(e instanceof Error ? e : new Error(String(e))); }
}

// Usage:
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return err("Division by zero");
  return ok(a / b);
}

const result = divide(10, 2);
if (isOk(result)) console.log(result.value); // 5

// Chain operations:
const chained = flatMap(
  flatMap(divide(10, 2), n => divide(n, 2)),
  n => ok(n.toFixed(2))
);
// Ok("2.50")
```

---

**Q94. How do you implement `DeepPick` and `DeepOmit` in TypeScript?**

```typescript
// Deep path picking/omitting — select/exclude nested properties

type Path<T, Key extends keyof T = keyof T> =
  Key extends string
    ? T[Key] extends Record<string, any>
      ? | `${Key}.${Path<T[Key]>}`
        | Key
      : Key
    : never;

// DeepPick — pick by dotted path
type DeepPickByPath<T, P extends string> =
  P extends `${infer Key}.${infer Rest}`
    ? Key extends keyof T
      ? { [K in Key]: DeepPickByPath<T[K], Rest> }
      : never
    : P extends keyof T
      ? { [K in P]: T[K] }
      : never;

// Simpler deep required/partial (different approach):
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type DeepRequired<T> = {
  [K in keyof T]-?: T[K] extends object ? DeepRequired<T[K]> : T[K];
};

// Deep path type:
interface Config {
  server: { host: string; port: number; tls: { cert: string; key: string } };
  db: { url: string; pool: { min: number; max: number } };
}

type ConfigPaths = Path<Config>;
// "server" | "db" | "server.host" | "server.port" | "server.tls" | 
// "server.tls.cert" | "server.tls.key" | "db.url" | "db.pool" |
// "db.pool.min" | "db.pool.max"

// Type-safe deep get:
type DeepGet<T, P extends string> =
  P extends `${infer Key}.${infer Rest}`
    ? Key extends keyof T ? DeepGet<T[Key], Rest> : never
    : P extends keyof T ? T[P] : never;

type HostType = DeepGet<Config, "server.host">; // string
type PoolMax  = DeepGet<Config, "db.pool.max">; // number
```

---

**Q95. What is type-level arithmetic in TypeScript?**

```typescript
// TypeScript tuple length enables compile-time arithmetic

// Build array of length N:
type BuildTuple<N extends number, T extends any[] = []> =
  T["length"] extends N ? T : BuildTuple<N, [...T, unknown]>;

// Addition using tuple concatenation:
type Add<A extends number, B extends number> =
  [...BuildTuple<A>, ...BuildTuple<B>]["length"];

type Sum = Add<3, 4>; // 7

// Subtraction:
type Subtract<A extends number, B extends number> =
  BuildTuple<A> extends [...BuildTuple<B>, ...infer Rest]
    ? Rest["length"]
    : never;

type Diff = Subtract<10, 3>; // 7

// Less than:
type LessThan<A extends number, B extends number> =
  BuildTuple<A> extends [...(infer _), ...BuildTuple<B>]
    ? false
    : BuildTuple<B> extends [...(infer _), ...BuildTuple<A>]
      ? true
      : false;

type IsSmall = LessThan<3, 5>; // true
type IsLarge = LessThan<5, 3>; // false

// Range check:
type InRange<N extends number, Min extends number, Max extends number> =
  LessThan<N, Min> extends true ? false :
  LessThan<Max, N> extends true ? false : true;

type Valid = InRange<5, 1, 10>; // true
type TooLow = InRange<0, 1, 10>; // false

// Limits: TypeScript has recursion depth limit (~1000)
// Only works for small numbers
```

---

**Q96. How do you implement `Awaited` and `UnwrapPromise` from scratch?**

```typescript
// Built-in Awaited<T> implementation (educational):
type MyAwaited<T> =
  T extends null | undefined
    ? T
    : T extends object & { then(onfulfilled: infer F, ...args: any[]): any }
      ? F extends (value: infer V, ...args: any[]) => any
        ? MyAwaited<V>   // recursive — handles Promise<Promise<T>>
        : never
      : T;

// Examples:
type A = MyAwaited<Promise<string>>;             // string
type B = MyAwaited<Promise<Promise<number>>>;    // number
type C = MyAwaited<string>;                      // string (not a promise)
type D = MyAwaited<Promise<{ id: number }>>;     // { id: number }

// Awaited for union:
type E = MyAwaited<string | Promise<number>>;    // string | number

// Deep unwrap for nested async:
type UnwrapNested<T> = T extends Promise<infer U>
  ? UnwrapNested<U>   // keep unwrapping
  : T;

type F = UnwrapNested<Promise<Promise<Promise<string>>>>; // string

// Practical — get the value type of any async function:
async function fetchUsers(): Promise<User[]> { return []; }
async function processUser(u: User): Promise<{ ok: boolean }> { return { ok: true }; }

type FetchResult  = Awaited<ReturnType<typeof fetchUsers>>;  // User[]
type ProcessResult = Awaited<ReturnType<typeof processUser>>; // { ok: boolean }

// Type-safe Promise.all return:
type AwaitAll<T extends readonly Promise<any>[]> = {
  [K in keyof T]: Awaited<T[K]>
};
```

---

**Q97. What is the `Opaque` / branded type pattern?**

```typescript
// Opaque types: same runtime type, different compile-time identity
// Prevents accidentally using wrong value where another is expected

declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { readonly [__brand]: B };

// Branded primitives:
type UserId    = Brand<string, "UserId">;
type OrderId   = Brand<string, "OrderId">;
type Email     = Brand<string, "Email">;
type Dollars   = Brand<number, "Dollars">;
type Cents     = Brand<number, "Cents">;
type SafeHTML  = Brand<string, "SafeHTML">;

// Smart constructors — only way to create branded values:
function toUserId(raw: string): UserId {
  if (!/^usr_[a-z0-9]{8,}$/.test(raw)) throw new Error(`Invalid UserId: ${raw}`);
  return raw as UserId;
}

function toEmail(raw: string): Email {
  if (!raw.includes("@")) throw new Error(`Invalid email: ${raw}`);
  return raw.toLowerCase() as Email;
}

function sanitizeHTML(html: string): SafeHTML {
  return DOMPurify.sanitize(html) as SafeHTML;
}

// Functions require correct brand:
function sendEmail(to: Email, body: SafeHTML): void {}
function getUser(id: UserId): Promise<User> { return Promise.resolve({} as User); }

const userId = toUserId("usr_abc123");
const email  = toEmail("user@example.com");
const html   = sanitizeHTML("<b>Hello</b>");

sendEmail(email, html); // ✅
sendEmail("raw@string.com", html); // ❌ Error: string not assignable to Email
getUser(userId); // ✅
getUser("raw-string"); // ❌ Error: string not assignable to UserId
getUser("ord_123" as OrderId); // ❌ Error: OrderId not assignable to UserId
```

---

**Q98. How do you use TypeScript with Express for full type safety?**

```typescript
import express, { Request, Response, NextFunction, RequestHandler } from "express";
import { z, ZodSchema } from "zod";

// Typed route parameters:
interface TypedRequest<
  Body = undefined,
  Params extends Record<string, string> = {},
  Query extends Record<string, string | string[]> = {}
> extends Request {
  body: Body;
  params: Params;
  query: Query;
}

// Validation middleware factory:
function validate<T>(schema: ZodSchema<T>): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.flatten() });
    }
    req.body = result.data; // replace with validated+transformed data
    next();
  };
}

// DTO schemas:
const CreateUserSchema = z.object({
  name:  z.string().min(2).max(100),
  email: z.string().email().transform(s => s.toLowerCase()),
  role:  z.enum(["admin", "user", "editor"]).default("user"),
});

type CreateUserDto = z.infer<typeof CreateUserSchema>;

// Typed controllers:
const createUser: RequestHandler = async (
  req: TypedRequest<CreateUserDto, {}, {}>,
  res: Response<{ id: string; name: string } | { error: string }>
) => {
  const user = await userService.create(req.body); // body is typed!
  res.status(201).json({ id: user.id, name: user.name });
};

// Router:
const router = express.Router();
router.post("/users", validate(CreateUserSchema), createUser);

// Typed error handler:
const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction // MUST have 4 params for Express to recognize error handler
): void => {
  res.status(500).json({ error: err.message });
};
```

---

**Q99. What is `Exclude` and `Extract` with complex union types?**

```typescript
// Advanced union manipulation

type ApiResponse =
  | { type: "success"; data: User;    statusCode: 200 }
  | { type: "created"; data: User;    statusCode: 201; location: string }
  | { type: "error";   message: string; statusCode: 400 | 401 | 403 | 404 | 500 }
  | { type: "empty";   statusCode: 204 };

// Extract by discriminant:
type SuccessResponses = Extract<ApiResponse, { type: "success" | "created" | "empty" }>;
// { type: "success"... } | { type: "created"... } | { type: "empty"... }

// Extract by status code:
type ClientErrors = Extract<ApiResponse, { statusCode: 400 | 401 | 403 | 404 }>;

// Exclude error responses:
type OkResponses = Exclude<ApiResponse, { type: "error" }>;

// Get all status codes in union:
type AllStatusCodes = ApiResponse["statusCode"]; // 200 | 201 | 400 | 401 | 403 | 404 | 500 | 204

// Filter to success codes:
type SuccessCodes = Extract<AllStatusCodes, 200 | 201 | 204>; // 200 | 201 | 204

// Distributive filtering:
type FilterUnion<Union, Filter extends Union> = Extract<Union, Filter>;

// Get all types that have a `data` field:
type WithData = Extract<ApiResponse, { data: any }>;
// { type: "success", data: User } | { type: "created", data: User, location: string }

// Get data type from responses that have data:
type DataType = Extract<ApiResponse, { data: any }>["data"]; // User
```

---

**Q100. How do you implement a type-safe event system with TypeScript?**

```typescript
// Full type-safe event system with wildcard support

type EventMap = Record<string, unknown>;

type EventKey<T extends EventMap> = string & keyof T;
type EventHandler<T extends EventMap, K extends EventKey<T>> =
  T[K] extends void ? () => void : (payload: T[K]) => void;

class TypedEventBus<Events extends EventMap> {
  private listeners = new Map<string, Set<Function>>();
  private wildcardListeners = new Set<(event: string, payload: unknown) => void>();

  on<K extends EventKey<Events>>(
    event: K,
    handler: EventHandler<Events, K>
  ): () => void {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(handler);
    return () => this.off(event, handler);
  }

  onAny(handler: (event: EventKey<Events>, payload: Events[EventKey<Events>]) => void): () => void {
    this.wildcardListeners.add(handler as any);
    return () => this.wildcardListeners.delete(handler as any);
  }

  once<K extends EventKey<Events>>(event: K, handler: EventHandler<Events, K>): void {
    const unsub = this.on(event, ((...args: any[]) => {
      (handler as any)(...args);
      unsub();
    }) as EventHandler<Events, K>);
  }

  off<K extends EventKey<Events>>(event: K, handler: Function): void {
    this.listeners.get(event)?.delete(handler);
  }

  emit<K extends EventKey<Events>>(
    event: K,
    ...args: Events[K] extends void ? [] : [payload: Events[K]]
  ): void {
    const payload = args[0];
    this.listeners.get(event)?.forEach(h => h(payload));
    this.wildcardListeners.forEach(h => h(event, payload));
  }
}

// Usage:
interface AppEvents {
  "user:login":   { userId: string; timestamp: Date };
  "user:logout":  { userId: string };
  "order:placed": { orderId: string; total: number };
  "app:ready":    void;
}

const bus = new TypedEventBus<AppEvents>();

bus.on("user:login", ({ userId, timestamp }) => {
  console.log(`${userId} logged in at ${timestamp}`);
});

bus.emit("user:login", { userId: "usr_1", timestamp: new Date() }); // ✅
bus.emit("app:ready"); // ✅ no payload needed
bus.emit("user:login", "wrong"); // ❌ Error! wrong payload type
```

---

**Q101. What are TypeScript `const` type parameters?**

```typescript
// TypeScript 5.0: const type parameters — preserve literal types in generics

// Without const — types widened:
function identity<T>(value: T): T { return value; }
const result = identity(["a", "b", "c"]); 
// type: string[] — not readonly ["a","b","c"]

// With const — literal types preserved:
function identityConst<const T>(value: T): T { return value; }
const result2 = identityConst(["a", "b", "c"]);
// type: readonly ["a","b","c"] ✅

// Practical: type-safe route definition
function defineRoute<const T extends string>(path: T): T { return path; }
const route = defineRoute("/users/:id/posts/:postId");
// type: "/users/:id/posts/:postId" — literal preserved!

// Type-safe config:
function createConfig<const T extends Record<string, unknown>>(config: T): T {
  return config;
}

const config = createConfig({
  port: 3000,           // type: 3000, not number
  host: "localhost",    // type: "localhost", not string
  features: ["auth"],   // type: readonly ["auth"], not string[]
});

// Without const modifier:
// config.port type is: number
// With const modifier:
// config.port type is: 3000 — exact literal!

// Difference from `as const`:
// as const: applied at callsite by user
// const type param: enforced by function signature automatically
```

---

**Q102. How do you implement `Prettify` and `Simplify` utility types?**

```typescript
// Prettify / Simplify: flatten intersection types for readable display

// Problem: intersections show as A & B in hover tooltips — hard to read
type UserBase  = { id: string; createdAt: Date };
type UserExtra = { name: string; email: string };
type UserRaw   = UserBase & UserExtra;
// Hovering UserRaw shows: UserBase & UserExtra — not helpful!

// Prettify: force TypeScript to show flat object type
type Prettify<T> = { [K in keyof T]: T[K] } & {};
type User = Prettify<UserBase & UserExtra>;
// Hovering User shows: { id: string; createdAt: Date; name: string; email: string } ✅

// Simplify with deep resolution:
type DeepPrettify<T> =
  T extends (...args: any[]) => any
    ? T
    : T extends object
      ? { [K in keyof T]: DeepPrettify<T[K]> } & {}
      : T;

// Use in utility types to improve DX:
type MergedConfig<A extends object, B extends object> = Prettify<Omit<A, keyof B> & B>;

const merged: MergedConfig<{ a: number; b: string }, { b: number; c: boolean }> = {
  a: 1,   // from A
  b: 2,   // from B (overrides A's b: string)
  c: true // from B
};
// Shows as: { a: number; b: number; c: boolean } ✅ not Omit<...> & {...}

// Expand to make function types readable:
type ExpandFunction<T> =
  T extends (...args: infer A) => infer R
    ? (...args: { [K in keyof A]: A[K] }) => R
    : Prettify<T>;
```

---

**Q103. What is TypeScript's `accessors` flag and accessor keyword?**

```typescript
// TypeScript 4.9: accessor keyword — shorthand for get/set pair
// Generates get + set accessor with backing private field

class Temperature {
  // Old way — manual:
  private _celsius: number;
  get celsius() { return this._celsius; }
  set celsius(value: number) {
    if (value < -273.15) throw new RangeError("Below absolute zero");
    this._celsius = value;
  }

  // New way — accessor keyword:
  accessor kelvin: number = 273.15; // auto-generates get/set + backing field
}

// accessor generates:
// - Private backing field
// - get accessor
// - set accessor
// Useful for decorators that need to intercept property access:

function validate(min: number, max: number) {
  return function <T>(target: any, context: ClassAccessorDecoratorContext<T, number>) {
    return {
      get(this: T) { return context.access.get(this); },
      set(this: T, value: number) {
        if (value < min || value > max) throw new RangeError(`Must be ${min}–${max}`);
        context.access.set(this, value);
      }
    };
  };
}

class Player {
  @validate(0, 100)
  accessor health: number = 100;

  @validate(1, 50)
  accessor level: number = 1;
}

const p = new Player();
p.health = 50; // OK
p.health = 200; // RangeError: Must be 0–100
p.level = 1;   // OK
```

---

**Q104. What are TypeScript's control flow analysis improvements in 5.x?**

```typescript
// TypeScript 5.x: improved narrowing in more scenarios

// 1. Narrowing via instanceof in switch:
function process(shape: Circle | Square | Triangle) {
  switch (true) {
    case shape instanceof Circle:
      shape; // Circle — narrowed! ✅ (TS 5.3+)
      break;
    case shape instanceof Square:
      shape; // Square ✅
      break;
  }
}

// 2. Narrowing via symbol checks:
const OK = Symbol("ok");
const ERR = Symbol("err");

type Result = { tag: typeof OK; value: string } | { tag: typeof ERR; error: Error };

function handleResult(r: Result) {
  if (r.tag === OK) {
    r.value; // string ✅ — narrowed by symbol comparison
  }
}

// 3. Inferred type predicates (TS 5.5):
function isString(x: string | number): boolean {
  return typeof x === "string";
}
// TS 5.5 INFERS this as: x is string (no need to write it manually!)

const arr = [1, "hello", 2, "world", null];
const strings = arr.filter(x => typeof x === "string");
// TS 5.5: type is string[] — previously was (string | number | null)[]!

// 4. Narrowing in destructured conditionals:
function getUser(): { user: User; error: null } | { user: null; error: Error } {
  return { user: null, error: new Error() };
}

const result = getUser();
if (result.user) {
  result.user;  // User ✅
  result.error; // null ✅ — TS narrows both!
}
```

---

**Q105. What are TypeScript's `using` declarations for resource management?**

Already covered in depth — see Q35 extension here with patterns:

```typescript
// Pattern: database transaction management
class Transaction {
  #committed = false;
  readonly id = crypto.randomUUID();

  constructor(private db: Database) {}

  async execute<T>(sql: string, params: unknown[] = []): Promise<T> {
    return this.db.query<T>(sql, params);
  }

  async commit() {
    await this.db.query("COMMIT");
    this.#committed = true;
  }

  async [Symbol.asyncDispose]() {
    if (!this.#committed) {
      await this.db.query("ROLLBACK").catch(() => {}); // best effort rollback
    }
    this.db.releaseConnection();
  }
}

async function transferFunds(fromId: string, toId: string, amount: number) {
  await using tx = new Transaction(await db.getConnection());
  await tx.execute("BEGIN");

  const [from] = await tx.execute<Account[]>(
    "SELECT * FROM accounts WHERE id = $1 FOR UPDATE", [fromId]
  );
  if (!from || from.balance < amount) throw new Error("Insufficient funds");

  await tx.execute("UPDATE accounts SET balance = balance - $1 WHERE id = $2", [amount, fromId]);
  await tx.execute("UPDATE accounts SET balance = balance + $1 WHERE id = $2", [amount, toId]);
  await tx.commit();
} // tx auto-disposed: rollback if not committed, release connection always
```

---

**Q106. How do you type-check configuration files with TypeScript?**

```typescript
// Pattern: validate JSON config with TypeScript types at startup

import { z } from "zod";

// 1. Define schema (runtime + type-level):
const ServerConfigSchema = z.object({
  port:         z.number().int().min(1).max(65535).default(3000),
  host:         z.string().default("localhost"),
  tls: z.object({
    enabled:    z.boolean().default(false),
    certPath:   z.string().optional(),
    keyPath:    z.string().optional(),
  }).default({}),
  rateLimit: z.object({
    windowMs:   z.number().default(60000),
    max:        z.number().default(100),
  }).default({}),
  cors: z.object({
    origins:    z.array(z.string().url()).default([]),
    credentials: z.boolean().default(true),
  }).default({}),
});

// Infer TypeScript type from schema:
type ServerConfig = z.infer<typeof ServerConfigSchema>;
/*
{
  port: number;
  host: string;
  tls: { enabled: boolean; certPath?: string; keyPath?: string };
  rateLimit: { windowMs: number; max: number };
  cors: { origins: string[]; credentials: boolean };
}
*/

// 2. Load and validate at startup:
function loadConfig(path: string): ServerConfig {
  const raw = JSON.parse(fs.readFileSync(path, "utf-8"));
  const result = ServerConfigSchema.safeParse(raw);
  
  if (!result.success) {
    console.error("Invalid config:", result.error.flatten());
    process.exit(1);
  }
  
  return result.data; // fully typed, validated, with defaults applied
}

// 3. Export typed config:
export const config = loadConfig("./config.json");
config.port; // number ✅
config.tls.certPath; // string | undefined ✅
```

---

**Q107. What are TypeScript string manipulation types in practice?**

```typescript
// Built-in: Uppercase<S>, Lowercase<S>, Capitalize<S>, Uncapitalize<S>

// Generate API route constants:
type HttpMethod = "get" | "post" | "put" | "patch" | "delete";
type ApiRoute = `/${string}`;

type MethodRoute = `${Uppercase<HttpMethod>} ${ApiRoute}`;
type ValidRoute = MethodRoute;

const route: ValidRoute = "GET /users/123"; // ✅
const bad: ValidRoute   = "FETCH /users";   // ❌ Error

// Generate event names:
type Resource = "user" | "order" | "product";
type CrudEvent = `${Resource}${"Created" | "Updated" | "Deleted"}`;
// "userCreated" | "userUpdated" | "userDeleted" | "orderCreated" | ...

type EventHandler = `on${Capitalize<CrudEvent>}`;
// "onUserCreated" | "onUserUpdated" | ... | "onProductDeleted"

// Extract type from template:
type ExtractResourceFromEvent<E extends CrudEvent> =
  E extends `${infer R}${"Created" | "Updated" | "Deleted"}` ? R : never;

type R = ExtractResourceFromEvent<"userCreated">; // "user"

// CSS helper types:
type CSSProperty = "margin" | "padding" | "border";
type CSSDirection = "Top" | "Right" | "Bottom" | "Left";
type CSSVariant = `${CSSProperty}${CSSDirection}`;
// "marginTop" | "marginRight" | ... | "borderBottom" | "borderLeft"

type PositiveSize = `${number}px` | `${number}rem` | `${number}%`;
const size: PositiveSize = "16px"; // ✅
const bad2: PositiveSize = "16pt"; // ❌
```

---

**Q108. How do you handle TypeScript with monorepos and shared packages?**

```typescript
// tsconfig.json in root:
{
  "references": [
    { "path": "./packages/shared" },
    { "path": "./packages/api" },
    { "path": "./packages/web" }
  ]
}

// packages/shared/tsconfig.json:
{
  "compilerOptions": {
    "composite": true,     // required for project references
    "declaration": true,
    "declarationMap": true,
    "rootDir": "./src",
    "outDir": "./dist"
  }
}

// packages/api/tsconfig.json:
{
  "references": [{ "path": "../shared" }],
  "compilerOptions": {
    "paths": {
      "@myapp/shared": ["../shared/src"]  // direct source, not compiled
    }
  }
}

// Shared types package — packages/shared/src/types.ts:
export interface User { id: string; name: string; email: string; }
export interface ApiResponse<T> { data: T; meta: { total: number; page: number } }
export type UserId = string & { readonly __brand: "UserId" };

// packages/api/src/users.ts:
import type { User, ApiResponse, UserId } from "@myapp/shared";

// Build: tsc --build (respects references, incremental)
// Benefits:
// - Type errors caught across packages
// - Incremental builds (only rebuild changed packages)
// - Go-to-definition works across package boundaries
// - Circular dependency detection
```

---

**Q109. What is `satisfies` with `as const` for exhaustive object maps?**

```typescript
// Pattern: exhaustive map validated at type level

type Color = "red" | "green" | "blue" | "yellow";

// Without satisfies: either loses literal types OR allows missing keys
const colors1: Record<Color, string> = {
  red: "#ff0000", green: "#00ff00", blue: "#0000ff", yellow: "#ffff00"
};
colors1.red; // string — not "#ff0000"

// With satisfies + as const: validates completeness AND keeps literal types
const colors = {
  red:    "#ff0000",
  green:  "#00ff00",
  blue:   "#0000ff",
  yellow: "#ffff00",
} as const satisfies Record<Color, string>;

colors.red;    // "#ff0000" (literal!) ✅
// Missing a color → TypeScript error ✅
// Extra color → TypeScript error ✅

// Exhaustive action handlers:
type Action = "create" | "read" | "update" | "delete";

const handlers = {
  create: async (data: unknown) => { /* ... */ },
  read:   async (id: string)    => { /* ... */ },
  update: async (id: string, data: unknown) => { /* ... */ },
  delete: async (id: string)    => { /* ... */ },
} satisfies Record<Action, (...args: any[]) => Promise<unknown>>;
// If Action adds "patch", TypeScript immediately errors here ✅

// Combine with discriminated union:
type RouteConfig = {
  path: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  auth: boolean;
};

const routes = {
  listUsers:   { path: "/users",     method: "GET",    auth: true  },
  createUser:  { path: "/users",     method: "POST",   auth: true  },
  getUser:     { path: "/users/:id", method: "GET",    auth: true  },
  deleteUser:  { path: "/users/:id", method: "DELETE", auth: true  },
} as const satisfies Record<string, RouteConfig>;
// Each value keeps its literal types: method is "GET" not string
```

---

**Q110. How do you write TypeScript declaration files for JavaScript libraries?**

```typescript
// Writing .d.ts for a JavaScript library: "my-analytics.js"

// Simple case — module with named exports:
// my-analytics.d.ts:
export declare function track(event: string, properties?: Record<string, unknown>): void;
export declare function identify(userId: string, traits?: Record<string, unknown>): void;
export declare function page(name?: string, properties?: Record<string, unknown>): void;

export declare class Analytics {
  constructor(writeKey: string, options?: AnalyticsOptions);
  track(event: string, properties?: Record<string, unknown>): Promise<void>;
  flush(): Promise<void>;
  readonly initialized: boolean;
}

export interface AnalyticsOptions {
  host?: string;
  timeout?: number;
  maxQueueSize?: number;
  flushAt?: number;
  flushInterval?: number;
}

export declare const VERSION: string;
export default Analytics;

// For a UMD library (also available as window.Analytics):
// analytics-global.d.ts:
export as namespace Analytics;
export declare function track(event: string): void;

// Conditional types in declaration files:
export declare function parse<T extends "json" | "text">(
  response: Response,
  format: T
): Promise<T extends "json" ? unknown : string>;

// Overloads in .d.ts:
export declare function readFile(path: string, encoding: "utf8"): Promise<string>;
export declare function readFile(path: string): Promise<Buffer>;

// Module augmentation from library side:
declare module "express-serve-static-core" {
  interface Request {
    analytics: Analytics;
  }
}
```

---

**Q111–Q120. Rapid-fire TypeScript patterns**

```typescript
// Q111. Mapped type to make specific fields required:
type RequireFields<T, K extends keyof T> = T & Required<Pick<T, K>>;
type UserWithRequiredEmail = RequireFields<Partial<User>, "email">;
// email is Required, rest stays Partial

// Q112. Exclusive union (only one of A or B, not both):
type XOR<T, U> =
  | (T & { [K in keyof U]?: never })
  | (U & { [K in keyof T]?: never });

type CreditCard = { cardNumber: string; cvv: string };
type PayPal     = { paypalEmail: string };
type Payment    = XOR<CreditCard, PayPal>;

const p1: Payment = { cardNumber: "4111", cvv: "123" }; // ✅
const p2: Payment = { paypalEmail: "a@b.com" };          // ✅
const p3: Payment = { cardNumber: "4111", paypalEmail: "a@b.com" }; // ❌

// Q113. Tuple to union and union to intersection:
type TupleToUnion<T extends readonly unknown[]> = T[number];
type T = TupleToUnion<readonly [string, number, boolean]>; // string | number | boolean

type UnionToIntersection<U> =
  (U extends any ? (x: U) => void : never) extends (x: infer I) => void ? I : never;
type I = UnionToIntersection<{ a: 1 } | { b: 2 }>; // { a: 1 } & { b: 2 }

// Q114. Type-safe Object.entries with correct types:
function typedEntries<T extends object>(obj: T): [keyof T, T[keyof T]][] {
  return Object.entries(obj) as [keyof T, T[keyof T]][];
}

// Q115. Recursive Flatten type:
type Flatten<T> =
  T extends Array<infer Item> ? Flatten<Item> : T;
type F = Flatten<number[][][]>; // number

// Q116. Merge two object types (B overrides A):
type Merge<A, B> = Omit<A, keyof B> & B;
type Merged = Merge<{ a: string; b: number }, { b: string; c: boolean }>;
// { a: string; b: string; c: boolean }

// Q117. Make function parameters optional from the end:
type PartialRight<T extends any[], N extends number> =
  T extends [...infer Start, ...infer End extends { length: N }]
    ? [...Start, ...{ [K in keyof End]?: End[K] }]
    : never;

// Q118. Type-safe environment variable access:
const EnvSchema = z.object({
  NODE_ENV: z.enum(["development","test","production"]),
  PORT: z.coerce.number(),
  DATABASE_URL: z.string().url(),
});
const env = EnvSchema.parse(process.env);
env.PORT; // number ✅ (not string!)

// Q119. Discriminated union from object:
const ERRORS = {
  NOT_FOUND:   { code: 404, message: "Not found" },
  UNAUTHORIZED:{ code: 401, message: "Unauthorized" },
  FORBIDDEN:   { code: 403, message: "Forbidden" },
} as const;

type AppError = typeof ERRORS[keyof typeof ERRORS];
// { code: 404; message: "Not found" } | { code: 401; ... } | { code: 403; ... }

// Q120. Type-safe clone with brand preservation:
function clone<T>(obj: T): T {
  return structuredClone(obj);
}
// Branded types preserved through clone!
const id = "usr_123" as UserId;
const clonedId = clone(id); // type: UserId ✅ (not string)
```

---

*TypeScript file now contains 120 complete questions (Q1–Q120). Covers type system fundamentals, generics, conditional types, mapped types, advanced patterns, compiler internals, and production usage.*


---

**Q106. How do you implement strict null safety patterns?**
```typescript
// Non-null assertion vs optional chaining vs nullish coalescing
function processUser(user: User | null | undefined) {
  // Optional chaining — safe, returns undefined if null:
  const name = user?.name;                   // string | undefined
  const city = user?.address?.city;          // string | undefined
  const firstOrder = user?.orders?.[0];      // Order | undefined
  user?.greet?.();                           // method call only if exists

  // Nullish coalescing — only for null/undefined:
  const displayName = user?.name ?? "Anonymous"; // not "" or 0
  const count = user?.orders?.length ?? 0;

  // Non-null assertion — YOU guarantee it's not null:
  const forcedName = user!.name;  // throws at runtime if user is null
  // Only use when you KNOW it's not null (e.g., after a check)

  // Type narrowing (safest):
  if (!user) return null;
  user.name; // User — narrowed

  // Assertion function:
  function assertUser(u: unknown): asserts u is User {
    if (!u || typeof u !== 'object' || !('name' in u)) throw new Error('Not a user');
  }
  assertUser(user);
  user.name; // User
}
```

---

**Q107. What is the `infer` keyword in return position vs parameter position?**
```typescript
// Return position — covariant (multiple same-name infers → UNION):
type ReturnTypes<T extends (...args: any) => any> =
  T extends (...args: any) => infer R ? R : never;

// Parameter position — contravariant (multiple same-name infers → INTERSECTION):
type ParamType<T> =
  T extends { a: (x: infer U) => void; b: (x: infer U) => void } ? U : never;

type Intersection = ParamType<{ a: (x: string) => void; b: (x: number) => void }>;
// string & number = never (impossible intersection)

// Practical: extract Promise value from async method:
type AsyncReturn<T extends object, K extends keyof T> =
  T[K] extends (...args: any) => Promise<infer R> ? R : never;

interface Api {
  getUser(id: string): Promise<User>;
  getOrders(): Promise<Order[]>;
}

type UserResult  = AsyncReturn<Api, 'getUser'>;  // User
type OrderResult = AsyncReturn<Api, 'getOrders'>; // Order[]

// Last overload wins with infer:
function parse(s: string): number;
function parse(n: number): string;
function parse(x: any): any { return x; }

type ParseReturn = ReturnType<typeof parse>; // string (last overload)
```

---

**Q108. What is TypeScript's `NoInfer<T>` and when is it useful?**
```typescript
// NoInfer<T> (TypeScript 5.4+): prevents a position from influencing inference

// Without NoInfer — default value infers T incorrectly:
function createSignal<T>(value: T, defaultValue: T): [T, (v: T) => void] {
  return [value, () => {}];
}
createSignal(42, "fallback"); // T = string | number — not what we want!

// With NoInfer — only first arg infers T:
function createSignalFixed<T>(value: T, defaultValue: NoInfer<T>): [T, (v: T) => void] {
  return [value, () => {}];
}
createSignalFixed(42, "fallback"); // Error! T=number, "fallback" is not number ✅
createSignalFixed(42, 0);          // OK ✅

// Another use case: constrain related parameter:
function addHandler<T extends string>(
  event: T,
  handlers: Record<NoInfer<T>, () => void>  // T inferred from event, not handlers
): void {}

addHandler('click', { click: () => {}, mouseover: () => {} }); 
// Error: 'mouseover' not assignable to 'click' ✅
```

---

**Q109. How do you use `satisfies` to validate discriminated unions?**
```typescript
type Action =
  | { type: 'navigate'; path: string }
  | { type: 'fetch'; url: string; method: 'GET' | 'POST' }
  | { type: 'log'; message: string; level: 'info' | 'warn' | 'error' };

// Handlers map — satisfies ensures all action types are covered
const handlers = {
  navigate: (a: Extract<Action, { type: 'navigate' }>) => {
    window.location.href = a.path;
  },
  fetch: (a: Extract<Action, { type: 'fetch' }>) => {
    return window.fetch(a.url, { method: a.method });
  },
  log: (a: Extract<Action, { type: 'log' }>) => {
    console[a.level](a.message);
  },
} satisfies { [K in Action['type']]: (action: Extract<Action, { type: K }>) => unknown };

// Each handler keeps its specific type:
handlers.navigate; // (a: { type: 'navigate'; path: string }) => void
handlers.fetch;    // (a: { type: 'fetch'; url: string; method: 'GET'|'POST' }) => Promise<Response>

// If we add a new action type and forget the handler — error! ✅
function dispatch(action: Action) {
  (handlers[action.type] as any)(action);
}
```

---

**Q110. What are TypeScript's index signatures vs mapped types differences?**
```typescript
// Index signature — describes unknown string keys:
interface StringRecord {
  [key: string]: string;
  name: string; // OK — must match index sig type
  // count: number; // Error! number not assignable to string
}

// Mapped type — iterates known keys:
type KnownKeys = 'a' | 'b' | 'c';
type Mapped = { [K in KnownKeys]: string };
// { a: string; b: string; c: string }

// Key differences:
// Index signature: keys are unknown at compile time, any string
// Mapped type: keys are known, generates specific properties

// Index sig with template literal:
interface EventMap {
  [K: `on${string}`]: (e: Event) => void; // TS 4.4+
}

// Mapped type with remapping (as clause):
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
};
type UserGetters = Getters<{ name: string; age: number }>;
// { getName(): string; getAge(): number }

// noUncheckedIndexedAccess — index sig returns T | undefined:
// tsconfig: "noUncheckedIndexedAccess": true
const m: StringRecord = { name: 'Alice' };
const v = m['random']; // string | undefined (safer!)
v.toUpperCase(); // Error — might be undefined
v?.toUpperCase(); // OK
```

---

**Q111. How do you implement recursive TypeScript types safely?**
```typescript
// TypeScript has recursion depth limit — use lazy evaluation for deep types

// Direct recursion (limited depth):
type JSONValue =
  | string | number | boolean | null
  | JSONValue[]                        // recursive
  | { [key: string]: JSONValue };      // recursive

// Deep path with recursion guard:
type Paths<T, D extends number = 10> = [D] extends [0] ? never :
  T extends object ? {
    [K in keyof T & string]:
      K | `${K}.${Paths<T[K], [-1,0,1,2,3,4,5,6,7,8,9][D]>}`
  }[keyof T & string]
  : never;

// Tail recursion pattern (avoid stack overflow at type level):
type Reverse<T extends any[], Acc extends any[] = []> =
  T extends [infer Head, ...infer Tail]
    ? Reverse<Tail, [Head, ...Acc]>
    : Acc;

type Rev = Reverse<[1, 2, 3, 4, 5]>; // [5, 4, 3, 2, 1]

// Recursive conditional with counter to prevent infinite:
type DeepReplace<T, From, To, Depth extends any[] = []> =
  Depth['length'] extends 10 ? T :  // stop at depth 10
  T extends From ? To :
  T extends object ? {
    [K in keyof T]: DeepReplace<T[K], From, To, [0, ...Depth]>
  } : T;
```

---

**Q112–Q120. TypeScript quick reference patterns**
```typescript
// Q112. Extract keys by value type:
type KeysByValue<T, V> = { [K in keyof T]: T[K] extends V ? K : never }[keyof T];
interface User { id: number; name: string; active: boolean; age: number; }
type StringKeys = KeysByValue<User, string>; // "name"
type NumberKeys = KeysByValue<User, number>; // "id" | "age"

// Q113. Readonly deep partial (for default config merging):
type DeepReadonlyPartial<T> = {
  readonly [K in keyof T]?: T[K] extends object ? DeepReadonlyPartial<T[K]> : T[K]
};

// Q114. Create union from object values:
const ROLES = { ADMIN: 'admin', USER: 'user', EDITOR: 'editor' } as const;
type Role = typeof ROLES[keyof typeof ROLES]; // "admin" | "user" | "editor"

// Q115. Override specific fields in generic type:
type Override<T, U> = Omit<T, keyof U> & U;
type UserUpdate = Override<User, { age?: number; name?: string }>;

// Q116. PickPartial — some fields partial, rest required:
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
type CreateUser = PartialBy<User, 'id' | 'active'>; // id & active optional

// Q117. Function that returns typed subset:
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  return keys.reduce((acc, k) => ({ ...acc, [k]: obj[k] }), {} as Pick<T, K>);
}
const preview = pick(user, ['id', 'name']); // { id: number; name: string }

// Q118. Exhaustive match helper:
function match<T extends string, R>(
  value: T,
  cases: Record<T, () => R>
): R { return cases[value](); }
const label = match(status, {
  pending: () => 'Pending',
  active:  () => 'Active',
  done:    () => 'Done',
});

// Q119. Conditional required fields based on discriminant:
type Form =
  | { type: 'login';    email: string; password: string }
  | { type: 'register'; email: string; password: string; name: string }
  | { type: 'reset';    email: string };

// Q120. Type predicate array filter (TS 5.5):
const mixed = [1, 'hello', null, 2, 'world', undefined];
const strings = mixed.filter((x): x is string => typeof x === 'string');
// string[] — correctly typed!
const numbers = mixed.filter((x): x is number => typeof x === 'number');
// number[]
```
