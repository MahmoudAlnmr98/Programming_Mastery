# Backend Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. Explain RESTful API principles.

**Answer:**
REST (Representational State Transfer) principles:

- **Stateless**: Each request contains all information
- **Resource-Based**: URLs represent resources
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- **Status Codes**: 200, 201, 400, 404, 500
- **JSON/XML**: Data formats

### 2. Explain HTTP methods and their usage.

**Answer:**
- **GET**: Retrieve resource (idempotent, safe)
- **POST**: Create resource (not idempotent)
- **PUT**: Update resource (full update, idempotent)
- **PATCH**: Partial update (not idempotent)
- **DELETE**: Delete resource (idempotent)

### 3. Explain HTTP status codes.

**Answer:**
**2xx Success:**
- 200: OK
- 201: Created
- 204: No Content

**4xx Client Error:**
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict

**5xx Server Error:**
- 500: Internal Server Error
- 502: Bad Gateway
- 503: Service Unavailable

### 4. Explain authentication vs authorization.

**Answer:**
- **Authentication**: Who you are (login)
- **Authorization**: What you can do (permissions)

**Methods:**
- **Basic Auth**: Username/password
- **Token-based**: JWT tokens
- **OAuth**: Third-party authentication
- **Session-based**: Server-side sessions

### 5. Explain API versioning strategies.

**Answer:**
**URL Versioning:**
```
/api/v1/users
/api/v2/users
```

**Header Versioning:**
```
Accept: application/vnd.api.v1+json
```

**Query Parameter:**
```
/api/users?version=1
```

### 6. Explain database connection pooling.

**Answer:**
Connection pool reuses database connections.

**Benefits:**
- Reduces connection overhead
- Limits concurrent connections
- Better resource management

**Implementation:**
```java
// Java example
DataSource dataSource = new HikariDataSource();
dataSource.setMaximumPoolSize(20);
dataSource.setMinimumIdle(5);
```

### 7. Explain caching strategies.

**Answer:**
**Cache-Aside:**
- Application checks cache
- If miss, loads from database and caches

**Write-Through:**
- Write to cache and database simultaneously

**Write-Back:**
- Write to cache, write to database later

### 8. Explain API rate limiting.

**Answer:**
Limit number of requests per time period.

**Algorithms:**
- **Token Bucket**: Tokens added at rate
- **Leaky Bucket**: Requests processed at rate
- **Fixed Window**: Count in time window
- **Sliding Window**: Count in sliding window

### 9. Explain webhooks.

**Answer:**
Webhooks are HTTP callbacks triggered by events.

**How it works:**
1. Client registers webhook URL
2. Server sends HTTP POST to URL when event occurs
3. Client processes the event

**Use Cases:**
- Payment notifications
- CI/CD deployments
- Real-time updates
- Third-party integrations

**Example:**
```javascript
// Register webhook
POST /api/webhooks
{
  "url": "https://example.com/callback",
  "events": ["payment.completed", "order.shipped"]
}

// Server sends webhook
POST https://example.com/callback
{
  "event": "payment.completed",
  "data": { "orderId": "123", "amount": 100 }
}
```

### 10. Explain GraphQL vs REST.

**Answer:**
**REST:**
- Multiple endpoints per resource
- Over-fetching/under-fetching
- Fixed response structure
- HTTP methods for operations

**GraphQL:**
- Single endpoint
- Client specifies needed fields
- Flexible queries
- Type system

**Example:**
```graphql
# GraphQL query
query {
  user(id: "1") {
    name
    email
    posts {
      title
    }
  }
}
```

---

## Intermediate Level

### 11. Explain microservices architecture.

**Answer:**
Breaking application into independent services.

**Benefits:**
- Independent deployment
- Technology diversity
- Scalability
- Fault isolation

**Challenges:**
- Service communication
- Data consistency
- Distributed transactions
- Complexity

### 12. Explain message queues.

**Answer:**
Asynchronous communication between services.

**Benefits:**
- Decoupling
- Reliability
- Scalability
- Asynchronous processing

**Examples:**
- RabbitMQ
- Apache Kafka
- AWS SQS

### 13. Explain API Gateway pattern.

