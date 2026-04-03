# JavaScript — Interview Questions & Answers (Complete Enhanced Reference)
> 130 questions. Full answers with code. Easy → Medium → Hard. Covers engine internals, runtime behaviour, modern APIs, and production patterns.

---

## Table of Contents
- [Easy Questions (Q1–Q40)](#easy-questions)
- [Medium Questions (Q41–Q80)](#medium-questions)
- [Hard Questions (Q81–Q130)](#hard-questions)

---

## EASY QUESTIONS

---

**Q1. What is JavaScript and where does it run?**

JavaScript is a high-level, interpreted, dynamically typed, single-threaded, garbage-collected language with first-class functions. Originally designed for browsers, it now runs in:
- **Browsers** — Chrome (V8), Firefox (SpiderMonkey), Safari (JavaScriptCore)
- **Servers** — Node.js (V8), Deno (V8), Bun (JavaScriptCore)
- **Mobile** — React Native, Capacitor
- **Desktop** — Electron
- **Edge / CDN** — Cloudflare Workers, Vercel Edge Functions

---

**Q2. What is the difference between `var`, `let`, and `const`?**

| | `var` | `let` | `const` |
|--|-------|-------|---------|
| Scope | Function | Block | Block |
| Hoisting | Yes (initialized `undefined`) | Yes (TDZ — not initialized) | Yes (TDZ — not initialized) |
| Re-declare | Yes | No | No |
| Re-assign | Yes | Yes | No |

```javascript
if (true) {
  var x = 1;   // leaks to function scope
  let y = 2;   // block-scoped
  const z = 3; // block-scoped, cannot reassign
}
console.log(x); // 1 — var leaks!
console.log(y); // ReferenceError
console.log(z); // ReferenceError

const obj = { a: 1 };
obj.a = 2;      // OK — mutation allowed
obj = {};       // TypeError — reassignment not allowed
```

---

**Q3. What are JavaScript's primitive data types?**

JavaScript has 7 primitive types (immutable, stored by value):
1. `string` — `"hello"`, `'world'`, `` `template` ``
2. `number` — `42`, `3.14`, `NaN`, `Infinity`
3. `boolean` — `true`, `false`
4. `null` — intentional absence
5. `undefined` — declared but not assigned
6. `symbol` — unique identifier: `Symbol("id")`
7. `bigint` — arbitrary precision: `9007199254740992n`

Everything else is `object` (arrays, functions, dates, maps, etc.).

---

**Q4. What is the difference between `null` and `undefined`?**

```javascript
let a;             // undefined — JS sets this automatically
let b = null;      // null — developer intentionally set "no value"

typeof undefined   // "undefined"
typeof null        // "object" — historical JS bug, never fixed

null == undefined  // true  (loose)
null === undefined // false (strict)

// Practical difference:
function getUser(id) {
  if (!id) return null;    // user not found — intentional no-value
  return { id };
}
let user;                  // undefined — not yet fetched
user = getUser(0);         // null — explicitly not found
```

---

**Q5. What is `NaN` and how do you detect it?**

`NaN` (Not a Number) results from invalid numeric operations. It is of type `number` and is the only value not equal to itself.

```javascript
typeof NaN        // "number" — counterintuitive!
NaN === NaN       // false — only value not equal to itself

// Detection
Number.isNaN(NaN);        // true  ✅ — no coercion
Number.isNaN("hello");    // false ✅ — "hello" is not NaN
isNaN("hello");           // true  ❌ — coerces "hello" to NaN first
Number.isFinite(Infinity);// false — also useful
Object.is(NaN, NaN);      // true  ✅ — same-value equality
```

---

**Q6. What are truthy and falsy values?**

```javascript
// Falsy values (exactly 8):
false, 0, -0, 0n, "", '', ``, null, undefined, NaN

// Everything else is truthy, including:
"0"        // truthy (non-empty string)
[]         // truthy (empty array)
{}         // truthy (empty object)
-1         // truthy
Infinity   // truthy
new Boolean(false) // truthy (object wrapper!)

// Common pitfall:
if ([]) console.log("truthy"); // prints! empty array is truthy
if ([].length) console.log("truthy"); // doesn't print — 0 is falsy
```

---

**Q7. What is type coercion and what are common pitfalls?**

Type coercion is JavaScript automatically converting values between types.

```javascript
// String concatenation vs addition
"5" + 3       // "53" — number coerced to string
"5" - 3       // 2   — string coerced to number
"5" * "3"     // 15  — both coerced to numbers

// Comparison coercion
0 == false    // true — both become 0
"" == false   // true — both become 0
null == undefined // true
null == 0     // false — null only equals undefined in loose equality

// Object to primitive
[] + []       // "" — both become ""
[] + {}       // "[object Object]"
{} + []       // 0  — {} parsed as empty block, +[] is 0

// Always use strict equality (===) to avoid coercion surprises
```

---

**Q8. What is the difference between `==` and `===`?**

- `==` (loose equality): converts types before comparing
- `===` (strict equality): no conversion, must be same type AND value

```javascript
1 == "1"    // true  (string "1" coerced to number 1)
1 === "1"   // false (different types)

null == undefined   // true
null === undefined  // false

NaN == NaN  // false
NaN === NaN // false (NaN is never equal to itself)

// Rule: always use === except when explicitly checking null OR undefined:
if (value == null) { /* catches both null and undefined */ }
```

---

**Q9. What are the different ways to declare a function?**

```javascript
// 1. Function declaration — hoisted completely
function add(a, b) { return a + b; }

// 2. Function expression — not hoisted
const add = function(a, b) { return a + b; };

// 3. Arrow function — no own `this`, no `arguments`
const add = (a, b) => a + b;

// 4. Method shorthand (in object literals)
const obj = {
  add(a, b) { return a + b; }
};

// 5. Constructor function (old-style classes)
function Person(name) { this.name = name; }

// 6. Generator function
function* gen() { yield 1; yield 2; }

// 7. Async function
async function fetchData() { return await fetch("/api"); }

// Key difference: function declarations are fully hoisted
greet(); // works!
function greet() { console.log("hello"); }

greet2(); // TypeError: greet2 is not a function
var greet2 = function() { console.log("hello"); }; // var hoisted as undefined
```

---

**Q10. What is hoisting?**

Hoisting is JavaScript's behaviour of moving declarations to the top of their scope before execution. Only declarations are hoisted — not initializations.

```javascript
// What you write:
console.log(x); // undefined (not ReferenceError)
var x = 5;
greet();        // "Hello!" — works
function greet() { console.log("Hello!"); }

// What JS engine sees:
var x;           // declaration hoisted, initialized to undefined
function greet() { console.log("Hello!"); } // fully hoisted
console.log(x);
x = 5;
greet();

// let/const are hoisted but NOT initialized — Temporal Dead Zone:
console.log(y); // ReferenceError: Cannot access 'y' before initialization
let y = 10;

// Classes are also hoisted but in TDZ:
new Foo(); // ReferenceError
class Foo {}
```

---

**Q11. What is the Temporal Dead Zone (TDZ)?**

The TDZ is the period between entering a scope where `let`/`const` is declared and the actual declaration being executed. Accessing the variable during TDZ throws a `ReferenceError`.

```javascript
{
  // TDZ starts here for `x`
  console.log(typeof x); // ReferenceError — typeof doesn't protect you with let/const
  let x = 5;             // TDZ ends here
  console.log(x);        // 5
}

// TDZ with function parameters
function example(a = b, b = 1) { // ReferenceError: b is not defined
  return a + b;
}

// Practical: TDZ catches real bugs that var would silently hide
```

---

**Q12. What is a closure?**

A closure is a function that retains access to its lexical scope (the variables of its outer function) even after that outer function has returned.

```javascript
function makeCounter(start = 0) {
  let count = start; // count is captured by closure

  return {
    increment() { return ++count; },
    decrement() { return --count; },
    value()     { return count; },
  };
}

const counter = makeCounter(10);
counter.increment(); // 11
counter.increment(); // 12
counter.decrement(); // 11
counter.value();     // 11

// count is private — not accessible from outside
console.log(counter.count); // undefined

// Classic closure pitfall with var in loops:
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0); // 3, 3, 3 — all share same `i`
}

// Fix with let (block-scoped, new binding each iteration):
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0); // 0, 1, 2 ✅
}
```

---

**Q13. What is the scope chain?**

The scope chain is the mechanism JavaScript uses to resolve variable names. When a variable is referenced, JS looks in the current scope, then the outer scope, and so on up to the global scope.

```javascript
const global = "global";

function outer() {
  const outerVar = "outer";

  function inner() {
    const innerVar = "inner";
    console.log(innerVar); // "inner" — found in local scope
    console.log(outerVar); // "outer" — found in outer scope
    console.log(global);   // "global" — found in global scope
    console.log(notFound); // ReferenceError — not in any scope
  }

  inner();
}

outer();
```

---

**Q14. What is `this` and how is it determined?**

`this` is determined by HOW a function is called, not where it is defined (except arrow functions).

```javascript
// 1. Global context — `this` is globalThis (window in browser, global in Node)
console.log(this); // globalThis

// 2. Object method — `this` is the calling object
const obj = {
  name: "Alice",
  greet() { return `Hello, ${this.name}`; }
};
obj.greet(); // "Hello, Alice"

// 3. Extracted method — `this` is lost!
const greet = obj.greet;
greet(); // "Hello, undefined" — `this` is globalThis (or undefined in strict mode)

// 4. Arrow function — inherits `this` from enclosing scope (lexical this)
const obj2 = {
  name: "Bob",
  greet: () => `Hello, ${this.name}` // `this` is outer scope, NOT obj2!
};
obj2.greet(); // "Hello, undefined"

// 5. `new` keyword — `this` is the newly created object
function Person(name) { this.name = name; }
const p = new Person("Carol");
p.name; // "Carol"

// 6. Explicit binding — call, apply, bind
function greet(greeting) { return `${greeting}, ${this.name}`; }
greet.call({ name: "Dave" }, "Hi");     // "Hi, Dave"
greet.apply({ name: "Eve" }, ["Hey"]);  // "Hey, Eve"
const bound = greet.bind({ name: "Frank" });
bound("Hello");                          // "Hello, Frank"
```

---

**Q15. What is the difference between `call`, `apply`, and `bind`?**

All three explicitly set `this`. They differ in how arguments are passed and when the function executes.

```javascript
function introduce(greeting, punctuation) {
  return `${greeting}, I'm ${this.name}${punctuation}`;
}

const context = { name: "Alice" };

// call — invokes immediately, args passed individually
introduce.call(context, "Hello", "!");  // "Hello, I'm Alice!"

// apply — invokes immediately, args passed as array
introduce.apply(context, ["Hi", "."]);  // "Hi, I'm Alice."

// bind — returns new function with bound `this`, does NOT invoke
const boundFn = introduce.bind(context, "Hey");
boundFn("?"); // "Hey, I'm Alice?" — first arg already bound

// Practical use: borrowing methods
const arr = [1, 2, 3];
Math.max.apply(null, arr); // 3
Math.max(...arr);          // 3 — modern equivalent with spread
```

---

**Q16. What are arrow functions and how do they differ from regular functions?**

```javascript
// Arrow function differences:
// 1. No own `this` — inherits from enclosing lexical scope
class Timer {
  constructor() { this.seconds = 0; }

  start() {
    // Regular function — `this` would be undefined in strict mode:
    // setInterval(function() { this.seconds++; }, 1000); // BUG

    // Arrow function — `this` is the Timer instance:
    setInterval(() => { this.seconds++; }, 1000); // Correct ✅
  }
}

// 2. No `arguments` object
function regular() { console.log(arguments); } // Arguments object
const arrow = () => { console.log(arguments); }; // ReferenceError in strict mode

// 3. Cannot be used as constructor
const Foo = () => {};
new Foo(); // TypeError: Foo is not a constructor

// 4. No `prototype` property
console.log((() => {}).prototype); // undefined

// 5. Cannot be used as generators
// const gen = *() => {}; // SyntaxError

// Concise syntax:
const double = x => x * 2;              // single param, implicit return
const add = (a, b) => a + b;            // multiple params
const getObj = () => ({ key: "val" });   // return object literal (wrap in parens)
const log = x => { console.log(x); };   // block body (explicit return needed)
```

---

**Q17. What is the prototype chain?**

Every JavaScript object has an internal `[[Prototype]]` link to another object. When you access a property, JS looks up this chain until it finds the property or reaches `null`.

```javascript
const animal = {
  breathe() { return "breathing"; }
};

const dog = Object.create(animal); // dog's [[Prototype]] is animal
dog.bark = function() { return "woof"; };

dog.bark();    // "woof" — found on dog directly
dog.breathe(); // "breathing" — found on animal via prototype chain
dog.toString();// "[object Object]" — found on Object.prototype

// With classes (syntactic sugar over prototypes):
class Animal {
  breathe() { return "breathing"; }
}
class Dog extends Animal {
  bark() { return "woof"; }
}

const rex = new Dog();
// rex -> Dog.prototype -> Animal.prototype -> Object.prototype -> null

Object.getPrototypeOf(rex) === Dog.prototype; // true
rex instanceof Dog;    // true
rex instanceof Animal; // true

// hasOwnProperty — checks only the object, not the chain:
rex.hasOwnProperty("bark");    // false — bark is on Dog.prototype
rex.hasOwnProperty("name");    // false (unless set in constructor)
```

---

**Q18. What is the difference between `Object.create()`, `new`, and object literals?**

```javascript
// 1. Object literal — prototype is Object.prototype
const obj = { a: 1 };
Object.getPrototypeOf(obj) === Object.prototype; // true

// 2. Object.create(proto) — sets explicit prototype
const proto = { greet() { return "hello"; } };
const obj2 = Object.create(proto);
obj2.greet(); // "hello"
Object.getPrototypeOf(obj2) === proto; // true

// Create with null prototype (no Object.prototype methods):
const pure = Object.create(null);
pure.toString; // undefined — no prototype chain

// 3. new Constructor — creates object, sets prototype to Constructor.prototype
function Person(name) {
  this.name = name; // `this` is the new object
}
Person.prototype.greet = function() { return `Hi, ${this.name}`; };

const p = new Person("Alice");
// Equivalent to:
// const p = Object.create(Person.prototype);
// Person.call(p, "Alice");

p.greet(); // "Hi, Alice"
Object.getPrototypeOf(p) === Person.prototype; // true
```

---

**Q19. How does `typeof` work and what are its quirks?**

```javascript
typeof "hello"      // "string"
typeof 42           // "number"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof Symbol()     // "symbol"
typeof 42n          // "bigint"
typeof {}           // "object"
typeof []           // "object" — not "array"!
typeof null         // "object" — historical bug!
typeof function(){} // "function" — special case
typeof class{}      // "function" — classes are functions

// Better type checks:
Array.isArray([])         // true
value === null            // null check
value instanceof Date     // true for dates
Object.prototype.toString.call([]) // "[object Array]"
Object.prototype.toString.call(null) // "[object Null]"
```

---

**Q20. What is the event loop?**

The event loop is JavaScript's concurrency mechanism. JS is single-threaded — only one thing runs at a time. The event loop coordinates:
1. **Call stack** — where code currently executes
2. **Web APIs** — browser/Node APIs (setTimeout, fetch, DOM events)
3. **Microtask queue** — Promises, queueMicrotask, MutationObserver
4. **Macrotask queue** — setTimeout, setInterval, I/O callbacks

```javascript
console.log("1 — sync");

setTimeout(() => console.log("2 — macrotask"), 0);

Promise.resolve().then(() => console.log("3 — microtask"));

queueMicrotask(() => console.log("4 — microtask"));

console.log("5 — sync");

// Output: 1, 5, 3, 4, 2
// Rule: sync → microtasks (ALL) → macrotask → microtasks (ALL) → macrotask ...
```

---

**Q21. What is a Promise?**

A Promise is an object representing the eventual completion or failure of an asynchronous operation.

```javascript
// Creating a Promise:
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = true;
    if (success) resolve("data loaded");
    else reject(new Error("failed to load"));
  }, 1000);
});

// Consuming:
promise
  .then(data => console.log(data))       // "data loaded"
  .catch(err => console.error(err))
  .finally(() => console.log("done"));   // always runs

// Promise states: pending → fulfilled | rejected
// Promises are immutable once settled

// Promise chaining — each .then returns a new Promise:
fetch("/api/user")
  .then(res => res.json())
  .then(user => fetch(`/api/posts/${user.id}`))
  .then(res => res.json())
  .then(posts => console.log(posts))
  .catch(err => console.error(err)); // catches any error in the chain
```

---

**Q22. What is `async`/`await`?**

`async`/`await` is syntactic sugar over Promises making asynchronous code look synchronous.

```javascript
// Promise style:
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(user => user);
}

// Async/await style:
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`); // pauses here
  const user = await res.json();
  return user; // wraps in Promise.resolve automatically
}

// Error handling:
async function loadData() {
  try {
    const user = await fetchUser(1);
    const posts = await fetchPosts(user.id);
    return { user, posts };
  } catch (err) {
    console.error("Failed:", err);
    throw err; // re-throw if needed
  }
}

// Parallel execution — don't await sequentially if independent:
async function loadAll() {
  // Sequential (slow — waits for each):
  const a = await fetchA();
  const b = await fetchB();

  // Parallel (fast — both start together):
  const [a, b] = await Promise.all([fetchA(), fetchB()]);
}
```

---

**Q23. What are the Promise static methods?**

```javascript
const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.reject(new Error("fail"));

// Promise.all — all resolve OR first rejection rejects the whole thing
await Promise.all([p1, p2]);          // [1, 2]
await Promise.all([p1, p3]);          // throws Error("fail")

// Promise.allSettled — waits for all, never rejects, returns status objects
await Promise.allSettled([p1, p3]);
// [{ status: "fulfilled", value: 1 }, { status: "rejected", reason: Error }]

// Promise.race — first settled (resolve or reject) wins
await Promise.race([
  new Promise(r => setTimeout(() => r("slow"), 2000)),
  new Promise(r => setTimeout(() => r("fast"), 100)),
]); // "fast"

// Promise.any — first fulfilled wins; rejects only if ALL reject
await Promise.any([p3, p1]);          // 1 — p1 fulfilled
await Promise.any([p3, Promise.reject("x")]); // AggregateError

// Promise.resolve / Promise.reject — create already-settled promises
const resolved = Promise.resolve(42); // already fulfilled
const rejected = Promise.reject(new Error("oops")); // already rejected
```

---

**Q24. What are JavaScript modules (ESM)?**

```javascript
// Named exports:
// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export function subtract(a, b) { return a - b; }

// Named imports:
import { PI, add } from "./math.js";
import { add as sum } from "./math.js"; // rename
import * as math from "./math.js";      // namespace import

// Default export (one per file):
// utils.js
export default function formatDate(date) {
  return date.toISOString();
}

// Default import:
import formatDate from "./utils.js"; // any name
import myFormat from "./utils.js";   // any name

// Mixed:
import formatDate, { PI } from "./utils.js";

// Dynamic import (lazy, returns Promise):
const module = await import("./heavy-module.js");
module.default();

// Re-exports:
export { add, subtract } from "./math.js";
export { default as formatDate } from "./utils.js";
```

---

**Q25. What is destructuring?**

```javascript
// Array destructuring:
const [a, b, c] = [1, 2, 3];
const [first, , third] = [1, 2, 3]; // skip elements
const [x = 0, y = 0] = [10];        // default values
const [head, ...tail] = [1, 2, 3, 4]; // rest

// Object destructuring:
const { name, age } = { name: "Alice", age: 30 };
const { name: fullName } = { name: "Bob" }; // rename
const { role = "user" } = {};               // default value
const { address: { city } } = { address: { city: "Cairo" } }; // nested

// Function parameters:
function greet({ name, age = 0 }) {
  return `${name} is ${age}`;
}
greet({ name: "Alice", age: 30 });

// Swap variables:
let m = 1, n = 2;
[m, n] = [n, m]; // m = 2, n = 1

// From function return:
function getCoords() { return { x: 10, y: 20 }; }
const { x, y } = getCoords();
```

---

**Q26. What is the spread operator and rest parameters?**

```javascript
// Spread (...) — expands iterables:
const arr = [1, 2, 3];
const arr2 = [...arr, 4, 5]; // [1, 2, 3, 4, 5]
Math.max(...arr);             // 3

// Shallow clone:
const clone = [...arr]; // new array, same elements
const objClone = { ...obj }; // shallow clone object

// Merge objects:
const merged = { ...defaults, ...overrides }; // rightmost wins

// Rest parameters — collects remaining args into array:
function sum(first, ...rest) {
  return rest.reduce((acc, n) => acc + n, first);
}
sum(1, 2, 3, 4); // 10

// Difference from `arguments`:
// - rest is a real Array (has map, filter, etc.)
// - `arguments` is array-like, includes ALL args
// - arrow functions have no `arguments`
```

---

**Q27. What are template literals?**

```javascript
const name = "Alice";
const age = 30;

// Basic interpolation:
const msg = `Hello, ${name}! You are ${age} years old.`;

// Multi-line:
const html = `
  <div>
    <h1>${name}</h1>
  </div>
`;

// Expressions:
const result = `${2 + 2} is four`;
const upper = `${name.toUpperCase()}`;

// Tagged templates — function processes the template:
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] !== undefined ? `<strong>${values[i]}</strong>` : "";
    return result + str + value;
  }, "");
}

highlight`Hello, ${name}! You are ${age} years old.`;
// "Hello, <strong>Alice</strong>! You are <strong>30</strong> years old."

// Use cases: SQL builders, styled-components, i18n, sanitization
```

