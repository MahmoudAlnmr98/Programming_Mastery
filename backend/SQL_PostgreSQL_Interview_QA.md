# SQL & PostgreSQL — Interview Questions & Answers (Premium Reference)
> 160 questions. Full answers with code and diagrams. SQL fundamentals, joins, window functions, indexes, MVCC, transactions, performance tuning, PostgreSQL internals. No stubs — every question answered in full.

---

## Table of Contents
- [Section 1: SQL Fundamentals (Q1–Q25)](#section-1-sql-fundamentals)
- [Section 2: Joins & Set Operations (Q26–Q45)](#section-2-joins--set-operations)
- [Section 3: Aggregations, CTEs & Window Functions (Q46–Q75)](#section-3-aggregations-ctes--window-functions)
- [Section 4: Indexes & Query Planning (Q76–Q105)](#section-4-indexes--query-planning)
- [Section 5: Transactions, MVCC & Concurrency (Q106–Q125)](#section-5-transactions-mvcc--concurrency)
- [Section 6: PostgreSQL Internals & Architecture (Q126–Q140)](#section-6-postgresql-internals)
- [Section 7: Advanced Features (Q141–Q155)](#section-7-advanced-features)
- [Section 8: Schema Design & Production Patterns (Q156–Q160)](#section-8-schema-design)

---

## SECTION 1: SQL FUNDAMENTALS

---

**Q1. What is the order of SQL clause execution? Why does it matter?**

```
WRITTEN ORDER vs EXECUTION ORDER:

Written:         Executed:
1. SELECT        1. FROM          — identify source tables
2. FROM          2. JOIN          — combine tables
3. JOIN          3. WHERE         — filter individual rows
4. WHERE         4. GROUP BY      — group remaining rows
5. GROUP BY      5. HAVING        — filter groups
6. HAVING        6. SELECT        — compute output expressions
7. ORDER BY      7. DISTINCT      — remove duplicates
8. LIMIT         8. ORDER BY      — sort result set
                 9. LIMIT/OFFSET  — paginate

PRACTICAL CONSEQUENCES:
  ✗ Cannot reference SELECT aliases in WHERE  (alias not defined yet)
  ✓ Can reference SELECT aliases in ORDER BY  (evaluated after SELECT)
  ✗ Cannot use aggregate functions in WHERE   (use HAVING instead)
  ✓ Can use column numbers in GROUP BY/ORDER BY: GROUP BY 1, 2

Example:
  SELECT user_id, COUNT(*) AS cnt FROM orders
  WHERE cnt > 5    -- ERROR: cnt doesn't exist at WHERE evaluation time
  GROUP BY user_id
  HAVING COUNT(*) > 5;  -- CORRECT: HAVING evaluated after GROUP BY
```

---

**Q2. What is the difference between WHERE and HAVING?**

```
WHERE:
  - Filters rows BEFORE grouping
  - Cannot use aggregate functions (COUNT, SUM, AVG, etc.)
  - Can use any column from the table

HAVING:
  - Filters groups AFTER grouping
  - CAN use aggregate functions
  - Can only reference columns in GROUP BY or in aggregates

Example:
  SELECT department, AVG(salary) AS avg_sal
  FROM employees
  WHERE status = 'active'        -- filter rows first (no grouping yet)
  GROUP BY department
  HAVING AVG(salary) > 70000;   -- filter groups (aggregates allowed)

PERFORMANCE NOTE:
  Always filter with WHERE when possible — it reduces rows before grouping.
  HAVING filters happen on the already-grouped result set.
  Bad:  GROUP BY dept HAVING dept = 'Engineering'
  Good: WHERE dept = 'Engineering' GROUP BY dept
```

---

**Q3. What is the difference between DELETE, TRUNCATE, and DROP?**

```
DELETE:
  - DML (Data Manipulation Language)
  - Can have WHERE clause
  - Fires row-level triggers
  - Generates WAL for each deleted row (rollback-able)
  - Slow on large tables — row-by-row
  - Does NOT reset sequences (SERIAL/IDENTITY)
  - Transaction-safe

TRUNCATE:
  - DDL-like, but transaction-safe in PostgreSQL (unlike most DBs)
  - No WHERE clause — removes ALL rows
  - Much faster — metadata operation, minimal WAL
  - Fires statement-level triggers (not row-level by default)
  - Can CASCADE to referenced tables
  - Resets sequences with RESTART IDENTITY
  - Acquires ACCESS EXCLUSIVE lock

DROP:
  - DDL
  - Removes the entire TABLE (structure + data + indexes + constraints)
  - Not reversible outside a transaction
  - No WHERE clause, no filter

WHEN TO USE WHICH:
  Selective delete of rows        → DELETE WHERE ...
  Wipe a table completely, fast   → TRUNCATE
  Remove the table itself         → DROP
```

---

**Q4. What is a NULL and how does it behave in SQL?**

```
NULL = absence of a value / unknown

NULL is NOT zero, NOT empty string, NOT false.
NULL represents UNKNOWN — the result of most operations involving NULL is NULL.

COMPARISON RULES:
  NULL = NULL  →  NULL  (not TRUE — use IS NULL / IS NOT NULL)
  NULL != NULL →  NULL
  NULL + 5     →  NULL
  NULL OR TRUE →  TRUE  (exception — known true dominates)
  NULL AND FALSE → FALSE (exception — known false dominates)
  NOT NULL     →  NULL

CHECKING FOR NULL:
  WHERE col IS NULL       -- correct
  WHERE col IS NOT NULL   -- correct
  WHERE col = NULL        -- always false (never matches)
  WHERE col != NULL       -- always false

NULL IN AGGREGATES:
  COUNT(*) — counts all rows including NULLs
  COUNT(col) — counts only non-NULL values
  SUM/AVG/MIN/MAX — all ignore NULLs

NULL IN UNIQUE CONSTRAINTS:
  PostgreSQL (and SQL standard): multiple NULLs allowed in UNIQUE column
  Because NULL != NULL — they're not considered duplicates

NULL IN SORTING:
  ORDER BY col ASC  → NULLs last  (default in PostgreSQL)
  ORDER BY col DESC → NULLs first (default in PostgreSQL)
  ORDER BY col ASC NULLS FIRST  — explicit control
  ORDER BY col DESC NULLS LAST

USEFUL NULL FUNCTIONS:
  COALESCE(a, b, c)  — returns first non-NULL value
  NULLIF(a, b)       — returns NULL if a = b, otherwise a
  IS DISTINCT FROM   — NULL-safe !=  (NULL IS DISTINCT FROM NULL → false)
  IS NOT DISTINCT FROM — NULL-safe = (NULL IS NOT DISTINCT FROM NULL → true)
```

---

**Q5. Explain all JOIN types with examples.**

```
Setup:
  users: id=1 Alice, id=2 Bob, id=3 Carol
  orders: id=10 user_id=1, id=11 user_id=1, id=12 user_id=99

INNER JOIN — only matching rows from both tables
  SELECT u.name, o.id FROM users u JOIN orders o ON u.id = o.user_id;
  Result: Alice+10, Alice+11
  (Bob, Carol excluded; order 12 excluded)

LEFT JOIN — all left rows + matching right rows (NULL if no match)
  SELECT u.name, o.id FROM users u LEFT JOIN orders o ON u.id = o.user_id;
  Result: Alice+10, Alice+11, Bob+NULL, Carol+NULL

RIGHT JOIN — all right rows + matching left rows (NULL if no match)
  SELECT u.name, o.id FROM users u RIGHT JOIN orders o ON u.id = o.user_id;
  Result: Alice+10, Alice+11, NULL+12

FULL OUTER JOIN — all rows from both tables
  SELECT u.name, o.id FROM users u FULL OUTER JOIN orders o ON u.id = o.user_id;
  Result: Alice+10, Alice+11, Bob+NULL, Carol+NULL, NULL+12

CROSS JOIN — cartesian product (every combination)
  SELECT u.name, o.id FROM users u CROSS JOIN orders o;
  Result: 3 users × 3 orders = 9 rows (no ON clause)

SELF JOIN — table joined to itself
  SELECT e.name AS employee, m.name AS manager
  FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;

ANTI JOIN — rows in left with NO match in right (2 ways):
  -- Method 1: LEFT JOIN + IS NULL
  SELECT u.* FROM users u LEFT JOIN orders o ON u.id = o.user_id
  WHERE o.id IS NULL;
  
  -- Method 2: NOT EXISTS (often faster)
  SELECT u.* FROM users u
  WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

---

**Q6. What is a subquery? What types exist?**

```
A subquery is a query nested inside another query.

1. SCALAR SUBQUERY — returns exactly one row, one column
   SELECT name, (SELECT AVG(salary) FROM employees) AS company_avg
   FROM employees;

2. ROW SUBQUERY — returns one row, multiple columns
   SELECT * FROM employees WHERE (dept_id, salary) =
   (SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id LIMIT 1);

3. TABLE SUBQUERY (derived table) — returns a result set used in FROM
   SELECT dept, avg_sal FROM (
     SELECT department AS dept, AVG(salary) AS avg_sal
     FROM employees GROUP BY department
   ) stats WHERE avg_sal > 70000;

4. CORRELATED SUBQUERY — references outer query; runs once per row
   SELECT e.name FROM employees e
   WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department = e.department);
   PERFORMANCE: Can be very slow — recalculated for every outer row.
   Often rewritable as a window function or JOIN.

5. EXISTS/NOT EXISTS — efficient correlated existence check
   SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id);
   EXISTS stops at first match — very efficient.

6. IN/NOT IN — membership test
   SELECT * FROM products WHERE category_id IN (SELECT id FROM categories WHERE active);
   WARNING: NOT IN with NULLs in subquery returns no rows (NULL issue).
   Use NOT EXISTS instead of NOT IN to be safe.
```

---

**Q7. What is a CTE and when should you use it over a subquery?**

```sql
-- CTE (Common Table Expression): a named, reusable subquery within a statement
-- Syntax:
WITH cte_name AS (
  SELECT ...
)
SELECT * FROM cte_name;

-- CTE vs SUBQUERY comparison:

-- Subquery (messy when reused):
SELECT *
FROM (SELECT ...) t1
JOIN (SELECT ...) t2 ON ...
JOIN (SELECT ...) t3 ON ...;

-- CTE (readable, named, reusable):
WITH t1 AS (SELECT ...),
     t2 AS (SELECT ...),
     t3 AS (SELECT ...)
SELECT * FROM t1 JOIN t2 ON ... JOIN t3 ON ...;

USE CTEs WHEN:
  ✓ Same subquery needed multiple times → define once, reference many
  ✓ Complex query with multiple steps → each step as a CTE (readable)
  ✓ Recursive queries (trees, graphs) → ONLY doable with recursive CTE
  ✓ Incremental logic: filter → aggregate → rank → filter again

USE SUBQUERY WHEN:
  ✓ Simple one-off subquery used in one place
  ✓ You need the optimizer to inline it (CTE may materialize in PG11-)

RECURSIVE CTE (trees/hierarchies):
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 0 AS depth
  FROM employees WHERE manager_id IS NULL         -- base case: root nodes

  UNION ALL

  SELECT e.id, e.name, e.manager_id, o.depth + 1
  FROM employees e JOIN org o ON e.manager_id = o.id  -- recursive case
)
SELECT * FROM org ORDER BY depth, name;

-- PG12+ MATERIALIZATION CONTROL:
WITH stats AS MATERIALIZED (...)       -- force: run once, cache result
WITH stats AS NOT MATERIALIZED (...)   -- force: inline into outer query
```

---

**Q8. What is the difference between UNION, UNION ALL, INTERSECT, and EXCEPT?**

```sql
-- All set operations combine results of two SELECT statements.
-- Both SELECTs must have same number of columns, compatible types.

UNION — combine + remove duplicates (implicit DISTINCT)
  SELECT city FROM customers
  UNION
  SELECT city FROM suppliers;
  -- Each city appears once, even if in both tables

UNION ALL — combine without removing duplicates (FASTER — no dedup step)
  SELECT city FROM customers
  UNION ALL
  SELECT city FROM suppliers;
  -- Cities may repeat. Use when you know there are no duplicates or want them.

INTERSECT — rows present in BOTH result sets (removes duplicates)
  SELECT city FROM customers
  INTERSECT
  SELECT city FROM suppliers;
  -- Only cities that appear in both tables

EXCEPT — rows in FIRST result set NOT in SECOND (removes duplicates)
  SELECT city FROM customers
  EXCEPT
  SELECT city FROM suppliers;
  -- Cities in customers that are NOT in suppliers

PERFORMANCE:
  UNION ALL >> UNION (no sort/dedup step)
  Always prefer UNION ALL unless you specifically need deduplication.

ORDER BY with set operations:
  (SELECT city FROM customers UNION SELECT city FROM suppliers)
  ORDER BY city;  -- ORDER BY applies to the entire result
```

---

**Q9. Explain GROUP BY with ROLLUP, CUBE, and GROUPING SETS.**

```sql
-- Standard GROUP BY: one level of grouping
SELECT region, product, SUM(sales) FROM sales GROUP BY region, product;

-- ROLLUP: hierarchical subtotals (most common for reports)
SELECT region, product, SUM(sales) FROM sales
GROUP BY ROLLUP (region, product);
-- Generates groups: (region, product), (region), ()
-- i.e., detail rows + regional subtotals + grand total

-- CUBE: all possible combinations of groupings
SELECT region, product, SUM(sales) FROM sales
GROUP BY CUBE (region, product);
-- Generates: (region,product), (region), (product), ()

-- GROUPING SETS: explicit control over which groupings to compute
SELECT region, product, SUM(sales) FROM sales
GROUP BY GROUPING SETS (
  (region, product),   -- by region and product
  (region),            -- by region only
  ()                   -- grand total
);

-- GROUPING() function: identifies which columns are NULL due to rollup
SELECT
  CASE WHEN GROUPING(region) = 1 THEN 'ALL REGIONS' ELSE region END AS region,
  CASE WHEN GROUPING(product) = 1 THEN 'ALL PRODUCTS' ELSE product END AS product,
  SUM(sales)
FROM sales
GROUP BY ROLLUP (region, product);
-- GROUPING(col) returns 1 if that col is aggregated (NULL due to rollup)

-- COALESCE alternative (works but can confuse actual NULLs with rollup NULLs):
SELECT COALESCE(region, 'ALL'), COALESCE(product, 'ALL'), SUM(sales)
FROM sales GROUP BY ROLLUP (region, product);
```

---

**Q10. What is DISTINCT ON and how is it different from DISTINCT?**

```sql
-- DISTINCT: removes all duplicate rows from the result
SELECT DISTINCT country FROM users;
-- Returns one row per unique country

-- DISTINCT ON (col): PostgreSQL-specific
-- Keeps ONE row per unique value of the specified column(s)
-- Which row is kept depends on ORDER BY
SELECT DISTINCT ON (user_id)
  user_id, order_id, total, created_at
FROM orders
ORDER BY user_id, created_at DESC;
-- Returns the MOST RECENT order per user (first after sorting by created_at DESC)

-- RULE: ORDER BY must start with the DISTINCT ON columns
-- Without ORDER BY the row chosen is arbitrary (use ORDER BY to control which)

-- COMMON USE CASE: "latest record per group"
-- Equivalent (but usually slower) with ROW_NUMBER():
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM orders
) t WHERE rn = 1;

-- DISTINCT ON is usually faster for this pattern in PostgreSQL.
```

---

**Q11. How does LIMIT/OFFSET pagination work and what are its problems?**

```sql
-- Basic pagination
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 0;   -- page 1
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 20;  -- page 2
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 100; -- page 6

PROBLEMS WITH OFFSET:
  1. SLOW on large offsets:
     OFFSET 100000 means: scan 100020 rows, discard first 100000.
     Gets slower with every page. O(offset + limit) I/O.

  2. MISSING/DUPLICATE ROWS:
     If a row is inserted/deleted between page requests,
     rows shift — you skip or see the same row twice.

SOLUTION: KEYSET PAGINATION (cursor-based)
  -- Page 1:
  SELECT * FROM products ORDER BY id LIMIT 20;
  -- Last id seen: 234

  -- Page 2 (use last seen id as cursor):
  SELECT * FROM products WHERE id > 234 ORDER BY id LIMIT 20;
  -- Always O(log N + limit) with index scan on id — fast at any depth
  -- Stable: inserts/deletes don't cause drift

  -- Composite cursor (when sorting by non-unique column):
  SELECT * FROM products
  WHERE (price, id) > (29.99, 500)   -- tuple comparison
  ORDER BY price, id
  LIMIT 20;

USE OFFSET WHEN:
  - Small tables or low page numbers
  - User can jump to arbitrary page
  - Simplicity is paramount

USE KEYSET WHEN:
  - Large tables
  - "Next page" / "infinite scroll" patterns
  - Performance matters
```

---

**Q12. What are CASE expressions and how do you use them?**

```sql
-- Simple CASE (compare to specific values)
SELECT name,
  CASE status
    WHEN 'active'   THEN 'Active User'
    WHEN 'inactive' THEN 'Inactive User'
    WHEN 'banned'   THEN 'Banned User'
    ELSE 'Unknown'
  END AS status_label
FROM users;

-- Searched CASE (arbitrary boolean conditions — more flexible)
SELECT name, salary,
  CASE
    WHEN salary >= 100000 THEN 'Senior'
    WHEN salary >= 70000  THEN 'Mid'
    WHEN salary >= 50000  THEN 'Junior'
    ELSE 'Entry Level'
  END AS level
FROM employees;

-- CASE in aggregate (conditional aggregation)
SELECT
  COUNT(*) AS total_orders,
  COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,
  COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS cancelled,
  SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END) AS completed_revenue
FROM orders;

-- Alternative with FILTER (cleaner in PostgreSQL)
SELECT
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE status = 'completed') AS completed,
  SUM(total) FILTER (WHERE status = 'completed') AS completed_revenue
FROM orders;

-- CASE in ORDER BY (custom sort order)
ORDER BY CASE status
  WHEN 'urgent'  THEN 1
  WHEN 'normal'  THEN 2
  WHEN 'low'     THEN 3
  ELSE 4
END;
```

---

**Q13. What is the difference between CHAR, VARCHAR, and TEXT in PostgreSQL?**

```
CHAR(n):
  Fixed-length. Always stored as exactly n characters.
  Shorter values padded with spaces.
  Comparisons: trailing spaces ignored in some contexts (can cause bugs).
  Virtually no use case in PostgreSQL — avoid.

VARCHAR(n):
  Variable-length up to n characters.
  Adds a length check constraint.
  No performance difference from TEXT internally.

TEXT:
  Variable-length, no limit.
  Idiomatic PostgreSQL type.
  Same internal storage as VARCHAR.
  No length check — more flexible.

KEY INSIGHT:
  In PostgreSQL, CHAR, VARCHAR, VARCHAR(n), and TEXT all use the same
  internal storage engine (varlena). The difference is only semantic:
    - VARCHAR(n) adds a CHECK constraint on character count
    - CHAR(n) pads with spaces
  There is NO performance difference.

RECOMMENDATION:
  Use TEXT for most string columns.
  Use VARCHAR(n) only when you genuinely need a maximum length constraint.
  Never use CHAR unless you're interfacing with a legacy system.

TOAST:
  PostgreSQL automatically compresses and moves large values (> ~2KB)
  to a separate TOAST table. This is transparent to the application.
  Affects: TEXT, VARCHAR, JSONB, BYTEA, arrays.
```

---

**Q14. What are the differences between NUMERIC, FLOAT, and MONEY for storing currency?**

```
FLOAT (REAL / DOUBLE PRECISION):
  Binary floating-point — approximate representation.
  0.1 + 0.2 = 0.30000000000000004 (not 0.3!)
  NEVER use for money. Rounding errors will accumulate.
  Fast arithmetic. Use for scientific calculations.

NUMERIC / DECIMAL:
  Exact decimal arithmetic. No rounding errors.
  NUMERIC(10, 2) = up to 8 digits before decimal, exactly 2 after.
  Slower than FLOAT (software arithmetic, not hardware FPU).
  ALWAYS use for money/financial values.
  Storage is variable — larger numbers take more space.

MONEY:
  Fixed-point, locale-dependent formatting.
  Tied to the database locale for currency symbol.
  Division returns FLOAT (loses precision).
  Can cause issues in multi-currency apps.
  AVOID in new schemas.

RECOMMENDATION FOR CURRENCY:
  Option A: NUMERIC(19, 4) — store with 4 decimal places for rounding headroom
  Option B: BIGINT — store in smallest currency unit (cents, pence)
    e.g., $29.99 → 2999 cents. Integer math is exact and fast.
    Convert to decimal in the application layer.
  Option B is used by Stripe, Square, most financial systems.
```

---

**Q15. What are PostgreSQL sequences and how do SERIAL vs IDENTITY differ?**

```sql
-- SEQUENCE: a database object that generates sequential integers

-- SERIAL (legacy — PG-specific, being phased out):
CREATE TABLE users (id SERIAL PRIMARY KEY);
-- Shorthand for:
CREATE SEQUENCE users_id_seq;
CREATE TABLE users (id INT DEFAULT nextval('users_id_seq'));
-- Sequence is NOT tightly coupled — you can INSERT manually with any value

-- IDENTITY (SQL standard — preferred in PG10+):
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
-- or:
id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY

GENERATED ALWAYS:
  - PostgreSQL will always generate the value
  - Manual INSERT of a value raises an error (OVERRIDING SYSTEM VALUE to bypass)
  - Stricter — prevents accidental overrides

GENERATED BY DEFAULT:
  - PostgreSQL generates by default but you can override with explicit value
  - More flexible but less safe

-- Sequence manipulation:
SELECT nextval('users_id_seq');     -- get next value (advances sequence)
SELECT currval('users_id_seq');     -- current value in this session
SELECT setval('users_id_seq', 1000); -- reset to 1000

-- After bulk INSERT that bypasses sequence, fix with:
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- KEY INSIGHT: Sequences are NOT transactional.
-- If a transaction rolls back, the sequence value is NOT returned.
-- This means IDs may have gaps — this is NORMAL and expected.
-- Do not rely on sequence values being gapless.
```

---

**Q16. What is the difference between a PRIMARY KEY, UNIQUE, and an index?**

```
PRIMARY KEY:
  - Uniqueness constraint: all values must be distinct
  - NOT NULL constraint: cannot be NULL
  - Automatically creates a unique B-Tree index
  - Only one per table
  - Used as the default target for FOREIGN KEY references

UNIQUE CONSTRAINT:
  - Uniqueness constraint: all values must be distinct
  - NULLs ARE allowed (multiple NULLs OK — NULLs are not equal)
  - Automatically creates a unique index
  - Multiple per table

INDEX:
  - A data structure to speed up queries — NOT a constraint
  - Does not enforce uniqueness (unless UNIQUE INDEX)
  - Must be maintained separately from constraints
  - Multiple per table, any columns

RELATIONSHIP:
  PRIMARY KEY → creates a UNIQUE, NOT NULL index implicitly
  UNIQUE constraint → creates a UNIQUE index implicitly
  INDEX → standalone performance object, no constraint

You can have an index without a constraint (for performance),
but every constraint creates an underlying index automatically.

CREATE UNIQUE INDEX — creates both a unique index AND effectively
a unique constraint that the planner can use.
```

---

**Q17. What is referential integrity and what are the ON DELETE options?**

```sql
-- FOREIGN KEY enforces that referenced row must exist
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);

ON DELETE behaviors (what happens when the referenced row is deleted):

NO ACTION (default):
  Raises an error at end of statement/transaction if FK violated.
  Actually deferred check — same as RESTRICT for non-deferrable FKs.
  DELETE FROM users WHERE id=1; → ERROR if orders reference user 1

RESTRICT:
  Immediately raises an error. Cannot be deferred.
  Stricter than NO ACTION — checked immediately, not at end of statement.

CASCADE:
  Automatically deletes all child rows.
  DELETE FROM users WHERE id=1 → also deletes all orders for user 1
  Use carefully — can cause unexpected mass deletes.

SET NULL:
  Sets the FK column to NULL in child rows.
  DELETE FROM users WHERE id=1 → orders.user_id = NULL for those orders
  Requires FK column to be nullable.

SET DEFAULT:
  Sets the FK column to its default value.
  Requires a valid default that references an existing row (or NULL).

DEFERRABLE constraints:
  DEFERRABLE INITIALLY DEFERRED — FK checked at COMMIT, not per statement
  Useful for circular references or complex multi-table inserts in one txn.
  Example: inserting two rows that reference each other.
```

---

**Q18. What is the difference between a view, materialized view, and a CTE?**

```sql
-- VIEW: stored query, no data stored
CREATE VIEW active_users AS
  SELECT * FROM users WHERE status = 'active';
SELECT * FROM active_users WHERE email LIKE '%@gmail.com';
-- Transparent: PostgreSQL merges the WHERE into the view query
-- Always fresh: executes underlying query every time
-- No storage overhead
-- Can be slow if the underlying query is complex

-- MATERIALIZED VIEW: stored query result (snapshot)
CREATE MATERIALIZED VIEW user_stats AS
  SELECT user_id, COUNT(*) AS orders, SUM(total) AS revenue
  FROM orders GROUP BY user_id;
-- Data physically stored — query runs at creation time
-- Fast to query (just reading cached data)
-- STALE: data gets old until you refresh

REFRESH MATERIALIZED VIEW user_stats;          -- blocks reads during refresh
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats; -- non-blocking (needs unique index)

CREATE UNIQUE INDEX ON user_stats(user_id);     -- needed for CONCURRENTLY

-- CTE: query-scoped named subquery
WITH user_stats AS (SELECT ...)
SELECT * FROM user_stats;
-- Exists only for the duration of the query
-- No persistent storage

COMPARISON:
  View             → no storage, always fresh, no refresh needed
  Materialized View → stored, fast reads, needs manual/scheduled refresh
  CTE              → in-query only, no storage, no persistence
  
WHEN TO USE EACH:
  View: hide complexity, share query logic, row-level security
  Materialized View: expensive aggregations queried often, can tolerate slight staleness
  CTE: organize complex multi-step queries within a single statement
```

---

**Q19. What are window functions and how do they differ from GROUP BY?**

```sql
-- GROUP BY collapses rows. Window functions DO NOT collapse rows.

-- GROUP BY: 4 rows → 2 rows (one per department)
SELECT department, AVG(salary)
FROM employees GROUP BY department;

-- Window function: 4 rows → still 4 rows (avg added per row)
SELECT name, department, salary,
  AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;

-- The OVER() clause defines the "window":
function() OVER (
  PARTITION BY col   -- divide rows into groups (like GROUP BY but keeps rows)
  ORDER BY col       -- ordering within each partition
  frame_clause       -- which rows to include in the window
)

-- COMMON WINDOW FUNCTIONS:
ROW_NUMBER()  → unique sequential number (no ties): 1, 2, 3, 4
RANK()        → ties get same rank, gaps after: 1, 1, 3, 4
DENSE_RANK()  → ties get same rank, no gaps: 1, 1, 2, 3
NTILE(n)      → divide into n equal buckets
LAG(col, n)   → value from n rows before current
LEAD(col, n)  → value from n rows after current
FIRST_VALUE() → first value in the window frame
LAST_VALUE()  → last value in the window frame
SUM/AVG/COUNT → aggregate over window (running total, moving average)

-- RUNNING TOTAL:
SUM(amount) OVER (ORDER BY date) AS running_total

-- 7-DAY MOVING AVERAGE:
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

-- % OF PARTITION TOTAL:
amount / SUM(amount) OVER (PARTITION BY region) * 100 AS pct_of_region
```

---

**Q20. What is COALESCE and when do you use it?**

```sql
-- COALESCE(a, b, c, ...) returns the first non-NULL value.
-- Short-circuits: stops evaluating after first non-NULL.

SELECT COALESCE(phone, mobile, 'N/A') AS contact FROM users;
-- Returns phone if not null, else mobile, else 'N/A'

-- Common use cases:
-- 1. Default value for NULL
SELECT COALESCE(discount, 0) AS discount FROM orders;

-- 2. After LEFT JOIN (NULLs from unmatched rows)
SELECT u.name, COALESCE(COUNT(o.id), 0) AS order_count
FROM users u LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
-- Note: COUNT(o.id) already returns 0 for no matches, not NULL
-- But COALESCE is explicit and readable

-- 3. Fallback chain
SELECT COALESCE(updated_at, created_at) AS last_activity FROM articles;

NULLIF(a, b):
  Returns NULL if a = b, otherwise returns a.
  Opposite of COALESCE in a sense.
  
  -- Prevent division by zero:
  SELECT 100.0 / NULLIF(denominator, 0) AS ratio FROM metrics;
  -- If denominator = 0, returns NULL instead of division-by-zero error

  -- Turn empty string into NULL:
  SELECT NULLIF(trim(phone), '') AS phone FROM users;
```

---

**Q21. How do you find duplicate rows and delete them while keeping one?**

```sql
-- FIND duplicates:
SELECT email, COUNT(*) AS cnt
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- SEE all duplicate rows with detail:
SELECT *
FROM users
WHERE email IN (
  SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1
);

-- Using window function to find duplicates:
SELECT * FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
  FROM users
) t
WHERE rn > 1;  -- all duplicates except the first occurrence

