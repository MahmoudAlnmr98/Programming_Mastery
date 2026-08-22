# Networking — Interview Questions & Answers
> 100 questions. HTTP/1.1/2/3, TCP/IP, DNS, WebSockets, TLS/SSL, CDN, Load Balancing.

---

## HTTP (Q1-Q30)

**Q1. HTTP/1.1 vs HTTP/2 vs HTTP/3.**
```
HTTP/1.1: One request per connection, 6 connections/domain browser limit, HoL blocking, text-based headers.
HTTP/2: Multiplexing (many requests one TCP connection), HPACK header compression, binary protocol. Still has TCP HoL blocking.
HTTP/3: QUIC protocol (UDP-based), no HoL blocking, 0-RTT reconnect, built-in TLS 1.3, connection migration.
```

**Q2. HTTP methods and status codes.**
```
Methods: GET (read, safe, idempotent) | POST (create) | PUT (replace, idempotent) | PATCH (partial update) | DELETE (idempotent) | HEAD (headers only) | OPTIONS (CORS preflight)

2xx: 200 OK, 201 Created + Location header, 202 Accepted (async), 204 No Content
3xx: 301 Permanent Redirect, 302 Temporary, 304 Not Modified, 307/308 preserve method
4xx: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Rate Limited + Retry-After
5xx: 500 Internal, 502 Bad Gateway, 503 Unavailable, 504 Gateway Timeout
```

**Q3. HTTP caching.**
```javascript
// Cache-Control directives:
// public: CDN + browser cacheable
// private: browser only (authenticated responses)
// no-cache: must revalidate (can store)
// no-store: never store (sensitive data)
// max-age=3600: fresh for 1 hour
// s-maxage=86400: CDN cache time (overrides max-age for CDN)
// stale-while-revalidate=3600: serve stale 1h while revalidating async
// immutable: never changes (hashed filenames)

// Static assets:
res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');

// Conditional requests - ETag:
res.setHeader('ETag', '"' + hash(content) + '"');
// Client sends: If-None-Match: "abc123" -> 304 Not Modified if unchanged
```

**Q4. TLS 1.3 handshake.**
```
Client -> Server: ClientHello (TLS version, cipher suites, DH public key, SNI)
Server -> Client: ServerHello + Certificate + CertificateVerify + Finished
  - Both compute shared secret via Diffie-Hellman key exchange
  - Encrypted from this point
Client -> Server: Finished
  - Verifies server certificate (CA chain of trust)

0-RTT: client uses session ticket from previous connection to send data immediately
mTLS: both sides present certificates (used in microservices / zero trust)
```

**Q5. CORS.**
```javascript
// Simple requests: GET/POST with simple headers - browser checks response headers
// Preflight: PUT/DELETE/custom headers - OPTIONS sent first

app.use(cors({
  origin: ['https://myapp.com', 'https://admin.myapp.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400,  // cache preflight 24h
}));

// Access-Control-Allow-Origin: https://myapp.com
// Access-Control-Allow-Credentials: true
// Access-Control-Allow-Methods: GET,POST,PUT,DELETE
// Omitting credentials=true means cookies/auth headers not sent cross-origin
```

---

## TCP/IP (Q31-Q50)

**Q31. TCP 3-way handshake.**
```
Client -> Server: SYN (seq=x)         "I want to connect"
Server -> Client: SYN-ACK (seq=y, ack=x+1)  "OK, I hear you"
Client -> Server: ACK (ack=y+1)       "Connected"

Cost: 1 RTT before data. HTTPS adds TLS: ~2-3 RTT total (HTTP/2+TLS1.3: 1-2 RTT)

4-way close:
Client: FIN -> Server: ACK -> Server: FIN -> Client: ACK
Client waits TIME_WAIT (2xMSL ~4min) to ensure clean close

TCP vs UDP:
TCP: reliable, ordered, error correction, connection-based, congestion control
UDP: unreliable, connectionless, faster. Used for: DNS, video streaming, gaming, QUIC
```

**Q32. DNS resolution.**
```
Query for api.example.com:
1. Browser cache -> OS cache -> /etc/hosts
2. Recursive resolver (ISP/8.8.8.8)
3. Root nameserver -> .com TLD nameserver
4. example.com authoritative nameserver -> A record: 93.184.216.34
5. Resolver caches (TTL), returns to client

Record types:
A: hostname -> IPv4  | AAAA: hostname -> IPv6  | CNAME: alias -> hostname
MX: mail servers     | TXT: SPF/DKIM/verification | NS: nameservers
PTR: reverse DNS     | SRV: service location       | CAA: allowed CAs

DNSSEC: cryptographic signing prevents cache poisoning
DoH/DoT: encrypt DNS queries for privacy
Low TTL (60s): fast failover | High TTL (86400): fewer queries, slow propagation
```

---

## WEBSOCKETS (Q51-Q65)

**Q51. WebSocket protocol.**
```javascript
// HTTP upgrade: GET request with Upgrade: websocket header
// Server responds: 101 Switching Protocols
// Both sides can now send frames at any time (full-duplex)

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws, req) => {
  // Heartbeat to detect dead connections:
  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    // Broadcast to all:
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) client.send(data);
    });
  });

  ws.on('close', () => cleanup(ws));
});

// Ping all 30s, kill dead connections:
setInterval(() => {
  wss.clients.forEach(ws => {
    if (!ws.isAlive) { ws.terminate(); return; }
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);
```

