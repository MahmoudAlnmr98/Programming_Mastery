# System Design Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. Design a URL Shortener (TinyURL).

**Requirements:**
- Shorten long URLs
- Redirect to original URL
- Handle 100M URLs/day
- 5-year retention

**Answer:**
**High-Level Design:**
```
User → API → Short URL Generator → Database
User → Short URL → Redirect Service → Original URL
```

**Components:**
1. **API Server**: Handle requests
2. **Short URL Generator**: Base62 encoding, hash function
3. **Database**: Store mapping (short URL → original URL)
4. **Cache**: Store frequently accessed URLs (Redis)
5. **Load Balancer**: Distribute traffic

**Database Schema:**
```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY,
    short_url VARCHAR(10) UNIQUE,
    original_url TEXT,
    created_at TIMESTAMP,
    expires_at TIMESTAMP
);
```

**Algorithm:**
- Use counter or hash function
- Base62 encoding: [a-z, A-Z, 0-9]
- 6 characters = 62^6 = 56 billion URLs

### 2. Design a Chat System (WhatsApp/Messenger).

**Requirements:**
- 1-on-1 messaging
- Group messaging
- Online status
- Message delivery status

**Answer:**
**High-Level Design:**
```
Client → WebSocket Server → Message Queue → [Service 1] [Service 2]
```

**Components:**
1. **WebSocket Server**: Real-time bidirectional communication
2. **Message Queue**: Store messages (Kafka, RabbitMQ)
3. **Presence Service**: Track online users
4. **Notification Service**: Push notifications
5. **Database**: Store messages, users, groups

**Database Schema:**
```sql
CREATE TABLE messages (
    id BIGINT PRIMARY KEY,
    sender_id BIGINT,
    receiver_id BIGINT,
    group_id BIGINT,
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(100),
    status VARCHAR(20) -- online, offline, away
);
```

### 3. Design a Rate Limiter.

**Requirements:**
- Limit requests per user/IP
- 100 requests per minute
- Distributed system

**Answer:**
**Algorithms:**
1. **Token Bucket**: Tokens added at fixed rate, request consumes token
2. **Leaky Bucket**: Requests added to bucket, processed at fixed rate
3. **Fixed Window**: Count requests in time window
4. **Sliding Window**: Count requests in sliding time window

**Implementation:**
```javascript
// Redis-based rate limiter
function rateLimit(userId, limit, window) {
    const key = `rate_limit:${userId}`;
    const current = redis.incr(key);
    
    if (current === 1) {
        redis.expire(key, window);
    }
    
    return current <= limit;
}
```

### 4. Design a Web Crawler.

**Requirements:**
- Crawl web pages
- Respect robots.txt
- Handle billions of pages
- Avoid duplicates

**Answer:**
**Components:**
1. **URL Frontier**: Queue of URLs to crawl
2. **DNS Resolver**: Resolve domain names
3. **Downloader**: Download web pages
4. **Parser**: Extract links and content
5. **Deduplicator**: Check if URL already crawled
6. **Storage**: Store crawled content

**Algorithm:**
```
1. Add seed URLs to frontier
2. While frontier not empty:
   a. Get URL from frontier
   b. Check if already crawled (Bloom filter)
   c. Download page
   d. Parse and extract links
   e. Add new URLs to frontier
   f. Store content
```

### 5. Design a Distributed Cache.

**Requirements:**
- Store key-value pairs
- High availability
- Low latency
- Handle millions of requests

**Answer:**
**Design:**
- **Consistent Hashing**: Distribute keys across nodes
- **Replication**: Multiple copies for availability
- **Eviction Policy**: LRU, LFU, TTL
- **Sharding**: Partition data across nodes

**Architecture:**
```
Client → Load Balancer → [Cache Node 1] [Cache Node 2] [Cache Node 3]
                              ↓                ↓                ↓
                         [Replica 1]      [Replica 2]      [Replica 3]
```

---

## Intermediate Level

### 6. Design Twitter.

**Requirements:**
- Post tweets (280 characters)
- Follow/unfollow users
- Timeline (home feed)
- 500M users, 200M tweets/day

**Answer:**
**Components:**
1. **Tweet Service**: Create, store tweets
2. **User Service**: User management, follow/unfollow
3. **Timeline Service**: Generate user timelines
4. **Feed Generation**: Fan-out approach

**Feed Generation Strategies:**
- **Fan-out on Write**: Push tweets to followers' timelines
  - Write-heavy, fast reads
  - Problem: Popular users have many followers
  
- **Fan-out on Read**: Generate timeline on read
  - Read-heavy, slower reads
  - Problem: Slow for users with many followings

**Hybrid Approach:**
- Fan-out for users with < 1M followers
- Generate on read for popular users

**Database Schema:**
```sql
CREATE TABLE tweets (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    content VARCHAR(280),
    created_at TIMESTAMP
);

CREATE TABLE follows (
    follower_id BIGINT,
    followee_id BIGINT,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE TABLE timelines (
    user_id BIGINT,
    tweet_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at, tweet_id)
);
```

### 7. Design a Search Engine.

**Requirements:**
- Search web pages
- Rank results by relevance
- Handle billions of pages
- Fast response time

