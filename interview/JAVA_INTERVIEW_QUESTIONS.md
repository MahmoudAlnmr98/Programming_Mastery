# Java Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Java? Explain its key features.

**Answer:**
Java is a high-level, object-oriented programming language developed by Sun Microsystems (now Oracle). Key features:

- **Platform Independent**: Write once, run anywhere (WORA) via JVM
- **Object-Oriented**: Everything is an object (except primitives)
- **Simple**: Easy to learn, clean syntax
- **Secure**: Built-in security features
- **Robust**: Strong memory management, exception handling
- **Multithreaded**: Built-in support for concurrent programming
- **Architecture Neutral**: Compiled to bytecode, runs on any platform with JVM

### 2. What is the difference between JDK, JRE, and JVM?

**Answer:**
- **JVM (Java Virtual Machine)**: Runtime environment that executes bytecode
- **JRE (Java Runtime Environment**: JVM + libraries needed to run Java applications
- **JDK (Java Development Kit)**: JRE + development tools (compiler, debugger, etc.)

```
JDK = JRE + Development Tools
JRE = JVM + Libraries
```

### 3. Explain the difference between `==` and `.equals()` in Java.

**Answer:**
- **`==`**: Compares references (memory addresses) for objects, values for primitives
- **`.equals()`**: Compares the actual content/value of objects

```java
String str1 = new String("Hello");
String str2 = new String("Hello");
String str3 = str1;

System.out.println(str1 == str2);        // false (different references)
System.out.println(str1.equals(str2));   // true (same content)
System.out.println(str1 == str3);       // true (same reference)

// For primitives
int a = 5;
int b = 5;
System.out.println(a == b);  // true
```

### 4. What are the access modifiers in Java?

**Answer:**
- **public**: Accessible from anywhere
- **private**: Accessible only within the same class
- **protected**: Accessible within same package and subclasses
- **default (package-private)**: Accessible within same package only

```java
public class Example {
    public int publicVar;        // Accessible everywhere
    private int privateVar;       // Only in this class
    protected int protectedVar;   // Same package + subclasses
    int packageVar;              // Same package only
}
```

### 5. Explain the difference between `String`, `StringBuilder`, and `StringBuffer`.

**Answer:**
- **String**: Immutable, thread-safe, creates new object on modification
- **StringBuilder**: Mutable, not thread-safe, faster than StringBuffer
- **StringBuffer**: Mutable, thread-safe (synchronized), slower than StringBuilder

```java
// String - creates new objects
String str = "Hello";
str += " World";  // Creates new String object

// StringBuilder - modifies existing object
StringBuilder sb = new StringBuilder("Hello");
sb.append(" World");  // Modifies existing object

// StringBuffer - thread-safe version
StringBuffer sbf = new StringBuffer("Hello");
sbf.append(" World");  // Thread-safe modification
```

### 6. What is the difference between checked and unchecked exceptions?

**Answer:**
- **Checked Exceptions**: Must be handled or declared (compile-time)
  - Examples: `IOException`, `SQLException`, `ClassNotFoundException`
  - Extend `Exception` (but not `RuntimeException`)
  
- **Unchecked Exceptions**: Don't need to be handled (runtime)
  - Examples: `NullPointerException`, `ArrayIndexOutOfBoundsException`
  - Extend `RuntimeException`

```java
// Checked exception - must handle
try {
    FileReader file = new FileReader("file.txt");
} catch (IOException e) {
    e.printStackTrace();
}

// Unchecked exception - optional to handle
int[] arr = new int[5];
int value = arr[10];  // ArrayIndexOutOfBoundsException (unchecked)
```

### 7. What is method overloading and overriding?

**Answer:**
- **Overloading**: Same method name, different parameters (compile-time polymorphism)
- **Overriding**: Subclass provides specific implementation of parent method (runtime polymorphism)

```java
// Overloading
class Calculator {
    int add(int a, int b) {
        return a + b;
    }
    
    double add(double a, double b) {
        return a + b;
    }
    
    int add(int a, int b, int c) {
        return a + b + c;
    }
}

// Overriding
class Animal {
    void makeSound() {
        System.out.println("Animal makes sound");
    }
}

class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("Dog barks");
    }
}
```

### 8. What is the `final` keyword used for?

**Answer:**
- **final variable**: Cannot be reassigned (constant)
- **final method**: Cannot be overridden
- **final class**: Cannot be extended

```java
final int MAX_SIZE = 100;  // Constant

class Parent {
    final void method() {  // Cannot be overridden
        // code
    }
}

final class Immutable {  // Cannot be extended
    // code
}
```

---

## Intermediate Level

### 9. Explain the difference between `ArrayList` and `LinkedList`.

**Answer:**
- **ArrayList**: Dynamic array, random access O(1), insertion/deletion O(n)
- **LinkedList**: Doubly linked list, random access O(n), insertion/deletion O(1)

```java
// ArrayList - better for random access
ArrayList<String> arrayList = new ArrayList<>();
arrayList.get(0);  // O(1)
arrayList.add(0, "item");  // O(n) - shifts elements

// LinkedList - better for frequent insertions/deletions
LinkedList<String> linkedList = new LinkedList<>();
linkedList.get(0);  // O(n) - must traverse
linkedList.addFirst("item");  // O(1)
linkedList.removeFirst();  // O(1)
```

**When to use:**
- **ArrayList**: Frequent reads, random access needed
- **LinkedList**: Frequent insertions/deletions, especially at ends

### 10. What is the difference between `HashMap` and `Hashtable`?

**Answer:**
- **HashMap**: Not synchronized, allows null keys/values, faster
- **Hashtable**: Synchronized (thread-safe), doesn't allow null, slower

```java
// HashMap - not thread-safe
HashMap<String, Integer> map = new HashMap<>();
map.put(null, 1);  // Allowed
map.put("key", null);  // Allowed

// Hashtable - thread-safe
Hashtable<String, Integer> table = new Hashtable<>();
table.put(null, 1);  // NullPointerException
table.put("key", null);  // NullPointerException
```

**Note**: For thread-safe HashMap, use `ConcurrentHashMap`.

### 11. Explain Java's memory model and garbage collection.

**Answer:**
**Memory Areas:**
- **Heap**: Objects stored here, divided into Young and Old generations
- **Stack**: Method calls, local variables, references
- **Method Area**: Class metadata, static variables
- **PC Register**: Current instruction pointer
- **Native Method Stack**: Native method calls

**Garbage Collection:**
- **Young Generation**: New objects, collected frequently (Minor GC)
  - Eden space: New objects
  - Survivor spaces (S0, S1): Surviving objects
- **Old Generation**: Long-lived objects (Major GC)
- **Permanent Generation**: Class metadata (removed in Java 8, replaced by Metaspace)

**GC Algorithms:**
- **Serial GC**: Single thread, for small applications
- **Parallel GC**: Multiple threads, default for server apps
- **G1 GC**: Low latency, divides heap into regions
- **ZGC**: Ultra-low latency, handles large heaps

### 12. What is the difference between `synchronized` and `volatile`?

**Answer:**
- **synchronized**: Provides mutual exclusion, ensures atomicity and visibility
- **volatile**: Ensures visibility only, doesn't provide atomicity

```java
// synchronized - mutual exclusion
class Counter {
    private int count = 0;
    
    public synchronized void increment() {
        count++;  // Atomic operation
    }
    
    public synchronized int getCount() {
        return count;  // Always sees latest value
    }
}

// volatile - visibility only
class Shared {
    private volatile boolean flag = false;
    
    public void setFlag() {
        flag = true;  // Visible to all threads immediately
    }
    
    public boolean getFlag() {
        return flag;  // Always reads from main memory
    }
}
```

**Key Differences:**
- `synchronized` provides both visibility and atomicity
- `volatile` provides only visibility
- `synchronized` can be used on methods/blocks
- `volatile` can only be used on variables

### 13. Explain the `equals()` and `hashCode()` contract.

**Answer:**
**Contract:**
1. If two objects are equal (`equals()` returns true), they must have the same `hashCode()`
2. If two objects have the same `hashCode()`, they may or may not be equal
3. `hashCode()` should be consistent (same value for same object)

```java
class Person {
    private String name;
    private int age;
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && Objects.equals(name, person.name);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

**Why important:**
- Used by `HashMap`, `HashSet` for efficient lookups
- Violating contract causes incorrect behavior in collections

### 14. What are Java 8 features? Explain Streams and Lambda expressions.

**Answer:**
**Key Java 8 Features:**
- Lambda expressions
- Stream API
- Optional
- Default methods in interfaces
- Method references
- Date/Time API

**Lambda Expressions:**
```java
// Before Java 8
List<String> names = Arrays.asList("John", "Jane", "Bob");
Collections.sort(names, new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.compareTo(b);
    }
});

