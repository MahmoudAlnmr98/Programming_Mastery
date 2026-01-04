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

---

## Intermediate Level

### 9. Explain microservices architecture.

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

### 10. Explain message queues.

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

### 11. Explain API Gateway pattern.

**Answer:**
Single entry point for all client requests.

**Functions:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Load balancing
- Request/Response transformation

### 12. Explain circuit breaker pattern.

**Answer:**
Prevents cascading failures.

**States:**
- **Closed**: Normal operation
- **Open**: Failing, reject requests
- **Half-Open**: Testing if service recovered

### 13. Explain database transactions.

**Answer:**
Group of operations that must all succeed or all fail.

**ACID Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

### 14. Explain load balancing.

**Answer:**
Distribute requests across multiple servers.

**Algorithms:**
- Round Robin
- Least Connections
- Weighted Round Robin
- IP Hash

---

## Advanced Level

### 15. Explain distributed systems challenges.

**Answer:**
- **Network Partitions**: Network splits
- **Clock Skew**: Different clocks
- **Split-Brain**: Multiple leaders
- **Consensus**: Agreement on value

### 16. Explain CAP theorem.

**Answer:**
Can have at most 2 of 3:
- **Consistency**: All nodes see same data
- **Availability**: System operational
- **Partition Tolerance**: Works despite network failures

### 17. Explain event-driven architecture.

**Answer:**
Components communicate via events.

**Benefits:**
- Loose coupling
- Scalability
- Flexibility

**Patterns:**
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)

---

This covers backend interview questions from beginner to advanced level.