**Q52. WebSocket scaling with Redis pub/sub.**
```javascript
// Problem: client on server1 can't receive from client on server2
// Solution: Redis pub/sub as message bus between server instances

const publisher  = createClient({ url: REDIS_URL });
const subscriber = createClient({ url: REDIS_URL });

// All servers subscribe to all room channels:
await subscriber.pSubscribe('room:*', (message, channel) => {
  const roomId = channel.replace('room:', '');
  // Forward to local clients in this room:
  clients.forEach(ws => {
    if (ws.rooms?.has(roomId)) ws.send(message);
  });
});

// When client sends message -> publish to Redis -> all servers forward to room members
await publisher.publish(`room:${roomId}`, JSON.stringify({ from: clientId, text }));
```

---

## LOAD BALANCING & CDN (Q66-Q85)

**Q66. Load balancing algorithms.**
```
Round Robin:           equal distribution. Good for identical servers.
Weighted Round Robin:  proportional by server weight. Good for different capacities.
Least Connections:     route to server with fewest active connections.
Least Response Time:   route to fastest responding server.
IP Hash:               same IP always -> same server (sticky sessions).
Random with 2 choices: pick 2 random, send to less loaded (prevents hot spots).

Layer 4 (TCP): routes by IP/port, fastest, no content inspection
Layer 7 (HTTP): routes by URL/headers/cookies, smarter routing
Health checks: active (probe endpoint) or passive (track errors)
```

**Q67. CDN architecture.**
```
PoPs (Points of Presence): globally distributed edge servers
User -> nearest PoP (Anycast DNS routing) -> origin if cache miss

Cache-Control headers control CDN behavior:
  s-maxage=86400: CDN caches 24h (browser respects max-age)
  stale-while-revalidate: serve stale, refresh in background
  Surrogate-Key / Cache-Tag: group objects for bulk invalidation

Origin Shield: one designated "shield" PoP between edges and origin
  1000 cache misses on different edges -> 1 request to origin

Edge computing (Cloudflare Workers, Lambda@Edge):
  Run code at edge for auth, A/B testing, personalization
  Sub-millisecond latency for computed responses
```

---

## NETWORK SECURITY (Q86-Q100)

**Q86. DDoS protection.**
```
Volumetric: flood with traffic (UDP/ICMP flood) -> exhaust bandwidth
Protocol: SYN flood -> exhaust server connection tables
Application (L7): HTTP flood -> exhaust server resources

SYN Flood: SYN cookies (encode state in seq number, no memory until ACK)
Rate limiting per IP/endpoint/method
Anycast: distribute traffic across many nodes
Cloudflare: absorbs at network level, 256 Tbps capacity
AWS Shield Standard (free) / Advanced ($3000/mo + DRT team)
```

**Q87. HTTP security headers.**
```javascript
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc:  ["'self'", "nonce-{nonce}"],
      objectSrc:  ["'none'"],
      upgradeInsecureRequests: [],
    }
  },
  frameguard: { action: 'deny' },           // X-Frame-Options: DENY
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  noSniff: true,                            // X-Content-Type-Options: nosniff
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  permittedCrossDomainPolicies: false,
}));
// Permissions-Policy: camera=(), microphone=(), geolocation=(self)
```

**Q88. mTLS for microservices.**
```javascript
// Standard TLS: server proves identity to client
// mTLS: BOTH sides present certificates
// Used in: zero trust, microservice authentication, Kubernetes pod-to-pod

const server = https.createServer({
  cert: fs.readFileSync('/certs/server.crt'),
  key:  fs.readFileSync('/certs/server.key'),
  ca:   fs.readFileSync('/certs/ca.crt'),  // trust this CA for client certs
  requestCert: true,
  rejectUnauthorized: true,
}, app);

// Istio service mesh: automatically handles mTLS between all pods
// No code changes needed, sidecar proxy (Envoy) handles everything
```

**Q89. Zero Trust Network principles.**
```
Traditional: trust inside network perimeter, block outside
Zero Trust: never trust, always verify - regardless of location

Principles:
1. Verify explicitly (identity, device, location, service)
2. Use least privilege access (JIT, just enough access)
3. Assume breach (minimize blast radius, segment network)

Implementation:
- mTLS between all services
- Service accounts with SPIFFE/SPIRE certificates
- Policy enforcement at service mesh (Istio)
- Network segmentation (microsegmentation)
- Audit all access (SIEM)

Tools: Cloudflare Access, BeyondCorp (Google), Istio, HashiCorp Vault
```

**Q90. Network troubleshooting.**
```bash
dig api.example.com              # DNS lookup
dig @8.8.8.8 api.example.com    # specific DNS server
ping api.example.com             # reachability
mtr api.example.com              # continuous traceroute
nc -zv api.example.com 443       # port check
curl -v https://api.example.com  # verbose HTTP
curl -w "%{time_total}\n" https://api.example.com  # timing
openssl s_client -connect api.example.com:443  # SSL inspection
ss -tuln                         # listening ports
lsof -i :3000                    # what's using port 3000
```


---

## COMPLETING NETWORKING Q17–Q100

**Q17. TCP flow control and congestion control.**
```
FLOW CONTROL (receiver controls sender speed):
- Receiver advertises window size (how much buffer available)
- Sender cannot send more than receiver's window
- When buffer full: window=0, sender stops
- Receiver sends window update when buffer frees up

CONGESTION CONTROL (network controls sender speed):
- Slow start: begin with small cwnd, double each RTT until threshold
- Congestion avoidance: increase linearly when near threshold
- Fast retransmit: 3 duplicate ACKs → retransmit without waiting for timeout
- Fast recovery: halve cwnd on duplicate ACKs (not timeout)
- Timeout: reset to slow start

BBRC (newer): bandwidth-based, estimates bottleneck bandwidth + RTT
```

