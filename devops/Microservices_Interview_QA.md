# Microservices Architecture — Interview Questions & Answers
> 100 questions. Service decomposition, communication, distributed transactions, observability, deployment.

---

## FOUNDATIONS (Q1-Q20)

**Q1. Monolith vs microservices — when to choose which.**
```
MONOLITH:
  Single deployable unit, shared database, direct function calls
  
  START HERE when:
  - Team < 10 engineers
  - Domain not well understood yet
  - Moving fast on product-market fit
  - Startup / early stage

  Problems that signal you should break apart:
  - Deploy one thing → need to test/redeploy everything
  - One team's bug brings down whole system
  - Can't scale one hot component independently
  - Team coordination overhead slowing everyone down

MICROSERVICES:
  Independent deployable services, each with own DB, communicating over network
  
  BENEFITS:
  - Independent deployment (deploy UserService without touching OrderService)
  - Independent scaling (scale checkout service 10x on Black Friday)
  - Technology heterogeneity (Java for payments, Node for notifications)
  - Fault isolation (notification failure doesn't break checkout)
  - Team autonomy (each team owns their service end-to-end)
  
  COSTS (often underestimated):
  - Network complexity (every call can fail, timeout, or be slow)
  - Distributed transactions (no single ACID transaction across services)
  - Observability complexity (trace a request across 10 services)
  - Testing complexity (integration testing requires many services running)
  - Operational overhead (10 services = 10 deployment pipelines)
  - Data consistency challenges (eventual consistency everywhere)
  
  WHEN TO USE:
  - Large engineering org (50+ engineers)
  - Clear domain boundaries
  - Need independent scaling
  - Multiple teams need to deploy independently

STRANGLER FIG PATTERN (safest migration):
  Don't rewrite monolith — add new features as services
  Gradually migrate existing functionality behind an API gateway
  Eventually the monolith is "strangled" (replaced piece by piece)
```

**Q2. Service decomposition — how to draw boundaries.**
```
DOMAIN-DRIVEN DESIGN (DDD) BOUNDARIES:
  Bounded Context = service boundary
  Each service owns its domain model completely
  No shared domain objects across services (copies OK, references by ID)

  Core domains (competitive advantage → invest most):
    Payment processing, recommendation engine, core marketplace logic
  
  Supporting domains (needed but not differentiating → buy or use SaaS):
    Authentication, notifications, analytics

DECOMPOSITION STRATEGIES:
  1. By business capability (recommended):
     UserService, OrderService, PaymentService, InventoryService, NotificationService
  
  2. By subdomain (DDD):
     Identify bounded contexts from domain model
  
  3. By data (anti-pattern — avoid):
     "UserDB Service" — leads to chatty services and tight coupling
  
  4. Strangler fig (migration):
     New features as services, migrate existing gradually

SIGNS OF BAD BOUNDARIES:
  - Services that always deploy together (should be one service)
  - Services that need to query each other's DBs (data coupling)
  - Single request goes through 10 services in sequence (deep coupling)
  - Circular dependencies between services

GOLDEN RULE:
  A service should be deployable and changeable independently.
  If changing Service A always requires changing Service B → wrong boundary.
```

**Q3. Service communication — sync vs async.**
```
SYNCHRONOUS (HTTP/gRPC):
  Service A calls Service B and waits for response
  
  Use when:
  - User is waiting for the result
  - Need immediate confirmation
  - Simple request-response
  
  Problems:
  - Cascading failures: B is slow → A hangs → A's callers hang → ...
  - Temporal coupling: A and B must both be running
  - Hard to scale: A is blocked waiting

  Mitigate with: Circuit breaker, timeouts, retries with backoff

ASYNCHRONOUS (message queues: Kafka, RabbitMQ, SQS):
  Service A publishes event → B processes when ready
  
  Use when:
  - User doesn't need immediate response
  - Decoupling is more important than latency
  - Reliable delivery required (retry if B is down)
  - Multiple consumers (fan-out)
  
  Benefits:
  - Temporal decoupling (A and B don't need to run simultaneously)
  - Back-pressure (B processes at its own pace)
  - Replay (process historical events again)
  - Audit log (all events are stored)
  
  Problems:
  - Eventual consistency
  - Harder to debug (async flows)
  - Message ordering challenges
  - At-least-once delivery requires idempotent consumers

DECISION RULE:
  User-facing, needs immediate result → Sync (HTTP/gRPC)
  Background processing, fire-and-forget → Async (Kafka/SQS)
  Multiple services need same event → Async (pub/sub)
```

**Q4. Inter-service communication patterns.**
```javascript
// SERVICE MESH (Istio/Linkerd):
// Handles: mTLS, retries, circuit breaking, tracing — without code changes
// Sidecar proxy (Envoy) injected alongside every service pod
// See iq_11_devops.md for full Istio configuration

// DIRECT HTTP (with resilience):
import CircuitBreaker from 'opossum';

const paymentBreaker = new CircuitBreaker(
  (orderId) => httpClient.post('/payments', { orderId }),
  {
    timeout: 3000,          // request timeout
    errorThresholdPercentage: 50, // open after 50% failure rate
    resetTimeout: 30000,    // try half-open after 30s
  }
);

paymentBreaker.fallback((orderId) => ({ status: 'pending', retry: true }));

// RETRY WITH EXPONENTIAL BACKOFF:
async function callWithRetry(fn, maxRetries = 3) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries) throw err;
      if (!isRetryable(err)) throw err; // 400, 401, 403 → don't retry
      const delay = Math.min(100 * 2 ** attempt + Math.random() * 100, 30000);
      await sleep(delay);
    }
  }
}

// SERVICE DISCOVERY:
// Kubernetes: DNS-based (service.namespace.svc.cluster.local)
// Consul: register on startup, health checks, DNS/HTTP API
// Eureka (Java/Spring): client-side load balancing

// BULKHEAD PATTERN — isolate failure:
// Separate thread pools/connection pools per downstream service
// Payment service slow → doesn't exhaust all connections for Notification service
const httpClients = {
  payments:      new HttpClient({ maxConnections: 10, timeout: 3000 }),
  notifications: new HttpClient({ maxConnections: 20, timeout: 1000 }),
  inventory:     new HttpClient({ maxConnections: 15, timeout: 2000 }),
};
```

