# Java & Spring Boot — Interview Questions & Answers (Complete Premium Reference)
> 150 questions. Core Java, OOP, Generics, Collections, Concurrency, JVM Internals, Spring Boot, Spring Security, JPA/Hibernate, Testing, Java 21+. Easy → Medium → Hard. Every answer is production-grade with full code examples.

---

## Table of Contents
- [Easy (Q1–Q40)](#easy)
- [Medium (Q41–Q100)](#medium)
- [Hard (Q101–Q150)](#hard)

---

## EASY (Q1–Q40)

---

**Q1. How does Java work — JVM, JDK, JRE?**
```
JDK (Java Development Kit) = JRE + compiler (javac) + tools (jshell, jmap, jstack)
JRE (Java Runtime Environment) = JVM + standard libraries (rt.jar / modules)
JVM (Java Virtual Machine) = executes bytecode

Compilation:  YourCode.java → [javac] → YourCode.class (platform-independent bytecode)
Execution:    YourCode.class → [ClassLoader] → [JVM Interpreter] → [JIT] → native code

WRITE ONCE RUN ANYWHERE:
  Bytecode is identical on all platforms.
  JVM is platform-specific and handles the native translation.

JIT (Just-In-Time) compiler:
  1. JVM interprets bytecode on first execution.
  2. HotSpot profiler tracks which methods are "hot" (called frequently).
  3. Hot methods compiled to native machine code (C1 → C2 tiered compilation).
  4. After warmup: native speed with dynamic optimisations (inlining, escape analysis).

Java versions: LTS releases → Java 8, 11, 17, 21. Use 21 for new projects.
```

---

**Q2. What are Java's primitive types?**
```java
byte    b = 127;           // 8-bit  signed, -128 to 127
short   s = 32767;         // 16-bit signed
int     i = 2_147_483_647; // 32-bit signed (most common integer)
long    l = 9_999_999_999L;// 64-bit signed (note L suffix)
float   f = 3.14f;         // 32-bit IEEE 754 (note f suffix)
double  d = 3.14159;       // 64-bit IEEE 754 (default decimal type)
boolean flag = true;       // true or false (JVM uses int internally)
char    c = 'A';           // 16-bit Unicode (0 to 65535)

// Wrapper classes (autoboxing / unboxing):
Integer n = 42;            // autoboxing:  int → Integer (heap object)
int     m = n;             // unboxing:    Integer → int

// Integer cache: JVM caches Integer -128 to 127
Integer x = 127; Integer y = 127; System.out.println(x == y); // true  (cached)
Integer p = 128; Integer q = 128; System.out.println(p == q); // false (new objects)

// Useful constants:
Integer.MAX_VALUE;         // 2147483647
Integer.MIN_VALUE;         // -2147483648
Integer.parseInt("42");    // String → int
Integer.toBinaryString(10);// "1010"
Double.isNaN(0.0/0.0);     // true
```

---

**Q3. What is the difference between `==` and `.equals()`?**
```java
// == compares REFERENCES (memory addresses) for objects
// .equals() compares CONTENT (must be overridden for meaningful comparison)

String a = new String("hello");
String b = new String("hello");
a == b;        // false — different heap objects
a.equals(b);   // true  — same content

// String pool (literal interning):
String c = "hello";   // goes to string pool
String d = "hello";   // returns same pool object
c == d;               // true! (same pooled reference)
c.intern() == d;      // true  (force pool)

// ALWAYS use .equals() for strings:
if ("active".equals(status)) { } // null-safe (avoids NPE if status is null)

// Objects.equals — null-safe wrapper:
Objects.equals(a, b);  // null-safe, same as a != null ? a.equals(b) : b == null

// Override equals (and hashCode!) in domain classes:
record Point(int x, int y) {} // records auto-generate equals, hashCode, toString
Point p1 = new Point(1, 2);
Point p2 = new Point(1, 2);
p1.equals(p2); // true — record equality is value-based
```

---

**Q4. What is OOP? Explain the 4 pillars.**
```java
// 1. ENCAPSULATION — hide internal state, expose via controlled API
public class BankAccount {
    private double balance;              // private — hidden from outside

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Must be positive");
        balance += amount;
    }
    public double getBalance() { return balance; } // controlled read access
}

// 2. INHERITANCE — reuse and extend parent behaviour
public class Animal {
    public void breathe() { System.out.println("breathing"); }
}
public class Dog extends Animal {
    @Override public void breathe() { System.out.println("panting"); } // override
    public void bark() { System.out.println("woof"); }
}

// 3. POLYMORPHISM — one interface, many implementations
public abstract class Shape {
    public abstract double area();
    public String describe() { return "Area: " + area(); } // uses overridden area()
}
public class Circle extends Shape {
    double r;
    @Override public double area() { return Math.PI * r * r; }
}
public class Square extends Shape {
    double s;
    @Override public double area() { return s * s; }
}
// Runtime dispatch:
Shape[] shapes = { new Circle(), new Square() };
for (Shape shape : shapes) System.out.println(shape.area()); // each calls own area()

// 4. ABSTRACTION — expose WHAT, hide HOW
public interface PaymentGateway {
    PaymentResult charge(String cardToken, Money amount);
    void refund(String transactionId);
}
// Caller only knows the contract, not Stripe/PayPal/Square implementation
```

---

**Q5. Abstract class vs Interface — when to use each?**
```java
// ABSTRACT CLASS:
// - Can have instance fields, constructors, concrete + abstract methods
// - Single inheritance only (extends ONE class)
// - Use: shared base with common state for closely related classes
public abstract class HttpHandler {
    protected final Logger log = LoggerFactory.getLogger(getClass());
    protected String basePath;                    // shared state

    public HttpHandler(String basePath) {          // constructor
        this.basePath = basePath;
    }
    public abstract Response handle(Request req); // subclass must implement
    protected void logRequest(Request req) {       // concrete shared method
        log.info("{} {}", req.method(), req.path());
    }
}

// INTERFACE (Java 8+):
// - No instance fields (only public static final constants)
// - default and static methods allowed (Java 8)
// - private methods allowed (Java 9)
// - Class implements MULTIPLE interfaces
public interface Auditable {
    default void auditLog(String action) { AuditService.log(getClass(), action); }
    static Auditable noOp() { return action -> {}; }
}
public interface Cacheable {
    String cacheKey();
    default Duration ttl() { return Duration.ofMinutes(5); }
}

// Implementing multiple contracts:
public class UserService extends BaseService implements Auditable, Cacheable {
    @Override public String cacheKey() { return "users"; }
    // auditLog() from Auditable available automatically
}

// DECISION TABLE:
// Use abstract class when: you need instance state, a template method pattern,
//   or sharing code among strongly related classes.
// Use interface when: defining a contract that unrelated classes implement,
//   you want multiple inheritance of type, or marking capability (Serializable).
```

---

**Q6. What are Java's main Collection types?**
```java
// ── LIST — ordered, allows duplicates ──────────────────────────────────
List<String> list = new ArrayList<>();    // dynamic array, O(1) get, O(n) insert-mid
list.add("a"); list.add(0, "b");          // addLast, addFirst by index
list.get(0); list.set(0, "c");
list.remove(0);                           // by index
list.remove("a");                         // by value
list.subList(0, 2);                       // view, not copy

LinkedList<String> ll = new LinkedList<>(); // doubly linked, O(1) head/tail ops
ll.addFirst("x"); ll.addLast("y");
ll.peekFirst(); ll.pollLast();

// ── SET — no duplicates ──────────────────────────────────────────────
Set<String> hash   = new HashSet<>();    // O(1) avg, no order
Set<String> tree   = new TreeSet<>();    // sorted (natural order or Comparator)
Set<String> linked = new LinkedHashSet<>(); // insertion-order, O(1) ops

// ── MAP — key → value ────────────────────────────────────────────────
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.getOrDefault("missing", 0);          // default if absent
map.putIfAbsent("a", 99);               // only puts if key absent
map.computeIfAbsent("list", k -> new ArrayList<>()); // create on demand
map.merge("count", 1, Integer::sum);    // add 1 to existing count
map.forEach((k, v) -> System.out.println(k + "=" + v));
map.entrySet().stream()...;

TreeMap<String, Integer> sorted = new TreeMap<>(); // sorted by key, O(log n)
LinkedHashMap<String, Integer> ordered = new LinkedHashMap<>(); // insertion order

// ── QUEUE / DEQUE ────────────────────────────────────────────────────
Queue<Integer> q = new LinkedList<>();
q.offer(1); q.poll(); q.peek();          // non-throwing: add/remove/inspect

Deque<Integer> dq = new ArrayDeque<>();  // faster than LinkedList for queue use
dq.addFirst(1); dq.addLast(2);
dq.pollFirst(); dq.pollLast();

PriorityQueue<Integer> pq = new PriorityQueue<>();     // min-heap
PriorityQueue<Integer> maxPQ = new PriorityQueue<>(Collections.reverseOrder());
pq.offer(3); pq.offer(1); pq.poll();     // returns 1 (min)

// ── CONCURRENT COLLECTIONS ───────────────────────────────────────────
ConcurrentHashMap<String, Integer> cm = new ConcurrentHashMap<>();
CopyOnWriteArrayList<String> cowList = new CopyOnWriteArrayList<>(); // read-heavy
```

---

**Q7. What are generics and what is type erasure?**
```java
// Generics = type-safe containers and algorithms without casting

// Generic class:
public class Box<T> {
    private T value;
    public Box(T value) { this.value = value; }
    public T get() { return value; }
}
Box<String> strBox = new Box<>("hello");
String s = strBox.get(); // no cast needed

// Generic method:
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
max("apple", "banana"); // "banana"

// Bounded wildcards — PECS (Producer Extends, Consumer Super):
// ? extends T — can READ T from it (covariant, producer)
public double sum(List<? extends Number> list) {
    return list.stream().mapToDouble(Number::doubleValue).sum();
}
sum(List.of(1, 2.5, 3L)); // works with Integer, Double, Long lists

// ? super T — can WRITE T into it (contravariant, consumer)
public void addDefaults(List<? super Integer> list) {
    list.add(0); list.add(-1);
}

// TYPE ERASURE — generics are compile-time only:
// At runtime, List<String> and List<Integer> are both just List
// JVM has no knowledge of T at runtime
List<String> ls = new ArrayList<>();
List<Integer> li = new ArrayList<>();
ls.getClass() == li.getClass(); // true! both are ArrayList.class

// Consequence: cannot do:
// new T()              — no type token
// new T[]              — no generic arrays
// instanceof List<String> — only instanceof List<?>

// Workaround with Class<T>:
public <T> T fromJson(String json, Class<T> clazz) {
    return objectMapper.readValue(json, clazz);
}
```

---

**Q8. What is exception handling — checked vs unchecked?**
```java
// CHECKED (extend Exception): compiler forces you to handle or declare
// Signals recoverable conditions: file not found, network timeout
public String readFile(String path) throws IOException {
    return Files.readString(Path.of(path));
}

// UNCHECKED (extend RuntimeException): no forced handling
// Signals programming errors: null pointer, bad argument, index out of bounds
public int divide(int a, int b) {
    if (b == 0) throw new IllegalArgumentException("Divisor cannot be zero");
    return a / b;
}

// ERROR (extend Error): JVM-level, do NOT catch
// OutOfMemoryError, StackOverflowError, AssertionError

// TRY-CATCH-FINALLY:
try {
    String result = fetchData();
    int value = Integer.parseInt(result); // may throw NumberFormatException
} catch (NumberFormatException e) {
    log.warn("Malformed number: {}", e.getMessage());
} catch (IOException | SQLException e) {  // multi-catch (Java 7)
    log.error("IO or DB error", e);
    throw new ServiceException("Dependency failed", e); // wrap and rethrow
} finally {
    cleanup(); // ALWAYS runs, even on exception or return
}

// TRY-WITH-RESOURCES (auto-close Autocloseable): Java 7+
try (Connection conn = ds.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql)) {
    ResultSet rs = ps.executeQuery();
    // conn + ps closed in reverse order in finally block automatically
}

// CUSTOM EXCEPTION best practices:
public class OrderNotFoundException extends RuntimeException {
    private final String orderId;

    public OrderNotFoundException(String orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }
    public OrderNotFoundException(String orderId, Throwable cause) {
        super("Order not found: " + orderId, cause); // preserve cause chain!
        this.orderId = orderId;
    }
    public String getOrderId() { return orderId; }
}
```

---

**Q9. What are Java Streams — how do they work?**
```java
// Streams = declarative pipelines for processing sequences of elements.
// Lazy: intermediate ops (filter, map) don't execute until terminal op called.
// Single-use: a stream cannot be reused after terminal op.

List<Employee> employees = getEmployees();

// ── INTERMEDIATE OPS (lazy) ──────────────────────────────────────────
employees.stream()
    .filter(e -> e.getSalary() > 50_000)   // predicate
    .map(Employee::getName)                 // transform T → R
    .sorted()                               // natural order
    .distinct()                             // remove duplicates
    .limit(10)                              // first 10
    .skip(5)                                // skip first 5
    .peek(e -> log.debug("Processing: {}", e)); // side-effect for debug

// ── TERMINAL OPS (trigger execution) ─────────────────────────────────
long count   = stream.count();
Optional<E>  = stream.findFirst();
boolean any  = stream.anyMatch(predicate);
boolean all  = stream.allMatch(predicate);
boolean none = stream.noneMatch(predicate);
List<T> list = stream.collect(Collectors.toList());   // or toUnmodifiableList()
Set<T>  set  = stream.collect(Collectors.toSet());
String joined = stream.collect(Collectors.joining(", ", "[", "]"));

// ── COLLECTORS ────────────────────────────────────────────────────────
Map<String, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

Map<String, Double> avgSalary = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingDouble(Employee::getSalary)));

Map<Boolean, List<Employee>> partitioned = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 70_000));

// ── FLAT MAP ──────────────────────────────────────────────────────────
// flatMap: Stream<List<T>> → Stream<T>
List<String> allSkills = employees.stream()
    .flatMap(e -> e.getSkills().stream())
    .distinct()
    .sorted()
    .collect(Collectors.toList());

// ── REDUCE ────────────────────────────────────────────────────────────
Optional<Integer> sum = List.of(1,2,3,4).stream().reduce(Integer::sum); // 10
int sumWithIdentity    = List.of(1,2,3).stream().reduce(0, Integer::sum);

// ── PRIMITIVE STREAMS ─────────────────────────────────────────────────
IntStream.range(0, 10).forEach(i -> {}); // 0–9
IntStream.rangeClosed(1, 5).sum();        // 15
employees.stream().mapToDouble(Employee::getSalary).average();
employees.stream().mapToInt(Employee::getAge).summaryStatistics(); // min,max,avg,sum

// ── PARALLEL STREAMS ──────────────────────────────────────────────────
// Use only for CPU-intensive work on large datasets.
// ForkJoinPool.commonPool() — shared across whole JVM.
long result = employees.parallelStream()
    .filter(this::isExpensive)  // CPU-bound work
    .mapToLong(Employee::computeScore)
    .sum();
// Avoid for: IO-bound work, stateful ops, small collections, ordered results
```

---

**Q10. Multithreading — Thread lifecycle and creation.**
```java
// Thread lifecycle: NEW → RUNNABLE → BLOCKED/WAITING/TIMED_WAITING → TERMINATED

// 1. Extend Thread (avoid — tight coupling):
class MyThread extends Thread {
    @Override public void run() { System.out.println("running"); }
}
new MyThread().start(); // start() creates OS thread and calls run()

// 2. Implement Runnable (preferred for separation of concerns):
Runnable task = () -> System.out.println("task");
new Thread(task).start();

// 3. ExecutorService (preferred for production):
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<String> future = pool.submit(() -> {
    Thread.sleep(1000);
    return "result";
});
String result = future.get(5, TimeUnit.SECONDS); // blocking get with timeout
pool.shutdown();                    // stop accepting new tasks
pool.awaitTermination(30, TimeUnit.SECONDS);

// Thread pool types:
Executors.newFixedThreadPool(n);       // fixed n threads
Executors.newCachedThreadPool();       // grow/shrink, 60s idle TTL
Executors.newSingleThreadExecutor();   // 1 thread, sequential
Executors.newScheduledThreadPool(n);   // delayed/periodic tasks

// ThreadPoolExecutor for full control:
ThreadPoolExecutor tpe = new ThreadPoolExecutor(
    4,                          // corePoolSize
    8,                          // maximumPoolSize
    60L, TimeUnit.SECONDS,      // keepAliveTime for extra threads
    new LinkedBlockingQueue<>(100), // work queue (bounded!)
    new ThreadPoolExecutor.CallerRunsPolicy()); // rejection policy
```

---

**Q11. Synchronization — `synchronized`, `volatile`, locks.**
```java
// SYNCHRONIZED — mutual exclusion (one thread at a time):
public class Counter {
    private int count = 0;

    public synchronized void increment() { count++; } // method lock on 'this'
    public synchronized int get() { return count; }

    private final Object lock = new Object(); // separate lock object
    public void decrement() {
        synchronized (lock) { count--; } // block-level lock
    }
}

// VOLATILE — visibility guarantee (no caching in registers):
private volatile boolean shutdown = false;
// Thread writing shutdown=true flushes to main memory immediately
// Thread reading shutdown sees the latest value
// Does NOT make compound ops (i++) atomic!

// REENTRANT LOCK — more flexible than synchronized:
private final ReentrantLock lock = new ReentrantLock();
public void update() {
    lock.lock();
    try {
        // critical section
    } finally {
        lock.unlock(); // MUST be in finally
    }
}
// tryLock with timeout (avoids deadlock):
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
    try { /* work */ } finally { lock.unlock(); }
} else {
    // couldn't acquire lock — handle gracefully
}

// READ-WRITE LOCK — multiple readers OR one writer:
ReadWriteLock rwLock = new ReentrantReadWriteLock();
public String read() {
    rwLock.readLock().lock();
    try { return data; } finally { rwLock.readLock().unlock(); }
}
public void write(String d) {
    rwLock.writeLock().lock();
    try { data = d; } finally { rwLock.writeLock().unlock(); }
}

// ATOMIC CLASSES — lock-free with CAS (compare-and-swap):
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();         // thread-safe increment
counter.compareAndSet(0, 1);       // CAS: if current==0, set to 1
counter.getAndUpdate(x -> x * 2);  // atomic update function

AtomicReference<Node> head = new AtomicReference<>(); // lock-free data structures
```

---

**Q12. CompletableFuture — async programming.**
```java
// CompletableFuture = non-blocking async computation chains

// Create:
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> fetchData());
CompletableFuture<Void> run = CompletableFuture.runAsync(() -> fireAndForget());

// Chain transformations:
CompletableFuture<User> userFuture = CompletableFuture
    .supplyAsync(() -> fetchUserId())          // async: returns String
    .thenApply(id -> id.toUpperCase())          // sync transform
    .thenApplyAsync(id -> fetchUser(id))        // async transform
    .thenCompose(user -> enrichUser(user))      // flatMap (avoids nesting)
    .exceptionally(ex -> {
        log.error("Failed: {}", ex.getMessage());
        return User.ANONYMOUS;                  // fallback on error
    })
    .whenComplete((user, ex) -> auditLog(user, ex)); // always runs

// Combine multiple:
CompletableFuture<User>    userF    = fetchUserAsync(id);
CompletableFuture<Account> accountF = fetchAccountAsync(id);
CompletableFuture<Profile> combined = userF.thenCombine(accountF,
    (user, account) -> buildProfile(user, account));

// Wait for all / any:
CompletableFuture.allOf(f1, f2, f3).thenRun(() -> allDone());
CompletableFuture.anyOf(f1, f2, f3).thenAccept(result -> gotFirst(result));

// Timeout (Java 9+):
cf.orTimeout(5, TimeUnit.SECONDS)
  .completeOnTimeout(defaultValue, 3, TimeUnit.SECONDS);

// Get result (blocks — only at the edge of your system):
User user = userFuture.get(10, TimeUnit.SECONDS); // throws checked exceptions
User user2 = userFuture.join();                   // throws unchecked CompletionException
```

---

**Q13. Java Memory Model — heap, stack, metaspace.**
```
HEAP:
  - All objects and arrays live here.
  - Shared across all threads — subject to visibility issues.
  - Managed by GC.
  - Young Gen (Eden + 2 Survivor spaces) + Old Gen + (Metaspace in Java 8+).

STACK:
  - Per-thread — each thread has its own stack.
  - Holds stack frames: local variables, method params, return address.
  - Primitives and object REFERENCES (not objects) stored on stack.
  - StackOverflowError if too deep (infinite recursion).

METASPACE (replaces PermGen since Java 8):
  - Stores class metadata, bytecode, method data.
  - Native memory (not heap) — grows dynamically.
  - OutOfMemoryError: Metaspace if unbounded class loading.

CODE CACHE:
  - JIT-compiled native code stored here.
  - Native memory.

ESCAPE ANALYSIS (JVM optimisation):
  - If JVM proves an object doesn't escape a method, it can allocate it
    on the stack instead of heap — avoiding GC pressure.
  - Enables lock elision (sync on non-shared object removed entirely).
```

---

**Q14. String, StringBuilder, StringBuffer.**
```java
// STRING — immutable, thread-safe, pooled literals
String s = "Hello, World!";
s.length();                      // 13
s.charAt(7);                     // 'W'
s.substring(7, 12);              // "World"
s.indexOf("World");              // 7
s.contains("World");             // true
s.startsWith("Hello");           // true
s.replace("World", "Java");      // "Hello, Java!"
s.toLowerCase(); s.toUpperCase();
s.trim(); s.strip();             // strip() handles Unicode whitespace
s.split(",\\s*");                // ["Hello", "World!"]
s.formatted("Hello, %s!", name); // Java 15+ instance method
String.valueOf(42);              // "42"
String.format("%.2f", 3.14159); // "3.14"

// String pool:
String a = "hello";     // pool reference
String b = "hello";     // same pool reference
a == b;                 // true! (both point to pool object)
new String("hello") == "hello"; // false (new forces heap object)
new String("hello").intern() == "hello"; // true (intern returns pool reference)

// STRINGBUILDER — mutable, NOT thread-safe, fast for single-thread:
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1_000; i++) sb.append(i).append(",");
sb.deleteCharAt(sb.length() - 1); // remove trailing comma
String result = sb.toString();
sb.insert(0, "START:"); sb.reverse(); sb.replace(0, 5, "HELLO");

// STRINGBUFFER — mutable, thread-safe (synchronized), slower:
// Use only when multiple threads share the same buffer (rare).

// Java compiler auto-converts + concatenation in loops to StringBuilder.
// Exception: concatenation in tight loops with + is fine in modern Java
// due to StringConcatFactory (Java 9+) — but explicit SB still clearer.
```

---

**Q15. Functional interfaces and lambda expressions.**
```java
// @FunctionalInterface = interface with exactly ONE abstract method
// Lambdas provide implementations inline

// Built-in functional interfaces:
Function<String, Integer>  fn  = String::length;    // T → R
fn.apply("hello");                                   // 5
fn.andThen(n -> n * 2).apply("hello");               // 10 (compose)

BiFunction<String, Integer, String> biFn = String::substring;
biFn.apply("hello", 2);                              // "llo"

Predicate<String>  pred = s -> s.length() > 3;
pred.test("hi");                                     // false
pred.and(s -> s.startsWith("h")).test("hello");      // true

Consumer<String>   cons = System.out::println;
cons.accept("hello");

BiConsumer<String, Integer> biCons = (s, n) -> System.out.printf("%s=%d%n", s, n);

Supplier<List<String>> sup = ArrayList::new;
sup.get();                                           // new ArrayList each time

UnaryOperator<String>  uo = String::toUpperCase;
BinaryOperator<Integer> bo = Integer::sum;

// Method references — 4 kinds:
String::length        // instance method of class
"hello"::length       // instance method of specific object
String::new           // constructor reference
Integer::parseInt     // static method reference

// Effectively final — lambdas capture variables that don't change:
String prefix = "Mr.";  // effectively final
Function<String, String> greet = name -> prefix + " " + name;
// prefix = "Mrs."; — would cause compile error (lambda captures final snapshot)
```

---

**Q16. Optional — null-safe programming.**
```java
// Optional<T> — a container that may or may not hold a value.
// Use in return types, NOT in fields or method parameters.

// Creation:
Optional<String> present  = Optional.of("value");     // throws NPE if null
Optional<String> nullable = Optional.ofNullable(maybeNull); // safe
Optional<String> empty    = Optional.empty();

// Check and get (avoid unless necessary):
opt.isPresent();          // true if value exists
opt.isEmpty();            // Java 11: true if empty
opt.get();                // throws NoSuchElementException if empty — avoid!

// Safe retrieval:
opt.orElse("default");                       // return default if empty
opt.orElseGet(() -> computeDefault());       // lazy — only called if empty
opt.orElseThrow(() -> new NotFoundException()); // throw if empty
opt.orElseThrow(NotFoundException::new);     // method reference form

// Transform:
opt.map(String::toUpperCase);                // Optional<String> or empty
opt.flatMap(s -> parseId(s));                // use when mapper returns Optional
opt.filter(s -> s.length() > 3);            // empty if predicate fails

// Side effects:
opt.ifPresent(s -> process(s));
opt.ifPresentOrElse(                         // Java 9
    s -> process(s),
    () -> handleEmpty());

// Chaining — avoid nested null checks:
Optional<String> city = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .filter(c -> !c.isEmpty());

// Bad: return Optional from void returns, or use as field type.
// Good: return Optional from methods that might not find a value.
```

---

**Q17. Java records (Java 16+).**
```java
// Records = immutable data carriers. Auto-generate:
//   - private final fields
//   - canonical constructor
//   - equals(), hashCode(), toString()
//   - accessors (name(), age() — not getName())

public record Point(int x, int y) {}

Point p = new Point(3, 4);
p.x();      // 3
p.y();      // 4
p.equals(new Point(3, 4)); // true
p.toString();               // "Point[x=3, y=4]"

// Compact constructor (validate inputs):
public record Range(int min, int max) {
    Range {  // compact — no parameter list, fields auto-assigned after
        if (min > max) throw new IllegalArgumentException("min > max");
    }
}

// Custom methods allowed:
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) throw new IllegalArgumentException();
        return new Money(this.amount.add(other.amount), this.currency);
    }
    public boolean isPositive() { return amount.compareTo(BigDecimal.ZERO) > 0; }
}

// Records can implement interfaces:
public record PersonRecord(String name, int age) implements Comparable<PersonRecord> {
    @Override public int compareTo(PersonRecord other) {
        return Integer.compare(this.age, other.age);
    }
}

// Use cases: DTOs, value objects, API request/response bodies, configuration.
// Cannot extend another class. Cannot be extended (implicitly final).
```

---

**Q18. Sealed classes (Java 17+).**
```java
// Sealed = restrict which classes can extend/implement a type.
// The compiler knows ALL subtypes — enables exhaustive pattern matching.

public sealed interface Shape
    permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public final class Triangle implements Shape {
    public final double base, height;
    // ...
}

// Pattern matching switch (Java 21 — exhaustive because sealed):
double area = switch (shape) {
    case Circle c       -> Math.PI * c.radius() * c.radius();
    case Rectangle r    -> r.width() * r.height();
    case Triangle t     -> 0.5 * t.base * t.height;
    // NO default needed — compiler knows all cases covered
};

// Guarded patterns:
String describe = switch (shape) {
    case Circle c when c.radius() > 100 -> "huge circle";
    case Circle c                       -> "circle r=" + c.radius();
    case Rectangle r when r.width() == r.height() -> "square";
    case Rectangle r                    -> "rectangle";
    case Triangle t                     -> "triangle";
};
```

---

**Q19. Enums in Java.**
```java
// Enums are full classes — can have fields, methods, constructors

public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS  (4.869e+24, 6.0518e6),
    EARTH  (5.976e+24, 6.37814e6);

    private final double mass;    // kg
    private final double radius;  // m

    Planet(double mass, double radius) {
        this.mass = mass; this.radius = radius;
    }
    static final double G = 6.67300E-11;
    public double surfaceGravity() { return G * mass / (radius * radius); }
    public double surfaceWeight(double otherMass) { return otherMass * surfaceGravity(); }
}

// Enum methods:
Planet.EARTH.name();         // "EARTH"
Planet.EARTH.ordinal();      // 2 (0-based index)
Planet.valueOf("MARS");      // Planet.MARS (throws if unknown)
Planet.values();             // Planet[] array of all values
EnumSet.allOf(Planet.class); // efficient bit-set backed set
EnumMap<Planet, String> m = new EnumMap<>(Planet.class); // efficient map

// Abstract method per constant:
public enum Operation {
    PLUS("+")   { @Override public double apply(double x, double y) { return x + y; } },
    MINUS("-")  { @Override public double apply(double x, double y) { return x - y; } };

    private final String symbol;
    Operation(String symbol) { this.symbol = symbol; }
    public abstract double apply(double x, double y);
    @Override public String toString() { return symbol; }
}

// Enums are inherently singletons and thread-safe.
// Enum singleton pattern — best singleton implementation in Java.
public enum AppConfig {
    INSTANCE;
    private final String dbUrl = System.getenv("DB_URL");
    public String getDbUrl() { return dbUrl; }
}
```

---

**Q20. Comparable vs Comparator.**
```java
// Comparable: natural ordering — implement in the class itself
public class Employee implements Comparable<Employee> {
    private String name;
    private double salary;

    @Override
    public int compareTo(Employee other) {
        return Double.compare(this.salary, other.salary); // ascending salary
    }
}
List<Employee> employees = ...;
Collections.sort(employees); // uses compareTo

// Comparator: external/flexible ordering
Comparator<Employee> byName       = Comparator.comparing(Employee::getName);
Comparator<Employee> bySalaryDesc = Comparator.comparingDouble(Employee::getSalary)
                                               .reversed();
Comparator<Employee> byDeptThenSalary = Comparator
    .comparing(Employee::getDepartment)
    .thenComparingDouble(Employee::getSalary);

employees.sort(byDeptThenSalary);
employees.stream().max(Comparator.comparingDouble(Employee::getSalary));

// Null-safe comparator:
Comparator<Employee> nullSafe = Comparator.nullsFirst(
    Comparator.comparing(Employee::getName));

// TreeSet/TreeMap with custom comparator:
TreeSet<Employee> set = new TreeSet<>(bySalaryDesc);
```

---

**Q21. What are Java's `final`, `finally`, `finalize()`?**
```java
// FINAL:
final int MAX = 100;           // constant — cannot reassign
final String name;             // blank final — must assign in constructor
class MyClass {
    final String id;
    MyClass(String id) { this.id = id; }  // assigned in constructor
}
final class ImmutablePoint { }  // class — cannot be subclassed (String, Integer)
public final void method() { }  // method — cannot be overridden in subclasses

// FINALLY:
// Block that ALWAYS runs after try/catch — guaranteed cleanup
try { conn = openConnection(); doWork(conn); }
catch (Exception e) { handleError(e); }
finally { if (conn != null) conn.close(); } // runs on success, exception, or return

// Exception: System.exit() or JVM crash prevent finally from running.
// Try-with-resources is preferred over finally for Autocloseable resources.

// FINALIZE() — deprecated since Java 9, removed in Java 18:
// Called by GC before reclaiming object — unreliable timing, performance issue.
// DO NOT use. Use Cleaner/PhantomReference for cleanup, or try-with-resources.
@Override protected void finalize() throws Throwable {
    // DO NOT implement this — unreliable and deprecated
}
```

---

**Q22. Autoboxing pitfalls.**
```java
// Autoboxing: int → Integer (compiler inserts Integer.valueOf())
// Unboxing: Integer → int (compiler inserts intValue())

// PITFALL 1: NullPointerException from unboxing null:
Integer value = null;
int i = value;  // NullPointerException! unboxing null → NPE

// PITFALL 2: == comparison with cached range (-128 to 127):
Integer a = 100; Integer b = 100; System.out.println(a == b); // true (cached)
Integer c = 200; Integer d = 200; System.out.println(c == d); // false (new objects!)
// Always use .equals() for Integer comparison!

// PITFALL 3: Performance — boxing in tight loops:
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;  // unboxes sum, adds, reboxes sum — 1M box/unbox operations!
}
long sumPrimitive = 0L; // use primitive Long → long

// PITFALL 4: Overloading resolution:
void method(int i) { System.out.println("int"); }
void method(Integer i) { System.out.println("Integer"); }
method(42);              // calls int version
method(Integer.valueOf(42)); // calls Integer version

// PITFALL 5: Collections always box:
List<Integer> list = new ArrayList<>();
list.add(42); // always boxes — use IntStream or primitive arrays for perf
int[] arr = {1, 2, 3}; // no boxing — prefer for performance-critical code
```

---

**Q23. HashMap internals — how does it work?**
```java
// HashMap<K,V> is an array of buckets (default capacity 16).
// Each bucket holds a linked list (or red-black tree if > 8 entries).

// PUT operation:
// 1. Compute hash(key): hash = key.hashCode() XOR (hash >>> 16)
//    (spreads high bits to reduce collisions)
// 2. bucket index = hash & (capacity - 1)   (faster than modulo)
// 3. Check bucket:
//    - Empty → create new Node and insert
//    - Collision → traverse list, find key by equals(), update or append
//    - If list length > 8 (TREEIFY_THRESHOLD) → convert to TreeNode (O(log n))
// 4. If load factor exceeded (default 0.75): resize (double capacity, rehash all entries)

// LOAD FACTOR = entries / capacity
// At 0.75: 75% full triggers resize — balance of time (collisions) vs space

// equals() and hashCode() CONTRACT — critical for HashMap correctness:
// If a.equals(b) → a.hashCode() == b.hashCode() (REQUIRED)
// If a.hashCode() == b.hashCode() → NOT necessarily equals (collision OK)

// Breaking the contract breaks HashMap:
class BadKey {
    int id;
    @Override public boolean equals(Object o) { return ((BadKey)o).id == id; }
    // NO hashCode override! Uses Object.hashCode (identity) → two equal objects
    // land in different buckets → get() never finds them!
}

// Java 8+ improvements:
// - Treeification: bin converts to red-black tree when length > 8 → O(log n) worst case
// - Untreeify: converts back if bin shrinks below 6

// Thread safety:
// HashMap — NOT thread-safe. Never share across threads without sync.
// ConcurrentHashMap — thread-safe, segments (Java 8: Node-level CAS + sync)
// Collections.synchronizedMap(map) — wraps with mutex (coarse-grained lock)
```

---

**Q24. Immutability and defensive copying.**
```java
// Immutable object: state cannot change after construction.
// Benefits: thread-safe by default, safe as HashMap keys, easy to reason about.

// Immutable class recipe:
public final class ImmutablePoint {         // 1. final class
    private final int x;                    // 2. private final fields
    private final int y;

    public ImmutablePoint(int x, int y) {   // 3. constructor sets all fields
        this.x = x;
        this.y = y;
    }
    public int getX() { return x; }         // 4. no setters
    public int getY() { return y; }

    // Operations return new objects:
    public ImmutablePoint translate(int dx, int dy) {
        return new ImmutablePoint(x + dx, y + dy);
    }
}

// Mutable field in "immutable" class — must defensively copy:
public final class DateRange {
    private final Date start; // Date is mutable!
    private final Date end;

    public DateRange(Date start, Date end) {
        this.start = new Date(start.getTime()); // defensive copy in
        this.end   = new Date(end.getTime());
    }
    public Date getStart() {
        return new Date(start.getTime()); // defensive copy out
    }
}

// Modern approach: use LocalDate (immutable) instead of Date
public final class DateRange {
    private final LocalDate start; // LocalDate is immutable — no copy needed
    private final LocalDate end;
    public DateRange(LocalDate start, LocalDate end) { ... }
}

// Collections in immutable class:
public final class Catalog {
    private final List<String> items;
    public Catalog(List<String> items) {
        this.items = List.copyOf(items); // unmodifiable defensive copy
    }
    public List<String> getItems() { return items; } // safe — already unmodifiable
}
```

---

**Q25. Java 8 — Stream and Date-Time API.**
```java
// DATE-TIME API (java.time) — replaces broken Date/Calendar:
LocalDate today = LocalDate.now();          // 2024-01-15
LocalDate birthday = LocalDate.of(1990, Month.JUNE, 15);
LocalDate nextWeek = today.plusWeeks(1);
LocalDate firstDay = today.with(TemporalAdjusters.firstDayOfMonth());

LocalTime time = LocalTime.of(14, 30, 0);  // 14:30:00
LocalTime now = LocalTime.now();

LocalDateTime dt = LocalDateTime.of(today, time); // 2024-01-15T14:30
LocalDateTime in3Hours = dt.plusHours(3);
dt.format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm"));

ZonedDateTime utc  = ZonedDateTime.now(ZoneId.of("UTC"));
ZonedDateTime cairo = utc.withZoneSameInstant(ZoneId.of("Africa/Cairo"));

Instant now2 = Instant.now();  // machine time (epoch millis)
Duration d = Duration.between(start, end); d.toMinutes();
Period p = Period.between(birthday, today); p.getYears();

// Parsing:
LocalDate parsed = LocalDate.parse("2024-01-15", DateTimeFormatter.ISO_LOCAL_DATE);

// Comparisons:
today.isBefore(nextWeek);    // true
today.isEqual(today);        // true
today.compareTo(birthday);   // positive (today is after birthday)
```

---

**Q26. Java Modules (JPMS — Java 9+).**
```java
// module-info.java — declares module dependencies and exports
module com.example.myapp {
    requires java.sql;                      // compile + runtime dep
    requires transitive java.logging;       // re-exports to dependents
    requires static java.xml;               // optional (only compile-time)

    exports com.example.myapp.api;          // accessible to all
    exports com.example.myapp.internal to  // only to specific modules
        com.example.tests;

    opens com.example.myapp.config to      // allow reflection (e.g., for Jackson)
        com.fasterxml.jackson.databind;

    provides com.example.spi.Parser
        with com.example.myapp.JsonParser;  // service provider

    uses com.example.spi.Parser;            // service consumer
}
```

---

**Q27. Iterator pattern and Iterable.**
```java
// Implementing Iterable to support for-each:
public class Range implements Iterable<Integer> {
    private final int start, end;
    public Range(int start, int end) { this.start = start; this.end = end; }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<>() {
            int current = start;
            @Override public boolean hasNext() { return current < end; }
            @Override public Integer next() {
                if (!hasNext()) throw new NoSuchElementException();
                return current++;
            }
        };
    }
}
for (int n : new Range(1, 5)) System.out.println(n); // 1 2 3 4

// ListIterator — bidirectional:
ListIterator<String> it = list.listIterator();
while (it.hasNext()) {
    String s = it.next();
    if (shouldRemove(s)) it.remove(); // safe remove during iteration
    it.set(transform(s));              // replace current element
    it.add(newElement);                // insert before next
}
// Fail-fast: modifying collection directly during iteration → ConcurrentModificationException
// Safe: use iterator.remove(), CopyOnWriteArrayList, or collect and removeAll
```

---

**Q28. Java I/O and NIO.**
```java
// Files utility (java.nio.file) — modern I/O:
Path path = Path.of("/data/file.txt");
String content = Files.readString(path);              // read all as String
List<String> lines = Files.readAllLines(path);        // all lines
byte[] bytes = Files.readAllBytes(path);

Files.writeString(path, "content");                   // write all
Files.write(path, lines, StandardOpenOption.APPEND);
Files.copy(src, dst, StandardCopyOption.REPLACE_EXISTING);
Files.move(src, dst);
Files.delete(path);
Files.exists(path); Files.isRegularFile(path); Files.isDirectory(path);

// Walk directory tree:
try (Stream<Path> walk = Files.walk(Path.of("/data"))) {
    walk.filter(Files::isRegularFile)
        .filter(p -> p.toString().endsWith(".log"))
        .forEach(p -> processLog(p));
}

// Buffered I/O for large files:
try (BufferedReader br = Files.newBufferedReader(path);
     BufferedWriter bw = Files.newBufferedWriter(outPath)) {
    String line;
    while ((line = br.readLine()) != null) {
        bw.write(transform(line));
        bw.newLine();
    }
}

// Temp files:
Path temp = Files.createTempFile("prefix", ".tmp");
Files.deleteIfExists(temp);

// Watch service — monitor file changes:
WatchService watcher = FileSystems.getDefault().newWatchService();
Path dir = Path.of("/config");
dir.register(watcher, ENTRY_CREATE, ENTRY_MODIFY, ENTRY_DELETE);
WatchKey key = watcher.take(); // blocks
for (WatchEvent<?> event : key.pollEvents()) { process(event); }
```

---

**Q29. Reflection API.**
```java
// Reflection: inspect and manipulate classes, fields, methods at runtime.
// Used by: Spring DI, Jackson, JUnit, JPA providers, mock frameworks.

Class<?> clazz = Class.forName("com.example.User"); // by name
Class<User> c = User.class;                          // literal
Class<?> c2 = user.getClass();                       // from instance

// Inspect:
clazz.getName();                    // "com.example.User"
clazz.getSimpleName();              // "User"
clazz.getDeclaredFields();          // all fields (including private)
clazz.getDeclaredMethods();         // all methods (including private)
clazz.getDeclaredConstructors();
clazz.getAnnotations();
clazz.getSuperclass();
clazz.getInterfaces();

// Instantiate:
User user = (User) clazz.getDeclaredConstructor(String.class, int.class)
                        .newInstance("Alice", 30);

// Access private field:
Field field = clazz.getDeclaredField("password");
field.setAccessible(true);           // bypass access control
String pwd = (String) field.get(user);
field.set(user, "newPassword");

// Invoke method:
Method method = clazz.getDeclaredMethod("greet", String.class);
method.setAccessible(true);
String result = (String) method.invoke(user, "Hello");

// Performance: reflection is ~10-50x slower than direct calls.
// Cache Method/Field objects. Use MethodHandles (Java 7+) for better performance.
// Java 9+ modules restrict setAccessible — requires opens in module-info.
```

---

**Q30. Annotations — built-in and custom.**
```java
// BUILT-IN:
@Override           // compiler checks you're actually overriding
@Deprecated         // warn callers not to use
@SuppressWarnings("unchecked") // suppress specific warning
@FunctionalInterface // compiler enforces single abstract method
@SafeVarargs         // suppress heap pollution warning for generics varargs

// CUSTOM ANNOTATION:
@Retention(RetentionPolicy.RUNTIME)   // visible at runtime via reflection
@Target({ElementType.METHOD, ElementType.TYPE}) // where it can be used
@Documented                           // include in Javadoc
public @interface Timed {
    String value() default "";        // element with default
    TimeUnit unit() default TimeUnit.MILLISECONDS;
}

// Usage:
@Timed(value = "fetchUser", unit = TimeUnit.NANOSECONDS)
public User fetchUser(String id) { ... }

// Processing at runtime:
Method m = UserService.class.getMethod("fetchUser", String.class);
Timed timed = m.getAnnotation(Timed.class);
if (timed != null) {
    long start = System.nanoTime();
    // invoke method
    long elapsed = System.nanoTime() - start;
    System.out.printf("%s took %d %s%n", timed.value(), elapsed, timed.unit());
}
```

---

**Q31. Java 11–21 — key new features summary.**
```java
// JAVA 11:
String s = "  hello  ";
s.isBlank();           // true if empty or whitespace
s.strip();             // Unicode-aware trim
s.repeat(3);           // "  hello    hello    hello  "
s.lines().count();     // stream of lines
"Hello".stripLeading().stripTrailing();
var list = new ArrayList<String>(); // local variable type inference (Java 10)

// JAVA 14: switch expressions (standard):
String result = switch (day) {
    case MONDAY, TUESDAY -> "weekday";
    case SATURDAY, SUNDAY -> "weekend";
    default -> "midweek";
};

// JAVA 15: text blocks:
String json = """
        {
            "name": "Alice",
            "age": 30
        }
        """; // trailing """ position determines indentation

// JAVA 16: records, instanceof pattern matching:
if (obj instanceof String s) {
    System.out.println(s.length()); // s already cast and scoped
}

// JAVA 17: sealed classes (final standard), pattern matching in switch (preview)

// JAVA 21 (LTS):
// Virtual threads (Project Loom):
try (ExecutorService vte = Executors.newVirtualThreadPerTaskExecutor()) {
    vte.submit(() -> blockingIO()); // millions of virtual threads possible
}
Thread.ofVirtual().start(() -> blockingIO()); // individual virtual thread

// Sequenced collections (new interface):
SequencedCollection<String> sc = new ArrayList<>(List.of("a","b","c"));
sc.getFirst();  sc.getLast();
sc.addFirst("x"); sc.addLast("z");
sc.reversed();   // reversed view

// Record patterns (destructuring):
if (obj instanceof Point(int x, int y)) {
    System.out.println("x=" + x + " y=" + y);
}
```

---

**Q32. Java concurrency utilities — `CountDownLatch`, `CyclicBarrier`, `Semaphore`.**
```java
// COUNTDOWNLATCH — wait for N events to complete (one-time):
CountDownLatch latch = new CountDownLatch(3);
ExecutorService pool = Executors.newFixedThreadPool(3);
for (int i = 0; i < 3; i++) {
    pool.submit(() -> {
        doWork();
        latch.countDown(); // decrement counter
    });
}
latch.await(10, TimeUnit.SECONDS); // main thread waits until count=0
System.out.println("All 3 workers done!");

// CYCLICBARRIER — wait for N threads to all reach a barrier (reusable):
CyclicBarrier barrier = new CyclicBarrier(3, () -> System.out.println("All at barrier!"));
for (int i = 0; i < 3; i++) {
    pool.submit(() -> {
        doPhase1();
        barrier.await(); // all 3 wait here before proceeding
        doPhase2();
        barrier.await(); // barrier resets automatically for phase 3
        doPhase3();
    });
}

// SEMAPHORE — limit concurrent access (resource pool):
Semaphore semaphore = new Semaphore(3); // max 3 concurrent
void accessDatabase() throws InterruptedException {
    semaphore.acquire(); // blocks if 3 already acquired
    try { useConnection(); }
    finally { semaphore.release(); } // always release!
}

// EXCHANGER — two threads swap objects at a sync point:
Exchanger<List<String>> ex = new Exchanger<>();
// Thread 1: List<String> full = ex.exchange(buffer); // swap
// Thread 2: List<String> toProcess = ex.exchange(new ArrayList<>());

// PHASER — flexible barrier (dynamic registration, multiple phases):
Phaser phaser = new Phaser(1); // register main thread
for (int i = 0; i < 3; i++) {
    phaser.register();
    pool.submit(() -> { doWork(); phaser.arriveAndDeregister(); });
}
phaser.arriveAndAwaitAdvance(); // wait for all
```

---

**Q33. Java NIO — non-blocking I/O channels.**
```java
// NIO (java.nio): Channels + Buffers + Selectors (non-blocking I/O)

// FileChannel — random access file I/O:
try (FileChannel fc = FileChannel.open(path, StandardOpenOption.READ)) {
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    while (fc.read(buffer) > 0) {
        buffer.flip();     // switch from write to read mode
        while (buffer.hasRemaining()) process(buffer.get());
        buffer.clear();    // ready for next read
    }
}

// Memory-mapped file — extremely fast for large files:
try (FileChannel fc = FileChannel.open(path, READ, WRITE)) {
    MappedByteBuffer mbb = fc.map(MapMode.READ_WRITE, 0, fc.size());
    mbb.put(0, (byte) 'H'); // direct memory write, no syscall
}

// Selector — single thread manages multiple non-blocking channels:
Selector selector = Selector.open();
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(8080));
server.configureBlocking(false);
server.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select(); // blocks until at least one channel ready
    Set<SelectionKey> keys = selector.selectedKeys();
    for (SelectionKey key : keys) {
        if (key.isAcceptable()) { /* accept connection */ }
        if (key.isReadable())   { /* read data */ }
        if (key.isWritable())   { /* write data */ }
    }
    keys.clear();
}
```

---

**Q34. Garbage Collection — how does it work?**
```
GENERATIONAL HYPOTHESIS: most objects die young.
This lets GC focus on young gen (cheap), rarely scanning old gen.

GENERATIONS:
  Young Gen (Eden + Survivor S0 + S1) — most objects created here
    Minor GC: fast (ms range), copies live objects to survivor or promotes to Old
    Stop-the-world but very short

  Old Gen — long-lived objects promoted from Young Gen
    Major/Full GC: expensive, pauses application for longer

  Metaspace — class metadata (not GC'd the same way)

GC ALGORITHMS:
  Serial GC (-XX:+UseSerialGC):
    Single-threaded, stop-the-world. Good for small heaps, embedded.

  Parallel GC (-XX:+UseParallelGC):
    Multi-threaded minor + major GC. High throughput, longer pauses.
    Default in Java 8 for servers.

  G1 GC (-XX:+UseG1GC):
    Heap divided into equal-sized regions (not fixed gen layout).
    Concurrent marking + parallel evacuation.
    Predictable pause times (target with -XX:MaxGCPauseMillis=200).
    Default since Java 9.

  ZGC (-XX:+UseZGC):
    Pause times < 1ms regardless of heap size (terabytes).
    Concurrent (app runs during GC).
    Java 15+ production-ready.

  Shenandoah: similar to ZGC, low-pause concurrent GC.

TUNING TIPS:
  -Xms4g -Xmx4g       set heap (equal to avoid resize)
  -XX:NewRatio=2       Old:Young ratio (2 = 2:1 → 1/3 young)
  -XX:+PrintGCDetails  log GC events
  -XX:+HeapDumpOnOutOfMemoryError  dump on OOM for analysis
```

---

**Q35. equals() and hashCode() contract.**
```java
// CONTRACT (from Object spec):
// 1. Reflexive:  x.equals(x) == true
// 2. Symmetric:  x.equals(y) == y.equals(x)
// 3. Transitive: if x.equals(y) && y.equals(z) → x.equals(z)
// 4. Consistent: multiple calls return same result (if no state change)
// 5. x.equals(null) == false

// hashCode contract:
// - If x.equals(y) → x.hashCode() == y.hashCode()
// - (converse not required: same hashCode doesn't mean equals)

// ALWAYS override hashCode when you override equals:
public class Employee {
    private String id;
    private String name;
    private double salary;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                           // identity check
        if (!(o instanceof Employee)) return false;           // null-safe type check
        Employee e = (Employee) o;
        return Objects.equals(id, e.id) &&                   // null-safe field compare
               Objects.equals(name, e.name);
        // salary intentionally excluded — business equality by id+name
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name); // must include same fields as equals
    }
}

// Records auto-generate correct equals/hashCode using all fields.
// Lombok @EqualsAndHashCode generates it for you.
// IntelliJ/Eclipse can auto-generate — always review which fields to include.

// Common bug: include mutable fields in hashCode → object changes bucket in HashMap!
// Rule: only include fields that won't change after object is put in a HashMap/Set.
```

---

**Q36. Java Concurrency — deadlock, livelock, starvation.**
```java
// DEADLOCK: Thread A holds lock1, waits for lock2.
//           Thread B holds lock2, waits for lock1. Both wait forever.

// Classic deadlock:
Object lock1 = new Object(), lock2 = new Object();
Thread t1 = new Thread(() -> {
    synchronized(lock1) { Thread.sleep(100); synchronized(lock2) { } }
});
Thread t2 = new Thread(() -> {
    synchronized(lock2) { Thread.sleep(100); synchronized(lock1) { } }
});

// PREVENTION:
// 1. Lock ordering — always acquire locks in the same order:
void transfer(Account from, Account to, double amount) {
    Account first  = from.id < to.id ? from : to;   // always lock lower id first
    Account second = from.id < to.id ? to   : from;
    synchronized(first)  { synchronized(second) { from.debit(amount); to.credit(amount); } }
}

// 2. tryLock with timeout:
if (lock1.tryLock(100, MILLISECONDS)) {
    try {
        if (lock2.tryLock(100, MILLISECONDS)) {
            try { /* work */ } finally { lock2.unlock(); }
        } else { /* couldn't get lock2, back off and retry */ }
    } finally { lock1.unlock(); }
}

// LIVELOCK: threads keep retrying but never make progress (both yield to each other)
// STARVATION: low-priority thread never gets CPU because high-priority threads dominate
// Fix starvation: fair lock (new ReentrantLock(true) — FIFO ordering)

// DETECT DEADLOCK at runtime:
ThreadMXBean bean = ManagementFactory.getThreadMXBean();
long[] deadlocked = bean.findDeadlockedThreads(); // returns thread IDs or null
```

---

**Q37. ThreadLocal.**
```java
// ThreadLocal provides per-thread storage — each thread has its own value.
// Use cases: per-request context (user ID, transaction ID), SimpleDateFormat, DB connections.

public class RequestContext {
    private static final ThreadLocal<String> userId = new ThreadLocal<>();
    private static final ThreadLocal<String> requestId =
        ThreadLocal.withInitial(() -> UUID.randomUUID().toString()); // initial value

    public static void setUserId(String id) { userId.set(id); }
    public static String getUserId() { return userId.get(); }
    public static void clear() { userId.remove(); } // MUST call to prevent memory leaks
}

// In servlet filter / interceptor:
public void doFilter(HttpServletRequest req, ...) {
    try {
        RequestContext.setUserId(extractUserId(req));
        chain.doFilter(req, resp);
    } finally {
        RequestContext.clear(); // CRITICAL: thread pool reuses threads!
    }
}

// MEMORY LEAK WARNING:
// ThreadLocal values survive thread reuse in thread pools.
// Always remove() in finally block in server environments.
// InheritableThreadLocal — child threads inherit parent's values (use with care).
```

---

**Q38. Fork/Join framework — parallel divide-and-conquer.**
```java
// ForkJoinPool: work-stealing thread pool for recursive parallel tasks.
// Each thread has its own deque; idle threads steal tasks from others.

public class MergeSort extends RecursiveAction {
    private final int[] array;
    private final int start, end;

    public MergeSort(int[] array, int start, int end) {
        this.array = array; this.start = start; this.end = end;
    }

    @Override
    protected void compute() {
        if (end - start <= 1000) { // base case: sort sequentially
            Arrays.sort(array, start, end);
            return;
        }
        int mid = (start + end) / 2;
        MergeSort left  = new MergeSort(array, start, mid);
        MergeSort right = new MergeSort(array, mid, end);
        invokeAll(left, right); // fork both, wait for completion
        merge(array, start, mid, end);
    }
}

// RecursiveTask<T> for tasks that return a result:
public class SumTask extends RecursiveTask<Long> {
    @Override protected Long compute() {
        if (end - start <= 1000) return sumSequentially();
        int mid = (start + end) / 2;
        SumTask left = new SumTask(array, start, mid);
        left.fork(); // async
        long rightResult = new SumTask(array, mid, end).compute(); // inline
        return left.join() + rightResult; // join after inline work
    }
}

// Usage:
ForkJoinPool pool = ForkJoinPool.commonPool(); // shared, uses all CPUs
long result = pool.invoke(new SumTask(data, 0, data.length));
```

---

**Q39. Design patterns — common patterns in Java.**
```java
// SINGLETON (thread-safe, lazy — Initialization-on-demand holder):
public class DatabasePool {
    private DatabasePool() {}
    private static class Holder {
        static final DatabasePool INSTANCE = new DatabasePool();
    }
    public static DatabasePool getInstance() { return Holder.INSTANCE; }
}

// BUILDER:
public class Request {
    private final String url;
    private final Map<String, String> headers;
    private final int timeoutMs;

    private Request(Builder b) { this.url = b.url; this.headers = b.headers; this.timeoutMs = b.timeoutMs; }

    public static class Builder {
        private String url;
        private Map<String, String> headers = new HashMap<>();
        private int timeoutMs = 5000;
        public Builder url(String url) { this.url = url; return this; }
        public Builder header(String k, String v) { headers.put(k, v); return this; }
        public Builder timeout(int ms) { this.timeoutMs = ms; return this; }
        public Request build() {
            Objects.requireNonNull(url, "URL required");
            return new Request(this);
        }
    }
}
Request req = new Request.Builder().url("https://api.example.com").timeout(3000).build();

// FACTORY METHOD:
public interface Notification { void send(String msg); }
public class NotificationFactory {
    public static Notification create(String type) {
        return switch (type) {
            case "email" -> new EmailNotification();
            case "sms"   -> new SmsNotification();
            case "push"  -> new PushNotification();
            default      -> throw new IllegalArgumentException("Unknown: " + type);
        };
    }
}

// OBSERVER (built into Java via listeners):
public interface EventListener<T> { void onEvent(T event); }
public class EventBus<T> {
    private final List<EventListener<T>> listeners = new CopyOnWriteArrayList<>();
    public void subscribe(EventListener<T> l) { listeners.add(l); }
    public void publish(T event) { listeners.forEach(l -> l.onEvent(event)); }
}
```

---

**Q40. Java testing — JUnit 5 basics.**
```java
// JUnit 5 (Jupiter):
@Test
void addition() {
    assertEquals(4, 2 + 2);
    assertNotNull(result);
    assertTrue(list.isEmpty());
    assertThrows(IllegalArgumentException.class, () -> new Range(5, 1));
    assertAll(
        () -> assertEquals("Alice", user.getName()),
        () -> assertEquals(30, user.getAge())
    );
}

@BeforeEach void setUp() { /* runs before each test */ }
@AfterEach  void tearDown() { }
@BeforeAll  static void setUpClass() { /* once for class */ }
@AfterAll   static void tearDownClass() { }

@ParameterizedTest
@ValueSource(strings = { "Alice", "Bob", "Charlie" })
void testWithNames(String name) { assertTrue(name.length() > 0); }

@ParameterizedTest
@CsvSource({ "Alice,30", "Bob,25" })
void testWithCSV(String name, int age) { /* test */ }

@ParameterizedTest
@MethodSource("provideUsers")
void testUsers(User user) { assertNotNull(user.getId()); }
static Stream<User> provideUsers() { return Stream.of(new User("Alice"), new User("Bob")); }

@Nested class WhenEmpty { /* nested test class for context */ }
@Tag("integration") class IntegrationTest { }
@Disabled("WIP") void skippedTest() { }
@Timeout(value = 5, unit = TimeUnit.SECONDS) void slowTest() { }
```

---

## MEDIUM (Q41–Q100)

---

**Q41. Spring IoC and Dependency Injection.**
```java
// IoC (Inversion of Control): Spring manages object creation and wiring.
// DI (Dependency Injection): dependencies provided from outside, not created inside.

// 3 ways to inject:
// 1. CONSTRUCTOR INJECTION (preferred — guarantees immutability and testability):
@Service
public class OrderService {
    private final OrderRepository orderRepo;
    private final PaymentService paymentService;

    // @Autowired optional when single constructor (Spring 4.3+):
    public OrderService(OrderRepository orderRepo, PaymentService paymentService) {
        this.orderRepo = orderRepo;
        this.paymentService = paymentService;
    }
}

// 2. SETTER INJECTION (optional dependencies):
@Service
public class NotificationService {
    private EmailService emailService;
    @Autowired(required = false)
    public void setEmailService(EmailService emailService) {
        this.emailService = emailService;
    }
}

// 3. FIELD INJECTION (not recommended — hard to test without Spring):
@Service
public class ProductService {
    @Autowired private ProductRepository repo; // hidden dependency, final not possible
}

// Qualifying multiple implementations:
@Service @Primary class PostgresUserRepo implements UserRepository {}
@Service @Qualifier("mongo") class MongoUserRepo implements UserRepository {}

@Service class UserService {
    UserService(@Qualifier("mongo") UserRepository repo) {} // explicit qual
}
```

---

**Q42. Spring Boot auto-configuration.**
```java
// Auto-configuration: Spring Boot inspects classpath and configures beans automatically.
// @EnableAutoConfiguration (inside @SpringBootApplication) triggers this.

// How it works:
// 1. @SpringBootApplication = @Configuration + @EnableAutoConfiguration + @ComponentScan
// 2. Spring Boot reads META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
// 3. Each listed class is a @Configuration with @ConditionalOn* conditions
// 4. Conditions determine whether to create beans

// Example: DataSource auto-config (simplified):
@Configuration
@ConditionalOnClass(DataSource.class)          // HikariCP on classpath?
@ConditionalOnMissingBean(DataSource.class)    // no custom DataSource defined?
@EnableConfigurationProperties(DataSourceProperties.class)
public class DataSourceAutoConfiguration {
    @Bean
    @ConditionalOnProperty(prefix = "spring.datasource", name = "url")
    public DataSource dataSource(DataSourceProperties props) {
        return props.initializeDataSourceBuilder().build();
    }
}

// Override auto-config by defining your own bean:
@Bean
public DataSource dataSource() {
    HikariDataSource ds = new HikariDataSource();
    ds.setJdbcUrl("jdbc:postgresql://...");
    ds.setMaximumPoolSize(10);
    return ds; // Spring Boot sees this → skips auto-config DataSource
}

// application.properties/yaml:
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=pass
spring.datasource.hikari.maximum-pool-size=10
```

---

**Q43. Spring Boot REST API — complete example.**
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
@Validated
public class UserController {
    private final UserService userService;

    @GetMapping
    public ResponseEntity<Page<UserDTO>> getUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String search) {
        return ResponseEntity.ok(userService.findAll(page, size, search));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable @NotNull UUID id) {
        return userService.findById(id)
                .map(ResponseEntity::ok)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @PostMapping
    public ResponseEntity<UserDTO> createUser(
            @RequestBody @Valid CreateUserRequest request) {
        UserDTO created = userService.create(request);
        URI location = URI.create("/api/users/" + created.id());
        return ResponseEntity.created(location).body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> updateUser(
            @PathVariable UUID id,
            @RequestBody @Valid UpdateUserRequest request) {
        return ResponseEntity.ok(userService.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable UUID id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}

// Global exception handler:
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException e) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ErrorResponse(e.getMessage(), "NOT_FOUND"));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
                .map(f -> f.getField() + ": " + f.getDefaultMessage())
                .collect(Collectors.joining(", "));
        return ResponseEntity.badRequest().body(new ErrorResponse(msg, "VALIDATION_ERROR"));
    }
}
```

---

**Q44. Spring Data JPA — repositories, JPQL, specifications.**
```java
// Repository hierarchy:
// Repository → CrudRepository → PagingAndSortingRepository → JpaRepository

@Repository
public interface UserRepository extends JpaRepository<User, UUID> {

    // Derived query (Spring generates SQL from method name):
    Optional<User> findByEmail(String email);
    List<User> findByDepartmentAndActiveTrue(String dept);
    List<User> findByAgeBetweenOrderBySalaryDesc(int min, int max);
    long countByDepartment(String dept);
    boolean existsByEmail(String email);

    // Custom JPQL:
    @Query("SELECT u FROM User u WHERE u.salary > :minSalary AND u.dept = :dept")
    List<User> findHighEarners(@Param("minSalary") double salary,
                               @Param("dept") String dept);

    // Native SQL:
    @Query(value = "SELECT * FROM users WHERE email ILIKE :pattern", nativeQuery = true)
    List<User> searchByEmail(@Param("pattern") String pattern);

    // Projection (fetch only needed columns):
    List<UserSummary> findByDepartment(String dept); // UserSummary = interface with getName(), getEmail()

    // Modifying query:
    @Modifying @Transactional
    @Query("UPDATE User u SET u.active = false WHERE u.lastLoginDate < :cutoff")
    int deactivateInactiveUsers(@Param("cutoff") LocalDate cutoff);

    // Pagination:
    Page<User> findByDepartment(String dept, Pageable pageable);
}

// JpaSpecificationExecutor — dynamic queries:
public class UserSpecs {
    public static Specification<User> hasName(String name) {
        return (root, query, cb) -> name == null ? null :
                cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }
    public static Specification<User> hasMinSalary(Double min) {
        return (root, query, cb) -> min == null ? null :
                cb.greaterThanOrEqualTo(root.get("salary"), min);
    }
}

List<User> users = userRepo.findAll(
    Specification.where(UserSpecs.hasName(name)).and(UserSpecs.hasMinSalary(min)));
```

---

**Q45. JPA entity relationships.**
```java
@Entity @Table(name = "orders")
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)  // LAZY = default for @ManyToOne in best practice
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @OneToMany(mappedBy = "order",      // mappedBy = FK is on OrderItem side
               cascade = CascadeType.ALL,
               orphanRemoval = true,
               fetch = FetchType.LAZY)  // ALWAYS lazy for collections!
    private List<OrderItem> items = new ArrayList<>();

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "order_promotions",
               joinColumns = @JoinColumn(name = "order_id"),
               inverseJoinColumns = @JoinColumn(name = "promo_id"))
    private Set<Promotion> promotions = new HashSet<>();

    // Bidirectional helper methods (keep both sides in sync):
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }
    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}

