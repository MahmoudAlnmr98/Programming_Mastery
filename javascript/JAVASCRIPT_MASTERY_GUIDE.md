# JavaScript — Complete Reference Guide (Zero to Advanced)

> This guide assumes **zero prior knowledge**. Every concept is explained from the ground up with detailed examples, mental models, and real-world context. Nothing is skipped.

---

## Table of Contents

1. [What is JavaScript?](#1-what-is-javascript)
2. [How JavaScript Runs — The Engine & Runtime](#2-how-javascript-runs--the-engine--runtime)
3. [Variables & Memory](#3-variables--memory)
4. [Data Types in Depth](#4-data-types-in-depth)
5. [Operators](#5-operators)
6. [Control Flow](#6-control-flow)
7. [Functions — Every Detail](#7-functions--every-detail)
8. [Scope, Closures & the Lexical Environment](#8-scope-closures--the-lexical-environment)
9. [The `this` Keyword](#9-the-this-keyword)
10. [Prototypes & Prototype Chain](#10-prototypes--prototype-chain)
11. [Classes](#11-classes)
12. [Arrays — Complete Guide](#12-arrays--complete-guide)
13. [Objects — Complete Guide](#13-objects--complete-guide)
14. [Destructuring & Spread / Rest](#14-destructuring--spread--rest)
15. [Iterators & Generators](#15-iterators--generators)
16. [Symbols & Well-Known Symbols](#16-symbols--well-known-symbols)
17. [The Event Loop — Deep Dive](#17-the-event-loop--deep-dive)
18. [Promises — Complete Guide](#18-promises--complete-guide)
19. [Async / Await](#19-async--await)
20. [Error Handling](#20-error-handling)
21. [Modules (ESM & CJS)](#21-modules-esm--cjs)
22. [Map, Set, WeakMap, WeakSet](#22-map-set-weakmap-weakset)
23. [Regular Expressions](#23-regular-expressions)
24. [JSON](#24-json)
25. [The DOM (Browser Environment)](#25-the-dom-browser-environment)
26. [Events & Event Delegation](#26-events--event-delegation)
27. [Fetch API & HTTP](#27-fetch-api--http)
28. [Storage APIs](#28-storage-apis)
29. [Functional Programming Patterns](#29-functional-programming-patterns)
30. [Design Patterns in JavaScript](#30-design-patterns-in-javascript)
31. [Memory Management & Garbage Collection](#31-memory-management--garbage-collection)
32. [Performance Optimization](#32-performance-optimization)
33. [Security Basics](#33-security-basics)
34. [Node.js Fundamentals](#34-nodejs-fundamentals)
35. [Testing in JavaScript](#35-testing-in-javascript)
36. [Modern JavaScript Tooling](#36-modern-javascript-tooling)

---

## 1. What is JavaScript?

JavaScript is a **high-level**, **interpreted** (or just-in-time compiled), **dynamically typed**, **single-threaded**, **garbage-collected** programming language with **first-class functions**.

Let's unpack every adjective:

| Term | Meaning |
|------|---------|
| High-level | You don't manage memory manually (unlike C/C++) |
| Interpreted / JIT | Code is read and executed directly, not compiled to a binary ahead of time (though modern engines do JIT compile) |
| Dynamically typed | Variable types are determined at runtime, not compile time |
| Single-threaded | Only one thing executes at a time on the main thread |
| Garbage-collected | Memory no longer in use is automatically freed |
| First-class functions | Functions are values — they can be stored in variables, passed as arguments, returned from other functions |

### Where does JavaScript run?

JavaScript was originally designed to run **inside browsers** to make web pages interactive. Today it also runs on servers (Node.js), mobile apps (React Native), desktop apps (Electron), IoT devices, and more.

```
Browser:
  HTML + CSS = structure and style
  JavaScript = behavior (clicks, animations, data fetching, etc.)

Server (Node.js):
  JavaScript = file system, networking, databases, APIs
```

### A brief history

- **1995** — Brendan Eich created JavaScript in 10 days at Netscape
- **1997** — Standardized as ECMAScript (ES1)
- **2009** — ES5 — major improvements (strict mode, JSON, Array methods)
- **2015** — ES6/ES2015 — the biggest update ever (let/const, classes, arrow functions, promises, modules, etc.)
- **2016–present** — Yearly releases (ES2016, ES2017, …, ES2024)

---

## 2. How JavaScript Runs — The Engine & Runtime

### The JavaScript Engine

A JS engine reads your code and executes it. The most famous engine is **V8** (used in Chrome and Node.js). Other engines: SpiderMonkey (Firefox), JavaScriptCore (Safari).

**What V8 does internally:**

```
Your JS Code
    ↓
[Parser] — reads characters, checks syntax, builds AST
    ↓
[AST — Abstract Syntax Tree] — tree representation of your code
    ↓
[Interpreter (Ignition)] — generates bytecode and executes it
    ↓
[Profiler] — watches hot (frequently called) code
    ↓
[Compiler (TurboFan)] — compiles hot code to optimized machine code
    ↓
[Machine Code] — runs directly on the CPU
```

This process is called **JIT (Just-In-Time) compilation** — it's why modern JavaScript is very fast despite being "interpreted."

### The Runtime

The engine alone cannot do everything. The **runtime** adds:
- The **Call Stack** — tracks function calls
- **Web APIs** (browser) or **Node APIs** (Node.js) — timers, DOM, fetch, fs, etc.
- The **Event Loop** — coordinates async operations
- **Callback Queue / Microtask Queue** — holds async callbacks waiting to run

```
┌─────────────────────────────────────────────┐
│                 JS Engine                   │
│  ┌────────────┐    ┌──────────────────────┐ │
│  │ Call Stack │    │      Heap            │ │
│  │            │    │  (object storage)    │ │
│  └────────────┘    └──────────────────────┘ │
└─────────────────────────────────────────────┘
          ↕ Event Loop ↕
┌─────────────────────────────────────────────┐
│          Web APIs / Node APIs               │
│  setTimeout, fetch, fs.readFile, etc.       │
└─────────────────────────────────────────────┘
          ↕
┌──────────────────┐  ┌──────────────────────┐
│  Microtask Queue │  │   Callback Queue     │
│  (Promises, etc) │  │  (setTimeout, etc)   │
└──────────────────┘  └──────────────────────┘
```

We'll revisit this in the Event Loop section.

---

## 3. Variables & Memory

### Declaring Variables

JavaScript has three ways to declare variables:

```javascript
var name = "Alice";   // Old way — avoid in modern code
let age = 30;         // Block-scoped, can be reassigned
const PI = 3.14;      // Block-scoped, cannot be reassigned
```

### `var` — The Old Way (and Why to Avoid It)

`var` has **function scope** (not block scope), and it's **hoisted** to the top of its containing function.

```javascript
function example() {
  console.log(x); // undefined — NOT an error! (hoisting)
  var x = 5;
  console.log(x); // 5
}

// var leaks out of blocks (if, for, while)
if (true) {
  var leaked = "I escape the block!";
}
console.log(leaked); // "I escape the block!" — this is usually a bug
```

**Hoisting with `var`**: The declaration `var x` is moved to the top of the function during the compilation phase. The assignment `x = 5` stays in place. So the variable exists but is `undefined` before the assignment.

### `let` — Block-Scoped, Reassignable

```javascript
let counter = 0;
counter = 1;    // OK — reassignment allowed
counter = 2;    // OK

if (true) {
  let blockVar = "only here";
  console.log(blockVar); // "only here"
}
console.log(blockVar); // ReferenceError — blockVar is not defined outside the block

// let is also hoisted but NOT initialized (temporal dead zone)
console.log(y); // ReferenceError — cannot access 'y' before initialization
let y = 10;
```

**Temporal Dead Zone (TDZ)**: `let` and `const` are hoisted but not initialized. Accessing them before declaration throws a `ReferenceError`. This is actually a feature — it prevents the confusing behavior of `var`.

### `const` — Block-Scoped, Not Reassignable

```javascript
const MAX_SIZE = 100;
MAX_SIZE = 200; // TypeError: Assignment to constant variable

// IMPORTANT: const does NOT make objects immutable
const user = { name: "Alice" };
user.name = "Bob"; // This IS allowed — you're mutating the object
user = {};         // This is NOT allowed — you're reassigning the variable

// Same with arrays
const arr = [1, 2, 3];
arr.push(4);       // Allowed — mutating the array
arr = [];          // Not allowed — reassignment
```

**Mental model**: `const` means "this variable always points to the same value/reference." It doesn't freeze the value itself.

### When to use which?

```
const  — default choice for everything
let    — when you need to reassign (loop counters, state variables)
var    — never (in modern code)
```

### How Variables Are Stored in Memory

JavaScript stores values in two places:

**Stack** — stores primitive values directly (small, fixed-size)
**Heap** — stores objects/arrays/functions (dynamic size, accessed via reference)

```javascript
// Primitives are copied by VALUE
let a = 5;
let b = a;  // b gets a copy of the value 5
b = 10;
console.log(a); // 5 — a is unchanged

// Objects are copied by REFERENCE
let obj1 = { x: 1 };
let obj2 = obj1;  // obj2 gets a reference to the SAME object
obj2.x = 99;
console.log(obj1.x); // 99 — obj1 was changed!
```

```
Stack:
  a → [5]
  b → [10]

Heap:
  obj1 → points to → { x: 99 }
  obj2 → points to → { x: 99 }  (same object!)
```

---

## 4. Data Types in Depth

JavaScript has **8 data types**: 7 primitives + 1 object type.

### Primitives (Stored by Value)

#### 1. `number`

JavaScript uses **64-bit IEEE 754 floating-point** for ALL numbers (no separate int type).

```javascript
let integer = 42;
let float = 3.14;
let negative = -10;
let scientific = 1.5e6;    // 1,500,000
let hex = 0xFF;            // 255
let octal = 0o17;          // 15
let binary = 0b1010;       // 10

// Special values
let inf = Infinity;
let negInf = -Infinity;
let notANumber = NaN;      // "Not a Number" — result of invalid math

// NaN is weird — it's not equal to itself!
console.log(NaN === NaN);  // false
console.log(isNaN(NaN));   // true
console.log(Number.isNaN(NaN)); // true (better — doesn't coerce types)

// Floating point gotcha
console.log(0.1 + 0.2);   // 0.30000000000000004 — NOT 0.3!
// This is a fundamental limitation of IEEE 754 floating-point arithmetic
// Solution: use toFixed, multiply by 100, or use a library like decimal.js
console.log((0.1 + 0.2).toFixed(1)); // "0.3" (string)

// Safe integer range
console.log(Number.MAX_SAFE_INTEGER); // 9007199254740991 (2^53 - 1)
console.log(Number.MIN_SAFE_INTEGER); // -9007199254740991
// Beyond this range, integers can't be represented exactly
```

#### `BigInt` — For Very Large Integers

```javascript
const huge = 9007199254740991n; // n suffix makes it BigInt
const also = BigInt("9007199254740991");

console.log(huge + 1n); // 9007199254740992n — precise!
// Cannot mix BigInt and Number in operations
console.log(huge + 1); // TypeError
console.log(Number(huge) + 1); // OK but may lose precision
```

#### 2. `string`

Strings are **immutable sequences of UTF-16 code units**.

```javascript
let single = 'Hello';
let double = "World";
let backtick = `Template literal`;

// Immutability — you can't change a character in place
let str = "hello";
str[0] = "H";    // Silently fails in non-strict mode
console.log(str); // "hello" — unchanged

// String concatenation
let a = "Hello" + " " + "World";  // "Hello World"
let b = "Number: " + 42;          // "Number: 42" (42 is coerced to string)

// Template literals (backtick strings)
let name = "Alice";
let age = 30;
let greeting = `Hello, ${name}! You are ${age} years old.`;
// Multi-line strings
let multiLine = `
  Line 1
  Line 2
  Line 3
`;
// Expressions inside ${}
let result = `${2 + 2} is four`;
let upper = `${name.toUpperCase()} is shouting`;
// Tagged templates (advanced)
function tag(strings, ...values) {
  return strings.raw[0]; // raw string (no escape processing)
}
let raw = tag`Hello\nWorld`; // "Hello\nWorld" — the \n is NOT processed

// Useful string methods
let s = "  Hello, World!  ";
console.log(s.length);              // 17
console.log(s.trim());              // "Hello, World!"
console.log(s.trimStart());         // "Hello, World!  "
console.log(s.trimEnd());           // "  Hello, World!"
console.log(s.toUpperCase());       // "  HELLO, WORLD!  "
console.log(s.toLowerCase());       // "  hello, world!  "
console.log(s.includes("World"));   // true
console.log(s.startsWith("  Hel")); // true
console.log(s.endsWith("!  "));     // true
console.log(s.indexOf("o"));        // 4
console.log(s.lastIndexOf("o"));    // 9
console.log(s.slice(2, 7));         // "Hello"
console.log(s.slice(-3));           // "  " (from end)
console.log(s.split(", "));         // ["  Hello", "World!  "]
console.log(s.replace("World", "JS")); // "  Hello, JS!  "
console.log(s.replaceAll("l", "L")); // "  HeLLo, WorLd!  "
console.log("5".padStart(3, "0"));  // "005"
console.log("5".padEnd(3, "0"));    // "500"
console.log("ha".repeat(3));        // "hahaha"
console.log(s.charAt(2));           // "H"
console.log(s.charCodeAt(2));       // 72 (ASCII code of "H")
console.log(String.fromCharCode(72)); // "H"

// String to array
console.log([..."hello"]); // ["h","e","l","l","o"] — spread into chars
```

#### 3. `boolean`

```javascript
let isActive = true;
let isDeleted = false;

// Truthy and Falsy values — CRITICAL to understand
// Falsy values (evaluate to false in boolean context):
false
0
-0
0n          // BigInt zero
""          // empty string
null
undefined
NaN

// Everything else is truthy, including:
"0"         // non-empty string
[]          // empty array
{}          // empty object
-1          // negative number
Infinity
```

```javascript
// Boolean coercion
console.log(Boolean(0));   // false
console.log(Boolean(""));  // false
console.log(Boolean(null)); // false
console.log(Boolean([]));  // true — empty array IS truthy!
console.log(Boolean({}));  // true — empty object IS truthy!
console.log(!!value);      // Double negation — quick coercion to boolean
```

#### 4. `null`

Represents the **intentional absence** of a value. It's a value you set deliberately.

```javascript
let user = null; // "there is no user" (intentional)
console.log(typeof null); // "object" — this is a historical bug in JavaScript!
```

#### 5. `undefined`

Represents a variable that has been declared but not assigned a value. It's also the default return value of functions.

```javascript
let x;
console.log(x);            // undefined
console.log(typeof x);     // "undefined"

function doNothing() {}
console.log(doNothing());  // undefined

let obj = {};
console.log(obj.missing);  // undefined (accessing non-existent property)
```

**null vs undefined:**
```javascript
// null — you explicitly set it to "no value"
// undefined — JavaScript set it to "no value" (variable not initialized, missing property, etc.)

// Both are falsy
if (!null) console.log("null is falsy");      // prints
if (!undefined) console.log("undef is falsy"); // prints

// Loose equality — null and undefined are equal to each other and nothing else
console.log(null == undefined);  // true
console.log(null == false);      // false (!)
console.log(null == 0);          // false (!)
console.log(null === undefined); // false (strict)
```

#### 6. `symbol`

Symbols are **unique and immutable** identifiers. Two symbols are never equal, even if they have the same description.

```javascript
let sym1 = Symbol("id");
let sym2 = Symbol("id");
console.log(sym1 === sym2); // false — always unique

// Use as object keys that can't accidentally clash
const ID = Symbol("id");
const obj = {
  [ID]: 123,
  name: "Alice"
};
console.log(obj[ID]); // 123
// Symbols are not shown in for...in or Object.keys()
console.log(Object.keys(obj)); // ["name"] — ID is hidden
```

We'll cover Symbols more in the dedicated section.

#### 7. `bigint`

Already covered above.

### Object Type (Everything Else)

Objects, Arrays, Functions, Dates, RegExp, Map, Set — all are objects.

```javascript
typeof {}           // "object"
typeof []           // "object"
typeof null         // "object" (bug!)
typeof function(){} // "function" (special case)
typeof new Date()   // "object"
typeof /regex/      // "object"
```

### Type Checking

```javascript
// typeof — works for primitives
typeof 42          // "number"
typeof "hello"     // "string"
typeof true        // "boolean"
typeof undefined   // "undefined"
typeof Symbol()    // "symbol"
typeof 42n         // "bigint"
typeof {}          // "object"
typeof []          // "object" (not "array"!)
typeof null        // "object" (bug!)
typeof function(){} // "function"

// instanceof — for objects/classes
[] instanceof Array      // true
{} instanceof Object     // true
new Date() instanceof Date // true

// Array.isArray — reliable array check
Array.isArray([])        // true
Array.isArray({})        // false

// Object.prototype.toString — most reliable
Object.prototype.toString.call([]);    // "[object Array]"
Object.prototype.toString.call(null);  // "[object Null]"
Object.prototype.toString.call({});    // "[object Object]"
```

### Type Coercion — The Tricky Part

JavaScript automatically converts types in many situations. Understanding this prevents bugs.

```javascript
// Implicit coercion examples
console.log(1 + "2");      // "12" — number coerced to string
console.log("3" - 1);      // 2 — string coerced to number
console.log(true + 1);     // 2 — true is 1
console.log(false + 1);    // 1 — false is 0
console.log(null + 1);     // 1 — null is 0
console.log(undefined + 1); // NaN — undefined becomes NaN
console.log("5" * 2);      // 10 — "*" only works on numbers
console.log(+"5");          // 5 — unary + converts to number
console.log(+true);         // 1
console.log(+false);        // 0
console.log(+null);         // 0
console.log(+undefined);    // NaN
console.log(+"");           // 0
console.log(+"hello");      // NaN

// Explicit conversion
Number("42");       // 42
Number("");         // 0
Number("hello");    // NaN
Number(true);       // 1
Number(false);      // 0
Number(null);       // 0
Number(undefined);  // NaN

String(42);         // "42"
String(true);       // "true"
String(null);       // "null"
String(undefined);  // "undefined"

Boolean(0);         // false
Boolean("");        // false
Boolean("0");       // true (!)
Boolean([]);        // true (!)
```

### Loose vs Strict Equality

```javascript
// == (loose equality) — coerces types before comparing
console.log(0 == false);   // true
console.log("" == false);  // true
console.log(null == undefined); // true
console.log(1 == "1");     // true

// === (strict equality) — NO type coercion
console.log(0 === false);  // false
console.log("1" === 1);    // false
console.log(null === undefined); // false

// ALWAYS use === unless you specifically want coercion
```

---

## 5. Operators

### Arithmetic Operators

```javascript
let a = 10, b = 3;
console.log(a + b);   // 13 — addition
console.log(a - b);   // 7  — subtraction
console.log(a * b);   // 30 — multiplication
console.log(a / b);   // 3.333... — division
console.log(a % b);   // 1  — modulo (remainder)
console.log(a ** b);  // 1000 — exponentiation (10^3)

// Increment / Decrement
let x = 5;
console.log(x++); // 5 — returns THEN increments
console.log(x);   // 6
console.log(++x); // 7 — increments THEN returns
console.log(x--); // 7 — returns THEN decrements
console.log(x);   // 6
console.log(--x); // 5 — decrements THEN returns
```

### Assignment Operators

```javascript
let x = 10;
x += 5;   // x = x + 5  = 15
x -= 3;   // x = x - 3  = 12
x *= 2;   // x = x * 2  = 24
x /= 4;   // x = x / 4  = 6
x %= 4;   // x = x % 4  = 2
x **= 3;  // x = x ** 3 = 8

// Logical assignment (ES2021)
let a = null;
a ??= "default";   // a = a ?? "default" → "default" (only if null/undefined)
let b = 0;
b ||= 42;           // b = b || 42 → 42 (if b is falsy)
let c = 5;
c &&= c * 2;        // c = c && c*2 → 10 (if c is truthy)
```

### Comparison Operators

```javascript
console.log(5 > 3);    // true
console.log(5 >= 5);   // true
console.log(3 < 5);    // true
console.log(3 <= 2);   // false
console.log(5 == "5"); // true (loose)
console.log(5 === "5"); // false (strict)
console.log(5 != "5"); // false (loose)
console.log(5 !== "5"); // true (strict)
```

### Logical Operators

```javascript
// AND — returns first falsy value, or last value if all truthy
console.log(true && true);   // true
console.log(true && false);  // false
console.log(1 && 2 && 3);    // 3 — all truthy, returns last
console.log(1 && 0 && 3);    // 0 — first falsy
console.log(0 && anything);  // 0 — short-circuits

// OR — returns first truthy value, or last value if all falsy
console.log(false || true);  // true
console.log(0 || "hello");   // "hello" — first truthy
console.log(0 || "" || null);// null — all falsy, returns last
console.log(null || undefined || "default"); // "default"

// NOT
console.log(!true);  // false
console.log(!0);     // true
console.log(!"");    // true
console.log(!!"hi"); // true — double negation to boolean

// Nullish Coalescing (??) — only checks null/undefined (not all falsy)
console.log(null ?? "default");     // "default"
console.log(undefined ?? "default");// "default"
console.log(0 ?? "default");        // 0 — 0 is NOT null/undefined!
console.log("" ?? "default");       // "" — "" is NOT null/undefined!
// Very useful for default values where 0 or "" are valid
let count = userCount ?? 0; // use 0 if userCount is null/undefined
```

### Optional Chaining (?.)

Safely access nested properties without crashing if a middle value is null/undefined.

```javascript
let user = null;

// Without optional chaining — crashes!
// console.log(user.profile.name); // TypeError: Cannot read properties of null

// With optional chaining — returns undefined safely
console.log(user?.profile?.name); // undefined — no crash!

// Works with method calls too
let arr = null;
console.log(arr?.map(x => x * 2)); // undefined — no crash

// And bracket notation
let key = "name";
console.log(user?.[key]); // undefined

// Common pattern: optional chaining + nullish coalescing
let displayName = user?.profile?.name ?? "Anonymous";
```

### Bitwise Operators

```javascript
// Work on 32-bit integers
let a = 5;  // binary: 0101
let b = 3;  // binary: 0011

console.log(a & b);  // 1    — AND (0001)
console.log(a | b);  // 7    — OR  (0111)
console.log(a ^ b);  // 6    — XOR (0110) — 1 where bits differ
console.log(~a);     // -6   — NOT (flips all bits + two's complement)
console.log(a << 1); // 10   — left shift (0101 → 1010 = 10)
console.log(a >> 1); // 2    — right shift (0101 → 0010 = 2)
console.log(a >>> 1);// 2    — unsigned right shift

// Practical uses:
// Fast integer truncation (equivalent to Math.floor for positives)
console.log(4.7 | 0);  // 4 — truncates decimal
console.log(~~4.7);     // 4 — same effect

// Check even/odd
console.log(4 & 1); // 0 — even
console.log(5 & 1); // 1 — odd
```

### Ternary Operator

```javascript
// condition ? valueIfTrue : valueIfFalse
let age = 20;
let category = age >= 18 ? "adult" : "minor"; // "adult"

// Can be nested (but becomes hard to read quickly)
let score = 75;
let grade = score >= 90 ? "A"
          : score >= 80 ? "B"
          : score >= 70 ? "C"
          : "F";
// grade = "C"
```

### `typeof` and `instanceof`

```javascript
typeof 42          // "number"
typeof "hi"        // "string"
typeof true        // "boolean"
typeof undefined   // "undefined"
typeof null        // "object" (bug!)
typeof {}          // "object"
typeof []          // "object"
typeof function(){} // "function"

[] instanceof Array   // true
{} instanceof Object  // true

// instanceof checks the prototype chain
class Animal {}
class Dog extends Animal {}
let d = new Dog();
console.log(d instanceof Dog);    // true
console.log(d instanceof Animal); // true — inheritance chain!
```

---

## 6. Control Flow

### `if / else if / else`

```javascript
let temperature = 25;

if (temperature > 30) {
  console.log("Hot");
} else if (temperature > 20) {
  console.log("Warm"); // This runs
} else if (temperature > 10) {
  console.log("Cool");
} else {
  console.log("Cold");
}

// Without braces (only for single statements — generally avoid)
if (temperature > 20) console.log("Warm");

// Short-circuit for simple cases
temperature > 20 && console.log("Warm");  // same as above
```

### `switch`

```javascript
let day = "Monday";

switch (day) {
  case "Monday":
  case "Tuesday":
  case "Wednesday":
  case "Thursday":
  case "Friday":
    console.log("Weekday");
    break; // MUST break, otherwise falls through to next case
  case "Saturday":
  case "Sunday":
    console.log("Weekend");
    break;
  default:
    console.log("Invalid day");
}

// switch uses strict equality (===)
let x = "1";
switch (x) {
  case 1:
    console.log("number 1"); // NOT executed (string "1" !== number 1)
    break;
  case "1":
    console.log("string 1"); // Executed
    break;
}

// Fall-through (intentional, no break)
let val = 1;
switch (val) {
  case 1:
    console.log("one");
    // falls through
  case 2:
    console.log("one or two"); // also runs when val is 1!
    break;
}
// Output: "one" then "one or two"
```

### `for` Loop

```javascript
// Classic for loop
for (let i = 0; i < 5; i++) {
  console.log(i); // 0, 1, 2, 3, 4
}

// Reverse loop
for (let i = 4; i >= 0; i--) {
  console.log(i); // 4, 3, 2, 1, 0
}

// Nested loops
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    console.log(`${i},${j}`);
  }
}

// break — exit loop immediately
for (let i = 0; i < 10; i++) {
  if (i === 5) break;
  console.log(i); // 0, 1, 2, 3, 4
}

// continue — skip current iteration
for (let i = 0; i < 10; i++) {
  if (i % 2 === 0) continue;
  console.log(i); // 1, 3, 5, 7, 9
}

// Labeled statements (for nested loops)
outer: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) break outer; // breaks the OUTER loop
    console.log(`${i},${j}`);
  }
}
// Only logs "0,0"
```

### `while` Loop

```javascript
let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}

// do...while — executes body at least once
let count = 0;
do {
  console.log(count); // runs at least once even if condition is false initially
  count++;
} while (count < 3);
// Logs: 0, 1, 2
```

### `for...of` — Iterate Over Iterables

```javascript
// Arrays
let fruits = ["apple", "banana", "cherry"];
for (let fruit of fruits) {
  console.log(fruit);
}

// With index using entries()
for (let [index, fruit] of fruits.entries()) {
  console.log(`${index}: ${fruit}`);
}

// Strings
for (let char of "hello") {
  console.log(char); // h, e, l, l, o
}

// Map
let map = new Map([["a", 1], ["b", 2]]);
for (let [key, value] of map) {
  console.log(`${key}: ${value}`);
}

// Set
let set = new Set([1, 2, 3]);
for (let value of set) {
  console.log(value);
}

// Works with any iterable (has Symbol.iterator)
```

### `for...in` — Iterate Over Object Keys

```javascript
let person = { name: "Alice", age: 30, city: "NYC" };

for (let key in person) {
  console.log(`${key}: ${person[key]}`);
}
// name: Alice
// age: 30
// city: NYC

// IMPORTANT: for...in also iterates inherited properties!
function Animal(name) { this.name = name; }
Animal.prototype.type = "animal";
let dog = new Animal("Rex");

for (let key in dog) {
  console.log(key); // "name" AND "type" — "type" is from prototype!
}

// Filter to own properties only
for (let key in dog) {
  if (dog.hasOwnProperty(key)) {
    console.log(key); // only "name"
  }
}

// Avoid for...in on arrays — use for...of or forEach instead
```

### Exception Handling with `try/catch/finally`

```javascript
try {
  // Code that might throw an error
  let result = JSON.parse("invalid json");
} catch (error) {
  // error is an Error object with .name, .message, .stack
  console.log(error.name);    // "SyntaxError"
  console.log(error.message); // "Unexpected token..."
} finally {
  // Always runs — cleanup code
  console.log("This always runs");
}

// Throwing your own errors
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}

try {
  divide(10, 0);
} catch (e) {
  console.log(e.message); // "Cannot divide by zero"
}

// Different error types
throw new TypeError("Expected a number");
throw new RangeError("Value out of range");
throw new ReferenceError("Variable not defined");
throw new SyntaxError("Invalid syntax");

// You can throw anything (but Error objects are best practice)
throw "error string"; // possible but not recommended
throw 42;             // possible but not recommended
throw { code: 404, message: "Not found" }; // possible but not recommended
```

---

## 7. Functions — Every Detail

Functions are **first-class citizens** in JavaScript — they can be:
- Stored in variables
- Passed as arguments
- Returned from other functions
- Have properties

### Function Declaration

```javascript
// Hoisted — can be called before declaration in the file
greet("Alice"); // Works!

function greet(name) {
  return `Hello, ${name}!`;
}
```

**Hoisting**: Function declarations are fully hoisted — the entire function (name + body) is moved to the top of its scope during compilation.

### Function Expression

```javascript
// NOT hoisted (the variable is hoisted as undefined, not the function)
// sayHi(); // TypeError: sayHi is not a function

const sayHi = function(name) {
  return `Hi, ${name}!`;
};
// The function can optionally have a name (useful for recursion and debugging)
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n - 1); // can refer to itself as "fact"
};
```

### Arrow Functions

Arrow functions are a concise syntax introduced in ES6. They have important differences from regular functions.

```javascript
// Regular function
const add = function(a, b) { return a + b; };

// Arrow function
const add = (a, b) => { return a + b; };

// If body is a single expression, braces and return are implicit
const add = (a, b) => a + b;

// Single parameter — parentheses optional
const double = x => x * 2;

// No parameters — parentheses required
const getRandom = () => Math.random();

// Returning an object literal — wrap in parentheses to avoid ambiguity
const makeUser = (name) => ({ name, active: true }); // () wraps the {}

// Multi-line body — requires braces and explicit return
const complexCalc = (a, b) => {
  const sum = a + b;
  const product = a * b;
  return { sum, product };
};
```

**Key Differences from Regular Functions:**

1. **No `this` binding** — arrow functions capture `this` from the surrounding scope (lexical `this`)
2. **No `arguments` object**
3. **Cannot be used as constructors** (`new arrowFn()` throws TypeError)
4. **No `prototype` property**

```javascript
// this in regular function vs arrow function
const counter = {
  count: 0,
  // Regular function — 'this' depends on how it's called
  incrementRegular: function() {
    setTimeout(function() {
      this.count++; // 'this' is NOT counter — it's global (or undefined in strict mode)
      console.log(this.count); // NaN or error
    }, 100);
  },
  // Arrow function — 'this' is lexically inherited from incrementArrow's this
  incrementArrow: function() {
    setTimeout(() => {
      this.count++; // 'this' IS counter — inherited from surrounding method
      console.log(this.count); // 1
    }, 100);
  }
};
```

### Parameters in Depth

```javascript
// Default parameters
function greet(name = "World", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
greet();              // "Hello, World!"
greet("Alice");       // "Hello, Alice!"
greet("Bob", "Hi");   // "Hi, Bob!"

// Default can be an expression or even a function call
function createUser(name, id = Math.random()) {
  return { name, id };
}

// Rest parameters — collects remaining args into an array
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
sum(1, 2, 3, 4, 5); // 15

// Must be the last parameter
function log(level, ...messages) {
  messages.forEach(msg => console.log(`[${level}] ${msg}`));
}
log("ERROR", "File not found", "Please check path");

// arguments object (old way, only in regular functions)
function oldStyle() {
  console.log(arguments); // array-like object with all args
  console.log(Array.from(arguments)); // convert to real array
}
// Arrow functions do NOT have arguments:
const arrowFn = () => {
  console.log(arguments); // ReferenceError or captures outer scope's arguments
};
```

### The Spread Operator in Function Calls

```javascript
const nums = [1, 2, 3, 4, 5];
console.log(Math.max(...nums)); // 5 — spreads array into individual args

function add(a, b, c) { return a + b + c; }
add(...nums); // add(1, 2, 3) — uses first 3, ignores rest
```

### Higher-Order Functions

Functions that take functions as arguments or return functions.

```javascript
// Taking a function as argument
function applyTwice(fn, value) {
  return fn(fn(value));
}
applyTwice(x => x * 2, 3); // 12 — doubles twice

// Returning a function
function multiplier(factor) {
  return (number) => number * factor; // returns a function!
}
const double = multiplier(2);
const triple = multiplier(3);
double(5);  // 10
triple(5);  // 15

// This pattern is called a "closure" — double "remembers" factor=2
```

### Immediately Invoked Function Expression (IIFE)

```javascript
// Defined and immediately called
(function() {
  let privateVar = "I'm private";
  console.log(privateVar);
})();

// Arrow IIFE
(() => {
  console.log("Arrow IIFE");
})();

// With argument
(function(x) {
  console.log(x * 2);
})(5); // 10

// Used to create private scope (before ES modules)
```

### Recursion

A function that calls itself.

```javascript
// Factorial
function factorial(n) {
  if (n <= 1) return 1;    // base case — prevents infinite recursion
  return n * factorial(n - 1); // recursive case
}
factorial(5); // 120 — 5 * 4 * 3 * 2 * 1

// Fibonacci
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
fibonacci(10); // 55

// Tree traversal
function sumTree(node) {
  if (!node) return 0;
  return node.value + sumTree(node.left) + sumTree(node.right);
}

// Tail call optimization (TCO) — some engines optimize this
function factTCO(n, accumulator = 1) {
  if (n <= 1) return accumulator;
  return factTCO(n - 1, n * accumulator); // tail position — last thing called
}
```

### Memoization

Caching function results to avoid redundant computation.

```javascript
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key); // return cached result
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const memoFib = memoize(function fib(n) {
  if (n <= 1) return n;
  return memoFib(n - 1) + memoFib(n - 2);
});

memoFib(40); // Much faster! Each value computed only once
```

### Function Methods: `call`, `apply`, `bind`

These control what `this` is inside a function.

```javascript
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}

const person = { name: "Alice" };

// call — calls immediately, passes args individually
greet.call(person, "Hello", "!"); // "Hello, Alice!"

// apply — calls immediately, passes args as array
greet.apply(person, ["Hi", "?"]); // "Hi, Alice?"

// bind — returns a NEW function with 'this' bound
const boundGreet = greet.bind(person);
boundGreet("Hey", "."); // "Hey, Alice."

// Partial application with bind
const helloAlice = greet.bind(person, "Hello");
helloAlice("!"); // "Hello, Alice!"
helloAlice("?"); // "Hello, Alice?"
```

---

## 8. Scope, Closures & the Lexical Environment

### Scope

Scope determines where a variable is accessible.

```javascript
// Global scope — accessible everywhere
let globalVar = "I'm global";

function outer() {
  // Function scope
  let outerVar = "I'm in outer";
  
  function inner() {
    // Inner function scope
    let innerVar = "I'm in inner";
    
    // Can access all outer scopes (scope chain lookup)
    console.log(innerVar);  // own scope
    console.log(outerVar);  // parent scope
    console.log(globalVar); // global scope
  }
  
  inner();
  // console.log(innerVar); // ReferenceError — can't access inner scope
}

outer();
```

**Scope Chain**: When JavaScript looks up a variable, it starts in the current scope and works outward until it finds the variable or reaches the global scope.

### The Lexical Environment

Every function has a hidden `[[Environment]]` property that stores a reference to the scope in which it was **defined** (not called). This is the foundation of closures.

```javascript
// Lexical environment in action
let x = 1;

function outer() {
  let x = 2; // shadows global x
  
  function inner() {
    // inner's [[Environment]] points to outer's scope
    console.log(x); // 2 — uses outer's x, not global x
  }
  
  return inner;
}

let fn = outer();
fn(); // 2 — even though outer() has returned!
```

### Closures

A **closure** is a function that "closes over" (remembers) its surrounding scope — even after the outer function has returned.

```javascript
function makeCounter(initialValue = 0) {
  let count = initialValue; // this variable is "enclosed"
  
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount()  { return count; },
    reset()     { count = initialValue; }
  };
}

const counter = makeCounter(10);
counter.increment(); // 11
counter.increment(); // 12
counter.decrement(); // 11
counter.getCount();  // 11

// Each call to makeCounter creates a NEW closure with its own 'count'
const counter2 = makeCounter();
counter2.increment(); // 1 — separate from counter!
counter.getCount();   // 11 — unchanged
```

**Closures enable:**
- Data privacy (variables only accessible through the returned API)
- Stateful functions
- Partial application / currying
- Module pattern

### Classic Closure Gotcha

```javascript
// Problem: all functions share the same 'i'
var functions = [];
for (var i = 0; i < 3; i++) {
  functions.push(function() { console.log(i); });
}
functions[0](); // 3 — not 0!
functions[1](); // 3 — not 1!
functions[2](); // 3 — not 2!
// All three share the SAME 'i' (var is function-scoped)
// By the time they run, the loop is done and i = 3

// Fix 1: use let (block-scoped — each iteration has its own 'i')
var functions2 = [];
for (let i = 0; i < 3; i++) {
  functions2.push(function() { console.log(i); });
}
functions2[0](); // 0
functions2[1](); // 1
functions2[2](); // 2

// Fix 2: IIFE to capture value (old way before let)
var functions3 = [];
for (var i = 0; i < 3; i++) {
  functions3.push((function(captured) {
    return function() { console.log(captured); };
  })(i));
}
```

### Module Pattern (using Closures)

```javascript
const bankAccount = (function() {
  let balance = 0; // private — not accessible from outside
  let transactionHistory = []; // private
  
  return {
    deposit(amount) {
      if (amount <= 0) throw new Error("Amount must be positive");
      balance += amount;
      transactionHistory.push({ type: "deposit", amount, balance });
      return balance;
    },
    withdraw(amount) {
      if (amount > balance) throw new Error("Insufficient funds");
      balance -= amount;
      transactionHistory.push({ type: "withdrawal", amount, balance });
      return balance;
    },
    getBalance() { return balance; },
    getHistory() { return [...transactionHistory]; } // returns copy, not original
  };
})();

bankAccount.deposit(100);   // 100
bankAccount.withdraw(30);   // 70
bankAccount.getBalance();   // 70
// balance — not accessible directly!
```

---

## 9. The `this` Keyword

`this` is one of JavaScript's most confusing topics. The value of `this` depends entirely on **how a function is called**, not where it's defined (except for arrow functions).

### Rule 1: Default Binding (Standalone Function Call)

```javascript
function showThis() {
  console.log(this);
}
showThis(); // In browser: window (global object)
            // In strict mode: undefined

"use strict";
function showThisStrict() {
  console.log(this); // undefined
}
showThisStrict();
```

### Rule 2: Implicit Binding (Method Call)

```javascript
const person = {
  name: "Alice",
  greet() {
    console.log(this.name); // 'this' is the object before the dot
  }
};
person.greet(); // "Alice" — this = person

// Careful: extracting the method loses the binding
const greetFn = person.greet;
greetFn(); // undefined — this is global/undefined (lost binding!)
```

### Rule 3: Explicit Binding (`call`, `apply`, `bind`)

```javascript
function greet(greeting) {
  console.log(`${greeting}, ${this.name}!`);
}
const user = { name: "Bob" };
greet.call(user, "Hello");  // "Hello, Bob!" — this = user
greet.apply(user, ["Hi"]);  // "Hi, Bob!" — this = user
const boundGreet = greet.bind(user);
boundGreet("Hey");          // "Hey, Bob!" — this = user (always)
```

### Rule 4: `new` Binding

```javascript
function Person(name) {
  // When called with 'new':
  // 1. A new empty object is created
  // 2. 'this' points to that new object
  // 3. The function body runs (sets properties on this)
  // 4. The object is returned (implicitly)
  this.name = name;
  this.greet = function() {
    console.log(`Hello, I'm ${this.name}`);
  };
}

const alice = new Person("Alice"); // 'this' inside = the new alice object
alice.greet(); // "Hello, I'm Alice"
```

### Rule 5: Arrow Function (Lexical `this`)

Arrow functions do NOT have their own `this`. They inherit `this` from the surrounding scope where they are **defined**.

```javascript
const timer = {
  seconds: 0,
  start() {
    // 'this' here is the timer object (method call rule)
    setInterval(() => {
      // Arrow function: 'this' inherited from start()'s 'this'
      this.seconds++; // 'this' is still the timer object!
      console.log(this.seconds);
    }, 1000);
  }
};
timer.start(); // correctly logs 1, 2, 3...
```

### Rule Priority

When multiple rules apply, priority is:
```
new > explicit (call/apply/bind) > implicit (method) > default
```

### `this` in Classes

```javascript
class Counter {
  constructor() {
    this.count = 0;
    // Bind method to instance (one way to handle event listeners etc.)
    this.increment = this.increment.bind(this);
  }
  
  increment() {
    this.count++;
  }
  
  // Class field method — arrow function, so 'this' is always the instance
  decrement = () => {
    this.count--;
  };
}
```

---

## 10. Prototypes & Prototype Chain

Every JavaScript object has a hidden `[[Prototype]]` property that links to another object. This is the foundation of inheritance in JavaScript.

### The Prototype Chain

```javascript
// When you access a property on an object, JavaScript:
// 1. Looks at the object itself
// 2. If not found, looks at its [[Prototype]]
// 3. Continues up the chain until it finds it or reaches null

const animal = {
  breathe() { return "breathing"; }
};

const dog = {
  bark() { return "woof"; }
};

// Set dog's prototype to animal
Object.setPrototypeOf(dog, animal);
// Or: dog.__proto__ = animal; (older syntax, avoid in production)

dog.bark();    // "woof" — own property
dog.breathe(); // "breathing" — inherited from animal's prototype

// The chain: dog → animal → Object.prototype → null
```

### Constructor Functions & Prototype

```javascript
function Animal(name) {
  this.name = name; // own property
}

// Methods on prototype are SHARED across all instances
Animal.prototype.speak = function() {
  return `${this.name} makes a sound.`;
};

Animal.prototype.breathe = function() {
  return `${this.name} breathes.`;
};

const cat = new Animal("Cat");
const dog = new Animal("Dog");

cat.speak();   // "Cat makes a sound."
dog.speak();   // "Dog makes a sound."

// Both instances share the same speak function
console.log(cat.speak === dog.speak); // true — same function reference

// Checking prototype
console.log(cat.__proto__ === Animal.prototype); // true
console.log(Object.getPrototypeOf(cat) === Animal.prototype); // true (preferred)
console.log(cat instanceof Animal); // true
```

### Prototype Chain Lookup Diagram

```
cat instance
  ├── name: "Cat"
  └── [[Prototype]] → Animal.prototype
                        ├── speak: function
                        ├── breathe: function
                        └── [[Prototype]] → Object.prototype
                                              ├── toString: function
                                              ├── hasOwnProperty: function
                                              └── [[Prototype]] → null
```

### `Object.create()`

Creates an object with a specified prototype.

```javascript
const vehiclePrototype = {
  start() { return `${this.brand} is starting`; },
  stop() { return `${this.brand} stopped`; }
};

// Create car with vehiclePrototype as its prototype
const car = Object.create(vehiclePrototype);
car.brand = "Toyota";
car.start(); // "Toyota is starting"

// Creating truly empty objects (no prototype)
const pure = Object.create(null);
// pure has NO inherited methods — no toString, no hasOwnProperty, etc.
// Useful for pure hash maps
```

### Prototype-based Inheritance

```javascript
function Animal(name) {
  this.name = name;
}
Animal.prototype.speak = function() {
  return `${this.name} makes a sound.`;
};

function Dog(name, breed) {
  Animal.call(this, name); // Call parent constructor (sets this.name)
  this.breed = breed;
}

// Set up inheritance: Dog.prototype inherits from Animal.prototype
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog; // Fix the constructor reference

// Override speak
Dog.prototype.speak = function() {
  return `${this.name} barks.`;
};

// Add new methods
Dog.prototype.fetch = function() {
  return `${this.name} fetches!`;
};

const rex = new Dog("Rex", "German Shepherd");
rex.speak();   // "Rex barks." — overridden
rex.fetch();   // "Rex fetches!" — Dog-specific
rex instanceof Dog;    // true
rex instanceof Animal; // true — inherits from Animal
```

### Property Descriptor & Attributes

```javascript
const obj = { x: 42 };

// Get the property descriptor
Object.getOwnPropertyDescriptor(obj, "x");
// {
//   value: 42,
//   writable: true,    — can change the value?
//   enumerable: true,  — shows in for...in and Object.keys?
//   configurable: true — can delete or reconfigure?
// }

// Define a property with custom attributes
Object.defineProperty(obj, "constant", {
  value: 100,
  writable: false,     // can't change
  enumerable: true,    // shows up in loops
  configurable: false  // can't delete or redefine
});

obj.constant = 200; // silently fails (or throws in strict mode)
console.log(obj.constant); // 100

// Non-enumerable property (hidden from loops)
Object.defineProperty(obj, "secret", {
  value: "hidden",
  enumerable: false
});
for (let key in obj) console.log(key); // "x", "constant" — not "secret"
Object.keys(obj); // ["x", "constant"] — not "secret"
console.log(obj.secret); // "hidden" — still accessible directly

// Getters and Setters via defineProperty
let _age = 0;
Object.defineProperty(obj, "age", {
  get() { return _age; },
  set(value) {
    if (value < 0) throw new Error("Age cannot be negative");
    _age = value;
  },
  enumerable: true,
  configurable: true
});
obj.age = 25;  // calls setter
obj.age;       // calls getter — 25
```

### Sealing and Freezing Objects

```javascript
// Object.seal() — no new properties, can't delete, CAN modify existing values
const sealed = Object.seal({ x: 1, y: 2 });
sealed.x = 99;     // OK — modifying existing property
sealed.z = 3;      // Silently fails (or throws in strict mode)
delete sealed.x;   // Silently fails
console.log(sealed); // { x: 99, y: 2 }

// Object.freeze() — no new properties, no deletion, CANNOT modify existing
const frozen = Object.freeze({ x: 1, y: { z: 2 } });
frozen.x = 99;     // Silently fails
frozen.w = 4;      // Silently fails
frozen.y.z = 99;   // THIS WORKS — freeze is SHALLOW!
// For deep freeze, you'd need a recursive function

function deepFreeze(obj) {
  Object.getOwnPropertyNames(obj).forEach(name => {
    const value = obj[name];
    if (typeof value === "object" && value !== null) {
      deepFreeze(value);
    }
  });
  return Object.freeze(obj);
}
```

---

## 11. Classes

ES6 classes are **syntactic sugar** over prototype-based inheritance — they don't introduce a new object model.

### Basic Class

```javascript
class Animal {
  // Constructor — called when you do 'new Animal()'
  constructor(name, sound) {
    this.name = name;   // instance property
    this.sound = sound;
  }
  
  // Prototype method — shared by all instances
  speak() {
    return `${this.name} says ${this.sound}`;
  }
  
  // Getter
  get info() {
    return `Name: ${this.name}`;
  }
  
  // Setter
  set rename(newName) {
    if (typeof newName !== "string") throw new TypeError("Name must be a string");
    this.name = newName;
  }
  
  // Static method — called on the class, not on instances
  static create(name, sound) {
    return new Animal(name, sound);
  }
  
  // toString override
  toString() {
    return `Animal(${this.name})`;
  }
}

const cat = new Animal("Cat", "meow");
cat.speak();  // "Cat says meow"
cat.info;     // "Name: Cat" (getter)
cat.rename = "Kitty"; // (setter)
Animal.create("Dog", "woof"); // static method

// Private fields (ES2022) — truly private, not accessible from outside
class BankAccount {
  #balance = 0; // private field — # prefix
  #transactionLog = []; // private field
  
  constructor(initialBalance) {
    this.#balance = initialBalance;
  }
  
  deposit(amount) {
    this.#balance += amount;
    this.#transactionLog.push(`Deposit: ${amount}`);
  }
  
  get balance() { return this.#balance; } // public getter for private field
}

const account = new BankAccount(100);
account.deposit(50);
account.balance;   // 150
account.#balance;  // SyntaxError — truly private!
```

### Inheritance with `extends`

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  
  speak() {
    return `${this.name} makes a noise.`;
  }
  
  toString() {
    return `[Animal: ${this.name}]`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name); // MUST call super() before using 'this'
    this.breed = breed;
  }
  
  // Override parent method
  speak() {
    const parentSpeak = super.speak(); // call parent's version
    return `${this.name} barks. (${parentSpeak})`;
  }
  
  // New method
  fetch(item) {
    return `${this.name} fetches the ${item}!`;
  }
}

const dog = new Dog("Rex", "Labrador");
dog.speak();        // "Rex barks. (Rex makes a noise.)"
dog.fetch("ball");  // "Rex fetches the ball!"
dog instanceof Dog;    // true
dog instanceof Animal; // true — inheritance chain
```

### Class Fields (Modern Syntax)

```javascript
class Counter {
  // Public instance fields — initialized for each instance
  count = 0;
  label = "Counter";
  
  // Private instance fields
  #history = [];
  
  // Static fields
  static instances = 0;
  static #maxInstances = 100;
  
  // Static private field
  static #instanceCount = 0;
  
  constructor(label) {
    this.label = label;
    Counter.instances++;
    Counter.#instanceCount++;
  }
  
  // Public method using arrow (bound to instance)
  increment = () => {
    this.count++;
    this.#history.push(this.count);
  };
  
  // Regular prototype method
  getHistory() {
    return [...this.#history];
  }
  
  static getInstanceCount() {
    return Counter.#instanceCount;
  }
}
```

### Mixins — Composing Behavior

JavaScript doesn't support multiple inheritance, but mixins can simulate it.

```javascript
const Serializable = (Base) => class extends Base {
  serialize() {
    return JSON.stringify(this);
  }
  
  static deserialize(json) {
    return Object.assign(new this(), JSON.parse(json));
  }
};

const Validatable = (Base) => class extends Base {
  validate() {
    return Object.entries(this).every(([key, value]) => value !== null);
  }
};

class User extends Serializable(Validatable(class {})) {
  constructor(name, email) {
    super();
    this.name = name;
    this.email = email;
  }
}

const user = new User("Alice", "alice@example.com");
user.serialize();  // JSON string
user.validate();   // true
```

---

## 12. Arrays — Complete Guide

Arrays in JavaScript are dynamic, ordered lists that can hold any type of value.

### Creating Arrays

```javascript
// Literal (most common)
const arr1 = [1, 2, 3];
const mixed = [1, "two", true, null, { a: 1 }, [1, 2]];

// Array constructor
const arr2 = new Array(3);        // [undefined × 3] — empty holes!
const arr3 = new Array(1, 2, 3);  // [1, 2, 3]
const arr4 = Array.of(3);         // [3] — avoids the length ambiguity
const arr5 = Array.from("hello"); // ["h", "e", "l", "l", "o"]
const arr6 = Array.from({length: 5}, (_, i) => i); // [0, 1, 2, 3, 4]
const arr7 = Array.from(new Set([1, 2, 2, 3])); // [1, 2, 3]
```

### Basic Operations

```javascript
let arr = [1, 2, 3, 4, 5];

// Accessing elements
arr[0];          // 1 — zero-indexed
arr[arr.length - 1]; // 5 — last element
arr.at(-1);      // 5 — at() with negative index (ES2022)
arr.at(-2);      // 4

// Length
arr.length;      // 5
arr.length = 3;  // Truncates! arr is now [1, 2, 3]

// Adding elements
arr.push(4);          // [1, 2, 3, 4] — adds to end, returns new length
arr.unshift(0);       // [0, 1, 2, 3, 4] — adds to beginning, returns new length

// Removing elements
arr.pop();            // removes and returns last element
arr.shift();          // removes and returns first element

// Finding elements
arr.indexOf(2);        // 1 — index of first occurrence (or -1 if not found)
arr.lastIndexOf(2);    // last occurrence
arr.includes(2);       // true
arr.find(x => x > 2);          // 3 — first element matching predicate
arr.findIndex(x => x > 2);     // 2 — index of first match
arr.findLast(x => x < 4);      // 3 — last match (ES2023)
arr.findLastIndex(x => x < 4); // 2 — last match index
```

### `splice` and `slice`

```javascript
let arr = [1, 2, 3, 4, 5];

// slice(start, end) — returns new array, does NOT modify original
arr.slice(1, 3);  // [2, 3] — elements at index 1 and 2 (end is exclusive)
arr.slice(2);     // [3, 4, 5] — from index 2 to end
arr.slice(-2);    // [4, 5] — last 2 elements
arr.slice();      // [1, 2, 3, 4, 5] — copy of array

// splice(start, deleteCount, ...itemsToInsert) — MODIFIES original
let removed = arr.splice(1, 2);      // removes 2 elements starting at index 1
// arr is now [1, 4, 5], removed is [2, 3]

arr.splice(1, 0, 2, 3);             // insert at index 1, delete 0 elements
// arr is now [1, 2, 3, 4, 5]

arr.splice(1, 2, "a", "b", "c");   // replace 2 elements with 3
// arr is now [1, "a", "b", "c", 4, 5]
```

### Transformation Methods (All Return New Arrays)

```javascript
const numbers = [1, 2, 3, 4, 5];

// map — transform each element
numbers.map(x => x * 2);           // [2, 4, 6, 8, 10]
numbers.map((x, i) => `${i}:${x}`); // ["0:1", "1:2", ...]

// filter — keep elements matching predicate
numbers.filter(x => x % 2 === 0);  // [2, 4]
numbers.filter(x => x > 3);        // [4, 5]

// reduce — accumulate into single value
numbers.reduce((acc, x) => acc + x, 0);   // 15 — sum
numbers.reduce((acc, x) => acc * x, 1);   // 120 — product
// Building an object from an array
["a", "b", "c"].reduce((acc, val, i) => {
  acc[val] = i;
  return acc;
}, {}); // { a: 0, b: 1, c: 2 }

// reduceRight — reduce from right to left
["a", "b", "c"].reduceRight((acc, x) => acc + x, ""); // "cba"

// flat — flatten nested arrays
[1, [2, 3], [4, [5, 6]]].flat();     // [1, 2, 3, 4, [5, 6]] — depth 1
[1, [2, 3], [4, [5, 6]]].flat(2);    // [1, 2, 3, 4, 5, 6] — depth 2
[1, [2, [3, [4]]]].flat(Infinity);   // [1, 2, 3, 4] — fully flatten

// flatMap — map then flat (depth 1)
[1, 2, 3].flatMap(x => [x, x * 2]); // [1, 2, 2, 4, 3, 6]
// More useful:
["hello world", "foo bar"].flatMap(s => s.split(" ")); // ["hello", "world", "foo", "bar"]
```

### Sorting

```javascript
// sort() — MODIFIES original array
// Default: converts to strings and sorts lexicographically!
[10, 9, 2, 1, 100].sort();           // [1, 10, 100, 2, 9] — wrong for numbers!
["banana", "apple", "cherry"].sort(); // ["apple", "banana", "cherry"] — correct for strings

// Numeric sort — provide comparison function
[10, 9, 2, 1, 100].sort((a, b) => a - b);  // [1, 2, 9, 10, 100] — ascending
[10, 9, 2, 1, 100].sort((a, b) => b - a);  // [100, 10, 9, 2, 1] — descending

// Sorting objects
const people = [
  { name: "Charlie", age: 30 },
  { name: "Alice", age: 25 },
  { name: "Bob", age: 35 }
];
people.sort((a, b) => a.age - b.age);  // by age ascending
people.sort((a, b) => a.name.localeCompare(b.name)); // by name

// Stable sort: Since ES2019, sort() is guaranteed to be stable
// (equal elements maintain their original relative order)

// toSorted() — returns new sorted array (ES2023, non-mutating)
const sorted = [3, 1, 2].toSorted((a, b) => a - b); // [1, 2, 3]
```

### Searching & Testing

```javascript
const arr = [1, 2, 3, 4, 5];

// every — are ALL elements matching?
arr.every(x => x > 0);  // true
arr.every(x => x > 2);  // false

// some — are ANY elements matching?
arr.some(x => x > 4);   // true
arr.some(x => x > 10);  // false

// forEach — iterate, returns undefined (does NOT create new array)
arr.forEach((value, index, array) => {
  console.log(`${index}: ${value}`);
});
// Cannot break out of forEach — use for...of instead if you need break
```

### Combining Arrays

```javascript
// concat — merge arrays
[1, 2].concat([3, 4], [5, 6]); // [1, 2, 3, 4, 5, 6]
[1, 2].concat(3, 4);           // [1, 2, 3, 4]

// spread — usually clearer
[...[1, 2], ...[3, 4]]; // [1, 2, 3, 4]
[1, 2, ...[3, 4], 5];   // [1, 2, 3, 4, 5]

// join — convert to string
[1, 2, 3].join("-"); // "1-2-3"
[1, 2, 3].join("");  // "123"
[1, 2, 3].join();    // "1,2,3" (default separator is comma)
```

### Copying Arrays

```javascript
const original = [1, 2, 3];

// Shallow copy methods
const copy1 = original.slice();
const copy2 = [...original];
const copy3 = Array.from(original);
const copy4 = original.concat();

// All create NEW arrays — modifying copy doesn't affect original
copy1.push(4);
console.log(original); // [1, 2, 3] — unchanged

// But nested objects/arrays are still shared (shallow copy!)
const nested = [[1, 2], [3, 4]];
const shallowCopy = [...nested];
shallowCopy[0].push(99);
console.log(nested[0]); // [1, 2, 99] — changed! (shared reference)

// Deep copy — use structuredClone (ES2022, modern browsers/Node 17+)
const deep = structuredClone(nested);
deep[0].push(99);
console.log(nested[0]); // [1, 2] — unchanged
```

### Destructuring Arrays

```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Skip elements
const [a, , b] = [1, 2, 3]; // a = 1, b = 3

// Default values
const [x = 10, y = 20] = [1]; // x = 1, y = 20 (default)

// Swap variables
let p = 1, q = 2;
[p, q] = [q, p]; // p = 2, q = 1

// Nested destructuring
const [[a1, a2], [b1, b2]] = [[1, 2], [3, 4]];
```

---

## 13. Objects — Complete Guide

### Creating Objects

```javascript
// Object literal
const person = {
  name: "Alice",
  age: 30,
  "favorite color": "blue", // quoted keys for special characters
  greet() { return `Hi, I'm ${this.name}`; }, // method shorthand
  get fullInfo() { return `${this.name}, ${this.age}`; } // getter
};

// Computed property names
const key = "dynamicKey";
const obj = {
  [key]: "value",
  [`prefix_${key}`]: "prefixed value"
};

// Property shorthand (when variable name matches key name)
const name = "Bob";
const age = 25;
const user = { name, age }; // { name: "Bob", age: 25 }
```

### Accessing Properties

```javascript
const obj = { name: "Alice", "my key": "value", nested: { x: 1 } };

// Dot notation
obj.name;         // "Alice"
obj.nested.x;     // 1

// Bracket notation — required for keys with spaces or dynamic keys
obj["my key"];    // "value"
const key = "name";
obj[key];         // "Alice"

// Optional chaining
obj?.nested?.y;   // undefined — no crash if nested doesn't have y
```

### Object Methods

```javascript
const obj = { a: 1, b: 2, c: 3 };

// Get all keys
Object.keys(obj);    // ["a", "b", "c"]
// Get all values
Object.values(obj);  // [1, 2, 3]
// Get key-value pairs
Object.entries(obj); // [["a", 1], ["b", 2], ["c", 3]]
// Create from entries
Object.fromEntries([["a", 1], ["b", 2]]); // { a: 1, b: 2 }
Object.fromEntries(new Map([["a", 1]]));  // { a: 1 }

// Check if property exists
"a" in obj;              // true
obj.hasOwnProperty("a"); // true — only own properties
Object.hasOwn(obj, "a"); // true — modern, safer alternative (ES2022)

// Merge objects
const merged = Object.assign({}, obj, { d: 4 }); // { a:1, b:2, c:3, d:4 }
const merged2 = { ...obj, d: 4 };                // Same with spread

// Note: Object.assign is shallow — nested objects are still references
const target = { a: { x: 1 } };
const source = { a: { y: 2 } };
Object.assign(target, source); // target.a = { y: 2 } — REPLACED, not merged!

// Deep merge requires custom code or lodash:
function deepMerge(target, source) {
  const result = { ...target };
  for (const key in source) {
    if (source[key] && typeof source[key] === "object" && !Array.isArray(source[key])) {
      result[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}
```

### Destructuring Objects

```javascript
const user = { name: "Alice", age: 30, email: "alice@example.com", role: "admin" };

// Basic destructuring
const { name, age } = user; // name = "Alice", age = 30

// Rename while destructuring
const { name: userName, age: userAge } = user; // userName = "Alice"

// Default values
const { name, location = "Unknown" } = user; // location = "Unknown"

// Rest
const { name, ...rest } = user;
// name = "Alice", rest = { age: 30, email: "...", role: "..." }

// Nested
const data = { user: { address: { city: "NYC" } } };
const { user: { address: { city } } } = data; // city = "NYC"

// In function parameters
function displayUser({ name, age, role = "user" }) {
  console.log(`${name} (${age}) — ${role}`);
}
displayUser(user); // "Alice (30) — admin"
```

### Property Descriptors & Object Immutability

Already covered in the Prototypes section above.

### Shallow vs Deep Copy

```javascript
const original = { a: 1, b: { c: 2 } };

// Shallow copy — nested objects are shared
const shallow = { ...original };
shallow.a = 99;          // OK — doesn't affect original
shallow.b.c = 99;        // Changes original.b.c too!
console.log(original.b.c); // 99

// Deep copy options:
// 1. structuredClone (modern, handles most cases)
const deep = structuredClone(original);
deep.b.c = 999;
console.log(original.b.c); // 99 — unchanged

// 2. JSON round-trip (old way, loses functions, dates, undefined, etc.)
const jsonCopy = JSON.parse(JSON.stringify(original));
// Loses: functions, undefined, Symbol, Date (converted to string), etc.
```

---

## 14. Destructuring & Spread / Rest

### Spread Operator (`...`)

```javascript
// Spread array elements
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];         // [1, 2, 3, 4, 5, 6]
const withExtra = [0, ...arr1, ...arr2, 7]; // [0, 1, 2, 3, 4, 5, 6, 7]

// Spread into function call
Math.max(...arr1); // 3

// Spread object properties
const obj1 = { a: 1, b: 2 };
const obj2 = { c: 3, d: 4 };
const merged = { ...obj1, ...obj2 };  // { a:1, b:2, c:3, d:4 }
const overridden = { ...obj1, b: 99 }; // { a:1, b:99 } — b is overridden

// Spread string into characters
[..."hello"] // ["h", "e", "l", "l", "o"]
```

### Rest Parameters (`...`)

```javascript
// Collect remaining function arguments
function log(level, timestamp, ...messages) {
  messages.forEach(msg => console.log(`[${level}][${timestamp}] ${msg}`));
}
log("INFO", "2024-01-01", "Server started", "Port 3000", "Ready"); 
// Logs 3 messages

// Rest in destructuring — collect remaining elements
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first=1, second=2, rest=[3,4,5]

const { a, b, ...others } = { a: 1, b: 2, c: 3, d: 4 };
// a=1, b=2, others={c:3, d:4}
```

---

## 15. Iterators & Generators

### Iterators

An **iterator** is an object with a `next()` method that returns `{ value, done }` objects.

```javascript
// Manual iterator
function createRange(start, end) {
  let current = start;
  return {
    next() {
      if (current <= end) {
        return { value: current++, done: false };
      }
      return { value: undefined, done: true };
    }
  };
}

const range = createRange(1, 3);
range.next(); // { value: 1, done: false }
range.next(); // { value: 2, done: false }
range.next(); // { value: 3, done: false }
range.next(); // { value: undefined, done: true }
```

### Iterables

An object is **iterable** if it has a `[Symbol.iterator]` method that returns an iterator.

```javascript
// Making a custom iterable
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        if (current <= last) return { value: current++, done: false };
        return { value: undefined, done: true };
      }
    };
  }
};

// Now we can use for...of!
for (let num of range) {
  console.log(num); // 1, 2, 3, 4, 5
}

// And spread!
console.log([...range]); // [1, 2, 3, 4, 5]

// And destructuring!
const [a, b, c] = range; // a=1, b=2, c=3
```

### Generators

Generators are functions that can **pause** their execution and resume later. They automatically implement the iterator protocol.

```javascript
function* simpleGenerator() {
  console.log("Start");
  yield 1;           // pause, return 1
  console.log("After 1");
  yield 2;           // pause, return 2
  console.log("After 2");
  yield 3;           // pause, return 3
  console.log("End");
}

const gen = simpleGenerator();
gen.next(); // logs "Start", returns { value: 1, done: false }
gen.next(); // logs "After 1", returns { value: 2, done: false }
gen.next(); // logs "After 2", returns { value: 3, done: false }
gen.next(); // logs "End", returns { value: undefined, done: true }

// Generators are iterable
for (let val of simpleGenerator()) {
  console.log(val); // 1, 2, 3
}

// Practical: Infinite sequence generator
function* naturals(start = 1) {
  while (true) {
    yield start++;
  }
}

function take(gen, n) {
  const result = [];
  for (let val of gen) {
    result.push(val);
    if (result.length === n) return result;
  }
}

take(naturals(), 5); // [1, 2, 3, 4, 5]
take(naturals(10), 5); // [10, 11, 12, 13, 14]

// Passing values to generators
function* accumulator() {
  let total = 0;
  while (true) {
    const value = yield total; // yield returns the passed-in value
    total += value;
  }
}

const acc = accumulator();
acc.next();     // { value: 0, done: false } — start
acc.next(10);   // { value: 10, done: false } — total is 10
acc.next(20);   // { value: 30, done: false } — total is 30

// yield* — delegate to another iterable/generator
function* concat(...iterables) {
  for (const iterable of iterables) {
    yield* iterable;
  }
}
[...concat([1,2], [3,4], [5,6])]; // [1, 2, 3, 4, 5, 6]
```

---

## 16. Symbols & Well-Known Symbols

### Symbols

```javascript
// Every Symbol() call creates a unique symbol
const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log(sym1 === sym2); // false — always unique!

// Global symbol registry
const global1 = Symbol.for("shared");
const global2 = Symbol.for("shared");
console.log(global1 === global2); // true — same symbol

// Use as object key
const ID = Symbol("id");
const obj = { [ID]: 42, name: "Alice" };
obj[ID]; // 42
Object.keys(obj); // ["name"] — Symbol not in keys
JSON.stringify(obj); // '{"name":"Alice"}' — Symbol ignored by JSON
```

### Well-Known Symbols

Built-in symbols that hook into JavaScript's internal behavior.

```javascript
// Symbol.iterator — makes objects iterable
class Range {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
  
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    return {
      next() {
        return current <= end
          ? { value: current++, done: false }
          : { value: undefined, done: true };
      }
    };
  }
}
[...new Range(1, 5)]; // [1, 2, 3, 4, 5]

// Symbol.toPrimitive — control type conversion
class Temperature {
  constructor(celsius) { this.celsius = celsius; }
  
  [Symbol.toPrimitive](hint) {
    if (hint === "number") return this.celsius;
    if (hint === "string") return `${this.celsius}°C`;
    return this.celsius; // default
  }
}
const temp = new Temperature(25);
+temp;          // 25 (number hint)
`${temp}`;      // "25°C" (string hint)
temp + 0;       // 25 (default hint)

// Symbol.hasInstance — controls instanceof behavior
class EvenNumber {
  static [Symbol.hasInstance](num) {
    return Number.isInteger(num) && num % 2 === 0;
  }
}
2 instanceof EvenNumber;  // true
3 instanceof EvenNumber;  // false

// Symbol.toStringTag — customize Object.prototype.toString
class MyCollection {
  get [Symbol.toStringTag]() { return "MyCollection"; }
}
Object.prototype.toString.call(new MyCollection()); // "[object MyCollection]"
```

---

## 17. The Event Loop — Deep Dive

This is the most important concept for understanding JavaScript's async behavior.

### The Call Stack

The call stack tracks what's currently executing. JavaScript is single-threaded — it can only do ONE thing at a time.

```javascript
function third() {
  console.log("Third");
}

function second() {
  third();
  console.log("Second");
}

function first() {
  second();
  console.log("First");
}

first();
// Call Stack progression:
// [first] → [first, second] → [first, second, third] → "Third"
//         → [first, second] → "Second"
//         → [first] → "First"
//         → []
```

### Web APIs / Node APIs

When you call `setTimeout`, `fetch`, `fs.readFile`, etc., the work is delegated to the browser/Node.js runtime (outside the JS engine). The callback is registered there.

```javascript
console.log("1 - Start");

setTimeout(() => {
  console.log("3 - Timeout callback"); // queued by browser after 0ms
}, 0);

console.log("2 - End");

// Output:
// 1 - Start
// 2 - End
// 3 - Timeout callback
// Even with 0ms delay! Because the callback goes through the queue.
```

### Microtask Queue vs Macrotask Queue

```
Microtask Queue (higher priority):
  - Promise callbacks (.then, .catch, .finally)
  - queueMicrotask()
  - MutationObserver callbacks

Macrotask Queue (also called Callback Queue, lower priority):
  - setTimeout callbacks
  - setInterval callbacks
  - I/O callbacks (Node.js)
  - UI rendering events
```

### The Event Loop Algorithm

```
while (true) {
  1. Execute ALL tasks in the call stack until it's empty
  2. Execute ALL microtasks (drain the entire microtask queue)
  3. Render (browser only, if needed)
  4. Pick ONE macrotask from the macrotask queue and execute it
  5. Go back to step 2
}
```

```javascript
console.log("Script start");            // 1

setTimeout(() => {
  console.log("setTimeout");           // 5 — macrotask
}, 0);

Promise.resolve()
  .then(() => console.log("Promise 1")) // 3 — microtask
  .then(() => console.log("Promise 2")); // 4 — microtask (chained)

console.log("Script end");              // 2

// Output:
// Script start
// Script end
// Promise 1
// Promise 2
// setTimeout
```

### More Complex Example

```javascript
console.log("1");

setTimeout(() => {
  console.log("2");
  Promise.resolve().then(() => console.log("3"));
}, 0);

setTimeout(() => {
  console.log("4");
}, 0);

Promise.resolve()
  .then(() => {
    console.log("5");
    setTimeout(() => console.log("6"), 0);
  })
  .then(() => console.log("7"));

console.log("8");

// Output: 1, 8, 5, 7, 2, 3, 4, 6
// Explanation:
// Sync: 1, 8
// Microtasks: 5, 7
//   (setTimeout from inside 5 is queued as macrotask)
// Macrotasks: 2 (then microtask: 3), 4, 6
```

### `setImmediate` and `process.nextTick` (Node.js)

```javascript
// process.nextTick — runs BEFORE any I/O events and BEFORE Promise callbacks
// Technically NOT in the event loop — it's a special Node.js queue

process.nextTick(() => console.log("nextTick")); // runs before microtasks!
Promise.resolve().then(() => console.log("Promise"));
setTimeout(() => console.log("setTimeout"), 0);
console.log("sync");

// Output:
// sync
// nextTick
// Promise
// setTimeout
```

---

## 18. Promises — Complete Guide

A Promise represents a value that may not be available yet.

### Promise States

```
Pending → Fulfilled (with a value)
        → Rejected (with a reason/error)
```

Once settled (fulfilled or rejected), a promise cannot change state.

### Creating Promises

```javascript
const promise = new Promise((resolve, reject) => {
  // Executor function — runs immediately
  
  // Simulate async work
  const success = Math.random() > 0.5;
  
  if (success) {
    resolve("Operation succeeded!"); // fulfills the promise
  } else {
    reject(new Error("Operation failed")); // rejects the promise
  }
});
```

### Consuming Promises

```javascript
promise
  .then(value => {
    // Runs when fulfilled
    console.log("Success:", value);
    return "processed"; // can return a new value
  })
  .catch(error => {
    // Runs when rejected (or when .then throws)
    console.log("Error:", error.message);
    // Can recover by returning a value (promise continues as fulfilled)
    return "recovered";
  })
  .finally(() => {
    // Runs regardless of success or failure
    console.log("Cleanup");
    // Cannot change the value/error (it passes through)
  });
```

### Promise Chaining

```javascript
fetch("https://api.example.com/user/1")
  .then(response => {
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    return response.json(); // returns a new promise!
  })
  .then(user => {
    console.log("User:", user);
    return fetch(`https://api.example.com/posts?userId=${user.id}`);
  })
  .then(response => response.json())
  .then(posts => {
    console.log("Posts:", posts);
  })
  .catch(error => {
    // Catches ANY error in the chain above
    console.error("Something went wrong:", error);
  });
```

### Static Promise Methods

```javascript
// Promise.resolve() — creates an already-fulfilled promise
Promise.resolve(42).then(v => console.log(v)); // 42

// Promise.reject() — creates an already-rejected promise
Promise.reject(new Error("fail")).catch(e => console.log(e.message));

// Promise.all() — wait for ALL to succeed (rejects if ANY reject)
const p1 = fetch("/api/users");
const p2 = fetch("/api/posts");
const p3 = fetch("/api/comments");

Promise.all([p1, p2, p3])
  .then(([users, posts, comments]) => {
    // All three resolved — destructured!
  })
  .catch(error => {
    // Called as soon as FIRST promise rejects
  });

// Promise.allSettled() — wait for ALL to settle (never rejects)
Promise.allSettled([p1, p2, Promise.reject("err")])
  .then(results => {
    results.forEach(result => {
      if (result.status === "fulfilled") {
        console.log("Success:", result.value);
      } else {
        console.log("Failure:", result.reason);
      }
    });
  });

// Promise.race() — resolves/rejects with FIRST settled promise
Promise.race([
  fetch("/api/data"),
  new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout")), 5000))
])
  .then(data => console.log("Got data!"))
  .catch(err => console.log("Timed out or error:", err.message));

// Promise.any() — resolves with FIRST fulfilled promise (ignores rejections)
// Only rejects if ALL reject
Promise.any([
  Promise.reject("fail1"),
  Promise.resolve("success"),
  Promise.reject("fail2")
])
  .then(value => console.log(value)); // "success"
```

### Creating Promise Utilities

```javascript
// Promisify a callback-based function
function readFileAsync(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, "utf8", (error, data) => {
      if (error) reject(error);
      else resolve(data);
    });
  });
}

// Delay/sleep function
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
await sleep(1000); // pause for 1 second

// Retry with exponential backoff
async function retry(fn, maxAttempts, baseDelay = 1000) {
  let attempt = 0;
  while (attempt < maxAttempts) {
    try {
      return await fn();
    } catch (error) {
      attempt++;
      if (attempt === maxAttempts) throw error;
      await sleep(baseDelay * 2 ** attempt);
    }
  }
}
```

---

## 19. Async / Await

`async/await` is syntactic sugar over Promises — it makes async code look and behave like synchronous code.

### Basics

```javascript
// Any function with 'async' keyword always returns a Promise
async function fetchUser(id) {
  // 'await' pauses execution until the promise settles
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user; // this is wrapped in Promise.resolve(user)
}

// Equivalent to:
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(response => response.json());
}

// Consuming the async function
fetchUser(1)
  .then(user => console.log(user))
  .catch(error => console.error(error));

// Or with another async function:
async function main() {
  const user = await fetchUser(1);
  console.log(user);
}
```

### Error Handling with try/catch

```javascript
async function loadUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const user = await response.json();
    
    const postsResponse = await fetch(`/api/posts?userId=${userId}`);
    const posts = await postsResponse.json();
    
    return { user, posts };
  } catch (error) {
    console.error("Failed to load user data:", error);
    throw error; // re-throw if you want callers to handle it
  } finally {
    console.log("Fetch attempt completed");
  }
}
```

### Running in Parallel vs Sequential

```javascript
// SEQUENTIAL — one after another (slow if independent)
async function sequential() {
  const user = await fetchUser(1);       // 500ms
  const posts = await fetchPosts(1);     // 500ms
  // Total: ~1000ms
  return { user, posts };
}

// PARALLEL — all at once (fast!)
async function parallel() {
  const [user, posts] = await Promise.all([
    fetchUser(1),   // starts immediately
    fetchPosts(1)   // starts immediately too
  ]);
  // Total: ~500ms (they run concurrently)
  return { user, posts };
}

// PARALLEL with individual results (even if one fails)
async function parallelSafe() {
  const [userResult, postsResult] = await Promise.allSettled([
    fetchUser(1),
    fetchPosts(1)
  ]);
  
  const user = userResult.status === "fulfilled" ? userResult.value : null;
  const posts = postsResult.status === "fulfilled" ? postsResult.value : [];
  
  return { user, posts };
}
```

### Async Iteration

```javascript
// Async iterators for streaming data
async function* generateData() {
  for (let i = 0; i < 5; i++) {
    await sleep(100);
    yield i;
  }
}

// for await...of
async function processStream() {
  for await (const value of generateData()) {
    console.log(value); // 0, 1, 2, 3, 4 (each after 100ms delay)
  }
}

// Real use case: streaming API responses
async function* streamJson(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value);
  }
}
```

### Top-Level Await (ES2022)

```javascript
// In ES modules, you can use await at the top level (outside async functions)
const config = await fetch("/config.json").then(r => r.json());
const db = await initDatabase(config.dbUrl);

export { db };
// Other modules that import from this file will wait for the await to resolve
```

---

## 20. Error Handling

### Error Types

```javascript
// Built-in error types
new Error("Generic error");           // base type
new TypeError("Wrong type");          // wrong type of value
new RangeError("Out of range");       // number out of valid range
new ReferenceError("Not defined");    // undefined variable
new SyntaxError("Invalid syntax");    // syntax problem
new URIError("Bad URI");              // malformed URI
new EvalError("eval() problem");      // problem with eval()

// Error properties
const err = new Error("Something went wrong");
err.name;    // "Error"
err.message; // "Something went wrong"
err.stack;   // Stack trace string
```

### Custom Error Classes

```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);              // sets this.message
    this.name = "AppError";      // override name
    this.statusCode = statusCode;
    
    // Fix prototype chain for instanceof to work correctly
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

class ValidationError extends AppError {
  constructor(field, message) {
    super(message, 400);
    this.name = "ValidationError";
    this.field = field;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`, 404);
    this.name = "NotFoundError";
    this.resource = resource;
    this.id = id;
  }
}

// Usage
try {
  throw new ValidationError("email", "Invalid email format");
} catch (error) {
  if (error instanceof ValidationError) {
    console.log(`Validation failed: ${error.field} — ${error.message}`);
  } else if (error instanceof NotFoundError) {
    console.log(`Not found: ${error.resource} #${error.id}`);
  } else if (error instanceof AppError) {
    console.log(`App error (${error.statusCode}): ${error.message}`);
  } else {
    console.log("Unknown error:", error);
    throw error; // re-throw unexpected errors
  }
}
```

### Error Handling Patterns

```javascript
// 1. Result pattern (no throwing)
function divide(a, b) {
  if (b === 0) return { error: new Error("Division by zero"), value: null };
  return { error: null, value: a / b };
}

const { error, value } = divide(10, 0);
if (error) console.log("Error:", error.message);
else console.log("Result:", value);

// 2. Try-catch in async functions
async function safeOperation() {
  try {
    const data = await riskyOperation();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 3. Global error handlers
// Browser
window.onerror = function(message, source, lineno, colno, error) {
  console.error("Global error:", message);
  // Report to error tracking service
};
window.addEventListener("unhandledrejection", event => {
  console.error("Unhandled promise rejection:", event.reason);
  event.preventDefault(); // prevent browser from logging
});

// Node.js
process.on("uncaughtException", (error) => {
  console.error("Uncaught exception:", error);
  process.exit(1); // exit gracefully
});
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled rejection at:", promise, "reason:", reason);
});
```

---

## 21. Modules (ESM & CJS)

### CommonJS (CJS) — Node.js Default (Historically)

```javascript
// Exporting (math.js)
const PI = 3.14159;

function add(a, b) { return a + b; }
function multiply(a, b) { return a * b; }

module.exports = { PI, add, multiply };
// Or individual exports:
// module.exports.add = add;
// exports.add = add; // 'exports' is a shorthand reference

// Importing (main.js)
const { PI, add, multiply } = require("./math");
const math = require("./math"); // math.PI, math.add, etc.
const add = require("./math").add; // single item

// require() is synchronous
// The required file is cached — same object returned on repeated requires
```

### ES Modules (ESM) — Modern Standard

```javascript
// Named exports (math.js)
export const PI = 3.14159;

export function add(a, b) { return a + b; }

export function multiply(a, b) { return a * b; }

// Default export — one per module
export default function subtract(a, b) { return a - b; }

// Or export at the end
const PI = 3.14159;
function add(a, b) { return a + b; }
export { PI, add, add as addNumbers }; // can rename with 'as'

// Importing (main.js)
import subtract from "./math.js";         // default import
import { PI, add } from "./math.js";      // named imports
import { add as sum } from "./math.js";   // rename
import * as math from "./math.js";        // import all as namespace
import subtract, { PI, add } from "./math.js"; // both default and named

// Dynamic imports — lazy loading
async function loadMath() {
  const { add, multiply } = await import("./math.js");
  console.log(add(1, 2));
}

// Re-exporting
export { add } from "./math.js";           // re-export named
export { default } from "./math.js";       // re-export default
export * from "./math.js";                 // re-export all named
export * as MathUtils from "./math.js";    // re-export as namespace
```

**ESM vs CJS key differences:**

| Feature | ESM | CJS |
|---------|-----|-----|
| Syntax | `import/export` | `require/module.exports` |
| Loading | Static (parsed at compile time) | Dynamic (executed at runtime) |
| Async | Yes (supports top-level await) | No (synchronous) |
| Tree shaking | Yes (bundlers can eliminate unused exports) | Harder |
| Circular deps | Handled differently (live bindings) | Can cause issues |
| File extension | `.mjs` or `"type":"module"` in package.json | `.cjs` or default in Node |

---

## 22. Map, Set, WeakMap, WeakSet

### Map

A `Map` holds key-value pairs where keys can be **any type** (unlike objects where keys are always strings/symbols).

```javascript
const map = new Map();

// Setting values
map.set("name", "Alice");
map.set(42, "number key");
map.set(true, "boolean key");
const objKey = { id: 1 };
map.set(objKey, "object key");

// Getting values
map.get("name");    // "Alice"
map.get(42);        // "number key"
map.get(objKey);    // "object key" — same reference!
map.get({ id: 1 }); // undefined — different object!

// Checking
map.has("name");    // true
map.has("missing"); // false

// Size
map.size;           // 4

// Deleting
map.delete("name"); // true
map.clear();        // removes all entries

// Creating from array of pairs
const map2 = new Map([
  ["a", 1],
  ["b", 2],
  ["c", 3]
]);

// Iterating
for (let [key, value] of map2) {
  console.log(`${key}: ${value}`);
}
for (let key of map2.keys()) { ... }
for (let value of map2.values()) { ... }
for (let entry of map2.entries()) { ... } // same as for...of map

map2.forEach((value, key) => console.log(`${key}: ${value}`));

// Converting
Array.from(map2);           // [["a",1], ["b",2], ["c",3]]
[...map2];                  // same
Object.fromEntries(map2);   // { a:1, b:2, c:3 }

// Map vs Object:
// - Map preserves insertion order
// - Map keys can be any type
// - Map has size property
// - Map is iterable directly
// - Map has no prototype key conflicts
```

### Set

A `Set` is a collection of **unique** values.

```javascript
const set = new Set([1, 2, 3, 2, 1]); // {1, 2, 3} — duplicates removed

set.add(4);       // {1, 2, 3, 4}
set.add(2);       // {1, 2, 3, 4} — no duplicate added
set.has(2);       // true
set.has(5);       // false
set.delete(2);    // {1, 3, 4}
set.size;         // 3
set.clear();      // {}

// Iterating
for (let value of set) { ... }
set.forEach(value => ...);
[...set]; // convert to array

// Set operations (manual — not built-in)
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);

// Union
const union = new Set([...a, ...b]); // {1,2,3,4,5,6}

// Intersection
const intersection = new Set([...a].filter(x => b.has(x))); // {3,4}

// Difference (a - b)
const difference = new Set([...a].filter(x => !b.has(x))); // {1,2}

// Remove duplicates from array
const arr = [1, 1, 2, 2, 3, 3];
const unique = [...new Set(arr)]; // [1, 2, 3]
```

### WeakMap

Like Map, but keys must be **objects** and are held **weakly** (don't prevent garbage collection).

```javascript
const weakMap = new WeakMap();
let user = { name: "Alice" };
weakMap.set(user, { sessionId: "abc123" });

weakMap.get(user);     // { sessionId: "abc123" }
weakMap.has(user);     // true
weakMap.delete(user);  // removes the entry

// When user object is garbage collected, the WeakMap entry is automatically cleaned up
user = null; // now { name: "Alice" } can be garbage collected

// WeakMap is NOT iterable — no size, no forEach, no entries()
// Used for: private data, caching without memory leaks
```

### WeakSet

```javascript
const weakSet = new WeakSet();
let obj = { data: "something" };
weakSet.add(obj);
weakSet.has(obj); // true
weakSet.delete(obj);

// Also not iterable
// Use case: tracking which objects have been processed without preventing GC
```

**When to use each:**
- `Map`: key-value pairs with non-string keys, ordered iteration, frequent additions/deletions
- `Set`: unique values, efficient has() checks, mathematical set operations
- `WeakMap`: associating data with objects when you don't want to control their lifetime (caching, private data)
- `WeakSet`: tracking object membership without memory concerns

---

## 23. Regular Expressions

Regular expressions are patterns for matching text.

### Creating RegExp

```javascript
// Literal notation (compiled at load time)
const re1 = /hello/;
const re2 = /hello/gi; // with flags: g=global, i=case-insensitive

// Constructor (dynamic, compiled at runtime)
const pattern = "hello";
const re3 = new RegExp(pattern, "gi");
const re4 = new RegExp(`^${pattern}$`, "i"); // with template literal
```

### Flags

| Flag | Meaning |
|------|---------|
| `g` | Global — find all matches (not just first) |
| `i` | Case-insensitive |
| `m` | Multiline — ^ and $ match start/end of each line |
| `s` | Dotall — `.` matches newlines too |
| `u` | Unicode — enables full Unicode matching |
| `v` | UnicodeSets — extended Unicode mode (ES2024) |
| `d` | Indices — provides start/end indices of matches |

### Character Classes & Patterns

```javascript
// Exact character
/a/          // matches "a"

// Character classes
/[abc]/      // matches a, b, or c
/[a-z]/      // any lowercase letter
/[A-Z]/      // any uppercase letter
/[0-9]/      // any digit
/[a-zA-Z]/   // any letter
/[^abc]/     // NOT a, b, or c (negated)

// Shorthand classes
/\d/         // [0-9] — digit
/\D/         // [^0-9] — non-digit
/\w/         // [a-zA-Z0-9_] — word character
/\W/         // non-word character
/\s/         // whitespace (space, tab, newline)
/\S/         // non-whitespace
/./          // any character except newline (with s flag, includes newline)

// Anchors
/^hello/     // matches "hello" at START of string/line
/world$/     // matches "world" at END of string/line
/^hello$/    // matches exactly "hello" (whole string)
/\bhello\b/  // word boundary — "hello" as whole word

// Quantifiers
/a*/         // 0 or more 'a'
/a+/         // 1 or more 'a'
/a?/         // 0 or 1 'a' (optional)
/a{3}/       // exactly 3 'a'
/a{2,4}/     // 2 to 4 'a'
/a{2,}/      // 2 or more 'a'

// Lazy (non-greedy) — add ?
/a+?/        // as few 'a' as possible
/a{2,4}?/    // as few as possible (2)

// Groups
/(ab)+/      // capture group — matches "ababab", captures "ab"
/(?:ab)+/    // non-capturing group — matches but doesn't capture
/(?<name>\w+)/ // named capture group

// Alternation
/cat|dog/    // matches "cat" or "dog"
/(cat|dog)s/ // matches "cats" or "dogs"

// Lookahead / Lookbehind
/\d+(?=px)/  // digits followed by "px" (lookahead, "px" not captured)
/(?<=\$)\d+/ // digits preceded by "$" (lookbehind)
/\d+(?!px)/  // digits NOT followed by "px" (negative lookahead)
/(?<!\$)\d+/ // digits NOT preceded by "$" (negative lookbehind)
```

### String Methods with RegExp

```javascript
const str = "Hello World, hello JavaScript";

// test — returns boolean
/hello/i.test(str);  // true

// match — returns array of matches
str.match(/hello/i);  // ["Hello"] — first match, with index and input
str.match(/hello/gi); // ["Hello", "hello"] — all matches (global flag)

// matchAll — returns iterator of all matches with groups
const matches = [...str.matchAll(/(\w+)\s(\w+)/g)];
matches.forEach(m => console.log(m[0], m[1], m[2]));

// search — returns index of first match (or -1)
str.search(/world/i); // 6

// replace — replaces matches
str.replace(/hello/i, "Hi");   // "Hi World, hello JavaScript"
str.replace(/hello/gi, "Hi");  // "Hi World, Hi JavaScript"
// With function:
str.replace(/(\w+)/g, (match) => match.toUpperCase()); // ALL CAPS
str.replace(/(\w+)/g, (match, p1, offset) => `${p1}@${offset}`);

// replaceAll — replaces all (no need for g flag)
str.replaceAll("hello", "Hi"); // case-sensitive, no regex

// split — split by regex
"one1two2three".split(/\d/); // ["one", "two", "three"]
```

### Named Capture Groups

```javascript
const dateStr = "2024-01-15";
const dateRegex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match = dateStr.match(dateRegex);

if (match) {
  const { year, month, day } = match.groups;
  console.log(year, month, day); // "2024" "01" "15"
}

// In replace
"2024-01-15".replace(
  /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/,
  "$<day>/$<month>/$<year>"
); // "15/01/2024"
```

---

## 24. JSON

JSON (JavaScript Object Notation) is a text format for representing structured data.

### Serializing and Parsing

```javascript
// JSON.stringify — convert JS to JSON string
const user = { name: "Alice", age: 30, active: true };
JSON.stringify(user);                    // '{"name":"Alice","age":30,"active":true}'
JSON.stringify(user, null, 2);          // pretty-printed with 2-space indent
JSON.stringify(user, ["name", "age"]);  // only include specified keys
// Replacer function:
JSON.stringify(user, (key, value) => {
  if (typeof value === "number") return value * 2; // transform numbers
  return value;
}); // '{"name":"Alice","age":60,"active":true}'

// JSON.parse — convert JSON string to JS
const json = '{"name":"Alice","age":30}';
const parsed = JSON.parse(json); // { name: "Alice", age: 30 }

// Reviver function:
const withDates = '{"name":"Alice","createdAt":"2024-01-01T00:00:00.000Z"}';
JSON.parse(withDates, (key, value) => {
  if (key === "createdAt") return new Date(value); // convert string to Date
  return value;
});
```

### What JSON Supports

```
✅ Supported: string, number, boolean, null, array, object
❌ NOT supported: undefined, function, Symbol, Date, Map, Set, RegExp, Infinity, NaN
```

```javascript
JSON.stringify({ a: undefined, b: function(){}, c: Symbol() }); // '{}'
JSON.stringify({ a: Infinity, b: NaN }); // '{"a":null,"b":null}'
JSON.stringify([undefined, function(){}]); // '[null,null]'
```

### Custom JSON Serialization

```javascript
class User {
  constructor(name, password) {
    this.name = name;
    this.password = password; // don't want this in JSON!
  }
  
  toJSON() {
    // Only serialize safe fields
    return { name: this.name };
  }
}

const user = new User("Alice", "secret123");
JSON.stringify(user); // '{"name":"Alice"}' — password excluded!
```

---

## 25. The DOM (Browser Environment)

The DOM (Document Object Model) is the browser's API for interacting with HTML.

### Selecting Elements

```javascript
// Single element selectors
document.getElementById("myId");              // by ID
document.querySelector(".my-class");          // first match (CSS selector)
document.querySelector("#id .class > p");     // complex CSS selector

// Multiple element selectors
document.querySelectorAll(".item");           // NodeList (static)
document.getElementsByClassName("item");     // HTMLCollection (live)
document.getElementsByTagName("div");         // HTMLCollection (live)

// Relative to an element
const container = document.querySelector(".container");
container.querySelector(".child");            // within container
container.querySelectorAll("li");             // all li within container

// Navigating the DOM tree
const el = document.querySelector("p");
el.parentElement;          // parent element
el.parentNode;             // parent node (could be document)
el.children;               // element children (HTMLCollection)
el.childNodes;             // all child nodes (includes text, comments)
el.firstElementChild;      // first element child
el.lastElementChild;       // last element child
el.nextElementSibling;     // next element sibling
el.previousElementSibling; // previous element sibling
```

### Modifying Elements

```javascript
const el = document.querySelector("#myDiv");

// Content
el.textContent = "Just text — no HTML parsing";
el.innerHTML = "<strong>Bold</strong> text"; // Parses HTML (XSS risk!)
el.innerText = "Visible text only";          // Respects CSS visibility

// Attributes
el.setAttribute("data-id", "42");
el.getAttribute("data-id"); // "42"
el.removeAttribute("data-id");
el.hasAttribute("class");    // boolean

// Properties (often mirrors attributes for built-in ones)
el.id = "newId";
el.className = "class1 class2";

// classList — better way to manage classes
el.classList.add("active");
el.classList.remove("inactive");
el.classList.toggle("hidden");    // add if absent, remove if present
el.classList.contains("active");  // boolean
el.classList.replace("old", "new");

// Style
el.style.backgroundColor = "red";
el.style.fontSize = "16px";
el.style.display = "none";
// Get computed style (includes CSS from stylesheets)
getComputedStyle(el).backgroundColor;

// Data attributes
el.dataset.userId = "42";      // sets data-user-id="42"
el.dataset.userId;             // reads data-user-id
el.dataset.firstName;          // reads data-first-name
```

### Creating & Inserting Elements

```javascript
// Create
const div = document.createElement("div");
div.textContent = "Hello";
div.className = "card";

// Insert
document.body.appendChild(div);          // add as last child
document.body.prepend(div);              // add as first child
container.insertBefore(div, reference); // before a reference element

// Modern methods
el.append(div, "text");         // add multiple children/text
el.prepend(div);                // add as first child
el.before(div);                 // insert before the element itself
el.after(div);                  // insert after the element itself
el.replaceWith(div);            // replace the element

// Remove
el.remove();                    // remove from DOM
parent.removeChild(el);         // old way

// Clone
const clone = el.cloneNode(true);  // true = deep clone (includes children)
const shallow = el.cloneNode(false); // shallow = no children
```

### Efficient DOM Manipulation

```javascript
// DocumentFragment — build DOM off-screen, then insert once
const fragment = document.createDocumentFragment();

for (let i = 0; i < 1000; i++) {
  const li = document.createElement("li");
  li.textContent = `Item ${i}`;
  fragment.appendChild(li); // no reflow yet!
}

// Single DOM operation — one reflow
ul.appendChild(fragment);

// innerHTML for large updates (but watch XSS)
const items = ["apple", "banana", "cherry"];
ul.innerHTML = items.map(item => `<li>${item}</li>`).join("");

// insertAdjacentHTML — fast and safe for known positions
el.insertAdjacentHTML("beforebegin", "<p>Before el</p>");
el.insertAdjacentHTML("afterbegin", "<p>First child</p>");
el.insertAdjacentHTML("beforeend", "<p>Last child</p>");
el.insertAdjacentHTML("afterend", "<p>After el</p>");
```

---

## 26. Events & Event Delegation

### Adding Event Listeners

```javascript
const button = document.querySelector("button");

// addEventListener — preferred method
button.addEventListener("click", function(event) {
  console.log("Clicked!", event);
});

// Arrow function (but 'this' won't be the element)
button.addEventListener("click", (event) => {
  console.log(event.target); // the element that was clicked
});

// Named function (can be removed)
function handleClick(event) {
  console.log("Click!");
}
button.addEventListener("click", handleClick);
button.removeEventListener("click", handleClick); // must pass same reference

// Options object
button.addEventListener("click", handler, {
  once: true,    // auto-removes after first call
  capture: true, // capture phase instead of bubble phase
  passive: true  // won't call preventDefault (better scroll performance)
});
```

### The Event Object

```javascript
element.addEventListener("click", function(event) {
  event.target;           // element that triggered the event
  event.currentTarget;    // element the listener is attached to
  event.type;             // "click"
  event.bubbles;          // does it bubble?
  event.cancelable;       // can it be prevented?
  event.timeStamp;        // when it occurred
  
  event.preventDefault(); // prevent default behavior (link navigation, form submit)
  event.stopPropagation(); // stop bubbling up
  event.stopImmediatePropagation(); // stop other listeners on same element too
  
  // Mouse events
  event.clientX; event.clientY; // position relative to viewport
  event.pageX; event.pageY;     // position relative to document
  event.offsetX; event.offsetY; // position relative to element
  
  // Keyboard events
  event.key;    // "Enter", "ArrowUp", "a", etc.
  event.code;   // "KeyA", "Space", "Enter" — physical key
  event.ctrlKey; event.altKey; event.shiftKey; event.metaKey; // modifier keys
  
  // Touch events
  event.touches;       // list of all touch points
  event.changedTouches; // touches that changed
});
```

### Event Bubbling & Capturing

```javascript
// Events bubble UP from target to root (default behavior)
// parent → grandparent → document → window

document.querySelector(".child").addEventListener("click", (e) => {
  console.log("child clicked");
  // e.stopPropagation() would stop the bubbling here
});

document.querySelector(".parent").addEventListener("click", () => {
  console.log("parent handler called too!"); // because of bubbling
});

// Capture phase — listener fires on the way DOWN from root to target
document.querySelector(".parent").addEventListener("click", () => {
  console.log("capture on parent"); // fires BEFORE child handler
}, true); // true = capture phase
```

### Event Delegation

Instead of attaching listeners to each child, attach ONE listener to the parent and use `event.target`.

```javascript
// Without delegation — 1000 event listeners!
document.querySelectorAll(".item").forEach(item => {
  item.addEventListener("click", handleItemClick);
});

// With delegation — 1 listener, works for dynamically added items too!
document.querySelector(".list").addEventListener("click", function(event) {
  // Check if the clicked element (or its ancestor) is what we care about
  const item = event.target.closest(".item");
  if (!item) return; // clicked something that's not an .item
  
  console.log("Item clicked:", item.dataset.id);
});

// closest() — traverses up the DOM tree to find matching ancestor
const btn = event.target.closest("[data-action]");
if (btn) {
  const action = btn.dataset.action;
  // Handle different actions based on data attribute
}
```

### Custom Events

```javascript
// Create and dispatch custom events
const customEvent = new CustomEvent("user-logged-in", {
  detail: { userId: 42, username: "Alice" }, // custom data
  bubbles: true,
  cancelable: true
});

document.dispatchEvent(customEvent);

// Listen for custom events
document.addEventListener("user-logged-in", (event) => {
  console.log("User logged in:", event.detail.username);
});

// Simple EventEmitter pattern (for non-DOM use)
class EventEmitter {
  #listeners = new Map();
  
  on(event, callback) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, []);
    this.#listeners.get(event).push(callback);
    return () => this.off(event, callback); // return unsubscribe fn
  }
  
  off(event, callback) {
    const callbacks = this.#listeners.get(event) || [];
    this.#listeners.set(event, callbacks.filter(cb => cb !== callback));
  }
  
  emit(event, ...args) {
    (this.#listeners.get(event) || []).forEach(cb => cb(...args));
  }
  
  once(event, callback) {
    const wrapper = (...args) => {
      callback(...args);
      this.off(event, wrapper);
    };
    this.on(event, wrapper);
  }
}
```

---

## 27. Fetch API & HTTP

### Basic Fetch

```javascript
// GET request
fetch("https://api.example.com/users")
  .then(response => {
    console.log(response.status);  // 200
    console.log(response.ok);      // true if 200-299
    console.log(response.headers.get("Content-Type"));
    return response.json(); // parses JSON body
  })
  .then(data => console.log(data))
  .catch(error => console.error("Network error:", error));
  // Note: fetch only rejects on NETWORK errors, not HTTP errors (4xx, 5xx)!

// Using async/await
async function getUsers() {
  const response = await fetch("https://api.example.com/users");
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}
```

### POST, PUT, DELETE Requests

```javascript
// POST — create
const newUser = { name: "Alice", email: "alice@example.com" };
const response = await fetch("/api/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer my-token"
  },
  body: JSON.stringify(newUser)
});

// PUT — update (full replacement)
await fetch("/api/users/1", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Alice Updated", email: "new@example.com" })
});

// PATCH — partial update
await fetch("/api/users/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Alice Updated" }) // only the changed fields
});

// DELETE
await fetch("/api/users/1", { method: "DELETE" });
```

### Response Types

```javascript
response.json();     // parse as JSON
response.text();     // get as text
response.blob();     // get as Blob (files, images)
response.arrayBuffer(); // raw binary data
response.formData(); // as FormData
```

### Aborting Requests

```javascript
const controller = new AbortController();

// Cancel after 5 seconds
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch("/api/data", {
    signal: controller.signal
  });
  clearTimeout(timeout);
  return await response.json();
} catch (error) {
  if (error.name === "AbortError") {
    console.log("Request was cancelled");
  } else {
    throw error;
  }
}
```

### Upload with FormData

```javascript
const formData = new FormData();
formData.append("name", "Alice");
formData.append("avatar", fileInput.files[0]); // file upload

await fetch("/api/profile", {
  method: "POST",
  body: formData
  // Don't set Content-Type — browser will set it with the boundary
});
```

---

## 28. Storage APIs

### localStorage and sessionStorage

```javascript
// localStorage — persists until explicitly cleared
localStorage.setItem("user", JSON.stringify({ name: "Alice" }));
const user = JSON.parse(localStorage.getItem("user"));
localStorage.removeItem("user");
localStorage.clear(); // clears all localStorage data
localStorage.length;  // number of items
localStorage.key(0);  // get key at index

// sessionStorage — cleared when tab/browser closes
sessionStorage.setItem("tempData", "value");
// Same API as localStorage

// Wrapper for safe JSON storage
const storage = {
  get: (key, defaultValue = null) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch { return defaultValue; }
  },
  set: (key, value) => {
    try { localStorage.setItem(key, JSON.stringify(value)); }
    catch (e) { console.error("Storage failed:", e); }
  },
  remove: (key) => localStorage.removeItem(key),
  clear: () => localStorage.clear()
};
```

### Cookies

```javascript
// Setting cookies
document.cookie = "name=Alice; expires=Fri, 31 Dec 2024 23:59:59 GMT; path=/";
document.cookie = "theme=dark; max-age=86400; SameSite=Lax; Secure";

// Reading cookies (all at once as a string)
document.cookie; // "name=Alice; theme=dark"

// Cookie utility
function getCookie(name) {
  const cookies = document.cookie.split("; ");
  const cookie = cookies.find(row => row.startsWith(name + "="));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
}

function setCookie(name, value, days = 7, options = {}) {
  const maxAge = days * 24 * 60 * 60;
  let cookie = `${name}=${encodeURIComponent(value)}; max-age=${maxAge}; path=${options.path || "/"}`;
  if (options.sameSite) cookie += `; SameSite=${options.sameSite}`;
  if (options.secure) cookie += "; Secure";
  document.cookie = cookie;
}
```

---

## 29. Functional Programming Patterns

JavaScript supports functional programming (FP) — a style where you:
- Use **pure functions** (no side effects, same input always gives same output)
- **Avoid mutation** (create new values instead of modifying existing ones)
- Treat functions as data (**first-class functions**)

### Pure Functions

```javascript
// Impure — has side effects, depends on external state
let total = 0;
function addToTotal(amount) {
  total += amount; // side effect: modifies external variable
  return total;
}

// Pure — same input always gives same output, no side effects
function add(a, b) {
  return a + b; // no side effects, no external dependencies
}

// Impure — mutates input
function sortItems(arr) {
  return arr.sort(); // sort() modifies the original array!
}

// Pure — creates new sorted array
function sortItems(arr) {
  return [...arr].sort(); // copy first, then sort
}
```

### Immutability

```javascript
// Instead of mutating:
const user = { name: "Alice", age: 30 };
user.age = 31; // mutation — bad in FP

// Create new object with the change:
const updatedUser = { ...user, age: 31 }; // user is unchanged

// Array immutability
const arr = [1, 2, 3];
// Bad (mutating):
arr.push(4);
arr.sort();

// Good (non-mutating):
const newArr = [...arr, 4];       // add
const filtered = arr.filter(...); // filter
const mapped = arr.map(...);      // transform
const sorted = [...arr].sort();   // sort (copy first!)
```

### Composition

```javascript
// Composing functions — output of one becomes input of next
const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

const double = x => x * 2;
const addOne = x => x + 1;
const square = x => x * x;

const transform = pipe(double, addOne, square);
transform(3); // pipe(3): double(3)=6, addOne(6)=7, square(7)=49
```

### Currying

```javascript
// Currying — convert f(a, b, c) into f(a)(b)(c)
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}

const add = (a, b, c) => a + b + c;
const curriedAdd = curry(add);

curriedAdd(1)(2)(3);  // 6
curriedAdd(1, 2)(3);  // 6
curriedAdd(1)(2, 3);  // 6
curriedAdd(1, 2, 3);  // 6

// Useful for creating specialized functions
const multiply = (factor, value) => factor * value;
const curriedMultiply = curry(multiply);
const double = curriedMultiply(2); // partially applied
const triple = curriedMultiply(3);

double(5);  // 10
triple(5);  // 15
[1,2,3].map(double); // [2, 4, 6]
```

### Functor, Monad-like Patterns

```javascript
// Maybe monad — handle null/undefined safely
class Maybe {
  constructor(value) {
    this._value = value;
  }
  
  static of(value) { return new Maybe(value); }
  static empty() { return new Maybe(null); }
  
  isNothing() { return this._value === null || this._value === undefined; }
  
  map(fn) {
    return this.isNothing() ? Maybe.empty() : Maybe.of(fn(this._value));
  }
  
  getOrElse(defaultValue) {
    return this.isNothing() ? defaultValue : this._value;
  }
  
  flatMap(fn) {
    return this.isNothing() ? Maybe.empty() : fn(this._value);
  }
}

// Usage
const user = null;
const result = Maybe.of(user)
  .map(u => u.profile)
  .map(p => p.name)
  .getOrElse("Anonymous");
// result = "Anonymous" — no null pointer exceptions!
```

### Transducers (Advanced)

```javascript
// Problem: multiple array passes are inefficient
const result = [1, 2, 3, 4, 5]
  .filter(x => x % 2 === 0)  // creates new array
  .map(x => x * x)            // creates another new array
  .reduce((sum, x) => sum + x, 0);
// 3 passes through the data

// Transducers — compose transformations into a single pass
const filter = (pred) => (reducer) => (acc, value) =>
  pred(value) ? reducer(acc, value) : acc;

const map = (transform) => (reducer) => (acc, value) =>
  reducer(acc, transform(value));

const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

const xform = compose(
  filter(x => x % 2 === 0),
  map(x => x * x)
);

const result = [1, 2, 3, 4, 5].reduce(
  xform((sum, x) => sum + x), // the final reducer
  0
);
// 20 — but in a single pass!
```

---

## 30. Design Patterns in JavaScript

### Creational Patterns

#### Singleton

```javascript
class Database {
  static #instance = null;
  
  constructor(connectionString) {
    if (Database.#instance) {
      return Database.#instance;
    }
    this.connection = this.connect(connectionString);
    Database.#instance = this;
  }
  
  connect(connectionString) {
    console.log("Connecting to:", connectionString);
    return { status: "connected" };
  }
  
  static getInstance(connectionString) {
    if (!Database.#instance) {
      new Database(connectionString);
    }
    return Database.#instance;
  }
}

const db1 = Database.getInstance("mongodb://localhost");
const db2 = Database.getInstance("mongodb://other");
db1 === db2; // true — same instance
```

#### Factory Pattern

```javascript
// Simple factory
class UserFactory {
  static create(type, data) {
    switch (type) {
      case "admin":   return new AdminUser(data);
      case "guest":   return new GuestUser(data);
      case "regular": return new RegularUser(data);
      default: throw new Error(`Unknown user type: ${type}`);
    }
  }
}

const admin = UserFactory.create("admin", { name: "Bob" });

// Factory function (without classes)
function createButton(type) {
  const base = {
    render: () => console.log(`Rendering ${type} button`),
    onClick: () => {}
  };
  
  if (type === "primary") {
    return { ...base, className: "btn-primary", variant: "filled" };
  } else if (type === "secondary") {
    return { ...base, className: "btn-secondary", variant: "outlined" };
  }
  
  return base;
}
```

#### Builder Pattern

```javascript
class QueryBuilder {
  #table = "";
  #conditions = [];
  #columns = ["*"];
  #limit = null;
  #orderBy = null;
  
  from(table) {
    this.#table = table;
    return this; // enables chaining
  }
  
  select(...columns) {
    this.#columns = columns;
    return this;
  }
  
  where(condition) {
    this.#conditions.push(condition);
    return this;
  }
  
  orderBy(column, direction = "ASC") {
    this.#orderBy = `${column} ${direction}`;
    return this;
  }
  
  limit(n) {
    this.#limit = n;
    return this;
  }
  
  build() {
    let query = `SELECT ${this.#columns.join(", ")} FROM ${this.#table}`;
    if (this.#conditions.length > 0) {
      query += ` WHERE ${this.#conditions.join(" AND ")}`;
    }
    if (this.#orderBy) query += ` ORDER BY ${this.#orderBy}`;
    if (this.#limit) query += ` LIMIT ${this.#limit}`;
    return query;
  }
}

const query = new QueryBuilder()
  .from("users")
  .select("id", "name", "email")
  .where("active = true")
  .where("age > 18")
  .orderBy("name")
  .limit(10)
  .build();
// "SELECT id, name, email FROM users WHERE active = true AND age > 18 ORDER BY name ASC LIMIT 10"
```

### Structural Patterns

#### Observer Pattern

```javascript
class EventBus {
  #subscribers = new Map();
  
  subscribe(event, callback) {
    if (!this.#subscribers.has(event)) {
      this.#subscribers.set(event, new Set());
    }
    this.#subscribers.get(event).add(callback);
    // Return unsubscribe function
    return () => this.#subscribers.get(event)?.delete(callback);
  }
  
  publish(event, data) {
    this.#subscribers.get(event)?.forEach(callback => {
      try {
        callback(data);
      } catch (e) {
        console.error(`Error in subscriber for ${event}:`, e);
      }
    });
  }
  
  once(event, callback) {
    const unsubscribe = this.subscribe(event, (data) => {
      callback(data);
      unsubscribe();
    });
    return unsubscribe;
  }
}

const bus = new EventBus();
const unsub = bus.subscribe("user:login", (user) => console.log("Login:", user));
bus.publish("user:login", { name: "Alice" }); // "Login: Alice"
unsub(); // stop listening
```

#### Proxy Pattern

```javascript
function createValidator(target, validators) {
  return new Proxy(target, {
    set(obj, prop, value) {
      if (validators[prop]) {
        const error = validators[prop](value);
        if (error) throw new TypeError(error);
      }
      obj[prop] = value;
      return true;
    }
  });
}

const user = createValidator({}, {
  age: (val) => {
    if (typeof val !== "number") return "Age must be a number";
    if (val < 0 || val > 150) return "Age must be between 0 and 150";
  },
  email: (val) => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) return "Invalid email";
  }
});

user.age = 25;     // OK
user.email = "alice@example.com"; // OK
user.age = -5;     // TypeError: Age must be between 0 and 150

// Proxy for logging/tracing
function createLogged(target) {
  return new Proxy(target, {
    get(obj, prop) {
      if (typeof obj[prop] === "function") {
        return function(...args) {
          console.log(`Calling ${prop} with`, args);
          const result = obj[prop].apply(obj, args);
          console.log(`${prop} returned`, result);
          return result;
        };
      }
      console.log(`Getting ${prop}:`, obj[prop]);
      return obj[prop];
    },
    set(obj, prop, value) {
      console.log(`Setting ${prop} to`, value);
      obj[prop] = value;
      return true;
    }
  });
}
```

### Behavioral Patterns

#### Strategy Pattern

```javascript
// Sort strategies
const sortStrategies = {
  bubble(arr) {
    // bubble sort implementation
    const a = [...arr];
    for (let i = 0; i < a.length - 1; i++) {
      for (let j = 0; j < a.length - i - 1; j++) {
        if (a[j] > a[j + 1]) [a[j], a[j + 1]] = [a[j + 1], a[j]];
      }
    }
    return a;
  },
  merge(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = sortStrategies.merge(arr.slice(0, mid));
    const right = sortStrategies.merge(arr.slice(mid));
    const result = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
      result.push(left[i] <= right[j] ? left[i++] : right[j++]);
    }
    return [...result, ...left.slice(i), ...right.slice(j)];
  },
  native(arr) {
    return [...arr].sort((a, b) => a - b);
  }
};

class Sorter {
  constructor(strategy = "native") {
    this.strategy = strategy;
  }
  
  sort(arr) {
    return sortStrategies[this.strategy](arr);
  }
  
  setStrategy(strategy) {
    this.strategy = strategy;
  }
}

const sorter = new Sorter("merge");
sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]); // [1, 1, 2, 3, 4, 5, 6, 9]
```

---

## 31. Memory Management & Garbage Collection

### How GC Works

JavaScript uses **mark-and-sweep** garbage collection:
1. Starting from "roots" (global variables, call stack)
2. Mark everything reachable
3. Sweep (delete) everything not marked

```javascript
// Object becomes garbage when no references remain
let obj = { data: "large data" };
let ref = obj; // two references

obj = null; // still one reference (ref)
ref = null; // zero references — now eligible for GC
```

### Memory Leaks

```javascript
// 1. Unintentional global variables (in non-strict mode)
function leak() {
  // 'accidentalGlobal' is not declared with var/let/const
  // It becomes a property of the global object!
  accidentalGlobal = "This leaks!"; // BAD
}

// 2. Forgotten event listeners
const element = document.querySelector("#myBtn");
function heavyHandler() {
  // holds reference to large data
}
element.addEventListener("click", heavyHandler);
// If element is removed from DOM but handler not removed:
element.remove(); // handler is never collected! (the element stays in memory)
// Fix:
element.removeEventListener("click", heavyHandler);

// 3. Closures holding references unnecessarily
function createLeak() {
  const largeData = new Array(1000000).fill("data"); // 1MB
  return function() {
    return largeData[0]; // only needs first element but keeps ALL
  };
}
// Fix: extract only what's needed
function createOptimized() {
  const largeData = new Array(1000000).fill("data");
  const firstItem = largeData[0]; // extract
  // largeData can now be collected
  return function() { return firstItem; };
}

// 4. Timers not cleared
const timer = setInterval(() => {
  // runs forever, holding references
}, 1000);
// clearInterval(timer); // must clear when done!

// 5. Detached DOM nodes
let detachedNode = document.querySelector("#myEl");
detachedNode.parentNode.removeChild(detachedNode);
// detachedNode variable still holds the element — it can't be collected!
detachedNode = null; // now it can be collected
```

---

## 32. Performance Optimization

### Debounce & Throttle

```javascript
// Debounce — wait until activity stops, then fire ONCE
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Usage: search input — only search after user stops typing for 300ms
const searchInput = document.querySelector("#search");
searchInput.addEventListener("input", debounce(async (e) => {
  const results = await search(e.target.value);
  displayResults(results);
}, 300));

// Throttle — fire at most once per interval
function throttle(fn, interval) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      return fn.apply(this, args);
    }
  };
}

// Usage: scroll handler — fire at most once per 100ms
window.addEventListener("scroll", throttle(() => {
  updateScrollPosition();
}, 100));
```

### Lazy Loading and Code Splitting

```javascript
// Dynamic import for code splitting
async function loadHeavyFeature() {
  const { HeavyComponent } = await import("./HeavyComponent.js");
  return new HeavyComponent();
}

// Intersection Observer for lazy loading images
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src; // load image
      observer.unobserve(img);   // stop observing
    }
  });
}, { rootMargin: "200px" }); // start loading 200px before visible