**Answer:**
**Components:**
1. **Crawler**: Crawl and index web pages
2. **Indexer**: Build inverted index
3. **Ranker**: Rank results (PageRank, TF-IDF)
4. **Query Processor**: Process search queries

**Inverted Index:**
```
"javascript" → [doc1, doc3, doc5]
"react" → [doc2, doc3, doc7]
```

**Ranking:**
- **TF-IDF**: Term frequency × Inverse document frequency
- **PageRank**: Link-based ranking
- **Relevance**: Keyword matching, freshness

### 8. Design a Notification System.

**Requirements:**
- Send notifications (email, SMS, push)
- Support multiple channels
- Handle millions of notifications
- Reliable delivery

**Answer:**
**Components:**
1. **Notification Service**: Create notifications
2. **Message Queue**: Queue notifications
3. **Channel Handlers**: Email, SMS, Push services
4. **Retry Mechanism**: Retry failed notifications
5. **Rate Limiter**: Limit per user/channel

**Architecture:**
```
Notification Service → Message Queue → [Email Handler] [SMS Handler] [Push Handler]
                                                          ↓              ↓
                                                    [Email Service] [SMS Service]
```

### 9. Design a Distributed File Storage (Dropbox).

**Requirements:**
- Store files
- Sync across devices
- Version history
- Handle large files

**Answer:**
**Components:**
1. **Upload Service**: Handle file uploads
2. **Storage Service**: Store file chunks
3. **Metadata Service**: Store file metadata
4. **Sync Service**: Sync files across devices
5. **Version Service**: Maintain file versions

**File Chunking:**
- Split large files into chunks
- Store chunks separately
- Deduplicate chunks

**Database Schema:**
```sql
CREATE TABLE files (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(255),
    path VARCHAR(500),
    size BIGINT,
    version INT,
    created_at TIMESTAMP
);

CREATE TABLE chunks (
    id BIGINT PRIMARY KEY,
    file_id BIGINT,
    chunk_index INT,
    chunk_hash VARCHAR(64),
    storage_location VARCHAR(255)
);
```

### 10. Design a Video Streaming Service (YouTube).

**Requirements:**
- Upload videos
- Stream videos
- Search videos
- Recommendations

**Answer:**
**Components:**
1. **Upload Service**: Handle video uploads
2. **Encoding Service**: Convert to multiple formats/resolutions
3. **CDN**: Distribute video content
4. **Metadata Service**: Store video metadata
5. **Recommendation Engine**: Suggest videos

**Video Processing:**
```
Upload → Storage → Encoding → [1080p, 720p, 480p, 360p] → CDN
```

**CDN Strategy:**
- Push popular videos to edge servers
- Pull on demand for less popular videos

---

## Advanced Level

### 11. Design a Distributed Lock Service.

**Requirements:**
- Acquire/release locks
- Handle failures
- Low latency
- High availability

**Answer:**
**Implementation Options:**
1. **Redis with SET NX**: Simple, but single point of failure
2. **ZooKeeper**: Consensus-based, reliable
3. **etcd**: Distributed key-value store

**Redis Implementation:**
```javascript
function acquireLock(lockKey, timeout) {
    const lockValue = Date.now().toString();
    const acquired = redis.set(lockKey, lockValue, 'PX', timeout, 'NX');
    
    if (acquired) {
        return lockValue;
    }
    return null;
}

function releaseLock(lockKey, lockValue) {
    const script = `
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
    `;
    return redis.eval(script, 1, lockKey, lockValue);
}
```

### 12. Design a Distributed Counter.

**Requirements:**
- Increment/decrement counter
- Handle high throughput
- Eventually consistent

**Answer:**
**Approaches:**
1. **Sharded Counter**: Partition across nodes
2. **CRDT (Conflict-free Replicated Data Type)**: Merge without conflicts
3. **Approximate Counter**: Probabilistic counting (HyperLogLog)

**Sharded Counter:**
```
Counter = Counter_1 + Counter_2 + ... + Counter_N
```

### 13. Design a Real-time Analytics System.

**Requirements:**
- Track events in real-time
- Aggregate metrics
- Handle millions of events/second
- Low latency queries

**Answer:**
**Components:**
1. **Event Collector**: Collect events
2. **Stream Processor**: Process events (Kafka Streams, Flink)
3. **Time-Series Database**: Store metrics (InfluxDB, TimescaleDB)
4. **Query Service**: Serve queries

**Architecture:**
```
Events → Kafka → Stream Processor → Time-Series DB → Query Service
```

### 14. Design a Distributed Task Scheduler.

**Requirements:**
- Schedule tasks
- Execute tasks reliably
- Handle failures
- Support cron expressions

**Answer:**
**Components:**
1. **Scheduler**: Schedule tasks
2. **Worker Pool**: Execute tasks
3. **Task Queue**: Queue tasks
4. **Result Store**: Store task results

**Implementation:**
- Use distributed lock for leader election
- Leader schedules tasks
- Workers pull tasks from queue
- Retry failed tasks

### 15. Design a Multi-Tenant SaaS System.

**Requirements:**
- Support multiple tenants
- Data isolation
- Customizable per tenant
- Scalable