// Java 8 - Lambda
Collections.sort(names, (a, b) -> a.compareTo(b));
// Or method reference
Collections.sort(names, String::compareTo);
```

**Stream API:**
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Filter and map
List<Integer> squares = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList());

// Reduce
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Parallel stream
int sum = numbers.parallelStream()
    .mapToInt(Integer::intValue)
    .sum();
```

### 15. Explain the difference between `Comparable` and `Comparator`.

**Answer:**
- **Comparable**: Natural ordering, implemented by the class itself
- **Comparator**: External ordering, separate class

```java
// Comparable - natural ordering
class Person implements Comparable<Person> {
    private String name;
    private int age;
    
    @Override
    public int compareTo(Person other) {
        return this.name.compareTo(other.name);
    }
}

// Usage
Collections.sort(people);  // Uses compareTo

// Comparator - external ordering
Comparator<Person> ageComparator = new Comparator<Person>() {
    @Override
    public int compare(Person p1, Person p2) {
        return Integer.compare(p1.getAge(), p2.getAge());
    }
};

// Usage
Collections.sort(people, ageComparator);

// Java 8 - Lambda
Collections.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
```

### 16. What is the difference between `wait()`, `notify()`, and `notifyAll()`?

**Answer:**
- **wait()**: Releases lock and waits until notified
- **notify()**: Wakes up one waiting thread
- **notifyAll()**: Wakes up all waiting threads

```java
class SharedResource {
    private boolean available = false;
    
    public synchronized void produce() throws InterruptedException {
        while (available) {
            wait();  // Wait if already produced
        }
        available = true;
        System.out.println("Produced");
        notify();  // Notify consumer
    }
    
    public synchronized void consume() throws InterruptedException {
        while (!available) {
            wait();  // Wait if not available
        }
        available = false;
        System.out.println("Consumed");
        notify();  // Notify producer
    }
}
```

**Key Points:**
- Must be called from synchronized block
- `wait()` releases the lock
- `notify()` doesn't release lock immediately
- Use `notifyAll()` when multiple threads waiting

---

## Advanced Level

### 17. Explain Java's reflection API with examples.