**Q5. API Gateway patterns.**
```javascript
// API Gateway = single entry point for all external clients
// Handles: auth, routing, rate limiting, SSL, request transformation

// GATEWAY RESPONSIBILITIES:
//   Authentication: verify JWT before forwarding to services
//   Authorization: check permissions before routing
//   Rate limiting: per user/client/tier
//   SSL termination: HTTPS to gateway, HTTP to internal services
//   Request routing: /api/users → user-service, /api/orders → order-service
//   Request transformation: add headers, translate protocols
//   Response aggregation: call multiple services, combine responses
//   Caching: cache responses at gateway layer
//   Logging: centralized access logs
//   Circuit breaking: fail fast if downstream is down

// BFF (Backend for Frontend):
// Instead of one gateway for all clients:
// - Mobile BFF: smaller payloads, push notifications, mobile auth
// - Web BFF: server-side rendering, web sessions
// - Third-party BFF: rate-limited, public API keys, API versioning

// Kong configuration (declarative):
// plugins:
//   - name: jwt (auth)
//   - name: rate-limiting (config: minute: 60)
//   - name: cors
//   - name: request-transformer (add X-Service header)
//   - name: response-transformer (remove internal headers)
//   - name: prometheus (metrics)
//   - name: zipkin (tracing)

// AGGREGATION at gateway:
async function getUserDashboard(req, res) {
  const userId = req.params.id;
  const timeout = 3000;

  const [user, orders, notifications] = await Promise.allSettled([
    serviceCall('user-service', `/users/${userId}`, { timeout }),
    serviceCall('order-service', `/users/${userId}/orders?limit=5`, { timeout }),
    serviceCall('notification-service', `/users/${userId}/unread`, { timeout }),
  ]);

  res.json({
    user:          user.status === 'fulfilled' ? user.value : null,
    recentOrders:  orders.status === 'fulfilled' ? orders.value : [],
    notifications: notifications.status === 'fulfilled' ? notifications.value : { count: 0 },
  });
  // Partial failures return degraded but functional response
}
```

---

## DISTRIBUTED TRANSACTIONS (Q21-Q40)

**Q21. The distributed transaction problem.**
```
PROBLEM:
  Order service: debit account
  Inventory service: reserve item
  Shipping service: create shipment
  
  What if debit succeeds but inventory reservation fails?
  Can't use single ACID transaction across 3 separate databases!

OPTIONS:
  1. Two-phase commit (2PC) — avoid in microservices
     - Distributed lock prevents independent scaling
     - Coordinator failure = all participants blocked
     - Synchronous, slow
  
  2. SAGA pattern — standard microservices approach
     - Local transactions + compensating transactions
     - No distributed lock
     - Eventual consistency
  
  3. Choreography-based Saga
     Services react to events, no central coordinator
     Simpler, but harder to track overall flow
  
  4. Orchestration-based Saga
     Central coordinator directs each step
     Harder to deploy, but explicit flow visible in one place
```

**Q22. Saga pattern — orchestration vs choreography.**
```javascript
// ORCHESTRATION SAGA — central coordinator:
class OrderSaga {
  async execute(orderData) {
    const sagaId = generateId();
    
    // Step 1: Reserve inventory
    let inventoryReservation;
    try {
      inventoryReservation = await inventoryService.reserve(orderData.items);
    } catch (err) {
      await this.handleFailure(sagaId, 'inventory_failed', {});
      throw new SagaException('Inventory reservation failed', err);
    }

    // Step 2: Process payment
    let payment;
    try {
      payment = await paymentService.charge(orderData.userId, orderData.total);
    } catch (err) {
      // Compensate: release inventory reservation
      await inventoryService.release(inventoryReservation.id);
      throw new SagaException('Payment failed', err);
    }

    // Step 3: Create shipment
    try {
      await shippingService.createShipment(orderData, inventoryReservation);
    } catch (err) {
      // Compensate: refund payment + release inventory
      await paymentService.refund(payment.id);
      await inventoryService.release(inventoryReservation.id);
      throw new SagaException('Shipment creation failed', err);
    }

    await orderRepo.updateStatus(orderData.orderId, 'confirmed');
  }
}

// CHOREOGRAPHY SAGA — event-driven, no coordinator:
// OrderService:
eventBus.publish('order.created', { orderId, userId, items, total });

// InventoryService listens:
eventBus.on('order.created', async (event) => {
  try {
    await inventoryRepo.reserve(event.orderId, event.items);
    eventBus.publish('inventory.reserved', { orderId: event.orderId });
  } catch {
    eventBus.publish('inventory.reservation.failed', { orderId: event.orderId });
  }
});

// PaymentService listens for inventory.reserved:
eventBus.on('inventory.reserved', async (event) => {
  try {
    await paymentRepo.charge(event.orderId);
    eventBus.publish('payment.processed', { orderId: event.orderId });
  } catch {
    eventBus.publish('payment.failed', { orderId: event.orderId });
    // InventoryService listens for payment.failed and releases reservation
  }
});

// COMPARISON:
// Orchestration: explicit flow, easier to debug, single coordinator (SPOF risk)
// Choreography: more decoupled, no SPOF, harder to trace full flow, implicit logic
```

**Q23. Distributed locking.**
```javascript
// When you need exclusive access to a shared resource across services
// Example: don't send duplicate emails, don't double-charge a card

// REDIS REDLOCK ALGORITHM:
// Acquire lock on majority (3/5) of Redis nodes simultaneously
// Prevents single Redis node failure from causing duplicate processing

class DistributedLock {
  constructor(private redis: Redis) {}

  async acquire(key: string, ttlMs: number): Promise<string | null> {
    const token = crypto.randomUUID();
    const result = await this.redis.set(
      `lock:${key}`,
      token,
      'PX', ttlMs,  // expire in ttlMs milliseconds
      'NX'          // only set if NOT exists
    );
    return result === 'OK' ? token : null;
  }

  async release(key: string, token: string): Promise<boolean> {
    // Lua script for atomic check-and-delete:
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    const result = await this.redis.eval(script, 1, `lock:${key}`, token);
    return result === 1;
  }

  async withLock<T>(key: string, ttlMs: number, fn: () => Promise<T>): Promise<T> {
    const token = await this.acquire(key, ttlMs);
    if (!token) throw new LockAcquisitionError(`Failed to acquire lock: ${key}`);

    try {
      return await fn();
    } finally {
      await this.release(key, token);
    }
  }
}

// Usage:
const lock = new DistributedLock(redis);
await lock.withLock(`user:${userId}:email:welcome`, 30000, async () => {
  const alreadySent = await db.emailLog.findUnique({ where: { userId, type: 'welcome' } });
  if (!alreadySent) {
    await emailService.sendWelcome(user);
    await db.emailLog.create({ data: { userId, type: 'welcome' } });
  }
});
```

---

## SERVICE MESH & OBSERVABILITY (Q41-Q60)

