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

### 31. Explain WeakMap and WeakSet.

**Answer:**
**WeakMap:**
- Keys must be objects
- Weak references (garbage collectable)
- No iteration methods
- No size property

```javascript
const weakMap = new WeakMap();
const obj = {};

weakMap.set(obj, 'value');
console.log(weakMap.get(obj)); // 'value'

// When obj is garbage collected, entry is removed
```

**WeakSet:**
- Values must be objects
- Weak references
- No iteration methods

```javascript
const weakSet = new WeakSet();
const obj = {};

weakSet.add(obj);
console.log(weakSet.has(obj)); // true
```

**Use Cases:**
- Storing metadata about objects
- Private data storage
- DOM element tracking

### 32. Explain Reflect API.

**Answer:**
Reflect provides methods for interceptable operations.

```javascript
const obj = { name: 'John', age: 30 };

// Reflect.get
Reflect.get(obj, 'name'); // 'John'

// Reflect.set
Reflect.set(obj, 'name', 'Jane');

// Reflect.has
Reflect.has(obj, 'name'); // true

// Reflect.ownKeys
Reflect.ownKeys(obj); // ['name', 'age']

// Reflect.construct
class Person {
    constructor(name) {
        this.name = name;
    }
}
const person = Reflect.construct(Person, ['John']);

// Reflect.apply
Reflect.apply(Math.max, null, [1, 2, 3]); // 3
```

**Benefits:**
- Works with Proxy
- Returns boolean for success/failure
- More functional style

### 33. Explain Promise.allSettled, Promise.any, and Promise.race in detail.

**Answer:**
**Promise.allSettled:**
```javascript
// Waits for all promises, doesn't reject
Promise.allSettled([promise1, promise2, promise3])
    .then(results => {
        results.forEach(result => {
            if (result.status === 'fulfilled') {
                console.log('Success:', result.value);
            } else {
                console.log('Failed:', result.reason);
            }
        });
    });
```

**Promise.any:**
```javascript
// Resolves with first fulfilled promise
Promise.any([promise1, promise2, promise3])
    .then(first => console.log('First success:', first))
    .catch(errors => console.log('All failed:', errors));
```

**Promise.race:**
```javascript
// Resolves/rejects with first settled promise
Promise.race([promise1, promise2])
    .then(result => console.log('First:', result));
```

### 34. Explain JavaScript memory management and garbage collection.

**Answer:**
JavaScript uses automatic garbage collection.

**Memory Lifecycle:**
1. **Allocation**: Memory allocated when creating objects
2. **Use**: Memory used by program
3. **Release**: Garbage collector frees unused memory

**Garbage Collection Algorithms:**

**Mark-and-Sweep:**
- Marks reachable objects
- Sweeps unmarked objects
- Most common algorithm

**Reference Counting:**
- Counts references to objects
- Frees when count reaches zero
- Problem: Circular references

**Memory Leaks:**
```javascript
// Global variables
window.data = largeArray; // Never garbage collected

// Closures holding references
function outer() {
    const largeData = new Array(1000000).fill(0);
    return function inner() {
        // largeData kept in memory
        console.log('inner');
    };
}

// Event listeners
element.addEventListener('click', handler);
// Remove: element.removeEventListener('click', handler);

// Timers
const timer = setInterval(() => {}, 1000);
// Clear: clearInterval(timer);
```

**Best Practices:**
- Avoid global variables
- Remove event listeners
- Clear timers
- Use WeakMap/WeakSet for weak references

### 35. Explain JavaScript module systems (CommonJS, ES6, AMD).

**Answer:**
**CommonJS (Node.js):**
```javascript
// Export
module.exports = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b
};

// Or
exports.add = (a, b) => a + b;

// Import
const { add, subtract } = require('./math');
const math = require('./math');
```

**ES6 Modules:**
```javascript
// Export
export const add = (a, b) => a + b;
export default function subtract(a, b) { return a - b; }

// Import
import { add } from './math.js';
import subtract from './math.js';
import * as math from './math.js';
```

**AMD (Asynchronous Module Definition):**
```javascript
// Define
define(['dependency1', 'dependency2'], function(dep1, dep2) {
    return {
        method: function() {}
    };
});

// Require
require(['module'], function(module) {
    module.method();
});
```

**Differences:**
- **CommonJS**: Synchronous, runtime, Node.js
- **ES6**: Static, compile-time, browser/Node.js
- **AMD**: Asynchronous, browser (RequireJS)

### 36. Explain JavaScript proxy and reflect APIs.

**Answer:**
**Proxy:**
Proxy wraps object to intercept operations.

```javascript
const target = { name: 'John', age: 30 };

const handler = {
    get(target, prop) {
        console.log(`Getting ${prop}`);
        return target[prop];
    },
    set(target, prop, value) {
        console.log(`Setting ${prop} to ${value}`);
        target[prop] = value;
        return true;
    },
    has(target, prop) {
        return prop in target;
    },
    deleteProperty(target, prop) {
        delete target[prop];
        return true;
    }
};

const proxy = new Proxy(target, handler);
proxy.name; // Logs: Getting name
proxy.age = 31; // Logs: Setting age to 31
```

**Use Cases:**
- Validation
- Logging
- Default values
- Virtual properties

**Reflect:**
Reflect provides methods for proxy operations.

