# The Complete Java & Spring Boot Mastery Guide
> One document to rule them all. Every concept explained from first principles, with theory, diagrams, pitfalls, and production-grade examples.

---

## Table of Contents

### Part I — Core Java
1. [How Java Works — JVM, JDK, JRE](#chapter-1-how-java-works)
2. [Data Types, Variables & Memory](#chapter-2-data-types-variables--memory)
3. [Operators & Expressions](#chapter-3-operators--expressions)
4. [Control Flow](#chapter-4-control-flow)
5. [Methods & Recursion](#chapter-5-methods--recursion)
6. [OOP — Classes, Objects & Encapsulation](#chapter-6-oop--classes-objects--encapsulation)
7. [Inheritance & the IS-A Relationship](#chapter-7-inheritance--the-is-a-relationship)
8. [Polymorphism & Dynamic Dispatch](#chapter-8-polymorphism--dynamic-dispatch)
9. [Abstraction — Abstract Classes & Interfaces](#chapter-9-abstraction--abstract-classes--interfaces)
10. [Strings — Deep Dive](#chapter-10-strings--deep-dive)
11. [Arrays](#chapter-11-arrays)
12. [Collections Framework](#chapter-12-collections-framework)
13. [Generics](#chapter-13-generics)
14. [Exception Handling](#chapter-14-exception-handling)
15. [Java I/O & NIO](#chapter-15-java-io--nio)
16. [Multithreading & Concurrency](#chapter-16-multithreading--concurrency)
17. [Functional Programming — Lambdas & Streams](#chapter-17-functional-programming--lambdas--streams)
18. [Modern Java (Java 8 → 21)](#chapter-18-modern-java-java-8--21)
19. [JVM Internals & Memory Management](#chapter-19-jvm-internals--memory-management)
20. [Design Patterns](#chapter-20-design-patterns)
21. [Annotations & Reflection](#chapter-21-annotations--reflection)

### Part II — Data Structures & Algorithms
22. [Complexity Analysis](#chapter-22-complexity-analysis)
23. [Searching & Sorting](#chapter-23-searching--sorting)
24. [Linked Lists, Stacks & Queues](#chapter-24-linked-lists-stacks--queues)
25. [Trees & Graphs](#chapter-25-trees--graphs)
26. [Dynamic Programming & Greedy](#chapter-26-dynamic-programming--greedy)

### Part III — Enterprise Java
27. [JDBC](#chapter-27-jdbc)
28. [Servlets & JSP](#chapter-28-servlets--jsp)
29. [Hibernate & JPA](#chapter-29-hibernate--jpa)

### Part IV — Spring Ecosystem
30. [Spring Core — IoC & DI](#chapter-30-spring-core--ioc--di)
31. [Spring AOP](#chapter-31-spring-aop)
32. [Spring Boot](#chapter-32-spring-boot)
33. [Spring MVC](#chapter-33-spring-mvc)
34. [Spring REST API](#chapter-34-spring-rest-api)
35. [Spring Data & Transactions](#chapter-35-spring-data--transactions)
36. [Spring Security & JWT](#chapter-36-spring-security--jwt)
37. [Spring Cloud & Microservices](#chapter-37-spring-cloud--microservices)
38. [Testing](#chapter-38-testing)
39. [Build Tools — Maven & Gradle](#chapter-39-build-tools--maven--gradle)

---

# PART I — CORE JAVA

---

## Chapter 1: How Java Works

### 1.1 The Big Picture — Why Java is Special

Most compiled languages (like C/C++) compile directly to **machine code** — binary instructions your specific CPU understands. The problem: a program compiled on Windows x64 won't run on Linux ARM. You must recompile for every target platform.

Java solved this with a two-step approach:

```
Step 1: Compile ONCE
  YourCode.java  ──[javac compiler]──▶  YourCode.class (bytecode)
                                         ↑ platform-independent

Step 2: Run ANYWHERE
  YourCode.class ──[JVM on Windows]──▶  Windows machine code
  YourCode.class ──[JVM on Linux  ]──▶  Linux machine code
  YourCode.class ──[JVM on macOS  ]──▶  macOS machine code
```

**Bytecode** is not machine code — it's an intermediate representation designed for the JVM (Java Virtual Machine). The JVM is a program that reads bytecode and either interprets it or compiles it further to native code (via JIT). Since every OS has a JVM implementation, the same `.class` files run everywhere. This is the **Write Once, Run Anywhere (WORA)** promise.

### 1.2 JDK vs JRE vs JVM — The Exact Difference

People confuse these constantly. Here's the precise breakdown:

```
┌─────────────────────────────────────────────────────────────┐
│  JDK (Java Development Kit)                                  │
│  Everything you need to WRITE and RUN Java programs         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  JRE (Java Runtime Environment)                        │  │
│  │  Everything you need to RUN Java programs              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  JVM (Java Virtual Machine)                      │  │  │
│  │  │  Executes bytecode; manages memory; runs GC      │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  + Java Standard Library (java.util, java.io, etc.)   │  │
│  └───────────────────────────────────────────────────────┘  │
│  + javac (compiler)                                          │
│  + javadoc, jdb (debugger), jconsole, jvisualvm, etc.       │
└─────────────────────────────────────────────────────────────┘
```

- **You are a developer** → install the JDK
- **End user just runs your app** → only needs JRE (or a bundled JDK via jlink)
- **JVM alone** → the runtime engine inside JRE

### 1.3 Inside the JVM — How Bytecode Becomes Execution

The JVM has several subsystems working together:

```
┌──────────────────────────────────────────────────────────────┐
│                      JVM                                       │
│                                                                │
│  ① Class Loader Subsystem                                     │
│     Bootstrap CL → Platform CL → Application CL              │
│     Loads .class files on demand (lazy loading)               │
│                                                                │
│  ② Runtime Data Areas (Memory)                               │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│     │  Method  │ │   Heap   │ │  Stack   │ │  PC Register│  │
│     │   Area   │ │(objects) │ │(frames)  │ │ (per thread)│  │
│     └──────────┘ └──────────┘ └──────────┘ └─────────────┘  │
│                                                                │
│  ③ Execution Engine                                           │
│     Interpreter: reads & executes bytecode one instruction    │
│                  at a time — slow but starts fast             │
│     JIT Compiler: detects "hot" code (run often) and         │
│                   compiles it to native machine code          │
│                   → after warmup, Java is near-native speed  │
│     GC: reclaims memory from unreachable objects              │
└──────────────────────────────────────────────────────────────┘
```

**JIT (Just-In-Time) Compilation** is why Java's reputation for being "slow" is outdated. The JVM profiles your running program and compiles the hottest methods to native code, often with aggressive optimisations (inlining, escape analysis, loop unrolling) that even hand-written C can't beat for long-running server workloads.

### 1.4 The Java Compilation & Execution Cycle

```java
// File: Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

```bash
# Compile: produces Hello.class in the same directory
javac Hello.java

# Run: JVM loads Hello.class and calls main()
java Hello

# See the bytecode (human-readable disassembly)
javap -c Hello.class
```

**What `javap -c Hello` shows:**
```
public static void main(java.lang.String[]);
  Code:
     0: getstatic     #7   // Field java/lang/System.out
     3: ldc           #13  // String "Hello, World!"
     5: invokevirtual #15  // Method println:(Ljava/lang/String;)V
     8: return
```

Each line is a bytecode instruction. `getstatic` loads `System.out` onto the operand stack. `ldc` loads the string literal. `invokevirtual` calls the method. The JVM is a stack machine — most operations push/pop values from an operand stack.

### 1.5 Class Structure — Rules the Compiler Enforces

```java
// Rule 1: ONE public class per file; file name MUST match the public class name
// File: MyProgram.java
public class MyProgram {       // ← public class name matches filename ✅

    // Rule 2: The JVM entry point is ALWAYS this exact signature
    public static void main(String[] args) {
        // 'public'  — JVM must be able to call it from outside
        // 'static'  — JVM calls it without creating an instance
        // 'void'    — returns nothing to the OS
        // 'String[] args' — command-line arguments
    }
}

// Rule 3: A file CAN have multiple non-public classes
class Helper {   // no 'public' — only visible within this package
    void assist() { }
}
```

### 1.6 Java Editions

| Edition | Full Name | Purpose |
|---------|-----------|---------|
| **Java SE** | Standard Edition | Core language, Collections, I/O, concurrency — what this guide covers |
| **Jakarta EE** | Enterprise Edition (formerly Java EE) | Servlets, JPA, JAX-RS, EJB — enterprise server APIs |
| **Java ME** | Micro Edition | Embedded devices, IoT |
| **Java Card** | — | Smart cards, SIM cards |

> This guide covers **Java SE** deeply, then **Jakarta EE components** (Servlets, JPA) and the **Spring Framework** which sits on top of SE.

---

## Chapter 2: Data Types, Variables & Memory

### 2.1 Why Type Systems Exist

A **type** tells the compiler two things: (1) how much memory to allocate, and (2) what operations are valid. `5 / 2` means something different if those are `int`s (result: 2) vs `double`s (result: 2.5). The compiler uses types to catch errors before your code runs — trying to call `.length()` on an `int` is caught at compile time, not as a crash at 3am in production.

Java is **statically typed** (types checked at compile time) and **strongly typed** (no implicit conversions that lose information — you must explicitly cast). This is different from Python (dynamically typed) or C (weakly typed).

### 2.2 The 8 Primitive Types

Java has exactly 8 primitive types. They are **not objects** — they live directly on the **stack** (or inside objects on the heap), have no methods, and are extremely fast.

| Type | Size | Min Value | Max Value | Default | Notes |
|------|------|-----------|-----------|---------|-------|
| `byte` | 8 bits | -128 | 127 | 0 | Useful for binary data, network protocols |
| `short` | 16 bits | -32,768 | 32,767 | 0 | Rarely used; arrays of shorts save memory |
| `int` | 32 bits | -2,147,483,648 | 2,147,483,647 | 0 | **Default integer type** |
| `long` | 64 bits | -9.2 × 10¹⁸ | 9.2 × 10¹⁸ | 0L | Timestamps, large IDs; needs `L` suffix |
| `float` | 32 bits | ~1.4×10⁻⁴⁵ | ~3.4×10³⁸ | 0.0f | ~7 decimal digits precision; needs `f` suffix |
| `double` | 64 bits | ~5×10⁻³²⁴ | ~1.8×10³⁰⁸ | 0.0d | **Default decimal type**; ~15 digits precision |
| `char` | 16 bits | '\u0000' (0) | '\uffff' (65535) | '\u0000' | UTF-16 code unit; single quotes |
| `boolean` | 1 bit* | — | — | false | Only `true` or `false` |

*JVM typically uses 4 bytes for `boolean` fields, 1 byte in arrays, for alignment reasons.

```java
// Literal syntax examples
byte  b  = 127;
short s  = 32_000;          // underscores for readability (Java 7+)
int   i  = 2_147_483_647;
long  l  = 9_223_372_036_854_775_807L;   // 'L' suffix REQUIRED

float  f  = 3.14f;          // 'f' suffix REQUIRED (without it, it's a double literal)
double d  = 3.141592653589793;
double d2 = 1.5e10;         // scientific notation = 15,000,000,000.0

char  c1 = 'A';             // character literal
char  c2 = '\n';            // newline escape sequence
char  c3 = '\u00e9';        // Unicode: é
char  c4 = 65;              // same as 'A' — chars are unsigned 16-bit integers

boolean flag = true;
```

**Why float precision matters:**
```java
float  f = 0.1f + 0.2f;
double d = 0.1  + 0.2;
System.out.println(f);  // 0.3  (accidentally rounds to look correct)
System.out.println(d);  // 0.30000000000000004  (IEEE 754 reality)

// For money: NEVER use float or double. Use BigDecimal.
BigDecimal price = new BigDecimal("0.10").add(new BigDecimal("0.20"));
System.out.println(price);  // 0.30  ✅ exact
```

### 2.3 Reference Types — Everything Else

In Java, every type that isn't a primitive is a **reference type** — classes, interfaces, arrays, enums. A variable of a reference type doesn't hold the object itself; it holds a **reference** (essentially a pointer) to where the object lives on the heap.

```java
// Primitive: value stored directly in variable
int x = 5;   // x IS the value 5

// Reference: variable stores address of object
String name = "Alice";
// name stores the memory address of the String object
// the String object {"Alice"} lives on the heap

Person p1 = new Person("Alice");
Person p2 = p1;   // p2 holds SAME address as p1
                  // they both point to the same object
p2.setName("Bob");
System.out.println(p1.getName());  // "Bob" ← p1 sees the change!
```

**The null reference:**
```java
String s = null;   // s holds no address — it points to nothing
s.length();        // NullPointerException — can't call method on nothing
```

`null` is not an object; it's the absence of a reference. Java 14+ gives helpful NPE messages:
```
Cannot invoke "String.length()" because "s" is null
```

### 2.4 Variable Scope and Kinds

```java
public class BankAccount {

    // ① Instance variable (field) — belongs to each object
    //    Lives on the heap inside the object
    //    Initialised to default (0, false, null) if not set
    private double balance;
    private String owner;

    // ② Static (class) variable — ONE copy shared by ALL instances
    //    Lives in the Method Area (not the heap per-object)
    private static int totalAccounts = 0;
    public static final double INTEREST_RATE = 0.05;  // constant

    // ③ Static initializer block — runs once when class first loads
    static {
        System.out.println("BankAccount class loaded");
        totalAccounts = loadFromDatabase();  // one-time setup
    }

    public BankAccount(String owner, double initialBalance) {
        // ④ Local variable — lives on the stack; MUST be initialized before use
        //    No default value — reading uninitialized local = compile error
        double fee = 5.0;                    // local variable
        this.owner = owner;
        this.balance = initialBalance - fee;
        totalAccounts++;
    }

    public void deposit(double amount) {
        // Local variables are created on method entry and destroyed on exit
        boolean valid = amount > 0;          // local boolean
        if (valid) {
            balance += amount;
        }
        // 'valid' ceases to exist here
    }
}
```

### 2.5 Type Conversion — Widening vs Narrowing

**Widening conversion** goes from a "smaller" type to a "larger" type. No data is lost, so the compiler does it automatically (implicitly).

```
byte → short → int → long → float → double
                 ↑
                char
```

```java
int    i = 100;
long   l = i;        // widening: int → long (automatic, no cast)
double d = i;        // widening: int → double (automatic)
float  f = i;        // widening: int → float (automatic, but precision loss for large ints!)

// Tricky: int → float can lose precision!
int big = 123_456_789;
float f2 = big;
System.out.println(big);  // 123456789
System.out.println(f2);   // 1.23456792E8  ← slight precision loss
```

**Narrowing conversion** goes to a smaller type. Data MAY be lost — the compiler forces you to be explicit with a cast.

```java
double d = 9.99;
int    i = (int) d;     // truncates (not rounds): i = 9
System.out.println(i);  // 9

long big = 10_000_000_000L;   // too big for int
int  cut = (int) big;         // only keeps lower 32 bits: 1410065408
System.out.println(cut);      // 1410065408 — silent data corruption!

// The cast tells the compiler: "I know what I'm doing"
// It does NOT change the underlying bits intelligently
```

**Numeric String conversions:**
```java
// int → String
String s1 = String.valueOf(42);      // "42"  (preferred)
String s2 = Integer.toString(42);    // "42"
String s3 = 42 + "";                 // "42"  (works but inefficient — creates StringBuilder)

// String → int
int n1 = Integer.parseInt("42");     // 42
int n2 = Integer.valueOf("42");      // returns Integer (autoboxed to int)
// Integer.parseInt("abc") → NumberFormatException

// Numeric conversions
int n = 255;
System.out.println(Integer.toBinaryString(n));  // "11111111"
System.out.println(Integer.toHexString(n));     // "ff"
System.out.println(Integer.toOctalString(n));   // "377"
```

### 2.6 Wrapper Classes & Autoboxing

Every primitive has a wrapper class in `java.lang` that boxes it into an object. This is needed because **collections only work with objects**, not primitives.

| Primitive | Wrapper | Cache Range |
|-----------|---------|-------------|
| `int` | `Integer` | -128 to 127 |
| `long` | `Long` | -128 to 127 |
| `double` | `Double` | none |
| `float` | `Float` | none |
| `short` | `Short` | -128 to 127 |
| `byte` | `Byte` | -128 to 127 |
| `char` | `Character` | 0 to 127 |
| `boolean` | `Boolean` | true, false |

**Autoboxing** = automatic primitive → wrapper. **Unboxing** = automatic wrapper → primitive. The compiler inserts the conversion for you.

```java
// Autoboxing: compiler rewrites  Integer x = 10;
//                            to  Integer x = Integer.valueOf(10);
Integer x = 10;

// Unboxing: compiler rewrites  int y = x;
//                          to  int y = x.intValue();
int y = x;

// Why this matters for performance:
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) {
    list.add(i);   // autoboxing: creates 1 million Integer objects!
}
// For performance-critical code, use IntStream or primitive arrays instead

// The Integer cache TRAP — a famous Java gotcha:
Integer a = 127;
Integer b = 127;
System.out.println(a == b);    // TRUE  — both point to cached object

Integer c = 128;
Integer d = 128;
System.out.println(c == d);    // FALSE — outside cache range; new objects
System.out.println(c.equals(d)); // TRUE — value equality

// LESSON: ALWAYS use .equals() to compare wrapper objects, never ==
```

**Useful Wrapper Methods:**
```java
Integer.MAX_VALUE          // 2147483647
Integer.MIN_VALUE          // -2147483648
Integer.parseInt("FF", 16) // parse hex string → 255
Integer.bitCount(255)       // number of 1-bits → 8
Integer.reverse(1)          // bit-reverse
Integer.compare(a, b)       // safe comparison (-1, 0, 1)
Integer.sum(a, b)           // same as a+b but usable as method reference
Integer.max(a, b)           // max of two

Double.isNaN(0.0/0.0)      // true (Not a Number)
Double.isInfinite(1.0/0.0) // true
Double.parseDouble("3.14") // 3.14
```

### 2.7 The `var` Keyword — Local Variable Type Inference (Java 10+)

`var` tells the compiler to infer the type from the right-hand side. It is **not** a dynamic type like Python — the type is fixed at compile time, you just don't have to write it.

```java
// Without var — type written twice
ArrayList<Map<String, List<Integer>>> data = new ArrayList<Map<String, List<Integer>>>();

// With var — DRY (Don't Repeat Yourself)
var data = new ArrayList<Map<String, List<Integer>>>();  // type inferred

var name  = "Alice";         // inferred: String
var count = 42;              // inferred: int
var list  = new ArrayList<String>();  // inferred: ArrayList<String>

// var in enhanced for loop
for (var entry : map.entrySet()) {   // inferred: Map.Entry<K,V>
    System.out.println(entry.getKey() + "=" + entry.getValue());
}

// Restrictions — var does NOT work in these cases:
var x;              // ❌ no initializer — type cannot be inferred
var y = null;       // ❌ null has no type
var z = {1, 2, 3}; // ❌ array initialiser without type

class Foo {
    var field = 5;  // ❌ cannot use var for class fields
    public var method() { }  // ❌ cannot use var as return type
    public void param(var x) { }  // ❌ cannot use var as parameter
}
```

---

## Chapter 3: Operators & Expressions

### 3.1 Arithmetic Operators

```java
int a = 17, b = 5;

System.out.println(a + b);   // 22  — addition
System.out.println(a - b);   // 12  — subtraction
System.out.println(a * b);   // 85  — multiplication
System.out.println(a / b);   // 3   — INTEGER division: truncates toward zero
System.out.println(a % b);   // 2   — modulo (remainder): 17 = 3×5 + 2

// Integer division truncates — does NOT round
System.out.println(7  / 2);   //  3 (not 3.5)
System.out.println(-7 / 2);   // -3 (not -4 — truncation toward zero)
System.out.println(7  % 2);   //  1
System.out.println(-7 % 2);   // -1 (sign follows dividend in Java)

// Force floating-point division
System.out.println(7.0 / 2);         // 3.5
System.out.println((double) 7 / 2);  // 3.5 — cast one operand

// Overflow — silently wraps around (no exception!)
int max = Integer.MAX_VALUE;  // 2147483647
System.out.println(max + 1);  // -2147483648 ← overflow!
// Use long or Math.addExact() for overflow detection:
Math.addExact(max, 1);  // throws ArithmeticException: integer overflow
```

**Increment & Decrement:**
```java
int x = 5;

// Post-increment: USE the current value, THEN increment
int y = x++;     // y = 5, then x becomes 6
System.out.println(x + ", " + y);  // 6, 5

// Pre-increment: INCREMENT first, THEN use the new value
int z = ++x;     // x becomes 7, then z = 7
System.out.println(x + ", " + z);  // 7, 7

// Common mistake in loops:
for (int i = 0; i < 5; i++) { }   // i++ and ++i behave the same here
// because the incremented value is discarded; prefer i++ by convention
```

### 3.2 Comparison & Logical Operators

```java
// Comparison — always produce a boolean
int a = 5, b = 10;
a == b    // false — equal to
a != b    // true  — not equal to
a <  b    // true  — less than
a >  b    // false — greater than
a <= b    // true  — less than or equal
a >= b    // false — greater than or equal

// CRITICAL: == on objects compares REFERENCES (addresses), not content!
String s1 = new String("hello");
String s2 = new String("hello");
System.out.println(s1 == s2);       // false — different objects
System.out.println(s1.equals(s2));  // true  — same content

// Logical operators
boolean t = true, f = false;
t && f   // false — AND: true only if BOTH true
t || f   // true  — OR:  true if AT LEAST ONE true
!t       // false — NOT: flips the boolean

// Short-circuit evaluation — critically important!
// &&: if left side is FALSE, right side is NEVER evaluated
// ||: if left side is TRUE, right side is NEVER evaluated
String s = null;
if (s != null && s.length() > 0) {  // safe — s.length() only called if s != null
    System.out.println("Not empty");
}
// Without short-circuit, s.length() on null = NullPointerException

// Bitwise logical operators — no short-circuit; operate on individual bits
5 & 3    // 1:   0101 & 0011 = 0001
5 | 3    // 7:   0101 | 0011 = 0111
5 ^ 3    // 6:   0101 ^ 0011 = 0110  (XOR: different bits = 1)
~5       // -6:  NOT 0101 = 1111...11111010 (two's complement)

// Bit shifts
5  << 1   // 10:  shift left  1 = multiply by 2
20 >> 2   // 5:   shift right 2 = divide by 4 (arithmetic: preserves sign bit)
-1 >>> 1  // 2147483647: logical right shift — fills with 0, not sign bit
```

### 3.3 Assignment & Compound Assignment

```java
int x = 10;
x += 5;    // x = x + 5  = 15
x -= 3;    // x = x - 3  = 12
x *= 2;    // x = x * 2  = 24
x /= 4;    // x = x / 4  = 6
x %= 4;    // x = x % 4  = 2

// Compound assignment with bitwise
x &= 3;    // x = x & 3
x |= 8;    // x = x | 8
x ^= 1;    // x = x ^ 1  (toggles last bit)
x <<= 2;   // x = x << 2 (multiply by 4)
x >>= 1;   // x = x >> 1 (divide by 2)

// Subtle type narrowing in compound assignment:
byte b = 10;
b = b + 1;   // ❌ COMPILE ERROR: 'b + 1' promotes to int; can't assign int to byte
b += 1;      // ✅ compound assignment includes implicit narrowing cast
b = (byte)(b + 1);  // ✅ explicit cast also works
```

### 3.4 Ternary Operator

The ternary operator `? :` is a compact `if-else` for producing a value. It is an **expression** (has a value), not a statement.

```java
// Syntax: condition ? valueIfTrue : valueIfFalse
int age = 20;
String status = (age >= 18) ? "adult" : "minor";   // "adult"

// Use for simple value selection — keep it readable
int abs = (x >= 0) ? x : -x;    // absolute value

// Can be nested, but DON'T — it hurts readability
String grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
// Better as if-else

// Ternary is useful in log statements to avoid computing expensive values:
logger.debug("User: " + (user != null ? user.getName() : "null"));
```

### 3.5 `instanceof` Operator

```java
Object obj = "Hello World";

// Traditional instanceof — check then cast (2 steps)
if (obj instanceof String) {           // checks runtime type
    String s = (String) obj;           // explicit cast
    System.out.println(s.length());    // 11
}

// Pattern matching instanceof (Java 16+) — check AND cast in one step
if (obj instanceof String s) {         // if obj is String, bind to 's'
    System.out.println(s.length());    // 's' is directly usable
}

// With guard condition (Java 16+)
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);  // "Long string: Hello World"
}

// Returns false for null
Object o = null;
System.out.println(o instanceof String);  // false (no NullPointerException)
```

### 3.6 Operator Precedence

When an expression has multiple operators, Java evaluates them in a defined order:

```
Highest precedence (evaluated first)
  [] . ()             array access, member access, method call
  ++ -- ~ ! (cast)    unary operators (right-to-left)
  * / %               multiplicative
  + -                 additive
  << >> >>>           shift
  < > <= >= instanceof  relational
  == !=               equality
  &                   bitwise AND
  ^                   bitwise XOR
  |                   bitwise OR
  &&                  logical AND
  ||                  logical OR
  ?:                  ternary (right-to-left)
  = += -= ...         assignment (right-to-left)
Lowest precedence (evaluated last)
```

**Practical advice:** Don't memorise this. Use parentheses to make intent clear:
```java
// Confusing:
int result = a + b * c - d / e & f;

// Clear:
int result = ((a + (b * c)) - (d / e)) & f;
```

---

## Chapter 4: Control Flow

### 4.1 if / else if / else

```java
int score = 75;

if (score >= 90) {
    System.out.println("Grade: A");
} else if (score >= 80) {
    System.out.println("Grade: B");
} else if (score >= 70) {
    System.out.println("Grade: C");
} else if (score >= 60) {
    System.out.println("Grade: D");
} else {
    System.out.println("Grade: F");
}
// Exactly ONE branch executes; conditions checked top-to-bottom

// Single-statement bodies can omit braces (but DON'T — it causes bugs):
if (x > 0)
    doThis();    // only this line is in the if
    doThat();    // ALWAYS executes — NOT part of the if!
// Always use braces — the Apple SSL bug and countless others come from missing braces.
```

### 4.2 Switch Statement (Traditional)

Switch tests a single expression against multiple constant values. It works with `int`, `char`, `String` (Java 7+), and `enum`.

```java
int day = 3;

switch (day) {
    case 1:
        System.out.println("Monday");
        break;          // EXIT the switch; without break, execution "falls through"
    case 2:
        System.out.println("Tuesday");
        break;
    case 3:
    case 4:             // fall-through: cases 3 AND 4 share the same body
        System.out.println("Mid-week");
        break;
    case 5:
        System.out.println("Friday");
        break;
    default:            // optional; executes if no case matched
        System.out.println("Weekend");
}

// Fall-through can be intentional or a bug — always comment intentional fall-through:
switch (command) {
    case "quit":
    case "exit":
    case "bye":        // intentional fall-through — all mean the same
        shutdown();
        break;
}
```

**Switch with String:**
```java
String color = "red";
switch (color) {         // uses .equals() for comparison, null-safe only if not null
    case "red":   System.out.println("#FF0000"); break;
    case "green": System.out.println("#00FF00"); break;
    default:      System.out.println("Unknown");
}
// WARNING: NullPointerException if color == null
```

### 4.3 Switch Expressions (Java 14+)

Switch expressions produce a **value** and use arrow syntax that eliminates fall-through and `break`.

```java
// Arrow switch expression — concise, no fall-through, no break needed
int day = 3;
String dayName = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3 -> "Wednesday";
    case 4 -> "Thursday";
    case 5 -> "Friday";
    case 6, 7 -> "Weekend";        // multiple labels on one case
    default -> throw new IllegalArgumentException("Invalid day: " + day);
};

// Multi-statement case with yield
String category = switch (score) {
    case 10 -> "Perfect";
    default -> {
        String base = score >= 5 ? "Pass" : "Fail";
        yield base + " (" + score + "/10)";  // yield returns the value from the block
    }
};

// Switch with enums — compiler ensures exhaustiveness
Day d = Day.MONDAY;
int numLetters = switch (d) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
};  // no default needed — all enum values covered
```

### 4.4 Loops — The Full Picture

**for loop** — best when you know the iteration count in advance:
```java
// Standard for
for (int i = 0; i < 5; i++) {
    System.out.print(i + " ");  // 0 1 2 3 4
}
// initialization; condition; update — all optional:
for (;;) { }  // infinite loop

// Multiple variables in for
for (int i = 0, j = 10; i < j; i++, j--) {
    System.out.println(i + " " + j);  // 0 10, 1 9, 2 8, 3 7, 4 6
}
```

**while loop** — best when you don't know the count; checks condition BEFORE first iteration:
```java
Scanner sc = new Scanner(System.in);
String input;
while (!(input = sc.nextLine()).equals("quit")) {
    process(input);
}
// Condition may be false immediately → body may never execute
```

**do-while loop** — body executes AT LEAST ONCE; checks condition AFTER first iteration:
```java
// Perfect for: "ask for input, validate, repeat if invalid"
int num;
do {
    System.out.print("Enter a positive number: ");
    num = sc.nextInt();
} while (num <= 0);
// User is guaranteed to enter at least once
```

**Enhanced for (for-each)** — iterates any `Iterable` or array; no index management:
```java
int[] primes = {2, 3, 5, 7, 11};
for (int p : primes) {
    System.out.print(p + " ");  // 2 3 5 7 11
}

List<String> names = List.of("Alice", "Bob", "Carol");
for (String name : names) {
    System.out.println(name);
}

// LIMITATION: can't modify the loop variable to change the original array
for (int p : primes) {
    p = p * 2;  // this only changes the local copy, NOT primes[i]
}
// Use traditional for if you need index access or modification
```

### 4.5 break, continue, and Labels

```java
// break — immediately exits the innermost enclosing loop or switch
for (int i = 0; i < 10; i++) {
    if (i == 5) break;
    System.out.print(i + " ");  // 0 1 2 3 4
}

// continue — skips the rest of the current iteration; jumps to next iteration
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;   // skip even numbers
    System.out.print(i + " ");   // 1 3 5 7 9
}

// Labeled break — breaks out of the labeled (outer) loop, not just the inner one
outer:                                    // label must immediately precede the loop
for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
        if (i == 2 && j == 2) {
            break outer;                  // exits BOTH loops
        }
        System.out.println(i + "," + j);
    }
}

// Labeled continue — continues the labeled loop
outerLoop:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) continue outerLoop;  // skip rest of inner, go to next i
        System.out.println(i + "," + j); // prints (0,0), (1,0), (2,0)
    }
}
```

### 4.6 Choosing the Right Loop

| Scenario | Best Choice |
|----------|------------|
| Known iteration count | `for` |
| Iterate array/collection | `for-each` |
| While condition holds; may not enter | `while` |
| Must execute at least once | `do-while` |
| Need index while iterating collection | `for` with index OR `IntStream.range` |

---

## Chapter 5: Methods & Recursion

### 5.1 Method Anatomy

A method is a named block of code that performs a specific task. It promotes **reuse** (call it many times), **abstraction** (callers don't need to know HOW it works), and **testability** (test each piece independently).

```java
// Complete method anatomy:
//   access modifier      return type   name      parameter list
public               static    double    average(  int[] numbers  ) {
    // Body
    if (numbers.length == 0) {
        throw new IllegalArgumentException("Cannot average empty array");
    }
    double sum = 0;
    for (int n : numbers) {
        sum += n;
    }
    return sum / numbers.length;   // return statement
}
```

- **Access modifier** (`public`, `private`, `protected`, package-private): who can call it
- **`static`**: belongs to the class, not an instance (optional)
- **Return type**: the type of value returned; `void` if nothing is returned
- **Method name**: camelCase by convention
- **Parameters**: input data; a method signature is the name + parameter types
- **`return`**: exits the method and optionally provides a value; void methods can use bare `return;`

### 5.2 Method Overloading

The same method name with different parameter lists. The compiler picks the right one at compile time based on the argument types (this is **compile-time polymorphism**).

```java
public class Printer {
    // Method overloading — same name, different parameters
    public void print(int n)    { System.out.println("int: " + n); }
    public void print(double d) { System.out.println("double: " + d); }
    public void print(String s) { System.out.println("String: " + s); }
    public void print(int a, int b) { System.out.println("two ints: " + a + ", " + b); }

    // Return type alone does NOT distinguish overloads — compile error:
    // public double print(int n) { }  ❌
}

Printer p = new Printer();
p.print(5);          // calls print(int)
p.print(3.14);       // calls print(double)
p.print("Hello");    // calls print(String)
p.print(1, 2);       // calls print(int, int)
```

**Widening in method calls:** if no exact match, Java widens:
```java
p.print('A');    // char widens to int → calls print(int): "int: 65"
```

### 5.3 Pass by Value — Java's Only Mechanism

Java is **strictly pass-by-value**. Always. There is no pass-by-reference in Java.

**For primitives:** the value is copied. The original cannot be changed by the method.
```java
void doubleIt(int x) {
    x = x * 2;   // modifies only the local copy
}
int a = 5;
doubleIt(a);
System.out.println(a);   // still 5 — a is unchanged
```

**For reference types:** the **reference (address)** is copied. Both the original variable and the parameter point to the **same object**. The method CAN modify the object's state through its copy of the reference, but CANNOT make the original variable point to a different object.

```java
void addName(List<String> list, String name) {
    list.add(name);       // modifies the SAME list object — caller sees this
    list = new ArrayList<>(); // changes local copy of reference — caller's 'list' unchanged
}

List<String> names = new ArrayList<>();
names.add("Alice");
addName(names, "Bob");
System.out.println(names);  // [Alice, Bob] — the add was visible
// 'names' still points to original list, not the new ArrayList created in method
```

### 5.4 Varargs (Variable-Length Arguments)

```java
// Varargs: 'int... nums' — caller can pass 0 or more ints
public int sum(int... nums) {
    int total = 0;
    for (int n : nums) total += n;  // nums is just an int[] internally
    return total;
}

sum();             // 0
sum(1);            // 1
sum(1, 2, 3);      // 6
sum(new int[]{1, 2, 3});  // can also pass an array

// Rules:
// 1. Varargs parameter must be LAST in the parameter list
// 2. Only ONE varargs parameter per method
public void log(String level, String... messages) { ... }  // ✅
// public void bad(int... a, String... b) { }  ❌
```

### 5.5 Recursion

Recursion is when a method calls itself. Every recursive solution has:
1. **Base case**: the simplest input that can be answered directly (no more recursion)
2. **Recursive case**: break the problem into a smaller version of itself + base case

```java
// Factorial: n! = n × (n-1)!
// Base case: 0! = 1
public static long factorial(int n) {
    if (n < 0) throw new IllegalArgumentException("Negative");
    if (n == 0) return 1;              // base case
    return n * factorial(n - 1);      // recursive case
}
// factorial(5) = 5 × factorial(4)
//              = 5 × 4 × factorial(3)
//              = 5 × 4 × 3 × factorial(2)
//              = 5 × 4 × 3 × 2 × factorial(1)
//              = 5 × 4 × 3 × 2 × 1 × factorial(0)
//              = 5 × 4 × 3 × 2 × 1 × 1 = 120

// Fibonacci with memoization (avoids exponential time)
private static Map<Integer, Long> memo = new HashMap<>();
public static long fib(int n) {
    if (n <= 1) return n;                   // base cases: fib(0)=0, fib(1)=1
    if (memo.containsKey(n)) return memo.get(n);  // return cached result
    long result = fib(n - 1) + fib(n - 2);
    memo.put(n, result);                    // cache before returning
    return result;
}
```

**Stack overflow from recursion:**
Each method call creates a new stack frame. Too many recursive calls = `StackOverflowError`. Java's default stack depth is ~500-1000 calls.
```java
// This WILL crash for large n:
public static int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);  // 100,000 deep = StackOverflowError
}
// Solution: use iteration or tail recursion (which Java doesn't optimise, so use loops)
public static long sumIterative(int n) {
    long total = 0;
    for (int i = 1; i <= n; i++) total += i;
    return total;  // or: n * (n+1) / 2
}
```

---

## Chapter 6: OOP — Classes, Objects & Encapsulation

### 6.1 Why Object-Oriented Programming?

Before OOP, programs were sequences of procedures operating on global data. As programs grew, this became unmanageable — any procedure could change any data, making bugs hard to find and changes risky.

OOP organises code around **objects** — self-contained units that combine:
- **State** (data/fields): what the object knows
- **Behaviour** (methods): what the object can do

The four pillars — Encapsulation, Inheritance, Polymorphism, Abstraction — are engineering principles that make large codebases manageable, extensible, and testable.

### 6.2 Classes vs Objects — The Blueprint Analogy

A **class** is a blueprint or template. An **object** (instance) is a concrete realisation created from that blueprint.

```
Class: BankAccount              Objects (instances):
  - fields: balance, owner        alice's account: balance=1000, owner="Alice"
  - methods: deposit, withdraw    bob's account:   balance=500,  owner="Bob"
```

```java
// Class definition — the blueprint
public class BankAccount {
    // Instance fields — each object gets its own copy
    private String owner;
    private double balance;

    // Static field — ONE copy shared across ALL BankAccount objects
    private static int totalAccounts = 0;

    // Constructor — called when 'new BankAccount(...)' is used
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;           // 'this' = the object being constructed
        this.balance = initialBalance;
        totalAccounts++;
    }

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
        balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount > balance) return false;  // insufficient funds
        balance -= amount;
        return true;
    }

    public double getBalance() { return balance; }
    public String getOwner()   { return owner; }
    public static int getTotalAccounts() { return totalAccounts; }

    @Override
    public String toString() {
        return String.format("BankAccount[owner=%s, balance=%.2f]", owner, balance);
    }
}

// Creating objects
BankAccount alice = new BankAccount("Alice", 1000.0);  // 'new' allocates heap memory
BankAccount bob   = new BankAccount("Bob",   500.0);

alice.deposit(250.0);
alice.withdraw(100.0);

System.out.println(alice.getBalance());         // 1150.0
System.out.println(BankAccount.getTotalAccounts()); // 2  — static: called on class
System.out.println(alice);                      // BankAccount[owner=Alice, balance=1150.00]
```

### 6.3 Constructors — The Full Picture

```java
public class Person {
    private String name;
    private int age;
    private String email;

    // Default constructor — no parameters
    // If you define ANY constructor, the compiler no longer auto-generates a default one
    public Person() {
        this("Unknown", 0);   // constructor chaining — must be FIRST statement
    }

    // Parameterized constructor
    public Person(String name, int age) {
        this(name, age, null);  // chain to the most specific constructor
    }

    // Most specific constructor — all validation here
    public Person(String name, int age, String email) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("Name required");
        if (age < 0 || age > 150)           throw new IllegalArgumentException("Invalid age");
        this.name  = name;
        this.age   = age;
        this.email = email;
    }

    // Copy constructor — creates a new object with the same values
    public Person(Person other) {
        this(other.name, other.age, other.email);
    }
}

// Constructor overloading in action:
Person p1 = new Person();                         // name="Unknown", age=0
Person p2 = new Person("Alice", 30);              // email=null
Person p3 = new Person("Bob", 25, "bob@ex.com");
Person p4 = new Person(p3);                       // independent copy of p3
```

### 6.4 Encapsulation — Information Hiding

Encapsulation means making fields `private` and controlling access through `public` methods. This is NOT just about getter/setter boilerplate — it's about **protecting invariants** (rules your object must always satisfy).

```java
public class Temperature {
    private double celsius;   // private — can only change through our methods

    public Temperature(double celsius) {
        setCelsius(celsius);  // reuse setter validation in constructor
    }

    public double getCelsius()    { return celsius; }
    public double getFahrenheit() { return celsius * 9.0/5.0 + 32; }
    public double getKelvin()     { return celsius + 273.15; }

    public void setCelsius(double celsius) {
        if (celsius < -273.15) {  // absolute zero — physical law
            throw new IllegalArgumentException("Below absolute zero: " + celsius);
        }
        this.celsius = celsius;
    }

    public void setFahrenheit(double f) {
        setCelsius((f - 32) * 5.0 / 9.0);  // convert then validate
    }
}

// Without encapsulation, users could do:
// temperature.celsius = -999;   // physically impossible — no way to prevent it
// With encapsulation:
Temperature t = new Temperature(25);
// t.celsius = -999;  ❌ compile error — field is private
t.setCelsius(-999);   // ✅ throws IllegalArgumentException — invariant protected
```

**When NOT to make getters/setters:**
Not every field needs both. A `Circle` might have:
- `getRadius()` — yes, reading the radius is useful
- `setRadius(r)` — only if circles can change size
- `getArea()` — computed, no corresponding field
- No setter for `area` — it's derived, setting it directly makes no sense

### 6.5 `this` Keyword — Three Distinct Uses

```java
public class Node {
    private int value;
    private Node next;

    // Use 1: Distinguish field from parameter (same name)
    public Node(int value) {
        this.value = value;   // 'this.value' = field; 'value' = parameter
    }

    // Use 2: Constructor chaining — this() calls another constructor
    //         MUST be the very first statement
    public Node(int value, Node next) {
        this(value);          // calls Node(int value) above
        this.next = next;
    }

    // Use 3: Return current object — enables method chaining (fluent API)
    public Node setNext(Node next) {
        this.next = next;
        return this;   // return reference to self
    }
}

// Method chaining thanks to 'return this'
Node head = new Node(1).setNext(new Node(2).setNext(new Node(3)));
```

### 6.6 Static Members — Class-Level Data and Behaviour

```java
public class IdGenerator {
    // Static field: one copy for the entire class
    private static int lastId = 0;

    // Static constant: public, immutable, shared
    public static final String PREFIX = "ID-";

    // Static method: no 'this'; can only access static members
    public static String generate() {
        return PREFIX + (++lastId);
    }

    // Static initializer block: runs ONCE when class is first loaded by JVM
    static {
        lastId = loadLastIdFromDatabase();   // expensive one-time setup
        System.out.println("IdGenerator initialized with lastId=" + lastId);
    }

    // Instance initializer block: runs BEFORE every constructor call
    {
        System.out.println("New IdGenerator object created");
    }
}

// Usage: no object needed for static methods
String id1 = IdGenerator.generate();  // "ID-1"
String id2 = IdGenerator.generate();  // "ID-2"
```

**Singleton Pattern using static:**
```java
public class ConfigManager {
    // volatile ensures visibility across threads
    private static volatile ConfigManager instance;
    private final Properties config;

    private ConfigManager() {   // private constructor — prevents direct instantiation
        config = loadConfig();
    }

    // Double-checked locking for thread-safe lazy initialization
    public static ConfigManager getInstance() {
        if (instance == null) {                     // first check (no lock)
            synchronized (ConfigManager.class) {
                if (instance == null) {             // second check (with lock)
                    instance = new ConfigManager();
                }
            }
        }
        return instance;
    }

    public String get(String key) { return config.getProperty(key); }
}
```

### 6.7 The Object Class — Root of Everything

Every class in Java implicitly extends `java.lang.Object`. These are the methods you should know how to override:

```java
public class Product implements Comparable<Product> {
    private final String id;
    private final String name;
    private final double price;

    public Product(String id, String name, double price) {
        this.id = id; this.name = name; this.price = price;
    }

    // equals — defines LOGICAL equality
    // Contract: reflexive, symmetric, transitive, consistent, x.equals(null)==false
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                    // same reference: trivially equal
        if (!(o instanceof Product other)) return false;  // null check + type check + cast
        return Objects.equals(id, other.id);           // products equal if same ID
    }

    // hashCode — MUST be overridden when equals is overridden
    // Contract: equal objects MUST have equal hashCodes
    //           (unequal objects SHOULD have different hashCodes for performance)
    @Override
    public int hashCode() {
        return Objects.hash(id);  // use same fields as equals
    }

    // toString — human-readable representation; used by println, log statements, etc.
    @Override
    public String toString() {
        return String.format("Product{id='%s', name='%s', price=%.2f}", id, name, price);
    }

    // compareTo — natural ordering; used by Collections.sort, TreeSet, etc.
    @Override
    public int compareTo(Product other) {
        return Double.compare(this.price, other.price);  // sort by price ascending
    }
}

// Why equals AND hashCode must be consistent:
Product p1 = new Product("A001", "Laptop", 999.99);
Product p2 = new Product("A001", "Laptop", 999.99);

System.out.println(p1.equals(p2));    // true — same id
System.out.println(p1 == p2);         // false — different objects

Set<Product> set = new HashSet<>();
set.add(p1);
System.out.println(set.contains(p2)); // true ONLY if hashCode is overridden correctly
// HashSet uses: hash bucket = hashCode() % buckets; then equals() to confirm
// If hashCode() is not overridden, p1 and p2 land in different buckets → contains() returns false!
```

### 6.8 Inner Classes

```java
public class Outer {
    private int x = 10;

    // 1. STATIC Nested Class
    //    - Declared with 'static'
    //    - Does NOT hold a reference to the Outer instance
    //    - Cannot access Outer's instance fields/methods
    //    - Use when the nested class logically belongs to the outer class
    //      but doesn't need Outer's state (e.g., Builder, entry types)
    static class StaticNested {
        void display() { System.out.println("Static nested"); }
        // System.out.println(x);  ❌ can't access Outer.x — no Outer instance
    }

    // 2. Non-static (Inner) Class
    //    - Implicitly holds a reference to the enclosing Outer instance
    //    - CAN access all of Outer's members (even private)
    //    - Causes a memory leak if inner instance outlives outer — be careful
    class Inner {
        void display() {
            System.out.println("x = " + x);   // accesses Outer.this.x
        }
    }

    void methodWithLocals() {
        int localVar = 42;   // effectively final — captured by local classes/lambdas

        // 3. Local Inner Class — defined inside a method; rarely used
        class Local {
            void run() {
                System.out.println("local: " + localVar);  // captures effectively-final local
            }
        }
        new Local().run();

        // 4. Anonymous Inner Class — unnamed; implement interface or extend class inline
        //    Great for one-off implementations; lambdas are now preferred for single-method interfaces
        Comparator<String> comp = new Comparator<String>() {
            @Override
            public int compare(String a, String b) {
                return a.length() - b.length();   // sort by length
            }
        };
        // With lambda (Java 8+): Comparator<String> comp = (a, b) -> a.length() - b.length();
    }
}

// Instantiation rules:
Outer outer = new Outer();
Outer.StaticNested sn = new Outer.StaticNested();  // no Outer instance needed
Outer.Inner inner = outer.new Inner();              // MUST have an Outer instance
```

---

## Chapter 7: Inheritance & the IS-A Relationship

### 7.1 Why Inheritance Exists

Consider building a zoo management system. You need `Lion`, `Eagle`, `Salmon`. All animals share common properties (name, age) and behaviours (eat, sleep). Without inheritance, you'd copy these into every class. If the `eat()` logic changes, you'd update it in 50 places. That's the problem inheritance solves: **define common behaviour once, specialise in subclasses**.

### 7.2 extends Keyword — How Inheritance Works

```java
// Superclass (parent) — the common base
public class Animal {
    protected String name;   // 'protected': accessible in this class and all subclasses
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age  = age;
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }

    public void sleep() {
        System.out.println(name + " is sleeping.");
    }

    public String describe() {
        return name + " (age " + age + ")";
    }
}

// Subclass (child) — inherits ALL non-private members
public class Dog extends Animal {
    private String breed;

    // Must call a parent constructor as the VERY FIRST thing
    // If you don't, the compiler inserts 'super()' automatically
    // — but only if the parent HAS a no-arg constructor
    public Dog(String name, int age, String breed) {
        super(name, age);      // calls Animal(String, int)
        this.breed = breed;
    }

    // Overrides Animal.eat() — provides specialised behaviour
    @Override
    public void eat() {
        System.out.println(name + " (a dog) gobbles the food!");
        // Can call the parent's version:
        // super.eat();
    }

    // New method only in Dog
    public void bark() {
        System.out.println(name + " says: Woof!");
    }

    @Override
    public String describe() {
        return super.describe() + ", breed=" + breed;  // extend parent's version
    }
}

Dog d = new Dog("Rex", 3, "Labrador");
d.eat();       // calls Dog.eat(): "Rex (a dog) gobbles the food!"
d.sleep();     // inherited from Animal: "Rex is sleeping."
d.bark();      // Dog-specific
System.out.println(d.describe()); // "Rex (age 3), breed=Labrador"
```

**What is inherited:**
- All `public` and `protected` fields and methods
- Package-private fields and methods (if subclass is in the same package)

**What is NOT inherited:**
- `private` fields and methods (exist in object, but invisible to subclass code)
- Constructors (must be explicitly chained via `super()`)

### 7.3 The `super` Keyword

```java
class Vehicle {
    protected String brand;
    protected int speed;

    public Vehicle(String brand) {
        this.brand = brand;
        this.speed = 0;
    }

    public void accelerate(int amount) {
        speed += amount;
        System.out.println(brand + " now at " + speed + " km/h");
    }
}

class ElectricCar extends Vehicle {
    private int batteryPercent;

    public ElectricCar(String brand, int battery) {
        super(brand);          // ① Call parent constructor — MUST be first
        this.batteryPercent = battery;
    }

    @Override
    public void accelerate(int amount) {
        if (batteryPercent < 10) {
            System.out.println("Low battery! Cannot accelerate.");
            return;
        }
        super.accelerate(amount);    // ② Call parent method — run original logic first
        batteryPercent -= 5;         // then add subclass-specific logic
    }

    public void showBrand() {
        System.out.println(super.brand); // ③ Access parent field (rarely needed)
    }
}
```

### 7.4 Inheritance Hierarchies

```java
// Multilevel inheritance: C → B → A
class A { void methodA() { System.out.println("A"); } }
class B extends A { void methodB() { System.out.println("B"); } }
class C extends B { void methodC() { System.out.println("C"); } }

C c = new C();
c.methodA();  // inherited from A (through B)
c.methodB();  // inherited from B
c.methodC();  // defined in C

// Hierarchical: multiple classes extend one parent
class Cat  extends Animal { void meow()  { } }
class Bird extends Animal { void chirp() { } }
class Fish extends Animal { void swim()  { } }
```

**Why Java forbids multiple class inheritance (the Diamond Problem):**
```java
class A { void hello() { print("A"); } }
class B extends A { void hello() { print("B"); } }
class C extends A { void hello() { print("C"); } }
// class D extends B, C { }  ← FORBIDDEN in Java
// If allowed: d.hello() → which version? B's or C's? Ambiguous!
// Java resolves this by allowing multiple INTERFACE inheritance (interfaces have defaults)
```

### 7.5 Method Overriding Rules

```java
class Parent {
    public    Object returnSomething()  { return new Object(); }  // covariant return
    protected void   doStuff()          { }
    public    String format(int n)      { return "Parent: " + n; }
    public final void sealedMethod()    { }  // cannot be overridden
}

class Child extends Parent {
    // ✅ Covariant return type — can return a MORE specific type
    @Override
    public String returnSomething() { return "hello"; }  // String is subtype of Object

    // ✅ Widen access — override can be MORE accessible but not less
    @Override
    public void doStuff() { }   // protected → public is fine

    // ❌ Cannot narrow access:
    // @Override private void doStuff() { }  // compile error

    // ✅ Must have same name and parameters
    @Override
    public String format(int n) { return "Child: " + n; }

    // ❌ Cannot override final:
    // @Override public void sealedMethod() { }  // compile error
}
```

**`@Override` annotation is a best practice — not optional:**
Without it, if you misspell the method name, the compiler thinks you're defining a NEW method rather than overriding. `@Override` makes the compiler verify you're actually overriding something.

### 7.6 `final` Keyword — Three Meanings

```java
// 1. final VARIABLE — value cannot be reassigned after initialization
final int MAX = 100;
// MAX = 200;  ❌ compile error

// For reference types: the REFERENCE is final, not the object itself
final List<String> list = new ArrayList<>();
list.add("Alice");   // ✅ modifying the object is allowed
// list = new ArrayList<>();  ❌ can't make list point to a different object

// 2. final METHOD — cannot be overridden in any subclass
class Base {
    public final void criticalOperation() {
        validate();
        execute();
    }
    protected void validate() { }  // subclasses can override this
    protected void execute()  { }  // and this
}

// 3. final CLASS — cannot be subclassed at all
// String, Integer, and most wrapper classes are final:
// class MyString extends String { }  ❌ compile error
// Why? Security (no one can override String.equals to compromise security checks)
//      and performance (JIT can inline calls without virtual dispatch)
final class ImmutablePoint {
    public final int x, y;
    public ImmutablePoint(int x, int y) { this.x = x; this.y = y; }
    // No setters — truly immutable value object
}
```

---

## Chapter 8: Polymorphism & Dynamic Dispatch

### 8.1 What Polymorphism Means

"Poly" = many, "morph" = forms. Polymorphism allows one interface to be used with many underlying implementations. In practice: you call the same method on different objects and each does the right thing for its type.

Java has two kinds:
- **Compile-time (static)** polymorphism = method overloading (resolved by compiler)
- **Runtime (dynamic)** polymorphism = method overriding + virtual dispatch (resolved at runtime)

### 8.2 Runtime Polymorphism — The Core Mechanism

```java
abstract class Shape {
    abstract double area();
    abstract double perimeter();

    void describe() {
        // This method calls area() and perimeter()
        // At compile time, it doesn't know WHICH implementation will run
        // At runtime, it uses the ACTUAL object type — that's dynamic dispatch
        System.out.printf("%s: area=%.2f, perimeter=%.2f%n",
            getClass().getSimpleName(), area(), perimeter());
    }
}

class Circle extends Shape {
    double radius;
    Circle(double r) { this.radius = r; }
    @Override double area()      { return Math.PI * radius * radius; }
    @Override double perimeter() { return 2 * Math.PI * radius; }
}

class Rectangle extends Shape {
    double w, h;
    Rectangle(double w, double h) { this.w = w; this.h = h; }
    @Override double area()      { return w * h; }
    @Override double perimeter() { return 2 * (w + h); }
}

class Triangle extends Shape {
    double a, b, c;
    Triangle(double a, double b, double c) { this.a = a; this.b = b; this.c = c; }
    @Override double area() {
        double s = (a+b+c)/2;
        return Math.sqrt(s*(s-a)*(s-b)*(s-c));  // Heron's formula
    }
    @Override double perimeter() { return a + b + c; }
}

// Polymorphic array — holds different Shape subtypes
Shape[] shapes = {
    new Circle(5),
    new Rectangle(4, 6),
    new Triangle(3, 4, 5)
};

// The same call 'shape.describe()' does different things for each object
for (Shape shape : shapes) {
    shape.describe();   // dynamic dispatch — calls the right area() and perimeter()
}
// Circle: area=78.54, perimeter=31.42
// Rectangle: area=24.00, perimeter=20.00
// Triangle: area=6.00, perimeter=12.00

// This lets you add new shapes WITHOUT changing any existing code
// Just add a new class extending Shape — Open/Closed Principle
```

### 8.3 Dynamic Method Dispatch (DMD) — Under the Hood

Every class has a **vtable** (virtual method table) — an array of method pointers. When you call a virtual method on a reference, the JVM looks up the vtable of the ACTUAL object (not the reference type):

```
Reference type: Shape        Actual object: Circle
                              Circle.vtable:
Shape ref = new Circle();       area()      → Circle.area()
ref.area(); ───────────────────▶perimeter() → Circle.perimeter()
                              ↑ JVM looks here, not at Shape.vtable
```

```java
Shape s = new Circle(5);
s.area();    // JVM: look at runtime type (Circle), find Circle.area(), call it
             // NOT: look at reference type (Shape) — that would be compile-time binding

// Static methods are NOT polymorphic — no vtable lookup
class Parent { static void staticMethod() { print("Parent"); } }
class Child  extends Parent { static void staticMethod() { print("Child"); } }

Parent ref = new Child();
ref.staticMethod();  // prints "Parent" — static method hiding, not overriding
// Always call static methods on the class name, not a reference
```

### 8.4 Upcasting & Downcasting

```java
// UPCASTING: subclass reference → parent type
// Always safe, always automatic (implicit)
Dog dog = new Dog("Rex", 3, "Lab");
Animal a = dog;    // upcast — no syntax needed
// 'a' now sees Dog as an Animal; Dog-specific methods are hidden
a.eat();    // ✅ — eat() is in Animal (but Dog's version runs due to DMD)
// a.bark();  ❌ compile error — Animal doesn't know about bark()

// DOWNCASTING: parent reference → subclass type
// Potentially unsafe — must verify at runtime
Animal ref = new Dog("Buddy", 2, "Poodle");  // actual type is Dog
Dog d = (Dog) ref;    // explicit downcast — OK because actual object IS a Dog
d.bark();             // ✅ works fine

// DANGER — wrong downcast:
Animal cat = new Cat("Whiskers", 4);
// Dog d2 = (Dog) cat;  // compiles ✅ but throws ClassCastException at runtime ❌

// SAFE PATTERN — always check before downcasting:
if (ref instanceof Dog dogRef) {   // pattern matching: check + cast in one step
    dogRef.bark();                  // safe — we verified the type
}

// Real-world use case: processing a heterogeneous list
List<Animal> zoo = List.of(new Dog("Rex",2,"Lab"), new Cat("Luna",3), new Bird("Tweety",1));
for (Animal a2 : zoo) {
    if (a2 instanceof Dog d2)  d2.bark();
    if (a2 instanceof Cat c)   c.meow();
    if (a2 instanceof Bird b)  b.chirp();
}
```

---

## Chapter 9: Abstraction — Abstract Classes & Interfaces

### 9.1 What Abstraction Means

Abstraction means hiding the WHAT and HOW behind a common contract — users of the abstraction only need to know WHAT it does, not HOW it does it. This is how you write code that can work with future implementations that don't exist yet.

### 9.2 Abstract Classes

An abstract class is a class that CANNOT be instantiated. It serves as a template that provides partial implementation and forces subclasses to fill in the rest.

```java
public abstract class DatabaseRepository<T, ID> {
    // Abstract methods — subclasses MUST implement these
    public abstract T findById(ID id);
    public abstract List<T> findAll();
    public abstract T save(T entity);
    public abstract void delete(ID id);

    // Concrete methods — shared logic subclasses can use as-is
    public boolean exists(ID id) {
        return findById(id) != null;  // reuses abstract findById()
    }

    public List<T> saveAll(List<T> entities) {
        List<T> saved = new ArrayList<>();
        for (T entity : entities) {
            saved.add(save(entity));
        }
        return saved;
    }

    // Template method pattern: define the algorithm skeleton
    // Let subclasses override specific steps
    public final T findOrCreate(ID id, T defaultEntity) {
        T found = findById(id);              // subclass implementation
        if (found == null) {
            return save(defaultEntity);       // subclass implementation
        }
        return found;
    }
}

// Concrete implementation for MySQL
public class MySqlUserRepository extends DatabaseRepository<User, Long> {
    @Override
    public User findById(Long id) {
        // execute: SELECT * FROM users WHERE id = ?
        return executeQuery("SELECT * FROM users WHERE id = ?", id);
    }
    @Override public List<User> findAll() { ... }
    @Override public User save(User user) { ... }
    @Override public void delete(Long id) { ... }
}

// Concrete implementation for MongoDB — completely different HOW, same WHAT
public class MongoUserRepository extends DatabaseRepository<User, String> {
    @Override public User findById(String id) { /* MongoDB query */ }
    // ...
}
```

**When to use abstract classes vs interfaces:**

Abstract class is right when:
- You want to share implementation (not just the contract)
- Subclasses share common state (fields)
- You need constructors
- You have an IS-A relationship with common behaviour

### 9.3 Interfaces — The Contract

An interface defines a pure contract — it says WHAT something must be able to do, with no (or minimal) implementation. The power: a class can implement multiple interfaces, enabling mix-and-match capabilities.

```java
// Basic interface — all methods are public abstract by default
public interface Printable {
    void print();           // implicitly: public abstract void print();
    void printPDF();        // another abstract method
}

public interface Saveable {
    boolean save(String destination);
    boolean load(String source);

    // Default method (Java 8+): provides a default implementation
    // Subclasses can override it or use the default
    default boolean saveWithBackup(String dest) {
        if (save(dest + ".bak")) {     // create backup first
            return save(dest);
        }
        return false;
    }

    // Static method (Java 8+): utility method; not inherited by implementors
    static String getDefaultDestination() { return "./output"; }

    // Private method (Java 9+): helper for default methods; not visible outside
    private void logSaveAttempt(String dest) {
        System.out.println("Attempting to save to: " + dest);
    }

    // Interface constants — implicitly public static final
    int MAX_FILE_SIZE = 10 * 1024 * 1024;  // 10 MB
}

// A class can implement MULTIPLE interfaces
public class Report implements Printable, Saveable {
    private String content;

    public Report(String content) { this.content = content; }

    @Override public void print()    { System.out.println(content); }
    @Override public void printPDF() { /* PDF generation */ }
    @Override public boolean save(String dest) { /* write to file */ return true; }
    @Override public boolean load(String src)  { /* read from file */ return true; }
    // saveWithBackup() is inherited from Saveable — don't need to override
}
```

### 9.4 Abstract Class vs Interface — Decision Guide

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Instantiation | ❌ | ❌ |
| Constructors | ✅ Yes | ❌ No |
| Instance fields | ✅ Any | Only `public static final` constants |
| Method types | Abstract + Concrete | Abstract + Default + Static + Private |
| Multiple inheritance | ❌ Single only | ✅ Implement many |
| `extends`/`implements` | `extends` | `implements` |
| **Use for** | Shared state + common code | Pure behaviour contract |

```java
// Practical example: Abstract class for shared state, interfaces for capabilities
abstract class Vehicle {          // shared state: speed, fuel
    protected int speed;
    protected double fuelLevel;
    public abstract void accelerate();
}

interface Electric  { void chargeBattery(); double getBatteryLevel(); }
interface Autonomous { void enableAutopilot(); void setDestination(String dest); }

// Tesla combines all three:
class TeslaModelS extends Vehicle implements Electric, Autonomous {
    private double batteryLevel;

    @Override public void accelerate()  { speed += 30; batteryLevel -= 0.5; }
    @Override public void chargeBattery() { batteryLevel = 100; }
    @Override public double getBatteryLevel() { return batteryLevel; }
    @Override public void enableAutopilot()  { /* activate */ }
    @Override public void setDestination(String d) { /* navigate */ }
}
```

### 9.5 Enums — Type-Safe Constants

An enum is a special class whose instances are a fixed set of constants. It's much safer than using `int` or `String` constants.

```java
public enum OrderStatus {
    // These are instances of OrderStatus — created when the class loads
    PENDING,
    CONFIRMED,
    PROCESSING,
    SHIPPED,
    DELIVERED,
    CANCELLED;

    // Enums can have methods
    public boolean isFinal() {
        return this == DELIVERED || this == CANCELLED;
    }

    public boolean canTransitionTo(OrderStatus next) {
        return switch (this) {
            case PENDING    -> next == CONFIRMED || next == CANCELLED;
            case CONFIRMED  -> next == PROCESSING || next == CANCELLED;
            case PROCESSING -> next == SHIPPED;
            case SHIPPED    -> next == DELIVERED;
            default         -> false;   // DELIVERED and CANCELLED are terminal
        };
    }
}

// Enums with fields (each constant can have different data)
public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS  (4.869e+24, 6.0518e6),
    EARTH  (5.976e+24, 6.37814e6),
    MARS   (6.421e+23, 3.3972e6);

    private final double mass;    // kg
    private final double radius;  // m
    static final double G = 6.67300E-11;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    public double surfaceGravity() {
        return G * mass / (radius * radius);
    }

    public double surfaceWeight(double otherMass) {
        return otherMass * surfaceGravity();
    }
}

// Usage
OrderStatus status = OrderStatus.PENDING;
System.out.println(status.canTransitionTo(OrderStatus.CONFIRMED));  // true
System.out.println(status.canTransitionTo(OrderStatus.SHIPPED));    // false

for (Planet p : Planet.values()) {
    System.out.printf("Weight on %s: %.2f N%n", p, p.surfaceWeight(75));
}

// Enum utility methods
status.name();        // "PENDING" — string name
status.ordinal();     // 0 — zero-based position
OrderStatus.valueOf("SHIPPED");  // OrderStatus.SHIPPED

// EnumSet and EnumMap — efficient implementations for enums
EnumSet<OrderStatus> activeStatuses = EnumSet.of(
    OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.SHIPPED);
EnumMap<OrderStatus, String> descriptions = new EnumMap<>(OrderStatus.class);
descriptions.put(OrderStatus.PENDING, "Awaiting confirmation");
```

---

## Chapter 10: Strings — Deep Dive

### 10.1 String Immutability — Why and What it Means

`String` in Java is **immutable**: once created, its character sequence can never change. Every operation that seems to "modify" a String actually creates a new String object.

**Why immutability?**
1. **Thread safety**: Multiple threads can share the same String without synchronisation
2. **Caching hashCode**: String caches its hash (computed once, reused) — critical for HashMap performance
3. **Security**: Class names loaded by ClassLoader, file paths, network connections — all Strings. If mutable, malicious code could change them after security checks.
4. **String Pool**: JVM can safely intern and reuse literal Strings because they never change.

```java
String s = "Hello";
s = s + " World";   // Does NOT modify "Hello"
                    // Creates a new String "Hello World"
                    // 's' now points to the new String
                    // "Hello" is still in memory (until GC)

// Proof:
String a = "Hello";
String b = a;         // b points to same "Hello"
a = a + "!";          // a now points to "Hello!"
System.out.println(b); // "Hello" — b still points to original, unchanged
```

### 10.2 String Pool — Memory Optimisation

The JVM maintains a **String Pool** (interning pool) — a special area in the heap (Metaspace since Java 8) where String literals are stored. When you write `"hello"` twice, there's only ONE "hello" object.

```java
// String literals — go into the pool
String s1 = "Java";
String s2 = "Java";
System.out.println(s1 == s2);       // TRUE — same object from pool

// 'new String()' — always creates a new object on the heap, OUTSIDE the pool
String s3 = new String("Java");
System.out.println(s1 == s3);       // FALSE — different objects
System.out.println(s1.equals(s3));  // TRUE — same content

// String.intern() — add to pool (or return existing pool entry)
String s4 = s3.intern();
System.out.println(s1 == s4);       // TRUE — s4 is the pool entry

// GOLDEN RULE: NEVER compare Strings with ==
// Always use .equals() or .equalsIgnoreCase()
```

### 10.3 String Methods — Complete Reference

```java
String s = "  Hello, World!  ";

// ── Length & Indexing ──────────────────────────────────────────
s.length()                     // 18  — number of chars
s.charAt(7)                    // 'W' — char at index
s.codePointAt(7)               // 87  — Unicode code point
s.indexOf("World")             // 9   — first occurrence (-1 if not found)
s.indexOf("l")                 // 5   — first 'l'
s.lastIndexOf("l")             // 14  — last occurrence
s.indexOf("l", 6)              // 11  — first 'l' at or after index 6

// ── Substring ─────────────────────────────────────────────────
s.substring(7)                 // "World!  " — from index 7 to end
s.substring(7, 12)             // "World"    — [7, 12) — end is EXCLUSIVE
// Pitfall: substring on large strings in old Java (pre-7u6) kept original char array
// — potential memory leak; current Java copies the chars

// ── Searching & Testing ───────────────────────────────────────
s.contains("World")            // true
s.startsWith("  Hello")        // true
s.endsWith("!  ")              // true
s.isEmpty()                    // false (length == 0)
s.isBlank()                    // false (Java 11: only whitespace / length 0)
"   ".isBlank()                // true
s.matches(".*World.*")         // true — full regex match

// ── Transformation ────────────────────────────────────────────
s.trim()                       // "Hello, World!" — removes ASCII whitespace at ends
s.strip()                      // "Hello, World!" — Unicode whitespace aware (Java 11)
s.stripLeading()               // "Hello, World!  " — only leading
s.stripTrailing()              // "  Hello, World!" — only trailing
s.toUpperCase()                // "  HELLO, WORLD!  "
s.toLowerCase()                // "  hello, world!  "
s.replace('l', 'r')            // "  Herro, Worrd!  " — char replacement
s.replace("World", "Java")     // "  Hello, Java!  "  — substring replacement
s.replaceAll("\\s+", " ")      // replaces all whitespace runs with single space
s.replaceFirst("\\s+", "_")    // replaces only first match

// ── Splitting & Joining ───────────────────────────────────────
"a,b,,c".split(",")            // ["a", "b", "", "c"]
"a,b,,c".split(",", -1)        // ["a", "b", "", "c"] — keep trailing empties
"a,b,,c".split(",", 2)         // ["a", "b,,c"]       — max 2 parts
String.join("-", "a", "b", "c")    // "a-b-c"
String.join(", ", List.of("x","y"))// "x, y"

// ── Conversion ────────────────────────────────────────────────
String.valueOf(42)             // "42" — int to String
String.valueOf(3.14)           // "3.14"
String.valueOf(true)           // "true"
String.format("%.2f", 3.14159) // "3.14"
"%d items @ $%.2f".formatted(5, 9.99)  // "5 items @ $9.99" (Java 15)

// ── Comparison ────────────────────────────────────────────────
"abc".equals("abc")            // true
"abc".equalsIgnoreCase("ABC")  // true
"abc".compareTo("abd")         // negative (c < d)
"abc".compareToIgnoreCase("ABC") // 0

// ── Char Array ────────────────────────────────────────────────
char[] chars = "hello".toCharArray();  // ['h','e','l','l','o']
new String(chars)                      // "hello"
new String(chars, 1, 3)                // "ell" (offset=1, count=3)

// ── Modern String Methods (Java 11-12+) ───────────────────────
"line1\nline2\nline3".lines()           // Stream<String> of lines
"ab".repeat(3)                          // "ababab"
"  hi  ".strip().isBlank()             // false
```

### 10.4 StringBuilder — When to Use It

Every `+` on Strings creates a new object. In a loop, this is O(n²) — terrible performance.

```java
// ❌ O(n²) — creates n intermediate String objects
String result = "";
for (int i = 0; i < 10000; i++) {
    result += i + ",";    // each += creates and discards a new String
}

// ✅ O(n) — one buffer, all modifications in-place
StringBuilder sb = new StringBuilder(50000);  // pre-size to avoid resizing
for (int i = 0; i < 10000; i++) {
    sb.append(i).append(',');  // method chaining — append returns 'this'
}
String result2 = sb.toString();

// StringBuilder API
StringBuilder sb2 = new StringBuilder("Hello");
sb2.append(" World");           // "Hello World"
sb2.insert(5, ",");             // "Hello, World"
sb2.delete(5, 6);               // "Hello World"
sb2.replace(6, 11, "Java");     // "Hello Java"
sb2.reverse();                  // "avaJ olleH"
sb2.setCharAt(0, 'X');          // "XvaJ olleH"
sb2.deleteCharAt(0);            // "vaJ olleH"
sb2.length();                   // current length
sb2.capacity();                 // current internal buffer size
sb2.ensureCapacity(100);        // guarantee at least 100 chars without resize
```

**StringBuilder vs StringBuffer:**
- `StringBuilder` (Java 5+): NOT thread-safe; faster
- `StringBuffer` (Java 1.0): thread-safe (synchronized); slower
- Use `StringBuilder` in all single-threaded code (nearly always)
- Use `StringBuffer` only if multiple threads share the same buffer (rare)

### 10.5 Text Blocks (Java 15+)

```java
// Old way: escape-heavy, error-prone
String json = "{\n" +
              "    \"name\": \"Alice\",\n" +
              "    \"age\": 30,\n" +
              "    \"active\": true\n" +
              "}";

// Text Block: preserves formatting, no escape required
String json2 = """
        {
            "name": "Alice",
            "age": 30,
            "active": true
        }
        """;
// The indentation common to all lines (8 spaces here) is stripped
// The closing """ determines the base indentation level

// Multiline SQL
String sql = """
        SELECT u.id, u.name, o.total
        FROM users u
        JOIN orders o ON o.user_id = u.id
        WHERE u.active = true
          AND o.total > :minTotal
        ORDER BY o.total DESC
        """;

// With String.formatted() or %s replacement
String html = """
        <html>
          <body>
            <h1>Hello, %s!</h1>
          </body>
        </html>
        """.formatted("World");
```

---

## Chapter 11: Arrays

### 11.1 Arrays — The Foundation of Data Structures

An array is a contiguous block of memory holding a fixed number of elements of the same type. It's the simplest and fastest data structure for random access.

```java
// Declaration and allocation — three equivalent forms
int[] nums = new int[5];        // [0, 0, 0, 0, 0] — default-initialized
int[] primes = {2, 3, 5, 7, 11};  // declaration + initialization shorthand
int[] squares = new int[]{1, 4, 9, 16, 25};  // explicit — useful in expressions

String[] names;          // just declaration — names is null
names = new String[3];   // allocation — ["null", "null", "null"] (reference default)

// Accessing elements — O(1) — direct memory address: base + index × elementSize
System.out.println(primes[0]);     // 2
System.out.println(primes[4]);     // 11
primes[2] = 99;                    // modify

// Length property (NOT a method — no parentheses)
System.out.println(primes.length); // 5  — fixed at creation time

// ArrayIndexOutOfBoundsException: valid indices are [0, length-1]
// primes[5];   ← runtime exception
// primes[-1];  ← runtime exception
```

### 11.2 The Arrays Utility Class

```java
import java.util.Arrays;

int[] a = {5, 3, 1, 4, 2};

// Sorting — uses Dual-Pivot Quicksort for primitives (O(n log n) average)
Arrays.sort(a);                          // a is now {1, 2, 3, 4, 5}
Arrays.sort(a, 1, 4);                    // sort only indices [1, 4)

String[] words = {"banana", "apple", "cherry"};
Arrays.sort(words);                      // {"apple", "banana", "cherry"}
Arrays.sort(words, Comparator.comparingInt(String::length));  // by length

// Binary search (requires sorted array!)
int idx = Arrays.binarySearch(a, 3);     // returns index of 3 (which is 2)
// Returns negative: -(insertion point) - 1 if not found

// Comparison
int[] b = {1, 2, 3, 4, 5};
System.out.println(Arrays.equals(a, b));      // true  — element-wise comparison
System.out.println(a == b);                   // false — reference comparison

int[][] m1 = {{1,2},{3,4}};
int[][] m2 = {{1,2},{3,4}};
System.out.println(Arrays.deepEquals(m1, m2)); // true — recursive comparison

// Filling
Arrays.fill(a, 0);                       // {0, 0, 0, 0, 0}
Arrays.fill(a, 1, 4, 9);                // {0, 9, 9, 9, 0} — fill range [1,4)

// Copying
int[] copy1 = Arrays.copyOf(a, a.length);      // exact copy
int[] copy2 = Arrays.copyOf(a, 8);             // longer — padded with 0s
int[] copy3 = Arrays.copyOf(a, 3);             // shorter — truncated
int[] copy4 = Arrays.copyOfRange(a, 1, 4);     // [1, 4) — indices 1,2,3

System.arraycopy(a, 0, copy1, 0, a.length);    // fast native copy

// String representation
System.out.println(Arrays.toString(a));         // "[1, 2, 3, 4, 5]"
System.out.println(Arrays.deepToString(m1));    // "[[1, 2], [3, 4]]"

// Stream conversion
int sum = Arrays.stream(a).sum();
int max = Arrays.stream(a).max().getAsInt();
Arrays.stream(words).filter(w -> w.length() > 5).forEach(System.out::println);

// Parallel sorting (for very large arrays, uses multiple threads)
Arrays.parallelSort(a);
```

### 11.3 Multi-dimensional Arrays

Java doesn't have true multi-dimensional arrays — it has arrays OF arrays. This makes them flexible (jagged) but slightly different from C.

```java
// 2D array — rectangular
int[][] matrix = new int[3][4];   // 3 rows, 4 columns
int[][] grid = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Access: [row][column]
System.out.println(grid[1][2]);  // 6 (row 1, col 2)

// Iterate 2D
for (int row = 0; row < grid.length; row++) {
    for (int col = 0; col < grid[row].length; col++) {
        System.out.printf("%3d", grid[row][col]);
    }
    System.out.println();
}

// Memory layout — grid is an array of row-arrays:
// grid → [ref0] [ref1] [ref2]
//          ↓       ↓       ↓
//        [1,2,3] [4,5,6] [7,8,9]

// Jagged array — rows have different lengths
int[][] triangle = new int[5][];
for (int i = 0; i < 5; i++) {
    triangle[i] = new int[i + 1];   // row 0 has 1 element, row 4 has 5
    Arrays.fill(triangle[i], i + 1);
}
// triangle[0] = {1}
// triangle[1] = {2, 2}
// triangle[2] = {3, 3, 3}

// 3D array
int[][][] cube = new int[3][3][3];
cube[0][1][2] = 42;

System.out.println(Arrays.deepToString(grid));  // "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
```

### 11.4 Arrays of Objects & Enhanced Sorting

```java
// Array of objects
Person[] people = {
    new Person("Charlie", 30),
    new Person("Alice", 25),
    new Person("Bob", 35)
};

// Sort with Comparator
Arrays.sort(people, (p1, p2) -> p1.getName().compareTo(p2.getName()));
// people is now: [Alice, Bob, Charlie]

// Method reference
Arrays.sort(people, Comparator.comparing(Person::getName));

// Chained comparators: primary by age, secondary by name
Arrays.sort(people, Comparator.comparingInt(Person::getAge)
                               .thenComparing(Person::getName));

// Reverse sort
Arrays.sort(people, Comparator.comparing(Person::getName).reversed());
```

### 11.5 Why Arrays Aren't Enough — The Bridge to Collections

Arrays have fundamental limitations that led to the Collections Framework:

| Limitation | Problem | Solution in Collections |
|-----------|---------|------------------------|
| Fixed size | Can't grow or shrink | `ArrayList`, `LinkedList` dynamically resize |
| No insert/delete | Shifting elements is O(n) manual work | `List.add(index)`, `List.remove()` handle it |
| No search method | Must write your own | `List.contains()`, `Map.get()` |
| Primitives only efficiently | Boxing required for generics | `IntStream`, specialised collections |
| No key-based access | Must iterate to find | `Map<K,V>` provides O(1) key lookup |
| Not type-safe without generics | `Object[]` accepts anything | `List<String>` rejects wrong types |

---

## Chapter 12: Collections Framework

### 12.1 The Framework Architecture

The Collections Framework is a unified architecture for storing and manipulating groups of objects. Understanding the hierarchy lets you choose the right data structure for every problem.

```
java.lang.Iterable
└── java.util.Collection
    ├── List          — ordered, indexed, allows duplicates
    │   ├── ArrayList     O(1) random access; O(n) insert/delete middle
    │   ├── LinkedList    O(n) access; O(1) insert/delete at ends
    │   └── Vector        like ArrayList but synchronized (legacy)
    │       └── Stack     push/pop stack (legacy; use ArrayDeque)
    ├── Set           — no duplicates; may or may not be ordered
    │   ├── HashSet       O(1) add/remove/contains; no order guarantee
    │   ├── LinkedHashSet O(1) operations; maintains insertion order
    │   └── TreeSet       O(log n); sorted natural or custom order
    └── Queue         — ordering for processing
        ├── PriorityQueue  natural/custom priority, not FIFO
        ├── ArrayDeque     fast; use as stack or queue
        └── LinkedList     also implements Deque

java.util.Map             — key-value pairs; keys unique
├── HashMap               O(1) average; no ordering
├── LinkedHashMap         O(1); maintains insertion order
├── TreeMap               O(log n); sorted by keys
├── Hashtable             synchronized HashMap (legacy)
└── ConcurrentHashMap     thread-safe; fine-grained locking
```

### 12.2 ArrayList — The Workhorse

```java
// ArrayList backed by an Object[] that doubles in size when full
// Initial capacity: 10; grows to 15, 22, 33, ... when exceeded
List<String> list = new ArrayList<>();          // starts at default capacity 10
List<String> list2 = new ArrayList<>(100);      // pre-size to avoid 3 resizes for 100 items
List<String> list3 = new ArrayList<>(existingCollection); // copy constructor

// ── Adding ────────────────────────────────────────────────────
list.add("Apple");                 // O(1) amortized — appends to end
list.add("Banana");
list.add("Cherry");
list.add(1, "Blueberry");          // O(n) — inserts at index 1, shifts others right
list.addAll(List.of("Date","Fig")); // append another collection

// ── Accessing ─────────────────────────────────────────────────
String first = list.get(0);        // O(1) — direct array access
int size = list.size();             // number of elements
boolean empty = list.isEmpty();
boolean has = list.contains("Apple");  // O(n) — scans linearly
int idx = list.indexOf("Apple");       // O(n) — first occurrence (-1 if absent)
int lastIdx = list.lastIndexOf("Apple");

// ── Removing ──────────────────────────────────────────────────
list.remove("Apple");              // O(n) — by value; removes first occurrence
list.remove(0);                    // O(n) — by index; shifts elements left
list.removeIf(s -> s.startsWith("B"));  // removes all matching (Java 8)
list.clear();                      // O(n) — removes all

// ── Modifying ─────────────────────────────────────────────────
list.set(0, "Avocado");            // O(1) — replace at index
list.replaceAll(String::toUpperCase); // replace each element (Java 8)

// ── Iterating ─────────────────────────────────────────────────
for (String s : list)               System.out.println(s);  // for-each (fastest)
list.forEach(System.out::println);                            // forEach with lambda
for (int i = 0; i < list.size(); i++) System.out.println(list.get(i));  // with index

// ListIterator — bidirectional, can modify during iteration
ListIterator<String> it = list.listIterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.isEmpty()) it.remove();   // safe removal during iteration
    it.set(s.toUpperCase());        // replace current element
    it.add("NEW");                  // insert after current
}

// ── Sorting ───────────────────────────────────────────────────
Collections.sort(list);                              // natural order (String: alphabetical)
list.sort(Comparator.naturalOrder());                // same via List.sort
list.sort(Comparator.reverseOrder());                // reverse
list.sort(Comparator.comparingInt(String::length)); // by length

// ── Searching ─────────────────────────────────────────────────
Collections.binarySearch(list, "Cherry");  // O(log n) — list must be sorted first!
// Returns index if found; -(insertion point)-1 if not

// ── Views ─────────────────────────────────────────────────────
List<String> sub = list.subList(1, 3);  // live view of [1,3); changes affect original
List<String> readOnly = Collections.unmodifiableList(list);  // throws on modification
List<String> synced   = Collections.synchronizedList(list);  // thread-safe

// ── Immutable Lists (Java 9+) ─────────────────────────────────
List<String> immutable = List.of("a", "b", "c");   // null not allowed; fixed size
List<String> copy      = List.copyOf(existingList);  // defensive copy
```

### 12.3 LinkedList — When and Why

```java
// LinkedList: doubly-linked; each node stores data + prev + next references
// Use when: frequent insert/delete at ends; implementing stacks/queues
// Avoid when: random access (get(i) is O(n)); memory overhead per element

LinkedList<Integer> ll = new LinkedList<>();

// Deque operations (use as double-ended queue)
ll.addFirst(1);   ll.offerFirst(0);   // add to front: O(1)
ll.addLast(2);    ll.offerLast(3);    // add to back:  O(1)
ll.removeFirst(); ll.pollFirst();     // remove from front: O(1)
ll.removeLast();  ll.pollLast();      // remove from back:  O(1)
ll.peekFirst();   ll.peekLast();      // look without removing

// As a Stack: push = addFirst, pop = removeFirst, peek = peekFirst
ll.push(10); ll.push(20); ll.push(30);
System.out.println(ll.pop());   // 30 — LIFO

// As a Queue: offer = addLast, poll = removeFirst
ll.offer("a"); ll.offer("b");
System.out.println(ll.poll());  // "a" — FIFO
```

### 12.4 HashSet / LinkedHashSet / TreeSet

```java
// HashSet: backed by HashMap; O(1) add/contains/remove; no order; allows ONE null
Set<String> hashSet = new HashSet<>();
hashSet.add("banana"); hashSet.add("apple"); hashSet.add("cherry");
hashSet.add("apple");   // duplicate — silently ignored; set stays size 3
System.out.println(hashSet.contains("apple"));  // true — O(1)
System.out.println(hashSet);  // output order not guaranteed!

// LinkedHashSet: insertion-order maintained; slightly slower than HashSet
Set<String> linked = new LinkedHashSet<>();
linked.add("banana"); linked.add("apple"); linked.add("cherry");
System.out.println(linked);  // [banana, apple, cherry] — insertion order preserved

// TreeSet: sorted order; backed by Red-Black Tree; O(log n) operations; no null
Set<Integer> sorted = new TreeSet<>();
sorted.add(5); sorted.add(1); sorted.add(3); sorted.add(2); sorted.add(4);
System.out.println(sorted);         // [1, 2, 3, 4, 5] — always sorted

// TreeSet with custom comparator
Set<String> byLength = new TreeSet<>(Comparator.comparingInt(String::length)
                                                .thenComparing(Comparator.naturalOrder()));
byLength.add("fig"); byLength.add("apple"); byLength.add("kiwi"); byLength.add("pear");
System.out.println(byLength);  // [fig, kiwi, pear, apple] — by length then alpha

// NavigableSet operations (TreeSet implements NavigableSet)
TreeSet<Integer> ts = new TreeSet<>(Set.of(1, 3, 5, 7, 9));
ts.floor(6)        // 5 — greatest element ≤ 6
ts.ceiling(6)      // 7 — smallest element ≥ 6
ts.lower(5)        // 3 — greatest element < 5
ts.higher(5)       // 7 — smallest element > 5
ts.headSet(5)      // [1, 3] — elements < 5
ts.tailSet(5)      // [5, 7, 9] — elements ≥ 5
ts.subSet(3, 8)    // [3, 5, 7] — elements in [3, 8)
ts.first()         // 1
ts.last()          // 9
ts.pollFirst()     // removes and returns 1
ts.pollLast()      // removes and returns 9

// Set operations — fundamental for data analysis
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3, 4, 5));
Set<Integer> b = new HashSet<>(Set.of(4, 5, 6, 7, 8));

Set<Integer> union        = new HashSet<>(a); union.addAll(b);        // {1..8}
Set<Integer> intersection = new HashSet<>(a); intersection.retainAll(b); // {4,5}
Set<Integer> difference   = new HashSet<>(a); difference.removeAll(b);   // {1,2,3}
boolean subset = a.containsAll(Set.of(1,2));  // true — {1,2} ⊂ a
```

### 12.5 HashMap — The Most Important Map

```java
// HashMap: key-value pairs; keys must be unique; O(1) average get/put/remove
// Internally: array of buckets; hashCode() → bucket; equals() → exact key match
Map<String, Integer> scores = new HashMap<>();

// ── Adding / Updating ─────────────────────────────────────────
scores.put("Alice", 95);        // add or update
scores.put("Bob",   82);
scores.put("Carol", 91);
scores.put("Alice", 98);        // update: replaces 95 with 98

// Put variants — return previous value or null
Integer old = scores.putIfAbsent("Dave", 75);  // only adds if absent; returns null (added) or old
scores.putIfAbsent("Alice", 70);   // Alice already there; returns 98; map unchanged

// ── Getting ───────────────────────────────────────────────────
scores.get("Alice")              // 98
scores.get("Nobody")             // null (not found)
scores.getOrDefault("Nobody", 0) // 0 (default if absent)
scores.containsKey("Bob")        // true
scores.containsValue(82)         // true — O(n) linear scan

// ── Computing (Java 8) — the most powerful Map operations ─────
// compute: update or compute fresh value for a key
scores.compute("Alice", (key, val) -> val == null ? 1 : val + 10);  // Alice: 98 → 108

// computeIfAbsent: only compute if key is missing
Map<String, List<String>> groups = new HashMap<>();
groups.computeIfAbsent("fruits", k -> new ArrayList<>()).add("apple");
groups.computeIfAbsent("fruits", k -> new ArrayList<>()).add("banana");
// groups: {"fruits": ["apple", "banana"]}

// computeIfPresent: only update if key exists
scores.computeIfPresent("Bob", (k, v) -> v + 5);  // Bob: 82 → 87; no-op if absent

// merge: combine existing value with new value
Map<String, Integer> wordCount = new HashMap<>();
for (String word : text.split(" ")) {
    wordCount.merge(word, 1, Integer::sum);  // start with 1, sum if already present
}

// ── Removing ──────────────────────────────────────────────────
scores.remove("Dave");           // remove by key
scores.remove("Bob", 82);        // conditional remove — only if value matches

// ── Iterating ─────────────────────────────────────────────────
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + " → " + entry.getValue());
}
scores.forEach((name, score) -> System.out.println(name + ": " + score));  // cleaner
scores.keySet().forEach(System.out::println);
scores.values().stream().mapToInt(Integer::intValue).sum();  // sum all values

// ── Collections of Maps ───────────────────────────────────────
Map<String, Integer> map = Map.of("a", 1, "b", 2, "c", 3);  // immutable, up to 10 entries
Map<String, Integer> map2 = Map.ofEntries(
    Map.entry("alice", 90), Map.entry("bob", 85));

// ── LinkedHashMap and TreeMap ──────────────────────────────────
// LinkedHashMap: insertion order preserved; useful for LRU cache (accessOrder=true)
Map<String, Integer> ordered = new LinkedHashMap<>();
// LinkedHashMap(capacity, loadFactor, accessOrder=true) → used as LRU cache:
Map<String, String> lruCache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override protected boolean removeEldestEntry(Map.Entry<String,String> eldest) {
        return size() > 100;   // evict oldest when capacity exceeded
    }
};

// TreeMap: keys sorted; O(log n); useful for range queries
TreeMap<String, Integer> tm = new TreeMap<>(scores);
tm.firstKey();               // alphabetically first
tm.lastKey();                // alphabetically last
tm.floorKey("C");            // greatest key ≤ "C"
tm.subMap("A", "C");         // keys in ["A", "C")
tm.headMap("B");             // keys < "B"
tm.tailMap("B");             // keys ≥ "B"
```

### 12.6 Queue, Deque & PriorityQueue

```java
// Queue — FIFO
Queue<String> queue = new ArrayDeque<>();  // ArrayDeque: faster than LinkedList for queues
queue.offer("first");    // add to tail; returns false if capacity exceeded (never for ArrayDeque)
queue.offer("second");
queue.offer("third");
queue.poll();            // "first" — remove and return head; null if empty
queue.peek();            // "second" — return head WITHOUT removing; null if empty
queue.size();            // 2

// PriorityQueue — elements dequeued in PRIORITY order (not insertion order)
// Default: min-heap (smallest first); backed by a heap array
Queue<Integer> minPQ = new PriorityQueue<>();
minPQ.offer(5); minPQ.offer(1); minPQ.offer(3);
System.out.println(minPQ.poll()); // 1 — smallest always comes out first
System.out.println(minPQ.poll()); // 3
System.out.println(minPQ.poll()); // 5

// Max-heap: provide reverse-order comparator
Queue<Integer> maxPQ = new PriorityQueue<>(Comparator.reverseOrder());

// Custom priority
Queue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparingInt(Task::getPriority).reversed()
);

// Deque (Double-Ended Queue) — add/remove from both ends
Deque<String> deque = new ArrayDeque<>();
deque.offerFirst("head");   deque.offerLast("tail");
deque.offerFirst("new head");
// [new head, head, tail]
deque.pollFirst();  // "new head"
deque.pollLast();   // "tail"

// ArrayDeque as Stack (faster than java.util.Stack)
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.push(2); stack.push(3);  // push = addFirst
stack.pop();   // 3 — LIFO
stack.peek();  // 2 — look without removing
```

### 12.7 Comparator & Comparable — Sorting Mastery

```java
// Comparable — "natural ordering" — implemented IN the class
public class Employee implements Comparable<Employee> {
    private String name;
    private double salary;
    private LocalDate hireDate;

    @Override
    public int compareTo(Employee other) {
        // Must return: negative if this < other, 0 if equal, positive if this > other
        return this.name.compareTo(other.name);  // natural order: alphabetical by name
    }
}
// Collections.sort(employees) uses compareTo automatically

// Comparator — "custom ordering" — defined outside the class
// Compose complex orderings using factory methods:
Comparator<Employee> bySalary    = Comparator.comparingDouble(Employee::getSalary);
Comparator<Employee> byName      = Comparator.comparing(Employee::getName);
Comparator<Employee> byHireDate  = Comparator.comparing(Employee::getHireDate);

// Chain: primary sort by salary desc, then by name asc
Comparator<Employee> complex = bySalary.reversed().thenComparing(byName);

// Sort: ArrayList sorts with given comparator
employees.sort(complex);

// TreeSet/TreeMap can take a comparator in constructor
TreeSet<Employee> byHire = new TreeSet<>(byHireDate);

// Null-safe comparators
Comparator<String> nullsFirst = Comparator.nullsFirst(Comparator.naturalOrder());
Comparator<String> nullsLast  = Comparator.nullsLast(Comparator.naturalOrder());
```

---

## Chapter 13: Generics

### 13.1 Why Generics Exist

Before generics (Java 1.4), collections stored `Object`:
```java
List list = new ArrayList();
list.add("hello");
list.add(42);         // no compiler complaint — but mixing types is usually a bug
String s = (String) list.get(1); // ClassCastException at runtime — 42 is not a String
```

Generics move this error to compile time:
```java
List<String> list = new ArrayList<>();
list.add("hello");
// list.add(42);      ❌ compile error — caught immediately
String s = list.get(0);  // no cast needed
```

### 13.2 Generic Classes and Methods

```java
// Generic class — T is a TYPE PARAMETER (placeholder; resolved at compile time)
public class Pair<A, B> {
    private final A first;
    private final B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public A getFirst()  { return first; }
    public B getSecond() { return second; }

    // Generic method — independent type parameter <C>
    public <C> Pair<A, C> withSecond(C newSecond) {
        return new Pair<>(first, newSecond);
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}

Pair<String, Integer> p1 = new Pair<>("Alice", 30);
Pair<String, Double>  p2 = p1.withSecond(99.9);
System.out.println(p1);  // (Alice, 30)
System.out.println(p2);  // (Alice, 99.9)

// Generic method — can be in non-generic class
public static <T extends Comparable<T>> T max(T a, T b, T c) {
    T maxAB = a.compareTo(b) >= 0 ? a : b;
    return maxAB.compareTo(c) >= 0 ? maxAB : c;
}
System.out.println(max(3, 1, 4));        // 4
System.out.println(max("cat","ant","dog")); // "dog"
```

### 13.3 Bounded Type Parameters

```java
// Upper bound: T must be Number or a subclass of Number
public static <T extends Number> double sum(List<T> list) {
    double total = 0;
    for (T item : list) {
        total += item.doubleValue();  // doubleValue() is in Number
    }
    return total;
}
sum(List.of(1, 2, 3));          // 6.0 — Integer extends Number ✅
sum(List.of(1.5, 2.5, 3.0));    // 7.0 — Double extends Number ✅
// sum(List.of("a","b"));       ❌ compile error — String doesn't extend Number

// Multiple bounds: T must extend Animal AND implement Comparable<T>
public <T extends Animal & Comparable<T>> T findSmallest(List<T> animals) {
    return animals.stream().min(Comparator.naturalOrder()).orElseThrow();
}
```

### 13.4 Wildcards — The Most Confusing Part

```java
// ? — the "unknown type" wildcard

// Upper bounded wildcard: ? extends Number
// Meaning: "a List of some type that IS-A Number"
// Can READ elements as Number; CANNOT WRITE (don't know exact type)
public void printNumbers(List<? extends Number> list) {
    for (Number n : list) {          // safe to read as Number
        System.out.println(n);
    }
    // list.add(42);   ❌ can't add — list might be List<Double>, and 42 is Integer
}
printNumbers(new ArrayList<Integer>());  // ✅
printNumbers(new ArrayList<Double>());   // ✅

// Lower bounded wildcard: ? super Integer
// Meaning: "a List of some type that Integer IS-A"
// Can WRITE Integer (or subtypes); cannot read as Integer (might be Object)
public void addNumbers(List<? super Integer> list) {
    list.add(1); list.add(2); list.add(3);  // ✅ safe to add Integer
    // Integer x = list.get(0);  ❌ might be List<Number> or List<Object>
}
addNumbers(new ArrayList<Integer>()); // ✅
addNumbers(new ArrayList<Number>());  // ✅
addNumbers(new ArrayList<Object>());  // ✅

// Unbounded wildcard: ?
// "a List of some unknown type" — only use Object methods
public void print(List<?> list) {
    for (Object o : list) System.out.println(o);
    // list.add("anything");  ❌ can't add even Object — unknown type
}
```

**PECS — Producer Extends Consumer Super (Joshua Bloch's rule):**
- If a parameterized type **produces** (you read from it) → use `extends`
- If it **consumes** (you write to it) → use `super`
- If both → no wildcard (exact type needed)

### 13.5 Type Erasure — Why Some Things Are Impossible

At compile time, generics are checked. At runtime, ALL type parameters are **erased** — replaced with `Object` (or their bound). This is for backward compatibility.

```java
// What you write:            // What the compiler generates:
List<String> list;            List list;
list.get(0);                  (String) list.get(0);   // cast inserted

// Consequences of type erasure:
List<String> ls = new ArrayList<>();
List<Integer> li = new ArrayList<>();
System.out.println(ls.getClass() == li.getClass()); // TRUE — same class at runtime

// Things you CANNOT do:
// new T()                  — can't create instance of type parameter
// new T[]                  — can't create generic array
// T.class                  — no class literal for type parameter
// instanceof List<String>  — can only do instanceof List<?> or instanceof List

// Heap pollution warning: unchecked cast from raw type to generic
@SuppressWarnings("unchecked")
List<String> dangerously = (List<String>) getRawList();  // might fail at runtime
```

---

## Chapter 14: Exception Handling

### 14.1 What is an Exception and Why It Exists

Without exception handling, error handling would contaminate every line of code:
```java
// Without exceptions (C-style error codes)
int result = divide(a, b);
if (result == ERROR_DIVIDE_BY_ZERO) { handle error }
String name = readName(file);
if (name == null) { handle read error }
// ... every call needs error checking; business logic is buried
```

Java exceptions separate the "happy path" from error handling:
```java
try {
    int result = divide(a, b);
    String name = readName(file);
    // ... business logic is clear
} catch (ArithmeticException | IOException e) {
    // error handling in one place
}
```

### 14.2 The Exception Hierarchy in Detail

```
java.lang.Throwable
├── java.lang.Error                     — JVM-level problems; NEVER catch
│   ├── OutOfMemoryError                — heap full; recovery usually impossible
│   ├── StackOverflowError              — infinite recursion
│   ├── VirtualMachineError
│   └── AssertionError
│
└── java.lang.Exception
    │
    ├── RuntimeException (UNCHECKED)    — programming bugs; don't need to declare
    │   ├── NullPointerException        — dereferencing null
    │   ├── ArrayIndexOutOfBoundsException — index outside [0, length)
    │   ├── StringIndexOutOfBoundsException
    │   ├── ClassCastException          — invalid downcast
    │   ├── ArithmeticException         — e.g., / by zero
    │   ├── IllegalArgumentException    — bad method argument
    │   │   └── NumberFormatException   — invalid string-to-number conversion
    │   ├── IllegalStateException       — object in wrong state for this call
    │   ├── UnsupportedOperationException — e.g., immutable list .add()
    │   ├── ConcurrentModificationException — modifying collection during iteration
    │   └── StackOverflowError (also Error)
    │
    └── Checked Exception               — must handle or declare with 'throws'
        ├── IOException
        │   ├── FileNotFoundException
        │   ├── SocketException
        │   └── EOFException
        ├── SQLException
        ├── ParseException
        ├── InterruptedException
        └── CloneNotSupportedException
```

**Checked vs Unchecked — the philosophical difference:**
- **Checked** = exceptional conditions the caller can reasonably recover from (file not found → show error dialog, ask user to choose another file)
- **Unchecked** = programming bugs (null pointer → fix your code; don't catch and hide it)

### 14.3 try-catch-finally — Deep Dive

```java
try {
    // Code that might throw
    riskyOperation();
} catch (SpecificException e) {
    // Handle specific type — most specific FIRST
    System.err.println("Specific error: " + e.getMessage());
    e.printStackTrace();        // prints full stack trace
    logger.error("Failed", e);  // proper logging includes the exception object
} catch (AnotherException | YetAnother e) {
    // Multi-catch (Java 7): handle multiple types the same way
    System.err.println("Multiple types: " + e.getClass().getSimpleName());
    // 'e' is effectively final in multi-catch
} catch (Exception e) {
    // Broad catch — catches anything not caught above
    // Consider: is this hiding bugs? Only catch what you can handle.
    throw new ServiceException("Service failed", e);  // wrap and re-throw
} finally {
    // ALWAYS runs — even if:
    //   - exception was thrown and not caught
    //   - return statement executed in try or catch
    //   - System.exit() called? (No — finally skipped after System.exit())
    cleanup();  // close resources, unlock locks, reset state
}

// What happens when finally has a return statement?
public int tricky() {
    try {
        throw new RuntimeException("problem");
    } finally {
        return 42;   // ← this SUPPRESSES the exception! Don't do this.
    }
}
// Method returns 42; the RuntimeException is silently swallowed — TERRIBLE practice
```

### 14.4 try-with-resources — The Right Way to Handle Resources

Any object implementing `AutoCloseable` (which includes `Closeable`) can be used in try-with-resources. The JVM calls `close()` automatically — even if an exception occurs.

```java
// ❌ Old way — verbose, error-prone (what if close() throws?)
Connection conn = null;
PreparedStatement stmt = null;
ResultSet rs = null;
try {
    conn = dataSource.getConnection();
    stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
    stmt.setLong(1, userId);
    rs = stmt.executeQuery();
    while (rs.next()) { process(rs); }
} catch (SQLException e) {
    logger.error("DB error", e);
} finally {
    try { if (rs   != null) rs.close();   } catch (SQLException e) { /* suppress */ }
    try { if (stmt != null) stmt.close(); } catch (SQLException e) { /* suppress */ }
    try { if (conn != null) conn.close(); } catch (SQLException e) { /* suppress */ }
}

// ✅ try-with-resources — clean, correct, and closed in REVERSE order
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?")) {
    stmt.setLong(1, userId);
    try (ResultSet rs = stmt.executeQuery()) {
        while (rs.next()) { process(rs); }
    }
} catch (SQLException e) {
    logger.error("DB error", e);
}
// stmt closed before conn (reverse declaration order) — automatically handles exceptions

// Suppressed exceptions: if both body AND close() throw, body exception is primary
// close() exceptions are suppressed (retrievable via e.getSuppressed())
```

### 14.5 Creating Meaningful Custom Exceptions

```java
// ✅ Custom checked exception — extend Exception
public class PaymentException extends Exception {
    private final String transactionId;
    private final PaymentErrorCode errorCode;

    public PaymentException(String message, String transactionId,
                            PaymentErrorCode errorCode) {
        super(message);
        this.transactionId = transactionId;
        this.errorCode = errorCode;
    }

    // Chaining: wraps a lower-level cause
    public PaymentException(String message, String transactionId,
                            PaymentErrorCode errorCode, Throwable cause) {
        super(message, cause);
        this.transactionId = transactionId;
        this.errorCode = errorCode;
    }

    public String getTransactionId() { return transactionId; }
    public PaymentErrorCode getErrorCode() { return errorCode; }
}

public enum PaymentErrorCode {
    INSUFFICIENT_FUNDS, CARD_EXPIRED, NETWORK_ERROR, INVALID_CARD
}

// ✅ Custom unchecked exception — extend RuntimeException
public class UserNotFoundException extends RuntimeException {
    private final long userId;

    public UserNotFoundException(long userId) {
        super("User not found: " + userId);
        this.userId = userId;
    }

    public long getUserId() { return userId; }
}

// Usage
public Payment processPayment(String txId, double amount) throws PaymentException {
    if (balance < amount) {
        throw new PaymentException(
            "Insufficient balance for transaction " + txId,
            txId,
            PaymentErrorCode.INSUFFICIENT_FUNDS
        );
    }
    // ...
}

// Exception chaining — always preserve the cause
try {
    DatabaseUtils.executeUpdate(sql, params);
} catch (SQLException e) {
    throw new DataAccessException("Failed to save user: " + user.getId(), e);
    // 'e' is the cause — stack trace shows BOTH exceptions when printed
}
```

---

## Chapter 15: Java I/O & NIO

### 15.1 Streams Architecture

Java I/O uses the **Decorator pattern** — wrap a basic stream in buffering, compression, or encoding layers:

```
InputStream (raw bytes)
  └── FileInputStream (reads from file)
       └── BufferedInputStream (adds buffering: batch reads into memory)
            └── DataInputStream (adds typed read methods: readInt, readDouble)
                 └── ObjectInputStream (adds object deserialization)

Writer (Unicode characters)
  └── FileWriter (writes to file with charset encoding)
       └── BufferedWriter (adds buffering)
            └── PrintWriter (adds print/println convenience)
```

### 15.2 Reading and Writing Files

```java
// ── Reading text file ──────────────────────────────────────────
// Approach 1: Files utility (best for whole file)
String content = Files.readString(Path.of("data.txt"));           // Java 11+
List<String> lines = Files.readAllLines(Path.of("data.txt"));     // all lines at once
Stream<String> lineStream = Files.lines(Path.of("data.txt"));     // lazy stream (close!)

// Approach 2: BufferedReader for large files (streaming, memory-efficient)
try (BufferedReader br = new BufferedReader(new FileReader("data.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        processLine(line);
    }
}

// Approach 3: with explicit charset
try (BufferedReader br = Files.newBufferedReader(Path.of("data.txt"), StandardCharsets.UTF_8)) {
    br.lines().filter(l -> !l.isBlank()).forEach(this::process);
}

// ── Writing text file ──────────────────────────────────────────
// Approach 1: Files utility
Files.writeString(Path.of("out.txt"), "Hello, World!\n");
Files.write(Path.of("out.txt"), List.of("line1", "line2", "line3"));
// Append to file:
Files.writeString(Path.of("log.txt"), "New entry\n",
    StandardOpenOption.CREATE, StandardOpenOption.APPEND);

// Approach 2: BufferedWriter for lots of data
try (BufferedWriter bw = new BufferedWriter(new FileWriter("out.txt"))) {
    bw.write("First line");
    bw.newLine();       // OS-appropriate line separator
    bw.write("Second line");
}

// Approach 3: PrintWriter — convenient printf-style
try (PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("report.txt")))) {
    pw.println("=== Report ===");
    pw.printf("Total: %,d items @ $%.2f each%n", 1000, 9.99);
}
```

### 15.3 Serialization — Persist Objects

```java
// Make class serializable — marker interface; no methods to implement
public class UserSession implements Serializable {
    private static final long serialVersionUID = 1L;  // version control: change when fields change
    private String username;
    private List<String> permissions;
    private transient String token;    // 'transient': not serialized (secrets, connections)
    private transient Connection dbConn; // connections can't be serialized

    // Custom serialization: write specific fields manually
    private void writeObject(ObjectOutputStream oos) throws IOException {
        oos.defaultWriteObject();    // serialize non-transient fields
        oos.writeObject(encryptToken(token)); // manually serialize encrypted version
    }

    private void readObject(ObjectInputStream ois) throws IOException, ClassNotFoundException {
        ois.defaultReadObject();
        this.token = decryptToken((String) ois.readObject());
    }
}

// Serialize to file
try (ObjectOutputStream oos = new ObjectOutputStream(
         new BufferedOutputStream(new FileOutputStream("session.ser")))) {
    oos.writeObject(session);
}

// Deserialize from file
try (ObjectInputStream ois = new ObjectInputStream(
         new BufferedInputStream(new FileInputStream("session.ser")))) {
    UserSession session = (UserSession) ois.readObject();
}
```

### 15.4 NIO — Path and Files

```java
import java.nio.file.*;
import java.nio.file.attribute.*;

// Path — immutable representation of a file system path
Path p = Path.of("src", "main", "resources", "config.yml");  // platform-independent separator
Path abs = p.toAbsolutePath();           // /home/user/project/src/main/resources/config.yml
Path norm = Path.of("a/./b/../c").normalize();  // a/c
Path parent = p.getParent();             // src/main/resources
Path filename = p.getFileName();         // config.yml
Path relative = Path.of("/a/b").relativize(Path.of("/a/b/c/d")); // c/d

// ── File queries ───────────────────────────────────────────────
Files.exists(p)
Files.notExists(p)
Files.isDirectory(p)
Files.isRegularFile(p)
Files.isReadable(p)
Files.isWritable(p)
Files.isHidden(p)
Files.size(p)                            // bytes
Files.getLastModifiedTime(p)

// ── File operations ────────────────────────────────────────────
Files.createFile(p);                     // create empty file (throws if exists)
Files.createDirectories(Path.of("a/b/c")); // create entire path
Files.copy(src, dest, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.COPY_ATTRIBUTES);
Files.move(src, dest, StandardCopyOption.ATOMIC_MOVE);
Files.delete(p);                         // throws NoSuchFileException if not exists
Files.deleteIfExists(p);                 // safe: returns false if not exists

// ── Directory walking ──────────────────────────────────────────
// Walk up to depth 2 — find all .java files
Files.walk(Path.of("src"), 10)           // maxDepth
    .filter(Files::isRegularFile)
    .filter(path -> path.toString().endsWith(".java"))
    .forEach(System.out::println);

// Find with custom matcher
PathMatcher glob = FileSystems.getDefault().getPathMatcher("glob:**/*.{java,kt}");
Files.walk(Path.of("src"))
    .filter(glob::matches)
    .forEach(System.out::println);

// List directory contents (non-recursive)
try (DirectoryStream<Path> ds = Files.newDirectoryStream(Path.of("dir"), "*.log")) {
    for (Path file : ds) System.out.println(file);
}

// ── Watch service ──────────────────────────────────────────────
WatchService watcher = FileSystems.getDefault().newWatchService();
Path dir = Path.of("watched");
dir.register(watcher,
    StandardWatchEventKinds.ENTRY_CREATE,
    StandardWatchEventKinds.ENTRY_MODIFY,
    StandardWatchEventKinds.ENTRY_DELETE);

// Poll for events in a loop
while (true) {
    WatchKey key = watcher.take();  // blocks until event
    for (WatchEvent<?> event : key.pollEvents()) {
        Path changed = (Path) event.context();
        System.out.println(event.kind() + ": " + changed);
    }
    if (!key.reset()) break;  // directory no longer accessible
}
```

---

## Chapter 16: Multithreading & Concurrency

### 16.1 Threads — The Foundation

A **thread** is the smallest unit of execution — an independent path through your program's code. All threads in a JVM share the same heap (objects are visible to all threads) but each has its own **stack** (local variables, method call frames).

**Why multithreading?**
1. **Performance**: Modern CPUs have multiple cores; one thread wastes N-1 cores
2. **Responsiveness**: UI thread stays responsive while background work runs on other threads
3. **I/O efficiency**: While one thread waits for a network response, others can do CPU work

**The catch**: threads sharing mutable state without coordination → **race conditions**, **deadlocks**, **visibility bugs**. Concurrency is hard to get right.

```java
// Creating threads — 3 approaches

// Approach 1: Extend Thread (avoid — you lose the ability to extend another class)
class CounterThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(getName() + ": " + i);
        }
    }
}
new CounterThread().start();  // start() creates OS thread and calls run() on it
// NEVER call run() directly — that just executes on the current thread, no new thread

// Approach 2: Implement Runnable (preferred for simple fire-and-forget)
Runnable task = () -> {
    for (int i = 0; i < 5; i++) {
        System.out.println(Thread.currentThread().getName() + ": " + i);
    }
};
Thread t = new Thread(task, "WorkerThread");
t.setDaemon(true);  // daemon thread: won't prevent JVM shutdown
t.setPriority(Thread.NORM_PRIORITY);  // 1=MIN, 5=NORM, 10=MAX (hint only)
t.start();
t.join();       // current thread WAITS for t to finish
t.join(2000);   // wait at most 2 seconds

// Approach 3: Callable (returns result, can throw checked exceptions)
Callable<Integer> computation = () -> {
    Thread.sleep(1000);  // throws InterruptedException
    return heavyCompute();
};
```

### 16.2 Thread States — The Lifecycle

```
NEW                          ← Thread created but start() not called
 │
 ▼ start()
RUNNABLE                     ← Running on CPU or ready to run
 │
 ├── Object.wait() ──────────▶ WAITING        ← indefinite wait
 ├── Thread.sleep(n) ─────────▶ TIMED_WAITING  ← wait with timeout
 ├── synchronized block ──────▶ BLOCKED        ← waiting for a lock
 │
 ▼ run() returns
TERMINATED
```

```java
Thread t = new Thread(() -> {
    try {
        System.out.println("State: " + Thread.currentThread().getState()); // RUNNABLE
        Thread.sleep(1000);   // → TIMED_WAITING; reachable when timeout expires
    } catch (InterruptedException e) {
        // InterruptedException means another thread called t.interrupt()
        // ALWAYS restore the interrupt flag if you can't handle it here:
        Thread.currentThread().interrupt();
        System.out.println("Thread was interrupted");
    }
});
System.out.println(t.getState());  // NEW
t.start();
System.out.println(t.getState());  // RUNNABLE or TIMED_WAITING
t.join();
System.out.println(t.getState());  // TERMINATED
```

### 16.3 The Race Condition Problem

```java
// WRONG: unsynchronized counter
class UnsafeCounter {
    private int count = 0;

    public void increment() {
        count++;   // NOT atomic! Expands to 3 operations:
                   // 1. READ count from memory → register
                   // 2. ADD 1 in register
                   // 3. WRITE register → memory
                   // Two threads can interleave these 3 steps → lost updates
    }
}

// Demonstrate the bug:
UnsafeCounter c = new UnsafeCounter();
ExecutorService pool = Executors.newFixedThreadPool(10);
for (int i = 0; i < 10_000; i++) {
    pool.submit(c::increment);
}
pool.shutdown();
pool.awaitTermination(5, TimeUnit.SECONDS);
System.out.println(c.count);  // Expected: 10000; Actual: somewhere between 9000-10000
```

### 16.4 Synchronization — Making Operations Atomic

```java
// Fix 1: synchronized method — only one thread at a time can execute
class SafeCounterSync {
    private int count = 0;
    // Acquires the intrinsic lock of 'this' object
    public synchronized void increment() { count++; }
    public synchronized int getCount()   { return count; }
}

// Fix 2: synchronized block — more fine-grained, lock only what's critical
class SafeCounterBlock {
    private int count = 0;
    private final Object lock = new Object();  // dedicated lock object

    public void increment() {
        synchronized (lock) {   // acquires lock of 'lock' object
            count++;
        }
        // long non-critical work can happen outside the synchronized block
    }
}

// Fix 3: AtomicInteger — lock-free, uses CPU CAS (Compare-And-Swap) instructions
import java.util.concurrent.atomic.*;
class SafeCounterAtomic {
    private final AtomicInteger count = new AtomicInteger(0);
    public void increment()    { count.incrementAndGet(); }
    public int getCount()      { return count.get(); }
    public int addAndGet(int n) { return count.addAndGet(n); }
    public boolean compareAndSet(int expect, int update) {
        return count.compareAndSet(expect, update);  // atomic: set to update only if == expect
    }
}

// Deadlock — two threads each wait for a lock the other holds:
// Thread 1: lock A, then try to lock B
// Thread 2: lock B, then try to lock A
// → circular wait; both stuck forever
// Prevention: always acquire locks in the same order (e.g., sort by lock ID)
```

### 16.5 volatile — Visibility Without Atomicity

```java
// The problem: CPU caches can make thread A's writes invisible to thread B
class StopFlagBroken {
    private boolean stopped = false;  // thread B might cache stale value

    public void stop()     { stopped = true; }
    public void run() {
        while (!stopped) { doWork(); }  // thread B may loop forever
    }
}

// volatile: guarantees visibility — writes are immediately flushed to main memory
//           reads always from main memory, not CPU cache
class StopFlagFixed {
    private volatile boolean stopped = false;

    public void stop()     { stopped = true; }
    public void run() {
        while (!stopped) { doWork(); }  // guaranteed to see latest value
    }
}

// volatile does NOT make compound operations atomic!
// volatile int count; count++;  — still a race condition (3 operations, not 1)
// For compound ops: use AtomicInteger, synchronized, or Lock
```

### 16.6 The Executor Framework — Thread Pools

Creating threads is expensive (~1MB stack allocation, OS system call). Thread pools create threads once and reuse them.

```java
import java.util.concurrent.*;

// ── Thread Pool Types ──────────────────────────────────────────
ExecutorService fixed    = Executors.newFixedThreadPool(4);      // exactly 4 threads
ExecutorService single   = Executors.newSingleThreadExecutor();  // 1 thread; serialises tasks
ExecutorService cached   = Executors.newCachedThreadPool();      // grows as needed; idle threads reused
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);

// ── Submitting Work ────────────────────────────────────────────
// Execute: fire and forget (Runnable, no result)
fixed.execute(() -> System.out.println("Task 1"));

// Submit Runnable: returns Future<?> — can check completion
Future<?> f1 = fixed.submit(() -> doWork());
f1.get();   // blocks until done; throws ExecutionException if task threw

// Submit Callable: returns Future<T> — can get result
Future<Integer> f2 = fixed.submit(() -> computeExpensiveValue());
// Do other work here while computation runs...
int result = f2.get(5, TimeUnit.SECONDS);  // block max 5s; throws TimeoutException

// Invoke many: wait for all
List<Callable<String>> tasks = List.of(
    () -> "task1", () -> "task2", () -> "task3"
);
List<Future<String>> futures = fixed.invokeAll(tasks);  // blocks until ALL complete
for (Future<String> future : futures) {
    System.out.println(future.get());
}

// invokeAny: return result of fastest; cancel others
String first = fixed.invokeAny(tasks);  // fastest completes

// ── Scheduled Tasks ────────────────────────────────────────────
// Run once after 5-second delay
scheduled.schedule(() -> System.out.println("Delayed"), 5, TimeUnit.SECONDS);

// Run repeatedly: first at 0s, then every 10s
scheduled.scheduleAtFixedRate(() -> checkHealth(), 0, 10, TimeUnit.SECONDS);

// Run repeatedly: wait 10s AFTER each completion before starting next
scheduled.scheduleWithFixedDelay(() -> processBatch(), 0, 10, TimeUnit.SECONDS);

// ── Proper Shutdown ────────────────────────────────────────────
fixed.shutdown();              // stop accepting new tasks; wait for existing to finish
if (!fixed.awaitTermination(30, TimeUnit.SECONDS)) {
    fixed.shutdownNow();       // interrupt running tasks; return unstarted ones
}
```

### 16.7 CompletableFuture — Asynchronous Pipelines

```java
// CompletableFuture chains async operations without blocking intermediate steps

CompletableFuture<User> userFuture = CompletableFuture
    .supplyAsync(() -> database.findUser(userId))         // runs in ForkJoinPool
    .thenApply(user -> enrichWithProfile(user))           // transform (still async)
    .thenApply(user -> applyBusinessRules(user))
    .exceptionally(ex -> {                                // handle errors in pipeline
        logger.error("User fetch failed", ex);
        return User.anonymous();                          // return fallback
    });

// Non-blocking consumption
userFuture.thenAccept(user -> displayInUI(user));

// Combine two independent async operations
CompletableFuture<Order[]> ordersFuture = CompletableFuture
    .supplyAsync(() -> orderService.findByUser(userId));

CompletableFuture<UserProfile> profileFuture = CompletableFuture
    .supplyAsync(() -> profileService.find(userId));

// Wait for both and combine
CompletableFuture<Dashboard> dashboard = userFuture.thenCombine(
    profileFuture,
    (user, profile) -> new Dashboard(user, profile)
);

// Wait for ALL to complete
CompletableFuture.allOf(ordersFuture, profileFuture, userFuture)
    .thenRun(() -> System.out.println("All loaded"));

// Wait for FIRST to complete
CompletableFuture.anyOf(replica1.fetch(key), replica2.fetch(key))
    .thenApply(result -> (String) result);

// Get result — BLOCKING (defeats the purpose; use only at program boundaries)
String value = future.get();                       // blocks; throws checked exceptions
String value2 = future.join();                     // blocks; throws unchecked
String value3 = future.getNow("default");          // returns default if not done yet
```

### 16.8 ReentrantLock & Advanced Synchronization

```java
import java.util.concurrent.locks.*;

// ReentrantLock — more flexible than synchronized
ReentrantLock lock = new ReentrantLock(true);  // true = fair lock (FIFO)

lock.lock();  // acquire; blocks if held by another thread
try {
    // critical section
    accessSharedResource();
} finally {
    lock.unlock();  // ALWAYS unlock in finally — lock is not auto-released
}

// Try lock — don't block if unavailable
if (lock.tryLock()) {
    try { /* work */ } finally { lock.unlock(); }
} else {
    System.out.println("Resource busy, skipping");
}

// Try with timeout
if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {
    try { /* work */ } finally { lock.unlock(); }
}

// ReadWriteLock — allow concurrent reads, exclusive writes
ReadWriteLock rwLock = new ReentrantReadWriteLock();
// Multiple threads can hold readLock simultaneously
rwLock.readLock().lock();
try { return readData(); } finally { rwLock.readLock().unlock(); }
// Only one thread can hold writeLock; no readLock can be held concurrently
rwLock.writeLock().lock();
try { writeData(value); } finally { rwLock.writeLock().unlock(); }

// Condition variables — finer-grained than wait/notify
Condition notFull  = lock.newCondition();
Condition notEmpty = lock.newCondition();

// Producer:
lock.lock();
try {
    while (queue.isFull()) notFull.await();   // release lock, wait for signal
    queue.add(item);
    notEmpty.signal();  // wake up one consumer
} finally { lock.unlock(); }

// Consumer:
lock.lock();
try {
    while (queue.isEmpty()) notEmpty.await();
    Item item = queue.remove();
    notFull.signal();
} finally { lock.unlock(); }
```

---

## Chapter 17: Functional Programming — Lambdas & Streams

### 17.1 Functional Interfaces — The Foundation

A **functional interface** has exactly one abstract method. It can be instantiated with a lambda expression. Java 8+ ships many in `java.util.function`.

```java
// The four fundamental types:

// 1. Predicate<T> — T → boolean (test/filter)
Predicate<String> isLong    = s -> s.length() > 5;
Predicate<String> startsA   = s -> s.startsWith("A");
Predicate<String> combined  = isLong.and(startsA);   // AND
Predicate<String> either    = isLong.or(startsA);    // OR
Predicate<String> notLong   = isLong.negate();       // NOT
Predicate<Object> notNull   = Predicate.not(Objects::isNull); // Java 11

isLong.test("Hello World");  // true

// 2. Function<T, R> — T → R (transform)
Function<String, Integer> strLen  = String::length;
Function<Integer, String> intStr  = Object::toString;
Function<String, String>  composed = strLen.andThen(intStr);  // String → Integer → String
// or compose (applies argument first, then this):
Function<String, String> composed2 = intStr.compose(strLen);  // same result

strLen.apply("Hello");  // 5

// 3. Consumer<T> — T → void (side effect)
Consumer<String> print      = System.out::println;
Consumer<String> printUpper = s -> System.out.println(s.toUpperCase());
Consumer<String> both       = print.andThen(printUpper);

both.accept("hello");  // prints "hello", then "HELLO"

// 4. Supplier<T> — () → T (produce a value)
Supplier<List<String>> listFactory = ArrayList::new;
Supplier<LocalDateTime> now        = LocalDateTime::now;
Supplier<String> greeting          = () -> "Hello, World!";

greeting.get();  // "Hello, World!"

// ── More Specialized Types ─────────────────────────────────────
BiFunction<String, Integer, String> repeat = (s, n) -> s.repeat(n);
repeat.apply("ab", 3);  // "ababab"

UnaryOperator<String> shout     = s -> s.toUpperCase() + "!";  // Function<T,T>
BinaryOperator<Integer> add     = Integer::sum;                 // BiFunction<T,T,T>
BinaryOperator<Integer> maxOf   = Integer::max;

// Primitive specialisations (avoid boxing overhead):
IntPredicate  isEven = n -> n % 2 == 0;
IntFunction<String> intToStr = Integer::toString;
ToIntFunction<String> toLen  = String::length;
IntUnaryOperator  square     = n -> n * n;
IntBinaryOperator multiply   = (a, b) -> a * b;
```

### 17.2 Lambda Expressions — Full Syntax

```java
// Syntax variants:

// 0 parameters:
Runnable r = () -> System.out.println("Hello");

// 1 parameter (parentheses optional):
Consumer<String> c1 = s  -> System.out.println(s);
Consumer<String> c2 = (s) -> System.out.println(s);
Consumer<String> c3 = (String s) -> System.out.println(s);  // explicit type

// 2+ parameters (parentheses required):
Comparator<String> comp = (a, b) -> a.length() - b.length();

// Multi-statement body with braces and explicit return:
Function<Integer, String> classify = n -> {
    if (n < 0) return "negative";
    if (n == 0) return "zero";
    if (n < 10) return "small";
    return "large";
};

// Variable capture — lambda can reference EFFECTIVELY FINAL outer variables
// (variables that could be declared final — never reassigned after initial assignment)
String prefix = ">>>";  // effectively final
Consumer<String> logged = msg -> System.out.println(prefix + " " + msg);
// prefix = "!!!";  ← would make lambda capture invalid — compile error

// 'this' in lambda refers to the ENCLOSING OBJECT (not the lambda itself)
// This is different from anonymous inner classes where 'this' = the anonymous class
class Greeter {
    private String name = "Alice";
    void greet() {
        Runnable r = () -> System.out.println("Hello from " + this.name);  // Greeter.this.name
        r.run();
    }
}
```

### 17.3 Method References — Shorthand for Lambdas

```java
// When a lambda just calls an existing method, use a method reference instead
// They're not faster — just cleaner to read

// 1. Static method reference:  ClassName::staticMethod
// Lambda:    x -> Integer.parseInt(x)
// Reference: Integer::parseInt
Function<String, Integer> parse = Integer::parseInt;
Function<Double, Double>  abs   = Math::abs;

// 2. Instance method of a specific object: instance::method
String greeting = "Hello";
// Lambda:    () -> greeting.toUpperCase()
Supplier<String> upper = greeting::toUpperCase;

// 3. Instance method of an arbitrary object: ClassName::instanceMethod
// Lambda:    (s) -> s.toUpperCase()  (the parameter is the receiver)
Function<String, String> toUpper = String::toUpperCase;
// Lambda:    (s1, s2) -> s1.compareTo(s2)
Comparator<String> comp = String::compareTo;

// 4. Constructor reference: ClassName::new
// Lambda:    () -> new ArrayList<>()
Supplier<ArrayList<String>> factory1 = ArrayList::new;
// Lambda:    (n) -> new int[n]
IntFunction<int[]> arrayFactory = int[]::new;
// Lambda:    (name, age) -> new Person(name, age)
BiFunction<String, Integer, Person> personFactory = Person::new;
```

### 17.4 Stream API — Processing Collections Declaratively

A Stream is a pipeline of operations over a sequence of elements. Three parts:
1. **Source**: where elements come from
2. **Intermediate operations**: lazy transformations (return Stream)
3. **Terminal operation**: triggers execution, produces result

```java
// ── Creating Streams ──────────────────────────────────────────
Stream<String> from_collection = list.stream();
Stream<String> parallel        = list.parallelStream();
Stream<String> of_values       = Stream.of("a", "b", "c");
Stream<String> empty           = Stream.empty();

// Primitive streams — no boxing overhead
IntStream ints       = IntStream.range(1, 11);       // 1..10
IntStream intsInc    = IntStream.rangeClosed(1, 10); // 1..10
LongStream longs     = LongStream.of(1L, 2L, 3L);
DoubleStream doubles = DoubleStream.of(1.1, 2.2);

// Infinite streams
Stream<Integer> naturals = Stream.iterate(1, n -> n + 1);
Stream<Integer> evens    = Stream.iterate(0, n -> n + 2).limit(100);
Stream<Integer> evensPred = Stream.iterate(0, n -> n < 100, n -> n + 2); // Java 9
Stream<Double> randoms   = Stream.generate(Math::random);

// ── Intermediate Operations (LAZY — nothing runs yet) ─────────
List<Person> people = fetchPeople();

people.stream()
    .filter(p -> p.getAge() >= 18)        // keep only adults
    .filter(p -> p.getActive())           // keep active
    .map(Person::getName)                 // transform to name
    .map(String::toUpperCase)             // uppercase
    .sorted()                             // natural order
    .distinct()                           // remove duplicates
    .skip(5)                              // skip first 5
    .limit(10)                            // take at most 10
    .peek(name -> log.debug("Processing: " + name))  // side-effect for debugging
    .collect(Collectors.toList());

// flatMap: flatten nested structures
List<List<Integer>> nested = List.of(List.of(1,2,3), List.of(4,5), List.of(6));
List<Integer> flat = nested.stream()
    .flatMap(Collection::stream)  // each inner list → individual elements
    .collect(Collectors.toList()); // [1,2,3,4,5,6]

// With Strings:
List<String> sentences = List.of("hello world", "foo bar baz");
List<String> words = sentences.stream()
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .collect(Collectors.toList()); // [hello, world, foo, bar, baz]

// ── Terminal Operations ───────────────────────────────────────
// Count
long count = people.stream().filter(p -> p.getAge() > 30).count();

// Match
boolean anyAdults = people.stream().anyMatch(p -> p.getAge() >= 18);  // short-circuits
boolean allActive = people.stream().allMatch(Person::getActive);
boolean noneMinor = people.stream().noneMatch(p -> p.getAge() < 0);

// Find (short-circuits)
Optional<Person> first = people.stream().filter(Person::getActive).findFirst();
Optional<Person> any   = people.parallelStream().filter(Person::getActive).findAny();

// Reduce — fold elements into one value
int sum = IntStream.rangeClosed(1, 100).sum();                    // 5050
OptionalInt max = IntStream.of(3,1,4,1,5,9).max();
int product = List.of(1,2,3,4,5).stream().reduce(1, (a,b) -> a*b);  // 120
// BinaryOperator<T> reduce(T identity, BinaryOperator<T>)
// Optional<T> reduce(BinaryOperator<T>)  — no identity, might be empty

// forEach (terminal — consumes the stream)
people.stream().filter(Person::getActive).forEach(this::process);

// ── Collectors ────────────────────────────────────────────────
import java.util.stream.Collectors;

// Collect to collections
List<String>        toList  = stream.collect(Collectors.toList());         // mutable
List<String>        toUnmod = stream.collect(Collectors.toUnmodifiableList()); // immutable
Set<String>         toSet   = stream.collect(Collectors.toSet());
LinkedList<String>  toLList = stream.collect(Collectors.toCollection(LinkedList::new));

// Join strings
String joined = Stream.of("a","b","c").collect(Collectors.joining());          // "abc"
String csv    = Stream.of("a","b","c").collect(Collectors.joining(", "));      // "a, b, c"
String full   = Stream.of("a","b","c").collect(Collectors.joining(", ","[","]")); // "[a, b, c]"

// Aggregate statistics
DoubleSummaryStatistics stats = people.stream()
    .collect(Collectors.summarizingDouble(Person::getSalary));
System.out.println(stats.getCount() + " people, avg salary: " + stats.getAverage());

// Group elements: produces Map<Key, List<Value>>
Map<String, List<Person>> byCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity));

// Group with downstream collector
Map<String, Long> countByCity = people.stream()
    .collect(Collectors.groupingBy(Person::getCity, Collectors.counting()));

Map<String, Double> avgSalaryByCity = people.stream()
    .collect(Collectors.groupingBy(
        Person::getCity,
        Collectors.averagingDouble(Person::getSalary)
    ));

Map<String, Optional<Person>> highestPaidByCity = people.stream()
    .collect(Collectors.groupingBy(
        Person::getCity,
        Collectors.maxBy(Comparator.comparingDouble(Person::getSalary))
    ));

// Partition: produces Map<Boolean, List<Value>>
Map<Boolean, List<Person>> adultMinor = people.stream()
    .collect(Collectors.partitioningBy(p -> p.getAge() >= 18));
List<Person> adults = adultMinor.get(true);
List<Person> minors = adultMinor.get(false);

// toMap
Map<Long, Person> byId = people.stream()
    .collect(Collectors.toMap(Person::getId, p -> p));
// If duplicate keys → IllegalStateException; provide merge function:
Map<String, Person> byName = people.stream()
    .collect(Collectors.toMap(
        Person::getName,
        p -> p,
        (existing, duplicate) -> existing  // keep first on conflict
    ));

// ── Numeric Stream Operations ──────────────────────────────────
IntStream salaries = people.stream().mapToInt(Person::getSalary);
salaries.sum();      // total
salaries.average();  // OptionalDouble
salaries.max();      // OptionalInt
salaries.min();      // OptionalInt

// Box/unbox conversions
IntStream ints2 = Stream.of(1,2,3).mapToInt(Integer::intValue); // Stream<Integer> → IntStream
Stream<Integer> boxed = ints2.boxed();                           // IntStream → Stream<Integer>
```

---

## Chapter 18: Modern Java (Java 8 → 21)

### 18.1 Optional — Eliminating NullPointerExceptions

`Optional<T>` is a container that may or may not hold a value. It forces callers to think about the absent case.

```java
// Creating Optional
Optional<String> present = Optional.of("Alice");         // non-null; throws if null
Optional<String> empty   = Optional.empty();             // no value
Optional<String> maybe   = Optional.ofNullable(getName()); // null → empty

// Testing
present.isPresent();   // true
empty.isEmpty();       // true (Java 11)

// Getting values — different trade-offs
present.get();                           // "Alice"; throws NoSuchElementException if empty (avoid)
empty.orElse("Default");                 // "Default" — eager: always evaluates fallback
empty.orElseGet(() -> computeDefault()); // lazy: only computes if empty (prefer)
empty.orElseThrow();                     // throws NoSuchElementException
empty.orElseThrow(() -> new UserNotFoundException("No user found"));

// Transforming (chain operations, stay in Optional context)
Optional<Integer> nameLength = present.map(String::length);            // Optional[5]
Optional<String>  upper      = present.map(String::toUpperCase);       // Optional["ALICE"]
Optional<String>  filtered   = present.filter(s -> s.startsWith("A")); // Optional["Alice"]
// flatMap: when the mapping function itself returns Optional (avoid Optional<Optional<T>>)
Optional<Address> addr = findUser(id).flatMap(User::getAddress);

// Side effects
present.ifPresent(System.out::println);           // run if present
empty.ifPresentOrElse(                             // Java 9
    s -> System.out.println("Found: " + s),
    () -> System.out.println("Not found")
);

// Optional in method signatures
// ✅ Return type — signals value might be absent
public Optional<User> findByEmail(String email) { ... }
// ❌ Parameter — callers would have to wrap every call in Optional.of(); use overloads instead
// ❌ Field — use null + @Nullable annotation for fields; Optional has overhead

// Chaining Optionals for safe navigation (replaces null checks)
// Old way:
String city = null;
if (user != null && user.getAddress() != null && user.getAddress().getCity() != null) {
    city = user.getAddress().getCity().toUpperCase();
}
// New way:
String city2 = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase)
    .orElse("Unknown");
```

### 18.2 Records (Java 16+)

Records are transparent, immutable data carriers. They eliminate the boilerplate of POJOs (Plain Old Java Objects) used purely to hold data.

```java
// A classic POJO — 40+ lines for 3 fields
public final class PersonPOJO {
    private final String name;
    private final int age;
    private final String email;
    public PersonPOJO(String name, int age, String email) {
        this.name = name; this.age = age; this.email = email;
    }
    public String getName() { return name; }
    public int getAge()     { return age; }
    public String getEmail(){ return email; }
    @Override public boolean equals(Object o) { ... }
    @Override public int hashCode()            { ... }
    @Override public String toString()         { ... }
}

// Same thing as a Record — 1 line
public record Person(String name, int age, String email) { }
// Compiler generates: canonical constructor, accessor methods name()/age()/email(),
// equals, hashCode, toString — all based on the record components

// Accessor methods use component names directly (no "get" prefix):
Person p = new Person("Alice", 30, "alice@example.com");
p.name();   // "Alice"  (NOT getName())
p.age();    // 30
System.out.println(p);  // Person[name=Alice, age=30, email=alice@example.com]

// Adding validation — compact constructor:
public record Range(int min, int max) {
    public Range {  // compact constructor: parameters auto-assigned after this block
        if (min > max) throw new IllegalArgumentException("min > max: " + min + " > " + max);
        // Normalise:
        min = Math.max(min, 0);  // clamp to >= 0
    }
    // Custom methods:
    public int span()      { return max - min; }
    public boolean contains(int n) { return n >= min && n <= max; }
}

// Records can implement interfaces
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {
    @Override
    public int compareTo(Money other) {
        if (!this.currency.equals(other.currency))
            throw new IllegalArgumentException("Cannot compare different currencies");
        return this.amount.compareTo(other.amount);
    }
}

// Records are great for:
// - DTOs (Data Transfer Objects) from/to APIs
// - Value objects (coordinates, ranges, money)
// - Projection results from queries
// - Immutable configuration holders
```

### 18.3 Sealed Classes (Java 17+)

Sealed classes restrict which classes can extend them. Used with pattern matching, they allow exhaustive type checks — the compiler can verify all cases are handled.

```java
// Sealed hierarchy — complete set of subtypes is known at compile time
public sealed interface Shape permits Circle, Rectangle, Triangle, Line { }

public record Circle(double radius) implements Shape { }
public record Rectangle(double width, double height) implements Shape { }
public record Triangle(double a, double b, double c) implements Shape { }
public non-sealed class Line implements Shape { /* can be extended further */ }

// Pattern matching in switch — exhaustive (no default needed for sealed types)
public double area(Shape shape) {
    return switch (shape) {
        case Circle(var r)           -> Math.PI * r * r;  // Destructuring (Java 21)
        case Rectangle(var w, var h) -> w * h;
        case Triangle(var a, var b, var c) -> {
            double s = (a + b + c) / 2;
            yield Math.sqrt(s * (s-a) * (s-b) * (s-c));
        }
        case Line l -> 0;  // line has no area
    };
    // No default needed: compiler knows all cases are covered
    // Add a new Shape subtype → immediate compile error here: case not handled
}
```

### 18.4 Pattern Matching — instanceof and Switch

```java
// Pattern matching instanceof (Java 16)
Object obj = fetchFromNetwork();

// Old way — 3 steps
if (obj instanceof String) {
    String s = (String) obj;  // redundant cast
    System.out.println(s.length());
}

// New way — 1 step: check + bind + use
if (obj instanceof String s) {          // s is in scope here
    System.out.println(s.length());
}

// Guard condition — add && to filter
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}

// Switch pattern matching (Java 21)
String describe(Object obj) {
    return switch (obj) {
        case Integer i when i < 0    -> "negative integer: " + i;
        case Integer i               -> "non-negative integer: " + i;
        case Double d                -> "double: " + d;
        case String s when s.isBlank()-> "blank string";
        case String s                -> "string: " + s;
        case int[]  arr              -> "int array of length " + arr.length;
        case null                    -> "null value";
        default                      -> "unknown: " + obj.getClass().getSimpleName();
    };
}
```

### 18.5 Date & Time API (java.time — Java 8+)

The old `java.util.Date` and `Calendar` are notoriously broken (mutable, confusing months 0-11). The `java.time` package is the replacement.

```java
import java.time.*;
import java.time.format.*;
import java.time.temporal.*;

// ── Core Types ────────────────────────────────────────────────
LocalDate date = LocalDate.now();               // date only, no time, no timezone
LocalDate bday = LocalDate.of(1995, 3, 15);     // months 1-12 (not 0-11!)
LocalDate bday2= LocalDate.of(1995, Month.MARCH, 15);

LocalTime time = LocalTime.now();               // time only, no date, no timezone
LocalTime noon = LocalTime.of(12, 0, 0);        // 12:00:00
LocalTime now  = LocalTime.of(14, 30, 45, 500_000_000); // 14:30:45.5

LocalDateTime dt = LocalDateTime.now();         // date + time, no timezone
LocalDateTime meeting = LocalDateTime.of(2024, 6, 15, 14, 30);

ZonedDateTime zdt = ZonedDateTime.now();        // date + time + timezone
ZonedDateTime cairo = ZonedDateTime.now(ZoneId.of("Africa/Cairo"));
ZoneId.getAvailableZoneIds();                   // all timezone IDs

Instant now2 = Instant.now();                   // machine time: nanoseconds from epoch
// Use Instant for timestamps, logging, durations

// ── Arithmetic ────────────────────────────────────────────────
LocalDate nextWeek    = date.plusDays(7);
LocalDate lastMonth   = date.minusMonths(1);
LocalDate nextYear    = date.plusYears(1);
LocalDate threeMonths = date.plus(3, ChronoUnit.MONTHS);  // generic method

LocalDateTime inTwoHours = dt.plusHours(2).plusMinutes(30);

// ── Comparing & Querying ──────────────────────────────────────
date.isBefore(LocalDate.of(2030, 1, 1));         // true
date.isAfter(LocalDate.of(2000, 1, 1));          // true
date.isEqual(LocalDate.now());                    // true
date.getDayOfWeek();                              // DayOfWeek.MONDAY etc.
date.getDayOfMonth();                             // 1-31
date.getMonth();                                  // Month.MARCH etc.
date.getYear();
date.lengthOfMonth();                             // days in current month
date.isLeapYear();

// ── Duration and Period ───────────────────────────────────────
Duration d = Duration.between(startInstant, endInstant);  // time-based
d.toHours(); d.toMinutes(); d.toSeconds(); d.toMillis();

Period p = Period.between(startDate, endDate);   // date-based
p.getYears(); p.getMonths(); p.getDays();

long days = ChronoUnit.DAYS.between(startDate, endDate);

// ── Formatting & Parsing ──────────────────────────────────────
DateTimeFormatter fmt1 = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
DateTimeFormatter fmt2 = DateTimeFormatter.ofPattern("MMMM d, yyyy", Locale.ENGLISH);
DateTimeFormatter iso  = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

String formatted = dt.format(fmt1);                  // "15/06/2024 14:30:00"
LocalDateTime parsed = LocalDateTime.parse("15/06/2024 14:30:00", fmt1);

// Common built-in formatters:
DateTimeFormatter.ISO_DATE             // 2024-06-15
DateTimeFormatter.ISO_DATE_TIME        // 2024-06-15T14:30:00
DateTimeFormatter.RFC_1123_DATE_TIME   // Mon, 15 Jun 2024 14:30:00 GMT

// ── Timezone Conversions ──────────────────────────────────────
ZonedDateTime utc   = ZonedDateTime.now(ZoneId.of("UTC"));
ZonedDateTime nyc   = utc.withZoneSameInstant(ZoneId.of("America/New_York"));
ZonedDateTime tokyo = utc.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
```

### 18.6 Virtual Threads (Java 21 — Project Loom)

Virtual threads are lightweight, JVM-managed threads. You can create millions of them.

```java
// Platform thread — expensive: 1 OS thread (~1MB stack)
Thread heavy = new Thread(() -> handleRequest());
heavy.start();

// Virtual thread — cheap: ~few hundred bytes; JVM multiplexes onto OS threads
Thread light = Thread.ofVirtual().name("virtual-1").start(() -> handleRequest());

// Virtual thread executor — 1 virtual thread per task, ideal for I/O-bound work
try (ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 1_000_000; i++) {
        int taskId = i;
        exec.submit(() -> {
            // I/O operation: virtual thread is unmounted from OS thread while blocking
            // OS thread is free to run other virtual threads during the wait
            String data = fetchFromNetwork(taskId);  // blocks, but not the OS thread
            processData(data);
        });
    }
}  // executor.close() waits for all tasks to complete

// When virtual threads shine:  I/O-bound workloads (web requests, DB queries)
// When they don't help:        CPU-bound work (cryptography, image processing)
// Key constraint: avoid synchronized blocks in virtual threads (pins the carrier thread)
//                 use ReentrantLock instead of synchronized when possible
```

---

## Chapter 19: JVM Internals & Memory Management

### 19.1 JVM Memory Areas

```
┌────────────────────────────────────────────────────────────────┐
│  Metaspace (non-heap, unlimited by default)                     │
│  ├── Class metadata (.class structure)                          │
│  ├── Method bytecode                                            │
│  ├── Static fields (Java 8+ moved here from PermGen)           │
│  └── String pool / interned strings                             │
├────────────────────────────────────────────────────────────────┤
│  Heap (shared; Garbage Collected)                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Young Generation (objects die young — minor GC)          │  │
│  │  ┌──────────┐  ┌────────────┐  ┌────────────┐           │  │
│  │  │  Eden    │  │ Survivor 0 │  │ Survivor 1 │           │  │
│  │  │ (new obj)│  │ (age 1-15) │  │ (empty)    │           │  │
│  │  └──────────┘  └────────────┘  └────────────┘           │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Old Generation / Tenured (survived many GCs)            │  │
│  │  Objects that survived ~15 minor GCs get promoted here   │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│  Stack (per-thread; NOT garbage collected)                      │
│  ├── Stack frames: one per method call                          │
│  │   ├── Local variables                                        │
│  │   ├── Operand stack                                          │
│  │   └── Return address                                         │
│  └── Automatically freed when method returns                    │
├────────────────────────────────────────────────────────────────┤
│  PC (Program Counter) Register — per-thread; current instruction│
│  Native Method Stack — for JNI C/C++ calls                     │
└────────────────────────────────────────────────────────────────┘
```

### 19.2 Garbage Collection — Detailed

```
Object lifecycle:
  1. Allocated in EDEN
  2. Survives minor GC → copied to Survivor 0 or Survivor 1 (alternates)
  3. Age counter incremented each minor GC
  4. Age reaches threshold (default: 15) → promoted to OLD GEN
  5. OLD GEN fills → Major/Full GC triggered (expensive, "stop-the-world")
  6. Object unreachable → eligible for GC

An object is REACHABLE if you can reach it from:
  - Local variables in any thread's stack
  - Static fields
  - JNI references
  - ... (root set)
  
An object is UNREACHABLE when NO live reference points to it.
```

**GC Algorithms — choosing the right one:**
```
Serial GC (-XX:+UseSerialGC)
  Single-threaded collection; pauses entire app
  Use for: single-core machines, tiny heaps, CLI tools

Parallel GC (-XX:+UseParallelGC)
  Multi-threaded Young GC; stop-the-world
  Use for: batch jobs where throughput > pause time

G1 GC (-XX:+UseG1GC) [DEFAULT since Java 9]
  Divides heap into regions; concurrent mostly
  Aims for predictable pause time (default: 200ms)
  Use for: most server applications; heaps 4GB+

ZGC (-XX:+UseZGC) [Production since Java 15]
  Concurrent, almost no pause (< 10ms even for TB heaps)
  Use for: latency-sensitive; very large heaps

Shenandoah (-XX:+UseShenandoahGC)
  Concurrent compaction; low pauses
  Use for: similar to ZGC; preferred in some OpenJDK builds
```

**JVM tuning flags:**
```bash
-Xms512m                          # initial heap size
-Xmx4g                            # maximum heap size (set = Xms for predictability)
-XX:NewRatio=3                    # old:young ratio (3:1 → 75% old, 25% young)
-XX:SurvivorRatio=8               # eden:survivor ratio (8:1:1 per default)
-XX:MaxGCPauseMillis=200          # G1 target pause time (soft goal)
-XX:G1HeapRegionSize=16m          # G1 region size
-XX:+UseStringDeduplication       # deduplicate equal Strings in heap (G1 only)
-XX:+PrintGCDetails -XX:+PrintGCDateStamps  # GC logging
-XX:+HeapDumpOnOutOfMemoryError   # capture heap dump when OOM
-XX:HeapDumpPath=/tmp/heap.hprof
```

### 19.3 Memory Leaks in Java

Java has GC, but you can still leak memory by keeping references you don't need:

```java
// 1. Static collections accumulating without bounds
public class Registry {
    private static final Map<String, Object> cache = new HashMap<>();
    public static void register(String key, Object value) {
        cache.put(key, value);   // grows forever if nothing is removed
    }
    // Fix: use WeakHashMap, or set a max size with eviction
}

// 2. Listeners not deregistered
button.addActionListener(this::handleClick);
// If 'button' outlives 'this', 'this' can't be GC'd — listener holds a reference
// Fix: remove listener when 'this' is done: button.removeActionListener(listener)

// 3. ThreadLocal not cleaned up
ThreadLocal<Connection> connectionHolder = new ThreadLocal<>();
// In thread pool, threads are reused. ThreadLocal values survive between tasks!
// Fix: always call connectionHolder.remove() when done
try {
    connectionHolder.set(getConnection());
    doWork();
} finally {
    connectionHolder.remove();  // CRITICAL in thread pools
}

// 4. Inner classes holding outer class reference
class Outer {
    private byte[] bigData = new byte[1024 * 1024];
    class Inner {  // holds implicit reference to Outer.this
        void run() { /* even if doesn't use bigData */ }
    }
    // If Inner is stored somewhere, bigData can't be GC'd
    // Fix: make Inner static if it doesn't need Outer's state
}
```

---

## Chapter 20: Design Patterns

### 20.1 Creational Patterns

**Singleton — one instance per JVM:**
```java
// Best implementation: Initialization-on-demand holder (thread-safe, lazy)
public final class AppConfig {
    private AppConfig() { loadFromFile(); }

    private static final class Holder {
        static final AppConfig INSTANCE = new AppConfig();
    }

    public static AppConfig getInstance() {
        return Holder.INSTANCE;  // JVM guarantees Holder is loaded only once
    }
}

// Enum Singleton (simplest; serialization-safe; reflection-resistant):
public enum DatabasePool {
    INSTANCE;
    private final HikariDataSource ds = createPool();
    public Connection getConnection() throws SQLException { return ds.getConnection(); }
}
```

**Builder — constructing complex objects step by step:**
```java
public class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final String body;
    private final int timeoutSeconds;

    private HttpRequest(Builder b) {
        this.url = b.url; this.method = b.method;
        this.headers = Map.copyOf(b.headers);
        this.body = b.body; this.timeoutSeconds = b.timeoutSeconds;
    }

    // Static inner Builder class
    public static class Builder {
        private final String url;         // required
        private String method = "GET";    // optional with default
        private Map<String, String> headers = new LinkedHashMap<>();
        private String body;
        private int timeoutSeconds = 30;

        public Builder(String url) {
            if (url == null) throw new IllegalArgumentException("url required");
            this.url = url;
        }

        public Builder method(String m)              { this.method = m; return this; }
        public Builder header(String k, String v)    { headers.put(k, v); return this; }
        public Builder body(String b)                { this.body = b; return this; }
        public Builder timeout(int seconds)          { this.timeoutSeconds = seconds; return this; }
        public HttpRequest build()                   { return new HttpRequest(this); }
    }
}