**Q41. Distributed tracing — end-to-end visibility.**
```javascript
// Without tracing: a request fails in service D.
// You know: the user got a 500. You don't know: why.
// With tracing: trace shows the full path + timing for every step

// TRACE PROPAGATION:
// Every service reads trace headers from incoming request
// Adds its own span (operation) to the trace
// Forwards trace headers to downstream services

// W3C Trace Context (standard headers):
// traceparent: 00-{trace-id}-{parent-span-id}-{flags}
// tracestate: vendor-specific data

// OpenTelemetry auto-propagation:
// When you use @opentelemetry/instrumentation-http:
// - Automatically reads traceparent from incoming requests
// - Adds traceparent to all outgoing requests
// - Creates spans for every incoming/outgoing HTTP call
// - You get the full trace with zero code changes!

// Custom business span:
const tracer = trace.getTracer('order-service');

async function processOrder(ctx: Context, orderId: string) {
  const span = tracer.startSpan('order.process', {
    attributes: {
      'order.id': orderId,
      'service.version': '2.1.0',
    }
  }, ctx);

  try {
    // Child spans automatically parented to this span:
    await validateOrder(trace.setSpan(ctx, span), orderId);
    await chargePayment(trace.setSpan(ctx, span), orderId);
    span.setStatus({ code: SpanStatusCode.OK });
  } catch (err) {
    span.recordException(err);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw err;
  } finally {
    span.end();
  }
}

// What you can debug with traces:
// - Which service is slow? (sorted by duration)
// - Where in the call chain did the error originate?
// - What was the DB query that took 5 seconds?
// - Are there serial calls that could be parallelized?
// - What percentage of requests go through each code path?
```

**Q42. Microservices testing strategy.**
```
TESTING LAYERS FOR MICROSERVICES:

1. UNIT TESTS (fast, many):
   Test business logic in isolation
   Mock all external calls (DB, HTTP, queues)
   Run in milliseconds

2. COMPONENT TESTS (medium speed, some):
   Test ONE service with real infrastructure (DB, Redis)
   Mock all OTHER services (WireMock, MockServer)
   Testcontainers for real databases
   Test service API contracts

3. CONTRACT TESTS (fast, key integrations):
   Consumer-driven contracts (Pact)
   Verify service boundaries without running both services
   Runs in seconds

4. INTEGRATION TESTS (slow, few):
   Run 2-3 services together
   Use only for critical flows you can't test otherwise
   Example: checkout flow (order + payment + inventory)

5. E2E TESTS (slowest, minimal):
   Full system up
   Only critical user journeys
   "Happy path" + "most important error path"
   Accept flakiness, invest in retry logic

KEY PRINCIPLE: Test each service in isolation.
  If you need to spin up 10 services to test one thing → wrong test level.
  Fix the abstraction boundary instead.

CONTRACT-FIRST DEVELOPMENT:
  1. Teams agree on API contract (OpenAPI spec or Pact)
  2. Consumer team writes tests against mock
  3. Provider team implements to pass contract tests
  4. Integration happens only when both sides pass contracts
  Result: no "integration hell" weeks
```

---

## SERVICE DESIGN PATTERNS (Q61-Q80)

**Q61. Event-driven microservices.**
```javascript
// Domain events: things that happened in your domain
// Integration events: events you publish for other services to react to

// EVENT DESIGN:
// Good event: { type: "order.placed", orderId, userId, items, total, timestamp }
// Bad event: { type: "db.orders.inserted", row: { ...all db columns... } }
// Rule: events describe BUSINESS FACTS, not technical implementation

// OUTBOX PATTERN — guaranteed event publishing:
// Problem: publish event AFTER DB write, but crash between write and publish
// Solution: write to outbox table in SAME transaction, publish asynchronously

// In order service (single transaction):
await db.transaction(async (tx) => {
  const order = await tx.orders.create({ data: orderData });
  await tx.outboxEvents.create({
    data: {
      type:      'order.placed',
      payload:   JSON.stringify(order),
      createdAt: new Date(),
      published: false,
    }
  });
});

// Outbox processor (separate process, polls DB or uses Debezium CDC):
async function processOutbox() {
  const events = await db.outboxEvents.findMany({
    where: { published: false },
    orderBy: { createdAt: 'asc' },
    take: 100,
  });

  for (const event of events) {
    await kafka.produce(event.type, JSON.parse(event.payload));
    await db.outboxEvents.update({
      where: { id: event.id },
      data:  { published: true, publishedAt: new Date() },
    });
  }
}

// IDEMPOTENT CONSUMERS — process same event twice = same result:
async function handleOrderPlaced(event: OrderPlacedEvent) {
  // Check if already processed:
  const processed = await redis.get(`processed:${event.eventId}`);
  if (processed) { return; } // already handled, skip

  await inventoryService.reserve(event.orderId, event.items);
  await redis.setEx(`processed:${event.eventId}`, 86400, '1'); // remember 24h
}
```

**Q62. Service decomposition — database per service.**
```
PATTERN: Each microservice owns its data. No shared databases.

WHY:
  Shared DB = tight coupling (schema change in one service breaks others)
  Shared DB = scaling one DB scales for all (no independent scaling)
  Shared DB = one team's bad query brings down all services

CONSEQUENCES:
  - No JOINs across service boundaries
  - Data may be duplicated (order service stores user name)
  - Eventual consistency between services
  - More complex data management

QUERY PATTERNS ACROSS SERVICES:

1. API COMPOSITION (simplest):
   Gateway calls both services, joins in application code
   User → Gateway → {UserService.getUser(id), OrderService.getOrders(userId)}
   Gateway merges: { user, orders }
   Works well for small datasets

2. CQRS WITH READ MODELS:
   Maintain denormalized view combining data from multiple services
   Updated via domain events
   "UserOrders" read model: userId, userName, orderId, orderStatus
   Updated by listening to user.updated + order.placed events

3. DATA SYNCHRONIZATION:
   Services publish events when data changes
   Other services maintain their own copy (eventual consistency)
   UserService publishes user.updated → OrderService updates its user cache

4. API CALLS WITHIN SERVICE:
   When you need User data in OrderService:
   OrderService calls UserService API (not DB directly)
   Cache aggressively (user data doesn't change often)
```

---

## DEPLOYMENT PATTERNS (Q81-Q100)

**Q81. Blue-green and canary deployments.**
```yaml
# BLUE-GREEN DEPLOYMENT:
# Two identical production environments (blue = current, green = new)
# Deploy to green → test → switch traffic → blue becomes standby

# Kubernetes blue-green with services:
# Blue deployment (current):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
  labels:
    version: blue
spec:
  replicas: 5
  selector:
    matchLabels:
      app: api
      version: blue
---
# Green deployment (new version):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
  labels:
    version: green
spec:
  replicas: 5
  selector:
    matchLabels:
      app: api
      version: green
---
# Service — switch by changing selector:
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
    version: blue  # change to 'green' to switch traffic
  ports:
    - port: 80
      targetPort: 3000

# CANARY DEPLOYMENT (Argo Rollouts):
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 5     # 5% of traffic to canary
        - pause: {duration: 10m}
        - analysis:        # automated health check
            templates:
              - templateName: error-rate
        - setWeight: 25
        - pause: {duration: 15m}
        - setWeight: 50
        - pause: {duration: 15m}
        - setWeight: 100   # full rollout
      canaryMetadata:
        labels:
          version: canary
      stableMetadata:
        labels:
          version: stable
      # Auto-rollback if error rate > 5%:
      analysis:
        templates:
          - templateName: error-rate-check
```

