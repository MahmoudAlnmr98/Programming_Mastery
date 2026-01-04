# C++ Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. Explain the difference between C and C++.

**Answer:**
- **C**: Procedural language, no OOP, manual memory management
- **C++**: Multi-paradigm (OOP, procedural, generic), classes, STL, RAII

### 2. Explain pointers and references.

**Answer:**
**Pointers:**
```cpp
int x = 10;
int* ptr = &x;  // Pointer to x
*ptr = 20;      // Dereference and modify
```

**References:**
```cpp
int x = 10;
int& ref = x;   // Reference to x
ref = 20;       // Modify x directly
```

**Differences:**
- Pointer can be NULL, reference cannot
- Pointer can be reassigned, reference cannot
- Pointer needs dereferencing, reference does not

### 3. Explain new vs malloc.

**Answer:**
- **new**: C++ operator, calls constructor, returns typed pointer, throws exception on failure
- **malloc**: C function, doesn't call constructor, returns void*, returns NULL on failure

```cpp
// new
int* ptr = new int(10);
delete ptr;

// malloc
int* ptr = (int*)malloc(sizeof(int));
free(ptr);
```

### 4. Explain constructors and destructors.

**Answer:**
```cpp
class MyClass {
private:
    int* data;
    
public:
    // Default constructor
    MyClass() : data(nullptr) {}
    
    // Parameterized constructor
    MyClass(int value) : data(new int(value)) {}
    
    // Copy constructor
    MyClass(const MyClass& other) : data(new int(*other.data)) {}
    
    // Destructor
    ~MyClass() {
        delete data;
    }
};
```

### 5. Explain function overloading.

**Answer:**
Multiple functions with same name but different parameters.

```cpp
int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

int add(int a, int b, int c) {
    return a + b + c;
}
```

### 6. Explain operator overloading.

**Answer:**
Define behavior of operators for custom types.

```cpp
class Vector {
private:
    int x, y;
    
public:
    Vector(int x, int y) : x(x), y(y) {}
    
    Vector operator+(const Vector& other) const {
        return Vector(x + other.x, y + other.y);
    }
    
    bool operator==(const Vector& other) const {
        return x == other.x && y == other.y;
    }
};
```

### 7. Explain inheritance.

**Answer:**
```cpp
class Animal {
protected:
    string name;
    
public:
    Animal(string name) : name(name) {}
    virtual void makeSound() = 0;  // Pure virtual
};

class Dog : public Animal {
public:
    Dog(string name) : Animal(name) {}
    
    void makeSound() override {
        cout << "Woof" << endl;
    }
};
```

### 8. Explain virtual functions and polymorphism.

**Answer:**
Virtual functions enable runtime polymorphism.

```cpp
class Base {
public:
    virtual void display() {
        cout << "Base" << endl;
    }
};

class Derived : public Base {
public:
    void display() override {
        cout << "Derived" << endl;
    }
};

Base* ptr = new Derived();
ptr->display();  // Calls Derived::display()
```

---

## Intermediate Level

### 9. Explain smart pointers.

**Answer:**
Smart pointers manage memory automatically.

**unique_ptr:**
```cpp
unique_ptr<int> ptr = make_unique<int>(10);
// Automatically deleted when out of scope
```

**shared_ptr:**
```cpp
shared_ptr<int> ptr1 = make_shared<int>(10);
shared_ptr<int> ptr2 = ptr1;  // Shared ownership
// Deleted when last shared_ptr destroyed
```

**weak_ptr:**
```cpp
weak_ptr<int> weak = shared_ptr<int>(new int(10));
// Doesn't increase reference count
```

### 10. Explain STL containers.

**Answer:**
**Sequence Containers:**
- `vector`: Dynamic array
- `list`: Doubly linked list
- `deque`: Double-ended queue

**Associative Containers:**
- `set`: Sorted unique elements
- `map`: Key-value pairs
- `unordered_set`: Hash set
- `unordered_map`: Hash map

### 11. Explain templates.

**Answer:**
Templates enable generic programming.

```cpp
template<typename T>
T maximum(T a, T b) {
    return a > b ? a : b;
}

template<class T>
class Stack {
private:
    vector<T> elements;
    
public:
    void push(T element) {
        elements.push_back(element);
    }
    
    T pop() {
        T element = elements.back();
        elements.pop_back();
        return element;
    }
};
```