-- DELETE duplicates keeping the row with the lowest id:
DELETE FROM users
WHERE id IN (
  SELECT id FROM (
    SELECT id,
      ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM users
  ) t
  WHERE rn > 1
);

-- PostgreSQL-specific: DELETE with CTE (cleaner)
WITH duplicates AS (
  SELECT id,
    ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
  FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);

-- ADD UNIQUE constraint after cleanup to prevent future duplicates:
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);
```

---

**Q22. What is the difference between IN, EXISTS, and a JOIN for filtering?**

```sql
-- Three ways to "filter users who have at least one order":

-- METHOD 1: IN with subquery
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
-- Subquery returns a list; PostgreSQL checks membership.
-- If NULL appears in the IN list → issues with NOT IN (returns no rows!)
-- NOT IN with NULLs: WHERE id NOT IN (SELECT user_id FROM orders)
-- → if any user_id is NULL in orders, entire NOT IN returns empty!
-- SAFE for IN, DANGEROUS for NOT IN when NULLs possible.

-- METHOD 2: EXISTS (recommended for correlated check)
SELECT * FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
-- Short-circuits on first match — can be very fast.
-- NULL-safe: no issue with NULLs.
-- NOT EXISTS is always safe (unlike NOT IN).

-- METHOD 3: JOIN + DISTINCT
SELECT DISTINCT u.* FROM users u JOIN orders o ON u.id = o.user_id;
-- Can return duplicate users if multiple orders per user (hence DISTINCT).
-- DISTINCT adds overhead; usually less readable for this pattern.