**Q82. Feature flags for microservices.**
```javascript
// Feature flags = deploy code disabled, enable for % of users without deploying
// Essential for: canary releases, A/B tests, kill switches, gradual rollouts

import LaunchDarkly from '@launchdarkly/node-server-sdk';

const ldClient = LaunchDarkly.init(process.env.LD_SDK_KEY);

// In service code:
async function processPayment(userId: string, amount: number) {
  const context = { kind: 'user', key: userId };

  // Check feature flag:
  const useNewPaymentProvider = await ldClient.variation(
    'new-payment-provider', // flag key
    context,
    false // default (flag off = use old provider)
  );

  if (useNewPaymentProvider) {
    return await stripeV2.charge(userId, amount);
  } else {
    return await stripeV1.charge(userId, amount);
  }
}

// FLAG TYPES:
// Boolean: on/off (kill switch, feature enable)
// String: "v1" | "v2" | "v3" (version routing)
// Number: percentage throttle
// JSON: complex configuration without deploy

// TARGETING RULES:
// 100% of internal employees → see flag = true
// 1% of all users → see flag = true (canary)
// Specific user IDs → see flag = true (beta testers)
// Users in US timezone → see flag = true (geographic rollout)

// KILL SWITCH PATTERN:
// Deploy with flag off → code is deployed but not running
// Enable flag for 1% → monitor errors
// Ramp to 100% → full rollout
// If issues: flip flag to false → instant rollback without redeploy

// TECHNICAL DEBT: flags accumulate. Remove within 1 sprint of full rollout.
// Stale flags = dead code = maintenance burden
```

---

**Q83. Circuit breaker pattern — implementation and states.**

```javascript
// Circuit breaker protects against cascading failures
// States: CLOSED (normal) → OPEN (failing, reject calls) → HALF-OPEN (test recovery)

class CircuitBreaker {
  #state = 'CLOSED';
  #failureCount = 0;
  #successCount = 0;
  #lastFailureTime = null;
  #options;

  constructor(options = {}) {
    this.#options = {
      failureThreshold: options.failureThreshold || 5,
      successThreshold: options.successThreshold || 3,
      timeout: options.timeout || 30000, // ms before trying again
      ...options,
    };
  }

  async execute(fn) {
    if (this.#state === 'OPEN') {
      if (Date.now() - this.#lastFailureTime > this.#options.timeout) {
        this.#state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN — request rejected');
      }
    }

    try {
      const result = await fn();
      this.#onSuccess();
      return result;
    } catch (error) {
      this.#onFailure();
      throw error;
    }
  }

  #onSuccess() {
    if (this.#state === 'HALF_OPEN') {
      this.#successCount++;
      if (this.#successCount >= this.#options.successThreshold) {
        this.#state = 'CLOSED';
        this.#failureCount = 0;
        this.#successCount = 0;
      }
    }
    this.#failureCount = 0;
  }

  #onFailure() {
    this.#failureCount++;
    this.#lastFailureTime = Date.now();
    if (this.#failureCount >= this.#options.failureThreshold) {
      this.#state = 'OPEN';
    }
  }

  get state() { return this.#state; }
}

// Usage:
const paymentBreaker = new CircuitBreaker({ failureThreshold: 3, timeout: 60000 });
try {
  const result = await paymentBreaker.execute(() => paymentService.charge(order));
} catch (err) {
  if (err.message.includes('OPEN')) {
    return fallbackPaymentFlow(order); // degrade gracefully
  }
  throw err;
}

// Libraries: opossum (Node.js), resilience4j (Java), Polly (.NET)
// Istio/Envoy: circuit breaking at network level (no code changes)
```

---

**Q84. Saga pattern — distributed transactions without 2PC.**

```
PROBLEM: In microservices, a single business operation spans multiple services.
Traditional DB transactions (ACID) don't work across service boundaries.

SAGA: a sequence of local transactions. Each step has a compensating action (undo).

TWO TYPES:

1. CHOREOGRAPHY (event-driven, no coordinator):
   OrderService → "OrderCreated" event
   PaymentService listens → charges card → "PaymentCompleted" event
   InventoryService listens → reserves stock → "StockReserved" event
   ShippingService listens → creates shipment → "OrderFulfilled" event

   If PaymentService fails → emits "PaymentFailed"
   OrderService listens → cancels order (compensating action)

   Pros: loosely coupled, simple for 3-4 steps
   Cons: hard to track overall flow, debugging is painful

2. ORCHESTRATION (central coordinator):
   OrderSaga orchestrator drives each step:
```
```javascript
class OrderSaga {
  async execute(orderData) {
    const steps = [
      {
        action: () => this.paymentService.charge(orderData),
        compensate: () => this.paymentService.refund(orderData),
      },
      {
        action: () => this.inventoryService.reserve(orderData),
        compensate: () => this.inventoryService.release(orderData),
      },
      {
        action: () => this.shippingService.createShipment(orderData),
        compensate: () => this.shippingService.cancelShipment(orderData),
      },
    ];

    const completed = [];
    for (const step of steps) {
      try {
        await step.action();
        completed.push(step);
      } catch (error) {
        // Compensate in reverse order:
        for (const s of completed.reverse()) {
          await s.compensate();
        }
        throw new SagaFailedError(error, completed.length);
      }
    }
  }
}

// Orchestration pros: clear flow, easy to debug, centralized error handling
// Orchestration cons: coordinator is a single point of coupling
// Use orchestration for complex flows (5+ steps), choreography for simple ones
```

---

**Q85. Event sourcing — storing state as a sequence of events.**

```javascript
// Instead of storing CURRENT state, store every STATE CHANGE as an immutable event.
// Current state = replay all events from the beginning.

// Event store:
class EventStore {
  #events = []; // In production: append-only table or Kafka topic

  append(aggregateId, event) {
    this.#events.push({
      aggregateId,
      type: event.type,
      data: event.data,
      timestamp: new Date(),
      version: this.getEvents(aggregateId).length + 1,
    });
  }

  getEvents(aggregateId) {
    return this.#events.filter(e => e.aggregateId === aggregateId);
  }
}

// Account aggregate rebuilt from events:
class BankAccount {
  #balance = 0;
  #id;

  static fromEvents(id, events) {
    const account = new BankAccount(id);
    for (const event of events) {
      account.#apply(event);
    }
    return account;
  }

  #apply(event) {
    switch (event.type) {
      case 'AccountOpened':   this.#balance = event.data.initialDeposit; break;
      case 'MoneyDeposited':  this.#balance += event.data.amount; break;
      case 'MoneyWithdrawn':  this.#balance -= event.data.amount; break;
    }
  }

  get balance() { return this.#balance; }
}

// Events for account #123:
// { type: 'AccountOpened',  data: { initialDeposit: 1000 } }
// { type: 'MoneyDeposited', data: { amount: 500 } }
// { type: 'MoneyWithdrawn', data: { amount: 200 } }
// Replayed state: balance = 1300

// WHY EVENT SOURCING:
// ✅ Complete audit trail (every change recorded)
// ✅ Temporal queries ("what was the balance on March 1st?")
// ✅ Event replay for debugging, testing
// ✅ CQRS synergy (project events into read models)
// ❌ Complexity: eventual consistency, event versioning
// ❌ Storage growth (use snapshots to optimize)

// SNAPSHOT optimization:
// Every N events, store a snapshot of current state
// Rebuild = load snapshot + replay events after snapshot
```