**Q18. HTTP caching deep dive.**
```
Cache-Control headers:
public:                   CDN + browser can cache
private:                  browser only (authenticated content)
no-cache:                 must revalidate before use (not "don't cache")
no-store:                 never cache (sensitive data)
max-age=3600:             fresh for 3600 seconds
s-maxage=86400:           CDN max age (overrides max-age for CDNs)
stale-while-revalidate:   serve stale, refresh async
immutable:                never changes (versioned assets)
must-revalidate:          revalidate on stale (don't use stale)

Validation:
ETag: "abc123"            content hash
Last-Modified: Mon...     modification date
If-None-Match:            client sends ETag → 304 if unchanged
If-Modified-Since:        client sends date → 304 if unchanged

Vary header:
Vary: Accept-Encoding     separate cache per encoding
Vary: Accept-Language     separate cache per language
Vary: *                   don't cache (always different)
```

**Q19. DNS security — DNSSEC and DNS over HTTPS.**
```
DNSSEC (DNS Security Extensions):
- Cryptographically signs DNS records
- Prevents cache poisoning attacks (Kaminsky attack)
- Chain of trust from root zone to domain
- Records: RRSIG (signature), DNSKEY (public key), DS (key digest)
- Adoption: ~30% of domains, growing

DNS Cache Poisoning (Kaminsky attack):
- Attacker floods resolver with fake responses
- Hopes to win race before legitimate response
- Fix: randomize source port + transaction ID (Birthday paradox harder)

DNS over HTTPS (DoH):
- Encrypts DNS queries in HTTPS (port 443)
- Hides queries from ISP/network observers
- Supported: Chrome, Firefox, Windows 11
- Providers: Cloudflare (1.1.1.1), Google (8.8.8.8), Quad9

DNS over TLS (DoT):
- Encrypts DNS queries in TLS (port 853)
- Simpler than DoH, distinct port easier to identify
```

**Q20–Q60: Networking patterns**
```
Q20. Anycast routing: same IP announced from multiple locations
  - Request routes to nearest PoP automatically
  - Used by: CDNs, DNS providers, DDoS mitigation
  - Cloudflare: 300+ PoPs with Anycast

Q21. BGP (Border Gateway Protocol):
  - Routing between autonomous systems (AS) on internet
  - Path vector protocol: know which AS a route goes through
  - BGP hijacking: malicious AS announces others' IP prefixes

Q22. NAT (Network Address Translation):
  - Many private IPs → one public IP
  - NAT64: IPv6 only clients access IPv4 servers
  - CGNAT: carrier-grade NAT for ISPs

Q23. VPN protocols:
  - WireGuard: modern, fast, simple, 4000 lines of code
  - OpenVPN: mature, flexible, slower
  - IPSec/IKEv2: enterprise, built into OS
  - TLS-based (SSL VPN): works through HTTPS proxy

Q24. HTTP/3 internals:
  - Built on QUIC (Quick UDP Internet Connections)
  - UDP instead of TCP: no 3-way handshake blocking
  - 0-RTT: send data with first packet (session resumption)
  - Stream independence: packet loss only affects one stream
  - Connection migration: change network (WiFi → 4G) without reconnect

Q25. WebSocket handshake details:
  Client request:
  GET /chat HTTP/1.1
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
  Sec-WebSocket-Version: 13

  Server response:
  HTTP/1.1 101 Switching Protocols
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo= (SHA1 of key+magic)

Q26. TLS certificate types:
  DV (Domain Validation): just proves domain ownership, minutes to get
  OV (Organization Validation): validates organization, days
  EV (Extended Validation): thorough vetting, shows org in browser bar
  Wildcard: *.example.com — all subdomains
  SAN: Subject Alternative Name — multiple domains in one cert

Q27. Certificate Transparency (CT):
  - All certs must be logged in public CT logs
  - Browsers reject certs not in CT logs
  - Allows detecting misissued/fraudulent certificates
  - Google Chrome enforces CT since 2018

Q28. OCSP stapling:
  - Server proves certificate not revoked in TLS handshake
  - Avoids browser needing to contact OCSP server
  - Faster, more private than direct OCSP check

Q29. HTTP/2 server push (largely abandoned):
  - Server sends resources before client requests
  - Problem: doesn't check cache, may push already-cached assets
  - Better alternative: 103 Early Hints response
  - 103 Early Hints: server sends preload hints before 200 response

Q30. Keep-Alive and persistent connections:
  HTTP/1.0: new connection per request (Connection: close)
  HTTP/1.1: keep-alive by default (Connection: keep-alive)
  HTTP/2: multiplexing over one connection (keep-alive always)
  Keep-Alive header: Keep-Alive: timeout=30, max=1000

Q31–Q60: Additional networking topics
  Q31. IP addressing: CIDR notation, subnetting, VLSM
  Q32. Private IP ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
  Q33. IPv6 adoption: ~40% of traffic, dual-stack, NAT64/DNS64
  Q34. ICMP: ping (echo request/reply), traceroute, path MTU discovery
  Q35. ARP: resolve IP to MAC address on local network
  Q36. DHCP: automatic IP assignment, lease time, DHCP snooping
  Q37. Ethernet frame: source/dest MAC, EtherType, payload, FCS
  Q38. VLANs: logical network separation on same physical switch
  Q39. Spanning Tree Protocol: prevent loops in switched networks
  Q40. OSPF/RIP: interior routing protocols for enterprise networks
  Q41. Load balancer algorithms: round robin, least connections, IP hash
  Q42. L4 vs L7 load balancing trade-offs
  Q43. Reverse proxy vs forward proxy
  Q44. SOCKS proxy vs HTTP proxy
  Q45. Content delivery network architecture
  Q46. Peering: direct interconnection between ISPs/CDNs
  Q47. Internet exchange points (IXP): physical peering locations
  Q48. BGP communities: tagging routes for routing policy
  Q49. QoS: prioritize traffic (VoIP over bulk downloads)
  Q50. Deep Packet Inspection (DPI): inspect payload, not just headers
  Q51. Traffic shaping vs policing: buffer vs drop excess
  Q52. Network function virtualization (NFV): software firewalls, LBs
  Q53. Software-defined networking (SDN): separate control and data plane
  Q54. eBPF: kernel programmability, network observability, XDP
  Q55. Service mesh data plane: Envoy proxy per pod
  Q56. East-west traffic: service to service within datacenter
  Q57. North-south traffic: client to datacenter
  Q58. Microsegmentation: fine-grained network policy per workload
  Q59. Zero trust network access: authenticate all connections
  Q60. Network observability: flow records, packet capture, metrics

Q61–Q100: Security and monitoring
  Q61. Firewall stateful inspection vs packet filtering
  Q62. IDS vs IPS: detect vs prevent intrusions
  Q63. WAF rule types: signature, behavioral, reputation
  Q64. DDoS mitigation tiers: on-premise, transit, cloud scrubbing
  Q65. Anycast DDoS absorption
  Q66. SYN cookies implementation
  Q67. IP reputation and blocklists
  Q68. Rate limiting at network layer vs application layer
  Q69. SSL/TLS interception and inspection
  Q70. Certificate pinning: trust only specific certificate
  Q71. HPKP (deprecated) vs expect-ct vs certificate pinning
  Q72. DNS hijacking attacks and prevention
  Q73. BGP route hijacking and RPKI
  Q74. ARP spoofing and mitigation
  Q75. Man-in-the-middle attack vectors
  Q76. Network time protocol (NTP) security
  Q77. 802.1X port-based network access control
  Q78. Wi-Fi security: WPA3, enterprise 802.1X
  Q79. Network segmentation for PCI/HIPAA compliance
  Q80. VPC design: public, private, isolated subnets
  Q81. AWS security groups vs NACLs
  Q82. Network flow logs: NetFlow, IPFIX, VPC Flow Logs
  Q83. SNMP for network device monitoring
  Q84. Syslog protocol for centralized logging
  Q85. NetFlow/sFlow for traffic analysis
  Q86. Network packet capture tools: tcpdump, Wireshark, tshark
  Q87. Network performance testing: iperf3, ping, traceroute
  Q88. MTU and jumbo frames: 1500 vs 9000 bytes
  Q89. TCP window scaling for high bandwidth-delay products
  Q90. BBR congestion control algorithm
  Q91. MPTCP: multipath TCP for multiple interfaces
  Q92. QUIC internals: connection IDs, packet coalescing
  Q93. HTTP/3 adoption challenges: UDP blocking in enterprises
  Q94. 5G network slicing: virtual networks for different use cases
  Q95. Edge computing: computation at network edge, not central cloud
  Q96. IoT protocol comparison: MQTT, CoAP, AMQP, HTTP
  Q97. Time-sensitive networking (TSN) for industrial IoT
  Q98. Network automation with Python: Netmiko, NAPALM, Nornir
  Q99. Intent-based networking: describe desired state, system implements
  Q100. Future of networking: AI-driven, autonomous network operations
```

