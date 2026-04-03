# The Complete Python Mastery Guide
> From CPython internals and the data model through async/await, metaprogramming, the scientific stack, and production patterns. Every concept explained from first principles.

---

## Table of Contents

### Part I — Language Foundations
1. [Why Python? CPython Internals & Execution Model](#chapter-1-why-python-cpython-internals)
2. [Types, Variables & the Object Model](#chapter-2-types-variables--the-object-model)
3. [Operators, Expressions & Built-in Functions](#chapter-3-operators-expressions--built-in-functions)
4. [Control Flow](#chapter-4-control-flow)
5. [Functions — First-Class Everything](#chapter-5-functions--first-class-everything)
6. [Closures & Decorators](#chapter-6-closures--decorators)
7. [Generators & Iterators — The Protocol](#chapter-7-generators--iterators)

### Part II — Data Structures
8. [Strings — Deep Dive](#chapter-8-strings--deep-dive)
9. [Lists, Tuples & Arrays](#chapter-9-lists-tuples--arrays)
10. [Dictionaries & Sets — Hash Tables Explained](#chapter-10-dictionaries--sets)
11. [Comprehensions & Functional Tools](#chapter-11-comprehensions--functional-tools)

### Part III — Object-Oriented Python
12. [Classes & the Data Model](#chapter-12-classes--the-data-model)
13. [Inheritance, MRO & Mixins](#chapter-13-inheritance-mro--mixins)
14. [Dunder Methods — The Full Protocol](#chapter-14-dunder-methods--the-full-protocol)
15. [Descriptors, Properties & Slots](#chapter-15-descriptors-properties--slots)
16. [Metaclasses](#chapter-16-metaclasses)

### Part IV — Modern Python
17. [Type Hints & Static Analysis](#chapter-17-type-hints--static-analysis)
18. [dataclasses, attrs & Pydantic](#chapter-18-dataclasses-attrs--pydantic)
19. [Context Managers](#chapter-19-context-managers)
20. [Async/Await & asyncio](#chapter-20-asyncawait--asyncio)

### Part V — Standard Library & Ecosystem
21. [File I/O, os & pathlib](#chapter-21-file-io-os--pathlib)
22. [Error Handling — Exceptions Deep Dive](#chapter-22-error-handling)
23. [Modules, Packages & Imports](#chapter-23-modules-packages--imports)
24. [Testing — unittest, pytest & mocking](#chapter-24-testing)
25. [Concurrency — threading, multiprocessing, concurrent.futures](#chapter-25-concurrency)
26. [The Standard Library — Essential Modules](#chapter-26-the-standard-library)

### Part VI — Production Python
27. [Performance — Profiling & Optimization](#chapter-27-performance)
28. [Packaging — pip, Poetry, pyproject.toml](#chapter-28-packaging)
29. [Design Patterns in Python](#chapter-29-design-patterns)
30. [Data & Scientific Stack — NumPy, pandas, requests](#chapter-30-data--scientific-stack)

---

# PART I — LANGUAGE FOUNDATIONS

---

## Chapter 1: Why Python? CPython Internals

### 1.1 Python's Design Philosophy

```python
import this   # The Zen of Python, by Tim Peters
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Errors should never pass silently.
# There should be one-- and preferably only one --obvious way to do it.
# Now is better than never. Although never is often better than *right* now.
```

Python prioritises **developer productivity and code readability** over raw execution speed. The philosophy: programmer time is more valuable than CPU time for most applications.

**Where Python excels:**
- Rapid prototyping and scripting
- Data science, ML, AI (NumPy, pandas, scikit-learn, PyTorch, TensorFlow)
- Web development (Django, FastAPI, Flask)
- Automation and DevOps
- Glue code — integrating systems

**Where Python is NOT ideal:**
- CPU-intensive computation (use C extensions, Cython, or Rust via PyO3)
- Mobile apps (though Kivy exists)
- Systems programming (use C, C++, Rust, Go)

### 1.2 CPython — How Python Actually Runs

CPython (the reference implementation) is an **interpreter** written in C. Execution flow:

```
Source code: hello.py
      │
      ▼ ① Lexing/Tokenizing
         Converts source text to tokens (keywords, identifiers, operators...)
      │
      ▼ ② Parsing
         Tokens → Abstract Syntax Tree (AST)
         View with: import ast; print(ast.dump(ast.parse("x = 1 + 2")))
      │
      ▼ ③ Compilation
         AST → bytecode (.pyc files in __pycache__)
         View with: import dis; dis.dis(lambda x: x + 1)
      │
      ▼ ④ Execution
         CPython's eval loop interprets bytecode instruction by instruction
         PVM (Python Virtual Machine) = the eval loop in ceval.c
```

```python
import dis
import ast

# See the AST
tree = ast.parse("x = 1 + 2")
print(ast.dump(tree, indent=2))
# Module(body=[Assign(targets=[Name(id='x')], value=BinOp(left=Constant(value=1),
#              op=Add(), right=Constant(value=2)))])

# See the bytecode
def greet(name):
    return "Hello, " + name + "!"

dis.dis(greet)
#   2           0 RESUME          0
#   3           2 LOAD_CONST      1 ('Hello, ')
#               4 LOAD_FAST       0 (name)
#               6 BINARY_OP      0 (+)
#               8 LOAD_CONST      2 ('!')
#              10 BINARY_OP      0 (+)
#              12 RETURN_VALUE
```

### 1.3 The GIL — Global Interpreter Lock

The GIL is CPython's biggest architectural limitation and most misunderstood feature:

```
What it is:
  A mutex that allows only ONE Python thread to execute bytecode at a time.
  It's held by the currently running thread; released at regular intervals
  (every 5ms by default, sys.getswitchinterval()) or during I/O operations.

Why it exists:
  CPython's memory management (reference counting) is not thread-safe.
  Rather than making every object operation thread-safe (slow), the GIL
  serialises all Python execution (simpler).

What this means:
  ❌ CPU-bound multithreaded Python is NOT parallel (threads take turns)
  ✅ I/O-bound multithreaded Python IS faster (GIL released during I/O waits)
  ✅ Multiple PROCESSES are parallel (each has its own GIL)
  ✅ C extensions can release the GIL for CPU-bound work (NumPy does this)

Python 3.13+: experimental "free-threaded" mode (--disable-gil)
              True multithreading, but ecosystem compatibility still evolving.
```

```python
import threading
import time

# GIL demo: CPU-bound threads don't run in parallel
def count_up(n):
    x = 0
    for _ in range(n):
        x += 1

start = time.time()
# Sequential
count_up(50_000_000)
count_up(50_000_000)
print(f"Sequential: {time.time()-start:.2f}s")

start = time.time()
# "Parallel" threads — same speed because of GIL!
t1 = threading.Thread(target=count_up, args=(50_000_000,))
t2 = threading.Thread(target=count_up, args=(50_000_000,))
t1.start(); t2.start(); t1.join(); t2.join()
print(f"Threaded:   {time.time()-start:.2f}s")  # ~same as sequential

# Fix: use multiprocessing for CPU-bound
from multiprocessing import Process
start = time.time()
p1 = Process(target=count_up, args=(50_000_000,))
p2 = Process(target=count_up, args=(50_000_000,))
p1.start(); p2.start(); p1.join(); p2.join()
print(f"Processes:  {time.time()-start:.2f}s")  # ~half the time
```

### 1.4 Reference Counting and Garbage Collection

```python
import sys
import gc

# Every Python object has a reference count
x = [1, 2, 3]
print(sys.getrefcount(x))    # 2 (x + argument to getrefcount)

y = x                         # another reference
print(sys.getrefcount(x))    # 3

del y                         # remove reference
print(sys.getrefcount(x))    # 2

# When refcount hits 0: object is immediately deallocated
# (unlike GC languages where deletion is non-deterministic)

# But: circular references are NOT handled by reference counting!
class Node:
    def __init__(self): self.next = None

a = Node()
b = Node()
a.next = b    # a → b
b.next = a    # b → a (cycle!)
del a; del b  # refcounts don't reach 0! Cycle must be collected by GC.

# Python's cyclic GC (generational) handles cycles
gc.collect()    # force collection
gc.get_count()  # (gen0, gen1, gen2) object counts
gc.disable()    # disable cyclic GC (if you know you have no cycles — faster)

# __del__ method: called when object is garbage collected
# WARNING: __del__ delays GC of objects in cycles; avoid if possible
```

### 1.5 Python Versions and Implementations

```
CPython:   Reference implementation (C); what everyone uses
PyPy:      JIT-compiled Python; 3-10x faster for CPU-bound; compatible with most code
Jython:    Python on JVM; access to Java libraries; no GIL
IronPython: Python on .NET/CLR
MicroPython: Python for microcontrollers (ESP32, Raspberry Pi Pico)
GraalPython: Python on GraalVM; polyglot (call Java, JS, Ruby, R)

Python version history:
Python 2.7: EOL 2020 — DO NOT USE for new code
Python 3.8:  walrus operator :=, positional-only params /
Python 3.9:  dict|dict merge, list[str] type hints
Python 3.10: match/case, better error messages, parenthesized context managers
Python 3.11: 10-60% faster than 3.10, tomllib, exception notes
Python 3.12: f-string improvements, @override, type parameter syntax
Python 3.13: free-threaded mode (no GIL), interactive REPL improvements

Use Python 3.11+ for best performance.
```

---

## Chapter 2: Types, Variables & the Object Model

### 2.1 Everything Is an Object

In Python, EVERYTHING is an object — integers, functions, classes, modules, `None`. Every object has:
- An **identity** (memory address): `id(obj)`
- A **type**: `type(obj)`
- A **value**: the data

```python
# Even "primitives" are objects
x = 42
print(type(x))       # <class 'int'>
print(id(x))         # memory address (e.g., 140234567890)
print(x.__class__)   # <class 'int'>

# Functions are objects
def greet(name): return f"Hello, {name}!"
print(type(greet))     # <class 'function'>
greet.custom_attr = "I'm a function attribute!"  # ← adding attributes to functions

# Classes are objects too
print(type(int))        # <class 'type'>
print(type(type))       # <class 'type'> (type is its own metaclass)
print(isinstance(int, type))  # True
```

### 2.2 Variable Assignment — Names, Not Boxes

Python variables are **names** (labels/references) bound to objects. Assignment doesn't copy — it creates a new binding.

```python
# Name binding, not value copying
x = [1, 2, 3]      # x is a name bound to a list object
y = x               # y is ANOTHER name for the SAME object
y.append(4)
print(x)            # [1, 2, 3, 4] — x sees the change (same object!)

# To copy:
z = x.copy()        # shallow copy — new list, same elements
z.append(5)
print(x)            # [1, 2, 3, 4] — unchanged
print(z)            # [1, 2, 3, 4, 5]

import copy
deep = copy.deepcopy(x)  # deep copy — recursively copies nested objects

# Augmented assignment on immutables creates new objects
a = 5
print(id(a))        # some address e.g. 140234001234
a += 1              # creates new int 6, binds 'a' to it
print(id(a))        # DIFFERENT address!

# Augmented assignment on mutables modifies in-place
lst = [1, 2]
print(id(lst))      # some address
lst += [3]          # calls list.__iadd__ → modifies in place!
print(id(lst))      # SAME address
```

### 2.3 Integer Caching and Identity vs Equality

```python
# CPython caches small integers (-5 to 256) and interned strings
a = 5
b = 5
print(a is b)       # True — same cached object
print(a == b)       # True

a = 1000
b = 1000
print(a is b)       # False (in most contexts) — large ints not cached
print(a == b)       # True

# is checks IDENTITY (same object in memory)
# == checks EQUALITY (same value, calls __eq__)
# NEVER use 'is' to compare values — use 'is' only for None, True, False

# Correct None check:
x = None
if x is None: print("x is None")   # ✅ correct
if x == None: print("x is None")   # ⚠️ works but wrong — custom __eq__ could lie

# String interning
s1 = "hello"
s2 = "hello"
print(s1 is s2)     # True — Python interns string literals
s3 = "".join(["h","e","l","l","o"])
print(s1 is s3)     # False (dynamically created)
print(s1 == s3)     # True (same value)

import sys
sys.intern("my_repeated_key")  # manually intern a string (for performance in dicts)
```

### 2.4 Python's Built-in Types

```python
# ── Numeric Types ─────────────────────────────────────────────
int_val    = 42              # arbitrary precision (no overflow!)
big_int    = 10 ** 1000      # works! (very large but finite)
float_val  = 3.14            # 64-bit IEEE 754 double
complex_val = 3 + 4j         # complex number: real=3, imag=4
bool_val   = True            # bool is a subclass of int: True==1, False==0

# int operations
abs(-5)                      # 5
divmod(17, 5)               # (3, 2) — quotient and remainder
pow(2, 10)                   # 1024
pow(2, 10, 1000)             # 24 — modular exponentiation (fast!)
bin(255)                     # '0b11111111'
oct(255)                     # '0o377'
hex(255)                     # '0xff'
int('ff', 16)                # 255 — parse hex string
int('0b1010', 2)             # 10 — parse binary string

# float operations
import math
math.floor(3.7)              # 3
math.ceil(3.2)               # 4
math.trunc(3.9)              # 3 (toward zero)
round(3.14159, 2)            # 3.14
math.isfinite(float('inf'))  # False
math.isnan(float('nan'))     # True
math.sqrt(16)                # 4.0
math.log(math.e)             # 1.0 (natural log)
math.log2(1024)              # 10.0
math.log10(1000)             # 3.0

# Decimal for exact decimal arithmetic
from decimal import Decimal, getcontext
getcontext().prec = 50           # set precision to 50 significant digits
d = Decimal('0.1') + Decimal('0.2')  # exactly 0.3
print(d)                         # 0.3 ✓

# Fraction for exact rational arithmetic
from fractions import Fraction
f = Fraction(1, 3) + Fraction(1, 6)
print(f)                         # 1/2

# ── None ──────────────────────────────────────────────────────
x = None                # singleton — there's only one None object
print(type(None))       # <class 'NoneType'>
print(x is None)        # True

# ── Boolean ───────────────────────────────────────────────────
print(True  + 1)        # 2 (bool subclasses int; True == 1)
print(False + 1)        # 1 (False == 0)
print(isinstance(True, int))  # True

# Truthy and falsy values — Python's truth testing
# Falsy: None, False, 0, 0.0, 0j, "", b"", [], (), {}, set(), range(0), any empty container
# Truthy: everything else

falsy = [None, False, 0, 0.0, 0j, "", b"", [], (), {}, set()]
for val in falsy:
    print(f"{val!r:15} → {bool(val)}")

# if obj: is equivalent to if bool(obj): which calls obj.__bool__() or obj.__len__()
```

### 2.5 Variable Scope — LEGB Rule

```python
# Python uses LEGB scope resolution:
# L: Local — inside the current function
# E: Enclosing — in any enclosing functions (closures)
# G: Global — at module level
# B: Built-in — Python built-ins (len, print, etc.)

x = "global"    # G

def outer():
    x = "enclosing"   # E (for inner)
    
    def inner():
        x = "local"   # L
        print(x)      # "local" — local shadows enclosing and global
    
    inner()
    print(x)          # "enclosing"

outer()
print(x)              # "global"

# Modifying outer scope variables
count = 0
def increment():
    global count       # declare we're using the global 'count'
    count += 1

increment()
print(count)          # 1

def make_counter():
    count = 0
    def inc():
        nonlocal count  # declare we're modifying the enclosing 'count'
        count += 1
        return count
    return inc

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3

# Without nonlocal/global: assignment creates a new LOCAL variable
def broken():
    count = 0
    def inc():
        count += 1   # ❌ UnboundLocalError: reading count before "assigning" it
                     # Python sees the assignment count += 1 → count is local
                     # but it hasn't been assigned yet in this local scope
    inc()
```

---

## Chapter 3: Operators, Expressions & Built-in Functions

### 3.1 All Operators

```python
# ── Arithmetic ────────────────────────────────────────────────
17 + 5   # 22
17 - 5   # 12
17 * 5   # 85
17 / 5   # 3.4   — true division (ALWAYS float in Python 3)
17 // 5  # 3     — floor division (rounds toward -∞, not toward 0)
17 % 5   # 2     — modulo (sign follows DIVISOR in Python, unlike C)
2 ** 10  # 1024  — exponentiation (right-associative: 2**3**2 = 2**9 = 512)

# Floor division with negatives (rounds toward -∞):
-7 // 2   # -4 (not -3! Python floors toward -∞)
7 // -2   # -4

# Modulo with negatives (result has same sign as divisor):
-7 % 3    # 2  (because -7 = (-3)*3 + 2)
7 % -3    # -2 (because 7 = (-3)*(-3) + (-2))

# ── String Operators ──────────────────────────────────────────
"hello" + " " + "world"   # "hello world"   (concatenation)
"ha" * 3                   # "hahaha"         (repetition)
"lo" in "hello"            # True             (membership)

# ── Comparison ────────────────────────────────────────────────
3 == 3.0    # True  (== checks value; int 3 == float 3.0)
3 is 3.0    # False (is checks identity; different objects)
# Chained comparisons (Python-specific, very Pythonic):
1 < 2 < 3   # True  (equivalent to: 1 < 2 and 2 < 3)
1 < 5 < 3   # False (5 < 3 is False)
a = b = 5
1 < a == b < 10  # True (1<5 and 5==5 and 5<10)

# ── Boolean Operators ─────────────────────────────────────────
# and, or return one of their OPERANDS (not True/False necessarily)
# Short-circuit: and returns first falsy or last value
#                or  returns first truthy or last value
"" or "default"      # "default" (empty string is falsy)
"value" or "default" # "value"   (first truthy)
None or [] or {}     # {}        (last value, all falsy)
5 and 6              # 6         (last value, all truthy)
0 and 6              # 0         (first falsy)

# Practical uses:
name = user_name or "Anonymous"          # default if falsy
value = config.get("key") or "fallback"  # common pattern

# ── Bitwise Operators ─────────────────────────────────────────
0b1010 & 0b1100   # 0b1000 = 8  (AND)
0b1010 | 0b1100   # 0b1110 = 14 (OR)
0b1010 ^ 0b1100   # 0b0110 = 6  (XOR)
~0b1010           # -11         (NOT: ~x = -(x+1) for integers)
0b1010 << 2       # 0b101000 = 40 (left shift)
0b1010 >> 1       # 0b0101 = 5   (arithmetic right shift)

# ── Walrus Operator := (Python 3.8+) — assignment expression ──
# Assigns AND evaluates in an expression
import re
if match := re.search(r'\d+', "abc123def"):
    print(match.group())  # "123" — match is assigned AND checked

# Avoid repeated computation
while chunk := file.read(8192):   # assign and check truthy in one
    process(chunk)

# In comprehensions (filter and transform)
results = [y for x in data if (y := expensive(x)) > 0]
```

### 3.2 Essential Built-in Functions

```python
# ── Type conversion ───────────────────────────────────────────
int("42")           # 42
int("0xff", 16)     # 255
int(3.9)            # 3 (truncates toward zero)
float("3.14")       # 3.14
str(42)             # "42"
bool(0)             # False
list("abc")         # ['a', 'b', 'c']
tuple([1,2,3])      # (1, 2, 3)
set([1,2,2,3])      # {1, 2, 3}
dict(a=1, b=2)      # {'a': 1, 'b': 2}
bytes("hello", "utf-8")  # b'hello'
bytearray(b"hello")      # bytearray(b'hello') — mutable bytes

# ── Inspection ───────────────────────────────────────────────
type(42)             # <class 'int'>
isinstance(42, int)  # True
isinstance(True, int)# True (bool is subclass of int)
isinstance(42, (int, float))  # True — check against tuple of types
issubclass(bool, int)# True
id(42)               # memory address
hash("hello")        # integer hash (stable within a process)
dir([])              # list all attributes of an object
vars(obj)            # obj.__dict__ — instance attributes as dict
getattr(obj, "name") # obj.name — access attribute by string name
setattr(obj, "name", val)  # obj.name = val
hasattr(obj, "name") # True if attribute exists
delattr(obj, "name") # del obj.name
callable(print)      # True — has __call__
repr("hello")        # "'hello'" — unambiguous string representation

# ── Iteration ─────────────────────────────────────────────────
len([1,2,3])         # 3
range(5)             # range(0, 5) — lazy sequence 0,1,2,3,4
range(1, 10, 2)      # 1,3,5,7,9
enumerate(["a","b","c"])          # (0,'a'), (1,'b'), (2,'c')
enumerate(["a","b"], start=1)     # (1,'a'), (2,'b')
zip([1,2,3], ["a","b","c"])      # (1,'a'), (2,'b'), (3,'c')
zip([1,2], ["a","b","c"])        # stops at shortest: (1,'a'), (2,'b')

from itertools import zip_longest
zip_longest([1,2], ["a","b","c"], fillvalue=None)  # (1,'a'),(2,'b'),(None,'c')

map(str, [1,2,3])    # lazy: '1','2','3'
filter(None, [0,1,None,2,""])    # lazy: 1,2 (filters falsy)
filter(lambda x: x>0, [-1,0,1,2])  # lazy: 1,2
reversed([1,2,3])    # lazy iterator in reverse
sorted([3,1,2])      # [1,2,3] — new sorted list
sorted([3,1,2], reverse=True)    # [3,2,1]
sorted(["banana","apple","cherry"], key=len)  # by length: ['apple','banana','cherry']

# ── Aggregation ───────────────────────────────────────────────
sum([1,2,3,4,5])     # 15
sum([[1,2],[3,4]], [])  # [1,2,3,4] — flatten (sum with initial=[])
min(3, 1, 4, 1, 5)   # 1
max([3,1,4,1,5])      # 5
min(["banana","apple"], key=len)  # "apple"
all([True, True, False])  # False — all truthy?
any([False, False, True]) # True  — any truthy?
abs(-5)               # 5

# ── Object creation ───────────────────────────────────────────
object()             # bare object instance
super()              # proxy to parent class (in methods)
property(fget, fset) # create property descriptor
staticmethod(fn)     # mark as static method
classmethod(fn)      # mark as class method

# ── I/O ──────────────────────────────────────────────────────
print("hello", "world", sep=", ", end="!\n")  # "hello, world!\n"
print(*[1,2,3], sep="-")                       # "1-2-3"
x = input("Enter: ")         # reads one line from stdin (always str)
open("file.txt", "r")        # open file (returns file object)

# ── Introspection ────────────────────────────────────────────
help(len)            # print docstring
print(len.__doc__)   # "Return the number of items in a container."
import inspect
inspect.signature(sorted)     # (iterable, /, *, key=None, reverse=False)
inspect.getsource(sorted)     # source code (if available)
```

---

## Chapter 4: Control Flow

### 4.1 if / elif / else

```python
# Basic
score = 75
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# One-liner (ternary / conditional expression)
grade = "pass" if score >= 60 else "fail"

# Nested ternary (avoid — hard to read)
grade = "A" if score >= 90 else ("B" if score >= 80 else "C")

# Pattern matching — match/case (Python 3.10+)
command = ("go", "north")
match command:
    case ("quit",):
        print("Quitting")
    case ("go", direction):
        print(f"Going {direction}")    # direction bound to "north"
    case ("get", item, *rest):         # rest captures remaining args
        print(f"Getting {item}")
    case {"action": action, "target": target}:  # match dict
        print(f"{action} on {target}")
    case Point(x=0, y=0):             # match class with attributes
        print("Origin")
    case [int(), int()] as pair:       # type check + binding
        print(f"Pair of ints: {pair}")
    case _:                            # wildcard (like default)
        print("Unknown command")

# Guards in match
match point:
    case (x, y) if x == y:
        print("On diagonal")
    case (x, y):
        print(f"Point: {x}, {y}")
```

### 4.2 Loops

```python
# for loop — iterates any iterable
for i in range(10):
    print(i)

for char in "hello":
    print(char)

for key, val in {"a": 1, "b": 2}.items():
    print(f"{key}: {val}")

# enumerate — index + value
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip — iterate multiple iterables together
names = ["Alice", "Bob"]
scores = [90, 85]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# for/else — else runs only if loop completed without break
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed without break")   # prints: loop didn't find 10

# while loop
n = 1
while n < 100:
    n *= 2
print(n)  # 128

# while/else
n = 10
while n > 0:
    n -= 1
else:
    print("n reached 0")  # runs: loop completed normally

# break, continue
for i in range(10):
    if i % 2 == 0:
        continue   # skip even numbers
    if i > 7:
        break      # stop at 7
    print(i)       # 1, 3, 5, 7

# pass — null statement (placeholder)
class AbstractBase:
    def method(self):
        pass  # to be implemented by subclasses

# Iterating with mutation — don't modify a list while iterating it!
items = [1, 2, 3, 4, 5]
# ❌ Wrong: skips elements
for i, item in enumerate(items):
    if item % 2 == 0:
        items.remove(item)  # shifts indices; next element skipped

# ✅ Correct: iterate a copy, or build new list
items = [x for x in items if x % 2 != 0]
# or: items[:] = [x for x in items if x % 2 != 0]  (in-place replacement)
```

---

## Chapter 5: Functions — First-Class Everything

### 5.1 Function Definition and Arguments

```python
# Basic function
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting string.
    
    Args:
        name: The person's name.
        greeting: The greeting word (default: "Hello").
    
    Returns:
        A formatted greeting string.
    """
    return f"{greeting}, {name}!"

# Calling with positional and keyword args
greet("Alice")                    # "Hello, Alice!"
greet("Bob", "Hi")               # "Hi, Bob!"
greet(name="Carol", greeting="Hey")  # keyword arguments (order doesn't matter)
greet("Dave", greeting="Howdy")  # mix positional and keyword

# ── All parameter types ────────────────────────────────────────
def comprehensive(
    pos_only_a,          # positional-only (before /)
    pos_only_b,
    /,                   # ← everything before / is positional-only
    normal_a,            # positional-or-keyword
    normal_b = "default",
    *args,               # ← positional-only after this (varargs)
    keyword_only_a,      # keyword-only (after *)
    keyword_only_b = "kw_default",
    **kwargs             # additional keyword arguments
):
    print(pos_only_a, normal_a, args, keyword_only_a, kwargs)

comprehensive(1, 2, 3, keyword_only_a="required")
# pos_only_a=1, pos_only_b=2, normal_a=3, normal_b="default",
# args=(), keyword_only_a="required", keyword_only_b="kw_default", kwargs={}

# *args — collects extra positional args as tuple
def sumAll(*args):
    return sum(args)
sumAll(1, 2, 3, 4, 5)  # 15

# **kwargs — collects extra keyword args as dict
def printConfig(**kwargs):
    for key, val in kwargs.items():
        print(f"{key} = {val}")
printConfig(host="localhost", port=8080, debug=True)

# Unpacking when calling
nums = [1, 2, 3]
print(*nums)                  # print(1, 2, 3) — spreads list as positional args
settings = {"sep": ", ", "end": "!\n"}
print(1, 2, 3, **settings)   # print(1, 2, 3, sep=", ", end="!\n")

# Function annotations (type hints)
def add(a: int, b: int) -> int:
    return a + b

# Annotations are stored in __annotations__ dict
print(add.__annotations__)    # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
# NOTE: annotations are NOT enforced at runtime — only for type checkers (mypy, pyright)
```

### 5.2 Functions as Objects

```python
# Functions are first-class objects — can be stored, passed, returned

# Store in a variable
def square(x): return x * x
sq = square           # sq is another name for the same function object
print(sq(5))          # 25
print(sq is square)   # True — same object

# Store in data structures
ops = {"double": lambda x: x*2, "square": lambda x: x**2, "negate": lambda x: -x}
for name, op in ops.items():
    print(f"{name}(5) = {op(5)}")

# Pass as argument (higher-order functions)
def apply(func, value):
    return func(value)
apply(square, 4)   # 16
apply(str.upper, "hello")  # "HELLO"

# Return from a function
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply  # return the inner function

double = multiplier(2)
triple = multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
print(type(double))  # <class 'function'>

# Lambda — anonymous function (single expression only)
square_lambda = lambda x: x * x
add = lambda a, b: a + b
# Lambdas are useful when passing a small function as an argument:
sorted(people, key=lambda p: p.age)  # sort by age
sorted(words, key=lambda w: (len(w), w))  # sort by length, then alphabetically

# Built-in higher-order functions
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
list(map(square, nums))                          # [1,4,9,16,25,36,49,64,81,100]
list(filter(lambda x: x % 2 == 0, nums))        # [2,4,6,8,10]
from functools import reduce
reduce(lambda acc, x: acc + x, nums)             # 55 (sum)
reduce(lambda acc, x: acc * x, nums, 1)          # 3628800 (factorial 10)
```

### 5.3 functools — Function Utilities

```python
from functools import (
    partial, wraps, lru_cache, cache, cached_property,
    reduce, total_ordering, singledispatch
)

# partial — fix some arguments of a function
def power(base, exp): return base ** exp
square = partial(power, exp=2)  # fix exp=2
cube   = partial(power, exp=3)
square(5)   # 25
cube(3)     # 27

add10 = partial(int.__add__, 10)  # add10(x) = 10 + x

# lru_cache — memoize function results (Least Recently Used cache)
@lru_cache(maxsize=128)   # cache up to 128 results
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

fib(100)  # instant! (without cache: 2^100 calls)
print(fib.cache_info())  # CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)
fib.cache_clear()        # clear the cache

@cache  # Python 3.9+: like lru_cache(maxsize=None) — unbounded
def expensive(n): return n * n

# cached_property — compute once, store on instance
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        import math
        print("Computing area...")
        return math.pi * self.radius ** 2

c = Circle(5)
c.area  # "Computing area..." then 78.54...
c.area  # No message — returns cached value

# total_ordering — define all comparison methods from just __eq__ and one of <,<=,>,>=
@total_ordering
class Student:
    def __init__(self, name, gpa):
        self.name, self.gpa = name, gpa
    def __eq__(self, other): return self.gpa == other.gpa
    def __lt__(self, other): return self.gpa < other.gpa
    # Python generates __le__, __gt__, __ge__ automatically

# singledispatch — overload function by type of first argument
@singledispatch
def process(arg):
    raise NotImplementedError(f"Cannot process {type(arg)}")

@process.register(int)
def _(n): return n * 2

@process.register(str)
def _(s): return s.upper()

@process.register(list)
def _(lst): return [process(x) for x in lst]

process(5)          # 10
process("hello")    # "HELLO"
process([1,"a",2])  # [2, "A", 4]
```

---

## Chapter 6: Closures & Decorators

### 6.1 Closures — Functions That Remember

```python
# A closure is a function that captures variables from its enclosing scope
# even after that scope has finished executing.

def make_adder(n):
    # 'n' is a free variable — it lives in the enclosing scope
    def adder(x):
        return x + n   # 'n' is captured from make_adder's scope
    return adder

add5  = make_adder(5)
add10 = make_adder(10)
print(add5(3))   # 8  — add5 "remembers" n=5
print(add10(3))  # 13 — add10 "remembers" n=10

# Inspect the closure
print(add5.__closure__)       # (<cell at 0x...>)
print(add5.__closure__[0].cell_contents)  # 5

# Mutable state in closures
def make_counter(start=0):
    count = [start]  # list trick: mutate the list instead of rebinding
    def counter():
        count[0] += 1
        return count[0]
    return counter

# Cleaner with nonlocal (Python 3)
def make_counter_clean(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter_clean()
print(c(), c(), c())  # 1 2 3

# Classic closure bug — loop variable capture
# ❌ BUG: all lambdas capture the SAME variable 'i', which ends up as 9
funcs_bad = [lambda: i for i in range(10)]
print(funcs_bad[0]())  # 9 (not 0!)
print(funcs_bad[5]())  # 9 (not 5!)

# ✅ FIX: use default argument to capture current value
funcs_good = [lambda i=i: i for i in range(10)]
print(funcs_good[0]())  # 0
print(funcs_good[5]())  # 5
```

### 6.2 Decorators — Functions That Wrap Functions

```python
# A decorator is a function that takes a function and returns a modified function
# @decorator syntax is just syntactic sugar for: func = decorator(func)

# Basic decorator structure
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)  # call original function
        print("After call")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
# Before call
# Hello, Alice!
# After call

# Equivalent to: say_hello = my_decorator(say_hello)

# ── Using functools.wraps — ALWAYS do this ─────────────────────
# Without wraps: decorated function loses its name, docstring, and signature
from functools import wraps

def timer(func):
    @wraps(func)   # preserves __name__, __doc__, __annotations__, __wrapped__
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """This function is slow."""
    import time; time.sleep(0.1)

slow_function()               # "slow_function took 0.1001s"
print(slow_function.__name__)  # "slow_function" (preserved by @wraps)
print(slow_function.__doc__)   # "This function is slow." (preserved)

# ── Decorator with arguments ───────────────────────────────────
# Need an extra layer of wrapping

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retry a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    # might raise ConnectionError or TimeoutError
    return requests.get(url).json()

# ── Class-based decorator ──────────────────────────────────────
class cache_result:
    """Cache the return value of a function indefinitely."""
    def __init__(self, func):
        self.func = func
        self.cache = {}
        wraps(func)(self)  # copy over metadata

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@cache_result
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# ── Stacking decorators ────────────────────────────────────────
# Applied bottom-up: @d1 @d2 @d3 → d1(d2(d3(func)))
@timer
@retry(max_attempts=2)
def risky_and_timed():
    pass

# ── Practical decorator examples ──────────────────────────────

# Rate limiter
from functools import wraps
from collections import deque
import time

def rate_limit(calls_per_second):
    def decorator(func):
        timestamps = deque()
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove timestamps older than 1 second
            while timestamps and now - timestamps[0] > 1.0:
                timestamps.popleft()
            if len(timestamps) >= calls_per_second:
                sleep_time = 1.0 - (now - timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            timestamps.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Validate arguments
def validate(**type_checks):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, expected_type in type_checks.items():
                if name in bound.arguments:
                    val = bound.arguments[name]
                    if not isinstance(val, expected_type):
                        raise TypeError(
                            f"{name} must be {expected_type.__name__}, got {type(val).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(name=str, age=int)
def create_user(name, age):
    return {"name": name, "age": age}

create_user("Alice", 30)   # ✅
# create_user("Alice", "30") → TypeError: age must be int, got str
```

---

## Chapter 7: Generators & Iterators — The Protocol

### 7.1 The Iterator Protocol

```python
# An iterable is any object you can loop over.
# An iterator is an object that tracks position and returns items one at a time.

# The iterator protocol:
# __iter__(self) → returns the iterator (usually self)
# __next__(self) → returns next item, raises StopIteration when done

# How for loops work INTERNALLY:
lst = [1, 2, 3]
# for x in lst: ... is equivalent to:
it = iter(lst)          # calls lst.__iter__()
while True:
    try:
        x = next(it)   # calls it.__next__()
        print(x)
    except StopIteration:
        break

# Custom iterator
class CountUp:
    """Iterator that counts from start to stop."""
    def __init__(self, start, stop):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self  # iterator returns itself

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

for n in CountUp(1, 6):
    print(n)   # 1 2 3 4 5

# Infinite iterator
class InfiniteCounter:
    def __init__(self): self.n = 0
    def __iter__(self): return self
    def __next__(self):
        self.n += 1
        return self.n

# Must use break or islice with infinite iterators
from itertools import islice
first_5 = list(islice(InfiniteCounter(), 5))  # [1, 2, 3, 4, 5]
```

### 7.2 Generators — Lazy Iterators

```python
# Generator function: uses 'yield' instead of 'return'
# Each call to __next__() runs until the next 'yield', then suspends

def count_up(start, stop):
    current = start
    while current < stop:
        yield current    # suspend here, return current
        current += 1     # resume here next time __next__() is called
    # implicit return → raises StopIteration

gen = count_up(1, 6)
print(type(gen))         # <class 'generator'>
print(next(gen))         # 1
print(next(gen))         # 2
for n in gen:            # continues from where we left off
    print(n)             # 3, 4, 5

# Generators are lazy — they produce values one at a time
# Perfect for: large datasets, infinite sequences, pipelines

# Infinite generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice, takewhile
list(islice(fibonacci(), 10))   # [0,1,1,2,3,5,8,13,21,34]
list(takewhile(lambda x: x < 100, fibonacci()))  # [0,1,1,2,3,5,8,13,21,34,55,89]

# yield from — delegate to another generator
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # recursively flatten
        else:
            yield item

list(flatten([1, [2, [3, 4]], [5, 6]]))  # [1, 2, 3, 4, 5, 6]

# Generator expressions — like list comprehensions but lazy
squares_list = [x**2 for x in range(1000000)]  # allocates 1M items immediately
squares_gen  = (x**2 for x in range(1000000))  # no memory allocation yet

sum(x**2 for x in range(1000000))    # sum without creating a list (efficient)
any(x > 100 for x in range(1000000)) # short-circuits at first True

# Generator pipeline
def read_lines(filename):
    with open(filename) as f:
        yield from f

def parse_integers(lines):
    for line in lines:
        try:
            yield int(line.strip())
        except ValueError:
            pass  # skip non-integer lines

def filter_positives(nums):
    return (n for n in nums if n > 0)

# Process a huge file without loading it into memory:
pipeline = filter_positives(parse_integers(read_lines("data.txt")))
total = sum(pipeline)
```

### 7.3 Generator send(), throw(), and close()

```python
# Generators can receive values via send() — makes them coroutines

def accumulator():
    total = 0
    while True:
        value = yield total  # yield sends total OUT, receives value IN
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)           # advance to first yield (required before send())
gen.send(10)        # send 10, total becomes 10, returns 10
gen.send(20)        # send 20, total becomes 30, returns 30
gen.send(5)         # send 5, total becomes 35, returns 35
gen.close()         # send GeneratorExit exception (cleanup)

# throw() — inject an exception into the generator
def safe_gen():
    try:
        while True:
            value = yield
    except ValueError as e:
        yield f"Handled: {e}"
    finally:
        print("Generator cleanup")  # runs on close() or when generator ends

g = safe_gen()
next(g)
g.throw(ValueError, "bad value")   # injects ValueError; generator handles it
# → "Handled: bad value"
```

---

## Chapter 8: Strings — Deep Dive

### 8.1 String Fundamentals

```python
# Python strings are IMMUTABLE sequences of Unicode code points
# str is the type; internally stored as UTF-8, Latin-1, or UCS-2/UCS-4
# depending on what characters it contains (PEP 393 flexible string representation)

s = "Hello, 世界! 🌍"
len(s)              # 12 (characters, not bytes)
s[0]                # 'H'
s[-1]               # '🌍'
s[7:9]              # '世界' (slicing by character index)

# Encoding: str → bytes
encoded = s.encode("utf-8")    # b'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x8c\x8d'
encoded = s.encode("utf-16")   # UTF-16 with BOM
encoded = s.encode("ascii", errors="replace")  # b'Hello, ??! ?'

# Decoding: bytes → str
decoded = encoded.decode("utf-8")

# errors parameter:
"café".encode("ascii", errors="ignore")    # b'caf' (removes non-ASCII)
"café".encode("ascii", errors="replace")   # b'caf?' (replaces with ?)
"café".encode("ascii", errors="xmlcharrefreplace")  # b'caf&#233;' (XML entity)
"café".encode("ascii", errors="backslashreplace")   # b'caf\\xe9'

# ── String literals ───────────────────────────────────────────
single  = 'single quotes'
double  = "double quotes"
triple  = """triple quoted
             spans multiple lines"""
raw     = r"raw\nstring"    # r prefix: backslashes are literal, \n is two chars
bytes_  = b"bytes literal"  # b prefix: bytes object, not str
f_str   = f"Hello, {2+2}"  # f prefix: f-string (formatted string literal)
```

### 8.2 F-Strings — Full Power

```python
name = "Alice"
age  = 30
pi   = 3.14159265

# Basic expression
f"Hello, {name}!"                      # "Hello, Alice!"
f"In 5 years: {age + 5}"             # "In 5 years: 35"
f"{'upper'.upper()}"                   # "UPPER" — call methods
f"{len(name)}"                         # 5 — call functions

# Format specification: {value:format_spec}
# width, fill, alignment, sign, type
f"{pi:.4f}"           # "3.1416"     — 4 decimal places
f"{pi:10.2f}"         # "      3.14" — width 10, 2 decimal places, right-aligned
f"{pi:>10.2f}"        # "      3.14" — explicit right-align
f"{pi:<10.2f}"        # "3.14      " — left-align
f"{pi:^10.2f}"        # "   3.14   " — center-align
f"{pi:*^10.2f}"       # "***3.14***" — fill with *
f"{1234567:,}"        # "1,234,567"  — thousands separator
f"{1234567:_}"        # "1_234_567"  — underscore separator
f"{0.95:.1%}"         # "95.0%"      — percentage
f"{255:#010x}"        # "0x000000ff" — hex with prefix, padded to 10 chars
f"{255:#08b}"         # "0b001111111" — binary with prefix
f"{255:e}"            # "2.550000e+02" — scientific notation

# Debugging: = suffix (Python 3.8+) — shows expression and value
x = 42
f"{x=}"               # "x=42"
f"{x + 1=}"           # "x + 1=43"
f"{name=!r}"          # "name='Alice'" — !r applies repr()

# Nested f-strings
width = 10
f"{'center':^{width}}"   # "  center  " — dynamic width

# Multi-line f-strings
msg = (
    f"Name: {name}\n"
    f"Age:  {age}\n"
    f"Pi:   {pi:.2f}"
)

# Python 3.12+: f-strings can contain arbitrary expressions including quotes
f"{'it\\'s fine'}"   # works in Python 3.12+

# format() method (older style, still common)
"{name} is {age} years old".format(name="Alice", age=30)
"{0} + {1} = {2}".format(1, 2, 3)
"{:.2f}".format(3.14159)   # "3.14"

# % formatting (old style, avoid in new code)
"%s is %d years old" % ("Alice", 30)
"%.2f" % 3.14159
```

### 8.3 String Methods — Complete Reference

```python
s = "  Hello, World!  "

# ── Case ─────────────────────────────────────────────────────
s.upper()               # "  HELLO, WORLD!  "
s.lower()               # "  hello, world!  "
s.title()               # "  Hello, World!  " (capitalize each word)
s.capitalize()          # "  hello, world!  " → "  hello, world!  " (only first letter)
s.swapcase()            # "  hELLO, wORLD!  "
s.casefold()            # "  hello, world!  " — aggressive lowercase for comparison

# ── Strip whitespace ──────────────────────────────────────────
s.strip()               # "Hello, World!"  — both ends
s.lstrip()              # "Hello, World!  "
s.rstrip()              # "  Hello, World!"
"___hello___".strip("_")  # "hello" — strip specific chars

# ── Search ────────────────────────────────────────────────────
s = "Hello, World!"
s.find("World")          # 7  — returns -1 if not found
s.rfind("l")             # 10 — last occurrence
s.index("World")         # 7  — like find but raises ValueError if not found
s.count("l")             # 3
"World" in s             # True  (preferred over find for boolean check)
s.startswith("Hello")    # True
s.endswith("!")           # True
s.startswith(("Hello", "Hi"))  # True — check against tuple of prefixes

# ── Replace ───────────────────────────────────────────────────
s.replace("World", "Python")        # "Hello, Python!"
s.replace("l", "L", 2)             # "HeLLo, World!" — replace only first 2

# ── Split and Join ────────────────────────────────────────────
"a,b,c,d".split(",")               # ['a', 'b', 'c', 'd']
"a,b,c".split(",", maxsplit=1)     # ['a', 'b,c'] — only first split
"hello world".split()              # ['hello', 'world'] — split on whitespace
"line1\nline2\nline3".splitlines() # ['line1', 'line2', 'line3']

",".join(["a", "b", "c"])          # "a,b,c"
" ".join(["Hello", "World"])       # "Hello World"
"\n".join(lines)                   # join with newline

# ── Validation ────────────────────────────────────────────────
"123".isdigit()         # True
"abc".isalpha()         # True
"abc123".isalnum()      # True
"  \t\n".isspace()      # True
"Hello World".istitle() # True
"HELLO".isupper()       # True
"hello".islower()       # True
"hello".isidentifier()  # True
"3hello".isidentifier() # False (starts with digit)
"hello".isascii()       # True
"héllo".isascii()       # False

# ── Padding ───────────────────────────────────────────────────
"42".zfill(6)           # "000042" — zero-pad
"hi".ljust(10)          # "hi        "
"hi".rjust(10)          # "        hi"
"hi".center(10)         # "    hi    "
"hi".center(10, "-")    # "----hi----"

# ── Encoding ─────────────────────────────────────────────────
"hello".encode("utf-8")    # b'hello'
b"hello".decode("utf-8")   # "hello"

# ── Translation ───────────────────────────────────────────────
table = str.maketrans("aeiou", "AEIOU")           # vowel table
"hello world".translate(table)                     # "hEllO wOrld"
table2 = str.maketrans("", "", "!?.,")            # deletion table
"Hello, World!".translate(table2)                  # "Hello World"
```

### 8.4 Regular Expressions

```python
import re

text = "Contact: alice@example.com or bob.smith@company.org for info"

# ── Basic operations ──────────────────────────────────────────
# re.search — find first match anywhere in string
match = re.search(r'\b\w+@\w+\.\w+\b', text)
if match:
    print(match.group())    # "alice@example.com"
    print(match.start())    # 9
    print(match.end())      # 26
    print(match.span())     # (9, 26)

# re.match — match only at START of string
re.match(r'\d+', "123abc")   # match object
re.match(r'\d+', "abc123")   # None — doesn't start with digit

# re.fullmatch — entire string must match
re.fullmatch(r'\d+', "123")    # match
re.fullmatch(r'\d+', "123abc") # None

# re.findall — find all matches, return list of strings
emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
# ["alice@example.com", "bob.smith@company.org"]

# re.finditer — find all matches, return iterator of match objects
for m in re.finditer(r'\b\w+@\w+\.\w+\b', text):
    print(f"Found {m.group()} at {m.span()}")

# re.sub — replace matches
cleaned = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', "[REDACTED]", text)
# "Contact: [REDACTED] or [REDACTED] for info"

# re.split — split on pattern
re.split(r'[,\s]+', "one, two,three  four")  # ['one', 'two', 'three', 'four']

# ── Compiled patterns (for reuse — faster) ────────────────────
email_re = re.compile(r'\b[\w.-]+@[\w.-]+\.\w+\b', re.IGNORECASE)
email_re.findall(text)
email_re.sub("[EMAIL]", text)

# ── Groups ────────────────────────────────────────────────────
# Capturing groups with ()
m = re.search(r'(\d{4})-(\d{2})-(\d{2})', "Today is 2024-03-15")
m.group(0)   # "2024-03-15" (entire match)
m.group(1)   # "2024" (first group)
m.group(2)   # "03"
m.group(3)   # "15"
m.groups()   # ("2024", "03", "15")

# Named groups with (?P<name>...)
m = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', "2024-03-15")
m.group("year")     # "2024"
m.group("month")    # "03"
m.groupdict()       # {"year":"2024","month":"03","day":"15"}

# Non-capturing group (?:...)
re.findall(r'(?:Mr|Mrs|Ms)\. \w+', "Mr. Smith and Mrs. Jones")
# ["Mr. Smith", "Mrs. Jones"]

# ── Common patterns ───────────────────────────────────────────
# Email:         r'[\w.-]+@[\w.-]+\.\w{2,}'
# URL:           r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
# Phone (US):    r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
# IP address:    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
# Integer:       r'-?\d+'
# Float:         r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'
# Hex color:     r'#[0-9a-fA-F]{6}\b'
# Date ISO:      r'\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])'

# ── Flags ─────────────────────────────────────────────────────
re.IGNORECASE  # or re.I — case-insensitive
re.MULTILINE   # or re.M — ^ and $ match line boundaries
re.DOTALL      # or re.S — . matches newlines too
re.VERBOSE     # or re.X — allow whitespace and comments in pattern

phone_re = re.compile(r"""
    (?:                  # non-capturing group for area code
        \(\d{3}\)       # (XXX)
        |               # or
        \d{3}           # XXX
    )
    [-.\s]?             # optional separator
    \d{3}               # exchange
    [-.\s]?             # optional separator
    \d{4}               # number
""", re.VERBOSE)
```

---

## Chapter 9: Lists, Tuples & Arrays

### 9.1 Lists — Dynamic Arrays

```python
# List: ordered, mutable, allows duplicates, can mix types
lst = [1, "hello", 3.14, True, None, [1, 2]]

# ── Construction ─────────────────────────────────────────────
[]                          # empty list
list()                      # empty list
list("abc")                 # ['a', 'b', 'c'] — from iterable
list(range(5))              # [0, 1, 2, 3, 4]
[0] * 5                     # [0, 0, 0, 0, 0] — repeat
[None] * 3                  # [None, None, None]

# ── Access ────────────────────────────────────────────────────
lst = [10, 20, 30, 40, 50]
lst[0]                      # 10 — first
lst[-1]                     # 50 — last
lst[-2]                     # 40 — second from last
lst[1:4]                    # [20, 30, 40] — slice [start:stop) (stop exclusive)
lst[::2]                    # [10, 30, 50] — every 2nd
lst[::-1]                   # [50, 40, 30, 20, 10] — reversed
lst[1:4:2]                  # [20, 40] — [start:stop:step]

# ── Modification ──────────────────────────────────────────────
lst.append(60)              # [10,20,30,40,50,60] — add to end
lst.extend([70, 80])        # add multiple: [10,20,30,40,50,60,70,80]
lst += [90, 100]            # same as extend (in-place)
lst.insert(0, 0)            # insert at index 0: [0,10,20,...]
lst[1:3] = [15, 25]        # slice assignment: replaces elements

lst.pop()                   # remove and return last element
lst.pop(0)                  # remove and return element at index 0
lst.remove(30)              # remove FIRST occurrence of 30 (ValueError if absent)
del lst[0]                  # delete by index
del lst[1:4]                # delete slice
lst.clear()                 # remove all elements

lst[0] = 99                 # replace element
lst[1:3] = [200, 300]      # replace slice

# ── Searching ────────────────────────────────────────────────
lst = [3, 1, 4, 1, 5, 9, 2, 6, 5]
3 in lst                    # True
lst.index(5)                # 4 — first occurrence index
lst.count(1)                # 2 — how many times 1 appears
lst.index(5, 5)             # 8 — search from index 5

# ── Sorting ───────────────────────────────────────────────────
lst.sort()                              # sort in place (returns None!)
lst.sort(reverse=True)                  # descending
lst.sort(key=abs)                       # by absolute value
sorted(lst)                             # returns new sorted list (doesn't modify)
sorted(lst, key=lambda x: -x)          # new sorted list, descending
sorted(people, key=lambda p: (p.age, p.name))  # multi-key sort

# ── Utility ───────────────────────────────────────────────────
lst.copy()                  # shallow copy
lst.reverse()               # in-place reverse (returns None)
list(reversed(lst))         # new reversed list
len(lst)                    # length
min(lst); max(lst); sum(lst)

# ── List as stack (LIFO) ─────────────────────────────────────
stack = []
stack.append(1); stack.append(2); stack.append(3)
stack.pop()     # 3 (LIFO: last in, first out) — O(1)

# ── List as queue (inefficient — use collections.deque) ───────
from collections import deque
queue = deque([1, 2, 3])
queue.appendleft(0)    # add to front — O(1)
queue.append(4)        # add to back  — O(1)
queue.popleft()        # remove from front — O(1)
queue.pop()            # remove from back  — O(1)
```

### 9.2 Tuples — Immutable Sequences

```python
# Tuples: ordered, IMMUTABLE, allows duplicates, often used for heterogeneous data
t = (1, "hello", 3.14)
empty = ()
single = (42,)          # comma required for single-element tuple!
# single = (42)         # ← this is just 42 (parentheses, not tuple)

# Without parentheses (tuple packing)
coordinates = 3, 4      # same as (3, 4)
a, b = 1, 2             # unpacking
x, *rest = [1,2,3,4,5]  # x=1, rest=[2,3,4,5]
first, *mid, last = [1,2,3,4,5]  # first=1, mid=[2,3,4], last=5
*_, last2 = [1,2,3]     # last2=3 (discard rest)

# Access same as list
t[0]; t[-1]; t[1:3]

# Named tuples — like lightweight classes
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x; p.y                # attribute access
p[0]; p[1]              # also index access
p._asdict()             # {'x': 3, 'y': 4}
p._replace(x=10)        # Point(x=10, y=4) — new tuple with replacement

# typing.NamedTuple — with type hints
from typing import NamedTuple
class Employee(NamedTuple):
    name: str
    dept: str
    salary: float = 0.0  # default value

e = Employee("Alice", "Engineering", 95000)

# When to use tuple vs list:
# tuple: fixed-size heterogeneous data (coordinates, RGB, DB rows, function returns)
#        hashable (can be dict key or set element if all elements are hashable)
#        slightly faster and less memory than list
# list:  homogeneous data that changes size or elements change

# Tuple as dict key
graph = {(0,0): "start", (1,0): "path", (1,1): "end"}
```

### 9.3 array Module and memoryview

```python
# For homogeneous numeric arrays — more memory efficient than lists
import array

# Type codes: 'b'=int8, 'B'=uint8, 'h'=int16, 'H'=uint16,
#             'i'=int32, 'I'=uint32, 'l'=int64, 'L'=uint64,
#             'f'=float32, 'd'=float64
arr = array.array('i', [1, 2, 3, 4, 5])   # array of signed ints
arr.append(6)
arr.extend([7, 8, 9])
arr[0]                  # 1 — indexing
arr.tolist()            # [1,2,3,4,5,6,7,8,9] — convert to list
arr.tobytes()           # raw bytes representation
arr.frombytes(b'\x00\x01')  # add from bytes

# memoryview — zero-copy view of buffer objects
data = bytearray(b'Hello, World!')
view = memoryview(data)
view[0]                 # 72 (ASCII 'H')
view[0:5]               # memoryview of first 5 bytes
bytes(view[0:5])        # b'Hello'
view[0] = 74            # changes 'H' to 'J' in original data!
# Useful for: processing binary protocols without copying

# For serious numeric work: use NumPy (see Chapter 30)
```

---

## Chapter 10: Dictionaries & Sets — Hash Tables Explained

### 10.1 How Python Dictionaries Work

```python
# Python dicts are hash tables (open addressing in CPython 3.6+)
# Since Python 3.7: insertion order is GUARANTEED (part of the language spec)

# Hash table: key → hash(key) → slot in an array → (key, value)

# Requirements for dict keys:
# 1. Must be HASHABLE (have __hash__ method)
# 2. Must be COMPARABLE (have __eq__ method)
# 3. hash(a) == hash(b) must hold if a == b

# Hashable types: int, float, complex, bool, str, bytes, tuple (if all elements hashable), frozenset
# NOT hashable: list, dict, set (mutable — their hash would change!)

# Why mutables can't be dict keys:
# If you mutate a key after insertion, hash changes, dict can't find it anymore → corruption

# Performance: O(1) average for get, set, delete
# Worst case: O(n) with many hash collisions (rare with good hash functions)
```

### 10.2 Dictionary Operations

```python
# ── Construction ──────────────────────────────────────────────
d = {}                              # empty
d = {"name": "Alice", "age": 30}   # literal (preferred)
d = dict(name="Alice", age=30)      # keyword args (keys must be identifiers)
d = dict([("name","Alice"),("age",30)])  # from list of pairs
d = dict.fromkeys(["a","b","c"], 0)      # {"a":0,"b":0,"c":0}
d = {k: v for k, v in pairs}            # dict comprehension

# ── Access ────────────────────────────────────────────────────
d["name"]               # "Alice" — KeyError if missing
d.get("name")           # "Alice" — None if missing (no error)
d.get("missing", "N/A") # "N/A"  — default value

# ── Modification ─────────────────────────────────────────────
d["email"] = "alice@example.com"       # add or update
d.update({"city": "NYC", "age": 31})   # update multiple
d.update(city="NYC", age=31)           # alternative syntax

# setdefault: get value or insert default if missing
d.setdefault("score", 0)   # returns 0 and sets d["score"]=0 if not present
d.setdefault("name", "Unknown")  # returns "Alice" (already exists, unchanged)

# ── Removal ──────────────────────────────────────────────────
del d["email"]                  # remove key (KeyError if absent)
val = d.pop("age")              # remove and return value (KeyError if absent)
val = d.pop("missing", None)    # remove, return default if absent
key, val = d.popitem()          # remove and return LAST inserted item (LIFO)
d.clear()                       # remove all items

# ── Membership ────────────────────────────────────────────────
"name" in d         # True — check key membership (O(1))
"Alice" in d        # False — not a VALUE check!
"Alice" in d.values()  # True — value check (O(n) linear scan)

# ── Iteration ────────────────────────────────────────────────
d = {"a": 1, "b": 2, "c": 3}

for key in d:                    # iterate keys (default)
    print(key)

for key in d.keys():             # explicit keys view
    print(key)

for val in d.values():           # values view
    print(val)

for key, val in d.items():       # items view (key, value pairs)
    print(f"{key}: {val}")

# Views are LIVE — they reflect changes to the dict
keys = d.keys()
d["d"] = 4
print(keys)   # dict_keys(['a', 'b', 'c', 'd']) — includes new key

# ── Merging ──────────────────────────────────────────────────
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}   # d2 wins for key "b"

merged = {**d1, **d2}          # {"a":1, "b":3, "c":4} — unpacking merge
merged = d1 | d2               # Python 3.9+ pipe operator (same result)
d1 |= d2                       # Python 3.9+ in-place merge

d1.update(d2)                  # modifies d1 in-place

# ── Dict comprehensions ───────────────────────────────────────
squares = {x: x**2 for x in range(1, 6)}   # {1:1, 2:4, 3:9, 4:16, 5:25}
inverted = {v: k for k, v in d.items()}     # swap keys and values
filtered = {k: v for k, v in d.items() if v > 1}

# ── Common patterns ───────────────────────────────────────────
# Counting occurrences
from collections import Counter
words = "the quick brown fox jumps over the lazy dog the".split()
counts = Counter(words)          # Counter({'the': 3, 'quick': 1, ...})
counts.most_common(3)            # [('the', 3), ('quick', 1), ('brown', 1)]
counts["the"]                    # 3
counts["missing"]                # 0 (Counter never raises KeyError)

# Grouping
from collections import defaultdict
by_length = defaultdict(list)    # default value is list() for missing keys
for word in words:
    by_length[len(word)].append(word)
# {3: ['the', 'fox', 'the', 'the'], 5: ['quick', 'brown', 'jumps', ...], ...}

# Nested dict (defaultdict of defaultdicts)
matrix = defaultdict(lambda: defaultdict(int))
matrix["row1"]["col1"] += 1     # no KeyError even for new keys

# OrderedDict (pre-3.7 dict didn't preserve order; now rarely needed)
from collections import OrderedDict
od = OrderedDict([("a", 1), ("b", 2)])
od.move_to_end("a")   # move "a" to end
od.move_to_end("b", last=False)  # move "b" to front
```

### 10.3 Sets

```python
# Set: unordered, unique elements, mutable, elements must be hashable
# Implemented as hash table with only keys (no values) → O(1) membership

s = {1, 2, 3, 4, 5}
empty_set = set()          # NOT {} — that's an empty dict!
s2 = set([1, 2, 2, 3])   # {1, 2, 3} — duplicates removed
s3 = frozenset({1, 2, 3}) # immutable set — hashable (can be dict key)

# ── Operations ────────────────────────────────────────────────
s.add(6)            # add element
s.discard(10)       # remove if present (no error if absent)
s.remove(5)         # remove (KeyError if absent)
s.pop()             # remove and return ARBITRARY element

# ── Set math ─────────────────────────────────────────────────
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

a | b               # {1,2,3,4,5,6,7,8} — union (OR)
a & b               # {4, 5}            — intersection (AND)
a - b               # {1, 2, 3}         — difference (in a, not in b)
b - a               # {6, 7, 8}         — difference (in b, not in a)
a ^ b               # {1,2,3,6,7,8}     — symmetric difference (XOR, not in both)

# Augmented assignment (in-place)
a |= b              # a = a | b
a &= b              # a = a & b
a -= b              # a = a - b
a ^= b              # a = a ^ b

# Subset / superset
{1, 2} <= {1, 2, 3}    # True — is subset
{1, 2} < {1, 2, 3}     # True — is PROPER subset (not equal)
{1, 2, 3} >= {1, 2}    # True — is superset
a.isdisjoint(b)         # True if no common elements
a.issubset(b)           # equivalent to a <= b
a.issuperset(b)         # equivalent to a >= b

# ── Common uses ───────────────────────────────────────────────
# Deduplication
unique = list(set([1,2,2,3,3,3]))   # [1, 2, 3] — order not guaranteed

# O(1) membership test (vs O(n) for list)
valid_extensions = {".jpg", ".png", ".gif", ".webp"}
if ext in valid_extensions: ...     # O(1) hash lookup

# Set comprehension
evens = {x for x in range(20) if x % 2 == 0}

# Find common elements
set1 = {"alice", "bob", "carol"}
set2 = {"bob", "dave", "carol"}
common = set1 & set2   # {"bob", "carol"}
only_in_1 = set1 - set2  # {"alice"}
```

---

## Chapter 11: Comprehensions & Functional Tools

### 11.1 All Comprehension Types

```python
# ── List comprehension ────────────────────────────────────────
# [expression for item in iterable if condition]
squares    = [x**2 for x in range(10)]
evens      = [x for x in range(20) if x % 2 == 0]
processed  = [x.strip().lower() for x in lines if x.strip()]

# Nested loops in comprehension
pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
# [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]

matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat   = [x for row in matrix for x in row]     # [1,2,3,4,5,6,7,8,9]
transposed = [[row[i] for row in matrix] for i in range(3)]  # transpose matrix

# ── Dict comprehension ────────────────────────────────────────
squares_dict = {x: x**2 for x in range(1, 6)}
inverted     = {v: k for k, v in original.items()}
scores       = {name: get_score(name) for name in students if is_eligible(name)}

# ── Set comprehension ─────────────────────────────────────────
unique_lengths = {len(word) for word in words}
first_chars    = {s[0].upper() for s in strings if s}

# ── Generator expression ─────────────────────────────────────
# Like list comprehension but LAZY (no [] brackets — use ())
gen = (x**2 for x in range(1000000))    # no memory allocated
sum(x**2 for x in range(1000000))       # efficient: no list created
any(x > 500 for x in range(1000))       # short-circuits at x=501

# As function argument (no extra parens needed if only argument):
sum(x**2 for x in range(10))     # ← no extra () needed here
max(len(s) for s in strings)
",".join(str(x) for x in nums)
```

### 11.2 itertools — The Iteration Toolkit

```python
import itertools as it

# ── Infinite iterators ────────────────────────────────────────
it.count(10, 2)          # 10, 12, 14, 16, ... (infinite arithmetic sequence)
it.cycle([1, 2, 3])      # 1, 2, 3, 1, 2, 3, ... (infinite cycle)
it.repeat(42)            # 42, 42, 42, ... (infinite)
it.repeat(42, 5)         # 42, 42, 42, 42, 42 (finite)

# ── Finite iterators ──────────────────────────────────────────
list(it.chain([1,2],[3,4],[5]))            # [1,2,3,4,5] — concatenate iterables
list(it.chain.from_iterable([[1,2],[3,4]])) # same, from nested iterable
list(it.islice(range(100), 5, 20, 3))      # [5,8,11,14,17] — slice iterator
list(it.takewhile(lambda x: x<5, range(10))) # [0,1,2,3,4]
list(it.dropwhile(lambda x: x<5, range(10))) # [5,6,7,8,9]
list(it.filterfalse(lambda x: x%2, range(10))) # [0,2,4,6,8] — filter(not pred)
list(it.compress("ABCDE", [1,0,1,0,1]))   # ['A','C','E'] — select by mask

# ── Combinatoric iterators ────────────────────────────────────
list(it.permutations("ABC", 2))     # all 2-length permutations
# [('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')]

list(it.combinations("ABC", 2))     # all 2-length combinations (no repeats)
# [('A','B'),('A','C'),('B','C')]

list(it.combinations_with_replacement("AB", 2))  # with repetition
# [('A','A'),('A','B'),('B','B')]

list(it.product("AB", repeat=2))    # Cartesian product
# [('A','A'),('A','B'),('B','A'),('B','B')]

# ── Grouping ─────────────────────────────────────────────────
# groupby: groups consecutive elements with same key
# IMPORTANT: input must be SORTED by the same key first
data = sorted([("alice", 90), ("bob", 85), ("alice", 95)], key=lambda x: x[0])
for name, group in it.groupby(data, key=lambda x: x[0]):
    scores = [score for _, score in group]
    print(f"{name}: {scores}")
# alice: [90, 95]
# bob: [85]

# ── Accumulate ────────────────────────────────────────────────
list(it.accumulate([1,2,3,4,5]))                    # [1,3,6,10,15] — running sum
list(it.accumulate([1,2,3,4,5], max))               # [1,2,3,4,5] — running max
list(it.accumulate([1,2,3,4,5], lambda a,b: a*b))   # [1,2,6,24,120] — factorial
list(it.accumulate([1,2,3,4,5], initial=0))          # [0,1,3,6,10,15] — with initial

# ── Zip variants ──────────────────────────────────────────────
list(it.zip_longest([1,2,3],[4,5], fillvalue=0))    # [(1,4),(2,5),(3,0)]
list(it.pairwise([1,2,3,4,5]))    # [(1,2),(2,3),(3,4),(4,5)] Python 3.10+

# ── Practical examples ────────────────────────────────────────
# Generate batches
def batched(iterable, n):          # Python 3.12: it.batched()
    it_iter = iter(iterable)
    while batch := list(it.islice(it_iter, n)):
        yield batch

list(batched(range(10), 3))   # [[0,1,2],[3,4,5],[6,7,8],[9]]

# Flatten nested structure
def flatten(nested):
    return it.chain.from_iterable(nested)

list(flatten([[1,2],[3,4],[5]]))  # [1,2,3,4,5]

# Sliding window
def sliding_window(iterable, n):
    iters = it.tee(iterable, n)
    for i, it_ in enumerate(iters):
        next(it.islice(it_, i, i), None)   # advance each iterator
    return zip(*iters)
# Or use collections.deque with maxlen:
from collections import deque
def sliding_window2(iterable, n):
    window = deque(it.islice(iterable, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for item in iterable:
        window.append(item)
        yield tuple(window)
```
# Python Mastery Guide — Part 2
# Chapters 12–20: OOP Deep Dive, Modern Python, Async

---

## Chapter 12: Classes & the Data Model

### 12.1 Class Anatomy — Everything Inside a Class

```python
class BankAccount:
    """
    A bank account with deposit, withdrawal, and interest.
    
    Class docstring — access via BankAccount.__doc__
    """

    # ── Class variables — shared across ALL instances ─────────
    interest_rate: float = 0.05          # type-annotated class variable
    _total_accounts: int = 0             # private (convention: single underscore)
    __bank_name: str = "PyBank"          # name-mangled: _BankAccount__bank_name
    MIN_BALANCE: float = 0.0             # constant by convention (UPPERCASE)

    # ── __slots__ — restrict instance dict (memory optimization) ──
    # If defined, instances use a fixed array instead of __dict__
    # __slots__ = ('_owner', '_balance', '_id')  # uncomment to enable

    # ── __init__ — initializer (NOT constructor; object already exists) ──
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        if initial_balance < self.MIN_BALANCE:
            raise ValueError(f"Initial balance cannot be negative, got {initial_balance}")
        # Instance variables — unique to each instance
        self._owner:   str   = owner
        self._balance: float = initial_balance
        self._id:      int   = BankAccount._total_accounts
        self._history: list  = []

        BankAccount._total_accounts += 1   # update class variable via class name

    # ── Instance methods — take self as first argument ────────
    def deposit(self, amount: float) -> "BankAccount":
        """Deposit amount. Returns self for chaining."""
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}")
        self._balance += amount
        self._history.append(("deposit", amount, self._balance))
        return self   # enables method chaining: account.deposit(100).deposit(50)

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            return False
        self._balance -= amount
        self._history.append(("withdraw", amount, self._balance))
        return True

    # ── Properties — controlled attribute access ───────────────
    @property
    def balance(self) -> float:
        """Read-only balance property."""
        return self._balance

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValueError("Owner name cannot be empty")
        self._owner = new_name.strip()

    @property
    def history(self) -> list:
        return list(self._history)   # return copy so caller can't mutate internal state

    # ── Class methods — take cls as first argument ─────────────
    @classmethod
    def from_dict(cls, data: dict) -> "BankAccount":
        """Alternative constructor from dictionary."""
        return cls(owner=data["owner"], initial_balance=data.get("balance", 0.0))

    @classmethod
    def get_total_accounts(cls) -> int:
        return cls._total_accounts

    @classmethod
    def set_interest_rate(cls, rate: float) -> None:
        if not 0 <= rate <= 1:
            raise ValueError("Interest rate must be between 0 and 1")
        cls.interest_rate = rate

    # ── Static methods — no self or cls, logically grouped ─────
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate a monetary amount. No access to instance or class."""
        return isinstance(amount, (int, float)) and amount > 0

    # ── Dunder methods for Python protocol ────────────────────
    def __repr__(self) -> str:
        """Unambiguous developer representation: eval(repr(obj)) should recreate obj."""
        return f"BankAccount(owner={self._owner!r}, initial_balance={self._balance!r})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Account #{self._id} ({self._owner}): ${self._balance:,.2f}"

    def __len__(self) -> int:
        """len(account) returns number of transactions."""
        return len(self._history)

    def __bool__(self) -> bool:
        """bool(account) is True if balance > 0."""
        return self._balance > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented   # not False! — lets other side try
        return self._id == other._id

    def __hash__(self) -> int:
        """Required when defining __eq__; use immutable identity."""
        return hash(self._id)

    def __lt__(self, other: "BankAccount") -> bool:
        return self._balance < other._balance

    def __add__(self, other: "BankAccount") -> "BankAccount":
        """account1 + account2 → merge accounts."""
        merged = BankAccount(f"{self._owner} & {other._owner}")
        merged._balance = self._balance + other._balance
        return merged

    def __contains__(self, transaction_type: str) -> bool:
        """'deposit' in account → True if any deposit exists."""
        return any(t[0] == transaction_type for t in self._history)

    def __iter__(self):
        """for transaction in account → iterate history."""
        return iter(self._history)

    def __getitem__(self, index: int) -> tuple:
        """account[0] → first transaction."""
        return self._history[index]

    def __del__(self) -> None:
        """Finalizer — called when object is garbage collected."""
        # Avoid heavy work here; not guaranteed to run, not guaranteed when
        BankAccount._total_accounts = max(0, BankAccount._total_accounts - 1)


# ── Usage ─────────────────────────────────────────────────────
acc = BankAccount("Alice", 1000.0)
acc.deposit(500).deposit(250)  # method chaining
acc.withdraw(200)

print(acc)                    # Account #0 (Alice): $1,550.00
print(repr(acc))              # BankAccount(owner='Alice', initial_balance=1000.0)
print(acc.balance)            # 1550.0 — via property
print(len(acc))               # 3 — transactions
print(bool(acc))              # True — has balance
print("deposit" in acc)       # True — has deposits

for txn in acc:               # iterate transactions
    print(txn)

acc2 = BankAccount.from_dict({"owner": "Bob", "balance": 500.0})
merged = acc + acc2           # __add__
print(merged.balance)         # 2050.0

print(BankAccount.get_total_accounts())  # class method
print(BankAccount._BankAccount__bank_name)  # name mangling access
```

### 12.2 Class vs Instance Variable — The Lookup Chain

```python
class Demo:
    class_var = "class"

    def __init__(self):
        self.instance_var = "instance"

d = Demo()

# Attribute lookup order (MRO + instance dict + class dict):
# 1. Data descriptors from class (properties with __set__)
# 2. Instance __dict__
# 3. Non-data descriptors + class __dict__

# Class var accessed from instance:
print(d.class_var)         # "class" — falls through to class dict
d.class_var = "shadow"     # creates instance var that SHADOWS class var
print(d.class_var)         # "shadow" — instance dict
print(Demo.class_var)      # "class"  — class dict unchanged

# DANGEROUS mutation pattern
class Counter:
    count = 0          # class variable — shared!

    def increment(self):
        self.count += 1    # creates INSTANCE variable 'count' — doesn't change class var!

c1 = Counter()
c2 = Counter()
c1.increment()
print(c1.count)       # 1 — instance var
print(c2.count)       # 0 — class var (unchanged)
print(Counter.count)  # 0 — class var (unchanged)

# Fix: always reference class variable through class name
class Counter2:
    count = 0
    def increment(self):
        Counter2.count += 1   # modifies class variable correctly
```

### 12.3 __new__ vs __init__ — Object Creation

```python
# __new__: creates the object (allocates memory), returns the new instance
# __init__: initializes the object, receives the new instance as self
# Called in order: __new__ → __init__

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value: int):
        self.value = value

s1 = Singleton(1)
s2 = Singleton(2)
print(s1 is s2)        # True — same object
print(s1.value)        # 2 — __init__ ran again on same object


# Immutable classes use __new__ to set values (can't set in __init__ for truly immutable)
class ImmutablePoint:
    def __new__(cls, x: float, y: float):
        instance = super().__new__(cls)
        object.__setattr__(instance, '_x', x)   # bypass __setattr__
        object.__setattr__(instance, '_y', y)
        return instance

    @property
    def x(self): return self._x
    @property
    def y(self): return self._y

    def __setattr__(self, name, value):
        raise AttributeError("ImmutablePoint is immutable")

    def __repr__(self):
        return f"ImmutablePoint({self._x}, {self._y})"

p = ImmutablePoint(3, 4)
print(p.x)              # 3
# p.x = 10             # AttributeError: ImmutablePoint is immutable


# __new__ for custom type creation (metaclass-like behavior)
class TypeChecked:
    """Only allows integer attributes."""
    def __setattr__(self, name, value):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be int, got {type(value).__name__}")
        super().__setattr__(name, value)
```

---

## Chapter 13: Inheritance, MRO & Mixins

### 13.1 Single Inheritance

```python
class Animal:
    def __init__(self, name: str, sound: str):
        self.name  = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"

    def describe(self) -> str:
        return f"I am {self.name}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, "Woof")   # super() calls parent __init__
        self.breed = breed

    # Override parent method
    def speak(self) -> str:
        return f"{self.name} barks: WOOF WOOF!"

    # Extend parent method (call parent + add behavior)
    def describe(self) -> str:
        base = super().describe()        # get parent's description
        return f"{base}, a {self.breed} dog"

    # New method only in Dog
    def fetch(self, item: str) -> str:
        return f"{self.name} fetches the {item}!"


class GuideDog(Dog):
    def __init__(self, name: str, breed: str, owner: str):
        super().__init__(name, breed)
        self.owner = owner

    def speak(self) -> str:
        parent = super().speak()
        return f"{parent} (quietly, this is a guide dog)"


rex = Dog("Rex", "Labrador")
print(rex.speak())       # Rex barks: WOOF WOOF!
print(rex.describe())    # I am Rex, a Labrador dog
print(rex.fetch("ball")) # Rex fetches the ball!

# isinstance and issubclass
print(isinstance(rex, Dog))    # True
print(isinstance(rex, Animal)) # True (Dog IS-A Animal)
print(issubclass(Dog, Animal)) # True
print(issubclass(Animal, Dog)) # False

# Accessing class hierarchy
print(Dog.__bases__)           # (<class '__main__.Animal'>,)
print(Dog.__mro__)             # MRO tuple
```

### 13.2 MRO — Method Resolution Order

```python
# Python uses C3 Linearization algorithm to determine MRO
# MRO determines which method gets called in multiple inheritance

class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):
    pass  # no method override

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# Python reads left-to-right, bottom-to-top in the class hierarchy

d = D()
print(d.method())    # "B" — first in MRO after D itself

# The Diamond Problem — Python's MRO solves it cleanly
#     A
#    / \
#   B   C
#    \ /
#     D
# A.method() called ONCE, from the most-derived class first

class A:
    def greet(self):
        print("A.greet")
        super().greet()   # super() in MRO context — calls next in MRO

class B(A):
    def greet(self):
        print("B.greet")
        super().greet()

class C(A):
    def greet(self):
        print("C.greet")
        super().greet()

class D(B, C):
    def greet(self):
        print("D.greet")
        super().greet()

# MRO: D → B → C → A → object
d = D()
d.greet()
# D.greet
# B.greet
# C.greet
# A.greet
# Each super() forwards to the NEXT class in MRO — cooperative multiple inheritance
```

### 13.3 Mixins — Composing Behavior

```python
# Mixins: small, focused classes that add specific behavior
# Not meant to be instantiated alone; mixed into other classes

class SerializableMixin:
    """Adds JSON serialization to any class."""
    import json as _json

    def to_dict(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_')
        }

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj


class LoggableMixin:
    """Adds logging to method calls."""
    import logging as _logging

    def _log(self, msg: str, level: str = "info") -> None:
        logger = __import__("logging").getLogger(self.__class__.__name__)
        getattr(logger, level)(msg)


class TimestampMixin:
    """Adds created_at and updated_at timestamps."""
    from datetime import datetime

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime, timezone
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def touch(self) -> None:
        from datetime import datetime, timezone
        self.updated_at = datetime.now(timezone.utc)


class ValidatableMixin:
    """Adds validate() hook called after __init__."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    def validate(self) -> None:
        """Override in subclass to add validation logic."""
        pass


# Compose mixins into a real class
class User(TimestampMixin, SerializableMixin, LoggableMixin):
    def __init__(self, name: str, email: str):
        super().__init__()    # cooperative super() chains through mixins
        self.name  = name
        self.email = email

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.touch()          # from TimestampMixin
        self._log(f"User {self.name} updated")  # from LoggableMixin

user = User("Alice", "alice@example.com")
print(user.to_json())         # from SerializableMixin
user.update(name="Alice Smith")
print(user.created_at)        # from TimestampMixin
```

### 13.4 Abstract Base Classes

```python
from abc import ABC, abstractmethod, abstractproperty
from typing import Iterator

class Shape(ABC):
    """Abstract base class for all shapes."""

    @abstractmethod
    def area(self) -> float:
        """Must be implemented by subclass."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    # Concrete method in ABC — subclasses inherit this
    def describe(self) -> str:
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

    # __init_subclass__ — runs when a subclass is defined
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"New Shape subclass registered: {cls.__name__}")


class Circle(Shape):
    import math

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

    @property
    def name(self) -> str:
        return "Circle"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:      return self.width * self.height
    def perimeter(self) -> float: return 2 * (self.width + self.height)

    @property
    def name(self) -> str:        return "Rectangle"


# Shape()   # TypeError: Can't instantiate abstract class Shape
c = Circle(5)
print(c.describe())   # Circle: area=78.54, perimeter=31.42

# Register an existing class as a "virtual subclass" of ABC
class Triangle:  # doesn't inherit Shape
    def area(self): return 6.0
    def perimeter(self): return 12.0
    name = "Triangle"

Shape.register(Triangle)
print(isinstance(Triangle(), Shape))   # True — virtual subclass

# ABC from collections.abc for container protocols
from collections.abc import MutableMapping, Sequence, Iterable

class MyMapping(MutableMapping):
    def __init__(self): self._data = {}
    def __getitem__(self, key): return self._data[key]
    def __setitem__(self, key, val): self._data[key] = val
    def __delitem__(self, key): del self._data[key]
    def __iter__(self): return iter(self._data)
    def __len__(self): return len(self._data)
    # MutableMapping provides: get, pop, update, keys, values, items, __contains__
```

---

## Chapter 14: Dunder Methods — The Full Protocol

### 14.1 Arithmetic Operators

```python
class Vector:
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x, self.y, self.z = x, y, z

    # ── Binary arithmetic ─────────────────────────────────────
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented   # allows Python to try other.__radd__(self)
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        """Right-hand add: called when other + self fails (other doesn't know Vector)."""
        return self.__add__(other)   # addition is commutative

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector":
        """Vector * scalar."""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
        return NotImplemented

    def __rmul__(self, scalar: float) -> "Vector":
        """scalar * Vector — Python tries this when scalar.__mul__(vector) returns NotImplemented."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vector":
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar: float) -> "Vector":
        return Vector(self.x // scalar, self.y // scalar, self.z // scalar)

    def __mod__(self, scalar: float) -> "Vector":
        return Vector(self.x % scalar, self.y % scalar, self.z % scalar)

    def __pow__(self, exp: float) -> "Vector":
        return Vector(self.x ** exp, self.y ** exp, self.z ** exp)

    def __matmul__(self, other: "Vector") -> float:
        """@ operator — dot product."""
        return self.x*other.x + self.y*other.y + self.z*other.z

    # ── In-place arithmetic (augmented assignment) ────────────
    def __iadd__(self, other: "Vector") -> "Vector":
        """v += other — modify self in place, return self."""
        self.x += other.x; self.y += other.y; self.z += other.z
        return self

    def __imul__(self, scalar: float) -> "Vector":
        self.x *= scalar; self.y *= scalar; self.z *= scalar
        return self

    # ── Unary operators ───────────────────────────────────────
    def __neg__(self) -> "Vector":      return Vector(-self.x, -self.y, -self.z)
    def __pos__(self) -> "Vector":      return Vector(+self.x, +self.y, +self.z)
    def __abs__(self) -> float:
        """abs(v) → magnitude."""
        import math
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __round__(self, n: int = 0) -> "Vector":
        return Vector(round(self.x, n), round(self.y, n), round(self.z, n))

    # ── Comparison ────────────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector): return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __lt__(self, other: "Vector") -> bool:
        return abs(self) < abs(other)   # compare by magnitude

    def __le__(self, other: "Vector") -> bool:  return abs(self) <= abs(other)
    def __gt__(self, other: "Vector") -> bool:  return abs(self) >  abs(other)
    def __ge__(self, other: "Vector") -> bool:  return abs(self) >= abs(other)

    # ── Representation ────────────────────────────────────────
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __format__(self, spec: str) -> str:
        """f"{v:.2f}" → custom formatting."""
        if spec:
            return f"Vector({self.x:{spec}}, {self.y:{spec}}, {self.z:{spec}})"
        return repr(self)

    def __bool__(self) -> bool:  return abs(self) != 0
    def __hash__(self) -> int:   return hash((self.x, self.y, self.z))


v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
print(v1 + v2)          # Vector(5, 7, 9)
print(v1 * 2)           # Vector(2, 4, 6)
print(3 * v1)           # Vector(3, 6, 9) — __rmul__
print(v1 @ v2)          # 32.0 — dot product
print(abs(v1))          # 3.7416...
print(f"{v1:.2f}")      # Vector(1.00, 2.00, 3.00)
print(-v1)              # Vector(-1, -2, -3)
```

### 14.2 Container & Sequence Protocol

```python
class SortedList:
    """Always-sorted list with full container protocol."""

    def __init__(self, iterable=None):
        self._data = sorted(iterable) if iterable else []

    # ── Core container protocol ───────────────────────────────
    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index):
        """Support index and slice access."""
        return self._data[index]   # slicing returns a list, not SortedList

    def __setitem__(self, index, value):
        self._data[index] = value
        self._data.sort()          # maintain sorted order

    def __delitem__(self, index):
        del self._data[index]

    def __contains__(self, item) -> bool:
        """'x' in sl — uses binary search for O(log n)."""
        import bisect
        i = bisect.bisect_left(self._data, item)
        return i < len(self._data) and self._data[i] == item

    # ── Iteration ─────────────────────────────────────────────
    def __iter__(self):
        return iter(self._data)

    def __reversed__(self):
        return reversed(self._data)

    # ── Adding items ──────────────────────────────────────────
    def append(self, item) -> None:
        import bisect
        bisect.insort(self._data, item)   # insert in sorted position O(n) but sorted

    def extend(self, iterable) -> None:
        for item in iterable:
            self.append(item)

    def __iadd__(self, iterable):
        self.extend(iterable)
        return self

    # ── Copy ─────────────────────────────────────────────────
    def __copy__(self):
        import copy
        return SortedList(copy.copy(self._data))

    def __deepcopy__(self, memo):
        import copy
        return SortedList(copy.deepcopy(self._data, memo))

    def __repr__(self): return f"SortedList({self._data!r})"


sl = SortedList([5, 2, 8, 1, 9])
print(sl)            # SortedList([1, 2, 5, 8, 9])
print(3 in sl)       # False
sl.append(3)
print(3 in sl)       # True
print(sl[2])         # 3
for x in sl: print(x)   # 1 2 3 5 8 9
```

### 14.3 Context Manager Protocol

```python
# __enter__ and __exit__ — for the 'with' statement

class DatabaseTransaction:
    def __init__(self, connection):
        self.conn = connection
        self.tx   = None

    def __enter__(self):
        """Called at 'with' entry. Return value bound to 'as' target."""
        self.tx = self.conn.begin_transaction()
        return self.tx    # → the tx object bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Called at 'with' exit, even on exception.
        
        Args:
            exc_type: Exception class if exception occurred, else None
            exc_val:  Exception instance
            exc_tb:   Traceback object
        
        Returns:
            True  → exception is suppressed (swallowed)
            False → exception propagates (or no exception)
        """
        if exc_type is None:
            # No exception → commit
            self.tx.commit()
        else:
            # Exception occurred → rollback
            self.tx.rollback()
            # Return False to let the exception propagate
        return False   # don't suppress exceptions


# Usage
with DatabaseTransaction(conn) as tx:
    tx.execute("INSERT INTO users VALUES (?)", ("Alice",))
    tx.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    # If any line raises, __exit__ rolls back automatically

# Timer context manager
import time

class Timer:
    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self._start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False   # don't suppress exceptions

    @property
    def seconds(self): return self.elapsed

with Timer() as t:
    time.sleep(0.1)
    heavy_computation()
print(f"Took {t.seconds:.4f}s")

# Suppress specific exceptions
class Suppress:
    def __init__(self, *exception_types):
        self.exception_types = exception_types

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return exc_type is not None and issubclass(exc_type, self.exception_types)

with Suppress(FileNotFoundError):
    os.remove("nonexistent.txt")   # silently suppressed
# equivalent to contextlib.suppress
```

---

## Chapter 15: Descriptors, Properties & __slots__

### 15.1 The Descriptor Protocol

```python
# A descriptor is any object that defines __get__, __set__, or __delete__
# Properties are implemented as descriptors under the hood

# Data descriptor: defines __set__ (or __delete__) — takes priority over instance __dict__
# Non-data descriptor: only defines __get__ — instance __dict__ takes priority

class Validator:
    """Descriptor that validates type and range."""

    def __init__(self, type_, min_=None, max_=None, name=None):
        self.type_ = type_
        self.min_  = min_
        self.max_  = max_
        self.name  = name   # set by __set_name__

    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to a class attribute.
        owner = the class; name = attribute name."""
        self.name     = name
        self.storage  = f"_{name}"   # store actual value in _name

    def __get__(self, obj, objtype=None):
        """Called on attribute access: obj.name or Class.name"""
        if obj is None:
            return self   # Class.name → return the descriptor itself
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        """Called on attribute assignment: obj.name = value"""
        if not isinstance(value, self.type_):
            raise TypeError(
                f"{self.name} must be {self.type_.__name__}, got {type(value).__name__}"
            )
        if self.min_ is not None and value < self.min_:
            raise ValueError(f"{self.name} must be >= {self.min_}, got {value}")
        if self.max_ is not None and value > self.max_:
            raise ValueError(f"{self.name} must be <= {self.max_}, got {value}")
        setattr(obj, self.storage, value)

    def __delete__(self, obj):
        delattr(obj, self.storage)


class Person:
    # Descriptors are class variables
    name  = Validator(str)
    age   = Validator(int,   min_=0,   max_=150)
    score = Validator(float, min_=0.0, max_=100.0)

    def __init__(self, name: str, age: int, score: float):
        self.name  = name    # calls Validator.__set__
        self.age   = age
        self.score = score


p = Person("Alice", 30, 95.5)
# Person("Alice", -1, 95.5)   # ValueError: age must be >= 0
# Person(123, 30, 95.5)       # TypeError: name must be str


# Property is a built-in descriptor — equivalent to above but simpler
class Temperature:
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"Temperature below absolute zero: {value}")
        self._celsius = value

    @celsius.deleter
    def celsius(self) -> None:
        del self._celsius

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5/9  # goes through celsius setter for validation
```

### 15.2 __slots__ — Memory Optimization

```python
# By default, each instance stores attributes in a __dict__ (a dictionary)
# __slots__ replaces __dict__ with a fixed array — saves 40-60% memory per instance

class Point:
    __slots__ = ('x', 'y')   # only these attributes allowed

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


import sys
class PointDict:
    def __init__(self, x, y): self.x, self.y = x, y

p1 = Point(1.0, 2.0)
p2 = PointDict(1.0, 2.0)

print(sys.getsizeof(p1))              # ~56 bytes (slots)
print(sys.getsizeof(p2))              # ~56 bytes (object)
# print(sys.getsizeof(p2.__dict__))   # ~232 bytes (the dict alone!)

# p1.z = 3.0   # AttributeError: 'Point' object has no attribute 'z'
# p1.__dict__  # AttributeError: 'Point' has no __dict__

# Inheritance with __slots__:
class Point3D(Point):
    __slots__ = ('z',)   # add slot; inherits x, y from Point
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

# If subclass doesn't define __slots__, it gets a __dict__ anyway
# — subclasses MUST also define __slots__ for the optimization to hold

# When to use __slots__:
# ✅ Classes with many instances (data science, game objects, millions of points)
# ✅ Known-at-design-time attribute set that never changes
# ❌ When you need to add arbitrary attributes dynamically
# ❌ When using __weakref__ (add '__weakref__' to __slots__ if needed)
# ❌ When pickling (extra steps needed)
```

---

## Chapter 16: Metaclasses

### 16.1 What Are Metaclasses?

```python
# In Python, EVERYTHING is an object — including classes.
# A metaclass is the class of a class. It controls class creation.

# type() is the default metaclass of all classes
print(type(42))         # <class 'int'>
print(type(int))        # <class 'type'>   — int is an instance of type!
print(type(type))       # <class 'type'>   — type is its own metaclass

class Foo: pass
print(type(Foo))        # <class 'type'>   — all classes are instances of type

# type() can create classes dynamically:
# type(name, bases, dict) → creates a new class
MyClass = type('MyClass', (object,), {
    'x': 10,
    'greet': lambda self: f"Hello from {self.x}",
})
obj = MyClass()
print(obj.greet())      # Hello from 10

# Class creation process:
# 1. Python reads the class body and builds a namespace dict
# 2. Calls metaclass(name, bases, namespace) to create the class object
# 3. Default metaclass is type; can be overridden
```

### 16.2 Custom Metaclass

```python
class SingletonMeta(type):
    """Metaclass that ensures only one instance per class."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Called when class is instantiated: MyClass(...)."""
        if cls not in cls._instances:
            # type.__call__ creates and initializes the instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def connect(self): pass


db1 = Database("postgresql://localhost/mydb")
db2 = Database("postgresql://other/db")   # __init__ runs but returns same object
print(db1 is db2)     # True — singleton!
print(db2.url)        # "postgresql://localhost/mydb" — first init wins


class RegistryMeta(type):
    """Metaclass that auto-registers all subclasses."""
    _registry: dict = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself, only subclasses
        if bases:
            mcs._registry[name] = cls
        return cls

    @classmethod
    def get_registry(mcs) -> dict:
        return dict(mcs._registry)


class Plugin(metaclass=RegistryMeta):
    def run(self): raise NotImplementedError


class EmailPlugin(Plugin):
    def run(self): print("Sending email")


class SlackPlugin(Plugin):
    def run(self): print("Sending to Slack")


print(RegistryMeta.get_registry())
# {'EmailPlugin': <class '__main__.EmailPlugin'>, 'SlackPlugin': ...}

# Dynamically run a plugin by name
plugin_name = "EmailPlugin"
RegistryMeta.get_registry()[plugin_name]().run()   # Sending email


class ValidatedMeta(type):
    """Metaclass that validates class definition at class creation time."""

    def __new__(mcs, name, bases, namespace):
        # Enforce: all public methods must have type annotations
        for attr_name, attr_val in namespace.items():
            if callable(attr_val) and not attr_name.startswith('_'):
                if not hasattr(attr_val, '__annotations__'):
                    pass  # simplification; real check uses inspect
        
        # Enforce: must define 'schema' class attribute
        if bases and 'schema' not in namespace:
            raise TypeError(f"Class {name} must define a 'schema' attribute")
        
        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ValidatedMeta):
    schema = {}   # base class defines it

class UserModel(Model):
    schema = {"name": str, "age": int}  # ✅

# class BadModel(Model):  # ❌ TypeError: must define schema
#     pass
```

### 16.3 __init_subclass__ — Lighter Than Metaclass

```python
# Python 3.6+: __init_subclass__ is called when a class is subclassed
# Simpler alternative to metaclasses for many use cases

class Plugin:
    _registry: dict = {}

    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        """Called when Plugin is subclassed."""
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls
        print(f"Plugin registered: {name}")

    @classmethod
    def get(cls, name: str) -> type:
        return cls._registry[name]


class EmailSender(Plugin, plugin_name="email"):
    def send(self, to: str, msg: str): print(f"Email to {to}: {msg}")

class SlackSender(Plugin, plugin_name="slack"):
    def send(self, channel: str, msg: str): print(f"Slack #{channel}: {msg}")


sender = Plugin.get("email")()
sender.send("alice@example.com", "Hello!")
```

---

## Chapter 17: Type Hints & Static Analysis

### 17.1 Type Hints — Complete Reference

```python
from typing import (
    Any, Union, Optional, Literal, Final, ClassVar,
    List, Dict, Set, Tuple, FrozenSet, Deque, DefaultDict,
    Callable, Iterator, Generator, AsyncIterator, AsyncGenerator,
    Type, TypeVar, Generic, Protocol, runtime_checkable,
    Awaitable, Coroutine, AsyncContextManager, ContextManager,
    NamedTuple, TypedDict, overload, cast, TYPE_CHECKING,
    get_type_hints, get_args, get_origin
)
from typing import Annotated   # Python 3.9+
import sys

# ── Basic types ───────────────────────────────────────────────
x: int    = 42
y: float  = 3.14
s: str    = "hello"
b: bool   = True
n: None   = None   # the value None

# ── Union types ───────────────────────────────────────────────
# Old syntax:
def f(x: Union[int, str]) -> None: ...
# Python 3.10+ new syntax:
def f2(x: int | str) -> None: ...

# Optional[T] = Union[T, None] = T | None
def g(name: Optional[str] = None) -> str:
    return name or "default"

# ── Literal — restrict to specific values ─────────────────────
from typing import Literal
Direction = Literal["north", "south", "east", "west"]
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def move(direction: Direction, steps: int) -> None: ...
def request(method: HttpMethod, url: str) -> None: ...

# move("diagonal")   # mypy/pyright error: not a valid Direction

# ── Collection types (Python 3.9+: use built-in directly) ─────
# Old:  List[int], Dict[str, int], Tuple[int, ...]
# New:  list[int], dict[str, int], tuple[int, ...]

names: list[str]          = ["Alice", "Bob"]
scores: dict[str, int]    = {"Alice": 90}
point: tuple[int, int]    = (3, 4)
mixed: tuple[str, int, float] = ("Alice", 30, 95.5)  # fixed-length
coords: tuple[float, ...] = (1.0, 2.0, 3.0)  # variable-length, all float
unique: set[str]          = {"a", "b", "c"}
frozen: frozenset[int]    = frozenset({1, 2, 3})

# ── Callable ──────────────────────────────────────────────────
# Callable[[arg1_type, arg2_type], return_type]
from typing import Callable

Predicate = Callable[[int], bool]
Transformer = Callable[[str, int], str]

def apply(items: list[int], pred: Predicate) -> list[int]:
    return [x for x in items if pred(x)]

# ── TypeVar — generic type variable ───────────────────────────
T   = TypeVar("T")
K   = TypeVar("K")
V   = TypeVar("V")
T_co = TypeVar("T_co", covariant=True)     # covariant
T_contra = TypeVar("T_contra", contravariant=True)  # contravariant
Num = TypeVar("Num", int, float, complex)  # constrained: only these types

def first(lst: list[T]) -> T:              # return type matches input type
    return lst[0]

n: int   = first([1, 2, 3])     # T=int
s: str   = first(["a", "b"])    # T=str

def add_items(a: Num, b: Num) -> Num:      # constrained TypeVar
    return a + b

# ── Generic classes ───────────────────────────────────────────
from typing import Generic

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)


int_stack: Stack[int] = Stack()
int_stack.push(1)
x2: int = int_stack.pop()      # x2 is int, fully typed

# ── Protocol — structural subtyping ───────────────────────────
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...
    def resize(self, factor: float) -> None: ...

class Circle:   # does NOT inherit Drawable
    def draw(self) -> None:    print("drawing circle")
    def resize(self, f: float) -> None: print(f"resizing circle by {f}")

def render_all(shapes: list[Drawable]) -> None:
    for shape in shapes:
        shape.draw()

render_all([Circle()])  # ✅ Circle satisfies Drawable structurally
print(isinstance(Circle(), Drawable))  # True — runtime_checkable

# ── TypedDict — typed dictionary ──────────────────────────────
from typing import TypedDict

class UserDict(TypedDict):
    id:    int
    name:  str
    email: str
    role:  Literal["admin", "user"]

class PartialUserDict(TypedDict, total=False):  # all keys optional
    name: str
    email: str

user: UserDict = {"id": 1, "name": "Alice", "email": "alice@ex.com", "role": "admin"}
# user: UserDict = {"id": 1}   # mypy error: missing keys

# ── Final and ClassVar ─────────────────────────────────────────
from typing import Final, ClassVar

MAX_RETRIES: Final = 3          # constant — cannot be reassigned
# MAX_RETRIES = 5               # mypy error

class MyService:
    instance_count: ClassVar[int] = 0   # class variable, not instance variable
    MAX_CONN: Final[int] = 100          # per-class constant

# ── Annotated — attach metadata to types ──────────────────────
from typing import Annotated
import dataclasses

# Annotated[T, metadata...] — type is still T; metadata is for tools/validators
Positive = Annotated[float, "must be > 0"]
Email    = Annotated[str, "must be valid email format"]
Age      = Annotated[int, "0 <= age <= 150"]

# Pydantic/msgspec use Annotated for validation
from pydantic import Field
BoundedFloat = Annotated[float, Field(ge=0.0, le=1.0)]

# ── overload — multiple signatures for one function ───────────
from typing import overload

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
@overload
def process(x: list[int]) -> list[int]: ...

def process(x):   # actual implementation (no overload decorator)
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x.upper()
    elif isinstance(x, list):
        return [i * 2 for i in x]

# Type checker knows:
result_int: int       = process(5)        # ✅
result_str: str       = process("hello")  # ✅
# result_bad: int     = process("hello")  # mypy error

# ── TYPE_CHECKING — avoid circular imports ────────────────────
if TYPE_CHECKING:
    from mymodule import HeavyType   # only imported during type checking, not runtime

def func(x: "HeavyType") -> None: ...  # use string annotation if not imported
```

### 17.2 mypy and pyright Configuration

```python
# mypy.ini or pyproject.toml [tool.mypy]
"""
[mypy]
python_version = 3.12
strict = true          # enables all strict checks
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
no_implicit_reexport = true

# Per-module overrides
[mypy-third_party_lib.*]
ignore_missing_imports = true  # for libs without stubs
"""

# Type: ignore comments — suppress specific mypy errors
x: int = get_value()  # type: ignore[assignment]
y = legacy_function()  # type: ignore[no-any-return]
```

---

## Chapter 18: dataclasses, attrs & Pydantic

### 18.1 dataclasses — Auto-Generated Boilerplate

```python
from dataclasses import (
    dataclass, field, fields, asdict, astuple,
    replace, InitVar, KW_ONLY, make_dataclass
)
from typing import ClassVar

@dataclass
class Point:
    x: float
    y: float

# Auto-generated:
# __init__(self, x: float, y: float)
# __repr__(self) → "Point(x=1.0, y=2.0)"
# __eq__(self, other) → compares all fields

p = Point(1.0, 2.0)
print(p)          # Point(x=1.0, y=2.0)
print(p == Point(1.0, 2.0))  # True


@dataclass(order=True, frozen=True)   # frozen=immutable, order=comparison operators
class Version:
    major: int
    minor: int
    patch: int = 0

    def __str__(self): return f"{self.major}.{self.minor}.{self.patch}"


v1 = Version(1, 0)
v2 = Version(2, 3, 1)
print(v1 < v2)    # True — order=True generates __lt__, __le__, __gt__, __ge__
# v1.major = 2    # FrozenInstanceError — frozen=True
print(hash(v1))   # hashable because frozen=True


@dataclass
class User:
    # ── Field customization ───────────────────────────────────
    id:    int
    name:  str
    email: str

    # field() for customization:
    tags:     list[str]  = field(default_factory=list)   # mutable default!
    metadata: dict       = field(default_factory=dict)
    score:    float      = field(default=0.0, compare=False)  # exclude from __eq__
    _secret:  str        = field(default="", repr=False, compare=False)   # hide in repr

    # ClassVar: not a field — shared across instances
    count:    ClassVar[int] = 0

    # InitVar: passed to __init__ and __post_init__ but not stored
    raw_data: InitVar[str | None] = None

    def __post_init__(self, raw_data: str | None) -> None:
        """Called after __init__. Process/validate fields."""
        User.count += 1
        if self.score < 0 or self.score > 100:
            raise ValueError(f"Score must be 0-100, got {self.score}")
        if raw_data:
            # process raw_data here, it's not stored as an attribute
            parsed = json.loads(raw_data)
            self.metadata.update(parsed)

    # KW_ONLY (Python 3.10+): all following fields are keyword-only
    # @dataclass
    # class Config:
    #     host: str
    #     _: KW_ONLY
    #     port: int = 8080     # keyword-only
    #     debug: bool = False   # keyword-only


# Utility functions
u = User(id=1, name="Alice", email="alice@ex.com", score=95.0)
print(asdict(u))     # converts to dict (deep — nested dataclasses too)
print(astuple(u))    # converts to tuple
u2 = replace(u, name="Alice Smith", score=98.0)  # immutable update (like copy with changes)

for f in fields(User):
    print(f.name, f.type, f.default)


# Inheritance
@dataclass
class AdminUser(User):
    permissions: list[str] = field(default_factory=list)
    # __init__ automatically includes all parent fields first, then child fields
```

### 18.2 Pydantic — Runtime Validation

```python
# Pydantic v2 (the current version)
from pydantic import (
    BaseModel, Field, field_validator, model_validator,
    computed_field, ConfigDict, ValidationError,
    EmailStr, HttpUrl, AnyUrl, SecretStr
)
from typing import Annotated
from datetime import datetime

class Address(BaseModel):
    street: str
    city:   str
    zip:    str
    country: str = "US"


class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,      # strip whitespace from strings
        validate_assignment=True,        # validate on attribute assignment too
        use_enum_values=True,
        from_attributes=True,            # allow creating from ORM objects (SQLAlchemy)
        populate_by_name=True,           # allow both alias and field name
    )

    id:         int
    name:       Annotated[str, Field(min_length=1, max_length=100)]
    email:      EmailStr
    password:   SecretStr                # hidden in repr/json
    score:      Annotated[float, Field(ge=0.0, le=100.0)] = 0.0
    tags:       list[str] = []
    address:    Address | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    role:       Literal["admin", "user", "guest"] = "user"

    # ── Field-level validator ─────────────────────────────────
    @field_validator("name")
    @classmethod
    def name_must_be_ascii(cls, v: str) -> str:
        if not v.isascii():
            raise ValueError("Name must contain only ASCII characters")
        return v.title()   # normalize to Title Case

    @field_validator("tags", mode="before")  # mode="before": run before type coercion
    @classmethod
    def tags_lowercase(cls, v) -> list:
        if isinstance(v, str):
            v = v.split(",")    # accept comma-separated string
        return [tag.strip().lower() for tag in v]

    # ── Model-level validator (access multiple fields) ─────────
    @model_validator(mode="after")   # mode="after": all fields already validated
    def check_admin_has_high_score(self) -> "User":
        if self.role == "admin" and self.score < 80:
            raise ValueError("Admin users must have score >= 80")
        return self

    # ── Computed field (not stored, computed from other fields) ──
    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name} <{self.email}>"


# Creation with validation
try:
    user = User(
        id=1, name="  alice  ", email="alice@example.com",
        password="secret123", score=95.0, role="admin",
        tags="python, web, ai"
    )
    print(user.name)          # "Alice" — stripped and title-cased
    print(user.display_name)  # "Alice <alice@example.com>"
    print(user.model_dump())  # dict (password hidden)
    print(user.model_dump_json(indent=2))  # JSON string

    # From dict / JSON
    user2 = User.model_validate({"id": 2, "name": "Bob", "email": "bob@ex.com", "password": "pw"})
    user3 = User.model_validate_json('{"id": 3, "name": "Carol", "email": "carol@ex.com", "password": "pw"}')

except ValidationError as e:
    print(e.json())      # detailed JSON error report
    for err in e.errors():
        print(err["loc"], err["msg"], err["type"])


# JSON Schema generation (for API docs, frontend validation)
schema = User.model_json_schema()
print(schema)   # full JSON Schema dict
```

---

## Chapter 19: Context Managers

### 19.1 contextlib — The Full Toolkit

```python
from contextlib import (
    contextmanager, asynccontextmanager,
    contextmanager, suppress, redirect_stdout, redirect_stderr,
    ExitStack, AsyncExitStack,
    contextmanager, closing, nullcontext, AbstractContextManager
)
import io

# ── @contextmanager — generator-based context manager ─────────
# Most ergonomic way to create context managers without a full class

@contextmanager
def managed_resource(name: str):
    """Acquire, yield, always release — with full exception handling."""
    resource = acquire_resource(name)
    try:
        yield resource       # code inside 'with' block executes here
    except ValueError as e:
        print(f"Handled ValueError: {e}")
        # don't re-raise → exception suppressed
    except Exception:
        print("Unexpected error, releasing resource")
        raise               # re-raise — exception propagates
    finally:
        resource.release()   # ALWAYS runs, even on exception or return

with managed_resource("db") as r:
    r.do_work()


# Real-world example: temporary directory
import tempfile, shutil, os

@contextmanager
def temp_directory():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

with temp_directory() as d:
    path = os.path.join(d, "output.txt")
    with open(path, "w") as f:
        f.write("data")
    # process files...
# tmpdir automatically deleted


# ── suppress — context manager to swallow exceptions ──────────
with suppress(FileNotFoundError, PermissionError):
    os.remove("/tmp/maybe_missing.txt")   # silently ignored if not found
# equivalent to:
# try:
#     os.remove(...)
# except (FileNotFoundError, PermissionError):
#     pass


# ── redirect_stdout / redirect_stderr — capture output ─────────
output_buffer = io.StringIO()
with redirect_stdout(output_buffer):
    print("This goes to buffer, not console")
    print("So does this")

captured = output_buffer.getvalue()   # "This goes to buffer...\nSo does this\n"


# ── ExitStack — dynamic set of context managers ───────────────
# When you don't know at compile time how many context managers you need

def open_files(paths: list[str]):
    """Open an arbitrary number of files, close all even if one fails."""
    with ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        # ExitStack closes all files when the with block exits
        return process_files(files)   # ← files are valid here

# Another pattern: conditional context managers
with ExitStack() as stack:
    if use_transaction:
        stack.enter_context(db.transaction())
    if use_lock:
        stack.enter_context(lock)
    do_work()

# Register cleanup callbacks
with ExitStack() as stack:
    conn = create_connection()
    stack.callback(conn.close)   # called on exit, like defer in Go
    stack.callback(log_exit)     # callbacks run in LIFO order


# ── nullcontext — no-op context manager (Python 3.7+) ─────────
def process(data, *, lock=None):
    # Use real lock if provided, no-op if None
    with (lock if lock is not None else nullcontext()):
        do_work(data)


# ── @asynccontextmanager — async version ──────────────────────
@asynccontextmanager
async def async_managed_resource(url: str):
    session = await create_async_session(url)
    try:
        yield session
    finally:
        await session.close()

async def main():
    async with async_managed_resource("https://api.example.com") as session:
        result = await session.get("/users")
```

---

## Chapter 20: Async/Await & asyncio

### 20.1 Concurrency Model — asyncio vs Threading vs Multiprocessing

```python
"""
Python has three concurrency models:

1. asyncio (cooperative multitasking):
   ✅ Best for: I/O-bound tasks (HTTP, DB, files, sockets)
   ✅ Single thread — no GIL issues
   ✅ Lightweight: millions of coroutines possible
   ❌ Single-threaded: one CPU core; doesn't parallelize CPU work
   ❌ Cooperative: a blocking call blocks the ENTIRE event loop
   How: coroutines yield control with 'await'; event loop runs the ready ones

2. threading:
   ✅ Good for: I/O-bound tasks with blocking libraries, GUI, callbacks
   ✅ Preemptive: OS switches threads even without yield points
   ❌ GIL: only one thread executes Python bytecode at a time
   ❌ Thread overhead: ~8MB stack per thread; OS scheduling
   ❌ Race conditions need careful locking

3. multiprocessing:
   ✅ Best for: CPU-bound tasks (image processing, ML training, cryptography)
   ✅ Bypasses GIL: each process has its own Python interpreter
   ❌ Expensive: process creation ~100ms, separate memory space
   ❌ Communication overhead: must serialize data between processes

Rule of thumb:
  I/O bound + modern async library → asyncio
  I/O bound + blocking library     → threading
  CPU bound                        → multiprocessing
"""
```

### 20.2 Coroutines and the Event Loop

```python
import asyncio

# async def creates a coroutine function
# Calling it returns a coroutine object (doesn't execute yet!)
async def greet(name: str) -> str:
    """A coroutine: can be suspended with await."""
    print(f"Starting greeting {name}")
    await asyncio.sleep(1)   # yields control to event loop for 1 second
    print(f"Done greeting {name}")
    return f"Hello, {name}!"

# asyncio.run() — entry point: creates event loop, runs until coroutine completes
async def main():
    result = await greet("Alice")   # await suspends main, runs greet
    print(result)

asyncio.run(main())

# Coroutine object is created but NOT run until awaited:
coro = greet("Bob")      # <coroutine object greet at 0x...> — nothing runs yet
# asyncio.run(coro)      # now it runs

# Without await: forgot to await → coroutine never runs (Python warns)
# async def buggy():
#     greet("Alice")    # RuntimeWarning: coroutine 'greet' was never awaited
```

### 20.3 Tasks — Concurrent Execution

```python
import asyncio
import aiohttp   # pip install aiohttp — async HTTP client

# asyncio.create_task() — schedule coroutine to run concurrently
async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_sequential(urls: list[str]) -> list[dict]:
    """Fetch URLs one by one — SLOW: total = sum of all response times."""
    results = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            result = await fetch_url(session, url)  # waits for each one
            results.append(result)
    return results

async def fetch_all_concurrent(urls: list[str]) -> list[dict]:
    """Fetch URLs concurrently — FAST: total = max of all response times."""
    async with aiohttp.ClientSession() as session:
        # asyncio.gather: run all coroutines concurrently
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        # gather returns results in the SAME ORDER as tasks
    return list(results)

# asyncio.gather vs asyncio.TaskGroup vs asyncio.wait

# asyncio.gather — most common, returns results in order
async def example_gather():
    results = await asyncio.gather(
        coro1(), coro2(), coro3(),
        return_exceptions=True   # don't raise on first error; collect exceptions as results
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            print(f"Result: {r}")

# asyncio.TaskGroup (Python 3.11+) — structured concurrency
async def example_task_group():
    results = []
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(coro1())
        task2 = tg.create_task(coro2())
        task3 = tg.create_task(coro3())
    # All tasks done when block exits; if ANY fails, all are cancelled
    results = [task1.result(), task2.result(), task3.result()]

# asyncio.wait — more control over completion
async def example_wait():
    tasks = {asyncio.create_task(coro()) for coro in [coro1, coro2, coro3]}
    
    # FIRST_COMPLETED: process results as they come in
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            print(task.result())

# asyncio.wait_for — add timeout to any coroutine
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Operation timed out!")
```

### 20.4 Async Patterns

```python
# ── Async generators ──────────────────────────────────────────
async def paginate_api(url: str, page_size: int = 100):
    """Async generator: yields pages of results."""
    async with aiohttp.ClientSession() as session:
        cursor = None
        while True:
            params = {"limit": page_size}
            if cursor:
                params["cursor"] = cursor

            async with session.get(url, params=params) as resp:
                data = await resp.json()

            for item in data["items"]:
                yield item             # yield from async generator

            cursor = data.get("next_cursor")
            if not cursor:
                break

async def process_all():
    async for item in paginate_api("https://api.example.com/items"):
        await process_item(item)

# async comprehension
items = [item async for item in paginate_api("https://api.example.com/items")]
filtered = [x async for x in paginate_api(url) if x["active"]]


# ── Async context managers ────────────────────────────────────
class AsyncDatabase:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, *args):
        await self.conn.close()

async def use_db():
    async with AsyncDatabase() as conn:
        await conn.execute("SELECT 1")


# ── Producer/Consumer with asyncio.Queue ─────────────────────
async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0.1)   # simulate production time
    # Signal consumers to stop
    for _ in range(NUM_CONSUMERS):
        await queue.put(None)

async def consumer(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        if item is None:          # sentinel: time to stop
            queue.task_done()
            break
        print(f"Worker {worker_id} processing {item}")
        await asyncio.sleep(0.5)  # simulate processing time
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)   # bounded buffer
    NUM_CONSUMERS = 3

    producers = [asyncio.create_task(producer(queue, items))]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(NUM_CONSUMERS)]

    await asyncio.gather(*producers, *consumers)


# ── Semaphore — limit concurrency ─────────────────────────────
async def limited_concurrent_fetch(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)  # at most 10 concurrent requests

    async def fetch_with_limit(session, url):
        async with semaphore:   # blocks if 10 already running
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[fetch_with_limit(session, url) for url in urls]
        )


# ── asyncio.Lock, Event, Condition ───────────────────────────
lock = asyncio.Lock()
event = asyncio.Event()
condition = asyncio.Condition()

async def update_shared_resource():
    async with lock:
        shared_data.append("new item")

async def wait_for_event():
    await event.wait()           # suspends until event.set() is called
    print("Event occurred!")

async def signal_event():
    await asyncio.sleep(2)
    event.set()                  # wakes all waiters

# ── Running sync code in executor (don't block event loop!) ───
import concurrent.futures

async def call_blocking_function():
    loop = asyncio.get_event_loop()

    # Run CPU-bound or blocking I/O in thread pool
    result = await loop.run_in_executor(
        None,                     # None = default ThreadPoolExecutor
        blocking_function,        # the function to call
        arg1, arg2                # arguments
    )

    # CPU-bound: use ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, cpu_heavy_function, data)
```

### 20.5 Error Handling in Async Code

```python
import asyncio
import traceback

async def risky() -> str:
    await asyncio.sleep(0.1)
    raise ValueError("something went wrong")

# ── Handle exceptions from gather ────────────────────────────
async def handle_gather_errors():
    results = await asyncio.gather(
        risky(), risky(), successful_coro(),
        return_exceptions=True
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")

# ── Handle exceptions from tasks ─────────────────────────────
async def handle_task_errors():
    task = asyncio.create_task(risky())
    task.add_done_callback(
        lambda t: print(f"Task failed: {t.exception()}") if t.exception() else None
    )
    try:
        await task
    except ValueError as e:
        print(f"Caught: {e}")

# ── Global exception handler for unhandled task exceptions ─────
def handle_exception(loop, context):
    exception = context.get("exception")
    if exception:
        traceback.print_exception(type(exception), exception, exception.__traceback__)
    else:
        print(f"Caught exception: {context['message']}")

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
```
# Python Mastery Guide — Part 3
# Chapters 21–30: Standard Library, Testing, Concurrency, Performance, Production

---

## Chapter 21: File I/O, os & pathlib

### 21.1 File Operations

```python
import os
from pathlib import Path

# ── Opening files ─────────────────────────────────────────────
# open(file, mode, encoding, errors, buffering, newline)
# Modes:
#   'r'  read text (default)
#   'w'  write text (creates/truncates)
#   'a'  append text
#   'x'  exclusive create (fails if exists)
#   'b'  binary (combine: 'rb', 'wb')
#   '+'  read+write ('r+', 'w+')

# ALWAYS use context manager — guarantees file.close()
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()              # read entire file as string

# Read line by line — memory efficient for large files
with open("large.txt", "r", encoding="utf-8") as f:
    for line in f:                  # f is a lazy iterator over lines
        process(line.rstrip("\n"))  # strip newline

# Read all lines into list
with open("data.txt") as f:
    lines = f.readlines()           # list of strings including \n
    lines = [l.rstrip() for l in f.readlines()]  # stripped

# Read chunks — for very large files
with open("huge.bin", "rb") as f:
    while chunk := f.read(65536):   # walrus operator: 64KB chunks
        process(chunk)

# Write
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("line 1\n")
    f.write("line 2\n")
    print("line 3", file=f)         # print() accepts file= argument

# Append
with open("log.txt", "a", encoding="utf-8") as f:
    f.write(f"[{datetime.now()}] Event occurred\n")

# Read and write simultaneously
with open("data.txt", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0)                       # seek to beginning
    f.write(content.upper())
    f.truncate()                    # remove any remaining old content

# Binary files
with open("image.png", "rb") as f:
    header = f.read(8)              # read first 8 bytes (PNG signature)
    f.seek(0, 2)                    # seek to end (whence=2)
    size = f.tell()                 # file size in bytes

with open("output.bin", "wb") as f:
    import struct
    f.write(struct.pack(">IHH", 1234567, 100, 200))  # big-endian uint32, uint16, uint16


# ── File object methods ───────────────────────────────────────
f.read(n)        # read n bytes/chars (all if n omitted)
f.readline()     # read one line including \n
f.readlines()    # list of all lines
f.write(s)       # write string/bytes
f.writelines(ls) # write sequence (no \n added)
f.tell()         # current position
f.seek(pos)      # seek to absolute position
f.seek(n, 0)     # seek from start (whence=0)
f.seek(n, 1)     # seek relative to current (whence=1)
f.seek(0, 2)     # seek to end (whence=2)
f.flush()        # flush write buffer to OS
f.truncate(n)    # truncate to n bytes (or current position if n omitted)
f.fileno()       # file descriptor number
f.isatty()       # True if connected to terminal
f.closed         # True after close()
f.name           # filename
f.mode           # open mode string
f.encoding       # text encoding


# ── io module — in-memory files ───────────────────────────────
import io

# StringIO — in-memory text file
buf = io.StringIO()
buf.write("hello ")
print("world", file=buf)
buf.getvalue()          # "hello world\n"
buf.seek(0)
buf.read()              # "hello world\n"

# BytesIO — in-memory binary file
img_buf = io.BytesIO()
img_buf.write(b"\x89PNG\r\n\x1a\n")
img_buf.seek(0)
header = img_buf.read(4)    # b'\x89PNG'
```

### 21.2 pathlib — Modern Path Handling

```python
from pathlib import Path

# Creating paths — use / to join
p = Path("/home/user/documents/report.txt")
p = Path.home() / "documents" / "report.txt"   # ~ expanded automatically
p = Path("relative/path/to/file.py")
p = Path(".")                                   # current directory

# ── Path properties ───────────────────────────────────────────
p = Path("/home/alice/projects/myapp/src/main.py")
p.name          # "main.py"
p.stem          # "main"
p.suffix        # ".py"
p.suffixes      # [".py"] (multiple: [".tar", ".gz"])
p.parent        # Path("/home/alice/projects/myapp/src")
p.parents       # [src/, myapp/, projects/, alice/, home/, /]
p.parts         # ('/', 'home', 'alice', 'projects', 'myapp', 'src', 'main.py')
p.root          # "/"
p.anchor        # "/"
p.drive         # "" (Unix) or "C:" (Windows)
p.is_absolute() # True

# ── Path operations ───────────────────────────────────────────
p / "subdir" / "file.txt"              # join with /
p.with_name("other.py")               # same dir, different name
p.with_stem("renamed")                # same dir, different stem
p.with_suffix(".txt")                 # change extension
p.relative_to("/home/alice")          # Path("projects/myapp/src/main.py")
p.resolve()                           # absolute path with symlinks resolved
str(p)                                # convert to string

# ── Querying filesystem ───────────────────────────────────────
p.exists()          # True if path exists (file or dir)
p.is_file()         # True if regular file
p.is_dir()          # True if directory
p.is_symlink()      # True if symbolic link
p.is_mount()        # True if mount point
p.stat()            # os.stat_result (size, mtime, permissions...)
p.stat().st_size    # file size in bytes
p.stat().st_mtime   # last modification time (Unix timestamp)
p.lstat()           # stat without following symlinks

# ── Reading and writing ───────────────────────────────────────
text = p.read_text(encoding="utf-8")          # entire file as string
raw  = p.read_bytes()                          # entire file as bytes
p.write_text("content\n", encoding="utf-8")   # write string (overwrites)
p.write_bytes(b"\x00\x01\x02")               # write bytes

# ── Directory operations ──────────────────────────────────────
d = Path("mydir")
d.mkdir(exist_ok=True)                  # create directory
d.mkdir(parents=True, exist_ok=True)    # create parents too
d.rmdir()                               # remove empty directory

# List directory contents
for item in d.iterdir():               # direct children
    print(item.name, item.is_dir())

# Glob — pattern matching
for py_file in d.glob("*.py"):         # non-recursive
    print(py_file)

for py_file in d.rglob("*.py"):        # recursive (all descendants)
    print(py_file)

for test in d.glob("test_*.py"):       # prefix pattern
    print(test)

# Sort, filter
py_files = sorted(d.rglob("*.py"), key=lambda p: p.stat().st_mtime)  # by mtime

# ── File operations ───────────────────────────────────────────
import shutil

p.rename(p.with_name("renamed.py"))    # rename/move (same filesystem)
p.replace(dest)                        # rename, overwrite if dest exists
shutil.move(str(src), str(dst))        # cross-filesystem move
shutil.copy2(str(src), str(dst))       # copy with metadata
shutil.copytree(str(src_dir), str(dst_dir))  # copy entire directory tree
p.unlink(missing_ok=True)             # delete file (Python 3.8+)
shutil.rmtree(str(d))                 # delete directory tree

# ── Temporary files and directories ──────────────────────────
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    tmp = Path(tmpdir)
    (tmp / "work.txt").write_text("temp data")
    process(tmp)
# tmpdir deleted automatically

with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
    json.dump(data, f)
    tmp_path = Path(f.name)
# file persists after close (delete=False); delete manually when done
```

### 21.3 os Module

```python
import os

# Environment variables
os.environ["MY_VAR"] = "value"         # set
os.environ.get("MY_VAR", "default")   # get with default
os.getenv("MY_VAR", "default")        # same
del os.environ["MY_VAR"]              # delete
dict(os.environ)                       # all env vars as dict

# Process information
os.getpid()          # current process ID
os.getppid()         # parent process ID
os.getcwd()          # current working directory as string
os.chdir("/tmp")     # change working directory
os.listdir(".")      # list directory (strings)
os.getlogin()        # current user's login name

# File system operations (use pathlib when possible)
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("dir/")
os.path.join("dir", "sub", "file.txt")  # → "dir/sub/file.txt"
os.path.abspath("relative/path")
os.path.dirname("/home/user/file.txt")  # → "/home/user"
os.path.basename("/home/user/file.txt") # → "file.txt"
os.path.splitext("file.tar.gz")         # → ("file.tar", ".gz")
os.path.expanduser("~/.bashrc")         # → "/home/user/.bashrc"
os.path.expandvars("$HOME/.bashrc")     # → "/home/user/.bashrc"
os.path.getsize("file.txt")
os.path.getmtime("file.txt")            # modification time

# Walk directory tree
for dirpath, dirnames, filenames in os.walk("/home/user"):
    print(f"In {dirpath}:")
    for f in filenames:
        print(f"  {f}")
    # Modify dirnames in-place to control recursion:
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]  # skip hidden

# Symbolic links
os.symlink("target.txt", "link.txt")
os.readlink("link.txt")                 # "target.txt"

# File permissions
os.chmod("script.py", 0o755)           # rwxr-xr-x
os.stat("file.txt").st_mode            # mode bits
import stat
stat.S_IRWXU  # owner read, write, execute

# Running system commands — prefer subprocess
os.system("ls -la")                    # runs in shell, returns exit code
# Better:
import subprocess
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
print(result.returncode)
```

---

## Chapter 22: Error Handling — Exceptions Deep Dive

### 22.1 Exception Hierarchy

```python
# Python's built-in exception hierarchy:
# BaseException
#   ├── SystemExit           — sys.exit()
#   ├── KeyboardInterrupt    — Ctrl+C
#   ├── GeneratorExit        — generator.close()
#   └── Exception            — all regular exceptions
#         ├── ArithmeticError
#         │     ├── ZeroDivisionError
#         │     ├── OverflowError
#         │     └── FloatingPointError
#         ├── LookupError
#         │     ├── IndexError
#         │     └── KeyError
#         ├── AttributeError
#         ├── NameError        ← UnboundLocalError
#         ├── TypeError
#         ├── ValueError       ← UnicodeError
#         ├── RuntimeError     ← NotImplementedError, RecursionError
#         ├── OSError          ← FileNotFoundError, PermissionError,
#         │                      IsADirectoryError, TimeoutError, etc.
#         ├── StopIteration
#         ├── StopAsyncIteration
#         ├── ImportError      ← ModuleNotFoundError
#         ├── SyntaxError      ← IndentationError, TabError
#         ├── MemoryError
#         ├── BufferError
#         ├── EOFError
#         ├── ConnectionError  ← BrokenPipeError, ConnectionRefusedError, etc.
#         └── Warning          ← DeprecationWarning, UserWarning, etc.

# ALWAYS catch specific exceptions — never bare except:
try:
    result = risky_operation()
except ValueError as e:
    handle_value_error(e)
except (TypeError, AttributeError) as e:
    handle_type_issue(e)
except OSError as e:
    if e.errno == errno.ENOENT:
        handle_file_not_found()
    else:
        raise   # re-raise unhandled OS errors
except Exception as e:
    # last resort — catch anything derived from Exception
    logger.exception("Unexpected error")   # logs with traceback
    raise
# except:        # ← NEVER DO THIS — catches SystemExit, KeyboardInterrupt!
# except BaseException:  # ← Only if you specifically want to catch those
```

### 22.2 try / except / else / finally — Full Semantics

```python
try:
    result = int("42")
except ValueError as e:
    # Runs IF ValueError raised
    print(f"Cannot convert: {e}")
    result = 0
else:
    # Runs ONLY IF no exception was raised
    # (distinct from code after try/except — runs before finally)
    print(f"Successfully converted: {result}")
finally:
    # ALWAYS runs: after try (success), after except (handled error), even after return/break/continue
    print("Cleanup — always runs")

# Exception chaining
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Config file not found: {path}") from e
        # 'from e': chains exceptions — shows both in traceback
        # 'from None': suppresses the original exception in traceback

# Exception groups (Python 3.11+) — ExceptionGroup
try:
    raise ExceptionGroup("multiple errors", [
        ValueError("bad value"),
        TypeError("wrong type"),
        RuntimeError("runtime issue"),
    ])
except* ValueError as eg:         # except* handles exception groups
    print(f"Value errors: {eg.exceptions}")
except* (TypeError, RuntimeError) as eg:
    print(f"Other errors: {eg.exceptions}")

# Exception notes (Python 3.11+)
try:
    int("abc")
except ValueError as e:
    e.add_note("Attempted to parse user input")
    e.add_note(f"Input was: 'abc'")
    raise   # traceback will include the notes
```

### 22.3 Custom Exceptions

```python
# Custom exception hierarchy for your application
class AppError(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str = "UNKNOWN", **context):
        super().__init__(message)
        self.message = message
        self.code    = code
        self.context = context

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r}, code={self.code!r})"

    def to_dict(self) -> dict:
        return {"error": self.code, "message": self.message, **self.context}


class ValidationError(AppError):
    def __init__(self, field: str, message: str, value=None):
        super().__init__(
            message=f"Validation failed for '{field}': {message}",
            code="VALIDATION_ERROR",
            field=field,
            value=str(value) if value is not None else None,
        )
        self.field = field
        self.value = value


class NotFoundError(AppError):
    def __init__(self, resource: str, id):
        super().__init__(
            message=f"{resource} with id {id!r} not found",
            code="NOT_FOUND",
            resource=resource,
            id=str(id),
        )


class AuthError(AppError):
    def __init__(self, reason: str = "Unauthorized"):
        super().__init__(reason, code="UNAUTHORIZED")


class RateLimitError(AppError):
    def __init__(self, limit: int, window_seconds: int):
        super().__init__(
            f"Rate limit {limit} requests per {window_seconds}s exceeded",
            code="RATE_LIMITED",
            limit=limit,
            window_seconds=window_seconds,
        )


# Usage
def get_user(user_id: int) -> dict:
    user = db.find(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user

def create_user(data: dict) -> dict:
    if not data.get("email"):
        raise ValidationError("email", "Email is required")
    if "@" not in data["email"]:
        raise ValidationError("email", "Invalid email format", data["email"])
    return db.create(data)

try:
    user = get_user(999)
except NotFoundError as e:
    response = {"status": 404, **e.to_dict()}
except ValidationError as e:
    response = {"status": 400, **e.to_dict()}
except AppError as e:
    response = {"status": 500, **e.to_dict()}
```

---

## Chapter 23: Modules, Packages & Imports

### 23.1 Import System

```python
# Basic imports
import os                          # import module; access via os.path.join(...)
import os.path                     # import submodule
from os import path, getcwd        # import specific names
from os.path import join, exists   # from submodule
import os as operating_system      # alias
from os.path import join as pjoin  # alias for specific name
from typing import *               # star import (avoid — pollutes namespace)

# Import search path (in order):
# 1. sys.modules cache (already imported modules)
# 2. Built-in modules (math, sys, os, etc.)
# 3. Frozen modules (compiled into interpreter)
# 4. Import path: sys.path list
#    sys.path[0] = directory of running script (or '')
#    PYTHONPATH environment variable entries
#    Installation-dependent defaults (site-packages)

import sys
print(sys.path)                    # current import search path
sys.path.insert(0, "/my/custom/path")  # add to search path at runtime

# Relative imports (only inside packages)
# from . import sibling_module      # import from same package
# from .. import parent_module      # import from parent package
# from .sibling import some_function


# ── Module attributes ─────────────────────────────────────────
import mymodule
mymodule.__name__        # "mymodule"
mymodule.__file__        # "/path/to/mymodule.py"
mymodule.__doc__         # module docstring
mymodule.__dict__        # module's namespace dict
mymodule.__package__     # package name (if part of a package)
mymodule.__spec__        # ModuleSpec with import details


# ── if __name__ == "__main__" ─────────────────────────────────
# __name__ == "__main__" when file is run directly
# __name__ == "module_name" when file is imported
# Used to: run tests, demos, CLI when run directly; be importable as library

def main():
    print("Running as script")

if __name__ == "__main__":
    main()


# ── importlib — dynamic imports ───────────────────────────────
import importlib

module = importlib.import_module("os.path")      # equivalent to: import os.path
klass  = getattr(importlib.import_module("mypackage.models"), "User")

# Reload a module (picks up changes without restarting Python)
importlib.reload(mymodule)

# Lazy import — defer expensive import until first use
from importlib import import_module
_numpy = None

def get_numpy():
    global _numpy
    if _numpy is None:
        _numpy = import_module("numpy")
    return _numpy
```

### 23.2 Package Structure

```
mypackage/
├── __init__.py          ← makes the directory a package
├── __main__.py          ← python -m mypackage runs this
├── module_a.py
├── module_b.py
├── subpackage/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── test_a.py
    └── test_b.py
```

```python
# __init__.py — package initialization and public API
# mypackage/__init__.py
"""
MyPackage: A useful library.

Public API:
    - Client: main interface class
    - Config: configuration class
    - Error: base exception
"""

from .module_a import Client          # re-export for convenience
from .module_b import Config, Error   # users can do: from mypackage import Client
from .subpackage.core import process  # expose subpackage functionality

# __all__ — defines what 'from mypackage import *' exports
__all__ = ["Client", "Config", "Error", "process"]

# Version
__version__ = "2.1.0"
__author__  = "Alice Smith"
```

---

## Chapter 24: Testing — unittest, pytest & Mocking

### 24.1 pytest — The Standard

```python
# pip install pytest pytest-cov pytest-asyncio pytest-mock

# test_calculator.py
import pytest
from myapp.calculator import Calculator, DivisionByZeroError

# ── Basic test functions ───────────────────────────────────────
def test_addition():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_subtraction():
    assert Calculator().subtract(10, 3) == 7

def test_division_normal():
    result = Calculator().divide(10, 2)
    assert result == 5.0
    assert isinstance(result, float)

# ── Testing exceptions ────────────────────────────────────────
def test_division_by_zero():
    with pytest.raises(DivisionByZeroError) as exc_info:
        Calculator().divide(10, 0)
    assert "Cannot divide by zero" in str(exc_info.value)
    assert exc_info.value.dividend == 10

def test_division_by_zero_match():
    with pytest.raises(DivisionByZeroError, match="Cannot divide by zero"):
        Calculator().divide(10, 0)

# ── Parametrize — test multiple inputs ───────────────────────
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (1.5, 2.5, 4.0),
])
def test_add_parametrized(a, b, expected):
    assert Calculator().add(a, b) == expected

# Parametrize with pytest.param (for custom ids and marks)
@pytest.mark.parametrize("x, expected", [
    pytest.param(4, 2.0, id="perfect-square"),
    pytest.param(2, 1.4142, id="irrational", marks=pytest.mark.approx),
    pytest.param(-1, None, id="negative", marks=pytest.mark.xfail),
])
def test_sqrt(x, expected):
    import math
    assert math.sqrt(x) == pytest.approx(expected, abs=0.001)

# ── Fixtures ──────────────────────────────────────────────────
@pytest.fixture
def calculator():
    """Provide a fresh Calculator instance."""
    return Calculator()

@pytest.fixture
def calculator_with_history():
    """Calculator pre-loaded with history."""
    calc = Calculator()
    calc.add(1, 2)
    calc.add(3, 4)
    return calc

def test_with_fixture(calculator):
    assert calculator.add(5, 5) == 10

def test_with_history(calculator_with_history):
    assert len(calculator_with_history.history) == 2


# ── Fixture scope and setup/teardown ──────────────────────────
@pytest.fixture(scope="module")   # created once per test module
def database_connection():
    conn = create_test_database()
    yield conn          # yield = setup done; code after yield = teardown
    conn.close()
    drop_test_database()

@pytest.fixture(scope="session")  # created once per entire test session
def redis_client():
    client = redis.Redis(host="localhost", port=6379, db=15)  # test DB
    yield client
    client.flushdb()

@pytest.fixture(autouse=True)   # applied to ALL tests in scope automatically
def reset_config():
    original = config.copy()
    yield
    config.update(original)     # restore config after each test


# ── Marks — categorize and control tests ──────────────────────
@pytest.mark.slow
def test_performance():
    result = run_heavy_computation()
    assert result == expected

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass

@pytest.mark.xfail(reason="Known bug #123", strict=True)
def test_known_failure():
    assert 1 == 2   # expected to fail; strict=True means failure if it passes

# Run: pytest -m "not slow"        → skip slow tests
# Run: pytest -m "unit and not db" → only unit tests, no DB tests

# conftest.py — shared fixtures across test files
# pytest.ini or pyproject.toml [tool.pytest.ini_options]
```

### 24.2 Mocking

```python
from unittest.mock import (
    Mock, MagicMock, AsyncMock, patch, patch_object,
    call, sentinel, ANY, PropertyMock, create_autospec
)
import pytest

# ── Mock basics ───────────────────────────────────────────────
m = Mock()
m.method("arg1", kwarg="val")
m.attribute = "value"

# Verify calls
m.method.assert_called_once_with("arg1", kwarg="val")
m.method.assert_called_with("arg1", kwarg="val")   # most recent call
m.method.assert_called()                            # any call
m.method.call_count                                 # number of calls
m.method.call_args_list                             # list of all calls
m.method.call_args                                  # most recent call args

# Configure return values
m.method.return_value = 42
m.method("any", "args")   # → 42

m.method.side_effect = [1, 2, 3]          # return different values per call
m.method.side_effect = ValueError("oops")  # always raise exception
m.method.side_effect = lambda x: x * 2    # call this function instead

# MagicMock — Mock with magic methods already set up
mm = MagicMock()
mm.__len__.return_value = 5
len(mm)   # → 5
mm.__getitem__.return_value = "item"
mm[0]     # → "item"


# ── patch — replace objects during test ──────────────────────
# patch as decorator
@patch("myapp.services.requests.get")
def test_api_call(mock_get, calculator):
    mock_get.return_value.json.return_value = {"status": "ok"}
    mock_get.return_value.status_code = 200
    result = myapp.services.fetch_data("https://api.example.com")
    mock_get.assert_called_once_with("https://api.example.com", timeout=30)
    assert result == {"status": "ok"}

# patch as context manager
def test_with_patch():
    with patch("myapp.services.send_email") as mock_email:
        mock_email.return_value = True
        result = register_user("alice@example.com", "password")
        mock_email.assert_called_once()
        assert result.success

# patch object — patch attribute of a specific object
def test_patch_object(calculator):
    with patch.object(calculator, "add", return_value=999) as mock_add:
        result = calculator.add(1, 2)
        assert result == 999
        mock_add.assert_called_once_with(1, 2)

# patch dict — temporarily modify a dict
with patch.dict(os.environ, {"API_KEY": "test_key", "DEBUG": "true"}):
    assert os.environ["API_KEY"] == "test_key"

# create_autospec — mock that enforces the real interface
class UserService:
    def get_user(self, user_id: int) -> dict: ...
    def create_user(self, name: str, email: str) -> dict: ...

mock_service = create_autospec(UserService, instance=True)
mock_service.get_user(1)           # ✅ valid call
# mock_service.get_user("not-int") # TypeError — spec enforced
# mock_service.nonexistent()       # AttributeError — spec enforced


# ── AsyncMock — for async functions ──────────────────────────
@pytest.mark.asyncio
async def test_async_function():
    with patch("myapp.db.fetch_user", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"id": 1, "name": "Alice"}
        result = await myapp.service.get_user_profile(1)
        mock_fetch.assert_awaited_once_with(1)
        assert result["name"] == "Alice"


# ── pytest-mock integration ───────────────────────────────────
def test_with_mocker(mocker):
    """mocker fixture: cleaner syntax, auto-cleanup"""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"ok": True}
    
    spy = mocker.spy(calculator, "add")   # spy: real method called + tracked
    calculator.add(1, 2)
    spy.assert_called_once_with(1, 2)


# ── Testing with real databases (integration tests) ───────────
@pytest.fixture
def db_session():
    """Create a test database session with rollback."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_user_repository(db_session):
    repo = UserRepository(db_session)
    user = repo.create(name="Alice", email="alice@test.com")
    assert user.id is not None
    found = repo.get_by_id(user.id)
    assert found.name == "Alice"
```

### 24.3 Coverage and Test Organization

```bash
# Run tests
pytest                                 # all tests
pytest tests/unit/                     # specific directory
pytest tests/unit/test_user.py        # specific file
pytest tests/unit/test_user.py::test_creation  # specific test
pytest -v                              # verbose
pytest -x                             # stop on first failure
pytest -k "add or subtract"           # run tests matching expression
pytest --lf                           # rerun last failed
pytest -n 4                           # parallel (pip install pytest-xdist)

# Coverage
pytest --cov=myapp --cov-report=term-missing --cov-report=html
# --cov-fail-under=80  → fail if coverage < 80%

# Configuration in pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
markers = [
    "slow: marks tests as slow",
    "unit: unit tests (no I/O)",
    "integration: integration tests",
    "e2e: end-to-end tests",
]
addopts = "-v --strict-markers"
asyncio_mode = "auto"   # for pytest-asyncio

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]
```

---

## Chapter 25: Concurrency — threading, multiprocessing, concurrent.futures

### 25.1 threading

```python
import threading
import time
from typing import Any

# ── Thread creation ───────────────────────────────────────────
def worker(name: str, n: int) -> None:
    for i in range(n):
        print(f"{name}: {i}")
        time.sleep(0.1)

# Create and start thread
t = threading.Thread(target=worker, args=("T1", 5), kwargs={}, daemon=True)
t.start()       # start thread (non-blocking)
t.join()        # wait for thread to finish
t.join(timeout=5.0)  # wait max 5 seconds
t.is_alive()    # True if thread is still running

# daemon=True: thread is killed when main thread exits
# daemon=False (default): program waits for thread to finish before exit

# Thread subclass (alternative pattern)
class WorkerThread(threading.Thread):
    def __init__(self, items: list):
        super().__init__(daemon=True)
        self.items  = items
        self.result = None

    def run(self) -> None:
        self.result = sum(self.items)

t = WorkerThread([1, 2, 3, 4, 5])
t.start()
t.join()
print(t.result)   # 15

# Thread-local storage — each thread has its own copy
local = threading.local()
local.user_id = 42   # only visible to current thread

def process_request(user_id: int):
    local.user_id = user_id
    do_work()   # can access local.user_id from anywhere in this thread


# ── Synchronization primitives ────────────────────────────────
lock = threading.Lock()

# Mutex lock
with lock:               # acquire in __enter__, release in __exit__
    shared_list.append(item)   # protected critical section

if lock.acquire(blocking=True, timeout=5.0):
    try:
        do_work()
    finally:
        lock.release()   # ALWAYS release in finally

# RLock — reentrant lock: same thread can acquire multiple times
rlock = threading.RLock()
with rlock:
    with rlock:    # would deadlock with regular Lock; fine with RLock
        do_work()

# Condition — wait for a condition to be True
condition = threading.Condition(lock=None)   # has internal lock

def consumer():
    with condition:
        while queue.empty():
            condition.wait()    # releases lock, waits for notify, re-acquires
        item = queue.get()

def producer():
    with condition:
        queue.put(item)
        condition.notify()      # wake one waiter
        # condition.notify_all() # wake all waiters

# Event — simple flag: set/clear/wait
event = threading.Event()
event.set()            # set flag to True
event.clear()          # set flag to False
event.is_set()         # check flag
event.wait()           # block until set
event.wait(timeout=5)  # block up to 5 seconds

# Semaphore — limit concurrent access
semaphore = threading.Semaphore(5)   # allow at most 5 concurrent
with semaphore:
    do_limited_work()

# BoundedSemaphore — like Semaphore but raises if released too many times

# Barrier — synchronization point: wait for N threads
barrier = threading.Barrier(3)  # for 3 threads
def phase1():
    do_work()
    barrier.wait()    # all 3 threads must reach here before any proceed
    do_phase2()

# Timer — run function after delay
timer = threading.Timer(5.0, callback, args=[arg1], kwargs={})
timer.start()
timer.cancel()  # cancel before it fires


# ── Queue — thread-safe producer/consumer ─────────────────────
from queue import Queue, LifoQueue, PriorityQueue, Empty, Full

q: Queue[str] = Queue(maxsize=10)   # maxsize=0 means unlimited

# Producer
q.put("item")              # blocks if full
q.put("item", timeout=1.0) # wait max 1 second
q.put_nowait("item")       # raises Full if full

# Consumer
item = q.get()             # blocks if empty
item = q.get(timeout=1.0)  # wait max 1 second
item = q.get_nowait()      # raises Empty if empty

# Signal completion
q.task_done()              # must call after processing each item
q.join()                   # blocks until all items have task_done() called

# Thread pool using Queue
def worker_pool(n_workers: int, task_queue: Queue):
    threads = []
    for _ in range(n_workers):
        t = threading.Thread(target=worker_task, args=(task_queue,), daemon=True)
        t.start()
        threads.append(t)
    return threads

def worker_task(q: Queue):
    while True:
        try:
            item = q.get(timeout=1.0)
        except Empty:
            break
        process(item)
        q.task_done()
```

### 25.2 multiprocessing

```python
import multiprocessing as mp
from multiprocessing import Pool, Process, Queue, Pipe, Manager, Value, Array
import os

# ── Process ───────────────────────────────────────────────────
def compute(n: int) -> int:
    return sum(i*i for i in range(n))

p = mp.Process(target=compute, args=(10_000_000,))
p.start()
p.join()
p.exitcode    # 0 = success, None = still running, negative = signal

# Get return value via Queue (Process doesn't return values directly)
def worker_with_result(n: int, result_queue: mp.Queue):
    result = compute(n)
    result_queue.put(result)

q = mp.Queue()
p = mp.Process(target=worker_with_result, args=(10_000_000, q))
p.start()
result = q.get()   # blocks until result available
p.join()

# ── Pool — process pool for parallel map ──────────────────────
def square(n: int) -> int:
    return n * n

with Pool(processes=4) as pool:   # 4 worker processes
    # map: apply function to each item (blocks until all done)
    results = pool.map(square, range(20))

    # imap: lazy iterator (good for large iterables)
    for r in pool.imap(square, range(1000), chunksize=50):
        process(r)

    # starmap: for functions taking multiple arguments
    results = pool.starmap(pow, [(2, 10), (3, 5), (5, 3)])

    # apply_async: non-blocking, get result later
    future = pool.apply_async(square, (42,))
    result = future.get(timeout=5.0)

    # map_async: non-blocking map
    async_result = pool.map_async(square, range(20))
    results = async_result.get()


# ── Shared memory — share data between processes ──────────────
# Value — single shared value
counter = mp.Value("i", 0)    # "i" = C int; initial value 0
with counter.get_lock():
    counter.value += 1

# Array — shared array
shared_arr = mp.Array("d", [1.0, 2.0, 3.0])  # "d" = double
shared_arr[0] = 99.9

# Manager — shared Python objects (dict, list, etc.)
with mp.Manager() as manager:
    shared_dict = manager.dict()
    shared_list = manager.list()

    def worker(d, l, key, val):
        d[key] = val
        l.append(val)

    processes = [mp.Process(target=worker, args=(shared_dict, shared_list, i, i*10))
                 for i in range(5)]
    [p.start() for p in processes]
    [p.join() for p in processes]
    print(dict(shared_dict))   # {0:0, 1:10, 2:20, 3:30, 4:40}

# if __name__ == "__main__": guard REQUIRED on Windows for multiprocessing
if __name__ == "__main__":
    pool = Pool(4)
    # ...
```

### 25.3 concurrent.futures — High-Level Interface

```python
from concurrent.futures import (
    ThreadPoolExecutor, ProcessPoolExecutor,
    as_completed, wait, FIRST_COMPLETED, ALL_COMPLETED
)

# ── ThreadPoolExecutor ────────────────────────────────────────
def fetch_url(url: str) -> tuple[str, int]:
    response = requests.get(url, timeout=10)
    return url, response.status_code

urls = ["https://example.com", "https://python.org", "https://github.com"]

with ThreadPoolExecutor(max_workers=10) as executor:
    # map: submit all, iterate results in submission order
    for url, status in executor.map(fetch_url, urls):
        print(f"{url}: {status}")

    # submit: get Future objects for each task
    futures = {executor.submit(fetch_url, url): url for url in urls}

    # as_completed: process results as they finish (any order)
    for future in as_completed(futures, timeout=30):
        url = futures[future]
        try:
            url, status = future.result()
            print(f"{url}: {status}")
        except Exception as e:
            print(f"{url} failed: {e}")

# ── ProcessPoolExecutor ───────────────────────────────────────
import math

def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
    numbers = range(2, 1_000_000)
    primes = list(filter(None, executor.map(is_prime, numbers, chunksize=1000)))

# ── Future object API ─────────────────────────────────────────
future = executor.submit(my_function, arg1, arg2)
future.result(timeout=5.0)    # get result (blocks; raises exception if task failed)
future.exception()            # get exception if any (None if no exception)
future.done()                 # True if finished
future.running()              # True if currently running
future.cancelled()            # True if cancelled
future.cancel()               # attempt to cancel (only if not started)
future.add_done_callback(fn)  # fn(future) called when done

# ── wait — wait for multiple futures ─────────────────────────
done, not_done = wait(futures, timeout=10, return_when=ALL_COMPLETED)
done, not_done = wait(futures, return_when=FIRST_COMPLETED)
for f in done:
    print(f.result())
```

---

## Chapter 26: The Standard Library — Essential Modules

### 26.1 collections

```python
from collections import (
    Counter, defaultdict, OrderedDict, namedtuple,
    deque, ChainMap, UserDict, UserList, UserString
)

# ── Counter ───────────────────────────────────────────────────
words = "the quick brown fox jumps over the lazy dog the".split()
c = Counter(words)
print(c)                       # Counter({'the': 3, 'quick': 1, ...})
c.most_common(3)               # [('the', 3), ('quick', 1), ('brown', 1)]
c["the"]                       # 3
c["missing"]                   # 0 (no KeyError!)
c.total()                      # total count (Python 3.10+)
c.update(["the", "fox"])       # increment counts
c.subtract(["the"])            # decrement counts (can go negative)
c1 + c2                        # combine (add counts)
c1 - c2                        # subtract (remove zero/negative)
c1 & c2                        # intersection (min counts)
c1 | c2                        # union (max counts)
list(c.elements())             # expand: ['the', 'the', 'the', 'quick', ...]

# ── defaultdict ───────────────────────────────────────────────
# Like dict but provides a default value for missing keys
word_lengths = defaultdict(list)
for word in words:
    word_lengths[len(word)].append(word)
# {3: ['the', 'fox', 'the', 'the'], 5: ['quick', 'brown', ...], ...}

# default_factory can be any callable
dd_int  = defaultdict(int)     # default: 0
dd_list = defaultdict(list)    # default: []
dd_dict = defaultdict(dict)    # default: {}
dd_set  = defaultdict(set)     # default: set()
dd_zero = defaultdict(lambda: "N/A")   # custom default

# ── deque — double-ended queue ────────────────────────────────
d = deque([1, 2, 3], maxlen=5)   # maxlen: auto-discards from opposite end
d.appendleft(0)    # O(1) — insert at front
d.append(4)        # O(1) — insert at back
d.popleft()        # O(1) — remove from front
d.pop()            # O(1) — remove from back
d.rotate(1)        # rotate right by 1 (rotate(-1) = rotate left)
d.extend([5,6])
d.extendleft([7,8])  # extends from left (each element prepended in turn)

# Use deque for:
# ✅ Queue (FIFO): appendleft + pop, or append + popleft
# ✅ Stack (LIFO): append + pop (same as list, but O(1) guaranteed)
# ✅ Sliding window (maxlen): keeps last N elements automatically
# ❌ Random access: O(n) (not O(1) like list)

# Sliding window example
from collections import deque
def moving_average(values: list, window: int) -> list:
    dq = deque(maxlen=window)
    avgs = []
    for v in values:
        dq.append(v)
        if len(dq) == window:
            avgs.append(sum(dq) / window)
    return avgs

# ── OrderedDict ───────────────────────────────────────────────
# dict preserves insertion order since Python 3.7
# OrderedDict additional features:
od = OrderedDict([("b", 2), ("a", 1), ("c", 3)])
od.move_to_end("a")         # move "a" to end
od.move_to_end("c", False)  # move "c" to front
od.popitem()                # remove last inserted
od.popitem(last=False)      # remove first inserted

# ── ChainMap ──────────────────────────────────────────────────
# Logical merge of multiple dicts (reads all, writes to first)
defaults = {"color": "blue", "size": "medium"}
user_prefs = {"color": "red"}
cm = ChainMap(user_prefs, defaults)
cm["color"]    # "red" (from user_prefs)
cm["size"]     # "medium" (from defaults, user_prefs doesn't have it)
cm["font"] = "Arial"   # writes to user_prefs
```

### 26.2 functools

```python
from functools import (
    reduce, partial, partialmethod, wraps, lru_cache, cache,
    cached_property, total_ordering, singledispatch,
    singledispatchmethod, cmp_to_key, update_wrapper
)

# Covered in Chapter 5 — additional items:

# cmp_to_key — convert old-style comparison function to key function
# (for sorting with legacy comparison functions)
def compare(a, b):
    return (a > b) - (a < b)   # -1, 0, or 1

sorted(items, key=cmp_to_key(compare))

# partialmethod — like partial but for methods
class Widget:
    def _update(self, kind, value):
        print(f"Update {kind}={value}")

    set_color = partialmethod(_update, "color")
    set_size  = partialmethod(_update, "size")

w = Widget()
w.set_color("red")   # → Widget._update("color", "red")
w.set_size("large")  # → Widget._update("size", "large")
```

### 26.3 itertools (additional)

```python
import itertools as it

# accumulate with initial
list(it.accumulate([1,2,3,4,5], initial=0))  # [0,1,3,6,10,15]

# batched (Python 3.12)
list(it.batched("ABCDEFG", 3))  # [('A','B','C'),('D','E','F'),('G',)]

# pairwise (Python 3.10)
list(it.pairwise("ABCDE"))  # [('A','B'),('B','C'),('C','D'),('D','E')]
```

### 26.4 datetime and time

```python
from datetime import date, time, datetime, timedelta, timezone
import zoneinfo   # Python 3.9+

# ── date ──────────────────────────────────────────────────────
d = date.today()
d = date(2024, 3, 15)
d.year; d.month; d.day
d.isoformat()              # "2024-03-15"
d.strftime("%d/%m/%Y")    # "15/03/2024"
date.fromisoformat("2024-03-15")
d.weekday()                # 0=Monday, 6=Sunday
d.isoweekday()             # 1=Monday, 7=Sunday
d.isocalendar()            # (year, week, weekday)
d.replace(year=2025)       # new date with year changed
d + timedelta(days=30)     # arithmetic
(d2 - d1).days             # difference in days

# ── datetime ──────────────────────────────────────────────────
now = datetime.now()                          # naive (no timezone)
utc_now = datetime.now(timezone.utc)          # timezone-aware UTC
                                              # ALWAYS use aware datetimes!

dt = datetime(2024, 3, 15, 14, 30, 0)
dt = datetime.fromisoformat("2024-03-15T14:30:00+00:00")
dt = datetime.strptime("15/03/2024 14:30", "%d/%m/%Y %H:%M")
dt.isoformat()             # "2024-03-15T14:30:00"
dt.strftime("%Y-%m-%d %H:%M:%S")

# Timezone-aware datetimes
tz_ny = zoneinfo.ZoneInfo("America/New_York")
dt_ny = datetime.now(tz_ny)
dt_utc = dt_ny.astimezone(timezone.utc)     # convert to UTC
dt_tz = dt.replace(tzinfo=timezone.utc)     # make naive datetime aware
dt.tzinfo                                   # timezone info (None if naive)

# Timestamp conversion
dt.timestamp()                # Unix timestamp (float seconds since epoch)
datetime.fromtimestamp(1234567890.0, tz=timezone.utc)  # from Unix timestamp

# ── timedelta ─────────────────────────────────────────────────
delta = timedelta(days=7, hours=12, minutes=30, seconds=15)
delta.total_seconds()          # 648615.0
datetime.now() + timedelta(days=30)
datetime.now() - timedelta(weeks=1)

# ── time module (not datetime.time) ───────────────────────────
import time
time.time()            # current Unix timestamp as float
time.sleep(0.5)        # sleep 0.5 seconds
time.monotonic()       # monotonic clock (for measuring elapsed time; never goes back)
time.perf_counter()    # high-resolution performance counter (most precise)
time.process_time()    # CPU time for current process

start = time.perf_counter()
expensive_operation()
elapsed = time.perf_counter() - start
```

### 26.5 logging

```python
import logging
import logging.handlers
from typing import Any

# ── Basic setup ───────────────────────────────────────────────
# Level hierarchy: DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),           # console
        logging.FileHandler("app.log"),    # file
    ]
)

logger = logging.getLogger(__name__)   # best practice: use module name
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
logger.exception("Error with traceback", exc_info=True)  # logs traceback

# ── Structured logging ────────────────────────────────────────
# Log extra context as key-value pairs
logger.info("User logged in", extra={"user_id": 42, "ip": "192.168.1.1"})

# Using structlog (popular library for structured logging)
import structlog
log = structlog.get_logger()
log.info("request.received", method="POST", path="/api/users", duration_ms=23)
log.error("db.query.failed", query="SELECT ...", error=str(e))

# ── Production configuration ──────────────────────────────────
def setup_logging(level: str = "INFO") -> None:
    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # Rotating file handler — keeps last N files
    file_handler = logging.handlers.RotatingFileHandler(
        "app.log",
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=5,
    )
    file_handler.setFormatter(formatter)

    # Timed rotating — new file each day
    timed_handler = logging.handlers.TimedRotatingFileHandler(
        "app.log", when="midnight", interval=1, backupCount=30
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.addHandler(file_handler)

    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
```

### 26.6 json, csv, configparser, argparse

```python
import json

# ── JSON ─────────────────────────────────────────────────────
data = {"name": "Alice", "age": 30, "scores": [95, 87, 92]}

# Serialize
json_str = json.dumps(data)
json_pretty = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
json.dump(data, open("data.json", "w"))  # write to file

# Deserialize
parsed = json.loads(json_str)           # from string
parsed = json.load(open("data.json"))   # from file

# Custom encoder/decoder
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)   # raises TypeError for unknown types

json.dumps({"ts": datetime.now()}, cls=DateTimeEncoder)

# Decoder with object_hook
def decode_datetime(dct):
    for k, v in dct.items():
        if isinstance(v, str):
            try:
                dct[k] = datetime.fromisoformat(v)
            except ValueError:
                pass
    return dct

json.loads(json_str, object_hook=decode_datetime)


# ── CSV ──────────────────────────────────────────────────────
import csv

# Write
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "email"])
    writer.writeheader()
    writer.writerows([
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "Bob",   "age": 25, "email": "bob@example.com"},
    ])

# Read
with open("data.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])  # OrderedDict-like access

# ── argparse — CLI argument parsing ──────────────────────────
import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Process some data files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python script.py -v -n 10 input.txt output.txt"
    )

    # Positional arguments (required)
    parser.add_argument("input",  help="Input file path")
    parser.add_argument("output", help="Output file path")

    # Optional arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-n", "--count",   type=int, default=10, metavar="N", help="Number of items (default: 10)")
    parser.add_argument("-f", "--format",  choices=["json", "csv", "tsv"], default="json")
    parser.add_argument("--workers",       type=int, default=4)
    parser.add_argument("--tags",          nargs="+", help="One or more tags")  # --tags a b c
    parser.add_argument("--config",        type=argparse.FileType("r"))         # opens file

    # Subcommands
    subparsers = parser.add_subparsers(dest="command")
    import_parser = subparsers.add_parser("import", help="Import data")
    import_parser.add_argument("source", help="Source database URL")

    return parser

args = create_parser().parse_args()
print(args.verbose, args.count, args.format)
```

---

## Chapter 27: Performance — Profiling & Optimization

### 27.1 Profiling

```python
# ── timeit — microbenchmarking ───────────────────────────────
import timeit

# Time a statement
t = timeit.timeit("sum(range(1000))", number=10000)
print(f"Total: {t:.4f}s, per iteration: {t/10000*1000:.4f}ms")

# Compare two approaches
t1 = timeit.timeit("[x**2 for x in range(1000)]", number=10000)
t2 = timeit.timeit("list(map(lambda x: x**2, range(1000)))", number=10000)
print(f"List comp: {t1:.4f}s, map: {t2:.4f}s")

# As decorator
from functools import wraps
import time

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}: {elapsed*1000:.3f}ms")
        return result
    return wrapper

# ── cProfile — full profiling ─────────────────────────────────
import cProfile
import pstats
import io

profiler = cProfile.Profile()
profiler.enable()
main_function()
profiler.disable()

# Print stats
stats = pstats.Stats(profiler, stream=sys.stdout)
stats.sort_stats("cumulative")   # sort by cumulative time
stats.print_stats(20)            # print top 20 functions

# ── line_profiler — line-by-line profiling ────────────────────
# pip install line_profiler
# @profile decorator (added by kernprof tool)
# kernprof -l -v script.py

# ── memory_profiler — memory usage per line ───────────────────
# pip install memory_profiler
# @profile decorator
# python -m memory_profiler script.py

# ── tracemalloc — built-in memory profiling ───────────────────
import tracemalloc

tracemalloc.start()
main_function()
snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics("lineno")
for stat in stats[:10]:
    print(stat)
# Output: mymodule.py:42: size=1.5 MiB, count=10000, average=157 B
```

### 27.2 Optimization Techniques

```python
# ── Local variable vs global — always use local ───────────────
# Accessing local variables (LOAD_FAST) is faster than globals (LOAD_GLOBAL)

# ❌ Slow: accesses len as global on every iteration
def process_slow(items):
    result = []
    for i in range(len(items)):   # len accessed from global on each call
        result.append(items[i])
    return result

# ✅ Fast: cache to local variable
def process_fast(items):
    result = []
    _append = result.append  # cache method lookup
    for item in items:
        _append(item)
    return result

# ── String concatenation ──────────────────────────────────────
# ❌ Slow: O(n²) — creates new string on each +=
def concat_slow(items):
    result = ""
    for item in items:
        result += str(item)
    return result

# ✅ Fast: join is O(n)
def concat_fast(items):
    return "".join(str(item) for item in items)

# ── List comprehension vs for loop ────────────────────────────
# Comprehensions are faster (compiled differently, avoid attribute lookup)
squares_slow = []
for x in range(1000):
    squares_slow.append(x * x)

squares_fast = [x * x for x in range(1000)]  # ~30% faster

# But: for very large data, generator expression saves memory
total = sum(x * x for x in range(10_000_000))  # no list created

# ── set for membership testing ────────────────────────────────
items_list = list(range(100_000))
items_set  = set(items_list)

# ❌ O(n) — linear search
99999 in items_list    # scans up to 100,000 elements

# ✅ O(1) — hash lookup
99999 in items_set     # ~constant time

# ── Use built-ins and standard library (implemented in C) ─────
# sum(), min(), max(), sorted(), map(), filter() are all C-implemented
# Much faster than equivalent Python loops

# ✅ Built-in (C speed)
total = sum(x for x in data)
minimum = min(data)
unique = set(data)

# ❌ Python loop (slower)
total = 0
for x in data:
    total += x

# ── Avoid repeated dictionary lookups ─────────────────────────
d = {"a": 1, "b": 2, "c": 3}

# ❌ Multiple lookups for same key
if "a" in d:
    print(d["a"] + 1)
    process(d["a"])

# ✅ Single lookup
val = d.get("a")
if val is not None:
    print(val + 1)
    process(val)

# ── Use slots for many small objects ──────────────────────────
# (See Chapter 15.2)

# ── Numpy for numerical computation ───────────────────────────
import numpy as np

# ❌ Python loop — very slow for math
data = list(range(1_000_000))
result = [x * x for x in data]
total  = sum(result)

# ✅ NumPy vectorized — 50-100x faster
data_np = np.arange(1_000_000)
result_np = data_np * data_np       # element-wise, no Python loop
total_np  = result_np.sum()         # optimized sum

# ── Use lru_cache for expensive repeated computations ─────────
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2: return n
    return fib(n-1) + fib(n-2)

# Without cache: O(2^n) recursive calls
# With cache: O(n) unique calls, rest hit cache

# ── io.BytesIO / StringIO instead of file I/O ─────────────────
import io
buf = io.StringIO()
# Write to in-memory buffer (no disk I/O)
for item in items:
    buf.write(str(item))
result = buf.getvalue()
```

---

## Chapter 28: Packaging — pip, Poetry, pyproject.toml

### 28.1 pyproject.toml — Modern Python Packaging

```toml
# pyproject.toml — PEP 517/518/660 standard
[build-system]
requires      = ["hatchling"]        # or: "setuptools", "flit-core", "poetry-core"
build-backend = "hatchling.build"

[project]
name            = "mypackage"
version         = "2.1.0"
description     = "A useful Python library"
readme          = "README.md"
license         = { text = "MIT" }
authors         = [{ name = "Alice Smith", email = "alice@example.com" }]
keywords        = ["async", "utilities"]
classifiers     = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Topic :: Utilities",
]
requires-python = ">=3.11"

dependencies = [
    "httpx>=0.26.0",
    "pydantic>=2.5.0",
    "tenacity>=8.0.0",
]

[project.optional-dependencies]
dev  = ["pytest>=7.4", "pytest-cov", "mypy", "ruff", "black"]
docs = ["mkdocs", "mkdocstrings"]

[project.scripts]
myapp = "mypackage.cli:main"   # creates `myapp` command

[project.urls]
Homepage    = "https://github.com/alice/mypackage"
Repository  = "https://github.com/alice/mypackage"
Issues      = "https://github.com/alice/mypackage/issues"

# ── Tool configuration ────────────────────────────────────────
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts   = "-v --cov=mypackage --cov-report=term-missing"

[tool.mypy]
python_version        = "3.12"
strict                = true
ignore_missing_imports = true

[tool.ruff]          # linter + formatter
line-length    = 88
target-version = ["py311"]
select         = ["E", "F", "I", "N", "UP", "B", "A"]  # error sets
ignore         = ["E501"]

[tool.black]         # formatter
line-length    = 88
target-version = ["py311"]

[tool.coverage.run]
source = ["mypackage"]
omit   = ["*/tests/*"]
```

### 28.2 Poetry

```bash
# Create new project
poetry new mypackage
cd mypackage

# Add dependencies
poetry add httpx pydantic
poetry add --group dev pytest mypy ruff

# Install project + deps
poetry install

# Virtual environment
poetry env info
poetry shell           # activate venv
poetry run python -m mypackage

# Build and publish
poetry build           # creates dist/*.whl and dist/*.tar.gz
poetry publish         # uploads to PyPI (needs account/token)
poetry publish --repository testpypi

# Lock file management
poetry update          # update all deps
poetry update httpx    # update specific dep
poetry show            # list all installed packages
poetry check           # validate pyproject.toml

# Export requirements (for Docker etc.)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### 28.3 Virtual Environments

```bash
# venv (built-in)
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate.bat    # Windows
deactivate

# pip commands
pip install package
pip install "package>=1.0,<2.0"
pip install -r requirements.txt
pip install -e .              # editable install (develop mode)
pip freeze > requirements.txt
pip list --outdated
pip show package

# uv (modern, Rust-based, much faster than pip)
uv pip install httpx
uv venv
uv run python script.py

# pipx — install CLI tools in isolated envs
pipx install black mypy ruff
pipx run pytest               # run without installing
```

---

## Chapter 29: Design Patterns in Python

### 29.1 Creational Patterns

```python
# ── Singleton ─────────────────────────────────────────────────
class Config:
    _instance: "Config | None" = None

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._data = {}
            self._initialized = True

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value

# Singleton via module — simpler and Pythonic
# config.py:
# _config = {}
# def get(key, default=None): return _config.get(key, default)
# def set(key, value): _config[key] = value


# ── Factory Method ────────────────────────────────────────────
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Email to {recipient}: {message}")
        return True

class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"SMS to {recipient}: {message}")
        return True

class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"Push to {recipient}: {message}")
        return True

def notification_factory(channel: str) -> Notification:
    channels = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "push":  PushNotification,
    }
    if channel not in channels:
        raise ValueError(f"Unknown channel: {channel!r}. Valid: {list(channels)}")
    return channels[channel]()


# ── Builder ───────────────────────────────────────────────────
from dataclasses import dataclass, field
from typing import Self

@dataclass
class QueryConfig:
    table:   str
    columns: list[str]   = field(default_factory=lambda: ["*"])
    where:   list[str]   = field(default_factory=list)
    order:   list[str]   = field(default_factory=list)
    limit:   int | None  = None
    offset:  int         = 0

class QueryBuilder:
    def __init__(self, table: str) -> None:
        self._config = QueryConfig(table=table)

    def select(self, *columns: str) -> Self:
        self._config.columns = list(columns)
        return self

    def where(self, condition: str) -> Self:
        self._config.where.append(condition)
        return self

    def order_by(self, *columns: str) -> Self:
        self._config.order.extend(columns)
        return self

    def limit(self, n: int) -> Self:
        self._config.limit = n
        return self

    def offset(self, n: int) -> Self:
        self._config.offset = n
        return self

    def build(self) -> str:
        cfg = self._config
        sql = f"SELECT {', '.join(cfg.columns)} FROM {cfg.table}"
        if cfg.where:
            sql += " WHERE " + " AND ".join(cfg.where)
        if cfg.order:
            sql += " ORDER BY " + ", ".join(cfg.order)
        if cfg.limit is not None:
            sql += f" LIMIT {cfg.limit}"
        if cfg.offset:
            sql += f" OFFSET {cfg.offset}"
        return sql

query = (QueryBuilder("users")
    .select("id", "name", "email")
    .where("active = true")
    .where("age >= 18")
    .order_by("name ASC")
    .limit(20)
    .offset(40)
    .build())
```

### 29.2 Structural Patterns

```python
# ── Decorator Pattern (not the Python decorator syntax) ───────
class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str: ...

class PlainText(TextProcessor):
    def process(self, text: str) -> str:
        return text

class TextDecorator(TextProcessor):
    def __init__(self, component: TextProcessor):
        self._component = component

    def process(self, text: str) -> str:
        return self._component.process(text)

class UpperCaseDecorator(TextDecorator):
    def process(self, text: str) -> str:
        return super().process(text).upper()

class TrimDecorator(TextDecorator):
    def process(self, text: str) -> str:
        return super().process(text).strip()

class SuffixDecorator(TextDecorator):
    def __init__(self, component: TextProcessor, suffix: str):
        super().__init__(component)
        self._suffix = suffix

    def process(self, text: str) -> str:
        return super().process(text) + self._suffix

# Compose decorators
processor = SuffixDecorator(UpperCaseDecorator(TrimDecorator(PlainText())), "!")
print(processor.process("  hello world  "))   # "HELLO WORLD!"


# ── Proxy / Lazy Loading ──────────────────────────────────────
class ExpensiveResource:
    def __init__(self):
        print("Loading expensive resource...")
        import time; time.sleep(1)
        self.data = "expensive data"

    def process(self) -> str:
        return self.data

class LazyProxy:
    def __init__(self):
        self._resource: ExpensiveResource | None = None

    @property
    def resource(self) -> ExpensiveResource:
        if self._resource is None:
            self._resource = ExpensiveResource()  # created on first access
        return self._resource

    def process(self) -> str:
        return self.resource.process()

proxy = LazyProxy()       # fast — resource not loaded
result = proxy.process()  # slow first call — loads resource
result = proxy.process()  # fast — resource already loaded


# ── Adapter ───────────────────────────────────────────────────
class OldEmailSystem:
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        print(f"OldSystem: sending to {to_email}")
        return True

class NewNotificationInterface(ABC):
    @abstractmethod
    def notify(self, recipient: str, message: str, **options) -> bool: ...

class EmailAdapter(NewNotificationInterface):
    def __init__(self, old_system: OldEmailSystem):
        self._old_system = old_system

    def notify(self, recipient: str, message: str, **options) -> bool:
        subject = options.get("subject", "Notification")
        return self._old_system.send_email(recipient, subject, message)
```

### 29.3 Behavioral Patterns

```python
# ── Observer ──────────────────────────────────────────────────
from typing import Callable

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback: Callable) -> None:
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class UserService(EventEmitter):
    def create_user(self, name: str, email: str) -> dict:
        user = {"id": 1, "name": name, "email": email}
        self.emit("user.created", user)
        return user

    def delete_user(self, user_id: int) -> None:
        self.emit("user.deleted", user_id)


service = UserService()
service.on("user.created", lambda u: print(f"Welcome {u['name']}!"))
service.on("user.created", lambda u: send_welcome_email(u["email"]))
service.on("user.deleted", lambda uid: audit_log(f"User {uid} deleted"))

service.create_user("Alice", "alice@example.com")
# → Welcome Alice!
# → (sends welcome email)


# ── Strategy ──────────────────────────────────────────────────
from typing import Protocol

class SortStrategy(Protocol):
    def sort(self, data: list) -> list: ...

class BubbleSort:
    def sort(self, data: list) -> list:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(n - i - 1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        return result

class QuickSort:
    def sort(self, data: list) -> list:
        if len(data) <= 1: return data
        pivot = data[len(data) // 2]
        left   = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right  = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

    # Swap strategy at runtime
    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy


# In Python, functions work as strategies (simpler approach)
def sort_with(data: list, strategy: Callable[[list], list]) -> list:
    return strategy(data)

sort_with([3,1,4,1,5], sorted)            # built-in
sort_with([3,1,4,1,5], lambda l: l[::-1]) # reverse


# ── Command ───────────────────────────────────────────────────
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class TextEditor:
    def __init__(self):
        self.text = ""
        self._history: list[Command] = []

    def execute(self, cmd: Command) -> None:
        cmd.execute()
        self._history.append(cmd)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()

class InsertCommand(Command):
    def __init__(self, editor: TextEditor, pos: int, text: str):
        self.editor = editor
        self.pos    = pos
        self.text   = text

    def execute(self) -> None:
        self.editor.text = (
            self.editor.text[:self.pos] + self.text + self.editor.text[self.pos:]
        )

    def undo(self) -> None:
        self.editor.text = (
            self.editor.text[:self.pos] + self.editor.text[self.pos + len(self.text):]
        )
```

---

## Chapter 30: Data & Scientific Stack

### 30.1 NumPy — Numerical Arrays

```python
import numpy as np

# ── Array creation ────────────────────────────────────────────
a = np.array([1, 2, 3, 4, 5])              # from list
b = np.array([[1,2,3],[4,5,6]])             # 2D array
c = np.zeros((3, 4))                        # 3×4 array of zeros
d = np.ones((2, 3), dtype=np.float32)       # 2×3 array of ones (float32)
e = np.full((3, 3), 7)                      # filled with 7
f = np.eye(4)                               # 4×4 identity matrix
g = np.arange(0, 10, 0.5)                  # like range() but float, returns array
h = np.linspace(0, 1, 100)                 # 100 equally-spaced values from 0 to 1
i = np.random.rand(3, 3)                   # random uniform [0, 1)
j = np.random.randn(3, 3)                  # random standard normal
k = np.random.randint(0, 10, (5, 5))      # random integers

# ── Array properties ──────────────────────────────────────────
a.shape     # (5,) — tuple of dimensions
b.shape     # (2, 3)
a.ndim      # 1 (number of dimensions)
b.ndim      # 2
a.dtype     # dtype('int64')
a.size      # 5 (total number of elements)
b.size      # 6
a.nbytes    # 40 (bytes: size × itemsize)
a.itemsize  # 8 (bytes per element)

# ── Indexing and slicing ──────────────────────────────────────
a = np.array([10, 20, 30, 40, 50])
a[0]        # 10
a[-1]       # 50
a[1:4]      # array([20, 30, 40])
a[::2]      # array([10, 30, 50])

b = np.array([[1,2,3],[4,5,6],[7,8,9]])
b[0, 2]     # 3 (row 0, col 2) — NumPy syntax
b[1, :]     # array([4, 5, 6]) — entire row 1
b[:, 2]     # array([3, 6, 9]) — entire column 2
b[0:2, 1:3] # array([[2,3],[5,6]]) — sub-matrix

# Boolean indexing (masking)
a = np.array([1, -2, 3, -4, 5])
mask = a > 0                # array([True, False, True, False, True])
a[mask]                     # array([1, 3, 5]) — only positive values
a[a > 0] = 0               # set all positive to 0

# Fancy indexing (array of indices)
a[[0, 2, 4]]               # array([1, 3, 5])
a[np.array([0, 2, 4])]    # same

# ── Vectorized operations — NO PYTHON LOOPS NEEDED ───────────
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

a + b          # array([11, 22, 33, 44, 55]) — element-wise
a * b          # array([10, 40, 90, 160, 250])
a ** 2         # array([1, 4, 9, 16, 25])
np.sqrt(a)     # array([1.0, 1.414, 1.732, 2.0, 2.236])
np.sin(a)      # element-wise sin
np.exp(a)      # element-wise e^x

# Broadcasting — operations between arrays of different shapes
a = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
b = np.array([10, 20, 30])              # shape (3,)
a + b   # broadcasts b across rows: [[11,22,33],[14,25,36]]

c = np.array([[10], [20]])              # shape (2, 1)
a + c   # broadcasts c across columns: [[11,12,13],[24,25,26]]

# ── Aggregations ─────────────────────────────────────────────
a.sum()             # sum of all
a.sum(axis=0)       # sum along rows (result is 1D)
a.sum(axis=1)       # sum along columns (result is 1D)
a.min(); a.max()
a.mean(); a.std(); a.var()
a.cumsum()          # cumulative sum
np.argmin(a)        # index of minimum
np.argmax(a)        # index of maximum
np.unique(a)        # unique elements (sorted)
np.sort(a, axis=-1) # sort along last axis

# ── Reshaping ─────────────────────────────────────────────────
a = np.arange(12)    # [0..11]
a.reshape(3, 4)      # 3×4 matrix (must be compatible)
a.reshape(2, -1)     # 2 rows, infer columns (→ 2×6)
a.reshape(-1, 4)     # infer rows, 4 cols (→ 3×4)
a.ravel()            # flatten to 1D
a.flatten()          # flatten to 1D (always copy)
a.T                  # transpose
a.swapaxes(0, 1)    # swap axes
np.expand_dims(a, axis=0)  # add dimension at axis 0
a[:, np.newaxis]     # add dimension: (n,) → (n, 1)
np.squeeze(a)        # remove dimensions of size 1

# ── Linear algebra ───────────────────────────────────────────
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B              # matrix multiply: [[19,22],[43,50]]
np.dot(A, B)       # same as @
np.linalg.det(A)   # determinant: -2.0
np.linalg.inv(A)   # inverse matrix
np.linalg.norm(A)  # Frobenius norm
eigenvalues, eigenvectors = np.linalg.eig(A)
U, S, Vt = np.linalg.svd(A)   # singular value decomposition
np.linalg.solve(A, np.array([1, 2]))  # solve Ax = b
```

### 30.2 pandas — Data Analysis

```python
import pandas as pd
import numpy as np

# ── Series — 1D labeled array ─────────────────────────────────
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
s["b"]          # 20 — label-based
s[1]            # 20 — position-based
s[["a", "c"]]   # Series with a and c
s[s > 15]       # boolean indexing → Series([20, 30, 40])
s.mean()        # 25.0
s.describe()    # count, mean, std, min, 25%, 50%, 75%, max

# ── DataFrame — 2D labeled table ──────────────────────────────
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "age":    [30, 25, 35, 28],
    "score":  [95.0, 87.5, 92.0, 88.0],
    "active": [True, True, False, True],
})

# From various sources
df = pd.read_csv("data.csv")
df = pd.read_json("data.json")
df = pd.read_excel("data.xlsx")
df = pd.read_sql("SELECT * FROM users", connection)
df = pd.read_parquet("data.parquet")   # columnar format, great for analytics

# Save
df.to_csv("output.csv", index=False)
df.to_json("output.json", orient="records")
df.to_parquet("output.parquet")

# ── Inspection ────────────────────────────────────────────────
df.shape           # (4, 4)
df.dtypes          # data types per column
df.info()          # columns, dtypes, non-null counts, memory
df.describe()      # statistics for numeric columns
df.head(3)         # first 3 rows
df.tail(3)         # last 3 rows
df.sample(3)       # random 3 rows
df.columns         # Index(['name', 'age', 'score', 'active'])
df.index           # RangeIndex(start=0, stop=4, step=1)

# ── Selection ─────────────────────────────────────────────────
df["name"]         # select column → Series
df[["name", "age"]]  # select multiple columns → DataFrame
df[df["age"] > 28]   # boolean filter → DataFrame
df.loc[0]          # row by label
df.loc[1:3, "name":"score"]  # rows 1-3, cols name to score (INCLUSIVE)
df.iloc[0]         # row by integer position
df.iloc[0:2, 0:2]  # rows 0-1, cols 0-1 (exclusive end like Python)

# ── Filtering ─────────────────────────────────────────────────
df[df["active"]]                          # active users
df[(df["age"] > 25) & (df["score"] > 90)] # AND conditions
df[(df["age"] < 26) | (df["age"] > 33)]  # OR conditions
df[df["name"].isin(["Alice", "Bob"])]     # in list
df[df["name"].str.startswith("A")]        # string filter
df[df["age"].between(25, 30)]             # range filter
df[df["score"].notna()]                   # not null

# query() method — string-based filter
df.query("age > 25 and score > 90")
df.query("name in ['Alice', 'Bob']")
df.query("age > @min_age", engine="python")  # use local variable

# ── Manipulation ──────────────────────────────────────────────
# Add column
df["grade"] = df["score"].apply(lambda s: "A" if s >= 90 else "B")
df["normalized"] = (df["score"] - df["score"].mean()) / df["score"].std()

# Remove column
df = df.drop(columns=["grade"])
df.drop("score", axis=1, inplace=True)

# Rename columns
df.rename(columns={"name": "full_name", "age": "years"}, inplace=True)

# Sort
df.sort_values("age", ascending=False)
df.sort_values(["active", "score"], ascending=[True, False])

# Apply function
df["score"].apply(lambda x: round(x))
df.apply(lambda row: row["age"] + row["score"], axis=1)  # row-wise

# Map values
df["active"].map({True: "yes", False: "no"})

# ── Missing data ──────────────────────────────────────────────
df.isnull().any()              # which columns have nulls
df.isnull().sum()              # count nulls per column
df.dropna()                    # drop rows with ANY null
df.dropna(subset=["email"])    # drop only if specific col is null
df.fillna(0)                   # fill with value
df.fillna(method="ffill")      # forward fill (propagate last valid)
df.fillna(df.mean())           # fill with column mean

# ── Groupby ───────────────────────────────────────────────────
# Split-Apply-Combine pattern
grouped = df.groupby("active")
grouped["score"].mean()        # mean score by active status
grouped.agg({
    "score": ["mean", "std", "count"],
    "age":   ["min", "max"],
})

df.groupby(["active", "grade"]).size()   # cross-tabulation
df.groupby("active").apply(lambda g: g.sort_values("score").head(2))  # top 2 per group

# ── Merge and Join ────────────────────────────────────────────
users  = pd.DataFrame({"id": [1,2,3], "name": ["Alice","Bob","Carol"]})
orders = pd.DataFrame({"user_id": [1,1,2], "amount": [100, 200, 150]})

pd.merge(users, orders, left_on="id", right_on="user_id", how="inner")  # INNER JOIN
pd.merge(users, orders, left_on="id", right_on="user_id", how="left")   # LEFT JOIN
pd.concat([df1, df2], ignore_index=True)   # stack vertically

# ── Time series ───────────────────────────────────────────────
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.resample("D").mean()        # resample to daily frequency
df.rolling(window=7).mean()    # 7-day rolling average
df["2024"]                     # select year
df["2024-03":"2024-06"]        # select date range


# ── Pivot tables ──────────────────────────────────────────────
df.pivot_table(
    values="score",
    index="active",
    columns="grade",
    aggfunc="mean",
    fill_value=0,
)
```

### 30.3 requests — HTTP Client

```python
import requests
from requests import Session, Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ── Basic requests ────────────────────────────────────────────
response = requests.get("https://api.example.com/users")
response.status_code    # 200
response.json()          # parse JSON body
response.text            # body as string
response.content         # body as bytes
response.headers         # response headers dict
response.url             # final URL (after redirects)
response.raise_for_status()  # raises HTTPError if 4xx or 5xx

# POST with JSON
r = requests.post(
    "https://api.example.com/users",
    json={"name": "Alice", "email": "alice@example.com"},  # auto-sets Content-Type
    headers={"Authorization": "Bearer token123"},
    timeout=(5, 30),   # (connect_timeout, read_timeout) in seconds
)

# File upload
with open("image.png", "rb") as f:
    r = requests.post(url, files={"file": f})

# Query parameters
r = requests.get(url, params={"limit": 10, "offset": 20, "sort": "name"})
# → GET /url?limit=10&offset=20&sort=name

# ── Session — reuse connection, cookies, headers ──────────────
session = Session()
session.headers.update({
    "Authorization": "Bearer your-token",
    "User-Agent":    "MyApp/1.0",
})
session.auth = ("username", "password")  # basic auth

r1 = session.get("https://api.example.com/users")    # reuses TCP connection
r2 = session.post("https://api.example.com/orders")  # shares headers + auth

# ── Retry logic ───────────────────────────────────────────────
retry_strategy = Retry(
    total=3,
    backoff_factor=1,            # 1s, 2s, 4s between retries
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

# ── Context manager ───────────────────────────────────────────
with Session() as session:
    r = session.get(url)
    # session closed automatically

# ── Streaming response ────────────────────────────────────────
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open("large_file.bin", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

# Text streaming (Server-Sent Events)
with requests.get(sse_url, stream=True, headers={"Accept": "text/event-stream"}) as r:
    for line in r.iter_lines():
        if line:
            process_event(line.decode("utf-8"))
```

---

## Python Quick Reference Cheat Sheet

### Data Types Decision Table
```
Need:                                  Use:
─────────────────────────────────────────────────────────────────────────
Ordered, mutable, indexed collection   list
Ordered, immutable, hashable           tuple
Fast O(1) key lookup, ordered (3.7+)  dict
Unique elements, set math              set
Immutable set (dict key, frozenset)    frozenset
Ordered dict with move operations      collections.OrderedDict
Count occurrences                      collections.Counter
Dict with default values               collections.defaultdict
O(1) append/pop from both ends         collections.deque
Compact homogeneous numbers            array.array or numpy.ndarray
Immutable with validation              Pydantic model / frozen dataclass
Typed struct                           dataclass / NamedTuple
```

### Common Gotchas
```python
# 1. Mutable default argument
def bad(items=[]):  # same list object shared across all calls!
    items.append(1)
def good(items=None):
    if items is None: items = []

# 2. Late binding in closures  
fns = [lambda: i for i in range(3)]  # all print 2!
fns = [lambda i=i: i for i in range(3)]  # fixed: capture by default arg

# 3. is vs ==
a = 1000; b = 1000
a is b   # False (large int not cached)
a == b   # True

# 4. Augmented assignment on tuples
t = ([1,2], [3,4])
t[0] += [5]   # TypeError! But t is mutated: t = ([1,2,5], [3,4])
              # += calls __iadd__ which modifies list, then tries to reassign

# 5. Chained comparisons
x = 5
1 < x < 10   # True (evaluated as: 1 < x AND x < 10)

# 6. dict.keys() is a view
d = {"a": 1}
keys = d.keys()
d["b"] = 2
print(keys)  # dict_keys(['a', 'b']) — includes 'b'!

# 7. None as default vs sentinel
def f(arg=None):     # None means "not provided" — but what if None is valid?
    if arg is None:  # can't distinguish "not provided" from "provided None"
        arg = []
# Better: use a sentinel
_MISSING = object()  # unique object, never equal to anything else
def f(arg=_MISSING):
    if arg is _MISSING:
        arg = []
```

### Complexity Reference
```
Operation          list    dict/set   deque   heap   sorted list
─────────────────────────────────────────────────────────────────────
Access by index    O(1)    —          O(n)    O(1)   O(1)
Search (in)        O(n)    O(1)       O(n)    O(n)   O(log n)
Insert at end      O(1)*   O(1)*      O(1)    O(log n) O(n)
Insert at front    O(n)    —          O(1)    —      O(n)
Delete by value    O(n)    O(1)       O(n)    —      O(n)
Delete by index    O(n)    —          O(n)    —      O(n)
Min/Max            O(n)    —          O(n)    O(1)   O(1)
Sort               O(n log n)  —      —       —      —

* amortized
```
