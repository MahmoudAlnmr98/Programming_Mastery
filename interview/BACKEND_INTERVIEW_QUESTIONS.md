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

---

This covers backend interview questions from beginner to advanced level with comprehensive coverage of essential topics.