**Answer:**
Reflection allows inspection and modification of classes, methods, fields at runtime.

```java
import java.lang.reflect.*;

class ReflectionExample {
    public static void main(String[] args) throws Exception {
        // Get Class object
        Class<?> clazz = Class.forName("com.example.MyClass");
        
        // Create instance
        Object instance = clazz.getDeclaredConstructor().newInstance();
        
        // Get methods
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println(method.getName());
        }
        
        // Invoke method
        Method method = clazz.getDeclaredMethod("methodName", String.class);
        method.setAccessible(true);
        Object result = method.invoke(instance, "argument");
        
        // Get fields
        Field field = clazz.getDeclaredField("fieldName");
        field.setAccessible(true);
        field.set(instance, "value");
        Object value = field.get(instance);
        
        // Get constructors
        Constructor<?>[] constructors = clazz.getDeclaredConstructors();
    }
}
```

**Use Cases:**
- Frameworks (Spring, Hibernate)
- Testing frameworks (JUnit)
- Serialization/Deserialization
- Debugging tools

### 18. Explain the Java Memory Model and happens-before relationship.

**Answer:**
**Java Memory Model (JMM):**
Defines how threads interact through memory, ensuring visibility and ordering.

**Happens-Before Relationship:**
Establishes ordering between operations:
1. **Program Order**: Operations in same thread
2. **Monitor Lock**: Unlock happens-before subsequent lock
3. **Volatile**: Write happens-before subsequent read
4. **Thread Start**: `start()` happens-before thread's actions
5. **Thread Join**: Thread's actions happen-before `join()` returns
6. **Transitivity**: If A happens-before B, and B happens-before C, then A happens-before C

```java
class MemoryModelExample {
    private int x = 0;
    private volatile boolean flag = false;
    
    // Thread 1
    public void writer() {
        x = 42;           // 1
        flag = true;       // 2 - volatile write
    }
    
    // Thread 2
    public void reader() {
        if (flag) {        // 3 - volatile read
            int r = x;     // 4 - guaranteed to see x = 42
        }
    }
}
```

### 19. Explain different types of class loaders in Java.

**Answer:**
**Class Loader Hierarchy:**
1. **Bootstrap Class Loader**: Loads core Java classes (rt.jar)
2. **Extension Class Loader**: Loads extension classes
3. **Application Class Loader**: Loads application classes (classpath)

**Custom Class Loader:**
```java
class CustomClassLoader extends ClassLoader {
    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = loadClassData(name);
        return defineClass(name, classData, 0, classData.length);
    }
    
    private byte[] loadClassData(String className) {
        // Load class bytes from custom location
        // Return byte array
    }
}
```

**Delegation Model:**
- Class loader first delegates to parent
- Only loads if parent can't find class

### 20. Explain the difference between `ConcurrentHashMap` and `HashMap`.

**Answer:**
- **HashMap**: Not thread-safe, allows null keys/values
- **ConcurrentHashMap**: Thread-safe, doesn't allow null, uses segment locking

```java
// HashMap - not thread-safe
HashMap<String, Integer> map = new HashMap<>();
// Concurrent modification exception in multi-threaded environment

// ConcurrentHashMap - thread-safe
ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
// Safe for concurrent access

// Java 8 improvements
concurrentMap.computeIfAbsent("key", k -> computeValue(k));
concurrentMap.forEach((k, v) -> System.out.println(k + "=" + v));
```

**Internal Implementation:**
- **Java 7**: Segment-based locking (16 segments)
- **Java 8**: Node-based locking, uses CAS operations
- Better performance than `Hashtable` (fine-grained locking)

### 21. Explain the Producer-Consumer problem and solution.

**Answer:**
**Problem**: Producer produces items, consumer consumes. Need synchronization.

**Solution using wait/notify:**
```java
import java.util.LinkedList;
import java.util.Queue;

class ProducerConsumer {
    private Queue<Integer> queue = new LinkedList<>();
    private int capacity = 10;
    
    public synchronized void produce() throws InterruptedException {
        while (queue.size() == capacity) {
            wait();  // Wait if queue is full
        }
        int item = (int) (Math.random() * 100);
        queue.offer(item);
        System.out.println("Produced: " + item);
        notify();  // Notify consumer
    }
    
    public synchronized void consume() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();  // Wait if queue is empty
        }
        int item = queue.poll();
        System.out.println("Consumed: " + item);
        notify();  // Notify producer
    }
}
```

**Solution using BlockingQueue:**
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);

// Producer
queue.put(item);  // Blocks if full

// Consumer
int item = queue.take();  // Blocks if empty
```

### 22. Explain Java's Fork/Join framework.

**Answer:**
Framework for parallel execution of tasks that can be recursively split.

```java
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

class SumTask extends RecursiveTask<Long> {
    private int[] array;
    private int start, end;
    private static final int THRESHOLD = 1000;
    