---

**Q28. What are getters and setters?**

```javascript
class Temperature {
  #celsius;

  constructor(celsius) {
    this.#celsius = celsius;
  }

  get fahrenheit() {
    return this.#celsius * 9/5 + 32;
  }

  set fahrenheit(value) {
    this.#celsius = (value - 32) * 5/9;
  }

  get celsius() { return this.#celsius; }
  set celsius(value) {
    if (value < -273.15) throw new RangeError("Below absolute zero!");
    this.#celsius = value;
  }
}

const temp = new Temperature(0);
temp.fahrenheit; // 32 — accessed like a property
temp.fahrenheit = 212; // sets celsius to 100
temp.celsius;   // 100

// Object literal getters/setters:
const circle = {
  _radius: 5,
  get area() { return Math.PI * this._radius ** 2; },
  set radius(r) { this._radius = r; }
};
```

---

**Q29. What are JavaScript classes?**

```javascript
class Animal {
  // Private field (truly private, not accessible outside)
  #health = 100;

  constructor(name, sound) {
    this.name = name;   // public field
    this.sound = sound;
  }

  // Instance method
  speak() { return `${this.name} says ${this.sound}`; }

  // Static method — called on class, not instance
  static create(name, sound) { return new Animal(name, sound); }

  // Getter
  get isHealthy() { return this.#health > 0; }

  // Private method
  #heal() { this.#health = 100; }
}

class Dog extends Animal {
  #tricks = [];

  constructor(name) {
    super(name, "woof"); // must call super before using `this`
  }

  learn(trick) { this.#tricks.push(trick); }

  // Override parent method
  speak() {
    return `${super.speak()} (and knows ${this.#tricks.length} tricks)`;
  }
}

const dog = new Dog("Rex");
dog.speak(); // "Rex says woof (and knows 0 tricks)"
dog.learn("sit");
dog.#tricks; // SyntaxError — private!
```

---

**Q30. What are Symbols?**

```javascript
// Symbols are unique, immutable identifiers
const id = Symbol("id");
const id2 = Symbol("id");
id === id2; // false — always unique

// Use as unique object keys (won't clash with strings):
const USER_ID = Symbol("userId");
const obj = {
  [USER_ID]: 42,
  name: "Alice"
};
obj[USER_ID]; // 42
// Won't appear in for...in or Object.keys:
Object.keys(obj); // ["name"] — Symbol keys hidden

// Well-known Symbols — hooks into JS internals:
class Range {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }

  // Makes Range iterable with for...of
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    return {
      next() {
        if (current <= end) return { value: current++, done: false };
        return { value: undefined, done: true };
      }
    };
  }
}

for (const n of new Range(1, 5)) {
  console.log(n); // 1, 2, 3, 4, 5
}

// Symbol.toPrimitive, Symbol.hasInstance, Symbol.toStringTag, etc.
```

---

**Q31. What is optional chaining (`?.`) and nullish coalescing (`??`)?**

```javascript
const user = {
  profile: {
    address: null
  }
};

// Optional chaining — short-circuits on null/undefined:
user?.profile?.address?.city  // undefined (no error)
user?.profile?.getCity?.()    // undefined (method call)
user?.data?.[0]               // undefined (array access)

// Without it:
user && user.profile && user.profile.address && user.profile.address.city

// Nullish coalescing — returns right side only when LEFT is null/undefined:
null ?? "default"       // "default"
undefined ?? "default"  // "default"
0 ?? "default"          // 0     — 0 is NOT null/undefined
"" ?? "default"         // ""    — "" is NOT null/undefined
false ?? "default"      // false — false is NOT null/undefined

// Compare with || (OR) — returns right side when left is FALSY:
0 || "default"     // "default" — 0 is falsy
"" || "default"    // "default" — "" is falsy

// Nullish assignment:
user.settings ??= {};          // assign only if null/undefined
user.count ||= 0;              // assign if falsy
user.count &&= user.count + 1; // assign if truthy
```

---

**Q32. What is the difference between `for...in` and `for...of`?**

```javascript
const arr = [10, 20, 30];
arr.custom = "oops";

// for...in — iterates KEYS (indices for arrays, property names for objects)
for (const key in arr) {
  console.log(key); // "0", "1", "2", "custom" — includes added properties!
}
// for...in is for OBJECTS, not arrays — use with caution on arrays

// for...of — iterates VALUES of iterables (arrays, strings, maps, sets)
for (const value of arr) {
  console.log(value); // 10, 20, 30 — doesn't include "custom"
}

// for...of with entries():
for (const [index, value] of arr.entries()) {
  console.log(index, value); // 0 10, 1 20, 2 30
}

// for...in on objects (its intended use):
const obj = { a: 1, b: 2 };
for (const key in obj) {
  if (obj.hasOwnProperty(key)) { // filter inherited properties
    console.log(key, obj[key]);
  }
}

// for...of works on any iterable: strings, Maps, Sets, generators
for (const char of "hello") console.log(char); // h, e, l, l, o
for (const [k, v] of new Map([["a", 1]])) console.log(k, v);
```

---

**Q33. What are WeakMap and WeakSet?**

```javascript
// WeakMap — keys must be objects, held weakly (GC can collect keys)
const cache = new WeakMap();

function processUser(user) {
  if (cache.has(user)) return cache.get(user);
  const result = expensiveOperation(user);
  cache.set(user, result);
  return result;
}

// When `user` object is garbage collected, WeakMap entry is automatically removed
// WeakMap cannot be iterated — no .keys(), .values(), .entries(), .size

// WeakSet — set of objects, held weakly
const seen = new WeakSet();

function process(obj) {
  if (seen.has(obj)) return; // already processed
  seen.add(obj);
  // ... process
}

// Key differences from Map/Set:
// - Keys/values must be objects (or registered symbols)
// - Entries are automatically removed when object is garbage collected
// - Cannot iterate — no size, no forEach
// - Use cases: private data, tracking DOM nodes, memoization without memory leaks

// WeakRef — weak reference to object
const ref = new WeakRef(someObject);
const obj = ref.deref(); // returns object OR undefined if GC'd
if (obj) { /* safe to use */ }
```

---

**Q34. What is the difference between `Map` and a plain object?**

```javascript
// Plain object:
const obj = {};
obj["key"] = "value";
// Keys must be strings or symbols — numbers are coerced to strings
obj[1] = "one";
Object.keys(obj); // ["1"] — coerced!
// Inherits from Object.prototype — prototype pollution risk
obj.constructor; // exists (from prototype)

// Map:
const map = new Map();
map.set(1, "one");     // any value as key
map.set({ id: 1 }, "user"); // object as key!
map.set(true, "bool");

map.get(1);    // "one"
map.size;      // 3 — O(1) size
map.has(true); // true

// Map maintains insertion order:
for (const [key, value] of map) {
  console.log(key, value);
}

// When to use Map over object:
// - Unknown/dynamic keys (avoids prototype pollution)
// - Non-string keys needed
// - Need size property
// - Need guaranteed insertion order
// - Frequent additions/deletions (Map is optimized for this)

// Converting:
const fromObj = new Map(Object.entries({ a: 1, b: 2 }));
const toObj = Object.fromEntries(map.entries()); // keys must be strings
```

---

**Q35. What is `JSON.stringify` and `JSON.parse` and their limitations?**

```javascript
// JSON.stringify — converts value to JSON string
JSON.stringify({ name: "Alice", age: 30 }); // '{"name":"Alice","age":30}'

// Values that are LOST or converted:
JSON.stringify({
  fn: function() {},    // undefined — functions omitted
  undef: undefined,     // undefined — omitted
  symbol: Symbol(),     // undefined — omitted
  nan: NaN,             // "null"
  inf: Infinity,        // "null"
  date: new Date(),     // "2024-01-01T..." — string, not Date
  map: new Map(),       // "{}" — empty object
  regex: /hello/,       // "{}" — empty object
});

// Circular references throw:
const obj = {};
obj.self = obj;
JSON.stringify(obj); // TypeError: cyclic object value

// Replacer and spacing:
JSON.stringify(obj, ["name", "age"], 2); // pretty print, only name/age
JSON.stringify(obj, (key, value) => {
  if (typeof value === "number") return value * 2;
  return value;
});

// JSON.parse — converts JSON string to value
const user = JSON.parse('{"name":"Alice"}'); // { name: "Alice" }

// Reviver:
JSON.parse('{"date":"2024-01-01"}', (key, value) => {
  if (key === "date") return new Date(value); // restore Date
  return value;
});
```

---

**Q36. What are iterators and iterables?**

```javascript
// Iterable — object with [Symbol.iterator]() method
// Iterator — object with next() method returning { value, done }

// Making a custom iterable:
class NumberRange {
  constructor(start, end) { this.start = start; this.end = end; }

  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    return {
      next() {
        if (current <= end) return { value: current++, done: false };
        return { value: undefined, done: true };
      },
      [Symbol.iterator]() { return this; } // iterator is also iterable
    };
  }
}

const range = new NumberRange(1, 5);
[...range];                    // [1, 2, 3, 4, 5] — spread works
for (const n of range) { }    // for...of works
const [first, second] = range; // destructuring works

// Built-in iterables: Array, String, Map, Set, arguments, NodeList, generators
```

---

**Q37. What are generators?**

```javascript
function* counter(start = 0) {
  while (true) {
    const reset = yield start++;
    if (reset) start = 0;
  }
}

const gen = counter(10);
gen.next();       // { value: 10, done: false }
gen.next();       // { value: 11, done: false }
gen.next(true);   // { value: 0, done: false } — reset passed in
gen.next();       // { value: 1, done: false }

// Finite generator:
function* range(start, end, step = 1) {
  for (let i = start; i < end; i += step) {
    yield i;
  }
}
[...range(0, 10, 2)]; // [0, 2, 4, 6, 8]

// Generator delegation with yield*:
function* innerGen() { yield "a"; yield "b"; }
function* outerGen() {
  yield 1;
  yield* innerGen(); // delegates to innerGen
  yield 2;
}
[...outerGen()]; // [1, "a", "b", 2]

// Infinite sequence (lazy evaluation):
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) { yield a; [a, b] = [b, a + b]; }
}
const fib = fibonacci();
Array.from({ length: 10 }, () => fib.next().value); // [0,1,1,2,3,5,8,13,21,34]
```

---

**Q38. What are the array methods you must know?**

```javascript
const nums = [1, 2, 3, 4, 5];

// Transformation:
nums.map(x => x * 2);          // [2,4,6,8,10] — new array
nums.filter(x => x % 2 === 0); // [2,4]         — new array
nums.reduce((acc, x) => acc + x, 0); // 15       — single value
nums.flatMap(x => [x, x * 2]); // [1,2,2,4,3,6,...] — map + flatten 1 level
[1,[2,[3]]].flat(Infinity);    // [1,2,3] — deep flatten

// Search:
nums.find(x => x > 3);        // 4 — first match
nums.findIndex(x => x > 3);   // 3 — index of first match
nums.some(x => x > 4);        // true — any match
nums.every(x => x > 0);       // true — all match
nums.includes(3);              // true
nums.indexOf(3);               // 2

// Mutation (modify in place):
nums.push(6);           // add to end, returns new length
nums.pop();             // remove from end, returns element
nums.unshift(0);        // add to start, returns new length
nums.shift();           // remove from start, returns element
nums.splice(1, 2, 99);  // remove 2 at index 1, insert 99
nums.reverse();         // in-place reverse
nums.sort((a, b) => a - b); // sort numerically (default sort is lexicographic!)

// Utility:
nums.slice(1, 3);  // [2,3] — non-mutating subset
nums.join(", ");   // "1, 2, 3, 4, 5"
Array.from({ length: 5 }, (_, i) => i); // [0,1,2,3,4]
Array.from(new Set([1,1,2,2,3]));       // [1,2,3] — deduplicate
```

---

**Q39. What is error handling in JavaScript?**

```javascript
// try/catch/finally:
function parseJSON(str) {
  try {
    return JSON.parse(str);
  } catch (err) {
    if (err instanceof SyntaxError) {
      console.error("Invalid JSON:", err.message);
      return null;
    }
    throw err; // re-throw unexpected errors
  } finally {
    console.log("always runs"); // cleanup, closes files, etc.
  }
}

// Custom error types:
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = "ValidationError";
    this.field = field;
  }
}

class NetworkError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.name = "NetworkError";
    this.statusCode = statusCode;
  }
}

try {
  throw new ValidationError("Invalid email", "email");
} catch (err) {
  if (err instanceof ValidationError) {
    console.log(err.field); // "email"
  } else if (err instanceof NetworkError) {
    console.log(err.statusCode);
  } else {
    throw err; // unknown error
  }
}

// Async error handling:
async function fetchData() {
  try {
    const res = await fetch("/api");
    if (!res.ok) throw new NetworkError("Request failed", res.status);
    return await res.json();
  } catch (err) {
    // handles both fetch errors and NetworkError
    console.error(err);
  }
}
```

---

**Q40. What are the most important `String` methods?**

```javascript
const str = "Hello, World!";

// Search:
str.includes("World");      // true
str.startsWith("Hello");    // true
str.endsWith("!");          // true
str.indexOf("o");           // 4 (first occurrence)
str.lastIndexOf("o");       // 8 (last occurrence)
str.search(/world/i);       // 7 — regex search, returns index

// Transform:
str.toUpperCase();          // "HELLO, WORLD!"
str.toLowerCase();          // "hello, world!"
str.trim();                 // removes leading/trailing whitespace
str.trimStart();            // remove from start only
str.trimEnd();              // remove from end only
str.replace("World", "JS"); // "Hello, JS!" — first match
str.replaceAll("l", "L");   // "HeLLo, WorLd!"
str.slice(7, 12);           // "World"
str.substring(7, 12);       // "World"

// Split/Join:
"a,b,c".split(",");         // ["a", "b", "c"]
["a","b","c"].join("-");    // "a-b-c"

// Padding and repeat:
"5".padStart(3, "0");      // "005"
"hi".padEnd(5, ".");       // "hi..."
"ha".repeat(3);            // "hahaha"

// Regular expressions:
"cat bat sat".match(/[a-z]at/g);          // ["cat", "bat", "sat"]
"hello".matchAll(/l/g);                    // iterator of all matches
"hello world".replace(/(\w+)/g, "[$1]"); // "[hello] [world]"
```

---

## MEDIUM QUESTIONS

---

**Q41. Explain the event loop in detail — macrotasks vs microtasks.**

The event loop runs in phases. After each macrotask, ALL pending microtasks are drained before the next macrotask runs.

```javascript
// Execution order:
// 1. Synchronous code (call stack)
// 2. Microtask queue drains completely (Promises, queueMicrotask, MutationObserver)
// 3. One macrotask executes (setTimeout, setInterval, I/O)
// 4. Microtask queue drains again
// 5. Repeat

console.log("1");                            // sync

setTimeout(() => console.log("2"), 0);       // macrotask queue

Promise.resolve()
  .then(() => {
    console.log("3");                        // microtask
    setTimeout(() => console.log("4"), 0);  // schedules another macrotask
    return Promise.resolve();
  })
  .then(() => console.log("5"));             // microtask (after "3" microtask)

queueMicrotask(() => console.log("6"));      // microtask

console.log("7");                            // sync

// Output: 1, 7, 3, 6, 5, 2, 4
// Breakdown:
// Sync: 1, 7
// Microtasks: 3, then schedules macrotask "4", then 6, then 5 (chained)
// Macrotask: 2
// Microtasks: (empty)
// Macrotask: 4
```

---

**Q42. What is debouncing and throttling?**

Both control how often a function executes. Debouncing delays execution until after a quiet period. Throttling limits execution to at most once per time period.

```javascript
// Debounce — waits for N ms of inactivity then fires once
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

const search = debounce((query) => {
  fetch(`/api/search?q=${query}`);
}, 300);

input.addEventListener("input", e => search(e.target.value));
// Only fires 300ms after user stops typing

// Throttle — fires at most once per N ms
function throttle(fn, limit) {
  let lastRun = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastRun >= limit) {
      lastRun = now;
      return fn.apply(this, args);
    }
  };
}

const onScroll = throttle(() => {
  updateScrollIndicator();
}, 16); // ~60fps

window.addEventListener("scroll", onScroll);
// Fires at most every 16ms regardless of scroll events per second
```

---

**Q43. Explain prototypal inheritance vs classical inheritance.**

```javascript
// Classical inheritance (Java/C++ style) — classes create objects
// Prototypal inheritance (JavaScript) — objects inherit from objects

// Prototypal — differential inheritance
const vehicleProto = {
  start() { return `${this.type} engine starting`; },
  stop() { return `${this.type} engine stopping`; },
};

const carProto = Object.create(vehicleProto);
carProto.honk = function() { return "beep!"; };

function createCar(type, model) {
  const car = Object.create(carProto);
  car.type = type;
  car.model = model;
  return car;
}

const myCar = createCar("gasoline", "Toyota");
myCar.start(); // "gasoline engine starting" — found via prototype chain
myCar.honk();  // "beep!" — found on carProto

// Prototype chain: myCar → carProto → vehicleProto → Object.prototype → null

// ES6 class syntax — still prototypal underneath:
class Vehicle {
  constructor(type) { this.type = type; }
  start() { return `${this.type} starting`; }
}

class Car extends Vehicle {
  honk() { return "beep!"; }
}

// typeof Car === "function" — class IS a function
// Car.prototype.honk — method lives on prototype, shared by all instances
// NOT copied to each instance (memory-efficient)
```

---

**Q44. What is memoization?**

```javascript
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Example: expensive Fibonacci without memoization is O(2^n)
function fib(n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

const memoFib = memoize(function fib(n) {
  if (n <= 1) return n;
  return memoFib(n - 1) + memoFib(n - 2); // call memoized version
});

memoFib(40); // fast — O(n) with memoization

// Memoization is only correct for pure functions (same input → same output)
// WeakMap-based memoization for object args (prevents memory leaks):
function memoizeWeak(fn) {
  const cache = new WeakMap();
  return function(obj) { // single object argument
    if (cache.has(obj)) return cache.get(obj);
    const result = fn(obj);
    cache.set(obj, result);
    return result;
  };
}
```

---

**Q45. What is currying?**

```javascript
// Currying transforms f(a,b,c) into f(a)(b)(c)

// Manual curry:
const add = a => b => c => a + b + c;
add(1)(2)(3); // 6
const add1 = add(1);     // partially applied
const add1and2 = add1(2); // partially applied
add1and2(3);              // 6

// General curry function:
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...more) {
      return curried.apply(this, args.concat(more));
    };
  };
}

const multiply = curry((a, b, c) => a * b * c);
multiply(2)(3)(4);    // 24
multiply(2, 3)(4);    // 24
multiply(2)(3, 4);    // 24
multiply(2, 3, 4);    // 24

// Real-world use — reusable, configurable functions:
const formatCurrency = curry((symbol, decimals, amount) =>
  `${symbol}${amount.toFixed(decimals)}`
);

const formatUSD = formatCurrency("$", 2);
const formatEUR = formatCurrency("€", 2);

formatUSD(19.99);  // "$19.99"
formatEUR(19.99);  // "€19.99"
```

---

**Q46. What is function composition?**

```javascript
// Compose: right-to-left application
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

// Pipe: left-to-right application (more readable)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const double = x => x * 2;
const addOne = x => x + 1;
const square = x => x ** 2;

const transform = pipe(double, addOne, square);
transform(3); // square(addOne(double(3))) = square(addOne(6)) = square(7) = 49

// Real-world pipeline:
const processUser = pipe(
  user => ({ ...user, email: user.email.toLowerCase() }),
  user => ({ ...user, name: user.name.trim() }),
  user => ({ ...user, createdAt: new Date() }),
  user => ({ ...user, role: user.role ?? "user" }),
);

processUser({ name: "  Alice  ", email: "ALICE@EXAMPLE.COM" });
// { name: "Alice", email: "alice@example.com", createdAt: Date, role: "user" }
```

---

**Q47. What is the difference between shallow copy and deep copy?**

```javascript
const original = {
  name: "Alice",
  address: { city: "Cairo", zip: "11511" },
  hobbies: ["reading", "coding"],
};

// SHALLOW COPY — top-level properties are copied, nested objects are referenced

// Method 1: spread
const shallow1 = { ...original };

// Method 2: Object.assign
const shallow2 = Object.assign({}, original);

shallow1.name = "Bob";              // doesn't affect original ✅
shallow1.address.city = "Alex";     // AFFECTS original ❌ (same reference)
shallow1.hobbies.push("gaming");    // AFFECTS original ❌ (same reference)

// DEEP COPY — everything is copied recursively

// Method 1: structuredClone (modern, native, handles many types)
const deep1 = structuredClone(original);
deep1.address.city = "Giza"; // doesn't affect original ✅

// Method 2: JSON round-trip (loses functions, undefined, dates become strings)
const deep2 = JSON.parse(JSON.stringify(original));

// Method 3: Custom recursive deep clone
function deepClone(value) {
  if (value === null || typeof value !== "object") return value;
  if (Array.isArray(value)) return value.map(deepClone);
  if (value instanceof Date) return new Date(value);
  if (value instanceof Map) return new Map([...value].map(([k,v]) => [deepClone(k), deepClone(v)]));
  return Object.fromEntries(Object.entries(value).map(([k,v]) => [k, deepClone(v)]));
}
```

---

**Q48. How does garbage collection work in JavaScript?**

```javascript
// V8 uses generational garbage collection:
// - NEW SPACE (Minor GC / Scavenger): short-lived objects, fast collection
// - OLD SPACE (Major GC / Mark-Sweep-Compact): survived objects, less frequent