document.querySelectorAll("img[data-src]").forEach(img => observer.observe(img));
```

### Web Workers

```javascript
// Run CPU-intensive tasks on a background thread
// main.js
const worker = new Worker("worker.js");

worker.postMessage({ data: largeDataset, operation: "sort" });

worker.onmessage = function(event) {
  const { result } = event.data;
  displayResult(result);
};

// worker.js
self.onmessage = function(event) {
  const { data, operation } = event.data;
  
  if (operation === "sort") {
    const result = data.sort((a, b) => a - b); // runs in background!
    self.postMessage({ result });
  }
};
```

---

## 33. Security Basics

### XSS (Cross-Site Scripting)

```javascript
// VULNERABLE — inserting user data directly into HTML
const userInput = "<script>document.cookie // steal cookies</script>";
element.innerHTML = userInput; // DANGEROUS!

// SAFE — use textContent instead
element.textContent = userInput; // text, not HTML

// SAFE — sanitize if you must use innerHTML
function sanitize(html) {
  const div = document.createElement("div");
  div.textContent = html;
  return div.innerHTML; // entities are escaped
}
element.innerHTML = sanitize(userInput);

// Or use DOMPurify library:
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Content Security Policy (CSP)

```html
<!-- HTTP header or meta tag restricting what can load -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'nonce-abc123'">
```

