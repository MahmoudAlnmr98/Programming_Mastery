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

### 26. Explain React Portals.

**Answer:**
Portals render children into DOM node outside parent hierarchy.

```jsx
import { createPortal } from 'react-dom';

function Modal({ children }) {
    return createPortal(
        <div className="modal">
            {children}
        </div>,
        document.body
    );
}
```

**Use Cases:**
- Modals
- Tooltips
- Dropdowns
- Overlays

### 27. Explain React's useReducer hook.

**Answer:**
useReducer manages complex state logic.

```jsx
function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        case 'reset':
            return { count: 0 };
        default:
            return state;
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0 });
    
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

### 28. Explain React's useLayoutEffect hook.

**Answer:**
useLayoutEffect runs synchronously after DOM mutations but before paint.

```jsx
function Tooltip({ children, position }) {
    const ref = useRef(null);
    
    useLayoutEffect(() => {
        // Measure DOM before paint
        const { width, height } = ref.current.getBoundingClientRect();
        // Adjust position
    }, [position]);
    
    return <div ref={ref}>{children}</div>;
}
```

**Difference from useEffect:**
- useLayoutEffect: Synchronous, before paint
- useEffect: Asynchronous, after paint

### 29. Explain React's useImperativeHandle hook.

**Answer:**
useImperativeHandle customizes instance value exposed to parent via ref.

```jsx
const FancyInput = forwardRef((props, ref) => {
    const inputRef = useRef();
    
    useImperativeHandle(ref, () => ({
        focus: () => {
            inputRef.current.focus();
        },
        clear: () => {
            inputRef.current.value = '';
        }
    }));
    
    return <input ref={inputRef} {...props} />;
});

// Usage
function Parent() {
    const inputRef = useRef();
    
    return (
        <>
            <FancyInput ref={inputRef} />
            <button onClick={() => inputRef.current.focus()}>Focus</button>
        </>
    );
}
```

### 30. Explain React's useDebugValue hook.

**Answer:**
useDebugValue displays label in React DevTools for custom hooks.

```jsx
function useCounter(initialValue) {
    const [count, setCount] = useState(initialValue);
    
    useDebugValue(count > 10 ? 'High' : 'Low');
    
    return [count, setCount];
}
```

### 31. Explain useDeferredValue hook in detail.

**Answer:**
useDeferredValue defers updating value until more urgent updates complete.

```jsx
import { useDeferredValue, useState } from 'react';

function SearchResults({ query }) {
    const deferredQuery = useDeferredValue(query);
    
    // Use deferredQuery for expensive operations
    const results = useMemo(() => {
        return expensiveSearch(deferredQuery);
    }, [deferredQuery]);
    
    return (
        <div>
            {query !== deferredQuery && <div>Searching...</div>}
            <ResultsList results={results} />
        </div>
    );
}
```

**Use Cases:**
- Deferring expensive computations
- Keeping UI responsive
- Prioritizing urgent updates

### 32. Explain React's useId hook.

**Answer:**
useId generates unique IDs for accessibility.

```jsx
import { useId } from 'react';

function Form() {
    const id = useId();
    
    return (
        <>
            <label htmlFor={id}>Name</label>
            <input id={id} type="text" />
        </>
    );
}

// Multiple IDs
function Form() {
    const nameId = useId();
    const emailId = useId();
    
    return (
        <>
            <label htmlFor={nameId}>Name</label>
            <input id={nameId} type="text" />
            <label htmlFor={emailId}>Email</label>
            <input id={emailId} type="email" />
        </>
    );
}
```

### 33. Explain React's useSyncExternalStore hook.

**Answer:**
useSyncExternalStore subscribes to external store.

```jsx
import { useSyncExternalStore } from 'react';

function useStore(store) {
    return useSyncExternalStore(
        store.subscribe,
        store.getSnapshot
    );
}

