# DevOps — Interview Questions & Answers (Premium Reference)
> 160 questions. Full answers with code. Docker, Kubernetes, CI/CD, IaC, Cloud/AWS, Observability, Security. Every question answered in full — no stubs.

---

## Table of Contents
- [Section 1: Docker (Q1–Q30)](#section-1-docker)
- [Section 2: Kubernetes Core (Q31–Q70)](#section-2-kubernetes-core)
- [Section 3: kubectl Mastery (Q71–Q95)](#section-3-kubectl-mastery)
- [Section 4: CI/CD (Q96–Q115)](#section-4-cicd)
- [Section 5: Infrastructure as Code (Q116–Q130)](#section-5-infrastructure-as-code)
- [Section 6: Cloud / AWS (Q131–Q143)](#section-6-cloud--aws)
- [Section 7: Monitoring & Observability (Q144–Q157)](#section-7-monitoring--observability)
- [Section 8: Security & Supply Chain (Q158–Q165)](#section-8-security--supply-chain)

---

## SECTION 1: DOCKER

---

**Q1. What is Docker and how does it differ from a virtual machine?**

```
DOCKER (CONTAINERS):
  Packages app + all dependencies into a container image.
  Container = isolated process running on the host OS kernel.
  Layers: read-only image layers + thin writable container layer.

  Isolation via Linux kernel features:
  - Namespaces: isolate PID, network, mount, UTS, IPC, user
  - cgroups: limit CPU, memory, disk I/O, network bandwidth
  - Union filesystem (OverlayFS): layer-based image storage

  Startup: milliseconds (process launch)
  Size: MB (shares host kernel, only app + libs)
  Density: 100s of containers per host

VIRTUAL MACHINES:
  Full OS emulation via hypervisor (VMware, VirtualBox, KVM, Hyper-V).
  Each VM has its own OS kernel + all system libraries.
  Startup: minutes (full OS boot)
  Size: GB (entire OS)
  Density: 10-20 VMs per host

WHEN TO USE VMs OVER CONTAINERS:
  - Hard isolation requirement (different kernel versions)
  - Non-Linux workloads (Windows apps)
  - Security isolation that goes beyond namespace separation
  - Legacy applications that can't be containerized

KEY INSIGHT: Containers share the host OS kernel.
This is their advantage (speed, density) and limitation (all containers must
be compatible with the host kernel — though WSL2 and VMs bridge this gap).
```

---

**Q2. Explain Dockerfile instructions: CMD vs ENTRYPOINT vs RUN — in depth.**

```dockerfile
# RUN — executes during IMAGE BUILD, creates a new layer
# Used for: installing packages, compiling code, creating directories
RUN apt-get update && apt-get install -y curl  # shell form (spawns /bin/sh -c)
RUN ["apt-get", "install", "-y", "curl"]       # exec form (no shell, no variable expansion)

# ---- Shell form vs exec form difference ----
# Shell form: /bin/sh -c "echo $HOME"   → shell processes variables, globbing, pipes
# Exec form:  ["echo", "$HOME"]          → NO shell → $HOME is literal, not expanded
# Exec form IS required for ENTRYPOINT/CMD so signals reach the process directly

# ENTRYPOINT — the executable that always runs when the container starts
# It is NOT overridden by arguments passed to `docker run`
ENTRYPOINT ["node", "dist/main.js"]
# docker run myapp --port=4000  →  node dist/main.js --port=4000  (appended)

# CMD — default arguments to ENTRYPOINT, OR default command if no ENTRYPOINT
CMD ["--env", "production"]
# docker run myapp  →  node dist/main.js --env production  (CMD appended to ENTRYPOINT)
# docker run myapp --env staging  →  node dist/main.js --env staging  (CMD REPLACED)

# ---- The interaction matrix ----
# No ENTRYPOINT  + CMD ["node","app.js"]  → runs: node app.js
# ENTRYPOINT ["node","app.js"] + CMD ["--prod"]  → runs: node app.js --prod
# ENTRYPOINT ["node","app.js"] + docker run myimage --dev  → runs: node app.js --dev
# ENTRYPOINT ["node","app.js"] + docker run --entrypoint sh myimage  → overrides ENTRYPOINT

# ---- ENTRYPOINT shell script pattern (best for production) ----
# entrypoint.sh:
#!/bin/sh
set -e
# Run migrations before starting app:
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Running migrations..."
  node dist/migrate.js
fi
# Hand off to CMD (exec replaces shell process → signals propagate correctly):
exec "$@"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["node", "dist/main.js"]
# docker run myimage  → entrypoint.sh runs migrations → exec node dist/main.js
# docker run myimage npm test  → entrypoint.sh runs → exec npm test

# ---- Signal handling (critical for Kubernetes) ----
# PID 1 must handle SIGTERM for graceful shutdown
# Shell form: /bin/sh -c "node app.js" → shell is PID 1, doesn't forward SIGTERM to node
# Exec form: ["node", "app.js"]       → node IS PID 1, receives SIGTERM directly
# Always use exec form in production!
```

---

**Q3. COPY vs ADD — when to use each.**

```dockerfile
# COPY — simple, predictable: copies files/directories from build context
COPY package.json ./
COPY src/ ./src/
COPY --chown=node:node . .          # change ownership
COPY --chmod=755 scripts/ ./scripts/  # set permissions (Dockerfile 1.2+)
COPY --from=builder /app/dist ./dist  # copy from another stage

# ADD — everything COPY does, PLUS:
# 1. Auto-extracts tar archives (dangerous if unexpected)
# 2. Downloads remote URLs (downloads at build time — bad for layer caching)

ADD archive.tar.gz /app/       # extracts → /app/contents/
ADD https://example.com/file.txt /tmp/  # downloads (avoid! use curl in RUN instead)

# ---- When to use ADD ----
# ONLY for the tar-extraction feature:
ADD rootfs.tar.gz /            # extracting a base filesystem

# NEVER use ADD for:
# - Regular file copies (use COPY)
# - Remote URLs (use RUN curl instead — better caching, security)

# ---- Why COPY is almost always correct ----
# 1. Explicit intent — no hidden behaviour
# 2. Better Docker layer caching (predictable)
# 3. Security — no surprise extraction or URL downloads
# 4. Linters (hadolint) will warn you if you use ADD unnecessarily

# Real-world pattern: never use ADD for URLs
# WRONG:
ADD https://github.com/user/repo/archive/main.tar.gz /app/

# RIGHT:
RUN curl -fsSL https://github.com/user/repo/archive/main.tar.gz \
      -o /tmp/repo.tar.gz \
    && tar -xzf /tmp/repo.tar.gz -C /app \
    && rm /tmp/repo.tar.gz
```

---

**Q4. ARG vs ENV — difference and correct usage.**

```dockerfile
# ARG — build-time variable only. Not available in the running container.
ARG NODE_VERSION=20
ARG BUILD_DATE
ARG GIT_COMMIT

FROM node:${NODE_VERSION}-alpine  # ARG available before FROM

# ENV — runtime environment variable. Available during build AND in running container.
ENV NODE_ENV=production
ENV PORT=3000

# ---- Key differences ----
# ARG: only during `docker build`, gone after build, NOT in running container
# ENV: persists in image metadata, available at runtime, visible via `docker inspect`

# NEVER store secrets in ENV (they appear in `docker inspect` and image layers!)
# WRONG:
ENV DB_PASSWORD=secret123     # visible in image metadata forever!
ARG DB_PASSWORD               # slightly better (not in final image), but still bad practice

# RIGHT: inject secrets at runtime
docker run -e DB_PASSWORD=$DB_PASSWORD myapp
# Or use Docker secrets, Kubernetes secrets, Vault

# ---- Common pattern: ARG for versioning ----
ARG APP_VERSION=unknown
ARG BUILD_DATE=unknown
ARG GIT_SHA=unknown

LABEL org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${GIT_SHA}"

# Build with:
# docker build \
#   --build-arg APP_VERSION=2.1.0 \
#   --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
#   --build-arg GIT_SHA=$(git rev-parse --short HEAD) \
#   -t myapp:2.1.0 .

# ---- ARG scope: defined before FROM is only usable in FROM ----
ARG BASE_VERSION=20-alpine
FROM node:${BASE_VERSION}     # works
RUN echo ${BASE_VERSION}      # EMPTY — ARG scope ended at FROM
# Re-declare ARG after FROM to use inside build:
ARG BASE_VERSION              # re-declare (no default needed, inherited)
RUN echo ${BASE_VERSION}      # works now

# ---- Override ENV at runtime ----
ENV LOG_LEVEL=info
# docker run -e LOG_LEVEL=debug myapp  → overrides to debug
# docker run --env-file .env myapp     → load from file
```

---

**Q5. Docker multi-stage builds — optimization in depth.**

```dockerfile
# Multi-stage build: separate build environment from runtime image
# Result: tiny production image with only what's needed to RUN the app

# ---- TypeScript/Node.js example ----
# Stage 1: Install ALL dependencies (dev + prod) for building
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci                          # install exact versions from lockfile

# Stage 2: Build TypeScript to JavaScript
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build                   # tsc → dist/
RUN npm prune --omit=dev            # remove devDependencies

# Stage 3: Minimal production image
FROM node:20-alpine AS production
# Security: non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser  --system --uid 1001 nextjs
WORKDIR /app
# Only copy production artifacts:
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist         ./dist
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER nextjs
EXPOSE 3000
ENV NODE_ENV=production PORT=3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/main.js"]

# Size comparison (typical Node.js app):
# Without multi-stage: ~1.2GB  (node:20 + devDeps + source)
# With multi-stage:    ~180MB  (node:20-alpine + prodDeps + dist only)

# ---- Layer caching strategy ----
# Order from least-changing to most-changing:
# 1. Base image          (changes: never)
# 2. System packages     (changes: rarely)
# 3. package.json only   (changes: when deps change)
# 4. RUN npm install     (only re-runs if package.json changed)
# 5. Source code         (changes: every commit)
# WRONG order destroys caching:
COPY . .                # copies ALL files → invalidates cache on every change
RUN npm ci              # re-runs every time!
# RIGHT order:
COPY package*.json ./   # only package files first
RUN npm ci              # cached unless package.json changed
COPY . .                # source code last

# ---- Target specific stage ----
docker build --target deps .     # stop after deps stage
docker build --target builder .  # stop after builder stage (for CI debugging)
docker build --target production . # full build (default)
```

---

**Q6. Docker networking — all drivers in detail.**

```
NETWORK DRIVERS:

1. BRIDGE (default)
   - Software bridge on host: docker0
   - Each container gets a virtual NIC connected to the bridge
   - Containers on same bridge talk by name (DNS)
   - Port publishing: -p HOST:CONTAINER maps NAT rules
   - Isolation: containers on different bridges can't communicate by default
   - Use case: standalone containers on single host

   docker network create --driver bridge my-net
   docker run --network my-net myapp

2. HOST
   - Container shares host network namespace — NO isolation
   - Container uses host IP directly, no NAT
   - Best performance (no network overhead)
   - Risk: container port conflicts with host services
   - Use case: high-performance apps where network is the bottleneck
   docker run --network host myapp
   # Container's :3000 IS host's :3000 — no -p needed

3. OVERLAY
   - Spans multiple Docker hosts (Docker Swarm or Kubernetes)
   - Creates virtual network across hosts using VXLAN encapsulation
   - Traffic encrypted (--opt encrypted=true)
   - Use case: distributed applications, Docker Swarm services

4. MACVLAN
   - Container gets its own MAC address on the physical network
   - Appears as a physical device on the LAN
   - Container gets IP directly from router DHCP (not Docker NAT)
   - Use case: legacy apps that need to be directly on the LAN
   docker network create -d macvlan \
     --subnet=192.168.1.0/24 \
     --gateway=192.168.1.1 \
     -o parent=eth0 \
     my-macvlan

5. IPVLAN
   - Like macvlan but shares MAC address of parent interface
   - L2 mode: same subnet as host
   - L3 mode: container acts as router (different subnets)

6. NONE
   - Container has no network interface (only loopback)
   - Complete network isolation
   - Use case: batch processing jobs with no network needs
   docker run --network none myapp

DOCKER COMPOSE NETWORK ISOLATION:
```
```yaml
networks:
  public:     {}   # nginx can reach
  private:    {}   # only internal services
  data:       {}   # only services that need DB

services:
  nginx:    { networks: [public] }
  api:      { networks: [public, private] }
  worker:   { networks: [private] }
  postgres: { networks: [data] }
  redis:    { networks: [private, data] }
# postgres is unreachable from nginx — correct!
```

---

**Q7. Docker volumes — volume vs bind mount vs tmpfs.**

```
THREE TYPES OF STORAGE:

1. NAMED VOLUME
   Managed by Docker daemon, stored in /var/lib/docker/volumes/
   Survives container removal, portable, Docker manages lifecycle.

   docker volume create pgdata
   docker run -v pgdata:/var/lib/postgresql/data postgres

   Pros:  Docker manages it, backup/migrate with docker cp, portable
   Cons:  Not easily inspectable from host filesystem

2. BIND MOUNT
   Maps a specific host path into the container.
   docker run -v /host/path:/container/path myapp
   docker run -v $(pwd):/app myapp    # dev: hot reload

   Pros:  Direct access to host files, hot-reload in dev, easy inspection
   Cons:  Host-path dependent (not portable), security risk (full host FS access)
   Use:   Development hot-reload, config files, logs you want on host

3. TMPFS MOUNT
   In-memory filesystem, never written to disk.
   docker run --tmpfs /tmp:size=100m myapp
   Or in docker run: --mount type=tmpfs,destination=/tmp

   Pros:  Fast (in-memory), secure (nothing written to disk or container layer)
   Cons:  Lost on container restart
   Use:   Temporary files, secrets that shouldn't touch disk, caches

DOCKER COMPOSE PATTERNS:
```
```yaml
services:
  postgres:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data        # named volume (persistent)
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # bind mount (read-only)
      - type: tmpfs                             # tmpfs for temp files
        target: /tmp

  api:
    volumes:
      - .:/app                                 # bind mount (dev hot-reload)
      - /app/node_modules                      # anonymous volume (don't override!)
      # ↑ This preserves container's node_modules even when . is bind-mounted

volumes:
  pgdata:
    driver: local
    # For production: use cloud volumes (EBS, GCP PD, Azure Disk)
    driver_opts:
      type: ext4
      device: /dev/xvdb
```
```
VOLUME BACKUP PATTERN:
docker run --rm \
  -v pgdata:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/pgdata-$(date +%Y%m%d).tar.gz -C /data .

VOLUME MIGRATION:
docker run --rm \
  -v pgdata_old:/from \
  -v pgdata_new:/to \
  alpine sh -c "cp -av /from/. /to"
```

---

**Q8. Docker security hardening — comprehensive guide.**

```dockerfile
# 1. Use minimal base images — reduce attack surface
FROM node:20-alpine          # Alpine: 5MB base
FROM gcr.io/distroless/nodejs20-debian12  # Distroless: no shell, no package manager
FROM scratch                 # Empty: for compiled static binaries (Go)

# 2. Non-root user — prevent container breakout privilege escalation
# Alpine:
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
# Debian/Ubuntu:
RUN useradd -r -s /bin/false -u 1001 appuser
USER 1001
# node image has built-in:
USER node

# 3. Read-only filesystem + tmpfs for writable paths
docker run \
  --read-only \
  --tmpfs /tmp:size=50m,mode=1777 \
  --tmpfs /app/logs:size=100m \
  myapp

# 4. Drop all capabilities, add only what's needed
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
# NET_BIND_SERVICE: allows binding to ports < 1024
# Rarely needed — run on unprivileged port (3000) instead of 80

# 5. No privilege escalation
docker run --security-opt=no-new-privileges myapp

# 6. Resource limits (prevent DoS)
docker run \
  --memory="512m" \
  --memory-swap="512m"  \  # same as memory = no swap
  --cpus="0.5" \
  --pids-limit=100 \
  myapp

# 7. Never store secrets in image
# BAD: visible in `docker history` and `docker inspect`
ENV DB_PASSWORD=secret
ARG DB_PASSWORD=secret

# GOOD: inject at runtime
docker run -e DB_PASSWORD="$DB_PASSWORD" myapp
docker run --env-file .env.production myapp

# 8. Multi-stage builds to exclude dev tools from production image
# (see Q5 — tools like compilers, npm devDependencies, .git never in prod image)

# 9. Image scanning in CI/CD
# Trivy (open source, fast):
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:latest

# Docker Scout (Docker Desktop + CI):
docker scout cves myapp:latest
docker scout recommendations myapp:latest

# Snyk:
snyk container test myapp:latest --severity-threshold=high

# 10. Sign images for supply chain security (see Q161)
cosign sign --key cosign.key myregistry/myapp:latest
cosign verify --key cosign.pub myregistry/myapp:latest

# 11. .dockerignore — prevent sensitive files from entering build context
```
```
# .dockerignore
.git
.env
.env.*
node_modules
*.log
.DS_Store
coverage/
__tests__/
.github/
Dockerfile*
docker-compose*
README.md
# NEVER add secrets to build context
*.pem
*.key
secrets/
```

---

**Q9. docker save vs docker export — and docker commit vs docker build.**

```bash
# ---- docker save vs docker export ----

# docker save: saves a COMPLETE IMAGE (all layers, metadata, tags)
# Output: a tar file containing all image layers
docker save myapp:latest -o myapp.tar
docker save myapp:latest | gzip > myapp.tar.gz     # compressed
# Restore on another machine:
docker load -i myapp.tar.gz
# Use case: move images to air-gapped systems, backup a full image with history

# docker export: exports a CONTAINER FILESYSTEM (flat — no layers, no history)
docker run --name mycontainer myapp
docker export mycontainer -o mycontainer-fs.tar
# Import as a new image (loses metadata, CMD, ENV, etc.):
docker import mycontainer-fs.tar myapp:flat
# docker import does NOT restore the image configuration!
# Use case: debugging (inspect filesystem), creating a base layer

# KEY DIFFERENCE:
# docker save preserves: all layers, image history, metadata, multi-arch manifests
# docker export produces: a single flat tarball of the container's filesystem only

# ---- docker commit vs docker build ----

# docker commit: creates an image from a RUNNING CONTAINER'S current state
docker run -it ubuntu bash
# (manually install things inside the container)
# apt-get install -y nginx
# exit
docker commit mycontainer mynginx:v1

# Problems with docker commit:
# - Not reproducible (manual steps, no documentation)
# - No layer caching (each commit is one opaque layer)
# - Can accidentally commit secrets (env vars, mounted secrets)
# - Cannot be reviewed in version control
# - Violates immutable infrastructure principle

# docker build: creates an image from a Dockerfile
# Pros: reproducible, version-controlled, cacheable layers, reviewable, auditable
# Use docker commit ONLY for: emergency debugging, creating a base layer once

# RULE: Never use docker commit for production images. Always use Dockerfile.
```

---

**Q10. docker exec vs docker attach — and docker system prune.**

```bash
# ---- docker exec ----
# Runs a NEW process inside a running container
docker exec -it mycontainer sh          # interactive shell
docker exec mycontainer ls /app         # one-off command (non-interactive)
docker exec -it mycontainer bash -c "cat /app/config.json | jq ."
docker exec -it -u root mycontainer sh  # run as root even if container runs as appuser
docker exec -e DEBUG=true mycontainer node inspect.js  # inject env var

# Most common uses:
docker exec -it mycontainer sh          # debug container filesystem
docker exec -it postgres psql -U postgres  # connect to DB
docker exec mycontainer cat /etc/hosts  # inspect networking

# ---- docker attach ----
# ATTACHES your terminal to the container's MAIN PROCESS (PID 1) stdin/stdout/stderr
docker attach mycontainer
# WARNING: if you press Ctrl+C, it sends SIGINT to PID 1 — KILLS the container!
# Detach without killing: Ctrl+P, Ctrl+Q (detach sequence)
# Use case: monitoring the main process output (logs)
# Better alternative: docker logs -f mycontainer  (safe, read-only)

# KEY DIFFERENCE:
# exec: starts a NEW process (won't affect PID 1, safe to Ctrl+C)
# attach: connects to EXISTING PID 1 (Ctrl+C kills the container)
# Always prefer exec unless you specifically need to interact with PID 1

# ---- docker system prune — reclaim disk space ----

# Show disk usage:
docker system df
# TYPE          TOTAL   ACTIVE  SIZE     RECLAIMABLE
# Images         45      12     15.2GB   8.1GB (54%)
# Containers      8       3     2.3MB    1.1MB (50%)
# Volumes        12       4     4.5GB    2.1GB (46%)
# Build Cache     -       -     3.2GB    3.2GB

# Remove stopped containers + dangling images + unused networks + build cache:
docker system prune
# Add --volumes to also remove unused volumes (CAREFUL — data loss):
docker system prune --volumes
# Skip confirmation:
docker system prune -f
# Include ALL unused images (not just dangling):
docker system prune -a

# Targeted cleanup:
docker container prune          # remove stopped containers
docker image prune              # remove dangling images (untagged)
docker image prune -a           # remove ALL unused images (not referenced by container)
docker volume prune             # remove unused volumes (DATA LOSS if you have important volumes)
docker network prune            # remove unused networks
docker builder prune            # remove build cache
docker builder prune --keep-storage 5GB  # keep 5GB of cache (prune oldest)

# Production safety: never run docker system prune --volumes on prod
# Always check docker system df first to understand what will be removed
```

---

**Q11. Container runtimes — Docker vs containerd vs CRI-O.**

```
CONTAINER RUNTIME LAYERS:

High-level runtime (manages images, networking, volumes):
  Docker, containerd, podman, CRI-O

Low-level runtime (actually creates the container using kernel features):
  runc (OCI-compliant), crun (faster, C), gvisor (sandbox), kata-containers (VM)

HISTORY:
  Docker (2013): Originally monolithic. Docker daemon → libcontainer → runc.
  Kubernetes (2014): Started using Docker via dockershim.
  containerd (2017): Docker split out the runtime as a standalone project → CNCF.
  CRI (Container Runtime Interface): K8s standard for talking to runtimes.
  dockershim removed (K8s 1.24, 2022): Kubernetes no longer supports Docker directly.

CURRENT STATE OF K8S RUNTIMES:

containerd (most common):
  - Used by: EKS, GKE, AKS, most managed K8s
  - Pulls images, manages lifecycle, calls runc
  - Lightweight, battle-tested, CNCF graduated
  - Config: /etc/containerd/config.toml
  - CLI: crictl (for debugging on nodes)

CRI-O:
  - Purpose-built for Kubernetes (nothing outside K8s use cases)
  - Used by: OpenShift, some bare-metal clusters
  - Follows OCI specs strictly
  - Smaller binary than containerd

gVisor (runsc):
  - Sandboxed runtime by Google: intercepts syscalls in userspace
  - Better security isolation (protection against kernel exploits)
  - Slight performance overhead (~10-20%)
  - Used by: GKE Sandbox, security-sensitive workloads

Kata Containers:
  - Each container runs in a lightweight VM
  - Full hardware-level isolation
  - OCI-compatible interface
  - Use case: multi-tenant platforms, regulatory compliance

PODMAN (Docker alternative on the CLI):
  - Daemonless: no background process (runs as user process)
  - Rootless: containers without root privileges
  - Docker-compatible: docker alias podman works for most commands
  - Use case: developer workstations, rootless containers in CI
  podman run -it ubuntu bash    # identical to docker run
  podman build -t myapp .       # identical to docker build
  podman compose up             # via podman-compose
```

---

**Q12. Docker Compose — production patterns and advanced features.**

```yaml
# docker-compose.yml — production-ready patterns

version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
      args:
        - APP_VERSION=${APP_VERSION:-local}
        - GIT_SHA=${GIT_SHA:-dev}
    image: myregistry/api:${APP_VERSION:-local}
    restart: unless-stopped              # auto-restart on crash (not on manual stop)
    deploy:
      replicas: 2
      resources:
        limits:   { cpus: "0.5", memory: 512M }
        reservations: { cpus: "0.1", memory: 128M }
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 5s
    environment:
      NODE_ENV: production
      PORT: "3000"
    env_file:
      - .env.production        # secret values from file (not committed to git)
    ports:
      - target: 3000
        published: 3000
        protocol: tcp
        mode: host
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
    networks:
      - public
      - internal

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB:       ${DB_NAME}
      POSTGRES_USER:     ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 10
    networks:
      - internal

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: >
      redis-server
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
      --requirepass ${REDIS_PASSWORD}
      --save 60 1000
    volumes:
      - redis_data:/data
    networks:
      - internal

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - public

networks:
  public:   {}
  internal:
    driver: bridge
    internal: true    # no external access to internal network

volumes:
  pgdata:
  redis_data:

# Profiles — run different service subsets:
# docker compose --profile monitoring up  → starts api + postgres + grafana + prometheus
# docker compose up  → starts only services without a profile
#
# services:
#   prometheus:
#     profiles: ["monitoring"]
#     image: prom/prometheus
```

---

**Q13. Dockerfile best practices — complete checklist.**

```dockerfile
# COMPLETE PRODUCTION DOCKERFILE

# 1. Pin exact base image versions (not :latest — breaks reproducibility)
FROM node:20.11.1-alpine3.19 AS base
# Or use digest for maximum pinning:
# FROM node:20-alpine@sha256:abc123...

# 2. Set WORKDIR (avoid RUN cd)
WORKDIR /app

# 3. Create non-root user early
RUN addgroup --system --gid 1001 nodejs && \
    adduser  --system --uid 1001 --ingroup nodejs nextjs

# 4. Install ONLY what you need (no dev tools in prod)
FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force   # clean npm cache to reduce layer size

FROM base AS builder
COPY package*.json ./
RUN npm ci
COPY --chown=nextjs:nodejs . .
RUN npm run build && \
    npm prune --omit=dev

# 5. Minimal production stage
FROM base AS production
ENV NODE_ENV=production \
    PORT=3000 \
    TZ=UTC

# 6. Copy only artifacts, not source
COPY --from=deps    --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist         ./dist
COPY --chown=nextjs:nodejs package.json ./

# 7. Switch to non-root user
USER nextjs

# 8. Expose port (documentation only — doesn't actually open port)
EXPOSE 3000

# 9. Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# 10. Use exec form for CMD (correct signal handling)
CMD ["node", "dist/main.js"]

# LAYER OPTIMIZATION RULES:
# - Combine RUN commands with && (fewer layers)
# - Clean up in same RUN as install (apt-get clean, npm cache clean)
# - Order: rarely-changing → frequently-changing
# - .dockerignore excludes .git, node_modules, .env, *.log

# IMAGE SIZE REDUCTION TECHNIQUES:
# - Alpine vs Debian: 5MB vs 74MB base
# - Multi-stage: exclude build tools from production
# - npm ci --only=production: exclude devDependencies
# - RUN apt-get ... && rm -rf /var/lib/apt/lists/*  (clean apt cache same layer)
```

---

**Q14. Docker image registries — Harbor, ECR, GHCR.**

```bash
# ---- GitHub Container Registry (GHCR) ----
# Free for public, included with GitHub Actions minutes for private
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker tag myapp:latest ghcr.io/myorg/myapp:latest
docker push ghcr.io/myorg/myapp:latest

# GitHub Actions login:
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}  # automatic, no setup needed

# ---- AWS Elastic Container Registry (ECR) ----
# Authenticate (token expires in 12h):
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Create repository:
aws ecr create-repository --repository-name myapp --image-scanning-configuration scanOnPush=true

# Tag and push:
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest

# ECR features:
# - Image scanning on push (basic Clair, or enhanced with Inspector)
# - Lifecycle policies (delete images older than 30 days automatically)
# - Cross-account access via resource-based policies
# - Public ECR gallery: public.ecr.aws

# ---- Harbor (self-hosted, enterprise) ----
# Harbor: open-source cloud-native registry by VMware → CNCF
# Features: RBAC, image scanning (Trivy built-in), replication,
#           vulnerability reports, content trust (Notary/cosign), webhooks

docker login registry.mycompany.com
docker tag myapp:latest registry.mycompany.com/myproject/myapp:latest
docker push registry.mycompany.com/myproject/myapp:latest

# Harbor replication — sync between registries:
# Harbor UI → Administration → Registrations → Create → point to ECR/GCR/DockerHub
# Policy: filter by tag pattern, trigger on push or scheduled

# ---- Registry best practices ----
# 1. Tag strategy: semver + sha + environment
#    myapp:2.1.0         # semantic version
#    myapp:sha-abc1234   # git sha for traceability
#    myapp:latest        # avoid in production Kubernetes (always use specific tag)

# 2. Immutable tags: never overwrite a tagged image (ECR supports this)
#    aws ecr put-image-tag-mutability --image-tag-mutability IMMUTABLE

# 3. Lifecycle policies (ECR example):
aws ecr put-lifecycle-policy --repository-name myapp --lifecycle-policy '{
  "rules": [{
    "rulePriority": 1,
    "description": "Keep last 10 production images",
    "selection": {
      "tagStatus": "tagged",
      "tagPrefixList": ["v"],
      "countType": "imageCountMoreThan",
      "countNumber": 10
    },
    "action": { "type": "expire" }
  }, {
    "rulePriority": 2,
    "description": "Remove untagged images after 7 days",
    "selection": {
      "tagStatus": "untagged",
      "countType": "sinceImagePushed",
      "countUnit": "days",
      "countNumber": 7
    },
    "action": { "type": "expire" }
  }]
}'
```

---

**Q15. Docker Compose profiles and multi-environment patterns.**

```yaml
# profiles: run different service subsets per environment

services:
  # Core services — always started
  api:
    build: .
    depends_on:
      postgres: { condition: service_healthy }

  postgres:
    image: postgres:16-alpine
    environment: { POSTGRES_PASSWORD: dev }

  # Development extras — only with: docker compose --profile dev up
  pgadmin:
    image: dpage/pgadmin4
    profiles: ["dev"]
    ports: ["5050:80"]
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local.dev
      PGADMIN_DEFAULT_PASSWORD: admin

  redis-insight:
    image: redislabs/redisinsight
    profiles: ["dev"]
    ports: ["8001:8001"]

  # Testing — only with: docker compose --profile test up
  test-runner:
    build: { context: ., target: test }
    profiles: ["test"]
    command: npm test -- --coverage
    depends_on:
      postgres: { condition: service_healthy }
    environment:
      DATABASE_URL: postgresql://postgres:dev@postgres:5432/testdb

  # Monitoring — only with: docker compose --profile monitoring up
  prometheus:
    image: prom/prometheus
    profiles: ["monitoring"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports: ["9090:9090"]

  grafana:
    image: grafana/grafana
    profiles: ["monitoring"]
    ports: ["3001:3000"]
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

# Usage:
# docker compose up                              # core only
# docker compose --profile dev up               # core + dev tools
# docker compose --profile dev --profile monitoring up  # core + dev + monitoring
# docker compose --profile test run test-runner # run tests, then exit
```

---

**Q16–Q30: Docker quick reference (essential for interviews)**

```bash
# Q16. Docker image commands
docker images                          # list images
docker image ls --filter dangling=true # dangling images (untagged)
docker image inspect myapp:latest      # full metadata (layers, env, entrypoint)
docker image history myapp:latest      # layer history + sizes
docker image rm myapp:latest           # remove image
docker pull myapp:latest               # pull from registry
docker push myapp:latest               # push to registry
docker tag myapp:old myapp:new         # add tag

# Q17. Docker container lifecycle
docker run -d --name api myapp:latest  # run detached, named
docker run -it --rm ubuntu bash        # interactive, remove on exit
docker ps                              # running containers
docker ps -a                           # all containers (including stopped)
docker stop api                        # SIGTERM → wait 10s → SIGKILL
docker kill api                        # SIGKILL immediately
docker start api                       # start stopped container
docker restart api                     # stop + start
docker rm api                          # remove stopped container
docker rm -f api                       # force remove running container

# Q18. Docker logs
docker logs api                        # all logs
docker logs api -f                     # follow (stream new logs)
docker logs api --tail 50              # last 50 lines
docker logs api --since 30m            # last 30 minutes
docker logs api --since "2024-01-15"   # since date
docker logs api 2>&1 | grep ERROR      # grep errors

# Q19. Docker networking commands
docker network ls
docker network create my-network
docker network connect my-network api     # connect running container
docker network disconnect my-network api
docker network inspect my-network         # see connected containers, IPs

# Q20. Docker volume commands
docker volume ls
docker volume create myvolume
docker volume inspect myvolume            # location on host
docker volume rm myvolume
docker volume prune                       # remove unused volumes

# Q21. Debugging containers
docker stats                              # live CPU/memory/network/disk per container
docker stats --no-stream                  # snapshot (no live)
docker top api                            # processes inside container
docker diff api                           # filesystem changes since start
docker inspect api                        # full container config, IP, mounts
docker inspect api --format '{{.NetworkSettings.IPAddress}}'  # just IP
docker inspect api --format '{{json .Config.Env}}' | jq .     # env vars

# Q22. Build optimization
docker build --no-cache .                 # ignore cache
docker build --progress=plain .           # verbose build output
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:multi .  # multi-arch
docker buildx ls                          # list builders
docker buildx create --use --name mybuilder  # create BuildKit builder

# Q23. Docker context (multi-host management)
docker context create remote --docker "host=ssh://user@remote-host"
docker context use remote               # now docker commands run on remote host
docker context use default              # back to local

# Q24. Docker secrets (Swarm mode)
echo "supersecret" | docker secret create db_password -
docker service create --secret db_password myapp
# Secret available at /run/secrets/db_password inside container

# Q25. Docker resource monitoring
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
docker system df -v                     # detailed disk usage per image/container/volume

# Q26. Copy files to/from containers
docker cp api:/app/logs/app.log ./app.log    # container → host
docker cp ./config.json api:/app/config.json # host → container

# Q27. Override at runtime
docker run -e NODE_ENV=staging \                    # override env
  -v $(pwd)/config:/app/config:ro \               # extra volume
  --entrypoint /bin/sh \                          # override entrypoint
  --memory 1g \                                   # override resource limits
  myapp:latest -c "node /app/dist/migrate.js"

# Q28. Docker Buildx — extended build capabilities
docker buildx build \
  --platform linux/amd64,linux/arm64 \            # multi-arch
  --cache-from type=registry,ref=ghcr.io/org/myapp:cache \
  --cache-to   type=registry,ref=ghcr.io/org/myapp:cache,mode=max \
  --provenance=true \                             # SLSA provenance
  --sbom=true \                                   # software bill of materials
  --push \
  -t ghcr.io/org/myapp:latest .

# Q29. OCI image spec
# OCI (Open Container Initiative) Image Specification:
# - image index (manifest list for multi-arch)
# - image manifest (references config + layers)
# - image config (cmd, env, entrypoint, layers metadata)
# - layers (compressed tarballs of filesystem diffs)
# Docker images ARE OCI images — fully compatible with containerd, podman, skopeo

# Q30. skopeo — inspect and copy images without pulling
skopeo inspect docker://ubuntu:22.04         # inspect without pulling
skopeo copy docker://source:tag oci:./local  # copy to local OCI format
skopeo copy --override-os linux \            # copy between registries
  docker://ghcr.io/org/app:latest \
  docker://123456.dkr.ecr.us-east-1.amazonaws.com/app:latest
```


---

## SECTION 2: KUBERNETES CORE

---

**Q31. Kubernetes architecture — control plane and worker nodes in depth.**

```
CONTROL PLANE (master):

1. kube-apiserver
   - Single source of truth: ALL cluster communication goes through it
   - REST API + watch mechanism (clients watch for changes)
   - Authentication (certs, tokens, OIDC), authorization (RBAC), admission control
   - Horizontal scaling: multiple instances behind load balancer
   - State stored in etcd only (API server is stateless)

2. etcd
   - Distributed consistent KV store (Raft consensus algorithm)
   - Stores ALL cluster state: pods, services, configmaps, secrets, etc.
   - Strong consistency: every read reflects latest write
   - Backup regularly! etcd loss = cluster state loss
   - Typically 3 or 5 instances (Raft quorum = floor(n/2) + 1)
   - Performance critical: use SSD with low fsync latency

3. kube-scheduler
   - Watches for unscheduled pods → picks the best node
   - Scheduling factors:
     * Resource requests (CPU/memory): does node have enough?
     * Affinity/anti-affinity rules
     * Taints and tolerations
     * Node selectors and labels
     * Pod topology spread constraints (spread across AZs)
     * Priority classes
   - Two phases: Filtering (which nodes CAN run it?) → Scoring (which node is BEST?)

4. kube-controller-manager
   - Runs all built-in controllers as goroutines in one binary
   - Deployment controller: ensures desired ReplicaSet exists
   - ReplicaSet controller: ensures correct number of pods
   - Node controller: handles node heartbeats, marks NotReady
   - Job controller: manages batch job completion
   - ServiceAccount controller: creates default SAs per namespace
   - Control loop: observe desired state → compare to actual → act to reconcile

5. cloud-controller-manager (optional)
   - Integrates with cloud providers (AWS, GCP, Azure)
   - Manages: load balancers (for Services type:LoadBalancer), 
              volumes (PVs), route tables, node lifecycle

WORKER NODE:

1. kubelet
   - Agent running on every node — implements the container lifecycle
   - Watches API server for pods assigned to its node
   - Calls CRI (containerd/CRI-O) to create/stop containers
   - Reports pod status, node status, resource usage back to API server
   - Runs probes (liveness, readiness, startup)
   - Garbage collects unused images and containers

2. kube-proxy
   - Maintains iptables/ipvs rules for Service routing
   - Service VIP (ClusterIP) → Pod IPs (load balanced)
   - Modes: iptables (default), ipvs (better for large clusters), eBPF (Cilium)

3. Container runtime
   - containerd (most common), CRI-O, Docker (deprecated in K8s 1.24+)
   - Implements CRI: pull image, run container, stop container
```

---

**Q32. Kubernetes resource types — when to use which.**

```yaml
# WORKLOADS:

# Deployment: stateless apps (API servers, web servers, microservices)
# - Manages ReplicaSets, rolling updates, rollbacks
# - All pods are identical and interchangeable
kind: Deployment
# Use when: stateless, no stable network identity needed, horizontal scaling

# StatefulSet: stateful apps (databases, caches, message brokers)
# - Stable pod names: redis-0, redis-1, redis-2 (not random hash)
# - Stable persistent storage: each pod gets its own PVC
# - Ordered startup and shutdown (redis-0 before redis-1)
kind: StatefulSet
# Use when: persistent storage per pod, stable network identity, ordered deployment

# DaemonSet: one pod per node (or per node matching a selector)
# - Node-level infrastructure: log collectors, monitoring agents, CNI plugins
# - Auto-added to new nodes as they join
kind: DaemonSet
# Use when: every node must run the pod (e.g., Fluentd, Datadog agent, Falco)

# Job: run to completion (batch processing)
# - Runs N completions total with P parallelism
# - Restarts on failure until completions reached
kind: Job
# Use when: database migrations, report generation, data processing pipelines

# CronJob: scheduled Job
# - Cron syntax: "*/5 * * * *" (every 5 minutes)
# - Manages Job history (successfulJobsHistoryLimit, failedJobsHistoryLimit)
kind: CronJob
# Use when: periodic tasks (cleanup, snapshots, report emails)

# NETWORKING:

# Service types:
# ClusterIP (default): stable virtual IP, only reachable within cluster
# NodePort: exposes on each node's IP at a static port (30000-32767)
# LoadBalancer: provisions cloud LB (ELB, GCP LB), external access
# ExternalName: DNS CNAME alias for external service (maps to external DB hostname)
# Headless (ClusterIP: None): no VIP, returns pod IPs directly (for StatefulSets)

# Ingress: L7 HTTP routing (host + path → Service)
# - Requires an IngressController (nginx-ingress, traefik, ALB ingress)
# - Handles TLS termination, rate limiting, auth

# STORAGE:
# PersistentVolume (PV): admin-provisioned storage resource
# PersistentVolumeClaim (PVC): user request for storage
# StorageClass: dynamic provisioning recipe (type=gp3, provisioner=ebs.csi.aws.com)
# VolumeSnapshot: point-in-time snapshot of a PVC

# CONFIGURATION:
# ConfigMap: non-sensitive config (env vars, config files, feature flags)
# Secret: sensitive data (passwords, tokens, TLS certs)
#   Types: Opaque (generic), kubernetes.io/tls, kubernetes.io/dockerconfigjson
```

---

**Q33. Kubernetes Deployments — full manifest with every production setting.**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: production
  labels:
    app: api
    version: "2.1.0"
    team: backend
  annotations:
    deployment.kubernetes.io/revision: "7"
    kubernetes.io/change-cause: "Release 2.1.0: add payment retry logic"
spec:
  replicas: 3

  # Rolling update strategy (zero-downtime deployments):
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # allow 1 extra pod (4 total during update)
      maxUnavailable: 0     # never reduce below 3 — all requests served

  # Label selector (immutable after creation):
  selector:
    matchLabels:
      app: api

  template:
    metadata:
      labels:
        app: api
        version: "2.1.0"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"

    spec:
      # Service account for IRSA / Workload Identity:
      serviceAccountName: api-sa

      # Security context (pod-level):
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        runAsGroup: 1001
        fsGroup: 1001
        seccompProfile:
          type: RuntimeDefault

      # Graceful shutdown: give app time to finish in-flight requests:
      terminationGracePeriodSeconds: 30

      containers:
        - name: api
          image: ghcr.io/myorg/api:2.1.0
          imagePullPolicy: IfNotPresent    # Always for :latest, IfNotPresent otherwise

          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
            - name: metrics
              containerPort: 9090

          # Resource limits (ALWAYS set in production):
          resources:
            requests:
              memory: "256Mi"    # Scheduler uses this for placement
              cpu: "100m"        # 0.1 CPU core
            limits:
              memory: "512Mi"    # OOMKilled if exceeded
              cpu: "500m"        # Throttled if exceeded (CPU is compressible)

          # Environment variables:
          env:
            - name: NODE_ENV
              value: "production"
            - name: PORT
              value: "3000"
            - name: POD_NAME              # Inject pod metadata (for logging/tracing)
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: NODE_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP

          # Load all keys from ConfigMap as env vars:
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets
                optional: false

          # Mount config file as volume:
          volumeMounts:
            - name: app-config
              mountPath: /app/config
              readOnly: true
            - name: tmp-dir
              mountPath: /tmp

          # Security context (container-level):
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true     # immutable container filesystem
            capabilities:
              drop: ["ALL"]

          # Liveness: if fails → container RESTARTED (unhealthy, needs restart)
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
            successThreshold: 1

          # Readiness: if fails → removed from Service endpoints (don't send traffic)
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

          # Startup: extra time for slow-starting apps (disables liveness until succeeded)
          startupProbe:
            httpGet:
              path: /health/live
              port: http
            failureThreshold: 30    # 30 * 10s = 5 minutes max startup time
            periodSeconds: 10

          # Lifecycle hooks:
          lifecycle:
            preStop:
              exec:
                # Sleep to let load balancer drain connections before SIGTERM
                command: ["/bin/sh", "-c", "sleep 5"]

      volumes:
        - name: app-config
          configMap:
            name: api-config
        - name: tmp-dir
          emptyDir:
            medium: Memory    # tmpfs — fast, cleared on pod restart
            sizeLimit: 50Mi

      # Spread pods across availability zones:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api

      # Anti-affinity: don't schedule 2 api pods on same node:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: api
                topologyKey: kubernetes.io/hostname

      # Image pull secret for private registry:
      imagePullSecrets:
        - name: ghcr-secret
```

---

**Q34. Kubernetes Services — all types with use cases.**

```yaml
# 1. ClusterIP — internal only (default)
apiVersion: v1
kind: Service
metadata:
  name: api-svc
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - name: http
      port: 80           # port clients use
      targetPort: 3000   # port on pod
      protocol: TCP
# Access: api-svc.production.svc.cluster.local:80
# or just: api-svc:80 (within same namespace)

---
# 2. NodePort — external access via node IP (dev/testing only)
apiVersion: v1
kind: Service
metadata:
  name: api-nodeport
spec:
  type: NodePort
  selector: { app: api }
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 30080    # optional: 30000-32767 range
# Access: <any-node-ip>:30080

---
# 3. LoadBalancer — provisions cloud load balancer (production)
apiVersion: v1
kind: Service
metadata:
  name: api-lb
  annotations:
    # AWS NLB (Network Load Balancer):
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector: { app: api }
  ports:
    - port: 443
      targetPort: 3000

---
# 4. Headless — no VIP, DNS returns pod IPs directly
apiVersion: v1
kind: Service
metadata:
  name: redis-headless
spec:
  clusterIP: None   # headless
  selector: { app: redis }
  ports:
    - port: 6379
# DNS: redis-headless → [10.0.1.5, 10.0.1.6, 10.0.1.7]  (all pod IPs)
# StatefulSet pods: redis-0.redis-headless.default.svc.cluster.local

---
# 5. ExternalName — DNS alias for external service
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: mydb.rds.amazonaws.com   # CNAME alias
# app connects to external-db:5432 → resolves to mydb.rds.amazonaws.com
# Allows changing external service without app code changes

---
# 6. Ingress — L7 HTTP routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [api.example.com, admin.example.com]
      secretName: example-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service: { name: api-svc, port: { number: 80 } }
    - host: admin.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: admin-svc, port: { number: 80 } }
```

---

**Q35. Kubernetes autoscaling — HPA, VPA, KEDA, Cluster Autoscaler, Karpenter.**

```yaml
# 1. HPA — Horizontal Pod Autoscaler (more/fewer pods)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 50
  metrics:
    # CPU-based scaling:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70   # scale out when avg CPU > 70%
    # Memory-based scaling:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    # Custom metric from Prometheus (KEDA or custom metrics adapter):
    - type: External
      external:
        metric:
          name: http_requests_per_second
          selector:
            matchLabels: { app: api }
        target:
          type: AverageValue
          averageValue: "1000"      # 1000 rps per pod
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60     # wait 60s before scaling up again
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60              # add at most 4 pods per minute
    scaleDown:
      stabilizationWindowSeconds: 300    # wait 5min before scaling down
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60              # remove at most 10% per minute

---
# 2. VPA — Vertical Pod Autoscaler (adjust CPU/memory requests)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: "Off"    # Off: recommendations only (safe start)
    # Auto: applies recommendations (causes pod restarts!)
    # Initial: only for new pods
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed: { cpu: 50m, memory: 64Mi }
        maxAllowed: { cpu: 2000m, memory: 2Gi }
# Check recommendations: kubectl describe vpa api-vpa
# VPA vs HPA: use HPA for replicas, VPA for right-sizing requests

---
# 3. KEDA — event-driven autoscaling (scale to zero!)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: api-scaledobject
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicaCount: 0      # scale to ZERO when no messages
  maxReplicaCount: 50
  pollingInterval: 15
  cooldownPeriod: 300
  triggers:
    # Scale based on Kafka consumer lag:
    - type: kafka
      metadata:
        bootstrapServers: kafka:9092
        consumerGroup: api-consumer-group
        topic: orders
        lagThreshold: "100"       # scale out when lag > 100 per pod
    # Scale based on RabbitMQ queue depth:
    - type: rabbitmq
      metadata:
        host: amqp://rabbitmq:5672
        queueName: tasks
        queueLength: "50"          # 1 pod per 50 messages
    # Scale based on Prometheus metric:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: active_users
        threshold: "100"
        query: sum(active_sessions{app="api"})
```

```
# 4. Cluster Autoscaler vs Karpenter

CLUSTER AUTOSCALER:
  - Scales node GROUPS (predefined ASG in AWS)
  - Watches for pending pods → adds nodes from node group
  - Works with: GKE, EKS (with ASGs), AKS
  - Limitation: all nodes in group are same type
  - Slow: typically 2-5 minutes to provision

KARPENTER (AWS):
  - Next-gen node provisioning for AWS EKS
  - Provisions EXACTLY the right instance type for pending pods
  - Example: 3 pods needing 3.5 CPU → picks c5.xlarge (4 CPU) exactly
  - Consolidation: bin-packs pods, terminates underutilized nodes
  - Spot instance support: automatically falls back to on-demand
  - Faster: typically 30-60 seconds

KARPENTER NODEPOOL:
```
```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]   # prefer spot, fall back to on-demand
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["c5.xlarge", "c5.2xlarge", "c5a.xlarge", "m5.xlarge"]
      nodeClassRef:
        apiVersion: karpenter.k8s.aws/v1beta1
        kind: EC2NodeClass
        name: default
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s    # terminate underutilized nodes after 30s
  limits:
    cpu: 1000              # max 1000 CPU cores for this NodePool
```

---

**Q36. Kubernetes RBAC — full guide with real examples.**

```yaml
# RBAC components:
# Role/ClusterRole: WHAT can be done (verbs on resources)
# RoleBinding/ClusterRoleBinding: WHO can do WHAT

# Role: namespace-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-role
  namespace: staging
rules:
  - apiGroups: [""]                              # core API group
    resources: ["pods", "pods/log", "pods/exec"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: []                                    # no access to secrets

---
# ClusterRole: cluster-wide (or reusable across namespaces)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only-cluster
rules:
  - apiGroups: ["*"]
    resources: ["*"]
    verbs: ["get", "list", "watch"]      # read-only everywhere
  - nonResourceURLs: ["/metrics", "/healthz"]
    verbs: ["get"]

---
# RoleBinding: bind Role to users/groups/serviceaccounts
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: staging
subjects:
  - kind: User
    name: john@company.com               # from identity provider
    apiGroup: rbac.authorization.k8s.io
  - kind: Group
    name: backend-team                   # from OIDC group claim
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: ci-sa
    namespace: staging
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io

---
# ServiceAccount for app with IRSA (AWS IAM Roles for Service Accounts):
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456:role/api-production-role
    eks.amazonaws.com/audience: sts.amazonaws.com

---
# NetworkPolicy: restrict pod-to-pod communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes: ["Ingress", "Egress"]
  ingress:
    - from:
        - namespaceSelector:             # only from production namespace
            matchLabels:
              kubernetes.io/metadata.name: production
          podSelector:                   # only from nginx
            matchLabels:
              app: nginx
      ports:
        - protocol: TCP
          port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379
    - to:                               # allow DNS
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
```

---

**Q37. Kubernetes ConfigMaps and Secrets — patterns and external secrets.**

```yaml
# ConfigMap — three ways to create:

# 1. From literals:
kubectl create configmap app-config \
  --from-literal=NODE_ENV=production \
  --from-literal=LOG_LEVEL=info

# 2. From file:
kubectl create configmap nginx-config --from-file=./nginx.conf

# 3. As YAML:
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  REDIS_URL: "redis://redis-svc:6379"
  # Multi-line value (config file):
  app.properties: |
    server.port=3000
    server.timeout=30s
    feature.newUI=true

---
# Secret — types:
# Opaque: base64-encoded arbitrary data
# kubernetes.io/tls: TLS certificate + key
# kubernetes.io/dockerconfigjson: registry credentials
# kubernetes.io/service-account-token: SA token (auto-created)

apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:                     # plaintext → auto-base64
  DATABASE_URL: "postgresql://user:pass@db:5432/mydb"
  JWT_SECRET: "min32charssecretkey1234567890abcdef"
  STRIPE_SECRET_KEY: "sk_live_..."

---
# EXTERNAL SECRETS OPERATOR (production best practice):
# Syncs secrets from AWS Secrets Manager, Vault, GCP Secret Manager into K8s Secrets

apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h               # re-sync every hour
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: app-secrets                # K8s Secret name to create/update
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL        # key in K8s Secret
      remoteRef:
        key: production/api          # path in Secrets Manager
        property: database_url       # specific field in JSON
    - secretKey: JWT_SECRET
      remoteRef:
        key: production/api
        property: jwt_secret

---
# ClusterSecretStore (AWS):
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:                         # IRSA authentication
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets

---
# Sealed Secrets (encrypt secrets for GitOps — can commit to git):
# Encrypt with kubeseal (public key):
kubeseal --cert cert.pem < secret.yaml > sealed-secret.yaml
# git add sealed-secret.yaml ← safe to commit!
# Controller decrypts in-cluster with private key
```

---

**Q38. Kubernetes Jobs and CronJobs — production patterns.**

```yaml
# Job — run to completion
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  namespace: production
spec:
  completions: 1               # total successful completions needed
  parallelism: 1               # pods running simultaneously
  backoffLimit: 3              # retry 3 times before marking failed
  activeDeadlineSeconds: 600   # kill job after 10 minutes
  ttlSecondsAfterFinished: 86400  # clean up job 24h after completion
  template:
    spec:
      restartPolicy: OnFailure    # Never or OnFailure (not Always)
      containers:
        - name: migration
          image: ghcr.io/myorg/api:2.1.0
          command: ["node", "dist/migrate.js"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: DATABASE_URL
          resources:
            requests: { memory: 256Mi, cpu: 100m }
            limits:   { memory: 512Mi, cpu: 500m }

---
# Parallel job with work queue (N items, M workers):
spec:
  completions: 100             # process 100 items total
  parallelism: 10              # 10 workers in parallel
  completionMode: Indexed      # each pod gets an index (0-99)
  template:
    spec:
      containers:
        - env:
            - name: JOB_COMPLETION_INDEX
              valueFrom:
                fieldRef:
                  fieldPath: metadata.annotations['batch.kubernetes.io/job-completion-index']

---
# CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-report
  namespace: production
spec:
  schedule: "0 2 * * *"              # 2 AM daily
  timeZone: "America/New_York"       # explicit timezone (K8s 1.27+)
  concurrencyPolicy: Forbid          # skip if previous still running
  # Allow: allow concurrent runs
  # Replace: cancel previous run, start new
  successfulJobsHistoryLimit: 3      # keep last 3 successful
  failedJobsHistoryLimit: 5          # keep last 5 failed
  startingDeadlineSeconds: 300       # skip if couldn't start within 5min
  suspend: false                     # set true to pause
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: report
              image: ghcr.io/myorg/reporter:latest
              command: ["node", "dist/generate-report.js"]

# Trigger manually (useful for testing):
# kubectl create job --from=cronjob/nightly-report manual-run-$(date +%s)
```

---

**Q39. Kubernetes init containers and sidecar containers.**

```yaml
spec:
  # Init containers run SEQUENTIALLY before main containers start.
  # Must complete successfully — if any fails, pod restarts.
  initContainers:

    # Wait for database to be ready:
    - name: wait-for-db
      image: busybox:1.36
      command:
        - sh
        - -c
        - |
          until nc -z postgres-svc 5432; do
            echo "Waiting for postgres..."
            sleep 2
          done
          echo "PostgreSQL ready!"

    # Run database migration:
    - name: run-migration
      image: ghcr.io/myorg/api:2.1.0
      command: ["node", "dist/migrate.js"]
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL

    # Download config from S3:
    - name: config-loader
      image: amazon/aws-cli
      command:
        - sh
        - -c
        - aws s3 cp s3://my-config/app.json /config/app.json
      volumeMounts:
        - name: config-volume
          mountPath: /config
      env:
        - name: AWS_REGION
          value: us-east-1

  containers:
    - name: api
      volumeMounts:
        - name: config-volume
          mountPath: /app/config
          readOnly: true

    # SIDECAR containers run alongside main container:

    # Log shipper sidecar:
    - name: log-shipper
      image: fluent/fluent-bit:2.2
      volumeMounts:
        - name: app-logs
          mountPath: /var/log/app
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc
      resources:
        requests: { memory: 32Mi, cpu: 10m }
        limits:   { memory: 64Mi, cpu: 50m }

    # OTel collector sidecar:
    - name: otel-collector
      image: otel/opentelemetry-collector-contrib:0.91.0
      args: ["--config=/conf/otel-config.yaml"]
      volumeMounts:
        - name: otel-config
          mountPath: /conf

  volumes:
    - name: config-volume
      emptyDir: {}
    - name: app-logs
      emptyDir: {}
    - name: fluent-bit-config
      configMap:
        name: fluent-bit-config
    - name: otel-config
      configMap:
        name: otel-config

# NOTE: Kubernetes 1.29+ has native sidecar support (restartPolicy: Always on initContainer)
# This ensures sidecars start before main containers and don't block pod termination
initContainers:
  - name: otel-sidecar
    restartPolicy: Always     # marks it as a true sidecar (K8s 1.29+)
    image: otel/opentelemetry-collector:latest
```

---

**Q40. Kubernetes admission controllers — webhooks and policies.**

```
ADMISSION CONTROLLERS: intercept API server requests BEFORE persisting to etcd
Two phases:
1. Mutating admission: can modify the request (inject sidecars, set defaults)
2. Validating admission: can reject the request (enforce policies)

BUILT-IN CONTROLLERS:
- NamespaceLifecycle: reject creation in terminating namespaces
- LimitRanger: set default resource limits
- ServiceAccount: auto-inject service account
- PodSecurity: enforce Pod Security Standards
- MutatingAdmissionWebhook: call external webhook to mutate
- ValidatingAdmissionWebhook: call external webhook to validate

POD SECURITY STANDARDS (replacement for PodSecurityPolicy, K8s 1.25+):
  Privileged: unrestricted (CI/CD, system pods)
  Baseline:   prevent known privilege escalations (most workloads)
  Restricted: hardened (security-sensitive workloads)

  Apply per namespace:
```
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```
```
OPA GATEKEEPER (policy as code):
  Installs as MutatingAdmissionWebhook + ValidatingAdmissionWebhook
  Policies written in Rego (OPA policy language)
```
```yaml
# Constraint Template (defines the policy schema):
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names: { kind: K8sRequiredLabels }
      validation:
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items: { type: string }
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }

---
# Constraint (instance of the policy):
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds: [{ apiGroups: ["apps"], kinds: ["Deployment"] }]
    namespaces: ["production", "staging"]
  parameters:
    labels: ["team", "app", "version"]
```
```
KYVERNO (K8s-native policy engine, simpler than OPA):
  Policies are Kubernetes resources (no Rego needed)
```
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: enforce
  rules:
    - name: check-container-limits
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "Resource limits are required for all containers"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"

    - name: disallow-latest-tag
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "Use specific image tags, not :latest"
        pattern:
          spec:
            containers:
              - image: "!*:latest"

    # Auto-inject sidecar (mutating):
    - name: inject-otel-sidecar
      match:
        any:
          - resources:
              kinds: ["Deployment"]
              namespaces: ["production"]
      mutate:
        patchStrategicMerge:
          spec:
            template:
              spec:
                containers:
                  - (name): "*"
                    env:
                      - name: OTEL_EXPORTER_OTLP_ENDPOINT
                        value: "http://otel-collector:4318"
```


---

## SECTION 3: kubectl MASTERY

---

**Q41. kubectl apply vs kubectl create — key difference.**

```bash
# kubectl create: IMPERATIVE — creates resource, fails if it already exists
kubectl create deployment api --image=myapp:latest
kubectl create -f deployment.yaml     # fails if deployment already exists

# kubectl apply: DECLARATIVE — creates OR updates, stores last-applied config
kubectl apply -f deployment.yaml      # create if not exists, update if exists
kubectl apply -f ./manifests/          # apply all YAML files in directory
kubectl apply -f https://raw.github.com/org/repo/main/deploy.yaml

# How apply tracks changes:
# Stores last-applied-configuration as an annotation on the resource
# On next apply: compares desired (file) vs last-applied → computes diff → patches

# kubectl apply vs kubectl replace:
# apply: PATCH (3-way merge, preserves fields you didn't touch)
# replace: PUT (full replacement, fails if resource doesn't exist)
# replace --force: delete + recreate (causes downtime!)

# Server-Side Apply (SSA) — recommended for CI/CD:
kubectl apply --server-side -f deployment.yaml
# Tracks field ownership on the server (prevents conflicting updates from multiple tools)
# If kubectl and Helm both manage the same Deployment, SSA detects conflicts

# Dry run — preview what would change:
kubectl apply -f deployment.yaml --dry-run=client   # local validation only
kubectl apply -f deployment.yaml --dry-run=server   # full server validation (best)
kubectl diff -f deployment.yaml                      # show diff vs current state
```

---

**Q42. kubectl get, describe, explain — knowing each one.**

```bash
# kubectl get — list resources
kubectl get pods                                    # in default namespace
kubectl get pods -n production                      # specific namespace
kubectl get pods -A                                 # ALL namespaces
kubectl get pods -o wide                            # extra columns (node, IP)
kubectl get pods -o yaml                            # full YAML
kubectl get pods -o json | jq .items[].metadata.name  # JSON + jq
kubectl get pods -o jsonpath='{.items[*].metadata.name}' # jsonpath
kubectl get pods --field-selector=status.phase=Running   # filter by field
kubectl get pods -l app=api,version=v2              # filter by label
kubectl get pods --watch                            # watch for changes
kubectl get pods --sort-by=.metadata.creationTimestamp  # sort
kubectl get all -n production                       # pods, svc, deploy, replicasets
kubectl get events --sort-by='.lastTimestamp' -n production  # recent events

# Custom columns:
kubectl get pods -o custom-columns='NAME:.metadata.name,IMAGE:.spec.containers[0].image,STATUS:.status.phase'

# kubectl describe — human-readable detailed info (includes events!)
kubectl describe pod api-7d9f5b-xyz -n production
# Shows: node, labels, containers, volumes, conditions, events (MOST USEFUL for debugging)
# Key sections: Events (at bottom) — explains WHY a pod is failing

kubectl describe deployment api
kubectl describe node ip-10-0-1-5.ec2.internal     # node pressure, allocatable resources

# kubectl explain — documentation for resource fields
kubectl explain pod                                  # top-level fields
kubectl explain pod.spec                             # pod.spec fields
kubectl explain pod.spec.containers                  # container fields
kubectl explain pod.spec.containers.livenessProbe    # liveness probe fields
kubectl explain deployment.spec.strategy.rollingUpdate
# Great for discovering allowed values without looking up docs
```

---

**Q43. kubectl logs — all important flags.**

```bash
# Basic:
kubectl logs api-pod-xyz
kubectl logs api-pod-xyz -c sidecar          # specific container in multi-container pod
kubectl logs api-pod-xyz --all-containers    # all containers in the pod

# Streaming and filtering:
kubectl logs api-pod-xyz -f                  # follow (stream new logs)
kubectl logs api-pod-xyz --tail=100          # last 100 lines
kubectl logs api-pod-xyz --tail=100 -f       # last 100 lines then follow
kubectl logs api-pod-xyz --since=1h          # last 1 hour
kubectl logs api-pod-xyz --since=30m         # last 30 minutes
kubectl logs api-pod-xyz --since-time="2024-01-15T10:00:00Z"  # since datetime

# Previous container (after crash):
kubectl logs api-pod-xyz --previous          # logs from previous container instance
kubectl logs api-pod-xyz -p                  # short form

# All pods matching a label:
kubectl logs -l app=api -n production        # logs from all pods with app=api
kubectl logs -l app=api -n production --tail=50 -f  # follow all matching pods

# Label selector with max log lines:
kubectl logs -l app=api --max-log-requests=10  # allow 10 concurrent requests

# Practical debugging flow:
kubectl get pods -n production               # see pod status
kubectl describe pod api-xyz -n production   # check events (why not starting?)
kubectl logs api-xyz -n production --previous  # crash logs
kubectl logs api-xyz -n production -f        # watch live
```

---

**Q44. kubectl exec, port-forward, cp — interactive debugging.**

```bash
# kubectl exec — run command in container
kubectl exec -it api-pod-xyz -- sh           # interactive shell (sh, not bash for alpine)
kubectl exec -it api-pod-xyz -- bash         # bash (if available)
kubectl exec -it api-pod-xyz -c sidecar -- sh  # specific container
kubectl exec -it api-pod-xyz -n production -- sh  # specific namespace
kubectl exec api-pod-xyz -- ls /app          # non-interactive, one-off command
kubectl exec api-pod-xyz -- cat /etc/hosts   # inspect networking
kubectl exec api-pod-xyz -- env              # list environment variables
kubectl exec api-pod-xyz -u root -- sh       # run as root (if allowed by security context)

# kubectl port-forward — forward local port to pod/service
kubectl port-forward pod/api-pod-xyz 8080:3000          # local:8080 → pod:3000
kubectl port-forward svc/api-svc 8080:80                # to service (preferred — survives pod restarts)
kubectl port-forward deploy/api 8080:3000               # to deployment
kubectl port-forward svc/postgres 5432:5432 -n production  # DB access from local

# Forward to background:
kubectl port-forward svc/api 8080:80 &
curl http://localhost:8080/health
kill %1    # stop background port-forward

# kubectl cp — copy files to/from containers
kubectl cp api-pod-xyz:/app/logs/app.log ./app.log      # container → local
kubectl cp ./config.json api-pod-xyz:/app/config.json   # local → container
kubectl cp api-pod-xyz:/var/log ./logs/ -n production    # copy directory

# kubectl debug — ephemeral debug containers (K8s 1.23+)
# Add a debug container to a RUNNING pod without modifying the pod spec:
kubectl debug api-pod-xyz -it --image=busybox --target=api
kubectl debug api-pod-xyz -it --image=nicolaka/netshoot  # network debugging tools
# Shares network/process namespace of target container

# Debug a node:
kubectl debug node/ip-10-0-1-5.ec2.internal -it --image=ubuntu
# Mounts host filesystem at /host — examine node-level issues

# Copy pod spec and change image for debugging:
kubectl debug api-pod-xyz --copy-to=debug-pod --set-image=api=ubuntu -it
```

---

**Q45. kubectl rollout — deployments in depth.**

```bash
# Check rollout status:
kubectl rollout status deployment/api              # watch until rollout completes
kubectl rollout status deployment/api -n production --timeout=5m

# View rollout history:
kubectl rollout history deployment/api
# REVISION  CHANGE-CAUSE
# 1         Initial deployment
# 2         Update to v1.5.0: new payment feature
# 3         Hotfix: fix memory leak

kubectl rollout history deployment/api --revision=2  # details of revision 2

# Rollback:
kubectl rollout undo deployment/api                 # rollback to previous revision
kubectl rollout undo deployment/api --to-revision=2 # rollback to specific revision

# Pause/resume (for canary-style manual rollout):
kubectl rollout pause deployment/api               # pause mid-rollout
# (inspect, test, verify)
kubectl rollout resume deployment/api              # continue rollout

# Restart (rolling restart of all pods — useful for picking up ConfigMap changes):
kubectl rollout restart deployment/api
kubectl rollout restart deployment/api -n production

# Force update (even if image tag didn't change):
kubectl patch deployment api -p \
  '{"spec":{"template":{"metadata":{"annotations":{"kubectl.kubernetes.io/restartedAt":"'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'"}}}}}'

# Update image:
kubectl set image deployment/api api=ghcr.io/org/api:2.1.0
kubectl rollout status deployment/api              # watch the rollout
```

---

**Q46. kubectl scale, taint, cordon, drain.**

```bash
# kubectl scale — manual scaling
kubectl scale deployment/api --replicas=10
kubectl scale deployment/api --replicas=0          # scale to zero (maintenance)
kubectl scale statefulset/redis --replicas=3
# Multiple resources at once:
kubectl scale deployment/api deployment/worker --replicas=5

# kubectl autoscale — create HPA
kubectl autoscale deployment/api --min=3 --max=50 --cpu-percent=70
# Creates an HPA resource

# kubectl taint — prevent scheduling on a node
kubectl taint nodes node1 key=value:NoSchedule     # no new pods (unless tolerated)
kubectl taint nodes node1 key=value:NoExecute      # evict existing pods + no new
kubectl taint nodes node1 key=value:PreferNoSchedule  # prefer not to schedule
# Remove taint:
kubectl taint nodes node1 key=value:NoSchedule-    # trailing dash removes it

# kubectl cordon — mark node unschedulable (no new pods, existing stay)
kubectl cordon node1                                # maintenance: stop new pods
kubectl uncordon node1                              # re-enable scheduling

# kubectl drain — gracefully evict all pods from a node
kubectl drain node1 \
  --ignore-daemonsets \         # DaemonSet pods can't be evicted (stay)
  --delete-emptydir-data \      # allow deletion of emptyDir volumes
  --grace-period=30 \           # wait 30s for graceful shutdown
  --timeout=5m                  # give up after 5 minutes
# Use case: node maintenance, patching, decommission
# After drain → node is cordoned + all pods evicted → safe to take offline
kubectl uncordon node1          # after maintenance, re-enable

# kubectl label and annotate:
kubectl label nodes node1 node-type=worker
kubectl label pods api-pod-xyz version=v2 --overwrite
kubectl label pods api-pod-xyz version-         # remove label (dash suffix)
kubectl annotate deployment/api \
  kubernetes.io/change-cause="Release 2.1.0: payment retry" --overwrite
```

---

**Q47. kubectl config — managing multiple clusters.**

```bash
# kubeconfig file: ~/.kube/config
# Contains: clusters, users (credentials), contexts (cluster+user+namespace combo)

# View current context:
kubectl config current-context
kubectl config view                                  # full kubeconfig
kubectl config view --minify                         # only current context

# List contexts:
kubectl config get-contexts
# CURRENT   NAME         CLUSTER      AUTHINFO      NAMESPACE
# *         production   prod-eks     prod-admin     production
#           staging      stg-eks      stg-developer  staging
#           local        minikube     minikube       default

# Switch context:
kubectl config use-context staging
kubectl config use-context production

# Set default namespace for current context:
kubectl config set-context --current --namespace=production

# Create new context:
kubectl config set-cluster new-cluster --server=https://k8s.example.com
kubectl config set-credentials new-user --token=eyJhbGci...
kubectl config set-context new-ctx --cluster=new-cluster --user=new-user --namespace=default

# Merge multiple kubeconfig files:
KUBECONFIG=~/.kube/config:~/.kube/config-staging kubectl config view --flatten > ~/.kube/merged-config

# kubectx (third-party tool for faster switching):
kubectx                 # list contexts
kubectx production      # switch to production
kubectx -               # switch to previous context
kubens                  # list namespaces
kubens production       # switch namespace in current context

# Multiple cluster management in CI/CD:
aws eks update-kubeconfig --name production-cluster --region us-east-1
gcloud container clusters get-credentials production --zone us-central1-a
kubectl config use-context gke_myproject_us-central1-a_production
```

---

**Q48. kubectl advanced: diff, kustomize, api-resources, top.**

```bash
# kubectl diff — show what would change (BEFORE applying)
kubectl diff -f deployment.yaml          # diff between file and cluster state
kubectl diff -f ./manifests/             # diff entire directory
# Uses server-side dry-run — most accurate

# kubectl top — resource usage (requires metrics-server installed)
kubectl top pods                         # CPU/memory of all pods
kubectl top pods -n production           # specific namespace
kubectl top pods -l app=api              # filtered by label
kubectl top pods --containers            # per-container breakdown
kubectl top nodes                        # node-level CPU/memory

# kubectl api-resources — discover all resource types
kubectl api-resources                    # all resources in the cluster
kubectl api-resources --namespaced=true  # only namespace-scoped
kubectl api-resources --namespaced=false # only cluster-scoped
kubectl api-resources -o name | grep cert  # find cert-related resources
kubectl api-resources --api-group=apps   # only resources in 'apps' group

# kubectl api-versions — all available API versions
kubectl api-versions                     # e.g., apps/v1, batch/v1, networking.k8s.io/v1

# kubectl kustomize — apply Kustomize overlays
kubectl apply -k ./overlays/production/  # apply kustomization
kubectl diff -k ./overlays/staging/      # preview kustomize changes
kubectl kustomize ./overlays/production/ # print rendered YAML without applying
```
```yaml
# Kustomize structure:
k8s/
  base/
    deployment.yaml
    service.yaml
    kustomization.yaml
  overlays/
    staging/
      kustomization.yaml    # extends base
      replica-patch.yaml    # patch replicas to 1
    production/
      kustomization.yaml    # extends base
      replica-patch.yaml    # patch replicas to 10
      resource-patch.yaml   # larger resource limits

# base/kustomization.yaml:
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
commonLabels:
  managed-by: kustomize
images:
  - name: myapp
    newTag: latest

# overlays/production/kustomization.yaml:
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: production
resources:
  - ../../base
patches:
  - path: replica-patch.yaml
    target: { kind: Deployment, name: api }
  - path: resource-patch.yaml
images:
  - name: myapp
    newTag: 2.1.0    # override image tag for production
configMapGenerator:
  - name: app-config
    envs: [production.env]
secretGenerator:
  - name: app-secrets
    envs: [production.secrets.env]    # generated secrets (gitignore this file!)
```

---

**Q49. Debugging pods — systematic approach.**

```bash
# STEP 1: Get pod status
kubectl get pods -n production
# STATUS:
# Pending:           not scheduled (resource limits, node selector, taints)
# ContainerCreating: image pulling or volume mounting
# CrashLoopBackOff:  container keeps crashing (check logs --previous)
# OOMKilled:         exceeded memory limit (increase limits or fix memory leak)
# Error:             command failed (non-zero exit code)
# Evicted:           node ran out of resources
# ImagePullBackOff:  can't pull image (wrong tag, missing pull secret, registry down)

# STEP 2: Describe the pod (events section is gold)
kubectl describe pod api-xyz -n production
# Look for:
# Events section at the bottom
# "Failed to pull image" → wrong registry/tag or imagePullSecret missing
# "Insufficient memory" → node doesn't have enough resources
# "0/3 nodes are available" → pod anti-affinity, taints, resource pressure
# "Back-off restarting failed container" → CrashLoopBackOff

# STEP 3: Get logs
kubectl logs api-xyz -n production           # current container
kubectl logs api-xyz -n production --previous  # previous crash instance

# STEP 4: Check events (cluster-wide)
kubectl get events -n production --sort-by='.lastTimestamp'
kubectl get events -n production --field-selector=reason=BackOff

# STEP 5: Check resource usage
kubectl top pod api-xyz -n production --containers
kubectl describe node $(kubectl get pod api-xyz -n production -o jsonpath='{.spec.nodeName}')

# STEP 6: Debug interactively
kubectl exec -it api-xyz -n production -- sh

# Common crash causes and fixes:
# CrashLoopBackOff after config change → check env vars, secrets exist
kubectl exec api-xyz -- env | grep DATABASE_URL

# OOMKilled → check memory usage trend
kubectl top pods -n production --sort-by=memory

# Pending → node resources or anti-affinity
kubectl describe pod api-xyz | grep -A 10 Events

# ImagePullBackOff → verify image exists and pull secret configured
kubectl get secret ghcr-secret -n production -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d
```

---

**Q50. kubectl patch, set, edit — modifying resources.**

```bash
# kubectl set image — update container image
kubectl set image deployment/api api=ghcr.io/org/api:2.1.0 -n production
kubectl set image deployment/api api=ghcr.io/org/api:2.1.0 --record  # deprecated, use annotation

# kubectl set env — update environment variables
kubectl set env deployment/api LOG_LEVEL=debug
kubectl set env deployment/api LOG_LEVEL-        # remove env var

# kubectl edit — open resource in $EDITOR (vim by default)
kubectl edit deployment/api -n production
KUBE_EDITOR=nano kubectl edit deployment/api     # use nano instead

# kubectl patch — update specific fields without opening editor
# JSON merge patch:
kubectl patch deployment/api -p '{"spec":{"replicas":5}}'

# Strategic merge patch (for arrays — merges instead of replaces):
kubectl patch deployment/api --type strategic -p '
  spec:
    template:
      spec:
        containers:
          - name: api
            resources:
              limits:
                memory: "1Gi"'

# JSON patch (RFC 6902 — precise operations):
kubectl patch deployment/api --type json -p '[
  {"op": "replace", "path": "/spec/replicas", "value": 5},
  {"op": "add", "path": "/metadata/annotations/deployment.kubernetes.io~1change-cause",
   "value": "Manual scale to 5"}
]'

# Force rollout by adding annotation:
kubectl patch deployment/api -p \
  "{\"spec\":{\"template\":{\"metadata\":{\"annotations\":{\"force-restart\":\"$(date +%s)\"}}}}}"

# kubectl label / annotate — add metadata
kubectl label deployment/api environment=production tier=backend
kubectl annotate deployment/api \
  kubernetes.io/change-cause="v2.1.0: add payment retry" --overwrite
```


---

## SECTION 4: CI/CD

---

**Q51. GitHub Actions — complete production workflow.**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ["v*.*.*"]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true    # cancel older runs of same branch

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ---- QUALITY GATES ----
  lint-and-type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd "pg_isready -U test"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
      redis:
        image: redis:7-alpine
        options: --health-cmd "redis-cli ping" --health-interval 5s --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20", cache: "npm" }
      - run: npm ci
      - run: npm test -- --coverage --forceExit
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
          NODE_ENV: test
      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: "fs"
          severity: "CRITICAL,HIGH"
          exit-code: "1"
          ignore-unfixed: true

  # ---- BUILD ----
  build:
    needs: [lint-and-type-check, test, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name != 'pull_request'
    outputs:
      image-tag: ${{ steps.meta.outputs.version }}
      image-digest: ${{ steps.push.outputs.digest }}

    permissions:
      contents: read
      packages: write
      id-token: write    # for OIDC/Sigstore signing

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=sha-,format=short
          labels: |
            org.opencontainers.image.title=API Service
            org.opencontainers.image.vendor=MyOrg

      - id: push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true          # SLSA provenance attestation
          sbom: true                # Software Bill of Materials

      # Sign image with Sigstore cosign (keyless OIDC signing):
      - uses: sigstore/cosign-installer@v3
      - run: |
          cosign sign --yes \
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.push.outputs.digest }}

      # Scan the built image:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.push.outputs.digest }}
          severity: "CRITICAL"
          exit-code: "1"

  # ---- DEPLOY STAGING ----
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://api-staging.example.com
    if: github.ref == 'refs/heads/develop'

    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      - run: |
          kubectl set image deployment/api \
            api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }} \
            -n staging
          kubectl rollout status deployment/api -n staging --timeout=5m

  # ---- DEPLOY PRODUCTION ----
  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    if: startsWith(github.ref, 'refs/tags/v')

    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
      - run: |
          kubectl set image deployment/api \
            api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.image-tag }} \
            -n production
          kubectl rollout status deployment/api -n production --timeout=10m
```

---

**Q52. GitLab CI — complete pipeline.**

```yaml
# .gitlab-ci.yml

stages:
  - test
  - build
  - security
  - deploy-staging
  - deploy-production

variables:
  DOCKER_BUILDKIT: "1"
  REGISTRY: $CI_REGISTRY
  IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest

# ---- TEMPLATES ----
.docker-login: &docker-login
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

.k8s-deploy: &k8s-deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $K8S_CONTEXT
    - kubectl set image deployment/api api=$IMAGE -n $NAMESPACE
    - kubectl rollout status deployment/api -n $NAMESPACE --timeout=5m

# ---- TEST ----
test:
  stage: test
  image: node:20-alpine
  services:
    - name: postgres:16-alpine
      alias: postgres
      variables: { POSTGRES_DB: testdb, POSTGRES_USER: test, POSTGRES_PASSWORD: test }
  variables:
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths: [node_modules/]
  script:
    - npm ci
    - npm run lint
    - npm run type-check
    - npm test -- --coverage
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    when: always
    reports:
      junit: coverage/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths: [coverage/]
    expire_in: 1 week

# ---- BUILD ----
build:
  stage: build
  <<: *docker-login
  script:
    - docker buildx build
        --cache-from type=registry,ref=$CI_REGISTRY_IMAGE:cache
        --cache-to   type=registry,ref=$CI_REGISTRY_IMAGE:cache,mode=max
        --build-arg GIT_SHA=$CI_COMMIT_SHORT_SHA
        --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        --tag $IMAGE
        --tag $IMAGE_LATEST
        --push
        .
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG

# ---- SECURITY SCAN ----
trivy-scan:
  stage: security
  needs: [build]
  image: aquasec/trivy:latest
  script:
    - trivy image --severity CRITICAL,HIGH --exit-code 1 --no-progress $IMAGE
  allow_failure: false

dependency-check:
  stage: security
  image: node:20-alpine
  script:
    - npm audit --audit-level=high

# ---- DEPLOY STAGING ----
deploy-staging:
  stage: deploy-staging
  needs: [build, trivy-scan]
  <<: *k8s-deploy
  variables:
    K8S_CONTEXT: $K8S_STAGING_CONTEXT
    NAMESPACE: staging
  environment:
    name: staging
    url: https://api-staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

# ---- DEPLOY PRODUCTION (manual gate) ----
deploy-production:
  stage: deploy-production
  needs: [build, trivy-scan, deploy-staging]
  <<: *k8s-deploy
  variables:
    K8S_CONTEXT: $K8S_PROD_CONTEXT
    NAMESPACE: production
  environment:
    name: production
    url: https://api.example.com
  when: manual       # requires manual approval
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/   # only on version tags
```

---

**Q53. Blue-green and canary deployments — implementation patterns.**

```
BLUE-GREEN DEPLOYMENT:
  Two identical environments: blue (current live) and green (new version).
  Traffic switch is instant (update DNS/load balancer pointer).
  Rollback is instant (switch back to blue).

  Steps:
  1. Both blue and green running simultaneously
  2. Deploy new version to green, run smoke tests
  3. Switch 100% of traffic from blue to green (DNS update or LB rule)
  4. Monitor green for issues
  5. If good: terminate blue (or keep as fallback)
  6. If bad: switch traffic back to blue instantly

  Cost: 2x infrastructure during transition
  Use case: high-stakes deploys where instant rollback is critical (payments, auth)
```
```yaml
# Kubernetes blue-green via Service selector swap:

# Blue deployment (current live):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-blue
spec:
  replicas: 3
  selector:
    matchLabels: { app: api, version: blue }
  template:
    metadata:
      labels: { app: api, version: blue }
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:1.9.0

---
# Green deployment (new version):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
spec:
  replicas: 3
  selector:
    matchLabels: { app: api, version: green }
  template:
    metadata:
      labels: { app: api, version: green }
    spec:
      containers:
        - name: api
          image: ghcr.io/org/api:2.0.0

---
# Service points to BLUE initially:
apiVersion: v1
kind: Service
metadata:
  name: api-svc
spec:
  selector:
    app: api
    version: blue    # ← change to "green" to switch traffic
  ports:
    - port: 80
      targetPort: 3000

# Switch traffic:
kubectl patch svc api-svc -p '{"spec":{"selector":{"version":"green"}}}'
# Rollback:
kubectl patch svc api-svc -p '{"spec":{"selector":{"version":"blue"}}}'
```

```yaml
# CANARY DEPLOYMENT (gradual traffic shift):
# Route small % of traffic to new version, gradually increase

# With Kubernetes + nginx-ingress annotations:
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"  # 10% to canary
    # OR by header: nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: api-canary-svc, port: { number: 80 } }

# Gradual rollout:
# Week 1: 5%  → monitor error rate, latency, business metrics
# Week 2: 25% → looks good? increase
# Week 3: 50% → halfway, validate
# Week 4: 100% → full migration
# Any time: set canary-weight to 0 for instant rollback

# Argo Rollouts (advanced canary/blue-green with automated analysis):
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: { duration: 30m }    # pause 30 min at 5%
        - setWeight: 25
        - pause: { duration: 1h }
        - analysis:
            templates:
              - templateName: error-rate-check
        - setWeight: 100
      analysis:
        templates:
          - templateName: error-rate
        startingStep: 2               # start analysis at step 2
      trafficRouting:
        nginx:
          stableIngress: api-stable
```

---

**Q54. CI/CD security scanning — SAST, DAST, SCA, image scanning.**

```
TYPES OF SECURITY SCANNING IN CI/CD:

1. SCA (Software Composition Analysis) — dependency vulnerabilities
   Tool: npm audit, Snyk, OWASP Dependency Check
   What: finds CVEs in your npm/pip/maven dependencies
   When: after npm install, before build

2. SAST (Static Application Security Testing) — code analysis
   Tool: Semgrep, SonarQube, CodeQL (GitHub)
   What: finds SQL injection, XSS, hardcoded secrets, insecure patterns in your code
   When: on every push/PR (runs on source code)

3. Secret Detection — hardcoded secrets in code
   Tool: TruffleHog, GitLeaks, GitHub secret scanning
   What: finds API keys, passwords, tokens accidentally committed
   When: pre-commit hook + CI scan

4. Container Image Scanning — CVEs in OS packages and libraries
   Tool: Trivy (best open source), Snyk Container, Grype, Docker Scout
   What: scans layers of Docker image for known CVEs
   When: after docker build, before push to registry

5. DAST (Dynamic Application Security Testing) — runtime testing
   Tool: OWASP ZAP, Nuclei
   What: automated penetration testing against running app
   When: against staging environment
```
```yaml
# GitHub Actions — complete security pipeline:
security:
  runs-on: ubuntu-latest
  steps:
    # 1. Dependency audit:
    - run: npm audit --audit-level=high
    - uses: snyk/actions/node@master
      with:
        args: --severity-threshold=high
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

    # 2. SAST with Semgrep:
    - uses: returntocorp/semgrep-action@v1
      with:
        config: "p/nodejs p/typescript p/security-audit"

    # 3. CodeQL (GitHub Advanced Security):
    - uses: github/codeql-action/init@v3
      with:
        languages: javascript
    - uses: github/codeql-action/autobuild@v3
    - uses: github/codeql-action/analyze@v3

    # 4. Secret scanning with TruffleHog:
    - uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: ${{ github.event.repository.default_branch }}

    # 5. Image scanning (after build):
    - uses: aquasecurity/trivy-action@master
      with:
        image-ref: ghcr.io/org/myapp:latest
        format: sarif
        output: trivy-results.sarif
        severity: CRITICAL,HIGH
        exit-code: "1"
        ignore-unfixed: true    # don't fail on unfixable CVEs
    - uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: trivy-results.sarif

    # 6. DAST with OWASP ZAP (against staging):
    - uses: zaproxy/action-full-scan@v0.8.0
      with:
        target: 'https://api-staging.example.com'
        rules_file_name: '.zap/rules.tsv'
        cmd_options: '-a'
```

---

**Q55. Semantic versioning and automated releases.**

```bash
# Semantic Versioning: MAJOR.MINOR.PATCH
# MAJOR: breaking API changes (1.0.0 → 2.0.0)
# MINOR: backward-compatible new features (1.0.0 → 1.1.0)
# PATCH: backward-compatible bug fixes (1.0.0 → 1.0.1)
# Pre-release: 1.0.0-alpha.1, 1.0.0-beta.2, 1.0.0-rc.1

# Conventional Commits (enables automated versioning):
# Format: type(scope): description
# Types:
# feat: new feature → bumps MINOR
# fix: bug fix → bumps PATCH
# feat!: or BREAKING CHANGE footer → bumps MAJOR
# chore, docs, style, refactor, test → no version bump

# Commit examples:
git commit -m "feat(auth): add OAuth2 login"
git commit -m "fix(api): handle null user correctly"
git commit -m "feat!: remove deprecated /v1 endpoints"
git commit -m "feat(payments): add retry logic

BREAKING CHANGE: PaymentService.charge() now returns Promise<Result> instead of throwing"

# Semantic Release — fully automated:
# Reads commits since last tag → determines version bump → creates tag → publishes

# .releaserc.json:
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    ["@semantic-release/npm", { "npmPublish": false }],
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): ${nextRelease.version} [skip ci]"
    }],
    "@semantic-release/github"
  ]
}

# GitHub Actions integration:
release:
  needs: [build]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  permissions:
    contents: write
    issues: write
    pull-requests: write
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0            # fetch full history for commit analysis
    - uses: actions/setup-node@v4
      with: { node-version: "20" }
    - run: npm ci
    - run: npx semantic-release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

**Q56. GitOps — ArgoCD and Flux CD.**

```yaml
# ARGOCD:
# App of Apps pattern — one ArgoCD Application manages all other Applications:

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-configs.git
    targetRevision: HEAD
    path: apps                  # folder containing Application manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true               # delete resources removed from git
      selfHeal: true            # revert manual changes to match git
    retry:
      limit: 5
      backoff:
        duration: 5s
        maxDuration: 3m
        factor: 2

---
# ApplicationSet — template-based multi-environment apps:
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: api-app
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: staging
            namespace: staging
            imageTag: develop
          - env: production
            namespace: production
            imageTag: latest
  template:
    metadata:
      name: "api-{{env}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/org/k8s-configs.git
        targetRevision: HEAD
        path: "apps/api/{{env}}"
        helm:
          values: |
            image:
              tag: "{{imageTag}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{namespace}}"
      syncPolicy:
        automated: { prune: true, selfHeal: true }
```

```yaml
# FLUX CD (alternative GitOps tool):
# Flux is a set of Kubernetes controllers — no separate UI (use CLI)

# GitRepository source:
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: k8s-configs
  namespace: flux-system
spec:
  interval: 1m                    # check for changes every minute
  url: https://github.com/org/k8s-configs
  ref:
    branch: main
  secretRef:
    name: github-credentials      # for private repos

---
# Kustomization (applies Kustomize overlays from the GitRepository):
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: production-apps
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: k8s-configs
  path: ./overlays/production     # path in the git repo
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: api
      namespace: production
  timeout: 10m

---
# HelmRelease (deploy a Helm chart from a chart repository):
apiVersion: helm.toolkit.fluxcd.io/v2beta2
kind: HelmRelease
metadata:
  name: api
  namespace: production
spec:
  interval: 10m
  chart:
    spec:
      chart: my-api
      version: ">=1.0.0"
      sourceRef:
        kind: HelmRepository
        name: my-org-charts
  values:
    image:
      repository: ghcr.io/org/api
      tag: 2.1.0
    replicaCount: 3

# Flux CLI:
flux get kustomizations              # list all kustomizations
flux reconcile kustomization apps    # force sync
flux logs --level=error              # view controller logs
flux diff kustomization apps         # show pending changes
```


---

## SECTION 5: INFRASTRUCTURE AS CODE

---

**Q57. Terraform — complete production guide.**

```hcl
# TERRAFORM CORE CONCEPTS:
# Provider: plugin to interact with AWS/GCP/Azure/etc
# Resource: infrastructure object (aws_instance, aws_s3_bucket)
# Data source: read existing infrastructure
# Module: reusable group of resources
# State: terraform.tfstate — tracks what Terraform manages
# Plan: preview changes before applying
# Backend: where state is stored (S3, GCS, Terraform Cloud)

# ---- State management (critical) ----
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state in S3 with DynamoDB locking:
  backend "s3" {
    bucket         = "myorg-terraform-state"
    key            = "production/api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456:key/abc123"

    # State locking — prevents concurrent applies:
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = var.environment
      Project     = var.project_name
    }
  }
}

# ---- Variables ----
variable "environment"  { type = string }
variable "aws_region"   { type = string, default = "us-east-1" }
variable "project_name" { type = string }
variable "db_password" {
  type      = string
  sensitive = true    # won't appear in logs or plan output
}

# ---- Locals ----
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    CreatedAt   = timestamp()
  }
}

# ---- Data sources ----
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
}

# Reference: data.aws_caller_identity.current.account_id

# ---- Resources ----
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${local.name_prefix}-vpc" }
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = { Name = "${local.name_prefix}-private-${count.index}" }
}

# ---- Outputs ----
output "vpc_id"          { value = aws_vpc.main.id }
output "private_subnets" { value = aws_subnet.private[*].id }
output "account_id"      { value = data.aws_caller_identity.current.account_id }

# ---- Modules ----
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${local.name_prefix}-eks"
  cluster_version = "1.29"

  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.private[*].id

  eks_managed_node_groups = {
    workers = {
      min_size       = 2
      max_size       = 20
      desired_size   = 3
      instance_types = ["m5.xlarge"]
      capacity_type  = "ON_DEMAND"
    }
    spot_workers = {
      min_size       = 0
      max_size       = 50
      desired_size   = 0
      instance_types = ["c5.xlarge", "c5.2xlarge", "m5.xlarge"]
      capacity_type  = "SPOT"
    }
  }
}
```

```bash
# ---- Terraform workflow ----
terraform init                    # initialize, download providers + modules
terraform init -upgrade           # upgrade providers to latest allowed version
terraform validate                # syntax + type validation
terraform fmt -recursive          # format all .tf files
terraform plan                    # preview changes
terraform plan -out=tfplan        # save plan (for apply in CI/CD)
terraform apply                   # interactive apply
terraform apply tfplan            # apply saved plan (non-interactive)
terraform apply -auto-approve     # skip confirmation (CI/CD)
terraform destroy                 # destroy all resources
terraform destroy -target=aws_instance.web  # destroy specific resource

