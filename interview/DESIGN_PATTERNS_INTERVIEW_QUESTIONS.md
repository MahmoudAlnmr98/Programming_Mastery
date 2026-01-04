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

### 16. Explain Template Method Pattern.

**Answer:**
Defines algorithm skeleton, subclasses implement steps.

**Java:**
```java
abstract class DataProcessor {
    // Template method
    public final void process() {
        readData();
        processData();
        saveData();
    }
    
    abstract void readData();
    abstract void processData();
    abstract void saveData();
}

class CSVProcessor extends DataProcessor {
    void readData() {
        System.out.println("Reading CSV");
    }
    void processData() {
        System.out.println("Processing CSV");
    }
    void saveData() {
        System.out.println("Saving CSV");
    }
}
```

### 17. Explain State Pattern.

**Answer:**
Object behavior changes based on internal state.

**Java:**
```java
interface State {
    void handle(Context context);
}

class ConcreteStateA implements State {
    public void handle(Context context) {
        System.out.println("State A");
        context.setState(new ConcreteStateB());
    }
}

class ConcreteStateB implements State {
    public void handle(Context context) {
        System.out.println("State B");
        context.setState(new ConcreteStateA());
    }
}

class Context {
    private State state;
    
    public void setState(State state) {
        this.state = state;
    }
    
    public void request() {
        state.handle(this);
    }
}
```

### 18. Explain Visitor Pattern.

**Answer:**
Separates algorithm from object structure.

**Java:**
```java
interface Visitor {
    void visit(ElementA element);
    void visit(ElementB element);
}

interface Element {
    void accept(Visitor visitor);
}

class ElementA implements Element {
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

class ConcreteVisitor implements Visitor {
    public void visit(ElementA element) {
        System.out.println("Visiting ElementA");
    }
    public void visit(ElementB element) {
        System.out.println("Visiting ElementB");
    }
}
```

### 19. Explain Mediator Pattern.

**Answer:**
Reduces coupling by having objects communicate through mediator.

**Java:**
```java
interface Mediator {
    void send(String message, Colleague colleague);
}

class ConcreteMediator implements Mediator {
    private Colleague colleague1;
    private Colleague colleague2;
    
    public void setColleague1(Colleague c) {
        this.colleague1 = c;
    }
    
    public void send(String message, Colleague colleague) {
        if (colleague == colleague1) {
            colleague2.receive(message);
        } else {
            colleague1.receive(message);
        }
    }
}

abstract class Colleague {
    protected Mediator mediator;
    
    public Colleague(Mediator mediator) {
        this.mediator = mediator;
    }
    
    public abstract void send(String message);
    public abstract void receive(String message);
}
```

### 20. Explain Memento Pattern.

**Answer:**
Captures and restores object state.

**Java:**
```java
class Memento {
    private String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
}

class Originator {
    private String state;
    
    public void setState(String state) {
        this.state = state;
    }
    
    public Memento save() {
        return new Memento(state);
    }
    
    public void restore(Memento memento) {
        state = memento.getState();
    }
}

class Caretaker {
    private List<Memento> mementos = new ArrayList<>();
    
    public void addMemento(Memento memento) {
        mementos.add(memento);
    }
    
    public Memento getMemento(int index) {
        return mementos.get(index);
    }
}
```

### 21. Explain Flyweight Pattern.

**Answer:**
Shares common state to reduce memory usage.

**Java:**
```java
class Flyweight {
    private String intrinsicState;
    
    public Flyweight(String intrinsicState) {
        this.intrinsicState = intrinsicState;
    }
    
    public void operation(String extrinsicState) {
        System.out.println("Intrinsic: " + intrinsicState);
        System.out.println("Extrinsic: " + extrinsicState);
    }
}

class FlyweightFactory {
    private Map<String, Flyweight> flyweights = new HashMap<>();
    
    public Flyweight getFlyweight(String key) {
        if (!flyweights.containsKey(key)) {
            flyweights.put(key, new Flyweight(key));
        }
        return flyweights.get(key);
    }
}
```

### 22. Explain Bridge Pattern.

**Answer:**
Separates abstraction from implementation.

**Java:**
```java
interface Implementor {
    void operationImpl();
}

class ConcreteImplementorA implements Implementor {
    public void operationImpl() {
        System.out.println("Implementation A");
    }
}

abstract class Abstraction {
    protected Implementor implementor;
    
    public Abstraction(Implementor implementor) {
        this.implementor = implementor;
    }
    
    public void operation() {
        implementor.operationImpl();
    }
}

class RefinedAbstraction extends Abstraction {
    public RefinedAbstraction(Implementor implementor) {
        super(implementor);
    }
    
    public void refinedOperation() {
        operation();
    }
}
```