---

## DEEP DIVE: HTTP INTERNALS (Q31-Q50)

**Q31. TCP congestion control — how it works.**
```
TCP uses congestion control to prevent overwhelming the network.

SLOW START:
- Begin with cwnd (congestion window) = 1 MSS (max segment size, ~1460 bytes)
- Each ACK received → cwnd doubles (exponential growth)
- Until cwnd reaches ssthresh (slow start threshold, initially ~64KB)
- Then switch to Congestion Avoidance

CONGESTION AVOIDANCE:
- cwnd increases by 1 MSS per RTT (linear growth)
- Much slower — probing for available bandwidth

CONGESTION DETECTION:
- Packet loss (timeout): ssthresh = cwnd/2, cwnd = 1 MSS, restart slow start
- Triple duplicate ACK (fast retransmit): ssthresh = cwnd/2, cwnd = ssthresh (fast recovery)

BBR (Bottleneck Bandwidth and RTT) — Google's modern algorithm:
- Models the network bottleneck (bandwidth + RTT)
- Doesn't rely on packet loss as signal (loss can happen without congestion)
- Much better throughput on long-distance, high-bandwidth links
- Used by YouTube, deployed in Linux kernel, HTTP/3 (QUIC uses BBR by default)

Practical impact:
- Short connections (most HTTP/1.1): slow start limits throughput
- HTTP/2 multiplexing on one connection: one RTT to build cwnd, amortized across streams
- HTTP/3 with 0-RTT: no slow start penalty for resumed connections
```