PERFORMANCE IN POSTGRESQL:
  Modern PostgreSQL optimizer converts IN (subquery) to a semi-join,
  which is often equivalent to EXISTS in performance.
  Manual EXISTS/NOT EXISTS is still clearer for intent.
  
  Approximate performance order for this use case:
  EXISTS ≈ IN (PostgreSQL optimizes both to semi-join)
  JOIN+DISTINCT: may be slower due to dedup step

RULE OF THUMB:
  Use EXISTS/NOT EXISTS — it's NULL-safe, intent is clear, optimizer handles it well.
  Avoid NOT IN when the subquery might return NULLs.
```

---

**Q23. What are the most important string functions in PostgreSQL?**

```sql
-- LENGTH / CHAR_LENGTH
length('hello')              → 5
char_length('héllo')         → 5  (character count, not bytes)
octet_length('héllo')        → 6  (byte count — 'é' is 2 bytes in UTF-8)

-- CASE
upper('hello')               → 'HELLO'
lower('HELLO')               → 'hello'
initcap('hello world')       → 'Hello World'

-- TRIMMING
trim('  hello  ')            → 'hello'
ltrim('  hello  ')           → 'hello  '
rtrim('  hello  ')           → '  hello'
trim(both 'x' FROM 'xxhelloxx') → 'hello'

-- SEARCHING
position('world' IN 'hello world')  → 7
strpos('hello world', 'world')      → 7  (same)
starts_with('foobar', 'foo')        → true

-- SUBSTRING / EXTRACTION
substring('hello world', 7)        → 'world'
substring('hello world', 1, 5)     → 'hello'
substring('hello world' FROM 'w\w+') → 'world'  (regex)
left('hello world', 5)             → 'hello'
right('hello world', 5)            → 'world'

-- SPLITTING
split_part('a,b,c,d', ',', 2)      → 'b'
string_to_array('a,b,c', ',')      → '{a,b,c}'
regexp_split_to_table('a,b,c', ',') → rows: a, b, c
regexp_split_to_array('a,b,c', ',') → array

-- REPLACING / FORMATTING
replace('hello world', 'world', 'postgresql')  → 'hello postgresql'
regexp_replace('foo123bar', '\d+', 'NUM')      → 'fooNUMbar'
format('Hello %s, you are %s years old', 'Alice', 30) → 'Hello Alice, you are 30 years old'
lpad('42', 5, '0')                            → '00042'
rpad('hello', 10, '-')                        → 'hello-----'

-- AGGREGATION
string_agg(name, ', ' ORDER BY name)  → 'Alice, Bob, Carol'
```

---

**Q24. How do you perform date arithmetic in PostgreSQL?**

```sql
-- INTERVAL arithmetic
NOW() + INTERVAL '7 days'
NOW() - INTERVAL '1 month'
NOW() + INTERVAL '2 hours 30 minutes'
DATE '2024-01-01' + 30                    -- add 30 days (integer + date)

-- DATE_TRUNC — truncate to a precision
DATE_TRUNC('month', NOW())                -- first moment of current month
DATE_TRUNC('week', NOW())                 -- start of current week (Monday in ISO)
DATE_TRUNC('hour', NOW())                 -- current hour:00:00

-- EXTRACT — get a part of a date
EXTRACT(year   FROM NOW())                -- 2024
EXTRACT(month  FROM NOW())                -- 1
EXTRACT(day    FROM NOW())                -- 15
EXTRACT(dow    FROM NOW())                -- 0=Sunday, 1=Monday ... 6=Saturday
EXTRACT(epoch  FROM NOW())                -- Unix timestamp (seconds since 1970)
EXTRACT(epoch  FROM INTERVAL '2 hours')  -- 7200

-- DATE_PART (older syntax, equivalent)
DATE_PART('year', NOW())

-- AGE — human-readable interval between two timestamps
AGE(NOW(), created_at)                    -- '3 years 2 months 15 days'
AGE(TIMESTAMP '2020-01-01')              -- age from today

-- COMMON PATTERNS:
-- Records from last 7 days:
WHERE created_at >= NOW() - INTERVAL '7 days'

-- Records in current month:
WHERE DATE_TRUNC('month', created_at) = DATE_TRUNC('month', NOW())

-- Group by day:
SELECT DATE_TRUNC('day', created_at) AS day, COUNT(*) FROM orders GROUP BY 1;

-- Calculate business metric by month:
SELECT
  TO_CHAR(DATE_TRUNC('month', created_at), 'YYYY-MM') AS month,
  SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY 1;
```

---

**Q25. What is EXPLAIN and EXPLAIN ANALYZE? How do you read them?**

```
EXPLAIN: Shows the PLANNED execution strategy (no actual execution)
EXPLAIN ANALYZE: Actually RUNS the query and shows real vs estimated stats
EXPLAIN (ANALYZE, BUFFERS): Also shows memory/disk page access counts

Example output:
Hash Join  (cost=340..1195 rows=50000 width=28) (actual time=12..44 rows=48203 loops=1)
  │         └── planner estimate ──┘              └──── actual results ───────┘
  │
  ├── cost=X..Y: X = startup cost, Y = total cost (planner units, relative)
  ├── rows=N: planner's row estimate
  ├── actual time=X..Y: real time in ms (startup..total)
  ├── actual rows=N: real row count produced
  └── loops=N: how many times this node ran (1 for top-level, N for inner side of nested loop)

RED FLAGS:
  estimated rows << actual rows → bad statistics → run ANALYZE
  Seq Scan on large table → consider adding an index
  Hash Batches > 1 → hash table spilled to disk → increase work_mem
  loops=N on expensive node → nested loop problem
  Sort → large sort may spill to disk if work_mem is too low

BUFFERS output:
  shared hit=N  → pages read from shared_buffers (fast, in RAM)
  shared read=N → pages read from disk (slow)
  High read/hit ratio → data is well cached
  High read → cache miss, may benefit from larger shared_buffers

BEST PRACTICES:
  Always use EXPLAIN (ANALYZE, BUFFERS) for performance investigation.
  Never use SET enable_seqscan=off in production.
  Compare estimated vs actual rows — large discrepancies = stale stats.
  Run ANALYZE on the table if estimates are wildly off.
```

---

## SECTION 2: JOINS & SET OPERATIONS

---

**Q26. What is a self join and when do you use it?**

```sql
-- A self join joins a table to itself.
-- Required when rows within the same table have relationships to each other.

-- COMMON USE CASES:
-- 1. Hierarchical data (employees and their managers)
-- 2. Finding pairs within the same table
-- 3. Comparing rows of the same table to each other

-- EXAMPLE 1: Employee-Manager hierarchy
SELECT
  e.name AS employee,
  e.salary,
  m.name AS manager,
  m.salary AS manager_salary
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
-- Same table aliased twice: e = employee row, m = manager row

-- EXAMPLE 2: Find products in same category with lower price
SELECT a.name AS product, b.name AS cheaper_alternative
FROM products a
JOIN products b ON a.category_id = b.category_id
              AND b.price < a.price
              AND a.id != b.id;

-- EXAMPLE 3: Find consecutive events (comparing to previous row)
SELECT curr.id, curr.event_type, prev.event_type AS prev_event
FROM events curr
LEFT JOIN events prev ON prev.id = (
  SELECT MAX(id) FROM events WHERE id < curr.id
);
-- Better done with LAG() window function in practice
```

---

**Q27. How do you find records in table A that don't exist in table B?**

```sql
-- Three methods — all equivalent logically:

-- METHOD 1: LEFT JOIN + IS NULL (most common, readable)
SELECT u.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
-- "Users with no orders"
-- The IS NULL check on the RIGHT table column identifies non-matched rows

-- METHOD 2: NOT EXISTS (most semantically clear, NULL-safe)
SELECT u.*
FROM users u
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- METHOD 3: NOT IN (be careful with NULLs!)
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders);
-- DANGER: if any user_id in orders is NULL, this returns ZERO rows
-- NOT IN with NULLs: NULL makes the entire NOT IN condition unknown
-- Only safe when you know the subquery column has no NULLs

-- METHOD 4: EXCEPT (set operation)
SELECT id FROM users
EXCEPT
SELECT user_id FROM orders;
-- Returns user IDs that don't appear in orders
-- Simple but may not give you the full user row

RECOMMENDATION:
  Use NOT EXISTS — it's NULL-safe, clear intent, well-optimized by PostgreSQL.
  LEFT JOIN + IS NULL is also fine. Avoid NOT IN.
```

---

**Q28. What is the difference between equi-join, theta-join, and natural join?**

```sql
-- EQUI-JOIN: join condition uses equality (=)
-- Most common. What you use 99% of the time.
SELECT * FROM orders o JOIN users u ON o.user_id = u.id;

-- THETA-JOIN: join condition uses any comparison operator (>, <, !=, >=, etc.)
-- Non-equality join
SELECT a.name, b.name AS competitor
FROM products a
JOIN products b ON a.category = b.category
              AND a.price > b.price;  -- not equality — theta join

-- NATURAL JOIN: automatically joins on columns with the same name
SELECT * FROM orders NATURAL JOIN users;
-- Dangerous: joins on ALL columns with matching names (id, created_at, etc.)
-- Schema changes can silently break queries
-- NEVER use in production code — always be explicit with ON or USING

-- USING clause (safe alternative to NATURAL JOIN):
SELECT * FROM orders JOIN users USING (user_id);
-- Joins on user_id column, which must exist in both tables
-- Safer: explicit about which column to join on
-- output: user_id appears once (not twice like with ON)
```

---

**Q29. Explain how hash join works internally.**

```
HASH JOIN algorithm:

Phase 1: BUILD
  - Choose the smaller table (inner/build side)
  - Scan it entirely
  - Build an in-memory hash table:
      key = join column value
      value = list of rows with that key
  - Hash table lives in work_mem

Phase 2: PROBE
  - Scan the larger table (outer/probe side)
  - For each row, hash its join column
  - Look up hash table for matching rows
  - Output matching row combinations

DIAGRAM:
  users table (small)           orders table (large)
  → hash by user_id             → probe hash table
  ┌─────────────────┐           for each order row:
  │ HT: 1 → [Alice] │  ◀──────  hash(order.user_id) → lookup
  │      2 → [Bob]  │           find Alice → output Alice+order
  │      3 → [Carol]│
  └─────────────────┘

CHARACTERISTICS:
  Best for: large tables with no useful index, equi-joins only
  Memory: hash table must fit in work_mem
  If it doesn't fit: BATCHED hash join (spills to disk) → much slower
  Time: O(N + M) — linear in both table sizes

WHEN PLANNER CHOOSES HASH JOIN:
  - Tables are large
  - No index on join column
  - Enough work_mem for the smaller table
  - Equi-join condition (=)