**Answer:**
Single entry point for all client requests.

**Functions:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Load balancing
- Request/Response transformation

### 14. Explain circuit breaker pattern.

**Answer:**
Prevents cascading failures.

**States:**
- **Closed**: Normal operation
- **Open**: Failing, reject requests
- **Half-Open**: Testing if service recovered

### 15. Explain database transactions.

**Answer:**
Group of operations that must all succeed or all fail.

**ACID Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

### 16. Explain load balancing.

**Answer:**
Distribute requests across multiple servers.

**Algorithms:**
- Round Robin
- Least Connections
- Weighted Round Robin
- IP Hash

### 17. Explain JWT (JSON Web Tokens) in detail.

**Answer:**
JWT is a compact token format for authentication.

**Structure:**
- **Header**: Algorithm and token type
- **Payload**: Claims (user data)
- **Signature**: Verifies token integrity

**Example:**
```javascript
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

**Benefits:**
- Stateless
- Scalable
- Self-contained

**Security:**
- Use HTTPS
- Short expiration
- Store secrets securely
- Validate signature

### 18. Explain OAuth 2.0 flow.

**Answer:**
OAuth 2.0 is authorization framework.

**Authorization Code Flow:**
1. Client redirects user to authorization server
2. User authorizes
3. Server returns authorization code
4. Client exchanges code for access token
5. Client uses access token for API calls

**Grant Types:**
- **Authorization Code**: Web apps
- **Client Credentials**: Server-to-server
- **Implicit**: Deprecated
- **Refresh Token**: Get new access token

### 19. Explain API documentation best practices.

**Answer:**
**Tools:**
- OpenAPI/Swagger
- Postman Collections
- API Blueprint

**Best Practices:**
- Document all endpoints
- Include request/response examples
- Document error codes
- Include authentication
- Version documentation
- Interactive examples

### 20. Explain health checks and monitoring.

**Answer:**
**Health Check Endpoints:**
```javascript
GET /health
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "uptime": 3600
}
```

**Monitoring:**
- **Metrics**: Response time, error rate, throughput
- **Logging**: Structured logs, log aggregation
- **Alerting**: Set thresholds, notify on issues
- **Tracing**: Distributed tracing for microservices

---

## Advanced Level

### 21. Explain distributed systems challenges.

**Answer:**
- **Network Partitions**: Network splits
- **Clock Skew**: Different clocks
- **Split-Brain**: Multiple leaders
- **Consensus**: Agreement on value

### 22. Explain CAP theorem.

**Answer:**
Can have at most 2 of 3:
- **Consistency**: All nodes see same data
- **Availability**: System operational
- **Partition Tolerance**: Works despite network failures

### 23. Explain event-driven architecture.

**Answer:**
Components communicate via events.

**Benefits:**
- Loose coupling
- Scalability
- Flexibility

**Patterns:**
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)

### 24. Explain Saga pattern for distributed transactions.

**Answer:**
Saga manages distributed transactions across services.

**Choreography:**
- Services publish events
- Each service reacts to events
- No central coordinator

**Orchestration:**
- Central orchestrator coordinates
- Sends commands to services
- Manages rollback

**Example:**
```javascript
// Order Saga
1. Create Order
2. Reserve Inventory
3. Process Payment
4. If any fails, compensate (rollback)
```

### 25. Explain API security best practices.

**Answer:**
**Authentication:**
- Use JWT or OAuth 2.0
- Implement refresh tokens
- Secure token storage

**Authorization:**
- Role-based access control (RBAC)
- Resource-level permissions
- Principle of least privilege

**Input Validation:**
- Validate all inputs
- Sanitize data
- Use parameterized queries

**Rate Limiting:**
- Prevent abuse
- Protect against DDoS
- Implement per-user limits

**HTTPS:**
- Encrypt all traffic
- Use TLS 1.2+
- Validate certificates

**Other:**
- CORS configuration
- API versioning
- Error handling (don't leak info)
- Logging and monitoring

### 26. Explain request/response compression.

**Answer:**
Compression reduces payload size.

**Algorithms:**
- **Gzip**: Good compression, widely supported
- **Brotli**: Better compression than Gzip
- **Deflate**: Older, less efficient

**Implementation:**
```javascript
// Express.js example
const compression = require('compression');
app.use(compression());