# State operations:
terraform state list              # list managed resources
terraform state show aws_vpc.main # show state for specific resource
terraform state mv aws_s3_bucket.old aws_s3_bucket.new  # rename
terraform state rm aws_instance.legacy  # remove from state (but don't destroy)
terraform import aws_s3_bucket.main mybucket  # import existing resource

# Workspaces (separate state per environment):
terraform workspace new staging
terraform workspace new production
terraform workspace select staging
terraform workspace list
# Use: var.environment = terraform.workspace

# Targeted apply (only specific resources):
terraform apply -target=module.eks -target=aws_vpc.main
```

---

**Q58. Terraform modules — structuring a production codebase.**

```
MONOREPO STRUCTURE:
infra/
  modules/           # reusable modules (shared across environments)
    vpc/
      main.tf
      variables.tf
      outputs.tf
      README.md
    eks/
    rds/
    redis/
    s3-bucket/
  environments/      # environment-specific configuration
    staging/
      main.tf        # calls modules with staging config
      variables.tf
      terraform.tfvars  # staging values (committed)
      backend.tf
    production/
      main.tf
      variables.tf
      terraform.tfvars.example  # template (actual values in Secrets Manager)
      backend.tf
  global/            # account-wide resources (IAM, Route53)
    main.tf

# ---- Example module: modules/rds/main.tf ----
variable "identifier"   { type = string }
variable "environment"  { type = string }
variable "subnet_ids"   { type = list(string) }
variable "vpc_id"       { type = string }
variable "db_name"      { type = string }
variable "db_username"  { type = string }
variable "db_password"  { type = string, sensitive = true }
variable "instance_class" {
  type    = string
  default = "db.t3.medium"
}
variable "multi_az" {
  type    = bool
  default = false
}