// Usage
function Component() {
    const value = useStore(myStore);
    return <div>{value}</div>;
}
```

### 34. Explain React performance optimization techniques.

**Answer:**
**Techniques:**

**1. React.memo:**
```jsx
const ExpensiveComponent = React.memo(({ data }) => {
    return <div>{data}</div>;
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data; // Custom comparison
});
```

**2. useMemo:**
```jsx
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]); // Only recompute when a or b changes
```

**3. useCallback:**
```jsx
const handleClick = useCallback(() => {
    doSomething(id);
}, [id]); // Stable reference
```

**4. Code Splitting:**
```jsx
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <LazyComponent />
        </Suspense>
    );
}
```

**5. Virtualization:**
```jsx
import { FixedSizeList } from 'react-window';

function List({ items }) {
    return (
        <FixedSizeList
            height={600}
            itemCount={items.length}
            itemSize={50}
        >
            {({ index, style }) => (
                <div style={style}>{items[index]}</div>
            )}
        </FixedSizeList>
    );
}
```

### 35. Explain React error boundaries in detail.

**Answer:**
Error boundaries catch errors in component tree.

```jsx
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }
    
    componentDidCatch(error, errorInfo) {
        // Log to error reporting service
        console.error('Error caught:', error, errorInfo);
    }
    
    render() {
        if (this.state.hasError) {
            return (
                <div>
                    <h2>Something went wrong</h2>
                    <button onClick={() => this.setState({ hasError: false })}>
                        Try again
                    </button>
                </div>
            );
        }
        return this.props.children;
    }
}

// Usage
<ErrorBoundary>
    <App />
</ErrorBoundary>
```

**Limitations:**
- Doesn't catch errors in event handlers
- Doesn't catch errors in async code
- Doesn't catch errors during server-side rendering

### 36. Explain React Server Components (RSC).

**Answer:**
Server Components render on server, reducing client bundle.

**Server Component:**
```jsx
// app/users/page.js (Server Component)
async function UsersPage() {
    const users = await fetchUsers(); // Runs on server
    
    return (
        <div>
            {users.map(user => (
                <UserCard key={user.id} user={user} />
            ))}
        </div>
    );
}
```

**Client Component:**
```jsx
'use client'; // Directive for Client Component

import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Benefits:**
- Smaller client bundle
- Direct database access
- Better security (API keys on server)
- Improved performance

### 37. Explain React testing strategies.

**Answer:**
**Unit Testing with Jest and React Testing Library:**
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from './Button';

test('renders button and handles click', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
});
```

**Testing Hooks:**
```jsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('increments counter', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
        result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
});
```

**Snapshot Testing:**
```jsx
test('matches snapshot', () => {
    const { container } = render(<Component />);
    expect(container).toMatchSnapshot();
});
```

### 38. Explain React's useRef hook in detail.

**Answer:**
useRef returns mutable ref object that persists across renders.

```jsx
import { useRef, useEffect } from 'react';

function Component() {
    const inputRef = useRef(null);
    const countRef = useRef(0);
    
    useEffect(() => {
        inputRef.current.focus(); // Access DOM element
    }, []);
    
    const handleClick = () => {
        countRef.current += 1; // Mutable value (doesn't trigger re-render)
        console.log(countRef.current);
    };
    
    return (
        <>
            <input ref={inputRef} />
            <button onClick={handleClick}>Count: {countRef.current}</button>
        </>
    );
}
```

**Use Cases:**
- DOM element access
- Storing mutable values without re-render
- Previous value tracking

### 39. Explain React's forwardRef and useImperativeHandle.

**Answer:**
**forwardRef:**
```jsx
const FancyInput = forwardRef((props, ref) => {
    return <input ref={ref} {...props} />;
});

// Usage
function Parent() {
    const inputRef = useRef();
    
    return (
        <>
            <FancyInput ref={inputRef} />
            <button onClick={() => inputRef.current.focus()}>Focus</button>
        </>
    );
}
```

**useImperativeHandle:**
```jsx
const FancyInput = forwardRef((props, ref) => {
    const inputRef = useRef();
    
    useImperativeHandle(ref, () => ({
        focus: () => inputRef.current.focus(),
        clear: () => { inputRef.current.value = ''; },
        getValue: () => inputRef.current.value
    }));
    
    return <input ref={inputRef} {...props} />;
});
```

### 40. Explain React's useTransition hook.

**Answer:**
useTransition marks state updates as non-urgent transitions.

```jsx
import { useTransition, useState } from 'react';

