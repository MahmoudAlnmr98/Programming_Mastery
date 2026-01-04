# Database Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is ACID? Explain each property.

**Answer:**
ACID properties ensure reliable database transactions.

- **Atomicity**: All or nothing - transaction either completes fully or not at all
- **Consistency**: Database remains in valid state - constraints always satisfied
- **Isolation**: Concurrent transactions don't interfere - appear to run serially
- **Durability**: Committed changes persist - survive system failures

### 2. Explain normalization and its forms.

**Answer:**
Normalization reduces redundancy and improves data integrity.

**1NF (First Normal Form):**
- Atomic values, no repeating groups
- Each column contains single value

**2NF (Second Normal Form):**
- 1NF + no partial dependencies
- All non-key attributes fully dependent on primary key

**3NF (Third Normal Form):**
- 2NF + no transitive dependencies
- Non-key attributes not dependent on other non-key attributes

**Example:**
```sql
-- Not normalized
CREATE TABLE Orders (
    OrderID INT,
    CustomerName VARCHAR(100),
    Product1 VARCHAR(100),
    Product2 VARCHAR(100),
    Product1Price DECIMAL
);

-- Normalized
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE
);

CREATE TABLE OrderItems (
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Price DECIMAL
);
```

### 3. Explain primary key, foreign key, and unique key.

**Answer:**
- **Primary Key**: Uniquely identifies each row, cannot be NULL, only one per table
- **Foreign Key**: References primary key in another table, maintains referential integrity
- **Unique Key**: Ensures uniqueness, can be NULL, multiple per table

```sql
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Email VARCHAR(100) UNIQUE,
    Name VARCHAR(100)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
```

### 4. Explain SQL JOIN types.

**Answer:**
**INNER JOIN**: Returns matching rows from both tables
```sql
SELECT * FROM A
INNER JOIN B ON A.id = B.id;
```

**LEFT JOIN**: Returns all rows from left table, matching from right
```sql
SELECT * FROM A
LEFT JOIN B ON A.id = B.id;
```

**RIGHT JOIN**: Returns all rows from right table, matching from left
```sql
SELECT * FROM A
RIGHT JOIN B ON A.id = B.id;
```

**FULL OUTER JOIN**: Returns all rows from both tables
```sql
SELECT * FROM A
FULL OUTER JOIN B ON A.id = B.id;
```

### 5. Explain indexes and their types.

**Answer:**
Indexes speed up queries by creating data structure for fast lookups.

**Types:**
- **Primary Index**: Automatically created for primary key
- **Secondary Index**: Created on non-primary columns
- **Composite Index**: Multiple columns
- **Unique Index**: Ensures uniqueness

```sql
-- Create index
CREATE INDEX idx_email ON users(email);

-- Composite index
CREATE INDEX idx_name_email ON users(name, email);

-- Unique index
CREATE UNIQUE INDEX idx_username ON users(username);
```

**When to use:**
- Frequently queried columns
- Foreign keys
- Columns in WHERE, JOIN, ORDER BY

**When not to use:**
- Small tables
- Frequently updated columns
- Columns with few unique values

### 6. Explain the difference between DELETE, TRUNCATE, and DROP.

**Answer:**
- **DELETE**: Removes rows, can use WHERE, can rollback, slower, maintains structure
- **TRUNCATE**: Removes all rows, cannot use WHERE, cannot rollback, faster, resets auto-increment
- **DROP**: Removes entire table, cannot rollback, fastest

```sql
-- DELETE
DELETE FROM users WHERE id = 1;
DELETE FROM users;  -- Removes all rows

-- TRUNCATE
TRUNCATE TABLE users;  -- Removes all rows, faster

-- DROP
DROP TABLE users;  -- Removes entire table
```

### 7. Explain transactions and COMMIT/ROLLBACK.

**Answer:**
Transaction groups operations that must all succeed or all fail.

```sql
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If both succeed
COMMIT;

-- If any fails
ROLLBACK;
```

### 8. Explain SQL vs NoSQL databases.

**Answer:**
**SQL (Relational):**
- Structured data, fixed schema
- ACID transactions
- Vertical scaling
- Examples: MySQL, PostgreSQL, Oracle

**NoSQL:**
- Unstructured/flexible schema
- Eventual consistency
- Horizontal scaling
- Types: Document, Key-Value, Column, Graph
- Examples: MongoDB, Redis, Cassandra, Neo4j

---

## Intermediate Level

### 9. Explain database indexing strategies.

**Answer:**
**B-Tree Index:**
- Balanced tree structure
- O(log n) search time
- Good for range queries
- Default in most databases

**Hash Index:**
- O(1) average lookup
- Only equality queries
- No range queries

**Bitmap Index:**
- Good for low-cardinality columns
- Space efficient
- Fast for AND/OR operations

**Covering Index:**
- Contains all columns needed for query
- Avoids table lookup

```sql
-- Covering index
CREATE INDEX idx_covering ON orders(customer_id, order_date, total);
-- Query can use index without accessing table
SELECT customer_id, order_date, total FROM orders WHERE customer_id = 1;
```

### 10. Explain query optimization techniques.

