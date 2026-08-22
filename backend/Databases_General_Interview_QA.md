# Databases — Interview Questions & Answers
> 120 questions. SQL, NoSQL, indexes, transactions, query optimization, Redis, MongoDB.

---

## EASY (Q1–Q30)

**Q1. What is ACID?**
```
A — Atomicity: transaction is all-or-nothing
    If any step fails, ALL changes are rolled back

C — Consistency: transaction brings DB from one valid state to another
    All constraints (FK, unique, check) must hold before and after

I — Isolation: concurrent transactions don't interfere with each other
    Different isolation levels trade performance vs correctness

D — Durability: committed transaction persists even after crash
    Achieved via WAL (Write-Ahead Log) + fsync

Example: bank transfer $100 from Alice to Bob
  BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 'alice'; -- A: both must succeed
    UPDATE accounts SET balance = balance + 100 WHERE id = 'bob';
  COMMIT; -- D: persisted
  -- C: total money unchanged
  -- I: another transaction can't see partial transfer
```

**Q2. What are the SQL JOIN types?**
```sql
-- INNER JOIN: rows with matches in BOTH tables
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: all rows from LEFT + matching from RIGHT (NULL if no match)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;  -- includes users with 0 orders

-- RIGHT JOIN: all rows from RIGHT + matching from LEFT (rarely used, just swap tables)

-- FULL OUTER JOIN: all rows from both, NULL where no match
SELECT * FROM table_a
FULL OUTER JOIN table_b ON table_a.id = table_b.id;

-- CROSS JOIN: cartesian product (every row × every row)
SELECT colors.name, sizes.name FROM colors CROSS JOIN sizes;  -- all color-size combos

-- SELF JOIN: join table with itself
SELECT e.name, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

**Q3. What are database indexes?**
```sql
-- Index: data structure (B-Tree by default) for fast lookups
-- Without index: O(n) full table scan
-- With index: O(log n) B-Tree traversal

-- Create indexes:
CREATE INDEX idx_users_email ON users(email);               -- single column
CREATE INDEX idx_users_dept_name ON users(department, name); -- composite
CREATE UNIQUE INDEX idx_users_email_unique ON users(email); -- unique constraint
CREATE INDEX idx_orders_created ON orders(created_at DESC); -- with direction
CREATE INDEX idx_orders_active ON orders(user_id) WHERE status = 'active'; -- partial

-- Composite index column order matters!
-- index ON (a, b, c) can be used for queries filtering on: a, (a,b), (a,b,c)
-- but NOT for: b only, c only, (b,c) — must start from leftmost column!

-- Explain query plan:
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';
-- Look for: Seq Scan (bad for large tables), Index Scan (good), Index Only Scan (best)

-- Index types:
-- B-Tree (default): equality, range queries, ORDER BY, <, >, LIKE 'prefix%'
-- Hash: only equality queries (=), slightly faster than B-Tree for equality
-- GiST/GIN: full-text search, arrays, JSON, geometric types
-- BRIN: very large tables sorted by column (e.g., time-series)

-- When NOT to index:
-- Small tables (< 1000 rows)
-- Columns with low cardinality (e.g., boolean — only 2 values)
-- Heavily written tables (indexes slow down writes)
-- Rarely queried columns
```

**Q4. What are the SQL aggregate functions?**
```sql
SELECT
  COUNT(*)                          AS total_rows,
  COUNT(DISTINCT user_id)           AS unique_users,
  SUM(amount)                       AS total_amount,
  AVG(amount)                       AS avg_amount,
  MIN(created_at)                   AS first_order,
  MAX(created_at)                   AS last_order,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_amount,
  STDDEV(amount)                    AS std_dev,
  STRING_AGG(tag, ', ')             AS all_tags
FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY department
HAVING COUNT(*) > 10
ORDER BY total_amount DESC
LIMIT 5;
```

**Q5. What are window functions?**
```sql
-- Window functions: aggregate ACROSS rows without collapsing them

SELECT
  name, department, salary,
  -- Rank within department by salary:
  RANK() OVER (PARTITION BY department ORDER BY salary DESC)    AS rank,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,

  -- Running total:
  SUM(salary) OVER (PARTITION BY department ORDER BY salary)    AS running_total,

  -- Lag/Lead:
  LAG(salary, 1) OVER (PARTITION BY department ORDER BY salary) AS prev_salary,
  LEAD(salary, 1) OVER (PARTITION BY department ORDER BY salary) AS next_salary,

  -- Percent of total:
  ROUND(salary * 100.0 / SUM(salary) OVER (PARTITION BY department), 2) AS pct_of_dept,

  -- Nth value:
  FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS top_salary,
  NTH_VALUE(salary, 3) OVER (PARTITION BY department ORDER BY salary DESC) AS 3rd_salary

FROM employees;

-- Top N per group (e.g., top 3 salaries per department):
WITH ranked AS (
  SELECT *, RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS r
  FROM employees
)
SELECT * FROM ranked WHERE r <= 3;
```

**Q6. What are CTEs (Common Table Expressions)?**
```sql
-- CTE: named subquery, improves readability
-- Materialized or not depending on optimizer

-- Basic CTE:
WITH active_users AS (
  SELECT * FROM users WHERE active = true AND last_login > NOW() - INTERVAL '30 days'
),
user_revenue AS (
  SELECT user_id, SUM(amount) as total
  FROM orders
  WHERE status = 'completed'
  GROUP BY user_id
)
SELECT u.name, u.email, COALESCE(r.total, 0) as revenue
FROM active_users u
LEFT JOIN user_revenue r ON u.id = r.user_id
ORDER BY revenue DESC;