    public SumTask(int[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end = end;
    }
    
    @Override
    protected Long compute() {
        int length = end - start;
        if (length <= THRESHOLD) {
            // Base case: compute directly
            long sum = 0;
            for (int i = start; i < end; i++) {
                sum += array[i];
            }
            return sum;
        } else {
            // Split task
            int mid = start + length / 2;
            SumTask left = new SumTask(array, start, mid);
            SumTask right = new SumTask(array, mid, end);
            left.fork();  // Execute asynchronously
            long rightResult = right.compute();  // Compute directly
            long leftResult = left.join();  // Wait for result
            return leftResult + rightResult;
        }
    }
}

// Usage
ForkJoinPool pool = new ForkJoinPool();
SumTask task = new SumTask(array, 0, array.length);
long result = pool.invoke(task);
```

### 23. Explain the difference between `ExecutorService`, `ForkJoinPool`, and `ThreadPoolExecutor`.

**Answer:**
- **ExecutorService**: Interface for executing tasks asynchronously
- **ForkJoinPool**: Specialized for fork/join tasks, work-stealing algorithm
- **ThreadPoolExecutor**: Implementation of ExecutorService, configurable thread pool

```java
// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<String> future = executor.submit(() -> "Result");
String result = future.get();
executor.shutdown();

// ForkJoinPool - for recursive tasks
ForkJoinPool forkJoinPool = new ForkJoinPool();
RecursiveTask<Long> task = new MyRecursiveTask();
Long result = forkJoinPool.invoke(task);

// ThreadPoolExecutor - more control
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5,  // core pool size
    10, // maximum pool size
    60L, TimeUnit.SECONDS, // keep-alive time
    new LinkedBlockingQueue<>() // work queue
);
```

### 24. Explain Java's annotation processing and custom annotations.

**Answer:**
**Custom Annotation:**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyAnnotation {
    String value() default "";
    int count() default 0;
}
```

**Using Annotation:**
```java
class MyClass {
    @MyAnnotation(value = "test", count = 5)
    public void myMethod() {
        // code
    }
}
```

**Processing Annotation:**
```java
Method method = MyClass.class.getDeclaredMethod("myMethod");
MyAnnotation annotation = method.getAnnotation(MyAnnotation.class);
if (annotation != null) {
    String value = annotation.value();
    int count = annotation.count();
}
```

**Annotation Processors:**
- Compile-time processing
- Generate code, validate code
- Used by frameworks (Lombok, Dagger)

### 25. Explain JVM tuning and performance optimization.

**Answer:**
**Heap Size:**
```bash
-Xms512m  # Initial heap size
-Xmx2g    # Maximum heap size
```

**GC Selection:**
```bash
-XX:+UseG1GC           # Use G1 garbage collector
-XX:+UseParallelGC     # Use parallel GC
-XX:+UseConcMarkSweepGC # Use CMS GC (deprecated)
```

**GC Tuning:**
```bash
-XX:NewRatio=2         # Ratio of old to young generation
-XX:SurvivorRatio=8     # Ratio of eden to survivor spaces
-XX:MaxGCPauseMillis=200 # Target max GC pause time
```

**Monitoring:**
```bash
-XX:+PrintGCDetails    # Print GC details
-XX:+HeapDumpOnOutOfMemoryError # Create heap dump on OOM
```

**Best Practices:**
- Set initial and max heap same to avoid resizing
- Use appropriate GC for workload
- Monitor GC logs
- Tune based on application behavior

### 26. Explain Java 9+ features (Modules, Records, Pattern Matching).

**Answer:**
**Java 9 - Modules:**
```java
// module-info.java
module com.example.app {
    requires java.base;
    requires java.sql;
    exports com.example.api;
}
```

**Java 14 - Records:**
```java
public record Person(String name, int age) {
    // Automatically generates:
    // - Constructor
    // - Getters
    // - equals(), hashCode(), toString()
}

// Usage
Person person = new Person("John", 30);
System.out.println(person.name()); // John
```

**Java 14 - Pattern Matching (Preview):**
```java
// instanceof pattern matching
if (obj instanceof String str) {
    System.out.println(str.length()); // str is available
}

// Switch expressions
int result = switch (value) {
    case 1 -> 10;
    case 2 -> 20;
    default -> 0;
};
```

### 27. Explain CompletableFuture in detail.

**Answer:**
CompletableFuture provides asynchronous programming.

```java
// Create
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Result";
});

// Chain operations
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenApply(String::toUpperCase);

// Combine futures
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<String> combined = future1.thenCombine(future2, (a, b) -> a + " " + b);

// Handle errors
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> {
        if (true) throw new RuntimeException("Error");
        return "Success";
    })
    .exceptionally(ex -> "Error: " + ex.getMessage());
```

### 28. Explain Java's Optional class best practices.

**Answer:**
Optional represents value that may or may not be present.

```java
// Create
Optional<String> empty = Optional.empty();
Optional<String> of = Optional.of("value"); // Non-null
Optional<String> nullable = Optional.ofNullable(null); // Can be null

// Usage
Optional<String> name = Optional.of("John");
name.ifPresent(System.out::println); // Prints if present
String value = name.orElse("Default"); // Default if empty
String value2 = name.orElseGet(() -> "Default"); // Lazy default

// Map and filter
Optional<String> upper = name.map(String::toUpperCase);
Optional<String> filtered = name.filter(s -> s.length() > 5);
```

**Best Practices:**
- Don't use for method parameters
- Don't use for class fields
- Use for return types
- Avoid Optional.get() without checking

### 29. Explain Java's Stream API advanced operations.

**Answer:**
**Collectors:**
```java
// Grouping
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity));

// Partitioning
Map<Boolean, List<Person>> partitioned = people.stream()
    .collect(Collectors.partitioningBy(p -> p.getAge() > 18));

// Joining
String names = people.stream()
    .map(Person::getName)
    .collect(Collectors.joining(", "));

// Summarizing
IntSummaryStatistics stats = numbers.stream()
    .collect(Collectors.summarizingInt(Integer::intValue));
```