resource "aws_db_instance" "this" {
  identifier     = var.identifier
  engine         = "postgres"
  engine_version = "16"
  instance_class = var.instance_class

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  multi_az              = var.multi_az
  deletion_protection   = var.environment == "production"
  skip_final_snapshot   = var.environment != "production"

  backup_retention_period = var.environment == "production" ? 14 : 1
  storage_encrypted       = true

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.this.name
}

output "endpoint" { value = aws_db_instance.this.endpoint }
output "port"     { value = aws_db_instance.this.port }

# ---- Using the module: environments/production/main.tf ----
module "rds" {
  source = "../../modules/rds"

  identifier     = "myapp-production"
  environment    = "production"
  subnet_ids     = module.vpc.private_subnets
  vpc_id         = module.vpc.vpc_id
  db_name        = "myapp"
  db_username    = var.db_username
  db_password    = data.aws_secretsmanager_secret_version.db_pass.secret_string
  instance_class = "db.r6g.large"
  multi_az       = true
}
```

---

**Q59. Pulumi — infrastructure as real code (TypeScript).**

```typescript
// Pulumi: IaC using actual programming languages (TypeScript, Python, Go, C#)
// vs Terraform: domain-specific HCL language

// pulumi/index.ts:
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as eks from "@pulumi/eks";
import * as k8s from "@pulumi/kubernetes";

const config = new pulumi.Config();
const env = config.require("environment");   // pulumi config set environment production

// VPC:
const vpc = new awsx.ec2.Vpc(`myapp-${env}`, {
  numberOfAvailabilityZones: 3,
  subnetStrategy: awsx.ec2.SubnetAllocationStrategy.Auto,
  natGateways: { strategy: awsx.ec2.NatGatewayStrategy.OnePerAz },
});

// EKS Cluster:
const cluster = new eks.Cluster(`myapp-${env}`, {
  vpcId:                 vpc.vpcId,
  privateSubnetIds:      vpc.privateSubnetIds,
  instanceType:          "m5.xlarge",
  desiredCapacity:       3,
  minSize:               2,
  maxSize:               20,
  endpointPrivateAccess: true,
  endpointPublicAccess:  false,
});

// RDS:
const db = new aws.rds.Instance(`myapp-${env}-db`, {
  engine:                "postgres",
  engineVersion:         "16",
  instanceClass:         env === "production" ? "db.r6g.large" : "db.t3.medium",
  allocatedStorage:      env === "production" ? 100 : 20,
  dbName:                "myapp",
  username:              config.require("dbUsername"),
  password:              config.requireSecret("dbPassword"),   // encrypted in state
  multiAz:               env === "production",
  deletionProtection:    env === "production",
  backupRetentionPeriod: env === "production" ? 14 : 1,
  storageEncrypted:      true,
  dbSubnetGroupName:     dbSubnetGroup.name,
  vpcSecurityGroupIds:   [dbSg.id],
});

// K8s Deployment using the EKS cluster:
const k8sProvider = new k8s.Provider("eks-k8s", {
  kubeconfig: cluster.kubeconfig,
});

const apiDeployment = new k8s.apps.v1.Deployment("api", {
  metadata: { namespace: "production" },
  spec: {
    replicas: env === "production" ? 3 : 1,
    selector: { matchLabels: { app: "api" } },
    template: {
      metadata: { labels: { app: "api" } },
      spec: {
        containers: [{
          name:  "api",
          image: `ghcr.io/org/api:${config.require("imageTag")}`,
          resources: {
            requests: { memory: "256Mi", cpu: "100m" },
            limits:   { memory: "512Mi", cpu: "500m" },
          },
        }],
      },
    },
  },
}, { provider: k8sProvider });

// Pulumi advantages over Terraform:
// - Real loops and conditions (no HCL for_each limitations)
// - TypeScript type checking catches config errors at compile time
// - Pulumi state can be stored in Pulumi Cloud or self-hosted S3
// - Component resources (reusable higher-level abstractions)
// - Testing with Jest/pytest/etc. (import as a module and test)
export const clusterName = cluster.eksCluster.name;
export const dbEndpoint  = db.endpoint;
```

---

**Q60. OpenTofu — open source Terraform fork.**

```
OpenTofu: open source fork of Terraform (after HashiCorp changed Terraform's license
to BSL 1.1 in August 2023 — no longer open source by OSI definition).
Maintained by the Linux Foundation and community.

COMPATIBILITY:
  OpenTofu 1.6+ is compatible with Terraform 1.5 syntax and state files.
  Most Terraform providers work with OpenTofu unchanged.
  Migration is typically: replace `terraform` with `tofu` in commands.

DIFFERENCES (OpenTofu 1.7+):
  - Encrypted state (encrypt blocks in backend config)
  - Provider-defined functions
  - Removed (formerly Terraform) commercial features (Sentinel, module sharing via registry)
  - All test files use .tftest.hcl (same as Terraform 1.7)

MIGRATION:
```
```bash
# Install OpenTofu:
brew install opentofu    # macOS
# or via official installer: https://opentofu.org/docs/intro/install/

# Existing Terraform project:
cd existing-terraform-project/
tofu init           # reads same terraform.tfstate and .terraform.lock.hcl
tofu plan           # same output as terraform plan
tofu apply          # same as terraform apply

# Replace `terraform` → `tofu` in CI/CD scripts
# No state migration needed — same file format

# Encrypted state (OpenTofu 1.7+):
terraform {
  backend "s3" {
    bucket = "state-bucket"
    key    = "production.tfstate"
    region = "us-east-1"
  }
  encryption {
    key_provider "pbkdf2" "master" {
      passphrase = var.state_passphrase
    }
    method "aes_gcm" "default" {
      keys = key_provider.pbkdf2.master
    }
    state {
      method = method.aes_gcm.default
    }
  }
}
```

---

**Q61. Helm — advanced patterns and templating.**

```yaml
# Helm chart TESTING:
# templates/tests/connection-test.yaml:
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-api.fullname" . }}-test"
  annotations:
    "helm.sh/hook": test                   # runs on: helm test
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
    - name: wget
      image: busybox
      command:
        - wget
        - "-qO-"
        - "http://{{ include "my-api.fullname" . }}:{{ .Values.service.port }}/health"

# helm test myapp -n production  → runs the test pod, fails if exit != 0

# Helm HOOKS — lifecycle management:
# pre-install / post-install / pre-upgrade / post-upgrade / pre-delete / post-delete

# templates/migrations.yaml:
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration-{{ .Release.Revision }}
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "-5"                # lower = runs first
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: migration
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["node", "dist/migrate.js"]
          envFrom:
            - secretRef: { name: "{{ include "my-api.fullname" . }}-secrets" }

# Helm LIBRARY CHARTS — shared templates across multiple charts:
# Chart.yaml: type: library
# Other charts declare it as a dependency:
dependencies:
  - name: common
    version: "1.x.x"
    repository: "https://charts.myorg.com"

# Use shared templates:
# templates/deployment.yaml:
{{- include "common.deployment" . }}

# HELM DIFF PLUGIN:
helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade myapp ./chart -f values-prod.yaml  # show what would change

# HELM SECRETS PLUGIN (encrypt secrets with sops):
helm plugin install https://github.com/jkroepke/helm-secrets
helm secrets install myapp ./chart -f secrets.yaml   # secrets.yaml encrypted with sops
```


---

## SECTION 6: CLOUD / AWS

---

**Q62. AWS core services — complete reference for backend engineers.**

```
COMPUTE:
  EC2: virtual machines. Full OS control. Use when: need specific OS/kernel,
       stateful workloads, existing lift-and-shift.
  ECS: AWS-native container orchestration. Simpler than K8s. Managed by AWS.
  EKS: managed Kubernetes. Portable, industry standard. More operational overhead.
  Fargate: serverless containers (no EC2 management). Works with ECS and EKS.
  Lambda: serverless functions. Pay per 100ms. Cold start: 100ms-1s.
           Max 15min timeout, 10GB memory, 512MB-10GB tmp storage.
  App Runner: managed containerized apps. Simplest deployment path.

STORAGE:
  S3: object storage. 99.999999999% durability. Unlimited scale. 
      Classes: Standard, IA (Infrequent Access), Glacier (archive).
  EBS: block storage. Attached to single EC2. Types: gp3 (most), io2 (high IOPS DB).
  EFS: managed NFS. Multi-AZ. Multiple instances can mount simultaneously.
  FSx: managed Lustre (HPC), Windows FS, NetApp ONTAP, OpenZFS.

DATABASES:
  RDS: managed relational (PostgreSQL, MySQL, SQL Server, Oracle, MariaDB).
       Multi-AZ: synchronous standby in other AZ, failover in ~1-2 minutes.
       Read Replicas: async replication for read scaling (up to 5 for MySQL/Postgres).
  Aurora: AWS MySQL/PostgreSQL compatible. 5× MySQL throughput.
           Serverless v2: scales in 0.5 ACU increments, perfect for variable load.
  DynamoDB: managed NoSQL. Single-digit ms at any scale. Global tables for multi-region.
  ElastiCache: managed Redis (cluster mode) or Memcached.
  Keyspaces: managed Cassandra.
  DocumentDB: managed MongoDB-compatible.
  Neptune: managed graph database.
  Timestream: managed time-series database.

NETWORKING:
  VPC: virtual private cloud. Private network in AWS. Subnets, route tables, NACLs.
  ALB (Application Load Balancer): L7, path/host routing, WebSocket, mTLS, WAF integration.
  NLB (Network Load Balancer): L4, ultra-low latency, static IP, TCP/UDP/TLS.
  GLB (Gateway Load Balancer): L3, for inline appliances (firewalls, IDS/IPS).
  CloudFront: CDN. Global edge locations. Caches static + dynamic content.
  Route53: DNS + health checks + routing policies (latency, geolocation, failover).
  API Gateway: REST/HTTP/WebSocket API management. Throttling, auth, caching.
  Direct Connect: dedicated network connection from data center to AWS.
  VPN: site-to-site or client VPN to your VPC.
  Transit Gateway: hub connecting multiple VPCs and on-premise networks.
  PrivateLink: private connectivity to AWS services (no internet traversal).

MESSAGING:
  SQS: fully managed message queue.
       Standard: at-least-once delivery, best-effort ordering, unlimited throughput.
       FIFO: exactly-once, strict ordering, 3000 msg/s (300 without batching).
       Visibility timeout: message hidden during processing (default 30s).
       Dead Letter Queue (DLQ): messages that fail N times go here.
  SNS: pub/sub. Fan-out to SQS, Lambda, email, HTTP, SMS.
  Kinesis Data Streams: real-time streaming. Shards (1MB/s in, 2MB/s out each).
  EventBridge: event bus. Rule-based routing to 20+ targets. SaaS integrations.
  MSK: managed Kafka.
  MQ: managed ActiveMQ and RabbitMQ.

SECURITY:
  IAM: users, groups, roles, policies. Always use roles, not users, for services.
  Cognito: user pools (authentication) + identity pools (federated AWS access).
  ACM: managed TLS certificates. Auto-renewal. Free for ALB/CloudFront.
  KMS: key management. CMK encryption. Key rotation. CloudHSM for hardware.
  Secrets Manager: store and auto-rotate secrets.
  Parameter Store (SSM): hierarchical config + secrets (cheaper than Secrets Manager).
  WAF: layer 7 firewall. Managed rule groups. Rate limiting. IP blocking.
  Shield: DDoS protection. Standard (free), Advanced ($3000/month + DRT support).
  GuardDuty: ML-based threat detection. Analyzes VPC flow logs, CloudTrail, DNS.
  Security Hub: security posture management. Aggregates findings.
  Inspector: automated vulnerability assessment for EC2, ECS, Lambda.
  Macie: ML-based sensitive data discovery in S3 (PII, financial data).
```

---

**Q63. AWS IAM — deep dive: policies, roles, and least privilege.**

```json
// POLICY STRUCTURE:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadWrite",           // optional identifier
      "Effect": "Allow",                   // Allow or Deny
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::myapp-${aws:PrincipalTag/Environment}-data",
        "arn:aws:s3:::myapp-${aws:PrincipalTag/Environment}-data/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:prefix": ["uploads/"]
        },
        "Bool": {
          "aws:SecureTransport": "true"     // require HTTPS
        },
        "IpAddress": {
          "aws:SourceIp": ["10.0.0.0/8"]  // restrict to internal network
        },
        "DateLessThan": {
          "aws:CurrentTime": "2025-12-31T00:00:00Z"  // time-limited
        }
      }
    },
    {
      "Effect": "Deny",                    // explicit Deny overrides any Allow
      "Action": "s3:DeleteBucket",
      "Resource": "*"                      // no one can delete buckets
    }
  ]
}
```
```bash
# POLICY TYPES:
# Identity-based: attached to user/role (what can this principal DO?)
# Resource-based:  attached to resource (who can ACCESS this resource?)
#   - S3 bucket policies, SQS policies, Lambda resource policies
# Permission boundaries: maximum permissions an identity can have
# Service Control Policies (SCP): org-level guardrails (AWS Organizations)
# Session policies: temporary restriction for assumed roles

# IAM ROLES PATTERN FOR ECS/EKS:
# Task execution role: permissions for ECS agent (pull image, write logs)
# Task role: permissions for the app code (read S3, write DynamoDB)

# IRSA (IAM Roles for Service Accounts) — fine-grained K8s pod access to AWS:
aws iam create-role --role-name api-production \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/ABC123"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/ABC123:sub": "system:serviceaccount:production:api-sa",
          "oidc.eks.us-east-1.amazonaws.com/id/ABC123:aud": "sts.amazonaws.com"
        }
      }
    }]
  }'

# Annotate K8s ServiceAccount:
kubectl annotate serviceaccount api-sa -n production \
  eks.amazonaws.com/role-arn=arn:aws:iam::123456:role/api-production