// Fluent usage:
HttpRequest req = new HttpRequest.Builder("https://api.example.com/users/1")
    .method("PUT")
    .header("Authorization", "Bearer " + token)
    .header("Content-Type", "application/json")
    .body("{\"name\":\"Alice\"}")
    .timeout(10)
    .build();
```

**Factory Method — let subclasses decide which class to instantiate:**
```java
// Abstract factory method
abstract class Dialog {
    // Factory method — subclass decides which button to create
    abstract Button createButton();

    // Template method uses the factory method
    void render() {
        Button b = createButton();  // polymorphic creation
        b.onClick(() -> close());
        b.render();
    }
}

class WindowsDialog extends Dialog {
    @Override
    Button createButton() { return new WindowsButton(); }
}

class WebDialog extends Dialog {
    @Override
    Button createButton() { return new HtmlButton(); }
}

// Static factory method (simpler; common in Java):
public class ConnectionFactory {
    public static Connection create(ConnectionType type) {
        return switch (type) {
            case MYSQL    -> new MySqlConnection();
            case POSTGRES -> new PostgresConnection();
            case SQLITE   -> new SQLiteConnection();
        };
    }
}
```

### 20.2 Structural Patterns

**Decorator — add behaviour without subclassing:**
```java
interface TextProcessor { String process(String text); }

