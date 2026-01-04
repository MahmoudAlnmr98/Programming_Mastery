# TypeScript Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is TypeScript? Why use it?

**Answer:**
TypeScript is a superset of JavaScript that adds static type checking.

**Benefits:**
- **Type Safety**: Catch errors at compile time
- **Better IDE Support**: Autocomplete, refactoring
- **Documentation**: Types serve as documentation
- **Refactoring**: Safer code changes
- **Scalability**: Better for large codebases

### 2. Explain basic types in TypeScript.

**Answer:**
```typescript
// Primitive types
let name: string = "John";
let age: number = 30;
let isActive: boolean = true;
let nothing: null = null;
let notDefined: undefined = undefined;

// Arrays
let numbers: number[] = [1, 2, 3];
let names: Array<string> = ["John", "Jane"];

// Tuples
let tuple: [string, number] = ["John", 30];

// Any
let anything: any = "can be anything";

// Void
function log(): void {
    console.log("Hello");
}

// Never
function error(): never {
    throw new Error("Error");
}
```

### 3. What is the difference between `interface` and `type`?

**Answer:**
**Interface:**
```typescript
interface User {
    name: string;
    age: number;
}

interface User {
    email: string; // Can be extended
}
```

**Type:**
```typescript
type User = {
    name: string;
    age: number;
}

// Can use unions, intersections
type ID = string | number;
type Admin = User & { role: "admin" };
```

**Differences:**
- Interfaces can be merged (declaration merging)
- Types can use unions, intersections, primitives
- Interfaces are better for object shapes
- Types are more flexible

### 4. Explain type inference in TypeScript.

**Answer:**
TypeScript infers types when not explicitly provided.

```typescript
let x = 10; // TypeScript infers: number
let y = "hello"; // TypeScript infers: string

function add(a: number, b: number) {
    return a + b; // Return type inferred as number
}

// Explicit types
let x: number = 10;
function add(a: number, b: number): number {
    return a + b;
}
```

### 5. Explain optional and readonly properties.

**Answer:**
```typescript
interface User {
    name: string;
    age?: number; // Optional
    readonly id: number; // Readonly
}

const user: User = {
    name: "John",
    id: 1
};

// user.id = 2; // Error: Cannot assign to 'id'
// user.age is optional, may be undefined
```

### 6. Explain function types in TypeScript.

**Answer:**
```typescript
// Function type
function greet(name: string): string {
    return `Hello, ${name}`;
}

// Function type annotation
let greetFn: (name: string) => string;
greetFn = (name: string) => `Hello, ${name}`;

// Optional parameters
function greet(name: string, title?: string): string {
    return title ? `Hello, ${title} ${name}` : `Hello, ${name}`;
}

// Default parameters
function greet(name: string, title: string = "Mr"): string {
    return `Hello, ${title} ${name}`;
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((a, b) => a + b, 0);
}
```

### 7. Explain union and intersection types.

**Answer:**
```typescript
// Union type
type ID = string | number;
let id: ID = "123";
id = 123; // Also valid

// Intersection type
type Admin = User & { role: "admin" };

interface User {
    name: string;
}

interface Admin {
    role: "admin";
}

type AdminUser = User & Admin;
```

### 8. Explain enums in TypeScript.

**Answer:**
```typescript
// Numeric enum
enum Status {
    Pending,    // 0
    Approved,   // 1
    Rejected    // 2
}

// String enum
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}

// Const enum (inlined at compile time)
const enum Color {
    Red,
    Green,
    Blue
}
```

---

## Intermediate Level

### 9. Explain generics in TypeScript.

**Answer:**
Generics allow creating reusable components.

```typescript
// Generic function
function identity<T>(arg: T): T {
    return arg;
}

let output = identity<string>("hello");
let output2 = identity<number>(42);

// Generic interface
interface Box<T> {
    value: T;
}

let box: Box<number> = { value: 42 };

// Generic class
class Stack<T> {
    private items: T[] = [];
    
    push(item: T): void {
        this.items.push(item);
    }
    
    pop(): T | undefined {
        return this.items.pop();
    }
}

let stack = new Stack<number>();
```

