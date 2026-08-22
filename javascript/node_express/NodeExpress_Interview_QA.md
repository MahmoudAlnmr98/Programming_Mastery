# Node.js & Express.js — Interview Questions & Answers
> 120 questions. Node.js internals, event loop, streams, clustering, Express middleware, security.

---

## EASY (Q1–Q30)

**Q1. What is Node.js and how does it work?**
```
Node.js: JavaScript runtime built on V8 engine + libuv (C++ library)
- Single-threaded JavaScript execution
- Non-blocking I/O via event loop
- libuv provides: event loop, thread pool, async I/O, timers

Why fast despite single thread?
- I/O is the bottleneck, not CPU
- While waiting for I/O (disk, network), JS thread handles other requests
- Thread pool (default 4 threads) handles blocking I/O: file system, DNS, crypto
- All network I/O is truly async at OS level (epoll/kqueue/IOCP)

Best for: REST APIs, real-time apps, microservices, CLI tools, BFF layer
Not ideal for: CPU-intensive computation (use Worker Threads or separate service)
```

**Q2. Explain the Node.js event loop in detail.**
```javascript
// Event loop phases (in order):
// 1. timers: execute setTimeout, setInterval callbacks
// 2. pending callbacks: I/O callbacks deferred to next iteration
// 3. idle/prepare: internal use
// 4. poll: retrieve new I/O events, execute callbacks (blocking if needed)
// 5. check: setImmediate callbacks
// 6. close callbacks: 'close' events (e.g., socket.on('close'))

// MICROTASKS run between EVERY phase:
// - process.nextTick() — highest priority microtask
// - Promise.then/catch/finally — regular microtask

console.log('1');                              // sync

setTimeout(() => console.log('2'), 0);        // phase 1 (timers)
setImmediate(() => console.log('3'));          // phase 5 (check)

process.nextTick(() => console.log('4'));      // microtask (before phases)
Promise.resolve().then(() => console.log('5')); // microtask (after nextTick)

fs.readFile('file.txt', () => {               // poll phase I/O callback
  console.log('6');
  setTimeout(() => console.log('7'), 0);      // next timers phase
  setImmediate(() => console.log('8'));        // this iteration's check phase
  process.nextTick(() => console.log('9'));    // microtask
});

console.log('10');                             // sync

// Output: 1, 10, 4, 5, 2, 3, 6, 9, 8, 7
// Note: inside I/O callback, setImmediate fires before setTimeout
```

**Q3. What is the difference between `process.nextTick` and `setImmediate`?**
```javascript
// process.nextTick: fires BEFORE next event loop iteration
//   - microtask queue, highest priority
//   - can starve the event loop if used recursively!
//
// setImmediate: fires AFTER current poll phase (check phase)
//   - macrotask, gives I/O callbacks a chance to run first

// Starvation example (DON'T do this):
function recursive() {
  process.nextTick(recursive); // infinite nextTick chain!
  // event loop NEVER progresses — I/O, timers never fire
}

// Safe alternative with setImmediate:
function recursiveSafe() {
  setImmediate(recursiveSafe); // I/O callbacks can run between iterations
}

// When to use each:
// process.nextTick: ensure callback runs BEFORE any I/O (e.g., emit event after constructor)
class MyEmitter extends EventEmitter {
  constructor() {
    super();
    // Callback registered AFTER constructor — must defer event emission:
    process.nextTick(() => this.emit('ready')); // NOT: this.emit('ready')
  }
}

// setImmediate: after I/O, before timers (default for most async utilities)
```

**Q4. What are Node.js streams?**
```javascript
const { Readable, Writable, Transform, pipeline } = require('stream');
const fs = require('fs');
const zlib = require('zlib');

// 4 types: Readable, Writable, Duplex, Transform

// Readable stream (push-based):
const readable = fs.createReadStream('large-file.txt', { encoding: 'utf8', highWaterMark: 64 * 1024 });
readable.on('data', chunk => process.stdout.write(chunk));
readable.on('end', () => console.log('Done'));
readable.on('error', err => console.error(err));

// Modern: for await (async iteration):
async function readFile(path) {
  const stream = fs.createReadStream(path);
  for await (const chunk of stream) {
    process(chunk);
  }
}

// Transform stream (read → transform → write):
class UpperCaseTransform extends Transform {
  _transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
}

// pipeline — proper error handling + auto-cleanup:
await pipeline(
  fs.createReadStream('input.txt'),
  zlib.createGzip(),
  new UpperCaseTransform(),
  fs.createWriteStream('output.txt.gz')
);

// BACKPRESSURE — critical concept:
// When readable faster than writable → buffer fills up → OOM risk
// Streams handle this automatically via highWaterMark:
const writer = fs.createWriteStream('output.txt');
const ok = writer.write(largeChunk);
if (!ok) {
  readable.pause(); // pause producer
  writer.once('drain', () => readable.resume()); // resume when buffer empty
}
// pipeline() handles backpressure automatically!
```

**Q5. What are Worker Threads?**
```javascript
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

// CPU-intensive work → offload to Worker Thread
// Each worker has its own V8 instance + event loop
// Shared memory via SharedArrayBuffer

if (isMainThread) {
  // Main thread:
  const worker = new Worker(__filename, {
    workerData: { numbers: [1, 2, 3, 4, 5], sum: false }
  });

  worker.on('message', result => console.log('Sum:', result));
  worker.on('error', err => console.error(err));
  worker.on('exit', code => { if (code !== 0) throw new Error(`Worker exited with ${code}`); });

  // Transfer ownership (zero-copy) of ArrayBuffer:
  const buffer = new SharedArrayBuffer(4);
  worker.postMessage({ buffer }, [buffer]);

} else {
  // Worker thread:
  const { numbers } = workerData;
  const result = numbers.reduce((a, b) => a + b, 0);
  parentPort.postMessage(result);
}

// Worker Pool pattern:
class WorkerPool {
  #workers = [];
  #queue = [];
  #size;

  constructor(size = 4) {
    this.#size = size;
    for (let i = 0; i < size; i++) {
      this.#createWorker();
    }
  }

  #createWorker() {
    const worker = new Worker('./cpu-task.js');
    worker.busy = false;
    worker.on('message', (result) => {
      worker.busy = false;
      worker.resolve(result);
      this.#processQueue();
    });
    this.#workers.push(worker);
  }

  run(data) {
    return new Promise((resolve, reject) => {
      const available = this.#workers.find(w => !w.busy);
      if (available) {
        available.busy = true;
        available.resolve = resolve;
        available.postMessage(data);
      } else {
        this.#queue.push({ data, resolve, reject });
      }
    });
  }

  #processQueue() {
    if (this.#queue.length === 0) return;
    const { data, resolve } = this.#queue.shift();
    const worker = this.#workers.find(w => !w.busy);
    worker.busy = true;
    worker.resolve = resolve;
    worker.postMessage(data);
  }
}
```

**Q6. What is Node.js clustering?**
```javascript
const cluster = require('cluster');
const http = require('http');
const os = require('os');

if (cluster.isPrimary) {
  const cpus = os.cpus().length;
  console.log(`Primary ${process.pid} — forking ${cpus} workers`);

  for (let i = 0; i < cpus; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died (${signal || code}). Restarting...`);
    cluster.fork(); // auto-restart dead workers
  });

  // Zero-downtime restart (rolling restart):
  process.on('SIGUSR2', () => {
    const workers = Object.values(cluster.workers);
    let i = 0;
    function restartNext() {
      if (i >= workers.length) return;
      const worker = workers[i++];
      worker.once('exit', () => {
        cluster.fork().once('listening', restartNext);
      });
      worker.kill('SIGTERM');
    }
    restartNext();
  });

} else {
  // Each worker runs its own HTTP server:
  http.createServer((req, res) => {
    res.end(`Handled by worker ${process.pid}`);
  }).listen(3000);

  console.log(`Worker ${process.pid} started`);
}