class PlainProcessor implements TextProcessor {
    public String process(String text) { return text; }
}

abstract class TextDecorator implements TextProcessor {
    protected final TextProcessor wrapped;
    public TextDecorator(TextProcessor p) { this.wrapped = p; }
}

class TrimDecorator extends TextDecorator {
    public TrimDecorator(TextProcessor p) { super(p); }
    public String process(String text) { return wrapped.process(text).trim(); }
}

class UpperCaseDecorator extends TextDecorator {
    public UpperCaseDecorator(TextProcessor p) { super(p); }
    public String process(String text) { return wrapped.process(text).toUpperCase(); }
}

class HtmlEncodeDecorator extends TextDecorator {
    public HtmlEncodeDecorator(TextProcessor p) { super(p); }
    public String process(String text) {
        return wrapped.process(text)
            .replace("&","&amp;").replace("<","&lt;").replace(">","&gt;");
    }
}

// Stack decorators as needed:
TextProcessor processor = new HtmlEncodeDecorator(
                          new UpperCaseDecorator(
                          new TrimDecorator(
                          new PlainProcessor())));
processor.process("  <hello> & world  ");  // "&LT;HELLO&GT; &AMP; WORLD"
```

**Strategy — swap algorithms at runtime:**
```java
interface SortStrategy { void sort(int[] arr); }