### 10. Explain type guards and narrowing.

**Answer:**
Type guards narrow types within conditional blocks.

```typescript
// typeof guard
function padLeft(value: string, padding: string | number) {
    if (typeof padding === "number") {
        return Array(padding + 1).join(" ") + value;
    }
    return padding + value;
}

// instanceof guard
function process(value: Date | string) {
    if (value instanceof Date) {
        return value.toISOString();
    }
    return value.toUpperCase();
}

// in guard
interface Fish {
    swim: () => void;
}
interface Bird {
    fly: () => void;
}

function move(animal: Fish | Bird) {
    if ("swim" in animal) {
        animal.swim();
    } else {
        animal.fly();
    }
}

// Custom type guard
function isString(value: unknown): value is string {
    return typeof value === "string";
}
```

### 11. Explain utility types.

**Answer:**
TypeScript provides utility types for common transformations.

```typescript
interface User {
    name: string;
    age: number;
    email: string;
}

// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Readonly - all properties readonly
type ReadonlyUser = Readonly<User>;

// Pick - select properties
type UserName = Pick<User, "name">;

// Omit - exclude properties
type UserWithoutEmail = Omit<User, "email">;

// Record - create object type
type UserMap = Record<string, User>;

// Exclude - exclude types from union
type NonNull = Exclude<string | null | undefined, null | undefined>;

// Extract - extract types from union
type StringOnly = Extract<string | number, string>;
```

### 12. Explain decorators in TypeScript.

**Answer:**
Decorators add metadata and modify classes, methods, properties.

```typescript
// Class decorator
function sealed(constructor: Function) {
    Object.seal(constructor);
    Object.seal(constructor.prototype);
}

@sealed
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
}

// Method decorator
function log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = function (...args: any[]) {
        console.log(`Calling ${propertyKey} with`, args);
        return originalMethod.apply(this, args);
    };
}

class Calculator {
    @log
    add(a: number, b: number): number {
        return a + b;
    }
}
```

### 13. Explain namespaces and modules.

**Answer:**
**Namespaces:**
```typescript
namespace MathUtils {
    export function add(a: number, b: number): number {
        return a + b;
    }
}

MathUtils.add(1, 2);
```

**Modules:**
```typescript
// math.ts
export function add(a: number, b: number): number {
    return a + b;
}

export default function multiply(a: number, b: number): number {
    return a * b;
}

// app.ts
import multiply, { add } from './math';
```

### 14. Explain conditional types.

**Answer:**
Conditional types select types based on conditions.

```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;

type Parameters<T> = T extends (...args: infer P) => any ? P : never;

// Example usage
type T1 = NonNullable<string | null>; // string
type T2 = ReturnType<() => string>; // string
type T3 = Parameters<(a: number, b: string) => void>; // [number, string]
```

### 15. Explain mapped types.

**Answer:**
Mapped types create new types by transforming properties.

```typescript
// Make all properties optional
type Optional<T> = {
    [P in keyof T]?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

// Make all properties nullable
type Nullable<T> = {
    [P in keyof T]: T[P] | null;
};

// Custom mapped type
type Getters<T> = {
    [P in keyof T as `get${Capitalize<string & P>}`]: () => T[P];
};
```

---

## Advanced Level

### 16. Explain template literal types.

**Answer:**
Template literal types create string literal types.

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;
type ClickEvent = EventName<"click">; // "onClick"

type PropName<T extends string> = `get${Capitalize<T>}`;
type GetName = PropName<"name">; // "getName"

// Complex example
type ApiEndpoint = "users" | "posts" | "comments";
type HttpMethod = "get" | "post" | "put" | "delete";
type ApiRoute = `${HttpMethod} /api/${ApiEndpoint}`;
```

### 17. Explain recursive types.

**Answer:**
Types that reference themselves.

```typescript
// Recursive type
type JsonValue = 
    | string
    | number
    | boolean
    | null
    | JsonValue[]
    | { [key: string]: JsonValue };