**Answer:**
**Data Isolation Strategies:**
1. **Separate Database**: Each tenant has own database
2. **Shared Database, Separate Schema**: Each tenant has own schema
3. **Shared Database, Shared Schema**: Tenant ID in each table

**Architecture:**
```
Request → Tenant Resolver → [Tenant 1 DB] [Tenant 2 DB] [Tenant 3 DB]
```

### 16. Design a Payment Processing System.

**Requirements:**
- Process payments
- Handle failures
- Idempotent operations
- Fraud detection
- Refunds

**Answer:**
**Components:**
1. **Payment Gateway**: External payment processor
2. **Payment Service**: Business logic
3. **Transaction Service**: Track transactions
4. **Fraud Detection**: Analyze for fraud
5. **Notification Service**: Send receipts

**Flow:**
```
User → Payment Service → Fraud Check → Payment Gateway
                        ↓
                   Transaction DB
                        ↓
                   Notification Service
```

**Idempotency:**
- Use idempotency keys
- Check before processing
- Return same result for duplicate requests

### 17. Design a Content Delivery Network (CDN).

**Requirements:**
- Distribute content globally
- Low latency
- High availability
- Cache management

**Answer:**
**Architecture:**
```
Origin Server → Edge Servers (Global) → Users
```

**Strategies:**
- **Push CDN**: Pre-populate edge servers
- **Pull CDN**: Cache on demand
- **Hybrid**: Push popular, pull others

**Cache Invalidation:**
- TTL-based expiration
- Manual invalidation
- Version-based URLs

### 18. Design a Distributed Logging System.

**Requirements:**
- Collect logs from services
- Store logs
- Search logs
- Real-time monitoring

**Answer:**
**Components:**
1. **Log Collectors**: Collect from services
2. **Message Queue**: Buffer logs (Kafka)
3. **Storage**: Time-series database
4. **Search Engine**: Elasticsearch
5. **Dashboard**: Visualization

**Architecture:**
```
Services → Log Collectors → Kafka → [Elasticsearch] [Time-Series DB]
                                              ↓
                                         Dashboard
```

### 19. Design a Recommendation System.

**Requirements:**
- Recommend items to users
- Real-time recommendations
- Handle cold start
- Scalable

**Answer:**
**Approaches:**
1. **Collaborative Filtering**: User-based, item-based
2. **Content-Based**: Item features
3. **Hybrid**: Combine approaches

**Architecture:**
```
User → Recommendation Service → [Feature Store] [Model Service]
                                        ↓
                                   [ML Pipeline]
```

**Cold Start:**
- Popular items
- Demographic-based
- Content-based features

### 20. Design a Distributed Lock Service.

**Requirements:**
- Acquire/release locks
- Handle failures
- Low latency
- High availability

**Answer:**
**Implementation Options:**
1. **Redis**: SET NX with expiration
2. **ZooKeeper**: Ephemeral nodes
3. **etcd**: Distributed consensus

**Redis Implementation:**
```javascript
function acquireLock(lockKey, timeout) {
    const lockValue = Date.now().toString();
    const acquired = redis.set(lockKey, lockValue, 'PX', timeout, 'NX');
    return acquired ? lockValue : null;
}

function releaseLock(lockKey, lockValue) {
    const script = `
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
    `;
    return redis.eval(script, 1, lockKey, lockValue);
}
```

### 21. Design a Real-time Analytics Dashboard.

**Requirements:**
- Real-time metrics
- Historical data
- Multiple data sources
- Low latency queries

**Answer:**
**Components:**
1. **Event Collectors**: Collect events
2. **Stream Processor**: Process in real-time (Kafka Streams, Flink)
3. **Time-Series DB**: Store metrics (InfluxDB)
4. **Query Service**: Serve queries
5. **Dashboard**: Visualization

**Architecture:**
```
Events → Kafka → Stream Processor → Time-Series DB → Query Service → Dashboard
```

### 22. Design a Distributed Configuration Service.

**Requirements:**
- Store configurations
- Update configurations
- Notify services of changes
- Version control

**Answer:**
**Components:**
1. **Config Store**: Database for configs
2. **Config Service**: CRUD operations
3. **Notification**: Push updates (WebSocket, polling)
4. **Versioning**: Track changes

**Implementation:**
- **etcd**: Distributed key-value store
- **Consul**: Service discovery + config
- **ZooKeeper**: Configuration management

### 23. Design a Distributed Task Queue.

**Requirements:**
- Queue tasks
- Process tasks
- Retry failed tasks
- Priority queues

**Answer:**
**Components:**
1. **Task Queue**: Store tasks (Redis, RabbitMQ)
2. **Workers**: Process tasks
3. **Scheduler**: Schedule tasks
4. **Result Store**: Store results

**Architecture:**
```
Producer → Task Queue → Workers → Result Store
```

**Features:**
- Priority queues
- Delayed tasks
- Retry mechanism
- Dead letter queue

### 24. Design a Distributed Search System.

**Requirements:**
- Index documents
- Search across documents
- Handle large scale
- Fast queries