**Q32. Nginx — configuration deep dive.**
```nginx
# Production Nginx configuration:
user nginx;
worker_processes auto;           # one per CPU core
worker_rlimit_nofile 65535;      # max open files per worker

events {
    worker_connections 4096;     # connections per worker (total = workers × this)
    multi_accept on;             # accept all pending connections at once
    use epoll;                   # Linux: epoll is fastest
}

http {
    # Basic settings:
    sendfile on;                 # kernel-level file sending (zero-copy)
    tcp_nopush on;               # batch TCP packets (better with sendfile)
    tcp_nodelay on;              # disable Nagle's algorithm (low latency)
    keepalive_timeout 65;        # idle connection timeout
    keepalive_requests 1000;     # max requests per keepalive connection
    types_hash_max_size 2048;
    server_tokens off;           # hide Nginx version

    # Compression:
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    # Rate limiting:
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn:10m;

    # Upstream (backend servers):
    upstream api_backend {
        least_conn;                          # least connections algorithm
        keepalive 32;                        # persistent connections to backend
        server 10.0.1.10:3000 weight=3;
        server 10.0.1.11:3000 weight=3;
        server 10.0.1.12:3000 weight=1 backup; # only used if others fail
        server 10.0.1.13:3000 down;          # manually disabled
    }

    server {
        listen 80;
        server_name api.example.com;
        return 301 https://$server_name$request_uri; # redirect to HTTPS
    }

    server {
        listen 443 ssl http2;
        server_name api.example.com;

        # SSL:
        ssl_certificate     /etc/ssl/certs/api.crt;
        ssl_certificate_key /etc/ssl/private/api.key;
        ssl_protocols       TLSv1.2 TLSv1.3;
        ssl_ciphers         ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;
        ssl_session_cache   shared:SSL:10m;
        ssl_session_timeout 1d;
        ssl_stapling        on;    # OCSP stapling (faster cert validation)
        ssl_stapling_verify on;

        # Security headers:
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header Referrer-Policy strict-origin-when-cross-origin always;

        # Rate limiting:
        limit_req zone=api burst=20 nodelay;
        limit_conn conn 10;

        # Proxy to Node.js:
        location /api/ {
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;      # WebSocket support
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 60s;
            proxy_connect_timeout 5s;
            proxy_buffer_size 128k;
            proxy_buffers 4 256k;
        }

        # Static files — serve directly:
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }

        # Health check (no logging):
        location /health {
            proxy_pass http://api_backend;
            access_log off;
        }
    }
}
```

**Q33. How does a reverse proxy differ from a forward proxy?**
```
FORWARD PROXY (client-side proxy):
- Client → Forward Proxy → Internet
- Client knows about the proxy (configured explicitly)
- Use cases: corporate firewall, content filtering, anonymization, caching
- Server sees proxy IP, not client IP
- Examples: Squid, corporate VPN

REVERSE PROXY (server-side proxy):
- Client → Reverse Proxy → Backend Servers
- Client doesn't know about backend servers (sees one endpoint)
- Use cases: load balancing, SSL termination, caching, WAF, compression
- Client sees one IP (proxy), not backend IPs
- Examples: Nginx, HAProxy, Traefik, Caddy, Envoy

TRANSPARENT PROXY:
- Neither client nor server knows about it
- ISPs use for caching/content filtering
- Intercepts all traffic invisibly

API GATEWAY vs REVERSE PROXY:
- Reverse proxy: routing, SSL, load balancing, caching
- API Gateway: all of above + auth, rate limiting, request transformation, analytics, versioning
- Nginx can act as either, but purpose-built gateways (Kong, AWS API GW) add business logic
```

**Q34. Network address translation (NAT) and how private IPs work.**
```
PRIVATE IP RANGES (RFC 1918):
  10.0.0.0/8         → 10.0.0.0 – 10.255.255.255     (16M addresses)
  172.16.0.0/12      → 172.16.0.0 – 172.31.255.255   (1M addresses)
  192.168.0.0/16     → 192.168.0.0 – 192.168.255.255 (65K addresses)

LOOPBACK: 127.0.0.0/8 (127.0.0.1 = localhost)
LINK-LOCAL: 169.254.0.0/16 (auto-assigned when no DHCP, AWS instance metadata)

NAT (Network Address Translation):
  Private IP:Port → Public IP:Port mapping table maintained by router
  
  Outgoing: 192.168.1.10:54321 → rewrite to 203.0.113.1:41234 → internet
  Incoming: 203.0.113.1:41234 → look up table → forward to 192.168.1.10:54321

SNAT (Source NAT): masquerade private clients with public IP (outbound)
DNAT (Destination NAT): port forwarding — map public port to internal server
  e.g., 203.0.113.1:80 → 192.168.1.20:3000 (port forward to web server)

AWS VPC:
  - Private subnets: no internet access (DB, app servers)
  - Public subnets: internet gateway attached
  - NAT Gateway: private subnet resources can reach internet (outbound only)
  - Elastic IP: static public IP for EC2 instances

CIDR notation: 10.0.0.0/24 = 10.0.0.0 with 256 addresses (10.0.0.0–10.0.0.255)
  /24 = 256 hosts | /16 = 65536 hosts | /8 = 16M hosts | /32 = single host
```

**Q35. HTTP/2 and HTTP/3 implementation details.**
```javascript
// HTTP/2 in Node.js:
import http2 from 'http2';
import fs from 'fs';

const server = http2.createSecureServer({
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem'),
});

server.on('stream', (stream, headers) => {
  const path = headers[':path'];
  const method = headers[':method'];

  // Server Push — push CSS before browser requests it:
  if (path === '/') {
    stream.pushStream({ ':path': '/styles.css' }, (err, pushStream) => {
      if (!err) {
        pushStream.respondWithFile('styles.css', {
          'content-type': 'text/css',
          'cache-control': 'max-age=3600',
        });
      }
    });
  }

  stream.respond({
    ':status': 200,
    'content-type': 'text/html',
  });
  stream.end('<h1>Hello HTTP/2</h1>');
});

server.listen(8443);

// HTTP/3 (QUIC) — Node.js support via quic module (experimental)
// Or use Nginx/Caddy as HTTP/3 termination proxy

// Caddy — automatic HTTPS + HTTP/3:
// Caddyfile:
// api.example.com {
//   reverse_proxy localhost:3000
//   encode zstd gzip
// }
// Caddy automatically obtains Let's Encrypt cert + enables HTTP/3

// Performance testing with h2load:
// h2load -n 10000 -c 100 -m 10 https://api.example.com
// -n: total requests, -c: clients, -m: max concurrent streams per client
```