WHEN NOT CHOSEN:
  - Inequality joins (can't hash non-equality)
  - Input is already sorted → merge join preferred
  - One side is very small → nested loop with index preferred
```

---

**Q30. What is a lateral join?**

```sql
-- LATERAL allows a subquery in FROM to reference columns from tables on its left.
-- Without LATERAL, subqueries cannot reference outer query columns.

-- Example: get top 3 orders per user
SELECT u.name, o.id, o.total
FROM users u
CROSS JOIN LATERAL (
  SELECT id, total FROM orders
  WHERE user_id = u.id          -- ← references u.id from left table
  ORDER BY total DESC
  LIMIT 3
) o;

-- Equivalent (and often interchangeable):
JOIN LATERAL (...) ON true
CROSS JOIN LATERAL (...)    -- both work; ON true = always join

-- Without LATERAL (would fail):
SELECT u.name, top_orders.id FROM users u
JOIN (
  SELECT id, total FROM orders WHERE user_id = u.id  -- ERROR: u.id unknown here
  LIMIT 3
) top_orders ON true;

-- LATERAL is useful for:
-- 1. Correlated subqueries that return multiple rows
-- 2. Calling set-returning functions per row
-- 3. "Top N per group" patterns
-- 4. Unnesting arrays per row

-- EXAMPLE: Unnest array per row
SELECT u.name, tag
FROM users u
CROSS JOIN LATERAL unnest(u.tags) AS tag;
-- Same as: SELECT name, unnest(tags) FROM users;
```

---

## SECTION 3: AGGREGATIONS, CTEs & WINDOW FUNCTIONS

---

**Q46. What is the difference between ROW_NUMBER, RANK, and DENSE_RANK?**

```sql
-- All three assign numbers within a partition, ordered by ORDER BY.
-- They differ in how they handle TIES.

-- Setup: employees with same salary
SELECT name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
  RANK()       OVER (ORDER BY salary DESC) AS rank,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;

-- Result with salaries: 90000, 90000, 80000, 70000
-- name    salary  row_num  rank  dense_rank
-- Alice   90000      1       1       1
-- Bob     90000      2       1       1
-- Carol   80000      3       3       2     ← rank skips 2, dense_rank doesn't
-- Dave    70000      4       4       3

ROW_NUMBER: Always unique, even for ties (arbitrary within ties unless tie-broken)
  1, 2, 3, 4 — no shared numbers

RANK: Ties share the same rank, then SKIPS the next rank(s)
  1, 1, 3, 4 — gap after ties (think: "two people tied for 1st, no 2nd place")

DENSE_RANK: Ties share the same rank, NO gaps
  1, 1, 2, 3 — continuous numbers

USE CASES:
  ROW_NUMBER: when you need a unique row identifier (pagination, dedup)
  RANK: competition ranking ("tied for 1st place — no 2nd")
  DENSE_RANK: category grouping where you want consecutive groups

-- PRACTICAL: Select top 1 per group (dedup)
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t WHERE rn = 1;

-- Select all employees with highest salary per dept (including ties)
SELECT * FROM (
  SELECT *, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
  FROM employees
) t WHERE dr = 1;
```

---

**Q47. How do you calculate a running total and a moving average?**

```sql
-- RUNNING TOTAL (cumulative sum):
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total
FROM transactions;
-- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- Adds all amounts from the beginning up to and including the current row

-- Running total per group (per user):
SUM(amount) OVER (PARTITION BY user_id ORDER BY date) AS user_running_total

-- MOVING AVERAGE (7-day):
SELECT
  date,
  amount,
  AVG(amount) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM daily_metrics;
-- Uses the 7 most recent rows (including current) regardless of date gaps

-- ROWS vs RANGE frame:
-- ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
--   → physical 6 previous rows
-- RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
--   → rows within 6 days (handles date gaps correctly)

-- Running COUNT:
COUNT(*) OVER (ORDER BY date) AS running_count

-- Running MAX (high water mark):
MAX(price) OVER (ORDER BY date) AS all_time_high

-- Day-over-day change:
SELECT date, revenue,
  revenue - LAG(revenue) OVER (ORDER BY date) AS daily_change,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY date))
    / NULLIF(LAG(revenue) OVER (ORDER BY date), 0), 2) AS pct_change
FROM daily_revenue;
```

---

**Q48. How do you use FILTER with aggregate functions?**

```sql
-- FILTER is a PostgreSQL/SQL-standard way to conditionally aggregate.
-- More readable than CASE inside aggregate.

-- Traditional CASE approach:
SELECT
  COUNT(CASE WHEN status = 'active'   THEN 1 END) AS active_count,
  COUNT(CASE WHEN status = 'inactive' THEN 1 END) AS inactive_count,
  SUM(CASE WHEN status = 'active' THEN total ELSE 0 END) AS active_revenue
FROM orders;

-- FILTER approach (cleaner):
SELECT
  COUNT(*) FILTER (WHERE status = 'active')   AS active_count,
  COUNT(*) FILTER (WHERE status = 'inactive') AS inactive_count,
  SUM(total) FILTER (WHERE status = 'active') AS active_revenue,
  AVG(rating) FILTER (WHERE rating IS NOT NULL) AS avg_rating
FROM orders;

-- FILTER also works with window functions:
SELECT date,
  COUNT(*) FILTER (WHERE status = 'error')
    OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS errors_7d
FROM events;

-- CROSS-TABULATION (pivot) using FILTER:
SELECT
  DATE_TRUNC('month', created_at) AS month,
  SUM(total) FILTER (WHERE region = 'US') AS us_revenue,
  SUM(total) FILTER (WHERE region = 'EU') AS eu_revenue,
  SUM(total) FILTER (WHERE region = 'APAC') AS apac_revenue
FROM orders
GROUP BY 1 ORDER BY 1;
```

---

## SECTION 4: INDEXES & QUERY PLANNING

---

**Q76. What types of indexes does PostgreSQL support?**

```
B-TREE (default):
  - Balanced tree structure
  - Supports: =, <, >, <=, >=, BETWEEN, IN, LIKE 'prefix%'
  - Good for: most queries, range scans, equality lookups
  - Sorted → also used to satisfy ORDER BY without a sort step

HASH:
  - Single-level hash table
  - Supports: = only (no range scans)
  - Smaller than B-Tree for equality-only columns
  - Rare — B-Tree is usually preferred even for equality

GIN (Generalized Inverted Index):
  - Maps each element → set of row IDs containing it
  - Best for: JSONB, arrays, full-text search (tsvector)
  - Supports: @>, <@, ?, ?|, ?&, @@
  - Slower to build/update, very fast to query for containment

GiST (Generalized Search Tree):
  - Extensible tree structure
  - Best for: geometric types, ranges (TSTZRANGE), PostGIS geography
  - Also used for nearest-neighbor (KNN) queries
  - Required for EXCLUDE constraints

BRIN (Block Range INdex):
  - Stores min/max per block range (group of pages)
  - Extremely small index (100-1000x smaller than B-Tree)
  - Best for: very large tables with naturally ordered data (time-series)
  - Trades query speed for dramatically smaller size
  - Good fit: append-only event logs ordered by timestamp

SP-GiST (Space-Partitioned GiST):
  - Non-balanced tree for non-uniform distributions
  - Best for: IP addresses, phone numbers, hierarchical data

pg_trgm extension + GIN:
  - Trigram indexing for LIKE '%pattern%' and fuzzy matching
  CREATE EXTENSION pg_trgm;
  CREATE INDEX ON users USING GIN(name gin_trgm_ops);
  -- Enables: WHERE name LIKE '%alice%' or WHERE name % 'alice'
```

---

**Q77. What is a composite index? What is the leftmost prefix rule?**

```sql
-- A composite index indexes multiple columns together.
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- The LEFTMOST PREFIX RULE:
-- A composite index (A, B, C) can be used for queries filtering on:
--   A                → ✓ uses index (leftmost prefix)
--   A, B             → ✓ uses index
--   A, B, C          → ✓ uses full index
--   B                → ✗ cannot use this index alone
--   B, C             → ✗ cannot use this index alone
--   A, C             → partial use: can use A portion, filter on C separately

-- Example:
CREATE INDEX ON orders(user_id, status, created_at);

-- Can use index:
WHERE user_id = 5                                   -- prefix: user_id
WHERE user_id = 5 AND status = 'active'             -- prefix: user_id, status
WHERE user_id = 5 AND status = 'active' AND created_at > '2024-01-01'  -- full

-- Cannot use index (not starting from leftmost):
WHERE status = 'active'                             -- no user_id
WHERE status = 'active' AND created_at > '2024-01-01' -- no user_id

-- INDEX COLUMN ORDER guidelines:
-- 1. Equality-filtered columns first
-- 2. Range-filtered columns last (range "stops" the index from filtering further)
-- 3. High-cardinality columns first (more selective = smaller scan)

-- EXAMPLE:
-- Query: WHERE user_id = 5 AND created_at BETWEEN 'a' AND 'b' AND status = 'active'
-- Best index: (user_id, status, created_at) — not (user_id, created_at, status)
-- Reason: equality on user_id and status first, then range on created_at
```

---

**Q78. What is an index-only scan? What enables it?**

```sql
-- NORMAL INDEX SCAN:
--   1. Scan index → get list of heap (table) page locations (ctid)
--   2. Fetch actual rows from heap pages
--   Two I/O operations per row

-- INDEX-ONLY SCAN:
--   1. Scan index → get all needed column values from index leaf nodes
--   No heap access needed!
--   Much faster when query only needs indexed columns

-- REQUIREMENTS for index-only scan:
-- 1. All columns in SELECT and WHERE must be in the index
-- 2. Visibility map must show page as "all-visible" (VACUUM must have run)
--    If visibility info is stale → heap visit needed to check MVCC visibility

-- HOW TO ENABLE:

-- Option A: Include all needed columns in index
CREATE INDEX idx_orders_user ON orders(user_id, total, status, created_at);
-- Now: SELECT total, status FROM orders WHERE user_id = 5
--      → index-only scan (all 3 output cols + filter col in index)

-- Option B: INCLUDE clause (PG11+) — covers additional non-key columns
CREATE INDEX idx_orders_user_covering ON orders(user_id)
INCLUDE (total, status, created_at);
-- user_id is the key (searchable, ordered)
-- total/status/created_at stored in leaf nodes (accessible, not sorted)

-- Check if index-only scan is used:
EXPLAIN (ANALYZE, BUFFERS) SELECT total, status FROM orders WHERE user_id = 5;
-- Look for: "Index Only Scan" in plan
-- Look for: "Heap Fetches: 0" → no heap visits needed

-- VACUUM importance:
-- Visibility map is updated by VACUUM/autovacuum.
-- On frequently-updated tables, pages may not be "all-visible"
-- → index-only scan degrades to regular index scan
-- → run VACUUM regularly on tables where index-only scans are important
```

---

**Q79. What is a partial index? When do you use one?**

```sql
-- A partial index includes only rows matching a WHERE condition.
-- Smaller, faster to build and scan than a full index.
-- Planner can only use it if the query has a compatible WHERE clause.

-- USE CASE 1: Only index the "interesting" subset
-- Most queries only look at active users — index only them
CREATE INDEX idx_active_users_email ON users(email) WHERE status = 'active';
-- Supports: WHERE email = 'x@y.com' AND status = 'active'
-- Does NOT help: WHERE email = 'x@y.com' (without status filter)

-- USE CASE 2: Exclude common values (low-selectivity filtering)
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';
-- 99% of orders are 'completed' — no need to index them

-- USE CASE 3: Soft-delete aware unique constraint
CREATE UNIQUE INDEX idx_users_active_email ON users(email) WHERE deleted_at IS NULL;
-- Allows multiple rows with same email (if deleted), enforces uniqueness for active

-- USE CASE 4: Index only non-NULL values
CREATE INDEX idx_orders_ext_id ON orders(external_id) WHERE external_id IS NOT NULL;
-- Skips rows where external_id is NULL — huge saving if most are NULL

-- PERFORMANCE BENEFIT:
-- A partial index may be 10x-100x smaller than a full index.
-- Smaller index → more of it fits in shared_buffers → faster scans.
-- AUTOVACUUM processes it faster.

-- VERIFY planner uses it (query must include matching condition):
EXPLAIN SELECT * FROM users WHERE email = 'x' AND status = 'active';
-- Should show: Index Scan using idx_active_users_email
```

---

**Q80. How does the query planner decide between a sequential scan and an index scan?**

```
COST-BASED DECISION:
  The planner computes a cost for each possible plan.
  Cost is measured in "page access units" (not ms directly).
  Chooses the lowest-cost plan.

COST FACTORS:
  seq_page_cost    = 1.0    (reading one page sequentially)
  random_page_cost = 4.0    (reading one page randomly, disk)
                   = 1.1    (for SSD — change this!)
  cpu_tuple_cost   = 0.01   (processing one row)

SEQUENTIAL SCAN is chosen when:
  - The filter is not very selective (many rows match)
  - e.g., WHERE status = 'active' where 80% of rows are active
  - Reading 80% of the table randomly is slower than reading it all sequentially
  - Rule of thumb: seq scan often wins if >5-10% of table will be returned

INDEX SCAN is chosen when:
  - The filter is highly selective (few rows match)
  - e.g., WHERE email = 'x@y.com' (1 row from millions)
  - Random I/O cost of finding just a few pages < seq scan cost

INDEX-ONLY SCAN is chosen when:
  - All needed columns are in the index AND
  - Visibility map says pages are "all-visible"

BITMAP INDEX SCAN:
  - Middle ground — many matching rows but not all
  - Scans index → builds bitmap of matching pages → sorted page order
  - Fetches pages in order (reduces random I/O vs plain index scan)