---

**Q86. CQRS — Command Query Responsibility Segregation.**

```
CQRS separates READ and WRITE models:
- Command side: handles writes (create, update, delete)
- Query side: handles reads (optimized read models)

WHY:
- Reads and writes have different scaling needs (reads >> writes)
- Read models can be denormalized for fast queries
- Write model can use event sourcing for consistency
- Each side can use different databases

WRITE SIDE:                        READ SIDE:
  API → Command Handler            API → Query Handler
  → Domain Model (validates)        → Read Database (denormalized)
  → Event Store (persists)          ← Projector (builds read model
  → Publishes Domain Events             from events)
```
```javascript
// Command side:
class CreateOrderHandler {
  async handle(command) {
    const order = new Order(command.customerId, command.items);
    order.validate(); // domain rules
    await this.eventStore.append(order.id, {
      type: 'OrderCreated',
      data: { customerId: command.customerId, items: command.items, total: order.total },
    });
    await this.eventBus.publish('OrderCreated', order);
  }
}

// Query side — projector builds read model:
class OrderProjector {
  async handle(event) {
    if (event.type === 'OrderCreated') {
      await this.readDb.orders.insert({
        id: event.aggregateId,
        customerName: await this.getCustomerName(event.data.customerId),
        items: event.data.items,
        total: event.data.total,
        status: 'pending',
        createdAt: event.timestamp,
      });
    }
    if (event.type === 'OrderShipped') {
      await this.readDb.orders.update(event.aggregateId, {
        status: 'shipped',
        trackingNumber: event.data.trackingNumber,
      });
    }
  }
}

// Query handler (fast, denormalized reads):
class GetOrdersByCustomerHandler {
  async handle(query) {
    return this.readDb.orders.find({
      customerName: query.customerName,
      status: query.status,
    }); // No joins needed — already denormalized
  }
}

// WHEN TO USE CQRS:
// ✅ Read/write ratio is heavily skewed (100:1 reads:writes)
// ✅ Complex domain with rich business rules on write side
// ✅ Need different read models for different consumers (API, reports, search)
// ❌ Simple CRUD apps — CQRS adds unnecessary complexity
// ❌ Small teams — operational overhead of maintaining two models
```

---

**Q87. API Gateway pattern — routing, auth, rate limiting.**

```javascript
// API Gateway sits between clients and microservices.
// Single entry point — handles cross-cutting concerns.

// RESPONSIBILITIES:
// 1. Request routing → direct to correct service
// 2. Authentication/authorization → verify JWT, API keys
// 3. Rate limiting → protect services from overload
// 4. Request/response transformation → aggregate, filter
// 5. Load balancing → distribute across instances
// 6. Caching → cache GET responses
// 7. Circuit breaking → protect failing services
// 8. Logging/metrics → centralized observability

// Express-based API Gateway:
const gateway = express();

// Auth middleware (applied to all routes):
gateway.use(async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  try {
    req.user = await verifyJWT(token);
    next();
  } catch { res.status(401).json({ error: 'Invalid token' }); }
});

// Rate limiting:
const rateLimit = require('express-rate-limit');
gateway.use(rateLimit({
  windowMs: 60 * 1000,
  max: 100, // 100 requests per minute per IP
  standardHeaders: true,
}));

// Route to services:
const { createProxyMiddleware } = require('http-proxy-middleware');
gateway.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  pathRewrite: { '^/api/users': '/users' },
}));
gateway.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  pathRewrite: { '^/api/orders': '/orders' },
}));

// BFF (Backend for Frontend) pattern:
// Different gateways for different clients:
// Mobile BFF → aggregates data, smaller payloads
// Web BFF → richer data, pagination
// Third-party API → versioned, rate-limited

// Production gateways: Kong, AWS API Gateway, Traefik, NGINX, Envoy
```

---

**Q88. Service discovery — how services find each other.**

```
PROBLEM: In microservices, service instances are dynamic (scaling, restarts,
deployments). Hardcoding URLs doesn't work.

TWO PATTERNS:

1. CLIENT-SIDE DISCOVERY:
   Client queries a service registry → gets list of instances → load-balances itself.
   Registry: Consul, Eureka, etcd
   Pros: client can make smart routing decisions
   Cons: each client needs discovery logic

2. SERVER-SIDE DISCOVERY:
   Client sends request to load balancer → LB queries registry → routes request.
   LB: AWS ALB, NGINX, Kubernetes Service
   Pros: clients are simple (just call one URL)
   Cons: LB is a potential bottleneck

KUBERNETES APPROACH (server-side, built-in):
  - Every Service gets a DNS name: <service-name>.<namespace>.svc.cluster.local
  - kube-proxy routes traffic to healthy pods
  - No external registry needed
```
```yaml
# Kubernetes Service (built-in discovery):
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP  # internal only
# Other services call: http://user-service/users
```
```javascript
// Consul-based discovery (non-Kubernetes):
const Consul = require('consul');
const consul = new Consul({ host: 'consul-server' });

// Register service on startup:
await consul.agent.service.register({
  name: 'order-service',
  address: '10.0.1.5',
  port: 3002,
  check: {
    http: 'http://10.0.1.5:3002/health',
    interval: '10s',
    deregistercriticalserviceafter: '30s',
  },
});

// Discover service:
const services = await consul.health.service({ service: 'user-service', passing: true });
const instance = services[Math.floor(Math.random() * services.length)];
const url = `http://${instance.Service.Address}:${instance.Service.Port}`;
```

---

**Q89. Distributed tracing — tracking requests across services.**

```javascript
// A single user request may hit 5+ services.
// Distributed tracing connects the dots with trace IDs.

// KEY CONCEPTS:
// Trace: end-to-end journey of a request
// Span: a single operation within a trace (one service call)
// Context propagation: passing trace ID between services

// OpenTelemetry auto-instrumentation (Node.js):
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: 'http://jaeger:4318/v1/traces' }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
// Now every HTTP request, DB query, and message automatically gets traced

// Manual span creation:
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('order-service');

async function processOrder(orderId) {
  return tracer.startActiveSpan('processOrder', async (span) => {
    span.setAttribute('order.id', orderId);
    
    // This HTTP call automatically propagates trace context:
    const user = await fetch('http://user-service/users/' + userId);
    
    // Child span:
    await tracer.startActiveSpan('validateInventory', async (childSpan) => {
      await inventoryService.check(orderId);
      childSpan.end();
    });
    
    span.end();
  });
}

