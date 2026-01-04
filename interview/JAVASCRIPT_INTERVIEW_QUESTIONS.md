# JavaScript Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is JavaScript? Explain its key features.

**Answer:**
JavaScript is a high-level, interpreted programming language primarily used for web development.

**Key Features:**
- **Dynamic Typing**: Types determined at runtime
- **First-Class Functions**: Functions are objects
- **Prototype-Based**: Objects inherit from other objects
- **Event-Driven**: Asynchronous programming model
- **Single-Threaded**: Uses event loop for concurrency
- **Closures**: Functions can access outer scope

### 2. Explain the difference between `var`, `let`, and `const`.

**Answer:**
- **var**: Function-scoped, hoisted, can be redeclared
- **let**: Block-scoped, temporal dead zone, cannot be redeclared
- **const**: Block-scoped, must be initialized, cannot be reassigned

```javascript
// var - function scoped
function example() {
    console.log(x); // undefined (hoisted)
    var x = 5;
    if (true) {
        var y = 10; // Function-scoped
    }
    console.log(y); // 10
}

// let - block scoped
function example() {
    // console.log(x); // ReferenceError (TDZ)
    let x = 5;
    if (true) {
        let y = 10; // Block-scoped
    }
    // console.log(y); // ReferenceError
}

// const - block scoped, immutable binding
const PI = 3.14159;
// PI = 3.14; // TypeError

const obj = { name: "John" };
obj.name = "Jane"; // OK - object is mutable
// obj = {}; // TypeError - cannot reassign
```

### 3. What is hoisting in JavaScript?

**Answer:**
Hoisting is JavaScript's behavior of moving declarations to the top of their scope.

```javascript
// Function declarations are fully hoisted
console.log(hoisted()); // "Hello" - works!

function hoisted() {
    return "Hello";
}

// var declarations are hoisted but not initialized
console.log(x); // undefined (not ReferenceError)
var x = 5;

// let/const are hoisted but in Temporal Dead Zone
// console.log(y); // ReferenceError
let y = 5;
```

### 4. Explain `this` keyword in JavaScript.

**Answer:**
`this` refers to the object that owns the function. Its value depends on how the function is called.

```javascript
// Global context
console.log(this); // Window (browser) or global (Node)

// Object method
const obj = {
    name: "John",
    greet: function() {
        console.log(this.name); // "John"
    }
};

// Arrow function (lexical this)
const obj2 = {
    name: "John",
    greet: () => {
        console.log(this.name); // undefined (this = outer scope)
    },
    greet2: function() {
        setTimeout(() => {
            console.log(this.name); // "John" (arrow preserves this)
        }, 100);
    }
};

// Explicit binding
function greet() {
    console.log(this.name);
}
const person = { name: "John" };
greet.call(person);    // "John"
greet.apply(person);    // "John"
const bound = greet.bind(person);
bound(); // "John"
```

### 5. What is the difference between `==` and `===`?

**Answer:**
- **`==`**: Loose equality, performs type coercion
- **`===`**: Strict equality, no type coercion

```javascript
5 == "5";   // true (coercion)
5 === "5";  // false (no coercion)

null == undefined;   // true
null === undefined;  // false

0 == false;   // true
0 === false;  // false

[] == false;   // true (coercion)
[] === false;  // false
```

**Best Practice**: Always use `===` unless you specifically need coercion.

### 6. Explain closures in JavaScript.

**Answer:**
A closure is a function that has access to variables in its outer (enclosing) scope even after the outer function has returned.

```javascript
function outer() {
    let count = 0;
    
    return function inner() {
        count++;
        return count;
    };
}

const counter = outer();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3

// Each call to outer() creates a new closure
const counter2 = outer();
console.log(counter2()); // 1 (independent)
```

**Use Cases:**
- Data privacy
- Function factories
- Event handlers
- Callbacks

### 7. What are the different data types in JavaScript?

**Answer:**
**Primitive Types:**
- `string`, `number`, `boolean`, `undefined`, `null`, `symbol`, `bigint`

**Reference Types:**
- `object` (includes arrays, functions, dates, etc.)