-- Recursive CTE (tree traversal, org charts, BOM):
WITH RECURSIVE org_chart AS (
  -- Base case: top-level managers
  SELECT id, name, manager_id, 0 AS level
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive case: employees reporting to someone in the CTE
  SELECT e.id, e.name, e.manager_id, oc.level + 1
  FROM employees e
  INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT REPEAT('  ', level) || name AS hierarchy
FROM org_chart
ORDER BY level, name;
```

**Q7. What are transactions and isolation levels?**
```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- or ROLLBACK;

-- ISOLATION LEVELS and what they prevent:
-- READ UNCOMMITTED: allows dirty reads (see uncommitted changes) — never use
-- READ COMMITTED (default PostgreSQL): prevents dirty reads
-- REPEATABLE READ (default MySQL): prevents dirty + non-repeatable reads
-- SERIALIZABLE: prevents dirty + non-repeatable + phantom reads

-- Phenomena:
-- Dirty Read: reading uncommitted data from another transaction
-- Non-repeatable Read: same row gives different results in same transaction
-- Phantom Read: same range query gives different row COUNT in same transaction

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
  SELECT balance FROM accounts WHERE id = 1; -- 1000
  -- another transaction changes and commits the balance
  SELECT balance FROM accounts WHERE id = 1; -- still 1000 with REPEATABLE READ
COMMIT;

-- SAVEPOINTS — partial rollback:
BEGIN;
  UPDATE users SET name = 'Alice' WHERE id = 1;
  SAVEPOINT after_update;
  DELETE FROM users WHERE id = 2; -- might fail
ROLLBACK TO SAVEPOINT after_update; -- only undoes the DELETE
COMMIT; -- commits the UPDATE
```

**Q8. What is normalization?**
```
1NF (First Normal Form):
  - Each column has atomic (indivisible) values
  - No repeating groups
  - BAD: tags column = "java,python,javascript" → one row per tag

2NF (Second Normal Form):
  - 1NF + no partial dependencies (all non-key attributes depend on WHOLE primary key)
  - Only applies when composite primary key
  - BAD: order_id+product_id → product_name (product_name depends only on product_id)
  - FIX: move product_name to products table

3NF (Third Normal Form):
  - 2NF + no transitive dependencies
  - BAD: order → customer_id → customer_zip (zip depends on customer, not order)
  - FIX: separate customers table

BCNF (Boyce-Codd Normal Form):
  - Stricter version of 3NF (handles some edge cases)

4NF: no multi-valued dependencies
5NF: no join dependencies

Denormalization: intentionally violate normalization for query performance
  - Pre-compute aggregates (user.order_count)
  - Duplicate data to avoid joins (order.customer_name)
  - Common in read-heavy systems with clear write-read ratio
```

**Q9. What are stored procedures, triggers, and views?**
```sql
-- STORED PROCEDURE (logic in the DB):
CREATE OR REPLACE PROCEDURE process_payment(
  p_order_id BIGINT,
  p_amount DECIMAL(10,2)
)
LANGUAGE plpgsql AS $$
DECLARE
  v_balance DECIMAL(10,2);
BEGIN
  SELECT balance INTO v_balance FROM accounts WHERE order_id = p_order_id FOR UPDATE;
  IF v_balance < p_amount THEN
    RAISE EXCEPTION 'Insufficient funds: % < %', v_balance, p_amount;
  END IF;
  UPDATE accounts SET balance = balance - p_amount WHERE order_id = p_order_id;
  INSERT INTO payments(order_id, amount, created_at) VALUES (p_order_id, p_amount, NOW());
  COMMIT;
END;
$$;
CALL process_payment(12345, 99.99);

-- VIEW (virtual table — saved query):
CREATE VIEW active_user_summary AS
  SELECT u.id, u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
  FROM users u LEFT JOIN orders o ON u.id = o.user_id
  WHERE u.active = true
  GROUP BY u.id, u.name;
-- Query it like a table:
SELECT * FROM active_user_summary WHERE total_spent > 1000;

-- MATERIALIZED VIEW (cached result — must refresh):
CREATE MATERIALIZED VIEW monthly_revenue AS
  SELECT DATE_TRUNC('month', created_at) as month, SUM(amount) as revenue
  FROM orders GROUP BY 1;
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue; -- refresh without blocking reads

-- TRIGGER (auto-execute on table changes):
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_modified_at();
```

**Q10. What is query optimization?**
```sql
-- EXECUTION PLAN:
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT u.name, COUNT(o.id)
FROM users u JOIN orders o ON u.id = o.user_id
WHERE o.created_at > NOW() - INTERVAL '7 days'
GROUP BY u.id, u.name;

-- Key terms in EXPLAIN output:
-- Seq Scan: full table scan — add index if large table
-- Index Scan: using B-tree index
-- Index Only Scan: query satisfied entirely from index (fastest!)
-- Hash Join: build hash table from smaller table, probe with larger
-- Nested Loop: for small result sets, uses index on inner table
-- Sort: needs sort — can be eliminated with matching index

-- Optimization techniques:
-- 1. Use covering index (includes all columns needed by query):
CREATE INDEX idx_orders_user_date_amount ON orders(user_id, created_at, amount);
-- Query SELECT amount WHERE user_id=X AND created_at>Y → Index Only Scan!

-- 2. Avoid functions on indexed columns:
-- BAD:  WHERE LOWER(email) = 'alice@example.com' -- can't use index on email
-- GOOD: CREATE INDEX idx_lower_email ON users(LOWER(email));
-- OR:   store email already lowercased

-- 3. Avoid SELECT * — only fetch needed columns

-- 4. Use LIMIT to stop early

-- 5. Partition large tables:
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
-- Queries with date range skip irrelevant partitions (partition pruning)

-- 6. Statistics and ANALYZE:
ANALYZE orders; -- update statistics used by query planner
ALTER TABLE orders ALTER COLUMN user_id SET STATISTICS 500; -- more histogram buckets
```

---

## MEDIUM (Q31–Q70)

**Q31. Explain B-Tree index internals.**
```
B-Tree (Balanced Tree):
- Self-balancing tree structure
- Each node has N-1 keys and N children (N = order)
- All leaves at same depth
- Leaf nodes are linked (for range scans)

Structure for index ON users(age):
  Root: [25 | 50 | 75]
  /           |          \         \
[10,15,20] [25,30,40] [50,55,65] [75,80,95]
  ↓            ↓          ↓          ↓
 rows         rows       rows      rows

Operations:
- Point lookup: O(log N) — traverse tree top to bottom
- Range scan: O(log N + k) — find start, then scan linked leaves
- Insert: O(log N) — find position, split nodes if needed
- Delete: O(log N) — find and remove, rebalance if needed

Properties:
- Height = O(log N) where N = number of entries
- For 1M rows, height ≈ 3-4 levels (branching factor ~100)
- All operations guaranteed O(log N)

B+ Tree (what databases actually use):
- Data only in leaf nodes (internal nodes = index only)
- Leaf nodes linked → fast range scans
- Higher branching factor → shorter tree → fewer I/Os
```

**Q32. What is MVCC (Multi-Version Concurrency Control)?**
```sql
-- MVCC allows concurrent reads and writes without locking
-- Each row has: xmin (created by transaction), xmax (deleted by transaction)
-- Readers see a "snapshot" of the DB as of their transaction start
-- Readers never block writers, writers never block readers

-- PostgreSQL MVCC:
-- Each transaction has a transaction ID (txid)
-- Row versions stored with xmin, xmax
-- Visible if: xmin committed before snapshot AND (xmax is NULL OR not yet committed)

-- See transaction IDs:
SELECT txid_current();

-- Vacuum: MVCC creates dead tuples (old versions) — VACUUM reclaims space
VACUUM ANALYZE users;       -- reclaim dead tuples, update stats
VACUUM FULL users;          -- exclusive lock, reclaim more space (avoid in prod)

-- autovacuum: PostgreSQL auto-runs this in background
-- Symptoms of insufficient vacuuming: bloat, slow queries, txid wraparound

-- Transaction ID wraparound (critical!):
-- txid is 32-bit → wraps after ~2B transactions
-- PostgreSQL freezes old transactions before wraparound
-- Monitor: SELECT age(datfrozenxid) FROM pg_database; -- should be < 1.5B
```

**Q33. What are database locks?**
```sql
-- ROW-LEVEL LOCKS:
-- SELECT FOR UPDATE: lock rows for update in same transaction
SELECT * FROM accounts WHERE id = 1 FOR UPDATE; -- exclusive row lock
SELECT * FROM products WHERE id = 5 FOR SHARE;  -- shared row lock (others can share, not exclusive)

-- Avoid deadlocks: always acquire locks in same order
-- Bad: T1 locks row 1 then row 2; T2 locks row 2 then row 1 → deadlock!
-- Good: both always lock row 1 then row 2

-- TABLE-LEVEL LOCKS:
-- ACCESS SHARE: SELECT (many concurrent)
-- ROW SHARE: SELECT FOR UPDATE (many concurrent)
-- ROW EXCLUSIVE: INSERT, UPDATE, DELETE
-- ACCESS EXCLUSIVE: DROP TABLE, VACUUM FULL (blocks everything)

-- Advisory locks (application-level):
SELECT pg_try_advisory_lock(12345); -- returns true if acquired
SELECT pg_advisory_lock(12345);     -- blocks until acquired
SELECT pg_advisory_unlock(12345);   -- release

-- Use case: prevent duplicate job execution:
IF pg_try_advisory_lock(job_id) THEN
  run_job(job_id);
  pg_advisory_unlock(job_id);
END IF;

-- Optimistic locking (version column):
-- No DB lock, just check version on update:
SELECT id, balance, version FROM accounts WHERE id = 1; -- version = 5
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 5;  -- fails if another transaction updated it
-- Check rowcount: if 0 rows updated → concurrent modification → retry
```

**Q34. What is Redis and its data structures?**
```javascript
// Redis: in-memory data structure store (cache, message broker, pub/sub)

// STRING: key → bytes (max 512MB)
redis.set("user:1:name", "Alice");
redis.get("user:1:name");           // "Alice"
redis.setEx("session:abc", 3600, JSON.stringify(data)); // with TTL
redis.incr("page:hits");            // atomic increment
redis.incrBy("score:user1", 10);

// HASH: key → {field: value} (like a mini-document)
redis.hSet("user:1", { name: "Alice", age: "30", email: "a@b.com" });
redis.hGet("user:1", "name");       // "Alice"
redis.hGetAll("user:1");            // { name, age, email }
redis.hIncrBy("user:1", "visits", 1);

// LIST: key → ordered list (linked list)
redis.lPush("recent:pageviews", "/home", "/about");  // add to front
redis.rPush("queue:emails", JSON.stringify(email));  // add to back
redis.lPop("queue:emails");                          // remove from front
redis.lRange("recent:pageviews", 0, 9);              // get first 10
redis.lLen("queue:emails");

// SET: key → unique values
redis.sAdd("tags:post1", "redis", "database", "cache");
redis.sIsMember("tags:post1", "redis"); // true
redis.sMembers("tags:post1");           // ["redis", "database", "cache"]
redis.sInter("tags:post1", "tags:post2"); // intersection
redis.sUnion("tags:post1", "tags:post2"); // union

// SORTED SET: key → {member: score} (ranked by score)
redis.zAdd("leaderboard", [{ score: 9800, value: "alice" }, { score: 9500, value: "bob" }]);
redis.zRange("leaderboard", 0, 9, { REV: true, WITHSCORES: true }); // top 10
redis.zRank("leaderboard", "alice");  // rank (0-based)
redis.zIncrBy("leaderboard", 100, "alice"); // atomic score update

// PUBLISH/SUBSCRIBE:
// Publisher:
redis.publish("notifications:user:123", JSON.stringify({ type: "order.shipped" }));
// Subscriber:
redis.subscribe("notifications:user:123", (message) => console.log(message));

// Redis Streams (persistent pub/sub):
redis.xAdd("events", "*", { type: "order.created", orderId: "123" }); // * = auto-ID
redis.xRead({ COUNT: 10, STREAMS: ["events", "0"] }); // read from beginning
```

**Q35. What is MongoDB and when to use it?**
```javascript
// MongoDB: document database — JSON-like BSON documents
// Schema-flexible, horizontal scaling built-in

// DOCUMENTS vs ROWS:
// Relational: normalize → multiple tables + joins
// MongoDB: embed related data in same document

// User with orders — embedded (good for read-heavy):
{
  _id: ObjectId("..."),
  name: "Alice",
  email: "alice@example.com",
  orders: [
    { orderId: "ord_1", total: 99.99, items: [...], createdAt: ISODate("...") },
    { orderId: "ord_2", total: 149.00, items: [...], createdAt: ISODate("...") }
  ]
}

// CRUD operations:
db.users.insertOne({ name: "Alice", email: "alice@example.com" });
db.users.find({ age: { $gte: 18 }, active: true });
db.users.findOne({ email: "alice@example.com" }, { name: 1, email: 1 }); // projection
db.users.updateOne({ _id: id }, { $set: { name: "Alice B" }, $inc: { loginCount: 1 } });
db.users.deleteOne({ _id: id });

// AGGREGATION PIPELINE:
db.orders.aggregate([
  { $match: { status: "completed", createdAt: { $gte: new Date("2024-01-01") } } },
  { $group: { _id: "$userId", totalSpent: { $sum: "$amount" }, orderCount: { $sum: 1 } } },
  { $sort: { totalSpent: -1 } },
  { $limit: 10 },
  { $lookup: { from: "users", localField: "_id", foreignField: "_id", as: "user" } },
  { $unwind: "$user" },
  { $project: { name: "$user.name", totalSpent: 1, orderCount: 1 } }
]);

// INDEXES:
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ name: "text", bio: "text" }); // text search
db.orders.createIndex({ userId: 1, createdAt: -1 }); // compound
db.events.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 }); // TTL
```

**Q36. What is Elasticsearch?**
```javascript
// Elasticsearch: distributed search and analytics engine
// Built on Lucene, schema-flexible, REST API