// MARK AND SWEEP algorithm:
// 1. Mark phase: start from GC roots (global, stack frames), mark all reachable objects
// 2. Sweep phase: collect unmarked (unreachable) objects
// 3. Compact phase: defragment memory (optional)

// GC roots: global variables, current call stack, closures keeping references

// Memory leaks in JavaScript:
// 1. Accidental global variables:
function leak() { x = "I leak!"; } // no var/let/const — becomes global

// 2. Forgotten event listeners:
const el = document.getElementById("btn");
el.addEventListener("click", handler);
// If el is removed from DOM but handler still holds reference:
el.remove(); // DOM removed but listener keeps el alive
// Fix:
el.removeEventListener("click", handler);

// 3. Closures holding large data:
function createLeak() {
  const bigData = new Array(1000000).fill("data");
  return function() {
    console.log(bigData[0]); // bigData kept alive by closure
  };
}

// 4. Timers and intervals:
const timer = setInterval(() => {
  // holds reference to data
}, 1000);
// Fix:
clearInterval(timer); // when done

// 5. Caches without eviction:
const cache = {};
function memoize(fn) {
  return (key) => {
    cache[key] = cache[key] ?? fn(key); // grows forever
    return cache[key];
  };
}
// Fix: use WeakMap or LRU cache with size limit
```

---

**Q49. What is the module pattern and why was it used?**

```javascript
// Before ES modules, the Module Pattern provided encapsulation via closures:

const UserModule = (function() {
  // Private state
  let users = [];
  let nextId = 1;

  // Private function
  function validateUser(user) {
    return user.name && user.email;
  }

  // Public API (returned object)
  return {
    add(user) {
      if (!validateUser(user)) throw new Error("Invalid user");
      users.push({ ...user, id: nextId++ });
    },
    getAll() { return [...users]; }, // return copy
    find(id) { return users.find(u => u.id === id); },
    remove(id) { users = users.filter(u => u.id !== id); },
  };
})(); // IIFE — immediately invoked

UserModule.add({ name: "Alice", email: "alice@example.com" });
UserModule.getAll(); // [{ name: "Alice", email: "...", id: 1 }]
UserModule.users;    // undefined — private!

// Revealing Module Pattern (cleaner):
const CounterModule = (function() {
  let count = 0;
  const increment = () => ++count;
  const decrement = () => --count;
  const reset = () => { count = 0; };
  const value = () => count;

  return { increment, decrement, reset, value };
})();
```

---

**Q50. What is the Observer pattern in JavaScript?**

```javascript
class EventEmitter {
  #events = new Map();

  on(event, listener) {
    if (!this.#events.has(event)) this.#events.set(event, new Set());
    this.#events.get(event).add(listener);
    return this; // chainable
  }

  once(event, listener) {
    const wrapper = (...args) => {
      listener(...args);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }

  off(event, listener) {
    this.#events.get(event)?.delete(listener);
    return this;
  }

  emit(event, ...args) {
    this.#events.get(event)?.forEach(listener => {
      try { listener(...args); }
      catch (err) { console.error(`Error in ${event} listener:`, err); }
    });
    return this;
  }
}

// Usage:
class Store extends EventEmitter {
  #state;
  constructor(initial) { super(); this.#state = initial; }
  setState(update) {
    this.#state = { ...this.#state, ...update };
    this.emit("change", this.#state);
  }
  getState() { return this.#state; }
}

const store = new Store({ count: 0 });
store.on("change", state => console.log("State:", state));
store.setState({ count: 1 }); // "State: { count: 1 }"
```

---

**Q51. What is the Proxy object?**

```javascript
// Proxy intercepts fundamental operations on objects

const handler = {
  get(target, prop, receiver) {
    if (prop in target) return Reflect.get(target, prop, receiver);
    throw new ReferenceError(`Property "${prop}" does not exist`);
  },

  set(target, prop, value, receiver) {
    if (prop === "age" && typeof value !== "number") {
      throw new TypeError("Age must be a number");
    }
    return Reflect.set(target, prop, value, receiver);
  },

  deleteProperty(target, prop) {
    if (prop === "id") throw new Error("Cannot delete id");
    return Reflect.deleteProperty(target, prop);
  },

  has(target, prop) {
    return prop in target;
  }
};

const user = new Proxy({ id: 1, name: "Alice", age: 30 }, handler);
user.name;         // "Alice"
user.missing;      // ReferenceError: Property "missing" does not exist
user.age = "old";  // TypeError: Age must be a number
user.age = 31;     // OK
delete user.id;    // Error: Cannot delete id

// Reactive data with Proxy (like Vue 3's reactivity):
function reactive(obj) {
  return new Proxy(obj, {
    set(target, key, value) {
      Reflect.set(target, key, value);
      console.log(`${key} changed to ${value}`);
      return true;
    }
  });
}

const state = reactive({ count: 0 });
state.count = 1; // "count changed to 1"
```

---

**Q52. What is `Reflect` and how does it relate to `Proxy`?**

```javascript
// Reflect provides static methods matching Proxy trap names
// It provides the default behavior for Proxy traps

// Without Reflect (fragile):
const proxy = new Proxy(obj, {
  get(target, prop) {
    // return target[prop]; // breaks if target uses getters with `this`
    return Reflect.get(target, prop, receiver); // ✅ correct
  }
});

// All Reflect methods:
Reflect.get(target, prop, receiver);       // target[prop]
Reflect.set(target, prop, value, receiver); // target[prop] = value
Reflect.has(target, prop);                 // prop in target
Reflect.deleteProperty(target, prop);      // delete target[prop]
Reflect.ownKeys(target);                   // Object.getOwnPropertyNames + Symbols
Reflect.apply(fn, thisArg, args);          // fn.apply(thisArg, args)
Reflect.construct(Target, args, newTarget); // new Target(...args)
Reflect.defineProperty(target, prop, desc);
Reflect.getPrototypeOf(target);
Reflect.setPrototypeOf(target, proto);

// Why use Reflect over direct operations?
// 1. Returns boolean success instead of throwing (set, deleteProperty)
// 2. Preserves receiver for correct getter/setter behavior
// 3. Consistent API mirroring Proxy traps
// 4. Proper handling of non-writable properties
```

---

**Q53. Explain `Promise` internals — how does `.then()` work?**

```javascript
// Simplified Promise implementation:
class MyPromise {
  #state = "pending";
  #value = undefined;
  #callbacks = [];

  constructor(executor) {
    const resolve = (value) => {
      if (this.#state !== "pending") return;
      this.#state = "fulfilled";
      this.#value = value;
      // Schedule callbacks as microtasks (not synchronous!)
      queueMicrotask(() => this.#callbacks.forEach(cb => cb.onFulfilled?.(value)));
    };

    const reject = (reason) => {
      if (this.#state !== "pending") return;
      this.#state = "rejected";
      this.#value = reason;
      queueMicrotask(() => this.#callbacks.forEach(cb => cb.onRejected?.(reason)));
    };

    try { executor(resolve, reject); }
    catch(err) { reject(err); }
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handleFulfilled = (value) => {
        try {
          const result = onFulfilled ? onFulfilled(value) : value;
          if (result instanceof MyPromise) result.then(resolve, reject);
          else resolve(result);
        } catch(err) { reject(err); }
      };

      if (this.#state === "fulfilled") queueMicrotask(() => handleFulfilled(this.#value));
      else if (this.#state === "pending") this.#callbacks.push({ onFulfilled: handleFulfilled, onRejected });
    });
  }

  catch(onRejected) { return this.then(undefined, onRejected); }
}
```

---

**Q54. What is the difference between `setTimeout(fn, 0)` and `Promise.resolve().then(fn)`?**

```javascript
// setTimeout(fn, 0) — schedules fn as a MACROTASK
// Promise.resolve().then(fn) — schedules fn as a MICROTASK

// Microtasks always run before the next macrotask

setTimeout(() => console.log("macrotask"), 0);
Promise.resolve().then(() => console.log("microtask"));

// Output: "microtask", then "macrotask"

// This matters when you need something to run "after current code but before rendering":

// Rendering happens between macrotasks in browsers
// Microtasks block rendering (careful with long microtask chains!)

// Starvation example:
function recursiveMicrotask() {
  Promise.resolve().then(recursiveMicrotask); // infinite microtask chain
}
// This will block the browser FOREVER — microtasks never let macrotasks (rendering) run

// Use setImmediate (Node), setTimeout, or requestAnimationFrame for macrotask scheduling
```

---

**Q55. What are `async` generators?**

```javascript
// Async generators combine async/await with generators
// They produce values asynchronously, consumed with for await...of

async function* fetchPages(baseUrl) {
  let page = 1;
  while (true) {
    const res = await fetch(`${baseUrl}?page=${page}`);
    const data = await res.json();
    if (data.items.length === 0) return;
    yield data.items;
    page++;
  }
}

// Consuming:
async function loadAll(url) {
  const allItems = [];
  for await (const items of fetchPages(url)) {
    allItems.push(...items);
    if (allItems.length >= 100) break; // early exit
  }
  return allItems;
}

// Async generator with transform:
async function* map(iterable, fn) {
  for await (const item of iterable) {
    yield await fn(item);
  }
}

async function* filter(iterable, pred) {
  for await (const item of iterable) {
    if (await pred(item)) yield item;
  }
}

// Pipeline:
const activeUsers = filter(
  fetchPages("/api/users"),
  async (users) => users.filter(u => u.active)
);
```

---

**Q56. What is the difference between `Object.freeze()`, `Object.seal()`, and `Object.preventExtensions()`?**

```javascript
// Object.preventExtensions — cannot ADD properties, can modify/delete existing
const obj1 = Object.preventExtensions({ a: 1, b: 2 });
obj1.c = 3;      // silently fails (TypeError in strict mode)
obj1.a = 10;     // OK ✅
delete obj1.b;   // OK ✅

// Object.seal — cannot ADD or DELETE properties, can modify values
const obj2 = Object.seal({ a: 1, b: 2 });
obj2.c = 3;      // fails silently
delete obj2.a;   // fails silently
obj2.b = 99;     // OK ✅ — value still mutable

// Object.freeze — cannot ADD, DELETE, or MODIFY (shallow!)
const obj3 = Object.freeze({ a: 1, nested: { x: 1 } });
obj3.a = 10;          // fails silently (TypeError in strict mode)
obj3.nested.x = 99;   // OK ❌ — freeze is SHALLOW!

// Deep freeze:
function deepFreeze(obj) {
  Object.getOwnPropertyNames(obj).forEach(name => {
    const value = obj[name];
    if (typeof value === "object" && value !== null) deepFreeze(value);
  });
  return Object.freeze(obj);
}

// Check status:
Object.isFrozen(obj3);       // true
Object.isSealed(obj2);       // true
Object.isExtensible(obj1);   // false
```

---

**Q57. Explain `Object.defineProperty()` and property descriptors.**

```javascript
// Every property has a descriptor with these attributes:
// value, writable, enumerable, configurable
// (or get/set for accessor properties)

const obj = {};

Object.defineProperty(obj, "id", {
  value: 1,
  writable: false,      // cannot reassign
  enumerable: false,    // hidden from for...in, Object.keys
  configurable: false,  // cannot delete or redefine
});

obj.id = 2;         // silently fails (TypeError in strict mode)
"id" in obj;        // true — `in` ignores enumerable
Object.keys(obj);   // [] — enumerable: false hides it
delete obj.id;      // fails — configurable: false

// Accessor descriptor:
let _name = "Alice";
Object.defineProperty(obj, "name", {
  get() { return _name; },
  set(value) {
    if (typeof value !== "string") throw new TypeError();
    _name = value;
  },
  enumerable: true,
  configurable: true,
});

// Define multiple properties:
Object.defineProperties(obj, {
  x: { value: 1, writable: true, enumerable: true, configurable: true },
  y: { value: 2, writable: true, enumerable: true, configurable: true },
});

// Inspect descriptor:
Object.getOwnPropertyDescriptor(obj, "id");
// { value: 1, writable: false, enumerable: false, configurable: false }
```

---

**Q58. What are the different ways to handle asynchronous code and their tradeoffs?**

```javascript
// 1. Callbacks — oldest pattern
fs.readFile("file.txt", (err, data) => {
  if (err) return handleError(err);
  processData(data, (err, result) => {
    if (err) return handleError(err);
    saveResult(result, (err) => { // Callback Hell / Pyramid of Doom
      if (err) return handleError(err);
    });
  });
});
// Cons: deeply nested, hard to handle errors, no return values

// 2. Promises — flat chaining
readFile("file.txt")
  .then(processData)
  .then(saveResult)
  .catch(handleError);
// Pros: flat, error propagation, composable
// Cons: slightly verbose, harder to use with loops

// 3. Async/Await — synchronous style
async function run() {
  try {
    const data = await readFile("file.txt");
    const result = await processData(data);
    await saveResult(result);
  } catch (err) {
    handleError(err);
  }
}
// Pros: most readable, easy error handling, easy loops
// Cons: need to remember parallel execution

// 4. Observables (RxJS) — stream of events
from(readFile$("file.txt")).pipe(
  switchMap(processData$),
  switchMap(saveResult$),
  catchError(handleError$)
).subscribe();
// Pros: cancellable, composable operators, handles multiple values
// Cons: steep learning curve, heavy dependency
```

---

**Q59. What is `AbortController` and when do you use it?**

```javascript
// AbortController allows you to cancel fetch requests and other async operations

async function fetchWithTimeout(url, timeoutMs) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    return await res.json();
  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error(`Request to ${url} timed out after ${timeoutMs}ms`);
    }
    throw err;
  }
}

// Cancel multiple requests when component unmounts (React pattern):
function useData(url) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then(r => r.json())
      .then(setData)
      .catch(err => {
        if (err.name !== "AbortError") console.error(err);
      });

    return () => controller.abort(); // cleanup on unmount
  }, [url]);

  return data;
}

// AbortSignal.any() — abort when any of multiple signals fires
const combinedSignal = AbortSignal.any([timeoutSignal, userCancelSignal]);

// AbortSignal.timeout() — built-in timeout signal
fetch(url, { signal: AbortSignal.timeout(5000) });
```

---

**Q60. What is the `Structured Clone Algorithm`?**

```javascript
// structuredClone() uses the Structured Clone Algorithm for deep copying

// What it CAN clone:
structuredClone({
  arr: [1, 2, 3],
  date: new Date(),
  map: new Map([["a", 1]]),
  set: new Set([1, 2, 3]),
  typed: new Uint8Array([1, 2, 3]),
  regexp: /hello/gi,
  error: new Error("oops"),
  nested: { deeply: { nested: true } },
});

// What it CANNOT clone (throws DataCloneError):
// - Functions
// - DOM nodes
// - Symbols (as values, not keys)
// - WeakMap, WeakSet, WeakRef
// - Getters/setters (loses them, copies value only)

// Circular references are handled:
const circular = {};
circular.self = circular;
const cloned = structuredClone(circular);
cloned.self === cloned; // true ✅

// Transfer ownership (moves, doesn't copy — zero-copy transfer):
const buffer = new ArrayBuffer(1024);
const transferred = structuredClone(buffer, { transfer: [buffer] });
// buffer is now detached (zero-length), transferred has the data
```

---

**Q61. What are Symbols used for in practice?**

```javascript
// 1. Unique property keys (avoid naming collisions in libraries):
const PRIVATE_KEY = Symbol("privateData");
const lib1Key = Symbol("data");
const lib2Key = Symbol("data"); // different from lib1Key!

// 2. Well-known symbols (protocol hooks):
class SmartArray {
  constructor(...items) { this.items = items; }

  // Make custom class work with +
  [Symbol.toPrimitive](hint) {
    if (hint === "number") return this.items.length;
    if (hint === "string") return this.items.join(", ");
    return this.items.length; // default
  }

  // Change instanceof behavior:
  static [Symbol.hasInstance](instance) {
    return Array.isArray(instance?.items);
  }

  // Change Object.prototype.toString.call result:
  get [Symbol.toStringTag]() { return "SmartArray"; }

  // Make iterable:
  [Symbol.iterator]() { return this.items.values(); }
}

const sa = new SmartArray(1, 2, 3);
+sa;                // 3 (hint: "number")
`${sa}`;            // "1, 2, 3" (hint: "string")
[...sa];            // [1, 2, 3]
Object.prototype.toString.call(sa); // "[object SmartArray]"

// 3. Enum-like constants:
const Direction = Object.freeze({
  UP: Symbol("UP"),
  DOWN: Symbol("DOWN"),
  LEFT: Symbol("LEFT"),
  RIGHT: Symbol("RIGHT"),
});
Direction.UP === Direction.UP; // true
Direction.UP === Symbol("UP"); // false — unique!
```

---

**Q62. What is `Object.keys()` vs `Object.values()` vs `Object.entries()` vs `Object.fromEntries()`?**

```javascript
const obj = { a: 1, b: 2, c: 3 };

Object.keys(obj);    // ["a", "b", "c"] — string keys
Object.values(obj);  // [1, 2, 3]       — values
Object.entries(obj); // [["a",1],["b",2],["c",3]] — pairs

// All three: only own enumerable string-keyed properties
// Symbols are excluded, inherited properties excluded

// Object.fromEntries — inverse of Object.entries
Object.fromEntries([["a",1],["b",2]]); // { a: 1, b: 2 }

// Power pattern — transform object values:
const doubled = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2])
);
// { a: 2, b: 4, c: 6 }

// Filter object properties:
const onlyEven = Object.fromEntries(
  Object.entries(obj).filter(([, v]) => v % 2 === 0)
);
// { b: 2 }

// Works with any iterable of [key, value] pairs:
Object.fromEntries(new Map([["x", 1], ["y", 2]]));
// { x: 1, y: 2 }
```

---

**Q63. What are the different ways to create objects in JavaScript?**

```javascript
// 1. Object literal
const obj1 = { name: "Alice", greet() { return `Hi, ${this.name}`; } };

// 2. Constructor function
function Person(name) { this.name = name; }
Person.prototype.greet = function() { return `Hi, ${this.name}`; };
const obj2 = new Person("Bob");

// 3. Object.create()
const proto = { greet() { return `Hi, ${this.name}`; } };
const obj3 = Object.create(proto);
obj3.name = "Carol";

// 4. ES6 Class
class PersonClass {
  constructor(name) { this.name = name; }
  greet() { return `Hi, ${this.name}`; }
}
const obj4 = new PersonClass("Dave");

// 5. Factory function (preferred for encapsulation without classes)
function createPerson(name) {
  let _privateData = "secret";
  return {
    name,
    greet() { return `Hi, ${this.name}`; },
    getPrivate() { return _privateData; },
  };
}
const obj5 = createPerson("Eve");

// 6. Object.assign()
const obj6 = Object.assign({}, defaults, overrides);

// 7. Proxy-based
const obj7 = new Proxy({}, handler);

// Trade-offs:
// Literal: simple, no shared prototype methods (but usually fine)
// Class/Constructor: shared methods via prototype, supports instanceof
// Factory: true privacy via closure, no `new` required, composition-friendly
// Object.create: explicit prototype chain
```

---

**Q64. What is tail call optimization (TCO)?**

```javascript
// A tail call is a function call that is the LAST operation in a function
// TCO allows the engine to reuse the current stack frame — prevents stack overflow

// NOT tail call (need to return, then multiply):
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1); // can't reuse frame — must remember `n`
}
factorial(100000); // Stack overflow!

// Tail call (accumulator pattern):
function factorial(n, acc = 1) {
  if (n <= 1) return acc;
  return factorial(n - 1, n * acc); // tail position — nothing to do after
}
// Engine can reuse the stack frame — constant stack space

// TCO status in JS engines:
// - Specified in ES6 strict mode
// - Only Safari/JSC implements it
// - V8 (Chrome/Node) never implemented it (removed after backlash)
// - In practice: use iterative solutions for large recursion:
function factorialIterative(n) {
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}

// Trampoline — manual TCO for any engine:
function trampoline(fn) {
  return function(...args) {
    let result = fn(...args);
    while (typeof result === "function") result = result();
    return result;
  };
}

const safeFact = trampoline(function fact(n, acc = 1) {
  if (n <= 1) return acc;
  return () => fact(n - 1, n * acc); // return thunk instead of recursing
});
safeFact(100000); // works!
```

---

**Q65. What is the `with` statement and why is it forbidden in strict mode?**

```javascript
// `with` adds an object to the scope chain
const obj = { a: 1, b: 2, c: 3 };
with (obj) {
  console.log(a + b + c); // 6 — reads from obj
}

// Why it's dangerous:
const Math = { sin: () => "fake" };
with (Math) {
  sin(0); // "fake" or real Math.sin? Ambiguous!
}

// Optimisation killer: JS engine can't determine at parse time
// whether `a` refers to local var or `with` object property
// So it can't optimize the function at all

// Strict mode:
"use strict";
with (obj) {} // SyntaxError — `with` is forbidden in strict mode

// Module code is always strict — `with` never works in modules
// The only valid use was namespacing (now solved by modules)
```

---

**Q66. What is the difference between `for await...of` and `Promise.all`?**

```javascript
// Promise.all — parallel, fails fast on first rejection
async function parallel(urls) {
  const results = await Promise.all(urls.map(url => fetch(url).then(r => r.json())));
  // All requests start simultaneously — total time = slowest request
  return results;
}