```javascript
const obj = { name: 'John' };

// Reflect methods mirror proxy traps
Reflect.get(obj, 'name'); // 'John'
Reflect.set(obj, 'age', 30); // true
Reflect.has(obj, 'name'); // true
Reflect.deleteProperty(obj, 'name'); // true
Reflect.ownKeys(obj); // ['age']
```

### 37. Explain JavaScript iterators and generators.

**Answer:**
**Iterators:**
Objects that implement iterator protocol.

```javascript
const iterable = {
    [Symbol.iterator]() {
        let count = 0;
        return {
            next() {
                if (count < 3) {
                    return { value: count++, done: false };
                }
                return { done: true };
            }
        };
    }
};

for (const value of iterable) {
    console.log(value); // 0, 1, 2
}
```

**Generators:**
Functions that return generator objects.

```javascript
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = numberGenerator();
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 3, done: false }
console.log(gen.next()); // { done: true }
```

**Generator Use Cases:**
```javascript
// Infinite sequence
function* fibonacci() {
    let [prev, curr] = [0, 1];
    while (true) {
        yield curr;
        [prev, curr] = [curr, prev + curr];
    }
}

// Lazy evaluation
function* filter(iterable, predicate) {
    for (const item of iterable) {
        if (predicate(item)) {
            yield item;
        }
    }
}
```

### 38. Explain the difference between `Object.freeze()`, `Object.seal()`, and `Object.preventExtensions()`.

**Answer:**
**Object.preventExtensions():**
```javascript
const obj = { name: "John" };
Object.preventExtensions(obj);
obj.age = 30; // Error in strict mode, silently fails otherwise
obj.name = "Jane"; // OK - can modify existing
delete obj.name; // OK - can delete
```

**Object.seal():**
```javascript
const obj = { name: "John" };
Object.seal(obj);
obj.age = 30; // Error - cannot add
obj.name = "Jane"; // OK - can modify existing
delete obj.name; // Error - cannot delete
```

**Object.freeze():**
```javascript
const obj = { name: "John" };
Object.freeze(obj);
obj.age = 30; // Error - cannot add
obj.name = "Jane"; // Error - cannot modify
delete obj.name; // Error - cannot delete
```

**Summary:**
- `preventExtensions`: Cannot add, can modify/delete
- `seal`: Cannot add/delete, can modify
- `freeze`: Cannot add/modify/delete (shallow)

### 39. Explain the difference between `Array.from()`, `Array.of()`, and spread operator.

**Answer:**
**Array.from():**
```javascript
// From array-like objects
Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']
Array.from({ length: 5 }, (_, i) => i); // [0, 1, 2, 3, 4]

// From iterables
Array.from(new Set([1, 2, 3])); // [1, 2, 3]
```

**Array.of():**
```javascript
Array.of(1, 2, 3); // [1, 2, 3]
Array.of(7); // [7] (not [7, undefined, undefined, undefined, undefined, undefined, undefined])
Array(7); // [empty × 7] - different behavior
```

**Spread Operator:**
```javascript
const arr = [1, 2, 3];
const newArr = [...arr]; // [1, 2, 3] - shallow copy

// Combining arrays
const combined = [...arr, 4, 5]; // [1, 2, 3, 4, 5]
```

### 40. Explain the difference between `setTimeout` and `setInterval`.

**Answer:**
**setTimeout:**
```javascript
// Executes once after delay
const timer = setTimeout(() => {
    console.log('Executed once');
}, 1000);

clearTimeout(timer); // Cancel before execution
```

**setInterval:**
```javascript
// Executes repeatedly at intervals
const interval = setInterval(() => {
    console.log('Executed repeatedly');
}, 1000);

clearInterval(interval); // Stop execution
```

**Common Pitfall:**
```javascript
// Wrong - creates multiple intervals
function startTimer() {
    setInterval(() => {
        console.log('Tick');
    }, 1000);
}

// Correct - single interval
let intervalId;
function startTimer() {
    if (!intervalId) {
        intervalId = setInterval(() => {
            console.log('Tick');
        }, 1000);
    }
}
```

### 41. Explain the difference between `Object.keys()`, `Object.values()`, and `Object.entries()`.

**Answer:**
```javascript
const obj = { a: 1, b: 2, c: 3 };

// Object.keys() - returns keys
Object.keys(obj); // ['a', 'b', 'c']

// Object.values() - returns values
Object.values(obj); // [1, 2, 3]

// Object.entries() - returns [key, value] pairs
Object.entries(obj); // [['a', 1], ['b', 2], ['c', 3]]

// Iteration
for (const [key, value] of Object.entries(obj)) {
    console.log(key, value);
}

// Convert to Map
const map = new Map(Object.entries(obj));
```

### 42. Explain the difference between `Array.isArray()` and `instanceof Array`.

**Answer:**
```javascript
// Array.isArray() - recommended
Array.isArray([]); // true
Array.isArray({}); // false
Array.isArray(null); // false

// instanceof - can fail with cross-frame/iframe
const arr = [];
arr instanceof Array; // true

// Problem with instanceof
const iframe = document.createElement('iframe');
document.body.appendChild(iframe);
const iframeArray = iframe.contentWindow.Array;
const arr2 = new iframeArray();
arr2 instanceof Array; // false (different Array constructor)
Array.isArray(arr2); // true (works correctly)
```

