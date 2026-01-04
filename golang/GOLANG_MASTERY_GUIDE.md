# Complete Go (Golang) Mastery Guide

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Data Types & Variables](#data-types--variables)
3. [Operators & Expressions](#operators--expressions)
4. [Control Flow](#control-flow)
5. [Functions](#functions)
6. [Structs & Methods](#structs--methods)
7. [Interfaces](#interfaces)
8. [Arrays & Slices](#arrays--slices)
9. [Maps](#maps)
10. [Pointers](#pointers)
11. [Error Handling](#error-handling)
12. [Concurrency](#concurrency)
13. [Channels](#channels)
14. [Goroutines](#goroutines)
15. [Packages & Modules](#packages--modules)
16. [I/O Operations](#io-operations)
17. [JSON & Encoding](#json--encoding)
18. [Testing](#testing)
19. [Reflection](#reflection)
20. [Context](#context)
21. [Best Practices](#best-practices)
22. [Advanced Topics](#advanced-topics)

---

## Fundamentals

### What is Go?
Go (Golang) is a statically typed, compiled programming language designed by Google. It's:
- **Simple**: Clean syntax, easy to learn
- **Fast**: Compiled to machine code
- **Concurrent**: Built-in support for goroutines and channels
- **Garbage Collected**: Automatic memory management
- **Statically Typed**: Type checking at compile time
- **Cross-Platform**: Compile for different OS/architectures

### Go Installation
```bash
# Download from https://golang.org/dl/
# Verify installation
go version

# Set up workspace (optional, Go modules preferred)
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

### Hello World
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

### Running Go Code
```bash
# Run directly
go run main.go

# Build executable
go build main.go
./main

# Build for specific platform
GOOS=linux GOARCH=amd64 go build main.go
```

### Go Workspace Structure
```
workspace/
├── go.mod          # Module definition
├── go.sum          # Dependency checksums
├── main.go
└── pkg/            # Package code
    └── utils/
        └── helper.go
```

---

## Data Types & Variables

### Basic Data Types
```go
// Boolean
var b bool = true
var b2 bool  // false (zero value)

// Integer types
var i int = 42           // Platform-dependent (32 or 64 bit)
var i8 int8 = 127        // -128 to 127
var i16 int16 = 32767    // -32,768 to 32,767
var i32 int32 = 2147483647
var i64 int64 = 9223372036854775807

// Unsigned integers
var u uint = 42
var u8 uint8 = 255       // 0 to 255
var u16 uint16 = 65535
var u32 uint32
var u64 uint64

// Byte and Rune
var by byte = 255        // alias for uint8
var r rune = 'A'         // alias for int32 (Unicode code point)

// Floating point
var f32 float32 = 3.14
var f64 float64 = 3.141592653589793

// Complex numbers
var c64 complex64 = 1 + 2i
var c128 complex128 = 1 + 2i

// String
var s string = "Hello, World!"
```

### Variable Declarations
```go
// Explicit type
var name string = "John"
var age int = 30

// Type inference
var name = "John"        // string
var age = 30             // int

// Multiple variables
var (
    name string = "John"
    age  int    = 30
)

// Short variable declaration (inside functions)
name := "John"
age := 30
x, y := 10, 20

// Zero values
var i int        // 0
var f float64    // 0.0
var b bool       // false
var s string     // ""
var p *int       // nil
var sl []int     // nil
var m map[string]int  // nil
```

### Type Conversion
```go
// Explicit conversion (no implicit conversion)
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)

// String conversion
import "strconv"

s := strconv.Itoa(42)           // "42"
i, _ := strconv.Atoi("42")      // 42
f, _ := strconv.ParseFloat("3.14", 64)

// Type assertions (for interfaces)
var i interface{} = "hello"
s := i.(string)                 // "hello"
s, ok := i.(string)             // "hello", true
```

### Constants
```go
// Single constant
const Pi = 3.14159

// Typed constant
const Pi float64 = 3.14159

// Multiple constants
const (
    StatusOK    = 200
    StatusError = 500
)

// iota (enumerations)
const (
    Sunday = iota    // 0
    Monday           // 1
    Tuesday          // 2
    Wednesday        // 3
)

const (
    _  = iota             // ignore first value
    KB = 1 << (10 * iota) // 1024
    MB                    // 1048576
    GB                    // 1073741824
)
```

---

## Operators & Expressions

### Arithmetic Operators
```go
+  // Addition
-  // Subtraction
*  // Multiplication
/  // Division
%  // Modulo
++ // Increment (postfix only)
-- // Decrement (postfix only)
```

### Comparison Operators
```go
==  // Equal to
!=  // Not equal to
<   // Less than
>   // Greater than
<=  // Less than or equal
>=  // Greater than or equal
```

### Logical Operators
```go
&&  // Logical AND
||  // Logical OR
!   // Logical NOT
```

### Bitwise Operators
```go
&   // AND
|   // OR
^   // XOR
&^  // AND NOT (bit clear)
<<  // Left shift
>>  // Right shift
```

### Assignment Operators
```go
=   // Assignment
+=  // Addition assignment
-=  // Subtraction assignment
*=  // Multiplication assignment
/=  // Division assignment
%=  // Modulo assignment
&=  // Bitwise AND assignment
|=  // Bitwise OR assignment
^=  // Bitwise XOR assignment
<<= // Left shift assignment
>>= // Right shift assignment
```

### Address Operators
```go
&   // Address of (pointer)
*   // Dereference (value at pointer)
```

---

## Control Flow

### Conditional Statements
```go
// if/else
if condition {
    // code
} else if anotherCondition {
    // code
} else {
    // code
}

// if with initialization
if err := doSomething(); err != nil {
    // handle error
}

// if with multiple conditions
if x > 0 && x < 10 {
    // code
}
```

### Switch Statement
```go
// Basic switch
switch value {
case 1:
    // code
case 2, 3:
    // code (multiple values)
case 4:
    // code
default:
    // code
}

// Switch without condition (like if-else chain)
switch {
case x < 0:
    // code
case x == 0:
    // code
case x > 0:
    // code
}

// Switch with initialization
switch x := getValue(); x {
case 1:
    // code
default:
    // code
}

// Type switch
switch v := i.(type) {
case int:
    fmt.Printf("Integer: %d\n", v)
case string:
    fmt.Printf("String: %s\n", v)
default:
    fmt.Printf("Unknown type\n")
}
```

### Loops
```go
// for loop (only loop in Go)
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// while-style loop
i := 0
for i < 10 {
    fmt.Println(i)
    i++
}

// infinite loop
for {
    // code
    if condition {
        break
    }
}

// range loop (for slices, arrays, maps, strings, channels)
for index, value := range slice {
    fmt.Println(index, value)
}

// range with index only
for i := range slice {
    fmt.Println(i)
}

// range with value only
for _, value := range slice {
    fmt.Println(value)
}
```

### Control Flow Statements
```go
break       // Exit loop or switch
continue    // Skip to next iteration
return      // Exit function
goto        // Jump to label (use sparingly)
```

---

## Functions

### Function Declaration
```go
// Basic function
func greet(name string) {
    fmt.Printf("Hello, %s!\n", name)
}

// Function with return value
func add(a int, b int) int {
    return a + b
}

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func calculate(x, y int) (sum int, product int) {
    sum = x + y
    product = x * y
    return  // Naked return
}

// Variadic function
func sum(numbers ...int) int {
    total := 0
    for _, num := range numbers {
        total += num
    }
    return total
}

// Function as value
var fn func(int, int) int = add
result := fn(5, 3)
```

### Function Types
```go
// Function type
type Operation func(int, int) int

func apply(a, b int, op Operation) int {
    return op(a, b)
}

// Usage
add := func(x, y int) int { return x + y }
result := apply(5, 3, add)
```

### Closures
```go
// Closure example
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

c := counter()
fmt.Println(c()) // 1
fmt.Println(c()) // 2
fmt.Println(c()) // 3
```

### Methods vs Functions
```go
// Function
func Add(a, b int) int {
    return a + b
}

// Method (function with receiver)
type Point struct {
    X, Y float64
}

func (p Point) Distance() float64 {
    return math.Sqrt(p.X*p.X + p.Y*p.Y)
}

// Pointer receiver (can modify)
func (p *Point) Move(dx, dy float64) {
    p.X += dx
    p.Y += dy
}
```

### Defer Statement
```go
// Defer executes when function returns
func example() {
    defer fmt.Println("World")
    fmt.Println("Hello")
}
// Output: Hello\nWorld

// Multiple defers (LIFO - Last In First Out)
func example() {
    defer fmt.Println("First")
    defer fmt.Println("Second")
    defer fmt.Println("Third")
}
// Output: Third\nSecond\nFirst

// Common use case: closing resources
func readFile(filename string) error {
    file, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer file.Close()  // Always closes, even on error
    
    // Read file
    return nil
}
```

---

## Structs & Methods

### Struct Definition
```go
// Basic struct
type Person struct {
    Name string
    Age  int
}

// Struct initialization
p1 := Person{"John", 30}                    // Positional
p2 := Person{Name: "John", Age: 30}         // Named fields
p3 := Person{Name: "John"}                  // Age: 0 (zero value)
p4 := Person{}                               // All zero values

// Pointer to struct
p5 := &Person{Name: "John", Age: 30}
p6 := new(Person)  // Returns pointer with zero values
```

### Struct Methods
```go
type Rectangle struct {
    Width  float64
    Height float64
}

// Value receiver (doesn't modify)
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// Pointer receiver (can modify)
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

// Method call
rect := Rectangle{Width: 10, Height: 5}
area := rect.Area()        // Value receiver
rect.Scale(2)              // Pointer receiver (Go automatically handles &)
```

### Embedded Structs
```go
type Person struct {
    Name string
    Age  int
}

type Employee struct {
    Person           // Embedded struct
    EmployeeID int
    Salary    float64
}

// Usage
emp := Employee{
    Person: Person{Name: "John", Age: 30},
    EmployeeID: 12345,
    Salary: 50000,
}

// Access embedded fields
fmt.Println(emp.Name)      // Direct access
fmt.Println(emp.Person.Age) // Explicit access
```

### Struct Tags
```go
type User struct {
    ID    int    `json:"id" db:"user_id"`
    Name  string `json:"name" validate:"required"`
    Email string `json:"email" validate:"email"`
}
```

---

## Interfaces

### Interface Definition
```go
// Basic interface
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

// Interface usage
func printArea(s Shape) {
    fmt.Printf("Area: %.2f\n", s.Area())
}

circle := Circle{Radius: 5}
printArea(circle)
```

### Empty Interface
```go
// interface{} (or any in Go 1.18+)
var i interface{} = 42
var i any = "hello"  // Go 1.18+

// Type assertion
if s, ok := i.(string); ok {
    fmt.Println(s)
}

// Type switch
switch v := i.(type) {
case int:
    fmt.Printf("Integer: %d\n", v)
case string:
    fmt.Printf("String: %s\n", v)
default:
    fmt.Printf("Unknown type\n")
}
```

### Interface Composition
```go
type Reader interface {
    Read([]byte) (int, error)
}

type Writer interface {
    Write([]byte) (int, error)
}

type ReadWriter interface {
    Reader
    Writer
}
```

### Interface Best Practices
```go
// Prefer small interfaces
type Reader interface {
    Read([]byte) (int, error)
}

// Accept interfaces, return structs
func ProcessData(r Reader) Data {
    // Process
    return data
}
```

---

## Arrays & Slices

### Arrays
```go
// Array declaration
var arr [5]int                    // Zero values
arr := [5]int{1, 2, 3, 4, 5}      // Initialized
arr := [...]int{1, 2, 3, 4, 5}    // Size inferred

// Array operations
len(arr)                          // Length
arr[0]                            // Access element
arr[0] = 10                       // Modify element

// Multi-dimensional array
var matrix [3][3]int
matrix := [3][3]int{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
```

### Slices
```go
// Slice declaration
var s []int                       // nil slice
s := []int{1, 2, 3, 4, 5}        // Literal
s := make([]int, 5)               // Length 5, capacity 5
s := make([]int, 5, 10)           // Length 5, capacity 10

// Slice from array
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]                     // [2, 3, 4]

// Slice operations
len(s)                            // Length
cap(s)                            // Capacity
s[0]                              // Access element
s[0] = 10                         // Modify element
s = append(s, 6)                  // Append element
s = append(s, 7, 8, 9)           // Append multiple
s = append(s, s2...)              // Append slice

// Slice slicing
s := []int{1, 2, 3, 4, 5}
s1 := s[1:3]                      // [2, 3]
s2 := s[:3]                       // [1, 2, 3]
s3 := s[2:]                       // [3, 4, 5]
s4 := s[:]                        // Copy of entire slice
```

### Slice Internals
```go
// Slice header (pointer, length, capacity)
type slice struct {
    ptr    *T
    len    int
    cap    int
}

// Copying slices
s1 := []int{1, 2, 3}
s2 := make([]int, len(s1))
copy(s2, s1)                      // Deep copy

// Iterating slices
for i, v := range s {
    fmt.Println(i, v)
}

for i := range s {
    fmt.Println(i)
}

for _, v := range s {
    fmt.Println(v)
}
```

### Common Slice Operations
```go
// Remove element at index
func remove(s []int, i int) []int {
    return append(s[:i], s[i+1:]...)
}

// Insert element at index
func insert(s []int, i int, v int) []int {
    s = append(s, 0)
    copy(s[i+1:], s[i:])
    s[i] = v
    return s
}

// Filter slice
func filter(s []int, fn func(int) bool) []int {
    var result []int
    for _, v := range s {
        if fn(v) {
            result = append(result, v)
        }
    }
    return result
}
```

---

## Maps

### Map Declaration
```go
// Map declaration
var m map[string]int              // nil map
m := make(map[string]int)          // Empty map
m := map[string]int{               // Literal
    "apple":  5,
    "banana": 3,
}

// Map operations
m["apple"] = 10                    // Set value
value := m["apple"]                // Get value
value, ok := m["apple"]            // Check existence
delete(m, "apple")                 // Delete key
len(m)                             // Number of key-value pairs

// Iterating maps
for key, value := range m {
    fmt.Println(key, value)
}

for key := range m {
    fmt.Println(key)
}
```

### Map Best Practices
```go
// Check if key exists
if value, ok := m["key"]; ok {
    // Key exists
    fmt.Println(value)
}

// Initialize map with capacity
m := make(map[string]int, 100)

// Map of slices
m := make(map[string][]int)
m["numbers"] = []int{1, 2, 3}
```

---

## Pointers

### Pointer Basics
```go
// Pointer declaration
var p *int                         // nil pointer
x := 42
p := &x                            // Address of x

// Dereferencing
value := *p                        // Value at address

// Pointer to pointer
var pp **int = &p

// Pointer to struct
type Point struct {
    X, Y float64
}

p := &Point{X: 1, Y: 2}
(*p).X = 10                        // Explicit dereference
p.X = 10                           // Implicit dereference (Go shorthand)
```

### Pointer Usage
```go
// Passing by reference
func modify(x *int) {
    *x = 100
}

value := 42
modify(&value)
fmt.Println(value)  // 100

// Returning pointer
func newInt() *int {
    v := 42
    return &v  // Go handles memory (escape analysis)
}

// Pointer receiver
func (p *Point) Move(dx, dy float64) {
    p.X += dx
    p.Y += dy
}
```

### nil Pointers
```go
var p *int
if p != nil {
    fmt.Println(*p)
} else {
    fmt.Println("p is nil")
}
```

---

## Error Handling

### Error Interface
```go
// Error is an interface
type error interface {
    Error() string
}

// Creating errors
import "errors"
err := errors.New("something went wrong")

import "fmt"
err := fmt.Errorf("error: %v", value)

// Custom error type
type MyError struct {
    Code    int
    Message string
}

func (e *MyError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}
```

### Error Handling Patterns
```go
// Explicit error checking
result, err := doSomething()
if err != nil {
    return err
}

// Error wrapping (Go 1.13+)
import "errors"
import "fmt"

if err != nil {
    return fmt.Errorf("failed to process: %w", err)
}

// Unwrapping errors
import "errors"
unwrapped := errors.Unwrap(err)

// Checking error types
var targetErr *MyError
if errors.As(err, &targetErr) {
    // Handle MyError
}

// Sentinel errors
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) {
    // Handle not found
}
```

### Panic and Recover
```go
// Panic (unrecoverable error)
panic("something went wrong")

// Recover (catch panic)
func safeFunction() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from:", r)
        }
    }()
    
    panic("panic occurred")
}
```

---

## Concurrency

### Goroutines
```go
// Starting goroutine
go function()

// Example
func sayHello() {
    fmt.Println("Hello")
}

go sayHello()

// Anonymous function
go func() {
    fmt.Println("Hello from goroutine")
}()

// With parameters
go func(name string) {
    fmt.Printf("Hello, %s\n", name)
}("John")
```

### WaitGroup
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

### Mutex
```go
import "sync"

var mu sync.Mutex
var counter int

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++
}

// RWMutex (read-write mutex)
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

---

## Channels

### Channel Basics
```go
// Channel declaration
ch := make(chan int)               // Unbuffered
ch := make(chan int, 10)            // Buffered (capacity 10)

// Sending
ch <- 42

// Receiving
value := <-ch
value, ok := <-ch                   // ok is false if channel closed

// Closing channel
close(ch)

// Channel direction
func send(ch chan<- int) {          // Send-only
    ch <- 42
}

func receive(ch <-chan int) {       // Receive-only
    value := <-ch
}
```

### Channel Patterns
```go
// Range over channel
for value := range ch {
    fmt.Println(value)
}

// Select statement
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

// Fan-out pattern
func fanOut(input <-chan int, outputs []chan<- int) {
    for value := range input {
        for _, out := range outputs {
            select {
            case out <- value:
            default:
            }
        }
    }
}

// Fan-in pattern
func fanIn(inputs []<-chan int, output chan<- int) {
    var wg sync.WaitGroup
    for _, in := range inputs {
        wg.Add(1)
        go func(ch <-chan int) {
            defer wg.Done()
            for value := range ch {
                output <- value
            }
        }(in)
    }
    go func() {
        wg.Wait()
        close(output)
    }()
}
```

### Channel Best Practices
```go
// Close channels to signal completion
// Only sender should close channel
// Check if channel is closed
value, ok := <-ch
if !ok {
    // Channel closed
}

// Use buffered channels to prevent blocking
ch := make(chan int, 100)
```

---

## Goroutines

### Goroutine Patterns
```go
// Worker pool pattern
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

// Pipeline pattern
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

---

## Packages & Modules

### Package Declaration
```go
// Package declaration (first line)
package main

// Import packages
import "fmt"
import "math"

// Multiple imports
import (
    "fmt"
    "math"
    "os"
)

// Import with alias
import f "fmt"
f.Println("Hello")

// Blank import (for side effects)
import _ "database/sql/driver"
```

### Creating Packages
```go
// utils/helper.go
package utils

import "fmt"

// Exported function (capitalized)
func Greet(name string) {
    fmt.Printf("Hello, %s!\n", name)
}

// Unexported function (lowercase)
func greet(name string) {
    fmt.Printf("Hello, %s!\n", name)
}
```

### Go Modules
```go
// Initialize module
go mod init example.com/myproject

// go.mod file
module example.com/myproject

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
)

// Add dependency
go get github.com/gin-gonic/gin

// Update dependencies
go get -u ./...

// Remove unused dependencies
go mod tidy

// Vendor dependencies
go mod vendor
```

---

## I/O Operations

### File Operations
```go
import (
    "os"
    "io"
    "bufio"
)

// Reading file
file, err := os.Open("file.txt")
if err != nil {
    log.Fatal(err)
}
defer file.Close()

// Read all
data, err := os.ReadFile("file.txt")

// Read line by line
scanner := bufio.NewScanner(file)
for scanner.Scan() {
    line := scanner.Text()
    fmt.Println(line)
}

// Writing file
data := []byte("Hello, World!")
err := os.WriteFile("output.txt", data, 0644)

// Writing line by line
file, err := os.Create("output.txt")
if err != nil {
    log.Fatal(err)
}
defer file.Close()

writer := bufio.NewWriter(file)
writer.WriteString("Hello\n")
writer.Flush()
```

### Standard I/O
```go
import (
    "fmt"
    "os"
)

// Reading from stdin
scanner := bufio.NewScanner(os.Stdin)
for scanner.Scan() {
    line := scanner.Text()
    fmt.Println("You entered:", line)
}

// Writing to stdout/stderr
fmt.Print("Hello")
fmt.Println("World")
fmt.Printf("Value: %d\n", 42)
fmt.Fprintf(os.Stderr, "Error: %v\n", err)
```

---

## JSON & Encoding

### JSON Encoding/Decoding
```go
import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

// Encoding (struct to JSON)
person := Person{Name: "John", Age: 30}
jsonData, err := json.Marshal(person)
if err != nil {
    log.Fatal(err)
}
fmt.Println(string(jsonData))  // {"name":"John","age":30}

// Pretty print
jsonData, err := json.MarshalIndent(person, "", "  ")

// Decoding (JSON to struct)
var person Person
jsonStr := `{"name":"John","age":30}`
err := json.Unmarshal([]byte(jsonStr), &person)
if err != nil {
    log.Fatal(err)
}

// Decoding to map
var result map[string]interface{}
json.Unmarshal([]byte(jsonStr), &result)
```

### Custom JSON Marshaling
```go
type CustomDate struct {
    time.Time
}

func (d CustomDate) MarshalJSON() ([]byte, error) {
    return []byte(fmt.Sprintf(`"%s"`, d.Format("2006-01-02"))), nil
}

func (d *CustomDate) UnmarshalJSON(data []byte) error {
    str := strings.Trim(string(data), `"`)
    t, err := time.Parse("2006-01-02", str)
    if err != nil {
        return err
    }
    d.Time = t
    return nil
}
```

---

## Testing

### Unit Testing
```go
// math_test.go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5
    if result != expected {
        t.Errorf("Add(2, 3) = %d; expected %d", result, expected)
    }
}

// Table-driven tests
func TestAddTable(t *testing.T) {
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
            t.Errorf("Add(%d, %d) = %d; expected %d",
                tt.a, tt.b, result, tt.expected)
        }
    }
}

// Running tests
// go test
// go test -v          // Verbose
// go test -run TestAdd  // Run specific test
// go test -cover      // Coverage
```

### Benchmarking
```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}

// Running benchmarks
// go test -bench=.
// go test -bench=BenchmarkAdd
// go test -benchmem  // Memory allocation stats
```

### Example Tests
```go
func ExampleAdd() {
    result := Add(2, 3)
    fmt.Println(result)
    // Output: 5
}
```

---

## Reflection

### Reflection Basics
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

---

## Context

### Context Package
```go
import (
    "context"
    "time"
)

// Background context
ctx := context.Background()

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// With deadline
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// With value
ctx := context.WithValue(context.Background(), "key", "value")
value := ctx.Value("key")

// With cancellation
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// Check if context is done
select {
case <-ctx.Done():
    fmt.Println("Context cancelled")
    return ctx.Err()
default:
    // Continue
}
```

### Context Best Practices
```go
// Pass context as first parameter
func processData(ctx context.Context, data []byte) error {
    // Check context
    if ctx.Err() != nil {
        return ctx.Err()
    }
    
    // Long-running operation
    select {
    case <-ctx.Done():
        return ctx.Err()
    case result := <-longOperation():
        // Process result
    }
    return nil
}
```

---

## Best Practices

### Code Organization
1. **Package naming**: lowercase, single word
2. **File naming**: snake_case.go
3. **Function naming**: camelCase, exported functions capitalized
4. **Constants**: UPPER_SNAKE_CASE
5. **Error handling**: Always check errors
6. **Defer**: Use for cleanup
7. **Interfaces**: Keep small, prefer composition

### Error Handling
```go
// Always check errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed: %w", err)
}

// Don't ignore errors
_, err := doSomething()
if err != nil {
    log.Printf("Warning: %v", err)
}
```

### Performance
```go
// Pre-allocate slices when size is known
s := make([]int, 0, 100)  // Length 0, capacity 100

// Use strings.Builder for string concatenation
var builder strings.Builder
for i := 0; i < 1000; i++ {
    builder.WriteString("text")
}
result := builder.String()

// Avoid unnecessary allocations
// Use sync.Pool for frequently allocated objects
var pool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

buf := pool.Get().([]byte)
defer pool.Put(buf)
```

### Concurrency Best Practices
```go
// Use channels for communication
// Use mutexes for shared state protection
// Avoid sharing memory, share by communicating
// Use context for cancellation
// Always close channels when done
// Use select for non-blocking operations
```

---

## Advanced Topics

### Generics (Go 1.18+)
```go
// Generic function
func Swap[T any](a, b T) (T, T) {
    return b, a
}

// Usage
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

### Embedding
```go
// Interface embedding
type Reader interface {
    Read([]byte) (int, error)
}

type Writer interface {
    Write([]byte) (int, error)
}

type ReadWriter interface {
    Reader
    Writer
}

// Struct embedding
type Person struct {
    Name string
}

type Employee struct {
    Person
    EmployeeID int
}

// Method promotion
func (p Person) Greet() {
    fmt.Printf("Hello, I'm %s\n", p.Name)
}

emp := Employee{Person: Person{Name: "John"}, EmployeeID: 123}
emp.Greet()  // Method promoted from Person
```

### Build Tags
```go
// +build linux darwin

package main

// File only compiled on Linux and Darwin
```

### CGO
```go
/*
#include <stdio.h>
void hello() {
    printf("Hello from C\n");
}
*/
import "C"

func main() {
    C.hello()
}
```

### Unsafe Package
```go
import "unsafe"

// Size of type
size := unsafe.Sizeof(x)

// Pointer arithmetic
ptr := unsafe.Pointer(&x)
offset := unsafe.Pointer(uintptr(ptr) + offset)
```

---

## Resources for Further Learning

1. **Go Official Documentation** - https://golang.org/doc/
2. **Effective Go** - Go best practices guide
3. **Go by Example** - Hands-on examples
4. **The Go Programming Language** - Book by Donovan & Kernighan
5. **Go Blog** - Official Go blog
6. **Awesome Go** - Curated list of Go packages
7. **Go Playground** - Online Go compiler
8. **Go Weekly** - Weekly Go newsletter

---

## Conclusion

This guide covers Go from fundamentals to advanced topics. Mastery comes through:
- **Practice**: Build projects, solve problems
- **Understanding**: Know why, not just how
- **Reading**: Study well-written Go code (standard library)
- **Teaching**: Explain concepts to others
- **Staying Current**: Follow Go evolution

Remember: Go emphasizes simplicity, clarity, and concurrency. Keep learning, keep practicing, and keep building!

### Key Takeaways
- Go is simple, fast, and concurrent
- Master goroutines and channels for concurrency
- Understand interfaces and type system
- Use slices and maps effectively
- Handle errors explicitly
- Follow Go idioms and best practices
- Leverage the standard library
- Write clear, readable code

