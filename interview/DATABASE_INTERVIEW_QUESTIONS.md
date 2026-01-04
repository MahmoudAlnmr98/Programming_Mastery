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

---

This covers database interview questions from beginner to advanced level with detailed explanations.