### CSRF Protection

```javascript
// Include CSRF token in state-changing requests
async function updateUser(data) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
  return fetch("/api/users/me", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": csrfToken
    },
    body: JSON.stringify(data)
  });
}
```

---

## 34. Node.js Fundamentals

Node.js runs JavaScript outside the browser using V8 + additional APIs.

### Core Modules

```javascript
// File System
const fs = require("fs"); // sync
const fsPromises = require("fs/promises"); // promise-based

// Read file
const data = fs.readFileSync("file.txt", "utf8"); // synchronous
const data = await fsPromises.readFile("file.txt", "utf8"); // async

// Write file
fs.writeFileSync("output.txt", "Hello");
await fsPromises.writeFile("output.txt", "Hello");

// Append
await fsPromises.appendFile("log.txt", "New line\n");

// List directory
const files = await fsPromises.readdir("./src");

// File info
const stats = await fsPromises.stat("file.txt");
stats.isFile();      // true
stats.isDirectory(); // false
stats.size;          // bytes

// Path module
const path = require("path");
path.join("/home", "user", "file.txt"); // "/home/user/file.txt"
path.resolve("./relative");             // absolute path
path.basename("/path/to/file.txt");     // "file.txt"
path.dirname("/path/to/file.txt");      // "/path/to"
path.extname("file.txt");               // ".txt"
path.parse("/path/to/file.txt");        // { root, dir, base, ext, name }

// OS module
const os = require("os");
os.platform();   // "linux", "darwin", "win32"
os.cpus();       // CPU info
os.totalmem();   // total memory in bytes
os.freemem();    // free memory
os.homedir();    // home directory
os.hostname();   // machine hostname
```

