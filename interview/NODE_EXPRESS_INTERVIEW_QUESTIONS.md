# Node.js & Express.js Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Node.js? Explain its key features.

**Answer:**
Node.js is a JavaScript runtime built on Chrome's V8 engine.

**Key Features:**
- **Asynchronous**: Non-blocking I/O operations
- **Event-Driven**: Uses event loop for concurrency
- **Single-Threaded**: Uses event loop instead of threads
- **Cross-Platform**: Runs on Windows, macOS, Linux
- **NPM**: Package manager with vast ecosystem

### 2. Explain the event loop in Node.js.

**Answer:**
Event loop handles asynchronous operations.

**Phases:**
1. **Timers**: Execute callbacks scheduled by setTimeout/setInterval
2. **Pending Callbacks**: Execute I/O callbacks deferred to next loop
3. **Idle, Prepare**: Internal use
4. **Poll**: Fetch new I/O events
5. **Check**: Execute setImmediate callbacks
6. **Close Callbacks**: Execute close callbacks

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);
setImmediate(() => console.log("3"));
process.nextTick(() => console.log("4"));

console.log("5");

// Output: 1, 5, 4, 2, 3
// process.nextTick runs before event loop phases
```

### 3. What is the difference between `require` and `import`?

**Answer:**
- **require**: CommonJS (Node.js default), synchronous, dynamic
- **import**: ES6 modules, asynchronous, static

```javascript
// CommonJS
const express = require('express');
module.exports = {};

// ES6 Modules
import express from 'express';
export default {};
```

### 4. Explain Express.js middleware.

**Answer:**
Middleware functions execute during request-response cycle.

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

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});
```

### 5. Explain the difference between `app.get()` and `app.use()`.

**Answer:**
- **app.get()**: Handles GET requests for specific route
- **app.use()**: Mounts middleware or handles all HTTP methods

```javascript
// app.get - only GET requests
app.get('/users', (req, res) => {
    res.send('Get users');
});

// app.use - all HTTP methods
app.use('/users', (req, res) => {
    res.send('Any method');
});
```

### 6. What is the difference between `res.send()`, `res.json()`, and `res.end()`?

**Answer:**
- **res.send()**: Sends response (auto-detects type)
- **res.json()**: Sends JSON response
- **res.end()**: Ends response without data

```javascript
res.send('Hello');           // Text
res.send({name: 'John'});    // JSON
res.json({name: 'John'});    // JSON (explicit)
res.end();                    // End without data
```

### 7. Explain Express routing.

**Answer:**
Routing determines how application responds to client requests.

```javascript
// Basic route
app.get('/', (req, res) => {
    res.send('Home');
});

// Route parameters
app.get('/user/:id', (req, res) => {
    res.send(`User ${req.params.id}`);
});

// Query parameters
app.get('/search', (req, res) => {
    res.json(req.query); // ?q=nodejs
});

// Route modules
const router = express.Router();
router.get('/', (req, res) => {
    res.send('Users');
});
app.use('/users', router);
```

---

## Intermediate Level

### 8. Explain async/await in Node.js.

**Answer:**
Async/await provides cleaner syntax for promises.

```javascript
// Promises
function fetchData() {
    return fetch('https://api.example.com/data')
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.error(err));
}

// Async/await
async function fetchData() {
    try {
        const res = await fetch('https://api.example.com/data');
        const data = await res.json();
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}

// Express with async/await
app.get('/users/:id', async (req, res, next) => {
    try {
        const user = await User.findById(req.params.id);
        res.json(user);
    } catch (err) {
        next(err);
    }
});
```

### 9. Explain error handling in Express.

**Answer:**
**Synchronous Errors:**
```javascript
app.get('/', (req, res) => {
    throw new Error('Something went wrong');
});
```