**Custom Collectors:**
```java
Collector<Person, ?, List<String>> customCollector = Collector.of(
    ArrayList::new,
    (list, person) -> list.add(person.getName()),
    (list1, list2) -> {
        list1.addAll(list2);
        return list1;
    },
    Collector.Characteristics.IDENTITY_FINISH
);
```

### 30. Explain Java's new Date/Time API (java.time).

**Answer:**
**LocalDate, LocalTime, LocalDateTime:**
```java
LocalDate date = LocalDate.now();
LocalDate specificDate = LocalDate.of(2024, 1, 15);
LocalDate parsed = LocalDate.parse("2024-01-15");

LocalTime time = LocalTime.now();
LocalTime specificTime = LocalTime.of(14, 30);

LocalDateTime dateTime = LocalDateTime.now();
```

**ZonedDateTime:**
```java
ZonedDateTime zoned = ZonedDateTime.now(ZoneId.of("America/New_York"));
ZonedDateTime utc = ZonedDateTime.now(ZoneId.of("UTC"));
```

**Duration and Period:**
```java
Duration duration = Duration.between(start, end);
Period period = Period.between(startDate, endDate);
```

**Formatting:**
```java
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = dateTime.format(formatter);
LocalDateTime parsed = LocalDateTime.parse("2024-01-15 10:30:00", formatter);
```

### 31. Explain Spring MVC architecture.

**Answer:**
Spring MVC is a web framework implementing Model-View-Controller pattern.

**Components:**
1. **DispatcherServlet**: Front controller, routes requests
2. **HandlerMapping**: Maps URLs to controllers
3. **Controller**: Handles requests, returns model/view
4. **ViewResolver**: Resolves view names to actual views
5. **Model**: Data passed to view

**Flow:**
```
Request → DispatcherServlet → HandlerMapping → Controller
                                                      ↓
Response ← ViewResolver ← View ← Model ← Controller
```

**Example:**
```java
@Controller
@RequestMapping("/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public String getUser(@PathVariable Long id, Model model) {
        User user = userService.findById(id);
        model.addAttribute("user", user);
        return "user-detail"; // View name
    }
    
    @PostMapping
    @ResponseBody
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.save(user);
        return ResponseEntity.ok(created);
    }
}
```

**Configuration:**
```java
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        registry.jsp("/WEB-INF/views/", ".jsp");
    }
}
```

### 32. Explain Spring Bean lifecycle and scopes.

**Answer:**
**Bean Lifecycle:**
1. Instantiation
2. Populate properties
3. BeanNameAware.setBeanName()
4. BeanFactoryAware.setBeanFactory()
5. ApplicationContextAware.setApplicationContext()
6. @PostConstruct
7. InitializingBean.afterPropertiesSet()
8. Custom init method
9. Bean ready
10. @PreDestroy
11. DisposableBean.destroy()
12. Custom destroy method

**Bean Scopes:**
- **singleton**: One instance per container (default)
- **prototype**: New instance each time
- **request**: One per HTTP request (web)
- **session**: One per HTTP session (web)
- **application**: One per ServletContext (web)

```java
@Component
@Scope("prototype")
public class PrototypeBean {
    // New instance each time
}

@Component
@Scope("request")
public class RequestBean {
    // One per HTTP request
}
```

### 33. Explain Inner Beans in Spring.

**Answer:**
Inner beans are beans defined within another bean's definition.

**XML Configuration:**
```xml
<bean id="outerBean" class="com.example.OuterBean">
    <property name="innerBean">
        <bean class="com.example.InnerBean">
            <property name="name" value="Inner"/>
        </bean>
    </property>
</bean>
```

**Java Configuration:**
```java
@Configuration
public class AppConfig {
    
    @Bean
    public OuterBean outerBean() {
        OuterBean outer = new OuterBean();
        outer.setInnerBean(innerBean()); // Inner bean
        return outer;
    }
    
    @Bean
    public InnerBean innerBean() {
        return new InnerBean("Inner");
    }
}
```

**Characteristics:**
- No ID/name (anonymous)
- Cannot be accessed outside parent bean
- Cannot be injected elsewhere
- Useful for one-time use

### 34. Explain the volatile keyword in detail.

**Answer:**
`volatile` ensures visibility of variable changes across threads.

**Without volatile:**
```java
class Shared {
    private boolean flag = false; // May be cached
    
    public void setFlag() {
        flag = true; // May not be visible to other threads
    }
    
    public boolean getFlag() {
        return flag; // May read stale value
    }
}
```

**With volatile:**
```java
class Shared {
    private volatile boolean flag = false; // Always reads from main memory
    
    public void setFlag() {
        flag = true; // Immediately visible to all threads
    }
    
    public boolean getFlag() {
        return flag; // Always reads from main memory
    }
}
```

**Properties:**
- **Visibility**: Changes visible to all threads
- **No Atomicity**: Not atomic for compound operations
- **No Ordering**: Doesn't provide ordering guarantees

**Use Cases:**
- Status flags
- Shutdown signals
- Single-writer scenarios

**Limitations:**
```java
// NOT atomic - needs synchronization
private volatile int count = 0;

public void increment() {
    count++; // Read-modify-write (not atomic)
}

// Solution: Use AtomicInteger
private AtomicInteger count = new AtomicInteger(0);

public void increment() {
    count.incrementAndGet(); // Atomic
}
```

### 35. Explain the difference between abstract class and interface in Java.

**Answer:**
**Abstract Class:**
- Can have instance variables
- Can have constructors
- Can have concrete methods
- Can have abstract methods
- Single inheritance
- Can have any access modifier