**Best Practice:** Always use `Array.isArray()`.

### 43. Explain the difference between `parseInt()` and `parseFloat()`.

**Answer:**
**parseInt():**
```javascript
parseInt('123'); // 123
parseInt('123.45'); // 123 (stops at decimal)
parseInt('123abc'); // 123 (stops at non-numeric)
parseInt('abc123'); // NaN
parseInt('10', 2); // 2 (binary)
parseInt('10', 8); // 8 (octal)
parseInt('10', 16); // 16 (hexadecimal)
```

**parseFloat():**
```javascript
parseFloat('123'); // 123
parseFloat('123.45'); // 123.45
parseFloat('123.45.67'); // 123.45 (stops at second decimal)
parseFloat('123abc'); // 123 (stops at non-numeric)
parseFloat('abc123'); // NaN
```

**Number():**
```javascript
Number('123'); // 123
Number('123.45'); // 123.45
Number('123abc'); // NaN (strict)
Number(''); // 0
Number(' '); // 0
```

### 44. Explain the difference between `String.slice()`, `String.substring()`, and `String.substr()`.

**Answer:**
**slice():**
```javascript
const str = 'Hello World';
str.slice(0, 5); // 'Hello'
str.slice(-5); // 'World' (negative index)
str.slice(5, 0); // '' (returns empty if start > end)
```

**substring():**
```javascript
const str = 'Hello World';
str.substring(0, 5); // 'Hello'
str.substring(-5); // 'Hello World' (treats negative as 0)
str.substring(5, 0); // 'Hello' (swaps if start > end)
```

**substr() (deprecated):**
```javascript
const str = 'Hello World';
str.substr(0, 5); // 'Hello' (start, length)
str.substr(-5); // 'World' (negative start from end)
str.substr(5, 0); // '' (length 0)
```

**Best Practice:** Use `slice()` for modern code.

### 45. Explain the difference between `Array.splice()` and `Array.slice()`.

**Answer:**
**slice() - Non-mutating:**
```javascript
const arr = [1, 2, 3, 4, 5];
const newArr = arr.slice(1, 3); // [2, 3]
console.log(arr); // [1, 2, 3, 4, 5] (unchanged)
```

**splice() - Mutating:**
```javascript
const arr = [1, 2, 3, 4, 5];
const removed = arr.splice(1, 2); // [2, 3]
console.log(arr); // [1, 4, 5] (modified)
console.log(removed); // [2, 3]

// Insert elements
arr.splice(1, 0, 'a', 'b'); // Insert at index 1
console.log(arr); // [1, 'a', 'b', 4, 5]

// Replace elements
arr.splice(1, 2, 'x', 'y'); // Replace 2 elements
console.log(arr); // [1, 'x', 'y', 4, 5]
```

### 46. Explain the difference between `Array.find()` and `Array.filter()`.

**Answer:**
**find() - Returns first match:**
```javascript
const users = [
    { id: 1, name: 'John', active: true },
    { id: 2, name: 'Jane', active: false },
    { id: 3, name: 'Bob', active: true }
];

const user = users.find(u => u.active); // { id: 1, name: 'John', active: true }
const user2 = users.find(u => u.id === 5); // undefined
```

**filter() - Returns all matches:**
```javascript
const activeUsers = users.filter(u => u.active);
// [{ id: 1, name: 'John', active: true }, { id: 3, name: 'Bob', active: true }]

const empty = users.filter(u => u.id === 5); // []
```

**Key Differences:**
- `find()` returns first element or `undefined`
- `filter()` returns array (empty if no matches)

### 47. Explain the difference between `Array.some()` and `Array.every()`.

**Answer:**
**some() - Returns true if any element passes:**
```javascript
const numbers = [1, 2, 3, 4, 5];
numbers.some(n => n > 3); // true (4 and 5 are > 3)
numbers.some(n => n > 10); // false (none > 10)
```

**every() - Returns true if all elements pass:**
```javascript
const numbers = [1, 2, 3, 4, 5];
numbers.every(n => n > 0); // true (all > 0)
numbers.every(n => n > 3); // false (1, 2, 3 are not > 3)
```

**Use Cases:**
```javascript
// Validation
const form = { name: 'John', age: 25, email: 'john@example.com' };
const isValid = Object.values(form).every(val => val !== '');
const hasEmpty = Object.values(form).some(val => val === '');
```

### 48. Explain the difference between `Array.includes()` and `Array.indexOf()`.

**Answer:**
**includes() - Returns boolean:**
```javascript
const arr = [1, 2, 3, NaN];
arr.includes(2); // true
arr.includes(4); // false
arr.includes(NaN); // true (correctly handles NaN)
arr.includes(2, 3); // false (starts from index 3)
```

**indexOf() - Returns index or -1:**
```javascript
const arr = [1, 2, 3, NaN];
arr.indexOf(2); // 1
arr.indexOf(4); // -1
arr.indexOf(NaN); // -1 (cannot find NaN)
arr.indexOf(2, 3); // -1 (starts from index 3)
```

**When to use:**
- `includes()`: Check existence (simpler)
- `indexOf()`: Need index position

### 49. Explain the difference between `String.trim()`, `String.trimStart()`, and `String.trimEnd()`.