**Answer:**
**1. Use Indexes:**
```sql
-- Bad: Full table scan
SELECT * FROM users WHERE name LIKE '%john%';

-- Good: Use index
SELECT * FROM users WHERE name LIKE 'john%';
```

**2. Avoid SELECT *:**
```sql
-- Bad
SELECT * FROM users;

-- Good
SELECT id, name, email FROM users;
```

**3. Use JOINs instead of subqueries:**
```sql
-- Bad: N+1 queries
SELECT * FROM users;
-- Then for each: SELECT * FROM orders WHERE user_id = ?

-- Good: Single query
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

**4. Limit results:**
```sql
SELECT * FROM users LIMIT 10;
```

**5. Use EXPLAIN:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

### 11. Explain database replication.

**Answer:**
Replication copies data across multiple databases.

**Master-Slave (Primary-Secondary):**
- One master handles writes
- Slaves handle reads
- Asynchronous replication

**Master-Master:**
- Multiple masters handle writes
- Requires conflict resolution
- Better write scalability

**Benefits:**
- High availability
- Read scalability
- Geographic distribution
- Backup

### 12. Explain database sharding.

**Answer:**
Sharding partitions data across multiple databases.

**Strategies:**
- **Range-based**: Partition by value ranges
- **Hash-based**: Partition by hash function
- **Directory-based**: Lookup table for routing

**Challenges:**
- Cross-shard queries
- Rebalancing
- Transaction support
- Hot spots

### 13. Explain CAP theorem in databases.

**Answer:**
CAP theorem: Can have at most 2 of 3:
- **Consistency**: All nodes see same data
- **Availability**: System remains operational
- **Partition Tolerance**: Works despite network failures

**SQL Databases**: CP (Consistency + Partition Tolerance)
- Strong consistency
- May sacrifice availability during partitions

**NoSQL Databases**: AP (Availability + Partition Tolerance)
- High availability
- Eventual consistency

### 14. Explain database connection pooling.

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
Connection conn = dataSource.getConnection();
```

### 15. Explain database transactions isolation levels.

**Answer:**
**READ UNCOMMITTED:**
- Lowest isolation
- Can read uncommitted data
- Dirty reads possible

**READ COMMITTED:**
- Can only read committed data
- No dirty reads
- Non-repeatable reads possible

**REPEATABLE READ:**
- Same read returns same result
- No non-repeatable reads
- Phantom reads possible

**SERIALIZABLE:**
- Highest isolation
- Transactions appear serial
- No phantom reads
- Lowest concurrency

---

## Advanced Level

### 16. Explain database deadlocks and how to prevent them.

**Answer:**
Deadlock occurs when transactions wait for each other.

**Example:**
```
Transaction 1: Locks A, waits for B
Transaction 2: Locks B, waits for A
```

**Prevention:**
- Lock ordering (always lock in same order)
- Timeout on locks
- Deadlock detection and rollback

### 17. Explain database partitioning.

**Answer:**
Partitioning splits large table into smaller pieces.

**Types:**
- **Horizontal**: Split rows (sharding)
- **Vertical**: Split columns

**Benefits:**
- Better performance
- Easier management
- Improved availability

### 18. Explain eventual consistency.

**Answer:**
System eventually converges to consistent state.

**Use Cases:**
- Social media feeds
- DNS
- CDN content

**Trade-offs:**
- High availability
- Better performance
- May read stale data

### 19. Explain database backup and recovery strategies.

**Answer:**
**Backup Types:**
- **Full Backup**: Complete database copy
- **Incremental**: Changes since last backup
- **Differential**: Changes since last full backup

**Recovery:**
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss

### 20. Explain NoSQL database types.

**Answer:**
**Document Databases (MongoDB):**
- Store documents (JSON-like)
- Flexible schema
- Good for content management

**Key-Value (Redis):**
- Simple key-value pairs
- Very fast
- Good for caching

**Column-Family (Cassandra):**
- Wide tables
- Good for time-series data
- Excellent write performance

**Graph (Neo4j):**
- Nodes and edges
- Good for relationships
- Social networks, recommendations

### 21. Explain database indexing internals (B-Tree, B+ Tree).

**Answer:**
**B-Tree:**
- Balanced tree structure
- All nodes store data
- Good for range queries
- Used in older databases

**B+ Tree:**
- Only leaf nodes store data
- Internal nodes store keys only
- All data in leaves (linked list)
- Better for range scans

**Comparison:**
- B+ Tree: Better for sequential access
- B+ Tree: More efficient for large datasets
- B+ Tree: Lower tree height

### 22. Explain database connection pooling in detail.

**Answer:**
Connection pool manages database connections.

**Benefits:**
- Reuse connections
- Limit connections
- Better performance
- Resource management

**Configuration:**
```java
HikariConfig config = new HikariConfig();
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);
```

**Pool States:**
- Active: In use
- Idle: Available
- Pending: Waiting for connection

### 23. Explain database query optimization techniques.

**Answer:**
**Techniques:**
1. **Use Indexes**: On frequently queried columns
2. **Avoid SELECT ***: Select only needed columns
3. **Use JOINs**: Instead of subqueries
4. **Limit Results**: Use LIMIT/TOP
5. **Analyze Queries**: Use EXPLAIN