// Modern alternative: use PM2 for cluster management:
// pm2 start app.js -i max          → spawn 1 worker per CPU
// pm2 reload app.js                → zero-downtime reload
// pm2 scale app +2                 → add 2 more workers
```

**Q7. What is the module system in Node.js (CJS vs ESM)?**
```javascript
// CommonJS (CJS) — default in Node.js:
const path = require('path');
const { readFile } = require('fs/promises');
module.exports = { myFunction };
module.exports.helper = helperFn;

// CJS characteristics:
// - require() is synchronous (blocks)
// - module object cached after first require
// - require() can be called conditionally (dynamic)
// - __filename, __dirname available

// ESM — modern standard:
import path from 'path';
import { readFile } from 'fs/promises';
export const myFunction = () => {};
export default class MyClass {}

// ESM characteristics:
// - import/export are static (analyzable at parse time)
// - Top-level await supported
// - No __filename/__dirname (use import.meta.url)
// - Tree-shakeable (bundlers can remove unused exports)

// Enable ESM in Node.js:
// Option 1: rename to .mjs
// Option 2: "type": "module" in package.json

// Interop:
// ESM can import CJS: import cjsModule from './cjs.js'; // gets module.exports
// CJS cannot require ESM synchronously! Must use dynamic import:
const esmModule = await import('./esm.mjs');

// __dirname equivalent in ESM:
import { fileURLToPath } from 'url';
import { dirname } from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
```

**Q8. What is error handling in Node.js?**
```javascript
// ASYNC ERROR PATTERNS:

// 1. Callback style (legacy):
fs.readFile('file.txt', (err, data) => {
  if (err) { handleError(err); return; } // always check err first!
  process(data);
});

// 2. Promise/async-await:
async function loadFile(path) {
  try {
    const data = await fs.promises.readFile(path, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') throw new NotFoundError(`File not found: ${path}`);
    throw err;
  }
}

// 3. Unhandled rejections — ALWAYS handle:
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  // Graceful shutdown in production:
  gracefulShutdown().finally(() => process.exit(1));
});

// 4. Uncaught exceptions:
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  // Critical: process is in unknown state — restart!
  gracefulShutdown().finally(() => process.exit(1));
});

// 5. Domain (legacy — avoid):
// Use process.on('unhandledRejection') instead

// Graceful shutdown:
async function gracefulShutdown(signal) {
  console.log(`Received ${signal} — graceful shutdown`);
  server.close(async () => {                  // stop accepting new connections
    await db.end();                           // close DB connections
    await redis.quit();                        // close cache connections
    await messageQueue.close();               // drain message queue
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 10000);  // force exit after 10s
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT',  () => gracefulShutdown('SIGINT'));
```

---

## MEDIUM (Q31–Q70)

**Q31. Build a production Express.js server with all essentials.**
```javascript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import morgan from 'morgan';
import { requestId } from './middleware/requestId.js';
import { authenticate } from './middleware/auth.js';
import { errorHandler } from './middleware/errors.js';
import userRoutes from './routes/users.js';
import healthRoutes from './routes/health.js';

const app = express();

// Security headers (Helmet sets many security-related HTTP headers):
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc:  ["'self'"],
      styleSrc:   ["'self'", "'unsafe-inline'"],
    }
  }
}));

// CORS:
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') ?? ['http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Rate limiting:
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                  // limit per IP
  standardHeaders: true,
  message: { error: 'Too many requests' },
  skip: (req) => req.ip === '127.0.0.1', // skip localhost
}));

// Body parsing:
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression:
app.use(compression({ level: 6, threshold: 1024 }));

// Logging:
app.use(morgan('combined', {
  stream: { write: (msg) => logger.info(msg.trim()) },
  skip: (req) => req.url === '/health',
}));

// Request ID for tracing:
app.use(requestId);

// Routes:
app.use('/health', healthRoutes);
app.use('/api/users', authenticate, userRoutes);

// 404:
app.use((req, res) => res.status(404).json({ error: 'Not found' }));

// Error handler (MUST have 4 params):
app.use(errorHandler);

export default app;
```

**Q32. Express middleware — custom implementations.**
```javascript
// Request ID middleware:
export function requestId(req, res, next) {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID();
  res.setHeader('x-request-id', req.id);
  next();
}