**Answer:**
```javascript
const str = '  Hello World  ';

str.trim(); // 'Hello World' (both sides)
str.trimStart(); // 'Hello World  ' (left side)
str.trimEnd(); // '  Hello World' (right side)

// Legacy
str.trimLeft(); // Same as trimStart()
str.trimRight(); // Same as trimEnd()
```

### 50. Explain the difference between `String.startsWith()` and `String.endsWith()`.

**Answer:**
```javascript
const str = 'Hello World';

str.startsWith('Hello'); // true
str.startsWith('World'); // false
str.startsWith('World', 6); // true (starts from index 6)

str.endsWith('World'); // true
str.endsWith('Hello'); // false
str.endsWith('Hello', 5); // true (checks first 5 characters)
```

### 51. Explain the difference between `String.replace()` and `String.replaceAll()`.

**Answer:**
**replace() - Replaces first match:**
```javascript
const str = 'Hello World World';
str.replace('World', 'Universe'); // 'Hello Universe World'
str.replace(/World/g, 'Universe'); // 'Hello Universe Universe' (with regex)
```

**replaceAll() - Replaces all matches:**
```javascript
const str = 'Hello World World';
str.replaceAll('World', 'Universe'); // 'Hello Universe Universe'
str.replaceAll(/World/g, 'Universe'); // 'Hello Universe Universe'
```

### 52. Explain the difference between `Array.push()` and `Array.unshift()`.

**Answer:**
**push() - Adds to end:**
```javascript
const arr = [1, 2, 3];
arr.push(4); // [1, 2, 3, 4]
arr.push(5, 6); // [1, 2, 3, 4, 5, 6]
```

**unshift() - Adds to beginning:**
```javascript
const arr = [1, 2, 3];
arr.unshift(0); // [0, 1, 2, 3]
arr.unshift(-2, -1); // [-2, -1, 0, 1, 2, 3]
```

**Performance:** `push()` is faster than `unshift()` (no need to shift elements).

### 53. Explain the difference between `Array.pop()` and `Array.shift()`.

**Answer:**
**pop() - Removes from end:**
```javascript
const arr = [1, 2, 3];
const last = arr.pop(); // 3
console.log(arr); // [1, 2]
```

**shift() - Removes from beginning:**
```javascript
const arr = [1, 2, 3];
const first = arr.shift(); // 1
console.log(arr); // [2, 3]
```

**Performance:** `pop()` is faster than `shift()`.

### 54. Explain the difference between `Array.concat()` and spread operator for arrays.

**Answer:**
**concat() - Method:**
```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = arr1.concat(arr2); // [1, 2, 3, 4, 5, 6]
const combined2 = arr1.concat(arr2, [7, 8]); // [1, 2, 3, 4, 5, 6, 7, 8]
```

**Spread Operator - Syntax:**
```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2]; // [1, 2, 3, 4, 5, 6]
const combined2 = [...arr1, ...arr2, 7, 8]; // [1, 2, 3, 4, 5, 6, 7, 8]
```

**Differences:**
- Spread is more readable and flexible
- `concat()` can handle non-array values: `[1, 2].concat(3)` vs `[...[1, 2], 3]`

### 55. Explain the difference between `Array.reduce()` and `Array.reduceRight()`.

**Answer:**
**reduce() - Left to right:**
```javascript
const arr = [1, 2, 3, 4];
arr.reduce((acc, val) => acc + val, 0); // 10
// Steps: 0+1=1, 1+2=3, 3+3=6, 6+4=10
```

**reduceRight() - Right to left:**
```javascript
const arr = [1, 2, 3, 4];
arr.reduceRight((acc, val) => acc + val, 0); // 10
// Steps: 0+4=4, 4+3=7, 7+2=9, 9+1=10

// String reversal
const str = 'hello';
str.split('').reduceRight((acc, char) => acc + char, ''); // 'olleh'
```

### 56. Explain the difference between `Array.sort()` with and without compare function.

**Answer:**
**Without compare function (string sort):**
```javascript
const numbers = [10, 2, 5, 1, 9];
numbers.sort(); // [1, 10, 2, 5, 9] (incorrect - string comparison)

const strings = ['banana', 'apple', 'cherry'];
strings.sort(); // ['apple', 'banana', 'cherry'] (correct)
```

**With compare function:**
```javascript
const numbers = [10, 2, 5, 1, 9];
numbers.sort((a, b) => a - b); // [1, 2, 5, 9, 10] (ascending)
numbers.sort((a, b) => b - a); // [10, 9, 5, 2, 1] (descending)

// Objects
const users = [
    { name: 'John', age: 30 },
    { name: 'Jane', age: 25 }
];
users.sort((a, b) => a.age - b.age); // Sort by age
```

### 57. Explain the difference between `Array.forEach()` and `Array.map()`.

**Answer:**
**forEach() - Iterates, returns undefined:**
```javascript
const arr = [1, 2, 3];
const result = arr.forEach(n => n * 2); // undefined
console.log(arr); // [1, 2, 3] (unchanged)

// Side effects
arr.forEach(n => console.log(n)); // 1, 2, 3
```

**map() - Transforms, returns new array:**
```javascript
const arr = [1, 2, 3];
const doubled = arr.map(n => n * 2); // [2, 4, 6]
console.log(arr); // [1, 2, 3] (unchanged)
```

**When to use:**
- `forEach()`: Side effects, no return value needed
- `map()`: Transform array, need return value