// N+1 QUERY PROBLEM — fetch join to solve:
// BAD: for each order, JPA fires a separate query for customer (N+1)
// GOOD: fetch join loads everything in one query:
@Query("SELECT o FROM Order o JOIN FETCH o.customer JOIN FETCH o.items WHERE o.id = :id")
Optional<Order> findByIdWithDetails(@Param("id") UUID id);

// @EntityGraph alternative (declarative):
@EntityGraph(attributePaths = {"customer", "items"})
Optional<Order> findById(UUID id);
```

---

**Q46. Spring `@Transactional` — internals and pitfalls.**
```java
@Service
public class TransferService {
    @Transactional  // creates new transaction, commits on success, rolls back on RuntimeException
    public void transfer(UUID fromId, UUID toId, BigDecimal amount) {
        Account from = accountRepo.findById(fromId).orElseThrow();
        Account to   = accountRepo.findById(toId).orElseThrow();
        from.debit(amount);
        to.credit(amount);
        accountRepo.save(from);
        accountRepo.save(to);
        // If any exception → Spring rolls back both saves atomically
    }
}

// Propagation modes (most important):
// REQUIRED (default): use existing transaction, or create new
// REQUIRES_NEW: always create new (suspend existing if any)
// NESTED: savepoint within current transaction
// SUPPORTS: use existing if present, run non-transactionally if none
// NOT_SUPPORTED: suspend existing, run non-transactionally
// NEVER: throw if transaction exists

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void auditLog(String action) { /* always own transaction */ }

