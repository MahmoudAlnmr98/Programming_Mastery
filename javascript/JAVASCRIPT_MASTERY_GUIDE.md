# Complete JavaScript Mastery Guide

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Data Types & Variables](#data-types--variables)
3. [Operators & Expressions](#operators--expressions)
4. [Control Flow](#control-flow)
5. [Functions](#functions)
6. [Objects & Arrays](#objects--arrays)
7. [Advanced Functions](#advanced-functions)
8. [Classes & OOP](#classes--oop)
9. [Asynchronous JavaScript](#asynchronous-javascript)
10. [ES6+ Features](#es6-features)
11. [Functional Programming](#functional-programming)
12. [Error Handling](#error-handling)
13. [Modules & Imports](#modules--imports)
14. [DOM Manipulation](#dom-manipulation)
15. [Event Handling](#event-handling)
16. [APIs & Fetch](#apis--fetch)
17. [Storage & Cookies](#storage--cookies)
18. [Performance Optimization](#performance-optimization)
19. [Security Best Practices](#security-best-practices)
20. [Testing](#testing)
21. [Design Patterns](#design-patterns)
22. [Advanced Topics](#advanced-topics)

---

## Fundamentals

### What is JavaScript?
JavaScript is a high-level, interpreted programming language that conforms to the ECMAScript specification. It's:
- **Dynamic**: Types are determined at runtime
- **Weakly Typed**: Implicit type coercion
- **Multi-paradigm**: Supports OOP, functional, and procedural programming
- **Single-threaded**: Uses event loop for concurrency
- **Prototype-based**: Objects inherit from other objects

### Execution Context
JavaScript code runs in an execution context:
- **Global Context**: Default context when code first loads
- **Function Context**: Created when a function is invoked
- **Eval Context**: Code executed inside eval()

Each context has:
- Variable object (VO)
- Scope chain
- `this` binding

---

## Data Types & Variables

### Primitive Types
```javascript
// 7 Primitive Types
let str = "Hello";           // String
let num = 42;                // Number (includes integers, floats, NaN, Infinity)
let bool = true;             // Boolean
let undef = undefined;       // Undefined
let nul = null;              // Null
let sym = Symbol('id');      // Symbol (ES6)
let big = 9007199254740991n; // BigInt (ES2020)

// Type checking
typeof str;        // "string"
typeof num;        // "number"
typeof bool;       // "boolean"
typeof undef;      // "undefined"
typeof nul;        // "object" (historical bug)
typeof sym;        // "symbol"
typeof big;        // "bigint"
```

### Reference Types
```javascript
// Objects (everything else)
let obj = {};                 // Object
let arr = [];                 // Array
let func = function() {};     // Function
let date = new Date();        // Date
let regex = /pattern/;        // RegExp
```

### Variable Declarations

#### var (Function-scoped, hoisted)
```javascript
function example() {
    console.log(x); // undefined (hoisted but not initialized)
    var x = 5;
    if (true) {
        var y = 10; // Function-scoped, not block-scoped
    }
    console.log(y); // 10 (accessible outside block)
}
```

#### let (Block-scoped, temporal dead zone)
```javascript
function example() {
    // console.log(x); // ReferenceError (temporal dead zone)
    let x = 5;
    if (true) {
        let y = 10; // Block-scoped
    }
    // console.log(y); // ReferenceError
}
```

#### const (Block-scoped, immutable binding)
```javascript
const PI = 3.14159;
// PI = 3.14; // TypeError

const obj = { name: "John" };
obj.name = "Jane"; // OK - object is mutable
// obj = {}; // TypeError - cannot reassign binding

const arr = [1, 2, 3];
arr.push(4); // OK
// arr = []; // TypeError
```

### Type Coercion
```javascript
// Implicit Coercion
"5" + 3;        // "53" (number to string)
"5" - 3;        // 2 (string to number)
"5" * "2";      // 10
true + 1;       // 2
false + 1;      // 1
null + 1;       // 1
undefined + 1;  // NaN

// Explicit Coercion
String(123);           // "123"
Number("123");         // 123
Boolean(1);            // true
parseInt("123px");     // 123
parseFloat("12.5px");  // 12.5
```

### Truthy & Falsy Values
```javascript
// Falsy values (6 total)
false
0
-0
0n (BigInt zero)
"" (empty string)
null
undefined
NaN

// Everything else is truthy
if ("0") { }        // truthy
if ([]) { }         // truthy
if ({}) { }         // truthy
```

---

## Operators & Expressions

### Arithmetic Operators
```javascript
+  // Addition or concatenation
-  // Subtraction
*  // Multiplication
/  // Division
%  // Modulo
** // Exponentiation (ES2016)
++ // Increment
-- // Decrement
```

### Comparison Operators
```javascript
==  // Loose equality (with coercion)
=== // Strict equality (no coercion)
!=  // Loose inequality
!== // Strict inequality
<   // Less than
>   // Greater than
<=  // Less than or equal
>=  // Greater than or equal

// Examples
"5" == 5;   // true (coercion)
"5" === 5;  // false (no coercion)
null == undefined;  // true
null === undefined; // false
```

### Logical Operators
```javascript
&&  // Logical AND (returns first falsy or last truthy)
||  // Logical OR (returns first truthy or last falsy)
!   // Logical NOT

// Short-circuit evaluation
const value = obj && obj.property && obj.property.nested;
const name = user.name || "Anonymous";
```

### Assignment Operators
```javascript
=   // Assignment
+=  // Addition assignment
-=  // Subtraction assignment
*=  // Multiplication assignment
/=  // Division assignment
%=  // Modulo assignment
**= // Exponentiation assignment
```

### Bitwise Operators
```javascript
&   // AND
|   // OR
^   // XOR
~   // NOT
<<  // Left shift
>>  // Right shift
>>> // Unsigned right shift
```

### Other Operators
```javascript
// Ternary operator
condition ? valueIfTrue : valueIfFalse;

// Nullish coalescing (ES2020)
value ?? defaultValue; // Returns defaultValue if value is null or undefined

// Optional chaining (ES2020)
obj?.property?.nested?.method?.();

// Spread operator
[...array]
{...object}

// Destructuring
const {a, b} = obj;
const [x, y] = array;
```

---

## Control Flow

### Conditional Statements
```javascript
// if/else
if (condition) {
    // code
} else if (anotherCondition) {
    // code
} else {
    // code
}

// Ternary
const result = condition ? value1 : value2;

// Switch
switch (value) {
    case 1:
        // code
        break;
    case 2:
    case 3:
        // code (fall-through)
        break;
    default:
        // code
}
```

### Loops
```javascript
// for loop
for (let i = 0; i < 10; i++) {
    console.log(i);
}

// for...in (iterates over object keys)
for (let key in object) {
    console.log(key, object[key]);
}

// for...of (iterates over iterable values)
for (let value of array) {
    console.log(value);
}

// while loop
while (condition) {
    // code
}

// do...while loop
do {
    // code
} while (condition);

// Array methods (preferred for arrays)
array.forEach((item, index) => { });
array.map(item => item * 2);
array.filter(item => item > 5);
array.reduce((acc, item) => acc + item, 0);
```

### Control Flow Statements
```javascript
break;      // Exit loop
continue;   // Skip to next iteration
return;     // Exit function
throw;      // Throw error
```

---

## Functions

### Function Declarations
```javascript
function greet(name) {
    return `Hello, ${name}!`;
}

// Hoisted - can be called before declaration
greet("John"); // Works
```

### Function Expressions
```javascript
const greet = function(name) {
    return `Hello, ${name}!`;
};

// Not hoisted - must be called after declaration
```

### Arrow Functions (ES6)
```javascript
// Single parameter, single expression
const greet = name => `Hello, ${name}!`;

// Multiple parameters
const add = (a, b) => a + b;

// No parameters
const sayHi = () => console.log("Hi");

// Multiple statements
const process = (data) => {
    const result = data.map(item => item * 2);
    return result.filter(item => item > 10);
};

// Important: Arrow functions don't have their own 'this'
const obj = {
    name: "John",
    regular: function() {
        console.log(this.name); // "John"
    },
    arrow: () => {
        console.log(this.name); // undefined (this refers to outer scope)
    }
};
```

### Function Parameters
```javascript
// Default parameters
function greet(name = "Guest") {
    return `Hello, ${name}!`;
}

// Rest parameters
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}

// Destructuring parameters
function process({name, age, city = "Unknown"}) {
    console.log(`${name}, ${age}, ${city}`);
}
```

### IIFE (Immediately Invoked Function Expression)
```javascript
(function() {
    // Private scope
    const private = "secret";
})();

// With arrow function
(() => {
    // code
})();
```

---

## Objects & Arrays

### Objects
```javascript
// Object literal
const person = {
    name: "John",
    age: 30,
    greet: function() {
        return `Hello, I'm ${this.name}`;
    },
    // Shorthand (ES6)
    greet() {
        return `Hello, I'm ${this.name}`;
    }
};

// Accessing properties
person.name;           // Dot notation
person["name"];        // Bracket notation
person[propName];      // Dynamic property access

// Adding/Modifying
person.city = "NYC";
person["city"] = "NYC";

// Deleting
delete person.age;

// Object methods
Object.keys(person);      // ["name", "age", "greet"]
Object.values(person);    // ["John", 30, function...]
Object.entries(person);   // [["name", "John"], ...]
Object.assign({}, person); // Shallow copy
Object.freeze(person);     // Immutable
Object.seal(person);       // Can't add/remove, can modify
```

### Arrays
```javascript
// Array creation
const arr = [1, 2, 3];
const arr2 = new Array(1, 2, 3);
const arr3 = Array.from("hello"); // ["h", "e", "l", "l", "o"]
const arr4 = Array.of(1, 2, 3);

// Array methods
arr.length;                    // Length
arr.push(4);                   // Add to end
arr.pop();                     // Remove from end
arr.unshift(0);                // Add to beginning
arr.shift();                   // Remove from beginning
arr.indexOf(2);                // Find index
arr.includes(2);               // Check existence
arr.slice(1, 3);               // Extract portion (non-mutating)
arr.splice(1, 1, "new");       // Remove/insert (mutating)
arr.concat([4, 5]);            // Concatenate (non-mutating)
arr.join(", ");                // Join to string
arr.reverse();                 // Reverse (mutating)
arr.sort();                    // Sort (mutating)

// Iteration methods (non-mutating)
arr.forEach((item, index) => { });
arr.map(item => item * 2);     // Transform
arr.filter(item => item > 2);  // Filter
arr.reduce((acc, item) => acc + item, 0); // Accumulate
arr.find(item => item > 2);    // Find first match
arr.findIndex(item => item > 2); // Find index
arr.some(item => item > 2);    // Any match
arr.every(item => item > 0);   // All match
```

### Array Destructuring
```javascript
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

const [a, , c] = [1, 2, 3]; // Skip element
// a = 1, c = 3

const [x = 10, y = 20] = [1]; // Default values
// x = 1, y = 20
```

### Object Destructuring
```javascript
const {name, age} = {name: "John", age: 30};
// name = "John", age = 30

const {name: personName, age: personAge} = {name: "John", age: 30};
// personName = "John", personAge = 30

const {name, ...rest} = {name: "John", age: 30, city: "NYC"};
// name = "John", rest = {age: 30, city: "NYC"}

const {name = "Guest"} = {}; // Default value
// name = "Guest"
```

### Spread Operator
```javascript
// Arrays
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2]; // [1, 2, 3, 4, 5, 6]
const copy = [...arr1]; // Shallow copy

// Objects
const obj1 = {a: 1, b: 2};
const obj2 = {c: 3, d: 4};
const merged = {...obj1, ...obj2}; // {a: 1, b: 2, c: 3, d: 4}
const copy = {...obj1}; // Shallow copy
```

---

## Advanced Functions

### Higher-Order Functions
Functions that operate on other functions:
```javascript
// Function that returns a function
function multiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

const double = multiplier(2);
double(5); // 10

// Function that takes a function as argument
function applyOperation(a, b, operation) {
    return operation(a, b);
}

applyOperation(5, 3, (x, y) => x + y); // 8
```

### Closures
```javascript
function outer() {
    let count = 0;
    
    return function inner() {
        count++;
        return count;
    };
}

const counter = outer();
counter(); // 1
counter(); // 2
counter(); // 3

// Each call to outer() creates a new closure
const counter2 = outer();
counter2(); // 1 (independent closure)
```

### Currying
```javascript
// Traditional function
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

// ES6 arrow function currying
const curriedAdd = a => b => c => a + b + c;

curriedAdd(1)(2)(3); // 6

// Partial application
const add5 = curriedAdd(5);
const add5And10 = add5(10);
add5And10(15); // 30
```

### Function Composition
```javascript
const compose = (...fns) => (value) => 
    fns.reduceRight((acc, fn) => fn(acc), value);

const pipe = (...fns) => (value) => 
    fns.reduce((acc, fn) => fn(acc), value);

const add1 = x => x + 1;
const multiply2 = x => x * 2;
const square = x => x * x;

const composed = compose(square, multiply2, add1);
composed(5); // ((5 + 1) * 2)² = 144

const piped = pipe(add1, multiply2, square);
piped(5); // ((5 + 1) * 2)² = 144
```

### Memoization
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

const expensiveFunction = (n) => {
    console.log("Computing...");
    return n * 2;
};

const memoized = memoize(expensiveFunction);
memoized(5); // Computing... 10
memoized(5); // 10 (from cache)
```

### Generators
```javascript
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}

const gen = numberGenerator();
gen.next(); // {value: 1, done: false}
gen.next(); // {value: 2, done: false}
gen.next(); // {value: 3, done: false}
gen.next(); // {value: undefined, done: true}

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

---

## Classes & OOP

### Prototypes
```javascript
// Every object has a prototype
function Person(name) {
    this.name = name;
}

Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

const john = new Person("John");
john.greet(); // "Hello, I'm John"

// Prototype chain
john.__proto__ === Person.prototype; // true
Person.prototype.__proto__ === Object.prototype; // true
Object.prototype.__proto__ === null; // true
```

### Classes (ES6)
```javascript
class Person {
    // Constructor
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    // Instance method
    greet() {
        return `Hello, I'm ${this.name}`;
    }
    
    // Static method
    static compareAge(person1, person2) {
        return person1.age - person2.age;
    }
    
    // Getter
    get info() {
        return `${this.name} is ${this.age} years old`;
    }
    
    // Setter
    set age(newAge) {
        if (newAge > 0) {
            this._age = newAge;
        }
    }
}

// Inheritance
class Student extends Person {
    constructor(name, age, school) {
        super(name, age); // Call parent constructor
        this.school = school;
    }
    
    // Override method
    greet() {
        return `${super.greet()} and I study at ${this.school}`;
    }
}

// Private fields (ES2022)
class BankAccount {
    #balance = 0; // Private field
    
    deposit(amount) {
        this.#balance += amount;
    }
    
    getBalance() {
        return this.#balance;
    }
}
```

### this Binding
```javascript
// Default binding
function regular() {
    console.log(this); // Window (browser) or global (Node)
}

// Implicit binding
const obj = {
    name: "John",
    greet: function() {
        console.log(this.name); // "John"
    }
};

// Explicit binding
function greet() {
    console.log(this.name);
}
const person = {name: "John"};
greet.call(person);    // "John"
greet.apply(person);   // "John"
const bound = greet.bind(person);
bound(); // "John"

// New binding
function Person(name) {
    this.name = name;
}
const john = new Person("John"); // this = john

// Arrow functions (lexical this)
const obj = {
    name: "John",
    regular: function() {
        setTimeout(function() {
            console.log(this.name); // undefined (this = window)
        }, 100);
    },
    arrow: function() {
        setTimeout(() => {
            console.log(this.name); // "John" (this = obj)
        }, 100);
    }
};
```

---

## Asynchronous JavaScript

### Callbacks
```javascript
function fetchData(callback) {
    setTimeout(() => {
        callback("Data received");
    }, 1000);
}

fetchData((data) => {
    console.log(data);
});

// Callback hell
fetchData1((data1) => {
    fetchData2(data1, (data2) => {
        fetchData3(data2, (data3) => {
            // Nested callbacks
        });
    });
});
```

### Promises
```javascript
// Creating promises
const promise = new Promise((resolve, reject) => {
    const success = true;
    if (success) {
        resolve("Success!");
    } else {
        reject("Error!");
    }
});

// Consuming promises
promise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));

// Promise methods
Promise.all([promise1, promise2, promise3])
    .then(results => {
        // All resolved
    })
    .catch(error => {
        // First rejection
    });

Promise.allSettled([promise1, promise2])
    .then(results => {
        // All settled (resolved or rejected)
    });

Promise.race([promise1, promise2])
    .then(result => {
        // First to settle
    });

Promise.any([promise1, promise2])
    .then(result => {
        // First to resolve
    });
```

### async/await
```javascript
// Async function always returns a promise
async function fetchData() {
    return "Data";
}

// Await pauses execution until promise settles
async function processData() {
    try {
        const data1 = await fetchData1();
        const data2 = await fetchData2(data1);
        const data3 = await fetchData3(data2);
        return data3;
    } catch (error) {
        console.error(error);
    }
}

// Parallel execution
async function fetchAll() {
    const [data1, data2, data3] = await Promise.all([
        fetchData1(),
        fetchData2(),
        fetchData3()
    ]);
    return {data1, data2, data3};
}

// Error handling
async function handleErrors() {
    try {
        const result = await riskyOperation();
        return result;
    } catch (error) {
        // Handle error
        throw error; // Re-throw if needed
    }
}
```

### Event Loop
```javascript
// JavaScript is single-threaded but uses event loop for concurrency

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

---

## ES6+ Features

### Template Literals
```javascript
const name = "John";
const age = 30;

// Multi-line strings
const text = `Hello,
World!`;

// Interpolation
const message = `Hello, ${name}! You are ${age} years old.`;

// Tagged templates
function tag(strings, ...values) {
    return strings.reduce((result, str, i) => {
        return result + str + (values[i] || "");
    }, "");
}
```

### Destructuring
```javascript
// Array destructuring
const [a, b, c] = [1, 2, 3];
const [first, ...rest] = [1, 2, 3, 4];

// Object destructuring
const {name, age} = {name: "John", age: 30};
const {name: personName} = {name: "John"};

// Nested destructuring
const {user: {name, settings: {theme}}} = {
    user: {name: "John", settings: {theme: "dark"}}
};
```

### Default Parameters
```javascript
function greet(name = "Guest", greeting = "Hello") {
    return `${greeting}, ${name}!`;
}
```

### Rest & Spread
```javascript
// Rest (collecting)
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}

// Spread (expanding)
const arr = [1, 2, 3];
const newArr = [...arr, 4, 5];
```

### Symbols
```javascript
const sym1 = Symbol("id");
const sym2 = Symbol("id");
sym1 === sym2; // false (unique)

// Global symbols
const globalSym = Symbol.for("id");
const sameSym = Symbol.for("id");
globalSym === sameSym; // true
```

### Iterators & Iterables
```javascript
// Iterable protocol
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

### Map & Set
```javascript
// Map (key-value pairs, any type as key)
const map = new Map();
map.set("name", "John");
map.set(1, "one");
map.set({}, "object");

map.get("name"); // "John"
map.has("name"); // true
map.delete("name");
map.size; // 2

// Set (unique values)
const set = new Set([1, 2, 3, 3, 4]);
set.add(5);
set.has(3); // true
set.delete(3);
set.size; // 4

// WeakMap & WeakSet (weak references)
const weakMap = new WeakMap();
const weakSet = new WeakSet();
```

### Optional Chaining & Nullish Coalescing
```javascript
// Optional chaining (ES2020)
const user = {
    profile: {
        name: "John"
    }
};

user?.profile?.name; // "John"
user?.profile?.age; // undefined (no error)
user?.address?.city; // undefined

// Nullish coalescing (ES2020)
const value = null ?? "default"; // "default"
const value2 = undefined ?? "default"; // "default"
const value3 = 0 ?? "default"; // 0 (not null/undefined)
const value4 = "" ?? "default"; // "" (not null/undefined)
```

### BigInt
```javascript
const big = 9007199254740991n;
const big2 = BigInt("9007199254740991");

big + 1n; // 9007199254740992n
// big + 1; // TypeError (can't mix with Number)
```

---

## Functional Programming

### Pure Functions
```javascript
// Pure function (no side effects, same input = same output)
function add(a, b) {
    return a + b;
}

// Impure function
let counter = 0;
function increment() {
    counter++; // Side effect
    return counter;
}
```

### Immutability
```javascript
// Immutable operations
const arr = [1, 2, 3];
const newArr = [...arr, 4]; // Don't mutate arr

const obj = {a: 1, b: 2};
const newObj = {...obj, c: 3}; // Don't mutate obj

// Deep cloning
const deepClone = JSON.parse(JSON.stringify(obj));
// Or use structuredClone (modern browsers)
const clone = structuredClone(obj);
```

### Map, Filter, Reduce
```javascript
// Map (transform)
const doubled = [1, 2, 3].map(x => x * 2); // [2, 4, 6]

// Filter (select)
const evens = [1, 2, 3, 4].filter(x => x % 2 === 0); // [2, 4]

// Reduce (accumulate)
const sum = [1, 2, 3].reduce((acc, x) => acc + x, 0); // 6
const grouped = [{type: "a", val: 1}, {type: "b", val: 2}]
    .reduce((acc, item) => {
        acc[item.type] = (acc[item.type] || []).concat(item.val);
        return acc;
    }, {}); // {a: [1], b: [2]}
```

### Recursion
```javascript
// Factorial
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Tail recursion (optimized)
function factorialTail(n, acc = 1) {
    if (n <= 1) return acc;
    return factorialTail(n - 1, n * acc);
}

// Fibonacci
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Memoized fibonacci
const memoFib = (() => {
    const cache = {};
    return function fib(n) {
        if (n in cache) return cache[n];
        if (n <= 1) return n;
        cache[n] = fib(n - 1) + fib(n - 2);
        return cache[n];
    };
})();
```

---

## Error Handling

### try/catch/finally
```javascript
try {
    // Risky code
    throw new Error("Something went wrong");
} catch (error) {
    // Handle error
    console.error(error.message);
} finally {
    // Always executes
    console.log("Cleanup");
}

// Custom errors
class CustomError extends Error {
    constructor(message, code) {
        super(message);
        this.name = "CustomError";
        this.code = code;
    }
}

throw new CustomError("Custom error", 500);
```

### Error Types
```javascript
// Built-in error types
new Error("Generic error");
new SyntaxError("Syntax error");
new ReferenceError("Reference error");
new TypeError("Type error");
new RangeError("Range error");
new URIError("URI error");
```

### Promise Error Handling
```javascript
// Promise chains
promise
    .then(result => process(result))
    .catch(error => handleError(error))
    .finally(() => cleanup());

// async/await
async function handle() {
    try {
        const result = await promise;
        return process(result);
    } catch (error) {
        handleError(error);
    } finally {
        cleanup();
    }
}
```

---

## Modules & Imports

### ES6 Modules
```javascript
// math.js (export)
export const PI = 3.14159;
export function add(a, b) {
    return a + b;
}
export default function multiply(a, b) {
    return a * b;
}

// app.js (import)
import multiply, {PI, add} from "./math.js";
import * as math from "./math.js";
import {add as sum} from "./math.js";
```

### CommonJS (Node.js)
```javascript
// math.js
module.exports = {
    PI: 3.14159,
    add: (a, b) => a + b
};

// app.js
const math = require("./math");
const {add, PI} = require("./math");
```

---

## DOM Manipulation

### Selecting Elements
```javascript
// Single element
document.getElementById("id");
document.querySelector(".class");
document.querySelector("#id");

// Multiple elements
document.getElementsByClassName("class");
document.getElementsByTagName("div");
document.querySelectorAll(".class");
```

### Modifying Elements
```javascript
const element = document.querySelector("#myDiv");

// Content
element.textContent = "New text";
element.innerHTML = "<strong>HTML</strong>";
element.innerText = "Text only";

// Attributes
element.setAttribute("id", "newId");
element.getAttribute("id");
element.removeAttribute("id");
element.id = "newId"; // Direct property access

// Classes
element.classList.add("new-class");
element.classList.remove("old-class");
element.classList.toggle("active");
element.classList.contains("active");

// Styles
element.style.color = "red";
element.style.backgroundColor = "blue";
element.style.cssText = "color: red; background: blue;";
```

### Creating Elements
```javascript
// Create
const div = document.createElement("div");
div.textContent = "Hello";
div.className = "container";

// Append
document.body.appendChild(div);
element.insertBefore(newElement, referenceElement);
element.replaceChild(newElement, oldElement);

// Remove
element.removeChild(child);
child.remove();
```

### Traversing DOM
```javascript
// Parent
element.parentElement;
element.parentNode;

// Children
element.children; // HTMLCollection
element.childNodes; // NodeList
element.firstElementChild;
element.lastElementChild;

// Siblings
element.nextElementSibling;
element.previousElementSibling;
```

---

## Event Handling

### Event Listeners
```javascript
// addEventListener (preferred)
element.addEventListener("click", function(event) {
    console.log("Clicked");
});

// Arrow function
element.addEventListener("click", (event) => {
    console.log("Clicked");
});

// Remove listener
const handler = function(event) {
    console.log("Clicked");
};
element.addEventListener("click", handler);
element.removeEventListener("click", handler);

// Event delegation
document.addEventListener("click", (event) => {
    if (event.target.matches(".button")) {
        // Handle button click
    }
});
```

### Event Object
```javascript
element.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent default behavior
    event.stopPropagation(); // Stop bubbling
    event.stopImmediatePropagation(); // Stop all handlers
    
    event.target; // Element that triggered event
    event.currentTarget; // Element with listener
    event.type; // Event type
    event.timeStamp; // When event occurred
});
```

### Common Events
```javascript
// Mouse events
"click"
"dblclick"
"mousedown"
"mouseup"
"mousemove"
"mouseenter"
"mouseleave"
"mouseover"
"mouseout"

// Keyboard events
"keydown"
"keyup"
"keypress"

// Form events
"submit"
"change"
"input"
"focus"
"blur"

// Window events
"load"
"DOMContentLoaded"
"resize"
"scroll"
"beforeunload"
```

### Custom Events
```javascript
// Create and dispatch
const event = new CustomEvent("myEvent", {
    detail: {data: "value"},
    bubbles: true,
    cancelable: true
});

element.dispatchEvent(event);

// Listen
element.addEventListener("myEvent", (event) => {
    console.log(event.detail.data);
});
```

---

## APIs & Fetch

### Fetch API
```javascript
// Basic GET request
fetch("https://api.example.com/data")
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error(error));

// With async/await
async function fetchData() {
    try {
        const response = await fetch("https://api.example.com/data");
        if (!response.ok) throw new Error("Network error");
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

// POST request
fetch("https://api.example.com/data", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({name: "John", age: 30})
})
    .then(response => response.json())
    .then(data => console.log(data));

// With options
fetch(url, {
    method: "GET",
    headers: {
        "Authorization": "Bearer token",
        "Content-Type": "application/json"
    },
    mode: "cors",
    cache: "no-cache",
    credentials: "include"
});
```

### XMLHttpRequest (Legacy)
```javascript
const xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/data");
xhr.onload = function() {
    if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        console.log(data);
    }
};
xhr.send();
```

### Axios (Library)
```javascript
// GET
axios.get("https://api.example.com/data")
    .then(response => console.log(response.data))
    .catch(error => console.error(error));

// POST
axios.post("https://api.example.com/data", {
    name: "John",
    age: 30
})
    .then(response => console.log(response.data));

// With async/await
async function fetchData() {
    try {
        const response = await axios.get("https://api.example.com/data");
        return response.data;
    } catch (error) {
        console.error(error);
    }
}
```

---

## Storage & Cookies

### localStorage
```javascript
// Set
localStorage.setItem("key", "value");
localStorage.setItem("user", JSON.stringify({name: "John"}));

// Get
const value = localStorage.getItem("key");
const user = JSON.parse(localStorage.getItem("user"));

// Remove
localStorage.removeItem("key");

// Clear all
localStorage.clear();

// Check if available
if (typeof Storage !== "undefined") {
    // localStorage available
}
```

### sessionStorage
```javascript
// Same API as localStorage but cleared when tab closes
sessionStorage.setItem("key", "value");
sessionStorage.getItem("key");
sessionStorage.removeItem("key");
sessionStorage.clear();
```

### Cookies
```javascript
// Set cookie
document.cookie = "name=John; expires=Thu, 18 Dec 2024 12:00:00 UTC; path=/";

// Get cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// Delete cookie
document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
```

### IndexedDB
```javascript
// Open database
const request = indexedDB.open("MyDB", 1);

request.onupgradeneeded = (event) => {
    const db = event.target.result;
    const objectStore = db.createObjectStore("users", {keyPath: "id"});
};

request.onsuccess = (event) => {
    const db = event.target.result;
    // Use database
};

// Add data
const transaction = db.transaction(["users"], "readwrite");
const objectStore = transaction.objectStore("users");
objectStore.add({id: 1, name: "John"});
```

---

## Performance Optimization

### Debouncing
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
    // Search logic
}, 300);
```

### Throttling
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
    // Scroll logic
}, 100);
```

### Lazy Loading
```javascript
// Intersection Observer
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.src = entry.target.dataset.src;
            observer.unobserve(entry.target);
        }
    });
});

document.querySelectorAll("img[data-src]").forEach(img => {
    observer.observe(img);
});
```

### Code Splitting
```javascript
// Dynamic imports
const module = await import("./module.js");

// React lazy loading
const LazyComponent = React.lazy(() => import("./Component"));
```

### Memory Management
```javascript
// Avoid memory leaks
// 1. Remove event listeners
element.removeEventListener("click", handler);

// 2. Clear intervals/timeouts
clearInterval(intervalId);
clearTimeout(timeoutId);

// 3. Null references
largeObject = null;

// 4. WeakMap/WeakSet for temporary data
const cache = new WeakMap();
```

---

## Security Best Practices

### XSS Prevention
```javascript
// Escape user input
function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Use textContent instead of innerHTML
element.textContent = userInput; // Safe
// element.innerHTML = userInput; // Dangerous
```

### CSRF Protection
```javascript
// Include CSRF token in requests
fetch("/api/data", {
    method: "POST",
    headers: {
        "X-CSRF-Token": getCsrfToken()
    },
    body: JSON.stringify(data)
});
```

### Content Security Policy
```javascript
// Set CSP header
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

### Input Validation
```javascript
// Validate on client and server
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function sanitizeInput(input) {
    return input.trim().replace(/[<>]/g, "");
}
```

---

## Testing

### Unit Testing (Jest)
```javascript
// test.js
function add(a, b) {
    return a + b;
}

// __tests__/add.test.js
describe("add function", () => {
    test("adds 1 + 2 to equal 3", () => {
        expect(add(1, 2)).toBe(3);
    });
    
    test("handles negative numbers", () => {
        expect(add(-1, -2)).toBe(-3);
    });
});
```

### Test Structure
```javascript
describe("Test Suite", () => {
    beforeAll(() => {
        // Runs once before all tests
    });
    
    beforeEach(() => {
        // Runs before each test
    });
    
    test("test case", () => {
        // Test code
        expect(actual).toBe(expected);
    });
    
    afterEach(() => {
        // Runs after each test
    });
    
    afterAll(() => {
        // Runs once after all tests
    });
});
```

### Async Testing
```javascript
test("async function", async () => {
    const result = await asyncFunction();
    expect(result).toBe(expected);
});

test("promise", () => {
    return promiseFunction().then(result => {
        expect(result).toBe(expected);
    });
});
```

---

## Design Patterns

### Singleton
```javascript
const Singleton = (function() {
    let instance;
    
    function createInstance() {
        return {
            data: "Singleton data"
        };
    }
    
    return {
        getInstance: function() {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();
```

### Factory
```javascript
function createUser(type) {
    if (type === "admin") {
        return new AdminUser();
    } else if (type === "regular") {
        return new RegularUser();
    }
}

class AdminUser {
    constructor() {
        this.role = "admin";
    }
}
```

### Observer
```javascript
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }
    
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => callback(data));
        }
    }
    
    off(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    }
}
```

### Module Pattern
```javascript
const Module = (function() {
    let privateVar = 0;
    
    function privateFunction() {
        return privateVar;
    }
    
    return {
        publicMethod: function() {
            return privateFunction();
        },
        increment: function() {
            privateVar++;
        }
    };
})();
```

### Proxy Pattern
```javascript
const target = {
    message: "hello"
};

const handler = {
    get: function(target, prop) {
        return prop in target ? target[prop] : "default";
    },
    set: function(target, prop, value) {
        target[prop] = value;
        return true;
    }
};

const proxy = new Proxy(target, handler);
```

---

## Advanced Topics

### Proxies
```javascript
const handler = {
    get(target, prop) {
        return prop in target ? target[prop] : 37;
    },
    set(target, prop, value) {
        if (typeof value === "number") {
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
```

### Reflect API
```javascript
const obj = {name: "John"};

Reflect.get(obj, "name"); // "John"
Reflect.set(obj, "age", 30); // true
Reflect.has(obj, "name"); // true
Reflect.deleteProperty(obj, "age"); // true
Reflect.ownKeys(obj); // ["name"]
```

### WeakMap & WeakSet
```javascript
// WeakMap (keys must be objects, weak references)
const weakMap = new WeakMap();
const obj = {};
weakMap.set(obj, "value");
weakMap.get(obj); // "value"

// WeakSet (values must be objects, weak references)
const weakSet = new WeakSet();
weakSet.add(obj);
weakSet.has(obj); // true
```

### Typed Arrays
```javascript
// ArrayBuffer
const buffer = new ArrayBuffer(16);

// Typed arrays
const int8 = new Int8Array(buffer);
const int16 = new Int16Array(buffer);
const float32 = new Float32Array(buffer);

// DataView
const view = new DataView(buffer);
view.setInt8(0, 127);
view.getInt8(0); // 127
```

### Web Workers
```javascript
// main.js
const worker = new Worker("worker.js");
worker.postMessage({data: "Hello"});
worker.onmessage = (event) => {
    console.log(event.data);
};

// worker.js
self.onmessage = (event) => {
    const result = processData(event.data);
    self.postMessage(result);
};
```

### Service Workers
```javascript
// Register
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js")
        .then(registration => console.log("Registered"))
        .catch(error => console.error("Error"));
}

// sw.js
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open("v1").then(cache => {
            return cache.addAll(["/", "/index.html"]);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
```

### WebAssembly
```javascript
// Load and instantiate WASM
WebAssembly.instantiateStreaming(fetch("module.wasm"))
    .then(result => {
        const {add} = result.instance.exports;
        console.log(add(2, 3));
    });
```

---

## Best Practices Summary

### Code Quality
1. **Use const/let, avoid var**
2. **Use strict equality (===)**
3. **Handle errors properly**
4. **Write pure functions when possible**
5. **Use meaningful variable names**
6. **Keep functions small and focused**
7. **Avoid deep nesting**
8. **Use modern ES6+ features**
9. **Comment complex logic**
10. **Follow consistent code style**

### Performance
1. **Minimize DOM manipulation**
2. **Use event delegation**
3. **Debounce/throttle expensive operations**
4. **Lazy load resources**
5. **Use Web Workers for heavy computation**
6. **Cache frequently accessed data**
7. **Avoid memory leaks**
8. **Use requestAnimationFrame for animations**

### Security
1. **Validate and sanitize input**
2. **Use HTTPS**
3. **Implement CSP**
4. **Avoid eval() and innerHTML with user input**
5. **Use parameterized queries for databases**
6. **Implement proper authentication**
7. **Protect against XSS and CSRF**

---

## Resources for Further Learning

1. **MDN Web Docs** - Comprehensive JavaScript reference
2. **JavaScript.info** - Modern JavaScript tutorial
3. **You Don't Know JS** - Deep dive book series
4. **Eloquent JavaScript** - Free online book
5. **JavaScript30** - 30 vanilla JS projects
6. **LeetCode** - Practice algorithms
7. **CodeWars** - Coding challenges
8. **JavaScript Weekly** - Stay updated

---

## Conclusion

This guide covers JavaScript from fundamentals to advanced topics. Mastery comes through:
- **Practice**: Build projects, solve problems
- **Understanding**: Know why, not just how
- **Reading**: Study well-written code
- **Teaching**: Explain concepts to others
- **Staying Current**: Follow JavaScript evolution

Remember: JavaScript is constantly evolving. Keep learning, keep practicing, and keep building!