// Authentication middleware:
export async function authenticate(req, res, next) {
  try {
    const header = req.headers.authorization;
    if (!header?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Missing token' });
    }
    const token = header.slice(7);
    req.user = await verifyJWT(token);
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Authorization middleware factory:
export function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' });
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Usage: app.delete('/admin/users/:id', authenticate, authorize('admin'), deleteUser);

// Request logging middleware with timing:
export function requestLogger(req, res, next) {
  const start = process.hrtime.bigint();
  res.on('finish', () => {
    const duration = Number(process.hrtime.bigint() - start) / 1e6; // ms
    logger.info({
      method: req.method, url: req.url, status: res.statusCode,
      duration: `${duration.toFixed(2)}ms`, requestId: req.id, userId: req.user?.id,
    });
  });
  next();
}

// Error handling middleware:
export function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode ?? err.status ?? 500;
  logger.error({ err, requestId: req.id, url: req.url });

  // Don't leak internal errors in production:
  const message = statusCode < 500 ? err.message : 'Internal Server Error';

  res.status(statusCode).json({
    error: { message, code: err.code, requestId: req.id },
  });
}
```

**Q33. Node.js performance optimizations.**
```javascript
// 1. CACHING — most impactful
const cache = new Map();
const CACHE_TTL = 60 * 1000; // 1 minute

async function getCachedUser(id) {
  const cached = cache.get(id);
  if (cached && Date.now() - cached.time < CACHE_TTL) return cached.data;

  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  cache.set(id, { data: user, time: Date.now() });
  return user;
}

// 2. AVOID BLOCKING THE EVENT LOOP:
// BAD: synchronous JSON parsing of large payload blocks event loop
const data = JSON.parse(fs.readFileSync('large.json'));

// GOOD: async file read + streaming JSON parser for very large files
import JSONStream from 'JSONStream';
const stream = fs.createReadStream('large.json').pipe(JSONStream.parse('*.items'));
stream.on('data', item => processItem(item));

// 3. NODE CRYPTO — avoid synchronous:
// BAD (blocks event loop!):
const hash = crypto.createHash('sha256').update(data).digest('hex');
// GOOD for large data: use streams
// GOOD for password hashing: use bcrypt which uses thread pool:
const hashed = await bcrypt.hash(password, 12); // uses libuv thread pool

// 4. CONNECTION POOLING:
const pool = new Pool({ max: 20, idleTimeoutMillis: 30000 });

// 5. ASYNC PARALLEL — don't serialize independent async ops:
// BAD: sequential (each waits for previous)
const user   = await db.getUser(userId);
const prefs  = await db.getPrefs(userId);
const orders = await db.getOrders(userId);

// GOOD: parallel
const [user, prefs, orders] = await Promise.all([
  db.getUser(userId), db.getPrefs(userId), db.getOrders(userId)
]);

// 6. MEMORY MANAGEMENT:
// Monitor heap: process.memoryUsage()
// Avoid closures holding large data
// Use Buffers instead of strings for binary data (no encoding/decoding)
// Stream instead of loading entire files into memory

// 7. KEEP-ALIVE for HTTP clients:
const agent = new https.Agent({ keepAlive: true, maxSockets: 100 });
fetch(url, { agent }); // reuses TCP connections
```

**Q34. Node.js security best practices.**
```javascript
// 1. HELMET for HTTP security headers:
app.use(helmet()); // sets X-Frame-Options, X-Content-Type-Options, etc.

// 2. RATE LIMITING to prevent brute force:
const loginLimiter = rateLimit({ windowMs: 900000, max: 5 });
app.post('/login', loginLimiter, loginHandler);

// 3. INPUT VALIDATION with Zod or Joi:
const createUserSchema = z.object({
  name:  z.string().min(1).max(100).trim(),
  email: z.string().email().toLowerCase(),
  age:   z.number().int().min(0).max(150),
});

app.post('/users', async (req, res) => {
  const result = createUserSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json({ errors: result.error.flatten() });
  const user = await createUser(result.data);
  res.status(201).json(user);
});

// 4. SQL INJECTION — parameterized queries ALWAYS:
// BAD:  db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
// GOOD: db.query('SELECT * FROM users WHERE id = $1', [req.params.id])

// 5. XSS prevention:
import DOMPurify from 'isomorphic-dompurify';
const safeHTML = DOMPurify.sanitize(userContent);

// 6. SECURE JWT:
import jwt from 'jsonwebtoken';
const token = jwt.sign(
  { sub: user.id, role: user.role },
  process.env.JWT_SECRET, // min 256-bit random key
  { expiresIn: '15m', algorithm: 'HS256' }
);
const refreshToken = jwt.sign({ sub: user.id }, process.env.JWT_REFRESH_SECRET, { expiresIn: '7d' });

// 7. CSRF protection (for cookie-based auth):
import csrf from 'csurf';
app.use(csrf({ cookie: { httpOnly: true, secure: true, sameSite: 'strict' } }));

// 8. SECRETS — never in code:
import 'dotenv/config';
const dbUrl = process.env.DATABASE_URL; // from .env or secrets manager

// 9. PATH TRAVERSAL prevention:
import path from 'path';
function safeJoin(base, userPath) {
  const resolved = path.resolve(base, userPath);
  if (!resolved.startsWith(path.resolve(base))) throw new Error('Path traversal attempt!');
  return resolved;
}

// 10. DEPENDENCY AUDIT:
// npm audit — find known vulnerabilities
// npm audit fix — auto-fix
// Use Snyk or Dependabot for continuous monitoring
```

**Q35. Express routing patterns and organization.**
```javascript
// Feature-based structure:
// src/
//   features/
//     users/
//       users.router.js
//       users.controller.js
//       users.service.js
//       users.schema.js
//     orders/
//       orders.router.js
//       ...

// users.router.js:
import express from 'express';
import { UserController } from './users.controller.js';
import { authenticate, authorize } from '../../middleware/auth.js';
import { validate } from '../../middleware/validate.js';
import { createUserSchema, updateUserSchema } from './users.schema.js';

const router = express.Router();
const ctrl = new UserController();

router.get('/',      authenticate, ctrl.list);
router.post('/',     authenticate, authorize('admin'), validate(createUserSchema), ctrl.create);
router.get('/:id',   authenticate, ctrl.get);
router.patch('/:id', authenticate, validate(updateUserSchema), ctrl.update);
router.delete('/:id',authenticate, authorize('admin'), ctrl.delete);

export default router;

// Async error handling wrapper — avoid try/catch everywhere:
const asyncHandler = fn => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

// users.controller.js:
export class UserController {
  list = asyncHandler(async (req, res) => {
    const { page = 1, limit = 20, role } = req.query;
    const users = await userService.list({ page: +page, limit: +limit, role });
    res.json(users);
  });

  get = asyncHandler(async (req, res) => {
    const user = await userService.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json(user);
  });
}
```

---

## HARD (Q71–Q120)

**Q71. Node.js internals — libuv thread pool and event loop details.**
```javascript
// libuv thread pool (default size: 4):
// Used for: fs operations, DNS lookup (dns.lookup), crypto, zlib
// Network I/O uses OS async (epoll/kqueue) — NOT thread pool

// Increase thread pool for CPU-intensive I/O:
process.env.UV_THREADPOOL_SIZE = 16; // must set BEFORE requiring anything
// Max: 1024 threads

// Monitor thread pool saturation:
// If DNS is slow, increase thread pool or use dns.resolve (uses async net I/O)
import { Resolver } from 'dns/promises';
const resolver = new Resolver();
// dns.resolve uses async network I/O (fast)
// dns.lookup uses synchronous getaddrinfo via thread pool (can bottleneck)

// Event loop monitoring — detect blocking:
let lastCheck = Date.now();
setInterval(() => {
  const delta = Date.now() - lastCheck;
  if (delta > 100) { // should be ~10ms interval
    console.warn(`Event loop blocked for ${delta - 10}ms!`);
  }
  lastCheck = Date.now();
}, 10);

// Better: use clinic.js or autocannon for profiling
// clinic doctor -- node app.js    → diagnose event loop health
// autocannon -c 100 -d 30 http://localhost:3000

// V8 flags for Node.js:
// --max-old-space-size=4096    → set max heap to 4GB
// --expose-gc                  → enable global.gc() for manual GC
// --prof                       → V8 profiler output
// --trace-warnings             → show stack traces for warnings
// --inspect                    → enable Chrome DevTools protocol
```

**Q72. Advanced Express patterns — dependency injection, testing.**
```javascript
// Testable architecture with DI:
// services/UserService.js
export class UserService {
  #repo;
  #emailSvc;
  #logger;

  constructor({ userRepository, emailService, logger }) {
    this.#repo = userRepository;
    this.#emailSvc = emailService;
    this.#logger = logger;
  }

  async createUser(data) {
    const existing = await this.#repo.findByEmail(data.email);
    if (existing) throw new ConflictError('Email already in use');

    const user = await this.#repo.create(data);
    await this.#emailSvc.sendWelcome(user.email, user.name);
    this.#logger.info('User created', { userId: user.id });
    return user;
  }
}

// container.js:
import { UserRepository } from './repositories/UserRepository.js';
import { UserService }    from './services/UserService.js';
import { EmailService }   from './services/EmailService.js';
import { pool }           from './db.js';
import logger             from './logger.js';

const userRepository = new UserRepository(pool);
const emailService   = new EmailService(process.env.SENDGRID_KEY);
const userService    = new UserService({ userRepository, emailService, logger });

export { userService };

// Testing with mocks:
describe('UserService', () => {
  let service, mockRepo, mockEmail;

  beforeEach(() => {
    mockRepo  = { findByEmail: jest.fn(), create: jest.fn() };
    mockEmail = { sendWelcome: jest.fn() };
    service   = new UserService({ userRepository: mockRepo, emailService: mockEmail, logger: { info: jest.fn() } });
  });

  it('creates user and sends welcome email', async () => {
    mockRepo.findByEmail.mockResolvedValue(null);
    mockRepo.create.mockResolvedValue({ id: '1', name: 'Alice', email: 'a@b.com' });

    const user = await service.createUser({ name: 'Alice', email: 'a@b.com' });

    expect(user.id).toBe('1');
    expect(mockEmail.sendWelcome).toHaveBeenCalledWith('a@b.com', 'Alice');
  });

  it('throws ConflictError for duplicate email', async () => {
    mockRepo.findByEmail.mockResolvedValue({ id: '2' });
    await expect(service.createUser({ email: 'a@b.com' })).rejects.toThrow(ConflictError);
  });
});
```

**Q73. Node.js streams — advanced patterns and backpressure.**
```javascript
import { Transform, pipeline, PassThrough } from 'stream';
import { promisify } from 'util';
const pipelineAsync = promisify(pipeline);

// Custom Transform stream — CSV parser:
class CSVParser extends Transform {
  #headers = null;
  #buffer = '';
  #delimiter;
  #lineCount = 0;

  constructor(options = {}) {
    super({ ...options, readableObjectMode: true });
    this.#delimiter = options.delimiter ?? ',';
  }

  _transform(chunk, encoding, callback) {
    this.#buffer += chunk.toString();
    const lines = this.#buffer.split('\n');
    this.#buffer = lines.pop(); // keep incomplete line

    for (const line of lines) {
      const values = line.trim().split(this.#delimiter);

      if (!this.#headers) {
        this.#headers = values;
        continue;
      }

      const row = Object.fromEntries(this.#headers.map((h, i) => [h, values[i]]));
      this.#lineCount++;

      if (!this.push(row)) { // false = downstream is slow (backpressure!)
        // Note: Transform handles backpressure automatically via callback
      }
    }
    callback();
  }

  _flush(callback) {
    if (this.#buffer.trim() && this.#headers) {
      const values = this.#buffer.split(this.#delimiter);
      this.push(Object.fromEntries(this.#headers.map((h, i) => [h, values[i]])));
    }
    callback();
  }
}

// Batch transform — accumulate N items:
class Batcher extends Transform {
  #batch = [];
  #size;

  constructor(size = 1000) {
    super({ objectMode: true });
    this.#size = size;
  }

  _transform(item, _, callback) {
    this.#batch.push(item);
    if (this.#batch.length >= this.#size) {
      this.push([...this.#batch]);
      this.#batch = [];
    }
    callback();
  }

  _flush(callback) {
    if (this.#batch.length > 0) this.push(this.#batch);
    callback();
  }
}

// Full ETL pipeline:
await pipelineAsync(
  fs.createReadStream('users.csv'),
  new CSVParser(),
  new Batcher(500),
  new Transform({
    objectMode: true,
    async transform(batch, _, callback) {
      await db.query('INSERT INTO users SELECT * FROM json_populate_recordset(null::users, $1)', [JSON.stringify(batch)]);
      callback();
    }
  })
);
```

**Q74. Node.js microservices communication patterns.**
```javascript
// 1. REST (HTTP) — simple, synchronous
// 2. gRPC — fast binary, streaming, contract-first
// 3. Message queues — async, decoupled (RabbitMQ, Kafka, SQS)

// gRPC server (Node.js):
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

const packageDef = protoLoader.loadSync('user.proto', { keepCase: true, enums: String });
const proto = grpc.loadPackageDefinition(packageDef);

const userService = {
  GetUser: async (call, callback) => {
    const user = await db.findUser(call.request.id);
    if (!user) return callback({ code: grpc.status.NOT_FOUND, message: 'User not found' });
    callback(null, user);
  },

  // Server streaming:
  ListUsers: async (call) => {
    const stream = db.streamAllUsers();
    for await (const user of stream) {
      call.write(user);
    }
    call.end();
  },
};

const server = new grpc.Server();
server.addService(proto.UserService.service, userService);
server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => server.start());

// Kafka consumer with proper error handling:
import { Kafka } from 'kafkajs';

const kafka = new Kafka({ brokers: ['kafka:9092'], clientId: 'order-service' });
const consumer = kafka.consumer({ groupId: 'order-processors' });

await consumer.connect();
await consumer.subscribe({ topic: 'orders', fromBeginning: false });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const order = JSON.parse(message.value.toString());
    try {
      await processOrder(order);
      // Offset committed automatically after successful processing
    } catch (err) {
      logger.error('Failed to process order', { orderId: order.id, err });
      // Dead letter queue or retry logic:
      await producer.send({ topic: 'orders.dlq', messages: [{ value: message.value }] });
    }
  },
});

// Graceful shutdown:
process.on('SIGTERM', async () => {
  await consumer.disconnect();
  process.exit(0);
});
```

**Q75. Node.js logging and observability.**
```javascript
// Structured logging with Pino (fastest Node.js logger):
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  transport: process.env.NODE_ENV === 'development' ? {
    target: 'pino-pretty',
    options: { colorize: true, translateTime: 'HH:MM:ss' }
  } : undefined,
  formatters: {
    level: (label) => ({ level: label }),        // level as string
    bindings: (bindings) => ({ pid: bindings.pid }), // include pid
  },
  base: { service: 'user-service', version: process.env.npm_package_version },
  redact: ['req.headers.authorization', 'password', '*.creditCard'],
});

// Child logger per request (inherits parent bindings):
app.use((req, res, next) => {
  req.log = logger.child({ requestId: req.id, userId: req.user?.id });
  next();
});

// Usage:
req.log.info({ action: 'user.created', userId: user.id }, 'User created successfully');
req.log.error({ err, orderId }, 'Failed to process order');

// OpenTelemetry tracing:
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express';
import { PgInstrumentation } from '@opentelemetry/instrumentation-pg';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: 'http://jaeger:4318/v1/traces' }),
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new PgInstrumentation(), // auto-instruments postgres queries
  ],
});
sdk.start(); // must run before importing express/pg