// Rollback rules:
@Transactional(rollbackFor = Exception.class)         // also rollback checked exceptions
@Transactional(noRollbackFor = ValidationException.class)

// Isolation levels:
@Transactional(isolation = Isolation.SERIALIZABLE)    // strictest, highest contention
@Transactional(isolation = Isolation.READ_COMMITTED)  // default in most DBs

// PITFALL 1: self-invocation bypasses proxy:
@Service class MyService {
    @Transactional void outer() { this.inner(); } // inner() runs WITHOUT transaction!
    @Transactional void inner() { }               // @Transactional ignored on self-call
}
// Fix: inject self, use AspectJ mode, or refactor to separate service

// PITFALL 2: @Transactional on private/protected methods — ignored!
// Proxy only intercepts public methods.
```

---

**Q47. Spring Security — authentication and JWT.**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(AbstractHttpConfigurer::disable)  // disable for REST APIs
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/public/**").permitAll()
                .anyRequest().authenticated())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }

    @Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(12); }
}

// JWT filter:
@Component @RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {
    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest req, ...) {
        String authHeader = req.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(req, resp); return;
        }
        String token = authHeader.substring(7);
        String username = jwtService.extractUsername(token);
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails user = userDetailsService.loadUserByUsername(username);
            if (jwtService.isTokenValid(token, user)) {
                UsernamePasswordAuthenticationToken auth =
                    new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(req));
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        }
        filterChain.doFilter(req, resp);
    }
}
```