### 12. Explain exception handling.

**Answer:**
```cpp
try {
    if (value < 0) {
        throw invalid_argument("Value must be positive");
    }
} catch (const invalid_argument& e) {
    cout << "Error: " << e.what() << endl;
} catch (...) {
    cout << "Unknown error" << endl;
}
```

### 13. Explain RAII (Resource Acquisition Is Initialization).

**Answer:**
RAII ties resource lifetime to object lifetime.

```cpp
class FileHandler {
private:
    FILE* file;
    
public:
    FileHandler(const char* filename) {
        file = fopen(filename, "r");
        if (!file) throw runtime_error("Cannot open file");
    }
    
    ~FileHandler() {
        if (file) fclose(file);
    }
    
    // Delete copy constructor/assignment
    FileHandler(const FileHandler&) = delete;
    FileHandler& operator=(const FileHandler&) = delete;
};
```

### 14. Explain move semantics.

**Answer:**
Move semantics avoid unnecessary copies.

```cpp
class MyClass {
private:
    int* data;
    
public:
    // Move constructor
    MyClass(MyClass&& other) noexcept : data(other.data) {
        other.data = nullptr;
    }
    
    // Move assignment
    MyClass& operator=(MyClass&& other) noexcept {
        if (this != &other) {
            delete data;
            data = other.data;
            other.data = nullptr;
        }
        return *this;
    }
};
```

---

## Advanced Level

### 15. Explain const correctness.

**Answer:**
```cpp
class MyClass {
private:
    int value;
    mutable int cache;
    
public:
    // Const member function
    int getValue() const {
        return value;  // Cannot modify non-mutable members
    }
    
    // Mutable member can be modified in const function
    void updateCache() const {
        cache = 10;  // OK - cache is mutable
    }
};

const MyClass obj;
obj.getValue();  // OK - const function
```

### 16. Explain lambda expressions.

**Answer:**
```cpp
// Basic lambda
auto add = [](int a, int b) { return a + b; };

// With capture
int x = 10;
auto lambda = [x](int y) { return x + y; };

// Capture by reference
auto lambda2 = [&x](int y) { x += y; };

// Generic lambda (C++14)
auto generic = [](auto a, auto b) { return a + b; };
```

### 17. Explain multithreading in C++.

**Answer:**
```cpp
#include <thread>
#include <mutex>

mutex mtx;

void function(int id) {
    lock_guard<mutex> lock(mtx);
    cout << "Thread " << id << endl;
}

int main() {
    thread t1(function, 1);
    thread t2(function, 2);
    
    t1.join();
    t2.join();
    return 0;
}
```

### 18. Explain copy elision and RVO (Return Value Optimization).

**Answer:**
Copy elision allows compiler to omit unnecessary copies.

**RVO (Return Value Optimization):**
```cpp
// Compiler may elide copy
MyClass create() {
    return MyClass();  // No copy, constructed directly
}

MyClass obj = create();  // Direct construction
```

**Mandatory Copy Elision (C++17):**
- Temporary objects
- Return statements
- Initialization from prvalues

### 19. Explain perfect forwarding.

**Answer:**
Perfect forwarding preserves value category (lvalue/rvalue).

```cpp
template<typename T>
void forwarder(T&& arg) {
    func(std::forward<T>(arg));  // Preserves lvalue/rvalue
}

// Usage
int x = 10;
forwarder(x);        // Passes as lvalue
forwarder(10);       // Passes as rvalue
forwarder(move(x));  // Passes as rvalue
```

### 20. Explain SFINAE (Substitution Failure Is Not An Error).

**Answer:**
SFINAE allows template substitution failures to be ignored.

```cpp
#include <type_traits>

// Enable if integer
template<typename T>
typename std::enable_if<std::is_integral<T>::value, void>::type
func(T value) {
    cout << "Integer: " << value << endl;
}

// Enable if floating point
template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, void>::type
func(T value) {
    cout << "Float: " << value << endl;
}
```

### 21. Explain CRTP (Curiously Recurring Template Pattern).

**Answer:**
CRTP is when derived class inherits from template base using itself.

```cpp
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }
};

class Derived : public Base<Derived> {
public:
    void implementation() {
        cout << "Derived implementation" << endl;
    }
};
```