PLANNER CAN BE WRONG WHEN:
  - Statistics are stale (run ANALYZE)
  - random_page_cost = 4.0 but you have SSD (should be 1.1)
  - effective_cache_size is set too low (hints to planner about OS cache)
  - Table has correlated columns (stats don't capture correlation)
```

---

**Q81. What is index bloat and how do you deal with it?**

```
INDEX BLOAT: indexes grow larger than needed due to dead tuple accumulation.

HOW IT HAPPENS:
  MVCC keeps old row versions (dead tuples) in the heap.
  Dead tuples are also referenced in indexes (as ctid pointers).
  VACUUM marks heap dead tuples as reusable but may not reclaim index space.
  Over time: index contains many pointers to dead tuples.
  
  On high-update tables (e.g., status field updated frequently):
  The index can become 2-10x larger than the live data justifies.

EFFECTS:
  - Larger index = more pages to scan = slower queries
  - More shared_buffers consumed by stale index pages
  - Slower VACUUM (more to process)
  - More I/O

DETECTION:
SELECT
  indexrelid::regclass AS index_name,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
  idx_scan AS times_used
FROM pg_stat_user_indexes
JOIN pg_index USING (indexrelid)
ORDER BY pg_relation_size(indexrelid) DESC;

-- Or use pgstattuple extension for precise bloat measurement:
CREATE EXTENSION pgstattuple;
SELECT * FROM pgstatindex('idx_users_email');
-- Shows: leaf_fragmentation, avg_leaf_density, dead_leaf_pages

SOLUTIONS:
  REINDEX INDEX idx_name;                    -- rebuilds, locks table (old PG)
  REINDEX INDEX CONCURRENTLY idx_name;       -- PG12+: no lock, safe for production

  -- pg_repack extension: online table + index rebuild without locks
  pg_repack -t users -i idx_users_email

  -- For severe cases: create new index, drop old
  CREATE INDEX CONCURRENTLY idx_new ON users(email);
  DROP INDEX idx_old;
```

---

## SECTION 5: TRANSACTIONS, MVCC & CONCURRENCY

---

**Q106. What is MVCC and why does PostgreSQL use it?**

```
MVCC = Multi-Version Concurrency Control

THE PROBLEM IT SOLVES:
  Without MVCC: readers must wait for writers (or vice versa).
  Long reads block writes. Long writes block reads.
  In a busy system: everything grinds to a halt.

THE MVCC SOLUTION:
  Each transaction sees a SNAPSHOT of the database as of when it started.
  Writers create new versions of rows — they don't modify the old version.
  Readers always see the old version (consistent snapshot).
  Writers don't block readers. Readers don't block writers.

HOW IT WORKS (PostgreSQL):
  Each row stores:
    xmin = transaction ID that created this version
    xmax = transaction ID that deleted/updated this version (0 if live)

  When TXN 200 reads:
    It sees rows where xmin < 200 (created before this transaction)
    AND (xmax = 0 OR xmax >= 200) (not yet deleted from my perspective)

  When TXN 300 updates a row:
    OLD row: xmin=original, xmax=300 (marked as deleted by 300)
    NEW row: xmin=300, xmax=0 (fresh version created by 300)
    
  TXN 200, still running, reads old row — doesn't see new row.
  TXN 400, starting after 300 commits, reads new row.

DOWNSIDE:
  Dead tuples accumulate — old row versions that no transaction can see.
  Solved by VACUUM: marks dead tuples' space as reusable.
  VACUUM FULL: reclaims space to OS but requires exclusive lock.

ALTERNATIVES:
  MySQL InnoDB: MVCC via undo log (dead versions in separate undo space)
  Oracle: MVCC via undo tablespace
  PostgreSQL: MVCC in-place in the heap (simpler but more VACUUM dependency)
```

---

**Q107. What are the four isolation levels and what anomalies do they prevent?**

```
ANOMALIES:

DIRTY READ: Reading uncommitted data from another transaction.
  TXN A writes X=10 (uncommitted). TXN B reads X=10. TXN A rolls back.
  TXN B saw data that never existed.

NON-REPEATABLE READ: Same row reads return different values in same transaction.
  TXN B reads user name = "Alice". TXN A updates name to "Bob" and commits.
  TXN B reads same user → "Bob". Data changed under TXN B.

PHANTOM READ: Same query returns different ROWS in same transaction.
  TXN B queries users WHERE age > 30 → 5 rows. 
  TXN A inserts a new user age=35 and commits.
  TXN B repeats query → 6 rows. A new "phantom" row appeared.

SERIALIZATION ANOMALY: Concurrent transactions produce result impossible in serial execution.

ISOLATION LEVEL PROTECTION:
                     DIRTY  NON-REP  PHANTOM  SERIAL
READ UNCOMMITTED      no     no       no       no    ← not in PG (treated as RC)
READ COMMITTED        YES    no       no       no    ← PG DEFAULT
REPEATABLE READ       YES    YES      YES*     no    ← PG also prevents phantoms
SERIALIZABLE          YES    YES      YES      YES

* PostgreSQL's REPEATABLE READ also prevents phantom reads (stronger than standard).

POSTGRESQL SPECIFICS:
  - READ UNCOMMITTED = READ COMMITTED (PostgreSQL never shows dirty reads)
  - SERIALIZABLE uses SSI (Serializable Snapshot Isolation):
    detects conflicts between concurrent txns and aborts the loser
    Full serializability WITHOUT blocking locks — just rollbacks on conflict

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN ISOLATION LEVEL SERIALIZABLE;
```

---

**Q108. What is a deadlock and how does PostgreSQL handle it?**

```
DEADLOCK: Two transactions each hold a lock the other needs.

TXN A: locks row 1, wants row 2
TXN B: locks row 2, wants row 1
Both wait forever → deadlock.

EXAMPLE:
  TXN A: UPDATE accounts SET balance=balance-100 WHERE id=1;  -- locks id=1
  TXN B: UPDATE accounts SET balance=balance-100 WHERE id=2;  -- locks id=2
  TXN A: UPDATE accounts SET balance=balance+100 WHERE id=2;  -- waits for B
  TXN B: UPDATE accounts SET balance=balance+100 WHERE id=1;  -- waits for A
  DEADLOCK!

POSTGRESQL'S DETECTION:
  PostgreSQL runs a deadlock detection algorithm periodically (deadlock_timeout, default 1s).
  When detected: PostgreSQL picks one transaction as the "victim" and aborts it.
  Victim gets: ERROR: deadlock detected
  The other transaction proceeds.

APPLICATION RESPONSE:
  Must catch deadlock error and retry the transaction.
  -- In psycopg2/asyncpg: catch DeadlockDetected exception
  -- In application code: retry with exponential backoff

PREVENTION STRATEGIES:
  1. Always acquire locks in the same order (e.g., always lock lower id first)
     TXN A: lock id=1 then id=2
     TXN B: lock id=1 then id=2 (same order → waits, no deadlock)

  2. Use SELECT ... FOR UPDATE to acquire all needed locks upfront

  3. Minimize transaction length — shorter transactions = shorter lock hold times

  4. Use NOWAIT or SKIP LOCKED to fail fast instead of waiting

-- Check for deadlocks in logs:
-- LOG: deadlock detected
-- DETAIL: Process 12345 waits for ...
```

---

**Q109. What is SELECT FOR UPDATE and when do you use it?**

```sql
-- SELECT FOR UPDATE acquires an exclusive row lock.
-- Other transactions cannot UPDATE or DELETE the locked row.
-- Other SELECT FOR UPDATE statements will wait.

-- USE CASE: Read-then-write atomicity

-- WITHOUT FOR UPDATE (race condition):
-- TXN A: reads balance = 1000
-- TXN B: reads balance = 1000
-- TXN A: writes balance = 900 (withdrew 100)
-- TXN B: writes balance = 900 (also withdrew 100 — based on stale read!)
-- Both succeeded, but only 100 was actually withdrawn. LOST UPDATE.

-- WITH FOR UPDATE:
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE; -- locks the row
-- TXN B also runs FOR UPDATE → waits here
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
-- TXN B gets lock, reads updated balance = 900, then withdraws correctly

-- VARIANTS:

FOR UPDATE:
  Exclusive lock. Prevents concurrent updates, deletes, and other FOR UPDATEs.

FOR SHARE:
  Shared lock. Prevents concurrent updates/deletes. Allows other FOR SHAREs.
  Use when you want to prevent deletion but allow concurrent readers.

FOR UPDATE SKIP LOCKED:
  If the row is already locked → skip it, don't wait.
  Perfect for JOB QUEUE pattern:
  SELECT id, payload FROM jobs WHERE status='pending'
  ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
  -- Each worker grabs a different unclaimed job, no contention.

FOR UPDATE NOWAIT:
  If the row is already locked → immediately raise an error (no waiting).
  For UIs where you want immediate feedback that a resource is in use.

FOR NO KEY UPDATE:
  Weaker than FOR UPDATE — compatible with FOR KEY SHARE.
  Doesn't block FK checks on the row.
```

---

**Q110. What is optimistic vs pessimistic locking?**

```
PESSIMISTIC LOCKING:
  Assume conflicts WILL happen → lock data before reading/writing.
  Implemented with: SELECT FOR UPDATE (row-level DB locks)
  
  Flow:
    BEGIN → SELECT FOR UPDATE → process → UPDATE → COMMIT

  Pros: guaranteed consistency, no retries needed
  Cons: locks held for duration of processing, blocks other transactions,
        can lead to deadlocks, poor throughput under high contention

OPTIMISTIC LOCKING:
  Assume conflicts are RARE → don't lock, just detect conflicts at update time.
  Implemented with: a version column (or updated_at timestamp)
  
  Flow:
    Read row (get version=5) → process → UPDATE WHERE version=5
    If 0 rows updated → someone else changed it → retry

  -- Schema:
  CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name TEXT,
    price NUMERIC(10,2),
    version INT NOT NULL DEFAULT 1
  );

  -- Application:
  -- 1. Read: SELECT id, name, price, version FROM products WHERE id=1;
  --    → version=5
  -- 2. Update:
  UPDATE products
  SET name='New Name', price=29.99, version=version+1
  WHERE id=1 AND version=5;
  --    → 0 rows affected = concurrent modification detected → retry
  --    → 1 row affected = success

  Pros: no locks held, high throughput, no deadlocks
  Cons: application must handle retries, worse under high contention

WHEN TO USE WHICH:
  Pessimistic: high contention, long processing time, financial operations
  Optimistic: low contention, short processing time, user-facing CRUD
```

---

## SECTION 6: POSTGRESQL INTERNALS

---

**Q126. How does PostgreSQL store data on disk?**

```
HEAP FILES:
  Each table is a file (or multiple files if > 1GB, split into segments).
  Location: $PGDATA/base/<database_oid>/<relation_oid>

  The file is divided into 8KB pages (blocks).
  Each page contains:
    - PageHeader (24 bytes): LSN, checksum, pd_lower, pd_upper, pd_special
    - ItemId array: offsets + lengths of each tuple (grows from start ↓)
    - Free space (between ItemIds and tuples)
    - Tuples (grow from end ↑)
    - Special area (used by indexes, empty for heap)

  Page layout:
  ┌──────────┬───────────────────┬──────────────┬──────────┐
  │ Header   │ ItemId[1][2][3]   │  Free space  │  Tuples  │
  │ (24 B)   │ (4B each) ────────►              ◄────────  │
  └──────────┴───────────────────┴──────────────┴──────────┘

TUPLE STRUCTURE (row):
  Each tuple (row version) contains:
  - HeapTupleHeader: xmin, xmax, cmin, cmax, ctid, natts, infomask
  - NULL bitmap (if any nullable columns)
  - Column data (fixed-length in declaration order, then variable-length)

ctid: physical location (page number, slot index) — not stable! Can change after VACUUM FULL.
xmin: XID that inserted this tuple version
xmax: XID that deleted this tuple version (0 = still live)

TOAST (The Oversized-Attribute Storage Technique):
  Values > ~2KB → compressed inline, or moved to a TOAST table.
  Transparent to queries. TOAST table: pg_toast_<reloid>
  Compression algorithms: pglz (default), lz4 (PG14+)
  Can also be stored external + compressed or external + plain (no compression).
```

---

**Q127. What is the WAL (Write-Ahead Log) and why is it critical?**

```
WAL = Write-Ahead Log (also called transaction log)

CORE PRINCIPLE: "Don't modify data on disk before writing to the log."

WHY WAL?
  Without WAL: crash during write → partial data on disk → corruption.
  With WAL: all changes written to WAL first (sequential, fast).
            If crash: replay WAL from last checkpoint → full recovery.

HOW IT WORKS:
  1. Transaction modifies data in shared_buffers (in-memory pages).
  2. BEFORE flushing modified page to disk, WAL record is written to WAL buffer.
  3. At COMMIT: WAL buffer is flushed to disk (fsync). Only then: commit confirmed.
  4. Background writer eventually flushes data pages to disk.
  5. At checkpoint: guarantee all WAL up to this point is on disk.

WAL BENEFITS:
  DURABILITY: committed data survives crashes (replayed from WAL)
  CRASH RECOVERY: replays WAL from last checkpoint
  REPLICATION: standbys receive and replay WAL stream
  PITR: Point-In-Time Recovery — restore to any moment using base backup + WAL

WAL FILES:
  Location: $PGDATA/pg_wal/
  Fixed size: 16MB per segment (configurable)
  Circular reuse: old segments deleted or archived

DURABILITY TRADEOFFS:
  synchronous_commit = on     → WAL flushed before COMMIT returns (safe)
  synchronous_commit = off    → COMMIT returns before WAL flush (~100ms risk)
  synchronous_commit = remote_apply → wait for standby to apply (no data loss)
  fsync = off                 → NEVER in production — data loss on crash

LSN (Log Sequence Number):
  64-bit monotonically increasing position in the WAL stream.
  Used to track replication lag, recovery progress.
  SELECT pg_current_wal_lsn(); -- current WAL position on primary
```

---

**Q128. What is autovacuum and why is it essential?**

```
AUTOVACUUM: a background daemon that automatically runs VACUUM and ANALYZE.
It's not optional — it's critical for database health.

WHY VACUUM IS NEEDED:
  MVCC creates dead tuples (old row versions no longer visible to any transaction).
  Dead tuples occupy space, slow down scans, bloat indexes.
  VACUUM reclaims them.

  Transaction ID wraparound: PostgreSQL uses 32-bit XIDs (~2.1B).
  Anti-wraparound VACUUM must periodically freeze old XIDs.
  Without it: catastrophic data loss when XIDs wrap around.

AUTOVACUUM TRIGGERS (per table):
  n_dead_tup > autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor × n_live_tup
  Default: 50 + 0.2 × table_rows
  i.e., when dead tuples exceed 20% of table + 50

AUTOVACUUM ANALYZE triggers:
  n_mod_since_analyze > autovacuum_analyze_threshold + autovacuum_analyze_scale_factor × n_live_tup
  Default: 50 + 0.1 × table_rows
  Keeps statistics current for the planner.

