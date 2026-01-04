# Complete System Design Mastery Guide

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [System Design Principles](#system-design-principles)
3. [Scalability](#scalability)
4. [Load Balancing](#load-balancing)
5. [Caching](#caching)
6. [Database Design](#database-design)
7. [Distributed Systems](#distributed-systems)
8. [Microservices](#microservices)
9. [Message Queues](#message-queues)
10. [API Design](#api-design)
11. [Security](#security)
12. [Monitoring & Observability](#monitoring--observability)
13. [Performance Optimization](#performance-optimization)
14. [Design Patterns](#design-patterns)
15. [Common System Designs](#common-system-designs)
16. [Best Practices](#best-practices)
17. [Interview Preparation](#interview-preparation)

---

## Fundamentals

### What is System Design?

System design is the process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements. It's a critical discipline in software engineering that bridges the gap between business requirements and technical implementation.

**Theoretical Foundation:**
System design is rooted in several computer science disciplines:
- **Software Architecture**: The high-level structure of software systems
- **Distributed Systems Theory**: How systems work across multiple machines
- **Computer Networks**: How components communicate
- **Database Theory**: How data is stored and accessed
- **Algorithm Design**: How operations are performed efficiently

**Why System Design Matters:**
1. **Complexity Management**: Large systems are inherently complex. Good design breaks complexity into manageable pieces.
2. **Scalability**: Systems must grow with user demand without complete redesign.
3. **Reliability**: Systems must work correctly even when components fail.
4. **Performance**: Systems must respond quickly to user requests.
5. **Cost Optimization**: Efficient design reduces infrastructure costs.

**Design Philosophy:**
- **Separation of Concerns**: Each component has a single, well-defined responsibility
- **Modularity**: Systems are built from independent, interchangeable modules
- **Abstraction**: Hide implementation details behind clean interfaces
- **Layering**: Organize systems into logical layers (presentation, business logic, data)

### Goals of System Design

#### Scalability
**Definition**: The ability of a system to handle growth in users, data, traffic, or complexity without significant redesign.

**Theoretical Aspects:**
- **Amdahl's Law**: Maximum speedup is limited by the sequential portion of the program
  - Speedup = 1 / (S + (1-S)/N) where S is sequential portion, N is number of processors
- **Gustafson's Law**: As problem size increases, parallel portion becomes more significant
- **Scalability Types**:
  - **Load Scalability**: Handle more concurrent users
  - **Geographic Scalability**: Work across different locations
  - **Administrative Scalability**: Manage more components

**Scaling Dimensions:**
- **Horizontal (Scale Out)**: Add more machines
  - Pros: No hardware limits, better fault tolerance, cost-effective
  - Cons: Network overhead, data consistency challenges
- **Vertical (Scale Up)**: Add more power to existing machines
  - Pros: Simpler architecture, no data distribution, lower latency
  - Cons: Hardware limits, single point of failure, expensive

#### Reliability
**Definition**: The probability that a system will perform its intended function under stated conditions for a specified period.

**Theoretical Foundation:**
- **Mean Time Between Failures (MTBF)**: Average time between system failures
- **Mean Time To Repair (MTTR)**: Average time to fix a failure
- **Availability = MTBF / (MTBF + MTTR)**

**Reliability Principles:**
- **Fault Tolerance**: System continues operating despite failures
  - **Fault Types**: Transient (temporary), Intermittent (occasional), Permanent
  - **Fault Models**: Crash failure, Omission failure, Byzantine failure
- **Redundancy**: Duplicate critical components
  - **Active Redundancy**: All components run simultaneously
  - **Passive Redundancy**: Backup components activate on failure
- **Error Detection**: Identify failures quickly
  - **Checksums**: Detect data corruption
  - **Heartbeats**: Detect component failures
  - **Timeouts**: Detect unresponsive components

#### Availability
**Definition**: The percentage of time a system is operational and accessible.

**Availability Levels:**
- **99% (Two 9s)**: 87.6 hours downtime/year
- **99.9% (Three 9s)**: 8.76 hours downtime/year
- **99.99% (Four 9s)**: 52.56 minutes downtime/year
- **99.999% (Five 9s)**: 5.26 minutes downtime/year

**Theoretical Model:**
Availability = Uptime / (Uptime + Downtime)

**Achieving High Availability:**
- **Redundancy**: Multiple components prevent single points of failure
- **Failover**: Automatic switching to backup systems
- **Load Distribution**: Spread load to prevent overload
- **Health Monitoring**: Detect and respond to issues quickly

#### Performance
**Definition**: How quickly and efficiently a system responds to requests.

**Performance Metrics:**
- **Latency**: Time to process a single request
  - **Network Latency**: Time for data to travel
  - **Processing Latency**: Time to process request
  - **Queue Latency**: Time waiting in queue
- **Throughput**: Number of requests processed per second
  - **Requests Per Second (RPS)**: Total requests handled
  - **Transactions Per Second (TPS)**: Successful transactions
- **Response Time**: Time from request to response
  - **P50 (Median)**: 50% of requests faster
  - **P95**: 95% of requests faster
  - **P99**: 99% of requests faster

**Performance Theory:**
- **Little's Law**: L = λ × W
  - L = Average number of requests in system
  - λ = Arrival rate (requests/second)
  - W = Average time in system
- **Queueing Theory**: Models system behavior under load
  - **M/M/1 Queue**: Single server, exponential arrivals/service
  - **M/M/c Queue**: Multiple servers

#### Maintainability
**Definition**: The ease with which a system can be modified, updated, or extended.

**Maintainability Factors:**
- **Code Quality**: Clean, readable, well-documented code
- **Modularity**: Independent, replaceable components
- **Testability**: Easy to test and verify correctness
- **Documentation**: Clear documentation of design and implementation

#### Cost-Effectiveness
**Definition**: Achieving desired performance and reliability at minimal cost.

**Cost Components:**
- **Infrastructure**: Servers, storage, networking
- **Development**: Engineering time and resources
- **Operations**: Maintenance and support
- **Opportunity Cost**: Trade-offs between features and resources

### System Design Process

The system design process is a structured approach to creating scalable, reliable systems. It follows a top-down methodology, starting with high-level requirements and progressively refining to implementation details.

#### 1. Requirements Gathering

**Theoretical Foundation:**
Requirements gathering is based on software engineering principles of understanding stakeholder needs and translating them into technical specifications.

**Functional Requirements:**
- **Definition**: What the system must do
- **Examples**: User authentication, data storage, report generation
- **Characteristics**: 
  - Specific and measurable
  - Testable
  - Traceable to business needs
- **Documentation Format**: Use cases, user stories, functional specifications

**Non-Functional Requirements:**
- **Definition**: How well the system performs
- **Categories**:
  - **Performance**: Response time, throughput
  - **Scalability**: Growth capacity
  - **Reliability**: Uptime, error rates
  - **Security**: Authentication, authorization, encryption
  - **Usability**: User experience, accessibility
  - **Maintainability**: Code quality, documentation
- **Measurement**: Quantifiable metrics (e.g., "99.9% uptime", "< 200ms response time")

**Constraints:**
- **Technical**: Technology stack, platform limitations
- **Business**: Budget, timeline, resources
- **Regulatory**: Compliance requirements (GDPR, HIPAA)
- **Operational**: Team expertise, infrastructure

**Assumptions:**
- **Explicit**: Clearly stated assumptions
- **Validated**: Verify assumptions are reasonable
- **Documented**: Record for future reference

#### 2. Capacity Estimation

**Theoretical Foundation:**
Capacity estimation uses mathematical modeling to predict resource requirements. It's based on queueing theory, probability, and statistical analysis.

**Traffic Estimates:**
- **Read/Write Ratio**: Percentage of read vs write operations
  - Example: 100:1 read/write ratio means 100 reads per write
- **Peak Traffic**: Maximum expected load
  - Calculate: Average traffic × Peak factor (typically 2-5x)
- **Growth Projection**: Expected growth over time
  - Linear growth: Simple multiplication
  - Exponential growth: Compound interest formula

**Calculation Example:**
```
Daily Active Users (DAU): 1 million
Average requests per user per day: 10
Total daily requests: 1M × 10 = 10M requests/day
Requests per second: 10M / (24 × 3600) ≈ 116 RPS
Peak traffic (3x average): 116 × 3 = 348 RPS
```

**Storage Estimates:**
- **Data Volume**: Amount of data to store
  - User data: Number of users × Average data per user
  - Media files: Number of files × Average file size
  - Logs: Requests per day × Log size per request × Retention period
- **Growth Rate**: How fast data grows
- **Replication Factor**: Number of copies (typically 3 for reliability)

**Calculation Example:**
```
Users: 1 million
Average data per user: 1 MB
Total storage: 1M × 1 MB = 1 TB
With 3x replication: 3 TB
5-year growth (20% annually): 3 TB × (1.2)^5 ≈ 7.5 TB
```

**Bandwidth Estimates:**
- **Incoming**: Data received by system
- **Outgoing**: Data sent by system
- **Calculation**: Request size × Requests per second × 8 (bits per byte)

**Calculation Example:**
```
Average request size: 1 KB
Requests per second: 348
Incoming bandwidth: 348 × 1 KB × 8 = 2.78 Mbps
Average response size: 10 KB
Outgoing bandwidth: 348 × 10 KB × 8 = 27.8 Mbps
```

#### 3. System API Design

**Theoretical Foundation:**
API design follows principles of interface design, information hiding, and contract-based programming.

**API Design Principles:**
- **RESTful**: Representational State Transfer
  - Resources as nouns (e.g., /users, /orders)
  - HTTP methods as verbs (GET, POST, PUT, DELETE)
  - Stateless: Each request contains all necessary information
- **GraphQL**: Query language for APIs
  - Single endpoint
  - Client specifies required fields
  - Reduces over-fetching and under-fetching
- **gRPC**: High-performance RPC framework
  - Protocol Buffers for serialization
  - HTTP/2 for transport
  - Strong typing

**Request/Response Formats:**
- **JSON**: Human-readable, widely supported
- **Protocol Buffers**: Binary, efficient, strongly typed
- **MessagePack**: Binary JSON alternative

**API Versioning Strategies:**
- **URL Versioning**: /api/v1/users
- **Header Versioning**: Accept: application/vnd.api.v1+json
- **Query Parameter**: /api/users?version=1

#### 4. Database Design

**Theoretical Foundation:**
Database design is based on relational algebra, normalization theory, and distributed database principles.

**Data Models:**
- **Relational Model**: Based on set theory and predicate logic
  - Tables (relations), rows (tuples), columns (attributes)
  - Normalization: Eliminate redundancy (1NF, 2NF, 3NF, BCNF)
- **Document Model**: Hierarchical, tree-like structures
- **Key-Value Model**: Simple key-value pairs
- **Graph Model**: Nodes and edges

**Schema Design:**
- **Normalization**: Reduce redundancy, improve integrity
- **Denormalization**: Improve read performance at cost of redundancy
- **Indexing Strategy**: Balance query performance and write cost

**Data Partitioning:**
- **Horizontal Partitioning (Sharding)**: Split rows across databases
- **Vertical Partitioning**: Split columns across databases
- **Partitioning Strategies**:
  - Range-based: Partition by value ranges
  - Hash-based: Partition by hash function
  - Directory-based: Lookup table for routing

#### 5. High-Level Design

**Theoretical Foundation:**
High-level design uses architectural patterns and design principles to organize system components.

**Architectural Patterns:**
- **Layered Architecture**: Presentation, Business Logic, Data layers
- **Microservices**: Independent, loosely coupled services
- **Event-Driven**: Components communicate via events
- **Service-Oriented**: Services provide functionality

**Component Interactions:**
- **Synchronous**: Request-response pattern
- **Asynchronous**: Message queues, event streams
- **Communication Protocols**: HTTP, gRPC, WebSocket, Message Queue

#### 6. Detailed Design

**Theoretical Foundation:**
Detailed design applies algorithms, data structures, and design patterns to implement components.

**Algorithm Selection:**
- **Time Complexity**: Big O notation (O(1), O(log n), O(n), O(n²))
- **Space Complexity**: Memory requirements
- **Trade-offs**: Speed vs memory, accuracy vs approximation

**Data Structure Selection:**
- **Arrays**: O(1) access, O(n) insertion
- **Hash Tables**: O(1) average access, O(n) worst case
- **Trees**: O(log n) operations for balanced trees
- **Graphs**: Represent relationships

#### 7. Identify Bottlenecks

**Theoretical Foundation:**
Bottleneck analysis uses performance profiling, queueing theory, and system analysis.

**Bottleneck Types:**
- **CPU Bound**: Limited by processing power
- **Memory Bound**: Limited by available memory
- **I/O Bound**: Limited by disk or network I/O
- **Database Bound**: Limited by database performance

**Analysis Methods:**
- **Profiling**: Measure where time is spent
- **Load Testing**: Test under expected load
- **Capacity Planning**: Predict when limits are reached

#### 8. Scale the Design

**Theoretical Foundation:**
Scaling strategies are based on distributed systems theory, load balancing algorithms, and caching principles.

**Scaling Strategies:**
- **Horizontal Scaling**: Add more machines
  - Requires load balancing
  - Requires data distribution
- **Vertical Scaling**: Increase machine power
  - Limited by hardware
  - Simpler but expensive
- **Caching**: Reduce load on backend
  - Trade memory for speed
  - Cache invalidation strategies

### Key Metrics

**Theoretical Foundation:**
Metrics provide quantitative measures of system behavior. They're based on probability theory, statistics, and performance analysis.

#### Latency
**Definition**: Time to process a single request from start to finish.

**Components:**
- **Network Latency**: Propagation delay + transmission delay + queuing delay
  - Propagation: Distance / Speed of light
  - Transmission: Packet size / Bandwidth
  - Queuing: Time in network buffers
- **Processing Latency**: CPU time to process request
- **I/O Latency**: Time for disk or database operations

**Measurement:**
- **Percentiles**: P50 (median), P95, P99, P99.9
- **Distribution**: Normal, exponential, long-tail

#### Throughput
**Definition**: Number of requests processed per unit time.

**Theoretical Model:**
Throughput = 1 / (Average Latency) × Number of Parallel Workers

**Factors:**
- **Concurrency**: Number of simultaneous requests
- **Bottlenecks**: Slowest component limits throughput
- **Resource Utilization**: CPU, memory, I/O usage

#### Availability
**Definition**: Percentage of time system is operational.

**Mathematical Model:**
Availability = (Total Time - Downtime) / Total Time

**Components:**
- **MTBF (Mean Time Between Failures)**: Average uptime
- **MTTR (Mean Time To Repair)**: Average repair time
- **Availability = MTBF / (MTBF + MTTR)**

**Redundancy Impact:**
- **Single Component**: Availability = A
- **N Components in Series**: Availability = A^N (decreases)
- **N Components in Parallel**: Availability = 1 - (1-A)^N (increases)

#### Consistency
**Definition**: Guarantees about data correctness across system.

**Consistency Models:**
- **Strong Consistency**: All nodes see same data immediately
  - Linearizability: All operations appear atomic
  - Sequential Consistency: Operations appear in some sequential order
- **Eventual Consistency**: Nodes eventually converge to same state
  - BASE: Basically Available, Soft state, Eventual consistency
- **Weak Consistency**: No guarantees about when updates are visible

**CAP Theorem:**
- **Consistency**: All nodes see same data
- **Availability**: System remains operational
- **Partition Tolerance**: System works despite network failures
- **Impossibility**: Cannot have all three simultaneously

#### Durability
**Definition**: Guarantee that committed data persists even after failures.

**ACID Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Valid state transitions
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

**Implementation:**
- **Write-Ahead Logging (WAL)**: Log changes before applying
- **Replication**: Multiple copies of data
- **Backups**: Periodic snapshots

---

## System Design Principles

### Scalability

**Theoretical Foundation:**
Scalability theory is based on parallel computing, distributed systems, and performance analysis. It addresses how systems can grow to handle increased load.

#### Horizontal Scaling (Scale Out)

**Definition**: Adding more machines to handle increased load.

**Theoretical Model:**
- **Linear Scaling**: Performance increases proportionally with machines
  - Ideal: 2 machines = 2x performance
  - Reality: Overhead reduces efficiency
- **Amdahl's Law**: Maximum speedup limited by sequential portion
  - Speedup = 1 / (S + (1-S)/N)
  - S = Sequential portion (0 to 1)
  - N = Number of processors
  - Example: If 10% is sequential, max speedup = 10x (regardless of N)

**Challenges:**
- **Network Overhead**: Communication between machines
- **Data Distribution**: Ensuring data is accessible
- **Load Balancing**: Distributing work evenly
- **Consistency**: Maintaining data consistency across machines

**When to Use:**
- High read-to-write ratio
- Stateless services
- Need for geographic distribution
- Cost-effective commodity hardware

#### Vertical Scaling (Scale Up)

**Definition**: Increasing power of existing machines (CPU, RAM, storage).

**Theoretical Model:**
- **Hardware Limits**: Physical constraints on single machine
- **Cost Curve**: Exponential cost increase for linear performance gain
- **Single Point of Failure**: One machine handles all load

**Advantages:**
- Simpler architecture
- No data distribution needed
- Lower latency (no network overhead)
- Easier to manage

**Limitations:**
- Hardware limits
- Expensive at high scale
- Single point of failure
- Limited by physical laws

#### Stateless Services

**Theoretical Foundation:**
Stateless design follows the principle of idempotency and request independence.

**Definition**: Services that don't store client state between requests.

**Benefits:**
- **Horizontal Scalability**: Any server can handle any request
- **Load Balancing**: Easy to distribute load
- **Fault Tolerance**: Server failure doesn't lose state
- **Simplified Architecture**: No state synchronization needed

**State Management Strategies:**
- **Client-Side State**: Store in cookies, local storage
- **Database State**: Store in shared database
- **Cache State**: Store in distributed cache (Redis)
- **Token-Based**: JWT tokens contain state

**Example:**
```javascript
// Stateless (scalable)
app.get('/api/user', (req, res) => {
  const userId = req.headers['user-id']; // State in request
  const user = database.getUser(userId);
  res.json(user);
});

// Stateful (not scalable)
const sessions = {}; // State in memory
app.get('/api/user', (req, res) => {
  const sessionId = req.cookies.sessionId;
  const user = sessions[sessionId]; // Problem: only on one server
  res.json(user);
});
```

#### Database Sharding

**Theoretical Foundation:**
Sharding is based on data partitioning theory, hash functions, and distributed database principles.

**Definition**: Partitioning data across multiple databases.

**Sharding Strategies:**
1. **Range-Based Sharding**
   - Partition by value ranges
   - Example: Users A-F in shard 1, G-M in shard 2
   - Pros: Simple, good for range queries
   - Cons: Uneven distribution, hot spots

2. **Hash-Based Sharding**
   - Partition by hash function
   - Example: hash(user_id) % num_shards
   - Pros: Even distribution
   - Cons: Difficult to change shard count

3. **Directory-Based Sharding**
   - Lookup table maps keys to shards
   - Pros: Flexible, easy to rebalance
   - Cons: Single point of failure, lookup overhead

**Sharding Challenges:**
- **Cross-Shard Queries**: Difficult to query across shards
- **Rebalancing**: Moving data when adding/removing shards
- **Transaction Support**: ACID transactions across shards are complex
- **Hot Spots**: Some shards may have more load

### Reliability

**Theoretical Foundation:**
Reliability theory is based on probability, fault tolerance, and system resilience.

#### Fault Tolerance

**Definition**: System's ability to continue operating despite component failures.

**Fault Models:**
1. **Crash Failure**: Component stops working
   - Simplest to handle
   - Can detect via timeouts/heartbeats

2. **Omission Failure**: Component fails to send/receive messages
   - Network partitions
   - Message loss

3. **Byzantine Failure**: Component behaves arbitrarily
   - Most difficult to handle
   - Requires consensus algorithms

**Fault Tolerance Techniques:**
- **Replication**: Multiple copies of components
- **Checkpointing**: Save state periodically
- **Rollback Recovery**: Restore to previous state
- **Error Detection**: Identify failures quickly

#### Redundancy

**Theoretical Foundation:**
Redundancy theory is based on probability and reliability engineering.

**Redundancy Types:**
1. **Active Redundancy (Hot Standby)**
   - All components run simultaneously
   - Fast failover
   - Higher resource usage

2. **Passive Redundancy (Cold Standby)**
   - Backup components activate on failure
   - Slower failover
   - Lower resource usage

3. **N+1 Redundancy**
   - N components needed, N+1 available
   - Can tolerate one failure

**Reliability Calculation:**
- Single component reliability: R
- N components in parallel: Reliability = 1 - (1-R)^N
- Example: R=0.9, N=3 → Reliability = 1 - (0.1)^3 = 0.999

#### Health Checks

**Theoretical Foundation:**
Health monitoring uses heartbeat protocols and failure detection algorithms.

**Health Check Types:**
- **Liveness Check**: Is component running?
- **Readiness Check**: Can component handle requests?
- **Startup Check**: Has component initialized?

**Implementation:**
- **Heartbeat**: Periodic "I'm alive" messages
- **Timeout**: Detect missing heartbeats
- **Exponential Backoff**: Reduce check frequency for healthy components

#### Graceful Degradation

**Theoretical Foundation:**
Degradation strategies are based on service prioritization and quality of service (QoS) principles.

**Definition**: System reduces functionality rather than failing completely.

**Strategies:**
- **Feature Flags**: Disable non-critical features
- **Read-Only Mode**: Allow reads, disable writes
- **Reduced Functionality**: Provide basic service
- **Queue Throttling**: Limit request rate

### Availability

**Theoretical Foundation:**
Availability theory combines reliability engineering with system design principles.

#### High Availability (HA)

**Definition**: System designed for 99.9%+ uptime.

**Mathematical Model:**
- Availability = Uptime / (Uptime + Downtime)
- Downtime = MTTR / (MTBF + MTTR)
- Availability = MTBF / (MTBF + MTTR)

**Achieving High Availability:**
1. **Eliminate Single Points of Failure**
   - Multiple components
   - Redundant paths

2. **Fast Failure Detection**
   - Health checks
   - Monitoring

3. **Automatic Failover**
   - No manual intervention
   - Minimal downtime

4. **Data Replication**
   - Multiple copies
   - Geographic distribution

#### Replication

**Theoretical Foundation:**
Replication theory addresses consistency, availability, and partition tolerance trade-offs.

**Replication Strategies:**
1. **Master-Slave (Primary-Secondary)**
   - One master handles writes
   - Slaves handle reads
   - Simple but master is bottleneck

2. **Master-Master (Multi-Master)**
   - Multiple masters handle writes
   - Better write scalability
   - Conflict resolution needed

3. **Quorum-Based**
   - Write to majority of replicas
   - Read from majority
   - Ensures consistency

**Replication Models:**
- **Synchronous**: Wait for all replicas
  - Strong consistency
  - Higher latency
- **Asynchronous**: Don't wait
  - Lower latency
  - Eventual consistency

#### Failover

**Theoretical Foundation:**
Failover mechanisms use leader election algorithms and consensus protocols.

**Failover Types:**
1. **Automatic Failover**
   - No human intervention
   - Fast recovery
   - Requires monitoring

2. **Manual Failover**
   - Human decision
   - Slower
   - More control

**Failover Process:**
1. Detect failure (health check, timeout)
2. Elect new primary (leader election)
3. Update routing (DNS, load balancer)
4. Verify new primary is ready

#### Disaster Recovery

**Theoretical Foundation:**
Disaster recovery planning is based on risk assessment and business continuity principles.

**Recovery Objectives:**
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss

**Recovery Strategies:**
- **Backup and Restore**: Periodic backups, restore on failure
- **Hot Standby**: Always-on backup system
- **Multi-Region**: Geographic redundancy

### Consistency

**Theoretical Foundation:**
Consistency models are based on distributed systems theory, particularly the CAP theorem and ACID properties.

#### Strong Consistency

**Definition**: All nodes see the same data simultaneously.

**Consistency Models:**
1. **Linearizability**
   - All operations appear atomic
   - Total order of operations
   - Strongest consistency model

2. **Sequential Consistency**
   - Operations appear in some sequential order
   - Order consistent per process
   - Weaker than linearizability

3. **Causal Consistency**
   - Preserves cause-effect relationships
   - Weaker than sequential

**Implementation:**
- **Two-Phase Commit (2PC)**: Coordinated commit across nodes
- **Paxos/Raft**: Consensus algorithms
- **Quorum Reads/Writes**: Read/write from majority

#### Eventual Consistency

**Definition**: Nodes eventually converge to the same state.

**Theoretical Model:**
- **BASE**: Basically Available, Soft state, Eventual consistency
- **Convergence**: All replicas eventually agree
- **No Guarantees**: No timing guarantees

**Use Cases:**
- Social media feeds
- DNS
- CDN content
- Analytics systems

**Trade-offs:**
- **Pros**: High availability, better performance
- **Cons**: May read stale data, conflict resolution needed

#### CAP Theorem

**Theoretical Foundation:**
CAP theorem (Brewer's Theorem) is a fundamental result in distributed systems theory.

**Statement**: In a distributed system, you can have at most 2 of 3:
- **Consistency**: All nodes see same data
- **Availability**: System remains operational
- **Partition Tolerance**: System works despite network failures

**Proof Intuition:**
- During network partition, nodes can't communicate
- If we choose Availability: Nodes respond with potentially stale data (sacrifice Consistency)
- If we choose Consistency: Nodes wait for partition to heal (sacrifice Availability)
- Partition Tolerance is required in distributed systems (networks can fail)

**CAP Trade-offs:**
1. **CP (Consistency + Partition Tolerance)**
   - Examples: Traditional databases, distributed locks
   - Sacrifice: Availability during partitions

2. **AP (Availability + Partition Tolerance)**
   - Examples: DNS, CDN, NoSQL (DynamoDB, Cassandra)
   - Sacrifice: Consistency (eventual consistency)

3. **CA (Consistency + Availability)**
   - Only possible in non-distributed systems
   - Single-node systems

**Real-World Systems:**
- Most systems choose AP with eventual consistency
- Strong consistency when needed (financial transactions)
- Weak consistency for performance (social feeds)

### Performance

**Theoretical Foundation:**
Performance optimization is based on computer architecture, algorithms, and system analysis.

#### Caching

**Theoretical Foundation:**
Caching theory is based on locality of reference and memory hierarchy.

**Locality Principles:**
- **Temporal Locality**: Recently accessed data likely to be accessed again
- **Spatial Locality**: Data near recently accessed data likely to be accessed

**Cache Performance:**
- **Hit Rate**: Percentage of requests served from cache
- **Miss Rate**: 1 - Hit Rate
- **Effective Access Time**: Hit Time × Hit Rate + Miss Time × Miss Rate

**Cache Replacement Policies:**
- **LRU (Least Recently Used)**: Evict least recently used
- **LFU (Least Frequently Used)**: Evict least frequently used
- **FIFO (First In First Out)**: Evict oldest
- **Random**: Random eviction

#### CDN (Content Delivery Network)

**Theoretical Foundation:**
CDN theory is based on network topology, caching, and geographic distribution.

**How CDNs Work:**
1. **Origin Server**: Original content source
2. **Edge Servers**: Distributed servers close to users
3. **Caching**: Store content at edge
4. **Routing**: Route users to nearest edge

**Benefits:**
- **Reduced Latency**: Shorter distance to content
- **Reduced Bandwidth**: Less load on origin
- **Better Availability**: Multiple copies

**CDN Strategies:**
- **Push CDN**: Proactively push content to edges
- **Pull CDN**: Cache on first request

#### Database Optimization

**Theoretical Foundation:**
Database optimization is based on query processing, indexing theory, and access methods.

**Indexing Theory:**
- **B-Tree Index**: O(log n) search, good for range queries
- **Hash Index**: O(1) average, O(n) worst case, equality only
- **Bitmap Index**: Good for low-cardinality columns

**Query Optimization:**
- **Cost-Based Optimization**: Estimate cost of different plans
- **Rule-Based Optimization**: Apply transformation rules
- **Join Algorithms**: Nested loop, hash join, merge join

#### Asynchronous Processing

**Theoretical Foundation:**
Asynchronous processing is based on concurrency theory and event-driven architecture.

**Benefits:**
- **Non-Blocking**: Don't wait for slow operations
- **Better Throughput**: Process multiple requests concurrently
- **Resource Utilization**: Better CPU/IO utilization

**Patterns:**
- **Message Queues**: Decouple producers and consumers
- **Event-Driven**: React to events
- **Callback/Promise**: Handle async results

---

## Scalability

### Horizontal Scaling
```
Single Server
    ↓
Load Balancer
    ↓
[Server 1] [Server 2] [Server 3] ... [Server N]
```

**Advantages:**
- No hardware limits
- Cost-effective
- Better fault tolerance

**Challenges:**
- Data consistency
- Session management
- Distributed transactions

### Vertical Scaling
```
Small Server → Medium Server → Large Server
```

**Advantages:**
- Simpler architecture
- No data distribution needed
- Lower latency

**Challenges:**
- Hardware limits
- Single point of failure
- Expensive

### Scaling Strategies

#### 1. Read Replicas
```
Write → Master Database
Read → [Replica 1] [Replica 2] [Replica 3]
```

#### 2. Database Sharding
```
Shard 1: Users A-F
Shard 2: Users G-M
Shard 3: Users N-Z
```

#### 3. Caching Layer
```
Application → Cache → Database
```

#### 4. CDN
```
User → CDN Edge Server → Origin Server
```

### Scalability Patterns

#### Stateless Services
```javascript
// Stateless service (scalable)
app.get('/api/user', (req, res) => {
  const userId = req.headers['user-id'];
  const user = getUserFromDatabase(userId);
  res.json(user);
});

// Stateful service (not scalable)
const sessions = {}; // Stored in memory
app.get('/api/user', (req, res) => {
  const sessionId = req.cookies.sessionId;
  const user = sessions[sessionId]; // Problem: sessions only on one server
  res.json(user);
});
```

#### Database Partitioning
```sql
-- Horizontal partitioning (sharding)
-- Shard 1: user_id % 4 = 0
-- Shard 2: user_id % 4 = 1
-- Shard 3: user_id % 4 = 2
-- Shard 4: user_id % 4 = 3

-- Vertical partitioning
-- Table 1: user_id, name, email
-- Table 2: user_id, profile_data, settings
```

---

## Load Balancing

### What is Load Balancing?

**Theoretical Foundation:**
Load balancing is based on queueing theory, network routing algorithms, and distributed systems principles. It's a fundamental technique for achieving scalability and high availability.

**Definition**: Distributing incoming network traffic across multiple servers to ensure no single server is overwhelmed, optimizing resource utilization and maximizing throughput.

**Mathematical Model:**
- **Load Distribution**: Given N servers, distribute load L such that each server handles approximately L/N
- **Queueing Theory**: Model each server as a queue
  - Arrival rate: λ (requests/second)
  - Service rate: μ (requests/second per server)
  - Utilization: ρ = λ / (N × μ)
  - For stability: ρ < 1

**Benefits:**
1. **Scalability**: Add servers to handle more load
2. **Availability**: If one server fails, others continue
3. **Performance**: Distribute load evenly
4. **Flexibility**: Add/remove servers dynamically

**Load Balancing Architecture:**
```
Client Request
    ↓
Load Balancer (Decision Point)
    ↓
[Server 1] [Server 2] [Server 3] ... [Server N]
```

### Load Balancing Algorithms

**Theoretical Foundation:**
Load balancing algorithms are based on scheduling theory, graph algorithms, and optimization techniques.

#### 1. Round Robin

**Definition**: Distribute requests sequentially across servers in rotation.

**Algorithm:**
```
Server index = (Request number) mod (Number of servers)
```

**Mathematical Model:**
- **Fairness**: Each server gets 1/N of requests (assuming equal capacity)
- **Time Complexity**: O(1) per request
- **Space Complexity**: O(1) for state

**Advantages:**
- Simple to implement
- Fair distribution (if servers equal)
- No state needed

**Disadvantages:**
- Doesn't consider server load
- Doesn't consider server capacity
- Uneven if servers have different capacities

**Use Case**: Servers with equal capacity and similar load

#### 2. Least Connections

**Definition**: Route to server with fewest active connections.

**Algorithm:**
```
Selected server = argmin(active_connections[i] for i in servers)
```

**Theoretical Foundation:**
Based on queueing theory - servers with fewer connections likely have shorter queues.

**Mathematical Model:**
- **Queue Length**: Number of active connections approximates queue length
- **Response Time**: Shorter queue → lower response time (Little's Law)

**Advantages:**
- Adapts to server load
- Better for long-lived connections
- Considers current state

**Disadvantages:**
- Requires tracking connection counts
- May not reflect actual load (connections may be idle)
- More complex than round robin

**Use Case**: Long-lived connections (WebSocket, database connections)

#### 3. Weighted Round Robin

**Definition**: Round robin with weights representing server capacity.

**Algorithm:**
```
Total weight = sum(weights)
Current weight = (Current weight + Server weight) mod Total weight
Select server with highest current weight
```

**Mathematical Model:**
- **Distribution**: Server i gets (weight[i] / total_weight) fraction of requests
- **Example**: Weights [3, 1, 2] → Server 1 gets 50%, Server 2 gets 16.7%, Server 3 gets 33.3%

**Advantages:**
- Handles servers with different capacities
- Still simple to implement
- Predictable distribution

**Disadvantages:**
- Weights must be manually configured
- Doesn't adapt to changing load
- Assumes weights reflect actual capacity

**Use Case**: Servers with known different capacities

#### 4. IP Hash

**Definition**: Hash client IP address to consistently route to same server.

**Algorithm:**
```
Server index = hash(client_ip) mod (Number of servers)
```

**Theoretical Foundation:**
Based on consistent hashing and hash functions. Ensures same client always goes to same server (useful for session persistence).

**Hash Function Properties:**
- **Deterministic**: Same input → same output
- **Uniform Distribution**: Even distribution across servers
- **Avalanche Effect**: Small input change → large output change

**Mathematical Model:**
- **Collision Probability**: For N servers, probability of collision ≈ 1/N
- **Distribution**: With good hash function, each server gets ~1/N of clients

**Advantages:**
- Session persistence (sticky sessions)
- No state needed in load balancer
- Deterministic routing

**Disadvantages:**
- Uneven if IP distribution is skewed
- Difficult to add/remove servers (rehashing)
- Doesn't consider server load

**Use Case**: When session persistence is needed

**Consistent Hashing:**
- Solves rehashing problem
- Only remaps K/N keys when adding/removing server (K = keys, N = servers)
- Uses hash ring: servers and keys mapped to ring

#### 5. Least Response Time

**Definition**: Route to server with lowest average response time.

**Algorithm:**
```
Selected server = argmin(avg_response_time[i] for i in servers)
```

**Theoretical Foundation:**
Based on performance monitoring and adaptive algorithms. Response time is a good indicator of server health and load.

**Mathematical Model:**
- **Exponential Moving Average**: 
  - EMA = α × current_response + (1-α) × previous_EMA
  - α = smoothing factor (typically 0.1-0.3)
- **Response Time Components**: Network latency + processing time + queue time

**Advantages:**
- Adapts to server performance
- Considers actual server health
- Better user experience

**Disadvantages:**
- Requires response time measurement
- May cause oscillations (all traffic to fastest server)
- More complex implementation

**Use Case**: When response time is critical

#### 6. Resource-Based (CPU/Memory)

**Definition**: Route based on server resource utilization.

**Algorithm:**
```
Selected server = argmin(cpu_usage[i] or memory_usage[i] for i in servers)
```

**Theoretical Foundation:**
Based on resource monitoring and capacity planning. Directly measures server capacity.

**Advantages:**
- Direct measure of server capacity
- Prevents overloading servers
- Adapts to changing conditions

**Disadvantages:**
- Requires resource monitoring
- May not reflect actual request handling capacity
- More overhead

**Use Case**: When resource utilization is critical

### Load Balancer Types

#### 1. Layer 4 (Transport Layer)
- Routes based on IP and port
- Faster, less intelligent
- Examples: AWS Network Load Balancer

#### 2. Layer 7 (Application Layer)
- Routes based on HTTP headers, URL
- More intelligent, can do SSL termination
- Examples: AWS Application Load Balancer, Nginx

### Load Balancer Placement

```
Internet
    ↓
DNS Load Balancer (Round Robin)
    ↓
[Load Balancer 1] [Load Balancer 2]
    ↓                    ↓
[App Server 1]    [App Server 2]
[App Server 3]    [App Server 4]
```

### Session Persistence (Sticky Sessions)
```
Client → Load Balancer → Server 1
Client → Load Balancer → Server 1 (same server)
```

**Implementation:**
- Cookie-based routing
- IP-based routing
- URL-based routing

### Health Checks
```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: Date.now(),
    database: checkDatabase(),
    cache: checkCache()
  };
  
  if (health.database && health.cache) {
    res.status(200).json(health);
  } else {
    res.status(503).json(health);
  }
});
```

---

## Caching

### What is Caching?

**Theoretical Foundation:**
Caching is based on the principle of locality of reference, memory hierarchy, and the time-space trade-off. It's one of the most fundamental optimization techniques in computer science.

**Definition**: Storing frequently accessed data in fast storage (closer to the processor or user) to reduce access latency and backend load.

**Locality of Reference:**
- **Temporal Locality**: Recently accessed data is likely to be accessed again soon
  - Principle: "If you used it recently, you'll probably use it again"
  - Example: User profile accessed once, likely accessed again
- **Spatial Locality**: Data near recently accessed data is likely to be accessed
  - Principle: "If you used this, you'll probably use nearby data"
  - Example: Accessing array elements sequentially

**Memory Hierarchy:**
```
CPU Registers (fastest, smallest)
    ↓
L1 Cache
    ↓
L2 Cache
    ↓
L3 Cache
    ↓
RAM
    ↓
SSD/HDD (slowest, largest)
```

**Cache Performance Metrics:**
- **Hit Rate (H)**: Percentage of requests served from cache
  - H = Cache Hits / Total Requests
- **Miss Rate (M)**: Percentage of requests not in cache
  - M = 1 - H = Cache Misses / Total Requests
- **Effective Access Time (EAT)**:
  - EAT = H × Hit_Time + M × Miss_Time
  - Example: H=0.9, Hit_Time=1ms, Miss_Time=100ms
  - EAT = 0.9×1 + 0.1×100 = 10.9ms (vs 100ms without cache)

**Cache Benefits:**
1. **Reduced Latency**: Fast access to cached data
2. **Reduced Load**: Less load on backend systems
3. **Better Scalability**: Handle more requests with same backend
4. **Cost Savings**: Reduce database/API costs

**Cache Trade-offs:**
- **Memory Cost**: Caching requires memory/storage
- **Consistency**: Cached data may be stale
- **Complexity**: Cache invalidation and management

### Cache Types

**Theoretical Foundation:**
Different cache types are positioned at different layers of the system architecture, following the principle of placing data closer to where it's needed.

#### 1. Application Cache (In-Memory Cache)

**Architecture:**
```
Application → Cache (Memory) → Database
```

**Theoretical Model:**
- **Storage**: RAM (fastest, but volatile)
- **Access Time**: ~100 nanoseconds (vs milliseconds for disk)
- **Capacity**: Limited by available RAM
- **Persistence**: Lost on restart (unless persisted)

**Cache Implementations:**
- **Local Cache**: In-process memory (fastest, but not shared)
- **Distributed Cache**: Shared across processes (Redis, Memcached)

**Mathematical Model:**
- **Memory Usage**: Cache_Size = Number_of_Items × Average_Item_Size
- **Hit Rate**: Depends on access pattern (Zipf distribution common)
- **Eviction**: When cache full, evict items (LRU, LFU, etc.)

**Use Cases:**
- Frequently accessed database queries
- Session data
- Computed results
- API responses

#### 2. CDN Cache (Content Delivery Network)

**Architecture:**
```
User → CDN Edge Server (cached) → Origin Server
```

**Theoretical Foundation:**
CDN caching is based on geographic distribution, network topology, and content replication.

**How CDNs Work:**
1. **Origin Server**: Original content source
2. **Edge Servers**: Distributed servers geographically close to users
3. **Caching**: Store content at edge servers
4. **Routing**: Route users to nearest edge (DNS-based or Anycast)

**Mathematical Model:**
- **Latency Reduction**: 
  - Without CDN: User → Origin (distance D, latency L)
  - With CDN: User → Edge (distance d, latency l) where d << D
  - Latency reduction: L - l
- **Bandwidth Savings**: 
  - If hit rate H, bandwidth saved = H × Content_Size × Requests

**CDN Strategies:**
- **Push CDN**: Proactively push content to edges
  - Good for: Predictable content, high traffic
- **Pull CDN**: Cache on first request
  - Good for: Dynamic content, unpredictable traffic

**Use Cases:**
- Static assets (images, CSS, JS)
- Video streaming
- Software downloads
- API responses (if cacheable)

#### 3. Database Cache (Query Result Cache)

**Architecture:**
```
Query → Cache (Query Result) → Database
```

**Theoretical Foundation:**
Database caching is based on query result caching and materialized views.

**Cache Granularity:**
- **Query-Level**: Cache entire query results
- **Table-Level**: Cache entire tables
- **Row-Level**: Cache individual rows

**Mathematical Model:**
- **Cache Key**: Hash of query + parameters
- **Cache Value**: Query result set
- **Invalidation**: On table/row updates

**Benefits:**
- **Reduced Database Load**: Expensive queries cached
- **Faster Response**: No database query needed
- **Scalability**: Handle more queries

**Challenges:**
- **Cache Invalidation**: When data changes, cache must update
- **Memory Usage**: Large result sets consume memory
- **Consistency**: Stale data if invalidation fails

**Use Cases:**
- Expensive queries (joins, aggregations)
- Frequently accessed data
- Read-heavy workloads

#### 4. Browser Cache (Client-Side Cache)

**Architecture:**
```
Browser → Cache (Local Storage) → Server
```

**Theoretical Foundation:**
Browser caching uses HTTP caching headers and local storage mechanisms.

**HTTP Caching:**
- **Cache-Control**: max-age, no-cache, no-store
- **ETag**: Entity tag for validation
- **Last-Modified**: Timestamp for validation
- **Expires**: Absolute expiration time

**Cache Validation:**
- **Strong Validation**: If-Modified-Since, If-None-Match
- **Server Response**: 304 Not Modified (use cache) or 200 OK (new content)

**Browser Storage Types:**
- **HTTP Cache**: Automatic, controlled by headers
- **LocalStorage**: Persistent, 5-10MB limit
- **SessionStorage**: Session-scoped, 5-10MB limit
- **IndexedDB**: Large storage, structured data

**Mathematical Model:**
- **Bandwidth Savings**: 
  - Saved_Bandwidth = Cache_Hit_Rate × Content_Size × Requests
- **Latency Reduction**: 
  - Local access: ~1ms (vs network: 50-200ms)

**Use Cases:**
- Static assets (images, CSS, JS)
- API responses (if cacheable)
- User preferences
- Offline functionality

### Caching Strategies

**Theoretical Foundation:**
Caching strategies are based on write-through vs write-back policies, cache coherence protocols, and consistency models. Each strategy represents a different trade-off between consistency, performance, and complexity.

#### 1. Cache-Aside (Lazy Loading)

**Theoretical Foundation:**
Cache-aside follows the principle of "load on demand" - data is loaded into cache only when needed (cache miss).

**Definition**: Application is responsible for loading data into cache. Cache doesn't interact with database directly.

**Algorithm:**
```
1. Check cache
2. If cache hit: return data
3. If cache miss:
   a. Load from database
   b. Store in cache
   c. Return data
```

**Mathematical Model:**
- **Expected Access Time**: 
  - EAT = H × Cache_Time + (1-H) × (Cache_Time + DB_Time + Write_Cache_Time)
  - Where H = hit rate
- **Cache Hit Rate**: Depends on access pattern
  - Uniform: H = min(1, Cache_Size / Total_Items)
  - Zipf (common): H higher for popular items

**Advantages:**
- **Simple**: Easy to implement
- **Flexible**: Application controls what to cache
- **Fault Tolerant**: Cache failure doesn't break application

**Disadvantages:**
- **Cache Miss Penalty**: Two round trips (cache + database)
- **Stale Data Risk**: Cache may have stale data if updated elsewhere
- **Cache Stampede**: Multiple requests miss simultaneously, all query database

**Use Cases:**
- Read-heavy workloads
- When cache is optional (not critical path)
- When data access patterns are unpredictable

**Implementation:**
```javascript
async function getUser(userId) {
  // Check cache
  let user = cache.get(`user:${userId}`);
  
  if (!user) {
    // Cache miss - load from database
    user = await database.getUser(userId);
    // Store in cache
    cache.set(`user:${userId}`, user, 3600); // TTL: 1 hour
  }
  
  return user;
}
```

**Cache Stampede Prevention:**
```javascript
const locks = new Map();

async function getUser(userId) {
  let user = cache.get(`user:${userId}`);
  if (user) return user;
  
  // Check if another request is loading
  if (locks.has(userId)) {
    await locks.get(userId);
    return cache.get(`user:${userId}`);
  }
  
  // Lock and load
  const promise = database.getUser(userId).then(user => {
    cache.set(`user:${userId}`, user);
    locks.delete(userId);
    return user;
  });
  
  locks.set(userId, promise);
  return promise;
}
```

#### 2. Write-Through

**Theoretical Foundation:**
Write-through follows the principle of "write to both cache and database synchronously" - ensures cache and database are always consistent.

**Definition**: Write to cache and database simultaneously. Cache acts as write-through buffer.

**Algorithm:**
```
1. Write to database
2. Write to cache
3. Return success
```

**Mathematical Model:**
- **Write Latency**: 
  - Latency = max(DB_Write_Time, Cache_Write_Time)
  - Typically: Latency = DB_Write_Time (slower)
- **Consistency**: Strong consistency (cache and DB always match)

**Advantages:**
- **Strong Consistency**: Cache and database always in sync
- **Data Safety**: Data persisted immediately
- **Simple**: Straightforward logic

**Disadvantages:**
- **Higher Write Latency**: Must wait for both writes
- **Write Amplification**: Every write does two operations
- **Cache Pollution**: May cache data that's never read again

**Use Cases:**
- When consistency is critical
- When write performance is acceptable
- Financial transactions
- Critical data updates

**Implementation:**
```javascript
async function updateUser(userId, data) {
  // Update database
  await database.updateUser(userId, data);
  // Update cache
  cache.set(`user:${userId}`, data);
}
```

#### 3. Write-Back (Write-Behind)

**Theoretical Foundation:**
Write-back follows the principle of "write to cache first, database later" - optimizes for write performance at the cost of consistency and durability.

**Definition**: Write to cache immediately, write to database asynchronously later.

**Algorithm:**
```
1. Write to cache (mark as dirty)
2. Queue database write
3. Return success immediately
4. Background: Write dirty items to database
```

**Mathematical Model:**
- **Write Latency**: 
  - Latency = Cache_Write_Time (very fast)
  - vs Write-Through: Latency = DB_Write_Time
- **Durability Risk**: 
  - If cache fails before database write, data lost
  - Risk = P(Cache_Failure) × P(Not_Yet_Written)

**Advantages:**
- **Low Write Latency**: Returns immediately
- **High Write Throughput**: Can batch database writes
- **Better Performance**: Optimized for write-heavy workloads

**Disadvantages:**
- **Data Loss Risk**: Cache failure before database write loses data
- **Complexity**: Need to track dirty items, handle failures
- **Consistency**: Cache and database may be temporarily inconsistent

**Use Cases:**
- Write-heavy workloads
- When write latency is critical
- When some data loss is acceptable
- Analytics, logging

**Implementation:**
```javascript
const dirtyItems = new Set();
const writeQueue = [];

async function updateUser(userId, data) {
  // Update cache immediately
  cache.set(`user:${userId}`, data);
  dirtyItems.add(userId);
  
  // Queue database write
  writeQueue.push({ userId, data });
  
  // Process queue asynchronously
  if (writeQueue.length === 1) {
    processWriteQueue();
  }
}

async function processWriteQueue() {
  while (writeQueue.length > 0) {
    const batch = writeQueue.splice(0, 100); // Batch writes
    await Promise.all(
      batch.map(item => database.updateUser(item.userId, item.data))
    );
    batch.forEach(item => dirtyItems.delete(item.userId));
  }
}
```

#### 4. Refresh-Ahead

**Theoretical Foundation:**
Refresh-ahead is based on predictive caching and proactive data loading. It predicts which data will be needed and preloads it.

**Definition**: Proactively refresh cache entries before they expire, based on access patterns.

**Algorithm:**
```
1. Monitor cache access patterns
2. Predict which items will be accessed soon
3. Refresh those items before expiration
4. User gets fresh data from cache
```

**Mathematical Model:**
- **Refresh Window**: Refresh items expiring within time window W
- **Access Prediction**: 
  - Simple: Refresh items accessed in last T seconds
  - Advanced: Use machine learning to predict access
- **Hit Rate Improvement**: 
  - Without: H = Cache_Hit_Rate
  - With: H' = H + P(Refresh_Before_Expiry) × (1-H)

**Advantages:**
- **Better Hit Rate**: Items refreshed before needed
- **Lower Latency**: Data ready when needed
- **Smoother Performance**: Avoids sudden cache misses

**Disadvantages:**
- **Complexity**: Need prediction logic
- **Resource Usage**: May refresh unused items
- **Tuning Required**: Need to tune refresh window

**Use Cases:**
- Predictable access patterns
- When cache misses are expensive
- Time-sensitive data

**Implementation:**
```javascript
// Simple refresh-ahead: refresh items expiring soon
setInterval(() => {
  const keys = cache.getKeys('user:*');
  keys.forEach(key => {
    const ttl = cache.getTTL(key);
    // Refresh if expiring within 5 minutes
    if (ttl < 300000) {
      const userId = extractUserId(key);
      const user = database.getUser(userId);
      cache.set(key, user, 3600000); // Refresh with new TTL
    }
  });
}, 60000); // Check every minute
```

#### 5. Write-Around

**Theoretical Foundation:**
Write-around is a hybrid approach that writes directly to database, bypassing cache for writes but using cache for reads.

**Definition**: Write directly to database, bypass cache. Cache only used for reads (cache-aside for reads).

**Algorithm:**
```
Write:
1. Write to database
2. Don't update cache
3. Cache will be populated on next read (if needed)

Read:
1. Check cache (cache-aside)
2. If miss, load from database and cache
```

**Advantages:**
- **Avoids Cache Pollution**: Don't cache data that's never read
- **Simple Writes**: No cache update needed
- **Fresh Reads**: Always get latest from database on cache miss

**Disadvantages:**
- **Write-Then-Read Miss**: Write followed by read will miss cache
- **Lower Hit Rate**: May have lower hit rate than write-through

**Use Cases:**
- Write-heavy, read-rarely data
- When cache space is limited
- When avoiding cache pollution is important

### Cache Invalidation

#### 1. Time-Based (TTL)
```javascript
cache.set('key', 'value', 3600); // Expires in 1 hour
```

#### 2. Event-Based
```javascript
// On user update
function updateUser(userId, data) {
  database.updateUser(userId, data);
  cache.delete(`user:${userId}`); // Invalidate cache
}
```

#### 3. Manual Invalidation
```javascript
cache.delete('key');
cache.clear(); // Clear all
```

### Cache Patterns

#### Cache Stampede Prevention
```javascript
const locks = new Map();

async function getUser(userId) {
  let user = cache.get(`user:${userId}`);
  
  if (user) return user;
  
  // Check if another request is loading
  if (locks.has(userId)) {
    // Wait for other request
    await locks.get(userId);
    return cache.get(`user:${userId}`);
  }
  
  // Lock
  const promise = database.getUser(userId);
  locks.set(userId, promise);
  
  try {
    user = await promise;
    cache.set(`user:${userId}`, user);
    return user;
  } finally {
    locks.delete(userId);
  }
}
```

### Popular Caching Solutions

#### Redis
```javascript
const redis = require('redis');
const client = redis.createClient();

// Set
await client.set('key', 'value', { EX: 3600 });

// Get
const value = await client.get('key');

// Hash
await client.hSet('user:1', { name: 'John', age: '30' });
const user = await client.hGetAll('user:1');
```

#### Memcached
```javascript
const memcached = require('memcached');
const client = new memcached('localhost:11211');

// Set
client.set('key', 'value', 3600, (err) => {});

// Get
client.get('key', (err, data) => {});
```

---

## Database Design

### Database Types

**Theoretical Foundation:**
Database design is based on data modeling theory, relational algebra, and distributed systems principles. Different database types represent different trade-offs in the CAP theorem space.

#### 1. Relational (SQL) Databases

**Theoretical Foundation:**
Relational databases are based on relational algebra, set theory, and the ACID properties. They follow Codd's relational model (1970).

**Core Concepts:**
- **Relational Model**: Data organized in tables (relations)
  - Table = Relation
  - Row = Tuple
  - Column = Attribute
- **Relational Algebra**: Mathematical foundation
  - Operations: Select (σ), Project (π), Join (⨝), Union (∪), etc.
- **Normalization**: Eliminate redundancy
  - 1NF: Atomic values, no repeating groups
  - 2NF: 1NF + no partial dependencies
  - 3NF: 2NF + no transitive dependencies
  - BCNF: 3NF + every determinant is candidate key

**ACID Properties:**
- **Atomicity**: All or nothing
  - Transactions are indivisible
  - Either all operations succeed or all fail
  - Implemented via: Transaction logs, rollback
- **Consistency**: Valid state transitions
  - Database remains in valid state
  - Constraints are always satisfied
  - Implemented via: Constraints, triggers
- **Isolation**: Concurrent transactions don't interfere
  - Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable
  - Implemented via: Locking, MVCC (Multi-Version Concurrency Control)
- **Durability**: Committed changes persist
  - Survives system failures
  - Implemented via: Write-ahead logging (WAL), replication

**Mathematical Model:**
- **Transaction**: Sequence of operations that must satisfy ACID
- **Serializability**: Concurrent execution equivalent to some serial execution
- **Conflict Serializability**: Order conflicting operations consistently

**Examples**: MySQL, PostgreSQL, Oracle, SQL Server

**Use Cases:**
- Structured data with relationships
- Transactions requiring ACID guarantees
- Complex queries with joins
- Financial systems, e-commerce

**Trade-offs:**
- **Pros**: Strong consistency, ACID guarantees, mature ecosystem
- **Cons**: Difficult to scale horizontally, schema rigidity

#### 2. NoSQL Databases

**Theoretical Foundation:**
NoSQL databases emerged to address limitations of relational databases, particularly around scalability and schema flexibility. They prioritize availability and partition tolerance (AP in CAP theorem).

**NoSQL Categories:**

##### Document Databases

**Theoretical Foundation:**
Based on document-oriented data modeling, similar to object-oriented programming.

**Data Model:**
- **Documents**: Self-contained units (JSON, BSON, XML)
- **Collections**: Groups of documents
- **No Schema**: Flexible structure

**Mathematical Model:**
- **Document**: Key-value pair where value is nested structure
- **Query**: Path-based access (e.g., user.address.city)

**Examples**: MongoDB, CouchDB, DynamoDB (document mode)

**Use Cases:**
- Content management
- User profiles
- Catalogs
- Semi-structured data

**Trade-offs:**
- **Pros**: Flexible schema, good for hierarchical data, horizontal scaling
- **Cons**: No joins, eventual consistency, limited transactions

##### Key-Value Databases

**Theoretical Foundation:**
Simplest data model, based on hash tables and associative arrays.

**Data Model:**
- **Key**: Unique identifier (string, number, binary)
- **Value**: Any data (string, number, object, binary)
- **Operations**: Get, Put, Delete

**Mathematical Model:**
- **Function**: f: Key → Value
- **Complexity**: O(1) average for hash-based implementations
- **Distribution**: Consistent hashing for sharding

**Examples**: Redis, DynamoDB, Riak, Memcached

**Use Cases:**
- Caching
- Session storage
- Shopping carts
- Real-time analytics

**Trade-offs:**
- **Pros**: Simple, fast, scalable
- **Cons**: No queries, no relationships, limited data types

##### Column-Family Databases

**Theoretical Foundation:**
Based on BigTable model (Google), optimized for wide tables and columnar access.

**Data Model:**
- **Column Families**: Groups of columns
- **Rows**: Identified by row key
- **Columns**: Sparse, can vary per row
- **Time Series**: Versions of values

**Mathematical Model:**
- **Table**: Sparse matrix
- **Access Pattern**: Row key → Column family → Column → Value
- **Storage**: Column-oriented (efficient for analytics)

**Examples**: Cassandra, HBase, Amazon DynamoDB

**Use Cases:**
- Time-series data
- Analytics
- Wide tables
- High write throughput

**Trade-offs:**
- **Pros**: Excellent write performance, horizontal scaling, good for analytics
- **Cons**: Complex data model, eventual consistency, limited transactions

##### Graph Databases

**Theoretical Foundation:**
Based on graph theory, optimized for relationship-heavy data.

**Data Model:**
- **Nodes**: Entities (vertices)
- **Edges**: Relationships (with properties)
- **Properties**: Attributes on nodes and edges

**Mathematical Model:**
- **Graph**: G = (V, E) where V = vertices, E = edges
- **Traversal**: Path finding algorithms (BFS, DFS, shortest path)
- **Queries**: Graph pattern matching

**Examples**: Neo4j, Amazon Neptune, ArangoDB

**Use Cases:**
- Social networks
- Recommendation engines
- Fraud detection
- Knowledge graphs

**Trade-offs:**
- **Pros**: Excellent for relationships, complex queries, intuitive model
- **Cons**: Not good for simple queries, scaling challenges, specialized use case

### Database Scaling

**Theoretical Foundation:**
Database scaling addresses the fundamental challenge of handling increasing load. It's based on distributed systems theory, replication protocols, and partitioning algorithms.

#### 1. Master-Slave Replication (Primary-Secondary)

**Theoretical Foundation:**
Based on primary-backup replication model. One primary handles writes, replicas handle reads.

**Architecture:**
```
Write → Master (Primary)
Read → [Slave 1] [Slave 2] [Slave 3] (Secondaries)
```

**Replication Process:**
1. **Write to Master**: Transaction committed on master
2. **Write-Ahead Log (WAL)**: Changes logged
3. **Replication**: Log entries sent to slaves
4. **Apply Changes**: Slaves apply log entries
5. **Read from Slaves**: Reads can go to any slave

**Mathematical Model:**
- **Replication Lag**: Time between master write and slave apply
  - Lag = Network_Latency + Apply_Time
  - Typical: 10-100ms
- **Read Distribution**: 
  - If N slaves, each handles 1/N of reads (ideally)
  - Read capacity = Master_Capacity + N × Slave_Capacity

**Consistency Model:**
- **Master**: Strong consistency (always latest)
- **Slaves**: Eventual consistency (may be slightly stale)
- **Read-After-Write**: Read from master to ensure consistency

**Advantages:**
- **Read Scalability**: Distribute reads across slaves
- **Fault Tolerance**: Slaves can take over if master fails
- **Geographic Distribution**: Slaves in different regions
- **Backup**: Slaves serve as backups

**Disadvantages:**
- **Replication Lag**: Slaves may have stale data
- **Master Bottleneck**: All writes go through master
- **Failover Complexity**: Promoting slave to master

**Use Cases:**
- Read-heavy workloads
- When some staleness is acceptable
- Geographic distribution

#### 2. Master-Master Replication (Multi-Master)

**Theoretical Foundation:**
Based on active-active replication. Multiple masters can handle writes, requiring conflict resolution.

**Architecture:**
```
Write → [Master 1] ↔ [Master 2] ↔ [Master 3]
```

**Replication Process:**
1. **Write to Any Master**: Can write to any master
2. **Replicate to Others**: Changes replicated to all masters
3. **Conflict Resolution**: Resolve conflicts if same data written to multiple masters

**Conflict Resolution Strategies:**
- **Last Write Wins (LWW)**: Timestamp-based, last write wins
- **Vector Clocks**: Track causality, detect conflicts
- **Application-Level**: Application decides how to resolve
- **Partitioning**: Partition data so no conflicts (e.g., by user_id)

**Mathematical Model:**
- **Write Capacity**: N × Single_Master_Capacity (theoretically)
  - Reality: Replication overhead reduces this
- **Conflict Probability**: 
  - P(Conflict) = P(Concurrent_Writes_to_Same_Key)
  - Depends on access pattern

**Consistency Model:**
- **Eventual Consistency**: All masters eventually converge
- **Conflict Handling**: May need manual resolution
- **Causal Consistency**: Preserve cause-effect relationships

**Advantages:**
- **Write Scalability**: Multiple masters handle writes
- **Fault Tolerance**: Any master can fail
- **Geographic Distribution**: Masters in different regions

**Disadvantages:**
- **Conflict Resolution**: Complex conflict handling
- **Consistency**: Weaker consistency guarantees
- **Complexity**: More complex than master-slave

**Use Cases:**
- Write-heavy workloads
- Geographic distribution
- When conflicts are rare or acceptable

#### 3. Sharding (Horizontal Partitioning)

**Theoretical Foundation:**
Sharding is based on data partitioning theory, hash functions, and distributed database principles. It's the primary technique for horizontal scaling.

**Definition**: Partition data across multiple databases (shards) based on a shard key.

**Architecture:**
```
Shard 1: Users 0-999 (hash(user_id) % 4 = 0)
Shard 2: Users 1000-1999 (hash(user_id) % 4 = 1)
Shard 3: Users 2000-2999 (hash(user_id) % 4 = 2)
Shard 4: Users 3000-3999 (hash(user_id) % 4 = 3)
```

**Sharding Strategies:**

##### Range-Based Sharding
- **Partition by Value Ranges**
  - Example: Users A-F in shard 1, G-M in shard 2
- **Pros**: Simple, good for range queries
- **Cons**: Uneven distribution, hot spots

##### Hash-Based Sharding
- **Partition by Hash Function**
  - Example: hash(user_id) % num_shards
- **Pros**: Even distribution
- **Cons**: Difficult to change shard count, no range queries

**Mathematical Model:**
- **Distribution**: 
  - With good hash function, each shard gets ~1/N of data
  - Variance depends on hash function quality
- **Query Routing**: 
  - O(1) for single-key queries (hash lookup)
  - O(N) for cross-shard queries (query all shards)

**Sharding Challenges:**
- **Cross-Shard Queries**: Difficult to query across shards
  - Solution: Denormalize, or query all shards and merge
- **Rebalancing**: Moving data when adding/removing shards
  - Solution: Consistent hashing (only remap K/N keys)
- **Transaction Support**: ACID transactions across shards are complex
  - Solution: Two-phase commit (2PC), or accept weaker guarantees
- **Hot Spots**: Some shards may have more load
  - Solution: Better shard key selection, rebalancing

**Consistent Hashing:**
- **Problem**: Adding/removing shards requires rehashing all keys
- **Solution**: Hash ring, only remap keys near changed shard
- **Mathematical Model**: 
  - Keys and shards mapped to ring (0 to 2^m-1)
  - Key assigned to first shard clockwise
  - Adding shard: Only remap keys between previous and new shard

**Use Cases:**
- Very large datasets
- Need for horizontal scaling
- When single database can't handle load

### Database Indexing
```sql
-- Single column index
CREATE INDEX idx_email ON users(email);

-- Composite index
CREATE INDEX idx_name_email ON users(name, email);

-- Unique index
CREATE UNIQUE INDEX idx_username ON users(username);
```

### Database Partitioning

#### Horizontal Partitioning (Sharding)
```sql
-- Partition by user_id
CREATE TABLE users_0 PARTITION OF users
  FOR VALUES FROM (0) TO (1000);

CREATE TABLE users_1 PARTITION OF users
  FOR VALUES FROM (1000) TO (2000);
```

#### Vertical Partitioning
```sql
-- Split table
CREATE TABLE users_basic (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100)
);

CREATE TABLE users_profile (
  user_id INT PRIMARY KEY,
  bio TEXT,
  avatar_url VARCHAR(255)
);
```

### Database Consistency Models

**Theoretical Foundation:**
Consistency models define guarantees about when updates become visible. They're fundamental to distributed systems theory and are formalized using mathematical models of system behavior.

#### Strong Consistency

**Theoretical Foundation:**
Strong consistency ensures all nodes see the same data simultaneously. It's based on linearizability and sequential consistency models.

**Definition**: All replicas are updated immediately and synchronously. All reads return the latest written value.

**Mathematical Model:**
- **Linearizability**: All operations appear atomic and in some total order
  - For any two operations, one appears to happen before the other
  - Real-time ordering preserved
- **Sequential Consistency**: Operations appear in some sequential order consistent with program order
  - Weaker than linearizability (no real-time requirement)

**Implementation Mechanisms:**
1. **Two-Phase Commit (2PC)**
   - Phase 1: Coordinator asks all participants to prepare
   - Phase 2: If all prepared, coordinator commits; otherwise aborts
   - **Problem**: Blocking if coordinator fails
   - **Mathematical Model**: 
     - Latency = 2 × Network_Round_Trip + Processing_Time
     - Availability = P(All_Nodes_Available)

2. **Quorum-Based Reads/Writes**
   - Write to majority (W > N/2)
   - Read from majority (R > N/2)
   - Ensure R + W > N for consistency
   - **Mathematical Model**: 
     - Can tolerate (N-1)/2 failures
     - Read/Write latency = Majority_Response_Time

3. **Paxos/Raft Consensus**
   - Distributed consensus algorithms
   - Ensure all nodes agree on same value
   - **Mathematical Model**: 
     - Requires majority to agree
     - Can tolerate minority failures

**Trade-offs:**
- **Pros**: Always correct data, simple to reason about
- **Cons**: Higher latency, lower availability, requires coordination

**Use Cases:**
- Financial transactions
- Critical data
- When correctness is paramount

#### Eventual Consistency

**Theoretical Foundation:**
Eventual consistency is based on the BASE principle (Basically Available, Soft state, Eventual consistency) and is fundamental to many distributed systems.

**Definition**: System will eventually converge to consistent state. No guarantees about when.

**Mathematical Model:**
- **Convergence Time**: Time until all replicas agree
  - Depends on: Replication lag, network conditions, conflict resolution
  - Typical: Seconds to minutes
- **Staleness Bound**: Maximum time data can be stale
  - Depends on replication frequency
  - May be unbounded

**Consistency Variants:**
1. **Causal Consistency**
   - Preserves cause-effect relationships
   - If A happens before B, all nodes see A before B
   - **Mathematical Model**: Vector clocks track causality

2. **Session Consistency**
   - User's session sees consistent view
   - Different users may see different states
   - **Use Case**: User-specific data

3. **Monotonic Read Consistency**
   - User never sees older data after seeing newer data
   - **Use Case**: Timeline views

**Implementation:**
- **Asynchronous Replication**: Replicate in background
- **Conflict Resolution**: Last-write-wins, application-level, CRDTs
- **Vector Clocks**: Track causality for conflict detection

**Trade-offs:**
- **Pros**: High availability, better performance, geographic distribution
- **Cons**: May read stale data, complex conflict resolution

**Use Cases:**
- Social media feeds
- DNS
- CDN content
- Analytics systems

#### CAP Theorem (Brewer's Theorem)

**Theoretical Foundation:**
CAP theorem is a fundamental result in distributed systems theory, proven by Gilbert and Lynch (2002). It formalizes trade-offs in distributed systems.

**Formal Statement:**
In a distributed system, it's impossible to simultaneously guarantee all three:
- **Consistency (C)**: All nodes see the same data simultaneously
- **Availability (A)**: System remains operational (responds to requests)
- **Partition Tolerance (P)**: System works despite network failures (partitions)

**Proof Intuition:**
1. **Network Partition**: Network splits into two groups that can't communicate
2. **If we choose Availability**: 
   - Both groups must respond to requests
   - They can't communicate to ensure consistency
   - Result: Inconsistent responses (sacrifice Consistency)
3. **If we choose Consistency**: 
   - Both groups must return same data
   - They can't communicate to synchronize
   - Result: One group must block (sacrifice Availability)
4. **Partition Tolerance is Required**: 
   - In distributed systems, networks can and will fail
   - Must handle partitions

**Formal Proof (Gilbert & Lynch, 2002):**
- Consider system with two nodes, network partition
- If both nodes must respond (Availability) and be consistent:
  - Node 1 writes value v1
  - Node 2 must have v1 (consistency)
  - But partition prevents communication
  - Contradiction: Can't have both

**CAP Trade-offs:**

##### CP (Consistency + Partition Tolerance)
- **Sacrifice**: Availability
- **Behavior**: During partition, system blocks or returns errors
- **Examples**: 
  - Traditional databases (PostgreSQL, MySQL with replication)
  - Distributed locks
  - Financial systems
- **Use Case**: When consistency is critical

##### AP (Availability + Partition Tolerance)
- **Sacrifice**: Consistency (eventual consistency)
- **Behavior**: System continues operating, may return stale data
- **Examples**: 
  - DNS
  - CDN
  - NoSQL databases (Cassandra, DynamoDB, CouchDB)
  - Social media feeds
- **Use Case**: When availability is critical

##### CA (Consistency + Availability)
- **Sacrifice**: Partition tolerance
- **Behavior**: Only works when no network partitions
- **Reality**: Not possible in true distributed system
- **Examples**: Single-node systems, local databases
- **Note**: Some systems claim CA but actually choose CP or AP during partitions

**Real-World Systems:**
- **Most systems choose AP**: High availability with eventual consistency
- **Strong consistency when needed**: Use CP systems for critical operations
- **Hybrid approaches**: Use both AP and CP systems in same architecture

**CAP Theorem Criticisms:**
- **Oversimplification**: Real systems have more nuanced trade-offs
- **Consistency is a spectrum**: Not binary (strong vs eventual)
- **Partitions are rare**: In practice, may optimize for normal case
- **PACELC Extension**: 
  - If Partition: choose Availability or Consistency (CAP)
  - Else: choose Latency or Consistency (PACELC)

**Practical Implications:**
1. **Design for normal case**: Optimize for no partitions
2. **Degrade gracefully**: During partitions, choose AP or CP based on use case
3. **Use appropriate consistency**: Not everything needs strong consistency
4. **Layer consistency**: Different parts of system can have different guarantees

---

## Distributed Systems

### What are Distributed Systems?

**Theoretical Foundation:**
Distributed systems theory is a fundamental area of computer science, combining concepts from networking, concurrency, fault tolerance, and algorithms. It addresses the challenges of building systems that span multiple machines.

**Definition**: A distributed system is a collection of independent computers that appear to users as a single coherent system. Components are located on different networked computers and coordinate their actions by passing messages.

**Key Characteristics:**
1. **Concurrency**: Multiple components executing simultaneously
   - **Theoretical Model**: Concurrent processes, threads, or nodes
   - **Challenges**: Race conditions, deadlocks, livelocks
   - **Solutions**: Locks, transactions, message passing

2. **No Global Clock**: No single source of time
   - **Problem**: Different nodes have different clocks (clock skew)
   - **Theoretical Model**: Partial ordering of events (happens-before relation)
   - **Solutions**: Logical clocks (Lamport, Vector), NTP synchronization

3. **Independent Failures**: Components fail independently
   - **Failure Models**: Crash, omission, Byzantine
   - **Theoretical Model**: Failure probability P(failure)
   - **System Reliability**: R_system = (1 - P(failure))^N for N components

4. **Message Passing**: Communication via messages
   - **Communication Models**: Synchronous, asynchronous
   - **Message Ordering**: FIFO, causal, total order
   - **Network Assumptions**: Reliable, unreliable, ordered, unordered

**Theoretical Models:**

#### System Model
- **Synchronous System**: 
  - Bounded message delay
  - Bounded processing time
  - Bounded clock drift
- **Asynchronous System**: 
  - No bounds on delays
  - More realistic but harder to reason about

#### Failure Model
- **Crash Failure**: Component stops (simplest)
- **Omission Failure**: Fails to send/receive messages
- **Byzantine Failure**: Component behaves arbitrarily (most difficult)

#### Communication Model
- **Reliable**: Messages eventually delivered
- **Unreliable**: Messages may be lost
- **Ordered**: Messages delivered in order
- **Unordered**: No ordering guarantees

### Distributed Systems Challenges

**Theoretical Foundation:**
These challenges arise from fundamental limitations of distributed systems and are studied in distributed algorithms and systems theory.

#### 1. Network Partitions

**Definition**: Network splits into disconnected groups.

**Theoretical Model:**
- **Graph Theory**: Network as graph G = (V, E)
- **Partition**: Graph splits into disconnected components
- **CAP Theorem**: Must choose between consistency and availability

**Handling Strategies:**
- **Detect Partition**: Heartbeats, timeouts
- **Choose Strategy**: AP (continue) or CP (block)
- **Merge After Partition**: Resolve conflicts, merge state

#### 2. Clock Skew

**Definition**: Different nodes have different clock times.

**Theoretical Model:**
- **Physical Clocks**: Real time (UTC)
  - Clock drift: Clocks drift apart over time
  - Typical drift: 1-10ms per second
- **Logical Clocks**: Order events without real time
  - Lamport clocks: Scalar timestamp
  - Vector clocks: Vector of timestamps (captures causality)

**Solutions:**
- **NTP (Network Time Protocol)**: Synchronize clocks
- **Logical Clocks**: Order events without real time
- **Hybrid Logical Clocks**: Combine physical and logical

#### 3. Split-Brain

**Definition**: Multiple nodes think they're the leader.

**Theoretical Model:**
- **Leader Election**: Only one leader should exist
- **Problem**: Network partition causes multiple leaders
- **Solution**: Quorum-based election, fencing

**Prevention:**
- **Quorum**: Require majority to elect leader
- **Fencing**: Prevent old leader from making changes
- **Lease**: Time-limited leadership

#### 4. Consensus

**Definition**: All nodes agree on same value.

**Theoretical Foundation:**
Consensus is fundamental to distributed systems. FLP theorem (Fischer, Lynch, Patterson, 1985) proves consensus is impossible in asynchronous systems with even one failure.

**FLP Impossibility:**
- **Theorem**: In asynchronous system with one crash failure, consensus is impossible
- **Proof**: By contradiction - any algorithm can be delayed indefinitely
- **Implication**: Must use timeouts or failure detectors

**Consensus Algorithms:**
1. **Paxos**: 
   - Proposed by Lamport (1998)
   - Requires majority
   - Handles crash failures
   - **Phases**: Prepare, Accept

2. **Raft**: 
   - Simpler than Paxos
   - Leader-based
   - **Phases**: Leader election, Log replication

3. **PBFT (Practical Byzantine Fault Tolerance)**: 
   - Handles Byzantine failures
   - Requires 3f+1 nodes for f failures

**Mathematical Model:**
- **Quorum**: Majority (N/2 + 1) of N nodes
- **Fault Tolerance**: Can tolerate (N-1)/2 failures
- **Latency**: Requires majority responses

### Distributed System Patterns

#### 1. Leader Election
```javascript
// Using ZooKeeper
const zookeeper = require('node-zookeeper-client');

function electLeader() {
  const client = zookeeper.createClient('localhost:2181');
  
  client.create('/election/leader', Buffer.from(process.pid.toString()), 
    zookeeper.CreateMode.EPHEMERAL,
    (err, path) => {
      if (err) {
        // Another node is leader
        watchForLeader();
      } else {
        // This node is leader
        becomeLeader();
      }
    }
  );
}
```

#### 2. Distributed Locking
```javascript
// Using Redis
const redis = require('redis');
const client = redis.createClient();

async function acquireLock(lockKey, timeout = 5000) {
  const lockValue = Date.now().toString();
  const acquired = await client.set(lockKey, lockValue, {
    PX: timeout,
    NX: true
  });
  
  if (acquired) {
    return lockValue;
  }
  return null;
}

async function releaseLock(lockKey, lockValue) {
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `;
  await client.eval(script, 1, lockKey, lockValue);
}
```

#### 3. Distributed Transactions
```javascript
// Two-Phase Commit
class TransactionCoordinator {
  async commit(participants) {
    // Phase 1: Prepare
    const prepared = await Promise.all(
      participants.map(p => p.prepare())
    );
    
    if (prepared.every(p => p.success)) {
      // Phase 2: Commit
      await Promise.all(
        participants.map(p => p.commit())
      );
    } else {
      // Phase 2: Abort
      await Promise.all(
        participants.map(p => p.abort())
      );
    }
  }
}
```

### Consensus Algorithms

#### Raft
```
Leader Election → Log Replication → Safety
```

#### Paxos
```
Proposer → Acceptor → Learner
```

### Distributed System Challenges

#### 1. Network Partitions
```
[Node A] [Node B] | [Node C] [Node D]
   Network Split
```

#### 2. Clock Skew
```
Node 1: 10:00:00
Node 2: 10:00:05 (5 seconds ahead)
```

#### 3. Split-Brain
```
Two nodes both think they're the leader
```

---

## Microservices

### What are Microservices?

**Theoretical Foundation:**
Microservices architecture is based on principles of modularity, service-oriented architecture (SOA), and distributed systems. It applies concepts from software engineering (separation of concerns, single responsibility) to distributed systems.

**Definition**: Architectural approach where application is built as a collection of small, independent services that communicate over well-defined APIs. Each service is independently deployable and scalable.

**Core Principles:**
1. **Single Responsibility**: Each service does one thing well
   - **Theoretical Basis**: Separation of concerns, modularity
   - **Benefit**: Easier to understand, test, and maintain

2. **Independence**: Services are independently deployable
   - **Theoretical Basis**: Loose coupling, high cohesion
   - **Benefit**: Independent development and deployment

3. **Decentralization**: No central database or coordination
   - **Theoretical Basis**: Distributed systems principles
   - **Benefit**: Better scalability, fault isolation

4. **Failure Isolation**: Service failures don't cascade
   - **Theoretical Basis**: Fault tolerance, circuit breakers
   - **Benefit**: Better resilience

**Mathematical Model:**
- **Service Count**: N services
- **Communication Complexity**: O(N²) potential connections
  - Mitigated by: API Gateway, service mesh
- **Deployment Complexity**: N independent deployments
- **Testing Complexity**: Need to test N services + interactions

### Microservices vs Monolith

**Theoretical Foundation:**
The choice between microservices and monolith represents a fundamental trade-off in software architecture, balancing complexity, scalability, and development velocity.

#### Monolith

**Definition**: Single application containing all functionality.

**Architecture:**
```
┌─────────────────────┐
│   Single Application│
│  - User Service     │
│  - Order Service    │
│  - Payment Service  │
└─────────────────────┘
```

**Theoretical Model:**
- **Complexity**: O(1) deployment, O(N) code complexity
- **Communication**: In-process calls (very fast, ~nanoseconds)
- **Consistency**: ACID transactions across all components
- **Scaling**: Scale entire application together

**Advantages:**
- **Simplicity**: Single codebase, single deployment
- **Performance**: In-process calls, no network overhead
- **Transactions**: ACID across all components
- **Development**: Easier for small teams

**Disadvantages:**
- **Scalability**: Must scale entire application
- **Technology Lock-in**: Single technology stack
- **Deployment**: All-or-nothing deployment
- **Fault Isolation**: One component failure affects all

**When to Use:**
- Small to medium applications
- Small teams
- Simple requirements
- Performance critical

#### Microservices

**Definition**: Application split into independent services.

**Architecture:**
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│   User   │  │  Order   │  │ Payment  │
│ Service  │  │ Service  │  │ Service  │
└──────────┘  └──────────┘  └──────────┘
      ↓            ↓            ↓
  [Database]  [Database]  [Database]
```

**Theoretical Model:**
- **Complexity**: O(N) deployments, O(N²) potential interactions
- **Communication**: Network calls (milliseconds, 1000x slower)
- **Consistency**: Eventual consistency, distributed transactions complex
- **Scaling**: Scale services independently

**Advantages:**
- **Scalability**: Scale services independently
- **Technology Diversity**: Different tech stacks per service
- **Deployment**: Independent deployments
- **Fault Isolation**: Service failures isolated
- **Team Autonomy**: Teams work independently

**Disadvantages:**
- **Complexity**: More moving parts, network calls
- **Performance**: Network latency, serialization overhead
- **Transactions**: Distributed transactions complex
- **Testing**: Need to test service interactions
- **Operational Overhead**: More services to monitor

**When to Use:**
- Large applications
- Multiple teams
- Different scaling requirements
- Need for technology diversity

**Theoretical Trade-offs:**

**Communication Overhead:**
- Monolith: In-process call ~100ns
- Microservices: Network call ~1-10ms
- **Overhead**: 10,000-100,000x slower

**Consistency:**
- Monolith: ACID transactions (strong consistency)
- Microservices: Eventual consistency or complex 2PC

**Complexity:**
- Monolith: O(N) code complexity
- Microservices: O(N²) interaction complexity

**Conway's Law:**
- "Organizations design systems that mirror their communication structure"
- Microservices allow teams to work independently
- Monoliths require more coordination

### Microservices Communication

#### 1. Synchronous (HTTP/REST)
```javascript
// Service A calls Service B
const response = await fetch('http://service-b/api/users');
const users = await response.json();
```

#### 2. Asynchronous (Message Queue)
```javascript
// Service A publishes event
await messageQueue.publish('user.created', { userId: 123 });

// Service B subscribes
messageQueue.subscribe('user.created', async (event) => {
  await processUser(event.userId);
});
```

### Service Discovery
```javascript
// Service Registry
class ServiceRegistry {
  register(serviceName, address) {
    registry[serviceName] = address;
  }
  
  discover(serviceName) {
    return registry[serviceName];
  }
}

// Client-side discovery
const serviceAddress = serviceRegistry.discover('user-service');
const response = await fetch(`http://${serviceAddress}/api/users`);
```

### API Gateway
```
Client → API Gateway → [Service 1] [Service 2] [Service 3]
```

**Functions:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Load balancing
- Request/Response transformation

### Circuit Breaker
```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }
  
  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }
  
  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.lastFailure = Date.now();
    }
  }
}
```

---

## Message Queues

### What are Message Queues?
Asynchronous communication mechanism between services.

### Message Queue Patterns

#### 1. Point-to-Point
```
Producer → Queue → Consumer
```

#### 2. Publish-Subscribe
```
Publisher → Topic → [Subscriber 1] [Subscriber 2] [Subscriber 3]
```

### Message Queue Benefits
- **Decoupling**: Services don't need to know about each other
- **Reliability**: Messages persisted until processed
- **Scalability**: Multiple consumers can process messages
- **Asynchronous**: Non-blocking communication

### Popular Message Queues

#### RabbitMQ
```javascript
const amqp = require('amqplib');

// Producer
const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();
await channel.assertQueue('tasks');
channel.sendToQueue('tasks', Buffer.from('task data'));

// Consumer
const connection = await amqp.connect('amqp://localhost');
const channel = await connection.createChannel();
await channel.assertQueue('tasks');
channel.consume('tasks', (msg) => {
  console.log(msg.content.toString());
  channel.ack(msg);
});
```

#### Apache Kafka
```javascript
const kafka = require('kafkajs');

const client = kafka({
  brokers: ['localhost:9092']
});

// Producer
const producer = client.producer();
await producer.send({
  topic: 'events',
  messages: [{ value: 'event data' }]
});

// Consumer
const consumer = client.consumer({ groupId: 'my-group' });
await consumer.subscribe({ topic: 'events' });
await consumer.run({
  eachMessage: async ({ message }) => {
    console.log(message.value.toString());
  }
});
```

### Message Queue Patterns

#### 1. Work Queue
```
Producer → Queue → [Worker 1] [Worker 2] [Worker 3]
```

#### 2. Fan-Out
```
Producer → Exchange → [Queue 1] [Queue 2] [Queue 3]
```

#### 3. Routing
```
Producer → Exchange (routing key) → [Queue 1] [Queue 2]
```

---

## API Design

### RESTful API Principles
- **Stateless**: Each request contains all information needed
- **Resource-Based**: URLs represent resources
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- **Status Codes**: 200, 201, 400, 404, 500, etc.

### RESTful API Design
```javascript
// Resources
GET    /api/users           // List users
GET    /api/users/:id       // Get user
POST   /api/users           // Create user
PUT    /api/users/:id       // Update user
PATCH  /api/users/:id       // Partial update
DELETE /api/users/:id       // Delete user

// Nested resources
GET    /api/users/:id/posts // Get user's posts
POST   /api/users/:id/posts // Create post for user
```

### API Versioning
```javascript
// URL versioning
GET /api/v1/users
GET /api/v2/users

// Header versioning
GET /api/users
Headers: Accept: application/vnd.api.v1+json

// Query parameter
GET /api/users?version=1
```

### API Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests'
});

app.use('/api/', limiter);
```

### API Pagination
```javascript
// Offset-based
GET /api/users?page=1&limit=20

// Cursor-based
GET /api/users?cursor=abc123&limit=20

// Response
{
  "data": [...],
  "pagination": {
    "next": "/api/users?cursor=xyz789",
    "prev": "/api/users?cursor=abc123"
  }
}
```

### API Filtering & Sorting
```javascript
// Filtering
GET /api/users?status=active&role=admin

// Sorting
GET /api/users?sort=name&order=asc

// Field selection
GET /api/users?fields=id,name,email
```

---

## Security

### Authentication & Authorization

#### JWT (JSON Web Tokens)
```javascript
const jwt = require('jsonwebtoken');

// Generate token
const token = jwt.sign(
  { userId: 123, role: 'admin' },
  'secret-key',
  { expiresIn: '1h' }
);

// Verify token
const decoded = jwt.verify(token, 'secret-key');
```

#### OAuth 2.0
```
Client → Authorization Server → Resource Server
```

### Security Best Practices

#### 1. Input Validation
```javascript
const validator = require('validator');

function validateInput(input) {
  if (!validator.isEmail(input.email)) {
    throw new Error('Invalid email');
  }
  if (!validator.isLength(input.password, { min: 8 })) {
    throw new Error('Password too short');
  }
}
```

#### 2. SQL Injection Prevention
```javascript
// Bad
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Good
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

#### 3. XSS Prevention
```javascript
const xss = require('xss');

const clean = xss(userInput);
```

#### 4. CSRF Protection
```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);
```

#### 5. HTTPS
```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

https.createServer(options, app).listen(443);
```

### Security Headers
```javascript
app.use(helmet());
// Sets various security headers:
// - X-Content-Type-Options
// - X-Frame-Options
// - X-XSS-Protection
// - Strict-Transport-Security
```

---

## Monitoring & Observability

### Three Pillars of Observability

#### 1. Metrics
```javascript
// Prometheus metrics
const prometheus = require('prom-client');

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status']
});

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration.observe(
      { method: req.method, route: req.route.path, status: res.statusCode },
      duration
    );
  });
  next();
});
```

#### 2. Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

logger.info('User logged in', { userId: 123 });
logger.error('Database connection failed', { error: err.message });
```

#### 3. Tracing
```javascript
// OpenTelemetry
const { trace } = require('@opentelemetry/api');

const tracer = trace.getTracer('my-service');

function processOrder(orderId) {
  const span = tracer.startSpan('processOrder');
  span.setAttribute('order.id', orderId);
  
  try {
    // Process order
    span.setStatus({ code: 1 }); // OK
  } catch (error) {
    span.setStatus({ code: 2, message: error.message }); // ERROR
    throw error;
  } finally {
    span.end();
  }
}
```

### Health Checks
```javascript
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: Date.now(),
    checks: {
      database: await checkDatabase(),
      cache: await checkCache(),
      externalAPI: await checkExternalAPI()
    }
  };
  
  const isHealthy = Object.values(health.checks).every(check => check.status === 'up');
  res.status(isHealthy ? 200 : 503).json(health);
});
```

### Alerting
```javascript
// Alert on high error rate
if (errorRate > 0.05) {
  sendAlert({
    severity: 'critical',
    message: 'High error rate detected',
    value: errorRate
  });
}
```

---

## Performance Optimization

### Database Optimization

#### 1. Indexing
```sql
-- Create index
CREATE INDEX idx_email ON users(email);

-- Composite index
CREATE INDEX idx_name_email ON users(name, email);

-- Analyze query
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

#### 2. Query Optimization
```sql
-- Bad: Full table scan
SELECT * FROM users WHERE name LIKE '%john%';

-- Good: Use index
SELECT * FROM users WHERE name LIKE 'john%';

-- Bad: N+1 queries
SELECT * FROM users;
-- Then for each user: SELECT * FROM posts WHERE user_id = ?

-- Good: Join
SELECT u.*, p.* FROM users u
LEFT JOIN posts p ON u.id = p.user_id;
```

#### 3. Connection Pooling
```javascript
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

### Caching Strategies

#### 1. Application-Level Caching
```javascript
const cache = new Map();

function getUser(userId) {
  if (cache.has(userId)) {
    return cache.get(userId);
  }
  const user = database.getUser(userId);
  cache.set(userId, user);
  return user;
}
```

#### 2. CDN Caching
```
User → CDN Edge (cached) → Origin Server
```

#### 3. Database Query Caching
```javascript
const queryCache = new Map();

function executeQuery(sql, params) {
  const cacheKey = `${sql}:${JSON.stringify(params)}`;
  if (queryCache.has(cacheKey)) {
    return queryCache.get(cacheKey);
  }
  const result = database.query(sql, params);
  queryCache.set(cacheKey, result);
  return result;
}
```

### Asynchronous Processing
```javascript
// Synchronous (blocking)
app.post('/process', (req, res) => {
  const result = heavyComputation(req.body);
  res.json(result);
});

// Asynchronous (non-blocking)
app.post('/process', (req, res) => {
  queue.add('heavy-computation', req.body);
  res.json({ status: 'processing', jobId: job.id });
});
```

---

## Design Patterns

### 1. Singleton Pattern
```javascript
class DatabaseConnection {
  constructor() {
    if (DatabaseConnection.instance) {
      return DatabaseConnection.instance;
    }
    DatabaseConnection.instance = this;
    this.connection = connect();
  }
}
```

### 2. Factory Pattern
```javascript
class DatabaseFactory {
  create(type) {
    switch (type) {
      case 'mysql':
        return new MySQLConnection();
      case 'postgres':
        return new PostgresConnection();
      default:
        throw new Error('Unknown database type');
    }
  }
}
```

### 3. Observer Pattern
```javascript
class EventEmitter {
  constructor() {
    this.listeners = {};
  }
  
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }
  
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }
}
```

### 4. Strategy Pattern
```javascript
class PaymentProcessor {
  constructor(strategy) {
    this.strategy = strategy;
  }
  
  process(amount) {
    return this.strategy.pay(amount);
  }
}

class CreditCardStrategy {
  pay(amount) {
    // Process credit card payment
  }
}

class PayPalStrategy {
  pay(amount) {
    // Process PayPal payment
  }
}
```

---

## Common System Designs

### 1. URL Shortener (TinyURL)

#### Requirements
- Shorten long URLs
- Redirect to original URL
- Handle 100M URLs/day
- 5-year retention

#### Design
```
User → API → Short URL Generator → Database
User → Short URL → Redirect Service → Original URL
```

#### Key Components
- **Hash Function**: Generate short code (base62 encoding)
- **Database**: Store mapping (short URL → original URL)
- **Cache**: Store frequently accessed URLs
- **Load Balancer**: Distribute traffic

### 2. Twitter-like System

#### Requirements
- Post tweets (140 characters)
- Follow/unfollow users
- Timeline (home feed)
- 500M users, 200M tweets/day

#### Design
```
User → API → [Tweet Service] [User Service] [Timeline Service]
                ↓                ↓                ↓
            [Database]      [Database]      [Cache]
```

#### Key Components
- **Fan-out**: Push tweets to followers' timelines
- **Timeline Generation**: Merge user's tweets + following tweets
- **Caching**: Cache user timelines
- **Database Sharding**: Shard by user_id

### 3. Chat System

#### Requirements
- 1-on-1 messaging
- Group messaging
- Online status
- Message delivery status

#### Design
```
Client → WebSocket Server → Message Queue → [Service 1] [Service 2]
```

#### Key Components
- **WebSocket**: Real-time bidirectional communication
- **Message Queue**: Store messages
- **Presence Service**: Track online users
- **Notification Service**: Push notifications

### 4. Video Streaming (YouTube)

#### Requirements
- Upload videos
- Stream videos
- Search videos
- Recommendations

#### Design
```
Upload → Storage → Encoding → CDN
Stream → CDN → Client
```

#### Key Components
- **CDN**: Distribute video content
- **Encoding Service**: Convert videos to multiple formats
- **Storage**: Store video files
- **Recommendation Engine**: Suggest videos

---

## Best Practices

### 1. Design for Scale
- Start simple, scale as needed
- Use horizontal scaling
- Design stateless services
- Cache aggressively

### 2. Design for Failure
- Assume everything fails
- Implement circuit breakers
- Use retries with exponential backoff
- Have fallback mechanisms

### 3. Design for Performance
- Minimize latency
- Optimize database queries
- Use caching
- Implement async processing

### 4. Design for Security
- Authenticate and authorize
- Encrypt sensitive data
- Validate input
- Use HTTPS

### 5. Design for Maintainability
- Keep it simple
- Document your design
- Use standard patterns
- Write tests

---

## Interview Preparation

### System Design Interview Process

#### 1. Clarify Requirements (5-10 min)
- Functional requirements
- Non-functional requirements
- Scale requirements
- Constraints

#### 2. High-Level Design (10-15 min)
- Draw architecture diagram
- Identify major components
- Define APIs
- Data models

#### 3. Detailed Design (10-15 min)
- Database schema
- Algorithms
- Specific technologies
- Data flow

#### 4. Scale the Design (5-10 min)
- Identify bottlenecks
- Add caching
- Add load balancing
- Database sharding

### Common Interview Questions

1. **Design a URL shortener**
2. **Design Twitter**
3. **Design a chat system**
4. **Design a video streaming service**
5. **Design a web crawler**
6. **Design a distributed cache**
7. **Design a notification system**
8. **Design a rate limiter**
9. **Design a search engine**
10. **Design a payment system**

### Interview Tips

1. **Think Out Loud**: Explain your thought process
2. **Ask Questions**: Clarify requirements
3. **Start Simple**: Begin with basic design, then scale
4. **Consider Trade-offs**: Discuss pros and cons
5. **Be Flexible**: Adapt based on feedback

---

## Resources for Further Learning

1. **System Design Primer** - GitHub repository
2. **Designing Data-Intensive Applications** - Book by Martin Kleppmann
3. **High Scalability** - Blog on scalable systems
4. **AWS Architecture Center** - Reference architectures
5. **Google Cloud Architecture** - Best practices
6. **System Design Interview** - Book by Alex Xu
7. **Distributed Systems** - Course materials
8. **Microservices Patterns** - Book by Chris Richardson

---

## Theoretical Framework Summary

### Fundamental Theorems and Principles

**1. CAP Theorem (Brewer, 2000; Gilbert & Lynch, 2002)**
- **Statement**: Cannot have all three: Consistency, Availability, Partition tolerance
- **Implication**: Must choose trade-offs based on use case
- **Application**: Most systems choose AP (availability + partition tolerance)

**2. FLP Impossibility (Fischer, Lynch, Patterson, 1985)**
- **Statement**: Consensus impossible in asynchronous system with one failure
- **Implication**: Need timeouts or failure detectors
- **Application**: Consensus algorithms (Paxos, Raft) use timeouts

**3. Amdahl's Law (1967)**
- **Statement**: Speedup = 1 / (S + (1-S)/N)
- **Implication**: Sequential portion limits parallel speedup
- **Application**: Identify bottlenecks, optimize sequential code

**4. Little's Law (1961)**
- **Statement**: L = λ × W (L = items in system, λ = arrival rate, W = wait time)
- **Implication**: Relates throughput, latency, and concurrency
- **Application**: Capacity planning, performance analysis

**5. BASE Principle**
- **Statement**: Basically Available, Soft state, Eventual consistency
- **Implication**: Alternative to ACID for distributed systems
- **Application**: NoSQL databases, distributed caches

### Design Principles Hierarchy

```
System Goals
    ↓
Scalability ←→ Reliability ←→ Performance
    ↓              ↓              ↓
Horizontal    Fault          Caching
Scaling       Tolerance      Optimization
    ↓              ↓              ↓
Sharding      Redundancy     CDN
Load          Replication    Database
Balancing                    Indexing
```

### Mathematical Models

**Performance Models:**
- **Queueing Theory**: M/M/1, M/M/c queues
- **Response Time**: R = S / (1 - U) where U = utilization
- **Throughput**: X = U × S where S = service time

**Reliability Models:**
- **MTBF/MTTR**: Availability = MTBF / (MTBF + MTTR)
- **Redundancy**: R_system = 1 - (1 - R_component)^N
- **Series/Parallel**: Series decreases, parallel increases reliability

**Scalability Models:**
- **Amdahl's Law**: Limits of parallel speedup
- **Gustafson's Law**: Scaling with problem size
- **Karp-Flatt Metric**: Measures parallel overhead

### Design Decision Framework

**1. Requirements Analysis**
- Functional vs Non-functional
- Quantify: RPS, storage, latency requirements
- Identify constraints and assumptions

**2. Capacity Planning**
- Traffic estimation: Peak = Average × Peak_Factor
- Storage estimation: Current × Growth_Rate^Years
- Bandwidth: Request_Size × RPS × 8

**3. Architecture Selection**
- Monolith vs Microservices
- SQL vs NoSQL
- Synchronous vs Asynchronous

**4. Scaling Strategy**
- Horizontal vs Vertical
- Read replicas vs Sharding
- Caching strategy

**5. Consistency Model**
- Strong vs Eventual (CAP theorem)
- ACID vs BASE
- Transaction requirements

**6. Failure Handling**
- Redundancy strategy
- Failover mechanism
- Disaster recovery

### Common Patterns and Their Theory

**1. Caching Patterns**
- **Locality of Reference**: Temporal and spatial
- **Cache Performance**: EAT = H×Hit_Time + (1-H)×Miss_Time
- **Replacement Policies**: LRU, LFU, FIFO

**2. Load Balancing**
- **Algorithms**: Round robin, least connections, weighted
- **Queueing Theory**: Distribute load to minimize queue length
- **Health Checks**: Detect failures quickly

**3. Replication**
- **Master-Slave**: Read scalability, write bottleneck
- **Master-Master**: Write scalability, conflict resolution
- **Quorum**: R + W > N for consistency

**4. Sharding**
- **Hash-Based**: Even distribution, no range queries
- **Range-Based**: Range queries, uneven distribution
- **Consistent Hashing**: Minimal rehashing on changes

**5. Microservices**
- **Service Independence**: Loose coupling, high cohesion
- **Communication**: Network calls vs in-process
- **Complexity**: O(N²) interactions for N services

### Performance Optimization Theory

**1. Caching**
- **Hit Rate**: Critical for performance
- **Cache Size**: Larger cache → higher hit rate (diminishing returns)
- **TTL**: Balance freshness vs hit rate

**2. Database Optimization**
- **Indexing**: B-tree O(log n), Hash O(1) average
- **Query Optimization**: Cost-based, rule-based
- **Normalization**: Reduce redundancy, improve integrity

**3. Asynchronous Processing**
- **Non-Blocking**: Don't wait for slow operations
- **Message Queues**: Decouple producers and consumers
- **Event-Driven**: React to events, not poll

**4. CDN**
- **Geographic Distribution**: Reduce latency
- **Caching**: Store content at edge
- **Latency Reduction**: Distance reduction → latency reduction

### Reliability and Availability Theory

**1. Fault Models**
- **Crash**: Simplest, easiest to handle
- **Omission**: Network failures, message loss
- **Byzantine**: Arbitrary behavior, most difficult

**2. Redundancy**
- **Active**: All components run (fast failover)
- **Passive**: Backup activates on failure (slower)
- **N+1**: N needed, N+1 available

**3. Failure Detection**
- **Heartbeats**: Periodic "I'm alive" messages
- **Timeouts**: Detect missing heartbeats
- **Failure Detectors**: Unreliable but useful

**4. Availability Calculation**
- **Single Component**: A
- **Series**: A^N (decreases)
- **Parallel**: 1 - (1-A)^N (increases)

### Scalability Theory

**1. Horizontal Scaling**
- **Linear Scaling**: Ideal (rarely achieved)
- **Amdahl's Law**: Sequential portion limits speedup
- **Overhead**: Network, coordination, data distribution

**2. Vertical Scaling**
- **Hardware Limits**: Physical constraints
- **Cost Curve**: Exponential cost for linear performance
- **Single Point of Failure**: One machine

**3. Stateless Design**
- **Scalability**: Any server can handle any request
- **Load Balancing**: Easy to distribute
- **State Management**: Externalize state (database, cache)

### Consistency Theory

**1. Consistency Models**
- **Strong**: Linearizability, sequential consistency
- **Weak**: Eventual, causal, session consistency
- **Trade-offs**: Consistency vs Availability (CAP)

**2. CAP Theorem Applications**
- **CP Systems**: Financial, critical data
- **AP Systems**: Social media, CDN, DNS
- **Hybrid**: Use both in same system

**3. Transaction Models**
- **ACID**: Strong consistency, isolation
- **BASE**: Availability, eventual consistency
- **2PC**: Distributed transactions (blocking)

## Conclusion

This comprehensive guide covers system design from fundamentals to advanced topics, with deep theoretical foundations. Mastery comes through:

- **Theoretical Understanding**: Know the "why" behind design decisions
  - CAP theorem explains consistency-availability trade-offs
  - Queueing theory models system performance
  - Distributed systems theory addresses fundamental challenges

- **Practical Application**: Apply theory to real problems
  - Design systems based on requirements
  - Make informed trade-offs
  - Optimize for specific use cases

- **Continuous Learning**: 
  - Study well-designed systems
  - Learn from failures
  - Stay current with industry practices

- **Practice**: 
  - Design systems from scratch
  - Solve interview problems
  - Build real systems

**Remember**: Good system design balances multiple competing concerns:
- **Scalability** vs **Complexity**
- **Consistency** vs **Availability**
- **Performance** vs **Cost**
- **Simplicity** vs **Features**

The theoretical foundations provided in this guide give you the tools to make informed decisions and understand the trade-offs involved.

### Key Theoretical Takeaways

1. **CAP Theorem**: Fundamental constraint in distributed systems
2. **Amdahl's Law**: Limits of parallel speedup
3. **Little's Law**: Relates throughput, latency, concurrency
4. **Locality of Reference**: Basis for caching effectiveness
5. **Queueing Theory**: Models system behavior under load
6. **Consistency Models**: Trade-offs between correctness and performance
7. **Fault Tolerance**: Design for failure, not perfection
8. **Scalability Patterns**: Horizontal scaling, sharding, replication

### Final Thoughts

System design is both an art and a science. The theoretical foundations provide the science - the mathematical models, theorems, and principles that guide our decisions. The art comes from applying these principles creatively to solve real-world problems.

Keep learning, keep practicing, and keep designing. Every system you design teaches you something new. Every failure is a learning opportunity. Every success validates your understanding.

**Design with theory. Build with practice. Learn from both.**