### HTTP Server (Built-in)

```javascript
const http = require("http");

const server = http.createServer((req, res) => {
  // req: IncomingMessage
  console.log(req.method, req.url, req.headers);
  
  // Read body
  let body = "";
  req.on("data", chunk => body += chunk.toString());
  req.on("end", () => {
    const data = body ? JSON.parse(body) : null;
    
    // res: ServerResponse
    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ message: "Hello!", data }));
  });
});

server.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

### Streams

```javascript
const fs = require("fs");
const { Transform } = require("stream");

// Readable stream
const readable = fs.createReadStream("large-file.txt", { encoding: "utf8" });
readable.on("data", chunk => console.log("Chunk:", chunk.length));
readable.on("end", () => console.log("Done reading"));
readable.on("error", err => console.error(err));

// Writable stream
const writable = fs.createWriteStream("output.txt");
writable.write("Hello ");
writable.write("World");
writable.end(); // signal we're done

// Transform stream — read, process, write
const upperCase = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
});

// Piping streams together
fs.createReadStream("input.txt")
  .pipe(upperCase)
  .pipe(fs.createWriteStream("output.txt"));

// Async iteration over streams (modern)
async function processFile(path) {
  const stream = fs.createReadStream(path, { encoding: "utf8" });
  for await (const chunk of stream) {
    process(chunk);
  }
}
```

### Environment Variables

```javascript
// Access env vars
process.env.NODE_ENV;         // "development", "production", "test"
process.env.PORT || 3000;     // with fallback
process.env.DATABASE_URL;