// Trace visualization in Jaeger/Zipkin shows:
// [Gateway] → [OrderService.processOrder] → [UserService.getUser]
//                                         → [InventoryService.check]
//                                         → [PaymentService.charge]
// With timing for each span — instantly see which service is slow

// W3C Trace Context headers (standard):
// traceparent: 00-<trace-id>-<span-id>-<flags>
// tracestate: vendor-specific data
```

---

**Q90. Bulkhead pattern — isolating failures.**

```javascript
// Named after ship bulkheads that contain flooding to one compartment.
// Isolate resources so one failing service doesn't exhaust all resources.

// THREAD POOL BULKHEAD:
// Each service call gets its own limited pool.
// If payment service is slow, it only exhausts its own pool,
// not the entire application's connection pool.

class BulkheadPool {
  #maxConcurrent;
  #active = 0;
  #queue = [];

  constructor(maxConcurrent) {
    this.#maxConcurrent = maxConcurrent;
  }

  async execute(fn) {
    if (this.#active >= this.#maxConcurrent) {
      // Queue or reject
      return new Promise((resolve, reject) => {
        this.#queue.push({ fn, resolve, reject });
        // Timeout queued requests after 5s:
        setTimeout(() => {
          const idx = this.#queue.findIndex(q => q.resolve === resolve);
          if (idx !== -1) {
            this.#queue.splice(idx, 1);
            reject(new Error('Bulkhead queue timeout'));
          }
        }, 5000);
      });
    }

    this.#active++;
    try {
      return await fn();
    } finally {
      this.#active--;
      if (this.#queue.length > 0) {
        const next = this.#queue.shift();
        this.execute(next.fn).then(next.resolve, next.reject);
      }
    }
  }
}

// Usage — each service gets its own bulkhead:
const paymentBulkhead = new BulkheadPool(10);    // max 10 concurrent
const inventoryBulkhead = new BulkheadPool(20);  // max 20 concurrent
const emailBulkhead = new BulkheadPool(5);       // max 5 concurrent

// Even if payment is slow and all 10 slots are busy,
// inventory and email still have their own pools.
await paymentBulkhead.execute(() => paymentService.charge(order));
await inventoryBulkhead.execute(() => inventoryService.reserve(items));
```

---

**Q91. Sidecar pattern and service mesh architecture.**

```
SIDECAR: a helper container deployed alongside your main application container.
Both share the same pod (Kubernetes) or host. The sidecar handles cross-cutting
concerns so the app doesn't have to.

COMMON SIDECARS:
- Envoy proxy (traffic management, mTLS, observability)
- Fluentd/Fluent Bit (log collection)
- Vault Agent (secrets injection)
- Jaeger Agent (trace collection)
```
```yaml
# Pod with sidecar:
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
    - name: app
      image: myapp:v1
      ports:
        - containerPort: 3000
    - name: envoy-sidecar  # sidecar
      image: envoyproxy/envoy:v1.28
      ports:
        - containerPort: 9901
      volumeMounts:
        - name: envoy-config
          mountPath: /etc/envoy
    - name: log-collector  # another sidecar
      image: fluent/fluent-bit:2.0
      volumeMounts:
        - name: app-logs
          mountPath: /var/log/app
```
```
SERVICE MESH = sidecar proxies on EVERY service + control plane.

Data Plane (sidecar proxies):
  - Handle all service-to-service traffic
  - mTLS encryption (automatic)
  - Load balancing, retries, circuit breaking
  - Metrics collection

Control Plane:
  - Configures all sidecar proxies
  - Certificate management
  - Traffic policies
  - Service discovery

Popular meshes: Istio (Envoy sidecars), Linkerd (linkerd2-proxy), Cilium (eBPF, no sidecars)

WHEN TO USE:
✅ 20+ microservices needing consistent networking policies
✅ Zero-trust security requirement (mTLS everywhere)
✅ Complex traffic management (canary, A/B, fault injection)
❌ < 10 services (overhead not justified)
❌ Team can't operate Kubernetes well yet
```

---

**Q92. Data consistency patterns in microservices.**

```
CHALLENGE: Each microservice owns its own database.
No distributed transactions. How to keep data consistent?

PATTERN 1: EVENTUAL CONSISTENCY (most common)
  Services emit events. Other services update asynchronously.
  Order placed → event → Inventory updated (eventually)
  Trade-off: short window of inconsistency

PATTERN 2: SAGA (see Q84)
  Sequence of local transactions with compensating actions.

PATTERN 3: OUTBOX PATTERN (reliable event publishing)
  Problem: "write to DB" and "publish event" are two operations.
  If app crashes between them, event is lost.
  Solution: write event to an OUTBOX TABLE in the same DB transaction.
  A separate process reads outbox and publishes events.
```
```javascript
// Outbox pattern implementation:
async function createOrder(orderData) {
  await db.transaction(async (tx) => {
    // 1. Write to orders table:
    const order = await tx.orders.insert(orderData);
    
    // 2. Write event to outbox (SAME transaction):
    await tx.outbox.insert({
      aggregateId: order.id,
      eventType: 'OrderCreated',
      payload: JSON.stringify(order),
      createdAt: new Date(),
      published: false,
    });
  });
  // Both writes succeed or both fail — no inconsistency
}

// Outbox relay (separate process):
async function publishOutboxEvents() {
  const events = await db.outbox.find({ published: false, limit: 100 });
  for (const event of events) {
    await messageBroker.publish(event.eventType, event.payload);
    await db.outbox.update(event.id, { published: true });
  }
}
// Run every few seconds or use CDC (Change Data Capture) with Debezium

// PATTERN 4: Change Data Capture (CDC)
// Debezium reads database transaction log (WAL in Postgres)
// Publishes changes to Kafka automatically
// No application code changes needed
// Most reliable approach for outbox pattern
```

---

**Q93. API versioning strategies for microservices.**

```javascript
// 1. URL PATH VERSIONING (most common):
// GET /api/v1/users
// GET /api/v2/users
// Pros: explicit, easy to understand, easy to route
// Cons: URL changes, breaks bookmarks

// 2. HEADER VERSIONING:
// GET /api/users  +  Accept: application/vnd.myapi.v2+json
// Pros: clean URLs
// Cons: harder to test in browser, less discoverable

// 3. QUERY PARAMETER:
// GET /api/users?version=2
// Pros: simple
// Cons: optional parameter → ambiguous default

// BEST PRACTICE: URL versioning for public APIs, header for internal

// Handling multiple versions:
// Option A: separate controllers
app.use('/api/v1/users', usersV1Router);
app.use('/api/v2/users', usersV2Router);

// Option B: version middleware
app.use('/api/users', (req, res, next) => {
  const version = req.headers['api-version'] || 'v2';
  req.apiVersion = version;
  next();
});

