# Spring Boot Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Spring Boot? Explain its key features.

**Answer:**
Spring Boot is a framework that simplifies Spring application development.

**Key Features:**
- **Auto-Configuration**: Automatically configures Spring based on dependencies
- **Starter Dependencies**: Pre-configured dependency sets
- **Embedded Server**: Tomcat/Jetty included
- **Production Ready**: Actuator for monitoring
- **No XML Configuration**: Java/annotation-based
- **Opinionated Defaults**: Sensible defaults, can be overridden

### 2. Explain Spring Boot auto-configuration.

**Answer:**
Auto-configuration automatically configures beans based on classpath.

**How it works:**
- Scans classpath for dependencies
- Applies configuration if dependencies found
- Can be overridden with explicit configuration

**Example:**
- If `spring-boot-starter-data-jpa` on classpath → Auto-configures DataSource, EntityManager
- If `spring-boot-starter-web` on classpath → Auto-configures DispatcherServlet, embedded server

### 3. Explain Spring Boot starters.

**Answer:**
Starters are dependency descriptors that include multiple dependencies.

**Common Starters:**
```xml
<!-- Web -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- JPA -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<!-- Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### 4. Explain @SpringBootApplication annotation.

**Answer:**
`@SpringBootApplication` combines three annotations:

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// Equivalent to:
@Configuration
@EnableAutoConfiguration
@ComponentScan
```

- **@Configuration**: Marks as configuration class
- **@EnableAutoConfiguration**: Enables auto-configuration
- **@ComponentScan**: Scans for components

### 5. Explain Spring Boot profiles.

**Answer:**
Profiles allow different configurations for different environments.

```java
// application.properties
spring.profiles.active=dev

// application-dev.properties
database.url=jdbc:mysql://localhost:3306/devdb

// application-prod.properties
database.url=jdbc:mysql://prod-server:3306/proddb
```

**Using Profiles:**
```java
@Profile("dev")
@Configuration
public class DevConfig {
    // Dev-specific configuration
}
```

### 6. Explain Spring Boot Actuator.

**Answer:**
Actuator provides production-ready features for monitoring and management.

**Endpoints:**
- `/actuator/health`: Application health
- `/actuator/info`: Application information
- `/actuator/metrics`: Application metrics
- `/actuator/env`: Environment properties

**Configuration:**
```properties
management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always
```

### 7. Explain dependency injection in Spring Boot.

**Answer:**
Spring Boot uses dependency injection to manage object dependencies.

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// Constructor injection (recommended)
@Service
public class UserService {
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### 8. Explain @RestController vs @Controller.

**Answer:**
- **@Controller**: Returns view name, used with @ResponseBody for JSON
- **@RestController**: Combines @Controller + @ResponseBody, returns JSON/XML

```java
@RestController
public class UserController {
    @GetMapping("/users")
    public List<User> getUsers() {
        return userService.findAll();
    }
}

@Controller
public class UserController {
    @GetMapping("/users")
    @ResponseBody
    public List<User> getUsers() {
        return userService.findAll();
    }
}
```

---

## Intermediate Level

### 9. Explain Spring Boot JPA and repositories.

**Answer:**
**Entity:**
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    private String email;
}
```

**Repository:**
```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByName(String name);
    Optional<User> findByEmail(String email);
    @Query("SELECT u FROM User u WHERE u.age > :age")
    List<User> findUsersOlderThan(@Param("age") int age);
}
```

### 10. Explain Spring Boot Security.

**Answer:**
**Basic Configuration:**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .httpBasic();
        return http.build();
    }
}
```

**JWT Authentication:**
```java
@Configuration
public class JwtConfig {
    @Bean
    public JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder.withJwkSetUri("https://example.com/.well-known/jwks.json")
            .build();
    }
}
```

### 11. Explain Spring Boot exception handling.

**Answer:**
**Global Exception Handler:**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 12. Explain Spring Boot transaction management.