**Query Hints:**
```sql
-- Force index usage
SELECT * FROM users USE INDEX (idx_email) WHERE email = 'test@example.com';

-- Analyze query plan
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

### 24. Explain database locking mechanisms.

**Answer:**
**Lock Types:**
- **Shared Lock**: Read lock, multiple readers
- **Exclusive Lock**: Write lock, single writer
- **Intent Lock**: Table-level lock

**Lock Granularity:**
- **Row-level**: Lock individual rows
- **Page-level**: Lock pages
- **Table-level**: Lock entire table

**Deadlock Prevention:**
- Lock ordering
- Timeout
- Deadlock detection

### 25. Explain database backup and recovery in detail.

**Answer:**
**Backup Types:**
- **Full Backup**: Complete database
- **Incremental**: Changes since last backup
- **Differential**: Changes since last full backup
- **Transaction Log**: All transactions

**Recovery Models:**
- **Simple**: No log backups
- **Full**: Complete recovery
- **Bulk-Logged**: Minimal logging

**RTO/RPO:**
- **RTO**: Recovery Time Objective
- **RPO**: Recovery Point Objective

**Point-in-Time Recovery:**
```sql
-- Restore full backup
RESTORE DATABASE MyDB FROM DISK = 'backup.bak';

-- Restore transaction log
RESTORE LOG MyDB FROM DISK = 'log.trn' WITH STOPAT = '2024-01-01 12:00:00';
```

### 26. Explain database partitioning strategies.

**Answer:**
**Partitioning Types:**
- **Range**: Partition by value ranges
- **Hash**: Partition by hash function
- **List**: Partition by list of values
- **Composite**: Multiple strategies

**Example (Range Partitioning):**
```sql
CREATE TABLE orders (
    id INT,
    order_date DATE,
    amount DECIMAL
) PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025)
);
```

**Benefits:**
- Better performance
- Easier management
- Improved availability

### 27. Explain database replication lag and consistency.

**Answer:**
**Replication Lag:**
- Delay between write and replication
- Causes: Network, load, distance

**Consistency Levels:**
- **Strong**: Read from primary
- **Eventual**: Read from replica (may be stale)
- **Read-Your-Writes**: Read own writes from primary

**Handling Lag:**
- Monitor replication delay
- Route critical reads to primary
- Use read replicas for analytics

### 28. Explain database connection string and security.

**Answer:**
**Connection String:**
```
jdbc:mysql://host:port/database?user=user&password=pass
```

**Security Best Practices:**
- Use encrypted connections (SSL/TLS)
- Store credentials securely
- Use connection pooling
- Limit privileges
- Regular security updates

**Encryption:**
- **At Rest**: Encrypt database files
- **In Transit**: SSL/TLS for connections
- **Application**: Encrypt sensitive data

### 29. Explain database connection string best practices.

**Answer:**
Connection strings contain database connection information.

**Format:**
```
postgresql://username:password@host:port/database?params
mysql://user:pass@localhost:3306/dbname
mongodb://user:pass@host:27017/dbname
```

**Best Practices:**
- Store in environment variables
- Use connection pooling
- Encrypt sensitive data
- Use read replicas for reads
- Set timeouts
- Use SSL/TLS

**Example:**
```javascript
// Environment variable
const connectionString = process.env.DATABASE_URL;

// With connection pooling
const pool = new Pool({
    connectionString,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
    ssl: {
        rejectUnauthorized: false
    }
});
```

### 30. Explain database query execution plans.

**Answer:**
Execution plan shows how database executes query.

**Analyzing Plans:**
```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- MySQL
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- SQL Server
SET SHOWPLAN_ALL ON;
SELECT * FROM users WHERE email = 'user@example.com';
```

**Plan Components:**
- **Seq Scan**: Full table scan (slow)
- **Index Scan**: Uses index (fast)
- **Index Only Scan**: Uses index only (fastest)
- **Nested Loop**: Join algorithm
- **Hash Join**: Hash-based join
- **Sort**: Sorting operation

**Optimization:**
- Look for sequential scans on large tables
- Ensure indexes are used
- Check join algorithms
- Monitor sort operations

### 31. Explain database materialized views.

**Answer:**
Materialized views store query results physically.

**Creating:**
```sql
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    user_id,
    COUNT(*) as order_count,
    SUM(total) as total_spent
FROM orders
GROUP BY user_id;

-- Refresh
REFRESH MATERIALIZED VIEW user_stats;
```

**Use Cases:**
- Expensive aggregations
- Complex joins
- Reporting queries
- Data warehousing

**Trade-offs:**
- Faster reads
- Stale data (needs refresh)
- Storage overhead
- Maintenance required

### 32. Explain database stored procedures and functions.

**Answer:**
**Stored Procedures:**
```sql
CREATE PROCEDURE GetUserOrders(IN user_id INT)
BEGIN
    SELECT * FROM orders WHERE user_id = user_id;
END;