**Asynchronous Errors:**
```javascript
app.get('/users/:id', async (req, res, next) => {
    try {
        const user = await User.findById(req.params.id);
        res.json(user);
    } catch (err) {
        next(err); // Pass to error handler
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});
```

**Custom Error Handler:**
```javascript
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
    }
}

app.use((err, req, res, next) => {
    err.statusCode = err.statusCode || 500;
    res.status(err.statusCode).json({
        status: 'error',
        message: err.message
    });
});
```

### 10. Explain streams in Node.js.

**Answer:**
Streams handle data in chunks, efficient for large data.

**Types:**
- **Readable**: Read data
- **Writable**: Write data
- **Duplex**: Read and write
- **Transform**: Modify data while reading/writing

```javascript
const fs = require('fs');

// Readable stream
const readable = fs.createReadStream('large-file.txt');
readable.on('data', (chunk) => {
    console.log(chunk);
});

// Writable stream
const writable = fs.createWriteStream('output.txt');
writable.write('Hello\n');
writable.end();

// Piping
fs.createReadStream('input.txt')
    .pipe(fs.createWriteStream('output.txt'));
```

### 11. Explain clustering in Node.js.

**Answer:**
Clustering allows Node.js to use multiple CPU cores.

```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    // Fork workers
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
    
    cluster.on('exit', (worker) => {
        console.log('Worker died');
        cluster.fork(); // Restart
    });
} else {
    // Worker process
    const express = require('express');
    const app = express();
    app.listen(3000);
}
```

### 12. Explain JWT authentication in Express.

**Answer:**
JWT (JSON Web Token) for stateless authentication.

```javascript
const jwt = require('jsonwebtoken');

// Generate token
app.post('/login', (req, res) => {
    const user = { id: 1, username: 'john' };
    const token = jwt.sign(user, 'secret-key', { expiresIn: '1h' });
    res.json({ token });
});

// Verify token
function authenticateToken(req, res, next) {
    const token = req.headers['authorization']?.split(' ')[1];
    
    if (!token) {
        return res.status(401).send('Access denied');
    }
    
    jwt.verify(token, 'secret-key', (err, user) => {
        if (err) return res.status(403).send('Invalid token');
        req.user = user;
        next();
    });
}

// Protected route
app.get('/protected', authenticateToken, (req, res) => {
    res.json({ message: 'Protected data', user: req.user });
});
```

### 13. Explain file uploads with Multer.

**Answer:**
Multer handles multipart/form-data for file uploads.

```javascript
const multer = require('multer');

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
```

### 14. Explain RESTful API design.

**Answer:**
REST (Representational State Transfer) principles.

**HTTP Methods:**
- GET: Retrieve resource
- POST: Create resource
- PUT: Update resource (full)
- PATCH: Update resource (partial)
- DELETE: Delete resource

```javascript
// RESTful routes
app.get('/api/users', getUsers);           // Get all
app.get('/api/users/:id', getUser);        // Get one
app.post('/api/users', createUser);        // Create
app.put('/api/users/:id', updateUser);      // Update
app.delete('/api/users/:id', deleteUser);  // Delete
```

**Best Practices:**
- Use nouns for resources
- Use HTTP status codes
- Version APIs
- Use query parameters for filtering

---

## Advanced Level

### 15. Explain middleware chaining and execution order.

**Answer:**
Middleware executes in order they're defined.

```javascript
app.use((req, res, next) => {
    console.log('1');
    next();
});

app.use((req, res, next) => {
    console.log('2');
    next();
});

app.get('/', (req, res) => {
    console.log('3');
    res.send('Done');
});

// Output: 1, 2, 3
```

**Error in Middleware:**
```javascript
app.use((req, res, next) => {
    try {
        // code
    } catch (err) {
        next(err); // Pass to error handler
    }
});
```

### 16. Explain Express.js performance optimization.

**Answer:**
**Techniques:**
1. **Compression**: Gzip responses
2. **Caching**: Cache responses
3. **Clustering**: Use multiple processes
4. **Database Connection Pooling**: Reuse connections
5. **Async Operations**: Don't block event loop

