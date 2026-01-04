# Design Patterns Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What are Design Patterns?

**Answer:**
Design patterns are reusable solutions to common problems in software design. They provide templates for solving recurring design problems.

**Categories:**
- **Creational**: Object creation patterns
- **Structural**: Composition of classes/objects
- **Behavioral**: Communication between objects

### 2. Explain Singleton Pattern.

**Answer:**
Ensures a class has only one instance and provides global access.

**Java:**
```java
public class Singleton {
    private static Singleton instance;
    
    private Singleton() {}
    
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
    public void doSomething() {}
}
```

**JavaScript:**
```javascript
const Singleton = (function() {
    let instance;
    
    function createInstance() {
        return {
            data: "Singleton data"
        };
    }
    
    return {
        getInstance: function() {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();
```

### 3. Explain Factory Pattern.

**Answer:**
Creates objects without specifying exact class.

**Java:**
```java
interface Animal {
    void makeSound();
}

class Dog implements Animal {
    public void makeSound() {
        System.out.println("Woof");
    }
}

class Cat implements Animal {
    public void makeSound() {
        System.out.println("Meow");
    }
}

class AnimalFactory {
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

**JavaScript:**
```javascript
class Dog {
    makeSound() {
        console.log("Woof");
    }
}

class Cat {
    makeSound() {
        console.log("Meow");
    }
}

class AnimalFactory {
    static createAnimal(type) {
        if (type === "dog") return new Dog();
        if (type === "cat") return new Cat();
        throw new Error("Unknown animal type");
    }
}
```

### 4. Explain Observer Pattern.

**Answer:**
One-to-many dependency between objects. When one changes, all dependents are notified.

**Java:**
```java
import java.util.*;

interface Observer {
    void update(String message);
}

class Subject {
    private List<Observer> observers = new ArrayList<>();
    
    public void addObserver(Observer observer) {
        observers.add(observer);
    }
    
    public void notifyObservers(String message) {
        for (Observer observer : observers) {
            observer.update(message);
        }
    }
}
```

**JavaScript:**
```javascript
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }
    
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => callback(data));
        }
    }
    
    off(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    }
}
```

### 5. Explain Strategy Pattern.

**Answer:**
Defines family of algorithms, encapsulates each, makes them interchangeable.

**Java:**
```java
interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using credit card");
    }
}

class PayPalPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using PayPal");
    }
}

class ShoppingCart {
    private PaymentStrategy paymentStrategy;
    
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }
    
    public void checkout(double amount) {
        paymentStrategy.pay(amount);
    }
}
```

**JavaScript:**
```javascript
class CreditCardPayment {
    pay(amount) {
        console.log(`Paid ${amount} using credit card`);
    }
}

class PayPalPayment {
    pay(amount) {
        console.log(`Paid ${amount} using PayPal`);
    }
}

class ShoppingCart {
    constructor() {
        this.paymentStrategy = null;
    }
    
    setPaymentStrategy(strategy) {
        this.paymentStrategy = strategy;
    }
    
    checkout(amount) {
        this.paymentStrategy.pay(amount);
    }
}
```

---

## Intermediate Level

### 6. Explain Builder Pattern.

**Answer:**
Constructs complex objects step by step.

**Java:**
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

**JavaScript:**
```javascript
class PersonBuilder {
    constructor() {
        this.name = null;
        this.age = null;
        this.email = null;
    }
    
    setName(name) {
        this.name = name;
        return this;
    }
    
    setAge(age) {
        this.age = age;
        return this;
    }
    
    setEmail(email) {
        this.email = email;
        return this;
    }
    
    build() {
        return new Person(this.name, this.age, this.email);
    }
}

// Usage
const person = new PersonBuilder()
    .setName("John")
    .setAge(30)
    .setEmail("john@example.com")
    .build();
```

### 7. Explain Adapter Pattern.

**Answer:**
Allows incompatible interfaces to work together.

**Java:**
```java
interface MediaPlayer {
    void play(String audioType, String fileName);
}

interface AdvancedMediaPlayer {
    void playVlc(String fileName);
    void playMp4(String fileName);
}

class VlcPlayer implements AdvancedMediaPlayer {
    public void playVlc(String fileName) {
        System.out.println("Playing vlc file: " + fileName);
    }
    public void playMp4(String fileName) {}
}

class MediaAdapter implements MediaPlayer {
    AdvancedMediaPlayer advancedPlayer;
    
    public MediaAdapter(String audioType) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedPlayer = new VlcPlayer();
        }
    }
    
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedPlayer.playVlc(fileName);
        }
    }
}
```

### 8. Explain Decorator Pattern.

**Answer:**
Adds behavior to objects dynamically.

**Java:**
```java
interface Coffee {
    double cost();
    String description();
}

class SimpleCoffee implements Coffee {
    public double cost() { return 2.0; }
    public String description() { return "Simple coffee"; }
}

abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
    
    public double cost() {
        return coffee.cost();
    }
    
    public String description() {
        return coffee.description();
    }
}

class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    public double cost() {
        return coffee.cost() + 0.5;
    }
    
    public String description() {
        return coffee.description() + ", milk";
    }
}
```

### 9. Explain Facade Pattern.

**Answer:**
Provides simplified interface to complex subsystem.

**Java:**
```java
class CPU {
    public void freeze() {}
    public void jump(long position) {}
    public void execute() {}
}

class Memory {
    public void load(long position, byte[] data) {}
}

class HardDrive {
    public byte[] read(long lba, int size) { return null; }
}

class ComputerFacade {
    private CPU cpu;
    private Memory memory;
    private HardDrive hardDrive;
    
    public ComputerFacade() {
        this.cpu = new CPU();
        this.memory = new Memory();
        this.hardDrive = new HardDrive();
    }
    
    public void startComputer() {
        cpu.freeze();
        memory.load(0, hardDrive.read(0, 1024));
        cpu.jump(0);
        cpu.execute();
    }
}
```

### 10. Explain Command Pattern.

**Answer:**
Encapsulates request as object.

**Java:**
```java
interface Command {
    void execute();
}

class Light {
    public void on() {
        System.out.println("Light is on");
    }
    public void off() {
        System.out.println("Light is off");
    }
}

class LightOnCommand implements Command {
    private Light light;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    public void execute() {
        light.on();
    }
}

class RemoteControl {
    private Command command;
    
    public void setCommand(Command command) {
        this.command = command;
    }
    
    public void pressButton() {
        command.execute();
    }
}
```

---

## Advanced Level

### 11. Explain MVC Pattern.

**Answer:**
Separates application into Model, View, Controller.

**Structure:**
- **Model**: Data and business logic
- **View**: User interface
- **Controller**: Handles input, coordinates Model and View

**Example:**
```javascript
// Model
class UserModel {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        this.users.push(user);
    }
    
    getUsers() {
        return this.users;
    }
}

// View
class UserView {
    displayUsers(users) {
        users.forEach(user => {
            console.log(`${user.name} - ${user.email}`);
        });
    }
}

// Controller
class UserController {
    constructor(model, view) {
        this.model = model;
        this.view = view;
    }
    
    addUser(name, email) {
        this.model.addUser({ name, email });
        this.updateView();
    }
    
    updateView() {
        const users = this.model.getUsers();
        this.view.displayUsers(users);
    }
}
```

### 12. Explain Repository Pattern.

**Answer:**
Abstraction layer between business logic and data access.

**Java:**
```java
interface Repository<T> {
    T findById(Long id);
    List<T> findAll();
    void save(T entity);
    void delete(T entity);
}

class UserRepository implements Repository<User> {
    // Implementation
}

class UserService {
    private UserRepository repository;
    
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
    
    public User getUser(Long id) {
        return repository.findById(id);
    }
}
```

### 13. Explain Dependency Injection.

**Answer:**
Objects receive dependencies from external source rather than creating them.

**Java:**
```java
// Without DI
class UserService {
    private UserRepository repository = new UserRepository();
}

// With DI
class UserService {
    private UserRepository repository;
    
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// Usage
UserRepository repo = new UserRepository();
UserService service = new UserService(repo);
```

### 14. Explain Proxy Pattern.

**Answer:**
Provides placeholder for another object to control access.

**Java:**
```java
interface Image {
    void display();
}

class RealImage implements Image {
    private String filename;
    
    public RealImage(String filename) {
        this.filename = filename;
        loadFromDisk();
    }
    
    private void loadFromDisk() {
        System.out.println("Loading " + filename);
    }
    
    public void display() {
        System.out.println("Displaying " + filename);
    }
}

class ProxyImage implements Image {
    private RealImage realImage;
    private String filename;
    
    public ProxyImage(String filename) {
        this.filename = filename;
    }
    
    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename);
        }
        realImage.display();
    }
}
```

### 15. Explain Chain of Responsibility.

**Answer:**
Passes request along chain of handlers.

**Java:**
```java
abstract class Handler {
    protected Handler next;
    
    public void setNext(Handler next) {
        this.next = next;
    }
    
    public abstract void handle(Request request);
}

class AuthenticationHandler extends Handler {
    public void handle(Request request) {
        if (request.isAuthenticated()) {
            if (next != null) {
                next.handle(request);
            }
        } else {
            throw new RuntimeException("Not authenticated");
        }
    }
}

class AuthorizationHandler extends Handler {
    public void handle(Request request) {
        if (request.hasPermission()) {
            if (next != null) {
                next.handle(request);
            }
        } else {
            throw new RuntimeException("Not authorized");
        }
    }
}
```

---

This covers design patterns interview questions from beginner to advanced level with implementations in Java and JavaScript.