```javascript
typeof "hello";     // "string"
typeof 42;          // "number"
typeof true;        // "boolean"
typeof undefined;   // "undefined"
typeof null;        // "object" (historical bug)
typeof Symbol();    // "symbol"
typeof 1n;          // "bigint"
typeof {};          // "object"
typeof [];          // "object"
typeof function(){}; // "function"
```

### 8. Explain the difference between `null` and `undefined`.

**Answer:**
- **`undefined`**: Variable declared but not assigned, missing property
- **`null`**: Explicitly assigned value representing "no value"

```javascript
let x;
console.log(x); // undefined

let y = null;
console.log(y); // null

// typeof
typeof undefined; // "undefined"
typeof null;      // "object"

// Equality
null == undefined;   // true
null === undefined;  // false
```

---

## Intermediate Level

### 9. Explain promises and async/await.

**Answer:**
**Promises:**
```javascript
// Creating promise
const promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("Success!");
    }, 1000);
});

// Consuming promise
promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));

// Promise methods
Promise.all([promise1, promise2, promise3])
    .then(results => console.log(results));

Promise.race([promise1, promise2])
    .then(result => console.log(result));
```

**Async/Await:**
```javascript
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

// Parallel execution
async function fetchAll() {
    const [data1, data2] = await Promise.all([
        fetchData1(),
        fetchData2()
    ]);
    return { data1, data2 };
}
```

### 10. Explain the event loop and how JavaScript handles asynchrony.

**Answer:**
JavaScript is single-threaded but uses an event loop for concurrency.

**Event Loop Phases:**
1. Call Stack: Synchronous code execution
2. Web APIs: Browser APIs (setTimeout, fetch, etc.)
3. Callback Queue: Queued callbacks
4. Event Loop: Moves callbacks from queue to stack

```javascript
console.log("1");

setTimeout(() => {
    console.log("2");
}, 0);

Promise.resolve().then(() => {
    console.log("3");
});

console.log("4");

// Output: 1, 4, 3, 2
// Microtasks (Promises) run before macrotasks (setTimeout)
```

**Execution Order:**
1. Synchronous code
2. Microtasks (Promises, queueMicrotask)
3. Macrotasks (setTimeout, setInterval, I/O)

### 11. Explain prototypal inheritance in JavaScript.

**Answer:**
JavaScript uses prototypal inheritance - objects inherit from other objects.

```javascript
// Prototype chain
function Person(name) {
    this.name = name;
}

Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

function Student(name, school) {
    Person.call(this, name);
    this.school = school;
}

// Inherit from Person
Student.prototype = Object.create(Person.prototype);
Student.prototype.constructor = Student;

Student.prototype.study = function() {
    return `${this.name} studies at ${this.school}`;
};

const student = new Student("John", "MIT");
console.log(student.greet()); // "Hello, I'm John"
console.log(student.study()); // "John studies at MIT"

// ES6 Classes
class Person {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}

class Student extends Person {
    constructor(name, school) {
        super(name);
        this.school = school;
    }
    
    study() {
        return `${this.name} studies at ${this.school}`;
    }
}
```

### 12. Explain `call`, `apply`, and `bind`.

**Answer:**
Methods to explicitly set `this` and pass arguments.

```javascript
function greet(greeting, punctuation) {
    return `${greeting}, ${this.name}${punctuation}`;
}

const person = { name: "John" };

// call - arguments as comma-separated values
greet.call(person, "Hello", "!"); // "Hello, John!"

// apply - arguments as array
greet.apply(person, ["Hello", "!"]); // "Hello, John!"

// bind - returns new function with bound this
const boundGreet = greet.bind(person);
boundGreet("Hello", "!"); // "Hello, John!"

// Partial application
const sayHello = greet.bind(person, "Hello");
sayHello("!"); // "Hello, John!"
```

### 13. Explain debouncing and throttling.

**Answer:**
**Debouncing**: Execute function after delay, reset on each call.
```javascript
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Usage
const debouncedSearch = debounce((query) => {
    console.log("Searching:", query);
}, 300);
```

