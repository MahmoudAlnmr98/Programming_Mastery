# Golang Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Go? Explain its key features.

**Answer:**
Go (Golang) is a statically typed, compiled programming language developed by Google.

**Key Features:**
- **Simple**: Clean syntax, easy to learn
- **Fast**: Compiled to machine code
- **Concurrent**: Built-in goroutines and channels
- **Garbage Collected**: Automatic memory management
- **Statically Typed**: Type checking at compile time
- **Cross-Platform**: Compile for different OS/architectures

### 2. Explain the difference between `var`, `:=`, and `const`.

**Answer:**
```go
// var - explicit type or inference
var x int = 10
var y = 20  // Type inferred

// := - short variable declaration (inside functions)
x := 10  // Type inferred, only in functions

// const - constant
const PI = 3.14159
const MaxSize = 100
```

### 3. What are goroutines? How do they differ from threads?

**Answer:**
Goroutines are lightweight threads managed by Go runtime.

**Differences:**
- **Goroutines**: Lightweight (2KB stack), managed by Go runtime, millions possible
- **Threads**: Heavier (1-2MB), managed by OS, limited (thousands)

```go
// Starting goroutine
go function()

// Example
go func() {
    fmt.Println("Hello from goroutine")
}()

// With parameters
go func(name string) {
    fmt.Printf("Hello, %s\n", name)
}("John")
```

### 4. Explain channels in Go.

**Answer:**
Channels are typed conduits for communication between goroutines.

```go
// Create channel
ch := make(chan int)        // Unbuffered
ch := make(chan int, 10)    // Buffered

// Send
ch <- 42

// Receive
value := <-ch
value, ok := <-ch  // ok is false if channel closed

// Close
close(ch)

// Range over channel
for value := range ch {
    fmt.Println(value)
}
```

### 5. What is the difference between buffered and unbuffered channels?

**Answer:**
- **Unbuffered**: Sender blocks until receiver receives
- **Buffered**: Sender blocks only when buffer is full

```go
// Unbuffered - synchronous
ch := make(chan int)
ch <- 1  // Blocks until received

// Buffered - asynchronous (up to capacity)
ch := make(chan int, 3)
ch <- 1  // Doesn't block
ch <- 2  // Doesn't block
ch <- 3  // Doesn't block
ch <- 4  // Blocks (buffer full)
```

### 6. Explain `defer` in Go.

**Answer:**
`defer` schedules function to execute when surrounding function returns.

```go
func example() {
    defer fmt.Println("World")
    fmt.Println("Hello")
}
// Output: Hello\nWorld

// Multiple defers (LIFO)
func example() {
    defer fmt.Println("First")
    defer fmt.Println("Second")
    defer fmt.Println("Third")
}
// Output: Third\nSecond\nFirst

// Common use: closing resources
func readFile(filename string) error {
    file, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer file.Close()  // Always closes
    
    // Read file
    return nil
}
```

### 7. Explain pointers in Go.

**Answer:**
Pointers hold memory address of a value.

```go
// Pointer declaration
var p *int
x := 42
p = &x  // Address of x

// Dereferencing
value := *p  // Value at address

// Pointer to struct
type Point struct {
    X, Y float64
}

p := &Point{X: 1, Y: 2}
p.X = 10  // Go automatically dereferences
```

### 8. Explain slices vs arrays in Go.

**Answer:**
- **Array**: Fixed size, value type
- **Slice**: Dynamic size, reference type (points to underlying array)

```go
// Array
var arr [5]int
arr := [5]int{1, 2, 3, 4, 5}

// Slice
var s []int
s := []int{1, 2, 3, 4, 5}
s := make([]int, 5)      // Length 5
s := make([]int, 5, 10)  // Length 5, capacity 10

// Slice from array
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]  // [2, 3, 4]
```

---

## Intermediate Level

### 9. Explain interfaces in Go.

**Answer:**
Interfaces define set of methods. Types implement interfaces implicitly.

```go
// Interface definition
type Shape interface {
    Area() float64
    Perimeter() float64
}

// Implementing interface (implicit)
type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return math.Pi * c.Radius * c.Radius
}

func (c Circle) Perimeter() float64 {
    return 2 * math.Pi * c.Radius
}

// Usage
var s Shape = Circle{Radius: 5}
fmt.Println(s.Area())
```

### 10. Explain error handling in Go.