// Recursive interface
interface TreeNode<T> {
    value: T;
    children?: TreeNode<T>[];
}
```

### 18. Explain brand types and nominal typing.

**Answer:**
Brand types create distinct types from same underlying type.

```typescript
// Brand type
type UserId = string & { readonly brand: unique symbol };
type ProductId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
    return id as UserId;
}

function createProductId(id: string): ProductId {
    return id as ProductId;
}

let userId = createUserId("123");
let productId = createProductId("123");

// userId === productId; // Type error
```

### 19. Explain assertion functions.

**Answer:**
Functions that assert types at runtime.

```typescript
function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== "string") {
        throw new Error("Not a string");
    }
}

function process(value: unknown) {
    assertIsString(value);
    // value is now string
    value.toUpperCase();
}
```

### 20. Explain module augmentation.

**Answer:**
Extending existing module types.

```typescript
// Augment existing module
declare module "express" {
    interface Request {
        user?: User;
    }
}

// Now Request has user property
app.get("/", (req, res) => {
    req.user; // TypeScript knows this exists
});
```

### 21. Explain type-level programming.

**Answer:**
Programming at the type level.

```typescript
// Type-level arithmetic
type Length<T extends any[]> = T["length"];

type Tuple3 = [1, 2, 3];
type Len = Length<Tuple3>; // 3

// Type-level conditionals
type If<C extends boolean, T, F> = C extends true ? T : F;

type Result = If<true, string, number>; // string

// Type-level recursion
type Reverse<T extends any[]> = T extends [infer First, ...infer Rest]
    ? [...Reverse<Rest>, First]
    : [];
```

### 22. Explain variance in TypeScript.

**Answer:**
How subtyping works with generics.

```typescript
// Covariance - preserves subtyping
interface Animal {
    name: string;
}
interface Dog extends Animal {
    breed: string;
}

let animals: Animal[] = [];
let dogs: Dog[] = [];
animals = dogs; // OK - covariant

// Contravariance - reverses subtyping
type Handler<T> = (value: T) => void;

let animalHandler: Handler<Animal> = (animal: Animal) => {};
let dogHandler: Handler<Dog> = (dog: Dog) => {};

dogHandler = animalHandler; // OK - contravariant
// animalHandler = dogHandler; // Error
```

### 23. Explain declaration merging.

**Answer:**
TypeScript merges multiple declarations of same name.

```typescript
// Interface merging
interface User {
    name: string;
}
interface User {
    age: number;
}
// Result: { name: string; age: number; }

// Namespace merging
namespace Math {
    export function add(a: number, b: number): number {
        return a + b;
    }
}
namespace Math {
    export function subtract(a: number, b: number): number {
        return a - b;
    }
}
```

### 24. Explain type erasure and runtime behavior.

**Answer:**
TypeScript types are erased at compile time.

```typescript
// TypeScript
function add(a: number, b: number): number {
    return a + b;
}

// Compiled JavaScript
function add(a, b) {
    return a + b;
}

// Runtime type checking needed
function isString(value: unknown): value is string {
    return typeof value === "string";
}
```

### 25. Explain advanced generic constraints.

**Answer:**
```typescript
// Multiple constraints
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

// Keyof constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

// Conditional constraints
type NonFunctionPropertyNames<T> = {
    [K in keyof T]: T[K] extends Function ? never : K;
}[keyof T];

