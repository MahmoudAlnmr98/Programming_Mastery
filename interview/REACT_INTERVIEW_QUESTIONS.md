# React Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is React? Explain its key features.

**Answer:**
React is a JavaScript library for building user interfaces, developed by Facebook.

**Key Features:**
- **Component-Based**: Build encapsulated components
- **Declarative**: Describe what UI should look like
- **Virtual DOM**: Efficient updates and rendering
- **Unidirectional Data Flow**: Data flows down, events flow up
- **JSX**: JavaScript syntax extension
- **One-Way Data Binding**: Props flow down, events flow up

### 2. What is JSX?

**Answer:**
JSX (JavaScript XML) is a syntax extension that allows writing HTML-like code in JavaScript.

```jsx
// JSX
const element = <h1>Hello, World!</h1>;

// Compiled to
const element = React.createElement('h1', null, 'Hello, World!');

// JSX with expressions
const name = "John";
const element = <h1>Hello, {name}!</h1>;

// JSX attributes
const element = <div className="container" id="main">Content</div>;
```

**JSX Rules:**
- Return single root element (or Fragment)
- Use `className` instead of `class`
- Use camelCase for attributes
- Close all tags

### 3. Explain the difference between functional and class components.

**Answer:**
**Functional Component:**
```jsx
function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
}

// Arrow function
const Welcome = (props) => {
    return <h1>Hello, {props.name}!</h1>;
};
```

**Class Component:**
```jsx
class Welcome extends React.Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
```

**Differences:**
- Functional: Simpler, no `this`, hooks for state/effects
- Class: More verbose, `this` binding, lifecycle methods

### 4. What are props in React?

**Answer:**
Props (properties) are read-only data passed from parent to child components.

```jsx
// Parent component
function App() {
    return <UserProfile name="John" age={30} />;
}

// Child component
function UserProfile({ name, age }) {
    return (
        <div>
            <h1>{name}</h1>
            <p>Age: {age}</p>
        </div>
    );
}
```

**Props Rules:**
- Props are read-only (immutable)
- Props flow down (parent to child)
- Use props for configuration

### 5. What is state in React?

**Answer:**
State is component-specific data that can change over time.

```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}
```

**State Rules:**
- State is local to component
- State changes trigger re-render
- Use `setState` or state setter to update

### 6. Explain the difference between props and state.

**Answer:**
| Props | State |
|-------|-------|
| Passed from parent | Managed within component |
| Read-only | Mutable |
| External data | Internal data |
| Cannot be changed | Can be changed |

```jsx
function Parent() {
    const [name, setName] = useState("John"); // State
    
    return <Child name={name} />; // Props
}

function Child({ name }) {
    // name is prop, cannot modify
    return <h1>{name}</h1>;
}
```

### 7. What are React Hooks?

**Answer:**
Hooks are functions that let you use state and other React features in functional components.

**Common Hooks:**
- `useState`: Manage state
- `useEffect`: Side effects
- `useContext`: Access context
- `useReducer`: Complex state logic
- `useMemo`: Memoize values
- `useCallback`: Memoize functions

```jsx
import { useState, useEffect } from 'react';

function Example() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        document.title = `Count: ${count}`;
    }, [count]);

    return (
        <button onClick={() => setCount(count + 1)}>
            Count: {count}
        </button>
    );
}
```

### 8. What is the Virtual DOM?

**Answer:**
Virtual DOM is a JavaScript representation of the real DOM. React uses it for efficient updates.

**How it works:**
1. React creates Virtual DOM tree
2. On state change, new Virtual DOM created
3. React compares (diffs) old and new Virtual DOM
4. Only changed nodes updated in real DOM

**Benefits:**
- Faster updates (batched)
- Efficient re-rendering
- Cross-browser compatibility

---

## Intermediate Level

### 9. Explain the `useEffect` hook in detail.

**Answer:**
`useEffect` handles side effects in functional components.