function App() {
    const [isPending, startTransition] = useTransition();
    const [count, setCount] = useState(0);
    const [items, setItems] = useState([]);
    
    const handleClick = () => {
        setCount(count + 1); // Urgent update
        
        startTransition(() => {
            // Non-urgent update
            setItems(Array.from({ length: 10000 }, (_, i) => i));
        });
    };
    
    return (
        <div>
            {isPending && <div>Loading...</div>}
            <button onClick={handleClick}>Count: {count}</button>
            <ul>
                {items.map(item => <li key={item}>{item}</li>)}
            </ul>
        </div>
    );
}
```

**Benefits:**
- Keeps UI responsive during heavy updates
- Prioritizes urgent updates
- Better user experience

### 41. Explain React's useDeferredValue hook.

**Answer:**
useDeferredValue defers value updates until more urgent updates complete.

```jsx
import { useDeferredValue, useState, useMemo } from 'react';

function SearchResults({ query }) {
    const deferredQuery = useDeferredValue(query);
    
    const results = useMemo(() => {
        return expensiveSearch(deferredQuery);
    }, [deferredQuery]);
    
    return (
        <div>
            {query !== deferredQuery && <div>Searching...</div>}
            <ResultsList results={results} />
        </div>
    );
}
```

**Use Cases:**
- Deferring expensive computations
- Keeping UI responsive
- Prioritizing urgent updates

### 42. Explain React's useId hook.

**Answer:**
useId generates unique IDs for accessibility attributes.

```jsx
import { useId } from 'react';

function Form() {
    const nameId = useId();
    const emailId = useId();
    
    return (
        <>
            <label htmlFor={nameId}>Name</label>
            <input id={nameId} type="text" />
            
            <label htmlFor={emailId}>Email</label>
            <input id={emailId} type="email" />
        </>
    );
}
```

**Benefits:**
- Unique IDs across server and client
- Stable across re-renders
- No hydration mismatches

### 43. Explain React's useSyncExternalStore hook.

**Answer:**
useSyncExternalStore subscribes to external stores.

```jsx
import { useSyncExternalStore } from 'react';

function useStore(store) {
    return useSyncExternalStore(
        store.subscribe,
        store.getSnapshot
    );
}

// Usage
function Component() {
    const value = useStore(myStore);
    return <div>{value}</div>;
}
```

**Use Cases:**
- Redux, Zustand, other state management
- Browser APIs (localStorage, etc.)
- External data sources

### 44. Explain React's useInsertionEffect hook.

**Answer:**
useInsertionEffect runs synchronously before DOM mutations.

```jsx
import { useInsertionEffect } from 'react';

function Component() {
    useInsertionEffect(() => {
        // Inject styles before DOM updates
        const style = document.createElement('style');
        style.textContent = '.my-class { color: red; }';
        document.head.appendChild(style);
        
        return () => {
            document.head.removeChild(style);
        };
    });
    
    return <div className="my-class">Content</div>;
}
```

**Use Cases:**
- CSS-in-JS libraries
- Dynamic style injection
- DOM mutations before paint

### 45. Explain React's Strict Mode and its effects.

**Answer:**
Strict Mode helps identify problems in development.

**Effects:**
- Double-invokes functions to detect side effects
- Warns about deprecated APIs
- Detects unexpected side effects
- Detects legacy string ref usage

```jsx
import { StrictMode } from 'react';

function App() {
    return (
        <StrictMode>
            <MyApp />
        </StrictMode>
    );
}
```

**Double Invocation:**
```jsx
function Component() {
    useEffect(() => {
        console.log('Effect runs'); // Logs twice in Strict Mode (dev only)
    }, []);
    
    return <div>Content</div>;
}
```

### 46. Explain React's key prop and its importance.

**Answer:**
Keys help React identify which items changed, added, or removed.

```jsx
// Without key - inefficient
{items.map(item => <Item data={item} />)}

