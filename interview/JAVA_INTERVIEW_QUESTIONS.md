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

---

This covers Java interview questions from beginner to advanced level. Each answer includes code examples and explanations.