COMMON AUTOVACUUM PROBLEMS:
  - Too slow on large tables → tune autovacuum_vacuum_cost_delay
  - Blocked by long-running transactions (can't vacuum rows still visible to old txns)
  - Anti-wraparound vacuum can't be prevented — may cause load spikes

TUNING:
  autovacuum_vacuum_scale_factor = 0.05  -- trigger at 5% (default 20%, too high for large tables)
  autovacuum_max_workers = 5             -- more parallel workers
  autovacuum_vacuum_cost_delay = 2ms     -- less throttling (default 2ms, was 20ms in older PG)

MONITORING:
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze,
       autovacuum_count, autoanalyze_count
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;
```

---

## SECTION 7: ADVANCED FEATURES

---

**Q141. How does full-text search work in PostgreSQL?**

```sql
-- CORE COMPONENTS:

-- tsvector: processed document
-- Words → lexemes (normalized, stemmed, stop words removed)
SELECT to_tsvector('english', 'The quick brown fox jumped over the lazy dogs');
-- 'brown':3 'dog':9 'fox':4 'jump':5 'lazi':8 'quick':2
-- "The","over" are English stop words (ignored)
-- "jumped"→"jump", "lazy"→"lazi", "dogs"→"dog" (stemmed)

-- tsquery: processed search query
SELECT to_tsquery('english', 'jump & fox');        -- AND
SELECT to_tsquery('english', 'jump | cat');        -- OR
SELECT to_tsquery('english', 'fox & !cat');        -- AND NOT
SELECT to_tsquery('english', 'quick <-> fox');     -- FOLLOWED BY (adjacent)
SELECT plainto_tsquery('english', 'quick brown fox'); -- auto-AND
SELECT websearch_to_tsquery('english', '"quick fox"'); -- phrase

-- MATCH:
SELECT to_tsvector('english', 'quick brown fox') @@ to_tsquery('english', 'fox');
-- → true

-- FULL IMPLEMENTATION:
-- Option 1: Generated column (auto-updated)
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  search_vector TSVECTOR GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||  -- title = weight A (highest)
    setweight(to_tsvector('english', coalesce(body, '')), 'B')      -- body = weight B
  ) STORED
);
CREATE INDEX idx_articles_fts ON articles USING GIN(search_vector);

-- Option 2: Trigger-maintained column (older PG)
-- Option 3: Compute at query time (no stored column — simpler, less efficient)

-- SEARCH QUERY:
SELECT
  id, title,
  ts_rank(search_vector, query) AS relevance,
  ts_headline('english', body, query,
    'MaxWords=20, MinWords=10, StartSel=<b>, StopSel=</b>') AS snippet
FROM articles,
     websearch_to_tsquery('english', 'postgresql performance') AS query
WHERE search_vector @@ query
ORDER BY relevance DESC
LIMIT 10;

-- ts_rank: relevance score (higher = more relevant)
-- ts_headline: extract snippet with matched terms highlighted
```

---

**Q142. What is JSONB and what are its operators?**

```sql
-- JSONB: binary JSON format with indexing support
-- Always prefer JSONB over JSON (JSON is just stored text, no indexing, slower)

-- OPERATORS:
->     returns JSON value:    attributes->'color'     → "red" (JSON type)
->>    returns text value:    attributes->>'color'    → red   (text type)
#>     path to JSON:          attributes#>'{a,b}'     → nested value as JSON
#>>    path to text:          attributes#>>'{a,b}'    → nested value as text
@>     contains:              attributes @> '{"color":"red"}' → boolean
<@     is contained by:       '{"a":1}' <@ attributes
?      has key:               attributes ? 'color'
?|     has any key:           attributes ?| ARRAY['a','b']
?&     has all keys:          attributes ?& ARRAY['a','b']
||     concatenate/merge:     attributes || '{"new_key": "val"}'
-      remove key:            attributes - 'key'
#-     remove path:           attributes #- '{a,b}'

-- MODIFICATION FUNCTIONS:
jsonb_set(target, path, new_value)        -- set value at path
jsonb_set(target, '{price}', '39.99')
jsonb_insert(target, path, new_value)     -- insert at path (arrays)
jsonb_delete_path(target, path)           -- remove nested path

-- CONSTRUCTION:
jsonb_build_object('name', 'Alice', 'age', 30)  → {"name":"Alice","age":30}
jsonb_build_array(1, 2, 3)                       → [1,2,3]
row_to_json(table_row)                           → full row as JSON
to_jsonb(value)                                  → cast to JSONB

-- ITERATION:
jsonb_each(jsonb)               -- expand keys to rows: (key text, value jsonb)
jsonb_each_text(jsonb)          -- expand keys to rows: (key text, value text)
jsonb_object_keys(jsonb)        -- set of key names
jsonb_array_elements(jsonb)     -- expand array to rows of jsonb
jsonb_array_elements_text(jsonb)-- expand array to rows of text
jsonb_array_length(jsonb)       -- array length

-- INDEXING:
CREATE INDEX ON products USING GIN(attributes);           -- all keys
CREATE INDEX ON products((attributes->>'color'));         -- specific key (btree)
CREATE INDEX ON products USING GIN(attributes jsonb_path_ops); -- @> only, smaller
```

---

**Q143. What is table partitioning? When should you use it?**

```sql
-- PARTITIONING: split one logical table into multiple physical tables (child partitions).
-- From the application perspective: one table. Internally: multiple storage units.

-- WHEN TO PARTITION:
-- ✓ Table has hundreds of millions+ of rows
-- ✓ You routinely query or delete by a specific column (date, region, tenant)
-- ✓ Old data can be completely dropped (time-series, logs)
-- ✓ Individual partition indexes fit better in cache than one large index

-- WHEN NOT TO PARTITION:
-- Table is < 50M rows (overhead not worth it)
-- No clear partition key in your queries
-- You need cross-partition JOINs frequently

-- THREE TYPES:

-- RANGE (most common — for time-series, sequential data):
CREATE TABLE events (
  id BIGINT,
  user_id BIGINT,
  type TEXT,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_q1 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
CREATE TABLE events_2024_q2 PARTITION OF events
  FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
CREATE TABLE events_default PARTITION OF events DEFAULT;

-- LIST (for known discrete values):
CREATE TABLE orders (id BIGINT, region TEXT, total NUMERIC)
PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US', 'CA', 'MX');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('UK', 'DE', 'FR');

-- HASH (for even distribution — sharding without range logic):
CREATE TABLE users (id BIGINT, email TEXT)
PARTITION BY HASH (id);

CREATE TABLE users_0 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE users_1 PARTITION OF users FOR VALUES WITH (MODULUS 4, REMAINDER 1);
-- ... etc.

-- PARTITION PRUNING:
-- The planner automatically skips irrelevant partitions.
EXPLAIN SELECT * FROM events WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01';
-- Shows: "Partitions selected: events_2024_q1" — others excluded

-- INSTANT DROP (huge advantage for time-series):
DROP TABLE events_2024_q1;  -- instant, no VACUUM needed
-- vs DELETE FROM events WHERE created_at < '2024-04-01'; -- slow, needs VACUUM

-- DETACH (keep data but remove from partitioned table):
ALTER TABLE events DETACH PARTITION events_2024_q1;
```

---

## SECTION 8: SCHEMA DESIGN

---

**Q156. What is database normalization? Explain 1NF, 2NF, 3NF.**

```
NORMALIZATION: process of organizing a database to reduce redundancy
and improve data integrity. Each normal form eliminates a specific type of problem.

FIRST NORMAL FORM (1NF):
  Rules:
    - Each column contains atomic (indivisible) values
    - No repeating groups
    - All rows are unique (have a primary key)

  VIOLATION:
    orders: id=1, items="Laptop,Mouse,Keyboard", quantities="1,2,1"
    items and quantities are multi-valued — not atomic.

  FIX:
    orders(id, customer_id)
    order_items(order_id, item_name, quantity)

SECOND NORMAL FORM (2NF):
  Rules:
    - Must be in 1NF
    - Every non-key column depends on the ENTIRE primary key (no partial dependency)
    - Only relevant when primary key is composite

  VIOLATION (composite PK: order_id + product_id):
    order_items(order_id, product_id, quantity, product_name, product_price)
    product_name depends only on product_id — NOT on the full (order_id, product_id)
    This is a PARTIAL DEPENDENCY → 2NF violation.

  FIX:
    order_items(order_id, product_id, quantity)
    products(product_id, product_name, product_price)

THIRD NORMAL FORM (3NF):
  Rules:
    - Must be in 2NF
    - No transitive dependencies (non-key → non-key → primary key is not allowed)

  VIOLATION:
    employees(id, dept_id, dept_name, dept_location)
    dept_name depends on dept_id, which depends on id (the PK).
    dept_name has a TRANSITIVE DEPENDENCY through dept_id.

  FIX:
    employees(id, dept_id)
    departments(dept_id, dept_name, dept_location)

DENORMALIZATION (intentional violations):
  Sometimes break normal forms for performance.
  Example: store customer_email in orders (snapshot at order time)
  Even though email is in users table — prevents broken order history if email changes.
  RULE: always document WHY, add a comment in migration.
```

---

**Q157. How do you design a schema for a multi-tenant application?**

```sql
-- THREE MAIN APPROACHES:

-- APPROACH 1: ROW-LEVEL MULTITENANCY (shared tables, tenant_id column)
-- All tenants share the same tables. tenant_id on every row.
CREATE TABLE organizations (id BIGINT PRIMARY KEY, name TEXT);
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  org_id BIGINT NOT NULL REFERENCES organizations(id),
  email TEXT NOT NULL,
  UNIQUE (org_id, email)  -- email unique per tenant, not globally
);
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  org_id BIGINT NOT NULL REFERENCES organizations(id),
  user_id BIGINT NOT NULL REFERENCES users(id),
  total NUMERIC(10,2)
);

-- Indexes MUST include org_id first:
CREATE INDEX ON users(org_id, email);
CREATE INDEX ON orders(org_id, user_id);

-- Row Level Security (PostgreSQL) — enforce tenant isolation at DB level:
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (org_id = current_setting('app.current_org_id')::BIGINT);

-- Application: SET app.current_org_id = '42' at session start.
-- Now all queries on orders automatically filter to org 42.

Pros: simple, one schema, easy to add tenants
Cons: tenant isolation is at app/policy level, cross-tenant queries easier to leak

-- APPROACH 2: SCHEMA-PER-TENANT
-- Each tenant gets their own PostgreSQL schema (namespace).
CREATE SCHEMA tenant_42;
CREATE TABLE tenant_42.orders (...);
-- search_path = tenant_42 for that tenant's session.

Pros: physical isolation, easy per-tenant backup/restore
Cons: schema management overhead, hard to query across tenants

-- APPROACH 3: DATABASE-PER-TENANT
-- Separate PostgreSQL database per tenant.
Pros: full isolation, different versions per tenant, easy data deletion
Cons: connection pooling complexity, much higher infrastructure cost

RECOMMENDATION:
  < 1000 tenants with similar sizes → Row-level + RLS (most practical)
  Regulated/enterprise customers demanding isolation → Schema-per-tenant
  Different data models per tenant → Database-per-tenant
```

---

**Q158. What is the N+1 query problem and how do you solve it?**

```
THE PROBLEM:
  1 query to get a list of N items.
  Then N individual queries to get related data for each item.
  Total: N+1 queries. Performance killer.

EXAMPLE (in application code):
  users = db.query("SELECT id, name FROM users LIMIT 100")  -- 1 query
  for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")  -- 100 queries
    # Total: 101 queries — instead of 2!

SOLUTIONS:

1. JOIN — load related data in one query:
   SELECT u.id, u.name, o.id AS order_id, o.total
   FROM users u
   LEFT JOIN orders o ON u.id = o.user_id
   LIMIT 100;
   -- 1 query, returns flat result with all data

2. IN BATCH — fetch related records for all IDs at once:
   -- First query:
   SELECT id, name FROM users LIMIT 100;
   -- Collect IDs: [1, 2, 3, ..., 100]
   -- Second query:
   SELECT * FROM orders WHERE user_id IN (1, 2, 3, ..., 100);
   -- Group in application by user_id → 2 queries total

3. ARRAY_AGG / JSON_AGG — aggregate in DB:
   SELECT
     u.id, u.name,
     JSON_AGG(JSON_BUILD_OBJECT('id', o.id, 'total', o.total)) AS orders
   FROM users u
   LEFT JOIN orders o ON u.id = o.user_id
   GROUP BY u.id, u.name
   LIMIT 100;
   -- 1 query, returns each user with embedded orders array

DETECTION:
  Watch your query count per request in logs.
  Set query count threshold in APM (Datadog, New Relic).
  In development: use pg_stat_statements to spot repeated queries.

RULE: If you're looping in application code and making DB calls → N+1 alert.
```

---

**Q159. When would you use JSONB vs a relational column?**

```
USE RELATIONAL COLUMNS WHEN:
  ✓ You query, filter, or sort by this data regularly
     WHERE product_name = 'Widget' → needs indexed column, not JSONB key
  ✓ You need foreign key constraints (no FK on JSONB keys)
  ✓ You need NOT NULL constraints on specific fields
  ✓ Data structure is stable and well-defined
  ✓ Aggregations on this data (SUM, AVG → harder with JSONB)
  ✓ Most rows have this data (not sparse)

USE JSONB WHEN:
  ✓ Schema is flexible / varies per row (e-commerce attributes: shirts have size+color,
    electronics have RAM+storage — different keys per product type)
  ✓ Schema evolves rapidly (adding a new attribute = no migration)
  ✓ You primarily store/retrieve the whole blob, not query individual keys
  ✓ Third-party data with variable structure
  ✓ Sparse optional metadata (most rows won't have most keys)
  ✓ Prototyping (figure out structure before committing to schema)

ANTI-PATTERNS:
  Bad: storing user's name in JSONB when you filter by name constantly
  Bad: storing order total in JSONB when you SUM it in reports
  Good: storing product's variant attributes (color, size, material) in JSONB
  Good: storing audit log details as JSONB (flexible, append-only)

HYBRID APPROACH (common in practice):
  CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,            -- relational: queried, indexed
    price NUMERIC(10,2) NOT NULL,  -- relational: summed, sorted
    category_id INT REFERENCES ...,-- relational: FK, filtered
    attributes JSONB               -- JSONB: flexible variant data
  );
  -- Index frequently queried JSONB keys:
  CREATE INDEX ON products((attributes->>'color'));
```

---

**Q160. What are the most important production PostgreSQL monitoring queries?**

```sql
-- 1. SLOW QUERIES (requires pg_stat_statements)
CREATE EXTENSION pg_stat_statements;
SELECT
  LEFT(query, 100) AS query_snippet,
  calls,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  ROUND((100 * total_exec_time / SUM(total_exec_time) OVER ())::numeric, 2) AS pct_total
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 2. TABLE BLOAT / VACUUM HEALTH
SELECT relname, n_live_tup, n_dead_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- 3. INDEX USAGE (find unused indexes)
SELECT schemaname, tablename, indexname, idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 100
ORDER BY pg_relation_size(indexrelid) DESC;

-- 4. TABLE & INDEX SIZES
SELECT relname,
  pg_size_pretty(pg_relation_size(relid)) AS table_size,
  pg_size_pretty(pg_indexes_size(relid)) AS indexes_size,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- 5. ACTIVE CONNECTIONS & LONG-RUNNING QUERIES