**Answer:**
Go uses explicit error returns (no exceptions).

```go
// Error interface
type error interface {
    Error() string
}

// Creating errors
import "errors"
err := errors.New("something went wrong")

import "fmt"
err := fmt.Errorf("error: %v", value)

// Error handling
result, err := doSomething()
if err != nil {
    return err
}

// Custom error type
type MyError struct {
    Code    int
    Message string
}

func (e *MyError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}
```

### 11. Explain `select` statement.

**Answer:**
`select` waits on multiple channel operations.

```go
select {
case msg := <-ch1:
    fmt.Println("Received from ch1:", msg)
case msg := <-ch2:
    fmt.Println("Received from ch2:", msg)
case ch3 <- 42:
    fmt.Println("Sent to ch3")
default:
    fmt.Println("No communication")
}

// Timeout pattern
select {
case result := <-ch:
    fmt.Println(result)
case <-time.After(5 * time.Second):
    fmt.Println("Timeout")
}
```

### 12. Explain `sync.WaitGroup`.

**Answer:**
WaitGroup waits for collection of goroutines to finish.

```go
import "sync"

var wg sync.WaitGroup

for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        fmt.Printf("Goroutine %d\n", id)
    }(i)
}

wg.Wait()  // Wait for all goroutines
```

### 13. Explain `sync.Mutex` and `sync.RWMutex`.

**Answer:**
Mutex provides mutual exclusion for shared resources.

```go
import "sync"

var mu sync.Mutex
var counter int

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}

// RWMutex - multiple readers or one writer
var rwmu sync.RWMutex

// Read lock
rwmu.RLock()
// Read operations
rwmu.RUnlock()

// Write lock
rwmu.Lock()
// Write operations
rwmu.Unlock()
```

### 14. Explain method receivers: value vs pointer.

**Answer:**
- **Value receiver**: Operates on copy, cannot modify original
- **Pointer receiver**: Operates on original, can modify

```go
type Point struct {
    X, Y float64
}

// Value receiver (doesn't modify)
func (p Point) Distance() float64 {
    return math.Sqrt(p.X*p.X + p.Y*p.Y)
}

// Pointer receiver (can modify)
func (p *Point) Move(dx, dy float64) {
    p.X += dx
    p.Y += dy
}

// Go automatically handles & for pointer receivers
p := Point{X: 1, Y: 2}
p.Move(1, 1)  // Go converts to (&p).Move(1, 1)
```

### 15. Explain `context` package.

**Answer:**
Context carries deadlines, cancellation signals, and values.

```go
import "context"

// Background context
ctx := context.Background()

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// With value
ctx := context.WithValue(context.Background(), "key", "value")
value := ctx.Value("key")

// Check if context is done
select {
case <-ctx.Done():
    fmt.Println("Context cancelled")
    return ctx.Err()
default:
    // Continue
}
```

### 16. Explain `make` vs `new`.

**Answer:**
- **make**: Allocates and initializes slices, maps, channels (returns initialized value)
- **new**: Allocates memory, returns pointer to zero value

```go
// make - for slices, maps, channels
s := make([]int, 5)        // Slice with length 5
m := make(map[string]int)  // Empty map
ch := make(chan int)       // Unbuffered channel

// new - returns pointer to zero value
p := new(int)  // *int pointing to 0
// Equivalent to:
var p *int = new(int)
```

### 17. Explain embedding in Go.

**Answer:**
Embedding allows struct to include another struct (composition).

```go
type Person struct {
    Name string
    Age  int
}

type Employee struct {
    Person           // Embedded
    EmployeeID int
    Salary    float64
}

// Usage
emp := Employee{
    Person: Person{Name: "John", Age: 30},
    EmployeeID: 12345,
    Salary: 50000,
}

// Direct access to embedded fields
fmt.Println(emp.Name)      // Direct access
fmt.Println(emp.Person.Age) // Explicit access
```

---

## Advanced Level

### 18. Explain reflection in Go.

**Answer:**
Reflection allows inspection and manipulation of types at runtime.

