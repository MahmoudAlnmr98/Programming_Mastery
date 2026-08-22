# The Complete Kubernetes Mastery Guide
> Architecture, core objects, scheduling, networking, storage, security, scaling, and production operations. First principles to production.

---

## Table of Contents
1. [Architecture — Control Plane & Node Components](#chapter-1-architecture)
2. [Core Objects — Pods, Deployments, Services](#chapter-2-core-objects)
3. [Configuration — ConfigMaps, Secrets, Environment](#chapter-3-configuration)
4. [Storage — PV, PVC, StorageClass](#chapter-4-storage)
5. [Networking — Services, Ingress, DNS, Network Policy](#chapter-5-networking)
6. [Scheduling — Node Selectors, Affinity, Taints & Tolerations](#chapter-6-scheduling)
7. [Scaling — HPA, VPA, KEDA, Cluster Autoscaler](#chapter-7-scaling)
8. [Workload Types — StatefulSets, DaemonSets, Jobs, CronJobs](#chapter-8-workloads)
9. [Security — RBAC, PSA, NetworkPolicy, ServiceAccounts](#chapter-9-security)
10. [Observability — Probes, Metrics, Logging](#chapter-10-observability)
11. [Helm & Kustomize](#chapter-11-helm--kustomize)
12. [Production Operations & Troubleshooting](#chapter-12-production)

---

## Chapter 1: Architecture

### 1.1 The Big Picture

```
KUBERNETES = automated container orchestration platform.
Manages: scheduling, scaling, self-healing, networking, storage, config.

CLUSTER:
  Control Plane (master): makes decisions about the cluster
  Worker Nodes: run your application containers (Pods)

  ┌─────────────────────────────────────────────────────────┐
  │                    CONTROL PLANE                        │
  │  ┌─────────────┐  ┌──────────┐  ┌──────────────────┐  │
  │  │ API Server  │  │ etcd     │  │ Scheduler        │  │
  │  │ (kube-api)  │  │          │  │ (kube-scheduler)  │  │
  │  └─────────────┘  └──────────┘  └──────────────────┘  │
  │  ┌─────────────────────────────────────────────────┐    │
  │  │ Controller Manager (kube-controller-manager)    │    │
  │  └─────────────────────────────────────────────────┘    │
  └─────────────────────────────────────────────────────────┘
           │ watches & acts on cluster state
           ▼
  ┌──────────────────────┐   ┌──────────────────────┐
  │   WORKER NODE 1      │   │   WORKER NODE 2      │
  │  ┌───────────────┐   │   │  ┌───────────────┐   │
  │  │  kubelet      │   │   │  │  kubelet      │   │
  │  │  kube-proxy   │   │   │  │  kube-proxy   │   │
  │  │  containerd   │   │   │  │  containerd   │   │
  │  └───────────────┘   │   │  └───────────────┘   │
  │  [Pod][Pod][Pod]      │   │  [Pod][Pod]          │
  └──────────────────────┘   └──────────────────────┘
```

### 1.2 Control Plane Components

```
API SERVER (kube-apiserver):
  The gateway to the cluster. ALL communication goes through here.
  Exposes REST API. Validates, authenticates, authorizes requests.
  Writes state to etcd. Notifies controllers of changes.
  Horizontally scalable (multiple replicas for HA).

ETCD:
  Distributed, consistent key-value store.
  Single source of truth — all cluster state lives here.
  Strong consistency via Raft consensus protocol.
  Must be backed up! Losing etcd = losing all cluster state.
  Typically: 3 or 5 replicas for HA (odd number for quorum).

SCHEDULER (kube-scheduler):
  Watches for unscheduled Pods (no nodeName set).
  Selects the best node based on:
    - Resource requests (CPU/memory) vs node capacity
    - Node selectors, affinity/anti-affinity rules
    - Taints and tolerations
    - Pod topology spread constraints
    - Custom scheduler plugins
  Writes chosen node to Pod.spec.nodeName.
  Does NOT run the pod — that's kubelet's job.

CONTROLLER MANAGER (kube-controller-manager):
  Runs many control loops (controllers) in one binary.
  Each controller watches for desired state vs actual state.
  Examples:
    Deployment controller: ensures correct number of ReplicaSet pods
    ReplicaSet controller: ensures correct number of Pod replicas
    Node controller: monitors node health, evicts pods from failed nodes
    Service controller: creates load balancers for LoadBalancer services
    Job controller: manages batch job completion

CLOUD CONTROLLER MANAGER:
  Cloud-specific control loops (separate from core).
  Manages: LoadBalancer provisioning, Node lifecycle (cloud instances),
           Routes (cloud networking), Volume provisioning.
```

### 1.3 Node Components

```
KUBELET:
  Agent running on every node. Primary node agent.
  Watches API server for Pods assigned to this node.
  Tells container runtime (containerd) to start/stop containers.
  Reports node and pod status back to API server.
  Runs probes (liveness, readiness, startup).
  Does NOT manage containers not created by Kubernetes.

KUBE-PROXY:
  Implements Kubernetes Service networking on each node.
  Maintains iptables (or IPVS) rules for Service → Pod routing.
  Load balances traffic across Pod endpoints.
  Watches Service and Endpoint objects.

  MODES:
    iptables (default): writes iptables DNAT rules. Scales poorly at 10k+ services.
    IPVS: uses Linux IPVS (IP Virtual Server). Much better performance at scale.
          Multiple load balancing algorithms: rr, lc, dh, sh, sed, nq.
    eBPF (via Cilium): replaces kube-proxy entirely. Best performance.

CONTAINER RUNTIME:
  Implements CRI (Container Runtime Interface).
  Pulls images, manages container lifecycle.
  containerd: most common (used by most managed K8s: EKS, GKE, AKS)
  CRI-O: lightweight, used by OpenShift
  Docker: was supported until K8s 1.24 (dockershim removed)
```

### 1.4 How a Pod Gets Scheduled — Step by Step

```
User: kubectl apply -f pod.yaml

1. kubectl → API server (HTTPS REST POST /api/v1/pods)
2. API server: authenticate, authorize (RBAC), validate schema
3. API server: write Pod object to etcd (status: Pending, no nodeName)
4. Scheduler: detects new Pod with no nodeName (watching etcd via API server)
5. Scheduler: filter nodes (node selectors, taints, resources)
   → score remaining nodes (spread, affinity, resource usage)
   → pick best node
6. Scheduler: PATCH Pod.spec.nodeName = "node-2" in API server → etcd
7. kubelet on node-2: detects Pod assigned to it (watches API server)
8. kubelet: instructs containerd to pull image if not cached
9. containerd: pulls image, creates container
10. kubelet: starts container, sets up volumes, env vars
11. kubelet: starts liveness/readiness probes
12. kubelet: updates Pod status → API server → etcd
13. kube-proxy: updates iptables rules when Pod becomes Ready
    (Endpoints object updated → Service starts routing to new Pod)
```

---

## Chapter 2: Core Objects

### 2.1 Pod

```yaml
# A Pod is the smallest deployable unit in Kubernetes.
# Contains one or more containers sharing: network namespace, storage volumes.
# All containers in a Pod have the same IP address, can communicate via localhost.

apiVersion: v1
kind: Pod
metadata:
  name: myapp
  namespace: default
  labels:
    app: myapp
    version: v1
  annotations:
    description: "Main application pod"
spec:
  containers:
  - name: app
    image: myapp:v1.2.3
    ports:
    - containerPort: 3000
      protocol: TCP
    
    # Resource requests (scheduling) and limits (enforcement)
    resources:
      requests:
        cpu: "250m"     # 0.25 cores (scheduling guarantee)
        memory: "256Mi"
      limits:
        cpu: "1000m"    # 1 core max
        memory: "512Mi" # 512MB max (OOMKilled if exceeded)
    
    # Environment
    env:
    - name: NODE_ENV
      value: "production"
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    envFrom:
    - configMapRef:
        name: app-config
    
    # Probes
    livenessProbe:
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 30
      periodSeconds: 10
      failureThreshold: 3
    
    readinessProbe:
      httpGet:
        path: /ready
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 5
    
    # Volume mounts
    volumeMounts:
    - name: config
      mountPath: /app/config
      readOnly: true
    - name: data
      mountPath: /app/data
  
  # Sidecar container (e.g., log shipper)
  - name: log-shipper
    image: fluentd:v1.16
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  
  # Init containers — run to completion BEFORE main containers start
  initContainers:
  - name: db-migrate
    image: myapp:v1.2.3
    command: ["node", "migrate.js"]
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
  
  volumes:
  - name: config
    configMap:
      name: app-config
  - name: data
    persistentVolumeClaim:
      claimName: app-data-pvc
  - name: logs
    emptyDir: {}
  
  # Pod-level settings
  restartPolicy: Always        # Always | OnFailure | Never
  terminationGracePeriodSeconds: 30
  serviceAccountName: app-sa
  
  # Node placement
  nodeSelector:
    kubernetes.io/arch: amd64

# POD LIFECYCLE:
# Pending → Running → Succeeded/Failed
# ContainerCreating → PodInitializing → Running
# Terminating: SIGTERM → grace period → SIGKILL
```

### 2.2 Deployment

```yaml
# Deployment manages a ReplicaSet which manages Pods.
# Provides: declarative updates, rolling updates, rollback.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: default
  labels:
    app: myapp
spec:
  replicas: 3
  
  selector:
    matchLabels:
      app: myapp       # selects pods with this label
  
  # Update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1    # max pods unavailable during update (abs or %)
      maxSurge: 1          # max extra pods during update (abs or %)
      # maxUnavailable: 0 + maxSurge: 1 → zero-downtime (always full capacity)
  
  template:             # Pod template
    metadata:
      labels:
        app: myapp      # MUST match selector.matchLabels
        version: v1
    spec:
      containers:
      - name: app
        image: myapp:v1.2.3
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          periodSeconds: 10
      
      # Pod Disruption Budget ensures minimum availability during voluntary disruptions
      # (node drains, cluster upgrades)

# DEPLOYMENT OPERATIONS:
# kubectl apply -f deployment.yaml          → apply changes
# kubectl set image deploy/myapp app=myapp:v2  → update image (rolling)
# kubectl rollout status deploy/myapp       → watch rollout progress
# kubectl rollout history deploy/myapp      → see revision history
# kubectl rollout undo deploy/myapp         → rollback to previous
# kubectl rollout undo deploy/myapp --to-revision=3  → specific revision
# kubectl scale deploy/myapp --replicas=5   → scale manually
# kubectl rollout pause deploy/myapp        → pause rollout
# kubectl rollout resume deploy/myapp       → resume

# RECREATE STRATEGY (for incompatible schema changes):
# strategy:
#   type: Recreate  # kill all old pods, then create new ones — downtime!
```

### 2.3 Services

```yaml
# Service = stable virtual IP (ClusterIP) for a set of Pods.
# Pods come and go (new IPs), Service IP is stable.
# Service → kube-proxy iptables rules → Pod IP routing.

---
# ClusterIP (default) — internal cluster access only
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp            # routes to pods with this label
  ports:
  - port: 80              # port exposed by Service
    targetPort: 3000      # port on the Pod
    protocol: TCP
  # ClusterIP assigned automatically (or set explicitly)

---
# NodePort — exposes on every node's IP at a static port
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
    nodePort: 30080      # 30000-32767 range. External: nodeIP:30080

---
# LoadBalancer — provisions cloud load balancer
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000

---
# ExternalName — DNS alias to external service
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: mydb.example.com  # CNAME in cluster DNS

---
# Headless Service — no ClusterIP, returns Pod IPs directly
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
spec:
  clusterIP: None         # headless
  selector:
    app: myapp
  ports:
  - port: 3000
# DNS returns: list of Pod IPs (used by StatefulSets for stable DNS per pod)
# myapp-0.myapp-headless.default.svc.cluster.local
```

---

## Chapter 3: Configuration

### 3.1 ConfigMaps

```yaml
# ConfigMap: store non-sensitive configuration data.

apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Key-value pairs (env vars)
  LOG_LEVEL: "info"
  API_URL: "https://api.example.com"
  
  # File content (mounted as file)
  nginx.conf: |
    server {
      listen 80;
      location / {
        proxy_pass http://localhost:3000;
      }
    }
  
  config.json: |
    {
      "debug": false,
      "timeout": 30
    }

# USE AS ENVIRONMENT VARIABLES:
env:
- name: LOG_LEVEL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: LOG_LEVEL

# USE ALL KEYS AS ENV VARS:
envFrom:
- configMapRef:
    name: app-config

# USE AS MOUNTED FILE:
volumes:
- name: config-vol
  configMap:
    name: app-config
    items:
    - key: nginx.conf
      path: nginx.conf     # mounted at /etc/nginx/nginx.conf (with mountPath)

volumeMounts:
- name: config-vol
  mountPath: /etc/nginx
  readOnly: true

# NOTE: ConfigMap changes to mounted files are eventually reflected in pods
# (without restart — ~1min propagation).
# ConfigMap changes to env vars: require pod restart.
```

### 3.2 Secrets

```yaml
# Secret: store sensitive data (passwords, tokens, certs).
# Base64 encoded (NOT encrypted by default in etcd!).
# Enable etcd encryption at rest for true security.

apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque           # generic key-value secret
data:
  password: cGFzc3dvcmQxMjM=   # base64("password123")
  username: dXNlcg==           # base64("user")
stringData:            # plain text (base64'd automatically)
  url: "postgres://user:password123@db:5432/myapp"

# SECRET TYPES:
# Opaque              → generic (most common)
# kubernetes.io/tls   → TLS certificate and key
# kubernetes.io/dockerconfigjson → registry credentials
# kubernetes.io/service-account-token → SA tokens (auto-created)

# TLS SECRET:
kubectl create secret tls myapp-tls \
  --cert=tls.crt \
  --key=tls.key

# REGISTRY SECRET (for private images):
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.io \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=user@example.com
# Use in Pod:
imagePullSecrets:
- name: regcred

# USE AS ENV VAR:
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password

# USE AS MOUNTED FILE:
volumes:
- name: db-secret-vol
  secret:
    secretName: db-secret
    defaultMode: 0400   # read-only by owner
volumeMounts:
- name: db-secret-vol
  mountPath: /secrets
  readOnly: true

# EXTERNAL SECRET MANAGERS (production best practice):
# External Secrets Operator: syncs secrets from AWS Secrets Manager / Vault / GCP SM
# Vault Agent Injector: injects Vault secrets as sidecar
# Sealed Secrets: encrypted secrets safe to store in git
```

---

## Chapter 4: Storage

### 4.1 Persistent Volumes

```yaml
# PersistentVolume (PV): cluster-level storage resource (like a node is a compute resource)
# PersistentVolumeClaim (PVC): user request for storage (like a Pod requests compute)
# StorageClass: defines how PVs are dynamically provisioned

# STATIC PROVISIONING (admin creates PV):
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce           # RWO: one node at a time
  # ReadOnlyMany (ROX)     : many nodes, read-only
  # ReadWriteMany (RWX)    : many nodes, read-write (needs NFS/Ceph)
  # ReadWriteOncePod (RWOP): only one pod (K8s 1.22+)
  persistentVolumeReclaimPolicy: Retain   # Retain | Delete | Recycle
  storageClassName: ""     # empty = no storage class
  hostPath:                # local path (dev/testing only)
    path: /data/my-pv

---
# PersistentVolumeClaim (user):
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: gp3   # requests dynamic provisioning

---
# DYNAMIC PROVISIONING (StorageClass creates PV automatically):
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
reclaimPolicy: Delete       # delete PV when PVC deleted
allowVolumeExpansion: true  # allow PVC resize
volumeBindingMode: WaitForFirstConsumer  # don't provision until pod scheduled
                                         # ensures same AZ as pod

# USE IN POD:
volumes:
- name: data
  persistentVolumeClaim:
    claimName: my-pvc
volumeMounts:
- name: data
  mountPath: /data

# RECLAIM POLICIES:
# Retain: PV kept after PVC deleted (manual cleanup). Good for databases.
# Delete: PV and underlying storage deleted when PVC deleted. Good for ephemeral.
# Recycle: DEPRECATED. Scrub and make available. Use dynamic provisioning instead.
```

---

## Chapter 5: Networking

### 5.1 Ingress

```yaml
# Ingress: HTTP/HTTPS routing from external to internal services.
# Requires an Ingress Controller (nginx-ingress, traefik, AWS ALB, etc.)

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx        # which ingress controller
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls         # TLS secret (cert-manager auto-fills)
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /static
        pathType: Prefix
        backend:
          service:
            name: static-service
            port:
              number: 80
  - host: admin.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: admin-service
            port:
              number: 80

# INGRESS vs GATEWAY API:
# Gateway API (newer): more expressive, multi-team, standardized
# HTTPRoute, GRPCRoute, TCPRoute, TLSRoute resources
# Replacing Ingress for new deployments
```

### 5.2 Network Policy

```yaml
# NetworkPolicy: firewall rules for Pod-to-Pod communication.
# Default (no NetworkPolicy): all pods can talk to all pods.
# NetworkPolicy: whitelist — only explicitly allowed traffic passes.
# Requires CNI that supports NetworkPolicy (Calico, Cilium, Weave).

# DENY ALL ingress to app namespace (start with deny-all):
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: app
spec:
  podSelector: {}    # selects ALL pods in namespace
  policyTypes:
  - Ingress
  - Egress
  # No ingress/egress rules = deny all

---
# Allow API pods to receive traffic only from nginx pods:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-nginx-to-api
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx
    ports:
    - protocol: TCP
      port: 3000

---
# Allow API pods to reach DB and external DNS only:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-egress
  namespace: app
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: db
    ports:
    - port: 5432
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - port: 53    # DNS
      protocol: UDP
    - port: 53
      protocol: TCP
```

### 5.3 Kubernetes DNS

```
CoreDNS runs as a Deployment in kube-system namespace.
Every Pod gets DNS configured to point to CoreDNS ClusterIP.

DNS NAMING SCHEME:
  Pod:     pod-ip.namespace.pod.cluster.local  (rarely used)
  Service: <service>.<namespace>.svc.cluster.local

  Short names (resolved automatically by search domains):
    myservice                     → within same namespace
    myservice.other-ns            → across namespaces
    myservice.other-ns.svc.cluster.local → fully qualified

EXAMPLES:
  db.default.svc.cluster.local        → ClusterIP of db service in default ns
  redis.cache.svc.cluster.local       → redis in cache namespace
  myapp-0.myapp.default.svc.cluster.local  → StatefulSet pod-specific DNS

  # Inside a pod, ping to "db" → CoreDNS → db.default.svc.cluster.local → ClusterIP

HEADLESS SERVICE DNS:
  Returns A records for each Pod IP (not a single ClusterIP).
  Used by StatefulSets for stable per-pod DNS.
  myapp-0.myapp-headless.default.svc.cluster.local → Pod 0's IP
  myapp-1.myapp-headless.default.svc.cluster.local → Pod 1's IP

ndots setting (/etc/resolv.conf):
  search default.svc.cluster.local svc.cluster.local cluster.local
  ndots: 5   → if name has < 5 dots, try search domains first
  Performance tip: use fully qualified names (trailing dot) for external DNS
  to avoid unnecessary search domain lookups.
```

---

## Chapter 6: Scheduling

### 6.1 Resource Requests and Limits

```yaml
resources:
  requests:
    cpu: "250m"       # 0.25 cores — used for SCHEDULING (guarantee)
    memory: "256Mi"   # used for SCHEDULING
  limits:
    cpu: "1000m"      # 1 core — throttled if exceeded (not killed)
    memory: "512Mi"   # killed (OOMKilled) if exceeded

# requests = what the scheduler uses to decide placement
# limits = what the kernel enforces at runtime

# CPU BEHAVIOR:
# cpu request: guaranteed CPU share (cgroups cpu.shares)
# cpu limit: throttled via cgroups cpu.cfs_quota_us — never killed for CPU

# MEMORY BEHAVIOR:
# memory request: soft guarantee — scheduling hint
# memory limit: hard limit — process killed (OOMKilled exit 137) if exceeded

# QUALITY OF SERVICE CLASSES:
# Guaranteed: requests == limits for ALL containers → highest priority
# Burstable:  requests < limits for at least one container → medium priority
# BestEffort: no requests or limits → lowest priority (first evicted)

# NAMESPACE RESOURCE QUOTAS:
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ns-quota
  namespace: app
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "100"
    services: "20"

# LIMIT RANGES (defaults and limits per container):
apiVersion: v1
kind: LimitRange
metadata:
  name: container-limits
  namespace: app
spec:
  limits:
  - type: Container
    default:          # applied if container doesn't specify limits
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:   # applied if container doesn't specify requests
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
```

### 6.2 Affinity and Anti-Affinity

```yaml
spec:
  affinity:
    # NODE AFFINITY — prefer or require specific nodes
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:  # HARD rule (must match)
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values: ["us-east-1a", "us-east-1b"]
      
      preferredDuringSchedulingIgnoredDuringExecution:  # SOFT rule (prefer)
      - weight: 100
        preference:
          matchExpressions:
          - key: node-type
            operator: In
            values: ["compute-optimized"]
    
    # POD ANTI-AFFINITY — spread replicas across nodes/zones
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: myapp   # don't place on node that already has myapp pod
          topologyKey: kubernetes.io/hostname   # "spread across nodes"
    
    # POD AFFINITY — co-locate with other pods (e.g., co-locate cache with app)
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: redis-sidecar
        topologyKey: kubernetes.io/hostname

# TOPOLOGY SPREAD CONSTRAINTS (preferred over anti-affinity for even spread):
topologySpreadConstraints:
- maxSkew: 1                             # max difference between zones
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule      # or ScheduleAnyway
  labelSelector:
    matchLabels:
      app: myapp
```

### 6.3 Taints and Tolerations

```yaml
# TAINT: mark a node to repel Pods (unless Pod tolerates it)
kubectl taint nodes node1 gpu=true:NoSchedule
kubectl taint nodes node1 maintenance=true:NoExecute  # evicts existing pods too

# TAINT EFFECTS:
# NoSchedule:   new pods not scheduled here (existing pods stay)
# PreferNoSchedule: avoid scheduling here (soft version)
# NoExecute:    new pods not scheduled + existing pods evicted (unless tolerated)

# TOLERATION: allow a Pod to be scheduled on a tainted node
spec:
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
  
  - key: "maintenance"
    operator: "Exists"    # tolerate any value for this key
    effect: "NoExecute"
    tolerationSeconds: 3600  # only tolerate for 1 hour, then evicted
  
  # Tolerate any taint (NOT recommended in production):
  - operator: "Exists"

# COMMON USE CASES:
# Dedicated GPU nodes: taint nodes, only GPU pods tolerate
# Spot/preemptible nodes: taint, only fault-tolerant pods tolerate
# Master/control plane nodes: NoSchedule by default (don't run workloads)
# Node maintenance: NoExecute to drain and migrate pods
```

---

## Chapter 7: Scaling

### 7.1 Horizontal Pod Autoscaler (HPA)

```yaml
# HPA automatically scales Deployment replicas based on metrics.
# Default metric: CPU utilization.
# Custom metrics: via metrics-server, Prometheus Adapter.

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
  # CPU-based:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # scale when avg CPU > 70% of requests
  
  # Memory-based:
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 400Mi
  
  # Custom metric (from Prometheus via adapter):
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  
  # External metric (SQS queue depth, etc.):
  - type: External
    external:
      metric:
        name: sqs_messages_visible
        selector:
          matchLabels:
            queue: myapp-queue
      target:
        type: Value
        value: "500"
  
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # wait 5min before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60    # scale down max 50% per minute
    scaleUp:
      stabilizationWindowSeconds: 0    # scale up immediately
      policies:
      - type: Pods
        value: 4
        periodSeconds: 60    # scale up max 4 pods per minute

# REQUIREMENTS:
# - containers must have resource requests (for CPU/memory metrics)
# - metrics-server must be installed in cluster
# kubectl top pods  # verify metrics-server works
```

### 7.2 Cluster Autoscaler & KEDA

```
CLUSTER AUTOSCALER:
  Automatically adds or removes NODES from the cluster.
  Watches for pods that can't be scheduled (insufficient resources) → add node.
  Watches for underutilized nodes → remove node (drain + delete).
  
  Works with cloud providers: AWS ASG, GCP MIG, Azure VMSS.
  
  Configured via cluster-autoscaler deployment.
  Key settings:
    --scale-down-utilization-threshold=0.5    → remove if < 50% utilized
    --scale-down-delay-after-add=10m          → wait 10m after adding before removing
    --skip-nodes-with-local-storage=true      → don't remove nodes with PVs

KEDA (Kubernetes Event-Driven Autoscaling):
  Scales Deployments/Jobs to ZERO based on external event sources.
  Works with: Kafka lag, RabbitMQ queue depth, SQS, Redis lists, cron, etc.
  Extends HPA — adds event-driven scalers.

  apiVersion: keda.sh/v1alpha1
  kind: ScaledObject
  metadata:
    name: myapp-scaler
  spec:
    scaleTargetRef:
      name: myapp
    minReplicaCount: 0         # can scale to ZERO (HPA minimum is 1)
    maxReplicaCount: 100
    triggers:
    - type: rabbitmq
      metadata:
        queueName: tasks
        queueLength: "10"      # target: 10 messages per replica
        host: amqp://rabbitmq:5672
    - type: kafka
      metadata:
        bootstrapServers: kafka:9092
        consumerGroup: mygroup
        topic: mytopic
        lagThreshold: "50"

  SCALE TO ZERO:
    Workers idle when queue is empty → 0 replicas → zero cost.
    First message arrives → scales from 0 → 1+ within seconds.
```

---

## Chapter 8: Workload Types

### 8.1 StatefulSet

```yaml
# StatefulSet: manages stateful applications (databases, distributed systems).
# Provides: stable network identity, stable storage, ordered deployment/scaling.

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless   # headless service for DNS
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: pg-secret
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  
  # VolumeClaimTemplates: creates one PVC per pod (stable, named)
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: gp3
      resources:
        requests:
          storage: 20Gi

# WHAT STATEFULSET PROVIDES:
# Stable hostname: postgres-0, postgres-1, postgres-2 (predictable)
# Stable DNS: postgres-0.postgres-headless.default.svc.cluster.local
# Stable storage: postgres-0 always gets same PVC (data-postgres-0)
# Ordered: pods created 0→1→2, deleted 2→1→0
# Ordered updates: one pod at a time (updateStrategy: RollingUpdate)

# HEADLESS SERVICE (required for StatefulSet DNS):
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None      # headless
  selector:
    app: postgres
  ports:
  - port: 5432
```

### 8.2 DaemonSet, Jobs, and CronJobs

```yaml
# DAEMONSET: runs one pod on every node (or selected nodes)
# Use for: log agents, monitoring agents, network plugins, storage daemons
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule              # also run on master nodes
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log

---
# JOB: runs pods to completion (batch processing)
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  completions: 1            # number of successful completions needed
  parallelism: 1            # pods running in parallel
  backoffLimit: 4           # retry on failure up to 4 times
  activeDeadlineSeconds: 300  # kill job after 5 minutes
  template:
    spec:
      restartPolicy: OnFailure   # Never | OnFailure (not Always)
      containers:
      - name: migrate
        image: myapp:v1.2.3
        command: ["node", "migrate.js"]

---
# CRONJOB: scheduled jobs (like cron)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-report
spec:
  schedule: "0 2 * * *"        # 2am daily (cron syntax)
  concurrencyPolicy: Forbid    # Allow | Forbid | Replace
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 300  # if missed, allow start within 5min
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: report
            image: myapp:v1.2.3
            command: ["node", "generate-report.js"]
```

---

## Chapter 9: Security

### 9.1 RBAC

```yaml
# RBAC: Role-Based Access Control
# Subjects: Users, Groups, ServiceAccounts
# Verbs: get, list, watch, create, update, patch, delete
# Resources: pods, deployments, services, secrets, etc.

# ROLE (namespace-scoped):
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: app
rules:
- apiGroups: [""]             # "" = core API group
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["app-secret"]  # restrict to specific named resource

# ROLEBINDING: attach Role to Subject
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: app
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: app
- kind: User
  name: "alice@example.com"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io

# CLUSTERROLE + CLUSTERROLEBINDING: cluster-wide permissions
# Use for: cluster admins, viewing all namespaces, node management

# SERVICE ACCOUNT (for pods to call K8s API):
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: app
automountServiceAccountToken: false  # disable auto-mount (security: opt-in)
# Mount only when needed:
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: true

# CHECK PERMISSIONS:
kubectl auth can-i list pods --namespace app --as system:serviceaccount:app:app-sa
kubectl auth can-i create deployments --namespace app --as alice@example.com
```

### 9.2 Pod Security Admission (PSA)

```yaml
# PSA replaces deprecated PodSecurityPolicy (K8s 1.25+)
# Enforced at namespace level via labels
# Three profiles: privileged, baseline, restricted

# Apply to namespace (labels):
apiVersion: v1
kind: Namespace
metadata:
  name: app
  labels:
    pod-security.kubernetes.io/enforce: restricted    # enforce strict rules
    pod-security.kubernetes.io/warn: restricted       # warn in logs
    pod-security.kubernetes.io/audit: restricted      # audit log violations

# RESTRICTED PROFILE requirements (pods must meet):
# - runAsNonRoot: true
# - allowPrivilegeEscalation: false
# - seccompProfile.type: RuntimeDefault or Localhost
# - capabilities: drop ALL

# SECURE CONTAINER SPEC:
securityContext:                         # container-level
  runAsNonRoot: true
  runAsUser: 1001
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop: ["ALL"]
    add: ["NET_BIND_SERVICE"]            # add back only what's needed

# POD-LEVEL SECURITY CONTEXT:
spec:
  securityContext:
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001                        # ownership of mounted volumes
    fsGroupChangePolicy: OnRootMismatch  # faster: only change if needed
    seccompProfile:
      type: RuntimeDefault
    sysctls:                             # namespaced kernel params
    - name: net.core.somaxconn
      value: "65535"
```

---

## Chapter 10: Observability

### 10.1 Probes

```yaml
# THREE PROBE TYPES:
# livenessProbe:  is the container alive? Fail → restart container
# readinessProbe: is the container ready to serve traffic? Fail → remove from Service endpoints
# startupProbe:   is the container done starting up? Until success, liveness/readiness paused

# PROBE METHODS:
# httpGet:   HTTP GET — success if status 200-399
# tcpSocket: TCP connect — success if connection established
# exec:      run command — success if exit code 0
# grpc:      gRPC health check (K8s 1.24+)

livenessProbe:
  httpGet:
    path: /health
    port: 3000
    httpHeaders:
    - name: Custom-Header
      value: liveness
  initialDelaySeconds: 30   # wait 30s before first check (startup time)
  periodSeconds: 10         # check every 10s
  timeoutSeconds: 5         # check must complete in 5s
  successThreshold: 1       # successes needed to be "healthy" (must be 1 for liveness)
  failureThreshold: 3       # failures before action taken

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3       # 3 failures → removed from Service endpoints (no restart)

startupProbe:
  httpGet:
    path: /health
    port: 3000
  failureThreshold: 30      # 30 * periodSeconds = max startup time
  periodSeconds: 10         # total: 5 minutes for startup
  # While startupProbe is failing, liveness/readiness probes are paused
  # After startupProbe succeeds, hands off to liveness/readiness

# BEST PRACTICES:
# readinessProbe != livenessProbe (different semantics)
# readiness fails: traffic stops (connection draining)
# liveness fails: container restarted (may lose in-flight requests)
# Never make liveness depend on external services (DB down → restart loop!)
# readiness CAN depend on external services (DB down → remove from LB)
```

---

## Chapter 11: Helm & Kustomize

### 11.1 Helm

```yaml
# Helm: Kubernetes package manager.
# Chart: package (templates + default values)
# Release: installed chart instance
# Repository: collection of charts

# INSTALL:
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install myredis bitnami/redis \
  --namespace cache \
  --create-namespace \
  --set auth.password=secret \
  --values my-values.yaml

# CHART STRUCTURE:
mychart/
  Chart.yaml          # metadata (name, version, description)
  values.yaml         # default values
  templates/          # Go template manifests
    deployment.yaml
    service.yaml
    _helpers.tpl      # template helpers/partials
  charts/             # subcharts/dependencies
  README.md

# TEMPLATE SYNTAX:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        resources:
          {{- toYaml .Values.resources | nindent 12 }}

# OPERATIONS:
helm list -A                          # all releases all namespaces
helm status myredis -n cache          # release status
helm upgrade myredis bitnami/redis --values new-values.yaml
helm rollback myredis 1               # rollback to revision 1
helm uninstall myredis -n cache
helm template mychart ./mychart       # render templates locally (debug)
helm lint ./mychart                   # validate chart
```

### 11.2 Kustomize

```yaml
# Kustomize: template-free Kubernetes configuration management.
# Overlay pattern: base config + environment-specific patches.
# Built into kubectl: kubectl apply -k ./

# DIRECTORY STRUCTURE:
k8s/
  base/
    kustomization.yaml
    deployment.yaml
    service.yaml
  overlays/
    dev/
      kustomization.yaml
      patch-replicas.yaml
    prod/
      kustomization.yaml
      patch-replicas.yaml
      patch-resources.yaml

# base/kustomization.yaml:
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
commonLabels:
  app: myapp
  managed-by: kustomize

# overlays/prod/kustomization.yaml:
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
- ../../base
namePrefix: prod-
nameSuffix: ""
namespace: production
images:
- name: myapp
  newTag: v1.2.3    # override image tag
patchesStrategicMerge:
- patch-replicas.yaml
- patch-resources.yaml
configMapGenerator:
- name: app-config
  envs:
  - .env.prod

# overlays/prod/patch-replicas.yaml:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp      # must match base resource name
spec:
  replicas: 10     # override base replicas

# APPLY:
kubectl apply -k ./k8s/overlays/prod
kubectl diff -k ./k8s/overlays/prod   # dry-run diff
kustomize build ./k8s/overlays/prod   # render to stdout
```

---

## Chapter 12: Production Operations

### 12.1 Pod Disruption Budget

```yaml
# PDB: minimum availability during voluntary disruptions
# (node drain, cluster upgrade, rolling deploy)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2         # always keep 2 pods running
  # OR:
  # maxUnavailable: 1     # allow 1 to be unavailable at a time
  selector:
    matchLabels:
      app: myapp

# EFFECT: kubectl drain node → blocked if it would violate PDB
# Use with replicas >= 3 to allow meaningful PDB (minAvailable: 2 needs 3+)
```

### 12.2 Namespace Strategy

```
RECOMMENDED NAMESPACE STRUCTURE:
  default         → dev experiments (not production)
  kube-system     → system components (don't touch)
  kube-public     → publicly readable (cluster info)
  monitoring      → Prometheus, Grafana, alerting
  ingress-nginx   → ingress controller
  cert-manager    → TLS certificate management
  production      → production workloads
  staging         → staging workloads
  dev             → development workloads
  <team-name>     → per-team namespaces

NAMESPACE ISOLATION:
  NetworkPolicy: restrict pod-to-pod traffic
  ResourceQuota: limit resources per namespace
  LimitRange: default and max limits per container
  RBAC: team can only manage their namespace
```

### 12.3 Troubleshooting Playbook

```bash
# Pod not running:
kubectl get pods -n myns                    # list pods, see status
kubectl describe pod myapp-xxx -n myns      # events, conditions, probe results
kubectl logs myapp-xxx -n myns              # container logs
kubectl logs myapp-xxx -n myns --previous   # logs from previous crash
kubectl logs myapp-xxx -c mycontainer       # specific container in multi-container pod

# Pod stuck in Pending:
kubectl describe pod myapp-xxx | grep Events   # look for scheduling failures
# Common causes:
# - Insufficient CPU/memory on all nodes
# - Node selector / affinity not matching any node
# - PVC not bound (check PVC status)
# - ImagePullBackOff: bad image name, no pull secret

# Pod CrashLoopBackOff:
kubectl logs myapp-xxx --previous     # logs from the crashed container
# Exit code 1: app error (check logs)
# Exit code 137: OOMKilled (increase memory limit)
# Exit code 139: segfault

# Service not routing traffic:
kubectl get endpoints myservice       # are pod IPs listed?
# No endpoints = selector not matching any pods
# Check: kubectl get pods --show-labels | grep expected-label
kubectl port-forward svc/myservice 8080:80  # bypass LB, test directly

# Node issues:
kubectl get nodes                     # Ready/NotReady
kubectl describe node mynode          # events, conditions, allocated resources
kubectl top nodes                     # CPU/memory usage

# Resource usage:
kubectl top pods -A --sort-by=memory  # most memory-hungry pods
kubectl top pods -A --sort-by=cpu

# Audit: what changed recently?
kubectl get events -n myns --sort-by=lastTimestamp | tail -20
kubectl rollout history deployment/myapp
```

---

*End of Kubernetes Mastery Guide*