SELECT pid, now() - pg_stat_activity.query_start AS duration,
  state, query
FROM pg_stat_activity
WHERE state != 'idle' AND query_start IS NOT NULL
ORDER BY duration DESC;

-- 6. BLOCKING QUERIES (who is blocking whom)
SELECT blocked.pid, blocked.query, blocking.pid AS blocking_pid, blocking.query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;

-- 7. TRANSACTION ID WRAPAROUND (CRITICAL — check monthly)
SELECT datname, age(datfrozenxid) AS xid_age,
  2000000000 - age(datfrozenxid) AS xids_remaining
FROM pg_database ORDER BY age(datfrozenxid) DESC;
-- Alert if xid_age > 1,500,000,000

-- 8. REPLICATION LAG
SELECT
  application_name,
  pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn)) AS lag_bytes,
  now() - reply_time AS lag_time
FROM pg_stat_replication;

-- 9. CACHE HIT RATE (should be > 99%)
SELECT
  SUM(heap_blks_hit) / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0) * 100 AS table_cache_hit_pct,
  SUM(idx_blks_hit)  / NULLIF(SUM(idx_blks_hit)  + SUM(idx_blks_read),  0) * 100 AS index_cache_hit_pct
FROM pg_statio_user_tables;

-- 10. LOCKS (identify contention)
SELECT pid, relation::regclass, mode, granted, query
FROM pg_locks l
JOIN pg_stat_activity a ON a.pid = l.pid
WHERE relation IS NOT NULL
ORDER BY granted, relation;
```

---

---

## SECTION 9: BACKUP, RECOVERY & OPERATIONS (Gap-Fill)

---

**Q161. What is logical replication and how does it differ from physical (streaming) replication?**

```
PHYSICAL REPLICATION (Streaming):
  Replicates at the BLOCK level — raw WAL bytes.
  The standby is a byte-for-byte copy of the primary.
  Uses WAL sender/receiver processes.
  Standby must be the same PostgreSQL major version (usually).
  Standby can only be read-only — cannot write at all.
  Replicates EVERYTHING: all databases, all tables, all DDL.

LOGICAL REPLICATION:
  Replicates at the ROW level — decoded as INSERT/UPDATE/DELETE operations.
  Uses the logical decoding feature of WAL.
  Can replicate SELECTIVE tables (not the whole cluster).
  Subscriber can write to tables NOT being replicated.
  Works ACROSS major PostgreSQL versions (e.g., PG14 → PG15 upgrade).
  Cannot replicate DDL (schema changes must be applied manually).
  Cannot replicate sequences directly.

ARCHITECTURE:
  PRIMARY                            SUBSCRIBER
  ┌────────────────────┐             ┌──────────────────────┐
  │  Publication       │             │  Subscription        │
  │  (selected tables) │──WAL────▶  │  (apply worker)      │
  │                    │  logical    │  receives rows,      │
  │  WAL decoder       │  stream     │  applies as DML      │
  └────────────────────┘             └──────────────────────┘

SETUP:
  -- On primary (postgresql.conf):
  wal_level = logical   ← required (physical only needs 'replica')

  -- On primary: create publication
  CREATE PUBLICATION my_pub FOR TABLE users, orders;
  CREATE PUBLICATION all_tables FOR ALL TABLES;

  -- On subscriber: create subscription
  CREATE SUBSCRIPTION my_sub
    CONNECTION 'host=primary dbname=mydb user=replicator password=secret'
    PUBLICATION my_pub;

  -- Monitor:
  SELECT * FROM pg_stat_replication;      -- on primary
  SELECT * FROM pg_stat_subscription;     -- on subscriber

USE CASES FOR LOGICAL REPLICATION:
  ✓ Zero-downtime major version upgrades (replicate to new PG version, switchover)
  ✓ Replicate specific tables to an analytics database
  ✓ Data pipelines (Debezium uses logical replication for CDC)
  ✓ Partial replication (multitenancy — replicate only one tenant's tables)
  ✓ Fan-out: one primary → multiple subscribers with different subsets

LIMITATIONS:
  ✗ Cannot replicate sequences (fix: set up manual sequence sync or use UUIDs)
  ✗ Cannot replicate DDL (must apply schema changes on subscriber first)
  ✗ Tables must have a PRIMARY KEY or REPLICA IDENTITY for UPDATE/DELETE
  ✗ Large objects (lo_*) not replicated
```

---

**Q162. What is Point-in-Time Recovery (PITR) and how does it work?**

```
PITR = ability to restore a database to ANY specific moment in time.
Not just "last backup" — but any second within the WAL archive window.

WHY IT EXISTS:
  "Oops, someone ran DROP TABLE users at 14:32:47."
  PITR lets you restore to 14:32:46 — one second before the mistake.

HOW IT WORKS:
  1. BASE BACKUP: periodic full snapshot of the cluster data directory.
     pg_basebackup -h localhost -U replicator -D /backups/base -Ft -z -Xs -P

  2. WAL ARCHIVE: continuously ship WAL segments to archive storage as they complete.
     archive_mode = on
     archive_command = 'aws s3 cp %p s3://my-bucket/wal/%f'
     # %p = path to WAL file, %f = file name

  3. RECOVERY: copy base backup, replay archived WAL up to target point.
     recovery_target_time = '2024-01-15 14:32:46'
     -- or:
     recovery_target_lsn = 'A/B3C00000'    -- specific WAL position
     recovery_target_transaction = 12345    -- specific XID
     recovery_target_name = 'before_migration'  -- named restore point

RECOVERY PROCESS:
  1. Stop PostgreSQL on recovery target server
  2. Restore base backup to data directory
  3. Create recovery.conf (PG11-) or postgresql.conf entries (PG12+):

     restore_command = 'aws s3 cp s3://my-bucket/wal/%f %p'
     recovery_target_time = '2024-01-15 14:32:46'
     recovery_target_action = 'promote'  -- become primary after recovery

  4. Start PostgreSQL → it replays WAL until the target point → stops
  5. Verify data, then promote to writable

KEY CONFIG PARAMETERS:
  archive_mode = on                    -- enables WAL archiving
  archive_command = 'cp %p /wal/%f'   -- command to archive each WAL segment
  archive_cleanup_command              -- cleanup old archived WAL
  restore_command                      -- command to retrieve archived WAL during recovery
  wal_keep_size                        -- keep N MB of WAL locally as buffer

TOOLS THAT AUTOMATE PITR:
  pgBackRest — enterprise-grade, parallel backup/restore, S3 support
  WAL-G — open source, cloud-native, very fast
  Barman — backup and recovery manager

RTO (Recovery Time Objective) considerations:
  Large base backup + many WAL segments = long replay = high RTO
  Reduce by: more frequent base backups, streaming standby as warm spare
```

---

**Q163. What is PgBouncer and why is it essential for production PostgreSQL?**

```
PROBLEM:
  PostgreSQL is PROCESS-based — each connection = one OS process.
  Creating a process is expensive: ~5-10ms, ~5-10MB RAM.
  100 connections = 100 processes, 500-1000MB RAM just for connection overhead.
  Applications (especially web servers) open many short-lived connections.
  Result: constant fork overhead, high memory usage, PostgreSQL degradation.

PGBOUNCER:
  A lightweight connection pooler that sits between app and PostgreSQL.
  Maintains a small pool of long-lived connections to PostgreSQL.
  Applications connect to PgBouncer — PgBouncer routes to PostgreSQL.
  PgBouncer is single-process, event-driven (libevent) — very efficient.

ARCHITECTURE:
  App server (100 threads)        PgBouncer           PostgreSQL
  ──────────────────────          ──────────           ──────────
  conn 1  ──┐                     pool of 10     ───▶  10 backend
  conn 2  ──┤                     real PG conns         processes
  conn 3  ──┤──▶  PgBouncer ──▶
  ...     ──┤
  conn 100──┘
  100 app connections         PgBouncer holds 10 real PG connections
  
POOLING MODES (critical to understand):

SESSION POOLING (default):
  Client gets one server connection for its entire session.
  Connection returned to pool only when client disconnects.
  Least connection savings. Works with all features (prepared statements, SET, etc.)

TRANSACTION POOLING (most common for OLTP):
  Client holds server connection only during an active transaction.
  Between transactions: connection returned to pool immediately.
  Best connection multiplexing — 1000 app connections → 20 PG connections.
  LIMITATION: Cannot use session-level features:
    ✗ SET variable persists (session state lost between transactions)
    ✗ LISTEN/NOTIFY
    ✗ Prepared statements (require workaround with server_reset_query)
    ✗ Advisory locks

STATEMENT POOLING (rarely used):
  Connection returned after every single statement.
  Most aggressive multiplexing but breaks multi-statement transactions.

PGBOUNCER CONFIG (pgbouncer.ini):
  [databases]
  myapp = host=postgres-primary port=5432 dbname=myapp

  [pgbouncer]
  listen_port = 6432
  listen_addr = *
  auth_type = md5
  auth_file = /etc/pgbouncer/userlist.txt
  pool_mode = transaction
  max_client_conn = 1000       -- max app connections to PgBouncer
  default_pool_size = 20       -- real PG connections per database/user pair
  min_pool_size = 5            -- keep at least 5 open
  reserve_pool_size = 5        -- emergency extra connections
  server_idle_timeout = 600    -- close idle server connections after 10min

MONITORING:
  SHOW POOLS;      -- pool utilization
  SHOW STATS;      -- request rates, latency
  SHOW CLIENTS;    -- current app connections
  SHOW SERVERS;    -- current PG backend connections
  
ALTERNATIVES: Odyssey (Yandex), pgpool-II (also does load balancing/HA)
```

---

**Q164. What is BRIN index in depth? When does it outperform a B-Tree?**

```
BRIN = Block Range INdex

HOW IT WORKS:
  Instead of indexing every value, BRIN stores SUMMARY information
  (min + max values) for each "block range" (group of consecutive heap pages).
  Default: 128 pages per range (128 × 8KB = 1MB of heap per range entry).

  TABLE (append-only events, ordered by created_at):
  Pages 1-128:   min_created_at='2024-01-01', max_created_at='2024-01-05'
  Pages 129-256: min_created_at='2024-01-05', max_created_at='2024-01-10'
  Pages 257-384: min_created_at='2024-01-10', max_created_at='2024-01-15'

  QUERY: WHERE created_at = '2024-01-07'
  BRIN: check each range → '2024-01-07' in [01-05, 01-10]? Yes → scan pages 129-256
  Skip ranges where query value is outside [min, max].

SIZE COMPARISON:
  B-Tree on 1 billion row table: ~21 GB
  BRIN on same table: ~3 MB (10,000x smaller!)

  Why so small? BRIN stores 1 entry per 128 pages (~1000 rows).
  Entire BRIN fits in a single shared_buffers page in most cases.

WHEN BRIN OUTPERFORMS B-TREE:
  ✓ Very large tables (hundreds of millions to billions of rows)
  ✓ Data is naturally correlated with physical order (i.e., inserted in order)
    - Time-series: events inserted with increasing timestamp
    - Log tables: log_id increases with time
    - IoT sensor data: sensor_time is always increasing
  ✓ Queries that filter on the ordered column (date ranges especially)
  ✓ Write-heavy tables (B-Tree has significant write overhead; BRIN is almost free)

WHEN BRIN IS BAD:
  ✗ Data is NOT ordered (e.g., user_id inserted randomly)
    → BRIN ranges will overlap widely → almost every range matches → full scan
  ✗ High-selectivity point queries (WHERE created_at = '2024-01-07 15:32:01')
    → BRIN gives you a 1MB range to scan; B-Tree gives you 1 page
  ✗ Small tables (B-Tree overhead is fine, BRIN offers no advantage)

CORRELATION CHECK (is your data suited for BRIN?):
  SELECT attname, correlation FROM pg_stats
  WHERE tablename = 'events' AND attname = 'created_at';
  -- correlation close to 1.0 → data is naturally sorted → BRIN is great
  -- correlation close to 0   → data is random → BRIN is useless

CREATE BRIN INDEX:
  CREATE INDEX idx_events_brin ON events USING BRIN(created_at);
  -- Optional: tune pages_per_range (smaller = more precise, larger index)
  CREATE INDEX idx_events_brin ON events USING BRIN(created_at) WITH (pages_per_range=64);

MAINTENANCE:
  BRIN index is NOT automatically updated for new pages until vacuumed.
  Use: SELECT brin_summarize_new_values('idx_events_brin'); -- scan new pages
  Or: autovacuum handles it automatically.
```

---

**Q165. What is TOAST and how does it affect large text and JSONB columns?**

```
TOAST = The Oversized-Attribute Storage Technique

THE PROBLEM:
  PostgreSQL stores rows in 8KB pages.
  A single row cannot exceed ~2KB if it must fit with other rows efficiently.
  But TEXT, JSONB, BYTEA values can be megabytes or gigabytes.

THE SOLUTION: TOAST
  Large values are automatically broken out of the main table (heap) and
  stored in a separate "TOAST table": pg_toast_<relation_oid>.
  The main row stores a "toast pointer" (18 bytes) referencing the actual value.
  Completely transparent to SQL queries — you never interact with TOAST directly.

THRESHOLD:
  Values > ~2KB (TOAST_TUPLE_THRESHOLD) are candidates for toasting.
  This is not per-column — it's per-ROW. If the full row > 2KB, Postgres
  applies TOAST strategies to try to fit it in one page.

TOAST STRATEGIES (per column):
  PLAIN:    no compression, no out-of-line storage. For short fixed types (INT, BOOL).
  EXTENDED: try compression first; if still too big, move out-of-line. DEFAULT for TEXT/JSONB.
  EXTERNAL: move out-of-line immediately, no compression. For BYTEA when you want no CPU.
  MAIN:     try compression; keep inline if possible. Only move out-of-line as last resort.

COMPRESSION:
  Default: pglz (always available)
  PG14+: lz4 (faster compression/decompression — configure with default_toast_compression)
  SET default_toast_compression = 'lz4'; -- use lz4 for new toasted values

PERFORMANCE IMPLICATIONS:
  ✓ TOAST allows rows larger than 8KB — enabling large document storage
  ✓ Compression often reduces actual storage by 50-80% for text/JSON
  ✗ TOAST access requires extra heap fetch (random I/O to TOAST table)
  ✗ Large JSONB values → heavy TOAST I/O on every read
  ✗ SELECTing wide JSONB columns in large result sets can be very slow

PRACTICAL ADVICE:
  -- Check TOAST table size:
  SELECT
    relname AS toast_table,
    pg_size_pretty(pg_relation_size(oid)) AS size
  FROM pg_class WHERE relkind = 't';

  -- Change strategy for a column:
  ALTER TABLE articles ALTER COLUMN body SET STORAGE EXTERNAL;
  -- EXTERNAL: skip compression (faster decompression, larger storage)

  -- Avoid SELECTing wide JSONB columns when you only need a key:
  SELECT attributes->>'color' FROM products; -- reads only needed part
  -- vs:
  SELECT attributes FROM products;           -- fetches entire TOAST value

  -- For large binary data: consider storing file paths and using object storage
  -- (S3/MinIO) instead of BYTEA columns.
```

---

**Q166. What is pg_repack and how does it differ from VACUUM FULL?**

```
THE PROBLEM WITH VACUUM FULL:
  After massive DELETEs or UPDATEs, tables accumulate bloat (dead space).
  Regular VACUUM reclaims space for reuse but does NOT return it to the OS.
  VACUUM FULL rewrites the entire table and returns space to OS.

  BUT: VACUUM FULL requires ACCESS EXCLUSIVE LOCK — blocks ALL queries.
  On a 500GB table: VACUUM FULL may take hours. Hours of downtime. Unacceptable.

PG_REPACK:
  An extension that rewrites a table (and its indexes) online — WITH NO LOCKS.
  (A very brief lock at the end only, for a few milliseconds.)

HOW PG_REPACK WORKS:
  1. Creates a new empty table (same structure as original)
  2. Copies existing rows in bulk (background, non-blocking)
  3. Creates a trigger on the original table to log new changes (INSERT/UPDATE/DELETE)
     into a log table while copying is in progress
  4. After bulk copy: replays the logged changes onto the new table
  5. Atomically swaps old table with new table (brief exclusive lock — milliseconds)
  6. Drops old table

  The exclusive lock is held only during step 5 — typically < 100ms.
  Rest of the process: no blocking.

USAGE:
  -- Install:
  CREATE EXTENSION pg_repack;

  -- Repack a table (online, non-blocking):
  pg_repack -h localhost -U postgres -d mydb -t users

  -- Repack all tables in a database:
  pg_repack -h localhost -U postgres -d mydb

  -- Repack only indexes (if only index bloat, table is fine):
  pg_repack -h localhost -U postgres -d mydb -t users --only-indexes

  -- Dry run (see what would happen):
  pg_repack -h localhost -U postgres -d mydb -t users --dry-run

REQUIREMENTS:
  - Table must have a PRIMARY KEY or UNIQUE NOT NULL constraint
  - Sufficient disk space (temporary copy of table during repack)
  - pg_repack installed on both client and server

WHEN TO USE:
  VACUUM (regular): routine dead tuple cleanup — always running via autovacuum
  VACUUM FULL: only when offline maintenance window is acceptable (rare)
  pg_repack: when table is severely bloated and downtime is not an option

BLOAT DETECTION (before deciding to repack):
  CREATE EXTENSION pgstattuple;
  SELECT * FROM pgstattuple('users');
  -- Check: dead_tuple_percent > 20% → consider repack
  -- Check: free_percent > 20% → table has bloat worth reclaiming
```

---

**Q167. How do you tune autovacuum for a large, heavily updated table?**

```sql
-- DEFAULT AUTOVACUUM is tuned for "average" tables.
-- For large (100M+ rows) or heavily updated tables, defaults are too conservative.

-- DEFAULT TRIGGER:
-- autovacuum fires when: dead_tuples > 50 + 0.2 × n_live_tup
-- On a 100M row table: 50 + 0.2 × 100M = 20,000,050 dead tuples before vacuum!
-- That's 20 million dead tuples accumulating before cleanup.

-- APPROACH 1: Per-table autovacuum settings (preferred)
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,   -- fire at 1% dead tuples (not 20%)
  autovacuum_vacuum_threshold = 1000,      -- always fire if > 1000 dead tuples
  autovacuum_analyze_scale_factor = 0.005, -- analyze at 0.5% changed rows
  autovacuum_vacuum_cost_delay = 2,        -- ms of sleep between cost units (2ms = faster)
  autovacuum_vacuum_cost_limit = 400       -- cost limit before sleeping (default 200)
);