// Mapped type constraints
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};
```

### 26. Explain TypeScript's module resolution.

**Answer:**
TypeScript resolves modules using module resolution strategies.

**Resolution Strategies:**
- **Classic**: For TypeScript < 1.6
- **Node**: Mimics Node.js resolution

**Node Resolution:**
```json
{
  "compilerOptions": {
    "moduleResolution": "node",
    "baseUrl": "./",
    "paths": {
      "@/*": ["src/*"],
      "components/*": ["src/components/*"]
    }
  }
}
```

### 27. Explain TypeScript's strict mode.

**Answer:**
Strict mode enables all strict type checking options.

```json
{
  "compilerOptions": {
    "strict": true,
    // Or individually:
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

**Benefits:**
- Catches more errors at compile time
- Better type safety
- Prevents common bugs

### 28. Explain TypeScript's declaration files (.d.ts).

**Answer:**
Declaration files provide type information for JavaScript libraries.

```typescript
// types.d.ts
declare module 'my-library' {
    export function doSomething(): void;
    export const value: number;
}

// Global declarations
declare global {
    interface Window {
        myCustomProperty: string;
    }
}
```

### 29. Explain TypeScript's tsconfig.json options.

**Answer:**
**Common Options:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "sourceMap": true,
    "declaration": true,
    "removeComments": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 30. Explain TypeScript's type narrowing techniques.

**Answer:**
Type narrowing reduces type to more specific type.

**Techniques:**
```typescript
// typeof guards
function process(value: string | number) {
    if (typeof value === 'string') {
        return value.toUpperCase(); // string
    }
    return value.toFixed(2); // number
}

// instanceof guards
function process(value: Date | string) {
    if (value instanceof Date) {
        return value.toISOString(); // Date
    }
    return value.toUpperCase(); // string
}

// Discriminated unions
type Success = { status: 'success'; data: string };
type Error = { status: 'error'; message: string };
type Result = Success | Error;

function handle(result: Result) {
    if (result.status === 'success') {
        console.log(result.data); // Success
    } else {
        console.log(result.message); // Error
    }
}
```

### 31. Explain TypeScript utility types in detail.

**Answer:**
Utility types transform existing types.

**Partial:**
```typescript
interface User {
    name: string;
    age: number;
    email: string;
}

type PartialUser = Partial<User>;
// { name?: string; age?: number; email?: string; }
```

**Required:**
```typescript
type RequiredUser = Required<PartialUser>;
// All properties required
```

**Readonly:**
```typescript
type ReadonlyUser = Readonly<User>;
// All properties readonly
```

**Pick:**
```typescript
type UserName = Pick<User, 'name' | 'email'>;
// { name: string; email: string; }
```

**Omit:**
```typescript
type UserWithoutEmail = Omit<User, 'email'>;
// { name: string; age: number; }
```

**Record:**
```typescript
type UserMap = Record<string, User>;
// { [key: string]: User; }
```

**Exclude/Extract:**
```typescript
type T1 = Exclude<'a' | 'b' | 'c', 'a'>; // 'b' | 'c'
type T2 = Extract<'a' | 'b' | 'c', 'a' | 'd'>; // 'a'
```

**NonNullable:**
```typescript
type T = NonNullable<string | null | undefined>; // string
```

### 32. Explain TypeScript conditional types.

**Answer:**
Conditional types select types based on conditions.

```typescript
type IsArray<T> = T extends Array<any> ? true : false;

type T1 = IsArray<string[]>; // true
type T2 = IsArray<string>; // false
```

**Infer Keyword:**
```typescript
type ArrayElementType<T> = T extends Array<infer U> ? U : never;

type T1 = ArrayElementType<string[]>; // string
type T2 = ArrayElementType<number[]>; // number
```

**Flatten Array:**
```typescript
type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T;

type T1 = Flatten<string[][]>; // string
type T2 = Flatten<number[][][]>; // number
```

**Return Type:**
```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type T = ReturnType<() => string>; // string
```

### 33. Explain TypeScript template literal types.

**Answer:**
Template literal types create string literal types.

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<'click'>; // 'onClick'
type ChangeEvent = EventName<'change'>; // 'onChange'
```

**String Manipulation:**
```typescript
type Uppercase<S extends string> = // Built-in
type Lowercase<S extends string> = // Built-in
type Capitalize<S extends string> = // Built-in
type Uncapitalize<S extends string> = // Built-in
```

**Path Types:**
```typescript
type Path<T> = T extends object
    ? {
        [K in keyof T]: K extends string
            ? `${K}` | `${K}.${Path<T[K]>}`
            : never;
    }[keyof T]
    : never;

type UserPaths = Path<{ name: string; address: { city: string } }>;
// 'name' | 'address' | 'address.city'
```

### 34. Explain TypeScript declaration merging.

**Answer:**
Declaration merging combines multiple declarations.

**Interface Merging:**
```typescript
interface User {
    name: string;
}

interface User {
    age: number;
}

// Merged: { name: string; age: number; }
```

**Namespace Merging:**
```typescript
namespace MyLib {
    export function func1() {}
}

namespace MyLib {
    export function func2() {}
}

// Both func1 and func2 available
```

**Module Augmentation:**
```typescript
// Original module
declare module 'express' {
    interface Request {
        user?: User;
    }
}

// Usage
app.use((req, res) => {
    req.user; // TypeScript knows about this
});
```

### 35. Explain TypeScript performance and compilation options.

**Answer:**
**Compiler Options:**
```json
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "lib": ["ES2020", "DOM"],
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "incremental": true,
        "tsBuildInfoFile": ".tsbuildinfo"
    }
}
```

**Performance Tips:**
- Use `incremental` for faster rebuilds
- Use `skipLibCheck` to skip type checking libraries
- Use project references for large codebases
- Use `isolatedModules` for faster compilation

**Project References:**
```json
{
    "references": [
        { "path": "./shared" },
        { "path": "./utils" }
    ]
}
```

### 36. Explain TypeScript's const assertions.

**Answer:**
const assertions create readonly literal types.

```typescript
// Without const assertion
const arr = [1, 2, 3]; // number[]