```jsx
import { useEffect, useState } from 'react';

function Example() {
    const [data, setData] = useState(null);

    // Run on every render
    useEffect(() => {
        console.log('Rendered');
    });

    // Run only on mount
    useEffect(() => {
        fetchData();
    }, []);

    // Run when dependencies change
    useEffect(() => {
        fetchUser(userId);
    }, [userId]);

    // Cleanup function
    useEffect(() => {
        const timer = setInterval(() => {
            console.log('Tick');
        }, 1000);

        return () => {
            clearInterval(timer); // Cleanup
        };
    }, []);
}
```

**Use Cases:**
- API calls
- Subscriptions
- DOM manipulation
- Timers

### 10. Explain React's component lifecycle.

**Answer:**
**Class Component Lifecycle:**
```jsx
class Component extends React.Component {
    constructor(props) {
        super(props);
        // Initialize state
    }

    componentDidMount() {
        // After mount - API calls, subscriptions
    }

    componentDidUpdate(prevProps, prevState) {
        // After update - react to prop/state changes
    }

    componentWillUnmount() {
        // Before unmount - cleanup
    }

    render() {
        return <div>Content</div>;
    }
}
```

**Functional Component Equivalent:**
```jsx
function Component() {
    // componentDidMount
    useEffect(() => {
        // Mount logic
    }, []);

    // componentDidUpdate
    useEffect(() => {
        // Update logic
    }, [dependency]);

    // componentWillUnmount
    useEffect(() => {
        return () => {
            // Cleanup
        };
    }, []);
}
```

### 11. Explain the Context API.

**Answer:**
Context provides a way to pass data through component tree without prop drilling.

```jsx
import { createContext, useContext, useState } from 'react';

// Create context
const ThemeContext = createContext('light');

// Provider
function App() {
    const [theme, setTheme] = useState('dark');
    
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Toolbar />
        </ThemeContext.Provider>
    );
}

// Consumer
function Toolbar() {
    const { theme, setTheme } = useContext(ThemeContext);
    
    return (
        <div>
            <p>Theme: {theme}</p>
            <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
                Toggle
            </button>
        </div>
    );
}
```

### 12. Explain React's reconciliation and diffing algorithm.

**Answer:**
**Reconciliation:** Process of updating DOM to match React elements.

**Diffing Algorithm:**
1. **Elements of different types**: Tear down old, build new
2. **Same DOM element**: Update changed attributes
3. **Component elements**: Update props, re-render if needed
4. **List items**: Use keys for efficient updates

```jsx
// Without key - inefficient
{items.map(item => <Item data={item} />)}

// With key - efficient
{items.map(item => <Item key={item.id} data={item} />)}
```

**Keys:**
- Help React identify which items changed
- Should be stable, unique, predictable
- Don't use index if list can reorder

### 13. Explain `useMemo` and `useCallback`.

**Answer:**
**useMemo:** Memoize expensive calculations
```jsx
import { useMemo } from 'react';

function ExpensiveComponent({ items }) {
    const expensiveValue = useMemo(() => {
        return items.reduce((sum, item) => sum + item.value, 0);
    }, [items]);

    return <div>Total: {expensiveValue}</div>;
}
```

**useCallback:** Memoize functions
```jsx
import { useCallback } from 'react';

function Parent({ items }) {
    const handleClick = useCallback((id) => {
        console.log('Clicked:', id);
    }, []);

    return <Child items={items} onClick={handleClick} />;
}
```

**When to use:**
- `useMemo`: Expensive calculations
- `useCallback`: Functions passed as props to prevent re-renders

### 14. Explain React.memo and when to use it.

**Answer:**
`React.memo` is a higher-order component that memoizes functional components.

```jsx
import { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
    // Expensive rendering
    return <div>{/* Complex UI */}</div>;
});

// Only re-renders if props change
```

**When to use:**
- Component renders frequently
- Props change rarely
- Expensive rendering

**When not to use:**
- Props change frequently
- Component is cheap to render
- Premature optimization

### 15. Explain error boundaries in React.

**Answer:**
Error boundaries catch JavaScript errors in component tree.

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
        console.error('Error:', error, errorInfo);
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

**Limitations:**
- Only catches errors in:
  - Render methods
  - Lifecycle methods
  - Constructors
- Doesn't catch:
  - Event handlers
  - Async code
  - Server-side rendering errors