### 23. Explain Composite Pattern.

**Answer:**
Composes objects into tree structures.

**Java:**
```java
interface Component {
    void operation();
    void add(Component component);
    void remove(Component component);
}

class Leaf implements Component {
    public void operation() {
        System.out.println("Leaf operation");
    }
    
    public void add(Component component) {
        throw new UnsupportedOperationException();
    }
    
    public void remove(Component component) {
        throw new UnsupportedOperationException();
    }
}

class Composite implements Component {
    private List<Component> children = new ArrayList<>();
    
    public void operation() {
        for (Component child : children) {
            child.operation();
        }
    }
    
    public void add(Component component) {
        children.add(component);
    }
    
    public void remove(Component component) {
        children.remove(component);
    }
}
```

### 24. Explain Iterator Pattern.

**Answer:**
Provides way to access elements sequentially.

**Java:**
```java
interface Iterator<T> {
    boolean hasNext();
    T next();
}

interface Aggregate<T> {
    Iterator<T> createIterator();
}

class ConcreteIterator<T> implements Iterator<T> {
    private List<T> items;
    private int position = 0;
    
    public ConcreteIterator(List<T> items) {
        this.items = items;
    }
    
    public boolean hasNext() {
        return position < items.size();
    }
    
    public T next() {
        return items.get(position++);
    }
}

class ConcreteAggregate<T> implements Aggregate<T> {
    private List<T> items = new ArrayList<>();
    
    public void add(T item) {
        items.add(item);
    }
    
    public Iterator<T> createIterator() {
        return new ConcreteIterator<>(items);
    }
}
```

### 25. Explain Observer Pattern (Detailed).

**Answer:**
One-to-many dependency between objects.

**Java (Push Model):**
```java
interface Observer {
    void update(String data);
}

class Subject {
    private List<Observer> observers = new ArrayList<>();
    private String state;
    
    public void attach(Observer observer) {
        observers.add(observer);
    }
    
    public void setState(String state) {
        this.state = state;
        notifyObservers();
    }
    
    private void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(state);
        }
    }
}
```

**Java (Pull Model):**
```java
interface Observer {
    void update(Subject subject);
}

class Subject {
    private List<Observer> observers = new ArrayList<>();
    private String state;
    
    public String getState() {
        return state;
    }
    
    public void setState(String state) {
        this.state = state;
        notifyObservers();
    }
    
    private void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(this);
        }
    }
}
```

### 26. Explain SOLID Principles.

**Answer:**
SOLID principles guide object-oriented design.

**S - Single Responsibility Principle:**
- Class should have one reason to change
- One responsibility per class

```java
// Bad
class User {
    void save() { }
    void sendEmail() { }
    void generateReport() { }
}

// Good
class User {
    void save() { }
}
class EmailService {
    void sendEmail() { }
}
class ReportGenerator {
    void generateReport() { }
}
```

**O - Open/Closed Principle:**
- Open for extension, closed for modification
- Use inheritance/abstraction

```java
interface PaymentMethod {
    void pay(double amount);
}

class CreditCardPayment implements PaymentMethod {
    public void pay(double amount) { }
}

class PayPalPayment implements PaymentMethod {
    public void pay(double amount) { }
}
```

**L - Liskov Substitution Principle:**
- Subtypes must be substitutable for base types
- Derived classes shouldn't break base class behavior

```java
class Bird {
    void fly() { }
}

// Violates LSP
class Penguin extends Bird {
    void fly() {
        throw new UnsupportedOperationException();
    }
}

// Better
interface Flyable {
    void fly();
}
class Bird implements Flyable {
    public void fly() { }
}
class Penguin extends Bird {
    // Doesn't implement Flyable
}
```

**I - Interface Segregation Principle:**
- Clients shouldn't depend on interfaces they don't use
- Prefer specific interfaces over general ones

```java
// Bad
interface Worker {
    void work();
    void eat();
    void sleep();
}

// Good
interface Workable {
    void work();
}
interface Eatable {
    void eat();
}
```

**D - Dependency Inversion Principle:**
- Depend on abstractions, not concretions
- High-level modules shouldn't depend on low-level modules

```java
// Bad
class UserService {
    private MySQLDatabase db = new MySQLDatabase();
}

// Good
class UserService {
    private Database db;
    public UserService(Database db) {
        this.db = db;
    }
}
```

### 27. Explain the Object Pool Pattern.

**Answer:**
Reuses expensive-to-create objects to improve performance.