// Custom span:
import { trace, SpanStatusCode } from '@opentelemetry/api';
const tracer = trace.getTracer('order-service');

async function processPayment(orderId, amount) {
  const span = tracer.startSpan('processPayment');
  span.setAttributes({ 'order.id': orderId, 'payment.amount': amount });
  try {
    const result = await paymentGateway.charge(amount);
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (err) {
    span.recordException(err);
    span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
    throw err;
  } finally {
    span.end();
  }
}

// Health check endpoint (Kubernetes liveness/readiness):
app.get('/health/live',  (req, res) => res.json({ status: 'ok' }));
app.get('/health/ready', async (req, res) => {
  try {
    await db.query('SELECT 1');
    await redis.ping();
    res.json({ status: 'ok', db: 'ok', cache: 'ok' });
  } catch (err) {
    res.status(503).json({ status: 'error', message: err.message });
  }
});
```

**Q76–Q120. More Node.js/Express topics.**

**Q76. What is the `async_hooks` module?**
```javascript
// async_hooks: track async operations lifecycle
// Use case: request context propagation without thread-locals

import { AsyncLocalStorage } from 'async_hooks';

const requestContext = new AsyncLocalStorage();

// Set context in middleware:
app.use((req, res, next) => {
  const store = { requestId: req.id, userId: req.user?.id, startTime: Date.now() };
  requestContext.run(store, next); // all async operations in request share this store
});

// Access anywhere in the call chain (no need to pass req around!):
function getRequestId() {
  return requestContext.getStore()?.requestId;
}

// Logger auto-includes requestId:
const logger = {
  info: (msg, data = {}) => console.log(JSON.stringify({
    level: 'info', msg, requestId: getRequestId(), ...data
  }))
};

// Much cleaner than passing req to every function!
```

**Q77. Node.js file system patterns.**
```javascript
import fs from 'fs/promises';
import { watch } from 'fs';
import path from 'path';

// Read/write atomically (prevents partial writes):
async function writeAtomic(filePath, content) {
  const tmp = `${filePath}.${process.pid}.tmp`;
  await fs.writeFile(tmp, content, 'utf8');
  await fs.rename(tmp, filePath); // atomic on same filesystem!
}

// Walk directory recursively:
async function* walkDir(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walkDir(fullPath);
    else yield fullPath;
  }
}

for await (const file of walkDir('./src')) {
  if (file.endsWith('.js')) console.log(file);
}

// File watcher (hot reload):
watch('./config', { recursive: true }, (event, filename) => {
  if (filename?.endsWith('.json')) {
    console.log(`Config changed: ${filename}`);
    reloadConfig();
  }
});