# IAM BEST PRACTICES:
# 1. Root account: enable MFA, no access keys, only for account-level tasks
# 2. Break-glass account: separate admin IAM user, MFA required, rarely used
# 3. Federation: use SSO (AWS IAM Identity Center) instead of IAM users
# 4. Least privilege: start with no permissions, add as needed
# 5. Roles over users: services get roles, not long-lived access keys
# 6. Permission boundaries: prevent privilege escalation in delegated admin scenarios
# 7. AWS Config + CloudTrail: audit all API calls and config changes
# 8. Access Analyzer: identify unintended public or cross-account access
```

---

**Q64. AWS EKS — production setup.**

```bash
# Create EKS cluster with eksctl:
eksctl create cluster \
  --name production \
  --region us-east-1 \
  --version 1.29 \
  --nodegroup-name workers \
  --node-type m5.xlarge \
  --nodes 3 --nodes-min 2 --nodes-max 20 \
  --managed \                    # managed node groups (AWS patches nodes)
  --with-oidc \                  # enable OIDC for IRSA
  --ssh-access \
  --asg-access \                 # allow cluster autoscaler to manage ASG
  --alb-ingress-access \         # allow ALB ingress controller
  --full-ecr-access \            # allow ECR image pull
  --enable-ssm                   # allow SSM Session Manager for node access

# Install essential add-ons:
# 1. AWS Load Balancer Controller:
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=production \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller

# 2. EBS CSI Driver (persistent volumes on EKS):
eksctl create addon --name aws-ebs-csi-driver --cluster production \
  --service-account-role-arn arn:aws:iam::123456:role/ebs-csi-role

# 3. Cluster Autoscaler or Karpenter:
helm install cluster-autoscaler autoscaler/cluster-autoscaler \
  --set autoDiscovery.clusterName=production \
  --set awsRegion=us-east-1

# 4. External DNS:
helm install external-dns bitnami/external-dns \
  --set provider=aws \
  --set aws.region=us-east-1

# 5. cert-manager (TLS certificates):
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true

# 6. External Secrets Operator:
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets --create-namespace

# EKS UPGRADE STRATEGY:
# 1. Check add-on compatibility with new K8s version
# 2. Update node groups one at a time (blue-green node groups)
# 3. Test in staging first
# 4. Announce maintenance window
# eksctl upgrade cluster --name production --version 1.30 --approve
# eksctl upgrade nodegroup --cluster production --name workers --kubernetes-version 1.30
```

---

**Q65. AWS Lambda — advanced patterns.**

```javascript
// COLD START OPTIMIZATION:
// Problem: Lambda creates new container on first invocation → 100ms-2s delay

// Mitigation strategies:

// 1. Provisioned Concurrency (eliminates cold starts):
// aws lambda put-provisioned-concurrency-config \
//   --function-name my-function \
//   --qualifier production \
//   --provisioned-concurrent-executions 10

// 2. ARM64 architecture (faster cold start + cheaper):
// Runtime: nodejs20.x on arm64
// Cost: 20% cheaper than x86_64

// 3. Keep dependencies minimal (smaller deployment package = faster init):
// BAD: import all of lodash, aws-sdk v2 (huge)
// GOOD: import { DynamoDBClient } from "@aws-sdk/client-dynamodb" (tree-shakeable)

// 4. Move heavy init outside handler (persists across invocations):
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

// Initialized ONCE when Lambda container starts, reused across invocations:
const client = new DynamoDBClient({ region: process.env.AWS_REGION });
const ddb = DynamoDBDocumentClient.from(client);
let dbConnection; // database connection pool

async function getDbConnection() {
  if (!dbConnection) {
    dbConnection = await createConnection(process.env.DATABASE_URL);
  }
  return dbConnection;
}

// Lambda handler:
export const handler = async (event, context) => {
  // context.callbackWaitsForEmptyEventLoop = false; // don't wait for DB connections to close

  const db = await getDbConnection();

  // Process event...
  const { httpMethod, body, pathParameters } = event;

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({ message: "OK" }),
  };
};

// LAMBDA PATTERNS:
// Fan-out: SNS → multiple Lambda functions (parallel processing)
// Queue-triggered: SQS → Lambda (automatic scaling, batch processing)
// Stream-triggered: Kinesis/DynamoDB Streams → Lambda (real-time processing)
// Scheduled: EventBridge rule → Lambda (cron jobs)
// API: API Gateway → Lambda (serverless REST API)
// Edge: Lambda@Edge (CloudFront) → auth, URL rewriting, A/B testing

// LAMBDA POWER TUNING:
// Use aws-lambda-power-tuning to find optimal memory size
// Higher memory = more CPU = faster execution = potentially cheaper
// 3008MB Lambda can be cheaper than 512MB if execution time is 4x faster
```


---

## SECTION 7: MONITORING & OBSERVABILITY

---

**Q66. The four golden signals and observability pillars.**

```
THE FOUR GOLDEN SIGNALS (Google SRE):

1. LATENCY — time to serve a request
   - Track SUCCESS latency separately from ERROR latency
   - Use percentiles (P50, P95, P99), not averages (averages hide outliers)
   - P99 = 99% of requests are faster than this value
   - Target: P99 < 200ms for API, P99 < 2s for complex operations

2. TRAFFIC — demand on the system
   - HTTP: requests per second (RPS)
   - Streaming: messages per second, bytes per second
   - Database: queries per second, transactions per second
   - Goal: understand baseline and detect traffic anomalies

3. ERRORS — rate of failed requests
   - Explicit errors: HTTP 5xx, exceptions, timeout errors
   - Implicit errors: HTTP 200 but wrong data, slow degraded responses
   - Target: < 0.1% error rate for most services

4. SATURATION — how "full" the service is
   - CPU: above 80% → may need more capacity
   - Memory: above 80% → risk of OOM
   - Disk: above 80% → risk of writes failing
   - Queue depth: growing → consumers not keeping up
   - Connection pool: exhausted → requests queuing

---

THE THREE PILLARS OF OBSERVABILITY:
  Logs:    what happened (structured events with context)
  Metrics: how much/how often (numeric time-series data)
  Traces:  how long each step took (distributed request flows)

RED METHOD (services):
  Rate:     requests per second
  Errors:   errors per second (or error %)
  Duration: distribution of latency (histogram)

USE METHOD (resources/infrastructure):
  Utilization: % busy (CPU time, disk bandwidth)
  Saturation:  queue depth, wait time
  Errors:      error events (disk errors, dropped packets)

OBSERVABILITY MATURITY:
  Level 0: no monitoring (flying blind)
  Level 1: uptime checks, basic alerting
  Level 2: metrics + dashboards (Prometheus + Grafana)
  Level 3: structured logging + log aggregation (ELK/Loki)
  Level 4: distributed tracing (Jaeger/Tempo)
  Level 5: continuous profiling (Pyroscope/Parca) + business metrics
```

---

**Q67. Prometheus and Grafana — complete setup and best practices.**

```yaml
# prometheus.yml — production configuration:
global:
  scrape_interval:     15s
  evaluation_interval: 15s
  external_labels:
    cluster: production
    region:  us-east-1

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
      timeout: 10s