**Java:**
```java
class ConnectionPool {
    private Queue<Connection> pool = new LinkedList<>();
    private int maxSize;
    
    public ConnectionPool(int maxSize) {
        this.maxSize = maxSize;
        initializePool();
    }
    
    private void initializePool() {
        for (int i = 0; i < maxSize; i++) {
            pool.offer(new Connection());
        }
    }
    
    public Connection acquire() {
        Connection conn = pool.poll();
        if (conn == null) {
            conn = new Connection(); // Create new if pool empty
        }
        return conn;
    }
    
    public void release(Connection conn) {
        conn.reset();
        if (pool.size() < maxSize) {
            pool.offer(conn);
        }
    }
}
```

**Use Cases:**
- Database connections
- Thread pools
- Network connections

### 28. Explain the Specification Pattern.

**Answer:**
Encapsulates business rules as reusable specifications.

**Java:**
```java
interface Specification<T> {
    boolean isSatisfiedBy(T item);
    Specification<T> and(Specification<T> other);
    Specification<T> or(Specification<T> other);
    Specification<T> not();
}

class PriceSpecification implements Specification<Product> {
    private double minPrice;
    
    public PriceSpecification(double minPrice) {
        this.minPrice = minPrice;
    }
    
    @Override
    public boolean isSatisfiedBy(Product product) {
        return product.getPrice() >= minPrice;
    }
    
    @Override
    public Specification<Product> and(Specification<Product> other) {
        return new AndSpecification<>(this, other);
    }
}

// Usage
Specification<Product> spec = new PriceSpecification(100)
    .and(new CategorySpecification("Electronics"));
List<Product> filtered = products.stream()
    .filter(spec::isSatisfiedBy)
    .collect(Collectors.toList());
```

### 29. Explain the Chain of Responsibility Pattern.

**Answer:**
Passes request along chain of handlers until one handles it.

**Java:**
```java
abstract class Handler {
    protected Handler next;
    
    public Handler setNext(Handler next) {
        this.next = next;
        return next;
    }
    
    public abstract void handle(Request request);
}

class AuthenticationHandler extends Handler {
    @Override
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
    @Override
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

// Usage
Handler chain = new AuthenticationHandler();
chain.setNext(new AuthorizationHandler());
chain.handle(request);
```

**Use Cases:**
- Middleware chains
- Event handling
- Request processing

### 30. Explain the Template Method Pattern.

**Answer:**
Defines algorithm skeleton, subclasses override steps.

**Java:**
```java
abstract class DataProcessor {
    // Template method
    public final void process() {
        readData();
        processData();
        saveData();
    }
    
    protected abstract void readData();
    protected abstract void processData();
    protected abstract void saveData();
}

class CSVProcessor extends DataProcessor {
    @Override
    protected void readData() {
        System.out.println("Reading CSV");
    }
    
    @Override
    protected void processData() {
        System.out.println("Processing CSV");
    }
    
    @Override
    protected void saveData() {
        System.out.println("Saving CSV");
    }
}
```

**Use Cases:**
- Framework design
- Algorithm variations
- Code reuse

### 31. Explain the Strategy Pattern vs State Pattern.

**Answer:**
**Strategy Pattern:** Different algorithms, same interface
```java
interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid with credit card");
    }
}

class PayPalPayment implements PaymentStrategy {
    public void pay(double amount) {
        System.out.println("Paid with PayPal");
    }
}
```

**State Pattern:** Behavior changes with internal state
```java
interface State {
    void handle(Context context);
}

class StateA implements State {
    public void handle(Context context) {
        System.out.println("State A");
        context.setState(new StateB());
    }
}

class StateB implements State {
    public void handle(Context context) {
        System.out.println("State B");
        context.setState(new StateA());
    }
}
```

**Differences:**
- Strategy: Algorithm selection (external)
- State: State-dependent behavior (internal)

### 32. Explain the Visitor Pattern.

**Answer:**
Separates algorithm from object structure.

**Java:**
```java
interface Visitor {
    void visit(ElementA element);
    void visit(ElementB element);
}

interface Element {
    void accept(Visitor visitor);
}

class ElementA implements Element {
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

class ConcreteVisitor implements Visitor {
    public void visit(ElementA element) {
        System.out.println("Visiting ElementA");
    }
    
    public void visit(ElementB element) {
        System.out.println("Visiting ElementB");
    }
}
```

**Use Cases:**
- Compiler design
- AST traversal
- Report generation

### 33. Explain the Memento Pattern.

**Answer:**
Captures and restores object state without violating encapsulation.