---

**Q48. Spring AOP — aspect-oriented programming.**
```java
@Aspect @Component
public class TimingAspect {
    private static final Logger log = LoggerFactory.getLogger(TimingAspect.class);

    // Pointcut: all public methods in service layer
    @Pointcut("execution(public * com.example.service.*.*(..))")
    public void serviceLayer() {}

    // Around advice — wraps the method:
    @Around("serviceLayer()")
    public Object timeMethod(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            Object result = pjp.proceed(); // call the actual method
            long elapsed = System.nanoTime() - start;
            log.info("{}.{} completed in {}ms",
                pjp.getTarget().getClass().getSimpleName(),
                pjp.getSignature().getName(), elapsed / 1_000_000);
            return result;
        } catch (Throwable t) {
            log.error("Exception in {}: {}", pjp.getSignature(), t.getMessage());
            throw t;
        }
    }

    // Before advice — before method runs:
    @Before("@annotation(com.example.annotation.RequiresAuth)")
    public void checkAuth(JoinPoint jp) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) throw new UnauthorizedException();
    }

    // AfterReturning — after successful return:
    @AfterReturning(pointcut = "execution(* *.createOrder(..))", returning = "order")
    public void auditOrderCreated(Object order) { auditService.log(order); }

    // AfterThrowing:
    @AfterThrowing(pointcut = "serviceLayer()", throwing = "ex")
    public void handleException(Exception ex) { alertService.send(ex); }
}
```

---

**Q49. Spring Boot configuration — profiles and externalized config.**
```java
// application.properties / application.yml hierarchy (later overrides earlier):
// 1. Embedded defaults (@Value defaults)
// 2. application.properties in classpath
// 3. application-{profile}.properties
// 4. OS environment variables
// 5. Command-line args (--server.port=9090)

// application.yml:
server:
  port: 8080
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:h2:mem:testdb}  # env var with fallback
    username: ${DB_USER:sa}
  jpa:
    show-sql: false
    hibernate.ddl-auto: validate

// Profiles:
@Profile("dev")  @Component class DevMailSender implements MailSender { /* stub */ }
@Profile("prod") @Component class SmtpMailSender implements MailSender { /* real */ }
// Activate: spring.profiles.active=prod  or  --spring.profiles.active=prod

// Type-safe configuration:
@ConfigurationProperties(prefix = "app")
@Validated
public record AppConfig(
    @NotBlank String jwtSecret,
    @Min(300) int jwtExpirySeconds,
    @NotNull CorsConfig cors
) {
    public record CorsConfig(List<String> allowedOrigins) {}
}

@EnableConfigurationProperties(AppConfig.class)  // in @Configuration class
// Then inject normally: @Autowired AppConfig config;

// @Value for single values:
@Value("${app.jwt-secret}") private String jwtSecret;
@Value("${server.port:8080}") private int port;
```

---

**Q50. Spring Boot testing — unit vs integration.**
```java
// UNIT TEST — test service in isolation with mocks:
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository orderRepo;
    @Mock PaymentService  paymentService;
    @InjectMocks OrderService orderService;

    @Test
    void createOrder_shouldSaveAndCharge() {
        // Arrange
        CreateOrderRequest req = new CreateOrderRequest(customerId, items);
        Order saved = Order.builder().id(UUID.randomUUID()).build();
        when(orderRepo.save(any())).thenReturn(saved);
        when(paymentService.charge(any(), any())).thenReturn(PaymentResult.SUCCESS);

        // Act
        Order result = orderService.createOrder(req);

        // Assert
        assertNotNull(result.getId());
        verify(orderRepo).save(any(Order.class));
        verify(paymentService).charge(eq(customerId), any(Money.class));
    }

    @Test
    void createOrder_whenPaymentFails_shouldThrow() {
        when(paymentService.charge(any(), any())).thenThrow(new PaymentException("declined"));
        assertThrows(PaymentException.class, () -> orderService.createOrder(req));
        verify(orderRepo, never()).save(any()); // should not save if payment fails
    }
}

// INTEGRATION TEST — full Spring context with test database:
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
class UserControllerIT {
    @Container static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16")
            .withDatabaseName("testdb");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", pg::getJdbcUrl);
    }

    @Autowired TestRestTemplate rest;

    @Test
    void createAndFetchUser() {
        ResponseEntity<UserDTO> created = rest.postForEntity(
            "/api/users", new CreateUserRequest("Alice", "alice@example.com"), UserDTO.class);
        assertEquals(201, created.getStatusCodeValue());
        UUID id = created.getBody().id();

        ResponseEntity<UserDTO> fetched = rest.getForEntity("/api/users/" + id, UserDTO.class);
        assertEquals("Alice", fetched.getBody().name());
    }
}
```

---

**Q51. Hibernate N+1 problem and solutions.**
```java
// N+1 PROBLEM:
// Fetching 100 orders, each with a customer → 1 query for orders + 100 for customers = 101 queries

// SOLUTION 1: JPQL fetch join
@Query("SELECT o FROM Order o JOIN FETCH o.customer JOIN FETCH o.items")
List<Order> findAllWithDetails();

// SOLUTION 2: @EntityGraph (cleaner for repository methods)
@EntityGraph(attributePaths = {"customer", "items", "items.product"})
List<Order> findAll();

// SOLUTION 3: Batch fetching (@BatchSize)
@Entity class Order {
    @OneToMany @BatchSize(size = 50) // JPA fetches 50 collections in one IN clause
    private List<OrderItem> items;
}

// SOLUTION 4: DTO projection with single query
@Query("SELECT new com.example.dto.OrderSummary(o.id, c.name, COUNT(i)) " +
       "FROM Order o JOIN o.customer c LEFT JOIN o.items i GROUP BY o.id, c.name")
List<OrderSummary> findOrderSummaries();

// DETECTION: enable SQL logging and count queries
spring.jpa.show-sql=true
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.stat=DEBUG
spring.jpa.properties.hibernate.generate_statistics=true
// Or use p6spy / Hibernate Statistics to auto-detect N+1

// PITFALL: EAGER fetch by default on @ManyToOne — change to LAZY:
@ManyToOne(fetch = FetchType.LAZY) // always do this
private Customer customer;
```

---

**Q52. Spring caching — @Cacheable, @CacheEvict.**
```java
@EnableCaching // on @Configuration class
@Configuration
public class CacheConfig {
    @Bean CacheManager cacheManager() {
        RedisCacheManager cm = RedisCacheManager.builder(redisConnectionFactory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10))
                .serializeValuesWith(
                    RedisSerializationContext.SerializationPair.fromSerializer(
                        new GenericJackson2JsonRedisSerializer())))
            .build();
        return cm;
    }
}

@Service
public class ProductService {
    @Cacheable(value = "products", key = "#id",
               condition = "#id != null",
               unless = "#result == null")  // don't cache null results
    public ProductDTO findById(UUID id) {
        return productRepo.findById(id).map(mapper::toDTO).orElse(null);
    }

    @CachePut(value = "products", key = "#result.id") // update cache on write
    public ProductDTO updateProduct(UUID id, UpdateProductRequest req) {
        Product p = productRepo.findById(id).orElseThrow();
        mapper.update(p, req);
        return mapper.toDTO(productRepo.save(p));
    }

    @CacheEvict(value = "products", key = "#id")  // remove from cache
    public void deleteProduct(UUID id) { productRepo.deleteById(id); }

    @CacheEvict(value = "products", allEntries = true) // clear entire cache
    @Scheduled(cron = "0 0 * * * *") // every hour
    public void evictProductCache() { }
}
```

---

**Q53. Spring WebFlux — reactive programming.**
```java
// WebFlux = reactive, non-blocking HTTP framework.
// Mono<T> = 0 or 1 item. Flux<T> = 0 to N items.
// Built on Project Reactor, runs on Netty (not Servlet container).

@RestController @RequestMapping("/api/reactive")
public class ReactiveUserController {
    private final ReactiveUserRepository userRepo;

    @GetMapping("/{id}")
    public Mono<ResponseEntity<User>> getUser(@PathVariable String id) {
        return userRepo.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE) // SSE
    public Flux<User> streamUsers() {
        return userRepo.findAll()
                .delayElements(Duration.ofMillis(100)); // emit one per 100ms
    }

    @PostMapping
    public Mono<ResponseEntity<User>> createUser(@RequestBody Mono<CreateUserRequest> body) {
        return body
            .flatMap(req -> userRepo.save(toUser(req)))
            .map(saved -> ResponseEntity.created(URI.create("/api/reactive/" + saved.getId()))
                    .body(saved));
    }
}

// Combine multiple async operations:
public Mono<OrderDetails> getOrderDetails(String orderId) {
    return Mono.zip(
        orderRepo.findById(orderId),
        userRepo.findById(order.getUserId()),
        inventoryService.checkStock(order.getProductIds())
    ).map(tuple -> new OrderDetails(tuple.getT1(), tuple.getT2(), tuple.getT3()));
}

// Error handling:
public Mono<Product> getProduct(String id) {
    return productRepo.findById(id)
        .switchIfEmpty(Mono.error(new NotFoundException("Product: " + id)))
        .onErrorResume(TimeoutException.class, e -> getCachedProduct(id))
        .timeout(Duration.ofSeconds(3));
}
```

---

**Q54. Virtual Threads (Project Loom — Java 21).**
```java
// Virtual threads: lightweight threads managed by JVM (not OS).
// OS thread: ~1MB stack, expensive context switch → limits to thousands.
// Virtual thread: ~few KB, cheap park/unpark → millions possible.

// Old approach — blocking IO wastes OS thread:
ExecutorService pool = Executors.newFixedThreadPool(200);
pool.submit(() -> {
    String data = Files.readString(path); // OS thread BLOCKED during IO
    processData(data);
});

// Virtual threads — OS thread freed during blocking:
ExecutorService vte = Executors.newVirtualThreadPerTaskExecutor();
vte.submit(() -> {
    String data = Files.readString(path); // JVM parks virtual thread, OS thread free
    processData(data);
}); // Now handle 100K concurrent requests without 100K OS threads

// Spring Boot 3.2+ auto-config virtual threads:
spring.threads.virtual.enabled=true
// All @Async, Tomcat request threads, @Scheduled → virtual threads automatically

// Direct creation:
Thread.ofVirtual().name("worker-1").start(() -> doWork());
Thread.ofVirtual().start(Runnable runnable);

// IMPORTANT: virtual threads are NOT always faster:
// ✓ Good: lots of blocking IO (HTTP calls, DB queries, file reads)
// ✗ Neutral: CPU-bound work (no benefit — still needs OS thread)
// ✗ Avoid: synchronized blocks + IO (pins carrier OS thread!)
//   Fix: use ReentrantLock instead of synchronized for IO-bound code

// Structured concurrency (Java 21 preview → 23 standard):
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<User>    user    = scope.fork(() -> fetchUser(id));
    Future<Account> account = scope.fork(() -> fetchAccount(id));
    scope.join().throwIfFailed();
    return new Profile(user.get(), account.get()); // both fetched concurrently
}
```

---

**Q55. Java performance tuning — profiling and optimization.**
```java
// PROFILING TOOLS:
// JFR (Java Flight Recorder) — low-overhead production profiling:
jcmd <pid> JFR.start name=myrecording duration=60s filename=recording.jfr
// Analyse in JDK Mission Control or async-profiler

// JVM FLAGS for performance insight:
-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:gc.log
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof
-XX:+UseG1GC -XX:MaxGCPauseMillis=200
-Xss512k    // reduce stack size if creating many threads
-Xms4g -Xmx4g  // fix heap size to avoid resize pauses

// MICROBENCHMARKING with JMH (Java Microbenchmark Harness):
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
public class StringBenchmark {
    @Param({"10", "100", "1000"}) int iterations;

    @Benchmark
    public String concatenation() {
        String s = "";
        for (int i = 0; i < iterations; i++) s += i;
        return s;
    }

    @Benchmark
    public String stringBuilder() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < iterations; i++) sb.append(i);
        return sb.toString();
    }
}

// COMMON PERFORMANCE PATTERNS:
// 1. Object pooling (for expensive-to-create objects):
ObjectPool<Connection> pool = new GenericObjectPool<>(factory);

// 2. Avoid autoboxing in hot paths — use primitive collections:
int[] arr = new int[1000]; // not Integer[]
// Or use Eclipse Collections / Koloboke for primitive Maps/Sets

// 3. String.intern() for repeated strings (save heap):
String country = rawCountry.intern(); // reuse pooled reference

// 4. Efficient serialization — Jackson vs Kryo vs Protobuf:
// Jackson: flexible, slower. Kryo: fast binary. Protobuf: cross-language schema.

// 5. Lazy initialization with double-checked locking:
private volatile ExpensiveObject obj;
public ExpensiveObject get() {
    if (obj == null) {
        synchronized(this) {
            if (obj == null) obj = new ExpensiveObject(); // double check
        }
    }
    return obj;
}
```

---

**Q56. Java design patterns — behavioral patterns.**
```java
// STRATEGY — swap algorithm at runtime:
public interface SortStrategy { void sort(int[] data); }
public class QuickSort implements SortStrategy { @Override public void sort(int[] d) { Arrays.sort(d); } }
public class Sorter {
    private SortStrategy strategy;
    public Sorter(SortStrategy s) { this.strategy = s; }
    public void setStrategy(SortStrategy s) { this.strategy = s; }
    public void sort(int[] d) { strategy.sort(d); }
}

// TEMPLATE METHOD — define skeleton, fill details in subclasses:
public abstract class DataProcessor {
    public final void process() { // final — cannot be overridden
        readData(); transformData(); writeData(); // hook points
    }
    protected abstract void readData();
    protected abstract void transformData();
    protected void writeData() { /* default impl */ } // optional override
}

// CHAIN OF RESPONSIBILITY — pass request along handlers:
public abstract class Handler {
    private Handler next;
    public Handler setNext(Handler h) { this.next = h; return h; }
    public void handle(Request req) {
        if (canHandle(req)) doHandle(req);
        else if (next != null) next.handle(req);
    }
    protected abstract boolean canHandle(Request req);
    protected abstract void doHandle(Request req);
}

// COMMAND — encapsulate action as object (undo, queue, log):
public interface Command { void execute(); void undo(); }
public class MoveCommand implements Command {
    private final Robot robot;
    private final int dx, dy;
    private int prevX, prevY;
    @Override public void execute() { prevX=robot.x; prevY=robot.y; robot.move(dx, dy); }
    @Override public void undo() { robot.moveTo(prevX, prevY); }
}

// DECORATOR — add behaviour without subclassing:
public interface TextTransformer { String transform(String text); }
public class UpperCaseTransformer implements TextTransformer {
    private final TextTransformer inner;
    public UpperCaseTransformer(TextTransformer t) { this.inner = t; }
    @Override public String transform(String text) { return inner.transform(text).toUpperCase(); }
}
```

---

**Q57. Java memory leaks — common causes and fixes.**
```java
// 1. STATIC COLLECTIONS accumulating objects:
public class Cache {
    private static final Map<String, Object> CACHE = new HashMap<>();
    // LEAK: entries never removed, CACHE grows forever
}
// Fix: use WeakHashMap (keys GC'd when not otherwise referenced), or bounded LRU cache:
private static final Map<String, Object> CACHE =
    Collections.synchronizedMap(new LinkedHashMap<>(100, 0.75f, true) {
        @Override protected boolean removeEldestEntry(Map.Entry<String, Object> eldest) {
            return size() > 100; // evict when over 100 entries
        }
    });

// 2. LISTENERS not deregistered:
button.addActionListener(this); // 'this' held by button → can't be GC'd
// Fix: always remove listeners:
button.removeActionListener(this);
// Or: use WeakReference<ActionListener>

// 3. INNER CLASSES holding outer class reference:
class Outer {
    byte[] bigData = new byte[1_000_000];
    class Inner { } // Inner holds implicit reference to Outer!
}
// Fix: make inner class static

// 4. THREAD LOCAL not cleared:
threadLocal.set(largeObject);
// Thread pool reuses threads → value survives request!
// Fix: always remove in finally:
try { threadLocal.set(v); work(); } finally { threadLocal.remove(); }

// 5. UNCLOSED STREAMS / CONNECTIONS:
// Fix: always try-with-resources

// DETECTION:
// - jmap -histo:live <pid> — histogram of live objects
// - jmap -dump:live,format=b,file=heap.hprof <pid>
// - Eclipse MAT / IntelliJ heap analyser
// - async-profiler for allocation profiling
```