```go
import "reflect"

// Get type
var x float64 = 3.14
t := reflect.TypeOf(x)
fmt.Println(t)  // float64

// Get value
v := reflect.ValueOf(x)
fmt.Println(v.Float())  // 3.14

// Set value (must use pointer)
var x float64 = 3.14
v := reflect.ValueOf(&x).Elem()
v.SetFloat(7.1)
fmt.Println(x)  // 7.1

// Inspect struct
type Person struct {
    Name string
    Age  int
}

p := Person{Name: "John", Age: 30}
v := reflect.ValueOf(p)
t := reflect.TypeOf(p)

for i := 0; i < v.NumField(); i++ {
    field := t.Field(i)
    value := v.Field(i)
    fmt.Printf("%s: %v\n", field.Name, value.Interface())
}
```

### 19. Explain generics in Go (Go 1.18+).

**Answer:**
Generics allow writing code that works with multiple types.

```go
// Generic function
func Swap[T any](a, b T) (T, T) {
    return b, a
}

x, y := Swap(1, 2)
s1, s2 := Swap("hello", "world")

// Generic type
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() T {
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item
}

// Usage
stack := &Stack[int]{}
stack.Push(1)
stack.Push(2)
value := stack.Pop()

// Type constraints
type Number interface {
    int | float64
}

func Add[T Number](a, b T) T {
    return a + b
}
```

### 20. Explain worker pool pattern.

**Answer:**
Worker pool limits number of concurrent goroutines.

```go
func workerPool(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- process(job)
    }
}

jobs := make(chan int, 100)
results := make(chan int, 100)

// Start workers
for w := 0; w < 10; w++ {
    go workerPool(jobs, results)
}

// Send jobs
for j := 1; j <= 100; j++ {
    jobs <- j
}
close(jobs)

// Collect results
for r := 1; r <= 100; r++ {
    <-results
}
```

### 21. Explain pipeline pattern.

**Answer:**
Pipeline chains processing stages.

```go
// Generator
func generator(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// Square stage
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// Usage
numbers := generator(2, 3, 4)
squares := square(numbers)
for result := range squares {
    fmt.Println(result)
}
```

### 22. Explain `sync.Pool`.

**Answer:**
Pool manages temporary objects to reduce allocations.

```go
import "sync"

var pool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

// Get from pool
buf := pool.Get().([]byte)
defer pool.Put(buf)

// Use buffer
// ...
```

### 23. Explain `atomic` package.

**Answer:**
Atomic operations for lock-free programming.

```go
import "sync/atomic"

var counter int64

// Atomic operations
atomic.AddInt64(&counter, 1)
value := atomic.LoadInt64(&counter)
atomic.StoreInt64(&counter, 10)
swapped := atomic.CompareAndSwapInt64(&counter, 10, 20)
```

### 24. Explain `unsafe` package.

**Answer:**
Unsafe allows low-level memory operations.

```go
import "unsafe"

// Size of type
size := unsafe.Sizeof(x)

// Pointer arithmetic
ptr := unsafe.Pointer(&x)
offset := unsafe.Pointer(uintptr(ptr) + offset)

// Type conversion
type MyInt int
var i MyInt = 10
var j int = *(*int)(unsafe.Pointer(&i))
```

### 25. Explain Go's garbage collector.

**Answer:**
Go uses concurrent, tri-color mark-and-sweep GC.

**Features:**
- **Concurrent**: Runs alongside program
- **Low Latency**: Short pause times
- **Tunable**: GOGC environment variable

**GC Phases:**
1. Mark: Mark reachable objects
2. Sweep: Free unmarked objects

**Tuning:**
```bash
GOGC=100  # Default (100% heap growth triggers GC)
GOGC=200  # Less frequent GC (more memory)
GOGC=50   # More frequent GC (less memory)
```

---

### 26. Explain Go Context Package.

**Answer:**
Context carries deadlines, cancellation signals, and values.

**Basic Usage:**
```go
ctx := context.Background()
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()

// Pass context to functions
result, err := doSomething(ctx)
```

**With Deadline:**
```go
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()
```

**With Value:**
```go
ctx := context.WithValue(context.Background(), "userID", 123)
userID := ctx.Value("userID").(int)
```

**Cancellation:**
```go
ctx, cancel := context.WithCancel(context.Background())
go func() {
    time.Sleep(2 * time.Second)
    cancel() // Cancel after 2 seconds
}()
```

### 27. Explain Go Error Handling Best Practices.

**Answer:**
**Error Wrapping:**
```go
import "fmt"

func process() error {
    if err := step1(); err != nil {
        return fmt.Errorf("step1 failed: %w", err)
    }
    return nil
}
```