**Java:**
```java
class Memento {
    private String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
}

class Originator {
    private String state;
    
    public void setState(String state) {
        this.state = state;
    }
    
    public Memento save() {
        return new Memento(state);
    }
    
    public void restore(Memento memento) {
        state = memento.getState();
    }
}

class Caretaker {
    private List<Memento> history = new ArrayList<>();
    
    public void save(Memento memento) {
        history.add(memento);
    }
    
    public Memento undo() {
        if (history.size() > 1) {
            history.remove(history.size() - 1);
            return history.get(history.size() - 1);
        }
        return null;
    }
}
```

**Use Cases:**
- Undo/redo functionality
- State snapshots
- Checkpoint systems

### 34. Explain the Interpreter Pattern.

**Answer:**
Defines grammar representation and interpreter.

**Java:**
```java
interface Expression {
    int interpret();
}

class Number implements Expression {
    private int value;
    
    public Number(int value) {
        this.value = value;
    }
    
    public int interpret() {
        return value;
    }
}

class Add implements Expression {
    private Expression left;
    private Expression right;
    
    public Add(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }
    
    public int interpret() {
        return left.interpret() + right.interpret();
    }
}

// Usage: 1 + 2
Expression expr = new Add(new Number(1), new Number(2));
int result = expr.interpret(); // 3
```

**Use Cases:**
- Language parsers
- Rule engines
- Query languages

### 35. Explain the Flyweight Pattern.

**Answer:**
Shares common state to reduce memory usage.

**Java:**
```java
class Flyweight {
    private String intrinsicState;
    
    public Flyweight(String intrinsicState) {
        this.intrinsicState = intrinsicState;
    }
    
    public void operation(String extrinsicState) {
        System.out.println("Intrinsic: " + intrinsicState);
        System.out.println("Extrinsic: " + extrinsicState);
    }
}

class FlyweightFactory {
    private Map<String, Flyweight> flyweights = new HashMap<>();
    
    public Flyweight getFlyweight(String key) {
        if (!flyweights.containsKey(key)) {
            flyweights.put(key, new Flyweight(key));
        }
        return flyweights.get(key);
    }
}
```

**Use Cases:**
- Text editors (character formatting)
- Game development (tree/grass rendering)
- GUI libraries

### 36. Explain the Bridge Pattern.

**Answer:**
Separates abstraction from implementation.

**Java:**
```java
interface Implementor {
    void operation();
}

class ConcreteImplementorA implements Implementor {
    public void operation() {
        System.out.println("Implementation A");
    }
}

abstract class Abstraction {
    protected Implementor implementor;
    
    public Abstraction(Implementor implementor) {
        this.implementor = implementor;
    }
    
    public abstract void operation();
}

class RefinedAbstraction extends Abstraction {
    public RefinedAbstraction(Implementor implementor) {
        super(implementor);
    }
    
    public void operation() {
        implementor.operation();
    }
}
```

**Use Cases:**
- Platform independence
- Database drivers
- GUI frameworks

### 37. Explain the Decorator Pattern vs Adapter Pattern.

**Answer:**
**Decorator:** Adds behavior dynamically
```java
interface Component {
    void operation();
}

class ConcreteComponent implements Component {
    public void operation() {
        System.out.println("Base operation");
    }
}

class Decorator implements Component {
    protected Component component;
    
    public Decorator(Component component) {
        this.component = component;
    }
    
    public void operation() {
        component.operation();
    }
}

class ConcreteDecorator extends Decorator {
    public ConcreteDecorator(Component component) {
        super(component);
    }
    
    public void operation() {
        super.operation();
        System.out.println("Added behavior");
    }
}
```

**Adapter:** Makes incompatible interfaces work together
```java
class Adaptee {
    public void specificRequest() {
        System.out.println("Specific request");
    }
}

class Adapter implements Target {
    private Adaptee adaptee;
    
    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }
    
    public void request() {
        adaptee.specificRequest();
    }
}
```

**Differences:**
- Decorator: Extends functionality
- Adapter: Makes incompatible interfaces compatible

### 38. Explain the Proxy Pattern Types.

**Answer:**
**Virtual Proxy:** Lazy loading
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

**Protection Proxy:** Access control
```java
class ProtectionProxy implements Subject {
    private RealSubject realSubject;
    private String userRole;
    
    public ProtectionProxy(String userRole) {
        this.userRole = userRole;
    }
    
    public void request() {
        if (userRole.equals("admin")) {
            if (realSubject == null) {
                realSubject = new RealSubject();
            }
            realSubject.request();
        } else {
            throw new RuntimeException("Access denied");
        }
    }
}
```

**Remote Proxy:** Network communication
**Smart Proxy:** Additional functionality (logging, caching)

---

This covers design patterns interview questions from beginner to advanced level with implementations in Java and JavaScript.