// With key - efficient
{items.map(item => <Item key={item.id} data={item} />)}
```

**Rules:**
- Must be unique among siblings
- Should be stable (not random)
- Don't use index if list can reorder
- Don't use index if items can be added/removed

**Common Mistakes:**
```jsx
// Bad - index as key
{items.map((item, index) => <Item key={index} data={item} />)}

// Bad - random key
{items.map(item => <Item key={Math.random()} data={item} />)}

// Good - stable unique key
{items.map(item => <Item key={item.id} data={item} />)}
```

### 47. Explain React's render props pattern vs hooks.

**Answer:**
**Render Props:**
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
<Mouse render={({ x, y }) => <p>Position: {x}, {y}</p>} />
```

**Hooks (Preferred):**
```jsx
function useMouse() {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    
    useEffect(() => {
        const handleMouseMove = (e) => {
            setPosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);
    
    return position;
}

// Usage
function Component() {
    const { x, y } = useMouse();
    return <p>Position: {x}, {y}</p>;
}
```

**When to use:**
- Hooks: Preferred for most cases
- Render Props: When you need flexibility in rendering

### 48. Explain React's compound components pattern.

**Answer:**
Compound components work together to form complete UI.

```jsx
function Tabs({ children }) {
    const [activeIndex, setActiveIndex] = useState(0);
    
    return (
        <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
            {children}
        </TabsContext.Provider>
    );
}

function TabList({ children }) {
    return <div className="tab-list">{children}</div>;
}

function Tab({ index, children }) {
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

function TabPanels({ children }) {
    const { activeIndex } = useContext(TabsContext);
    return <div>{children[activeIndex]}</div>;
}

function TabPanel({ children }) {
    return <div>{children}</div>;
}

// Usage
<Tabs>
    <TabList>
        <Tab index={0}>Tab 1</Tab>
        <Tab index={1}>Tab 2</Tab>
    </TabList>
    <TabPanels>
        <TabPanel>Content 1</TabPanel>
        <TabPanel>Content 2</TabPanel>
    </TabPanels>
</Tabs>
```

### 49. Explain React's controlled vs uncontrolled components in detail.

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
        <>
            <input ref={inputRef} type="text" />
            <button onClick={handleSubmit}>Submit</button>
        </>
    );
}
```

**When to use:**
- Controlled: Most cases, need validation, form libraries
- Uncontrolled: Simple forms, file inputs, third-party libraries

### 50. Explain React's error boundaries in detail.

**Answer:**
Error boundaries catch JavaScript errors in component tree.

```jsx
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }
    
    componentDidCatch(error, errorInfo) {
        // Log to error reporting service
        console.error('Error:', error, errorInfo);
    }
    
    render() {
        if (this.state.hasError) {
            return (
                <div>
                    <h2>Something went wrong</h2>
                    <button onClick={() => this.setState({ hasError: false })}>
                        Try again
                    </button>
                </div>
            );
        }
        return this.props.children;
    }
}

// Usage
<ErrorBoundary>
    <App />
</ErrorBoundary>
```

**Limitations:**
- Doesn't catch errors in event handlers
- Doesn't catch errors in async code
- Doesn't catch errors during SSR

### 51. Explain React's Suspense and lazy loading.

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

**Multiple Suspense Boundaries:**
```jsx
function App() {
    return (
        <Suspense fallback={<div>Loading app...</div>}>
            <Header />
            <Suspense fallback={<div>Loading content...</div>}>
                <Content />
            </Suspense>
        </Suspense>
    );
}
```

**Benefits:**
- Smaller initial bundle
- Faster initial load
- Load code on demand

### 52. Explain React's reconciliation algorithm in detail.

**Answer:**
**Diffing Algorithm:**
1. Elements of different types: Tear down old, build new
2. Same DOM element: Update changed attributes
3. Component elements: Update props, re-render if needed
4. List items: Use keys for efficient updates

**Example:**
```jsx
// Different types - full replacement
<div>
    <Counter />
</div>
// Changes to
<span>
    <Counter />
</span>
// Counter unmounts and remounts

// Same type - update attributes
<div className="before" />
// Changes to
<div className="after" />
// Only className updated