class BubbleSort implements SortStrategy {
    public void sort(int[] arr) { /* bubble sort */ }
}
class MergeSort implements SortStrategy {
    public void sort(int[] arr) { /* merge sort */ }
}

class DataSorter {
    private SortStrategy strategy;
    public DataSorter(SortStrategy strategy) { this.strategy = strategy; }
    public void setStrategy(SortStrategy s) { this.strategy = s; }
    public void sort(int[] data) { strategy.sort(data); }
}

// Swap strategy based on data size:
DataSorter sorter = new DataSorter(new BubbleSort());
if (data.length > 1000) sorter.setStrategy(new MergeSort());
sorter.sort(data);
```

**Observer — event notification system:**
```java
// Event system with generics
public class EventBus<T> {
    private final List<Consumer<T>> listeners = new CopyOnWriteArrayList<>();

    public void subscribe(Consumer<T> listener)   { listeners.add(listener); }
    public void unsubscribe(Consumer<T> listener) { listeners.remove(listener); }
    public void publish(T event) {
        listeners.forEach(listener -> {
            try { listener.accept(event); }
            catch (Exception e) { log.error("Listener error", e); }
        });
    }
}

// Usage:
EventBus<OrderEvent> orderBus = new EventBus<>();
orderBus.subscribe(event -> emailService.notifyUser(event.getUserId()));
orderBus.subscribe(event -> inventoryService.reserve(event.getProductId()));
orderBus.publish(new OrderEvent(orderId, userId, productId));
```

---

## Chapter 21: Annotations & Reflection

### 21.1 Annotations — Metadata for Code

```java
import java.lang.annotation.*;