**Answer:**
**Components:**
1. **Indexer**: Build inverted index
2. **Search Engine**: Elasticsearch, Solr
3. **Query Processor**: Process queries
4. **Ranking**: Rank results

**Inverted Index:**
```
"javascript" → [doc1, doc3, doc5]
"react" → [doc2, doc3, doc7]
```

**Sharding:**
- Partition index by document ID
- Distribute across nodes
- Aggregate results

### 25. Design a Distributed Cache with Consistency.

**Requirements:**
- Distributed caching
- Consistency guarantees
- High availability
- Cache invalidation

**Answer:**
**Strategies:**
1. **Write-Through**: Write to cache and DB
2. **Write-Back**: Write to cache, async to DB
3. **Cache-Aside**: App manages cache

**Consistency:**
- **Strong**: Synchronous replication
- **Eventual**: Asynchronous replication
- **Read-Repair**: Fix inconsistencies on read

**Cache Invalidation:**
- TTL-based
- Event-based
- Manual invalidation
- Version-based

### 26. Design a distributed task scheduler.

**Answer:**
System to schedule and execute tasks across distributed workers.

**Requirements:**
- Schedule tasks with delay/cron
- Execute tasks reliably
- Scale horizontally
- Handle failures

**Architecture:**
```
Client → API Gateway → Task Scheduler
                          ↓
                    Message Queue (RabbitMQ/Kafka)
                          ↓
                    Worker Pool
                          ↓
                    Database (PostgreSQL)
```

**Components:**
1. **Scheduler Service**: Accepts tasks, schedules execution
2. **Message Queue**: Stores pending tasks
3. **Worker Pool**: Executes tasks
4. **Database**: Stores task metadata, history
5. **Monitoring**: Track task status, failures

**Task Storage:**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    type VARCHAR(50),
    payload JSONB,
    scheduled_at TIMESTAMP,
    status VARCHAR(20),
    retry_count INT,
    created_at TIMESTAMP
);
```

**Scheduling:**
- **Delayed Tasks**: Store with scheduled_at timestamp
- **Cron Tasks**: Parse cron expression, calculate next run
- **Periodic Polling**: Workers poll for due tasks

**Reliability:**
- Idempotent tasks
- Retry mechanism
- Dead letter queue
- Task deduplication

### 27. Design a real-time analytics system.

**Answer:**
System to process and analyze events in real-time.

**Requirements:**
- Low latency (< 100ms)
- High throughput (millions events/sec)
- Real-time dashboards
- Historical analysis

**Architecture:**
```
Events → Kafka → Stream Processor (Flink/Storm)
                    ↓
            Time-Series DB (InfluxDB)
                    ↓
            Dashboard (Grafana)
```

**Components:**
1. **Event Ingestion**: Kafka for event streaming
2. **Stream Processing**: Flink/Storm for real-time processing
3. **Storage**: 
   - Time-series DB for metrics
   - Data warehouse for historical
4. **Visualization**: Grafana/Kibana dashboards

**Processing:**
- **Windowing**: Sliding/tumbling windows
- **Aggregation**: Count, sum, average
- **Filtering**: Filter relevant events
- **Enrichment**: Add context to events

**Scaling:**
- Partition events by key
- Parallel processing
- Horizontal scaling

### 28. Design a configuration management service.

**Answer:**
Centralized service for application configuration.

**Requirements:**
- Centralized config storage
- Dynamic updates
- Versioning
- Environment-specific configs
- Access control

**Architecture:**
```
Apps → Config Service API
          ↓
    Database (PostgreSQL)
          ↓
    Cache (Redis)
          ↓
    Notification (WebSocket/Pub-Sub)
```

**Features:**
- **Hierarchical Config**: App → Environment → Feature
- **Versioning**: Track config changes
- **Rollback**: Revert to previous version
- **Validation**: Validate config before applying
- **Notifications**: Notify apps of changes

**Implementation:**
```javascript
// Config structure
{
    "app": "user-service",
    "environment": "production",
    "config": {
        "database": {
            "host": "db.example.com",
            "port": 5432
        },
        "features": {
            "newFeature": true
        }
    },
    "version": 1,
    "updatedAt": "2024-01-01T00:00:00Z"
}
```

**Caching:**
- Cache configs in Redis
- TTL-based expiration
- Invalidate on updates

### 29. Design a distributed lock service.

**Answer:**
Service to coordinate access to shared resources.

**Requirements:**
- Mutual exclusion
- Deadlock prevention
- Fault tolerance
- Low latency

**Implementation Options:**

**1. Redis:**
```javascript
// Acquire lock
const lock = await redis.set(
    'lock:resource',
    'owner-id',
    'EX', 10,  // Expire in 10 seconds
    'NX'      // Only if not exists
);

// Release lock
if (await redis.get('lock:resource') === 'owner-id') {
    await redis.del('lock:resource');
}
```

**2. ZooKeeper:**
- Ephemeral nodes
- Sequential nodes
- Watch mechanism

**3. Database:**
```sql
-- Acquire lock
INSERT INTO locks (resource, owner, expires_at)
VALUES ('resource-id', 'owner-id', NOW() + INTERVAL '10 seconds')
ON CONFLICT (resource) DO NOTHING;

