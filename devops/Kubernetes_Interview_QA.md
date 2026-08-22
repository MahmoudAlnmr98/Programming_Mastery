# Kubernetes — Interview Questions & Answers (Premium Reference)
> 90 questions. Full answers with YAML and diagrams. Architecture, Pods, Services, Networking, Storage, Scheduling, Security, Scaling, kubectl. No stubs.

---

## Table of Contents
- [Section 1: Architecture (Q1–Q15)](#section-1-architecture)
- [Section 2: Core Objects (Q16–Q35)](#section-2-core-objects)
- [Section 3: Networking & Services (Q36–Q50)](#section-3-networking--services)
- [Section 4: Storage (Q51–Q58)](#section-4-storage)
- [Section 5: Scheduling & Resources (Q59–Q68)](#section-5-scheduling--resources)
- [Section 6: Security (Q69–Q75)](#section-6-security)
- [Section 7: Scaling & Workloads (Q76–Q82)](#section-7-scaling--workloads)
- [Section 8: kubectl & Operations (Q83–Q90)](#section-8-kubectl--operations)

---

## SECTION 1: ARCHITECTURE

---

**Q1. What are the components of the Kubernetes control plane?**

```
API SERVER (kube-apiserver):
  Central hub. ALL communication goes through the API server.
  Exposes REST API. Validates and authenticates every request.
  Reads/writes cluster state to etcd.
  Horizontally scalable for HA.

ETCD:
  Distributed, consistent key-value store.
  Single source of truth for all cluster state.
  Strong consistency via Raft consensus.
  MUST be backed up. Losing etcd = losing the cluster.
  Typically 3 or 5 replicas for HA (odd number for quorum).

SCHEDULER (kube-scheduler):
  Watches for unscheduled Pods (nodeName not set).
  Selects best node based on: resource requests, affinity/anti-affinity,
  taints/tolerations, topology spread constraints.
  Writes chosen node to Pod.spec.nodeName.
  Does NOT run the pod — kubelet does that.

CONTROLLER MANAGER (kube-controller-manager):
  Runs many control loops in one binary.
  Each controller reconciles actual state → desired state.
  Examples: Deployment controller, ReplicaSet controller,
  Node controller, Endpoints controller, Job controller.

CLOUD CONTROLLER MANAGER:
  Cloud-specific control loops (separate binary).
  Manages: LoadBalancer provisioning, Node lifecycle,
  Volume provisioning.
```

---

**Q2. What are the node components?**

```
KUBELET:
  Agent on every node. Primary node agent.
  Watches API server for Pods assigned to this node.
  Tells container runtime (containerd) to start/stop containers.
  Reports node and pod status back to API server.
  Runs liveness/readiness probes.

KUBE-PROXY:
  Implements Service networking via iptables or IPVS rules.
  Watches Service and Endpoints objects.
  Routes traffic from Service ClusterIP → Pod IPs.
  MODES:
    iptables: writes NAT rules. Default. Scales to ~5k services.
    IPVS: IP Virtual Server. Much faster at scale (10k+ services).
    eBPF (Cilium): replaces kube-proxy entirely. Best performance.

CONTAINER RUNTIME:
  Implements CRI (Container Runtime Interface).
  Pulls images, manages container lifecycle.
  containerd: most common (EKS, GKE, AKS default)
  CRI-O: OpenShift
  Docker: removed as default in K8s 1.24 (dockershim dropped)
```

---

**Q3. What is etcd and what happens if it goes down?**

```
ETCD:
  Distributed key-value store using Raft consensus.
  Stores: all K8s objects (Pods, Services, Deployments, Secrets, ConfigMaps)
          cluster state, RBAC policies, everything.
  
  Strong consistency: read always returns latest written value.
  Every change goes through Raft → majority of nodes must acknowledge.

IF ETCD GOES DOWN:
  API server cannot write new state → no changes accepted.
  kubectl commands fail or stall.
  Existing pods KEEP RUNNING (kubelet works independently).
  New pods cannot be scheduled.
  Scaling, rolling updates, self-healing all stop.
  
  Essentially: cluster is frozen in current state but still serving traffic.

HA SETUP:
  3 etcd nodes: tolerates 1 failure (quorum = 2)
  5 etcd nodes: tolerates 2 failures (quorum = 3)
  Odd numbers always: quorum = floor(N/2) + 1

BACKUP:
  ETCDCTL_API=3 etcdctl snapshot save /backup/etcd.db \
    --endpoints=https://etcd:2379 \
    --cacert=/etc/etcd/ca.crt \
    --cert=/etc/etcd/server.crt \
    --key=/etc/etcd/server.key
  
  Restore:
  etcdctl snapshot restore /backup/etcd.db --data-dir /var/lib/etcd-new
```

---

**Q4. What is the difference between a Deployment, ReplicaSet, and Pod?**

```
POD:
  Smallest deployable unit. Contains one or more containers.
  Containers in a Pod share: network namespace (same IP), volumes.
  Pods are ephemeral. You almost never create Pods directly.

REPLICASET:
  Ensures N replicas of a Pod are always running.
  Watches for pod failures → creates replacement pods.
  Selector matches pods by labels.
  You almost never create ReplicaSets directly.

DEPLOYMENT:
  Manages ReplicaSets.
  Provides: declarative updates, rolling updates, rollback.
  When you update a Deployment (e.g., new image):
    1. Creates a NEW ReplicaSet with new pod template
    2. Scales up new ReplicaSet (by rollingUpdate.maxSurge)
    3. Scales down old ReplicaSet (by rollingUpdate.maxUnavailable)
    4. Old ReplicaSet kept with 0 replicas (for rollback)

HIERARCHY:
  Deployment → manages → ReplicaSet(s) → manages → Pod(s)
  
  kubectl get rs   # see ReplicaSets
  kubectl get pods # see pods with owner ReplicaSet

ROLLBACK:
  kubectl rollout undo deployment/myapp
  → old ReplicaSet scaled back up, new one scaled to 0
  History kept (--revision-history-limit, default 10)
```

---

**Q5. How does Kubernetes achieve self-healing?**

```
MULTIPLE MECHANISMS:

1. REPLICASET CONTROLLER:
   Continuously watches pod count vs desired replicas.
   Pod deleted/crashed → creates replacement immediately.
   
2. LIVENESS PROBE:
   kubelet runs liveness check on container.
   Fails → kubelet kills container → restartPolicy triggers restart.
   restartPolicy: Always → always restart (Deployment default)
   restartPolicy: OnFailure → restart only on error exit
   Backoff: 10s, 20s, 40s, 80s, 160s, 300s (max) between restarts
   CrashLoopBackOff = container failing repeatedly, backoff accumulating.

3. NODE CONTROLLER:
   Monitors node heartbeats (Node status updates every 5s).
   Node unresponsive for node-monitor-grace-period (default 40s):
     → marks node condition = Unknown
   After pod-eviction-timeout (default 5m):
     → evicts all pods from the node
     → ReplicaSet controller re-creates them on healthy nodes.

4. SCHEDULER:
   If node fails, scheduler places new pods elsewhere.
   Pod requests + anti-affinity rules ensure spread.

5. HORIZONTAL POD AUTOSCALER:
   Scales pods based on metrics.
   Prevents overload by adding replicas before saturation.

6. POD DISRUPTION BUDGET:
   Prevents too many pods being taken down simultaneously.
   Protects availability during voluntary disruptions (node drains).
```

---

**Q6. What happens when you run `kubectl apply -f deployment.yaml`?**

```
Step-by-step:

1. kubectl reads deployment.yaml, serializes to JSON.
2. kubectl POST to API server: /apis/apps/v1/namespaces/default/deployments
3. API server: authenticates (client cert or token)
4. API server: authorizes (RBAC — can this user create Deployments here?)
5. API server: validates (schema check — required fields, types)
6. API server: runs admission webhooks (mutating: add defaults, validating: policy checks)
7. API server: writes Deployment object to etcd
8. Deployment controller (in controller-manager) detects new Deployment
9. Deployment controller creates a ReplicaSet matching the pod template
10. ReplicaSet controller detects new ReplicaSet (desired=3, actual=0)
11. ReplicaSet controller creates 3 Pod objects (no nodeName yet)
12. Scheduler detects 3 Pods with no nodeName
13. Scheduler assigns each pod to a node (writes nodeName)
14. kubelet on each node detects its assigned pods
15. kubelet instructs containerd to pull image + start containers
16. kubelet reports pod status → Running
17. Endpoints controller updates Service Endpoints (if Service exists)
18. kube-proxy updates iptables rules to include new pod IPs
```

---

**Q7. What is the difference between kubectl apply and kubectl create?**

```
kubectl create -f file.yaml:
  Creates the resource. Fails if resource already exists.
  Stores NO apply configuration annotation.
  Cannot be used for incremental updates easily.
  Use for: one-time creation, scripts where re-run = error.

kubectl apply -f file.yaml:
  Creates if not exists. Updates if exists (merge patch).
  Stores the applied configuration in an annotation:
    kubectl.kubernetes.io/last-applied-configuration
  Computes a 3-way merge: last-applied + current + new.
  Fields NOT in the YAML but in current state are preserved.
  Fields removed from YAML are deleted (if they were in last-applied).
  Use for: GitOps, CI/CD, most day-to-day operations.

kubectl replace -f file.yaml:
  Replaces the ENTIRE resource spec.
  Equivalent to: delete + create.
  Some resources can't be replaced (requires recreation).
  Fails if resource doesn't exist.

kubectl diff -f file.yaml:
  Shows what kubectl apply WOULD change (dry run + diff).
  Essential before applying in production.

RECOMMENDATION: Always use kubectl apply for declarative management.
kubectl create for: Namespaces, Secrets (simpler syntax), one-off jobs.
```

---

**Q8. What is a Namespace and when should you use one?**

```yaml
# Namespace: virtual cluster within a cluster.
# Provides: isolation of names, RBAC scope, resource quota scope.

# USE NAMESPACES FOR:
✓ Environment separation: dev, staging, production
✓ Team separation: team-a, team-b (with RBAC per namespace)
✓ Application separation: monitoring, cert-manager, ingress-nginx
✓ Resource quotas per namespace (limit what teams can use)

# DON'T USE NAMESPACES FOR:
✗ Strong security isolation (namespaces don't stop network traffic — add NetworkPolicy)
✗ Different Kubernetes versions (use separate clusters)
✗ Every single microservice (overkill — use labels)

# DEFAULT NAMESPACES:
default        → where resources go if no namespace specified
kube-system    → Kubernetes system components (coredns, kube-proxy)
kube-public    → publicly readable (cluster-info)
kube-node-lease→ node heartbeat leases (performance optimization)

# NOT NAMESPACED (cluster-scoped):
Node, PersistentVolume, ClusterRole, StorageClass, Namespace itself

# OPERATIONS:
kubectl get pods -n myns            # resources in namespace
kubectl get pods -A                 # all namespaces
kubectl config set-context --current --namespace=myns  # set default ns
kubectl create namespace production
```

---

**Q9. What is a ConfigMap vs Secret and when do you use each?**

```
CONFIGMAP:
  Stores non-sensitive configuration as key-value pairs or files.
  Stored in etcd as plain text.
  Visible to anyone with cluster read access.
  Use for: LOG_LEVEL, API_URL, feature flags, config files.

SECRET:
  Stores sensitive data: passwords, tokens, certificates.
  Stored in etcd as base64-encoded (NOT encrypted by default).
  Access controlled by RBAC (can restrict who reads secrets).
  Use for: DB passwords, API keys, TLS certs, SSH keys.
  
  IMPORTANT: base64 is NOT encryption — it's encoding.
  Enable etcd encryption at rest for true security.
  Or use External Secrets Operator to fetch from real vaults.

BOTH CAN BE USED AS:
  Environment variables:
    env.valueFrom.configMapKeyRef / secretKeyRef
  All keys as env vars:
    envFrom.configMapRef / secretRef
  Mounted files:
    volumes.configMap / volumes.secret

DIFFERENCES IN BEHAVIOR:
  ConfigMap mounted files: auto-update propagated to pods (~1min, no restart)
  Secret mounted files: also auto-updated
  Env vars: NOT auto-updated — pod must restart to get new values

SIZE LIMIT: 1MB per ConfigMap or Secret (etcd limit)

SECRET TYPES:
  Opaque              → generic (most common)
  kubernetes.io/tls   → TLS cert + key
  kubernetes.io/dockerconfigjson → registry auth
  kubernetes.io/service-account-token → auto-created for SA
```

---

**Q10. What is a liveness probe vs a readiness probe vs a startup probe?**

```
LIVENESS PROBE:
  Question: Is the container still alive? Should Kubernetes restart it?
  Failure action: restart the container (kubelet kills + restarts)
  Use for: detecting deadlocks, hung processes, memory leaks that 
           cause the app to stop responding but not crash.
  
  IMPORTANT: Never make liveness depend on external services.
  If DB is down → liveness fails → container restarts → still can't connect
  → restart loop! Liveness should only check the app itself.

READINESS PROBE:
  Question: Is the container ready to serve traffic?
  Failure action: remove from Service Endpoints (no restart, just traffic stop)
  Use for: app not ready yet (loading cache, warming up),
           app temporarily overloaded (shed load temporarily),
           dependency unavailable (DB down → stop receiving requests).
  
  CAN depend on external services.
  Pod stays running but gets no traffic until ready again.

STARTUP PROBE:
  Question: Has the application finished starting up?
  Failure action: restart container
  Until startupProbe succeeds: liveness and readiness probes are PAUSED.
  Use for: slow-starting apps (JVM with 60s warmup, DB migrations at startup).
  
  Without startupProbe: set initialDelaySeconds high on liveness (blunt instrument).
  With startupProbe: precise startup detection, aggressive liveness after startup.

PROBE METHODS:
  httpGet: HTTP GET → 200-399 = success
  tcpSocket: TCP connect → success if connection established
  exec: run command → exit 0 = success
  grpc: gRPC health check (K8s 1.24+)

COMMON MISTAKE:
  readinessProbe == livenessProbe (same check)
  These should be different endpoints with different semantics.
  /health → liveness (just "am I alive")
  /ready → readiness (am I ready AND can reach DB AND cache)
```

---

**Q11. Explain rolling updates and how to achieve zero-downtime.**

```yaml
ROLLING UPDATE (default strategy):
  Creates new pods gradually, removes old pods gradually.
  maxSurge: max extra pods above desired count during update
  maxUnavailable: max pods allowed to be unavailable during update

# ZERO-DOWNTIME CONFIGURATION:
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0    # never reduce capacity below desired
    maxSurge: 1          # add 1 extra pod, then remove 1 old

# HOW IT WORKS WITH maxUnavailable:0, maxSurge:1, replicas:3:
# Start: 3 old pods running
# Step 1: Create 1 new pod (4 total, 3 old + 1 new) → surge
# Step 2: New pod passes readinessProbe → becomes Ready
# Step 3: Terminate 1 old pod (3 total, 2 old + 1 new)
# Step 4: Repeat until all 3 are new pods

REQUIREMENTS FOR TRUE ZERO DOWNTIME:
✓ readinessProbe configured (new pod gets traffic only when ready)
✓ minReadySeconds set (optional wait after ready before counting as available)
✓ PodDisruptionBudget (protects during voluntary disruptions)
✓ App handles SIGTERM gracefully (30s drain of in-flight requests)
✓ preStop hook with sleep (allows LB to drain connections before SIGTERM):
  lifecycle:
    preStop:
      exec:
        command: ["sh", "-c", "sleep 5"]  # wait for LB to deregister
✓ terminationGracePeriodSeconds: 30+

CANARY DEPLOYMENT (manual):
  Deploy small percentage of new pods alongside old:
  # myapp-stable:  replicas: 9 (image: v1)
  # myapp-canary:  replicas: 1 (image: v2)
  # Service selects both (common label app: myapp)
  # 10% of traffic hits canary. Monitor. Scale up or rollback.
```

---

**Q12. What is a StatefulSet and when do you use it instead of a Deployment?**

```yaml
DEPLOYMENT:
  Pods are INTERCHANGEABLE.
  Random names: myapp-5d4b6f-xkj2p (pod hash)
  Random scheduling: any node
  Shared storage (all pods mount same PVC, or no persistent storage)
  All pods updated simultaneously in rolling fashion
  Use for: stateless apps, web servers, APIs

STATEFULSET:
  Pods have STABLE IDENTITY.
  Ordered names: postgres-0, postgres-1, postgres-2
  Stable DNS: postgres-0.postgres-headless.ns.svc.cluster.local
  Each pod gets its OWN PVC (via volumeClaimTemplates)
    postgres-0 always gets PVC data-postgres-0
    postgres-1 always gets PVC data-postgres-1
  Ordered creation: 0 → 1 → 2 (each ready before next starts)
  Ordered deletion: 2 → 1 → 0
  Ordered updates: one pod at a time (updateStrategy: RollingUpdate)
  Use for: databases, message queues, distributed systems needing
           stable identity (Kafka, Zookeeper, Elasticsearch, Redis Cluster)

KEY STATEFULSET REQUIREMENTS:
  1. Headless Service (clusterIP: None) for stable DNS per pod
  2. Persistent storage via volumeClaimTemplates
  3. Application must support pod identity (primary/replica roles)

WHY ORDERED IS IMPORTANT:
  PostgreSQL replication: primary (postgres-0) must start first,
  replicas (postgres-1, postgres-2) connect to postgres-0.
  If pods started randomly, replicas might try connecting before primary ready.

SCALING DOWN IS CAREFUL:
  Pods deleted in reverse order (2 → 1 → 0).
  PVCs are NOT deleted (to prevent data loss).
  Must manually delete PVCs if you want the data gone.
```

---

**Q13. What is a DaemonSet?**

```yaml
# DaemonSet: ensures exactly ONE pod runs on EVERY node (or selected nodes).
# When a new node joins: DaemonSet pod automatically created on it.
# When node removed: DaemonSet pod garbage collected.

USE CASES (must run on every node):
  Log collection agents: Fluentd, Filebeat (read /var/log from each node)
  Monitoring agents: Prometheus node-exporter (metrics per node)
  Network plugins: Calico, Cilium, Flannel (CNI — node-level networking)
  Storage agents: GlusterFS, Portworx
  Security agents: Falco, Twistlock

apiVersion: apps/v1
kind: DaemonSet
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    spec:
      hostNetwork: true       # share host network namespace
      hostPID: true           # see host processes
      tolerations:            # run on master nodes too
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        ports:
        - containerPort: 9100
          hostPort: 9100       # bind to host port
        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
      volumes:
      - name: proc
        hostPath:
          path: /proc

UPDATE STRATEGY:
  RollingUpdate (default): update one node at a time
  OnDelete: only update when pod is manually deleted

LIMITING TO SPECIFIC NODES:
  nodeSelector: { disktype: ssd }
  nodeAffinity: more expressive node selection
```

---

**Q14. What is an Ingress and how does it differ from a Service?**

```
SERVICE:
  Layer 4 load balancer (TCP/UDP).
  ClusterIP: internal only.
  NodePort: external via node IP + port.
  LoadBalancer: provisions cloud LB (one LB per service = $$$ expensive).
  No concept of hostnames, paths, or TLS termination.

INGRESS:
  Layer 7 (HTTP/HTTPS) routing.
  Single cloud LB → many services (much cheaper than LoadBalancer per service).
  Host-based routing: api.example.com → api-service
  Path-based routing: /api → api-service, /static → cdn-service
  TLS termination (HTTPS → HTTP internally).
  WebSocket, gRPC support.
  Annotations for advanced features (rate limiting, auth, rewrites).

INGRESS CONTROLLER (required):
  Ingress spec is just a declaration — needs a controller to implement it.
  nginx-ingress: most common, open source
  traefik: dynamic config, auto TLS, dashboard
  AWS ALB Controller: creates ALB per Ingress
  GCE Ingress: creates Google Cloud HTTP LB
  Istio Gateway: service mesh ingress

GATEWAY API (new standard, replacing Ingress):
  More expressive, multi-tenant, supports TCP/UDP/gRPC natively.
  HTTPRoute, GRPCRoute, TCPRoute, TLSRoute
  Separate roles: infrastructure (Gateway) vs application (Route)
  Being adopted by most ingress controllers as next-gen API.

INGRESS WITHOUT CONTROLLER = NOTHING HAPPENS.
  Ingress objects just sit in etcd — no traffic routing until controller installed.
```

---

**Q15. What is RBAC and how do you set up permissions for a Service Account?**

```yaml
# RBAC: Role-Based Access Control
# Who: Subject (User, Group, ServiceAccount)
# Can do what: Verbs (get, list, watch, create, update, patch, delete)
# On what: Resources (pods, deployments, secrets, etc.)

# Step 1: Create ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: app
automountServiceAccountToken: false   # disable auto-mount (security)

---
# Step 2: Create Role (namespace-scoped permissions)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: app
rules:
- apiGroups: [""]                  # "" = core group (pods, services, configmaps)
  resources: ["pods", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]

---
# Step 3: Bind Role to ServiceAccount
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: app
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: app
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io

---
# Step 4: Use ServiceAccount in Pod
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: true  # now mount only when needed

# VERIFY:
kubectl auth can-i list pods \
  --namespace app \
  --as system:serviceaccount:app:app-sa
# → yes (if correctly configured)

# CLUSTERROLE + CLUSTERROLEBINDING:
# For cluster-wide permissions (reading nodes, PVs, etc.)
# ClusterRole can also be bound with RoleBinding (namespaced scope)
# ClusterRoleBinding: cluster-wide scope (use minimally)
```

---

## SECTION 2: CORE OBJECTS

---

**Q16. What is a Pod and what are init containers?**

```yaml
# Pod: smallest deployable unit. Contains 1+ containers sharing network + volumes.
# All containers: same IP address, can communicate via localhost.
# All containers: can share volumes via volumeMounts.

INIT CONTAINERS:
  Run to completion BEFORE main containers start.
  Ordered: init-1 must complete before init-2 starts.
  If init container fails → pod restarts until it succeeds.
  
  USE CASES:
  ✓ Database migrations (run migrate.js before API starts)
  ✓ Config generation (fetch secrets from vault, write to shared volume)
  ✓ Wait for dependency (wait for DB to be ready before app starts)
  ✓ Permission setup (chown files that main container needs)
  ✓ Network setup (configure iptables before app)

  initContainers:
  - name: wait-for-db
    image: busybox
    command: ['sh', '-c', 
      'until nc -z db 5432; do echo waiting for db; sleep 2; done']
  
  - name: run-migrations
    image: myapp:v1
    command: ["node", "migrate.js"]
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url

SIDECAR CONTAINERS (K8s 1.29+ native, or regular containers):
  Run alongside main container throughout pod lifetime.
  Use for: log shippers, proxies (Envoy), metric collectors.
  
  # Native sidecar (K8s 1.29+):
  initContainers:
  - name: log-shipper
    image: fluentd:v1.16
    restartPolicy: Always    # makes it a sidecar (stays alive)
```

---

**Q17. What is the difference between Recreate and RollingUpdate strategies?**

```yaml
RECREATE:
  Kills ALL old pods first, THEN creates new pods.
  Downtime guaranteed (gap between old dying and new starting).
  USE WHEN:
    - Old and new versions cannot coexist (incompatible DB schema)
    - App doesn't support two versions running simultaneously
    - Stateful app that can't have duplicate instances

  strategy:
    type: Recreate

ROLLING UPDATE:
  Gradually replaces old pods with new ones.
  Configurable via maxUnavailable and maxSurge.
  Zero downtime achievable with correct configuration.
  USE WHEN:
    - Old and new versions can coexist (backward-compatible API)
    - Database migration is backward compatible
    - Most web applications and APIs

  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0    # zero-downtime: never go below desired replicas
      maxSurge: 1          # create 1 new before removing 1 old

BLUE-GREEN (not built-in, manual with two Deployments):
  Run v1 and v2 simultaneously.
  Switch Service selector from v1 to v2 (instant cutover).
  Keep v1 running for instant rollback.
  Cost: 2x resources during switchover.

CANARY (manual with labels/weights):
  Small percentage of traffic to new version.
  Monitor metrics. Gradually shift more traffic.
  Requires: multiple Deployments + weighted load balancing
  (Ingress canary annotations or service mesh like Istio).
```

---

**Q18. What are resource requests and limits? What happens when a container exceeds them?**

```yaml
resources:
  requests:
    cpu: "250m"      # 0.25 cores — used for SCHEDULING
    memory: "256Mi"  # used for SCHEDULING
  limits:
    cpu: "1000m"     # 1 core — THROTTLED if exceeded (not killed)
    memory: "512Mi"  # KILLED (OOMKilled) if exceeded

REQUESTS (scheduling):
  Scheduler only places pod on a node with enough available capacity.
  "Available" = allocatable - sum of all pod requests on that node.
  Guarantee: pod gets at least its requested resources.
  Actual node CPU = 4 cores, requests sum = 3.5 cores → scheduler won't place
  another pod with cpu request 0.6 on this node (not enough guaranteed capacity).

CPU LIMIT BEHAVIOR:
  CPU is compressible. If container tries to use more than limit:
  → throttled (slowed down via cgroups CFS quota)
  → NOT killed, just slower
  
  Controversial: CPU throttling can cause latency spikes.
  Some teams run without CPU limits (rely on requests only).

MEMORY LIMIT BEHAVIOR:
  Memory is NOT compressible. If container exceeds memory limit:
  → Linux OOM killer kills the container process
  → Container exits with code 137 (128 + 9/SIGKILL)
  → Pod status: OOMKilled
  → kubelet restarts container (per restartPolicy)

QOS CLASSES (eviction priority):
  Guaranteed: requests == limits for ALL containers → never evicted first
  Burstable:  requests < limits → evicted second
  BestEffort: no requests or limits → evicted first (under pressure)

  Under node memory pressure, BestEffort pods are killed first.
  Under severe pressure, Burstable pods are killed by memory usage.
  Guaranteed pods are almost never evicted.
```

---

**Q19. What are taints and tolerations?**

```yaml
TAINT: mark a node so that pods are NOT scheduled there by default.
  kubectl taint nodes gpu-node1 gpu=true:NoSchedule
  kubectl taint nodes db-node  dedicated=db:NoSchedule

TOLERATION: allow a specific pod to be scheduled on a tainted node.
  (Toleration doesn't ATTRACT, it just ALLOWS)

TAINT EFFECTS:
  NoSchedule:       New pods without matching toleration NOT scheduled here.
                    Existing pods NOT evicted.
  PreferNoSchedule: Scheduler tries to avoid (soft). Will schedule if no alternative.
  NoExecute:        New pods without toleration not scheduled here.
                    EXISTING pods without toleration are EVICTED.

USE CASES:
  # GPU nodes (only GPU pods should use expensive GPU nodes):
  kubectl taint nodes gpu-node1 gpu=true:NoSchedule
  # GPU pod:
  tolerations:
  - key: gpu
    operator: Equal
    value: "true"
    effect: NoSchedule
  nodeSelector:
    gpu: "true"   # also attract to gpu node (toleration alone doesn't)
  
  # Spot/preemptible nodes:
  kubectl taint nodes spot-node1 cloud.google.com/gke-spot=true:NoSchedule
  # Only fault-tolerant pods that can handle termination tolerate this.
  
  # Node maintenance:
  kubectl taint nodes node1 maintenance=true:NoExecute
  # All pods without toleration evicted within tolerationSeconds.
  # Same as kubectl drain (more controlled).

  # Control plane (master) nodes are tainted by default:
  node-role.kubernetes.io/master:NoSchedule
  # Only system pods (with toleration) run on masters.
```

---

**Q20. What is a PodDisruptionBudget and why is it important?**

```yaml
# PDB: ensures minimum availability during VOLUNTARY disruptions.
# Voluntary: node drain, cluster upgrade, kubectl delete pod.
# Involuntary: node crash (NOT protected by PDB).

apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2    # at least 2 pods must always be running
  # OR:
  # maxUnavailable: 1  # max 1 pod unavailable at any time
  selector:
    matchLabels:
      app: myapp

# EFFECT:
kubectl drain node1    # attempting to drain this node
# → Eviction API called for each pod
# → PDB check: would eviction violate minAvailable?
# → If yes: eviction BLOCKED. Drain waits.
# → If no: eviction allowed. Pod moved.

# REQUIREMENTS:
# minAvailable: 2 requires replicas >= 3 to be useful.
# With replicas=2, minAvailable=2: drain is impossible (would violate PDB).
# With replicas=3, minAvailable=2: one pod can be evicted at a time.

# COMBINED WITH ROLLING UPDATES:
# PDB protects during kubectl drain AND during Deployment rolling updates.
# Rolling update respects PDB — won't violate it during update.

# PERCENTAGE-BASED:
spec:
  minAvailable: "75%"   # at least 75% of pods must be running
  maxUnavailable: "25%" # at most 25% can be unavailable

# CHECK:
kubectl get pdb myapp-pdb
# Shows: ALLOWED-DISRUPTIONS column — how many pods can currently be disrupted.
```

---

## SECTION 3: NETWORKING & SERVICES

---

**Q36. What are the four types of Kubernetes Services?**

```yaml
CLUSTERIP (default):
  Creates a virtual IP within the cluster.
  Only accessible from within the cluster.
  DNS: myservice.namespace.svc.cluster.local
  USE: internal service-to-service communication.

NODEPORT:
  Exposes service on a static port on EVERY node (30000-32767).
  External access: <any-node-ip>:<nodePort>
  Built on top of ClusterIP (ClusterIP also created).
  USE: dev/testing, on-premises without cloud LB.

LOADBALANCER:
  Provisions a cloud load balancer (AWS ELB/ALB/NLB, GCP LB, Azure LB).
  External traffic → cloud LB → NodePort → ClusterIP → Pod.
  One cloud LB per LoadBalancer Service = expensive at scale.
  Built on top of NodePort.
  USE: production external services (prefer Ingress to share one LB).

EXTERNALNAME:
  Creates a CNAME DNS alias.
  No proxying — just DNS.
  Access external-db → resolves to mydb.example.com.
  USE: abstract external services; swap implementation without code changes.

HEADLESS (not a type, a variant):
  clusterIP: None
  DNS returns individual Pod IPs (not VIP).
  Used with StatefulSets for per-pod stable DNS.

kubectl expose deployment myapp --port=80 --target-port=3000 --type=ClusterIP
kubectl expose deployment myapp --port=80 --target-port=3000 --type=LoadBalancer
```

---

**Q37. How does Kubernetes DNS work?**

```
CoreDNS: runs as a Deployment in kube-system. Handles all cluster DNS.
Every Pod: /etc/resolv.conf points to CoreDNS ClusterIP (10.96.0.10).

DNS FORMAT:
  Service: <service>.<namespace>.svc.cluster.local
  Pod (rarely used): <pod-ip>.<namespace>.pod.cluster.local

SEARCH DOMAINS (from resolv.conf):
  search default.svc.cluster.local svc.cluster.local cluster.local
  ndots: 5

  "myservice" → tries myservice.default.svc.cluster.local → resolves!
  "myservice.other-ns" → myservice.other-ns.svc.cluster.local → resolves!
  "google.com" → has 1 dot < ndots(5) → tries search domains first, then falls back

HEADLESS SERVICE DNS:
  Returns A records for each Pod IP.
  StatefulSet pod: postgres-0.postgres-hs.default.svc.cluster.local
  postgres-1.postgres-hs.default.svc.cluster.local → different IP

CUSTOM DNS (CoreDNS ConfigMap):
  Override: add custom domains, forward specific zones to other resolvers.
  kubectl edit configmap coredns -n kube-system
  
  # Forward company.internal to internal DNS:
  company.internal:53 {
      forward . 192.168.1.100
  }

TROUBLESHOOT DNS:
  kubectl run -it --rm debug --image=busybox -- nslookup myservice
  kubectl exec -it mypod -- nslookup myservice.mynamespace
  kubectl exec -it mypod -- cat /etc/resolv.conf
```

---

**Q38. What is the difference between ClusterIP and Headless services?**

```yaml
CLUSTERIP:
  Assigns a virtual IP (VIP) from the service CIDR range.
  kube-proxy configures iptables: VIP → one of the Pod IPs (load balanced).
  All traffic hits the VIP → kube-proxy distributes to pods.
  Client sees a single stable IP. Pods are transparent.
  DNS: returns single ClusterIP.
  USE: any regular service (APIs, databases accessed normally).

HEADLESS (clusterIP: None):
  No VIP assigned.
  kube-proxy does NOTHING for this service.
  DNS: returns A records for each Pod IP directly.
  Client does its own load balancing or targeting.
  Client knows individual pod IPs.
  USE: StatefulSets (each pod has stable DNS), custom load balancing,
       service discovery where client needs all endpoints.

EXAMPLE:
  Regular Service DNS: postgres → 10.96.10.5 (VIP)
    → kube-proxy → one of [10.244.1.5, 10.244.2.3, 10.244.3.7]
  
  Headless Service DNS: postgres-headless → [10.244.1.5, 10.244.2.3, 10.244.3.7]
    → application chooses which IP to connect to

STATEFULSET + HEADLESS:
  Each pod gets a stable DNS name:
  postgres-0.postgres-headless.default.svc.cluster.local → 10.244.1.5 (always)
  postgres-1.postgres-headless.default.svc.cluster.local → 10.244.2.3 (always)
  Even if pod is rescheduled → same DNS name, new IP (DNS updates automatically).
```

---

## SECTION 4: STORAGE

---

**Q51. Explain PersistentVolume, PersistentVolumeClaim, and StorageClass.**

```yaml
PERSISTENT VOLUME (PV):
  Cluster-level storage resource (like a node is a compute resource).
  Created by admin (static) or automatically by StorageClass (dynamic).
  Has: capacity, accessModes, reclaimPolicy, storageClassName.

PERSISTENT VOLUME CLAIM (PVC):
  User request for storage (like a Pod requesting compute).
  Specifies: size, accessModes, storageClassName.
  K8s binds PVC to a matching PV (or dynamically creates one via StorageClass).
  Pod mounts the PVC.

STORAGE CLASS:
  Template for dynamic PV provisioning.
  Defines: provisioner (ebs.csi.aws.com), parameters (volume type, encryption).
  PVC requests a StorageClass → StorageClass automatically creates PV.

FLOW:
  Developer creates PVC → K8s finds matching StorageClass → 
  Provisioner (CSI driver) creates volume in cloud → PV created → 
  PVC bound to PV → Pod can mount PVC

ACCESS MODES:
  ReadWriteOnce (RWO): one node at a time (most CSI volumes: EBS, GCP PD)
  ReadOnlyMany (ROX):  many nodes, read-only
  ReadWriteMany (RWX): many nodes, read-write (needs NFS, Ceph, EFS)
  ReadWriteOncePod (RWOP): only one pod (K8s 1.22+)

RECLAIM POLICIES:
  Delete: PV and storage deleted when PVC deleted (good for disposable)
  Retain: PV kept (requires manual cleanup). Good for databases.
  Recycle: DEPRECATED. Scrub data and reuse PV.

IMPORTANT:
  StatefulSets create one PVC per pod (volumeClaimTemplates).
  Pods can reference the same PVC only if it's RWX (or same node for RWO).
  Deleting a StatefulSet does NOT delete its PVCs (data safety).
```

---

## SECTION 5: SCHEDULING & RESOURCES

---

**Q59. How does the Kubernetes scheduler work?**

```
SCHEDULING CYCLE (for each unscheduled Pod):

PHASE 1: FILTERING (eliminates unfit nodes)
  NodeName filter:    skip if Pod specifies specific node
  NodeUnschedulable: skip nodes marked unschedulable
  TaintToleration:   skip nodes with taints the pod doesn't tolerate
  NodeAffinity:      skip nodes that don't match required nodeAffinity
  PodAffinity:       skip nodes that don't satisfy required podAffinity
  PodAntiAffinity:   skip nodes that violate required antiAffinity
  Resources:         skip nodes with insufficient CPU/memory for requests
  VolumeZone:        skip nodes in wrong AZ for requested PVCs

PHASE 2: SCORING (ranks remaining nodes)
  LeastAllocated:     prefer nodes with more free resources
  BalancedAllocation: prefer nodes where CPU and memory ratios are balanced
  NodeAffinity:       higher score for preferred affinity matches
  PodAffinity:        higher score for preferred co-location
  InterPodAntiAffinity: lower score if co-location violates soft anti-affinity
  ImageLocality:      prefer nodes that already have the required image cached
  TaintToleration:    lower score for nodes with preferred-no-schedule taints
  TopologySpread:     score based on topology spread constraints

PHASE 3: SELECTION
  Highest score wins. Ties broken randomly.
  Scheduler updates Pod.spec.nodeName.

SCHEDULER PROFILES (K8s 1.18+):
  Configure which plugins run in each phase.
  Multiple schedulers possible (custom scheduler for GPU workloads).

PREEMPTION:
  High-priority pod can't fit → scheduler may evict lower-priority pods.
  PriorityClass defines pod priority (0-1000000000).
  system-cluster-critical, system-node-critical: highest (built-in).
```

---

## SECTION 6: SECURITY

---

**Q69. What is Pod Security Admission?**

```yaml
# PSA replaces PodSecurityPolicy (removed in K8s 1.25).
# Enforces security profiles at the NAMESPACE level.
# Built into API server — no controller needed.

THREE PROFILES:
  privileged: no restrictions (equivalent to no policy)
  baseline:   prevents known privilege escalations (hostPID, hostNetwork, dangerous caps)
  restricted: heavily restricted (non-root, no privilege escalation, seccomp, drop all caps)

THREE MODES (per profile):
  enforce: reject pods violating the policy
  warn:    allow but warn in API server response
  audit:   allow but record in audit log

CONFIGURE VIA NAMESPACE LABELS:
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

# RESTRICTED PROFILE: pods MUST have:
securityContext:
  runAsNonRoot: true
  runAsUser: 1000           # non-zero UID
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true   # recommended (not strictly required by restricted)
  seccompProfile:
    type: RuntimeDefault    # or Localhost
  capabilities:
    drop: ["ALL"]

# CHECK IF POD WOULD VIOLATE POLICY:
kubectl label ns myns pod-security.kubernetes.io/warn=restricted --overwrite
kubectl apply -f my-pod.yaml   # shows warnings if pod violates restricted

# THIRD-PARTY ALTERNATIVES (more powerful):
# OPA/Gatekeeper: arbitrary Rego policies
# Kyverno: YAML-based policies, easier to write
```

---

## SECTION 7: SCALING & WORKLOADS

---

**Q76. What is the Horizontal Pod Autoscaler?**

```yaml
# HPA: automatically scales Deployment/ReplicaSet replicas based on metrics.
# Checks metrics every 15s (default).
# Uses: metrics-server (CPU/memory), Prometheus Adapter (custom metrics), KEDA.

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # scale when avg CPU > 70% of request
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # wait 5min before scale down
    scaleUp:
      stabilizationWindowSeconds: 0     # scale up immediately

ALGORITHM:
  desiredReplicas = ceil(currentReplicas × (currentMetric / targetMetric))
  If currentReplicas=3, CPU=90%, target=70%:
    desiredReplicas = ceil(3 × 90/70) = ceil(3.86) = 4

REQUIREMENTS:
  ✓ containers must have resource requests set (for CPU/memory metrics)
  ✓ metrics-server installed and running
  ✓ kubectl top pods must work

HPA vs VPA (Vertical Pod Autoscaler):
  HPA: scales OUT (more replicas) — horizontal
  VPA: scales UP (bigger resources) — vertical
    Adjusts CPU/memory requests automatically based on usage history.
    Must restart pod to apply new resources (limitation).
    Not recommended to use HPA + VPA on same metric simultaneously.

# VIEW HPA STATUS:
kubectl get hpa myapp-hpa
# Shows: TARGETS (current/target), MINPODS, MAXPODS, REPLICAS
```

---

## SECTION 8: kubectl & OPERATIONS

---

**Q83. What are the most important kubectl commands?**

```bash
# CLUSTER INFO
kubectl cluster-info
kubectl get nodes -o wide           # node IPs, OS, container runtime
kubectl describe node mynode        # detailed node info (CPU/mem allocated)
kubectl top nodes                   # CPU/memory usage (needs metrics-server)

# PODS
kubectl get pods -A                 # all namespaces
kubectl get pods -n myns -o wide    # with node names and IPs
kubectl get pods --show-labels      # show all labels
kubectl get pods -l app=myapp       # label selector filter
kubectl describe pod myapp-xxx      # events, conditions, probe results
kubectl logs myapp-xxx              # container logs
kubectl logs myapp-xxx --previous   # logs from crashed container
kubectl logs myapp-xxx -c mycontainer -f   # follow, specific container
kubectl exec -it myapp-xxx -- sh    # interactive shell
kubectl exec myapp-xxx -- env       # run command
kubectl port-forward pod/myapp-xxx 8080:3000   # local port forward
kubectl cp myapp-xxx:/app/file.log ./file.log  # copy file from pod

# DEPLOYMENTS
kubectl rollout status deploy/myapp       # watch rollout
kubectl rollout history deploy/myapp      # revision history
kubectl rollout undo deploy/myapp         # rollback to previous
kubectl rollout undo deploy/myapp --to-revision=3
kubectl set image deploy/myapp app=myapp:v2   # update image (triggers rollout)
kubectl scale deploy/myapp --replicas=5
kubectl rollout pause deploy/myapp       # pause rolling update
kubectl rollout resume deploy/myapp

# RESOURCES
kubectl apply -f file.yaml          # create or update
kubectl delete -f file.yaml         # delete resources defined in file
kubectl diff -f file.yaml           # show what would change
kubectl get all -n myns             # pods, services, deployments, etc.
kubectl get events -n myns --sort-by=lastTimestamp   # recent events

# DEBUGGING
kubectl run debug --image=busybox --rm -it -- sh    # ephemeral debug pod
kubectl debug myapp-xxx -it --image=busybox         # debug sidecar
kubectl get endpoints myservice     # are pod IPs in the service?
kubectl auth can-i list pods --as=myuser             # check permissions

# OUTPUT FORMATS
kubectl get pods -o yaml            # full YAML
kubectl get pods -o json            # JSON
kubectl get pods -o jsonpath='{.items[*].metadata.name}'  # custom query
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
kubectl get pods --sort-by=.status.startTime        # sort by field

# CONTEXT & NAMESPACE
kubectl config get-contexts         # list all contexts
kubectl config use-context prod     # switch context
kubectl config set-context --current --namespace=myns  # set default namespace
```

---

**Q84. How do you debug a pod that is stuck in CrashLoopBackOff?**

```bash
# CrashLoopBackOff = container starts, crashes, K8s tries to restart,
# backoff increases: 10s → 20s → 40s → 80s → 160s → 300s (max 5min)

# STEP 1: Check exit code
kubectl describe pod myapp-xxx
# Look for: "Last State: Terminated, Reason: Error, Exit Code: X"
# Exit 1   = application error
# Exit 137 = OOMKilled (increase memory limit)
# Exit 139 = segfault (bug in app)
# Exit 143 = SIGTERM (something killed it)

# STEP 2: View logs from crashed container
kubectl logs myapp-xxx --previous   # ← KEY: logs from BEFORE the crash

# STEP 3: Describe for events
kubectl describe pod myapp-xxx
# Look in Events section for: BackOff, Pulling, OOMKilling, etc.

# STEP 4: Override entrypoint to prevent crash (explore filesystem)
kubectl run debug-pod \
  --image=myapp:v1 \
  --command -- sleep 3600   # override CMD/ENTRYPOINT with sleep
kubectl exec -it debug-pod -- sh
# Now you can manually run the app, check environment, inspect files

# STEP 5: Check resource limits
kubectl describe pod myapp-xxx | grep -A 5 "Limits:"
kubectl describe pod myapp-xxx | grep -A 5 "Requests:"

# STEP 6: Check environment variables
kubectl exec myapp-xxx -- env
# Config or secret missing? Wrong value?

# STEP 7: Check volume mounts
kubectl describe pod myapp-xxx | grep -A 10 "Volumes:"
# PVC not bound? Wrong mount path?

# COMMON CAUSES:
# Missing required env var → app exits 1
# OOMKilled → increase memory limit
# Wrong image entrypoint → exec /bin/sh: no such file
# Bad config/secret → app fails validation at startup
# Init container fails → main container never starts
# readinessProbe too aggressive → pod removed then killed
```

---

**Q85. How do you perform a rolling restart of a Deployment?**

```bash
# ROLLING RESTART (without changing image/config):
# Triggers a rolling update that replaces all pods one by one.
# Useful: pick up new ConfigMap values, force pod renewal, apply node config.

kubectl rollout restart deployment/myapp
# Adds annotation: kubectl.kubernetes.io/restartedAt: "2024-01-15T10:00:00Z"
# Triggers new ReplicaSet (same image, new pods)
# Respects: rollingUpdate.maxUnavailable, rollingUpdate.maxSurge
# Respects: PodDisruptionBudget

# WATCH PROGRESS:
kubectl rollout status deployment/myapp
# Waiting for deployment/myapp rollout to finish: 1 out of 3 updated...
# Waiting for deployment/myapp rollout to finish: 2 out of 3 updated...
# deployment "myapp" successfully rolled out

# RESTART ALL DEPLOYMENTS IN NAMESPACE:
kubectl rollout restart deployment -n myns

# RESTART STATEFULSET:
kubectl rollout restart statefulset/mydb

# RESTART DAEMONSET:
kubectl rollout restart daemonset/fluentd

# ALTERNATIVE (old way — not recommended):
kubectl set env deployment/myapp RESTART="$(date)"   # force config change
# Triggers a rollout but pollutes environment

# WHEN TO USE:
# ConfigMap or Secret updated and you want pods to pick up new values
# Node kernel updated, want pods to reschedule with fresh environment
# Debugging: force pod onto different node to isolate node issues
```

---

**Q86. What is kubectl drain vs kubectl cordon?**

```bash
# CORDON: mark node as unschedulable (no new pods scheduled here)
kubectl cordon node1
# Effect: node.spec.unschedulable = true
# Existing pods STAY running. No new pods scheduled.
# Use: temporarily prevent new workloads while node has issues.

kubectl uncordon node1   # allow scheduling again

# DRAIN: cordon + evict all pods from the node
kubectl drain node1 \
  --ignore-daemonsets \         # DaemonSet pods can't be evicted (ignore them)
  --delete-emptydir-data \      # delete pods using emptyDir volumes
  --grace-period=60 \           # give pods 60s to gracefully shutdown
  --timeout=300s                # give up after 5 minutes

# WHAT DRAIN DOES:
# 1. Cordons node (no new pods)
# 2. For each pod: calls Eviction API
# 3. Eviction API checks PodDisruptionBudget → blocks if would violate
# 4. Pod receives SIGTERM → drains → exits (or SIGKILL after grace period)
# 5. ReplicaSet/Deployment reschedules pods on other nodes

# USE CASES:
# Node maintenance (hardware, OS upgrade)
# Node decommission
# Cluster upgrade (rolling node replacement)

# FORCE (bypasses PDB — use with caution):
kubectl drain node1 --force --ignore-daemonsets
# WARNING: may violate PDB, causing service disruption

# AFTER MAINTENANCE:
kubectl uncordon node1   # re-enable scheduling

# CHECK WHICH PODS WOULD BE EVICTED:
kubectl drain node1 --ignore-daemonsets --dry-run=client
```

---

**Q87. How do you get resource usage metrics from Kubernetes?**

```bash
# REQUIRES: metrics-server installed in cluster

# NODE METRICS:
kubectl top nodes                              # all nodes
kubectl top nodes --sort-by=cpu               # sorted by CPU
kubectl top nodes --sort-by=memory

# POD METRICS:
kubectl top pods -n myns                       # all pods in namespace
kubectl top pods -A --sort-by=memory          # all namespaces, sorted
kubectl top pods -l app=myapp                 # filtered by label
kubectl top pod myapp-xxx --containers        # per-container breakdown

# METRIC SERVER STATUS:
kubectl get deployment metrics-server -n kube-system
kubectl top pods -n kube-system | grep metrics

# RESOURCE USAGE VS REQUESTS:
kubectl describe nodes | grep -A 10 "Allocated resources"
# Shows: CPU requests/limits as % of node capacity
# Shows: Memory requests/limits

# PRODUCTION MONITORING (beyond kubectl top):
# Prometheus + Grafana: cluster-level metrics, historical data, alerting
# Kubernetes Dashboard: visual overview
# Datadog/Dynatrace/New Relic: commercial APM
# Kube-state-metrics: K8s object state (pod restarts, deployment status)
# Node-exporter: OS-level metrics (disk, network, CPU steal)

# HPA CHECK:
kubectl get hpa -A                      # all HPAs
kubectl describe hpa myapp-hpa          # current/target metrics, events

# EVENTS (recent cluster activity):
kubectl get events -n myns --sort-by=lastTimestamp | tail -30
kubectl get events -A --field-selector type=Warning   # only warnings
```

---

**Q88. What is kubectl port-forward and when do you use it?**

```bash
# port-forward: tunnel traffic from localhost to a pod/service/deployment.
# No need to expose service externally.
# Useful for: debugging, accessing internal services locally.

# Forward to a specific pod:
kubectl port-forward pod/myapp-xxx 8080:3000
# localhost:8080 → pod myapp-xxx:3000

# Forward to a service (distributes to any healthy pod):
kubectl port-forward svc/myapp 8080:80
# localhost:8080 → Service myapp:80 → random pod:targetPort

# Forward to deployment (picks one pod):
kubectl port-forward deployment/myapp 8080:3000

# Multiple ports:
kubectl port-forward svc/postgres 5432:5432 8080:8080

# Bind to all interfaces (allow access from other machines on network):
kubectl port-forward --address=0.0.0.0 svc/myapp 8080:80

# COMMON USE CASES:
# Access database (postgres:5432) without exposing it externally
# Access internal admin UI (grafana, kibana)
# Debug API that only has ClusterIP
# Test service before creating an Ingress

# Note: port-forward is NOT for production traffic.
# Single connection, no load balancing, breaks if pod restarts.
# For production: use Service (ClusterIP/LB) or Ingress.

# USEFUL COMBINATION (port-forward + psql):
kubectl port-forward svc/postgres 5432:5432 &
psql -h localhost -U user -d mydb
# ^ connects to K8s postgres through the tunnel
```

---

**Q89. How do you manage multiple Kubernetes clusters with kubectl?**

```bash
# KUBECONFIG: configuration file with cluster, user, and context info.
# Default: ~/.kube/config
# Multiple files: KUBECONFIG=/path/a:/path/b kubectl ...

# CONTEXT: combination of cluster + user + namespace
kubectl config get-contexts            # list all contexts
kubectl config current-context         # show active context
kubectl config use-context prod-cluster  # switch context

# VIEW CONFIG:
kubectl config view                    # merged kubeconfig
kubectl config view --minify           # current context only

# ADD A CLUSTER (example: EKS):
aws eks update-kubeconfig --name my-cluster --region us-east-1
# Adds context to ~/.kube/config

# ADD CLUSTER MANUALLY:
kubectl config set-cluster mycluster \
  --server=https://api.mycluster.com \
  --certificate-authority=/path/to/ca.crt

kubectl config set-credentials myuser \
  --client-certificate=/path/to/client.crt \
  --client-key=/path/to/client.key

kubectl config set-context mycontext \
  --cluster=mycluster \
  --user=myuser \
  --namespace=default

# MERGE CONFIGS:
KUBECONFIG=~/.kube/config:~/new-cluster.yaml kubectl config view --flatten > merged.yaml

# NAMESPACE SWITCHING:
kubectl config set-context --current --namespace=production

# TOOLS FOR MULTI-CLUSTER:
# kubectx / kubens: fast context/namespace switching (brew install kubectx)
# k9s: terminal UI for K8s (visual, multi-cluster)
# Lens: GUI K8s IDE
# Rancher: multi-cluster management platform
# ArgoCD: GitOps, manages multiple clusters from one control plane
```

---

**Q90. What is the difference between kubectl delete and kubectl drain?**

```bash
# kubectl delete pod myapp-xxx:
  Immediately deletes the Pod object from API server.
  kubelet gets notified → sends SIGTERM → waits terminationGracePeriodSeconds → SIGKILL.
  Pod is GONE. If owned by ReplicaSet/Deployment → immediately replaced.
  Use for: quickly kill a specific misbehaving pod, force pod restart.

# kubectl drain node1:
  Cordons node (prevents new scheduling).
  Uses Eviction API to gracefully remove pods one by one.
  Respects PodDisruptionBudgets (won't violate minAvailable).
  Each pod gets terminationGracePeriodSeconds to shut down.
  Waits for each eviction to complete before next.
  Use for: node maintenance (you want ALL pods moved, safely).

EVICTION API vs DELETE:
  kubectl delete pod: bypasses PDB (pod is deleted immediately)
  Eviction API: checks PDB → rejects if violating → kubectl drain waits
  
  # Equivalent to drain's per-pod eviction:
  kubectl create -f eviction.json   # proper eviction that respects PDB

GRACEFUL TERMINATION PROCESS (both delete and drain):
  1. Pod status → Terminating
  2. Endpoints controller removes pod from Service (no more traffic)
  3. preStop hook runs (if defined) — add sleep here to drain connections
  4. SIGTERM sent to PID 1
  5. App shuts down (finish in-flight requests)
  6. After terminationGracePeriodSeconds: SIGKILL (if not exited)
  7. Volumes unmounted, pod object deleted from etcd

FORCE DELETE (emergency only):
  kubectl delete pod myapp-xxx --force --grace-period=0
  → Immediately removes pod from API server WITHOUT waiting for shutdown
  → Pod may still be running on node (kubelet catches up)
  → Risk: data corruption for stateful apps
  → Use only when pod is truly stuck and you've exhausted other options
```

---

*End of Kubernetes Interview Questions (90 questions)*