// for await...of — sequential, one after another
async function sequential(urls) {
  const results = [];
  for (const url of urls) {
    const data = await fetch(url).then(r => r.json());
    results.push(data); // each request waits for the previous
  }
  return results;
  // Total time = sum of all request times (much slower!)
}

// for await...of with async iterable — correct use case
async function processStream(asyncIterable) {
  for await (const chunk of asyncIterable) {
    processChunk(chunk); // process as items arrive
  }
}

// Controlled concurrency (N at a time):
async function batchRequests(urls, concurrency = 3) {
  const results = [];
  for (let i = 0; i < urls.length; i += concurrency) {
    const batch = urls.slice(i, i + concurrency);
    const batchResults = await Promise.all(batch.map(fetch));
    results.push(...batchResults);
  }
  return results;
}
```

---

**Q67. What are labeled statements in JavaScript?**

```javascript
// Labels allow breaking/continuing specific outer loops

outer: for (let i = 0; i < 5; i++) {
  for (let j = 0; j < 5; j++) {
    if (j === 2) continue outer; // skip to next iteration of outer loop
    if (i === 3) break outer;    // exit the outer loop entirely
    console.log(i, j);
  }
}

// Without labels you'd need flags:
let shouldBreak = false;
for (let i = 0; i < 5 && !shouldBreak; i++) {
  for (let j = 0; j < 5; j++) {
    if (condition) { shouldBreak = true; break; }
  }
}

// Labels are rarely used and considered code smell
// Better approach: extract to function and use return
function findPair(matrix) {
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      if (matrix[i][j] === target) return [i, j]; // clean exit
    }
  }
  return null;
}
```

---

**Q68. What is `globalThis` and why was it introduced?**

```javascript
// Before globalThis, accessing the global object was environment-specific:
// - Browser main thread: window, self, frames
// - Browser worker: self
// - Node.js: global
// - New Function("return this")() — worked everywhere (but not in strict modules)

// globalThis — universal access to global object (ES2020)
globalThis.setTimeout === window.setTimeout; // true in browsers
globalThis.process === process;              // true in Node.js

// Use case: write code that works in any environment
if (typeof globalThis.fetch === "undefined") {
  globalThis.fetch = require("node-fetch"); // polyfill
}

// Checking environment:
const isBrowser = typeof globalThis.window !== "undefined";
const isNode = typeof globalThis.process !== "undefined" && process.versions?.node;
const isWorker = typeof globalThis.WorkerGlobalScope !== "undefined";
```

---

**Q69. What are `ArrayBuffer`, `TypedArray`, and `DataView`?**

```javascript
// ArrayBuffer — raw binary data, fixed-size buffer
const buffer = new ArrayBuffer(16); // 16 bytes

// TypedArrays — typed views into ArrayBuffer
const int32 = new Int32Array(buffer);    // 4 elements (4 bytes each)
const uint8 = new Uint8Array(buffer);    // 16 elements (1 byte each)
const float64 = new Float64Array(buffer); // 2 elements (8 bytes each)

int32[0] = 42;
uint8[0]; // 42 (same underlying buffer!)

// DataView — fine-grained control over byte order (endianness)
const view = new DataView(buffer);
view.setInt32(0, 42, true);   // little-endian
view.setInt32(4, -1, false);  // big-endian
view.getInt32(0, true);       // 42

// Real-world uses:
// - WebGL (passing vertex data to GPU)
// - WebSockets (binary protocols)
// - File parsing (binary formats: BMP, WAV, ZIP)
// - Crypto APIs
// - WASM memory

// Example: Parse BMP header
const bmp = new DataView(arrayBuffer);
const signature = String.fromCharCode(bmp.getUint8(0), bmp.getUint8(1));
if (signature !== "BM") throw new Error("Not a BMP");
const fileSize = bmp.getUint32(2, true); // little-endian
const pixelOffset = bmp.getUint32(10, true);
```

---

**Q70. What is `structuredClone` vs `JSON.parse(JSON.stringify())`?**

```javascript
// Detailed comparison:

const complex = {
  date: new Date("2024-01-01"),
  regex: /hello/gi,
  map: new Map([["a", 1]]),
  set: new Set([1, 2, 3]),
  circular: null,
  undef: undefined,
  fn: function() {},
  typed: new Uint8Array([1, 2, 3]),
};
complex.circular = complex;

// JSON.parse(JSON.stringify(complex)):
// ❌ date → string "2024-01-01T00:00:00.000Z" (not Date object)
// ❌ regex → {} (empty object)
// ❌ map → {} (empty object)
// ❌ set → {} (empty object)
// ❌ circular → TypeError: circular structure
// ❌ undef → omitted entirely
// ❌ fn → omitted entirely
// ❌ typed → { "0": 1, "1": 2, "2": 3 }
// ✅ nested objects and arrays work

// structuredClone(complex):
// ✅ date → new Date object
// ✅ regex → /hello/gi (cloned)
// ✅ map → new Map (cloned)
// ✅ set → new Set (cloned)
// ✅ circular → handled correctly
// ❌ undef properties → cloned
// ❌ fn → DataCloneError (throws!)
// ✅ typed → new Uint8Array

// Performance: structuredClone is generally faster than JSON round-trip
// for complex objects (no serialization to string)
```

---

**Q71. What is the `in` operator vs `hasOwnProperty` vs `Object.hasOwn()`?**

```javascript
const parent = { inherited: true };
const child = Object.create(parent);
child.own = true;

// `in` — checks own AND inherited properties
"own" in child;        // true
"inherited" in child;  // true — found in prototype chain
"toString" in child;   // true — found in Object.prototype

// hasOwnProperty — checks own properties only
child.hasOwnProperty("own");        // true
child.hasOwnProperty("inherited");  // false
child.hasOwnProperty("toString");   // false

// Problem: hasOwnProperty can be overridden or unavailable
const obj = Object.create(null); // no prototype!
obj.key = "value";
obj.hasOwnProperty("key"); // TypeError: obj.hasOwnProperty is not a function!
// Fix: Object.prototype.hasOwnProperty.call(obj, "key") — verbose

// Object.hasOwn() — ES2022, modern replacement
Object.hasOwn(child, "own");        // true  ✅
Object.hasOwn(child, "inherited");  // false ✅
Object.hasOwn(obj, "key");         // true  ✅ — works with null-prototype objects

// Always prefer Object.hasOwn() over hasOwnProperty in modern code
```

---

**Q72. What is `requestAnimationFrame` and how does it differ from `setTimeout`?**

```javascript
// setTimeout/setInterval — not synchronized with display refresh
// Can run between frames (wasted work) or multiple times per frame (janky)

// requestAnimationFrame — runs just before the browser repaints
// Synchronized to display refresh rate (~60fps = every 16.67ms)
// Pauses when tab is hidden (saves battery/CPU)

// Animation with rAF:
function animate(element, targetX, duration) {
  const startX = element.offsetLeft;
  const startTime = performance.now();

  function step(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Easing function:
    const eased = progress < 0.5
      ? 2 * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 2) / 2;

    element.style.left = `${startX + (targetX - startX) * eased}px`;

    if (progress < 1) {
      requestAnimationFrame(step); // schedule next frame
    }
  }

  requestAnimationFrame(step); // start
}

// Cancel animation:
const frameId = requestAnimationFrame(step);
cancelAnimationFrame(frameId);

// Measure real frame rate:
let lastTime = 0;
let frameCount = 0;
function measureFPS(time) {
  frameCount++;
  if (time - lastTime >= 1000) {
    console.log(`FPS: ${frameCount}`);
    frameCount = 0;
    lastTime = time;
  }
  requestAnimationFrame(measureFPS);
}
requestAnimationFrame(measureFPS);
```

---

**Q73. What are the differences between `Map` and `WeakMap` in practice?**

```javascript
// Map — strong references, iterable, any key type, has .size
const map = new Map();
let key = { id: 1 };
map.set(key, "data");
map.size; // 1
key = null; // original reference removed
// BUT: Map still holds reference! Object NOT garbage collected
// map still has the entry! Memory leak if key objects accumulate

// WeakMap — weak references, NOT iterable, object keys only, no .size
const weakMap = new WeakMap();
let key2 = { id: 2 };
weakMap.set(key2, "data");
key2 = null; // original reference removed
// WeakMap entry is automatically removed when object is GC'd ✅

// Use case 1: Private data per instance (better than class private fields for mixins)
const _private = new WeakMap();

class Foo {
  constructor() {
    _private.set(this, { secret: 42, history: [] });
  }
  getSecret() { return _private.get(this).secret; }
}

// Use case 2: Caching computed results per DOM element
const renderCache = new WeakMap();
function render(domNode) {
  if (renderCache.has(domNode)) return renderCache.get(domNode);
  const result = expensiveRender(domNode);
  renderCache.set(domNode, result);
  return result;
}
// When domNode is removed from DOM and GC'd, cache entry is automatically cleared ✅

// Use case 3: Tracking objects without preventing GC
const processed = new WeakSet();
function processOnce(obj) {
  if (processed.has(obj)) return;
  processed.add(obj);
  doProcess(obj);
}
```

---

**Q74. What are `Proxy` traps and their use cases?**

```javascript
const TRAPS = {
  // Property access: target.prop
  get(target, prop, receiver) {},

  // Property assignment: target.prop = value
  set(target, prop, value, receiver) {},

  // Property existence: prop in target
  has(target, prop) {},

  // Property deletion: delete target.prop
  deleteProperty(target, prop) {},

  // Function call: fn(...args)
  apply(target, thisArg, args) {},

  // new keyword: new Ctor(...args)
  construct(target, args, newTarget) {},

  // Object.keys, for...in enumeration
  ownKeys(target) {},

  // Object.getOwnPropertyDescriptor
  getOwnPropertyDescriptor(target, prop) {},

  // Object.defineProperty
  defineProperty(target, prop, descriptor) {},

  // Object.getPrototypeOf
  getPrototypeOf(target) {},

  // Object.setPrototypeOf
  setPrototypeOf(target, proto) {},

  // Object.isExtensible
  isExtensible(target) {},

  // Object.preventExtensions
  preventExtensions(target) {},
};

// Practical example — validation proxy:
function createValidated(schema) {
  return new Proxy({}, {
    set(target, prop, value) {
      if (prop in schema) {
        const { type, required, min, max } = schema[prop];
        if (typeof value !== type) throw new TypeError(`${prop} must be ${type}`);
        if (type === "number" && min !== undefined && value < min)
          throw new RangeError(`${prop} must be >= ${min}`);
      }
      return Reflect.set(target, prop, value);
    }
  });
}

const user = createValidated({
  age: { type: "number", min: 0, max: 150 },
  name: { type: "string" },
});
user.age = -1; // RangeError: age must be >= 0
user.name = 42; // TypeError: name must be string
```

---

**Q75. What is `eval()` and why is it dangerous?**

```javascript
// eval() executes a string as JavaScript code in the current scope
let x = 42;
eval("x = 99");
console.log(x); // 99 — eval modified local variable!

// Security: arbitrary code execution
function danger(userInput) {
  eval(userInput); // CRITICAL VULNERABILITY
  // User could pass: "require('fs').unlinkSync('/important/file')"
}

// Performance: eval prevents V8 from optimizing the containing function
// V8 can't know what eval will create/modify, so it disables optimizations

// Alternatives:
// 1. JSON.parse for data
JSON.parse(userInput);

// 2. Function constructor (slightly safer — no local scope access)
const fn = new Function("a", "b", "return a + b");
fn(1, 2); // 3

// 3. Strategy pattern instead of dynamic code
const ops = { add: (a,b) => a+b, sub: (a,b) => a-b };
ops[userInput]?.(1, 2);

// 4. Template processing via functions
const template = (data) => `Hello, ${data.name}!`;

// 5. CSP header prevents eval in browsers:
// Content-Security-Policy: script-src 'self'
// (without 'unsafe-eval')
```

---

**Q76. What is function overloading in JavaScript?**

```javascript
// JavaScript has no native function overloading
// Pattern 1: Check argument types/count

function process(input) {
  if (typeof input === "string") return processString(input);
  if (typeof input === "number") return processNumber(input);
  if (Array.isArray(input)) return processArray(input);
  if (input instanceof Date) return processDate(input);
  throw new TypeError(`Unsupported type: ${typeof input}`);
}

// Pattern 2: Options object (most flexible)
function createServer({ host = "localhost", port = 3000, ssl = false } = {}) {
  return { host, port, ssl };
}
createServer();                          // defaults
createServer({ port: 8080 });            // override one
createServer({ port: 443, ssl: true });  // override multiple

// Pattern 3: Rest parameters with type checking
function sum(...args) {
  if (args.every(a => typeof a === "number")) return args.reduce((a,b) => a+b, 0);
  if (args.every(a => typeof a === "string")) return args.join("");
  throw new TypeError("Mixed types");
}

// Pattern 4: Method dispatch via Symbol or type tag
class Shape {
  area() { throw new Error("Not implemented"); }
}
class Circle extends Shape {
  constructor(r) { super(); this.r = r; }
  area() { return Math.PI * this.r ** 2; }
}
class Rectangle extends Shape {
  constructor(w, h) { super(); this.w = w; this.h = h; }
  area() { return this.w * this.h; }
}
```

---

**Q77. What are JavaScript's bitwise operators and when are they actually useful?**

```javascript
// Bitwise operators work on 32-bit integers:
5 & 3    // 1  — AND:  0101 & 0011 = 0001
5 | 3    // 7  — OR:   0101 | 0011 = 0111
5 ^ 3    // 6  — XOR:  0101 ^ 0011 = 0110
~5       // -6 — NOT:  ~0101 = ...11111010 (two's complement)
5 << 1   // 10 — left shift (multiply by 2^n)
5 >> 1   // 2  — right shift (divide by 2^n, preserves sign)
-1 >>> 0 // 4294967295 — unsigned right shift (converts to uint32)

// Practical uses:
// 1. Feature flags / bitmask permissions (efficient storage)
const READ    = 0b001; // 1
const WRITE   = 0b010; // 2
const EXECUTE = 0b100; // 4

let perms = READ | WRITE; // 3 = 0b011 — user can read and write
perms & READ;    // 1 — truthy: has read permission
perms & EXECUTE; // 0 — falsy: no execute permission
perms |= EXECUTE; // grant execute
perms &= ~WRITE;  // revoke write

// 2. Fast integer truncation (faster than Math.floor for positive numbers)
~~3.7;    // 3
3.7 | 0;  // 3

// 3. Check odd/even:
n & 1; // 1 if odd, 0 if even

// 4. Swap without temp (XOR swap):
a ^= b; b ^= a; a ^= b; // swaps a and b

// 5. Count set bits (Brian Kernighan):
function countBits(n) {
  let count = 0;
  while (n) { n &= n - 1; count++; }
  return count;
}
```

---

**Q78. What is `Object.create(null)` and when do you use it?**

```javascript
// Normal object inherits from Object.prototype
const normal = {};
normal.toString;    // [Function: toString] — from Object.prototype
normal.hasOwnProperty; // [Function: hasOwnProperty]
normal.constructor; // [Function: Object]

// Object.create(null) — no prototype, truly empty
const pure = Object.create(null);
pure.toString;      // undefined — no prototype chain
pure.constructor;   // undefined

// Use cases:
// 1. Safe dictionary / hashmap (no prototype pollution risk)
function createDict() { return Object.create(null); }
const dict = createDict();
dict["toString"] = "my value"; // safe — no conflict with inherited methods
dict["__proto__"] = "safe";    // safe — no prototype hijacking

// 2. Property name from user input:
const userStore = Object.create(null);
function set(key, value) { userStore[key] = value; }
set("constructor", "value"); // safe! would corrupt normal object's constructor

// 3. Microoptimization — V8 can optimize plain objects better
// (no need to check prototype chain for common properties)

// Downside: can't use methods that assume Object.prototype:
// JSON.stringify(pure) — works
// pure.hasOwnProperty — TypeError! use Object.hasOwn(pure, key) instead
```

---

**Q79. What is the difference between `arguments` and rest parameters?**

```javascript
// `arguments` — legacy array-like object in non-arrow functions
function old() {
  console.log(arguments[0]);     // first arg
  console.log(arguments.length); // number of args
  // NOT a real array:
  arguments.map;   // undefined!
  // Convert to array:
  const arr = Array.from(arguments);
  const arr2 = [...arguments]; // spread also works
}

// Rest parameters — real array, modern
function modern(first, second, ...rest) {
  console.log(first);  // first arg
  console.log(rest);   // array of remaining args
  rest.map(x => x * 2); // works! real array
}

// Key differences:
// 1. `arguments` includes ALL args; rest includes only uncaptured args
// 2. `arguments` is array-like; rest is real Array
// 3. Arrow functions don't have `arguments`; rest works in all functions
// 4. `arguments` has .callee (deprecated in strict mode); rest doesn't
// 5. rest can only be the LAST parameter

// `arguments.callee` (deprecated):
// var factorial = function(n) {
//   return n <= 1 ? 1 : n * arguments.callee(n - 1); // bad!
// }
// Use named function expression instead:
const factorial = function fact(n) {
  return n <= 1 ? 1 : n * fact(n - 1);
};
```

---

**Q80. What is `Symbol.iterator` and how do you make an object iterable?**

```javascript
// To make any object iterable, add [Symbol.iterator]() method
// It must return an iterator: object with next() returning {value, done}

// Simple range iterable:
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { value: undefined, done: true };
      }
    };
  }
};
[...range];     // [1, 2, 3, 4, 5]
for (const n of range) console.log(n);

// Infinite iterable (lazy):
const naturals = {
  [Symbol.iterator]() {
    let n = 1;
    return { next: () => ({ value: n++, done: false }) };
  }
};
// Use with take():
function take(n, iterable) {
  const result = [];
  for (const item of iterable) {
    result.push(item);
    if (result.length >= n) break;
  }
  return result;
}
take(5, naturals); // [1, 2, 3, 4, 5]

// Make class iterable:
class Fibonacci {
  [Symbol.iterator]() {
    let [a, b] = [0, 1];
    return {
      next() {
        const value = a;
        [a, b] = [b, a + b];
        return { value, done: false };
      }
    };
  }
}
take(8, new Fibonacci()); // [0, 1, 1, 2, 3, 5, 8, 13]
```

---

## HARD QUESTIONS

---

**Q81. How does the V8 engine optimize JavaScript? Explain JIT compilation, hidden classes, and inline caching.**

V8 converts JavaScript to machine code using a multi-tier compilation pipeline.

```javascript
// V8 Pipeline:
// Source → Parser → AST → Ignition (bytecode interpreter) → Sparkplug (baseline JIT)
//                                                          → Maglev (mid-tier JIT)
//                                                          → Turbofan (optimizing JIT)

// HIDDEN CLASSES (Shapes/Maps in V8 terminology):
// V8 assigns a hidden class to each object based on its property structure
// Objects with the same property names in the same order share a hidden class

// Efficient (same hidden class):
function createPoint(x, y) {
  const p = {};
  p.x = x; // hidden class C0 → C1 (added x)
  p.y = y; // hidden class C1 → C2 (added y)
  return p;
}
const p1 = createPoint(1, 2);
const p2 = createPoint(3, 4);
// p1 and p2 share hidden class C2 → V8 can optimize property access

// Inefficient (different hidden classes — different order):
const p3 = { x: 1, y: 2 }; // C2
const p4 = { y: 2, x: 1 }; // different hidden class D2!
// p3 and p4 have DIFFERENT hidden classes → deoptimized

// Adding properties after construction breaks hidden class sharing:
const p5 = { x: 1, y: 2 };
p5.z = 3; // creates new hidden class — avoid this pattern

// INLINE CACHING (IC):
// V8 caches the result of property lookups
// After seeing the same hidden class, it remembers where the property is

function getX(point) {
  return point.x; // V8 caches: "for hidden class C2, x is at offset 8"
}
// Monomorphic IC: called with one hidden class → FAST
getX({ x: 1, y: 2 });
getX({ x: 3, y: 4 }); // same hidden class → fast!

// Polymorphic IC: 2-4 hidden classes → slower
getX({ x: 1 });         // different hidden class
getX({ x: 1, y: 2 });   // V8 checks both

// Megamorphic IC: 5+ hidden classes → not cached, slow!
// Deoptimization: V8 reverts to interpreter when assumptions are violated

// Best practices:
// 1. Initialize all properties in constructor
// 2. Don't add properties after construction
// 3. Keep property order consistent
// 4. Avoid delete (changes hidden class)
// 5. Use TypedArrays for numeric data (V8 optimizes differently)
```

---

**Q82. Explain memory management in JavaScript — the generational garbage collector, incremental marking, and how to debug memory leaks.**

```javascript
// V8 GENERATIONAL GC:
// Memory is divided into spaces:
// - Young generation (new space): ~1-8MB, most objects allocated here
//   - Nursery (semi-space 1): new allocations
//   - Intermediate: survived one GC
// - Old generation (old space): objects that survived young GC twice
// - Large object space: objects > 1MB (not moved)
// - Code space: compiled code
// - Map space: hidden class objects

// MINOR GC (Scavenger) — fast, frequent:
// 1. Stops all threads briefly (stop-the-world, but short)
// 2. Traces from roots (stack, globals)
// 3. Copies live objects from nursery → intermediate or old space
// 4. Dead objects abandoned (allocation pointer reset)
// Young GC runs every few MB of allocation

// MAJOR GC (Mark-Sweep-Compact) — slower, less frequent:
// 1. INCREMENTAL MARKING: marks in small increments between JS code
//    (reduces pause time — "tri-color marking": white=unvisited, gray=in queue, black=done)
// 2. CONCURRENT MARKING: marks in parallel threads (ES2018+)
// 3. SWEEP: reclaim dead memory (can be lazy/concurrent)
// 4. COMPACT: move live objects to reduce fragmentation