// BREAKING vs NON-BREAKING changes:
// Non-breaking (no new version needed):
// - Adding new fields to response
// - Adding new optional query parameters
// - Adding new endpoints
// Breaking (requires new version):
// - Removing or renaming fields
// - Changing field types
// - Changing error response format
// - Removing endpoints

// DEPRECATION STRATEGY:
// 1. Announce deprecation (6 months notice)
// 2. Add Sunset header: Sunset: Sat, 01 Jun 2025 00:00:00 GMT
// 3. Add Deprecation header: Deprecation: true
// 4. Log v1 usage to track migration progress
// 5. Return 410 Gone after sunset date
```

---

**Q94. Strangler Fig pattern — migrating monolith to microservices.**

```
Named after strangler fig trees that grow around a host tree, eventually replacing it.

APPROACH: gradually replace monolith features with microservices,
routing traffic piece by piece, until the monolith is empty.

STEPS:
1. Identify a bounded context to extract (e.g., "Payments")
2. Build the new Payment microservice
3. Route payment traffic to new service (proxy/facade)
4. Verify: run old and new in parallel, compare results
5. Cut over: route 100% to new service
6. Remove payment code from monolith
7. Repeat for next bounded context

ANTI-CORRUPTION LAYER:
  Sits between monolith and new service.
  Translates monolith data models → new domain models.
  Prevents monolith's "corruption" from leaking into clean services.
```
```javascript
// Strangler facade (routes to old or new):
app.use('/api/payments', (req, res, next) => {
  if (useNewPaymentService(req)) {
    // Route to new microservice:
    proxy.web(req, res, { target: 'http://payment-service:3010' });
  } else {
    // Route to monolith:
    proxy.web(req, res, { target: 'http://monolith:8080' });
  }
});

function useNewPaymentService(req) {
  // Gradual migration strategies:
  // 1. By feature flag
  // 2. By customer segment (enterprise first)
  // 3. By geography (EU first)
  // 4. By percentage (canary)
  return featureFlags.isEnabled('new-payment-service', {
    userId: req.user?.id,
    percentage: 25, // 25% of traffic
  });
}

// PARALLEL RUN (verify correctness before full cutover):
app.use('/api/payments', async (req, res) => {
  const [monolithResult, serviceResult] = await Promise.allSettled([
    callMonolith(req),
    callNewService(req),
  ]);
  
  // Compare results (log differences, don't affect response):
  if (JSON.stringify(monolithResult) !== JSON.stringify(serviceResult)) {
    logger.warn('Payment result mismatch', { monolithResult, serviceResult });
  }
  
  // Return monolith result (trusted) until fully validated:
  res.json(monolithResult.value);
});
```

---

**Q95. Health checks and readiness probes in microservices.**

```javascript
// Three types of health endpoints:

// 1. LIVENESS — "is the process alive?"
// If fails → Kubernetes restarts the pod
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});