### 58. Explain the difference between `Array.flat()` and `Array.flatMap()`.

**Answer:**
**flat() - Flattens array:**
```javascript
const arr = [1, [2, 3], [4, [5, 6]]];
arr.flat(); // [1, 2, 3, 4, [5, 6]]
arr.flat(2); // [1, 2, 3, 4, 5, 6]
arr.flat(Infinity); // [1, 2, 3, 4, 5, 6] (all levels)
```

**flatMap() - Map then flatten:**
```javascript
const arr = [1, 2, 3];
arr.flatMap(n => [n, n * 2]); // [1, 2, 2, 4, 3, 6]
// Equivalent to: arr.map(n => [n, n * 2]).flat()

// Only flattens one level
arr.flatMap(n => [[n * 2]]); // [[2], [4], [6]] (not flattened)
```

### 59. Explain the difference between `Array.findIndex()` and `Array.indexOf()`.

**Answer:**
**indexOf() - Simple value search:**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.indexOf(3); // 2
arr.indexOf(6); // -1
arr.indexOf(3, 3); // -1 (starts from index 3)
```

**findIndex() - Condition-based search:**
```javascript
const users = [
    { id: 1, name: 'John', active: true },
    { id: 2, name: 'Jane', active: false },
    { id: 3, name: 'Bob', active: true }
];

users.findIndex(u => u.active); // 0 (first active user)
users.findIndex(u => u.id === 2); // 1
users.findIndex(u => u.id === 5); // -1
```

### 60. Explain the difference between `Array.fill()` and `Array.from()` for array initialization.

**Answer:**
**fill() - Fills existing array:**
```javascript
const arr = new Array(5).fill(0); // [0, 0, 0, 0, 0]
const arr2 = new Array(5).fill(0, 1, 3); // [empty, 0, 0, empty, empty]
```

**Array.from() - Creates and fills:**
```javascript
Array.from({ length: 5 }, () => 0); // [0, 0, 0, 0, 0]
Array.from({ length: 5 }, (_, i) => i); // [0, 1, 2, 3, 4]
Array.from({ length: 5 }, (_, i) => i * 2); // [0, 2, 4, 6, 8]
```

**When to use:**
- `fill()`: Same value for all elements
- `Array.from()`: Different values based on index

### 61. What is the output of `3 + 2 + "7"` in JavaScript?

**Answer:**
```javascript
3 + 2 + "7"  // "57"
```

**Explanation:**
- `3 + 2` evaluates to `5` (number)
- `5 + "7"` performs string concatenation, resulting in `"57"`

**More Examples:**
```javascript
"3" + 2 + 7;     // "327" (left to right, string concatenation)
3 + 2 + 7;       // 12 (all numbers, addition)
"3" + (2 + 7);   // "39" (parentheses evaluated first)
```

### 62. Explain the difference between `null` and `undefined` in detail.

**Answer:**
**undefined:**
- Variable declared but not assigned
- Missing function parameters
- Missing object properties
- Function with no return statement

**null:**
- Explicitly assigned value
- Represents intentional absence of value
- Must be assigned

```javascript
let x;
console.log(x);        // undefined

let y = null;
console.log(y);        // null

// typeof
typeof undefined;      // "undefined"
typeof null;           // "object" (historical bug)

// Equality
null == undefined;     // true (loose equality)
null === undefined;    // false (strict equality)
```

### 63. Explain JavaScript's type coercion with examples.

**Answer:**
Type coercion converts one type to another automatically.

**String Coercion:**
```javascript
"5" + 3;        // "53" (number to string)
"5" - 3;        // 2 (string to number)
"5" * "2";      // 10 (both to numbers)
```

**Boolean Coercion:**
```javascript
if ("hello") { }    // true (non-empty string)
if (0) { }          // false (zero)
if ([]) { }         // true (array is truthy)
if ({}) { }         // true (object is truthy)
```

**Number Coercion:**
```javascript
+"5";            // 5
Number("5");     // 5
parseInt("5");   // 5
```

**Falsy Values:**
- `false`, `0`, `""`, `null`, `undefined`, `NaN`

### 64. Explain JavaScript's `this` binding in different scenarios.

**Answer:**
**Global Context:**
```javascript
console.log(this); // Window (browser) or global (Node)
```

**Function Call:**
```javascript
function regular() {
    console.log(this); // Window/global (non-strict) or undefined (strict)
}
```

**Method Call:**
```javascript
const obj = {
    name: "John",
    greet: function() {
        console.log(this.name); // "John"
    }
};
obj.greet();
```

**Arrow Function:**
```javascript
const obj = {
    name: "John",
    greet: () => {
        console.log(this.name); // undefined (lexical this)
    }
};
```

**Constructor:**
```javascript
function Person(name) {
    this.name = name; // this = new object
}
const person = new Person("John");
```

### 65. Explain JavaScript's `arguments` object.

**Answer:**
`arguments` is array-like object containing function arguments.

```javascript
function sum() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