-- Call
CALL GetUserOrders(123);
```

**Functions:**
```sql
CREATE FUNCTION CalculateTotal(price DECIMAL, quantity INT)
RETURNS DECIMAL
BEGIN
    RETURN price * quantity;
END;

-- Use
SELECT CalculateTotal(10.00, 5) AS total;
```

**Benefits:**
- Performance (precompiled)
- Security (controlled access)
- Reusability
- Business logic in database

**Drawbacks:**
- Database-specific
- Harder to test
- Version control challenges
- Less flexible

### 33. Explain database triggers.

**Answer:**
Triggers execute automatically on events.

**Creating Trigger:**
```sql
CREATE TRIGGER update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END;
```

**Trigger Types:**
- **BEFORE**: Executes before operation
- **AFTER**: Executes after operation
- **INSTEAD OF**: Replaces operation (views)

**Use Cases:**
- Audit logging
- Data validation
- Automatic calculations
- Maintaining denormalized data

**Example:**
```sql
CREATE TRIGGER log_user_changes
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_audit_log (user_id, old_value, new_value, changed_at)
    VALUES (NEW.id, OLD.email, NEW.email, NOW());
END;
```

### 34. Explain SQL Window Functions.

**Answer:**
Window functions perform calculations across set of rows.

**ROW_NUMBER():**
```sql
SELECT 
    name, 
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

**RANK() and DENSE_RANK():**
```sql
SELECT 
    name, 
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;
-- RANK: 1, 2, 2, 4 (skips 3)
-- DENSE_RANK: 1, 2, 2, 3 (no gaps)
```

**PARTITION BY:**
```sql
SELECT 
    department,
    name,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;
```

**LAG() and LEAD():**
```sql
SELECT 
    date,
    sales,
    LAG(sales, 1) OVER (ORDER BY date) as prev_sales,
    LEAD(sales, 1) OVER (ORDER BY date) as next_sales
FROM sales;
```

**SUM() OVER:**
```sql
SELECT 
    date,
    sales,
    SUM(sales) OVER (ORDER BY date) as running_total
FROM sales;
```

### 35. Explain SQL Common Table Expressions (CTEs).

**Answer:**
CTEs provide temporary result set for query.

**Simple CTE:**
```sql
WITH high_salary AS (
    SELECT * FROM employees WHERE salary > 50000
)
SELECT * FROM high_salary WHERE department = 'IT';
```

**Recursive CTE:**
```sql
WITH RECURSIVE hierarchy AS (
    -- Base case
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy;
```

**Multiple CTEs:**
```sql
WITH 
    high_salary AS (
        SELECT * FROM employees WHERE salary > 50000
    ),
    it_employees AS (
        SELECT * FROM high_salary WHERE department = 'IT'
    )
SELECT * FROM it_employees;
```

### 36. Explain SQL Subqueries vs JOINs.

**Answer:**
**Subquery:**
```sql
-- Scalar subquery
SELECT name, 
       (SELECT AVG(salary) FROM employees) as avg_salary
FROM employees;

-- Correlated subquery
SELECT name, salary
FROM employees e1
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees e2 
    WHERE e2.department = e1.department
);

-- EXISTS subquery
SELECT name
FROM employees e
WHERE EXISTS (
    SELECT 1 FROM projects p 
    WHERE p.employee_id = e.id
);
```

**JOIN:**
```sql
SELECT e.name, p.project_name
FROM employees e
INNER JOIN projects p ON e.id = p.employee_id;
```

**When to use:**
- **Subquery**: When you need single value or existence check
- **JOIN**: When you need data from multiple tables

### 37. Explain SQL Indexes and their types.

**Answer:**
**B-Tree Index (Default):**
```sql
CREATE INDEX idx_name ON employees(name);
-- Good for: Equality and range queries
```

**Composite Index:**
```sql
CREATE INDEX idx_dept_salary ON employees(department, salary);
-- Order matters: (department, salary) vs (salary, department)
```

**Unique Index:**
```sql
CREATE UNIQUE INDEX idx_email ON employees(email);
```

**Partial Index:**
```sql
CREATE INDEX idx_active ON employees(name) WHERE active = true;
```

**Covering Index:**
```sql
CREATE INDEX idx_covering ON employees(department, salary, name);
-- Includes all columns needed for query
```

**Hash Index:**
```sql
-- PostgreSQL
CREATE INDEX idx_hash ON employees USING HASH(email);
-- Good for: Equality only
```

### 38. Explain SQL Query Optimization Techniques.

**Answer:**
**1. Use Indexes:**
```sql
-- Add index on frequently queried columns
CREATE INDEX idx_department ON employees(department);
```

**2. Avoid SELECT *:**
```sql
-- Bad
SELECT * FROM employees;

-- Good
SELECT id, name, email FROM employees;
```

**3. Use LIMIT:**
```sql
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;
```

**4. Avoid Functions on Indexed Columns:**
```sql
-- Bad (can't use index)
SELECT * FROM employees WHERE UPPER(name) = 'JOHN';

-- Good
SELECT * FROM employees WHERE name = 'John';
```