// Client request
Accept-Encoding: gzip, deflate, br

// Server response
Content-Encoding: gzip
```

**Benefits:**
- Faster transfers
- Reduced bandwidth
- Better user experience

### 27. Explain idempotency in APIs.

**Answer:**
Idempotent operations produce same result when called multiple times.

**Idempotent Methods:**
- GET, PUT, DELETE (by HTTP spec)
- POST (if designed to be)

**Implementation:**
```javascript
// Using idempotency key
POST /api/orders
Idempotency-Key: unique-key-123

// Server checks if key exists
if (idempotencyKeyExists(key)) {
  return previousResponse;
}
// Process and store response
```

**Benefits:**
- Safe retries
- Prevents duplicate operations
- Better error handling

### 28. Explain CI/CD pipelines and best practices.

**Answer:**
CI/CD automates building, testing, and deployment.

**CI (Continuous Integration):**
- Automatically build on code changes
- Run tests
- Check code quality
- Generate artifacts

**CD (Continuous Deployment/Delivery):**
- Automatically deploy to environments
- Run integration tests
- Monitor deployment

**Pipeline Stages:**
```yaml
# Example: GitHub Actions
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run build
      - name: Deploy
        run: npm run deploy
```

**Best Practices:**
- Fast feedback loops
- Automated testing
- Environment parity
- Version control everything
- Rollback capability
- Monitoring and alerts

### 29. Explain monitoring and logging strategies.

**Answer:**
**Monitoring:**
- **Metrics**: CPU, memory, response time, error rate
- **Logging**: Application logs, error logs, access logs
- **Tracing**: Distributed tracing for microservices
- **Alerting**: Notify on thresholds

**Logging Best Practices:**
```javascript
// Structured logging
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

// Log levels
logger.error('Error occurred', { error, userId, requestId });
logger.warn('Warning message', { context });
logger.info('Info message', { data });
logger.debug('Debug message', { details });
```

**Metrics:**
- **Counters**: Total requests, errors
- **Gauges**: Current connections, queue size
- **Histograms**: Response time distribution
- **Timers**: Operation duration

**Tools:**
- **Logging**: ELK Stack, Splunk, CloudWatch
- **Metrics**: Prometheus, Grafana, Datadog
- **Tracing**: Jaeger, Zipkin, AWS X-Ray

### 30. Explain deployment strategies.

**Answer:**
**Blue-Green Deployment:**
- Two identical environments
- Switch traffic from blue to green
- Instant rollback

**Canary Deployment:**
- Deploy to small subset
- Monitor metrics
- Gradually increase traffic
- Rollback if issues

**Rolling Deployment:**
- Update instances gradually
- No downtime
- Slower deployment

**A/B Testing:**
- Deploy different versions
- Route traffic based on criteria
- Compare metrics

**Example:**
```bash
# Blue-Green with Docker
docker-compose -f docker-compose.blue.yml up -d
# Test blue
# Switch load balancer to blue
docker-compose -f docker-compose.green.yml up -d
# Test green
# Switch load balancer to green
docker-compose -f docker-compose.blue.yml down
```

### 31. Explain API security vulnerabilities and prevention.

**Answer:**
**Common Vulnerabilities:**

**1. SQL Injection:**
```javascript
// Vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Safe
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

**2. XSS (Cross-Site Scripting):**
```javascript
// Sanitize inputs
const sanitize = require('sanitize-html');
const clean = sanitize(userInput);
```

**3. CSRF (Cross-Site Request Forgery):**
```javascript
// Use CSRF tokens
const csrf = require('csurf');
app.use(csrf({ cookie: true }));

app.get('/form', (req, res) => {
    res.render('form', { csrfToken: req.csrfToken() });
});
```

**4. Authentication Bypass:**
- Use strong authentication
- Implement rate limiting
- Validate tokens properly
- Use HTTPS

**5. Insecure Direct Object References:**
```javascript
// Check authorization
app.get('/users/:id', authenticate, async (req, res) => {
    if (req.user.id !== req.params.id && !req.user.isAdmin) {
        return res.status(403).json({ error: 'Forbidden' });
    }
    // Return user data
});
```