// Command line args
process.argv;      // ["node", "script.js", "arg1", "arg2"]
process.argv[2];   // first user arg

// process events
process.on("exit", (code) => console.log("Exiting with code:", code));
process.on("SIGTERM", () => { cleanup(); process.exit(0); });
process.on("SIGINT", () => { cleanup(); process.exit(0); });

// process.nextTick
process.nextTick(() => console.log("Runs before other async")); // microtask-like
```

### Buffers

```javascript
// Buffer — fixed-size chunks of memory (binary data)
const buf1 = Buffer.from("Hello", "utf8");
const buf2 = Buffer.from([72, 101, 108, 108, 111]); // same as above
const buf3 = Buffer.alloc(10); // 10 bytes of zeros

buf1.toString();          // "Hello"
buf1.toString("hex");     // "48656c6c6f"
buf1.toString("base64");  // "SGVsbG8="

Buffer.concat([buf1, buf2]);  // combine buffers
buf1.length;                  // 5 (bytes)
```

---

## 35. Testing in JavaScript

### Types of Tests

```
Unit Tests     — test individual functions/components in isolation
Integration Tests — test how multiple units work together
E2E Tests      — test the entire user journey in a real browser
```

### Jest (Most Popular Testing Framework)

```javascript
// Basic test structure
describe("Calculator", () => {
  describe("add function", () => {
    it("adds two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });
    
    it("handles negative numbers", () => {
      expect(add(-2, 3)).toBe(1);
    });
    
    test("returns 0 when both args are 0", () => { // 'test' is alias for 'it'
      expect(add(0, 0)).toBe(0);
    });
  });
});

// Matchers
expect(value).toBe(exact);           // strict equality (===)
expect(value).toEqual(obj);          // deep equality (for objects/arrays)
expect(value).toBeTruthy();          // truthy
expect(value).toBeFalsy();           // falsy
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();
expect(value).toBeNaN();
expect(num).toBeGreaterThan(n);
expect(num).toBeLessThan(n);
expect(num).toBeCloseTo(n, decimals); // for floating point
expect(str).toMatch(/regex/);
expect(str).toContain("substring");
expect(arr).toContain(item);
expect(arr).toHaveLength(n);
expect(obj).toHaveProperty("key");
expect(obj).toHaveProperty("nested.key", "value");
expect(fn).toThrow();
expect(fn).toThrow("error message");
expect(fn).toThrow(ErrorType);

// Async tests
test("fetches user", async () => {
  const user = await fetchUser(1);
  expect(user).toHaveProperty("name");
});

// Mocking
jest.fn() // create a mock function
const mockFetch = jest.fn().mockResolvedValue({ name: "Alice" });
// Or:
jest.mock("./api", () => ({
  fetchUser: jest.fn().mockResolvedValue({ name: "Alice" })
}));

// Setup and teardown
beforeAll(() => { /* runs once before all tests in file */ });
afterAll(() => { /* runs once after all tests */ });
beforeEach(() => { /* runs before each test */ });
afterEach(() => { /* runs after each test */ });

// Snapshot testing
expect(component).toMatchSnapshot(); // creates/compares snapshot file
```

---

## 36. Modern JavaScript Tooling

### npm / Package Management

```bash
# Initialize project
npm init -y                    # creates package.json with defaults

# Install dependencies
npm install express             # production dependency
npm install --save-dev jest     # dev dependency (not in production)
npm install -g nodemon          # global package

# package.json scripts
{
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "build": "tsc",
    "lint": "eslint src/"
  }
}
```

### Babel — JavaScript Transpiler

```javascript
// .babelrc
{
  "presets": [
    ["@babel/preset-env", {
      "targets": { "browsers": ["last 2 versions"] }
    }]
  ],
  "plugins": ["@babel/plugin-proposal-class-properties"]
}
```

### ESLint — Linting

```javascript
// .eslintrc.js
module.exports = {
  env: { browser: true, node: true, es2022: true },
  extends: ["eslint:recommended"],
  rules: {
    "no-var": "error",
    "prefer-const": "warn",
    "no-unused-vars": "warn",
    "eqeqeq": "error", // require === instead of ==
    "no-console": "warn"
  }
};
```

### Webpack / Vite — Bundlers

```javascript
// vite.config.js — simple, fast, modern bundler
import { defineConfig } from "vite";
export default defineConfig({
  build: {
    outDir: "dist",
    rollupOptions: {
      input: "src/main.js"
    }
  },
  server: {
    port: 3000,
    proxy: {
      "/api": "http://localhost:8080"
    }
  }
});
```

---

## Quick Reference: ES2015–ES2024 Features

```javascript
// ES2015 (ES6)
let, const, arrow functions, classes, template literals,
destructuring, default params, rest/spread, Promise,
Map, Set, Symbol, iterators, generators, modules (import/export),
for...of, Proxy, Reflect