// List with keys
<ul>
    <li key="a">A</li>
    <li key="b">B</li>
</ul>
// Changes to
<ul>
    <li key="b">B</li>
    <li key="a">A</li>
</ul>
// Only reordered, not recreated
```

### 53. Explain React's performance optimization techniques.

**Answer:**
**1. React.memo:**
```jsx
const ExpensiveComponent = React.memo(({ data }) => {
    return <div>{data}</div>;
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data;
});
```

**2. useMemo:**
```jsx
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]);
```

**3. useCallback:**
```jsx
const handleClick = useCallback(() => {
    doSomething(id);
}, [id]);
```

**4. Code Splitting:**
```jsx
const LazyComponent = React.lazy(() => import('./LazyComponent'));
```

**5. Virtualization:**
```jsx
import { FixedSizeList } from 'react-window';

function List({ items }) {
    return (
        <FixedSizeList
            height={600}
            itemCount={items.length}
            itemSize={50}
        >
            {({ index, style }) => (
                <div style={style}>{items[index]}</div>
            )}
        </FixedSizeList>
    );
}
```

### 54. Explain React's Server Components (RSC) in detail.

**Answer:**
Server Components render on server, reducing client bundle.

**Server Component:**
```jsx
// app/users/page.js (Server Component)
async function UsersPage() {
    const users = await fetchUsers(); // Runs on server
    
    return (
        <div>
            {users.map(user => (
                <UserCard key={user.id} user={user} />
            ))}
        </div>
    );
}
```

**Client Component:**
```jsx
'use client'; // Directive for Client Component

import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Benefits:**
- Smaller client bundle
- Direct database access
- Better security (API keys on server)
- Improved performance

### 55. Explain React's testing best practices.

**Answer:**
**Unit Testing:**
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('renders button and handles click', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
});
```

**Testing Hooks:**
```jsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

test('increments counter', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
        result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
});
```

**Best Practices:**
- Test user behavior, not implementation
- Use data-testid sparingly
- Test accessibility
- Mock external dependencies

### 56. Explain React's Fragment and when to use it.

**Answer:**
Fragment allows grouping elements without adding extra DOM node.

```jsx
// Without Fragment
function Component() {
    return (
        <div>
            <h1>Title</h1>
            <p>Content</p>
        </div>
    );
}

// With Fragment
function Component() {
    return (
        <>
            <h1>Title</h1>
            <p>Content</p>
        </>
    );
}

// Or
function Component() {
    return (
        <React.Fragment>
            <h1>Title</h1>
            <p>Content</p>
        </React.Fragment>
    );
}
```

**When to use:**
- Group elements without wrapper
- Return multiple elements
- Avoid unnecessary DOM nodes

### 57. Explain React's defaultProps and propTypes.

**Answer:**
**defaultProps:**
```jsx
function Component({ name, age }) {
    return <div>{name} is {age} years old</div>;
}

Component.defaultProps = {
    name: 'Anonymous',
    age: 0
};
```

**propTypes:**
```jsx
import PropTypes from 'prop-types';

function Component({ name, age, email }) {
    return <div>{name}</div>;
}

Component.propTypes = {
    name: PropTypes.string.isRequired,
    age: PropTypes.number,
    email: PropTypes.string
};
```

**Note:** In modern React, use default parameters and TypeScript instead.

### 58. Explain React's children prop.

**Answer:**
`children` prop allows passing components as data.

```jsx
function Container({ children }) {
    return <div className="container">{children}</div>;
}

// Usage
<Container>
    <h1>Title</h1>
    <p>Content</p>
</Container>
```

**Multiple Children:**
```jsx
function Layout({ header, sidebar, content }) {
    return (
        <div>
            {header}
            <div>
                {sidebar}
                {content}
            </div>
        </div>
    );
}

// Usage
<Layout
    header={<Header />}
    sidebar={<Sidebar />}
    content={<Content />}
/>
```

### 59. Explain React's useReducer for complex state.

**Answer:**
useReducer manages complex state logic.

```jsx
function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        case 'reset':
            return { count: 0 };
        default:
            return state;
    }
}