-- Release lock
DELETE FROM locks WHERE resource = 'resource-id' AND owner = 'owner-id';
```

**Best Practices:**
- Set expiration time
- Use unique owner ID
- Implement renewal mechanism
- Handle failures gracefully

### 30. Design a multi-tenant SaaS system.

**Answer:**
System serving multiple customers (tenants) from single codebase.

**Tenancy Models:**

**1. Database per Tenant:**
- Isolation: Complete
- Scalability: High
- Cost: High

**2. Shared Database, Separate Schemas:**
- Isolation: Good
- Scalability: Medium
- Cost: Medium

**3. Shared Database, Shared Schema:**
- Isolation: Application-level
- Scalability: High
- Cost: Low

**Architecture:**
```
Request → Tenant Resolver → Tenant Context
                              ↓
                        Application Logic
                              ↓
                        Tenant-Aware DB
```

**Tenant Identification:**
- Subdomain: `tenant1.app.com`
- Path: `app.com/tenant1/...`
- Header: `X-Tenant-ID`

**Data Isolation:**
```sql
-- Row-level security
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Query
SET app.tenant_id = 'tenant-uuid';
SELECT * FROM users;  -- Only returns tenant's users
```

**Features:**
- Tenant-specific configuration
- Custom branding
- Usage quotas
- Billing per tenant

### 31. Design a Distributed Cache System.

**Requirements:**
- Store key-value pairs
- High availability
- Low latency
- Handle 1M requests/second

**Answer:**
**Components:**
1. **Cache Servers**: Redis/Memcached clusters
2. **Consistent Hashing**: Distribute keys across servers
3. **Replication**: Master-slave for availability
4. **Cache Invalidation**: TTL, LRU eviction

**Architecture:**
```
Client → Load Balancer → Cache Cluster
                          ├── Node 1 (Hash Ring)
                          ├── Node 2 (Hash Ring)
                          └── Node 3 (Hash Ring)
```

**Key Design:**
- Consistent hashing for distribution
- Replication for fault tolerance
- Cache warming strategies
- Cache aside pattern

### 32. Design a Search Engine (Google-like).

**Requirements:**
- Index billions of web pages
- Fast search results
- Handle 1B queries/day
- Rank results by relevance

**Answer:**
**Components:**
1. **Web Crawler**: Discover and fetch pages
2. **Indexer**: Build inverted index
3. **Ranking Service**: PageRank, relevance scoring
4. **Query Processor**: Parse and execute queries
5. **Result Aggregator**: Combine results

**Architecture:**
```
Crawler → Indexer → Inverted Index → Query Processor → Results
```

**Key Design:**
- Inverted index: word → [doc1, doc2, ...]
- Distributed indexing (MapReduce)
- Ranking algorithms (PageRank, TF-IDF)
- Caching popular queries

### 33. Design a Notification System.

**Requirements:**
- Send notifications (email, SMS, push)
- Support multiple channels
- Handle 10M notifications/day
- Delivery tracking

**Answer:**
**Components:**
1. **Notification Service**: Core service
2. **Channel Handlers**: Email, SMS, Push
3. **Message Queue**: Async processing
4. **Template Engine**: Message templates
5. **Delivery Tracker**: Status tracking

**Architecture:**
```
API → Notification Service → Message Queue → Channel Handlers
                                              ├── Email Service
                                              ├── SMS Service
                                              └── Push Service
```

**Key Design:**
- Queue-based async processing
- Retry mechanism for failures
- Rate limiting per channel
- Template management

### 34. Design a File Storage System (Dropbox-like).

**Requirements:**
- Store files up to 10GB
- Sync across devices
- Version history
- Handle 100M users

**Answer:**
**Components:**
1. **API Gateway**: Handle requests
2. **Metadata Service**: File metadata (name, size, version)
3. **Storage Service**: Object storage (S3-like)
4. **Sync Service**: Detect and sync changes
5. **Version Control**: Track file versions

**Architecture:**
```
Client → API Gateway → Metadata DB → Storage Service
                        ↓
                    Sync Service
```

**Key Design:**
- Separate metadata and file storage
- Chunking for large files
- Delta sync (only changed chunks)
- Conflict resolution

### 35. Design a Real-time Analytics System.

**Requirements:**
- Process 1M events/second
- Real-time dashboards
- Historical data storage
- Support multiple metrics

**Answer:**
**Components:**
1. **Event Ingestion**: Kafka/Pulsar
2. **Stream Processing**: Flink/Storm
3. **Time-Series DB**: InfluxDB, TimescaleDB
4. **Aggregation Service**: Pre-compute metrics
5. **Dashboard Service**: Serve analytics

**Architecture:**
```
Events → Kafka → Stream Processor → Time-Series DB → Dashboard
```

**Key Design:**
- Event streaming architecture
- Windowing for aggregations
- Pre-aggregation for common queries
- Caching for dashboards

### 36. Design a Payment Processing System.

**Requirements:**
- Process payments securely
- Support multiple payment methods
- Handle 1M transactions/day
- Fraud detection

**Answer:**
**Components:**
1. **Payment Gateway**: Process payments
2. **Payment Methods**: Credit card, PayPal, etc.
3. **Fraud Detection**: ML-based detection
4. **Transaction Service**: Record transactions
5. **Settlement Service**: Batch settlement

**Architecture:**
```
Client → Payment Gateway → Fraud Detection → Payment Processor
                                              ↓
                                        Transaction DB