sum(1, 2, 3); // 6
```

**Convert to Array:**
```javascript
function example() {
    const args = Array.from(arguments);
    // Or
    const args2 = [...arguments];
}
```

**Note:** Arrow functions don't have `arguments` object.

### 66. Explain JavaScript's `eval()` and why it's dangerous.

**Answer:**
`eval()` executes string as JavaScript code.

```javascript
eval("2 + 2"); // 4
eval("console.log('Hello')"); // Executes code
```

**Dangers:**
- Security risk (code injection)
- Performance issues (no optimization)
- Debugging difficulties

**Alternatives:**
```javascript
// Use Function constructor (safer)
const add = new Function('a', 'b', 'return a + b');
add(2, 3); // 5

// Use JSON.parse for data
const data = JSON.parse('{"name": "John"}');
```

### 67. Explain JavaScript's `with` statement and why it's deprecated.

**Answer:**
`with` adds object properties to scope chain.

```javascript
const obj = { a: 1, b: 2 };
with (obj) {
    console.log(a + b); // 3
}
```

**Problems:**
- Performance issues
- Ambiguity
- Deprecated in strict mode

**Alternative:**
```javascript
// Use destructuring
const { a, b } = obj;
console.log(a + b);
```

### 68. Explain JavaScript's `delete` operator.

**Answer:**
`delete` removes property from object.

```javascript
const obj = { a: 1, b: 2, c: 3 };
delete obj.b;
console.log(obj); // { a: 1, c: 3 }

// Array elements
const arr = [1, 2, 3];
delete arr[1];
console.log(arr); // [1, empty, 3] (length unchanged)
```

**Limitations:**
- Cannot delete variables
- Cannot delete function parameters
- Cannot delete non-configurable properties

### 69. Explain JavaScript's `void` operator.

**Answer:**
`void` evaluates expression and returns `undefined`.

```javascript
void 0;              // undefined
void (1 + 2);        // undefined
void console.log('Hello'); // undefined (but logs 'Hello')
```

**Use Cases:**
- Ensure expression returns undefined
- Prevent navigation in links: `<a href="javascript:void(0)">`
- IIFE: `void function() { }()`

### 70. Explain JavaScript's `in` operator.

**Answer:**
`in` checks if property exists in object.

```javascript
const obj = { a: 1, b: 2 };
'a' in obj;          // true
'c' in obj;          // false

// Arrays
const arr = [1, 2, 3];
0 in arr;            // true (index exists)
5 in arr;            // false (index doesn't exist)
'length' in arr;     // true (property exists)
```

**vs `hasOwnProperty()`:**
```javascript
const obj = Object.create({ inherited: true });
obj.own = true;

'inherited' in obj;           // true (checks prototype chain)
obj.hasOwnProperty('inherited'); // false (only own properties)
```

### 71. Explain JavaScript's `instanceof` operator.

**Answer:**
`instanceof` checks if object is instance of constructor.

```javascript
[] instanceof Array;          // true
[] instanceof Object;        // true (Array extends Object)
{} instanceof Object;        // true

function Person() {}
const person = new Person();
person instanceof Person;    // true
person instanceof Object;   // true
```

**Custom instanceof:**
```javascript
function myInstanceof(obj, constructor) {
    let proto = Object.getPrototypeOf(obj);
    while (proto) {
        if (proto === constructor.prototype) return true;
        proto = Object.getPrototypeOf(proto);
    }
    return false;
}
```

### 72. Explain JavaScript's `typeof` operator quirks.

**Answer:**
**Normal Cases:**
```javascript
typeof "hello";      // "string"
typeof 42;           // "number"
typeof true;         // "boolean"
typeof undefined;    // "undefined"
typeof Symbol();     // "symbol"
typeof function(){}; // "function"
```

**Quirks:**
```javascript
typeof null;         // "object" (historical bug)
typeof [];           // "object"
typeof {};           // "object"
typeof NaN;          // "number"
typeof Infinity;     // "number"
```

**Better Type Checking:**
```javascript
Object.prototype.toString.call(null);      // "[object Null]"
Object.prototype.toString.call([]);        // "[object Array]"
Object.prototype.toString.call({});       // "[object Object]"
```

### 73. Explain JavaScript's `new` operator.

**Answer:**
`new` creates instance of constructor function.

**What `new` does:**
1. Creates new object
2. Sets prototype to constructor's prototype
3. Binds `this` to new object
4. Returns object (unless constructor returns object)

```javascript
function Person(name) {
    this.name = name;
}

const person = new Person("John");
// Equivalent to:
// 1. const obj = {};
// 2. obj.__proto__ = Person.prototype;
// 3. Person.call(obj, "John");
// 4. return obj;
```

**Manual Implementation:**
```javascript
function myNew(constructor, ...args) {
    const obj = Object.create(constructor.prototype);
    const result = constructor.apply(obj, args);
    return result instanceof Object ? result : obj;
}
```

### 74. Explain JavaScript's `super` keyword.

**Answer:**
`super` calls parent class methods/constructor.

**In Constructor:**
```javascript
class Parent {
    constructor(name) {
        this.name = name;
    }
}

class Child extends Parent {
    constructor(name, age) {
        super(name); // Call parent constructor
        this.age = age;
    }
}
```

**In Methods:**
```javascript
class Parent {
    greet() {
        return "Hello from parent";
    }
}

class Child extends Parent {
    greet() {
        return super.greet() + " and child";
    }
}
```

**In Static Methods:**
```javascript
class Parent {
    static getType() {
        return "Parent";
    }
}