function Counter() {
    const [state, dispatch] = useReducer(reducer, { count: 0 });
    
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

**When to use:**
- Complex state logic
- Multiple sub-values
- State updates depend on previous state

### 60. Explain React's useLayoutEffect vs useEffect.

**Answer:**
**useEffect:**
- Runs after render and paint
- Asynchronous
- Good for: API calls, subscriptions, side effects

**useLayoutEffect:**
- Runs after render but before paint
- Synchronous
- Good for: DOM measurements, preventing flicker

```jsx
function Component() {
    const [width, setWidth] = useState(0);
    const ref = useRef();
    
    useLayoutEffect(() => {
        // Measure before paint
        setWidth(ref.current.offsetWidth);
    }, []);
    
    return <div ref={ref}>Content</div>;
}
```

### 61. Explain React's custom hooks best practices.

**Answer:**
**Naming:**
- Always start with `use`
- Descriptive names

**Single Responsibility:**
```jsx
// Good - focused hook
function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);
    const increment = () => setCount(count + 1);
    const decrement = () => setCount(count - 1);
    return { count, increment, decrement };
}

// Bad - does too much
function useCounterAndTimer(initialValue) {
    // Counter logic
    // Timer logic
    // Too many responsibilities
}
```

**Return Consistent Structure:**
```jsx
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

### 62. Explain React's prop drilling and solutions.

**Answer:**
**Problem:**
```jsx
function App() {
    const user = { name: 'John' };
    return <ComponentA user={user} />;
}

function ComponentA({ user }) {
    return <ComponentB user={user} />;
}

function ComponentB({ user }) {
    return <ComponentC user={user} />;
}
```

**Solutions:**
1. **Context API:**
```jsx
const UserContext = createContext();

function App() {
    return (
        <UserContext.Provider value={{ name: 'John' }}>
            <ComponentA />
        </UserContext.Provider>
    );
}

function ComponentC() {
    const user = useContext(UserContext);
    return <div>{user.name}</div>;
}
```

2. **Composition:**
```jsx
function App() {
    return <ComponentA><ComponentC /></ComponentA>;
}
```

### 63. Explain React's state lifting.

**Answer:**
Lifting state moves state to common ancestor.

```jsx
// Before - state in child
function TemperatureInput() {
    const [temperature, setTemperature] = useState('');
    return <input value={temperature} onChange={e => setTemperature(e.target.value)} />;
}

// After - state lifted to parent
function Calculator() {
    const [temperature, setTemperature] = useState('');
    
    return (
        <div>
            <TemperatureInput value={temperature} onChange={setTemperature} />
            <TemperatureDisplay temperature={temperature} />
        </div>
    );
}
```

### 64. Explain React's controlled components pattern.

**Answer:**
Controlled components have React control their value.

```jsx
function Form() {
    const [formData, setFormData] = useState({
        name: '',
        email: ''
    });
    
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    
    return (
        <form>
            <input
                name="name"
                value={formData.name}
                onChange={handleChange}
            />
            <input
                name="email"
                value={formData.email}
                onChange={handleChange}
            />
        </form>
    );
}
```

### 65. Explain React's form handling.

**Answer:**
**Controlled Form:**
```jsx
function Form() {
    const [name, setName] = useState('');
    
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(name);
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input value={name} onChange={e => setName(e.target.value)} />
            <button type="submit">Submit</button>
        </form>
    );
}
```

**Uncontrolled Form:**
```jsx
function Form() {
    const formRef = useRef();
    
    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData(formRef.current);
        console.log(formData.get('name'));
    };
    
    return (
        <form ref={formRef} onSubmit={handleSubmit}>
            <input name="name" />
            <button type="submit">Submit</button>
        </form>
    );
}
```

### 66. Explain React's event handling.

**Answer:**
**Synthetic Events:**
```jsx
function Button() {
    const handleClick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('Clicked');
    };
    
    return <button onClick={handleClick}>Click me</button>;
}
```

**Event Pooling (React < 17):**
```jsx
// Event object reused, need to persist
function handleClick(e) {
    e.persist(); // React < 17
    setTimeout(() => {
        console.log(e.type);
    }, 100);
}
```

**Passing Arguments:**
```jsx
function List({ items }) {
    const handleClick = (id) => {
        console.log('Clicked:', id);
    };
    
    return (
        <ul>
            {items.map(item => (
                <li key={item.id} onClick={() => handleClick(item.id)}>
                    {item.name}
                </li>
            ))}
        </ul>
    );
}
```

### 67. Explain React's conditional rendering.

**Answer:**
**If Statement:**
```jsx
function Component({ isLoggedIn }) {
    if (isLoggedIn) {
        return <Dashboard />;
    }
    return <Login />;
}
```

**Ternary Operator:**
```jsx
function Component({ isLoggedIn }) {
    return (
        <div>
            {isLoggedIn ? <Dashboard /> : <Login />}
        </div>
    );
}
```

**Logical AND:**
```jsx
function Component({ items }) {
    return (
        <div>
            {items.length > 0 && <ItemList items={items} />}
        </div>
    );
}
```

**Immediately Invoked Function:**
```jsx
function Component({ user }) {
    return (
        <div>
            {(() => {
                if (user.role === 'admin') return <AdminPanel />;
                if (user.role === 'user') return <UserPanel />;
                return <GuestPanel />;
            })()}
        </div>
    );
}
```

### 68. Explain React's list rendering and keys.

**Answer:**
**Basic List:**
```jsx
function List({ items }) {
    return (
        <ul>
            {items.map(item => (
                <li key={item.id}>{item.name}</li>
            ))}
        </ul>
    );
}
```

**Keys Must Be:**
- Unique among siblings
- Stable across renders
- Predictable

**Common Mistakes:**
```jsx
// Bad - index as key (if list can reorder)
{items.map((item, index) => <Item key={index} data={item} />)}