```

**Key Design:**
- Idempotency keys
- Two-phase commit for consistency
- Encryption (PCI-DSS compliance)
- Retry with exponential backoff

### 37. Design a Social Media Feed (Twitter-like).

**Requirements:**
- Post tweets (280 chars)
- Follow/unfollow users
- Timeline generation
- Handle 500M users

**Answer:**
**Components:**
1. **Post Service**: Create/read posts
2. **Follow Service**: Manage relationships
3. **Timeline Service**: Generate feeds
4. **Fan-out Service**: Push to followers
5. **Search Service**: Full-text search

**Architecture:**
```
Post → Fan-out → Followers' Timeline Cache
                ↓
            Timeline Service
```

**Key Design:**
- Push model (fan-out on write)
- Pull model (on read) for inactive users
- Hybrid approach
- Caching for hot timelines

### 38. Design a Video Streaming Service (YouTube-like).

**Requirements:**
- Upload videos
- Stream videos
- Handle 1B users
- Support multiple resolutions

**Answer:**
**Components:**
1. **Upload Service**: Handle video uploads
2. **Transcoding Service**: Convert to multiple formats
3. **CDN**: Distribute video content
4. **Streaming Service**: Adaptive bitrate streaming
5. **Metadata Service**: Video info, thumbnails

**Architecture:**
```
Upload → Transcoding → Storage → CDN → Client
```

**Key Design:**
- Chunked upload for large files
- Multiple quality levels (240p, 480p, 720p, 1080p)
- CDN for global distribution
- Adaptive bitrate (HLS/DASH)

### 39. Design a Distributed Lock Service.

**Requirements:**
- Acquire/release locks
- Handle lock expiration
- High availability
- Low latency

**Answer:**
**Components:**
1. **Lock Service**: Core locking logic
2. **Consensus Algorithm**: Raft/Paxos
3. **Lease Management**: TTL for locks
4. **Watch Service**: Notify on lock release

**Architecture:**
```
Client → Lock Service Cluster (Raft) → Lock Storage
```

**Key Design:**
- Distributed consensus (Raft)
- Lease-based locks (auto-expire)
- Watch mechanism for notifications
- Fencing tokens for safety

### 40. Design a Recommendation System (Netflix-like).

**Requirements:**
- Recommend content to users
- Handle 200M users
- Real-time recommendations
- Multiple recommendation types

**Answer:**
**Components:**
1. **Feature Store**: User/item features
2. **ML Models**: Collaborative filtering, content-based
3. **Ranking Service**: Score and rank items
4. **A/B Testing**: Test different algorithms
5. **Cache**: Pre-computed recommendations

**Architecture:**
```
User → Recommendation API → ML Models → Ranking → Results
```

**Key Design:**
- Collaborative filtering (user-based, item-based)
- Content-based filtering
- Hybrid approach
- Real-time and batch processing

### 41. Design a Distributed Logging System.

**Requirements:**
- Collect logs from services
- Store logs efficiently
- Search and query logs
- Handle 1B log entries/day

**Answer:**
**Components:**
1. **Log Collector**: Collect from services
2. **Message Queue**: Buffer logs
3. **Log Storage**: Distributed storage
4. **Index Service**: Index for search
5. **Query Service**: Search interface

**Architecture:**
```
Services → Log Collector → Kafka → Storage → Index → Query
```

**Key Design:**
- Structured logging (JSON)
- Partitioning by time/service
- Compression for storage
- Full-text search index

### 42. Design a Distributed Configuration Service.

**Requirements:**
- Store configuration
- Real-time updates
- Version history
- Support multiple environments

**Answer:**
**Components:**
1. **Config Service**: Core service
2. **Watch Service**: Notify on changes
3. **Version Control**: Track versions
4. **Environment Management**: Dev, staging, prod

**Architecture:**
```
Config Service → Watch Service → Clients
```

**Key Design:**
- Hierarchical configuration
- Watch mechanism (push updates)
- Versioning and rollback
- Encryption for sensitive data

### 43. Design a Distributed Task Scheduler (Cron-like).

**Requirements:**
- Schedule tasks
- Execute at specified times
- Handle failures
- Support millions of tasks

**Answer:**
**Components:**
1. **Scheduler Service**: Schedule tasks
2. **Task Queue**: Priority queue
3. **Worker Pool**: Execute tasks
4. **Retry Service**: Handle failures
5. **Monitoring**: Track execution

**Architecture:**
```
Scheduler → Task Queue → Workers → Retry Service
```

**Key Design:**
- Priority queue (time-based)
- Distributed workers
- Idempotent tasks
- Dead letter queue for failures

### 44. Design a Distributed Counter Service.

**Requirements:**
- Increment/decrement counters
- High throughput
- Eventually consistent
- Handle 10M operations/second

**Answer:**
**Components:**
1. **Counter Service**: Core service
2. **Sharding**: Distribute counters
3. **Replication**: For availability
4. **Aggregation Service**: Merge shards

**Architecture:**
```
Client → Counter Service → Shards → Replication
```

**Key Design:**
- Sharding by counter ID
- CRDTs for conflict resolution
- Batching for efficiency
- Periodic aggregation

### 45. Design a Distributed Queue System.

**Requirements:**
- Enqueue/dequeue messages
- At-least-once delivery
- Ordering guarantees
- Handle 1M messages/second

**Answer:**
**Components:**
1. **Queue Service**: Core service
2. **Partitioning**: Distribute queues
3. **Replication**: For durability
4. **Consumer Groups**: Parallel processing

**Architecture:**
```
Producer → Queue Partitions → Consumer Groups
```

**Key Design:**
- Partitioning for scalability
- Replication for durability
- Consumer groups for parallelism
- Dead letter queue

### 46. Design a Web Crawler.

**Requirements:**
- Crawl web pages
- Respect robots.txt
- Handle billions of pages
- Avoid duplicates

**Answer:**
**Components:**
1. **URL Frontier**: Queue of URLs to crawl
2. **DNS Resolver**: Resolve domain names
3. **Fetcher**: Download pages
4. **Parser**: Extract links and content
5. **Deduplicator**: Check for duplicates
6. **Storage**: Store crawled content

**Architecture:**
```
Seed URLs → URL Frontier → Fetcher → Parser → Storage
                              ↓
                          Deduplicator