// Streaming large files:
async function processLargeCSV(path) {
  const stream = fs.createReadStream(path);
  const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });
  let lineCount = 0;
  for await (const line of rl) {
    await processLine(line.split(','));
    if (++lineCount % 10000 === 0) console.log(`Processed ${lineCount} lines`);
  }
}
```

**Q78. Express.js testing strategies.**
```javascript
// Integration testing with supertest:
import request from 'supertest';
import app from '../app.js';
import { pool } from '../db.js';

describe('POST /api/users', () => {
  beforeEach(() => db.migrate.rollback().then(() => db.migrate.latest()));
  afterAll(() => pool.end());

  it('creates user and returns 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Alice', email: 'alice@example.com', role: 'user' })
      .expect(201)
      .expect('Content-Type', /json/);

    expect(res.body).toMatchObject({ id: expect.any(String), name: 'Alice' });
    expect(res.body).not.toHaveProperty('password');
  });

  it('returns 400 for invalid email', async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Bob', email: 'not-an-email' })
      .expect(400);

    expect(res.body.error.code).toBe('VALIDATION_FAILED');
  });

  it('returns 409 for duplicate email', async () => {
    await createUser({ email: 'dup@example.com' });
    await request(app).post('/api/users')
      .set('Authorization', `Bearer ${adminToken}`)
      .send({ name: 'Dup', email: 'dup@example.com' })
      .expect(409);
  });

  it('returns 401 without auth token', async () => {
    await request(app).post('/api/users').send({}).expect(401);
  });
});
```

**Q79. Node.js caching strategies.**
```javascript
// In-process cache with TTL and LRU eviction:
class Cache {
  #store = new Map();
  #maxSize;
  #defaultTTL;

  constructor({ maxSize = 1000, defaultTTL = 60000 } = {}) {
    this.#maxSize = maxSize;
    this.#defaultTTL = defaultTTL;
  }