// Defining a custom annotation
@Target({ElementType.METHOD, ElementType.TYPE})   // where it can be applied
@Retention(RetentionPolicy.RUNTIME)               // available at runtime via reflection
@Documented                                       // appears in Javadoc
@Inherited                                        // subclasses inherit it (only for types)
public @interface Cacheable {
    String key() default "";             // element with default
    int ttlSeconds() default 300;        // 5 minutes
    boolean condition() default true;    // cache only if true
}

// Using it:
@Cacheable(key = "user:{id}", ttlSeconds = 3600)
public User findUser(Long id) { ... }

// Processing at runtime via reflection:
Method method = UserService.class.getMethod("findUser", Long.class);
Cacheable cache = method.getAnnotation(Cacheable.class);
if (cache != null) {
    System.out.println("Cache key: " + cache.key());
    System.out.println("TTL: " + cache.ttlSeconds());
}
```

### 21.2 Reflection — Inspect and Manipulate at Runtime

```java
// Get Class object
Class<?> clazz = String.class;
Class<?> clazz2 = Class.forName("java.lang.String");  // dynamic loading
Class<?> clazz3 = "hello".getClass();

// Inspect class structure
System.out.println(clazz.getName());             // java.lang.String
System.out.println(clazz.getSimpleName());       // String
System.out.println(clazz.getSuperclass());       // class java.lang.Object
Arrays.stream(clazz.getInterfaces()).forEach(i -> System.out.println(i.getSimpleName()));

// Inspect and invoke methods
Method[] methods = clazz.getDeclaredMethods();
Method lengthMethod = clazz.getMethod("length");          // public methods only
Method trimMethod   = clazz.getMethod("trim");
int len = (int) lengthMethod.invoke("Hello World");       // invoke: 11

// Inspect and access fields
Field[] fields = MyClass.class.getDeclaredFields();
Field secret = MyClass.class.getDeclaredField("secretField");
secret.setAccessible(true);                      // bypass access control (Java 9+: requires --add-opens)
Object value = secret.get(myInstance);
secret.set(myInstance, "new value");

// Create instances dynamically
Constructor<?> ctor = StringBuilder.class.getConstructor(String.class);
StringBuilder sb = (StringBuilder) ctor.newInstance("Hello");

// Practical use cases:
// - Dependency injection frameworks (Spring uses reflection to inject beans)
// - ORM frameworks (Hibernate maps fields to columns via reflection)
// - Testing frameworks (JUnit finds @Test methods via reflection)
// - JSON serialisation (Jackson reads/writes fields via reflection)
```

---

# PART II — DATA STRUCTURES & ALGORITHMS

---

## Chapter 22: Complexity Analysis

### 22.1 Why It Matters

An algorithm that processes 1,000 items in 1ms might take 1,000,000ms for 1,000,000 items if it's O(n²). Understanding complexity lets you choose algorithms that scale.

```
n=10:      O(n)=10,     O(n²)=100,          O(n log n)=33
n=1,000:   O(n)=1K,     O(n²)=1,000,000,    O(n log n)=10K
n=1,000,000: O(n)=1M,   O(n²)=1,000,000,000,000 ← unusable
```

### 22.2 Big O Notation

| Notation | Name | Example Operations |
|----------|------|--------------------|
| O(1) | Constant | Array index, HashMap get, push/pop |
| O(log n) | Logarithmic | Binary search, TreeMap operations |
| O(n) | Linear | Linear search, single traversal |
| O(n log n) | Linearithmic | Merge sort, quick sort (average) |
| O(n²) | Quadratic | Bubble/insertion/selection sort, nested loops |
| O(2ⁿ) | Exponential | Naive Fibonacci, power set |
| O(n!) | Factorial | Permutations, naive TSP |

**How to calculate:**
```java
// O(1) — constant number of operations regardless of input size
int getFirst(int[] arr) { return arr[0]; }

// O(n) — loop over all n elements
int sum(int[] arr) {
    int total = 0;
    for (int x : arr) total += x;  // executes n times
    return total;
}

// O(n²) — nested loop over all pairs
void printPairs(int[] arr) {
    for (int i = 0; i < arr.length; i++) {       // n iterations
        for (int j = 0; j < arr.length; j++) {   // n iterations each
            System.out.println(arr[i] + "," + arr[j]); // n × n = n²
        }
    }
}

// O(n log n) — divide and conquer
void mergeSort(int[] arr, int l, int r) {
    if (l >= r) return;
    int mid = (l + r) / 2;
    mergeSort(arr, l, mid);     // log n levels of recursion
    mergeSort(arr, mid+1, r);
    merge(arr, l, mid, r);      // each level does O(n) work
}

// Dropping constants and lower-order terms (Big O notation rules):
// O(2n)        → O(n)
// O(n + n²)    → O(n²)
// O(n + 500)   → O(n)
// O(n³ + n²)   → O(n³)
```

---

## Chapter 23: Searching & Sorting

### 23.1 Linear Search

```java
// O(n) time, O(1) space
// Use when: unsorted data, small n, searching non-comparables
public static int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) return i;
    }
    return -1;  // not found
}

// Generic version
public static <T> int linearSearch(T[] arr, T target) {
    for (int i = 0; i < arr.length; i++) {
        if (Objects.equals(arr[i], target)) return i;
    }
    return -1;
}
```

### 23.2 Binary Search

```java
// O(log n) time, O(1) space — requires SORTED array
// Each step eliminates HALF the remaining elements
// For n=1,000,000: max 20 comparisons (log₂(1,000,000) ≈ 20)

// Iterative (preferred — no stack overhead)
public static int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;   // avoids integer overflow vs (low+high)/2
        if      (arr[mid] == target) return mid;
        else if (arr[mid]  < target) low  = mid + 1;  // target in right half
        else                         high = mid - 1;  // target in left half
    }
    return -1;  // not found
    // If you need insertion point: return -(low + 1)
}

// Recursive
public static int binarySearchRec(int[] arr, int target, int low, int high) {
    if (low > high) return -1;
    int mid = low + (high - low) / 2;
    if      (arr[mid] == target) return mid;
    else if (arr[mid]  < target) return binarySearchRec(arr, target, mid + 1, high);
    else                         return binarySearchRec(arr, target, low, mid - 1);
}

// Template for binary search on answer (bisection):
// "Find the smallest x such that condition(x) is true"
int binarySearchOnAnswer(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (condition(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

### 23.3 Sorting Algorithms

```java
// ── Bubble Sort — O(n²) ──────────────────────────────────────
public static void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int pass = 0; pass < n - 1; pass++) {
        boolean swapped = false;
        for (int j = 0; j < n - pass - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j]; arr[j] = arr[j+1]; arr[j+1] = tmp;
                swapped = true;
            }
        }
        if (!swapped) break;  // already sorted — early exit
    }
}
// Best: O(n) when nearly sorted. Average/Worst: O(n²). Stable. In-place.

// ── Selection Sort — O(n²) ───────────────────────────────────
public static void selectionSort(int[] arr) {
    for (int i = 0; i < arr.length - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        // Swap minimum to position i
        if (minIdx != i) {
            int tmp = arr[i]; arr[i] = arr[minIdx]; arr[minIdx] = tmp;
        }
    }
}
// Always O(n²). NOT stable. In-place. Minimum swaps: n-1.

// ── Insertion Sort — O(n²) ───────────────────────────────────
public static void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        // Shift elements > key one position right
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;  // insert key in correct position
    }
}
// Best: O(n) for nearly sorted. Worst: O(n²). Stable. In-place.
// Java uses Insertion Sort for arrays of size ≤ 47 (threshold in DualPivotQuicksort)

// ── Merge Sort — O(n log n) ───────────────────────────────────
public static void mergeSort(int[] arr, int left, int right) {
    if (left >= right) return;  // base case: 0 or 1 element
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);       // sort left half
    mergeSort(arr, mid + 1, right);  // sort right half
    merge(arr, left, mid, right);    // merge two sorted halves
}

private static void merge(int[] arr, int left, int mid, int right) {
    // Copy subarrays to temporary arrays
    int[] L = Arrays.copyOfRange(arr, left, mid + 1);
    int[] R = Arrays.copyOfRange(arr, mid + 1, right + 1);
    int i = 0, j = 0, k = left;
    while (i < L.length && j < R.length) {
        if (L[i] <= R[j]) arr[k++] = L[i++];  // <= makes it stable
        else              arr[k++] = R[j++];
    }
    while (i < L.length) arr[k++] = L[i++];
    while (j < R.length) arr[k++] = R[j++];
}
// Always O(n log n). Stable. NOT in-place (needs O(n) extra memory).
// Best sort when stability required or for linked lists.

// ── Quick Sort — O(n log n) average ──────────────────────────
public static void quickSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int pivotIdx = partition(arr, low, high);
    quickSort(arr, low, pivotIdx - 1);   // sort left of pivot
    quickSort(arr, pivotIdx + 1, high);  // sort right of pivot
}

private static int partition(int[] arr, int low, int high) {
    // Lomuto partition: pivot = last element
    int pivot = arr[high];
    int i = low - 1;  // boundary of "less than pivot" region
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
        }
    }
    // Place pivot in correct position
    int tmp = arr[i+1]; arr[i+1] = arr[high]; arr[high] = tmp;
    return i + 1;
}
// Average O(n log n). Worst O(n²) for sorted input (use random pivot to mitigate).
// NOT stable. In-place (O(log n) stack space).
// Fastest in practice due to CPU cache locality.
```

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |

---

## Chapter 24: Linked Lists, Stacks & Queues

### 24.1 Singly Linked List — Full Implementation

```java
public class LinkedList<T> {
    private static class Node<T> {
        T data;
        Node<T> next;
        Node(T data) { this.data = data; this.next = null; }
    }

    private Node<T> head;
    private int size;

    // Insert at end — O(n)
    public void addLast(T data) {
        Node<T> newNode = new Node<>(data);
        if (head == null) { head = newNode; size++; return; }
        Node<T> cur = head;
        while (cur.next != null) cur = cur.next;
        cur.next = newNode;
        size++;
    }

    // Insert at beginning — O(1)
    public void addFirst(T data) {
        Node<T> newNode = new Node<>(data);
        newNode.next = head;
        head = newNode;
        size++;
    }

    // Insert at index — O(n)
    public void addAt(int index, T data) {
        if (index < 0 || index > size) throw new IndexOutOfBoundsException(index);
        if (index == 0) { addFirst(data); return; }
        Node<T> cur = head;
        for (int i = 0; i < index - 1; i++) cur = cur.next;
        Node<T> newNode = new Node<>(data);
        newNode.next = cur.next;
        cur.next = newNode;
        size++;
    }

    // Delete at index — O(n)
    public T removeAt(int index) {
        if (index < 0 || index >= size) throw new IndexOutOfBoundsException(index);
        T removed;
        if (index == 0) {
            removed = head.data;
            head = head.next;
        } else {
            Node<T> cur = head;
            for (int i = 0; i < index - 1; i++) cur = cur.next;
            removed = cur.next.data;
            cur.next = cur.next.next;
        }
        size--;
        return removed;
    }

    // Reverse in-place — O(n)
    public void reverse() {
        Node<T> prev = null, curr = head;
        while (curr != null) {
            Node<T> next = curr.next;  // save next before overwriting
            curr.next = prev;           // reverse the link
            prev = curr;               // advance prev
            curr = next;               // advance curr
        }
        head = prev;  // prev is new head
    }

    // Detect cycle — Floyd's Tortoise and Hare
    public boolean hasCycle() {
        Node<T> slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;         // 1 step
            fast = fast.next.next;    // 2 steps
            if (slow == fast) return true;  // met inside cycle
        }
        return false;
    }

    public int size() { return size; }

    public void display() {
        Node<T> cur = head;
        StringBuilder sb = new StringBuilder("HEAD → ");
        while (cur != null) { sb.append(cur.data).append(" → "); cur = cur.next; }
        System.out.println(sb.append("NULL"));
    }
}
```

### 24.2 Stack — Full Implementation

```java
// Array-based fixed stack
public class Stack<T> {
    private final Object[] data;
    private int top = -1;

    public Stack(int capacity) { data = new Object[capacity]; }

    public void push(T item) {
        if (isFull()) throw new RuntimeException("Stack overflow");
        data[++top] = item;
    }

    @SuppressWarnings("unchecked")
    public T pop() {
        if (isEmpty()) throw new EmptyStackException();
        T item = (T) data[top];
        data[top--] = null;   // null out for GC
        return item;
    }

    @SuppressWarnings("unchecked")
    public T peek()          { if (isEmpty()) throw new EmptyStackException(); return (T) data[top]; }
    public int  size()       { return top + 1; }
    public boolean isEmpty() { return top == -1; }
    public boolean isFull()  { return top == data.length - 1; }
}

// Dynamic stack backed by ArrayList
public class DynamicStack<T> {
    private final ArrayList<T> list = new ArrayList<>();
    public void push(T item)  { list.add(item); }
    public T    pop()         { if (isEmpty()) throw new EmptyStackException();
                                return list.remove(list.size() - 1); }
    public T    peek()        { if (isEmpty()) throw new EmptyStackException();
                                return list.get(list.size() - 1); }
    public boolean isEmpty()  { return list.isEmpty(); }
    public int  size()        { return list.size(); }
}

// Classic Stack problem: balanced parentheses checker
public static boolean isBalanced(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (c=='(' || c=='{' || c=='[') { stack.push(c); }
        else if (c==')' || c=='}' || c==']') {
            if (stack.isEmpty()) return false;
            char top = stack.pop();
            if ((c==')' && top!='(') || (c=='}' && top!='{') || (c==']' && top!='['))
                return false;
        }
    }
    return stack.isEmpty();
}
```

---

## Chapter 25: Trees & Graphs

### 25.1 Binary Search Tree — Full Implementation

```java
public class BST {
    private static class Node {
        int data;
        Node left, right;
        Node(int data) { this.data = data; }
    }
    private Node root;

    // Insert — O(h); h=log n balanced, h=n worst case
    public void insert(int data) { root = insertRec(root, data); }
    private Node insertRec(Node node, int data) {
        if (node == null) return new Node(data);
        if      (data < node.data) node.left  = insertRec(node.left,  data);
        else if (data > node.data) node.right = insertRec(node.right, data);
        // data == node.data: duplicate, do nothing
        return node;
    }

    // Search — O(h)
    public boolean contains(int data) { return containsRec(root, data); }
    private boolean containsRec(Node node, int data) {
        if (node == null) return false;
        if (data == node.data) return true;
        return data < node.data
            ? containsRec(node.left, data)
            : containsRec(node.right, data);
    }

    // Tree Traversals:
    // In-order (Left→Root→Right) — produces SORTED output for BST
    public void inOrder()   { inOrderRec(root); System.out.println(); }
    private void inOrderRec(Node n) {
        if (n == null) return;
        inOrderRec(n.left);
        System.out.print(n.data + " ");
        inOrderRec(n.right);
    }

    // Pre-order (Root→Left→Right) — used to copy/serialize tree
    public void preOrder()  { preOrderRec(root); System.out.println(); }
    private void preOrderRec(Node n) {
        if (n == null) return;
        System.out.print(n.data + " ");
        preOrderRec(n.left);
        preOrderRec(n.right);
    }

    // Post-order (Left→Right→Root) — used to delete tree, expression evaluation
    public void postOrder() { postOrderRec(root); System.out.println(); }
    private void postOrderRec(Node n) {
        if (n == null) return;
        postOrderRec(n.left);
        postOrderRec(n.right);
        System.out.print(n.data + " ");
    }

    // Level-order (BFS) — uses Queue
    public void levelOrder() {
        if (root == null) return;
        Queue<Node> queue = new ArrayDeque<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            Node cur = queue.poll();
            System.out.print(cur.data + " ");
            if (cur.left  != null) queue.offer(cur.left);
            if (cur.right != null) queue.offer(cur.right);
        }
        System.out.println();
    }

    // Height — O(n)
    public int height() { return heightRec(root); }
    private int heightRec(Node n) {
        if (n == null) return 0;
        return 1 + Math.max(heightRec(n.left), heightRec(n.right));
    }

    // Delete — O(h); 3 cases
    public void delete(int data) { root = deleteRec(root, data); }
    private Node deleteRec(Node node, int data) {
        if (node == null) return null;
        if      (data < node.data) node.left  = deleteRec(node.left,  data);
        else if (data > node.data) node.right = deleteRec(node.right, data);
        else {  // found node to delete
            if (node.left  == null) return node.right; // case 1: no left child
            if (node.right == null) return node.left;  // case 2: no right child
            // case 3: two children — replace with in-order successor (min of right subtree)
            Node successor = findMin(node.right);
            node.data  = successor.data;
            node.right = deleteRec(node.right, successor.data);
        }
        return node;
    }
    private Node findMin(Node n) { while (n.left != null) n = n.left; return n; }
}
```

### 25.2 Graph — BFS and DFS

```java
// Graph represented as adjacency list
public class Graph {
    private final int vertices;
    private final List<List<Integer>> adj;

    public Graph(int v) {
        vertices = v;
        adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
    }

    public void addEdge(int u, int v) {
        adj.get(u).add(v);
        adj.get(v).add(u);  // remove this line for directed graph
    }

    // BFS — level-by-level traversal; shortest path in unweighted graphs
    public void bfs(int start) {
        boolean[] visited = new boolean[vertices];
        Queue<Integer> queue = new ArrayDeque<>();
        visited[start] = true;
        queue.offer(start);
        while (!queue.isEmpty()) {
            int node = queue.poll();
            System.out.print(node + " ");
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
    }

    // DFS — depth-first; cycle detection, topological sort, connected components
    public void dfs(int start) {
        boolean[] visited = new boolean[vertices];
        dfsRec(start, visited);
    }
    private void dfsRec(int node, boolean[] visited) {
        visited[node] = true;
        System.out.print(node + " ");
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) dfsRec(neighbor, visited);
        }
    }
}
```

---

## Chapter 26: Dynamic Programming & Greedy

### 26.1 Dynamic Programming — Key Concepts

DP = break a problem into overlapping subproblems, solve each once, cache results.

**When to use DP:** optimal substructure + overlapping subproblems.

```java
// Classic DP: Fibonacci with memoization
private Map<Integer, Long> memo = new HashMap<>();
public long fib(int n) {
    if (n <= 1) return n;
    return memo.computeIfAbsent(n, k -> fib(k-1) + fib(k-2));
}

// Bottom-up DP (tabulation): Fibonacci without recursion
public long fibDP(int n) {
    if (n <= 1) return n;
    long[] dp = new long[n + 1];
    dp[0] = 0; dp[1] = 1;
    for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}

// 0/1 Knapsack: max value from items with weight limit
// dp[i][w] = max value using first i items with weight capacity w
public int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            // Option 1: don't take item i
            dp[i][w] = dp[i-1][w];
            // Option 2: take item i (if it fits)
            if (weights[i-1] <= w) {
                dp[i][w] = Math.max(dp[i][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]);
            }
        }
    }
    return dp[n][capacity];
}

// Longest Common Subsequence
public int lcs(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m+1][n+1];
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i-1) == s2.charAt(j-1))
                dp[i][j] = dp[i-1][j-1] + 1;
            else
                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
        }
    }
    return dp[m][n];
}

// Coin Change (minimum coins)
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);  // initialize to "impossible"
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

# PART III — ENTERPRISE JAVA

---

## Chapter 27: JDBC

### 27.1 Why JDBC Exists — The Problem It Solves

Before JDBC, every database vendor had a completely different, proprietary Java API. Code written for Oracle couldn't run against MySQL. JDBC (Java Database Connectivity), introduced in Java 1.1, defines a **standard API** that every database vendor implements through a **driver**. Your code talks to the JDBC API; the driver translates to the database's native protocol.

```
Your Java code
      │
      ▼
  JDBC API (java.sql.*)           ← standard, in JDK
      │
      ▼
  JDBC Driver (vendor JAR)        ← e.g., mysql-connector-j-8.x.jar
      │
      ▼
  Database (MySQL / PostgreSQL / Oracle / SQLite / H2 ...)
```

**Four driver types (you only need to know Type 4):**
- Type 1: JDBC-ODBC bridge (legacy, removed Java 8)
- Type 2: Native-API driver (needs native libs)
- Type 3: Network protocol driver (middleware)
- **Type 4: Pure Java driver** — connects directly to DB; most common; `mysql-connector-j`, `postgresql`, `h2`

### 27.2 Setting Up JDBC

```xml
<!-- pom.xml — MySQL example -->
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <version>8.3.0</version>
</dependency>

<!-- PostgreSQL -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.7.1</version>
</dependency>

<!-- H2 — in-memory database, great for testing -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <version>2.2.224</version>
    <scope>test</scope>
</dependency>
```

### 27.3 The Seven Steps of JDBC

Every JDBC operation follows the same pattern:

```
1. Load driver (automatic in JDBC 4.0+ via ServiceLoader)
2. Get Connection
3. Create Statement / PreparedStatement
4. Execute query / update
5. Process ResultSet (for SELECT)
6. Close resources (in reverse order: ResultSet → Statement → Connection)
```

```java
// Step 2: Get Connection
// JDBC URL format: jdbc:<subprotocol>://<host>:<port>/<database>?<params>
String url  = "jdbc:mysql://localhost:3306/school?useSSL=false&serverTimezone=UTC";
String user = "root";
String pass = "secret";

try (Connection conn = DriverManager.getConnection(url, user, pass)) {
    // Connection auto-closed at end of try block

    DatabaseMetaData meta = conn.getMetaData();
    System.out.println("DB: " + meta.getDatabaseProductName()
                      + " " + meta.getDatabaseProductVersion());
    System.out.println("Driver: " + meta.getDriverName());
}
```

### 27.4 Statement vs PreparedStatement vs CallableStatement

**Never use Statement for user input — SQL Injection danger:**

```java
// ❌ VULNERABLE to SQL Injection!
String name = request.getParameter("name");  // attacker inputs: ' OR '1'='1
String sql = "SELECT * FROM users WHERE name = '" + name + "'";
// Resulting query: SELECT * FROM users WHERE name = '' OR '1'='1'
// Returns ALL rows! Attacker can also DROP TABLE, exfiltrate data, etc.
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);

// ✅ SAFE — PreparedStatement with parameters
String sql2 = "SELECT * FROM users WHERE name = ?";  // ? is a placeholder
PreparedStatement ps = conn.prepareStatement(sql2);
ps.setString(1, name);   // 1-indexed; escapes special characters automatically
ResultSet rs2 = ps.executeQuery();
// Even if name = "' OR '1'='1", it's treated as a literal string, not SQL
```

**PreparedStatement — full CRUD:**

```java
// CREATE
String insertSQL = "INSERT INTO students (name, email, grade, enroll_date) VALUES (?, ?, ?, ?)";
try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement ps = conn.prepareStatement(insertSQL, Statement.RETURN_GENERATED_KEYS)) {

    ps.setString(1, "Alice Johnson");
    ps.setString(2, "alice@university.edu");
    ps.setInt(3, 95);
    ps.setDate(4, Date.valueOf(LocalDate.now()));   // java.sql.Date

    int rowsAffected = ps.executeUpdate();  // returns number of rows changed
    System.out.println("Inserted " + rowsAffected + " row(s)");

    // Retrieve auto-generated keys
    try (ResultSet keys = ps.getGeneratedKeys()) {
        if (keys.next()) {
            long newId = keys.getLong(1);
            System.out.println("New student ID: " + newId);
        }
    }
}

// READ — iterate ResultSet
String selectSQL = "SELECT id, name, email, grade FROM students WHERE grade >= ?";
try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement ps = conn.prepareStatement(selectSQL)) {

    ps.setInt(1, 80);
    // Optionally set fetch size for large results:
    ps.setFetchSize(100);  // fetch 100 rows at a time from DB

    try (ResultSet rs = ps.executeQuery()) {
        // ResultSet starts BEFORE the first row; call next() to advance
        while (rs.next()) {
            long   id    = rs.getLong("id");         // by column name (preferred)
            String name  = rs.getString("name");
            String email = rs.getString("email");
            int    grade = rs.getInt(4);             // by column index (1-based)

            // Handling NULL values:
            // rs.getInt() returns 0 for NULL — check with wasNull()
            int score = rs.getInt("score");
            if (rs.wasNull()) { /* score was NULL in DB */ }

            // Or use getObject for nullable columns:
            Integer nullableGrade = (Integer) rs.getObject("grade");

            System.out.printf("ID=%d  %-20s  %s  Grade=%d%n", id, name, email, grade);
        }
    }
}

// UPDATE
String updateSQL = "UPDATE students SET grade = grade + ? WHERE id = ?";
try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement ps = conn.prepareStatement(updateSQL)) {
    ps.setInt(1, 5);     // add 5 to grade
    ps.setLong(2, 42L);  // student id 42
    int updated = ps.executeUpdate();
    System.out.println("Updated " + updated + " student(s)");
}

// DELETE
String deleteSQL = "DELETE FROM students WHERE grade < ? AND enroll_date < ?";
try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement ps = conn.prepareStatement(deleteSQL)) {
    ps.setInt(1, 60);
    ps.setDate(2, Date.valueOf(LocalDate.now().minusYears(5)));
    ps.executeUpdate();
}
```

### 27.5 Transactions — ACID Properties

A **transaction** is a sequence of operations treated as a single unit:
- **Atomic**: all succeed or all fail — no partial updates
- **Consistent**: database moves from one valid state to another
- **Isolated**: concurrent transactions don't interfere
- **Durable**: committed changes survive crashes

```java
Connection conn = DriverManager.getConnection(url, user, pass);
conn.setAutoCommit(false);   // Disable auto-commit — start manual transaction control
// By default, each statement is its own auto-committed transaction

try {
    // Operation 1: debit sender
    try (PreparedStatement debit = conn.prepareStatement(
            "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance >= ?")) {
        debit.setDouble(1, 500.00);
        debit.setLong(2, senderId);
        debit.setDouble(3, 500.00);  // ensure sufficient funds
        int rows = debit.executeUpdate();
        if (rows == 0) throw new IllegalStateException("Insufficient funds or account not found");
    }

    // Operation 2: credit receiver
    try (PreparedStatement credit = conn.prepareStatement(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?")) {
        credit.setDouble(1, 500.00);
        credit.setLong(2, receiverId);
        credit.executeUpdate();
    }

    // Operation 3: log the transaction
    try (PreparedStatement log = conn.prepareStatement(
            "INSERT INTO transfer_log (from_id, to_id, amount, ts) VALUES (?,?,?,?)")) {
        log.setLong(1, senderId);
        log.setLong(2, receiverId);
        log.setDouble(3, 500.00);
        log.setTimestamp(4, Timestamp.from(Instant.now()));
        log.executeUpdate();
    }

    conn.commit();   // All three operations succeeded — commit atomically
    System.out.println("Transfer successful");

} catch (Exception e) {
    try {
        conn.rollback();  // Any failure — undo EVERYTHING
        System.err.println("Transfer rolled back: " + e.getMessage());
    } catch (SQLException rollbackEx) {
        System.err.println("Rollback failed: " + rollbackEx);
    }
    throw e;  // re-throw so caller knows it failed

} finally {
    conn.setAutoCommit(true);  // Restore auto-commit
    conn.close();
}
```

**Savepoints — partial rollback:**
```java
conn.setAutoCommit(false);
Savepoint sp1 = conn.setSavepoint("AFTER_INSERT");
try {
    // more operations...
    conn.commit();
} catch (SQLException e) {
    conn.rollback(sp1);  // rollback only to savepoint, not entire transaction
    conn.commit();       // commit what was done before the savepoint
}
```

### 27.6 Batch Processing — Performance for Bulk Operations

```java
// Without batching: 1000 round-trips to DB = very slow
// With batching: 1 round-trip for every 500 rows = much faster

String insertSQL = "INSERT INTO events (name, category, timestamp) VALUES (?,?,?)";
try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement ps = conn.prepareStatement(insertSQL)) {

    conn.setAutoCommit(false);  // batch + transaction for speed and atomicity

    List<Event> events = generateEvents(50_000);
    int batchSize = 500;

    for (int i = 0; i < events.size(); i++) {
        Event e = events.get(i);
        ps.setString(1, e.getName());
        ps.setString(2, e.getCategory());
        ps.setTimestamp(3, Timestamp.from(e.getTimestamp()));
        ps.addBatch();  // add to current batch

        if ((i + 1) % batchSize == 0) {
            int[] results = ps.executeBatch();  // execute and clear batch
            ps.clearBatch();
            System.out.println("Inserted " + results.length + " rows");
        }
    }
    // Execute any remaining rows
    ps.executeBatch();
    conn.commit();
}
```

### 27.7 Connection Pooling — Production Best Practice

Opening a new database connection for every request is expensive (~20-100ms). A **connection pool** pre-creates connections and reuses them.

```xml
<!-- HikariCP — fastest connection pool -->
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.1.0</version>
</dependency>
```

```java
// Configure HikariCP
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/school");
config.setUsername("root");
config.setPassword("secret");
config.setMaximumPoolSize(20);         // max concurrent connections
config.setMinimumIdle(5);              // keep 5 idle connections ready
config.setConnectionTimeout(30_000);   // wait max 30s for a connection
config.setIdleTimeout(600_000);        // close connections idle > 10 minutes
config.setMaxLifetime(1_800_000);      // recycle connections after 30 minutes
config.setConnectionTestQuery("SELECT 1"); // heartbeat query to verify liveness

DataSource dataSource = new HikariDataSource(config);

// Use exactly like DriverManager, but much faster:
try (Connection conn = dataSource.getConnection()) {  // borrowed from pool
    // ... use connection
}  // connection returned to pool, NOT closed
```

---

## Chapter 28: Servlets & JSP

### 28.1 What is a Servlet?

A **Servlet** is a Java class that handles HTTP requests on a server. It's the foundation of all Java web frameworks — Spring MVC, Struts, JSF all build on top of the Servlet API.

**The Servlet Container** (Tomcat, Jetty, Undertow) manages the servlet lifecycle, handles threading (one thread per request), and provides the HTTP plumbing.

```
Browser ──HTTP Request──▶  Servlet Container (Tomcat)
                                │
                                ▼ matches URL pattern
                           Your Servlet.service()
                                │
                                ├── doGet()    ← GET requests
                                ├── doPost()   ← POST requests
                                ├── doPut()    ← PUT requests
                                └── doDelete() ← DELETE requests
                                │
                                ▼
Browser ◀──HTTP Response── write to HttpServletResponse
```

### 28.2 Servlet Lifecycle — In Detail

```
JVM Start
   │
   ▼
1. LOADING: Container loads the Servlet class (first request or eager init)
   │
   ▼
2. INSTANTIATION: Container calls no-arg constructor → one Servlet instance
   │           (Servlets are SINGLETONS — one instance, many threads!)
   ▼
3. INITIALIZATION: Container calls init(ServletConfig config) ONCE
   │           Use for: opening DB connections, loading config, warming caches
   ▼
4. SERVICE: For EVERY request → Container calls service(req, res)
   │       service() dispatches to doGet() / doPost() etc.
   │       IMPORTANT: Multiple threads call this concurrently!
   │       Never store request-specific data in instance fields!
   ▼
5. DESTRUCTION: Container calls destroy() ONCE before unloading
              Use for: closing connections, flushing caches, cleanup
```

```java
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.*;
import java.sql.*;

@WebServlet(
    name        = "StudentServlet",
    urlPatterns = {"/students", "/students/*"},
    loadOnStartup = 1   // initialize at startup (not on first request)
)
public class StudentServlet extends HttpServlet {

    // ⚠️ Instance variables are shared across ALL threads — only put thread-safe things here
    private DataSource dataSource;
    private static final Logger log = Logger.getLogger(StudentServlet.class.getName());

    @Override
    public void init(ServletConfig config) throws ServletException {
        super.init(config);   // MUST call super.init() to store ServletConfig
        // Context parameters from web.xml:
        String dbUrl = config.getServletContext().getInitParameter("dbUrl");
        dataSource = createPool(dbUrl);
        log.info("StudentServlet initialized");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // Every request creates new req and res — these are THREAD LOCAL automatically
        String pathInfo = req.getPathInfo();   // "/42" for /students/42

        if (pathInfo == null || "/".equals(pathInfo)) {
            // List all students
            listStudents(req, res);
        } else {
            // Get single student by ID
            long id = Long.parseLong(pathInfo.substring(1));
            getStudent(id, req, res);
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        // Set character encoding BEFORE reading parameters
        req.setCharacterEncoding("UTF-8");

        String name  = req.getParameter("name");   // form field named "name"
        String email = req.getParameter("email");
        String gradeStr = req.getParameter("grade");

        // Validation
        if (name == null || name.isBlank()) {
            res.sendError(HttpServletResponse.SC_BAD_REQUEST, "Name is required");
            return;
        }

        try {
            int grade = Integer.parseInt(gradeStr);
            Student saved = saveToDatabase(name, email, grade);
            // Post-Redirect-Get pattern: redirect after POST to avoid duplicate submission on refresh
            res.sendRedirect(req.getContextPath() + "/students/" + saved.getId());
        } catch (NumberFormatException e) {
            res.sendError(HttpServletResponse.SC_BAD_REQUEST, "Invalid grade");
        }
    }

    private void listStudents(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT * FROM students ORDER BY name");
             ResultSet rs = ps.executeQuery()) {

            List<Student> students = new ArrayList<>();
            while (rs.next()) students.add(mapRow(rs));

            req.setAttribute("students", students);   // put data in request scope
            // Forward to JSP view — server-side redirect; URL stays the same
            req.getRequestDispatcher("/WEB-INF/views/students/list.jsp").forward(req, res);

        } catch (SQLException e) {
            throw new ServletException("Database error", e);
        }
    }

    @Override
    public void destroy() {
        // Cleanup — close pool, etc.
        log.info("StudentServlet destroyed");
    }
}
```

### 28.3 Request, Response & Parameters

```java
// ── HttpServletRequest — reading the incoming request ─────────
String method       = req.getMethod();         // "GET", "POST", "PUT", "DELETE"
String uri          = req.getRequestURI();     // "/app/students/42"
String contextPath  = req.getContextPath();    // "/app" (context root)
String servletPath  = req.getServletPath();    // "/students"
String pathInfo     = req.getPathInfo();       // "/42"
String queryString  = req.getQueryString();    // "page=2&sort=name"
String remoteAddr   = req.getRemoteAddr();     // client IP

// Query/form parameters (GET query string + POST form body)
String name         = req.getParameter("name");       // single value
String[] hobbies    = req.getParameterValues("hobby"); // multiple values (checkboxes)
Map<String,String[]> all = req.getParameterMap();      // all params

// Request attributes (set/get within same request)
req.setAttribute("result", computedResult);
Object result = req.getAttribute("result");
req.removeAttribute("result");

// Headers
String accept       = req.getHeader("Accept");
String contentType  = req.getContentType();
String auth         = req.getHeader("Authorization");
Enumeration<String> headerNames = req.getHeaderNames();

// Reading request body (for JSON/XML REST APIs)
String body = req.getReader().lines().collect(Collectors.joining());
// Or: InputStream body = req.getInputStream();

// ── HttpServletResponse — building the response ───────────────
res.setStatus(HttpServletResponse.SC_OK);          // 200
res.setStatus(HttpServletResponse.SC_CREATED);     // 201
res.setStatus(HttpServletResponse.SC_NOT_FOUND);   // 404

res.setContentType("application/json");
res.setContentType("text/html;charset=UTF-8");
res.setCharacterEncoding("UTF-8");
res.setHeader("Cache-Control", "no-cache, no-store");
res.setHeader("X-Request-ID", UUID.randomUUID().toString());
res.addCookie(new Cookie("sessionToken", token));

// Send JSON response
res.setContentType("application/json");
res.setStatus(200);
PrintWriter out = res.getWriter();
out.print("{\"id\":42, \"name\":\"Alice\"}");
// NEVER call out.flush() or out.close() explicitly — container handles it

// Redirect (tells browser to make a NEW request)
res.sendRedirect("/login");                        // absolute path
res.sendRedirect(req.getContextPath() + "/home");  // context-relative