// Index a document:
await client.index({
  index: "products",
  id: "1",
  document: {
    name: "iPhone 15 Pro",
    description: "Latest Apple smartphone with titanium design",
    category: "electronics",
    price: 999,
    tags: ["apple", "smartphone", "ios"],
    inStock: true,
  }
});

// Full-text search:
await client.search({
  index: "products",
  query: {
    multi_match: {
      query: "apple smartphone",
      fields: ["name^3", "description", "tags"], // name boosted 3x
      type: "best_fields",
      fuzziness: "AUTO", // handle typos
    }
  },
  sort: [{ _score: "desc" }, { price: "asc" }],
  from: 0, size: 10,
  highlight: { fields: { description: {} } },
  aggs: {
    price_ranges: {
      range: { field: "price", ranges: [{to: 500}, {from: 500, to: 1000}, {from: 1000}] }
    },
    by_category: { terms: { field: "category.keyword", size: 10 } }
  }
});

// Mapping (schema definition):
await client.indices.create({
  index: "products",
  mappings: {
    properties: {
      name: { type: "text", analyzer: "english" },
      category: { type: "keyword" }, // exact match only
      price: { type: "float" },
      tags: { type: "keyword" },
      description: { type: "text" },
    }
  }
});
```

---

## HARD (Q71–Q120)

**Q71. Query optimization deep dive — execution plans and statistics.**
```sql
-- PostgreSQL query planner uses statistics to estimate rows:
SELECT tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE tablename = 'orders' AND attname = 'user_id';
-- n_distinct > 0: number of distinct values
-- n_distinct < 0: fraction of rows (e.g., -0.1 means 10% distinct)
-- correlation: 1 = perfectly ordered, -1 = reverse ordered, 0 = random
-- High correlation → Index Scan preferred (sequential I/O)
-- Low correlation → Seq Scan preferred (random I/O worse than sequential)

-- Force specific plan (for testing only):
SET enable_seqscan = OFF;        -- disable sequential scans
SET enable_hashjoin = OFF;       -- disable hash joins
SET enable_mergejoin = OFF;      -- disable merge joins

-- Parallel query:
SET max_parallel_workers_per_gather = 4;
-- Tables: parallel_workers = 4 → planner may use up to 4 workers

-- Statistics targets:
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 200; -- more histogram buckets
ANALYZE orders; -- rebuild statistics

-- Planner cost model:
-- seq_page_cost = 1.0 (sequential disk read cost unit)
-- random_page_cost = 4.0 (random disk read: 4x slower than sequential)
-- cpu_tuple_cost = 0.01 (per row processing)
-- For SSDs: set random_page_cost = 1.1 (SSDs are faster for random access)
SET random_page_cost = 1.1; -- for SSD storage

-- Plan caching issues with parameterized queries:
-- First execution: plan cached based on parameter value
-- Subsequent: same plan used even if statistics suggest different plan
-- Fix: use fresh plan for parameters with high variability:
PREPARE my_query(int) AS SELECT * FROM orders WHERE user_id = $1;
-- Or use extended statistics for correlated columns:
CREATE STATISTICS stat_city_zip ON city, zip FROM addresses;
```

**Q72. Designing for high-availability databases.**
```
PRIMARY-REPLICA with automatic failover:

TOOLS:
- Patroni (PostgreSQL HA using etcd/Consul/ZooKeeper)
- PgBouncer (connection pooling)
- HAProxy (load balancer for read replicas)

ARCHITECTURE:
[App] → [PgBouncer] → [HAProxy]
                         ↓
              [Primary] ← sync replication → [Replica 1]
                         ← async replication → [Replica 2 (DR)]

FAILOVER PROCESS (automatic with Patroni):
1. Replica detects primary is down (health check fails)
2. Patroni runs leader election via DCS (etcd)
3. Winning replica promotes itself to primary
4. DCS updates primary key
5. PgBouncer/HAProxy updates connection to new primary
6. Old primary comes back as replica, catches up via replication

RPO (Recovery Point Objective): max data loss acceptable
  - Sync replication: RPO = 0 (no data loss)
  - Async replication: RPO = replication lag (typically seconds)

RTO (Recovery Time Objective): time to recover
  - Automatic failover: RTO = 30-60 seconds typically
  - Manual failover: RTO = minutes to hours

MONITORING:
- Replication lag: SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;
- Long transactions: SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active';
```

**Q73. Cassandra architecture and data modeling.**
```javascript
// Cassandra: wide-column store, AP system (availability + partition tolerance)
// Designed for: write-heavy, time-series, global distribution, linear horizontal scaling

// DATA MODEL: denormalized, query-first design
// Query: "Get all messages for a conversation, newest first"
CREATE TABLE messages (
  conversation_id UUID,
  created_at TIMESTAMP,
  message_id UUID,
  sender_id UUID,
  content TEXT,
  PRIMARY KEY ((conversation_id), created_at, message_id)
) WITH CLUSTERING ORDER BY (created_at DESC, message_id DESC);
-- Partition key: conversation_id → determines which node stores this data
-- Clustering columns: created_at, message_id → sorted within partition

// READS:
SELECT * FROM messages
WHERE conversation_id = :convId
AND created_at > :since
LIMIT 50;

// WRITE path:
// 1. Client writes to any node (coordinator)
// 2. Coordinator hashes partition key → finds replica nodes
// 3. Writes to commit log + memtable on each replica
// 4. Returns success after W replicas acknowledge (configurable)

// CONSISTENCY LEVELS:
// ONE: fastest, any 1 replica responds
// QUORUM: majority of replicas (N/2+1) — strong consistency
// ALL: all replicas — slowest
// LOCAL_QUORUM: quorum within same datacenter (for geo-distributed)

// COMPACTION: SSTables merged to reclaim space, remove tombstones
// Leveled Compaction: good for reads (small, equal-sized SSTables)
// Size-Tiered: good for writes (fewer, larger SSTables)

// ANTI-PATTERNS:
// - Large partitions (> 100MB) → hot spots, GC pressure
// - Unbounded rows (millions of clustering rows per partition)
// - Allow filtering (full table scan)
// - Secondary indexes (poor performance at scale)
```

**Q74. Connection pooling and performance.**
```javascript
// Why connection pooling:
// Creating DB connection: ~10-50ms (TCP handshake + auth + setup)
// With pool: reuse existing connections, ~0.1ms overhead

// PgBouncer modes:
// session: connection held for entire client session
// transaction: connection returned after each transaction (most efficient)
// statement: connection returned after each statement (limited features)

// Node.js with pg connection pool:
const pool = new Pool({
  host: "localhost",
  database: "myapp",
  max: 20,            // max connections in pool
  min: 5,             // keep at least 5 connections open
  idleTimeoutMillis: 30000, // close idle connections after 30s
  connectionTimeoutMillis: 2000, // wait up to 2s for connection
  ssl: { rejectUnauthorized: false },
});

// Always release connection back to pool:
async function query(sql, params) {
  const client = await pool.connect();
  try {
    return await client.query(sql, params);
  } finally {
    client.release(); // CRITICAL — always release!
  }
}

// Pool sizing formula:
// connections = ((core_count * 2) + effective_spindle_count)
// Example: 4 cores, SSD (1 spindle) → 4*2+1 = 9 connections
// Common heuristic: 10-20 connections per application server