**Q36. Websocket vs SSE vs Long Polling — detailed comparison.**
```javascript
// LONG POLLING — simulate push with repeated requests
async function longPoll(lastEventId) {
  while (true) {
    const response = await fetch(`/api/events?since=${lastEventId}`, {
      signal: AbortSignal.timeout(30000) // 30s timeout
    });
    if (response.ok) {
      const events = await response.json();
      events.forEach(e => { process(e); lastEventId = e.id; });
    }
    // Immediately request again
  }
}
// Cons: high server load, latency of one request cycle

// SSE — Server-Sent Events (server → client only)
// Server:
app.get('/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no', // disable Nginx buffering
  });

  // Send event:
  const send = (event, data, id) => {
    if (id) res.write(`id: ${id}\n`);
    if (event !== 'message') res.write(`event: ${event}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  // Heartbeat every 15s (prevent proxy timeout):
  const heartbeat = setInterval(() => res.write(': heartbeat\n\n'), 15000);

  send('connected', { userId: req.user.id });

  const unsubscribe = eventBus.subscribe(req.user.id, (event) => {
    send(event.type, event.data, event.id);
  });

  req.on('close', () => { clearInterval(heartbeat); unsubscribe(); });
});

// Client:
const es = new EventSource('/events', { withCredentials: true });
es.onmessage = (e) => console.log(JSON.parse(e.data));
es.addEventListener('order.shipped', (e) => showNotification(JSON.parse(e.data)));
es.onerror = () => { /* browser auto-reconnects with Last-Event-ID header */ };

// SSE advantages over WebSocket:
// - Works over HTTP/1.1, HTTP/2
// - CDN-friendly (can be cached/routed like HTTP)
// - Auto-reconnect built into browser
// - Simpler server (no upgrade, no frame parsing)
// - Multiplexing over HTTP/2 (many SSE streams = one connection)

// WebSocket advantages over SSE:
// - Bidirectional (SSE = server→client only)
// - Binary data support
// - Lower overhead per message after handshake
// - Better for real-time interactive apps (chat, gaming, collaborative editing)
```

**Q37. DNS load balancing and health checking.**
```
DNS LOAD BALANCING:
  Multiple A records for same domain → clients pick one (usually first)
  Simple, but no awareness of server health or load

  api.example.com → [1.2.3.4, 1.2.3.5, 1.2.3.6]

  Round-Robin DNS: each query gets different order (crude load balancing)
  Problem: TTL caching — clients may hit dead server until TTL expires

DNS-BASED GLOBAL LOAD BALANCING:
  Route53 routing policies:
  - Latency-based: route to region with lowest latency for client
  - Geolocation: route based on client's country/continent
  - Weighted: split traffic (90% → v1, 10% → v2 for canary)
  - Failover: primary + secondary, switch if health check fails
  - Multivalue: like round-robin but with health checks per IP

HEALTH CHECKS IN ROUTE53:
  - HTTP check: GET /health → expect 200
  - TCP check: establish TCP connection
  - HTTPS check: TLS + HTTP check
  - Calculated: combine multiple checks with AND/OR logic
  - CloudWatch alarm: based on custom metrics

TTL STRATEGY FOR FAILOVER:
  Normal: TTL=300 (5min) — caches longer, fewer DNS queries
  Pre-failover warning: lower TTL to 60s
  During incident: immediately route away (new queries get new IP)
  Limitation: clients that cached old IP before TTL lowered still affected

ANYCAST DNS:
  Same IP announced from multiple locations via BGP
  User routed to "nearest" (fewest hops) location automatically
  Used by: Cloudflare (1.1.1.1), Google (8.8.8.8), AWS Route53 nameservers
```

**Q38. TCP keepalive vs application-level keepalive.**
```javascript
// TCP KEEPALIVE (OS-level):
// After N seconds of inactivity, OS sends TCP keepalive probes
// Detects dead connections at OS level
// Configured per socket, not per application

import net from 'net';
const socket = new net.Socket();
socket.setKeepAlive(true, 60000); // enable, first probe after 60s
// OS then sends probes every tcp_keepalive_intvl (default 75s)
// After tcp_keepalive_probes (default 9) failures → close connection

// APPLICATION KEEPALIVE (heartbeat):
// WebSocket ping/pong
// HTTP keep-alive header
// Custom heartbeat messages

// HTTP KEEP-ALIVE (connection reuse):
// HTTP/1.1: Connection: keep-alive (default)
// HTTP/1.0: must explicitly request Keep-Alive

// Nginx upstream keepalive:
// Maintains pool of persistent connections to backend
upstream api {
    server localhost:3000;
    keepalive 32;          // pool of 32 idle connections
    keepalive_timeout 60s; // idle connection lifetime
    keepalive_requests 100;// max requests per connection
}

// Node.js HTTP agent keepalive:
import http from 'http';
const agent = new http.Agent({
  keepAlive: true,
  maxSockets: 50,           // max concurrent connections per host
  maxFreeSockets: 10,       // max idle connections in pool
  timeout: 60000,           // socket timeout
  freeSocketTimeout: 30000, // idle socket timeout
});

// All fetch/axios calls share this agent:
fetch(url, { agent });

// WHY KEEPALIVE MATTERS:
// Without: TCP handshake (1 RTT) + TLS handshake (1-2 RTT) per request = 200-400ms overhead
// With:    Reuse existing connection = ~0ms overhead
// For 100 API calls: 20-40s overhead vs negligible
```

**Q39. BGP routing — how the internet routes packets.**
```
BGP (Border Gateway Protocol) = the routing protocol of the internet
- Autonomous Systems (AS): independently administered networks
  (ISPs, cloud providers, companies)
  AWS = AS16509, Cloudflare = AS13335, Google = AS15169
- Each AS has its own IP ranges and routing policies