**Answer:**
```java
@Service
@Transactional
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @Transactional(rollbackFor = Exception.class)
    public void transferMoney(Long fromId, Long toId, BigDecimal amount) {
        User from = userRepository.findById(fromId).orElseThrow();
        User to = userRepository.findById(toId).orElseThrow();
        
        from.setBalance(from.getBalance().subtract(amount));
        to.setBalance(to.getBalance().add(amount));
        
        userRepository.save(from);
        userRepository.save(to);
    }
}
```

### 13. Explain Spring Boot caching.

**Answer:**
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("users");
    }
}

@Service
public class UserService {
    @Cacheable("users")
    public User getUser(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
    
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
```

### 14. Explain Spring Boot testing.

**Answer:**
```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    void testGetUser() throws Exception {
        when(userService.getUser(1L)).thenReturn(new User(1L, "John"));
        
        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}
```

### 15. Explain Spring Boot configuration properties.

**Answer:**
```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int version;
    private Database database;
    
    // Getters and setters
    
    public static class Database {
        private String url;
        private String username;
        private String password;
        // Getters and setters
    }
}

// application.properties
app.name=MyApp
app.version=1
app.database.url=jdbc:mysql://localhost:3306/mydb
app.database.username=root
app.database.password=password
```

---

## Advanced Level

### 16. Explain Spring Boot AOP.

**Answer:**
Aspect-Oriented Programming for cross-cutting concerns.

```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Before: " + joinPoint.getSignature());
    }
    
    @Around("@annotation(LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object proceed = joinPoint.proceed();
        long executionTime = System.currentTimeMillis() - start;
        System.out.println("Execution time: " + executionTime + "ms");
        return proceed;
    }
}
```

### 17. Explain Spring Boot async processing.

**Answer:**
```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.initialize();
        return executor;
    }
}