---

**Q58. Jackson — JSON serialization with Java.**
```java
// ObjectMapper is thread-safe — create once, share:
@Bean ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())           // LocalDate, Instant support
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
        .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES) // ignore extra fields
        .enable(MapperFeature.ACCEPT_CASE_INSENSITIVE_ENUMS)
        .setSerializationInclusion(JsonInclude.Include.NON_NULL); // omit null fields
}

// Annotations:
public class UserDTO {
    @JsonProperty("user_id")           String id;
    @JsonIgnore                         String password; // never serialize
    @JsonFormat(pattern = "yyyy-MM-dd") LocalDate birthday;
    @JsonInclude(JsonInclude.Include.NON_EMPTY) List<String> tags;
    @JsonAlias({"full_name", "display_name"}) String name; // accept multiple names on deserialization

    @JsonCreator // for deserialization with non-default constructor:
    public UserDTO(@JsonProperty("user_id") String id, @JsonProperty("name") String name) { ... }
}

// Polymorphism:
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = CatPet.class,  name = "cat"),
    @JsonSubTypes.Type(value = DogPet.class,  name = "dog"),
})
public abstract class Pet { }

// Serialization / deserialization:
String json = objectMapper.writeValueAsString(user);
User user   = objectMapper.readValue(json, User.class);
List<User> users = objectMapper.readValue(json, new TypeReference<List<User>>() {});
JsonNode node = objectMapper.readTree(json);
node.get("name").asText();
```

---

**Q59. Spring Boot actuator and observability.**
```java
// Add dependency: spring-boot-starter-actuator
// Expose endpoints:
management.endpoints.web.exposure.include=health,info,metrics,prometheus,loggers
management.endpoint.health.show-details=always
management.health.db.enabled=true

// Custom health indicator:
@Component
public class ExternalApiHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        try {
            ResponseEntity<String> r = restTemplate.getForEntity("https://api.example.com/health", String.class);
            return r.getStatusCode().is2xxSuccessful()
                ? Health.up().withDetail("status", "reachable").build()
                : Health.down().withDetail("status", r.getStatusCode()).build();
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
    }
}

// Custom metrics with Micrometer:
@Service @RequiredArgsConstructor
public class OrderService {
    private final MeterRegistry meterRegistry;

    public Order createOrder(CreateOrderRequest req) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            Order order = processOrder(req);
            meterRegistry.counter("orders.created", "status", "success").increment();
            return order;
        } catch (Exception e) {
            meterRegistry.counter("orders.created", "status", "error").increment();
            throw e;
        } finally {
            sample.stop(meterRegistry.timer("orders.processing.time"));
        }
    }
}

// Distributed tracing with Micrometer Tracing (Zipkin/Jaeger):
// Just add dependency + config — Spring auto-instruments HTTP, DB, messaging.
management.tracing.sampling.probability=1.0  # 100% sampling in dev
```

---

**Q60. Spring Events — application-internal messaging.**
```java
// Publisher:
@Service @RequiredArgsConstructor
public class OrderService {
    private final ApplicationEventPublisher publisher;

    @Transactional
    public Order createOrder(CreateOrderRequest req) {
        Order order = orderRepo.save(buildOrder(req));
        publisher.publishEvent(new OrderCreatedEvent(this, order)); // sync by default
        return order;
    }
}

// Event class:
public class OrderCreatedEvent extends ApplicationEvent {
    private final Order order;
    public OrderCreatedEvent(Object source, Order order) {
        super(source); this.order = order;
    }
    public Order getOrder() { return order; }
}

// Listener (synchronous — runs in same transaction):
@Component
public class OrderEventListener {
    @EventListener
    @Async  // async — runs in different thread (add @EnableAsync to config)
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT) // after TX commits
    public void onOrderCreated(OrderCreatedEvent event) {
        sendConfirmationEmail(event.getOrder());
        updateInventory(event.getOrder());
    }
}

// @TransactionalEventListener phases:
// AFTER_COMMIT (default): fires after TX commits → safe for side effects
// AFTER_ROLLBACK: fires if TX rolled back
// AFTER_COMPLETION: fires after TX ends (commit or rollback)
// BEFORE_COMMIT: fires before TX commits
```

---

**Q61. Java generics — advanced wildcards and type tokens.**
```java
// TYPE TOKEN — pass Class<T> to preserve generic type at runtime:
public class TypedCache {
    private Map<Class<?>, Object> cache = new HashMap<>();

    public <T> void put(Class<T> type, T value) { cache.put(type, value); }
    @SuppressWarnings("unchecked")
    public <T> T get(Class<T> type) { return type.cast(cache.get(type)); }
}
TypedCache tc = new TypedCache();
tc.put(String.class, "hello");
String s = tc.get(String.class); // no unchecked cast for caller

// SUPER TYPE TOKEN (Neal Gafter) — capture generic types at runtime:
abstract class TypeRef<T> {
    final Type type;
    TypeRef() { type = ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[0]; }
}
// TypeReference<List<User>> in Jackson works the same way:
List<User> users = mapper.readValue(json, new TypeReference<List<User>>() {});

// PRODUCER EXTENDS, CONSUMER SUPER (PECS):
// Copy from source to destination:
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) dest.add(item);
}
List<Integer> ints  = List.of(1, 2, 3);
List<Number>  nums  = new ArrayList<>();
copy(ints, nums);  // ints is producer (extends), nums is consumer (super)

// Wildcard capture (when you need to name the wildcard type):
public static <T> void swap(List<T> list, int i, int j) { // T names the wildcard
    T temp = list.get(i); list.set(i, list.get(j)); list.set(j, temp);
}
// Calls swap internally: swap(wildcardList, 0, 1) — capture helper pattern
```

---

**Q62. CompletableFuture — advanced patterns.**
```java
// RETRY with exponential backoff:
public <T> CompletableFuture<T> withRetry(Supplier<CompletableFuture<T>> taskFactory,
                                            int maxAttempts, Duration baseDelay) {
    return taskFactory.get().exceptionallyCompose(ex -> {
        if (maxAttempts <= 1) return CompletableFuture.failedFuture(ex);
        return CompletableFuture.delayedExecutor(baseDelay.toMillis(), MILLISECONDS)
            .execute(() -> {})
            .thenCompose(v -> withRetry(taskFactory, maxAttempts - 1, baseDelay.multipliedBy(2)));
    });
}

// BULKHEAD — limit concurrency with Semaphore:
Semaphore semaphore = new Semaphore(10);
public CompletableFuture<Response> callExternalApi(Request req) {
    semaphore.acquire();
    return httpClient.sendAsync(buildRequest(req), BodyHandlers.ofString())
        .whenComplete((r, t) -> semaphore.release());
}

// FAN-OUT / FAN-IN:
List<String> userIds = List.of("u1", "u2", "u3");
List<CompletableFuture<User>> futures = userIds.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetchUser(id), executor))
    .collect(toList());

CompletableFuture<List<User>> allUsers = CompletableFuture
    .allOf(futures.toArray(new CompletableFuture[0]))
    .thenApply(v -> futures.stream().map(CompletableFuture::join).collect(toList()));

// TIMEOUT with fallback:
CompletableFuture<String> result = fetchData()
    .completeOnTimeout("FALLBACK", 3, SECONDS)  // Java 9
    .orTimeout(5, SECONDS);                      // hard timeout — throws on expiry
```

---

**Q63. Java serialization and alternatives.**
```java
// JAVA SERIALIZATION (Serializable) — avoid for new code:
public class User implements Serializable {
    private static final long serialVersionUID = 1L; // version control
    private String name;
    private transient String password; // transient = NOT serialized
    private transient String computedHash; // recompute on read

    // readObject for validation / recompute transients:
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        this.computedHash = computeHash(); // restore transient on deserialization
    }
}

// SECURITY WARNING: Java deserialization of untrusted data → RCE!
// Use ObjectInputFilter (Java 9+) to whitelist classes:
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("com.example.*;java.base/*;!*");
ois.setObjectInputFilter(filter);

// ALTERNATIVES (use these instead):
// JSON: Jackson, Gson — human-readable, widely compatible
// Protocol Buffers: binary, schema-defined, cross-language, fast
// Avro: schema evolution, used with Kafka
// Kryo: fast Java-specific binary serialization
// MessagePack: compact binary JSON

// Kotlin data classes, Java records — use with Jackson for clean JSON serialization.

// EXTERNALIZATION (custom serialization):
public class Config implements Externalizable {
    @Override public void writeExternal(ObjectOutput out) throws IOException {
        out.writeUTF(name); out.writeInt(version); // explicit control
    }
    @Override public void readExternal(ObjectInput in) throws IOException {
        name = in.readUTF(); version = in.readInt();
    }
}
```

---

**Q64. Spring Batch — large-scale data processing.**
```java
@Configuration @EnableBatchProcessing
public class BatchConfig {
    @Bean
    public Job importUsersJob(JobRepository repo, Step step) {
        return new JobBuilder("importUsers", repo)
            .start(step)
            .build();
    }

    @Bean
    public Step importStep(JobRepository repo, PlatformTransactionManager tm,
                           FlatFileItemReader<UserRow> reader,
                           ItemProcessor<UserRow, User> processor,
                           RepositoryItemWriter<User> writer) {
        return new StepBuilder("importStep", repo)
            .<UserRow, User>chunk(500, tm)   // process 500 items per transaction
            .reader(reader)
            .processor(processor)
            .writer(writer)
            .faultTolerant()
            .skipLimit(100).skip(ValidationException.class)  // skip bad records
            .retryLimit(3).retry(TransientDataAccessException.class)
            .build();
    }

    @Bean
    public FlatFileItemReader<UserRow> csvReader() {
        return new FlatFileItemReaderBuilder<UserRow>()
            .name("userReader")
            .resource(new ClassPathResource("users.csv"))
            .delimited().names("name", "email", "department")
            .targetType(UserRow.class)
            .build();
    }

    @Bean
    public ItemProcessor<UserRow, User> processor() {
        return row -> {
            if (!isValid(row)) throw new ValidationException("Invalid: " + row);
            return User.of(row.getName(), row.getEmail().toLowerCase(), row.getDepartment());
        };
    }
}
```

---

**Q65. Spring Cloud — microservices patterns.**
```java
// SERVICE DISCOVERY with Eureka:
@SpringBootApplication @EnableEurekaServer
public class DiscoveryServer { }

@SpringBootApplication @EnableDiscoveryClient
public class UserService { }

// application.yml (Eureka client):
eureka.client.service-url.defaultZone=http://discovery:8761/eureka/

// LOAD-BALANCED RestTemplate / WebClient:
@Bean @LoadBalanced RestTemplate restTemplate() { return new RestTemplate(); }
// Now service names work: restTemplate.getForObject("http://order-service/api/orders", ...)

// CIRCUIT BREAKER with Resilience4j:
@CircuitBreaker(name = "orderService", fallbackMethod = "fallbackOrder")
@Retry(name = "orderService")
@TimeLimiter(name = "orderService")
public CompletableFuture<OrderDTO> getOrder(String id) {
    return CompletableFuture.supplyAsync(() -> orderServiceClient.getOrder(id));
}
public CompletableFuture<OrderDTO> fallbackOrder(String id, Exception ex) {
    return CompletableFuture.completedFuture(OrderDTO.unavailable());
}

// application.yml:
resilience4j.circuitbreaker.instances.orderService:
  sliding-window-size: 10
  failure-rate-threshold: 50        # open after 50% failures
  wait-duration-in-open-state: 30s  # half-open after 30s
  permitted-number-of-calls-in-half-open-state: 3

// CONFIG SERVER:
@SpringBootApplication @EnableConfigServer
public class ConfigServer { }
// bootstrap.yml in clients:
spring.config.import=configserver:http://config:8888
```

---

**Q66. Kafka with Spring — producer and consumer.**
```java
// Dependency: spring-kafka

// Producer:
@Service @RequiredArgsConstructor
public class OrderEventProducer {
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        OrderEvent event = new OrderCreatedEvent(order.getId(), order.getUserId(),
                                                  order.getTotalAmount(), Instant.now());
        kafkaTemplate.send("order-events", order.getId().toString(), event)
            .whenComplete((result, ex) -> {
                if (ex != null) log.error("Failed to publish: {}", ex.getMessage());
                else log.debug("Published to partition {} offset {}",
                    result.getRecordMetadata().partition(),
                    result.getRecordMetadata().offset());
            });
    }
}

// Consumer:
@Component
public class OrderEventConsumer {
    @KafkaListener(topics = "order-events",
                   groupId = "notification-service",
                   containerFactory = "kafkaListenerContainerFactory")
    public void handleOrderCreated(
            @Payload OrderCreatedEvent event,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            Acknowledgment ack) {
        try {
            notificationService.sendConfirmation(event.getUserId(), event.getOrderId());
            ack.acknowledge(); // manual commit after successful processing
        } catch (Exception e) {
            log.error("Failed to process event at partition {} offset {}", partition, offset, e);
            // don't ack → re-processed on restart / assign to DLT
        }
    }
}

// application.yml:
spring.kafka.bootstrap-servers=kafka:9092
spring.kafka.consumer.auto-offset-reset=earliest
spring.kafka.consumer.enable-auto-commit=false  # manual ack
spring.kafka.listener.ack-mode=manual_immediate
```

---

**Q67. JPA entity lifecycle and `@EntityListeners`.**
```java
// Entity lifecycle callbacks:
@Entity
public class Order {
    @Id UUID id;
    LocalDateTime createdAt;
    LocalDateTime updatedAt;

    @PrePersist    void prePersist()  { createdAt = updatedAt = LocalDateTime.now(); }
    @PreUpdate     void preUpdate()   { updatedAt = LocalDateTime.now(); }
    @PreRemove     void preRemove()   { log.info("Deleting order {}", id); }
    @PostLoad      void postLoad()    { /* initialize transient fields */ }
    @PostPersist   void postPersist() { /* fire domain events */ }
}

// External listener (separates concerns):
public class AuditListener {
    @PrePersist @PreUpdate
    public void setAuditFields(Auditable entity) {
        entity.setUpdatedBy(SecurityContextHolder.getContext().getAuthentication().getName());
        entity.setUpdatedAt(Instant.now());
    }
}

@Entity @EntityListeners(AuditListener.class)
public class Product implements Auditable { ... }

// Spring Data Auditing (simpler):
@EnableJpaAuditing(auditorAwareRef = "auditorProvider")
@Configuration public class JpaConfig {}

@Bean AuditorAware<String> auditorProvider() {
    return () -> Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
                         .map(Authentication::getName);
}

@Entity public class Product {
    @CreatedDate   LocalDateTime createdAt;
    @LastModifiedDate LocalDateTime updatedAt;
    @CreatedBy     String createdBy;
    @LastModifiedBy String updatedBy;
}
```

---

**Q68. Hibernate optimistic and pessimistic locking.**
```java
// OPTIMISTIC LOCKING — detect concurrent modification with version field:
@Entity
public class Product {
    @Id Long id;
    String name;
    int stock;
    @Version int version; // auto-incremented on each update
}

// Concurrent scenario:
// Thread A: reads Product{version=1, stock=100}
// Thread B: reads Product{version=1, stock=100}
// Thread B: updates → version becomes 2, stock=90 ✓
// Thread A: tries update → WHERE id=1 AND version=1 → no row found!
//           Hibernate throws OptimisticLockException → handle and retry

// Handle optimistic lock:
@Retryable(value = OptimisticLockException.class, maxAttempts = 3)
@Transactional
public void reserveStock(Long productId, int qty) {
    Product p = productRepo.findById(productId).orElseThrow();
    if (p.getStock() < qty) throw new InsufficientStockException();
    p.setStock(p.getStock() - qty);
    productRepo.save(p); // may throw OptimisticLockException
}

// PESSIMISTIC LOCKING — database-level row lock:
@Lock(LockModeType.PESSIMISTIC_WRITE) // SELECT ... FOR UPDATE
@Query("SELECT p FROM Product p WHERE p.id = :id")
Optional<Product> findByIdForUpdate(@Param("id") Long id);

// Pessimistic vs Optimistic:
// Optimistic: low contention, retries on conflict (better for most apps)
// Pessimistic: high contention (e.g., inventory), prevents retry storms
// Always: prefer optimistic; use pessimistic only when conflicts are very frequent
```

---

**Q69. Java records — advanced patterns.**
```java
// VALIDATION in compact constructor:
public record EmailAddress(String value) {
    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");
    EmailAddress {
        Objects.requireNonNull(value, "Email cannot be null");
        if (!EMAIL_PATTERN.matcher(value).matches())
            throw new IllegalArgumentException("Invalid email: " + value);
        value = value.toLowerCase(); // normalise
    }
}

// CUSTOM ACCESSORS:
public record FullName(String firstName, String lastName) {
    public String fullName() { return firstName + " " + lastName; } // extra method
    public String initials() { return firstName.charAt(0) + "." + lastName.charAt(0) + "."; }
    @Override public String toString() { return fullName(); } // override toString
}

// GENERIC RECORD:
public record Pair<A, B>(A first, B second) {
    public Pair<B, A> swap() { return new Pair<>(second, first); }
    public static <A, B> Pair<A, B> of(A a, B b) { return new Pair<>(a, b); }
}

// DTO MAPPING:
public record UserDTO(UUID id, String name, String email) {
    public static UserDTO from(User user) {
        return new UserDTO(user.getId(), user.getName(), user.getEmail());
    }
    public User toEntity() { return new User(id, name, email); }
}

// PATTERN MATCHING with records (Java 21):
if (shape instanceof Circle(double radius)) {
    System.out.println("Circle radius = " + radius);
}
switch (shape) {
    case Circle(double r)         when r > 50 -> "Large circle";
    case Circle(double r)                     -> "Circle r=" + r;
    case Rectangle(double w, double h)         -> "Rectangle " + w + "x" + h;
    case Triangle(double b, double h)          -> "Triangle";
}
```

---

**Q70. Java streams — collectors and custom collectors.**
```java
// BUILT-IN COLLECTORS:
// toList, toSet, toMap, toUnmodifiableList/Set/Map (Java 10)
// joining, counting, summingInt, averagingDouble, summarizingInt
// groupingBy, partitioningBy, toCollection

// DOWNSTREAM COLLECTORS (chaining):
Map<String, Long> countByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept, Collectors.counting()));

Map<String, Optional<Employee>> highestPaidByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept,
        Collectors.maxBy(Comparator.comparingDouble(Employee::getSalary))));

Map<String, Map<String, List<Employee>>> byDeptThenRole = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept,
        Collectors.groupingBy(Employee::getRole)));  // nested grouping

// TEEING COLLECTOR (Java 12):
var stats = employees.stream().collect(Collectors.teeing(
    Collectors.counting(),
    Collectors.averagingDouble(Employee::getSalary),
    (count, avg) -> Map.of("count", count, "avgSalary", avg)
));

// CUSTOM COLLECTOR:
public class TopNCollector<T> implements Collector<T, PriorityQueue<T>, List<T>> {
    private final int n;
    private final Comparator<T> comparator;

    @Override public Supplier<PriorityQueue<T>> supplier() {
        return () -> new PriorityQueue<>(n + 1, comparator);
    }
    @Override public BiConsumer<PriorityQueue<T>, T> accumulator() {
        return (pq, item) -> { pq.offer(item); if (pq.size() > n) pq.poll(); };
    }
    @Override public BinaryOperator<PriorityQueue<T>> combiner() {
        return (pq1, pq2) -> { pq2.forEach(pq1::offer); return pq1; };
    }
    @Override public Function<PriorityQueue<T>, List<T>> finisher() {
        return pq -> { List<T> list = new ArrayList<>(pq); Collections.sort(list, comparator.reversed()); return list; };
    }
    @Override public Set<Characteristics> characteristics() { return Set.of(); }
}
// Usage: stream.collect(new TopNCollector<>(10, Comparator.comparingInt(Integer::intValue)));
```

---

**Q71. Spring Scheduler and async tasks.**
```java
@Configuration @EnableScheduling @EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}

@Service
public class ReportService {
    // Cron: second minute hour day-of-month month day-of-week
    @Scheduled(cron = "0 0 2 * * *")      // 2am every day
    @Scheduled(fixedRate = 60_000)         // every 60 seconds
    @Scheduled(fixedDelay = 5_000)         // 5 seconds after last completion
    @Scheduled(initialDelay = 10_000, fixedRate = 60_000)
    public void generateDailyReport() { /* no return, no args for @Scheduled */ }

    @Async
    public CompletableFuture<Report> generateReportAsync(Date from, Date to) {
        Report r = expensiveOperation(from, to);
        return CompletableFuture.completedFuture(r);
    }

    @Async
    public void sendEmailAsync(String to, String subject, String body) {
        mailService.send(to, subject, body); // runs in async executor thread
    }
}
```

---