**5. Use EXISTS instead of COUNT:**
```sql
-- Bad
SELECT * FROM employees 
WHERE (SELECT COUNT(*) FROM projects WHERE employee_id = employees.id) > 0;

-- Good
SELECT * FROM employees e
WHERE EXISTS (SELECT 1 FROM projects p WHERE p.employee_id = e.id);
```

**6. Avoid N+1 Queries:**
```sql
-- Bad: Multiple queries
SELECT * FROM employees;
-- Then for each employee:
SELECT * FROM projects WHERE employee_id = ?

-- Good: Single query with JOIN
SELECT e.*, p.*
FROM employees e
LEFT JOIN projects p ON e.id = p.employee_id;
```

### 39. Explain SQL Transactions and Isolation Levels.

**Answer:**
**Transaction Properties (ACID):**
- **Atomicity**: All or nothing
- **Consistency**: Valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

**Isolation Levels:**
```sql
-- Read Uncommitted (lowest isolation)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- Issues: Dirty reads

-- Read Committed (default in most DBs)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Issues: Non-repeatable reads

-- Repeatable Read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Issues: Phantom reads

-- Serializable (highest isolation)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- No issues but slowest
```

**Transaction Example:**
```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- Or
ROLLBACK;
```

### 40. Explain SQL Stored Procedures and Functions.

**Answer:**
**Stored Procedure:**
```sql
CREATE PROCEDURE GetEmployeeByDepartment(IN dept_name VARCHAR(50))
BEGIN
    SELECT * FROM employees WHERE department = dept_name;
END;

-- Call
CALL GetEmployeeByDepartment('IT');
```

**Function:**
```sql
CREATE FUNCTION GetEmployeeCount(dept_name VARCHAR(50))
RETURNS INT
BEGIN
    DECLARE count INT;
    SELECT COUNT(*) INTO count FROM employees WHERE department = dept_name;
    RETURN count;
END;

-- Use
SELECT GetEmployeeCount('IT');
```

**Differences:**
- **Procedure**: Can return multiple values, can have side effects
- **Function**: Returns single value, should be pure (no side effects)

### 41. Explain SQL Triggers.

**Answer:**
Triggers execute automatically on specified events.

**BEFORE INSERT Trigger:**
```sql
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary < 0 THEN
        SET NEW.salary = 0;
    END IF;
END;
```

**AFTER UPDATE Trigger:**
```sql
CREATE TRIGGER after_employee_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_audit (employee_id, old_salary, new_salary, changed_at)
    VALUES (NEW.id, OLD.salary, NEW.salary, NOW());
END;
```

**INSTEAD OF Trigger (Views):**
```sql
CREATE TRIGGER instead_of_delete
INSTEAD OF DELETE ON employee_view
FOR EACH ROW
BEGIN
    DELETE FROM employees WHERE id = OLD.id;
END;
```

### 42. Explain SQL Views and Materialized Views.

**Answer:**
**View (Virtual):**
```sql
CREATE VIEW high_salary_employees AS
SELECT name, salary, department
FROM employees
WHERE salary > 50000;

-- Use
SELECT * FROM high_salary_employees;
```

**Materialized View (Physical):**
```sql
-- PostgreSQL
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    product_id,
    SUM(quantity) as total_quantity,
    SUM(amount) as total_amount
FROM sales
GROUP BY product_id;

-- Refresh
REFRESH MATERIALIZED VIEW sales_summary;
```

**Differences:**
- **View**: Virtual, always up-to-date, slower for complex queries
- **Materialized View**: Physical storage, faster, needs refresh

### 43. Explain SQL Pivot and Unpivot.

**Answer:**
**Pivot (Rows to Columns):**
```sql
-- PostgreSQL
SELECT *
FROM (
    SELECT department, name, salary
    FROM employees
) AS source
PIVOT (
    SUM(salary)
    FOR department IN ('IT', 'HR', 'Finance')
) AS pivot_table;
```

**Unpivot (Columns to Rows):**
```sql
SELECT name, 'Q1' as quarter, q1_sales as sales
FROM sales
UNION ALL
SELECT name, 'Q2', q2_sales
FROM sales
UNION ALL
SELECT name, 'Q3', q3_sales
FROM sales
UNION ALL
SELECT name, 'Q4', q4_sales
FROM sales;
```

### 44. Explain SQL Aggregate Functions.

**Answer:**
**Basic Aggregates:**
```sql
SELECT 
    COUNT(*) as total,
    SUM(salary) as total_salary,
    AVG(salary) as avg_salary,
    MIN(salary) as min_salary,
    MAX(salary) as max_salary
FROM employees;
```

**GROUP BY:**
```sql
SELECT 
    department,
    COUNT(*) as count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department;
```

**HAVING:**
```sql
SELECT 
    department,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;
```

**DISTINCT with Aggregates:**
```sql
SELECT COUNT(DISTINCT department) FROM employees;
```

### 45. Explain SQL Date and Time Functions.