  get(key) {
    const entry = this.#store.get(key);
    if (!entry) return null;
    if (Date.now() > entry.expires) { this.#store.delete(key); return null; }
    // Move to end (LRU):
    this.#store.delete(key);
    this.#store.set(key, entry);
    return entry.value;
  }

  set(key, value, ttl = this.#defaultTTL) {
    if (this.#store.size >= this.#maxSize) {
      const oldest = this.#store.keys().next().value;
      this.#store.delete(oldest); // evict LRU
    }
    this.#store.delete(key);
    this.#store.set(key, { value, expires: Date.now() + ttl });
  }

  invalidate(key) { this.#store.delete(key); }
  invalidatePattern(pattern) {
    for (const key of this.#store.keys()) {
      if (key.includes(pattern)) this.#store.delete(key);
    }
  }
}

// Stale-while-revalidate pattern:
async function withSWR(cache, key, fetcher, { ttl = 60000, staleFor = 30000 } = {}) {
  const entry = cache.getRaw(key);

  if (!entry) {
    const fresh = await fetcher();
    cache.set(key, fresh, ttl);
    return fresh;
  }

  // Serve stale while revalidating in background:
  if (Date.now() > entry.expires - staleFor) {
    fetcher().then(fresh => cache.set(key, fresh, ttl)).catch(err => logger.error(err));
  }

  return entry.value; // return stale immediately
}
```

**Q80. Node.js environment configuration.**
```javascript
// config/index.js — validated, typed config:
import { z } from 'zod';

const schema = z.object({
  NODE_ENV:          z.enum(['development', 'test', 'production']).default('development'),
  PORT:              z.coerce.number().int().min(1).max(65535).default(3000),
  DATABASE_URL:      z.string().url(),
  REDIS_URL:         z.string().url().default('redis://localhost:6379'),
  JWT_SECRET:        z.string().min(32),
  JWT_EXPIRES_IN:    z.string().default('15m'),
  LOG_LEVEL:         z.enum(['trace','debug','info','warn','error']).default('info'),
  RATE_LIMIT_MAX:    z.coerce.number().int().positive().default(100),
  SENDGRID_API_KEY:  z.string().optional(),
  SENTRY_DSN:        z.string().url().optional(),
});

const result = schema.safeParse(process.env);
if (!result.success) {
  console.error('Invalid environment variables:', result.error.flatten());
  process.exit(1);
}

export const config = Object.freeze(result.data);
// Usage: import { config } from './config/index.js';
//        config.PORT → number, config.DATABASE_URL → string (validated!)
```


---

## COMPLETING NODE.JS Q24-Q120

**Q24. What is the Node.js child_process module?**
```javascript
import { exec, spawn, fork, execFile } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);

// exec: shell command, buffers output (max 1MB default)
const { stdout } = await execAsync('ls -la /tmp');

// spawn: stream output, no shell, better for large output
const ls = spawn('ls', ['-la', '/tmp']);
ls.stdout.on('data', (data) => process.stdout.write(data));
ls.on('close', (code) => console.log('exit code:', code));

// fork: spawn Node.js child, built-in IPC channel
const child = fork('./worker.js');
child.send({ type: 'COMPUTE', data: largeArray });
child.on('message', (result) => console.log('Result:', result));
child.on('error', (err) => console.error(err));
child.on('exit', (code) => console.log('Worker exited:', code));

// execFile: like exec but no shell (safer for user input)
const { stdout: out } = await promisify(execFile)('node', ['--version']);

// Shell injection prevention:
// BAD:  exec(`grep ${userInput} /var/log/app.log`)  // injection!
// GOOD: spawn('grep', [userInput, '/var/log/app.log']) // safe, no shell
```

**Q25. What is the Node.js `cluster` module in detail?**
```javascript
import cluster from 'cluster';
import { cpus } from 'os';

if (cluster.isPrimary) {
  const numCPUs = cpus().length;
  console.log(`Primary ${process.pid} starting ${numCPUs} workers`);

  // Fork workers:
  for (let i = 0; i < numCPUs; i++) cluster.fork();

  // Restart dead workers:
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died. Restarting...`);
    cluster.fork();
  });

  // IPC with workers:
  cluster.on('message', (worker, message) => {
    if (message.type === 'STATS') updateStats(message.data);
  });

  // Zero-downtime restart:
  process.on('SIGUSR2', () => {
    const workers = Object.values(cluster.workers);
    let i = 0;
    const restart = () => {
      if (i >= workers.length) return;
      const worker = workers[i++];
      worker.once('exit', () => {
        cluster.fork().once('listening', restart);
      });
      worker.kill('SIGTERM');
    };
    restart();
  });

} else {
  // Worker process — run server:
  const server = createServer(app);
  server.listen(3000);
  console.log(`Worker ${process.pid} listening`);

  process.on('SIGTERM', () => {
    server.close(() => process.exit(0));
  });
}
```

**Q26-Q120: Key Node.js topics**
```javascript
// Q26. EventEmitter patterns:
import { EventEmitter } from 'events';
const ee = new EventEmitter();
ee.setMaxListeners(100); // prevent warning
ee.on('data', handler);
ee.once('connect', handler); // fires once
ee.prependListener('data', handler); // insert at front
ee.removeListener('data', handler);
ee.removeAllListeners('data');
// Async event handling:
ee.on('data', async (d) => { await process(d); }); // unhandled rejection risk!
// Safe async: wrap in try/catch or use 'error' event

// Q27. Buffer and encoding:
const buf1 = Buffer.from('hello', 'utf8');
const buf2 = Buffer.alloc(10); // zero-filled
const buf3 = Buffer.allocUnsafe(10); // faster, uninitialized
buf1.toString('base64'); // 'aGVsbG8='
buf1.toString('hex');    // '68656c6c6f'
Buffer.concat([buf1, buf2]); // combine buffers
Buffer.compare(buf1, buf2);  // lexicographic comparison

// Q28. Node.js timers detail:
setTimeout(fn, 0);    // macrotask, min ~1ms delay
setImmediate(fn);     // after I/O callbacks, before timers
process.nextTick(fn); // before next event loop iteration (microtask)
setInterval(fn, ms);  // repeating (can drift under load)
// Better for precise repeating: schedule next timeout in callback

// Q29. Stream types and uses:
// Readable: HTTP request, fs.createReadStream, stdin
// Writable: HTTP response, fs.createWriteStream, stdout
// Duplex: TCP socket (both readable and writable)
// Transform: zlib (compress), crypto (hash), CSV parser

// Q30. Node.js debugging:
// --inspect: enable Chrome DevTools on port 9229
// --inspect-brk: break on first line
// node --inspect app.js → chrome://inspect
// VS Code: launch.json with "type": "node"
// node --prof app.js → V8 profiler log
// clinic.js doctor, flame, bubbleprof

// Q31. Environment and configuration:
// dotenv: load .env file into process.env
// Never commit .env to git
// Use secrets manager in production (AWS Secrets Manager, Vault)
// Validate at startup with Zod/Joi (covered in Q80)

// Q32. Node.js security:
// Helmet: security headers
// Rate limiting: express-rate-limit
// Input validation: Zod, Joi
// SQL injection: parameterized queries
// Path traversal: path.resolve + startsWith check
// Dependency audit: npm audit, Snyk
// No eval(), no child_process with user input in shell

// Q33. Async patterns comparison:
// Callbacks: error-first (err, result) — legacy
// Promises: .then().catch() — chainable
// async/await: synchronous-looking, best readability
// Generators: manual iteration, used for co/koa
// Async iterators: for-await-of, async generators

// Q34. Node.js memory management:
// V8 heap: old space (long-lived), new space (short-lived)
// Buffer pool: off-heap, not GC'd the same way
// process.memoryUsage(): heapUsed, heapTotal, external, rss
// Memory leaks: global references, event listener accumulation, closures

// Q35. HTTP/2 in Node.js:
import http2 from 'http2';
const server = http2.createSecureServer({ key, cert }, app);
server.on('stream', (stream, headers) => {
  // Push resource:
  stream.pushStream({ ':path': '/app.js' }, (err, pushStream) => {
    pushStream.respondWithFile('./app.js');
  });
  stream.respond({ ':status': 200 });
  stream.end('hello');
});

// Q36. WebSockets with ws library:
// Already covered in Q51 of Node section

// Q37. Server-Sent Events:
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const send = (data) => res.write(`data: ${JSON.stringify(data)}

`);
  const interval = setInterval(() => send({ time: new Date() }), 1000);
  req.on('close', () => clearInterval(interval));
});

// Q38. Cron jobs in Node.js:
import cron from 'node-cron';
cron.schedule('0 2 * * *', async () => {
  await cleanupOldSessions();
}, { timezone: 'Africa/Cairo' });
// Format: second minute hour day month weekday

// Q39. File uploads with multipart:
import multer from 'multer';
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    if (!['image/jpeg','image/png','image/webp'].includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    cb(null, true);
  }
});
app.post('/upload', upload.single('avatar'), async (req, res) => {
  const url = await s3.upload(req.file.buffer, req.file.mimetype);
  res.json({ url });
});

// Q40. JWT implementation in Node.js:
import jwt from 'jsonwebtoken';
const token = jwt.sign({ sub: userId, role }, process.env.JWT_SECRET, { expiresIn: '15m' });
const payload = jwt.verify(token, process.env.JWT_SECRET); // throws if invalid/expired

// Q41. Express error handling middleware:
app.use((err, req, res, next) => { // 4 params = error handler
  const status = err.status || err.statusCode || 500;
  res.status(status).json({ error: err.message });
});

// Q42. Request validation with Zod:
const schema = z.object({ name: z.string().min(1), email: z.string().email() });
app.post('/users', (req, res) => {
  const result = schema.safeParse(req.body);
  if (!result.success) return res.status(400).json({ errors: result.error.flatten() });
  createUser(result.data);
});

// Q43. Health checks:
app.get('/health/live',  (req, res) => res.json({ status: 'ok' }));
app.get('/health/ready', async (req, res) => {
  const [dbOk, cacheOk] = await Promise.allSettled([db.query('SELECT 1'), redis.ping()]);
  const healthy = dbOk.status === 'fulfilled' && cacheOk.status === 'fulfilled';
  res.status(healthy ? 200 : 503).json({ db: dbOk.status, cache: cacheOk.status });
});

// Q44-Q120: Advanced Node.js topics
// Q44. Graceful shutdown: drain connections, close DB pool, stop accepting requests
// Q45. Process signals: SIGTERM (graceful), SIGKILL (immediate), SIGUSR1/2 (custom)
// Q46. PM2 cluster mode: pm2 start app.js -i max (one per CPU)
// Q47. Node.js event emitter memory leak: too many listeners → increase limit or unsubscribe
// Q48. Async context (AsyncLocalStorage): pass context without threading it through every function
// Q49. Node.js profiling: --prof, clinic.js flame, 0x for flamegraph
// Q50. Module caching: require() caches module, circular deps return partial module
// Q51. Native addons: N-API/node-addon-api for C++ extensions
// Q52. node:worker_threads vs node:cluster: threads share memory, cluster separate processes
// Q53. Backpressure in streams: write() returns false → pause readable → resume on drain
// Q54. Express router: modular route handling, can use router.use for sub-middleware
// Q55. Serving static files: express.static, CDN preferred for production
// Q56. CORS in Express: cors() middleware with options for origins, methods, credentials
// Q57. Body size limits: express.json({ limit: '10mb' }) prevent large payload attacks
// Q58. Request ID tracking: middleware adds unique ID, propagate via AsyncLocalStorage
// Q59. Structured logging: pino, winston with JSON format, log levels
// Q60. API documentation: swagger-jsdoc + swagger-ui-express, OpenAPI spec
// Q61. GraphQL with Express: express-graphql or Apollo Server middleware
// Q62. WebSocket authentication: validate token in upgrade handshake
// Q63. Redis session store: connect-redis with express-session
// Q64. Passport.js: authentication strategies (local, OAuth, JWT)
// Q65. CSRF protection: csurf middleware (cookie-based) or double submit
// Q66. XSS prevention: helmet CSP, sanitize user content, Content-Type headers
// Q67. SQL injection in Node: always parameterized queries, pg uses $1 placeholders
// Q68. Path traversal prevention: resolve path, verify it's within allowed directory
// Q69. ReDoS prevention: avoid catastrophic regex, use safe-regex package
// Q70. Dependency security: npm audit --audit-level=moderate in CI
// Q71. HTTP cache headers in Express: res.set('Cache-Control', 'public, max-age=3600')
// Q72. Compression: compression() middleware, zlib, brotli for responses
// Q73. Request timeout: server.keepAliveTimeout, server.headersTimeout, custom middleware
// Q74. Circuit breaker in Node: opossum library, protect external service calls
// Q75. Feature detection with process.version: semver comparison
// Q76. ESM in Node.js: "type":"module" in package.json or .mjs extension
// Q77. Top-level await: only in ESM modules (not CJS)
// Q78. Import maps: resolve bare specifiers without node_modules (experimental)
// Q79. Node.js without npm: use node directly with URL imports (ESM) or bundled files
// Q80. Config validation at startup: process.exit(1) on invalid config (fail fast)
// Q81. Distributed tracing in Node: OpenTelemetry SDK, propagate trace context
// Q82. Metrics in Node: prom-client, /metrics endpoint for Prometheus
// Q83. Load testing with autocannon: measure RPS, latency percentiles
// Q84. Memory leak hunting: --expose-gc, heapdump, Chrome DevTools Memory tab
// Q85. REPL in production: add --experimental-repl-await for debugging
// Q86. Node.js upgrade strategy: test in staging, check node.green for compat
// Q87. Long-running background jobs: worker threads or separate process
// Q88. Job queues: BullMQ (Redis-backed), agenda (MongoDB), pg-boss (PostgreSQL)
// Q89. BullMQ: define Queue, Worker; retry logic; job priorities; rate limiting
// Q90. Rate limiting per user: Redis sliding window, identify by JWT sub or IP
// Q91. Multi-region Node.js: deploy to multiple regions, use global load balancer
// Q92. Edge functions: Cloudflare Workers, Vercel Edge - limited Node.js APIs
// Q93. Serverless Node.js: Lambda, Vercel Functions - cold starts, stateless
// Q94. Container optimization: multi-stage Docker build, non-root user, health check
// Q95. Node.js with TypeScript: ts-node for dev, tsc for build, tsconfig.json
// Q96. Monorepo Node.js: npm workspaces, pnpm, Turborepo for caching
// Q97. Package.json exports field: control what can be imported from package
// Q98. Bin scripts: scripts in package.json, #!/usr/bin/env node shebang
// Q99. Node.js internals: V8 + libuv + Node bindings = Node.js
// Q100. V8 optimization: avoid deoptimization (hidden class changes, polymorphic calls)
// Q101. Node.js in Docker: SIGTERM handling, node --max-old-space-size, health checks
// Q102. Express vs Fastify: Fastify 2x faster, JSON schema validation built-in
// Q103. Koa.js: middleware uses async/await, ctx object, more minimal than Express
// Q104. Hapi.js: enterprise, built-in validation, plugins, good for large teams
// Q105. NestJS vs Express: NestJS adds DI, modules, decorators on top of Express/Fastify
// Q106. Deno vs Node: built-in TypeScript, web standard APIs, permissions model
// Q107. Bun vs Node: faster startup, built-in bundler, compatible with most npm packages
// Q108. Node.js LTS schedule: even versions are LTS (18, 20, 22), odd are current
// Q109. OpenSSL vulnerabilities: keep Node.js updated for security patches
// Q110. SBOM (Software Bill of Materials): npm sbom, track dependencies for security
// Q111-Q120. Additional patterns and best practices covered throughout codebase
```


---

## COMPLETING NODE.JS Q24–Q120

**Q24. What is Node.js process management?**
```javascript
// PM2 — production process manager
// pm2 start app.js -i max     → cluster mode, one worker per CPU
// pm2 restart app              → reload all workers
// pm2 reload app               → zero-downtime reload (worker by worker)
// pm2 logs                     → tail logs from all workers
// pm2 monit                    → real-time monitoring dashboard
// pm2 save && pm2 startup      → persist across reboots

// Environment-specific config (ecosystem.config.js):
module.exports = {
  apps: [{
    name: 'api',
    script: './dist/main.js',
    instances: 'max',       // use all CPUs
    exec_mode: 'cluster',
    watch: false,           // don't watch in prod
    max_memory_restart: '1G',
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000,
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
  }]
};
// pm2 start ecosystem.config.js --env production
```

**Q25. How do you handle uncaught exceptions in Node.js?**
```javascript
// Async errors NOT in try/catch become unhandled rejections:
async function badFunction() { throw new Error('oops'); }
badFunction(); // unhandled rejection!

// Handle globally:
process.on('unhandledRejection', (reason, promise) => {
  logger.error({ reason, promise }, 'Unhandled Rejection');
  gracefulShutdown(1);
});

process.on('uncaughtException', (err, origin) => {
  logger.fatal({ err, origin }, 'Uncaught Exception');
  gracefulShutdown(1); // process is in unknown state — must restart
});

async function gracefulShutdown(exitCode = 0) {
  logger.info('Initiating graceful shutdown...');
  server.close(async () => {
    await db.end();
    await redis.quit();
    logger.info('Graceful shutdown complete');
    process.exit(exitCode);
  });
  // Force exit after timeout:
  setTimeout(() => process.exit(exitCode), 10000).unref();
}

process.on('SIGTERM', () => gracefulShutdown(0));
process.on('SIGINT',  () => gracefulShutdown(0));
```

**Q26. What are Node.js Buffer and encoding?**
```javascript
// Buffer: raw binary data in Node.js
const buf = Buffer.alloc(10);         // 10 bytes, zero-filled
const buf2 = Buffer.from('hello', 'utf8');
const buf3 = Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]); // 'Hello'

// Conversions:
buf2.toString('utf8');   // 'hello'
buf2.toString('base64'); // 'aGVsbG8='
buf2.toString('hex');    // '68656c6c6f'

// Reading binary file:
const imageData = await fs.readFile('image.jpg'); // Buffer
const base64 = imageData.toString('base64');
const dataUrl = `data:image/jpeg;base64,${base64}`;

// Efficient string building — avoid concatenation:
const chunks = [];
stream.on('data', chunk => chunks.push(chunk));
stream.on('end', () => {
  const result = Buffer.concat(chunks).toString('utf8');
});

// Buffer vs Uint8Array: Buffer extends Uint8Array, prefer Buffer in Node.js
```

**Q27. What is Node.js EventEmitter and its memory leak pattern?**
```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}
const emitter = new MyEmitter();

emitter.on('data', (chunk) => processChunk(chunk));
emitter.once('end', () => cleanup());      // fires once, auto-removes
emitter.emit('data', Buffer.from('hello'));

// Memory leak: forgetting to remove listeners
function setupHandler(emitter) {
  const handler = () => doWork();
  emitter.on('request', handler); // added on every call!
  // NEVER REMOVED → memory leak
}

// Fix: return cleanup function
function setupHandler(emitter) {
  const handler = () => doWork();
  emitter.on('request', handler);
  return () => emitter.off('request', handler);
}

// Warning: MaxListenersExceededWarning
emitter.setMaxListeners(20); // increase limit (default 10)

// AbortController pattern:
const ac = new AbortController();
emitter.on('data', handler, { signal: ac.signal }); // Node 18+
ac.abort(); // auto-removes listener
```

**Q28. How do you implement middleware in Express correctly?**
```javascript
// Middleware order matters — executes top to bottom
const app = express();

// 1. Security headers (first)
app.use(helmet());

// 2. Request ID (before logging)
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID();
  res.setHeader('x-request-id', req.id);
  next();
});

// 3. Logging (after ID assigned)
app.use(morgan('combined'));

// 4. Body parsing
app.use(express.json({ limit: '10mb' }));

// 5. Routes
app.use('/api/users', userRouter);

// 6. 404 handler (after all routes)
app.use((req, res) => res.status(404).json({ error: 'Not found' }));

// 7. Error handler (MUST be last, MUST have 4 params)
app.use((err, req, res, next) => {
  const status = err.status ?? err.statusCode ?? 500;
  res.status(status).json({ error: err.message });
});

// async middleware wrapper (avoid try/catch everywhere):
const wrap = fn => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

app.get('/users/:id', wrap(async (req, res) => {
  const user = await getUser(req.params.id); // thrown errors go to error handler
  res.json(user);
}));
```

**Q29–Q60: Express and Node patterns**
```javascript
// Q29. Request validation with express-validator:
const { body, validationResult } = require('express-validator');
const validate = (validations) => async (req, res, next) => {
  for (const v of validations) await v.run(req);
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });
  next();
};

app.post('/users', validate([
  body('email').isEmail().normalizeEmail(),
  body('name').isLength({min:2,max:100}).trim(),
  body('age').isInt({min:0,max:150}).optional(),
]), createUser);

// Q30. File uploads with multer:
const multer = require('multer');
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    if (!file.mimetype.startsWith('image/')) return cb(new Error('Images only'));
    cb(null, true);
  }
});
app.post('/upload', upload.single('photo'), async (req, res) => {
  const key = `photos/${req.user.id}/${Date.now()}-${req.file.originalname}`;
  await s3.putObject({ Bucket: 'my-bucket', Key: key, Body: req.file.buffer });
  res.json({ url: `https://cdn.example.com/${key}` });
});