**Q72. JVM class loading — parent delegation model.**
```
CLASS LOADING:
  Bootstrap ClassLoader (native, loads rt.jar / java.base module)
        ↑ parent
  Platform ClassLoader (loads java.* extension modules)
        ↑ parent
  Application ClassLoader (loads -classpath, user code)
        ↑ parent
  Custom ClassLoaders (application servers, frameworks, plugins)

PARENT DELEGATION:
  1. Child loader receives load request for com.example.Foo
  2. FIRST delegates to parent (don't load yourself if parent can)
  3. Parent tries its parent (up to Bootstrap)
  4. Bootstrap fails → Platform tries → App ClassLoader tries → loads from classpath
  5. If none find it → ClassNotFoundException

WHY: Security — rogue rt.jar classes can't replace java.lang.String
     Consistency — same class object everywhere in JVM

BREAKING DELEGATION (SPI — Service Provider Interface):
  Context ClassLoader (Thread.currentThread().getContextClassLoader()):
  Bootstrap-loaded code (java.util.ServiceLoader) needs to load app-provided implementations.
  Uses context class loader set on thread to reach application classes.

CLASS LOADING PHASES:
  Loading → Linking (Verify → Prepare → Resolve) → Initialization

DYNAMIC CLASS LOADING:
  Class.forName("com.mysql.Driver") — loads and initializes
  ClassLoader.loadClass("com.example.Foo") — loads only, not initializes
```

---

**Q73. Java NIO2 — async file and network I/O.**
```java
// Async file channel — callback-based or Future-based:
AsynchronousFileChannel afc = AsynchronousFileChannel.open(
    path, StandardOpenOption.READ, StandardOpenOption.WRITE);

// Future-based:
ByteBuffer buf = ByteBuffer.allocate(4096);
Future<Integer> readFuture = afc.read(buf, 0L);  // non-blocking
// ... do other work ...
int bytesRead = readFuture.get(); // blocks only when result needed

// Completion handler-based:
afc.read(buf, 0L, buf, new CompletionHandler<Integer, ByteBuffer>() {
    @Override public void completed(Integer result, ByteBuffer attachment) {
        attachment.flip();
        processBuffer(attachment);
    }
    @Override public void failed(Throwable exc, ByteBuffer attachment) {
        log.error("Read failed", exc);
    }
});

// Async server socket channel:
AsynchronousServerSocketChannel server =
    AsynchronousServerSocketChannel.open().bind(new InetSocketAddress(8080));
server.accept(null, new CompletionHandler<AsynchronousSocketChannel, Void>() {
    @Override public void completed(AsynchronousSocketChannel client, Void att) {
        server.accept(null, this); // accept next connection immediately
        handleClient(client);
    }
    @Override public void failed(Throwable exc, Void att) { log.error("Accept failed", exc); }
});
```

---

**Q74. Spring Data Redis — caching and data structures.**
```java
@Configuration
public class RedisConfig {
    @Bean RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory cf) {
        RedisTemplate<String, Object> tpl = new RedisTemplate<>();
        tpl.setConnectionFactory(cf);
        tpl.setKeySerializer(new StringRedisSerializer());
        tpl.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        tpl.setHashKeySerializer(new StringRedisSerializer());
        tpl.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        return tpl;
    }
}

@Service @RequiredArgsConstructor
public class SessionService {
    private final RedisTemplate<String, Object> redis;
    private final StringRedisTemplate stringRedis;

    // String operations:
    public void setSession(String token, UserSession session, Duration ttl) {
        redis.opsForValue().set("session:" + token, session, ttl);
    }
    public UserSession getSession(String token) {
        return (UserSession) redis.opsForValue().get("session:" + token);
    }

    // Hash operations:
    public void updateUserField(String userId, String field, Object value) {
        redis.opsForHash().put("user:" + userId, field, value);
    }
    public Map<Object, Object> getUser(String userId) {
        return redis.opsForHash().entries("user:" + userId);
    }

    // Sorted Set — leaderboard:
    public void updateScore(String userId, double score) {
        redis.opsForZSet().add("leaderboard", userId, score);
    }
    public Set<ZSetOperations.TypedTuple<Object>> getTopN(int n) {
        return redis.opsForZSet().reverseRangeWithScores("leaderboard", 0, n - 1);
    }

    // Rate limiting with atomic increment:
    public boolean isRateLimited(String ip) {
        String key = "ratelimit:" + ip + ":" + (System.currentTimeMillis() / 60_000);
        Long count = redis.opsForValue().increment(key);
        if (count == 1) redis.expire(key, Duration.ofMinutes(1));
        return count > 100;
    }
}
```

---

**Q75. Spring Boot + PostgreSQL + Flyway migrations.**
```java
// Flyway: database migration tool — versioned SQL scripts.
// Files: src/main/resources/db/migration/
//   V1__create_users.sql
//   V2__add_indexes.sql
//   V3__create_orders.sql
// (V{version}__{description}.sql)

// Dependency: flyway-core
// Auto-runs on startup: spring.flyway.enabled=true (default)
// Runs pending migrations in version order before app starts.

// Spring Boot Flyway properties:
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true   // use on existing DBs
spring.flyway.out-of-order=false         // enforce order
spring.flyway.validate-on-migrate=true   // verify applied migrations match files

// Example migration SQL:
// V1__create_users.sql:
// CREATE TABLE users (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   email VARCHAR(255) NOT NULL UNIQUE,
//   name VARCHAR(255) NOT NULL,
//   created_at TIMESTAMPTZ DEFAULT NOW(),
//   updated_at TIMESTAMPTZ DEFAULT NOW()
// );
// CREATE INDEX idx_users_email ON users(email);

// Test with @FlywayTest:
@SpringBootTest @Transactional
@Sql("/db/test-data/users.sql")  // insert test data, rolled back after test
class UserRepositoryTest { ... }

// Programmatic migration (e.g., conditional):
@Component
public class DataMigration {
    @Autowired Flyway flyway;
    @PostConstruct void migrate() {
        if (needsSpecialMigration()) flyway.repair();
        flyway.migrate();
    }
}
```

---

**Q76. Java — immutable collections and value-based classes.**
```java
// Immutable collection factory methods (Java 9+):
List<String> list  = List.of("a", "b", "c");          // no nulls, no mutation
Set<Integer> set   = Set.of(1, 2, 3);                  // no nulls, no duplicates
Map<String, Integer> map = Map.of("one", 1, "two", 2); // up to 10 entries
Map<String, Integer> bigMap = Map.ofEntries(
    Map.entry("a", 1), Map.entry("b", 2), Map.entry("c", 3));

// All throw UnsupportedOperationException on mutation:
list.add("d");  // throws!

// Copies (defensive — safe to share):
List<String> copy = List.copyOf(mutableList);          // unmodifiable snapshot
Set<String>  sc   = Set.copyOf(existingSet);

// Collections.unmodifiable wrappers (backed by original — NOT snapshot):
List<String> wrapped = Collections.unmodifiableList(mutableList);
mutableList.add("x"); // STILL appears in wrapped! (just blocks writes through wrapped)

// VALUE-BASED CLASSES (Java 16+): LocalDate, Optional, records
// - Do not use == for identity comparison
// - May have multiple instances representing same value
// - Immutable, no meaningful identity

// Guava (3rd party) for richer immutable collections:
ImmutableList<String> il = ImmutableList.of("a", "b", "c");
ImmutableMap<String, Integer> im = ImmutableMap.<String, Integer>builder()
    .put("a", 1).put("b", 2).build();
ImmutableSortedSet<Integer> iss = ImmutableSortedSet.of(3, 1, 4, 1, 5); // {1, 3, 4, 5}
```

---

**Q77. Spring Security — method-level security.**
```java
@Configuration @EnableMethodSecurity  // (replaces @EnableGlobalMethodSecurity)
public class MethodSecurityConfig { }

@Service
public class DocumentService {
    @PreAuthorize("hasRole('ADMIN') or hasAuthority('DOCUMENT_READ')")
    public Document findById(UUID id) { return docRepo.findById(id).orElseThrow(); }

    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.name")
    public List<Document> findByUser(String userId) { return docRepo.findByUserId(userId); }

    @PostAuthorize("returnObject.ownerId == authentication.name or hasRole('ADMIN')")
    public Document findSecure(UUID id) { return docRepo.findById(id).orElseThrow(); }

    @PreFilter("filterObject.ownerId == authentication.name") // filter input collection
    public void processDocuments(List<Document> docs) { }

    @PostFilter("filterObject.visibility == 'PUBLIC' or hasRole('ADMIN')") // filter result
    public List<Document> findAll() { return docRepo.findAll(); }

    @Secured({"ROLE_ADMIN", "ROLE_MANAGER"})  // simpler but less powerful
    public void deleteDocument(UUID id) { docRepo.deleteById(id); }
}

// Custom permission evaluator:
@Component
public class DocumentPermissionEvaluator implements PermissionEvaluator {
    @Override
    public boolean hasPermission(Authentication auth, Object target, Object permission) {
        if (target instanceof Document doc) {
            return switch (permission.toString()) {
                case "read"   -> doc.isPublic() || doc.getOwnerId().equals(auth.getName());
                case "write"  -> doc.getOwnerId().equals(auth.getName());
                default       -> false;
            };
        }
        return false;
    }
}
// Usage: @PreAuthorize("hasPermission(#doc, 'write')")
```

---

**Q78. Java concurrency patterns — producer-consumer.**
```java
// BOUNDED BLOCKING QUEUE — classic producer-consumer:
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100); // capacity 100

// Producer (blocks when full):
ExecutorService producers = Executors.newFixedThreadPool(4);
for (int i = 0; i < 4; i++) {
    producers.submit(() -> {
        while (!Thread.currentThread().isInterrupted()) {
            Task task = generateTask();
            queue.put(task); // blocks if queue full
        }
    });
}

// Consumer (blocks when empty):
ExecutorService consumers = Executors.newFixedThreadPool(8);
for (int i = 0; i < 8; i++) {
    consumers.submit(() -> {
        while (true) {
            Task task = queue.poll(5, TimeUnit.SECONDS); // blocks up to 5s
            if (task == null) break; // timeout → shutdown signal
            processTask(task);
        }
    });
}

// DISRUPTOR PATTERN — lock-free ring buffer (LMAX Disruptor):
// Single writer principle → CAS instead of locks → extremely high throughput
// Used in: trading systems, high-perf messaging, logging frameworks (Log4j2)

// WORK STEALING — ForkJoinPool:
// Each worker thread has its own deque.
// Idle threads steal tasks from tail of busy thread's deque.
// → Better cache locality for the primary worker, but still feeds idle workers.
ForkJoinPool customPool = new ForkJoinPool(
    Runtime.getRuntime().availableProcessors(),
    ForkJoinPool.defaultForkJoinWorkerThreadFactory,
    null, true); // asyncMode=true for stream-like tasks
```

---

**Q79. Spring MVC — interceptors, filters, and middleware.**
```java
// FILTER (Servlet-level — before DispatcherServlet):
@Component @Order(1)
public class RequestLoggingFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse resp,
                                     FilterChain chain) throws ServletException, IOException {
        long start = System.currentTimeMillis();
        String requestId = UUID.randomUUID().toString();
        req.setAttribute("requestId", requestId);
        MDC.put("requestId", requestId);  // Logback/SLF4J MDC for log correlation
        try {
            chain.doFilter(req, resp);
        } finally {
            long elapsed = System.currentTimeMillis() - start;
            log.info("{} {} {} {}ms", req.getMethod(), req.getRequestURI(),
                resp.getStatus(), elapsed);
            MDC.clear();
        }
    }
}

// INTERCEPTOR (Spring MVC level — after DispatcherServlet):
@Component
public class AuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse resp,
                             Object handler) {
        String token = req.getHeader("X-Api-Key");
        if (token == null || !apiKeyService.isValid(token)) {
            resp.setStatus(HttpStatus.UNAUTHORIZED.value());
            return false; // stop processing
        }
        return true; // continue
    }

    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse resp,
                                Object handler, Exception ex) {
        // cleanup after response sent
    }
}

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/auth/**", "/api/health");
    }
}
```

---

**Q80. Java — key interview traps and puzzles.**
```java
// TRAP 1: String switch with null → NullPointerException
switch (nullableStr) { case "a": break; } // NPE if null

// TRAP 2: Integer overflow
int max = Integer.MAX_VALUE;
System.out.println(max + 1); // -2147483648 (wraps!)
long safe = (long) max + 1;  // 2147483648 ✓

// TRAP 3: Floating-point equality
0.1 + 0.2 == 0.3; // false! (0.30000000000000004)
Math.abs(0.1 + 0.2 - 0.3) < 1e-9; // correct comparison
BigDecimal.valueOf(0.1).add(BigDecimal.valueOf(0.2)).equals(BigDecimal.valueOf(0.3)); // true

// TRAP 4: Array covariance
String[] strings = new String[1];
Object[] objects = strings; // compiles!
objects[0] = 42; // ArrayStoreException at runtime!

// TRAP 5: ConcurrentModificationException
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
for (String s : list) { if (s.equals("b")) list.remove(s); } // EXCEPTION!
list.removeIf(s -> s.equals("b")); // ✓ correct way

// TRAP 6: substring memory leak (Java 7u5 and earlier — String retains original char[])
// Fixed in Java 7u6 — no longer an issue in modern Java

// TRAP 7: Static field in test causes test pollution
// Solution: use @DirtiesContext or reset state in @BeforeEach

// TRAP 8: Double-checked locking without volatile:
private static MyClass instance;  // NOT volatile → broken!
private static volatile MyClass instance; // ✓ correct

// TRAP 9: Exception swallowing:
try { riskyOp(); }
catch (Exception e) { } // NEVER do this — silently ignores errors!
catch (Exception e) { log.error("...", e); throw e; } // always log and/or rethrow
```

---

## HARD (Q101–Q150)

---

**Q101. JVM GC deep dive — G1 GC internals.**
```
G1 GC DESIGN:
  Heap divided into equal-sized regions (1–32MB each, total ~2048 regions).
  Regions tagged as: Eden, Survivor, Old, Humongous (objects > 50% region size).
  No fixed young/old gen boundary — regions reassigned dynamically.

PHASES:
  1. YOUNG GC (Minor):
     - Stop-the-world (STW), parallel threads.
     - Evacuates Eden + Survivors → new Survivor or Old regions.
     - Updates Remembered Sets (RSet: who references this region from outside).
     - Target: meet MaxGCPauseMillis.

  2. CONCURRENT MARKING CYCLE (when heap > InitiatingHeapOccupancyPercent ~45%):
     a. Initial Mark (STW, piggybacked on Young GC): mark GC roots
     b. Root Region Scan (concurrent): scan survivor regions
     c. Concurrent Mark (concurrent): mark live objects in parallel with app
     d. Remark (STW): handle objects changed since concurrent mark (SATB barrier)
     e. Cleanup (STW + concurrent): identify empty regions, update RSets

  3. MIXED GC:
     After marking, collect Young + selected Old regions.
     Selects regions with most garbage (highest ROI).
     Mixed GC collections until old gen is clean enough.

  4. FULL GC (fallback, STW single-threaded):
     Happens if G1 can't keep up with allocation rate.
     Means: heap too small, GC threads too few, or allocation rate too high.

TUNING FLAGS:
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200        (target, not guarantee)
  -XX:G1HeapRegionSize=16m        (tune for humongous object threshold)
  -XX:ParallelGCThreads=8         (STW parallel threads)
  -XX:ConcGCThreads=2             (concurrent marking threads)
  -XX:InitiatingHeapOccupancyPercent=45

G1 vs ZGC:
  G1:  pause < 200ms, good for most apps, default since Java 9
  ZGC: pause < 1ms, concurrent compaction, for latency-critical apps
```

---

**Q102. Java Memory Model — happens-before and reordering.**
```java
// JMM defines when one thread's writes are VISIBLE to another thread.
// Without synchronization, the JMM allows compilers/CPUs to reorder operations.

// HAPPENS-BEFORE RELATIONSHIPS:
// 1. Program order: each action HB next action in same thread
// 2. Monitor lock: unlock HB subsequent lock of same monitor
// 3. Volatile write: write HB subsequent read of same volatile variable
// 4. Thread start: Thread.start() HB any action in the new thread
// 5. Thread join: all actions in thread HB Thread.join() returning
// 6. Transitivity: if A HB B and B HB C → A HB C

// BROKEN double-checked locking (non-volatile):
private static Singleton instance;  // missing volatile!
public static Singleton getInstance() {
    if (instance == null) {
        synchronized(Singleton.class) {
            if (instance == null) {
                instance = new Singleton(); // UNSAFE!
                // JVM may reorder:
                // 1. allocate memory
                // 2. assign to instance   ← another thread sees non-null but uninitialized!
                // 3. call constructor
            }
        }
    }
    return instance; // may return partially-constructed object!
}

// FIXED with volatile:
private static volatile Singleton instance; // volatile write HB volatile read → safe

// SAFE PUBLICATION patterns:
// 1. static field (class init is thread-safe):
private static final Singleton INSTANCE = new Singleton(); // safe

// 2. Initialization-on-demand holder:
private static class Holder { static final Singleton INSTANCE = new Singleton(); }

// 3. Immutable objects are always safely published (fields final → guaranteed visibility)
// 4. volatile / synchronized / AtomicReference for mutable objects

// FALSE SHARING:
@Contended // jdk.internal.vm.annotation (or @sun.misc.Contended with JVM flag)
class PaddedCounter {
    volatile long value; // on its own 64-byte cache line → no false sharing
}
```

---

**Q103. Advanced Spring Security — OAuth2 resource server.**
```java
@Configuration @EnableWebSecurity
public class ResourceServerConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .decoder(jwtDecoder())
                    .jwtAuthenticationConverter(jwtAuthConverter())))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasAuthority("SCOPE_admin")
                .anyRequest().hasAuthority("SCOPE_api"))
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .build();
    }

    @Bean
    JwtDecoder jwtDecoder() {
        // Validate JWT with JWKS from Auth server:
        return NimbusJwtDecoder.withJwkSetUri("https://auth.example.com/.well-known/jwks.json")
                               .build();
    }

    @Bean
    JwtAuthenticationConverter jwtAuthConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthConverter = new JwtGrantedAuthoritiesConverter();
        grantedAuthConverter.setAuthoritiesClaimName("permissions"); // custom claim
        grantedAuthConverter.setAuthorityPrefix("PERMISSION_");
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(grantedAuthConverter);
        return converter;
    }
}

// Accessing JWT claims in controller:
@GetMapping("/me")
public UserProfile me(@AuthenticationPrincipal Jwt jwt) {
    String userId = jwt.getSubject();
    List<String> roles = jwt.getClaimAsStringList("roles");
    return userService.findById(userId);
}
```

---

**Q104. Spring Reactive WebClient — non-blocking HTTP client.**
```java
@Configuration
public class WebClientConfig {
    @Bean
    WebClient userServiceClient() {
        return WebClient.builder()
            .baseUrl("https://user-service")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .filter(ExchangeFilterFunction.ofRequestProcessor(req -> {
                log.debug("Request: {} {}", req.method(), req.url()); return Mono.just(req);
            }))
            .filter(retryFilter())
            .codecs(c -> c.defaultCodecs().maxInMemorySize(2 * 1024 * 1024)) // 2MB
            .build();
    }

    private ExchangeFilterFunction retryFilter() {
        return (req, next) -> next.exchange(req)
            .retryWhen(Retry.backoff(3, Duration.ofMillis(500))
                .filter(ex -> ex instanceof WebClientResponseException wce && wce.getStatusCode().is5xxServerError()));
    }
}

@Service @RequiredArgsConstructor
public class UserClient {
    private final WebClient userServiceClient;

    public Mono<User> findById(String id) {
        return userServiceClient.get()
            .uri("/api/users/{id}", id)
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError,
                r -> r.bodyToMono(ErrorResponse.class).map(e -> new UserNotFoundException(e.message())))
            .onStatus(HttpStatusCode::is5xxServerError,
                r -> Mono.error(new ServiceUnavailableException("user-service down")))
            .bodyToMono(User.class)
            .timeout(Duration.ofSeconds(5))
            .cache(Duration.ofMinutes(1)); // cache result for 1 minute
    }

    public Flux<User> findAll(List<String> ids) {
        return Flux.fromIterable(ids)
            .flatMap(id -> findById(id).onErrorResume(e -> Mono.empty()), 10); // concurrency 10
    }
}
```

---