**Answer:**
**Date Functions:**
```sql
-- Current date/time
SELECT NOW(), CURRENT_DATE, CURRENT_TIME;

-- Extract parts
SELECT 
    EXTRACT(YEAR FROM hire_date) as year,
    EXTRACT(MONTH FROM hire_date) as month,
    EXTRACT(DAY FROM hire_date) as day
FROM employees;

-- Date arithmetic
SELECT hire_date + INTERVAL '1 year' as anniversary
FROM employees;

-- Date difference
SELECT DATEDIFF('2024-01-01', '2023-01-01') as days_diff;

-- Format date
SELECT DATE_FORMAT(hire_date, '%Y-%m-%d') as formatted_date
FROM employees;
```

### 46. Explain SQL String Functions.

**Answer:**
**Common String Functions:**
```sql
-- Concatenation
SELECT CONCAT(first_name, ' ', last_name) as full_name FROM employees;

-- Substring
SELECT SUBSTRING(name, 1, 5) FROM employees;

-- Length
SELECT LENGTH(name) FROM employees;

-- Upper/Lower
SELECT UPPER(name), LOWER(name) FROM employees;

-- Trim
SELECT TRIM('  hello  ') as trimmed;

-- Replace
SELECT REPLACE(name, 'John', 'Jon') FROM employees;

-- Pattern matching
SELECT * FROM employees WHERE name LIKE 'J%';
SELECT * FROM employees WHERE name REGEXP '^J';
```

### 47. Explain SQL NULL Handling.

**Answer:**
**IS NULL / IS NOT NULL:**
```sql
SELECT * FROM employees WHERE manager_id IS NULL;
SELECT * FROM employees WHERE manager_id IS NOT NULL;
```

**COALESCE:**
```sql
SELECT COALESCE(manager_id, 0) as manager_id FROM employees;
-- Returns first non-NULL value
```

**NULLIF:**
```sql
SELECT NULLIF(salary, 0) as salary FROM employees;
-- Returns NULL if values are equal
```

**Aggregates with NULL:**
```sql
-- COUNT(*) counts all rows
-- COUNT(column) ignores NULLs
SELECT COUNT(*), COUNT(manager_id) FROM employees;
```

### 48. Explain SQL CASE Statements.

**Answer:**
**Simple CASE:**
```sql
SELECT 
    name,
    CASE department
        WHEN 'IT' THEN 'Technology'
        WHEN 'HR' THEN 'Human Resources'
        ELSE 'Other'
    END as dept_name
FROM employees;
```

**Searched CASE:**
```sql
SELECT 
    name,
    salary,
    CASE
        WHEN salary > 100000 THEN 'High'
        WHEN salary > 50000 THEN 'Medium'
        ELSE 'Low'
    END as salary_level
FROM employees;
```

**CASE in Aggregates:**
```sql
SELECT 
    COUNT(CASE WHEN salary > 100000 THEN 1 END) as high_salary_count,
    COUNT(CASE WHEN salary <= 100000 THEN 1 END) as other_count
FROM employees;
```

### 49. Explain SQL UNION, INTERSECT, and EXCEPT.

**Answer:**
**UNION (All distinct rows):**
```sql
SELECT name FROM employees
UNION
SELECT name FROM contractors;
-- Removes duplicates
```

**UNION ALL (All rows):**
```sql
SELECT name FROM employees
UNION ALL
SELECT name FROM contractors;
-- Keeps duplicates
```

**INTERSECT (Common rows):**
```sql
SELECT name FROM employees
INTERSECT
SELECT name FROM contractors;
```

**EXCEPT (Rows in first but not second):**
```sql
SELECT name FROM employees
EXCEPT
SELECT name FROM contractors;
```

### 50. Explain NoSQL Database Types.

**Answer:**
**Document Databases (MongoDB, CouchDB):**
```javascript
// MongoDB example
{
    "_id": "123",
    "name": "John",
    "email": "john@example.com",
    "address": {
        "street": "123 Main St",
        "city": "New York"
    }
}
```

**Key-Value Stores (Redis, DynamoDB):**
```javascript
// Redis example
SET user:123:name "John"
GET user:123:name
```

**Column-Family (Cassandra, HBase):**
- Stores data in columns instead of rows
- Good for time-series data

**Graph Databases (Neo4j):**
```cypher
// Neo4j example
CREATE (john:Person {name: "John"})
CREATE (jane:Person {name: "Jane"})
CREATE (john)-[:FRIENDS]->(jane)
```

### 51. Find Second Highest Salary (Common Interview Problem).

**Answer:**
```sql
-- Method 1: Subquery
SELECT MAX(salary) as second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 2: LIMIT/OFFSET
SELECT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Method 3: DENSE_RANK
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk
    FROM employees
) ranked
WHERE rnk = 2;
```

### 52. Find Nth Highest Salary.

**Answer:**
```sql
-- Method 1: LIMIT/OFFSET
SELECT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET (N - 1);

-- Method 2: DENSE_RANK
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk
    FROM employees
) ranked
WHERE rnk = N;
```

### 53. Find Employees with Same Salary.

**Answer:**
```sql
-- Using GROUP BY
SELECT salary, COUNT(*) as count
FROM employees
GROUP BY salary
HAVING COUNT(*) > 1;

-- Using Self Join
SELECT DISTINCT e1.name, e1.salary
FROM employees e1
JOIN employees e2 ON e1.salary = e2.salary AND e1.id != e2.id;
```