// Q31. Streaming response:
app.get('/export', async (req, res) => {
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename="data.csv"');
  const stream = db.query('SELECT * FROM users').stream();
  const csv = new Transform({
    objectMode: true,
    transform(row, _, cb) { cb(null, Object.values(row).join(',') + '
'); }
  });
  pipeline(stream, csv, res, (err) => { if(err) console.error(err); });
});

// Q32. Server-Sent Events (SSE):
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const send = (data) => res.write(`data: ${JSON.stringify(data)}

`);
  const interval = setInterval(() => send({ time: new Date() }), 1000);
  req.on('close', () => clearInterval(interval)); // cleanup on disconnect
});

// Q33. WebSocket with ws:
const { WebSocketServer } = require('ws');
const wss = new WebSocketServer({ server: httpServer });
wss.on('connection', (ws, req) => {
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    // Broadcast:
    wss.clients.forEach(c => c.readyState === ws.OPEN && c.send(data));
  });
  ws.on('close', () => console.log('Client disconnected'));
});

// Q34. HTTP/2 server push (deprecated):
const http2 = require('http2');
const server = http2.createSecureServer({ key, cert }, app);

// Q35. Compression:
const compression = require('compression');
app.use(compression({ filter: (req,res) => req.headers.accept?.includes('json') }));

