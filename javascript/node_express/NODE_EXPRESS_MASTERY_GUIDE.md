# The Complete Node.js & Express.js Mastery Guide

> Every concept explained from first principles — V8 internals, the event loop,
> streams, clustering, the entire Node.js standard library, Express.js architecture,
> middleware, routing, authentication, databases, testing, deployment, and production
> patterns. Written to the same depth as a professional reference.

---

## Table of Contents

### Part I — Node.js Foundations
1. [Why Node.js? V8, the Event Loop & Architecture](#chapter-1-why-nodejs-v8-the-event-loop--architecture)
2. [The Module System — CommonJS & ES Modules](#chapter-2-the-module-system)
3. [npm & the Ecosystem](#chapter-3-npm--the-ecosystem)
4. [Core Built-in Modules](#chapter-4-core-built-in-modules)
5. [The Event System — EventEmitter](#chapter-5-the-event-system--eventemitter)
6. [Streams — The Most Powerful API in Node.js](#chapter-6-streams)
7. [File System — fs Module Deep Dive](#chapter-7-file-system)
8. [Networking — http, https, net, dgram](#chapter-8-networking)
9. [Child Processes & Worker Threads](#chapter-9-child-processes--worker-threads)
10. [Timers, Scheduling & the Event Loop Phases](#chapter-10-timers-scheduling--event-loop-phases)
11. [Buffers, TypedArrays & Binary Data](#chapter-11-buffers-typedarrays--binary-data)
12. [Error Handling Patterns in Node.js](#chapter-12-error-handling-patterns)
13. [Cluster & Load Balancing](#chapter-13-cluster--load-balancing)
14. [Debugging & Profiling Node.js](#chapter-14-debugging--profiling)

### Part II — Express.js Complete
15. [Express.js — Architecture & Philosophy](#chapter-15-expressjs--architecture--philosophy)
16. [Routing — Complete Reference](#chapter-16-routing)
17. [Middleware — Deep Dive](#chapter-17-middleware)
18. [Request & Response Objects](#chapter-18-request--response-objects)
19. [Template Engines & Static Files](#chapter-19-template-engines--static-files)
20. [Error Handling in Express](#chapter-20-error-handling-in-express)

### Part III — Production Express Applications
21. [Authentication & Authorization — JWT, Sessions, OAuth](#chapter-21-authentication--authorization)
22. [Database Integration — PostgreSQL, MongoDB, Redis](#chapter-22-database-integration)
23. [Input Validation & Security](#chapter-23-input-validation--security)
24. [File Uploads & Multipart](#chapter-24-file-uploads--multipart)
25. [WebSockets & Real-Time with Socket.io](#chapter-25-websockets--real-time)
26. [REST API Design & Best Practices](#chapter-26-rest-api-design)
27. [Testing Node.js & Express — Jest, Supertest](#chapter-27-testing)
28. [Logging, Monitoring & Observability](#chapter-28-logging-monitoring--observability)
29. [Configuration & Environment Management](#chapter-29-configuration--environment-management)
30. [Performance, Caching & Scalability](#chapter-30-performance-caching--scalability)
31. [Deployment — Docker, PM2, Nginx](#chapter-31-deployment)
32. [Design Patterns in Node.js](#chapter-32-design-patterns)

---

# PART I — NODE.JS FOUNDATIONS

---

## Chapter 1: Why Node.js? V8, the Event Loop & Architecture

### 1.1 What Node.js Actually Is

Node.js is NOT a language — it is a **runtime environment** for executing JavaScript outside of a browser. It wraps Google's V8 JavaScript engine with a set of C++ bindings that expose the operating system's capabilities to JavaScript.

```
Node.js architecture:

┌───────────────────────────────────────────────────────────────┐
│  Your JavaScript application code                              │
├───────────────────────────────────────────────────────────────┤
│  Node.js Standard Library (JavaScript)                        │
│  fs, http, path, crypto, events, streams, child_process...    │
├───────────────────────────────────────────────────────────────┤
│  Node.js Bindings (C++)                                        │
│  Bridges JS ↔ libuv, OpenSSL, zlib, V8 APIs                  │
├──────────────────┬────────────────────────────────────────────┤
│  V8 (C++)        │  libuv (C)                                 │
│  JS engine:      │  Async I/O & event loop:                   │
│  parse, compile, │  thread pool, epoll/kqueue/IOCP,           │
│  optimize,       │  timers, networking, file system           │
│  garbage collect │                                             │
└──────────────────┴────────────────────────────────────────────┘

V8:     Compiles JS to machine code (JIT), manages JS heap
libuv:  Provides the event loop, thread pool, platform-abstracted async I/O
```

### 1.2 The Problem Node.js Solves

Traditional web servers (Apache, Tomcat) use the **thread-per-request** model:

```
Thread-per-request (Java/Apache):
  Request 1 → Thread 1 → waiting for DB (thread blocked, occupies ~1MB RAM)
  Request 2 → Thread 2 → waiting for DB (blocked)
  Request 3 → Thread 3 → waiting for DB (blocked)
  ...
  Request 1000 → Thread 1000 → 1GB RAM just for idle threads!
  Request 1001 → No thread available → queue or reject

Node.js single-threaded event loop:
  Request 1 → starts DB query → REGISTERS CALLBACK → goes back to event loop
  Request 2 → starts DB query → REGISTERS CALLBACK → goes back to event loop
  Request 3 → starts DB query → REGISTERS CALLBACK → goes back to event loop
  DB finishes for Request 1 → callback fires → response sent
  DB finishes for Request 3 → callback fires → response sent
  DB finishes for Request 2 → callback fires → response sent

  One thread handles thousands of concurrent connections.
  Why? I/O wait time doesn't consume CPU or threads.
```

### 1.3 V8 — JavaScript Engine Internals

```
V8 compilation pipeline:
  Source JS → Parser → AST → Ignition (bytecode interpreter) → Turbofan (JIT)

  1. Parser:   Converts JS source text into an Abstract Syntax Tree (AST)
  2. Ignition: Bytecode interpreter — executes immediately, collects type feedback
  3. Turbofan: Optimizing JIT compiler — recompiles hot functions to machine code
               using type feedback. If types change (deoptimization), falls back.

Key V8 concepts:
  Hidden classes:  V8 builds internal "shapes" for objects based on property order.
                   Objects with same properties in same order share a hidden class.
                   Adding properties out of order creates new hidden class → slower.
  Inline caches:   V8 remembers the type of objects at call sites.
                   Same type every time → fast path (monomorphic).
                   Different types → slower (polymorphic / megamorphic).
  Heap zones:
    New Space:     Short-lived objects. Minor GC (Scavenge) is fast.
    Old Space:     Objects that survived multiple minor GCs. Major GC (Mark-Sweep).
    Code Space:    JIT-compiled code.
    Large Object Space: Objects > 128KB — never moved.
```

```javascript
// Implications for writing fast Node.js code:

// ❌ Bad — breaks hidden class (different shapes for same "type")
function processUser(user) {
  user.processed = true;   // adds property dynamically — may create new hidden class
}

// ✅ Good — define all properties at construction time, in same order
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    this.processed = false;  // defined at construction — consistent hidden class
  }
}

// ❌ Bad — megamorphic call site (V8 can't optimize well)
function add(a, b) { return a + b; }
add(1, 2);          // int + int
add("a", "b");      // string + string
add(1.5, 2.5);      // float + float

// ✅ Good — keep call sites monomorphic (same types every time)
function addInts(a, b)    { return a + b; }  // always called with ints
function addStrings(a, b) { return a + b; }  // always called with strings
```

### 1.4 The Event Loop — The Heart of Node.js

The event loop is a C loop implemented by libuv that continuously processes events. Understanding its phases is essential for writing correct asynchronous code.

```
┌─────────────────────────────────────────────────────────────┐
│                   EVENT LOOP PHASES                          │
│                                                              │
│  ┌──────────┐                                               │
│  │  timers  │  ← setTimeout, setInterval callbacks          │
│  └────┬─────┘                                               │
│       │                                                      │
│  ┌────▼──────────┐                                          │
│  │ pending       │  ← I/O callbacks deferred to next loop   │
│  │ callbacks     │                                           │
│  └────┬──────────┘                                          │
│       │                                                      │
│  ┌────▼──────────┐                                          │
│  │ idle, prepare │  ← internal use                          │
│  └────┬──────────┘                                          │
│       │                                                      │
│  ┌────▼──────────┐                                          │
│  │    poll       │  ← retrieve new I/O events; execute I/O  │
│  │               │    callbacks. If timers ready → timers.  │
│  │               │    If nothing → block & wait here.       │
│  └────┬──────────┘                                          │
│       │                                                      │
│  ┌────▼──────────┐                                          │
│  │    check      │  ← setImmediate() callbacks              │
│  └────┬──────────┘                                          │
│       │                                                      │
│  ┌────▼──────────┐                                          │
│  │  close        │  ← socket.on('close', ...) callbacks     │
│  │  callbacks    │                                           │
│  └────┬──────────┘                                          │
│       │ (loop back)                                          │
└───────┴─────────────────────────────────────────────────────┘

Between EACH phase:
  process.nextTick() queue is drained COMPLETELY
  Promise microtask queue is drained COMPLETELY
  (nextTick runs before promises)
```

```javascript
// Event loop order demonstration — crucial for interviews
console.log('1 - synchronous start');

setTimeout(() => console.log('2 - setTimeout 0ms'), 0);

Promise.resolve().then(() => console.log('3 - Promise.then'));

process.nextTick(() => console.log('4 - nextTick'));

setImmediate(() => console.log('5 - setImmediate'));

console.log('6 - synchronous end');

// Output order:
// 1 - synchronous start
// 6 - synchronous end
// 4 - nextTick          ← nextTick queue (before ANY phase transition)
// 3 - Promise.then      ← microtask queue (after nextTick, before phases)
// 2 - setTimeout 0ms    ← timers phase
// 5 - setImmediate      ← check phase (after poll)

// ⚠️ Between phases, nextTick and Promises always run first
// ⚠️ nextTick is processed before Promises (even though both are "microtasks")
// ⚠️ setTimeout(fn, 0) vs setImmediate: order depends on context
//    - In I/O callback: setImmediate always before setTimeout(fn, 0)
//    - At top level: order is non-deterministic (OS timer resolution)

// Starvation: overloading nextTick prevents I/O from processing
function recurse(n) {
  if (n > 0) process.nextTick(() => recurse(n - 1));
}
// recurse(1_000_000) — I/O callbacks NEVER fire while nextTick queue not empty
// Use setImmediate for recursive scheduling instead:
function safeRecurse(n) {
  if (n > 0) setImmediate(() => safeRecurse(n - 1));
}
```

### 1.5 libuv Thread Pool

```
The event loop runs on the MAIN thread — single-threaded.
BUT: some operations are not async at the OS level (file system, DNS, crypto).
libuv uses a THREAD POOL for these.

Default pool size: 4 threads (configurable: UV_THREADPOOL_SIZE=16)

Operations that use the thread pool:
  fs.readFile, fs.writeFile, fs.stat, etc.  (all fs async operations)
  crypto.pbkdf2, crypto.randomBytes (CPU-intensive crypto)
  dns.lookup (not dns.resolve — that's network async)
  zlib compression operations
  User-defined C++ addons that opt in

Operations that do NOT use thread pool (handled by OS async):
  TCP/UDP networking (epoll/kqueue/IOCP)
  Pipes
  Child process (fork/spawn)
  Timers

Implication: if you do 4 fs.readFile() concurrently with pool size 4,
a 5th fs.readFile() waits for a pool thread to become free.
```

```javascript
// Checking if you're blocking the event loop
const { monitorEventLoopDelay } = require('perf_hooks');

const histogram = monitorEventLoopDelay({ resolution: 10 });
histogram.enable();

setInterval(() => {
  console.log(`Event loop delay: mean=${histogram.mean / 1e6}ms, max=${histogram.max / 1e6}ms`);
  histogram.reset();
}, 5000);

// > 100ms mean delay → you have blocking code; find and fix it
```

---

## Chapter 2: The Module System

### 2.1 CommonJS (CJS) — The Original

```javascript
// CommonJS: require() / module.exports / exports
// Synchronous loading, executed at require() time
// Each file is wrapped in a function by Node.js:
// (function(exports, require, module, __filename, __dirname) {
//   // Your file code here
// })

// ── Exporting ─────────────────────────────────────────────────

// Method 1: module.exports — replace the entire exports object
// math.js
function add(a, b)      { return a + b; }
function subtract(a, b) { return a - b; }
const PI = 3.14159;

module.exports = { add, subtract, PI };        // export an object
// or:
module.exports = function createUser(name) {   // export a single function/class
  return { name, id: Math.random() };
};

// Method 2: exports.name — add properties to the existing exports object
// utils.js
exports.capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
exports.slugify    = (str) => str.toLowerCase().replace(/\s+/g, '-');
exports.VERSION    = '1.0.0';
// ⚠️ NEVER reassign exports itself: exports = {...}  — breaks the reference!
// exports is a REFERENCE to module.exports; reassigning breaks the link.

// ── Importing ─────────────────────────────────────────────────
const math   = require('./math');              // local module (./relative path)
const { add, PI } = require('./math');        // destructuring import
const fs     = require('fs');                  // built-in module
const lodash = require('lodash');              // npm package (looks in node_modules)
const config = require('./config.json');       // JSON files work directly

// require() caches modules — same instance returned on repeated require()
const a = require('./myModule');
const b = require('./myModule');
console.log(a === b);   // true — same cached object

// Clearing cache (useful in tests)
delete require.cache[require.resolve('./myModule')];

// Conditional / dynamic require (runs at call time)
if (process.env.NODE_ENV === 'test') {
  const mock = require('./mocks/db');
}

// __filename and __dirname — available in every CJS module
console.log(__filename); // /home/user/project/src/app.js (absolute path of this file)
console.log(__dirname);  // /home/user/project/src            (directory of this file)

const path = require('path');
const configPath = path.join(__dirname, '..', 'config', 'settings.json');
```

### 2.2 ES Modules (ESM) — Modern Standard

```javascript
// ES Modules: import / export
// Asynchronous loading (allows top-level await), statically analyzable
// Enable: "type": "module" in package.json, or use .mjs extension

// ── Named exports ─────────────────────────────────────────────
// math.mjs
export function add(a, b)      { return a + b; }
export function subtract(a, b) { return a - b; }
export const PI = 3.14159;

// Or export at end:
function multiply(a, b) { return a * b; }
const E = 2.71828;
export { multiply, E };
export { multiply as mult, E as eulerNumber };  // with rename

// ── Default export ────────────────────────────────────────────
// One per module; can be anonymous
export default class Database {
  constructor(url) { this.url = url; }
  connect()        { return Promise.resolve(); }
}
// or:
export default function createApp() { /* ... */ }

// ── Named imports ─────────────────────────────────────────────
import { add, PI } from './math.mjs';
import { add as sum, PI as pi } from './math.mjs';     // rename on import
import * as MathUtils from './math.mjs';               // namespace import
import DefaultExport from './database.mjs';             // default import
import DefaultExport, { namedExport } from './module.mjs'; // both

// ── Dynamic import — async, returns Promise ───────────────────
// Can import ESM or CJS from ESM
const module = await import('./heavy-module.mjs');
module.default();       // access default export
module.namedExport();   // access named export

// Conditional dynamic import (code splitting)
async function loadPlugin(name) {
  const plugin = await import(`./plugins/${name}.mjs`);
  return plugin.default;
}

// ── Top-level await (ESM only) ────────────────────────────────
// Only available in ES modules — allows await at module scope
const config = await loadConfig();          // blocks module loading until resolved
const db     = await connectToDatabase();   // executes before any importer runs

export { config, db };

// ── Import assertions (Node 18+) ─────────────────────────────
import data from './data.json' assert { type: 'json' };

// ── __filename and __dirname equivalents in ESM ───────────────
import { fileURLToPath } from 'url';
import { dirname }       from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
// Or: import.meta.url gives you the file URL directly
```

### 2.3 CJS vs ESM — When to Use Which

```
CommonJS (require/module.exports):
  ✅ All Node.js versions (it was the only system until Node 12)
  ✅ Works with most npm packages
  ✅ Dynamic require() — conditional imports at runtime
  ✅ Synchronous — simpler mental model
  ❌ Cannot use top-level await
  ❌ Not statically analyzable (tree shaking harder)
  ❌ Interop with ESM packages requires workarounds
  ❌ .js extension, package.json must NOT have "type":"module"

ES Modules (import/export):
  ✅ Standard (works in browser and Node.js)
  ✅ Static analysis → tree shaking, better IDE support
  ✅ Top-level await
  ✅ Named exports cleaner than module.exports
  ❌ Requires "type":"module" in package.json or .mjs extension
  ❌ require() not available (use createRequire() wrapper if needed)
  ❌ __filename / __dirname not available (use import.meta.url)
  ❌ Some CJS-only packages require workarounds

Interoperability:
  ESM can import CJS:  import cjsModule from './legacy.cjs';  (default import only)
  CJS cannot import ESM directly (require() is sync; ESM loading is async)
    Workaround: import() dynamic import or async IIFE
```

### 2.4 Module Resolution Algorithm

```javascript
// When you write: require('express')
// Node.js follows this algorithm:

// 1. Is it a core module? (fs, http, path, etc.) → use it
// 2. Does it start with ./ ../ /? → file path
//    a. Try exact path
//    b. Try path + .js, .json, .node
//    c. Try path as directory: path/index.js, path/index.json
// 3. Otherwise: look in node_modules
//    Starting from current directory, walk UP the tree:
//    ./node_modules/express
//    ../node_modules/express
//    ../../node_modules/express
//    ... (until filesystem root)

// package.json "main" field: specifies entry point for packages
// package.json "exports" field (modern): fine-grained export control
// package.json "type" field: "module" or "commonjs"

// Example package.json with exports map:
// {
//   "name": "mypackage",
//   "exports": {
//     ".": {
//       "import": "./dist/esm/index.js",   // for ESM consumers
//       "require": "./dist/cjs/index.js",  // for CJS consumers
//       "types": "./dist/types/index.d.ts"  // for TypeScript
//     },
//     "./utils": "./dist/utils.js",         // subpath exports
//   }
// }
```

---

## Chapter 3: npm & the Ecosystem

### 3.1 package.json — Complete Reference

```json
{
  "name": "my-app",
  "version": "1.2.3",
  "description": "A production Node.js application",
  "type": "module",
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import":  "./dist/index.esm.js",
      "require": "./dist/index.cjs.js",
      "types":   "./dist/index.d.ts"
    }
  },
  "scripts": {
    "start":         "node dist/index.js",
    "dev":           "nodemon --watch src --ext ts,js --exec 'ts-node src/index.ts'",
    "build":         "tsc -p tsconfig.json",
    "test":          "jest --coverage",
    "test:watch":    "jest --watch",
    "lint":          "eslint src --ext .ts,.js",
    "lint:fix":      "eslint src --ext .ts,.js --fix",
    "format":        "prettier --write 'src/**/*.{ts,js}'",
    "typecheck":     "tsc --noEmit",
    "clean":         "rm -rf dist coverage",
    "prestart":      "npm run build",
    "prepare":       "husky install",
    "postinstall":   "node scripts/setup.js"
  },
  "dependencies": {
    "express":       "^4.18.2",
    "pg":            "^8.11.3",
    "redis":         "^4.6.10",
    "jsonwebtoken":  "^9.0.2",
    "bcryptjs":      "^2.4.3",
    "zod":           "^3.22.4",
    "pino":          "^8.17.2",
    "dotenv":        "^16.3.1"
  },
  "devDependencies": {
    "@types/express":     "^4.17.21",
    "@types/node":        "^20.10.0",
    "typescript":         "^5.3.3",
    "ts-node":            "^10.9.2",
    "nodemon":            "^3.0.2",
    "jest":               "^29.7.0",
    "supertest":          "^6.3.3",
    "@types/jest":        "^29.5.11",
    "eslint":             "^8.56.0",
    "prettier":           "^3.1.1"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm":  ">=9.0.0"
  },
  "license":   "MIT",
  "private":   true,
  "keywords":  ["api", "rest", "nodejs"],
  "repository": {
    "type": "git",
    "url":  "https://github.com/user/repo.git"
  }
}
```

### 3.2 npm Commands — Complete Reference

```bash
# ── Project setup ─────────────────────────────────────────────
npm init                      # interactive setup
npm init -y                   # defaults (skip prompts)
npm init @scope/template      # from template (e.g. npm init fastify)

# ── Installing packages ───────────────────────────────────────
npm install                   # install all from package.json + package-lock.json
npm install express           # add to dependencies
npm install --save-dev jest   # add to devDependencies
npm install --save-optional sharp  # add to optionalDependencies
npm install -g nodemon        # global install (avoid; use npx instead)
npm install express@4.18.2    # specific version
npm install express@^4        # latest v4.x
npm install express@latest    # latest stable
npm install github:user/repo  # from GitHub
npm install ./local-package   # from local path
npm ci                        # clean install (ONLY from package-lock.json; CI/CD use)

# ── Version management ────────────────────────────────────────
npm update                    # update packages to semver-compatible versions
npm update express            # update specific package
npm outdated                  # list packages with newer versions available
npm audit                     # check for known vulnerabilities
npm audit fix                 # auto-fix vulnerabilities
npm audit fix --force         # fix including breaking changes

# ── Inspecting packages ───────────────────────────────────────
npm list                      # tree of installed packages
npm list --depth=0            # only direct dependencies
npm ls express                # why is express installed
npm info express              # metadata about package
npm info express versions     # all published versions

# ── Running scripts ───────────────────────────────────────────
npm run start
npm run test -- --coverage    # pass args to script
npm test                      # shorthand for npm run test
npm start                     # shorthand for npm run start

# ── npx — run without installing globally ─────────────────────
npx create-react-app myapp    # run package temporarily
npx ts-node src/index.ts      # run TypeScript directly
npx --yes jest                # auto-install if needed

# ── Publishing ────────────────────────────────────────────────
npm publish                   # publish to npm registry
npm publish --access public   # for scoped packages (@scope/name)
npm version patch             # bump patch version (1.0.0 → 1.0.1)
npm version minor             # bump minor (1.0.1 → 1.1.0)
npm version major             # bump major (1.1.0 → 2.0.0)
```

### 3.3 Semantic Versioning & package-lock.json

```
Semantic Versioning: MAJOR.MINOR.PATCH
  MAJOR: breaking changes (incompatible API)
  MINOR: new features (backward compatible)
  PATCH: bug fixes (backward compatible)

Version specifiers in package.json:
  "1.2.3"   exact version only
  "^1.2.3"  compatible: 1.x.x (same major; allows minor and patch updates)
  "~1.2.3"  approximately: 1.2.x (same major and minor; allows patch updates)
  ">=1.2.3" at least this version
  "*"        any version (dangerous)
  "1.x"     any 1.x.x version

package-lock.json:
  Created automatically by npm install
  Locks EXACT versions of ALL packages (including transitive dependencies)
  Guarantees identical installs across machines and CI
  ALWAYS commit this file to version control!
  npm ci uses ONLY this file — fails if package.json and lock are out of sync
```

---

## Chapter 4: Core Built-in Modules

### 4.1 path — File Paths

```javascript
const path = require('path');

// path.join — join segments with OS separator (handles extra slashes, ..)
path.join('/home', 'user', 'docs', 'file.txt'); // '/home/user/docs/file.txt'
path.join('/home', 'user', '../other', 'file'); // '/home/other/file' (resolves ..)
path.join(__dirname, 'config', 'settings.json'); // absolute path from current file

// path.resolve — resolve to ABSOLUTE path (from right, stops when absolute)
path.resolve('folder', 'file.txt');       // cwd + /folder/file.txt
path.resolve('/home', 'user', 'file.txt'); // '/home/user/file.txt'
path.resolve('/home', '/abs', 'file.txt'); // '/abs/file.txt' (restarts from /abs)

// Decomposing paths
const p = '/home/alice/project/src/index.js';
path.dirname(p);   // '/home/alice/project/src'
path.basename(p);  // 'index.js'
path.basename(p, '.js'); // 'index' (strip extension)
path.extname(p);   // '.js'
path.parse(p);
// { root: '/', dir: '/home/alice/project/src', base: 'index.js',
//   ext: '.js', name: 'index' }
path.format({ dir: '/home', base: 'file.txt' }); // '/home/file.txt'

// Normalizing
path.normalize('/home//user/../alice/./file.txt'); // '/home/alice/file.txt'

// Relative path between two absolute paths
path.relative('/home/user/a', '/home/user/b/file.txt'); // '../b/file.txt'

// Platform-specific
path.sep;     // '/' on Unix, '\\' on Windows
path.delimiter; // ':' on Unix, ';' on Windows (for PATH env var)
path.posix.join('/a', 'b');  // always forward slashes
path.win32.join('C:\\', 'a'); // always backslashes
```

### 4.2 os — Operating System Info

```javascript
const os = require('os');

os.platform();     // 'linux', 'darwin', 'win32'
os.arch();         // 'x64', 'arm64', 'ia32'
os.release();      // OS version string
os.version();      // kernel version (Linux) or OS version (macOS)
os.type();         // 'Linux', 'Darwin', 'Windows_NT'

os.hostname();     // computer's hostname
os.homedir();      // '/home/alice' or 'C:\\Users\\Alice'
os.tmpdir();       // '/tmp' or 'C:\\Temp'

os.cpus();         // array of CPU core info { model, speed, times }
os.cpus().length;  // number of logical CPU cores

os.totalmem();     // total system RAM in bytes
os.freemem();      // free RAM in bytes
(os.freemem() / os.totalmem() * 100).toFixed(1) + '%'; // free percent

os.loadavg();      // [1min, 5min, 15min] load averages (Unix only; [] on Windows)

os.networkInterfaces(); // network interface info (IP addresses, MAC, etc.)

os.userInfo();     // { uid, gid, username, homedir, shell }

os.EOL;            // '\n' on Unix, '\r\n' on Windows
os.devNull;        // '/dev/null' on Unix, '\\\\.\\nul' on Windows
```

### 4.3 url & querystring

```javascript
const { URL, URLSearchParams } = require('url'); // or global in Node 10+

// URL — WHATWG URL API (modern, preferred)
const url = new URL('https://api.example.com:3000/users?limit=10&page=2#section1');

url.href;       // 'https://api.example.com:3000/users?limit=10&page=2#section1'
url.protocol;   // 'https:'
url.host;       // 'api.example.com:3000'
url.hostname;   // 'api.example.com'
url.port;       // '3000'
url.pathname;   // '/users'
url.search;     // '?limit=10&page=2'
url.hash;       // '#section1'
url.origin;     // 'https://api.example.com:3000'

url.searchParams.get('limit');      // '10'
url.searchParams.getAll('tag');     // all values for 'tag'
url.searchParams.set('limit', '20');
url.searchParams.append('tag', 'node');
url.searchParams.delete('page');
url.searchParams.has('limit');      // true
for (const [key, val] of url.searchParams) { /* iterate */ }
url.searchParams.toString();        // 'limit=20&tag=node'

// Resolving relative URLs
new URL('/users/1', 'https://api.example.com').href; // 'https://api.example.com/users/1'

// URLSearchParams standalone
const params = new URLSearchParams({ name: 'Alice', age: '30', tags: ['a','b'] });
params.toString(); // 'name=Alice&age=30&tags=a&tags=b'

// url.parse / url.format (legacy, still widely used)
const urlLegacy = require('url');
const parsed = urlLegacy.parse('https://example.com/path?q=1', true); // true = parse query
parsed.query; // { q: '1' }  — as object with true flag
```

### 4.4 crypto — Cryptography

```javascript
const crypto = require('crypto');

// ── Hashing ───────────────────────────────────────────────────
const hash = crypto.createHash('sha256');
hash.update('data to hash');
hash.update(' more data');   // can call update multiple times
const digest = hash.digest('hex'); // 'base64', 'hex', or Buffer

// One-liner
const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const md5    = (data) => crypto.createHash('md5').update(data).digest('hex');

// HMAC (keyed hash — for message authentication)
const hmac = crypto.createHmac('sha256', 'secret-key');
hmac.update('message');
const mac = hmac.digest('hex');

// Verify HMAC (timing-safe comparison!)
const expectedMac = computeHmac(message);
const isValid = crypto.timingSafeEqual(
  Buffer.from(receivedMac, 'hex'),
  Buffer.from(expectedMac, 'hex')
);
// NEVER use === for MAC comparison — timing attacks!

// ── Random bytes ──────────────────────────────────────────────
const randomBytes   = crypto.randomBytes(32);       // Buffer of 32 random bytes
const randomHex     = crypto.randomBytes(32).toString('hex');  // 64-char hex string
const randomBase64  = crypto.randomBytes(32).toString('base64');
const randomUUID    = crypto.randomUUID();          // 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
const randomInt     = crypto.randomInt(1, 100);     // integer in [1, 100)

// ── Password hashing — use bcrypt (safer than crypto directly) ─
// npm install bcryptjs
const bcrypt = require('bcryptjs');
const hash2  = await bcrypt.hash('userPassword', 12);   // 12 = cost factor
const valid  = await bcrypt.compare('userPassword', hash2); // true

// ── Key derivation (when you must use crypto) ─────────────────
const { promisify } = require('util');
const pbkdf2 = promisify(crypto.pbkdf2);

const salt    = crypto.randomBytes(32);
const derived = await pbkdf2('password', salt, 100000, 64, 'sha512');
// iterations=100000, keyLength=64 bytes, digest=sha512

// ── Symmetric encryption (AES-GCM — authenticated encryption) ─
function encrypt(text, key) {
  const iv         = crypto.randomBytes(16);
  const cipher     = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted  = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()]);
  const authTag    = cipher.getAuthTag();
  return { iv: iv.toString('hex'), encrypted: encrypted.toString('hex'), authTag: authTag.toString('hex') };
}

function decrypt({ iv, encrypted, authTag }, key) {
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'hex'));
  decipher.setAuthTag(Buffer.from(authTag, 'hex'));
  return decipher.update(Buffer.from(encrypted, 'hex')) + decipher.final('utf8');
}

const key  = crypto.randomBytes(32);  // 256-bit key
const data = encrypt('secret message', key);
const orig = decrypt(data, key);

// ── Hashing to compare passwords (DO NOT — use bcrypt instead) ─
// crypto.createHash for passwords is WRONG — it's too fast, easily brute-forced
// Always use bcrypt, argon2, or scrypt for passwords
```

### 4.5 util — Utilities

```javascript
const util = require('util');

// ── Promisify — convert callback-style to Promise ─────────────
const fs          = require('fs');
const readFile    = util.promisify(fs.readFile);
const writeFile   = util.promisify(fs.writeFile);

// Before promisify:
fs.readFile('/etc/hosts', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// After promisify:
const data = await readFile('/etc/hosts', 'utf8');
console.log(data);

// Functions that follow Node.js callback convention (err-first) work automatically
// If function has custom last-arg convention, use util.promisify.custom symbol

// ── callbackify — convert Promise to callback style ───────────
async function asyncFn() { return 'result'; }
const callbackFn = util.callbackify(asyncFn);
callbackFn((err, result) => {
  if (err) throw err;
  console.log(result); // 'result'
});

// ── util.inspect — deep inspection ───────────────────────────
const obj = { a: 1, b: [1, 2, { c: 3 }], fn: () => {} };
console.log(util.inspect(obj, {
  depth: null,         // unlimited depth (null = unlimited)
  colors: true,        // ANSI color codes
  compact: false,      // multiline output
  showHidden: false,   // show non-enumerable properties
  breakLength: 80,     // line wrap length
}));

// ── util.format — printf-style formatting ────────────────────
util.format('%s has %d messages', 'Alice', 5); // 'Alice has 5 messages'
util.format('%j', { a: 1 });                   // '{"a":1}' (JSON)
util.format('%o', { a: 1 });                   // util.inspect style

// ── util.types — type checks ─────────────────────────────────
util.types.isPromise(Promise.resolve());    // true
util.types.isGeneratorFunction(function*(){}); // true
util.types.isAsyncFunction(async () => {}); // true
util.types.isDate(new Date());              // true
util.types.isMap(new Map());                // true
util.types.isSet(new Set());                // true

// ── util.deprecate — mark deprecated APIs ────────────────────
const oldFunction = util.deprecate(
  () => 'legacy result',
  'oldFunction is deprecated; use newFunction instead',
  'DEP001'
);
// Prints warning once, then runs the function

// ── TextEncoder / TextDecoder ─────────────────────────────────
const encoder = new util.TextEncoder();
const decoder = new util.TextDecoder('utf-8');
const bytes   = encoder.encode('hello');   // Uint8Array
const str     = decoder.decode(bytes);     // 'hello'

// ── util.parseArgs (Node 18+) ────────────────────────────────
const { values, positionals } = util.parseArgs({
  args: process.argv.slice(2),
  options: {
    port:  { type: 'string',  short: 'p', default: '3000' },
    debug: { type: 'boolean', short: 'd', default: false },
    env:   { type: 'string',  short: 'e' },
  },
  allowPositionals: true,
});
// node app.js -p 8080 -d --env production file.txt
// values = { port: '8080', debug: true, env: 'production' }
// positionals = ['file.txt']
```

### 4.6 process — The Process Object

```javascript
// process is a global — no require() needed

// ── Environment ───────────────────────────────────────────────
process.env.NODE_ENV          // 'development', 'production', 'test'
process.env.PORT              // environment variable
process.env.DATABASE_URL
// Always set sensitive values via environment, never hardcode

// ── Arguments ────────────────────────────────────────────────
process.argv                  // ['node', 'script.js', 'arg1', 'arg2']
process.argv.slice(2)         // ['arg1', 'arg2'] — just user args
process.execArgv              // ['--max-old-space-size=4096'] — node flags

// ── Process info ─────────────────────────────────────────────
process.pid                   // process ID
process.ppid                  // parent process ID
process.version               // 'v20.10.0'
process.versions              // { node: '20.10.0', v8: '11.3.244', ... }
process.platform              // 'linux', 'darwin', 'win32'
process.arch                  // 'x64', 'arm64'
process.cwd()                 // current working directory
process.chdir('/tmp')         // change working directory
process.uptime()              // seconds since process started
process.hrtime.bigint()       // nanosecond-precision timer (for benchmarks)
process.memoryUsage()         // { rss, heapTotal, heapUsed, external, arrayBuffers }
process.cpuUsage()            // { user, system } microseconds

// ── Standard I/O ─────────────────────────────────────────────
process.stdin                 // readable stream (keyboard / piped input)
process.stdout                // writable stream (terminal / pipe)
process.stderr                // writable stream (error output)

process.stdout.write('no newline');
process.stderr.write('error message\n');
// console.log uses process.stdout internally
// console.error uses process.stderr

// ── Exit ─────────────────────────────────────────────────────
process.exit(0)               // exit with code 0 (success)
process.exit(1)               // exit with code 1 (error)
// process.exit() is SYNCHRONOUS — skips async cleanup!

// Graceful exit: use events
process.on('exit', (code) => {
  // Synchronous only — last chance to clean up
  // Cannot do async here
  fs.writeFileSync('shutdown.log', `Exited with code ${code}`);
});

process.on('beforeExit', async (code) => {
  // Called when event loop is empty (before exit)
  // CAN do async here — will prevent exit if you queue more work
  await flushLogs();
});

// ── Signal handling ───────────────────────────────────────────
process.on('SIGTERM', async () => {
  // Docker stop, Kubernetes pod termination, kill -15
  console.log('SIGTERM received — graceful shutdown starting');
  await server.close();
  await database.disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  // Ctrl+C in terminal
  console.log('SIGINT received — shutting down');
  process.exit(0);
});

// ── Uncaught error handlers ───────────────────────────────────
process.on('uncaughtException', (error, origin) => {
  // Synchronous code threw and nothing caught it
  // Log and exit — process is in UNKNOWN STATE; restart it!
  console.error('Uncaught exception:', error);
  console.error('Origin:', origin);
  process.exit(1);  // MUST exit; continuing is dangerous
});

process.on('unhandledRejection', (reason, promise) => {
  // A Promise was rejected and nothing caught it
  // In Node 15+: automatically crashes the process (like uncaughtException)
  console.error('Unhandled rejection:', reason);
  // process.exit(1); // explicitly exit
});

process.on('warning', (warning) => {
  console.warn('Warning:', warning.name, warning.message);
});
```

---

## Chapter 5: The Event System — EventEmitter

### 5.1 EventEmitter — Foundation of Node.js

```javascript
const { EventEmitter } = require('events');
// Or: const EventEmitter = require('events').EventEmitter;

const emitter = new EventEmitter();

// ── Emitting and listening ────────────────────────────────────
emitter.on('data', (chunk) => {
  console.log('Received:', chunk);
});

emitter.on('data', (chunk) => {
  process(chunk);  // second listener — both fire
});

emitter.emit('data', 'hello');   // fires all 'data' listeners synchronously
emitter.emit('data', Buffer.from('binary'));

// once — fires only the first time
emitter.once('connect', () => {
  console.log('Connected!');  // only runs on first 'connect' event
});

// ── Removing listeners ────────────────────────────────────────
const handler = (data) => console.log(data);
emitter.on('event', handler);
emitter.off('event', handler);       // remove specific listener (Node 10+)
emitter.removeListener('event', handler);  // same as off
emitter.removeAllListeners('event'); // remove all 'event' listeners
emitter.removeAllListeners();        // remove ALL listeners for ALL events

// ── Listener inspection ───────────────────────────────────────
emitter.listenerCount('data');       // number of listeners for 'data'
emitter.listeners('data');           // array of listener functions
emitter.eventNames();                // ['data', 'connect', ...]
emitter.rawListeners('data');        // includes 'once' wrappers

// ── Max listeners warning ─────────────────────────────────────
// Default: warn after 10 listeners (possible memory leak)
emitter.setMaxListeners(20);         // increase limit for this emitter
EventEmitter.defaultMaxListeners = 20; // global default
emitter.getMaxListeners();           // current limit

// ── Error events — SPECIAL HANDLING ──────────────────────────
// 'error' event without listener → crashes the process!
emitter.on('error', (err) => {
  console.error('Emitter error:', err);
  // handle it; don't re-throw unless you want to crash
});
emitter.emit('error', new Error('something went wrong')); // handled

// ── prepend — add listener to FRONT of queue ──────────────────
emitter.prependListener('data', (d) => console.log('fires first:', d));
emitter.prependOnceListener('data', (d) => console.log('once, first'));
```

### 5.2 Extending EventEmitter — The Right Pattern

```javascript
const { EventEmitter } = require('events');
const { createReadStream } = require('fs');

// Extend EventEmitter for your own classes
class DataPipeline extends EventEmitter {
  #running = false;
  #paused  = false;

  constructor(options = {}) {
    super();
    this.batchSize = options.batchSize ?? 100;
    this.retries   = options.retries ?? 3;
  }

  async start(source) {
    if (this.#running) throw new Error('Pipeline already running');
    this.#running = true;
    this.emit('start', { source });

    try {
      let batch = [];
      for await (const item of source) {
        if (this.#paused) {
          await this.#waitForResume();
        }

        batch.push(item);
        this.emit('item', item);

        if (batch.length >= this.batchSize) {
          this.emit('batch', batch);
          batch = [];
        }
      }

      if (batch.length > 0) {
        this.emit('batch', batch);   // final incomplete batch
      }

      this.emit('end');
    } catch (err) {
      this.emit('error', err);      // propagate errors as events
    } finally {
      this.#running = false;
    }
  }

  pause()  { this.#paused = true;  this.emit('pause');  }
  resume() { this.#paused = false; this.emit('resume'); }

  #waitForResume() {
    return new Promise(resolve => this.once('resume', resolve));
  }
}

// Usage
const pipeline = new DataPipeline({ batchSize: 50 });

pipeline.on('start',  ({ source }) => console.log(`Processing ${source}`));
pipeline.on('item',   (item)       => /* process */ null);
pipeline.on('batch',  (batch)      => db.bulkInsert(batch));
pipeline.on('end',    ()           => console.log('Done!'));
pipeline.on('error',  (err)        => console.error('Pipeline error:', err));

await pipeline.start(dataSource);


// ── EventEmitter with TypeScript (for type safety) ────────────
// npm install typed-emitter (or use EventEmitter generic with declaration merging)
import { EventEmitter } from 'events';
import TypedEmitter from 'typed-emitter';

interface DataPipelineEvents {
  start:  (source: string) => void;
  item:   (item: Record<string, unknown>) => void;
  batch:  (batch: Record<string, unknown>[]) => void;
  end:    () => void;
  error:  (err: Error) => void;
  pause:  () => void;
  resume: () => void;
}

class TypedDataPipeline extends (EventEmitter as new() => TypedEmitter<DataPipelineEvents>) {
  // now emitter.on('item', ...) knows the callback signature
}
```

### 5.3 Async EventEmitter Patterns

```javascript
const { EventEmitter, once } = require('events');

// events.once — wait for a single event as a Promise
const emitter = new EventEmitter();
setTimeout(() => emitter.emit('ready', 'data'), 1000);

const [data] = await once(emitter, 'ready');  // waits for 'ready', destructures args
console.log(data); // 'data'

// With timeout (prevent hanging forever)
const { once: onceEvent } = require('events');
async function waitForEvent(emitter, event, timeoutMs = 5000) {
  const timeoutError = new Error(`Timeout waiting for '${event}' (${timeoutMs}ms)`);
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(timeoutError), timeoutMs)
  );
  return Promise.race([onceEvent(emitter, event), timeout]);
}

// events.on — async iterable for multiple events
const { on } = require('events');

async function processEvents(emitter) {
  for await (const [data] of on(emitter, 'data')) {
    await process(data);
    // 'break' to stop iteration
  }
}
// Note: on() creates an internal queue; events emitted before consumption are buffered
```

---

## Chapter 6: Streams

### 6.1 Why Streams?

```
Problem without streams: load entire file into memory
  fs.readFile('10GB.video', callback)  → needs 10GB RAM → crashes!

Problem with streams: read/process in small chunks
  fs.createReadStream('10GB.video')    → uses ~64KB RAM at a time → works!

Streams are EventEmitters that represent a sequence of data over time.
They are the most important and most misunderstood API in Node.js.

Four types of streams:
  Readable:  data flows OUT  (fs.createReadStream, http.IncomingMessage, process.stdin)
  Writable:  data flows IN   (fs.createWriteStream, http.ServerResponse, process.stdout)
  Duplex:    both directions (net.Socket — TCP socket)
  Transform: read + modify   (zlib.createGzip — compress as data passes through)
```

### 6.2 Readable Streams

```javascript
const fs        = require('fs');
const { Readable } = require('stream');

// ── Consuming readable streams ────────────────────────────────

// Method 1: 'data' event (flowing mode — push data as fast as possible)
const readable = fs.createReadStream('large-file.txt', { encoding: 'utf8' });

readable.on('data', (chunk) => {
  console.log(`Received ${chunk.length} bytes`);
  // ⚠️ data arrives as fast as the source can produce it
  // if your handler is slow → backpressure accumulates in memory
});

readable.on('end', () => console.log('Done reading'));
readable.on('error', (err) => console.error('Read error:', err));

// Method 2: for await...of (async iteration — BEST for most cases)
// Handles backpressure automatically, cleaner async code
async function processFile(path) {
  const stream = fs.createReadStream(path, { encoding: 'utf8', highWaterMark: 64 * 1024 });

  for await (const chunk of stream) {
    await processChunk(chunk);  // backpressure: stream pauses while we await
  }
}

// Method 3: pipe (connect readable to writable)
const readStream  = fs.createReadStream('input.txt');
const writeStream = fs.createWriteStream('output.txt');
readStream.pipe(writeStream);  // handles backpressure automatically
// writeStream automatically closed when readStream ends

// Method 4: pipeline (pipe with proper error handling — PREFERRED)
const { pipeline } = require('stream/promises');
const zlib = require('zlib');

await pipeline(
  fs.createReadStream('input.txt'),
  zlib.createGzip(),                    // compress on the fly
  fs.createWriteStream('output.txt.gz')
);
// If ANY stream errors → ALL streams are closed and error is thrown

// ── Creating custom readable streams ─────────────────────────
class NumberStream extends Readable {
  constructor(options = {}) {
    super({ ...options, objectMode: true }); // objectMode: emit objects, not Buffers
    this.current = options.start ?? 0;
    this.end     = options.end ?? 100;
  }

  _read() {
    // Called by the stream system when consumer is ready for more data
    // Push data until push() returns false (consumer is full → backpressure)
    while (this.current <= this.end) {
      const shouldContinue = this.push(this.current++);
      if (!shouldContinue) return; // stop pushing — resume when _read called again
    }
    this.push(null); // null signals end of stream
  }
}

const numbers = new NumberStream({ start: 1, end: 10 });
for await (const num of numbers) {
  console.log(num); // 1 2 3 ... 10
}

// Readable.from() — create readable from any iterable or async iterable
const { Readable } = require('stream');
const readable2 = Readable.from([1, 2, 3, 4, 5], { objectMode: true });
const readable3 = Readable.from(async function* () {
  for (let i = 0; i < 100; i++) {
    await sleep(10);
    yield { id: i, data: `item-${i}` };
  }
}());
```

### 6.3 Writable Streams

```javascript
const { Writable } = require('stream');

// ── Writing to writable streams ───────────────────────────────
const writeStream = fs.createWriteStream('output.txt');

// write() returns false when internal buffer is full (backpressure signal)
const canContinue = writeStream.write('chunk of data\n', 'utf8');
if (!canContinue) {
  // wait for 'drain' event before writing more
  await new Promise(resolve => writeStream.once('drain', resolve));
}

writeStream.write(Buffer.from([0x00, 0x01, 0x02])); // binary data
writeStream.end('final line\n'); // flush and close (optional final chunk)
await new Promise((resolve, reject) => {
  writeStream.on('finish', resolve);  // 'finish' after end() + all data flushed
  writeStream.on('error', reject);
});

// ── Custom writable stream ────────────────────────────────────
class DatabaseWriter extends Writable {
  constructor(db, options = {}) {
    super({ ...options, objectMode: true });
    this.db = db;
    this.batch = [];
    this.batchSize = options.batchSize ?? 100;
  }

  async _write(chunk, encoding, callback) {
    // Called for each write(); call callback when done
    // callback(err) to signal error; callback() to signal success
    try {
      this.batch.push(chunk);
      if (this.batch.length >= this.batchSize) {
        await this.db.bulkInsert(this.batch);
        this.batch = [];
      }
      callback(); // signal ready for next chunk
    } catch (err) {
      callback(err); // propagate error through stream
    }
  }

  async _final(callback) {
    // Called when end() is called — flush remaining data
    try {
      if (this.batch.length > 0) {
        await this.db.bulkInsert(this.batch);
        this.batch = [];
      }
      callback();
    } catch (err) {
      callback(err);
    }
  }

  _writev(chunks, callback) {
    // Optional: handle multiple buffered chunks at once (more efficient)
    const allChunks = chunks.map(({ chunk }) => chunk);
    this.db.bulkInsert(allChunks).then(() => callback(), callback);
  }
}
```

### 6.4 Transform Streams

```javascript
const { Transform } = require('stream');

// Transform: read data in, transform it, push transformed data out
class CSVParser extends Transform {
  constructor(options = {}) {
    super({ ...options, readableObjectMode: true }); // emit objects
    this.buffer   = '';
    this.headers  = null;
    this.isFirst  = true;
  }

  _transform(chunk, encoding, callback) {
    this.buffer += chunk.toString('utf8');
    const lines  = this.buffer.split('\n');
    this.buffer  = lines.pop(); // last incomplete line stays in buffer

    for (const line of lines) {
      if (!line.trim()) continue;

      const values = this.#parseCSVLine(line);

      if (this.isFirst) {
        this.headers = values;
        this.isFirst = false;
        continue;
      }

      const obj = {};
      this.headers.forEach((header, i) => { obj[header] = values[i] ?? null; });
      this.push(obj); // push object to readable side
    }

    callback(); // ready for next chunk
  }

  _flush(callback) {
    // Process any remaining buffered data
    if (this.buffer.trim()) {
      const values = this.#parseCSVLine(this.buffer);
      if (this.headers && values.length === this.headers.length) {
        const obj = {};
        this.headers.forEach((h, i) => { obj[h] = values[i]; });
        this.push(obj);
      }
    }
    callback();
  }

  #parseCSVLine(line) {
    // Simplified CSV parser (real one handles quoted values)
    return line.split(',').map(v => v.trim());
  }
}

// Usage
await pipeline(
  fs.createReadStream('data.csv'),
  new CSVParser(),
  new Writable({
    objectMode: true,
    write(obj, enc, cb) {
      console.log('Row:', obj);
      cb();
    }
  })
);

// Built-in transform streams
const zlib = require('zlib');
const { createCipheriv, createDecipheriv, randomBytes } = require('crypto');

// Compression pipeline
await pipeline(
  fs.createReadStream('large.json'),
  zlib.createGzip(),                 // compress
  fs.createWriteStream('large.json.gz')
);

// Decompression pipeline
await pipeline(
  fs.createReadStream('large.json.gz'),
  zlib.createGunzip(),               // decompress
  fs.createWriteStream('large.json')
);
```

### 6.5 Backpressure — The Most Important Concept

```javascript
// Backpressure: producer is faster than consumer → memory builds up → crash
// Proper stream usage handles this automatically

// ❌ BAD: ignoring backpressure — fills memory
const readable = fs.createReadStream('huge.bin');
const writable = net.createConnection(3000);

readable.on('data', (chunk) => {
  writable.write(chunk); // if writable is slow, chunks pile up in memory!
});

// ✅ GOOD: pipe handles backpressure automatically
readable.pipe(writable);
// When writable buffer is full: write() returns false
// pipe() listens for 'drain' and pauses the readable

// ✅ BEST: pipeline with async/await error handling
const { pipeline } = require('stream/promises');
await pipeline(readable, writable);

// Manual backpressure implementation (for understanding):
async function manualPipe(readable, writable) {
  for await (const chunk of readable) {
    const ok = writable.write(chunk);
    if (!ok) {
      await new Promise(resolve => writable.once('drain', resolve));
    }
  }
  writable.end();
  await new Promise((resolve, reject) => {
    writable.on('finish', resolve);
    writable.on('error', reject);
  });
}
```

---

## Chapter 7: File System

### 7.1 fs Module — Complete API

```javascript
const fs      = require('fs');
const fsp     = require('fs/promises'); // promise-based (Node 10+)
const path    = require('path');

// ── Synchronous vs Asynchronous ───────────────────────────────
// NEVER use sync versions in a server (blocks the event loop!)
// OK to use sync versions in: startup scripts, CLI tools, build scripts

// ❌ Never in server code:
const data = fs.readFileSync('/etc/hosts', 'utf8'); // BLOCKS event loop

// ✅ In server code:
const data = await fsp.readFile('/etc/hosts', 'utf8'); // non-blocking

// ── Reading files ─────────────────────────────────────────────
// Entire file into memory (fine for small files)
const text    = await fsp.readFile('data.txt', 'utf8');
const buffer  = await fsp.readFile('image.png');        // Buffer (no encoding)

// Stream large files (don't load into memory)
const stream  = fs.createReadStream('large.txt', {
  encoding:       'utf8',
  highWaterMark:  64 * 1024,  // 64KB chunks
  start:          0,           // byte offset start
  end:            1000,        // byte offset end (inclusive)
});

// ── Writing files ─────────────────────────────────────────────
await fsp.writeFile('output.txt', 'content', 'utf8');  // creates or overwrites
await fsp.writeFile('output.bin', buffer);              // Buffer
await fsp.appendFile('log.txt', 'new line\n');         // append
await fsp.writeFile('file.txt', data, {
  encoding: 'utf8',
  flag:     'w',    // 'w'=create/overwrite, 'a'=append, 'wx'=create (fail if exists)
  mode:     0o644,  // file permissions
});

// ── File metadata ─────────────────────────────────────────────
const stat = await fsp.stat('file.txt');
stat.size;         // bytes
stat.mtime;        // Date — last modified
stat.birthtime;    // Date — created (not on all systems)
stat.mode;         // permissions (use fs.constants to interpret)
stat.isFile();     // true
stat.isDirectory(); // false
stat.isSymbolicLink(); // false (always false with stat; use lstat instead)

const lstat = await fsp.lstat('link.txt');  // stat without following symlinks
lstat.isSymbolicLink(); // true if it's a symlink

await fsp.access('file.txt', fs.constants.R_OK | fs.constants.W_OK); // throws if no permission

// ── Directory operations ──────────────────────────────────────
await fsp.mkdir('new-dir');
await fsp.mkdir('a/b/c', { recursive: true });  // create parents

const entries = await fsp.readdir('.');
const detailed = await fsp.readdir('.', { withFileTypes: true });
// detailed = [Dirent { name: 'file.txt', ... }]
// dirent.isFile(), dirent.isDirectory(), dirent.name

await fsp.rmdir('empty-dir');
await fsp.rm('dir-or-file', { recursive: true, force: true }); // rm -rf (Node 14.14+)

// ── File operations ───────────────────────────────────────────
await fsp.rename('old.txt', 'new.txt');   // rename or move (same filesystem)
await fsp.copyFile('src.txt', 'dst.txt');
await fsp.copyFile('src', 'dst', fs.constants.COPYFILE_EXCL); // fail if dst exists
await fsp.unlink('file.txt');             // delete file

// ── Symbolic links ────────────────────────────────────────────
await fsp.symlink('target', 'link-name');
await fsp.readlink('link-name');          // returns 'target'

// ── File descriptors — low-level ─────────────────────────────
const fd = await fsp.open('file.txt', 'r+'); // file descriptor
await fsp.read(fd, buffer, 0, buffer.length, null);   // read
await fsp.write(fd, data, 0, data.length, null);       // write
await fsp.fsync(fd);                                   // flush to disk
await fd.close();                                      // close (FileHandle object in v10+)

// ── Watching for changes ──────────────────────────────────────
const watcher = fs.watch('src/', { recursive: true }, (eventType, filename) => {
  console.log(`${eventType}: ${filename}`);  // 'change' or 'rename'
});
// watcher.close() to stop watching

// Better: use chokidar (npm) for cross-platform reliable watching
const chokidar = require('chokidar');
const watcher2 = chokidar.watch('src/', {
  ignored:    /(^|[\/\\])\../,  // ignore dotfiles
  persistent: true,
  awaitWriteFinish: { stabilityThreshold: 200 },
});
watcher2
  .on('add',    path => console.log(`Added: ${path}`))
  .on('change', path => console.log(`Changed: ${path}`))
  .on('unlink', path => console.log(`Deleted: ${path}`))
  .on('error',  err  => console.error('Watch error:', err));
```

### 7.2 Walking Directories Recursively

```javascript
const { readdir, stat } = require('fs/promises');
const path = require('path');

// Recursive directory walk
async function* walk(dir, options = {}) {
  const { filter, maxDepth = Infinity } = options;

  async function* walkDir(currentDir, depth) {
    if (depth > maxDepth) return;

    const entries = await readdir(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory()) {
        yield* walkDir(fullPath, depth + 1); // recurse
      } else if (entry.isFile()) {
        if (!filter || filter(entry.name, fullPath)) {
          yield fullPath;
        }
      }
    }
  }

  yield* walkDir(dir, 0);
}

// Usage
for await (const file of walk('./src', { filter: (name) => name.endsWith('.js') })) {
  console.log(file);
}

// Collect all TypeScript files
const tsFiles = [];
for await (const file of walk('./src', { filter: (n) => n.endsWith('.ts') })) {
  tsFiles.push(file);
}

// Or use fs.glob (Node 22+) or fast-glob npm package
const fg = require('fast-glob');
const files = await fg(['src/**/*.ts', '!src/**/*.spec.ts']);
```

---

## Chapter 8: Networking

### 8.1 http Module — HTTP Server from Scratch

```javascript
const http  = require('http');
const https = require('https');
const fs    = require('fs');
const url   = require('url');

// ── Basic HTTP server ─────────────────────────────────────────
const server = http.createServer((req, res) => {
  // req: http.IncomingMessage (Readable stream)
  // res: http.ServerResponse  (Writable stream)

  // Request info
  console.log(req.method);    // 'GET', 'POST', etc.
  console.log(req.url);       // '/path?query=string'
  console.log(req.headers);   // { 'content-type': '...', 'authorization': '...' }
  console.log(req.httpVersion); // '1.1'

  // Parse URL
  const parsed  = url.parse(req.url, true);
  const pathname = parsed.pathname;  // '/path'
  const query    = parsed.query;     // { key: 'value' }

  // Read request body (req is a Readable stream)
  let body = '';
  req.on('data',  (chunk) => { body += chunk.toString(); });
  req.on('end',   () => {
    const data = body ? JSON.parse(body) : null;

    // Write response
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('X-Request-Id', crypto.randomUUID());
    res.end(JSON.stringify({ received: data, url: pathname }));
  });
  req.on('error', (err) => {
    res.statusCode = 400;
    res.end('Bad request');
  });
});

// Body reading helper
function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data',  (chunk) => chunks.push(chunk));
    req.on('end',   () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
    req.on('aborted', () => reject(new Error('Request aborted')));
  });
}

// ── Server configuration ──────────────────────────────────────
server.listen(3000, '0.0.0.0', () => {
  console.log('Server running on http://0.0.0.0:3000');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error('Port 3000 already in use');
    process.exit(1);
  }
});

server.timeout      = 30000;     // 30 second request timeout
server.keepAliveTimeout = 65000; // 65s — must be > nginx's 60s keepalive

// Graceful shutdown
process.on('SIGTERM', () => {
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
  // Force close after 30s if requests don't finish
  setTimeout(() => process.exit(1), 30000);
});

// ── HTTPS server ──────────────────────────────────────────────
const httpsServer = https.createServer({
  cert: fs.readFileSync('server.crt'),
  key:  fs.readFileSync('server.key'),
}, requestHandler);
httpsServer.listen(443);

// ── HTTP/2 server ─────────────────────────────────────────────
const http2 = require('http2');
const h2server = http2.createSecureServer({
  cert: fs.readFileSync('server.crt'),
  key:  fs.readFileSync('server.key'),
}, (req, res) => {
  res.setHeader('content-type', 'application/json');
  res.end(JSON.stringify({ protocol: 'HTTP/2' }));
});
```

### 8.2 HTTP Client (http.request)

```javascript
const http  = require('http');
const https = require('https');

// ── Making HTTP requests ──────────────────────────────────────
function httpRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const lib = options.protocol === 'https:' ? https : http;

    const req = lib.request(options, (res) => {
      const chunks = [];
      res.on('data',  (chunk) => chunks.push(chunk));
      res.on('end',   () => {
        const body = Buffer.concat(chunks).toString();
        if (res.statusCode >= 400) {
          reject(Object.assign(new Error(`HTTP ${res.statusCode}`), {
            statusCode: res.statusCode,
            body,
            headers: res.headers,
          }));
        } else {
          resolve({ statusCode: res.statusCode, headers: res.headers, body });
        }
      });
      res.on('error', reject);
    });

    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy(new Error('Request timed out'));
    });

    if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

// JSON GET request
const { body } = await httpRequest({
  hostname: 'api.example.com',
  port:     443,
  path:     '/users?limit=10',
  method:   'GET',
  protocol: 'https:',
  headers:  { 'Authorization': 'Bearer token', 'Accept': 'application/json' },
});
const users = JSON.parse(body);

// In practice: use fetch (Node 18+) or node-fetch/axios/got
const response = await fetch('https://api.example.com/users');
const data = await response.json();

// fetch with options
const result = await fetch('https://api.example.com/users', {
  method:  'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
  body:    JSON.stringify({ name: 'Alice' }),
  signal:  AbortSignal.timeout(10000),  // 10 second timeout
});

if (!result.ok) throw new Error(`HTTP ${result.status}: ${await result.text()}`);
const created = await result.json();
```

### 8.3 net Module — Raw TCP

```javascript
const net = require('net');

// ── TCP Server ────────────────────────────────────────────────
const tcpServer = net.createServer((socket) => {
  // socket: net.Socket — Duplex stream
  console.log(`Client connected: ${socket.remoteAddress}:${socket.remotePort}`);

  socket.setEncoding('utf8');
  socket.setTimeout(30000); // 30s idle timeout

  socket.on('data', (data) => {
    console.log('Received:', data);
    socket.write(`Echo: ${data}`); // write back
  });

  socket.on('end', () => {
    console.log('Client disconnected (half-close)');
    socket.end(); // complete the half-close
  });

  socket.on('close', (hadError) => {
    console.log('Socket fully closed', { hadError });
  });

  socket.on('error', (err) => {
    console.error('Socket error:', err.code);
  });

  socket.on('timeout', () => {
    console.log('Socket timeout — destroying');
    socket.destroy();
  });
});

tcpServer.listen(9000, '0.0.0.0', () => console.log('TCP server on port 9000'));

// ── TCP Client ────────────────────────────────────────────────
const client = net.createConnection({ host: 'localhost', port: 9000 }, () => {
  client.write('Hello, server!');
});

client.on('data', (data) => {
  console.log('Server says:', data.toString());
  client.end();
});
```

---

## Chapter 9: Child Processes & Worker Threads

### 9.1 child_process Module

```javascript
const {
  exec, execSync,
  execFile, execFileSync,
  spawn, spawnSync,
  fork
} = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// ── exec — run shell command, buffer output ────────────────────
// ⚠️ Shell injection risk with user input! Use execFile or spawn instead.
exec('ls -la /tmp', { maxBuffer: 1024 * 1024 }, (err, stdout, stderr) => {
  if (err) { console.error(err); return; }
  console.log(stdout);
  if (stderr) console.error(stderr);
});

// Promisified (better)
try {
  const { stdout, stderr } = await execAsync('git log --oneline -5');
  console.log(stdout);
} catch (err) {
  console.error('exit code:', err.code);
  console.error('stderr:', err.stderr);
}

// ── execFile — run file without shell (safer than exec) ───────
execFile('/usr/bin/find', ['/tmp', '-name', '*.log'], (err, stdout) => {
  console.log(stdout);
});

// ── spawn — stream output (for long-running or large output) ──
const child = spawn('node', ['worker.js'], {
  env:   { ...process.env, WORKER_ID: '1' },
  cwd:   '/app',
  stdio: ['pipe', 'pipe', 'pipe'],  // stdin, stdout, stderr
  // stdio: 'inherit'  — share parent's stdio (output goes to parent's console)
  // stdio: ['pipe', 'inherit', 'inherit']  — pipe stdin, inherit stdout/stderr
});

child.stdout.on('data', (chunk) => process.stdout.write(chunk));
child.stderr.on('data', (chunk) => process.stderr.write(chunk));
child.stdin.write('some input\n');
child.stdin.end();

child.on('close', (code, signal) => {
  console.log(`Process exited: code=${code}, signal=${signal}`);
});
child.on('error', (err) => console.error('Failed to start process:', err));

// Kill child process
child.kill('SIGTERM');
child.kill('SIGKILL');  // force kill (cannot be caught)

// ── fork — spawn another Node.js process with IPC channel ──────
// IPC = Inter-Process Communication via process.send() / process.on('message')
const worker = fork('./worker.js', [], {
  env: process.env,
  silent: false,  // true = pipe stdio; false = inherit
});

// Send message to child
worker.send({ type: 'compute', data: [1, 2, 3, 4, 5] });

// Receive message from child
worker.on('message', (msg) => {
  console.log('Child result:', msg.result);
});

worker.on('exit', (code) => {
  console.log(`Worker exited with code ${code}`);
});

// In worker.js:
process.on('message', async (msg) => {
  const result = await heavyComputation(msg.data);
  process.send({ result });
});
```

### 9.2 Worker Threads — True CPU Parallelism

```javascript
const { Worker, isMainThread, parentPort, workerData, threadId } = require('worker_threads');

// ── worker_threads vs child_process ──────────────────────────
// child_process (fork): separate Node.js process, separate heap, IPC with serialization
//   Use for: completely independent tasks, running different scripts, isolation
// worker_threads: thread in same process, SHARED memory possible, faster IPC
//   Use for: CPU-intensive work with shared data, matrix operations, image processing

// ── Main thread ───────────────────────────────────────────────
if (isMainThread) {
  // Create shared memory buffer (SharedArrayBuffer)
  const sharedBuffer = new SharedArrayBuffer(4);
  const sharedArray  = new Int32Array(sharedBuffer);
  sharedArray[0]     = 0;  // counter

  // Create worker
  const worker = new Worker(__filename, {
    workerData: {
      sharedBuffer,
      iterations: 1_000_000,
    }
  });

  worker.on('message', (msg) => {
    console.log('Worker message:', msg);
    console.log('Shared counter:', sharedArray[0]);
  });

  worker.on('error',  (err)  => console.error('Worker error:', err));
  worker.on('exit',   (code) => console.log(`Worker exited: ${code}`));

  // Post message with transferable (zero-copy)
  const buffer = new ArrayBuffer(1024 * 1024);
  worker.postMessage({ type: 'process', buffer }, [buffer]); // transferred, not copied
  // buffer is now detached (unusable in main thread)

} else {
  // ── Worker thread ─────────────────────────────────────────
  const { sharedBuffer, iterations } = workerData;
  const sharedArray = new Int32Array(sharedBuffer);

  // CPU-intensive work — doesn't block main thread's event loop
  let result = 0;
  for (let i = 0; i < iterations; i++) {
    result += Math.sqrt(i);
    // Atomic operations for shared memory (thread-safe)
    Atomics.add(sharedArray, 0, 1);
  }

  // Listen for messages from main thread
  parentPort.on('message', ({ type, buffer }) => {
    if (type === 'process') {
      const view = new Uint8Array(buffer);
      // process buffer...
      parentPort.postMessage({ processed: view.length });
    }
  });

  parentPort.postMessage({ threadId, result });
}

// ── Worker Pool Pattern ───────────────────────────────────────
class WorkerPool {
  #workers = [];
  #queue   = [];
  #idleWorkers = [];

  constructor(workerFile, size = require('os').cpus().length) {
    for (let i = 0; i < size; i++) {
      const worker = new Worker(workerFile);
      worker.on('message', (result) => {
        const { resolve } = this.#queue.shift();
        resolve(result);
        this.#idleWorkers.push(worker);
        this.#processQueue();
      });
      worker.on('error', (err) => {
        const { reject } = this.#queue.shift();
        reject(err);
        this.#idleWorkers.push(worker);
        this.#processQueue();
      });
      this.#idleWorkers.push(worker);
    }
  }

  run(data) {
    return new Promise((resolve, reject) => {
      this.#queue.push({ resolve, reject, data });
      this.#processQueue();
    });
  }

  #processQueue() {
    while (this.#queue.length > 0 && this.#idleWorkers.length > 0) {
      const worker = this.#idleWorkers.pop();
      const { data } = this.#queue[0];
      worker.postMessage(data);
    }
  }

  async destroy() {
    await Promise.all(this.#workers.map(w => w.terminate()));
  }
}

const pool = new WorkerPool('./compute-worker.js', 4);
const results = await Promise.all(
  largeDatasets.map(data => pool.run(data))
);
```

---

## Chapter 10: Timers, Scheduling & the Event Loop Phases

### 10.1 Timer Functions

```javascript
// ── setTimeout — schedule after minimum delay ─────────────────
const timerId = setTimeout(() => {
  console.log('At least 100ms have passed');
}, 100);

clearTimeout(timerId); // cancel before it fires

// Common pattern: timeout around async operation
async function withTimeout(promise, ms) {
  let timer;
  const timeoutPromise = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms);
  });
  try {
    return await Promise.race([promise, timeoutPromise]);
  } finally {
    clearTimeout(timer);
  }
}

// ── setInterval — repeat at interval ─────────────────────────
const intervalId = setInterval(() => {
  checkDatabaseHealth();
}, 30_000);  // every 30 seconds

clearInterval(intervalId);

// Better: use recursive setTimeout (prevents overlap if work takes longer than interval)
function scheduleWork() {
  setTimeout(async () => {
    try {
      await doWork();
    } catch (err) {
      console.error(err);
    } finally {
      scheduleWork(); // always reschedule, even on error
    }
  }, 30_000);
}
scheduleWork();

// ── setImmediate — run after I/O callbacks in this iteration ──
setImmediate(() => {
  console.log('After I/O in this event loop iteration');
});
clearImmediate(/* handle */);

// ── process.nextTick — run before NEXT phase (highest priority) ─
process.nextTick(() => {
  console.log('Before any I/O event or timer');
});
// ⚠️ nextTick callbacks run BETWEEN every event loop phase transition
// Overusing nextTick starves I/O → use sparingly

// ── queueMicrotask — Promise microtask queue ──────────────────
queueMicrotask(() => {
  console.log('Promise microtask queue');
});
// Same queue as Promise.then() — runs after nextTick, before timers

// ── Practical scheduling examples ─────────────────────────────

// Health check every 30s, starting 30s from now
const healthCheck = setInterval(async () => {
  try {
    const ok = await db.ping();
    metrics.record('db.health', ok ? 1 : 0);
  } catch (err) {
    metrics.record('db.health', 0);
    logger.error('Database health check failed', { error: err.message });
  }
}, 30_000);
// Don't forget to clearInterval(healthCheck) on shutdown!

// Debounce — only fire after activity stops for N ms
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// Throttle — fire at most once per N ms
function throttle(fn, limit) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      return fn(...args);
    }
  };
}
```

---

## Chapter 11: Buffers, TypedArrays & Binary Data

### 11.1 Buffer — Node.js Binary Data

```javascript
// Buffer: fixed-size chunk of memory (raw binary data)
// Subclass of Uint8Array — each element is a byte (0-255)

// ── Creating Buffers ──────────────────────────────────────────
// NEVER use new Buffer() — deprecated, security risk (uninitialized memory)

Buffer.alloc(10)           // 10 zeros — SAFE (zero-filled)
Buffer.alloc(10, 0xff)    // 10 bytes, all 0xFF
Buffer.allocUnsafe(10)    // 10 bytes, NOT zero-filled (faster; dangerous with sensitive data)
Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]) // from byte array → 'Hello'
Buffer.from('Hello', 'utf8')    // from string
Buffer.from('SGVsbG8=', 'base64') // from base64
Buffer.from('48656c6c6f', 'hex') // from hex string
Buffer.concat([buf1, buf2, buf3]) // concatenate

// ── Encoding/decoding ─────────────────────────────────────────
const buf = Buffer.from('Hello, World!', 'utf8');
buf.toString('utf8')   // 'Hello, World!'
buf.toString('base64') // 'SGVsbG8sIFdvcmxkIQ=='
buf.toString('hex')    // '48656c6c6f2c20576f726c6421'
buf.length             // 13 (bytes)
buf.byteLength         // 13 (same as .length for Buffer)

// ── Reading/writing values ────────────────────────────────────
const data = Buffer.alloc(8);
data.writeUInt32BE(0x12345678, 0); // write uint32 big-endian at offset 0
data.writeUInt32LE(0xdeadbeef, 4); // write uint32 little-endian at offset 4
data.readUInt32BE(0);  // 0x12345678
data.readUInt32LE(4);  // 0xdeadbeef
data.readInt16BE(0);   // signed int16 at offset 0
data.readFloatLE(0);   // 32-bit float little-endian
data.readDoubleBE(0);  // 64-bit double big-endian

// ── Buffer operations ─────────────────────────────────────────
buf.slice(0, 5)           // Buffer view of bytes 0-4 (shares memory!)
buf.subarray(7, 13)       // alias for slice (preferred in modern code)
buf.copy(target, targetStart, sourceStart, sourceEnd)
Buffer.compare(buf1, buf2) // -1, 0, 1
buf.equals(buf2)          // true if same bytes
buf.indexOf('World')      // 7
buf.includes('Hello')     // true
buf.fill(0)               // zero out entire buffer
buf.fill(0xff, 2, 6)     // fill bytes 2-5 with 0xFF

// ── Buffer and TypedArrays ────────────────────────────────────
// Buffer is a Uint8Array with extra methods
const uint8 = new Uint8Array([1, 2, 3]);
const buf2  = Buffer.from(uint8.buffer); // share ArrayBuffer (zero-copy)
// Changes to buf2 affect uint8 and vice versa!

// Independent copy:
const buf3 = Buffer.from(uint8); // copy — no shared memory

// ArrayBuffer → Buffer
const ab  = new ArrayBuffer(16);
const buf4 = Buffer.from(ab, 4, 8); // view of ab at offset 4, length 8
```

---

## Chapter 12: Error Handling Patterns

### 12.1 The Node.js Error Model

```javascript
// Node.js errors fall into four categories:
// 1. Synchronous exceptions (throw) — caught by try/catch
// 2. Async errors in callbacks — passed as first argument
// 3. Promise rejections — caught with .catch() or try/catch in async
// 4. 'error' events on EventEmitters — uncaught crashes the process

// ── Callback-style error handling (legacy) ────────────────────
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) {
    if (err.code === 'ENOENT') return console.error('File not found');
    if (err.code === 'EACCES') return console.error('Permission denied');
    throw err; // unexpected error — rethrow
  }
  process(data);
});

// ── Promise / async-await (modern) ───────────────────────────
async function readConfig(path) {
  try {
    const data = await fs.promises.readFile(path, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') return {}; // file not found → return defaults
    if (err instanceof SyntaxError) throw new Error(`Invalid JSON in ${path}: ${err.message}`);
    throw err; // re-throw unexpected errors
  }
}

// ── Custom error classes ──────────────────────────────────────
class AppError extends Error {
  constructor(message, code, statusCode = 500, details = {}) {
    super(message);
    this.name       = this.constructor.name;
    this.code       = code;
    this.statusCode = statusCode;
    this.details    = details;
    this.isOperational = true; // vs programming errors
    Error.captureStackTrace(this, this.constructor); // clean stack trace
  }
}

class ValidationError extends AppError {
  constructor(message, fields = {}) {
    super(message, 'VALIDATION_ERROR', 400, { fields });
    this.fields = fields;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} ${id} not found`, 'NOT_FOUND', 404, { resource, id });
    this.resource = resource;
    this.id = id;
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

class ConflictError extends AppError {
  constructor(message) {
    super(message, 'CONFLICT', 409);
  }
}

// ── Error identification ──────────────────────────────────────
function isNodeError(err, code) {
  return err instanceof Error && err.code === code;
}

// Common Node.js system error codes:
// ENOENT   — No such file or directory
// EACCES   — Permission denied
// EADDRINUSE — Address already in use (port taken)
// ECONNREFUSED — Connection refused (service down)
// ETIMEDOUT — Connection timed out
// ENOTFOUND — DNS lookup failed
// EPIPE    — Broken pipe (other end closed)
// EMFILE   — Too many open files

// ── Result pattern (avoid throw for expected failures) ────────
class Result {
  #ok;
  #value;
  #error;

  static ok(value)   { const r = new Result(); r.#ok = true;  r.#value = value; return r; }
  static err(error)  { const r = new Result(); r.#ok = false; r.#error = error; return r; }

  get isOk()    { return this.#ok; }
  get isErr()   { return !this.#ok; }
  get value()   { if (!this.#ok) throw new Error('Result is an error'); return this.#value; }
  get error()   { if (this.#ok)  throw new Error('Result is ok');       return this.#error; }
  unwrap()      { return this.value; }
  unwrapOr(def) { return this.#ok ? this.#value : def; }

  map(fn)       { return this.#ok ? Result.ok(fn(this.#value)) : this; }
  flatMap(fn)   { return this.#ok ? fn(this.#value) : this; }
}

async function findUser(id) {
  const user = await db.users.findById(id);
  if (!user) return Result.err(new NotFoundError('User', id));
  return Result.ok(user);
}

const result = await findUser(42);
if (result.isErr) {
  const err = result.error;
  logger.warn('User not found', { id: 42 });
  return res.status(404).json({ error: err.message });
}
const user = result.value;
```

---

## Chapter 13: Cluster & Load Balancing

### 13.1 The cluster Module

```javascript
const cluster = require('cluster');
const os      = require('os');
const http    = require('http');

// Node.js is single-threaded, but modern servers have multiple CPU cores.
// cluster creates multiple child processes that all share the same port.
// The OS kernel distributes incoming connections across them (round-robin on Linux).

if (cluster.isPrimary) {
  // ── Primary process ─────────────────────────────────────────
  const numCPUs = os.cpus().length;
  console.log(`Primary ${process.pid} starting ${numCPUs} workers`);

  // Fork one worker per CPU core
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Restart workers that crash
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died (code=${code}, signal=${signal})`);
    if (!worker.exitedAfterDisconnect) {
      console.log('Restarting worker...');
      cluster.fork();
    }
  });

  cluster.on('online', (worker) => {
    console.log(`Worker ${worker.process.pid} online`);
  });

  // Zero-downtime restart (rolling restart)
  process.on('SIGUSR2', async () => {
    const workers = Object.values(cluster.workers);
    for (const worker of workers) {
      await new Promise((resolve) => {
        worker.on('exit', resolve);
        worker.send('graceful-shutdown');
        setTimeout(() => worker.kill(), 30000); // force after 30s
      });
      cluster.fork();
      await new Promise(resolve => cluster.once('online', resolve));
    }
  });

  // IPC: send messages to all workers
  function broadcast(message) {
    Object.values(cluster.workers).forEach(worker => worker.send(message));
  }

  broadcast({ type: 'config-update', config: newConfig });

} else {
  // ── Worker process ──────────────────────────────────────────
  const server = http.createServer(requestHandler);
  server.listen(3000, () => {
    console.log(`Worker ${process.pid} listening`);
  });

  process.on('message', (msg) => {
    if (msg === 'graceful-shutdown') {
      server.close(() => {
        process.exit(0);
      });
    }
    if (msg.type === 'config-update') {
      reloadConfig(msg.config);
    }
  });
}
```

---

## Chapter 14: Debugging & Profiling

### 14.1 Built-in Debugger

```bash
# Node.js built-in inspector
node --inspect server.js              # start with inspector on default port 9229
node --inspect=0.0.0.0:9229 server.js # specify host:port
node --inspect-brk server.js         # pause at first line (for startup issues)

# Connect: Chrome → chrome://inspect → Remote Target → inspect

# V8 profiler (CPU profiling)
node --prof server.js                 # creates isolate-*.log file
node --prof-process isolate-*.log    # process the log (human-readable)

# Heap snapshots
node --heapdump server.js            # take heap snapshot on SIGUSR2

# Memory limits
node --max-old-space-size=4096 server.js  # 4GB heap
```

```javascript
// ── Programmatic debugging ────────────────────────────────────
const inspector = require('inspector');
const session   = new inspector.Session();
session.connect();

// CPU profiling from code
session.post('Profiler.enable');
session.post('Profiler.start');
// ... run code to profile ...
session.post('Profiler.stop', (err, { profile }) => {
  require('fs').writeFileSync('profile.cpuprofile', JSON.stringify(profile));
  // Open in Chrome DevTools → Performance tab
});

// Heap snapshot
session.post('HeapProfiler.enable');
session.post('HeapProfiler.takeHeapSnapshot', null, (err, { profile }) => {
  require('fs').writeFileSync('snapshot.heapsnapshot', JSON.stringify(profile));
  // Open in Chrome DevTools → Memory tab
});

// ── console methods ───────────────────────────────────────────
console.log('Message');
console.error('Error (to stderr)');
console.warn('Warning (to stderr)');
console.info('Info (same as log)');
console.debug('Debug (same as log)');

// Timing
console.time('operation');
await expensiveOperation();
console.timeEnd('operation');   // 'operation: 1234.5ms'
console.timeLog('operation', 'checkpoint'); // 'operation: 456ms checkpoint'

// Counting
console.count('requests');   // 'requests: 1'
console.count('requests');   // 'requests: 2'
console.countReset('requests');

// Table formatting
console.table([
  { name: 'Alice', age: 30 },
  { name: 'Bob',   age: 25 },
]);

// Grouping
console.group('Database');
console.log('Connected');
console.groupEnd();

// Assertion
console.assert(1 === 1, 'This will not print');
console.assert(1 === 2, 'This WILL print as an error');

// Stack trace
console.trace('Execution reached here');

// ── Performance measurement ───────────────────────────────────
const { performance, PerformanceObserver } = require('perf_hooks');

// mark + measure
performance.mark('start');
await doWork();
performance.mark('end');
performance.measure('doWork', 'start', 'end');
const entries = performance.getEntriesByName('doWork');
console.log(`doWork took: ${entries[0].duration}ms`);

// High-resolution timer
const start = performance.now(); // ms with microsecond precision
doSyncWork();
console.log(`${performance.now() - start}ms`);

// Observe all measurements
const obs = new PerformanceObserver((items) => {
  items.getEntries().forEach(entry => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});
obs.observe({ entryTypes: ['measure', 'function'] });
```

---

# PART II — EXPRESS.JS COMPLETE

---

## Chapter 15: Express.js — Architecture & Philosophy

### 15.1 What Express Is and Is Not

```
Express.js is a MINIMAL web framework for Node.js. It adds:
  ① Router — maps HTTP method + path to handler functions
  ② Middleware — functions that run in sequence for every request
  ③ Request/Response helpers — convenience methods on req and res
  ④ Template engine integration — render HTML server-side

Express does NOT include:
  ❌ ORM / database driver (use pg, mongoose, drizzle separately)
  ❌ Authentication (use passport, jsonwebtoken separately)
  ❌ Input validation (use zod, joi, express-validator separately)
  ❌ File upload handling (use multer separately)
  ❌ Rate limiting (use express-rate-limit separately)
  ❌ Logging (use pino, morgan separately)

This minimalism is intentional — compose the pieces you need.
Compare: Koa (more modern, smaller core), Fastify (faster, schema-first),
         Hapi (more opinionated), NestJS (Angular-style, full framework).
```

### 15.2 Express Application Setup

```javascript
const express = require('express');
const path    = require('path');

// ── Create application ────────────────────────────────────────
const app = express();

// ── Application settings ──────────────────────────────────────
app.set('env', process.env.NODE_ENV || 'development');  // 'development' or 'production'
app.set('port', process.env.PORT || 3000);
app.set('trust proxy', 1);  // Trust first proxy (for req.ip behind nginx/load balancer)
                              // 'loopback', 'linklocal', 'uniquelocal', 1, true
app.set('x-powered-by', false); // Remove X-Powered-By: Express header (security)
app.set('strict routing', true);  // /Users ≠ /users (default: false)
app.set('case sensitive routing', true); // /Users ≠ /users (default: false)
app.set('etag', 'strong');   // ETag generation: false, 'weak', 'strong', function
app.set('query parser', 'extended'); // 'simple'=querystring, 'extended'=qs (default)
app.set('json spaces', 2);   // pretty-print JSON in development

// app.get(setting) to read settings
console.log(app.get('env'));  // 'development'

// ── Body parsers (middleware) ─────────────────────────────────
app.use(express.json({ limit: '10mb' }));                   // parse application/json
app.use(express.urlencoded({ extended: true, limit: '10mb' })); // parse form data
// extended: true  → use qs library (supports nested objects)
// extended: false → use querystring module (flat only)

// ── Starting the server ───────────────────────────────────────
const server = app.listen(app.get('port'), () => {
  console.log(`Express server running on port ${app.get('port')} in ${app.get('env')} mode`);
});

// With explicit binding
const server2 = app.listen(3000, '127.0.0.1', () => {
  console.log('Listening on 127.0.0.1:3000');
});

// Using http.createServer directly (required for HTTPS, HTTP/2, WebSockets)
const http = require('http');
const httpServer = http.createServer(app);
httpServer.listen(3000);

// Using https
const https = require('https');
const fs    = require('fs');
const httpsServer = https.createServer({
  cert: fs.readFileSync('cert.pem'),
  key:  fs.readFileSync('key.pem'),
}, app);
httpsServer.listen(443);

// app itself is a function(req, res, next) — can be used as a handler
// This makes it compatible with any Node.js http server
```

---

## Chapter 16: Routing — Complete Reference

### 16.1 Basic Routing

```javascript
// Route: app.METHOD(path, ...handlers)
// METHOD: get, post, put, patch, delete, head, options, all

// ── HTTP method routes ────────────────────────────────────────
app.get('/', (req, res) => {
  res.send('GET /');
});

app.post('/users', (req, res) => {
  const user = req.body;
  res.status(201).json({ created: user });
});

app.put('/users/:id', (req, res) => {
  res.json({ updated: req.params.id });
});

app.patch('/users/:id', (req, res) => {
  res.json({ patched: req.params.id });
});

app.delete('/users/:id', (req, res) => {
  res.sendStatus(204);
});

app.head('/users', (req, res) => {
  res.set('X-Total-Count', '42');
  res.end();
});

app.options('/users', (req, res) => {
  res.set('Allow', 'GET, POST, HEAD, OPTIONS');
  res.end();
});

// app.all — match ANY HTTP method
app.all('/secret', (req, res) => {
  res.send('All methods welcome here');
});

// ── Route parameters ──────────────────────────────────────────
// :param — required named parameter
app.get('/users/:userId/posts/:postId', (req, res) => {
  const { userId, postId } = req.params;
  // /users/42/posts/7 → { userId: '42', postId: '7' }
  res.json({ userId, postId });
});

// :param? — optional parameter (must be at end)
app.get('/users/:id?', (req, res) => {
  if (req.params.id) {
    res.json({ user: req.params.id });
  } else {
    res.json({ users: 'all' });
  }
});

// ── Route parameter validation with app.param ─────────────────
// Runs before any route handler where :userId appears
app.param('userId', async (req, res, next, id) => {
  if (!/^\d+$/.test(id)) {
    return res.status(400).json({ error: 'userId must be a number' });
  }
  try {
    req.user = await db.users.findById(Number(id));
    if (!req.user) return res.status(404).json({ error: 'User not found' });
    next();
  } catch (err) {
    next(err);
  }
});

// Now all routes with :userId automatically have req.user loaded
app.get('/users/:userId', (req, res) => {
  res.json(req.user); // already fetched by param handler
});
app.get('/users/:userId/posts', async (req, res) => {
  const posts = await db.posts.findByUserId(req.user.id);
  res.json(posts);
});

// ── Route patterns ────────────────────────────────────────────
app.get('/ab?cd', handler);    // /acd or /abcd (? = optional preceding char)
app.get('/ab+cd', handler);    // /abcd, /abbcd, /abbbcd (+ = one or more)
app.get('/ab*cd', handler);    // /abcd, /abXcd, /abANYTHINGcd (* = any chars)
app.get('/a(bc)?d', handler);  // /ad or /abcd (grouping)
app.get(/\/users\/\d+/, handler); // regex route

// ── Multiple handlers per route ───────────────────────────────
// Useful for composing middleware for specific routes
app.get('/admin',
  requireAuth,        // first: authenticate
  requireAdmin,       // second: authorize
  async (req, res) => { // third: handle
    res.json({ admin: true });
  }
);

// Array of handlers
const handlers = [requireAuth, requireAdmin, handleRequest];
app.get('/admin', handlers);

// next('route') — skip remaining handlers, try next matching route
app.get('/users/:id',
  (req, res, next) => {
    if (req.params.id === 'me') {
      return next('route'); // skip this route, go to next matching
    }
    next(); // continue to next handler in this route
  },
  (req, res) => res.json({ user: req.params.id })
);

app.get('/users/:id', (req, res) => {
  // This handles the 'me' case
  res.json({ currentUser: req.user });
});
```

### 16.2 Express Router — Modular Routing

```javascript
// router/users.js — a mini-application with own middleware stack
const express = require('express');
const router  = express.Router();

// Router-level middleware (applies only to routes in this router)
router.use(requireAuth);
router.use(rateLimiter({ windowMs: 60_000, max: 100 }));

// router.param — local to this router
router.param('userId', async (req, res, next, id) => {
  req.userParam = await loadUser(id);
  next();
});

// Routes
router.route('/') // chain multiple methods on same path
  .get(  async (req, res) => { res.json(await db.users.findAll()); })
  .post( async (req, res) => {
    const user = await db.users.create(req.body);
    res.status(201).json(user);
  });

router.route('/:userId')
  .get(    (req, res) => res.json(req.userParam))
  .put(    async (req, res) => { res.json(await db.users.update(req.params.userId, req.body)); })
  .delete( async (req, res) => { await db.users.delete(req.params.userId); res.sendStatus(204); });

// Nested router
const postsRouter = require('./posts');
router.use('/:userId/posts', postsRouter); // mount posts under users

module.exports = router;

// ─────────────────────────────────────────────────────────────
// router/posts.js
const postsRouter = express.Router({ mergeParams: true }); // mergeParams: inherit :userId
// Without mergeParams: :userId is undefined in postsRouter

postsRouter.get('/', async (req, res) => {
  // req.params.userId available because mergeParams: true
  const posts = await db.posts.findByUser(req.params.userId);
  res.json(posts);
});

module.exports = postsRouter;

// ─────────────────────────────────────────────────────────────
// app.js — mount routers
const usersRouter  = require('./router/users');
const authRouter   = require('./router/auth');
const healthRouter = require('./router/health');

app.use('/api/v1/users',  usersRouter);  // /api/v1/users, /api/v1/users/:id, etc.
app.use('/api/v1/auth',   authRouter);
app.use('/health',        healthRouter);

// Router options
const strictRouter = express.Router({
  strict:      true,  // /users/ ≠ /users
  caseSensitive: true, // /Users ≠ /users
  mergeParams:   false, // don't inherit parent params by default
});
```

### 16.3 Route Organization — Production Structure

```
src/
├── app.js               ← Express app (no server.listen — separated for testing)
├── server.js            ← Entry point (creates HTTP server, starts listening)
├── routes/
│   ├── index.js         ← Combines all routers, applies versioning
│   ├── users.routes.js  ← /users routes
│   ├── auth.routes.js   ← /auth routes
│   └── orders.routes.js ← /orders routes
├── controllers/
│   ├── users.controller.js   ← Request/response handling (thin)
│   └── auth.controller.js
├── services/
│   ├── users.service.js      ← Business logic
│   └── auth.service.js
├── middleware/
│   ├── auth.middleware.js
│   ├── validate.middleware.js
│   └── rate-limit.middleware.js
├── models/              ← Database models / schemas
├── repositories/        ← Database access layer
└── utils/
```

```javascript
// routes/index.js
const express = require('express');
const router  = express.Router();

const usersRouter  = require('./users.routes');
const authRouter   = require('./auth.routes');
const ordersRouter = require('./orders.routes');

// API versioning
router.use('/v1/users',  usersRouter);
router.use('/v1/auth',   authRouter);
router.use('/v1/orders', ordersRouter);

// Future version
// router.use('/v2/users', usersV2Router);

module.exports = router;

// app.js
const express = require('express');
const routes  = require('./routes');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/api', routes);

// 404 handler (no route matched)
app.use((req, res) => {
  res.status(404).json({ error: `Route ${req.method} ${req.path} not found` });
});

// Error handler (see Chapter 20)
app.use((err, req, res, next) => {
  res.status(err.statusCode || 500).json({ error: err.message });
});

module.exports = app;
```

---

## Chapter 17: Middleware — Deep Dive

### 17.1 What Middleware Is

```javascript
// Middleware is a function with signature: (req, res, next) => void
// 'next' is a function:
//   next()       → pass to next middleware/route
//   next(err)    → pass to error-handling middleware (4-arg)
//   next('route')→ skip remaining handlers in current route

// Middleware functions are executed in the ORDER they are registered with app.use()

// ── Application-level middleware ──────────────────────────────
app.use((req, res, next) => {
  // Runs for EVERY request, regardless of path or method
  req.requestId = require('crypto').randomUUID();
  req.startTime = Date.now();
  next(); // MUST call next() or send a response — otherwise request hangs!
});

// Path-specific middleware
app.use('/admin', requireAdmin); // only for /admin/*
app.use('/api',   apiRateLimiter);

// Method-specific middleware (uncommon)
app.get('/users', (req, res, next) => {
  if (!req.accepts('application/json')) {
    return res.status(406).json({ error: 'Only JSON accepted' });
  }
  next();
}, getUsersHandler);

// ── Router-level middleware ───────────────────────────────────
const router = express.Router();
router.use(requireAuth); // applies only to routes in this router

// ── Error-handling middleware — 4 parameters ──────────────────
// MUST have exactly 4 parameters for Express to recognize it as error handler
app.use((err, req, res, next) => {
  logger.error({ err, requestId: req.requestId });
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({ error: err.message });
});
```

### 17.2 Essential Middleware Implementations

```javascript
// ── Request logger ────────────────────────────────────────────
const morgan = require('morgan');

// Predefined formats: 'combined', 'common', 'dev', 'tiny', 'short'
app.use(morgan('dev'));         // development
app.use(morgan('combined'));   // Apache combined format (production)

// Custom format
app.use(morgan((tokens, req, res) => [
  tokens.method(req, res),
  tokens.url(req, res),
  tokens.status(req, res),
  tokens.res(req, res, 'content-length'),
  '-',
  tokens['response-time'](req, res), 'ms',
  req.requestId,
].join(' ')));

// Using pino for structured logging
const pinoHttp = require('pino-http');
app.use(pinoHttp({ logger: pino({ level: 'info' }) }));

// ── Security headers (helmet) ─────────────────────────────────
const helmet = require('helmet');
app.use(helmet());
// Adds: Content-Security-Policy, X-Content-Type-Options, X-Frame-Options,
//       X-XSS-Protection, Strict-Transport-Security, and more

// Fine-grained control
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc:   ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net'],
      scriptSrc:  ["'self'"],
      imgSrc:     ["'self'", 'data:', 'https:'],
    },
  },
  crossOriginEmbedderPolicy: false,  // may break some resources
}));

// ── CORS ──────────────────────────────────────────────────────
const cors = require('cors');

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-Id'],
  exposedHeaders: ['X-Total-Count', 'X-Request-Id'],
  credentials: true,        // Allow cookies to be sent
  maxAge: 86400,            // Pre-flight cache: 24 hours
}));

// Dynamic CORS
const allowedOrigins = new Set(process.env.ALLOWED_ORIGINS?.split(','));
app.use(cors({
  origin: (origin, callback) => {
    // Allow no origin (server-to-server) or whitelisted origins
    if (!origin || allowedOrigins.has(origin)) return callback(null, true);
    callback(new Error(`CORS: ${origin} not allowed`));
  },
  credentials: true,
}));

// ── Rate limiting ─────────────────────────────────────────────
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis').default;

// Global rate limit
app.use(rateLimit({
  windowMs:         15 * 60 * 1000, // 15 minutes
  max:              100,             // max requests per window
  standardHeaders:  true,   // Return RateLimit-* headers
  legacyHeaders:    false,
  message:          { error: 'Too many requests, please try again later' },
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:global:',
  }),
}));

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true, // only count failed requests
  message: { error: 'Too many authentication attempts' },
});
app.use('/api/auth/login', authLimiter);

// ── Compression ───────────────────────────────────────────────
const compression = require('compression');
app.use(compression({
  threshold: 1024,      // Only compress responses > 1KB
  level:     6,         // zlib compression level (1-9; 6 is default)
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false;
    return compression.filter(req, res); // default filter
  },
}));

// ── Request ID ────────────────────────────────────────────────
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] || require('crypto').randomUUID();
  res.setHeader('X-Request-Id', req.id);
  next();
});

// ── Slow request logging ──────────────────────────────────────
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const ms = Date.now() - start;
    if (ms > 1000) {
      logger.warn('Slow request', {
        method: req.method,
        path:   req.path,
        ms,
        statusCode: res.statusCode,
      });
    }
  });
  next();
});

// ── Request timeout ───────────────────────────────────────────
const timeout = require('connect-timeout');
app.use(timeout('30s'));
app.use((req, res, next) => {
  if (!req.timedout) next();
});
```

### 17.3 Authentication Middleware

```javascript
const jwt = require('jsonwebtoken');

// ── JWT authentication middleware ─────────────────────────────
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.slice(7);
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      audience:   'myapp',
      issuer:     'myapp-auth',
    });
    req.user = payload;   // attach to request for downstream handlers
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    if (err.name === 'JsonWebTokenError') {
      return res.status(401).json({ error: 'Invalid token', code: 'TOKEN_INVALID' });
    }
    next(err); // unexpected error
  }
}

// Optional auth — sets req.user if token valid, but doesn't require it
function optionalAuthenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) return next(); // no token — that's ok

  const token = authHeader.slice(7);
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
  } catch {
    // invalid token — just ignore it for optional auth
  }
  next();
}

// ── Role-based authorization ──────────────────────────────────
function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: `Required role: ${roles.join(' or ')}` });
    }
    next();
  };
}

// Usage
router.get('/admin/users',    authenticate, requireRole('admin'), listUsers);
router.delete('/admin/users', authenticate, requireRole('admin', 'superadmin'), deleteUser);

// ── API Key authentication ────────────────────────────────────
async function authenticateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey) return res.status(401).json({ error: 'API key required' });

  const hashedKey = crypto.createHash('sha256').update(apiKey).digest('hex');
  const client = await db.apiKeys.findOne({ hash: hashedKey, active: true });
  if (!client) return res.status(401).json({ error: 'Invalid API key' });

  req.apiClient = client;
  await db.apiKeys.updateOne({ hash: hashedKey }, { $set: { lastUsed: new Date() } });
  next();
}
```

### 17.4 Validation Middleware

```javascript
const { z } = require('zod');

// ── Zod validation middleware factory ─────────────────────────
function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse({
      body:   req.body,
      query:  req.query,
      params: req.params,
    });

    if (!result.success) {
      return res.status(400).json({
        error:   'Validation failed',
        details: result.error.flatten(),
      });
    }

    // Replace with validated/coerced values
    req.body   = result.data.body   ?? req.body;
    req.query  = result.data.query  ?? req.query;
    req.params = result.data.params ?? req.params;
    next();
  };
}

// Define schemas
const createUserSchema = z.object({
  body: z.object({
    name:  z.string().min(1).max(100).trim(),
    email: z.string().email().toLowerCase(),
    age:   z.number().int().min(18).max(120).optional(),
    role:  z.enum(['user', 'admin']).default('user'),
  }),
});

const getUserSchema = z.object({
  params: z.object({
    id: z.string().regex(/^\d+$/, 'Must be a number').transform(Number),
  }),
});

const listUsersSchema = z.object({
  query: z.object({
    page:   z.string().regex(/^\d+$/).transform(Number).default('1'),
    limit:  z.string().regex(/^\d+$/).transform(Number).pipe(z.number().max(100)).default('20'),
    search: z.string().max(100).optional(),
    sort:   z.enum(['name', 'email', 'createdAt']).default('createdAt'),
    order:  z.enum(['asc', 'desc']).default('desc'),
  }),
});

// Usage in routes
router.post('/', validate(createUserSchema), createUserController);
router.get('/:id', validate(getUserSchema),  getUserController);
router.get('/',    validate(listUsersSchema), listUsersController);

// ── express-validator alternative ────────────────────────────
const { body, param, query, validationResult } = require('express-validator');

function checkValidation(req, res, next) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  next();
}

const createUserValidation = [
  body('name').trim().notEmpty().withMessage('Name is required')
              .isLength({ max: 100 }),
  body('email').isEmail().normalizeEmail(),
  body('age').optional().isInt({ min: 18, max: 120 }),
  checkValidation,
];

router.post('/', ...createUserValidation, createUserHandler);
```

---

## Chapter 18: Request & Response Objects

### 18.1 The Request Object (req)

```javascript
// req: express.Request — extends http.IncomingMessage

// ── URL & routing ─────────────────────────────────────────────
req.method       // 'GET', 'POST', 'PUT', etc.
req.url          // '/users?sort=name' (from http.IncomingMessage — includes query)
req.path         // '/users'           (path only, no query string)
req.originalUrl  // '/api/v1/users?sort=name' (full path including mount point)
req.baseUrl      // '/api/v1'          (path of router mount point)
req.params       // { id: '42', userId: '7' } — URL parameters
req.query        // { sort: 'name', page: '2', tags: ['a','b'] } — query string
req.hostname     // 'api.example.com'  (from Host header, or X-Forwarded-Host if trusted)
req.ip           // '192.168.1.1'     (client IP, or X-Forwarded-For if trusted)
req.ips          // ['proxy2', 'proxy1', 'client'] — X-Forwarded-For chain
req.protocol     // 'https'           (http or https)
req.secure       // true if HTTPS
req.subdomains   // ['api', 'v1'] for api.v1.example.com
req.xhr          // true if X-Requested-With: XMLHttpRequest

// ── Headers ───────────────────────────────────────────────────
req.headers                    // object — all request headers (lowercase keys)
req.get('Content-Type')        // 'application/json; charset=utf-8'
req.get('Authorization')       // 'Bearer eyJhb...'
req.headers['x-request-id']   // header by lowercase name

// Content negotiation
req.accepts('json')            // 'json' or false
req.accepts(['json', 'html'])  // 'json' if preferred
req.acceptsCharsets('utf-8')   // 'utf-8' or false
req.acceptsEncodings('gzip')   // 'gzip' or false
req.acceptsLanguages('en')     // 'en' or false
req.is('application/json')     // true if Content-Type matches

// ── Body ──────────────────────────────────────────────────────
// Only populated after body-parsing middleware (express.json(), express.urlencoded())
req.body         // parsed request body (object for JSON, object for form data)

// ── Cookies ───────────────────────────────────────────────────
// Requires cookie-parser middleware: npm install cookie-parser
const cookieParser = require('cookie-parser');
app.use(cookieParser('cookie-secret')); // secret for signed cookies
req.cookies           // { name: 'value' } — unsigned cookies
req.signedCookies     // { sessionId: 'abc' } — signed (and verified) cookies

// ── Custom properties (attached by middleware) ─────────────────
req.user       // added by auth middleware
req.id         // added by request-id middleware
req.db         // database connection (if attached by middleware)
req.log        // pino-http logger instance
req.startTime  // timing middleware
```

### 18.2 The Response Object (res)

```javascript
// res: express.Response — extends http.ServerResponse

// ── Sending responses ─────────────────────────────────────────
res.send(body)       // send with smart Content-Type detection
                     // string → text/html, Buffer → bin, object → JSON

res.json(data)       // always JSON with Content-Type: application/json
                     // equivalent: res.send(JSON.stringify(data)) but sets header

res.jsonp(data)      // JSONP response

res.sendStatus(code) // set status code AND send default message as body
                     // res.sendStatus(204) → 204 No Content (empty body)
                     // res.sendStatus(404) → "Not Found"

// ── Status codes ─────────────────────────────────────────────
res.status(404).json({ error: 'Not found' });  // chain status() and json()
res.status(201).json({ created: user });
res.status(204).end();   // No Content — end() not send()!

// ── Headers ───────────────────────────────────────────────────
res.set('Content-Type', 'application/json');
res.set('X-Custom-Header', 'value');
res.set({ 'X-A': '1', 'X-B': '2' });   // set multiple
res.setHeader('X-Header', 'value');      // same as res.set (Node.js method)
res.append('Link', '<http://example.com>; rel="next"'); // append to existing
res.get('Content-Type');                 // read a header
res.removeHeader('X-Powered-By');

// Content-Type shortcuts
res.type('json');        // Content-Type: application/json
res.type('html');        // Content-Type: text/html
res.type('text');        // Content-Type: text/plain
res.type('png');         // Content-Type: image/png
res.type('application/pdf');  // or any MIME type

// ── Cookies ───────────────────────────────────────────────────
res.cookie('name', 'value', {
  maxAge:   7 * 24 * 60 * 60 * 1000,  // milliseconds (7 days)
  httpOnly: true,   // not accessible via JavaScript (XSS protection)
  secure:   true,   // HTTPS only (set this in production!)
  sameSite: 'strict', // 'strict', 'lax', 'none'
  domain:   '.example.com',
  path:     '/',
  signed:   true,   // requires cookie-parser with secret
});
res.clearCookie('name', { path: '/' }); // delete cookie

// ── Redirects ─────────────────────────────────────────────────
res.redirect('/new-path');           // 302 Found (temporary)
res.redirect(301, '/permanent');     // 301 Moved Permanently
res.redirect(307, '/temp');          // 307 Temporary Redirect (preserve method)
res.redirect('back');                // redirect to Referer header
res.redirect('https://external.com');

// ── File responses ────────────────────────────────────────────
res.sendFile(path.join(__dirname, 'public', 'index.html'), {
  root: '/',
  maxAge: '1d',
  dotfiles: 'deny',
}); // sends file with proper headers

res.download('/files/report.pdf', 'monthly-report.pdf', (err) => {
  if (err) console.error('Download error:', err);
});
// Sets Content-Disposition: attachment; filename="monthly-report.pdf"

// ── Streaming responses ───────────────────────────────────────
res.setHeader('Content-Type', 'text/plain');
res.setHeader('Transfer-Encoding', 'chunked');

// Stream a file
const fileStream = fs.createReadStream('large-file.txt');
fileStream.pipe(res);

// Server-Sent Events
res.setHeader('Content-Type', 'text/event-stream');
res.setHeader('Cache-Control', 'no-cache');
res.setHeader('Connection', 'keep-alive');

function sendSSE(data) {
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

const interval = setInterval(() => {
  sendSSE({ timestamp: Date.now(), value: Math.random() });
}, 1000);

req.on('close', () => {
  clearInterval(interval);
  res.end();
});

// ── res.locals — pass data through middleware chain ──────────
// Scoped to this request — NOT shared between requests
res.locals.user        = currentUser;
res.locals.flash       = getFlashMessages(req);
res.locals.csrfToken   = req.csrfToken();

// Accessible in templates: res.render() passes res.locals automatically
// Accessible in next middleware: next handler can read res.locals
```

---

## Chapter 19: Template Engines & Static Files

### 19.1 Serving Static Files

```javascript
// express.static — serve files from a directory
app.use(express.static('public', {
  index:      'index.html',       // directory index file
  dotfiles:   'ignore',           // 'allow', 'deny', 'ignore'
  etag:       true,               // ETag header for caching
  maxAge:     '1d',              // Cache-Control: max-age (parseable string or ms)
  lastModified: true,
  redirect:   true,               // redirect to trailing slash for directories
  setHeaders: (res, path, stat) => {
    if (path.endsWith('.html')) {
      res.setHeader('Cache-Control', 'no-cache'); // don't cache HTML
    }
    if (path.endsWith('.js') || path.endsWith('.css')) {
      res.setHeader('Cache-Control', 'max-age=31536000, immutable'); // 1 year for hashed assets
    }
  },
}));

// Multiple static directories
app.use(express.static('public'));
app.use(express.static('uploads'));
app.use('/static', express.static('assets')); // mount at path
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Conditional static serving (based on environment)
if (process.env.NODE_ENV === 'production') {
  app.use(express.static('dist')); // serve React build
  app.get('*', (req, res) => {    // SPA fallback
    res.sendFile(path.join(__dirname, 'dist', 'index.html'));
  });
}
```

### 19.2 Template Engines (EJS)

```javascript
// npm install ejs

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));  // directory of view files

// res.render(view, locals, callback)
app.get('/dashboard', authenticate, async (req, res, next) => {
  try {
    const [users, stats] = await Promise.all([
      db.users.findAll({ limit: 10 }),
      db.stats.getSummary(),
    ]);

    res.render('dashboard', {   // renders views/dashboard.ejs
      title:  'Dashboard',
      users,
      stats,
      user:   req.user,
      layout: 'layouts/main',   // with express-ejs-layouts
    });
  } catch (err) {
    next(err);
  }
});

// views/dashboard.ejs
```
```html
<!-- views/dashboard.ejs -->
<!DOCTYPE html>
<html lang="en">
<head>
  <title><%= title %> | My App</title>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Welcome, <%= user.name %></h1>
  
  <!-- Output escaped HTML (XSS safe): <%= expression %> -->
  <!-- Output UNESCAPED HTML (dangerous): <%- expression %> -->
  <!-- Code block (no output): <% code %> -->
  <!-- Comment: <%# this is a comment %> -->
  
  <ul>
  <% users.forEach(function(u) { %>
    <li>
      <%= u.name %> - 
      <a href="/users/<%= u.id %>"><%= u.email %></a>
    </li>
  <% }) %>
  </ul>
  
  <% if (stats.total > 0) { %>
    <p>Total: <%= stats.total %></p>
  <% } else { %>
    <p>No data yet</p>
  <% } %>
  
  <%- include('partials/footer') %>
</body>
</html>
```

---

## Chapter 20: Error Handling in Express

### 20.1 Synchronous and Async Error Handling

```javascript
// ── Synchronous errors — just throw ──────────────────────────
app.get('/sync-error', (req, res) => {
  throw new Error('Synchronous error'); // Express catches this automatically
});

// ── Async errors — MUST call next(err) ───────────────────────
// Express 4: does NOT catch async errors automatically!
app.get('/async-error', async (req, res, next) => {
  try {
    const result = await riskyOperation();
    res.json(result);
  } catch (err) {
    next(err); // MUST pass to next for Express to handle
  }
});

// ❌ Without try/catch in async route → unhandled rejection → crash!
app.get('/broken', async (req, res) => {
  const result = await mightFail(); // if this throws → process crashes (Node 15+)
  res.json(result);
});

// Solution 1: Async wrapper utility
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
    // fn(req, res, next) returns a Promise; if it rejects, call next(err)
  };
}

app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);
  res.json(user);
}));

// Solution 2: express-async-errors (monkey-patches Express to catch async errors)
require('express-async-errors');
// Now async route handlers automatically have their rejected promises caught

// Solution 3: Express 5 (async errors handled automatically)
// npm install express@5 (when available in stable)

// ── Error-handling middleware ─────────────────────────────────
// MUST have EXACTLY 4 parameters: (err, req, res, next)
// Express recognizes 4-arg middleware as error handler
// Register AFTER all routes and regular middleware

// 404 handler (no route matched) — MUST come after all routes
app.use((req, res, next) => {
  next(new NotFoundError(`Route ${req.method} ${req.path} not found`));
});

// Final error handler — MUST come last, MUST have 4 args
app.use((err, req, res, next) => {
  // Log the error
  logger.error({
    err:       err,
    requestId: req.id,
    userId:    req.user?.id,
    method:    req.method,
    path:      req.path,
    ip:        req.ip,
  });

  // Determine if this is an operational error (expected) or programming error
  const isOperational = err.isOperational === true;
  const statusCode    = err.statusCode || 500;

  // Response body varies by environment
  const body = {
    error:   err.message,
    code:    err.code || 'INTERNAL_ERROR',
    ...(process.env.NODE_ENV === 'development' && {
      stack:   err.stack,
      details: err.details,
    }),
  };

  // Add validation details for 400 errors
  if (statusCode === 400 && err.details) {
    body.details = err.details;
  }

  // Don't send error body for 204 (no content)
  if (statusCode === 204) {
    return res.sendStatus(204);
  }

  res.status(statusCode).json(body);

  // If not operational (programming error) — restart the process
  // ONLY if you have a process manager that will restart (PM2, Kubernetes)
  if (!isOperational) {
    // Give server time to send the response
    setImmediate(() => process.exit(1));
  }
});

// ── Multiple error handlers for different contexts ────────────
// Error handler for API routes (JSON)
app.use('/api', (err, req, res, next) => {
  if (res.headersSent) return next(err); // already responded
  res.status(err.statusCode || 500).json({ error: err.message });
});

// Error handler for web routes (HTML)
app.use((err, req, res, next) => {
  if (res.headersSent) return next(err);
  res.status(err.statusCode || 500).render('error', { err });
});
```

---

# PART III — PRODUCTION EXPRESS APPLICATIONS

---

## Chapter 21: Authentication & Authorization

### 21.1 JWT Authentication — Complete Implementation

```javascript
const jwt       = require('jsonwebtoken');
const bcrypt    = require('bcryptjs');
const crypto    = require('crypto');
const { z }     = require('zod');

// ── Token generation ──────────────────────────────────────────
const JWT_CONFIG = {
  accessSecret:  process.env.JWT_ACCESS_SECRET,
  refreshSecret: process.env.JWT_REFRESH_SECRET,
  accessExpiry:  '15m',   // short-lived (15 minutes)
  refreshExpiry: '7d',    // long-lived (7 days)
  issuer:        'myapp',
  audience:      'myapp-users',
};

function generateTokens(user) {
  const payload = {
    sub:   user.id,     // subject (user ID)
    email: user.email,
    role:  user.role,
    // Don't include sensitive data — tokens are base64, not encrypted!
  };

  const accessToken = jwt.sign(payload, JWT_CONFIG.accessSecret, {
    expiresIn: JWT_CONFIG.accessExpiry,
    issuer:    JWT_CONFIG.issuer,
    audience:  JWT_CONFIG.audience,
    algorithm: 'HS256',
    jwtid:     crypto.randomUUID(),  // unique ID for each token
  });

  const refreshToken = jwt.sign(
    { sub: user.id },              // minimal payload for refresh token
    JWT_CONFIG.refreshSecret,
    { expiresIn: JWT_CONFIG.refreshExpiry }
  );

  return { accessToken, refreshToken };
}

function verifyAccessToken(token) {
  return jwt.verify(token, JWT_CONFIG.accessSecret, {
    algorithms: ['HS256'],
    issuer:     JWT_CONFIG.issuer,
    audience:   JWT_CONFIG.audience,
  });
}

function verifyRefreshToken(token) {
  return jwt.verify(token, JWT_CONFIG.refreshSecret);
}

// ── Auth routes ───────────────────────────────────────────────
const authRouter = express.Router();

const loginSchema = z.object({
  body: z.object({
    email:    z.string().email(),
    password: z.string().min(1),
  }),
});

// POST /auth/register
authRouter.post('/register', validate(registerSchema), asyncHandler(async (req, res) => {
  const { name, email, password } = req.body;

  const existing = await db.users.findByEmail(email);
  if (existing) throw new ConflictError('Email already in use');

  const passwordHash = await bcrypt.hash(password, 12);
  const user = await db.users.create({ name, email, passwordHash, role: 'user' });

  const tokens = generateTokens(user);

  // Store refresh token (hashed) in DB
  const hashedRefresh = crypto.createHash('sha256').update(tokens.refreshToken).digest('hex');
  await db.refreshTokens.create({
    userId:    user.id,
    tokenHash: hashedRefresh,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  });

  // Send refresh token as httpOnly cookie
  res.cookie('refreshToken', tokens.refreshToken, {
    httpOnly: true,
    secure:   process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge:   7 * 24 * 60 * 60 * 1000, // 7 days in ms
  });

  res.status(201).json({
    accessToken: tokens.accessToken,
    user: { id: user.id, name: user.name, email: user.email, role: user.role },
  });
}));

// POST /auth/login
authRouter.post('/login', authLimiter, validate(loginSchema), asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  const user = await db.users.findByEmail(email);
  if (!user) throw new UnauthorizedError('Invalid credentials');

  const validPassword = await bcrypt.compare(password, user.passwordHash);
  if (!validPassword) throw new UnauthorizedError('Invalid credentials');

  if (!user.active) throw new UnauthorizedError('Account disabled');

  const tokens = generateTokens(user);
  await storeRefreshToken(user.id, tokens.refreshToken);

  res.cookie('refreshToken', tokens.refreshToken, { httpOnly: true, secure: true, sameSite: 'strict', maxAge: 7 * 24 * 60 * 60 * 1000 });
  res.json({ accessToken: tokens.accessToken, expiresIn: 900 }); // 900 = 15 min in seconds
}));

// POST /auth/refresh
authRouter.post('/refresh', asyncHandler(async (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  if (!refreshToken) throw new UnauthorizedError('No refresh token');

  let payload;
  try {
    payload = verifyRefreshToken(refreshToken);
  } catch {
    res.clearCookie('refreshToken');
    throw new UnauthorizedError('Invalid refresh token');
  }

  // Verify token is in DB and not revoked
  const hashedToken = crypto.createHash('sha256').update(refreshToken).digest('hex');
  const storedToken = await db.refreshTokens.findOne({ userId: payload.sub, tokenHash: hashedToken });
  if (!storedToken || storedToken.revoked || storedToken.expiresAt < new Date()) {
    res.clearCookie('refreshToken');
    throw new UnauthorizedError('Refresh token revoked or expired');
  }

  const user = await db.users.findById(payload.sub);
  if (!user || !user.active) throw new UnauthorizedError('User not found or inactive');

  // Rotate refresh token (invalidate old, issue new)
  await db.refreshTokens.revokeOne(storedToken.id);
  const newTokens = generateTokens(user);
  await storeRefreshToken(user.id, newTokens.refreshToken);

  res.cookie('refreshToken', newTokens.refreshToken, { httpOnly: true, secure: true, sameSite: 'strict', maxAge: 7 * 24 * 60 * 60 * 1000 });
  res.json({ accessToken: newTokens.accessToken, expiresIn: 900 });
}));

// POST /auth/logout
authRouter.post('/logout', authenticate, asyncHandler(async (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  if (refreshToken) {
    const hashedToken = crypto.createHash('sha256').update(refreshToken).digest('hex');
    await db.refreshTokens.revokeByHash(hashedToken);
  }
  res.clearCookie('refreshToken');
  res.sendStatus(204);
}));

// POST /auth/logout-all
authRouter.post('/logout-all', authenticate, asyncHandler(async (req, res) => {
  await db.refreshTokens.revokeAllForUser(req.user.sub);
  res.clearCookie('refreshToken');
  res.sendStatus(204);
}));
```

### 21.2 Session-Based Authentication

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

app.use(session({
  store:  new RedisStore({ client: redisClient, prefix: 'sess:' }),
  secret: process.env.SESSION_SECRET,   // must be long random string
  resave: false,                         // don't save session if unmodified
  saveUninitialized: false,              // don't create session until data stored
  name: 'sid',                           // cookie name (don't use default 'connect.sid')
  cookie: {
    httpOnly: true,
    secure:   process.env.NODE_ENV === 'production', // HTTPS only in prod
    sameSite: 'lax',
    maxAge:   24 * 60 * 60 * 1000,      // 24 hours
  },
  rolling: true, // reset expiry on each request
}));

// Session usage
app.post('/login', async (req, res) => {
  const user = await verifyCredentials(req.body.email, req.body.password);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  // Regenerate session ID after login (prevents session fixation attack!)
  await new Promise((resolve, reject) =>
    req.session.regenerate(err => err ? reject(err) : resolve())
  );

  req.session.userId = user.id;
  req.session.role   = user.role;
  req.session.save();

  res.json({ success: true });
});

app.post('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) console.error(err);
    res.clearCookie('sid');
    res.json({ success: true });
  });
});

// Session auth middleware
function requireSession(req, res, next) {
  if (!req.session.userId) return res.status(401).json({ error: 'Please log in' });
  next();
}
```

---

## Chapter 22: Database Integration

### 22.1 PostgreSQL with pg

```javascript
const { Pool } = require('pg');

// ── Connection pool ───────────────────────────────────────────
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Or individual options:
  host:     process.env.DB_HOST || 'localhost',
  port:     Number(process.env.DB_PORT) || 5432,
  database: process.env.DB_NAME,
  user:     process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  ssl:      process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,

  max:              20,    // max connections in pool
  min:              2,     // min connections to maintain
  idleTimeoutMillis: 30000, // close idle connections after 30s
  connectionTimeoutMillis: 5000, // fail if can't connect in 5s
  allowExitOnIdle: true,   // allow process to exit if only idle connections remain
});

pool.on('error', (err, client) => {
  console.error('Unexpected pg pool error:', err);
  process.exit(1);
});

pool.on('connect', (client) => {
  client.query("SET application_name = 'myapp'"); // identify your app to DB
});

// ── Query execution ───────────────────────────────────────────
// Simple query (pool manages connection checkout/return)
const { rows } = await pool.query(
  'SELECT id, name, email FROM users WHERE active = $1 ORDER BY name LIMIT $2',
  [true, 10]  // parameterized — prevents SQL injection
);

// Query with named result destructuring
const { rows: [user], rowCount } = await pool.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);
if (rowCount === 0) throw new NotFoundError('User', userId);

// INSERT returning new record
const { rows: [newUser] } = await pool.query(
  `INSERT INTO users (name, email, password_hash, role)
   VALUES ($1, $2, $3, $4)
   RETURNING id, name, email, role, created_at`,
  [name, email, passwordHash, 'user']
);

// UPDATE
const { rowCount: affected } = await pool.query(
  'UPDATE users SET name = $1, updated_at = NOW() WHERE id = $2 AND org_id = $3',
  [name, userId, orgId]
);
if (affected === 0) throw new NotFoundError('User', userId);

// DELETE
await pool.query('DELETE FROM users WHERE id = $1', [userId]);

// ── Transactions ──────────────────────────────────────────────
async function transferFunds(fromId, toId, amount) {
  const client = await pool.connect(); // checkout dedicated connection
  try {
    await client.query('BEGIN');
    await client.query('SET TRANSACTION ISOLATION LEVEL READ COMMITTED');

    const { rows: [from] } = await client.query(
      'SELECT balance FROM accounts WHERE id = $1 FOR UPDATE', [fromId]
    );
    if (from.balance < amount) throw new Error('Insufficient funds');

    await client.query(
      'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
      [amount, fromId]
    );
    await client.query(
      'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
      [amount, toId]
    );

    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release(); // ALWAYS return connection to pool
  }
}

// ── Repository pattern ────────────────────────────────────────
class UserRepository {
  constructor(pool) {
    this.pool = pool;
  }

  async findById(id) {
    const { rows: [user] } = await this.pool.query(
      'SELECT id, name, email, role, active, created_at FROM users WHERE id = $1',
      [id]
    );
    return user || null;
  }

  async findByEmail(email) {
    const { rows: [user] } = await this.pool.query(
      'SELECT * FROM users WHERE LOWER(email) = LOWER($1)',
      [email]
    );
    return user || null;
  }

  async findAll({ limit = 20, offset = 0, search, role, active } = {}) {
    const conditions = ['1=1'];
    const values = [];
    let i = 1;

    if (search) {
      conditions.push(`(name ILIKE $${i} OR email ILIKE $${i})`);
      values.push(`%${search}%`);
      i++;
    }
    if (role)          { conditions.push(`role = $${i++}`);   values.push(role); }
    if (active != null){ conditions.push(`active = $${i++}`); values.push(active); }

    values.push(limit, offset);

    const { rows } = await this.pool.query(
      `SELECT id, name, email, role, active, created_at
       FROM users
       WHERE ${conditions.join(' AND ')}
       ORDER BY created_at DESC
       LIMIT $${i} OFFSET $${i + 1}`,
      values
    );

    const { rows: [{ count }] } = await this.pool.query(
      `SELECT COUNT(*) FROM users WHERE ${conditions.slice(0, -0).join(' AND ')}`,
      values.slice(0, -2)  // exclude limit and offset
    );

    return { users: rows, total: Number(count) };
  }

  async create({ name, email, passwordHash, role = 'user' }) {
    const { rows: [user] } = await this.pool.query(
      `INSERT INTO users (name, email, password_hash, role)
       VALUES ($1, $2, $3, $4)
       RETURNING id, name, email, role, created_at`,
      [name, email, passwordHash, role]
    );
    return user;
  }

  async update(id, updates) {
    const fields = Object.entries(updates)
      .filter(([, v]) => v !== undefined)
      .map(([k, _], i) => `${this.#toSnake(k)} = $${i + 2}`);

    if (fields.length === 0) throw new Error('No fields to update');

    const values = Object.values(updates).filter(v => v !== undefined);
    const { rows: [user] } = await this.pool.query(
      `UPDATE users SET ${fields.join(', ')}, updated_at = NOW()
       WHERE id = $1
       RETURNING id, name, email, role, updated_at`,
      [id, ...values]
    );
    return user || null;
  }

  async delete(id) {
    const { rowCount } = await this.pool.query('DELETE FROM users WHERE id = $1', [id]);
    return rowCount > 0;
  }

  #toSnake(camel) {
    return camel.replace(/[A-Z]/g, c => `_${c.toLowerCase()}`);
  }
}
```

### 22.2 Redis Integration

```javascript
const { createClient } = require('redis');

const redis = createClient({
  url:      process.env.REDIS_URL || 'redis://localhost:6379',
  socket: {
    reconnectStrategy: (retries) => Math.min(retries * 50, 3000),
    connectTimeout:    10000,
  },
});

redis.on('error',       (err) => console.error('Redis error:', err));
redis.on('connect',     ()    => console.log('Redis connected'));
redis.on('reconnecting',()    => console.log('Redis reconnecting'));

await redis.connect();

// ── Caching middleware ────────────────────────────────────────
function cache(keyFn, ttlSeconds = 300) {
  return asyncHandler(async (req, res, next) => {
    const key = `cache:${typeof keyFn === 'function' ? keyFn(req) : keyFn}`;

    const cached = await redis.get(key);
    if (cached) {
      res.set('X-Cache', 'HIT');
      return res.json(JSON.parse(cached));
    }

    // Intercept res.json to cache the response
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      redis.setEx(key, ttlSeconds, JSON.stringify(data)).catch(console.error);
      res.set('X-Cache', 'MISS');
      return originalJson(data);
    };

    next();
  });
}

// Cache invalidation
async function invalidateCache(pattern) {
  const keys = await redis.keys(`cache:${pattern}`);
  if (keys.length > 0) await redis.del(keys);
}

// Usage
router.get('/users', cache('users:list', 60), listUsersController);
router.post('/users', asyncHandler(async (req, res) => {
  const user = await userService.create(req.body);
  await invalidateCache('users:*');  // invalidate all user caches
  res.status(201).json(user);
}));

// ── Redis data patterns ───────────────────────────────────────

// Key-value caching
await redis.setEx('user:42', 3600, JSON.stringify(user));
const cached = JSON.parse(await redis.get('user:42') || 'null');

// Counter / rate limiting
const count = await redis.incr('requests:api:' + userId);
await redis.expire('requests:api:' + userId, 60); // 1 minute window

// Distributed lock (prevent concurrent execution)
async function withLock(key, ttl, fn) {
  const lockKey = `lock:${key}`;
  const lockId  = crypto.randomUUID();
  const acquired = await redis.set(lockKey, lockId, { NX: true, EX: ttl });
  if (!acquired) throw new Error('Could not acquire lock');
  try {
    return await fn();
  } finally {
    // Only release if we still own the lock (Lua script for atomicity)
    const script = `
      if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
      else
        return 0
      end
    `;
    await redis.eval(script, { keys: [lockKey], arguments: [lockId] });
  }
}

// Pub/Sub
const subscriber = redis.duplicate();
await subscriber.connect();
await subscriber.subscribe('notifications', (message, channel) => {
  broadcastToWebSocketClients(JSON.parse(message));
});

await redis.publish('notifications', JSON.stringify({ type: 'user.created', userId: 42 }));

// Sorted sets for leaderboards
await redis.zAdd('leaderboard', [{ score: 95, value: 'alice' }]);
await redis.zAdd('leaderboard', [{ score: 87, value: 'bob' }]);
const topUsers = await redis.zRangeWithScores('leaderboard', 0, 9, { REV: true }); // top 10
```

---

## Chapter 23: Input Validation & Security

### 23.1 Security Best Practices

```javascript
// ── SQL Injection Prevention ───────────────────────────────────
// ❌ NEVER concatenate user input into SQL
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;
// Attacker input: "admin@example.com' OR '1'='1" → returns all users

// ✅ ALWAYS use parameterized queries
pool.query('SELECT * FROM users WHERE email = $1', [req.body.email]);

// ── XSS Prevention ────────────────────────────────────────────
// ❌ Never inject user input into HTML without escaping
res.send(`<div>${req.query.name}</div>`); // XSS if name = "<script>alert('xss')</script>"

// ✅ Use template engine escaping (EJS: <%= %> auto-escapes)
// ✅ For React/Vue: they escape by default
// ✅ Use DOMPurify for user HTML content
const DOMPurify = require('isomorphic-dompurify');
const clean = DOMPurify.sanitize(userHtml);

// ✅ Set Content-Security-Policy header (helmet does this)

// ── CSRF Prevention ───────────────────────────────────────────
// For traditional web apps using cookies for sessions:
const csrf = require('csurf');
app.use(csrf({ cookie: true }));

// In forms: include CSRF token
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});
// In form: <input type="hidden" name="_csrf" value="<%= csrfToken %>">

// For APIs (JWT-based): CSRF is less relevant (tokens not auto-sent like cookies)
// But if you use cookie-based JWT: implement CSRF or use SameSite=Strict

// ── NoSQL Injection (MongoDB) ─────────────────────────────────
// ❌ Dangerous — user can send { "$gt": "" } as email
const user = await User.findOne({ email: req.body.email });

// ✅ Validate that email is a string first
if (typeof req.body.email !== 'string') throw new ValidationError(...);
const user2 = await User.findOne({ email: req.body.email });

// ✅ Or use Mongoose which validates schema types

// ── Path Traversal Prevention ─────────────────────────────────
// ❌ Never use user input directly in file paths
const file = path.join('/uploads', req.params.filename);
// Attacker: ../../etc/passwd

// ✅ Sanitize filename and resolve relative paths
function safeFilePath(uploadDir, filename) {
  const safeFilename = path.basename(filename); // strip directory separators
  const fullPath = path.resolve(uploadDir, safeFilename);
  if (!fullPath.startsWith(path.resolve(uploadDir))) {
    throw new Error('Path traversal detected');
  }
  return fullPath;
}

// ── Sensitive Data ────────────────────────────────────────────
// Never log passwords, tokens, credit cards
const { password, ...safeBody } = req.body;
logger.info('Login attempt', { email: safeBody.email }); // not password

// Mask sensitive fields in errors
function sanitizeError(err) {
  const safe = { ...err };
  delete safe.password;
  delete safe.token;
  return safe;
}

// ── HTTP Security Headers ─────────────────────────────────────
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc:  ["'self'", 'cdn.jsdelivr.net'],
      styleSrc:   ["'self'", "'unsafe-inline'"],
      imgSrc:     ["'self'", 'data:', 'https://s3.amazonaws.com'],
      connectSrc: ["'self'", 'wss://myapp.com'],
      frameSrc:   ["'none'"],
      objectSrc:  ["'none'"],
    },
  },
  hsts: {
    maxAge:            31536000,  // 1 year
    includeSubDomains: true,
    preload:           true,
  },
}));
```

---

## Chapter 24: File Uploads & Multipart

### 24.1 Multer — File Upload Middleware

```javascript
const multer  = require('multer');
const sharp   = require('sharp');   // image processing
const path    = require('path');
const crypto  = require('crypto');

// ── Memory storage (for small files or processing before saving) ──
const memoryUpload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024,  // 5MB per file
    files: 5,                    // max 5 files per request
    fields: 10,                  // max 10 non-file fields
  },
  fileFilter(req, file, cb) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new ValidationError('File type not allowed', {
        allowed: allowedTypes,
        received: file.mimetype,
      }));
    }
    cb(null, true); // accept the file
  },
});

// ── Disk storage (for large files — stream to disk) ───────────
const diskUpload = multer({
  storage: multer.diskStorage({
    destination(req, file, cb) {
      cb(null, 'uploads/temp/');
    },
    filename(req, file, cb) {
      // Generate unique filename to prevent collisions
      const ext  = path.extname(file.originalname).toLowerCase();
      const name = crypto.randomBytes(16).toString('hex');
      cb(null, `${name}${ext}`);
    },
  }),
  limits: { fileSize: 100 * 1024 * 1024 }, // 100MB
});

// ── S3 storage (production — stream directly to S3) ───────────
const multerS3 = require('multer-s3');
const { S3Client } = require('@aws-sdk/client-s3');

const s3 = new S3Client({ region: process.env.AWS_REGION });
const s3Upload = multer({
  storage: multerS3({
    s3,
    bucket: process.env.S3_BUCKET,
    contentType: multerS3.AUTO_CONTENT_TYPE,
    key(req, file, cb) {
      const ext  = path.extname(file.originalname);
      const name = crypto.randomBytes(16).toString('hex');
      cb(null, `uploads/${req.user.id}/${name}${ext}`);
    },
    metadata(req, file, cb) {
      cb(null, { originalName: file.originalname, uploadedBy: req.user.id });
    },
  }),
  limits: { fileSize: 50 * 1024 * 1024 },
});

// ── Upload routes ─────────────────────────────────────────────
// Single file upload
router.post('/avatar',
  authenticate,
  memoryUpload.single('avatar'),  // 'avatar' = form field name
  asyncHandler(async (req, res) => {
    if (!req.file) throw new ValidationError('No file uploaded');

    // Process image with sharp (resize, convert format, strip EXIF)
    const processed = await sharp(req.file.buffer)
      .resize(200, 200, { fit: 'cover' })
      .webp({ quality: 80 })
      .toBuffer();

    // Upload to S3 / MinIO
    const key = `avatars/${req.user.sub}-${Date.now()}.webp`;
    await s3.putObject({ Bucket: process.env.S3_BUCKET, Key: key, Body: processed, ContentType: 'image/webp' });

    const url = `https://${process.env.S3_BUCKET}.s3.amazonaws.com/${key}`;
    await db.users.update(req.user.sub, { avatarUrl: url });

    res.json({ avatarUrl: url });
  })
);

// Multiple files
router.post('/documents',
  authenticate,
  memoryUpload.array('files', 10), // up to 10 files
  asyncHandler(async (req, res) => {
    const uploaded = await Promise.all(
      req.files.map(async (file) => {
        const key = `documents/${req.user.sub}/${Date.now()}-${file.originalname}`;
        await s3.putObject({ Bucket: process.env.S3_BUCKET, Key: key, Body: file.buffer });
        return { originalName: file.originalname, key, size: file.size };
      })
    );
    res.json({ files: uploaded });
  })
);

// Mixed fields and files
router.post('/listings',
  authenticate,
  memoryUpload.fields([
    { name: 'thumbnail', maxCount: 1 },
    { name: 'images',    maxCount: 10 },
  ]),
  validate(createListingSchema),
  asyncHandler(async (req, res) => {
    const { title, price, description } = req.body;
    const thumbnail = req.files.thumbnail?.[0];
    const images    = req.files.images || [];
    // process...
    res.status(201).json({ created: true });
  })
);

// Handle multer errors
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large' });
    }
    if (err.code === 'LIMIT_FILE_COUNT') {
      return res.status(400).json({ error: 'Too many files' });
    }
    return res.status(400).json({ error: err.message });
  }
  next(err);
});
```

---

## Chapter 25: WebSockets & Real-Time with Socket.io

### 25.1 Socket.io — Full Implementation

```javascript
const { createServer } = require('http');
const { Server }       = require('socket.io');
const jwt              = require('jsonwebtoken');

const app        = express();
const httpServer = createServer(app);
const io         = new Server(httpServer, {
  cors: {
    origin:      process.env.CLIENT_URL,
    credentials: true,
    methods:     ['GET', 'POST'],
  },
  pingTimeout:  60000,
  pingInterval: 25000,
  transports:   ['websocket', 'polling'],  // try WebSocket first, fall back to polling
});

// ── Authentication middleware for Socket.io ───────────────────
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token
      || socket.handshake.headers.authorization?.replace('Bearer ', '');

    if (!token) return next(new Error('Authentication required'));

    const payload = jwt.verify(token, process.env.JWT_SECRET);
    socket.data.user = payload;  // attach to socket
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

// ── Namespace for chat ────────────────────────────────────────
const chatNs = io.of('/chat'); // namespace: clients connect to /chat

chatNs.use(authMiddleware); // namespace-specific middleware

chatNs.on('connection', (socket) => {
  const { user } = socket.data;
  console.log(`User ${user.id} connected (socket: ${socket.id})`);

  // ── Rooms — group sockets ───────────────────────────────────
  socket.on('join-room', async (roomId) => {
    // Validate user has access to room
    const room = await db.rooms.findById(roomId);
    if (!room || !room.members.includes(user.id)) {
      return socket.emit('error', { message: 'Access denied' });
    }

    await socket.join(roomId);  // join the room
    socket.emit('joined', { roomId, members: room.members });

    // Notify others in room
    socket.to(roomId).emit('user-joined', { userId: user.id, name: user.name });
  });

  socket.on('leave-room', (roomId) => {
    socket.leave(roomId);
    socket.to(roomId).emit('user-left', { userId: user.id });
  });

  // ── Messaging ─────────────────────────────────────────────
  socket.on('send-message', async ({ roomId, content }) => {
    // Validate
    if (!content?.trim()) return;
    if (content.length > 5000) return socket.emit('error', { message: 'Message too long' });

    // Check user is in room
    const rooms = socket.rooms; // Set of rooms this socket is in
    if (!rooms.has(roomId)) return socket.emit('error', { message: 'Not in room' });

    const message = await db.messages.create({
      roomId, userId: user.id, content: content.trim()
    });

    // Emit to EVERYONE in room (including sender)
    chatNs.to(roomId).emit('new-message', {
      id:        message.id,
      content:   message.content,
      sender:    { id: user.id, name: user.name, avatar: user.avatar },
      timestamp: message.createdAt.toISOString(),
    });
  });

  // ── Typing indicators ─────────────────────────────────────
  socket.on('typing-start', ({ roomId }) => {
    socket.to(roomId).emit('user-typing', { userId: user.id, name: user.name });
  });
  socket.on('typing-stop', ({ roomId }) => {
    socket.to(roomId).emit('user-stopped-typing', { userId: user.id });
  });

  // ── Presence ──────────────────────────────────────────────
  socket.on('disconnect', (reason) => {
    console.log(`User ${user.id} disconnected: ${reason}`);
    // Notify all rooms this socket was in
    socket.rooms.forEach(room => {
      if (room !== socket.id) {
        socket.to(room).emit('user-offline', { userId: user.id });
      }
    });
  });
});

// ── Emitting from outside a socket (e.g., from REST route) ────
router.post('/broadcast', authenticate, requireRole('admin'), asyncHandler(async (req, res) => {
  const { roomId, message } = req.body;

  // Emit to all in a room
  io.of('/chat').to(roomId).emit('system-message', { content: message });

  // Emit to specific user (by their socket)
  const targetSocketId = await getUserSocketId(targetUserId); // stored in Redis
  if (targetSocketId) {
    io.of('/chat').to(targetSocketId).emit('direct-message', { content: message });
  }

  res.json({ sent: true });
}));

// ── Socket.io with Redis adapter (multi-server scaling) ───────
const { createAdapter } = require('@socket.io/redis-adapter');
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
await Promise.all([pubClient.connect(), subClient.connect()]);
io.adapter(createAdapter(pubClient, subClient));
// Now Socket.io works across multiple Node.js instances!
```

---

## Chapter 26: REST API Design & Best Practices

### 26.1 RESTful API Design Principles

```javascript
// ── Resource naming ───────────────────────────────────────────
// ✅ Plural nouns for collections
GET    /api/v1/users             // list users
POST   /api/v1/users             // create user
GET    /api/v1/users/:id         // get user
PUT    /api/v1/users/:id         // full replace user
PATCH  /api/v1/users/:id         // partial update user
DELETE /api/v1/users/:id         // delete user

// ✅ Nested resources for relationships
GET    /api/v1/users/:id/orders  // user's orders
POST   /api/v1/users/:id/orders  // create order for user
GET    /api/v1/users/:id/orders/:orderId // specific order

// ❌ Avoid verbs in URLs
// GET /api/getUsers  (use GET /api/users)
// POST /api/createUser (use POST /api/users)
// POST /api/users/:id/deactivate? (sometimes verbs are ok for actions)

// ✅ Non-CRUD actions as sub-resources
POST /api/v1/users/:id/password    // change password
POST /api/v1/users/:id/avatar      // upload avatar
POST /api/v1/auth/login            // login (action, not resource)
POST /api/v1/orders/:id/cancel     // cancel order

// ── HTTP status codes ─────────────────────────────────────────
// 200 OK            — GET, PUT, PATCH success (with body)
// 201 Created       — POST success (new resource created)
// 204 No Content    — DELETE success (no body) or PUT with no body
// 400 Bad Request   — validation error, malformed request
// 401 Unauthorized  — not authenticated (no or invalid token)
// 403 Forbidden     — authenticated but not authorized (wrong role)
// 404 Not Found     — resource doesn't exist
// 409 Conflict      — conflict with current state (duplicate email)
// 422 Unprocessable — semantically invalid (business rule violation)
// 429 Too Many Requests — rate limit exceeded
// 500 Internal Server Error — unexpected server error

// ── Consistent response format ────────────────────────────────
// Collection response
res.json({
  data:  users,          // the resources
  meta: {
    total:    100,       // total count (for pagination)
    page:     2,
    pageSize: 20,
    pages:    5,
  },
  links: {
    self:  '/api/v1/users?page=2',
    prev:  '/api/v1/users?page=1',
    next:  '/api/v1/users?page=3',
    first: '/api/v1/users?page=1',
    last:  '/api/v1/users?page=5',
  }
});

// Single resource
res.json({
  data: user,
  links: { self: `/api/v1/users/${user.id}` }
});

// Error response
res.status(400).json({
  error: {
    code:    'VALIDATION_ERROR',
    message: 'Validation failed',
    details: {
      email:    ['Invalid email format'],
      password: ['Must be at least 8 characters'],
    },
    requestId: req.id,
    timestamp: new Date().toISOString(),
  }
});

// ── Query parameters ──────────────────────────────────────────
// Pagination
GET /api/v1/users?page=2&pageSize=20          // page-based
GET /api/v1/users?cursor=abc123&limit=20      // cursor-based (preferred for real-time)

// Filtering
GET /api/v1/users?role=admin&active=true
GET /api/v1/users?createdAfter=2024-01-01&createdBefore=2024-12-31

// Sorting
GET /api/v1/users?sort=-createdAt              // - prefix = descending
GET /api/v1/users?sort=name,-createdAt        // multiple fields

// Field selection (sparse fieldsets)
GET /api/v1/users?fields=id,name,email         // only return these fields

// Including related resources
GET /api/v1/users?include=orders,profile       // eager load relationships

// Searching
GET /api/v1/users?q=alice&searchFields=name,email

// ── Pagination implementation ─────────────────────────────────
async function paginateQuery(queryFn, { page = 1, limit = 20 }) {
  limit  = Math.min(Math.max(1, limit), 100); // enforce max 100
  page   = Math.max(1, page);
  const offset = (page - 1) * limit;

  const [data, total] = await Promise.all([
    queryFn({ limit, offset }),
    queryFn.count(),  // separate count query
  ]);

  const pages = Math.ceil(total / limit);
  return {
    data,
    meta:  { total, page, pageSize: limit, pages, hasNext: page < pages, hasPrev: page > 1 },
  };
}

// Cursor-based pagination (better for large datasets)
async function cursorPaginate(db, { cursor, limit = 20 }) {
  const items = await db.query(`
    SELECT * FROM posts
    WHERE id < $1
    ORDER BY id DESC
    LIMIT $2
  `, [cursor || Number.MAX_SAFE_INTEGER, limit + 1]);

  const hasMore = items.length > limit;
  const data = hasMore ? items.slice(0, limit) : items;
  const nextCursor = hasMore ? data[data.length - 1].id : null;

  return { data, meta: { hasMore, nextCursor } };
}
```

---

## Chapter 27: Testing Node.js & Express

### 27.1 Jest Setup

```javascript
// package.json
// "jest": {
//   "testEnvironment": "node",
//   "testMatch": ["**/*.test.js", "**/*.spec.js"],
//   "collectCoverageFrom": ["src/**/*.js", "!src/**/*.test.js"],
//   "coverageThreshold": { "global": { "lines": 80 } },
//   "setupFilesAfterFramework": ["./tests/setup.js"],
//   "globalSetup": "./tests/globalSetup.js",
//   "globalTeardown": "./tests/globalTeardown.js"
// }

// tests/setup.js
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret';
process.env.DATABASE_URL = 'postgresql://localhost:5432/myapp_test';

// tests/globalSetup.js
module.exports = async () => {
  // Start test database, run migrations
  await runMigrations();
};

// tests/globalTeardown.js
module.exports = async () => {
  await cleanupTestDatabase();
};
```

### 27.2 Supertest — HTTP Integration Tests

```javascript
const request    = require('supertest');
const app        = require('../src/app');
const { Pool }   = require('pg');
const jwt        = require('jsonwebtoken');

// ── Test utilities ────────────────────────────────────────────
function generateTestToken(overrides = {}) {
  return jwt.sign(
    { sub: '1', email: 'test@example.com', role: 'user', ...overrides },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
}

// ── User routes tests ─────────────────────────────────────────
describe('GET /api/v1/users', () => {
  let token;

  beforeAll(async () => {
    token = generateTestToken({ role: 'admin' });
    // Seed test data
    await pool.query(`INSERT INTO users (id, name, email, role) VALUES
      ('1', 'Alice', 'alice@test.com', 'admin'),
      ('2', 'Bob',   'bob@test.com',   'user')`);
  });

  afterAll(async () => {
    await pool.query('DELETE FROM users WHERE email LIKE \'%@test.com\'');
  });

  it('returns 401 without token', async () => {
    const res = await request(app).get('/api/v1/users');
    expect(res.status).toBe(401);
    expect(res.body).toMatchObject({ error: expect.any(String) });
  });

  it('returns 403 for non-admin', async () => {
    const userToken = generateTestToken({ role: 'user' });
    const res = await request(app)
      .get('/api/v1/users')
      .set('Authorization', `Bearer ${userToken}`);
    expect(res.status).toBe(403);
  });

  it('returns paginated users list', async () => {
    const res = await request(app)
      .get('/api/v1/users?page=1&limit=10')
      .set('Authorization', `Bearer ${token}`);

    expect(res.status).toBe(200);
    expect(res.body.data).toBeInstanceOf(Array);
    expect(res.body.meta).toMatchObject({
      page:     1,
      pageSize: 10,
      total:    expect.any(Number),
    });
  });
});

describe('POST /api/v1/users', () => {
  it('creates a user with valid data', async () => {
    const adminToken = generateTestToken({ role: 'admin' });
    const userData = {
      name:     'Carol',
      email:    `carol-${Date.now()}@test.com`,
      password: 'password123',
    };

    const res = await request(app)
      .post('/api/v1/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(userData);

    expect(res.status).toBe(201);
    expect(res.body.data).toMatchObject({
      id:    expect.any(String),
      name:  userData.name,
      email: userData.email,
    });
    expect(res.body.data.password).toBeUndefined(); // no password in response!
  });

  it('returns 400 for invalid email', async () => {
    const adminToken = generateTestToken({ role: 'admin' });
    const res = await request(app)
      .post('/api/v1/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Test', email: 'not-an-email', password: 'pass123' });

    expect(res.status).toBe(400);
    expect(res.body.error.details.email).toBeDefined();
  });

  it('returns 409 for duplicate email', async () => {
    const adminToken = generateTestToken({ role: 'admin' });
    const body = { name: 'Alice2', email: 'alice@test.com', password: 'pass123' };

    const res = await request(app)
      .post('/api/v1/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send(body);

    expect(res.status).toBe(409);
  });
});

// ── Testing file uploads ──────────────────────────────────────
it('uploads avatar successfully', async () => {
  const token = generateTestToken();
  const res = await request(app)
    .post('/api/v1/users/me/avatar')
    .set('Authorization', `Bearer ${token}`)
    .attach('avatar', Buffer.from('fake image data'), {
      filename:    'avatar.jpg',
      contentType: 'image/jpeg',
    });

  expect(res.status).toBe(200);
  expect(res.body.avatarUrl).toMatch(/^https?:\/\//);
});
```

### 27.3 Unit Testing Services

```javascript
// Unit tests — test business logic in isolation (mock dependencies)
describe('UserService', () => {
  let userService;
  let mockUserRepo;
  let mockEmailService;
  let mockCache;

  beforeEach(() => {
    // Create mocks
    mockUserRepo = {
      findByEmail: jest.fn(),
      create:      jest.fn(),
      findById:    jest.fn(),
      update:      jest.fn(),
    };
    mockEmailService = { sendWelcome: jest.fn() };
    mockCache        = { set: jest.fn(), get: jest.fn(), del: jest.fn() };

    userService = new UserService(mockUserRepo, mockEmailService, mockCache);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    const validInput = { name: 'Alice', email: 'alice@example.com', password: 'pass123' };

    it('creates user and sends welcome email', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null); // email not taken
      mockUserRepo.create.mockResolvedValue({ id: '1', ...validInput });
      mockEmailService.sendWelcome.mockResolvedValue(true);

      const user = await userService.createUser(validInput);

      expect(mockUserRepo.findByEmail).toHaveBeenCalledWith(validInput.email);
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.objectContaining({ name: validInput.name, email: validInput.email })
      );
      expect(mockEmailService.sendWelcome).toHaveBeenCalledWith(validInput.email, validInput.name);
      expect(user.id).toBe('1');
    });

    it('throws ConflictError if email already exists', async () => {
      mockUserRepo.findByEmail.mockResolvedValue({ id: 'existing' });

      await expect(userService.createUser(validInput))
        .rejects
        .toThrow(ConflictError);

      expect(mockUserRepo.create).not.toHaveBeenCalled();
      expect(mockEmailService.sendWelcome).not.toHaveBeenCalled();
    });

    it('still creates user even if welcome email fails', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockResolvedValue({ id: '1', ...validInput });
      mockEmailService.sendWelcome.mockRejectedValue(new Error('Email failed'));

      // Should not throw — email failure is non-critical
      const user = await userService.createUser(validInput);
      expect(user.id).toBe('1');
    });
  });
});
```

---

## Chapter 28: Logging, Monitoring & Observability

### 28.1 Pino — Structured Logging

```javascript
const pino = require('pino');

// ── Logger configuration ──────────────────────────────────────
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  // Pretty print in development
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true, translateTime: 'SYS:standard' } }
    : undefined,

  // Custom serializers — transform objects before logging
  serializers: {
    req(req) {
      return {
        id:     req.id,
        method: req.method,
        url:    req.url,
        ip:     req.ip,
      };
    },
    res(res) {
      return { statusCode: res.statusCode };
    },
    err: pino.stdSerializers.err,  // format Error objects
  },

  // Add base fields to every log line
  base: {
    pid:         process.pid,
    service:     process.env.SERVICE_NAME || 'api',
    environment: process.env.NODE_ENV,
    version:     process.env.APP_VERSION,
  },

  // Redact sensitive fields from log output
  redact: {
    paths: ['req.headers.authorization', 'req.body.password', '*.token', '*.secret'],
    censor: '[REDACTED]',
  },
});

// ── Request logging ───────────────────────────────────────────
const pinoHttp = require('pino-http');
app.use(pinoHttp({
  logger,
  customLogLevel(req, res, err) {
    if (err || res.statusCode >= 500) return 'error';
    if (res.statusCode >= 400)        return 'warn';
    return 'info';
  },
  customSuccessMessage(req, res) {
    return `${req.method} ${req.url} → ${res.statusCode}`;
  },
  customErrorMessage(req, res, err) {
    return `${req.method} ${req.url} → ${res.statusCode}: ${err.message}`;
  },
}));

// ── Structured log calls ──────────────────────────────────────
// Use structured logging — searchable key-value pairs, not string interpolation
logger.info({ userId: user.id, action: 'login', ip: req.ip }, 'User logged in');
logger.warn({ userId: user.id, attempts: 3 }, 'Multiple failed login attempts');
logger.error({ err, orderId: order.id, userId }, 'Failed to process payment');

// Child logger — add context to all logs in a scope
const requestLogger = logger.child({ requestId: req.id, userId: req.user?.sub });
requestLogger.info({ action: 'fetch-user' }, 'Fetching user');
requestLogger.debug({ query: 'SELECT...' }, 'Executing DB query');

// ── Log rotation and shipping ─────────────────────────────────
// In production: pipe pino output to a log shipping service
// node app.js | pino-elasticsearch --es-url http://localhost:9200
// node app.js | tee app.log | pino-pretty
// Or use pino.transport() for async file writing:
const transport = pino.transport({
  targets: [
    { target: 'pino/file', options: { destination: '/var/log/app.log' } },
    { target: 'pino-sentry', options: { dsn: process.env.SENTRY_DSN } },
  ],
});
```

---

## Chapter 29: Configuration & Environment Management

### 29.1 Environment Variables & dotenv

```javascript
// .env file (NEVER commit to git — add to .gitignore)
// .env.example (commit this — shows required variables)

// .env.example
// NODE_ENV=development
// PORT=3000
// DATABASE_URL=postgresql://user:password@localhost:5432/myapp
// REDIS_URL=redis://localhost:6379
// JWT_SECRET=change-this-in-production-min-32-chars
// JWT_REFRESH_SECRET=different-secret-min-32-chars

// Load env file
require('dotenv').config({
  path: `.env.${process.env.NODE_ENV || 'development'}`,
});
// Or: import 'dotenv/config';

// ── Config module — centralize and validate ───────────────────
const { z } = require('zod');

const configSchema = z.object({
  NODE_ENV:          z.enum(['development', 'test', 'production']).default('development'),
  PORT:              z.string().regex(/^\d+$/).transform(Number).default('3000'),
  DATABASE_URL:      z.string().url(),
  REDIS_URL:         z.string().url().default('redis://localhost:6379'),
  JWT_SECRET:        z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  JWT_REFRESH_SECRET:z.string().min(32),
  JWT_EXPIRES_IN:    z.string().default('15m'),
  BCRYPT_ROUNDS:     z.string().transform(Number).default('12'),
  ALLOWED_ORIGINS:   z.string().default('http://localhost:3000'),
  LOG_LEVEL:         z.enum(['trace','debug','info','warn','error','fatal']).default('info'),
  S3_BUCKET:         z.string().optional(),
  AWS_REGION:        z.string().default('us-east-1'),
  SMTP_HOST:         z.string().optional(),
  SMTP_PORT:         z.string().transform(Number).default('587'),
  SMTP_USER:         z.string().optional(),
  SMTP_PASS:         z.string().optional(),
  SENTRY_DSN:        z.string().url().optional(),
});

function loadConfig() {
  const result = configSchema.safeParse(process.env);
  if (!result.success) {
    const errors = result.error.flatten().fieldErrors;
    const missing = Object.entries(errors)
      .map(([k, v]) => `  ${k}: ${v.join(', ')}`)
      .join('\n');
    throw new Error(`Invalid environment configuration:\n${missing}`);
  }
  return result.data;
}

const config = loadConfig();
// Fail fast: if env is invalid, crash immediately with clear message
// Never let the app start with bad config

module.exports = config;

// Usage
const { PORT, DATABASE_URL, JWT_SECRET } = require('./config');
```

---

## Chapter 30: Performance, Caching & Scalability

### 30.1 Performance Optimization

```javascript
// ── Connection pooling ────────────────────────────────────────
// Already covered in Chapter 22 — use pg Pool, redis client

// ── Response caching ──────────────────────────────────────────
// Cache at multiple levels:
// 1. HTTP cache (Cache-Control headers) — browser & CDN cache
// 2. Application cache (Redis) — server-side caching
// 3. Database query cache — not recommended (unreliable)

// Set HTTP cache headers for static content
app.use('/static', express.static('public', {
  maxAge: '1y', // 1 year — with content-hashed filenames this is safe
  immutable: true, // tell browsers not to revalidate (Content-Encoding: immutable)
}));

// API response caching with ETags
app.get('/api/products', asyncHandler(async (req, res) => {
  const products = await getProductsFromDb();
  const etag = `"${crypto.createHash('md5').update(JSON.stringify(products)).digest('hex')}"`;

  res.set('ETag', etag);
  res.set('Cache-Control', 'private, max-age=0, must-revalidate');

  if (req.headers['if-none-match'] === etag) {
    return res.sendStatus(304); // Not Modified — client uses cached version
  }

  res.json(products);
}));

// ── Compression ───────────────────────────────────────────────
// Already covered in Chapter 17 — use compression middleware

// ── Database query optimization ───────────────────────────────
// N+1 query problem and solution
// ❌ N+1: 1 query for posts + N queries for each post's author
async function getPostsBad() {
  const posts = await db.query('SELECT * FROM posts LIMIT 20');
  for (const post of posts.rows) {
    const author = await db.query('SELECT * FROM users WHERE id = $1', [post.author_id]);
    post.author = author.rows[0];
  }
  return posts.rows;
}

// ✅ Single query with JOIN
async function getPostsGood() {
  const { rows } = await db.query(`
    SELECT
      p.*,
      u.id AS author_id, u.name AS author_name, u.avatar AS author_avatar
    FROM posts p
    JOIN users u ON u.id = p.author_id
    WHERE p.published = true
    ORDER BY p.created_at DESC
    LIMIT 20
  `);
  return rows.map(row => ({
    ...row,
    author: { id: row.author_id, name: row.author_name, avatar: row.author_avatar },
  }));
}

// DataLoader — batch and cache db lookups (for GraphQL, but useful anywhere)
const DataLoader = require('dataloader');

const userLoader = new DataLoader(async (userIds) => {
  const { rows } = await db.query('SELECT * FROM users WHERE id = ANY($1)', [userIds]);
  const userMap = new Map(rows.map(u => [u.id, u]));
  return userIds.map(id => userMap.get(id) || null);
});

// Now 100 userLoader.load(id) calls → batched into 1 DB query
const user = await userLoader.load(userId);

// ── Load testing ──────────────────────────────────────────────
// k6, Artillery, wrk, autocannon
// autocannon (Node.js):
const autocannon = require('autocannon');
const result = await autocannon({
  url:         'http://localhost:3000/api/users',
  connections: 100,    // concurrent connections
  duration:    30,     // seconds
  pipelining:  10,     // requests per connection
  headers: { authorization: `Bearer ${token}` },
});
console.log(autocannon.printResult(result));
```

---

## Chapter 31: Deployment — Docker, PM2, Nginx

### 31.1 Docker

```dockerfile
# Dockerfile
FROM node:20-alpine AS base
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Dependencies stage — cached unless package.json changes
FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Build stage (if TypeScript)
FROM base AS builder
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM base AS production
ENV NODE_ENV=production

# Copy production node_modules
COPY --from=deps    /app/node_modules ./node_modules
# Copy built code
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Security: run as non-root user
USER appuser

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "dist/server.js"]
```

```yaml
# docker-compose.yml
version: '3.9'
services:
  api:
    build:
      context: .
      target:  production
    ports:
      - "3000:3000"
    environment:
      NODE_ENV:       production
      DATABASE_URL:   postgresql://postgres:password@postgres:5432/myapp
      REDIS_URL:      redis://redis:6379
      JWT_SECRET:     ${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:   { cpus: '0.5', memory: '512M' }
        reservations: { cpus: '0.25', memory: '256M' }

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB:       myapp
      POSTGRES_USER:     postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test:     ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout:  5s
      retries:  5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    healthcheck:
      test:     ["CMD", "redis-cli", "ping"]
      interval: 10s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

### 31.2 PM2 — Process Manager

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name:        'my-api',
    script:      'dist/server.js',
    instances:   'max',     // one per CPU core
    exec_mode:   'cluster', // cluster mode — shares port
    watch:       false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'development',
      PORT:     3000,
    },
    env_production: {
      NODE_ENV: 'production',
      PORT:     3000,
    },
    error_file:   '/var/log/pm2/api-error.log',
    out_file:     '/var/log/pm2/api-out.log',
    log_file:     '/var/log/pm2/api-combined.log',
    time:         true,    // timestamps in logs
    kill_timeout: 30000,   // 30s graceful shutdown timeout
    wait_ready:   true,    // wait for process.send('ready')
    listen_timeout: 10000,
    exp_backoff_restart_delay: 100, // exponential backoff on restart
  }],
};
```

```bash
pm2 start ecosystem.config.js --env production
pm2 list                                    # show all apps
pm2 logs my-api --lines 100                # view logs
pm2 monit                                   # real-time dashboard
pm2 reload my-api                          # zero-downtime reload
pm2 restart my-api                         # restart (brief downtime)
pm2 stop my-api
pm2 delete my-api
pm2 save                                   # save list (persists on reboot)
pm2 startup                               # generate startup script
```

### 31.3 Nginx Configuration

```nginx
# /etc/nginx/nginx.conf
events { worker_connections 1024; }

http {
  upstream node_app {
    least_conn;                         # balance by least connections
    server 127.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    # or with Docker: server api:3000;
    keepalive 32;                       # keep 32 upstream connections alive
  }

  # Rate limiting zone
  limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

  # SSL settings
  ssl_session_cache    shared:SSL:10m;
  ssl_session_timeout  5m;
  ssl_ciphers          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
  ssl_protocols        TLSv1.2 TLSv1.3;
  ssl_prefer_server_ciphers on;

  server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;  # redirect HTTP → HTTPS
  }

  server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate      /etc/nginx/ssl/cert.pem;
    ssl_certificate_key  /etc/nginx/ssl/key.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    # Rate limiting
    limit_req zone=api burst=20 nodelay;

    # Static files (serve directly without Node.js)
    location /static/ {
      alias   /app/public/;
      expires 1y;
      add_header Cache-Control "public, immutable";
    }

    # Node.js API
    location /api/ {
      proxy_pass         http://node_app;
      proxy_http_version 1.1;
      proxy_set_header   Upgrade           $http_upgrade;
      proxy_set_header   Connection        'upgrade';  # for WebSockets
      proxy_set_header   Host              $host;
      proxy_set_header   X-Real-IP         $remote_addr;
      proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto $scheme;
      proxy_cache_bypass $http_upgrade;

      proxy_read_timeout  60s;
      proxy_connect_timeout 5s;
      proxy_send_timeout  60s;

      proxy_buffering    on;
      proxy_buffer_size  4k;
      proxy_buffers      8 4k;

      # Enable gzip for API responses
      gzip on;
      gzip_types application/json;
    }

    # Health check (no rate limiting)
    location /health {
      proxy_pass http://node_app;
      limit_req  off;
    }
  }
}
```

---

## Chapter 32: Design Patterns in Node.js

### 32.1 Repository Pattern — Data Access Layer

```javascript
// Clean separation: routes → controllers → services → repositories → database

// Generic repository interface
class BaseRepository {
  constructor(pool, tableName) {
    this.pool  = pool;
    this.table = tableName;
  }

  async findById(id) {
    const { rows: [row] } = await this.pool.query(
      `SELECT * FROM ${this.table} WHERE id = $1`, [id]
    );
    return row || null;
  }

  async findAll({ limit = 20, offset = 0, where = {}, orderBy = 'created_at DESC' } = {}) {
    const conditions = Object.entries(where)
      .map(([k, _], i) => `${k} = $${i + 3}`)
      .join(' AND ');
    const values = [limit, offset, ...Object.values(where)];

    const sql = `
      SELECT * FROM ${this.table}
      ${conditions ? 'WHERE ' + conditions : ''}
      ORDER BY ${orderBy}
      LIMIT $1 OFFSET $2
    `;
    const { rows } = await this.pool.query(sql, values);
    return rows;
  }

  async create(data) {
    const keys   = Object.keys(data);
    const values = Object.values(data);
    const cols   = keys.join(', ');
    const params = keys.map((_, i) => `$${i + 1}`).join(', ');

    const { rows: [row] } = await this.pool.query(
      `INSERT INTO ${this.table} (${cols}) VALUES (${params}) RETURNING *`,
      values
    );
    return row;
  }

  async update(id, data) {
    const entries = Object.entries(data).filter(([,v]) => v !== undefined);
    const sets    = entries.map(([k, _], i) => `${k} = $${i + 2}`).join(', ');
    const values  = [id, ...entries.map(([,v]) => v)];

    const { rows: [row] } = await this.pool.query(
      `UPDATE ${this.table} SET ${sets}, updated_at = NOW() WHERE id = $1 RETURNING *`,
      values
    );
    return row || null;
  }

  async delete(id) {
    const { rowCount } = await this.pool.query(
      `DELETE FROM ${this.table} WHERE id = $1`, [id]
    );
    return rowCount > 0;
  }

  async count(where = {}) {
    const conditions = Object.entries(where).map(([k,_], i) => `${k} = $${i+1}`).join(' AND ');
    const { rows: [{ count }] } = await this.pool.query(
      `SELECT COUNT(*) FROM ${this.table} ${conditions ? 'WHERE '+conditions : ''}`,
      Object.values(where)
    );
    return Number(count);
  }
}

// Specific repository with custom queries
class UserRepository extends BaseRepository {
  constructor(pool) { super(pool, 'users'); }

  async findByEmail(email) {
    const { rows: [user] } = await this.pool.query(
      'SELECT * FROM users WHERE LOWER(email) = LOWER($1)', [email]
    );
    return user || null;
  }

  async findActiveWithOrders({ limit, offset }) {
    const { rows } = await this.pool.query(`
      SELECT u.*, COUNT(o.id) AS order_count
      FROM users u
      LEFT JOIN orders o ON o.user_id = u.id AND o.status != 'cancelled'
      WHERE u.active = true
      GROUP BY u.id
      ORDER BY order_count DESC
      LIMIT $1 OFFSET $2
    `, [limit, offset]);
    return rows;
  }
}
```

### 32.2 Middleware Composition Pattern

```javascript
// Composing middleware functionally
const compose = (...middlewares) => (req, res, next) => {
  const dispatch = (i) => {
    if (i >= middlewares.length) return next();
    const middleware = middlewares[i];
    middleware(req, res, (err) => {
      if (err) return next(err);
      dispatch(i + 1);
    });
  };
  dispatch(0);
};

// Usage
const apiMiddleware = compose(
  requestId,
  logger,
  authenticate,
  rateLimiter({ max: 100 }),
  cors({ origin: allowedOrigins }),
);

app.use('/api', apiMiddleware);

// Conditional middleware
function when(predicate, ...middlewares) {
  return (req, res, next) => {
    if (predicate(req)) {
      return compose(...middlewares)(req, res, next);
    }
    next();
  };
}

app.use(when(
  (req) => req.path.startsWith('/api/admin'),
  authenticate,
  requireRole('admin'),
  auditLog,
));
```

---

## Quick Reference — Node.js & Express Cheat Sheet

### Event Loop Priority Order
```
1. Synchronous code (runs to completion before loop starts)
2. process.nextTick() queue (between every phase)
3. Promise microtask queue (after nextTick, before phases)
4. Timers phase: setTimeout, setInterval (expired timers)
5. Pending callbacks: some system errors
6. Idle/prepare: internal
7. Poll: new I/O events — executes I/O callbacks
8. Check: setImmediate()
9. Close callbacks: socket.on('close', ...)
```

### Stream Types
```
Readable:  source of data  → pipe to Writable or Transform
Writable:  sink for data   → written to by pipe or manual write()
Duplex:    read + write    → TCP socket (net.Socket)
Transform: read + modify   → compression (zlib), encryption, parsing
```

### HTTP Status Codes Reference
```
2xx Success:    200 OK, 201 Created, 204 No Content
3xx Redirect:   301 Permanent, 302 Temporary, 304 Not Modified
4xx Client:     400 Bad Request, 401 Unauthorized, 403 Forbidden,
                404 Not Found, 409 Conflict, 422 Unprocessable, 429 Too Many
5xx Server:     500 Internal Error, 502 Bad Gateway, 503 Unavailable
```

### Express Middleware Order
```
1. Security: helmet()
2. CORS: cors()
3. Body parsing: express.json(), express.urlencoded()
4. Static files: express.static()
5. Logging: morgan() or pinoHttp()
6. Session: session()
7. Request ID / timing
8. Rate limiting
9. Routes
10. 404 handler (after all routes)
11. Error handler (4-arg, last)
```

### Key npm Packages
```
HTTP framework:    express, fastify, koa, hono
Auth:              jsonwebtoken, passport, bcryptjs
DB — Postgres:     pg, drizzle-orm, prisma, knex
DB — MongoDB:      mongoose, mongodb
DB — ORM/Query:    sequelize, typeorm, objection
Cache/Queue:       redis, ioredis, bull, bullmq
Validation:        zod, joi, yup, express-validator
Logging:           pino, winston, morgan
Testing:           jest, supertest, vitest, mocha
Security:          helmet, cors, express-rate-limit, csurf
Uploads:           multer, busboy, formidable
WebSocket:         socket.io, ws
HTTP client:       axios, node-fetch, got, ky
Config:            dotenv, dotenv-safe, convict
Process:           pm2, nodemon, ts-node, tsx
```