**Interface:**
- Only constants (public static final)
- No constructors
- Can have default methods (Java 8+)
- Can have static methods (Java 8+)
- Can have private methods (Java 9+)
- Multiple inheritance
- All methods public (unless private)

```java
// Abstract class
abstract class Animal {
    protected String name; // Instance variable
    
    public Animal(String name) { // Constructor
        this.name = name;
    }
    
    public void eat() { // Concrete method
        System.out.println(name + " is eating");
    }
    
    abstract void makeSound(); // Abstract method
}

// Interface
interface Flyable {
    int MAX_HEIGHT = 1000; // Constant
    
    void fly(); // Abstract method
    
    default void land() { // Default method (Java 8+)
        System.out.println("Landing");
    }
    
    static void info() { // Static method (Java 8+)
        System.out.println("Flying interface");
    }
}
```

**When to use:**
- **Abstract Class**: Share code, common state
- **Interface**: Define contract, multiple inheritance

### 36. Explain Java's Collections Framework hierarchy.

**Answer:**
**Collection Interface Hierarchy:**
```
Collection
├── List
│   ├── ArrayList
│   ├── LinkedList
│   └── Vector
├── Set
│   ├── HashSet
│   ├── LinkedHashSet
│   └── TreeSet
└── Queue
    ├── PriorityQueue
    └── Deque
        └── ArrayDeque
```

**Map Interface:**
```
Map
├── HashMap
├── LinkedHashMap
├── TreeMap
└── Hashtable
```

**Key Differences:**
- **List**: Ordered, allows duplicates
- **Set**: No duplicates
- **Queue**: FIFO order
- **Map**: Key-value pairs

### 37. Explain the difference between `ArrayList` and `Vector`.

**Answer:**
- **ArrayList**: Not synchronized, faster, not thread-safe
- **Vector**: Synchronized, slower, thread-safe

```java
// ArrayList - not thread-safe
ArrayList<String> list = new ArrayList<>();
list.add("item");

// Vector - thread-safe (synchronized)
Vector<String> vector = new Vector<>();
vector.add("item");

// For thread-safe ArrayList, use Collections.synchronizedList()
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
```

**Note**: `Vector` is legacy, prefer `ArrayList` with `Collections.synchronizedList()` if needed.

### 38. Explain the difference between `HashSet`, `LinkedHashSet`, and `TreeSet`.

**Answer:**
**HashSet:**
```java
HashSet<String> set = new HashSet<>();
set.add("c");
set.add("a");
set.add("b");
// Order: Not guaranteed (may be: a, b, c or c, a, b)
```

**LinkedHashSet:**
```java
LinkedHashSet<String> set = new LinkedHashSet<>();
set.add("c");
set.add("a");
set.add("b");
// Order: Insertion order (c, a, b)
```

**TreeSet:**
```java
TreeSet<String> set = new TreeSet<>();
set.add("c");
set.add("a");
set.add("b");
// Order: Sorted order (a, b, c)
```

**Performance:**
- **HashSet**: O(1) average, O(n) worst
- **LinkedHashSet**: O(1) average, maintains order
- **TreeSet**: O(log n), sorted order

### 39. Explain the difference between `HashMap`, `LinkedHashMap`, and `TreeMap`.

**Answer:**
**HashMap:**
```java
HashMap<String, Integer> map = new HashMap<>();
map.put("c", 3);
map.put("a", 1);
map.put("b", 2);
// Order: Not guaranteed
```

**LinkedHashMap:**
```java
LinkedHashMap<String, Integer> map = new LinkedHashMap<>();
map.put("c", 3);
map.put("a", 1);
map.put("b", 2);
// Order: Insertion order (c, a, b)
```

**TreeMap:**
```java
TreeMap<String, Integer> map = new TreeMap<>();
map.put("c", 3);
map.put("a", 1);
map.put("b", 2);
// Order: Sorted by key (a, b, c)
```

**Performance:**
- **HashMap**: O(1) average
- **LinkedHashMap**: O(1) average, maintains order
- **TreeMap**: O(log n), sorted by key

### 40. Explain Java's `Optional` class in detail.

**Answer:**
Optional represents value that may or may not be present.

```java
// Create Optional
Optional<String> empty = Optional.empty();
Optional<String> of = Optional.of("value"); // Non-null
Optional<String> nullable = Optional.ofNullable(null); // Can be null

// Check and get
if (optional.isPresent()) {
    String value = optional.get();
}

// Or else
String value = optional.orElse("default");
String value2 = optional.orElseGet(() -> "default"); // Lazy
String value3 = optional.orElseThrow(() -> new RuntimeException()); // Throw if empty

// Map and filter
Optional<String> upper = optional.map(String::toUpperCase);
Optional<String> filtered = optional.filter(s -> s.length() > 5);

// FlatMap
Optional<String> flatMapped = optional.flatMap(s -> Optional.of(s.toUpperCase()));
```

**Best Practices:**
- Don't use for method parameters
- Don't use for class fields
- Use for return types
- Avoid `Optional.get()` without checking

### 41. Explain Java's `Stream` API terminal operations.

**Answer:**
**Collect:**
```java
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
Map<String, Integer> map = stream.collect(
    Collectors.toMap(s -> s, String::length)
);
```

**Reduce:**
```java
Optional<Integer> sum = stream.reduce(Integer::sum);
Integer sum2 = stream.reduce(0, Integer::sum);
```