rule_files:
  - /etc/prometheus/rules/*.yml

scrape_configs:
  # Kubernetes pod auto-discovery:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: [production, staging]
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape: "true" annotation:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Use custom path from annotation:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      # Use custom port from annotation:
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      # Add pod metadata as labels:
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

  # Node exporter (host metrics):
  - job_name: node-exporter
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
```

```yaml
# Alerting rules — production-ready:
groups:
  - name: api-alerts
    rules:
      # Error rate > 5% for 5 minutes:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary:     "High error rate for {{ $labels.service }}"
          description: "Error rate: {{ $value | humanizePercentage }}"
          runbook:     "https://runbooks.example.com/high-error-rate"

      # P99 latency > 2s for 10 minutes:
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          ) > 2
        for: 10m
        labels: { severity: warning }
        annotations:
          summary: "High P99 latency for {{ $labels.service }}: {{ $value | humanizeDuration }}"

      # Pod crash looping:
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 15 > 0
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping"

      # Node disk > 85%:
      - alert: NodeDiskPressure
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.15
        for: 15m
        labels: { severity: warning }
        annotations:
          summary: "Node {{ $labels.instance }} disk usage above 85%"

      # Kafka consumer lag:
      - alert: KafkaConsumerLag
        expr: kafka_consumer_group_lag_sum > 50000
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Kafka consumer group {{ $labels.group }} lag: {{ $value }}"
```

---

**Q68. OpenTelemetry — complete Node.js instrumentation.**

```javascript
// tracing.ts — initialize BEFORE any other imports:
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-proto";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-proto";
import { OTLPLogExporter } from "@opentelemetry/exporter-logs-otlp-proto";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";
import { BatchLogRecordProcessor } from "@opentelemetry/sdk-logs";
import { Resource } from "@opentelemetry/resources";
import { SEMRESATTRS_SERVICE_NAME, SEMRESATTRS_SERVICE_VERSION, SEMRESATTRS_DEPLOYMENT_ENVIRONMENT } from "@opentelemetry/semantic-conventions";
import { HttpInstrumentation } from "@opentelemetry/instrumentation-http";
import { ExpressInstrumentation } from "@opentelemetry/instrumentation-express";
import { PgInstrumentation } from "@opentelemetry/instrumentation-pg";
import { RedisInstrumentation } from "@opentelemetry/instrumentation-redis-4";
import { KafkaJsInstrumentation } from "@opentelemetry/instrumentation-kafkajs";
import { AmqplibInstrumentation } from "@opentelemetry/instrumentation-amqplib";

const OTEL_ENDPOINT = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://otel-collector:4318";

const sdk = new NodeSDK({
  resource: new Resource({
    [SEMRESATTRS_SERVICE_NAME]:              process.env.SERVICE_NAME ?? "api",
    [SEMRESATTRS_SERVICE_VERSION]:           process.env.npm_package_version ?? "unknown",
    [SEMRESATTRS_DEPLOYMENT_ENVIRONMENT]:    process.env.NODE_ENV ?? "development",
    "service.instance.id":                   process.env.POD_NAME ?? require("os").hostname(),
    "k8s.namespace.name":                    process.env.POD_NAMESPACE ?? "local",
  }),

  traceExporter: new OTLPTraceExporter({
    url: `${OTEL_ENDPOINT}/v1/traces`,
  }),

  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({ url: `${OTEL_ENDPOINT}/v1/metrics` }),
    exportIntervalMillis: 15_000,
  }),

  logRecordProcessor: new BatchLogRecordProcessor(
    new OTLPLogExporter({ url: `${OTEL_ENDPOINT}/v1/logs` })
  ),

  instrumentations: [
    new HttpInstrumentation({
      ignoreIncomingRequestHook: (req) =>
        req.url === "/health" || req.url === "/metrics",   // don't trace health checks
      requestHook: (span, req) => {
        span.setAttribute("http.request.id", req.headers["x-request-id"] as string);
      },
    }),
    new ExpressInstrumentation({
      requestHook: (span, info) => {
        span.setAttribute("http.route", info.route);
      },
    }),
    new PgInstrumentation({ enhancedDatabaseReporting: true }),  // include query in spans
    new RedisInstrumentation(),
    new KafkaJsInstrumentation(),
    new AmqplibInstrumentation(),
  ],
});

sdk.start();

// Graceful shutdown:
process.on("SIGTERM", async () => {
  await sdk.shutdown();
  process.exit(0);
});

// --- MANUAL INSTRUMENTATION ---
import { trace, SpanStatusCode, SpanKind, context, propagation } from "@opentelemetry/api";

const tracer = trace.getTracer("order-service", "1.0.0");

async function processPayment(orderId: string, amount: number): Promise<void> {
  const span = tracer.startSpan("processPayment", {
    kind: SpanKind.INTERNAL,
    attributes: {
      "order.id":     orderId,
      "payment.amount": amount,
      "payment.currency": "USD",
    },
  });

  // Make child span the active span in this context:
  await context.with(trace.setSpan(context.active(), span), async () => {
    try {
      await chargeCard(amount);  // nested calls create child spans automatically
      await updateOrderStatus(orderId, "paid");

      span.setStatus({ code: SpanStatusCode.OK });
      span.setAttributes({ "payment.status": "success" });
    } catch (err) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: (err as Error).message });
      span.recordException(err as Error);
      throw err;
    } finally {
      span.end();
    }
  });
}

// Propagate trace context to downstream HTTP calls:
async function callDownstreamService(url: string): Promise<Response> {
  const headers: Record<string, string> = {};
  propagation.inject(context.active(), headers);   // injects traceparent, tracestate headers
  return fetch(url, { headers });
}
```

---

**Q69. ELK Stack and Loki — structured logging.**

```javascript
// STRUCTURED LOGGING — output JSON logs (don't use console.log in production)

// pino (fastest Node.js logger):
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  // In production: output as JSON (parsed by log aggregators)
  // In development: output as pretty (human-readable)
  transport: process.env.NODE_ENV === "development"
    ? { target: "pino-pretty", options: { colorize: true } }
    : undefined,

  // Redact sensitive fields automatically:
  redact: {
    paths: ["req.headers.authorization", "req.body.password", "res.headers['set-cookie']"],
    censor: "[REDACTED]",
  },

  // Add base fields to every log:
  base: {
    service: process.env.SERVICE_NAME ?? "api",
    version: process.env.npm_package_version,
    environment: process.env.NODE_ENV,
    pid: process.pid,
  },
});

// Express integration:
import pinoHttp from "pino-http";
app.use(pinoHttp({
  logger,
  // Enrich request logs:
  customProps: (req) => ({
    userId:    (req as any).user?.id,
    requestId: req.headers["x-request-id"],
    traceId:   trace.getActiveSpan()?.spanContext().traceId,  // correlate with traces!
  }),
  // Don't log health checks:
  autoLogging: {
    ignore: (req) => req.url === "/health",
  },
}));

// Structured log usage:
logger.info({ orderId: "ord_123", amount: 50.00 }, "Payment processed");
logger.error({ err, userId: "usr_456", operation: "createOrder" }, "Failed to create order");
logger.warn({ memoryUsage: process.memoryUsage().heapUsed / 1024 / 1024 }, "High memory usage");

// LOG FORMAT (what goes to Elasticsearch/Loki):
// {
//   "level": "info",
//   "time": "2024-01-15T10:30:00.000Z",
//   "service": "api",
//   "version": "2.1.0",
//   "environment": "production",
//   "traceId": "abc123def456",      ← CRITICAL: ties logs to traces
//   "requestId": "req_789",
//   "userId": "usr_456",
//   "orderId": "ord_123",
//   "amount": 50.00,
//   "msg": "Payment processed",
//   "responseTime": 145
// }
```

```yaml
# GRAFANA LOKI (lightweight alternative to ELK for K8s logs):
# No indexing of log content — only indexes labels (much cheaper than Elasticsearch)

# Promtail (log shipper, like Filebeat for Loki):
# values.yaml for promtail helm chart:
config:
  clients:
    - url: http://loki:3100/loki/api/v1/push
  snippets:
    pipelineStages:
      - cri: {}             # parse CRI log format (Kubernetes)
      - json:               # parse the JSON log body
          expressions:
            level:     level
            traceId:   traceId
            requestId: requestId
      - labels:             # these become Loki labels (indexed)
          level:
          traceId:
      - output:             # set the log line
          source: message

# LogQL queries in Grafana:
# All errors from API service:
# {namespace="production",app="api"} |= `"level":"error"`
# or: {namespace="production",app="api"} | json | level="error"

# Request rate by status:
# sum by (status) (rate({app="api"} | json | unwrap status [5m]))

# P99 response time from logs:
# quantile_over_time(0.99, {app="api"} | json | unwrap responseTime [5m]) by (path)

# Error messages with traceId (click traceId → Tempo trace):
# {app="api"} | json | level="error" | line_format "{{.msg}} traceId={{.traceId}}"
```

---

**Q70. SLOs, error budgets, and multi-window burn rate alerting.**

```javascript
// SLO FRAMEWORK:

// SLI (Service Level Indicator): the metric you're measuring
// SLO (Service Level Objective): your reliability target
// Error Budget: (1 - SLO) = how much unreliability you're allowed

// EXAMPLE SLOs:
// - Availability: 99.9% of requests succeed (allows 43.2 min/month downtime)
// - Latency: 95% of requests < 200ms, 99% < 1s
// - Freshness: data updated within 30 minutes 99.5% of the time

// ERROR BUDGET MATH:
// SLO: 99.9% availability
// Error budget: 0.1% = 43.8 min/month = 10.1 min/week = 86.4 sec/day

// BURN RATE: how fast you're consuming the error budget
// Burn rate 1 = consuming at exactly the allowed rate (budget lasts full window)
// Burn rate 14.4 = consuming 14.4x the allowed rate (hourly budget gone in ~4 min)

// MULTI-WINDOW, MULTI-BURN-RATE ALERTING (Google SRE recommendation):
// Combination of: short window (detect fast) + long window (avoid false alerts)
```
```yaml
# Prometheus alerting rules — multi-window burn rate:
groups:
  - name: slo-error-budget
    rules:
      # Fast burn (will exhaust budget in ~1 hour):
      - alert: ErrorBudgetBurnFast
        expr: |
          (
            job:slo_errors:ratio5m{service="api"} > (14.4 * 0.001)
            and
            job:slo_errors:ratio1h{service="api"} > (14.4 * 0.001)
          )
        labels:
          severity: critical
          page: "true"                  # wake up on-call
        annotations:
          summary: "Fast error budget burn for api"
          description: |
            Current 5m error rate: {{ $value | humanizePercentage }}
            At this rate, monthly error budget will be exhausted in
            {{ div 1 (div $value 0.001) | humanizeDuration }}

      # Medium burn (will exhaust in ~6 hours):
      - alert: ErrorBudgetBurnMedium
        expr: |
          (
            job:slo_errors:ratio30m{service="api"} > (6 * 0.001)
            and
            job:slo_errors:ratio6h{service="api"} > (6 * 0.001)
          )
        labels:
          severity: warning
          page: "false"                 # Slack notification only
        annotations:
          summary: "Elevated error budget burn for api"

      # Slow burn (will exhaust in ~3 days):
      - alert: ErrorBudgetBurnSlow
        expr: |
          job:slo_errors:ratio6h{service="api"} > (3 * 0.001)
          and
          job:slo_errors:ratio3d{service="api"} > (3 * 0.001)
        labels:
          severity: info
        annotations:
          summary: "Slow error budget burn — investigation needed"

    # Recording rules for efficiency (pre-compute expensive queries):
    - record: job:slo_errors:ratio5m
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
        /
        sum(rate(http_requests_total[5m])) by (service)
    - record: job:slo_errors:ratio1h
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[1h])) by (service)
        /
        sum(rate(http_requests_total[1h])) by (service)
    - record: job:slo_errors:ratio30m
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[30m])) by (service)
        /
        sum(rate(http_requests_total[30m])) by (service)
    - record: job:slo_errors:ratio6h
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[6h])) by (service)
        /
        sum(rate(http_requests_total[6h])) by (service)
    - record: job:slo_errors:ratio3d
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[3d])) by (service)
        /
        sum(rate(http_requests_total[3d])) by (service)
```

---

**Q71. Chaos engineering — principles and practice.**

```javascript
// CHAOS ENGINEERING: intentionally inject failures to find weaknesses before production does

// PRINCIPLES (Chaos Monkey / Netflix model):
// 1. Define "steady state" (baseline metrics: error rate, latency, throughput)
// 2. Hypothesize: "system will remain in steady state during this failure"
// 3. Introduce failure (varied: smallest blast radius first)
// 4. Observe (does steady state break? by how much? alarms trigger?)
// 5. Fix weaknesses found
// 6. Automate (run in CI/staging regularly)

// TYPES OF CHAOS EXPERIMENTS:
// Network: latency injection (add 500ms delay), packet loss, network partition
// Resource: CPU stress, memory exhaustion, disk I/O saturation
// Infrastructure: terminate instances/pods, kill containers
// Application: inject HTTP errors (500s), slow down responses
// State: corrupt cache entries, inject DB failures

// TOOLS:
// Chaos Monkey (Netflix): random EC2 termination
// Gremlin: SaaS chaos platform (network, CPU, memory, disk, state)
// Chaos Mesh: Kubernetes-native chaos tool (CNCF)
// LitmusChaos: Kubernetes chaos (CNCF)
// k6 + chaos: load test + chaos simultaneously
```
```yaml
# CHAOS MESH — Kubernetes chaos experiments:

# 1. Kill a random pod (like Chaos Monkey):
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: api-pod-kill
  namespace: chaos-testing
spec:
  action: pod-kill
  mode: one              # kill one random pod
  selector:
    namespaces: [production]
    labelSelectors:
      app: api
  scheduler:
    cron: "@every 1h"    # run every hour (continuous chaos!)

---
# 2. Network latency injection (add 200ms delay to 50% of traffic):
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: api-network-delay
spec:
  action: delay
  mode: all
  selector:
    namespaces: [production]
    labelSelectors: { app: api }
  delay:
    latency: 200ms
    correlation: "25"
    jitter: 50ms
  duration: 10m

---
# 3. Memory stress (simulate memory pressure):
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: api-memory-stress
spec:
  mode: one
  selector:
    namespaces: [production]
    labelSelectors: { app: api }
  stressors:
    memory:
      workers: 2
      size: 256MiB    # consume 256MB per worker
  duration: 5m
```

```
GAME DAYS:
  Planned chaos exercises with the full team.
  Schedule: quarterly or after major system changes.
  Process:
  1. Define experiment and expected outcome
  2. Announce to team (it's a learning exercise, not blame)
  3. Establish rollback plan
  4. Execute experiment
  5. Observe: did monitoring detect it? Did on-call respond correctly?
  6. Fix gaps in observability, alerting, or runbooks
  7. Document in postmortem

WHAT CHAOS ENGINEERING IS NOT:
  NOT: random destruction for fun
  NOT: testing in production without safeguards
  IS:  scientific method applied to infrastructure resilience
  IS:  building confidence in system behavior under failure conditions
```


---

## SECTION 8: SECURITY & SUPPLY CHAIN

---

**Q72. Software supply chain security — SLSA, Sigstore, cosign, SBOM.**

```
SOFTWARE SUPPLY CHAIN ATTACKS:
  Attacker compromises a dependency/build tool/registry → your legitimate software
  ships malicious code without you knowing.

  High-profile attacks:
  - SolarWinds (2020): build pipeline backdoor → 18,000+ organizations affected
  - Log4Shell (2021): vulnerability in ubiquitous logging library
  - XZ Utils (2024): maintainer social engineering, backdoor in compression library
  - npm package hijacking: malicious typosquats (lodash vs 1odash)

SLSA (Supply chain Levels for Software Artifacts):
  Framework from Google to rate supply chain security maturity.

  Level 1 (basic):  builds are scripted, provenance exists
  Level 2 (managed): builds use hosted CI, signed provenance
  Level 3 (hardened): hardened CI, non-falsifiable provenance
  Level 4 (maximum): two-party review, hermetic builds

  SLSA Provenance: cryptographically signed statement of:
    "This artifact was built from this source code on this build system
     using these build steps at this time by this builder identity"
```
```yaml
# GitHub Actions: generate SLSA provenance automatically:
- uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/org/myapp:latest
    provenance: true    # generates and attaches SLSA provenance to image

# View provenance:
# cosign verify-attestation --type slsaprovenance ghcr.io/org/myapp:latest
```

```bash
# SIGSTORE / COSIGN — image signing and verification:
# Sigstore: open standard for signing software artifacts
# cosign: CLI tool implementing Sigstore for container images

# KEYLESS signing (uses OIDC identity — GitHub Actions, Google, etc.):
# In GitHub Actions:
- uses: sigstore/cosign-installer@v3
- run: |
    cosign sign --yes \
      --rekor-url https://rekor.sigstore.dev \
      ghcr.io/org/myapp@${IMAGE_DIGEST}
    # Creates a transparency log entry — permanently auditable
    # Certificate contains: github.com/org/repo, workflow name, SHA
    # No key management needed!

# Verify image (anyone can verify):
cosign verify \
  --certificate-identity-regexp "https://github.com/myorg/myrepo" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  ghcr.io/org/myapp:latest

# KEY-BASED signing (for private infrastructure):
cosign generate-key-pair        # generates cosign.key + cosign.pub
cosign sign --key cosign.key ghcr.io/org/myapp:latest
cosign verify --key cosign.pub ghcr.io/org/myapp:latest

# Enforce signature verification in Kubernetes:
# Kyverno policy — reject unsigned images:
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: enforce
  rules:
    - name: verify-cosign-signature
      match:
        any:
          - resources:
              kinds: ["Pod"]
      verifyImages:
        - imageReferences: ["ghcr.io/myorg/*"]
          attestors:
            - count: 1
              entries:
                - keyless:
                    subject: "https://github.com/myorg/myrepo/.github/workflows/*"
                    issuer: "https://token.actions.githubusercontent.com"

# SBOM (Software Bill of Materials):
# List of ALL components in your software (open-source dependencies, versions, licenses)

# Generate SBOM with Syft:
syft ghcr.io/org/myapp:latest -o spdx-json=sbom.spdx.json
syft ghcr.io/org/myapp:latest -o cyclonedx-json=sbom.cyclonedx.json

# Attach SBOM to image:
cosign attach sbom --sbom sbom.spdx.json ghcr.io/org/myapp:latest

# Scan SBOM for vulnerabilities with Grype:
grype sbom:sbom.spdx.json --fail-on high

# SBOM in GitHub Actions:
- uses: docker/build-push-action@v5
  with:
    sbom: true          # auto-generates and attaches SBOM
    provenance: true    # attach SLSA provenance
```

---

**Q73. Vault — dynamic secrets and zero-trust secret management.**

```javascript
// VAULT ARCHITECTURE:
// - Secrets engine: plugins that handle different secret types
//   (KV, database, AWS, PKI, SSH, Transit, TOTP, etc.)
// - Auth method: how clients authenticate (Kubernetes, OIDC, AWS, LDAP)
// - Policy: what a client can access after authentication
// - Lease: time-limited access with renewal option

// VAULT KUBERNETES AUTH FLOW:
// 1. Pod has K8s service account token at /var/run/secrets/kubernetes.io/serviceaccount/token
// 2. Pod presents token to Vault
// 3. Vault verifies with K8s API (is this a real service account? does it exist?)
// 4. Vault checks role binding: "api-production SA → api-policy"
// 5. Vault returns Vault token with api-policy permissions
// 6. Pod uses Vault token to request secrets

// DYNAMIC DATABASE CREDENTIALS (no more static passwords):
import Vault from "node-vault";

class SecretManager {
  private vault: Vault.client;
  private dbCreds: { username: string; password: string; expiry: Date } | null = null;

  constructor() {
    this.vault = Vault({
      apiVersion: "v1",
      endpoint: process.env.VAULT_ADDR ?? "https://vault.internal:8200",
    });
  }

  async authenticate(): Promise<void> {
    const token = fs.readFileSync(
      "/var/run/secrets/kubernetes.io/serviceaccount/token",
      "utf8"
    );

    const result = await this.vault.kubernetesLogin({
      mount_point: "kubernetes",
      role: `${process.env.SERVICE_NAME}-${process.env.NODE_ENV}`,
      jwt: token,
    });

    this.vault.token = result.auth.client_token;
  }

  async getDatabaseCredentials(): Promise<{ username: string; password: string }> {
    // Renew if within 5 minutes of expiry:
    if (this.dbCreds && this.dbCreds.expiry.getTime() - Date.now() > 5 * 60 * 1000) {
      return this.dbCreds;
    }

    const { data } = await this.vault.read(
      `database/creds/api-${process.env.NODE_ENV}`
    );

    this.dbCreds = {
      username: data.username,     // "v-k8s-api-prod-xyz123-1705316400"
      password: data.password,     // auto-generated, expires in 1 hour
      expiry: new Date(Date.now() + data.lease_duration * 1000),
    };

    return this.dbCreds;
  }

  async encryptData(plaintext: string): Promise<string> {
    const { data } = await this.vault.write("transit/encrypt/app-key", {
      plaintext: Buffer.from(plaintext).toString("base64"),
    });
    return data.ciphertext;    // "vault:v1:abc123..."
  }

  async decryptData(ciphertext: string): Promise<string> {
    const { data } = await this.vault.write("transit/decrypt/app-key", {
      ciphertext,
    });
    return Buffer.from(data.plaintext, "base64").toString();
  }
}

// VAULT AGENT SIDECAR (no code changes needed!):
// Vault Agent runs alongside your app:
// - Authenticates to Vault automatically
// - Writes secrets to a tmpfs volume
// - App reads from files (environment-agnostic)
// - Agent auto-renews before expiry

// vault-agent-config.hcl:
// auto_auth {
//   method "kubernetes" {
//     mount_path = "auth/kubernetes"
//     config { role = "api-production" }
//   }
//   sink "file" { config { path = "/vault/token" } }
// }
// template {
//   source      = "/vault/templates/db.tpl"
//   destination = "/vault/secrets/database.env"
// }
// {{- with secret "database/creds/api-production" }}
// DATABASE_URL=postgresql://{{ .Data.username }}:{{ .Data.password }}@db:5432/myapp
// {{- end }}
```

---

**Q74. Istio and mTLS — zero trust networking.**

```yaml
# ZERO TRUST NETWORKING:
# Never trust, always verify. Every service-to-service call is:
# - Authenticated (mutual TLS — both sides prove identity)
# - Authorized (explicit policy allows this call)
# - Encrypted (TLS in transit)

# ISTIO IMPLEMENTATION:
# Sidecar proxy (Envoy) injected into every pod automatically.
# Handles mTLS without any application code changes.

# STEP 1: Install Istio
# istioctl install --set profile=production
# kubectl label namespace production istio-injection=enabled

# STEP 2: Strict mTLS (all communication must be mutual TLS):
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT   # reject plaintext traffic between pods

---
# STEP 3: Authorization policies (who can talk to whom):
# Allow only frontend → api (not worker → api):
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              # SPIFFE identity: spiffe://cluster.local/ns/production/sa/frontend-sa
              - "cluster.local/ns/production/sa/frontend-sa"
              - "cluster.local/ns/production/sa/admin-sa"
      to:
        - operation:
            methods: ["GET", "POST", "PUT", "DELETE"]
            paths: ["/api/*"]
      when:
        - key: source.ip
          notValues: ["10.0.0.0/8"]    # deny if not from internal network

---
# STEP 4: Traffic management (circuit breaking):
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: api-circuit-breaker
spec:
  host: api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5     # eject host after 5 consecutive errors
      interval: 30s               # check interval
      baseEjectionTime: 30s       # eject for minimum 30s
      maxEjectionPercent: 50      # never eject more than 50% of hosts
      minHealthPercent: 30        # stop ejection if < 30% healthy

---
# STEP 5: Observability — Istio provides automatic metrics, traces, logs:
# Metrics:
#   istio_requests_total{destination_service="api", response_code="200"} 
#   istio_request_duration_milliseconds_bucket{destination_service="api"}
# All without any instrumentation code!

# SPIFFE (Secure Production Identity Framework for Everyone):
# Istio assigns cryptographic identity to each workload:
# spiffe://cluster.local/ns/production/sa/api-sa
# Identity certificate: auto-rotated every 24h by Istio CA (Citadel)
# Encoded in X.509 SAN extension of the mTLS certificate
```

---

**Q75. Container runtime security — Falco and runtime threat detection.**

```yaml
# FALCO: open-source runtime security monitoring for containers and K8s
# Detects: unexpected system calls, privilege escalation, network anomalies,
#          data exfiltration, container escapes, crypto mining

# HOW FALCO WORKS:
# Deployed as DaemonSet → runs on every node
# Uses eBPF (modern) or kernel module to intercept syscalls
# Compares syscalls against rules → alerts on violations

# FALCO RULES (custom + community rules from falco-rules):

# Detect shell spawned in a container (should never happen in production):
- rule: Shell Spawned in Container
  desc: >
    A shell was spawned in a container. This may indicate an attacker
    got shell access or a legitimate admin action.
  condition: >
    container and
    proc.name in (shell_binaries) and
    spawned_process and
    container.name not in (allowed_containers) and
    not container.image startswith "pairing/ci"
  output: >
    Shell spawned in a container
    (user=%user.name container=%container.name image=%container.image.repository
     shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
  priority: WARNING
  tags: [container, shell, mitre_execution]

# Detect privilege escalation:
- rule: Privilege Escalation via chmod
  condition: >
    spawned_process and
    proc.name = chmod and
    (proc.args contains "777" or proc.args contains "u+s") and
    container
  output: >
    chmod called with suspicious args (user=%user.name container=%container.name
     cmdline=%proc.cmdline)
  priority: ERROR

# Detect crypto mining (typical first activity after container compromise):
- rule: Crypto Mining Detected
  condition: >
    (proc.name in (crypto_miners)) or
    (proc.cmdline contains "--stratum" or proc.cmdline contains "xmrig") or
    outbound and
    fd.sport in (3333, 4444, 5555, 7777, 8888, 9999, 14444, 45700)
  output: Crypto mining activity detected (container=%container.name user=%user.name)
  priority: CRITICAL
  tags: [cryptomining, mitre_impact]

# Detect data exfiltration (large outbound data to external IP):
- rule: Sensitive Data Exfiltration Attempt
  condition: >
    outbound and
    fd.typechar = 4 and                    # TCP
    fd.rip != "10.0.0.0/8" and            # not internal
    fd.rip != "172.16.0.0/12" and
    evt.rawres > 10485760                  # > 10MB in single write
  output: Large data transfer to external IP (container=%container.name ip=%fd.rip bytes=%evt.rawres)
  priority: WARNING

# Falco Sidekick — forward alerts to Slack, PagerDuty, OpsGenie, Webhook:
# falcosidekick config:
customfields:
  environment: production
  cluster: eks-us-east-1
slack:
  webhookurl: https://hooks.slack.com/services/xxx/yyy/zzz
  minimumpriority: warning
  messageformat: >
    *{{.rule}}*
    Container: `{{index .outputfields "container.name"}}`
    Image: `{{index .outputfields "container.image.repository"}}`
    ```{{.output}}```
pagerduty:
  routingkey: your-pagerduty-integration-key
  minimumpriority: critical
```

---

**Q76. On-call, incidents, and postmortems.**

```
INCIDENT SEVERITY LEVELS:
  P1 (Critical): complete outage or data loss. On-call paged immediately.
                 Revenue impact. All hands.
                 Response time: 15 minutes to acknowledge, 1h to mitigate.
                 Example: payment service down, all users logged out.

  P2 (High):     major feature broken, significant user impact.
                 On-call paged during business hours immediately, off-hours: 30min.
                 Response time: 30 minutes to acknowledge, 4h to mitigate.
                 Example: search feature returning errors for 20% of users.

  P3 (Medium):   minor feature degraded, small % affected.
                 Slack notification, next business day.
                 Example: email notifications delayed 10 minutes.

  P4 (Low):      cosmetic issues, no user impact.
                 Backlog ticket.

INCIDENT LIFECYCLE:
  1. Detection: alert fires (automated) or user reports (manual)
  2. Acknowledgment: on-call claims the incident
  3. Triage: how bad is it? how many users affected? revenue impact?
  4. Communication: incident channel created, status page updated
  5. Investigation: what changed? (recent deploys, config changes, traffic spikes)
  6. Mitigation: restore service (rollback, traffic shift, scale up)
  7. Resolution: root cause fixed, monitoring normal
  8. Postmortem: 48-72h after incident

INCIDENT COMMUNICATION TEMPLATE:
  [P1 INCIDENT] Payment service degraded
  Status: Investigating
  Impact: ~30% of checkout attempts failing with 500 errors
  Started: 2024-01-15 14:23 UTC
  Engineer: @on-call-engineer
  Bridge: https://zoom.us/j/123456789
  Updates every 30 minutes

POSTMORTEM (blameless culture):
  Goal: learn, not punish. Systems fail, not people.

  Structure:
  Summary:        What happened and what was the impact?
  Timeline:       Chronological sequence of events (UTC timestamps)
  Root cause:     The actual technical cause (5 Whys analysis)
  Contributing factors: What made this worse or made detection harder?
  Impact:         Duration, users affected, revenue impact
  What went well: What helped us detect/respond faster?
  What went wrong: What slowed us down or made it worse?
  Action items:   Specific, assignable, deadline-bound improvements

  5 WHYS EXAMPLE:
  Why did users get 500 errors?
    → Database connections exhausted.
  Why were connections exhausted?
    → New deploy increased query count per request by 10x.
  Why did the query count increase?
    → N+1 query bug in new feature code.
  Why wasn't this caught in staging?
    → Staging has 1/100th the data volume (N+1 not visible with small data).
  Why does staging have so little data?
    → We never set up realistic data seeding.
  Root cause: No production-representative data in staging.
  Fix: Implement data seeding with 10% production data anonymization.
```

---

**Q77. Production readiness checklist.**

```
DEPLOYMENT & RELIABILITY:
  ☐ Health checks: /health/live (liveness) and /health/ready (readiness) endpoints
  ☐ Graceful shutdown: handle SIGTERM, drain in-flight requests, close DB connections
  ☐ Resource limits: CPU requests/limits and memory requests/limits set
  ☐ Replicas: minimum 2 (never 1 — no single point of failure)
  ☐ PodDisruptionBudget: at least 1 pod always available
  ☐ TopologySpreadConstraints: pods spread across AZs
  ☐ Rolling update strategy: maxUnavailable: 0 for zero-downtime
  ☐ Rollback plan: tested rollback procedure documented
  ☐ Feature flags: new features behind flags for safe rollout

OBSERVABILITY:
  ☐ Structured JSON logging with correlation IDs (requestId, traceId)
  ☐ Prometheus metrics exported at /metrics
  ☐ Distributed tracing instrumented (OpenTelemetry)
  ☐ Alerting rules: error rate, latency P99, memory, CPU, disk
  ☐ Dashboards: RED metrics (Rate, Errors, Duration) per service
  ☐ On-call runbook linked from alerts
  ☐ SLO defined and tracked

SECURITY:
  ☐ Non-root user in container
  ☐ Read-only root filesystem
  ☐ No privileged containers
  ☐ Resource limits (CPU, memory, PIDs)
  ☐ NetworkPolicy: deny-by-default, allow only needed communication
  ☐ Secrets from Vault or External Secrets (not hardcoded or in ConfigMap)
  ☐ Image signed with cosign
  ☐ Image scanned for CVEs in CI/CD
  ☐ RBAC: service account with minimal permissions
  ☐ Admission policies enforce security standards (Kyverno/OPA)

PERFORMANCE:
  ☐ Load tested: can handle 2x expected peak traffic
  ☐ HPA configured: auto-scales on CPU/memory/custom metrics
  ☐ Database connection pooling configured
  ☐ Caching strategy defined (where appropriate)
  ☐ Database indexes validated (no slow queries in load test)

OPERATIONS:
  ☐ Runbook created: how to debug, restart, scale, rollback
  ☐ Alert routing: who is paged for what?
  ☐ Change management: all changes tracked in git
  ☐ Deployment approved: code review + staging validation
  ☐ Disaster recovery tested: can restore from backup?
  ☐ Secrets rotation: credentials can be rotated without downtime
```


---

## SECTION 9: KUBERNETES NETWORKING & STORAGE

---

**Q78. Kubernetes networking — CNI, Cilium, Calico.**

```
KUBERNETES NETWORKING REQUIREMENTS (from the spec):
  1. Every pod gets its own IP address
  2. Pods on the same node can communicate without NAT
  3. Pods on different nodes can communicate without NAT
  4. Agents on a node can communicate with all pods on that node

CNI (Container Network Interface):
  Standard plugin interface for Kubernetes networking.
  Kubernetes calls CNI plugin to: set up pod network interface, assign IP, configure routing.

POPULAR CNI PLUGINS:

FLANNEL (simplest):
  - VXLAN overlay: wraps pod traffic in UDP packets, routes between nodes
  - Simple, limited features (no NetworkPolicy enforcement)
  - Good for: development, learning, small clusters

CALICO (most common in production):
  - BGP routing (no overlay for same-network nodes) = better performance
  - Full NetworkPolicy support (plus its own CRDs for richer policies)
  - Supports: Linux kernel, eBPF dataplane (optional)
  - GlobalNetworkPolicy: enforce policies across all namespaces
  - Works well with: AWS, GCP, bare metal

CILIUM (modern eBPF-based):
  - eBPF: injects code directly into Linux kernel → near-native performance
  - No iptables rules (eBPF replaces kube-proxy too)
  - L7 network policies: can filter based on HTTP method, URL, gRPC method
  - Built-in observability: Hubble provides flow visibility
  - Cilium Service Mesh: replaces Istio for many use cases
  - Tetragon: eBPF-based runtime security (part of Cilium ecosystem)
  - Used by: Google, Adobe, Capital One, Datadog

COMPARISON:
  Feature               Flannel   Calico   Cilium
  NetworkPolicy         No        Yes      Yes
  L7 policy             No        No       Yes (eBPF)
  Performance           Good      Better   Best (eBPF)
  Observability         Limited   Limited  Excellent (Hubble)
  Service Mesh          No        No       Yes (optional)
  Complexity            Low       Medium   Higher
```
```yaml
# CILIUM — install and use:
# helm install cilium cilium/cilium --namespace kube-system \
#   --set kubeProxyReplacement=true \   # replace kube-proxy with eBPF
#   --set hubble.enabled=true \         # flow observability
#   --set hubble.relay.enabled=true \
#   --set hubble.ui.enabled=true

# Cilium L7 NetworkPolicy (HTTP-aware):
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-l7-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "3000"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: /api/products.*
              - method: POST
                path: /api/orders
                # Reject /api/admin from frontend entirely
  egress:
    - toEndpoints:
        - matchLabels:
            app: postgres
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP

# Hubble CLI — observe network flows:
# hubble observe --namespace production
# hubble observe --pod api-xyz --protocol http
# hubble observe --verdict DROPPED   # see what's being blocked
```

---

**Q79. Kubernetes StatefulSets — databases in Kubernetes.**

```yaml
# StatefulSet: ordered, stable pods for stateful applications
# Key properties vs Deployment:
# 1. Stable pod names: redis-0, redis-1, redis-2 (not random hashes)
# 2. Stable network identity: redis-0.redis-headless.default.svc.cluster.local
# 3. Ordered creation: redis-0 fully ready before redis-1 starts
# 4. Ordered deletion: reverse order (redis-2 → redis-1 → redis-0)
# 5. Stable storage: each pod gets its own PVC (redis-0 always gets data-redis-0)

# Redis Cluster StatefulSet:
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: production
spec:
  serviceName: redis-headless    # headless service for stable DNS
  replicas: 6                    # 3 primary + 3 replica
  podManagementPolicy: Parallel  # start all at once (override default ordered)
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0               # update all pods (set to N to do canary)
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      terminationGracePeriodSeconds: 60  # time to finish pending ops
      initContainers:
        - name: config
          image: redis:7-alpine
          command: ["sh", "-c"]
          args:
            - |
              # Determine if this is a primary or replica based on pod index
              POD_INDEX=${HOSTNAME##*-}
              if [ "$POD_INDEX" -lt 3 ]; then
                echo "cluster-enabled yes" > /conf/redis.conf
              else
                echo "cluster-enabled yes" > /conf/redis.conf
                echo "slaveof redis-$((POD_INDEX - 3)).redis-headless 6379" >> /conf/redis.conf
              fi
          volumeMounts:
            - name: conf
              mountPath: /conf
      containers:
        - name: redis
          image: redis:7-alpine
          command: ["redis-server", "/conf/redis.conf"]
          ports:
            - containerPort: 6379
              name: redis
          resources:
            requests: { memory: 512Mi, cpu: 100m }
            limits:   { memory: 1Gi,  cpu: 500m }
          livenessProbe:
            exec:
              command: ["redis-cli", "ping"]
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command: ["redis-cli", "ping"]
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: data
              mountPath: /data
            - name: conf
              mountPath: /conf
      volumes:
        - name: conf
          emptyDir: {}

  # Each pod gets its own PVC — stable across restarts and rescheduling:
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 10Gi

---
# Headless service — DNS returns individual pod IPs:
apiVersion: v1
kind: Service
metadata:
  name: redis-headless
  namespace: production
spec:
  clusterIP: None       # headless
  selector:
    app: redis
  ports:
    - port: 6379
      name: redis
# DNS records created:
# redis-0.redis-headless.production.svc.cluster.local → pod-0 IP
# redis-1.redis-headless.production.svc.cluster.local → pod-1 IP
# etc.

---
# Regular service for client connections:
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: redis
  ports:
    - port: 6379
```

---

**Q80. Kubernetes storage — StorageClasses, PVs, PVCs, CSI.**

```yaml
# STORAGE HIERARCHY:
# StorageClass: how to provision storage (provisioner + parameters)
# PersistentVolume (PV): actual storage resource (created by admin or dynamically)
# PersistentVolumeClaim (PVC): user request for storage
# Pod: mounts PVC as a volume

# CSI (Container Storage Interface): standard for volume plugins
# Every cloud provider has a CSI driver:
# AWS: aws-ebs-csi-driver (EBS), aws-efs-csi-driver (EFS)
# GCP: gce-pd-csi-driver
# Azure: azuredisk-csi-driver

# StorageClasses for AWS:
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3                  # gp3: better baseline performance than gp2
  iops: "3000"               # baseline IOPS (free with gp3)
  throughput: "125"          # MB/s
  encrypted: "true"
  kmsKeyId: arn:aws:kms:us-east-1:123456:key/abc123
reclaimPolicy: Retain        # keep EBS volume after PVC delete (safe for databases)
allowVolumeExpansion: true   # allow resizing
volumeBindingMode: WaitForFirstConsumer  # provision in same AZ as pod

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
reclaimPolicy: Delete        # delete EBS when PVC deleted (safe for non-critical data)
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
# PVC — request storage dynamically provisioned:
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-data
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce          # only one node can mount (block storage)
    # ReadWriteMany: multiple nodes (NFS, EFS only)
    # ReadOnlyMany: multiple nodes, read-only
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
  # Resize: edit request to 200Gi + edit EBS volume → k8s expands filesystem

---
# VolumeSnapshot — point-in-time backup:
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: postgres-snapshot-20240115
  namespace: production
spec:
  volumeSnapshotClassName: csi-aws-vsc
  source:
    persistentVolumeClaimName: postgres-data
# Creates EBS snapshot → restore by creating PVC from snapshot

# Restore from snapshot:
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-restored
spec:
  storageClassName: fast-ssd
  dataSource:
    name: postgres-snapshot-20240115
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes: [ReadWriteOnce]
  resources:
    requests: { storage: 100Gi }
```

---

**Q81. cert-manager — automatic TLS certificate management.**

```yaml
# cert-manager: automates TLS certificate lifecycle (issuance, renewal)
# Supports: Let's Encrypt (ACME), Vault PKI, self-signed, AWS ACM (via external issuer)

# Install:
# helm install cert-manager jetstack/cert-manager \
#   --namespace cert-manager --create-namespace \
#   --set installCRDs=true \
#   --set prometheus.enabled=true

# ClusterIssuer — Let's Encrypt production:
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: devops@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      # DNS-01 challenge (works for wildcard certs):
      - dns01:
          route53:
            region: us-east-1
            hostedZoneID: Z1234567890ABC
        selector:
          dnsZones: ["example.com"]
      # HTTP-01 challenge (simpler, no DNS access needed):
      - http01:
          ingress:
            class: nginx
        selector:
          dnsNames: ["api.example.com"]

---
# ClusterIssuer — Let's Encrypt staging (for testing, no rate limits):
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: devops@example.com
    privateKeySecretRef:
      name: letsencrypt-staging-key
    solvers:
      - http01:
          ingress:
            class: nginx

---
# Certificate — explicit certificate request:
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls
  namespace: production
spec:
  secretName: api-tls-secret    # created/updated automatically
  duration: 2160h               # 90 days (Let's Encrypt default)
  renewBefore: 360h             # renew 15 days before expiry
  isCA: false
  privateKey:
    algorithm: ECDSA
    size: 256
  dnsNames:
    - api.example.com
    - "*.api.example.com"       # wildcard (requires DNS-01)
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer

# OR: let cert-manager issue automatically via Ingress annotation:
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod  # ← cert-manager issues cert
spec:
  tls:
    - hosts: [api.example.com]
      secretName: api-tls     # cert-manager creates this Secret
  rules: [...]

# Check certificate status:
# kubectl get certificate -n production
# kubectl describe certificate api-tls -n production
# kubectl get certificaterequest -n production

# Vault PKI Issuer (internal CA for service-to-service mTLS):
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-issuer
spec:
  vault:
    server: https://vault.internal:8200
    path: pki/sign/api-production    # Vault PKI role
    auth:
      kubernetes:
        mountPath: /v1/auth/kubernetes
        role: cert-manager
        secretRef:
          name: cert-manager-vault-token
          key: token
```

---

**Q82. Ansible — configuration management for DevOps.**

```yaml
# ANSIBLE: agentless configuration management and automation
# Uses SSH to connect to hosts, no agent installation required
# Written in YAML (playbooks), idempotent by design

# INVENTORY (hosts.ini):
[web]
web1.example.com
web2.example.com

[db]
db1.example.com ansible_user=ubuntu ansible_become=yes

[production:children]
web
db

[all:vars]
ansible_python_interpreter=/usr/bin/python3

# PLAYBOOK (deploy-api.yml):
---
- name: Deploy API Service
  hosts: web
  become: yes          # sudo
  vars:
    app_version: "{{ lookup('env', 'APP_VERSION') }}"
    app_dir: /opt/api
    app_user: apiuser

  pre_tasks:
    - name: Ensure Python 3 is installed
      raw: apt-get install -y python3
      changed_when: false

  tasks:
    - name: Create app user
      user:
        name: "{{ app_user }}"
        system: yes
        shell: /bin/false
        createhome: no
        state: present

    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
        mode: "0750"

    - name: Install Node.js 20
      block:
        - name: Add NodeSource repository
          shell: curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
          args:
            creates: /etc/apt/sources.list.d/nodesource.list

        - name: Install nodejs
          apt:
            name: nodejs
            state: present
            update_cache: yes

    - name: Copy application files
      synchronize:
        src: "{{ playbook_dir }}/../dist/"
        dest: "{{ app_dir }}/dist/"
        delete: yes
        rsync_opts: ["--exclude=node_modules"]
      notify: Restart API service

    - name: Install production dependencies
      npm:
        path: "{{ app_dir }}"
        production: yes
        state: present

    - name: Configure environment
      template:
        src: templates/api.env.j2
        dest: "{{ app_dir }}/.env"
        owner: "{{ app_user }}"
        mode: "0600"
      notify: Restart API service

    - name: Install systemd service
      template:
        src: templates/api.service.j2
        dest: /etc/systemd/system/api.service
      notify:
        - Reload systemd
        - Restart API service

    - name: Enable and start API service
      systemd:
        name: api
        enabled: yes
        state: started
        daemon_reload: yes

    - name: Wait for API to be healthy
      uri:
        url: http://localhost:3000/health
        status_code: 200
      register: health
      until: health.status == 200
      retries: 12
      delay: 5

  handlers:
    - name: Reload systemd
      systemd:
        daemon_reload: yes

    - name: Restart API service
      systemd:
        name: api
        state: restarted

# RUN:
ansible-playbook deploy-api.yml -i hosts.ini \
  -e "APP_VERSION=2.1.0" \
  --limit web1.example.com   # deploy to one host first (canary)

# ANSIBLE VAULT — encrypt secrets:
ansible-vault encrypt vars/secrets.yml
ansible-vault view vars/secrets.yml
ansible-playbook deploy.yml --ask-vault-pass
ansible-playbook deploy.yml --vault-password-file ~/.vault_pass

# ROLES — reusable, shareable units:
roles/
  nodejs/
    tasks/main.yml
    handlers/main.yml
    defaults/main.yml    # role defaults (lowest priority vars)
    vars/main.yml        # role vars (higher priority)
    templates/
    files/

# Use role in playbook:
- hosts: web
  roles:
    - { role: nodejs, node_version: "20" }
    - { role: nginx, nginx_port: 80 }
    - { role: api, app_version: "{{ lookup('env', 'APP_VERSION') }}" }
```

---

**Q83. AWS networking — VPC, Transit Gateway, PrivateLink.**

```
VPC (Virtual Private Cloud):
  Your isolated network in AWS. You choose: CIDR, subnets, routing, security.

  COMPONENTS:
  - CIDR block: IP range (e.g., 10.0.0.0/16 = 65,536 IPs)
  - Subnets: divisions of VPC CIDR per AZ
    - Public subnet: has route to Internet Gateway
    - Private subnet: route to NAT Gateway for outbound only
    - Isolated subnet: no internet access (databases)
  - Route table: routing rules per subnet
  - Internet Gateway (IGW): allows inbound+outbound internet for public subnets
  - NAT Gateway: allows OUTBOUND internet for private subnets (one per AZ for HA)
  - Security Groups: stateful firewall per ENI (elastic network interface)
  - Network ACLs: stateless firewall per subnet

  DESIGN PATTERN (3-tier):
    Public:   10.0.0.0/24, 10.0.1.0/24, 10.0.2.0/24   (load balancers)
    Private:  10.0.10.0/24, 10.0.11.0/24, 10.0.12.0/24  (application servers)
    Isolated: 10.0.20.0/24, 10.0.21.0/24, 10.0.22.0/24  (databases)

VPC PEERING:
  Direct private connectivity between two VPCs (same or different accounts/regions).
  Not transitive: if A↔B and B↔C, A cannot reach C via B.
  Route tables must be updated on both sides.
  Use case: small number of VPCs, simple connectivity.

TRANSIT GATEWAY (TGW):
  Hub-and-spoke: connects many VPCs + on-premise networks through a single gateway.
  Transitive routing: A→TGW→B, A→TGW→C, B→TGW→C all work.
  Centralized: one attachment per VPC, routing managed in TGW route tables.
  Supports: Inter-region peering, VPN, Direct Connect Gateway.
  Cost: per attachment + per GB processed.
  Use case: many VPCs, complex connectivity, multi-account organizations.

AWS PRIVATELINK:
  Private connectivity to AWS services or partner services WITHOUT internet traversal.
  Uses VPC Endpoints:
  - Interface endpoint: ENI in your subnet → private IP for the service
  - Gateway endpoint: route table entry (S3 and DynamoDB only, free)

  Example: EC2 → S3 without internet:
    Create S3 Gateway endpoint in your VPC → traffic stays on AWS backbone.

  Example: access AWS Secrets Manager privately:
    Interface endpoint for secretsmanager → resolves to private IP in your VPC.

  Example: expose YOUR service to other VPCs (PrivateLink):
    Your service → NLB → VPC Endpoint Service → consumers create Interface Endpoint
    Consumers access your service via private IP (no peering, no IP overlap issues).
```
```bash
# Terraform: multi-VPC architecture with Transit Gateway
resource "aws_ec2_transit_gateway" "main" {
  description = "Production Transit Gateway"
  auto_accept_shared_attachments  = "disable"
  default_route_table_association = "disable"
  default_route_table_propagation = "disable"
  tags = { Name = "prod-tgw" }
}

# Attach VPCs to TGW:
resource "aws_ec2_transit_gateway_vpc_attachment" "app" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.app_vpc.vpc_id
  subnet_ids         = module.app_vpc.private_subnets
}

resource "aws_ec2_transit_gateway_vpc_attachment" "shared" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.shared_vpc.vpc_id
  subnet_ids         = module.shared_vpc.private_subnets
}

# VPC Endpoint for Secrets Manager (private access, no internet):
resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id              = module.app_vpc.vpc_id
  service_name        = "com.amazonaws.us-east-1.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = module.app_vpc.private_subnets
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true   # secretsmanager.us-east-1.amazonaws.com → private IP
}
```

---

**Q84. AWS RDS — Multi-AZ, Read Replicas, Aurora, connection pooling.**

```
RDS DEPLOYMENT OPTIONS:

1. SINGLE INSTANCE:
   One DB server. No HA.
   Failover: manual restore from backup (10min-hours of downtime).
   Use: dev, staging, non-critical workloads.

2. MULTI-AZ:
   Primary instance + synchronous standby in another AZ.
   Standby is NOT readable (only for failover).
   Automatic failover: 1-2 minutes (DNS update, no IP change).
   Handles: AZ failure, instance failure, OS patching.
   Cost: 2x single instance.
   Use: production databases where downtime is unacceptable.

3. READ REPLICAS:
   Asynchronous replication from primary to replicas.
   Replicas ARE readable: offload read traffic from primary.
   Can be promoted to standalone DB (disaster recovery).
   Cross-region replicas: RPO measured in seconds, used for DR.
   Max replicas: 5 for MySQL/PostgreSQL, 15 for Aurora.
   Use: read-heavy workloads, analytics queries, geographic distribution.

4. AURORA:
   AWS-proprietary storage engine, compatible MySQL/PostgreSQL driver.
   Storage: distributed across 6 nodes in 3 AZs (always).
   Compute: separate from storage (Aurora can have 1 writer + up to 15 readers).
   Failover: 30 seconds (vs RDS Multi-AZ 60-120s).
   Aurora Serverless v2: scales in 0.5 ACU increments (0.5-256 ACUs).
     ACU = 2GB RAM + proportional CPU.
     Ideal for: variable/unpredictable workloads, dev/staging, bursty apps.
   Aurora Global Database: primary region + up to 5 read-only secondary regions.
     RPO < 1 second. RTO < 1 minute. Use for DR + low-latency reads globally.

CONNECTION POOLING:
  Problem: PostgreSQL has a per-connection process model.
  Each connection uses ~10MB RAM. 1000 connections = 10GB just for connection overhead.
  Lambda + RDS = connection storm (each Lambda invocation creates new connection).

  SOLUTIONS:
  - PgBouncer: lightweight connection pooler (transaction or session pooling)
  - RDS Proxy: AWS-managed proxy, scales connection pooling, IAM auth, failover handling
```
```javascript
// RDS Proxy in Node.js (transparent — same connection string, just different endpoint):
import { Pool } from "pg";

// Without RDS Proxy: app → RDS (direct, 1 connection per app instance)
// With RDS Proxy:    app → RDS Proxy → RDS (pooled, IAM auth, failover handled)

const pool = new Pool({
  host:     process.env.RDS_PROXY_ENDPOINT,   // xxx.proxy-xxx.us-east-1.rds.amazonaws.com
  database: process.env.DB_NAME,
  user:     process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  port:     5432,
  max:      10,          // connection pool size per app instance
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
  // SSL required for RDS Proxy:
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync("rds-ca-2019-root.pem"),
  },
});

// Read/write splitting (Route writes to primary, reads to replica):
const primaryPool = new Pool({ host: process.env.RDS_WRITER_ENDPOINT, ... });
const replicaPool = new Pool({ host: process.env.RDS_READER_ENDPOINT, ... });

class DatabaseClient {
  query(sql: string, params?: any[]) {
    return primaryPool.query(sql, params);   // default: write-capable primary
  }
  readQuery(sql: string, params?: any[]) {
    return replicaPool.query(sql, params);   // offload to read replica
  }
}
```

---

**Q85. AWS SQS and SNS — messaging patterns.**

```javascript
// SQS (Simple Queue Service) — decoupled message queue
import { SQSClient, SendMessageCommand, ReceiveMessageCommand, DeleteMessageCommand, ChangeMessageVisibilityCommand } from "@aws-sdk/client-sqs";

const sqs = new SQSClient({ region: "us-east-1" });
const QUEUE_URL = process.env.SQS_QUEUE_URL!;

// PRODUCER — send message:
await sqs.send(new SendMessageCommand({
  QueueUrl:     QUEUE_URL,
  MessageBody:  JSON.stringify({ orderId: "ord_123", amount: 99.99 }),
  // FIFO queue only:
  MessageGroupId:         "orders",      // same group = ordered
  MessageDeduplicationId: "ord_123",     // prevent duplicate processing
  // Standard queue — delay delivery:
  DelaySeconds: 30,
  // Add attributes for filtering (SNS subscription filter only):
  MessageAttributes: {
    eventType: { DataType: "String", StringValue: "order.created" },
    priority:  { DataType: "Number", StringValue: "1" },
  },
}));

// CONSUMER — poll and process:
async function processMessages() {
  while (true) {
    const response = await sqs.send(new ReceiveMessageCommand({
      QueueUrl:              QUEUE_URL,
      MaxNumberOfMessages:   10,        // batch up to 10
      WaitTimeSeconds:       20,        // long polling (reduce empty responses)
      VisibilityTimeout:     300,       // 5 minutes to process before becoming visible again
      AttributeNames:        ["All"],
      MessageAttributeNames: ["All"],
    }));

    if (!response.Messages?.length) continue;

    await Promise.allSettled(
      response.Messages.map(async (msg) => {
        try {
          const body = JSON.parse(msg.Body!);
          await processOrder(body);

          // Delete only after SUCCESSFUL processing:
          await sqs.send(new DeleteMessageCommand({
            QueueUrl:      QUEUE_URL,
            ReceiptHandle: msg.ReceiptHandle!,
          }));
        } catch (err) {
          console.error({ err, messageId: msg.MessageId }, "Failed to process message");
          // Don't delete → message becomes visible again after VisibilityTimeout
          // After maxReceiveCount failures → goes to Dead Letter Queue (DLQ)

          // Extend visibility timeout if processing takes longer than expected:
          if (isLongRunning) {
            await sqs.send(new ChangeMessageVisibilityCommand({
              QueueUrl:          QUEUE_URL,
              ReceiptHandle:     msg.ReceiptHandle!,
              VisibilityTimeout: 300,   // extend 5 more minutes
            }));
          }
        }
      })
    );
  }
}

// SQS PATTERNS:
// 1. Dead Letter Queue (DLQ) — capture failed messages:
//    Main queue: maxReceiveCount=3 → after 3 failures, moves to DLQ
//    DLQ: alert on any messages, investigate root cause, replay after fix
//    aws sqs redrive-messages --source-queue-url $DLQ_URL --destination-queue-url $QUEUE_URL

// 2. Lambda trigger (event-driven, auto-scales):
//    SQS → Lambda trigger → batchSize=10, concurrency controlled by reservedConcurrency
//    Lambda auto-deletes messages on success, leaves on failure (partial batch response)

// 3. Fan-out (SNS → multiple SQS):
//    SNS topic → SQS queue A (email processor)
//                SQS queue B (analytics processor)
//                SQS queue C (audit logger)
//    All queues receive EVERY message (fan-out pattern)

// SNS subscription filtering (route by event type):
// Filter policy on SQS subscription:
// { "eventType": ["order.created", "order.updated"] }
// → only messages with matching MessageAttribute delivered to this queue
```

---

**Q86. Kubernetes multi-tenancy and namespace isolation.**

```yaml
# MULTI-TENANCY PATTERNS:
# 1. Namespace per team/environment (soft isolation)
# 2. Cluster per team/environment (hard isolation)
# 3. Virtual clusters (vcluster — K8s inside K8s)

# NAMESPACE ISOLATION SETUP:
# Each team gets: namespace + ResourceQuota + LimitRange + NetworkPolicy + RBAC

# Namespace with team metadata:
apiVersion: v1
kind: Namespace
metadata:
  name: team-payments
  labels:
    team: payments
    cost-center: "CC-1234"
    environment: production
    pod-security.kubernetes.io/enforce: restricted

---
# ResourceQuota — limit total resources:
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-payments-quota
  namespace: team-payments
spec:
  hard:
    pods: "50"
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    services: "10"
    persistentvolumeclaims: "10"
    count/deployments.apps: "20"
    count/secrets: "50"

---
# LimitRange — default limits for containers:
apiVersion: v1
kind: LimitRange
metadata:
  name: team-payments-limits
  namespace: team-payments
spec:
  limits:
    - type: Container
      default:         { cpu: 200m, memory: 256Mi }
      defaultRequest:  { cpu: 50m,  memory: 64Mi }
      max:             { cpu: 2000m, memory: 4Gi }
      min:             { cpu: 10m,  memory: 16Mi }
    - type: PersistentVolumeClaim
      max: { storage: 50Gi }
      min: { storage: 1Gi }

---
# NetworkPolicy — namespace isolation:
# Deny all ingress from other namespaces:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-from-other-namespaces
  namespace: team-payments
spec:
  podSelector: {}      # applies to all pods in namespace
  policyTypes: [Ingress]
  ingress:
    # Allow from same namespace:
    - from:
        - podSelector: {}
    # Allow from monitoring namespace (Prometheus scraping):
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: monitoring
      ports:
        - protocol: TCP
          port: 9090
    # Allow from ingress controller:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx

---
# RBAC — team gets admin on their namespace only:
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-payments-admin
  namespace: team-payments
subjects:
  - kind: Group
    name: payments-team          # from OIDC/LDAP group
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin                    # built-in admin role (namespace-scoped)
  apiGroup: rbac.authorization.k8s.io
```


---

## SECTION 10: PERFORMANCE, COST & ADVANCED PATTERNS

---

**Q87. Load testing with k6 — performance testing in CI/CD.**

```javascript
// k6: modern load testing tool written in Go, scripts in JavaScript
// Runs from CI/CD, reports metrics to InfluxDB/Prometheus/Datadog

// load-test.js:
import http from "k6/http";
import { check, group, sleep } from "k6";
import { Rate, Trend, Counter } from "k6/metrics";
import { SharedArray } from "k6/data";

// Custom metrics:
const errorRate = new Rate("error_rate");
const checkoutDuration = new Trend("checkout_duration", true);  // true = time unit
const ordersCreated = new Counter("orders_created");

// Load test data (shared across VUs for efficiency):
const users = new SharedArray("users", () => JSON.parse(open("./test-users.json")));

// TEST STAGES — define load profile:
export const options = {
  stages: [
    { duration: "2m",  target: 10  },  // ramp up to 10 virtual users
    { duration: "5m",  target: 10  },  // stay at 10 VUs (baseline)
    { duration: "2m",  target: 50  },  // ramp up to 50 VUs (normal load)
    { duration: "10m", target: 50  },  // stay at 50 VUs
    { duration: "2m",  target: 200 },  // spike to 200 VUs
    { duration: "5m",  target: 200 },  // stay at spike
    { duration: "2m",  target: 0   },  // ramp down
  ],

  // THRESHOLDS — fail the test if violated:
  thresholds: {
    "http_req_duration":               ["p(95)<500", "p(99)<2000"],  // 95th < 500ms
    "http_req_duration{endpoint:checkout}": ["p(99)<3000"],          // checkout < 3s P99
    "http_req_failed":                 ["rate<0.01"],    // < 1% errors
    "error_rate":                      ["rate<0.05"],
    "checks":                          ["rate>0.95"],    // 95% checks pass
  },

  // Output to InfluxDB for Grafana dashboard:
  ext: {
    loadimpact: {
      projectID: 123456,
      name: "API Load Test - Main Flow",
    },
  },
};

// MAIN TEST SCENARIO:
export default function () {
  const user = users[Math.floor(Math.random() * users.length)];

  group("authentication", () => {
    const loginRes = http.post(
      `${__ENV.BASE_URL}/api/auth/login`,
      JSON.stringify({ email: user.email, password: user.password }),
      { headers: { "Content-Type": "application/json" } }
    );

    check(loginRes, {
      "login status 200": (r) => r.status === 200,
      "has access token":  (r) => JSON.parse(r.body).accessToken !== undefined,
    }) || errorRate.add(1);

    const token = JSON.parse(loginRes.body).accessToken;

    group("browse products", () => {
      const productsRes = http.get(`${__ENV.BASE_URL}/api/products?limit=20`, {
        headers: { Authorization: `Bearer ${token}` },
        tags: { endpoint: "products" },
      });
      check(productsRes, { "products 200": (r) => r.status === 200 });
    });

    group("checkout", () => {
      const startTime = Date.now();

      const checkoutRes = http.post(
        `${__ENV.BASE_URL}/api/orders`,
        JSON.stringify({ items: [{ productId: "prod_123", qty: 1 }] }),
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          tags: { endpoint: "checkout" },
        }
      );

      checkoutDuration.add(Date.now() - startTime);

      if (check(checkoutRes, { "order created": (r) => r.status === 201 })) {
        ordersCreated.add(1);
      } else {
        errorRate.add(1);
      }
    });
  });

  sleep(1);   // think time between iterations
}

// TEARDOWN — cleanup after test:
export function teardown(data) {
  console.log(`Load test complete. Orders created: ${ordersCreated.name}`);
}

// RUN:
# k6 run --env BASE_URL=https://api-staging.example.com load-test.js
# k6 run --out influxdb=http://influxdb:8086/k6 load-test.js
# k6 run --out experimental-prometheus-rw load-test.js

# GITHUB ACTIONS integration:
# - uses: grafana/k6-action@v0.3.0
#   with:
#     filename: tests/k6/load-test.js
#   env:
#     BASE_URL: https://api-staging.example.com
#     K6_CLOUD_TOKEN: ${{ secrets.K6_CLOUD_TOKEN }}
```

---

**Q88. Kubernetes cost optimization — in depth.**

```
COST BREAKDOWN IN KUBERNETES:
  Node costs:      EC2/GCP/Azure instance hours  (usually 60-70% of bill)
  Storage costs:   EBS/GCP PD/Azure Disk volumes (10-20%)
  Data transfer:   cross-AZ, cross-region, internet egress (10-15%)
  LB costs:        NLB/ALB per hour + per LCU (5-10%)

RIGHTSIZING — biggest opportunity:
  The #1 cost mistake: setting requests too high.
  Engineers set requests conservatively (large safety margin) → nodes fill up more slowly
  → you're paying for reserved capacity you're not using.

  Process:
  1. Measure actual P90 CPU and memory over 2 weeks (Prometheus / Goldilocks)
  2. Set CPU request = P90 actual CPU
  3. Set memory request = P90 actual memory * 1.2 (safety buffer)
  4. VPA "Off" mode: generate recommendations without applying them
     kubectl describe vpa api-vpa  →  shows Container Recommendations

  Tools:
  - Goldilocks (open source): VPA wrapper that generates recommendations in a dashboard
  - Kubecost: full cost visibility, rightsizing recommendations, per-team chargeback
  - AWS Compute Optimizer: rightsizes EC2 instances (EKS nodes)

SPOT INSTANCES:
  AWS Spot: up to 90% cheaper than on-demand.
  Constraint: 2-minute termination notice (SIGTERM → container should gracefully stop).

  Safe for:
  - Stateless services (API servers, workers) with proper graceful shutdown
  - Batch jobs (k8s Jobs with restartPolicy=OnFailure)
  - CI/CD runners

  NOT safe for:
  - Databases (StatefulSets with data)
  - Control plane nodes
  - Any workload that can't tolerate interruption

  Implementation with Karpenter:
  - NodePool: capacity-type: [spot, on-demand]  → prefers spot, falls back to on-demand
  - Disruption controller: when spot terminated, Karpenter provisions replacement

  Implementation with node groups:
  - Separate spot node group + on-demand node group
  - Pod anti-affinity or node selector + toleration to control placement
  - PodDisruptionBudget ensures graceful migration on spot interruption

RESOURCE QUOTAS PER TEAM (showback/chargeback):
  Label all resources with team/cost-center.
  OpenCost/Kubecost: aggregates cost by namespace, label, team.
  Monthly report per team: "Team Payments: $12,450 this month"
  → Teams self-optimize when they see their cost.

IDLE RESOURCE DETECTION:
  Deployments with scale=0: still paying for PVCs and LBs
  CronJobs that never run: zombie resources
  Old PVCs not mounted: paying for storage nobody uses

  kubectl get pvc -A | grep -v Bound  # unbound PVCs
  kubectl get deploy -A -o json | jq '.items[] | select(.spec.replicas == 0)'
```

---

**Q89. Container image optimization — build times and sizes.**

```bash
# STRATEGIES TO REDUCE IMAGE SIZE:

# 1. Choose the right base image:
# node:20          → 1.1GB (Debian, full OS)
# node:20-slim     → 240MB (Debian, fewer packages)
# node:20-alpine   → 170MB (Alpine Linux — minimal)
# node:20-bookworm-slim → 230MB (Debian Bookworm slim)
# distroless       → 120MB (Google distroless — no shell, no package manager)
# scratch          → binary size only (for compiled Go binaries)

# 2. Multi-stage builds (essential):
# See Q5 — keeps build tools out of final image

# 3. Combine RUN commands:
# BAD (3 layers):
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# GOOD (1 layer, also cleans cache):
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget \
    && rm -rf /var/lib/apt/lists/*

# 4. .dockerignore — keep build context small:
# Large build contexts slow down docker build (copies to daemon before build starts)

# 5. Use npm ci not npm install:
# npm ci: exact versions from lockfile, faster, removes node_modules first

# 6. Leverage layer caching correctly:
# Docker caches each layer. When a layer changes, all subsequent layers rebuild.
# Order: dependencies (rare change) → source code (frequent change)

# STRATEGIES TO REDUCE BUILD TIMES:

# Build cache from registry (CI/CD):
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/org/myapp:cache \
  --cache-to type=registry,ref=ghcr.io/org/myapp:cache,mode=max \
  .
# "mode=max" caches ALL intermediate layers, not just final

# GitHub Actions cache:
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# BuildKit inline cache (simpler, bakes cache into image):
DOCKER_BUILDKIT=1 docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from myapp:latest \
  -t myapp:latest .

# Parallel builds (multi-platform):
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push .
# Both platforms build simultaneously

# Build time analysis:
docker buildx build --progress=plain . 2>&1 | grep "^#"
# Shows each step, time spent, cache hits (CACHED vs running)

# DIVE — inspect image layers:
dive myapp:latest
# Shows: layer sizes, what's in each layer, wasted space (files overwritten by later layers)

# Nix flakes (reproducible builds — advanced):
# Every build produces exactly the same output given the same input
# No "it works on my machine" — hermetic builds
# Learning curve: steep. Worth it for: highly security-sensitive or complex builds
```

---

**Q90. Kubernetes operators — extending Kubernetes.**

```
OPERATOR PATTERN:
  An Operator is a custom controller that extends Kubernetes
  to manage complex stateful applications using domain-specific knowledge.

  K8s knows how to manage generic workloads (deployments, services).
  An Operator knows how to manage YOUR specific app (PostgreSQL cluster, Kafka, Redis).

  The Operator:
  1. Defines Custom Resource Definitions (CRDs) — new API types
  2. Watches those CRDs for changes
  3. Takes action to make actual state match desired state (reconciliation loop)

  Examples of production operators:
  - Prometheus Operator: define PrometheusRule, ServiceMonitor CRDs
  - cert-manager: define Certificate, ClusterIssuer CRDs
  - External Secrets Operator: define ExternalSecret CRDs
  - Strimzi (Kafka Operator): define Kafka, KafkaTopic CRDs
  - CloudNativePG: manages PostgreSQL clusters
  - Argo Rollouts: define Rollout, AnalysisRun CRDs

CUSTOM RESOURCE DEFINITION (CRD) EXAMPLE:
```
```yaml
# CRD — define the new resource type:
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: redisclusters.cache.example.com
spec:
  group: cache.example.com
  names:
    kind: RedisCluster
    plural: redisclusters
    singular: rediscluster
    shortNames: [rc]
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 9
                memory:
                  type: string
                  pattern: "^[0-9]+(Mi|Gi)$"
                version:
                  type: string
                  enum: ["6.2", "7.0", "7.2"]
              required: [replicas, memory, version]
            status:
              type: object
              properties:
                phase:
                  type: string
                  enum: [Pending, Running, Degraded, Failed]
                readyReplicas:
                  type: integer
      subresources:
        status: {}    # allow /status subresource
      additionalPrinterColumns:
        - name: Replicas
          type: integer
          jsonPath: .spec.replicas
        - name: Phase
          type: string
          jsonPath: .status.phase

---
# Custom Resource — use the new type:
apiVersion: cache.example.com/v1
kind: RedisCluster
metadata:
  name: session-cache
  namespace: production
spec:
  replicas: 3
  memory: 512Mi
  version: "7.2"
# The Operator sees this → creates StatefulSet, Services, ConfigMaps, Secrets
# automatically, handling all the Redis clustering complexity
```

```typescript
// Building an operator with operator-sdk (simplified):
// The reconcile loop — called whenever a RedisCluster changes:

async function reconcile(req: ReconcileRequest): Promise<void> {
  const cluster = await k8s.getCustomObject("cache.example.com/v1", "RedisCluster", req.name, req.namespace);

  // Desired state:
  const desiredReplicas = cluster.spec.replicas;

  // Actual state:
  const statefulSet = await k8s.getStatefulSet(req.name, req.namespace);
  const actualReplicas = statefulSet?.spec?.replicas ?? 0;

  if (!statefulSet) {
    // Create StatefulSet for this Redis cluster:
    await k8s.createStatefulSet(buildStatefulSet(cluster));
    await updateStatus(req, "Pending");
    return;
  }

  if (actualReplicas !== desiredReplicas) {
    // Scale the StatefulSet:
    await k8s.patchStatefulSet(req.name, req.namespace, {
      spec: { replicas: desiredReplicas }
    });
  }

  // Check health and update status:
  const readyReplicas = statefulSet.status?.readyReplicas ?? 0;
  const phase = readyReplicas === desiredReplicas ? "Running" : "Degraded";
  await updateStatus(req, phase, readyReplicas);
}
```

---

**Q91. Disaster recovery — RTO, RPO, backup strategies.**

```
DISASTER RECOVERY TERMS:

RPO (Recovery Point Objective):
  Maximum acceptable data loss measured in time.
  "We can lose at most X minutes of data"
  RPO = 0:   zero data loss (synchronous replication)
  RPO = 1h:  up to 1 hour of data can be lost
  Determines: backup frequency, replication strategy

RTO (Recovery Time Objective):
  Maximum acceptable downtime.
  "We must be back online within X minutes/hours"
  RTO = 5m:   very low tolerance (automated failover, hot standby)
  RTO = 4h:   moderate tolerance (warm standby, semi-automated restore)
  RTO = 24h:  low priority (cold standby, manual restore from backup)
  Determines: architecture complexity and cost

TIER 1: ACTIVE-ACTIVE (RPO=0, RTO=0, most expensive)
  Multiple regions, all active, load balanced.
  Any region can fail with no downtime and no data loss.
  Requires: multi-region database sync (Aurora Global, CockroachDB, Spanner)
  Challenge: distributed transactions, consistency vs availability trade-offs
  Cost: 3-4x single region
  Use: financial systems, payments, safety-critical

TIER 2: ACTIVE-PASSIVE / HOT STANDBY (RPO<1min, RTO<5min)
  Primary region active. Standby region has all infrastructure running.
  Data replication: synchronous (RDS Multi-AZ) or near-sync (Aurora Global <1s lag)
  Failover: automated DNS update, pre-warmed environment
  Cost: ~2x single region
  Use: SaaS with strong uptime SLAs

TIER 3: WARM STANDBY (RPO<15min, RTO<30min)
  Primary region active. Secondary has minimal infrastructure (not full scale).
  Scale up secondary on failover.
  Data: asynchronous replication, async S3 cross-region sync
  Cost: ~1.2x single region
  Use: most production applications

TIER 4: COLD STANDBY / BACKUP-RESTORE (RPO=hours, RTO=hours)
  Primary region active. Disaster → restore from backup to new region.
  Backups: automated (RDS automated backups, S3 cross-region replication)
  Cost: minimal (only backup storage)
  Use: non-critical, cost-sensitive
```
```bash
# VELERO — Kubernetes backup and disaster recovery:
# Backups: all K8s resources + PVC data snapshots
# Can restore to same or different cluster (DR)

# Install:
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket my-velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1

# Backup entire namespace:
velero backup create production-backup \
  --include-namespaces production \
  --ttl 720h0m0s   # keep for 30 days

# Scheduled backup (daily at 1am):
velero schedule create daily-backup \
  --schedule "0 1 * * *" \
  --include-namespaces production,staging \
  --ttl 720h

# Check backup status:
velero backup describe production-backup --details
velero backup logs production-backup

# RESTORE:
velero restore create \
  --from-backup production-backup \
  --include-namespaces production \
  --namespace-mappings production:production-restored   # restore to different NS

# Cross-region DR:
# 1. Velero in region-B pointing to same S3 bucket
# 2. velero restore create --from-backup daily-backup-20240115000000
# 3. Update DNS / Route53 to point to region-B

# DATABASE BACKUP PATTERN:
# Automated: RDS automated backups (1-35 days PITR) + weekly manual snapshot
# Export to S3: pg_dump → S3 (cross-region replication enabled)
# Test restores: monthly restore drill to verify backups actually work

# pg_dump to S3:
pg_dump $DATABASE_URL | gzip | aws s3 cp - \
  s3://my-backups/postgres/$(date +%Y/%m/%d)/prod-$(date +%H%M%S).sql.gz \
  --sse aws:kms --sse-kms-key-id $KMS_KEY_ID
```

---

**Q92. Continuous profiling — Pyroscope and performance analysis.**

```javascript
// CONTINUOUS PROFILING: always-on performance profiling in production
// Profiles CPU, memory, goroutines, mutex contention, I/O — continuously
// Overhead: < 1-2% CPU (much less than manual profiling)
// Value: find performance regressions automatically, understand production behavior

// PYROSCOPE — open-source continuous profiling server:
// Client sends profiles every N seconds → server aggregates, queryable by time range

// Node.js instrumentation:
import Pyroscope from "@pyroscope/nodejs";

Pyroscope.init({
  serverAddress: process.env.PYROSCOPE_SERVER_URL ?? "http://pyroscope:4040",
  appName:       `api.${process.env.NODE_ENV}`,
  tags: {
    service:     process.env.SERVICE_NAME ?? "api",
    pod:         process.env.POD_NAME    ?? "unknown",
    namespace:   process.env.POD_NAMESPACE ?? "unknown",
    version:     process.env.npm_package_version ?? "unknown",
  },
  // Profile types to collect:
  profileTypes: ["wall", "heap", "cpu"],
  sampleRate:   100,      // samples per second
  detectSubprocesses: false,
});

Pyroscope.start();
process.on("SIGTERM", () => Pyroscope.stop());

// WHAT PROFILES SHOW:
// CPU (wall clock): where does time actually go? network calls? DB queries? JSON parse?
// Heap: what's allocating memory? where are memory leaks?
// Goroutines (Go only): what are goroutines blocked on?

// USAGE IN GRAFANA:
// Grafana datasource: Pyroscope
// Query: { service_name="api", namespace="production" }
// Compare: last week vs today (detect regressions in deploy)
// Correlate: when P99 latency spike → query profile at that time → find hot function

// NODE.JS BUILT-IN PROFILING (no external tool):
// CPU profile for 30 seconds:
// node --prof server.js   → runs with V8 profiling → creates isolate-*.log
// node --prof-process isolate-*.log > processed.txt

// Heap snapshot (for memory leaks):
import { writeHeapSnapshot } from "v8";
process.on("SIGUSR2", () => {
  const filename = writeHeapSnapshot();
  console.log(`Heap snapshot written to ${filename}`);
  // Analysis: Chrome DevTools → Memory → Load snapshot → find detached DOM nodes, retained objects
});

// CLINIC.JS — Node.js performance toolkit:
// clinic doctor  -- node server.js  → diagnose: I/O bound? CPU bound? memory leak?
// clinic bubbleprof -- node server.js  → profile async operations (where is time spent?)
// clinic flame   -- node server.js  → CPU flame graph (which functions?)
// clinic heapprofiler -- node server.js → memory allocation profiling
```

---

**Q93. Feature flags and progressive delivery.**

```javascript
// FEATURE FLAGS: control feature rollout at runtime without code deployment
// Enable: A/B testing, canary releases, kill switches, beta programs

// IMPLEMENTATION WITH UNLEASH (open source):
import { Unleash, InMemStorageProvider } from "unleash-client";

const unleash = new Unleash({
  url:    process.env.UNLEASH_URL ?? "http://unleash:4242/api",
  appName: "api",
  customHeaders: { Authorization: process.env.UNLEASH_API_TOKEN! },
  refreshInterval:  15,    // check for changes every 15s
  metricsInterval:  60,    // send metrics every 60s
  storageProvider: new InMemStorageProvider(),
});

await unleash.start();

// Check flag:
if (unleash.isEnabled("new-checkout-flow")) {
  return newCheckout(cart);
}
return legacyCheckout(cart);

// Gradual rollout (% of users):
// Unleash console: new-checkout-flow → gradual rollout → 5% → 25% → 100%

// User-segment targeting:
const context = {
  userId:     req.user.id,
  properties: {
    plan:     req.user.plan,     // "enterprise"
    region:   req.user.region,  // "EU"
    betaTester: req.user.betaTester ? "true" : "false",
  },
};
if (unleash.isEnabled("new-checkout-flow", context)) { ... }

// IMPLEMENTATION WITH LAUNCHDARKLY (SaaS):
import LaunchDarkly from "launchdarkly-node-server-sdk";

const ldClient = LaunchDarkly.init(process.env.LD_SDK_KEY!);
await ldClient.waitForInitialization();

// Boolean flag:
const enabled = await ldClient.variation("new-checkout-flow", {
  key:  req.user.id,
  email: req.user.email,
  custom: { plan: req.user.plan },
}, false);  // default value if flag not found

// String/Number flag (multivariate):
const checkoutVersion = await ldClient.variation("checkout-version",
  { key: req.user.id }, "v1"
);
// Returns: "v1", "v2", or "v3" based on targeting rules

// OPENFEATURE (vendor-neutral standard):
import { OpenFeature } from "@openfeature/server-sdk";
import { UnleashClientProvider } from "@openfeature/unleash-provider";

OpenFeature.setProvider(new UnleashClientProvider(unleashClient));
const client = OpenFeature.getClient("api");

const newUI = await client.getBooleanValue("new-checkout-flow", false, {
  targetingKey: req.user.id,
});
```

```yaml
# KUBERNETES + FEATURE FLAGS:
# Flagger — automated canary analysis using feature flags:
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  service:
    port: 80
    targetPort: 3000
  analysis:
    interval: 1m
    threshold: 5          # fail after 5 consecutive errors
    maxWeight: 50         # max 50% canary traffic
    stepWeight: 10        # increase by 10% each interval
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99          # require 99% success rate
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500         # require P99 < 500ms
        interval: 1m
    # Webhook: check Unleash flag before promoting:
    webhooks:
      - name: acceptance-test
        type: pre-rollout
        url: http://flagger-loadtester/
        timeout: 30s
        metadata:
          type: bash
          cmd: "curl -s http://api-canary/health | jq .status | grep -q ok"
```

---

**Q94. Kubernetes Helm — managing secrets with sops.**

```bash
# SOPS (Secrets OPerationS) — Mozilla project
# Encrypts values in YAML/JSON/dotenv files
# Supports: AWS KMS, GCP KMS, Azure Key Vault, Age, PGP

# SETUP with AWS KMS:
# Create KMS key → get ARN
export KMS_ARN=arn:aws:kms:us-east-1:123456:key/abc-123

# .sops.yaml (define encryption rules):
creation_rules:
  - path_regex: charts/.*/values/secrets-production\.yaml$
    kms: "${KMS_ARN}"
  - path_regex: charts/.*/values/secrets-staging\.yaml$
    kms: "${STAGING_KMS_ARN}"