// With const assertion
const arr = [1, 2, 3] as const; // readonly [1, 2, 3]

// Object
const obj = { name: 'John', age: 30 } as const;
// { readonly name: "John"; readonly age: 30; }
```

**Use Cases:**
- Immutable data structures
- Literal types
- Tuple types

### 37. Explain TypeScript's satisfies operator.

**Answer:**
satisfies ensures type matches without widening.

```typescript
// Without satisfies
const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000
}; // Type is inferred

// With satisfies
const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000
} satisfies Config; // Type checked but not widened
```

**Benefits:**
- Type checking without type widening
- Preserves literal types
- Better autocomplete

### 38. Explain TypeScript's satisfies vs as const.

**Answer:**
**as const:**
```typescript
const config = { apiUrl: 'https://api.example.com' } as const;
// Makes everything readonly and literal
```

**satisfies:**
```typescript
const config = { apiUrl: 'https://api.example.com' } satisfies Config;
// Type checks but preserves types
```

**Differences:**
- `as const`: Makes readonly, literal types
- `satisfies`: Type checks, preserves original types

### 39. Explain TypeScript's module augmentation for third-party libraries.

**Answer:**
Extend types from third-party libraries.

```typescript
// node_modules/@types/express/index.d.ts
declare module 'express' {
    interface Request {
        user?: User;
    }
}

// Now Request has user property
app.get('/', (req, res) => {
    req.user; // TypeScript knows about this
});
```

**Global Augmentation:**
```typescript
declare global {
    interface Window {
        myCustomProperty: string;
    }
}
```

### 40. Explain TypeScript's type predicates in detail.

**Answer:**
Type predicates narrow types in conditional blocks.

```typescript
function isString(value: unknown): value is string {
    return typeof value === 'string';
}

function process(value: unknown) {
    if (isString(value)) {
        // value is string here
        value.toUpperCase();
    }
}
```

**Complex Example:**
```typescript
interface Cat {
    type: 'cat';
    meow: () => void;
}

interface Dog {
    type: 'dog';
    bark: () => void;
}

function isCat(animal: Cat | Dog): animal is Cat {
    return animal.type === 'cat';
}

function handle(animal: Cat | Dog) {
    if (isCat(animal)) {
        animal.meow(); // TypeScript knows it's Cat
    } else {
        animal.bark(); // TypeScript knows it's Dog
    }
}
```

### 41. Explain TypeScript's assertion functions.

**Answer:**
Functions that assert types at runtime.

```typescript
function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== 'string') {
        throw new Error('Not a string');
    }
}

function process(value: unknown) {
    assertIsString(value);
    // value is string here
    value.toUpperCase();
}
```

**Assertion with Condition:**
```typescript
function assert(condition: unknown): asserts condition {
    if (!condition) {
        throw new Error('Assertion failed');
    }
}

function process(value: unknown) {
    assert(typeof value === 'string');
    // value is string here
}
```

### 42. Explain TypeScript's readonly modifier.

**Answer:**
readonly prevents mutation.

```typescript
interface User {
    readonly id: number;
    readonly name: string;
    age: number; // Mutable
}