-- APPROACH 2: Global settings in postgresql.conf (affects all tables)
autovacuum_vacuum_scale_factor = 0.05      -- 5% (down from 20%)
autovacuum_vacuum_threshold = 1000
autovacuum_max_workers = 5                 -- more parallel workers (default 3)
autovacuum_vacuum_cost_delay = 2ms         -- less throttling (was 20ms in older versions)
autovacuum_vacuum_cost_limit = 400         -- default 200

-- COST-BASED THROTTLING:
-- Autovacuum intentionally slows itself down to avoid impacting live queries.
-- autovacuum_vacuum_cost_limit: total cost budget before sleeping
-- autovacuum_vacuum_cost_delay: sleep duration after hitting budget
-- vacuum_cost_page_hit = 1    (page from shared_buffers)
-- vacuum_cost_page_miss = 2   (page from disk)
-- vacuum_cost_page_dirty = 20 (dirty page write)
-- Lower cost_delay + higher cost_limit = vacuum runs faster (more I/O impact)
-- Higher cost_delay + lower cost_limit = vacuum runs slower (less I/O impact)

-- MONITORING autovacuum effectiveness:
SELECT
  relname,
  n_live_tup,
  n_dead_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
  last_vacuum,
  last_autovacuum,
  vacuum_count,
  autovacuum_count,
  last_analyze,
  last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- DETECT if autovacuum is being blocked by long transactions:
SELECT pid, now() - xact_start AS txn_duration, query, state
FROM pg_stat_activity
WHERE state != 'idle' AND xact_start < NOW() - INTERVAL '10 minutes'
ORDER BY txn_duration DESC;
-- Long-running transactions prevent autovacuum from cleaning up rows
-- they still have visibility over.

-- FORCE MANUAL VACUUM (for immediate cleanup):
VACUUM (VERBOSE, ANALYZE) orders;

-- VACUUM FREEZE (for XID wraparound prevention):
VACUUM FREEZE orders;
-- Sets xmin of all rows to FrozenXID — safe for all future transactions.
-- autovacuum does this automatically when age(datfrozenxid) gets high.
```

---

**Q168. How does pg_dump and pg_restore work? What are the key options?**

```
pg_dump: exports a PostgreSQL database to a file (logical backup).
pg_restore: restores from a non-plain-text pg_dump archive.
pg_dumpall: dumps ALL databases + global objects (roles, tablespaces).

pg_dump OUTPUT FORMATS:
  plain (-Fp):   SQL text file. Restore with: psql < dump.sql
  custom (-Fc):  Compressed binary. Restore with: pg_restore. Supports parallel restore.
  directory (-Fd): One file per table. Supports parallel dump AND restore.
  tar (-Ft):     Tar archive. Supports pg_restore but not parallel.

RECOMMENDED for production: CUSTOM or DIRECTORY format.

BASIC USAGE:
  -- Dump entire database (custom format, compressed):
  pg_dump -h localhost -U postgres -d mydb -Fc -f mydb.dump

  -- Dump specific tables only:
  pg_dump -h localhost -U postgres -d mydb -t users -t orders -Fc -f partial.dump

  -- Dump schema only (no data):
  pg_dump -h localhost -U postgres -d mydb --schema-only -f schema.sql

  -- Dump data only (no schema):
  pg_dump -h localhost -U postgres -d mydb --data-only -Fc -f data.dump

  -- Parallel directory dump (4 workers — much faster for large DBs):
  pg_dump -h localhost -U postgres -d mydb -Fd -j 4 -f mydb_dir/

RESTORE:
  -- Full restore from custom format:
  pg_restore -h localhost -U postgres -d mydb_new mydb.dump

  -- Parallel restore (4 workers — custom or directory format only):
  pg_restore -h localhost -U postgres -d mydb_new -j 4 mydb.dump

  -- Restore only specific tables:
  pg_restore -h localhost -U postgres -d mydb_new -t users mydb.dump

  -- List contents of dump (without restoring):
  pg_restore --list mydb.dump

  -- Restore as transaction (all-or-nothing):
  pg_restore -h localhost -U postgres -d mydb_new --single-transaction mydb.dump

KEY DIFFERENCES FROM PITR:
  pg_dump: logical backup — data at a single consistent point in time.
    Portable across major versions. Can restore specific tables.
    No WAL needed. Requires re-importing all data.
    Slow for very large databases.

  PITR (base backup + WAL): physical backup.
    Very fast restore for large databases (just copy files + replay WAL).
    Cannot restore specific tables — it's the whole cluster.
    Requires same major PostgreSQL version.
    Enables restore to any point in time, not just backup time.

PRODUCTION BACKUP STRATEGY (layered):
  1. Continuous WAL archiving + periodic base backups (PITR) — primary recovery
  2. Daily/weekly pg_dump — for cross-version migration, partial restore, offsite storage
  3. Logical replication standby — for near-zero RTO failover
```

---

**Q169. What is GIN fastupdate and when should you tune it?**

```
GIN INDEX WRITE PROBLEM:
  GIN (Generalized Inverted Index) maps each element → set of matching row IDs.
  When you INSERT a row with 10 tags, GIN must update up to 10 index entries.
  This is expensive — each update may cause tree rebalancing.
  On heavy-write tables (e.g., article tagging, JSONB inserts): GIN updates slow writes.

GIN FASTUPDATE:
  A write-optimization feature that buffers GIN index updates in a "pending list."
  Instead of updating the tree immediately, inserts go to a flat list.
  The pending list is merged into the main index periodically:
    - Automatically during any GIN index scan
    - Automatically during autovacuum

  TRADEOFF:
    Faster writes (no immediate tree update)
    Slightly slower reads (must check both tree AND pending list)
    Pending list can grow large → eventually merged, causing a write spike

CREATE INDEX idx_products_gin ON products USING GIN(attributes)
WITH (fastupdate = on);   -- DEFAULT: on

-- Turn off for read-heavy, write-light tables (reads skip pending list check):
CREATE INDEX idx_products_gin ON products USING GIN(attributes)
WITH (fastupdate = off);

-- Check and flush pending list manually:
SELECT gin_clean_pending_list('idx_products_gin');

-- Control max pending list size:
gin_pending_list_limit = 4MB  -- postgresql.conf or per-index
-- When pending list exceeds this → immediate merge (can cause write latency spike)
-- Increase to delay merges on write-heavy tables:
CREATE INDEX idx ON table USING GIN(col) WITH (fastupdate=on, gin_pending_list_limit=32768);
-- 32768 = 32MB

WHEN TO TUNE:
  ✓ Write-heavy tables with GIN indexes (tagging, full-text, JSONB)
    → keep fastupdate=on, increase gin_pending_list_limit
  ✓ Read-heavy tables with occasional writes
    → consider fastupdate=off for more predictable read latency
  ✓ Experiencing write latency spikes?
    → likely pending list being flushed; increase limit or schedule manual flush
```

---

**Q170. How do you create and manage time-series partitions automatically?**

```sql
-- PostgreSQL does NOT auto-create new partitions — you must do it in advance.
-- Three approaches:

-- APPROACH 1: pg_partman extension (production standard)
-- pg_partman automates partition creation and maintenance.
  CREATE EXTENSION pg_partman;

  -- Tell pg_partman to manage your partitioned table:
  SELECT partman.create_parent(
    p_parent_table  => 'public.events',
    p_control       => 'created_at',
    p_type          => 'native',
    p_interval      => 'monthly',
    p_premake       => 4           -- create 4 future partitions in advance
  );

  -- Run pg_partman's background worker (or call manually):
  SELECT partman.run_maintenance_proc();
  -- This: creates needed future partitions, drops/detaches old ones if configured

  -- Configure retention (auto-drop partitions older than 12 months):
  UPDATE partman.part_config
  SET retention = '12 months',
      retention_keep_table = false  -- actually drop (not just detach)
  WHERE parent_table = 'public.events';

-- APPROACH 2: Scheduled stored procedure (no extension)
CREATE OR REPLACE PROCEDURE create_monthly_partitions(months_ahead INT DEFAULT 3)
LANGUAGE plpgsql AS $$
DECLARE
  start_date DATE;
  end_date DATE;
  partition_name TEXT;
BEGIN
  FOR i IN 0..months_ahead LOOP
    start_date := DATE_TRUNC('month', NOW()) + (i || ' months')::INTERVAL;
    end_date   := start_date + INTERVAL '1 month';
    partition_name := 'events_' || TO_CHAR(start_date, 'YYYY_MM');

    -- Only create if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = partition_name) THEN
      EXECUTE FORMAT(
        'CREATE TABLE %I PARTITION OF events
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
      );
      -- Create partition-specific indexes
      EXECUTE FORMAT(
        'CREATE INDEX ON %I (user_id)', partition_name
      );
      RAISE NOTICE 'Created partition: %', partition_name;
    END IF;
  END LOOP;
END;
$$;

-- Schedule via pg_cron extension:
CREATE EXTENSION pg_cron;
SELECT cron.schedule('0 0 1 * *', $$CALL create_monthly_partitions(3)$$);
-- Runs on 1st of every month at midnight

-- APPROACH 3: Application-level partition management
-- Application checks before insert whether target partition exists.
-- If not: creates it (requires DDL privileges from app). Not recommended.

-- PARTITION ATTACH (add an existing table as a partition):
-- Useful when pre-populating data in a staging table, then attaching
CREATE TABLE events_2025_01 (LIKE events INCLUDING ALL);
-- Load data...
ALTER TABLE events ATTACH PARTITION events_2025_01
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- PARTITION DETACH (remove from partition set, keep as standalone table):
ALTER TABLE events DETACH PARTITION events_2023_01;
-- Table events_2023_01 still exists with its data, just no longer part of events.
-- Archive it, dump it, then drop it:
COPY events_2023_01 TO '/archive/events_2023_01.csv';
DROP TABLE events_2023_01;
```

---

*End of SQL & PostgreSQL Interview Questions (170 questions — complete edition)*
