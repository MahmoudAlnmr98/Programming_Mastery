# oRPC, PostgreSQL & Drizzle ORM — Complete Reference Guide (Zero to Advanced)

> This guide assumes zero prior knowledge of any of these technologies. It covers every concept in depth — from what a database actually is, through SQL fundamentals, advanced PostgreSQL internals, Drizzle ORM patterns, and the oRPC typed API layer. Nothing is skipped.

---

## Table of Contents

1. [What is a Database? Why PostgreSQL?](#1-what-is-a-database-why-postgresql)
2. [How PostgreSQL Works Internally](#2-how-postgresql-works-internally)
3. [SQL Fundamentals — Complete Reference](#3-sql-fundamentals--complete-reference)
4. [Advanced SQL — Every Pattern You Need](#4-advanced-sql--every-pattern-you-need)
5. [Relational Data Modeling — Deep Dive](#5-relational-data-modeling--deep-dive)
6. [PostgreSQL-Specific Features](#6-postgresql-specific-features)
7. [Indexes — Complete Guide](#7-indexes--complete-guide)
8. [Transactions & Concurrency Control (MVCC)](#8-transactions--concurrency-control-mvcc)
9. [Performance Tuning & EXPLAIN ANALYZE](#9-performance-tuning--explain-analyze)
10. [Drizzle ORM — Complete Guide](#10-drizzle-orm--complete-guide)
11. [Drizzle Schema Design Patterns](#11-drizzle-schema-design-patterns)
12. [Drizzle Queries — Every Pattern](#12-drizzle-queries--every-pattern)
13. [Drizzle Migrations & Configuration](#13-drizzle-migrations--configuration)
14. [oRPC — What It Is and Why It Exists](#14-orpc--what-it-is-and-why-it-exists)
15. [oRPC Core Concepts](#15-orpc-core-concepts)
16. [oRPC Middleware & Context](#16-orpc-middleware--context)
17. [oRPC Routers & Procedures](#17-orpc-routers--procedures)
18. [oRPC with Next.js Integration](#18-orpc-with-nextjs-integration)
19. [oRPC Client Usage](#19-orpc-client-usage)
20. [Database Patterns for Production Systems](#20-database-patterns-for-production-systems)

---

## 1. What is a Database? Why PostgreSQL?

### What a Database Actually Is

A database is a **persistent, organized store of data** with a **query engine** that lets you retrieve and manipulate that data efficiently.

Without a database, you'd store data in files. The problems with raw files:
- **No concurrent access** — two processes writing the same file at the same time corrupts it
- **No queries** — to find one record, you read the entire file
- **No relationships** — linking data across files is manual and error-prone
- **No guarantees** — a crash mid-write leaves the file corrupt

A **relational database** (like PostgreSQL) solves all of this by providing:

```
ACID Guarantees:
  Atomicity   — a transaction either fully completes or fully fails (no partial writes)
  Consistency — the database always moves from one valid state to another
  Isolation   — concurrent transactions don't see each other's partial changes
  Durability  — committed data survives crashes (written to disk)

Query Language (SQL):
  Declarative — you say WHAT data you want, not HOW to get it
  Relational  — data lives in tables with typed columns and relationships

Concurrency:
  Many readers and writers at the same time, with no data corruption
  MVCC (Multi-Version Concurrency Control) — readers don't block writers

Indexing:
  B-tree, hash, and other index structures for fast lookups
  Without indexes: scan every row; with index: jump directly to matching rows
```

### Why PostgreSQL Specifically

PostgreSQL is an open-source, enterprise-grade relational database that has been in development since 1986. It's the most feature-rich open-source database:

```
PostgreSQL advantages over MySQL/SQLite/others:
  ✅ True ACID — most complete implementation
  ✅ Advanced types — JSONB, arrays, hstore, range types, UUID
  ✅ Full-text search — built-in tsvector/tsquery
  ✅ Advanced indexing — partial indexes, expression indexes, GIN, GiST
  ✅ Window functions — advanced analytics
  ✅ CTEs (WITH clauses) — readable complex queries
  ✅ Row-level security — policy-based access control at DB level
  ✅ Logical replication — streaming changes to subscribers
  ✅ Extensions — PostGIS (geo), pgvector (embeddings), pg_cron, etc.
  ✅ Standards compliance — closest to ANSI SQL standard
  ✅ MVCC — non-blocking reads and writes
```

---

## 2. How PostgreSQL Works Internally

### The Storage Layer

```
PostgreSQL file structure:
  $PGDATA/
  ├── base/                     ← databases (each has its own directory)
  │   └── 16384/                ← OID (object identifier) of "mydb" database
  │       ├── 1234              ← heap file for table OID 1234
  │       ├── 1234_fsm          ← free space map (which pages have room)
  │       └── 1234_vm           ← visibility map (which pages are all-visible)
  ├── global/                   ← cluster-wide tables (pg_database, pg_user, etc.)
  ├── pg_wal/                   ← Write-Ahead Log files
  └── postgresql.conf           ← configuration

Pages (Blocks):
  PostgreSQL stores data in 8KB pages (blocks)
  A heap file is a sequence of pages
  Each page contains:
    - Header (24 bytes) — LSN, flags, free space info
    - ItemIds — array of (offset, length) pointers to rows on this page
    - Rows (tuples) — the actual data, stored from the bottom of the page up
    - Free space — between ItemIds and rows
```

### The Write-Ahead Log (WAL)

```
WAL is how PostgreSQL ensures durability:

1. Before ANY change to data pages, the change is written to WAL
2. WAL is written sequentially (fast)
3. Data pages are written lazily (async)
4. On crash: replay WAL from last checkpoint to recover

Why WAL:
  Writing data pages is slow (random I/O across the heap)
  Writing WAL is fast (sequential I/O to append-only log)
  "WAL before data" guarantees: if a commit is acknowledged, the WAL record exists
  Even if the data page wasn't flushed, we can replay from WAL after crash

WAL also enables:
  Streaming replication — ship WAL to replicas in real-time
  Point-in-time recovery — restore to any moment in history
  Logical decoding — stream logical changes (for CDC, event sourcing)
```

### Query Processing Pipeline

```
SQL Query → Parser → Analyzer → Rewriter → Planner/Optimizer → Executor → Results

1. Parser: tokenizes SQL text, builds parse tree, checks syntax
2. Analyzer: resolves table/column names, checks permissions, semantic analysis
3. Rewriter: applies rules (views are rewritten as subqueries here)
4. Planner: generates possible execution plans, estimates costs, picks the cheapest
5. Executor: runs the chosen plan, fetches pages, applies filters, returns rows
```

### MVCC — Multi-Version Concurrency Control

This is fundamental to understanding PostgreSQL's behavior:

```
Traditional approach (locking):
  Reader takes a lock → Writer must wait → Reader releases lock → Writer proceeds
  Problem: readers and writers block each other

PostgreSQL MVCC:
  Every row has hidden system columns:
    xmin: transaction ID that INSERTED this row version
    xmax: transaction ID that DELETED this row version (0 = still alive)
    ctid: physical location of the current version of this row

  When you UPDATE a row:
    1. The old row version gets xmax set to the current transaction ID
    2. A NEW row version is created with xmin set to the current transaction ID
    3. Both versions exist physically in the heap
    4. COMMIT: the new version becomes visible, old version is "dead"
    5. ROLLBACK: the new version is discarded, old version remains alive

  When you DELETE a row:
    1. xmax of the row is set to the current transaction ID
    2. COMMIT: the row is invisible (dead tuple)
    3. VACUUM removes dead tuples to reclaim space

  Snapshot isolation:
    Every transaction gets a "snapshot" — a list of committed transactions
    A row is visible to a transaction if xmin committed before the snapshot
    and xmax is either 0 or committed AFTER the snapshot
    This means: readers NEVER block writers, writers NEVER block readers!
```

---

## 3. SQL Fundamentals — Complete Reference

### Creating Tables

```sql
-- CREATE TABLE with all data type options
CREATE TABLE users (
    -- Identity
    id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    -- or: id BIGSERIAL PRIMARY KEY  (auto-incrementing integer)

    -- Text
    name        VARCHAR(100)    NOT NULL,
    email       TEXT            NOT NULL UNIQUE,
    bio         TEXT,                           -- nullable (optional)

    -- Numbers
    age         INTEGER         CHECK (age >= 0 AND age <= 150),
    score       NUMERIC(10, 2), -- exact decimal: 10 total digits, 2 after decimal
    ratio       DOUBLE PRECISION,               -- floating point

    -- Boolean
    is_active   BOOLEAN         NOT NULL DEFAULT true,
    is_verified BOOLEAN         NOT NULL DEFAULT false,

    -- Dates and Times
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ,                    -- null means not deleted
    birth_date  DATE,

    -- Enums
    role        TEXT            NOT NULL DEFAULT 'user'
                                CHECK (role IN ('admin', 'user', 'moderator')),
    -- or use a proper enum type:
    -- role  user_role  NOT NULL DEFAULT 'user',

    -- Foreign Keys
    org_id      UUID            NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    -- ON DELETE CASCADE: when org is deleted, all its users are deleted too
    -- ON DELETE RESTRICT: prevent deleting org if it has users (default if omitted)
    -- ON DELETE SET NULL: set org_id to NULL when org is deleted
    -- ON DELETE SET DEFAULT: set to default value

    -- PostgreSQL-specific
    tags        TEXT[],                         -- array of strings
    metadata    JSONB,                          -- binary JSON (queryable)
    preferences JSONB           NOT NULL DEFAULT '{}',

    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Create index for frequently queried columns
CREATE INDEX idx_users_email     ON users(email);
CREATE INDEX idx_users_org_id    ON users(org_id);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
-- Partial index — only indexes active users (smaller, faster)
CREATE INDEX idx_users_active    ON users(org_id) WHERE deleted_at IS NULL;
```

### Basic CRUD

```sql
-- INSERT
INSERT INTO users (name, email, org_id)
VALUES ('Alice', 'alice@example.com', 'org-uuid-here');

-- INSERT multiple rows
INSERT INTO users (name, email, org_id) VALUES
    ('Bob',     'bob@example.com',     'org-uuid-here'),
    ('Charlie', 'charlie@example.com', 'org-uuid-here');

-- INSERT with RETURNING — get the inserted row back
INSERT INTO users (name, email, org_id)
VALUES ('Dave', 'dave@example.com', 'org-uuid-here')
RETURNING id, name, created_at;

-- SELECT basics
SELECT * FROM users;                          -- all columns (avoid in production)
SELECT id, name, email FROM users;            -- specific columns
SELECT name AS display_name FROM users;        -- column alias
SELECT DISTINCT role FROM users;              -- unique values only
SELECT COUNT(*) FROM users;                   -- count all rows
SELECT COUNT(*) FROM users WHERE is_active = true; -- count with filter

-- UPDATE
UPDATE users
SET name = 'Alice Smith', updated_at = NOW()
WHERE id = 'user-uuid-here'
RETURNING id, name, updated_at;   -- get result

-- UPDATE multiple columns
UPDATE users
SET
    is_active = false,
    deleted_at = NOW(),
    updated_at = NOW()
WHERE org_id = 'org-uuid'
  AND role = 'user';

-- DELETE
DELETE FROM users WHERE id = 'user-uuid-here' RETURNING *;

-- Soft delete (preferred)
UPDATE users SET deleted_at = NOW() WHERE id = 'user-uuid-here';
```

### WHERE Clause — All Operators

```sql
-- Comparison operators
WHERE age = 30          -- equal
WHERE age != 30         -- not equal (also: <>)
WHERE age > 18          -- greater than
WHERE age >= 18         -- greater than or equal
WHERE age < 65          -- less than
WHERE age <= 65         -- less than or equal

-- NULL checks (NEVER use = NULL or != NULL!)
WHERE deleted_at IS NULL        -- not deleted
WHERE deleted_at IS NOT NULL    -- deleted

-- Range
WHERE age BETWEEN 18 AND 65    -- inclusive range (same as age >= 18 AND age <= 65)
WHERE age NOT BETWEEN 18 AND 65

-- IN / NOT IN
WHERE role IN ('admin', 'moderator')
WHERE role NOT IN ('guest', 'banned')
WHERE id IN (SELECT user_id FROM premium_subscriptions)  -- subquery

-- LIKE — pattern matching (case-sensitive)
WHERE name LIKE 'Alice%'      -- starts with Alice
WHERE name LIKE '%Smith'      -- ends with Smith
WHERE name LIKE '%alice%'     -- contains alice
WHERE name LIKE '_alice_'     -- single char wildcard: _

-- ILIKE — case-insensitive LIKE (PostgreSQL-specific)
WHERE name ILIKE '%alice%'    -- case-insensitive contains

-- Regular expressions (PostgreSQL-specific)
WHERE email ~ '^admin'         -- regex match (case-sensitive)
WHERE email ~* '^admin'        -- regex match (case-insensitive)
WHERE email !~ 'example'       -- does NOT match
WHERE email !~* 'example'      -- does NOT match (case-insensitive)

-- Boolean logic
WHERE is_active = true AND age > 18
WHERE is_active = true OR role = 'admin'
WHERE NOT is_active
WHERE (role = 'admin' OR role = 'moderator') AND is_active = true

-- ANY / ALL with arrays
WHERE 'admin' = ANY(roles)     -- 'admin' is in the roles array
WHERE 5 > ALL(scores)          -- 5 is greater than every value in scores
```

### ORDER BY, LIMIT, OFFSET

```sql
-- Sorting
SELECT * FROM users ORDER BY created_at DESC;      -- newest first
SELECT * FROM users ORDER BY name ASC;             -- alphabetical
SELECT * FROM users ORDER BY role ASC, name DESC;  -- multi-column sort
SELECT * FROM users ORDER BY LOWER(name);          -- sort by expression

-- NULLs in sorting (default: NULLs sort LAST in ASC, FIRST in DESC)
ORDER BY deleted_at NULLS LAST     -- explicit: NULLs at end
ORDER BY deleted_at NULLS FIRST    -- NULLs at beginning

-- Pagination
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;
-- Returns rows 41-60 (page 3 of 20-per-page)
-- Problem: OFFSET gets slower as it grows (must scan and skip rows)
-- Solution: cursor-based pagination (covered later)

-- FETCH (SQL standard equivalent of LIMIT/OFFSET)
SELECT * FROM users ORDER BY id
FETCH FIRST 20 ROWS ONLY;
FETCH NEXT 20 ROWS ONLY OFFSET 40 ROWS;
```

### Aggregate Functions

```sql
-- Basic aggregates
SELECT COUNT(*) FROM users;                    -- total rows
SELECT COUNT(email) FROM users;                -- rows with non-NULL email
SELECT COUNT(DISTINCT role) FROM users;        -- distinct values
SELECT SUM(score) FROM users WHERE is_active;  -- sum of score column
SELECT AVG(age) FROM users;                    -- average
SELECT MIN(created_at) FROM users;             -- earliest creation
SELECT MAX(score) FROM users;                  -- highest score
SELECT STDDEV(score) FROM users;               -- standard deviation
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) FROM users; -- median

-- GROUP BY — aggregate per group
SELECT
    role,
    COUNT(*) AS user_count,
    AVG(age) AS avg_age,
    MAX(created_at) AS newest_user
FROM users
WHERE is_active = true
GROUP BY role;

-- Multiple GROUP BY columns
SELECT
    org_id,
    role,
    COUNT(*) AS count
FROM users
GROUP BY org_id, role
ORDER BY org_id, count DESC;

-- HAVING — filter groups (WHERE runs before GROUP BY, HAVING after)
SELECT
    org_id,
    COUNT(*) AS user_count
FROM users
GROUP BY org_id
HAVING COUNT(*) > 10   -- only orgs with more than 10 users
ORDER BY user_count DESC;

-- FILTER in aggregates (PostgreSQL-specific, cleaner than CASE)
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE role = 'admin')   AS admin_count,
    COUNT(*) FILTER (WHERE is_active = true) AS active_count,
    AVG(age) FILTER (WHERE role = 'user')    AS avg_user_age
FROM users;
```

---

## 4. Advanced SQL — Every Pattern You Need

### JOINs — Complete Coverage

```sql
-- Setup: users belong to organizations, users have posts
--   organizations(id, name, created_at)
--   users(id, name, email, org_id FK→organizations)
--   posts(id, title, content, user_id FK→users, published_at)

-- INNER JOIN — only rows with matching values in BOTH tables
SELECT
    u.name,
    u.email,
    o.name AS org_name
FROM users u
INNER JOIN organizations o ON u.org_id = o.id;
-- Users without an org are EXCLUDED
-- Orgs without users are EXCLUDED

-- LEFT JOIN (LEFT OUTER JOIN) — all rows from LEFT table, NULLs for unmatched right
SELECT
    u.name,
    COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id, u.name;
-- ALL users are included, even those with 0 posts (post_count = 0)

-- RIGHT JOIN — all rows from RIGHT table, NULLs for unmatched left
-- (Rarely used — just swap table order and use LEFT JOIN)

-- FULL OUTER JOIN — all rows from BOTH tables, NULLs on either side
SELECT
    u.name    AS user_name,
    o.name    AS org_name
FROM users u
FULL OUTER JOIN organizations o ON u.org_id = o.id;
-- Users without org: org_name = NULL
-- Orgs without users: user_name = NULL

-- CROSS JOIN — cartesian product (every row paired with every row)
SELECT u.name, r.role
FROM users u
CROSS JOIN (VALUES ('admin'), ('user'), ('moderator')) AS r(role);
-- 3 users × 3 roles = 9 rows

-- SELF JOIN — joining a table to itself
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
-- employees table has a self-referential foreign key

-- Multiple JOINs
SELECT
    p.title,
    p.published_at,
    u.name AS author_name,
    o.name AS org_name
FROM posts p
INNER JOIN users u ON p.user_id = u.id
INNER JOIN organizations o ON u.org_id = o.id
WHERE p.published_at IS NOT NULL
ORDER BY p.published_at DESC;
```

### Subqueries

```sql
-- Subquery in WHERE
SELECT name, email
FROM users
WHERE org_id IN (
    SELECT id FROM organizations WHERE created_at > NOW() - INTERVAL '30 days'
);

-- Correlated subquery (references outer query — runs once per outer row)
SELECT
    u.name,
    u.email,
    (SELECT COUNT(*) FROM posts WHERE user_id = u.id) AS post_count
FROM users u;
-- Inefficient for large tables — use JOIN instead!

-- Subquery in FROM (derived table)
SELECT
    org_stats.org_name,
    org_stats.user_count
FROM (
    SELECT
        o.name AS org_name,
        COUNT(u.id) AS user_count
    FROM organizations o
    LEFT JOIN users u ON u.org_id = o.id
    GROUP BY o.id, o.name
) AS org_stats
WHERE org_stats.user_count > 5;

-- EXISTS / NOT EXISTS (often faster than IN for large datasets)
SELECT name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts WHERE user_id = u.id AND published_at IS NOT NULL
);
-- "users who have at least one published post"

SELECT name
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM posts WHERE user_id = u.id
);
-- "users who have never posted"
```

### CTEs (Common Table Expressions — WITH Clauses)

CTEs make complex queries readable by naming intermediate results.

```sql
-- Basic CTE
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE is_active = true AND deleted_at IS NULL
)
SELECT * FROM active_users WHERE role = 'admin';

-- Multiple CTEs
WITH
active_users AS (
    SELECT id, name, org_id FROM users WHERE is_active = true
),
org_sizes AS (
    SELECT org_id, COUNT(*) AS member_count
    FROM active_users
    GROUP BY org_id
),
large_orgs AS (
    SELECT org_id FROM org_sizes WHERE member_count >= 10
)
SELECT
    u.name,
    o.name AS org_name,
    os.member_count
FROM active_users u
INNER JOIN large_orgs lo ON u.org_id = lo.org_id
INNER JOIN organizations o ON u.org_id = o.id
INNER JOIN org_sizes os ON u.org_id = os.org_id;

-- Recursive CTE (for hierarchical data — org charts, categories, threads)
WITH RECURSIVE org_hierarchy AS (
    -- Base case: top-level employees (no manager)
    SELECT id, name, manager_id, 0 AS depth, ARRAY[name] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees with managers
    SELECT
        e.id,
        e.name,
        e.manager_id,
        h.depth + 1,
        h.path || e.name   -- append name to path array
    FROM employees e
    INNER JOIN org_hierarchy h ON e.manager_id = h.id
)
SELECT
    name,
    depth,
    array_to_string(path, ' → ') AS hierarchy_path
FROM org_hierarchy
ORDER BY path;

-- Recursive CTE for category tree
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 AS level
    FROM categories
    WHERE parent_id IS NULL   -- root categories

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT
    repeat('  ', level) || name AS indented_name,
    level
FROM category_tree
ORDER BY path; -- use an ordering path for proper tree order
```

### Window Functions

Window functions perform calculations over a "window" of rows related to the current row — without collapsing them into a single row (unlike GROUP BY).

```sql
-- Syntax: function() OVER (PARTITION BY col ORDER BY col ROWS/RANGE ...)

-- ROW_NUMBER — sequential number within partition
SELECT
    name,
    org_id,
    score,
    ROW_NUMBER() OVER (PARTITION BY org_id ORDER BY score DESC) AS rank_in_org
FROM users;
-- Each org gets its own 1, 2, 3... numbering ordered by score

-- RANK — like ROW_NUMBER but ties get same rank, then gap
-- DENSE_RANK — like RANK but no gap after ties
SELECT
    name, score,
    RANK()       OVER (ORDER BY score DESC) AS rank,        -- 1, 2, 2, 4
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank,  -- 1, 2, 2, 3
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num      -- 1, 2, 3, 4
FROM users;

-- Aggregate window functions (show aggregates without GROUP BY)
SELECT
    name,
    score,
    AVG(score) OVER () AS global_avg,                              -- average over ALL rows
    AVG(score) OVER (PARTITION BY org_id) AS org_avg,              -- average per org
    MAX(score) OVER (PARTITION BY org_id) AS org_max,              -- max per org
    score - AVG(score) OVER (PARTITION BY org_id) AS vs_org_avg,  -- deviation from org avg
    SUM(score) OVER (ORDER BY created_at) AS running_total         -- cumulative sum
FROM users;

-- LAG and LEAD — access previous/next rows
SELECT
    event_date,
    revenue,
    LAG(revenue, 1, 0) OVER (ORDER BY event_date) AS prev_day_revenue,
    LEAD(revenue) OVER (ORDER BY event_date) AS next_day_revenue,
    revenue - LAG(revenue, 1, 0) OVER (ORDER BY event_date) AS day_over_day_change
FROM daily_revenue;

-- NTILE — divide into N buckets
SELECT
    name, score,
    NTILE(4) OVER (ORDER BY score DESC) AS quartile
FROM users;
-- quartile 1 = top 25%, quartile 4 = bottom 25%

-- FIRST_VALUE / LAST_VALUE — first/last in window
SELECT
    name, org_id, score,
    FIRST_VALUE(name) OVER (PARTITION BY org_id ORDER BY score DESC) AS top_scorer
FROM users;

-- Frame specification (which rows are in the window)
SELECT
    created_at,
    amount,
    SUM(amount) OVER (
        ORDER BY created_at
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW  -- 7-day rolling sum
    ) AS rolling_7day_sum,
    AVG(amount) OVER (
        ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- cumulative average
    ) AS running_avg
FROM transactions;
```

### Set Operations

```sql
-- UNION — combine results, remove duplicates
SELECT email FROM customers
UNION
SELECT email FROM newsletter_subscribers;

-- UNION ALL — combine results, keep duplicates (faster)
SELECT email FROM customers
UNION ALL
SELECT email FROM newsletter_subscribers;

-- INTERSECT — rows in BOTH queries
SELECT email FROM customers
INTERSECT
SELECT email FROM newsletter_subscribers;

-- EXCEPT — rows in first but NOT in second
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers;
-- "customers who are NOT in the newsletter"
```

### String Functions

```sql
-- Concatenation
SELECT first_name || ' ' || last_name AS full_name FROM users;
SELECT CONCAT(first_name, ' ', last_name) FROM users;
SELECT CONCAT_WS(' ', first_name, middle_name, last_name) FROM users; -- separator

-- Case conversion
SELECT UPPER(name), LOWER(email), INITCAP(name) FROM users;

-- Trimming
SELECT TRIM('  hello  '), LTRIM('  hello'), RTRIM('hello  ') FROM users;

-- Length
SELECT LENGTH(name), OCTET_LENGTH(name) FROM users; -- chars vs bytes

-- Extraction
SELECT SUBSTRING(email FROM 1 FOR 5) FROM users;    -- first 5 chars
SELECT LEFT(email, 5), RIGHT(email, 3) FROM users;
SELECT POSITION('@' IN email) FROM users;            -- find position

-- Replacement
SELECT REPLACE(email, '.com', '.net') FROM users;
SELECT REGEXP_REPLACE(phone, '[^0-9]', '', 'g') FROM users; -- remove non-digits

-- Splitting and formatting
SELECT SPLIT_PART('a.b.c', '.', 2) AS middle;  -- returns 'b'
SELECT FORMAT('Hello %s, you are %s years old', name, age) FROM users;

-- Search
SELECT * FROM products WHERE to_tsvector('english', description) @@ to_tsquery('chocolate');
```

### Date and Time Functions

```sql
-- Current time
SELECT NOW();                   -- current timestamp with timezone
SELECT CURRENT_TIMESTAMP;       -- same
SELECT CURRENT_DATE;            -- date only (no time)
SELECT CURRENT_TIME;            -- time only

-- Arithmetic
SELECT created_at + INTERVAL '7 days' FROM users;
SELECT NOW() - created_at AS account_age FROM users;    -- returns INTERVAL
SELECT EXTRACT(DAYS FROM NOW() - created_at) AS days FROM users;  -- returns number

-- Truncation
SELECT DATE_TRUNC('month', created_at) AS month FROM orders;  -- first of month
SELECT DATE_TRUNC('day', created_at) AS day FROM orders;      -- midnight

-- Extraction
SELECT
    EXTRACT(YEAR FROM created_at) AS year,
    EXTRACT(MONTH FROM created_at) AS month,
    EXTRACT(DOW FROM created_at) AS day_of_week  -- 0=Sunday, 6=Saturday
FROM orders;

-- Formatting
SELECT TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') FROM orders;
SELECT TO_CHAR(NOW(), 'Month DD, YYYY') AS formatted_date;

-- Comparing
SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days';
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- Age
SELECT AGE(NOW(), created_at) AS how_old FROM users;
SELECT EXTRACT(YEAR FROM AGE(NOW(), birth_date)) AS age_years FROM users;

-- Timezone
SELECT NOW() AT TIME ZONE 'UTC';
SELECT NOW() AT TIME ZONE 'America/New_York';
```

---

## 5. Relational Data Modeling — Deep Dive

### Normal Forms — Why They Matter

Normalization removes data redundancy and prevents anomalies.

```sql
-- UNNORMALIZED (bad) — store CSV of tags in a single column
CREATE TABLE products_bad (
    id      INT PRIMARY KEY,
    name    TEXT,
    tags    TEXT     -- "electronics,phone,mobile"  ← bad!
);
-- Problem: Can't efficiently search by tag, can't add/remove individual tags

-- 1NF (First Normal Form) — each column holds atomic values, no repeating groups
-- Each value must be indivisible
CREATE TABLE products (
    id      INT PRIMARY KEY,
    name    TEXT NOT NULL
);
CREATE TABLE product_tags (
    product_id  INT REFERENCES products(id),
    tag         TEXT NOT NULL,
    PRIMARY KEY (product_id, tag)
);

-- 2NF (Second Normal Form) — 1NF + every non-key column depends on the WHOLE primary key
-- (Relevant when you have composite primary keys)
-- Bad: order_items(order_id, product_id, quantity, product_name)
--   product_name depends only on product_id, not the composite key
-- Good: separate products table

-- 3NF (Third Normal Form) — 2NF + no transitive dependencies
-- Bad: employees(id, dept_id, dept_name)
--   dept_name depends on dept_id, not on id (transitive)
-- Good: employees(id, dept_id) + departments(id, name)

-- When to DENORMALIZE:
--   When normalized queries are too slow and can't be fixed by indexing
--   When data is read much more than written (analytics, reporting)
--   Example: store computed totals, materialized views, event stores
```

### Cardinality — The Three Relationships

```sql
-- ONE-TO-ONE: each user has at most one profile
CREATE TABLE users (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email   TEXT NOT NULL UNIQUE
);
CREATE TABLE user_profiles (
    user_id     UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    -- user_id is BOTH PK and FK — enforces one-to-one
    bio         TEXT,
    avatar_url  TEXT,
    birth_date  DATE
);

-- ONE-TO-MANY: one org has many users
CREATE TABLE organizations (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name    TEXT NOT NULL
);
CREATE TABLE users (
    id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id  UUID NOT NULL REFERENCES organizations(id) ON DELETE RESTRICT,
    -- one org_id per user, but many users can share same org_id
    name    TEXT NOT NULL
);

-- MANY-TO-MANY: users can have many roles, roles can have many users
CREATE TABLE users (...);
CREATE TABLE roles (
    id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE  -- 'admin', 'editor', 'viewer'
);
CREATE TABLE user_roles (
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id     UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    granted_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by  UUID REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)  -- composite PK prevents duplicates
);
-- Query: get all roles for a user
SELECT r.name FROM roles r
INNER JOIN user_roles ur ON r.id = ur.role_id
WHERE ur.user_id = $1;
```

### Designing a Real Schema (Agentic System)

```sql
-- Full schema for an AI agent platform

CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- for gen_random_uuid()

-- Organizations (multi-tenant)
CREATE TABLE organizations (
    id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT            NOT NULL,
    slug        TEXT            NOT NULL UNIQUE,
    plan        TEXT            NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),
    settings    JSONB           NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id          UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email           TEXT        NOT NULL UNIQUE,
    name            TEXT        NOT NULL,
    role            TEXT        NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
    password_hash   TEXT,                       -- NULL for OAuth users
    avatar_url      TEXT,
    last_login_at   TIMESTAMPTZ,
    is_active       BOOLEAN     NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ             -- soft delete
);
CREATE INDEX idx_users_org_id ON users(org_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;

-- AI Agents
CREATE TABLE agents (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id          UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    created_by      UUID        NOT NULL REFERENCES users(id),
    name            TEXT        NOT NULL,
    description     TEXT,
    model           TEXT        NOT NULL DEFAULT 'gpt-4',
    system_prompt   TEXT,
    temperature     NUMERIC(3,2) NOT NULL DEFAULT 0.7 CHECK (temperature BETWEEN 0 AND 2),
    max_tokens      INTEGER     NOT NULL DEFAULT 2000,
    tools           JSONB       NOT NULL DEFAULT '[]',   -- array of tool configs
    metadata        JSONB       NOT NULL DEFAULT '{}',
    is_public       BOOLEAN     NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);
CREATE INDEX idx_agents_org_id ON agents(org_id) WHERE deleted_at IS NULL;

-- Conversations (a session between a user and an agent)
CREATE TABLE conversations (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id          UUID        NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id        UUID        NOT NULL REFERENCES agents(id) ON DELETE RESTRICT,
    user_id         UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           TEXT,
    status          TEXT        NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
    metadata        JSONB       NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at TIMESTAMPTZ
);
CREATE INDEX idx_conversations_user_id ON conversations(user_id, last_message_at DESC);
CREATE INDEX idx_conversations_agent_id ON conversations(agent_id);

-- Messages
CREATE TABLE messages (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID        NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role            TEXT        NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
    content         TEXT        NOT NULL,
    tool_calls      JSONB,      -- for assistant messages with tool use
    tool_call_id    TEXT,       -- for tool response messages
    tokens_used     INTEGER,    -- token count for this message
    model           TEXT,       -- model used (for assistant messages)
    metadata        JSONB       NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
    -- Messages are IMMUTABLE — no updated_at (history must not change)
);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id, created_at ASC);
-- This index serves the most common query: "get all messages in order for a conversation"

-- Usage tracking
CREATE TABLE usage_events (
    id              BIGSERIAL   PRIMARY KEY,    -- bigserial for high-write tables
    org_id          UUID        NOT NULL,       -- no FK for performance (denormalized)
    user_id         UUID        NOT NULL,
    agent_id        UUID        NOT NULL,
    conversation_id UUID        NOT NULL,
    model           TEXT        NOT NULL,
    prompt_tokens   INTEGER     NOT NULL,
    completion_tokens INTEGER   NOT NULL,
    total_tokens    INTEGER     NOT NULL GENERATED ALWAYS AS (prompt_tokens + completion_tokens) STORED,
    cost_usd        NUMERIC(10, 8),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
PARTITION BY RANGE (created_at);  -- partition by month for large volumes

-- Create monthly partitions
CREATE TABLE usage_events_2024_01 PARTITION OF usage_events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE usage_events_2024_02 PARTITION OF usage_events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- etc.
CREATE INDEX idx_usage_org_date ON usage_events(org_id, created_at DESC);
```

---

## 6. PostgreSQL-Specific Features

### JSONB — Binary JSON in PostgreSQL

```sql
-- JSONB is stored in a binary format — faster to query than TEXT JSON
-- Supports indexing, operators, and functions

-- Inserting JSONB
INSERT INTO agents (name, tools, metadata)
VALUES (
    'My Agent',
    '[{"name":"search","description":"Search the web"},{"name":"calculator","description":"Do math"}]',
    '{"version": 2, "capabilities": ["vision", "tools"], "maxContextLength": 128000}'
);

-- JSONB operators
SELECT
    metadata->>'version'         AS version,     -- text output (use for text values)
    metadata->'capabilities'     AS capabilities, -- JSONB output (use for objects/arrays)
    metadata#>>'{capabilities,0}' AS first_cap    -- nested path, text output
FROM agents;

-- Check if key exists
SELECT * FROM agents WHERE metadata ? 'version';           -- has key "version"
SELECT * FROM agents WHERE metadata ?| ARRAY['a', 'b'];    -- has key 'a' OR 'b'
SELECT * FROM agents WHERE metadata ?& ARRAY['a', 'b'];    -- has BOTH keys

-- Check if JSON contains another JSON (containment)
SELECT * FROM agents WHERE tools @> '[{"name":"search"}]';  -- has a tool named "search"
SELECT * FROM agents WHERE metadata @> '{"version": 2}';    -- version is 2

-- Reverse containment
SELECT * FROM agents WHERE '[{"name":"search"},{"name":"calc"}]' @> tools;

-- Update JSONB fields (immutable — returns new value)
UPDATE agents
SET metadata = jsonb_set(metadata, '{version}', '3')
WHERE id = 'agent-uuid';

UPDATE agents
SET metadata = metadata || '{"newField": "value"}'  -- merge JSON
WHERE id = 'agent-uuid';

UPDATE agents
SET metadata = metadata - 'oldField'  -- remove key
WHERE id = 'agent-uuid';

-- GIN index for JSONB (enables fast @>, ?, ?|, ?& operations)
CREATE INDEX idx_agents_metadata ON agents USING GIN(metadata);
CREATE INDEX idx_agents_tools ON agents USING GIN(tools);

-- Query JSONB arrays
SELECT id, tool
FROM agents,
LATERAL jsonb_array_elements(tools) AS tool  -- unnest the array
WHERE tool->>'name' = 'search';

-- Aggregate into JSONB
SELECT
    org_id,
    jsonb_agg(jsonb_build_object('id', id, 'name', name)) AS agents
FROM agents
GROUP BY org_id;
```

### Arrays

```sql
-- Create table with array column
CREATE TABLE posts (
    id      UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    title   TEXT    NOT NULL,
    tags    TEXT[]  NOT NULL DEFAULT '{}'
);

-- Insert array values
INSERT INTO posts (title, tags) VALUES
    ('Hello World', ARRAY['tech', 'intro']),
    ('PostgreSQL Tips', ARRAY['database', 'postgresql', 'tips']);

-- Array operators
SELECT * FROM posts WHERE tags @> ARRAY['tech'];           -- contains 'tech'
SELECT * FROM posts WHERE tags && ARRAY['tech', 'ai'];     -- overlaps (has ANY of these)
SELECT * FROM posts WHERE 'tech' = ANY(tags);              -- equivalent to @>

-- Array functions
SELECT
    array_length(tags, 1) AS tag_count,    -- length of 1st dimension
    array_to_string(tags, ', ') AS tags_csv,
    unnest(tags) AS individual_tag          -- expand array to rows
FROM posts;

-- Modify arrays
UPDATE posts SET tags = array_append(tags, 'new-tag')   WHERE id = $1;
UPDATE posts SET tags = array_remove(tags, 'old-tag')   WHERE id = $1;
UPDATE posts SET tags = tags || ARRAY['a', 'b']         WHERE id = $1;  -- concatenate
```

### Full-Text Search

```sql
-- Create a tsvector column for efficient full-text search
ALTER TABLE posts ADD COLUMN search_vector TSVECTOR;

-- Populate it
UPDATE posts SET search_vector =
    to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(content, ''));

-- Auto-update with trigger
CREATE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_search_vector_update
    BEFORE INSERT OR UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- GIN index on tsvector for fast search
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Search queries
SELECT title, ts_rank(search_vector, query) AS rank
FROM posts, to_tsquery('english', 'postgresql & (tips | tricks)') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Phrase search
SELECT * FROM posts WHERE search_vector @@ phraseto_tsquery('english', 'query optimization');

-- Highlighting matches
SELECT title, ts_headline('english', content, to_tsquery('postgresql'))
FROM posts WHERE search_vector @@ to_tsquery('postgresql');

-- Weights for ranking (title matches matter more than body matches)
SELECT
    title,
    ts_rank_cd(
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', content), 'B'),
        query
    ) AS rank
FROM posts, to_tsquery('english', 'database') AS query
WHERE
    to_tsvector('english', title) @@ query OR
    to_tsvector('english', content) @@ query
ORDER BY rank DESC;
```

### UUID Generation & Other Useful Functions

```sql
-- UUIDs
SELECT gen_random_uuid();  -- requires pgcrypto
SELECT uuid_generate_v4(); -- requires uuid-ossp extension
-- PostgreSQL 13+: gen_random_uuid() is built-in (no extension needed)

-- Generated columns (computed, stored automatically)
CREATE TABLE orders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(10,2) NOT NULL,
    total_price     NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

-- Sequences
CREATE SEQUENCE invoice_number_seq START 1000 INCREMENT 1;
SELECT nextval('invoice_number_seq');
SELECT currval('invoice_number_seq');

-- Range types
CREATE TABLE reservations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id     UUID NOT NULL,
    reserved_for TSTZRANGE NOT NULL,  -- range of timestamps
    EXCLUDE USING GIST (room_id WITH =, reserved_for WITH &&)
    -- constraint: no two reservations for same room can overlap!
);

INSERT INTO reservations (room_id, reserved_for)
VALUES ('room-1', '[2024-01-01 09:00, 2024-01-01 11:00)');
-- [) means: includes start, excludes end

-- Check overlap
SELECT * FROM reservations
WHERE room_id = 'room-1'
  AND reserved_for && '[2024-01-01 10:00, 2024-01-01 12:00)';
```

---

## 7. Indexes — Complete Guide

### What an Index Is and How It Works

```
Without an index (sequential scan):
  Query: WHERE email = 'alice@example.com'
  PostgreSQL: read EVERY row in the table, check if email matches
  Cost: O(n) — scales with table size

With a B-tree index on email:
  PostgreSQL: traverse the B-tree to find the exact entry
  Cost: O(log n) — tree depth is log2(table_size)
  For 1 million rows: ~20 comparisons instead of ~1,000,000

B-tree structure:
  Root node
  ├── ['a'-'m']
  │   ├── ['a'-'f']
  │   │   ├── 'alice@...' → row location (ctid)
  │   │   └── 'bob@...'   → row location
  │   └── ['g'-'m']
  │       └── ...
  └── ['n'-'z']
      └── ...

Index trade-offs:
  READ: faster (for indexed columns)
  WRITE: slower (INSERT/UPDATE/DELETE must also update the index)
  STORAGE: each index takes disk space
  Rule of thumb: index columns you frequently search/sort/join on
```

### Index Types

```sql
-- B-tree (default) — for: =, <, >, BETWEEN, IN, ORDER BY, LIKE 'prefix%'
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at DESC);

-- Hash — only for = comparisons, theoretically faster than B-tree for =
-- But rarely chosen by query planner since PostgreSQL 10 improved B-trees
CREATE INDEX idx_users_id_hash ON users USING HASH(id);

-- GIN (Generalized Inverted Index) — for: JSONB @>, ?, arrays @>, &&, full-text @@
CREATE INDEX idx_agents_tools_gin ON agents USING GIN(tools);
CREATE INDEX idx_posts_search_gin ON posts USING GIN(search_vector);
CREATE INDEX idx_users_tags ON users USING GIN(tags);

-- GiST — for: geometric types, full-text (alternative to GIN), range types
CREATE INDEX idx_reservations_range ON reservations USING GIST(reserved_for);

-- BRIN (Block Range Index) — for large tables with naturally ordered data (timestamps)
-- Very small index; works by recording min/max values per block range
CREATE INDEX idx_events_created_brin ON usage_events USING BRIN(created_at);

-- Expression indexes — index a computed expression
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
-- Now this query uses the index: WHERE LOWER(email) = LOWER('Alice@example.com')

-- Partial indexes — index only rows matching a condition
CREATE INDEX idx_users_active_email ON users(email) WHERE deleted_at IS NULL;
-- Only active users are indexed — smaller, faster

-- Composite indexes — multiple columns
CREATE INDEX idx_messages_conv_time ON messages(conversation_id, created_at ASC);
-- Serves: WHERE conversation_id = $1 ORDER BY created_at
-- Also serves: WHERE conversation_id = $1 (uses first column of composite)
-- Does NOT serve: WHERE created_at > $1 (first column must be in the query)

-- Covering indexes (include non-indexed columns)
CREATE INDEX idx_users_email_covering ON users(email) INCLUDE (name, role);
-- Query: SELECT name, role FROM users WHERE email = $1
-- PostgreSQL can answer this entirely from the index — no heap access needed ("index-only scan")
```

### When NOT to Use Indexes

```sql
-- Indexes can HURT performance when:

-- 1. Small tables — a sequential scan is faster than index + heap access
-- Rule: don't index tables with < ~1000 rows

-- 2. Very low-cardinality columns — boolean, 2-3 enum values
-- WHERE is_active = true → 90% of rows → full scan is cheaper
-- Exception: combine with other conditions in a composite index

-- 3. Columns never in WHERE/JOIN/ORDER BY

-- 4. Write-heavy tables where index maintenance slows down INSERTs/UPDATEs
-- Consider: partial indexes, deferred index creation, or removing unused indexes

-- Find unused indexes:
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan AS times_used,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 10   -- used fewer than 10 times
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 8. Transactions & Concurrency Control (MVCC)

### Transactions

```sql
-- A transaction is a group of operations that are atomic (all succeed or all fail)

BEGIN;  -- or: START TRANSACTION

UPDATE accounts SET balance = balance - 100 WHERE id = 'alice';
UPDATE accounts SET balance = balance + 100 WHERE id = 'bob';

COMMIT;   -- apply all changes permanently
-- or:
ROLLBACK; -- undo all changes since BEGIN

-- Savepoints — rollback to a point within a transaction
BEGIN;

INSERT INTO orders (user_id, total) VALUES ('user-1', 100);
SAVEPOINT after_order;

INSERT INTO payments (order_id, amount) VALUES ('order-1', 100);
-- If payment fails:
ROLLBACK TO after_order;  -- undo payment, keep order
-- Do something else...

COMMIT;
```

### Isolation Levels

```sql
-- PostgreSQL supports four isolation levels (with MVCC guarantees)

-- 1. READ UNCOMMITTED — same as READ COMMITTED in PostgreSQL (MVCC prevents dirty reads)
-- 2. READ COMMITTED (default) — each statement sees the latest committed data
-- 3. REPEATABLE READ — all statements in transaction see same snapshot
-- 4. SERIALIZABLE — full serializability (transactions appear to run one at a time)

-- Set isolation level
BEGIN ISOLATION LEVEL REPEATABLE READ;
-- or
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Concurrency anomalies and isolation levels:

-- DIRTY READ: reading uncommitted changes from another transaction
-- Prevented by ALL PostgreSQL isolation levels (MVCC)

-- NON-REPEATABLE READ: a row read twice in same transaction has different values
-- Scenario: T1 reads row, T2 updates+commits that row, T1 reads again → different value
-- Prevented by: REPEATABLE READ and above

-- PHANTOM READ: a query run twice returns different rows (rows were inserted/deleted)
-- Scenario: T1 queries WHERE age > 30, T2 inserts a new row matching, T1 queries again → new row
-- Prevented by: SERIALIZABLE

-- SERIALIZATION ANOMALY: result would be impossible if transactions ran serially
-- Prevented by: SERIALIZABLE only

-- When to use each:
-- READ COMMITTED (default): most web applications
-- REPEATABLE READ: analytics, reports that read multiple related tables
-- SERIALIZABLE: financial transfers, inventory deductions, any "check-then-act" logic

-- Example: inventory deduction needing SERIALIZABLE
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT quantity FROM products WHERE id = $1;    -- reads 5
UPDATE products SET quantity = quantity - 1 WHERE id = $1 AND quantity > 0;
-- With SERIALIZABLE: if two transactions both read 5 and try to decrement,
-- one succeeds, one gets a "serialization failure" error and must retry
COMMIT;
```

### Locking

```sql
-- Row-level locks (acquired by DML automatically)
SELECT * FROM users WHERE id = $1 FOR UPDATE;         -- exclusive lock (no one else can lock this row)
SELECT * FROM users WHERE id = $1 FOR SHARE;          -- shared lock (others can read but not update)
SELECT * FROM users WHERE id = $1 FOR UPDATE NOWAIT;  -- fail immediately if locked
SELECT * FROM users WHERE id = $1 FOR UPDATE SKIP LOCKED; -- skip locked rows (useful for job queues)

-- Table-level locks (rarely needed — PostgreSQL handles most with row locks)
LOCK TABLE users IN EXCLUSIVE MODE;    -- block all writes
LOCK TABLE users IN ACCESS SHARE MODE; -- just reading

-- Advisory locks — application-level locks using lock IDs
SELECT pg_advisory_lock(42);           -- acquire lock on arbitrary number 42
SELECT pg_advisory_unlock(42);         -- release it
SELECT pg_try_advisory_lock(42);       -- non-blocking — returns true/false

-- Deadlock:
-- T1 locks row A, waits for row B
-- T2 locks row B, waits for row A
-- PostgreSQL detects deadlocks and aborts one transaction automatically
-- Prevention: always acquire locks in the same order
```

---

## 9. Performance Tuning & EXPLAIN ANALYZE

### Understanding EXPLAIN ANALYZE

```sql
-- EXPLAIN: shows the query plan (estimated costs, no execution)
-- EXPLAIN ANALYZE: executes the query AND shows actual timings and row counts
-- EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT): includes buffer cache hit/miss info

EXPLAIN ANALYZE
SELECT u.name, COUNT(m.id) AS message_count
FROM users u
LEFT JOIN conversations c ON c.user_id = u.id
LEFT JOIN messages m ON m.conversation_id = c.id
WHERE u.org_id = 'org-uuid'
  AND u.deleted_at IS NULL
GROUP BY u.id, u.name
ORDER BY message_count DESC
LIMIT 10;

-- Output explanation:
--
-- Limit  (cost=2847.23..2847.25 rows=10 width=40) (actual time=45.234..45.236 rows=10 loops=1)
--   ->  Sort  (cost=2847.23..2862.23 rows=6000 width=40) (actual time=45.231..45.232 rows=10 loops=1)
--         Sort Key: (count(m.id)) DESC
--         Sort Method: top-N heapsort  Memory: 26kB
--         ->  HashAggregate  (cost=2487.23..2547.23 rows=6000 width=40) (actual ...)
--               Group Key: u.id, u.name
--               ->  Hash Left Join  (cost=567.00..2187.23 rows=120000 width=32)
--                     Hash Cond: (c.user_id = u.id)
--                     ->  Hash Left Join  (cost=234.00..1567.23 rows=120000 width=24)
--                           Hash Cond: (m.conversation_id = c.id)
--                           ->  Seq Scan on messages m  (cost=0.00..834.00 rows=50000 ...)
--                                   ← NO INDEX ON messages.conversation_id!
--                           ->  Hash  (cost=184.00..184.00 rows=4000 width=16) (...)
--                                 ->  Seq Scan on conversations c  (...)
--                     ->  Hash  (cost=283.00..283.00 rows=4000 width=24) (...)
--                           ->  Index Scan using idx_users_org_id on users u
--                                 Index Cond: (org_id = 'org-uuid')
--                                 Filter: (deleted_at IS NULL)
--
-- Key terms:
-- Seq Scan = reading every row (usually bad on large tables)
-- Index Scan = using an index (usually good)
-- Index Only Scan = getting data entirely from index (very good)
-- Bitmap Heap Scan = using index to build bitmap, then fetching pages (good for bulk reads)
-- Hash Join = build hash table from one side, probe with other (good for large equi-joins)
-- Nested Loop = for each row in outer, find matching rows in inner (good when inner is small)
-- Merge Join = both inputs sorted, then merged (good when both sides are sorted)
--
-- cost=X..Y: X=startup cost (before first row), Y=total cost
-- rows=N: estimated row count
-- actual time=X..Y: actual execution time in milliseconds
-- loops=N: how many times this node was executed

-- Signs of performance problems:
-- Seq Scan on large table (> 100k rows) → add index
-- Rows estimate is WAY off from actual → run ANALYZE on the table
-- Nested loop with many loops → consider index or join reorder
-- Hash Batches > 1 → increase work_mem
-- Sort on disk → increase work_mem
```

### Common Optimizations

```sql
-- 1. Add missing indexes
-- Find slow queries:
SELECT
    query,
    calls,
    total_exec_time / calls AS avg_ms,
    total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 2. Update table statistics
ANALYZE users;           -- update statistics for query planner
ANALYZE;                 -- update all tables
VACUUM ANALYZE users;    -- reclaim space + update statistics

-- 3. Connection pooling (use PgBouncer)
-- Each PostgreSQL connection uses ~5-10MB memory
-- PgBouncer maintains a pool and multiplexes many app connections onto few DB connections

-- 4. Avoid SELECT *
-- SELECT * forces PostgreSQL to fetch ALL columns
-- SELECT name, email means only those columns are fetched

-- 5. Use LIMIT early in subqueries when possible

-- 6. Avoid functions on indexed columns in WHERE
-- Bad (can't use index on email):
WHERE UPPER(email) = 'ALICE@EXAMPLE.COM'
-- Good (create index on expression):
CREATE INDEX idx_users_upper_email ON users(UPPER(email));
WHERE UPPER(email) = 'ALICE@EXAMPLE.COM'

-- 7. Pagination: cursor > offset
-- Bad: OFFSET 10000 — scans and discards 10000 rows
-- Good: WHERE id > last_seen_id ORDER BY id LIMIT 20

-- 8. Materialized views for expensive aggregations
CREATE MATERIALIZED VIEW org_stats AS
SELECT
    o.id AS org_id,
    o.name AS org_name,
    COUNT(DISTINCT u.id) AS user_count,
    COUNT(DISTINCT a.id) AS agent_count,
    SUM(ue.total_tokens) AS total_tokens_used
FROM organizations o
LEFT JOIN users u ON u.org_id = o.id AND u.deleted_at IS NULL
LEFT JOIN agents a ON a.org_id = o.id AND a.deleted_at IS NULL
LEFT JOIN usage_events ue ON ue.org_id = o.id
GROUP BY o.id, o.name;

CREATE UNIQUE INDEX ON org_stats(org_id);

-- Refresh when needed (or on schedule)
REFRESH MATERIALIZED VIEW CONCURRENTLY org_stats;
-- CONCURRENTLY: doesn't lock the view during refresh
```

---

## 10. Drizzle ORM — Complete Guide

### What is Drizzle ORM?

Drizzle is a **TypeScript-first ORM** for PostgreSQL, MySQL, and SQLite. Unlike traditional ORMs (Sequelize, TypeORM), Drizzle:

```
Philosophy: "headless ORM" — minimal magic, maximum control

Key properties:
  ✅ Schema as TypeScript — define your tables in TypeScript, get full type inference
  ✅ SQL-like queries — your TypeScript looks like SQL (less mental mapping)
  ✅ Type-safe — every query result is fully typed, no any, no casting
  ✅ Lightweight — no runtime reflection, no metadata, no decorators
  ✅ Performant — generates efficient SQL, no N+1 by default
  ✅ Migration system — drizzle-kit generates migration files from schema diffs
  ✅ Zero abstraction leaks — you always know what SQL is generated
```

### Installation and Setup

```bash
npm install drizzle-orm pg
npm install -D drizzle-kit @types/pg
```

```typescript
// lib/db.ts — database connection
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,              // maximum connections in pool
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 2_000,
});

// Export the database instance
export const db = drizzle(pool, { schema });
// schema is passed to enable db.query.tableName syntax (relational queries)

// For serverless (Neon, Supabase) — use HTTP driver
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });

// For edge functions — use connection pooling (Neon serverless)
import { Pool } from "@neondatabase/serverless";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

---

## 11. Drizzle Schema Design Patterns

### Defining Tables

```typescript
// db/schema.ts
import {
  pgTable, pgEnum,
  uuid, text, varchar, integer, numeric, boolean, timestamp, date,
  jsonb, json, bigserial, serial, smallint,
  primaryKey, unique, index, uniqueIndex,
  check, foreignKey,
} from "drizzle-orm/pg-core";
import { relations, sql } from "drizzle-orm";

// ── Enums ───────────────────────────────────────────────────────
export const userRoleEnum = pgEnum("user_role", ["owner", "admin", "member"]);
export const planEnum = pgEnum("plan", ["free", "pro", "enterprise"]);
export const messageRoleEnum = pgEnum("message_role", ["user", "assistant", "system", "tool"]);

// ── Organizations ───────────────────────────────────────────────
export const organizations = pgTable("organizations", {
  id:        uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  name:      text("name").notNull(),
  slug:      text("slug").notNull().unique(),
  plan:      planEnum("plan").notNull().default("free"),
  settings:  jsonb("settings").notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Organization = typeof organizations.$inferSelect;    // SELECT result type
export type NewOrganization = typeof organizations.$inferInsert; // INSERT input type

// ── Users ────────────────────────────────────────────────────────
export const users = pgTable(
  "users",
  {
    id:           uuid("id").primaryKey().default(sql`gen_random_uuid()`),
    orgId:        uuid("org_id").notNull().references(() => organizations.id, { onDelete: "cascade" }),
    email:        text("email").notNull().unique(),
    name:         text("name").notNull(),
    role:         userRoleEnum("role").notNull().default("member"),
    passwordHash: text("password_hash"),           // null for OAuth users
    avatarUrl:    text("avatar_url"),
    lastLoginAt:  timestamp("last_login_at", { withTimezone: true }),
    isActive:     boolean("is_active").notNull().default(true),
    metadata:     jsonb("metadata").notNull().$type<Record<string, unknown>>().default({}),
    createdAt:    timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt:    timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
    deletedAt:    timestamp("deleted_at", { withTimezone: true }),
  },
  (table) => ({
    // Named indexes
    orgIdIdx:     index("idx_users_org_id").on(table.orgId),
    emailIdx:     uniqueIndex("idx_users_email").on(table.email),
    // Partial index (only active users) — note: Drizzle doesn't support .where() on indexes yet
    // Use raw SQL for partial indexes (run after migration)
  })
);

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;

// ── Agents ────────────────────────────────────────────────────────
export const agents = pgTable("agents", {
  id:           uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  orgId:        uuid("org_id").notNull().references(() => organizations.id, { onDelete: "cascade" }),
  createdBy:    uuid("created_by").notNull().references(() => users.id),
  name:         text("name").notNull(),
  description:  text("description"),
  model:        text("model").notNull().default("gpt-4"),
  systemPrompt: text("system_prompt"),
  temperature:  numeric("temperature", { precision: 3, scale: 2 }).notNull().default("0.7"),
  maxTokens:    integer("max_tokens").notNull().default(2000),
  tools:        jsonb("tools").notNull().$type<AgentTool[]>().default([]),
  isPublic:     boolean("is_public").notNull().default(false),
  createdAt:    timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt:    timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  deletedAt:    timestamp("deleted_at", { withTimezone: true }),
});

export type Agent = typeof agents.$inferSelect;
export type NewAgent = typeof agents.$inferInsert;

// ── Conversations ──────────────────────────────────────────────
export const conversations = pgTable("conversations", {
  id:            uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  orgId:         uuid("org_id").notNull().references(() => organizations.id, { onDelete: "cascade" }),
  agentId:       uuid("agent_id").notNull().references(() => agents.id, { onDelete: "restrict" }),
  userId:        uuid("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  title:         text("title"),
  status:        text("status").notNull().default("active"),
  metadata:      jsonb("metadata").notNull().default({}),
  createdAt:     timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt:     timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  lastMessageAt: timestamp("last_message_at", { withTimezone: true }),
});

export type Conversation = typeof conversations.$inferSelect;

// ── Messages ───────────────────────────────────────────────────
export const messages = pgTable("messages", {
  id:             uuid("id").primaryKey().default(sql`gen_random_uuid()`),
  conversationId: uuid("conversation_id").notNull().references(() => conversations.id, { onDelete: "cascade" }),
  role:           messageRoleEnum("role").notNull(),
  content:        text("content").notNull(),
  toolCalls:      jsonb("tool_calls").$type<ToolCall[] | null>(),
  toolCallId:     text("tool_call_id"),
  tokensUsed:     integer("tokens_used"),
  model:          text("model"),
  metadata:       jsonb("metadata").notNull().default({}),
  createdAt:      timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Message = typeof messages.$inferSelect;
export type NewMessage = typeof messages.$inferInsert;

// ── Relations (for db.query API) ─────────────────────────────
export const organizationRelations = relations(organizations, ({ many }) => ({
  users:  many(users),
  agents: many(agents),
}));

export const userRelations = relations(users, ({ one, many }) => ({
  organization:  one(organizations, { fields: [users.orgId], references: [organizations.id] }),
  conversations: many(conversations),
  createdAgents: many(agents, { relationName: "agentCreator" }),
}));

export const agentRelations = relations(agents, ({ one, many }) => ({
  organization:  one(organizations, { fields: [agents.orgId], references: [organizations.id] }),
  creator:       one(users, { fields: [agents.createdBy], references: [users.id], relationName: "agentCreator" }),
  conversations: many(conversations),
}));

export const conversationRelations = relations(conversations, ({ one, many }) => ({
  organization: one(organizations, { fields: [conversations.orgId], references: [organizations.id] }),
  agent:        one(agents, { fields: [conversations.agentId], references: [agents.id] }),
  user:         one(users, { fields: [conversations.userId], references: [users.id] }),
  messages:     many(messages),
}));

export const messageRelations = relations(messages, ({ one }) => ({
  conversation: one(conversations, { fields: [messages.conversationId], references: [conversations.id] }),
}));
```

---

## 12. Drizzle Queries — Every Pattern

### Basic CRUD

```typescript
import { db } from "./db";
import { users, agents, conversations, messages, organizations } from "./schema";
import { eq, and, or, not, isNull, isNotNull, gt, gte, lt, lte, like, ilike,
         inArray, notInArray, between, asc, desc, sql, count, sum, avg, max, min } from "drizzle-orm";

// ── SELECT ────────────────────────────────────────────────────

// Select all columns
const allUsers = await db.select().from(users);
// Type: { id: string; orgId: string; email: string; ... }[]

// Select specific columns
const userPreviews = await db
  .select({ id: users.id, name: users.name, email: users.email })
  .from(users);
// Type: { id: string; name: string; email: string }[]

// Select with WHERE
const activeAdmins = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.orgId, orgId),
      eq(users.role, "admin"),
      isNull(users.deletedAt)
    )
  );

// Select with complex conditions
const result = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.orgId, orgId),
      isNull(users.deletedAt),
      or(
        eq(users.role, "admin"),
        and(eq(users.role, "member"), eq(users.isActive, true))
      )
    )
  );

// Select with ORDER BY, LIMIT, OFFSET
const paginatedUsers = await db
  .select()
  .from(users)
  .where(and(eq(users.orgId, orgId), isNull(users.deletedAt)))
  .orderBy(asc(users.name))
  .limit(20)
  .offset((page - 1) * 20);

// ── INSERT ────────────────────────────────────────────────────

// Insert one row
const [newUser] = await db
  .insert(users)
  .values({
    orgId:        orgId,
    email:        "alice@example.com",
    name:         "Alice",
    passwordHash: await hashPassword("secret"),
  })
  .returning(); // returns the created row
// newUser: User type (all columns)

// Insert multiple rows
await db.insert(messages).values([
  { conversationId, role: "system", content: systemPrompt },
  { conversationId, role: "user", content: userMessage },
]);

// UPSERT (insert or update on conflict)
await db
  .insert(users)
  .values({ email: "alice@example.com", name: "Alice", orgId })
  .onConflictDoUpdate({
    target: users.email,     // conflict on email unique constraint
    set: {
      name:      sql`EXCLUDED.name`,   // use the new name from the attempted insert
      updatedAt: sql`NOW()`,
    },
  });

// Ignore conflicts
await db.insert(users).values(data).onConflictDoNothing();

// ── UPDATE ────────────────────────────────────────────────────

const [updated] = await db
  .update(users)
  .set({
    name:      newName,
    updatedAt: new Date(),
  })
  .where(and(eq(users.id, userId), eq(users.orgId, orgId))) // multi-condition
  .returning();

if (!updated) throw new NotFoundError("User", userId);

// Increment a counter
await db
  .update(conversations)
  .set({
    lastMessageAt: new Date(),
    updatedAt:     new Date(),
  })
  .where(eq(conversations.id, conversationId));

// Update with SQL expression
await db
  .update(agents)
  .set({ tokensUsed: sql`${agents.tokensUsed} + ${tokensToAdd}` })
  .where(eq(agents.id, agentId));

// ── DELETE ────────────────────────────────────────────────────

// Hard delete
const [deleted] = await db
  .delete(users)
  .where(eq(users.id, userId))
  .returning({ id: users.id });

// Soft delete
await db
  .update(users)
  .set({ deletedAt: new Date(), updatedAt: new Date() })
  .where(and(eq(users.id, userId), isNull(users.deletedAt)));
```

### JOINs in Drizzle

```typescript
// INNER JOIN
const userWithOrg = await db
  .select({
    userId:  users.id,
    userName: users.name,
    orgName: organizations.name,
    orgPlan: organizations.plan,
  })
  .from(users)
  .innerJoin(organizations, eq(users.orgId, organizations.id))
  .where(eq(users.id, userId));

// LEFT JOIN — include users with no conversations
const usersWithConvCount = await db
  .select({
    userId:    users.id,
    userName:  users.name,
    convCount: count(conversations.id),
  })
  .from(users)
  .leftJoin(conversations, and(
    eq(conversations.userId, users.id),
    isNull(conversations.deletedAt)
  ))
  .where(eq(users.orgId, orgId))
  .groupBy(users.id, users.name)
  .orderBy(desc(count(conversations.id)));

// Multiple JOINs
const fullConversation = await db
  .select({
    convId:    conversations.id,
    convTitle: conversations.title,
    userName:  users.name,
    agentName: agents.name,
  })
  .from(conversations)
  .innerJoin(users, eq(conversations.userId, users.id))
  .innerJoin(agents, eq(conversations.agentId, agents.id))
  .where(eq(conversations.id, conversationId));
```

### Relational Queries (db.query API)

The `db.query` API lets you write object-graph queries without thinking about JOINs:

```typescript
// Must pass schema to drizzle() constructor for this to work
// db = drizzle(pool, { schema })

// Find one with relations
const user = await db.query.users.findFirst({
  where: and(eq(users.id, userId), isNull(users.deletedAt)),
  with: {
    organization: true,     // includes related organization
    conversations: {
      limit: 5,
      orderBy: desc(conversations.lastMessageAt),
      with: {
        agent: { columns: { id: true, name: true } }  // only some columns
      }
    }
  }
});
// user.organization is Organization
// user.conversations is Conversation[] with agent: { id, name }

// Find many with complex conditions
const agents = await db.query.agents.findMany({
  where: and(
    eq(agents.orgId, orgId),
    isNull(agents.deletedAt),
    eq(agents.isPublic, true)
  ),
  with: {
    creator: { columns: { id: true, name: true, avatarUrl: true } },
    conversations: {
      columns: { id: true, lastMessageAt: true },
      limit: 1,
      orderBy: desc(conversations.lastMessageAt),
    }
  },
  orderBy: desc(agents.createdAt),
  limit: 20,
  offset: 0,
});

// Columns filter — exclude sensitive fields
const safeUsers = await db.query.users.findMany({
  where: eq(users.orgId, orgId),
  columns: {
    passwordHash: false,   // exclude — don't expose password hash
    deletedAt: false,
  },
});
```

### Transactions in Drizzle

```typescript
// All operations in a transaction either commit together or rollback together
const result = await db.transaction(async (tx) => {
  // tx has the same API as db but within the transaction

  // Create organization
  const [org] = await tx
    .insert(organizations)
    .values({ name: dto.orgName, slug: dto.slug })
    .returning();

  // Create owner user
  const [user] = await tx
    .insert(users)
    .values({
      orgId:        org.id,
      email:        dto.email,
      name:         dto.name,
      role:         "owner",
      passwordHash: await hashPassword(dto.password),
    })
    .returning();

  // Create default agent
  const [agent] = await tx
    .insert(agents)
    .values({
      orgId:     org.id,
      createdBy: user.id,
      name:      "Default Assistant",
      model:     "gpt-4",
      systemPrompt: "You are a helpful assistant.",
    })
    .returning();

  // If ANY operation throws, ALL changes are rolled back
  return { org, user, agent };
});

// Nested transactions use SAVEPOINT
const result = await db.transaction(async (tx) => {
  const [order] = await tx.insert(orders).values(orderData).returning();

  try {
    await tx.insert(payments).values({ orderId: order.id, amount: order.total });
  } catch (e) {
    // Payment failed — rollback JUST the payment (savepoint)
    // The order remains committed
    await tx.rollback(); // rolls back to the savepoint
  }

  return order;
});
```

### Aggregations and Complex Queries

```typescript
// Count with conditions
const { total } = await db
  .select({ total: count() })
  .from(users)
  .where(and(eq(users.orgId, orgId), isNull(users.deletedAt)))
  .then(rows => rows[0]);

// Multiple aggregations
const stats = await db
  .select({
    totalUsers:   count(users.id),
    activeUsers:  count(sql`CASE WHEN ${users.isActive} THEN 1 END`),
    adminCount:   count(sql`CASE WHEN ${users.role} = 'admin' THEN 1 END`),
  })
  .from(users)
  .where(and(eq(users.orgId, orgId), isNull(users.deletedAt)));

// Group by with having
const agentUsage = await db
  .select({
    agentId:   messages.conversationId,
    msgCount:  count(),
    totalTokens: sum(messages.tokensUsed),
    avgTokens:   avg(messages.tokensUsed),
  })
  .from(messages)
  .innerJoin(conversations, eq(messages.conversationId, conversations.id))
  .where(eq(conversations.orgId, orgId))
  .groupBy(conversations.agentId)
  .having(gt(count(), 5))
  .orderBy(desc(sum(messages.tokensUsed)));

// Subqueries
const usersWithRecentActivity = await db
  .select()
  .from(users)
  .where(
    inArray(
      users.id,
      db.select({ userId: conversations.userId })
        .from(conversations)
        .where(gt(conversations.lastMessageAt, sql`NOW() - INTERVAL '7 days'`))
    )
  );

// Raw SQL when ORM isn't enough
const complexResult = await db.execute(sql`
  SELECT
    u.id,
    u.name,
    COUNT(c.id) FILTER (WHERE c.created_at > NOW() - INTERVAL '7 days') AS recent_convs,
    COALESCE(SUM(ue.total_tokens), 0) AS total_tokens
  FROM users u
  LEFT JOIN conversations c ON c.user_id = u.id
  LEFT JOIN usage_events ue ON ue.user_id = u.id
  WHERE u.org_id = ${orgId}
    AND u.deleted_at IS NULL
  GROUP BY u.id, u.name
  ORDER BY recent_convs DESC
  LIMIT ${limit}
`);

// Cursor-based pagination
async function getMessagesCursor(
  conversationId: string,
  cursor?: string,
  limit: number = 50
): Promise<{ items: Message[]; nextCursor: string | null }> {
  let cursorDate: Date | undefined;

  if (cursor) {
    const [cursorMsg] = await db
      .select({ createdAt: messages.createdAt })
      .from(messages)
      .where(eq(messages.id, cursor));
    cursorDate = cursorMsg?.createdAt;
  }

  const items = await db
    .select()
    .from(messages)
    .where(
      and(
        eq(messages.conversationId, conversationId),
        cursorDate ? lt(messages.createdAt, cursorDate) : undefined
      )
    )
    .orderBy(desc(messages.createdAt))
    .limit(limit + 1); // fetch one extra to detect hasMore

  const hasMore = items.length > limit;
  const result = hasMore ? items.slice(0, limit) : items;

  return {
    items:      result.reverse(),       // return in chronological order
    nextCursor: hasMore ? result[0].id : null,  // oldest item is the cursor
  };
}
```

---

## 13. Drizzle Migrations & Configuration

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";
import { env } from "./src/env";

export default defineConfig({
  schema:   "./src/db/schema.ts",     // your schema file(s)
  out:      "./drizzle",              // migration files output directory
  dialect:  "postgresql",
  dbCredentials: {
    url: env.DATABASE_URL,
  },
  verbose:  true,   // log SQL statements
  strict:   true,   // require confirmation for destructive changes
  breakpoints: true, // add breakpoints in migration files
});
```

```bash
# Generate a new migration from schema changes
npx drizzle-kit generate
# Creates: drizzle/0001_add_agents_table.sql

# Apply pending migrations
npx drizzle-kit migrate
# Runs all unapplied migration files

# Push schema to DB (dev only — skips migration files)
npx drizzle-kit push
# Good for: rapid prototyping, test databases
# Bad for: production (no migration history)

# Open Drizzle Studio (web UI for your database)
npx drizzle-kit studio

# Check the current state
npx drizzle-kit check  # verify schema is in sync with DB

# Drop all tables (DANGER)
npx drizzle-kit drop
```

```typescript
// Run migrations programmatically (for Docker/CI/CD)
// db/migrate.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
import { Pool } from "pg";

async function runMigrations() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const db = drizzle(pool);

  console.log("Running migrations...");
  await migrate(db, { migrationsFolder: "./drizzle" });
  console.log("Migrations complete!");

  await pool.end();
}

runMigrations().catch(e => {
  console.error("Migration failed:", e);
  process.exit(1);
});
```

---

## 14. oRPC — What It Is and Why It Exists

### The API Communication Problem

```
The traditional approach — REST with manual types:

  Server (TypeScript):
    app.get("/api/users/:id", async (req, res) => {
      const user = await db.users.findById(req.params.id);
      res.json(user); // TypeScript knows the type here...
    });

  Client (TypeScript):
    const response = await fetch("/api/users/123");
    const user = await response.json(); // ...but here it's 'any'!
    user.name; // no autocompletion, no type safety!

Problems:
  - Client has no idea what shape the API returns
  - Change server response shape → client breaks at runtime, not compile time
  - Writing types manually is duplication and gets out of sync
  - Input validation must be written twice (server and client)

tRPC solution:
  Define typed procedures on the server
  Client imports the type (NOT the implementation) → full type safety
  Zero code generation — pure TypeScript inference

oRPC:
  Similar to tRPC, but:
  - OpenAPI/REST compatible (procedures can be exposed as REST endpoints)
  - Designed for use with Server Actions in Next.js
  - Framework-agnostic (Express, Hono, Fastify, Next.js)
  - HTTP method semantics (GET for queries, POST for mutations)
  - Standards-first (compatible with existing HTTP tools)
```

---

## 15. oRPC Core Concepts

### Procedures

```typescript
import { os } from "@orpc/server";
import { ORPCError } from "@orpc/server";
import { z } from "zod";

// A procedure = one API endpoint
// os = the procedure builder (os stands for orpc server)

// QUERY (read operation — maps to HTTP GET)
const getUserProcedure = os
  .input(z.object({
    id: z.string().uuid("Must be a valid UUID"),
  }))
  .output(z.object({
    id:        z.string(),
    name:      z.string(),
    email:     z.string().email(),
    role:      z.enum(["owner", "admin", "member"]),
    createdAt: z.date(),
  }))
  .handler(async ({ input, context }) => {
    // input is typed: { id: string }
    // context is your custom context (auth, db, etc.)
    const user = await context.db.query.users.findFirst({
      where: and(eq(users.id, input.id), isNull(users.deletedAt)),
    });

    if (!user) {
      // Use ORPCError for structured errors — maps to HTTP status codes
      throw new ORPCError({
        code: "NOT_FOUND",
        message: `User ${input.id} not found`,
        // data: { extra: "details" }  // optional structured data
      });
    }

    return user; // validated against output schema
  });

// MUTATION (write operation — maps to HTTP POST/PUT/PATCH/DELETE)
const createUserProcedure = os
  .input(z.object({
    name:     z.string().min(1, "Name is required").max(100),
    email:    z.string().email("Invalid email format"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    role:     z.enum(["admin", "member"]).default("member"),
  }))
  .output(z.object({
    id:    z.string(),
    name:  z.string(),
    email: z.string(),
  }))
  .handler(async ({ input, context }) => {
    const existing = await context.db.query.users.findFirst({
      where: eq(users.email, input.email),
    });

    if (existing) {
      throw new ORPCError({
        code: "CONFLICT",
        message: `User with email ${input.email} already exists`,
        status: 409,
      });
    }

    const [user] = await context.db
      .insert(users)
      .values({
        orgId:        context.currentUser.orgId,
        email:        input.email,
        name:         input.name,
        passwordHash: await hashPassword(input.password),
        role:         input.role,
      })
      .returning();

    return { id: user.id, name: user.name, email: user.email };
  });

// Error codes map to HTTP status:
// NOT_FOUND → 404
// UNAUTHORIZED → 401
// FORBIDDEN → 403
// CONFLICT → 409
// BAD_REQUEST → 400
// TOO_MANY_REQUESTS → 429
// INTERNAL_SERVER_ERROR → 500
```

---

## 16. oRPC Middleware & Context

### Defining Context

```typescript
// server/context.ts
import type { NextRequest } from "next/server";
import { db } from "@/lib/db";
import { verifySessionToken } from "@/lib/auth";
import type { User } from "@/db/schema";

// The context type — available in every procedure handler
export interface AppContext {
  db: typeof db;
  currentUser: User | null;
  requestId: string;
  ipAddress: string;
  userAgent: string;
}

// Factory: creates a fresh context for each request
export async function createContext(request: NextRequest): Promise<AppContext> {
  const requestId = crypto.randomUUID();

  // Extract session token
  const token = request.cookies.get("session-token")?.value
    ?? request.headers.get("Authorization")?.replace("Bearer ", "");

  // Verify and decode token
  let currentUser: User | null = null;
  if (token) {
    try {
      const session = await verifySessionToken(token);
      if (session) {
        currentUser = await db.query.users.findFirst({
          where: and(eq(users.id, session.userId), isNull(users.deletedAt)),
        }) ?? null;
      }
    } catch {
      // Invalid token — user is null (not authenticated)
    }
  }

  return {
    db,
    currentUser,
    requestId,
    ipAddress: request.ip ?? request.headers.get("x-forwarded-for") ?? "unknown",
    userAgent: request.headers.get("user-agent") ?? "unknown",
  };
}
```

### Middleware Chains

```typescript
// server/middleware.ts
import { os } from "@orpc/server";
import { ORPCError } from "@orpc/server";
import type { AppContext } from "./context";
import type { User } from "@/db/schema";

const base = os.context<AppContext>();

// Logging middleware — runs for every procedure
const withLogging = base.middleware(async ({ context, next, path }) => {
  const start = Date.now();
  context.logger?.info("Procedure called", {
    path,
    userId: context.currentUser?.id,
    requestId: context.requestId,
  });

  const result = await next({ context });

  context.logger?.info("Procedure completed", {
    path,
    duration: Date.now() - start,
    requestId: context.requestId,
  });

  return result;
});

// Authentication middleware — ensures user is logged in
const withAuth = base.middleware(async ({ context, next }) => {
  if (!context.currentUser) {
    throw new ORPCError({
      code: "UNAUTHORIZED",
      message: "You must be logged in to perform this action",
    });
  }

  // Return next with augmented context (TypeScript now knows currentUser is User, not null)
  return next({
    context: {
      ...context,
      currentUser: context.currentUser, // TypeScript: User (not User | null)
    },
  });
});

// Admin authorization middleware
const withAdmin = base.middleware(async ({ context, next }) => {
  if (!context.currentUser) {
    throw new ORPCError({ code: "UNAUTHORIZED", message: "Authentication required" });
  }
  if (context.currentUser.role !== "admin" && context.currentUser.role !== "owner") {
    throw new ORPCError({ code: "FORBIDDEN", message: "Admin access required" });
  }
  return next({ context: { ...context, currentUser: context.currentUser } });
});

// Rate limiting middleware
const withRateLimit = (limit: number, windowSeconds: number) =>
  base.middleware(async ({ context, next }) => {
    const key = `rate:${context.currentUser?.id ?? context.ipAddress}`;
    const current = await redis.incr(key);
    if (current === 1) await redis.expire(key, windowSeconds);

    if (current > limit) {
      throw new ORPCError({
        code: "TOO_MANY_REQUESTS",
        message: `Rate limit exceeded: ${limit} requests per ${windowSeconds}s`,
        headers: {
          "Retry-After": String(await redis.ttl(key)),
        },
      });
    }

    return next({ context });
  });

// Build procedure builders with middleware pre-applied
export const publicProcedure    = base.use(withLogging);
export const protectedProcedure = base.use(withLogging).use(withAuth);
export const adminProcedure     = base.use(withLogging).use(withAuth).use(withAdmin);
export const rateLimitedProcedure = protectedProcedure.use(withRateLimit(100, 60));
```

---

## 17. oRPC Routers & Procedures

### Building the Router

```typescript
// server/routers/users.ts
import { z } from "zod";
import { eq, and, isNull, ilike, count, desc } from "drizzle-orm";
import { protectedProcedure, adminProcedure } from "../middleware";
import { users } from "@/db/schema";
import { ORPCError } from "@orpc/server";

const GetUserInput = z.object({
  id: z.string().uuid(),
});

const ListUsersInput = z.object({
  limit:   z.number().int().min(1).max(100).default(20),
  offset:  z.number().int().min(0).default(0),
  search:  z.string().optional(),
  role:    z.enum(["owner", "admin", "member"]).optional(),
});

const UpdateUserInput = z.object({
  id:    z.string().uuid(),
  name:  z.string().min(1).max(100).optional(),
  role:  z.enum(["admin", "member"]).optional(),
});

export const usersRouter = {
  get: protectedProcedure
    .input(GetUserInput)
    .handler(async ({ input, context }) => {
      const user = await context.db.query.users.findFirst({
        where: and(
          eq(users.id, input.id),
          eq(users.orgId, context.currentUser.orgId), // multi-tenant: only own org
          isNull(users.deletedAt)
        ),
      });
      if (!user) throw new ORPCError({ code: "NOT_FOUND", message: "User not found" });
      const { passwordHash, ...safeUser } = user; // never return password hash
      return safeUser;
    }),

  list: protectedProcedure
    .input(ListUsersInput)
    .handler(async ({ input, context }) => {
      const { limit, offset, search, role } = input;

      const whereConditions = [
        eq(users.orgId, context.currentUser.orgId),
        isNull(users.deletedAt),
        role ? eq(users.role, role) : undefined,
        search ? ilike(users.name, `%${search}%`) : undefined,
      ].filter(Boolean);

      const [items, [{ total }]] = await Promise.all([
        context.db.query.users.findMany({
          where: and(...whereConditions as any),
          columns: { passwordHash: false }, // exclude
          orderBy: desc(users.createdAt),
          limit,
          offset,
        }),
        context.db
          .select({ total: count() })
          .from(users)
          .where(and(...whereConditions as any)),
      ]);

      return { items, total, limit, offset };
    }),

  update: adminProcedure
    .input(UpdateUserInput)
    .handler(async ({ input, context }) => {
      const { id, ...updateData } = input;
      const [updated] = await context.db
        .update(users)
        .set({ ...updateData, updatedAt: new Date() })
        .where(and(eq(users.id, id), eq(users.orgId, context.currentUser.orgId)))
        .returning();

      if (!updated) throw new ORPCError({ code: "NOT_FOUND", message: "User not found" });
      const { passwordHash, ...safeUser } = updated;
      return safeUser;
    }),

  delete: adminProcedure
    .input(z.object({ id: z.string().uuid() }))
    .handler(async ({ input, context }) => {
      if (input.id === context.currentUser.id) {
        throw new ORPCError({ code: "BAD_REQUEST", message: "Cannot delete your own account" });
      }
      await context.db
        .update(users)
        .set({ deletedAt: new Date(), updatedAt: new Date() })
        .where(and(eq(users.id, input.id), eq(users.orgId, context.currentUser.orgId)));
    }),
};

// server/routers/agents.ts
export const agentsRouter = {
  list:   protectedProcedure.input(ListAgentsInput).handler(listAgentsHandler),
  get:    protectedProcedure.input(GetAgentInput).handler(getAgentHandler),
  create: protectedProcedure.input(CreateAgentInput).handler(createAgentHandler),
  update: protectedProcedure.input(UpdateAgentInput).handler(updateAgentHandler),
  delete: adminProcedure.input(z.object({ id: z.string().uuid() })).handler(deleteAgentHandler),
  run:    protectedProcedure.input(RunAgentInput).handler(runAgentHandler),
};

// server/router.ts — root router
import { usersRouter } from "./routers/users";
import { agentsRouter } from "./routers/agents";
import { conversationsRouter } from "./routers/conversations";

export const appRouter = {
  users:         usersRouter,
  agents:        agentsRouter,
  conversations: conversationsRouter,
};

// Export the type — clients import ONLY this (not the implementations)
export type AppRouter = typeof appRouter;
```

---

## 18. oRPC with Next.js Integration

```typescript
// app/api/[...orpc]/route.ts — catch-all route handler
import { createFetchHandler } from "@orpc/server/fetch";
import { appRouter } from "@/server/router";
import { createContext } from "@/server/context";

const handler = createFetchHandler({
  router: appRouter,
  createContext,

  // Optional: OpenAPI generation
  // openapi: {
  //   info: { title: "My API", version: "1.0.0" },
  //   path: "/api",
  // },

  onError({ error, context }) {
    // Log unexpected errors
    if (error.code === "INTERNAL_SERVER_ERROR") {
      console.error("Internal error:", error, { requestId: context?.requestId });
    }
  },
});

export { handler as GET, handler as POST, handler as PUT, handler as PATCH, handler as DELETE };

// Server-side direct calls (in Server Components, Server Actions)
// server/caller.ts
import { createCaller } from "@orpc/server";
import { appRouter } from "./router";
import type { AppContext } from "./context";

export function createServerCaller(context: AppContext) {
  return createCaller(appRouter, { context });
}

// Usage in a Server Component — bypasses HTTP entirely
async function AdminPage() {
  const context = await createContext(/* get request somehow */);
  const caller = createServerCaller(context);

  // Calls the procedure directly (no HTTP overhead)
  const users = await caller.users.list({ limit: 100 });
  return <AdminUserList users={users.items} />;
}
```

---

## 19. oRPC Client Usage

```typescript
// lib/orpc-client.ts
import { createORPCFetchClient } from "@orpc/client";
import type { AppRouter } from "@/server/router";

// Client for use in React components (browser)
export const orpc = createORPCFetchClient<AppRouter>({
  baseURL: "/api",  // relative to current domain
});

// React Query integration
// lib/orpc-react.ts
import { createORPCReactQueryUtils } from "@orpc/react-query";
import { orpc } from "./orpc-client";

export const { useQuery, useMutation, useInfiniteQuery } =
  createORPCReactQueryUtils(orpc);
```

```tsx
// Usage in React components
"use client";
import { orpc } from "@/lib/orpc-react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

function UserList({ orgId }: { orgId: string }) {
  const queryClient = useQueryClient();

  // Fetch users — fully typed!
  const { data, isLoading, error } = useQuery({
    queryKey: ["users", "list"],
    queryFn:  () => orpc.users.list({ limit: 20 }),
  });

  // Create user mutation
  const createUser = useMutation({
    mutationFn: orpc.users.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
    onError: (error) => {
      // error is typed — it's an ORPCError
      if (error.code === "CONFLICT") {
        alert("Email already in use!");
      }
    },
  });

  if (isLoading) return <Spinner />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {data?.items.map(user => (
        // user is fully typed: { id, name, email, role, createdAt, ... }
        <div key={user.id}>
          <span>{user.name}</span>
          <span>{user.email}</span>
          <span>{user.role}</span>
        </div>
      ))}

      <button onClick={() => createUser.mutate({
        name: "New User",
        email: "new@example.com",
        password: "password123",
      })}>
        Create User
      </button>
    </div>
  );
}
```

---

## 20. Database Patterns for Production Systems

### Repository Pattern

```typescript
// Encapsulate database access behind a typed interface
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findManyByOrg(orgId: string, options?: QueryOptions): Promise<PaginatedResult<User>>;
  create(data: NewUser): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  softDelete(id: string): Promise<void>;
  hardDelete(id: string): Promise<void>;
}

class DrizzleUserRepository implements IUserRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    return this.db.query.users.findFirst({
      where: and(eq(users.id, id), isNull(users.deletedAt)),
    }) ?? null;
  }

  async findManyByOrg(
    orgId: string,
    { limit = 20, offset = 0, search }: QueryOptions = {}
  ): Promise<PaginatedResult<User>> {
    const [items, [{ total }]] = await Promise.all([
      this.db.select().from(users)
        .where(and(
          eq(users.orgId, orgId),
          isNull(users.deletedAt),
          search ? ilike(users.name, `%${search}%`) : undefined
        ))
        .orderBy(desc(users.createdAt))
        .limit(limit)
        .offset(offset),
      this.db.select({ total: count() }).from(users)
        .where(and(eq(users.orgId, orgId), isNull(users.deletedAt))),
    ]);

    return { items, total, limit, offset };
  }
  // ... other methods
}
```

### N+1 Problem and Solutions

```typescript
// THE N+1 PROBLEM:
// Fetching 10 users + then fetching each user's org = 11 queries!
const users = await getUsers(); // 1 query
for (const user of users) {
  user.org = await getOrg(user.orgId); // N queries (one per user)
}
// Total: N+1 queries

// SOLUTION 1: JOIN (simplest)
const usersWithOrg = await db
  .select({
    userId: users.id,
    userName: users.name,
    orgId: organizations.id,
    orgName: organizations.name,
  })
  .from(users)
  .innerJoin(organizations, eq(users.orgId, organizations.id));
// 1 query total

// SOLUTION 2: Drizzle relational queries
const usersWithOrg = await db.query.users.findMany({
  with: { organization: true }
});
// 1-2 queries (Drizzle fetches relations efficiently)

// SOLUTION 3: DataLoader pattern (for GraphQL-style batching)
import DataLoader from "dataloader";

function createOrgLoader(db: Database) {
  return new DataLoader<string, Organization>(async (ids) => {
    const orgs = await db.query.organizations.findMany({
      where: inArray(organizations.id, [...ids]),
    });
    const orgMap = new Map(orgs.map(o => [o.id, o]));
    return ids.map(id => orgMap.get(id) ?? new Error(`Org ${id} not found`));
  });
}

// Each call to orgLoader.load(id) is batched into one query!
const orgLoader = createOrgLoader(db);
const users = await getUsers();
// These all batch into a single SELECT WHERE id IN (...)
const orgsPromises = users.map(user => orgLoader.load(user.orgId));
const orgs = await Promise.all(orgsPromises);
```

### Soft Deletes — Full Pattern

```typescript
// All queries for "active" records must filter deleted_at IS NULL
// Use a helper to avoid forgetting it

function activeWhere<T extends { deletedAt: Column }>(
  table: T,
  ...conditions: SQL[]
): SQL {
  return and(isNull(table.deletedAt), ...conditions) as SQL;
}

// Usage
const activeUsers = await db.select().from(users)
  .where(activeWhere(users, eq(users.orgId, orgId)));

// Better: create a base query builder
const activeUsersQuery = db.select().from(users).where(isNull(users.deletedAt));
const result = await activeUsersQuery.where(eq(users.orgId, orgId));

// Soft delete operation
async function softDeleteUser(userId: string, deletedBy: string): Promise<void> {
  await db.transaction(async (tx) => {
    await tx.update(users)
      .set({ deletedAt: new Date(), updatedAt: new Date() })
      .where(and(eq(users.id, userId), isNull(users.deletedAt)));

    // Audit log
    await tx.insert(auditLogs).values({
      action:     "USER_DELETED",
      entityType: "user",
      entityId:   userId,
      performedBy: deletedBy,
      metadata:   { soft: true },
    });
  });
}
```

### Audit Logging Pattern

```typescript
// Comprehensive audit trail — who did what, when
export const auditLogs = pgTable("audit_logs", {
  id:          bigserial("id", { mode: "number" }).primaryKey(),
  orgId:       uuid("org_id").notNull(),
  userId:      uuid("user_id"),                  // who performed the action
  action:      text("action").notNull(),          // "USER_CREATED", "ORDER_DELETED", etc.
  entityType:  text("entity_type").notNull(),     // "user", "agent", "order"
  entityId:    text("entity_id").notNull(),       // ID of the affected entity
  oldValue:    jsonb("old_value"),                // previous state
  newValue:    jsonb("new_value"),                // new state
  ipAddress:   text("ip_address"),
  userAgent:   text("user_agent"),
  metadata:    jsonb("metadata").notNull().default({}),
  createdAt:   timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

// Use in service layer
async function updateAgent(agentId: string, data: UpdateAgentDto, context: AppContext) {
  const [oldAgent] = await db.select().from(agents).where(eq(agents.id, agentId));
  if (!oldAgent) throw new NotFoundError("Agent", agentId);

  const [newAgent] = await db.update(agents).set(data).where(eq(agents.id, agentId)).returning();

  await db.insert(auditLogs).values({
    orgId:      context.currentUser.orgId,
    userId:     context.currentUser.id,
    action:     "AGENT_UPDATED",
    entityType: "agent",
    entityId:   agentId,
    oldValue:   oldAgent,
    newValue:   newAgent,
    ipAddress:  context.ipAddress,
    userAgent:  context.userAgent,
  });

  return newAgent;
}
```

### Connection Pool Best Practices

```typescript
// For Next.js serverless/edge — connections are important to manage carefully
import { Pool } from "pg";
import { drizzle } from "drizzle-orm/node-postgres";

// Singleton pattern — reuse pool across hot module reloads in development
declare global {
  var _pgPool: Pool | undefined;
}

function getPool(): Pool {
  if (!global._pgPool) {
    global._pgPool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: parseInt(process.env.DB_POOL_SIZE ?? "10"),
      idleTimeoutMillis: 30_000,
      connectionTimeoutMillis: 5_000,
      // For Neon serverless:
      ssl: { rejectUnauthorized: false },
    });

    global._pgPool.on("error", (err) => {
      console.error("Unexpected error on idle client", err);
    });
  }
  return global._pgPool;
}

export const db = drizzle(getPool(), { schema });

// Health check
export async function checkDatabaseConnection(): Promise<boolean> {
  try {
    await db.execute(sql`SELECT 1`);
    return true;
  } catch {
    return false;
  }
}
```

---

## Quick Reference: SQL Cheat Sheet

```sql
-- SELECT
SELECT [DISTINCT] cols FROM table
[JOIN table2 ON condition]
[WHERE conditions]
[GROUP BY cols]
[HAVING conditions]
[ORDER BY col [ASC|DESC] [NULLS FIRST|LAST]]
[LIMIT n] [OFFSET m];

-- JOINs
INNER JOIN  — matching rows only
LEFT JOIN   — all left + matching right (NULLs for unmatched)
FULL OUTER JOIN — all rows from both sides
CROSS JOIN  — cartesian product

-- Aggregates: COUNT, SUM, AVG, MIN, MAX, STDDEV
-- Window functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, NTILE

-- CTE
WITH name AS (SELECT ...) SELECT ... FROM name;
WITH RECURSIVE name AS (base UNION ALL recursive) ...;

-- INSERT
INSERT INTO table (cols) VALUES (...) [RETURNING cols];
INSERT INTO table (...) VALUES (...) ON CONFLICT (col) DO UPDATE SET ...;

-- UPDATE
UPDATE table SET col = val [WHERE ...] [RETURNING cols];

-- DELETE
DELETE FROM table [WHERE ...] [RETURNING cols];

-- TRANSACTIONS
BEGIN; ... COMMIT; / ROLLBACK;
SAVEPOINT name; ROLLBACK TO name;
BEGIN ISOLATION LEVEL SERIALIZABLE;

-- INDEXES
CREATE [UNIQUE] INDEX name ON table [USING type] (cols) [WHERE partial];
CREATE INDEX ... USING GIN(jsonb_col);
DROP INDEX name;
```

---

*This guide covers PostgreSQL internals, SQL from fundamentals to advanced patterns, Drizzle ORM complete usage, and oRPC for type-safe API design. The next file covers RabbitMQ, gRPC, and MinIO.*