### 32. Explain database migration strategies.

**Answer:**
**Migration Types:**
- **Schema Changes**: Add/remove columns, tables
- **Data Migrations**: Transform data
- **Rollback**: Revert changes

**Best Practices:**
```javascript
// Example: Using Knex.js
exports.up = function(knex) {
    return knex.schema.createTable('users', function(table) {
        table.increments('id');
        table.string('email').unique();
        table.string('password');
        table.timestamps();
    });
};

exports.down = function(knex) {
    return knex.schema.dropTable('users');
};
```

**Migration Strategy:**
1. **Backward Compatible**: Add columns as nullable first
2. **Gradual Rollout**: Migrate data in batches
3. **Feature Flags**: Enable new schema gradually
4. **Rollback Plan**: Always have rollback ready

**Zero-Downtime Migrations:**
- Add new column (nullable)
- Deploy code that writes to both
- Migrate existing data
- Deploy code that reads from new column
- Remove old column

### 33. Explain API documentation with OpenAPI/Swagger.

**Answer:**
OpenAPI/Swagger provides API documentation and testing.

**Example:**
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
```

**Integration:**
```javascript
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'API',
            version: '1.0.0',
        },
    },
    apis: ['./routes/*.js'],
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
```

### 34. Explain Microservices Communication Patterns.

**Answer:**
**Synchronous:**
- REST API
- gRPC
- GraphQL

**Asynchronous:**
- Message Queue (RabbitMQ, Kafka)
- Event Bus
- Pub/Sub

**Service Mesh:**
- Istio, Linkerd
- Handles service-to-service communication

### 35. Explain API Gateway Pattern.

**Answer:**
Single entry point for all client requests.

**Functions:**
- Routing
- Authentication
- Rate limiting
- Load balancing
- Request/response transformation

**Example:**
```
Client → API Gateway → [Service 1] [Service 2] [Service 3]
```

**Benefits:**
- Centralized cross-cutting concerns
- Simplified client
- Service abstraction

### 36. Explain Circuit Breaker Pattern.

**Answer:**
Prevents cascading failures.

**States:**
- Closed: Normal operation
- Open: Failing, reject requests
- Half-Open: Testing if service recovered

**Implementation:**
```javascript
class CircuitBreaker {
    constructor(threshold = 5, timeout = 60000) {
        this.failureCount = 0;
        this.threshold = threshold;
        this.timeout = timeout;
        this.state = 'CLOSED';
    }
    
    async execute(fn) {
        if (this.state === 'OPEN') {
            throw new Error('Circuit breaker is OPEN');
        }
        
        try {
            const result = await fn();
            this.onSuccess();
            return result;
        } catch (error) {
            this.onFailure();
            throw error;
        }
    }
    
    onSuccess() {
        this.failureCount = 0;
        this.state = 'CLOSED';
    }
    
    onFailure() {
        this.failureCount++;
        if (this.failureCount >= this.threshold) {
            this.state = 'OPEN';
            setTimeout(() => {
                this.state = 'HALF_OPEN';
            }, this.timeout);
        }
    }
}
```

### 37. Explain Saga Pattern.

**Answer:**
Manages distributed transactions.

**Choreography:**
- Each service knows what to do next
- Services communicate via events

**Orchestration:**
- Central orchestrator coordinates
- Services respond to commands

**Compensating Transactions:**
- Each step has compensating action
- Rollback on failure

### 38. Explain Event Sourcing.

**Answer:**
Store events instead of current state.

**Benefits:**
- Complete audit trail
- Time travel
- Replay events

**Example:**
```javascript
// Events
{ type: 'AccountCreated', accountId: '123', balance: 0 }
{ type: 'Deposit', accountId: '123', amount: 100 }
{ type: 'Withdrawal', accountId: '123', amount: 50 }