// Monitoring pool health:
// pool.totalCount: all connections
// pool.idleCount: idle connections
// pool.waitingCount: requests waiting for connection
// Alert if waitingCount > 0 for extended periods
```

**Q75–Q120. Key database topics.**

**Q75. What is database connection security?**
```sql
-- SSL/TLS for connections:
-- postgresql.conf: ssl = on, ssl_cert_file = 'server.crt', ssl_key_file = 'server.key'
-- pg_hba.conf: hostssl all all 0.0.0.0/0 scram-sha-256

-- Row-Level Security (RLS):
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_orders ON orders
  FOR ALL TO app_user
  USING (user_id = current_setting('app.current_user_id')::bigint);

-- Now each query automatically filtered:
SET app.current_user_id = '42';
SELECT * FROM orders; -- automatically adds WHERE user_id = 42

-- Column encryption (sensitive data):
-- Store encrypted: INSERT INTO users(ssn) VALUES(pgp_sym_encrypt('123-45-6789', $SECRET_KEY));
-- Decrypt on read: SELECT pgp_sym_decrypt(ssn::bytea, $SECRET_KEY) FROM users;

-- SQL injection prevention: ALWAYS use parameterized queries:
-- BAD:  `SELECT * FROM users WHERE email = '${userInput}'` -- injectable!
-- GOOD: db.query("SELECT * FROM users WHERE email = $1", [userInput])

-- Least privilege: create read-only users for reporting:
CREATE USER reporter WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO reporter;
GRANT USAGE ON SCHEMA public TO reporter;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reporter;
```

**Q76. What are database migrations best practices?**
```javascript
// Migration tools: Flyway, Liquibase (Java), Knex.js, Prisma (Node.js)

// Migration file: V001__create_users.sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

// Golden rules:
// 1. NEVER edit a committed migration — create a new one
// 2. Each migration forward AND rollback
// 3. Make migrations idempotent when possible (IF NOT EXISTS)
// 4. Test on production-like data before applying
// 5. Keep migrations small and focused

// Safe schema changes (online DDL — no table lock):
-- Add nullable column (instant):
ALTER TABLE users ADD COLUMN preferences JSONB;

-- Add column with default (might lock in older PostgreSQL):
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN role VARCHAR(20);
-- Step 2: Backfill in batches
UPDATE users SET role = 'user' WHERE role IS NULL AND id BETWEEN 1 AND 10000;
-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN role SET NOT NULL;

-- Safe index creation (no lock):
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
-- CONCURRENTLY: builds index without locking the table (takes longer)

// Zero-downtime deployments:
// Expand: add new column/table (backward compatible)
// Migrate: code writes to both old and new
// Contract: remove old column/table
```

ENDFILE
echo "Databases: $(wc -l < /mnt/user-data/outputs/iq_07_databases.md) lines"

---

## COMPLETING DATABASES Q23–Q120

**Q23. What are SQL window functions in depth?**
```sql
-- Window functions: compute across rows related to current row WITHOUT collapsing