HOW BGP WORKS:
1. AS peers establish BGP sessions (TCP port 179)
2. Peers exchange: "I can reach these IP prefixes via this path"
3. Each AS selects best path based on: path length, local preference, policy
4. Best paths advertised to peers

PATH SELECTION (simplified):
1. Highest LOCAL_PREF (internal policy)
2. Shortest AS_PATH (fewest hops)
3. Lowest MED (Multi-Exit Discriminator — hint from neighbor)
4. eBGP over iBGP (external over internal)
5. Lowest router ID (tiebreaker)

ANYCAST VIA BGP:
- Same IP block announced from multiple locations
- BGP routes each user to "closest" (fewest AS hops) location
- Used by: Cloudflare, Google, Akamai for global load balancing
- 1.1.1.1 answered by dozens of PoPs, user hits nearest one

BGP SECURITY:
- BGP hijacking: rogue AS announces someone else's IP range
  (Famous: 2008 Pakistan Telecom took down YouTube globally)
- RPKI (Resource Public Key Infrastructure): cryptographic validation
  of route announcements — becoming standard
- BGPsec: digitally signed route path (less deployed)
```

**Q40. Load balancer health checks and circuit breaking.**
```javascript
// Active health check — LB polls backend:
// Nginx Plus:
// health_check interval=5s fails=3 passes=2 uri=/health;
// → check every 5s, mark down after 3 failures, mark up after 2 passes

// Passive health check — based on real traffic:
// Nginx:
upstream api {
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    // Mark server down after 3 failures in 30s:
    // max_fails=3 fail_timeout=30s;
}

// HAProxy health check config:
// backend api_servers
//   option httpchk GET /health HTTP/1.1\r\nHost:\ api.internal
//   http-check expect status 200
//   default-server inter 5s fall 3 rise 2 slowstart 30s

// CIRCUIT BREAKER in load balancer:
// Closed state: pass all requests through
// Open state: immediately reject requests (fast fail)
// Half-open state: allow some requests through to test recovery

class LBCircuitBreaker {
  #state = 'CLOSED';
  #failureCount = 0;
  #lastFailureTime = null;
  #successInHalfOpen = 0;

  constructor({ threshold = 5, timeout = 30000, successThreshold = 2 } = {}) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.successThreshold = successThreshold;
  }

  canRoute() {
    if (this.#state === 'CLOSED') return true;
    if (this.#state === 'OPEN') {
      if (Date.now() - this.#lastFailureTime > this.timeout) {
        this.#state = 'HALF_OPEN';
        this.#successInHalfOpen = 0;
        return true;
      }
      return false; // fast fail
    }
    return true; // HALF_OPEN: allow test requests
  }

  recordSuccess() {
    if (this.#state === 'HALF_OPEN') {
      if (++this.#successInHalfOpen >= this.successThreshold) {
        this.#state = 'CLOSED';
        this.#failureCount = 0;
      }
    }
  }

  recordFailure() {
    this.#failureCount++;
    this.#lastFailureTime = Date.now();
    if (this.#failureCount >= this.threshold || this.#state === 'HALF_OPEN') {
      this.#state = 'OPEN';
    }
  }
}
```

**Q41. WebRTC — peer-to-peer communication.**
```javascript
// WebRTC: browser-to-browser real-time communication
// Used for: video calls, screen sharing, file transfer, peer-to-peer gaming

// SIGNALING (exchanging connection info via your server):
// ICE candidates: possible network paths (local IP, STUN-discovered public IP, TURN relay)
// SDP (Session Description Protocol): codec capabilities, media tracks

const peerConnection = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.example.com:3478' },  // STUN: discover public IP
    {
      urls: 'turn:turn.example.com:3478',     // TURN: relay if direct fails
      username: 'user',
      credential: 'pass',
    },
  ],
});

// CALLER:
// 1. Add local media:
const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));

// 2. Create offer:
const offer = await peerConnection.createOffer();
await peerConnection.setLocalDescription(offer);
signalingServer.send({ type: 'offer', sdp: offer.sdp }); // send via WebSocket

// 3. Handle ICE candidates:
peerConnection.onicecandidate = ({ candidate }) => {
  if (candidate) signalingServer.send({ type: 'ice', candidate });
};

// CALLEE:
signalingServer.on('offer', async ({ sdp }) => {
  await peerConnection.setRemoteDescription({ type: 'offer', sdp });
  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);
  signalingServer.send({ type: 'answer', sdp: answer.sdp });
});

signalingServer.on('ice', ({ candidate }) => {
  peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
});

// STUN: helps client discover its public IP/port (behind NAT)
// TURN: relay server when P2P impossible (symmetric NAT, strict firewall)
//       All traffic routes through TURN server (adds latency, costs bandwidth)
//       ~15-20% of calls need TURN

// Data channels (non-media):
const dataChannel = peerConnection.createDataChannel('chat', { ordered: true });
dataChannel.onmessage = ({ data }) => console.log('Received:', data);
dataChannel.send('Hello peer!');
```

**Q42. How TLS certificates work — CA hierarchy, OCSP, CT.**
```
CERTIFICATE HIERARCHY:
  Root CA → Intermediate CA → Leaf (server) certificate

Why intermediate? 
  - Root CA private key stored OFFLINE (air-gapped, HSM)
  - If intermediate compromised: revoke it without affecting root
  - Multiple intermediates for different purposes/regions