```javascript
const compression = require('compression');
app.use(compression());

// Caching
const cache = require('memory-cache');
app.get('/api/data', (req, res) => {
    const cached = cache.get('data');
    if (cached) {
        return res.json(cached);
    }
    const data = fetchData();
    cache.put('data', data, 60000); // 1 minute
    res.json(data);
});
```

### 17. Explain WebSockets with Socket.io.

**Answer:**
WebSockets for real-time bidirectional communication.

```javascript
const http = require('http');
const socketIo = require('socket.io');

const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', (socket) => {
    console.log('User connected');
    
    socket.on('message', (data) => {
        io.emit('message', data); // Broadcast to all
    });
    
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

server.listen(3000);
```

### 18. Explain GraphQL with Express.

**Answer:**
GraphQL provides flexible API queries.

```javascript
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

const schema = buildSchema(`
    type Query {
        hello: String
        user(id: ID!): User
    }
    type User {
        id: ID!
        name: String
    }
`);

const root = {
    hello: () => 'Hello World!',
    user: ({ id }) => getUserById(id)
};

app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true
}));
```

### 19. Explain microservices architecture with Express.

**Answer:**
Breaking application into independent services.

```javascript
// Service 1 - User Service
const express = require('express');
const app = express();

app.get('/api/users', (req, res) => {
    res.json({ users: [] });
});

app.listen(3001);

// Service 2 - Order Service
app.get('/api/orders', (req, res) => {
    res.json({ orders: [] });
});

app.listen(3002);

// API Gateway
app.use('/users', proxy('http://localhost:3001'));
app.use('/orders', proxy('http://localhost:3002'));
```

### 20. Explain testing Express applications.

**Answer:**
**Testing with Jest and Supertest:**

```javascript
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
    test('should create user', async () => {
        const response = await request(app)
            .post('/api/users')
            .send({ name: 'John', email: 'john@example.com' })
            .expect(201);
        
        expect(response.body).toHaveProperty('id');
    });
});
```

### 21. Explain security best practices in Express.

**Answer:**
**Security Measures:**
1. **Helmet**: Security headers
2. **CORS**: Cross-origin resource sharing
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize inputs
5. **HTTPS**: Encrypt traffic

```javascript
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

app.use(helmet());
app.use(cors({
    origin: 'https://example.com'
}));

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests
});
app.use('/api/', limiter);
```

### 22. Explain database integration with Express.

**Answer:**
**MongoDB with Mongoose:**
```javascript
const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost:27017/myapp');

const userSchema = new mongoose.Schema({
    name: String,
    email: String
});

const User = mongoose.model('User', userSchema);

app.get('/api/users', async (req, res) => {
    const users = await User.find();
    res.json(users);
});
```

**PostgreSQL with pg:**
```javascript
const { Pool } = require('pg');
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'myapp',
    password: 'password'
});

app.get('/api/users', async (req, res) => {
    const result = await pool.query('SELECT * FROM users');
    res.json(result.rows);
});
```

### 23. Explain session management in Express.

**Answer:**
**Using express-session:**
```javascript
const session = require('express-session');

app.use(session({
    secret: 'secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: true, maxAge: 60000 }
}));

app.post('/login', (req, res) => {
    req.session.userId = user.id;
    res.send('Logged in');
});

app.get('/profile', (req, res) => {
    if (req.session.userId) {
        res.send('Profile');
    } else {
        res.redirect('/login');
    }
});
```

### 24. Explain API versioning in Express.

**Answer:**
**URL Versioning:**
```javascript
app.use('/api/v1/users', usersRouterV1);
app.use('/api/v2/users', usersRouterV2);
```