**ForEach:**
```java
stream.forEach(System.out::println);
```

**Match:**
```java
boolean anyMatch = stream.anyMatch(s -> s.length() > 5);
boolean allMatch = stream.allMatch(s -> s.length() > 5);
boolean noneMatch = stream.noneMatch(s -> s.length() > 5);
```

**Find:**
```java
Optional<String> first = stream.findFirst();
Optional<String> any = stream.findAny();
```

**Count:**
```java
long count = stream.count();
```

### 42. Explain Java's `Stream` API intermediate operations.

**Answer:**
**Filter:**
```java
Stream<String> filtered = stream.filter(s -> s.length() > 5);
```

**Map:**
```java
Stream<Integer> lengths = stream.map(String::length);
```

**FlatMap:**
```java
Stream<String> flatMapped = stream.flatMap(s -> 
    Stream.of(s.split(" "))
);
```

**Distinct:**
```java
Stream<String> distinct = stream.distinct();
```

**Sorted:**
```java
Stream<String> sorted = stream.sorted();
Stream<String> sorted2 = stream.sorted(Comparator.reverseOrder());
```

**Limit and Skip:**
```java
Stream<String> limited = stream.limit(10);
Stream<String> skipped = stream.skip(5);
```

**Peek:**
```java
Stream<String> peeked = stream.peek(System.out::println);
```

### 43. Explain Java's `Collectors` utility class.

**Answer:**
**Basic Collectors:**
```java
// To list
List<String> list = stream.collect(Collectors.toList());

// To set
Set<String> set = stream.collect(Collectors.toSet());

// To map
Map<String, Integer> map = stream.collect(
    Collectors.toMap(s -> s, String::length)
);

// Joining
String joined = stream.collect(Collectors.joining(", "));
```

**Grouping:**
```java
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity));

Map<String, Long> countByCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity, Collectors.counting()));
```

**Partitioning:**
```java
Map<Boolean, List<Person>> partitioned = people.stream()
    .collect(Collectors.partitioningBy(p -> p.getAge() > 18));
```

**Summarizing:**
```java
IntSummaryStatistics stats = numbers.stream()
    .collect(Collectors.summarizingInt(Integer::intValue));
```

### 44. Explain Java's `CompletableFuture` in detail.

**Answer:**
CompletableFuture provides asynchronous programming.

```java
// Create
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Result";
});

// Chain operations
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenApply(String::toUpperCase);

// Combine futures
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");

CompletableFuture<String> combined = future1.thenCombine(
    future2, (a, b) -> a + " " + b
);

// Handle errors
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> {
        if (true) throw new RuntimeException("Error");
        return "Success";
    })
    .exceptionally(ex -> "Error: " + ex.getMessage());

// All of
CompletableFuture<Void> all = CompletableFuture.allOf(future1, future2);
```

### 45. Explain Java's `ExecutorService` and thread pools.

**Answer:**
**ExecutorService:**
```java
ExecutorService executor = Executors.newFixedThreadPool(10);
Future<String> future = executor.submit(() -> "Result");
String result = future.get();
executor.shutdown();
```

**Thread Pool Types:**
```java
// Fixed thread pool
ExecutorService fixed = Executors.newFixedThreadPool(10);

// Cached thread pool
ExecutorService cached = Executors.newCachedThreadPool();

// Single thread executor
ExecutorService single = Executors.newSingleThreadExecutor();

// Scheduled executor
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(5);
scheduled.schedule(() -> System.out.println("Task"), 5, TimeUnit.SECONDS);
```

**Custom Thread Pool:**
```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5,  // core pool size
    10, // maximum pool size
    60L, TimeUnit.SECONDS, // keep-alive time
    new LinkedBlockingQueue<>() // work queue
);
```

### 46. Explain Java's `Atomic` classes.

**Answer:**
Atomic classes provide thread-safe operations without synchronization.

```java
// AtomicInteger
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet(); // Atomic increment
count.getAndIncrement(); // Get then increment
count.addAndGet(5); // Add and get

// AtomicLong
AtomicLong longValue = new AtomicLong(0L);

// AtomicReference
AtomicReference<String> ref = new AtomicReference<>("initial");
ref.compareAndSet("initial", "updated"); // CAS operation

// AtomicBoolean
AtomicBoolean flag = new AtomicBoolean(false);
flag.compareAndSet(false, true);
```

**Benefits:**
- No synchronization needed
- Better performance than synchronized
- Lock-free operations

### 47. Explain Java's `CountDownLatch` and `CyclicBarrier`.

**Answer:**
**CountDownLatch:**
```java
CountDownLatch latch = new CountDownLatch(3);

// Thread 1
new Thread(() -> {
    // Do work
    latch.countDown();
}).start();

// Thread 2
new Thread(() -> {
    // Do work
    latch.countDown();
}).start();

// Thread 3
new Thread(() -> {
    // Do work
    latch.countDown();
}).start();

// Main thread waits
latch.await(); // Waits until count reaches 0
```

**CyclicBarrier:**
```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});

// Threads
for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        // Do work
        try {
            barrier.await(); // Wait for all threads
        } catch (Exception e) {}
    }).start();
}
```

**Differences:**
- **CountDownLatch**: One-time use, countdown
- **CyclicBarrier**: Reusable, all threads wait

### 48. Explain Java's `Semaphore`.

**Answer:**
Semaphore controls access to resource pool.