```

**Key Design:**
- Politeness (rate limiting per domain)
- Robots.txt compliance
- URL normalization
- Bloom filter for duplicate detection

### 47. Design a Distributed File System (GFS-like).

**Requirements:**
- Store large files
- Handle failures
- High throughput
- Replication

**Answer:**
**Components:**
1. **Master Node**: Metadata management
2. **Chunk Servers**: Store file chunks
3. **Client Library**: Interface for clients
4. **Replication**: Multiple copies of chunks

**Architecture:**
```
Client → Master (metadata) → Chunk Servers (data)
```

**Key Design:**
- Chunk-based storage (64MB chunks)
- Master keeps metadata only
- Replication (3 copies)
- Heartbeat for health checks

### 48. Design a News Feed System.

**Requirements:**
- Display personalized feed
- Real-time updates
- Handle 100M users
- Multiple content types

**Answer:**
**Components:**
1. **Content Service**: Store posts/articles
2. **Social Graph**: User relationships
3. **Ranking Service**: Personalize feed
4. **Feed Generator**: Build feed
5. **Cache**: Store pre-computed feeds

**Architecture:**
```
User → Feed API → Ranking → Feed Generator → Cache
```

**Key Design:**
- Pre-compute feeds (pull model)
- Real-time updates (push model)
- Ranking algorithm (relevance, recency)
- Caching strategy

### 49. Design a Distributed ID Generator.

**Requirements:**
- Generate unique IDs
- High throughput
- No collisions
- Distributed system

**Answer:**
**Approaches:**
1. **UUID**: 128-bit unique identifier
2. **Snowflake**: Twitter's ID generator (timestamp + machine + sequence)
3. **Database Sequence**: Auto-increment with sharding
4. **Redis INCR**: Atomic counter

**Snowflake Algorithm:**
```
64-bit ID = 41 bits (timestamp) + 10 bits (machine) + 12 bits (sequence)
```

**Key Design:**
- Monotonic IDs
- No coordination needed
- Time-based ordering
- High throughput

### 50. Design a Leaderboard System.

**Requirements:**
- Real-time rankings
- Handle millions of users
- Multiple leaderboards
- Historical data

**Answer:**
**Components:**
1. **Score Service**: Update scores
2. **Ranking Service**: Calculate ranks
3. **Storage**: Redis Sorted Sets
4. **Cache**: Top N players

**Architecture:**
```
Score Update → Ranking Service → Redis Sorted Set → Cache
```

**Key Design:**
- Redis Sorted Sets (ZADD, ZRANK)
- Periodic snapshots for history
- Sharding by leaderboard type
- Caching top players

### 51. Design a URL Shortener (Detailed).

**Requirements:**
- Shorten long URLs
- Redirect to original
- Analytics
- Handle 100M URLs/day

**Answer:**
**Components:**
1. **Short URL Generator**: Base62 encoding
2. **Mapping Service**: Store short → long mapping
3. **Redirect Service**: Handle redirects
4. **Analytics Service**: Track clicks
5. **Cache**: Redis for hot URLs

**Algorithm:**
- Counter-based: Auto-increment ID → Base62
- Hash-based: MD5/SHA → Base62 (first 6 chars)
- Random: Generate random string

**Database:**
```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY,
    short_url VARCHAR(10) UNIQUE,
    original_url TEXT,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    click_count INT
);
```

### 52. Design a Pastebin Service.

**Requirements:**
- Store text snippets
- Expiration support
- Syntax highlighting
- Handle 10M pastes/day

**Answer:**
**Components:**
1. **Paste Service**: Create/read pastes
2. **Storage**: Database + Object storage
3. **Expiration Service**: Clean up expired
4. **Syntax Highlighter**: Client-side or server-side

**Architecture:**
```
Client → API → Paste Service → Storage
                        ↓
                  Expiration Job