// Current state: balance = 50
```

### 39. Explain CQRS (Command Query Responsibility Segregation).

**Answer:**
Separate read and write models.

**Command Side:**
- Write operations
- Optimized for writes
- Normalized schema

**Query Side:**
- Read operations
- Optimized for reads
- Denormalized schema

**Benefits:**
- Independent scaling
- Optimized for each operation
- Better performance

### 40. Explain Database Sharding.

**Answer:**
Horizontal partitioning of database.

**Sharding Strategies:**
- Range-based: By ID range
- Hash-based: Hash function
- Directory-based: Lookup table

**Challenges:**
- Cross-shard queries
- Rebalancing
- Joins across shards

### 41. Explain Database Replication.

**Answer:**
Copy data across multiple servers.

**Types:**
- Master-Slave: One master, multiple slaves
- Master-Master: Multiple masters
- Multi-Master: All nodes can write

**Benefits:**
- High availability
- Read scalability
- Disaster recovery

### 42. Explain Load Balancing Algorithms.

**Answer:**
**Round Robin:**
- Distribute requests sequentially

**Least Connections:**
- Route to server with fewest connections

**Weighted Round Robin:**
- Assign weights to servers

**IP Hash:**
- Hash client IP to server

**Geographic:**
- Route based on location

### 43. Explain Health Checks and Monitoring.

**Answer:**
**Health Checks:**
```javascript
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: Date.now(),
        uptime: process.uptime()
    });
});
```

**Metrics:**
- Response time
- Error rate
- Throughput
- Resource usage

**Tools:**
- Prometheus
- Grafana
- New Relic
- Datadog

### 44. Explain Distributed Tracing.

**Answer:**
Track requests across services.

**Concepts:**
- Trace: Complete request journey
- Span: Single operation
- Context: Propagation between services

**Tools:**
- Jaeger
- Zipkin
- AWS X-Ray

### 45. Explain API Rate Limiting Strategies.

**Answer:**
**Fixed Window:**
- Count requests in time window

**Sliding Window:**
- Count requests in sliding window

**Token Bucket:**
- Tokens added at rate
- Request consumes token

**Leaky Bucket:**
- Requests added to bucket
- Processed at fixed rate

**Implementation:**
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests
});

app.use('/api/', limiter);
```

### 46. Explain Message Queue Patterns.

**Answer:**
**Point-to-Point:**
- One producer, one consumer
- Message consumed once

**Pub/Sub:**
- One producer, multiple consumers
- Message broadcast to all

**Request/Reply:**
- Request message
- Reply message with correlation ID

**Work Queue:**
- Multiple workers
- Load distribution

### 47. Explain Backend Caching Strategies.

**Answer:**
**Cache-Aside:**
```javascript
async function getData(key) {
    let data = await cache.get(key);
    if (!data) {
        data = await db.query(key);
        await cache.set(key, data);
    }
    return data;
}
```

**Write-Through:**
- Write to cache and DB simultaneously

**Write-Back:**
- Write to cache first
- Write to DB asynchronously

**Refresh-Ahead:**
- Refresh cache before expiration

### 48. Explain Backend Security Best Practices.

**Answer:**
**1. Authentication:**
- JWT tokens
- OAuth 2.0
- Session management

**2. Authorization:**
- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)

**3. Input Validation:**
- Validate all inputs
- Sanitize data
- Parameterized queries

**4. Encryption:**
- HTTPS/TLS
- Encrypt sensitive data at rest
- Hash passwords (bcrypt, argon2)

**5. Security Headers:**
- CORS
- CSP
- X-Frame-Options
- X-XSS-Protection

### 49. Explain GraphQL vs REST.

**Answer:**
**REST:**
- Multiple endpoints
- Fixed data structure
- Over-fetching/under-fetching

**GraphQL:**
- Single endpoint
- Flexible queries
- Client specifies fields

**Example:**
```graphql
query {
    user(id: "123") {
        name
        email
        posts {
            title
        }
    }
}
```

### 50. Explain WebSocket vs HTTP.

**Answer:**
**HTTP:**
- Request-response
- Stateless
- One-way communication

**WebSocket:**
- Persistent connection
- Bidirectional
- Real-time communication

**Use Cases:**
- HTTP: REST APIs, web pages
- WebSocket: Chat, gaming, real-time updates

### 51. Explain RESTful API Design Best Practices.