CERTIFICATE CONTENTS:
  - Subject: CN=api.example.com, O=Example Corp, C=US
  - Subject Alternative Names (SAN): api.example.com, *.api.example.com
  - Issuer: DigiCert SHA2 Secure Server CA
  - Valid: 2024-01-01 to 2025-01-01
  - Public key (RSA 2048 or EC P-256)
  - Signature (signed by CA's private key)
  - Serial number (unique per CA)

CERTIFICATE VALIDATION:
1. Chain valid: leaf signed by intermediate, intermediate signed by root
2. Root in trust store (OS/browser built-in list)
3. Not expired
4. Hostname matches (CN or SAN)
5. Not revoked (CRL or OCSP check)

OCSP (Online Certificate Status Protocol):
  Browser → CA's OCSP responder → "Is cert serial #X valid?"
  OCSP Stapling: server fetches and attaches OCSP response to TLS handshake
    → Browser doesn't need to contact CA → faster + more private

CERTIFICATE TRANSPARENCY (CT):
  All public certs must be logged in public CT logs (Chrome requirement since 2018)
  Anyone can monitor logs for misissued certs for their domain
  Certificate Monitoring tools: crt.sh, Facebook CT Monitor, Google's Argon/Xenon logs

CERTIFICATE TYPES:
  DV (Domain Validated): just proves domain ownership (automated, minutes)
  OV (Organization Validated): org identity verified (days)
  EV (Extended Validation): thorough verification (shows org name in browser) - less common now

LET'S ENCRYPT:
  Free, automated DV certificates via ACME protocol
  90-day validity, auto-renewed via Certbot/ACME clients
  Issued 3.5B certificates, used by 50%+ of HTTPS sites
```

**Q43. gRPC connection management and streaming internals.**
```javascript
// gRPC runs over HTTP/2 — each RPC = one HTTP/2 stream
// Multiple RPCs share single TCP connection (multiplexing)

// CLIENT SIDE LOAD BALANCING (preferred over proxy LB for gRPC):
// Why: gRPC connections are long-lived, proxy LB = one backend per connection

// Client-side LB with DNS + round-robin:
import * as grpc from '@grpc/grpc-js';

const client = new UserServiceClient(
  'dns:///api.example.com:50051',  // DNS resolves to multiple IPs
  grpc.credentials.createSsl(),
  {
    'grpc.service_config': JSON.stringify({
      loadBalancingPolicy: 'round_robin',  // or 'grpclb', 'xds'
    }),
    'grpc.keepalive_time_ms': 30000,          // send keepalive every 30s
    'grpc.keepalive_timeout_ms': 10000,        // 10s to respond
    'grpc.keepalive_permit_without_calls': 1,  // keepalive even with no RPCs
    'grpc.initial_reconnect_backoff_ms': 1000,
    'grpc.max_reconnect_backoff_ms': 30000,
    'grpc.http2.max_pings_without_data': 0,
  }
);

// Deadline propagation (cascade timeouts):
const deadline = new Date(Date.now() + 5000); // 5s from now
client.getUser({ id: '123' }, { deadline }, (err, user) => {
  if (err?.code === grpc.status.DEADLINE_EXCEEDED) {
    console.error('Request timed out');
  }
});

// With async/await:
const response = await new Promise((resolve, reject) => {
  client.getUser(
    { id: '123' },
    { deadline: new Date(Date.now() + 5000) },
    (err, res) => err ? reject(err) : resolve(res)
  );
});

// Bidirectional streaming:
const stream = client.chat();

stream.on('data', (message) => displayMessage(message));
stream.on('error', (err) => handleError(err));
stream.on('end', () => console.log('Stream closed'));

// Send messages:
stream.write({ text: 'Hello!', userId: currentUser.id });
stream.write({ text: 'How are you?', userId: currentUser.id });
stream.end(); // signal done sending
```

**Q44. Monitoring network performance.**
```javascript
// Browser Performance API:
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach(entry => {
    if (entry.entryType === 'resource') {
      console.log({
        name: entry.name,
        ttfb: entry.responseStart - entry.requestStart,  // Time to First Byte
        download: entry.responseEnd - entry.responseStart,
        total: entry.duration,
        transferSize: entry.transferSize,
        protocol: entry.nextHopProtocol,  // h2, h3, http/1.1
      });
    }
  });
});
observer.observe({ entryTypes: ['resource', 'navigation', 'paint'] });

// Navigation timing:
const nav = performance.getEntriesByType('navigation')[0];
const metrics = {
  dns:            nav.domainLookupEnd - nav.domainLookupStart,
  tcp:            nav.connectEnd - nav.connectStart,
  tls:            nav.secureConnectionStart > 0 ? nav.connectEnd - nav.secureConnectionStart : 0,
  ttfb:           nav.responseStart - nav.requestStart,
  download:       nav.responseEnd - nav.responseStart,
  domInteractive: nav.domInteractive - nav.fetchStart,
  domComplete:    nav.domComplete - nav.fetchStart,
  loadEvent:      nav.loadEventEnd - nav.fetchStart,
};

// Server-side: track upstream service latency
const start = process.hrtime.bigint();
const response = await fetch('https://upstream-api.com/data');
const latency = Number(process.hrtime.bigint() - start) / 1e6;

metrics.histogram('upstream_latency_ms', latency, {
  service: 'payment-api',
  status: response.status.toString(),
});

// Network quality metrics to track:
// P50, P95, P99 latency by endpoint
// Error rate by status code
// Bytes in/out per endpoint
// Connection pool utilization
// DNS lookup time (indicates DNS health)
// TLS handshake time (indicates cert issues)
```

**Q45-Q100: Advanced networking patterns covered in other files.**
See `iq_12_backend.md` for API patterns, `iq_11_devops.md` for service mesh/Istio, and `iq_06_system_design.md` for distributed system networking patterns.

---

*Enhanced file: now covers TCP congestion control, Nginx config, reverse proxy deep dive, NAT/CIDR, HTTP/2 internals, WebSocket vs SSE comparison, WebRTC, DNS load balancing, BGP routing, TLS certificate hierarchy, gRPC connection management, and network performance monitoring.*