**Throttling**: Execute function at most once per time period.
```javascript
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Usage
const throttledScroll = throttle(() => {
    console.log("Scrolled");
}, 100);
```

### 14. Explain the difference between `map`, `filter`, and `reduce`.

**Answer:**
```javascript
const numbers = [1, 2, 3, 4, 5];

// map - transform each element
const doubled = numbers.map(n => n * 2);
// [2, 4, 6, 8, 10]

// filter - select elements
const evens = numbers.filter(n => n % 2 === 0);
// [2, 4]

// reduce - accumulate to single value
const sum = numbers.reduce((acc, n) => acc + n, 0);
// 15

// Chaining
const result = numbers
    .filter(n => n % 2 === 0)
    .map(n => n * 2)
    .reduce((acc, n) => acc + n, 0);
// 12
```

### 15. Explain currying in JavaScript.

**Answer:**
Currying is converting a function that takes multiple arguments into a series of functions that each take one argument.

```javascript
// Regular function
function add(a, b, c) {
    return a + b + c;
}

// Curried version
function curriedAdd(a) {
    return function(b) {
        return function(c) {
            return a + b + c;
        };
    };
}

// ES6 arrow function
const curriedAdd = a => b => c => a + b + c;

curriedAdd(1)(2)(3); // 6

// Partial application
const add5 = curriedAdd(5);
const add5And10 = add5(10);
add5And10(15); // 30

// Generic curry function
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        } else {
            return function(...nextArgs) {
                return curried.apply(this, args.concat(nextArgs));
            };
        }
    };
}
```

### 16. Explain the module system (CommonJS vs ES6 modules).

**Answer:**
**CommonJS (Node.js):**
```javascript
// math.js
module.exports = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b
};

// Or
exports.add = (a, b) => a + b;

// app.js
const math = require('./math');
const { add } = require('./math');
```

**ES6 Modules:**
```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export default function multiply(a, b) {
    return a * b;
}

// app.js
import multiply, { add, subtract } from './math';
import * as math from './math';
```

**Differences:**
- CommonJS: Synchronous, runtime, dynamic
- ES6: Asynchronous, compile-time, static

---

## Advanced Level

### 17. Explain the Proxy API in JavaScript.

**Answer:**
Proxy allows you to intercept and customize operations on objects.

```javascript
const handler = {
    get(target, prop) {
        return prop in target ? target[prop] : 37;
    },
    set(target, prop, value) {
        if (typeof value === 'number') {
            target[prop] = value;
            return true;
        }
        return false;
    },
    has(target, prop) {
        return prop in target;
    },
    deleteProperty(target, prop) {
        delete target[prop];
        return true;
    }
};

const proxy = new Proxy({}, handler);
proxy.a = 1;
console.log(proxy.a); // 1
console.log(proxy.b); // 37 (default value)

// Use cases: Validation, logging, virtual properties
```

### 18. Explain generators and iterators.

**Answer:**
**Generators:**
```javascript
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = numberGenerator();
console.log(gen.next()); // {value: 1, done: false}
console.log(gen.next()); // {value: 2, done: false}
console.log(gen.next()); // {value: 3, done: false}
console.log(gen.next()); // {value: undefined, done: true}

// Infinite generator
function* infiniteSequence() {
    let i = 0;
    while (true) {
        yield i++;
    }
}

// Generator with parameters
function* generatorWithParams() {
    const x = yield "First";
    const y = yield x + " Second";
    return y + " Third";
}
```

**Iterators:**
```javascript
const iterable = {
    [Symbol.iterator]() {
        let step = 0;
        return {
            next() {
                step++;
                if (step === 1) return {value: "Hello", done: false};
                if (step === 2) return {value: "World", done: false};
                return {done: true};
            }
        };
    }
};

for (const value of iterable) {
    console.log(value);
}
```

### 19. Explain memory leaks in JavaScript and how to prevent them.

**Answer:**
**Common Causes:**
1. **Global Variables**
```javascript
// Bad
function leak() {
    globalVar = "leak"; // Creates global variable
}

// Good
function noLeak() {
    const localVar = "no leak";
}
```