// MEMORY LEAK DETECTION:

// Pattern 1: Detached DOM nodes
let elements = [];
function createAndDetach() {
  const el = document.createElement("div");
  document.body.appendChild(el);
  elements.push(el);        // keeps reference
  document.body.removeChild(el); // removed from DOM but el still referenced!
}

// Pattern 2: Event listeners on global objects
class Component {
  constructor() {
    this.handler = this.onResize.bind(this);
    window.addEventListener("resize", this.handler); // global holds ref to component!
  }
  onResize() {}
  destroy() {
    window.removeEventListener("resize", this.handler); // MUST clean up!
  }
}

// Pattern 3: Closures in timers
function badSetup() {
  const bigData = new Array(10000).fill("heavy");
  setInterval(() => {
    // bigData is captured — never GC'd while interval runs!
    console.log(bigData.length);
  }, 1000);
  // Never calls clearInterval!
}

// Debugging with Performance API:
const measure = (label, fn) => {
  const memBefore = performance.memory?.usedJSHeapSize;
  fn();
  const memAfter = performance.memory?.usedJSHeapSize;
  console.log(`${label}: ${((memAfter - memBefore) / 1024 / 1024).toFixed(2)}MB`);
};

// Chrome DevTools: Memory → Take Heap Snapshot → Compare snapshots
// Look for "Detached" nodes and growing Retained Size
```

---

**Q83. What is the full JavaScript execution context lifecycle — creation phase, execution phase, and the call stack?**

```javascript
// Every time code runs, JS creates an EXECUTION CONTEXT

// Types of execution contexts:
// 1. Global Execution Context (GEC) — created once when script starts
// 2. Function Execution Context (FEC) — created for each function call
// 3. Eval Execution Context — created by eval() (deprecated pattern)

// Each execution context has:
// - Variable Environment (var declarations, function declarations)
// - Lexical Environment (let, const, function scope chain)
// - `this` binding

// CREATION PHASE (before any code runs):
// 1. Create Variable Object:
//    - Scan for `function` declarations → add to Variable Object (fully hoisted)
//    - Scan for `var` declarations → add to Variable Object (initialized to undefined)
//    - let/const → added to TDZ (not initialized)
// 2. Set up scope chain
// 3. Determine `this` binding

// EXECUTION PHASE:
// Code runs line by line, values assigned

function example() {
  // Creation phase:
  // var x → hoisted, initialized to undefined
  // function inner → fully hoisted (value is the function itself)
  // let y → in TDZ

  console.log(x);     // undefined — var hoisted
  console.log(inner); // [Function: inner] — function fully hoisted
  // console.log(y);  // ReferenceError — let in TDZ

  var x = 10;

  function inner() { return "I exist!"; }

  let y = 20;
}

// CALL STACK:
// Stack of currently executing contexts (LIFO)
// Global context always at bottom
// Max size ~10,000-15,000 frames (implementation-specific)

function first() { second(); }
function second() { third(); }
function third() {
  // Call stack: [global, first, second, third]
  console.trace(); // prints current call stack
}
first();

// Stack overflow:
function recurse() { return recurse(); } // each call pushes new frame
recurse(); // RangeError: Maximum call stack size exceeded
```

---

**Q84. Explain how closures are implemented under the hood — heap allocation, scope chains, and the upvalue concept.**

```javascript
// When a function that closes over variables is created,
// those variables CANNOT stay on the stack (stack frame destroyed on return)
// V8 promotes them to the HEAP as "context objects"

function outer() {
  let x = 10;              // promoted to heap context
  let unused = "big data"; // NOT captured — stays on stack (if V8 optimizes)

  function inner() {
    return x++;            // closes over `x` — must be heap-allocated
  }

  return inner;
}

const fn = outer(); // outer's stack frame gone, but `x` lives on heap
fn(); // 10 — x is still accessible
fn(); // 11

// SCOPE CHAIN (internal [[Environment]] slot):
// Each function has an internal [[Environment]] reference
// When variable is accessed, JS walks up [[Environment]] chain

function a() {
  const x = 1;
  function b() {
    const y = 2;
    function c() {
      // c's [[Environment]] → b's scope → a's scope → global scope
      return x + y; // x found in a's scope, y found in b's scope
    }
    return c;
  }
  return b;
}

// V8 optimization: escape analysis
// If V8 proves a closure can't escape current function, it keeps var on stack
// This is called "scalar replacement" — eliminates heap allocation

// The "shared closure" trap:
function makeAdders() {
  const adders = [];
  for (var i = 0; i < 5; i++) {
    adders.push(() => i); // all closures share SAME `i` in outer context!
  }
  return adders;
}
makeAdders().map(fn => fn()); // [5,5,5,5,5] — all see final value

// Fix: create new scope per iteration
function makeAdders() {
  const adders = [];
  for (let i = 0; i < 5; i++) {
    // `let` creates new binding per iteration → each closure has own `i`
    adders.push(() => i);
  }
  return adders;
}
makeAdders().map(fn => fn()); // [0,1,2,3,4] ✅
```

---

**Q85. What is the `Temporal` API and how does it fix `Date`?**

```javascript
// Date problems:
// - Months are 0-indexed (Jan = 0, Dec = 11) — developer trap
// - No timezone support beyond UTC/local
// - Mutable — date.setMonth(2) modifies in place
// - No duration arithmetic
// - toString output is implementation-dependent

// Temporal API (TC39 Stage 3 / shipping in modern environments):
// Import or use via polyfill: npm install @js-temporal/polyfill

const { Temporal } = require("@js-temporal/polyfill");

// PlainDate — date without time or timezone
const today = Temporal.Now.plainDateISO();
const birthday = Temporal.PlainDate.from("1990-05-15");
const age = today.since(birthday);
console.log(age.years); // correct age in years

// PlainDateTime — date + time, no timezone
const meeting = Temporal.PlainDateTime.from("2024-06-15T14:30:00");
meeting.month; // 6 (not 5!) — 1-indexed!

// ZonedDateTime — date + time + timezone (complete, unambiguous)
const launch = Temporal.ZonedDateTime.from({
  year: 2024, month: 6, day: 15,
  hour: 14, minute: 30,
  timeZone: "America/New_York",
});
const launchInCairo = launch.withTimeZone("Africa/Cairo");

// Duration — rich time arithmetic
const duration = Temporal.Duration.from({ hours: 2, minutes: 30 });
const endTime = meeting.add(duration);

// Instant — exact point in time (UTC nanoseconds)
const now = Temporal.Now.instant();
const later = now.add({ hours: 24 });
now.until(later).hours; // 24

// Comparisons (immutable — returns new object):
const d1 = Temporal.PlainDate.from("2024-01-01");
const d2 = d1.add({ months: 3 }); // returns new PlainDate
Temporal.PlainDate.compare(d1, d2); // -1 (d1 before d2)
```

---

**Q86. What are `WeakRef` and `FinalizationRegistry` and when should you use them?**

```javascript
// WeakRef — hold weak reference to object (doesn't prevent GC)
let obj = { name: "important", data: new Array(1000000) };
const ref = new WeakRef(obj);

// Access the object:
const target = ref.deref();
if (target) {
  console.log(target.name); // "important" — object still alive
} else {
  console.log("Object was garbage collected");
}

// Setting obj to null allows GC to collect it
obj = null;
// At some future point:
ref.deref(); // May return undefined if GC ran

// FinalizationRegistry — callback when object is collected
const registry = new FinalizationRegistry((heldValue) => {
  // heldValue is what you registered, NOT the collected object
  // (you can't access the collected object — it's gone)
  console.log(`Object with id ${heldValue} was garbage collected`);
  cleanupResources(heldValue);
});

class Cache {
  #store = new Map();

  set(key, value) {
    const ref = new WeakRef(value);
    registry.register(value, key); // register for cleanup notification
    this.#store.set(key, ref);
  }

  get(key) {
    const ref = this.#store.get(key);
    const value = ref?.deref();
    if (!value) {
      this.#store.delete(key); // clean up stale entry
      return undefined;
    }
    return value;
  }
}

// IMPORTANT WARNINGS:
// - GC timing is non-deterministic — don't rely on it for correctness
// - FinalizationRegistry callback may never run (process exit, etc.)
// - Not a replacement for proper resource management (use finally/disposers)
// - Use WeakRef/FinalizationRegistry only for optional cache invalidation/cleanup
```

---

**Q87. Explain Async Iterators and the Async Iterator Protocol.**

```javascript
// Sync Iterator Protocol:
// - Object with [Symbol.iterator]() → returns iterator
// - Iterator has next() → { value, done }

// Async Iterator Protocol:
// - Object with [Symbol.asyncIterator]() → returns async iterator
// - Async iterator has next() → Promise<{ value, done }>

// Consuming: for await...of
async function consume(asyncIterable) {
  for await (const item of asyncIterable) {
    await process(item);
  }
}

// Creating a custom async iterable:
class WebSocketMessages {
  #socket;
  #messages = [];
  #resolvers = [];

