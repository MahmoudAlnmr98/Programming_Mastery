# RabbitMQ, gRPC, Protobuf & MinIO — Complete Reference Guide (Zero to Advanced)

> This guide assumes zero prior knowledge of any of these technologies. Every concept is explained from first principles — what the problem is, why the technology exists, how it works internally, and how to use it in TypeScript production systems.

---

## Table of Contents

1. [Asynchronous Systems — Why They Exist](#1-asynchronous-systems--why-they-exist)
2. [Message Queues — Core Concepts](#2-message-queues--core-concepts)
3. [RabbitMQ — Architecture Deep Dive](#3-rabbitmq--architecture-deep-dive)
4. [RabbitMQ Exchange Types — Every One Explained](#4-rabbitmq-exchange-types--every-one-explained)
5. [RabbitMQ Queue Properties & Message Lifecycle](#5-rabbitmq-queue-properties--message-lifecycle)
6. [Dead Letter Queues & Retry Patterns](#6-dead-letter-queues--retry-patterns)
7. [RabbitMQ in TypeScript — Complete Guide](#7-rabbitmq-in-typescript--complete-guide)
8. [RabbitMQ Production Patterns](#8-rabbitmq-production-patterns)
9. [gRPC — What It Is and Why It Exists](#9-grpc--what-it-is-and-why-it-exists)
10. [Protocol Buffers (Protobuf) — Complete Guide](#10-protocol-buffers-protobuf--complete-guide)
11. [gRPC Service Types — All Four Explained](#11-grpc-service-types--all-four-explained)
12. [gRPC in TypeScript — Complete Guide](#12-grpc-in-typescript--complete-guide)
13. [gRPC Production Patterns](#13-grpc-production-patterns)
14. [MinIO — Object Storage from Zero](#14-minio--object-storage-from-zero)
15. [MinIO Core Concepts](#15-minio-core-concepts)
16. [MinIO in TypeScript — Complete Guide](#16-minio-in-typescript--complete-guide)
17. [MinIO Production Patterns](#17-minio-production-patterns)
18. [System Design — How They Fit Together](#18-system-design--how-they-fit-together)

---

## 1. Asynchronous Systems — Why They Exist

### The Problem: Synchronous Coupling

Imagine you're building an e-commerce system. When a user places an order, you need to:

1. Save the order to the database
2. Charge the user's payment method
3. Send a confirmation email
4. Notify the warehouse to pick the items
5. Update inventory counts
6. Generate an invoice PDF
7. Log the sale in the analytics system

**If you do this synchronously (one by one, in-request):**

```
User clicks "Place Order"
  → saveOrder() — 50ms
  → chargePayment() — 800ms (network call to Stripe)
  → sendEmail() — 300ms (SMTP)
  → notifyWarehouse() — 200ms (HTTP call)
  → updateInventory() — 50ms
  → generateInvoice() — 500ms (PDF generation)
  → logAnalytics() — 100ms
  → Return response to user
Total: ~2000ms (2 seconds!) before user sees "Order confirmed"

Problems:
  ❌ User waits 2 seconds for things they don't need to see immediately
  ❌ If email service is down, the ENTIRE order fails
  ❌ If PDF generation crashes, the user gets an error even though the order was saved
  ❌ All services must be available at the same time
  ❌ Can't retry individual failures — the whole thing succeeds or fails
  ❌ Hard to scale — payment and PDF generation have very different load patterns
```

**With asynchronous messaging:**

```
User clicks "Place Order"
  → saveOrder() — 50ms
  → chargePayment() — 800ms (must be synchronous — need confirmation)
  → publish("order.confirmed", orderData) — 5ms (publish to message queue)
  → Return "Order confirmed!" to user
Total: ~855ms — user is happy immediately

Meanwhile, in the background:
  [queue: email]     → Email service sends confirmation — if it fails, retry later
  [queue: warehouse] → Warehouse service processes the notification
  [queue: inventory] → Inventory service updates counts
  [queue: invoice]   → Invoice service generates PDF and stores in MinIO
  [queue: analytics] → Analytics service logs the sale

Benefits:
  ✅ User gets fast response — only essential work done in-request
  ✅ Each service fails independently — email outage doesn't affect orders
  ✅ Each service retries independently — failed PDF generation retries without affecting anything else
  ✅ Services can be scaled separately — warehouse might need 10 workers, analytics might need 1
  ✅ Message persisted in queue — if warehouse service is down, message is held until it comes back
```

### The Trade-offs of Async

```
Async is NOT always better:

Use SYNCHRONOUS (direct HTTP/gRPC) when:
  ✅ You need the result immediately (user authentication, payment confirmation)
  ✅ The operation is fast (< 200ms)
  ✅ The caller MUST know if it succeeded
  ✅ You need transactional consistency (bank transfer needs to succeed atomically)

Use ASYNCHRONOUS (message queue) when:
  ✅ The work can be done later (background jobs)
  ✅ The work is slow (AI inference, PDF generation, video encoding)
  ✅ The caller doesn't need the result right away
  ✅ You want to decouple services
  ✅ You need fan-out (one event → many systems)
  ✅ You need buffering (spike of 10,000 requests, process at steady rate of 100/s)
  ✅ You need retry on failure
  ✅ The receiving service might be down temporarily
```

---

## 2. Message Queues — Core Concepts

### What a Message Queue Is

A message queue is a **durable, ordered buffer** that sits between a producer (sender) and consumer (receiver). It decouples them in three dimensions:

```
Space decoupling:
  Producer and consumer don't need to know each other's location or address.
  Producer sends to a named queue; consumer reads from a named queue.

Time decoupling:
  Producer and consumer don't need to be running at the same time.
  Messages are stored until the consumer is ready to process them.

Synchronization decoupling:
  Producer doesn't wait for consumer to finish.
  Fire and forget: publish, return immediately.
```

### Key Properties of Message Queues

```
Persistence (Durability):
  Durable queues + persistent messages = messages survive broker restarts.
  In-memory queues = faster but lost on crash.

Ordering:
  Most queues are FIFO (First In, First Out) — messages delivered in order sent.
  With multiple consumers, strict ordering is harder to guarantee.
  For strict ordering: one consumer per queue (or partition-keyed consumers).

Delivery Guarantees:
  At-most-once: message delivered 0 or 1 times (possible loss, no duplicates).
  At-least-once: message delivered 1 or more times (no loss, possible duplicates).
    → YOUR code must be idempotent (safe to process the same message twice).
  Exactly-once: message delivered exactly 1 time.
    → Very hard to achieve; requires coordination between producer, broker, and consumer.
    → RabbitMQ with publisher confirms + consumer acks approaches at-least-once.
    → For exactly-once semantics, use transactional outbox pattern.

Backpressure:
  If consumers are slower than producers, the queue grows.
  The queue buffers this difference.
  Operators can monitor queue depth as a health signal.
```

---

## 3. RabbitMQ — Architecture Deep Dive

### What RabbitMQ Is

RabbitMQ is an open-source **message broker** that implements the **AMQP 0-9-1 protocol** (Advanced Message Queuing Protocol). It was originally built by Rabbit Technologies (now VMware/Broadcom).

```
Key characteristics:
  Protocol: AMQP 0-9-1 (and MQTT, STOMP via plugins)
  Written in: Erlang (extremely reliable concurrent language)
  Delivery semantics: at-least-once with manual acks
  Ordering: FIFO per queue, per consumer
  Durability: optional (durable queues + persistent messages)
  Routing: flexible via exchanges (direct, fanout, topic, headers)
  Clustering: multiple nodes, queue mirroring or quorum queues
  Management UI: built-in web interface at port 15672
```

### The Complete Message Flow

```
Producer (your service)
    │
    │  TCP connection → AMQP channel
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                     RabbitMQ Broker                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   Virtual Host (vhost)            │   │
│  │                                                  │   │
│  │   ┌──────────────┐      ┌──────────────────────┐ │   │
│  │   │   Exchange   │─────▶│       Queue          │ │   │
│  │   │              │      │  ┌────────────────┐  │ │   │
│  │   │ (routes msgs)│      │  │ msg1 msg2 msg3 │  │ │   │
│  │   └──────────────┘      │  └────────────────┘  │ │   │
│  │          │              └──────────────────────┘ │   │
│  │      binding                       │              │   │
│  │    (routing key                    │              │   │
│  │      or pattern)                   │              │   │
│  └────────────────────────────────────┼──────────────┘   │
│                                       │                   │
└───────────────────────────────────────┼───────────────────┘
                                        │
                                        │  AMQP channel
                                        ▼
                                  Consumer (your service)
                                  processes message,
                                  sends ACK or NACK
```

### Virtual Hosts (vhosts)

```
A vhost is logical isolation within a single RabbitMQ broker.

Think of it like: one PostgreSQL server → multiple databases
                  one RabbitMQ broker  → multiple vhosts

Each vhost has:
  - Its own exchanges
  - Its own queues
  - Its own bindings
  - Its own permissions

Usage:
  vhost "/" (default) — for development or single-app setups
  vhost "/production" — production app
  vhost "/staging"    — staging environment
  vhost "/app-a"      — service A's exchanges and queues
  vhost "/app-b"      — service B's exchanges and queues (completely isolated)

Connection string includes vhost:
  amqp://user:password@host:5672/vhost
  amqp://admin:secret@rabbitmq:5672/%2F   ← %2F is URL-encoded "/"
```

### Connections vs Channels

```
TCP Connection:
  Expensive to create (~50ms, resource-intensive)
  One per process/service (maybe a few for high-throughput)
  Persistent — kept alive with heartbeats

AMQP Channel:
  Lightweight virtual connection over the TCP connection
  Very cheap to create — hundreds per TCP connection
  One per thread/coroutine/consumer (channels are NOT thread-safe)
  Each publisher and each consumer uses its own channel

                    ┌──────────────────────────────────────┐
  TCP Connection →  │  Channel 1: consume queue "jobs"     │
                    │  Channel 2: publish to "events"       │
                    │  Channel 3: consume queue "results"   │
                    │  Channel N: ...                       │
                    └──────────────────────────────────────┘
```

---

## 4. RabbitMQ Exchange Types — Every One Explained

### Default Exchange

```
The default exchange has no name ("").
Every queue is automatically bound to the default exchange with the queue name as binding key.

publish(exchange="", routingKey="my-queue", message)
  → delivered to queue named "my-queue"

Simple, but inflexible — no routing logic.
```

### Direct Exchange

```
Routing: exact match on routing key

Exchange: "notifications"
  Binding: queue "email-notifications"  ← bound with key "email"
  Binding: queue "sms-notifications"    ← bound with key "sms"
  Binding: queue "push-notifications"   ← bound with key "push"

publish(exchange="notifications", routingKey="email", msg) → email queue only
publish(exchange="notifications", routingKey="sms", msg)   → sms queue only
publish(exchange="notifications", routingKey="other", msg) → DROPPED (no binding)

Multiple queues can share the same binding key:
  queue "email-notifications" ← bound with "email"
  queue "all-notifications"   ← ALSO bound with "email"
  publish(key="email") → BOTH queues receive the message

Use cases:
  ✅ Simple task routing by type
  ✅ Worker queues where specific workers handle specific job types
  ✅ Routing to specific microservices
```

### Fanout Exchange

```
Routing: ignores routing key — delivers to ALL bound queues

Exchange: "order.events"
  Binding: queue "email-service"
  Binding: queue "analytics-service"
  Binding: queue "inventory-service"
  Binding: queue "audit-service"

publish(exchange="order.events", routingKey="anything", msg)
  → ALL FOUR queues receive a copy of the message

Adding a new service:
  Just bind a new queue to the exchange — no code changes needed anywhere else!
  The publisher doesn't even know who is listening.

Use cases:
  ✅ Broadcasting events to all interested services (order placed, user signed up)
  ✅ Cache invalidation (publish once, all cache nodes receive)
  ✅ Pub/sub where every subscriber gets every message
  ✅ Logging/monitoring (every message copy goes to a logging queue)
```

### Topic Exchange

```
Routing: wildcard pattern matching on routing key

Routing key: dot-separated words  e.g., "order.payment.failed"
Binding patterns:
  *  matches exactly ONE word
  #  matches ZERO OR MORE words (including none)

Exchange: "app.events"
  Binding: queue "payment-errors"  ← bound with "*.payment.failed"
  Binding: queue "all-errors"      ← bound with "#.failed"
  Binding: queue "order-events"    ← bound with "order.#"
  Binding: queue "everything"      ← bound with "#"

publish(key="order.payment.failed")
  → "*.payment.failed" matches (order = one word) → payment-errors ✅
  → "#.failed" matches (order.payment = zero or more words) → all-errors ✅
  → "order.#" matches (payment.failed = zero or more words) → order-events ✅
  → "#" matches everything → everything ✅
  Result: ALL FOUR queues receive it

publish(key="user.signup")
  → "*.payment.failed" → NO match
  → "#.failed" → NO match (doesn't end in "failed")
  → "order.#" → NO match (doesn't start with "order")
  → "#" → YES match → everything ✅
  Result: ONLY "everything" queue receives it

Real-world routing key conventions:
  "service.entity.action" → "order.payment.succeeded"
  "env.service.event"     → "prod.auth.login.failed"
  "priority.type"         → "high.email" or "low.report"

Use cases:
  ✅ Routing by service + severity ("user.*.error" = all user service errors)
  ✅ Multi-tenant routing ("tenant-a.#" = all events for tenant A)
  ✅ Flexible subscriptions where consumers pick what they care about
```

### Headers Exchange

```
Routing: based on message header key-value pairs (not routing key)

Rarely used in practice — topic exchange usually suffices.
Only mention if asked: routes on message headers with x-match=all (all headers must match)
or x-match=any (any header must match).
```

---

## 5. RabbitMQ Queue Properties & Message Lifecycle

### Queue Properties Explained

```typescript
// Queue declaration options
channel.assertQueue("task-queue", {
  // DURABILITY — survives broker restart?
  durable: true,
  // durable: true  → queue meta-data written to disk, survives restart
  // durable: false → in-memory only, faster, deleted on restart
  // For production: always durable: true

  // EXCLUSIVITY — only this connection can use it?
  exclusive: false,
  // exclusive: true  → only current connection can access; deleted when connection closes
  // exclusive: false → any connection can access
  // Use exclusive: true for temporary reply queues (RPC pattern)

  // AUTO-DELETE — delete when no consumers?
  autoDelete: false,
  // autoDelete: true  → queue deleted when last consumer disconnects
  // autoDelete: false → queue persists even with no consumers
  // Use autoDelete: true for transient subscription queues

  arguments: {
    // DEAD LETTER EXCHANGE — where failed messages go
    "x-dead-letter-exchange": "dlx",
    "x-dead-letter-routing-key": "failed",

    // MESSAGE TTL — messages expire after N milliseconds
    "x-message-ttl": 86400000, // 24 hours

    // QUEUE TTL — queue deleted after N ms of no consumers
    "x-expires": 3600000, // 1 hour

    // MAX LENGTH — queue length limit (oldest messages dropped or dead-lettered)
    "x-max-length": 10000,
    "x-max-length-bytes": 10 * 1024 * 1024, // 10MB

    // QUEUE TYPE — for quorum queues (highly available, replicated)
    "x-queue-type": "quorum",
    // quorum queues: replicated across cluster nodes, safer than classic mirrored queues
    // Use for: production queues that must not lose data

    // PRIORITY QUEUE — messages with higher priority are delivered first
    "x-max-priority": 10, // enables priority 0-10
  },
});
```

### Message Properties

```typescript
// Each message has properties attached
channel.publish(exchange, routingKey, content, {
  // PERSISTENCE
  persistent: true,
  // persistent: true  → message written to disk (survives broker restart)
  // persistent: false → in-memory only
  // Note: BOTH queue must be durable AND message must be persistent for full durability
  // deliveryMode: 2 is equivalent to persistent: true

  // EXPIRATION — message dies after N milliseconds if not consumed
  expiration: "60000", // 60 seconds (string, not number!)

  // MESSAGE ID — unique identifier for deduplication
  messageId: crypto.randomUUID(),

  // CORRELATION ID — for request-reply pattern (link reply to request)
  correlationId: requestId,

  // REPLY TO — where to send the reply (request-reply pattern)
  replyTo: "response-queue",

  // CONTENT TYPE — hint for consumers
  contentType: "application/json",

  // PRIORITY — for priority queues (0-9 or 0-255 depending on config)
  priority: 5,

  // HEADERS — custom metadata
  headers: {
    "x-retry-count": 0,
    "x-source-service": "api-server",
    "x-trace-id": traceId,
  },

  // TIMESTAMP — when the message was created
  timestamp: Math.floor(Date.now() / 1000), // Unix timestamp (seconds)
});
```

### Acknowledgment Modes

```
This is CRITICAL for reliability:

AUTO-ACK (noAck: true):
  Message is deleted from queue AS SOON AS it's delivered to consumer.
  If consumer crashes mid-processing, message is LOST FOREVER.
  Only use for: fire-and-forget metrics, idempotent operations you don't care about losing

MANUAL ACK (noAck: false — recommended):
  Consumer explicitly acknowledges after successfully processing.
  If consumer crashes before acking, message is requeued and redelivered.
  
  ack(deliveryTag)
    → "I successfully processed this message, remove it from the queue"
    → Message is permanently deleted from queue

  nack(deliveryTag, { requeue: true })
    → "I failed to process this message, put it back in the queue for retry"
    → Message goes back to the front of the queue
    → WARNING: if the message always fails, you get an infinite loop!
    → Combine with dead letter queue + retry limits

  nack(deliveryTag, { requeue: false })
    → "I cannot process this message, send it to the dead letter exchange"
    → If DLX configured: message goes to DLX → DLQ
    → If no DLX: message is discarded

  nack(deliveryTag, { multiple: true, requeue: false })
    → nack ALL unacknowledged messages up to this delivery tag

PREFETCH (QoS — Quality of Service):
  channel.prefetch(N)
  → Consumer receives at most N unacknowledged messages at once
  → CRITICAL: without prefetch, RabbitMQ delivers ALL messages in queue to one consumer!

  Without prefetch (broken):
    10 consumers. 100 messages. RabbitMQ round-robins:
    consumer1 gets messages 1,11,21,31...
    consumer2 gets messages 2,12,22,32...
    If consumer1 is busy with message 1, messages 11,21,31... are held waiting for it!
    Consumer2 might be idle!

  With prefetch(1) (correct):
    Each consumer gets ONE message at a time.
    When it finishes and acks, it gets the next one.
    Fast consumers get more messages. Slow consumers don't get overloaded.
    This is FAIR DISPATCH.

  Recommended values:
    prefetch(1): safest — one at a time, perfectly fair, lowest throughput
    prefetch(10-100): good balance for fast jobs
    prefetch(0): unlimited — don't do this in production
```

---

## 6. Dead Letter Queues & Retry Patterns

### What is a Dead Letter Queue?

A message becomes a "dead letter" when:
1. It is explicitly rejected (nacked) with `requeue: false`
2. It expires (TTL elapsed while in queue)
3. The queue reaches its maximum length

Dead letters are sent to the **Dead Letter Exchange (DLX)**, which routes them to the **Dead Letter Queue (DLQ)** for inspection and retry.

### Complete DLQ Setup

```typescript
// SETUP: exchanges and queues
async function setupQueues(channel: Channel): Promise<void> {
  // 1. Create the Dead Letter Exchange (DLX)
  await channel.assertExchange("dlx", "direct", { durable: true });

  // 2. Create the Dead Letter Queue (DLQ) — where failed messages land
  await channel.assertQueue("dlq", {
    durable: true,
    // The DLQ itself has no DLX — messages that fail in DLQ stay there
  });

  // 3. Bind DLQ to DLX
  await channel.bindQueue("dlq", "dlx", "failed");

  // 4. Create the actual work queue — configured to send failures to DLX
  await channel.assertQueue("tasks", {
    durable: true,
    arguments: {
      "x-dead-letter-exchange": "dlx",
      "x-dead-letter-routing-key": "failed",
      "x-message-ttl": 300000,          // messages expire after 5 minutes
    },
  });

  // 5. Create the work exchange and bind
  await channel.assertExchange("work", "direct", { durable: true });
  await channel.bindQueue("tasks", "work", "task");
}
```

### Retry with Exponential Backoff Pattern

```typescript
// PATTERN: Delayed Retry with Exponential Backoff
// When a message fails, don't just requeue immediately — wait before retry!
// This prevents hammering a failing downstream service.

// Setup: create delay queues with per-level TTLs
async function setupRetryQueues(channel: Channel): Promise<void> {
  // Main work exchange
  await channel.assertExchange("work", "direct", { durable: true });

  // DLX (for messages that exhausted all retries)
  await channel.assertExchange("dlx", "direct", { durable: true });
  await channel.assertQueue("dlq-final", { durable: true });
  await channel.bindQueue("dlq-final", "dlx", "dead");

  // Main work queue
  await channel.assertQueue("tasks", {
    durable: true,
    arguments: {
      "x-dead-letter-exchange": "work",  // on nack, go back to work exchange
      "x-dead-letter-routing-key": "retry",
    },
  });
  await channel.bindQueue("tasks", "work", "task");

  // Retry queue with delay levels (using TTL + dead-letter trick)
  const delays = [5000, 30000, 300000, 1800000]; // 5s, 30s, 5min, 30min

  for (let i = 0; i < delays.length; i++) {
    const queueName = `retry-delay-${i}`;
    await channel.assertQueue(queueName, {
      durable: true,
      arguments: {
        "x-message-ttl": delays[i],        // wait this long, then...
        "x-dead-letter-exchange": "work",  // ...send back to the work exchange
        "x-dead-letter-routing-key": "task", // ...as a regular task
        "x-expires": delays[i] * 3,        // delete the queue if unused
      },
    });
    await channel.bindQueue(queueName, "work", `retry-level-${i}`);
  }
}

// Consumer with retry logic
async function consumeWithRetry(channel: Channel): Promise<void> {
  await channel.prefetch(10);

  await channel.consume("tasks", async (msg) => {
    if (!msg) return;

    try {
      const payload = JSON.parse(msg.content.toString());
      const retryCount = (msg.properties.headers?.["x-retry-count"] as number) ?? 0;

      await processTask(payload);
      channel.ack(msg);

    } catch (error) {
      const retryCount = (msg.properties.headers?.["x-retry-count"] as number) ?? 0;
      const maxRetries = 4;

      if (retryCount < maxRetries) {
        // Send to the appropriate delay queue
        channel.nack(msg, false, false); // reject without requeue

        // Publish to the delay queue for this retry level
        channel.publish(
          "work",
          `retry-level-${retryCount}`,
          msg.content,
          {
            persistent: true,
            headers: {
              ...msg.properties.headers,
              "x-retry-count": retryCount + 1,
              "x-last-error": (error as Error).message,
              "x-original-queue": "tasks",
            },
          }
        );

        console.log(`Message scheduled for retry ${retryCount + 1}/${maxRetries} in ${[5,30,300,1800][retryCount]}s`);
      } else {
        // Exhausted retries — send to final dead letter queue
        channel.nack(msg, false, false);
        channel.publish(
          "dlx",
          "dead",
          msg.content,
          {
            persistent: true,
            headers: {
              ...msg.properties.headers,
              "x-final-error": (error as Error).message,
              "x-failed-at": new Date().toISOString(),
            },
          }
        );
        console.error(`Message permanently failed after ${maxRetries} retries`);
      }
    }
  });
}
```

---

## 7. RabbitMQ in TypeScript — Complete Guide

### Installation and Connection

```bash
npm install amqplib
npm install -D @types/amqplib
```

```typescript
// lib/rabbitmq.ts — robust connection with reconnection
import amqplib, { Connection, Channel, ConsumeMessage } from "amqplib";

interface RabbitMQConfig {
  url: string;
  reconnectDelay?: number;
  heartbeat?: number;
}

class RabbitMQConnection {
  private connection: Connection | null = null;
  private channel: Channel | null = null;
  private isConnecting = false;
  private reconnectTimer: NodeJS.Timeout | null = null;

  constructor(private readonly config: RabbitMQConfig) {}

  async connect(): Promise<void> {
    if (this.isConnecting) return;
    this.isConnecting = true;

    try {
      this.connection = await amqplib.connect(this.config.url, {
        heartbeat: this.config.heartbeat ?? 60, // detect dead connections
      });

      this.connection.on("error", (err) => {
        console.error("RabbitMQ connection error:", err.message);
        this.reconnect();
      });

      this.connection.on("close", () => {
        console.warn("RabbitMQ connection closed, reconnecting...");
        this.reconnect();
      });

      this.channel = await this.connection.createChannel();

      this.channel.on("error", (err) => {
        console.error("RabbitMQ channel error:", err.message);
      });

      this.channel.on("close", () => {
        console.warn("RabbitMQ channel closed");
      });

      console.log("✅ Connected to RabbitMQ");
      this.isConnecting = false;
    } catch (error) {
      this.isConnecting = false;
      console.error("Failed to connect to RabbitMQ:", (error as Error).message);
      this.reconnect();
    }
  }

  private reconnect(): void {
    if (this.reconnectTimer) return;
    const delay = this.config.reconnectDelay ?? 5000;
    console.log(`Reconnecting to RabbitMQ in ${delay}ms...`);
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connection = null;
      this.channel = null;
      this.connect();
    }, delay);
  }

  async getChannel(): Promise<Channel> {
    if (!this.channel) {
      await this.connect();
    }
    return this.channel!;
  }

  async close(): Promise<void> {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }
    await this.channel?.close();
    await this.connection?.close();
  }
}

// Singleton instance
let _rabbitMQ: RabbitMQConnection | null = null;

export function getRabbitMQ(): RabbitMQConnection {
  if (!_rabbitMQ) {
    _rabbitMQ = new RabbitMQConnection({
      url: process.env.RABBITMQ_URL ?? "amqp://guest:guest@localhost:5672",
      reconnectDelay: 5000,
      heartbeat: 60,
    });
  }
  return _rabbitMQ;
}
```

### Type-Safe Message Publisher

```typescript
// lib/publisher.ts

// Define all message types with their schemas
export interface Messages {
  "ai.inference.request": {
    jobId: string;
    conversationId: string;
    messages: Array<{ role: string; content: string }>;
    model: string;
    temperature: number;
    maxTokens: number;
    userId: string;
    orgId: string;
  };
  "ai.inference.complete": {
    jobId: string;
    conversationId: string;
    content: string;
    tokensUsed: number;
    model: string;
    durationMs: number;
  };
  "notification.email": {
    to: string;
    subject: string;
    templateId: string;
    templateData: Record<string, unknown>;
    userId?: string;
  };
  "notification.push": {
    userId: string;
    title: string;
    body: string;
    data?: Record<string, unknown>;
  };
  "file.uploaded": {
    fileId: string;
    bucket: string;
    objectKey: string;
    userId: string;
    orgId: string;
    contentType: string;
    sizeBytes: number;
  };
  "user.created": {
    userId: string;
    orgId: string;
    email: string;
    name: string;
  };
}

export type MessageType = keyof Messages;

class TypedPublisher {
  constructor(private readonly connection: RabbitMQConnection) {}

  async publish<T extends MessageType>(
    type: T,
    payload: Messages[T],
    options?: {
      priority?: number;
      delay?: number;
      correlationId?: string;
      traceId?: string;
    }
  ): Promise<void> {
    const channel = await this.connection.getChannel();

    const message = {
      type,
      payload,
      messageId: crypto.randomUUID(),
      timestamp: Date.now(),
      version: "1.0",
    };

    const content = Buffer.from(JSON.stringify(message));
    const routingKey = type; // e.g., "ai.inference.request"

    // Use topic exchange for flexible routing
    const published = channel.publish(
      "app.events",     // exchange name
      routingKey,
      content,
      {
        persistent: true,
        contentType: "application/json",
        messageId: message.messageId,
        timestamp: Math.floor(Date.now() / 1000),
        correlationId: options?.correlationId,
        priority: options?.priority,
        headers: {
          "x-trace-id": options?.traceId ?? crypto.randomUUID(),
          "x-source": process.env.SERVICE_NAME ?? "api",
          "x-retry-count": 0,
        },
      }
    );

    if (!published) {
      // Channel buffer full — wait for drain event
      await new Promise<void>((resolve) => channel.once("drain", resolve));
    }
  }

  // Convenience methods
  async publishAiInference(payload: Messages["ai.inference.request"]): Promise<void> {
    return this.publish("ai.inference.request", payload);
  }

  async publishEmail(payload: Messages["notification.email"]): Promise<void> {
    return this.publish("notification.email", payload);
  }

  async publishFileUploaded(payload: Messages["file.uploaded"]): Promise<void> {
    return this.publish("file.uploaded", payload);
  }
}
```

### Publisher Confirms — Guaranteed Delivery

```typescript
// Publisher confirms: RabbitMQ acks/nacks each published message
// Ensures the broker received and persisted the message (NOT that consumer received it)

async function publishWithConfirm<T extends MessageType>(
  channel: ConfirmChannel,  // not Channel — ConfirmChannel
  type: T,
  payload: Messages[T]
): Promise<void> {
  const content = Buffer.from(JSON.stringify({ type, payload, messageId: crypto.randomUUID() }));

  return new Promise((resolve, reject) => {
    channel.publish(
      "app.events",
      type,
      content,
      { persistent: true, contentType: "application/json" },
      (err, ok) => {
        // Callback called when broker confirms or rejects
        if (err) {
          reject(new Error(`Message rejected by broker: ${err.message}`));
        } else {
          resolve(); // broker persisted the message
        }
      }
    );
  });
}

// Create a confirm channel:
const channel = await connection.createConfirmChannel(); // NOT createChannel()
// ConfirmChannel waits for broker ACK on each publish
```

### Type-Safe Consumer

```typescript
// lib/consumer.ts

interface ConsumeOptions {
  prefetch?: number;       // max unacked messages (default: 10)
  noAck?: boolean;         // auto-ack (default: false)
  maxRetries?: number;     // max retry count (default: 3)
}

class TypedConsumer {
  constructor(private readonly connection: RabbitMQConnection) {}

  async subscribe<T extends MessageType>(
    messageType: T,
    queueName: string,
    handler: (payload: Messages[T], metadata: MessageMetadata) => Promise<void>,
    options: ConsumeOptions = {}
  ): Promise<void> {
    const { prefetch = 10, noAck = false, maxRetries = 3 } = options;

    const channel = await this.connection.getChannel();
    await channel.prefetch(prefetch);

    await channel.consume(queueName, async (msg) => {
      if (!msg) {
        // null msg = consumer cancelled by broker
        console.warn(`Consumer cancelled for queue: ${queueName}`);
        return;
      }

      const retryCount = (msg.properties.headers?.["x-retry-count"] as number) ?? 0;
      let parsed: { type: string; payload: Messages[T]; messageId: string };

      // Parse message
      try {
        parsed = JSON.parse(msg.content.toString());
      } catch (parseError) {
        console.error("Failed to parse message — sending to DLQ");
        channel.nack(msg, false, false); // don't requeue unparseable messages
        return;
      }

      // Type guard — ensure message type matches subscription
      if (parsed.type !== messageType) {
        console.warn(`Unexpected message type: ${parsed.type}, expected: ${messageType}`);
        channel.nack(msg, false, false);
        return;
      }

      const metadata: MessageMetadata = {
        messageId: msg.properties.messageId ?? parsed.messageId,
        correlationId: msg.properties.correlationId,
        traceId: msg.properties.headers?.["x-trace-id"] as string,
        retryCount,
        deliveryTag: msg.fields.deliveryTag,
        redelivered: msg.fields.redelivered,
        timestamp: msg.properties.timestamp
          ? new Date(msg.properties.timestamp * 1000)
          : new Date(),
      };

      // Process message
      try {
        await handler(parsed.payload, metadata);
        channel.ack(msg); // SUCCESS — remove from queue

      } catch (error) {
        const err = error as Error;
        console.error(`Error processing message ${metadata.messageId}:`, err.message);

        if (retryCount < maxRetries) {
          // Schedule retry (requeue with delay)
          channel.nack(msg, false, false); // reject without requeue
          // Publisher will re-publish to retry delay queue
          console.log(`Scheduling retry ${retryCount + 1}/${maxRetries} for message ${metadata.messageId}`);
        } else {
          // Max retries exhausted — dead letter
          channel.nack(msg, false, false);
          console.error(`Message ${metadata.messageId} permanently failed after ${maxRetries} retries`);
        }
      }
    }, { noAck });
  }
}

interface MessageMetadata {
  messageId: string;
  correlationId?: string;
  traceId?: string;
  retryCount: number;
  deliveryTag: number;
  redelivered: boolean;
  timestamp: Date;
}
```

---

## 8. RabbitMQ Production Patterns

### Work Queue Pattern — AI Inference Jobs

```typescript
// Worker service that processes AI inference jobs
async function startAiWorker(): Promise<void> {
  const rabbit = getRabbitMQ();
  const channel = await rabbit.getChannel();

  // Setup topology
  await channel.assertExchange("app.events", "topic", { durable: true });
  await channel.assertExchange("dlx", "direct", { durable: true });
  await channel.assertQueue("dlq", { durable: true });
  await channel.bindQueue("dlq", "dlx", "dead");

  // Main worker queue
  await channel.assertQueue("ai.inference.jobs", {
    durable: true,
    arguments: {
      "x-dead-letter-exchange": "dlx",
      "x-dead-letter-routing-key": "dead",
      "x-message-ttl": 3600000, // 1 hour — expired AI jobs go to DLQ
      "x-max-length": 1000,     // max 1000 queued jobs
    },
  });

  // Bind queue to topic exchange — subscribe to AI inference requests
  await channel.bindQueue("ai.inference.jobs", "app.events", "ai.inference.request");

  // Process one message at a time (AI inference is expensive)
  await channel.prefetch(1);

  await channel.consume("ai.inference.jobs", async (msg) => {
    if (!msg) return;

    const startTime = Date.now();

    try {
      const { payload } = JSON.parse(msg.content.toString()) as {
        payload: Messages["ai.inference.request"];
      };

      console.log(`Processing AI job ${payload.jobId} for conversation ${payload.conversationId}`);

      // Call AI service via gRPC (covered in next section)
      const result = await callAiService(payload);

      // Save result to database
      await saveMessageToDb({
        conversationId: payload.conversationId,
        role: "assistant",
        content: result.content,
        tokensUsed: result.tokensUsed,
        model: payload.model,
      });

      // Publish completion event for SSE streaming / webhook
      await publisher.publish("ai.inference.complete", {
        jobId: payload.jobId,
        conversationId: payload.conversationId,
        content: result.content,
        tokensUsed: result.tokensUsed,
        model: payload.model,
        durationMs: Date.now() - startTime,
      });

      channel.ack(msg);
      console.log(`✅ Job ${payload.jobId} completed in ${Date.now() - startTime}ms`);

    } catch (error) {
      const retryCount = (msg.properties.headers?.["x-retry-count"] as number) ?? 0;
      console.error(`❌ Job failed (attempt ${retryCount + 1}):`, (error as Error).message);

      if (retryCount < 3) {
        channel.nack(msg, false, false);
        // Message goes to DLX, consumer publishes it to delay queue
      } else {
        channel.nack(msg, false, false);
        // After 3 retries, goes to DLQ permanently
      }
    }
  });

  console.log("🤖 AI Worker started, waiting for jobs...");

  // Graceful shutdown
  process.on("SIGTERM", async () => {
    console.log("Worker shutting down...");
    await channel.close();
    await rabbit.close();
    process.exit(0);
  });
}
```

### Request-Reply Pattern (RPC over RabbitMQ)

```typescript
// Sometimes you need a synchronous response over an async channel
// The RPC-over-RabbitMQ pattern:
//   1. Client creates a temporary reply queue
//   2. Client publishes request with replyTo = reply queue name
//   3. Server processes request, publishes response TO reply queue
//   4. Client waits on reply queue, picks up response

class RabbitMQRpcClient {
  private pendingRequests = new Map<string, {
    resolve: (value: unknown) => void;
    reject: (error: Error) => void;
    timeout: NodeJS.Timeout;
  }>();

  constructor(private readonly channel: Channel) {}

  async initialize(): Promise<void> {
    // Create an exclusive reply queue (auto-deleted when connection closes)
    const { queue: replyQueue } = await this.channel.assertQueue("", {
      exclusive: true,
      autoDelete: true,
    });

    // Listen for responses on the reply queue
    await this.channel.consume(replyQueue, (msg) => {
      if (!msg) return;
      const correlationId = msg.properties.correlationId;
      const pending = this.pendingRequests.get(correlationId);

      if (pending) {
        clearTimeout(pending.timeout);
        this.pendingRequests.delete(correlationId);

        const response = JSON.parse(msg.content.toString());
        if (response.error) {
          pending.reject(new Error(response.error));
        } else {
          pending.resolve(response.result);
        }

        this.channel.ack(msg);
      }
    }, { noAck: false });

    this.replyQueue = replyQueue;
  }

  private replyQueue!: string;

  async call<T>(
    queueName: string,
    request: unknown,
    timeoutMs: number = 30000
  ): Promise<T> {
    const correlationId = crypto.randomUUID();

    return new Promise<T>((resolve, reject) => {
      // Set timeout
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(correlationId);
        reject(new Error(`RPC timeout after ${timeoutMs}ms`));
      }, timeoutMs);

      this.pendingRequests.set(correlationId, {
        resolve: resolve as (v: unknown) => void,
        reject,
        timeout,
      });

      // Publish the request
      this.channel.publish(
        "",  // default exchange
        queueName,
        Buffer.from(JSON.stringify(request)),
        {
          correlationId,
          replyTo: this.replyQueue,
          persistent: false,  // RPC requests typically don't need persistence
          expiration: String(timeoutMs),
        }
      );
    });
  }
}
```

---

## 9. gRPC — What It Is and Why It Exists

### The Problem: Cross-Language Service Communication

In a microservices architecture, services are often written in different languages:
- API gateway: TypeScript (Node.js)
- AI inference service: Python (has the best ML libraries)
- Image processing: Go (performance)
- Payment service: Java (enterprise ecosystem)

These services need to call each other. Options:

```
Option 1: REST with JSON
  ✅ Universal, browser-compatible, human-readable
  ❌ JSON parsing overhead (CPU-intensive for large payloads)
  ❌ No native streaming
  ❌ No code generation (each team writes their own client)
  ❌ Types are documentation-only (can get out of sync)
  ❌ HTTP/1.1 (one request per TCP connection by default)

Option 2: gRPC
  ✅ Binary Protocol Buffers (3-10x smaller than JSON, faster serialization)
  ✅ HTTP/2 (multiplexing, streaming, header compression)
  ✅ Native bidirectional streaming
  ✅ Code generation from .proto files (clients in any language, always in sync)
  ✅ Type-safe by definition (Protobuf schema is the contract)
  ✅ Built-in deadline/timeout, cancellation, metadata
  ❌ Not browser-native (needs grpc-web proxy for browser clients)
  ❌ Binary (not human-readable without tooling)
  ❌ Schema evolution requires care (though Protobuf is designed for it)
```

### gRPC vs REST — When to Use Each

```
Use REST/HTTP when:
  ✅ Public APIs (browsers, third-party clients)
  ✅ Simple CRUD operations
  ✅ Team prefers simplicity over performance
  ✅ Existing ecosystem (OpenAPI, Swagger, API gateways)

Use gRPC when:
  ✅ Internal service-to-service communication
  ✅ Performance is critical (low latency, high throughput)
  ✅ Streaming (server-sent events, bidirectional streaming)
  ✅ Multi-language teams (Python AI + TypeScript API + Go worker)
  ✅ Strong typing across service boundaries
  ✅ You're building on infrastructure that already uses gRPC (Kubernetes, Istio)

In the job description context:
  "Integrate backend services with AI components via gRPC" →
  Your TypeScript backend calls a Python AI service using gRPC
  The .proto file defines the contract both teams agree on
```

---

## 10. Protocol Buffers (Protobuf) — Complete Guide

### What is Protobuf?

Protocol Buffers (Protobuf) is Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. It serves as both:
1. The **schema definition language** for gRPC services
2. The **binary serialization format** for the wire

### Writing Proto Files

```protobuf
// proto/ai_service.proto

// Specify proto3 syntax (modern, recommended)
syntax = "proto3";

// Package name — prevents name collisions
package ai.v1;

// Go package option (for Go generated code)
option go_package = "github.com/myorg/myapp/gen/ai/v1;aiv1";

// Import standard types
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";

// ── ENUMS ──────────────────────────────────────────────────────
// Enums always have a zero value (first value)
enum Role {
  ROLE_UNSPECIFIED = 0;  // convention: enum_name_UNSPECIFIED = 0
  ROLE_USER = 1;
  ROLE_ASSISTANT = 2;
  ROLE_SYSTEM = 3;
  ROLE_TOOL = 4;
}

enum FinishReason {
  FINISH_REASON_UNSPECIFIED = 0;
  FINISH_REASON_STOP = 1;         // natural completion
  FINISH_REASON_LENGTH = 2;       // hit max_tokens limit
  FINISH_REASON_TOOL_CALL = 4;    // function/tool call requested
  FINISH_REASON_CONTENT_FILTER = 5; // filtered for safety
}

// ── MESSAGES ────────────────────────────────────────────────────
// A message is like a struct/class — a named group of fields

// Field numbers (1, 2, 3...) are used in binary encoding (NOT the names)
// Field numbers 1-15: one byte in encoding (use for frequent fields)
// Field numbers 16-2047: two bytes (for less common fields)
// NEVER change field numbers on deployed schemas — it breaks compatibility

message ChatMessage {
  // Field: type field_name = field_number;
  Role   role    = 1;
  string content = 2;

  // Optional name for the message author
  optional string name = 3;  // in proto3, optional makes it explicitly nullable

  // Tool call information (for assistant messages)
  repeated ToolCall tool_calls = 4;  // 'repeated' = array/list

  // Timestamp (using well-known type)
  google.protobuf.Timestamp created_at = 5;
}

message ToolCall {
  string id       = 1;  // unique tool call ID
  string name     = 2;  // tool/function name
  string arguments = 3; // JSON string of arguments
}

message ToolResult {
  string tool_call_id = 1;
  string content      = 2;
  bool   is_error     = 3;
}

// Configuration for AI generation
message GenerationConfig {
  string  model       = 1;
  float   temperature = 2;   // float = 32-bit; double = 64-bit
  int32   max_tokens  = 3;   // int32 = signed 32-bit integer
  float   top_p       = 4;
  float   frequency_penalty = 5;
  float   presence_penalty  = 6;
  repeated string stop_sequences = 7;
}

// ── REQUEST / RESPONSE MESSAGES ────────────────────────────────

message GenerateRequest {
  string                   job_id      = 1;  // unique identifier for this request
  repeated ChatMessage     messages    = 2;  // conversation history
  GenerationConfig         config      = 3;  // generation parameters
  string                   user_id     = 4;
  string                   org_id      = 5;

  // Map type — key-value pairs
  map<string, string>      metadata    = 6;
}

message GenerateResponse {
  string        job_id         = 1;
  string        content        = 2;    // complete response content
  int32         prompt_tokens  = 3;
  int32         completion_tokens = 4;
  int32         total_tokens   = 5;
  FinishReason  finish_reason  = 6;
  string        model          = 7;
  repeated ToolCall tool_calls = 8;   // if finish_reason = TOOL_CALL
  google.protobuf.Duration latency = 9;
}

// For streaming responses
message GenerateStreamChunk {
  string       job_id   = 1;
  string       delta    = 2;         // the new text chunk (delta, not full text)
  bool         is_final = 3;         // true on the last chunk
  // Optional: final metadata only sent with is_final=true
  optional int32  total_tokens  = 4;
  optional FinishReason finish_reason = 5;
}

// Error details
message ErrorInfo {
  string code    = 1;
  string message = 2;
  map<string, string> details = 3;
}

// ── SERVICE DEFINITION ──────────────────────────────────────────

service AiService {
  // Unary RPC — one request, one response
  rpc Generate (GenerateRequest) returns (GenerateResponse);

  // Server streaming RPC — one request, stream of responses
  rpc GenerateStream (GenerateRequest) returns (stream GenerateStreamChunk);

  // Health check (following gRPC health protocol)
  rpc HealthCheck (HealthCheckRequest) returns (HealthCheckResponse);
}

message HealthCheckRequest {
  string service = 1;
}

message HealthCheckResponse {
  enum ServingStatus {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
    SERVICE_UNKNOWN = 3;
  }
  ServingStatus status = 1;
}
```

### Protobuf Scalar Types

```protobuf
// All scalar types in proto3:

double    field1 = 1;   // 64-bit float
float     field2 = 2;   // 32-bit float
int32     field3 = 3;   // 32-bit signed integer (variable encoding)
int64     field4 = 4;   // 64-bit signed integer
uint32    field5 = 5;   // 32-bit unsigned integer
uint64    field6 = 6;   // 64-bit unsigned integer
sint32    field7 = 7;   // 32-bit signed (more efficient for negative numbers)
sint64    field8 = 8;   // 64-bit signed (more efficient for negative numbers)
fixed32   field9 = 9;   // always 4 bytes (better for values >= 2^28)
fixed64   fieldA = 10;  // always 8 bytes
sfixed32  fieldB = 11;  // always 4 bytes, signed
sfixed64  fieldC = 12;  // always 8 bytes, signed
bool      fieldD = 13;  // true/false
string    fieldE = 14;  // UTF-8 encoded string
bytes     fieldF = 15;  // arbitrary byte sequence

// Well-known types (import google/protobuf/...)
google.protobuf.Timestamp created_at  = 16;  // nanosecond precision timestamp
google.protobuf.Duration  duration    = 17;  // time duration
google.protobuf.Any       anything    = 18;  // any type (type URL + serialized message)
google.protobuf.Struct    json_object = 19;  // arbitrary JSON object
google.protobuf.Value     json_value  = 20;  // any JSON value
google.protobuf.Empty     empty       = 21;  // void / empty response

// Wrapper types (for nullable primitives)
google.protobuf.StringValue nullable_str = 22;
google.protobuf.Int32Value  nullable_int = 23;
google.protobuf.BoolValue   nullable_bool = 24;
```

### Proto Schema Evolution — Compatibility Rules

```protobuf
// Protobuf is designed for backward and forward compatibility
// FOLLOW THESE RULES to not break existing clients:

// SAFE changes (backward compatible):
//   ✅ Add new fields with new field numbers
//   ✅ Remove fields (old serialized data just ignores unknown fields)
//   ✅ Change field from singular to repeated (or vice versa — with care)
//   ✅ Add new values to enums

// UNSAFE changes (breaking):
//   ❌ Change a field's number (old clients parse wrong field)
//   ❌ Change a field's type (int32 to string breaks serialization)
//   ❌ Remove a field and reuse its number for a different field
//   ❌ Rename a field (field names not in binary encoding — this IS safe for binary, but breaks JSON)
//   ❌ Change required to optional (proto2 only — proto3 has no required)

// Best practices:
message UserV1 {
  string id    = 1;
  string name  = 2;
  string email = 3;
}

// Adding a new field — SAFE
message UserV2 {
  string id         = 1;
  string name       = 2;
  string email      = 3;
  string avatar_url = 4;  // new field — old clients ignore it, new clients read it
}

// WRONG: Don't reuse field numbers after deletion!
message UserV3_WRONG {
  string id      = 1;
  // name was field 2 — DELETED
  string email   = 3;
  int32  age     = 2;  // ❌ reusing field number 2! Old messages had "name" here!
}

// CORRECT: Reserve deleted field numbers
message UserV3_CORRECT {
  string id    = 1;
  reserved 2;           // field 2 ("name") is reserved — can't be reused
  reserved "name";      // reserve the name too (for JSON/reflection safety)
  string email = 3;
  int32  age   = 4;    // use a NEW number
}
```

---

## 11. gRPC Service Types — All Four Explained

```
gRPC has four service types based on streaming:

1. UNARY (one request → one response)
   Like a regular function call over the network.
   rpc GetUser(GetUserRequest) returns (UserResponse);

2. SERVER STREAMING (one request → stream of responses)
   Client sends one request, server sends many responses over time.
   Perfect for: progress updates, AI token streaming, real-time feeds.
   rpc GenerateStream(GenerateRequest) returns (stream GenerateStreamChunk);

3. CLIENT STREAMING (stream of requests → one response)
   Client sends many messages, server responds with one summary.
   Perfect for: uploading large files in chunks, batch operations.
   rpc UploadChunks(stream FileChunk) returns (UploadSummary);

4. BIDIRECTIONAL STREAMING (stream of requests ↔ stream of responses)
   Both sides send streams simultaneously, independently.
   Perfect for: real-time chat, collaborative editing, live telemetry.
   rpc Chat(stream ChatMessage) returns (stream ChatMessage);
```

---

## 12. gRPC in TypeScript — Complete Guide

### Installation and Code Generation

```bash
# Install runtime packages
npm install @grpc/grpc-js @grpc/proto-loader
npm install google-protobuf

# Install code generation tools (dev only)
npm install -D grpc-tools ts-proto
# ts-proto generates TypeScript code from .proto files
# grpc-tools includes protoc (the proto compiler)

# package.json script
{
  "scripts": {
    "proto:gen": "protoc --plugin=protoc-gen-ts_proto=./node_modules/.bin/protoc-gen-ts_proto --ts_proto_out=./src/gen --ts_proto_opt=outputServices=grpc-js,esModuleInterop=true,env=node -I ./proto ./proto/*.proto"
  }
}
```

### Generated TypeScript (ts-proto output)

```typescript
// src/gen/ai_service.ts — auto-generated by ts-proto (DO NOT EDIT)
// This is what ts-proto generates from your .proto file

export interface ChatMessage {
  role: Role;
  content: string;
  name?: string | undefined;
  toolCalls: ToolCall[];
  createdAt?: Date | undefined;
}

export interface GenerateRequest {
  jobId: string;
  messages: ChatMessage[];
  config: GenerationConfig | undefined;
  userId: string;
  orgId: string;
  metadata: { [key: string]: string };
}

export interface GenerateResponse {
  jobId: string;
  content: string;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  finishReason: FinishReason;
  model: string;
  toolCalls: ToolCall[];
}

export interface GenerateStreamChunk {
  jobId: string;
  delta: string;
  isFinal: boolean;
  totalTokens?: number | undefined;
  finishReason?: FinishReason | undefined;
}

// Service client interface — generated by ts-proto
export interface AiServiceClient {
  generate(
    request: GenerateRequest,
    callback: (error: ServiceError | null, response: GenerateResponse) => void
  ): ClientUnaryCall;

  generateStream(
    request: GenerateRequest
  ): ClientReadableStream<GenerateStreamChunk>;
}
```

### gRPC Client (TypeScript → AI Service)

```typescript
// lib/ai-client.ts

import * as grpc from "@grpc/grpc-js";
import {
  AiServiceClient,
  GenerateRequest,
  GenerateResponse,
  GenerateStreamChunk,
} from "../gen/ai_service";
import { AiServiceDefinition } from "../gen/ai_service.grpc-server"; // from ts-proto

// Create a gRPC client
function createAiClient(address: string): AiServiceClient {
  const credentials = process.env.NODE_ENV === "production"
    ? grpc.credentials.createSsl() // TLS for production
    : grpc.credentials.createInsecure(); // no TLS for local dev

  return new AiServiceClient(
    address, // "ai-service:50051" or "localhost:50051"
    credentials,
    {
      // Channel options for reliability
      "grpc.keepalive_time_ms": 10000,          // send keepalive ping every 10s
      "grpc.keepalive_timeout_ms": 5000,         // wait 5s for ping ack before closing
      "grpc.keepalive_permit_without_calls": 1,  // send keepalive even with no active calls
      "grpc.max_receive_message_length": 10 * 1024 * 1024, // 10MB max message
      "grpc.max_send_message_length": 10 * 1024 * 1024,
    }
  );
}

// Promisify the unary generate call
function generate(
  client: AiServiceClient,
  request: GenerateRequest,
  timeoutMs: number = 30000
): Promise<GenerateResponse> {
  return new Promise((resolve, reject) => {
    // Create metadata for the call (headers)
    const metadata = new grpc.Metadata();
    metadata.add("x-request-id", crypto.randomUUID());
    metadata.add("x-service", "api-gateway");

    // Deadline — absolute time by which the call must complete
    const deadline = new Date(Date.now() + timeoutMs);

    client.generate(
      request,
      metadata,
      { deadline },
      (error, response) => {
        if (error) {
          // Convert gRPC error to friendly error
          switch (error.code) {
            case grpc.status.NOT_FOUND:
              reject(new NotFoundError(error.message));
              break;
            case grpc.status.DEADLINE_EXCEEDED:
              reject(new Error(`AI request timed out after ${timeoutMs}ms`));
              break;
            case grpc.status.UNAVAILABLE:
              reject(new Error("AI service is unavailable"));
              break;
            case grpc.status.RESOURCE_EXHAUSTED:
              reject(new Error("AI service rate limit exceeded"));
              break;
            default:
              reject(new Error(`gRPC error: ${error.message} (code: ${error.code})`));
          }
        } else {
          resolve(response);
        }
      }
    );
  });
}

// Server streaming — for real-time token streaming
async function* generateStream(
  client: AiServiceClient,
  request: GenerateRequest,
  signal?: AbortSignal
): AsyncGenerator<GenerateStreamChunk> {
  const stream = client.generateStream(request);

  // Connect AbortSignal to cancel the stream
  signal?.addEventListener("abort", () => {
    stream.cancel();
  });

  try {
    for await (const chunk of stream) {
      yield chunk;
      if (chunk.isFinal) break;
    }
  } catch (error) {
    if (signal?.aborted) {
      return; // intentional cancellation
    }
    throw error;
  } finally {
    stream.destroy();
  }
}

// Usage example
async function runAiInference(jobData: JobData): Promise<void> {
  const client = createAiClient(process.env.AI_SERVICE_ADDRESS!);

  const request: GenerateRequest = {
    jobId: jobData.jobId,
    messages: jobData.messages,
    config: {
      model: jobData.model,
      temperature: jobData.temperature,
      maxTokens: jobData.maxTokens,
      topP: 1.0,
      frequencyPenalty: 0,
      presencePenalty: 0,
      stopSequences: [],
    },
    userId: jobData.userId,
    orgId: jobData.orgId,
    metadata: {},
  };

  // Option 1: Unary (get complete response at once)
  const response = await generate(client, request);
  console.log(`Generated ${response.totalTokens} tokens`);

  // Option 2: Streaming (get tokens as they're generated)
  const controller = new AbortController();
  let fullContent = "";

  for await (const chunk of generateStream(client, request, controller.signal)) {
    fullContent += chunk.delta;
    // Push chunk to client via SSE or WebSocket
    await pushChunkToClient(jobData.connectionId, chunk.delta);
    if (chunk.isFinal) {
      console.log(`Stream complete: ${chunk.totalTokens} tokens, reason: ${chunk.finishReason}`);
    }
  }
}
```

### gRPC Server (TypeScript — Implementing the Service)

```typescript
// server/ai-service.ts — if TypeScript IS the AI service

import * as grpc from "@grpc/grpc-js";
import type {
  ServerUnaryCall,
  ServerWritableStream,
  sendUnaryData,
} from "@grpc/grpc-js";
import type { AiServiceImplementation } from "../gen/ai_service.grpc-server";

// Implement the service
const aiServiceImpl: AiServiceImplementation = {
  // Unary handler
  async generate(
    call: ServerUnaryCall<GenerateRequest, GenerateResponse>,
    callback: sendUnaryData<GenerateResponse>
  ): Promise<void> {
    const { request } = call;

    // Read metadata from client
    const requestId = call.metadata.get("x-request-id")[0];
    const deadline = call.getDeadline();

    try {
      // Check deadline before starting expensive work
      if (deadline && Date.now() > (deadline as Date).getTime()) {
        callback({
          code: grpc.status.DEADLINE_EXCEEDED,
          message: "Deadline exceeded before processing started",
        });
        return;
      }

      const result = await runInference(request);

      callback(null, {
        jobId: request.jobId,
        content: result.content,
        promptTokens: result.promptTokens,
        completionTokens: result.completionTokens,
        totalTokens: result.totalTokens,
        finishReason: result.finishReason,
        model: request.config!.model,
        toolCalls: [],
      });

    } catch (error) {
      callback({
        code: grpc.status.INTERNAL,
        message: `Inference failed: ${(error as Error).message}`,
        details: JSON.stringify({ jobId: request.jobId }),
      });
    }
  },

  // Server streaming handler
  generateStream(
    call: ServerWritableStream<GenerateRequest, GenerateStreamChunk>
  ): void {
    const { request } = call;

    // Handle client cancellation
    call.on("cancelled", () => {
      console.log(`Stream ${request.jobId} cancelled by client`);
    });

    // Stream tokens asynchronously
    (async () => {
      try {
        for await (const token of streamInference(request)) {
          if (call.cancelled) break;

          const writable = call.write({
            jobId: request.jobId,
            delta: token.text,
            isFinal: token.isLast,
            totalTokens: token.isLast ? token.totalTokens : undefined,
            finishReason: token.isLast ? token.finishReason : undefined,
          });

          // If write returns false, buffer is full — wait for drain
          if (!writable) {
            await new Promise(resolve => call.once("drain", resolve));
          }
        }

        call.end(); // signal stream completion
      } catch (error) {
        call.destroy(error as Error);
      }
    })();
  },
};

// Start the server
function startGrpcServer(): void {
  const server = new grpc.Server({
    "grpc.max_receive_message_length": 10 * 1024 * 1024,
    "grpc.max_send_message_length": 10 * 1024 * 1024,
  });

  server.addService(AiServiceDefinition, aiServiceImpl);

  const port = process.env.GRPC_PORT ?? "50051";
  const credentials = process.env.NODE_ENV === "production"
    ? grpc.ServerCredentials.createSsl(null, [{
        private_key: Buffer.from(process.env.TLS_KEY!),
        cert_chain: Buffer.from(process.env.TLS_CERT!),
      }])
    : grpc.ServerCredentials.createInsecure();

  server.bindAsync(`0.0.0.0:${port}`, credentials, (error, port) => {
    if (error) {
      console.error("Failed to bind gRPC server:", error);
      process.exit(1);
    }
    server.start();
    console.log(`🚀 gRPC server listening on port ${port}`);
  });

  process.on("SIGTERM", () => {
    server.tryShutdown((error) => {
      if (error) console.error("Graceful shutdown failed:", error);
      process.exit(0);
    });
  });
}
```

---

## 13. gRPC Production Patterns

### Interceptors (Middleware for gRPC)

```typescript
// Client-side interceptor — runs for every outgoing call
function createLoggingInterceptor(): grpc.Interceptor {
  return (options, nextCall) => {
    const startTime = Date.now();
    const method = options.method_definition.path;

    return new grpc.InterceptingCall(nextCall(options), {
      start: (metadata, listener, next) => {
        console.log(`gRPC call started: ${method}`);
        next(metadata, {
          ...listener,
          onReceiveMessage: (message, next) => {
            console.log(`gRPC response received: ${method}`);
            next(message);
          },
          onReceiveStatus: (status, next) => {
            const duration = Date.now() - startTime;
            if (status.code !== grpc.status.OK) {
              console.error(`gRPC call failed: ${method} (${status.code}) in ${duration}ms`);
            } else {
              console.log(`gRPC call succeeded: ${method} in ${duration}ms`);
            }
            next(status);
          },
        });
      },
    });
  };
}

// Retry interceptor
function createRetryInterceptor(maxRetries: number = 3): grpc.Interceptor {
  return (options, nextCall) => {
    let retries = 0;
    const RETRYABLE_CODES = new Set([
      grpc.status.UNAVAILABLE,
      grpc.status.INTERNAL,
      grpc.status.RESOURCE_EXHAUSTED,
    ]);

    function invokeWithRetry(callback: Function) {
      const call = new grpc.InterceptingCall(nextCall(options));
      let savedMessage: unknown;
      let savedSend: Function;

      return new grpc.InterceptingCall(nextCall(options), {
        start: (metadata, listener, next) => {
          next(metadata, {
            ...listener,
            onReceiveStatus: (status, next) => {
              if (RETRYABLE_CODES.has(status.code) && retries < maxRetries) {
                retries++;
                const delay = Math.min(1000 * 2 ** retries, 30000); // exponential backoff
                setTimeout(() => invokeWithRetry(callback), delay);
              } else {
                next(status);
              }
            },
          });
        },
      });
    }

    return invokeWithRetry(() => {});
  };
}

// Apply interceptors to client
const client = new AiServiceClient(address, credentials, {
  interceptors: [
    createLoggingInterceptor(),
    createRetryInterceptor(3),
  ],
});
```

### Health Checks

```typescript
// Standard gRPC health check protocol
import { HealthImplementation } from "grpc-health-check";

const healthImpl = new HealthImplementation({
  "": HealthImplementation.ServingStatus.SERVING,  // overall health
  "ai.v1.AiService": HealthImplementation.ServingStatus.SERVING,
});

server.addService(healthImpl.service, healthImpl.implementation);

// Client-side health check
import { HealthClient } from "grpc-health-check";

const healthClient = new HealthClient(address, credentials);

async function checkHealth(): Promise<boolean> {
  return new Promise((resolve) => {
    healthClient.check({ service: "ai.v1.AiService" }, (err, response) => {
      resolve(!err && response?.status === 1); // 1 = SERVING
    });
  });
}
```

---

## 14. MinIO — Object Storage from Zero

### What is Object Storage?

Traditional storage paradigms:

```
Block Storage (like a hard drive):
  Data organized as fixed-size blocks
  OS formats it with a filesystem (ext4, NTFS)
  Fast random I/O — good for databases, VMs
  Examples: AWS EBS, local SSD

File Storage (filesystem):
  Hierarchical folder/file structure
  Good for shared access (network drives)
  Examples: NFS, AWS EFS, Samba

Object Storage:
  Flat namespace — objects stored in "buckets" (no folders, only prefixes)
  Each object: data + metadata + unique key
  Access via HTTP API (GET, PUT, DELETE)
  Designed for: massive scale, high durability, cheap cost
  NOT designed for: frequent overwrites, low-latency random access
  Examples: AWS S3, MinIO, Google Cloud Storage, Azure Blob Storage
```

### Why MinIO?

```
MinIO is an open-source, S3-compatible object storage server.

"S3-compatible" means:
  MinIO implements the same API as AWS S3
  Any code written for S3 works with MinIO unchanged
  Switch between S3 and MinIO by just changing the endpoint URL
  Great for: development (run MinIO locally), on-premise deployments,
             cost control (self-hosted vs AWS S3 pricing)

Use cases:
  ✅ Storing uploaded files (documents, images, videos, audio)
  ✅ AI model artifacts and datasets
  ✅ Generated PDFs, reports, exports
  ✅ Backups and archives
  ✅ Log file storage
  ✅ Static asset storage (though CDN is better for this)
  ✅ Storing chat attachments, agent tool outputs

Key properties:
  ✅ Highly durable (data replicated across disks/nodes)
  ✅ Practically unlimited storage
  ✅ Cheap per-GB cost (vs database storage)
  ✅ Efficient large file handling
  ✅ Built-in encryption, versioning, lifecycle policies
  ✅ Presigned URLs — grant temporary access without exposing credentials
```

---

## 15. MinIO Core Concepts

### Buckets and Objects

```
BUCKET:
  Top-level container (like a folder, but flat)
  Globally unique name within the MinIO instance
  Cannot nest buckets
  Have their own access policies, versioning, lifecycle rules

  Naming rules:
  - 3-63 characters
  - lowercase letters, numbers, hyphens
  - Must start with letter or number
  - Cannot look like an IP address

OBJECT:
  The actual file/data stored in a bucket
  Has: key (path-like name), data (bytes), metadata (headers)
  Max size: 5TB (5PB with multipart upload)
  Key is the "path" within the bucket: "org-123/user-456/uploads/document.pdf"
  Keys can contain "/" to simulate folder structure (they're just prefixes)

KEY NAMING CONVENTIONS:
  Good: "{orgId}/{userId}/{date}/{uuid}.{ext}"
  Example: "org-abc/user-123/2024/01/f47ac10b-document.pdf"

  Benefits of this structure:
  - List all files for an org: prefix="org-abc/"
  - List all files for a user: prefix="org-abc/user-123/"
  - Natural chronological order: prefix="org-abc/user-123/2024/01/"
  - Avoids hot partitions (MinIO shards by key prefix)

METADATA:
  System metadata: content-type, content-length, etag, last-modified
  User metadata: x-amz-meta-* headers (custom key-value pairs)
  Example: x-amz-meta-uploaded-by: "user-123"
           x-amz-meta-original-filename: "quarterly-report.pdf"
```

### Presigned URLs

```
A PRESIGNED URL is a temporary URL that grants access to a specific object
without requiring the requester to have credentials.

HOW IT WORKS:
  1. Your server (which has MinIO credentials) calls:
     minioClient.presignedGetObject("my-bucket", "path/to/file.pdf", expiry)
  
  2. MinIO returns a URL like:
     https://minio.example.com/my-bucket/path/to/file.pdf
       ?X-Amz-Algorithm=AWS4-HMAC-SHA256
       &X-Amz-Credential=myaccesskey/20240101/us-east-1/s3/aws4_request
       &X-Amz-Date=20240101T120000Z
       &X-Amz-Expires=3600
       &X-Amz-Signature=abc123...
  
  3. You return this URL to the client
  
  4. The client downloads directly from MinIO (NOT through your server)
     The URL expires after the specified time

WHY PRESIGNED URLS (vs proxying through server):
  ✅ Your server doesn't use bandwidth for file transfers
  ✅ Direct client ↔ MinIO connection — faster, lower latency
  ✅ MinIO can handle unlimited concurrent downloads without affecting your API
  ✅ Time-limited access — URLs expire automatically
  ✅ Scoped to specific objects — client can ONLY access that one object

PRESIGNED PUT (for uploads):
  Same idea but for uploading:
  1. Client requests "I want to upload file X"
  2. Server validates the request, returns a presigned PUT URL
  3. Client uploads directly to MinIO using PUT
  4. Client notifies server "upload complete"
  5. Server verifies object exists and records it in the database
```

---

## 16. MinIO in TypeScript — Complete Guide

### Installation and Client Setup

```bash
npm install minio
```

```typescript
// lib/minio.ts

import * as Minio from "minio";

// Create MinIO client
const minioClient = new Minio.Client({
  endPoint:  process.env.MINIO_ENDPOINT ?? "localhost",
  port:      parseInt(process.env.MINIO_PORT ?? "9000"),
  useSSL:    process.env.MINIO_USE_SSL === "true",
  accessKey: process.env.MINIO_ACCESS_KEY!,
  secretKey: process.env.MINIO_SECRET_KEY!,
  // For AWS S3 (same API):
  // endPoint: "s3.amazonaws.com"
  // port: 443
  // useSSL: true
  // region: "us-east-1"
});

// Bucket names as constants — prevent typos
export const BUCKETS = {
  UPLOADS: "uploads",           // user-uploaded files
  DOCUMENTS: "documents",       // processed documents
  EXPORTS: "exports",           // generated reports, PDFs
  MODELS: "ai-models",          // AI model artifacts
  AVATARS: "avatars",           // user profile pictures
} as const;

export type BucketName = typeof BUCKETS[keyof typeof BUCKETS];

// Initialize buckets on startup
export async function initializeBuckets(): Promise<void> {
  for (const bucket of Object.values(BUCKETS)) {
    const exists = await minioClient.bucketExists(bucket);
    if (!exists) {
      await minioClient.makeBucket(bucket, "us-east-1");
      console.log(`Created bucket: ${bucket}`);

      // Set bucket policy (public read for avatars, private for others)
      if (bucket === BUCKETS.AVATARS) {
        await setPublicReadPolicy(bucket);
      }
    }
  }
  console.log("✅ MinIO buckets initialized");
}

// Set bucket lifecycle — auto-delete old files
async function setExpirationPolicy(bucket: string, days: number): Promise<void> {
  await minioClient.setBucketLifecycle(bucket, {
    Rule: [{
      ID: "auto-expire",
      Status: "Enabled",
      Expiration: { Days: days },
      Filter: { Prefix: "" },  // applies to all objects
    }],
  });
}

export { minioClient };
```

### Upload and Download Operations

```typescript
// lib/storage.ts

import { minioClient, BUCKETS, BucketName } from "./minio";
import { Readable } from "stream";
import crypto from "crypto";

// Generate a safe, unique object key
function generateObjectKey(
  orgId: string,
  userId: string,
  originalFilename: string
): string {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const ext = originalFilename.split(".").pop()?.toLowerCase() ?? "bin";
  const uniqueId = crypto.randomUUID();

  return `${orgId}/${userId}/${year}/${month}/${uniqueId}.${ext}`;
  // Example: "org-abc/user-123/2024/01/f47ac10b-58e8-4c75-bc1c-cb2a1e395f01.pdf"
}

// Upload a file from a Buffer or Readable stream
interface UploadOptions {
  contentType: string;
  metadata?: Record<string, string>;
  tags?: Record<string, string>;
}

async function uploadFile(
  bucket: BucketName,
  objectKey: string,
  data: Buffer | Readable,
  size: number,
  options: UploadOptions
): Promise<{ etag: string; versionId: string | null }> {
  const metaData: Minio.ItemBucketMetadata = {
    "Content-Type": options.contentType,
    // Custom metadata — prefixed with x-amz-meta-
    ...Object.fromEntries(
      Object.entries(options.metadata ?? {}).map(([k, v]) => [`x-amz-meta-${k}`, v])
    ),
  };

  const result = await minioClient.putObject(
    bucket,
    objectKey,
    data,
    size,
    metaData
  );

  return { etag: result.etag, versionId: result.versionId };
}

// Upload a large file using multipart upload (automatically used by putObject for > 5MB)
async function uploadLargeFile(
  bucket: BucketName,
  objectKey: string,
  filePath: string,  // local filesystem path
  options: UploadOptions
): Promise<void> {
  await minioClient.fPutObject(
    bucket,
    objectKey,
    filePath,  // reads from local file
    { "Content-Type": options.contentType }
  );
}

// Download an object to memory
async function downloadToBuffer(
  bucket: BucketName,
  objectKey: string
): Promise<Buffer> {
  const stream = await minioClient.getObject(bucket, objectKey);
  const chunks: Buffer[] = [];

  return new Promise((resolve, reject) => {
    stream.on("data", (chunk: Buffer) => chunks.push(chunk));
    stream.on("end", () => resolve(Buffer.concat(chunks)));
    stream.on("error", reject);
  });
}

// Stream an object (for large files)
async function downloadAsStream(
  bucket: BucketName,
  objectKey: string
): Promise<Readable> {
  return minioClient.getObject(bucket, objectKey);
}

// Download to a local file
async function downloadToFile(
  bucket: BucketName,
  objectKey: string,
  localPath: string
): Promise<void> {
  await minioClient.fGetObject(bucket, objectKey, localPath);
}

// Get object metadata (without downloading)
async function getObjectInfo(
  bucket: BucketName,
  objectKey: string
): Promise<Minio.BucketItemStat> {
  return minioClient.statObject(bucket, objectKey);
}

// Check if object exists
async function objectExists(bucket: BucketName, objectKey: string): Promise<boolean> {
  try {
    await minioClient.statObject(bucket, objectKey);
    return true;
  } catch (error) {
    if ((error as { code?: string }).code === "NotFound") return false;
    throw error;
  }
}

// Delete an object
async function deleteObject(bucket: BucketName, objectKey: string): Promise<void> {
  await minioClient.removeObject(bucket, objectKey);
}

// Delete multiple objects
async function deleteObjects(
  bucket: BucketName,
  objectKeys: string[]
): Promise<void> {
  await minioClient.removeObjects(
    bucket,
    objectKeys.map(name => ({ name }))
  );
}

// Copy an object within MinIO (no download/upload needed)
async function copyObject(
  sourceBucket: BucketName,
  sourceKey: string,
  destBucket: BucketName,
  destKey: string
): Promise<void> {
  const conds = new Minio.CopyConditions();
  await minioClient.copyObject(destBucket, destKey, `/${sourceBucket}/${sourceKey}`, conds);
}

// List objects with a prefix
async function listObjects(
  bucket: BucketName,
  prefix: string,
  recursive: boolean = false
): Promise<Minio.BucketItem[]> {
  const items: Minio.BucketItem[] = [];

  return new Promise((resolve, reject) => {
    const stream = minioClient.listObjects(bucket, prefix, recursive);
    stream.on("data", (item) => items.push(item));
    stream.on("end", () => resolve(items));
    stream.on("error", reject);
  });
}
```

### Presigned URLs — Complete Implementation

```typescript
// lib/presigned.ts

const ALLOWED_MIME_TYPES = new Set([
  "image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml",
  "application/pdf",
  "text/plain", "text/csv", "text/markdown",
  "application/json",
  "video/mp4", "video/webm",
  "audio/mpeg", "audio/wav", "audio/ogg",
  "application/zip",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]);

const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB

// Get a presigned URL for downloading an object
async function getDownloadUrl(
  bucket: BucketName,
  objectKey: string,
  expirySeconds: number = 3600, // 1 hour default
  filename?: string             // force download with specific filename
): Promise<string> {
  const reqParams: Record<string, string> = {};

  if (filename) {
    // Force browser to download with the given filename
    reqParams["response-content-disposition"] =
      `attachment; filename="${encodeURIComponent(filename)}"`;
  }

  return minioClient.presignedGetObject(bucket, objectKey, expirySeconds, reqParams);
}

// Get a presigned URL for uploading (PUT)
async function getUploadUrl(
  bucket: BucketName,
  objectKey: string,
  expirySeconds: number = 300 // 5 minutes — uploads should be fast
): Promise<string> {
  return minioClient.presignedPutObject(bucket, objectKey, expirySeconds);
}

// Get a presigned POST URL (more secure than PUT — limits file size, type)
async function getUploadPost(
  bucket: BucketName,
  objectKey: string,
  options: {
    contentType: string;
    maxSizeBytes?: number;
    expirySeconds?: number;
  }
): Promise<{ url: string; fields: Record<string, string> }> {
  const policy = new Minio.PostPolicy();
  policy.setBucket(bucket);
  policy.setKey(objectKey);

  // Policy conditions
  const expiry = new Date(Date.now() + (options.expirySeconds ?? 300) * 1000);
  policy.setExpires(expiry);

  // Content type must exactly match
  policy.setContentType(options.contentType);

  // File size range
  const maxSize = options.maxSizeBytes ?? MAX_FILE_SIZE;
  policy.setContentLengthRange(1, maxSize);

  const { postURL, formData } = await minioClient.presignedPostPolicy(policy);
  return { url: postURL, fields: formData };
}

// API: Request upload URL (validates, generates presigned URL, records in DB)
export async function requestUploadUrl(
  userId: string,
  orgId: string,
  filename: string,
  contentType: string,
  sizeBytes: number
): Promise<{ uploadUrl: string; objectKey: string; expiresAt: Date }> {
  // Validate file type
  if (!ALLOWED_MIME_TYPES.has(contentType)) {
    throw new ValidationError({ contentType: [`File type '${contentType}' is not allowed`] });
  }

  // Validate file size
  if (sizeBytes > MAX_FILE_SIZE) {
    throw new ValidationError({ sizeBytes: [`File size exceeds limit of ${MAX_FILE_SIZE / 1024 / 1024}MB`] });
  }

  // Generate unique key with org/user namespace
  const objectKey = generateObjectKey(orgId, userId, filename);

  // Generate presigned PUT URL (5-minute expiry)
  const expirySeconds = 300;
  const uploadUrl = await getUploadUrl(BUCKETS.UPLOADS, objectKey, expirySeconds);

  const expiresAt = new Date(Date.now() + expirySeconds * 1000);

  // Record pending upload in database
  await db.insert(pendingUploads).values({
    userId, orgId, objectKey, contentType,
    sizeBytes, expiresAt, filename,
  });

  return { uploadUrl, objectKey, expiresAt };
}

// API: Confirm upload after client has finished uploading
export async function confirmUpload(
  userId: string,
  orgId: string,
  objectKey: string
): Promise<FileRecord> {
  // Verify the object actually exists in MinIO
  let stat: Minio.BucketItemStat;
  try {
    stat = await minioClient.statObject(BUCKETS.UPLOADS, objectKey);
  } catch {
    throw new NotFoundError("Upload not found in storage");
  }

  // Verify the pending upload belongs to this user
  const pending = await db.query.pendingUploads.findFirst({
    where: and(
      eq(pendingUploads.objectKey, objectKey),
      eq(pendingUploads.userId, userId),
      isNull(pendingUploads.confirmedAt),
      gt(pendingUploads.expiresAt, new Date())
    ),
  });

  if (!pending) {
    throw new NotFoundError("Upload request not found or expired");
  }

  return await db.transaction(async (tx) => {
    // Create permanent file record
    const [file] = await tx.insert(files).values({
      orgId, userId,
      objectKey,
      bucket: BUCKETS.UPLOADS,
      contentType: stat.metaData["content-type"] ?? pending.contentType,
      sizeBytes: stat.size,
      filename: pending.filename,
      etag: stat.etag,
    }).returning();

    // Mark pending upload as confirmed
    await tx.update(pendingUploads)
      .set({ confirmedAt: new Date() })
      .where(eq(pendingUploads.id, pending.id));

    return file;
  });
}

// API: Get download URL for a file
export async function getFileDownloadUrl(
  userId: string,
  orgId: string,
  fileId: string
): Promise<string> {
  const file = await db.query.files.findFirst({
    where: and(eq(files.id, fileId), eq(files.orgId, orgId)),
  });

  if (!file) throw new NotFoundError("File", fileId);

  return getDownloadUrl(
    file.bucket as BucketName,
    file.objectKey,
    3600,     // 1 hour expiry
    file.filename
  );
}
```

---

## 17. MinIO Production Patterns

### Bucket Policies & Access Control

```typescript
// Set bucket policy for public access (for avatars)
async function setPublicReadPolicy(bucket: string): Promise<void> {
  const policy = {
    Version: "2012-10-17",
    Statement: [{
      Sid: "PublicRead",
      Effect: "Allow",
      Principal: { AWS: ["*"] },
      Action: ["s3:GetObject"],
      Resource: [`arn:aws:s3:::${bucket}/*`],
    }],
  };
  await minioClient.setBucketPolicy(bucket, JSON.stringify(policy));
}

// Set private policy (deny all public access)
async function setPrivatePolicy(bucket: string): Promise<void> {
  await minioClient.setBucketPolicy(bucket, "");  // empty = private
}
```

### MinIO Notifications → RabbitMQ

MinIO can automatically publish events to RabbitMQ when objects are created or deleted:

```typescript
// Configure MinIO to send notifications to RabbitMQ
// This is configured in MinIO's config, not code (usually environment variables):
// MINIO_NOTIFY_AMQP_ENABLE=on
// MINIO_NOTIFY_AMQP_URL=amqp://guest:guest@rabbitmq:5672
// MINIO_NOTIFY_AMQP_EXCHANGE=minio.events
// MINIO_NOTIFY_AMQP_EXCHANGE_TYPE=direct
// MINIO_NOTIFY_AMQP_ROUTING_KEY=minio
// MINIO_NOTIFY_AMQP_DURABLE=on

// Alternatively, configure via the MinIO admin client:
async function configureMinioNotifications(): Promise<void> {
  const notification = new Minio.NotificationConfig();

  // Create AMQP queue config (points to RabbitMQ)
  const queue = new Minio.QueueConfig(
    "arn:minio:sqs::rabbitmq:amqp"  // ARN matching your MinIO AMQP config
  );

  // Which file types to notify about
  queue.addFilterSuffix(".pdf");
  queue.addFilterSuffix(".docx");
  queue.addFilterSuffix(".txt");
  queue.addFilterSuffix(".csv");
  queue.addFilterPrefix(`${process.env.ORG_ID}/`);  // only for specific org

  // Which events to notify about
  queue.addEvent(Minio.ObjectCreatedPut);         // PUT upload
  queue.addEvent(Minio.ObjectCreatedCompleteMultipartUpload); // multipart
  queue.addEvent(Minio.ObjectRemovedDelete);       // deletion

  notification.add(queue);
  await minioClient.setBucketNotification(BUCKETS.UPLOADS, notification);
}

// Consumer that processes MinIO notifications from RabbitMQ
interface MinioNotification {
  EventName: string; // "s3:ObjectCreated:Put"
  Key: string;       // "org-abc/user-123/2024/01/file.pdf"
  Records: Array<{
    s3: {
      bucket: { name: string };
      object: {
        key: string;
        size: number;
        eTag: string;
        contentType: string;
      };
    };
    eventTime: string;
    eventName: string;
  }>;
}

async function processMinioNotification(notification: MinioNotification): Promise<void> {
  for (const record of notification.Records) {
    const { bucket, object } = record.s3;
    const objectKey = decodeURIComponent(object.key.replace(/\+/g, " "));

    console.log(`MinIO event: ${record.eventName} for ${bucket.name}/${objectKey}`);

    if (record.eventName.startsWith("s3:ObjectCreated")) {
      // File was uploaded — process it
      await handleFileUploaded({
        bucket: bucket.name,
        objectKey,
        sizeBytes: object.size,
        contentType: object.contentType,
        etag: object.eTag,
      });
    } else if (record.eventName.startsWith("s3:ObjectRemoved")) {
      // File was deleted — update database
      await handleFileDeleted({ bucket: bucket.name, objectKey });
    }
  }
}
```

### Virus Scanning & File Processing Pipeline

```typescript
// After upload → scan for viruses → process (extract text, generate thumbnails) → mark ready

async function processUploadedFile(fileId: string, objectKey: string): Promise<void> {
  await db.update(files).set({ status: "processing" }).where(eq(files.id, fileId));

  try {
    // 1. Download file for scanning
    const fileBuffer = await downloadToBuffer(BUCKETS.UPLOADS, objectKey);

    // 2. Virus scan (using ClamAV or VirusTotal API)
    const scanResult = await scanForViruses(fileBuffer);
    if (scanResult.infected) {
      // Delete infected file
      await minioClient.removeObject(BUCKETS.UPLOADS, objectKey);
      await db.update(files).set({ status: "rejected", rejectionReason: "malware_detected" })
        .where(eq(files.id, fileId));
      return;
    }

    // 3. Process based on file type
    const file = await db.query.files.findFirst({ where: eq(files.id, fileId) });
    if (!file) return;

    if (file.contentType === "application/pdf") {
      // Extract text for full-text search
      const text = await extractPdfText(fileBuffer);
      const thumbnailBuffer = await generatePdfThumbnail(fileBuffer);

      // Store thumbnail
      const thumbKey = objectKey.replace(/\.pdf$/, "_thumb.jpg");
      await uploadFile(BUCKETS.DOCUMENTS, thumbKey, thumbnailBuffer, thumbnailBuffer.length, {
        contentType: "image/jpeg",
      });

      await db.update(files).set({
        status: "ready",
        extractedText: text,
        thumbnailKey: thumbKey,
        pageCount: text.pageCount,
      }).where(eq(files.id, fileId));

    } else if (file.contentType.startsWith("image/")) {
      // Generate thumbnails at multiple sizes
      const thumbSizes = [200, 400, 800];
      for (const size of thumbSizes) {
        const thumb = await resizeImage(fileBuffer, size);
        const thumbKey = objectKey.replace(/\.[^.]+$/, `_${size}w.webp`);
        await uploadFile(BUCKETS.DOCUMENTS, thumbKey, thumb, thumb.length, {
          contentType: "image/webp",
        });
      }

      await db.update(files).set({ status: "ready" }).where(eq(files.id, fileId));
    }

  } catch (error) {
    await db.update(files).set({ status: "error", processingError: (error as Error).message })
      .where(eq(files.id, fileId));
    throw error;
  }
}
```

---

## 18. System Design — How They Fit Together

### The Complete Agentic Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           User's Browser                                 │
│                    React + Next.js (Client Components)                   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ HTTPS
                               │ oRPC over HTTP/2
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Next.js Server                                    │
│              (Server Components, Server Actions, Route Handlers)         │
│                                                                          │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────────────┐ │
│  │  oRPC Router    │    │  Auth Middleware │    │  Rate Limiting       │ │
│  │  (type-safe API)│    │  (JWT/Session)  │    │  (Redis + sliding    │ │
│  └────────┬────────┘    └─────────────────┘    │   window)            │ │
│           │                                    └──────────────────────┘ │
│           │ Drizzle ORM                                                  │
│           ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      PostgreSQL                                   │    │
│  │  organizations, users, agents, conversations, messages           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ publish
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         RabbitMQ Broker                                  │
│                                                                          │
│  Exchanges (topic):                                                      │
│    "app.events"                                                          │
│                                                                          │
│  Queues (durable):                                                       │
│    [ai.inference.jobs]    → AI Worker (prefetch=1, heavy jobs)           │
│    [notifications.email]  → Email Worker (prefetch=50, fast)             │
│    [notifications.push]   → Push Worker (prefetch=100, very fast)        │
│    [files.processing]     → File Worker (prefetch=5, medium)             │
│    [analytics.events]     → Analytics Worker (prefetch=200, fast)        │
│    [dlq]                  → Dead Letter Queue (manual review)            │
└──┬──────────────────────────────────────────────────────────────────────┘
   │ subscribe
   ▼
┌──────────────────────────────────────────────────────────┐
│                    Worker Services                        │
│                                                          │
│  AI Worker:                                              │
│    1. Receives job from RabbitMQ                         │
│    2. Calls AI Service via gRPC (streaming)              │
│    3. Pushes chunks to Redis Pub/Sub                     │
│    4. API SSE endpoint reads from Redis, sends to client │
│    5. Saves complete response to PostgreSQL              │
│    6. Publishes "ai.inference.complete" event            │
│                                                          │
│  File Worker:                                            │
│    1. Receives file.uploaded from MinIO notification     │
│    2. Downloads from MinIO                               │
│    3. Virus scan, extract text, generate thumbnails      │
│    4. Stores processed artifacts back in MinIO           │
│    5. Updates PostgreSQL with file metadata              │
└──────────────────┬───────────────────────────────────────┘
                   │ gRPC (HTTP/2 + Protobuf)
                   ▼
┌──────────────────────────────────────────────────────────┐
│                    AI Service (Python)                    │
│                                                          │
│  gRPC Server (port 50051)                                │
│    - AiService.Generate (unary)                          │
│    - AiService.GenerateStream (server streaming)         │
│                                                          │
│  Calls: OpenAI API, Anthropic API, or local LLM         │
│  Streams: token by token back to caller                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       MinIO                              │
│                                                          │
│  Buckets:                                                │
│    uploads/ — raw user uploads (org/user/date/uuid.ext)  │
│    documents/ — processed files (thumbnails, text)       │
│    exports/ — generated reports, PDFs                    │
│    avatars/ — profile pictures (public read)             │
│                                                          │
│  Events → RabbitMQ:                                      │
│    ObjectCreated → file.uploaded queue                   │
│    ObjectDeleted → file.deleted queue                    │
│                                                          │
│  Client access:                                          │
│    Upload: API generates presigned PUT → client uploads  │
│    Download: API generates presigned GET → client fetches│
└──────────────────────────────────────────────────────────┘
```

### Complete Data Flow: AI Chat with File Attachment

```
Step-by-step flow for "user sends a PDF and asks the agent to summarize it":

1. [Browser] User selects PDF file
   → React component calls: orpc.files.requestUpload({ filename, contentType, sizeBytes })

2. [Next.js API] Validates request, generates presigned PUT URL
   → Returns: { uploadUrl, objectKey, expiresAt }
   → Records pending upload in PostgreSQL

3. [Browser] PUT file directly to MinIO using presigned URL
   → fetch(uploadUrl, { method: "PUT", body: file })
   → On success: calls orpc.files.confirmUpload({ objectKey })

4. [Next.js API] confirmUpload handler:
   → Verifies object exists in MinIO (statObject)
   → Creates file record in PostgreSQL
   → Publishes "file.uploaded" to RabbitMQ

5. [File Worker] Receives "file.uploaded":
   → Downloads PDF from MinIO
   → Extracts text using PDF parser
   → Stores extracted text in PostgreSQL
   → Updates file status to "ready"
   → Publishes "file.processed" event

6. [Browser] User types "Summarize this document" and hits Send
   → orpc.chat.sendMessage({ conversationId, content, attachmentIds: [fileId] })

7. [Next.js API] sendMessage handler:
   → Saves user message to PostgreSQL
   → Fetches extracted text from file record
   → Builds messages array with file content in system context
   → Publishes "ai.inference.request" to RabbitMQ
   → Returns { jobId } immediately (no waiting!)

8. [Browser] Subscribes to SSE stream: /api/stream/${jobId}
   → SSE endpoint polls Redis Pub/Sub for chunks

9. [AI Worker] Receives "ai.inference.request":
   → Calls Python AI Service via gRPC (GenerateStream)
   → For each chunk received from gRPC:
     a. Publishes chunk to Redis Pub/Sub: PUBLISH job:${jobId} ${chunk}
     b. [SSE endpoint reads this and sends to browser]

10. [Browser] Receives SSE chunks, appends to message in UI
    (user sees the summary appearing word by word)

11. [AI Worker] Stream complete:
    → Saves full assistant message to PostgreSQL
    → Acks the RabbitMQ message (success)
    → Publishes "ai.inference.complete" (for analytics, billing)

12. [Analytics Worker] Receives "ai.inference.complete":
    → Updates usage statistics in PostgreSQL
    → Records billing event
    → No need to respond — fire and forget
```

### Technology Choice Matrix

| Scenario | Technology | Reason |
|----------|-----------|--------|
| User login API | oRPC (sync HTTP) | Need immediate response with session token |
| Send AI chat message | RabbitMQ (async) | Work is slow (LLM inference), don't block user |
| Stream AI tokens to browser | SSE over HTTP | Browser-compatible real-time data push |
| TypeScript → Python AI service | gRPC | Binary performance, type-safe, streaming support |
| Upload 100MB PDF | Presigned PUT to MinIO | Server doesn't need to handle file bytes |
| Download processed report | Presigned GET from MinIO | Direct client ↔ MinIO, no server bandwidth |
| Alert all services of new user | RabbitMQ fanout | One event → many independent consumers |
| Failed message retry | RabbitMQ DLQ | Retry with backoff, don't lose failed work |
| Large dataset query from DB | Direct Drizzle ORM | No async needed, just query |
| Real-time dashboard metrics | WebSocket or SSE | Push updates when data changes |

---

## Quick Reference: Technology Summary

### RabbitMQ Quick Reference
```
Exchange types: direct (exact key), fanout (all queues), topic (* one word, # many words)
Message lifecycle: publish → exchange → binding → queue → consumer → ack/nack
Reliability: durable queues + persistent messages + publisher confirms + manual acks
Patterns: work queue, pub/sub, topic routing, RPC, delayed retry, DLQ
Key settings: prefetch(1) for fair dispatch, x-dead-letter-exchange for DLQ
```

### gRPC Quick Reference
```
Schema: Protocol Buffers (.proto files) — language-neutral, binary, versioned
Service types: unary, server-streaming, client-streaming, bidirectional
Transport: HTTP/2 (multiplexing, header compression, streaming)
vs REST: binary (faster), streaming (native), typed (codegen), not browser-native
Metadata: grpc.Metadata (like HTTP headers)
Error codes: OK, NOT_FOUND, UNAUTHORIZED, DEADLINE_EXCEEDED, UNAVAILABLE, etc.
```

### MinIO Quick Reference
```
S3-compatible: same API as AWS S3, just different endpoint
Core: buckets (containers) + objects (files) + keys (paths)
Access patterns: presigned URLs (temporary, direct) vs proxy (through server)
Key naming: orgId/userId/year/month/uuid.ext (namespace + chronological)
Events: configure bucket notifications → publish to RabbitMQ automatically
Security: IAM-style policies, versioning, server-side encryption
```

---

*This guide covers asynchronous system design, RabbitMQ in full depth, gRPC + Protobuf, and MinIO object storage with complete TypeScript implementations. The final file contains all interview questions for every topic covered across all six files.*
