# The Complete SQL & PostgreSQL Mastery Guide
> One document to rule them all. Every concept explained from first principles — architecture, internals, query planning, concurrency, indexing, and production patterns. No hand-waving.

---

## Table of Contents

### Part I — SQL Fundamentals
1. [How PostgreSQL Works — Architecture & Processes](#chapter-1-how-postgresql-works)
2. [Data Types — Deep Dive](#chapter-2-data-types)
3. [DDL — Schemas, Tables & Constraints](#chapter-3-ddl)
4. [DML — SELECT, INSERT, UPDATE, DELETE](#chapter-4-dml)
5. [Joins — Every Type, Explained Visually](#chapter-5-joins)
6. [Aggregations & GROUP BY](#chapter-6-aggregations)
7. [Subqueries & Common Table Expressions (CTEs)](#chapter-7-subqueries--ctes)
8. [Window Functions](#chapter-8-window-functions)

### Part II — PostgreSQL Internals
9. [Indexes — B-Tree, Hash, GIN, GiST, BRIN, Partial, Composite](#chapter-9-indexes)
10. [Query Planner & EXPLAIN ANALYZE](#chapter-10-query-planner)
11. [MVCC — Multi-Version Concurrency Control](#chapter-11-mvcc)
12. [Transactions, Isolation Levels & Locking](#chapter-12-transactions)

### Part III — Advanced PostgreSQL
13. [Stored Procedures, Functions & Triggers](#chapter-13-functions--triggers)
14. [JSONB, Arrays & Advanced Types](#chapter-14-jsonb--arrays)
15. [Full-Text Search](#chapter-15-full-text-search)
16. [Table Partitioning](#chapter-16-partitioning)
17. [Replication & High Availability](#chapter-17-replication)
18. [Performance Tuning — Production Playbook](#chapter-18-performance-tuning)
19. [Schema Design & Normalization](#chapter-19-schema-design)

---

# PART I — SQL FUNDAMENTALS

---

## Chapter 1: How PostgreSQL Works

### 1.1 The Big Picture — PostgreSQL Architecture

PostgreSQL is a **process-based** database server. Every client connection spawns a dedicated backend process. This is different from thread-based databases (MySQL uses threads). The tradeoff: more stable isolation per connection, but higher overhead at scale (which is why connection poolers like PgBouncer exist).

```
CLIENT APPLICATION
       │
       │ TCP/IP or Unix socket
       ▼
┌─────────────────────────────────────────────────────────┐
│                    POSTMASTER PROCESS                   │
│  (the master daemon — listens on port 5432)             │
│  Forks a new backend process for every connection       │
└────────────────────────┬────────────────────────────────┘
                         │ fork()
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    [Backend 1]    [Backend 2]    [Backend 3]
    (your psql)    (your app)     (another app)
          │              │              │
          └──────────────┴──────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │       SHARED MEMORY          │
          │                              │
          │  ┌────────────────────────┐  │
          │  │   Shared Buffer Pool   │  │ ← cached data pages
          │  │   (shared_buffers)     │  │
          │  └────────────────────────┘  │
          │  ┌────────────────────────┐  │
          │  │   WAL Buffers          │  │ ← write-ahead log buffer
          │  └────────────────────────┘  │
          │  ┌────────────────────────┐  │
          │  │   Lock Table           │  │ ← shared lock state
          │  └────────────────────────┘  │
          └──────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │       DISK STORAGE           │
          │                              │
          │  data/base/        ← table/index files (heap)
          │  data/pg_wal/      ← WAL segment files
          │  data/pg_clog/     ← transaction commit status
          │  data/global/      ← cluster-wide catalogs
          └──────────────────────────────┘
```

### 1.2 Background Processes

PostgreSQL runs several background processes you should know:

```
BACKGROUND WRITER (bgwriter)
  Periodically flushes dirty pages from shared_buffers to disk.
  Reduces the spike of I/O when a backend needs a buffer slot.

CHECKPOINTER
  Performs checkpoints: ensures all dirty pages are flushed to disk.
  After a crash, recovery only needs to replay WAL from the last checkpoint.
  Controlled by: checkpoint_completion_target, checkpoint_timeout

WAL WRITER
  Flushes WAL buffers to WAL files on disk.
  Ensures durability before backends report "committed".

AUTOVACUUM LAUNCHER + WORKERS
  Triggers VACUUM and ANALYZE on tables automatically.
  Critical for MVCC dead tuple cleanup. (More in Chapter 11.)

STATS COLLECTOR
  Gathers query stats, table access counts, index usage.
  Powers pg_stat_user_tables, pg_stat_statements, etc.

WAL SENDER / WAL RECEIVER
  Used in streaming replication.
  Primary sends WAL; standby receives and replays it.
```

### 1.3 How a Query Executes — End to End

```
Your SQL string
      │
      ▼
┌─────────────┐
│   PARSER    │  Tokenizes SQL, builds parse tree
│             │  Checks syntax only — not semantics
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ANALYZER   │  Resolves names: tables, columns, functions
│             │  Checks semantic validity, resolves types
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  REWRITER   │  Applies rules (e.g., view expansion)
│             │  Expands * into column list
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PLANNER /  │  Generates possible query plans
│  OPTIMIZER  │  Estimates costs using table statistics
│             │  Chooses lowest-cost plan
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EXECUTOR   │  Runs the chosen plan
│             │  Fetches pages from buffer pool or disk
│             │  Returns rows to client
└─────────────┘
```

### 1.4 Storage — Pages and Tuples

PostgreSQL stores data in **8KB pages** (blocks). Every table and index is a file divided into 8KB pages.

```
TABLE FILE (heap)
┌─────────────────────────────────────────────────────┐
│  Page 0 (8192 bytes)                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│  │  Header  │ │  Item    │ │  Free space          │ │
│  │  (24 B)  │ │  pointers│ │                      │ │
│  └──────────┘ └──────────┘ │        ▲             │ │
│                            │        │             │ │
│                            │   Tuples grow UP     │ │
│                            │   (from bottom)      │ │
│                            └──────────────────────┘ │
└─────────────────────────────────────────────────────┘

TUPLE (row) structure:
  - HeapTupleHeader: xmin, xmax, ctid, infomask
  - NULL bitmap (if any nullable columns)
  - Actual column data

xmin = transaction ID that inserted this version
xmax = transaction ID that deleted/updated this version
ctid  = physical location (page, offset) — used by indexes
```

---

## Chapter 2: Data Types

### 2.1 Numeric Types

```sql
-- INTEGER FAMILY
SMALLINT          -- 2 bytes, -32768 to +32767
INTEGER (INT)     -- 4 bytes, -2.1B to +2.1B   ← most common
BIGINT            -- 8 bytes, ±9.2 quintillion

-- AUTO-INCREMENT (sequences under the hood)
SERIAL            -- INTEGER + implicit sequence   (legacy)
BIGSERIAL         -- BIGINT  + implicit sequence   (legacy)
GENERATED ALWAYS AS IDENTITY   -- SQL standard, preferred

CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  ...
);

-- EXACT DECIMALS — use for money, never FLOAT
NUMERIC(precision, scale)   -- arbitrary precision, exact
DECIMAL(precision, scale)   -- alias for NUMERIC
-- NUMERIC(10, 2) → up to 10 total digits, 2 after decimal
-- stores as variable-length binary-coded decimal

-- FLOATING POINT — approximate, never use for money
REAL              -- 4 bytes, ~6 decimal digits precision
DOUBLE PRECISION  -- 8 bytes, ~15 decimal digits precision
-- WARNING: 0.1 + 0.2 ≠ 0.3 in floating point

-- MONEY — locale-dependent, avoid in new schemas
MONEY             -- 8 bytes, fixed-point with locale formatting
```

### 2.2 Text Types

```sql
-- PostgreSQL text storage: TOAST (The Oversized-Attribute Storage Technique)
-- Values > 2KB may be compressed and/or moved out of the main table row

VARCHAR(n)    -- variable-length, max n characters
CHAR(n)       -- fixed-length, padded with spaces — rarely useful
TEXT          -- unlimited variable-length

-- KEY INSIGHT: In PostgreSQL, VARCHAR, VARCHAR(n), and TEXT
-- all use the same internal storage (varlena). VARCHAR(n) just
-- adds a check constraint on length. TEXT is idiomatic Postgres.

-- PERFORMANCE: There is NO performance difference between TEXT and VARCHAR.
-- Prefer TEXT unless you need the length constraint.

-- String functions you must know:
SELECT
  length('hello'),                    -- 5
  upper('hello'),                     -- HELLO
  lower('HELLO'),                     -- hello
  trim('  hello  '),                  -- 'hello'
  ltrim('  hello'),                   -- 'hello'
  rtrim('hello  '),                   -- 'hello'
  substring('hello world', 1, 5),     -- 'hello'
  position('world' IN 'hello world'), -- 7
  replace('hello world', 'world', 'postgres'), -- 'hello postgres'
  split_part('a,b,c', ',', 2),        -- 'b'
  string_agg(col, ', '),              -- aggregate: join strings
  concat('hello', ' ', 'world'),      -- 'hello world'
  format('Hello %s, you are %s', 'Alice', 'great'); -- formatted string
```

### 2.3 Date & Time Types

```sql
DATE            -- date only, no time (4 bytes)
TIME            -- time only, no date (8 bytes)
TIMESTAMP       -- date + time, NO timezone (8 bytes)
TIMESTAMPTZ     -- date + time, WITH timezone (8 bytes)
INTERVAL        -- duration (16 bytes)

-- CRITICAL: Always use TIMESTAMPTZ for application timestamps.
-- TIMESTAMP stores the literal value you give it — no conversion.
-- TIMESTAMPTZ converts to UTC internally; displays in session timezone.

-- Example:
SET timezone = 'America/New_York';
INSERT INTO events (created_at) VALUES (NOW()); -- stored as UTC
SELECT created_at FROM events; -- displayed as America/New_York

-- Useful functions:
NOW()                          -- current timestamp with tz
CURRENT_TIMESTAMP              -- same as NOW()
CURRENT_DATE                   -- today's date
EXTRACT(year FROM NOW())       -- extract part
DATE_TRUNC('month', NOW())     -- truncate to month start
AGE(timestamp1, timestamp2)    -- returns INTERVAL
NOW() + INTERVAL '7 days'      -- date arithmetic
TO_CHAR(NOW(), 'YYYY-MM-DD')   -- format to string
TO_TIMESTAMP('2024-01-15', 'YYYY-MM-DD') -- parse from string
```

### 2.4 Boolean, UUID, Arrays, JSONB

```sql
-- BOOLEAN
BOOLEAN   -- true, false, NULL
-- Accepts: true/false, 't'/'f', 'yes'/'no', '1'/'0', 'on'/'off'

-- UUID
UUID      -- 16 bytes, universally unique identifier
-- Generate with: gen_random_uuid() [pgcrypto] or uuid_generate_v4()
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY
);

-- ARRAYS
INTEGER[]   -- array of integers
TEXT[]      -- array of text
-- PostgreSQL supports multi-dimensional arrays

CREATE TABLE tags (
  article_id INT,
  tags TEXT[]
);
INSERT INTO tags VALUES (1, ARRAY['postgres', 'sql', 'database']);
-- Or: '{postgres,sql,database}'

SELECT tags[1] FROM tags;           -- 'postgres' (1-indexed!)
SELECT * FROM tags WHERE 'sql' = ANY(tags);
SELECT * FROM tags WHERE tags @> ARRAY['sql']; -- contains

-- JSONB (Chapter 14 has full coverage)
JSONB   -- binary JSON, indexed, operators, fast
JSON    -- stored as text, slower — avoid in new schemas
```

---

## Chapter 3: DDL — Schemas, Tables & Constraints

### 3.1 Schemas

```sql
-- A schema is a namespace inside a database.
-- Default schema: public
-- search_path determines which schemas are searched first.

CREATE SCHEMA app;
CREATE SCHEMA audit;

SET search_path = app, public;  -- looks in 'app' first, then 'public'

-- Best practice: don't use public schema in production
-- Use named schemas per domain (app, auth, billing, etc.)
```

### 3.2 CREATE TABLE

```sql
CREATE TABLE users (
  -- Primary key — identity column (preferred over SERIAL)
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

  -- Text with constraints
  email         TEXT NOT NULL UNIQUE,
  username      TEXT NOT NULL CHECK (length(username) >= 3),
  display_name  TEXT,                          -- nullable

  -- Enums (use CHECK or CREATE TYPE)
  status        TEXT NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'inactive', 'banned')),

  -- Timestamps
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Foreign key
  role_id       INT REFERENCES roles(id) ON DELETE SET NULL
);

-- TABLE-LEVEL CONSTRAINTS (when constraint spans multiple columns)
CREATE TABLE order_items (
  order_id    BIGINT NOT NULL,
  product_id  BIGINT NOT NULL,
  quantity    INT NOT NULL CHECK (quantity > 0),
  price       NUMERIC(10,2) NOT NULL,
  PRIMARY KEY (order_id, product_id),           -- composite PK
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### 3.3 Constraints Deep Dive

```sql
-- NOT NULL: column cannot be NULL
-- UNIQUE: all values must be distinct (allows one NULL — NULLs are not equal)
-- CHECK: arbitrary boolean expression
-- PRIMARY KEY: NOT NULL + UNIQUE — every table should have one
-- FOREIGN KEY: referential integrity

-- FOREIGN KEY actions:
ON DELETE NO ACTION   -- default: error if referenced row deleted
ON DELETE RESTRICT    -- same as NO ACTION but checked immediately
ON DELETE CASCADE     -- delete child rows automatically
ON DELETE SET NULL    -- set FK column to NULL
ON DELETE SET DEFAULT -- set FK column to its default

-- DEFERRABLE CONSTRAINTS
-- By default, constraints are checked immediately (per statement).
-- DEFERRABLE allows deferring check to end of transaction.
-- Useful for circular references or bulk inserts.
ALTER TABLE order_items
  ADD CONSTRAINT fk_order
  FOREIGN KEY (order_id) REFERENCES orders(id)
  DEFERRABLE INITIALLY DEFERRED;

-- EXCLUSION CONSTRAINTS (PostgreSQL-specific)
-- Ensures no two rows satisfy a given operator combination.
-- Example: no overlapping room bookings
CREATE TABLE room_bookings (
  room_id   INT,
  during    TSTZRANGE,
  EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);
-- && = overlaps operator for ranges
```

### 3.4 ALTER TABLE

```sql
-- Add column
ALTER TABLE users ADD COLUMN phone TEXT;

-- Drop column
ALTER TABLE users DROP COLUMN phone;

-- Rename column
ALTER TABLE users RENAME COLUMN username TO user_name;

-- Change type (be careful — may require USING clause)
ALTER TABLE users ALTER COLUMN status TYPE VARCHAR(20);

-- Set default
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- Add constraint
ALTER TABLE users ADD CONSTRAINT chk_email CHECK (email LIKE '%@%');

-- Drop constraint
ALTER TABLE users DROP CONSTRAINT chk_email;

-- Add NOT NULL (requires no existing NULLs)
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- IMPORTANT: In PostgreSQL, ALTER TABLE ADD COLUMN with a DEFAULT
-- that is a volatile function (like NOW()) requires a full table rewrite
-- in older versions. In PG11+, non-null defaults with constant values
-- are metadata-only and instant.
```

---

## Chapter 4: DML — SELECT, INSERT, UPDATE, DELETE

### 4.1 SELECT — Execution Order

The most important thing to understand about SELECT is that SQL clauses are **not evaluated in the order you write them**:

```
Writing order:          Execution order:
1. SELECT               1. FROM          ← determine source tables
2. FROM                 2. JOIN          ← combine tables
3. JOIN                 3. WHERE         ← filter rows
4. WHERE                4. GROUP BY      ← group remaining rows
5. GROUP BY             5. HAVING        ← filter groups
6. HAVING               6. SELECT        ← compute output columns
7. ORDER BY             7. DISTINCT      ← remove duplicates
8. LIMIT/OFFSET         8. ORDER BY      ← sort results
                        9. LIMIT/OFFSET  ← paginate

WHY THIS MATTERS:
- You CANNOT use a SELECT alias in WHERE (alias doesn't exist yet)
- You CAN use SELECT alias in ORDER BY (it's evaluated later)
- You CANNOT use aggregate functions in WHERE (use HAVING)
- You CAN use GROUP BY column numbers: GROUP BY 1, 2
```

### 4.2 SELECT — Full Syntax

```sql
-- Basic query anatomy
SELECT
  u.id,
  u.email,
  u.created_at,
  COUNT(o.id) AS order_count,
  SUM(o.total) AS lifetime_value,
  CASE
    WHEN SUM(o.total) > 1000 THEN 'VIP'
    WHEN SUM(o.total) > 100  THEN 'Regular'
    ELSE 'New'
  END AS customer_tier
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
  AND u.created_at >= NOW() - INTERVAL '1 year'
GROUP BY u.id, u.email, u.created_at
HAVING COUNT(o.id) > 0
ORDER BY lifetime_value DESC NULLS LAST
LIMIT 100
OFFSET 0;

-- DISTINCT
SELECT DISTINCT country FROM users;

-- DISTINCT ON (PostgreSQL-specific) — keep one row per group
SELECT DISTINCT ON (user_id)
  user_id, created_at, total
FROM orders
ORDER BY user_id, created_at DESC;
-- Returns the most recent order per user
```

### 4.3 INSERT

```sql
-- Single row
INSERT INTO users (email, username) VALUES ('a@b.com', 'alice');

-- Multi-row
INSERT INTO users (email, username) VALUES
  ('b@b.com', 'bob'),
  ('c@b.com', 'carol');

-- INSERT from SELECT
INSERT INTO archived_users
SELECT * FROM users WHERE status = 'inactive';

-- RETURNING — get back generated values
INSERT INTO users (email) VALUES ('d@b.com')
RETURNING id, created_at;

-- UPSERT — ON CONFLICT
INSERT INTO users (email, username)
VALUES ('a@b.com', 'alice_new')
ON CONFLICT (email) DO UPDATE
  SET username = EXCLUDED.username,
      updated_at = NOW();
-- EXCLUDED refers to the row that was proposed for insertion

-- ON CONFLICT DO NOTHING — ignore if conflict
INSERT INTO users (email) VALUES ('a@b.com')
ON CONFLICT (email) DO NOTHING;
```

### 4.4 UPDATE

```sql
-- Basic update
UPDATE users SET status = 'inactive' WHERE last_login < NOW() - INTERVAL '90 days';

-- Update multiple columns
UPDATE products
SET price = price * 1.1,
    updated_at = NOW()
WHERE category = 'electronics';

-- UPDATE ... FROM (join in update)
UPDATE order_items oi
SET discounted_price = oi.price * (1 - d.discount_rate)
FROM discounts d
WHERE d.product_id = oi.product_id
  AND d.active = true;

-- RETURNING from UPDATE
UPDATE users SET status = 'banned' WHERE email = 'bad@actor.com'
RETURNING id, email, status;
```

### 4.5 DELETE

```sql
-- Basic delete
DELETE FROM sessions WHERE expires_at < NOW();

-- DELETE ... USING (join in delete)
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.id
  AND o.status = 'cancelled';

-- RETURNING from DELETE
DELETE FROM users WHERE status = 'deleted' RETURNING id, email;

-- TRUNCATE — fast bulk delete (no WHERE, no RETURNING)
TRUNCATE TABLE sessions;
TRUNCATE TABLE sessions, session_tokens; -- multiple tables
TRUNCATE TABLE orders CASCADE;           -- cascade to children

-- TRUNCATE vs DELETE:
-- DELETE: row-by-row, generates WAL for each row, triggers fire, can have WHERE
-- TRUNCATE: metadata operation, minimal WAL, triggers fire (but no row-level), no WHERE
-- TRUNCATE resets sequences if RESTART IDENTITY is used
```

---

## Chapter 5: Joins — Every Type, Explained Visually

### 5.1 Join Fundamentals

A join combines rows from two tables based on a related column. Think of it as a pipeline:

```
table A                   table B
┌────┬──────┐             ┌────┬──────────┐
│ id │ name │             │ id │ user_id  │
├────┼──────┤             ├────┼──────────┤
│  1 │ Alice│             │ 10 │    1     │  ← Alice has order
│  2 │ Bob  │             │ 11 │    1     │  ← Alice has another
│  3 │ Carol│             │ 12 │    4     │  ← user 4 doesn't exist
└────┴──────┘             └────┴──────────┘

INNER JOIN (ON users.id = orders.user_id):
  Only rows with matches in BOTH tables
  Result: Alice+order10, Alice+order11   (Bob, Carol excluded; order12 excluded)

LEFT JOIN:
  ALL rows from LEFT table, matched rows from RIGHT (NULLs for no match)
  Result: Alice+order10, Alice+order11, Bob+NULL, Carol+NULL

RIGHT JOIN:
  ALL rows from RIGHT table, matched rows from LEFT
  Result: Alice+order10, Alice+order11, NULL+order12

FULL OUTER JOIN:
  ALL rows from BOTH tables, NULLs where no match
  Result: Alice+order10, Alice+order11, Bob+NULL, Carol+NULL, NULL+order12

CROSS JOIN:
  Every combination (cartesian product) — 3 × 3 = 9 rows
  No ON clause
```

### 5.2 Join SQL Syntax

```sql
-- INNER JOIN (default JOIN keyword)
SELECT u.name, o.id, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN — all users, even without orders
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Finding rows with NO match (LEFT JOIN anti-pattern)
SELECT u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;  -- users who never ordered

-- FULL OUTER JOIN
SELECT u.name, o.id
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- CROSS JOIN (generates all combinations — use with care)
SELECT d.name, m.name
FROM departments d
CROSS JOIN months m;

-- SELF JOIN — table joined to itself
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- NATURAL JOIN — joins on columns with same name (avoid in production)
-- Dangerous: schema changes can silently break queries

-- USING clause — when join column has same name in both tables
SELECT u.name, o.total
FROM users u
JOIN orders o USING (user_id);  -- cleaner than ON u.user_id = o.user_id
```

### 5.3 Join Algorithms (How PostgreSQL Executes Joins)

```
NESTED LOOP JOIN
  For each row in outer table, scan inner table.
  Best when: outer table is small, inner has an index on join column.
  Cost: O(outer × inner) → O(outer) with index on inner

HASH JOIN
  Build a hash table from the smaller table.
  Probe it with each row from the larger table.
  Best when: large tables, no useful index, equi-joins.
  Cost: O(N + M)
  Memory: hash table must fit in work_mem

MERGE JOIN
  Both inputs must be sorted on the join key.
  Scans both in parallel — like merging two sorted lists.
  Best when: both inputs already sorted (index scan) or sort is needed anyway.
  Cost: O(N log N + M log M)

PostgreSQL chooses automatically based on:
  - Table statistics (row counts, column distribution)
  - Available indexes
  - work_mem setting
  - enable_hashjoin, enable_mergejoin, enable_nestloop flags
```

---

## Chapter 6: Aggregations & GROUP BY

### 6.1 Aggregate Functions

```sql
-- Standard aggregates
COUNT(*)           -- count all rows including NULLs
COUNT(col)         -- count non-NULL values
COUNT(DISTINCT col) -- count distinct non-NULL values
SUM(col)           -- sum of non-NULL values
AVG(col)           -- average of non-NULL values
MIN(col)           -- minimum
MAX(col)           -- maximum

-- Statistical aggregates
STDDEV(col)        -- standard deviation
VARIANCE(col)      -- variance
CORR(col1, col2)   -- correlation coefficient

-- String aggregation
STRING_AGG(col, separator)                    -- join strings
STRING_AGG(col, ',' ORDER BY col)             -- ordered join

-- Array aggregation
ARRAY_AGG(col)                                -- collect into array
ARRAY_AGG(col ORDER BY col DESC)

-- JSON aggregation
JSON_AGG(row)                                 -- collect rows as JSON array
JSONB_AGG(row)
JSON_OBJECT_AGG(key_col, val_col)            -- build JSON object

-- NULL handling: all aggregates IGNORE NULLs except COUNT(*)
-- AVG(col) = SUM(col) / COUNT(col) — not COUNT(*)
```

### 6.2 GROUP BY Rules and HAVING

```sql
-- GROUP BY Rule: every column in SELECT must be either:
--   a) in the GROUP BY clause, OR
--   b) inside an aggregate function

-- WRONG:
SELECT user_id, email, COUNT(*) FROM orders GROUP BY user_id;
-- email is neither aggregated nor in GROUP BY → ERROR

-- RIGHT:
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;

-- HAVING: filter AFTER grouping (can use aggregates)
-- WHERE:  filter BEFORE grouping (cannot use aggregates)

SELECT
  user_id,
  COUNT(*) AS order_count,
  SUM(total) AS revenue
FROM orders
WHERE created_at >= '2024-01-01'  -- filter rows first
GROUP BY user_id
HAVING COUNT(*) >= 3              -- filter groups
   AND SUM(total) > 100;

-- GROUPING SETS — multiple GROUP BY in one query
SELECT
  COALESCE(region, 'ALL') AS region,
  COALESCE(product, 'ALL') AS product,
  SUM(sales) AS total_sales
FROM sales_fact
GROUP BY GROUPING SETS (
  (region, product),  -- subtotals per region+product
  (region),           -- subtotals per region
  (product),          -- subtotals per product
  ()                  -- grand total
);

-- ROLLUP — hierarchical grouping (shorthand for common pattern)
GROUP BY ROLLUP (region, product)
-- Equivalent to GROUPING SETS ((region,product),(region),())

-- CUBE — all possible combinations
GROUP BY CUBE (region, product)
-- Equivalent to GROUPING SETS ((region,product),(region),(product),())
```

---

## Chapter 7: Subqueries & CTEs

### 7.1 Subquery Types

```sql
-- SCALAR SUBQUERY — returns exactly one value (one row, one column)
SELECT
  name,
  (SELECT AVG(salary) FROM employees) AS company_avg,
  salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;

-- ROW SUBQUERY — returns one row, multiple columns
SELECT * FROM employees
WHERE (department_id, salary) = (SELECT department_id, MAX(salary) FROM employees GROUP BY department_id LIMIT 1);

-- TABLE SUBQUERY (derived table) — used in FROM clause
SELECT dept_name, avg_salary
FROM (
  SELECT d.name AS dept_name, AVG(e.salary) AS avg_salary
  FROM departments d
  JOIN employees e ON e.department_id = d.id
  GROUP BY d.id, d.name
) AS dept_stats
WHERE avg_salary > 70000;

-- CORRELATED SUBQUERY — references outer query columns
-- Runs once per outer row — can be slow
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (
  SELECT AVG(salary) FROM employees WHERE department_id = e.department_id
);
-- Returns employees earning above their department average
-- Note: e.department_id in subquery references the outer query

-- EXISTS — returns true if subquery returns any rows
-- More efficient than IN for large datasets (short-circuits on first match)
SELECT * FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 500
);

-- NOT EXISTS — rows in left table with no matching row in right
SELECT * FROM users u
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- IN with subquery
SELECT * FROM products WHERE category_id IN (SELECT id FROM categories WHERE active = true);

-- ANY / ALL
SELECT name FROM employees WHERE salary > ANY (SELECT salary FROM managers);
-- > ANY means: greater than at least one manager's salary (> MIN)
SELECT name FROM employees WHERE salary > ALL (SELECT salary FROM managers);
-- > ALL means: greater than every manager's salary (> MAX)
```

### 7.2 Common Table Expressions (CTEs)

```sql
-- BASIC CTE — named subquery, runs once, reused
WITH active_users AS (
  SELECT id, email, created_at
  FROM users
  WHERE status = 'active'
),
user_stats AS (
  SELECT user_id, COUNT(*) AS orders, SUM(total) AS revenue
  FROM orders
  GROUP BY user_id
)
SELECT
  u.email,
  COALESCE(s.orders, 0) AS total_orders,
  COALESCE(s.revenue, 0.00) AS total_revenue
FROM active_users u
LEFT JOIN user_stats s ON s.user_id = u.id;

-- RECURSIVE CTE — for hierarchical / graph data
WITH RECURSIVE org_chart AS (
  -- Base case: top-level employees (no manager)
  SELECT id, name, manager_id, 1 AS depth, name::TEXT AS path
  FROM employees
  WHERE manager_id IS NULL

  UNION ALL

  -- Recursive case: employees who report to someone in the CTE
  SELECT e.id, e.name, e.manager_id, oc.depth + 1, oc.path || ' > ' || e.name
  FROM employees e
  JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT id, name, depth, path FROM org_chart ORDER BY path;

-- RECURSIVE CTE for number series
WITH RECURSIVE series AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM series WHERE n < 10
)
SELECT n FROM series;

-- CTE MATERIALIZATION (PostgreSQL 12+)
-- By default, CTEs are optimization fences (materialized once).
-- In PG12+, simple CTEs may be inlined (treated like subqueries).
-- Force materialization:
WITH expensive_query AS MATERIALIZED (
  SELECT ...
)
-- Force inlining (allow optimizer to merge with outer query):
WITH simple_cte AS NOT MATERIALIZED (
  SELECT ...
)

-- KEY INSIGHT: Recursive CTEs are the standard way to query tree/graph
-- data in SQL (org charts, categories, file systems, social graphs).
```

---

## Chapter 8: Window Functions

### 8.1 What Are Window Functions?

Window functions compute values across a set of rows **related to the current row**, without collapsing them into groups. They're the most powerful feature in SQL for analytics.

```
GROUP BY collapses:             Window function does NOT collapse:
┌────┬─────┬────────┐           ┌────┬─────┬────────┬───────────┐
│ id │ dept│ salary │           │ id │ dept│ salary │ dept_avg  │
├────┼─────┼────────┤           ├────┼─────┼────────┼───────────┤
│  1 │  A  │  70000 │           │  1 │  A  │  70000 │   75000   │
│  2 │  A  │  80000 │  GROUP BY │  2 │  A  │  80000 │   75000   │
│  3 │  B  │  60000 │ ────────▶ │  3 │  B  │  60000 │   65000   │
│  4 │  B  │  70000 │           │  4 │  B  │  70000 │   65000   │
└────┴─────┴────────┘           └────┴─────┴────────┴───────────┘
Returns 2 rows (one per dept)   Returns 4 rows (all rows kept)
```

### 8.2 Window Function Syntax

```sql
function_name() OVER (
  PARTITION BY col1, col2    -- divide rows into groups (like GROUP BY but rows kept)
  ORDER BY col3              -- order within the partition
  frame_clause               -- which rows to include in the frame
)

-- FRAME CLAUSE (optional, only meaningful for some functions):
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW   -- all rows from start to current
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING           -- sliding window of 3 rows
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING -- all rows in partition

-- Default frame when ORDER BY present:
-- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

### 8.3 Ranking Functions

```sql
SELECT
  name, department, salary,

  -- ROW_NUMBER: unique sequential number (no ties)
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,

  -- RANK: same rank for ties, gaps after ties (1,1,3,4)
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,

  -- DENSE_RANK: same rank for ties, NO gaps (1,1,2,3)
  DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,

  -- NTILE: divide into N equal buckets
  NTILE(4) OVER (ORDER BY salary DESC) AS quartile,

  -- PERCENT_RANK: relative rank 0 to 1
  PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank,

  -- CUME_DIST: cumulative distribution (what % earn ≤ this)
  CUME_DIST() OVER (ORDER BY salary) AS cume_dist

FROM employees;

-- PRACTICAL: Get top-1 employee per department
SELECT * FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
) ranked
WHERE rn = 1;
```

### 8.4 Offset Functions

```sql
SELECT
  date, value,

  -- LAG: value from N rows before current row
  LAG(value, 1) OVER (ORDER BY date) AS prev_day,
  LAG(value, 1, 0) OVER (ORDER BY date) AS prev_day_default_0,

  -- LEAD: value from N rows after current row
  LEAD(value, 1) OVER (ORDER BY date) AS next_day,

  -- FIRST_VALUE / LAST_VALUE: first/last in the window frame
  FIRST_VALUE(value) OVER (PARTITION BY month ORDER BY date) AS month_start_value,
  LAST_VALUE(value) OVER (
    PARTITION BY month ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- must extend frame!
  ) AS month_end_value,

  -- NTH_VALUE: value at position N in window
  NTH_VALUE(value, 2) OVER (PARTITION BY month ORDER BY date) AS second_value

FROM daily_metrics;

-- Day-over-day change:
SELECT date, value,
  value - LAG(value) OVER (ORDER BY date) AS daily_change,
  ROUND(100.0 * (value - LAG(value) OVER (ORDER BY date)) /
    NULLIF(LAG(value) OVER (ORDER BY date), 0), 2) AS pct_change
FROM daily_metrics;
```

### 8.5 Aggregate Window Functions

```sql
-- Any aggregate function can be a window function with OVER()
SELECT
  date, region, sales,

  -- Running total (cumulative sum)
  SUM(sales) OVER (PARTITION BY region ORDER BY date) AS running_total,

  -- Moving average (7-day)
  AVG(sales) OVER (
    PARTITION BY region ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d,

  -- Percentage of total
  sales / SUM(sales) OVER (PARTITION BY region) * 100 AS pct_of_region,

  -- Running count
  COUNT(*) OVER (PARTITION BY region ORDER BY date) AS running_count

FROM daily_sales;

-- NAMED WINDOWS — reuse the same window definition
SELECT
  name, salary,
  AVG(salary) OVER w AS dept_avg,
  MAX(salary) OVER w AS dept_max,
  MIN(salary) OVER w AS dept_min
FROM employees
WINDOW w AS (PARTITION BY department_id);
```

---

# PART II — POSTGRESQL INTERNALS

---

## Chapter 9: Indexes

### 9.1 Why Indexes Exist

```
WITHOUT INDEX:                    WITH INDEX (B-Tree on email):
SELECT * FROM users               Query finds the B-Tree leaf node
WHERE email = 'x@y.com';         directly → jumps to the exact page
                                  
Sequential scan:                  Index scan:
Read ALL pages (e.g. 10,000)     Read ~3-4 pages (tree height)
O(N) where N = table pages       O(log N)

RULE OF THUMB:
- Table < 1000 rows → sequential scan may be faster than index
- Table > 10,000 rows + selective query → index almost always helps
- Cardinality matters: an index on a boolean column (2 values) is
  useless for most queries — the planner will ignore it
```

### 9.2 B-Tree Index (Default)

```sql
-- Default index type — use for: =, <, >, <=, >=, BETWEEN, IN, LIKE 'prefix%'
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at DESC);  -- direction matters for ORDER BY

-- COMPOSITE INDEX — column order is critical
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- This index supports:
--   WHERE user_id = 5                         ✓ (leftmost prefix)
--   WHERE user_id = 5 AND status = 'active'   ✓ (full index)
--   WHERE status = 'active'                   ✗ (not leftmost — index not used)

-- RULE: A composite index (A, B) can be used for queries filtering on:
--   A alone, or A+B together, but NOT B alone.

-- COVERING INDEX (INCLUDE) — store extra columns in index leaf node
-- Avoids heap fetch ("index-only scan")
CREATE INDEX idx_orders_covering ON orders(user_id)
  INCLUDE (total, status, created_at);
-- Query: SELECT total, status FROM orders WHERE user_id = 5
-- Can be satisfied entirely from the index — no heap access!

-- UNIQUE INDEX
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- B-Tree supports: =, <, >, <=, >=, BETWEEN, IN, LIKE 'foo%' (prefix only)
-- B-Tree does NOT support: LIKE '%foo', LIKE '%foo%' (use pg_trgm + GIN for that)
```

### 9.3 Partial Index

```sql
-- Index only rows matching a condition — smaller, faster
-- Best when your queries always include that condition

-- Only index active users
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
-- Supports: WHERE email = 'x@y.com' AND status = 'active'
-- Does NOT help: WHERE email = 'x@y.com' (without status = 'active')

-- Only index non-null values
CREATE INDEX idx_orders_external_id ON orders(external_id)
WHERE external_id IS NOT NULL;

-- Index soft-deleted-aware unique constraint
CREATE UNIQUE INDEX idx_users_email_unique_active
ON users(email) WHERE deleted_at IS NULL;
-- Allows multiple rows with same email if deleted, enforces uniqueness for active
```

### 9.4 Expression Index (Functional Index)

```sql
-- Index the result of a function or expression
-- The query WHERE clause must use the exact same expression

-- Case-insensitive search
CREATE INDEX idx_users_email_lower ON users(lower(email));
-- Query must use: WHERE lower(email) = 'x@y.com'

-- Extract from date
CREATE INDEX idx_orders_year ON orders(EXTRACT(year FROM created_at));
-- Query: WHERE EXTRACT(year FROM created_at) = 2024

-- JSONB field
CREATE INDEX idx_users_metadata_country ON users((metadata->>'country'));

-- KEY INSIGHT: PostgreSQL cannot use idx_users_email_lower if the query says
-- WHERE email = 'X@Y.COM' — the expression must match exactly.
```

### 9.5 GIN Index (Generalized Inverted Index)

```sql
-- Best for: full-text search, JSONB, array containment (@>, <@, &&)
-- Structure: maps each element → set of row IDs containing it

-- JSONB queries
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);
-- Supports: WHERE attributes @> '{"color": "red"}'
-- Supports: WHERE attributes ? 'color'

-- Array queries
CREATE INDEX idx_articles_tags ON articles USING GIN(tags);
-- Supports: WHERE tags @> ARRAY['sql']
-- Supports: WHERE tags && ARRAY['sql', 'database']

-- Full-text search
CREATE INDEX idx_articles_fts ON articles USING GIN(to_tsvector('english', content));
-- Supports: WHERE to_tsvector('english', content) @@ to_tsquery('postgres')

-- pg_trgm — trigram index for LIKE '%pattern%'
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING GIN(name gin_trgm_ops);
-- Now supports: WHERE name LIKE '%alice%'
-- Also supports: WHERE name % 'alice' (fuzzy similarity)

-- GIN is slower to build and update but very fast to query for set containment
-- GIN FASTUPDATE: batches index updates for better write performance
```

### 9.6 Other Index Types

```sql
-- HASH INDEX
-- Only supports =, not ranges. Smaller than B-Tree for equality-only queries.
CREATE INDEX idx_sessions_token ON sessions USING HASH(token);

-- GiST (Generalized Search Tree)
-- For: geometric types, ranges, nearest-neighbor (KNN), PostGIS
CREATE INDEX idx_locations_geo ON locations USING GIST(coordinates);
CREATE INDEX idx_bookings_range ON bookings USING GIST(during); -- TSTZRANGE

-- BRIN (Block Range INdex)
-- Stores min/max per block range. Tiny index, for naturally ordered data.
-- Best: time-series tables where data is inserted in timestamp order
CREATE INDEX idx_events_created_brin ON events USING BRIN(created_at);
-- Tiny index (~100x smaller than B-Tree), good for huge time-series tables
-- Trades query performance for dramatically smaller index size

-- SP-GiST (Space-Partitioned GiST)
-- For: non-balanced tree structures, point data, prefix matching
CREATE INDEX idx_ips_spgist ON ip_addresses USING SPGIST(ip);
```

### 9.7 Index Internals & Maintenance

```sql
-- Check index usage
SELECT
  schemaname, tablename, indexname,
  idx_scan,    -- how many times this index was used
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan;

-- Find unused indexes (candidates for removal)
SELECT indexrelid::regclass, relid::regclass, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND NOT indisprimary
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index bloat — indexes accumulate dead versions from MVCC
-- REINDEX: rebuilds from scratch (locks table in older PG)
REINDEX INDEX CONCURRENTLY idx_users_email;  -- PG12+, no lock

-- VACUUM removes dead tuples, allowing index entries to be reclaimed
-- But index structure may still be bloated → REINDEX periodically

-- Check table and index sizes
SELECT
  relname,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  pg_size_pretty(pg_indexes_size(relid)) AS indexes_size,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

---

## Chapter 10: Query Planner & EXPLAIN ANALYZE

### 10.1 How the Planner Works

```
Table statistics collected by ANALYZE:
  pg_statistic: column distinct values, histogram, correlation
  pg_class: row count estimates (reltuples)

Planner estimates:
  - How many rows will each filter return?
  - Which join order is cheapest?
  - Which join algorithm? (Nested Loop / Hash / Merge)
  - Should I use an index? Seq scan might be cheaper for large result sets.
  - Will an index-only scan work? (INCLUDE columns)

Cost model:
  seq_page_cost = 1.0 (baseline)
  random_page_cost = 4.0 (disk random access is 4x more expensive)
  cpu_tuple_cost = 0.01
  cpu_index_tuple_cost = 0.005
  cpu_operator_cost = 0.0025
  
  On SSDs, set random_page_cost = 1.1 to reflect faster random I/O
```

### 10.2 EXPLAIN ANALYZE — Reading the Output

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name;

-- Sample output:
HashAggregate  (cost=1245.30..1345.30 rows=10000 width=36)
               (actual time=52.3..54.1 rows=8542 loops=1)
  Buffers: shared hit=342 read=891
  ->  Hash Join  (cost=340.00..1195.30 rows=50000 width=28)
                 (actual time=12.1..44.2 rows=48203 loops=1)
        Hash Cond: (o.user_id = u.id)
        Buffers: shared hit=342 read=891
        ->  Seq Scan on orders o  (cost=0..220.00 rows=60000 width=12)
                                  (actual time=0.1..8.2 rows=60000 loops=1)
        ->  Hash  (cost=215.00..215.00 rows=10000 width=20)
                  (actual time=11.8..11.8 rows=10000 loops=1)
              Buckets: 16384  Batches: 1  Memory Usage: 624kB
              ->  Seq Scan on users u  (cost=0..215.00 rows=10000 width=20)
                                       (actual time=0.1..6.1 rows=10000 loops=1)
                    Filter: (status = 'active')
                    Rows Removed by Filter: 2500
Planning Time: 1.2 ms
Execution Time: 54.8 ms

READING THIS:
  cost=X..Y     → X = startup cost, Y = total cost (planner estimates)
  rows=N        → planner's row estimate
  actual time=X..Y → real time (ms): startup..total
  actual rows=N → real row count (compare to estimate — big gaps = stale stats)
  loops=N       → node executed N times (nested loop inner side)
  
  Buffers: shared hit=N  → pages from shared_buffers (cache)
           shared read=N → pages read from disk

RED FLAGS in EXPLAIN output:
  - actual rows >> estimated rows → run ANALYZE
  - loops=N on expensive node → nested loop performance problem
  - Seq Scan on huge table without filter → missing index
  - Hash Batches > 1 → hash table spilled to disk → increase work_mem
  - Sort on large dataset → increase work_mem or add index for sort column
```

### 10.3 EXPLAIN Options & Planner Hints

```sql
-- Just the plan, no execution
EXPLAIN SELECT * FROM users;

-- Execute and show actual stats
EXPLAIN ANALYZE SELECT * FROM users;

-- Include buffer usage (essential for performance work)
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users;

-- JSON format (easier to parse programmatically)
EXPLAIN (ANALYZE, FORMAT JSON) SELECT * FROM users;

-- Force or disable specific strategies (for debugging only):
SET enable_seqscan = off;      -- force index scans
SET enable_hashjoin = off;     -- force other join types
SET enable_nestloop = off;
-- ALWAYS reset after: SET enable_seqscan = on;
-- Never set these permanently in production

-- Update statistics manually
ANALYZE users;
ANALYZE;  -- analyze all tables

-- Increase statistics target for columns with bad estimates
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
-- Default is 100. Higher = better estimates, more ANALYZE time.
```

---

## Chapter 11: MVCC — Multi-Version Concurrency Control

### 11.1 The Core Idea

```
MVCC = every transaction sees a SNAPSHOT of the database.
Writers don't block readers. Readers don't block writers.

How it works:
  Each row tuple has:
    xmin = transaction ID that created this version
    xmax = transaction ID that deleted/updated this version (or 0 if still live)

  When you UPDATE a row, PostgreSQL:
    1. Marks old row: xmax = current transaction ID
    2. Inserts NEW row: xmin = current transaction ID

  When you read, you see all rows where:
    xmin < your snapshot transaction ID (created before you started)
    xmax = 0 OR xmax > your snapshot ID (not yet deleted from your perspective)

EXAMPLE:
  TXN 100 inserts row: xmin=100, xmax=0  (Alice)
  TXN 200 reads → sees Alice (xmin=100 < 200, xmax=0)
  TXN 300 updates Alice → Bob:
    Old row: xmin=100, xmax=300
    New row: xmin=300, xmax=0
  TXN 200 still sees Alice (xmax=300 > 200 → not deleted from 200's perspective)
  TXN 400 reads → sees Bob (xmin=300 < 400, xmax=0)
```

### 11.2 Dead Tuples and VACUUM

```
The MVCC model means old row versions accumulate on disk.
These are called "dead tuples" — no longer visible to any transaction.

VACUUM:
  - Scans the table for dead tuples
  - Marks their space as reusable (doesn't return space to OS by default)
  - Updates visibility map (for index-only scans)
  - Updates free space map
  - Prevents transaction ID wraparound (critical!)

VACUUM FULL:
  - Rewrites the entire table (removes bloat, returns space to OS)
  - Requires an exclusive lock — blocks all queries
  - Use only when absolutely needed (e.g., massive deletes)
  - Prefer pg_repack extension for online table rewrites

AUTOVACUUM:
  Runs automatically based on:
    autovacuum_vacuum_threshold = 50       (min dead tuples before trigger)
    autovacuum_vacuum_scale_factor = 0.2   (20% of table size)
  Trigger when: dead_tuples > threshold + scale_factor * table_rows

-- Manually trigger vacuum
VACUUM users;           -- non-blocking cleanup
VACUUM ANALYZE users;  -- vacuum + update stats
VACUUM VERBOSE users;  -- verbose output

-- Check dead tuple count
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC;
```

### 11.3 Transaction ID Wraparound

```
PostgreSQL uses 32-bit transaction IDs (XID). That's ~2.1 billion.
After 2.1B transactions, XID wraps around to 0.

If this happens: EVERY existing row would appear to be in the future
→ invisible → catastrophic data loss.

PREVENTION:
  Autovacuum runs "anti-wraparound" vacuums before this point.
  PostgreSQL starts warning at 40M transactions before wraparound.
  At 3M transactions before: goes into read-only mode (emergency).

Monitor this:
SELECT datname, age(datfrozenxid) AS xid_age
FROM pg_database ORDER BY xid_age DESC;
-- age > 1.5 billion is a serious warning sign

Modern PostgreSQL (14+) uses 64-bit XIDs internally (xl_extended_xid)
but still maintains compatibility with 32-bit xmin/xmax in tuples.
```

---

## Chapter 12: Transactions, Isolation Levels & Locking

### 12.1 Transaction Basics

```sql
BEGIN;                          -- start transaction
-- ... SQL statements ...
COMMIT;                         -- save all changes atomically

BEGIN;
-- ... SQL statements ...
ROLLBACK;                       -- undo all changes

SAVEPOINT my_savepoint;         -- create a rollback point within a transaction
ROLLBACK TO SAVEPOINT my_savepoint;  -- roll back to savepoint (partial rollback)
RELEASE SAVEPOINT my_savepoint;     -- discard the savepoint

-- ACID properties:
-- Atomicity: all statements succeed or all fail
-- Consistency: database invariants (constraints) always hold
-- Isolation: concurrent transactions don't interfere
-- Durability: committed data survives crashes (WAL + fsync)
```

### 12.2 Isolation Levels

```
                     DIRTY    NON-REPEATABLE  PHANTOM
ISOLATION LEVEL      READ     READ            READ
──────────────────────────────────────────────────────
READ UNCOMMITTED     ✓ can    ✓ can           ✓ can
(not in PG)         occur    occur           occur

READ COMMITTED       ✗ no     ✓ can           ✓ can    ← PG DEFAULT
                             occur           occur

REPEATABLE READ      ✗ no     ✗ no            ✓ can
                                             occur (PG: also no)

SERIALIZABLE         ✗ no     ✗ no            ✗ no
──────────────────────────────────────────────────────

DIRTY READ: reading uncommitted data from another transaction
NON-REPEATABLE READ: same row reads return different values in same txn
PHANTOM READ: same query returns different ROWS (new rows appeared)

PostgreSQL specifics:
  - READ UNCOMMITTED = READ COMMITTED in PostgreSQL (never dirty reads)
  - REPEATABLE READ prevents phantom reads too (stronger than SQL standard)
  - SERIALIZABLE uses SSI (Serializable Snapshot Isolation) — 
    detects and aborts conflicting transactions, no locking needed

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- or:
BEGIN ISOLATION LEVEL SERIALIZABLE;
```

### 12.3 Locking

```sql
-- TABLE LOCKS (explicit)
LOCK TABLE users IN ACCESS SHARE MODE;       -- allows reads, blocks writes
LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE users IN EXCLUSIVE MODE;          -- blocks everything except reads
LOCK TABLE users IN ACCESS EXCLUSIVE MODE;   -- blocks everything (DDL default)

-- ROW LOCKS (explicit, within a transaction)
SELECT * FROM users WHERE id = 1 FOR UPDATE;        -- exclusive row lock
SELECT * FROM users WHERE id = 1 FOR SHARE;         -- shared row lock
SELECT * FROM users WHERE id = 1 FOR UPDATE SKIP LOCKED;  -- skip locked rows
SELECT * FROM users WHERE id = 1 FOR UPDATE NOWAIT;  -- fail immediately if locked

-- FOR UPDATE SKIP LOCKED pattern — job queue
BEGIN;
SELECT id, payload FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;
-- process the job...
UPDATE jobs SET status = 'done' WHERE id = $1;
COMMIT;

-- ADVISORY LOCKS — application-level locks
-- Useful for distributed coordination
SELECT pg_advisory_lock(12345);        -- session-level, blocks until acquired
SELECT pg_advisory_xact_lock(12345);   -- transaction-level, auto-released
SELECT pg_try_advisory_lock(12345);    -- non-blocking, returns boolean

-- Monitor locks
SELECT pid, relation::regclass, mode, granted
FROM pg_locks
WHERE NOT granted;  -- show waiting locks

-- Identify blocking queries
SELECT
  blocked.pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
```

---

# PART III — ADVANCED POSTGRESQL

---

## Chapter 13: Functions, Stored Procedures & Triggers

### 13.1 Functions (PL/pgSQL)

```sql
-- Basic function
CREATE OR REPLACE FUNCTION get_user_orders(p_user_id BIGINT)
RETURNS TABLE(order_id BIGINT, total NUMERIC, created_at TIMESTAMPTZ)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT o.id, o.total, o.created_at
  FROM orders o
  WHERE o.user_id = p_user_id
  ORDER BY o.created_at DESC;
END;
$$;

-- Call it:
SELECT * FROM get_user_orders(42);

-- Function with OUT parameters
CREATE OR REPLACE FUNCTION transfer_funds(
  p_from_account INT,
  p_to_account INT,
  p_amount NUMERIC,
  OUT success BOOLEAN,
  OUT message TEXT
) LANGUAGE plpgsql AS $$
DECLARE
  v_balance NUMERIC;
BEGIN
  -- Get current balance (with row lock)
  SELECT balance INTO v_balance FROM accounts WHERE id = p_from_account FOR UPDATE;

  IF v_balance < p_amount THEN
    success := false;
    message := 'Insufficient funds';
    RETURN;
  END IF;

  UPDATE accounts SET balance = balance - p_amount WHERE id = p_from_account;
  UPDATE accounts SET balance = balance + p_amount WHERE id = p_to_account;

  success := true;
  message := 'Transfer successful';
END;
$$;

-- FUNCTION VOLATILITY — affects optimization and caching
CREATE FUNCTION get_pi() RETURNS FLOAT LANGUAGE sql IMMUTABLE AS $$
  SELECT 3.14159265358979;
$$;
-- IMMUTABLE: same inputs always → same output. Can be cached. Can be used in indexes.
-- STABLE: same inputs within a query → same output. Can be used by planner.
-- VOLATILE: may return different values (default). NOW() is VOLATILE.
```

### 13.2 Stored Procedures (PG 11+)

```sql
-- Procedures can COMMIT/ROLLBACK inside them (functions cannot)
CREATE OR REPLACE PROCEDURE batch_process_orders()
LANGUAGE plpgsql AS $$
DECLARE
  batch_size INT := 1000;
  processed INT := 0;
BEGIN
  LOOP
    UPDATE orders
    SET status = 'processed'
    WHERE id IN (
      SELECT id FROM orders WHERE status = 'pending'
      LIMIT batch_size FOR UPDATE SKIP LOCKED
    );

    GET DIAGNOSTICS processed = ROW_COUNT;
    EXIT WHEN processed = 0;

    COMMIT;  -- commit each batch (can't do this in a function)
    PERFORM pg_sleep(0.1);  -- be kind to the system
  END LOOP;
END;
$$;

CALL batch_process_orders();
```

### 13.3 Triggers

```sql
-- Trigger function must return TRIGGER type
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := NOW();
  RETURN NEW;  -- return modified row (for BEFORE trigger)
END;
$$;

-- Create trigger
CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Audit trail trigger
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    INSERT INTO audit_log(table_name, operation, old_data, changed_at)
    VALUES (TG_TABLE_NAME, 'DELETE', row_to_json(OLD), NOW());
    RETURN OLD;
  ELSE
    INSERT INTO audit_log(table_name, operation, old_data, new_data, changed_at)
    VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW), NOW());
    RETURN NEW;
  END IF;
END;
$$;

CREATE TRIGGER users_audit
  AFTER INSERT OR UPDATE OR DELETE ON users
  FOR EACH ROW EXECUTE FUNCTION audit_changes();

-- Trigger special variables:
-- TG_OP: 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE'
-- TG_TABLE_NAME: name of the table
-- TG_WHEN: 'BEFORE', 'AFTER', 'INSTEAD OF'
-- NEW: new row data (INSERT/UPDATE)
-- OLD: old row data (UPDATE/DELETE)
-- RETURN NEW: use modified row (BEFORE trigger)
-- RETURN NULL: cancel the operation (BEFORE trigger)
```

---

## Chapter 14: JSONB & Arrays

### 14.1 JSONB vs JSON

```
JSON:   stores exact text representation (whitespace preserved)
JSONB:  stores binary, parsed representation

JSONB advantages over JSON:
  - Faster to query (no re-parsing)
  - Supports GIN indexing
  - Supports all JSON operators (@>, ?, etc.)
  - Removes duplicate keys, orders keys
  
Use JSONB always, unless you need to preserve exact formatting/key order.
```

### 14.2 JSONB Operators & Functions

```sql
-- Setup
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT,
  attributes JSONB
);

INSERT INTO products VALUES
  (1, 'T-Shirt', '{"color": "red", "size": "M", "tags": ["cotton","casual"], "price": 29.99}'),
  (2, 'Jeans', '{"color": "blue", "size": "L", "tags": ["denim"], "price": 79.99}');

-- ACCESS OPERATORS
SELECT attributes->'color' FROM products;          -- returns JSON: "red"
SELECT attributes->>'color' FROM products;         -- returns TEXT: red
SELECT attributes->'tags'->0 FROM products;        -- first element of array: "cotton"
SELECT attributes#>'{tags,0}' FROM products;       -- path: JSON
SELECT attributes#>>'{tags,0}' FROM products;      -- path: TEXT

-- CONTAINMENT OPERATORS
SELECT * FROM products WHERE attributes @> '{"color": "red"}'; -- contains
SELECT * FROM products WHERE '{"color": "red"}' <@ attributes; -- is contained by

-- EXISTENCE OPERATORS
SELECT * FROM products WHERE attributes ? 'color';             -- has key
SELECT * FROM products WHERE attributes ?| ARRAY['color', 'size']; -- has any key
SELECT * FROM products WHERE attributes ?& ARRAY['color', 'size']; -- has all keys

-- MODIFICATION FUNCTIONS
UPDATE products
SET attributes = attributes || '{"in_stock": true}'          -- merge/overwrite
WHERE id = 1;

UPDATE products
SET attributes = attributes - 'tags'                          -- remove key
WHERE id = 1;

UPDATE products
SET attributes = jsonb_set(attributes, '{price}', '39.99')   -- set nested value
WHERE id = 1;

UPDATE products
SET attributes = jsonb_set(attributes, '{tags,0}', '"premium"') -- set array element
WHERE id = 1;

-- QUERYING JSONB ARRAYS
SELECT * FROM products WHERE attributes->'tags' @> '["cotton"]';
SELECT * FROM products, jsonb_array_elements_text(attributes->'tags') AS tag
WHERE tag = 'cotton';

-- AGGREGATING JSONB
SELECT jsonb_agg(attributes) FROM products;            -- array of JSONB objects
SELECT jsonb_object_agg(name, attributes) FROM products; -- object keyed by name

-- INDEX for JSONB
CREATE INDEX idx_products_attrs ON products USING GIN(attributes);
-- Supports: @>, ?, ?|, ?&
CREATE INDEX idx_products_color ON products((attributes->>'color'));
-- Supports: WHERE attributes->>'color' = 'red' (equality on specific key)
```

---

## Chapter 15: Full-Text Search

### 15.1 Core Concepts

```sql
-- tsvector: processed document (lexemes, positions)
SELECT to_tsvector('english', 'The quick brown fox jumps over the lazy dog');
-- Result: 'brown':3 'dog':9 'fox':4 'jump':5 'lazi':8 'quick':2
-- Stop words removed (the, over), stemmed (jumps→jump, lazy→lazi)

-- tsquery: search query
SELECT to_tsquery('english', 'jump & fox');     -- AND
SELECT to_tsquery('english', 'jump | fox');     -- OR
SELECT to_tsquery('english', '!fox');           -- NOT
SELECT to_tsquery('english', 'jump <-> fox');   -- FOLLOWED BY
SELECT plainto_tsquery('english', 'quick fox'); -- auto AND
SELECT websearch_to_tsquery('english', '"quick fox" OR dog'); -- web-style

-- MATCH OPERATOR
SELECT to_tsvector('english', 'The quick brown fox') @@ to_tsquery('english', 'fox');
-- Returns true

-- Full example
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  fts_vector TSVECTOR GENERATED ALWAYS AS (
    setweight(to_tsvector('english', title), 'A') ||
    setweight(to_tsvector('english', body), 'B')
  ) STORED
);

CREATE INDEX idx_articles_fts ON articles USING GIN(fts_vector);

-- Search query
SELECT id, title,
  ts_rank(fts_vector, query) AS rank,
  ts_headline('english', body, query, 'MaxWords=20,MinWords=10') AS snippet
FROM articles,
     to_tsquery('english', 'postgresql & performance') AS query
WHERE fts_vector @@ query
ORDER BY rank DESC
LIMIT 10;
```

---

## Chapter 16: Table Partitioning

### 16.1 Why Partition?

```
Problems partitioning solves:
  - Table too large for queries to be fast (billions of rows)
  - Old data can be dropped instantly (DROP PARTITION = no VACUUM needed)
  - Partition pruning: query only touches relevant partitions
  - Index maintenance: smaller indexes per partition

PARTITION TYPES:
  RANGE  → based on value ranges (date ranges, ID ranges)
  LIST   → based on explicit value lists (country, status)
  HASH   → based on hash of column value (even distribution)
```

### 16.2 Range Partitioning

```sql
-- Parent table (no data stored here)
CREATE TABLE orders (
  id BIGINT NOT NULL,
  user_id BIGINT,
  total NUMERIC(10,2),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create partitions for each month
CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Default partition (catches anything not matched)
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Each partition can have its own indexes
CREATE INDEX ON orders_2024_01 (user_id);
CREATE INDEX ON orders_2024_02 (user_id);

-- Queries automatically go to the right partition (partition pruning)
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01';
-- Only scans orders_2024_01 — other partitions excluded

-- Instant partition drop (vs DELETE + VACUUM on full table)
DROP TABLE orders_2024_01;

-- Detach partition (keeps data, removes from partitioned table)
ALTER TABLE orders DETACH PARTITION orders_2024_01;
```

---

## Chapter 17: Replication & High Availability

### 17.1 Streaming Replication

```
PRIMARY                           STANDBY (replica)
  │                                    │
  │  WAL Writer flushes WAL to disk    │
  │                                    │
  │──── WAL Sender ─────────────────▶ WAL Receiver
  │     (background process)           │
  │     sends WAL stream               ▼
  │                              WAL files on disk
  │                                    │
  │                              Startup process
  │                              replays WAL
  │                              (physical copy of primary)

SYNCHRONOUS vs ASYNCHRONOUS:
  Async (default):
    Primary commits without waiting for standby acknowledgment.
    Best performance, risk of data loss if primary crashes.

  Synchronous:
    Primary waits for at least one standby to confirm WAL received.
    synchronous_commit = on (wait for WAL written to standby disk)
    synchronous_commit = remote_apply (wait for standby to apply WAL)
    No data loss on failover. Latency impact on writes.

SETUP on primary (postgresql.conf):
  wal_level = replica
  max_wal_senders = 10
  wal_keep_size = 1GB

SETUP on standby:
  # postgresql.conf:
  hot_standby = on   # allow read queries on standby

  # pg_hba.conf on primary — allow replication connections
  host replication replicator standby_ip/32 md5

  # Run on standby to start replication:
  pg_basebackup -h primary_host -U replicator -D /var/lib/postgresql/data -P -Xs -R
```

### 17.2 Logical Replication

```sql
-- Logical replication: replicate at the row level (not WAL blocks)
-- Allows: selective table replication, cross-version replication, filtering

-- On PRIMARY: create publication
CREATE PUBLICATION my_pub FOR TABLE users, orders;
-- Or all tables:
CREATE PUBLICATION all_tables FOR ALL TABLES;

-- On STANDBY/SUBSCRIBER: create subscription
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=primary_host dbname=mydb user=replicator'
  PUBLICATION my_pub;

-- Use cases:
-- - Replicate to different PostgreSQL version
-- - Replicate specific tables to analytics database
-- - Zero-downtime major version upgrades
-- - Data pipelines (Debezium uses logical replication)
```

---

## Chapter 18: Performance Tuning — Production Playbook

### 18.1 Key Configuration Parameters

```ini
# postgresql.conf — essential tunings

# Memory
shared_buffers = 25% of RAM              # PostgreSQL's cache — most important
effective_cache_size = 75% of RAM        # hint to planner (total cache incl. OS)
work_mem = RAM / (max_connections * 2)   # per-sort/hash operation, NOT per query!
maintenance_work_mem = 512MB             # for VACUUM, CREATE INDEX, etc.

# WAL / Durability
wal_level = replica          # needed for replication
synchronous_commit = on      # durability; set to 'off' for speed (risk data loss)
checkpoint_completion_target = 0.9   # spread checkpoint I/O over 90% of interval
wal_buffers = 64MB           # WAL buffer size

# Query planner
random_page_cost = 1.1       # for SSD; default 4.0 is for spinning disk
effective_io_concurrency = 200  # for SSD parallel I/O
default_statistics_target = 100  # increase for better estimates (up to 500)

# Connections
max_connections = 100        # use PgBouncer for high connection counts
```

### 18.2 Query Performance Checklist

```
1. Check slow query log:
   log_min_duration_statement = 1000  # log queries > 1 second

2. pg_stat_statements extension — aggregate query stats
   CREATE EXTENSION pg_stat_statements;
   SELECT query, calls, mean_exec_time, total_exec_time, rows
   FROM pg_stat_statements
   ORDER BY total_exec_time DESC
   LIMIT 20;

3. EXPLAIN ANALYZE the slow queries
   Look for: Seq Scan on large tables, bad row estimates, hash batches > 1

4. Add missing indexes
   Check pg_stat_user_indexes for unused indexes (remove them)
   Check pg_stat_user_tables for high seq_scan counts (add indexes)

5. Vacuum health
   SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables
   WHERE n_dead_tup > 10000;

6. Connection pooling
   Use PgBouncer in transaction mode for OLTP workloads
   Avoid max_connections > 200 (memory + context switch overhead)

7. Partitioning for large tables
   Tables > 100M rows benefit from range/hash partitioning

8. N+1 query detection
   1 query to get list + N queries for each item
   Fix with JOIN or array/id IN (...) batch query
```

---

## Chapter 19: Schema Design & Normalization

### 19.1 Normal Forms

```
FIRST NORMAL FORM (1NF):
  - Each column contains atomic (indivisible) values
  - No repeating groups / arrays of values in a column
  VIOLATION: tags = "sql,postgres,database" in one TEXT column
  FIX: separate tags table with foreign key

SECOND NORMAL FORM (2NF):
  - Must be 1NF
  - Every non-key column depends on the WHOLE primary key
  VIOLATION: order_items(order_id, product_id, product_name)
    product_name depends on product_id alone, not (order_id, product_id)
  FIX: product_name belongs in products table

THIRD NORMAL FORM (3NF):
  - Must be 2NF
  - No transitive dependencies (non-key column depending on another non-key)
  VIOLATION: employees(id, dept_id, dept_name)
    dept_name depends on dept_id, which depends on id
  FIX: departments table; employees references dept_id only

BOYCE-CODD NORMAL FORM (BCNF):
  - Stricter than 3NF
  - Every determinant must be a candidate key
  - Most schemas that satisfy 3NF also satisfy BCNF

DENORMALIZATION:
  Sometimes INTENTIONAL violation for performance:
  - Store product_name in order_items (snapshot at time of order)
  - Store order_count in users (avoid expensive COUNT on every request)
  - Materialized views for pre-computed aggregates
  Always document WHY you denormalized and maintain consistency.
```

### 19.2 Production Schema Patterns

```sql
-- SOFT DELETE pattern
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX ON users(deleted_at) WHERE deleted_at IS NOT NULL;
-- All queries need WHERE deleted_at IS NULL (use Row Level Security or views)

-- AUDIT TABLE pattern
CREATE TABLE audit_log (
  id BIGSERIAL PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id BIGINT NOT NULL,
  operation TEXT NOT NULL,  -- INSERT/UPDATE/DELETE
  changed_by BIGINT REFERENCES users(id),
  old_values JSONB,
  new_values JSONB,
  changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- POLYMORPHIC ASSOCIATION (avoid if possible, use with care)
-- Bad: one table that references multiple other tables
CREATE TABLE comments (
  id BIGSERIAL PRIMARY KEY,
  commentable_type TEXT,  -- 'Article' or 'Product'
  commentable_id BIGINT,
  body TEXT
);
-- Problems: no FK constraint, hard to query, no referential integrity
-- Better: separate tables (article_comments, product_comments) or join table

-- OPTIMISTIC LOCKING (version column)
CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name TEXT,
  price NUMERIC(10,2),
  version INT NOT NULL DEFAULT 1
);
-- Application reads version, then:
UPDATE products SET name='New', version = version + 1
WHERE id = $1 AND version = $read_version;
-- If 0 rows updated → someone else updated first → retry
```

---

---

## Chapter 20: Backup, Recovery & Operations

### 20.1 Logical Replication vs Physical Replication

```
PHYSICAL REPLICATION (Streaming):
  Replicates raw WAL bytes — block-level copy.
  Standby = exact byte-for-byte replica.
  Everything is replicated: all databases, all DDL, all tables.
  Standby must be same major version (or very close).
  Read-only standby only — cannot write to any table.
  WAL level required: replica

LOGICAL REPLICATION:
  Replicates decoded row-level changes (INSERT/UPDATE/DELETE).
  Selective: specific tables, specific columns (PG15+).
  Works across major PostgreSQL versions.
  Subscriber can write to other tables.
  Cannot replicate DDL or sequences directly.
  WAL level required: logical

SETUP:
  -- postgresql.conf on primary:
  wal_level = logical

  -- On primary:
  CREATE PUBLICATION my_pub FOR TABLE users, orders;

  -- On subscriber:
  CREATE SUBSCRIPTION my_sub
    CONNECTION 'host=primary dbname=mydb user=rep'
    PUBLICATION my_pub;

USE CASES:
  Physical → HA standby, read replicas, failover
  Logical  → major version upgrades, selective replication, CDC pipelines
```

### 20.2 Point-in-Time Recovery (PITR)

```
COMPONENTS:
  1. Base backup   — full snapshot of the cluster at a point in time
  2. WAL archive   — every WAL segment shipped to archive storage
  Together: restore to any moment between base backup and now.

ENABLE WAL ARCHIVING:
  # postgresql.conf
  archive_mode = on
  archive_command = 'cp %p /wal_archive/%f'
  # or: aws s3 cp %p s3://bucket/wal/%f

TAKE A BASE BACKUP:
  pg_basebackup -h localhost -U replicator -D /backups/base -Ft -z -P

RECOVERY:
  1. Stop server, restore base backup to data dir
  2. Set recovery target in postgresql.conf (PG12+):
     restore_command = 'cp /wal_archive/%f %p'
     recovery_target_time = '2024-01-15 14:32:46+00'
     recovery_target_action = 'promote'
  3. Start PostgreSQL → it replays WAL → stops at target → promotes

PRODUCTION TOOLS: pgBackRest, WAL-G (cloud-native, S3/GCS/Azure)
```

### 20.3 Connection Pooling with PgBouncer

```
WHY NEEDED:
  PostgreSQL: 1 connection = 1 OS process (~5MB RAM, ~5ms to create).
  200 app server threads × 10 pool connections each = 2000 PG connections.
  2000 × 5MB = 10GB RAM just for connection overhead. Unsustainable.
  PgBouncer maintains a small pool of real PG connections, shares them.

POOLING MODES:
  SESSION:     client holds server connection for entire session (weakest saving)
  TRANSACTION: client holds connection only during active transaction (recommended)
  STATEMENT:   connection returned after every statement (breaks multi-stmt txns)

TRANSACTION MODE LIMITATIONS:
  ✗ Session-level SET commands don't persist
  ✗ LISTEN/NOTIFY
  ✗ Prepared statements (need workaround)
  ✗ Advisory session locks

TYPICAL CONFIG:
  pool_mode = transaction
  max_client_conn = 1000     -- app connects up to 1000 times to PgBouncer
  default_pool_size = 20     -- PgBouncer holds 20 real PG connections

RESULT: 1000 app connections → 20 PostgreSQL backend processes. 98% reduction.
```

### 20.4 Backup with pg_dump / pg_restore

```
FORMATS:
  Plain (-Fp):    SQL text — restore with psql
  Custom (-Fc):   Compressed binary — restore with pg_restore (supports parallel)
  Directory (-Fd):One file per table — parallel dump AND restore
  Tar (-Ft):      Tar archive — restore with pg_restore

DUMP:
  pg_dump -h host -U user -d mydb -Fc -f mydb.dump
  pg_dump -h host -U user -d mydb -Fd -j 4 -f mydb_dir/   # parallel

RESTORE:
  pg_restore -h host -U user -d mydb_new -j 4 mydb.dump    # parallel

LAYER YOUR STRATEGY:
  1. PITR (WAL + base backup) → primary recovery, any point in time
  2. pg_dump daily → cross-version, single-table restore, offsite
  3. Logical standby → near-zero RTO failover
```

### 20.5 TOAST — Oversized Attribute Storage

```
PROBLEM: PostgreSQL rows live in 8KB pages. A single TEXT or JSONB value
can be megabytes. TOAST solves this transparently.

HOW: Values > ~2KB are moved to a separate TOAST table (pg_toast_<oid>).
The main row stores an 18-byte pointer. Completely transparent to queries.

STRATEGIES (per column):
  EXTENDED (default for TEXT/JSONB): compress first, then out-of-line
  EXTERNAL:  out-of-line immediately, no compression
  MAIN:      compress, keep inline if possible
  PLAIN:     no TOAST (for small fixed types)

COMPRESSION: pglz (default) or lz4 (PG14+, faster)
  SET default_toast_compression = 'lz4';

PERFORMANCE NOTES:
  ✓ Allows rows much larger than 8KB
  ✓ Compression reduces JSONB storage by 50-80%
  ✗ Reading a toasted column = extra random I/O to TOAST table
  ✗ Selecting wide JSONB in large result sets → heavy TOAST I/O

BEST PRACTICE: Only select the JSONB keys you need:
  SELECT attributes->>'color' FROM products;  -- reads only needed key
  -- vs: SELECT attributes FROM products;     -- fetches entire toasted blob
```

### 20.6 Automatic Partition Maintenance

```sql
-- PostgreSQL does NOT auto-create new partitions.
-- Must create future partitions before data arrives.

-- pg_partman extension (production standard):
CREATE EXTENSION pg_partman;

SELECT partman.create_parent(
  p_parent_table => 'public.events',
  p_control      => 'created_at',
  p_type         => 'native',
  p_interval     => 'monthly',
  p_premake      => 4    -- pre-create 4 months ahead
);

-- Run monthly (schedule with pg_cron):
SELECT partman.run_maintenance_proc();

-- Configure retention (drop partitions older than 12 months):
UPDATE partman.part_config
SET retention = '12 months', retention_keep_table = false
WHERE parent_table = 'public.events';

-- INSTANT DROP of old partition (no VACUUM needed):
DROP TABLE events_2023_01;  -- immediate, reclaims space instantly

-- DETACH (keep data, remove from partition set):
ALTER TABLE events DETACH PARTITION events_2023_01;
-- Then archive/dump/drop on your own schedule.
```

### 20.7 pg_repack — Online Table Rewrite

```
VACUUM FULL problem: rewrites entire table, requires ACCESS EXCLUSIVE LOCK.
On a 200GB table: hours of downtime. Unacceptable in production.

pg_repack: rebuilds table and indexes online — no blocking locks (except ~100ms at swap).

HOW:
  1. Create a new empty table (same schema)
  2. Copy existing rows in background (no lock)
  3. Trigger on original captures concurrent changes → log table
  4. Replay log onto new table
  5. Atomic swap (brief exclusive lock, < 100ms)
  6. Drop old table

USAGE:
  pg_repack -h localhost -U postgres -d mydb -t users
  pg_repack -h localhost -U postgres -d mydb           -- all tables
  pg_repack ... --only-indexes                         -- indexes only

REQUIREMENTS:
  - Table must have PRIMARY KEY or UNIQUE NOT NULL
  - Sufficient disk space for temporary copy

WHEN:
  VACUUM (autovacuum) → routine, always on
  VACUUM FULL         → only with acceptable downtime window
  pg_repack           → bloated table, production, no downtime allowed
```

---

*End of SQL & PostgreSQL Mastery Guide — Complete Edition*