// Error response
res.sendError(404, "Student not found");
res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
```

### 28.4 Session Management

HTTP is stateless — each request is independent. Sessions add state.

```java
// ── HttpSession — server-side session ────────────────────────
// Get session (create if not exists):
HttpSession session = req.getSession();
// Get session only if it already exists (returns null if no session):
HttpSession session2 = req.getSession(false);

// Store data in session
session.setAttribute("user", loggedInUser);
session.setAttribute("cart", new ShoppingCart());

// Retrieve
User user = (User) session.getAttribute("user");
ShoppingCart cart = (ShoppingCart) session.getAttribute("cart");

// Remove
session.removeAttribute("cart");

// Session properties
String sessionId = session.getId();          // UUID-like identifier
long created     = session.getCreationTime(); // milliseconds since epoch
long lastAccess  = session.getLastAccessedTime();
boolean isNew    = session.isNew();           // true if created this request

// Timeout
session.setMaxInactiveInterval(30 * 60);     // seconds; -1 = never expire

// Invalidate on logout
session.invalidate();   // removes all attributes and invalidates session ID

// ── Cookies ───────────────────────────────────────────────────
Cookie cookie = new Cookie("theme", "dark");
cookie.setMaxAge(7 * 24 * 3600);   // 7 days; 0 = delete; -1 = session cookie
cookie.setPath("/");                // available to entire app
cookie.setDomain("example.com");
cookie.setHttpOnly(true);           // prevents JavaScript access (XSS protection)
cookie.setSecure(true);             // HTTPS only
cookie.setAttribute("SameSite", "Strict");  // CSRF protection (Servlet 6.0+)
res.addCookie(cookie);

// Reading cookies
Cookie[] cookies = req.getCookies();  // null if no cookies
if (cookies != null) {
    for (Cookie c : cookies) {
        if ("theme".equals(c.getName())) {
            String theme = c.getValue();
        }
    }
}
```

### 28.5 Filters — Cross-Cutting Concerns

Filters intercept requests/responses before/after servlets. Perfect for logging, authentication, CORS, compression.

```java
@WebFilter(urlPatterns = "/*", asyncSupported = true)
@WebServlet(loadOnStartup = -1)
public class SecurityFilter implements Filter {

    @Override
    public void init(FilterConfig config) throws ServletException {
        // One-time setup
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest  req = (HttpServletRequest)  request;
        HttpServletResponse res = (HttpServletResponse) response;

        // ── Before Servlet ──────────────────────────
        long startTime = System.currentTimeMillis();
        String path = req.getRequestURI();

        // Add security headers
        res.setHeader("X-Content-Type-Options", "nosniff");
        res.setHeader("X-Frame-Options", "DENY");
        res.setHeader("X-XSS-Protection", "1; mode=block");

        // Check authentication (skip public paths)
        if (!isPublicPath(path)) {
            HttpSession session = req.getSession(false);
            if (session == null || session.getAttribute("user") == null) {
                res.sendRedirect(req.getContextPath() + "/login");
                return;   // stop processing — don't call chain.doFilter()
            }
        }

        // ── Pass to next filter / servlet ──────────
        chain.doFilter(request, response);

        // ── After Servlet (response is being written) ──
        long duration = System.currentTimeMillis() - startTime;
        log.info(req.getMethod() + " " + path + " → " + res.getStatus() + " (" + duration + "ms)");
    }

    private boolean isPublicPath(String path) {
        return path.endsWith("/login") || path.endsWith("/register")
            || path.contains("/static/") || path.contains("/css/");
    }
}

// Multiple filters execute in order defined in web.xml or by @WebFilter order
// Filter chain: F1 → F2 → F3 → Servlet → F3 → F2 → F1 (unwinds like a stack)
```

### 28.6 JSP — JavaServer Pages

JSP allows embedding Java in HTML. The Servlet container compiles JSP into a Servlet class automatically. Best practice: use JSP only for display (no business logic) with JSTL and EL.

```jsp
<%-- This is a JSP comment — not sent to browser --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.time.LocalDate" %>

<%-- JSTL tag libraries — much cleaner than scriptlets --%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt"  prefix="fmt" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fn"   prefix="fn" %>

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student List</title>
</head>
<body>

<%-- Expression Language (EL) — read attributes from scopes --%>
<%-- ${expr} searches: page → request → session → application scope --%>
<h1>Welcome, ${sessionScope.user.name}!</h1>
<p>Context: ${pageContext.request.contextPath}</p>

<%-- c:if — conditional rendering --%>
<c:if test="${empty students}">
    <p class="empty">No students found.</p>
</c:if>

<%-- c:choose — like switch/if-else --%>
<c:choose>
    <c:when test="${sessionScope.user.role == 'ADMIN'}">
        <a href="<c:url value='/admin'/>">Admin Panel</a>
    </c:when>
    <c:when test="${sessionScope.user.role == 'TEACHER'}">
        <a href="<c:url value='/grades'/>">Enter Grades</a>
    </c:when>
    <c:otherwise>
        <p>Student portal</p>
    </c:otherwise>
</c:choose>

<%-- c:forEach — iterate collections --%>
<table>
    <thead><tr><th>#</th><th>Name</th><th>Email</th><th>Grade</th></tr></thead>
    <tbody>
    <c:forEach var="student" items="${requestScope.students}" varStatus="status">
        <tr class="${status.index % 2 == 0 ? 'even' : 'odd'}">
            <td>${status.count}</td>       <%-- 1-based count --%>
            <td>
                <c:url value="/students/${student.id}" var="studentUrl"/>
                <a href="${studentUrl}"><c:out value="${student.name}"/></a>
                <%-- c:out escapes HTML entities — prevents XSS! --%>
            </td>
            <td>${fn:escapeXml(student.email)}</td>
            <td>
                <fmt:formatNumber value="${student.grade}" pattern="##.#"/>%
            </td>
        </tr>
    </c:forEach>
    </tbody>
</table>

<%-- c:url — context-aware URL generation; handles encoding --%>
<a href="<c:url value='/students/new'/>">Add Student</a>

<%-- Pagination --%>
<c:forEach begin="1" end="${totalPages}" var="page">
    <a href="<c:url value='/students?page=${page}'/>"
       class="${page == currentPage ? 'active' : ''}">${page}</a>
</c:forEach>

<%-- fmt: formatting --%>
<fmt:formatDate value="${student.enrollDate}" pattern="dd MMM yyyy"/>
<fmt:formatNumber value="${averageGrade}" type="percent" minFractionDigits="1"/>

<%-- Scriptlet (avoid — mixes Java in HTML; only shown for completeness) --%>
<%
    // This is a scriptlet — avoid in real code; use JSTL instead
    String title = (String) request.getAttribute("title");
    if (title != null) {
%>
    <h2><%= title %></h2>
<% } %>

</body>
</html>
```

**JSP Scopes and Implicit Objects:**
```
Scope         Object           Duration
─────────────────────────────────────────────────
page          pageContext      Current JSP page only
request       request          Single HTTP request
session       session          User's session (across requests)
application   application      Entire web app lifetime

Implicit variables in EL:
  ${param.name}                request.getParameter("name")
  ${paramValues.hobby}         request.getParameterValues("hobby")
  ${header['User-Agent']}      request.getHeader("User-Agent")
  ${cookie.theme.value}        cookie named "theme"
  ${initParam.dbUrl}           context init parameter
  ${pageContext.request.method} "GET" or "POST"
```

---

## Chapter 29: Hibernate & JPA

### 29.1 The Object-Relational Impedance Mismatch

Relational databases store data in **tables with rows and columns**. Java models data as **objects with fields and relationships**. This mismatch is called the **Object-Relational Impedance Mismatch**:

```
Java Object World          vs.     Relational World
────────────────────────           ────────────────
Objects with references            Foreign keys
Inheritance hierarchies            No native inheritance
Collections of objects             JOIN tables
Object identity (==)               Primary keys
Polymorphism                       No direct equivalent
```

**ORM (Object-Relational Mapping)** automates the translation. You define the mapping once; the ORM generates the SQL.

**JPA (Jakarta Persistence API)** is the specification. **Hibernate** is the most popular implementation. Spring Data JPA sits on top of both and adds further automation.

```
Your Code
    │
    ▼
Spring Data JPA (Repository pattern, query generation)
    │
    ▼
JPA API (javax/jakarta.persistence.*)         ← The standard spec
    │
    ▼
Hibernate (EntityManager, Session, HQL/JPQL)  ← The implementation
    │
    ▼
JDBC
    │
    ▼
Database
```

### 29.2 Entity Annotations — Complete Reference

```java
import jakarta.persistence.*;
import java.time.*;
import java.math.BigDecimal;

@Entity                          // Marks class as a JPA entity (maps to a table)
@Table(
    name = "employees",          // table name (default: class name)
    schema = "hr",               // database schema
    uniqueConstraints = {
        @UniqueConstraint(name = "uk_email", columnNames = {"email"}),
        @UniqueConstraint(name = "uk_emp_no", columnNames = {"department_id", "employee_number"})
    },
    indexes = {
        @Index(name = "idx_last_name", columnList = "last_name"),
        @Index(name = "idx_dept_hire", columnList = "department_id, hire_date DESC")
    }
)
public class Employee {

    // ── Primary Key Strategies ────────────────────────────────
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    // IDENTITY: auto-increment by DB (MySQL AUTO_INCREMENT, PostgreSQL SERIAL)
    // SEQUENCE: uses DB sequence (PostgreSQL, Oracle — allows batch optimization)
    // TABLE:    uses a special table (portable but slow; avoid)
    // AUTO:     JPA picks based on dialect (default)
    // UUID:     @GeneratedValue(strategy = GenerationType.UUID)  Java 17+
    private Long id;

    // ── Column Mapping ─────────────────────────────────────────
    @Column(
        name       = "first_name",    // column name (default: field name)
        nullable   = false,           // NOT NULL constraint
        length     = 50,              // VARCHAR length (only for String)
        updatable  = true,            // include in UPDATE statements
        insertable = true             // include in INSERT statements
    )
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 100)
    private String lastName;

    @Column(unique = true, nullable = false, length = 200)
    private String email;

    @Column(precision = 10, scale = 2)  // DECIMAL(10,2) — for monetary amounts
    private BigDecimal salary;

    @Column(columnDefinition = "TEXT")  // raw SQL column definition
    private String notes;

    @Column(name = "is_active", nullable = false)
    private boolean active = true;

    // ── Temporal Types ─────────────────────────────────────────
    @Column(name = "hire_date")
    private LocalDate hireDate;          // DATE in SQL

    @Column(name = "last_login")
    private LocalDateTime lastLogin;     // TIMESTAMP in SQL

    @Column(name = "created_at", updatable = false)
    private OffsetDateTime createdAt;    // TIMESTAMP WITH TIMEZONE

    // Automatically set timestamps:
    @PrePersist
    void onPersist() { createdAt = OffsetDateTime.now(); }

    @PreUpdate
    void onUpdate() { lastLogin = LocalDateTime.now(); }

    // ── Enum Mapping ───────────────────────────────────────────
    @Enumerated(EnumType.STRING)    // Store "FULL_TIME" not 0, 1, 2
    @Column(nullable = false)
    private EmploymentType type;    // ORDINAL is the default — fragile; always use STRING

    // ── Not Persisted ──────────────────────────────────────────
    @Transient                       // not mapped to any column
    private String computedFullName;

    // ── LOB — Large Objects ────────────────────────────────────
    @Lob                             // maps to CLOB/TEXT or BLOB/BYTEA
    @Column(name = "profile_picture")
    private byte[] profilePicture;  // BLOB

    @Lob
    @Column(name = "resume")
    private String resume;           // CLOB / TEXT

    // ── Version for Optimistic Locking ─────────────────────────
    @Version
    private Long version;            // JPA increments this on each UPDATE
    // Prevents lost updates: if two users load version 5 and both try to save,
    // first save succeeds (→ version 6), second throws OptimisticLockException

    // Constructors, getters, setters...
    // JPA requires a no-arg constructor (can be protected):
    protected Employee() { }

    public Employee(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName  = lastName;
        this.email     = email;
    }
}
```

### 29.3 Relationships — The Most Critical Part

**@ManyToOne / @OneToMany — the most common:**

```java
// Many employees belong to one department
@Entity
@Table(name = "departments")
public class Department {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    // mappedBy = field in Employee that owns the relationship
    // The "owner" side has the FK column; mappedBy side is inverse
    @OneToMany(
        mappedBy    = "department",
        cascade     = CascadeType.ALL,   // operations cascade to employees
        fetch       = FetchType.LAZY,    // LAZY = load on access; EAGER = load immediately
        orphanRemoval = true             // remove employees when removed from this list
    )
    private List<Employee> employees = new ArrayList<>();

    // Helper methods to keep both sides consistent (bi-directional relationship)
    public void addEmployee(Employee emp) {
        employees.add(emp);
        emp.setDepartment(this);
    }
    public void removeEmployee(Employee emp) {
        employees.remove(emp);
        emp.setDepartment(null);
    }
}

@Entity
public class Employee {
    // ... other fields ...

    @ManyToOne(fetch = FetchType.LAZY)   // LAZY for @ManyToOne prevents N+1 problem
    @JoinColumn(
        name = "department_id",           // FK column in employees table
        nullable = false,
        foreignKey = @ForeignKey(name = "fk_employee_department")
    )
    private Department department;
}
```

**@OneToOne:**
```java
@Entity
public class User {
    @Id @GeneratedValue private Long id;
    private String username;

    // One user has one profile
    @OneToOne(
        cascade = CascadeType.ALL,
        fetch   = FetchType.LAZY,
        optional = false   // profile is required (NOT NULL FK)
    )
    @JoinColumn(name = "profile_id", unique = true)
    private UserProfile profile;
}

@Entity
public class UserProfile {
    @Id @GeneratedValue private Long id;
    private String bio;
    private String avatarUrl;

    // Inverse side (no FK here — FK is in User table)
    @OneToOne(mappedBy = "profile")
    private User user;
}
```

**@ManyToMany:**
```java
@Entity
public class Student {
    @Id @GeneratedValue private Long id;
    private String name;

    @ManyToMany
    @JoinTable(
        name = "student_course_enrollments",      // join table name
        joinColumns        = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id"),
        uniqueConstraints  = @UniqueConstraint(columnNames = {"student_id", "course_id"})
    )
    private Set<Course> courses = new HashSet<>();
}

@Entity
public class Course {
    @Id @GeneratedValue private Long id;
    private String title;

    @ManyToMany(mappedBy = "courses")  // inverse side
    private Set<Student> students = new HashSet<>();
}
```

**Cascade Types — when operations propagate:**
```
CascadeType.PERSIST  → save child when parent is saved
CascadeType.MERGE    → update child when parent is merged (updated)
CascadeType.REMOVE   → delete child when parent is deleted  ← BE CAREFUL
CascadeType.REFRESH  → refresh child when parent is refreshed
CascadeType.DETACH   → detach child when parent is detached
CascadeType.ALL      → all of the above

Use ALL for parent-owns-child (Department→Employee).
NEVER use ALL for @ManyToMany — deleting a Course would delete all Students!
```

**FetchType — when to load related data:**
```
EAGER: Load immediately with the parent (1 JOIN query)
  Default for: @ManyToOne, @OneToOne
  Danger: loading a User always loads their entire Department, Address, etc.

LAZY: Load only when the getter is called (separate query on first access)
  Default for: @OneToMany, @ManyToMany
  Best practice: use LAZY everywhere, override with JOIN FETCH in queries

N+1 Problem (the most common Hibernate performance bug):
  List<Department> depts = repository.findAll();  // 1 query: SELECT * FROM departments
  for (Department d : depts) {
      d.getEmployees().size();  // N queries! One per department!
  }
  // Total: N+1 database round-trips

Fix with JOIN FETCH:
  @Query("SELECT d FROM Department d LEFT JOIN FETCH d.employees WHERE d.active = true")
  List<Department> findAllWithEmployees();
  // 1 query: SELECT * FROM departments d LEFT JOIN employees e ON e.dept_id = d.id
```

### 29.4 Inheritance Mapping Strategies

```java
// Strategy 1: SINGLE_TABLE — all subclasses in one table (fastest queries, nullable columns)
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "account_type", discriminatorType = DiscriminatorType.STRING)
public abstract class BankAccount {
    @Id @GeneratedValue private Long id;
    private String owner;
    private BigDecimal balance;
}

@Entity
@DiscriminatorValue("CHECKING")
public class CheckingAccount extends BankAccount {
    private double overdraftLimit;    // NULL for savings accounts
}

@Entity
@DiscriminatorValue("SAVINGS")
public class SavingsAccount extends BankAccount {
    private double interestRate;      // NULL for checking accounts
}
// Table: bank_accounts(id, owner, balance, account_type, overdraft_limit, interest_rate)

// Strategy 2: TABLE_PER_CLASS — each class has its own complete table (no JOINs but slow polymorphism)
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)

// Strategy 3: JOINED — normalized (separate tables, JOINed when querying)
@Inheritance(strategy = InheritanceType.JOINED)
// Tables: bank_accounts(id, owner, balance) + checking_accounts(id, overdraft_limit) + ...
// Cleanest design but requires JOINs
```

### 29.5 Spring Data JPA — The Full Picture

Spring Data JPA auto-generates repository implementations at startup:

```java
// Extend JpaRepository<EntityType, PrimaryKeyType>
// You get 18+ CRUD + pagination methods for free
public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // ═══ Derived Query Methods ════════════════════════════════
    // Spring parses the method name and generates JPQL automatically
    // Syntax: findBy<Property>[<Condition>][And/Or<Property>...]

    List<Employee> findByLastName(String lastName);
    List<Employee> findByLastNameIgnoreCase(String lastName);
    List<Employee> findByFirstNameContaining(String fragment);        // LIKE %fragment%
    List<Employee> findByFirstNameStartingWith(String prefix);        // LIKE prefix%
    List<Employee> findByFirstNameEndingWith(String suffix);          // LIKE %suffix
    List<Employee> findByFirstNameLike(String pattern);               // custom LIKE
    Optional<Employee> findByEmail(String email);

    List<Employee> findBySalaryGreaterThan(BigDecimal min);
    List<Employee> findBySalaryBetween(BigDecimal min, BigDecimal max);
    List<Employee> findByHireDateAfter(LocalDate date);
    List<Employee> findByHireDateBefore(LocalDate date);
    List<Employee> findByHireDateBetween(LocalDate start, LocalDate end);

    List<Employee> findByActiveTrue();
    List<Employee> findByActiveFalse();
    List<Employee> findByDepartmentId(Long deptId);             // traverse relationships
    List<Employee> findByDepartmentName(String deptName);       // JOIN automatically
    List<Employee> findByDepartmentNameAndActiveTrue(String deptName);

    boolean existsByEmail(String email);
    long    countByDepartmentId(Long deptId);
    long    countByActiveTrue();

    // Sorting
    List<Employee> findByActiveTrueOrderByLastNameAsc();
    List<Employee> findByDepartmentIdOrderBySalaryDesc(Long deptId);

    // Limiting results
    List<Employee>    findTop5ByOrderBySalaryDesc();             // top 5 by salary
    Optional<Employee> findFirstByDepartmentIdOrderBySalaryDesc(Long deptId); // highest paid in dept

    // Pagination
    Page<Employee>  findByActive(boolean active, Pageable pageable);
    Slice<Employee> findByDepartmentId(Long deptId, Pageable pageable);  // no total count

    // ═══ JPQL Queries ═════════════════════════════════════════
    // JPQL operates on entities/fields (not tables/columns)
    @Query("SELECT e FROM Employee e WHERE e.salary > :minSalary AND e.department.name = :dept")
    List<Employee> findHighEarnersInDept(
        @Param("minSalary") BigDecimal minSalary,
        @Param("dept") String deptName);

    // JOIN FETCH — solve N+1 problem
    @Query("SELECT DISTINCT d FROM Department d LEFT JOIN FETCH d.employees WHERE d.active = true")
    List<Department> findAllWithEmployees();

    // Projections — return only needed columns (faster, less memory)
    @Query("SELECT new com.example.dto.EmployeeSummary(e.id, e.firstName, e.lastName, e.salary) " +
           "FROM Employee e WHERE e.department.id = :deptId")
    List<EmployeeSummary> findSummariesByDept(@Param("deptId") Long deptId);

    // Aggregate queries
    @Query("SELECT e.department.name, AVG(e.salary), COUNT(e) FROM Employee e GROUP BY e.department.name")
    List<Object[]> getStatsByDepartment();

    // Modifying queries (UPDATE/DELETE) — must have @Modifying and @Transactional
    @Modifying
    @Transactional
    @Query("UPDATE Employee e SET e.active = false WHERE e.department.id = :deptId")
    int deactivateByDepartment(@Param("deptId") Long deptId);

    @Modifying
    @Transactional
    @Query("DELETE FROM Employee e WHERE e.active = false AND e.hireDat < :cutoff")
    int deleteInactiveOlderThan(@Param("cutoff") LocalDate cutoff);

    // ═══ Native SQL Queries ════════════════════════════════════
    // When JPQL isn't enough (window functions, CTEs, DB-specific features)
    @Query(value = """
        SELECT e.*, d.name AS dept_name,
               RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS salary_rank
        FROM employees e
        JOIN departments d ON d.id = e.department_id
        WHERE e.active = 1
        """,
        countQuery = "SELECT COUNT(*) FROM employees WHERE active = 1",
        nativeQuery = true)
    Page<Object[]> findWithSalaryRanking(Pageable pageable);

    // ═══ Specifications (Dynamic Queries) ═════════════════════
    // Extend JpaSpecificationExecutor<Employee> on the repository
    // Then: employeeRepo.findAll(spec) where spec is a Specification<Employee>
}

// Extend both:
public interface EmployeeRepository
        extends JpaRepository<Employee, Long>,
                JpaSpecificationExecutor<Employee> { ... }

// Build Specifications dynamically:
public class EmployeeSpec {
    public static Specification<Employee> hasName(String name) {
        return (root, query, cb) ->
            name == null ? null : cb.like(cb.lower(root.get("lastName")),
                                          "%" + name.toLowerCase() + "%");
    }

    public static Specification<Employee> inDepartment(Long deptId) {
        return (root, query, cb) ->
            deptId == null ? null : cb.equal(root.get("department").get("id"), deptId);
    }

    public static Specification<Employee> salaryRange(BigDecimal min, BigDecimal max) {
        return (root, query, cb) -> {
            if (min == null && max == null) return null;
            if (min == null) return cb.lessThanOrEqualTo(root.get("salary"), max);
            if (max == null) return cb.greaterThanOrEqualTo(root.get("salary"), min);
            return cb.between(root.get("salary"), min, max);
        };
    }
}

// Use dynamically:
Specification<Employee> spec = Specification
    .where(EmployeeSpec.hasName(searchName))
    .and(EmployeeSpec.inDepartment(deptFilter))
    .and(EmployeeSpec.salaryRange(minSal, maxSal));
Page<Employee> results = employeeRepo.findAll(spec, PageRequest.of(0, 20));
```

### 29.6 Pagination and Sorting

```java
// Pageable carries page number (0-based), page size, and sorting
Pageable page1 = PageRequest.of(0, 10);  // first page, 10 items
Pageable sorted = PageRequest.of(0, 10, Sort.by("lastName").ascending()
                                              .and(Sort.by("salary").descending()));
Pageable multiSort = PageRequest.of(0, 10,
    Sort.by(Sort.Order.asc("department.name"),
            Sort.Order.desc("salary"),
            Sort.Order.asc("lastName")));

// Page<T> — includes total count (requires COUNT query)
Page<Employee> page = repository.findByActive(true, sorted);
page.getContent();         // List<Employee> for this page
page.getTotalElements();   // total matching employees
page.getTotalPages();      // total pages
page.getNumber();          // current page (0-based)
page.getSize();            // page size
page.hasNext();            // is there a next page?
page.hasPrevious();
page.isFirst();
page.isLast();
page.nextPageable();       // Pageable for next page

// Slice<T> — like Page but no total count (cheaper; good for infinite scroll)
Slice<Employee> slice = repository.findByDepartmentId(deptId, page1);
slice.hasNext();           // whether there is a next slice (uses size+1 trick)
// Slice does NOT know the total; use when you only need "has more"
```

---

# PART IV — SPRING ECOSYSTEM

---

## Chapter 30: Spring Core — IoC & DI

### 30.1 The Problem Spring Solves

Consider building a service that depends on a repository and a cache:

```java
// ❌ Tightly coupled — hard to test, hard to change
public class OrderService {
    // Hard-wired dependencies — can never swap implementations
    private final OrderRepository repo    = new MySqlOrderRepository();
    private final CacheService    cache   = new RedisCacheService();
    private final EmailService    emailer = new SmtpEmailService();

    public Order placeOrder(Cart cart) { ... }
}
// To test OrderService, you MUST have a running MySQL, Redis, and SMTP server.
// To switch from Redis to Memcached, you must edit OrderService.
```

**Inversion of Control (IoC)**: instead of an object creating its own dependencies, an external entity (the IoC container) creates them and hands them in. Control over object creation is *inverted* — from the object itself to the container.

**Dependency Injection (DI)**: the specific mechanism — dependencies are *injected* (given) to an object rather than the object pulling them.

```java
// ✅ Loosely coupled — depends on interfaces, not implementations
public class OrderService {
    private final OrderRepository repo;    // interface
    private final CacheService    cache;   // interface
    private final EmailService    emailer; // interface

    // Constructor injection — Spring provides the implementations
    public OrderService(OrderRepository repo, CacheService cache, EmailService emailer) {
        this.repo    = repo;
        this.cache   = cache;
        this.emailer = emailer;
    }
}
// To test: inject mock implementations — no real DB/cache/email needed
// To switch Redis → Memcached: change one Spring configuration line
```

### 30.2 The ApplicationContext — Spring's IoC Container

```java
// Java-based configuration (modern approach)
@Configuration
@ComponentScan(basePackages = "com.example")
@PropertySource("classpath:application.properties")
public class AppConfig {

    // @Bean method — Spring calls this, stores the result as a managed bean
    @Bean
    @Scope("singleton")   // default — one instance per container (shared)
    public DataSource dataSource(@Value("${db.url}") String url,
                                 @Value("${db.user}") String user,
                                 @Value("${db.pass}") String pass) {
        HikariConfig cfg = new HikariConfig();
        cfg.setJdbcUrl(url);
        cfg.setUsername(user);
        cfg.setPassword(pass);
        cfg.setMaximumPoolSize(20);
        return new HikariDataSource(cfg);
    }

    @Bean
    public OrderRepository orderRepository(DataSource ds) {
        return new JdbcOrderRepository(ds);  // Spring injects dataSource automatically
    }

    // @Scope prototype — new instance every time the bean is requested
    @Bean
    @Scope("prototype")
    public OrderProcessor orderProcessor() {
        return new OrderProcessor();
    }
}

// XML configuration (legacy — rarely used in new code)
// <beans><bean id="dataSource" class="...HikariDataSource"><property name="jdbcUrl" value="${db.url}"/></bean></beans>

// Bootstrap the container:
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
OrderService svc = ctx.getBean(OrderService.class);

// Spring Boot does all this automatically based on classpath and @SpringBootApplication
```

### 30.3 Component Stereotypes — Auto-Discovery

Instead of declaring every bean in a `@Configuration` class, annotate your classes and Spring finds them via `@ComponentScan`:

```java
// @Component — generic Spring-managed component
@Component
public class TaxCalculator {
    public double calculate(double amount, String region) { ... }
}

// @Service — business logic layer
// (same as @Component; adds semantic meaning for developers and AOP advice)
@Service
@Transactional   // all methods participate in transactions by default
public class OrderService {
    private final OrderRepository orderRepo;
    private final InventoryService inventory;
    private final NotificationService notifier;

    // Constructor injection — preferred: immutable, easy to test, clear dependencies
    // @Autowired is optional when there is exactly one constructor (Spring 4.3+)
    public OrderService(OrderRepository orderRepo,
                        InventoryService inventory,
                        NotificationService notifier) {
        this.orderRepo  = orderRepo;
        this.inventory  = inventory;
        this.notifier   = notifier;
    }

    public Order placeOrder(Long customerId, List<CartItem> items) {
        // Business logic here
        inventory.reserve(items);
        Order order = orderRepo.save(new Order(customerId, items));
        notifier.sendConfirmation(order);
        return order;
    }
}

// @Repository — data access layer
// Translates DB exceptions (SQLException, HibernateException) to Spring DataAccessException hierarchy
@Repository
public class JpaOrderRepository implements OrderRepository {
    @PersistenceContext
    private EntityManager em;

    @Override
    public Order save(Order order) {
        if (order.getId() == null) em.persist(order);
        else order = em.merge(order);
        return order;
    }
}

// @Controller — Spring MVC controller (see Chapter 33)
@Controller
@RequestMapping("/orders")
public class OrderController { ... }

// @RestController — @Controller + @ResponseBody (see Chapter 34)
@RestController
@RequestMapping("/api/orders")
public class OrderApiController { ... }
```

### 30.4 Dependency Injection — Three Styles Compared

```java
@Service
public class UserService {

    // ────────────────────────────────────────────────────────
    // STYLE 1: Constructor Injection (RECOMMENDED)
    // ────────────────────────────────────────────────────────
    private final UserRepository repo;
    private final EmailService   emailer;

    public UserService(UserRepository repo, EmailService emailer) {
        // Dependencies are given at construction time — object is always fully initialized
        // final fields — dependencies can't change after construction (immutable)
        // Easy to test — just new UserService(mockRepo, mockEmail) in tests
        // Circular dependency → detected at startup (Spring throws BeanCurrentlyInCreationException)
        this.repo    = repo;
        this.emailer = emailer;
    }

    // ────────────────────────────────────────────────────────
    // STYLE 2: Setter Injection (use for OPTIONAL dependencies)
    // ────────────────────────────────────────────────────────
    private MetricsService metrics;  // optional — application works without it

    @Autowired(required = false)   // inject if bean exists; otherwise leave null
    public void setMetrics(MetricsService metrics) {
        this.metrics = metrics;
    }

    // ────────────────────────────────────────────────────────
    // STYLE 3: Field Injection (AVOID in production code)
    // ────────────────────────────────────────────────────────
    @Autowired
    private AuditService audit;
    // Problems:
    // 1. Can't use final — field might change
    // 2. Hard to test — must use Spring test context or Mockito @InjectMocks
    // 3. Hidden dependencies — no constructor documenting what's needed
    // 4. NullPointerException if used before Spring injects (e.g., in field initializer)
    // OK for: quick prototypes, test classes with @SpringBootTest
}
```

### 30.5 Handling Multiple Implementations

```java
// Scenario: two NotificationService implementations
@Component("emailNotifier")
public class EmailNotificationService implements NotificationService {
    @Override public void send(String msg) { /* email */ }
}

@Component("smsNotifier")
@Primary   // used by default when @Autowired without qualifier
public class SmsNotificationService implements NotificationService {
    @Override public void send(String msg) { /* SMS */ }
}

// In a service — gets the @Primary one (SmsNotificationService)
@Service
public class AlertService {
    @Autowired
    private NotificationService notifier;  // gets SmsNotificationService

    @Autowired
    @Qualifier("emailNotifier")   // override: get the specific one by name
    private NotificationService emailNotifier;

    // Or inject ALL implementations as a List:
    @Autowired
    private List<NotificationService> allNotifiers;  // [emailNotifier, smsNotifier]
    // Send to all channels: allNotifiers.forEach(n -> n.send(message));

    // Or inject as a Map (bean name → bean):
    @Autowired
    private Map<String, NotificationService> notifiers;
    // notifiers.get("smsNotifier").send(message);
}
```

### 30.6 @Value and @ConfigurationProperties

```java
@Component
public class AppSettings {

    // Simple value injection
    @Value("${app.name}")                  // from application.properties
    private String appName;

    @Value("${app.timeout:30}")            // with default 30 if missing
    private int timeout;

    @Value("${app.admins}")                // "alice,bob,carol"
    private List<String> admins;           // auto-split by Spring

    // SpEL expressions
    @Value("#{T(Math).PI}")                // Spring Expression Language
    private double pi;

    @Value("#{systemProperties['user.home']}")
    private String homeDir;

    @Value("#{environment['spring.profiles.active']}")
    private String activeProfile;

    @Value("#{orderService.getMaxItems()}")  // call another bean's method!
    private int maxItems;
}

// @ConfigurationProperties — bind entire prefix to a POJO (preferred for complex config)
@ConfigurationProperties(prefix = "mail")
@Component
public class MailProperties {
    private String host;
    private int port = 587;    // default value
    private String username;
    private String password;
    private boolean ssl = true;
    private Map<String, String> extra = new HashMap<>();

    // Getters and setters required for binding
}

// application.properties:
// mail.host=smtp.gmail.com
// mail.port=587
// mail.username=myapp@gmail.com
// mail.password=secret
// mail.ssl=true
// mail.extra.retry-count=3
```

### 30.7 Bean Lifecycle Callbacks

```java
@Component
public class DatabaseConnectionPool implements InitializingBean, DisposableBean {
    private HikariDataSource pool;

    // Method 1: @PostConstruct — called after injection, before bean is used
    @PostConstruct
    public void init() {
        System.out.println("Opening connection pool");
        // Runs after: constructor called + all @Autowired dependencies injected
    }

    // Method 2: InitializingBean.afterPropertiesSet()
    @Override
    public void afterPropertiesSet() throws Exception {
        // Same timing as @PostConstruct; @PostConstruct is preferred
    }

    // Method 3: @PreDestroy — called before bean is destroyed (on app shutdown)
    @PreDestroy
    public void cleanup() {
        System.out.println("Closing connection pool");
        if (pool != null) pool.close();
    }

    // Method 4: DisposableBean.destroy()
    @Override
    public void destroy() throws Exception {
        // Same timing as @PreDestroy
    }
}

// Full lifecycle order:
// 1. Instantiate (constructor)
// 2. Inject dependencies (@Autowired fields/setters)
// 3. @PostConstruct / afterPropertiesSet()
// 4. Bean in use ← normal operation
// 5. @PreDestroy / destroy()
// 6. Garbage collected
```

### 30.8 Bean Scopes

```java
@Bean
@Scope("singleton")   // ONE instance per ApplicationContext (default)
// Same instance returned for every ctx.getBean(MyBean.class) call
// ✅ Best for: stateless services, repositories, most beans
// ❌ Bad for: user-specific data, request-specific state
public MyService singleton() { return new MyService(); }

@Bean
@Scope("prototype")   // NEW instance every time bean is requested
// ✅ Best for: stateful, non-thread-safe objects
// ⚠️ Spring creates but does NOT manage lifecycle (no @PreDestroy called)
public Cart cart() { return new Cart(); }

// Web scopes (only in web ApplicationContext):
@Scope(value = "request",     proxyMode = ScopedProxyMode.TARGET_CLASS)
// New instance per HTTP request
@Scope(value = "session",     proxyMode = ScopedProxyMode.TARGET_CLASS)
// New instance per HTTP session
@Scope(value = "application", proxyMode = ScopedProxyMode.TARGET_CLASS)
// One instance per ServletContext

// proxyMode: when injecting request/session-scoped bean into singleton,
// Spring injects a proxy that delegates to the correct instance per request
```

---

## Chapter 31: Spring AOP

### 31.1 Why AOP? Cross-Cutting Concerns

Some concerns apply to many methods across many classes: logging, security checks, transaction management, performance monitoring, caching, input validation. If you implement these inline, every method is polluted with non-business logic:

```java
// ❌ Without AOP — every method has the same boilerplate
public Order placeOrder(Cart cart) {
    log.info("placeOrder called with: " + cart);        // logging
    securityCheck("ROLE_USER");                          // security
    long start = System.currentTimeMillis();             // performance
    try {
        Transaction tx = beginTransaction();             // transaction
        // ... ACTUAL 3 lines of business logic ...
        tx.commit();
        return order;
    } catch (Exception e) {
        tx.rollback();
        log.error("placeOrder failed", e);               // error logging
        throw e;
    } finally {
        log.info("placeOrder took: " + (now - start));  // performance
    }
}
```

**AOP (Aspect-Oriented Programming)** extracts these cross-cutting concerns into separate modules called **Aspects**, applied automatically to matching methods via **Pointcuts**.

### 31.2 AOP Concepts

```
Aspect      — The module containing cross-cutting logic (e.g., LoggingAspect)
Advice      — What the aspect does (before, after, around the method)
Pointcut    — Which methods to intercept (expression matching)
JoinPoint   — A specific method execution that was matched
Weaving     — The process of applying aspects to target objects
Proxy       — Spring wraps your bean in a proxy that applies aspects
```

### 31.3 Implementing Aspects

```java
@Aspect
@Component
public class ApplicationAspect {

    // ── Pointcut Expressions ────────────────────────────────────
    // "execution(modifiers? returnType declaring-class? methodName(params) throws?)"
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() { }          // any method in any service class

    @Pointcut("execution(public * com.example..*(..))")
    public void publicMethods() { }         // any public method in our package

    @Pointcut("within(com.example.service.OrderService)")
    public void orderService() { }          // any method in OrderService

    @Pointcut("@annotation(com.example.annotation.Auditable)")
    public void auditableMethods() { }      // methods annotated with @Auditable

    @Pointcut("@within(org.springframework.stereotype.Repository)")
    public void repositoryClasses() { }     // all methods in @Repository classes

    // Combine pointcuts
    @Pointcut("serviceLayer() && publicMethods()")
    public void publicServiceMethods() { }

    // ── @Before — runs BEFORE the method ────────────────────────
    @Before("serviceLayer()")
    public void logMethodEntry(JoinPoint jp) {
        String method = jp.getSignature().toShortString();
        Object[] args = jp.getArgs();
        log.debug("→ Entering: {} with args: {}", method, Arrays.toString(args));
    }

    // ── @AfterReturning — runs AFTER method returns normally ─────
    @AfterReturning(pointcut = "serviceLayer()", returning = "result")
    public void logMethodExit(JoinPoint jp, Object result) {
        log.debug("← Returning from: {} with result: {}",
            jp.getSignature().toShortString(), result);
    }