const user: User = { id: 1, name: 'John', age: 30 };
user.id = 2; // Error
user.age = 31; // OK

// Readonly array
const arr: readonly number[] = [1, 2, 3];
arr.push(4); // Error
arr[0] = 0; // Error
```

**Deep Readonly:**
```typescript
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};
```

### 43. Explain TypeScript's keyof operator.

**Answer:**
keyof creates union of object keys.

```typescript
interface User {
    id: number;
    name: string;
    email: string;
}

type UserKeys = keyof User; // 'id' | 'name' | 'email'

function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user: User = { id: 1, name: 'John', email: 'john@example.com' };
const name = getProperty(user, 'name'); // string
```

### 44. Explain TypeScript's typeof operator.

**Answer:**
typeof gets type of value.

```typescript
const user = {
    id: 1,
    name: 'John',
    email: 'john@example.com'
};

type UserType = typeof user;
// { id: number; name: string; email: string; }

// With functions
function createUser() {
    return { id: 1, name: 'John' };
}

type User = ReturnType<typeof createUser>;
// { id: number; name: string; }
```

### 45. Explain TypeScript's indexed access types.

**Answer:**
Access property types using bracket notation.

```typescript
interface User {
    id: number;
    name: string;
    address: {
        street: string;
        city: string;
    };
}

type UserName = User['name']; // string
type UserAddress = User['address']; // { street: string; city: string; }
type Street = User['address']['street']; // string

// Union of all property types
type UserValues = User[keyof User]; // number | string | { street: string; city: string; }
```

### 46. Explain TypeScript's template literal types with unions.

**Answer:**
Template literal types with unions create all combinations.

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiEndpoint = 'users' | 'posts' | 'comments';

type ApiRoute = `${HttpMethod} /api/${ApiEndpoint}`;
// "GET /api/users" | "GET /api/posts" | "GET /api/comments" | ...

// Complex example
type EventName<T extends string> = `on${Capitalize<T>}`;
type MouseEvent = EventName<'click' | 'hover'>;
// "onClick" | "onHover"
```

### 47. Explain TypeScript's distributive conditional types.

**Answer:**
Conditional types distribute over union types.

```typescript
type ToArray<T> = T extends any ? T[] : never;

type StrArrOrNumArr = ToArray<string | number>;
// string[] | number[] (distributed)

// Non-distributive
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type StrOrNumArr = ToArrayNonDist<string | number>;
// (string | number)[] (not distributed)
```

### 48. Explain TypeScript's mapped types with modifiers.

**Answer:**
Mapped types can add/remove modifiers.

```typescript
// Remove readonly
type Writable<T> = {
    -readonly [P in keyof T]: T[P];
};

// Remove optional
type Required<T> = {
    [P in keyof T]-?: T[P];
};

// Make optional
type Partial<T> = {
    [P in keyof T]?: T[P];
};
```

### 49. Explain TypeScript's string manipulation types.

**Answer:**
Built-in string manipulation types.

```typescript
type Uppercase<S extends string> = // Built-in
type Lowercase<S extends string> = // Built-in
type Capitalize<S extends string> = // Built-in
type Uncapitalize<S extends string> = // Built-in

type T1 = Uppercase<'hello'>; // "HELLO"
type T2 = Lowercase<'HELLO'>; // "hello"
type T3 = Capitalize<'hello'>; // "Hello"
type T4 = Uncapitalize<'Hello'>; // "hello"
```

### 50. Explain TypeScript's brand types for nominal typing.

**Answer:**
Brand types create distinct types from same underlying type.

```typescript
// Brand type
type UserId = string & { readonly brand: unique symbol };
type ProductId = string & { readonly brand: unique symbol };

function createUserId(id: string): UserId {
    return id as UserId;
}

function createProductId(id: string): ProductId {
    return id as ProductId;
}

let userId = createUserId('123');
let productId = createProductId('123');

// userId === productId; // Type error (different brands)
```

---

This covers TypeScript interview questions from beginner to advanced level with detailed explanations and code examples.