# Create and encrypt a secrets file:
cat > charts/api/values/secrets-production.yaml << EOF
database:
  password: "super-secret-password"
  url: "postgresql://user:pass@db:5432/prod"
jwt:
  secret: "long-random-jwt-secret-32-chars-min"
stripe:
  secretKey: "sk_live_xxxxx"
EOF

sops --encrypt charts/api/values/secrets-production.yaml \
  > charts/api/values/secrets-production.enc.yaml

# Git-safe: commit the .enc.yaml file (encrypted)
git add charts/api/values/secrets-production.enc.yaml
# NEVER commit the unencrypted file!

# HELM SECRETS PLUGIN:
helm plugin install https://github.com/jkroepke/helm-secrets

# Deploy with encrypted secrets:
helm secrets upgrade --install api ./charts/api \
  -f charts/api/values/production.yaml \
  -f charts/api/values/secrets-production.enc.yaml   # decrypted on-the-fly
  --namespace production

# How it works:
# 1. helm-secrets decrypts .enc.yaml to a temp file
# 2. helm uses temp file as values
# 3. temp file deleted after deploy
# Decryption uses IAM role (IRSA or node role) — no secret needed!

# GITOPS with sops + ArgoCD:
# ArgoCD Vault Plugin or ArgoCD Helm Secrets plugin
# ArgoCD has IAM role → decrypts secrets during sync
# Encrypted values in git → plain values in Kubernetes Secrets
```

---

**Q95. Kubernetes debugging — advanced techniques.**

```bash
# DEBUGGING PENDING PODS (node scheduler issues):
kubectl describe pod myapp-xyz
# Look in Events for:
# "0/3 nodes are available: 3 Insufficient memory"
#   → All nodes full. Scale up cluster or optimize resource requests.
# "0/3 nodes are available: 3 node(s) had taint..."
#   → Pod needs toleration for the taint.
# "0/3 nodes are available: 3 node(s) didn't match pod affinity"
#   → Anti-affinity rules prevent scheduling. Check topologySpreadConstraints.
# "0/3 nodes are available: 3 node(s) didn't match node selector"
#   → nodeSelector or nodeAffinity doesn't match any node.

# Check what's consuming resources on nodes:
kubectl describe nodes | grep -A 5 "Allocated resources"
kubectl top nodes
kubectl top pods -A --sort-by=memory | head -20   # memory hogs

# DEBUGGING CRASHLOOPBACKOFF:
kubectl describe pod myapp-xyz   # check Events for clue
kubectl logs myapp-xyz --previous  # logs from crashed container

# Common causes:
# - ENTRYPOINT/CMD wrong (file not found, permission denied)
# - Missing env var or secret
# - OOMKilled (increase memory limit)
# - Port already in use (port conflict in pod)
# - Config file wrong format
# - Failed health check before app is ready (increase initialDelaySeconds)

# DEBUGGING NETWORK ISSUES:
# Can pod A reach pod B?
kubectl exec -it pod-a -- wget -qO- http://pod-b-service:8080/health

# DNS resolution:
kubectl exec -it pod-a -- nslookup postgres-svc.production.svc.cluster.local
kubectl exec -it pod-a -- cat /etc/resolv.conf

# Network policy blocking traffic? Test with:
kubectl run netshoot --rm -it --image=nicolaka/netshoot -- \
  curl http://api-svc.production:80/health

# DEBUGGING IMAGE ISSUES:
# ImagePullBackOff → check pull secret and image name
kubectl get events | grep Failed
kubectl describe pod myapp | grep -A 5 "Failed to pull"

# Verify pull secret:
kubectl get secret ghcr-secret -n production -o json | \
  jq -r '.data[".dockerconfigjson"]' | base64 -d | jq .

# Test pull manually:
kubectl run pull-test \
  --image=ghcr.io/org/myapp:latest \
  --overrides='{"spec":{"imagePullSecrets":[{"name":"ghcr-secret"}]}}'

# EPHEMERAL DEBUG CONTAINERS (K8s 1.23+):
# Add tools to a running container without modifying its image:
kubectl debug -it api-pod-xyz \
  --image=nicolaka/netshoot \     # image with network debugging tools
  --target=api \                   # share PID/network namespace with api container
  -- bash

# Inside: can run tcpdump, dig, curl, ss, netstat, strace against the api process

# NODE DEBUGGING:
kubectl debug node/ip-10-0-1-5.ec2.internal \
  -it --image=ubuntu
# Creates pod on the node with host PID namespace
# /host mounts the node's filesystem → can inspect logs, configs, processes

# ETCD DEBUGGING (careful! etcd is sensitive):
kubectl exec -it -n kube-system etcd-master -- \
  etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  member list

# AUDIT LOGS — who changed what in the cluster:
# /var/log/kube-apiserver-audit.log (or CloudWatch Logs for EKS)
# Find who deleted a deployment:
cat audit.log | jq 'select(.verb=="delete" and .objectRef.resource=="deployments")'
```


---

## SECTION 11: HARD INTERVIEW QUESTIONS

---

**Q96. Design the CI/CD pipeline for a team of 50 engineers shipping 30 times a day.**

```
REQUIREMENTS ANALYSIS:
  50 engineers, 30 deploys/day, multiple services (assume 10-15 microservices).
  Goals: fast feedback (< 10 min from push to production), safe (no bad deploys),
  visible (every engineer knows state), recoverable (rollback in < 2 min).

PIPELINE DESIGN:

1. PULL REQUEST PHASE (< 5 min feedback):
   Trigger: on every commit to PR branch
   - lint + type-check (parallel, cached node_modules → 30s)
   - unit tests (parallelized across test suites, 2-3 min)
   - dependency vulnerability scan (npm audit + Snyk, 30s)
   - SAST scan (Semgrep, CodeQL, 2-3 min)
   - Secret detection (TruffleHog, 30s)
   All parallel. Fail fast. PR can't be merged until all green.

2. MAIN BRANCH PHASE (< 5 min):
   Trigger: on merge to main
   - Build Docker image (multi-stage, BuildKit cache from registry, ~2 min)
   - Image scan (Trivy, fail on CRITICAL, ~1 min)
   - Sign image (cosign keyless, ~30s)
   - Generate SBOM + provenance attestation (~30s)
   - Push to registry with git SHA tag

3. DEPLOY TO STAGING (< 3 min):
   Trigger: after successful image build
   - ArgoCD sync (GitOps: update image tag in k8s-configs repo)
   - kubectl rollout status (watch until complete, 2-3 min)
   - Smoke tests: 10 critical API endpoints checked (30s)
   - If smoke tests fail: auto-rollback + alert

4. AUTOMATED TESTING GATE (< 5 min):
   Against staging environment:
   - Integration tests (services talking to each other)
   - API contract tests (Pact)
   - k6 quick load test (30s, 50 VUs, reject if error rate > 1%)

5. PRODUCTION DEPLOY (< 5 min with gate):
   Trigger: staging tests pass (auto) OR manual approval for risky changes
   - Update production via GitOps (ArgoCD)
   - Canary: 5% traffic → watch 5 min → 25% → watch 5 min → 100%
   - Argo Rollouts: automated analysis at each step (error rate, latency P99)
   - If analysis fails: automatic rollback

TOTAL: PR phase 5min + build 5min + staging 5min + gate 5min + prod 5min = ~25 min
      Feature: PR approved → in production in 25-30 minutes total

SCALE CONSIDERATIONS:
  30 deploys/day = ~2-3/hour peak. Pipeline can run in parallel (one per service).
  Build cache in registry: critical for speed. Without cache: 10min build → with cache: 2min.
  Shared test infrastructure: containerized postgres/redis in CI (not shared live infra).
  Parallelism limits: set concurrency limits to not overwhelm staging.

OBSERVABILITY OF THE PIPELINE:
  - Slack notifications: PR checks, staging deploy done, production done, failures
  - Dashboard: deploy frequency, DORA metrics (lead time, failure rate, MTTR)
  - ArgoCD UI: visual diff of every change deployed
  - Every deploy tagged with git SHA → trace from production error → code commit
```

---

**Q97. How do you handle a database migration in production with zero downtime?**

```
THE PROBLEM:
  ALTER TABLE on a large table takes an exclusive lock → blocks all reads/writes.
  The bigger the table, the longer the lock → potential minutes of downtime.

THE SOLUTION: Expand-Contract (or Blue-Green migrations)

PHASE 1: EXPAND (backward-compatible change):
  Add column as nullable (no lock required for modern PostgreSQL with MVCC):
  ALTER TABLE orders ADD COLUMN new_status VARCHAR;
  
  Deploy new code: reads new_status if present, falls back to status.
  Old code: still works (ignores new column, it's nullable).

PHASE 2: BACKFILL:
  Populate new column for existing rows IN BATCHES (never one giant UPDATE):
  
  UPDATE orders SET new_status = status
  WHERE id BETWEEN $start AND $end AND new_status IS NULL;
  
  Process 1000 rows at a time, sleep between batches, run during off-peak.
  This avoids table-level locks and allows normal traffic to continue.

PHASE 3: SWITCH:
  Deploy code that writes to new_status only (both columns have same data).
  Add NOT NULL constraint + DEFAULT (cheap operation in PG 11+):
  ALTER TABLE orders ALTER COLUMN new_status SET DEFAULT 'pending' SET NOT NULL;

PHASE 4: CONTRACT (cleanup):
  After all code uses new_status, remove old column:
  ALTER TABLE orders DROP COLUMN status;
  Old code is no longer running → safe to drop.

ADDING INDEXES WITHOUT DOWNTIME:
  Normal: CREATE INDEX ... → table lock for duration (minutes/hours on large tables)
  Safe:   CREATE INDEX CONCURRENTLY ... → no lock, slower but online
  
  CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
  -- Verify index is valid:
  SELECT indexname, indisvalid FROM pg_indexes JOIN pg_index ON ...
  WHERE tablename = 'orders';

USING gh-ost (GitHub's online schema change):
  gh-ost is a tool that:
  1. Creates a shadow table (orders_ghc) with new schema
  2. Copies rows in batches from orders → orders_ghc
  3. Applies ongoing changes via MySQL binlog streaming (no triggers)
  4. When caught up: atomic table swap (orders ↔ orders_ghc)
  5. Old table available as orders_del for safety

  For PostgreSQL: pg_repack or pglogical-based migrations

MIGRATION FRAMEWORK (Node.js with Drizzle):
  1. Every migration is a .sql file or Drizzle migration script
  2. Migrations are idempotent (safe to run multiple times)
  3. Deploy migration BEFORE deploying new code (old code must tolerate new schema)
  4. Deploy new code AFTER migration completes
  5. Keep migration lock timeout short (fail fast, don't queue):
     SET lock_timeout = '3s';  -- fail if can't get lock in 3 seconds
     ALTER TABLE orders ADD COLUMN ...;
  6. Always have a DOWN migration for rollback
  7. Test migrations on a copy of production data before running on prod
```

---

**Q98. Explain the DORA metrics and how to improve them.**

```
DORA (DevOps Research and Assessment) — the 4 key metrics of software delivery:

1. DEPLOYMENT FREQUENCY
   How often do you deploy to production?
   Elite:    Multiple times per day
   High:     1x per day to 1x per week
   Medium:   1x per week to 1x per month
   Low:      Less than 1x per month

   How to improve: smaller batches, feature flags, trunk-based development,
   automated testing that gives confidence, remove manual approvals.

2. LEAD TIME FOR CHANGES
   Time from code committed → running in production.
   Elite:    < 1 hour
   High:     1 day to 1 week
   Medium:   1 week to 1 month
   Low:      1 to 6 months

   How to improve: faster CI/CD pipelines, parallel test execution,
   reduce PR review time (pair programming, smaller PRs), remove manual steps.

3. CHANGE FAILURE RATE
   % of deployments causing incidents or requiring rollback.
   Elite:    0-15%
   High:     16-30%
   Medium:   16-30% (same bracket — improvement here)
   Low:      46-60%

   How to improve: automated testing (unit, integration, E2E), canary deploys,
   feature flags, chaos engineering, better monitoring (catch before users do).

4. MEAN TIME TO RECOVER (MTTR)
   How long to restore service after an incident.
   Elite:    < 1 hour
   High:     < 1 day
   Medium:   1 day to 1 week
   Low:      > 1 week

   How to improve: automated rollbacks, blue-green deploys (instant switch),
   runbooks, on-call training, blameless postmortems, better observability.

MEASURING IN PRACTICE:

// Track in your deployment system:
type Deployment = {
  id:           string;
  commitSha:    string;
  commitTime:   Date;     // when commit was made
  deployTime:   Date;     // when deployed to production
  service:      string;
  status:       "success" | "failure" | "rollback";
  restoredAt?:  Date;     // if failure: when restored
};

// Lead time = deployTime - commitTime (per deploy)
// Deploy frequency = count(deploys per day) per service
// Change failure rate = count(failed/rollback deploys) / count(all deploys)
// MTTR = average(restoredAt - deployTime) for failed deploys

// Dashboard: Grafana + Prometheus or LinearB or Cortex.io
// Goal: review DORA metrics in engineering retrospectives monthly
// Watch for: MTTR creeping up (observability issue), failure rate up (test coverage),
//            lead time up (pipeline bottleneck, PR review time).
```

---

**Q99. What's your strategy for managing secrets at scale across 50 microservices?**

```
REQUIREMENTS AT SCALE:
  50 services × multiple environments (dev/staging/prod) × multiple secret types
  (DB passwords, API keys, TLS certs, JWT secrets, 3rd party credentials).
  
  Problems to solve:
  - How to distribute secrets without manual copy-paste (human error, exposure)
  - How to rotate secrets without downtime
  - How to audit who accessed what secret when
  - How to prevent secrets in source code, CI logs, container images

ARCHITECTURE: Vault + External Secrets Operator

1. VAULT (centralized secret store):
   - Dynamic secrets: Vault generates DB credentials per-service (not shared passwords)
   - Short-lived: credentials expire in 1h → compromise window limited
   - Audit log: every secret access logged with identity, timestamp, path
   - Secret engines: database (dynamic), KV v2 (static), PKI (TLS), AWS (dynamic IAM)
   
   Policy per service (least privilege):
   path "database/creds/payments-production" { capabilities = ["read"] }
   path "kv/data/payments/*" { capabilities = ["read"] }
   # payments service can ONLY read its own secrets

2. EXTERNAL SECRETS OPERATOR (bridge to Kubernetes):
   ExternalSecret CR → syncs from Vault → creates K8s Secret
   Auto-refreshes every hour (picks up rotated credentials)
   No service code changes needed (reads from K8s Secret as before)

3. ROTATION STRATEGY:
   DB passwords: Vault manages rotation automatically (db lease expires → new creds)
   API keys: rotate on schedule (monthly) using Vault KV version feature
   TLS certs: cert-manager auto-renews 15 days before expiry
   JWT secrets: rotate by running old + new simultaneously for 24h (all tokens reissued)
   
   Zero-downtime rotation:
   - Deploy new credential before removing old
   - Services pick up new credential via ExternalSecret refresh
   - Verify all services using new credential
   - Remove old credential

4. EMERGENCY PROCEDURES:
   Leaked secret → revoke immediately in Vault → ExternalSecret refreshes → new creds deployed
   Vault unavailable → K8s Secrets still work (last synced values persist)
   Vault disaster → restore from Raft snapshots (automated hourly backup to S3)

5. CI/CD SECRETS:
   GitHub Actions OIDC → assume AWS role → get secrets from Secrets Manager
   No long-lived AWS access keys in CI/CD
   Each pipeline has least-privilege IAM role for its needs

AUDIT AND COMPLIANCE:
  Vault audit log → S3 → Athena for querying → CloudWatch Alerts for anomalies
  Access review quarterly: which services access which secrets?
  Principle of least privilege enforced by policy as code (Vault + OPA)
```

---

**Q100. How does Kubernetes networking work under the hood — from pod to pod?**

```
SCENARIO: Pod A (10.0.1.15) → Service (10.96.0.100) → Pod B (10.0.2.20)
Both pods on different nodes.

STEP 1: Application calls Service ClusterIP (10.96.0.100)
  App creates TCP connection to 10.96.0.100:80.
  Packet enters pod's virtual network interface (eth0 in pod = veth pair on host).

STEP 2: Packet leaves pod, enters host network
  veth pair: one end in pod namespace, other end on host.
  Packet arrives on host network interface (veth_xyz or eth0).

STEP 3: iptables / eBPF intercepts (kube-proxy)
  kube-proxy has programmed iptables (or eBPF maps) rules:
  -A KUBE-SERVICES -d 10.96.0.100/32 -p tcp --dport 80 -j KUBE-SVC-XXXXX
  -A KUBE-SVC-XXXXX -m statistic --mode random --probability 0.5 -j KUBE-SEP-AAA
  -A KUBE-SVC-XXXXX -j KUBE-SEP-BBB
  
  iptables NAT: randomly selects Pod B (10.0.2.20:8080).
  DNAT: rewrites destination from 10.96.0.100:80 → 10.0.2.20:8080.
  Connection tracking: kernel remembers this mapping (SNAT on return path).

STEP 4: Routing to Pod B's node
  Now packet destination is 10.0.2.20. Where is this?
  CNI has programmed routes on each node:
  ip route show → 10.0.2.0/24 via 10.0.0.2 dev eth0
  (10.0.2.x pods are on node B, reached via node B's IP 10.0.0.2)
  
  With overlay (VXLAN/Flannel):
    Packet encapsulated in UDP with VXLAN header.
    Outer packet: Node A (10.0.0.1) → Node B (10.0.0.2) via regular network.
    Arrives at Node B, VXLAN decapsulated.
  
  With BGP (Calico):
    No encapsulation. Real routing protocol advertises pod CIDR routes.
    Node A's router knows: 10.0.2.0/24 is reachable via Node B.
    Pure L3 routing, no overhead.

STEP 5: Packet arrives at Node B
  Node B's kernel: destination 10.0.2.20 → which interface?
  ip route: 10.0.2.20 via dev veth_pod_b
  Packet delivered to Pod B's veth interface.

STEP 6: Response path
  Pod B responds: src=10.0.2.20, dst=10.0.1.15.
  Node B routes back to Node A via CNI routes.
  Node A's conntrack: sees response, un-NATed (10.0.2.20 → 10.96.0.100).
  Pod A receives response from 10.96.0.100 (never saw real Pod B IP).

KEY INSIGHTS:
- ClusterIP is a virtual IP: it lives ONLY in iptables/eBPF, not on any interface
- DNS: kube-dns/CoreDNS returns ClusterIP for service name
- kube-proxy is a lie of abstraction: it doesn't proxy packets, it programs the kernel
- eBPF (Cilium): replaces iptables with kernel-level programs (faster, observable via Hubble)
- CNI handles pod-to-pod routing across nodes
- Service mesh (Istio/Linkerd): intercepts packets BEFORE they leave the pod (transparent proxy via iptables rules that redirect to Envoy sidecar)
```

---

**Q101. Kubernetes pod scheduling — taints, tolerations, affinity, priority in one complete example.**

```yaml
# COMPLETE SCHEDULING SCENARIO:
# Requirement: GPU training job must run on GPU nodes only,
# API must spread across 3 AZs, batch workers prefer spot but tolerate on-demand.

# GPU NODE SETUP (taint prevents non-GPU pods):
# kubectl taint nodes gpu-node-1 nvidia.com/gpu=true:NoSchedule
# kubectl taint nodes gpu-node-1 workload=gpu:NoSchedule

# SPOT NODE SETUP:
# kubectl taint nodes spot-node-1 spot=true:NoSchedule

# 1. GPU Training Job — must run on GPU nodes:
apiVersion: batch/v1
kind: Job
metadata:
  name: model-training
spec:
  template:
    spec:
      # Tolerations: accept the taints on GPU nodes
      tolerations:
        - key: "nvidia.com/gpu"
          operator: Equal
          value: "true"
          effect: NoSchedule
        - key: "workload"
          operator: Equal
          value: "gpu"
          effect: NoSchedule

      # NodeSelector: must be on GPU node
      nodeSelector:
        accelerator: nvidia-tesla-v100    # label on GPU nodes

      # OR use NodeAffinity (more expressive):
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values: [p3.2xlarge, p3.8xlarge, p4d.24xlarge]

      # Priority class: preempt lower-priority pods if needed
      priorityClassName: high-priority

      containers:
        - name: trainer
          image: myorg/trainer:latest
          resources:
            requests:
              nvidia.com/gpu: 1     # request 1 GPU
            limits:
              nvidia.com/gpu: 1

      restartPolicy: OnFailure

---
# 2. API Deployment — spread across AZs, avoid same node:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 6
  template:
    spec:
      # Spread evenly across 3 AZs:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels: { app: api }
        # Also spread within each AZ (across nodes):
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: ScheduleAnyway   # prefer spread, but don't block
          labelSelector:
            matchLabels: { app: api }

      # Anti-affinity: prefer not to co-locate with other API pods:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels: { app: api }
              topologyKey: kubernetes.io/hostname   # never 2 api pods on same node
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 50
              podAffinityTerm:
                labelSelector:
                  matchLabels: { app: api }
                topologyKey: topology.kubernetes.io/zone  # prefer different AZ

      # Only schedule on on-demand nodes (don't run on spot):
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: karpenter.sh/capacity-type
                    operator: In
                    values: [on-demand]

---
# 3. Batch Worker — prefer spot, fall back to on-demand:
spec:
  template:
    spec:
      # Tolerate spot nodes:
      tolerations:
        - key: spot
          operator: Equal
          value: "true"
          effect: NoSchedule

      # Prefer spot (weight 100), accept on-demand:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: karpenter.sh/capacity-type
                    operator: In
                    values: [spot]

---
# Priority Classes:
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical-system
value: 2000000      # highest — preempts everything
globalDefault: false

---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000     # preempts medium and low

---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-priority
value: 100000
globalDefault: true  # default for everything that doesn't specify

---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1000        # batch jobs, can be preempted by higher priority
```

---

**Q102–Q108: Quick-fire hard questions (concise full answers)**

```
Q102. What happens when you delete a Kubernetes namespace?
  Kubernetes marks the namespace as Terminating and starts deleting all resources
  inside: pods, services, configmaps, secrets, PVCs, etc.
  Each resource goes through its own deletion lifecycle (finalizers must complete).
  If a resource has a finalizer, namespace stays Terminating until finalizer is removed.
  Stuck namespace: check for resources with finalizers:
    kubectl api-resources --verbs=list --namespaced -o name | \
      xargs -I {} kubectl get {} -n stuck-ns -o name 2>/dev/null
  Force remove finalizer: kubectl patch namespace stuck-ns -p '{"metadata":{"finalizers":[]}}' --type=merge

Q103. Explain pod disruption budgets and when they matter.
  PDB guarantees minimum availability during VOLUNTARY disruptions
  (kubectl drain, rolling updates, node upgrades).
  Does NOT protect against involuntary disruptions (node crashes, OOMKill).
  
  minAvailable: 2  → always keep 2 pods running
  maxUnavailable: 1 → at most 1 pod can be unavailable at any time
  
  Matters for: cluster upgrades (kubectl drain), Kubernetes version bumps,
  Cluster Autoscaler scale-down, spot instance termination.
  Without PDB: drain removes all pods from a node simultaneously → outage.
  With PDB: drain waits until replacement pods are ready before removing more.

Q104. How do you prevent secret sprawl in a large organization?
  1. Centralize: Vault as the single source of truth for all secrets
  2. Dynamic secrets: never have static shared credentials (revoked when lease expires)
  3. Policy as code: Vault policies in git, reviewed like code
  4. Audit: CloudTrail + Vault audit log + anomaly detection
  5. Scanning: TruffleHog + GitHub secret scanning + pre-commit hooks
  6. Namespacing: secrets scoped to service + environment (payments/production/db)
  7. Rotation: automated via Vault + External Secrets Operator
  8. Access review: quarterly review of who has access to what

Q105. Difference between kubectl create and kubectl apply for CRDs.
  CRDs should be applied with kubectl apply (or server-side apply).
  Never use kubectl create for CRDs in GitOps — it fails if already exists.
  Helm handles CRDs differently: helm install only creates CRDs, doesn't update them
  on helm upgrade (to prevent accidental schema changes). To update CRDs: apply separately.
  
  Pattern: in ArgoCD App of Apps:
    - App 1: apply CRDs (runs first, sync-wave: -1)
    - App 2: apply operators that use the CRDs (sync-wave: 0)
    - App 3: apply custom resources (sync-wave: 1)

Q106. How do you handle a production outage in a microservices system?
  1. Alert acknowledgment: on-call acknowledges within 5 minutes
  2. Triage: check dashboards — error rate, latency, which service? upstream or downstream?
  3. Communication: open incident channel, update status page, notify stakeholders
  4. Hypothesis: recent deploy? traffic spike? dependency failure?
     kubectl rollout history deploy/api → check recent deployments
     git log --since="1 hour ago" --all → what changed?
  5. Mitigate (fastest first):
     - Rollback: kubectl rollout undo deploy/api (< 2 min)
     - Feature flag: disable suspect feature
     - Traffic: shift to previous version via blue-green switch
     - Scale: add replicas if capacity issue
  6. Verify: metrics returning to normal, error rate dropping
  7. Communicate: "Service restored. Root cause investigation ongoing."
  8. Postmortem: within 48 hours (see Q76)

Q107. What is the difference between HPA and KEDA?
  HPA: Kubernetes-native, scales on CPU/memory/custom metrics (one metric API).
       Limited to: CPU %, memory %, metrics from custom metrics adapter.
       Cannot scale to zero (minimum 1 replica unless you patch).
  
  KEDA: event-driven, scales based on external event sources.
       50+ built-in scalers: Kafka lag, SQS depth, RabbitMQ queue, cron, Prometheus query,
       Azure Service Bus, MySQL query result, Datadog metric, etc.
       CAN scale to zero: when no messages, scale to 0 pods (cost saving for batch workers).
       Builds on top of HPA (creates an HPA under the hood, manages it).
       Use KEDA when: message-driven workloads, need to scale to zero, need event-source metrics.

Q108. Explain Kubernetes resource QoS classes.
  Kubernetes assigns one of three QoS classes to every pod, which determines
  eviction priority when nodes run out of resources:

  1. GUARANTEED (evicted last):
     CPU and memory requests == limits for every container.
     Pod gets exactly what it requested, no more.
     resources: { requests: {cpu: 500m, memory: 256Mi}, limits: {cpu: 500m, memory: 256Mi} }

  2. BURSTABLE (evicted second):
     At least one container has requests != limits, or only limits specified.
     Pod can use more than requests if node has capacity.
     resources: { requests: {cpu: 100m, memory: 64Mi}, limits: {cpu: 500m, memory: 256Mi} }

  3. BEST EFFORT (evicted first):
     No requests or limits specified at all.
     Gets what's left over. First to be killed under node pressure.
     resources: {}  ← don't do this in production!

  PRODUCTION RULE: always set both requests and limits.
  Critical services (payment, auth): Guaranteed QoS.
  General services: Burstable QoS.
  Batch/background jobs: Burstable is fine, or accept Best Effort if truly non-critical.
```

---

*End of DevOps Interview Questions & Answers — Premium Reference*
*Total: 108 questions fully answered with production-quality code examples.*
*Topics: Docker (Q1–Q30), Kubernetes Core (Q31–Q40), kubectl (Q41–Q50), CI/CD (Q51–Q56), IaC (Q57–Q61), AWS (Q62–Q65), Observability (Q66–Q71), Security & Supply Chain (Q72–Q77), K8s Networking & Storage (Q78–Q86), Performance & Advanced (Q87–Q95), Hard Interview Questions (Q96–Q108)*


---

## SECTION 10: COMPLETE AUDIT — ALL MISSING TOPICS (Q109–Q160)

> Every gap identified in external review, now answered in full with production code.

---

**Q109. EXPOSE vs -p in Docker — the single most common interview trick question.**

```
QUESTION: Your Dockerfile has EXPOSE 8080. You run: docker run -p 3333:8080 myapp.
Your app inside the container listens on port 8080. Will it work?

ANSWER: YES — and understanding why reveals exactly what each directive does.

EXPOSE — documentation only, does NOT publish the port:
  Records that the container intends to listen on 8080.
  Visible in: docker inspect / docker image inspect.
  Readable by tools like docker-compose to know which ports to map.
  Does NOT open any firewall rule.
  Does NOT make the port reachable from the host.

-p HOST_PORT:CONTAINER_PORT — actually maps the port:
  -p 3333:8080 means:
    Listen on the HOST at port 3333.
    Forward all traffic to CONTAINER port 8080.
  The app inside the container must listen on 8080 (not 3333).
  The app never knows about the host port.

TRAFFIC FLOW:
  Browser → localhost:3333
  → Docker NAT (iptables rule) forwards to container:8080
  → App inside container (listening on 8080) receives the request

SCENARIO TABLE:
  EXPOSE  | -p flag      | App listens | Reachable?
  ------------------------------------------------
  8080    | -p 3333:8080 | 8080        | YES ✓
  8080    | -p 3333:8080 | 3333        | NO  (app wrong port inside)
  8080    | (none)       | 8080        | NO  (port not published)
  (none)  | -p 3333:8080 | 8080        | YES (EXPOSE irrelevant)

KEY RULE: -p always wins. EXPOSE is ignored at runtime.
  What matters: your app's listen port == the right side of -p.

docker run -P (capital P) — the ONE case where EXPOSE matters:
  Publishes ALL exposed ports to random host ports.
  EXPOSE 8080 → mapped to something like 0.0.0.0:49153->8080/tcp.
  Never used in production — always use explicit -p.
```

---

**Q110. Service Mesh — Istio deep dive.**

```
A service mesh is a dedicated infrastructure layer for service-to-service
communication. It handles mTLS encryption, retries, circuit breaking,
traffic splitting, and observability — without any app code changes.

Implementation: Envoy sidecar injected into every pod.
Control plane (istiod) pushes config to all Envoy sidecars.

TRAFFIC WITH ISTIO:
  Pod A → Envoy-A ──mTLS──> Envoy-B → Pod B
  (encrypted, retried, traced, circuit-broken)
```

```yaml
# Traffic splitting — canary via VirtualService:
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-vs
  namespace: production
spec:
  hosts: [api]
  http:
    - match:
        - headers:
            x-canary: { exact: "true" }
      route:
        - destination: { host: api, subset: v2 }
    - route:
        - destination: { host: api, subset: v1 }
          weight: 90
        - destination: { host: api, subset: v2 }
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: 5xx,gateway-error,connect-failure
      timeout: 10s
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-dr
  namespace: production
spec:
  host: api
  trafficPolicy:
    outlierDetection:           # circuit breaker
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels: { version: v1 }
    - name: v2
      labels: { version: v2 }
---
# Fault injection — test resilience without code changes:
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-fault
spec:
  hosts: [api]
  http:
    - fault:
        delay:
          percentage: { value: 10.0 }
          fixedDelay: 5s
        abort:
          percentage: { value: 5.0 }
          httpStatus: 503
      route:
        - destination: { host: api }
---
# Strict mTLS — all service-to-service traffic encrypted:
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Zero-trust: deny unless explicitly allowed:
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-authz
  namespace: production
spec:
  selector:
    matchLabels: { app: api }
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/frontend"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/v1/*"]
```

```
ISTIO OBSERVABILITY (zero code changes):
  Metrics: RED metrics per service → Prometheus/Grafana (automatic)
  Traces:  every request traced (W3C headers injected) → Jaeger/Tempo
  Kiali:   visual service graph, health, config validation UI

ISTIO vs LINKERD vs CILIUM:
  Istio:   full-featured, L7 policies, multi-cluster. Complex to operate.
  Linkerd: lighter (Rust proxy), lower latency overhead. Simpler.
  Cilium:  eBPF-based, no sidecar. Best performance. No Envoy.
```

---

**Q111. Prometheus Operator — ServiceMonitor, PodMonitor, PrometheusRule.**

```yaml
# Prometheus Operator manages Prometheus via Kubernetes CRDs.
# Instead of editing prometheus.yml, you create CRD objects.
# Install: helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack

---
# ServiceMonitor — scrape metrics from a Kubernetes Service:
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-monitor
  namespace: monitoring
  labels:
    release: kube-prometheus-stack   # must match Prometheus selector
spec:
  selector:
    matchLabels: { app: api }
  namespaceSelector:
    matchNames: [production]
  endpoints:
    - port: metrics
      path: /metrics
      interval: 15s
      scrapeTimeout: 10s
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'go_.*'
          action: drop               # drop Go runtime noise

---
# PodMonitor — scrape Pods directly (no Service needed):
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: worker-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels: { app: worker }
  podMetricsEndpoints:
    - port: metrics
      interval: 30s

---
# PrometheusRule — alerting + recording rules as CRDs:
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-alerts
  namespace: monitoring
  labels:
    release: kube-prometheus-stack
spec:
  groups:
    - name: api.rules
      rules:
        # Recording rule — pre-compute expensive query:
        - record: job:api_request_duration_seconds:p99
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{job="api"}[5m]))
              by (le, route))

        # Alert — high error rate:
        - alert: APIHighErrorRate
          expr: |
            sum(rate(http_requests_total{job="api",status=~"5.."}[5m]))
            / sum(rate(http_requests_total{job="api"}[5m])) > 0.05
          for: 2m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "API error rate above 5%"
            description: "Error rate is {{ $value | humanizePercentage }}"
            runbook_url: "https://wiki.company.com/runbooks/api-errors"

        - alert: APIHighLatency
          expr: job:api_request_duration_seconds:p99 > 1.0
          for: 5m
          labels: { severity: warning }
          annotations:
            summary: "API P99 latency above 1s"