**Q105. Advanced JPA — second-level cache and query hints.**
```java
// SECOND-LEVEL CACHE (entity cache across sessions):
// Add Ehcache or Hazelcast as JPA cache provider

@Entity
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE) // Hibernate @Cache
public class Country {
    @Id Long id;
    String name;
    // Rarely changes → good candidate for L2 cache
}

// Enable in properties:
spring.jpa.properties.hibernate.cache.use_second_level_cache=true
spring.jpa.properties.hibernate.cache.region.factory_class=
    org.hibernate.cache.jcache.JCacheRegionFactory

// Query cache:
@Query("SELECT c FROM Country c ORDER BY c.name")
@QueryHints(value = @QueryHint(name = "org.hibernate.cacheable", value = "true"))
List<Country> findAllCached();

// QUERY HINTS for performance:
@QueryHints({
    @QueryHint(name = "jakarta.persistence.query.timeout", value = "5000"),
    @QueryHint(name = "org.hibernate.readOnly", value = "true"),
    @QueryHint(name = "org.hibernate.fetchSize", value = "100") // JDBC batch fetch
})
@Query("SELECT u FROM User u")
List<User> findAllReadOnly();

// STATELESS SESSION — bulk operations without dirty checking:
@PersistenceContext EntityManager em;
Session hibernateSession = em.unwrap(Session.class);
try (StatelessSession ss = hibernateSession.getSessionFactory().openStatelessSession()) {
    ScrollableResults<Product> results = ss.createQuery("FROM Product", Product.class)
        .scroll(ScrollMode.FORWARD_ONLY);
    while (results.next()) {
        Product p = results.get();
        p.setPrice(p.getPrice().multiply(BigDecimal.valueOf(1.1)));
        ss.update(p); // no dirty checking, no first-level cache
    }
}
```

---

**Q106. Advanced concurrency — ConcurrentHashMap internals.**
```java
// ConcurrentHashMap Java 8: segment locks removed → per-NODE locking
// Structure: array of Nodes (linked list or TreeNode when > 8 entries)
// PUT: uses CAS for empty bucket, synchronized on first node for collision bucket
// GET: lock-free (volatile reads)

ConcurrentHashMap<String, List<Integer>> map = new ConcurrentHashMap<>();

// Atomic compute operations:
map.compute("key", (k, existing) -> {
    if (existing == null) return new ArrayList<>();
    existing.add(42); return existing;
}); // entire compute is atomic — no separate get/put needed

map.computeIfAbsent("key", k -> new CopyOnWriteArrayList<>()); // thread-safe init

// merge — update existing or set new:
map.merge("count", 1, Integer::sum); // if "count" exists: sum; else: put 1

// forEach, reduce, search with parallelism threshold:
map.forEach(10_000L, (k, v) -> process(k, v)); // parallelise if > 10K entries
String found = map.search(10_000L, (k, v) -> v > 100 ? k : null);
int total = map.reduceValues(10_000L, v -> (Integer) v, Integer::sum);

// LongAdder for high-contention counters (better than AtomicLong):
ConcurrentHashMap<String, LongAdder> counters = new ConcurrentHashMap<>();
counters.computeIfAbsent("event", k -> new LongAdder()).increment();
// LongAdder uses multiple cells to reduce contention → much faster than AtomicLong
long total2 = counters.get("event").sum(); // sum all cells at read time
```

---

**Q107. Spring transaction internals — how @Transactional works.**
```
TRANSACTION PROXY MECHANISM:
  1. Spring creates a CGLIB proxy (or JDK dynamic proxy for interfaces) wrapping your bean.
  2. When you call @Transactional method through Spring container, the CALL goes to the PROXY.
  3. Proxy intercepts: checks for existing transaction, creates one if needed (per propagation).
  4. Calls actual method on the target object.
  5. On return: commits transaction.
  6. On exception: rolls back (RuntimeException/Error by default).

PROXY LIMITATION (self-invocation):
  @Service class OrderService {
      @Transactional void outer() { this.inner(); } // goes to target, NOT proxy → no TX!
      @Transactional void inner() { }
  }
  this.inner() bypasses the proxy → @Transactional on inner() is ignored.

  FIXES:
  a) Inject self: @Autowired @Lazy OrderService self; self.inner();
  b) Move inner() to a separate bean.
  c) Use AspectJ mode: @EnableTransactionManagement(mode = AdviceMode.ASPECTJ)
     (AspectJ weaves bytecode at compile-time, works on self-calls)

TRANSACTION SYNCHRONIZATION:
  After TX commit, Spring can fire post-commit hooks:
  TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
      @Override public void afterCommit() { sendEmail(); } // only if TX committed
  });
  @TransactionalEventListener does this automatically.

DISTRIBUTED TRANSACTIONS (XA):
  JTA + XA datasources for multiple databases in one TX.
  Modern alternative: SAGA pattern (compensating transactions, eventually consistent).
```

---

**Q108. Pattern matching and sealed types — advanced.**
```java
// Pattern matching switch (Java 21):
sealed interface Expr permits Num, Add, Mul, Neg {}
record Num(int value)      implements Expr {}
record Add(Expr l, Expr r) implements Expr {}
record Mul(Expr l, Expr r) implements Expr {}
record Neg(Expr expr)      implements Expr {}

// Recursive evaluator with pattern matching:
int eval(Expr e) {
    return switch (e) {
        case Num(int v)         -> v;
        case Add(Expr l, Expr r) -> eval(l) + eval(r);
        case Mul(Expr l, Expr r) -> eval(l) * eval(r);
        case Neg(Expr inner)     -> -eval(inner);
    }; // exhaustive — no default needed (sealed)
}

// Pretty printer:
String pretty(Expr e) {
    return switch (e) {
        case Num(int v)          -> String.valueOf(v);
        case Add(Expr l, Expr r) -> "(" + pretty(l) + " + " + pretty(r) + ")";
        case Mul(Expr l, Expr r) -> "(" + pretty(l) + " * " + pretty(r) + ")";
        case Neg(Expr inner)     -> "-" + pretty(inner);
    };
}

// Usage:
Expr expr = new Add(new Mul(new Num(2), new Num(3)), new Neg(new Num(4)));
System.out.println(pretty(expr)); // "(2 * 3) + (-4)"
System.out.println(eval(expr));   // 2
```

---

**Q109. Java — writing high-performance code.**
```java
// 1. AVOID OBJECT ALLOCATION IN HOT PATHS:
// Bad — creates new object every call:
public String formatDate(LocalDate d) { return DateTimeFormatter.ofPattern("yyyy-MM-dd").format(d); }
// Good — reuse formatter (immutable, thread-safe):
private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");
public String formatDate(LocalDate d) { return FMT.format(d); }

// 2. USE PRIMITIVE COLLECTIONS:
// Eclipse Collections / Koloboke:
MutableIntList list = IntLists.mutable.with(1, 2, 3);
MutableIntIntMap map = IntIntMaps.mutable.empty();
map.put(1, 100); map.get(1); // no boxing

// 3. FLYWEIGHT PATTERN — share immutable instances:
class Color {
    private static final Map<String, Color> POOL = new ConcurrentHashMap<>();
    public static Color of(String name) {
        return POOL.computeIfAbsent(name, Color::new);
    }
    private Color(String name) { this.name = name; }
}

// 4. ARRAY vs ARRAYLIST:
// For known-size fixed collections: int[] vs ArrayList<Integer>
// int[1000] = 4KB; ArrayList<Integer>(1000) = ~16KB (wrapper objects + ArrayList overhead)

// 5. BATCH DATABASE OPERATIONS:
// Instead of N inserts, use batch:
entityManager.persist(entity);
if (i % 50 == 0) { entityManager.flush(); entityManager.clear(); } // batch of 50

// JDBC batch:
PreparedStatement ps = conn.prepareStatement("INSERT INTO items VALUES (?, ?)");
for (Item item : items) {
    ps.setString(1, item.id()); ps.setString(2, item.name()); ps.addBatch();
}
ps.executeBatch();

// 6. CACHE HOT DATA:
// Application-level: Caffeine (fast in-JVM LRU/W-TinyLFU cache)
Cache<String, User> cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(5))
    .recordStats()
    .build();
```

---

**Q110. Spring Boot GraphQL.**
```java
// Dependency: spring-boot-starter-graphql

// Schema: src/main/resources/graphql/schema.graphqls
// type Query { user(id: ID!): User }
// type User { id: ID!, name: String!, orders: [Order!]! }

@Controller
public class UserGraphQLController {
    @Autowired UserService userService;
    @Autowired OrderService orderService;

    @QueryMapping                           // maps to Query.user in schema
    public User user(@Argument String id) {
        return userService.findById(UUID.fromString(id));
    }

    @SchemaMapping(typeName = "User", field = "orders") // resolves User.orders
    public List<Order> orders(User user) {
        return orderService.findByUserId(user.getId());
    }

    @MutationMapping
    public User createUser(@Argument CreateUserInput input) {
        return userService.create(input);
    }

    @SubscriptionMapping
    public Flux<Order> orderUpdates(@Argument String userId) {
        return orderEventService.streamOrdersForUser(userId);
    }
}

// DataLoader to avoid N+1 in GraphQL:
@Component
public class OrderDataLoader implements BatchLoaderWithContext<UUID, List<Order>> {
    @Override
    public CompletionStage<List<List<Order>>> load(List<UUID> userIds, BatchLoaderEnvironment env) {
        Map<UUID, List<Order>> map = orderService.findByUserIds(userIds);
        return CompletableFuture.completedFuture(
            userIds.stream().map(id -> map.getOrDefault(id, List.of())).collect(toList()));
    }
}
```

---

**Q111. Java agents and bytecode instrumentation.**
```java
// Java agents can transform class bytecode at load time.
// Used by: profilers (JProfiler, async-profiler), APM (Datadog, New Relic),
//          code coverage (JaCoCo), mocking frameworks (Mockito).

// JAVAAGENT manifest:
// Premain-Class: com.example.MyAgent
// Agent-Class: com.example.MyAgent  (for dynamic attach)
// Can-Redefine-Classes: true
// Can-Retransform-Classes: true

public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        inst.addTransformer(new TimingTransformer(), true);
    }
}

public class TimingTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> cls,
                            ProtectionDomain domain, byte[] bytecode) {
        if (!className.startsWith("com/example/service/")) return null; // no transform
        // Use Byte Buddy / ASM / Javassist to modify bytecode:
        try {
            return new ByteBuddy()
                .redefine(cls)
                .method(ElementMatchers.isPublic())
                .intercept(MethodDelegation.to(TimingInterceptor.class))
                .make().getBytes();
        } catch (Exception e) { return null; } // null = don't transform
    }
}

// Byte Buddy (simpler API than raw ASM):
new AgentBuilder.Default()
    .type(ElementMatchers.nameStartsWith("com.example.service"))
    .transform((builder, type, cl, md, pd) ->
        builder.method(ElementMatchers.isPublic())
               .intercept(MethodDelegation.to(TimingAdvice.class)))
    .installOn(instrumentation);
```

---

**Q112. Reactive streams — backpressure and schedulers.**
```java
// BACKPRESSURE: slow consumer signals to fast producer to slow down.
// In Project Reactor: Flux/Mono handle backpressure via demand signalling (request(n))

// Backpressure strategies:
Flux<Integer> source = Flux.range(1, 1_000_000);

source.onBackpressureBuffer(1000)       // buffer up to 1000, then error
source.onBackpressureLatest()           // keep only latest, drop old
source.onBackpressureDrop()             // drop items when downstream is slow
source.onBackpressureDrop(dropped -> log.warn("Dropped: {}", dropped))
source.onBackpressureError()            // error if downstream can't keep up

// SCHEDULERS — control which thread pool operations run on:
Flux.fromCallable(() -> blockingJdbcCall()) // blocking call
    .subscribeOn(Schedulers.boundedElastic())  // run blocking work here
    .publishOn(Schedulers.parallel())          // process results here
    .map(result -> transform(result))          // CPU work on parallel scheduler
    .subscribeOn(Schedulers.single());         // single thread for ordering

// Schedulers.parallel()       — fixed pool, size = CPU cores (CPU-bound work)
// Schedulers.boundedElastic() — elastic pool (bounded), ideal for blocking IO
// Schedulers.single()         — single thread (sequential, ordered)
// Schedulers.immediate()      — current thread (no switching)

// Zip multiple reactive sources:
Mono.zip(
    userService.findById(id).subscribeOn(Schedulers.boundedElastic()),
    orderService.findByUserId(id).subscribeOn(Schedulers.boundedElastic()),
    inventoryService.getStock().subscribeOn(Schedulers.boundedElastic())
).map(tuple -> new Dashboard(tuple.getT1(), tuple.getT2(), tuple.getT3()));
// All 3 fetched concurrently, zip waits for all
```

---

**Q113. Java — module system deep dive (JPMS).**
```java
// STRONG ENCAPSULATION: packages not listed in exports are inaccessible
// even via reflection by default (unlike pre-module classpath)

// module-info.java (full example):
module com.example.webapp {
    // Require standard modules:
    requires java.sql;
    requires java.net.http;

    // Transitive: dependents automatically get these too:
    requires transitive com.fasterxml.jackson.databind;

    // Static: compile-time only (optional at runtime):
    requires static lombok;

    // Export API to all:
    exports com.example.webapp.api;
    exports com.example.webapp.dto;

    // Export internals to specific trusted modules:
    exports com.example.webapp.internal to com.example.webapp.tests;

    // Open for reflection (needed by Jackson, Spring, Hibernate):
    opens com.example.webapp.model to com.fasterxml.jackson.databind;
    opens com.example.webapp.config to org.springframework.core;

    // Open all packages for full reflection (avoid if possible):
    // opens com.example.webapp;  // all packages

    // Service Provider Interface:
    provides com.example.spi.Serializer with com.example.webapp.JsonSerializer;
    uses com.example.spi.Authenticator; // discovers providers via ServiceLoader
}

// --add-opens to bypass strong encapsulation at runtime (legacy libs):
// java --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED

// Layer API — load modules dynamically:
ModuleFinder finder = ModuleFinder.of(Path.of("plugins/"));
ModuleLayer parent = ModuleLayer.boot();
Configuration cfg = parent.configuration().resolve(finder, ModuleFinder.of(), Set.of("plugin.module"));
ModuleLayer layer = parent.defineModulesWithOneLoader(cfg, ClassLoader.getSystemClassLoader());
Class<?> pluginClass = layer.findLoader("plugin.module").loadClass("com.example.Plugin");
```

---

**Q114. GraalVM Native Image.**
```java
// Native Image: AOT (Ahead-of-Time) compilation → standalone native binary.
// Benefits: near-instant startup (ms vs seconds), tiny memory footprint.
// Used by: serverless, CLIs, microservices, Quarkus, Micronaut, Spring Native.

// Build:
// native-image -jar myapp.jar   (standalone binary, no JVM needed)
// Spring Boot: ./mvnw -Pnative native:compile

// LIMITATIONS:
// No runtime class loading (must know all classes at compile-time)
// No dynamic proxies by default (must configure)
// No bytecode modification at runtime
// Reflection requires explicit config

// REFLECTION CONFIG (reflect-config.json or @RegisterReflectionForBinding):
// [{ "name": "com.example.User",
//    "allDeclaredConstructors": true,
//    "allDeclaredFields": true,
//    "allDeclaredMethods": true }]

// Spring Native: @SpringBootApplication auto-processes most reflection
// Custom: @RegisterReflectionForBinding(User.class, OrderDTO.class)

// TRACING AGENT — generate configs automatically by running tests:
// java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image ...

// Native Image build hints in Spring:
@Configuration @ImportRuntimeHints(MyRuntimeHints.class)
public class MyConfig {}
public class MyRuntimeHints implements RuntimeHintsRegistrar {
    @Override public void registerHints(RuntimeHints hints, ClassLoader cl) {
        hints.reflection().registerType(MyClass.class, MemberCategory.INVOKE_PUBLIC_METHODS);
        hints.resources().registerPattern("templates/*.html");
        hints.proxies().registerJdkProxy(MyInterface.class);
    }
}
```

---

**Q115. Testing — advanced Mockito patterns.**
```java
// ARGUMENT CAPTORS:
ArgumentCaptor<Order> orderCaptor = ArgumentCaptor.forClass(Order.class);
verify(orderRepo).save(orderCaptor.capture());
Order savedOrder = orderCaptor.getValue();
assertEquals("PENDING", savedOrder.getStatus());
assertNotNull(savedOrder.getCreatedAt());

// Multiple captures:
verify(emailService, times(3)).sendEmail(
    argThat(email -> email.getTo().contains("@example.com")),
    anyString()
);

// SPIES (partial mocking — real object with some methods mocked):
@Spy OrderService realOrderService = new OrderService(repo, paymentService);
doReturn(mock).when(realOrderService).expensiveOperation(); // stub one method
realOrderService.processOrders(); // other methods call real code

// ANSWER for dynamic responses:
when(repo.save(any())).thenAnswer(invocation -> {
    Order order = invocation.getArgument(0);
    order.setId(UUID.randomUUID()); // simulate DB-generated ID
    return order;
});

// SEQUENTIAL STUBBING:
when(service.getData())
    .thenReturn("first")
    .thenReturn("second")
    .thenThrow(new RuntimeException("third call fails"));

// IN-ORDER verification:
InOrder inOrder = inOrder(firstService, secondService);
inOrder.verify(firstService).validateOrder(any());
inOrder.verify(secondService).chargePayment(any());  // must happen after validate
inOrder.verify(firstService).fulfillOrder(any());

// MOCK STATIC METHODS (Mockito 3.4+):
try (MockedStatic<UUID> uuidMock = mockStatic(UUID.class)) {
    UUID fixed = UUID.fromString("00000000-0000-0000-0000-000000000001");
    uuidMock.when(UUID::randomUUID).thenReturn(fixed);
    Order order = orderService.createOrder(req);
    assertEquals(fixed, order.getId());
}
```

---

**Q116. Spring Boot — production-ready patterns.**
```java
// CIRCUIT BREAKER + BULKHEAD + RATE LIMITER (Resilience4j):
@Service
public class ExternalApiService {
    @CircuitBreaker(name = "extApi", fallbackMethod = "fallback")
    @Bulkhead(name = "extApi", type = Bulkhead.Type.SEMAPHORE)
    @RateLimiter(name = "extApi")
    @Retry(name = "extApi")
    public Data fetchData(String id) { return restTemplate.getForObject("...", Data.class); }

    private Data fallback(String id, Exception ex) { return Data.empty(); }
}

// application.yml:
resilience4j:
  circuitbreaker.instances.extApi:
    sliding-window-size: 20
    failure-rate-threshold: 50
    wait-duration-in-open-state: 10s
  bulkhead.instances.extApi:
    max-concurrent-calls: 20
  ratelimiter.instances.extApi:
    limit-for-period: 100
    limit-refresh-period: 1s

// GRACEFUL SHUTDOWN (Spring Boot 2.3+):
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
// On SIGTERM: stops accepting new requests, waits up to 30s for in-flight to complete.

// READINESS + LIVENESS probes (Kubernetes):
management.health.probes.enabled=true
// /actuator/health/liveness  → LivenessState.CORRECT / BROKEN
// /actuator/health/readiness → ReadinessState.ACCEPTING_TRAFFIC / REFUSING_TRAFFIC

// Mark readiness in code:
@Autowired ApplicationEventPublisher publisher;
publisher.publishEvent(new AvailabilityChangeEvent<>(this, ReadinessState.ACCEPTING_TRAFFIC));
publisher.publishEvent(new AvailabilityChangeEvent<>(this, ReadinessState.REFUSING_TRAFFIC));
```

---

**Q117. Java concurrency — StampedLock and optimistic reads.**
```java
// StampedLock (Java 8+) — faster than ReadWriteLock for read-heavy workloads.
// Three modes: write, read, optimistic read (no lock — verify after)

private final StampedLock lock = new StampedLock();
private double x, y;

// WRITE:
public void move(double dx, double dy) {
    long stamp = lock.writeLock();
    try { x += dx; y += dy; }
    finally { lock.unlockWrite(stamp); }
}

// READ (traditional — blocks writers):
public double distanceFromOrigin() {
    long stamp = lock.readLock();
    try { return Math.sqrt(x * x + y * y); }
    finally { lock.unlockRead(stamp); }
}

// OPTIMISTIC READ — fastest, no lock acquired:
public double distanceFromOriginOptimistic() {
    long stamp = lock.tryOptimisticRead(); // returns non-zero stamp
    double localX = x, localY = y;         // read fields optimistically
    if (!lock.validate(stamp)) {           // check if write happened since tryOptimisticRead
        stamp = lock.readLock();           // fallback to real read lock
        try { localX = x; localY = y; }
        finally { lock.unlockRead(stamp); }
    }
    return Math.sqrt(localX * localX + localY * localY);
}

// LOCK CONVERSION:
public void conditionalUpdate(double newX) {
    long stamp = lock.readLock();
    try {
        if (x < newX) {
            long writeStamp = lock.tryConvertToWriteLock(stamp);
            if (writeStamp != 0L) {
                stamp = writeStamp;  // converted!
                x = newX;
            } else {
                lock.unlockRead(stamp);
                stamp = lock.writeLock();
                x = newX;
            }
        }
    } finally { lock.unlock(stamp); }
}
// Note: StampedLock is NOT reentrant — don't use if same thread may re-lock
```

---