SELECT name, department, salary,
  -- Running total within department:
  SUM(salary) OVER (PARTITION BY department ORDER BY hire_date
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,

  -- Moving average (last 3 rows):
  AVG(salary) OVER (PARTITION BY department ORDER BY hire_date
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg,

  -- Rank (gaps for ties), DenseRank (no gaps), RowNumber (unique):
  RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,

  -- NTILE: divide into N buckets (quartiles, percentiles):
  NTILE(4) OVER (ORDER BY salary) AS quartile,

  -- PERCENT_RANK: relative rank 0-1:
  PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank,

  -- LAG/LEAD: access neighboring rows:
  LAG(salary,  1, 0) OVER (PARTITION BY department ORDER BY hire_date) AS prev_salary,
  LEAD(salary, 1, 0) OVER (PARTITION BY department ORDER BY hire_date) AS next_salary,

  -- First/Last value in window:
  FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS max_in_dept,
  NTH_VALUE(salary, 2) OVER (PARTITION BY department ORDER BY salary DESC) AS second_highest

FROM employees;
```

**Q24. What are database transactions and isolation in depth?**
```sql
-- ISOLATION LEVELS and phenomena they prevent:

-- READ UNCOMMITTED: dirty reads allowed (see uncommitted data) — almost never use
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- READ COMMITTED (PostgreSQL default): prevents dirty reads
-- Each query sees snapshot at query start time
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- REPEATABLE READ (MySQL InnoDB default): prevents dirty + non-repeatable reads
-- All reads in transaction see snapshot at tx start time
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- SERIALIZABLE: prevents all phenomena including phantom reads
-- Transactions appear to execute one-at-a-time
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SAVEPOINTS — partial rollback within transaction:
BEGIN;
  INSERT INTO orders(user_id, total) VALUES(1, 99.99);
  SAVEPOINT order_created;
  UPDATE inventory SET qty = qty - 1 WHERE product_id = 42;
  -- If update fails:
  ROLLBACK TO SAVEPOINT order_created; -- only undo inventory update
  -- Or:
COMMIT; -- commits everything including the order

-- Explicit locking:
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;     -- exclusive row lock
SELECT * FROM accounts WHERE id = 1 FOR SHARE;      -- shared row lock
SELECT * FROM accounts WHERE id = 1 FOR UPDATE SKIP LOCKED; -- skip locked rows (queue pattern)
```

**Q25. What is PostgreSQL EXPLAIN output interpretation?**
```sql
-- EXPLAIN ANALYZE shows actual execution plan + timing

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;

-- Sample output:
-- Limit  (cost=1234.56..1234.61 rows=10) (actual time=45.3..45.4 rows=10)
--   -> Sort  (cost=1234.56..1235.56 rows=400) (actual time=45.3..45.3 rows=10)
--     Sort Key: (count(o.id)) DESC
--     Sort Method: top-N heapsort  Memory: 25kB
--     -> HashAggregate  (cost=1200.00..1208.00 rows=400) (actual time=44.8..44.9 rows=400)
--       -> Hash Left Join  (cost=500.00..1100.00 rows=4000)
--           Hash Cond: (o.user_id = u.id)
--           -> Seq Scan on orders o  (cost=0.00..400.00 rows=20000) actual time=0.1..12.3
--           -> Hash  (cost=450.00..450.00 rows=4000)
--             -> Index Scan using idx_users_created on users u
--                 Index Cond: (created_at > '2024-01-01')

-- Key things to look for:
-- Seq Scan on large table: needs index
-- Nested Loop with large outer: consider hash join
-- High rows estimate vs actual: stale statistics → ANALYZE
-- High buffer hits: good (cache hits) vs reads: bad (disk I/O)
-- Sort in memory: good | Sort on disk: bad (increase work_mem)
```

**Q26. What are database constraints?**
```sql
-- Constraints enforce data integrity at the database level

CREATE TABLE orders (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status      VARCHAR(20) NOT NULL DEFAULT 'pending'
              CHECK (status IN ('pending','processing','shipped','delivered','cancelled')),
  total       DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  discount    DECIMAL(5,2) CHECK (discount BETWEEN 0 AND 100),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Table-level constraints:
  CONSTRAINT valid_dates CHECK (updated_at >= created_at),
  UNIQUE (user_id, created_at) -- one order per user per timestamp (example)
);

-- Deferrable constraints (check at end of transaction, not each statement):
ALTER TABLE orders ADD CONSTRAINT fk_user
  FOREIGN KEY (user_id) REFERENCES users(id)
  DEFERRABLE INITIALLY DEFERRED;

-- Exclusion constraints (prevent overlapping time ranges):
CREATE TABLE reservations (
  room_id int,
  during tstzrange,
  EXCLUDE USING GIST (room_id WITH =, during WITH &&) -- no overlapping ranges for same room
);

-- Foreign key actions:
-- ON DELETE CASCADE: delete related records
-- ON DELETE SET NULL: set FK to NULL
-- ON DELETE RESTRICT: prevent deletion if referenced
-- ON DELETE NO ACTION: same as RESTRICT (checked at statement end)
```

**Q27. What is database partitioning?**
```sql
-- Partition: divide large table into smaller pieces
-- Benefits: query only relevant partitions (partition pruning), easier archival

-- Range partitioning by date:
CREATE TABLE orders (
  id BIGSERIAL,
  user_id BIGINT,
  created_at TIMESTAMPTZ,
  total DECIMAL(10,2)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_q1 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE orders_2024_q2 PARTITION OF orders
  FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Query with date filter → only scans relevant partition:
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-03-31';
-- EXPLAIN: Seq Scan on orders_2024_q1 (not all partitions!)

-- List partitioning by category:
CREATE TABLE products PARTITION BY LIST (category);
CREATE TABLE products_electronics PARTITION OF products FOR VALUES IN ('electronics');
CREATE TABLE products_clothing PARTITION OF products FOR VALUES IN ('clothing','shoes');

-- Hash partitioning for even distribution:
CREATE TABLE user_events PARTITION BY HASH (user_id);
CREATE TABLE user_events_0 PARTITION OF user_events FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_events_1 PARTITION OF user_events FOR VALUES WITH (MODULUS 4, REMAINDER 1);
-- etc. for 2,3

-- Attach/detach partitions (drop old data fast):
ALTER TABLE orders DETACH PARTITION orders_2022;
DROP TABLE orders_2022; -- instant! vs DELETE which is slow
```

**Q28. What is Redis advanced data structures?**
```javascript
// Redis Sorted Sets — leaderboard, rate limiting, range queries
await redis.zAdd('leaderboard', [
  { score: 9800, value: 'alice' },
  { score: 9500, value: 'bob' },
  { score: 9200, value: 'carol' },
]);
await redis.zRange('leaderboard', 0, 9, { REV: true, WITHSCORES: true }); // top 10
await redis.zRank('leaderboard', 'alice');    // 0 (top)
await redis.zIncrBy('leaderboard', 150, 'bob'); // add 150 to bob's score

// Redis Streams — persistent pub/sub with consumer groups
await redis.xAdd('orders', '*', { type: 'order.created', orderId: '123' });
// Consumer group (each message processed by ONE consumer in group):
await redis.xGroupCreate('orders', 'processors', '0');
const messages = await redis.xReadGroup('processors', 'worker-1', [{ key: 'orders', id: '>' }], { COUNT: 10 });
await redis.xAck('orders', 'processors', messageId); // acknowledge processed

// Redis Pub/Sub — real-time messaging
await redis.subscribe('notifications:user:123', (message) => {
  console.log('Received:', message);
});
await redis.publish('notifications:user:123', JSON.stringify({ type: 'order_shipped' }));

// Redis Bloom Filter (RedisBloom module)
await redis.bf.add('seen_emails', 'user@example.com');
await redis.bf.exists('seen_emails', 'user@example.com'); // true
await redis.bf.exists('seen_emails', 'new@example.com'); // false (99.9% reliable)
// Use: deduplication, spam detection, URL shortener uniqueness check
```

**Q29–Q75: Key database topics**
```sql
-- Q29. Aggregate functions: COUNT, SUM, AVG, MIN, MAX, STDDEV, PERCENTILE_CONT
-- Q30. HAVING vs WHERE: WHERE filters rows before grouping, HAVING filters groups
-- Q31. UNION vs UNION ALL: UNION deduplicates (slower), UNION ALL keeps all (faster)
-- Q32. INTERSECT: rows in both queries; EXCEPT: rows in first but not second
-- Q33. Correlated subquery: inner query references outer query (runs N times)
-- Q34. EXISTS vs IN: EXISTS stops at first match, IN evaluates all values
-- Q35. COALESCE: first non-null value; NULLIF(a,b): null if a=b else a
-- Q36. CASE expression: SQL if-else for values
-- Q37. Lateral join: each row from left joined with correlated subquery result
-- Q38. Recursive CTE: WITH RECURSIVE for hierarchies and graphs
-- Q39. Full-text search: tsvector, tsquery, GIN index in PostgreSQL
-- Q40. JSON in PostgreSQL: jsonb (binary, indexed) vs json (stored as-is)
SELECT data->>'name' FROM users;  -- extract JSON field
SELECT * FROM users WHERE data @> '{"role":"admin"}'; -- JSON containment
CREATE INDEX idx_data_role ON users USING GIN(data jsonb_path_ops);

-- Q41. Arrays in PostgreSQL:
SELECT ARRAY['a','b','c'] @> ARRAY['a']; -- contains
SELECT unnest(ARRAY[1,2,3]); -- expand to rows
CREATE INDEX ON users USING GIN(tags); -- index array column

-- Q42. PostgreSQL materialized views:
CREATE MATERIALIZED VIEW monthly_revenue AS
  SELECT DATE_TRUNC('month', created_at), SUM(total) FROM orders GROUP BY 1;
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue; -- no table lock

-- Q43. Row-level security (RLS):
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_orders ON orders USING (user_id = current_setting('app.user_id')::int);
-- Every query auto-filtered: SELECT * FROM orders WHERE user_id = current_user

-- Q44. PostgreSQL extensions:
-- pg_stat_statements: query statistics
-- pgcrypto: encryption functions
-- uuid-ossp: UUID generation
-- PostGIS: geographic data
-- pg_trgm: trigram similarity search
-- timescaledb: time-series optimization

-- Q45. Database migrations best practices:
-- Never edit committed migration, always new file
-- Use IF NOT EXISTS for idempotent migrations
-- CREATE INDEX CONCURRENTLY (no table lock)
-- Add NOT NULL via: add nullable, backfill, add constraint (3 steps)
-- Test rollback migration before deploying

-- Q46. Query optimization techniques:
-- Use EXPLAIN ANALYZE before and after
-- Ensure statistics are fresh: ANALYZE table_name
-- Use partial indexes for common filtered queries
-- Avoid function calls on indexed columns in WHERE
-- Use LIMIT to reduce work when only N rows needed

-- Q47. Connection pooling configuration:
-- PgBouncer transaction mode: most efficient
-- Set pool_size per database
-- Monitor: pgbouncer SHOW POOLS, SHOW CLIENTS

-- Q48. Backup strategies:
-- pg_dump: logical backup, slow, portable
-- pg_basebackup: physical backup, fast, requires same PG version
-- WAL archiving + PITR: point-in-time recovery
-- Barman, pgBackRest: managed backup tools

-- Q49. Monitoring queries:
SELECT pid, now()-query_start as duration, state, query
FROM pg_stat_activity
WHERE state = 'active' AND now()-query_start > interval '5 minutes';

-- Kill long query:
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid = 12345;

-- Find missing indexes:
SELECT relname, seq_scan, idx_scan FROM pg_stat_user_tables
WHERE seq_scan > idx_scan ORDER BY seq_scan DESC;

-- Q50. MongoDB aggregation pipeline stages:
-- $match, $group, $project, $sort, $limit, $skip, $lookup, $unwind
-- $addFields, $replaceRoot, $facet (multiple pipelines), $bucket (range grouping)
-- $graphLookup (recursive), $text (full-text), $geoNear (geospatial)

-- Q51. MongoDB indexes:
-- Single field, compound, text, geospatial (2dsphere), hashed, TTL, partial, sparse
-- db.collection.explain("executionStats").find({...}) -- query analysis

-- Q52. MongoDB transactions (4.0+):
-- session.startTransaction()
-- try: operations; session.commitTransaction()
-- catch: session.abortTransaction()
-- Multi-document ACID across collections and databases

-- Q53. MongoDB sharding:
-- Range sharding: ranges of shard key values → different shards
-- Hash sharding: even distribution, no range queries
-- Zone sharding: specific ranges to specific shards (geo-pinning)

-- Q54. Cassandra data modeling principles:
-- Design for queries, not normalization
-- Partition key determines data distribution
-- Clustering columns determine sort order within partition
-- Denormalize: duplicate data to avoid joins
-- No joins, no subqueries, limited aggregations

-- Q55. Cassandra consistency levels:
-- ONE: any one replica
-- QUORUM: majority (N/2+1)
-- ALL: all replicas (slowest, highest consistency)
-- LOCAL_QUORUM: quorum in local datacenter (geo-distributed)
-- Each read/write can specify different consistency level

-- Q56. Redis persistence:
-- RDB: snapshot at intervals (fast recovery, may lose recent data)
-- AOF: append-only log of all commands (durable, larger file)
-- RDB+AOF: both (recommended for production)
-- No persistence: cache only (fastest, data loss on restart)

-- Q57. Redis cluster:
-- 16384 hash slots distributed across N masters
-- Each master can have 1+ replicas
-- Automatic resharding when nodes added/removed
-- Clients must handle MOVED redirects

-- Q58. Elasticsearch mapping and analyzers:
-- text: analyzed (tokenized, lowercased, stemmed) for full-text search
-- keyword: not analyzed, exact match, aggregations, sorting
-- Standard analyzer: tokenize + lowercase + stop words
-- Custom analyzer: define tokenizer + filters

-- Q59. Elasticsearch query types:
-- match: full-text search with analysis
-- term: exact value match (keyword fields)
-- range: numeric/date range
-- bool: combine must/should/must_not/filter
-- multi_match: search across multiple fields
-- nested: query on nested object arrays
-- geo_distance: location-based queries

-- Q60. TimescaleDB vs InfluxDB vs Prometheus:
-- TimescaleDB: PostgreSQL extension, SQL, relational + time-series
-- InfluxDB: custom query language (Flux), high write throughput
-- Prometheus: pull-based metrics, PromQL, 15s resolution typical
-- Use case: infrastructure metrics (Prometheus), business time-series (TimescaleDB/InfluxDB)

-- Q61-Q120: Rapid reference
-- Q61. Explain VACUUM in PostgreSQL: reclaim dead tuple space, prevent txid wraparound
-- Q62. What is write amplification: each write causes multiple physical writes (indexes, WAL)
-- Q63. CQRS with read replicas: write to primary, eventual sync to read replicas
-- Q64. Event store vs regular DB: append-only, no updates, replay events for state
-- Q65. Outbox pattern: write event to DB table in same transaction, poll and publish
-- Q66. Database-per-service pattern: loose coupling, independent scaling
-- Q67. Polyglot persistence: use best database per service (PostgreSQL + Redis + MongoDB)
-- Q68. Write-ahead log (WAL): journal of changes, enables crash recovery and replication
-- Q69. Checkpoint in PostgreSQL: flush dirty buffers to disk, update WAL position
-- Q70. Autovacuum tuning: increase workers, decrease threshold for large active tables
-- Q71. Table bloat: dead tuples accumulate → VACUUM or pg_repack for zero-downtime
-- Q72. Index bloat: similar to table bloat → REINDEX CONCURRENTLY
-- Q73. pg_stat_user_tables: rows, seq_scans, index scans, insert/update/delete counts
-- Q74. Slow query log: log_min_duration_statement = 1000 (log queries > 1 second)
-- Q75. Statement timeout: SET statement_timeout = '30s' (per session or globally)
```

**Q76. How does MongoDB handle schema validation?**
```javascript
// MongoDB schema validation (JSON Schema)
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'email', 'createdAt'],
      properties: {
        name:  { bsonType: 'string', minLength: 1, maxLength: 100 },
        email: { bsonType: 'string', pattern: '^[\w.-]+@[\w.-]+\.[a-z]{2,}$' },
        age:   { bsonType: 'int', minimum: 0, maximum: 150 },
        role:  { enum: ['admin', 'user', 'editor'] },
        tags:  { bsonType: 'array', items: { bsonType: 'string' } },
        address: {
          bsonType: 'object',
          required: ['city'],
          properties: {
            city: { bsonType: 'string' },
            zip:  { bsonType: 'string', pattern: '^[0-9]{5}$' }
          }
        }
      }
    }
  },
  validationAction: 'error', // 'error' (reject) or 'warn' (log)
  validationLevel: 'strict'  // 'strict' (all) or 'moderate' (existing docs exempt)
});