```

---

**Q112. Kubernetes Gateway API — successor to Ingress.**

```yaml
# Gateway API: GA in K8s 1.28. Replaces Ingress.
# Problem with Ingress: vendor annotation chaos, limited expressiveness.
# Solution: role-oriented, typed, extensible without annotations.

# ROLES:
#   Infrastructure provider → GatewayClass (e.g. nginx, istio)
#   Cluster operator        → Gateway (ports/protocols accepted)
#   App developer           → HTTPRoute / GRPCRoute (routing rules)

---
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: nginx
spec:
  controllerName: gateway.nginx.org/nginx-gateway-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: prod-gateway
  namespace: infra
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: wildcard-tls
      allowedRoutes:
        namespaces:
          from: Selector
          selector:
            matchLabels:
              gateway-access: allowed
---
# HTTPRoute — managed by app teams, attaches to Gateway:
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
  namespace: production
spec:
  parentRefs:
    - name: prod-gateway
      namespace: infra
      sectionName: https
  hostnames: ["api.example.com"]
  rules:
    - matches:
        - path: { type: PathPrefix, value: /v1 }
      backendRefs:
        - name: api-svc
          port: 80
          weight: 90
        - name: api-svc-canary    # native traffic splitting, no annotations
          port: 80
          weight: 10
      filters:
        - type: ResponseHeaderModifier
          responseHeaderModifier:
            add:
              - name: x-served-by
                value: gateway

# GATEWAY API vs INGRESS:
# Feature              Ingress        Gateway API
# Role separation      None           GatewayClass/Gateway/Route
# Traffic splitting    Annotations    weight field (native)
# Header manipulation  Annotations    filters (native)
# gRPC routing         No             GRPCRoute
# Cross-namespace      No             allowedRoutes
# Extensibility        Annotations    Policy attachment (typed)
```

---

**Q113. Terraform testing — Terratest, conftest, checkov.**

```bash
# THREE LEVELS:
# 1. Static analysis  — fast, no cloud calls
# 2. Policy as code   — OPA/conftest against terraform plan
# 3. Integration      — Terratest, real cloud resources

# Level 1: static
terraform validate
tflint --recursive
checkov -d . --framework terraform   # 1000+ security checks
```

```rego
# Level 2: conftest policy (OPA Rego)
# policy/s3.rego:
package terraform.s3
import future.keywords.contains

deny contains msg if {
  r := input.resource_changes[_]
  r.type == "aws_s3_bucket"
  r.change.after.acl == "public-read"
  msg := sprintf("S3 bucket '%s' must not be public-read", [r.address])
}

deny contains msg if {
  r := input.resource_changes[_]
  r.type == "aws_s3_bucket"
  not r.change.after.tags.Environment
  msg := sprintf("S3 bucket '%s' must have an Environment tag", [r.address])
}
```

```bash
# Run conftest:
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
conftest test tfplan.json --policy policy/
```

```go
// Level 3: Terratest (Go)
func TestVPCModule(t *testing.T) {
    t.Parallel()
    opts := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr":    "10.0.0.0/16",
            "environment": "test",
        },
    })
    defer terraform.Destroy(t, opts)
    terraform.InitAndApply(t, opts)

    vpcID := terraform.Output(t, opts, "vpc_id")
    assert.NotEmpty(t, vpcID)

    // Verify via AWS API:
    vpc := aws.GetVpcById(t, vpcID, "us-east-1")
    assert.Equal(t, "10.0.0.0/16", aws.GetVpcCidr(t, vpc))

    // Idempotency check — second apply must show 0 changes:
    exitCode := terraform.PlanExitCode(t, opts)
    assert.Equal(t, 0, exitCode)
}
```

```bash
go test ./test/ -v -timeout 45m

# CI ORDER:
# 1. validate + tflint + checkov  (fast, always run)
# 2. conftest plan JSON           (medium speed, always)
# 3. Terratest                    (slow/costly — run on main or nightly)
```

---

**Q114. Distributed tracing — Jaeger, Tempo, TraceQL.**

```
CONCEPTS:
  Trace:  entire request journey across services (unique trace ID)
  Span:   one unit of work within a trace (unique span ID)
  Parent span → child spans form a call tree

PROPAGATION (how Service B knows it belongs to the same trace):
  W3C Trace Context: traceparent: 00-{traceId}-{spanId}-{flags}
  B3 (legacy/Zipkin): X-B3-TraceId, X-B3-SpanId, X-B3-Sampled

SAMPLING:
  Head sampling: decide at start. 1% rate = might miss rare errors.
  Tail sampling: decide at end based on outcome.
    Always keep: errors, slow traces (>2s), specific attributes.
    Jaeger and Tempo both support tail-based sampling.

JAEGER vs TEMPO:
  Jaeger: own storage (Cassandra/Elasticsearch), mature, full UI.
  Tempo:  Grafana backend, uses S3/GCS (cheap), TraceQL language,
          Loki integration (click log line → jump to trace).
```

```yaml
# Tempo config (S3 storage):
storage:
  trace:
    backend: s3
    s3:
      bucket: my-tempo-traces
      region: us-east-1
distributor:
  receivers:
    otlp:
      protocols:
        grpc: { endpoint: 0.0.0.0:4317 }
        http: { endpoint: 0.0.0.0:4318 }
compactor:
  compaction:
    block_retention: 336h   # 14 days
```

```javascript
// TraceQL queries in Grafana:

// All traces with errors:
{ status = error }

// Slow DB queries (span > 500ms):
{ span.db.system = "postgresql" && duration > 500ms }

// All traces for specific user in payments service:
{ resource.service.name = "payments" && span.user.id = "usr_123" }
```

---

**Q115. eBPF — how it works and DevOps use cases.**

```
WHAT IS EBPF?
  Run sandboxed programs in the Linux kernel without modifying kernel
  source or loading kernel modules.

  eBPF approach:
  1. Write small C program → compile to eBPF bytecode
  2. Load into kernel via syscall
  3. Kernel verifier checks safety (no infinite loops, bounds checked)
  4. JIT compiled to native machine code
  5. Runs at kernel speed, attached to hook points

HOOK POINTS:
  Networking:  XDP (before network stack), TC (traffic control)
  Syscalls:    kprobes, tracepoints
  User space:  uprobes (trace malloc, etc.)
  Security:    LSM hooks

DEVOPS USE CASES:

1. NETWORKING (Cilium):
   - Replace iptables with eBPF maps (O(1) vs O(n) lookup)
   - kube-proxy replacement (load balancing in kernel)
   - L7 network policy (HTTP method filtering at kernel level, no sidecar)
   - WireGuard transparent encryption between nodes

2. OBSERVABILITY (Pixie, Parca):
   - Zero-instrumentation tracing: capture HTTP requests at kernel level
     with no code changes, no sidecars, no restarts
   - Continuous CPU profiling (< 2% overhead, production-safe)
   - Network flow visibility: pod-to-pod with latency

3. SECURITY (Tetragon, Falco eBPF driver):
   - System call filtering per container
   - File access monitoring (alert when /etc/shadow is read)
   - Process execution alerts (unexpected binary in container)
   - Network egress blocking (unexpected outbound connections)
```

```bash
# BCC tools (pre-built eBPF programs):
execsnoop             # watch all new processes + arguments
biolatency -mD 10     # disk I/O > 10ms
tcplife               # network connections with latency
fileslower 10         # filesystem ops slower than 10ms

# bpftrace one-liners:
bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[comm] = count(); }'
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'
```

---

**Q116. Pod Security Standards (PSS).**

```yaml
# PSS replaced PodSecurityPolicy (removed K8s 1.25).
# Three levels: privileged / baseline / restricted
# Three modes: enforce (reject) / audit (log) / warn (return warning)

# Apply to namespace via labels:
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.28
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

# Compliant pod for restricted namespace:
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: production
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:2.1.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: [ALL]
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}

# KYVERNO — enforce custom policies beyond built-in PSS:
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-resources
      match:
        any:
          - resources: { kinds: [Pod] }
      validate:
        message: "CPU and memory requests/limits are required"
        pattern:
          spec:
            containers:
              - resources:
                  requests:
                    memory: "?*"
                    cpu: "?*"
                  limits:
                    memory: "?*"
```

---

**Q117. Helm advanced — diff, test, library charts, sops secrets.**

```bash
# HELM DIFF — preview changes before upgrade:
# Install: helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade api ./charts/api --values values.prod.yaml
helm diff upgrade api ./charts/api --detailed-exitcode  # exit 2 = changes exist
```

```yaml
# HELM TEST — verify release health:
# charts/api/templates/tests/connection-test.yaml:
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test"
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
    - name: wget
      image: busybox
      command: ['wget', '--spider', '--timeout=5',
        'http://{{ .Release.Name }}-svc:{{ .Values.service.port }}/health']
```

```bash
helm test api --timeout 5m   # PASS: api/test/api-test-connection
```

```yaml
# LIBRARY CHART — shared templates across multiple charts:
# Chart.yaml: type: library  (cannot be installed directly)