    // ── @AfterThrowing — runs AFTER method throws exception ──────
    @AfterThrowing(pointcut = "serviceLayer()", throwing = "ex")
    public void logException(JoinPoint jp, Exception ex) {
        log.error("✗ Exception in: {} — {}",
            jp.getSignature().toShortString(), ex.getMessage());
        // Can inspect ex type and handle differently:
        if (ex instanceof DataAccessException) {
            alertOps("Database error: " + ex.getMessage());
        }
    }

    // ── @After — runs AFTER method (whether exception or not) ─────
    @After("serviceLayer()")
    public void afterFinally(JoinPoint jp) {
        // Like a finally block — good for cleanup/metrics
    }

    // ── @Around — full control — most powerful ─────────────────
    @Around("serviceLayer()")
    public Object measurePerformance(ProceedingJoinPoint pjp) throws Throwable {
        String method = pjp.getSignature().toShortString();
        long start = System.currentTimeMillis();
        try {
            Object result = pjp.proceed();   // ← calls the ACTUAL method
            // Can modify result: result = transform(result);
            return result;
        } catch (Exception e) {
            log.error("Exception in {}: {}", method, e.getMessage());
            throw e;   // re-throw (or swallow/replace if intended)
        } finally {
            long ms = System.currentTimeMillis() - start;
            log.info("{} completed in {}ms", method, ms);
            metrics.record(method, ms);
        }
    }

    // ── Custom annotation-based advice ──────────────────────────
    @Around("@annotation(rateLimited)")
    public Object enforceRateLimit(ProceedingJoinPoint pjp, RateLimited rateLimited)
            throws Throwable {
        String key = pjp.getSignature().getName();
        int limit = rateLimited.requestsPerMinute();
        if (rateLimiter.isLimitExceeded(key, limit)) {
            throw new TooManyRequestsException("Rate limit: " + limit + "/min for " + key);
        }
        return pjp.proceed();
    }
}
```

---

## Chapter 32: Spring Boot

### 32.1 What Spring Boot Does — Auto-configuration Explained

Spring Boot's `@SpringBootApplication` combines three annotations:
- `@Configuration` — this class provides bean definitions
- `@EnableAutoConfiguration` — automatically configure based on classpath
- `@ComponentScan` — scan the current package and sub-packages

**Auto-configuration mechanism:**
```
Spring Boot reads: META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
Contains 100+ auto-configuration classes (e.g., DataSourceAutoConfiguration)

Each class checks conditions:
  @ConditionalOnClass(HikariDataSource.class)   — only if HikariCP is on classpath
  @ConditionalOnMissingBean(DataSource.class)   — only if YOU haven't already configured one
  @ConditionalOnProperty(prefix="spring.datasource", name="url") — only if property is set

If all conditions pass → Spring Boot creates the bean for you
If you provide your own bean → auto-configuration backs off (@ConditionalOnMissingBean)
```

```java
@SpringBootApplication
// Equivalent to:
// @Configuration
// @EnableAutoConfiguration
// @ComponentScan(basePackages = "com.example.myapp")
public class MyApp {
    public static void main(String[] args) {
        ConfigurableApplicationContext ctx = SpringApplication.run(MyApp.class, args);
        // ctx is the fully-initialized ApplicationContext
        // Can access beans: ctx.getBean(MyService.class)
    }
}

// Customize SpringApplication:
SpringApplication app = new SpringApplication(MyApp.class);
app.setBannerMode(Banner.Mode.OFF);  // disable ASCII art banner
app.setWebApplicationType(WebApplicationType.REACTIVE);  // for WebFlux
app.run(args);

// Or using a builder:
new SpringApplicationBuilder(MyApp.class)
    .profiles("production")
    .logStartupInfo(true)
    .run(args);
```

### 32.2 application.properties vs application.yml

```properties
# application.properties — key=value format
server.port=8080
server.servlet.context-path=/api
server.error.include-message=always

spring.datasource.url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=secret
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5

spring.jpa.hibernate.ddl-auto=validate  # none/validate/update/create/create-drop
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false   # IMPORTANT: disable to avoid performance issues

logging.level.root=INFO
logging.level.com.example=DEBUG
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql=TRACE  # log SQL parameter values
logging.pattern.console=%d{HH:mm:ss.SSS} %-5level %logger{36} - %msg%n

# Custom properties
app.jwt.secret=mySecretKey256Bits
app.jwt.expiration-ms=86400000
app.mail.from=noreply@example.com
```

```yaml
# application.yml — YAML format (more readable for nested config)
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: true
    open-in-view: false

logging:
  level:
    root: INFO
    com.example: DEBUG

app:
  jwt:
    secret: mySecretKey
    expiration-ms: 86400000
```

### 32.3 Profiles — Environment-Specific Configuration

```properties
# application.properties (shared across all profiles)
app.name=My Application

# application-dev.properties (active when profile = dev)
spring.datasource.url=jdbc:h2:mem:devdb
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
logging.level.com.example=DEBUG

# application-prod.properties (active when profile = prod)
spring.datasource.url=jdbc:mysql://prod-db:3306/mydb
spring.datasource.username=${DB_USER}   # from environment variable
spring.datasource.password=${DB_PASS}
spring.jpa.hibernate.ddl-auto=validate
logging.level.root=WARN
```

```bash
# Activate profile:
java -jar app.jar --spring.profiles.active=prod
# Or: export SPRING_PROFILES_ACTIVE=prod
```

```java
// Profile-specific beans:
@Configuration
public class CacheConfig {
    @Bean
    @Profile("dev")    // only in dev profile
    public CacheManager devCacheManager() {
        return new SimpleCacheManager();   // in-memory, for development
    }

    @Bean
    @Profile("prod")   // only in prod
    public CacheManager redisCacheManager(RedisConnectionFactory factory) {
        return RedisCacheManager.builder(factory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10)))
            .build();
    }
}

// @Profile on component classes:
@Component
@Profile("!prod")   // active on any profile EXCEPT prod (dev, test, etc.)
public class DataInitializer implements CommandLineRunner {
    @Override
    public void run(String... args) {
        // Load test data only in non-production environments
        loadSampleData();
    }
}
```

### 32.4 Actuator — Production Monitoring

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```properties
# Expose endpoints (never expose all in production without authentication)
management.endpoints.web.exposure.include=health,info,metrics,prometheus
management.endpoints.web.base-path=/actuator
management.endpoint.health.show-details=when-authorized  # or: always / never
management.endpoint.health.show-components=always
management.info.env.enabled=true

# App info (shown in /actuator/info)
info.app.name=Order Service
info.app.version=@project.version@   # read from pom.xml
info.app.java.version=@java.version@
```

```
GET /actuator/health        → {"status":"UP","components":{"db":{"status":"UP"},...}}
GET /actuator/info          → app version, git commit, build info
GET /actuator/metrics       → list of metric names
GET /actuator/metrics/http.server.requests   → HTTP request statistics
GET /actuator/beans         → all Spring beans and dependencies
GET /actuator/env           → all configuration properties
GET /actuator/mappings      → all @RequestMapping mappings
GET /actuator/loggers       → logging levels; POST to change at runtime
GET /actuator/heapdump      → download heap dump
GET /actuator/threaddump    → all thread stack traces
GET /actuator/prometheus    → metrics in Prometheus format
```

```java
// Custom health indicator
@Component
public class ExternalApiHealthIndicator implements HealthIndicator {
    @Autowired private ExternalApiClient client;

    @Override
    public Health health() {
        try {
            boolean alive = client.ping();
            if (alive) {
                return Health.up().withDetail("responseTime", "15ms").build();
            }
            return Health.down().withDetail("reason", "API not responding").build();
        } catch (Exception e) {
            return Health.down(e).withDetail("error", e.getMessage()).build();
        }
    }
}

// Custom metric
@Service
public class OrderService {
    private final Counter orderCounter;
    private final Timer   orderTimer;

    public OrderService(MeterRegistry registry) {
        orderCounter = Counter.builder("orders.placed")
            .description("Total orders placed")
            .tag("service", "order")
            .register(registry);
        orderTimer = Timer.builder("orders.processing.time")
            .register(registry);
    }

    public Order placeOrder(Cart cart) {
        return orderTimer.record(() -> {
            // ... logic ...
            orderCounter.increment();
            return order;
        });
    }
}
```

---

## Chapter 33: Spring MVC

### 33.1 The DispatcherServlet — How Spring MVC Works

Spring MVC is built on a single Servlet called `DispatcherServlet` — the Front Controller. Every HTTP request goes through it:

```
HTTP Request
    │
    ▼