### 54. Find Duplicate Emails.

**Answer:**
```sql
-- Method 1: GROUP BY
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Method 2: Window Function
SELECT email
FROM (
    SELECT email, COUNT(*) OVER (PARTITION BY email) as cnt
    FROM users
) ranked
WHERE cnt > 1;
```

### 55. Delete Duplicate Rows (Keep One).

**Answer:**
```sql
-- PostgreSQL
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id)
    FROM users
    GROUP BY email
);

-- MySQL
DELETE u1 FROM users u1
INNER JOIN users u2
WHERE u1.id > u2.id AND u1.email = u2.email;
```

### 56. Find Employees Earning More Than Their Managers.

**Answer:**
```sql
SELECT e.name as employee, e.salary, m.name as manager, m.salary as manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### 57. Find Department with Highest Average Salary.

**Answer:**
```sql
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
LIMIT 1;

-- Or using window function
SELECT department, avg_salary
FROM (
    SELECT department, AVG(salary) as avg_salary,
           RANK() OVER (ORDER BY AVG(salary) DESC) as rnk
    FROM employees
    GROUP BY department
) ranked
WHERE rnk = 1;
```

### 58. Find Employees Who Never Have Projects.

**Answer:**
```sql
-- Method 1: LEFT JOIN
SELECT e.name
FROM employees e
LEFT JOIN projects p ON e.id = p.employee_id
WHERE p.id IS NULL;

-- Method 2: NOT EXISTS
SELECT name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM projects p WHERE p.employee_id = e.id
);

-- Method 3: NOT IN
SELECT name
FROM employees
WHERE id NOT IN (SELECT employee_id FROM projects WHERE employee_id IS NOT NULL);
```

### 59. Find Consecutive Numbers.

**Answer:**
```sql
-- Find numbers that appear at least 3 times consecutively
SELECT DISTINCT num as ConsecutiveNums
FROM (
    SELECT num,
           LAG(num, 1) OVER (ORDER BY id) as prev,
           LEAD(num, 1) OVER (ORDER BY id) as next
    FROM logs
) ranked
WHERE num = prev AND num = next;
```

### 60. Rank Employees by Salary in Each Department.

**Answer:**
```sql
SELECT 
    department,
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_dense_rank
FROM employees;
```

### 61. Find Customers Who Bought All Products.

**Answer:**
```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (
    SELECT COUNT(DISTINCT product_id) FROM products
);
```

### 62. Find Top 3 Salaries in Each Department.

**Answer:**
```sql
SELECT department, name, salary
FROM (
    SELECT 
        department,
        name,
        salary,
        DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rnk
    FROM employees
) ranked
WHERE rnk <= 3;
```

### 63. Swap Salary Values (Male/Female).

**Answer:**
```sql
-- Swap male and female salary values
UPDATE employees
SET salary = CASE
    WHEN sex = 'm' THEN (
        SELECT salary FROM employees e2 
        WHERE e2.sex = 'f' AND e2.id = employees.id
    )
    WHEN sex = 'f' THEN (
        SELECT salary FROM employees e2 
        WHERE e2.sex = 'm' AND e2.id = employees.id
    )
END;

-- Or using temporary table
UPDATE employees e1
JOIN employees e2 ON e1.id = e2.id
SET e1.salary = e2.salary, e2.salary = e1.salary
WHERE e1.sex != e2.sex;
```

### 64. Find Employees with Top N Salaries in Each Department.

**Answer:**
```sql
SELECT department, name, salary
FROM (
    SELECT 
        department,
        name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
) ranked
WHERE rn <= N;
```

### 65. Calculate Running Total.

**Answer:**
```sql
SELECT 
    date,
    sales,
    SUM(sales) OVER (ORDER BY date) as running_total
FROM sales;

-- By category
SELECT 
    category,
    date,
    sales,
    SUM(sales) OVER (PARTITION BY category ORDER BY date) as running_total
FROM sales;
```

### 66. Find Employees with Salary Between Range.

**Answer:**
```sql
SELECT name, salary
FROM employees
WHERE salary BETWEEN 50000 AND 100000;

-- Or
SELECT name, salary
FROM employees
WHERE salary >= 50000 AND salary <= 100000;
```

### 67. Find Employees Hired in Last N Months.

**Answer:**
```sql
SELECT name, hire_date
FROM employees
WHERE hire_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH);

-- PostgreSQL
SELECT name, hire_date
FROM employees
WHERE hire_date >= CURRENT_DATE - INTERVAL '6 months';
```

### 68. Find Employees with No Manager (Top Level).

**Answer:**
```sql
SELECT name
FROM employees
WHERE manager_id IS NULL;
```

### 69. Find Employees and Their Department Count.

**Answer:**
```sql
SELECT 
    e.name,
    COUNT(DISTINCT d.id) as dept_count
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
GROUP BY e.id, e.name;
```

### 70. Find Products Never Ordered.

**Answer:**
```sql
SELECT p.name
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE oi.product_id IS NULL;
```

### 71. Find Customers with Most Orders.

**Answer:**
```sql
SELECT customer_id, COUNT(*) as order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC
LIMIT 1;
```

### 72. Find Employees with Same Name.

**Answer:**
```sql
SELECT name, COUNT(*) as count
FROM employees
GROUP BY name
HAVING COUNT(*) > 1;
```

### 73. Find Latest Record for Each Group.

**Answer:**
```sql
-- Method 1: Window Function
SELECT id, name, date
FROM (
    SELECT 
        id, name, date,
        ROW_NUMBER() OVER (PARTITION BY name ORDER BY date DESC) as rn
    FROM records
) ranked
WHERE rn = 1;