2. **Closures**
```javascript
// Bad - keeps reference to large object
function createClosure() {
    const largeObject = new Array(1000000).fill(0);
    return function() {
        console.log(largeObject.length); // Keeps reference
    };
}

// Good - don't reference if not needed
function createClosure() {
    const largeObject = new Array(1000000).fill(0);
    return function() {
        // Don't reference largeObject
    };
}
```

3. **Event Listeners**
```javascript
// Bad - not removing listeners
element.addEventListener('click', handler);

// Good - remove when done
element.addEventListener('click', handler);
element.removeEventListener('click', handler);
```

4. **Timers**
```javascript
// Bad - not clearing
const timer = setInterval(() => {}, 1000);

// Good - clear when done
const timer = setInterval(() => {}, 1000);
clearInterval(timer);
```

### 20. Explain the difference between shallow and deep copy.

**Answer:**
**Shallow Copy:**
```javascript
const original = { a: 1, b: { c: 2 } };
const shallow = Object.assign({}, original);
// Or
const shallow2 = { ...original };

shallow.b.c = 3;
console.log(original.b.c); // 3 (changed!)
```

**Deep Copy:**
```javascript
// Method 1: JSON (limitations: no functions, dates, etc.)
const deep = JSON.parse(JSON.stringify(original));

// Method 2: structuredClone (modern browsers)
const deep2 = structuredClone(original);

// Method 3: Custom recursive function
function deepCopy(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj);
    if (obj instanceof Array) return obj.map(item => deepCopy(item));
    if (typeof obj === 'object') {
        const copy = {};
        Object.keys(obj).forEach(key => {
            copy[key] = deepCopy(obj[key]);
        });
        return copy;
    }
}
```

### 21. Explain the difference between `Object.create()`, `new`, and class syntax.

**Answer:**
```javascript
// Object.create - creates object with specified prototype
const proto = { greet: function() { return "Hello"; } };
const obj = Object.create(proto);
console.log(obj.greet()); // "Hello"

// new - constructor function
function Person(name) {
    this.name = name;
}
Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};
const person = new Person("John");

// class - syntactic sugar
class Person {
    constructor(name) {
        this.name = name;
    }
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}
const person2 = new Person("John");
```

### 22. Explain Web Workers and how they work.

**Answer:**
Web Workers allow JavaScript to run in background threads.

```javascript
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ data: "Hello" });
worker.onmessage = (event) => {
    console.log(event.data);
};

// worker.js
self.onmessage = (event) => {
    const result = processData(event.data);
    self.postMessage(result);
};

function processData(data) {
    // Heavy computation
    return data.toUpperCase();
}
```

**Limitations:**
- No DOM access
- Limited global objects
- Communication via messages only

### 23. Explain the difference between `setTimeout`, `setImmediate`, and `process.nextTick` (Node.js).

**Answer:**
**Execution Order:**
```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);
setImmediate(() => console.log("3"));
process.nextTick(() => console.log("4"));

console.log("5");

// Output: 1, 5, 4, 2, 3
// process.nextTick runs before setTimeout/setImmediate
```

**Differences:**
- **process.nextTick**: Highest priority, runs before event loop
- **setImmediate**: Runs in check phase of event loop
- **setTimeout**: Runs in timer phase of event loop

### 24. Explain memoization in JavaScript.

**Answer:**
Memoization caches function results to avoid redundant calculations.

```javascript
function memoize(fn) {
    const cache = {};
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache[key]) {
            return cache[key];
        }
        const result = fn.apply(this, args);
        cache[key] = result;
        return result;
    };
}

// Usage
const expensiveFunction = (n) => {
    console.log("Computing...");
    return n * 2;
};

const memoized = memoize(expensiveFunction);
memoized(5); // Computing... 10
memoized(5); // 10 (from cache)
```

### 25. Explain the difference between `for...in` and `for...of`.