  constructor(url) {
    this.#socket = new WebSocket(url);
    this.#socket.onmessage = ({ data }) => {
      if (this.#resolvers.length > 0) {
        this.#resolvers.shift()({ value: data, done: false });
      } else {
        this.#messages.push(data);
      }
    };
    this.#socket.onclose = () => {
      this.#resolvers.forEach(resolve => resolve({ value: undefined, done: true }));
    };
  }

  [Symbol.asyncIterator]() {
    return {
      next: () => {
        if (this.#messages.length > 0) {
          return Promise.resolve({ value: this.#messages.shift(), done: false });
        }
        return new Promise(resolve => this.#resolvers.push(resolve));
      }
    };
  }
}

// Usage:
const ws = new WebSocketMessages("wss://api.example.com");
for await (const message of ws) {
  console.log("Received:", message);
}

// Node.js Readable streams are async iterables:
const fs = require("fs");
const stream = fs.createReadStream("large-file.txt");
for await (const chunk of stream) {
  processChunk(chunk);
}
```

---

**Q88. What are TC39 proposals you should know — Records, Tuples, Pattern Matching, Pipe operator?**

```javascript
// TC39 STAGES: 0 (Idea) → 1 (Proposal) → 2 (Draft) → 3 (Candidate) → 4 (Finished)

// RECORDS AND TUPLES (Stage 2) — immutable, value-semantics primitives
// Use # prefix to distinguish from objects/arrays

const point = #{ x: 1, y: 2 }; // Record
const rgb = #[255, 0, 0];       // Tuple

// Value equality (unlike objects):
#{ x: 1 } === #{ x: 1 }; // true! (objects: false)
#[1, 2] === #[1, 2];      // true! (arrays: false)

// Immutable:
point.x = 10; // TypeError

// Deeply immutable — can only contain primitives and other records/tuples
const invalid = #{ fn: () => {} }; // TypeError!

// PATTERN MATCHING (Stage 1) — like switch but powerful
const result = match(response) {
  when ({ status: 200, body }) => processBody(body),
  when ({ status: 404 })       => null,
  when ({ status: 500, error }) => { throw new Error(error); },
  when (_)                     => throw new Error("Unexpected response"),
};

// PIPE OPERATOR (Stage 2) — |> feeds left value as argument to right
const result = value
  |> double(%)
  |> addOne(%)
  |> square(%);
// % is the "topic reference" — the piped value

// Equivalent to:
const result = square(addOne(double(value)));

// USING DECLARATIONS / Explicit Resource Management (Stage 4 — landed in TS 5.2+)
{
  using handle = openFile("data.txt"); // automatically calls handle[Symbol.dispose]()
  processFile(handle);
} // dispose() called here automatically, even on error

// Async version:
{
  await using conn = await openConnection(url);
  await fetchData(conn);
} // conn[Symbol.asyncDispose]() called

// ARRAY GROUPING (Stage 3 — available in modern engines)
const people = [
  { name: "Alice", dept: "engineering" },
  { name: "Bob", dept: "marketing" },
  { name: "Carol", dept: "engineering" },
];

const byDept = Object.groupBy(people, p => p.dept);
// { engineering: [Alice, Carol], marketing: [Bob] }

Map.groupBy(people, p => p.dept); // returns Map instead of object
```

---

**Q89. Explain the full event delegation pattern and its performance implications.**

```javascript
// NAIVE approach — attach handler to each element:
document.querySelectorAll(".btn").forEach(btn => {
  btn.addEventListener("click", handleClick);
  // Problems:
  // - 1000 buttons = 1000 event listeners = memory overhead
  // - Dynamically added elements don't get handlers
  // - Must remove listeners on cleanup (memory leaks)
});

// EVENT DELEGATION — attach ONE handler to ancestor:
document.getElementById("container").addEventListener("click", function(event) {
  // event.target — the actual element clicked
  // event.currentTarget — the element the handler is attached to (container)

  const btn = event.target.closest("[data-action]");
  if (!btn) return; // clicked somewhere without data-action

  const action = btn.dataset.action;
  const id = btn.dataset.id;

  // Dispatch to appropriate handler:
  const handlers = {
    delete: (id) => deleteItem(id),
    edit: (id) => editItem(id),
    view: (id) => viewItem(id),
  };

  handlers[action]?.(id);
});

// Works for dynamically added elements ✅
// One listener = memory efficient ✅
// Performance: event.target.closest() traverses DOM — should be fast

// ADVANCED: High-performance table with 10,000 rows
const table = document.getElementById("data-table");
table.addEventListener("click", (e) => {
  const row = e.target.closest("tr[data-row-id]");
  if (!row) return;
  const cell = e.target.closest("td[data-col]");
  if (!cell) return;

  handleCellClick(row.dataset.rowId, cell.dataset.col);
});

// Custom delegated event system:
class DelegatedEvents {
  #listeners = new Map();

  on(selector, event, handler) {
    this.#listeners.has(event) || this.#listeners.set(event, []);
    this.#listeners.get(event).push({ selector, handler });
  }

  attach(root) {
    for (const [event, entries] of this.#listeners) {
      root.addEventListener(event, (e) => {
        for (const { selector, handler } of entries) {
          if (e.target.matches(selector) || e.target.closest(selector)) {
            handler.call(e.target.closest(selector), e);
          }
        }
      });
    }
  }
}
```

---

**Q90. What is the JavaScript specification's internal method `[[Call]]` vs `[[Construct]]` and how does `new` work?**

```javascript
// EVERY function has [[Call]] — invoked normally
// Constructor functions also have [[Construct]] — invoked with `new`
// Arrow functions have [[Call]] but NOT [[Construct]]

// What `new` does (step by step):
function myNew(Constructor, ...args) {
  // 1. Create new object with Constructor's prototype
  const obj = Object.create(Constructor.prototype);

  // 2. Call constructor with `this` = new object
  const result = Constructor.apply(obj, args);

  // 3. If constructor returns an object, return it; otherwise return `new` object
  return (result !== null && typeof result === "object") ? result : obj;
}

// Demonstration:
function Person(name) {
  this.name = name;
  // Implicitly returns `this` (the new object)
}

const p1 = new Person("Alice");
const p2 = myNew(Person, "Alice");
// p1 and p2 behave identically

// Constructor returning object overrides new:
function WeirdConstructor() {
  this.x = 1;
  return { y: 2 }; // returns object → overrides `this`
}
const w = new WeirdConstructor();
w.x; // undefined! — returned object doesn't have x
w.y; // 2 — returned object used

// Arrow function can't be used with new:
const Arrow = () => {};
new Arrow(); // TypeError: Arrow is not a constructor

// new.target — tells if function was called with `new`
function FlexibleConstructor(name) {
  if (!new.target) {
    // Called without new — be lenient or throw
    return new FlexibleConstructor(name);
  }
  this.name = name;
}
```

---

**Q91. Explain how `async/await` is transformed to state machines internally.**

```javascript
// Babel transforms async functions to state machine generators:

// Original async function:
async function fetchUserAndPosts(userId) {
  const user = await fetchUser(userId);
  const posts = await fetchPosts(user.id);
  return { user, posts };
}

// Conceptual transformation (simplified):
function fetchUserAndPosts(userId) {
  return new Promise((resolve, reject) => {
    let _state = 0;
    let _user, _posts;

    function _step(value) {
      try {
        switch (_state) {
          case 0:
            _state = 1;
            const p = fetchUser(userId);
            p.then(_step, reject); // when fetchUser resolves, call _step again
            return;

          case 1:
            _user = value;  // value is the resolved user
            _state = 2;
            const p2 = fetchPosts(_user.id);
            p2.then(_step, reject);
            return;

          case 2:
            _posts = value; // value is the resolved posts
            resolve({ user: _user, posts: _posts });
            return;
        }
      } catch (err) {
        reject(err);
      }
    }

    _step(); // start
  });
}

// V8's actual implementation uses generators internally:
// async function → generator + promise wrapper
// `await` → `yield` that wraps the promise
// The generator is resumed in microtask callbacks

// This is why error handling with async/await needs care:
async function example() {
  // Unhandled rejection inside then:
  fetch("/api").then(r => r.json()).then(throwIfInvalid);
  // ^ This runs in a microtask — try/catch in example() won't catch it!

  // Correct — await it:
  const data = await fetch("/api").then(r => r.json()).then(throwIfInvalid);
}
```

---

**Q92. What is the Reactive programming model — comparing Signals, Observables, and Streams?**

```javascript
// THREE MODELS OF REACTIVITY:

// 1. SIGNALS — synchronous, fine-grained, automatic dependency tracking
// (Solid.js, Vue 3 Composition API, Angular 17+, Preact Signals)

function createSignal(initial) {
  let value = initial;
  const subscribers = new Set();
  let currentTracker = null;

  const read = () => {
    if (currentTracker) subscribers.add(currentTracker); // auto-track
    return value;
  };

  const write = (newVal) => {
    value = typeof newVal === "function" ? newVal(value) : newVal;
    subscribers.forEach(sub => sub());
  };

  return [read, write];
}

function createEffect(fn) {
  const run = () => {
    const prevTracker = currentTracker;
    currentTracker = run;
    fn();
    currentTracker = prevTracker;
  };
  run();
}

const [count, setCount] = createSignal(0);
const [name, setName] = createSignal("Alice");

// Computed signal:
const doubled = createMemo(() => count() * 2);

createEffect(() => {
  // Automatically re-runs when count or name changes (not doubled unless read)
  document.title = `${name()}: ${count()}`;
});

setCount(5); // triggers effect
setName("Bob"); // triggers effect

// 2. OBSERVABLES — push-based, lazy, cancellable, async
// (RxJS — multiple values over time, powerful operators)
import { fromEvent, debounceTime, distinctUntilChanged, switchMap } from "rxjs";

const searchResults$ = fromEvent(input, "input").pipe(
  debounceTime(300),
  map(e => e.target.value),
  distinctUntilChanged(),
  switchMap(query => from(fetch(`/api/search?q=${query}`).then(r => r.json()))),
);
const sub = searchResults$.subscribe(results => renderResults(results));
// Later:
sub.unsubscribe(); // cancellable ✅

// 3. NODE.JS STREAMS — push-based, buffered, backpressure
const { Transform, pipeline } = require("stream");
const zlib = require("zlib");

pipeline(
  fs.createReadStream("input.txt"),
  zlib.createGzip(),
  fs.createWriteStream("output.gz"),
  err => err ? console.error(err) : console.log("Done!")
);
// Handles backpressure automatically — won't overwhelm memory
```

---

**Q93. What are JavaScript's `Error` types and how do you build a robust error hierarchy?**

```javascript
// Built-in error types:
new Error("generic");          // base type
new TypeError("wrong type");   // wrong type used
new RangeError("out of range"); // number out of valid range
new ReferenceError("not defined"); // invalid reference
new SyntaxError("bad syntax"); // invalid syntax (usually parse-time)
new URIError("bad URI");       // malformed URI
new EvalError("eval problem"); // legacy
new AggregateError([e1, e2], "multiple errors"); // Promise.any rejections

// Custom error hierarchy:
class AppError extends Error {
  constructor(message, { code, statusCode = 500, cause } = {}) {
    super(message, { cause }); // native `cause` (ES2022)
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    this.timestamp = new Date().toISOString();

    // Fix stack trace (V8 only):
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      statusCode: this.statusCode,
      timestamp: this.timestamp,
    };
  }
}

class ValidationError extends AppError {
  constructor(message, { fields = [] } = {}) {
    super(message, { code: "VALIDATION_ERROR", statusCode: 400 });
    this.fields = fields;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`, { code: "NOT_FOUND", statusCode: 404 });
    this.resource = resource;
    this.resourceId = id;
  }
}

class DatabaseError extends AppError {
  constructor(message, { cause } = {}) {
    super(message, { code: "DB_ERROR", statusCode: 503, cause });
  }
}

// Error chaining with `cause`:
async function getUser(id) {
  try {
    return await db.query("SELECT * FROM users WHERE id = ?", [id]);
  } catch (err) {
    throw new DatabaseError("Failed to fetch user", { cause: err });
    // err.cause is the original DB error — full chain preserved!
  }
}

// Type-safe error handling:
function handleError(err) {
  if (err instanceof ValidationError) {
    return res.status(400).json({ errors: err.fields });
  }
  if (err instanceof NotFoundError) {
    return res.status(404).json({ message: err.message });
  }
  if (err instanceof AppError) {
    return res.status(err.statusCode).json(err.toJSON());
  }
  // Unknown error
  logger.error("Unexpected error", { error: err });
  return res.status(500).json({ message: "Internal Server Error" });
}
```

---

**Q94. How does the JavaScript event system bubble, capture, and how does `stopPropagation` differ from `stopImmediatePropagation`?**

```javascript
// EVENT PHASES:
// 1. CAPTURE phase: event travels DOWN from document → target
// 2. AT_TARGET: event is at the target element
// 3. BUBBLE phase: event travels UP from target → document

// addEventListener(event, handler, useCapture) — 3rd arg controls phase
// useCapture: true → capture phase, false → bubble phase (default)

document.addEventListener("click", () => console.log("doc CAPTURE"), true);
div.addEventListener("click", () => console.log("div CAPTURE"), true);
btn.addEventListener("click", () => console.log("btn target 1"));
btn.addEventListener("click", () => console.log("btn target 2"));
div.addEventListener("click", () => console.log("div BUBBLE"), false);
document.addEventListener("click", () => console.log("doc BUBBLE"), false);

// Click btn → output:
// "doc CAPTURE"
// "div CAPTURE"
// "btn target 1"  ← at-target: both capture and bubble handlers run in order added
// "btn target 2"
// "div BUBBLE"
// "doc BUBBLE"

// stopPropagation — stops event from traveling further (but other handlers on SAME element still run)
btn.addEventListener("click", (e) => {
  e.stopPropagation();
  console.log("handler 1"); // runs
});
btn.addEventListener("click", () => {
  console.log("handler 2"); // STILL RUNS — stopPropagation only stops travel
});
// div BUBBLE and doc BUBBLE do NOT run

// stopImmediatePropagation — stops propagation AND prevents other handlers on same element
btn.addEventListener("click", (e) => {
  e.stopImmediatePropagation();
  console.log("handler 1"); // runs
});
btn.addEventListener("click", () => {
  console.log("handler 2"); // DOES NOT RUN
});

// preventDefault — prevents default browser behavior (form submit, link navigate)
// Can be combined with stopPropagation or used alone
link.addEventListener("click", (e) => {
  e.preventDefault(); // don't navigate
  handleLinkClick();
});

// passive: true — tells browser handler won't call preventDefault (scroll optimization)
document.addEventListener("scroll", handler, { passive: true }); // browser can optimize scroll!
```

---

**Q95. Explain the HTML5 Web Worker API and how to share state between threads.**

```javascript
// JavaScript is single-threaded — Web Workers run in separate threads
// Workers have no access to DOM, window, or main thread variables
// Communication via message passing (postMessage / onmessage)

// main.js:
const worker = new Worker("worker.js");

// Send data (structured clone algorithm copies it):
worker.postMessage({ type: "COMPUTE", data: largeArray });

// Receive results:
worker.onmessage = ({ data }) => {
  if (data.type === "RESULT") {
    renderResults(data.result);
  }
};

worker.onerror = (err) => console.error("Worker error:", err);

// Terminate:
worker.terminate();

// worker.js:
self.onmessage = ({ data }) => {
  if (data.type === "COMPUTE") {
    const result = heavyComputation(data.data); // runs on worker thread
    self.postMessage({ type: "RESULT", result });
  }
};

// TRANSFERABLE OBJECTS — zero-copy transfer (moves data, doesn't copy)
// Main thread:
const buffer = new ArrayBuffer(1024 * 1024 * 64); // 64MB
worker.postMessage({ buffer }, [buffer]); // transfer ownership
// buffer is now detached (unusable) in main thread — transferred to worker

// SHARED ARRAY BUFFER — shared memory between threads (requires COOP/COEP headers)
const sharedBuffer = new SharedArrayBuffer(Int32Array.BYTES_PER_ELEMENT * 10);
const sharedArray = new Int32Array(sharedBuffer);

worker.postMessage({ sharedArray }); // passes reference, not copy!

// Synchronization with Atomics:
// Main thread:
Atomics.store(sharedArray, 0, 42);     // thread-safe write
Atomics.notify(sharedArray, 0, 1);    // wake one waiting thread

// Worker thread:
Atomics.wait(sharedArray, 0, 0);      // wait until sharedArray[0] !== 0
const value = Atomics.load(sharedArray, 0); // thread-safe read

// Module Worker:
const moduleWorker = new Worker("./worker.js", { type: "module" });
// Worker can use import/export!
```

---

**Q96. What is `structuredClone` with Transferables vs Comlink vs SharedArrayBuffer — when to use each?**

```javascript
// DATA TRANSFER STRATEGIES between threads:

// 1. structured clone (default postMessage) — COPY
// - Safe, simple, any serializable data
// - Cost: proportional to data size (serialize + deserialize)
worker.postMessage(bigArray); // copied — original unchanged
// Use when: small data, both threads need the data, simple types

// 2. Transferable objects — MOVE (zero-copy)
// - ArrayBuffer, MessagePort, ImageBitmap, OffscreenCanvas, ReadableStream
// - Cost: O(1) — pointer transfer
// - Source becomes unusable after transfer
const buffer = new Float64Array(1000000).buffer;
worker.postMessage({ buffer }, [buffer]); // transfer
// Use when: large binary data, source doesn't need data anymore

// 3. SharedArrayBuffer — SHARED MEMORY
// - True shared memory, both threads see same data
// - Requires Atomics for synchronization
// - Requires COOP/COEP HTTP headers
// - Security risk without isolation headers (Spectre)
const shared = new SharedArrayBuffer(4);
// Use when: high-frequency updates, lock-free data structures, real-time

// 4. Comlink — RPC over postMessage (library)
// Makes workers feel like regular objects:
// worker.js:
import { expose } from "comlink";
expose({
  async processData(data) {
    return heavyCompute(data);
  }
});

// main.js:
import { wrap } from "comlink";
const api = wrap(new Worker("./worker.js"));
const result = await api.processData(myData); // feels like regular async call!
// Use when: complex worker API, cleaner abstraction needed

// 5. OffscreenCanvas — canvas rendering in worker
const offscreen = canvas.transferControlToOffscreen();
worker.postMessage({ canvas: offscreen }, [offscreen]);
// Worker can now render to the canvas without touching DOM
```

---

**Q97. What are the `Symbol.toPrimitive`, `valueOf`, and `toString` conversion protocols?**

```javascript
// When JS needs to convert object to primitive:
// 1. Check for [Symbol.toPrimitive](hint) — hint: "number", "string", "default"
// 2. If no Symbol.toPrimitive:
//    - hint "string": toString() → valueOf()
//    - hint "number"/"default": valueOf() → toString()

class Vector {
  constructor(x, y) { this.x = x; this.y = y; }

  // Complete control over conversion:
  [Symbol.toPrimitive](hint) {
    if (hint === "number") return Math.sqrt(this.x**2 + this.y**2); // magnitude
    if (hint === "string") return `Vector(${this.x}, ${this.y})`;
    return this.x + this.y; // default
  }
}

const v = new Vector(3, 4);
+v;          // 5 (hint: "number") — magnitude
`${v}`;      // "Vector(3, 4)" (hint: "string")
v + 1;       // 8 (hint: "default") — 3+4+1
v == 7;      // true (hint: "default")

// Without Symbol.toPrimitive:
class Money {
  constructor(amount, currency) { this.amount = amount; this.currency = currency; }

  valueOf() { return this.amount; }    // called for arithmetic/comparison
  toString() { return `${this.amount} ${this.currency}`; }  // called for string
}

const price = new Money(99.99, "USD");
price + 10;        // 109.99 (uses valueOf)
`Cost: ${price}`;  // "Cost: 99.99 USD" (uses toString)
price > 50;        // true (uses valueOf)

// Conversion order for comparison:
// ToPrimitive called on both sides if one is object
// Then standard comparison rules apply
```

---

**Q98. Explain JavaScript's `Intl` API for internationalization.**

```javascript
// Intl provides locale-aware formatting without external libraries

// 1. Number formatting:
const formatter = new Intl.NumberFormat("ar-EG", {
  style: "currency",
  currency: "EGP",
  minimumFractionDigits: 2,
});
formatter.format(1234567.89); // "١٬٢٣٤٬٥٦٧٫٨٩ ج.م.‏"

new Intl.NumberFormat("en-US", { notation: "compact" }).format(1500000); // "1.5M"
new Intl.NumberFormat("de-DE", { style: "percent" }).format(0.85);        // "85 %"

// 2. Date formatting:
const dateFormatter = new Intl.DateTimeFormat("ar-EG", {
  dateStyle: "full",
  timeStyle: "short",
  timeZone: "Africa/Cairo",
});
dateFormatter.format(new Date()); // "الثلاثاء، ١٥ يناير ٢٠٢٤، ٣:٣٠ م"

// Relative time:
const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
rtf.format(-1, "day");   // "yesterday"
rtf.format(2, "hour");   // "in 2 hours"
rtf.format(-30, "minute"); // "30 minutes ago"

// 3. Collation (locale-aware string sorting):
const words = ["Ångström", "Zebra", "apple", "Über"];
words.sort(new Intl.Collator("en", { sensitivity: "base" }).compare);
// ["apple", "Ångström", "Über", "Zebra"] — correct Unicode sort

// 4. Plural rules:
const plural = new Intl.PluralRules("ar-EG");
plural.select(0);  // "zero"
plural.select(1);  // "one"
plural.select(2);  // "two"
plural.select(5);  // "few"
plural.select(11); // "many"
plural.select(100); // "other"
// Arabic has 6 plural forms!

// 5. List formatting:
const listFormatter = new Intl.ListFormat("en", { style: "long", type: "conjunction" });
listFormatter.format(["Alice", "Bob", "Carol"]); // "Alice, Bob, and Carol"

// 6. Segmentation (word/sentence boundaries):
const segmenter = new Intl.Segmenter("en", { granularity: "word" });
[...segmenter.segment("Hello, World!")].map(s => s.segment);
// ["Hello", ",", " ", "World", "!"]
```

---

**Q99. What are tagged template literals used for in production?**

```javascript
// Tagged templates: fn`template ${expr}` → fn(strings, ...values)
// strings: array of string parts (frozen, has .raw for unprocessed)
// values: interpolated expressions

// 1. SQL query builder (prevents SQL injection):
function sql(strings, ...values) {
  const query = strings.reduce((acc, str, i) => {
    return acc + str + (i < values.length ? `$${i + 1}` : "");
  }, "");
  return { query, params: values };
}

const userId = 42;
const minAge = 18;
const { query, params } = sql`
  SELECT * FROM users
  WHERE id = ${userId}
    AND age >= ${minAge}
`;
// query: "SELECT * FROM users WHERE id = $1 AND age >= $2"
// params: [42, 18]
// Safe parameterized query — no injection!

// 2. HTML escaping (prevents XSS):
function html(strings, ...values) {
  const escape = (str) => String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  return strings.reduce((acc, str, i) => {
    return acc + str + (i < values.length ? escape(values[i]) : "");
  }, "");
}

const userInput = '<script>alert("xss")</script>';
html`<div>${userInput}</div>`;
// "<div>&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;</div>" — safe!

// 3. i18n translations:
function t(strings, ...values) {
  const key = strings.join("{}");
  const translation = translations[currentLocale][key] ?? strings.join("");
  return values.reduce((acc, val) => acc.replace("{}", val), translation);
}

// 4. styled-components (CSS-in-JS):
const Button = styled.button`
  background: ${props => props.primary ? "blue" : "white"};
  color: ${props => props.primary ? "white" : "blue"};
  padding: 8px 16px;
`;

// 5. GraphQL queries:
const query = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      name
      email
    }
  }
`;
```

---

**Q100. What is the Temporal Dead Zone at a deeper level — how it's implemented in the spec?**

```javascript
// TDZ is specified in ECMAScript as a distinct "uninitialized" binding state
// Different from `undefined` — it's a property of the BINDING, not the value

// In the spec, CreateMutableBinding creates binding in "uninitialized" state
// GetBindingValue on uninitialized binding → throws ReferenceError
// InitializeBinding sets the value and marks it "initialized"

// let/const DECLARATION steps at parse time:
// 1. Compiler sees `let x` → creates binding record in current lexical environment
// 2. Marks binding as UNINITIALIZED (not undefined, not null — distinct state)

// Runtime: entering the block
// 3. No initialization happens → binding is still UNINITIALIZED

// Runtime: reaching the let declaration line
// 4. RHS is evaluated (if any)
// 5. InitializeBinding is called → binding becomes INITIALIZED

// The TDZ extends from START OF SCOPE to the DECLARATION line

// TDZ with typeof:
typeof undeclaredVar; // "undefined" — safe with undeclared variables
typeof tdzVar;        // ReferenceError! — let/const in TDZ
let tdzVar = 5;

// Class declarations are in TDZ too:
const instance = new MyClass(); // ReferenceError
class MyClass {}

// Default parameter values and TDZ:
function test(a = b, b = 2) { return a + b; }
test(); // ReferenceError: b is not defined — b is in TDZ when a's default is evaluated

// Interesting edge case:
let x = (x = 5); // Works! — let x enters TDZ, then `x = 5` is evaluated
                  // But wait — assigning to TDZ binding should throw?
                  // No — the RHS `x = 5` creates `x` as assignment expression
                  // and the let binding is initialized with the result
// Actually this DOES throw: let x = x; — ReferenceError (x in TDZ on RHS)
```

---

**Q101. What are JavaScript's concurrency patterns — Producer/Consumer, Semaphore, Mutex?**

```javascript
// JavaScript is single-threaded but async — still needs coordination patterns

// MUTEX — ensures only one async operation runs at a time
class AsyncMutex {
  #queue = [];
  #locked = false;

  async acquire() {
    if (!this.#locked) {
      this.#locked = true;
      return;
    }
    await new Promise(resolve => this.#queue.push(resolve));
    this.#locked = true;
  }

  release() {
    if (this.#queue.length > 0) {
      const next = this.#queue.shift();
      next(); // wake next waiter
    } else {
      this.#locked = false;
    }
  }

  async withLock(fn) {
    await this.acquire();
    try { return await fn(); }
    finally { this.release(); }
  }
}

// Usage — prevent concurrent writes to shared resource:
const mutex = new AsyncMutex();
async function updateFile(data) {
  await mutex.withLock(async () => {
    const current = await fs.readFile("data.json", "utf8");
    const merged = { ...JSON.parse(current), ...data };
    await fs.writeFile("data.json", JSON.stringify(merged));
  });
}

// SEMAPHORE — limits concurrent operations to N
class Semaphore {
  #permits;
  #queue = [];

  constructor(permits) { this.#permits = permits; }

  async acquire() {
    if (this.#permits > 0) { this.#permits--; return; }
    await new Promise(resolve => this.#queue.push(resolve));
  }

  release() {
    if (this.#queue.length > 0) this.#queue.shift()();
    else this.#permits++;
  }
}

// Limit concurrent HTTP requests to 5:
const sem = new Semaphore(5);
async function rateLimitedFetch(url) {
  await sem.acquire();
  try { return await fetch(url); }
  finally { sem.release(); }
}

// PRODUCER/CONSUMER with async queue:
class AsyncQueue {
  #items = [];
  #waiters = [];

  enqueue(item) {
    if (this.#waiters.length > 0) {
      this.#waiters.shift()(item);
    } else {
      this.#items.push(item);
    }
  }

  dequeue() {
    if (this.#items.length > 0) return Promise.resolve(this.#items.shift());
    return new Promise(resolve => this.#waiters.push(resolve));
  }

  async *[Symbol.asyncIterator]() {
    while (true) yield await this.dequeue();
  }
}
```

---

**Q102. Explain tree-shaking in depth — static analysis, side effects, and module graph optimization.**

```javascript
// Tree shaking = dead code elimination at bundle time
// ONLY works with ESM (ES Modules) — CJS cannot be tree-shaken reliably

// Why ESM enables tree shaking:
// 1. import/export are STATIC — known at parse time, not runtime
// 2. Module graph can be built without executing code
// 3. Unused exports can be identified and removed

// math.js:
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export const multiply = (a, b) => a * b; // never imported anywhere
export const divide = (a, b) => a / b;   // never imported anywhere

// app.js:
import { add, subtract } from "./math.js"; // only add and subtract imported
// Bundler sees: multiply and divide are never referenced → remove them

// SIDE EFFECTS block tree shaking:
// sideEffect.js:
console.log("This runs on import!"); // side effect!
export const fn = () => {};

// If bundler doesn't know a module is side-effect-free, it includes it all
// Solution: package.json "sideEffects" field:
{
  "sideEffects": false,           // all files are side-effect free
  "sideEffects": ["./src/polyfills.js", "*.css"] // only these have side effects
}

// CJS cannot be tree-shaken:
const math = require("./math");   // dynamic — could be:
const method = getConfig();
math[method](); // bundler can't know which methods are used!

// Re-export patterns that break tree shaking:
// BAD — index.js barrel file with namespace:
export * from "./moduleA";
export * from "./moduleB"; // bundler may not tree-shake efficiently

// BETTER — explicit re-exports:
export { specificFn } from "./moduleA";

// Checking tree shaking:
// Rollup --input app.js --format esm | grep "multiply" — should be absent
// webpack-bundle-analyzer to visualize included code
```

---

**Q103. What is the Shadow DOM and how does it relate to Web Components encapsulation?**

```javascript
// Shadow DOM — attached to an element, creates isolated DOM subtree
// Shadow DOM's styles don't leak out, outer styles don't leak in (by default)

class MyTooltip extends HTMLElement {
  #shadow;

  constructor() {
    super();
    // Attach shadow root:
    this.#shadow = this.attachShadow({ mode: "open" });
    // mode: "open" — accessible via element.shadowRoot
    // mode: "closed" — not accessible externally (true encapsulation)
  }

  connectedCallback() {
    // Styles are SCOPED — don't leak:
    this.#shadow.innerHTML = `
      <style>
        /* These styles ONLY apply inside this shadow root */
        :host { display: inline-block; position: relative; }
        :host([visible]) .tooltip { opacity: 1; }
        .tooltip {
          position: absolute;
          background: #333;
          color: white;
          padding: 4px 8px;
          border-radius: 4px;
          opacity: 0;
          transition: opacity 0.2s;
          white-space: nowrap;
          pointer-events: none;
        }
      </style>
      <slot></slot>  <!-- Light DOM content goes here -->
      <div class="tooltip">${this.getAttribute("text")}</div>
    `;

    this.addEventListener("mouseenter", () => this.setAttribute("visible", ""));
    this.addEventListener("mouseleave", () => this.removeAttribute("visible"));
  }

  static get observedAttributes() { return ["text"]; }
  attributeChangedCallback(name, _, newVal) {
    if (name === "text") {
      this.#shadow.querySelector(".tooltip").textContent = newVal;
    }
  }
}

customElements.define("my-tooltip", MyTooltip);

// Usage:
// <my-tooltip text="Click to learn more">
//   <button>Hover me</button>  ← goes into <slot>
// </my-tooltip>

// CSS custom properties DO pierce shadow DOM:
// :root { --tooltip-bg: blue; }
// .tooltip { background: var(--tooltip-bg, #333); } — works!

// ::part() allows styling from outside:
// my-tooltip::part(tooltip) { background: red; } — if tooltip has part="tooltip"
```

---

**Q104. What are JavaScript's latest features — ES2023, ES2024, and what's coming in ES2025?**

```javascript
// ES2023 (ECMAScript 2023):

// 1. Array find from last:
[1, 2, 3, 4].findLast(x => x % 2 === 0);       // 4
[1, 2, 3, 4].findLastIndex(x => x % 2 === 0);   // 3

// 2. Array toSorted, toReversed, toSpliced, with — non-mutating versions
const arr = [3, 1, 2];
arr.toSorted();                 // [1, 2, 3] — new array
arr.toReversed();               // [2, 1, 3] — new array
arr.with(1, 99);                // [3, 99, 2] — new array with index 1 = 99
arr; // [3, 1, 2] — original unchanged!

// 3. Symbol as WeakMap/WeakSet keys:
const key = Symbol("key");
const weakMap = new WeakMap();
weakMap.set(key, "value"); // Now allowed!

// 4. Hashbang grammar — #!/usr/bin/env node in first line

// ES2024 (ECMAScript 2024):

// 1. Object.groupBy (previously shown):
Object.groupBy([1,2,3,4,5], n => n % 2 === 0 ? "even" : "odd");
// { odd: [1,3,5], even: [2,4] }

// 2. Promise.withResolvers — expose resolve/reject outside Promise:
const { promise, resolve, reject } = Promise.withResolvers();
// Before: had to capture resolve/reject in variables with side effects
setTimeout(() => resolve(42), 1000);
const value = await promise; // 42

// 3. ArrayBuffer.prototype.resize and transfer:
const buf = new ArrayBuffer(8, { maxByteLength: 64 }); // resizable
buf.resize(32); // resize to 32 bytes (within max)
const transferred = buf.transfer(16); // new 16-byte buffer

// 4. String.prototype.isWellFormed and toWellFormed:
"hello\uD800".isWellFormed(); // false — lone surrogate
"hello\uD800".toWellFormed(); // "hello\uFFFD" — replace with replacement char
"hello".isWellFormed();       // true

// ES2025 (upcoming/stage 4):
// 1. Set methods: union, intersection, difference, symmetricDifference
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);
a.union(b);               // Set {1, 2, 3, 4}
a.intersection(b);        // Set {2, 3}
a.difference(b);          // Set {1}
a.symmetricDifference(b); // Set {1, 4}
a.isSubsetOf(b);          // false
a.isSupersetOf(b);        // false
a.isDisjointFrom(b);      // false

// 2. RegExp.escape (proposed):
RegExp.escape("hello.world+foo"); // "hello\\.world\\+foo" — escapes special chars

// 3. Explicit Resource Management (using declarations) — stage 4:
{
  using file = openFile("data.txt"); // calls file[Symbol.dispose]() on exit
  processFile(file);
} // automatic cleanup, even on throw!
```

---

**Q105. Explain the full mechanics of JavaScript module evaluation — circular dependencies, live bindings, and evaluation order.**

```javascript
// ESM EVALUATION STEPS:
// 1. PARSE: parse all modules in the graph (detect syntax errors)
// 2. INSTANTIATE: create bindings in memory (not yet evaluated)
// 3. EVALUATE: execute module code, populate bindings

// LIVE BINDINGS — exported values are live references, not copies:
// counter.js:
export let count = 0;
export function increment() { count++; }

// app.js:
import { count, increment } from "./counter.js";
console.log(count); // 0
increment();
console.log(count); // 1 ← live binding! reflects the change

// In CJS: const { count } = require("./counter") would copy the value (always 0)

// CIRCULAR DEPENDENCIES:
// a.js:
import { b } from "./b.js";
export const a = "a";
console.log("a module:", b); // might be undefined!

// b.js:
import { a } from "./a.js";
export const b = "b";
console.log("b module:", a); // might be undefined!

// Evaluation order with circular deps:
// 1. Start evaluating a.js
// 2. a.js imports b.js → evaluate b.js first
// 3. b.js imports a.js → a.js already being evaluated → returns current binding (undefined!)
// 4. b.js finishes → b = "b"
// 5. a.js continues → b is now "b", but already console.log'd undefined

// Fix: use functions (evaluated lazily, not at import time)
// a.js:
import { getB } from "./b.js";
export const a = "a";
export function getA() { return a; }

// b.js:
import { getA } from "./a.js";
export const b = "b";
export function getB() { return b; }

// MODULE EVALUATION IS CACHED:
// A module is only evaluated ONCE regardless of how many times it's imported
// Subsequent imports return the cached module namespace object
```

---

**Q106. What is `Atomics.waitAsync` and how does it enable non-blocking synchronization?**

```javascript
// SharedArrayBuffer + Atomics enable shared memory between threads
// Atomics.wait() BLOCKS the calling thread (can't use on main thread!)
// Atomics.waitAsync() — non-blocking version that returns a Promise

// Main thread (can't block):
const sharedBuffer = new SharedArrayBuffer(4);
const sharedInt = new Int32Array(sharedBuffer);

// waitAsync — non-blocking, returns promise
async function waitForWorkerSignal() {
  // Wait for sharedInt[0] to change from 0
  const result = await Atomics.waitAsync(sharedInt, 0, 0).value;
  if (result === "ok") {
    console.log("Worker signaled!");
    const value = Atomics.load(sharedInt, 0);
    console.log("Value:", value);
  }
}

// Communicate to worker:
worker.postMessage({ buffer: sharedBuffer });
await waitForWorkerSignal(); // non-blocking wait

// Worker thread:
// worker.js
self.onmessage = ({ data }) => {
  const sharedInt = new Int32Array(data.buffer);
  // Do heavy computation...
  const result = heavyCompute();

  // Atomically write result and wake main thread:
  Atomics.store(sharedInt, 0, result);
  Atomics.notify(sharedInt, 0, 1); // wake 1 thread waiting on index 0
};

// Lock-free data structures with Atomics:
function atomicPush(buffer, value) {
  const arr = new Int32Array(buffer);
  const LENGTH_IDX = 0;
  while (true) {
    const len = Atomics.load(arr, LENGTH_IDX);
    // Compare-and-swap: if arr[LENGTH_IDX] === len, set it to len+1
    const prev = Atomics.compareExchange(arr, LENGTH_IDX, len, len + 1);
    if (prev === len) {
      // We won the race — write our value at position len+1
      Atomics.store(arr, len + 1, value);
      return;
    }
    // Another thread changed it first — retry
  }
}
```

---

**Q107. What is the difference between `structuredClone`, the `History API`'s state cloning, and `MessageChannel` serialization?**

```javascript
// All three use the Structured Clone Algorithm but with different behaviors:

// 1. structuredClone — general purpose deep clone
const clone = structuredClone({
  date: new Date(),          // cloned as new Date
  map: new Map(),            // cloned as new Map
  circular: (() => {
    const o = {};
    o.self = o;
    return o;
  })(),                      // circular reference handled
});

// 2. History API — pushState/replaceState state cloning
history.pushState(
  { user: { name: "Alice" }, page: 1 }, // cloned and stored
  "",
  "/users/alice"
);
// History serializes state using structured clone
// Size limit: ~2-16MB depending on browser
// Cannot store: functions, DOM nodes, non-serializable objects

// 3. MessageChannel — transfers between contexts
const { port1, port2 } = new MessageChannel();

port2.onmessage = ({ data }) => {
  // data is structured clone of what was sent
  console.log(data);
};

port1.postMessage({
  data: new Float64Array([1.1, 2.2, 3.3]),
  meta: { timestamp: Date.now() },
});

// With transfer (zero-copy):
const buffer = new Float64Array(1e6).buffer;
port1.postMessage({ buffer }, [buffer]); // transfer ownership

// MessageChannel use cases:
// - Communication between iframes (cross-origin with postMessage + channel)
// - Service Worker ↔ page communication
// - Web Worker communication with reply capability
// - Off-main-thread task queue pattern
```

---

**Q108. What are JavaScript's `Proxy` invariants and what happens when you violate them?**

```javascript
// Proxy handlers must follow invariants specified in the ECMAScript spec
// Violating them causes a TypeError even if your handler seems to work

// INVARIANT 1: get must return the property value if it's non-writable & non-configurable
const obj = {};
Object.defineProperty(obj, "frozen", { value: 42, writable: false, configurable: false });

const proxy = new Proxy(obj, {
  get(target, prop) {
    if (prop === "frozen") return 999; // VIOLATION!
    return Reflect.get(target, prop);
  }
});
proxy.frozen; // TypeError: 'get' on proxy: property 'frozen' is non-writable...
// Must return 42 — the actual value

// INVARIANT 2: set must return false (or throw) if property is non-writable & non-configurable
const proxy2 = new Proxy(obj, {
  set(target, prop, value) {
    return true; // VIOLATION — claiming success on non-writable property!
  }
});
proxy2.frozen = 999; // TypeError: 'set' on proxy: non-writable property

// INVARIANT 3: has must return true if own non-configurable property
const proxy3 = new Proxy(obj, {
  has(target, prop) { return false; } // VIOLATION for "frozen"!
});
"frozen" in proxy3; // TypeError

// INVARIANT 4: deleteProperty cannot delete non-configurable properties
const proxy4 = new Proxy(obj, {
  deleteProperty(target, prop) { return true; } // VIOLATION for "frozen"
});
delete proxy4.frozen; // TypeError

// INVARIANT 5: ownKeys must include non-configurable own properties
const proxy5 = new Proxy(obj, {
  ownKeys() { return []; } // VIOLATION — must include "frozen"!
});
Object.keys(proxy5); // TypeError

// These invariants ensure proxies can't break fundamental JavaScript guarantees
// like: "non-configurable property has a fixed value"
```

---

**Q109. What is the JavaScript `using` declaration and the `Disposable` protocol?**

```javascript
// Explicit Resource Management (ES2025 / TypeScript 5.2+)
// Solves: resources not cleaned up on early return, throw, break

// Old way:
async function processFile(path) {
  let file;
  try {
    file = await openFile(path);
    const data = await file.read();
    return processData(data);
  } finally {
    await file?.close(); // must remember this!
  }
}

// New way with using:
async function processFile(path) {
  await using file = await openFile(path); // auto-dispose on scope exit
  const data = await file.read();
  return processData(data); // file.close() called automatically
}

// Implementing Disposable:
class DatabaseConnection {
  #pool;
  #connection;

  constructor(pool, connection) {
    this.#pool = pool;
    this.#connection = connection;
  }

  async query(sql, params) {
    return this.#connection.query(sql, params);
  }

  // Sync dispose:
  [Symbol.dispose]() {
    this.#pool.release(this.#connection);
  }
}

// Implementing AsyncDisposable:
class FileHandle {
  #fd;
  constructor(fd) { this.#fd = fd; }

  async [Symbol.asyncDispose]() {
    await fs.promises.close(this.#fd);
  }
}

// DisposableStack — collect multiple disposables:
function openResources() {
  using stack = new DisposableStack();
  const conn = stack.use(openConnection()); // registered for disposal
  const file = stack.use(openFile("data.txt"));
  stack.defer(() => cleanup()); // custom cleanup
  return process(conn, file);
  // all disposed in LIFO order on scope exit
}
```

---

**Q110. Explain the complete picture of JavaScript performance optimization.**

```javascript
// MEASUREMENT FIRST — never optimize without measuring:
const t0 = performance.now();
doWork();
const t1 = performance.now();
console.log(`Took ${t1 - t0}ms`);

// performance.mark and measure:
performance.mark("start-render");
renderUI();
performance.mark("end-render");
performance.measure("render", "start-render", "end-render");
const [measure] = performance.getEntriesByName("render");
console.log(measure.duration); // milliseconds with sub-ms precision

// 1. ALGORITHM/DATA STRUCTURE — biggest wins
// O(n²) search → O(1) hashmap lookup
const userMap = new Map(users.map(u => [u.id, u]));
userMap.get(userId); // O(1) vs O(n) array find

// 2. AVOID LAYOUT THRASHING (browser)
// Bad — reads and writes interleaved (forces browser reflow each time):
items.forEach(item => {
  const width = item.offsetWidth;   // READ — forces layout
  item.style.width = width * 2 + "px"; // WRITE
}); // n reads + n writes = n reflows

// Good — batch reads then writes:
const widths = items.map(item => item.offsetWidth); // all reads
items.forEach((item, i) => { item.style.width = widths[i] * 2 + "px"; }); // all writes

// 3. AVOID GC PRESSURE — reuse objects instead of creating new ones
// Object pool pattern:
class VectorPool {
  #pool = [];
  acquire(x, y) {
    const v = this.#pool.pop() ?? { x: 0, y: 0 };
    v.x = x; v.y = y;
    return v;
  }
  release(v) { this.#pool.push(v); }
}

// 4. USE TYPED ARRAYS for number-heavy code:
// Regular array: heap-allocated, boxed numbers, GC pressure
const regular = new Array(1000000).fill(0);

// TypedArray: contiguous memory, unboxed, cache-friendly
const typed = new Float64Array(1000000);
// 10-100x faster for numeric computation!

// 5. MEMOIZE expensive pure functions:
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const k = JSON.stringify(args);
    if (!cache.has(k)) cache.set(k, fn(...args));
    return cache.get(k);
  };
};

// 6. LAZY EVALUATION:
class LazyValue {
  #factory;
  #value;
  #computed = false;

  constructor(factory) { this.#factory = factory; }

  get value() {
    if (!this.#computed) {
      this.#value = this.#factory();
      this.#computed = true;
    }
    return this.#value;
  }
}

// 7. WEB WORKERS for CPU-intensive work:
// Main thread stays responsive, computation in worker

// 8. CODE SPLITTING — load only what's needed:
const HeavyChart = lazy(() => import("./HeavyChart")); // only loaded when rendered

// 9. VIRTUALIZATION — only render visible items:
// React Window, TanStack Virtual — render only ~20 rows of 10,000

// 10. AVOID MICRO-OPTIMIZATIONS until profiling shows they matter:
// V8 is very good at optimizing clear, readable code
// Complex micro-optimizations often make code harder to maintain
// and V8 may optimize the simple version better anyway
```

---

*This file contains 110 complete JavaScript interview questions with full code answers. Questions 1–40 are Easy, 41–80 Medium, 81–110 Hard. Together they cover every major JavaScript concept from language fundamentals to V8 internals, modern APIs, and production patterns.*

---

## ADDITIONAL HARD QUESTIONS (Q111–Q130)

---

**Q111. What is the difference between `Object.assign` and spread operator for merging?**

```javascript
const a = { x: 1, get val() { return 42; } };
const b = { y: 2 };

// Spread — copies enumerable own properties (invokes getters, copies value):
const spread = { ...a, ...b };
spread.val; // 42 — the value, getter is NOT copied

// Object.assign — also invokes getters, copies value:
const assigned = Object.assign({}, a, b);
assigned.val; // 42 — same behavior

// KEY DIFFERENCE: Object.assign mutates target
const target = { x: 0 };
Object.assign(target, a); // target is mutated!
target.x; // 1

// Both are SHALLOW copies:
const nested = { a: { b: 1 } };
const copy = { ...nested };
copy.a === nested.a; // true — same reference

// Object.assign vs spread for prototype:
const proto = { greet() { return "hi"; } };
const child = Object.create(proto);
child.name = "Alice";

{ ...child }; // { name: "Alice" } — proto methods NOT copied
Object.assign({}, child); // { name: "Alice" } — same, proto NOT copied

// To copy with prototype:
Object.create(Object.getPrototypeOf(child), Object.getOwnPropertyDescriptors(child));
```

---

**Q112. What is `queueMicrotask` and how does it differ from `Promise.resolve().then()`?**

```javascript
// Both schedule microtasks, but queueMicrotask is simpler:

// queueMicrotask — direct microtask scheduling:
queueMicrotask(() => console.log("microtask"));

// Promise.resolve().then — wraps in Promise machinery (slightly heavier):
Promise.resolve().then(() => console.log("promise microtask"));

// Both run in microtask queue after current sync code, before next macrotask.
// Output order: same — both are microtasks

// Key difference — error handling:
queueMicrotask(() => { throw new Error("oops"); });
// Throws as unhandled, no .catch() possible

Promise.resolve().then(() => { throw new Error("oops"); });
// Becomes unhandled rejection — catchable with process.on('unhandledRejection')

// Use queueMicrotask when:
// - You just want to defer to end of current microtask checkpoint
// - No need for Promise chaining
// - Slightly better performance (no Promise object created)

// Practical use — batch DOM updates:
let pending = false;
const updates = [];

function scheduleUpdate(item) {
  updates.push(item);
  if (!pending) {
    pending = true;
    queueMicrotask(() => {
      flushUpdates(updates.splice(0)); // process all at once
      pending = false;
    });
  }
}
```

---

**Q113. How does `Array.from` work and what are all its use cases?**

```javascript
// Array.from(arrayLike, mapFn?, thisArg?)
// Converts array-like or iterable to a real Array

// 1. From array-like (has length + indexed elements):
Array.from("hello");           // ["h","e","l","l","o"]
Array.from({ length: 3 });     // [undefined, undefined, undefined]
Array.from(arguments);         // convert arguments object
Array.from(document.querySelectorAll("div")); // NodeList → Array

// 2. From iterables:
Array.from(new Set([1, 2, 2, 3])); // [1, 2, 3] — dedup
Array.from(new Map([["a",1],["b",2]])); // [["a",1],["b",2]]
Array.from(new Range(1, 5));    // from custom iterable

// 3. With mapping function (like map but works during creation):
Array.from({ length: 5 }, (_, i) => i);          // [0,1,2,3,4]
Array.from({ length: 5 }, (_, i) => i * 2);      // [0,2,4,6,8]
Array.from({ length: 3 }, () => []);              // [[],[],[]] — separate arrays!
Array.from("hello", c => c.toUpperCase());        // ["H","E","L","L","O"]

// 4. Clone array:
Array.from([1, 2, 3]); // new array, shallow copy

// vs Array.of — creates array from arguments:
Array.of(3);           // [3]       — element is 3
new Array(3);          // [,,]      — length is 3 (sparse!)
Array.from({ length: 3 }, () => 0); // [0, 0, 0] — safe filled array

// Generate ranges:
const range = (start, end, step = 1) =>
  Array.from({ length: Math.ceil((end - start) / step) }, (_, i) => start + i * step);
range(1, 10, 2); // [1, 3, 5, 7, 9]
```

---

**Q114. What is the `Proxy` `apply` trap and how to intercept function calls?**

```javascript
// apply trap — intercepts function calls (fn(), fn.call(), fn.apply())

function greet(name) {
  return `Hello, ${name}!`;
}

const proxied = new Proxy(greet, {
  apply(target, thisArg, args) {
    console.log(`Called with args: ${args}`);
    const result = Reflect.apply(target, thisArg, args);
    console.log(`Returned: ${result}`);
    return result;
  }
});

proxied("Alice");
// Called with args: Alice
// Returned: Hello, Alice!
// "Hello, Alice!"

// Practical: function memoization via Proxy
function memoizeProxy(fn) {
  const cache = new Map();
  return new Proxy(fn, {
    apply(target, thisArg, args) {
      const key = JSON.stringify(args);
      if (cache.has(key)) return cache.get(key);
      const result = Reflect.apply(target, thisArg, args);
      cache.set(key, result);
      return result;
    }
  });
}

// Currying via Proxy:
function autoCurry(fn) {
  return new Proxy(fn, {
    apply(target, thisArg, args) {
      if (args.length >= target.length) {
        return Reflect.apply(target, thisArg, args);
      }
      // Return partially applied function:
      return autoCurry(target.bind(thisArg, ...args));
    }
  });
}

const add = autoCurry((a, b, c) => a + b + c);
add(1)(2)(3); // 6
add(1, 2)(3); // 6
add(1)(2, 3); // 6
```

---

**Q115. What is `structuredClone` vs `MessageChannel` serialization vs `history.pushState`?**

```javascript
// All three use the Structured Clone Algorithm but with subtle differences:

// 1. structuredClone() — general-purpose deep clone
const obj = { date: new Date(), map: new Map([["a", 1]]), circular: null };
obj.circular = obj;
const clone = structuredClone(obj);
// ✅ Date cloned, Map cloned, circular reference handled
// ❌ Functions, DOM nodes, Symbols (as values) not supported

// 2. MessageChannel — cross-context transfer
const { port1, port2 } = new MessageChannel();
port2.onmessage = ({ data }) => console.log(data); // structured clone of sent data
port1.postMessage({ date: new Date(), buffer: new ArrayBuffer(8) });
// ✅ Same as structuredClone capabilities
// ✅ Plus: can TRANSFER ownership (zero-copy) with second argument
port1.postMessage({ buffer }, [buffer]); // buffer transferred, not cloned

// 3. history.pushState — stores state with navigation
history.pushState({ date: new Date(), count: 42 }, "", "/page/2");
// ✅ Same structured clone
// ⚠️ Size limit: ~2-16MB depending on browser
// ❌ Functions, DOM nodes not cloneable

// Key capability matrix:
const capabilities = {
  //                    structuredClone  MessageChannel  pushState
  circularRefs:         true,            true,           true,
  Date:                 true,            true,           true,
  Map_Set:              true,            true,           true,
  ArrayBuffer:          true,            true,           true,
  transfer_ownership:   false,           true,           false,
  functions:            false,           false,          false,
  DOM_nodes:            false,           false,          false,
  sizeLimit:            false,           false,          true,
};
```

---

**Q116. Explain `generator` + `Promise` combination — async generators in depth.**

```javascript
// Async generator: yields Promises, consumed with for-await-of

async function* paginate(fetchPage) {
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const { data, nextPage } = await fetchPage(page); // await inside generator!
    yield data;            // yields array of items for this page
    hasMore = !!nextPage;
    page = nextPage ?? page + 1;
  }
}

// Usage — lazy, processes one page at a time:
async function processAllUsers() {
  const pages = paginate((page) => fetch(`/api/users?page=${page}`).then(r => r.json()));

  for await (const users of pages) {
    await Promise.all(users.map(processUser)); // process page in parallel
    // Next page only fetched when this iteration completes
  }
}

// Return value from generator:
async function* withReturn() {
  yield 1;
  yield 2;
  return "done"; // { value: "done", done: true } — usually ignored by for-await
}

// Early termination — generator cleanup:
async function* withCleanup() {
  const resource = await openResource();
  try {
    while (true) {
      yield await resource.read();
    }
  } finally {
    await resource.close(); // runs even on break or thrown error!
  }
}

async function consumer() {
  for await (const chunk of withCleanup()) {
    if (shouldStop(chunk)) break; // triggers finally in generator
    process(chunk);
  }
}

// Compose async generators (pipeline):
async function* map(iter, fn) {
  for await (const item of iter) yield fn(item);
}
async function* filter(iter, pred) {
  for await (const item of iter) if (pred(item)) yield item;
}
async function* take(iter, n) {
  let count = 0;
  for await (const item of iter) {
    yield item;
    if (++count >= n) return;
  }
}

const result = take(filter(map(paginate(fetch), transform), isValid), 100);
```

---

**Q117. What is `Symbol.species` and why is it controversial?**

```javascript
// Symbol.species — lets subclasses control what constructor derived methods use

class MyArray extends Array {
  static get [Symbol.species]() { return Array; } // map/filter return Array, not MyArray
  
  double() {
    return this.map(x => x * 2); // what does .map() return?
  }
}

const myArr = new MyArray(1, 2, 3);

// Without Symbol.species override:
const doubled = myArr.double();
doubled instanceof MyArray; // true — map returns MyArray by default

// With Symbol.species = Array:
const doubled2 = myArr.double();
doubled2 instanceof MyArray; // false — map returns plain Array
doubled2 instanceof Array;   // true

// Why controversial:
// - Confusing — method on MyArray instance returns different type
// - Security concern — malicious subclass can override species to return unexpected type
// - Difficult to optimize (engine must check species dynamically)
// - TC39 now recommends removing Symbol.species from new APIs
// - Array.prototype.map and similar may ignore it in future

// Practical: Promise.resolve in subclass:
class MyPromise extends Promise {
  static get [Symbol.species]() { return Promise; }
}
const p = new MyPromise(resolve => resolve(1));
p.then(() => {}) instanceof MyPromise; // false — returns plain Promise
```

---

**Q118. What is the JavaScript Temporal Dead Zone for class fields?**

```javascript
// Class fields also have a TDZ-like behavior in constructors

class Parent {
  value = this.compute(); // runs during construction

  compute() { return 42; }
}

class Child extends Parent {
  multiplier = 2; // field initialized AFTER super() in child

  compute() {
    // Called by Parent's `value = this.compute()` during super()
    // BUT: Child's own fields aren't initialized yet!
    return this.multiplier * 10; // multiplier is undefined here!
  }
}

const c = new Child();
c.value;      // NaN (undefined * 10 = NaN)
c.multiplier; // 2 — initialized after super() completes

// Fix: don't call overridden methods in parent field initializers
class ParentFixed {
  compute() { return 42; }
  value = this.compute(); // safe if subclasses don't override compute
}

// Class field initialization order:
class Example {
  a = console.log("1. field a");
  b = console.log("2. field b");

  constructor() {
    console.log("3. constructor body");
  }

  c = console.log("4. field c after constructor?"); // NO — fields run before body!
}
// Output: 1, 2, 4, 3 — NO! fields run in declaration order BEFORE constructor body
// Actually output: 1, 2, 3 — field c declaration is after constructor — ERROR in thinking
// Correct: fields declared anywhere in class run first in order, then constructor

// Real order:
class Real {
  x = 1;
  constructor() { console.log(this.x, this.y); } // 1, 2
  y = 2;
}
// x: 1 initialized, y: 2 initialized, then constructor runs → logs 1, 2
```

---

**Q119. What are well-known symbols and how do they customize built-in behavior?**

```javascript
// Well-known symbols let objects hook into JavaScript built-in operations

// Symbol.iterator — makes object iterable
class Counter {
  constructor(low, high) { this.low = low; this.high = high; }
  [Symbol.iterator]() {
    let n = this.low;
    return { next: () => n <= this.high
      ? { value: n++, done: false }
      : { value: undefined, done: true }
    };
  }
}
[...new Counter(1, 5)]; // [1,2,3,4,5]

// Symbol.toPrimitive — control type conversion
class Money {
  constructor(amount, currency) { this.amount = amount; this.currency = currency; }
  [Symbol.toPrimitive](hint) {
    if (hint === "number") return this.amount;
    if (hint === "string") return `${this.amount} ${this.currency}`;
    return this.amount; // default
  }
}
const price = new Money(9.99, "USD");
+price;       // 9.99    (number hint)
`${price}`;   // "9.99 USD" (string hint)
price * 2;    // 19.98  (number hint)

// Symbol.hasInstance — control instanceof behavior
class Range {
  constructor(min, max) { this.min = min; this.max = max; }
  static [Symbol.hasInstance](value) {
    return typeof value === "number" && value >= 0 && value <= 100;
  }
}
50 instanceof Range;  // true
150 instanceof Range; // false

// Symbol.toStringTag — control Object.prototype.toString.call()
class MyCollection {
  get [Symbol.toStringTag]() { return "MyCollection"; }
}
Object.prototype.toString.call(new MyCollection()); // "[object MyCollection]"

// Symbol.isConcatSpreadable — control Array.prototype.concat behavior
const arrayLike = { 0: "a", 1: "b", length: 2, [Symbol.isConcatSpreadable]: true };
["x"].concat(arrayLike); // ["x", "a", "b"] — spread!
const arr = [1, 2, 3];
arr[Symbol.isConcatSpreadable] = false;
[].concat(arr); // [[1,2,3]] — NOT spread

// Symbol.asyncIterator — async iteration protocol
class AsyncRange {
  constructor(start, end) { this.start = start; this.end = end; }
  [Symbol.asyncIterator]() {
    let n = this.start;
    return {
      next: async () => {
        await new Promise(r => setTimeout(r, 10)); // simulate async
        return n <= this.end ? { value: n++, done: false } : { done: true };
      }
    };
  }
}
for await (const n of new AsyncRange(1, 3)) console.log(n); // 1, 2, 3
```

---

**Q120. What is the JavaScript specification's `Completion Record`?**

```javascript
// Completion Record: internal spec mechanism for how statements complete
// Types: normal, break, continue, return, throw
// Each statement produces a completion record

// The spec defines statement evaluation in terms of completion records:
// { [[Type]]: normal|break|continue|return|throw, [[Value]]: any, [[Target]]: label }

// Why this matters in JavaScript behavior:

// 1. Block statement value (empty completion):
eval("{ 1; 2; 3; }"); // 3 — last normal completion value

// 2. try-finally completion interaction:
function tricky() {
  try {
    return 1; // return completion with value 1
  } finally {
    return 2; // overrides! finally's return takes precedence
  }
}
tricky(); // 2 — finally return overrides try return

function tricky2() {
  try {
    throw new Error("oops"); // throw completion
  } finally {
    return "recovered"; // return completion overrides throw!
  }
}
tricky2(); // "recovered" — exception suppressed by finally return!
// This is a common bug — avoid return in finally

// 3. break with label — abrupt completion:
outer: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) break outer; // break completion with target "outer"
  }
}

// 4. The spec's "?" shorthand (used in spec text):
// ? operation() means: if operation() is abrupt (throw), return that completion
// This is how error propagation is specified throughout the spec
```

---

**Q121. Explain `Object.getOwnPropertyDescriptors` and its practical uses.**

```javascript
// Returns all own property descriptors (including non-enumerable + getters/setters)

const source = {
  name: "Alice",
  get age() { return 30; },
  set age(v) { console.log("setting age:", v); },
};
Object.defineProperty(source, "secret", {
  value: "hidden", enumerable: false, configurable: true, writable: false
});

// Regular copy — loses getters/setters and non-enumerable:
const shallow = { ...source };
// { name: "Alice", age: 30 } — age getter was called, value copied; secret missing!

// Full copy preserving ALL descriptors:
const perfect = Object.create(
  Object.getPrototypeOf(source),
  Object.getOwnPropertyDescriptors(source)
);
// perfect has: name, working get/set age, non-enumerable secret!
perfect.age;        // 30 — calls getter
perfect.age = 50;   // calls setter: "setting age: 50"
perfect.secret;     // "hidden" — non-enumerable preserved
Object.keys(perfect); // ["name"] — secret not enumerable, age is get/set

// Mixin with descriptor preservation:
function mixin(target, ...sources) {
  for (const source of sources) {
    Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
  }
  return target;
}

// Freeze with getters preserved:
const obj = { get computed() { return Date.now(); } };
const frozen = Object.freeze(Object.create(null, Object.getOwnPropertyDescriptors(obj)));
frozen.computed; // still works (getter called)
frozen.x = 1;   // silently fails (frozen)
```

---

**Q122. What is the `Error.cause` property and error chaining?**

```javascript
// Error.cause — ES2022: attach original error when wrapping
// Creates chain of errors preserving full context

async function fetchUserData(userId) {
  try {
    const res = await fetch(`/api/users/${userId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return await res.json();
  } catch (err) {
    // Wrap with context, preserve original:
    throw new Error(`Failed to fetch user ${userId}`, { cause: err });
  }
}

async function renderUserProfile(userId) {
  try {
    const user = await fetchUserData(userId);
    return renderTemplate(user);
  } catch (err) {
    throw new Error("Failed to render user profile", { cause: err });
  }
}

// Consuming the chain:
try {
  await renderUserProfile("abc");
} catch (err) {
  console.error(err.message);        // "Failed to render user profile"
  console.error(err.cause?.message); // "Failed to fetch user abc"
  console.error(err.cause?.cause?.message); // "HTTP 404: Not Found"

  // Walk the chain:
  function getRootCause(err) {
    return err.cause ? getRootCause(err.cause) : err;
  }
  getRootCause(err).message; // "HTTP 404: Not Found"
}

// Custom error with cause:
class DatabaseError extends Error {
  constructor(message, options) {
    super(message, options); // passes { cause } to Error
    this.name = "DatabaseError";
    this.code = options?.code;
  }
}

throw new DatabaseError("Query failed", {
  cause: originalDbError,
  code: "QUERY_TIMEOUT"
});
```

---

**Q123. What is the `using` declaration with disposable pattern in JavaScript?**

```javascript
// Explicit Resource Management (Stage 4 / ES2025, available in TypeScript 5.2+)
// Automatically calls [Symbol.dispose]() when scope exits

// Implementing Disposable:
class DatabaseConnection {
  #closed = false;

  async query(sql) {
    if (this.#closed) throw new Error("Connection closed");
    return db.execute(sql);
  }

  [Symbol.dispose]() {
    this.#closed = true;
    connectionPool.release(this);
    console.log("Connection returned to pool");
  }
}

// Sync using:
function processData() {
  using conn = connectionPool.acquire();
  // conn auto-disposed when scope exits (even on throw!)
  return conn.query("SELECT * FROM data");
} // [Symbol.dispose]() called here

// Async using:
class FileHandle {
  async [Symbol.asyncDispose]() {
    await fs.promises.close(this.fd);
  }
}

async function readConfig(path) {
  await using file = await openFileHandle(path);
  return file.read();
} // asyncDispose called automatically

// DisposableStack — manage multiple resources:
function setupResources() {
  using stack = new DisposableStack();

  const conn = stack.use(new DatabaseConnection()); // registered
  const lock = stack.use(acquireLock("resource"));  // registered
  stack.defer(() => cleanupTemp());                  // custom cleanup

  return process(conn, lock);
  // All disposed in LIFO order on scope exit
}

// Error safety — dispose runs even if body throws:
function riskyOperation() {
  using resource = expensiveResource();
  throw new Error("something failed");
  // resource STILL disposed despite error!
}
```

---

**Q124. Explain `Array.prototype.at()`, `Object.hasOwn()`, and other recent additions.**

```javascript
// ES2022 additions:

// 1. Array.at() — negative indexing
const arr = [1, 2, 3, 4, 5];
arr.at(0);   // 1 — same as arr[0]
arr.at(-1);  // 5 — last element
arr.at(-2);  // 4 — second to last
// vs arr[arr.length - 1] — more readable!
// Works on strings too:
"hello".at(-1); // "o"

// 2. Object.hasOwn() — safer than hasOwnProperty
const nullProto = Object.create(null);
nullProto.key = "value";
nullProto.hasOwnProperty("key"); // TypeError — no prototype!
Object.hasOwn(nullProto, "key"); // true ✅

// 3. Error.cause (covered in Q122)

// 4. Class static blocks — run code when class is defined
class Config {
  static debug;
  static logLevel;

  static {
    // Complex initialization (can use try/catch, loops, etc.)
    try {
      const env = JSON.parse(process.env.APP_CONFIG ?? "{}");
      Config.debug = env.debug ?? false;
      Config.logLevel = env.logLevel ?? "info";
    } catch {
      Config.debug = false;
      Config.logLevel = "info";
    }
  }
}

// 5. Private class fields in — check without try/catch
class PersonWithPrivate {
  #name;
  constructor(name) { this.#name = name; }
  static isValid(obj) { return #name in obj; } // ✅ clean check
}
PersonWithPrivate.isValid(new PersonWithPrivate("Alice")); // true
PersonWithPrivate.isValid({}); // false (no #name)

// 6. at() on TypedArray:
new Uint8Array([10, 20, 30]).at(-1); // 30
```

---

**Q125. What is `Promise.withResolvers()` and its use cases?**

```javascript
// ES2024 — expose resolve/reject outside the Promise constructor

// OLD way — awkward variable capture:
let resolve, reject;
const promise = new Promise((res, rej) => {
  resolve = res; // capture from callback
  reject = rej;
});
// resolve and reject are now available... but eslint may warn

// NEW way — clean:
const { promise, resolve, reject } = Promise.withResolvers();
// All three available immediately, no callback needed

// Use case 1: Deferred pattern
class Deferred {
  constructor() {
    Object.assign(this, Promise.withResolvers());
  }
}

const d = new Deferred();
setTimeout(() => d.resolve("result"), 1000);
await d.promise; // "result"

// Use case 2: Expose promise completion to caller
function createTimeout(ms) {
  const { promise, resolve, reject } = Promise.withResolvers();
  const id = setTimeout(() => resolve(), ms);

  return {
    promise,
    cancel() {
      clearTimeout(id);
      reject(new Error("Cancelled"));
    }
  };
}

const timeout = createTimeout(5000);
timeout.cancel(); // cancel before it fires

// Use case 3: Queue with async pop
class AsyncQueue {
  #items = [];
  #waiters = [];

  push(item) {
    if (this.#waiters.length) {
      const { resolve } = this.#waiters.shift();
      resolve(item);
    } else {
      this.#items.push(item);
    }
  }

  pop() {
    if (this.#items.length) return Promise.resolve(this.#items.shift());
    const { promise, resolve } = Promise.withResolvers();
    this.#waiters.push({ resolve });
    return promise;
  }
}
```

---

**Q126. What is object rest/spread with nested destructuring patterns?**

```javascript
// Advanced destructuring combinations:

// Nested with defaults and renaming:
const { 
  user: { 
    name: userName = "Anonymous",
    address: { city = "Unknown", zip } = {}
  } = {}
} = apiResponse ?? {};

// Rest in objects:
const { id, createdAt, updatedAt, ...publicData } = user;
// publicData = everything except id, createdAt, updatedAt

// Computed property keys in destructuring:
const key = "name";
const { [key]: value } = { name: "Alice" };
value; // "Alice"

// Destructuring in function params with defaults:
function createServer({
  host = "localhost",
  port = 3000,
  tls: { enabled = false, cert, key } = {},
  middleware = [],
  ...options
} = {}) {
  return { host, port, tlsEnabled: enabled, cert, key, middleware, ...options };
}

// Swap multiple variables:
let a = 1, b = 2, c = 3;
[a, b, c] = [c, a, b]; // a=3, b=1, c=2

// Ignore elements with holes:
const [,, third, , fifth = "default"] = [1, 2, 3, 4];
third; // 3, fifth; // "default"

// Iterator destructuring (any iterable):
const [x, y, z] = new Set([10, 20, 30]);
const [first, ...rest] = "hello"; // first="h", rest=["e","l","l","o"]

// Nested array + object:
const [{ name: firstName }, { name: secondName }] = users;
```

---

**Q127. What is `globalThis` and cross-environment JavaScript?**

```javascript
// Before globalThis — environment-specific global access:
// Browser main thread: window, self
// Browser worker: self (no window!)
// Node.js: global (no window!)
// Deno: globalThis (modern)

// globalThis — universal (ES2020):
globalThis.setTimeout === setTimeout; // true everywhere

// Feature detection pattern:
const isBrowser = typeof globalThis.window !== "undefined"
  && typeof globalThis.document !== "undefined";

const isNode = typeof globalThis.process !== "undefined"
  && globalThis.process.versions?.node != null;

const isWebWorker = typeof globalThis.WorkerGlobalScope !== "undefined"
  && globalThis instanceof globalThis.WorkerGlobalScope;

const isDeno = typeof globalThis.Deno !== "undefined";
const isBun = typeof globalThis.Bun !== "undefined";

// Polyfill pattern:
if (typeof globalThis.fetch === "undefined") {
  if (isNode) {
    const { default: nodeFetch } = await import("node-fetch");
    globalThis.fetch = nodeFetch;
  }
}

// Environment-agnostic module:
export function getBaseURL() {
  if (isBrowser) return window.location.origin;
  if (isNode) return process.env.BASE_URL ?? "http://localhost:3000";
  return "http://localhost:3000";
}

// SharedArrayBuffer + globalThis in workers:
// Workers share globalThis.SharedArrayBuffer with main thread
const shared = new globalThis.SharedArrayBuffer(1024);
```

---

**Q128. What are the latest ES2024/ES2025 additions to JavaScript?**

```javascript
// ES2024:

// 1. Object.groupBy and Map.groupBy:
const people = [
  { name: "Alice", dept: "eng" },
  { name: "Bob",   dept: "mkt" },
  { name: "Carol", dept: "eng" },
];
const byDept = Object.groupBy(people, p => p.dept);
// { eng: [Alice, Carol], mkt: [Bob] }

Map.groupBy(people, p => p.dept);
// Map { "eng" => [Alice, Carol], "mkt" => [Bob] }

// 2. Promise.withResolvers() (covered in Q125)

// 3. ArrayBuffer resizable + transfer:
const buf = new ArrayBuffer(8, { maxByteLength: 64 }); // resizable
buf.resize(32);           // grow to 32 bytes
const newBuf = buf.transfer(16); // new 16-byte buffer, old detached

// 4. String.prototype.isWellFormed():
"hello\uD800".isWellFormed(); // false — lone surrogate
"hello\uD800".toWellFormed(); // "hello\uFFFD" — replacement char
"hello".isWellFormed();       // true

// ES2025 (Stage 4 / shipping):

// 1. Set methods:
const a = new Set([1, 2, 3]);
const b = new Set([2, 3, 4]);
a.union(b);               // Set {1,2,3,4}
a.intersection(b);        // Set {2,3}
a.difference(b);          // Set {1}
a.symmetricDifference(b); // Set {1,4}
a.isSubsetOf(b);          // false
a.isSupersetOf(new Set([1,2])); // true
a.isDisjointFrom(new Set([5,6])); // true

// 2. Import attributes:
import data from "./data.json" with { type: "json" };
import styles from "./styles.css" with { type: "css" };

// 3. Iterator methods (iterator helpers):
function* range(n) { for (let i = 0; i < n; i++) yield i; }

range(10).filter(n => n % 2 === 0).map(n => n * n).take(3).toArray();
// [0, 4, 16]
// No need to spread to array first!

range(Infinity).filter(isPrime).take(10).toArray(); // first 10 primes — lazy!
```

---

**Q129. How does JavaScript handle tail calls and deep recursion safely?**

```javascript
// Stack overflow occurs when call stack exceeds limit (~10K-15K frames in V8)

// PROBLEM — recursive fibonacci O(2^n):
function fib(n) {
  if (n <= 1) return n;
  return fib(n-1) + fib(n-2); // stack grows with each call
}
fib(50); // Stack overflow! (without memoization)

// SOLUTION 1: Memoization (cache results):
function fibMemo(n, memo = new Map()) {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n);
  const r = fibMemo(n-1, memo) + fibMemo(n-2, memo);
  memo.set(n, r);
  return r;
}
fibMemo(1000); // works — each n computed once

// SOLUTION 2: Iteration (always preferred for large n):
function fibIter(n) {
  if (n <= 1) return n;
  let [a, b] = [0, 1];
  for (let i = 2; i <= n; i++) [a, b] = [b, a + b];
  return b;
}

// SOLUTION 3: Trampoline (manual tail call optimization):
function trampoline(fn) {
  return function(...args) {
    let result = fn(...args);
    while (typeof result === "function") result = result();
    return result;
  };
}

const safeFib = trampoline(function fib(n, a = 0, b = 1) {
  if (n === 0) return a;
  if (n === 1) return b;
  return () => fib(n - 1, b, a + b); // return thunk instead of recursing
});

safeFib(100000); // works — constant stack space

// SOLUTION 4: Generator-based recursion:
function* fibGen() {
  let [a, b] = [0, 1];
  while (true) { yield a; [a, b] = [b, a + b]; }
}

// Get nth fibonacci:
function fibN(n) {
  const gen = fibGen();
  for (let i = 0; i < n; i++) gen.next();
  return gen.next().value;
}
```

---

**Q130. What are JavaScript module loading edge cases and circular dependency handling?**

```javascript
// CIRCULAR DEPENDENCIES in ESM:

// a.mjs:
export const a = "a";
export { b } from "./b.mjs"; // imports from b which imports from a!

// b.mjs:
import { a } from "./a.mjs"; // a might not be initialized yet!
export const b = `b needs ${a}`;

// ESM handles this via "live bindings" and two-pass evaluation:
// Pass 1: LINK — all modules parsed, binding records created (uninitialized)
// Pass 2: EVALUATE — modules executed depth-first

// Circular: a → b → a
// Evaluation order: b evaluated first (it's required by a), then a
// When b runs: `a` is an UNINITIALIZED binding (TDZ for module bindings)
// Result: ReferenceError if b tries to use `a` at module top level!

// SAFE circular pattern — use functions (lazy evaluation):
// a.mjs:
export function getA() { return "a"; } // function — not evaluated until called
export { getB } from "./b.mjs";

// b.mjs:
import { getA } from "./a.mjs";
export function getB() { return `b needs ${getA()}`; } // getA called lazily

// By the time getB() is called, getA is initialized ✅

// CJS circular (different behavior — synchronous, partial exports):
// a.js:
const b = require("./b"); // b.js starts loading
module.exports.a = "a";   // exports.a set after b loaded

// b.js:
const a = require("./a"); // gets PARTIAL exports (empty {} at this point!)
console.log(a.a); // undefined — a.js hasn't set exports.a yet!
module.exports.b = "b";

// CJS circular gives partial object — usually undefined for missing exports
// ESM circular gives uninitialized binding (TDZ) — throws if accessed early

// Best practice: avoid circular dependencies
// If needed: use factory functions or inject dependencies explicitly
```

---

*JavaScript file now contains 130 complete questions (Q1–Q130). Q1–Q110 cover fundamentals through advanced internals. Q111–Q130 cover ES2022–2025 features, Proxy traps, async generators, error chaining, and module loading edge cases.*
