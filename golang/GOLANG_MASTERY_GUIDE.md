# The Complete Go (Golang) Mastery Guide
> Every concept explained from first principles — why Go was built the way it was, how its type system, concurrency model, and toolchain work, with production-grade examples throughout.

---

## Table of Contents

### Part I — Language Foundations
1. [Why Go? Philosophy & Design](#chapter-1-why-go-philosophy--design)
2. [Program Structure & Toolchain](#chapter-2-program-structure--toolchain)
3. [Types, Variables & Constants](#chapter-3-types-variables--constants)
4. [Operators & Expressions](#chapter-4-operators--expressions)
5. [Control Flow](#chapter-5-control-flow)
6. [Functions — First-Class Citizens](#chapter-6-functions--first-class-citizens)
7. [Pointers — Go's Approach](#chapter-7-pointers--gos-approach)

### Part II — Composite Types
8. [Arrays & Slices — The Workhorse](#chapter-8-arrays--slices--the-workhorse)
9. [Maps](#chapter-9-maps)
10. [Structs](#chapter-10-structs)
11. [Methods](#chapter-11-methods)
12. [Interfaces — Go's Superpower](#chapter-12-interfaces--gos-superpower)

### Part III — Advanced Language Features
13. [Goroutines & Concurrency Model](#chapter-13-goroutines--concurrency-model)
14. [Channels — Communicating Sequential Processes](#chapter-14-channels--communicating-sequential-processes)
15. [The sync Package](#chapter-15-the-sync-package)
16. [Error Handling — Go's Philosophy](#chapter-16-error-handling--gos-philosophy)
17. [Generics (Go 1.18+)](#chapter-17-generics-go-118)
18. [Packages & Modules](#chapter-18-packages--modules)

### Part IV — Standard Library & Patterns
19. [Essential Standard Library](#chapter-19-essential-standard-library)
20. [Testing in Go](#chapter-20-testing-in-go)
21. [HTTP & REST with net/http](#chapter-21-http--rest-with-nethttp)
22. [Context — Deadlines & Cancellation](#chapter-22-context--deadlines--cancellation)
23. [Common Go Patterns](#chapter-23-common-go-patterns)
24. [Performance & Profiling](#chapter-24-performance--profiling)

---

# PART I — LANGUAGE FOUNDATIONS

---

## Chapter 1: Why Go? Philosophy & Design

### 1.1 The Problem Go Was Built to Solve

Go was created at Google in 2007 by Robert Griesemer, Rob Pike, and Ken Thompson — three of computing's legends. They were frustrated with the state of systems programming at Google's scale:

```
The problems at Google-scale:
  ❌ C/C++: fast, but compilation took 45 minutes for large codebases
              memory safety bugs, no garbage collection, complex build systems
  ❌ Java:   productive, but JVM startup latency, verbose code, heavyweight runtime
  ❌ Python:  readable, but too slow for systems code, GIL limits concurrency
  
What they wanted:
  ✅ Compilation speed of scripting languages
  ✅ Execution speed of C
  ✅ Safety of garbage collection
  ✅ Simplicity of Python
  ✅ Native concurrency for multi-core/networked systems
```

### 1.2 Go's Core Design Principles

**1. Simplicity over cleverness:** Go has 25 keywords (Java has 50+, C++ has 80+). If you can solve a problem in Go in one way, that's better than three clever ways.

**2. Explicit over implicit:** No hidden control flow, no operator overloading, no implicit conversions. What you read is exactly what happens.

**3. Composition over inheritance:** Go has no class hierarchy. Behaviour is composed via interfaces and struct embedding.

**4. Concurrency is a first-class citizen:** Goroutines and channels are built into the language, not bolted on via libraries.

**5. Errors are values:** No exception mechanism. Errors are regular values returned from functions — you handle them explicitly.

**6. Fast compilation to native code:** A 500,000 line Go program compiles in seconds. Go compiles to a single statically-linked binary.

### 1.3 What Go Is Not

```
Go deliberately omits:
  No inheritance (use interfaces + composition)
  No generics in Go < 1.18 (added in 1.18, but sparingly)
  No exceptions (use error values)
  No operator overloading
  No implicit type conversions
  No macros or templates
  No function/method overloading
  No default parameter values
  No optional named parameters

These omissions are INTENTIONAL. Each one reduces language complexity.
"A language that is too easy to write in is often too hard to read." — Rob Pike
```

### 1.4 Where Go Excels

```
✅ Web servers, APIs, microservices (net/http is fast and built-in)
✅ CLI tools (single static binary, fast startup)
✅ DevOps/infrastructure tools (Docker, Kubernetes, Terraform are written in Go)
✅ Concurrent systems (goroutines are lightweight; millions feasible)
✅ Network services (gRPC, message queues, proxies)
✅ Cloud-native backends

❌ System programming requiring direct memory control → use Rust/C
❌ GUI applications → use Electron/Qt with other languages
❌ Scientific computing → use Python + NumPy
❌ Android/iOS → use Kotlin/Swift (though Go Mobile exists)
```

---

## Chapter 2: Program Structure & Toolchain

### 2.1 Every Go Program

```go
// Every Go source file starts with a package declaration
package main  // 'main' is the entry-point package

// Import statements — only import what you use
import (
    "fmt"       // formatted I/O
    "os"        // operating system interface
    "strings"   // string utilities
)

// main() is the entry point — no parameters, no return value
// (Command-line args: os.Args, exit code: os.Exit)
func main() {
    fmt.Println("Hello, World!")
    
    // Command-line arguments
    args := os.Args     // os.Args[0] = program name
    if len(args) > 1 {
        fmt.Println("Hello,", args[1])
    }
}
```

```bash
# Go toolchain commands — all you need
go run main.go              # compile and run (no binary saved)
go build .                  # compile to binary (./main or main.exe)
go build -o myapp .         # compile with specific output name
go test ./...               # run all tests in all packages
go test -v ./...            # verbose test output
go test -run TestName ./... # run specific test
go test -bench=. ./...      # run benchmarks
go fmt ./...                # format all code (use gofmt style — not optional)
go vet ./...                # static analysis (catches common bugs)
go mod init module/name     # initialize Go module
go mod tidy                 # add missing, remove unused dependencies
go get github.com/pkg/...   # add a dependency
go doc fmt.Println          # documentation lookup
go install tool@latest      # install a tool binary
```

### 2.2 The Go Module System

```
Before Go modules (pre-1.11): GOPATH hell — all Go code in one global directory.
Go modules (1.11+): each project has its own go.mod — proper dependency management.
```

```bash
# Creating a new project
mkdir myproject && cd myproject
go mod init github.com/myname/myproject   # creates go.mod

# go.mod file:
module github.com/myname/myproject

go 1.21                           # minimum Go version

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/stretchr/testify v1.8.4
)

# go.sum: cryptographic checksums of every dependency version
# Always commit both go.mod and go.sum
```

### 2.3 Package Structure

```
myproject/
├── go.mod
├── go.sum
├── main.go              ← package main (entry point)
├── cmd/
│   └── server/
│       └── main.go      ← another executable (package main)
├── internal/            ← can only be imported by this module
│   └── auth/
│       ├── auth.go      ← package auth
│       └── auth_test.go ← package auth (or auth_test for black-box)
├── pkg/                 ← public packages (can be imported externally)
│   └── models/
│       └── user.go      ← package models
└── api/
    └── handlers.go      ← package api
```

```go
// internal/auth/auth.go
package auth

// Exported: starts with uppercase — visible outside package
func ValidateToken(token string) bool {
    return validateInternal(token)  // calls unexported function
}

// Unexported: starts with lowercase — only visible inside package auth
func validateInternal(token string) bool {
    return len(token) > 10
}

// Exported type
type User struct {
    ID       int
    Username string
    email    string    // unexported field — only accessible within package auth
}

// Constructor convention (Go has no 'new' keyword for custom types)
func NewUser(id int, username, email string) *User {
    return &User{
        ID:       id,
        Username: username,
        email:    email,
    }
}
```

### 2.4 init() — Package Initialization

```go
package database

import "fmt"

var connection *DB   // package-level variable

// init() runs automatically before main(), after all imports are initialized
// Each package can have multiple init() functions
// Executed in the order: imported packages first, then this package's init()
func init() {
    connection = connectToDatabase()
    fmt.Println("Database package initialized")
}

// Multiple init() in same package — both run (in order of appearance)
func init() {
    registerMetrics()
}
```

---

## Chapter 3: Types, Variables & Constants

### 3.1 The Type System — Static and Strong

Go is **statically typed** (types checked at compile time) and **strongly typed** (no implicit conversions between unrelated types). Unlike C, you cannot cast a pointer to an int. Unlike JavaScript, `1 + "1"` is a compile error.

```go
// Every variable has an exactly one type, known at compile time
var x int     = 5
var y float64 = 5.0
// z := x + y  // COMPILE ERROR: mismatched types int and float64
z := float64(x) + y  // explicit conversion required: 10.0
```

### 3.2 Built-in Types

```go
// ── Boolean ────────────────────────────────────────────────
var b bool = true         // false by default

// ── Integer Types ──────────────────────────────────────────
var i8   int8   = 127          // -128 to 127
var i16  int16  = 32767
var i32  int32  = 2147483647
var i64  int64  = 9223372036854775807
var u8   uint8  = 255          // byte alias
var u16  uint16 = 65535
var u32  uint32 = 4294967295
var u64  uint64 = 18446744073709551615

// Platform-dependent (32-bit on 32-bit OS, 64-bit on 64-bit OS)
var i  int  = -1000            // Use for: loop counters, lengths, indices
var u  uint = 1000             // Use for: bitmasks, unsigned arithmetic

// Aliases
var b2 byte = 65               // byte = uint8; for binary data
var r  rune = '©'              // rune = int32; for Unicode code points

// Special
var ptr uintptr                // integer large enough to hold a pointer (rarely needed)

// ── Floating Point ─────────────────────────────────────────
var f32 float32 = 3.14         // ~7 decimal digits precision
var f64 float64 = 3.14159265358979 // ~15 decimal digits (default float literal type)

// ── Complex ────────────────────────────────────────────────
var c64  complex64  = 1 + 2i   // two float32s
var c128 complex128 = 1 + 2i   // two float64s
real(c128)    // 1.0
imag(c128)    // 2.0

// ── String ─────────────────────────────────────────────────
var s string = "Hello, 世界"    // UTF-8 encoded, immutable byte sequence
len(s)        // 13 (bytes, not characters!)
// Iterate by runes (Unicode code points):
for i, r := range s {
    fmt.Printf("index %d: %c (%d)\n", i, r, r)
}

// ── Zero Values (default when declared but not initialized) ─
var zeroBool   bool    // false
var zeroInt    int     // 0
var zeroFloat  float64 // 0.0
var zeroString string  // ""
var zeroPtr    *int    // nil
var zeroSlice  []int   // nil
var zeroMap    map[string]int  // nil
var zeroFunc   func()  // nil
```

### 3.3 Variable Declaration — All Forms

```go
// Form 1: var with explicit type (for zero values, package scope)
var name string
var count int = 0
var pi float64 = 3.14159

// Form 2: var with inferred type
var greeting = "Hello"   // type inferred: string
var x, y = 1, 2          // multiple declaration

// Form 3: short declaration := (ONLY inside functions)
message := "Hello"       // most common in function bodies
a, b := 10, 20           // multiple short declaration
a, c := 30, 40           // ':=' can mix new (c) and existing (a) variables
                         // — at least one variable must be NEW

// Form 4: var block (group related declarations)
var (
    host    = "localhost"
    port    = 8080
    timeout = 30 * time.Second
    debug   bool  // zero value = false
)

// Form 5: blank identifier — discard values
result, _ := strconv.Atoi("42")   // _ discards the error (use with care!)
for _, v := range slice {         // _ discards the index
    process(v)
}
```

### 3.4 Constants

```go
// Constants are computed at compile time — must be computable by the compiler
const Pi = 3.14159265358979323846  // untyped constant — highly flexible
const MaxRetries int = 3           // typed constant

// Constant block
const (
    StatusOK    = 200
    StatusNotFound = 404
    AppName     = "MyApp"
    Version     = "1.0.0"
)

// iota — auto-incrementing integer for enumerations
type Direction int
const (
    North Direction = iota   // 0
    East                     // 1
    South                    // 2
    West                     // 3
)

type ByteSize float64
const (
    _           = iota             // ignore first value by assigning to blank identifier
    KB ByteSize = 1 << (10 * iota) // 1 << 10 = 1024
    MB                             // 1 << 20
    GB                             // 1 << 30
    TB                             // 1 << 40
)

// Untyped constants — more flexible; assume the type context demands
const Big = 1 << 62        // too big for int32, fine as untyped
var i64 int64 = Big        // used as int64: ok
// var i32 int32 = Big     // COMPILE ERROR: overflows int32

// Constants cannot be: addresses, slices, maps, channels, or runtime values
// const now = time.Now()  // COMPILE ERROR: time.Now() is runtime
```

### 3.5 Type Aliases and Defined Types

```go
// Type alias — exactly the same type, just another name
type Celsius = float64          // alias: Celsius IS float64

// Defined type — new distinct type with same underlying type
type Fahrenheit float64         // distinct: cannot mix with float64 without conversion
type Kelvin float64

func celsiusToFahrenheit(c Celsius) Fahrenheit {
    return Fahrenheit(c*9/5 + 32)   // explicit conversion required
}

c := Celsius(100)
f := celsiusToFahrenheit(c)         // Fahrenheit(212)
// var x float64 = f               // COMPILE ERROR: cannot use Fahrenheit as float64

// Why defined types? Type safety: prevents mixing up semantically different values
// e.g., can't accidentally pass Celsius where Fahrenheit is expected

// Methods can be added to defined types:
func (c Celsius) String() string {
    return fmt.Sprintf("%.1f°C", float64(c))
}
fmt.Println(c)  // "100.0°C"
```

### 3.6 Type Conversions

```go
// Go requires explicit type conversions — no implicit widening
var i int = 42
var f float64 = float64(i)   // explicit: int → float64
var u uint = uint(f)         // explicit: float64 → uint (truncates, loses sign)

// String conversions
s1 := string(65)             // "A" — int → string (rune interpretation!)
s2 := fmt.Sprintf("%d", 65)  // "65" — int to decimal string (use this)
s3 := strconv.Itoa(65)       // "65" — int to decimal string (most efficient)

n, err := strconv.Atoi("42") // "42" → 42 with error check
n2, err := strconv.ParseInt("0xFF", 16, 64) // hex to int64

// []byte ↔ string conversions (makes a copy)
b := []byte("hello")         // string → []byte
s4 := string(b)              // []byte → string

// Interface conversions (type assertions — discussed in interfaces chapter)
var v interface{} = "hello"
str, ok := v.(string)        // type assertion with safety check
```

---

## Chapter 4: Operators & Expressions

### 4.1 All Operators

```go
// ── Arithmetic ─────────────────────────────────────────────
a, b := 10, 3
fmt.Println(a + b)   // 13
fmt.Println(a - b)   // 7
fmt.Println(a * b)   // 30
fmt.Println(a / b)   // 3   (integer division: truncates toward zero)
fmt.Println(a % b)   // 1   (modulo)

// Floating point
fmt.Println(10.0 / 3.0)  // 3.3333333333333335
fmt.Println(10 / 3)      // 3 (integer division)
fmt.Println(float64(10) / float64(3))  // 3.3333... (convert first)

// Increment/decrement: STATEMENTS not expressions (can't use in expression)
i := 5
i++          // i = 6  (only postfix; no ++i in Go)
i--          // i = 5
// j := i++ // COMPILE ERROR: i++ is a statement, not expression

// ── Comparison ─────────────────────────────────────────────
fmt.Println(a == b)   // false
fmt.Println(a != b)   // true
fmt.Println(a <  b)   // false
fmt.Println(a >  b)   // true
fmt.Println(a <= b)   // false
fmt.Println(a >= b)   // true

// Structs are comparable if all fields are comparable
type Point struct{ X, Y int }
p1, p2 := Point{1, 2}, Point{1, 2}
fmt.Println(p1 == p2)  // true

// ── Logical ────────────────────────────────────────────────
fmt.Println(true && false)  // false (short-circuit)
fmt.Println(true || false)  // true  (short-circuit)
fmt.Println(!true)          // false

// ── Bitwise ────────────────────────────────────────────────
x := 0b1010  // 10
y := 0b1100  // 12
fmt.Printf("%04b\n", x & y)   // 1000 = 8  (AND)
fmt.Printf("%04b\n", x | y)   // 1110 = 14 (OR)
fmt.Printf("%04b\n", x ^ y)   // 0110 = 6  (XOR)
fmt.Printf("%04b\n", x &^ y)  // 0010 = 2  (AND NOT / bit clear — Go-specific)
fmt.Printf("%04b\n", x << 2)  // 101000 = 40 (left shift)
fmt.Printf("%04b\n", x >> 1)  // 0101 = 5  (right shift)

// ── Assignment ─────────────────────────────────────────────
n := 10
n += 5    // n = 15
n -= 3    // n = 12
n *= 2    // n = 24
n /= 4    // n = 6
n %= 4    // n = 2
n <<= 1   // n = 4
n >>= 1   // n = 2
n &= 3    // n = 2
n |= 8    // n = 10
n ^= 1    // n = 11

// ── Address & Dereference ──────────────────────────────────
val := 42
ptr := &val          // & takes address: ptr is *int
*ptr = 100           // * dereferences: val is now 100
fmt.Println(val)     // 100
```

### 4.2 Operator Precedence

```
Highest → Lowest:
  Unary:           + - ! ^ * & <-
  Multiplicative:  * / % << >> & &^
  Additive:        + - | ^
  Comparison:      == != < <= > >=
  Logical AND:     &&
  Logical OR:      ||

// When in doubt, use parentheses:
result := (a + b) * (c - d)   // clear intent
```

---

## Chapter 5: Control Flow

### 5.1 if / else — No Parentheses, but Braces Required

```go
// Basic if — no parentheses around condition (unlike C/Java)
x := 10
if x > 5 {
    fmt.Println("greater")
} else if x == 5 {
    fmt.Println("equal")
} else {
    fmt.Println("less")
}

// Init statement in if — scopes variable to the if block
// Pattern: declare variable + check error in one line
if err := doSomething(); err != nil {
    fmt.Println("error:", err)
    return
}
// err not accessible here — scope limited to if block

// Very common Go pattern:
if val, ok := myMap[key]; ok {
    fmt.Println("found:", val)
} else {
    fmt.Println("not found")
}

// Braces on same line are REQUIRED by gofmt:
// if x > 5
// {              ← COMPILE ERROR: unexpected newline before {
```

### 5.2 switch — No Fall-through by Default

```go
// switch: cases don't fall through by default (unlike C — no 'break' needed)
day := "Monday"
switch day {
case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday":
    fmt.Println("Weekday")
case "Saturday", "Sunday":
    fmt.Println("Weekend")
default:
    fmt.Println("Unknown")
}

// switch with init statement
switch os := runtime.GOOS; os {
case "darwin": fmt.Println("macOS")
case "linux":  fmt.Println("Linux")
case "windows": fmt.Println("Windows")
default:       fmt.Printf("Other: %s\n", os)
}

// switch with no condition = cleaner if-else chain
score := 75
switch {
case score >= 90: fmt.Println("A")
case score >= 80: fmt.Println("B")
case score >= 70: fmt.Println("C")
default:          fmt.Println("F")
}

// fallthrough: explicitly fall to next case
switch 2 {
case 1:
    fmt.Println("one")
    fallthrough     // falls to case 2
case 2:
    fmt.Println("two")
    fallthrough
case 3:
    fmt.Println("three")  // also prints
case 4:
    fmt.Println("four")   // does NOT print (fallthrough from 3 not specified)
}

// Type switch — interrogate interface values
func describe(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("int: %d\n", v)
    case string:
        fmt.Printf("string: %q\n", v)
    case bool:
        fmt.Printf("bool: %t\n", v)
    case []int:
        fmt.Printf("[]int: %v\n", v)
    default:
        fmt.Printf("unknown type: %T\n", v)
    }
}
```

### 5.3 for — Go's Only Loop

Go has ONE loop keyword: `for`. It covers all loop patterns.

```go
// Pattern 1: Traditional C-style for loop
for i := 0; i < 5; i++ {
    fmt.Println(i)
}

// Pattern 2: while-equivalent (condition only)
n := 1
for n < 100 {
    n *= 2
}

// Pattern 3: infinite loop
for {
    if shouldStop() { break }
    doWork()
}

// Pattern 4: range over slice
nums := []int{2, 3, 5, 7, 11}
for i, v := range nums {
    fmt.Printf("nums[%d] = %d\n", i, v)
}
for _, v := range nums { /* just value */ }
for i := range nums   { /* just index */ }

// Pattern 5: range over map (RANDOM order — never rely on order)
m := map[string]int{"alice": 90, "bob": 85}
for k, v := range m {
    fmt.Printf("%s: %d\n", k, v)
}

// Pattern 6: range over string (iterates RUNES, not bytes)
for i, r := range "Hello, 世界" {
    fmt.Printf("%d: %c\n", i, r)
}

// Pattern 7: range over channel (receive until closed)
ch := make(chan int)
go func() { ch <- 1; ch <- 2; close(ch) }()
for v := range ch {
    fmt.Println(v)  // 1, 2
}

// break and continue
for i := 0; i < 10; i++ {
    if i == 3 { continue }   // skip 3
    if i == 7 { break    }   // stop at 7
    fmt.Println(i)
}

// Labeled break/continue — for nested loops
outer:
for i := 0; i < 3; i++ {
    for j := 0; j < 3; j++ {
        if i == 1 && j == 1 {
            break outer     // exits BOTH loops
        }
        fmt.Printf("(%d,%d) ", i, j)
    }
}
```

### 5.4 defer — Deferred Execution

`defer` schedules a function call to run just before the surrounding function returns. Deferred calls run in **LIFO** (last-in, first-out) order.

```go
func processFile(filename string) error {
    f, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer f.Close()   // guaranteed to run when processFile returns
                      // even if a panic occurs
    
    // process f...
    return nil
}

// LIFO order of deferred calls:
func countdown() {
    for i := 3; i >= 0; i-- {
        defer fmt.Println(i)   // deferred calls stack up
    }
    // When function returns, deferred calls run: 0, 1, 2, 3 (LIFO)
}

// Defer arguments are evaluated IMMEDIATELY (not at call time):
x := 10
defer fmt.Println(x)   // captures x=10 NOW
x = 20
// prints 10 (not 20)

// Named return values + defer for cleanup and modification:
func doTransaction() (err error) {
    tx := beginTransaction()
    defer func() {
        if err != nil {
            tx.Rollback()   // can access named return 'err'
        } else {
            tx.Commit()
        }
    }()
    
    err = executeQuery(tx)
    return   // naked return; defer runs after this
}

// Common patterns:
// 1. Close resources
defer file.Close()
defer conn.Close()
defer resp.Body.Close()

// 2. Unlock mutexes
mu.Lock()
defer mu.Unlock()

// 3. Trace/timing
start := time.Now()
defer func() { fmt.Println("took:", time.Since(start)) }()
```

### 5.5 panic and recover

```go
// panic: signals a programming error that cannot continue safely
// Unlike exceptions, panics are meant for UNRECOVERABLE errors
func divide(a, b int) int {
    if b == 0 {
        panic("division by zero")   // prefer: return error
    }
    return a / b
}

// recover: catch a panic — only useful inside a deferred function
func safeDiv(a, b int) (result int, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("recovered from panic: %v", r)
        }
    }()
    result = divide(a, b)
    return
}

// When to use panic vs error return:
// panic: truly unexpected, unrecoverable programmer mistakes
//        (out-of-bounds access the runtime panics automatically)
// error: expected failure conditions (file not found, network timeout, validation)

// Runtime panics (the most common):
var s []int
_ = s[0]      // panic: runtime error: index out of range [0] with length 0

var p *int
_ = *p        // panic: runtime error: invalid memory address or nil pointer dereference

var m map[string]int
m["key"] = 1  // panic: assignment to entry in nil map
```

---

## Chapter 6: Functions — First-Class Citizens

### 6.1 Function Basics

```go
// Basic function — func keyword, name, params, return type
func add(a, b int) int {
    return a + b
}

// Multiple parameters of same type: shorthand
func addThree(a, b, c int) int {
    return a + b + c
}

// Multiple return values — Go's killer feature for error handling
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

result, err := divide(10, 3)
if err != nil {
    log.Fatal(err)
}
fmt.Println(result)  // 3.3333...

// Named return values — act as pre-declared variables
func minMax(arr []int) (min, max int) {
    min, max = arr[0], arr[0]
    for _, v := range arr[1:] {
        if v < min { min = v }
        if v > max { max = v }
    }
    return   // naked return: returns named values min and max
}

// Variadic functions — variable number of arguments
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)              // 6
sum(1, 2, 3, 4, 5)        // 15
nums := []int{1, 2, 3}
sum(nums...)               // spread a slice with ... operator
```

### 6.2 Functions as Values — First-Class Citizens

```go
// Functions are values — assign to variables, pass as arguments, return them

// Assign to variable
greet := func(name string) string {
    return "Hello, " + name
}
fmt.Println(greet("Alice"))   // "Hello, Alice"

// Function type
type MathFunc func(int, int) int

func apply(f MathFunc, a, b int) int {
    return f(a, b)
}
result := apply(func(a, b int) int { return a * b }, 3, 4)  // 12

// Return a function (higher-order function)
func multiplier(factor int) func(int) int {
    return func(x int) int {
        return x * factor
    }
}
double := multiplier(2)
triple := multiplier(3)
fmt.Println(double(5))  // 10
fmt.Println(triple(5))  // 15

// Closure — inner function captures outer variables
func counter() func() int {
    count := 0
    return func() int {
        count++         // captures and modifies 'count' from outer scope
        return count
    }
}
c1 := counter()
c2 := counter()
fmt.Println(c1())  // 1
fmt.Println(c1())  // 2  — c1 and c2 have SEPARATE 'count' variables
fmt.Println(c2())  // 1
```

### 6.3 Closures — Traps and Best Practices

```go
// ❌ Classic closure bug in loops
funcs := make([]func(), 3)
for i := 0; i < 3; i++ {
    funcs[i] = func() { fmt.Println(i) }  // captures variable 'i', not its value
}
for _, f := range funcs {
    f()  // prints 3, 3, 3 — 'i' is 3 when loop ends, all closures see it
}

// ✅ Fix 1: create a new variable in each iteration
for i := 0; i < 3; i++ {
    i := i  // shadows outer i; creates new variable for each iteration
    funcs[i] = func() { fmt.Println(i) }
}
// prints 0, 1, 2

// ✅ Fix 2: pass as argument
for i := 0; i < 3; i++ {
    funcs[i] = func(i int) func() {   // i is now a parameter, not captured
        return func() { fmt.Println(i) }
    }(i)
}
// prints 0, 1, 2

// Practical closure use cases:
// 1. Middleware / handler factories
func withLogging(handler func(r *Request) error) func(r *Request) error {
    return func(r *Request) error {
        log.Printf("handling request: %s", r.Path)
        err := handler(r)
        log.Printf("done: %v", err)
        return err
    }
}

// 2. Memoization
func memoize(f func(int) int) func(int) int {
    cache := make(map[int]int)
    return func(n int) int {
        if v, ok := cache[n]; ok {
            return v
        }
        result := f(n)
        cache[n] = result
        return result
    }
}
```

### 6.4 init() and blank imports

```go
// Blank import: import for side effects only (init() runs, but package symbols not available)
import _ "github.com/lib/pq"    // registers PostgreSQL driver
import _ "image/png"             // registers PNG decoder

// This is common for database drivers, image decoders, codec registrations
```

---

## Chapter 7: Pointers — Go's Approach

### 7.1 What Pointers Are and Why Go Has Them

A **pointer** holds the memory address of another value. Go has pointers to give you control over whether you're working with a copy or the original value. Unlike C, Go has:
- **Garbage collection** — no manual `free()`, no use-after-free
- **No pointer arithmetic** — can't do `ptr++` (prevents common C bugs)
- **Automatic stack-to-heap promotion** — compiler decides where to allocate

```
Value semantics (copy):                 Pointer semantics (share):
┌─────┐                                ┌─────┐
│  a  │ ← original value               │  a  │ ← original
│ 42  │                                │ 42  │
└─────┘                                └──↑──┘
                                          │
┌─────┐                                ┌──┴──┐
│  b  │ = a  (independent copy)        │  p  │ = &a (pointer to a)
│ 42  │                                │ 0x.. │
└─────┘                                └─────┘
b = 99 → b=99, a still 42             *p = 99 → a is now 99
```

### 7.2 Pointer Operations

```go
// & operator: address-of (create a pointer)
x := 42
p := &x          // p is *int pointing to x
fmt.Println(p)   // 0xc0000b4010 (memory address)
fmt.Println(*p)  // 42 (dereference)

// * operator: dereference (access the value at the address)
*p = 100         // modifies x through p
fmt.Println(x)   // 100

// new() — allocates memory for a zero value, returns a pointer
p2 := new(int)   // *int pointing to allocated zero int
*p2 = 5
fmt.Println(*p2) // 5

// nil pointer
var p3 *int      // nil pointer — points to nothing
fmt.Println(p3)  // <nil>
// *p3            // PANIC: nil pointer dereference

// Pointer to struct
type Point struct{ X, Y int }
pt := &Point{X: 1, Y: 2}    // composite literal with &: creates on heap
pt.X = 10                    // equivalent to (*pt).X = 10; Go does auto-dereference
fmt.Println(pt.X)            // 10

// Pointer equality
a := 1
b := 1
pa := &a
pb := &b
pc := &a
fmt.Println(pa == pb)   // false (different addresses)
fmt.Println(pa == pc)   // true  (same address)
fmt.Println(*pa == *pb) // true  (same value)
```

### 7.3 When to Use Pointers

```go
// 1. Modify the original in a function
func double(n *int) {
    *n *= 2
}
x := 5
double(&x)
fmt.Println(x)  // 10

// WITHOUT pointer: modifies only the copy
func doubleWrong(n int) {
    n *= 2    // modifies local copy only
}
x = 5
doubleWrong(x)
fmt.Println(x)  // still 5

// 2. Avoid copying large structs
type LargeStruct struct {
    Data [1000]int
    // ... many fields
}

// ❌ Copies the entire struct (thousands of bytes) on every call
func processValue(s LargeStruct) { /* ... */ }

// ✅ Only copies an 8-byte pointer
func processPointer(s *LargeStruct) { /* ... */ }

// 3. Represent optional/nullable values
type User struct {
    Name  string
    Email *string  // nil = email not provided
}
email := "alice@example.com"
u := User{Name: "Alice", Email: &email}
// u2 := User{Name: "Bob", Email: nil}  // Bob has no email

// 4. Methods that modify the receiver (covered in methods chapter)

// When NOT to use pointers:
// - Small, immutable values (int, bool, small structs) — copying is cheap
// - When you don't need sharing or mutation — value semantics are clearer
// - Slices, maps, channels — already reference types; don't need pointer to pointer
```

### 7.4 Stack vs Heap — Escape Analysis

```go
// The Go compiler performs "escape analysis" to decide:
// - Does this value live beyond the current function's scope?
// - YES → allocate on HEAP (garbage collected)
// - NO  → allocate on STACK (automatically freed)

func stackAlloc() int {
    x := 42      // x lives only in this function → stack allocated
    return x     // copy of x returned; x disappears
}

func heapAlloc() *int {
    x := 42      // x's address returned → x "escapes" to heap
    return &x    // &x is valid after function returns
}

// You don't need to think about this usually — the compiler handles it
// But know that: new() and &SomeStruct{} often result in heap allocation
// Local variables that don't escape → stack allocation (fast, no GC pressure)

// Check escape analysis:
// go build -gcflags="-m" ./...
```

---

# PART II — COMPOSITE TYPES

---

## Chapter 8: Arrays & Slices — The Workhorse

### 8.1 Arrays — Fixed Size, Value Type

```go
// Array: fixed length, value type (copying copies all elements)
var arr [5]int              // [0 0 0 0 0]
arr[0] = 10
arr[4] = 50

// Array literal
primes := [5]int{2, 3, 5, 7, 11}
colors := [3]string{"red", "green", "blue"}

// Let compiler count the size
auto := [...]int{1, 2, 3, 4, 5}  // [...] = count from literal

// Arrays are VALUE TYPES — assignment copies all elements
a := [3]int{1, 2, 3}
b := a         // b is a COMPLETE INDEPENDENT COPY
b[0] = 99
fmt.Println(a)  // [1 2 3] — unchanged
fmt.Println(b)  // [99 2 3]

// Arrays are comparable (if element type is comparable)
fmt.Println([3]int{1,2,3} == [3]int{1,2,3})  // true

// Length is part of the TYPE: [3]int ≠ [4]int
// This limits usefulness → use slices instead
```

### 8.2 Slices — Dynamic, Reference-Like Views

A slice is a **descriptor** for a contiguous segment of an underlying array. It contains three fields:
- **pointer**: to the start of the data
- **length**: number of elements in the slice  
- **capacity**: number of elements from the pointer to the end of the underlying array

```
underlying array: [0, 1, 2, 3, 4, 5, 6, 7]
                   ↑ ptr
slice s:          ptr=↑, len=5, cap=8
s = [0, 1, 2, 3, 4]

slice t = s[2:5]: ptr=ptr+2, len=3, cap=6
t = [2, 3, 4]

Modifying t[0] ALSO modifies s[2] — they share the same underlying array!
```

```go
// Creating slices
s1 := []int{1, 2, 3, 4, 5}            // slice literal (no size in brackets)
s2 := make([]int, 5)                   // make(type, len): len=5, cap=5, all zeros
s3 := make([]int, 3, 10)              // make(type, len, cap): len=3, cap=10
var s4 []int                           // nil slice: len=0, cap=0, ptr=nil

// nil vs empty slice
fmt.Println(s4 == nil)                 // true
fmt.Println(len(s4) == 0)             // true
s5 := []int{}                          // empty (non-nil) slice
fmt.Println(s5 == nil)                 // false
fmt.Println(len(s5) == 0)             // true

// Both nil and empty slices: len=0, range loops work fine, append works
// Prefer nil slice over empty slice; only use []T{} when nil check matters

// Slicing operations
arr := []int{0, 1, 2, 3, 4, 5, 6, 7}
s := arr[2:5]    // elements [2,3,4]; len=3, cap=6 (from index 2 to end of arr)
s = arr[:3]      // [0,1,2]; from beginning
s = arr[4:]      // [4,5,6,7]; to end
s = arr[:]       // all; s shares arr's memory
s = arr[1:5:7]   // three-index slice: [1:5] with cap limited to 7-1=6
                 // useful to prevent accidentally growing into arr's memory

// Slice shares memory — modification visible in original:
a := []int{1, 2, 3, 4, 5}
b := a[1:4]      // [2, 3, 4]
b[0] = 99        // modifies a[1] as well!
fmt.Println(a)   // [1, 99, 3, 4, 5]

// copy() — make an independent copy
src := []int{1, 2, 3}
dst := make([]int, len(src))
n := copy(dst, src)          // returns number of elements copied
dst[0] = 99
fmt.Println(src)             // [1, 2, 3] — unchanged

// Partial copy
dst2 := make([]int, 2)
copy(dst2, src)              // copies min(len(dst2), len(src)) = 2 elements
fmt.Println(dst2)            // [1, 2]
```

### 8.3 append — Growing Slices

```go
s := []int{1, 2, 3}

// append: may return a new slice if reallocation needed
s = append(s, 4)         // [1, 2, 3, 4]
s = append(s, 5, 6, 7)  // append multiple values
s = append(s, []int{8, 9, 10}...)  // spread another slice

// CRITICAL: always use the return value — original might be a different slice
// The append function returns the (possibly new) slice:
func addElement(s []int, v int) []int {
    return append(s, v)  // correct: return new slice
}
// Never do: append(s, v) without using the result

// Growth strategy:
// When appending beyond capacity: new backing array allocated (roughly doubles)
// Old backing array becomes unreachable → eventually garbage collected

s2 := make([]int, 0, 10)  // pre-size with capacity to avoid reallocation
for i := 0; i < 10; i++ {
    s2 = append(s2, i)    // no reallocation (fits in capacity)
}

// Append to nil slice (works fine):
var s3 []string
s3 = append(s3, "hello")
fmt.Println(s3)  // [hello]

// Patterns:
// Stack: append = push, s[len(s)-1] = peek, s[:len(s)-1] = pop
// Queue: append = enqueue (back), s[0] = front, s[1:] = dequeue
// Delete element i: s = append(s[:i], s[i+1:]...) — O(n), modifies order
// Delete element i (order doesn't matter): s[i] = s[len(s)-1]; s = s[:len(s)-1] — O(1)
// Insert at i: s = append(s[:i+1], s[i:]...); s[i] = newVal
```

### 8.4 Common Slice Patterns

```go
// Filter (doesn't allocate if using append-in-place trick)
func filter(s []int, f func(int) bool) []int {
    result := s[:0]  // reuse backing array
    for _, v := range s {
        if f(v) {
            result = append(result, v)
        }
    }
    return result
}

// Map/transform
func mapSlice(s []int, f func(int) int) []int {
    result := make([]int, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Reduce
func reduce(s []int, initial int, f func(int, int) int) int {
    result := initial
    for _, v := range s {
        result = f(result, v)
    }
    return result
}

// Reverse in-place
func reverse(s []int) {
    for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
        s[i], s[j] = s[j], s[i]
    }
}

// Contains
func contains(s []int, v int) bool {
    for _, x := range s {
        if x == v { return true }
    }
    return false
}

// Deduplicate sorted slice
func dedup(sorted []int) []int {
    result := sorted[:1]
    for _, v := range sorted[1:] {
        if v != result[len(result)-1] {
            result = append(result, v)
        }
    }
    return result
}

// Sort
import "sort"
nums := []int{5, 2, 8, 1, 9}
sort.Ints(nums)                                // ascending
sort.Sort(sort.Reverse(sort.IntSlice(nums)))   // descending

// Sort by custom criteria
type Person struct{ Name string; Age int }
people := []Person{{"Alice", 30}, {"Bob", 25}, {"Carol", 35}}
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})
// or: sort.SliceStable (preserves order of equal elements)
```

---

## Chapter 9: Maps

### 9.1 Maps — Hash Tables

```go
// Map: unordered collection of key-value pairs
// Keys must be comparable (==): all basic types, structs with comparable fields
// Values can be any type

// Creation
m := map[string]int{"alice": 90, "bob": 85, "carol": 92}  // map literal
m2 := make(map[string]int)          // empty map, ready to use
m2 = make(map[string]int, 100)      // with capacity hint (performance)
var m3 map[string]int               // nil map — can read (returns zero) but NOT write!

// ❌ PANIC: assignment to entry in nil map
// m3["key"] = 1

// Write
m["dave"] = 88
m["alice"] = 95     // update existing

// Read
score := m["alice"]           // 95
missing := m["nobody"]        // 0 (zero value for int — NOT an error)

// Read with ok check — distinguish missing from zero value
score, ok := m["alice"]       // score=95, ok=true
score, ok = m["nobody"]       // score=0,  ok=false
if score, ok := m["alice"]; ok {
    fmt.Println("Alice's score:", score)
}

// Delete
delete(m, "bob")
delete(m, "nobody")  // no-op: deleting nonexistent key is safe

// Check if key exists
_, exists := m["alice"]
if exists { /* ... */ }

// Length
fmt.Println(len(m))  // number of key-value pairs (NOT capacity)

// Iteration (random order — do NOT rely on order)
for k, v := range m {
    fmt.Printf("%s: %d\n", k, v)
}
for k := range m { /* keys only */ }

// Maps are reference types — function receives the same map
func addEntry(m map[string]int, key string, val int) {
    m[key] = val   // modifies caller's map (no need for *map)
}
```

### 9.2 Map Patterns

```go
// Count occurrences
func wordCount(text string) map[string]int {
    counts := make(map[string]int)
    for _, word := range strings.Fields(text) {
        counts[word]++   // zero value for int is 0; works on first occurrence
    }
    return counts
}

// Group by (map of slices)
func groupByLength(words []string) map[int][]string {
    groups := make(map[int][]string)
    for _, w := range words {
        groups[len(w)] = append(groups[len(w)], w)
    }
    return groups
}

// Set implementation (map[T]struct{})
// struct{} takes 0 bytes — efficient for sets
type Set map[string]struct{}

func NewSet(items ...string) Set {
    s := make(Set)
    for _, item := range items {
        s[item] = struct{}{}
    }
    return s
}
func (s Set) Contains(item string) bool {
    _, ok := s[item]
    return ok
}
func (s Set) Add(item string) { s[item] = struct{}{} }
func (s Set) Remove(item string) { delete(s, item) }

// Sorted map keys (maps are unordered, but you can sort keys)
keys := make([]string, 0, len(m))
for k := range m {
    keys = append(keys, k)
}
sort.Strings(keys)
for _, k := range keys {
    fmt.Printf("%s: %d\n", k, m[k])
}

// Nested maps
adjacency := map[string]map[string]int{
    "A": {"B": 1, "C": 4},
    "B": {"C": 2, "D": 5},
}
// Access: adjacency["A"]["B"] = 1
// Add edge safely:
if adjacency["X"] == nil {
    adjacency["X"] = make(map[string]int)
}
adjacency["X"]["Y"] = 3

// Thread safety: maps are NOT goroutine-safe
// Use sync.RWMutex or sync.Map for concurrent access (covered later)
```

---

## Chapter 10: Structs

### 10.1 Struct Basics

```go
// Struct: collection of named fields (like a record or class without methods)
type Person struct {
    Name    string
    Age     int
    Email   string
    address string     // unexported: lowercase, package-private
}

// Creating structs
p1 := Person{Name: "Alice", Age: 30, Email: "alice@ex.com"}  // named fields (preferred)
p2 := Person{"Bob", 25, "bob@ex.com", "123 Main St"}         // positional (fragile: order matters)
p3 := Person{Name: "Carol"}                                    // partial: Age=0, Email="", address=""
var p4 Person                                                   // zero value: all fields zeroed

// Accessing fields
fmt.Println(p1.Name)      // "Alice"
p1.Age = 31
fmt.Println(p1.Age)       // 31

// Struct pointer auto-dereference
pp := &p1
pp.Name = "Alicia"        // equivalent to (*pp).Name = "Alicia"

// Anonymous struct (no type name — useful for one-off grouping)
point := struct{ X, Y int }{X: 1, Y: 2}
fmt.Println(point.X, point.Y)

// Struct comparison — if all fields are comparable
type Coord struct{ Lat, Lon float64 }
c1 := Coord{40.7128, -74.0060}
c2 := Coord{40.7128, -74.0060}
fmt.Println(c1 == c2)   // true
```

### 10.2 Struct Embedding — Go's Composition

Go has no inheritance, but **struct embedding** achieves similar code reuse by promoting an embedded type's fields and methods to the outer struct.

```go
type Animal struct {
    Name string
    Age  int
}

func (a Animal) Speak() string {
    return a.Name + " makes a sound"
}

func (a Animal) Describe() string {
    return fmt.Sprintf("%s, age %d", a.Name, a.Age)
}

// Dog EMBEDS Animal — not "inherits from"
type Dog struct {
    Animal              // embedded (anonymous field): type name = field name
    Breed  string
}

func (d Dog) Speak() string {
    return d.Name + " barks: Woof!"   // access embedded field directly
}

d := Dog{
    Animal: Animal{Name: "Rex", Age: 3},
    Breed:  "Labrador",
}

// Promoted fields and methods:
fmt.Println(d.Name)      // "Rex"     — promoted from Animal
fmt.Println(d.Age)       // 3         — promoted from Animal
fmt.Println(d.Describe()) // "Rex, age 3" — promoted from Animal
fmt.Println(d.Speak())   // "Rex barks: Woof!" — Dog.Speak overrides Animal.Speak

// Explicit access through embedded type name
fmt.Println(d.Animal.Speak())  // "Rex makes a sound" — call Animal's version

// Multiple embedding
type Swimmer struct{ Speed float64 }
func (s Swimmer) Swim() string { return "swimming!" }

type Duck struct {
    Animal
    Swimmer
    Color string
}
duck := Duck{Animal: Animal{"Donald", 5}, Swimmer: Swimmer{1.5}, Color: "white"}
fmt.Println(duck.Swim())   // "swimming!" — promoted from Swimmer
fmt.Println(duck.Speak())  // "Donald makes a sound" — from Animal

// Embedding interfaces in structs — embed the interface type
type ReadWriter struct {
    io.Reader   // embedded interface
    io.Writer
}
```

### 10.3 Struct Tags

```go
import "encoding/json"

// Tags: metadata attached to fields (read via reflection)
type User struct {
    ID        int    `json:"id"`
    Username  string `json:"username"`
    Password  string `json:"-"`               // omit from JSON entirely
    Email     string `json:"email,omitempty"` // omit if empty string
    CreatedAt time.Time `json:"created_at"`
    Internal  string `json:"internal" db:"internal_col" validate:"required"`
}

u := User{ID: 1, Username: "alice", Password: "secret", Email: "alice@ex.com"}
jsonBytes, _ := json.Marshal(u)
fmt.Println(string(jsonBytes))
// {"id":1,"username":"alice","created_at":"0001-01-01T00:00:00Z"}
// Note: Password omitted (-), Email omitted (empty + omitempty)

// Decoding
var decoded User
json.Unmarshal(jsonBytes, &decoded)
fmt.Println(decoded.Username)  // "alice"
```

---

## Chapter 11: Methods

### 11.1 Methods — Functions with a Receiver

```go
type Rectangle struct {
    Width, Height float64
}

// Value receiver: method receives a COPY of the struct
// Use when: method doesn't modify struct, or struct is small
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

func (r Rectangle) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}

// Pointer receiver: method receives a POINTER to the struct
// Use when: method modifies the struct, OR struct is large (avoids copying)
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

func (r *Rectangle) String() string {
    return fmt.Sprintf("Rectangle(%.1f × %.1f)", r.Width, r.Height)
}

// Usage
rect := Rectangle{Width: 3, Height: 4}
fmt.Println(rect.Area())       // 12 — value receiver
rect.Scale(2)                  // Go automatically takes &rect for pointer receiver
fmt.Println(rect.Area())       // 48

// Important: be CONSISTENT — all methods should have same receiver type (pointer or value)
// If any method needs a pointer receiver, make ALL methods pointer receivers

// Methods on non-struct types (any named type in the SAME package)
type Duration int64

func (d Duration) Hours() float64 {
    return float64(d) / float64(time.Hour)
}

// Methods on type aliases from other packages — NOT allowed directly
// type MyInt = int
// func (m MyInt) Double() int { return int(m) * 2 }  // COMPILE ERROR
// Must create a named type: type MyInt int
```

### 11.2 Method Sets and Pointer Rules

```go
// Key rule:
// If T has a value receiver method M():
//   - T can call M()
//   - *T can call M() (Go auto-dereferences)

// If *T has a pointer receiver method M():
//   - *T can call M()
//   - T can call M() ONLY IF T is addressable (is a variable, not a temporary)

type Counter struct { n int }
func (c *Counter) Increment() { c.n++ }
func (c Counter)  Value() int  { return c.n }

c := Counter{}         // addressable
c.Increment()          // Go takes &c automatically → (&c).Increment()
fmt.Println(c.Value()) // 1

// Non-addressable: cannot call pointer receiver methods
// Counter{}.Increment()  // COMPILE ERROR: Counter{} is not addressable
// (&Counter{}).Increment() // ok: explicitly take address of composite literal

// Method value: bind a method to a specific receiver instance
inc := c.Increment     // inc is a func() with c bound as receiver
inc()
fmt.Println(c.Value()) // 2

// Method expression: treat method as a function with explicit receiver
incExpr := (*Counter).Increment   // func(*Counter)
incExpr(&c)
fmt.Println(c.Value()) // 3
```

---

## Chapter 12: Interfaces — Go's Superpower

### 12.1 What Interfaces Are — Implicit Satisfaction

In most OO languages (Java, C#), you **declare** that a type implements an interface:
```java
class Dog implements Animal { ... }  // explicit declaration
```

In Go, interfaces are **satisfied implicitly**. If a type has all the methods an interface requires, it automatically satisfies that interface — no `implements` keyword needed.

```go
// Define an interface: set of method signatures
type Animal interface {
    Speak() string
    Move()  string
}

// Dog automatically satisfies Animal (no "implements Animal" declaration)
type Dog struct{ Name string }
func (d Dog) Speak() string { return d.Name + ": Woof!" }
func (d Dog) Move()  string { return d.Name + " runs" }

type Cat struct{ Name string }
func (c Cat) Speak() string { return c.Name + ": Meow!" }
func (c Cat) Move()  string { return c.Name + " slinks" }

type Fish struct{ Name string }
func (f Fish) Speak() string { return f.Name + ": ..." }
func (f Fish) Move()  string { return f.Name + " swims" }

// All three can be used as Animal:
animals := []Animal{Dog{"Rex"}, Cat{"Luna"}, Fish{"Nemo"}}
for _, a := range animals {
    fmt.Println(a.Speak())
    fmt.Println(a.Move())
}

// Power: third-party type can satisfy YOUR interface without modifying it
// If http.ResponseWriter has Write(), it satisfies io.Writer automatically
```

### 12.2 Interface Values — Two Components

```go
// An interface value has two hidden components: (type, value)
// nil interface: both are nil
// non-nil interface: type is set; value might be nil

var a Animal          // a is nil: (nil, nil)
fmt.Println(a == nil) // true

a = Dog{"Rex"}        // a is: (*Dog, Rex) — type is non-nil
fmt.Println(a == nil) // false

// The nil interface trap:
func processAnimal(a Animal) {
    if a == nil {
        fmt.Println("nil animal")
        return
    }
    fmt.Println(a.Speak())
}

var d *Dog    // d is nil (nil pointer to Dog)
// processAnimal(d) — a is (*Dog, nil): type is set, but value is nil!
//                   a == nil is FALSE even though d == nil
// Calling a.Speak() on this would PANIC (nil pointer dereference)

// Fix: check for nil BEFORE assigning to interface
if d != nil {
    processAnimal(d)
}
```

### 12.3 Type Assertion and Type Switch

```go
// Type assertion: extract the concrete value from an interface
var a Animal = Dog{"Rex"}

// Assertion with panic if wrong type:
d := a.(Dog)           // d is Dog{"Rex"}; panics if a is not a Dog

// Safe assertion with ok check (prefer this):
d, ok := a.(Dog)       // ok=true, d=Dog{"Rex"}
c, ok := a.(Cat)       // ok=false, c=Cat{} (zero value)

// Type switch: match against multiple types
func describe(a Animal) {
    switch v := a.(type) {
    case Dog:
        fmt.Printf("It's a dog named %s\n", v.Name)
    case Cat:
        fmt.Printf("It's a cat named %s\n", v.Name)
    case nil:
        fmt.Println("nil animal")
    default:
        fmt.Printf("Unknown animal: %T\n", v)
    }
}
```

### 12.4 Important Standard Interfaces

```go
// io.Reader — any type from which bytes can be read
type Reader interface {
    Read(p []byte) (n int, err error)
}
// Implemented by: os.File, bytes.Buffer, strings.Reader, net.Conn, http.Body, ...

// io.Writer — any type to which bytes can be written
type Writer interface {
    Write(p []byte) (n int, err error)
}
// Implemented by: os.File, os.Stdout, bytes.Buffer, bufio.Writer, ...

// io.ReadWriter — both
type ReadWriter interface {
    Reader
    Writer
}

// fmt.Stringer — controls how a value is printed
type Stringer interface {
    String() string
}
// Implement to customise fmt.Println output for your types

// error — the built-in error interface
type error interface {
    Error() string
}

// sort.Interface — for custom sorting
type Interface interface {
    Len() int
    Less(i, j int) bool
    Swap(i, j int)
}

// Example: implement sort.Interface
type ByAge []Person

func (a ByAge) Len() int           { return len(a) }
func (a ByAge) Less(i, j int) bool { return a[i].Age < a[j].Age }
func (a ByAge) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

people := []Person{{"Alice", 30}, {"Bob", 25}}
sort.Sort(ByAge(people))   // uses ByAge's Less, Len, Swap

// Modern: sort.Slice (no interface needed)
sort.Slice(people, func(i, j int) bool {
    return people[i].Age < people[j].Age
})
```

### 12.5 Designing Interfaces — Go Proverbs

```go
// ① Small interfaces are powerful
// "The bigger the interface, the weaker the abstraction." — Rob Pike

// ❌ Too large — hard to implement, hard to mock
type UserStore interface {
    Create(u User) error
    GetByID(id int) (User, error)
    GetByEmail(email string) (User, error)
    Update(u User) error
    Delete(id int) error
    List(page, size int) ([]User, error)
    Search(query string) ([]User, error)
}

// ✅ Split into focused interfaces
type UserCreator interface {
    Create(u User) error
}
type UserGetter interface {
    GetByID(id int) (User, error)
}
// Functions take only the interface they need:
func sendWelcome(creator UserCreator, u User) error {
    return creator.Create(u)
}

// ② Define interfaces where they're USED, not where they're defined
// In Java: define interfaces in the implementing package
// In Go: define interfaces in the CONSUMING package

// Package db:
type UserRepository struct { db *sql.DB }
func (r *UserRepository) GetByID(id int) (User, error) { ... }

// Package service (defines and uses the interface):
type UserGetter interface {
    GetByID(id int) (User, error)
}
type UserService struct {
    repo UserGetter   // depends on interface, not concrete type
}
// db.UserRepository automatically satisfies UserGetter without knowing about it

// ③ Accept interfaces, return concrete types
func ProcessUsers(getter UserGetter) error { ... }   // flexible input
func NewUserRepository(db *sql.DB) *UserRepository { ... }  // concrete return
```

### 12.6 The Empty Interface — interface{} and any

```go
// interface{} (Go < 1.18) / any (Go 1.18+): satisfied by ALL types
// 'any' is just a type alias for interface{}
var v any = 42
v = "hello"
v = []int{1, 2, 3}
v = nil

// Common uses: containers holding values of different types
func printAll(items ...any) {
    for _, item := range items {
        fmt.Println(item)
    }
}
printAll(42, "hello", true, []int{1,2,3})

// Maps with unknown value type
data := map[string]any{
    "name": "Alice",
    "age":  30,
    "scores": []int{90, 85, 92},
}

// Type assertion is required to use the actual value:
name := data["name"].(string)
age  := data["age"].(int)

// Avoid overusing any — you lose type safety
// Prefer generics (Go 1.18+) for generic algorithms over any
```

---

# PART III — ADVANCED LANGUAGE FEATURES

---

## Chapter 13: Goroutines & Concurrency Model

### 13.1 The Concurrency Philosophy

Go's concurrency model is based on **Communicating Sequential Processes (CSP)**, a mathematical model by Tony Hoare (1978). The Go proverb captures it:

> **"Do not communicate by sharing memory; instead, share memory by communicating."**

Traditional concurrent programming:
```
Thread 1 ──────────────────────────────
                ↕ shared memory + lock
Thread 2 ──────────────────────────────
Problem: deadlocks, race conditions, lock complexity
```

Go's model:
```
Goroutine 1 ──── data ──── Channel ──── data ──── Goroutine 2
Problem: solved — only one goroutine handles the data at a time
```

### 13.2 Goroutines — Lightweight Threads

A **goroutine** is an independently executing function, multiplexed onto OS threads by the Go runtime.

```
OS Thread:   ~1-2 MB stack, OS kernel manages, expensive to create (~10μs)
Goroutine:   ~2-8 KB initial stack (grows as needed), Go runtime manages, cheap (~300ns)
→ You can run millions of goroutines on a handful of OS threads
```

```go
// Start a goroutine with the 'go' keyword
go doSomething()                     // run doSomething() concurrently
go func() { fmt.Println("async") }() // immediately-invoked goroutine

// The launching goroutine does NOT wait for the launched one
func main() {
    go fmt.Println("goroutine")      // might not run before main exits!
    fmt.Println("main")
    // main() exits → all goroutines are KILLED immediately
}

// To wait: use sync.WaitGroup or channels (covered next)
func main() {
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        wg.Add(1)       // increment counter BEFORE starting goroutine
        i := i          // capture loop variable (important!)
        go func() {
            defer wg.Done()  // decrement counter when done
            fmt.Println("goroutine", i)
        }()
    }
    wg.Wait()   // block until all goroutines call Done()
    fmt.Println("all goroutines complete")
}
```

### 13.3 The Go Scheduler — M:N Threading

```
Go uses M:N scheduling: M goroutines onto N OS threads

G = Goroutine (logical thread, managed by Go runtime)
M = Machine (OS thread)
P = Processor (logical CPU — GOMAXPROCS of them)

┌────────────────────────────────────────────────────────────┐
│  Run Queue: [G1] [G2] [G3] [G4] [G5] ...                  │
│                                                             │
│  P1: M1 running G1   P2: M2 running G3   P3: M3 running G5│
└────────────────────────────────────────────────────────────┘

When G1 makes a system call (file I/O):
  M1 blocks, but P1 is handed to M4 (or a new M) → continues running G2, G4
  G1 wakes up → back into run queue
  
This is why goroutines are "cheap for I/O bound work":
  While one goroutine waits, others run on the same OS thread.

GOMAXPROCS: how many P's (logical CPUs to use). Default: runtime.NumCPU()
runtime.GOMAXPROCS(4)  // use 4 OS threads for goroutine scheduling
```

### 13.4 Race Conditions — The Core Danger

```go
// DATA RACE: two goroutines access same memory, at least one writes, no synchronization
// Result: undefined behavior — value might be 1, 2, or something corrupt

counter := 0
for i := 0; i < 1000; i++ {
    go func() {
        counter++    // READ, then WRITE — not atomic! Race condition!
    }()
}
time.Sleep(time.Second)
fmt.Println(counter)  // Might be less than 1000

// Detect races: go run -race main.go (race detector)
// go test -race ./...

// The Go race detector instruments memory accesses.
// Always run tests with -race in CI.
```

---

## Chapter 14: Channels — Communicating Sequential Processes

### 14.1 Channel Fundamentals

A **channel** is a typed conduit through which goroutines send and receive values. The send and receive are the synchronization mechanism.

```go
// Create a channel
ch := make(chan int)          // unbuffered channel
ch2 := make(chan string, 10)  // buffered channel with capacity 10
var ch3 chan int               // nil channel — sends/receives block forever

// Send (blocks until receiver is ready, for unbuffered)
ch <- 42          // send 42

// Receive (blocks until sender sends, for unbuffered)
v := <-ch         // receive into v
v, ok := <-ch     // ok=false if channel is closed and empty

// Close a channel — signals no more values will be sent
close(ch)         // only the SENDER should close; receiving from closed is safe
// Sending to a closed channel: PANIC

// Range over channel — receives until channel is closed
for v := range ch {
    fmt.Println(v)   // blocks until next value or close
}
```

### 14.2 Unbuffered vs Buffered Channels

```go
// UNBUFFERED channel — synchronous, rendezvous point
// Send blocks until receiver is ready. Receive blocks until sender sends.
ch := make(chan int)

go func() {
    fmt.Println("sending 42...")
    ch <- 42             // blocks here until main goroutine receives
    fmt.Println("sent!")
}()

fmt.Println("receiving...")
v := <-ch               // main blocks here until goroutine sends
fmt.Printf("received %d\n", v)

// BUFFERED channel — asynchronous up to capacity
// Send blocks only when buffer is FULL. Receive blocks only when buffer is EMPTY.
ch2 := make(chan string, 3)

ch2 <- "first"    // doesn't block (buffer has room)
ch2 <- "second"   // doesn't block
ch2 <- "third"    // doesn't block
// ch2 <- "fourth" // would BLOCK: buffer full

fmt.Println(<-ch2)  // "first"  — FIFO order
fmt.Println(<-ch2)  // "second"
fmt.Println(<-ch2)  // "third"

// Use buffered channels when:
// - You know the exact number of sends (e.g., fan-out to N workers)
// - You want to decouple producer and consumer speeds
// - Implementing semaphores (limit concurrency)
```

### 14.3 Channel Direction — Restricting Use

```go
// Channel direction in type signatures increases safety
// chan T     — bidirectional (default)
// chan<- T   — send-only
// <-chan T   — receive-only

func producer(ch chan<- int, n int) {   // can only SEND on ch
    for i := 0; i < n; i++ {
        ch <- i
    }
    close(ch)
}

func consumer(ch <-chan int) {          // can only RECEIVE from ch
    for v := range ch {
        fmt.Println("received:", v)
    }
}

func main() {
    ch := make(chan int, 5)  // bidirectional
    go producer(ch, 5)       // ch implicitly converted to chan<- int
    consumer(ch)             // ch implicitly converted to <-chan int
}

// Prevents bugs: can't accidentally close a receive-only channel, etc.
```

### 14.4 select — Multiplexing Channels

```go
// select: like switch but for channel operations
// Waits until one of the cases can proceed, then executes that case
// If multiple are ready: chooses one RANDOMLY

func fanIn(ch1, ch2 <-chan string) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for {
            select {
            case v, ok := <-ch1:
                if !ok { ch1 = nil; continue }  // nil channel never ready
                out <- v
            case v, ok := <-ch2:
                if !ok { ch2 = nil; continue }
                out <- v
            }
            if ch1 == nil && ch2 == nil { return }
        }
    }()
    return out
}

// Non-blocking channel operation with default
func tryReceive(ch <-chan int) (int, bool) {
    select {
    case v := <-ch:
        return v, true    // received a value
    default:
        return 0, false   // channel empty — don't block
    }
}

// Timeout using time.After
func receiveWithTimeout(ch <-chan int, timeout time.Duration) (int, error) {
    select {
    case v := <-ch:
        return v, nil
    case <-time.After(timeout):
        return 0, fmt.Errorf("timeout after %v", timeout)
    }
}

// Done channel — cancellation pattern (before context package)
func doWork(done <-chan struct{}) {
    for {
        select {
        case <-done:
            fmt.Println("shutting down")
            return
        default:
            doOneUnit()
        }
    }
}
```

### 14.5 Pipeline Pattern

```go
// A pipeline is a series of stages connected by channels
// Each stage is a goroutine that receives from upstream and sends downstream

// Stage 1: generate numbers
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            out <- n
        }
    }()
    return out
}

// Stage 2: square each number
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            out <- n * n
        }
    }()
    return out
}

// Stage 3: filter even numbers
func filterEven(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            if n%2 == 0 {
                out <- n
            }
        }
    }()
    return out
}

// Connect stages: generate → square → filter → consume
func main() {
    c := generate(1, 2, 3, 4, 5)
    c = square(c)
    c = filterEven(c)

    for v := range c {
        fmt.Println(v)   // 4, 16  (2²=4, 4²=16)
    }
}
```

### 14.6 Worker Pool Pattern

```go
// Fan-out: distribute work to multiple goroutines
// Fan-in: collect results from multiple goroutines

type Job struct {
    ID    int
    Input string
}

type Result struct {
    JobID  int
    Output string
    Err    error
}

func processJob(job Job) Result {
    // Simulate work
    time.Sleep(10 * time.Millisecond)
    return Result{JobID: job.ID, Output: strings.ToUpper(job.Input)}
}

func workerPool(numWorkers int, jobs <-chan Job) <-chan Result {
    results := make(chan Result, numWorkers)
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {       // workers receive from shared jobs channel
                results <- processJob(job)
            }
        }()
    }

    // Close results when all workers are done
    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}

func main() {
    jobs := make(chan Job, 100)
    results := workerPool(5, jobs)  // 5 concurrent workers

    // Send jobs
    go func() {
        for i, word := range []string{"hello", "world", "foo", "bar", "baz"} {
            jobs <- Job{ID: i, Input: word}
        }
        close(jobs)  // signal no more jobs
    }()

    // Collect results
    for r := range results {
        if r.Err != nil {
            fmt.Printf("job %d failed: %v\n", r.JobID, r.Err)
        } else {
            fmt.Printf("job %d: %s\n", r.JobID, r.Output)
        }
    }
}
```

---

## Chapter 15: The sync Package

### 15.1 sync.Mutex — Mutual Exclusion

```go
import "sync"

// Mutex: only one goroutine can hold the lock at a time
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()         // acquire lock — blocks if another goroutine holds it
    defer c.mu.Unlock() // release lock when function returns (always use defer)
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}

// RWMutex: allows multiple concurrent readers OR one writer
type SafeCache struct {
    mu    sync.RWMutex
    data  map[string]string
}

func (c *SafeCache) Get(key string) (string, bool) {
    c.mu.RLock()         // multiple goroutines can hold RLock simultaneously
    defer c.mu.RUnlock()
    v, ok := c.data[key]
    return v, ok
}

func (c *SafeCache) Set(key, value string) {
    c.mu.Lock()          // exclusive write lock
    defer c.mu.Unlock()
    c.data[key] = value
}

// Good practices:
// 1. Use defer to always unlock
// 2. Keep critical sections short
// 3. Don't copy a mutex — always pass by pointer
// 4. Lock order: always acquire locks in the same order to avoid deadlock
```

### 15.2 sync.WaitGroup — Wait for Multiple Goroutines

```go
var wg sync.WaitGroup

// Start goroutines
for i := 0; i < 10; i++ {
    wg.Add(1)            // BEFORE starting goroutine
    go func(n int) {
        defer wg.Done()  // ALWAYS done with defer
        process(n)
    }(i)
}

wg.Wait()   // blocks until counter reaches 0
fmt.Println("all done")

// Common mistake: wg.Add(1) INSIDE goroutine — race condition!
// The loop might finish and wg.Wait() return before Add() is called
for i := 0; i < 10; i++ {
    go func(n int) {
        wg.Add(1)        // ❌ WRONG: might not be called before Wait()
        defer wg.Done()
        process(n)
    }(i)
}
```

### 15.3 sync.Once — One-time Initialization

```go
// sync.Once: function is called EXACTLY once, even if called from multiple goroutines
// Perfect for lazy initialization of expensive resources

type ExpensiveService struct {
    once   sync.Once
    client *expensiveClient
}

func (s *ExpensiveService) getClient() *expensiveClient {
    s.once.Do(func() {
        s.client = createExpensiveClient()   // called only once, thread-safe
    })
    return s.client
}

// Singleton pattern with sync.Once
var (
    instance *Config
    once     sync.Once
)

func GetConfig() *Config {
    once.Do(func() {
        instance = loadConfig()
    })
    return instance
}
```

### 15.4 sync.Map — Concurrent Safe Map

```go
// sync.Map: concurrent-safe map without explicit locking
// Use when: many goroutines read/write with mostly stable keys

var sm sync.Map

// Store
sm.Store("key", "value")
sm.Store(42, []int{1, 2, 3})   // any key/value types

// Load
if v, ok := sm.Load("key"); ok {
    fmt.Println(v.(string))   // type assertion needed
}

// LoadOrStore: load if exists, else store and return new
actual, loaded := sm.LoadOrStore("key2", "default")
// loaded=false → stored "default"; actual = "default"
// loaded=true  → loaded existing; actual = existing value

// Delete
sm.Delete("key")

// Range: iterate (no guaranteed order)
sm.Range(func(k, v any) bool {
    fmt.Println(k, v)
    return true  // return false to stop iteration
})

// When to prefer sync.Map over map + RWMutex:
// - Many goroutines, keys rarely change (e.g., caches with stable keys)
// - Read-heavy workloads
// For write-heavy or simple cases: map + RWMutex is often simpler and faster
```

### 15.5 sync.Pool — Object Reuse

```go
// sync.Pool: caches reusable objects to reduce GC pressure
// Objects in pool may be collected at any GC cycle

var bufPool = sync.Pool{
    New: func() any {
        return &bytes.Buffer{}  // create new if pool is empty
    },
}

func process(data []byte) {
    buf := bufPool.Get().(*bytes.Buffer)   // borrow from pool
    defer func() {
        buf.Reset()         // clean before returning
        bufPool.Put(buf)    // return to pool
    }()

    buf.Write(data)
    doWorkWith(buf)
}

// Common use: byte buffers, HTTP request contexts, encoding/decoding buffers
```

### 15.6 sync.Cond — Condition Variables

```go
// sync.Cond: goroutine waits for a condition to be true
// Rarely needed (channels usually better), but useful for broadcast patterns

type Queue struct {
    mu    sync.Mutex
    cond  *sync.Cond
    items []int
}

func NewQueue() *Queue {
    q := &Queue{}
    q.cond = sync.NewCond(&q.mu)
    return q
}

func (q *Queue) Put(item int) {
    q.mu.Lock()
    q.items = append(q.items, item)
    q.cond.Signal()   // wake ONE waiting goroutine (Broadcast() wakes all)
    q.mu.Unlock()
}

func (q *Queue) Get() int {
    q.mu.Lock()
    defer q.mu.Unlock()
    for len(q.items) == 0 {
        q.cond.Wait()   // atomically unlock mu and suspend; re-locks on wake
    }
    item := q.items[0]
    q.items = q.items[1:]
    return item
}
```

### 15.7 Atomic Operations

```go
import "sync/atomic"

// atomic: lock-free operations on primitive types (faster than mutex for simple cases)
var counter int64

atomic.AddInt64(&counter, 1)           // atomic increment
atomic.AddInt64(&counter, -1)          // atomic decrement
val := atomic.LoadInt64(&counter)      // atomic read
atomic.StoreInt64(&counter, 42)        // atomic write
old := atomic.SwapInt64(&counter, 100) // atomic swap; returns old value

// CAS: compare-and-swap — used for lock-free algorithms
swapped := atomic.CompareAndSwapInt64(&counter, 42, 43)
// swapped = true if counter was 42 (now 43); false otherwise

// atomic.Value: store/load any type atomically (useful for config hot-reload)
var config atomic.Value
config.Store(NewConfig())              // store
cfg := config.Load().(*Config)        // load (type assertion required)
```

---

## Chapter 16: Error Handling — Go's Philosophy

### 16.1 Errors Are Values

Go's error model is one of its most debated but ultimately powerful features. There are no exceptions — errors are just regular values returned from functions.

```go
// error is a built-in interface:
type error interface {
    Error() string
}

// Convention: return (result, error) — error is ALWAYS the last return value
// nil error = success; non-nil error = failure

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Caller MUST handle the error:
result, err := divide(10, 0)
if err != nil {
    // Handle error: log, return, retry, fallback
    log.Printf("divide failed: %v", err)
    return
}
fmt.Println(result)

// Why not exceptions?
// Exceptions create invisible control flow — any function might "throw"
// With error values: error paths are EXPLICIT in the code
// Easier to trace what can fail and why
```

### 16.2 Creating Errors

```go
// errors.New: simple static error message
err := errors.New("something went wrong")

// fmt.Errorf: formatted error message
err = fmt.Errorf("user %d not found", userID)

// Wrapping errors (Go 1.13+): preserve the error chain
original := errors.New("connection refused")
wrapped := fmt.Errorf("failed to connect to database: %w", original)
// %w creates a wrapped error

// Unwrap: access wrapped errors
errors.Is(wrapped, original)    // true — checks error chain
errors.As(wrapped, &target)     // extract error of specific type

// Custom error types — carry structured information
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: field %q — %s", e.Field, e.Message)
}

func validateAge(age int) error {
    if age < 0 {
        return &ValidationError{Field: "age", Message: "must be non-negative"}
    }
    if age > 150 {
        return &ValidationError{Field: "age", Message: "exceeds maximum"}
    }
    return nil
}

// Using errors.As to get the specific type:
err = validateAge(-1)
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Println("field:", valErr.Field)    // "age"
    fmt.Println("message:", valErr.Message)
}

// Sentinel errors: predefined errors for comparison with errors.Is
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrTimeout      = errors.New("operation timed out")
)

func findUser(id int) (*User, error) {
    if id <= 0 {
        return nil, fmt.Errorf("findUser %d: %w", id, ErrNotFound)
    }
    // ...
}

// Check for specific errors:
_, err = findUser(-1)
if errors.Is(err, ErrNotFound) {
    fmt.Println("user doesn't exist")
}
```

### 16.3 Error Handling Patterns

```go
// Pattern 1: Guard clause — check error and return early
func processUser(id int) (*UserProfile, error) {
    user, err := findUser(id)
    if err != nil {
        return nil, fmt.Errorf("processUser: %w", err)  // wrap with context
    }
    
    profile, err := loadProfile(user)
    if err != nil {
        return nil, fmt.Errorf("processUser: load profile: %w", err)
    }
    
    return profile, nil
}

// Pattern 2: errCheck helper (reduces boilerplate in long function)
func complexOperation() (err error) {
    check := func(e error, msg string) {
        if err == nil && e != nil {
            err = fmt.Errorf("%s: %w", msg, e)
        }
    }
    
    result1, e := step1(); check(e, "step1")
    result2, e := step2(result1); check(e, "step2")
    result3, e := step3(result2); check(e, "step3")
    _ = result3
    return
}

// Pattern 3: error accumulation (all errors, not just first)
type MultiError struct {
    Errors []error
}
func (m *MultiError) Error() string {
    msgs := make([]string, len(m.Errors))
    for i, e := range m.Errors {
        msgs[i] = e.Error()
    }
    return strings.Join(msgs, "; ")
}
func (m *MultiError) Add(err error) { m.Errors = append(m.Errors, err) }
func (m *MultiError) Err() error {
    if len(m.Errors) == 0 { return nil }
    return m
}

// Pattern 4: Retry with exponential backoff
func withRetry(fn func() error, maxAttempts int) error {
    var err error
    for attempt := 0; attempt < maxAttempts; attempt++ {
        err = fn()
        if err == nil { return nil }
        if !isRetryable(err) { return err }
        wait := time.Duration(1<<attempt) * 100 * time.Millisecond
        time.Sleep(wait)
    }
    return fmt.Errorf("failed after %d attempts: %w", maxAttempts, err)
}
```

### 16.4 The errors Package Deep Dive

```go
import "errors"

// errors.Is: checks if ANY error in the chain is the target
// Works across wrapping levels
base := errors.New("base error")
wrapped1 := fmt.Errorf("level 1: %w", base)
wrapped2 := fmt.Errorf("level 2: %w", wrapped1)

errors.Is(wrapped2, base)      // true — checks entire chain
errors.Is(wrapped2, wrapped1)  // true
errors.Is(wrapped2, errors.New("other")) // false

// Custom Is method: control how your error is compared
type TimeoutError struct{ Duration time.Duration }
func (e *TimeoutError) Error() string { return fmt.Sprintf("timeout after %v", e.Duration) }
func (e *TimeoutError) Is(target error) bool {
    _, ok := target.(*TimeoutError)  // match ANY TimeoutError, not just same instance
    return ok
}

// errors.As: extract error of specific type from chain
var timeoutErr *TimeoutError
if errors.As(err, &timeoutErr) {
    fmt.Println("timed out after:", timeoutErr.Duration)
}

// errors.Unwrap: get the wrapped error (one level)
type AppError struct{ Cause error }
func (e *AppError) Error() string  { return "app error: " + e.Cause.Error() }
func (e *AppError) Unwrap() error  { return e.Cause }   // required for errors.Is/As

// errors.Join (Go 1.20+): join multiple errors into one
err1 := errors.New("error 1")
err2 := errors.New("error 2")
combined := errors.Join(err1, err2)
fmt.Println(combined)              // "error 1\nerror 2"
errors.Is(combined, err1)          // true
errors.Is(combined, err2)          // true
```

---

## Chapter 17: Generics (Go 1.18+)

### 17.1 Why Generics Were Added

Before generics, Go code often:
- Used `interface{}` for container types — lost type safety
- Copy-pasted the same algorithm for each type (intSlice, stringSlice, etc.)
- Used `reflect` package — slow and complex

```go
// Before generics: one function per type (or use interface{})
func sumInts(nums []int) int {
    var total int
    for _, n := range nums { total += n }
    return total
}
func sumFloat64s(nums []float64) float64 {
    var total float64
    for _, n := range nums { total += n }
    return total
}

// With generics: one function for all numeric types
func Sum[T int | int32 | int64 | float32 | float64](nums []T) T {
    var total T
    for _, n := range nums { total += n }
    return total
}
Sum([]int{1, 2, 3})          // 6
Sum([]float64{1.1, 2.2})     // 3.3
```

### 17.2 Type Parameters and Constraints

```go
// Generic function: [T constraint] before parameter list
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

Map([]int{1, 2, 3}, func(n int) string { return fmt.Sprintf("%d", n) })
// → []string{"1", "2", "3"}

func Filter[T any](s []T, f func(T) bool) []T {
    var result []T
    for _, v := range s {
        if f(v) { result = append(result, v) }
    }
    return result
}

func Reduce[T, U any](s []T, init U, f func(U, T) U) U {
    result := init
    for _, v := range s { result = f(result, v) }
    return result
}

// Constraints using interfaces
type Number interface {
    int | int8 | int16 | int32 | int64 |
    uint | uint8 | uint16 | uint32 | uint64 |
    float32 | float64
}

func Min[T Number](a, b T) T {
    if a < b { return a }
    return b
}

// Built-in constraints from golang.org/x/exp/constraints (or constraints package):
// constraints.Ordered: types supporting < > <= >=
// constraints.Integer, constraints.Float, constraints.Signed, constraints.Unsigned

import "golang.org/x/exp/constraints"

func MaxSlice[T constraints.Ordered](s []T) T {
    if len(s) == 0 { panic("empty slice") }
    m := s[0]
    for _, v := range s[1:] {
        if v > m { m = v }
    }
    return m
}

// ~ (tilde): includes all types with this underlying type
type Stringer interface {
    ~string   // any type with underlying type string
    String() string
}

type MyString string
func (s MyString) String() string { return string(s) }
// MyString satisfies Stringer (underlying type is string)
```

### 17.3 Generic Data Structures

```go
// Generic Stack
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T)  { s.items = append(s.items, item) }
func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 { return zero, false }
    n := len(s.items) - 1
    item := s.items[n]
    s.items = s.items[:n]
    return item, true
}
func (s *Stack[T]) Peek() (T, bool) {
    var zero T
    if len(s.items) == 0 { return zero, false }
    return s.items[len(s.items)-1], true
}
func (s *Stack[T]) Len() int { return len(s.items) }

// Usage:
intStack := Stack[int]{}
intStack.Push(1); intStack.Push(2)
v, _ := intStack.Pop()  // v = 2, type is int (not interface{})

strStack := Stack[string]{}
strStack.Push("hello")

// Generic Set
type Set[T comparable] map[T]struct{}

func NewSet[T comparable](items ...T) Set[T] {
    s := make(Set[T])
    for _, item := range items { s[item] = struct{}{} }
    return s
}
func (s Set[T]) Add(item T)             { s[item] = struct{}{} }
func (s Set[T]) Contains(item T) bool   { _, ok := s[item]; return ok }
func (s Set[T]) Remove(item T)          { delete(s, item) }
func (s Set[T]) Len() int               { return len(s) }

// Generic Pair/Tuple
type Pair[A, B any] struct{ First A; Second B }
func MakePair[A, B any](a A, b B) Pair[A, B] { return Pair[A, B]{a, b} }
```

### 17.4 When to Use Generics

```go
// ✅ Use generics for:
// - Container/collection data structures (Stack, Queue, Set, Tree)
// - Generic algorithms (Map, Filter, Reduce, Sort)
// - Functions that work on multiple numeric types (Sum, Min, Max)
// - Type-safe wrappers around interface{} / any

// ❌ Don't use generics for:
// - Simple cases where interfaces work fine
// - When concrete types are sufficient
// - Just to avoid code duplication when the code is simple

// Rule of thumb: if you'd use interface{} with type assertions,
// consider generics. If you'd use an interface for polymorphism, 
// keep using interfaces.

// Example where interfaces are better (polymorphism):
type Logger interface { Log(msg string) }
// Many types implement Logger — use interface, not generics

// Example where generics are better (container):
type Option[T any] struct {
    value *T
}
func Some[T any](v T) Option[T] { return Option[T]{value: &v} }
func None[T any]() Option[T]    { return Option[T]{} }
func (o Option[T]) IsPresent() bool { return o.value != nil }
func (o Option[T]) Get() T {
    if o.value == nil { panic("Get on None") }
    return *o.value
}
func (o Option[T]) OrElse(def T) T {
    if o.value == nil { return def }
    return *o.value
}
```

---

## Chapter 18: Packages & Modules

### 18.1 Package Design Principles

```go
// Good package structure:
//   - Small, focused packages (one concept per package)
//   - Avoid circular imports (A imports B, B imports A → compile error)
//   - Package name = directory name (by convention)
//   - Package name should be short, lowercase, no underscores

// ✅ Good package names:
//   http, io, sync, fmt, strings, bytes

// ❌ Bad package names:
//   httputils, myHelpers, io_util, StringUtils

// Package documentation: comment immediately before package declaration
// Package user provides user authentication and management.
package user

// Exported API documentation: comment immediately before exported name
// User represents an authenticated application user.
type User struct { ... }

// NewUser creates a new User with the given username and email.
// Returns an error if username is empty or email is invalid.
func NewUser(username, email string) (*User, error) { ... }
```

### 18.2 The go.mod File and Versioning

```
module github.com/myorg/myapp   ← module path (unique identifier)

go 1.21                         ← minimum Go version required

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/go-sql-driver/mysql v1.7.1
    github.com/stretchr/testify v1.8.4
)

// Versioning follows Semantic Versioning: major.minor.patch
// v1.2.3: breaking API changes = v2, new features = minor, bug fixes = patch
// Import path for v2+: github.com/foo/bar/v2
import "github.com/foo/bar/v2"

// Replace directive: use local version or different source
replace github.com/foo/bar => ../localfoo

// Exclude: avoid a specific bad version
exclude github.com/foo/bar v1.2.3
```

```bash
# Module commands
go mod init github.com/user/repo    # create go.mod
go mod tidy                         # sync go.mod and go.sum with imports
go mod download                     # download modules to local cache
go mod vendor                       # copy dependencies to ./vendor
go list -m all                      # list all dependencies
go list -m -json all                # JSON format
go get github.com/foo/bar@v1.2.3   # add/upgrade specific version
go get github.com/foo/bar@latest   # upgrade to latest
go get github.com/foo/bar@none     # remove dependency
```

### 18.3 Internal Packages

```go
// 'internal' directory: packages only importable by parent tree
// myproject/internal/database — can only be imported by myproject/**

// This prevents external consumers from depending on internal implementation details
// Great for APIs you don't want to commit to publicly

// Example structure:
// myapp/
//   main.go                ← can import myapp/internal/...
//   api/
//     handlers.go          ← can import myapp/internal/...
//   internal/
//     database/
//       db.go              ← only importable within myapp
//     auth/
//       jwt.go             ← only importable within myapp

// Another package: github.com/other/pkg/main.go
// import "myapp/internal/database"  // COMPILE ERROR: cannot access internal package
```

---

# PART IV — STANDARD LIBRARY & PATTERNS

---

## Chapter 19: Essential Standard Library

### 19.1 fmt — Formatting

```go
import "fmt"

// Print functions
fmt.Print("no newline")
fmt.Println("with newline")
fmt.Printf("formatted: %d %.2f %s %v\n", 42, 3.14, "str", anyValue)

// Format verbs:
// %v   — default format (structs: {field1 field2})
// %+v  — struct with field names {Name:Alice Age:30}
// %#v  — Go syntax representation: main.Person{Name:"Alice", Age:30}
// %T   — type: main.Person
// %d   — integer decimal
// %b   — binary
// %o   — octal
// %x   — hex lowercase
// %X   — hex uppercase
// %f   — float: 3.140000
// %.2f — float with 2 decimal places: 3.14
// %e   — scientific: 3.140000e+00
// %s   — string (raw bytes)
// %q   — quoted string: "hello"
// %p   — pointer address: 0xc0000b4010
// %t   — boolean: true/false
// %c   — character (rune)
// Width and padding:
// %5d  — right-aligned in width 5: "   42"
// %-5d — left-aligned in width 5:  "42   "
// %05d — zero-padded: "00042"

// Sprintf: format to string
s := fmt.Sprintf("Hello, %s! You are %d years old.", name, age)

// Fprintf: format to writer
fmt.Fprintf(os.Stderr, "Error: %v\n", err)
fmt.Fprintf(os.Stdout, "Result: %d\n", result)

// Errorf: format to error
err = fmt.Errorf("failed to process user %d: %w", id, cause)

// Sscanf: parse from string
var name string
var age int
fmt.Sscanf("Alice 30", "%s %d", &name, &age)

// Stringer interface: implement String() string for custom formatting
type Point struct{ X, Y int }
func (p Point) String() string { return fmt.Sprintf("(%d, %d)", p.X, p.Y) }
fmt.Println(Point{3, 4})  // "(3, 4)"
```

### 19.2 strings Package

```go
import "strings"

s := "Hello, World!"

strings.Contains(s, "World")          // true
strings.HasPrefix(s, "Hello")         // true
strings.HasSuffix(s, "!")             // true
strings.Count(s, "l")                 // 3
strings.Index(s, "World")             // 7
strings.LastIndex(s, "l")             // 10

strings.ToUpper(s)                    // "HELLO, WORLD!"
strings.ToLower(s)                    // "hello, world!"
strings.Title("hello world")         // "Hello World" (deprecated; use cases.Title)
strings.TrimSpace("  hello  ")       // "hello"
strings.Trim("!!hello!!", "!")       // "hello"
strings.TrimLeft("!!hello!!", "!")   // "hello!!"
strings.TrimRight("!!hello!!", "!")  // "!!hello"
strings.TrimPrefix(s, "Hello, ")     // "World!"
strings.TrimSuffix(s, "!")           // "Hello, World"

strings.Replace(s, "World", "Go", 1)  // "Hello, Go!" (1 replacement)
strings.ReplaceAll(s, "l", "L")       // "HeLLo, WorLd!"

strings.Split("a,b,c", ",")          // ["a", "b", "c"]
strings.SplitN("a,b,c", ",", 2)      // ["a", "b,c"] (max 2 parts)
strings.SplitAfter("a,b,c", ",")     // ["a,", "b,", "c"]
strings.Fields("  foo bar  baz  ")   // ["foo", "bar", "baz"] (any whitespace)

strings.Join([]string{"a","b","c"}, "-")  // "a-b-c"
strings.Repeat("ab", 3)              // "ababab"
strings.EqualFold("Go", "go")        // true (case-insensitive)

// strings.Builder — efficient string building (better than + in loops)
var sb strings.Builder
for i := 0; i < 5; i++ {
    fmt.Fprintf(&sb, "%d ", i)
}
result := sb.String()   // "0 1 2 3 4 "
sb.Reset()              // reuse builder

// strings.Reader — implements io.Reader for a string
reader := strings.NewReader("hello world")
buf := make([]byte, 5)
n, _ := reader.Read(buf)  // reads up to 5 bytes
```

### 19.3 strconv — String Conversions

```go
import "strconv"

// Integer ↔ string
strconv.Itoa(42)                        // "42" (int to ASCII)
n, err := strconv.Atoi("42")           // 42, nil
n, err = strconv.Atoi("abc")           // 0, error

// More control with Parse functions
n64, err := strconv.ParseInt("FF", 16, 64)    // 255, nil (hex, 64-bit)
n64, err = strconv.ParseInt("-42", 10, 64)    // -42 (decimal, 64-bit)
u64, err := strconv.ParseUint("42", 10, 64)   // 42, nil

// Float
f, err := strconv.ParseFloat("3.14", 64)      // 3.14 (64-bit)
s := strconv.FormatFloat(3.14159, 'f', 2, 64) // "3.14" (format, precision, bits)
// format: 'f'=decimal, 'e'=scientific, 'g'=shortest

// Bool
b, err := strconv.ParseBool("true")    // true, nil
b, err = strconv.ParseBool("1")        // true, nil
s2 := strconv.FormatBool(true)         // "true"

// Quote/unquote strings safely
strconv.Quote("hello\nworld")          // `"hello\nworld"`
strconv.Unquote(`"hello\nworld"`)      // "hello\nworld", nil
```

### 19.4 os — Operating System Interface

```go
import "os"

// File operations
f, err := os.Open("file.txt")           // read-only
f, err = os.Create("file.txt")          // create/truncate write
f, err = os.OpenFile("file.txt", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)

// Flags: O_RDONLY, O_WRONLY, O_RDWR, O_APPEND, O_CREATE, O_TRUNC, O_EXCL
// Permissions: 0644 (owner rw, group r, others r)

defer f.Close()
f.Write([]byte("hello"))
f.WriteString("world\n")

buf := make([]byte, 1024)
n, err := f.Read(buf)          // reads up to len(buf) bytes
content, err := io.ReadAll(f)  // read entire file

// Convenience functions (Go 1.16+)
content, err = os.ReadFile("file.txt")                  // read entire file
err = os.WriteFile("file.txt", []byte("data"), 0644)    // write entire file

// File info
info, err := os.Stat("file.txt")
info.Name()     // "file.txt"
info.Size()     // bytes
info.Mode()     // permissions
info.ModTime()  // last modified
info.IsDir()    // false

// Directory operations
err = os.Mkdir("mydir", 0755)           // create directory
err = os.MkdirAll("a/b/c", 0755)       // create all parents
err = os.Remove("file.txt")             // delete file or empty dir
err = os.RemoveAll("mydir")             // delete directory tree
err = os.Rename("old.txt", "new.txt")  // rename/move
entries, err := os.ReadDir(".")         // list directory
for _, e := range entries {
    fmt.Println(e.Name(), e.IsDir())
}

// Environment
os.Getenv("HOME")                       // get env var ("" if not set)
os.Setenv("MY_VAR", "value")           // set env var
os.Unsetenv("MY_VAR")                  // remove env var
os.Environ()                            // all env vars as []string
os.LookupEnv("HOME")                   // (value, exists bool)

// Process
os.Args                                 // command-line args (os.Args[0] = program)
os.Exit(0)                              // exit with code 0 (success) or 1 (failure)
os.Getpid()                             // current process ID
os.Hostname()                           // (hostname, err)
os.Getwd()                              // current working directory
os.Chdir("/tmp")                        // change working directory
```

### 19.5 io — I/O Primitives

```go
import "io"

// Core interfaces
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }
type ReadCloser interface { Reader; Closer }
type WriteCloser interface { Writer; Closer }
type ReadWriter interface { Reader; Writer }
type ReadWriteCloser interface { Reader; Writer; Closer }
type ReadSeeker interface { Reader; Seeker }

// Seeker: position control
type Seeker interface {
    Seek(offset int64, whence int) (int64, error)
    // whence: io.SeekStart, io.SeekCurrent, io.SeekEnd
}

// Common io functions
data, err := io.ReadAll(r)                    // read everything from Reader
n, err := io.Copy(dst, src)                  // copy from Reader to Writer
n, err = io.CopyN(dst, src, 1024)            // copy exactly n bytes
n, err = io.WriteString(w, "hello")          // write string to Writer
r = io.LimitReader(r, 1024)                  // limit reads to 1024 bytes
r = io.MultiReader(r1, r2, r3)               // concatenate readers
w = io.MultiWriter(w1, w2, w3)               // write to multiple writers
r2, w2 := io.Pipe()                          // synchronous in-memory pipe

// Discard writer (like /dev/null)
io.Copy(io.Discard, resp.Body)               // drain and discard HTTP body

// EOF handling
buf := make([]byte, 10)
for {
    n, err := r.Read(buf)
    if n > 0 { process(buf[:n]) }
    if err == io.EOF { break }       // normal end of stream
    if err != nil { log.Fatal(err) } // real error
}
```

### 19.6 bufio — Buffered I/O

```go
import "bufio"

// bufio.Reader — buffered reading (reduces system calls)
br := bufio.NewReader(r)
br = bufio.NewReaderSize(r, 65536)   // custom buffer size

line, err := br.ReadString('\n')     // read until delimiter (inclusive)
line, isPrefix, err := br.ReadLine() // read one line (without \n)
line2, err := br.ReadBytes('\n')     // []byte version
r.UnreadByte()                       // push last byte back

// Most common: bufio.Scanner — line-by-line reading
scanner := bufio.NewScanner(r)
scanner.Buffer(make([]byte, 1024*1024), 1024*1024)  // increase max line size if needed
for scanner.Scan() {
    line := scanner.Text()    // or scanner.Bytes() for []byte
    process(line)
}
if err := scanner.Err(); err != nil {
    log.Fatal(err)
}

// Custom split function
scanner2 := bufio.NewScanner(r)
scanner2.Split(bufio.ScanWords)    // split by words (default: ScanLines)
// ScanLines, ScanWords, ScanBytes, ScanRunes, or custom func

// bufio.Writer — buffered writing (batch writes)
bw := bufio.NewWriter(w)
bw.WriteString("hello ")
bw.WriteString("world\n")
bw.Flush()   // MUST flush to actually write buffered data

// bufio.ReadWriter — both
brw := bufio.NewReadWriter(br, bw)
```

### 19.7 time Package

```go
import "time"

// Current time
now := time.Now()             // time.Time (local timezone)
utc := time.Now().UTC()       // UTC

// Creating times
t := time.Date(2024, time.March, 15, 10, 30, 0, 0, time.UTC)
t2 := time.Unix(1700000000, 0)   // from Unix timestamp

// Formatting — using a reference time (Mon Jan 2 15:04:05 MST 2006)
// The reference time is a specific moment: 01/02 03:04:05PM '06 -0700
s := now.Format("2006-01-02 15:04:05")     // "2024-03-15 10:30:00"
s = now.Format(time.RFC3339)               // "2024-03-15T10:30:00Z"
s = now.Format(time.RFC1123)               // "Fri, 15 Mar 2024 10:30:00 UTC"

// Parsing
t3, err := time.Parse("2006-01-02", "2024-03-15")
t4, err := time.Parse(time.RFC3339, "2024-03-15T10:30:00Z")

// Duration
d := 2*time.Hour + 30*time.Minute + 15*time.Second
fmt.Println(d)                // "2h30m15s"
d.Seconds()                  // 9015.0
d.Minutes()                  // 150.25
d.Hours()                    // 2.504166...

// Arithmetic
tomorrow := now.Add(24 * time.Hour)
yesterday := now.Add(-24 * time.Hour)
diff := tomorrow.Sub(yesterday)   // time.Duration between two times
now.Before(tomorrow)              // true
now.After(yesterday)              // true
now.Equal(now)                    // true

// Sleep and Timer
time.Sleep(100 * time.Millisecond)

timer := time.NewTimer(5 * time.Second)
<-timer.C                          // blocks for 5 seconds
timer.Stop()                       // cancel before firing

ticker := time.NewTicker(1 * time.Second)
for range ticker.C {              // fires every 1 second
    doPeriodicWork()
}
ticker.Stop()

// time.After — one-shot timer channel
select {
case <-time.After(5 * time.Second):
    fmt.Println("timeout")
case result := <-workChan:
    fmt.Println("got result:", result)
}

// Monotonic clock (for measuring elapsed time — not wall clock)
start := time.Now()
doWork()
elapsed := time.Since(start)   // time.Duration elapsed
fmt.Printf("took %v\n", elapsed)
```

### 19.8 math & math/rand

```go
import (
    "math"
    "math/rand"
    "math/rand/v2"   // Go 1.22+ improved API
)

// math package
math.Abs(-5.0)         // 5.0
math.Sqrt(16.0)        // 4.0
math.Pow(2, 10)        // 1024.0
math.Floor(3.7)        // 3.0
math.Ceil(3.2)         // 4.0
math.Round(3.5)        // 4.0
math.Max(3.0, 5.0)     // 5.0
math.Min(3.0, 5.0)     // 3.0
math.Log(math.E)       // 1.0 (natural log)
math.Log2(1024)        // 10.0
math.Log10(1000)       // 3.0
math.Sin(math.Pi/2)    // 1.0
math.Inf(1)            // +Inf
math.IsInf(x, 1)       // true if x is positive infinity
math.IsNaN(x)          // true if x is not a number
math.MaxFloat64        // largest float64
math.MaxInt            // largest int (platform-dependent)
math.MaxInt64          // 9223372036854775807

// math/rand (pseudorandom)
r := rand.New(rand.NewSource(time.Now().UnixNano()))  // seeded RNG
r.Intn(100)            // [0, 100)
r.Float64()            // [0.0, 1.0)
r.Shuffle(n, func(i, j int) { s[i], s[j] = s[j], s[i] })  // shuffle slice
r.Perm(10)             // random permutation [0,10)

// math/rand/v2 (Go 1.22+) — automatically seeded, cleaner API
rand.IntN(100)          // [0, 100) — global, automatically seeded
rand.Float64()          // [0.0, 1.0)
```

---

## Chapter 20: Testing in Go

### 20.1 Writing Tests

```go
// File: math_test.go (must end in _test.go)
// Package: same as production code (white-box) or packagename_test (black-box)
package math

import (
    "testing"
    "fmt"
)

// Test functions: func TestXxx(t *testing.T)
// 'Xxx' must not start with lowercase letter
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2,3) = %d, want 5", result)
    }
}

// t.Error / t.Errorf: mark test failed but continue
// t.Fatal / t.Fatalf: mark test failed and stop immediately
// t.Log / t.Logf:   print (only visible with -v flag)
// t.Skip / t.Skipf: skip the test

func TestDivide(t *testing.T) {
    // Table-driven tests — idiomatic Go testing
    tests := []struct {
        name     string
        a, b     float64
        expected float64
        wantErr  bool
    }{
        {"positive", 10, 2, 5, false},
        {"negative", -10, 2, -5, false},
        {"zero divisor", 10, 0, 0, true},
        {"both zero", 0, 0, 0, true},
        {"fraction", 7, 2, 3.5, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {   // subtests
            result, err := Divide(tt.a, tt.b)
            if (err != nil) != tt.wantErr {
                t.Errorf("Divide(%v, %v) error = %v, wantErr %v",
                    tt.a, tt.b, err, tt.wantErr)
                return
            }
            if !tt.wantErr && result != tt.expected {
                t.Errorf("Divide(%v, %v) = %v, want %v",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// Testing with testify (popular testing library)
import "github.com/stretchr/testify/assert"
import "github.com/stretchr/testify/require"

func TestWithTestify(t *testing.T) {
    result, err := Divide(10, 2)
    require.NoError(t, err)          // fatal if error
    assert.Equal(t, 5.0, result)     // non-fatal assertion
    assert.InDelta(t, 5.0, result, 0.001)  // floating point comparison
}
```

### 20.2 Benchmarks and Examples

```go
// Benchmark functions: func BenchmarkXxx(b *testing.B)
func BenchmarkSort(b *testing.B) {
    data := generateLargeSlice(1000)
    
    b.ResetTimer()     // exclude setup time from benchmark
    for i := 0; i < b.N; i++ {    // b.N adjusted by testing framework
        dataCopy := make([]int, len(data))
        copy(dataCopy, data)
        sort.Ints(dataCopy)
    }
}

// Compare two implementations:
func BenchmarkSortInts(b *testing.B) { /* ... */ }
func BenchmarkSortReflect(b *testing.B) { /* ... */ }

// Run: go test -bench=. -benchmem -benchtime=5s ./...
// -bench=.:    run all benchmarks
// -benchmem:   include memory allocation stats
// -benchtime:  how long to run each benchmark
// -count=5:    run each 5 times

// Example functions: documentation + test (must print exact output)
func ExampleAdd() {
    fmt.Println(Add(2, 3))
    // Output:
    // 5
}
```

### 20.3 Test Helpers and Fakes

```go
// Helper functions — call t.Helper() so failure line points to caller
func assertEqual(t *testing.T, got, want int) {
    t.Helper()
    if got != want {
        t.Errorf("got %d, want %d", got, want)
    }
}

// TestMain — setup/teardown for entire package
func TestMain(m *testing.M) {
    // Setup
    db := setupTestDatabase()
    
    // Run all tests
    code := m.Run()
    
    // Teardown
    db.Close()
    
    os.Exit(code)
}

// Fake implementations for testing (prefer over mocks)
type FakeUserStore struct {
    users map[int]*User
}

func NewFakeUserStore() *FakeUserStore {
    return &FakeUserStore{users: make(map[int]*User)}
}

func (f *FakeUserStore) GetByID(id int) (*User, error) {
    u, ok := f.users[id]
    if !ok { return nil, ErrNotFound }
    return u, nil
}

func (f *FakeUserStore) Create(u *User) error {
    f.users[u.ID] = u
    return nil
}

func TestUserService(t *testing.T) {
    store := NewFakeUserStore()
    store.users[1] = &User{ID: 1, Name: "Alice"}
    
    svc := NewUserService(store)
    user, err := svc.GetUser(1)
    // assertions...
}

// t.TempDir() — creates temporary directory cleaned up after test
func TestFileProcessing(t *testing.T) {
    dir := t.TempDir()   // automatically deleted when test finishes
    file := filepath.Join(dir, "test.txt")
    os.WriteFile(file, []byte("test data"), 0644)
    
    result, err := processFile(file)
    // assertions...
}

// t.Cleanup() — register cleanup function
func TestWithCleanup(t *testing.T) {
    conn := openConnection()
    t.Cleanup(func() { conn.Close() })  // runs after test, even on failure
    // test code...
}
```

### 20.4 Race Detection and Coverage

```bash
# Run with race detector (always do this in CI!)
go test -race ./...

# Code coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out     # visualize in browser
go tool cover -func=coverage.out     # function-level coverage stats

# Test specific function
go test -run TestDivide ./...
go test -run TestDivide/zero         # run specific subtest

# Verbose output
go test -v ./...

# Test timeout
go test -timeout 30s ./...

# Short mode: skip slow tests
func TestSlow(t *testing.T) {
    if testing.Short() { t.Skip("skipping in short mode") }
    // slow test...
}
go test -short ./...
```

---

## Chapter 21: HTTP & REST with net/http

### 21.1 HTTP Server

```go
import "net/http"

// Simple handler function
func helloHandler(w http.ResponseWriter, r *http.Request) {
    // r: *http.Request — incoming request
    // w: http.ResponseWriter — outgoing response
    
    // Read request
    fmt.Println("Method:", r.Method)
    fmt.Println("URL:", r.URL.Path)
    fmt.Println("Query:", r.URL.Query().Get("name"))
    
    // Read body
    body, err := io.ReadAll(r.Body)
    defer r.Body.Close()
    
    // Headers
    r.Header.Get("Authorization")
    r.Header.Get("Content-Type")
    
    // Path variables (with Go 1.22 enhanced routing)
    id := r.PathValue("id")   // Go 1.22+
    
    // Write response
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("X-Custom", "value")
    w.WriteHeader(http.StatusOK)   // must set before writing body
    fmt.Fprintf(w, `{"message": "hello"}`)
}

// ServeMux (router) — Go 1.22 enhanced routing
mux := http.NewServeMux()
mux.HandleFunc("GET /", helloHandler)
mux.HandleFunc("GET /users/{id}", getUserHandler)      // {id} path variable
mux.HandleFunc("POST /users", createUserHandler)
mux.HandleFunc("PUT /users/{id}", updateUserHandler)
mux.HandleFunc("DELETE /users/{id}", deleteUserHandler)
mux.HandleFunc("GET /users/{id}/posts/{postId}", getPostHandler)

// Serve static files
mux.Handle("GET /static/", http.StripPrefix("/static/", http.FileServer(http.Dir("./static"))))

// Start server
server := &http.Server{
    Addr:         ":8080",
    Handler:      mux,
    ReadTimeout:  15 * time.Second,
    WriteTimeout: 15 * time.Second,
    IdleTimeout:  60 * time.Second,
}
log.Printf("starting server on :8080")
if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
    log.Fatal(err)
}
```

### 21.2 Middleware Pattern

```go
// Middleware: wraps a handler to add cross-cutting behavior
type Middleware func(http.Handler) http.Handler

func Logging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        // Pre-processing
        log.Printf("→ %s %s", r.Method, r.URL.Path)
        
        next.ServeHTTP(w, r)   // call the next handler
        
        // Post-processing
        log.Printf("← %s %s (%v)", r.Method, r.URL.Path, time.Since(start))
    })
}

func Auth(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if !isValidToken(token) {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return   // don't call next
        }
        next.ServeHTTP(w, r)
    })
}

func CORS(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusOK)
            return
        }
        next.ServeHTTP(w, r)
    })
}

// Chain middleware
func chain(h http.Handler, middlewares ...Middleware) http.Handler {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}

// Usage
mux.Handle("/api/", chain(apiHandler, Logging, Auth, CORS))
```

### 21.3 JSON Handling

```go
import "encoding/json"

// Struct for JSON
type User struct {
    ID        int       `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email,omitempty"`
    CreatedAt time.Time `json:"created_at"`
    Internal  string    `json:"-"`          // excluded from JSON
}

// Encode: struct → JSON
user := User{ID: 1, Name: "Alice", Email: "alice@ex.com"}
data, err := json.Marshal(user)
// data = []byte(`{"id":1,"name":"Alice","email":"alice@ex.com","created_at":"0001-..."}`)

// Pretty print
data, err = json.MarshalIndent(user, "", "  ")

// Write JSON response
func jsonResponse(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(v); err != nil {
        log.Printf("json encode error: %v", err)
    }
}

// Decode: JSON → struct
body, _ := io.ReadAll(r.Body)
var user User
if err := json.Unmarshal(body, &user); err != nil {
    http.Error(w, "invalid json", http.StatusBadRequest)
    return
}

// Streaming decode (more efficient for large JSON)
if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
    http.Error(w, "invalid json", http.StatusBadRequest)
    return
}

// Decode into map (unknown structure)
var data map[string]any
json.Unmarshal(body, &data)
name, ok := data["name"].(string)

// Custom marshal/unmarshal
type Money struct {
    Amount   int64  // stored in cents
    Currency string
}

func (m Money) MarshalJSON() ([]byte, error) {
    return json.Marshal(struct {
        Amount   float64 `json:"amount"`
        Currency string  `json:"currency"`
    }{float64(m.Amount) / 100, m.Currency})
}

func (m *Money) UnmarshalJSON(data []byte) error {
    var tmp struct {
        Amount   float64 `json:"amount"`
        Currency string  `json:"currency"`
    }
    if err := json.Unmarshal(data, &tmp); err != nil {
        return err
    }
    m.Amount = int64(tmp.Amount * 100)
    m.Currency = tmp.Currency
    return nil
}
```

### 21.4 HTTP Client

```go
import "net/http"

// Simple GET
resp, err := http.Get("https://api.example.com/users")
if err != nil { log.Fatal(err) }
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    log.Fatalf("unexpected status: %s", resp.Status)
}

var users []User
json.NewDecoder(resp.Body).Decode(&users)

// Configured client (don't use http.DefaultClient in production)
client := &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
        TLSHandshakeTimeout: 10 * time.Second,
    },
}

// POST with JSON body
user := User{Name: "Alice", Email: "alice@example.com"}
body, _ := json.Marshal(user)

req, err := http.NewRequestWithContext(ctx, http.MethodPost,
    "https://api.example.com/users", bytes.NewBuffer(body))
if err != nil { log.Fatal(err) }

req.Header.Set("Content-Type", "application/json")
req.Header.Set("Authorization", "Bearer " + token)

resp, err = client.Do(req)
if err != nil { log.Fatal(err) }
defer resp.Body.Close()

// Parse response
var created User
json.NewDecoder(resp.Body).Decode(&created)
```

---

## Chapter 22: Context — Deadlines & Cancellation

### 22.1 Why Context Exists

```
Problem: request comes in → spawns goroutines → user cancels or timeout occurs
         How do you stop all running goroutines?

Before context: messy, error-prone cancellation channels
With context:   clean, composable cancellation propagation

context.Context: carries deadlines, cancellation signals, and request-scoped values
```

```go
import "context"

// Creating contexts
ctx := context.Background()              // root context — never cancelled
ctx = context.TODO()                     // placeholder when context type is unclear

// With cancellation
ctx, cancel := context.WithCancel(ctx)
defer cancel()                           // always call cancel to free resources
// cancel() can be called multiple times safely

// With timeout (automatic cancellation after duration)
ctx, cancel = context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// With deadline (specific time)
ctx, cancel = context.WithDeadline(ctx, time.Now().Add(5*time.Second))
defer cancel()

// With value (request-scoped data — use sparingly)
type contextKey string
const userIDKey contextKey = "userID"

ctx = context.WithValue(ctx, userIDKey, 42)
userID := ctx.Value(userIDKey).(int)     // type assertion required
```

### 22.2 Using Context in Functions

```go
// Convention: context is always the FIRST parameter
func fetchUser(ctx context.Context, userID int) (*User, error) {
    // Check if context is already cancelled
    select {
    case <-ctx.Done():
        return nil, ctx.Err()   // context.DeadlineExceeded or context.Canceled
    default:
    }
    
    // Pass context to downstream calls
    req, err := http.NewRequestWithContext(ctx, http.MethodGet,
        fmt.Sprintf("https://api.example.com/users/%d", userID), nil)
    if err != nil { return nil, err }
    
    resp, err := http.DefaultClient.Do(req)   // cancelled if ctx is done
    if err != nil { return nil, err }
    defer resp.Body.Close()
    
    var user User
    return &user, json.NewDecoder(resp.Body).Decode(&user)
}

// Cancel multiple goroutines
func doWorkWithCancellation(ctx context.Context) error {
    ctx, cancel := context.WithCancel(ctx)
    defer cancel()  // cancel all children when this function returns

    errCh := make(chan error, 3)
    
    go func() { errCh <- fetchFromDB(ctx) }()
    go func() { errCh <- fetchFromCache(ctx) }()
    go func() { errCh <- fetchFromAPI(ctx) }()

    for i := 0; i < 3; i++ {
        if err := <-errCh; err != nil {
            cancel()  // cancel siblings on first error
            return err
        }
    }
    return nil
}

// HTTP handler with context
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()   // request context — cancelled when client disconnects
    
    user, err := fetchUser(ctx, 42)
    if err != nil {
        if errors.Is(err, context.Canceled) {
            // Client disconnected — no need to respond
            return
        }
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    json.NewEncoder(w).Encode(user)
}
```

---

## Chapter 23: Common Go Patterns

### 23.1 Functional Options Pattern

```go
// Problem: functions with many optional parameters
// Bad: Server(host, port, timeout, maxConns, tls, certFile, ...) — unreadable
// Bad: configuration struct — all fields visible, order matters
// Good: functional options

type Server struct {
    host     string
    port     int
    timeout  time.Duration
    maxConns int
    tls      bool
}

type Option func(*Server)   // function that modifies Server

// Option constructors
func WithHost(host string) Option {
    return func(s *Server) { s.host = host }
}
func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}
func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}
func WithMaxConns(n int) Option {
    return func(s *Server) { s.maxConns = n }
}
func WithTLS() Option {
    return func(s *Server) { s.tls = true }
}

// Constructor with defaults + apply options
func NewServer(options ...Option) *Server {
    s := &Server{
        host:     "localhost",    // sensible defaults
        port:     8080,
        timeout:  30 * time.Second,
        maxConns: 100,
    }
    for _, opt := range options {
        opt(s)
    }
    return s
}

// Clean, self-documenting usage:
s := NewServer(
    WithPort(9090),
    WithTimeout(1 * time.Minute),
    WithTLS(),
)
```

### 23.2 The Builder Pattern

```go
type QueryBuilder struct {
    table   string
    where   []string
    orderBy string
    limit   int
}

func NewQuery(table string) *QueryBuilder {
    return &QueryBuilder{table: table, limit: -1}
}

func (q *QueryBuilder) Where(condition string) *QueryBuilder {
    q.where = append(q.where, condition)
    return q   // return self for chaining
}

func (q *QueryBuilder) OrderBy(field string) *QueryBuilder {
    q.orderBy = field
    return q
}

func (q *QueryBuilder) Limit(n int) *QueryBuilder {
    q.limit = n
    return q
}

func (q *QueryBuilder) Build() string {
    sql := "SELECT * FROM " + q.table
    if len(q.where) > 0 {
        sql += " WHERE " + strings.Join(q.where, " AND ")
    }
    if q.orderBy != "" {
        sql += " ORDER BY " + q.orderBy
    }
    if q.limit > 0 {
        sql += fmt.Sprintf(" LIMIT %d", q.limit)
    }
    return sql
}

// Fluent API:
sql := NewQuery("users").
    Where("active = true").
    Where("age >= 18").
    OrderBy("name ASC").
    Limit(20).
    Build()
```

### 23.3 The Result Pattern (Like Rust's Result)

```go
// For APIs where errors are expected and the caller always handles them
type Result[T any] struct {
    value T
    err   error
}

func Ok[T any](v T) Result[T]    { return Result[T]{value: v} }
func Err[T any](e error) Result[T] { return Result[T]{err: e} }

func (r Result[T]) IsOk() bool          { return r.err == nil }
func (r Result[T]) Value() T            { return r.value }
func (r Result[T]) Error() error        { return r.err }
func (r Result[T]) Unwrap() T {
    if r.err != nil { panic(r.err) }
    return r.value
}
func (r Result[T]) UnwrapOr(def T) T {
    if r.err != nil { return def }
    return r.value
}
```

### 23.4 Graceful Shutdown

```go
// Handle OS signals for graceful shutdown
func runServer() {
    server := &http.Server{Addr: ":8080", Handler: mux}

    // Channel to receive OS signals
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    // Start server in goroutine
    go func() {
        if err := server.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()
    log.Println("server started on :8080")

    // Block until signal received
    <-quit
    log.Println("shutdown signal received")

    // Give server 30 seconds to finish ongoing requests
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Printf("forced shutdown: %v", err)
    }
    log.Println("server stopped cleanly")
}
```

---

## Chapter 24: Performance & Profiling

### 24.1 Profiling Tools

```bash
# CPU profiling
go test -bench=. -cpuprofile=cpu.pprof ./...
go tool pprof cpu.pprof           # interactive CLI
go tool pprof -http=:8090 cpu.pprof  # web UI

# Memory profiling
go test -bench=. -memprofile=mem.pprof ./...
go tool pprof -alloc_space mem.pprof

# Block profiling (goroutine blocking)
go test -bench=. -blockprofile=block.pprof ./...

# Trace (timeline of goroutines)
go test -trace=trace.out ./...
go tool trace trace.out

# Escape analysis (see what goes to heap)
go build -gcflags="-m" ./...
```

```go
// Add profiling endpoints to running server
import _ "net/http/pprof"   // blank import registers /debug/pprof endpoints

// Access: http://localhost:8080/debug/pprof/
// Then: go tool pprof http://localhost:8080/debug/pprof/heap
```

### 24.2 Common Performance Patterns

```go
// 1. Pre-size slices and maps
result := make([]int, 0, expectedLen)  // avoid repeated reallocation
cache  := make(map[string]int, 1000)  // avoid resize

// 2. sync.Pool for frequently allocated objects
var pool = sync.Pool{New: func() any { return new(bytes.Buffer) }}
buf := pool.Get().(*bytes.Buffer)
buf.Reset()
defer pool.Put(buf)

// 3. Avoid string concatenation in loops (use strings.Builder)
var sb strings.Builder
sb.Grow(estimatedSize)
for _, s := range strs { sb.WriteString(s) }
result := sb.String()

// 4. Avoid unnecessary allocations in hot paths
// ❌ Allocates every call
func process(s string) { work([]byte(s)) }
// ✅ Accept []byte directly
func process(b []byte) { work(b) }

// 5. Use goroutines for I/O parallelism
var wg sync.WaitGroup
results := make([]Result, len(items))
for i, item := range items {
    wg.Add(1)
    go func(i int, item Item) {
        defer wg.Done()
        results[i] = fetch(item)
    }(i, item)
}
wg.Wait()

// 6. Buffer I/O
bw := bufio.NewWriter(w)
defer bw.Flush()
// write to bw instead of w — batches writes

// 7. Use encoding/json efficiently for large payloads
enc := json.NewEncoder(w)
enc.Encode(largeStruct)          // streams; no intermediate buffer
// vs: data, _ := json.Marshal(largeStruct); w.Write(data)  // two allocations

// 8. Avoid defer in tight loops (defer has ~100ns overhead)
for _, f := range files {
    processFile(f)  // defer inside here is fine
}
// but:
func inner(f *os.File) {
    defer f.Close()   // one defer per function call = fine
}
```

### 24.3 Memory Optimization

```go
// Struct field ordering matters (avoid padding)
// ❌ Wastes memory due to alignment padding
type BadStruct struct {
    a bool    // 1 byte + 7 bytes padding
    b float64 // 8 bytes
    c bool    // 1 byte + 7 bytes padding
    // Total: 24 bytes
}

// ✅ Group smaller fields together
type GoodStruct struct {
    b float64 // 8 bytes
    a bool    // 1 byte
    c bool    // 1 byte + 6 bytes padding
    // Total: 16 bytes
}
// Use: go vet -copylocks, and fieldalignment tool

// Check struct size
import "unsafe"
fmt.Println(unsafe.Sizeof(BadStruct{}))   // 24
fmt.Println(unsafe.Sizeof(GoodStruct{}))  // 16

// String interning (for frequently repeated strings)
// Use sync.Map to cache strings and deduplicate
```

---

## Appendix: Go Cheat Sheet

### Type Quick Reference
```go
bool, string
int, int8, int16, int32, int64
uint, uint8 (byte), uint16, uint32, uint64
float32, float64
complex64, complex128
rune (= int32)
uintptr
```

### Zero Values
```
bool:    false
int:     0
float:   0.0
string:  ""
pointer: nil
slice:   nil
map:     nil
channel: nil
func:    nil
interface: nil
```

### Common Idioms
```go
// Check error
v, err := something()
if err != nil { return fmt.Errorf("doing something: %w", err) }

// Open file, always close
f, err := os.Open(path)
if err != nil { return err }
defer f.Close()

// Safe type assertion
if str, ok := v.(string); ok { use(str) }

// Zero value works for maps/slices (nil is valid)
var s []int
s = append(s, 1)  // works on nil slice

// Receive from closed channel
v, ok := <-ch  // ok=false when channel closed and empty

// Context propagation
func Do(ctx context.Context, ...) error

// Cancel with defer
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// WaitGroup
var wg sync.WaitGroup
wg.Add(1)
go func() { defer wg.Done(); doWork() }()
wg.Wait()

// Goroutine-safe counter
var count int64
atomic.AddInt64(&count, 1)

// init once
var once sync.Once
once.Do(func() { expensive = createExpensive() })
```

### Common Packages
| Package | Use |
|---------|-----|
| `fmt` | Formatted I/O, Sprintf |
| `os` | Files, env, args, exit |
| `io` | Reader/Writer interfaces |
| `bufio` | Buffered I/O, Scanner |
| `strings` | String operations |
| `strconv` | String ↔ type conversions |
| `errors` | Error creation and wrapping |
| `sync` | Mutex, WaitGroup, Once, Pool |
| `sync/atomic` | Lock-free atomic ops |
| `context` | Cancellation, deadlines |
| `time` | Time, Duration, Timer, Ticker |
| `math` | Math functions |
| `math/rand` | Pseudorandom numbers |
| `sort` | Sorting algorithms |
| `encoding/json` | JSON marshal/unmarshal |
| `net/http` | HTTP client and server |
| `log` | Simple logging |
| `log/slog` | Structured logging (Go 1.21+) |
| `regexp` | Regular expressions |
| `path/filepath` | File path manipulation |
| `runtime` | Runtime info, goroutine info |
| `reflect` | Reflection |
| `testing` | Test framework |
| `flag` | Command-line flag parsing |
| `bytes` | Byte slice operations |

### Go Proverbs (Rob Pike)
```
Don't communicate by sharing memory; share memory by communicating.
Concurrency is not parallelism.
Channels orchestrate; mutexes serialize.
The bigger the interface, the weaker the abstraction.
Make the zero value useful.
interface{} says nothing.
Gofmt's style is no one's favorite, yet gofmt is everyone's favorite.
A little copying is better than a little dependency.
Clear is better than clever.
Errors are values.
Don't just check errors, handle them gracefully.
Design the architecture, name the components, document the details.
Documentation is for users.
Don't panic.
```

---

# Go Mastery Guide — Supplement: Missing & Thin Topics

---

## Chapter 25: database/sql — The Standard Database Package

### 25.1 Why database/sql Exists

Go's `database/sql` package provides a generic interface to SQL databases. The actual database driver is a separate package that registers itself — your application code stays portable across databases.

```
Your code → database/sql → driver interface → mysql driver → MySQL
                                            → postgres driver → PostgreSQL
                                            → sqlite3 driver → SQLite
```

```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"   // blank import: registers the driver, imports nothing else
    // _ "github.com/lib/pq"             // PostgreSQL
    // _ "github.com/mattn/go-sqlite3"   // SQLite (requires CGO)
    // _ "modernc.org/sqlite"            // SQLite (pure Go, no CGO)
)
```

### 25.2 Connection Pool and sql.DB

`sql.DB` is NOT a single connection — it's a **connection pool**. It manages opening, reusing, and closing connections automatically.

```go
func openDB(dsn string) (*sql.DB, error) {
    // dsn: Data Source Name
    // MySQL:     "user:pass@tcp(localhost:3306)/dbname?parseTime=true"
    // PostgreSQL: "postgres://user:pass@localhost/dbname?sslmode=disable"
    // SQLite:    "file:data.db?cache=shared&mode=rwc"

    db, err := sql.Open("mysql", dsn)
    if err != nil {
        return nil, fmt.Errorf("sql.Open: %w", err)
    }

    // sql.Open does NOT open a connection — it just validates the DSN.
    // Use Ping to verify connectivity:
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := db.PingContext(ctx); err != nil {
        return nil, fmt.Errorf("db.Ping: %w", err)
    }

    // Connection pool configuration
    db.SetMaxOpenConns(25)                  // max concurrent connections (default: unlimited)
    db.SetMaxIdleConns(10)                  // max idle connections kept in pool (default: 2)
    db.SetConnMaxLifetime(5 * time.Minute)  // recycle connections after 5 min
    db.SetConnMaxIdleTime(1 * time.Minute)  // close idle connections after 1 min

    return db, nil
}
```

### 25.3 Querying — Full CRUD

```go
type User struct {
    ID        int
    Name      string
    Email     string
    CreatedAt time.Time
    Active    bool
    Score     sql.NullFloat64  // nullable float
}

// ── QueryRowContext — single row ──────────────────────────────
func (r *UserRepository) GetByID(ctx context.Context, id int) (*User, error) {
    const q = `SELECT id, name, email, created_at, active, score
               FROM users WHERE id = ?`

    var u User
    err := r.db.QueryRowContext(ctx, q, id).Scan(
        &u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.Active, &u.Score,
    )
    if err == sql.ErrNoRows {
        return nil, fmt.Errorf("user %d: %w", id, ErrNotFound)
    }
    if err != nil {
        return nil, fmt.Errorf("GetByID: %w", err)
    }
    return &u, nil
}

// ── QueryContext — multiple rows ───────────────────────────────
func (r *UserRepository) ListActive(ctx context.Context) ([]User, error) {
    const q = `SELECT id, name, email, created_at, active, score
               FROM users WHERE active = true ORDER BY name`

    rows, err := r.db.QueryContext(ctx, q)
    if err != nil {
        return nil, fmt.Errorf("ListActive query: %w", err)
    }
    defer rows.Close()  // ALWAYS defer rows.Close()

    var users []User
    for rows.Next() {
        var u User
        if err := rows.Scan(
            &u.ID, &u.Name, &u.Email, &u.CreatedAt, &u.Active, &u.Score,
        ); err != nil {
            return nil, fmt.Errorf("ListActive scan: %w", err)
        }
        users = append(users, u)
    }
    // Check for errors during iteration (network failure mid-result)
    if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("ListActive rows: %w", err)
    }
    return users, nil
}

// ── ExecContext — INSERT/UPDATE/DELETE ─────────────────────────
func (r *UserRepository) Create(ctx context.Context, name, email string) (int64, error) {
    const q = `INSERT INTO users (name, email, created_at, active) VALUES (?, ?, NOW(), true)`

    result, err := r.db.ExecContext(ctx, q, name, email)
    if err != nil {
        return 0, fmt.Errorf("Create: %w", err)
    }

    id, err := result.LastInsertId()  // MySQL; PostgreSQL uses RETURNING id instead
    if err != nil {
        return 0, fmt.Errorf("LastInsertId: %w", err)
    }
    return id, nil
}

func (r *UserRepository) Update(ctx context.Context, id int, name string) error {
    const q = `UPDATE users SET name = ? WHERE id = ?`
    result, err := r.db.ExecContext(ctx, q, name, id)
    if err != nil {
        return fmt.Errorf("Update: %w", err)
    }
    rows, err := result.RowsAffected()
    if err != nil {
        return fmt.Errorf("RowsAffected: %w", err)
    }
    if rows == 0 {
        return fmt.Errorf("user %d: %w", id, ErrNotFound)
    }
    return nil
}

func (r *UserRepository) Delete(ctx context.Context, id int) error {
    _, err := r.db.ExecContext(ctx, `DELETE FROM users WHERE id = ?`, id)
    return err
}
```

### 25.4 Transactions

```go
func (r *UserRepository) TransferScore(ctx context.Context, fromID, toID int, amount float64) error {
    // Begin transaction
    tx, err := r.db.BeginTx(ctx, &sql.TxOptions{
        Isolation: sql.LevelReadCommitted,  // isolation level
        ReadOnly:  false,
    })
    if err != nil {
        return fmt.Errorf("begin tx: %w", err)
    }
    // Defer rollback: if we return before Commit(), this runs
    // If we already committed, Rollback() is a no-op
    defer tx.Rollback()

    // Debit
    _, err = tx.ExecContext(ctx,
        `UPDATE users SET score = score - ? WHERE id = ? AND score >= ?`,
        amount, fromID, amount,
    )
    if err != nil {
        return fmt.Errorf("debit: %w", err)
    }

    // Credit
    _, err = tx.ExecContext(ctx,
        `UPDATE users SET score = score + ? WHERE id = ?`,
        amount, toID,
    )
    if err != nil {
        return fmt.Errorf("credit: %w", err)
    }

    // Commit
    if err := tx.Commit(); err != nil {
        return fmt.Errorf("commit: %w", err)
    }
    return nil
}
```

### 25.5 Prepared Statements

```go
type UserRepository struct {
    db       *sql.DB
    stmtGet  *sql.Stmt
    stmtList *sql.Stmt
}

func NewUserRepository(db *sql.DB) (*UserRepository, error) {
    r := &UserRepository{db: db}
    var err error

    // Prepare frequently-used queries (compiled once, reused many times)
    r.stmtGet, err = db.Prepare(`SELECT id, name, email FROM users WHERE id = ?`)
    if err != nil {
        return nil, fmt.Errorf("prepare stmtGet: %w", err)
    }

    r.stmtList, err = db.Prepare(`SELECT id, name FROM users WHERE active = ? LIMIT ?`)
    if err != nil {
        r.stmtGet.Close()
        return nil, fmt.Errorf("prepare stmtList: %w", err)
    }

    return r, nil
}

func (r *UserRepository) Close() {
    r.stmtGet.Close()
    r.stmtList.Close()
}

func (r *UserRepository) GetByID(ctx context.Context, id int) (*User, error) {
    var u User
    err := r.stmtGet.QueryRowContext(ctx, id).Scan(&u.ID, &u.Name, &u.Email)
    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    return &u, err
}
```

### 25.6 Handling NULLs

```go
// SQL NULL cannot be scanned into Go's basic types (int, string, etc.)
// Use sql.Null* types or pointers

type Profile struct {
    UserID  int
    Bio     sql.NullString   // NULL or string
    Age     sql.NullInt64    // NULL or int64
    Score   sql.NullFloat64  // NULL or float64
    Deleted sql.NullTime     // NULL or time.Time

    // Alternative: use pointers
    Website *string          // nil = NULL
    Avatar  *string
}

// Scanning NULLs
var p Profile
err := db.QueryRowContext(ctx, `SELECT bio, age FROM profiles WHERE user_id = ?`, id).
    Scan(&p.Bio, &p.Age)

if p.Bio.Valid {
    fmt.Println("Bio:", p.Bio.String)
} else {
    fmt.Println("Bio: NULL")
}

// Inserting NULLs
bio := sql.NullString{String: "Gopher", Valid: true}    // non-null
noAge := sql.NullInt64{Valid: false}                     // NULL

db.ExecContext(ctx, `INSERT INTO profiles (bio, age) VALUES (?, ?)`, bio, noAge)
```

---

## Chapter 26: reflect Package — Runtime Reflection

### 26.1 What Reflection Is and When to Use It

Reflection lets you inspect and manipulate types and values at runtime. Go's reflection is in `reflect` package.

**Use reflection when:** building generic serialization (JSON, YAML), ORM field mapping, dependency injection, test utilities, struct validation.

**Don't use reflection when:** you know the types at compile time — use generics or interfaces instead. Reflection is slow and loses type safety.

```go
import "reflect"

// reflect.TypeOf — get type information
x := 42
t := reflect.TypeOf(x)       // reflect.Type
fmt.Println(t.Name())         // "int"
fmt.Println(t.Kind())         // reflect.Int
fmt.Println(t.Size())         // 8 (bytes on 64-bit)

s := "hello"
ts := reflect.TypeOf(s)
fmt.Println(ts.Kind())        // reflect.String

type Point struct{ X, Y int }
p := Point{3, 4}
tp := reflect.TypeOf(p)
fmt.Println(tp.Name())        // "Point"
fmt.Println(tp.Kind())        // reflect.Struct
fmt.Println(tp.NumField())    // 2

// reflect.ValueOf — get/set values
v := reflect.ValueOf(x)
fmt.Println(v.Int())          // 42
fmt.Println(v.Kind())         // reflect.Int

vp := reflect.ValueOf(&x).Elem()  // Elem() to get the value pointed to
vp.SetInt(100)                     // modifies x
fmt.Println(x)                     // 100
```

### 26.2 Inspecting Structs

```go
type User struct {
    ID       int    `json:"id" db:"user_id" validate:"required"`
    Name     string `json:"name" validate:"required,min=2"`
    Email    string `json:"email" validate:"email"`
    password string // unexported
}

func inspectStruct(v interface{}) {
    t := reflect.TypeOf(v)
    val := reflect.ValueOf(v)

    if t.Kind() == reflect.Ptr {
        t = t.Elem()       // dereference pointer
        val = val.Elem()
    }

    fmt.Printf("Type: %s\n", t.Name())
    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)         // reflect.StructField
        value := val.Field(i)       // reflect.Value

        // Skip unexported fields
        if !field.IsExported() {
            continue
        }

        fmt.Printf("Field: %-10s Type: %-10s Value: %v\n",
            field.Name, field.Type, value.Interface())

        // Read struct tags
        jsonTag  := field.Tag.Get("json")
        dbTag    := field.Tag.Get("db")
        valTag   := field.Tag.Get("validate")
        fmt.Printf("  json=%q db=%q validate=%q\n", jsonTag, dbTag, valTag)
    }
}

u := User{ID: 1, Name: "Alice", Email: "alice@example.com"}
inspectStruct(u)
// Type: User
// Field: ID         Type: int        Value: 1
//   json="id" db="user_id" validate="required"
// ...
```

### 26.3 Building a Simple Struct-to-Map Mapper

```go
// StructToMap converts a struct to map[string]interface{} using json tags
func StructToMap(v interface{}) map[string]interface{} {
    result := make(map[string]interface{})

    t := reflect.TypeOf(v)
    val := reflect.ValueOf(v)
    if t.Kind() == reflect.Ptr {
        t, val = t.Elem(), val.Elem()
    }
    if t.Kind() != reflect.Struct {
        return nil
    }

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        if !field.IsExported() {
            continue
        }
        key := field.Name
        if tag := field.Tag.Get("json"); tag != "" && tag != "-" {
            // Use json tag name (strip options like ",omitempty")
            if comma := strings.Index(tag, ","); comma != -1 {
                tag = tag[:comma]
            }
            key = tag
        }
        result[key] = val.Field(i).Interface()
    }
    return result
}

// MapToStruct fills a struct from a map using json tags
func MapToStruct(m map[string]interface{}, dest interface{}) error {
    t := reflect.TypeOf(dest).Elem()
    val := reflect.ValueOf(dest).Elem()

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        key := field.Name
        if tag := field.Tag.Get("json"); tag != "" {
            key = strings.Split(tag, ",")[0]
        }
        if v, ok := m[key]; ok {
            fv := val.Field(i)
            if fv.CanSet() {
                fv.Set(reflect.ValueOf(v).Convert(field.Type))
            }
        }
    }
    return nil
}
```

### 26.4 Calling Functions via Reflection

```go
// Call a method by name dynamically
func callMethod(obj interface{}, methodName string, args ...interface{}) ([]interface{}, error) {
    v := reflect.ValueOf(obj)
    method := v.MethodByName(methodName)
    if !method.IsValid() {
        return nil, fmt.Errorf("method %q not found", methodName)
    }

    // Convert args to reflect.Value
    in := make([]reflect.Value, len(args))
    for i, arg := range args {
        in[i] = reflect.ValueOf(arg)
    }

    // Call the method
    out := method.Call(in)

    // Convert results to interface{}
    result := make([]interface{}, len(out))
    for i, v := range out {
        result[i] = v.Interface()
    }
    return result, nil
}

type Calculator struct{}
func (c Calculator) Add(a, b int) int { return a + b }

calc := Calculator{}
results, _ := callMethod(calc, "Add", 3, 4)
fmt.Println(results[0]) // 7
```

---

## Chapter 27: Goroutine Leak Patterns & Prevention

### 27.1 What Is a Goroutine Leak?

A goroutine leak is a goroutine that's blocked forever — waiting on a channel, mutex, or HTTP request — and never terminates. Since goroutines are cheap but not free (~2-8KB each), thousands of leaked goroutines can exhaust memory.

```go
// ❌ Classic leak #1: sending to unbuffered channel with no receiver
func leak1() {
    ch := make(chan int)
    go func() {
        ch <- 1   // blocks FOREVER if no one reads from ch
    }()
    // function returns; ch goes out of scope; goroutine is stuck
}

// ❌ Classic leak #2: receiving from channel that never gets data or closed
func leak2(jobs <-chan Job) {
    go func() {
        for job := range jobs {  // blocks if jobs is never closed
            process(job)
        }
    }()
    // if jobs is never closed, goroutine lives forever
}

// ❌ Classic leak #3: goroutine blocked in HTTP request with no timeout
func leak3(url string) {
    go func() {
        resp, _ := http.Get(url)  // no context/timeout → can block indefinitely
        defer resp.Body.Close()
        process(resp)
    }()
}
```

### 27.2 Fixing Leaks with Context and Done Channels

```go
// ✅ Fix #1: use context for cancellation
func noLeak1(ctx context.Context) {
    ch := make(chan int, 1)  // buffered, or...
    go func() {
        select {
        case ch <- 1:       // if receiver ready, send
        case <-ctx.Done():  // if cancelled, exit
            return
        }
    }()
}

// ✅ Fix #2: always close channels when done producing
func noLeak2(ctx context.Context) <-chan Job {
    out := make(chan Job)
    go func() {
        defer close(out)  // ALWAYS close when producer is done
        for {
            select {
            case <-ctx.Done():
                return
            case job := <-fetchNextJob():
                out <- job
            }
        }
    }()
    return out
}

// ✅ Fix #3: always use context with HTTP
func noLeak3(ctx context.Context, url string) {
    go func() {
        req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
        if err != nil { return }
        resp, err := http.DefaultClient.Do(req)
        if err != nil { return }  // context cancelled → err is non-nil
        defer resp.Body.Close()
        process(resp)
    }()
}

// Detecting goroutine leaks in tests (goleak package)
import "go.uber.org/goleak"

func TestNoLeak(t *testing.T) {
    defer goleak.VerifyNone(t)  // fails test if goroutines are leaked
    // ... run code ...
}
```

### 27.3 errgroup — Goroutines with Error Propagation

```go
import "golang.org/x/sync/errgroup"

// errgroup.Group: like WaitGroup, but collects errors and cancels on first failure
func fetchAllUsers(ctx context.Context, ids []int) ([]*User, error) {
    g, ctx := errgroup.WithContext(ctx)  // cancel ctx when any goroutine returns an error

    users := make([]*User, len(ids))

    for i, id := range ids {
        i, id := i, id  // capture for goroutine
        g.Go(func() error {
            user, err := fetchUser(ctx, id)  // ctx cancelled if another goroutine failed
            if err != nil {
                return fmt.Errorf("fetch user %d: %w", id, err)
            }
            users[i] = user
            return nil
        })
    }

    // Wait for all goroutines. Returns first non-nil error.
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return users, nil
}

// Limit concurrency with errgroup + semaphore
func fetchWithLimit(ctx context.Context, ids []int, concurrency int) ([]*User, error) {
    g, ctx := errgroup.WithContext(ctx)
    sem := make(chan struct{}, concurrency)  // semaphore: max N concurrent

    users := make([]*User, len(ids))
    for i, id := range ids {
        i, id := i, id
        g.Go(func() error {
            sem <- struct{}{}        // acquire slot
            defer func() { <-sem }() // release slot

            user, err := fetchUser(ctx, id)
            if err != nil { return err }
            users[i] = user
            return nil
        })
    }
    return users, g.Wait()
}
```

---

## Chapter 28: Custom io.Reader and io.Writer

### 28.1 Implementing io.Reader

```go
// io.Reader interface: Read(p []byte) (n int, err error)
// Read fills p with up to len(p) bytes; returns n bytes read and any error
// Return (0, io.EOF) to signal end of data

// Example: CountingReader — wraps a Reader and counts bytes read
type CountingReader struct {
    r     io.Reader
    count int64
}

func (cr *CountingReader) Read(p []byte) (int, error) {
    n, err := cr.r.Read(p)
    cr.count += int64(n)
    return n, err
}

func (cr *CountingReader) BytesRead() int64 { return cr.count }

// Usage
f, _ := os.Open("bigfile.txt")
cr := &CountingReader{r: f}
io.Copy(io.Discard, cr)  // read all
fmt.Printf("Read %d bytes\n", cr.BytesRead())

// Example: LimitedRateReader — throttle reading to N bytes per second
type RateLimitedReader struct {
    r       io.Reader
    rate    int           // bytes per second
    lastRead time.Time
}

func (r *RateLimitedReader) Read(p []byte) (int, error) {
    // Throttle: sleep if reading too fast
    elapsed := time.Since(r.lastRead)
    if elapsed < time.Second && r.lastRead != (time.Time{}) {
        time.Sleep(time.Second - elapsed)
    }
    n, err := r.r.Read(p[:min(len(p), r.rate)])
    r.lastRead = time.Now()
    return n, err
}

// Example: StringsReader — read from a series of strings
type StringsReader struct {
    strs []string
    pos  int  // current string index
    off  int  // offset within current string
}

func NewStringsReader(strs ...string) *StringsReader {
    return &StringsReader{strs: strs}
}

func (r *StringsReader) Read(p []byte) (int, error) {
    if r.pos >= len(r.strs) {
        return 0, io.EOF
    }
    n := copy(p, r.strs[r.pos][r.off:])
    r.off += n
    if r.off >= len(r.strs[r.pos]) {
        r.pos++
        r.off = 0
    }
    return n, nil
}
```

### 28.2 Implementing io.Writer

```go
// io.Writer interface: Write(p []byte) (n int, err error)
// Must write all of p; returning n < len(p) is an error

// Example: MultiWriter that writes to multiple writers
type BroadcastWriter struct {
    writers []io.Writer
}

func (b *BroadcastWriter) Write(p []byte) (int, error) {
    for _, w := range b.writers {
        if n, err := w.Write(p); err != nil {
            return n, err
        }
    }
    return len(p), nil
}

// stdlib already has io.MultiWriter(w1, w2, w3)

// Example: HashWriter — write and compute hash simultaneously
import "crypto/sha256"

type HashWriter struct {
    w    io.Writer
    hash hash.Hash
}

func NewHashWriter(w io.Writer) *HashWriter {
    return &HashWriter{w: w, hash: sha256.New()}
}

func (hw *HashWriter) Write(p []byte) (int, error) {
    hw.hash.Write(p)   // update hash (never returns error)
    return hw.w.Write(p)
}

func (hw *HashWriter) Sum() []byte { return hw.hash.Sum(nil) }

// Usage: write to file and compute hash at the same time
f, _ := os.Create("output.bin")
hw := NewHashWriter(f)
io.Copy(hw, sourceReader)
fmt.Printf("SHA256: %x\n", hw.Sum())

// Example: LimitWriter — stop writing after N bytes
type LimitWriter struct {
    w       io.Writer
    limit   int64
    written int64
}

func (lw *LimitWriter) Write(p []byte) (int, error) {
    remaining := lw.limit - lw.written
    if remaining <= 0 {
        return 0, fmt.Errorf("write limit %d exceeded", lw.limit)
    }
    if int64(len(p)) > remaining {
        p = p[:remaining]  // truncate to remaining limit
    }
    n, err := lw.w.Write(p)
    lw.written += int64(n)
    return n, err
}
```

---

## Chapter 29: Structured Logging with log/slog (Go 1.21+)

### 29.1 Why slog?

Before Go 1.21, the standard `log` package only wrote unstructured text. Production systems need structured logs (JSON) for log aggregation tools (Elasticsearch, Splunk, Datadog).

```go
import "log/slog"

// Default logger: writes to stderr in text format
slog.Info("server started", "addr", ":8080", "env", "production")
// Output: time=2024-01-15T10:30:00Z level=INFO msg="server started" addr=:8080 env=production

slog.Warn("high memory", "used_mb", 850, "limit_mb", 1024)
slog.Error("request failed", "path", "/api/users", "error", err)
slog.Debug("cache hit", "key", "user:42")  // only shown if level <= Debug
```

### 29.2 Creating and Configuring Loggers

```go
// Text handler (human-readable for development)
textLogger := slog.New(slog.NewTextHandler(os.Stderr, &slog.HandlerOptions{
    Level:     slog.LevelDebug,   // minimum level to output
    AddSource: true,              // include file:line in log
}))

// JSON handler (machine-readable for production)
jsonLogger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
    ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
        // Rename the time key
        if a.Key == slog.TimeKey { a.Key = "@timestamp" }
        // Rename the message key
        if a.Key == slog.MessageKey { a.Key = "message" }
        return a
    },
}))
// Output: {"@timestamp":"2024-01-15T10:30:00Z","level":"INFO","message":"server started","addr":":8080"}

// Set as default logger
slog.SetDefault(jsonLogger)

// Logger with persistent context (always include these fields)
logger := slog.With(
    "service", "user-service",
    "version", "2.1.0",
    "host", hostname,
)
logger.Info("started")  // includes service, version, host in every log line
```

### 29.3 Logging Patterns

```go
// Log groups — nested attributes
slog.Info("request",
    slog.Group("http",
        "method", r.Method,
        "path", r.URL.Path,
        "status", status,
        "duration_ms", duration.Milliseconds(),
    ),
    slog.Group("user",
        "id", userID,
        "role", role,
    ),
)
// JSON: {"msg":"request","http":{"method":"GET","path":"/api","status":200},"user":{"id":42}}

// LogAttrs — most efficient (avoids interface{} boxing)
slog.LogAttrs(ctx, slog.LevelInfo, "processed",
    slog.Int("items", 100),
    slog.Duration("elapsed", elapsed),
    slog.String("status", "ok"),
)

// Context-aware logging — extract trace ID from context
type ctxKey string
const loggerKey ctxKey = "logger"

func WithLogger(ctx context.Context, logger *slog.Logger) context.Context {
    return context.WithValue(ctx, loggerKey, logger)
}

func LoggerFromCtx(ctx context.Context) *slog.Logger {
    if l, ok := ctx.Value(loggerKey).(*slog.Logger); ok {
        return l
    }
    return slog.Default()
}

// Middleware that adds request ID to logger
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := uuid.New().String()
        logger := slog.With("request_id", requestID, "path", r.URL.Path)
        ctx := WithLogger(r.Context(), logger)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// In handler:
func myHandler(w http.ResponseWriter, r *http.Request) {
    log := LoggerFromCtx(r.Context())
    log.Info("handling request")
    // log automatically has request_id and path
}
```

---

## Chapter 30: go:embed and go:generate Directives

### 30.1 //go:embed — Embed Files at Compile Time

```go
import "embed"

// Embed a single file as a string
//go:embed templates/welcome.html
var welcomeHTML string

// Embed a single file as bytes
//go:embed static/logo.png
var logoBytes []byte

// Embed an entire directory as fs.FS
//go:embed static
var staticFiles embed.FS

// Embed multiple files (can use glob patterns)
//go:embed templates/*.html
//go:embed config/*.json
var allFiles embed.FS

func main() {
    // Use the embedded string directly
    fmt.Println(welcomeHTML)

    // Serve static files from embedded FS
    http.Handle("/static/", http.StripPrefix("/static/",
        http.FileServer(http.FS(staticFiles))))

    // Read from embedded FS
    data, err := staticFiles.ReadFile("static/config.json")
    if err != nil {
        log.Fatal(err)
    }

    // Walk embedded directory
    entries, _ := staticFiles.ReadDir("static")
    for _, e := range entries {
        fmt.Println(e.Name())
    }

    // Open as io.File for streaming
    f, _ := staticFiles.Open("static/bigfile.bin")
    defer f.Close()
    io.Copy(w, f)
}

// embed.FS implements fs.FS, fs.ReadDirFS, and fs.ReadFileFS
// Works great for: HTML templates, SQL migrations, config defaults, certificates
```

### 30.2 //go:generate — Code Generation

```go
// go:generate runs a command when you run `go generate ./...`
// Place in any .go file; run manually during development

//go:generate stringer -type=Direction -output=direction_string.go
type Direction int
const (
    North Direction = iota
    East
    South
    West
)
// After running go generate: creates direction_string.go with String() method
// North.String() == "North", East.String() == "East", etc.

//go:generate mockgen -source=interfaces.go -destination=mocks/mock_interfaces.go
// Generates mock implementations for testing

//go:generate protoc --go_out=. --go-grpc_out=. api.proto
// Generates Go code from protobuf definition

//go:generate go run scripts/generate_constants.go
// Runs a custom generation script

// Workflow:
// 1. Edit template or interface
// 2. Run: go generate ./...
// 3. Commit the generated files (or regenerate in CI)
```

---

## Chapter 31: Benchmarking with testing.B

### 31.1 Writing Benchmarks

```go
// Benchmark functions: func BenchmarkXxx(b *testing.B)
// Run with: go test -bench=. -benchmem -benchtime=3s ./...

func BenchmarkStringConcat(b *testing.B) {
    strs := []string{"hello", " ", "world", "!"}
    b.ResetTimer()  // exclude setup from measurement

    for i := 0; i < b.N; i++ {  // b.N adjusted to run ~1 second by default
        var result string
        for _, s := range strs {
            result += s   // ← what we're measuring
        }
        _ = result  // prevent compiler from optimizing away
    }
}

func BenchmarkStringBuilder(b *testing.B) {
    strs := []string{"hello", " ", "world", "!"}
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        var sb strings.Builder
        for _, s := range strs {
            sb.WriteString(s)
        }
        _ = sb.String()
    }
}

// BenchmarkStringConcat   5000000   320 ns/op   48 B/op   3 allocs/op
// BenchmarkStringBuilder  20000000   72 ns/op    8 B/op   1 allocs/op

// -benchmem: show memory allocations (allocs/op and B/op)
// -benchtime=5s: run for 5 seconds instead of 1
// -count=5: run each benchmark 5 times (for statistical stability)
// -run='^$' -bench=.: run ONLY benchmarks (skip all tests)

// Sub-benchmarks
func BenchmarkMap(b *testing.B) {
    sizes := []int{10, 100, 1000, 10000}
    for _, size := range sizes {
        b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
            m := make(map[int]int, size)
            for i := 0; i < size; i++ {
                m[i] = i
            }
            b.ResetTimer()
            for i := 0; i < b.N; i++ {
                _ = m[size/2]  // lookup in the middle
            }
        })
    }
}
// Run specific sub-benchmark: go test -bench=BenchmarkMap/size=1000

// Parallel benchmarks
func BenchmarkConcurrentMap(b *testing.B) {
    var m sync.Map
    b.RunParallel(func(pb *testing.PB) {
        i := 0
        for pb.Next() {
            m.Store(i%100, i)
            i++
        }
    })
}

// Report custom metrics
func BenchmarkThroughput(b *testing.B) {
    data := make([]byte, 1024*1024) // 1 MB
    b.SetBytes(int64(len(data)))     // report MB/s
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        processData(data)
    }
}
// Output: 500 MB/s (bytes/op shown automatically)
```

---

## Chapter 32: Go Workspaces (go work)

```bash
# Go workspaces (Go 1.18+): develop multiple modules together locally
# without publishing to a registry

# Scenario: you're developing two modules simultaneously:
# myapp/ — your application
# mylib/ — a library myapp depends on

# Without workspace: you'd need to use replace directives in go.mod:
# require github.com/you/mylib v0.0.0
# replace github.com/you/mylib => ../mylib   ← remove before committing!

# With workspace:
cd /code
go work init myapp mylib   # creates go.work file

# go.work file:
go 1.22

use (
    ./myapp
    ./mylib
)

# Now: changes in ../mylib are immediately visible in myapp — no publishing needed
# go.work is NOT committed (it's local to your machine)
# Add go.work to .gitignore

# Add another module to workspace
go work use ./myotherthing

# Sync: update workspace after adding/removing modules  
go work sync

# Verify workspace is consistent
go work verify

# Build entire workspace
go build ./...  # from workspace root

# Turn off workspace (use module's go.mod instead)
GOWORK=off go build ./...
```

---

## Chapter 33: Advanced Concurrency Patterns

### 33.1 Fan-Out, Fan-In — Complete Implementation

```go
// Fan-out: distribute work across multiple goroutines
// Fan-in: collect results back into a single channel

func fanOut[T, R any](
    ctx context.Context,
    input <-chan T,
    numWorkers int,
    process func(context.Context, T) (R, error),
) <-chan Result[R] {
    out := make(chan Result[R], numWorkers)
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range input {
                select {
                case <-ctx.Done():
                    return
                default:
                }
                result, err := process(ctx, item)
                out <- Result[R]{Value: result, Err: err}
            }
        }()
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

type Result[T any] struct {
    Value T
    Err   error
}

// Usage
jobs := make(chan string, 10)
go func() {
    defer close(jobs)
    for _, url := range urls { jobs <- url }
}()

results := fanOut(ctx, jobs, 10, func(ctx context.Context, url string) ([]byte, error) {
    return fetchURL(ctx, url)
})

for r := range results {
    if r.Err != nil { log.Printf("error: %v", r.Err); continue }
    process(r.Value)
}
```

### 33.2 Circuit Breaker Pattern

```go
type State int
const (
    StateClosed   State = iota  // normal operation
    StateOpen                    // fast-fail (not sending requests)
    StateHalfOpen               // testing if service recovered
)

type CircuitBreaker struct {
    mu           sync.Mutex
    state        State
    failures     int
    threshold    int
    timeout      time.Duration
    lastFailure  time.Time
}

func NewCircuitBreaker(threshold int, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{threshold: threshold, timeout: timeout}
}

func (cb *CircuitBreaker) Execute(fn func() error) error {
    cb.mu.Lock()
    state := cb.state
    if state == StateOpen {
        if time.Since(cb.lastFailure) > cb.timeout {
            cb.state = StateHalfOpen
            state = StateHalfOpen
        }
    }
    cb.mu.Unlock()

    if state == StateOpen {
        return fmt.Errorf("circuit breaker open")
    }

    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.failures++
        cb.lastFailure = time.Now()
        if cb.failures >= cb.threshold {
            cb.state = StateOpen
        }
        return err
    }

    // Success — reset
    cb.failures = 0
    cb.state = StateClosed
    return nil
}

// Usage
cb := NewCircuitBreaker(5, 30*time.Second)

err := cb.Execute(func() error {
    return callExternalService()
})
if err != nil {
    handleError(err) // might be circuit-breaker or actual error
}
```

---

## Chapter 34: encoding/json — Deep Dive

### 34.1 Custom Marshal/Unmarshal

```go
// Implement json.Marshaler and json.Unmarshaler for full control

// Custom time format
type RFC3339Time time.Time

func (t RFC3339Time) MarshalJSON() ([]byte, error) {
    return json.Marshal(time.Time(t).Format(time.RFC3339))
}

func (t *RFC3339Time) UnmarshalJSON(data []byte) error {
    var s string
    if err := json.Unmarshal(data, &s); err != nil {
        return err
    }
    parsed, err := time.Parse(time.RFC3339, s)
    if err != nil {
        return err
    }
    *t = RFC3339Time(parsed)
    return nil
}

// Money type: store as cents, serialize as decimal
type Money int64 // cents

func (m Money) MarshalJSON() ([]byte, error) {
    return json.Marshal(float64(m) / 100)
}

func (m *Money) UnmarshalJSON(data []byte) error {
    var f float64
    if err := json.Unmarshal(data, &f); err != nil {
        return err
    }
    *m = Money(math.Round(f * 100))
    return nil
}

// Enum with string representation
type Status int
const (
    StatusActive Status = iota
    StatusInactive
    StatusBanned
)

var statusNames = map[Status]string{
    StatusActive:   "active",
    StatusInactive: "inactive",
    StatusBanned:   "banned",
}
var statusValues = map[string]Status{
    "active": StatusActive, "inactive": StatusInactive, "banned": StatusBanned,
}

func (s Status) MarshalJSON() ([]byte, error) {
    name, ok := statusNames[s]
    if !ok { return nil, fmt.Errorf("unknown status: %d", s) }
    return json.Marshal(name)
}

func (s *Status) UnmarshalJSON(data []byte) error {
    var name string
    if err := json.Unmarshal(data, &name); err != nil { return err }
    v, ok := statusValues[name]
    if !ok { return fmt.Errorf("unknown status: %q", name) }
    *s = v
    return nil
}
```

### 34.2 Streaming JSON

```go
// json.Decoder for reading large JSON files without loading into memory
func processLargeJSONFile(filename string) error {
    f, err := os.Open(filename)
    if err != nil { return err }
    defer f.Close()

    dec := json.NewDecoder(f)

    // Read opening [
    if _, err := dec.Token(); err != nil { return err }

    for dec.More() {  // returns true while there's more items in current array
        var item Item
        if err := dec.Decode(&item); err != nil { return err }
        process(item)
    }

    // Read closing ]
    if _, err := dec.Token(); err != nil { return err }
    return nil
}

// json.Encoder for writing large JSON without buffering
func writeJSONStream(w io.Writer, items []Item) error {
    enc := json.NewEncoder(w)
    enc.SetIndent("", "  ")  // pretty-print

    w.Write([]byte("["))
    for i, item := range items {
        if i > 0 { w.Write([]byte(",")) }
        if err := enc.Encode(item); err != nil { return err }
    }
    w.Write([]byte("]"))
    return nil
}

// Decode unknown JSON structure
var raw json.RawMessage
json.Unmarshal(data, &raw)  // store as raw bytes for later processing

// Decode into map for unknown structure
var m map[string]interface{}
json.Unmarshal(data, &m)
// Access: m["key"].(string), m["count"].(float64)

// Use json.Number to preserve precision for numbers
dec := json.NewDecoder(strings.NewReader(`{"big": 9999999999999999}`))
dec.UseNumber()  // numbers decoded as json.Number instead of float64
var m2 map[string]interface{}
dec.Decode(&m2)
n := m2["big"].(json.Number)
i64, _ := n.Int64()   // 9999999999999999 (exact)
```

---

## Quick Reference: Missing Go Standard Library Sections

### net package (raw TCP/UDP)
```go
// TCP server
ln, err := net.Listen("tcp", ":8080")
for {
    conn, _ := ln.Accept()
    go handleConn(conn)
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    conn.SetDeadline(time.Now().Add(30 * time.Second))
    buf := make([]byte, 4096)
    for {
        n, err := conn.Read(buf)
        if err != nil { return }
        conn.Write(buf[:n])  // echo server
    }
}

// TCP client
conn, err := net.Dial("tcp", "example.com:80")
defer conn.Close()

// UDP
addr, _ := net.ResolveUDPAddr("udp", ":9999")
conn, _ := net.ListenUDP("udp", addr)
buf := make([]byte, 1024)
n, remoteAddr, _ := conn.ReadFromUDP(buf)
conn.WriteToUDP(buf[:n], remoteAddr)
```

### sync.Once, sync.Map — Advanced Usage
```go
// sync.Once for expensive lazy initialization
type Service struct {
    once   sync.Once
    client *ExpensiveClient
}

func (s *Service) getClient() *ExpensiveClient {
    s.once.Do(func() {
        s.client = createExpensiveClient()  // called exactly once
    })
    return s.client
}

// sync.Map for read-heavy concurrent maps
var cache sync.Map

// Store
cache.Store("key", value)

// Load (ok = false if not found)
if v, ok := cache.Load("key"); ok {
    use(v.(*MyType))
}

// LoadOrStore: atomic get-or-set
actual, loaded := cache.LoadOrStore("key", newValue)
// loaded=true: key existed; actual=existing value
// loaded=false: stored newValue; actual=newValue

// Delete
cache.Delete("key")

// Range: iterate (order not guaranteed, may skip concurrent modifications)
cache.Range(func(k, v any) bool {
    process(k, v)
    return true  // return false to stop
})
```

### Go Module Proxy and Private Modules
```bash
# GOPATH and module cache
$GOPATH/pkg/mod/          # downloaded module cache
$GOPATH/bin/              # installed binaries

# Private modules (don't go through proxy)
export GONOSUMCHECK=github.com/mycompany/*
export GOPRIVATE=github.com/mycompany/*
export GOFLAGS=-mod=mod

# go.env — persistent settings
go env -w GOPRIVATE=github.com/mycompany/*
go env -w GONOSUMDB=github.com/mycompany/*

# Tidy: add missing, remove unused
go mod tidy

# Verify modules haven't been tampered with
go mod verify

# Why is a dependency included?
go mod why github.com/some/package

# Upgrade all dependencies
go get -u ./...
go get -u=patch ./...  # only patch versions
```