**Custom Errors:**
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}
```

**Error Checking:**
```go
if err != nil {
    if validationErr, ok := err.(*ValidationError); ok {
        // Handle validation error
    }
    return err
}
```

### 28. Explain Go Testing.

**Answer:**
**Unit Test:**
```go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Expected 5, got %d", result)
    }
}
```

**Table-Driven Tests:**
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        a, b, expected int
    }{
        {2, 3, 5},
        {0, 0, 0},
        {-1, 1, 0},
    }
    
    for _, tt := range tests {
        result := Add(tt.a, tt.b)
        if result != tt.expected {
            t.Errorf("Add(%d, %d) = %d, expected %d", tt.a, tt.b, result, tt.expected)
        }
    }
}
```

**Benchmark:**
```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

### 29. Explain Go Modules.

**Answer:**
Modules manage dependencies.

**Initialize:**
```bash
go mod init example.com/project
```

**Add Dependency:**
```bash
go get github.com/gin-gonic/gin
```

**Update:**
```bash
go get -u github.com/gin-gonic/gin
```

**Tidy:**
```bash
go mod tidy
```

**Vendor:**
```bash
go mod vendor
```

### 30. Explain Go Concurrency Patterns.

**Answer:**
**Worker Pool:**
```go
func workerPool(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- process(job)
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // Start workers
    for w := 0; w < 3; w++ {
        go workerPool(jobs, results)
    }
    
    // Send jobs
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)
    
    // Collect results
    for r := 1; r <= 5; r++ {
        fmt.Println(<-results)
    }
}
```

**Pipeline:**
```go
func pipeline(input <-chan int) <-chan int {
    output := make(chan int)
    go func() {
        defer close(output)
        for n := range input {
            output <- n * 2
        }
    }()
    return output
}
```

### 31. Explain Go Reflection.

**Answer:**
Reflection allows examining types at runtime.

**Type Information:**
```go
import "reflect"

func inspect(v interface{}) {
    t := reflect.TypeOf(v)
    v := reflect.ValueOf(v)
    
    fmt.Println("Type:", t.Name())
    fmt.Println("Kind:", t.Kind())
    fmt.Println("Value:", v.Interface())
}
```

**Struct Fields:**
```go
type Person struct {
    Name string
    Age  int
}

func inspectStruct(s interface{}) {
    v := reflect.ValueOf(s)
    t := reflect.TypeOf(s)
    
    for i := 0; i < v.NumField(); i++ {
        field := t.Field(i)
        value := v.Field(i)
        fmt.Printf("%s: %v\n", field.Name, value.Interface())
    }
}
```

### 32. Explain Go Interface Best Practices.

**Answer:**
**Small Interfaces:**
```go
type Reader interface {
    Read([]byte) (int, error)
}

type Writer interface {
    Write([]byte) (int, error)
}
```

**Composition:**
```go
type ReadWriter interface {
    Reader
    Writer
}
```

**Accept Interfaces, Return Structs:**
```go
func Process(r Reader) error {
    // Accept interface
}

func NewService() *Service {
    // Return concrete type
    return &Service{}
}
```

### 33. Explain Go Memory Management.

**Answer:**
**Stack vs Heap:**
- Stack: Fast, automatic cleanup
- Heap: Slower, managed by GC

**Escape Analysis:**
```go
// Escapes to heap
func escape() *int {
    x := 42
    return &x // x escapes to heap
}

// Stays on stack
func noEscape() int {
    x := 42
    return x // x stays on stack
}
```

**GC Tuning:**
```bash
GOGC=100 go run main.go  # Default
GOGC=200 go run main.go  # Less frequent GC
```

### 34. Explain Go Build Tags.

**Answer:**
Build tags control compilation.

**File-Level:**
```go
// +build linux darwin

package main
```

**Line-Level:**
```go
//go:build linux || darwin
```

**Build:**
```bash
go build -tags=dev
```

**Use Cases:**
- Platform-specific code
- Feature flags
- Testing

### 35. Explain Go Embedding.

**Answer:**
Embedding allows including files in binary.

**Embed Files:**
```go
import _ "embed"

//go:embed template.html
var template string

//go:embed static/*
var staticFiles embed.FS
```

**Usage:**
```go
func main() {
    fmt.Println(template)
    
    data, _ := staticFiles.ReadFile("static/style.css")
    fmt.Println(string(data))
}
```

---

This covers Golang interview questions from beginner to advanced level with detailed explanations and code examples.

