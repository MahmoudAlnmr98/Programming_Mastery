# Complete React Mastery Guide

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [JSX & Rendering](#jsx--rendering)
3. [Components](#components)
4. [Props](#props)
5. [State Management](#state-management)
6. [Hooks](#hooks)
7. [Event Handling](#event-handling)
8. [Conditional Rendering](#conditional-rendering)
9. [Lists & Keys](#lists--keys)
10. [Forms](#forms)
11. [Component Lifecycle](#component-lifecycle)
12. [Context API](#context-api)
13. [Refs & DOM Manipulation](#refs--dom-manipulation)
14. [Performance Optimization](#performance-optimization)
15. [Error Boundaries](#error-boundaries)
16. [Routing](#routing)
17. [State Management Libraries](#state-management-libraries)
18. [Testing](#testing)
19. [Advanced Patterns](#advanced-patterns)
20. [Best Practices](#best-practices)
21. [React Ecosystem](#react-ecosystem)

---

## Fundamentals

### What is React?
React is a JavaScript library for building user interfaces. It's:
- **Component-Based**: Build encapsulated components
- **Declarative**: Describe what UI should look like
- **Virtual DOM**: Efficient updates and rendering
- **Unidirectional Data Flow**: Data flows down, events flow up
- **Learn Once, Write Anywhere**: Works with web, mobile (React Native), desktop

### React Setup
```bash
# Create React app
npx create-react-app my-app
cd my-app
npm start

# Using Vite (faster)
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev

# Using Next.js (full-stack framework)
npx create-next-app@latest my-app
```

### Project Structure
```
my-app/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

### Basic React App
```jsx
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

// src/App.js
import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Hello, React!</h1>
    </div>
  );
}

export default App;
```

---

## JSX & Rendering

### JSX Basics
```jsx
// JSX is JavaScript XML
const element = <h1>Hello, World!</h1>;

// JSX expressions
const name = "John";
const element = <h1>Hello, {name}!</h1>;

// JSX attributes
const element = <div className="container" id="main">Content</div>;

// Self-closing tags
const element = <img src="image.jpg" alt="Description" />;
```

### JSX Rules
```jsx
// 1. Return single root element
function App() {
  return (
    <div>
      <h1>Title</h1>
      <p>Content</p>
    </div>
  );
}

// 2. Use Fragment to avoid wrapper
function App() {
  return (
    <>
      <h1>Title</h1>
      <p>Content</p>
    </>
  );
}

// 3. Use className instead of class
<div className="container">Content</div>

// 4. Use camelCase for attributes
<input type="text" tabIndex={0} />

// 5. Close all tags
<br />  // Not <br>
<img /> // Not <img>
```

### Embedding Expressions
```jsx
// Variables
const name = "John";
const element = <h1>Hello, {name}</h1>;

// Functions
function formatName(user) {
  return user.firstName + ' ' + user.lastName;
}
const element = <h1>Hello, {formatName(user)}!</h1>;

// Ternary operator
const element = <h1>{isLoggedIn ? 'Welcome' : 'Please login'}</h1>;

// Logical AND
const element = <div>{unreadMessages.length > 0 && <h2>You have messages</h2>}</div>;

// Array methods
const numbers = [1, 2, 3, 4, 5];
const listItems = numbers.map((number) => <li key={number}>{number}</li>);
```

### Rendering
```jsx
// Render element
const element = <h1>Hello, World!</h1>;
ReactDOM.render(element, document.getElementById('root'));

// Render component
function Welcome() {
  return <h1>Hello, World!</h1>;
}
ReactDOM.render(<Welcome />, document.getElementById('root'));

// Update rendered element
function tick() {
  const element = (
    <div>
      <h1>Hello, World!</h1>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  ReactDOM.render(element, document.getElementById('root'));
}
setInterval(tick, 1000);
```

---

## Components

### Function Components
```jsx
// Simple function component
function Welcome() {
  return <h1>Hello, World!</h1>;
}

// Arrow function component
const Welcome = () => {
  return <h1>Hello, World!</h1>;
};

// Component with props
function Welcome(props) {
  return <h1>Hello, {props.name}!</h1>;
}

// Using component
<Welcome name="John" />
```

### Class Components
```jsx
import React, { Component } from 'react';

class Welcome extends Component {
  render() {
    return <h1>Hello, {this.props.name}!</h1>;
  }
}

// Class component with state
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          Increment
        </button>
      </div>
    );
  }
}
```

### Component Composition
```jsx
// Parent component
function App() {
  return (
    <div>
      <Header />
      <Main />
      <Footer />
    </div>
  );
}

// Child components
function Header() {
  return <header>Header</header>;
}

function Main() {
  return <main>Main Content</main>;
}

function Footer() {
  return <footer>Footer</footer>;
}
```

### Component Reusability
```jsx
// Reusable Button component
function Button({ text, onClick, variant = 'primary' }) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {text}
    </button>
  );
}

// Usage
<Button text="Click me" onClick={handleClick} />
<Button text="Delete" onClick={handleDelete} variant="danger" />
```

---

## Props

### Passing Props
```jsx
// Parent component
function App() {
  const user = { name: "John", age: 30 };
  return <UserProfile user={user} />;
}

// Child component
function UserProfile({ user }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>Age: {user.age}</p>
    </div>
  );
}
```

### Props Destructuring
```jsx
// Without destructuring
function UserProfile(props) {
  return (
    <div>
      <h1>{props.name}</h1>
      <p>{props.email}</p>
    </div>
  );
}

// With destructuring
function UserProfile({ name, email }) {
  return (
    <div>
      <h1>{name}</h1>
      <p>{email}</p>
    </div>
  );
}

// With default values
function UserProfile({ name = "Guest", email = "guest@example.com" }) {
  return (
    <div>
      <h1>{name}</h1>
      <p>{email}</p>
    </div>
  );
}
```

### Children Prop
```jsx
// Component with children
function Card({ children, title }) {
  return (
    <div className="card">
      {title && <h2>{title}</h2>}
      <div className="card-body">{children}</div>
    </div>
  );
}

// Usage
<Card title="User Info">
  <p>Name: John</p>
  <p>Email: john@example.com</p>
</Card>
```

### PropTypes
```jsx
import PropTypes from 'prop-types';

function UserProfile({ name, age, email }) {
  return (
    <div>
      <h1>{name}</h1>
      <p>Age: {age}</p>
      <p>Email: {email}</p>
    </div>
  );
}

UserProfile.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number,
  email: PropTypes.string.isRequired,
};

UserProfile.defaultProps = {
  age: 0,
};
```

### TypeScript with Props
```tsx
// TypeScript interface
interface UserProfileProps {
  name: string;
  age?: number;
  email: string;
}

function UserProfile({ name, age = 0, email }: UserProfileProps) {
  return (
    <div>
      <h1>{name}</h1>
      <p>Age: {age}</p>
      <p>Email: {email}</p>
    </div>
  );
}
```

---

## State Management

### useState Hook
```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

### Multiple State Variables
```jsx
function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState(0);

  return (
    <form>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="number"
        value={age}
        onChange={(e) => setAge(Number(e.target.value))}
        placeholder="Age"
      />
    </form>
  );
}
```

### State with Objects
```jsx
function UserForm() {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0,
  });

  const handleChange = (field, value) => {
    setUser({ ...user, [field]: value });
  };

  return (
    <form>
      <input
        type="text"
        value={user.name}
        onChange={(e) => handleChange('name', e.target.value)}
      />
      <input
        type="email"
        value={user.email}
        onChange={(e) => handleChange('email', e.target.value)}
      />
    </form>
  );
}
```

### State with Arrays
```jsx
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput('');
  };

  const removeTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => removeTodo(todo.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Functional Updates
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  // Use functional update when new state depends on previous
  const increment = () => {
    setCount(prevCount => prevCount + 1);
  };

  const incrementBy = (amount) => {
    setCount(prevCount => prevCount + amount);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
      <button onClick={() => incrementBy(5)}>Increment by 5</button>
    </div>
  );
}
```

---

## Hooks

### useState
```jsx
import { useState } from 'react';

function Example() {
  const [state, setState] = useState(initialValue);
  // ...
}
```

### useEffect
```jsx
import { useEffect } from 'react';

// Run on every render
function Example() {
  useEffect(() => {
    console.log('Component rendered');
  });
}

// Run only on mount
function Example() {
  useEffect(() => {
    console.log('Component mounted');
  }, []);
}

// Run when dependencies change
function Example({ userId }) {
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);
}

// Cleanup function
function Example() {
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('Tick');
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);
}
```

### useContext
```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return <div>Theme: {theme}</div>;
}
```

### useReducer
```jsx
import { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return initialState;
    default:
      throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

### useMemo
```jsx
import { useMemo } from 'react';

function ExpensiveComponent({ items }) {
  const expensiveValue = useMemo(() => {
    return items.reduce((sum, item) => sum + item.value, 0);
  }, [items]);

  return <div>Total: {expensiveValue}</div>;
}
```

### useCallback
```jsx
import { useCallback } from 'react';

function Parent({ items }) {
  const handleClick = useCallback((id) => {
    console.log('Clicked:', id);
  }, []);

  return <Child items={items} onClick={handleClick} />;
}
```

### useRef
```jsx
import { useRef } from 'react';

function TextInput() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

### Custom Hooks
```jsx
// Custom hook
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}

// Using custom hook
function Counter() {
  const { count, increment, decrement, reset } = useCounter(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

### More Custom Hooks
```jsx
// useFetch hook
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [url]);

  return { data, loading, error };
}

// useLocalStorage hook
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}
```

---

## Event Handling

### Basic Event Handling
```jsx
function Button() {
  const handleClick = () => {
    console.log('Button clicked');
  };

  return <button onClick={handleClick}>Click me</button>;
}
```

### Event Object
```jsx
function Input() {
  const handleChange = (e) => {
    console.log('Value:', e.target.value);
  };

  return <input onChange={handleChange} />;
}
```

### Passing Arguments
```jsx
function TodoList({ todos }) {
  const handleDelete = (id) => {
    console.log('Delete:', id);
  };

  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          {todo.text}
          <button onClick={() => handleDelete(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

### Synthetic Events
```jsx
function Form() {
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Event Pooling (React 16 and earlier)
```jsx
// In React 16 and earlier, events were pooled
// In React 17+, events are not pooled
function Button() {
  const handleClick = (e) => {
    // Access event properties immediately
    console.log(e.type);
  };

  return <button onClick={handleClick}>Click</button>;
}
```

---

## Conditional Rendering

### if/else
```jsx
function Greeting({ isLoggedIn }) {
  if (isLoggedIn) {
    return <h1>Welcome back!</h1>;
  } else {
    return <h1>Please sign in.</h1>;
  }
}
```

### Ternary Operator
```jsx
function Greeting({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn ? (
        <h1>Welcome back!</h1>
      ) : (
        <h1>Please sign in.</h1>
      )}
    </div>
  );
}
```

### Logical AND
```jsx
function Mailbox({ unreadMessages }) {
  return (
    <div>
      <h1>Hello!</h1>
      {unreadMessages.length > 0 && (
        <h2>You have {unreadMessages.length} unread messages.</h2>
      )}
    </div>
  );
}
```

### Early Return
```jsx
function Component({ data }) {
  if (!data) {
    return <div>Loading...</div>;
  }

  return <div>{data.content}</div>;
}
```

### Switch Statement
```jsx
function Status({ status }) {
  switch (status) {
    case 'loading':
      return <div>Loading...</div>;
    case 'error':
      return <div>Error occurred</div>;
    case 'success':
      return <div>Success!</div>;
    default:
      return <div>Unknown status</div>;
  }
}
```

---

## Lists & Keys

### Rendering Lists
```jsx
function NumberList({ numbers }) {
  const listItems = numbers.map((number) => (
    <li key={number.toString()}>{number}</li>
  ));

  return <ul>{listItems}</ul>;
}
```

### Keys
```jsx
// Keys help React identify which items changed
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

### Key Rules
```jsx
// ✅ Good: Use stable, unique IDs
{todos.map(todo => (
  <TodoItem key={todo.id} todo={todo} />
))}

// ❌ Bad: Using index (only if list is static)
{todos.map((todo, index) => (
  <TodoItem key={index} todo={todo} />
))}

// ✅ Good: Extract to component
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </ul>
  );
}
```

### Keys in Components
```jsx
function TodoItem({ todo }) {
  return <li>{todo.text}</li>;
}

function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </ul>
  );
}
```

---

## Forms

### Controlled Components
```jsx
function NameForm() {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('A name was submitted: ' + value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Multiple Inputs
```jsx
function ReservationForm() {
  const [formData, setFormData] = useState({
    isGoing: true,
    numberOfGuests: 2,
  });

  const handleInputChange = (e) => {
    const target = e.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <form>
      <label>
        Is going:
        <input
          name="isGoing"
          type="checkbox"
          checked={formData.isGoing}
          onChange={handleInputChange}
        />
      </label>
      <br />
      <label>
        Number of guests:
        <input
          name="numberOfGuests"
          type="number"
          value={formData.numberOfGuests}
          onChange={handleInputChange}
        />
      </label>
    </form>
  );
}
```

### Uncontrolled Components
```jsx
function NameForm() {
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('A name was submitted: ' + inputRef.current.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input type="text" ref={inputRef} />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Form Validation
```jsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    if (password.length < 6) newErrors.password = 'Password must be at least 6 characters';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      // Submit form
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {errors.email && <span>{errors.email}</span>}
      </div>
      <div>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {errors.password && <span>{errors.password}</span>}
      </div>
      <button type="submit">Login</button>
    </form>
  );
}
```

---

## Component Lifecycle

### Class Component Lifecycle
```jsx
class Component extends React.Component {
  constructor(props) {
    super(props);
    // Initialize state
  }

  componentDidMount() {
    // Called after component is mounted
    // Good for API calls, subscriptions
  }

  componentDidUpdate(prevProps, prevState) {
    // Called after update
    // Good for reacting to prop/state changes
  }

  componentWillUnmount() {
    // Called before unmounting
    // Good for cleanup
  }

  render() {
    return <div>Content</div>;
  }
}
```

### useEffect Equivalents
```jsx
// componentDidMount
useEffect(() => {
  // Code here
}, []);

// componentDidUpdate
useEffect(() => {
  // Code here
}, [dependency]);

// componentWillUnmount
useEffect(() => {
  return () => {
    // Cleanup code
  };
}, []);
```

---

## Context API

### Creating Context
```jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function App() {
  return (
    <ThemeProvider>
      <Toolbar />
    </ThemeProvider>
  );
}

function Toolbar() {
  const { theme, setTheme } = useTheme();
  return (
    <div>
      <p>Current theme: {theme}</p>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle theme
      </button>
    </div>
  );
}
```

### Multiple Contexts
```jsx
const ThemeContext = createContext();
const UserContext = createContext();

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <UserContext.Provider value={{ name: 'John' }}>
        <Content />
      </UserContext.Provider>
    </ThemeContext.Provider>
  );
}
```

---

## Refs & DOM Manipulation

### useRef
```jsx
import { useRef } from 'react';

function TextInput() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

### Forwarding Refs
```jsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

const FancyInput = forwardRef((props, ref) => {
  const inputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current.focus();
    },
    getValue: () => {
      return inputRef.current.value;
    },
  }));

  return <input ref={inputRef} {...props} />;
});

function App() {
  const fancyInputRef = useRef(null);

  return (
    <div>
      <FancyInput ref={fancyInputRef} />
      <button onClick={() => fancyInputRef.current.focus()}>
        Focus
      </button>
    </div>
  );
}
```

### Callback Refs
```jsx
function MeasureExample() {
  const [height, setHeight] = useState(0);

  const measuredRef = useCallback((node) => {
    if (node !== null) {
      setHeight(node.getBoundingClientRect().height);
    }
  }, []);

  return (
    <div ref={measuredRef}>
      <h1>Hello, world</h1>
      <h2>The above header is {Math.round(height)}px tall</h2>
    </div>
  );
}
```

---

## Performance Optimization

### React.memo
```jsx
import { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  // Expensive rendering
  return <div>{/* Complex UI */}</div>;
});

// Only re-renders if props change
```

### useMemo
```jsx
import { useMemo } from 'react';

function ExpensiveComponent({ items }) {
  const expensiveValue = useMemo(() => {
    return items.reduce((sum, item) => sum + item.value, 0);
  }, [items]);

  return <div>Total: {expensiveValue}</div>;
}
```

### useCallback
```jsx
import { useCallback } from 'react';

function Parent({ items }) {
  const handleClick = useCallback((id) => {
    console.log('Clicked:', id);
  }, []);

  return <Child items={items} onClick={handleClick} />;
}
```

### Code Splitting
```jsx
import { lazy, Suspense } from 'react';

const LazyComponent = lazy(() => import('./LazyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}
```

### Virtualization
```jsx
// Using react-window
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

---

## Error Boundaries

### Error Boundary Class
```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <MyWidget />
</ErrorBoundary>
```

### Error Boundary Hook (Third-party)
```jsx
// Using react-error-boundary
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong:</p>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MyWidget />
    </ErrorBoundary>
  );
}
```

---

## Routing

### React Router
```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/users">Users</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
        <Route path="/users/:id" element={<UserDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Navigation
```jsx
import { useNavigate, useParams } from 'react-router-dom';

function UserDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div>
      <h1>User {id}</h1>
      <button onClick={() => navigate('/users')}>
        Back to Users
      </button>
    </div>
  );
}
```

### Protected Routes
```jsx
function ProtectedRoute({ children }) {
  const isAuthenticated = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

---

## State Management Libraries

### Redux
```jsx
// Store
import { createStore } from 'redux';

function counterReducer(state = { count: 0 }, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

const store = createStore(counterReducer);

// Component
import { useSelector, useDispatch } from 'react-redux';

function Counter() {
  const count = useSelector(state => state.count);
  const dispatch = useDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </div>
  );
}
```

### Zustand
```jsx
import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

function Counter() {
  const { count, increment, decrement } = useStore();
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### Jotai
```jsx
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(count - 1)}>-</button>
    </div>
  );
}
```

---

## Testing

### React Testing Library
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

test('increments counter', () => {
  render(<Counter />);
  const button = screen.getByText('Increment');
  fireEvent.click(button);
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

### Jest
```jsx
import { render } from '@testing-library/react';
import App from './App';

test('renders app', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
```

### Testing Hooks
```jsx
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from './useCounter';

test('increments counter', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});
```

---

## Advanced Patterns

### Higher-Order Components (HOC)
```jsx
function withLoading(Component) {
  return function WithLoadingComponent({ isLoading, ...props }) {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    return <Component {...props} />;
  };
}

const UserProfileWithLoading = withLoading(UserProfile);
```

### Render Props
```jsx
function Mouse({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return render(position);
}

// Usage
<Mouse render={({ x, y }) => (
  <p>The mouse position is ({x}, {y})</p>
)} />
```

### Compound Components
```jsx
function Tabs({ children }) {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabsList({ children }) {
  return <div className="tabs-list">{children}</div>;
}

function TabsTrigger({ index, children }) {
  const { activeIndex, setActiveIndex } = useContext(TabsContext);
  return (
    <button
      className={activeIndex === index ? 'active' : ''}
      onClick={() => setActiveIndex(index)}
    >
      {children}
    </button>
  );
}

// Usage
<Tabs>
  <TabsList>
    <TabsTrigger index={0}>Tab 1</TabsTrigger>
    <TabsTrigger index={1}>Tab 2</TabsTrigger>
  </TabsList>
</Tabs>
```

---

## Best Practices

### Component Organization
```jsx
// 1. One component per file
// 2. Use functional components
// 3. Keep components small and focused
// 4. Extract reusable logic to custom hooks
// 5. Use meaningful names
```

### State Management
```jsx
// 1. Lift state up when needed
// 2. Use Context for global state
// 3. Consider state management library for complex apps
// 4. Keep state as local as possible
```

### Performance
```jsx
// 1. Use React.memo for expensive components
// 2. Use useMemo for expensive calculations
// 3. Use useCallback for function props
// 4. Code split large components
// 5. Virtualize long lists
```

### Code Quality
```jsx
// 1. Use PropTypes or TypeScript
// 2. Handle errors with Error Boundaries
// 3. Write tests
// 4. Follow consistent naming conventions
// 5. Use ESLint and Prettier
```

---

## React Ecosystem

### Popular Libraries
- **Next.js**: Full-stack React framework
- **Gatsby**: Static site generator
- **Remix**: Full-stack web framework
- **React Native**: Mobile development
- **React Query**: Data fetching
- **React Hook Form**: Form management
- **Framer Motion**: Animation library
- **Material-UI**: Component library
- **Chakra UI**: Component library
- **Ant Design**: Component library

### Development Tools
- **React DevTools**: Browser extension
- **Create React App**: Boilerplate
- **Vite**: Fast build tool
- **ESLint**: Linting
- **Prettier**: Code formatting
- **Jest**: Testing framework
- **React Testing Library**: Testing utilities

---

## Resources for Further Learning

1. **React Official Documentation** - https://react.dev
2. **React Blog** - Official React blog
3. **React Patterns** - Common patterns and best practices
4. **Awesome React** - Curated list of React resources
5. **React TypeScript Cheatsheet** - TypeScript with React
6. **React Router** - Official routing library
7. **Redux** - State management library
8. **Next.js** - React framework

---

## Conclusion

This guide covers React from fundamentals to advanced topics. Mastery comes through:
- **Practice**: Build projects, solve problems
- **Understanding**: Know why, not just how
- **Reading**: Study well-written React code
- **Teaching**: Explain concepts to others
- **Staying Current**: Follow React evolution

Remember: React emphasizes component composition, unidirectional data flow, and declarative UI. Keep learning, keep practicing, and keep building!

### Key Takeaways
- React is component-based and declarative
- Master hooks for state and side effects
- Understand component lifecycle and rendering
- Use Context for global state
- Optimize performance with memoization
- Handle errors with Error Boundaries
- Follow React best practices and patterns
- Leverage the React ecosystem