DispatcherServlet  (registered in servlet container for /* or /)
    │
    ├──1── HandlerMapping         finds which @Controller/@RequestMapping handles this URL
    │
    ├──2── HandlerAdapter         adapts the handler (e.g., annotated controller → method invocation)
    │
    ├──3── Controller Method      your code executes; returns model + view name
    │
    ├──4── ViewResolver           "products/list" → /WEB-INF/templates/products/list.html
    │
    └──5── View (Thymeleaf/JSP)   renders HTML; sends response
```

### 33.2 Controllers — Complete Reference

```java
@Controller                           // returns view names (for Thymeleaf/JSP)
@RequestMapping("/products")          // base URL for all methods in this controller
@SessionAttributes("cart")            // auto-store/retrieve "cart" from HTTP session
public class ProductController {

    @Autowired private ProductService productService;
    @Autowired private CategoryService categoryService;

    // ── GET all products ────────────────────────────────────────
    @GetMapping                        // handles GET /products
    public String listProducts(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "12") int size,
            @RequestParam(required = false)    String category,
            @RequestParam(defaultValue = "name") String sortBy,
            Model model) {

        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
        Page<Product> products = productService.findAll(category, pageable);

        model.addAttribute("products",    products.getContent());
        model.addAttribute("page",        products);
        model.addAttribute("categories",  categoryService.findAll());
        model.addAttribute("currentCat",  category);

        return "products/list";   // view name → resolved to template
    }

    // ── GET single product ──────────────────────────────────────
    @GetMapping("/{id}")               // handles GET /products/42
    public String productDetail(
            @PathVariable Long id,
            Model model,
            RedirectAttributes redirectAttrs) {

        Optional<Product> product = productService.findById(id);
        if (product.isEmpty()) {
            redirectAttrs.addFlashAttribute("error", "Product " + id + " not found");
            return "redirect:/products";  // redirect with flash message
        }
        model.addAttribute("product", product.get());
        model.addAttribute("relatedProducts", productService.findRelated(id));
        return "products/detail";
    }

    // ── Show create form ────────────────────────────────────────
    @GetMapping("/new")
    public String showCreateForm(Model model) {
        model.addAttribute("product", new ProductForm());  // empty form object
        model.addAttribute("categories", categoryService.findAll());
        return "products/form";
    }

    // ── Handle form submission ──────────────────────────────────
    @PostMapping
    public String createProduct(
            @Valid @ModelAttribute("product") ProductForm form,
            BindingResult bindingResult,      // MUST immediately follow @Valid param
            Model model,
            RedirectAttributes redirectAttrs) {

        if (bindingResult.hasErrors()) {
            model.addAttribute("categories", categoryService.findAll());
            return "products/form";            // re-show form with errors
        }

        if (productService.existsBySku(form.getSku())) {
            bindingResult.rejectValue("sku", "duplicate.sku", "SKU already exists");
            return "products/form";
        }

        Product saved = productService.create(form);
        redirectAttrs.addFlashAttribute("success", "Product created: " + saved.getName());
        return "redirect:/products/" + saved.getId();  // PRG pattern
    }

    // ── AJAX / partial request ──────────────────────────────────
    @GetMapping("/search")
    @ResponseBody                        // return value written to response body (JSON)
    public List<ProductSummary> searchAjax(@RequestParam String q) {
        return productService.search(q).stream()
            .map(ProductSummary::new)
            .toList();
    }

    // ── @ModelAttribute method — adds data to EVERY model in this controller ──
    @ModelAttribute("currentUser")
    public User addCurrentUser(Principal principal) {
        return userService.findByUsername(principal.getName());
    }
}
```

### 33.3 Validation

```java
// Validation constraints on the form/DTO class
public class ProductForm {
    @NotBlank(message = "Product name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.01", message = "Price must be positive")
    @Digits(integer = 8, fraction = 2, message = "Invalid price format")
    private BigDecimal price;

    @NotBlank @Pattern(regexp = "[A-Z]{3}\\d{6}", message = "SKU format: 3 letters + 6 digits")
    private String sku;

    @Min(0) @Max(100000)
    private int stockLevel;

    @NotNull
    private Long categoryId;

    @Email(message = "Invalid supplier email")
    private String supplierEmail;

    @Valid                                    // cascade validation into nested object
    @NotNull
    private DimensionsForm dimensions;
}

// Custom validator
@Component
public class ProductFormValidator implements Validator {
    @Autowired private ProductService productService;

    @Override
    public boolean supports(Class<?> clazz) { return ProductForm.class.equals(clazz); }

    @Override
    public void validate(Object target, Errors errors) {
        ProductForm form = (ProductForm) target;
        if (form.getPrice() != null && form.getCostPrice() != null) {
            if (form.getPrice().compareTo(form.getCostPrice()) < 0) {
                errors.rejectValue("price", "price.below.cost",
                    "Selling price cannot be below cost price");
            }
        }
    }
}

// In controller — register custom validator:
@InitBinder
public void initBinder(WebDataBinder binder) {
    binder.addValidators(productFormValidator);
}
```

### 33.4 @ControllerAdvice — Global Error Handling

```java
@ControllerAdvice   // applies to all @Controller classes
public class GlobalExceptionHandler {

    // Handle specific exception across all controllers
    @ExceptionHandler(ResourceNotFoundException.class)
    public String handleNotFound(ResourceNotFoundException ex, Model model) {
        model.addAttribute("errorMessage", ex.getMessage());
        model.addAttribute("errorCode", 404);
        return "error/404";   // show 404.html template
    }

    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public String handleForbidden(AccessDeniedException ex, Model model) {
        model.addAttribute("errorMessage", "You don't have permission for this action");
        return "error/403";
    }

    // Catch-all
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public String handleGeneral(Exception ex, Model model, HttpServletRequest req) {
        log.error("Unhandled exception for request: " + req.getRequestURI(), ex);
        model.addAttribute("errorMessage", "An unexpected error occurred");
        return "error/500";
    }

    // Add data to every model in every controller
    @ModelAttribute("appVersion")
    public String appVersion() { return "2.1.0"; }
}
```

---

## Chapter 34: Spring REST API

### 34.1 Building REST APIs

```java
@RestController               // @Controller + @ResponseBody on every method
@RequestMapping("/api/v1/products")
@CrossOrigin(origins = "http://localhost:3000")  // allow CORS from React frontend
public class ProductApiController {

    @Autowired private ProductService productService;

    // GET /api/v1/products?page=0&size=20&sort=price,desc&category=electronics
    @GetMapping
    public ResponseEntity<PagedResponse<ProductDTO>> getAll(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String category,
            @SortDefault(sort = "name", direction = Sort.Direction.ASC) Pageable pageable) {

        Page<ProductDTO> result = productService.findAll(category, pageable);
        return ResponseEntity.ok(PagedResponse.from(result));
    }

    // GET /api/v1/products/42
    @GetMapping("/{id}")
    public ResponseEntity<ProductDTO> getById(@PathVariable Long id) {
        return productService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // POST /api/v1/products
    @PostMapping
    public ResponseEntity<ProductDTO> create(
            @Valid @RequestBody CreateProductRequest req,
            UriComponentsBuilder ucb) {

        ProductDTO created = productService.create(req);
        URI location = ucb.path("/api/v1/products/{id}")
            .buildAndExpand(created.getId())
            .toUri();
        return ResponseEntity.created(location).body(created);  // 201 Created + Location header
    }

    // PUT /api/v1/products/42 — full replacement
    @PutMapping("/{id}")
    public ResponseEntity<ProductDTO> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateProductRequest req) {

        return productService.update(id, req)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    // PATCH /api/v1/products/42 — partial update
    @PatchMapping("/{id}")
    public ResponseEntity<ProductDTO> patch(
            @PathVariable Long id,
            @RequestBody Map<String, Object> fields) {

        try {
            ProductDTO patched = productService.patch(id, fields);
            return ResponseEntity.ok(patched);
        } catch (ResourceNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // DELETE /api/v1/products/42
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!productService.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        productService.delete(id);
        return ResponseEntity.noContent().build();   // 204 No Content
    }

    // File upload
    @PostMapping("/{id}/image")
    public ResponseEntity<String> uploadImage(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {

        if (file.isEmpty()) return ResponseEntity.badRequest().body("No file provided");
        String imageUrl = productService.uploadImage(id, file);
        return ResponseEntity.ok(imageUrl);
    }
}
```

### 34.2 Standard Error Response Format

```java
// Consistent error DTO
public record ApiError(
    int status,
    String error,
    String message,
    String path,
    LocalDateTime timestamp,
    Map<String, String> validationErrors  // null for non-validation errors
) {
    // Factory methods
    static ApiError of(int status, String error, String message, String path) {
        return new ApiError(status, error, message, path, LocalDateTime.now(), null);
    }
    static ApiError validation(String message, String path, Map<String, String> errors) {
        return new ApiError(400, "Validation Failed", message, path, LocalDateTime.now(), errors);
    }
}

@RestControllerAdvice
public class RestGlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ApiError handleNotFound(ResourceNotFoundException ex, HttpServletRequest req) {
        return ApiError.of(404, "Not Found", ex.getMessage(), req.getRequestURI());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ApiError handleValidation(MethodArgumentNotValidException ex,
                                     HttpServletRequest req) {
        Map<String, String> errors = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(fe ->
            errors.put(fe.getField(), fe.getDefaultMessage()));
        ex.getBindingResult().getGlobalErrors().forEach(ge ->
            errors.put(ge.getObjectName(), ge.getDefaultMessage()));
        return ApiError.validation("Validation failed", req.getRequestURI(), errors);
    }

    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ApiError handleConstraintViolation(ConstraintViolationException ex,
                                               HttpServletRequest req) {
        Map<String, String> errors = new LinkedHashMap<>();
        ex.getConstraintViolations().forEach(cv ->
            errors.put(cv.getPropertyPath().toString(), cv.getMessage()));
        return ApiError.validation("Constraint violation", req.getRequestURI(), errors);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ApiError handleGeneral(Exception ex, HttpServletRequest req) {
        log.error("Unhandled exception", ex);
        return ApiError.of(500, "Internal Server Error",
            "An unexpected error occurred", req.getRequestURI());
    }
}
```

### 34.3 OpenAPI / Swagger Documentation

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

```java
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Product API")
                .description("REST API for product management")
                .version("v1.0")
                .contact(new Contact().name("Dev Team").email("dev@example.com"))
                .license(new License().name("MIT")))
            .externalDocs(new ExternalDocumentation()
                .description("Full documentation")
                .url("https://docs.example.com"))
            .components(new Components()
                .addSecuritySchemes("bearerAuth",
                    new SecurityScheme()
                        .name("bearerAuth")
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")))
            .addSecurityItem(new SecurityRequirement().addList("bearerAuth"));
    }
}

// Annotate controller methods for documentation:
@Operation(
    summary = "Get product by ID",
    description = "Returns a single product. Returns 404 if not found."
)
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "Product found",
        content = @Content(schema = @Schema(implementation = ProductDTO.class))),
    @ApiResponse(responseCode = "404", description = "Product not found",
        content = @Content(schema = @Schema(implementation = ApiError.class)))
})
@GetMapping("/{id}")
public ResponseEntity<ProductDTO> getById(
        @Parameter(description = "Product ID", example = "42") @PathVariable Long id) {
    ...
}

// Access UI: http://localhost:8080/swagger-ui.html
// Access JSON: http://localhost:8080/v3/api-docs
```

---

## Chapter 35: Spring Data & Transactions

### 35.1 @Transactional — Deep Dive

```java
@Service
public class OrderService {

    // @Transactional on the class — all public methods are transactional
    // @Transactional on a method — overrides class-level for that method

    @Transactional                     // uses default settings
    public Order placeOrder(PlaceOrderRequest req) {
        // Everything in this method is in ONE transaction:
        // - If all succeeds → COMMIT
        // - If ANY RuntimeException → ROLLBACK
        // - If checked exception → COMMIT by default (change with rollbackFor)
        inventory.reserve(req.getItems());
        Order order = orderRepo.save(new Order(req));
        payment.charge(order.getTotal(), req.getPaymentToken());
        emailService.sendConfirmation(order);   // if this fails, whole thing rolls back
        return order;
    }

    @Transactional(readOnly = true)    // tells Hibernate: no dirty checking, no flush
    // Faster for reads — Hibernate skips tracking changes to entities
    public Page<Order> findByCustomer(Long customerId, Pageable pageable) {
        return orderRepo.findByCustomerId(customerId, pageable);
    }

    @Transactional(rollbackFor = Exception.class)  // rollback on ALL exceptions (including checked)
    public void importOrders(InputStream csv) throws IOException {
        // IOException is checked — without rollbackFor, transaction would COMMIT even on IOException
    }

    @Transactional(noRollbackFor = {CommunicationException.class})
    // Commit even if CommunicationException (e.g., email failed — save the order anyway)
    public Order placeOrderLenient(PlaceOrderRequest req) {
        Order order = orderRepo.save(new Order(req));
        try {
            emailService.sendConfirmation(order);
        } catch (CommunicationException e) {
            log.warn("Email failed, but order was saved: " + order.getId());
        }
        return order;
    }

    @Transactional(timeout = 30)   // rollback if transaction takes > 30 seconds
    public void longRunningBatch() { ... }
}
```

**Propagation — what happens when a transactional method calls another:**

```java
// REQUIRED (default): join existing transaction, or create new one
//   Method A has tx → Method B joins A's tx
//   Method A no tx  → Method B creates new tx

// REQUIRES_NEW: always suspend current tx and create a new independent one
//   Use for: audit logging that must commit even if outer tx rolls back
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void auditLog(String action, Long userId) {
    auditRepo.save(new AuditEntry(action, userId));
    // This commits INDEPENDENTLY of the calling method's transaction
}

// MANDATORY: must run in existing transaction; throw if none
@Transactional(propagation = Propagation.MANDATORY)
public void validateBusinessRules(Order order) { ... }

// NEVER: must NOT run in a transaction; throw if one exists
@Transactional(propagation = Propagation.NEVER)
public void readOnlyOperation() { ... }

// SUPPORTS: run in tx if one exists; no tx if none
// NOT_SUPPORTED: suspend tx if one exists, run without tx
// NESTED: create savepoint within existing tx; partial rollback possible
```

**Isolation Levels — controlling visibility between concurrent transactions:**

```java
@Transactional(isolation = Isolation.READ_COMMITTED)   // default for most DBs
// Phenomena prevented:
//   Dirty Read:           reading uncommitted data from another tx ← READ_COMMITTED prevents
//   Non-Repeatable Read:  same row returns different values in same tx ← REPEATABLE_READ prevents
//   Phantom Read:         new rows appear between two reads in same tx ← SERIALIZABLE prevents

// Levels from weakest to strongest:
// READ_UNCOMMITTED: sees uncommitted changes — fastest, most bugs
// READ_COMMITTED:   sees only committed changes — good balance (PostgreSQL, Oracle default)
// REPEATABLE_READ:  same reads always return same data — MySQL default
// SERIALIZABLE:     complete isolation — slowest, safest
```

### 35.2 Spring JdbcTemplate

```java
@Repository
public class OrderJdbcRepository {
    private final JdbcTemplate jdbc;
    private final NamedParameterJdbcTemplate namedJdbc;

    public OrderJdbcRepository(JdbcTemplate jdbc, NamedParameterJdbcTemplate namedJdbc) {
        this.jdbc = jdbc;
        this.namedJdbc = namedJdbc;
    }

    // Simple query — single column result
    public int countByStatus(String status) {
        return jdbc.queryForObject("SELECT COUNT(*) FROM orders WHERE status = ?",
            Integer.class, status);
    }

    // Query for single row
    public Optional<Order> findById(Long id) {
        try {
            Order order = jdbc.queryForObject(
                "SELECT * FROM orders WHERE id = ?",
                orderRowMapper(),
                id
            );
            return Optional.ofNullable(order);
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    // Query for list
    public List<Order> findByCustomer(Long customerId) {
        return jdbc.query(
            "SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC",
            orderRowMapper(),
            customerId
        );
    }

    // RowMapper — convert ResultSet row to object
    private RowMapper<Order> orderRowMapper() {
        return (rs, rowNum) -> {
            Order order = new Order();
            order.setId(rs.getLong("id"));
            order.setCustomerId(rs.getLong("customer_id"));
            order.setStatus(OrderStatus.valueOf(rs.getString("status")));
            order.setTotal(rs.getBigDecimal("total"));
            order.setCreatedAt(rs.getTimestamp("created_at").toLocalDateTime());
            return order;
        };
    }

    // Named parameters (avoids positional confusion in large queries)
    public List<Order> findByFilter(OrderFilter filter) {
        String sql = """
            SELECT * FROM orders
            WHERE customer_id = :customerId
              AND status IN (:statuses)
              AND created_at BETWEEN :from AND :to
            ORDER BY created_at DESC
            LIMIT :limit
            """;
        MapSqlParameterSource params = new MapSqlParameterSource()
            .addValue("customerId", filter.getCustomerId())
            .addValue("statuses",   filter.getStatuses())  // List works with IN
            .addValue("from",       Timestamp.valueOf(filter.getFrom()))
            .addValue("to",         Timestamp.valueOf(filter.getTo()))
            .addValue("limit",      filter.getLimit());

        return namedJdbc.query(sql, params, orderRowMapper());
    }

    // Update
    public int updateStatus(Long id, String status) {
        return jdbc.update("UPDATE orders SET status = ?, updated_at = NOW() WHERE id = ?",
            status, id);
    }

    // Insert with generated key
    public Long insert(Order order) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                "INSERT INTO orders (customer_id, total, status) VALUES (?,?,?)",
                Statement.RETURN_GENERATED_KEYS);
            ps.setLong(1, order.getCustomerId());
            ps.setBigDecimal(2, order.getTotal());
            ps.setString(3, order.getStatus().name());
            return ps;
        }, keyHolder);
        return keyHolder.getKey().longValue();
    }

    // Batch update
    public int[] batchInsert(List<Order> orders) {
        return jdbc.batchUpdate(
            "INSERT INTO orders (customer_id, total, status) VALUES (?,?,?)",
            orders,
            100,  // batch size
            (ps, order) -> {
                ps.setLong(1, order.getCustomerId());
                ps.setBigDecimal(2, order.getTotal());
                ps.setString(3, order.getStatus().name());
            }
        );
    }
}
```

---

## Chapter 36: Spring Security & JWT

### 36.1 How Spring Security Works

```
HTTP Request
    │
    ▼
Security Filter Chain (ordered chain of filters)
    ├── SecurityContextPersistenceFilter   restore SecurityContext from session/header
    ├── UsernamePasswordAuthenticationFilter  process login form submission
    ├── JwtAuthenticationFilter (custom)   validate JWT token
    ├── BasicAuthenticationFilter          HTTP Basic auth
    ├── ExceptionTranslationFilter         translate security exceptions → 401/403
    └── FilterSecurityInterceptor          final access decision (authorize or deny)
    │
    ▼
Your Controller (only if all filters pass)
```

**Key concepts:**
- `SecurityContextHolder` — holds the current user's authentication (thread-local)
- `Authentication` — represents the authenticated user (principal + authorities)
- `UserDetails` — Spring's user representation (username, password, roles)
- `AuthenticationManager` — verifies credentials
- `AccessDecisionManager` — decides if authenticated user can access a resource

### 36.2 SecurityConfig — The Full Setup

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)   // enables @PreAuthorize, @PostAuthorize
public class SecurityConfig {

    @Autowired private JwtAuthFilter jwtAuthFilter;
    @Autowired private CustomUserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF for stateless REST APIs (CSRF is for session-based apps)
            .csrf(csrf -> csrf.disable())

            // CORS configuration
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))

            // Stateless sessions — no HTTP session; JWT carries all auth state
            .sessionManagement(sm ->
                sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

            // URL-based authorization rules (order matters — first match wins)
            .authorizeHttpRequests(auth -> auth
                // Completely public endpoints
                .requestMatchers("/api/auth/login", "/api/auth/register").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/products/**").permitAll()
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()

                // Role-based access
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.DELETE, "/api/**").hasAnyRole("ADMIN", "MANAGER")

                // Authority-based access
                .requestMatchers("/api/reports/**").hasAuthority("REPORT_VIEW")

                // Everything else requires authentication
                .anyRequest().authenticated()
            )

            // Exception handling
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(   // 401: not authenticated
                    (req, res, authEx) -> {
                        res.setContentType("application/json");
                        res.setStatus(401);
                        res.getWriter().write("{\"error\":\"Unauthorized\",\"message\":\"" +
                            authEx.getMessage() + "\"}");
                    })
                .accessDeniedHandler(        // 403: authenticated but not authorized
                    (req, res, accessEx) -> {
                        res.setContentType("application/json");
                        res.setStatus(403);
                        res.getWriter().write("{\"error\":\"Forbidden\",\"message\":\"" +
                            accessEx.getMessage() + "\"}");
                    })
            )

            // Add our JWT filter before the standard username/password filter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        // BCrypt with strength 12 (2^12 = 4096 rounds) — strong and secure
        // Higher strength = slower hashing = harder to brute force
        return new BCryptPasswordEncoder(12);
    }

    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http) throws Exception {
        return http.getSharedObject(AuthenticationManagerBuilder.class)
            .userDetailsService(userDetailsService)
            .passwordEncoder(passwordEncoder())
            .and()
            .build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(List.of("http://localhost:3000", "https://myapp.com"));
        config.setAllowedMethods(List.of("GET","POST","PUT","PATCH","DELETE","OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setExposedHeaders(List.of("Authorization", "X-Request-ID"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);   // cache preflight response for 1 hour

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

### 36.3 UserDetailsService — Load Users from Database

```java
@Entity
@Table(name = "app_users")
public class AppUser {
    @Id @GeneratedValue private Long id;
    @Column(unique = true, nullable = false) private String username;
    @Column(nullable = false) private String password;  // BCrypt hash
    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "role")
    private Set<String> roles = new HashSet<>();   // "ROLE_USER", "ROLE_ADMIN"
    private boolean enabled = true;
    private boolean accountNonExpired = true;
    private boolean credentialsNonExpired = true;
    private boolean accountNonLocked = true;
}

@Service
public class CustomUserDetailsService implements UserDetailsService {
    @Autowired private AppUserRepository userRepo;

    @Override
    @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        AppUser user = userRepo.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));

        // Convert our AppUser to Spring's UserDetails
        List<GrantedAuthority> authorities = user.getRoles().stream()
            .map(SimpleGrantedAuthority::new)
            .collect(Collectors.toList());

        return new org.springframework.security.core.userdetails.User(
            user.getUsername(),
            user.getPassword(),       // already BCrypt hashed in DB
            user.isEnabled(),
            user.isAccountNonExpired(),
            user.isCredentialsNonExpired(),
            user.isAccountNonLocked(),
            authorities
        );
    }
}
```

### 36.4 JWT — Complete Implementation

```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.5</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.5</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.5</version>
    <scope>runtime</scope>
</dependency>
```

```java
@Component
public class JwtService {

    @Value("${app.jwt.secret}")
    private String secretKey;

    @Value("${app.jwt.expiration-ms:86400000}")   // 24 hours default
    private long expirationMs;

    private SecretKey signingKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    // Generate JWT token
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("roles", userDetails.getAuthorities().stream()
            .map(GrantedAuthority::getAuthority)
            .collect(Collectors.toList()));

        return Jwts.builder()
            .claims(claims)
            .subject(userDetails.getUsername())
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + expirationMs))
            .signWith(signingKey(), Jwts.SIG.HS256)
            .compact();
    }

    // Generate refresh token (longer expiry, no roles)
    public String generateRefreshToken(UserDetails userDetails) {
        return Jwts.builder()
            .subject(userDetails.getUsername())
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + 7 * 24 * 3600 * 1000L)) // 7 days
            .signWith(signingKey())
            .compact();
    }

    // Extract username from token
    public String extractUsername(String token) {
        return extractClaims(token).getSubject();
    }

    // Validate token
    public boolean isTokenValid(String token, UserDetails userDetails) {
        try {
            Claims claims = extractClaims(token);
            return claims.getSubject().equals(userDetails.getUsername())
                && !claims.getExpiration().before(new Date());
        } catch (JwtException e) {
            return false;
        }
    }

    private Claims extractClaims(String token) {
        return Jwts.parser()
            .verifyWith(signingKey())
            .build()
            .parseSignedClaims(token)
            .getPayload();
    }
}

// JWT Filter — runs on every request
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    @Autowired private JwtService jwtService;
    @Autowired private CustomUserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain)
            throws ServletException, IOException {

        // 1. Extract Authorization header
        final String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            chain.doFilter(request, response);  // no JWT → pass to next filter
            return;
        }

        // 2. Extract token (remove "Bearer " prefix)
        final String token = authHeader.substring(7);

        try {
            // 3. Extract username from token
            final String username = jwtService.extractUsername(token);

            // 4. If username found and not already authenticated
            if (username != null
                    && SecurityContextHolder.getContext().getAuthentication() == null) {

                // 5. Load user from database
                UserDetails userDetails = userDetailsService.loadUserByUsername(username);

                // 6. Validate token
                if (jwtService.isTokenValid(token, userDetails)) {
                    // 7. Create authentication object
                    UsernamePasswordAuthenticationToken auth =
                        new UsernamePasswordAuthenticationToken(
                            userDetails,
                            null,                     // no credentials in token
                            userDetails.getAuthorities()
                        );
                    auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                    // 8. Store in SecurityContext — user is now authenticated
                    SecurityContextHolder.getContext().setAuthentication(auth);
                }
            }
        } catch (JwtException e) {
            // Invalid token — log it but don't set authentication
            log.warn("Invalid JWT token: " + e.getMessage());
        }

        chain.doFilter(request, response);
    }
}

// Auth controller — login and register
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired private AuthenticationManager authManager;
    @Autowired private JwtService jwtService;
    @Autowired private CustomUserDetailsService userDetailsService;
    @Autowired private AppUserRepository userRepo;
    @Autowired private PasswordEncoder encoder;

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest req) {
        try {
            // Authenticate — throws AuthenticationException if invalid
            authManager.authenticate(
                new UsernamePasswordAuthenticationToken(req.username(), req.password())
            );
        } catch (BadCredentialsException e) {
            return ResponseEntity.status(401).body(
                new AuthResponse(null, null, "Invalid credentials"));
        }

        UserDetails user  = userDetailsService.loadUserByUsername(req.username());
        String accessToken  = jwtService.generateToken(user);
        String refreshToken = jwtService.generateRefreshToken(user);

        return ResponseEntity.ok(new AuthResponse(accessToken, refreshToken, "Login successful"));
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest req) {
        if (userRepo.existsByUsername(req.username())) {
            return ResponseEntity.badRequest().body(
                new AuthResponse(null, null, "Username already taken"));
        }

        AppUser user = new AppUser();
        user.setUsername(req.username());
        user.setPassword(encoder.encode(req.password()));  // BCrypt hash
        user.setRoles(Set.of("ROLE_USER"));
        userRepo.save(user);

        UserDetails userDetails = userDetailsService.loadUserByUsername(user.getUsername());
        String token = jwtService.generateToken(userDetails);
        return ResponseEntity.status(201).body(new AuthResponse(token, null, "Registered"));
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refresh(@RequestBody RefreshRequest req) {
        String username = jwtService.extractUsername(req.refreshToken());
        UserDetails user = userDetailsService.loadUserByUsername(username);
        if (jwtService.isTokenValid(req.refreshToken(), user)) {
            String newToken = jwtService.generateToken(user);
            return ResponseEntity.ok(new AuthResponse(newToken, req.refreshToken(), "Token refreshed"));
        }
        return ResponseEntity.status(401).body(new AuthResponse(null, null, "Invalid refresh token"));
    }
}

public record LoginRequest(@NotBlank String username, @NotBlank String password) { }
public record RegisterRequest(@NotBlank String username, @Size(min=8) String password, @Email String email) { }
public record RefreshRequest(String refreshToken) { }
public record AuthResponse(String accessToken, String refreshToken, String message) { }
```

### 36.5 Method Security

```java
@Service
public class DocumentService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteAllDocuments() { ... }

    // SpEL to check if user owns the resource
    @PreAuthorize("hasRole('ADMIN') or #document.ownerId == authentication.principal.id")
    public void deleteDocument(Document document) { ... }

    // Access method parameter in expression
    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.username")
    public List<Document> getUserDocuments(String userId) { ... }

    // Filter return value — remove elements the user can't see
    @PostFilter("filterObject.ownerId == authentication.principal.id or hasRole('ADMIN')")
    public List<Document> findAll() { ... }

    // Filter input collection — remove elements user can't pass
    @PreFilter("filterObject.ownerId == authentication.principal.id")
    public void deleteAll(List<Document> docs) { ... }
}

// Get current user anywhere:
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
String username = auth.getName();
Collection<? extends GrantedAuthority> authorities = auth.getAuthorities();
UserDetails user = (UserDetails) auth.getPrincipal();

// In controller method:
@GetMapping("/profile")
public ResponseEntity<UserDTO> getProfile(
        @AuthenticationPrincipal UserDetails currentUser) {
    return ResponseEntity.ok(userService.getProfile(currentUser.getUsername()));
}
```

---

## Chapter 37: Spring Cloud & Microservices

### 37.1 Microservices — The Architecture Pattern

A **monolith** deploys as one unit. A **microservice** architecture decomposes it into small, independently deployable services:

```
Monolith                           Microservices
──────────────────────────────     ─────────────────────────────────────
┌───────────────────────────┐      ┌───────┐  ┌───────┐  ┌──────────┐
│ UserModule                │      │ User  │  │ Order │  │ Inventory│
│ OrderModule               │      │  Svc  │  │  Svc  │  │   Svc    │
│ InventoryModule           │ →    └──┬────┘  └──┬────┘  └────┬─────┘
│ NotificationModule        │         │ REST/gRPC │             │
│ SharedDatabase            │         └────────────────────────┘
└───────────────────────────┘                   each has own DB
```

**Benefits**: independent deployment, independent scaling, technology diversity, smaller teams
**Costs**: network latency, distributed transactions, operational complexity, eventual consistency

### 37.2 Service Discovery — Eureka

```xml
<!-- Eureka Server pom.xml -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

```java
@SpringBootApplication
@EnableEurekaServer
public class EurekaServer {
    public static void main(String[] args) { SpringApplication.run(EurekaServer.class, args); }
}
```

```properties
# Eureka server application.properties
server.port=8761
spring.application.name=eureka-server
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false
eureka.server.enable-self-preservation=false   # disable in dev
```

```properties
# Each microservice — registering as Eureka client
spring.application.name=order-service         # service name in registry
server.port=8082
eureka.client.service-url.defaultZone=http://localhost:8761/eureka
eureka.instance.prefer-ip-address=true
eureka.instance.instance-id=${spring.application.name}:${random.uuid}
```

### 37.3 API Gateway — Spring Cloud Gateway

```yaml
# gateway application.yml
spring:
  application:
    name: api-gateway
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service       # lb:// = load balance via Eureka
          predicates:
            - Path=/api/users/**
          filters:
            - RewritePath=/api/users/(?<segment>.*), /$\{segment}
            - AddRequestHeader=X-Request-Source, gateway
            - name: CircuitBreaker
              args:
                name: userServiceCB
                fallbackUri: forward:/fallback/users

        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
            - Method=GET,POST          # only GET and POST
          filters:
            - name: RateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20

        - id: static-content
          uri: http://content-server:8090
          predicates:
            - Path=/static/**
            - Header=Accept, text/html
```

```java
// Global filter — runs for ALL routes
@Component
public class AuthGatewayFilter implements GlobalFilter, Ordered {

    @Autowired private JwtService jwtService;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String path = exchange.getRequest().getPath().toString();
        // Skip auth for public paths
        if (path.startsWith("/api/auth/") || path.startsWith("/actuator/")) {
            return chain.filter(exchange);
        }

        String token = extractToken(exchange.getRequest());
        if (token == null || !jwtService.isValid(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        // Add user info to headers so downstream services know who's calling
        String username = jwtService.extractUsername(token);
        ServerHttpRequest modified = exchange.getRequest().mutate()
            .header("X-Auth-User", username)
            .header("X-Auth-Roles", String.join(",", jwtService.extractRoles(token)))
            .build();

        return chain.filter(exchange.mutate().request(modified).build());
    }

    @Override
    public int getOrder() { return -1; }  // run before other filters
}
```

### 37.4 OpenFeign — Declarative HTTP Client

```java
// Just define an interface — Feign generates the implementation
@FeignClient(
    name = "inventory-service",          // service name in Eureka
    fallback = InventoryClientFallback.class,  // circuit breaker fallback
    configuration = FeignConfig.class    // custom config (timeouts, interceptors)
)
public interface InventoryClient {

    @GetMapping("/api/inventory/{productId}")
    InventoryDTO getInventory(@PathVariable Long productId);

    @PostMapping("/api/inventory/reserve")
    ReservationResult reserve(@RequestBody ReservationRequest request);

    @DeleteMapping("/api/inventory/reservations/{reservationId}")
    void cancelReservation(@PathVariable String reservationId);

    @GetMapping("/api/inventory")
    Page<InventoryDTO> findAll(
        @RequestParam int page,
        @RequestParam int size,
        @RequestHeader("X-Auth-User") String user);  // pass headers
}

// Fallback — called when inventory-service is down or returns error
@Component
public class InventoryClientFallback implements InventoryClient {
    @Override
    public InventoryDTO getInventory(Long productId) {
        return InventoryDTO.unknown(productId);  // graceful degradation
    }

    @Override
    public ReservationResult reserve(ReservationRequest req) {
        throw new ServiceUnavailableException("Inventory service unavailable");
    }

    @Override
    public void cancelReservation(String id) {
        log.warn("Could not cancel reservation {} — inventory service down", id);
    }

    @Override
    public Page<InventoryDTO> findAll(int page, int size, String user) {
        return Page.empty();
    }
}

// Configuration
@Configuration
public class FeignConfig {
    @Bean
    public Request.Options requestOptions() {
        return new Request.Options(
            Duration.ofSeconds(5),   // connect timeout
            Duration.ofSeconds(10),  // read timeout
            true                     // follow redirects
        );
    }

    @Bean
    public ErrorDecoder errorDecoder() {
        return (methodKey, response) -> switch (response.status()) {
            case 404 -> new ResourceNotFoundException("Resource not found");
            case 503 -> new ServiceUnavailableException("Service unavailable");
            default  -> new RuntimeException("Feign error " + response.status());
        };
    }
}
```

### 37.5 Resilience4j — Circuit Breaker, Retry, Rate Limiter

```yaml
resilience4j:
  circuitbreaker:
    instances:
      inventoryService:
        failure-rate-threshold: 50           # open after 50% failures
        slow-call-rate-threshold: 80         # 80% slow calls also triggers opening
        slow-call-duration-threshold: 2s
        minimum-number-of-calls: 10          # evaluate after 10 calls
        wait-duration-in-open-state: 30s     # wait 30s before trying again
        permitted-number-of-calls-in-half-open-state: 5
        sliding-window-type: COUNT_BASED     # or TIME_BASED
        sliding-window-size: 20
  retry:
    instances:
      inventoryService:
        max-attempts: 3
        wait-duration: 500ms
        exponential-backoff-multiplier: 2    # 500ms, 1000ms, 2000ms
        retry-exceptions:
          - java.io.IOException
          - org.springframework.web.client.HttpServerErrorException
        ignore-exceptions:
          - com.example.exception.ValidationException
  timelimiter:
    instances:
      inventoryService:
        timeout-duration: 3s
  ratelimiter:
    instances:
      api:
        limit-for-period: 100
        limit-refresh-period: 1s
        timeout-duration: 100ms
```

```java
@Service
public class OrderService {

    @Autowired private InventoryClient inventoryClient;

    // Annotations apply in order: TimeLimiter → CircuitBreaker → Retry
    @TimeLimiter(name = "inventoryService")
    @CircuitBreaker(name = "inventoryService", fallbackMethod = "inventoryFallback")
    @Retry(name = "inventoryService")
    public CompletableFuture<InventoryDTO> checkInventory(Long productId) {
        return CompletableFuture.supplyAsync(() -> inventoryClient.getInventory(productId));
    }

    // Fallback signature must match original + extra Throwable parameter
    public CompletableFuture<InventoryDTO> inventoryFallback(Long productId, Exception e) {
        log.warn("Inventory circuit open for product {}: {}", productId, e.getMessage());
        return CompletableFuture.completedFuture(InventoryDTO.unavailable(productId));
    }
}
```

---

## Chapter 38: Testing

### 38.1 Testing Pyramid — Strategy

```
        ┌─────────────────────────────────────────────┐
        │               E2E Tests                     │
        │  Slow, expensive, tests whole system        │
        │  Selenium, Cypress, Playwright               │
        └────────────────────────────────────────────-┘
             ┌─────────────────────────────────────┐
             │       Integration Tests              │
             │  Test layers together (DB, HTTP)     │
             │  @SpringBootTest, TestContainers     │
             └─────────────────────────────────────┘
                  ┌─────────────────────────────┐
                  │       Unit Tests            │
                  │  Fast, isolated, mock deps  │
                  │  JUnit 5 + Mockito          │
                  └─────────────────────────────┘

Rule of thumb: 70% unit, 20% integration, 10% E2E
```

### 38.2 JUnit 5 — Complete Reference

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.*;
import org.junit.jupiter.params.provider.*;
import org.junit.jupiter.api.condition.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.*;

@DisplayName("OrderService Unit Tests")  // human-readable test class name
class OrderServiceTest {

    private OrderService service;
    private TestData testData;

    // ── Lifecycle methods ──────────────────────────────────────
    @BeforeAll                               // static: runs ONCE before all tests in this class
    static void setUpClass() {
        System.out.println("Test class setup");
    }

    @AfterAll                                // static: runs ONCE after all tests
    static void tearDownClass() {
        System.out.println("Test class teardown");
    }

    @BeforeEach                              // runs before EACH test
    void setUp() {
        service = new OrderService(new MockOrderRepo(), new MockInventory());
        testData = new TestData();
    }

    @AfterEach                               // runs after EACH test
    void tearDown() {
        // cleanup per test
    }

    // ── Basic test ─────────────────────────────────────────────
    @Test
    @DisplayName("should calculate total with discount correctly")
    void testCalculateTotalWithDiscount() {
        // Given
        Cart cart = testData.cartWith(
            new CartItem("PROD-001", 2, new BigDecimal("50.00")),
            new CartItem("PROD-002", 1, new BigDecimal("25.00"))
        );
        Discount discount = Discount.percentage(10);  // 10% off

        // When
        BigDecimal total = service.calculateTotal(cart, discount);

        // Then
        assertEquals(new BigDecimal("112.50"), total);
        // assertEquals(expected, actual)  ← note: expected FIRST
    }

    // ── Assertions ─────────────────────────────────────────────
    @Test
    void demonstrateAssertions() {
        // Basic
        assertEquals(5, 2 + 3);
        assertNotEquals(4, 2 + 3);
        assertTrue(5 > 3);
        assertFalse(5 < 3);
        assertNull(null);
        assertNotNull("hello");

        // Reference
        String s = "hello";
        assertSame(s, s);           // same reference
        assertNotSame(s, new String("hello")); // different reference

        // Arrays and collections
        assertArrayEquals(new int[]{1,2,3}, new int[]{1,2,3});
        assertIterableEquals(List.of(1,2,3), List.of(1,2,3));

        // String contains
        assertAll("multiple assertions — ALL run even if one fails",
            () -> assertEquals(5, 2 + 3),
            () -> assertTrue("hello".startsWith("h")),
            () -> assertNotNull(service)
        );

        // Exception testing
        IllegalArgumentException ex = assertThrows(
            IllegalArgumentException.class,
            () -> service.createOrder(null)   // should throw
        );
        assertEquals("Cart cannot be null", ex.getMessage());
        assertTrue(ex.getMessage().contains("null"));

        // Does NOT throw
        assertDoesNotThrow(() -> service.calculateTotal(testData.emptyCart(), null));

        // Timeout
        assertTimeout(Duration.ofMillis(100), () -> {
            Thread.sleep(50);   // must complete in 100ms
        });
        // Fail immediately if exceeded (doesn't wait for task to finish):
        assertTimeoutPreemptively(Duration.ofMillis(100), () -> service.quickOp());

        // Custom failure message (lazy string to avoid construction if passing)
        assertEquals(42, service.answer(), () -> "Expected 42 but got: " + service.answer());
    }

    // ── Exception testing (clean pattern) ─────────────────────
    @Test
    @DisplayName("placeOrder with null cart should throw IllegalArgumentException")
    void placeOrder_NullCart_ThrowsIllegalArgument() {
        assertThrows(IllegalArgumentException.class,
            () -> service.placeOrder(null, 1L));
    }

    @Test
    @DisplayName("placeOrder with insufficient stock should throw InsufficientStockException")
    void placeOrder_InsufficientStock_ThrowsException() {
        Cart cart = testData.cartRequiring(100);  // needs 100 units
        // inventory only has 5

        InsufficientStockException ex = assertThrows(
            InsufficientStockException.class,
            () -> service.placeOrder(cart, 1L)
        );
        assertEquals("PROD-001", ex.getProductId());
        assertEquals(5, ex.getAvailable());
        assertEquals(100, ex.getRequired());
    }

    // ── Parameterized tests ────────────────────────────────────
    @ParameterizedTest(name = "discount {0}% on ${1} = ${2}")
    @CsvSource({
        "0,  100.00, 100.00",
        "10, 100.00, 90.00",
        "50, 100.00, 50.00",
        "100,100.00, 0.00",
        "10, 99.99,  89.99"
    })
    void testDiscountCalculation(int pct, String amount, String expected) {
        BigDecimal result = service.applyDiscount(new BigDecimal(amount), pct);
        assertEquals(new BigDecimal(expected), result);
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "  ", "\t"})
    void testBlankProductName_ShouldFail(String name) {
        assertThrows(IllegalArgumentException.class,
            () -> service.createProduct(name, new BigDecimal("9.99")));
    }

    @ParameterizedTest
    @EnumSource(value = OrderStatus.class, names = {"DELIVERED", "CANCELLED"})
    void testFinalStatusCannotBeModified(OrderStatus status) {
        Order order = new Order(status);
        assertThrows(IllegalStateException.class, () -> service.updateStatus(order, OrderStatus.PROCESSING));
    }

    @ParameterizedTest
    @MethodSource("provideOrderScenarios")
    void testOrderTotal(Order order, BigDecimal expectedTotal) {
        assertEquals(expectedTotal, service.calculateTotal(order));
    }

    static Stream<Arguments> provideOrderScenarios() {
        return Stream.of(
            Arguments.of(new Order(100.00, 0),    new BigDecimal("100.00")),
            Arguments.of(new Order(100.00, 10),   new BigDecimal("90.00")),
            Arguments.of(new Order(0.00,   100),  new BigDecimal("0.00"))
        );
    }

    // ── Conditional execution ──────────────────────────────────
    @Test
    @EnabledOnOs(OS.WINDOWS)
    void runOnlyOnWindows() { ... }

    @Test
    @EnabledOnJre(JRE.JAVA_21)
    void runOnlyOnJava21() { ... }

    @Test
    @EnabledIfEnvironmentVariable(named = "CI", matches = "true")
    void runOnlyInCI() { ... }

    @Test
    void withAssumption() {
        assumeTrue(System.getenv("FEATURE_FLAG") != null,
            "Skipping: FEATURE_FLAG not set");
        // Test only runs if assumption is true
        service.featureMethod();
    }

    // ── Nested tests — logical grouping ───────────────────────
    @Nested
    @DisplayName("when cart is empty")
    class WhenCartIsEmpty {
        private Cart emptyCart;

        @BeforeEach void setUp() { emptyCart = new Cart(); }

        @Test void totalShouldBeZero()    { assertEquals(BigDecimal.ZERO, service.calculateTotal(emptyCart, null)); }
        @Test void shouldNotAllowOrder()  { assertThrows(EmptyCartException.class, () -> service.placeOrder(emptyCart, 1L)); }
    }

    @Nested
    @DisplayName("when cart has items")
    class WhenCartHasItems {
        private Cart cart;

        @BeforeEach void setUp() { cart = testData.standardCart(); }

        @Test void totalShouldBePositive() { assertTrue(service.calculateTotal(cart, null).compareTo(BigDecimal.ZERO) > 0); }
        @Test void shouldCreateOrder()     { assertDoesNotThrow(() -> service.placeOrder(cart, 1L)); }
    }

    // ── Test ordering (when execution order matters) ───────────
    @TestMethodOrder(MethodOrderer.OrderAnnotation.class)
    static class OrderedTests {
        @Test @Order(1) void first()  { }
        @Test @Order(2) void second() { }
        @Test @Order(3) void third()  { }
    }
}
```

### 38.3 Mockito — Complete Reference

```java
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.BDDMockito.*;   // Given/When/Then style

@ExtendWith(MockitoExtension.class)    // initializes mocks automatically
class OrderServiceMockitoTest {

    @Mock
    private OrderRepository orderRepo;     // creates a mock

    @Mock
    private InventoryService inventory;

    @Mock
    private EmailService emailService;

    @Spy
    private PricingEngine pricingEngine;   // real object, but spy = can verify calls

    @InjectMocks
    private OrderService orderService;     // creates instance, injects @Mock/@Spy fields

    @Captor
    private ArgumentCaptor<Order> orderCaptor;

    // ── Stubbing — configure what mocks return ─────────────────
    @Test
    void testPlaceOrder_Success() {
        // GIVEN — configure mock behaviour
        Cart cart = testData.cartWith("PROD-001", 2);
        Customer customer = testData.customer(1L, "Alice");

        when(inventory.isAvailable("PROD-001", 2))
            .thenReturn(true);

        when(orderRepo.save(any(Order.class)))
            .thenAnswer(invocation -> {
                Order o = invocation.getArgument(0);
                o.setId(42L);         // simulate DB auto-generating ID
                return o;
            });

        doNothing().when(emailService).sendConfirmation(any(Order.class));
        // or: when(emailService.sendConfirmation(any())).thenReturn(void); — for void methods

        // WHEN — call the method under test
        Order result = orderService.placeOrder(cart, customer.getId());

        // THEN — verify result and interactions
        assertNotNull(result);
        assertEquals(42L, result.getId());
        assertEquals(OrderStatus.CONFIRMED, result.getStatus());

        // Verify mocks were called correctly
        verify(inventory).isAvailable("PROD-001", 2);         // called once exactly
        verify(orderRepo, times(1)).save(any(Order.class));   // called exactly once
        verify(emailService, times(1)).sendConfirmation(result);

        // Capture and inspect argument passed to save()
        verify(orderRepo).save(orderCaptor.capture());
        Order savedOrder = orderCaptor.getValue();
        assertEquals(1L, savedOrder.getCustomerId());
        assertEquals("PROD-001", savedOrder.getItems().get(0).getProductId());
    }

    // ── Exception stubbing ─────────────────────────────────────
    @Test
    void testPlaceOrder_InventoryServiceDown_ThrowsException() {
        when(inventory.isAvailable(anyString(), anyInt()))
            .thenThrow(new ServiceUnavailableException("Inventory service down"));

        assertThrows(ServiceUnavailableException.class,
            () -> orderService.placeOrder(testData.standardCart(), 1L));

        // Verify order was never saved (transaction rolled back)
        verify(orderRepo, never()).save(any());
        verify(emailService, never()).sendConfirmation(any());
    }

    // ── Multiple stubbing — different on each call ─────────────
    @Test
    void testRetryLogic() {
        when(externalApi.call("data"))
            .thenThrow(new TimeoutException())    // 1st call: timeout
            .thenThrow(new TimeoutException())    // 2nd call: timeout
            .thenReturn("success");               // 3rd call: success

        String result = service.callWithRetry("data");
        assertEquals("success", result);
        verify(externalApi, times(3)).call("data");
    }

    // ── Argument matchers ──────────────────────────────────────
    @Test
    void testArgumentMatchers() {
        // Exact value
        when(repo.findById(42L)).thenReturn(Optional.of(order));

        // Any value of a type
        when(repo.findById(anyLong())).thenReturn(Optional.of(order));
        when(service.process(any())).thenReturn(result);           // any non-null
        when(service.process(any(Cart.class))).thenReturn(result); // any Cart

        // Predicates
        when(repo.findByStatus(eq("PENDING"))).thenReturn(pendingOrders);
        when(repo.findByTotal(argThat(t -> t.compareTo(BigDecimal.ZERO) > 0))).thenReturn(list);

        // String matchers
        when(service.search(contains("Alice"))).thenReturn(results);
        when(service.search(startsWith("Al"))).thenReturn(results);
        when(service.search(matches("[A-Z].*"))).thenReturn(results);

        // Null checks
        when(service.process(isNull())).thenThrow(NullPointerException.class);
        when(service.process(notNull())).thenReturn(ok);

        // Mixed: if using matchers, ALL arguments must use matchers
        // wrong: when(service.find(1L, "name"))         ← mixing real value + no matcher
        // right: when(service.find(eq(1L), eq("name"))) ← all matchers
        // or:    when(service.find(eq(1L), "name"))     ← compile error
    }

    // ── Verify interactions ────────────────────────────────────
    @Test
    void testVerifications() {
        service.doSomething();

        verify(mock).method();                          // called exactly once
        verify(mock, times(3)).method();               // called exactly 3 times
        verify(mock, atLeast(1)).method();             // called at least once
        verify(mock, atMost(5)).method();              // called at most 5 times
        verify(mock, never()).method();                // never called

        verifyNoMoreInteractions(mock, anotherMock);   // no other interactions
        verifyNoInteractions(ignoredMock);             // no interactions at all

        // Ordered verification
        InOrder inOrder = inOrder(mock1, mock2);
        inOrder.verify(mock1).firstMethod();
        inOrder.verify(mock2).secondMethod();
        inOrder.verify(mock1).thirdMethod();
    }

    // ── BDD Style (Given-When-Then) ────────────────────────────
    @Test
    void testBddStyle() {
        // given
        given(orderRepo.findById(1L)).willReturn(Optional.of(order));
        given(inventory.isAvailable(anyString(), anyInt())).willReturn(true);

        // when
        OrderDTO result = orderService.getOrder(1L);

        // then
        then(orderRepo).should().findById(1L);
        then(inventory).shouldHaveNoInteractions();
        assertNotNull(result);
    }
}
```

### 38.4 Spring Boot Testing — Slices and Integration

```java
// ── @SpringBootTest — loads FULL application context ──────────
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class OrderIntegrationTest {

    @Autowired private TestRestTemplate restTemplate;
    @Autowired private OrderRepository orderRepo;
    @LocalServerPort private int port;

    @BeforeEach void cleanDb() { orderRepo.deleteAll(); }

    @Test
    void createOrder_ShouldPersistAndReturn201() {
        CreateOrderRequest req = new CreateOrderRequest(1L, List.of(
            new OrderItemRequest("PROD-001", 2, new BigDecimal("49.99"))
        ));

        ResponseEntity<OrderDTO> response = restTemplate
            .withBasicAuth("user", "password")
            .postForEntity("/api/orders", req, OrderDTO.class);

        assertEquals(201, response.getStatusCode().value());
        assertNotNull(response.getBody().getId());
        assertEquals(1, orderRepo.count());
    }

    // MockBean replaces a real bean in context with a mock
    @MockBean
    private PaymentGateway paymentGateway;

    @Test
    void createOrder_PaymentFails_ShouldReturn402() {
        when(paymentGateway.charge(any(), any()))
            .thenThrow(new PaymentDeclinedException("Card declined"));

        ResponseEntity<ApiError> response = restTemplate
            .postForEntity("/api/orders", validRequest, ApiError.class);

        assertEquals(402, response.getStatusCode().value());
        assertEquals("PAYMENT_DECLINED", response.getBody().getError());
        assertEquals(0, orderRepo.count());   // order not persisted
    }
}

// ── @WebMvcTest — loads only Web layer (Controller + related) ──
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;  // JSON serializer

    @MockBean private OrderService orderService;  // mock the service layer

    @Test
    void getOrder_Found_Returns200WithOrder() throws Exception {
        OrderDTO order = new OrderDTO(1L, "CONFIRMED", new BigDecimal("99.99"));
        when(orderService.findById(1L)).thenReturn(Optional.of(order));

        mockMvc.perform(
            get("/api/orders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", "Bearer " + testToken)
            )
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.status").value("CONFIRMED"))
            .andExpect(jsonPath("$.total").value(99.99))
            .andDo(print());  // prints full request/response to console
    }

    @Test
    void createOrder_InvalidInput_Returns400() throws Exception {
        CreateOrderRequest invalid = new CreateOrderRequest(null, List.of());  // null customerId

        mockMvc.perform(
            post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalid))
            )
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.validationErrors.customerId").value("Customer ID is required"))
            .andExpect(jsonPath("$.validationErrors.items").value("At least one item required"));
    }

    @Test
    void getOrder_NotFound_Returns404() throws Exception {
        when(orderService.findById(99L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/orders/99"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.status").value(404));
    }

    @Test
    void getOrder_Unauthorized_Returns401() throws Exception {
        // no Authorization header
        mockMvc.perform(get("/api/orders/1"))
            .andExpect(status().isUnauthorized());
    }
}

// ── @DataJpaTest — loads only JPA layer ────────────────────────
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)  // use real DB
// Default: uses H2 in-memory; Replace.NONE = use configured datasource
class OrderRepositoryTest {

    @Autowired private OrderRepository orderRepo;
    @Autowired private TestEntityManager em;  // helper for test setup

    @Test
    @Transactional
    void findByCustomerId_ShouldReturnOnlyThatCustomersOrders() {
        // Setup — use em.persist for test data
        Customer c1 = em.persist(new Customer("Alice"));
        Customer c2 = em.persist(new Customer("Bob"));
        em.persist(new Order(c1.getId(), "CONFIRMED", BigDecimal.TEN));
        em.persist(new Order(c1.getId(), "PENDING",   BigDecimal.ONE));
        em.persist(new Order(c2.getId(), "CONFIRMED", BigDecimal.TEN));
        em.flush();   // write to DB so queries can find them
        em.clear();   // clear first-level cache to force DB query

        List<Order> aliceOrders = orderRepo.findByCustomerId(c1.getId());

        assertEquals(2, aliceOrders.size());
        assertTrue(aliceOrders.stream().allMatch(o -> o.getCustomerId().equals(c1.getId())));
    }

    @Test
    void findTopSpenders_ShouldReturnOrderedByTotalDesc() {
        em.persist(new Order(1L, "DELIVERED", new BigDecimal("50.00")));
        em.persist(new Order(2L, "DELIVERED", new BigDecimal("200.00")));
        em.persist(new Order(1L, "DELIVERED", new BigDecimal("75.00")));
        em.flush();

        List<CustomerSpending> result = orderRepo.findTopSpenders(
            PageRequest.of(0, 10));

        assertEquals(2, result.size());
        assertEquals(2L, result.get(0).getCustomerId());   // Bob: 200
        assertEquals(1L, result.get(1).getCustomerId());   // Alice: 125
    }
}

// ── @RestClientTest — test HTTP clients ───────────────────────
@RestClientTest(ExternalApiClient.class)
class ExternalApiClientTest {

    @Autowired private ExternalApiClient client;
    @Autowired private MockRestServiceServer server;

    @Test
    void fetchProduct_ShouldCallCorrectEndpoint() {
        server.expect(once(), requestTo("https://api.external.com/products/1"))
              .andExpect(method(HttpMethod.GET))
              .andExpect(header("Authorization", "Bearer test-key"))
              .andRespond(withSuccess(
                  "{\"id\":1,\"name\":\"Widget\",\"price\":9.99}",
                  MediaType.APPLICATION_JSON));

        ProductDTO product = client.fetchProduct(1L);

        assertEquals(1L, product.getId());
        assertEquals("Widget", product.getName());
        server.verify();   // verify all expected requests were made
    }
}
```

### 38.5 TestContainers — Real Databases in Tests

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>1.19.4</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>mysql</artifactId>
    <version>1.19.4</version>
    <scope>test</scope>
</dependency>
```

```java
@SpringBootTest
@Testcontainers
class RealDatabaseTest {

    // Start a real MySQL container for this test class
    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test")
        .withInitScript("test-schema.sql");   // run SQL on startup

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        // Tell Spring to use the container's dynamic URL/port
        registry.add("spring.datasource.url",      mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }

    @Autowired private OrderRepository orderRepo;

    @Test
    void complexQueryOnRealDatabase() {
        // This test runs against a REAL MySQL instance in Docker
        // No mocking — true integration test
        orderRepo.save(new Order(...));
        List<Order> found = orderRepo.findByComplexCriteria(...);
        assertFalse(found.isEmpty());
    }
}
```

---

## Chapter 39: Build Tools — Maven & Gradle

### 39.1 Maven — The Full Picture

Maven is a build tool that standardises project structure, dependency management, and build lifecycle.

**Standard Directory Layout:**
```
my-project/
├── pom.xml                         ← Project Object Model (configuration)
├── src/
│   ├── main/
│   │   ├── java/                   ← production source code
│   │   │   └── com/example/...
│   │   └── resources/              ← production resources (application.properties)
│   └── test/
│       ├── java/                   ← test source code
│       └── resources/              ← test resources
└── target/                         ← build output (generated by Maven)
    ├── classes/                    ← compiled .class files
    ├── test-classes/               ← compiled test .class files
    └── my-project-1.0.jar          ← packaged artifact
```

**pom.xml — Complete Reference:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <!-- ── Project Identity (the GAV coordinates) ────────────── -->
    <groupId>com.example</groupId>          <!-- organisation/group -->
    <artifactId>my-service</artifactId>     <!-- project name -->
    <version>1.2.3-SNAPSHOT</version>       <!-- SNAPSHOT = in development -->
    <packaging>jar</packaging>              <!-- jar / war / pom -->
    <name>My Service</name>
    <description>Order management service</description>

    <!-- ── Spring Boot Parent — manages versions for 200+ deps ── -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.3</version>
        <relativePath/>
    </parent>

    <!-- ── Properties — centralize versions ─────────────────── -->
    <properties>
        <java.version>21</java.version>
        <mapstruct.version>1.5.5.Final</mapstruct.version>
        <springdoc.version>2.3.0</springdoc.version>
    </properties>

    <!-- ── Dependencies ──────────────────────────────────────── -->
    <dependencies>
        <!-- Spring Boot starters — bundles of related dependencies -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <!-- includes: spring-mvc, jackson, tomcat, spring-core, etc. -->
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>  <!-- not needed at compile time -->
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Code generation -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>  <!-- not transitive to dependents -->
        </dependency>
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>${mapstruct.version}</version>
        </dependency>

        <!-- JWT -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.12.5</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.12.5</version>
            <scope>runtime</scope>
        </dependency>

        <!-- API Documentation -->
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>${springdoc.version}</version>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>  <!-- only in test classpath -->
            <!-- includes: JUnit 5, Mockito, AssertJ, Hamcrest, MockMvc -->
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>mysql</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <!-- ── Dependency Management — set versions without adding deps ── -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>2023.0.0</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>testcontainers-bom</artifactId>
                <version>1.19.4</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- ── Build Configuration ───────────────────────────────── -->
    <build>
        <plugins>
            <!-- Spring Boot plugin: creates fat JAR with all dependencies -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- Annotation processors for Lombok + MapStruct -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </path>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>${mapstruct.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>

            <!-- Surefire: runs unit tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>**/*IntegrationTest.java</exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- Failsafe: runs integration tests (bound to verify phase) -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-failsafe-plugin</artifactId>
                <executions>
                    <execution>
                        <goals>
                            <goal>integration-test</goal>
                            <goal>verify</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <includes>
                        <include>**/*IntegrationTest.java</include>
                    </includes>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <!-- ── Profiles ──────────────────────────────────────────── -->
    <profiles>
        <profile>
            <id>docker</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>com.google.cloud.tools</groupId>
                        <artifactId>jib-maven-plugin</artifactId>
                        <configuration>
                            <to><image>myrepo/my-service:${project.version}</image></to>
                        </configuration>
                    </plugin>
                </plugins>
            </build>
        </profile>
    </profiles>
</project>
```

**Maven Build Lifecycle Phases:**
```
validate   → check project structure is correct
compile    → compile source code to target/classes/
test       → run unit tests (via Surefire)
package    → create JAR/WAR in target/
verify     → run integration tests (via Failsafe) + quality checks
install    → copy artifact to ~/.m2/repository (local Maven repo)
deploy     → upload artifact to remote repository (Nexus, Artifactory)

Running a phase runs ALL previous phases too:
  mvn package  =  validate + compile + test + package
```

```bash
# Common Maven commands
mvn clean                           # delete target/ directory
mvn compile                         # compile only
mvn test                            # compile + run unit tests
mvn package                         # create JAR (skipping tests if -DskipTests)
mvn package -DskipTests             # skip test execution (still compiles tests)
mvn package -Dmaven.test.skip=true  # skip test compilation AND execution
mvn verify                          # run all tests including integration
mvn install                         # package + install to local repo
mvn spring-boot:run                 # run Spring Boot app directly
mvn spring-boot:build-image         # build Docker image with Cloud Native Buildpacks
mvn dependency:tree                 # show full dependency hierarchy
mvn dependency:analyze              # find unused/undeclared dependencies
mvn versions:display-dependency-updates  # show available version updates
mvn help:effective-pom              # show fully-resolved pom (after inheritance)
mvn -P docker package               # activate 'docker' profile
```

### 39.2 Gradle — The Modern Build Tool

```groovy
// build.gradle (Groovy DSL) — Spring Boot project
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.3'
    id 'io.spring.dependency-management' version '1.1.4'
}

group   = 'com.example'
version = '1.0.0-SNAPSHOT'
sourceCompatibility = '21'

configurations {
    compileOnly { extendsFrom annotationProcessor }
}

repositories {
    mavenCentral()
    // Custom repo:
    // maven { url 'https://repo.mycompany.com/releases' }
}

ext {
    set('springCloudVersion', '2023.0.0')
    set('testcontainersVersion', '1.19.4')
}

dependencies {
    // Spring Boot starters
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-security'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-actuator'

    // Cloud
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-client'
    implementation 'org.springframework.cloud:spring-cloud-starter-openfeign'

    // Database
    runtimeOnly 'com.mysql:mysql-connector-j'

    // Lombok
    compileOnly    'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'

    // Testing
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.springframework.security:spring-security-test'
    testImplementation 'org.testcontainers:junit-jupiter'
    testImplementation 'org.testcontainers:mysql'
    testRuntimeOnly    'com.h2database:h2'
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
        mavenBom "org.testcontainers:testcontainers-bom:${testcontainersVersion}"
    }
}

// Custom tasks
tasks.named('test') {
    useJUnitPlatform()
    // Exclude integration tests from 'test' task
    exclude '**/*IntegrationTest*'
    jvmArgs '-Xmx512m'
}

task integrationTest(type: Test) {
    useJUnitPlatform()
    include '**/*IntegrationTest*'
    shouldRunAfter test
}

// Separate unit and integration test source sets
sourceSets {
    integrationTest {
        java { srcDir 'src/integrationTest/java' }
        resources { srcDir 'src/integrationTest/resources' }
        compileClasspath += sourceSets.main.output + configurations.testRuntimeClasspath
        runtimeClasspath += output + compileClasspath
    }
}
```

```kotlin
// build.gradle.kts (Kotlin DSL) — modern, type-safe
plugins {
    java
    id("org.springframework.boot") version "3.2.3"
    id("io.spring.dependency-management") version "1.1.4"
}

group   = "com.example"
version = "1.0.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_21
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("com.mysql:mysql-connector-j")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

```bash
# Gradle commands
./gradlew clean                     # delete build/ directory
./gradlew compileJava               # compile only
./gradlew test                      # run tests
./gradlew build                     # compile + test + jar
./gradlew bootRun                   # run Spring Boot app
./gradlew bootJar                   # create fat JAR in build/libs/
./gradlew bootBuildImage            # build Docker image
./gradlew dependencies              # show dependency tree
./gradlew dependencyInsight --dependency spring-core  # trace one dependency
./gradlew -t test                   # continuous test (re-run on file change)
./gradlew test --tests "com.example.OrderServiceTest"  # run specific test
./gradlew test --tests "*.OrderServiceTest.testPlaceOrder"  # specific method
./gradlew build -x test             # skip tests
```

**Maven vs Gradle — choosing:**

| Aspect | Maven | Gradle |
|--------|-------|--------|
| Configuration | XML (verbose but clear) | Groovy/Kotlin DSL (concise) |
| Build speed | Slower | Faster (incremental, parallel, cache) |
| Flexibility | Convention over config | Highly customisable |
| Learning curve | Easier | Steeper |
| IDE support | Excellent | Excellent |
| Ecosystem | Huge | Large, growing |
| Spring Boot default | Both supported | Both supported |
| Enterprise adoption | High | Growing fast |

> For new Spring Boot projects: either works. Maven is simpler; Gradle is faster for large projects.

---

## Appendix: Quick Reference

### HTTP Status Codes for REST APIs

| Code | Meaning | When to Return |
|------|---------|----------------|
| 200 OK | Success | GET, PUT, PATCH with response body |
| 201 Created | Resource created | POST; include Location header |
| 204 No Content | Success, no body | DELETE, PUT/PATCH with no response body |
| 400 Bad Request | Invalid input | Validation errors, malformed JSON |
| 401 Unauthorized | Not authenticated | No/invalid token |
| 403 Forbidden | Not authorized | Valid token but insufficient permissions |
| 404 Not Found | Resource absent | Resource doesn't exist |
| 409 Conflict | State conflict | Duplicate unique field, optimistic lock conflict |
| 422 Unprocessable Entity | Semantic error | Valid JSON but invalid business logic |
| 429 Too Many Requests | Rate limited | Rate limiter triggered |
| 500 Internal Server Error | Server bug | Unhandled exception |
| 502 Bad Gateway | Upstream failure | Downstream service returned error |
| 503 Service Unavailable | Service down | Circuit breaker open, maintenance |

### Common JPA Annotations Summary

| Annotation | Purpose |
|-----------|---------|
| `@Entity` | Mark class as JPA entity |
| `@Table(name="...")` | Map to specific table |
| `@Id` | Primary key |
| `@GeneratedValue(strategy=IDENTITY)` | Auto-increment |
| `@Column(nullable=false)` | Column constraint |
| `@ManyToOne(fetch=LAZY)` | Many-to-one relationship |
| `@OneToMany(mappedBy="...")` | One-to-many (inverse side) |
| `@JoinColumn(name="fk_col")` | Foreign key column |
| `@Transient` | Don't persist this field |
| `@Enumerated(EnumType.STRING)` | Store enum as string |
| `@Version` | Optimistic locking |
| `@PrePersist` / `@PreUpdate` | Lifecycle callback |

### Spring Annotations Summary

| Annotation | Layer | Purpose |
|-----------|-------|---------|
| `@Component` | Any | Generic Spring bean |
| `@Service` | Business | Business logic |
| `@Repository` | Data | DAO; translates exceptions |
| `@Controller` | Web | MVC controller |
| `@RestController` | Web | REST controller (returns JSON) |
| `@Autowired` | Any | Inject dependency |
| `@Qualifier("name")` | Any | Specify which bean to inject |
| `@Primary` | Any | Default bean when multiple exist |
| `@Value("${prop}")` | Any | Inject property value |
| `@Configuration` | Config | Contains `@Bean` methods |
| `@Bean` | Config | Declare a managed bean |
| `@PostConstruct` | Any | Run after injection |
| `@PreDestroy` | Any | Run before destruction |
| `@Transactional` | Service | Wrap in transaction |
| `@GetMapping` | Controller | HTTP GET handler |
| `@PostMapping` | Controller | HTTP POST handler |
| `@PathVariable` | Controller | URL path segment |
| `@RequestParam` | Controller | Query string parameter |
| `@RequestBody` | Controller | Request body (JSON) |
| `@ResponseBody` | Controller | Return value is response body |
| `@Valid` | Controller | Trigger validation |
| `@PreAuthorize("...")` | Service | Method security check |

---

*Complete Java & Spring Boot Mastery Guide — Java 21 + Spring Boot 3.x + Jakarta EE 10*
*Covers: Core Java, DSA, JDBC, Servlets, JPA, Spring Core/AOP/Boot/MVC/REST/Security/Cloud, Testing, Build Tools*
