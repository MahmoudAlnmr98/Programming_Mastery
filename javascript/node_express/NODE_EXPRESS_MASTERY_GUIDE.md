# Complete Node.js & Express.js Mastery Guide

## Table of Contents
1. [Node.js Fundamentals](#nodejs-fundamentals)
2. [Node.js Core Modules](#nodejs-core-modules)
3. [File System Operations](#file-system-operations)
4. [Streams](#streams)
5. [Events & EventEmitter](#events--eventemitter)
6. [HTTP Module](#http-module)
7. [Asynchronous Programming](#asynchronous-programming)
8. [Modules & NPM](#modules--npm)
9. [Express.js Fundamentals](#expressjs-fundamentals)
10. [Routing](#routing)
11. [Middleware](#middleware)
12. [Request & Response](#request--response)
13. [Error Handling](#error-handling)
14. [Template Engines](#template-engines)
15. [Database Integration](#database-integration)
16. [Authentication & Security](#authentication--security)
17. [File Uploads](#file-uploads)
18. [API Development](#api-development)
19. [Testing](#testing)
20. [Performance Optimization](#performance-optimization)
21. [Deployment](#deployment)
22. [Best Practices](#best-practices)
23. [Advanced Topics](#advanced-topics)

---

## Node.js Fundamentals

### What is Node.js?
Node.js is a JavaScript runtime built on Chrome's V8 engine. It's:
- **Asynchronous**: Non-blocking I/O operations
- **Event-Driven**: Uses event loop for concurrency
- **Single-Threaded**: Uses event loop instead of threads
- **Cross-Platform**: Runs on Windows, macOS, Linux
- **NPM**: Package manager with vast ecosystem

### Installation
```bash
# Download from https://nodejs.org/
# Verify installation
node --version
npm --version

# Using nvm (Node Version Manager)
nvm install 20
nvm use 20
nvm list
```

### Hello World
```javascript
// app.js
console.log('Hello, World!');

// Run
node app.js
```

### REPL (Read-Eval-Print Loop)
```bash
# Start REPL
node

# In REPL
> console.log('Hello')
> 2 + 2
> .help
> .exit
```

### Node.js Architecture
```
Application Code
    ↓
Node.js API (JavaScript)
    ↓
V8 Engine (C++)
    ↓
libuv (C) - Event Loop
    ↓
Operating System
```

---

## Node.js Core Modules

### fs (File System)
```javascript
const fs = require('fs');

// Read file (synchronous)
const data = fs.readFileSync('file.txt', 'utf8');

// Read file (asynchronous)
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// Write file
fs.writeFile('output.txt', 'Hello', (err) => {
  if (err) throw err;
});

// Promises API
const fsPromises = require('fs').promises;
const data = await fsPromises.readFile('file.txt', 'utf8');
```

### path
```javascript
const path = require('path');

// Join paths
const fullPath = path.join(__dirname, 'public', 'index.html');

// Get directory name
const dir = path.dirname('/users/john/file.txt');

// Get filename
const file = path.basename('/users/john/file.txt');

// Get extension
const ext = path.extname('file.txt');

// Resolve path
const resolved = path.resolve('public', 'index.html');

// Parse path
const parsed = path.parse('/users/john/file.txt');
// { root: '/', dir: '/users/john', base: 'file.txt', ext: '.txt', name: 'file' }
```

### os
```javascript
const os = require('os');

os.platform();      // Operating system platform
os.arch();          // CPU architecture
os.cpus();          // CPU information
os.totalmem();      // Total memory
os.freemem();       // Free memory
os.hostname();      // Hostname
os.homedir();       // Home directory
os.tmpdir();        // Temp directory
```

### url
```javascript
const url = require('url');

// Parse URL
const parsed = url.parse('https://example.com/path?query=value#hash');

// Create URL
const myUrl = new URL('https://example.com/path?query=value#hash');
myUrl.hostname;     // 'example.com'
myUrl.pathname;     // '/path'
myUrl.search;       // '?query=value'
myUrl.searchParams.get('query'); // 'value'
```

### querystring
```javascript
const querystring = require('querystring');

// Parse query string
const parsed = querystring.parse('name=John&age=30');
// { name: 'John', age: '30' }

// Stringify
const str = querystring.stringify({ name: 'John', age: 30 });
// 'name=John&age=30'
```

### crypto
```javascript
const crypto = require('crypto');

// Hash
const hash = crypto.createHash('sha256');
hash.update('Hello');
hash.digest('hex');

// HMAC
const hmac = crypto.createHmac('sha256', 'secret');
hmac.update('Hello');
hmac.digest('hex');

// Random bytes
const random = crypto.randomBytes(16).toString('hex');

// Encryption
const cipher = crypto.createCipher('aes192', 'password');
let encrypted = cipher.update('Hello', 'utf8', 'hex');
encrypted += cipher.final('hex');
```

### util
```javascript
const util = require('util');

// Promisify callback function
const readFile = util.promisify(fs.readFile);

// Inspect object
util.inspect(obj, { depth: null });

// Inherit
util.inherits(Child, Parent);

// Format
util.format('%s:%s', 'foo', 'bar');
```

---

## File System Operations

### Reading Files
```javascript
const fs = require('fs');

// Synchronous
try {
  const data = fs.readFileSync('file.txt', 'utf8');
  console.log(data);
} catch (err) {
  console.error(err);
}

// Asynchronous
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
});

// Promises
const fsPromises = require('fs').promises;
async function readFile() {
  try {
    const data = await fsPromises.readFile('file.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

### Writing Files
```javascript
// Write file
fs.writeFile('output.txt', 'Hello', (err) => {
  if (err) throw err;
});

// Append to file
fs.appendFile('output.txt', 'World', (err) => {
  if (err) throw err;
});

// Write file sync
fs.writeFileSync('output.txt', 'Hello');
```

### Directory Operations
```javascript
// Create directory
fs.mkdir('newdir', (err) => {
  if (err) throw err;
});

// Read directory
fs.readdir('.', (err, files) => {
  if (err) throw err;
  files.forEach(file => {
    console.log(file);
  });
});

// Remove directory
fs.rmdir('dir', (err) => {
  if (err) throw err;
});

// Check if path exists
fs.access('file.txt', fs.constants.F_OK, (err) => {
  if (err) {
    console.log('File does not exist');
  } else {
    console.log('File exists');
  }
});
```

### File Stats
```javascript
fs.stat('file.txt', (err, stats) => {
  if (err) throw err;
  console.log(stats.isFile());
  console.log(stats.isDirectory());
  console.log(stats.size);
  console.log(stats.mtime);
});
```

---

## Streams

### Readable Stream
```javascript
const fs = require('fs');

const readable = fs.createReadStream('large-file.txt', 'utf8');

readable.on('data', (chunk) => {
  console.log('Received chunk:', chunk);
});

readable.on('end', () => {
  console.log('Finished reading');
});

readable.on('error', (err) => {
  console.error('Error:', err);
});
```

### Writable Stream
```javascript
const writable = fs.createWriteStream('output.txt');

writable.write('Hello\n');
writable.write('World\n');
writable.end();
```

### Piping Streams
```javascript
const fs = require('fs');

// Pipe readable to writable
fs.createReadStream('input.txt')
  .pipe(fs.createWriteStream('output.txt'));

// With transform
const { Transform } = require('stream');

const upperCase = new Transform({
  transform(chunk, encoding, callback) {
    callback(null, chunk.toString().toUpperCase());
  }
});

fs.createReadStream('input.txt')
  .pipe(upperCase)
  .pipe(fs.createWriteStream('output.txt'));
```

### Stream Types
```javascript
// Readable
const { Readable } = require('stream');
const readable = new Readable({
  read() {
    this.push('Hello');
    this.push(null); // End stream
  }
});

// Writable
const { Writable } = require('stream');
const writable = new Writable({
  write(chunk, encoding, callback) {
    console.log(chunk.toString());
    callback();
  }
});

// Duplex
const { Duplex } = require('stream');
const duplex = new Duplex({
  read() { /* ... */ },
  write(chunk, encoding, callback) { /* ... */ }
});

// Transform
const { Transform } = require('stream');
const transform = new Transform({
  transform(chunk, encoding, callback) {
    callback(null, chunk.toString().toUpperCase());
  }
});
```

---

## Events & EventEmitter

### EventEmitter
```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const myEmitter = new MyEmitter();

// Listen to event
myEmitter.on('event', () => {
  console.log('Event occurred');
});

// Emit event
myEmitter.emit('event');

// With data
myEmitter.on('data', (data) => {
  console.log('Received:', data);
});

myEmitter.emit('data', 'Hello');
```

### Event Methods
```javascript
// Once (listen only once)
myEmitter.once('event', () => {
  console.log('This will only fire once');
});

// Remove listener
const callback = () => console.log('Event');
myEmitter.on('event', callback);
myEmitter.removeListener('event', callback);

// Remove all listeners
myEmitter.removeAllListeners('event');

// Get listener count
myEmitter.listenerCount('event');

// Get listeners
myEmitter.listeners('event');
```

### Error Events
```javascript
// Error events are special
myEmitter.on('error', (err) => {
  console.error('Error:', err);
});

// If no error listener, process will crash
myEmitter.emit('error', new Error('Something went wrong'));
```

---

## HTTP Module

### Creating HTTP Server
```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello, World!');
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Request & Response
```javascript
const server = http.createServer((req, res) => {
  // Request
  console.log(req.method);      // GET, POST, etc.
  console.log(req.url);         // /path?query=value
  console.log(req.headers);     // Request headers

  // Response
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.write('<h1>Hello</h1>');
  res.end();
});
```

### HTTP Client
```javascript
const http = require('http');

const options = {
  hostname: 'example.com',
  port: 80,
  path: '/',
  method: 'GET'
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  res.on('data', (chunk) => {
    console.log(chunk.toString());
  });
});

req.on('error', (err) => {
  console.error(err);
});

req.end();
```

### HTTPS
```javascript
const https = require('https');

https.get('https://api.example.com/data', (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    console.log(JSON.parse(data));
  });
}).on('error', (err) => {
  console.error(err);
});
```

---

## Asynchronous Programming

### Callbacks
```javascript
// Callback pattern
function readFile(callback) {
  fs.readFile('file.txt', 'utf8', (err, data) => {
    if (err) return callback(err);
    callback(null, data);
  });
}

readFile((err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
});
```

### Promises
```javascript
// Creating promise
function readFilePromise() {
  return new Promise((resolve, reject) => {
    fs.readFile('file.txt', 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// Using promise
readFilePromise()
  .then(data => console.log(data))
  .catch(err => console.error(err));

// Promise.all
Promise.all([promise1, promise2, promise3])
  .then(results => {
    console.log(results);
  })
  .catch(err => {
    console.error(err);
  });
```

### async/await
```javascript
async function readFile() {
  try {
    const data = await fsPromises.readFile('file.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}

// Multiple async operations
async function fetchData() {
  try {
    const [data1, data2] = await Promise.all([
      fetchData1(),
      fetchData2()
    ]);
    return { data1, data2 };
  } catch (err) {
    console.error(err);
  }
}
```

---

## Modules & NPM

### CommonJS Modules
```javascript
// math.js
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = {
  add,
  subtract
};

// Or
exports.add = add;
exports.subtract = subtract;

// app.js
const math = require('./math');
console.log(math.add(2, 3));
```

### ES6 Modules (Node.js 14+)
```javascript
// math.mjs
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

// app.mjs
import { add, subtract } from './math.mjs';
console.log(add(2, 3));
```

### NPM Packages
```bash
# Initialize package
npm init
npm init -y  # Skip questions

# Install package
npm install express
npm install express --save-dev  # Dev dependency
npm install express --global    # Global install

# Install from package.json
npm install

# Update package
npm update express

# Uninstall
npm uninstall express

# List packages
npm list
npm list --depth=0
```

### package.json
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "My application",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0"
  },
  "devDependencies": {
    "nodemon": "^2.0.0"
  }
}
```

---

## Express.js Fundamentals

### Installation & Setup
```bash
npm install express
```

### Basic Express App
```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Express Generator
```bash
npx express-generator my-app
cd my-app
npm install
npm start
```

### Application Structure
```
my-app/
├── routes/
│   ├── index.js
│   └── users.js
├── views/
│   └── index.ejs
├── public/
│   ├── css/
│   ├── js/
│   └── images/
├── app.js
└── package.json
```

---

## Routing

### Basic Routes
```javascript
// GET request
app.get('/', (req, res) => {
  res.send('GET request');
});

// POST request
app.post('/', (req, res) => {
  res.send('POST request');
});

// PUT request
app.put('/user/:id', (req, res) => {
  res.send(`Update user ${req.params.id}`);
});

// DELETE request
app.delete('/user/:id', (req, res) => {
  res.send(`Delete user ${req.params.id}`);
});

// All HTTP methods
app.all('/secret', (req, res) => {
  res.send('Secret route');
});
```

### Route Parameters
```javascript
// Single parameter
app.get('/user/:id', (req, res) => {
  res.send(`User ID: ${req.params.id}`);
});

// Multiple parameters
app.get('/user/:userId/post/:postId', (req, res) => {
  res.send(`User: ${req.params.userId}, Post: ${req.params.postId}`);
});

// Optional parameter
app.get('/user/:id?', (req, res) => {
  if (req.params.id) {
    res.send(`User ID: ${req.params.id}`);
  } else {
    res.send('All users');
  }
});
```

### Query Parameters
```javascript
app.get('/search', (req, res) => {
  const query = req.query;
  res.json(query);
  // GET /search?q=nodejs&page=1
  // { q: 'nodejs', page: '1' }
});
```

### Route Handlers
```javascript
// Single handler
app.get('/', (req, res) => {
  res.send('Hello');
});

// Multiple handlers
app.get('/',
  (req, res, next) => {
    console.log('First handler');
    next();
  },
  (req, res) => {
    res.send('Second handler');
  }
);

// Array of handlers
const handlers = [
  (req, res, next) => { console.log('Handler 1'); next(); },
  (req, res, next) => { console.log('Handler 2'); next(); },
  (req, res) => { res.send('Handler 3'); }
];
app.get('/', handlers);
```

### Route Modules
```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.send('Users list');
});

router.get('/:id', (req, res) => {
  res.send(`User ${req.params.id}`);
});

module.exports = router;

// app.js
const usersRouter = require('./routes/users');
app.use('/users', usersRouter);
```

---

## Middleware

### What is Middleware?
Middleware functions have access to request, response, and next function.

### Basic Middleware
```javascript
// Application-level middleware
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// Route-specific middleware
app.use('/user/:id', (req, res, next) => {
  console.log('Request Type:', req.method);
  next();
});

// Multiple middleware
app.use((req, res, next) => {
  console.log('First middleware');
  next();
}, (req, res, next) => {
  console.log('Second middleware');
  next();
});
```

### Built-in Middleware
```javascript
// Parse JSON bodies
app.use(express.json());

// Parse URL-encoded bodies
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static('public'));

// Multiple static directories
app.use(express.static('public'));
app.use(express.static('files'));
```

### Third-party Middleware
```javascript
// CORS
const cors = require('cors');
app.use(cors());

// Helmet (security)
const helmet = require('helmet');
app.use(helmet());

// Morgan (logging)
const morgan = require('morgan');
app.use(morgan('combined'));

// Cookie parser
const cookieParser = require('cookie-parser');
app.use(cookieParser());
```

### Custom Middleware
```javascript
// Logger middleware
function logger(req, res, next) {
  console.log(`${req.method} ${req.url} - ${new Date()}`);
  next();
}

app.use(logger);

// Authentication middleware
function authenticate(req, res, next) {
  const token = req.headers.authorization;
  if (token === 'valid-token') {
    next();
  } else {
    res.status(401).send('Unauthorized');
  }
}

app.get('/protected', authenticate, (req, res) => {
  res.send('Protected route');
});
```

### Error Handling Middleware
```javascript
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Using with async
app.get('/', async (req, res, next) => {
  try {
    const data = await someAsyncOperation();
    res.send(data);
  } catch (err) {
    next(err);
  }
});
```

---

## Request & Response

### Request Object
```javascript
app.get('/', (req, res) => {
  // Properties
  req.app;           // Express app instance
  req.baseUrl;       // Base URL
  req.body;          // Request body (with body-parser)
  req.cookies;       // Cookies (with cookie-parser)
  req.fresh;         // If response is fresh
  req.hostname;      // Hostname
  req.ip;            // IP address
  req.ips;           // IP addresses
  req.method;        // HTTP method
  req.originalUrl;    // Original URL
  req.params;        // Route parameters
  req.path;          // Path portion
  req.protocol;      // Protocol (http/https)
  req.query;         // Query string parameters
  req.route;         // Matched route
  req.secure;        // If HTTPS
  req.signedCookies; // Signed cookies
  req.stale;         // If response is stale
  req.subdomains;    // Subdomains
  req.xhr;           // If XMLHttpRequest
});
```

### Response Object
```javascript
app.get('/', (req, res) => {
  // Methods
  res.send('Hello');                    // Send response
  res.json({ message: 'Hello' });       // Send JSON
  res.status(404).send('Not Found');    // Set status and send
  res.redirect('/other-route');         // Redirect
  res.render('view', { data });         // Render template
  res.sendFile('/path/to/file');        // Send file
  res.download('/path/to/file');        // Download file
  res.end();                            // End response
  res.set('Content-Type', 'text/html'); // Set header
  res.cookie('name', 'value');          // Set cookie
  res.clearCookie('name');              // Clear cookie
  res.location('/foo/bar');            // Set Location header
  res.type('text/html');               // Set Content-Type
});
```

### Request Body Parsing
```javascript
// JSON
app.use(express.json());
app.post('/user', (req, res) => {
  console.log(req.body);
  res.json(req.body);
});

// URL-encoded
app.use(express.urlencoded({ extended: true }));
app.post('/form', (req, res) => {
  console.log(req.body);
  res.json(req.body);
});

// Raw
app.use(express.raw({ type: 'application/octet-stream' }));

// Text
app.use(express.text({ type: 'text/plain' }));
```

---

## Error Handling

### Basic Error Handling
```javascript
// Synchronous errors
app.get('/', (req, res) => {
  throw new Error('Something went wrong');
});

// Asynchronous errors
app.get('/', async (req, res, next) => {
  try {
    const data = await someAsyncOperation();
    res.send(data);
  } catch (err) {
    next(err);
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

### Custom Error Handler
```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Usage
app.get('/user/:id', async (req, res, next) => {
  const user = await findUser(req.params.id);
  if (!user) {
    return next(new AppError('User not found', 404));
  }
  res.json(user);
});

// Error handler
app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  res.status(err.statusCode).json({
    status: err.status,
    message: err.message
  });
});
```

### Async Error Wrapper
```javascript
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
app.get('/user/:id', asyncHandler(async (req, res) => {
  const user = await findUser(req.params.id);
  if (!user) {
    throw new AppError('User not found', 404);
  }
  res.json(user);
}));
```

---

## Template Engines

### EJS
```javascript
// Install: npm install ejs

app.set('view engine', 'ejs');
app.set('views', './views');

app.get('/', (req, res) => {
  res.render('index', { title: 'Home', users: [] });
});

// views/index.ejs
<h1><%= title %></h1>
<ul>
  <% users.forEach(user => { %>
    <li><%= user.name %></li>
  <% }); %>
</ul>
```

### Handlebars
```javascript
// Install: npm install express-handlebars

const exphbs = require('express-handlebars');
app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');

app.get('/', (req, res) => {
  res.render('index', { title: 'Home' });
});
```

### Pug
```javascript
// Install: npm install pug

app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', (req, res) => {
  res.render('index', { title: 'Home' });
});

// views/index.pug
h1= title
p Welcome to #{title}
```

---

## Database Integration

### MongoDB with Mongoose
```javascript
// Install: npm install mongoose

const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/myapp');

// Schema
const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  age: Number
});

// Model
const User = mongoose.model('User', userSchema);

// Create
const user = new User({ name: 'John', email: 'john@example.com' });
await user.save();

// Find
const users = await User.find();
const user = await User.findById(id);

// Update
await User.findByIdAndUpdate(id, { name: 'Jane' });

// Delete
await User.findByIdAndDelete(id);
```

### PostgreSQL with pg
```javascript
// Install: npm install pg

const { Pool } = require('pg');
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'myapp',
  password: 'password',
  port: 5432,
});

// Query
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### MySQL with mysql2
```javascript
// Install: npm install mysql2

const mysql = require('mysql2/promise');
const connection = await mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'myapp'
});

// Query
const [rows] = await connection.execute('SELECT * FROM users WHERE id = ?', [userId]);
```

---

## Authentication & Security

### JWT Authentication
```javascript
// Install: npm install jsonwebtoken bcryptjs

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// Register
app.post('/register', async (req, res) => {
  const hashedPassword = await bcrypt.hash(req.body.password, 10);
  const user = await User.create({
    email: req.body.email,
    password: hashedPassword
  });
  res.json(user);
});

// Login
app.post('/login', async (req, res) => {
  const user = await User.findOne({ email: req.body.email });
  if (!user) return res.status(401).send('Invalid credentials');
  
  const valid = await bcrypt.compare(req.body.password, user.password);
  if (!valid) return res.status(401).send('Invalid credentials');
  
  const token = jwt.sign({ userId: user._id }, 'secret-key');
  res.json({ token });
});

// Protect route
function authenticateToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];
  if (!token) return res.status(401).send('Access denied');
  
  jwt.verify(token, 'secret-key', (err, user) => {
    if (err) return res.status(403).send('Invalid token');
    req.user = user;
    next();
  });
}

app.get('/protected', authenticateToken, (req, res) => {
  res.send('Protected route');
});
```

### Security Best Practices
```javascript
// Helmet
const helmet = require('helmet');
app.use(helmet());

// CORS
const cors = require('cors');
app.use(cors({
  origin: 'https://example.com',
  credentials: true
}));

// Rate limiting
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Input validation
const { body, validationResult } = require('express-validator');
app.post('/user',
  body('email').isEmail(),
  body('password').isLength({ min: 6 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);
```

---

## File Uploads

### Multer
```javascript
// Install: npm install multer

const multer = require('multer');

// Configure storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

// Single file
app.post('/upload', upload.single('file'), (req, res) => {
  res.json({ file: req.file });
});

// Multiple files
app.post('/upload', upload.array('files', 10), (req, res) => {
  res.json({ files: req.files });
});

// Multiple fields
app.post('/upload', upload.fields([
  { name: 'avatar', maxCount: 1 },
  { name: 'gallery', maxCount: 8 }
]), (req, res) => {
  res.json({ files: req.files });
});
```

---

## API Development

### RESTful API
```javascript
// GET /api/users - Get all users
app.get('/api/users', async (req, res) => {
  const users = await User.find();
  res.json(users);
});

// GET /api/users/:id - Get user by ID
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

// POST /api/users - Create user
app.post('/api/users', async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});

// PUT /api/users/:id - Update user
app.put('/api/users/:id', async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true }
  );
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json(user);
});

// DELETE /api/users/:id - Delete user
app.delete('/api/users/:id', async (req, res) => {
  const user = await User.findByIdAndDelete(req.params.id);
  if (!user) return res.status(404).json({ error: 'User not found' });
  res.json({ message: 'User deleted' });
});
```

### API Versioning
```javascript
// Version 1
app.use('/api/v1/users', usersRouterV1);

// Version 2
app.use('/api/v2/users', usersRouterV2);
```

### API Documentation (Swagger)
```javascript
// Install: npm install swagger-jsdoc swagger-ui-express

const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0',
    },
  },
  apis: ['./routes/*.js'],
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
```

---

## Testing

### Jest
```javascript
// Install: npm install --save-dev jest supertest

const request = require('supertest');
const app = require('./app');

describe('GET /api/users', () => {
  test('should return all users', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200);
    
    expect(response.body).toBeInstanceOf(Array);
  });
});

describe('POST /api/users', () => {
  test('should create a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201);
    
    expect(response.body).toHaveProperty('_id');
  });
});
```

### Mocha & Chai
```javascript
// Install: npm install --save-dev mocha chai

const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('./app');

chai.use(chaiHttp);
const expect = chai.expect;

describe('API Tests', () => {
  it('should get all users', (done) => {
    chai.request(app)
      .get('/api/users')
      .end((err, res) => {
        expect(res).to.have.status(200);
        expect(res.body).to.be.an('array');
        done();
      });
  });
});
```

---

## Performance Optimization

### Caching
```javascript
// Memory cache
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 });

app.get('/api/users', async (req, res) => {
  const cacheKey = 'users';
  const cached = cache.get(cacheKey);
  
  if (cached) {
    return res.json(cached);
  }
  
  const users = await User.find();
  cache.set(cacheKey, users);
  res.json(users);
});
```

### Compression
```javascript
// Install: npm install compression

const compression = require('compression');
app.use(compression());
```

### Clustering
```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  // Worker process
  const app = require('./app');
  app.listen(3000);
}
```

### Database Connection Pooling
```javascript
const { Pool } = require('pg');
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

---

## Deployment

### Environment Variables
```javascript
// Install: npm install dotenv

require('dotenv').config();

const PORT = process.env.PORT || 3000;
const DB_URL = process.env.DB_URL;
```

### PM2
```bash
# Install: npm install -g pm2

# Start app
pm2 start app.js

# Start with name
pm2 start app.js --name my-app

# List processes
pm2 list

# Stop process
pm2 stop my-app

# Restart
pm2 restart my-app

# Delete
pm2 delete my-app

# Monitor
pm2 monit

# Logs
pm2 logs
```

### Docker
```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

### Production Checklist
- [ ] Set NODE_ENV=production
- [ ] Use environment variables
- [ ] Enable compression
- [ ] Set up logging
- [ ] Configure CORS properly
- [ ] Use HTTPS
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Use process manager (PM2)
- [ ] Set up error tracking

---

## Best Practices

### Code Organization
```javascript
// app.js
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/users', require('./routes/users'));
app.use('/api/posts', require('./routes/posts'));

// Error handling
app.use(require('./middleware/errorHandler'));

module.exports = app;
```

### Error Handling
```javascript
// Always handle errors
app.get('/user/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    next(err);
  }
});
```

### Security
```javascript
// Use helmet
app.use(helmet());

// Validate input
app.use(express.json({ limit: '10kb' }));

// Sanitize input
const mongoSanitize = require('express-mongo-sanitize');
app.use(mongoSanitize());

// Prevent XSS
const xss = require('xss-clean');
app.use(xss());
```

### Performance
```javascript
// Enable compression
app.use(compression());

// Cache static files
app.use(express.static('public', {
  maxAge: '1d'
}));

// Use connection pooling
// Optimize database queries
// Use indexes
```

---

## Advanced Topics

### WebSockets (Socket.io)
```javascript
// Install: npm install socket.io

const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', (socket) => {
  console.log('User connected');
  
  socket.on('message', (data) => {
    io.emit('message', data);
  });
  
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

server.listen(3000);
```

### GraphQL
```javascript
// Install: npm install express-graphql graphql

const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

const schema = buildSchema(`
  type Query {
    hello: String
  }
`);

const root = {
  hello: () => 'Hello, World!'
};

app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true
}));
```

### Microservices
```javascript
// Service 1
const express = require('express');
const app = express();

app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});

app.listen(3001);

// Service 2
app.get('/api/posts', (req, res) => {
  res.json({ posts: [] });
});

app.listen(3002);
```

### Serverless (AWS Lambda)
```javascript
// serverless.yml
service: my-service
provider:
  name: aws
  runtime: nodejs18.x
functions:
  api:
    handler: handler.api
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

---

## Resources for Further Learning

1. **Node.js Official Documentation** - https://nodejs.org/docs
2. **Express.js Official Documentation** - https://expressjs.com
3. **Node.js Best Practices** - https://github.com/goldbergyoni/nodebestpractices
4. **Express Security Best Practices** - Security guidelines
5. **Awesome Node.js** - Curated list of Node.js resources
6. **Node.js Weekly** - Newsletter
7. **Express Examples** - Official examples
8. **Node.js Design Patterns** - Book by Mario Casciaro

---

## Conclusion

This guide covers Node.js and Express.js from fundamentals to advanced topics. Mastery comes through:
- **Practice**: Build projects, solve problems
- **Understanding**: Know why, not just how
- **Reading**: Study well-written Node.js/Express code
- **Teaching**: Explain concepts to others
- **Staying Current**: Follow Node.js/Express evolution

Remember: Node.js emphasizes asynchronous, event-driven programming. Express.js provides a minimal, flexible web framework. Keep learning, keep practicing, and keep building!

### Key Takeaways
- Node.js is asynchronous and event-driven
- Express.js is a minimal, flexible web framework
- Master middleware and routing
- Understand async/await and promises
- Use proper error handling
- Follow security best practices
- Optimize for performance
- Test your applications
- Deploy properly