-- Method 2: Self Join
SELECT r1.*
FROM records r1
LEFT JOIN records r2 ON r1.name = r2.name AND r1.date < r2.date
WHERE r2.id IS NULL;
```

### 74. Find Employees with Maximum Salary in Each Department.

**Answer:**
```sql
SELECT e.department, e.name, e.salary
FROM employees e
JOIN (
    SELECT department, MAX(salary) as max_salary
    FROM employees
    GROUP BY department
) max_sal ON e.department = max_sal.department 
         AND e.salary = max_sal.max_salary;
```

### 75. Find Employees Who Joined in Same Month.

**Answer:**
```sql
SELECT 
    EXTRACT(YEAR FROM hire_date) as year,
    EXTRACT(MONTH FROM hire_date) as month,
    COUNT(*) as count
FROM employees
GROUP BY EXTRACT(YEAR FROM hire_date), EXTRACT(MONTH FROM hire_date)
HAVING COUNT(*) > 1;
```

### 76. Find All Duplicate Emails (LeetCode Easy).

**Answer:**
```sql
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

### 77. Find Customers Who Never Order (LeetCode Easy).

**Answer:**
```sql
SELECT c.name as Customers
FROM customers c
LEFT JOIN orders o ON c.id = o.customerId
WHERE o.id IS NULL;
```

### 78. Rising Temperature (LeetCode Easy).

**Problem:** Find dates with temperature higher than previous day.

**Answer:**
```sql
SELECT w1.id
FROM weather w1
JOIN weather w2 ON DATEDIFF(w1.recordDate, w2.recordDate) = 1
WHERE w1.temperature > w2.temperature;
```

### 79. Delete Duplicate Emails (LeetCode Easy).

**Answer:**
```sql
DELETE p1 FROM person p1
INNER JOIN person p2
WHERE p1.email = p2.email AND p1.id > p2.id;
```

### 80. Combine Two Tables (LeetCode Easy).

**Answer:**
```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM person p
LEFT JOIN address a ON p.personId = a.personId;
```

### 81. Second Highest Salary (LeetCode Easy).

**Answer:**
```sql
SELECT MAX(salary) as SecondHighestSalary
FROM employee
WHERE salary < (SELECT MAX(salary) FROM employee);
```

### 82. Employees Earning More Than Their Managers (LeetCode Easy).

**Answer:**
```sql
SELECT e.name as Employee
FROM employee e
JOIN employee m ON e.managerId = m.id
WHERE e.salary > m.salary;
```

### 83. Duplicate Emails (LeetCode Easy).

**Answer:**
```sql
SELECT email
FROM person
GROUP BY email
HAVING COUNT(*) > 1;
```

### 84. Customers Who Never Order (LeetCode Easy).

**Answer:**
```sql
SELECT name as Customers
FROM customers
WHERE id NOT IN (
    SELECT customerId FROM orders WHERE customerId IS NOT NULL
);
```

### 85. Big Countries (LeetCode Easy).

**Answer:**
```sql
SELECT name, population, area
FROM world
WHERE area >= 3000000 OR population >= 25000000;
```

### 86. Classes More Than 5 Students (LeetCode Easy).

**Answer:**
```sql
SELECT class
FROM courses
GROUP BY class
HAVING COUNT(DISTINCT student) >= 5;
```

### 87. Not Boring Movies (LeetCode Easy).

**Answer:**
```sql
SELECT *
FROM cinema
WHERE id % 2 = 1 AND description != 'boring'
ORDER BY rating DESC;
```

### 88. Swap Salary (LeetCode Easy).

**Answer:**
```sql
UPDATE salary
SET sex = CASE
    WHEN sex = 'm' THEN 'f'
    WHEN sex = 'f' THEN 'm'
END;
```

### 89. Friend Requests I (LeetCode Easy).

**Answer:**
```sql
SELECT 
    ROUND(
        COUNT(DISTINCT requester_id, accepter_id) / 
        COUNT(DISTINCT sender_id, send_to_id) * 100, 
        2
    ) as accept_rate
FROM friend_request, request_accepted;
```

### 90. Consecutive Numbers (LeetCode Medium).

**Answer:**
```sql
SELECT DISTINCT l1.num as ConsecutiveNums
FROM logs l1
JOIN logs l2 ON l1.id = l2.id - 1
JOIN logs l3 ON l1.id = l3.id - 2
WHERE l1.num = l2.num AND l2.num = l3.num;
```

---

This covers database interview questions from beginner to advanced level with detailed explanations.