**Answer:**
```javascript
const arr = [1, 2, 3];
arr.customProp = "custom";

// for...in - iterates over enumerable properties (keys)
for (let key in arr) {
    console.log(key); // "0", "1", "2", "customProp"
}

// for...of - iterates over iterable values
for (let value of arr) {
    console.log(value); // 1, 2, 3
}

// Object iteration
const obj = { a: 1, b: 2, c: 3 };

for (let key in obj) {
    console.log(key, obj[key]); // "a" 1, "b" 2, "c" 3
}

// for...of with Object.entries
for (let [key, value] of Object.entries(obj)) {
    console.log(key, value); // "a" 1, "b" 2, "c" 3
}
```

### 26. Explain Symbol in JavaScript.

**Answer:**
Symbol is unique, immutable primitive type.

```javascript
// Create symbol
const sym1 = Symbol('description');
const sym2 = Symbol('description');
console.log(sym1 === sym2); // false (unique)

// Use as object key
const obj = {
    [sym1]: 'value1',
    [sym2]: 'value2'
};

// Well-known symbols
const arr = [1, 2, 3];
arr[Symbol.iterator] = function*() {
    yield 1;
    yield 2;
    yield 3;
};
```

### 27. Explain BigInt in JavaScript.

**Answer:**
BigInt represents integers larger than Number.MAX_SAFE_INTEGER.

```javascript
// Create BigInt
const bigInt = 9007199254740991n;
const bigInt2 = BigInt(9007199254740991);

// Operations
const sum = bigInt + 1n;
const product = bigInt * 2n;

// Cannot mix with Number
// const result = bigInt + 1; // TypeError
const result = bigInt + BigInt(1);
```

### 28. Explain Optional Chaining and Nullish Coalescing.

**Answer:**
**Optional Chaining (?.):**
```javascript
const user = {
    address: {
        street: '123 Main St'
    }
};

// Safe property access
const street = user?.address?.street; // "123 Main St"
const zip = user?.address?.zip; // undefined (no error)

// Safe method call
user?.getName?.(); // Only calls if exists

// Safe array access
const first = arr?.[0];
```

**Nullish Coalescing (??):**
```javascript
// Only null/undefined, not falsy values
const value = null ?? 'default'; // 'default'
const value2 = 0 ?? 'default'; // 0 (not 'default')
const value3 = '' ?? 'default'; // '' (not 'default')

// Combined
const name = user?.name ?? 'Anonymous';
```

### 29. Explain Array methods: flat, flatMap, and at.

**Answer:**
**flat():**
```javascript
const arr = [1, [2, 3], [4, [5, 6]]];
arr.flat(); // [1, 2, 3, 4, [5, 6]]
arr.flat(2); // [1, 2, 3, 4, 5, 6]
arr.flat(Infinity); // Flatten all levels
```

**flatMap():**
```javascript
const arr = [1, 2, 3];
arr.flatMap(x => [x, x * 2]); // [1, 2, 2, 4, 3, 6]
// Equivalent to: arr.map(...).flat()
```

**at():**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.at(0); // 1
arr.at(-1); // 5 (last element)
arr.at(-2); // 4
```

### 30. Explain Object methods: Object.assign, Object.entries, Object.fromEntries.

**Answer:**
**Object.assign():**
```javascript
const target = { a: 1 };
const source = { b: 2, c: 3 };
Object.assign(target, source); // { a: 1, b: 2, c: 3 }

// Shallow copy
const copy = Object.assign({}, source);
```

**Object.entries():**
```javascript
const obj = { a: 1, b: 2, c: 3 };
Object.entries(obj); // [['a', 1], ['b', 2], ['c', 3]]

// Convert to Map
const map = new Map(Object.entries(obj));
```

**Object.fromEntries():**
```javascript
const entries = [['a', 1], ['b', 2], ['c', 3]];
Object.fromEntries(entries); // { a: 1, b: 2, c: 3 }

// Convert from Map
const map = new Map([['a', 1], ['b', 2]]);
Object.fromEntries(map); // { a: 1, b: 2 }
```

---

This covers JavaScript interview questions from beginner to advanced level with detailed explanations and code examples.

