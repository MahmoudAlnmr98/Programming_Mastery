# Complete Java Mastery Guide

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Data Types & Variables](#data-types--variables)
3. [Operators & Expressions](#operators--expressions)
4. [Control Flow](#control-flow)
5. [Classes & Objects](#classes--objects)
6. [Inheritance & Polymorphism](#inheritance--polymorphism)
7. [Interfaces & Abstract Classes](#interfaces--abstract-classes)
8. [Packages & Access Modifiers](#packages--access-modifiers)
9. [Arrays & Collections](#arrays--collections)
10. [Generics](#generics)
11. [Exception Handling](#exception-handling)
12. [I/O Operations](#io-operations)
13. [Multithreading](#multithreading)
14. [Lambda Expressions & Streams](#lambda-expressions--streams)
15. [Annotations](#annotations)
16. [Reflection](#reflection)
17. [Design Patterns](#design-patterns)
18. [Memory Management](#memory-management)
19. [Performance Optimization](#performance-optimization)
20. [Best Practices](#best-practices)
21. [Advanced Topics](#advanced-topics)

---

## Fundamentals

### What is Java?
Java is a high-level, object-oriented programming language that is:
- **Platform Independent**: Write once, run anywhere (WORA) via JVM
- **Object-Oriented**: Everything is an object (except primitives)
- **Strongly Typed**: Type checking at compile time
- **Garbage Collected**: Automatic memory management
- **Multi-threaded**: Built-in support for concurrent programming
- **Secure**: Security features built into the language

### Java Architecture
```
Source Code (.java) 
    ↓
Compiler (javac)
    ↓
Bytecode (.class)
    ↓
JVM (Java Virtual Machine)
    ↓
Machine Code
```

### JVM, JRE, JDK
- **JDK (Java Development Kit)**: Tools to develop Java applications
- **JRE (Java Runtime Environment)**: Runtime environment to run Java applications
- **JVM (Java Virtual Machine)**: Virtual machine that executes bytecode

### Hello World
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

---

## Data Types & Variables

### Primitive Data Types
```java
// Integer types
byte b = 127;           // 8-bit, -128 to 127
short s = 32767;        // 16-bit, -32,768 to 32,767
int i = 2147483647;     // 32-bit, -2^31 to 2^31-1
long l = 9223372036854775807L; // 64-bit, -2^63 to 2^63-1

// Floating point types
float f = 3.14f;        // 32-bit IEEE 754
double d = 3.141592653589793; // 64-bit IEEE 754

// Character type
char c = 'A';           // 16-bit Unicode character

// Boolean type
boolean bool = true;    // true or false
```

### Reference Types
```java
// Objects (everything else)
String str = "Hello";
Object obj = new Object();
int[] array = new int[10];
MyClass myObj = new MyClass();
```

### Variable Declarations
```java
// Local variables
int x = 10;
String name = "John";

// Instance variables (non-static fields)
class MyClass {
    int instanceVar = 20;
}

// Class variables (static fields)
class MyClass {
    static int classVar = 30;
}

// Final variables (constants)
final int CONSTANT = 100;
final String MESSAGE = "Hello";
```

### Type Conversion
```java
// Widening (automatic)
int i = 10;
long l = i;        // Automatic conversion
double d = i;      // Automatic conversion

// Narrowing (explicit cast required)
double d = 10.5;
int i = (int) d;   // Explicit cast, i = 10

// String conversion
int num = 42;
String str = String.valueOf(num);  // "42"
int back = Integer.parseInt(str);   // 42
```

### Wrapper Classes
```java
// Primitive to Wrapper (autoboxing)
Integer i = 10;        // Autoboxing
int primitive = i;     // Unboxing

// Wrapper classes
Integer, Long, Short, Byte
Float, Double
Character
Boolean

// Useful methods
Integer.parseInt("123");
Integer.valueOf("123");
String.valueOf(123);
```

---

## Operators & Expressions

### Arithmetic Operators
```java
+  // Addition
-  // Subtraction
*  // Multiplication
/  // Division
%  // Modulo
++ // Increment
-- // Decrement
```

### Comparison Operators
```java
==  // Equal to
!=  // Not equal to
<   // Less than
>   // Greater than
<=  // Less than or equal
>=  // Greater than or equal
```

### Logical Operators
```java
&&  // Logical AND
||  // Logical OR
!   // Logical NOT
&   // Bitwise AND (also boolean)
|   // Bitwise OR (also boolean)
^   // Bitwise XOR
```

### Assignment Operators
```java
=   // Assignment
+=  // Addition assignment
-=  // Subtraction assignment
*=  // Multiplication assignment
/=  // Division assignment
%=  // Modulo assignment
```

### Bitwise Operators
```java
&   // AND
|   // OR
^   // XOR
~   // NOT
<<  // Left shift
>>  // Right shift (signed)
>>> // Right shift (unsigned)
```

### Other Operators
```java
// Ternary operator
int result = condition ? valueIfTrue : valueIfFalse;

// instanceof operator
if (obj instanceof String) {
    String str = (String) obj;
}

// new operator
MyClass obj = new MyClass();
```

---

## Control Flow

### Conditional Statements
```java
// if/else
if (condition) {
    // code
} else if (anotherCondition) {
    // code
} else {
    // code
}

// Ternary
int result = condition ? value1 : value2;

// Switch (traditional)
switch (value) {
    case 1:
        // code
        break;
    case 2:
    case 3:
        // code (fall-through)
        break;
    default:
        // code
}

// Switch expressions (Java 14+)
int result = switch (value) {
    case 1 -> 10;
    case 2, 3 -> 20;
    default -> 0;
};
```

### Loops
```java
// for loop
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// Enhanced for loop (for-each)
for (int num : array) {
    System.out.println(num);
}

// while loop
while (condition) {
    // code
}

// do-while loop
do {
    // code
} while (condition);
```

### Control Flow Statements
```java
break;      // Exit loop or switch
continue;   // Skip to next iteration
return;     // Exit method
throw;      // Throw exception
```

---

## Classes & Objects

### Class Definition
```java
public class Person {
    // Fields (instance variables)
    private String name;
    private int age;
    
    // Constructor
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Default constructor
    public Person() {
        this("Unknown", 0);
    }
    
    // Methods
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
}
```

### Object Creation
```java
// Using new keyword
Person person = new Person("John", 30);

// Accessing members
person.display();
String name = person.getName();
```

### Constructor Overloading
```java
public class Rectangle {
    private int width;
    private int height;
    
    public Rectangle() {
        this(1, 1);
    }
    
    public Rectangle(int size) {
        this(size, size);
    }
    
    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }
}
```

### Static Members
```java
public class MathUtils {
    // Static variable
    private static int count = 0;
    
    // Static method
    public static int add(int a, int b) {
        return a + b;
    }
    
    // Static block (initialization)
    static {
        count = 0;
    }
}

// Accessing static members
int result = MathUtils.add(5, 3);
```

### this Keyword
```java
public class MyClass {
    private int value;
    
    public void setValue(int value) {
        this.value = value;  // this refers to current instance
    }
    
    public MyClass getInstance() {
        return this;  // Return current instance
    }
}
```

### Method Overloading
```java
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public double add(double a, double b) {
        return a + b;
    }
    
    public int add(int a, int b, int c) {
        return a + b + c;
    }
}
```

---

## Inheritance & Polymorphism

### Inheritance
```java
// Parent class
public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public void eat() {
        System.out.println(name + " is eating");
    }
    
    public void sleep() {
        System.out.println(name + " is sleeping");
    }
}

// Child class
public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, String breed) {
        super(name);  // Call parent constructor
        this.breed = breed;
    }
    
    public void bark() {
        System.out.println(name + " is barking");
    }
    
    // Method overriding
    @Override
    public void eat() {
        super.eat();  // Call parent method
        System.out.println("Dog food");
    }
}
```

### Method Overriding
```java
public class Shape {
    public double area() {
        return 0;
    }
}

public class Circle extends Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}
```

### super Keyword
```java
public class Child extends Parent {
    public Child() {
        super();  // Call parent constructor
    }
    
    public void method() {
        super.method();  // Call parent method
    }
}
```

### Polymorphism
```java
// Runtime polymorphism
Animal animal = new Dog("Buddy", "Golden Retriever");
animal.eat();  // Calls Dog's eat() method

// Polymorphic array
Animal[] animals = {
    new Dog("Buddy", "Labrador"),
    new Cat("Whiskers")
};

for (Animal a : animals) {
    a.eat();  // Calls appropriate eat() method
}
```

### final Keyword
```java
// Final variable (constant)
final int MAX_SIZE = 100;

// Final method (cannot be overridden)
public final void method() {
    // code
}

// Final class (cannot be extended)
public final class ImmutableClass {
    // code
}
```

---

## Interfaces & Abstract Classes

### Interfaces
```java
// Interface definition
public interface Drawable {
    // Constant (implicitly public static final)
    String COLOR = "Black";
    
    // Abstract method (implicitly public abstract)
    void draw();
    
    // Default method (Java 8+)
    default void display() {
        System.out.println("Displaying");
    }
    
    // Static method (Java 8+)
    static void info() {
        System.out.println("Drawable interface");
    }
}

// Implementing interface
public class Circle implements Drawable {
    @Override
    public void draw() {
        System.out.println("Drawing circle");
    }
}

// Multiple interfaces
public class Square implements Drawable, Resizable {
    // Implement both interfaces
}
```

### Functional Interfaces (Java 8+)
```java
@FunctionalInterface
public interface Calculator {
    int calculate(int a, int b);
}

// Using lambda
Calculator add = (a, b) -> a + b;
int result = add.calculate(5, 3);
```

### Abstract Classes
```java
public abstract class Shape {
    protected String color;
    
    // Abstract method (must be implemented by subclass)
    public abstract double area();
    
    // Concrete method
    public void setColor(String color) {
        this.color = color;
    }
}

public class Rectangle extends Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double area() {
        return width * height;
    }
}
```

### Interface vs Abstract Class
- **Interface**: Multiple inheritance, all methods abstract (before Java 8), no instance variables
- **Abstract Class**: Single inheritance, can have concrete methods, can have instance variables

---

## Packages & Access Modifiers

### Packages
```java
// Package declaration
package com.example.util;

// Import statement
import java.util.ArrayList;
import java.util.List;
import java.util.*;  // Wildcard import

// Static import
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;
```

### Access Modifiers
```java
public class MyClass {
    public int publicVar;        // Accessible everywhere
    protected int protectedVar;  // Accessible in package and subclasses
    int packageVar;              // Accessible in package only (default)
    private int privateVar;      // Accessible in class only
    
    public void publicMethod() { }
    protected void protectedMethod() { }
    void packageMethod() { }
    private void privateMethod() { }
}
```

### Access Levels
```
Modifier    | Class | Package | Subclass | World
------------|-------|---------|----------|-------
public      |   ✓   |    ✓    |    ✓     |   ✓
protected   |   ✓   |    ✓    |    ✓     |   ✗
(default)   |   ✓   |    ✓    |    ✗     |   ✗
private     |   ✓   |    ✗    |    ✗     |   ✗
```

---

## Arrays & Collections

### Arrays
```java
// Array declaration and initialization
int[] numbers = new int[5];
int[] numbers = {1, 2, 3, 4, 5};
int[] numbers = new int[]{1, 2, 3, 4, 5};

// Accessing elements
numbers[0] = 10;
int value = numbers[0];

// Array length
int length = numbers.length;

// Multi-dimensional arrays
int[][] matrix = new int[3][3];
int[][] matrix = {{1, 2, 3}, {4, 5, 6}};

// Array methods
Arrays.sort(numbers);
Arrays.fill(numbers, 0);
Arrays.copyOf(numbers, 10);
Arrays.binarySearch(numbers, 5);
```

### Collections Framework
```java
// List (ordered, allows duplicates)
List<String> list = new ArrayList<>();
list.add("Apple");
list.add("Banana");
list.get(0);
list.size();
list.remove(0);
list.contains("Apple");

// Set (no duplicates)
Set<String> set = new HashSet<>();
set.add("Apple");
set.contains("Apple");
set.remove("Apple");

// Map (key-value pairs)
Map<String, Integer> map = new HashMap<>();
map.put("Apple", 1);
map.get("Apple");
map.containsKey("Apple");
map.remove("Apple");
```

### List Implementations
```java
// ArrayList (dynamic array)
List<String> arrayList = new ArrayList<>();

// LinkedList (doubly linked list)
List<String> linkedList = new LinkedList<>();

// Vector (synchronized ArrayList)
List<String> vector = new Vector<>();
```

### Set Implementations
```java
// HashSet (hash table, no order)
Set<String> hashSet = new HashSet<>();

// LinkedHashSet (hash table + linked list, insertion order)
Set<String> linkedHashSet = new LinkedHashSet<>();

// TreeSet (red-black tree, sorted)
Set<String> treeSet = new TreeSet<>();
```

### Map Implementations
```java
// HashMap (hash table, no order)
Map<String, Integer> hashMap = new HashMap<>();

// LinkedHashMap (hash table + linked list, insertion order)
Map<String, Integer> linkedHashMap = new LinkedHashMap<>();

// TreeMap (red-black tree, sorted)
Map<String, Integer> treeMap = new TreeMap<>();
```

### Collection Operations
```java
// Iterating
for (String item : list) {
    System.out.println(item);
}

// Iterator
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String item = it.next();
}

// Stream API (Java 8+)
list.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .forEach(System.out::println);
```

---

## Generics

### Generic Classes
```java
public class Box<T> {
    private T item;
    
    public void setItem(T item) {
        this.item = item;
    }
    
    public T getItem() {
        return item;
    }
}

// Usage
Box<String> stringBox = new Box<>();
stringBox.setItem("Hello");
String value = stringBox.getItem();

Box<Integer> intBox = new Box<>();
intBox.setItem(42);
Integer num = intBox.getItem();
```

### Generic Methods
```java
public class Utils {
    public static <T> void printArray(T[] array) {
        for (T item : array) {
            System.out.println(item);
        }
    }
    
    public static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }
}
```

### Bounded Type Parameters
```java
// Upper bound
public class NumberBox<T extends Number> {
    private T number;
    
    public double getDoubleValue() {
        return number.doubleValue();
    }
}

// Multiple bounds
public class MultiBound<T extends Number & Comparable<T>> {
    // T must extend Number and implement Comparable
}
```

### Wildcards
```java
// Unbounded wildcard
public void printList(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}

// Upper bounded wildcard
public void processNumbers(List<? extends Number> numbers) {
    // Can read, but cannot add
}

// Lower bounded wildcard
public void addNumbers(List<? super Integer> numbers) {
    numbers.add(42);  // Can add, but limited reading
}
```

---

## Exception Handling

### Try-Catch-Finally
```java
try {
    // Risky code
    int result = 10 / 0;
} catch (ArithmeticException e) {
    // Handle specific exception
    System.out.println("Division by zero: " + e.getMessage());
} catch (Exception e) {
    // Handle general exception
    System.out.println("Error: " + e.getMessage());
} finally {
    // Always executes
    System.out.println("Cleanup");
}
```

### Checked vs Unchecked Exceptions
```java
// Checked exception (must be handled or declared)
public void readFile() throws IOException {
    FileReader file = new FileReader("file.txt");
}

// Unchecked exception (RuntimeException)
public void divide(int a, int b) {
    if (b == 0) {
        throw new ArithmeticException("Division by zero");
    }
    return a / b;
}
```

### Custom Exceptions
```java
// Custom checked exception
public class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
    }
}

// Custom unchecked exception
public class CustomRuntimeException extends RuntimeException {
    public CustomRuntimeException(String message) {
        super(message);
    }
}

// Usage
throw new CustomException("Something went wrong");
```

### Exception Hierarchy
```
Throwable
├── Error (unchecked)
│   ├── OutOfMemoryError
│   └── StackOverflowError
└── Exception
    ├── RuntimeException (unchecked)
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   └── ArithmeticException
    └── Checked Exceptions
        ├── IOException
        ├── SQLException
        └── ClassNotFoundException
```

### Try-With-Resources (Java 7+)
```java
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
} catch (IOException e) {
    e.printStackTrace();
}
// Resources automatically closed
```

### Multiple Exceptions (Java 7+)
```java
try {
    // code
} catch (IOException | SQLException e) {
    // Handle both exceptions
    e.printStackTrace();
}
```

---

## I/O Operations

### File Operations
```java
import java.io.*;

// Reading file
try (BufferedReader br = new BufferedReader(
        new FileReader("file.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}

// Writing file
try (BufferedWriter bw = new BufferedWriter(
        new FileWriter("output.txt"))) {
    bw.write("Hello, World!");
} catch (IOException e) {
    e.printStackTrace();
}
```

### Scanner
```java
import java.util.Scanner;

Scanner scanner = new Scanner(System.in);
System.out.print("Enter your name: ");
String name = scanner.nextLine();
System.out.print("Enter your age: ");
int age = scanner.nextInt();
scanner.close();
```

### File Class
```java
import java.io.File;

File file = new File("example.txt");
file.exists();
file.isFile();
file.isDirectory();
file.length();
file.getName();
file.getAbsolutePath();
file.delete();
file.createNewFile();
```

### NIO (New I/O) - Java 7+
```java
import java.nio.file.*;

// Read all lines
List<String> lines = Files.readAllLines(Paths.get("file.txt"));

// Write lines
Files.write(Paths.get("output.txt"), lines);

// Copy file
Files.copy(source, destination, StandardCopyOption.REPLACE_EXISTING);

// Delete file
Files.delete(Paths.get("file.txt"));
```

---

## Multithreading

### Thread Creation
```java
// Extending Thread class
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running");
    }
}

MyThread thread = new MyThread();
thread.start();

// Implementing Runnable interface
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}

Thread thread = new Thread(new MyRunnable());
thread.start();

// Lambda expression (Java 8+)
Thread thread = new Thread(() -> {
    System.out.println("Lambda thread");
});
thread.start();
```

### Thread Methods
```java
thread.start();        // Start thread
thread.join();         // Wait for thread to complete
thread.sleep(1000);    // Sleep for 1 second
thread.interrupt();    // Interrupt thread
thread.isAlive();      // Check if thread is alive
Thread.currentThread(); // Get current thread
```

### Synchronization
```java
// Synchronized method
public synchronized void increment() {
    count++;
}

// Synchronized block
public void increment() {
    synchronized (this) {
        count++;
    }
}

// Synchronized static method
public static synchronized void method() {
    // code
}
```

### wait(), notify(), notifyAll()
```java
public class ProducerConsumer {
    private final Object lock = new Object();
    private boolean available = false;
    
    public void produce() throws InterruptedException {
        synchronized (lock) {
            while (available) {
                lock.wait();  // Wait until consumed
            }
            // Produce item
            available = true;
            lock.notify();  // Notify consumer
        }
    }
    
    public void consume() throws InterruptedException {
        synchronized (lock) {
            while (!available) {
                lock.wait();  // Wait until produced
            }
            // Consume item
            available = false;
            lock.notify();  // Notify producer
        }
    }
}
```

### Executor Framework (Java 5+)
```java
import java.util.concurrent.*;

// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(5);
executor.submit(() -> {
    System.out.println("Task running");
});
executor.shutdown();

// ScheduledExecutorService
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
scheduler.schedule(() -> {
    System.out.println("Delayed task");
}, 5, TimeUnit.SECONDS);
```

### Concurrent Collections
```java
import java.util.concurrent.*;

// Thread-safe collections
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
BlockingQueue<String> queue = new LinkedBlockingQueue<>();
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
```

### Atomic Classes
```java
import java.util.concurrent.atomic.*;

AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.getAndIncrement();
counter.compareAndSet(0, 10);
```

---

## Lambda Expressions & Streams

### Lambda Expressions (Java 8+)
```java
// Before (anonymous inner class)
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};

// After (lambda)
Runnable r = () -> System.out.println("Hello");

// With parameters
Comparator<String> comp = (s1, s2) -> s1.compareTo(s2);

// Method reference
Comparator<String> comp = String::compareTo;
```

### Functional Interfaces
```java
// Predicate (test condition)
Predicate<String> isEmpty = s -> s.isEmpty();
isEmpty.test("");  // true

// Function (transform)
Function<String, Integer> length = s -> s.length();
length.apply("Hello");  // 5

// Consumer (consume value)
Consumer<String> print = s -> System.out.println(s);
print.accept("Hello");

// Supplier (provide value)
Supplier<String> supplier = () -> "Hello";
supplier.get();
```

### Stream API (Java 8+)
```java
import java.util.stream.*;

List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// Filter
names.stream()
    .filter(name -> name.startsWith("A"))
    .forEach(System.out::println);

// Map
names.stream()
    .map(String::toUpperCase)
    .forEach(System.out::println);

// Reduce
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Collect
List<String> filtered = names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());

// Parallel stream
names.parallelStream()
    .forEach(System.out::println);
```

### Stream Operations
```java
// Intermediate operations (lazy)
stream.filter(...)
stream.map(...)
stream.sorted(...)
stream.distinct()
stream.limit(n)
stream.skip(n)

// Terminal operations (eager)
stream.forEach(...)
stream.collect(...)
stream.reduce(...)
stream.count()
stream.anyMatch(...)
stream.allMatch(...)
stream.findFirst()
stream.findAny()
```

---

## Annotations

### Built-in Annotations
```java
@Override       // Indicates method overrides parent
@Deprecated     // Marks element as deprecated
@SuppressWarnings("unchecked")  // Suppress warnings
@SafeVarargs    // Safe variable arguments
@FunctionalInterface  // Functional interface
```

### Custom Annotations
```java
// Define annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyAnnotation {
    String value() default "";
    int count() default 0;
}

// Use annotation
@MyAnnotation(value = "test", count = 5)
public void myMethod() {
    // code
}
```

### Meta-Annotations
```java
@Target(ElementType.METHOD)      // Where annotation can be used
@Retention(RetentionPolicy.RUNTIME)  // How long annotation is retained
@Documented                       // Include in JavaDoc
@Inherited                        // Inherited by subclasses
public @interface MyAnnotation {
    // ...
}
```

---

## Reflection

### Class Reflection
```java
import java.lang.reflect.*;

// Get Class object
Class<?> clazz = MyClass.class;
Class<?> clazz = obj.getClass();
Class<?> clazz = Class.forName("com.example.MyClass");

// Get fields
Field[] fields = clazz.getDeclaredFields();
Field field = clazz.getDeclaredField("fieldName");

// Get methods
Method[] methods = clazz.getDeclaredMethods();
Method method = clazz.getDeclaredMethod("methodName", paramTypes);

// Get constructors
Constructor<?>[] constructors = clazz.getDeclaredConstructors();
Constructor<?> constructor = clazz.getDeclaredConstructor(paramTypes);

// Create instance
Object instance = constructor.newInstance(args);

// Invoke method
method.setAccessible(true);
Object result = method.invoke(instance, args);

// Access field
field.setAccessible(true);
field.set(instance, value);
Object value = field.get(instance);
```

---

## Design Patterns

### Singleton Pattern
```java
public class Singleton {
    private static Singleton instance;
    
    private Singleton() {
        // Private constructor
    }
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// Enum singleton (thread-safe)
public enum Singleton {
    INSTANCE;
    
    public void doSomething() {
        // code
    }
}
```

### Factory Pattern
```java
public interface Animal {
    void makeSound();
}

public class Dog implements Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof");
    }
}

public class Cat implements Animal {
    @Override
    public void makeSound() {
        System.out.println("Meow");
    }
}

public class AnimalFactory {
    public static Animal createAnimal(String type) {
        if ("dog".equalsIgnoreCase(type)) {
            return new Dog();
        } else if ("cat".equalsIgnoreCase(type)) {
            return new Cat();
        }
        throw new IllegalArgumentException("Unknown animal type");
    }
}
```

### Observer Pattern
```java
import java.util.*;

public interface Observer {
    void update(String message);
}

public class Subject {
    private List<Observer> observers = new ArrayList<>();
    
    public void addObserver(Observer observer) {
        observers.add(observer);
    }
    
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }
    
    public void notifyObservers(String message) {
        for (Observer observer : observers) {
            observer.update(message);
        }
    }
}
```

### Builder Pattern
```java
public class Person {
    private String name;
    private int age;
    private String email;
    
    private Person(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.email = builder.email;
    }
    
    public static class Builder {
        private String name;
        private int age;
        private String email;
        
        public Builder name(String name) {
            this.name = name;
            return this;
        }
        
        public Builder age(int age) {
            this.age = age;
            return this;
        }
        
        public Builder email(String email) {
            this.email = email;
            return this;
        }
        
        public Person build() {
            return new Person(this);
        }
    }
}

// Usage
Person person = new Person.Builder()
    .name("John")
    .age(30)
    .email("john@example.com")
    .build();
```

### Strategy Pattern
```java
public interface PaymentStrategy {
    void pay(double amount);
}

public class CreditCardPayment implements PaymentStrategy {
    @Override
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using credit card");
    }
}

public class PayPalPayment implements PaymentStrategy {
    @Override
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using PayPal");
    }
}

public class ShoppingCart {
    private PaymentStrategy paymentStrategy;
    
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }
    
    public void checkout(double amount) {
        paymentStrategy.pay(amount);
    }
}
```

---

## Memory Management

### Garbage Collection
```java
// Request garbage collection (hint, not guaranteed)
System.gc();

// Finalize method (deprecated in Java 9+)
@Override
protected void finalize() throws Throwable {
    // Cleanup code
    super.finalize();
}

// Try-with-resources for automatic cleanup
try (Resource resource = new Resource()) {
    // Use resource
} // Resource automatically closed
```

### Memory Leaks Prevention
```java
// 1. Close resources
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // Use file
} // Automatically closed

// 2. Remove listeners
button.removeActionListener(listener);

// 3. Clear collections
list.clear();
map.clear();

// 4. Null references
largeObject = null;

// 5. Use WeakReference for caches
WeakReference<Object> weakRef = new WeakReference<>(object);
```

### Heap Memory
```java
// Get heap memory info
Runtime runtime = Runtime.getRuntime();
long maxMemory = runtime.maxMemory();
long totalMemory = runtime.totalMemory();
long freeMemory = runtime.freeMemory();
long usedMemory = totalMemory - freeMemory;
```

---

## Performance Optimization

### String Optimization
```java
// Use StringBuilder for string concatenation in loops
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();

// Use StringBuffer for thread-safe operations
StringBuffer sb = new StringBuffer();
```

### Collection Optimization
```java
// Pre-size collections when size is known
List<String> list = new ArrayList<>(1000);
Map<String, Integer> map = new HashMap<>(1000);

// Use appropriate collection type
// ArrayList for random access
// LinkedList for frequent insertions/deletions
// HashSet for fast lookups
// TreeSet for sorted data
```

### Caching
```java
// Simple cache using HashMap
public class Cache<K, V> {
    private Map<K, V> cache = new HashMap<>();
    
    public V get(K key) {
        return cache.get(key);
    }
    
    public void put(K key, V value) {
        cache.put(key, value);
    }
}

// LRU Cache using LinkedHashMap
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### Profiling
```java
// Measure execution time
long startTime = System.currentTimeMillis();
// Code to measure
long endTime = System.currentTimeMillis();
long duration = endTime - startTime;

// Using System.nanoTime() for more precision
long startTime = System.nanoTime();
// Code to measure
long endTime = System.nanoTime();
long duration = (endTime - startTime) / 1_000_000; // Convert to milliseconds
```

---

## Best Practices

### Code Quality
1. **Follow naming conventions**
   - Classes: PascalCase (MyClass)
   - Methods/Variables: camelCase (myMethod)
   - Constants: UPPER_SNAKE_CASE (MAX_SIZE)
   - Packages: lowercase (com.example.util)

2. **Use meaningful names**
   ```java
   // Bad
   int x = 10;
   void m() { }
   
   // Good
   int userCount = 10;
   void calculateTotal() { }
   ```

3. **Keep methods small and focused**
   ```java
   // Bad
   public void processData() {
       // 100 lines of code
   }
   
   // Good
   public void processData() {
       validateInput();
       transformData();
       saveData();
   }
   ```

4. **Use appropriate access modifiers**
   ```java
   // Make fields private, provide getters/setters
   private int value;
   public int getValue() { return value; }
   public void setValue(int value) { this.value = value; }
   ```

5. **Prefer composition over inheritance**
   ```java
   // Composition
   public class Car {
       private Engine engine;
       private Wheel[] wheels;
   }
   ```

6. **Use interfaces for abstraction**
   ```java
   // Program to interface, not implementation
   List<String> list = new ArrayList<>();
   ```

7. **Handle exceptions properly**
   ```java
   // Don't swallow exceptions
   try {
       // code
   } catch (Exception e) {
       logger.error("Error occurred", e);
       throw new CustomException("Failed to process", e);
   }
   ```

8. **Use try-with-resources**
   ```java
   // Automatic resource management
   try (Resource resource = new Resource()) {
       // Use resource
   }
   ```

9. **Avoid null pointer exceptions**
   ```java
   // Check for null
   if (obj != null) {
       obj.method();
   }
   
   // Use Optional (Java 8+)
   Optional<String> optional = Optional.ofNullable(str);
   optional.ifPresent(System.out::println);
   ```

10. **Use immutable objects when possible**
    ```java
    // Immutable class
    public final class ImmutableClass {
        private final String value;
        
        public ImmutableClass(String value) {
            this.value = value;
        }
        
        public String getValue() {
            return value;
        }
    }
    ```

### Performance
1. **Use StringBuilder for string concatenation in loops**
2. **Pre-size collections when size is known**
3. **Use appropriate collection types**
4. **Avoid unnecessary object creation**
5. **Use primitive types when possible**
6. **Cache expensive computations**
7. **Use parallel streams for CPU-intensive tasks**
8. **Profile before optimizing**

### Security
1. **Validate input**
   ```java
   public void processInput(String input) {
       if (input == null || input.isEmpty()) {
           throw new IllegalArgumentException("Input cannot be null or empty");
       }
       // Process input
   }
   ```

2. **Use prepared statements for SQL**
   ```java
   PreparedStatement stmt = connection.prepareStatement(
       "SELECT * FROM users WHERE id = ?");
   stmt.setInt(1, userId);
   ```

3. **Don't log sensitive information**
4. **Use secure random for security-sensitive operations**
   ```java
   SecureRandom random = new SecureRandom();
   byte[] bytes = new byte[16];
   random.nextBytes(bytes);
   ```

---

## Advanced Topics

### Optional (Java 8+)
```java
import java.util.Optional;

// Create Optional
Optional<String> optional = Optional.of("value");
Optional<String> empty = Optional.empty();
Optional<String> nullable = Optional.ofNullable(null);

// Check and get
if (optional.isPresent()) {
    String value = optional.get();
}

// Functional style
optional.ifPresent(System.out::println);
String value = optional.orElse("default");
String value = optional.orElseGet(() -> "default");
String value = optional.orElseThrow(() -> new RuntimeException());

// Transform
Optional<Integer> length = optional.map(String::length);
Optional<String> upper = optional.filter(s -> s.length() > 5);
```

### CompletableFuture (Java 8+)
```java
import java.util.concurrent.*;

// Create CompletableFuture
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "Result";
});

// Chain operations
future
    .thenApply(String::toUpperCase)
    .thenAccept(System.out::println)
    .thenRun(() -> System.out.println("Done"));

// Combine futures
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = future1.thenCombine(future2, (a, b) -> a + " " + b);

// Handle errors
future.exceptionally(ex -> {
    System.err.println("Error: " + ex.getMessage());
    return "Default";
});
```

### Records (Java 14+)
```java
// Record definition
public record Person(String name, int age) {
    // Compact constructor
    public Person {
        if (age < 0) {
            throw new IllegalArgumentException("Age cannot be negative");
        }
    }
    
    // Custom methods
    public String greeting() {
        return "Hello, I'm " + name;
    }
}

// Usage
Person person = new Person("John", 30);
String name = person.name();
int age = person.age();
```

### Sealed Classes (Java 17+)
```java
// Sealed class
public sealed class Shape
    permits Circle, Rectangle, Triangle {
    // Base class code
}

// Permitted subclasses
public final class Circle extends Shape {
    // Circle implementation
}

public final class Rectangle extends Shape {
    // Rectangle implementation
}

public final class Triangle extends Shape {
    // Triangle implementation
}
```

### Pattern Matching (Java 14+)
```java
// Pattern matching for instanceof
if (obj instanceof String str) {
    // str is automatically cast to String
    System.out.println(str.length());
}

// Pattern matching in switch (Java 17+)
String result = switch (obj) {
    case String s -> "String: " + s;
    case Integer i -> "Integer: " + i;
    case null -> "Null";
    default -> "Unknown";
};
```

### Modules (Java 9+)
```java
// module-info.java
module com.example.app {
    requires java.base;
    requires java.sql;
    exports com.example.util;
    exports com.example.model to com.example.client;
}
```

### Var Keyword (Java 10+)
```java
// Type inference for local variables
var list = new ArrayList<String>();
var map = new HashMap<String, Integer>();
var name = "John";
var count = 42;

// Cannot use with:
// - Method parameters
// - Return types
// - Fields
// - null initialization
```

---

## Resources for Further Learning

1. **Oracle Java Documentation** - Official Java documentation
2. **Java Tutorials** - Oracle's official tutorials
3. **Effective Java** - Book by Joshua Bloch
4. **Java Concurrency in Practice** - Book on multithreading
5. **Head First Java** - Beginner-friendly book
6. **LeetCode** - Practice algorithms in Java
7. **HackerRank** - Coding challenges
8. **Java Weekly** - Stay updated with Java news

---

## Conclusion

This guide covers Java from fundamentals to advanced topics. Mastery comes through:
- **Practice**: Build projects, solve problems
- **Understanding**: Know why, not just how
- **Reading**: Study well-written code (JDK source code)
- **Teaching**: Explain concepts to others
- **Staying Current**: Follow Java evolution (new releases every 6 months)

Remember: Java is constantly evolving. Keep learning, keep practicing, and keep building!

### Key Takeaways
- Java is object-oriented, platform-independent, and strongly typed
- Master OOP concepts: classes, inheritance, polymorphism, interfaces
- Understand collections framework and generics
- Learn exception handling and multithreading
- Use modern Java features: lambdas, streams, Optional
- Follow best practices for code quality and performance
- Practice design patterns for better code organization