// Q36. CORS configuration:
const cors = require('cors');
const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') ?? [];
app.use(cors({
  origin: (origin, cb) => {
    if(!origin || allowedOrigins.includes(origin)) cb(null, true);
    else cb(new Error('CORS blocked'));
  },
  credentials: true,
  methods: ['GET','POST','PUT','PATCH','DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Q37. Express Router organization:
const router = express.Router({ mergeParams: true }); // inherit parent params
router.param('userId', async (req, res, next, id) => {
  req.user = await getUser(id); // load user once for all userId routes
  if (!req.user) return res.status(404).json({ error: 'User not found' });
  next();
});
router.get('/:userId/orders', (req,res) => res.json(req.user.orders));

// Q38. Express caching with ETags:
const etag = require('etag');
app.get('/users', async (req, res) => {
  const users = await getUsers();
  const tag = etag(JSON.stringify(users));
  if (req.headers['if-none-match'] === tag) return res.status(304).end();
  res.setHeader('ETag', tag);
  res.setHeader('Cache-Control', 'public, max-age=60');
  res.json(users);
});

// Q39. Node.js crypto:
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update(data).digest('hex');
const hmac = crypto.createHmac('sha256', secret).update(data).digest('hex');
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const encrypted = crypto.publicEncrypt(publicKey, Buffer.from(message));
const decrypted = crypto.privateDecrypt(privateKey, encrypted).toString();

// Q40. Environment-based config:
const config = {
  port: Number(process.env.PORT) || 3000,
  db: {
    url: process.env.DATABASE_URL,
    pool: { max: Number(process.env.DB_POOL_MAX) || 10 }
  },
  jwt: { secret: process.env.JWT_SECRET, expiresIn: '15m' },
};
if (!config.db.url) throw new Error('DATABASE_URL is required');

// Q41–Q80: Key patterns
// Q41. Health check endpoint with dependency checks
// Q42. Graceful shutdown sequence: stop accepting, drain, close connections
// Q43. Circuit breaker with opossum library
// Q44. Retry with exponential backoff for HTTP calls
// Q45. Request deduplication: cache in-flight requests
// Q46. Timeout wrapper for async operations
// Q47. Memory profiling: node --inspect, heapdump, clinic.js
// Q48. CPU profiling: --prof flag, v8-profiler-next, autocannon
// Q49. Leak detection: heapdump + Chrome DevTools comparison
// Q50. Tracing with OpenTelemetry auto-instrumentation
// Q51. Structured logging: pino, winston with JSON output
// Q52. Log levels in production: info for normal ops, debug only on-demand
// Q53. Request correlation: AsyncLocalStorage for trace context
// Q54. API versioning: URL prefix /v1/, header, or URL suffix
// Q55. Pagination cursor-based for consistent results
// Q56. Background jobs: bull queue + Redis, agenda, node-cron
// Q57. Email sending: nodemailer + SMTP, SendGrid/SES API
// Q58. PDF generation: puppeteer (headless Chrome), pdfkit
// Q59. Image processing: sharp (libvips), jimp for simpler ops
// Q60. CSV/Excel processing: fast-csv, exceljs

// Q61–Q100: Advanced Node.js
// Q61. REPL: interactive Node shell, useful for debugging
// Q62. vm module: execute code in sandbox (careful! not truly secure)
// Q63. child_process.spawn vs exec vs fork
// Q64. fork: creates Node.js child with IPC channel
// Q65. cluster module internals: master routes connections to workers
// Q66. worker_threads shared memory via SharedArrayBuffer
// Q67. Atomics for thread-safe operations on shared buffer
// Q68. HTTP agent: connection pooling for outgoing HTTP
// Q69. keep-alive: reuse TCP connections (5x faster for many requests)
// Q70. DNS caching: cache DNS lookups to reduce latency
// Q71. IPv4 vs IPv6 in Node.js: ::1 vs 127.0.0.1 listen
// Q72. Unix socket vs TCP: unix sockets faster for local IPC
// Q73. HTTPS module vs http + tls: https = convenience wrapper
// Q74. HTTP/2 with Node.js: http2 module or express + spdy
// Q75. HTTP/3 with QUIC: experimental in Node.js 22+
// Q76. Server timing API: Server-Timing header for browser DevTools
// Q77. Content negotiation: Accept header, res.format()
// Q78. Conditional GET: ETag, Last-Modified, 304 responses
// Q79. Range requests: partial content delivery (video streaming)
// Q80. Multipart: handle form data, file uploads with boundaries

// Q81–Q120: Production patterns
// Q81. Zero-downtime deploy: rolling, blue/green with process manager
// Q82. Feature flags: LaunchDarkly, Unleash, or custom Redis flags
// Q83. Config hot reload: fs.watch on config, SIGHUP signal
// Q84. Memory limits: --max-old-space-size, auto-restart on OOM
// Q85. CPU affinity: pin workers to specific CPU cores
// Q86. Node.js in Docker: non-root user, health check, signal handling
// Q87. Multi-stage Docker: build stage then production stage
// Q88. npm ci vs npm install: ci is deterministic, faster in CI
// Q89. package-lock.json: exact versions, commit to repo
// Q90. Dependency security: npm audit, dependabot, snyk
// Q91. ESM migration: .mjs, type:module, dynamic import
// Q92. TypeScript with ts-node-dev, esbuild-register, tsx
// Q93. Testing Express: supertest for integration, jest for unit
// Q94. Mock external services: nock, msw, test containers
// Q95. Load testing: autocannon, k6, artillery
// Q96. Benchmarking: benchmark.js, node --perf-prof
// Q97. Node.js native addons: N-API, node-gyp for C++ modules
// Q98. WebAssembly in Node.js: wasm for CPU-intensive tasks
// Q99. Streams vs buffers: streams for large data, buffers for small
// Q100. Backpressure handling: highWaterMark, pause/resume
// Q101–Q120: Express routing, middleware chains, error propagation patterns
```