**Header Versioning:**
```javascript
app.use('/api/users', (req, res, next) => {
    const version = req.headers['api-version'];
    if (version === 'v1') {
        return usersRouterV1(req, res, next);
    }
    return usersRouterV2(req, res, next);
});
```

### 25. Explain deployment best practices.

**Answer:**
**Environment Variables:**
```javascript
require('dotenv').config();

const PORT = process.env.PORT || 3000;
const DB_URL = process.env.DB_URL;
```

**PM2 Process Manager:**
```bash
pm2 start app.js
pm2 start app.js --name my-app
pm2 list
pm2 restart my-app
```

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

**Best Practices:**
- Use environment variables
- Enable compression
- Set up logging
- Use process manager (PM2)
- Enable HTTPS
- Set up monitoring

### 26. Explain Node.js Buffer and Streams in detail.

**Answer:**
**Buffer:**
```javascript
// Create buffer
const buf = Buffer.from('Hello', 'utf8');
const buf2 = Buffer.alloc(10);
const buf3 = Buffer.allocUnsafe(10);

// Buffer operations
buf.toString('utf8');
buf.write('World', 0);
buf.slice(0, 5);
```

**Streams:**
```javascript
const { Readable, Writable, Transform, Duplex } = require('stream');

// Custom readable stream
class MyReadable extends Readable {
    constructor(options) {
        super(options);
        this.index = 0;
    }
    
    _read() {
        if (this.index < 10) {
            this.push(String(this.index++));
        } else {
            this.push(null);
        }
    }
}

// Piping streams
readableStream
    .pipe(transformStream)
    .pipe(writableStream);
```

### 27. Explain Node.js child processes.

**Answer:**
**spawn:**
```javascript
const { spawn } = require('child_process');

const child = spawn('ls', ['-la']);
child.stdout.on('data', (data) => {
    console.log(data.toString());
});
```

**exec:**
```javascript
const { exec } = require('child_process');

exec('ls -la', (error, stdout, stderr) => {
    if (error) {
        console.error(error);
        return;
    }
    console.log(stdout);
});
```

**fork:**
```javascript
const { fork } = require('child_process');
const child = fork('child.js');
child.send({ message: 'Hello' });
child.on('message', (msg) => {
    console.log('From child:', msg);
});
```

### 28. Explain Node.js EventEmitter in detail.

**Answer:**
```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}

const emitter = new MyEmitter();

// Listen to event
emitter.on('event', (data) => {
    console.log('Event received:', data);
});

// Emit event
emitter.emit('event', 'Hello');

// Once (fires only once)
emitter.once('event', () => {
    console.log('Fired once');
});

// Remove listener
emitter.removeListener('event', handler);

// Remove all listeners
emitter.removeAllListeners('event');
```

### 29. Explain Node.js cluster module in detail.

**Answer:**
```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    console.log(`Master ${process.pid} is running`);
    
    // Fork workers
    for (let i = 0; i < numCPUs; i++) {
        const worker = cluster.fork();
        worker.on('message', (msg) => {
            console.log('Message from worker:', msg);
        });
    }
    
    cluster.on('exit', (worker, code, signal) => {
        console.log(`Worker ${worker.process.pid} died`);
        cluster.fork(); // Restart
    });
} else {
    // Worker process
    require('./app.js');
    process.send({ type: 'ready' });
}
```

### 30. Explain Express.js middleware types and best practices.

**Answer:**
**Middleware Types:**
```javascript
// Application-level
app.use((req, res, next) => {
    console.log('Application middleware');
    next();
});

// Router-level
router.use((req, res, next) => {
    console.log('Router middleware');
    next();
});

// Error-handling (4 parameters)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

// Built-in middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
```

**Best Practices:**
- Order matters (execute in sequence)
- Always call next() or send response
- Handle errors properly
- Use middleware for cross-cutting concerns
- Keep middleware focused and reusable

---

This covers Node.js and Express.js interview questions from beginner to advanced level with detailed explanations and code examples.