@Service
public class UserService {
    @Async
    public CompletableFuture<User> getUserAsync(Long id) {
        return CompletableFuture.completedFuture(userRepository.findById(id).orElseThrow());
    }
}
```

### 18. Explain Spring Boot microservices patterns.

**Answer:**
**Service Discovery (Eureka):**
```java
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}
```

**API Gateway (Spring Cloud Gateway):**
```java
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/users/**")
                .uri("lb://user-service"))
            .build();
    }
}
```

### 19. Explain Spring Boot monitoring and metrics.

**Answer:**
**Custom Metrics:**
```java
@Service
public class UserService {
    private final Counter userCounter;
    
    public UserService(MeterRegistry registry) {
        this.userCounter = Counter.builder("users.created")
            .description("Number of users created")
            .register(registry);
    }
    
    public void createUser(User user) {
        userRepository.save(user);
        userCounter.increment();
    }
}
```

### 20. Explain Spring Boot database migrations.

**Answer:**
**Flyway:**
```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

**Liquibase:**
```xml
<changeSet id="1" author="developer">
    <createTable tableName="users">
        <column name="id" type="BIGINT">
            <constraints primaryKey="true"/>
        </column>
        <column name="name" type="VARCHAR(100)"/>
    </createTable>
</changeSet>
```

### 21. Explain Spring Boot Actuator endpoints in detail.

**Answer:**
Actuator provides production-ready monitoring endpoints.

**Health Endpoints:**
```java
// Custom health indicator
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        if (checkService()) {
            return Health.up().withDetail("service", "available").build();
        }
        return Health.down().withDetail("service", "unavailable").build();
    }
}
```

**Metrics:**
```java
@RestController
public class UserController {
    private final Counter userCounter;
    
    public UserController(MeterRegistry registry) {
        this.userCounter = Counter.builder("users.created")
            .register(registry);
    }
}
```

### 22. Explain Spring Boot's @Conditional annotations.

**Answer:**
Conditional annotations enable beans based on conditions.

```java
@ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
@Configuration
public class FeatureConfig {
    // Configuration only if property is true
}

@ConditionalOnClass(name = "com.example.Class")
@Bean
public MyBean myBean() {
    return new MyBean();
}

@ConditionalOnMissingBean(DataSource.class)
@Bean
public DataSource dataSource() {
    // Only if DataSource bean doesn't exist
}
```

### 23. Explain Spring Boot's application properties and YAML.

**Answer:**
**Properties:**
```properties
app.name=MyApp
app.version=1.0
app.database.url=jdbc:mysql://localhost:3306/mydb
app.database.username=root
app.database.password=password
```

**YAML:**
```yaml
app:
  name: MyApp
  version: 1.0
  database:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: password
```

**Profile-specific:**
```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/devdb

# application-prod.yml
spring:
  datasource:
    url: jdbc:mysql://prod-server:3306/proddb
```

### 24. Explain Spring Boot's @Scheduled annotation.

**Answer:**
@Scheduled enables task scheduling.

```java
@Component
public class ScheduledTasks {
    @Scheduled(fixedRate = 5000)
    public void task1() {
        // Runs every 5 seconds
    }
    
    @Scheduled(fixedDelay = 5000)
    public void task2() {
        // Runs 5 seconds after previous completion
    }
    
    @Scheduled(cron = "0 0 * * * ?")
    public void task3() {
        // Runs every hour
    }
}

// Enable scheduling
@SpringBootApplication
@EnableScheduling
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 25. Explain Spring Boot's validation and error handling.

**Answer:**
**Validation:**
```java
public class User {
    @NotNull
    @Size(min = 2, max = 50)
    private String name;
    
    @Email
    @NotBlank
    private String email;
}

@PostMapping("/users")
public ResponseEntity<?> createUser(@Valid @RequestBody User user) {
    // Validation happens automatically
    return ResponseEntity.ok(userService.save(user));
}
```

**Global Exception Handler:**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("Validation failed", errors));
    }
}
```

### 26. Explain Spring Boot Actuator endpoints.

**Answer:**
Actuator provides production-ready features.

**Dependencies:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Configuration:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: always
```

**Endpoints:**
- `/actuator/health` - Application health
- `/actuator/info` - Application information
- `/actuator/metrics` - Application metrics
- `/actuator/env` - Environment variables
- `/actuator/loggers` - Logger configuration

**Custom Health Indicator:**
```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // Check custom condition
        if (isHealthy()) {
            return Health.up()
                .withDetail("status", "OK")
                .build();
        }
        return Health.down()
            .withDetail("error", "Service unavailable")
            .build();
    }
}
```

### 27. Explain Spring Boot testing strategies.

**Answer:**
**Unit Testing:**
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    void testCreateUser() {
        User user = new User("John");
        when(userRepository.save(any())).thenReturn(user);
        
        User result = userService.createUser(user);
        assertEquals("John", result.getName());
    }
}
```

**Integration Testing:**
```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testGetUser() throws Exception {
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}
```

**Test Slices:**
```java
@WebMvcTest(UserController.class)
class UserControllerWebTest {
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
}
```

### 28. Explain Spring Boot profiles and configuration.

**Answer:**
Profiles allow environment-specific configuration.

**Application Properties:**
```properties
# application.properties
spring.profiles.active=dev

# application-dev.properties
server.port=8080
logging.level.root=DEBUG

# application-prod.properties
server.port=80
logging.level.root=INFO
```

**YAML Configuration:**
```yaml
spring:
  profiles:
    active: dev

---
spring:
  profiles: dev
server:
  port: 8080

---
spring:
  profiles: prod
server:
  port: 80
```

**Programmatic:**
```java
@Configuration
@Profile("dev")
public class DevConfig {
    // Dev-specific beans
}

@Configuration
@Profile("prod")
public class ProdConfig {
    // Prod-specific beans
}
```

### 29. Explain Spring Boot caching strategies.

**Answer:**
**Enable Caching:**
```java
@SpringBootApplication
@EnableCaching
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**Cache Annotations:**
```java
@Service
public class UserService {
    @Cacheable("users")
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
    
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
}
```

**Cache Providers:**
- Caffeine
- Redis
- EhCache
- Hazelcast

**Configuration:**
```yaml
spring:
  cache:
    type: caffeine
    caffeine:
      spec: maximumSize=500,expireAfterWrite=5m
```

### 30. Explain Spring Boot monitoring and metrics.

**Answer:**
**Micrometer Integration:**
```java
@Service
public class OrderService {
    private final Counter orderCounter;
    private final Timer orderTimer;
    
    public OrderService(MeterRegistry registry) {
        this.orderCounter = Counter.builder("orders.total")
            .description("Total orders")
            .register(registry);
        this.orderTimer = Timer.builder("orders.duration")
            .register(registry);
    }
    
    public void createOrder(Order order) {
        Timer.Sample sample = Timer.start();
        try {
            // Create order
            orderCounter.increment();
        } finally {
            sample.stop(orderTimer);
        }
    }
}
```

**Custom Metrics:**
```java
@Component
public class CustomMetrics {
    private final Gauge gauge;
    
    public CustomMetrics(MeterRegistry registry) {
        this.gauge = Gauge.builder("custom.value", this, CustomMetrics::getValue)
            .register(registry);
    }
    
    private double getValue() {
        return 42.0;
    }
}
```

**Prometheus Integration:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

### 31. Explain Spring Boot Actuator Endpoints.

**Answer:**
Actuator provides production-ready features.

**Dependencies:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Configuration:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: always
```

**Endpoints:**
- `/actuator/health`: Application health
- `/actuator/info`: Application information
- `/actuator/metrics`: Application metrics
- `/actuator/env`: Environment variables

### 32. Explain Spring Boot Profiles.

**Answer:**
Profiles enable environment-specific configuration.

**Application Properties:**
```yaml
# application.yml
spring:
  profiles:
    active: dev

---
# application-dev.yml
server:
  port: 8080

---
# application-prod.yml
server:
  port: 443
```

**Programmatic:**
```java
@Profile("dev")
@Configuration
public class DevConfig {
    // Dev-specific configuration
}
```

**Activation:**
```bash
java -jar app.jar --spring.profiles.active=prod
```

### 33. Explain Spring Boot Auto-Configuration.

**Answer:**
Auto-configuration automatically configures beans.

**How it works:**
1. Spring Boot scans classpath
2. Finds `@ConditionalOnClass` annotations
3. Auto-configures based on dependencies

**Example:**
```java
@Configuration
@ConditionalOnClass(DataSource.class)
public class DataSourceAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public DataSource dataSource() {
        return new HikariDataSource();
    }
}
```

**Disable:**
```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class Application {
    // ...
}
```

### 34. Explain Spring Boot Externalized Configuration.

**Answer:**
Externalized configuration allows external property sources.

**Property Sources (Order):**
1. Command line arguments
2. `SPRING_APPLICATION_JSON`
3. `ServletConfig` init parameters
4. `ServletContext` init parameters
5. JNDI attributes
6. Java system properties
7. OS environment variables
8. `application-{profile}.properties`
9. `application.properties`

**Usage:**
```java
@Value("${app.name}")
private String appName;

@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int version;
    // Getters and setters
}
```

### 35. Explain Spring Boot Testing.

**Answer:**
Spring Boot provides testing support.

**Unit Test:**
```java
@SpringBootTest
class UserServiceTest {
    @MockBean
    private UserRepository userRepository;
    
    @Autowired
    private UserService userService;
    
    @Test
    void testCreateUser() {
        // Test implementation
    }
}
```

**Web Test:**
```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testGetUser() throws Exception {
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk());
    }
}
```

### 36. Explain Spring Boot Data JPA.

**Answer:**
Spring Data JPA simplifies database access.

**Entity:**
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    // Getters and setters
}
```

**Repository:**
```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByName(String name);
    Optional<User> findByEmail(String email);
    
    @Query("SELECT u FROM User u WHERE u.age > :age")
    List<User> findUsersOlderThan(@Param("age") int age);
}
```

### 37. Explain Spring Boot Transaction Management.

**Answer:**
Spring Boot provides declarative transaction management.

**Configuration:**
```java
@Configuration
@EnableTransactionManagement
public class TransactionConfig {
    @Bean
    public PlatformTransactionManager transactionManager() {
        return new DataSourceTransactionManager(dataSource());
    }
}
```

**Usage:**
```java
@Service
@Transactional
public class UserService {
    @Transactional(rollbackFor = Exception.class)
    public void createUser(User user) {
        userRepository.save(user);
        // Transaction automatically managed
    }
    
    @Transactional(readOnly = true)
    public User getUser(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}
```

### 38. Explain Spring Boot Caching.

**Answer:**
Spring Boot provides caching abstraction.

**Configuration:**
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("users");
    }
}
```

**Usage:**
```java
@Service
public class UserService {
    @Cacheable("users")
    public User getUser(Long id) {
        return userRepository.findById(id).orElse(null);
    }
    
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
}
```

### 39. Explain Spring Boot Security.

**Answer:**
Spring Security provides authentication and authorization.

**Configuration:**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .formLogin();
        return http.build();
    }
}
```

**JWT Authentication:**
```java
@Configuration
public class JwtConfig {
    @Bean
    public JwtAuthenticationFilter jwtAuthenticationFilter() {
        return new JwtAuthenticationFilter();
    }
}
```

### 40. Explain Spring Boot REST API Best Practices.

**Answer:**
**RESTful Design:**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping
    public ResponseEntity<List<User>> getUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.getUser(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User created = userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

**Exception Handling:**
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }
}
```

### 41. Explain Spring Boot Async Processing.

**Answer:**
Spring Boot supports asynchronous processing.

**Configuration:**
```java
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.initialize();
        return executor;
    }
}
```

**Usage:**
```java
@Service
public class EmailService {
    @Async
    public CompletableFuture<Void> sendEmail(String to, String subject) {
        // Send email asynchronously
        return CompletableFuture.completedFuture(null);
    }
}
```

### 42. Explain Spring Boot Scheduling.

**Answer:**
Spring Boot supports scheduled tasks.

**Configuration:**
```java
@Configuration
@EnableScheduling
public class SchedulingConfig {
    // Configuration
}
```

**Usage:**
```java
@Component
public class ScheduledTasks {
    @Scheduled(fixedRate = 5000)
    public void reportCurrentTime() {
        System.out.println("Current time: " + new Date());
    }
    
    @Scheduled(cron = "0 0 12 * * ?")
    public void dailyTask() {
        // Run daily at noon
    }
}
```

### 43. Explain Spring Boot Validation.

**Answer:**
Spring Boot provides validation support.

**Entity:**
```java
public class User {
    @NotNull
    @Size(min = 2, max = 50)
    private String name;
    
    @Email
    @NotBlank
    private String email;
    
    @Min(18)
    @Max(100)
    private int age;
}
```

**Controller:**
```java
@PostMapping
public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
    return ResponseEntity.ok(userService.createUser(user));
}
```

### 44. Explain Spring Boot Monitoring.

**Answer:**
Spring Boot Actuator provides monitoring.

**Custom Metrics:**
```java
@Service
public class UserService {
    private final Counter userCounter;
    
    public UserService(MeterRegistry meterRegistry) {
        this.userCounter = Counter.builder("users.created")
            .description("Number of users created")
            .register(meterRegistry);
    }
    
    public User createUser(User user) {
        userCounter.increment();
        return userRepository.save(user);
    }
}
```

**Health Indicators:**
```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // Check health
        return Health.up().build();
    }
}
```

### 45. Explain Spring Boot Docker Deployment.

**Answer:**
Docker deployment for Spring Boot applications.

**Dockerfile:**
```dockerfile
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=mydb
```

---

This covers Spring Boot interview questions from beginner to advanced level with detailed explanations and code examples.

