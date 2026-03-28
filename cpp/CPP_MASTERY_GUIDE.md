# The Complete C++ Mastery Guide
> Every concept from first principles — memory model, RAII, templates, STL, move semantics, concurrency, the preprocessor, file I/O, design patterns, testing, and build systems. Written to the same depth as a professional reference.

---

## Table of Contents

### Part I — Foundations
1. [Why C++? Philosophy & Design](#chapter-1-why-c-philosophy--design)
2. [Compilation Model & Build Systems](#chapter-2-compilation-model--build-systems)
3. [Types, Variables & Literals](#chapter-3-types-variables--literals)
4. [Operators & Expressions](#chapter-4-operators--expressions)
5. [Control Flow](#chapter-5-control-flow)
6. [Functions — Full Coverage](#chapter-6-functions--full-coverage)
7. [The Memory Model — Stack, Heap, Pointers, References](#chapter-7-the-memory-model)
8. [The Preprocessor](#chapter-8-the-preprocessor)

### Part II — Object-Oriented C++
9. [Classes & Objects — Deep Dive](#chapter-9-classes--objects--deep-dive)
10. [Constructors, Destructors & RAII](#chapter-10-constructors-destructors--raii)
11. [Operator Overloading](#chapter-11-operator-overloading)
12. [Inheritance & Polymorphism](#chapter-12-inheritance--polymorphism)
13. [Templates & Generic Programming](#chapter-13-templates--generic-programming)

### Part III — Modern C++ (C++11 → C++23)
14. [Move Semantics & Rvalue References](#chapter-14-move-semantics--rvalue-references)
15. [Smart Pointers](#chapter-15-smart-pointers)
16. [Lambda Expressions](#chapter-16-lambda-expressions)
17. [Type Deduction — auto, decltype, Concepts](#chapter-17-type-deduction)

### Part IV — Standard Library
18. [Strings — Deep Dive](#chapter-18-strings--deep-dive)
19. [Containers — Complete STL](#chapter-19-containers--complete-stl)
20. [Algorithms & Ranges](#chapter-20-algorithms--ranges)
21. [Utility Types — optional, variant, any, span](#chapter-21-utility-types)
22. [File I/O & Streams](#chapter-22-file-io--streams)

### Part V — Systems & Concurrency
23. [Error Handling — Exceptions & std::expected](#chapter-23-error-handling)
24. [Concurrency — Threads, Mutexes, Atomics, Futures](#chapter-24-concurrency)
25. [Memory Management — Advanced](#chapter-25-memory-management--advanced)

### Part VI — Advanced Topics
26. [Metaprogramming & constexpr](#chapter-26-metaprogramming--constexpr)
27. [Design Patterns in C++](#chapter-27-design-patterns-in-c)
28. [Testing — Catch2, GoogleTest](#chapter-28-testing)
29. [Build Systems — CMake, vcpkg, Conan](#chapter-29-build-systems)
30. [Performance & Optimization](#chapter-30-performance--optimization)
31. [Best Practices & Undefined Behavior](#chapter-31-best-practices--undefined-behavior)

---

# PART I — FOUNDATIONS

---

## Chapter 1: Why C++? Philosophy & Design

### 1.1 The Core Mission — Zero-Overhead Abstraction

C++ was created by Bjarne Stroustrup starting in 1979 (as "C with Classes", standardized in 1998). Its design principle has never changed:

> **"You don't pay for what you don't use."**

This means every abstraction C++ provides — classes, virtual functions, templates, exceptions — compiles down to the same (or better) machine code as hand-written C. If you don't use virtual functions, you pay nothing for the vtable mechanism. If you don't use exceptions, the runtime cost is zero.

```
C++ performance spectrum:
  Raw arrays → std::array → std::vector → std::deque
  Cost:         =zero       =zero          =near-zero    (slight overhead for bounds)

  No virtual → virtual function
  Cost:         direct call   indirect call via vtable (~1-3ns on modern CPUs)

  No exceptions → exceptions enabled
  Cost (happy path): zero (table-driven EH; only costs when exception actually thrown)
```

### 1.2 C++ vs Other Languages — Engineering Tradeoffs

```
Language   GC?    Manual Mem  Overhead    Concurrency    Use case
─────────────────────────────────────────────────────────────────
C          No     Yes         Near-zero   POSIX only     OS kernels, embedded
C++        No     Optional    Near-zero   Full std lib   Systems, games, HFT, ML
Rust       No     Borrow chk  Near-zero   Full std lib   Systems, WebAssembly
Java       GC     No          JVM+GC      Full std lib   Enterprise, Android
Go         GC     No          GC pauses   Goroutines     Microservices, tools
Python     GC     No          Interpreter GIL limits     Scripting, data science

C++ excels when:
  ① Predictable latency required (no GC pauses): game engines, HFT, real-time systems
  ② Direct hardware control: OS, device drivers, embedded systems
  ③ Maximum CPU performance: ML inference, scientific computing, databases
  ④ Existing C++ codebase: Chromium, LLVM, MySQL, Unreal Engine, Qt

C++ is NOT ideal when:
  ① Rapid prototyping — Python is faster to write
  ② Web frontends — JavaScript/TypeScript
  ③ Mobile apps — Kotlin/Swift (though C++ via NDK/JNI is used for performance-critical parts)
```

### 1.3 C++ Standard Versions

```
C++98/03:  First standard. Templates, STL, exceptions. Foundation of everything.
           Problem: no move semantics → copies everywhere. No lambdas → verbose.

C++11:     THE revolution. Everything changed:
           • Move semantics + rvalue references → zero-cost ownership transfer
           • Smart pointers (unique_ptr, shared_ptr) → no raw new/delete
           • Lambdas → inline anonymous functions
           • auto type deduction → less boilerplate
           • nullptr → replaces NULL (safer)
           • Range-based for loop
           • constexpr → compile-time computation
           • Threads, atomics, futures → standard concurrency
           • initializer_list, uniform initialization
           • override, final → explicit virtual semantics
           • = delete, = default → explicit special member control
           • Variadic templates
           
C++14:     Refinements: generic lambdas (auto params), variable templates,
           make_unique, relaxed constexpr, digit separators (1'000'000).

C++17:     Significant additions:
           • Structured bindings: auto [x, y] = pair;
           • if constexpr → compile-time branching in templates
           • std::optional, std::variant, std::any
           • std::string_view → non-owning string reference
           • Parallel algorithms: std::sort(std::execution::par, ...)
           • Fold expressions → cleaner variadic templates
           • Class template argument deduction (CTAD): vector v{1,2,3};
           • Filesystem library (std::filesystem)
           • Inline variables

C++20:     Second revolution:
           • Concepts → constrained templates (readable error messages!)
           • Ranges + Views → lazy pipelines with | operator
           • Coroutines → co_await, co_yield, co_return
           • Modules → replacement for #include (faster compilation)
           • std::format → Python-style formatting
           • Three-way comparison operator <=> (spaceship)
           • std::span → non-owning view of contiguous memory
           • Designated initializers: Widget{.x=1, .y=2}
           • consteval, constinit
           • std::jthread → auto-joining thread

C++23:     std::expected (Rust-style Result), std::print, std::mdspan,
           ranges improvements, std::generator coroutine.

Write C++17 as minimum. Use C++20 where compiler support allows.
```

---

## Chapter 2: Compilation Model & Build Systems

### 2.1 The Full Compilation Pipeline

```
Source file: hello.cpp
      │
      ▼  ① Preprocessor (cpp)
         - Expands #include (textual insertion of header files)
         - Expands #define macros
         - Processes #ifdef / #ifndef / #endif
         - Strips comments
         → produces: Translation Unit (.i file, rarely seen directly)
      │
      ▼  ② Compiler (cc1/clang -cc1)
         - Parses C++ syntax
         - Type checking
         - Semantic analysis
         - Optimization (if -O1/-O2/-O3)
         - Code generation (AST → IR → machine code)
         → produces: Object file (.o / .obj)
      │
      ▼  ③ Linker (ld / lld / link.exe)
         - Combines multiple .o files
         - Resolves external symbols (finds definitions across files)
         - Links against static libraries (.a / .lib)
         - Records dynamic library dependencies (.so / .dll)
         → produces: Executable or shared library
```

```bash
# The four stages explicitly:
g++ -E   hello.cpp -o hello.i    # ① Preprocessing only
g++ -S   hello.cpp -o hello.s    # ② + Compile to assembly
g++ -c   hello.cpp -o hello.o    # ③ + Assemble to object file
g++ hello.o -o hello             # ④ Link to executable

# Normally: do all in one command
g++ -std=c++20 -Wall -Wextra -O2 hello.cpp -o hello

# See what the compiler actually produces (assembly):
g++ -std=c++20 -O2 -S -fverbose-asm hello.cpp -o hello.s
# Or view at https://godbolt.org (Compiler Explorer)

# See what symbols are defined/undefined in an object file:
nm hello.o
# Useful flags: nm -C (demangle C++ names), nm --defined-only

# Essential flags to always use:
# -std=c++17 or -std=c++20       — C++ standard
# -Wall -Wextra -Wpedantic        — all important warnings
# -Werror                          — treat warnings as errors (CI)
# -O0 -g                           — debug build (no optimization, debug symbols)
# -O2 or -O3                       — release build optimization
# -fsanitize=address               — AddressSanitizer: finds buffer overflows, UAF, leaks
# -fsanitize=undefined             — UBSanitizer: finds undefined behavior
# -fsanitize=thread                — ThreadSanitizer: finds data races
# -march=native -mtune=native      — optimize for your specific CPU
# -fno-omit-frame-pointer          — better stack traces in profiler
# -DNDEBUG                         — disable assert() in release builds
# -fvisibility=hidden              — hide symbols by default in shared libs
```

### 2.2 Headers, Source Files, and the ODR

```cpp
// The One Definition Rule (ODR):
// A declaration may appear many times (in multiple headers/source files).
// A DEFINITION may appear only ONCE across the entire program.

// Good: declaration in header, definition in .cpp
// ─────────────────────────────────────────────
// math.hpp
#pragma once           // include guard: prevents double-inclusion in single TU
                       // equivalent to: #ifndef MATH_HPP / #define MATH_HPP / ... / #endif

double square(double x);      // DECLARATION: just the signature
double cube(double x);

class Vector2D {              // class definition in header is fine (ODR applies to members)
public:
    double x, y;
    Vector2D(double x, double y);
    double length() const;    // member function DECLARATION
};

// math.cpp
#include "math.hpp"

double square(double x) { return x * x; }  // DEFINITION: only here
double cube(double x)   { return x * x * x; }

Vector2D::Vector2D(double x, double y) : x{x}, y{y} {}

double Vector2D::length() const {
    return std::sqrt(x*x + y*y);
}

// EXCEPTION — these CAN be defined in headers (each TU gets its own copy; ODR exemption):
inline double fast_square(double x) { return x * x; }  // inline function
template <typename T> T max2(T a, T b) { return a > b ? a : b; } // template
constexpr int BUFFER = 4096;        // constexpr variable (C++17: inline variable)
inline int global_counter = 0;      // inline variable (C++17)
```

### 2.3 Linking — Static vs Dynamic Libraries

```bash
# Static library (.a on Unix, .lib on Windows) — linked INTO the executable
ar rcs libmath.a math.o utils.o      # create static library
g++ main.o -L. -lmath -o program     # link against it
# Result: all library code embedded in executable (larger binary, no runtime dependency)

# Shared/dynamic library (.so on Unix, .dll on Windows) — loaded at runtime
g++ -fPIC -shared math.o -o libmath.so    # create shared library (-fPIC: position-independent code)
g++ main.o -L. -lmath -Wl,-rpath,. -o program  # link + set runtime path
# Result: smaller executable; library loaded dynamically; can update library without recompiling main

# Viewing an executable's dynamic dependencies:
ldd program        # Linux: show all dynamic libraries needed
otool -L program   # macOS equivalent
```

### 2.4 CMake — Complete Reference

```cmake
# CMakeLists.txt — the definitive build file

cmake_minimum_required(VERSION 3.20)   # minimum CMake version

project(MyProject
    VERSION 2.1.0
    DESCRIPTION "My awesome C++ project"
    LANGUAGES CXX C               # languages used
)

# ── C++ Standard ──────────────────────────────────────────────
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # error if compiler doesn't support it
set(CMAKE_CXX_EXTENSIONS OFF)        # use -std=c++20, not -std=gnu++20 (important for portability)

# ── Compiler Options ──────────────────────────────────────────
# Warnings (per-target is better than global)
add_compile_options(
    -Wall -Wextra -Wpedantic          # most warnings
    -Wno-unused-parameter             # suppress specific warning
)

# Build type configuration
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0 -fsanitize=address,undefined)
    add_link_options(-fsanitize=address,undefined)
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_options(-O3 -DNDEBUG -march=native)
elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
    add_compile_options(-O2 -g -DNDEBUG)
endif()

# ── Executables ───────────────────────────────────────────────
add_executable(myapp
    src/main.cpp
    src/app.cpp
    src/utils.cpp
)

# ── Libraries ─────────────────────────────────────────────────
add_library(mylib STATIC    # STATIC, SHARED, or INTERFACE (header-only)
    src/lib/math.cpp
    src/lib/string_utils.cpp
)

# Header-only library (INTERFACE: no compiled source)
add_library(myheaders INTERFACE)
target_include_directories(myheaders INTERFACE include/)

# ── Include Directories ───────────────────────────────────────
# PUBLIC: used by this target AND targets linking against it
# PRIVATE: only used by this target
# INTERFACE: only used by targets linking against it (header-only libs)
target_include_directories(mylib
    PUBLIC  include/               # headers for users of mylib
    PRIVATE src/internal/          # implementation headers
)
target_include_directories(myapp PRIVATE src/)

# ── Linking ───────────────────────────────────────────────────
target_link_libraries(myapp
    PRIVATE mylib          # link mylib; don't expose to myapp's users
    PRIVATE myheaders      # header-only library
    PRIVATE pthread        # system library
)

# ── Compiler Features per Target ──────────────────────────────
target_compile_features(myapp PRIVATE cxx_std_20)

# ── External Dependencies ──────────────────────────────────────
# Method 1: find_package (installed on system or via vcpkg/conan)
find_package(fmt REQUIRED)
find_package(GTest REQUIRED)
find_package(Boost COMPONENTS filesystem REQUIRED)
target_link_libraries(myapp PRIVATE fmt::fmt Boost::filesystem)

# Method 2: FetchContent (downloads at configure time)
include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
)
FetchContent_MakeAvailable(googletest)
target_link_libraries(tests PRIVATE GTest::gtest_main)

# ── Testing ───────────────────────────────────────────────────
enable_testing()
add_executable(unit_tests
    tests/math_test.cpp
    tests/utils_test.cpp
)
target_link_libraries(unit_tests PRIVATE mylib GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(unit_tests)    # auto-discovers TEST() and TEST_F() macros

# ── Installation ──────────────────────────────────────────────
install(TARGETS myapp mylib DESTINATION bin)
install(DIRECTORY include/ DESTINATION include)

# ── Custom Targets ────────────────────────────────────────────
add_custom_target(format
    COMMAND clang-format -i src/*.cpp include/*.hpp
    COMMENT "Formatting source files"
)
add_custom_target(lint
    COMMAND clang-tidy src/*.cpp -- -std=c++20
)
```

```bash
# Build workflow
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug         # configure
cmake --build . --parallel $(nproc)       # build (all cores)
ctest --output-on-failure                 # run tests
cmake --install . --prefix /usr/local     # install

# Release build
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/myapp
cmake --build . -j$(nproc)

# Presets (CMakePresets.json — modern approach)
cmake --preset debug                      # use named preset
cmake --build --preset debug
ctest --preset debug
```

---

## Chapter 3: Types, Variables & Literals

### 3.1 Fundamental Types — Complete Reference

```cpp
#include <cstdint>   // fixed-width integers
#include <cstddef>   // size_t, ptrdiff_t, nullptr_t
#include <limits>    // numeric_limits

// ── Boolean ──────────────────────────────────────────────────
bool b = true;               // true or false; sizeof(bool) typically 1

// ── Character Types ───────────────────────────────────────────
char         c1 = 'A';       // 1 byte; signed or unsigned (implementation-defined!)
signed char  c2 = -1;        // 1 byte; always signed; -128 to 127
unsigned char c3 = 255;      // 1 byte; always unsigned; 0 to 255
wchar_t      c4 = L'©';     // wide char; 2 bytes on Windows, 4 on Linux
char8_t      c5 = u8'a';    // UTF-8 code unit (C++20); 1 byte unsigned
char16_t     c6 = u'©';     // UTF-16 code unit (C++11); 2 bytes unsigned
char32_t     c7 = U'©';     // UTF-32 code point (C++11); 4 bytes unsigned

// ── Integer Types ─────────────────────────────────────────────
short int   s  = 32767;      // at least 16 bits; usually 16
int         i  = 2147483647; // at least 16 bits; usually 32; DEFAULT integer type
long int    l  = 2147483647L; // at least 32 bits; 32 on Windows x64, 64 on Linux x64
long long   ll = 9223372036854775807LL; // at least 64 bits; ALWAYS 64 bits

unsigned short  us  = 65535U;
unsigned int    ui  = 4294967295U;
unsigned long   ul  = 4294967295UL;
unsigned long long ull = 18446744073709551615ULL;

// Fixed-width types (ALWAYS use these when size matters)
int8_t    i8  = -128;             uint8_t   u8  = 255;
int16_t   i16 = -32768;           uint16_t  u16 = 65535;
int32_t   i32 = -2147483648;      uint32_t  u32 = 4294967295U;
int64_t   i64 = INT64_MIN;        uint64_t  u64 = UINT64_MAX;

// Minimum-width types (at least N bits, possibly larger)
int_least8_t   li8;
int_fast8_t    fi8;    // fastest type with at least 8 bits (might be 32-bit on some CPUs)

// Pointer-sized types
size_t    sz  = sizeof(int);         // unsigned; holds any object size; return type of sizeof
ptrdiff_t pd  = ptr2 - ptr1;        // signed; difference between two pointers
intptr_t  ip  = (intptr_t)ptr;      // signed integer that can hold a pointer
uintptr_t up  = (uintptr_t)ptr;     // unsigned equivalent

// ── Floating Point ────────────────────────────────────────────
float       f  = 3.14f;              // 32-bit IEEE 754; ~7 sig. digits; 'f' suffix
double      d  = 3.14159265358979;   // 64-bit IEEE 754; ~15 sig. digits; DEFAULT
long double ld = 3.14159265358979L;  // 80-bit (x86 extended) or 128-bit; 'L' suffix

// Special floating-point values
double pos_inf = std::numeric_limits<double>::infinity();      // +∞
double neg_inf = -std::numeric_limits<double>::infinity();     // -∞
double nan     = std::numeric_limits<double>::quiet_NaN();     // NaN (Not a Number)
bool is_inf    = std::isinf(pos_inf);     // true
bool is_nan    = std::isnan(nan);         // true

// Numeric limits
std::cout << std::numeric_limits<int>::max()         << "\n"; // 2147483647
std::cout << std::numeric_limits<int>::min()         << "\n"; // -2147483648
std::cout << std::numeric_limits<double>::epsilon()  << "\n"; // ~2.22e-16 (machine epsilon)
std::cout << std::numeric_limits<double>::max()      << "\n"; // ~1.8e+308
std::cout << std::numeric_limits<float>::lowest()    << "\n"; // -3.4e+38
std::cout << sizeof(int)                             << "\n"; // 4 (bytes)
std::cout << alignof(double)                         << "\n"; // 8 (alignment requirement)
```

### 3.2 Literals — All Forms

```cpp
// ── Integer Literals ──────────────────────────────────────────
int dec  = 42;            // decimal
int oct  = 052;           // octal (leading 0)
int hex  = 0x2A;          // hexadecimal
int bin  = 0b00101010;    // binary (C++14)
// Digit separators (C++14):
int big  = 1'000'000;           // readable million
int hex2 = 0xFF'FF'FF'FF;       // readable hex
long long big64 = 9'223'372'036'854'775'807LL;

// Suffixes
unsigned  u  = 42U;
long      l  = 42L;
long long ll = 42LL;
unsigned long long ull = 42ULL;

// ── Floating-Point Literals ───────────────────────────────────
double d1 = 3.14;          // double (default)
float  f1 = 3.14f;         // float (f or F suffix)
double d2 = 3.14e2;        // scientific: 314.0
double d3 = 0x1.8p1;       // hexadecimal float: 1.5 × 2¹ = 3.0

// ── Character Literals ────────────────────────────────────────
char     c1 = 'A';          // ASCII character
char     c2 = '\n';         // newline escape
char     c3 = '\t';         // tab
char     c4 = '\\';         // backslash
char     c5 = '\'';         // single quote
char     c6 = '\0';         // null character
char     c7 = '\x41';       // hex escape: 'A'
char     c8 = '\101';       // octal escape: 'A'
wchar_t  w1 = L'©';        // wide character
char32_t u1 = U'©';        // UTF-32
char16_t u2 = u'©';        // UTF-16

// ── String Literals ───────────────────────────────────────────
const char*    s1 = "hello";              // C-string; null-terminated
const wchar_t* s2 = L"hello";            // wide string
const char8_t* s3 = u8"hello";           // UTF-8 (C++20: type is const char8_t*)
const char16_t* s4 = u"héllo";          // UTF-16
const char32_t* s5 = U"héllo";          // UTF-32

// Raw string literals (C++11) — no escaping, exactly as written
const char* path = R"(C:\Users\Alice\Documents\file.txt)";  // path as-is
const char* regex = R"(\d+\.\d+)";           // regex without double-backslash
const char* json  = R"json({
    "name": "Alice",
    "age": 30,
    "active": true
})json";   // delimiter after R" and before ) — can be anything

// std::string literals (C++14 — using namespace std::string_literals)
using namespace std::literals;
std::string str1 = "hello"s;             // std::string, not const char*
std::string str2 = "hello\nworld"s;

// std::string_view literals (C++17)
using namespace std::string_view_literals;
std::string_view sv = "hello"sv;

// ── Boolean Literals ─────────────────────────────────────────
bool t = true;
bool f = false;

// ── nullptr ───────────────────────────────────────────────────
int*  p  = nullptr;        // null pointer constant (C++11; replaces NULL and 0)
void* vp = nullptr;
// NULL is just 0 or (void*)0 — confusable with int; nullptr has type nullptr_t
```

### 3.3 Variable Declaration and Initialization

```cpp
// C++ has multiple initialization syntaxes — they have subtle differences

// ① Default initialization — leaves fundamental types UNINITIALIZED (garbage)
int i;                 // UNINITIALIZED — reading this is UB!
double d;              // UNINITIALIZED
std::string s;         // OK: string has a constructor → empty string

// ② Copy initialization
int a = 5;
double b = 3.14;
std::string s2 = "hello";   // constructs from const char*

// ③ Direct initialization
int c(5);
double e(3.14);
std::vector<int> v(10);     // 10-element vector

// ④ List / Brace initialization (C++11) — PREFERRED for almost everything
// Advantage: prevents narrowing conversions (compile error instead of silent truncation)
int x{5};
double y{3.14};
std::string s3{"hello"};
std::vector<int> v2{1, 2, 3, 4, 5};   // initializer-list constructor

int bad{3.99};    // ❌ COMPILE ERROR: narrowing — 3.99 doesn't fit exactly in int
int ok = 3.99;    // ✅ compiles, but silently truncates to 3 (dangerous!)

// ⑤ Value initialization — zero-initializes fundamental types
int z{};          // 0
double d2{};      // 0.0
bool b2{};        // false
int* p{};         // nullptr
std::string s4{}; // ""

// ⑥ Zero initialization (static/global scope — always happens automatically)
static int global;   // 0 (guaranteed before any other initialization)
int array[5] = {};   // {0,0,0,0,0}

// auto — type deduction (C++11) — infers type from initializer
auto i2   = 42;           // int
auto d3   = 3.14;         // double
auto s5   = std::string{"hello"};  // std::string
auto c2   = 'X';          // char
auto ptr  = new int{5};   // int*
auto f3   = 3.14f;        // float (f suffix needed)
auto &ref = i2;           // int& (reference to i2)
const auto& cr = i2;      // const int& (const reference)

// auto strips top-level const and references:
const int ci = 5;
auto a2  = ci;            // a2 is int (not const int — top-level const stripped)
auto &a3 = ci;            // a3 is const int& (const preserved for references)
const auto a4 = ci;       // a4 is const int (explicit const added back)

// decltype — exact type of expression (doesn't strip const/ref)
int n = 5;
decltype(n)    d4 = 10;   // int (same type as n)
decltype((n))  d5 = n;    // int& (parenthesized expression = lvalue reference)
decltype(n+1)  d6 = 20;   // int (expression result type)

// Structured bindings (C++17) — unpack pairs, tuples, structs, arrays
auto [x2, y2]     = std::pair{3.0, 4.0};    // x2=double(3.0), y2=double(4.0)
auto [key, value] = *myMap.begin();          // unpack map entry
auto& [k, v]      = *myMap.begin();          // reference binding (modifies map)
auto [a, b, c]    = std::tuple{1, 2.0, "hi"}; // triple
auto [i3, j3]     = std::array{10, 20};      // from array

// Structured bindings with for
for (const auto& [name, score] : scores_map) {
    std::cout << name << ": " << score << "\n";
}
```

### 3.4 const, constexpr, constinit, consteval

```cpp
// const — value cannot change after initialization (runtime or compile-time)
const int MAX_SIZE = 100;
const std::string APP_NAME = "MyApp";
// MAX_SIZE = 200;  // ❌ COMPILE ERROR

// const pointer nuances (read right-to-left: "X is a Y")
int value = 42;
const int* p1 = &value;     // p1 is a pointer to const int
                              // → CAN change where p1 points (p1 = &other)
                              // → CANNOT change value through p1 (*p1 = 99) ❌
int* const p2 = &value;     // p2 is a const pointer to int
                              // → CANNOT change where p2 points ❌
                              // → CAN change value through p2 (*p2 = 99) ✅
const int* const p3 = &value; // const pointer to const int — neither can change

// constexpr (C++11) — computed at compile time; can also be called at runtime
constexpr int square(int n) { return n * n; }
constexpr int area = square(5);    // 25 — compile-time computation
// Now usable as compile-time constant:
std::array<int, square(5)> arr;    // array size must be compile-time constant ✅
static_assert(square(5) == 25);    // compile-time assertion ✅

// constexpr variables
constexpr double PI = 3.14159265358979323846;
constexpr int BUFFER_SIZE = 64 * 1024;   // 65536 — computed at compile time

// constexpr function rules (C++11-14 strict; C++14+ relaxed):
// C++14+: can have if, for, while, local variables, multiple return statements
constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
constexpr int fib10 = fibonacci(10);   // 55 — computed at compile time!

// C++20: almost any code can be constexpr (new, if consteval, etc.)
constexpr std::vector<int> makeVector() {   // constexpr vector! (C++20)
    std::vector<int> v;
    for (int i = 0; i < 5; ++i) v.push_back(i * i);
    return v;  // {0,1,4,9,16}
}

// consteval (C++20) — MUST be compile-time; runtime call is a COMPILE ERROR
consteval int mustCompileTime(int n) { return n * n; }
constexpr int r1 = mustCompileTime(5);  // ✅ compile-time
// int x = 5; mustCompileTime(x);        // ❌ COMPILE ERROR: x is not constant

// constinit (C++20) — initialized at compile time but CAN change later
// Solves "static initialization order fiasco" for global variables
constinit int global = computeAtCompileTime();  // guaranteed compile-time init
global = 42;   // can change later (unlike constexpr)
```

---

## Chapter 4: Operators & Expressions

### 4.1 Arithmetic and Assignment

```cpp
int a = 17, b = 5;

// Arithmetic
a + b    // 22
a - b    // 12
a * b    // 85
a / b    // 3   (integer division: truncates toward zero)
a % b    // 2   (modulo; same sign as dividend in C++: -7%2 = -1)

// Integer overflow is UNDEFINED BEHAVIOR for SIGNED types
int max = INT_MAX;
max + 1;             // UB — could wrap, trap, or do anything
unsigned int um = UINT_MAX;
um + 1;              // 0 — wrapping is DEFINED for unsigned

// Floating-point special cases
1.0 / 0.0;           // +∞ (not UB for floating-point!)
-1.0 / 0.0;          // -∞
0.0 / 0.0;           // NaN
std::sqrt(-1.0);     // NaN

// Increment/decrement
int i = 5;
int post = i++;      // post=5 (old value), i=6 (post-increment)
int pre  = ++i;      // i=7, pre=7 (pre-increment; use in loops: avoids temp copy for iterators)

// Compound assignment (all equivalent to: lhs = lhs OP rhs)
a += b;  a -= b;  a *= b;  a /= b;  a %= b;
a &= b;  a |= b;  a ^= b;  a <<= 1; a >>= 1;

// Comma operator (evaluate both, return right — mainly in for loops)
int j = (a=1, b=2, a+b);  // j = 3
for (int x=0, y=10; x<5; ++x, --y) { }  // multiple updates in for

// sizeof and alignof
sizeof(int)           // 4
sizeof(double)        // 8
sizeof("hello")       // 6 (includes null terminator)
sizeof arr / sizeof arr[0]  // number of elements in C array
alignof(double)       // 8 (alignment requirement in bytes)
alignof(char)         // 1

// Conditional (ternary)
int abs_a = (a >= 0) ? a : -a;
// Use for simple value selection; avoid nested ternary

// Three-way comparison <=> (C++20) "spaceship operator"
auto cmp = 5 <=> 10;             // std::strong_ordering::less
auto cmp2 = 3.14 <=> 3.14;      // std::partial_ordering::equivalent
// Returns: strong_ordering (integers), partial_ordering (floats — NaN breaks trichotomy)
// Ordered: less, equivalent, greater
// Three-way enables: if (a <=> b == std::strong_ordering::less) { ... }
// But more useful for: auto-generating all comparison operators for a class
```

### 4.2 Bitwise Operations — Full Coverage

```cpp
unsigned int x = 0b10110100;  // 180 = 0xB4
unsigned int y = 0b01101011;  // 107 = 0x6B

// Bitwise operations
x & y    // AND:  0b00100000 = 32  (bit set iff both set)
x | y    // OR:   0b11111111 = 255 (bit set if either set)
x ^ y    // XOR:  0b11011111 = 223 (bit set iff exactly one set)
~x       // NOT:  0b01001011 (flips all bits; for unsigned n-bit: result = 2^n - 1 - x)

x << 2   // left shift:  multiply by 4 = 720 (fills right with zeros)
x >> 2   // right shift: divide by 4 = 45  (for unsigned: fills left with zeros)
         // for SIGNED: >> is arithmetic right shift (sign-extends) — implementation defined pre-C++20

// Common bit manipulation patterns:
int flags = 0;
// Set bit k:
flags |= (1 << k);
// Clear bit k:
flags &= ~(1 << k);
// Toggle bit k:
flags ^= (1 << k);
// Test bit k:
bool isSet = (flags >> k) & 1;
// Clear lowest set bit:
flags &= (flags - 1);
// Isolate lowest set bit:
int lowest = flags & (-flags);   // two's complement trick
// Count set bits (popcount):
#include <bit>  // C++20
int count = std::popcount((unsigned)flags);   // hardware instruction on modern CPUs
// Check power of 2:
bool isPow2 = (x != 0) && (x & (x-1)) == 0;
// Next power of 2:
unsigned nextPow2 = std::bit_ceil(x);         // C++20
// Log2 (floor):
unsigned log2 = std::bit_width(x) - 1;        // C++20
```

### 4.3 Comparison and Logical Operators

```cpp
// Comparison — all return bool
a == b    // equal
a != b    // not equal
a <  b    // less than
a >  b    // greater than
a <= b    // less than or equal
a >= b    // greater than or equal

// TRAP: comparing signed and unsigned
int s = -1;
unsigned int u = 1;
if (s < u) { ... }  // WARNING: -1 converted to unsigned = 4294967295, so -1 < 1 is FALSE!
// Always be careful mixing signed/unsigned comparisons

// Floating-point comparison — equality is unreliable
double x = 0.1 + 0.2;
double y = 0.3;
x == y;    // false! (x = 0.30000000000000004)
// Use epsilon comparison:
#include <cmath>
bool approxEqual = std::abs(x - y) < 1e-9;           // absolute epsilon
bool relEqual    = std::abs(x - y) <= std::numeric_limits<double>::epsilon() * std::abs(x);

// Logical operators (short-circuit)
bool t = true, f = false;
t && f    // false: right side NOT evaluated if left is false
t || f    // true: right side NOT evaluated if left is true
!t        // false

// Short-circuit safety pattern:
if (ptr != nullptr && ptr->value > 0) { }  // ptr->value only evaluated if ptr is not null

// Bitwise logical (no short-circuit; evaluates both sides)
t & f     // false (both evaluated)
t | f     // true  (both evaluated)
t ^ f     // true  (XOR)
```

---

## Chapter 5: Control Flow

### 5.1 if / else — All Forms

```cpp
// Basic
if (condition) {
    // ...
} else if (other_condition) {
    // ...
} else {
    // ...
}

// if with initializer statement (C++17) — variable scoped to if block
if (auto it = map.find(key); it != map.end()) {
    use(it->second);
}   // 'it' not accessible here — reduces scope pollution

// Practical: error checking
if (FILE* f = fopen("data.txt", "r"); f != nullptr) {
    processFile(f);
    fclose(f);
} else {
    std::cerr << "cannot open file\n";
}

// Braces on same line REQUIRED (gofmt-like: style enforced by tools):
// if (x > 0)
// {          // ← compiles, but all style guides say don't do this
//     work();
// }

// Avoid the "dangling else" by always using braces:
if (x > 0)
    if (y > 0)
        doSomething();
    else              // ← this else belongs to the INNER if (y>0), not outer if (x>0)!
        surprise();   // This is a bug if you thought else matched the outer if
// With braces it's unambiguous
```

### 5.2 switch — Deep Dive

```cpp
// switch only works on: integral types (int, char, long, etc.) and enums
// NOT strings, NOT floats

int status = getStatus();
switch (status) {
    case 0:
        handleOK();
        break;                // REQUIRED to prevent fall-through
    case 1:
    case 2:                   // multiple cases sharing same body (intentional fall-through)
        handleWarning();
        break;
    case 3: {                 // braces for local variables in case
        std::string msg = "critical";
        log(msg);
        break;
    }
    [[fallthrough]];          // C++17: annotate intentional fall-through (suppresses warning)
    case 4:
        handleCritical();
        break;
    default:
        handleUnknown();
        break;                // good practice: break in default too
}

// switch with initializer (C++17)
switch (auto val = compute(); val) {
    case 1: handle1(); break;
    case 2: handle2(); break;
    default: handleDefault();
}

// Enum class in switch
enum class Color { Red, Green, Blue };
Color c = Color::Green;
switch (c) {
    case Color::Red:   std::cout << "Red\n";   break;
    case Color::Green: std::cout << "Green\n"; break;
    case Color::Blue:  std::cout << "Blue\n";  break;
    // With enum class: compiler warns if a case is missing (unlike raw int switch)
}
```

### 5.3 Loops — Every Variant

```cpp
// for loop — classic
for (int i = 0; i < 10; ++i) {
    if (i == 3) continue;   // skip to next iteration
    if (i == 7) break;       // exit loop
    std::cout << i << " ";
}

// Multiple initializers and updates
for (int i = 0, j = 10; i < j; ++i, --j) {
    std::cout << "(" << i << "," << j << ") ";
}

// Loop with iterator
std::vector<int> v = {1,2,3,4,5};
for (auto it = v.begin(); it != v.end(); ++it) {
    *it *= 2;   // modify through iterator
}

// while — check before first iteration
int n;
while (std::cin >> n && n != 0) {
    process(n);
}

// do-while — body executes at least once
std::string input;
do {
    std::cout << "Enter 'quit' to exit: ";
    std::cin >> input;
    process(input);
} while (input != "quit");

// Range-based for (C++11) — the cleanest way for containers
std::vector<std::string> names = {"Alice", "Bob", "Carol"};

for (const std::string& name : names) { std::cout << name << "\n"; }  // const reference (read-only)
for (std::string& name : names)        { name += "!"; }                // reference (modifiable)
for (std::string name : names)         { /* copies each element */ }   // copy (expensive for strings)
for (auto& name : names)               { /* auto deduces std::string& */ }

// Range-for with initializer (C++20)
for (int i = 0; auto& name : names) {  // i = index, C++20
    std::cout << i++ << ": " << name << "\n";
}

// Structured binding in range-for
std::map<std::string, int> scores{{"Alice",95},{"Bob",82}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}

// Infinite loop patterns
while (true) { if (done) break; }
for (;;) { if (done) break; }   // slightly preferred by C programmers

// goto — for breaking out of nested loops (last resort)
for (int i = 0; i < 10; ++i) {
    for (int j = 0; j < 10; ++j) {
        if (found(i, j)) goto done;
    }
}
done:
// Better: use a lambda for early return, or flag variable
```

---

## Chapter 6: Functions — Full Coverage

### 6.1 Function Declaration and Definition

```cpp
// Declaration (prototype) — in header; tells compiler the signature
double hypotenuse(double a, double b);
int    factorial(int n);
void   printMatrix(const int* matrix, int rows, int cols);

// Definition — in source file
#include <cmath>
double hypotenuse(double a, double b) {
    return std::sqrt(a*a + b*b);
}

// Default arguments — must be in declaration (header), rightmost first
void print(const std::string& msg,
           bool newline = true,
           char separator = ' ') {
    std::cout << msg;
    if (newline) std::cout << '\n';
}
print("hello");             // uses both defaults
print("hello", false);      // newline=false, sep=' '
print("hello", true, ',');  // no defaults used

// Function overloading — same name, different parameters
int    abs_val(int    x) { return x < 0 ? -x : x; }
double abs_val(double x) { return x < 0 ? -x : x; }
long   abs_val(long   x) { return x < 0 ? -x : x; }

// Return type does NOT disambiguate overloads:
// int    getValue() { return 1; }   // ❌ ambiguous with:
// double getValue() { return 1.0; } // ❌ both exist: which to call?

// Attributes
[[nodiscard]]  int  computeResult();    // warn if caller ignores return value
[[deprecated("use newAPI instead")]] void oldFunction();
[[noreturn]]   void fatalError(const std::string& msg);  // never returns (throws or exits)
[[likely]]     // hint: this branch is likely (C++20)
[[unlikely]]   // hint: this branch is unlikely (C++20)
```

### 6.2 Parameter Passing — Complete Guide

```cpp
// Value — copy; caller's variable unchanged
void byValue(int x) { x *= 2; }      // modifies local copy only
int n = 5;
byValue(n);
std::cout << n;  // 5 — unchanged

// When to pass by value:
// - Fundamental types (int, double, char, pointer): copy is cheap
// - When you need to modify a copy anyway (pass by value, then modify, don't create temp)
// - Small POD structs (< 2 pointers in size, ~16 bytes)
void processCopy(Widget w) {          // if you'll copy anyway, sink by value
    w.modify();
    storage.push_back(std::move(w));  // move into storage (no extra copy)
}

// Const reference — efficient read-only; no copy
void byConstRef(const std::string& s) {
    std::cout << s;
    // s = "other";  // ❌ COMPILE ERROR
}
std::string big = "large string with lots of data";
byConstRef(big);   // passes pointer + size (8+8 bytes) not the whole string

// When to pass by const reference:
// - Large types: std::string, std::vector, user-defined types (> 16 bytes)
// - When the function only reads the parameter

// Reference — modifiable reference; caller's variable IS affected
void doubleInPlace(int& x) { x *= 2; }
int m = 5;
doubleInPlace(m);
std::cout << m;  // 10

// Multiple "output" parameters via reference
void divide(double a, double b, double& quotient, double& remainder) {
    quotient  = std::floor(a / b);
    remainder = std::fmod(a, b);
}
double q, r;
divide(17.0, 5.0, q, r);  // q=3, r=2

// Modern alternative: return struct or tuple
struct DivResult { double quotient, remainder; };
DivResult divide2(double a, double b) {
    return {std::floor(a/b), std::fmod(a,b)};
}
auto [q2, r2] = divide2(17.0, 5.0);  // C++17 structured binding

// Pointer — nullable; caller passes address or nullptr
void processOptional(const Config* config) {
    if (config == nullptr) {
        useDefaults();
        return;
    }
    apply(*config);
}
processOptional(nullptr);    // no config
processOptional(&myConfig);  // with config

// Rvalue reference — move semantics (take ownership from temporaries)
void consume(std::vector<int>&& v) {
    storage_ = std::move(v);  // steal v's buffer
}
consume(std::vector<int>{1,2,3});      // ✅ temporary (rvalue)
std::vector<int> v = {1,2,3};
consume(std::move(v));                 // ✅ explicitly moved (v is now empty)
// consume(v);                          // ❌ can't pass lvalue to rvalue reference

// Forwarding reference (T&&) — in templates only; accepts any value category
template <typename T>
void forwardToStorage(T&& arg) {
    store(std::forward<T>(arg));  // preserves lvalue-ness or rvalue-ness
}
```

### 6.3 Advanced Function Features

```cpp
// Variadic functions (old-school C-style — avoid; use variadic templates instead)
#include <cstdarg>
int sum_c(int count, ...) {
    va_list args;
    va_start(args, count);
    int total = 0;
    for (int i = 0; i < count; ++i)
        total += va_arg(args, int);
    va_end(args);
    return total;
}
// sum_c(3, 10, 20, 30);  // 60 — but no type safety!

// Variadic templates (C++11 — type-safe, preferred)
template <typename... Args>
auto sum_modern(Args... args) {
    return (... + args);   // fold expression (C++17)
}
sum_modern(1, 2, 3);       // 6 — int
sum_modern(1.0, 2, 3.0f);  // 6.0 — double (promoted)

// Function returning multiple values
std::pair<bool, int>  parseAndValidate(const std::string& s);
std::tuple<int,int,int> rgb(uint32_t color);
struct ParseResult { bool ok; int value; std::string error; };  // most readable
ParseResult parseSafe(const std::string& s) {
    try {
        return {true, std::stoi(s), ""};
    } catch (const std::exception& e) {
        return {false, 0, e.what()};
    }
}

// Trailing return type (C++11) — for dependent return types
template <typename T, typename U>
auto multiply(T a, U b) -> decltype(a * b) {
    return a * b;
}
// C++14: can omit trailing return type (auto deduced):
template <typename T, typename U>
auto multiply2(T a, U b) { return a * b; }

// Inline function
inline int square(int x) { return x * x; }
// 'inline' for ODR (allow definition in multiple TUs); compilers inline as they see fit

// [[nodiscard]] — error if return value is ignored
[[nodiscard]] std::error_code writeFile(const std::string& path, std::string_view data);
// writeFile("out.txt", data);   // ❌ WARNING (or error with -Werror)
auto err = writeFile("out.txt", data);  // ✅

// Constexpr functions — usable at compile time
constexpr int power(int base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}
constexpr int p = power(2, 10);    // 1024 — computed at compile time
std::array<int, power(2, 4)> arr;  // array of 16 ints
```

### 6.4 std::function and Callable Objects

```cpp
#include <functional>

// std::function — type-erased callable (any function, lambda, functor matching signature)
std::function<int(int, int)> op;

op = [](int a, int b) { return a + b; };      // assign lambda
op = std::plus<int>{};                          // assign functor
op = add;                                       // assign free function

std::cout << op(3, 4) << "\n";  // 7

// Cost: std::function has overhead (heap allocation for large callables, virtual dispatch)
// For performance-critical code: use templates + auto instead

// Function pointer — no overhead; only for free functions and non-capturing lambdas
int (*fp)(int, int) = nullptr;
fp = [](int a, int b) { return a + b; };   // ✅ non-capturing lambda → function pointer
// int x = 5;
// fp = [x](int a, int b) { return a + b + x; };  // ❌ capturing lambda cannot be function pointer

// Functors — objects with operator()
struct Multiplier {
    int factor;
    Multiplier(int f) : factor{f} {}
    int operator()(int x) const { return x * factor; }
};
Multiplier triple{3};
std::cout << triple(5) << "\n";  // 15
std::transform(v.begin(), v.end(), v.begin(), triple);  // triple each element

// std::bind — partially apply function arguments (mostly superseded by lambdas)
auto add5 = std::bind(add, std::placeholders::_1, 5);
add5(3);  // 8 (equivalent to: [](int x){ return add(x, 5); })

// Callback patterns
void doWork(std::function<void(int)> callback) {
    for (int i = 0; i < 5; ++i) {
        callback(i);
    }
}
doWork([](int i) { std::cout << i << " "; });   // 0 1 2 3 4
```

---

## Chapter 7: The Memory Model

### 7.1 The Memory Layout of a C++ Program

```
Virtual Address Space (process):
┌─────────────────────────────────────────────────────────────┐
│  Kernel space (OS; not accessible from user code)            │
├─────────────────────────────────────────────────────────────┤
│  Stack           grows downward ↓                            │
│  • Function call frames                                      │
│  • Local variables                                           │
│  • Function parameters                                       │
│  • Return addresses, saved registers                         │
│  Size: 1-8MB (typical default; configurable with ulimit)     │
│  Speed: very fast (just move stack pointer)                  │
│  Management: automatic (LIFO; destroyed when scope exits)    │
├─────────────────────────────────────────────────────────────┤
│  ↓ (gap; stack overflow exception if they meet)              │
│  ↑                                                           │
│  Heap            grows upward ↑                              │
│  • Objects created with new                                   │
│  • malloc/calloc/realloc                                     │
│  Size: typically GBs (limited by RAM + swap)                 │
│  Speed: slower (memory allocator involved; fragmentation)     │
│  Management: manual (or RAII/GC)                             │
├─────────────────────────────────────────────────────────────┤
│  BSS Segment   (uninitialized globals — zero-initialized)    │
│  Data Segment  (initialized globals and statics)             │
│  Text Segment  (executable code — read-only)                 │
└─────────────────────────────────────────────────────────────┘
```

```cpp
// Stack allocation examples
void stackDemo() {
    int x = 5;            // 4 bytes on stack
    double arr[100];      // 800 bytes on stack
    char buf[1024];       // 1024 bytes on stack — RISKY if function is recursive
    // All destroyed when stackDemo() returns
}   // automatic cleanup here

// Heap allocation
void heapDemo() {
    int* p = new int{42};         // allocates on heap; p is on stack
    int* arr = new int[100];      // 100 ints on heap
    // p points to heap; MUST be manually freed (or use smart pointers)
    delete p;                      // free single object
    delete[] arr;                  // free array (must use delete[] for new[])
    // If delete is not called: memory leak (heap memory held until process exits)
}

// Global/static storage
int global_var = 10;              // Data segment; persists for program lifetime
static int file_var = 20;         // Same; only visible in this file

void func() {
    static int call_count = 0;    // Static local: initialized once; persists between calls
    ++call_count;
    std::cout << "Called " << call_count << " times\n";
}
```

### 7.2 Pointers — Complete Reference

```cpp
// Basic pointer operations
int value = 42;
int* ptr = &value;    // & = address-of operator; ptr holds the address of value
*ptr = 100;           // * = dereference operator; access/modify what ptr points to
std::cout << value;   // 100 (modified through ptr)
std::cout << ptr;     // e.g., 0x7ffd5e3a4b8c (the address)
std::cout << *ptr;    // 100 (the value at that address)
std::cout << &ptr;    // address of the ptr variable itself

// nullptr — the null pointer (C++11; replaces NULL and 0)
int* null_ptr = nullptr;
if (null_ptr != nullptr) { }  // always check before dereferencing
// *null_ptr;   // ❌ UNDEFINED BEHAVIOR — dereference of null pointer → crash

// Pointer arithmetic — only valid within arrays
int arr[] = {10, 20, 30, 40, 50};
int* p = arr;            // points to arr[0]
std::cout << *p;         // 10
std::cout << *(p + 1);   // 20 (advances by sizeof(int) bytes)
std::cout << *(p + 2);   // 30
p += 2;                  // p now points to arr[2]
std::cout << p[0];       // 30  (same as *(p+0))
std::cout << p[1];       // 40  (same as *(p+1))
std::cout << p - arr;    // 2   (ptrdiff_t: distance between pointers)

// Pointers and arrays
int* begin = arr;
int* end   = arr + 5;    // one-past-last (valid sentinel; do NOT dereference)
for (int* it = begin; it != end; ++it) {
    std::cout << *it << " ";
}

// void* — generic pointer (no type info; must cast before use; no arithmetic)
void* vp = &value;
int*  ip = static_cast<int*>(vp);   // must explicitly cast
std::cout << *ip;   // 100

// const and pointers (read declaration right-to-left)
int x = 5, y = 10;
const int* cp = &x;     // pointer to const int: can change ptr, not *ptr
*cp = 6;    // ❌ COMPILE ERROR
cp = &y;    // ✅ OK — change where ptr points

int* const pc = &x;     // const pointer to int: can change *ptr, not ptr
*pc = 6;    // ✅ OK
pc = &y;    // ❌ COMPILE ERROR

const int* const cpc = &x;  // const pointer to const int: neither changeable

// Pointer to pointer
int  val = 42;
int* p2  = &val;
int** pp = &p2;      // pointer to pointer
std::cout << **pp;   // 42 (double dereference)
*pp = &y;            // changes where p2 points
std::cout << *p2;    // 10 (now p2 points to y)

// Function pointers
int add(int a, int b) { return a + b; }
int (*func_ptr)(int, int) = add;    // pointer to function taking 2 ints, returning int
std::cout << func_ptr(3, 4);        // 7

// Member function pointers (rarely needed; prefer std::function)
class Widget {
public:
    void display() { std::cout << "Widget\n"; }
    int compute(int x) { return x * 2; }
};
void (Widget::*mfp)() = &Widget::display;   // pointer to member function
Widget w;
(w.*mfp)();    // call: "Widget"
// Or with pointer to object:
Widget* wp = &w;
(wp->*mfp)(); // "Widget"
```

### 7.3 References — Aliases

```cpp
// Reference: alternative name for an existing variable
int x = 10;
int& ref = x;       // ref IS x — same memory location
ref = 20;           // modifies x
std::cout << x;     // 20

// References MUST be initialized
// int& bad;        // ❌ COMPILE ERROR: reference must be bound at declaration

// References CANNOT be reseated (change what they refer to)
int y = 30;
ref = y;            // ← does NOT make ref refer to y
                    // ← COPIES y's value into x (ref still refers to x)
std::cout << x;     // 30 (x changed)
std::cout << (&ref == &x);  // true — they're the same object

// const reference — bind to rvalues and extend their lifetime
const int& cr1 = x;      // binds to lvalue
const int& cr2 = 42;     // binds to rvalue; temporary's lifetime extended to match cr2's
const int& cr3 = x + 1;  // binds to temporary rvalue

// Rvalue reference (C++11) — binds ONLY to rvalues
int&& rr = 42;            // binds to literal rvalue
int&& rr2 = x + 1;        // binds to rvalue expression
// int&& rr3 = x;          // ❌ x is an lvalue

// Reference vs pointer summary:
// Reference: must initialize; can't be null; can't reseat; auto-dereferences; no arithmetic
// Pointer:   can be uninitialized; can be null; can reseat; explicit *; supports arithmetic

// When to use:
// → Reference:   "I need an alias for this existing object; it must not be null"
// → Pointer:     "This might be null"; "I need to change what I'm pointing at"; "C APIs"
// → const&:      "read-only parameter of any size (most common for function params)"
// → unique_ptr:  "I own this heap object"
// → shared_ptr:  "Multiple owners of this heap object"
```

### 7.4 Memory Alignment and Struct Layout

```cpp
// Every type has an alignment requirement: must be stored at address divisible by alignof(T)
// Compiler inserts "padding bytes" to satisfy alignment

struct Padded {
    char  a;    // offset 0: 1 byte + 7 bytes padding
    double b;   // offset 8: 8 bytes (needs 8-byte alignment)
    char  c;    // offset 16: 1 byte + 7 bytes padding
    // Total: 24 bytes (!)
};
static_assert(sizeof(Padded) == 24);

struct Optimized {
    double b;   // offset 0: 8 bytes (largest member first)
    char   a;   // offset 8: 1 byte
    char   c;   // offset 9: 1 byte + 6 bytes padding (align to 8)
    // Total: 16 bytes
};
static_assert(sizeof(Optimized) == 16);  // 33% smaller!

// Rule of thumb: sort fields from largest alignment to smallest
// Use tools: pahole, -Wpadded compiler flag

// alignas — override alignment
struct alignas(16) SimdVector { float x, y, z, w; };  // aligned to 16 bytes for SSE/AVX
alignas(64) char cache_line[64];                        // aligned to cache line

// alignof — query alignment
static_assert(alignof(double) == 8);
static_assert(alignof(char)   == 1);

// offsetof — byte offset of member
#include <cstddef>
std::cout << offsetof(Padded, b) << "\n";  // 8 (because of 7 bytes padding after 'a')

// #pragma pack — override packing (use sparingly; may cause unaligned access)
#pragma pack(1)
struct Packed {
    char   a;   // offset 0: 1 byte
    double b;   // offset 1: 8 bytes (UNALIGNED — may be slow or crash on some CPUs)
    char   c;   // offset 9: 1 byte
};              // total: 10 bytes (no padding)
#pragma pack()  // restore default
// Use case: network protocols, file formats where exact layout matters
```

---

## Chapter 8: The Preprocessor

### 8.1 What the Preprocessor Does

The preprocessor runs BEFORE the compiler. It performs textual substitution — it knows nothing about C++ syntax or types.

```cpp
// The preprocessor handles:
// #include — textual file insertion
// #define  — macro definition
// #ifdef / #ifndef / #if / #else / #elif / #endif — conditional compilation
// #pragma  — implementation-defined directives
// #error   — force compile error
// #warning — force compile warning (non-standard but widely supported)
// #line    — change reported line number (for generated code)
// __FILE__, __LINE__, __func__, __DATE__, __TIME__ — predefined macros

// After preprocessing, the compiler sees a single huge file (the translation unit)
// with all #includes expanded and all macros substituted
```

### 8.2 #include Guards and #pragma once

```cpp
// Problem: if header A.hpp includes B.hpp, and main.cpp includes both A.hpp and B.hpp,
//          then B.hpp would be included twice → duplicate declarations → compile error

// Solution 1: Header guards (traditional; 100% portable)
#ifndef MY_LIBRARY_UTILS_HPP   // if this macro is not defined yet...
#define MY_LIBRARY_UTILS_HPP   // define it

// ... header content here ...

#endif  // MY_LIBRARY_UTILS_HPP

// Solution 2: #pragma once (non-standard but supported by all major compilers)
#pragma once
// ... header content here ...

// pragma once is simpler and avoids macro name collisions
// Prefer #pragma once for new code; use guards for maximum portability

// #include variants
#include <vector>           // system header: searched in compiler include paths
#include "myheader.hpp"     // user header: searched relative to current file first
#include MACRO_NAME         // macro expansion: the macro must expand to a header name
```

### 8.3 #define — Macros

```cpp
// Object-like macro: simple text substitution
#define PI 3.14159265358979
#define MAX_BUFFER 4096
#define COMPANY_NAME "ACME Corp"

// After preprocessing:
// double r = PI * PI;   →   double r = 3.14159265358979 * 3.14159265358979;

// ❌ PROBLEMS with object-like macros:
// No type safety, no scope, name collides globally, debugger sees substituted code
// Prefer: constexpr int MAX_BUFFER = 4096;

// Function-like macro: parameterized text substitution
#define SQUARE(x)   ((x) * (x))   // parentheses are CRITICAL
#define MAX(a, b)   ((a) > (b) ? (a) : (b))

// Pitfalls:
SQUARE(3 + 4)    // WITHOUT parens: 3 + 4 * 3 + 4 = 19 (WRONG), WITH: (3+4)*(3+4) = 49
MAX(x++, y)      // ❌ x++ evaluated TWICE if x > y: x incremented twice!
// Always put parens around each parameter and the whole expression

// ❌ NEVER use macros for constants or simple functions in C++
// ✅ Use: constexpr variables and constexpr/inline functions

// Variadic macros (C99/C++11)
#define LOG(fmt, ...) fprintf(stderr, fmt "\n", ##__VA_ARGS__)
LOG("Error: %s at line %d", message, lineNum);

// Stringification (#) and token-pasting (##)
#define STRINGIFY(x)     #x
#define TO_STRING(x)     STRINGIFY(x)
#define CONCAT(a, b)     a##b

STRINGIFY(hello)    // "hello" (the string "hello")
TO_STRING(__LINE__) // converts line number to string (useful for static_assert messages)
CONCAT(my, Var)     // myVar (token concatenation)

// #undef — undefine a macro
#define TEMP_VAL 42
// ... use TEMP_VAL ...
#undef TEMP_VAL

// Predefined macros (guaranteed by the standard)
__FILE__            // "main.cpp" — current source filename
__LINE__            // 42 — current line number
__DATE__            // "Jan 15 2024" — compilation date
__TIME__            // "14:30:00" — compilation time
__func__            // "main" — current function name (C++11)
__cplusplus         // 201703L (C++17), 202002L (C++20), etc.

// Useful for assertions and debugging:
#define ASSERT(condition, message) \
    do { \
        if (!(condition)) { \
            std::cerr << "Assertion failed: " << #condition \
                      << " at " << __FILE__ << ":" << __LINE__ \
                      << " in " << __func__ << ": " << message << "\n"; \
            std::abort(); \
        } \
    } while(false)  // do-while trick: makes macro behave like a statement
```

### 8.4 Conditional Compilation

```cpp
// Include/exclude code based on compile-time conditions

// Platform detection
#ifdef _WIN32           // Windows (32 or 64 bit)
    #include <windows.h>
    using Handle = HANDLE;
#elif defined(__APPLE__)  // macOS/iOS
    #include <unistd.h>
    using Handle = int;
#elif defined(__linux__)  // Linux
    #include <unistd.h>
    using Handle = int;
#else
    #error "Unsupported platform"
#endif

// Compiler detection
#if defined(__clang__)
    #pragma clang diagnostic push
    #pragma clang diagnostic ignored "-Wpadded"
#elif defined(__GNUC__)
    #pragma GCC diagnostic push
    #pragma GCC diagnostic ignored "-Wpadded"
#elif defined(_MSC_VER)
    // MSVC-specific
#endif

// Debug vs Release
#ifdef NDEBUG
    // Release: NDEBUG defined → assert() is a no-op
    #define DEBUG_LOG(x)   ((void)0)  // no-op
#else
    // Debug: NDEBUG not defined → assert() is active
    #define DEBUG_LOG(x)   (std::cout << "[DEBUG] " << x << "\n")
#endif

// Feature flags
#if __cplusplus >= 202002L  // C++20 or later
    #include <format>
    #define USE_STD_FORMAT 1
#else
    #include <sstream>   // fallback
#endif

// Versioning
#define MYLIB_VERSION_MAJOR 2
#define MYLIB_VERSION_MINOR 1
#define MYLIB_VERSION_PATCH 3
#define MYLIB_VERSION ((MYLIB_VERSION_MAJOR * 10000) + \
                       (MYLIB_VERSION_MINOR * 100)   + \
                        MYLIB_VERSION_PATCH)
// Check: #if MYLIB_VERSION >= 20100  // version >= 2.1.0

// #pragma — implementation-defined (most compilers support these)
#pragma once                            // include guard
#pragma pack(1)                         // set struct packing
#pragma warning(disable: 4996)         // disable specific MSVC warning
#pragma GCC optimize("O3")             // GCC: optimize this function at O3
#pragma clang diagnostic ignored "..."  // Clang: suppress warning
```

---

# PART II — OBJECT-ORIENTED C++

---

## Chapter 9: Classes & Objects — Deep Dive

### 9.1 Complete Class Anatomy

```cpp
#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>

class BankAccount {
    // ── Access specifiers ──────────────────────────────────────
public:
    // Accessible from anywhere

    // ── Type definitions within class ─────────────────────────
    using Balance = double;         // type alias inside class
    enum class Status { Active, Frozen, Closed };

    // ── Static constants ──────────────────────────────────────
    static constexpr double MINIMUM_BALANCE = 0.0;
    static constexpr double MAX_WITHDRAWAL  = 10'000.0;

    // ── Constructors ──────────────────────────────────────────
    // Default constructor
    BankAccount()
        : owner_{"unknown"}, balance_{0.0}, status_{Status::Active}, id_{nextId_++}
    {}

    // Parameterized constructor
    explicit BankAccount(std::string owner, Balance initial = 0.0)
        : owner_{std::move(owner)}
        , balance_{initial}
        , status_{Status::Active}
        , id_{nextId_++}
    {
        if (initial < MINIMUM_BALANCE) {
            throw std::invalid_argument("Initial balance cannot be negative");
        }
    }

    // Copy constructor (deep copy by default for this simple class)
    BankAccount(const BankAccount& other)
        : owner_{other.owner_}
        , balance_{other.balance_}
        , status_{other.status_}
        , id_{nextId_++}   // NEW unique id for the copy
        , history_{other.history_}
    {}

    // Move constructor
    BankAccount(BankAccount&& other) noexcept
        : owner_{std::move(other.owner_)}
        , balance_{other.balance_}
        , status_{other.status_}
        , id_{other.id_}    // take the original's id
        , history_{std::move(other.history_)}
    {
        other.balance_ = 0.0;
        other.status_  = Status::Closed;
    }

    // ── Destructor ────────────────────────────────────────────
    ~BankAccount() {
        if (balance_ > 0) {
            // Log unclosed account with remaining balance
        }
        --nextId_;   // just for illustration; real IDs wouldn't do this
    }

    // ── Mutating member functions ─────────────────────────────
    void deposit(Balance amount) {
        validateOpen();
        if (amount <= 0) throw std::invalid_argument("Deposit amount must be positive");
        balance_ += amount;
        recordTransaction("DEPOSIT", amount);
    }

    bool withdraw(Balance amount) {
        validateOpen();
        if (amount <= 0 || amount > MAX_WITHDRAWAL) return false;
        if (amount > balance_) return false;
        balance_ -= amount;
        recordTransaction("WITHDRAWAL", -amount);
        return true;
    }

    void freeze()  { status_ = Status::Frozen; }
    void unfreeze(){ status_ = Status::Active; }
    void close()   { status_ = Status::Closed; }

    // ── Assignment operators ──────────────────────────────────
    BankAccount& operator=(const BankAccount& rhs) {
        if (this == &rhs) return *this;    // self-assignment guard
        owner_   = rhs.owner_;
        balance_ = rhs.balance_;
        status_  = rhs.status_;
        history_ = rhs.history_;
        // id_ stays the same (this object keeps its identity)
        return *this;
    }

    BankAccount& operator=(BankAccount&& rhs) noexcept {
        if (this == &rhs) return *this;
        owner_   = std::move(rhs.owner_);
        balance_ = rhs.balance_;
        status_  = rhs.status_;
        history_ = std::move(rhs.history_);
        rhs.balance_ = 0.0;
        rhs.status_  = Status::Closed;
        return *this;
    }

    // ── Const member functions (observers) ────────────────────
    Balance     getBalance()  const { return balance_; }
    const std::string& getOwner() const { return owner_; }
    Status      getStatus()   const { return status_; }
    int         getId()       const { return id_; }
    bool        isActive()    const { return status_ == Status::Active; }
    const std::vector<std::string>& getHistory() const { return history_; }

    // ── Static member functions ───────────────────────────────
    static int getTotalAccounts() { return nextId_; }

    // ── Friend functions ──────────────────────────────────────
    // Friend: has access to ALL private members
    friend std::ostream& operator<<(std::ostream& os, const BankAccount& acc) {
        return os << "Account[" << acc.id_ << ":" << acc.owner_
                  << " $" << acc.balance_ << "]";
    }

    friend bool operator==(const BankAccount& lhs, const BankAccount& rhs) {
        return lhs.id_ == rhs.id_;
    }

protected:
    // Accessible from this class and derived classes
    void validateOpen() const {
        if (status_ != Status::Active)
            throw std::runtime_error("Account is not active");
    }

private:
    // ── Instance members ──────────────────────────────────────
    std::string              owner_;
    Balance                  balance_;
    Status                   status_;
    int                      id_;
    std::vector<std::string> history_;

    // ── Static members ────────────────────────────────────────
    static int nextId_;   // DECLARED here; DEFINED in .cpp file

    // ── Private helpers ───────────────────────────────────────
    void recordTransaction(const std::string& type, Balance amount) {
        history_.push_back(type + ": " + std::to_string(amount));
    }
};

// Static member DEFINITION (in .cpp file, not header):
int BankAccount::nextId_ = 1;

// Usage
BankAccount alice{"Alice", 1000.0};
alice.deposit(500.0);
bool ok = alice.withdraw(200.0);
std::cout << alice << "\n";              // Account[1:Alice $1300]
std::cout << alice.getBalance() << "\n"; // 1300
std::cout << BankAccount::getTotalAccounts() << "\n"; // 1
```

### 9.2 Member Initializer List — Why It Matters

```cpp
class Config {
    const std::string filename_;  // const: MUST use initializer list
    int&              ref_;       // reference: MUST use initializer list
    std::vector<int>  data_;
    std::string       description_;

public:
    // ✅ CORRECT: initializer list initializes members before body runs
    Config(const std::string& file, int& n, std::string desc)
        : filename_{file}          // copies file into filename_
        , ref_{n}                  // binds ref_ to n
        , data_(10, 0)             // 10 zeros (note: data_ is not const, using ())
        , description_{std::move(desc)}  // move desc into description_
    {
        // Body runs AFTER all members are initialized
        if (filename_.empty()) throw std::invalid_argument("filename empty");
        // Can validate here, but all members are already constructed
    }

    // ❌ WRONG: assigning in body
    Config(const std::string& file, int& n)
        : ref_{n}                  // references must still be in list
        // filename_ default-constructed here (empty string)
        // data_ default-constructed here (empty vector)
    {
        filename_ = file;    // this ASSIGNS (constructs then assigns — 2 operations)
        data_.resize(10);    // this ASSIGNS (constructs then resizes — 2 operations)
        // const_filename_ = file;  // ❌ COMPILE ERROR: can't assign to const
    }

    // CRITICAL: initialization order = ORDER OF DECLARATION (not order in list!)
    class DangerousOrder {
        int a_;    // initialized FIRST (order in class body)
        int b_;    // initialized SECOND
        int c_;    // initialized THIRD
    public:
        // The initializer list order (b_, a_, c_) does NOT match declaration order
        // c_ is initialized using a_ + b_, but when c_ initializes, a_ IS initialized
        // (a_ comes before c_ in declaration), so this is safe.
        // BUT: b_ initializes before a_ in the list, yet AFTER a_ in declaration order.
        // This means: list order is irrelevant; declaration order is what matters.
        DangerousOrder() : c_{a_ + b_}, b_{2}, a_{1} {}
        // a_ initialized first → 1
        // b_ initialized second → 2
        // c_ initialized third → a_ + b_ = 3  ✅ correct
    };
    // RULE: always write initializer list in same order as member declarations
};
```

---

## Chapter 18: Strings — Deep Dive

### 18.1 std::string — Owning, Mutable String

```cpp
#include <string>
#include <sstream>
#include <charconv>   // C++17 — fast number parsing/formatting

// ── Construction ──────────────────────────────────────────────
std::string s1;                    // empty string ""
std::string s2 = "Hello";         // from string literal (copy)
std::string s3{"World"};          // preferred brace-init
std::string s4(5, 'x');          // "xxxxx" — 5 copies of 'x'
std::string s5(s2);              // copy constructor
std::string s6(std::move(s5));   // move constructor (s5 is now "")
std::string s7(s2, 1, 3);       // "ell" — substr starting at 1, length 3
std::string s8(s2.begin(), s2.end()); // from iterators

// ── Size and Capacity ─────────────────────────────────────────
s2.length()             // 5 — number of chars (same as size())
s2.size()               // 5
s2.empty()              // false
s2.max_size()           // platform maximum (~2^63 or similar)
s2.capacity()           // allocated capacity (>= size)
s2.reserve(100)         // pre-allocate for 100 chars (avoids reallocation)
s2.shrink_to_fit()      // release excess capacity (may or may not work)
s2.resize(10)           // resize to 10 (fills with '\0' if growing)
s2.resize(10, 'x')      // resize to 10 (fills with 'x' if growing)
s2.clear()              // s2 = "" (size = 0, capacity unchanged)

// ── Access ────────────────────────────────────────────────────
s2[0]                   // 'H' — no bounds check (UB if out of range)
s2.at(0)                // 'H' — throws std::out_of_range if out of range
s2.front()              // 'H' — first character
s2.back()               // 'o' — last character
s2.data()               // const char* — raw pointer to buffer (null-terminated since C++11)
s2.c_str()              // const char* — C-string (same as data() for std::string)

// ── Modifying ─────────────────────────────────────────────────
s2 += " World";         // "Hello World" — append
s2.append(" World");    // same as +=
s2.append(s3, 0, 3);   // append first 3 chars of s3
s2.push_back('!');      // append single char
s2.pop_back();          // remove last char
s2.insert(5, ",");      // "Hello, World" — insert at position 5
s2.insert(s2.begin() + 5, ',');  // same, iterator version
s2.erase(5, 1);         // remove 1 char at position 5: "Hello World"
s2.erase(s2.begin() + 5);  // same, iterator version
s2.replace(0, 5, "Hi"); // "Hi World" — replace 5 chars at 0 with "Hi"

// ── Searching ─────────────────────────────────────────────────
std::string haystack = "Hello, World! Hello!";

haystack.find("Hello")           // 0  — first occurrence (or npos)
haystack.find("Hello", 1)        // 14 — search starting from position 1
haystack.rfind("Hello")          // 14 — last occurrence
haystack.find_first_of("aeiou")  // 1  — first of any vowel
haystack.find_last_of("aeiou")   // 17
haystack.find_first_not_of("Helo") // 4 — first char not in set (',')
haystack.find_last_not_of(" !") // 17

if (haystack.find("World") != std::string::npos) {
    std::cout << "found!\n";
}
// C++23: contains()
bool has = haystack.contains("World");    // C++23
bool starts = haystack.starts_with("Hello");  // C++20
bool ends   = haystack.ends_with("!");        // C++20

// ── Substrings ────────────────────────────────────────────────
haystack.substr(7, 5)   // "World" — position, length (NOT end position)
haystack.substr(7)      // "World! Hello!" — from position 7 to end

// ── Comparison ────────────────────────────────────────────────
s2.compare("Hello")    // 0 if equal, <0 if less, >0 if greater
s2 == "Hello"          // true
s2 <  "World"          // lexicographic comparison
// C++20 spaceship: auto cmp = s2 <=> std::string{"World"};

// ── Transformations ───────────────────────────────────────────
// Case conversion (locale-dependent — safer to use toupper with explicit locale or ASCII-only)
std::string lower = s2;
std::transform(lower.begin(), lower.end(), lower.begin(),
    [](unsigned char c){ return std::tolower(c); });

std::string upper = s2;
std::transform(upper.begin(), upper.end(), upper.begin(),
    [](unsigned char c){ return std::toupper(c); });

// Trim whitespace
auto ltrim = [](std::string& s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char c){ return !std::isspace(c); }));
};
auto rtrim = [](std::string& s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char c){ return !std::isspace(c); }).base(), s.end());
};
auto trim = [&](std::string& s) { ltrim(s); rtrim(s); };

// Split string by delimiter
std::vector<std::string> split(const std::string& s, char delim) {
    std::vector<std::string> tokens;
    std::stringstream ss(s);
    std::string token;
    while (std::getline(ss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}
auto parts = split("a,b,c,d", ',');  // {"a","b","c","d"}

// Join strings
std::string join(const std::vector<std::string>& v, const std::string& sep) {
    std::string result;
    for (size_t i = 0; i < v.size(); ++i) {
        if (i != 0) result += sep;
        result += v[i];
    }
    return result;
}

// ── Number Conversions ────────────────────────────────────────
// String → number
int    n1 = std::stoi("42");          // "42" → 42; throws if invalid
long   l1 = std::stol("1234567890");
double d1 = std::stod("3.14");
// std::stoi("abc") → throws std::invalid_argument
// std::stoi("42abc") → 42, and sets pos to 2

// Number → string
std::string s_n = std::to_string(42);     // "42" (may be locale-dependent for floats)
std::string s_f = std::to_string(3.14);   // "3.140000" (always 6 decimal places)

// Fast conversion with std::from_chars / std::to_chars (C++17, no locale, no allocation)
#include <charconv>
char buffer[20];
auto [ptr, ec] = std::to_chars(buffer, buffer + sizeof(buffer), 42);
// ec == std::errc{} on success

int value;
auto [ptr2, ec2] = std::from_chars("42abc", "42abc" + 7, value);
// value = 42; ptr2 points to 'a'; no exceptions, no allocation

// Fast float to string
double pi = 3.14159;
char fbuf[50];
auto [fptr, fec] = std::to_chars(fbuf, fbuf + sizeof(fbuf), pi, std::chars_format::fixed, 4);
// fbuf = "3.1416"

// ── String Building ──────────────────────────────────────────
// ❌ Slow: concatenation with +
std::string result;
for (int i = 0; i < 1000; ++i) result += std::to_string(i);  // O(n²) allocations

// ✅ Fast: std::ostringstream (buffered)
std::ostringstream oss;
for (int i = 0; i < 1000; ++i) oss << i;
std::string result2 = oss.str();

// ✅ Fast: reserve + append
std::string result3;
result3.reserve(4000);  // estimate
for (int i = 0; i < 1000; ++i) result3 += std::to_string(i);

// ✅ Fastest (C++20): std::format
#include <format>
std::string msg  = std::format("Hello, {}! Score: {:.2f}", name, score);
std::string hex  = std::format("{:#010x}", 255);   // "0x000000ff"
std::string wide = std::format("{:>20}", "right");  // right-aligned in 20 chars
std::string pad  = std::format("{:*<10}", "hi");    // "hi********"
```

### 18.2 std::string_view — Non-Owning Reference (C++17)

```cpp
#include <string_view>

// string_view: a non-owning view of a contiguous character sequence
// = pointer + length (16 bytes total)
// No allocation, no copy, O(1) for all non-mutating operations

std::string_view sv1 = "Hello";         // view of string literal
std::string str = "World";
std::string_view sv2 = str;             // view of std::string's buffer
std::string_view sv3{str.data() + 1, 3}; // view of substring "orl"

// All read operations work the same as std::string:
sv1.length()    // 5
sv1[0]          // 'H'
sv1.front()     // 'H'
sv1.substr(1)   // string_view "ello" (O(1) — just moves pointer/adjusts length)
sv1.find('e')   // 1
sv1.starts_with("He")  // true (C++20)
sv1.contains("ell")    // true (C++23)

// string_view has NO allocating operations (no push_back, no +=, etc.)

// CRITICAL RULE: string_view must NOT outlive the string it views
std::string_view dangling() {
    std::string local = "hello";
    return local;   // ❌ UB: local destroyed; string_view dangling
}

// CORRECT: string_view as function parameter (fastest for read-only strings)
// Accepts: string literal, std::string, char[], any string-like thing
size_t countVowels(std::string_view sv) {
    return std::count_if(sv.begin(), sv.end(), [](char c){
        return std::string_view{"aeiouAEIOU"}.find(c) != std::string_view::npos;
    });
}
countVowels("Hello World");   // ✅ from literal (no copy)
countVowels(str);              // ✅ from std::string (no copy)
countVowels(str.substr(1,3)); // ⚠️ temporary std::string — careful with lifetime

// When to use string_view vs string:
// string_view: function parameters for read-only access (always prefer this)
//              local variable viewing a longer-lived string
//              return type of function returning view into member (careful with lifetime)
// std::string: when you NEED ownership (storing, modifying, returning new string)
//              when null-termination required for C APIs (use string, then .c_str())
```

### 18.3 Raw String Literals and Unicode

```cpp
// Raw string literals: R"delimiter(content)delimiter"
// Content is taken literally — no escape sequences processed
std::string path     = R"(C:\Users\Alice\Documents\file.txt)";
std::string json     = R"({"name": "Alice", "age": 30})";
std::string regex    = R"(\d+\.\d{2})";     // no double-backslash needed
std::string multiline = R"(
    Line 1
    Line 2
    Line 3
)";  // includes the surrounding newlines

// Custom delimiter (when content contains ")"):
std::string tricky = R"delim(contains " and ) and even )" in middle)delim";

// Unicode string literals (C++11)
const char*     utf8  = u8"Hello, 世界! © ñ";  // UTF-8
const char16_t* utf16 = u"Hello, 世界!";         // UTF-16
const char32_t* utf32 = U"Hello, 世界!";         // UTF-32
const wchar_t*  wide  = L"Hello, 世界!";         // wide (platform-dependent)

// std::u8string (C++20) — explicit UTF-8 string type
std::u8string u8s = u8"Hello, 世界!";
// C++17: u8"..." has type const char* (confusing)
// C++20: u8"..." has type const char8_t* (explicit)

// Character classification (always pass unsigned char to avoid UB)
char c = 'A';
std::isupper((unsigned char)c)   // true
std::islower((unsigned char)c)   // false
std::isdigit((unsigned char)c)   // false
std::isalpha((unsigned char)c)   // true
std::isalnum((unsigned char)c)   // true
std::isspace((unsigned char)c)   // false
std::ispunct((unsigned char)c)   // false
std::toupper((unsigned char)'a') // 'A'
std::tolower((unsigned char)'A') // 'a'
```

---

## Chapter 19: Containers — Complete STL

### 19.1 std::vector — Dynamic Array

```cpp
#include <vector>

// Construction
std::vector<int> v1;                    // empty
std::vector<int> v2(10);               // 10 zeros
std::vector<int> v3(10, 42);           // 10 copies of 42
std::vector<int> v4{1, 2, 3, 4, 5};   // initializer list (PREFERRED)
std::vector<int> v5(v4.begin(), v4.end()); // from range
std::vector<std::string> vs{"a", "b", "c"};

// Internals: pointer to heap buffer + size + capacity
// vector<int> v: [ptr→heap][size=5][capacity=8]
// heap: [1][2][3][4][5][?][?][?]  ← ? = allocated but unused

// Capacity management
v4.reserve(100);        // allocate for 100 elements (no size change)
v4.resize(7);           // size=7, new elements zero-initialized
v4.resize(7, 99);       // size=7, new elements = 99
v4.resize(3);           // size=3, elements 3,4,5,6 destroyed
v4.shrink_to_fit();     // request capacity = size (implementation may ignore)
v4.capacity();          // ≥ v4.size()
v4.size();              // current element count
v4.empty();             // true if size == 0
v4.max_size();          // maximum possible size

// Element access
v4[0]                   // first (NO bounds check — UB if out of range)
v4.at(0)                // first (throws std::out_of_range if out of range)
v4.front()              // first element
v4.back()               // last element
v4.data()               // T* — raw pointer to contiguous array (valid for C APIs)

// Adding elements
v4.push_back(6);                    // copy/move at end, O(1) amortized
v4.emplace_back(7);                 // construct in-place at end (preferred)
v4.emplace_back(args...);           // forward args to constructor

v4.insert(v4.begin(), 0);           // insert at front, O(n) shift
v4.insert(v4.begin() + 2, 99);     // insert at position 2
v4.insert(v4.end(), {8, 9, 10});   // insert multiple at end
v4.emplace(v4.begin() + 1, 77);    // construct in-place at position

// Removing elements
v4.pop_back();                      // remove last, O(1)
v4.erase(v4.begin());              // remove first, O(n) shift
v4.erase(v4.begin()+1, v4.begin()+3); // remove range [begin+1, begin+3)
v4.clear();                         // remove all, O(n), capacity unchanged

// Efficient removal (erase-remove idiom)
// Remove all elements equal to 42:
v4.erase(std::remove(v4.begin(), v4.end(), 42), v4.end()); // pre-C++20
std::erase(v4, 42);                  // C++20: cleaner

// Remove all elements satisfying predicate:
v4.erase(std::remove_if(v4.begin(), v4.end(),
    [](int x){ return x % 2 == 0; }), v4.end());
std::erase_if(v4, [](int x){ return x % 2 == 0; });  // C++20

// O(1) removal without preserving order (swap with back, then pop):
void fastRemoveAt(std::vector<int>& v, size_t i) {
    std::swap(v[i], v.back());
    v.pop_back();
}

// Iteration
for (int x : v4) { }                           // range-for (preferred)
for (auto it = v4.begin(); it != v4.end(); ++it) { }  // iterator
for (size_t i = 0; i < v4.size(); ++i) { v4[i]; }     // index

// Reverse iteration
for (auto rit = v4.rbegin(); rit != v4.rend(); ++rit) { }
for (auto& x : v4 | std::views::reverse) { }  // C++20 ranges

// Sorting and searching
std::sort(v4.begin(), v4.end());
std::sort(v4.begin(), v4.end(), std::greater<int>{});
std::stable_sort(v4.begin(), v4.end());         // preserves order of equal elements
bool found = std::binary_search(v4.begin(), v4.end(), 42);  // requires sorted
auto it = std::lower_bound(v4.begin(), v4.end(), 42);       // first >= 42

// 2D vector
std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols, 0));
matrix[2][3] = 5;
```

### 19.2 std::array — Fixed-Size Stack Array

```cpp
#include <array>

// Fixed size at compile time; stored on stack (not heap like vector)
std::array<int, 5> arr = {1, 2, 3, 4, 5};
std::array<double, 3> coords{1.0, 2.0, 3.0};
std::array<int, 5> zeros{};   // value-initialized: {0,0,0,0,0}

// Same access API as vector:
arr[0]; arr.at(0); arr.front(); arr.back(); arr.data();

// Key differences from vector:
// - Size is part of the TYPE: array<int,5> ≠ array<int,6>
// - Cannot resize
// - Stored on stack (no heap allocation)
// - sizeof(array<int,5>) = 20 (just the data, no overhead)

// Use when: size known at compile time, small/medium sized, on stack

// Works with all std::algorithms:
std::sort(arr.begin(), arr.end());
auto max = *std::max_element(arr.begin(), arr.end());
```

### 19.3 std::deque, std::list, std::forward_list

```cpp
// std::deque — double-ended queue; O(1) at both ends, O(n) middle
#include <deque>
std::deque<int> dq{1, 2, 3, 4, 5};
dq.push_front(0);    // O(1)
dq.push_back(6);     // O(1)
dq.pop_front();      // O(1)
dq.pop_back();       // O(1)
dq[2];               // O(1) random access (but slower than vector)
// Internally: array of fixed-size blocks (not contiguous like vector)
// Use when: frequent insertion/deletion at both ends; doesn't need contiguous memory

// std::list — doubly-linked list; O(1) insert/delete anywhere (with iterator)
#include <list>
std::list<int> lst{1, 2, 3, 4, 5};
auto it = std::find(lst.begin(), lst.end(), 3);
lst.insert(it, 99);    // insert 99 before 3, O(1) (have iterator already)
lst.erase(it);         // erase element at it, O(1)
lst.push_front(0);     // O(1)
lst.splice(it, lst2);  // move elements from lst2 to before it — O(1)!
lst.sort();            // member sort (can't use std::sort — no random access)
lst.unique();          // remove consecutive duplicates (after sorting)
lst.merge(lst2);       // merge sorted list
// Disadvantages: no random access O(n); poor cache behavior; pointer overhead

// std::forward_list — singly-linked list; less memory than list
#include <forward_list>
std::forward_list<int> fl{1, 2, 3};
fl.push_front(0);
fl.insert_after(fl.begin(), 99);  // insert after an iterator position
fl.erase_after(fl.begin());
// No push_back, no size() — minimal overhead; only forward traversal
```

### 19.4 std::map, std::set and Unordered Variants

```cpp
// std::map — sorted key-value pairs; O(log n); Red-Black tree
#include <map>
std::map<std::string, int> scores;

// Insertion
scores["Alice"] = 95;                         // operator[] (creates if absent)
scores.insert({"Bob", 82});                   // insert pair
scores.insert(std::make_pair("Carol", 91));   // same
scores.emplace("Dave", 88);                   // in-place construction
auto [iter, inserted] = scores.insert({"Alice", 100}); // returns (iterator, bool)
// inserted = false: Alice already exists; score unchanged

scores.insert_or_assign("Alice", 100);        // update if exists, insert if not (C++17)
scores.try_emplace("Eve", 77);               // insert if key absent, no-op otherwise (C++17)

// Access
scores["Alice"]                  // 95 — CREATES entry with 0 if absent!
scores.at("Alice")               // 95 — throws if absent (SAFE)
scores.count("Alice")            // 1 or 0 (for map: at most 1; use contains() C++20)
scores.contains("Alice")         // true (C++20)

auto it2 = scores.find("Alice");
if (it2 != scores.end()) {
    std::cout << it2->first << ": " << it2->second << "\n";
    it2->second = 99;            // modify value through iterator
}

// Modifying via map::operator[] (common pattern)
scores["Alice"] += 5;           // increment: loads 95, +5, stores 100

// Iteration (always in sorted key order)
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}

// Deletion
scores.erase("Alice");           // by key; O(log n)
scores.erase(scores.find("Bob")); // by iterator; O(1) amortized
scores.erase(scores.begin(), scores.end()); // erase range
scores.clear();

// Range queries (key advantage of ordered containers)
auto lo = scores.lower_bound("C");    // first key >= "C"
auto hi = scores.upper_bound("D");    // first key > "D"
for (auto it3 = lo; it3 != hi; ++it3) {
    // All entries with keys in ["C", "D"]
}
scores.equal_range("C");   // pair of (lower_bound, upper_bound)

// std::multimap — allows duplicate keys
std::multimap<std::string, int> multi;
multi.emplace("Alice", 90);
multi.emplace("Alice", 85);  // allowed
multi.count("Alice");        // 2
auto range = multi.equal_range("Alice");  // get all Alice's entries

// std::set — sorted unique elements; O(log n)
#include <set>
std::set<int> s{5, 3, 1, 4, 2};      // {1,2,3,4,5} — auto-sorted
s.insert(6);
s.erase(3);
s.count(4);                            // 1 or 0
s.find(4) != s.end();                 // true if found
s.contains(4);                        // C++20

// std::unordered_map — hash map; O(1) average; no ordering
#include <unordered_map>
std::unordered_map<std::string, int> hash_scores;
// Same interface as map, but:
// - No ordering (iteration order unpredictable)
// - O(1) average for find/insert/erase (O(n) worst case with collisions)
// - Keys must be hashable

// Custom hash for user-defined types
struct Point { int x, y; };
struct PointHash {
    size_t operator()(const Point& p) const {
        // Combine hashes — classic technique
        return std::hash<int>{}(p.x) ^ (std::hash<int>{}(p.y) << 32);
    }
};
struct PointEqual {
    bool operator()(const Point& a, const Point& b) const {
        return a.x == b.x && a.y == b.y;
    }
};
std::unordered_map<Point, int, PointHash, PointEqual> pointMap;

// Performance comparison:
// std::map:          O(log n) find/insert — consistent, ordered
// std::unordered_map: O(1) average find/insert — faster for large n
// Prefer unordered for: high-frequency lookups, large datasets
// Prefer ordered for:   range queries, sorted iteration, small datasets

// std::priority_queue — max-heap by default
#include <queue>
std::priority_queue<int> maxPQ;           // max at top
maxPQ.push(5); maxPQ.push(1); maxPQ.push(3);
maxPQ.top();   // 5 (largest)
maxPQ.pop();   // removes 5

// Min-heap:
std::priority_queue<int, std::vector<int>, std::greater<int>> minPQ;
// Or: negate values when pushing/popping

// Custom comparator:
struct Task { int priority; std::string name; };
auto cmp = [](const Task& a, const Task& b) { return a.priority < b.priority; };
std::priority_queue<Task, std::vector<Task>, decltype(cmp)> taskQueue(cmp);
```

---

## Chapter 22: File I/O & Streams

### 22.1 Stream Architecture

```
std::ios_base (base class: flags, locale)
    └── std::basic_ios<char>
            ├── std::istream (input: >>, read, getline)
            │   ├── std::ifstream (file input)
            │   ├── std::istringstream (string input)
            │   └── std::cin
            ├── std::ostream (output: <<, write, put)
            │   ├── std::ofstream (file output)
            │   ├── std::ostringstream (string output)
            │   ├── std::cout
            │   ├── std::cerr (unbuffered)
            │   └── std::clog (buffered)
            └── std::iostream (both)
                ├── std::fstream (file input+output)
                └── std::stringstream (string I/O)
```

### 22.2 Console I/O

```cpp
#include <iostream>
#include <iomanip>   // for format manipulators

// Output formatting
std::cout << "Integer: " << 42 << "\n";
std::cout << "Float: " << 3.14159 << "\n";

// Format manipulators (sticky unless otherwise noted)
std::cout << std::fixed << std::setprecision(2) << 3.14159 << "\n"; // "3.14"
std::cout << std::scientific << 1234567.89 << "\n";  // "1.234568e+06"
std::cout << std::defaultfloat;   // reset to default

std::cout << std::setw(10) << "right";        // "     right" (not sticky!)
std::cout << std::left << std::setw(10) << "left" << "|\n";  // "left      |"
std::cout << std::right;   // reset to right

std::cout << std::setfill('0') << std::setw(6) << 42; // "000042"

std::cout << std::hex << 255;        // "ff"
std::cout << std::oct << 255;        // "377"
std::cout << std::dec << 255;        // "255"
std::cout << std::uppercase << std::hex << 255;  // "FF"

std::cout << std::boolalpha << true;  // "true" (instead of "1")
std::cout << std::noboolalpha;

std::cout << std::showpoint << 1.0;  // "1.00000" (show decimal point always)

// std::flush vs std::endl
std::cout << "hello" << std::flush;  // flush buffer immediately (no newline)
std::cout << "hello" << std::endl;   // "\nhello" + flush (slow — avoid in loops)
std::cout << "hello\n";              // just newline, no flush (fast — PREFER)

// Input reading
int n;
double d;
std::string word, line;

std::cin >> n;              // read one token (skips whitespace, stops at whitespace)
std::cin >> d >> word;      // chain reads
std::cin.ignore();          // discard '\n' left in buffer after >>
std::getline(std::cin, line); // read entire line including spaces

// Error checking
if (std::cin >> n) {
    // success
} else {
    std::cin.clear();           // clear error flags
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');  // clear buffer
}

// C++20: std::format (preferred over stream manipulators)
#include <format>
std::cout << std::format("{:>10.2f}\n", 3.14159);   // "      3.14"
std::cout << std::format("{:#010x}\n", 255);         // "0x000000ff"
std::cout << std::format("{:*<10}\n", "hi");         // "hi********"

// C++23: std::print (like Python's print)
#include <print>
std::print("Hello, {}! Score: {:.2f}\n", name, score);  // directly to stdout
std::println("Done");                                     // with automatic newline
```

### 22.3 File I/O

```cpp
#include <fstream>
#include <filesystem>
namespace fs = std::filesystem;

// ── Writing ───────────────────────────────────────────────────
std::ofstream out{"output.txt"};    // opens for writing (creates or truncates)
if (!out) {
    std::cerr << "Cannot open output.txt\n";
    return 1;
}
out << "Line 1\n";
out << "Value: " << 42 << "\n";
out << std::format("Float: {:.4f}\n", 3.14159);
// File closed automatically when 'out' goes out of scope (RAII)

// Append mode
std::ofstream appender{"log.txt", std::ios::app};  // don't truncate; append
appender << "New log entry\n";

// Binary mode
std::ofstream binary{"data.bin", std::ios::binary};
int values[] = {1, 2, 3, 4, 5};
binary.write(reinterpret_cast<const char*>(values), sizeof(values));

// ── Reading ───────────────────────────────────────────────────
std::ifstream in{"input.txt"};
if (!in) { throw std::runtime_error("Cannot open input.txt"); }

// Read line by line
std::string line;
while (std::getline(in, line)) {
    processLine(line);
}

// Read word by word
std::string word;
while (in >> word) {
    processWord(word);
}

// Read entire file into string (C++17)
std::ifstream f{"data.txt"};
std::string content((std::istreambuf_iterator<char>(f)),
                     std::istreambuf_iterator<char>());

// Or: read all at once efficiently
f.seekg(0, std::ios::end);
size_t size = f.tellg();
f.seekg(0, std::ios::beg);
std::string buffer(size, '\0');
f.read(buffer.data(), size);

// Read binary
std::ifstream bin{"data.bin", std::ios::binary};
int values2[5];
bin.read(reinterpret_cast<char*>(values2), sizeof(values2));

// ── std::fstream — read and write ────────────────────────────
std::fstream rw{"data.txt", std::ios::in | std::ios::out};
rw.seekg(0);               // seek to beginning (get position)
rw.seekp(10);              // seek to position 10 (put position)
std::streampos pos = rw.tellg();  // current read position
rw.seekg(0, std::ios::end);       // seek to end
rw.seekg(-10, std::ios::cur);     // seek 10 back from current

// Open flags
// ios::in       — open for reading
// ios::out      — open for writing
// ios::app      — append (all writes go to end)
// ios::binary   — binary mode (no newline translation)
// ios::trunc    — truncate file to zero on open
// ios::ate      — seek to end immediately after opening

// ── std::filesystem (C++17) ───────────────────────────────────
#include <filesystem>

fs::path p{"data/subdir/file.txt"};
p.filename()                    // "file.txt"
p.stem()                        // "file"
p.extension()                   // ".txt"
p.parent_path()                 // "data/subdir"
p.string()                      // "data/subdir/file.txt"
p.native()                      // platform path string
(p / "another.txt")             // "data/subdir/file.txt/another.txt" (concatenate)

// File queries
fs::exists(p)
fs::is_regular_file(p)
fs::is_directory(p)
fs::file_size(p)                // bytes
fs::last_write_time(p)          // modification time

// File operations
fs::copy("src.txt", "dst.txt");
fs::copy("src", "dst", fs::copy_options::recursive);  // copy directory tree
fs::rename("old.txt", "new.txt");
fs::remove("file.txt");          // delete file or empty directory
fs::remove_all("directory");     // delete directory and all contents
fs::create_directory("newdir");
fs::create_directories("a/b/c"); // create all parents

// Directory iteration
for (const fs::directory_entry& entry : fs::directory_iterator("mydir")) {
    std::cout << entry.path().filename() << "\n";
}
// Recursive:
for (const auto& entry : fs::recursive_directory_iterator("src")) {
    if (entry.path().extension() == ".cpp") {
        std::cout << entry.path() << "\n";
    }
}

// Get current directory, temp directory
fs::current_path()              // current working directory
fs::current_path("newdir")      // change current directory
fs::temp_directory_path()       // system temp directory
```

### 22.4 String Streams

```cpp
#include <sstream>

// ── ostringstream — build string ──────────────────────────────
std::ostringstream oss;
oss << "Hello, " << name << "!\n";
oss << "Score: " << std::fixed << std::setprecision(2) << score;
std::string result = oss.str();   // extract the built string
oss.str("");                       // reset/clear the stream

// Use cases: build error messages, format mixed types
std::string errorMsg = [&]{
    std::ostringstream ss;
    ss << "Error at [" << row << "," << col << "]: " << what;
    return ss.str();
}();

// ── istringstream — parse string ──────────────────────────────
std::string data = "Alice 95 3.14 true";
std::istringstream iss(data);
std::string name2;
int score2;
double value;
bool flag;
iss >> name2 >> score2 >> value;   // extracts "Alice", 95, 3.14
iss >> std::boolalpha >> flag;      // extracts true

// Parse CSV-like data
std::string csv = "10,20,30,40,50";
std::istringstream csvStream(csv);
std::vector<int> nums;
int n;
while (csvStream >> n) {
    nums.push_back(n);
    csvStream.ignore(1, ',');   // skip the comma
}

// ── stringstream — both read and write ────────────────────────
std::stringstream ss;
ss << 42 << " " << 3.14;
int a2; double b2;
ss >> a2 >> b2;   // a2=42, b2=3.14
```

---

## Chapter 24: Concurrency — Complete Reference

### 24.1 std::thread — Creating and Managing Threads

```cpp
#include <thread>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <future>
#include <latch>    // C++20
#include <barrier>  // C++20
#include <semaphore>// C++20

// Creating threads
std::thread t1([]{ std::cout << "Thread 1\n"; });   // lambda
std::thread t2(myFunction, arg1, arg2);              // function with args
std::thread t3(&MyClass::method, &obj, arg1);        // member function

// MUST join or detach before thread object is destroyed
t1.join();      // wait for t1 to finish (blocks calling thread)
t2.detach();    // let t2 run independently (careful: main must not exit first)

if (t3.joinable()) t3.join();   // safe: joinable() check

// Thread ID
std::thread::id id = t1.get_id();
std::cout << std::this_thread::get_id();   // current thread's ID

// Thread utilities
std::this_thread::sleep_for(std::chrono::milliseconds(100));
std::this_thread::sleep_until(std::chrono::system_clock::now() + 1s);
std::this_thread::yield();   // hint to OS: give time to other threads

// Hardware concurrency
unsigned int nthreads = std::thread::hardware_concurrency();  // logical CPUs

// RAII thread guard — auto-join on destruction
class JoiningThread {
    std::thread t_;
public:
    template <typename F, typename... Args>
    explicit JoiningThread(F&& f, Args&&... args)
        : t_{std::forward<F>(f), std::forward<Args>(args)...} {}
    ~JoiningThread() { if (t_.joinable()) t_.join(); }
    JoiningThread(const JoiningThread&) = delete;
    JoiningThread(JoiningThread&&) = default;
    void join() { t_.join(); }
    bool joinable() const { return t_.joinable(); }
};

// std::jthread (C++20) — auto-joins and cooperative cancellation
#include <stop_token>
std::jthread jt([](std::stop_token stop) {
    while (!stop.stop_requested()) {
        doWork();
        std::this_thread::sleep_for(10ms);
    }
});
jt.request_stop();   // signal thread to stop
// jt automatically joins when destroyed
```

### 24.2 Mutexes and Lock Types

```cpp
// std::mutex — exclusive access
std::mutex mtx;
int shared = 0;

void increment() {
    std::lock_guard<std::mutex> lock{mtx};  // RAII: acquires in ctor, releases in dtor
    ++shared;
}   // lock released here, even if exception thrown

// std::unique_lock — flexible (can unlock/relock, used with condition_variable)
void flexibleAccess() {
    std::unique_lock<std::mutex> lock{mtx};
    doProtectedWork();
    lock.unlock();         // explicitly release
    doExpensiveWork();     // without holding lock
    lock.lock();           // reacquire
    doMoreProtectedWork();
}   // released here

// std::scoped_lock (C++17) — lock multiple mutexes, deadlock-free
std::mutex m1, m2;
void transfer(Account& a, Account& b, double amount) {
    std::scoped_lock lock{m1, m2};  // acquires both atomically; uses std::lock internally
    a.balance -= amount;
    b.balance += amount;
}

// std::shared_mutex (C++17) — readers/writer lock
#include <shared_mutex>
std::shared_mutex rwmtx;

void readData() {
    std::shared_lock lock{rwmtx};   // multiple readers CAN hold this simultaneously
    return data_;
}

void writeData(int val) {
    std::unique_lock lock{rwmtx};   // exclusive: blocks all other readers and writers
    data_ = val;
}

// std::recursive_mutex — same thread can lock multiple times
std::recursive_mutex rmtx;
void recursiveFunc(int n) {
    std::lock_guard lock{rmtx};   // OK to lock again from same thread
    if (n > 0) recursiveFunc(n - 1);
}

// Try-lock (non-blocking attempt)
if (mtx.try_lock()) {
    // got the lock
    mtx.unlock();
} else {
    // couldn't get the lock; do something else
}

// Timed lock
if (mtx.try_lock_for(std::chrono::milliseconds(100))) {
    // got lock within 100ms
    mtx.unlock();
}
```

### 24.3 Condition Variables

```cpp
std::mutex cv_mtx;
std::condition_variable cv;
std::queue<int> work_queue;
bool done = false;

// Producer
void producer() {
    for (int i = 0; i < 100; ++i) {
        {
            std::lock_guard lock{cv_mtx};
            work_queue.push(i);
        }
        cv.notify_one();   // wake one waiting consumer
    }
    {
        std::lock_guard lock{cv_mtx};
        done = true;
    }
    cv.notify_all();  // wake all — they'll see done=true
}

// Consumer
void consumer() {
    while (true) {
        std::unique_lock lock{cv_mtx};
        // wait(lock, pred): while (!pred()) { atomically unlock + sleep; relock on wake }
        // Protects against spurious wakeups automatically
        cv.wait(lock, []{ return !work_queue.empty() || done; });

        if (work_queue.empty() && done) return;

        int item = work_queue.front();
        work_queue.pop();
        lock.unlock();   // release before processing (don't hold lock during slow work)
        process(item);
    }
}

// Timed wait
cv.wait_for(lock, std::chrono::seconds(5), predicate);
cv.wait_until(lock, deadline, predicate);
```

### 24.4 Atomics — Lock-Free Programming

```cpp
#include <atomic>

// Atomic operations — guaranteed to be indivisible (no partial reads/writes)
std::atomic<int> counter{0};

counter++;                               // atomic increment
counter.fetch_add(1);                    // same; returns OLD value
counter.fetch_sub(1);                    // atomic decrement
int old = counter.exchange(42);          // atomic swap; returns old value
bool swapped = counter.compare_exchange_strong(
    int expected = 41, int desired = 42);  // CAS: sets to desired iff == expected
// on failure: expected updated with actual value

counter.load();                          // atomic read
counter.store(0);                        // atomic write
counter.load(std::memory_order_relaxed); // specify memory ordering

// Memory ordering (from weakest to strongest):
// memory_order_relaxed:  no sync; just atomicity (fastest; for non-sync'd counters)
// memory_order_release:  all prior writes visible to threads doing acquire
// memory_order_acquire:  sees all writes up to paired release
// memory_order_acq_rel:  both acquire and release (for read-modify-write)
// memory_order_seq_cst:  total sequential consistency (default; slowest; safest)

// Typical pattern for a flag:
std::atomic<bool> ready{false};

// Thread 1 (producer):
prepareData();
ready.store(true, std::memory_order_release);   // all writes before this visible after acquire

// Thread 2 (consumer):
while (!ready.load(std::memory_order_acquire)) {} // spin-wait
consumeData();    // guaranteed to see data prepared in Thread 1

// std::atomic_flag — guaranteed lock-free on all platforms
std::atomic_flag lock = ATOMIC_FLAG_INIT;
void spinLock()   { while (lock.test_and_set(std::memory_order_acquire)) {} }
void spinUnlock() { lock.clear(std::memory_order_release); }

// Atomic operations on integral types:
std::atomic<uint64_t> bits{0};
bits.fetch_or(0x01);     // atomic OR
bits.fetch_and(0xFF);    // atomic AND
bits.fetch_xor(0xF0);    // atomic XOR
```

### 24.5 Futures and Promises

```cpp
#include <future>

// std::async — run function asynchronously
// launch::async: definitely new thread; launch::deferred: lazy (run when get() called)
auto fut = std::async(std::launch::async, computeHeavy, arg1, arg2);

// Do other work while computing...
doOtherWork();

// Get result (blocks if not ready, propagates exceptions)
try {
    int result = fut.get();   // get() can only be called ONCE
    use(result);
} catch (const std::exception& e) {
    // exception thrown in async function propagated here
}

// Check if ready without blocking
if (fut.wait_for(std::chrono::milliseconds(0)) == std::future_status::ready) {
    int r = fut.get();
}

// std::promise — manually set a future's value
std::promise<int> promise;
std::future<int> future = promise.get_future();

std::thread worker([p = std::move(promise)]() mutable {
    try {
        int result = heavyComputation();
        p.set_value(result);
    } catch (...) {
        p.set_exception(std::current_exception());
    }
});

int val = future.get();
worker.join();

// std::packaged_task — wrap a callable + future
std::packaged_task<int(int, int)> task{add};
std::future<int> fut2 = task.get_future();
std::thread t{std::move(task), 3, 4};
std::cout << fut2.get() << "\n";  // 7
t.join();

// std::shared_future — multiple threads can call get()
std::shared_future<Config> config_future = loadConfigAsync().share();
// All threads can:
const Config& cfg = config_future.get();   // blocks until ready; safe to call multiple times

// Parallel computation pattern
auto f1 = std::async(std::launch::async, computeA);
auto f2 = std::async(std::launch::async, computeB);
auto f3 = std::async(std::launch::async, computeC);
int a = f1.get(), b = f2.get(), c = f3.get();  // wait for all
```

### 24.6 C++20 Synchronization Primitives

```cpp
// std::latch — count-down latch; single-use barrier
#include <latch>
std::latch latch{5};   // count = 5

// Worker threads:
void worker(std::latch& l) {
    doWork();
    l.count_down();    // decrement counter
    // or: l.count_down(n) to decrement by n
}

// Main thread waits until count reaches 0:
latch.wait();          // blocks until count == 0

// Arrive and wait in one step:
latch.arrive_and_wait(); // count_down + wait atomically

// std::barrier — reusable synchronization point
#include <barrier>
std::barrier barrier{4, []{ std::cout << "All threads synced!\n"; }};
// Completion callback runs after each phase

void worker2(std::barrier<>& b) {
    for (int phase = 0; phase < 10; ++phase) {
        doPhaseWork(phase);
        b.arrive_and_wait();  // all threads must reach here before any proceeds
    }
}

// std::semaphore — counting or binary semaphore
#include <semaphore>
std::counting_semaphore<10> sem{3};   // max=10, initial count=3
sem.acquire();    // decrement (blocks if 0)
sem.release();    // increment

std::binary_semaphore binary{0};   // 0 or 1
binary.release();  // signal
binary.acquire();  // wait for signal
```

---

## Chapter 27: Design Patterns in C++

### 27.1 Creational Patterns

```cpp
// ── Singleton ─────────────────────────────────────────────────
// Meyers Singleton — thread-safe since C++11 (static local initialization is thread-safe)
class Logger {
public:
    static Logger& getInstance() {
        static Logger instance;   // created once, on first call; thread-safe
        return instance;
    }
    void log(const std::string& msg) {
        std::lock_guard lock{mtx_};
        std::cout << "[LOG] " << msg << "\n";
    }
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
private:
    Logger() {}     // private constructor
    std::mutex mtx_;
};
Logger::getInstance().log("Application started");

// ── RAII Factory ──────────────────────────────────────────────
// Factory method returning smart pointer — automatic memory management
struct Shape { virtual double area() const = 0; virtual ~Shape() = default; };
struct Circle    : Shape { double r; Circle(double r): r{r} {} double area() const override { return M_PI*r*r; } };
struct Rectangle : Shape { double w,h; Rectangle(double w,double h): w{w},h{h} {} double area() const override { return w*h; } };

std::unique_ptr<Shape> makeShape(std::string_view type, double a, double b = 0) {
    if (type == "circle")    return std::make_unique<Circle>(a);
    if (type == "rectangle") return std::make_unique<Rectangle>(a, b);
    throw std::invalid_argument("unknown shape: " + std::string{type});
}

// ── Builder Pattern ───────────────────────────────────────────
class HttpRequest {
public:
    class Builder {
        std::string url_;
        std::string method_{"GET"};
        std::unordered_map<std::string,std::string> headers_;
        std::string body_;
        std::chrono::seconds timeout_{30};

    public:
        explicit Builder(std::string url) : url_{std::move(url)} {}

        Builder& method(std::string m)         { method_ = std::move(m);  return *this; }
        Builder& header(std::string k, std::string v) { headers_[std::move(k)] = std::move(v); return *this; }
        Builder& body(std::string b)           { body_ = std::move(b);    return *this; }
        Builder& timeout(std::chrono::seconds t){ timeout_ = t;           return *this; }

        HttpRequest build() && {     // rvalue-qualified: builder is consumed
            return HttpRequest{std::move(*this)};
        }
    private:
        friend class HttpRequest;
    };

    static Builder create(std::string url) { return Builder{std::move(url)}; }

private:
    explicit HttpRequest(Builder&& b)
        : url_{std::move(b.url_)}, method_{std::move(b.method_)}
        , headers_{std::move(b.headers_)}, body_{std::move(b.body_)}
        , timeout_{b.timeout_} {}

    std::string url_, method_, body_;
    std::unordered_map<std::string,std::string> headers_;
    std::chrono::seconds timeout_;
};

auto req = HttpRequest::create("https://api.example.com/users")
    .method("POST")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer " + token)
    .body(R"({"name":"Alice"})")
    .timeout(10s)
    .build();
```

### 27.2 Structural Patterns

```cpp
// ── Decorator ─────────────────────────────────────────────────
struct Logger2 {
    virtual void log(std::string_view msg) = 0;
    virtual ~Logger2() = default;
};

struct ConsoleLogger : Logger2 {
    void log(std::string_view msg) override {
        std::cout << msg << "\n";
    }
};

struct TimestampDecorator : Logger2 {
    explicit TimestampDecorator(std::unique_ptr<Logger2> inner)
        : inner_{std::move(inner)} {}
    void log(std::string_view msg) override {
        auto now = std::chrono::system_clock::now();
        inner_->log(std::format("[{}] {}", now, msg));
    }
private:
    std::unique_ptr<Logger2> inner_;
};

struct LevelFilterDecorator : Logger2 {
    LevelFilterDecorator(std::unique_ptr<Logger2> inner, std::string minLevel)
        : inner_{std::move(inner)}, minLevel_{std::move(minLevel)} {}
    void log(std::string_view msg) override {
        if (meetsCriteria(msg)) inner_->log(msg);
    }
private:
    std::unique_ptr<Logger2> inner_;
    std::string minLevel_;
    bool meetsCriteria(std::string_view msg) { return true; /* ... */ }
};

// Compose decorators:
auto logger = std::make_unique<LevelFilterDecorator>(
    std::make_unique<TimestampDecorator>(
        std::make_unique<ConsoleLogger>()),
    "INFO"
);
logger->log("Application started");

// ── PIMPL Idiom (Pointer to Implementation) ───────────────────
// Hides implementation details, reduces compilation dependencies, enables ABI stability

// widget.hpp — public API only; no implementation details exposed
class Widget {
public:
    Widget();
    explicit Widget(const std::string& name);
    ~Widget();                              // must be in .cpp where Impl is complete
    Widget(Widget&&) noexcept;              // must be in .cpp
    Widget& operator=(Widget&&) noexcept;  // must be in .cpp
    Widget(const Widget&);                 // must be in .cpp
    Widget& operator=(const Widget&);      // must be in .cpp

    void doSomething();
    std::string getName() const;
    int compute(int x, int y) const;

private:
    class Impl;                           // forward declaration
    std::unique_ptr<Impl> pImpl_;         // pointer to implementation
};

// widget.cpp — implementation; clients don't see this
class Widget::Impl {
public:
    std::string name_;
    std::vector<int> data_;
    mutable std::mutex mtx_;
    // ... many private fields and helpers ...

    explicit Impl(const std::string& name) : name_{name} {}

    void doSomething() {
        // actual implementation
    }
    std::string getName() const { return name_; }
    int compute(int x, int y) const { return x * y + data_.size(); }
};

Widget::Widget() : pImpl_{std::make_unique<Impl>("")} {}
Widget::Widget(const std::string& name) : pImpl_{std::make_unique<Impl>(name)} {}
Widget::~Widget() = default;  // defined here: Impl is complete at this point
Widget::Widget(Widget&&) noexcept = default;
Widget& Widget::operator=(Widget&&) noexcept = default;
Widget::Widget(const Widget& other) : pImpl_{std::make_unique<Impl>(*other.pImpl_)} {}
Widget& Widget::operator=(const Widget& other) {
    if (this != &other) *pImpl_ = *other.pImpl_;
    return *this;
}
void Widget::doSomething()            { pImpl_->doSomething(); }
std::string Widget::getName() const   { return pImpl_->getName(); }
int Widget::compute(int x, int y) const { return pImpl_->compute(x, y); }
```

### 27.3 Behavioral Patterns

```cpp
// ── Observer / Event System ───────────────────────────────────
template <typename... Args>
class Event {
    using Handler = std::function<void(Args...)>;
    std::vector<Handler> handlers_;

public:
    // Returns a "connection" ID that can be used to disconnect
    size_t connect(Handler handler) {
        handlers_.push_back(std::move(handler));
        return handlers_.size() - 1;
    }

    void disconnect(size_t id) {
        if (id < handlers_.size()) handlers_[id] = nullptr;
    }

    void emit(Args... args) {
        for (auto& h : handlers_) {
            if (h) h(args...);
        }
    }

    Event& operator+=(Handler h) { connect(std::move(h)); return *this; }
};

// Usage:
Event<int, std::string> onUserAction;
onUserAction += [](int id, const std::string& action) {
    std::cout << "User " << id << " did: " << action << "\n";
};
onUserAction += [](int id, const std::string&) {
    logToDatabase(id);
};
onUserAction.emit(42, "login");

// ── Strategy Pattern ──────────────────────────────────────────
// Modern C++: use std::function instead of abstract base class
using SortStrategy = std::function<void(std::vector<int>&)>;

struct Sorter {
    SortStrategy strategy;
    void sort(std::vector<int>& v) { strategy(v); }
};

Sorter s;
s.strategy = [](std::vector<int>& v) { std::sort(v.begin(), v.end()); };
s.sort(data);
s.strategy = [](std::vector<int>& v) { /* custom sort */ };  // swap at runtime
s.sort(data);

// ── CRTP — Compile-Time Polymorphism ─────────────────────────
// Curiously Recurring Template Pattern: avoids vtable overhead
template <typename Derived>
class Printable {
public:
    void print() const {
        static_cast<const Derived*>(this)->printImpl();  // no virtual dispatch!
    }
};

class Widget2 : public Printable<Widget2> {
public:
    void printImpl() const { std::cout << "Widget2\n"; }
};

// ── Type Erasure ──────────────────────────────────────────────
// Hide concrete types behind a uniform interface without inheritance
class AnyCallable {
    struct Base { virtual void call(int) = 0; virtual ~Base() = default; };
    template <typename F>
    struct Derived : Base {
        F f;
        explicit Derived(F f) : f{std::move(f)} {}
        void call(int x) override { f(x); }
    };
    std::unique_ptr<Base> impl_;
public:
    template <typename F>
    AnyCallable(F f) : impl_{std::make_unique<Derived<F>>(std::move(f))} {}
    void operator()(int x) { impl_->call(x); }
};
// (This is essentially what std::function does internally)
```

---

## Chapter 28: Testing — Catch2 and GoogleTest

### 28.1 GoogleTest

```cpp
// test/math_test.cpp
#include <gtest/gtest.h>
#include "math_utils.hpp"

// Basic test
TEST(FactorialTest, HandlesZero) {    // (TestSuite, TestName)
    EXPECT_EQ(factorial(0), 1);
    EXPECT_EQ(factorial(1), 1);
}

TEST(FactorialTest, HandlesPositive) {
    EXPECT_EQ(factorial(5), 120);
    EXPECT_EQ(factorial(10), 3628800);
}

TEST(FactorialTest, ThrowsOnNegative) {
    EXPECT_THROW(factorial(-1), std::invalid_argument);
    EXPECT_THROW(factorial(-100), std::invalid_argument);
}

// Assertion macros:
// EXPECT_*  — marks test failed, continues
// ASSERT_*  — marks test failed, stops current test immediately
EXPECT_EQ(a, b)          // a == b
EXPECT_NE(a, b)          // a != b
EXPECT_LT(a, b)          // a < b
EXPECT_LE(a, b)          // a <= b
EXPECT_GT(a, b)          // a > b
EXPECT_GE(a, b)          // a >= b
EXPECT_TRUE(condition)
EXPECT_FALSE(condition)
EXPECT_NEAR(a, b, eps)   // |a-b| <= eps (for floating-point)
EXPECT_THROW(expr, ExceptionType)
EXPECT_NO_THROW(expr)
EXPECT_ANY_THROW(expr)
EXPECT_STREQ(s1, s2)     // C-string equality
EXPECT_STRNE(s1, s2)
FAIL() << "Explicit failure message";
SUCCEED() << "Explicit success";

// Test Fixture — shared setup/teardown
class BankAccountTest : public ::testing::Test {
protected:
    void SetUp() override {                      // runs before EACH test
        account = std::make_unique<BankAccount>("Alice", 1000.0);
    }
    void TearDown() override { }                 // runs after EACH test

    std::unique_ptr<BankAccount> account;
};

TEST_F(BankAccountTest, InitialBalance) {
    EXPECT_DOUBLE_EQ(account->getBalance(), 1000.0);
}

TEST_F(BankAccountTest, Deposit) {
    account->deposit(500.0);
    EXPECT_DOUBLE_EQ(account->getBalance(), 1500.0);
}

TEST_F(BankAccountTest, WithdrawSuccess) {
    bool result = account->withdraw(200.0);
    EXPECT_TRUE(result);
    EXPECT_DOUBLE_EQ(account->getBalance(), 800.0);
}

TEST_F(BankAccountTest, WithdrawInsufficientFunds) {
    bool result = account->withdraw(2000.0);
    EXPECT_FALSE(result);
    EXPECT_DOUBLE_EQ(account->getBalance(), 1000.0);  // unchanged
}

// Parameterized tests — same test with different inputs
class FactorialParamTest
    : public ::testing::TestWithParam<std::pair<int,long long>> {};

TEST_P(FactorialParamTest, ComputesCorrectly) {
    auto [input, expected] = GetParam();
    EXPECT_EQ(factorial(input), expected);
}

INSTANTIATE_TEST_SUITE_P(
    FactorialValues,
    FactorialParamTest,
    ::testing::Values(
        std::make_pair(0, 1LL),
        std::make_pair(1, 1LL),
        std::make_pair(5, 120LL),
        std::make_pair(10, 3628800LL)
    )
);

// Death tests — test that code calls abort/exit or throws
TEST(DeathTest, DivisionByZero) {
    EXPECT_DEATH(divide(1, 0), "division by zero");  // matches message with regex
}

// Test with mock (using GoogleMock)
#include <gmock/gmock.h>
class MockDatabase : public IDatabase {
public:
    MOCK_METHOD(User, findUser, (int id), (override));
    MOCK_METHOD(bool, saveUser, (const User& user), (override));
    MOCK_METHOD(void, deleteUser, (int id), (override));
};

TEST(UserServiceTest, GetExistingUser) {
    MockDatabase mockDb;
    User alice{1, "Alice", "alice@example.com"};

    EXPECT_CALL(mockDb, findUser(1))
        .Times(1)
        .WillOnce(::testing::Return(alice));

    UserService service{&mockDb};
    User result = service.getUser(1);
    EXPECT_EQ(result.name, "Alice");
}
```

### 28.2 Catch2

```cpp
// test/math_test.cpp
#define CATCH_CONFIG_MAIN  // or: #include <catch2/catch_session.hpp> in separate file
#include <catch2/catch_all.hpp>

TEST_CASE("factorial") {
    SECTION("base cases") {
        REQUIRE(factorial(0) == 1);
        REQUIRE(factorial(1) == 1);
    }

    SECTION("positive numbers") {
        REQUIRE(factorial(5)  == 120);
        REQUIRE(factorial(10) == 3628800);
    }

    SECTION("negative throws") {
        REQUIRE_THROWS_AS(factorial(-1), std::invalid_argument);
    }
}

// Catch2 assertions:
REQUIRE(expr)            // FAIL and stop test if false
CHECK(expr)              // FAIL but continue if false
REQUIRE_FALSE(expr)
CHECK_FALSE(expr)
REQUIRE_THROWS(expr)     // expr must throw something
REQUIRE_THROWS_AS(expr, ExceptionType)
REQUIRE_NOTHROW(expr)
REQUIRE_THAT(val, matcher)   // with Matchers

// Approx for floating-point
REQUIRE(3.14 == Catch::Approx(3.14159).epsilon(0.01));  // within 1%
REQUIRE(3.14 == Catch::Approx(3.14159).margin(0.002));  // within absolute margin

// BDD style
SCENARIO("bank account") {
    GIVEN("an account with $1000") {
        BankAccount account("Alice", 1000);

        WHEN("depositing $500") {
            account.deposit(500);
            THEN("balance is $1500") {
                REQUIRE(account.getBalance() == Approx(1500.0));
            }
        }

        WHEN("withdrawing $200") {
            bool ok = account.withdraw(200);
            THEN("succeeds and balance is $800") {
                REQUIRE(ok);
                REQUIRE(account.getBalance() == Approx(800.0));
            }
        }

        WHEN("withdrawing $2000 (insufficient funds)") {
            bool ok = account.withdraw(2000);
            THEN("fails and balance unchanged") {
                REQUIRE_FALSE(ok);
                REQUIRE(account.getBalance() == Approx(1000.0));
            }
        }
    }
}

// Parameterized tests
TEMPLATE_TEST_CASE("works for all numeric types", "", int, long, double, float) {
    TestType x = 5;
    TestType y = 3;
    REQUIRE(x + y == TestType{8});
}

TEST_CASE("various inputs", "[parameterized]") {
    auto [input, expected] = GENERATE(table<int, int>({
        {0, 0}, {1, 1}, {2, 4}, {3, 9}, {4, 16}
    }));
    REQUIRE(square(input) == expected);
}
```

---

## Chapter 29: Build Systems — CMake, vcpkg, Conan

### 29.1 vcpkg — Package Manager

```bash
# Install vcpkg
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg && ./bootstrap-vcpkg.sh

# Install packages
./vcpkg install fmt
./vcpkg install gtest
./vcpkg install boost-filesystem
./vcpkg install nlohmann-json
./vcpkg install spdlog

# Integrate with CMake (toolchain file method — preferred)
cmake .. -DCMAKE_TOOLCHAIN_FILE=/path/to/vcpkg/scripts/buildsystems/vcpkg.cmake

# Or: manifest mode (vcpkg.json in project root — reproducible builds)
# vcpkg.json:
{
  "name": "my-project",
  "version": "1.0.0",
  "dependencies": [
    "fmt",
    "gtest",
    { "name": "boost-filesystem", "version>=": "1.82.0" },
    "nlohmann-json"
  ]
}
# Then cmake automatically installs from vcpkg.json
```

### 29.2 Complete CMake Project Structure

```cmake
# Modern CMake project template

cmake_minimum_required(VERSION 3.25)
project(MyProject VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export compile commands for clangd (IDE integration)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ── Compile options helper ─────────────────────────────────────
function(set_project_warnings target)
    target_compile_options(${target} PRIVATE
        $<$<CXX_COMPILER_ID:GNU,Clang>:
            -Wall -Wextra -Wpedantic -Wconversion -Wshadow
            -Wno-unused-parameter>
        $<$<CXX_COMPILER_ID:MSVC>:
            /W4 /WX>
    )
endfunction()

# ── Sanitizers ─────────────────────────────────────────────────
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
option(ENABLE_UBSAN "Enable UBSanitizer" OFF)
option(ENABLE_TSAN "Enable ThreadSanitizer" OFF)

if(ENABLE_ASAN)
    add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
    add_link_options(-fsanitize=address)
endif()
if(ENABLE_UBSAN)
    add_compile_options(-fsanitize=undefined)
    add_link_options(-fsanitize=undefined)
endif()

# ── Dependencies ───────────────────────────────────────────────
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

include(FetchContent)
FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0)
FetchContent_MakeAvailable(googletest)

# ── Main library ───────────────────────────────────────────────
add_library(mylib STATIC
    src/utils.cpp
    src/math.cpp
    src/io.cpp
)
target_include_directories(mylib PUBLIC include/ PRIVATE src/)
target_link_libraries(mylib PUBLIC fmt::fmt PRIVATE spdlog::spdlog)
target_compile_features(mylib PUBLIC cxx_std_20)
set_project_warnings(mylib)

# ── Main executable ────────────────────────────────────────────
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)
set_project_warnings(myapp)

# ── Tests ──────────────────────────────────────────────────────
enable_testing()
add_executable(unit_tests
    tests/math_test.cpp
    tests/utils_test.cpp
    tests/io_test.cpp
)
target_link_libraries(unit_tests PRIVATE mylib GTest::gtest_main GTest::gmock)
set_project_warnings(unit_tests)
include(GoogleTest)
gtest_discover_tests(unit_tests PROPERTIES TIMEOUT 30)

# ── Code coverage ──────────────────────────────────────────────
option(ENABLE_COVERAGE "Enable code coverage" OFF)
if(ENABLE_COVERAGE)
    target_compile_options(mylib PRIVATE --coverage)
    target_link_options(mylib PRIVATE --coverage)
    # Run: gcov / lcov to collect and display coverage
endif()

# ── Installation ───────────────────────────────────────────────
include(GNUInstallDirs)
install(TARGETS myapp mylib
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# Generate package config for other CMake projects to use find_package
include(CMakePackageConfigHelpers)
install(EXPORT MyProjectTargets
    FILE MyProjectTargets.cmake
    NAMESPACE MyProject::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyProject
)
```

```bash
# Development workflow
mkdir build && cd build

# Debug with sanitizers
cmake .. -DCMAKE_BUILD_TYPE=Debug -DENABLE_ASAN=ON -DENABLE_UBSAN=ON
cmake --build . -j$(nproc)
ctest --output-on-failure

# Release
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)

# Coverage
cmake .. -DCMAKE_BUILD_TYPE=Debug -DENABLE_COVERAGE=ON
cmake --build .
ctest
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
```

---

## Chapter 30: Performance & Optimization

### 30.1 Measuring Before Optimizing

```cpp
// Rule: measure first, optimize second
// "Premature optimization is the root of all evil" — Knuth

// Simple timing
#include <chrono>
auto start = std::chrono::high_resolution_clock::now();
doExpensiveWork();
auto end   = std::chrono::high_resolution_clock::now();
auto dur   = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
std::cout << "Took: " << dur.count() << " µs\n";

// Google Benchmark (de facto standard)
#include <benchmark/benchmark.h>

static void BM_VectorPushBack(benchmark::State& state) {
    for (auto _ : state) {                    // loop controlled by benchmark framework
        std::vector<int> v;
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v.data());   // prevent optimization from removing code
        benchmark::ClobberMemory();           // force memory writes to complete
    }
    state.SetComplexityN(state.range(0));    // for O(n) complexity measurement
}
BENCHMARK(BM_VectorPushBack)->Range(8, 8<<10)->Complexity();

static void BM_VectorReserved(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        v.reserve(state.range(0));   // pre-allocate
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
    }
}
BENCHMARK(BM_VectorReserved)->Range(8, 8<<10);

BENCHMARK_MAIN();
```

### 30.2 Cache-Friendly Data Structures

```cpp
// L1 cache: ~32 KB, ~1ns
// L2 cache: ~256 KB, ~5ns
// L3 cache: ~8 MB, ~20ns
// RAM: GBs, ~60-100ns

// Cache line: 64 bytes on x86 — data loaded in 64-byte chunks

// ❌ Cache-unfriendly: Array of Structures (AoS)
struct Particle {
    float x, y, z;       // position (12 bytes)
    float vx, vy, vz;    // velocity (12 bytes)
    float mass;           // mass (4 bytes)
    float padding[1];     // 4 bytes padding → total 32 bytes per particle
};
std::vector<Particle> particles;

// Updating only positions: loads entire 32-byte particle into cache
// But only uses 12 bytes (x,y,z) → 62% cache waste
void updatePositions(std::vector<Particle>& p, float dt) {
    for (auto& particle : p) {
        particle.x += particle.vx * dt;   // good access
        particle.y += particle.vy * dt;   // but loads vx,vy,vz,mass unnecessarily
        particle.z += particle.vz * dt;
    }
}

// ✅ Cache-friendly: Structure of Arrays (SoA)
struct ParticlesSoA {
    std::vector<float> x, y, z;    // all positions together
    std::vector<float> vx, vy, vz; // all velocities together
    std::vector<float> mass;
    size_t count = 0;
};

// Updating positions: accesses x[], y[], z[], vx[], vy[], vz[]
// Sequential access = prefetcher works perfectly = near-peak memory bandwidth
void updatePositionsSoA(ParticlesSoA& p, float dt) {
    for (size_t i = 0; i < p.count; ++i) {
        p.x[i] += p.vx[i] * dt;   // 6 arrays accessed sequentially
        p.y[i] += p.vy[i] * dt;   // CPU prefetcher can predict next access
        p.z[i] += p.vz[i] * dt;
    }
    // This code also auto-vectorizes (SIMD) much better with SoA
}

// False sharing — different threads modify adjacent cache lines
// ❌ Thread 0 and Thread 1 both modify different fields that share a cache line:
struct BadCounters {
    int counter_t0;   // thread 0's counter
    int counter_t1;   // thread 1's counter
    // Both fit in ONE 64-byte cache line → writing to one invalidates other!
};

// ✅ Pad to separate cache lines
struct alignas(64) PaddedCounter {
    int value;
    char padding[60];  // pad to fill 64-byte cache line
};
PaddedCounter counters[2];  // now on separate cache lines
```

---

## Chapter 31: Best Practices & Undefined Behavior

### 31.1 The UB Catalogue — What to Never Do

```cpp
// UNDEFINED BEHAVIOR: the compiler may do ANYTHING (not just crash)
// The optimizer ASSUMES UB never happens → may produce wrong code silently

// ① Null pointer dereference
int* p = nullptr;
*p = 42;                    // ❌ UB — crash on most platforms, but not guaranteed

// ② Out-of-bounds array access
int arr[5];
arr[5] = 0;                 // ❌ UB — may corrupt memory or crash
arr[-1] = 0;                // ❌ UB

// ③ Signed integer overflow
int max = INT_MAX;
int overflow = max + 1;     // ❌ UB — compiler assumes this never happens!
// Optimizer may: remove the "if (x + 1 < x)" check (always false if no overflow)
// Use unsigned for wrapping, or __builtin_add_overflow, or std::add_sat (C++26)

// ④ Uninitialized variable reads
int x;
std::cout << x;             // ❌ UB — could be anything; optimizer may use "any" value

// ⑤ Dangling pointer/reference
int* makeInt() {
    int local = 42;
    return &local;           // ❌ local destroyed; pointer dangles
}
int* p2 = makeInt();
*p2;                        // ❌ UB — local is gone

// ⑥ Use after free
int* heap = new int{42};
delete heap;
*heap = 99;                 // ❌ UB — memory freed; might corrupt allocator

// ⑦ Double free
delete heap;                // ❌ UB — already freed!

// ⑧ Strict aliasing violation
// Accessing memory as a different type (except char/unsigned char/std::byte)
float f = 1.0f;
int*  ip = reinterpret_cast<int*>(&f);
*ip = 0;                    // ❌ UB (use std::bit_cast or memcpy instead)

// ⑨ Data races (two threads, one write, no sync)
int shared = 0;
std::thread t1([&]{ shared = 1; });  // ❌ UB: data race if no mutex
std::thread t2([&]{ shared = 2; });
t1.join(); t2.join();

// ⑩ Modifying a const object
const int ci = 42;
int* mutable_p = const_cast<int*>(&ci);
*mutable_p = 99;            // ❌ UB — const object modification

// ⑪ Calling a function through a wrong-typed pointer
void myFunc() {}
int (*wrongType)() = reinterpret_cast<int(*)()>(myFunc);
wrongType();                // ❌ UB — wrong function type

// ⑫ Returning from a non-void function without a return
int bad_func() {
    int x = 5;
    // no return!
}                           // ❌ UB if caller uses the return value

// HOW TO CATCH UB: compile with sanitizers!
// g++ -fsanitize=address,undefined,thread main.cpp -o main
// Run the program — sanitizers will catch UB at runtime

// Static analysis
// clang-tidy, cppcheck, PVS-Studio, Coverity
```

### 31.2 The Core Guidelines — Summary Rules

```cpp
// I. Use RAII for all resources
// ❌ raw new/delete
Widget* w = new Widget{};
doSomething(w);
delete w;  // might not execute!

// ✅ smart pointer
auto w = std::make_unique<Widget>();
doSomething(w.get());
// auto-deleted

// II. Prefer const
// Make everything const by default; remove const when you need to modify
void processUser(const User& user);      // ✅ read-only
int getCount() const;                    // ✅ const member function
const int SIZE = 100;                    // ✅ constant

// III. Prefer value semantics
// ❌ heap allocation for small objects
auto p = std::make_unique<Point>(1, 2);
p->x;

// ✅ value type (stack allocated, copyable, movable)
Point p{1, 2};
p.x;

// IV. Avoid raw owning pointers
// ✅ Use: unique_ptr (single owner), shared_ptr (shared), value type (no ownership)
// ✅ Raw pointer: only for non-owning access ("observer") — document this intent

// V. Use standard algorithms over raw loops
// ❌ Raw loop
int sum = 0;
for (int i = 0; i < v.size(); ++i) if (v[i] > 0) sum += v[i];

// ✅ Standard algorithms (more expressive, harder to get wrong)
int sum = std::reduce(
    std::execution::par,   // potentially parallel!
    v.begin(), v.end(), 0,
    [](int acc, int x){ return x > 0 ? acc + x : acc; }
);

// VI. Handle all errors
// ❌ Ignoring errors
void writeFile() {
    std::ofstream f{"out.txt"};
    f << data;  // what if write fails?
}

// ✅ Check and handle
void writeFile() {
    std::ofstream f{"out.txt"};
    if (!f) throw std::runtime_error("Cannot open out.txt");
    f << data;
    if (!f) throw std::runtime_error("Write failed");
}
```

---

## Appendix: C++ Quick Reference

### The Big Five Decision Table
```
Does your class manage a raw resource (pointer, file handle, socket, lock)?
    NO  → Rule of Zero: don't define any of the Big Five (compiler generates correct ones)
    YES → Rule of Five: define all five (destructor, copy ctor, copy =, move ctor, move =)

Quick pattern:
    class OwnedResource {
        Resource* ptr_;
    public:
        OwnedResource() : ptr_{new Resource{}} {}
        ~OwnedResource()                              { delete ptr_; }
        OwnedResource(const OwnedResource& o)         : ptr_{new Resource{*o.ptr_}} {}
        OwnedResource& operator=(const OwnedResource& o) {
            if (this != &o) { delete ptr_; ptr_ = new Resource{*o.ptr_}; }
            return *this;
        }
        OwnedResource(OwnedResource&& o) noexcept    : ptr_{std::exchange(o.ptr_, nullptr)} {}
        OwnedResource& operator=(OwnedResource&& o) noexcept {
            if (this != &o) { delete ptr_; ptr_ = std::exchange(o.ptr_, nullptr); }
            return *this;
        }
    };
```

### Parameter Passing Rules
```
Type             Read-only         Read-write / Out    Sink (take ownership)
─────────────────────────────────────────────────────────────────────────────
int, char, ptr   by value T        by reference T&     by value T
small struct     by value T        by reference T&     by value T
large struct     by const ref T&   by reference T&     by value T + move in body
unique_ptr       by *T or ref T&   by *T               by value unique_ptr<T>
shared_ptr       by const ref T&   by ref T&           by value shared_ptr<T>
string           by string_view    by string&          by value string + move
```

### When to Use What Container
```
Need:                              Use:
──────────────────────────────────────────────────────────────────────────
Fast random access                 std::vector (default choice)
Compile-time fixed size            std::array
Fast push/pop at both ends         std::deque
O(1) insert/delete anywhere        std::list (need iterator)
Sorted unique elements             std::set
Sorted key-value                   std::map
Fast O(1) lookup by key            std::unordered_map
LIFO (stack)                       std::stack or std::vector (with back)
FIFO (queue)                       std::queue or std::deque
Priority queue (max-heap)          std::priority_queue
Bitset                             std::bitset<N>
```

### Common Headers Reference
```cpp
// Language support
#include <cstddef>   // size_t, ptrdiff_t, nullptr_t, byte
#include <cstdint>   // int32_t, uint64_t, etc.
#include <cstdlib>   // malloc, free, exit, rand
#include <cassert>   // assert()
#include <cstring>   // memcpy, strlen, strcmp
#include <cmath>     // sqrt, sin, pow, floor, ceil
#include <climits>   // INT_MAX, CHAR_BIT
#include <limits>    // std::numeric_limits<T>
#include <typeinfo>  // typeid, type_info

// Utilities
#include <utility>      // move, forward, swap, pair, make_pair, exchange
#include <tuple>        // tuple, make_tuple, get, tie, apply
#include <optional>     // optional (C++17)
#include <variant>      // variant (C++17)
#include <any>          // any (C++17)
#include <expected>     // expected (C++23)
#include <functional>   // function, bind, placeholders, hash
#include <type_traits>  // is_integral_v, decay_t, etc.
#include <concepts>     // standard concepts (C++20)
#include <bit>          // popcount, bit_cast, bit_ceil (C++20)

// Memory
#include <memory>       // unique_ptr, shared_ptr, weak_ptr, make_unique, make_shared
#include <new>          // placement new, bad_alloc, nothrow
#include <memory_resource>  // pmr (C++17)

// Strings
#include <string>       // std::string
#include <string_view>  // std::string_view (C++17)
#include <charconv>     // from_chars, to_chars (C++17)
#include <format>       // std::format (C++20)
#include <regex>        // std::regex

// Containers
#include <array>        // std::array
#include <vector>       // std::vector
#include <deque>        // std::deque
#include <list>         // std::list
#include <forward_list> // std::forward_list
#include <set>          // std::set, std::multiset
#include <map>          // std::map, std::multimap
#include <unordered_set>// std::unordered_set
#include <unordered_map>// std::unordered_map
#include <stack>        // std::stack
#include <queue>        // std::queue, std::priority_queue
#include <bitset>       // std::bitset<N>
#include <span>         // std::span (C++20)
#include <mdspan>       // std::mdspan (C++23)

// Algorithms
#include <algorithm>    // sort, find, transform, reduce, etc.
#include <numeric>      // accumulate, iota, inner_product
#include <execution>    // execution policies: par, par_unseq (C++17)
#include <ranges>       // ranges, views (C++20)
#include <iterator>     // iterators, back_inserter, etc.

// I/O
#include <iostream>     // cin, cout, cerr, clog
#include <fstream>      // ifstream, ofstream, fstream
#include <sstream>      // stringstream, ostringstream, istringstream
#include <iomanip>      // setw, setprecision, hex, fixed, etc.
#include <filesystem>   // std::filesystem (C++17)
#include <print>        // std::print (C++23)

// Concurrency
#include <thread>       // std::thread, jthread (C++20)
#include <mutex>        // mutex, lock_guard, unique_lock, scoped_lock
#include <shared_mutex> // shared_mutex, shared_lock (C++17)
#include <condition_variable>  // condition_variable
#include <atomic>       // atomic<T>, atomic_flag
#include <future>       // future, promise, async, packaged_task
#include <semaphore>    // counting_semaphore, binary_semaphore (C++20)
#include <latch>        // latch (C++20)
#include <barrier>      // barrier (C++20)

// Error handling
#include <exception>    // exception, bad_exception, terminate
#include <stdexcept>    // runtime_error, logic_error, range_error, etc.
#include <system_error> // error_code, error_condition, system_error

// Time
#include <chrono>       // duration, time_point, system_clock, high_resolution_clock

// Random
#include <random>       // mt19937, uniform_int_distribution, etc.

// Math
#include <cmath>        // sin, cos, sqrt, pow, log, etc.
#include <numbers>      // pi, e, sqrt2, etc. (C++20)
#include <complex>      // complex<T>
#include <valarray>     // valarray (vectorized operations)
```

---

## Chapter 10 (continued): Constructors, Destructors & RAII — Full Depth

### The Big Five — Copy-and-Swap Idiom

```cpp
// Copy-and-swap: elegant, exception-safe assignment
class String {
    char* data_;
    size_t size_;

public:
    String(const char* s = "") : size_{strlen(s)}, data_{new char[size_ + 1]} {
        memcpy(data_, s, size_ + 1);
    }
    ~String() { delete[] data_; }

    // Copy constructor
    String(const String& other) : size_{other.size_}, data_{new char[size_ + 1]} {
        memcpy(data_, other.data_, size_ + 1);
    }

    // Move constructor
    String(String&& other) noexcept
        : size_{other.size_}, data_{other.data_} {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // UNIFIED assignment using copy-and-swap idiom:
    // Takes by VALUE: either copy-constructed or move-constructed depending on caller
    String& operator=(String other) noexcept {  // 'other' is already a copy/move
        swap(*this, other);                       // swap our data with the copy
        return *this;
        // 'other' (which now holds OUR old data) is destroyed here → safe
    }

    friend void swap(String& a, String& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
        swap(a.size_, b.size_);
    }
};

String s1{"hello"};
String s2{"world"};
s2 = s1;              // copy: operator=(String other) — other copy-constructed from s1
s2 = std::move(s1);   // move: operator=(String other) — other move-constructed from s1
```

---

## Chapter 13 (continued): Templates — Full Depth

### Template Specialization — Complete

```cpp
// Primary template
template <typename T>
struct TypeInfo {
    static const char* name() { return "unknown"; }
    static bool is_integer() { return false; }
};

// Full specialization — specific type
template <>
struct TypeInfo<int> {
    static const char* name() { return "int"; }
    static bool is_integer() { return true; }
    static int max() { return INT_MAX; }   // can add new members
};

template <>
struct TypeInfo<double> {
    static const char* name() { return "double"; }
    static bool is_integer() { return false; }
};

// Partial specialization — specialize for a family of types
template <typename T>
struct TypeInfo<T*> {
    static const char* name() { return "pointer"; }
    static bool is_pointer() { return true; }
};

template <typename T>
struct TypeInfo<std::vector<T>> {
    static const char* name() { return "vector"; }
    static size_t element_size() { return sizeof(T); }
};

// Usage
TypeInfo<int>::name()              // "int"
TypeInfo<double>::name()           // "double"
TypeInfo<int*>::name()             // "pointer"
TypeInfo<std::vector<float>>::element_size()  // 4

// Function template specialization (less useful than class specialization)
template <typename T>
void print(T val) { std::cout << val << "\n"; }

template <>
void print<bool>(bool val) { std::cout << (val ? "true" : "false") << "\n"; }
```

### SFINAE and enable_if (pre-C++20)

```cpp
// SFINAE: Substitution Failure Is Not An Error
// If a template substitution fails, that overload is silently discarded

// Only enable this function for integer types
template <typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
T doubleIt(T x) { return x * 2; }

// Alternative: return type SFINAE
template <typename T>
std::enable_if_t<std::is_integral_v<T>, T>  // return type is T only if T is integral
doubleIt2(T x) { return x * 2; }

// Multiple overloads selected by SFINAE:
template <typename T>
std::enable_if_t<std::is_floating_point_v<T>, std::string>
describe(T val) { return "float: " + std::to_string(val); }

template <typename T>
std::enable_if_t<std::is_integral_v<T>, std::string>
describe(T val) { return "int: " + std::to_string(val); }

// C++20 — replace all of the above with concepts (much cleaner):
template <std::integral T>
T doubleIt_20(T x) { return x * 2; }

std::string describe_20(std::floating_point auto val) { return "float: " + std::to_string(val); }
std::string describe_20(std::integral auto val)       { return "int: " + std::to_string(val); }
```

### Variadic Templates — Full Power

```cpp
// Fold expressions (C++17) — operate on parameter packs
template <typename... Args>
auto sum(Args... args) {
    return (... + args);          // left fold:  ((a+b)+c)+d
}
template <typename... Args>
auto product(Args... args) {
    return (args * ...);          // right fold: a*(b*(c*d))
}
template <typename... Args>
void print_all(Args&&... args) {
    (std::cout << ... << args);   // fold with <<: cout<<a, then <<b, then <<c
    std::cout << "\n";
}
template <typename... Args>
bool all_positive(Args... args) {
    return ((args > 0) && ...);   // fold with &&: a>0 && b>0 && c>0
}

sum(1, 2, 3, 4, 5);         // 15
all_positive(1, 2, 3);      // true
all_positive(1, -2, 3);     // false
print_all("hello", " ", 42, " world\n");

// Tuple iteration using fold
template <typename Tuple, typename Fn, size_t... I>
void tupleForEach_impl(Tuple&& t, Fn&& f, std::index_sequence<I...>) {
    (f(std::get<I>(t)), ...);   // fold: f(get<0>(t)), f(get<1>(t)), ...
}

template <typename Tuple, typename Fn>
void tupleForEach(Tuple&& t, Fn&& f) {
    constexpr size_t N = std::tuple_size_v<std::decay_t<Tuple>>;
    tupleForEach_impl(std::forward<Tuple>(t), std::forward<Fn>(f),
                      std::make_index_sequence<N>{});
}

auto tup = std::tuple{1, 2.5, std::string{"hello"}};
tupleForEach(tup, [](auto x){ std::cout << x << " "; });  // "1 2.5 hello"
```

---

## Chapter 14 (continued): Move Semantics — Full Depth

### Universal References vs Rvalue References

```cpp
// Rvalue reference in non-template: only binds to rvalues
void process(Widget&& w) { }  // rvalue reference — only temporaries/moved

// T&& in a TEMPLATE: this is a FORWARDING (UNIVERSAL) reference
// It binds to ANYTHING: lvalue, const lvalue, rvalue
template <typename T>
void forward_me(T&& arg) {     // T&& is a FORWARDING reference (not rvalue ref!)
    // If caller passes lvalue: T = Widget&, arg is Widget& (lvalue ref)
    // If caller passes rvalue: T = Widget,  arg is Widget&& (rvalue ref)
    process(std::forward<T>(arg));  // forward preserves the original value category
}

Widget w;
forward_me(w);           // lvalue: T=Widget&, passes lvalue to process
forward_me(Widget{});    // rvalue: T=Widget, passes rvalue to process
forward_me(std::move(w));// rvalue: same as above

// std::forward implementation (approximately):
template <typename T>
T&& my_forward(std::remove_reference_t<T>& t) {
    return static_cast<T&&>(t);  // cast to T&& (might be lvalue or rvalue ref)
}

// Named rvalue references ARE lvalues!
void demonstrate(Widget&& w) {
    // 'w' has a name → it IS an lvalue inside the function body
    process(w);             // passes as LVALUE (copies Widget)
    process(std::move(w));  // now passes as RVALUE (moves Widget)
}
```

### Perfect Forwarding — Factory Functions

```cpp
// emplace_back uses perfect forwarding to construct in-place:
template <typename T, typename Allocator>
template <typename... Args>
reference vector<T, Allocator>::emplace_back(Args&&... args) {
    // constructs T with args... directly in the vector's memory
    // no temporary created, no extra move
    construct(data_ + size_, std::forward<Args>(args)...);
    ++size_;
}

// Your own factory with perfect forwarding:
template <typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    return std::unique_ptr<T>{new T{std::forward<Args>(args)...}};
}
// Exactly what std::make_unique does

auto w = make<Widget>("hello", 42, true);
// Constructs Widget("hello", 42, true) directly on heap
// "hello" stays const char*; 42 stays int; true stays bool — no unnecessary conversions
```

---

## Chapter 15 (continued): Smart Pointers — Full Depth

### enable_shared_from_this — Safe shared_ptr from this

```cpp
// Problem: creating a shared_ptr from 'this' inside a member function
class Node : public std::enable_shared_from_this<Node> {
public:
    std::shared_ptr<Node> next;
    int value;

    explicit Node(int v) : value{v} {}

    // ❌ WRONG — creates SECOND independent control block — double free!
    std::shared_ptr<Node> getSelf_BAD() {
        return std::shared_ptr<Node>{this};  // two shared_ptrs, independent ref counts!
    }

    // ✅ CORRECT — returns shared_ptr sharing the EXISTING control block
    std::shared_ptr<Node> getSelf() {
        return shared_from_this();  // uses existing control block
    }
};

auto n = std::make_shared<Node>(42);
auto same = n->getSelf();    // same and n share ownership; ref count = 2
// std::shared_ptr<Node> bad{n.get()}; // ❌ creates a second control block!

// Common use: registering 'this' as a callback
class EventListener : public std::enable_shared_from_this<EventListener> {
    EventSystem& events_;
public:
    explicit EventListener(EventSystem& ev) : events_{ev} {}

    void subscribe() {
        // Register self as listener — safe because shared_from_this shares ownership
        events_.onEvent([self = shared_from_this()](Event e) {
            self->handleEvent(e);
        });
    }

    void handleEvent(Event e) { /* ... */ }
};
```

### Custom Deleters

```cpp
// unique_ptr with custom deleter
// Use for resources with non-standard cleanup

// FILE*
auto file = std::unique_ptr<FILE, decltype(&fclose)>{
    fopen("data.txt", "r"), fclose
};
// Or:
struct FileDeleter {
    void operator()(FILE* f) const { if (f) fclose(f); }
};
std::unique_ptr<FILE, FileDeleter> file2{fopen("data.txt", "r")};

// OpenGL resource
struct GLBufferDeleter {
    void operator()(GLuint* id) const {
        glDeleteBuffers(1, id);
        delete id;
    }
};
auto vbo = std::unique_ptr<GLuint, GLBufferDeleter>{new GLuint};
glGenBuffers(1, vbo.get());

// Generic RAII wrapper with custom deleter
template <typename T, typename Deleter = std::default_delete<T>>
using UniqueResource = std::unique_ptr<T, Deleter>;

// shared_ptr with custom deleter (stored in control block — type-erased)
std::shared_ptr<FILE> sharedFile{fopen("data.txt", "r"), fclose};
// shared_ptr deleter is type-erased, more flexible but larger overhead

// std::shared_ptr for non-owning management of arrays
auto arr = std::shared_ptr<int[]>{new int[100]};  // C++17: shared_ptr<T[]>
arr[0] = 1;  arr[99] = 99;  // works with []
```

---

## Data Structures & Algorithms in C++

### Complexity Analysis — C++ Perspective

```cpp
// Time complexity of STL containers:

// std::vector:
// push_back:      O(1) amortized (O(n) when reallocating)
// insert middle:  O(n) — shifts elements
// erase middle:   O(n) — shifts elements
// random access:  O(1) — arr[i]
// search:         O(n) — linear scan

// std::unordered_map:
// insert/find/erase: O(1) average, O(n) worst (hash collision)
// iteration:         O(n)

// std::map:
// insert/find/erase: O(log n) — Red-Black tree
// iteration:         O(n) in sorted order

// std::set:
// insert/find/erase: O(log n)

// std::priority_queue:
// push: O(log n)   pop: O(log n)   top: O(1)
```

### Implementing Key Algorithms

```cpp
// Binary Search
template <typename ForwardIt, typename T>
ForwardIt binarySearch(ForwardIt begin, ForwardIt end, const T& target) {
    auto lo = begin, hi = end;
    while (lo != hi) {
        auto mid = lo + std::distance(lo, hi) / 2;
        if (*mid < target)      lo = mid + 1;
        else if (target < *mid) hi = mid;
        else                    return mid;
    }
    return end;  // not found
}
// std::binary_search, std::lower_bound, std::upper_bound for real use

// Merge Sort
template <typename T>
void mergeSort(std::vector<T>& arr, size_t left, size_t right) {
    if (right - left <= 1) return;
    size_t mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid, right);
    std::inplace_merge(arr.begin() + left, arr.begin() + mid, arr.begin() + right);
}

// Quicksort (std::sort uses introsort, which is quicksort + heapsort + insertion)
template <typename T>
void quickSort(std::vector<T>& arr, int lo, int hi) {
    if (lo >= hi) return;
    T pivot = arr[lo + (hi - lo) / 2];
    int i = lo, j = hi;
    while (i <= j) {
        while (arr[i] < pivot) ++i;
        while (arr[j] > pivot) --j;
        if (i <= j) { std::swap(arr[i++], arr[j--]); }
    }
    quickSort(arr, lo, j);
    quickSort(arr, i, hi);
}
// In practice: std::sort() is always faster — uses introsort

// Graph BFS (C++ style)
#include <queue>
#include <unordered_map>
#include <unordered_set>

std::unordered_map<int, std::vector<int>> graph;

std::vector<int> bfs(int start) {
    std::vector<int> result;
    std::unordered_set<int> visited;
    std::queue<int> q;

    q.push(start);
    visited.insert(start);

    while (!q.empty()) {
        int node = q.front(); q.pop();
        result.push_back(node);
        for (int neighbor : graph[node]) {
            if (!visited.count(neighbor)) {
                visited.insert(neighbor);
                q.push(neighbor);
            }
        }
    }
    return result;
}

// Dijkstra's Shortest Path
#include <priority_queue>
std::vector<long long> dijkstra(int src, int n,
    const std::vector<std::vector<std::pair<int,int>>>& adj) {

    std::vector<long long> dist(n, LLONG_MAX);
    std::priority_queue<std::pair<long long,int>,
                        std::vector<std::pair<long long,int>>,
                        std::greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;  // stale entry
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// Dynamic Programming — LCS
int lcs(const std::string& a, const std::string& b) {
    int m = a.size(), n = b.size();
    std::vector<std::vector<int>> dp(m+1, std::vector<int>(n+1, 0));
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j)
            dp[i][j] = (a[i-1] == b[j-1]) ? dp[i-1][j-1] + 1
                                            : std::max(dp[i-1][j], dp[i][j-1]);
    return dp[m][n];
}

// Linked List (rarely written by hand; std::list for real code)
template <typename T>
struct Node { T data; Node* next = nullptr; };

template <typename T>
class LinkedList {
    Node<T>* head_ = nullptr;
    size_t   size_ = 0;
public:
    ~LinkedList() { while (head_) { auto n = head_->next; delete head_; head_ = n; } }

    void push_front(T val) {
        auto node = new Node<T>{val, head_};
        head_ = node;
        ++size_;
    }

    void reverse() {
        Node<T>* prev = nullptr;
        Node<T>* curr = head_;
        while (curr) {
            Node<T>* next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        head_ = prev;
    }

    bool hasCycle() const {
        auto slow = head_, fast = head_;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) return true;
        }
        return false;
    }
};
```

---

## Chapter 23 (continued): Error Handling — Full Depth

### Exception Safety and noexcept

```cpp
// Three levels of exception safety:

// ① Basic guarantee: no resource leaks; invariants maintained; object in valid state
void basicSafe(std::vector<int>& v, int val) {
    v.push_back(val);    // if this throws (bad_alloc): v is unchanged (push_back is strongly safe)
    throw std::runtime_error("oops");  // v still has the element we pushed
}   // no leaks — v is still a valid vector

// ② Strong guarantee: either succeeds completely or has no observable effect (transactional)
void strongSafe(MyData& data, const UpdateRequest& req) {
    MyData backup = data;          // save current state
    try {
        data.field1 = req.f1;
        data.process();            // might throw
        data.field2 = req.f2;
    } catch (...) {
        data = std::move(backup);  // restore original state
        throw;
    }
}

// ③ Nothrow guarantee: operation always succeeds (marked noexcept)
void nothrowSafe(int& a, int& b) noexcept {
    using std::swap;
    swap(a, b);    // swap of ints is noexcept
}

// WHY noexcept matters for performance:
// std::vector::resize, push_back, emplace_back check if move constructor is noexcept
// If it is: they MOVE elements when reallocating (fast)
// If not:   they COPY elements when reallocating (safe but slow)
// ALWAYS mark move constructor and move assignment as noexcept!

class MyClass {
public:
    MyClass(MyClass&&) noexcept = default;           // ✅ vector will MOVE
    MyClass& operator=(MyClass&&) noexcept = default; // ✅
};

// noexcept specifier can be conditional:
template <typename T>
void moveIfNoexcept(T& a, T& b) noexcept(std::is_nothrow_move_constructible_v<T>) {
    if constexpr (std::is_nothrow_move_constructible_v<T>)
        a = std::move(b);
    else
        a = b;
}

// Check at compile time whether an expression is noexcept:
static_assert(noexcept(std::swap(std::declval<int&>(), std::declval<int&>())));
```

### Error Handling Without Exceptions — std::error_code

```cpp
#include <system_error>

// std::error_code — used by filesystem, networking, system calls
// zero = success; nonzero = failure with specific code and category

// Use for system/IO errors where exceptions are too heavy:
std::error_code ec;
std::filesystem::create_directory("newdir", ec);
if (ec) {
    std::cerr << "Error: " << ec.message() << " (" << ec.value() << ")\n";
    // e.g., "Error: File exists (17)"
}

// Defining custom error categories:
enum class AppError {
    NetworkTimeout = 1,
    DatabaseUnavailable,
    InvalidInput,
    AuthenticationFailed
};

class AppErrorCategory : public std::error_category {
public:
    const char* name() const noexcept override { return "app"; }
    std::string message(int ev) const override {
        switch (static_cast<AppError>(ev)) {
            case AppError::NetworkTimeout:       return "network timeout";
            case AppError::DatabaseUnavailable:  return "database unavailable";
            case AppError::InvalidInput:         return "invalid input";
            case AppError::AuthenticationFailed: return "authentication failed";
            default:                             return "unknown app error";
        }
    }
    static const AppErrorCategory& instance() {
        static AppErrorCategory inst;
        return inst;
    }
};

std::error_code make_error_code(AppError e) {
    return {static_cast<int>(e), AppErrorCategory::instance()};
}
// Make AppError usable with std::error_code directly:
namespace std {
    template <>
    struct is_error_code_enum<AppError> : true_type {};
}

// Now use it:
std::error_code fetchUser(int id, User& out) {
    if (id <= 0) return AppError::InvalidInput;
    // ... network call ...
    if (timeout) return AppError::NetworkTimeout;
    return {};   // success: default-constructed error_code = no error
}

User user;
if (auto err = fetchUser(42, user); err) {
    std::cerr << "fetchUser failed: " << err.message() << "\n";
}
```

---

## Chapter 30 (continued): Performance — Compiler Optimizations

### SIMD and Vectorization

```cpp
// SIMD: Single Instruction, Multiple Data — process multiple values simultaneously
// Modern CPUs: SSE2 (4 floats at once), AVX (8 floats), AVX-512 (16 floats)

// Auto-vectorization: compiler generates SIMD automatically for simple loops
void addArrays(float* a, const float* b, const float* c, int n) {
    for (int i = 0; i < n; ++i) {
        a[i] = b[i] + c[i];    // compiler vectorizes: processes 8 floats per iteration with AVX
    }
}

// Help the compiler vectorize:
// 1. Use __restrict__ / restrict — pointers don't alias
void addNoAlias(float* __restrict__ a,
                const float* __restrict__ b,
                const float* __restrict__ c, int n) {
    for (int i = 0; i < n; ++i) {
        a[i] = b[i] + c[i];  // now compiler knows b,c,a don't overlap → vectorize
    }
}

// 2. Align data for SIMD
alignas(32) float a[1024];   // 32-byte alignment for AVX
alignas(32) float b[1024];

// 3. Use SoA instead of AoS (as discussed in performance chapter)

// 4. Prefer standard algorithms (often vectorized by standard library)
std::transform(b, b+n, c, a, std::plus<float>{});  // might use SIMD internally

// 5. Compile with appropriate flags:
// g++ -O3 -march=native -ffast-math main.cpp
// -ffast-math: allows reordering floating-point (less precise but much faster)

// Explicit SIMD with intrinsics (low-level, non-portable):
#include <immintrin.h>  // Intel intrinsics
void addAVX(float* a, const float* b, const float* c, int n) {
    int i = 0;
    for (; i <= n - 8; i += 8) {
        __m256 vb = _mm256_loadu_ps(&b[i]);   // load 8 floats
        __m256 vc = _mm256_loadu_ps(&c[i]);
        __m256 va = _mm256_add_ps(vb, vc);    // add 8 floats in one instruction
        _mm256_storeu_ps(&a[i], va);           // store 8 floats
    }
    for (; i < n; ++i) a[i] = b[i] + c[i];  // handle remainder
}
```

### Memory Allocation Performance

```cpp
// std::allocator — default; uses malloc/free; fine for most use
// Custom allocators: arena (bump), pool, stack — dramatically faster for specific patterns

// Stack allocator (bump allocator) — O(1) allocation, no deallocation overhead
class StackAllocator {
    char* buffer_;
    char* current_;
    size_t capacity_;
public:
    explicit StackAllocator(size_t capacity)
        : buffer_{new char[capacity]}, current_{buffer_}, capacity_{capacity} {}
    ~StackAllocator() { delete[] buffer_; }

    void* allocate(size_t size, size_t align = alignof(std::max_align_t)) {
        // Align current pointer
        auto aligned = reinterpret_cast<char*>(
            (reinterpret_cast<uintptr_t>(current_) + align - 1) & ~(align - 1)
        );
        if (aligned + size > buffer_ + capacity_) throw std::bad_alloc{};
        current_ = aligned + size;
        return aligned;
    }

    void reset() { current_ = buffer_; }  // free ALL at once — O(1)!
};

// PMR (Polymorphic Memory Resources) — C++17 standard way to use custom allocators
#include <memory_resource>

char buffer[64 * 1024];  // 64 KB stack buffer
std::pmr::monotonic_buffer_resource pool{buffer, sizeof(buffer)};
// monotonic: only allocates, never frees individually (O(1) alloc, O(1) bulk free)

std::pmr::vector<std::pmr::string> vec{&pool};  // vector and strings use pool
for (int i = 0; i < 100; ++i) {
    vec.emplace_back(std::to_string(i));  // no heap allocation! Uses stack buffer
}
// When pool goes out of scope: all memory freed at once
```

---

## Appendix: C++ vs Java — Key Differences

```
Feature              Java                          C++
───────────────────────────────────────────────────────────────────────────
Memory management    GC (automatic)                Manual + RAII + smart ptrs
Object model         Everything in heap             Stack or heap, your choice
Primitives           int, double, etc. (value)      Same, but also objects
Strings              java.lang.String (heap)        std::string (can be stack)
Null safety          NullPointerException at RT     Compile-time (references can't be null)
Generics             Type erasure (runtime)         Templates (compile-time, monomorphized)
Inheritance          Single class, multiple interface    Single class (multiple via RAII/composition)
Interfaces           Explicit implements            Implicit (satisfy at compile-time)
Exception handling   Checked + unchecked            All unchecked (no checked exceptions)
Concurrency          synchronized, volatile, java.util.concurrent  std::thread, std::mutex, std::atomic
Operator overloading No (except +/String)           Yes
Preprocessor         No                             Yes (#define, #include, etc.)
Build                JVM bytecode (portable)        Native code (platform-specific)
Performance          JIT-compiled; GC pauses        AOT; deterministic; no GC pauses
Zero-cost abstracts  No (virtual always costs)      Yes (templates, inline, constexpr)
Compile time comp.   Annotation processors          constexpr, templates, concepts
RAII                 try-with-resources (limited)   Destructors called automatically
Copy vs reference    Objects: reference; primitives: value    Configurable: value, ref, const ref, move
```