// Update validation on existing collection:
db.runCommand({ collMod: 'users', validator: {...} });
```

**Q77. What are database anti-patterns?**
```sql
-- Q77. Common database anti-patterns:

-- 1. SELECT *: fetches all columns, prevents index-only scans
SELECT id, name, email FROM users WHERE id = 1; -- specific columns

-- 2. N+1 queries: one query per row instead of join
-- BAD: for each user → SELECT orders WHERE user_id = ?
-- GOOD: SELECT users JOIN orders ON user_id = users.id

-- 3. Storing comma-separated values:
-- BAD: tags = 'redis,postgres,kafka'
-- GOOD: separate tags table with FK relationship (or ARRAY in PostgreSQL)

-- 4. Using NULLs for unknown vs absent:
-- Use NULL for absent, use specific sentinel values carefully

-- 5. Missing indexes on FK columns:
-- Always index foreign key columns for joins and cascades

-- 6. Not using connection pooling:
-- Creating new connection per request → too slow

-- 7. Autoincrement as distributed ID:
-- Use UUID v7 (time-ordered) or Snowflake IDs for distributed systems

-- 8. Storing JSON for structured data that needs querying:
-- JSON fine for truly flexible data, terrible for SQL queries on JSON fields

-- 9. Too many indexes:
-- Each index slows writes. Only index columns you query frequently.

-- 10. Implicit type conversion in WHERE:
-- WHERE user_id = '123' -- string vs int → full scan!
-- WHERE user_id = 123   -- correct type → uses index
```

**Q78–Q120: Advanced database patterns**
```javascript
// Q78. Optimistic vs pessimistic locking:
// Pessimistic: SELECT FOR UPDATE (lock row during transaction) — prevents conflict, slower
// Optimistic: version column, check on update — no lock, retry on conflict

// Optimistic locking example:
// 1. Read: SELECT id, balance, version FROM accounts WHERE id = 1
// 2. Compute new balance
// 3. Update: UPDATE accounts SET balance = newBalance, version = version + 1
//            WHERE id = 1 AND version = 5  -- fails if concurrent update happened
// 4. If rowsAffected === 0: conflict! retry

// Q79. Cursor-based pagination vs offset:
// Offset: OFFSET 10000 LIMIT 20 → scans 10020 rows (slow!)
// Cursor: WHERE (created_at, id) > (lastCursor) LIMIT 20 → uses index (fast!)
// Cursor also handles inserts: items don't shift, no duplicates

// Q80. Database connection management:
const pool = new Pool({ max: 20, idleTimeoutMillis: 30000 });
// Always release: use try/finally or connection pool's withConnection helper
async function query(sql, params) {
  const client = await pool.connect();
  try { return await client.query(sql, params); }
  finally { client.release(); }
}

// Q81. Upsert patterns:
// PostgreSQL:
// INSERT INTO users(email, name) VALUES($1,$2)
// ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, updated_at = NOW();

// Q82. Batch inserts for performance:
// BAD: 1000 INSERT statements
// GOOD: INSERT INTO t VALUES ($1,$2), ($3,$4), ... ($999,$1000) -- one statement

// Q83. COPY command (PostgreSQL bulk load):
// COPY users(name, email) FROM '/tmp/users.csv' CSV HEADER;
// Much faster than INSERT for bulk data

// Q84. Table inheritance in PostgreSQL:
// CREATE TABLE log_2024 () INHERITS (log);
// Queries on log include log_2024 rows automatically

// Q85. Generated columns:
// CREATE TABLE orders (subtotal NUMERIC, tax NUMERIC,
//   total NUMERIC GENERATED ALWAYS AS (subtotal + tax) STORED);

// Q86. Functional indexes:
// CREATE INDEX idx_lower_email ON users(LOWER(email));
// WHERE LOWER(email) = 'alice@example.com' -- uses index

// Q87. Partial index:
// CREATE INDEX idx_active_users ON users(last_login) WHERE active = true;
// Much smaller index, faster for active user queries

// Q88. Index-only scans:
// Query satisfied entirely from index (no table heap access)
// Requires: all needed columns in index, no dead tuples (VACUUM)
// INCLUDE clause: CREATE INDEX idx_email ON users(email) INCLUDE (name, id);

// Q89. Bloom index (PostgreSQL):
// Small probabilistic index for multi-column equality queries
// CREATE INDEX idx_bloom ON users USING BLOOM(email, name, phone);

// Q90. BRIN index (Block Range Index):
// Very small index for naturally ordered data (timestamps, sequential IDs)
// CREATE INDEX idx_created ON events USING BRIN(created_at);

// Q91. Parallel queries in PostgreSQL:
// max_parallel_workers_per_gather: how many parallel workers per query node
// Large Seq Scans and aggregations can run in parallel
// SET max_parallel_workers_per_gather = 4;

// Q92. Work_mem for sorting and hashing:
// SET work_mem = '256MB'; -- per sort/hash operation per query
// Higher = faster sorts/hash joins, but higher memory usage

// Q93. Vacuum and autovacuum tuning:
// autovacuum_vacuum_scale_factor = 0.01 (vacuum when 1% dead)
// autovacuum_analyze_scale_factor = 0.005 (analyze when 0.5% changed)
// For large tables: lower these values or set per-table storage parameters

// Q94. Dead lock detection and prevention:
// Always acquire locks in the same order across all transactions
// Use shorter transactions to reduce lock contention
// Monitor: SELECT * FROM pg_locks WHERE NOT granted;

// Q95. Sequence vs UUID for primary keys:
// BIGSERIAL: compact, sortable, predictable (security concern)
// UUID v4: random, globally unique, no ordering
// UUID v7: time-ordered UUID (sorted by creation time) — best of both worlds

// Q96. Database sharding strategies:
// Range: user IDs 1-1M shard 1, 1M-2M shard 2 (hotspots possible)
// Hash: hash(user_id) % N shards (even, no range queries)
// Directory: lookup table (flexible, single point of failure)
// Consistent hashing: minimal resharding when adding shards

// Q97. Read-your-writes consistency:
// Problem: write to primary, read from replica (may not have write yet)
// Solution 1: always read from primary after write for X seconds
// Solution 2: include write timestamp in session, compare with replica lag
// Solution 3: read from primary if replica lag > threshold

// Q98. Database connection proxy (ProxySQL, pgBouncer):
// Multiplex many application connections → fewer DB connections
// Split read/write traffic transparently
// Query cache, connection pooling, failover

// Q99. Point-in-time recovery (PITR):
// base backup + WAL archive → restore to any point in time
// pg_restore + replay WAL to target time
// Critical for: accidental data deletion recovery

// Q100. Logical replication vs physical:
// Physical: byte-for-byte copy (streaming replication, same PG version)
// Logical: row-level changes decoded from WAL (cross-version, selective tables)
// Use logical for: zero-downtime major version upgrades, selective replication