// Bad - random key
{items.map(item => <Item key={Math.random()} data={item} />)}

// Good - stable unique key
{items.map(item => <Item key={item.id} data={item} />)}
```

### 69. Explain React's component composition.

**Answer:**
Composition builds complex UIs from simple components.

**Containment:**
```jsx
function Container({ children }) {
    return <div className="container">{children}</div>;
}

function App() {
    return (
        <Container>
            <Header />
            <Content />
        </Container>
    );
}
```

**Specialization:**
```jsx
function Dialog({ title, children }) {
    return (
        <div className="dialog">
            <h1>{title}</h1>
            {children}
        </div>
    );
}

function WelcomeDialog() {
    return (
        <Dialog title="Welcome">
            <p>Thank you for visiting!</p>
        </Dialog>
    );
}
```

### 70. Explain React's higher-order components (HOCs).

**Answer:**
HOC is function that takes component and returns new component.

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

<UserProfileWithLoading isLoading={true} user={user} />
```

**Common HOCs:**
- `withRouter` (React Router)
- `connect` (Redux)
- `withAuth` (Authentication)

**Modern Alternative:** Use hooks instead of HOCs.

### 71. Explain React's ref forwarding with useImperativeHandle.

**Answer:**
```jsx
const FancyInput = forwardRef((props, ref) => {
    const inputRef = useRef();
    
    useImperativeHandle(ref, () => ({
        focus: () => inputRef.current.focus(),
        blur: () => inputRef.current.blur(),
        getValue: () => inputRef.current.value,
        setValue: (value) => { inputRef.current.value = value; }
    }));
    
    return <input ref={inputRef} {...props} />;
});

// Usage
function Parent() {
    const inputRef = useRef();
    
    const handleFocus = () => {
        inputRef.current.focus();
    };
    
    return (
        <>
            <FancyInput ref={inputRef} />
            <button onClick={handleFocus}>Focus Input</button>
        </>
    );
}
```

### 72. Explain React's useCallback vs useMemo.

**Answer:**
**useCallback - Memoize functions:**
```jsx
const handleClick = useCallback(() => {
    doSomething(id);
}, [id]); // Function recreated only if id changes
```

**useMemo - Memoize values:**
```jsx
const expensiveValue = useMemo(() => {
    return computeExpensiveValue(a, b);
}, [a, b]); // Value recomputed only if a or b changes
```