class Child extends Parent {
    static getType() {
        return super.getType() + " -> Child";
    }
}
```

### 75. Explain JavaScript's `yield` keyword and generator functions.

**Answer:**
`yield` pauses generator function execution.

**Basic Generator:**
```javascript
function* generator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = generator();
gen.next(); // { value: 1, done: false }
gen.next(); // { value: 2, done: false }
gen.next(); // { value: 3, done: false }
gen.next(); // { value: undefined, done: true }
```

**Yield with Value:**
```javascript
function* generator() {
    const x = yield "First";
    const y = yield x + " Second";
    return y + " Third";
}

const gen = generator();
gen.next();        // { value: "First", done: false }
gen.next("Hello"); // { value: "Hello Second", done: false }
gen.next("World"); // { value: "World Third", done: true }
```

**Use Cases:**
- Lazy evaluation
- Infinite sequences
- Async iteration

### 76. Explain JavaScript's `async` and `await` error handling.

**Answer:**
**Try-Catch:**
```javascript
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error; // Re-throw if needed
    }
}
```

**Promise Catch:**
```javascript
async function fetchData() {
    const response = await fetch('https://api.example.com/data')
        .catch(error => {
            console.error('Fetch error:', error);
            return null;
        });
    
    if (!response) return null;
    return response.json();
}
```

**Multiple Awaits:**
```javascript
async function fetchMultiple() {
    try {
        const [data1, data2] = await Promise.all([
            fetchData1(),
            fetchData2()
        ]);
        return { data1, data2 };
    } catch (error) {
        // Handles any error from either promise
        console.error('Error:', error);
    }
}
```

### 77. Explain JavaScript's `Promise.all()` vs `Promise.allSettled()`.

**Answer:**
**Promise.all():**
```javascript
Promise.all([promise1, promise2, promise3])
    .then(results => {
        // All resolved
    })
    .catch(error => {
        // First rejection stops all
    });
```

**Promise.allSettled():**
```javascript
Promise.allSettled([promise1, promise2, promise3])
    .then(results => {
        results.forEach(result => {
            if (result.status === 'fulfilled') {
                console.log('Success:', result.value);
            } else {
                console.log('Failed:', result.reason);
            }
        });
    });
```

**Differences:**
- `all()`: Fails fast (first rejection)
- `allSettled()`: Waits for all (never rejects)

### 78. Explain JavaScript's `JSON.parse()` and `JSON.stringify()`.

**Answer:**
**JSON.stringify():**
```javascript
const obj = { name: "John", age: 30 };
JSON.stringify(obj); // '{"name":"John","age":30}'

// With replacer
JSON.stringify(obj, ['name']); // '{"name":"John"}'

// With space (pretty print)
JSON.stringify(obj, null, 2);
```

**JSON.parse():**
```javascript
const json = '{"name":"John","age":30}';
JSON.parse(json); // { name: "John", age: 30 }

// With reviver
JSON.parse(json, (key, value) => {
    if (key === 'age') return value * 2;
    return value;
});
```

**Limitations:**
- Functions not stringified
- `undefined` not stringified
- `Date` becomes string
- Circular references cause error

### 79. Explain JavaScript's `Object.keys()`, `Object.values()`, `Object.entries()`.

**Answer:**
**Object.keys():**
```javascript
const obj = { a: 1, b: 2, c: 3 };
Object.keys(obj); // ['a', 'b', 'c']
```

**Object.values():**
```javascript
Object.values(obj); // [1, 2, 3]
```

**Object.entries():**
```javascript
Object.entries(obj); // [['a', 1], ['b', 2], ['c', 3]]

// Convert to Map
const map = new Map(Object.entries(obj));

// Iterate
for (const [key, value] of Object.entries(obj)) {
    console.log(key, value);
}
```

**Object.fromEntries():**
```javascript
const entries = [['a', 1], ['b', 2]];
Object.fromEntries(entries); // { a: 1, b: 2 }
```

### 80. Explain JavaScript's `Array.from()` vs spread operator.

**Answer:**
**Array.from():**
```javascript
Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']
Array.from({ length: 5 }, (_, i) => i); // [0, 1, 2, 3, 4]

// From array-like
const arrayLike = { 0: 'a', 1: 'b', length: 2 };
Array.from(arrayLike); // ['a', 'b']
```

**Spread Operator:**
```javascript
[...'hello']; // ['h', 'e', 'l', 'l', 'o']
[...arrayLike]; // Error (not iterable)

// Works with iterables
const set = new Set([1, 2, 3]);
[...set]; // [1, 2, 3]
```

**Differences:**
- `Array.from()`: Works with array-like objects
- Spread: Only works with iterables

### 81. Explain JavaScript's `Array.isArray()` and type checking.

**Answer:**
**Array.isArray():**
```javascript
Array.isArray([1, 2, 3]);     // true
Array.isArray({});            // false
Array.isArray('string');      // false
Array.isArray(null);          // false
```

**Type Checking:**
```javascript
// typeof limitations
typeof [];           // "object" (not helpful)
typeof null;         // "object" (bug)

// Better methods
Array.isArray([]);   // true
Object.prototype.toString.call([]); // "[object Array]"
```

### 82. Explain JavaScript's `Array.splice()` vs `Array.slice()`.

**Answer:**
**splice() - Mutates array:**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.splice(1, 2, 'a', 'b'); // [1, 'a', 'b', 4, 5]
// Removes 2 elements from index 1, inserts 'a', 'b'
```