**Answer:**
**Resource Naming:**
```
GET    /api/users           # List users
GET    /api/users/123       # Get user
POST   /api/users           # Create user
PUT    /api/users/123       # Update user (full)
PATCH  /api/users/123       # Update user (partial)
DELETE /api/users/123       # Delete user
```

**Status Codes:**
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

**Versioning:**
```
/api/v1/users
/api/v2/users
```

### 52. Explain API Pagination Strategies.

**Answer:**
**Offset-Based:**
```
GET /api/users?page=1&limit=10
```

**Cursor-Based:**
```
GET /api/users?cursor=abc123&limit=10
```

**Keyset Pagination:**
```
GET /api/users?last_id=123&limit=10
```

**Benefits:**
- Cursor-based: Better for large datasets
- Offset-based: Simple, allows jumping to page

### 53. Explain API Filtering, Sorting, and Searching.

**Answer:**
**Filtering:**
```
GET /api/users?status=active&role=admin
```

**Sorting:**
```
GET /api/users?sort=name&order=asc
```

**Searching:**
```
GET /api/users?search=john
```

**Implementation:**
```javascript
app.get('/api/users', (req, res) => {
    let query = User.find();
    
    if (req.query.status) {
        query = query.where('status').equals(req.query.status);
    }
    
    if (req.query.sort) {
        const order = req.query.order === 'desc' ? -1 : 1;
        query = query.sort({ [req.query.sort]: order });
    }
    
    query.exec((err, users) => {
        res.json(users);
    });
});
```

### 54. Explain API Authentication Methods.

**Answer:**
**1. Basic Auth:**
```javascript
// Client sends: Authorization: Basic base64(username:password)
const auth = Buffer.from(`${username}:${password}`).toString('base64');
```

**2. Bearer Token (JWT):**
```javascript
// Client sends: Authorization: Bearer <token>
const token = jwt.sign({ userId: 123 }, secret);
```

**3. API Keys:**
```javascript
// Client sends: X-API-Key: <key>
app.use((req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    if (!isValidKey(apiKey)) {
        return res.status(401).json({ error: 'Invalid API key' });
    }
    next();
});
```

**4. OAuth 2.0:**
- Authorization code flow
- Client credentials flow
- Implicit flow

### 55. Explain API Response Formatting.

**Answer:**
**Consistent Format:**
```javascript
// Success
{
    "status": "success",
    "data": { ... },
    "message": "User created successfully"
}

// Error
{
    "status": "error",
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid email format",
        "details": { ... }
    }
}
```

**Pagination:**
```javascript
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 10,
        "total": 100,
        "totalPages": 10
    }
}
```

### 56. Explain Database Connection Pooling.

**Answer:**
Connection pool reuses database connections.

**Benefits:**
- Reduces connection overhead
- Limits concurrent connections
- Better resource management

**Configuration:**
```javascript
const pool = new Pool({
    host: 'localhost',
    database: 'mydb',
    user: 'user',
    password: 'password',
    max: 20, // Maximum connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000
});
```

### 57. Explain Backend Logging Best Practices.

**Answer:**
**Structured Logging:**
```javascript
logger.info('User created', {
    userId: 123,
    email: 'user@example.com',
    timestamp: new Date()
});
```

**Log Levels:**
- ERROR: Errors that need attention
- WARN: Warning messages
- INFO: Informational messages
- DEBUG: Debug information

**Best Practices:**
- Use structured logging (JSON)
- Include context (user ID, request ID)
- Don't log sensitive data
- Centralized logging

### 58. Explain Backend Error Handling Patterns.

**Answer:**
**Custom Error Classes:**
```javascript
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

class ValidationError extends AppError {
    constructor(message) {
        super(message, 400);
    }
}
```

**Error Handler:**
```javascript
app.use((err, req, res, next) => {
    if (err.isOperational) {
        return res.status(err.statusCode).json({
            status: 'error',
            message: err.message
        });
    }
    
    // Log unexpected errors
    logger.error(err);
    
    res.status(500).json({
        status: 'error',
        message: 'Internal server error'
    });
});
```

### 59. Explain Backend Testing Strategies.

**Answer:**
**Unit Tests:**
```javascript
test('should create user', async () => {
    const user = await userService.createUser({
        name: 'John',
        email: 'john@example.com'
    });
    
    expect(user.name).toBe('John');
});
```