### 16. Explain controlled vs uncontrolled components.

**Answer:**
**Controlled Component:**
```jsx
function ControlledInput() {
    const [value, setValue] = useState('');

    return (
        <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
        />
    );
}
```

**Uncontrolled Component:**
```jsx
function UncontrolledInput() {
    const inputRef = useRef(null);

    const handleSubmit = () => {
        console.log(inputRef.current.value);
    };

    return (
        <input
            ref={inputRef}
            type="text"
        />
    );
}
```

**Differences:**
- Controlled: React controls value via state
- Uncontrolled: DOM controls value via ref

---

## Advanced Level

### 17. Explain React's Fiber architecture.

**Answer:**
Fiber is React's reconciliation algorithm rewrite for better performance.

**Features:**
- **Incremental Rendering**: Can split work into chunks
- **Priority Scheduling**: High priority updates first
- **Interruptible**: Can pause, abort, reuse work
- **Time Slicing**: Break work into small units

**Benefits:**
- Better performance
- Smoother animations
- More responsive UI

### 18. Explain custom hooks and how to create them.

**Answer:**
Custom hooks extract component logic into reusable functions.

```jsx
// Custom hook
function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);

    const increment = () => setCount(count + 1);
    const decrement = () => setCount(count - 1);
    const reset = () => setCount(initialValue);

    return { count, increment, decrement, reset };
}

// Usage
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
```

### 19. Explain code splitting and lazy loading in React.

**Answer:**
**Code Splitting:**
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

**Benefits:**
- Smaller initial bundle
- Faster initial load
- Load code on demand

### 20. Explain React's render props pattern.

**Answer:**
Render props is a pattern where component receives function as prop to render content.

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

### 21. Explain higher-order components (HOCs).

**Answer:**
HOC is a function that takes component and returns new component.

```jsx
function withLoading(Component) {
    return function WithLoadingComponent({ isLoading, ...props }) {
        if (isLoading) {
            return <div>Loading...</div>;
        }
        return <Component {...props} />;
    };
}

// Usage
const UserProfileWithLoading = withLoading(UserProfile);
```

**Use Cases:**
- Code reuse
- Logic abstraction
- Props manipulation

### 22. Explain React's concurrent features.

**Answer:**
**Concurrent Mode Features:**
- **Suspense**: Declarative loading states
- **useTransition**: Mark updates as transitions
- **useDeferredValue**: Defer value updates

```jsx
import { useTransition } from 'react';

function App() {
    const [isPending, startTransition] = useTransition();
    const [count, setCount] = useState(0);

    const handleClick = () => {
        startTransition(() => {
            setCount(count + 1);
        });
    };

    return (
        <div>
            {isPending && <div>Loading...</div>}
            <button onClick={handleClick}>Count: {count}</button>
        </div>
    );
}
```

### 23. Explain React Server Components.

**Answer:**
Server Components render on server, reducing client bundle size.

**Features:**
- Run on server
- Access backend directly
- Zero bundle size
- Can't use hooks, event handlers

**Use Cases:**
- Data fetching
- Static content
- Large dependencies

### 24. Explain React's performance optimization techniques.

**Answer:**
**Techniques:**
1. **React.memo**: Memoize components
2. **useMemo**: Memoize values
3. **useCallback**: Memoize functions
4. **Code Splitting**: Lazy load components
5. **Virtualization**: Render only visible items
6. **Key Optimization**: Proper keys in lists

```jsx
// Virtualization with react-window
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
    return (
        <FixedSizeList
            height={600}
            itemCount={items.length}
            itemSize={35}
        >
            {({ index, style }) => (
                <div style={style}>{items[index].name}</div>
            )}
        </FixedSizeList>
    );
}
```

### 25. Explain React's testing best practices.

**Answer:**
**Testing Libraries:**
- **Jest**: Test runner
- **React Testing Library**: Component testing
- **Enzyme**: Alternative testing utility

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

**Best Practices:**
- Test user behavior, not implementation
- Use data-testid sparingly
- Test accessibility
- Mock external dependencies

---

This covers React interview questions from beginner to advanced level with detailed explanations and code examples.

