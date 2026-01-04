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

---

This covers C++ interview questions from beginner to advanced level with detailed explanations and code examples.