**When to use:**
- `useCallback`: Memoize functions passed as props
- `useMemo`: Memoize expensive computations

### 73. Explain React's Context API performance considerations.

**Answer:**
**Problem:**
```jsx
// All consumers re-render when context value changes
const ThemeContext = createContext();

function App() {
    const [theme, setTheme] = useState('light');
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Component />
        </ThemeContext.Provider>
    );
}
```

**Solution - Split contexts:**
```jsx
const ThemeContext = createContext();
const ThemeUpdateContext = createContext();

function App() {
    const [theme, setTheme] = useState('light');
    return (
        <ThemeContext.Provider value={theme}>
            <ThemeUpdateContext.Provider value={setTheme}>
                <Component />
            </ThemeUpdateContext.Provider>
        </ThemeContext.Provider>
    );
}
```

### 74. Explain React's error boundaries with hooks.

**Answer:**
Error boundaries must be class components, but you can use hooks inside:

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
            return <ErrorFallback />;
        }
        return this.props.children;
    }
}

// Use with hooks components
<ErrorBoundary>
    <ComponentWithHooks />
</ErrorBoundary>
```

### 75. Explain React's Portal usage.

**Answer:**
Render children into DOM node outside parent hierarchy.

```jsx
import { createPortal } from 'react-dom';

function Modal({ children, isOpen }) {
    if (!isOpen) return null;
    
    return createPortal(
        <div className="modal">
            {children}
        </div>,
        document.body
    );
}

// Usage
function App() {
    return (
        <div>
            <Modal isOpen={true}>
                <h1>Modal Content</h1>
            </Modal>
        </div>
    );
}
```

**Benefits:**
- Render outside parent DOM
- Useful for modals, tooltips
- Event bubbling still works

### 76. Explain React's Profiler API.

**Answer:**
Measure component render performance.

```jsx
import { Profiler } from 'react';

function onRenderCallback(id, phase, actualDuration) {
    console.log('Component:', id);
    console.log('Phase:', phase); // mount or update
    console.log('Duration:', actualDuration);
}

function App() {
    return (
        <Profiler id="App" onRender={onRenderCallback}>
            <Component />
        </Profiler>
    );
}
```

### 77. Explain React's Concurrent Mode features.

**Answer:**
**useTransition:**
```jsx
const [isPending, startTransition] = useTransition();

const handleClick = () => {
    startTransition(() => {
        setCount(count + 1); // Non-urgent update
    });
};
```

**useDeferredValue:**
```jsx
const deferredQuery = useDeferredValue(query);
```

**Benefits:**
- Keep UI responsive
- Prioritize urgent updates
- Better user experience

### 78. Explain React's Server Components vs Client Components.

**Answer:**
**Server Component (Default):**
```jsx
// app/users/page.js
async function UsersPage() {
    const users = await fetchUsers(); // Runs on server
    
    return (
        <div>
            {users.map(user => <UserCard key={user.id} user={user} />)}
        </div>
    );
}
```

**Client Component:**
```jsx
'use client';

import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### 79. Explain React's Suspense boundaries.

**Answer:**
**Basic:**
```jsx
<Suspense fallback={<Loading />}>
    <LazyComponent />
</Suspense>
```

**Multiple boundaries:**
```jsx
<Suspense fallback={<HeaderSkeleton />}>
    <Header />
    <Suspense fallback={<ContentSkeleton />}>
        <Content />
    </Suspense>
</Suspense>
```

**Error boundaries with Suspense:**
```jsx
<ErrorBoundary>
    <Suspense fallback={<Loading />}>
        <Component />
    </Suspense>
</ErrorBoundary>
```

### 80. Explain React's testing with React Testing Library.

**Answer:**
**Basic test:**
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('renders button and handles click', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
});
```

**Async testing:**
```jsx
test('loads data', async () => {
    render(<DataComponent />);
    
    const data = await screen.findByText('Data loaded');
    expect(data).toBeInTheDocument();
});
```

---

This covers React interview questions from beginner to advanced level with detailed explanations and code examples.

