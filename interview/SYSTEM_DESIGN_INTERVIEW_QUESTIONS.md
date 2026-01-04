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

---

This covers system design interview questions from beginner to advanced level with detailed explanations and architectures.