**Q118. Advanced Hibernate — custom types and converters.**
```java
// JPA AttributeConverter — convert between Java type and DB column:
@Converter(autoApply = true)  // auto-apply to all fields of this type
public class MoneyConverter implements AttributeConverter<Money, BigDecimal> {
    @Override public BigDecimal convertToDatabaseColumn(Money money) {
        return money == null ? null : money.getAmount().setScale(2, HALF_UP);
    }
    @Override public Money convertToEntityAttribute(BigDecimal value) {
        return value == null ? null : Money.of(value, Currency.getInstance("USD"));
    }
}

// Store List<String> as JSON column:
@Converter
public class StringListConverter implements AttributeConverter<List<String>, String> {
    private static final ObjectMapper MAPPER = new ObjectMapper();
    @Override public String convertToDatabaseColumn(List<String> list) {
        try { return MAPPER.writeValueAsString(list); }
        catch (Exception e) { throw new RuntimeException(e); }
    }
    @Override public List<String> convertToEntityAttribute(String json) {
        try { return MAPPER.readValue(json, new TypeReference<>() {}); }
        catch (Exception e) { throw new RuntimeException(e); }
    }
}

@Entity public class User {
    @Convert(converter = StringListConverter.class)
    private List<String> roles;
}

// Custom Hibernate UserType (for complex types):
// Implement org.hibernate.usertype.UserType for full control over JDBC <-> Java mapping.
// Useful for: encrypted fields, binary protocols, geometric types.

// Hibernate PostgreSQL JSON column (using Jackson):
@Type(JsonType.class)  // from hibernate-types-60 library
@Column(columnDefinition = "jsonb")
private Map<String, Object> metadata;
```

---

**Q119. Spring Data — reactive repositories.**
```java
// R2DBC (Reactive Relational DB Connectivity) — non-blocking SQL
// Dependency: spring-boot-starter-data-r2dbc

@Repository
public interface UserR2dbcRepository extends ReactiveCrudRepository<User, UUID> {
    Flux<User> findByDepartment(String dept);
    Mono<User> findByEmail(String email);

    @Query("SELECT * FROM users WHERE salary > :salary ORDER BY salary DESC LIMIT :limit")
    Flux<User> findTopEarners(@Param("salary") double salary, @Param("limit") int limit);
}

@Service @RequiredArgsConstructor
public class ReactiveUserService {
    private final UserR2dbcRepository repo;
    private final ReactiveTransactionManager txManager;

    public Mono<User> createUser(CreateUserRequest req) {
        return TransactionalOperator.create(txManager)
            .transactional(
                Mono.fromCallable(() -> buildUser(req))
                    .flatMap(repo::save)
                    .flatMap(saved -> auditRepo.log(saved).thenReturn(saved))
            );
    }

    public Flux<UserDTO> findAllStream() {
        return repo.findAll()
            .publishOn(Schedulers.parallel())
            .map(user -> new UserDTO(user.getId(), user.getName()))
            .onErrorResume(DataAccessException.class, e ->
                Flux.error(new ServiceException("DB unavailable", e)));
    }
}

// application.yml:
spring.r2dbc.url=r2dbc:postgresql://localhost:5432/mydb
spring.r2dbc.username=user
spring.r2dbc.password=pass
spring.r2dbc.pool.max-size=20
```

---

**Q120. Java — records, sealed classes, and pattern matching combined.**
```java
// ALGEBRAIC DATA TYPES in Java 21 — full example:

sealed interface Result<T> permits Result.Ok, Result.Err {
    record Ok<T>(T value)      implements Result<T> {}
    record Err<T>(String error) implements Result<T> {}

    // Functional operations:
    default <U> Result<U> map(Function<T, U> fn) {
        return switch (this) {
            case Ok<T>(T v)    -> new Ok<>(fn.apply(v));
            case Err<T>(String e) -> new Err<>(e);
        };
    }
    default <U> Result<U> flatMap(Function<T, Result<U>> fn) {
        return switch (this) {
            case Ok<T>(T v)      -> fn.apply(v);
            case Err<T>(String e) -> new Err<>(e);
        };
    }
    default T getOrElse(T defaultValue) {
        return switch (this) {
            case Ok<T>(T v)    -> v;
            case Err<T> err    -> defaultValue;
        };
    }
    default T getOrThrow() {
        return switch (this) {
            case Ok<T>(T v)     -> v;
            case Err<T>(String e) -> throw new RuntimeException(e);
        };
    }
}

// Usage — Railway-oriented programming:
Result<User> findUser(String id) {
    return Optional.ofNullable(userRepo.findById(id))
        .map(Result.Ok::new)
        .orElse(new Result.Err<>("User not found: " + id));
}

Result<Profile> getProfile(String userId) {
    return findUser(userId)
        .flatMap(user -> validateUser(user))
        .map(user -> Profile.from(user));
}
```

---

**Q121. Spring Boot — multi-tenancy patterns.**
```java
// SCHEMA-BASED multi-tenancy (separate schema per tenant):
public class TenantInterceptor implements HandlerInterceptor {
    @Override public boolean preHandle(HttpServletRequest req, ...) {
        String tenantId = req.getHeader("X-Tenant-ID");
        if (tenantId == null) { resp.setStatus(400); return false; }
        TenantContext.setCurrentTenant(tenantId);
        return true;
    }
    @Override public void afterCompletion(...) { TenantContext.clear(); }
}

public class TenantAwareDataSource extends AbstractRoutingDataSource {
    @Override protected Object determineCurrentLookupKey() {
        return TenantContext.getCurrentTenant();
    }
}

// Hibernate multi-tenancy:
public class TenantConnectionProvider implements MultiTenantConnectionProvider<String> {
    @Override public Connection getConnection(String tenantId) throws SQLException {
        Connection conn = dataSource.getConnection();
        conn.createStatement().execute("SET search_path TO " + tenantId);
        return conn;
    }
    @Override public void releaseConnection(String tenantId, Connection conn) throws SQLException {
        conn.createStatement().execute("SET search_path TO public");
        conn.close();
    }
}

spring.jpa.properties.hibernate.multiTenancy=SCHEMA
spring.jpa.properties.hibernate.tenant_identifier_resolver=com.example.TenantResolver
spring.jpa.properties.hibernate.multi_tenant_connection_provider=com.example.TenantConnectionProvider
```

---

**Q122. Java — LRU cache implementation.**
```java
// LRU (Least Recently Used) cache: O(1) get and put.
// Data structure: HashMap + doubly linked list.
// HashMap for O(1) lookup. DLL for O(1) eviction (remove head) and promotion (move to tail).

public class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> map;
    private final Deque<Node<K, V>> deque = new LinkedList<>();

    record Node<K, V>(K key, V value) {}  // using record for immutability — value updated via map

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new LinkedHashMap<>(capacity, 0.75f, true) { // accessOrder=true
            @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > capacity;
            }
        };
    }

    // Actually, LinkedHashMap already does LRU! But here's manual for interviews:
    public V get(K key) {
        if (!map.containsKey(key)) return null;
        Node<K, V> node = map.get(key);
        deque.remove(node); deque.addLast(node); // move to recently used
        return node.value();
    }

    public void put(K key, V value) {
        if (map.containsKey(key)) {
            Node<K, V> old = map.get(key); deque.remove(old);
        } else if (map.size() == capacity) {
            Node<K, V> lru = deque.removeFirst(); // evict LRU
            map.remove(lru.key());
        }
        Node<K, V> node = new Node<>(key, value);
        deque.addLast(node); map.put(key, node);
    }
}

// Production: use Caffeine (faster than ConcurrentHashMap + DLL):
LoadingCache<String, User> cache = Caffeine.newBuilder()
    .maximumSize(10_000).expireAfterWrite(Duration.ofMinutes(5))
    .build(key -> userRepo.findById(key).orElse(null));
```

---

**Q123. Spring Boot — event-driven architecture with Kafka + Outbox pattern.**
```java
// OUTBOX PATTERN: avoid dual-write problem (DB + Kafka in same "transaction")
// Problem: save to DB succeeds, Kafka publish fails → inconsistency
// Solution: write event to outbox table in same DB transaction,
//           separate relay process reads outbox and publishes to Kafka.

@Entity @Table(name = "outbox_events")
public class OutboxEvent {
    @Id @GeneratedValue UUID id;
    String aggregateType;   // "ORDER"
    String aggregateId;
    String eventType;       // "ORDER_CREATED"
    @Column(columnDefinition = "jsonb") String payload;
    LocalDateTime createdAt;
    boolean published;
}

@Service @Transactional
public class OrderService {
    public Order createOrder(CreateOrderRequest req) {
        Order order = orderRepo.save(buildOrder(req));
        // Same transaction — atomic!
        outboxRepo.save(new OutboxEvent("ORDER", order.getId().toString(),
            "ORDER_CREATED", serialize(OrderCreatedEvent.from(order))));
        return order;
    }
}

// Relay — poll and publish (or use Debezium CDC for push-based):
@Scheduled(fixedDelay = 1000)
@Transactional
public void relayOutboxEvents() {
    List<OutboxEvent> pending = outboxRepo.findByPublishedFalseOrderByCreatedAtAsc(100);
    for (OutboxEvent event : pending) {
        kafkaTemplate.send(event.getAggregateType().toLowerCase(), event.getAggregateId(), event.getPayload());
        event.setPublished(true);
        outboxRepo.save(event);
    }
}
// Debezium: capture DB change log (CDC) → publish directly to Kafka → no polling needed
```

---

**Q124. Java — Design patterns for interviews (quick reference).**
```java
// PROXY — control access to object:
public interface Service { String getData(); }
public class ServiceProxy implements Service {
    private final Service real; private String cached;
    public ServiceProxy(Service real) { this.real = real; }
    @Override public String getData() {
        if (cached == null) cached = real.getData(); // caching proxy
        return cached;
    }
}
// Dynamic proxy (JDK):
Service proxy = (Service) Proxy.newProxyInstance(
    Service.class.getClassLoader(), new Class[]{Service.class},
    (p, method, args) -> {
        System.out.println("Before: " + method.getName());
        Object r = method.invoke(realService, args);
        System.out.println("After: " + method.getName());
        return r;
    });

// FLYWEIGHT — share immutable objects to save memory:
public class CharacterFactory {
    private static final Map<Character, FontCharacter> pool = new HashMap<>();
    public static FontCharacter get(char c, Font font) {
        return pool.computeIfAbsent(c, k -> new FontCharacter(k, font));
    }
}

// COMPOSITE — tree structure, treat leaf and composite uniformly:
public abstract class Component { abstract int size(); }
public class File extends Component { int size; @Override int size() { return size; } }
public class Directory extends Component {
    List<Component> children = new ArrayList<>();
    void add(Component c) { children.add(c); }
    @Override int size() { return children.stream().mapToInt(Component::size).sum(); }
}

// NULL OBJECT — avoid null checks:
public class NullUserService implements UserService {
    @Override public User findById(UUID id) { return User.ANONYMOUS; }
    @Override public void save(User u) { /* no-op */ }
}
```

---

**Q125. Java — `instanceof` pattern matching advanced.**
```java
// Type pattern (Java 16):
if (obj instanceof String s && s.length() > 5) {
    System.out.println(s.toUpperCase()); // s in scope here
}
// s is NOT in scope in else branch or after the if

// Pattern variable scope — tricky case:
if (!(obj instanceof String s)) {
    return; // s NOT accessible here (negated pattern)
}
s.toUpperCase(); // s IS accessible here (fall-through means it must be String)

// Switch pattern matching (Java 21):
String format = switch (number) {
    case Integer i when i < 0  -> "negative int: " + i;
    case Integer i             -> "positive int: " + i;
    case Long l                -> "long: " + l;
    case Double d              -> "double: " + d;
    case null                  -> "null";
    default                    -> "other: " + number;
};

// Nested deconstruction:
record Address(String city, String country) {}
record Person(String name, Address address) {}

if (person instanceof Person(String name, Address(String city, String country))) {
    System.out.printf("%s lives in %s, %s%n", name, city, country);
}

// In switch:
switch (person) {
    case Person(String name, Address(_, String country)) when country.equals("EG") ->
        System.out.println("Egyptian: " + name);
    case Person(String name, Address address) ->
        System.out.println(name + " from " + address.country());
}
```

---

**Q126. Spring Boot — observability with Micrometer Tracing.**
```java
// Distributed tracing: trace request across microservices.
// Trace ID: unique per request. Span ID: unique per operation within trace.

// Dependencies: micrometer-tracing-bridge-brave + zipkin-reporter-brave (for Zipkin)
//               or micrometer-tracing-bridge-otel (for OpenTelemetry)

// Auto-instrumented (zero code):
// - Spring MVC requests
// - WebClient/RestTemplate calls
// - Kafka producer/consumer
// - @Scheduled methods
// - @Async methods

// Custom spans:
@Service @RequiredArgsConstructor
public class OrderService {
    private final Tracer tracer;

    public Order processOrder(String orderId) {
        Span span = tracer.nextSpan().name("process-order").start();
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            span.tag("orderId", orderId);
            span.event("validation-started");
            validateOrder(orderId);
            span.event("payment-started");
            processPayment(orderId);
            return fulfillOrder(orderId);
        } catch (Exception e) {
            span.error(e);
            throw e;
        } finally {
            span.end();
        }
    }
}

// application.yml:
management.tracing.sampling.probability=1.0  # 100% in dev, 0.1 (10%) in prod
management.zipkin.tracing.endpoint=http://zipkin:9411/api/v2/spans
```

---

**Q127. JPA — native queries, stored procedures, projections.**
```java
// NATIVE SQL QUERY:
@Query(value = """
    SELECT u.id, u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > :since
    GROUP BY u.id, u.name
    HAVING COUNT(o.id) > :minOrders
    ORDER BY total_spent DESC
    LIMIT :limit
    """, nativeQuery = true)
List<UserOrderStats> findTopCustomers(@Param("since") LocalDate since,
                                      @Param("minOrders") int minOrders,
                                      @Param("limit") int limit);

// Projection interface (Spring Data):
public interface UserOrderStats {
    UUID getId();
    String getName();
    long getOrderCount();
    BigDecimal getTotalSpent();
}

// CLASS-BASED projection (DTO):
@Query("SELECT new com.example.dto.UserSummaryDTO(u.id, u.name, u.email, COUNT(o)) " +
       "FROM User u LEFT JOIN u.orders o GROUP BY u.id, u.name, u.email")
List<UserSummaryDTO> getUserSummaries();

// STORED PROCEDURE:
@Entity
@NamedStoredProcedureQuery(
    name = "User.activateExpiredUsers",
    procedureName = "activate_expired_users",
    parameters = {
        @StoredProcedureParameter(mode = IN,    name = "days_inactive", type = Integer.class),
        @StoredProcedureParameter(mode = OUT,   name = "activated_count", type = Integer.class)
    }
)
public class User { ... }

// Call it:
StoredProcedureQuery query = em.createNamedStoredProcedureQuery("User.activateExpiredUsers");
query.setParameter("days_inactive", 90);
query.execute();
int count = (int) query.getOutputParameterValue("activated_count");
```

---

**Q128. Java — reactive programming with Reactor advanced.**
```java
// HOT vs COLD:
// COLD publisher: starts fresh for each subscriber (HTTP request, file read)
// HOT publisher: shares events among all subscribers (mouse events, Kafka stream)

Flux<Integer> cold = Flux.range(1, 5); // each subscriber gets 1..5
Flux<Long> hot = Flux.interval(Duration.ofSeconds(1)).publish().refCount(1); // shared

// ConnectableFlux — multicast:
ConnectableFlux<Integer> hotSource = Flux.range(1, 10).publish();
hotSource.subscribe(System.out::println);   // subscriber 1
hotSource.subscribe(System.out::println);   // subscriber 2
hotSource.connect(); // starts emitting to BOTH subscribers

// MERGE — interleave items:
Flux<String> merged = Flux.merge(
    Flux.interval(Duration.ZERO, Duration.ofMillis(100)).map(i -> "A" + i).take(5),
    Flux.interval(Duration.ofMillis(50), Duration.ofMillis(100)).map(i -> "B" + i).take(5)
); // A0, B0, A1, B1... (interleaved by time)

// CONCAT — sequential (don't start next until current completes):
Flux<String> concat = Flux.concat(fetchPage(1), fetchPage(2), fetchPage(3));

// SWITCH_ON_NEXT / SWITCH_MAP (cancel previous on new emission):
Flux<String> searchResults = searchTerms.switchMap(term ->
    searchService.search(term).subscribeOn(Schedulers.boundedElastic()));
// If user types fast, previous search cancelled → only latest completes

// ERROR HANDLING:
Flux<User> users = repo.findAll()
    .onErrorMap(DataAccessException.class, e -> new ServiceException("DB error", e))
    .onErrorResume(ex -> {
        log.error("Recovering from {}", ex.getMessage());
        return fallbackRepo.findAll();
    })
    .retry(3)                                    // retry up to 3 times
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)).maxBackoff(Duration.ofSeconds(10)));
```

---

**Q129. Java — memory-mapped files and off-heap storage.**
```java
// MEMORY-MAPPED FILES — map file to process virtual memory.
// OS handles paging — only loaded pages in RAM. Zero-copy I/O.
// Used by: databases (RocksDB, LMDB), message queues (Chronicle Queue).

// Write large file:
try (FileChannel fc = FileChannel.open(path, CREATE, READ, WRITE)) {
    long size = 1024L * 1024 * 1024; // 1 GB
    MappedByteBuffer mbb = fc.map(MapMode.READ_WRITE, 0, size);
    // Write directly — OS writes to disk asynchronously
    for (int i = 0; i < 1_000_000; i++) {
        mbb.putLong(i * 8, (long) i);  // position, value
    }
    mbb.force(); // flush to disk (optional — OS does it eventually)
}

// Read mapped file:
try (FileChannel fc = FileChannel.open(path, READ)) {
    MappedByteBuffer mbb = fc.map(MapMode.READ_ONLY, 0, fc.size());
    long value = mbb.getLong(42 * 8); // O(1) random access
}

// OFF-HEAP with ByteBuffer.allocateDirect:
ByteBuffer direct = ByteBuffer.allocateDirect(1024 * 1024); // off-heap
// Avoids GC pressure — freed when buffer GC'd (or explicit with Unsafe.freeMemory)
// Used for: NIO channels (no copy to user space), large caches, Netty buffers

// UNSAFE (internal, discouraged in modern Java):
// sun.misc.Unsafe allows raw memory access, atomic ops without sync.
// Java 9+: use VarHandle instead.
VarHandle vh = MethodHandles.lookup().findVarHandle(MyClass.class, "counter", int.class);
vh.compareAndSet(myObj, 0, 1); // CAS via VarHandle — safe, no Unsafe needed
```

---

**Q130. Java — complete interview preparation checklist.**
```
CORE JAVA:
  ✓ JVM (JDK/JRE/JIT), class loading, GC algorithms
  ✓ Primitives, autoboxing, String pool
  ✓ OOP (encapsulation, inheritance, polymorphism, abstraction)
  ✓ equals/hashCode contract, Comparable/Comparator
  ✓ Generics, type erasure, wildcards, PECS
  ✓ Collections (ArrayList, LinkedList, HashMap, TreeMap, ConcurrentHashMap)
  ✓ Functional interfaces, lambda, method references, Optional
  ✓ Streams (intermediate, terminal, collectors, parallel)
  ✓ Exception handling (checked vs unchecked, try-with-resources)
  ✓ Records, sealed classes, pattern matching (Java 16-21)
  ✓ Modules (JPMS)

CONCURRENCY:
  ✓ Thread lifecycle, Executor framework, ThreadPoolExecutor
  ✓ synchronized, volatile, happens-before, JMM
  ✓ ReentrantLock, ReadWriteLock, StampedLock
  ✓ Atomic classes (AtomicInteger, AtomicReference, LongAdder)
  ✓ ConcurrentHashMap internals
  ✓ CompletableFuture (supplyAsync, thenApply, thenCompose, allOf)
  ✓ CountDownLatch, CyclicBarrier, Semaphore
  ✓ Virtual threads (Java 21, Project Loom)
  ✓ Deadlock detection and prevention
  ✓ ThreadLocal and memory leak prevention

JVM INTERNALS:
  ✓ Heap (Eden, Survivor, Old Gen), Metaspace, Stack
  ✓ GC algorithms (G1, ZGC, Shenandoah)
  ✓ Escape analysis, JIT compilation, tiered compilation
  ✓ Memory leaks (static collections, listeners, ThreadLocal)

SPRING BOOT:
  ✓ @SpringBootApplication, auto-configuration, @Conditional
  ✓ DI (constructor > setter > field), @Autowired, @Qualifier
  ✓ @Transactional (propagation, isolation, self-invocation pitfall)
  ✓ Spring Security (JWT, OAuth2, method-level @PreAuthorize)
  ✓ Spring Data JPA (repositories, N+1, @EntityGraph, specs)
  ✓ Spring AOP (aspects, pointcuts, @Around, @Before, @AfterReturning)
  ✓ Caching (@Cacheable, @CacheEvict, Redis)
  ✓ Spring Events (@EventListener, @TransactionalEventListener)
  ✓ Testing (MockitoExtension, @SpringBootTest, Testcontainers)
  ✓ Actuator, Micrometer, distributed tracing
  ✓ Kafka integration, Outbox pattern
  ✓ WebFlux / reactive (Mono, Flux, WebClient)
  ✓ Virtual threads in Spring Boot 3.2+
```