// 2. READINESS — "can the service handle traffic?"
// If fails → Kubernetes removes pod from Service (no traffic)
app.get('/health/ready', async (req, res) => {
  try {
    await db.query('SELECT 1');          // DB connection works
    await redis.ping();                   // Cache connection works
    // Check downstream dependencies:
    const deps = await checkDependencies();
    if (deps.allHealthy) {
      res.status(200).json({ status: 'ready', dependencies: deps });
    } else {
      res.status(503).json({ status: 'not ready', dependencies: deps });
    }
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// 3. STARTUP — "has the service finished initializing?"
// If fails → Kubernetes waits (doesn't restart yet)
// Useful for services with slow startup (loading ML models, warming cache)
app.get('/health/startup', (req, res) => {
  if (appInitialized) {
    res.status(200).json({ status: 'started' });
  } else {
    res.status(503).json({ status: 'starting' });
  }
});
```
```yaml
# Kubernetes probe configuration:
spec:
  containers:
    - name: app
      livenessProbe:
        httpGet:
          path: /health/live
          port: 3000
        initialDelaySeconds: 10
        periodSeconds: 15
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 3000
        initialDelaySeconds: 5
        periodSeconds: 10
        failureThreshold: 2
      startupProbe:
        httpGet:
          path: /health/startup
          port: 3000
        failureThreshold: 30
        periodSeconds: 10
        # Total startup budget: 30 × 10s = 300s (5 min)
```

---

**Q96. Inter-service communication — sync vs async patterns.**

```
SYNCHRONOUS (request-response):
  HTTP/REST, gRPC, GraphQL
  ✅ Simple mental model, immediate response
  ❌ Tight coupling, cascading failures, latency chain
  Use for: queries, real-time responses needed

ASYNCHRONOUS (message-based):
  Message queues (RabbitMQ, SQS), event streams (Kafka)
  ✅ Loose coupling, resilience, natural buffering
  ❌ Eventual consistency, harder debugging, message ordering
  Use for: commands, events, background processing

HYBRID (most production systems):
  Sync for queries (GET user profile)
  Async for commands/events (place order, send notification)
```
```javascript
// Sync: gRPC (faster than REST, typed contracts):
// user.proto:
// service UserService {
//   rpc GetUser (GetUserRequest) returns (User);
// }

// Async: Event-driven with RabbitMQ:
// Publisher (OrderService):
channel.publish('exchange', 'order.created', Buffer.from(JSON.stringify({
  orderId: '123',
  userId: 'abc',
  total: 99.99,
  items: [{ sku: 'WIDGET-1', qty: 2 }],
})));

// Consumer (EmailService):
channel.consume('email-queue', async (msg) => {
  const order = JSON.parse(msg.content.toString());
  await sendOrderConfirmationEmail(order);
  channel.ack(msg); // acknowledge processing
});

// Consumer (InventoryService):
channel.consume('inventory-queue', async (msg) => {
  const order = JSON.parse(msg.content.toString());
  await reserveInventory(order.items);
  channel.ack(msg);
});

// REQUEST-REPLY over async (when you need response via queue):
const correlationId = crypto.randomUUID();
channel.publish('exchange', 'inventory.check', Buffer.from(JSON.stringify({
  items: order.items,
})), { correlationId, replyTo: 'order-service-replies' });

// Wait for response on reply queue:
channel.consume('order-service-replies', (msg) => {
  if (msg.properties.correlationId === correlationId) {
    const result = JSON.parse(msg.content.toString());
    // Process inventory check result
  }
});
```

---

**Q97. Microservices testing strategies.**

```javascript
// TEST PYRAMID for microservices:
//        /  E2E  \          Few: slow, expensive, catch integration bugs
//       / Contract \        Moderate: verify service boundaries
//      /  Integration\      Moderate: test with real dependencies
//     /    Unit Tests  \    Many: fast, isolated, business logic

// 1. UNIT TESTS — pure business logic, no I/O:
test('calculateOrderTotal applies discount', () => {
  const items = [{ price: 100, qty: 2 }, { price: 50, qty: 1 }];
  expect(calculateOrderTotal(items, { discountPercent: 10 })).toBe(225);
});

// 2. INTEGRATION TESTS — test with real DB, real HTTP:
test('POST /orders creates order in database', async () => {
  const res = await request(app)
    .post('/orders')
    .send({ customerId: 'c1', items: [{ sku: 'A', qty: 1 }] })
    .expect(201);

  const order = await db.orders.findById(res.body.id);
  expect(order).toBeDefined();
  expect(order.status).toBe('pending');
});

// 3. CONTRACT TESTS — verify API contract between services:
// Using Pact:
// Consumer side (what OrderService expects from UserService):
const interaction = {
  state: 'user 123 exists',
  uponReceiving: 'a request for user 123',
  withRequest: { method: 'GET', path: '/users/123' },
  willRespondWith: {
    status: 200,
    body: { id: '123', name: like('John'), email: like('john@example.com') },
  },
};
// Pact generates a contract file → provider verifies against it
// If provider changes response shape → contract test FAILS

// 4. E2E TESTS — test full user flow across services:
test('user can place an order end to end', async () => {
  const user = await createTestUser();
  const product = await createTestProduct({ stock: 10 });
  
  const order = await api.post('/orders', {
    userId: user.id,
    items: [{ productId: product.id, qty: 2 }],
  });
  
  // Wait for async processing:
  await waitForCondition(() => 
    api.get(`/orders/${order.id}`).then(r => r.status === 'confirmed')
  , { timeout: 10000 });
  
  const updatedProduct = await api.get(`/products/${product.id}`);
  expect(updatedProduct.stock).toBe(8); // inventory reserved
});
```

---

**Q98. Distributed logging and log aggregation.**

```javascript
// Structured logging (JSON) — essential for microservices:
const logger = {
  info(message, context = {}) {
    console.log(JSON.stringify({
      level: 'info',
      message,
      service: process.env.SERVICE_NAME,
      traceId: context.traceId || getTraceId(),
      timestamp: new Date().toISOString(),
      ...context,
    }));
  },
  error(message, error, context = {}) {
    console.error(JSON.stringify({
      level: 'error',
      message,
      service: process.env.SERVICE_NAME,
      traceId: context.traceId || getTraceId(),
      error: { message: error.message, stack: error.stack, name: error.name },
      timestamp: new Date().toISOString(),
      ...context,
    }));
  },
};

// Correlation ID middleware (track request across services):
app.use((req, res, next) => {
  req.correlationId = req.headers['x-correlation-id'] || crypto.randomUUID();
  res.setHeader('x-correlation-id', req.correlationId);
  next();
});

// When calling other services, propagate:
const response = await fetch('http://user-service/users/123', {
  headers: { 'x-correlation-id': req.correlationId },
});

// LOG AGGREGATION STACK:
// 1. ELK: Elasticsearch + Logstash + Kibana
//    App → Filebeat (ships logs) → Logstash (transforms) → Elasticsearch (stores) → Kibana (visualize)
// 2. EFK: Elasticsearch + Fluentd + Kibana (Kubernetes-native)
// 3. Grafana Loki: lightweight, label-based (cheaper than ELK)
//    App → Promtail (ships logs) → Loki (stores) → Grafana (visualize)

// KEY PRACTICES:
// ✅ Always include: timestamp, service name, trace/correlation ID, log level
// ✅ Use structured (JSON) logs — never free-form text
// ✅ Log at boundaries: incoming requests, outgoing calls, errors
// ❌ Never log PII (emails, passwords, credit cards)
// ❌ Don't log at DEBUG level in production (volume)
```

---

**Q99. Microservices anti-patterns to avoid.**

```
1. DISTRIBUTED MONOLITH
   Looks like microservices but services are tightly coupled.
   Every change requires deploying 5 services together.
   Fix: true bounded contexts, async communication, independent deployability.

2. SHARED DATABASE
   Multiple services reading/writing the same database tables.
   One schema change breaks all services.
   Fix: database per service. Communicate via APIs/events.

3. CHATTY SERVICES
   Service A calls Service B 50 times to render one page.
   Fix: aggregate APIs, BFF pattern, batch endpoints, caching.

4. NANO-SERVICES (too small)
   50 services for a 3-person team. Operational overhead > benefit.
   Fix: start with fewer, larger services. Split when team/scale demands it.

5. NO API CONTRACTS
   Services break each other's integrations with every deploy.
   Fix: contract testing (Pact), API schemas (OpenAPI), versioning.

6. SYNCHRONOUS CHAINS
   A → B → C → D → E. If E is slow, everything is slow.
   Fix: async where possible, circuit breakers, timeouts, caching.

7. MISSING OBSERVABILITY
   Can't trace a request across services. Debugging = guessing.
   Fix: distributed tracing, structured logging, centralized metrics.

8. BIG BANG MIGRATION
   Rewriting the entire monolith at once.
   Fix: Strangler Fig pattern (gradual migration).

9. IGNORING DATA OWNERSHIP
   "Who owns user data?" → "...everyone?"
   Fix: clear bounded contexts, single source of truth per entity.

10. NO IDEMPOTENCY
    Retried messages process the same order twice.
    Fix: idempotency keys on all write operations.
```

---

**Q100. When to use microservices vs monolith — decision framework.**

```
START WITH A MONOLITH unless you have strong reasons not to.
Microservices are a scaling solution, not an architecture goal.

USE A MONOLITH WHEN:
✅ Small team (< 10 engineers)
✅ New product (domain boundaries unclear)
✅ Simple scaling needs (vertical scaling sufficient)
✅ Fast iteration needed (one codebase, one deploy)
✅ Limited DevOps capability

USE MICROSERVICES WHEN:
✅ Large organization (multiple teams, 20+ engineers)
✅ Well-understood domain boundaries
✅ Different scaling needs per component (search vs checkout)
✅ Independent deployment critical (multiple releases/day)
✅ Polyglot requirements (ML in Python, API in Go, UI in Node)
✅ Strong DevOps/platform team

MIGRATION SIGNALS (monolith → microservices):
- Deployments are risky and take hours
- Teams step on each other's code constantly
- One component's scaling needs are 10× others
- New developers take months to understand the codebase
- Test suite takes 45+ minutes

THE "MODULAR MONOLITH" MIDDLE GROUND:
  Monolith deployment but with clear module boundaries.
  Each module: own directory, own DB schema, communicates via internal APIs.
  When ready: extract a module into a service (it's already decoupled).

  Monolith → Modular Monolith → Selective Microservices
  This is the pragmatic path. Don't jump to microservices day one.

COST REALITY:
  Monolith: 1 server, 1 pipeline, 1 log file, 1 person can run it
  Microservices: 20+ servers, 20+ pipelines, distributed tracing,
    service mesh, API gateway, message broker, container orchestration
  The operational tax is REAL. Make sure the benefits outweigh it.
```