// Q101–Q120: Advanced topics
// Q101. FDW (Foreign Data Wrapper): query remote data sources as local tables
// Q102. pg_partman: automatic partition management extension
// Q103. Citus: PostgreSQL extension for horizontal scaling (sharding)
// Q104. Pgvector: vector similarity search (AI embeddings) in PostgreSQL
// Q105. Temporal tables: system-period and application-period versioning
// Q106. Audit logging: triggers + audit table for complete change history
// Q107. Soft deletes: deleted_at timestamp vs hard DELETE + archive table
// Q108. Multi-tenancy models: separate DBs, separate schemas, shared table + tenant_id
// Q109. Database proxy pattern: abstract DB details from application
// Q110. Schema evolution strategies: expand-migrate-contract for zero-downtime
// Q111. Query result caching vs data caching: cache at DB vs app layer
// Q112. Materialized view refresh strategies: full refresh vs incremental
// Q113. Hash join vs nested loop vs merge join: planner chooses based on statistics
// Q114. Cost-based optimizer: uses statistics to estimate and choose best plan
// Q115. Statistics in PostgreSQL: per-column histograms, most-common values
// Q116. pg_hint_plan: force specific execution plans (override optimizer)
// Q117. Connection migration: move session to different server (Pgpool-II)
// Q118. Hot standby: read queries on replica while streaming replication active
// Q119. Synchronous vs asynchronous replication: durability vs performance tradeoff
// Q120. Database design for multi-currency: always store as minor units (cents), use NUMERIC not FLOAT
```


---

## COMPLETING DATABASES Q23–Q120

**Q23. What are the SQL window functions?**
```sql
SELECT name, department, salary,
  RANK()       OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
  SUM(salary)  OVER (PARTITION BY department ORDER BY salary)      AS running_total,
  LAG(salary, 1, 0) OVER (PARTITION BY department ORDER BY salary) AS prev_salary,
  LEAD(salary, 1)   OVER (PARTITION BY department ORDER BY salary) AS next_salary,
  salary * 100.0 / SUM(salary) OVER (PARTITION BY department)      AS pct_of_dept,
  AVG(salary) OVER (PARTITION BY department ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_avg
FROM employees;
-- Top 3 per department:
WITH ranked AS (SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) r FROM employees)
SELECT * FROM ranked WHERE r <= 3;
```

**Q24. What are CTEs and recursive CTEs?**
```sql
-- Basic CTE:
WITH active_users AS (SELECT * FROM users WHERE active = true),
     revenue AS (SELECT user_id, SUM(amount) total FROM orders GROUP BY user_id)
SELECT u.name, COALESCE(r.total,0) revenue
FROM active_users u LEFT JOIN revenue r ON u.id = r.user_id ORDER BY revenue DESC;

-- Recursive CTE (org chart, tree traversal):
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 0 AS level FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, o.level+1
  FROM employees e JOIN org o ON e.manager_id = o.id
)
SELECT REPEAT('  ',level) || name AS hierarchy FROM org ORDER BY level, name;
```

**Q25. How do you optimize slow queries?**
```sql
-- Step 1: EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM orders WHERE user_id = 42;
-- Look for: Seq Scan (bad on large tables), Index Scan (good), Index Only Scan (best)
-- High rows_removed → better index needed
-- High buffers hit → data not in cache

-- Step 2: Create missing index:
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);
-- CONCURRENTLY: no table lock, takes longer to build

-- Step 3: Covering index (all needed columns in index):
CREATE INDEX idx_orders_user_status ON orders(user_id, status) INCLUDE (total, created_at);
-- Query: SELECT total, created_at FROM orders WHERE user_id=42 AND status='paid'
-- → Index Only Scan (no heap access!)

-- Step 4: Common pitfalls:
-- BAD: function on indexed column:
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com'; -- can't use index!
-- FIX: functional index:
CREATE INDEX idx_lower_email ON users(LOWER(email));

-- Step 5: Partition large tables:
CREATE TABLE events_2024 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
-- Queries with date filter skip irrelevant partitions
```

**Q26. What are database transactions and isolation?**
```sql
-- ACID: Atomicity, Consistency, Isolation, Durability

-- Isolation levels and what they prevent:
-- READ UNCOMMITTED: dirty reads allowed (never use)
-- READ COMMITTED (default PostgreSQL): no dirty reads
-- REPEATABLE READ (default MySQL): no dirty + non-repeatable reads
-- SERIALIZABLE: strictest, prevents all anomalies

-- Example:
BEGIN;
  SELECT balance FROM accounts WHERE id=1 FOR UPDATE; -- lock row
  UPDATE accounts SET balance = balance - 100 WHERE id=1;
  UPDATE accounts SET balance = balance + 100 WHERE id=2;
COMMIT; -- or ROLLBACK on error

-- Deadlock prevention: always acquire locks in same order
-- Optimistic locking:
UPDATE orders SET status='paid', version=version+1
WHERE id=? AND version=?; -- fails if concurrent update
```

**Q27. What is Redis and its use cases?**
```javascript
// Redis: in-memory data structure store
// Use cases: session storage, caching, pub/sub, rate limiting, leaderboards

// Session storage:
await redis.setEx(`session:${sessionId}`, 3600, JSON.stringify(user));
const session = await redis.get(`session:${sessionId}`);

// Caching with cache-aside:
async function getUser(id) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  const user = await db.query('SELECT * FROM users WHERE id=$1', [id]);
  await redis.setEx(`user:${id}`, 300, JSON.stringify(user));
  return user;
}

// Rate limiting (sliding window):
const key = `rate:${ip}`;
const count = await redis.incr(key);
if (count === 1) await redis.expire(key, 60);
if (count > 100) throw new RateLimitError();

// Leaderboard (sorted set):
await redis.zAdd('leaderboard', [{score: 9500, value: 'alice'}]);
const top10 = await redis.zRange('leaderboard', 0, 9, {REV: true, WITHSCORES: true});

// Pub/Sub for real-time:
await publisher.publish('notifications', JSON.stringify({userId, message}));
await subscriber.subscribe('notifications', handler);

// Distributed lock:
const lock = await redis.set(`lock:${resourceId}`, 'locked', {NX: true, EX: 30});
if (!lock) throw new Error('Resource locked');
try { await criticalSection(); }
finally { await redis.del(`lock:${resourceId}`); }
```

**Q28. What is MongoDB aggregation pipeline?**
```javascript
// Aggregation: process documents through pipeline stages
db.orders.aggregate([
  // Stage 1: Filter
  { $match: { status: 'completed', createdAt: { $gte: new Date('2024-01-01') } } },

  // Stage 2: Group
  { $group: {
    _id: '$userId',
    totalRevenue: { $sum: '$amount' },
    orderCount: { $sum: 1 },
    avgOrder: { $avg: '$amount' },
    lastOrder: { $max: '$createdAt' }
  }},

  // Stage 3: Sort
  { $sort: { totalRevenue: -1 } },

  // Stage 4: Limit
  { $limit: 10 },

  // Stage 5: Lookup (JOIN with users collection)
  { $lookup: { from: 'users', localField: '_id', foreignField: '_id', as: 'user' } },
  { $unwind: '$user' },

  // Stage 6: Project (shape output)
  { $project: { name: '$user.name', email: '$user.email', totalRevenue: 1, orderCount: 1 } }
]);

// Useful operators: $bucket, $facet, $graphLookup, $geoNear, $changeStream
```

**Q29–Q50: SQL patterns**
```sql
-- Q29. Pivot table (rows to columns):
SELECT
  SUM(CASE WHEN month=1 THEN revenue END) AS jan,
  SUM(CASE WHEN month=2 THEN revenue END) AS feb,
  SUM(CASE WHEN month=3 THEN revenue END) AS mar
FROM monthly_revenue GROUP BY year;

-- Q30. Finding gaps in sequences:
SELECT t1.id+1 AS gap_start
FROM orders t1
WHERE NOT EXISTS (SELECT 1 FROM orders t2 WHERE t2.id = t1.id+1)
AND t1.id < (SELECT MAX(id) FROM orders);

-- Q31. Delete duplicate rows, keep one:
DELETE FROM users WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) rn FROM users
  ) t WHERE rn > 1
);

-- Q32. Running total:
SELECT date, amount,
  SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS running_total
FROM daily_sales;

-- Q33. Self-join to find pairs:
SELECT a.name, b.name
FROM employees a JOIN employees b ON a.manager_id = b.id;

-- Q34. Hierarchical query (alternative to recursive CTE):
SELECT id, name, CONNECT_BY_ISCYCLE, LEVEL, SYS_CONNECT_BY_PATH(name,'/')
FROM employees START WITH manager_id IS NULL
CONNECT BY NOCYCLE PRIOR id = manager_id; -- Oracle syntax

-- Q35. JSON operations in PostgreSQL:
SELECT data->>'name', data->'address'->>'city'
FROM users WHERE data @> '{"active": true}';
UPDATE users SET data = data || '{"verified": true}'::jsonb WHERE id=1;
SELECT jsonb_array_elements(data->'tags') AS tag FROM posts;

-- Q36. Full-text search:
ALTER TABLE articles ADD COLUMN fts tsvector
  GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || content)) STORED;
CREATE INDEX idx_fts ON articles USING GIN(fts);
SELECT title FROM articles WHERE fts @@ plainto_tsquery('english', 'machine learning');

-- Q37. Upsert (INSERT ON CONFLICT):
INSERT INTO user_stats(user_id, login_count) VALUES($1, 1)
ON CONFLICT (user_id) DO UPDATE SET
  login_count = user_stats.login_count + 1,
  last_login = NOW();