**Integration Tests:**
```javascript
test('POST /api/users', async () => {
    const response = await request(app)
        .post('/api/users')
        .send({ name: 'John', email: 'john@example.com' })
        .expect(201);
    
    expect(response.body).toHaveProperty('id');
});
```

**Test Types:**
- Unit: Test individual functions
- Integration: Test API endpoints
- E2E: Test complete flows

### 60. Explain Backend Deployment Strategies.

**Answer:**
**Blue-Green Deployment:**
- Two identical environments
- Switch traffic between them
- Zero downtime

**Canary Deployment:**
- Deploy to subset of servers
- Gradually increase traffic
- Rollback if issues

**Rolling Deployment:**
- Deploy to servers one by one
- No downtime
- Slower process

### 61. Explain Backend Monitoring and Alerting.

**Answer:**
**Key Metrics:**
- Response time (p50, p95, p99)
- Error rate
- Throughput (requests/second)
- Resource usage (CPU, memory)

**Alerting:**
- Set thresholds
- Notify on anomalies
- Use tools: Prometheus, Grafana, Datadog

### 62. Explain Backend Scalability Patterns.

**Answer:**
**Vertical Scaling:**
- Increase server resources
- Limited by hardware

**Horizontal Scaling:**
- Add more servers
- Requires load balancing
- Stateless services

**Database Scaling:**
- Read replicas
- Sharding
- Caching

### 63. Explain Backend Data Validation.

**Answer:**
**Input Validation:**
```javascript
const schema = {
    email: {
        type: 'string',
        required: true,
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    },
    age: {
        type: 'number',
        min: 18,
        max: 100
    }
};

function validate(data, schema) {
    // Validation logic
}
```

**Libraries:**
- Joi (Node.js)
- Validator.js
- express-validator

### 64. Explain Backend File Upload Handling.

**Answer:**
**Multipart Form Data:**
```javascript
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
    res.json({ file: req.file });
});
```

**Best Practices:**
- Validate file type
- Limit file size
- Scan for viruses
- Store in object storage (S3)

### 65. Explain Backend Background Jobs.

**Answer:**
**Job Queue:**
```javascript
const Bull = require('bull');
const queue = new Bull('email-queue');

queue.process(async (job) => {
    await sendEmail(job.data);
});

queue.add({ to: 'user@example.com', subject: 'Hello' });
```

**Use Cases:**
- Email sending
- Image processing
- Report generation
- Data synchronization

### 66. Explain Backend API Versioning Strategies.

**Answer:**
**URL Versioning:**
```
/api/v1/users
/api/v2/users
```

**Header Versioning:**
```
Accept: application/vnd.api+json;version=1
```

**Query Parameter:**
```
/api/users?version=1
```

**Best Practice:** URL versioning is most common and explicit.

### 67. Explain Backend Request Validation.

**Answer:**
**Input Validation:**
```javascript
const schema = {
    email: {
        type: 'string',
        required: true,
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    },
    age: {
        type: 'number',
        min: 18,
        max: 100
    }
};

function validate(data, schema) {
    // Validation logic
    for (const [key, rules] of Object.entries(schema)) {
        if (rules.required && !data[key]) {
            throw new Error(`${key} is required`);
        }
        // More validation...
    }
}
```

**Libraries:**
- Joi
- express-validator
- yup

### 68. Explain Backend API Response Caching.

**Answer:**
**HTTP Caching:**
```javascript
app.get('/api/users', (req, res) => {
    res.set('Cache-Control', 'public, max-age=3600');
    res.json(users);
});
```

**Redis Caching:**
```javascript
async function getUsers() {
    const cached = await redis.get('users');
    if (cached) return JSON.parse(cached);
    
    const users = await db.query('SELECT * FROM users');
    await redis.setex('users', 3600, JSON.stringify(users));
    return users;
}
```

### 69. Explain Backend Database Migrations.

**Answer:**
**Migration Example:**
```javascript
// migrations/001_create_users.js
exports.up = function(knex) {
    return knex.schema.createTable('users', table => {
        table.increments('id');
        table.string('email').unique();
        table.string('name');
        table.timestamps();
    });
};

exports.down = function(knex) {
    return knex.schema.dropTable('users');
};
```