**Benefits:**
- Static polymorphism
- No virtual function overhead
- Compile-time dispatch

### 22. Explain memory alignment and padding.

**Answer:**
Data structures are aligned for performance.

```cpp
struct Example {
    char a;      // 1 byte
    // 3 bytes padding
    int b;       // 4 bytes (aligned to 4)
    double c;    // 8 bytes (aligned to 8)
    // Total: 16 bytes
};

// Packed (no padding)
struct __attribute__((packed)) Packed {
    char a;
    int b;
    double c;
    // Total: 13 bytes
};
```

### 23. Explain std::move and std::forward.

**Answer:**
**std::move:**
```cpp
// Converts to rvalue reference
string str = "hello";
string moved = std::move(str);  // str is now empty
```

**std::forward:**
```cpp
// Preserves value category
template<typename T>
void wrapper(T&& arg) {
    func(std::forward<T>(arg));  // Perfect forwarding
}
```

### 24. Explain variadic templates.

**Answer:**
Templates that accept variable number of arguments.

```cpp
// Base case
void print() {}

// Recursive case
template<typename T, typename... Args>
void print(T first, Args... args) {
    cout << first << " ";
    print(args...);  // Recursive call
}

// Usage
print(1, 2.5, "hello", 'c');  // 1 2.5 hello c
```

### 25. Explain RAII and exception safety.

**Answer:**
RAII ensures resources are released even if exceptions occur.

**Exception Safety Levels:**
1. **No-throw guarantee**: Never throws
2. **Strong guarantee**: All-or-nothing (rollback on exception)
3. **Basic guarantee**: Valid state maintained
4. **No guarantee**: May leave invalid state

```cpp
class FileHandler {
    FILE* file;
public:
    FileHandler(const char* name) : file(fopen(name, "r")) {
        if (!file) throw runtime_error("Cannot open");
    }
    
    ~FileHandler() {
        if (file) fclose(file);  // Always called
    }
    
    // Copy disabled
    FileHandler(const FileHandler&) = delete;
    FileHandler& operator=(const FileHandler&) = delete;
};
```

### 26. Explain C++ Smart Pointers in Detail.

**Answer:**
**unique_ptr:**
```cpp
#include <memory>

std::unique_ptr<int> ptr = std::make_unique<int>(42);
// Automatically deleted when out of scope
// Cannot be copied, only moved
std::unique_ptr<int> ptr2 = std::move(ptr);
```

**shared_ptr:**
```cpp
std::shared_ptr<int> ptr1 = std::make_shared<int>(42);
std::shared_ptr<int> ptr2 = ptr1; // Reference count: 2
// Deleted when last shared_ptr is destroyed
```

**weak_ptr:**
```cpp
std::shared_ptr<int> shared = std::make_shared<int>(42);
std::weak_ptr<int> weak = shared;

if (auto locked = weak.lock()) {
    // Use locked shared_ptr
}
```

### 27. Explain C++ Move Semantics.

**Answer:**
Move semantics transfer ownership without copying.

**Move Constructor:**
```cpp
class MyClass {
public:
    MyClass(MyClass&& other) noexcept
        : data(std::move(other.data)) {
        other.data = nullptr;
    }
    
    MyClass& operator=(MyClass&& other) noexcept {
        if (this != &other) {
            delete data;
            data = std::move(other.data);
            other.data = nullptr;
        }
        return *this;
    }
};
```

**std::move:**
```cpp
std::vector<int> vec1 = {1, 2, 3};
std::vector<int> vec2 = std::move(vec1);
// vec1 is now empty, vec2 has the data
```

### 28. Explain C++ Lambda Expressions.

**Answer:**
Lambdas create anonymous functions.

**Basic:**
```cpp
auto lambda = [](int x, int y) { return x + y; };
int result = lambda(3, 4); // 7
```

**Capture:**
```cpp
int a = 10;
auto lambda = [a](int x) { return a + x; }; // Capture by value
auto lambda2 = [&a](int x) { return a + x; }; // Capture by reference
auto lambda3 = [=](int x) { return a + x; }; // Capture all by value
auto lambda4 = [&](int x) { return a + x; }; // Capture all by reference
```

**Mutable:**
```cpp
int count = 0;
auto lambda = [count]() mutable { count++; };
```

### 29. Explain C++ Templates Advanced.