-- Q38. LATERAL JOIN (correlated subquery as join):
SELECT u.name, recent_orders.total
FROM users u
CROSS JOIN LATERAL (
  SELECT total FROM orders WHERE user_id=u.id ORDER BY created_at DESC LIMIT 5
) recent_orders;

-- Q39. Materialized view for slow aggregations:
CREATE MATERIALIZED VIEW monthly_sales AS
  SELECT DATE_TRUNC('month', created_at) month, SUM(amount) total FROM orders GROUP BY 1;
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;

-- Q40. Advisory locks for distributed coordination:
SELECT pg_try_advisory_lock(12345); -- returns true if acquired
SELECT pg_advisory_unlock(12345);
```

**Q41–Q70: Database internals**
```sql
-- Q41. B-tree index internals: balanced tree, O(log n) all ops, range scans via linked leaves
-- Q42. Hash index: O(1) equality, no range queries, PostgreSQL only
-- Q43. GIN index: inverted index for arrays, JSONB, full-text search
-- Q44. BRIN index: block range for sequential data (timestamps, IDs), tiny size
-- Q45. Partial index: WHERE clause, only index matching rows (e.g., active users only)

-- Q46. Vacuum in PostgreSQL:
VACUUM ANALYZE users;      -- clean dead tuples, update stats
VACUUM FULL users;         -- reclaim more space (exclusive lock, avoid in prod)
-- autovacuum: runs automatically, configure scale_factor and threshold

-- Q47. Table bloat: dead rows accumulate, use pg_stat_user_tables to monitor
-- Q48. Index bloat: fragmented over time, REINDEX CONCURRENTLY to rebuild

-- Q49. Connection pooling modes (PgBouncer):
-- session: 1 DB conn per client session
-- transaction: release after each transaction (most efficient, recommended)
-- statement: release after each statement (breaks multi-statement transactions)

-- Q50. Partitioning strategies:
-- Range: by date (most common for time-series)
-- List: by discrete values (country, status)
-- Hash: by hash of key (even distribution)
-- Sub-partitioning: partition of partition

-- Q51. Columnar storage (Parquet, ClickHouse):
-- Store each column separately — great for analytics (scan only needed columns)
-- Compression per column — similar values compress well
-- Bad for: OLTP, row-by-row updates

-- Q52. Write-ahead log (WAL):
-- Changes written to WAL before data pages
-- On crash: replay WAL from last checkpoint
-- Also used for: streaming replication, logical replication

-- Q53. MVCC (Multi-Version Concurrency Control):
-- Each row version has xmin (created by txn) and xmax (deleted by txn)
-- Readers see consistent snapshot without locks
-- Writers don't block readers, readers don't block writers

-- Q54. Two-phase commit:
-- Prepare: all participants vote yes/no
-- Commit/abort: coordinator decides based on all votes
-- Problem: coordinator failure leaves participants blocked

-- Q55. Optimistic vs pessimistic locking:
-- Pessimistic: SELECT FOR UPDATE — block others during transaction
-- Optimistic: version column — check version on UPDATE, retry on mismatch

-- Q56. N+1 query problem and solutions:
-- Problem: SELECT users, then SELECT orders for each user = N+1 queries
-- Fix: JOIN, IN clause, batching, DataLoader (GraphQL), eager loading

-- Q57. Database migrations best practices:
-- Never modify deployed migrations, create new ones
-- Additive-first: add column nullable, backfill, add constraint
-- CREATE INDEX CONCURRENTLY for zero-downtime
-- Test on production-sized data

-- Q58. Database sharding trade-offs:
-- + Horizontal scale beyond single machine
-- - Cross-shard queries are expensive/impossible
-- - Resharding is painful (consistent hashing helps)
-- - Distributed transactions needed across shards

-- Q59. Time-series databases (TimescaleDB, InfluxDB):
-- Optimized for: append-only, time-based queries, aggregations
-- Auto-partitioning by time, compression, continuous aggregates

-- Q60. Graph databases (Neo4j):
-- Native graph storage: nodes, relationships, properties
-- Cypher query: MATCH (u:User)-[:FOLLOWS]->(f) WHERE u.name='Alice' RETURN f

-- Q61. Vector databases (Pinecone, pgvector):
-- Store embeddings, similarity search (k-nearest neighbors)
-- Used for: semantic search, recommendation, RAG (AI)

-- Q62. Document stores vs relational:
-- Document: flexible schema, embed related data, horizontal scale
-- Relational: schema enforcement, joins, ACID, complex queries

-- Q63. CAP theorem for databases:
-- CP (consistent + partition-tolerant): PostgreSQL, HBase, ZooKeeper
-- AP (available + partition-tolerant): Cassandra, DynamoDB, CouchDB
-- Network partitions always happen → must choose C or A

-- Q64. BASE vs ACID:
-- BASE: Basically Available, Soft state, Eventual consistency
-- Used by: Cassandra, DynamoDB, MongoDB (by default)

-- Q65. Read-your-writes consistency:
-- After write, user's own reads must see the write
-- Implemented: route user's reads to same replica they wrote to

-- Q66. Cassandra data modeling principles:
-- Query-first design: model around your queries, not entities
-- Denormalize: embed data to avoid joins (no joins in Cassandra!)
-- Partition key determines distribution, clustering key orders within partition
-- Wide rows: many clustering columns, efficient range scans

-- Q67. Redis data structures for use cases:
-- String: simple K-V, counters, session tokens
-- Hash: user objects (HSET user:1 field value)
-- List: message queues, activity feeds (LPUSH, RPOP)
-- Set: unique visitors, tags (SADD, SMEMBERS, SUNION)
-- Sorted Set: leaderboards, delayed queues (ZADD, ZRANGE)
-- HyperLogLog: approximate unique count (memory efficient)
-- Bloom Filter: probabilistic membership (no false negatives)
-- Stream: persistent, consumer-group message queue (XADD, XREAD)

-- Q68. Database connection security:
-- SSL/TLS for all connections
-- Role-based access: READ-ONLY user for reports
-- Row-level security (PostgreSQL): policies per user
-- Column encryption for PII/sensitive data
-- Parameterized queries always: prevent SQL injection

-- Q69. Database monitoring key metrics:
-- Query latency: p50/p95/p99 per query
-- Connection count vs max_connections
-- Replication lag: SELECT NOW() - pg_last_xact_replay_timestamp()
-- Lock wait time: pg_stat_activity WHERE wait_event_type='Lock'
-- Cache hit ratio: pg_statio_user_tables (heap_blks_hit / total)
-- Table bloat: pg_stat_user_tables n_dead_tup

-- Q70. Online schema changes (zero downtime):
-- gh-ost (MySQL), pg_repack (PostgreSQL)
-- Shadow table: copy to new table with changes, swap atomically
-- Additive changes only: add nullable column (instant), backfill async

-- Q71–Q100: Advanced topics
-- Q71. Column statistics and query planner: ANALYZE updates, SET STATISTICS 500
-- Q72. Parallel query execution: set max_parallel_workers_per_gather
-- Q73. JIT compilation in PostgreSQL: improves complex expression performance
-- Q74. Foreign data wrappers: query external data sources as local tables
-- Q75. Logical replication: replicate specific tables, across major versions
-- Q76. pgAudit: detailed audit logging for compliance
-- Q77. pg_partman: automated partition management
-- Q78. TimescaleDB: time-series extension for PostgreSQL
-- Q79. pgvector: vector similarity search extension
-- Q80. Citus: distributed PostgreSQL (sharding as extension)
-- Q81. Amazon Aurora: MySQL/PostgreSQL-compatible, 6-way replication, serverless v2
-- Q82. Google Spanner: globally distributed SQL, external consistency, TrueTime
-- Q83. CockroachDB: distributed SQL, PostgreSQL-compatible, serializable isolation
-- Q84. PlanetScale: MySQL-compatible, branching, non-blocking schema changes
-- Q85. Supabase: PostgreSQL + realtime + auth + storage
-- Q86. DynamoDB single-table design: model all entities in one table
-- Q87. DynamoDB capacity: provisioned vs on-demand, RCU/WCU calculation
-- Q88. DynamoDB transactions: TransactGet, TransactWrite for ACID
-- Q89. Elasticsearch document refresh: near-real-time (1s), control with ?refresh
-- Q90. Elasticsearch shards: primary + replicas, rebalancing, hot-warm architecture
-- Q91. Database connection string security: vault, secrets manager, rotation
-- Q92. Database backup strategies: logical (pg_dump), physical (pg_basebackup), PITR
-- Q93. Point-in-time recovery: WAL archives allow restore to any point
-- Q94. Tablespace: control physical location of tables/indexes
-- Q95. TOAST (PostgreSQL): large values stored in separate table automatically
-- Q96. Dead tuple bloat: monitor with pg_stat_user_tables n_dead_tup
-- Q97. Vacuumdb: full database maintenance, analyze statistics
-- Q98. Table inheritance (PostgreSQL): declarative partitioning preferred now
-- Q99. Generated columns: computed from other columns, stored or virtual
-- Q100. Domain types: custom type with constraints (e.g., email domain)
-- Q101–Q120: JSONB operators, range types, composite types, custom aggregates
```