**Tools:**
- Knex.js
- Sequelize migrations
- TypeORM migrations

### 70. Explain Backend API Documentation.

**Answer:**
**Swagger/OpenAPI:**
```javascript
const swaggerJsdoc = require('swagger-jsdoc');

const swaggerSpec = swaggerJsdoc({
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'API',
            version: '1.0.0',
        },
    },
    apis: ['./routes/*.js'],
});

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
```

**JSDoc Comments:**
```javascript
/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: Get all users
 *     responses:
 *       200:
 *         description: List of users
 */
app.get('/api/users', getUsers);
```

### 71. Explain Backend Request/Response Interceptors.

**Answer:**
**Request Interceptor:**
```javascript
app.use((req, res, next) => {
    // Log request
    console.log(`${req.method} ${req.path}`);
    
    // Add request ID
    req.id = generateId();
    
    // Modify request
    req.timestamp = Date.now();
    
    next();
});
```

**Response Interceptor:**
```javascript
app.use((req, res, next) => {
    const originalSend = res.send;
    
    res.send = function(data) {
        // Modify response
        const response = {
            data: JSON.parse(data),
            timestamp: Date.now(),
            requestId: req.id
        };
        
        return originalSend.call(this, JSON.stringify(response));
    };
    
    next();
});
```

### 72. Explain Backend API Throttling.

**Answer:**
**Rate Limiting:**
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests
    message: 'Too many requests'
});

app.use('/api/', limiter);
```

**Per-User Throttling:**
```javascript
const userLimits = new Map();

function throttleUser(userId, limit) {
    const userLimit = userLimits.get(userId) || { count: 0, reset: Date.now() };
    
    if (Date.now() > userLimit.reset) {
        userLimit.count = 0;
        userLimit.reset = Date.now() + 60000;
    }
    
    if (userLimit.count >= limit) {
        throw new Error('Rate limit exceeded');
    }
    
    userLimit.count++;
    userLimits.set(userId, userLimit);
}
```

### 73. Explain Backend API Pagination Best Practices.

**Answer:**
**Offset-Based:**
```javascript
app.get('/api/users', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;
    
    const users = db.query('SELECT * FROM users LIMIT ? OFFSET ?', [limit, offset]);
    const total = db.query('SELECT COUNT(*) as count FROM users');
    
    res.json({
        data: users,
        pagination: {
            page,
            limit,
            total: total.count,
            totalPages: Math.ceil(total.count / limit)
        }
    });
});
```

**Cursor-Based:**
```javascript
app.get('/api/users', (req, res) => {
    const cursor = req.query.cursor;
    const limit = parseInt(req.query.limit) || 10;
    
    const users = db.query(
        'SELECT * FROM users WHERE id > ? ORDER BY id LIMIT ?',
        [cursor || 0, limit + 1]
    );
    
    const hasMore = users.length > limit;
    if (hasMore) users.pop();
    
    res.json({
        data: users,
        nextCursor: hasMore ? users[users.length - 1].id : null
    });
});
```

### 74. Explain Backend API Error Handling Best Practices.

**Answer:**
**Error Classes:**
```javascript
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
    }
}

class ValidationError extends AppError {
    constructor(message) {
        super(message, 400);
    }
}

class NotFoundError extends AppError {
    constructor(resource) {
        super(`${resource} not found`, 404);
    }
}
```

**Error Handler:**
```javascript
app.use((err, req, res, next) => {
    if (err.isOperational) {
        return res.status(err.statusCode).json({
            status: 'error',
            message: err.message
        });
    }
    
    // Log unexpected errors
    logger.error(err);
    
    res.status(500).json({
        status: 'error',
        message: 'Internal server error'
    });
});
```

### 75. Explain Backend API Security Headers.

**Answer:**
**Security Headers:**
```javascript
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000');
    res.setHeader('Content-Security-Policy', "default-src 'self'");
    next();
});
```

**Helmet.js:**
```javascript
const helmet = require('helmet');
app.use(helmet());
```

---

This covers backend interview questions from beginner to advanced level with comprehensive coverage of essential topics.