// ES2016
Array.prototype.includes, ** (exponentiation)

// ES2017
async/await, Object.entries, Object.values, String padding,
Object.getOwnPropertyDescriptors, SharedArrayBuffer

// ES2018
Promise.finally, async iteration (for await...of),
rest/spread in objects, RegExp named groups

// ES2019
Array.flat, Array.flatMap, Object.fromEntries,
String.trimStart, String.trimEnd, Optional catch binding

// ES2020
BigInt, Promise.allSettled, globalThis, ??  (nullish coalescing),
?. (optional chaining), Dynamic import, String.matchAll

// ES2021
Promise.any, AggregateError, WeakRef, FinalizationRegistry,
Logical assignment (&&=, ||=, ??=), Numeric separators (1_000_000)

// ES2022
class fields (#private), static class fields, at() method,
Object.hasOwn, Array.prototype.at, error.cause,
Top-level await, structuredClone

// ES2023
Array.findLast, Array.findLastIndex, Array.toReversed,
Array.toSorted, Array.toSpliced, Array.with, Hashbang grammar

// ES2024
Object.groupBy, Map.groupBy, Promise.withResolvers,
ArrayBuffer.prototype.resize, ArrayBuffer.prototype.transfer
```

---

*This guide covers the entire JavaScript language from the ground up. The next step is the TypeScript guide, which builds directly on this foundation.*