# charts/common-lib/templates/_deployment.yaml:
{{- define "common-lib.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
  labels: {{- include "common-lib.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount | default 2 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          resources: {{- toYaml .Values.resources | nindent 12 }}
{{- end -}}

# App chart imports library in Chart.yaml:
# dependencies:
#   - name: common-lib
#     version: "1.0.0"
#     repository: "oci://ghcr.io/myorg/charts"
# App's deployment.yaml: {{ include "common-lib.deployment" . }}
```

```bash
# HELM SECRETS + SOPS — encrypt values files:
# Install: helm plugin install https://github.com/jkroepke/helm-secrets

sops --encrypt --kms arn:aws:kms:us-east-1:123:key/abc secrets.yaml > secrets.enc.yaml
helm secrets upgrade api ./charts/api -f values.yaml -f secrets.enc.yaml
# sops decrypts transparently at helm time

# .sops.yaml:
# creation_rules:
#   - path_regex: .*secrets.*\.yaml$
#     kms: arn:aws:kms:us-east-1:123:key/abc
```

---

**Q118. GitOps advanced — ArgoCD ApplicationSet, sync waves, health checks.**

```yaml
# ApplicationSet — manage many Applications from one template:
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: all-services
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - service: api
            namespace: production
            replicaCount: "3"
          - service: worker
            namespace: production
            replicaCount: "5"
    # Git directory generator:
    # - git:
    #     repoURL: https://github.com/myorg/k8s-configs
    #     revision: HEAD
    #     directories:
    #       - path: services/*
    # Cluster generator (deploy to multiple clusters):
    # - clusters:
    #     selector:
    #       matchLabels: { environment: production }
  template:
    metadata:
      name: '{{service}}'
    spec:
      source:
        repoURL: https://github.com/myorg/k8s-configs
        path: 'services/{{service}}'
        helm:
          parameters:
            - name: replicaCount
              value: '{{replicaCount}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated: { prune: true, selfHeal: true }
        syncOptions: [CreateNamespace=true]

---
# Sync Waves — control resource deployment ORDER:
# Wave -1: CRDs first
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
# Wave 0: operators → Wave 1: databases → Wave 2: applications

---
# Custom Health Check — Lua script for custom CRD:
# In argocd-cm ConfigMap:
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.example.com_MyResource: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.phase == "Ready" then
        hs.status = "Healthy"
        hs.message = "Resource is ready"
      elseif obj.status.phase == "Failed" then
        hs.status = "Degraded"
        hs.message = obj.status.message
      else
        hs.status = "Progressing"
      end
    else
      hs.status = "Progressing"
    end
    return hs

  # Prevent ArgoCD drift alerts for HPA-managed replicas:
  resource.customizations.ignoreDifferences: |
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

---

**Q119. Multi-cloud — Azure and GCP core services for DevOps.**

```
AWS vs AZURE vs GCP SERVICE MAPPING:

Category        AWS                  Azure                   GCP
Container Reg   ECR                  Azure Container Reg     Artifact Registry
Kubernetes      EKS                  AKS                     GKE
Serverless      Lambda               Azure Functions         Cloud Run
Object Storage  S3                   Azure Blob Storage      Cloud Storage
Managed DB      RDS                  Azure Database          Cloud SQL
NoSQL           DynamoDB             Cosmos DB               Firestore/Bigtable
Message Queue   SQS                  Azure Service Bus       Pub/Sub
Secret Manager  Secrets Manager      Key Vault               Secret Manager
CDN             CloudFront           Azure CDN/Front Door    Cloud CDN
IaC State       S3 + DynamoDB lock   Azure Blob + lease      GCS + lock
IAM             IAM Roles/Policies   Azure AD + RBAC         Cloud IAM

AZURE CORE CONCEPTS:
  Resource Group:   logical container for related resources (billing, lifecycle)
  Subscription:     billing boundary (separate for dev/staging/prod)
  Service Principal: like IAM Role for apps/CI pipelines
  Managed Identity: like EC2 instance profile (no credentials)
  Workload Identity: K8s SA → Azure AD identity, no secrets

GCP CORE CONCEPTS:
  Project:   basic unit (like an AWS account)
  Workload Identity Federation: K8s SA → GCP Service Account, no key files
  GKE Autopilot: fully managed nodes (you only manage pods)
  Binary Authorization: only signed images deploy (like ECR + cosign)
```

```hcl
# Multi-cloud Terraform:
terraform {
  required_providers {
    aws     = { source = "hashicorp/aws",     version = "~> 5.0" }
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
    google  = { source = "hashicorp/google",  version = "~> 5.0" }
  }
}
provider "aws"     { region = var.aws_region }
provider "azurerm" { features {} }
provider "google"  { project = var.gcp_project }
```

---

**Q120. Ansible — configuration management deep dive.**

```yaml
# ANSIBLE vs TERRAFORM:
# Terraform: WHAT infrastructure exists (declarative, state-driven)
# Ansible:   HOW to configure it (procedural, agentless SSH-based)
# Together:  Terraform provisions → Ansible configures

---
# Dynamic inventory (AWS EC2):
plugin: amazon.aws.aws_ec2
regions: [us-east-1]
filters:
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role

---
# Full production playbook:
- name: Configure Node.js API servers
  hosts: webservers
  become: yes
  vars:
    node_version: "20"
    app_dir: /opt/api
    app_port: 3000
  vars_files:
    - vars/secrets.yml   # ansible-vault encrypted

  tasks:
    - name: Install Node.js
      block:
        - apt_key:
            url: https://deb.nodesource.com/gpgkey/nodesource.gpg.key
        - apt_repository:
            repo: "deb https://deb.nodesource.com/node_{{ node_version }}.x {{ ansible_distribution_release }} main"
        - apt: { name: nodejs, state: present }

    - name: Create app user
      user: { name: appuser, system: yes, shell: /bin/false }

    - name: Deploy app from git
      git:
        repo: https://github.com/myorg/api.git
        dest: "{{ app_dir }}/src"
        version: "{{ app_version | default('main') }}"
      notify: restart api

    - name: Install production dependencies
      npm: { path: "{{ app_dir }}/src", production: yes }

    - name: Configure systemd service
      template:
        src: templates/api.service.j2
        dest: /etc/systemd/system/api.service
      notify: [reload systemd, restart api]

    - name: Ensure api service is running
      systemd: { name: api, state: started, enabled: yes }

  handlers:
    - name: reload systemd
      systemd: { daemon_reload: yes }
    - name: restart api
      systemd: { name: api, state: restarted }

  post_tasks:
    - name: Verify API is healthy
      uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      retries: 10
      delay: 3

# ROLES — reusable composable playbooks:
# ansible-galaxy init roles/nodejs
# Structure: tasks/ handlers/ templates/ vars/ defaults/ meta/

# VAULT — encrypt secrets at rest:
# ansible-vault encrypt vars/secrets.yml
# ansible-playbook site.yml --vault-password-file ~/.vault-pass
```

---

**Q121. Velero — Kubernetes backup and disaster recovery.**

```bash
# VELERO: backup K8s resources + PV data to S3/GCS/Azure Blob

# Install:
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero

# Backup:
velero backup create production-$(date +%Y%m%d) \
  --include-namespaces production \
  --ttl 720h

# Schedule (daily at 2am, keep 30 days):
velero schedule create daily-production \
  --schedule "0 2 * * *" \
  --include-namespaces production \
  --ttl 720h

# Restore:
velero restore create --from-backup production-20240115
velero restore wait production-20240115

# DISASTER RECOVERY RUNBOOK (cluster total loss):
# 1. Provision new cluster (Terraform)
# 2. Install Velero pointing to same S3 bucket (discovers existing backups)
# 3. Restore in order (order matters):

# Step 1 — CRDs first:
velero restore create step1-crds \
  --from-backup full-cluster-20240115 \
  --include-resources customresourcedefinitions
velero restore wait step1-crds

# Step 2 — infra namespaces:
velero restore create step2-infra \
  --from-backup full-cluster-20240115 \
  --include-namespaces cert-manager,external-secrets,monitoring
velero restore wait step2-infra

# Step 3 — applications:
velero restore create step3-apps \
  --from-backup full-cluster-20240115 \
  --include-namespaces production
velero restore wait step3-apps

# 4. kubectl get pods --all-namespaces
# 5. Update DNS to new cluster load balancer

# ETCD BACKUP (self-managed clusters):
ETCDCTL_API=3 etcdctl snapshot save /tmp/etcd-$(date +%Y%m%d).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
```

---

**Q122. Kubernetes admission webhooks — validating and mutating.**

```go
// TWO TYPES:
// MutatingAdmissionWebhook:   can modify the object (inject sidecar, add labels)
// ValidatingAdmissionWebhook: can only approve or reject (policy enforcement)
// ORDER: Mutating → schema validation → Validating

// USE CASES:
// - Enforce resource limits on all pods
// - Validate image comes from approved registry
// - Inject Vault Agent / Istio sidecar
// - Add mandatory labels/annotations

// Validating webhook handler (Go):
func validatePod(w http.ResponseWriter, r *http.Request) {
    var review admissionv1.AdmissionReview
    json.NewDecoder(r.Body).Decode(&review)

    var pod corev1.Pod
    json.Unmarshal(review.Request.Object.Raw, &pod)

    resp := &admissionv1.AdmissionResponse{UID: review.Request.UID}

    for _, c := range pod.Spec.Containers {
        if c.Resources.Requests == nil || c.Resources.Limits == nil {
            resp.Allowed = false
            resp.Result = &metav1.Status{
                Message: fmt.Sprintf(
                    "container %s must have resource requests and limits", c.Name),
            }
            sendResponse(w, review, resp)
            return
        }
    }
    resp.Allowed = true
    sendResponse(w, review, resp)
}
```

```yaml
# Register the webhook:
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: pod-validator
  annotations:
    cert-manager.io/inject-ca-from: webhook-system/webhook-tls
webhooks:
  - name: validate-pods.myorg.io
    admissionReviewVersions: ["v1"]
    sideEffects: None
    failurePolicy: Fail      # reject if webhook unreachable (use Ignore for prod resilience)
    namespaceSelector:
      matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values: [kube-system, kube-public]   # never intercept system namespaces
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods"]
    clientConfig:
      service:
        name: pod-validator
        namespace: webhook-system
        path: /validate-pods
      caBundle: ""   # auto-injected by cert-manager
```

---

**Q123. Packer — immutable infrastructure and custom AMI builds.**

```hcl
# PACKER: build identical machine images for multiple platforms.
# Immutable infra: never modify a running server.
# Build new image → replace instances → delete old.

packer {
  required_plugins {
    amazon = { source = "github.com/hashicorp/amazon", version = ">= 1.2.8" }
  }
}

variable "app_version" { type = string }

source "amazon-ebs" "api" {
  ami_name      = "api-${var.app_version}-${formatdate("YYYYMMDD", timestamp())}"
  instance_type = "t3.medium"
  region        = "us-east-1"

  source_ami_filter {
    filters = {
      name                = "al2023-ami-*-x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["amazon"]
    most_recent = true
  }

  ssh_username = "ec2-user"

  launch_block_device_mappings {
    device_name           = "/dev/xvda"
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name       = "api-${var.app_version}"
    AppVersion = var.app_version
    Builder    = "packer"
  }
}

build {
  sources = ["source.amazon-ebs.api"]

  # Ansible configures the server:
  provisioner "ansible" {
    playbook_file = "ansible/configure-api.yml"
    extra_arguments = ["--extra-vars", "app_version=${var.app_version}"]
  }

  # Clean up before baking:
  provisioner "shell" {
    inline = [
      "sudo rm -rf /tmp/*",
      "sudo rm -f /home/ec2-user/.ssh/authorized_keys",
      "sudo yum clean all",
      "history -c",
    ]
  }

  post-processor "manifest" {
    output = "packer-manifest.json"
  }
}

# Usage: packer build -var app_version=2.1.0 .

# Terraform uses latest Packer AMI:
data "aws_ami" "api" {
  most_recent = true
  owners      = ["self"]
  filter { name = "tag:Builder", values = ["packer"] }
}
```

---

**Q124. Container image optimization — layers, size, build cache.**

```dockerfile
# BASE IMAGE SIZE COMPARISON:
# node:20               ~1.1GB (full Debian)
# node:20-slim          ~245MB (minimal Debian)
# node:20-alpine        ~175MB (Alpine)
# distroless/nodejs20   ~160MB (no shell, no pkg manager)
# scratch               +0MB   (Go/Rust static binaries)

# LAYER CACHING — order least-changing to most-changing:
# BAD (cache broken on every source change):
COPY . .
RUN npm ci

# GOOD:
COPY package*.json ./
RUN npm ci          # cached unless package.json changes
COPY . .            # source code last

# COMBINE RUN to reduce layers AND ensure cleanup is effective:
# BAD (cleanup is a separate layer, doesn't actually save space):
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# GOOD (all in one layer):
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# BUILDKIT CACHE MOUNTS — share npm cache across builds, not in image:
# syntax=docker/dockerfile:1
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# .dockerignore — critical, exclude:
# .git
# node_modules     (image installs fresh)
# .env*            (NEVER copy secrets into image)
# *.log
# coverage / __tests__

# DISTROLESS — maximum security (no shell):
FROM node:20-alpine AS builder
COPY . .
RUN npm ci && npm run build && npm prune --omit=dev

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER nonroot
CMD ["dist/main.js"]
# docker exec ... sh WILL FAIL — by design (no shell to exploit)
```

---

**Q125. k6 load testing — CI/CD integration.**

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate        = new Rate('error_rate');
const checkoutDuration = new Trend('checkout_duration', true);

export const options = {
  stages: [
    { duration: '2m', target: 50  },
    { duration: '5m', target: 50  },
    { duration: '2m', target: 200 },
    { duration: '3m', target: 200 },
    { duration: '2m', target: 0   },
  ],
  // Pipeline FAILS if these are breached:
  thresholds: {
    http_req_failed:   ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    checkout_duration: ['p(99)<2000'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com';

export default function () {
  const res = http.get(`${BASE_URL}/v1/products`,
    { tags: { name: 'GetProducts' } });
  check(res, { 'products 200': (r) => r.status === 200 }) || errorRate.add(1);
  sleep(1);

  const start = Date.now();
  const checkout = http.post(`${BASE_URL}/v1/checkout`,
    JSON.stringify({ cartId: 'cart_123', paymentMethod: 'card' }),
    { headers: { 'Content-Type': 'application/json',
                 'Authorization': `Bearer ${__ENV.AUTH_TOKEN}` },
      timeout: '10s' });
  checkoutDuration.add(Date.now() - start);
  check(checkout, { 'checkout 200': (r) => r.status === 200 }) || errorRate.add(1);
  sleep(1);
}
```

```yaml
# GitHub Actions integration:
- name: Load test
  run: |
    k6 run \
      --env BASE_URL=https://staging-api.example.com \
      --env AUTH_TOKEN=${{ secrets.LOAD_TEST_TOKEN }} \
      load-tests/checkout.js
  # Pipeline fails on threshold breach (k6 exit code 99)
```

---

## QUICK-FIRE Q&A (Q126–Q160)

**Q126. kubectl apply vs kubectl create vs server-side apply.**

```
kubectl create:
  Creates a resource. Fails with AlreadyExists if it exists.
  Imperative — "create this now." No re-run safety.
  Use for: one-off ops (create namespace, Secret once).

kubectl apply:
  Creates OR updates. Idempotent — safe to run repeatedly.
  Declarative — "make the cluster match this state."
  Tracks last-applied-configuration in annotation.
  Use for: everything in automation and GitOps.

kubectl apply --server-side (SSA):
  Apply logic runs on the API server (not client).
  Tracks field ownership — multiple controllers can own different fields.
  Conflicts reported precisely per field.
  Recommended for: ArgoCD, Flux, operators, CI pipelines.

RULE: always use kubectl apply in automation. kubectl create only for
interactive one-off operations.
```

---

**Q127. How to debug CrashLoopBackOff.**

```bash
# CrashLoopBackOff: container crashes, K8s restarts it with exponential backoff.

# Step 1: get exit code:
kubectl describe pod <pod> -n <ns>
# Exit codes: 1=app error, 137=OOMKilled, 139=segfault, 143=SIGTERM unhandled

# Step 2: check PREVIOUS container logs:
kubectl logs <pod> -n <ns> --previous   # crashed container logs

# Step 3: if crash too fast — override CMD to keep alive:
kubectl run debug --image=myapp:latest --command -- sleep infinity
kubectl exec -it debug -- sh
# Manually run app command to see error

# Step 4: OOMKilled → increase memory limit or fix memory leak:
kubectl top pod <pod> -n <ns>

# Common causes:
# Missing env var          → app panics on startup
# Missing secret/volume    → file not found
# Wrong CMD/ENTRYPOINT     → binary not found
# readOnlyRootFilesystem   → app tries to write → add emptyDir volume
# Liveness too aggressive  → add startupProbe to protect slow starts
```

---

**Q128. Rolling update in detail.**

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # allow 2 extra pods during update (12 total max)
      maxUnavailable: 0  # never drop below 10 → zero downtime

# PROCESS (10 replicas, maxSurge:2, maxUnavailable:0):
# 1. Create 2 new (v2) pods → 12 total
# 2. Wait for 2 new pods to pass readinessProbe
# 3. Delete 2 old pods → 10 total
# 4. Repeat until all 10 are v2

# ZERO-DOWNTIME REQUIREMENTS:
# 1. Correct readinessProbe (pod Ready only when truly able to serve)
# 2. maxUnavailable: 0
# 3. preStop hook to drain in-flight requests:
  lifecycle:
    preStop:
      exec:
        command: ["sleep", "15"]
# 4. Graceful SIGTERM handling in app
# 5. terminationGracePeriodSeconds: 30

# ROLLBACK:
# kubectl rollout undo deploy/api
# kubectl rollout undo deploy/api --to-revision=3
# kubectl rollout history deploy/api
# kubectl rollout status deploy/api
```

---

**Q129. Terraform workspaces vs separate directories.**

```hcl
# WORKSPACES — separate state files, same config:
terraform workspace new staging
terraform workspace select staging
terraform apply

# Access in config:
resource "aws_instance" "api" {
  instance_type = terraform.workspace == "production" ? "t3.xlarge" : "t3.small"
}

# Workspaces GOOD FOR: simple env differences, quick experiments.
# Workspaces BAD FOR: different cloud accounts per env, large teams
#   (easy to apply to wrong workspace), different backends per env.

# RECOMMENDED: separate directories per environment:
# infra/environments/
#   staging/
#     main.tf       # calls shared modules
#     backend.tf    # separate S3 key
#     terraform.tfvars
#   production/
#     main.tf
#     backend.tf    # different S3 key
#     terraform.tfvars
# infra/modules/
#   vpc/ eks/ rds/

# Benefits of separate dirs:
# - Separate blast radius (staging apply CANNOT touch production state)
# - Different config per env (prod has WAF, staging doesn't)
# - CI: PR to staging dir → plan staging; merge main → prod pipeline
```

---

**Q130. GitOps — what it is, how it works, ArgoCD vs Flux.**

```
TRADITIONAL CI/CD (push model):
  CI has write credentials to the cluster.
  CI deploys on every merge.
  Drift: someone kubectl applies manually → cluster diverges from git.
  No audit trail for manual changes.

GITOPS (pull model):
  Git repo = single source of truth for desired cluster state.
  An operator (ArgoCD/Flux) inside the cluster pulls from git.
  No external system has cluster write credentials.

GITOPS PROPERTIES:
  1. Declarative:  all desired state in git (YAML, Helm, Kustomize)
  2. Versioned:    every change is a git commit (audit trail)
  3. Pull-based:   operator continuously syncs cluster to git
  4. Reconciled:   drift detected and corrected automatically

GITOPS FLOW:
  PR merged → ArgoCD detects git change → compares git vs cluster
  → applies diff → reports sync status in ArgoCD UI + git commit status

BENEFITS:
  - Rollback: git revert → cluster reverts in <1 minute
  - Disaster recovery: point ArgoCD at git → cluster rebuilt
  - Audit: every cluster change has a git commit (who, what, when, why)
  - Security: cluster credentials never leave the cluster

ARGOCD vs FLUX:
  ArgoCD: Web UI, ApplicationSets, multi-cluster RBAC. Widely used.
  Flux:   CLI-focused, native Helm OCI support, lighter. CNCF graduated.
  Both:   production-ready. Choice is team preference.
```

---

**Q131. DNS resolution inside Kubernetes.**

```
KUBERNETES DNS (CoreDNS):
  All pods: /etc/resolv.conf points to CoreDNS (kube-system).

FULL FQDN:
  <service>.<namespace>.svc.cluster.local

EXAMPLES:
  Service "api" in "production":
    Full:  api.production.svc.cluster.local
    Short: api (within same namespace — search domain handles it)

  StatefulSet pod "redis-0":
    redis-0.redis-headless.production.svc.cluster.local

SEARCH DOMAINS (/etc/resolv.conf in a pod in "production" ns):
  search production.svc.cluster.local svc.cluster.local cluster.local
  "api" → tries api.production.svc.cluster.local first → found!

DEBUGGING DNS:
  kubectl run dns-debug --image=busybox:1.28 --rm -it --restart=Never -- sh
  nslookup api.production.svc.cluster.local
  cat /etc/resolv.conf
  kubectl logs -n kube-system -l k8s-app=kube-dns

CUSTOM DNS (route .example.com externally in CoreDNS ConfigMap):
  example.com:53 {
    forward . 8.8.8.8 8.8.4.4
  }
```

---

**Q132. Taints and tolerations.**

```yaml
# TAINT: mark a node to REPEL pods (unless pod tolerates it)
# TOLERATION: allow a pod to be scheduled on a tainted node

# Taint a node:
# kubectl taint nodes gpu-node-1 gpu=true:NoSchedule
# Effect types:
# NoSchedule:       don't schedule new pods (existing stay)
# PreferNoSchedule: soft constraint
# NoExecute:        evict existing + don't schedule new

# Pod toleration:
spec:
  tolerations:
    - key: gpu
      operator: Equal
      value: "true"
      effect: NoSchedule

    # Spot node: tolerate eviction, finish in-flight work within 120s:
    - key: spot
      operator: Equal
      value: "true"
      effect: NoExecute
      tolerationSeconds: 120

    # Wildcard — tolerate any taint:
    - operator: Exists

# BUILT-IN TAINTS (auto-added by K8s):
# node.kubernetes.io/not-ready
# node.kubernetes.io/unreachable
# node.kubernetes.io/memory-pressure
# node.kubernetes.io/disk-pressure
# Critical DaemonSets tolerate these automatically.

# TAINT vs NODE SELECTOR vs AFFINITY:
# nodeSelector:     hard key=value match
# nodeAffinity:     flexible expressions (in, notIn, exists)
# taints+tolerations: repel-based (node rejects unless tolerated)
# Combine all three for dedicated node pools with mutual exclusivity.
```

---

**Q133. NetworkPolicy — deny all by default.**

```yaml
# Without NetworkPolicy: all pods communicate freely.
# NetworkPolicy requires a policy-aware CNI (Calico, Cilium — NOT Flannel).

# STEP 1: deny ALL ingress + egress:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}       # all pods
  policyTypes: [Ingress, Egress]
  # no rules = deny all

---
# STEP 2: allow API to receive from ingress-nginx:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-api
  namespace: production
spec:
  podSelector:
    matchLabels: { app: api }
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000

---
# STEP 3: allow API egress to postgres + DNS:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-egress
  namespace: production
spec:
  podSelector:
    matchLabels: { app: api }
  policyTypes: [Egress]
  egress:
    - to:
        - podSelector:
            matchLabels: { app: postgres }
      ports:
        - protocol: TCP
          port: 5432
    # DNS — ALWAYS required or all DNS lookups fail:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels: { k8s-app: kube-dns }
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

---

**Q134. ConfigMap and Secret best practices — External Secrets Operator.**

```yaml
# CONFIGMAP — non-sensitive config:
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: production
data:
  APP_PORT: "3000"
  LOG_LEVEL: "info"
  nginx.conf: |
    server { listen 80; location / { proxy_pass http://api:3000; } }

# HOT RELOAD: volume-mounted ConfigMaps update in ~1min.
# Env vars: require pod restart.

---
# EXTERNAL SECRETS OPERATOR — sync from AWS Secrets Manager → K8s Secret:
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: api-secrets
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/api
        property: db_password
    - secretKey: API_KEY
      remoteRef:
        key: production/api
        property: api_key
---
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secretsmanager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets

# BEST PRACTICES:
# Never commit secrets to git (base64 is NOT encryption)
# Use ESO + Vault/AWS SM for production
# Enable etcd encryption at rest
# RBAC: restrict who can list/watch Secrets (list exposes all values)
# Rotate secrets via Vault — ESO re-syncs automatically
```

---

**Q135. Liveness, readiness, and startup probes.**

```yaml
spec:
  containers:
    - name: api

      # STARTUP PROBE — "has the app finished starting?"
      # While failing: liveness probe is DISABLED (protects slow starters).
      startupProbe:
        httpGet: { path: /health/startup, port: 3000 }
        failureThreshold: 30    # 30 × 10s = 5 min allowed for startup
        periodSeconds: 10

      # LIVENESS PROBE — "should this pod be restarted?"
      # Fails: pod KILLED and restarted.
      # NEVER check external deps (DB down → don't restart all pods!)
      livenessProbe:
        httpGet: { path: /health/live, port: 3000 }
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3

      # READINESS PROBE — "should this pod receive traffic?"
      # Fails: pod REMOVED from Service endpoints. NOT restarted.
      # CAN check dependencies (DB, cache).
      readinessProbe:
        httpGet: { path: /health/ready, port: 3000 }
        periodSeconds: 5
        timeoutSeconds: 3
        failureThreshold: 3

# HEALTH ENDPOINT DESIGN:
# /health/live:    200 if process alive. Never check external deps.
# /health/ready:   200 if ready to serve. CAN check DB connection.
# /health/startup: 200 once startup complete (migrations done, cache warm).

# PROBE TYPES:
# httpGet:   HTTP GET → 2xx/3xx = success
# tcpSocket: TCP connection → accepted = success
# exec:      run command → exit 0 = success
# grpc:      gRPC health check (K8s 1.23+)

# COMMON MISTAKE: using same endpoint for liveness and readiness.
# Readiness SHOULD fail temporarily (DB restart = pull from rotation).
# Liveness should ONLY fail for truly unrecoverable internal state.
```

---

**Q136. Init containers and sidecar containers.**

```yaml
spec:
  # INIT CONTAINERS — run sequentially before main containers start:
  initContainers:
    - name: wait-for-postgres
      image: busybox
      command: ['sh', '-c',
        'until nc -z postgres.production 5432; do sleep 2; done']

    - name: run-migrations
      image: myapp:2.1.0
      command: ['node', 'dist/migrate.js']
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef: { name: api-secrets, key: DATABASE_URL }

  # NATIVE SIDECAR (K8s 1.29+): restartPolicy: Always in initContainers:
  initContainers:
    - name: log-shipper
      image: fluent/fluent-bit:2.2
      restartPolicy: Always    # makes it a sidecar: starts before main, outlives it
      volumeMounts:
        - name: logs
          mountPath: /var/log/app

  containers:
    - name: api
      image: myapp:2.1.0
      volumeMounts:
        - name: logs
          mountPath: /app/logs
  volumes:
    - name: logs
      emptyDir: {}

# INIT vs SIDECAR:
# Init:    runs to completion before main, sequential order
# Sidecar: concurrent with main, same pod lifecycle
# Init use: migrations, dependency checks, secret fetching, config setup
# Sidecar use: log shipping, service mesh proxy, git-sync, Vault Agent
```

---

**Q137. Helm vs Kustomize — when to use which.**

```
HELM — templating + package manager:
  Use for: 3rd party software (nginx-ingress, cert-manager, prometheus),
           packaging internal apps as versioned charts,
           template logic (loops, conditionals, functions).

KUSTOMIZE — overlay system (built into kubectl):
  Use for: plain YAML (no templating language),
           simple env differences (replica count, image tag),
           GitOps with ArgoCD/Flux (both support natively).
```

```yaml
# KUSTOMIZE STRUCTURE:
# base/deployment.yaml + base/kustomization.yaml
# overlays/production/kustomization.yaml:
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases: [../../base]
namespace: production
images:
  - name: myapp
    newTag: 2.1.0
patchesStrategicMerge:
  - resource-limits.yaml

# overlays/production/resource-limits.yaml:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: api
          resources:
            requests: { cpu: 500m, memory: 512Mi }
            limits: { cpu: 2000m, memory: 1Gi }

# Apply: kubectl apply -k overlays/production/
# ArgoCD uses this natively — just point to the overlay directory.
```

---

**Q138. Blue-green and canary deployments.**

```
BLUE-GREEN:
  Two identical environments: Blue (current), Green (new).
  All traffic → Blue. Deploy + test Green.
  Flip LB selector → all traffic → Green. Blue = standby (instant rollback).
  Pros: instant rollback, zero-downtime cutover.
  Cons: double resources, DB migrations must be backward compatible.

CANARY:
  Gradually shift traffic: 5% → 25% → 50% → 100%.
  Monitor error rate + latency at each step. Auto-rollback on degradation.
  Pros: limit blast radius, real production traffic validates new version.
  Cons: multiple versions live, complex without service mesh.
```

```yaml
# BLUE-GREEN — flip Service selector:
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
    version: blue    # change to "green" to flip all traffic instantly

# Switch: kubectl patch service api -p '{"spec":{"selector":{"version":"green"}}}'
# Rollback: kubectl patch service api -p '{"spec":{"selector":{"version":"blue"}}}'

---
# CANARY with Argo Rollouts (auto metrics-based progression):
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  strategy:
    canary:
      canaryService: api-canary
      stableService: api-stable
      steps:
        - setWeight: 5
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 25
        - pause: { duration: 10m }
        - setWeight: 100
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: "result[0] >= 0.99"
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{status!~"5..",service="api-canary"}[5m]))
            / sum(rate(http_requests_total{service="api-canary"}[5m]))
```

---

**Q139. GitHub Actions — matrix builds, reusable workflows, environments.**

```yaml
# MATRIX BUILD:
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, windows-latest]
        exclude:
          - node: 18
            os: windows-latest
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: ${{ matrix.node }} }
      - run: npm ci && npm test

---
# REUSABLE WORKFLOW:
# .github/workflows/reusable-deploy.yml:
on:
  workflow_call:
    inputs:
      environment: { type: string, required: true }
      image-tag: { type: string, required: true }
    secrets:
      KUBE_CONFIG: { required: true }
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > ~/.kube/config
          helm upgrade --install api ./charts/api \
            --namespace ${{ inputs.environment }} \
            --set image.tag=${{ inputs.image-tag }} \
            --atomic --timeout 5m

# Caller:
jobs:
  deploy-staging:
    uses: myorg/infra/.github/workflows/reusable-deploy.yml@main
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
    secrets:
      KUBE_CONFIG: ${{ secrets.STAGING_KUBE_CONFIG }}

---
# CONCURRENCY — cancel outdated runs on new push:
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true

---
# ENVIRONMENTS + APPROVALS:
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://api.example.com
    # GitHub Settings → Environments → production → Required reviewers
    # Pipeline pauses until a reviewer clicks Approve in GitHub UI.

---
# CACHING:
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: npm-

---
# DYNAMIC OUTPUTS BETWEEN JOBS:
jobs:
  build:
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/myorg/api
          tags: type=sha,prefix=sha-
  deploy:
    needs: build
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.image-tag }}"
```

---

**Q140. Kubernetes API request flow — kubectl apply to pod running.**

```
FULL FLOW: kubectl apply -f pod.yaml → pod running

1. kubectl
   Reads ~/.kube/config → API server + credentials
   Serializes Pod → JSON
   HTTPS POST to /api/v1/namespaces/production/pods

2. API Server — Authentication
   Validates client cert / bearer token / OIDC JWT
   Identifies: WHO is making this request?

3. API Server — Authorization (RBAC)
   Can this user CREATE pods in this namespace?

4. API Server — Admission Control
   MutatingAdmissionWebhooks: modify object (inject sidecar, add labels)
   Schema validation: object matches API schema?
   ValidatingAdmissionWebhooks: approve or reject (policy enforcement)

5. API Server — Persist to etcd
   Stores object → returns 201 Created to kubectl

6. Scheduler (watching for pods with nodeName=""):
   Filtering: which nodes CAN run it? (resources, affinity, taints)
   Scoring: which is BEST? (least allocated, spread, affinity weight)
   Binds pod: sets pod.spec.nodeName

7. kubelet on target node (watching API for its pods):
   Pulls image via containerd
   Creates container (containerd → runc → namespaces + cgroups)
   Starts probes (startup → readiness → liveness)
   Reports status: Running, containerID, startTime

8. kube-proxy / Cilium:
   When pod passes readinessProbe → updates Service endpoint rules
   Traffic can now reach the new pod

9. Controller Manager:
   ReplicaSet controller watches: if pod dies → creates replacement

TOTAL TIME: typically 5–30 seconds (image pull is the main bottleneck)
```

---

**Q141. AWS IAM — IRSA and least privilege for EKS.**

```bash
# IRSA (IAM Roles for Service Accounts):
# WITHOUT: pods share the EC2 node's IAM role (all pods = same permissions!)
# WITH:    each K8s ServiceAccount has its own IAM Role (least privilege)

# 1. Create IAM Role with trust for a specific ServiceAccount:
aws iam create-role \
  --role-name api-s3-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED:sub":
            "system:serviceaccount:production:api-sa"
        }
      }
    }]
  }'

# 2. Attach permissions policy:
aws iam attach-role-policy \
  --role-name api-s3-role \
  --policy-arn arn:aws:iam::123456:policy/api-s3-policy

# 3. Annotate Kubernetes ServiceAccount:
kubectl annotate serviceaccount api-sa \
  -n production \
  eks.amazonaws.com/role-arn=arn:aws:iam::123456:role/api-s3-role

# Pod uses this SA → gets auto-injected AWS credentials via projected volume.
# AWS SDK picks them up automatically. No hardcoded credentials anywhere!
```

```hcl
# Terraform IRSA module:
module "irsa_api" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  role_name = "api-s3-access"
  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["production:api-sa"]
    }
  }
  role_policy_arns = { s3 = aws_iam_policy.api_s3.arn }
}

# IAM SECURITY BEST PRACTICES:
# 1. Never use root account (enable MFA, no access keys for root)
# 2. No long-lived access keys for apps (use roles, IRSA)
# 3. Least privilege: deny-all by default, add only needed permissions
# 4. SCPs: org-level guardrails even admins can't override
# 5. CloudTrail: log all API calls (who, what, when, from where)
# 6. IAM Access Analyzer: detect externally accessible resources
# 7. Access Advisor: see which permissions are actually used → remove unused
```

---

**Q142. SLSA, Sigstore, and supply chain security.**

```
SLSA (Supply-chain Levels for Software Artifacts):
  Framework of requirements for build pipeline security.

  SLSA 1: provenance exists (build documented, provenance generated)
  SLSA 2: tamper protection (CI-hosted build, provenance signed by CI)
  SLSA 3: hardened builds (isolated ephemeral env, source with code review)
  SLSA 4: max protection (two-person review, hermetic + reproducible builds)

SIGSTORE / COSIGN — image signing:
  Sign images with your identity (OIDC/GitHub Actions, keyless).
  Verify signatures before deployment.
  Rekor: append-only transparency log of all signatures.
```

```bash
# Sign image (keyless, uses GitHub Actions OIDC):
- name: Sign image
  run: |
    cosign sign --yes \
      --oidc-issuer=https://token.actions.githubusercontent.com \
      ghcr.io/myorg/api@${IMAGE_DIGEST}
  env:
    COSIGN_EXPERIMENTAL: "1"

# Verify before deploy:
cosign verify \
  --certificate-identity-regexp="https://github.com/myorg/api/.github/workflows/.*" \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  ghcr.io/myorg/api:2.1.0

# Generate SBOM (Software Bill of Materials):
syft ghcr.io/myorg/api:2.1.0 -o spdx-json > sbom.json
cosign attach sbom --sbom sbom.json ghcr.io/myorg/api:2.1.0
```

```yaml
# Kyverno policy — only allow signed images:
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-signed-images
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-signature
      match:
        any:
          - resources: { kinds: [Pod] }
      verifyImages:
        - imageReferences: ["ghcr.io/myorg/*"]
          attestors:
            - count: 1
              entries:
                - keyless:
                    subject: "https://github.com/myorg/*"
                    issuer: "https://token.actions.githubusercontent.com"
```

---

**Q143. CI/CD security scanning — SAST, DAST, container scanning, SCA.**

```yaml
# SAST (Static Application Security Testing) — scan source code:
- name: Semgrep SAST
  uses: semgrep/semgrep-action@v1
  with:
    config: p/typescript p/owasp-top-ten p/security-audit

- name: CodeQL (GitHub native, free for open source)
  uses: github/codeql-action/init@v3
  with: { languages: javascript }
- uses: github/codeql-action/analyze@v3

---
# SCA (Software Composition Analysis) — scan dependencies for CVEs:
- name: Snyk dependency scan
  uses: snyk/actions/node@master
  env: { SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }} }
  with: { args: --severity-threshold=high }

- name: Trivy filesystem scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    severity: CRITICAL,HIGH
    exit-code: 1

---
# CONTAINER IMAGE SCANNING:
- name: Trivy image scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
    format: sarif
    output: trivy-results.sarif

- name: Upload to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v3
  with: { sarif_file: trivy-results.sarif }

---
# SECRET SCANNING — prevent secrets committed to git:
- name: TruffleHog
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    head: HEAD
    extra_args: --only-verified

- name: GitLeaks
  uses: gitleaks/gitleaks-action@v2
  env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

---
# DAST (Dynamic Application Security Testing) — test running app:
- name: OWASP ZAP API scan
  uses: zaproxy/action-api-scan@v0.6.0
  with:
    target: https://staging-api.example.com/openapi.json
    fail_action: true
```

---

**Q144. Cost optimization — Kubernetes and cloud.**

```yaml
# 1. RIGHT-SIZING (biggest win: often 40-60% savings):
# Goldilocks uses VPA to recommend correct requests/limits:
# helm install goldilocks fairwinds-stable/goldilocks -n goldilocks
# kubectl label namespace production goldilocks.fairwinds.com/enabled=true
# View dashboard → shows per-workload resource recommendations

---
# 2. SPOT INSTANCES — 60-90% savings for interruptible workloads:
# Karpenter NodePool: spot-first, fall back to on-demand:
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: batch-workers
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
  disruption:
    consolidationPolicy: WhenUnderutilized

---
# 3. NAMESPACE RESOURCE QUOTAS — prevent runaway costs:
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-team-quota
  namespace: dev-team-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    count/pods: "50"
    requests.storage: 100Gi
```

```bash
# 4. SCALE TO ZERO off-hours (dev/staging):
kubectl scale deploy --all -n staging --replicas=0
# Or kube-downscaler:
# helm install kube-downscaler ... (auto-scales down nights + weekends)

# 5. S3 LIFECYCLE POLICY — move to cheaper storage tiers:
aws s3api put-bucket-lifecycle-configuration \
  --bucket mybucket \
  --lifecycle-configuration '{
    "Rules": [{
      "Status": "Enabled",
      "Transitions": [
        {"Days": 30,  "StorageClass": "STANDARD_IA"},
        {"Days": 90,  "StorageClass": "GLACIER"},
        {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
      ]
    }]
  }'

# 6. Find unused EBS volumes (not attached to any instance):
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].[VolumeId,Size,CreateTime]'
# "available" = not attached → delete or snapshot
```

---

**Q145. Chaos engineering — principles, Chaos Mesh, game days.**

```
CHAOS ENGINEERING: inject failures intentionally to discover weaknesses
before unplanned outages find them first.

PRINCIPLES:
  1. Define steady state (what does healthy look like quantitatively?)
  2. Vary real-world events (kill pods, add latency, fill disk)
  3. Run in production (or production-like)
  4. Automate experiments (run continuously)
  5. Minimize blast radius (start small, have kill switches)

STEADY STATE HYPOTHESIS:
  Define: error rate < 0.1%, P99 < 500ms.
  Inject failure → verify hypothesis still holds → system is resilient.
  Hypothesis fails → real weakness found → fix it.
```

```yaml
# Chaos Mesh — Kubernetes-native chaos:

# Kill 25% of API pods randomly every 10 minutes:
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: api-pod-kill
  namespace: production
spec:
  action: pod-kill
  mode: random-max-percent
  value: "25"
  selector:
    namespaces: [production]
    labelSelectors: { app: api }
  scheduler:
    cron: "@every 10m"

---
# Add 500ms latency between API and database:
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: api-db-latency
  namespace: production
spec:
  action: delay
  mode: all
  selector:
    namespaces: [production]
    labelSelectors: { app: api }
  delay:
    latency: "500ms"
    jitter: "50ms"
  direction: to
  target:
    mode: all
    selector:
      namespaces: [production]
      labelSelectors: { app: postgres }
  duration: "5m"
```

```
GAME DAY — structured chaos experiment:
  1. Define objectives (what do we want to learn?)
  2. Set up monitoring dashboards
  3. Announce to team (everyone watching)
  4. Run experiment with kill switch ready
  5. Document findings
  6. Prioritize fixes
  7. Automate experiment to run regularly
```

---

**Q146. Feature flags — implementation and best practices.**

```javascript
// FEATURE FLAGS: decouple deployment from release.
// Deploy code (flag off) → test → flip flag → release to users.
// Benefits: instant rollback, targeted rollout, A/B testing.

// OpenFeature SDK (vendor-neutral standard):
import { OpenFeature } from "@openfeature/sdk";
import { LaunchDarklyProvider } from "@openfeature/launchdarkly-provider";

await OpenFeature.setProviderAndWait(
  new LaunchDarklyProvider(process.env.LD_SDK_KEY!)
);
const client = OpenFeature.getClient();

async function processCheckout(order: Order, user: User) {
  const ctx = {
    targetingKey: user.id,
    plan: user.plan,
    country: user.country,
    betaUser: user.isBetaTester,
  };

  // Boolean flag — is new checkout enabled for this user?
  const useNew = await client.getBooleanValue("new-checkout-flow", false, ctx);
  if (useNew) return newCheckoutService.process(order);
  return legacyCheckoutService.process(order);
}

// String flag for A/B test:
const variant = await client.getStringValue("checkout-ab-test", "control", ctx);
// Returns "control" | "variant-a" | "variant-b"
// LD assigns same user to same variant consistently.

// JSON flag for complex config:
const rateLimitConfig = await client.getObjectValue(
  "rate-limit-config",
  { requestsPerMinute: 100 },
  ctx
);
```

```yaml
# Targeting rules in LaunchDarkly (via UI or API):
# Flag: new-checkout-flow
# Rules:
#   1. If user.betaUser = true → serve true
#   2. If user.plan = enterprise → serve true
#   3. If user.country IN [EG, SA] → serve 20% true (gradual rollout)
#   4. Default: false

# ConfigMap-based flags (simple, in-cluster, requires restart to update):
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
  namespace: production
data:
  NEW_CHECKOUT: "true"
  NEW_RECOMMENDATION_ENGINE: "false"
```

---

**Q147. Continuous Profiling.**

```
CONTINUOUS PROFILING: collect CPU/memory profiles in production 24/7
at very low overhead (1-3%).

VS TRADITIONAL PROFILING:
  Traditional: run profiler for hours in dev → findings don't match prod.
  Continuous:  always-on in prod → real production hot paths visible.

WHAT IT TELLS YOU:
  - Which functions consume the most CPU? (hot paths to optimize)
  - Where is memory being allocated? (GC pressure sources)
  - Which goroutines/threads are blocked? (lock contention)
  - Where does latency come from? (I/O vs compute vs memory)

TOOLS:
  Pyroscope (open-source, Grafana Labs):
    Agents for Go, Python, Java, Ruby, Node.js, eBPF.
    Flame graph UI, diff between time periods.

  Parca (open-source):
    eBPF-based (no code changes), Go/Java agents.

  CORRELATION:
    Grafana dashboard: Loki logs + Tempo traces + Pyroscope profiles.
    "We see slow traces in Tempo → jump to Pyroscope to see CPU hot spots at that time."
```

```javascript
// Pyroscope Node.js integration:
import Pyroscope from '@pyroscope/nodejs';

Pyroscope.init({
  serverAddress: 'http://pyroscope:4040',
  appName: 'api',
  tags: {
    version: process.env.APP_VERSION,
    environment: process.env.NODE_ENV,
  },
});
Pyroscope.start();
```

---

**Q148. Artifact management — Nexus, Artifactory.**

```
WHY ARTIFACT MANAGEMENT?
  Problem: CI pulls from internet on every build.
    - Reproducibility: packages can disappear from public registries.
    - Security: supply chain attacks via malicious packages.
    - Speed: re-downloading same packages on every run.
    - Compliance: need inventory of all packages in production.

  Solution: proxy all external registries through internal artifact manager.

ARTIFACTORY (JFrog):
  Formats: Docker, Maven, npm, PyPI, Helm, NuGet, Go modules, apt, yum.
  Remote repos: proxy external (npmjs, DockerHub, Maven Central).
  Local repos: store your own artifacts.
  Virtual repos: unified view of local + remote.
  Xray: dependency vulnerability scanning (CVEs).
  Best for: enterprise, all artifact types in one platform.

NEXUS (Sonatype OSS — free):
  Formats: Docker, Maven, npm, PyPI, Helm, apt, yum, raw.
  Nexus IQ: vulnerability scanning (paid).
  Best for: budget-conscious, primarily JVM + Docker.

HARBOR (CNCF, container images only):
  Built-in: Trivy scanning, RBAC, cosign signing, replication.
  Best for: organizations that primarily need a Docker registry.
```

```bash
# Proxy npm through Artifactory (.npmrc):
# registry=https://artifactory.mycompany.com/artifactory/api/npm/npm-virtual/
# All npm install now goes through Artifactory → cached internally

# Artifact PROMOTION pattern (never rebuild for promotions):
# Dev:     artifactory/docker-dev/api:sha-abc123
# Staging: promote (copy, not rebuild):
jfrog rt docker-promote api:sha-abc123 docker-dev docker-staging --copy=true
# Prod:    promote from staging:
jfrog rt docker-promote api:sha-abc123 docker-staging docker-prod --copy=true
# SAME artifact goes through all environments — no "it works in staging" surprises
```

---

**Q149. Kubernetes operators — pattern and implementation.**

```
OPERATOR PATTERN:
  A Kubernetes controller that manages custom resources (CRDs).
  Encodes operational knowledge (how to run complex apps) in code.

  Examples:
    postgres-operator: manages PostgreSQL clusters as CRDs
    prometheus-operator: manages Prometheus via ServiceMonitor CRDs
    cert-manager: manages TLS certs as Certificate CRDs

CONTROL LOOP:
  1. Watch: subscribe to events for your CRD
  2. Observe: get desired state (CRD spec) vs actual state (cluster)
  3. Act: create/update/delete resources to reconcile
  4. Update status: write results to CRD status subresource
  5. Repeat: triggered by any change or every N seconds (reconciliation)
```

```go
// Reconcile function (controller-runtime):
func (r *WebAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    webapp := &appsv1alpha1.WebApp{}
    if err := r.Get(ctx, req.NamespacedName, webapp); err != nil {
        if errors.IsNotFound(err) {
            return ctrl.Result{}, nil  // deleted, nothing to do
        }
        return ctrl.Result{}, err
    }

    // Ensure Deployment exists with correct spec:
    deployment := &appsv1.Deployment{}
    err := r.Get(ctx, req.NamespacedName, deployment)
    if errors.IsNotFound(err) {
        dep := r.buildDeployment(webapp)
        return ctrl.Result{Requeue: true}, r.Create(ctx, dep)
    }

    // Sync replica count:
    if *deployment.Spec.Replicas != webapp.Spec.Replicas {
        deployment.Spec.Replicas = &webapp.Spec.Replicas
        r.Update(ctx, deployment)
    }

    // Update status:
    webapp.Status.AvailableReplicas = deployment.Status.AvailableReplicas
    r.Status().Update(ctx, webapp)

    // Requeue after 30s to detect drift:
    return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
}

// Watch primary CRD + owned resources:
func (r *WebAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&appsv1alpha1.WebApp{}).
        Owns(&appsv1.Deployment{}).
        Owns(&corev1.Service{}).
        Complete(r)
}
```

---

**Q150. Quick-fire: Serverless beyond Lambda — Fargate and Cloud Run.**

```
FARGATE (AWS) — containers without managing EC2 nodes:
  ECS on Fargate: tasks run on Fargate micro-VMs (no EC2 to manage).
  EKS on Fargate: pods scheduled on Fargate (no node groups to manage).

  How: each pod gets its own micro-VM (hardware isolation).
  Billing: per vCPU-second + GB-second (no idle node cost).
  Startup: 30-120 seconds (slower than pre-warmed EC2).

  Fargate on EKS constraints:
  - No DaemonSets (no node-level components)
  - No privileged containers
  - No hostPath volumes
  - Storage: only emptyDir and EFS (no EBS)
  - Each pod = one Fargate node (no bin-packing)

  Use Fargate when:
  - Batch jobs (no idle nodes between runs)
  - Sporadic workloads (scale to zero between jobs)
  - Multi-tenant isolation required
  - Eliminate node management entirely

CLOUD RUN (GCP) — fully managed serverless containers:
  No Kubernetes knowledge needed.
  Scales 0 → N instances in seconds on request.
  Billed only while handling requests (true per-request billing).
  min-instances: 1 keeps one warm (eliminates cold starts).
  concurrency: 80 means 80 simultaneous requests per instance.

COLD START MITIGATION:
  Lambda:    provisioned concurrency (pre-warm N instances)
  Cloud Run: min-instances > 0
  Fargate:   pre-scale before expected traffic spike
  Knative:   minScale > 0 annotation

KNATIVE — Cloud Run features on your own K8s cluster:
  Serving: stateless containers, scale to zero, traffic splitting.
  Eventing: CloudEvents-based event-driven architecture.
  Use when: want Cloud Run on-prem, or OpenShift Serverless.
```

---

*End of DevOps Interview Questions & Answers — Complete Premium Reference*

*Total: 150 questions fully answered with production-quality code.*

*Sections: Docker (Q1–Q30), Kubernetes Core (Q31–Q70), kubectl (Q71–Q95),*
*CI/CD (Q96–Q115), IaC (Q116–Q130), Cloud/AWS (Q131–Q143),*
*Observability (Q144–Q157), Security & Supply Chain (Q158–Q165),*
*Gap-fill additions (Q109–Q150): EXPOSE vs -p, Istio, Prometheus Operator,*
*Gateway API, Terraform testing, Tracing, eBPF, PSS, Helm advanced,*
*GitOps advanced, Multi-cloud, Ansible, Velero, Admission webhooks, Packer,*
*Image optimization, k6, Blue-green/canary, GitHub Actions advanced,*
*API request flow, IRSA, SLSA/Sigstore, Security scanning, Cost optimization,*
*Chaos engineering, Feature flags, Continuous profiling, Artifact management,*
*Operators, Serverless/Fargate/Cloud Run.*