```java
Semaphore semaphore = new Semaphore(3); // 3 permits

// Acquire permit
semaphore.acquire();
try {
    // Access resource
} finally {
    semaphore.release(); // Release permit
}

// Try acquire (non-blocking)
if (semaphore.tryAcquire()) {
    try {
        // Access resource
    } finally {
        semaphore.release();
    }
}
```

**Use Cases:**
- Connection pooling
- Rate limiting
- Resource access control

### 49. Explain Java's `BlockingQueue` implementations.

**Answer:**
**ArrayBlockingQueue:**
```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
queue.put("item"); // Blocks if full
String item = queue.take(); // Blocks if empty
```

**LinkedBlockingQueue:**
```java
BlockingQueue<String> queue = new LinkedBlockingQueue<>();
queue.put("item");
String item = queue.take();
```

**PriorityBlockingQueue:**
```java
BlockingQueue<String> queue = new PriorityBlockingQueue<>();
queue.put("c");
queue.put("a");
queue.put("b");
String item = queue.take(); // "a" (sorted)
```

**SynchronousQueue:**
```java
BlockingQueue<String> queue = new SynchronousQueue<>();
// Each put must wait for take, and vice versa
```

### 50. Explain Java's `CopyOnWriteArrayList` and `CopyOnWriteArraySet`.

**Answer:**
**CopyOnWriteArrayList:**
```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("item");

// Thread-safe for reads
for (String item : list) {
    // Safe iteration (snapshot)
}

// Writes create new copy
list.add("new item"); // Creates new array
```

**CopyOnWriteArraySet:**
```java
CopyOnWriteArraySet<String> set = new CopyOnWriteArraySet<>();
set.add("item");
```

**Characteristics:**
- Thread-safe
- Expensive writes (copy entire array)
- Fast reads
- No locking for reads
- Best for read-heavy workloads

### 51. Explain Java's `ReentrantLock` vs `synchronized`.

**Answer:**
**synchronized:**
```java
public synchronized void method() {
    // Synchronized block
}

synchronized (obj) {
    // Synchronized block
}
```

**ReentrantLock:**
```java
ReentrantLock lock = new ReentrantLock();

public void method() {
    lock.lock();
    try {
        // Critical section
    } finally {
        lock.unlock();
    }
}
```

**Differences:**
- **ReentrantLock**: More flexible, tryLock, fair locking
- **synchronized**: Simpler, automatic unlock

**ReentrantLock Features:**
```java
ReentrantLock lock = new ReentrantLock(true); // Fair lock

// Try lock
if (lock.tryLock()) {
    try {
        // Critical section
    } finally {
        lock.unlock();
    }
}

// Try lock with timeout
if (lock.tryLock(5, TimeUnit.SECONDS)) {
    try {
        // Critical section
    } finally {
        lock.unlock();
    }
}
```

### 52. Explain Java's `ReadWriteLock`.

**Answer:**
ReadWriteLock allows multiple readers or single writer.

```java
ReadWriteLock lock = new ReentrantReadWriteLock();
Lock readLock = lock.readLock();
Lock writeLock = lock.writeLock();

// Read operation
readLock.lock();
try {
    // Read data
} finally {
    readLock.unlock();
}

// Write operation
writeLock.lock();
try {
    // Write data
} finally {
    writeLock.unlock();
}
```

**Benefits:**
- Multiple concurrent readers
- Exclusive writer
- Better performance for read-heavy workloads

### 53. Explain Java's `StampedLock`.

**Answer:**
StampedLock provides optimistic and pessimistic locking.

```java
StampedLock lock = new StampedLock();

// Optimistic read
long stamp = lock.tryOptimisticRead();
// Read data
if (!lock.validate(stamp)) {
    // Fallback to pessimistic read
    stamp = lock.readLock();
    try {
        // Read data
    } finally {
        lock.unlockRead(stamp);
    }
}

// Pessimistic read
long stamp = lock.readLock();
try {
    // Read data
} finally {
    lock.unlockRead(stamp);
}

// Write lock
long stamp = lock.writeLock();
try {
    // Write data
} finally {
    lock.unlockWrite(stamp);
}
```

**Benefits:**
- Optimistic reads (no locking)
- Better performance than ReadWriteLock
- More complex API

### 54. Explain Java's `Phaser`.

**Answer:**
Phaser is reusable synchronization barrier.

```java
Phaser phaser = new Phaser(3); // 3 parties

// Thread 1
new Thread(() -> {
    phaser.arriveAndAwaitAdvance(); // Wait for all
    // Continue
}).start();

// Thread 2
new Thread(() -> {
    phaser.arriveAndAwaitAdvance();
    // Continue
}).start();

// Thread 3
new Thread(() -> {
    phaser.arriveAndAwaitAdvance();
    // Continue
}).start();
```

**Features:**
- Dynamic party registration
- Multiple phases
- More flexible than CyclicBarrier

### 55. Explain Java's `Exchanger`.

**Answer:**
Exchanger allows two threads to exchange data.

```java
Exchanger<String> exchanger = new Exchanger<>();

// Thread 1
new Thread(() -> {
    try {
        String data = exchanger.exchange("Data from thread 1");
        System.out.println("Received: " + data);
    } catch (InterruptedException e) {}
}).start();

// Thread 2
new Thread(() -> {
    try {
        String data = exchanger.exchange("Data from thread 2");
        System.out.println("Received: " + data);
    } catch (InterruptedException e) {}
}).start();
```

**Use Cases:**
- Producer-consumer with data exchange
- Pipeline processing

---

This covers Java interview questions from beginner to advanced level. Each answer includes code examples and explanations.