```

**Key Design:**
- Short unique IDs
- TTL for expiration
- Compression for large pastes
- CDN for static assets

### 53. Design a Distributed Cache (Memcached-like).

**Requirements:**
- Key-value storage
- High throughput
- Low latency
- Distributed

**Answer:**
**Components:**
1. **Cache Nodes**: Store key-value pairs
2. **Consistent Hashing**: Distribute keys
3. **Replication**: For availability
4. **Eviction Policy**: LRU, LFU

**Architecture:**
```
Client → Hash Function → Cache Node → Memory Storage
```

**Key Design:**
- Consistent hashing
- Replication (master-slave)
- Eviction policies
- TTL support

### 54. Design a Rate Limiter (Detailed).

**Requirements:**
- Limit requests per user/IP
- Multiple algorithms
- Distributed system
- Handle 1M requests/second

**Answer:**
**Algorithms:**
1. **Token Bucket**: Tokens added at rate, request consumes token
2. **Leaky Bucket**: Requests added, processed at fixed rate
3. **Fixed Window**: Count in time window
4. **Sliding Window**: Count in sliding window

**Implementation:**
```javascript
class RateLimiter {
    constructor(maxRequests, windowMs) {
        this.maxRequests = maxRequests;
        this.windowMs = windowMs;
        this.requests = new Map();
    }
    
    isAllowed(identifier) {
        const now = Date.now();
        const windowStart = now - this.windowMs;
        
        if (!this.requests.has(identifier)) {
            this.requests.set(identifier, []);
        }
        
        const userRequests = this.requests.get(identifier);
        const recentRequests = userRequests.filter(time => time > windowStart);
        
        if (recentRequests.length >= this.maxRequests) {
            return false;
        }
        
        recentRequests.push(now);
        this.requests.set(identifier, recentRequests);
        return true;
    }
}
```

### 55. Design a Distributed Lock (Detailed).

**Requirements:**
- Acquire/release locks
- Handle failures
- Prevent deadlocks
- High availability

**Answer:**
**Implementation with Redis:**
```javascript
async function acquireLock(key, ttl) {
    const lockKey = `lock:${key}`;
    const result = await redis.set(lockKey, 'locked', 'EX', ttl, 'NX');
    return result === 'OK';
}

async function releaseLock(key) {
    await redis.del(`lock:${key}`);
}
```

**Redlock Algorithm:**
- Acquire lock on majority of nodes
- Prevents single point of failure
- Handles clock skew

### 56. Design a Distributed Counter.

**Requirements:**
- Increment/decrement
- High throughput
- Eventually consistent
- Handle 10M ops/second

**Answer:**
**Approaches:**
1. **Sharded Counters**: Distribute by key
2. **CRDTs**: Conflict-free replicated data types
3. **Redis INCR**: Atomic operations
4. **Cassandra Counters**: Distributed counters

**Sharded Approach:**
```
Counter ID → Hash → Shard → Local Counter → Periodic Aggregation
```

### 57. Design a Distributed Session Store.

**Requirements:**
- Store user sessions
- High availability
- Low latency
- Handle 100M sessions

**Answer:**
**Components:**
1. **Session Service**: Manage sessions
2. **Storage**: Redis cluster
3. **Replication**: For availability
4. **TTL**: Auto-expire sessions

**Architecture:**
```
Client → Session Service → Redis Cluster → Replication
```

**Key Design:**
- Session ID generation
- TTL management
- Replication strategy
- Sticky sessions vs stateless

### 58. Design a Distributed Tracing System.

**Requirements:**
- Track requests across services
- Low overhead
- Query traces
- Handle 1M traces/second

**Answer:**
**Components:**
1. **Tracer**: Instrument services
2. **Collector**: Gather traces
3. **Storage**: Time-series database
4. **Query Service**: Search traces

**Architecture:**
```
Service → Tracer → Collector → Storage → Query Service
```

**Key Design:**
- Trace ID propagation
- Sampling (reduce overhead)
- Span correlation
- Storage optimization

### 59. Design a Content Delivery Network (CDN).

**Requirements:**
- Serve static content globally
- Low latency
- High availability
- Handle 1B requests/day

**Answer:**
**Components:**
1. **Edge Servers**: Serve content
2. **Origin Server**: Source of truth
3. **DNS**: Route to nearest edge
4. **Cache**: Store popular content

**Architecture:**
```
User → DNS → Edge Server → Cache → Origin (if miss)
```

**Key Design:**
- Geographic distribution
- Cache invalidation
- Load balancing
- Health checks

### 60. Design a Distributed Search System.

**Requirements:**
- Full-text search
- Handle billions of documents
- Low latency
- High availability

**Answer:**
**Components:**
1. **Indexer**: Build inverted index
2. **Search Service**: Execute queries
3. **Sharding**: Distribute index
4. **Replication**: For availability

**Architecture:**
```
Documents → Indexer → Sharded Index → Search Service → Results
```

**Key Design:**
- Inverted index structure
- Sharding strategy
- Query routing
- Result merging

---

This covers system design interview questions from beginner to advanced level with detailed explanations and architectures.

