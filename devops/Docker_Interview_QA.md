# Docker — Interview Questions & Answers (Premium Reference)
> 80 questions. Full answers with code. Architecture, images, Dockerfile, networking, volumes, Compose, security, performance. No stubs.

---

## Table of Contents
- [Section 1: Architecture & Fundamentals (Q1–Q20)](#section-1-architecture--fundamentals)
- [Section 2: Images & Dockerfile (Q21–Q40)](#section-2-images--dockerfile)
- [Section 3: Networking & Volumes (Q41–Q55)](#section-3-networking--volumes)
- [Section 4: Compose, Registry & Security (Q56–Q70)](#section-4-compose-registry--security)
- [Section 5: Performance & Production (Q71–Q80)](#section-5-performance--production)

---

## SECTION 1: ARCHITECTURE & FUNDAMENTALS

---

**Q1. What is Docker and how does it differ from a virtual machine?**

```
DOCKER (CONTAINERS):
  Packages app + dependencies into a container image.
  Container = isolated process running on the host OS kernel.
  Isolation via Linux kernel features:
    Namespaces: PID, NET, MNT, UTS, IPC, USER, CGROUP
    cgroups: CPU, memory, disk I/O, pids limits
    OverlayFS: union filesystem for layered images
  Startup: milliseconds (just a process fork)
  Size: MB (shares host kernel, includes only app + libs)
  Density: 100s per host

VIRTUAL MACHINES:
  Full OS emulation via hypervisor (VMware, KVM, Hyper-V).
  Each VM has its own OS kernel.
  Startup: minutes (full OS boot)
  Size: GB (entire OS + kernel)
  Density: 10–20 per host

KEY INSIGHT: Containers share the host OS kernel.
  Advantage: speed and density.
  Limitation: all containers must be compatible with the host kernel.
  WSL2 / VMs bridge this for Windows/macOS.

USE VMs OVER CONTAINERS WHEN:
  - Hard kernel-level isolation required
  - Non-Linux workloads
  - Different kernel versions needed
  - Legacy apps that can't be containerized
```

---

**Q2. Explain the Docker architecture — daemon, containerd, runc.**

```
LAYERS:
  CLI ──REST──▶ dockerd ──gRPC──▶ containerd ──▶ runc ──▶ container process

docker CLI:
  User-facing tool. Translates commands to REST API calls.

dockerd (Docker daemon):
  Exposes the Docker API (Unix socket: /var/run/docker.sock).
  Manages: images, networks, volumes, API.
  Talks to containerd for container lifecycle.

containerd:
  Industry-standard container runtime (CNCF project).
  Handles: image pull/push, storage snapshots, container lifecycle.
  Used directly by Kubernetes (without dockerd).

runc:
  OCI-compliant low-level runtime.
  Actually calls clone() / unshare() to set up namespaces.
  Actually writes cgroup limits.
  Short-lived: spawns the container process, then exits.

OCI (Open Container Initiative):
  Standards body for container format and runtime.
  OCI Image Spec: how image layers are stored.
  OCI Runtime Spec: how containers are run (runc implements this).

RESULT: Kubernetes deprecating Docker (the daemon) for containerd
  directly is not about containers going away — it's about cutting out
  the unnecessary dockerd layer in the stack.
```

---

**Q3. What Linux kernel features make containers possible?**

```
NAMESPACES (isolation — what the container can SEE):
  PID   → container has its own process tree; PID 1 is the app
  NET   → own network interfaces, routing table, iptables
  MNT   → own filesystem mount points
  UTS   → own hostname and domain name
  IPC   → own System V IPC and POSIX message queues
  USER  → own UID/GID mapping (container root ≠ host root)
  CGROUP→ own view of cgroup hierarchy

CGROUPS (resource limits — what the container can USE):
  cpu    → CPU shares and quotas
  memory → RAM limit, OOM kill behavior
  blkio  → block I/O throttling
  pids   → max process count

UNION FILESYSTEM (OverlayFS):
  Merges read-only image layers with a read-write container layer.
  Copy-on-write: writes to container layer, never modifies image.

SECCOMP:
  System call filter. Docker's default profile blocks ~44 dangerous syscalls.
  (e.g., blocks: reboot, kexec_load, mount)

LINUX CAPABILITIES:
  Breaks root privilege into ~40 fine-grained capabilities.
  Docker drops most by default, keeping only what's needed.
```

---

**Q4. What is a container image and how are layers stored?**

```
IMAGE = a stack of read-only filesystem layers + metadata.
Each layer = the filesystem diff (added/modified/deleted files) from the prior layer.
Each layer identified by SHA256 content hash.

STORAGE (OverlayFS, default on modern Linux):
  lowerdir: read-only layers stacked (bottom = base OS, top = your app)
  upperdir: read-write container layer (per container instance)
  merged:   unified view (what the container sees)
  workdir:  OverlayFS internal temp space

LAYER SHARING:
  Multiple images sharing the same base (e.g., node:20) share those layers on disk.
  Docker stores each layer once, referenced by digest.
  docker pull is fast on subsequent pulls because layers already cached.

COPY-ON-WRITE (CoW):
  Container reads from lower layers (fast, no copy).
  Container writes to a file in a lower layer:
    1. File is copied UP to the container's upper layer (one-time cost)
    2. Write goes to the copy in the upper layer
    3. Lower layers untouched forever
  Container deletion removes upperdir. Image layers remain.

IMAGE MANIFEST:
  JSON document listing all layers (by digest) + config.
  docker pull fetches manifest first, then layers not already cached.
```

---

**Q5. What is the difference between ENTRYPOINT and CMD?**

```dockerfile
CMD — default command/arguments (overridable by docker run arguments)
ENTRYPOINT — fixed executable (not replaced by docker run args, only appended to)

INTERACTION MATRIX:
  No ENTRYPOINT + CMD ["node","app.js"]:
    docker run img         → node app.js
    docker run img server  → server   (CMD fully replaced)

  ENTRYPOINT ["node"] + CMD ["app.js"]:
    docker run img         → node app.js
    docker run img main.js → node main.js   (CMD replaced, ENTRYPOINT stays)
    docker run --entrypoint python img      → override ENTRYPOINT

  ENTRYPOINT ["node","app.js"] (no CMD):
    docker run img              → node app.js
    docker run img --port=3000  → node app.js --port=3000  (args appended)

EXEC vs SHELL FORM:
  Exec: ["node", "app.js"]  → direct exec, no shell, PID 1 = node, signals work
  Shell: node app.js        → /bin/sh -c, PID 1 = sh, signals may not reach node

RULE: Always use exec form for ENTRYPOINT. Shell form for ENTRYPOINT
means SIGTERM goes to /bin/sh, not your app → graceful shutdown broken.

PATTERN (entrypoint script):
  ENTRYPOINT ["/entrypoint.sh"]  # run init, then:
  CMD ["node", "dist/main.js"]   # exec "$@" at end of script passes CMD
```

---

**Q6. What is a multi-stage build and why does it matter?**

```dockerfile
Multi-stage builds use multiple FROM instructions.
Only the FINAL stage becomes the image. Earlier stages are discarded.
Separates build environment from runtime environment → dramatically smaller images.

EXAMPLE (Node.js):
FROM node:20 AS builder        ← heavy: node + all devDeps + source
WORKDIR /app
COPY package*.json ./
RUN npm ci                     # installs everything incl. devDependencies
COPY . .
RUN npm run build              # compiles TypeScript → dist/

FROM node:20-alpine AS prod    ← lean: alpine + prod deps + dist only
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production   # prod deps only
COPY --from=builder /app/dist ./dist   ← copies ONLY built output
USER node
CMD ["node", "dist/main.js"]

RESULT:
  Without multi-stage: ~900MB (node:20 + devDeps + source)
  With multi-stage:    ~120MB (alpine + prod deps + dist)

OTHER PATTERNS:
  Go static binary → FROM scratch (0MB OS, just the binary, ~15MB total)
  Java → builder with JDK, runtime with JRE only (saves ~300MB)
  Test stage → run tests in CI pipeline without installing test tools in prod image

  # Run specific stage (e.g., just tests):
  docker build --target builder -t myapp:builder .
  docker run --rm myapp:builder npm test
```

---

**Q7. Explain Docker layer caching and how to optimize for it.**

```
Docker caches each layer. Cache HIT = skip re-running (fast).
Cache MISS = re-run + ALL subsequent layers re-run.

INVALIDATION TRIGGERS:
  FROM:       base image changed (new digest)
  RUN:        exact command string changed
  COPY/ADD:   any file content in the source path changed
  ENV/ARG:    value changed

THE GOLDEN RULE: least-changing instructions first, most-changing last.

ANTI-PATTERN (cache busted on every code change):
  FROM node:20
  COPY . .           ← source code changes = cache miss here
  RUN npm install    ← runs every time (even if packages didn't change)

OPTIMIZED PATTERN:
  FROM node:20
  COPY package*.json ./   ← only manifest files (change rarely)
  RUN npm install         ← cached unless package.json changed
  COPY . .                ← source code (changes often — fine at end)

LAYER CACHE IN CI:
  # Pull cache from registry before building:
  docker pull myapp:cache || true
  docker build \
    --cache-from myapp:cache \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t myapp:latest \
    -t myapp:cache \
    .
  docker push myapp:cache   # push cache layer for next CI run

BUILDKIT CACHE MOUNTS (advanced):
  RUN --mount=type=cache,target=/root/.npm npm install
  # npm cache persists across builds on the same machine — massive speedup
  RUN --mount=type=cache,target=/root/.cache/go-build go build ./...
```

---

**Q8. What is Docker BuildKit and what does it add?**

```
BuildKit: Docker's next-gen build engine (default in Docker 23+).
Enable manually: DOCKER_BUILDKIT=1 docker build ...

FEATURES:

Parallel stage execution:
  Multi-stage builds: independent stages run in parallel (not sequential).
  Unneeded stages are skipped entirely.

Cache mounts:
  RUN --mount=type=cache,target=/root/.npm npm install
  Package manager caches survive across builds (massive speedup in CI).

Secret mounts (not stored in image):
  RUN --mount=type=secret,id=npmtoken npm install
  docker build --secret id=npmtoken,src=.npmrc .
  Secret available at /run/secrets/npmtoken during build, NOT in final image.

SSH mounts (forward SSH agent):
  RUN --mount=type=ssh git clone git@github.com:private/repo.git
  docker build --ssh default .

Inline cache:
  --build-arg BUILDKIT_INLINE_CACHE=1 embeds cache metadata in pushed image.
  --cache-from myapp:latest uses that metadata on next build.

Better output:
  Collapsible logs, progress bars, cleaner error messages.

.dockerignore patterns:
  BuildKit supports negation (!pattern) and double-star globs.
```

---

**Q9. How does docker stop work and why does graceful shutdown matter?**

```
SIGNAL FLOW:
  docker stop mycontainer
    1. Sends SIGTERM to PID 1 in the container
    2. Waits --stop-timeout seconds (default 10s)
    3. If still running: sends SIGKILL (cannot be caught)

  docker kill mycontainer
    → Sends SIGKILL immediately (no grace period)

WHY GRACEFUL SHUTDOWN MATTERS:
  SIGKILL = immediate death:
    - In-flight requests dropped mid-response
    - Database transactions rolled back (or worse: incomplete)
    - Cache not flushed
    - Temp files not cleaned up
    - K8s rolling updates cause user-visible errors

HANDLING SIGTERM CORRECTLY:
  Node.js:
  process.on('SIGTERM', async () => {
    console.log('SIGTERM received — shutting down...');
    await server.close();      // stop accepting new connections
    await db.pool.end();       // close DB connections
    process.exit(0);
  });

  Python (FastAPI):
  import signal
  signal.signal(signal.SIGTERM, lambda s, f: graceful_shutdown())

SHELL FORM PROBLEM:
  If ENTRYPOINT uses shell form: node app.js
  → PID 1 = /bin/sh -c "node app.js"
  → SIGTERM goes to /bin/sh, not node
  → node never gets SIGTERM → docker stop waits 10s → SIGKILL
  FIX: Use exec form: ["node", "app.js"]
  Or: Use --init flag (tini PID 1 that forwards signals correctly)

EXTEND TIMEOUT: docker stop --time=30 mycontainer
```

---

**Q10. What are the Docker network drivers and when do you use each?**

```
BRIDGE (default):
  Creates a virtual bridge on the host (docker0 or custom).
  Containers on same bridge can communicate via IP.
  Custom bridge: containers communicate by DNS name.
  NAT for external access (docker run -p).
  USE FOR: standalone containers, development, single-host apps.

HOST:
  Container shares host's network namespace directly.
  Container's ports ARE the host's ports (no mapping needed, no NAT overhead).
  No network isolation.
  USE FOR: high-performance networking, host-level monitoring tools.

NONE:
  Only loopback interface. No external connectivity.
  USE FOR: batch jobs with no network needs, security-sensitive workloads.

OVERLAY:
  Virtual network spanning multiple Docker hosts.
  Uses VXLAN tunneling.
  Required for Docker Swarm multi-host communication.
  USE FOR: Docker Swarm services communicating across nodes.

MACVLAN:
  Container gets its own MAC address on the physical network.
  Appears as a physical device on the LAN.
  No NAT — direct routing.
  USE FOR: legacy apps needing L2 access, network monitoring (promiscuous mode).

IPVLAN:
  Similar to macvlan but shares host MAC.
  L3 mode: IP routing (no broadcast traffic).
  USE FOR: environments where MAC proliferation is a problem (cloud VPCs).

CUSTOM PLUGIN:
  Weave, Cilium, Flannel (for Kubernetes), Calico.
```

---

**Q11. What is the difference between a bind mount, named volume, and tmpfs?**

```
NAMED VOLUME:
  Created and managed by Docker.
  Stored at /var/lib/docker/volumes/<name>/
  Survives container deletion.
  Can be shared between containers (both must mount the same name).
  Supports volume drivers (NFS, EBS, GCS, etc.).
  docker run -v mydata:/app/data myapp
  USE FOR: databases, persistent app data, production storage.

BIND MOUNT:
  Mounts a HOST directory or file into the container.
  Two-way sync: host and container see same data in real time.
  Host path must exist (no auto-creation).
  docker run -v /host/path:/container/path myapp
  USE FOR: development (live code reload), config files, CI artifact sharing.
  RISK: container can write/delete host files. Full host path access.

TMPFS:
  Stored in host RAM only. Never written to disk.
  Deleted when container stops.
  docker run --mount type=tmpfs,dst=/tmp,tmpfs-size=100m myapp
  USE FOR: sensitive data (secrets, tokens) that shouldn't touch disk,
           high-speed temporary storage.

ANONYMOUS VOLUME:
  Created by VOLUME instruction in Dockerfile.
  Random name assigned by Docker.
  Survives container stop but not docker run (new container = new anonymous vol).
  Can pile up — clean with: docker volume prune

COMPARISON:
  Persistence:   Named > Anonymous > Bind (depends on host) > tmpfs (none)
  Performance:   tmpfs > Bind > Named (usually)
  Sharing:       Named (easy) > Bind (host-path dependent) > tmpfs (no)
  Portability:   Named (driver-based) > tmpfs > Bind (host-path coupling)
```

---

**Q12. How does Docker networking DNS work between containers?**

```
DEFAULT BRIDGE (docker0):
  Containers communicate by IP address only.
  No automatic hostname resolution.
  --link flag (deprecated): adds /etc/hosts entry.

CUSTOM BRIDGE NETWORK:
  Docker embeds a DNS server at 127.0.0.11 inside each container.
  Container names → DNS-resolvable hostnames automatically.
  
  docker network create mynet
  docker run -d --network mynet --name db postgres:16
  docker run -d --network mynet --name api myapp
  # Inside api container: ping db → resolves to db container IP

COMPOSE NETWORKS:
  Compose creates a default bridge network per project.
  Service names = DNS hostnames.
  services:
    api:   # reachable as "api" from db, nginx, etc.
    db:    # reachable as "db" from api
  
  Containers can also have aliases:
  networks:
    mynet:
      aliases:
        - database
        - postgres

DNS RESOLUTION ORDER (inside container):
  1. Docker embedded DNS (127.0.0.11) — handles container/service names
  2. Host DNS servers (from /etc/resolv.conf)
  
  If Docker DNS fails → falls through to host DNS → external DNS.

SERVICE DISCOVERY ACROSS HOSTS:
  Docker Swarm: overlay network + built-in DNS for service names.
  Kubernetes: CoreDNS (separate pod) handles cluster-wide DNS.
```

---

**Q13. How does port mapping work internally?**

```
docker run -p 8080:80 nginx

WHAT ACTUALLY HAPPENS:
  1. Docker adds iptables NAT rules on the host.
  2. Incoming TCP to host:8080 → DNAT → container_ip:80
  3. Reply traffic: SNAT back to original source.

  iptables -t nat -A DOCKER -p tcp --dport 8080 -j DNAT --to-destination 172.17.0.2:80

BINDING ADDRESS:
  -p 8080:80         → 0.0.0.0:8080 → ALL interfaces (public + private)
  -p 127.0.0.1:8080:80 → localhost only (safer for internal services)
  -p 0.0.0.0:8080:80   → explicit all interfaces

FIREWALL BYPASS (important):
  Docker inserts rules in iptables BEFORE ufw/firewalld rules.
  A port mapped with -p 8080:80 is PUBLICLY accessible even if ufw blocks 8080.
  Fix: use 127.0.0.1:8080:80 OR configure DOCKER-USER iptables chain.

-P (uppercase): auto-assign host ports
  Publishes all EXPOSE'd ports on random high ports.
  docker port mycontainer → shows mappings.

INTERNAL CONTAINER NETWORKING:
  Containers on same custom network communicate on internal IPs without -p.
  -p is only needed when you want host or external access.
  DB container: no -p needed (only api needs to reach it, same network).
```

---

**Q14. What is a Docker health check and how does it affect orchestration?**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

PARAMETERS:
  --interval     : time between health checks (default 30s)
  --timeout      : check must complete in this time (default 30s)
  --start-period : grace period before first check counts (default 0s)
                   Use for slow-starting apps (JVM warmup, migrations)
  --retries      : consecutive failures before status = unhealthy (default 3)

EXIT CODES:
  0 = healthy
  1 = unhealthy
  2 = reserved (don't use)

CONTAINER STATES:
  starting → (grace period) → healthy / unhealthy

IMPACT ON ORCHESTRATION:
  Docker Compose depends_on + condition: service_healthy:
    api waits for db to be healthy before starting.
    Without this: api might start before DB accepts connections → crash loop.

  Docker Swarm:
    Unhealthy containers are restarted automatically.
    Rolling updates wait for healthy before proceeding to next instance.

  Kubernetes:
    readinessProbe (not Docker healthcheck): controls traffic routing.
    livenessProbe: controls container restart.
    startupProbe: handles slow startup.
    K8s ignores Docker HEALTHCHECK — define probes in Pod spec instead.

TESTING LOCALLY:
  docker inspect --format='{{.State.Health.Status}}' mycontainer
  docker inspect --format='{{json .State.Health}}' mycontainer | jq
```

---

**Q15. What does `docker run --init` do and why do you need it?**

```
PROBLEM: PID 1 in containers has special responsibilities:
  - Must reap zombie processes (wait() on dead child processes)
  - Must forward signals to child processes
  - If PID 1 exits, the entire container stops

If your app is PID 1 directly (via exec form CMD):
  - Node.js, Python, etc. do NOT reap zombies by default
  - Zombie processes accumulate over time → memory leak
  - Signal forwarding to children may not work

--init:
  Injects tini (a minimal init system) as PID 1.
  Your app becomes PID 2 (child of tini).
  tini: properly reaps zombie children, forwards signals (SIGTERM, SIGINT) to your process.

docker run --init myapp

Or embed in Dockerfile:
  FROM node:20
  RUN apk add --no-cache tini
  ENTRYPOINT ["/sbin/tini", "--"]
  CMD ["node", "app.js"]

WHEN YOU NEED --init:
  ✓ App spawns child processes (spawning shell commands, workers)
  ✓ App doesn't handle signals explicitly
  ✓ Container runs long enough for zombie accumulation to matter

WHEN YOU DON'T NEED --init:
  App is a single-process daemon that handles its own signals.
  App already uses exec form and handles SIGTERM.
```

---

**Q16. What are Docker labels and how are they used?**

```dockerfile
# Labels = key-value metadata attached to images, containers, networks, volumes.

# In Dockerfile:
LABEL maintainer="team@company.com"
LABEL version="1.2.3"
LABEL description="My web application"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.created="2024-01-15T10:00:00Z"
LABEL org.opencontainers.image.revision="a3b4c5d"

# OCI Annotation spec (recommended standard):
# org.opencontainers.image.title
# org.opencontainers.image.description
# org.opencontainers.image.version
# org.opencontainers.image.source
# org.opencontainers.image.created
# org.opencontainers.image.revision

USE CASES:

Filtering:
  docker ps --filter label=environment=production
  docker images --filter label=maintainer=team@company.com

Automation:
  Labels used by monitoring tools (Prometheus autodiscovery, Traefik routing).
  Traefik reads labels to configure routing:
  labels:
    - "traefik.http.routers.api.rule=Host('api.example.com')"

Tracing:
  Embed git SHA in image label → trace any container to exact commit.
  docker build --label git-sha=$(git rev-parse HEAD) .

Runtime labels on containers:
  docker run --label env=staging myapp
  docker ps --filter label=env=staging
```

---

**Q17. How do you pass secrets securely to a Docker container?**

```
WRONG APPROACHES:
  ENV DB_PASSWORD=secret     → visible in docker inspect, docker history, logs
  ARG DB_PASSWORD=secret     → visible in image cache (docker history)
  Baked into image           → anyone with image can extract secrets

CORRECT APPROACHES:

1. Runtime environment variables (acceptable for non-critical):
   docker run -e DB_PASSWORD=secret myapp
   # Visible in: docker inspect, /proc/1/environ inside container
   # Not baked in image — better, but not fully secure

2. env_file with strict permissions:
   docker run --env-file /secure/path/.env myapp
   # File must have mode 600, outside repo

3. Docker secrets (Swarm mode):
   echo "mysecret" | docker secret create db_pass -
   # In Swarm service:
   docker service create --secret db_pass myapp
   # Secret available at /run/secrets/db_pass (tmpfs — in memory only)
   # NEVER written to disk

4. BuildKit --secret (build time, not in image):
   docker build --secret id=npmtoken,src=.npmtoken .
   # In Dockerfile:
   RUN --mount=type=secret,id=npmtoken npm install
   # Secret NOT present in any image layer

5. External secret managers (production best practice):
   HashiCorp Vault / AWS Secrets Manager / GCP Secret Manager
   App authenticates to vault at startup, fetches secrets.
   Secrets never touch container image or host filesystem.
   Rotation is centralized and audited.

6. Kubernetes Secrets (if using K8s):
   Mounted as files or env vars via secretKeyRef.
   Stored in etcd (encrypted at rest if configured).
```

---

**Q18. What is the difference between COPY and ADD in a Dockerfile?**

```
COPY:
  Copies files from build context (or another stage) into the image.
  Simple, predictable, no side effects.
  PREFERRED for almost all use cases.

  COPY src/ /app/src/
  COPY package*.json ./
  COPY --chown=node:node . /app/       # with ownership
  COPY --from=builder /app/dist /app/  # from another stage

ADD:
  Superset of COPY — adds two extra behaviors:
  1. Fetch remote URLs: ADD https://example.com/file.tar.gz /tmp/
  2. Auto-extract tar archives: ADD archive.tar.gz /app/

WHEN TO USE ADD:
  Only when you specifically need URL fetch or tar auto-extraction.
  For URLs: prefer RUN curl/wget (more explicit, better cache control, can verify checksum).
  For tar: ADD archive.tar.gz /app/ is legitimate and concise.

WHY COPY IS PREFERRED:
  ADD with URL skips the build cache check → always re-downloads.
  ADD is harder to reason about (magic behavior).
  Security: ADD from URL gives no checksum verification by default.
  Linting tools (hadolint) warn against ADD when COPY would suffice.

MULTI-STAGE COPY (must use COPY --from):
  COPY --from=builder /app/dist /app/dist
  COPY --from=nginx:alpine /etc/nginx/nginx.conf /etc/nginx/  # from named image
```

---

**Q19. What is a Docker context and how do you manage multiple contexts?**

```
CONTEXT: named configuration pointing to a Docker endpoint.
Default: local Docker daemon via /var/run/docker.sock.

WHY CONTEXTS:
  Manage multiple Docker environments (local, remote server, AWS ECS, Kubernetes).
  Switch between them without changing environment variables.

COMMANDS:
  docker context ls                     # list all contexts
  docker context inspect default        # inspect current
  docker context use production         # switch active context
  
  # Create context for remote SSH host:
  docker context create remote \
    --docker "host=ssh://user@server.com"
  docker context use remote
  docker ps   # now talks to remote server's Docker daemon

  # Create context for AWS ECS (with ECS integration plugin):
  docker context create ecs myecscontext

BUILD CONTEXTS (different meaning in docker build):
  The build context = files sent to the Docker daemon for the build.
  docker build .          → current directory is build context
  docker build ./mydir    → specific directory
  docker build https://github.com/org/repo  → git repo as context
  docker build - < Dockerfile  → no context (pipe Dockerfile)
  
  Keep build context small with .dockerignore.
  Large context = slow build (network transfer to daemon).
```

---

**Q20. What is Docker Swarm and how does it compare to Kubernetes?**

```
DOCKER SWARM:
  Docker's native clustering and orchestration solution.
  Built directly into Docker daemon (no extra install).
  
  FEATURES:
    Declarative service model (desired state)
    Automatic load balancing (VIP or DNS round-robin)
    Rolling updates with rollback
    Overlay networking across nodes
    Docker secrets and configs
    Manager/worker node roles

  COMMANDS:
    docker swarm init                  # init swarm, current node = manager
    docker swarm join --token ...      # add worker nodes
    docker service create --replicas 3 myapp  # deploy service
    docker service update --image myapp:v2 myservice  # rolling update
    docker stack deploy -c docker-compose.yml mystack  # deploy compose stack

KUBERNETES:
  Open-source, CNCF project. Industry standard for production.
  Much more complex but far more powerful.
  Separate control plane (API server, etcd, scheduler, controller-manager).

SWARM vs KUBERNETES:
  Simplicity:     Swarm ✓ (works out of box) vs K8s (steep learning curve)
  Features:       K8s ✓ (RBAC, CRDs, HPA, PV, network policies, etc.)
  Ecosystem:      K8s ✓ (Helm, operators, massive tooling)
  Production use: K8s ✓ (dominant in enterprise)
  Suitable for:   Swarm = small teams, simple deployments
                  K8s = production, complex workloads, scale

STATUS: Docker Swarm is largely superseded by Kubernetes.
Most new deployments use K8s or managed K8s (EKS, GKE, AKS).
```

---

## SECTION 2: IMAGES & DOCKERFILE

---

**Q21. What is the difference between SHELL and EXEC form in Dockerfile instructions?**

```dockerfile
SHELL FORM: instruction args
  Runs as: /bin/sh -c "instruction args"
  Supports: shell features (variables, pipes, &&, ||, redirects, globbing)
  PID 1 (for ENTRYPOINT/CMD): /bin/sh — signals may not reach your app

  RUN apt-get update && apt-get install -y curl  # shell form — uses &&
  CMD node app.js                                 # shell form

EXEC FORM: ["instruction", "arg1", "arg2"]
  Runs directly — no shell intermediary.
  No shell expansion: $HOME is literal (not expanded)
  PID 1 (for ENTRYPOINT/CMD): your process — signals delivered directly.
  Required for Windows containers (no /bin/sh).

  RUN ["apt-get", "install", "-y", "curl"]   # exec form — no shell
  ENTRYPOINT ["node", "app.js"]              # signals reach node directly
  CMD ["--port", "3000"]                     # args to ENTRYPOINT

WHEN TO USE WHICH:
  RUN: shell form is fine (you want &&, pipes, variables)
  ENTRYPOINT: ALWAYS exec form (signals must reach your process)
  CMD: exec form preferred (clearer, works on Windows)

MIXING:
  ENTRYPOINT ["/entrypoint.sh"]   # exec form — runs script directly
  CMD ["node", "app.js"]         # exec form — passed as args to script
  # In entrypoint.sh: exec "$@"  # exec replaces shell with CMD
```

---

**Q22. How do you minimize Docker image size?**

```
ORDERED BY IMPACT:

1. MULTI-STAGE BUILDS (biggest win):
   Separate build stage from runtime.
   Only final stage is the image.
   Typically: 500MB → 80MB for Node.js

2. CHOOSE MINIMAL BASE IMAGE:
   ubuntu:22.04  78MB → debian:slim 74MB → alpine:3.19 7MB → scratch 0MB
   Match base to your runtime: node:20-alpine, python:3.12-slim, golang:1.22-alpine

3. COMBINE RUN COMMANDS:
   Each RUN = 1 layer. apt-get update + install + cleanup MUST be one RUN.
   RUN apt-get update && apt-get install -y --no-install-recommends curl \
       && rm -rf /var/lib/apt/lists/*
   Cleanup in same RUN — separate RUN can't delete previous layer's files.

4. .DOCKERIGNORE:
   Exclude: node_modules/, .git/, .env, *.log, dist/, coverage/
   Large context → slow build. Large context doesn't increase image size
   (only what's COPY'd matters) but it slows the context transfer.

5. COPY ONLY WHAT'S NEEDED:
   Don't COPY . . and then ignore files — use .dockerignore.
   Copy specific artifacts: COPY --from=builder /app/dist .

6. --NO-INSTALL-RECOMMENDS (Debian/Ubuntu):
   Skips optional recommended packages. Can save 20-50MB.

7. apk add --no-cache (Alpine):
   Skips writing apk cache to the layer.

MEASURE:
  docker images myapp              # total size
  docker history myapp             # size per layer
  dive myapp                       # interactive layer explorer
```

---

**Q23. What is the ARG instruction and how does it differ from ENV?**

```dockerfile
ARG — build-time variable (NOT available in running container):
  Declared in Dockerfile.
  Passed at build time: docker build --build-arg KEY=value .
  Only available DURING the build (in RUN, COPY, etc.).
  Not persisted in the final image (not visible in docker inspect).
  Exception: ARG value CAN appear in docker history — don't use for secrets.

ENV — runtime environment variable (persists in image AND container):
  Set in Dockerfile.
  Available during build AND at runtime.
  Visible in: docker inspect, /proc/1/environ inside container.
  Can be overridden at runtime: docker run -e KEY=newvalue myapp.

INTERACTION:
  ARG VERSION=20
  FROM node:${VERSION}     ← ARG used in FROM

  ARG BUILD_DATE           ← re-declare after FROM (scope resets per stage)
  ENV BUILD_DATE=${BUILD_DATE}  ← promote ARG to ENV (now runtime-visible)

SCOPING:
  ARG before first FROM: available ONLY in FROM instruction.
  ARG after FROM: available in that stage only.
  ENV set in stage 1: persists into stage 2 only if COPY'd.

COMMON PATTERN (version pinning via ARG with defaults):
  ARG APP_VERSION=1.0.0
  ARG NODE_ENV=production
  ENV NODE_ENV=${NODE_ENV}

  # Build with override:
  docker build --build-arg APP_VERSION=2.0.0 .
```

---

**Q24. How does the WORKDIR instruction work?**

```dockerfile
WORKDIR /app

WHAT IT DOES:
  Sets the working directory for all subsequent instructions:
    RUN, CMD, ENTRYPOINT, COPY, ADD
  Creates the directory if it doesn't exist (including parent dirs).
  Affects relative paths in all subsequent instructions.

COMPARED TO cd:
  RUN cd /app && npm install   ← cd only affects this RUN — resets after
  WORKDIR /app
  RUN npm install              ← WORKDIR persists across all instructions

MULTIPLE WORKDIR:
  WORKDIR /app
  WORKDIR src        ← relative: now at /app/src
  RUN pwd            ← outputs /app/src

ABSOLUTE vs RELATIVE:
  WORKDIR /app       → absolute: sets to /app regardless of current dir
  WORKDIR src        → relative: appends to current WORKDIR

DEFAULT WORKDIR:
  If not set: / (root of filesystem). Bad practice.
  Always set WORKDIR explicitly.

BEST PRACTICE:
  WORKDIR /app       # set early, use /app consistently
  COPY package*.json ./    # copies to /app/package.json
  RUN npm install          # runs in /app
  COPY . .                 # copies to /app/
  CMD ["node", "app.js"]   # runs in /app → finds app.js
```

---

**Q25. What is ONBUILD and when would you use it?**

```dockerfile
# ONBUILD adds trigger instructions to an image.
# These instructions DO NOT run when building the image itself.
# They run when another image uses this image as a BASE (FROM).

# Example: Create a base image for all Node.js apps
FROM node:20
WORKDIR /app
ONBUILD COPY package*.json ./
ONBUILD RUN npm ci
ONBUILD COPY . .
ONBUILD CMD ["node", "app.js"]
# Build and push: docker build -t mycompany/node-base .

# In a specific app's Dockerfile:
FROM mycompany/node-base
# The ONBUILD triggers fire here automatically:
# → COPY package*.json ./
# → RUN npm ci
# → COPY . .
# → CMD ["node", "app.js"]
# The app Dockerfile can be EMPTY (just FROM line)!

USE CASES:
  ✓ Shared base images for teams with standardized build patterns
  ✓ Framework images that inject build steps into child images
  ✓ Enforce company policies (linting, security scanning) on all images

DOWNSIDES:
  ✗ Hidden behavior — hard to debug (triggers not visible in child Dockerfile)
  ✗ Inflexible — all children get same triggers
  ✗ Generally considered bad practice for public images
  Modern alternative: Multi-stage builds with COPY --from (more explicit)
```

---

## SECTION 3: NETWORKING & VOLUMES

---

**Q41. How do you connect two Docker Compose projects together?**

```yaml
# PROJECT A: defines a shared network
# docker-compose.yml (project A):
services:
  db:
    image: postgres:16
    networks:
      - shared-net

networks:
  shared-net:
    name: shared-net   # explicit name so project B can reference it

---

# PROJECT B: joins the external network
# docker-compose.yml (project B):
services:
  api:
    image: myapp
    networks:
      - shared-net
      - internal

networks:
  shared-net:
    external: true     # pre-existing network, don't create/destroy
    name: shared-net
  internal:
    driver: bridge

# api service can now reach db by hostname "db"

ALTERNATIVES:
  1. Use a single Compose file with multiple services (simplest)
  2. Use --project-name to share a project namespace
  3. Use an overlay network (for multi-host scenarios)
  4. Use service mesh (for production microservices)
```

---

**Q42. What is a Docker volume driver and when would you use one?**

```
DEFAULT VOLUME DRIVER: local
  Stores volumes at /var/lib/docker/volumes/ on the local host.
  Not shared across hosts (single-node).

VOLUME DRIVERS (plugins):
  Allow volumes backed by external storage systems.

  local (with options):
    docker volume create --driver local \
      --opt type=nfs \
      --opt o=addr=nfs-server.com,rw \
      --opt device=:/path/on/nfs \
      mynfs
    # Mounts NFS share as a Docker volume

  rexray/ebs (AWS):
    docker volume create --driver rexray/ebs \
      --opt size=20 \
      --opt volumetype=gp3 \
      myebs
    # Provisions and mounts an AWS EBS volume

  rexray/s3fs: S3 bucket mounted as filesystem
  vieux/sshfs:  Remote volume over SSH
  portworx:     Cloud-native storage, HA volumes

USE CASES:
  ✓ Database volumes that must survive container migration to another host
  ✓ Shared storage across multiple containers on different hosts
  ✓ Cloud-native storage with automatic provisioning
  ✓ Kubernetes uses CSI drivers (Container Storage Interface) — same concept

KUBERNETES EQUIVALENT: PersistentVolume + StorageClass
  StorageClass = volume driver
  PVC = volume request → automatically provisions the volume
```

---

## SECTION 4: COMPOSE, REGISTRY & SECURITY

---

**Q56. What is Docker Compose and what problem does it solve?**

```yaml
PROBLEM:
  A real app has multiple containers: API, database, cache, reverse proxy, worker.
  Running each with docker run requires:
    - Long commands with many flags
    - Manual network creation
    - Remembering startup order
    - Manual environment setup per developer

COMPOSE SOLUTION:
  Declarative YAML file defines all services, networks, volumes.
  Single command: docker compose up -d → everything starts.
  Single command: docker compose down → everything stops.

WHAT COMPOSE PROVIDES:
  Service definition: image, ports, env, volumes, dependencies
  Automatic networking: services on same project network, DNS by service name
  Dependency ordering: depends_on ensures startup order
  Environment management: .env file, env_file, environment vars
  Override files: dev/prod/test configurations
  Health-aware startup: condition: service_healthy
  Scaling: docker compose up --scale api=3

TYPICAL STACK (docker-compose.yml):
services:
  api:
    build: .
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
  redis:
    image: redis:7-alpine
volumes:
  pgdata:

DEVELOPMENT WORKFLOW:
  docker compose up -d          # start everything
  docker compose logs -f api    # tail logs
  docker compose exec api sh    # shell into container
  docker compose restart api    # restart one service
  docker compose down -v        # stop + delete volumes (clean slate)
```

---

**Q57. How does Docker image promotion work across environments?**

```
PRINCIPLE: Build once, promote the same image through environments.
Never rebuild the image for staging or production.
Environment-specific config via environment variables, not image.

WORKFLOW:
  1. CI builds image on merge to main:
     docker build -t myapp:${GIT_SHA} .
     docker push myapp:${GIT_SHA}

  2. Deploy to development (automatic):
     kubectl set image deploy/api api=myapp:${GIT_SHA} -n dev
     # or: docker compose with IMAGE=myapp:${GIT_SHA}

  3. Promote to staging (test gate):
     docker tag myapp:${GIT_SHA} myapp:staging
     docker push myapp:staging
     # Deploy to staging environment

  4. Promote to production (approval gate):
     docker tag myapp:${GIT_SHA} myapp:v1.2.3
     docker tag myapp:${GIT_SHA} myapp:latest
     docker push myapp:v1.2.3
     docker push myapp:latest

IMMUTABILITY:
  Once an image is built with a git SHA tag, it never changes.
  Semantic version tags (v1.2.3) should also be immutable.
  Only :latest and :staging float (point to latest promoted image).

SCAN GATE:
  After build: scan image for vulnerabilities (trivy/grype).
  Only promote if scan passes (or CVSS score below threshold).

REGISTRY STRUCTURE:
  myregistry/myapp:abc1234  → immutable, built from commit abc1234
  myregistry/myapp:v1.2.3  → immutable, released version
  myregistry/myapp:staging → floating, current staging image
  myregistry/myapp:latest  → floating, current production image
```

---

**Q58. What is Docker Content Trust (DCT) and image signing?**

```
DOCKER CONTENT TRUST (DCT):
  Ensures images are cryptographically signed by the publisher.
  Prevents pulling tampered or unsigned images.
  Uses Notary (The Update Framework — TUF).

ENABLE:
  export DOCKER_CONTENT_TRUST=1
  # Now: docker pull unsigned-image → ERROR
  # docker push → automatically signs the image

SIGNING:
  # First push generates signing keys:
  docker trust key generate mykey
  docker trust signer add --key mykey.pub myname myregistry/myapp
  docker trust sign myregistry/myapp:v1.0.0

VERIFY:
  docker trust inspect --pretty myregistry/myapp:v1.0.0

COSIGN (modern alternative, Sigstore):
  Open source. Works with any OCI registry. No separate infrastructure.
  
  # Sign (after build, in CI):
  cosign sign --key cosign.key myapp:v1.0.0
  
  # Verify (before deployment):
  cosign verify --key cosign.pub myapp:v1.0.0
  
  # Keyless signing (using OIDC — for CI):
  cosign sign myapp:v1.0.0   # uses GitHub/GitLab OIDC token

KUBERNETES + COSIGN:
  Use policy controllers (Kyverno, OPA Gatekeeper) to reject unsigned images.
  policy: require all images to have valid cosign signature before scheduling.
```

---

## SECTION 5: PERFORMANCE & PRODUCTION

---

**Q71. How do you troubleshoot a container that keeps restarting?**

```bash
# Step 1: Check exit code
docker ps -a    # shows exited containers with exit code
# Exit code 1   = application error
# Exit code 137 = OOMKilled (137 = 128 + 9/SIGKILL)
# Exit code 139 = segfault (128 + 11/SIGSEGV)
# Exit code 143 = SIGTERM (128 + 15) — graceful but terminated

# Step 2: View logs (including from before crash)
docker logs mycontainer
docker logs --tail 100 mycontainer
docker logs --since 5m mycontainer

# Step 3: Inspect container state
docker inspect mycontainer | jq '.[0].State'
# Shows: Status, ExitCode, Error, OOMKilled, StartedAt, FinishedAt

# Step 4: Check resource limits
docker stats --no-stream mycontainer
docker inspect mycontainer | jq '.[0].HostConfig.Memory'
# If OOMKilled: increase --memory limit or reduce app memory usage

# Step 5: Run interactively for debugging
docker run --rm -it --entrypoint sh myapp
# Override entrypoint, explore filesystem, test commands manually

# Step 6: Check for startup dependency issues
# App crashes because DB not ready → add retry logic or healthcheck depends_on

# Step 7: Check oom_score_adj
docker inspect mycontainer | jq '.[0].HostConfig.OomKillDisable'

# RESTART POLICIES:
# no: never restart (default)
# always: always restart (even on docker daemon restart)
# on-failure[:max-retries]: restart only on non-zero exit
# unless-stopped: restart always except when manually stopped
```

---

**Q72. What is Docker BuildKit's cache mount feature?**

```dockerfile
# Cache mounts persist between builds on the same machine.
# Package manager caches survive — dramatically speeds up CI builds.

# Node.js npm cache:
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go build cache:
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    go build -o /app/server ./cmd/server

# Python pip cache:
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# apt-get cache:
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y curl

# HOW IT WORKS:
# --mount=type=cache,target=/path
#   → mounts a persistent cache at /path during this RUN only
#   → not included in the image layer
#   → persists on the build host between builds
#   → shared across all builds using the same target path

# RESULT:
# First build: npm install downloads everything → 60s
# Second build: cache populated → npm install reads from cache → 5s

# IMPORTANT: Cache mounts are NOT available at runtime — only during build.
# They are machine-local — CI must use the same runner for cache to persist,
# OR use --cache-to / --cache-from with registry for distributed caching.
```

---

**Q73. How do you implement zero-downtime deployments with Docker?**

```bash
# APPROACH 1: Blue-Green Deployment
# Run two versions simultaneously, switch traffic.

# Deploy new version (green):
docker run -d --name app-green myapp:v2

# Test green:
curl http://green-ip:3000/health

# Switch load balancer (nginx/traefik/HAProxy) from blue to green.
# If OK: stop old version (blue).
docker stop app-blue && docker rm app-blue

# APPROACH 2: Rolling Update (Docker Swarm)
docker service update \
  --image myapp:v2 \
  --update-parallelism 1 \    # update 1 replica at a time
  --update-delay 10s \        # wait 10s between each
  --update-failure-action rollback \  # rollback on failure
  myservice

# APPROACH 3: Docker Compose rolling update (manual)
# Update image in compose file, then:
docker compose pull api
docker compose up -d --no-deps api   # update api without restarting db/redis

# APPROACH 4: Kubernetes rolling update (most robust)
kubectl set image deployment/api api=myapp:v2
kubectl rollout status deployment/api   # watch progress
kubectl rollout undo deployment/api     # rollback if needed

# KEY REQUIREMENTS for zero-downtime:
✓ Graceful shutdown: handle SIGTERM, finish in-flight requests
✓ Health checks: new container healthy before traffic routed to it
✓ readinessProbe (K8s): controls when traffic is sent to pod
✓ maxUnavailable: 0 (in K8s) → always keep full capacity
✓ preStop hook: add small sleep before SIGTERM to drain connections
✓ Connection draining in load balancer before stopping old container
```

---

**Q74. What is Distroless and when should you use it?**

```dockerfile
# Distroless images (from Google) contain only:
#   - Your app and its runtime dependencies
#   - CA certificates
#   - /etc/passwd (minimal user info)
#   No shell, no package manager, no utilities

# SECURITY BENEFITS:
#   ✓ No shell → if attacker gets code exec, they can't get an interactive shell
#   ✓ No package manager → can't install tools to escalate attack
#   ✓ Smaller attack surface → fewer packages = fewer CVEs
#   ✓ Smaller image → faster pull, less storage

# Available distroless images:
#   gcr.io/distroless/static:nonroot   → for Go static binaries (5MB)
#   gcr.io/distroless/base:nonroot     → for binaries needing glibc (20MB)
#   gcr.io/distroless/nodejs:20        → for Node.js apps
#   gcr.io/distroless/python3          → for Python apps
#   gcr.io/distroless/java21           → for Java apps

# Go example:
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

FROM gcr.io/distroless/static:nonroot
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
# Image: ~5MB, no shell, no root

# DEBUG VARIANT:
#   gcr.io/distroless/nodejs:debug    → includes busybox shell
#   Use only in dev/staging for debugging

# DOWNSIDE:
#   No shell → harder to debug in production
#   No package manager → can't add tools at runtime
#   Must use distroless debug variant or copy tools in from another stage
```

---

**Q75. What is docker save, docker load, and when do you use them?**

```bash
# docker save: export image(s) to a tar archive
docker save -o myapp.tar myapp:v1.0.0
docker save myapp:v1.0.0 | gzip > myapp.tar.gz  # compressed

# Save multiple images:
docker save -o bundle.tar myapp:v1 nginx:alpine postgres:16

# docker load: import image from tar archive
docker load -i myapp.tar
docker load < myapp.tar
docker load < myapp.tar.gz  # supports gzip

# WHEN TO USE INSTEAD OF PUSH/PULL:
#   Air-gapped environments (no internet access to registry)
#   Transferring images to servers without registry access
#   Archiving specific image versions offline
#   Sharing images via USB/file transfer

# COMPARISON:
#   docker save/load: exports ALL layers including metadata
#     → full image, can be reloaded exactly
#   docker export/import (CONTAINER → tarball): exports filesystem only
#     → flattened, loses layer history, metadata, CMD, ENV

# docker export: export RUNNING CONTAINER filesystem (not image)
docker export mycontainer -o container.tar
# docker import: import container filesystem as NEW image
docker import container.tar myapp:imported
# Note: imported image loses: ENTRYPOINT, CMD, ENV, EXPOSE, etc.
# Only use import if you specifically need the container state.

# AIRG-GAPPED WORKFLOW:
# On internet-connected machine:
docker pull myapp:v1
docker save -o myapp.tar myapp:v1
# Transfer myapp.tar to airgapped machine
# On airgapped machine:
docker load -i myapp.tar
docker run myapp:v1
```

---

**Q76. How does Docker handle logging and what are the log drivers?**

```bash
# Docker captures stdout and stderr from PID 1 of the container.
# App must log to stdout/stderr — NOT to files inside the container.

# VIEW LOGS:
docker logs mycontainer            # all logs
docker logs -f mycontainer        # follow (tail -f)
docker logs --tail 100 mycontainer  # last 100 lines
docker logs --since 1h mycontainer  # last hour
docker logs --timestamps mycontainer  # include timestamps

# LOG DRIVERS (where logs are sent):
json-file (default):
  Stored at /var/lib/docker/containers/<id>/<id>-json.log
  Options: max-size=10m, max-file=3 (rotation)
  docker run --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 myapp

journald:
  Logs to systemd journal.
  docker logs still works. Also accessible via journalctl.

syslog / gelf:
  Forwards to syslog daemon or Graylog.

fluentd:
  Forwards to Fluentd → Elasticsearch, Splunk, etc.
  docker run --log-driver fluentd --log-opt fluentd-address=localhost:24224 myapp

awslogs:
  Directly to AWS CloudWatch Logs.
  docker run --log-driver awslogs \
    --log-opt awslogs-group=/myapp/production \
    --log-opt awslogs-region=us-east-1 myapp

gcplogs:
  Google Cloud Logging.

none:
  No logging. docker logs returns nothing.
  For very performance-sensitive containers.

# GLOBAL DEFAULT (daemon.json):
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

# BEST PRACTICE:
# Use json-file in development (docker logs works).
# Use fluentd/awslogs/gcplogs in production (centralized logging).
# App logs to stdout/stderr. Sidecar or log driver ships to ELK/CloudWatch.
```

---

**Q77. What is a Docker registry mirror and how do you configure it?**

```
PROBLEM:
  Every docker pull hits Docker Hub (hub.docker.com).
  Docker Hub has rate limits: 100 pulls/6h for anonymous, 200 for free accounts.
  In CI: hundreds of pulls → rate limit hit → builds fail.
  Latency: pulling from Docker Hub adds seconds to every build.

REGISTRY MIRROR (pull-through cache):
  Local or regional cache that proxies Docker Hub.
  First pull: fetches from Docker Hub, caches locally.
  Subsequent pulls: served from local cache (fast, no rate limit hit).

SETUP ON DOCKER DAEMON (/etc/docker/daemon.json):
{
  "registry-mirrors": [
    "https://mirror.gcr.io",     # Google's Docker Hub mirror (public)
    "https://my-mirror.internal" # your private mirror
  ]
}
# Then: sudo systemctl restart docker

SELF-HOSTED MIRROR (Harbor or registry:2):
  # Run registry with mirror mode:
  docker run -d -p 5000:5000 \
    -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
    registry:2

ALTERNATIVES TO DOCKER HUB:
  GitHub Container Registry (ghcr.io): generous limits for GitHub users
  AWS ECR Public: no rate limits for public images
  Google Artifact Registry: regional, fast in GCP
  Quay.io: Red Hat, good for enterprise
  Harbor: self-hosted, enterprise features (scanning, RBAC, replication)

IN KUBERNETES:
  Use imagePullPolicy: IfNotPresent (default for tagged images).
  Use node-local image caching (containerd pulls once per node, not per pod).
  Use ECR/GCR/ACR (cloud-native, no rate limits in cloud environments).
```

---

**Q78. What is a Docker plugin and how do volume plugins work?**

```
DOCKER PLUGIN SYSTEM:
  Extends Docker with third-party capabilities.
  Plugins run as containers with special capabilities.
  Types: volume, network, logging, authorization (authz).

  docker plugin install <plugin>   # install from Docker Hub
  docker plugin ls                 # list installed plugins
  docker plugin enable myplugin
  docker plugin disable myplugin
  docker plugin remove myplugin

VOLUME PLUGINS:
  Allow volumes to be backed by external storage systems.
  Plugin handles: create, mount, unmount, delete, list.

  # Install plugin:
  docker plugin install vieux/sshfs   # SSH filesystem volume

  # Create volume using plugin:
  docker volume create \
    --driver vieux/sshfs \
    --opt sshcmd=user@server:/remote/path \
    --opt password=secret \
    mysshvol

  # Use in container:
  docker run -v mysshvol:/app/data myapp
  # Container sees remote SSH path as local directory

COMMON PRODUCTION VOLUME PLUGINS:
  vieux/sshfs:    SFTP/SSH remote filesystem
  rexray/ebs:     AWS Elastic Block Store
  rexray/gcepd:   Google Persistent Disk
  rexray/azureud: Azure Unmanaged Disk
  portworx:       Cloud-native distributed storage (HA, snapshots)

KUBERNETES EQUIVALENT:
  Container Storage Interface (CSI) drivers.
  StorageClass + PersistentVolumeClaim — same concept, more standardized.
  EBS CSI driver, GCE PD CSI, Azure Disk CSI, etc.
```

---

**Q79. How do you run Docker in Docker (DinD) and what are the risks?**

```
DOCKER-IN-DOCKER (DinD):
  Running the Docker daemon inside a Docker container.
  Used in: CI/CD pipelines that need to build Docker images.

METHOD 1: Docker socket mount (preferred for CI)
  Mount the host Docker socket into the CI container.
  docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
  
  ✓ Simple — no privilege escalation needed
  ✓ Shares host Docker daemon (layer cache reused)
  ✗ SECURITY RISK: container has full control of host Docker daemon
    → can mount any host path, start any container, escape to host
  ✗ Sharing daemon: one CI job can interfere with another's containers

METHOD 2: True DinD (separate daemon inside container)
  docker run --privileged docker:dind
  
  ✓ Isolated Docker daemon (no access to host containers)
  ✗ Requires --privileged (full capabilities) — major security risk
  ✗ Doesn't share layer cache with host → every build re-pulls everything
  ✗ Nested virtualization can have performance issues

METHOD 3: Rootless Docker / User namespace
  Docker daemon running as non-root user.
  Safer but more complex to set up.

METHOD 4: Kaniko (recommended for Kubernetes)
  Builds Docker images without Docker daemon.
  Runs as a regular container (no privileges needed).
  docker run gcr.io/kaniko-project/executor:latest \
    --dockerfile Dockerfile \
    --context gs://mybucket/mycontext \
    --destination myapp:latest

METHOD 5: Buildah / Podman
  Build OCI-compatible images without Docker daemon.
  Rootless. Works in Kubernetes pods without privilege.

RECOMMENDATION:
  CI on Kubernetes: Kaniko or Buildah (no daemon, no --privileged)
  CI on VMs: Socket mount (accepted risk, good layer caching)
  Never: --privileged in production workloads
```

---

**Q80. What is the Docker security model and how do you harden a container?**

```
DOCKER DEFAULT SECURITY:
  ✓ Container process isolated via namespaces
  ✓ cgroups limit resource consumption
  ✓ Most Linux capabilities dropped by default
  ✓ Default seccomp profile blocks ~44 dangerous syscalls
  ✓ AppArmor/SELinux profiles (if enabled on host)
  
  ✗ Container runs as root by default
  ✗ Host kernel shared (container escape = host compromise)
  ✗ Docker socket is root-equivalent access to host
  ✗ No network policy enforcement by default

HARDENING CHECKLIST:

1. Run as non-root:
   USER 1001 in Dockerfile (most important single step)

2. Drop all capabilities, add only needed:
   docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp

3. Read-only filesystem:
   docker run --read-only --tmpfs /tmp myapp

4. No new privileges:
   docker run --security-opt no-new-privileges myapp
   Prevents privilege escalation via setuid binaries.

5. Limit resources:
   docker run --memory=512m --cpus=1.0 --pids-limit=100 myapp

6. Seccomp profile:
   docker run --security-opt seccomp=myapp-seccomp.json myapp
   Restrict to only needed syscalls (principle of least privilege).

7. AppArmor profile:
   docker run --security-opt apparmor=myapp-profile myapp

8. Minimal image (distroless or scratch):
   Fewer packages = fewer CVEs = smaller attack surface.

9. Scan image:
   trivy image myapp:latest
   grype myapp:latest

10. No --privileged EVER in production.
    docker run --privileged = effectively running on bare metal.

11. Rootless Docker:
    Run Docker daemon itself as non-root user.
    docker rootless mode (experimental but maturing).

12. Use Docker secrets:
    Never ENV for credentials. Use Docker secrets or external vault.
```

---

*End of Docker Interview Questions (80 questions)*