**Answer:**
**Variadic Templates:**
```cpp
template<typename... Args>
void print(Args... args) {
    ((std::cout << args << " "), ...);
}

print(1, 2.5, "hello"); // 1 2.5 hello
```

**Template Specialization:**
```cpp
template<typename T>
class MyClass {
    // Generic implementation
};

template<>
class MyClass<int> {
    // Specialized for int
};
```

**SFINAE:**
```cpp
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
foo(T t) {
    return t * 2;
}
```

### 30. Explain C++ Concurrency.

**Answer:**
**Threads:**
```cpp
#include <thread>

void function() {
    std::cout << "Thread running\n";
}

std::thread t(function);
t.join();
```

**Mutex:**
```cpp
#include <mutex>

std::mutex mtx;

void safeFunction() {
    std::lock_guard<std::mutex> lock(mtx);
    // Critical section
}
```

**Condition Variable:**
```cpp
#include <condition_variable>

std::condition_variable cv;
std::mutex mtx;
bool ready = false;

// Waiter
std::unique_lock<std::mutex> lock(mtx);
cv.wait(lock, []{ return ready; });

// Notifier
{
    std::lock_guard<std::mutex> lock(mtx);
    ready = true;
}
cv.notify_one();
```

### 31. Explain C++ RAII (Resource Acquisition Is Initialization).

**Answer:**
RAII manages resources through object lifetime.

**Example:**
```cpp
class File {
    FILE* file;
public:
    File(const char* filename) : file(fopen(filename, "r")) {
        if (!file) throw std::runtime_error("Cannot open file");
    }
    
    ~File() {
        if (file) fclose(file);
    }
    
    // Delete copy constructor and assignment
    File(const File&) = delete;
    File& operator=(const File&) = delete;
    
    // Allow move
    File(File&& other) : file(other.file) {
        other.file = nullptr;
    }
};
```

**Benefits:**
- Automatic resource management
- Exception safety
- No memory leaks

### 32. Explain C++ Exception Handling.

**Answer:**
**Try-Catch:**
```cpp
try {
    riskyFunction();
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
} catch (...) {
    std::cerr << "Unknown error" << std::endl;
}
```

**Custom Exception:**
```cpp
class MyException : public std::exception {
    const char* message;
public:
    MyException(const char* msg) : message(msg) {}
    const char* what() const noexcept override {
        return message;
    }
};
```

**Exception Safety:**
- Basic guarantee: No leaks
- Strong guarantee: All-or-nothing
- No-throw guarantee: Never throws

### 33. Explain C++ STL Algorithms.

**Answer:**
**Common Algorithms:**
```cpp
#include <algorithm>
#include <vector>

std::vector<int> vec = {3, 1, 4, 1, 5};

// Sort
std::sort(vec.begin(), vec.end());

// Find
auto it = std::find(vec.begin(), vec.end(), 4);

// Count
int count = std::count(vec.begin(), vec.end(), 1);

// Transform
std::transform(vec.begin(), vec.end(), vec.begin(),
    [](int x) { return x * 2; });

// Accumulate
#include <numeric>
int sum = std::accumulate(vec.begin(), vec.end(), 0);
```

### 34. Explain C++ Type Traits.

**Answer:**
Type traits provide type information.

**Common Traits:**
```cpp
#include <type_traits>

std::is_integral<int>::value; // true
std::is_pointer<int*>::value; // true
std::is_reference<int&>::value; // true

// Remove qualifiers
std::remove_const<const int>::type; // int
std::remove_reference<int&>::type; // int
std::remove_pointer<int*>::type; // int
```

**Enable If:**
```cpp
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
foo(T t) {
    return t * 2;
}
```

### 35. Explain C++ Perfect Forwarding.

**Answer:**
Perfect forwarding preserves value category.

**Example:**
```cpp
template<typename T>
void wrapper(T&& arg) {
    func(std::forward<T>(arg));
}

void func(int& x) { /* lvalue */ }
void func(int&& x) { /* rvalue */ }

int x = 42;
wrapper(x); // Calls func(int&)
wrapper(42); // Calls func(int&&)
```

**std::forward:**
```cpp
template<typename T>
T&& forward(typename std::remove_reference<T>::type& arg) {
    return static_cast<T&&>(arg);
}
```

---

This covers C++ interview questions from beginner to advanced level with detailed explanations and code examples.