**slice() - Returns new array:**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.slice(1, 3); // [2, 3] (original unchanged)
arr.slice(1);    // [2, 3, 4, 5]
arr.slice(-2);   // [4, 5] (last 2)
```

**Differences:**
- `splice()`: Mutates, can insert/delete
- `slice()`: Immutable, only extracts

### 83. Explain JavaScript's `Array.some()` and `Array.every()`.

**Answer:**
**some() - At least one:**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.some(n => n > 3);  // true (4, 5 exist)
arr.some(n => n > 10); // false
```

**every() - All:**
```javascript
const arr = [1, 2, 3, 4, 5];
arr.every(n => n > 0);  // true (all positive)
arr.every(n => n > 3);  // false (1, 2, 3 not > 3)
```

### 84. Explain JavaScript's `String.split()` and `Array.join()`.

**Answer:**
**split():**
```javascript
'hello world'.split(' ');     // ['hello', 'world']
'1,2,3'.split(',');           // ['1', '2', '3']
'abc'.split('');              // ['a', 'b', 'c']
'hello'.split('', 3);         // ['h', 'e', 'l'] (limit)
```

**join():**
```javascript
['a', 'b', 'c'].join();       // 'a,b,c'
['a', 'b', 'c'].join('');     // 'abc'
['a', 'b', 'c'].join('-');    // 'a-b-c'
```

### 85. Explain JavaScript's `String.substring()` vs `String.substr()` vs `String.slice()`.

**Answer:**
**substring() - Start to end:**
```javascript
'hello'.substring(1, 3);  // 'el' (start, end)
'hello'.substring(1);     // 'ello' (start to end)
'hello'.substring(3, 1);  // 'el' (swaps if start > end)
```

**substr() - Start and length (deprecated):**
```javascript
'hello'.substr(1, 3);  // 'ell' (start, length)
'hello'.substr(1);     // 'ello' (start to end)
```

**slice() - Start to end:**
```javascript
'hello'.slice(1, 3);   // 'el' (start, end)
'hello'.slice(1);       // 'ello' (start to end)
'hello'.slice(-3);      // 'llo' (negative index)
'hello'.slice(3, 1);    // '' (doesn't swap)
```

**Best Practice:** Use `slice()` (most flexible, works with arrays too).

### 86. Explain JavaScript's `String.replace()` and `String.replaceAll()`.

**Answer:**
**replace() - First match:**
```javascript
'hello world'.replace('l', 'L');  // 'heLlo world'
'hello world'.replace(/l/g, 'L'); // 'heLLo worLd' (regex)
```

**replaceAll() - All matches:**
```javascript
'hello world'.replaceAll('l', 'L'); // 'heLLo worLd'
'hello world'.replaceAll(/l/g, 'L'); // 'heLLo worLd'
```

### 87. Explain JavaScript's `String.includes()`, `String.startsWith()`, `String.endsWith()`.

**Answer:**
**includes():**
```javascript
'hello'.includes('ell');  // true
'hello'.includes('xyz');  // false
'hello'.includes('ell', 1); // true (start from index 1)
```

**startsWith():**
```javascript
'hello'.startsWith('he');  // true
'hello'.startsWith('lo');   // false
'hello'.startsWith('ll', 2); // true (start from index 2)
```

**endsWith():**
```javascript
'hello'.endsWith('lo');     // true
'hello'.endsWith('he');     // false
'hello'.endsWith('he', 2);  // true (check first 2 chars)
```

### 88. Explain JavaScript's `String.trim()`, `String.trimStart()`, `String.trimEnd()`.

**Answer:**
**trim():**
```javascript
'  hello  '.trim();        // 'hello' (both sides)
```

**trimStart() / trimLeft():**
```javascript
'  hello  '.trimStart();  // 'hello  ' (left only)
```

**trimEnd() / trimRight():**
```javascript
'  hello  '.trimEnd();     // '  hello' (right only)
```

### 89. Explain JavaScript's `String.padStart()` and `String.padEnd()`.

**Answer:**
**padStart():**
```javascript
'5'.padStart(3, '0');      // '005' (pad to length 3)
'5'.padStart(3);           // '  5' (default: space)
```

**padEnd():**
```javascript
'5'.padEnd(3, '0');        // '500'
'5'.padEnd(3);             // '5  '
```

**Use Cases:**
- Formatting numbers
- Aligning text
- Padding IDs

### 90. Explain JavaScript's `Number.parseInt()` and `Number.parseFloat()`.

**Answer:**
**parseInt():**
```javascript
parseInt('123');        // 123
parseInt('123.45');     // 123 (stops at decimal)
parseInt('123abc');     // 123 (stops at non-digit)
parseInt('abc123');     // NaN
parseInt('1010', 2);    // 10 (binary)
parseInt('FF', 16);     // 255 (hexadecimal)
```

**parseFloat():**
```javascript
parseFloat('123.45');   // 123.45
parseFloat('123.45abc'); // 123.45 (stops at non-digit)
parseFloat('abc123');    // NaN
```

**vs Number():**
```javascript
Number('123');          // 123
Number('123.45');       // 123.45
Number('123abc');       // NaN (strict)
```

---

This covers JavaScript interview questions from beginner to advanced level with detailed explanations and code examples.

