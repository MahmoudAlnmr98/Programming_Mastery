# The Complete Docker Mastery Guide
> From first principles to production. Architecture, internals, Dockerfile best practices, networking, volumes, Compose, security, and performance. No hand-waving.

---

## Table of Contents
1. [How Docker Works — Architecture & Kernel Primitives](#chapter-1-how-docker-works)
2. [Images — Layers, Cache & Build Internals](#chapter-2-images)
3. [Dockerfile — Every Instruction In Depth](#chapter-3-dockerfile)
4. [Containers — Lifecycle, Runtime & Internals](#chapter-4-containers)
5. [Networking — Bridge, Host, Overlay & DNS](#chapter-5-networking)
6. [Volumes & Storage — Bind Mounts, Named Volumes, tmpfs](#chapter-6-volumes)
7. [Docker Compose — Multi-Container Applications](#chapter-7-compose)
8. [Docker Registry — Push, Pull, Private Registries](#chapter-8-registry)
9. [Security — Rootless, Capabilities, Secrets, Scanning](#chapter-9-security)
10. [Performance — Multi-Stage Builds, Layer Optimization, Build Cache](#chapter-10-performance)
11. [Production Patterns & Troubleshooting](#chapter-11-production)

---

## Chapter 1: How Docker Works

### 1.1 Containers vs Virtual Machines — The Real Difference

Most explanations say "containers are lightweight VMs." That's wrong. They are fundamentally different things.

```
VIRTUAL MACHINE:                    CONTAINER:
┌──────────────┐                    ┌──────────────┐
│  App + Libs  │                    │  App + Libs  │
├──────────────┤                    ├──────────────┤
│  Guest OS    │ ← full OS kernel   │  (no OS)     │
├──────────────┤                    │              │
│  Hypervisor  │                    ├──────────────┤
├──────────────┤                    │  Host OS     │ ← shared kernel
│  Host OS     │                    │  Kernel      │
├──────────────┤                    ├──────────────┤
│  Hardware    │                    │  Hardware    │
└──────────────┘                    └──────────────┘

VM: hardware virtualization — hypervisor emulates hardware for guest OS
Container: process isolation — kernel features isolate a regular process

A container IS a process (or group of processes) on the host, with:
  - Its own view of the filesystem (via namespaces + union FS)
  - Its own view of the network (via network namespace)
  - Its own process tree (via PID namespace)
  - Resource limits enforced by the kernel (via cgroups)
```

### 1.2 Linux Kernel Primitives Docker Uses

Docker is not magic — it's a user-friendly API over existing kernel features:

```
NAMESPACES — isolation (what a container can see):
  PID    → container has its own PID 1, can't see host processes
  NET    → container has its own network stack, interfaces, routing table
  MNT    → container has its own mount points (filesystem view)
  UTS    → container has its own hostname and domain name
  IPC    → container has its own System V IPC, POSIX message queues
  USER   → container has its own UID/GID mapping (user namespaces)
  CGROUP → container has its own cgroup hierarchy view (kernel 4.6+)

CGROUPS (control groups) — resource limits (what a container can USE):
  cpu         → CPU time limits and shares
  memory      → RAM limit, swap limit, OOM kill behavior
  blkio       → disk I/O throttling
  net_cls     → network packet classification for QoS
  pids        → max number of processes

UNION FILESYSTEM (OverlayFS):
  Layers images into a single unified view.
  Read-only layers (image) + thin read-write layer (container).
  Copy-on-write: writes go to the top layer, never modify lower layers.

SECCOMP:
  Filters which syscalls a container can make.
  Default Docker profile blocks ~44 dangerous syscalls.

LINUX CAPABILITIES:
  Break root's all-or-nothing privilege into fine-grained capabilities.
  Docker drops most capabilities by default (see Chapter 9).
```

### 1.3 Docker Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Docker CLI (docker run, docker build, docker ps ...)   │
└──────────────────────────┬──────────────────────────────┘
                           │ REST API (Unix socket: /var/run/docker.sock)
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Docker Daemon (dockerd)                                │
│  - API server                                           │
│  - Image management                                     │
│  - Network management                                   │
│  - Volume management                                    │
└──────────────────────────┬──────────────────────────────┘
                           │ gRPC
                           ▼
┌─────────────────────────────────────────────────────────┐
│  containerd                                             │
│  - Container lifecycle management                       │
│  - Image pull/push                                      │
│  - Snapshot management                                  │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  runc (OCI runtime)                                     │
│  - Actually creates the container (calls clone(), etc.) │
│  - Sets up namespaces and cgroups                       │
│  - Executes the container process                       │
└─────────────────────────────────────────────────────────┘

KEY INSIGHT: runc is the actual container runtime. containerd manages it.
dockerd manages containerd. docker CLI talks to dockerd.
Kubernetes can use containerd directly (bypassing dockerd entirely).
```

---

## Chapter 2: Images — Layers, Cache & Build Internals

### 2.1 Image Layers

```
Every image is a stack of read-only layers.
Each layer = the filesystem diff from the previous layer.
Layers are identified by a SHA256 content hash.

DOCKERFILE:                    LAYER STACK:
FROM ubuntu:22.04          →   Layer 0: ubuntu:22.04 base (50MB)
RUN apt-get install curl   →   Layer 1: +curl package files (2MB)
RUN apt-get install git    →   Layer 2: +git package files (4MB)
COPY app/ /app             →   Layer 3: +your app files (1MB)
                               ─────────────────────────────────
                               Total image: 57MB

SHARING LAYERS:
  If two images share FROM ubuntu:22.04, that layer is stored ONCE on disk.
  Docker pulls only layers it doesn't already have.
  This is why: docker pull is fast after first pull of a base image.

CONTAINER LAYER:
  When you run a container, Docker adds a thin writable layer on top.
  All writes go here. Container deletion removes this layer.
  Image layers below are untouched (read-only forever).

  ubuntu:22.04 image layers (read-only, shared)
  ┌─────────────────────────────────┐
  │  Layer 3: your app              │ read-only
  │  Layer 2: git                   │ read-only
  │  Layer 1: curl                  │ read-only
  │  Layer 0: ubuntu base           │ read-only
  └─────────────────────────────────┘
  ┌─────────────────────────────────┐
  │  Container write layer          │ read-write (per container)
  └─────────────────────────────────┘

COPY-ON-WRITE (CoW):
  If a container modifies /etc/hosts (which exists in a lower layer):
  1. Docker copies /etc/hosts UP to the container layer
  2. The copy in the container layer is modified
  3. Lower layers are untouched
  This means: reading unmodified files reads from lower layers (fast).
  Writing or modifying: copies first (one-time cost), then writes.
```

### 2.2 Layer Cache

```
Docker caches each layer. If a layer's inputs haven't changed,
Docker reuses the cached layer instead of re-running the instruction.

CACHE INVALIDATION RULES:
  - FROM:   cache valid if base image hasn't changed
  - RUN:    cache valid if the EXACT command string hasn't changed
  - COPY/ADD: cache valid if the file content hash hasn't changed
  - Any layer cache miss → ALL subsequent layers are invalidated

WHY ORDER MATTERS:
  Bad Dockerfile (cache busted on every code change):
    FROM node:20
    COPY . .               ← copies ALL files including source code
    RUN npm install        ← runs every time because COPY above changed

  Good Dockerfile (npm install cached unless package.json changes):
    FROM node:20
    COPY package*.json ./  ← only copy dependency manifests
    RUN npm install        ← cached unless package*.json changed
    COPY . .               ← copy source code (changes frequently, OK at end)

RULE: Put instructions that change rarely at the TOP.
      Put instructions that change frequently at the BOTTOM.
      This maximizes cache hits → faster builds.
```

---

## Chapter 3: Dockerfile — Every Instruction In Depth

### 3.1 FROM

```dockerfile
# Syntax
FROM <image>[:<tag>] [AS <name>]

FROM ubuntu:22.04          # specific version tag (reproducible)
FROM ubuntu:latest         # floating tag (not reproducible — avoid in production)
FROM ubuntu@sha256:abc123  # digest pin — 100% reproducible, immune to tag changes

# Multi-stage build: name stages for reference
FROM node:20 AS builder
FROM nginx:alpine AS production

# Scratch — empty image for static binaries
FROM scratch
COPY myapp /myapp
ENTRYPOINT ["/myapp"]
# Smallest possible image: just your binary. No shell, no OS files.

# KEY INSIGHT: Always pin to specific versions in production.
# "latest" can change and break your build silently.
```

### 3.2 RUN

```dockerfile
# Shell form — spawns /bin/sh -c, supports variables/pipes/redirection
RUN apt-get update && apt-get install -y curl

# Exec form — no shell, no variable expansion, direct exec
RUN ["apt-get", "install", "-y", "curl"]

# BEST PRACTICE: Chain commands with && to minimize layers
# Bad: 3 layers, each package manager state cached separately
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

# Good: 1 layer, update + install + cleanup atomic
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       git \
    && rm -rf /var/lib/apt/lists/*
# --no-install-recommends: skip optional recommended packages (smaller image)
# rm -rf /var/lib/apt/lists/*: remove apt cache (not needed after install)
# These MUST be in the same RUN — separate RUN can't delete previous layer's files

# Build arguments available at build time:
ARG VERSION=1.0
RUN curl -O https://example.com/app-${VERSION}.tar.gz

# Heredoc (Docker 1.4+ BuildKit):
RUN <<EOF
apt-get update
apt-get install -y curl git
rm -rf /var/lib/apt/lists/*
EOF
```

### 3.3 CMD vs ENTRYPOINT

```dockerfile
# The interaction is often confusing. Here's the complete model:

# CMD — default command or default arguments
# ENTRYPOINT — the fixed executable (always runs)

# EXEC FORM (recommended): ["executable", "arg1", "arg2"]
# Signals delivered directly to process (no shell intermediary)
# PID 1 = your process

# SHELL FORM: command arg1 arg2
# Runs as: /bin/sh -c "command arg1 arg2"
# PID 1 = /bin/sh — signals may not reach your app!
# NEVER use shell form for ENTRYPOINT

# SCENARIO 1: CMD only (no ENTRYPOINT)
CMD ["node", "app.js"]
# docker run myimage           → node app.js
# docker run myimage python3   → python3  (CMD is REPLACED)

# SCENARIO 2: ENTRYPOINT only
ENTRYPOINT ["node", "app.js"]
# docker run myimage           → node app.js
# docker run myimage --port=3000 → node app.js --port=3000 (APPENDED)
# docker run --entrypoint="" myimage → override ENTRYPOINT

# SCENARIO 3: ENTRYPOINT + CMD (most flexible pattern)
ENTRYPOINT ["node"]
CMD ["app.js"]
# docker run myimage           → node app.js
# docker run myimage server.js → node server.js  (CMD replaced, ENTRYPOINT kept)

# PRODUCTION PATTERN: entrypoint script
# entrypoint.sh:
#!/bin/sh
set -e
# Run init tasks (migrations, env setup...)
if [ "$RUN_MIGRATIONS" = "true" ]; then
  node dist/migrate.js
fi
exec "$@"          # exec replaces shell with CMD — signals propagate correctly

ENTRYPOINT ["/entrypoint.sh"]
CMD ["node", "dist/main.js"]
```

### 3.4 COPY vs ADD

```dockerfile
# COPY — simple file copy (PREFERRED)
COPY src/ /app/src/
COPY package*.json ./

# ADD — superset of COPY (use only when you specifically need its extras)
ADD https://example.com/file.tar.gz /tmp/   # fetches remote URL (COPY can't)
ADD archive.tar.gz /app/                     # auto-extracts tar (COPY doesn't)

# BEST PRACTICE: Use COPY unless you specifically need ADD's URL/extract features.
# ADD from URL is hard to cache-bust and hard to verify. Use RUN curl instead:
RUN curl -fsSL https://example.com/file.tar.gz | tar -xz -C /app/

# COPY with --chown (avoid separate RUN chown — saves a layer)
COPY --chown=node:node app/ /app/

# COPY from another build stage (multi-stage)
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
```

### 3.5 ENV, ARG, and Variable Scoping

```dockerfile
# ARG — build-time variable only (not available in final image)
ARG NODE_VERSION=20
ARG BUILD_DATE
FROM node:${NODE_VERSION}

# ARG after FROM — scoped to that build stage
FROM node:20 AS builder
ARG NPM_TOKEN           # cleared after stage ends

# ENV — runtime environment variable (persists in image and container)
ENV NODE_ENV=production
ENV PORT=3000
ENV DB_HOST=localhost DB_PORT=5432   # multiple on one line

# Use ENV value in subsequent instructions:
ENV APP_DIR=/app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}

# SECURITY: Never put secrets in ENV or ARG — they appear in docker history
# Bad:
ENV DB_PASSWORD=supersecret   # visible in docker inspect and docker history

# Good: inject at runtime
# docker run -e DB_PASSWORD=secret myimage
# Or: use Docker secrets (see Chapter 9)

# ARG vs ENV scope:
ARG BUILD_ARG=value   # exists only during build, not at runtime
ENV RUNTIME_VAR=value # exists at runtime, visible in containers and docker inspect
```

### 3.6 WORKDIR, USER, EXPOSE, HEALTHCHECK

```dockerfile
# WORKDIR — set working directory (creates if doesn't exist)
WORKDIR /app
# Prefer over: RUN mkdir /app && cd /app (WORKDIR is cleaner and tracked)
# All subsequent COPY, RUN, CMD, ENTRYPOINT use this directory as base

# USER — switch to non-root user (security critical)
# Create user first:
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser
USER appuser
# Or for Alpine:
RUN addgroup -g 1001 appgroup && adduser -D -u 1001 -G appgroup appuser
USER appuser

# EXPOSE — documents which ports the container listens on (metadata only)
EXPOSE 3000
EXPOSE 8080/tcp
EXPOSE 9090/udp
# Does NOT actually publish ports — that's docker run -p 3000:3000

# HEALTHCHECK — lets Docker monitor container health
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
# interval: time between checks
# timeout: check must complete within this time
# start-period: grace period before checks start (for slow startup)
# retries: consecutive failures before "unhealthy"
# exit 0 = healthy, exit 1 = unhealthy

# HEALTHCHECK NONE — disable inherited healthcheck from base image
HEALTHCHECK NONE
```

### 3.7 Multi-Stage Builds

```dockerfile
# Multi-stage builds: separate build environment from runtime environment.
# Only the final stage ends up in the image — build tools stay out.

# ─── STAGE 1: Build ───────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app

# Install ALL dependencies (including devDependencies)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build
# Output: /app/dist

# ─── STAGE 2: Production ─────────────────────────────
FROM node:20-alpine AS production
WORKDIR /app

# Install ONLY production dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy only the built output from builder stage
COPY --from=builder /app/dist ./dist

# Non-root user
RUN addgroup -g 1001 appgroup && adduser -D -u 1001 -G appgroup appuser
USER appuser

EXPOSE 3000
CMD ["node", "dist/main.js"]

# RESULT:
# builder stage: node:20-alpine + all devDeps + source + build tools
# production image: node:20-alpine + prod deps + dist only
# Typical savings: 500MB → 80MB

# ─── LANGUAGE-SPECIFIC EXAMPLES ───────────────────────

# Go binary — smallest possible
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server .

FROM scratch AS production
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
ENTRYPOINT ["/server"]
# Image size: ~15MB (just the binary + CA certs)

# Java (with jlink for minimal JRE)
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./mvnw package -DskipTests

FROM eclipse-temurin:21-jre AS production
WORKDIR /app
COPY --from=builder /app/target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Chapter 4: Containers — Lifecycle, Runtime & Internals

### 4.1 Container Lifecycle

```
docker create  → allocates resources, creates writable layer — NOT started
docker start   → starts the container process
docker run     → create + start combined (most common)
docker pause   → freezes all processes (SIGSTOP) — no CPU used
docker unpause → resumes (SIGCONT)
docker stop    → sends SIGTERM, waits 10s, then SIGKILL (graceful)
docker kill    → sends SIGKILL immediately (forceful)
docker restart → stop + start
docker rm      → remove stopped container (rm -f to remove running)

STATES:
  created   → created but not started
  running   → process is running
  paused    → process is frozen
  exited    → process has stopped (exit code stored)
  dead      → container couldn't be removed (partial failure)

IMPORTANT: `docker stop` sends SIGTERM first.
Your app MUST handle SIGTERM for graceful shutdown:
  process.on('SIGTERM', () => {
    server.close(() => { db.disconnect(); process.exit(0); });
  });
If SIGTERM is not handled within --stop-timeout (default 10s): SIGKILL.
SIGKILL cannot be caught — process dies immediately (potential data loss).
```

### 4.2 docker run — Key Flags

```bash
# Basic run
docker run nginx:alpine

# Detached (background)
docker run -d nginx:alpine

# Name the container
docker run -d --name webserver nginx:alpine

# Port mapping: host:container
docker run -d -p 8080:80 nginx:alpine       # specific port
docker run -d -p 127.0.0.1:8080:80 nginx   # bind to specific host IP
docker run -d -P nginx:alpine               # auto-assign host ports for all EXPOSE'd ports

# Environment variables
docker run -e NODE_ENV=production -e PORT=3000 myapp
docker run --env-file .env myapp            # from file

# Volume mounts
docker run -v myvolume:/app/data myapp      # named volume
docker run -v $(pwd)/data:/app/data myapp   # bind mount (host path)
docker run --mount type=tmpfs,dst=/tmp myapp # tmpfs in memory

# Resource limits
docker run --memory=512m myapp              # 512MB RAM limit
docker run --memory=512m --memory-swap=1g myapp  # RAM + swap
docker run --cpus=1.5 myapp                 # 1.5 CPU cores
docker run --cpu-shares=512 myapp           # relative CPU weight

# Network
docker run --network=host myapp             # host networking
docker run --network=mynet myapp            # custom network
docker run --network=none myapp             # no networking

# Remove after exit
docker run --rm myapp                       # auto-remove when stopped

# Interactive (for debugging)
docker run -it --rm ubuntu:22.04 bash       # -i = stdin, -t = TTY

# Security
docker run --read-only myapp                # read-only filesystem
docker run --user 1001:1001 myapp           # run as specific UID:GID
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp

# Init process (proper PID 1)
docker run --init myapp                     # runs tini as PID 1 (handles zombie reaping)
```

### 4.3 Container Resource Limits & cgroups

```
MEMORY:
  --memory=512m             → hard limit (OOM kill if exceeded)
  --memory-reservation=256m → soft limit (hint to kernel under pressure)
  --memory-swap=1g          → total memory+swap (set = memory to disable swap)
  --oom-kill-disable        → disable OOM killer (use with care)

  OOM Kill: if container exceeds --memory, Linux OOM killer terminates it.
  Container exits with code 137 (SIGKILL = 9, 128+9 = 137)
  Kubernetes equivalent: OOMKilled status

CPU:
  --cpus=2.0                → limit to 2.0 CPU cores (hard limit)
  --cpu-shares=1024         → relative weight (only relevant under contention)
                              Default 1024. Container with 2048 gets 2x CPU time.
  --cpuset-cpus=0,1         → pin to specific CPU cores

PIDS:
  --pids-limit=100          → max number of processes in container

MONITORING resources:
  docker stats mycontainer   # live CPU, memory, I/O, net stats
  docker stats --no-stream   # snapshot
```

---

## Chapter 5: Networking

### 5.1 Network Drivers

```
BRIDGE (default for standalone containers):
  Creates a virtual ethernet bridge on the host (docker0).
  Containers on same bridge can communicate via IP.
  Containers on custom bridge can communicate via DNS name.
  NAT for external connectivity.

  docker network create mynet    # creates custom bridge
  docker run --network mynet myapp

HOST:
  Container shares the host's network stack directly.
  No network isolation. Container's ports = host's ports.
  Best performance (no NAT overhead).
  Useful for: network-intensive apps, Kubernetes node-local services.
  docker run --network host myapp

NONE:
  No network interfaces (only loopback).
  Completely isolated from network.
  For: batch processing, offline workloads.

OVERLAY (Swarm/multi-host):
  Creates a distributed network spanning multiple Docker hosts.
  Uses VXLAN encapsulation.
  Required for Docker Swarm services.

MACVLAN:
  Assigns a MAC address to the container, making it appear as a physical device.
  Container gets IP directly from the physical network (no NAT).
  For: legacy apps that need to be on the LAN, network monitoring.

IPVLAN:
  Similar to macvlan but shares the host's MAC address.
  Two modes: L2 (like macvlan) and L3 (routing-based).
```

### 5.2 DNS in Docker

```
DEFAULT BRIDGE (docker0):
  Containers communicate by IP only.
  No automatic DNS resolution by container name.
  --link flag (legacy): adds host entry but deprecated.

CUSTOM BRIDGE NETWORK:
  Docker runs an embedded DNS server at 127.0.0.11.
  Containers on the same custom network can resolve each other by NAME.
  
  docker network create mynet
  docker run -d --network mynet --name db postgres
  docker run -d --network mynet --name app myapp
  # app container can reach db at hostname "db"
  # Inside app: psql -h db -U postgres

COMPOSE NETWORKS:
  Docker Compose creates a custom bridge per project by default.
  Service names become DNS hostnames automatically.
  services:
    api:
      ...   # reachable as "api" from other services
    db:
      ...   # reachable as "db" from other services

DNS RESOLUTION ORDER (inside container):
  1. Docker embedded DNS (127.0.0.11) — container names, service names
  2. Host's DNS (from /etc/resolv.conf)
  3. External DNS
```

### 5.3 Port Mapping & iptables

```
docker run -p 8080:80 nginx

WHAT HAPPENS:
  Docker adds iptables NAT rules to redirect host:8080 → container:80.
  
  iptables -t nat -L DOCKER
  → DNAT rule: tcp dpt:8080 → container_ip:80

  Incoming request to host:8080
  → iptables PREROUTING → DNAT to container_ip:80
  → veth pair → container's eth0:80

IMPORTANT:
  -p 8080:80      → binds to 0.0.0.0:8080 (all interfaces — publicly accessible!)
  -p 127.0.0.1:8080:80 → binds to localhost only (safer for dev)
  
  Even if you have a firewall (ufw, firewalld), Docker bypasses it
  by inserting rules in the DOCKER-USER chain BEFORE the firewall rules.
  This is a common security surprise.
```

---

## Chapter 6: Volumes & Storage

### 6.1 Storage Types

```
NAMED VOLUMES (recommended for persistent data):
  Managed by Docker. Stored at /var/lib/docker/volumes/<name>/.
  Survive container deletion. Can be shared between containers.
  Can use volume drivers for cloud storage (AWS EBS, NFS, etc.).

  docker volume create mydata
  docker run -v mydata:/app/data myapp
  docker volume ls
  docker volume inspect mydata
  docker volume rm mydata

BIND MOUNTS:
  Mount a host path into the container.
  Full two-way sync: changes in container appear on host and vice versa.
  Used for: development (live code reload), config files, logs.

  docker run -v $(pwd)/src:/app/src myapp  # absolute path required
  # or --mount syntax (explicit, no ambiguity):
  docker run --mount type=bind,src=$(pwd)/src,dst=/app/src myapp

TMPFS MOUNTS:
  Stored in host memory. Never written to disk.
  For: temporary files, secrets that shouldn't touch disk.
  
  docker run --mount type=tmpfs,dst=/tmp,tmpfs-size=100m myapp

ANONYMOUS VOLUMES:
  Created by VOLUME instruction in Dockerfile.
  Managed by Docker. Random name. NOT shared by default.
  Persist after container removal (must manually clean up).
```

### 6.2 VOLUME in Dockerfile

```dockerfile
VOLUME ["/app/data"]
# Creates an anonymous volume at /app/data when container starts.
# Data written here persists after container stops.
# Even if you DON'T pass -v, Docker creates an anonymous volume.
# This prevents data loss from writing to the container layer.

# Use case: database containers
FROM postgres:16
VOLUME /var/lib/postgresql/data
# Ensures DB files are always on a volume, never in the container layer.

# IMPORTANT:
# VOLUME instruction only affects image metadata.
# Anything COPY'd or RUN'd after VOLUME won't write to the volume path.
# Volume is mounted AFTER the image is built.

# To pre-populate a volume:
COPY seed-data/ /app/data/   # This works — BEFORE VOLUME
VOLUME /app/data             # Mount point defined AFTER population
```

---

## Chapter 7: Docker Compose

### 7.1 Compose File Structure

```yaml
# docker-compose.yml — complete reference

version: "3.9"  # Compose file format version (optional in recent Docker)

services:
  # ── Service definition ──────────────────────────────────
  api:
    image: myapp:latest                   # use pre-built image
    build:                                # OR build from Dockerfile
      context: ./api                      # build context directory
      dockerfile: Dockerfile.prod         # specific Dockerfile
      args:                               # build arguments
        NODE_VERSION: "20"
      target: production                  # multi-stage target
      cache_from:                         # cache sources for CI
        - myapp:latest

    container_name: api_server            # fixed name (use with care in swarm)
    hostname: api                         # container hostname

    ports:
      - "3000:3000"                       # host:container
      - "127.0.0.1:3000:3000"            # bind to localhost only

    environment:
      NODE_ENV: production
      PORT: 3000
    env_file:
      - .env                              # load from file

    volumes:
      - ./logs:/app/logs                  # bind mount
      - appdata:/app/data                 # named volume

    networks:
      - frontend
      - backend

    depends_on:
      db:
        condition: service_healthy        # wait for db to be healthy

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

    restart: unless-stopped              # always|on-failure|unless-stopped|no

    deploy:                              # Swarm mode (docker stack deploy)
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password  # Docker secret
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 10

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    networks:
      - frontend
    depends_on:
      - api

volumes:
  pgdata:                               # named volume (Docker-managed)
  appdata:
    external: true                      # pre-existing volume (don't auto-create)

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true                      # no external connectivity (db isolation)

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 7.2 Compose Commands

```bash
# Start services (build if needed, detached)
docker compose up -d --build

# Start specific service
docker compose up -d db

# Stop and remove containers (keep volumes)
docker compose down

# Stop and remove containers AND volumes
docker compose down -v

# Scale a service
docker compose up -d --scale api=3

# View logs
docker compose logs -f api        # follow logs for api service
docker compose logs --tail=50

# Execute command in running service
docker compose exec api sh
docker compose exec db psql -U user myapp

# Run one-off command (new container, removed after)
docker compose run --rm api npm run migrate

# View status
docker compose ps

# Rebuild image without cache
docker compose build --no-cache api

# Override with additional compose file
docker compose -f docker-compose.yml -f docker-compose.override.yml up

# PROFILES — conditional services
docker compose --profile debug up     # starts services with profile: debug
```

### 7.3 Override Files Pattern

```yaml
# docker-compose.yml (base — used in all environments)
services:
  api:
    image: myapp:${TAG:-latest}
    environment:
      NODE_ENV: production

# docker-compose.override.yml (dev — auto-loaded by docker compose)
services:
  api:
    build: .            # build locally in dev
    environment:
      NODE_ENV: development
    volumes:
      - .:/app          # live reload
    ports:
      - "9229:9229"     # debug port

# docker-compose.prod.yml (production — explicit)
# docker compose -f docker-compose.yml -f docker-compose.prod.yml up
services:
  api:
    deploy:
      replicas: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Chapter 8: Docker Registry

### 8.1 Image Naming & Tagging

```
IMAGE NAME FORMAT:
  [registry/][namespace/]name[:tag][@digest]

  nginx                               → docker.io/library/nginx:latest
  nginx:1.25                          → docker.io/library/nginx:1.25
  myuser/myapp:v1.2.3                → docker.io/myuser/myapp:v1.2.3
  ghcr.io/myorg/myapp:latest         → GitHub Container Registry
  123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest → AWS ECR

TAGGING STRATEGY:
  :latest          → always points to most recent (floating — use carefully)
  :v1.2.3          → semantic version (immutable — preferred)
  :main-a3b4c5d    → branch + git SHA (traceable)
  :20240115        → date-based (for daily builds)
  
  docker build -t myapp:v1.2.3 -t myapp:latest .
  docker push myapp:v1.2.3
  docker push myapp:latest
```

### 8.2 Registry Operations

```bash
# Login
docker login                           # Docker Hub
docker login ghcr.io -u USERNAME       # GitHub CR
aws ecr get-login-password | docker login --username AWS --password-stdin <ecr-url>

# Build and push
docker build -t myregistry/myapp:v1 .
docker push myregistry/myapp:v1

# Pull
docker pull myregistry/myapp:v1

# Inspect without pulling (manifest)
docker manifest inspect myregistry/myapp:v1

# Copy between registries (crane tool)
crane copy source/image:tag dest/image:tag

# List tags (Docker Hub API)
curl -s "https://hub.docker.com/v2/repositories/library/nginx/tags/?page_size=10"

# Multi-platform build and push (BuildKit)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:v1 \
  --push .
```

---

## Chapter 9: Security

### 9.1 Run as Non-Root

```dockerfile
# The single most impactful security improvement.
# By default, Docker containers run as root (UID 0).
# If attacker escapes container AND process is root: host root access.

# Create user in Dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 appgroup \
    && adduser -D -u 1001 -G appgroup appuser

# Set permissions BEFORE switching user
COPY --chown=appuser:appgroup . /app
WORKDIR /app

USER appuser  # all subsequent instructions and container process runs as this user

# VERIFY: docker run --rm myapp id
# Should show: uid=1001(appuser) gid=1001(appgroup)

# Root-required operations (e.g., bind to port < 1024):
# Option 1: Use a port >= 1024 (e.g., 8080 instead of 80)
# Option 2: CAP_NET_BIND_SERVICE capability
# Option 3: Use a reverse proxy (nginx/traefik) to handle 80/443
```

### 9.2 Linux Capabilities

```bash
# Linux capabilities break root privilege into ~40 fine-grained capabilities.
# Docker drops many by default. Add ONLY what you need.

# Docker DEFAULT dropped capabilities:
# AUDIT_WRITE, CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL, MKNOD,
# NET_BIND_SERVICE, NET_RAW, SETFCAP, SETGID, SETPCAP, SETUID, SYS_CHROOT

# Drop ALL and add only what's needed:
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp
docker run --cap-drop ALL --cap-add CHOWN myapp

# Common capabilities and why you'd need them:
# NET_BIND_SERVICE → bind to ports < 1024
# CHOWN           → change file ownership
# NET_ADMIN       → network configuration (iptables, routing)
# SYS_PTRACE      → debug with strace/gdb (dev only)
# SYS_ADMIN       → broad admin (almost never needed, very dangerous)

# --privileged → gives ALL capabilities + access to ALL devices
# NEVER use --privileged in production unless absolutely necessary.
# Effectively bypasses all container isolation.
```

### 9.3 Read-Only Filesystem

```bash
# Prevent container filesystem writes:
docker run --read-only myapp

# Usually breaks things — add writable paths explicitly:
docker run --read-only \
  --tmpfs /tmp:rw,size=100m \    # writable tmpfs for temp files
  --tmpfs /var/run:rw,size=10m \ # writable for PID files
  -v myapp-logs:/app/logs \      # named volume for logs
  myapp

# In Compose:
services:
  api:
    read_only: true
    tmpfs:
      - /tmp:size=100m
    volumes:
      - logs:/app/logs
```

### 9.4 Secrets Management

```bash
# NEVER put secrets in:
# - ENV instructions in Dockerfile (visible in docker history)
# - ARG instructions (visible in build cache)
# - Environment variables passed on command line (visible in ps aux)

# OPTION 1: Environment variables at runtime (ok for non-sensitive)
docker run -e DB_HOST=localhost myapp

# OPTION 2: Docker secrets (Swarm mode)
echo "mysecretpassword" | docker secret create db_password -
# In compose:
services:
  db:
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
secrets:
  db_password:
    external: true
# Secret file is available at /run/secrets/<name> — tmpfs, not on disk

# OPTION 3: BuildKit --secret (build-time secrets, not in image)
# Build:
docker build --secret id=npmtoken,src=.npmrc .
# Dockerfile:
RUN --mount=type=secret,id=npmtoken \
    NPM_TOKEN=$(cat /run/secrets/npmtoken) npm install
# Secret NOT stored in image layers

# OPTION 4: External secret managers
# HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager
# App fetches secrets at startup from vault/AWS/GCP API.
```

### 9.5 Image Scanning

```bash
# Scan for CVEs in image layers
docker scout cves myapp:latest        # Docker Scout (built-in)
trivy image myapp:latest              # Trivy (open source, excellent)
grype myapp:latest                    # Grype (Anchore, popular in CI)
snyk container test myapp:latest      # Snyk (commercial)

# Trivy in CI pipeline:
trivy image \
  --exit-code 1 \              # fail pipeline if vulnerabilities found
  --severity CRITICAL,HIGH \   # only fail on high/critical
  --no-progress \
  myapp:${TAG}

# SBOM — Software Bill of Materials
docker sbom myapp:latest              # generate SBOM
syft myapp:latest -o json > sbom.json # Syft tool

# Lint Dockerfiles for best practices:
hadolint Dockerfile                   # Haskell Dockerfile Linter
```

---

## Chapter 10: Performance & Optimization

### 10.1 Build Performance

```bash
# BuildKit — Docker's next-gen build system (default in Docker 23+)
export DOCKER_BUILDKIT=1  # older Docker
# or: BUILDKIT_INLINE_CACHE=1 for cache embedding

# Parallel stage builds
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:v1 .

# Build cache from registry (CI/CD cache)
docker build \
  --cache-from myapp:cache \      # use remote image as cache source
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t myapp:latest \
  -t myapp:cache \
  .

# GitHub Actions cache
# Use: actions/cache + --cache-from type=gha

# .dockerignore — exclude files from build context
cat .dockerignore
node_modules/
.git/
.env
*.log
dist/
coverage/
README.md
# Build context sent to daemon — large context = slow build. Always have .dockerignore.
```

### 10.2 Image Size Optimization

```
TECHNIQUES FOR SMALL IMAGES:

1. Choose minimal base images:
   ubuntu:22.04     → 78MB
   debian:slim      → 74MB
   alpine:3.19      → 7MB    ← smallest general-purpose
   distroless       → ~2MB   ← no shell, no package manager
   scratch          → 0MB    ← for static binaries only

2. Multi-stage builds (Chapter 3.7) — biggest single win

3. Combine RUN commands with && (Chapter 3.2) — reduces layers

4. Remove package manager caches in same RUN:
   RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
   RUN apk add --no-cache curl  # Alpine: --no-cache skips cache entirely

5. Use --no-install-recommends:
   apt-get install -y --no-install-recommends curl

6. Copy only what you need (multi-stage: only copy build artifacts)

7. Use .dockerignore to exclude large unnecessary files

8. For Node.js: npm ci --only=production OR npm prune --production after build

MEASURING:
   docker images myapp                     # image size
   docker history myapp                    # size per layer
   dive myapp                              # interactive layer explorer (tool)
```

---

## Chapter 11: Production Patterns & Troubleshooting

### 11.1 Logging Best Practices

```bash
# Docker log drivers
docker run --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp

# Log drivers: json-file (default), journald, syslog, gelf, fluentd, awslogs, gcplogs

# BEST PRACTICE: Log to stdout/stderr from your app.
# Docker captures stdout/stderr automatically.
# NEVER log to files inside the container (use volumes if needed).

# View logs:
docker logs mycontainer
docker logs -f mycontainer     # follow
docker logs --tail 100 mycontainer
docker logs --since 1h mycontainer
docker logs --since 2024-01-15T14:00:00 mycontainer

# In production: ship logs to centralized system:
# docker run --log-driver=fluentd myapp   → Fluentd → Elasticsearch
# docker run --log-driver=awslogs myapp   → CloudWatch Logs
```

### 11.2 Debugging Containers

```bash
# Execute command in running container
docker exec -it mycontainer sh
docker exec mycontainer cat /etc/hosts
docker exec mycontainer env

# Inspect container details
docker inspect mycontainer                      # full JSON config
docker inspect -f '{{.NetworkSettings.IPAddress}}' mycontainer
docker inspect -f '{{.State.Status}}' mycontainer

# Copy files to/from container
docker cp mycontainer:/app/logs/error.log .     # copy out
docker cp ./config.json mycontainer:/app/       # copy in

# Resource usage
docker stats                           # all containers, live
docker stats --no-stream mycontainer   # snapshot

# View processes inside container
docker top mycontainer

# Container events
docker events --since 1h               # stream of Docker events

# Debug a STOPPED container (run new container with same image)
docker run --rm -it --entrypoint sh myapp

# Debug production container without shell:
# Use distroless debug variants:
FROM gcr.io/distroless/nodejs:debug AS debug
# Has busybox shell for debugging

# nsenter — enter container namespaces from host
PID=$(docker inspect -f '{{.State.Pid}}' mycontainer)
nsenter -t $PID -n ip addr  # see container's network namespace from host
```

### 11.3 Production Checklist

```
IMAGE:
  ✓ Non-root USER set
  ✓ Multi-stage build (minimal final image)
  ✓ Pinned base image version (not latest)
  ✓ .dockerignore present
  ✓ HEALTHCHECK defined
  ✓ Image scanned for CVEs (trivy/grype)
  ✓ Image size checked (dive)

RUNTIME:
  ✓ Resource limits set (--memory, --cpus)
  ✓ Restart policy set (--restart unless-stopped)
  ✓ Read-only filesystem where possible
  ✓ Capabilities dropped (--cap-drop ALL, add only needed)
  ✓ No --privileged
  ✓ Secrets via env at runtime or Docker secrets (not baked in)
  ✓ Logs to stdout/stderr (not files)
  ✓ Graceful shutdown handled (SIGTERM handler)

NETWORKING:
  ✓ Ports bound to 127.0.0.1 where not publicly needed
  ✓ Custom networks (not default bridge)
  ✓ Internal networks for DB/cache (no external connectivity)
```

---

*End of Docker Mastery Guide*
