# React & Next.js — Complete Reference Guide (Zero to Advanced)

> This guide assumes zero knowledge of React or Next.js but assumes you've read the JavaScript and TypeScript guides. Every concept is explained from first principles, with deep implementation details, TypeScript integration, and production-grade patterns.

---

## Table of Contents

1. [What is React and Why Does it Exist?](#1-what-is-react-and-why-does-it-exist)
2. [JSX — What It Really Is](#2-jsx--what-it-really-is)
3. [Components — The Building Block](#3-components--the-building-block)
4. [Props — Passing Data Down](#4-props--passing-data-down)
5. [State — Data That Changes](#5-state--data-that-changes)
6. [The Virtual DOM & Reconciliation](#6-the-virtual-dom--reconciliation)
7. [useState — Complete Guide](#7-usestate--complete-guide)
8. [useEffect — Complete Guide](#8-useeffect--complete-guide)
9. [useRef — Complete Guide](#9-useref--complete-guide)
10. [useMemo & useCallback — Complete Guide](#10-usememo--usecallback--complete-guide)
11. [useReducer — Complete Guide](#11-usereducer--complete-guide)
12. [useContext — Complete Guide](#12-usecontext--complete-guide)
13. [Custom Hooks — Patterns & Best Practices](#13-custom-hooks--patterns--best-practices)
14. [React 18 & 19 — New Hooks & Concurrent Features](#14-react-18--19--new-hooks--concurrent-features)
15. [Component Patterns](#15-component-patterns)
16. [Performance Optimization](#16-performance-optimization)
17. [Forms in React](#17-forms-in-react)
18. [Error Boundaries](#18-error-boundaries)
19. [Portals & Advanced DOM Control](#19-portals--advanced-dom-control)
20. [State Management — Beyond useState](#20-state-management--beyond-usestate)
21. [Data Fetching Patterns](#21-data-fetching-patterns)
22. [Testing React Components](#22-testing-react-components)
23. [What is Next.js?](#23-what-is-nextjs)
24. [Next.js App Router — Architecture](#24-nextjs-app-router--architecture)
25. [Server Components vs Client Components](#25-server-components-vs-client-components)
26. [Routing in the App Router](#26-routing-in-the-app-router)
27. [Layouts, Templates & Special Files](#27-layouts-templates--special-files)
28. [Data Fetching in Next.js](#28-data-fetching-in-nextjs)
29. [Caching in Next.js](#29-caching-in-nextjs)
30. [Server Actions](#30-server-actions)
31. [API Routes (Route Handlers)](#31-api-routes-route-handlers)
32. [Middleware](#32-middleware)
33. [Image, Font & Script Optimization](#33-image-font--script-optimization)
34. [Authentication Patterns](#34-authentication-patterns)
35. [Streaming & Suspense in Next.js](#35-streaming--suspense-in-nextjs)
36. [Deploying Next.js](#36-deploying-nextjs)

---

## 1. What is React and Why Does it Exist?

### The Problem Before React

Before React (and before libraries like it), building dynamic UIs meant manually manipulating the DOM with JavaScript. Here's what that looked like:

```javascript
// Old-school DOM manipulation — painful at scale
function addUser(user) {
  const li = document.createElement("li");
  li.textContent = user.name;
  li.setAttribute("data-id", user.id);
  li.addEventListener("click", function() {
    // do something with user.id
  });
  document.querySelector("#user-list").appendChild(li);
}

function removeUser(userId) {
  const el = document.querySelector(`[data-id="${userId}"]`);
  if (el) el.parentNode.removeChild(el);
}

function updateUser(user) {
  const el = document.querySelector(`[data-id="${user.id}"]`);
  if (el) {
    el.textContent = user.name;
    // what if the structure changed? what if there are children?
    // you'd need to manually handle every possible case
  }
}
```

**Problems with this approach:**
- **Imperative** — you say HOW to change the DOM, not WHAT the UI should look like
- **Fragile** — changing data structure means updating DOM manipulation code everywhere
- **State drift** — the UI state (what's displayed) and the application state (your data) can get out of sync
- **Hard to scale** — 10 engineers working on the same DOM is a nightmare
- **Hard to test** — DOM manipulation logic is deeply tangled with business logic

### What React Does Differently

React introduces a **declarative** model:

```
Instead of:
  "When a user is added, CREATE a list item and APPEND it to the list"
  "When a user is removed, FIND the item and REMOVE it from the list"

You say:
  "The UI is ALWAYS a function of the current state"
  "When state changes, React figures out what DOM changes are needed"
```

**React's Core Philosophy:**

```
UI = f(state)

Your component is a FUNCTION that receives state (via props) and returns
what the UI should look like RIGHT NOW. React handles translating that
description into real DOM operations.
```

**React's Key Ideas:**

1. **Declarative UI** — describe WHAT the UI looks like, not HOW to change it
2. **Components** — reusable, self-contained pieces of UI that own their state and rendering
3. **Unidirectional data flow** — data flows DOWN (parent → child via props), events flow UP (child → parent via callbacks)
4. **Virtual DOM** — React keeps an in-memory representation of the UI to compute minimal DOM changes
5. **Composition** — build complex UIs by combining simple components

### React in the Ecosystem

```
React = just the UI library (rendering components)
React DOM = connects React to the browser DOM
React Native = connects React to native mobile UI

Next.js = a FRAMEWORK built on top of React that adds:
  - File-based routing
  - Server-side rendering (SSR)
  - Static site generation (SSG)
  - API routes / route handlers
  - Server Components (render on server, send HTML)
  - Server Actions (server-side mutation functions)
  - Image optimization, font optimization, etc.
```

---

## 2. JSX — What It Really Is

JSX is **JavaScript XML** — a syntax extension that looks like HTML but is actually JavaScript.

### JSX is Syntactic Sugar

```tsx
// What you write (JSX):
const element = <h1 className="title">Hello, {name}!</h1>;

// What the compiler transforms it to:
const element = React.createElement(
  "h1",                        // element type (string for HTML, component for React)
  { className: "title" },      // props object
  `Hello, ${name}!`            // children
);

// React.createElement returns a plain JavaScript OBJECT (a "React element"):
// {
//   type: "h1",
//   props: {
//     className: "title",
//     children: "Hello, Alice!"
//   },
//   key: null,
//   ref: null,
//   $$typeof: Symbol(react.element)  // for security
// }
```

### JSX with Nested Children

```tsx
// JSX:
const card = (
  <div className="card">
    <h2>Title</h2>
    <p>Content</p>
  </div>
);

// Compiled to:
const card = React.createElement(
  "div",
  { className: "card" },
  React.createElement("h2", null, "Title"),
  React.createElement("p", null, "Content")
);

// Modern React (17+) uses a new JSX transform — you no longer need
// 'import React from "react"' in every file:
import { jsx as _jsx } from "react/jsx-runtime";
const card = _jsx("div", {
  className: "card",
  children: [_jsx("h2", { children: "Title" }), _jsx("p", { children: "Content" })]
});
```

### JSX Rules — Every One Explained

```tsx
// RULE 1: Must have one root element — OR use a Fragment
// ERROR:
function Component() {
  return (
    <h1>Title</h1>
    <p>Content</p>  // Cannot have sibling elements without a parent
  );
}

// OK: wrap in a div
function Component() {
  return (
    <div>
      <h1>Title</h1>
      <p>Content</p>
    </div>
  );
}

// BETTER: use Fragment — renders no DOM element
function Component() {
  return (
    <>
      <h1>Title</h1>
      <p>Content</p>
    </>
  );
}

// Fragment with key (for lists):
items.map(item => (
  <React.Fragment key={item.id}>
    <dt>{item.name}</dt>
    <dd>{item.value}</dd>
  </React.Fragment>
));

// RULE 2: HTML attributes use camelCase (and some are renamed)
<div className="card">          {/* class → className */}
<label htmlFor="email">         {/* for → htmlFor */}
<input onChange={handler}>      {/* onchange → onChange */}
<input tabIndex={0}>            {/* tabindex → tabIndex */}
<div style={{ color: "red", fontSize: "16px" }}>  {/* style takes object with camelCase */}

// RULE 3: Curly braces for JavaScript expressions
const name = "Alice";
const isAdmin = true;
<h1>{name}</h1>                        {/* string variable */}
<p>{2 + 2}</p>                          {/* expression: renders "4" */}
<p>{name.toUpperCase()}</p>             {/* method call */}
<p>{isAdmin ? "Admin" : "User"}</p>     {/* ternary */}
<div>{isAdmin && <AdminPanel />}</div>  {/* short-circuit rendering */}

// RULE 4: null, undefined, false, true render NOTHING
// Useful for conditional rendering:
{isLoggedIn && <UserMenu />}   // renders UserMenu only if isLoggedIn is true
{error && <ErrorMessage error={error} />}  // renders only if error is truthy

// CAREFUL: 0 IS rendered! (it's a valid number)
{items.length && <List items={items} />}  // BUG: renders "0" when empty!
{items.length > 0 && <List items={items} />}  // FIXED

// RULE 5: Self-closing tags must close
<img src="photo.jpg" />    // OK
<br />                      // OK
<Input />                   // OK (custom component)
// <img src="photo.jpg">   // Error — must self-close in JSX

// RULE 6: String literals vs expressions
<Button label="Click me" />     // string literal
<Button count={42} />           // number — must use {}
<Button active={true} />        // boolean — must use {}
<Button active />               // shorthand: same as active={true}
<Button style={{ color: "red" }} />  // object — double braces: outer = JSX, inner = object
```

---

## 3. Components — The Building Block

A component is a **function** that takes props and returns JSX (what to render).

### Function Components

```tsx
// Simplest component
function Greeting() {
  return <h1>Hello, World!</h1>;
}

// With TypeScript props
interface UserCardProps {
  name: string;
  email: string;
  role?: "admin" | "user";          // optional
  onClick: (id: string) => void;   // callback prop
}

function UserCard({ name, email, role = "user", onClick }: UserCardProps) {
  return (
    <div className="user-card">
      <h2>{name}</h2>
      <p>{email}</p>
      <span className={`badge badge-${role}`}>{role}</span>
      <button onClick={() => onClick(email)}>Select</button>
    </div>
  );
}

// Usage
<UserCard
  name="Alice"
  email="alice@example.com"
  role="admin"
  onClick={(email) => console.log(`Selected: ${email}`)}
/>
```

### Component Return Types with TypeScript

```tsx
// Modern React — use React.JSX.Element (or JSX.Element)
function Button(): React.JSX.Element {
  return <button>Click</button>;
}

// Can also return null (renders nothing)
function ConditionalComponent({ show }: { show: boolean }): React.JSX.Element | null {
  if (!show) return null;
  return <div>Visible!</div>;
}

// React.ReactNode — the most permissive return type
// (string, number, JSX, null, undefined, boolean, arrays, fragments)
function FlexibleComponent(): React.ReactNode {
  return "Just a string"; // valid!
}

// React.FC<Props> — older pattern, avoid in modern code
// It implicitly adds children to props (which React 18 removed)
// Prefer explicit function component signature
```

### The Children Prop

```tsx
// children is a special prop — represents content between opening and closing tags
interface CardProps {
  title: string;
  children: React.ReactNode;  // anything React can render
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <div className="card-header"><h2>{title}</h2></div>
      <div className="card-body">{children}</div>  {/* renders whatever is between <Card> tags */}
    </div>
  );
}

// Usage:
<Card title="User Profile">
  <UserAvatar />           {/* these become the children prop */}
  <p>Alice — Admin</p>
</Card>

// Children can be anything:
<Card title="Numbers">42</Card>
<Card title="Empty"></Card>

// Working with children programmatically
import { Children, cloneElement, isValidElement } from "react";

function RadioGroup({ children, name }: { children: React.ReactNode; name: string }) {
  return (
    <div role="radiogroup">
      {Children.map(children, (child) => {
        if (!isValidElement(child)) return child;
        // Inject 'name' prop into each child
        return cloneElement(child as React.ReactElement, { name });
      })}
    </div>
  );
}
```

### Component Composition Patterns

```tsx
// 1. Render Props — pass a function as a prop that returns JSX
interface DataLoaderProps<T> {
  url: string;
  render: (data: T, loading: boolean, error: Error | null) => React.ReactNode;
}

function DataLoader<T>({ url, render }: DataLoaderProps<T>) {
  const { data, loading, error } = useFetch<T>(url);
  return <>{render(data as T, loading, error)}</>;
}

<DataLoader
  url="/api/users"
  render={(users: User[], loading, error) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    return <UserList users={users} />;
  }}
/>

// 2. Slots pattern — named content areas
interface LayoutProps {
  header: React.ReactNode;
  sidebar: React.ReactNode;
  content: React.ReactNode;
  footer?: React.ReactNode;
}

function AppLayout({ header, sidebar, content, footer }: LayoutProps) {
  return (
    <div className="layout">
      <header>{header}</header>
      <div className="main">
        <aside>{sidebar}</aside>
        <main>{content}</main>
      </div>
      {footer && <footer>{footer}</footer>}
    </div>
  );
}

<AppLayout
  header={<NavBar />}
  sidebar={<NavigationMenu />}
  content={<ProductList />}
  footer={<Footer />}
/>

// 3. Compound Components — components that work together
// Like <select> and <option> in HTML

interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}
const TabsContext = React.createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext)!;
  return (
    <button
      role="tab"
      aria-selected={ctx.activeTab === id}
      onClick={() => ctx.setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext)!;
  if (ctx.activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach as properties for discoverable API
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage — reads like natural HTML
<Tabs defaultTab="users">
  <Tabs.List>
    <Tabs.Tab id="users">Users</Tabs.Tab>
    <Tabs.Tab id="orders">Orders</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="users"><UserList /></Tabs.Panel>
  <Tabs.Panel id="orders"><OrderList /></Tabs.Panel>
</Tabs>
```

---

## 4. Props — Passing Data Down

Props (properties) are how components receive data from their parent. They flow in ONE direction: parent → child.

```tsx
// Props are READ-ONLY — never mutate props
function Component({ count }: { count: number }) {
  // count = 5; // ERROR — props are immutable
  return <p>{count}</p>;
}

// All data types as props
interface AllPropTypes {
  // Primitives
  text: string;
  count: number;
  active: boolean;
  nothing: null;

  // Objects and arrays
  user: { id: string; name: string };
  items: string[];
  matrix: number[][];

  // Functions (callbacks)
  onClick: () => void;
  onChange: (value: string) => void;
  onSelect: (item: User) => void;

  // React types
  children: React.ReactNode;
  icon: React.ReactElement;          // a specific React element (not null, not strings)
  renderItem: (item: User) => React.ReactNode; // render prop

  // Optional
  className?: string;
  style?: React.CSSProperties;

  // Forwarded ref
  ref?: React.Ref<HTMLButtonElement>;

  // Event handlers from HTML — matches DOM event types
  onMouseEnter?: React.MouseEventHandler<HTMLDivElement>;
  onKeyDown?: React.KeyboardEventHandler<HTMLInputElement>;
  onFocus?: React.FocusEventHandler<HTMLElement>;
}

// Extending native HTML element props — common pattern for wrapper components
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
  isLoading?: boolean;
}

function Button({ variant = "primary", isLoading, children, ...rest }: ButtonProps) {
  return (
    <button
      {...rest}                            // spread all native button props
      className={`btn btn-${variant} ${rest.className ?? ""}`}
      disabled={isLoading || rest.disabled}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}
// Now Button accepts ALL standard button props PLUS our custom ones:
<Button onClick={() => {}} type="submit" variant="primary" disabled={false}>
  Submit
</Button>
```

### Prop Drilling Problem

```tsx
// When you pass props many levels deep — "prop drilling"
function App() {
  const [user, setUser] = useState<User | null>(null);
  return <Layout user={user} onLogout={() => setUser(null)} />;
}
function Layout({ user, onLogout }: { user: User | null; onLogout: () => void }) {
  return (
    <div>
      <Header user={user} onLogout={onLogout} /> {/* just passing through! */}
      <main>...</main>
    </div>
  );
}
function Header({ user, onLogout }: { user: User | null; onLogout: () => void }) {
  return (
    <nav>
      <UserMenu user={user} onLogout={onLogout} /> {/* still passing through! */}
    </nav>
  );
}
function UserMenu({ user, onLogout }: { user: User | null; onLogout: () => void }) {
  // FINALLY uses the props
  return user ? <button onClick={onLogout}>{user.name}</button> : null;
}

// Solutions:
// 1. Context API (for global-ish state like auth, theme)
// 2. State management (Zustand, Redux)
// 3. Component composition (pass components as props, not data)
// 4. Lift state down (move state closer to where it's used)
```

---

## 5. State — Data That Changes

State is data that can change over time and causes the component to re-render when it does.

### Why useState (Not Regular Variables)?

```tsx
// WRONG — regular variables don't trigger re-render
function Counter() {
  let count = 0; // this resets to 0 on every render!

  function increment() {
    count++; // this changes the variable...
    // ...but React doesn't know about it, so no re-render happens
  }

  return (
    <div>
      <p>{count}</p>
      <button onClick={increment}>+</button>
    </div>
  );
}

// CORRECT — useState triggers re-render and persists between renders
function Counter() {
  const [count, setCount] = useState(0);
  // React stores count OUTSIDE the component function
  // When setCount is called, React schedules a re-render
  // The new render uses the new count value

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

### State is a Snapshot

This is one of the most important concepts in React:

```tsx
function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    // Each call to setCount schedules a re-render with the given value
    // BUT: the 'count' variable here is the value FROM THIS RENDER — it's a snapshot
    setCount(count + 1); // schedules re-render with count+1
    setCount(count + 1); // schedules re-render with count+1 AGAIN (not count+2!)
    setCount(count + 1); // still count+1! All three read the same snapshot

    // After this event handler: React does ONE render with count = 1 (not 3)
  }

  // FIX: use functional updates — they receive the LATEST state as argument
  function handleClickFixed() {
    setCount(prev => prev + 1); // prev = latest count
    setCount(prev => prev + 1); // prev = latest count + 1
    setCount(prev => prev + 1); // prev = latest count + 2
    // After this: React renders with count = 3
  }

  return <button onClick={handleClick}>{count}</button>;
}
```

---

## 6. The Virtual DOM & Reconciliation

### What the Virtual DOM Is

The "Virtual DOM" is a JavaScript object tree that mirrors the structure of the real DOM. It's cheap to create and manipulate because it's just JavaScript objects — no actual browser DOM operations.

```
Real DOM Operation (expensive):
  document.createElement("div")  → triggers layout, paint, composite
  element.appendChild(child)     → triggers reflow
  element.style.color = "red"    → triggers repaint

Virtual DOM Operation (cheap):
  { type: "div", props: { style: { color: "red" } }, children: [...] }
  → just a JavaScript object creation
```

### The Reconciliation Algorithm

When state or props change, React:

1. **Renders** — calls your component function to get the new React element tree
2. **Diffs** — compares new tree vs previous tree (the "diffing" or "reconciliation" algorithm)
3. **Commits** — applies the minimal set of changes to the real DOM

```
Diffing Rules:

Rule 1: Different element TYPE → unmount old, mount new
  Old: <div>          New: <span>
  React destroys the div subtree entirely and creates a new span subtree
  This is expensive — avoid changing element types unnecessarily

Rule 2: Same element type → update changed props only
  Old: <div className="card active">
  New: <div className="card">
  React keeps the DOM node, just removes "active" class

Rule 3: Same component type → update props, re-render
  Old: <UserCard user={alice} />
  New: <UserCard user={bob} />
  React keeps the UserCard component instance, updates props, calls function again

Rule 4: Lists — use 'key' prop
  Without key: React compares by position (index 0 = index 0, etc.)
  With key: React matches by key — correctly handles reordering
```

### Why Keys Matter So Much

```tsx
// Scenario: user reorders a list or removes items from the middle

// WITHOUT KEYS — React uses index
const items = ["apple", "banana", "cherry"];
// Renders: <li>apple (index 0)</li>, <li>banana (index 1)</li>, <li>cherry (index 2)</li>

// Remove "banana" → items = ["apple", "cherry"]
// React diffs: index 0: apple (unchanged), index 1: cherry (was banana — UPDATES TEXT)
// React sees 2 items now (was 3) → removes the LAST one
// This is wrong if the components have their own state (text inputs, checkboxes, etc.)!

// WITH STABLE KEYS — React matches by key
items.map(item => <li key={item.id}>{item.name}</li>)
// React can correctly identify which item was removed/reordered

// NEVER use index as key for mutable lists:
items.map((item, index) => <li key={index}>...</li>)  // OK only for static lists!
// Bad when: items are added/removed/reordered
// Causes: incorrect state, animation bugs, focus loss

// GOOD keys: database IDs, stable unique identifiers
// BAD keys: array index (for dynamic lists), random values (crypto.randomUUID() in render)
```

### React 18: Concurrent Rendering

React 18 introduced concurrent mode — React can:
- **Interrupt** an ongoing render to work on something more urgent
- **Pause** rendering and resume it later
- **Prepare** multiple versions of the UI simultaneously

```tsx
// startTransition — mark state updates as non-urgent
import { useState, startTransition } from "react";

function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  function handleSearch(value: string) {
    setQuery(value); // URGENT — update input immediately

    startTransition(() => {
      // NON-URGENT — can be interrupted if user types again
      const filtered = massiveDataset.filter(item =>
        item.name.includes(value)
      );
      setResults(filtered);
    });
  }

  return (
    <>
      <input value={query} onChange={e => handleSearch(e.target.value)} />
      {/* While results are computing, the old results stay visible */}
      <ResultList results={results} />
    </>
  );
}
```

---

## 7. useState — Complete Guide

```tsx
import { useState } from "react";

// Basic patterns
const [value, setValue] = useState<string>("");
const [count, setCount] = useState(0);           // type inferred as number
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);
const [config, setConfig] = useState({
  theme: "light" as "light" | "dark",
  language: "en",
  notifications: true,
});

// Lazy initialization — function is called ONLY on first render
const [data, setData] = useState(() => {
  // Runs only once — not on every render
  const saved = localStorage.getItem("user-data");
  return saved ? JSON.parse(saved) : { theme: "light" };
});

// Updating objects — MUST create new object (immutability)
setConfig(prev => ({
  ...prev,         // spread existing properties
  theme: "dark",   // override the one that changed
}));
// NEVER DO: config.theme = "dark" — React won't re-render!

// Updating nested objects
const [state, setState] = useState({
  user: {
    profile: {
      name: "Alice",
      avatar: "alice.jpg"
    }
  }
});
// Update deeply nested value — must spread at every level
setState(prev => ({
  ...prev,
  user: {
    ...prev.user,
    profile: {
      ...prev.user.profile,
      name: "Bob"
    }
  }
}));
// For complex nested state, consider useImmer or normalization

// Updating arrays — all immutable operations
const [todos, setTodos] = useState<Todo[]>([]);

// Add item
setTodos(prev => [...prev, { id: Date.now(), text: "New todo", done: false }]);

// Remove item
setTodos(prev => prev.filter(todo => todo.id !== idToRemove));

// Update item
setTodos(prev => prev.map(todo =>
  todo.id === idToUpdate ? { ...todo, done: !todo.done } : todo
));

// Insert at position
setTodos(prev => [
  ...prev.slice(0, index),
  newItem,
  ...prev.slice(index)
]);

// Reorder
setTodos(prev => {
  const arr = [...prev];
  const [moved] = arr.splice(fromIndex, 1);
  arr.splice(toIndex, 0, moved);
  return arr;
});

// State reset — set back to initial value
const initialState = { count: 0, text: "" };
const [state, setState] = useState(initialState);
const resetState = () => setState(initialState);

// Derived state — compute from state instead of storing
const [price, setPrice] = useState(100);
const [quantity, setQuantity] = useState(1);
const total = price * quantity; // derived — not state!
// If you store derived values in state, they can get out of sync

// When NOT to use useState:
// - Constants that never change (use regular const)
// - Values that shouldn't trigger re-render (use useRef)
// - Complex state with many sub-values and inter-dependencies (use useReducer)
// - State shared between many components (use context or state manager)
```

---

## 8. useEffect — Complete Guide

`useEffect` lets you perform **side effects** in function components — things that happen outside of rendering (API calls, subscriptions, DOM manipulation, timers).

### Mental Model

```
useEffect(setup, dependencies?)

setup = a function that runs AFTER the component renders
     = can return a "cleanup" function that runs before the next effect or unmount

dependencies = array of values — the effect re-runs when any of these change
             = [] → run only once (on mount)
             = omitted → run after EVERY render (rarely what you want)
             = [a, b] → run when a or b changes
```

### The Four Cases

```tsx
import { useEffect, useState } from "react";

// CASE 1: No dependency array — runs after EVERY render
useEffect(() => {
  document.title = `Count: ${count}`;
  // Runs after EVERY render — be careful, this can be expensive!
}); // no second argument

// CASE 2: Empty dependency array — runs ONCE (on mount)
useEffect(() => {
  // Think: "when the component appears on the screen"
  const subscription = api.subscribe(handleUpdate);
  
  // Cleanup: return a function that runs when component UNMOUNTS
  return () => {
    subscription.unsubscribe();
  };
}, []); // empty array

// CASE 3: With dependencies — runs when dependencies change
useEffect(() => {
  if (!userId) return;
  
  let cancelled = false;
  
  async function fetchUser() {
    try {
      const user = await api.getUser(userId);
      if (!cancelled) setUser(user); // guard against stale closures
    } catch (e) {
      if (!cancelled) setError(e as Error);
    }
  }
  
  fetchUser();
  
  return () => {
    cancelled = true; // cancel if userId changes before fetch completes
  };
}, [userId]); // re-runs when userId changes

// CASE 4: With cleanup — for subscriptions, intervals, event listeners
useEffect(() => {
  const handleResize = () => setWindowWidth(window.innerWidth);
  window.addEventListener("resize", handleResize);
  
  // Cleanup: remove listener when component unmounts or effect re-runs
  return () => window.removeEventListener("resize", handleResize);
}, []); // only mount/unmount
```

### Common useEffect Patterns

```tsx
// Pattern 1: Data fetching with loading/error state
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch(`/api/users/${userId}`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err);
          setLoading(false);
        }
      });

    return () => { cancelled = true; };
  }, [userId]);

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return null;
  return <UserCard user={user} />;
}

// Pattern 2: Syncing state with external system (WebSocket)
function LiveDashboard({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const ws = new WebSocket(`wss://api.example.com/rooms/${roomId}`);

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data) as Message;
      setMessages(prev => [...prev, message]);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close(); // cleanup: close connection when roomId changes or unmounts
    };
  }, [roomId]);

  return <MessageList messages={messages} />;
}

// Pattern 3: Debouncing (search input)
function SearchBox() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      const data = await searchApi(query);
      setResults(data);
    }, 300); // wait 300ms after user stops typing

    return () => clearTimeout(timer); // clear timer if query changes
  }, [query]);

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultList items={results} />
    </>
  );
}

// Pattern 4: Document title sync
function PageTitle({ title }: { title: string }) {
  useEffect(() => {
    const previousTitle = document.title;
    document.title = title;
    return () => { document.title = previousTitle; }; // restore on unmount
  }, [title]);

  return null; // render nothing
}

// AVOID: Missing dependencies — the linter will catch this
const [count, setCount] = useState(0);
useEffect(() => {
  // 'count' is used here but NOT in deps — stale closure!
  const id = setInterval(() => {
    setCount(count + 1); // 'count' is always the value from first render!
  }, 1000);
  return () => clearInterval(id);
}, []); // Missing: count

// FIX 1: Add dependency
}, [count]); // effect re-runs every time count changes — creates new interval

// FIX 2: Use functional update (better for this case)
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1); // no longer needs to read 'count'
  }, 1000);
  return () => clearInterval(id);
}, []); // empty deps is now correct!
```

### React 18 Strict Mode Double Invocation

```tsx
// In development with React.StrictMode, effects run TWICE on mount:
// 1. Mount → run effect
// 2. Unmount → run cleanup
// 3. Remount → run effect again

// This intentionally reveals bugs where you forget cleanup
// ALL effects should be resilient to running twice in development

useEffect(() => {
  const connection = connectToServer(); // establishes connection

  return () => {
    connection.disconnect(); // MUST clean up — strict mode verifies this
  };
}, []);
```

---

## 9. useRef — Complete Guide

`useRef` creates a mutable container that persists between renders WITHOUT causing re-renders when changed.

### Two Main Use Cases

```tsx
import { useRef, useEffect } from "react";

// USE CASE 1: Accessing DOM elements directly
function FocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  // Initially null — React sets it to the DOM element after mount

  useEffect(() => {
    inputRef.current?.focus(); // focus input after component mounts
  }, []);

  return <input ref={inputRef} type="text" />;
}

// Programmatically control DOM:
const videoRef = useRef<HTMLVideoElement>(null);
videoRef.current?.play();
videoRef.current?.pause();
videoRef.current?.requestFullscreen();

const canvasRef = useRef<HTMLCanvasElement>(null);
const ctx = canvasRef.current?.getContext("2d");

// USE CASE 2: Storing mutable values that don't trigger re-render
function StopWatch() {
  const [time, setTime] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  function start() {
    intervalRef.current = setInterval(() => {
      setTime(prev => prev + 1); // updating STATE here causes re-render (correct)
    }, 1000);
  }

  function stop() {
    if (intervalRef.current) {
      clearInterval(intervalRef.current); // using REF here — no re-render
      intervalRef.current = null;
    }
  }

  return (
    <div>
      <p>{time}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// More ref use cases:
function Component() {
  // Track whether it's the first render
  const isFirstRender = useRef(true);
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return; // skip effect on first render
    }
    // only runs on subsequent renders
    console.log("State changed!");
  });

  // Store previous value
  const prevCountRef = useRef<number>(0);
  const [count, setCount] = useState(0);
  useEffect(() => {
    prevCountRef.current = count; // update after render
  });
  const prevCount = prevCountRef.current; // previous render's value

  // Store callbacks without causing re-renders (for stable references)
  const callbackRef = useRef<() => void>(() => {});
  callbackRef.current = someCallback; // update synchronously in render
}
```

### `useImperativeHandle` & `forwardRef`

```tsx
// forwardRef: pass a ref to a child component's DOM element
import { forwardRef, useImperativeHandle } from "react";

// Simple forwardRef — expose the input DOM element
const TextInput = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  function TextInput(props, ref) {
    return <input ref={ref} {...props} />;
  }
);

// Usage:
const inputRef = useRef<HTMLInputElement>(null);
<TextInput ref={inputRef} placeholder="Type here..." />
inputRef.current?.focus(); // works — ref points to the <input>

// useImperativeHandle — expose a CUSTOM interface instead of the DOM element
interface VideoPlayerHandle {
  play(): void;
  pause(): void;
  seek(seconds: number): void;
  getDuration(): number;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, { src: string }>(
  function VideoPlayer({ src }, ref) {
    const videoRef = useRef<HTMLVideoElement>(null);

    useImperativeHandle(ref, () => ({
      play: () => videoRef.current?.play(),
      pause: () => videoRef.current?.pause(),
      seek: (s) => { if (videoRef.current) videoRef.current.currentTime = s; },
      getDuration: () => videoRef.current?.duration ?? 0,
    }), []); // dependencies

    return <video ref={videoRef} src={src} />;
  }
);

// Usage:
const playerRef = useRef<VideoPlayerHandle>(null);
playerRef.current?.play();
playerRef.current?.seek(30);
// Cannot access videoRef.current directly — it's encapsulated
```

---

## 10. useMemo & useCallback — Complete Guide

These hooks **memoize** (cache) values and functions to avoid unnecessary recalculation or re-creation.

### When to Use Them (and When NOT To)

```
The golden rule: DON'T prematurely optimize. Most re-renders are fast.
Use useMemo/useCallback when:
  ✅ Expensive computation that's provably slow (measure first!)
  ✅ Reference stability is required (passing objects/functions to memo() components)
  ✅ Dependency of another hook that would cause infinite loops

Don't use when:
  ❌ Simple computations (a + b, string formatting, etc.)
  ❌ Components that re-render rarely anyway
  ❌ Without measuring that it's actually a problem
```

### useMemo — Cache Computed Values

```tsx
import { useMemo } from "react";

function ProductList({ products, filterText, sortBy }: Props) {
  // WITHOUT useMemo: this runs on EVERY render (including unrelated state changes)
  const filtered = products
    .filter(p => p.name.toLowerCase().includes(filterText.toLowerCase()))
    .sort((a, b) => a[sortBy] > b[sortBy] ? 1 : -1);

  // WITH useMemo: only recomputes when products, filterText, or sortBy changes
  const processedProducts = useMemo(() => {
    console.log("Computing filtered products..."); // see when it runs
    return products
      .filter(p => p.name.toLowerCase().includes(filterText.toLowerCase()))
      .sort((a, b) => a[sortBy] > b[sortBy] ? 1 : -1);
  }, [products, filterText, sortBy]);

  return <ul>{processedProducts.map(p => <ProductItem key={p.id} product={p} />)}</ul>;
}

// Reference stability example
function Parent() {
  const [count, setCount] = useState(0);

  // WITHOUT useMemo: config is a NEW object on every render
  const config = { timeout: 5000, retries: 3 };

  // WITH useMemo: config is the SAME object reference between renders
  const stableConfig = useMemo(() => ({ timeout: 5000, retries: 3 }), []);

  // If Child is wrapped in React.memo(), passing a new object each time
  // would break memoization (objects are compared by reference)
  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <ChildMemo config={stableConfig} /> {/* won't re-render when count changes */}
    </>
  );
}
```

### useCallback — Cache Functions

```tsx
import { useCallback } from "react";

function Parent() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState<string[]>([]);

  // WITHOUT useCallback: handleAddItem is a new function on every render
  const handleAddItem = (text: string) => {
    setItems(prev => [...prev, text]);
  };

  // WITH useCallback: same function reference between renders (when deps don't change)
  const handleAddItemCached = useCallback((text: string) => {
    setItems(prev => [...prev, text]);
  }, []); // no dependencies — function never changes

  // With dependencies:
  const handleSearch = useCallback(async (query: string) => {
    const results = await searchAPI(query, count); // depends on count
    setItems(results);
  }, [count]); // re-created when count changes

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      {/* If AddItemForm is wrapped in React.memo, passing stable handleAddItem prevents re-renders */}
      <AddItemFormMemo onAdd={handleAddItemCached} />
    </>
  );
}

// React.memo — memoize a component, skip re-render if props are shallowly equal
const AddItemForm = React.memo(function AddItemForm({
  onAdd
}: {
  onAdd: (text: string) => void
}) {
  console.log("AddItemForm renders"); // should only render when onAdd changes
  const [text, setText] = useState("");
  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={() => onAdd(text)}>Add</button>
    </div>
  );
});
// React.memo does a SHALLOW comparison of props by default
// For custom comparison: React.memo(Component, (prevProps, nextProps) => areEqual)
```

---

## 11. useReducer — Complete Guide

`useReducer` is an alternative to `useState` for complex state logic. It's inspired by Redux.

### When to Use useReducer Over useState

```
Use useReducer when:
  ✅ Multiple sub-values that change together
  ✅ Next state depends on multiple previous values
  ✅ Complex state transitions (state machines)
  ✅ The logic would need to be shared or tested
  ✅ State update logic is complex enough to deserve its own function
```

### The Pattern

```tsx
import { useReducer } from "react";

// 1. Define state type
interface CartState {
  items: CartItem[];
  isOpen: boolean;
  discountCode: string | null;
}

// 2. Define all possible actions (discriminated union)
type CartAction =
  | { type: "ADD_ITEM"; payload: CartItem }
  | { type: "REMOVE_ITEM"; payload: { id: string } }
  | { type: "UPDATE_QUANTITY"; payload: { id: string; quantity: number } }
  | { type: "APPLY_DISCOUNT"; payload: { code: string } }
  | { type: "REMOVE_DISCOUNT" }
  | { type: "OPEN_CART" }
  | { type: "CLOSE_CART" }
  | { type: "CLEAR_CART" };

// 3. Write the reducer — pure function, no side effects
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case "ADD_ITEM": {
      const existingIndex = state.items.findIndex(i => i.id === action.payload.id);
      if (existingIndex >= 0) {
        // Item already in cart — increase quantity
        return {
          ...state,
          items: state.items.map((item, i) =>
            i === existingIndex
              ? { ...item, quantity: item.quantity + action.payload.quantity }
              : item
          )
        };
      }
      return { ...state, items: [...state.items, action.payload] };
    }

    case "REMOVE_ITEM":
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload.id)
      };

    case "UPDATE_QUANTITY":
      return {
        ...state,
        items: state.items.map(i =>
          i.id === action.payload.id
            ? { ...i, quantity: Math.max(0, action.payload.quantity) }
            : i
        ).filter(i => i.quantity > 0) // remove items with quantity 0
      };

    case "APPLY_DISCOUNT":
      return { ...state, discountCode: action.payload.code };

    case "REMOVE_DISCOUNT":
      return { ...state, discountCode: null };

    case "OPEN_CART":
      return { ...state, isOpen: true };

    case "CLOSE_CART":
      return { ...state, isOpen: false };

    case "CLEAR_CART":
      return { items: [], isOpen: false, discountCode: null };

    default:
      // TypeScript ensures exhaustiveness with 'never'
      const exhaustiveCheck: never = action;
      return state;
  }
}

// 4. Use in component
const initialState: CartState = {
  items: [],
  isOpen: false,
  discountCode: null,
};

function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);

  // Derived values from state
  const itemCount = state.items.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const discount = state.discountCode === "SAVE10" ? subtotal * 0.1 : 0;
  const total = subtotal - discount;

  return (
    <div>
      <button onClick={() => dispatch({ type: "OPEN_CART" })}>
        Cart ({itemCount})
      </button>

      {state.isOpen && (
        <div className="cart-panel">
          {state.items.map(item => (
            <div key={item.id}>
              <span>{item.name}</span>
              <button onClick={() => dispatch({ type: "REMOVE_ITEM", payload: { id: item.id } })}>
                Remove
              </button>
              <input
                type="number"
                value={item.quantity}
                onChange={e => dispatch({
                  type: "UPDATE_QUANTITY",
                  payload: { id: item.id, quantity: parseInt(e.target.value) }
                })}
              />
            </div>
          ))}
          <p>Total: ${total.toFixed(2)}</p>
          <button onClick={() => dispatch({ type: "CLEAR_CART" })}>Clear</button>
        </div>
      )}
    </div>
  );
}
```

---

## 12. useContext — Complete Guide

Context solves the **prop drilling** problem by making data available to any component in the tree without passing it through every level.

### Creating and Using Context

```tsx
import { createContext, useContext, useState, useMemo } from "react";

// 1. Define what the context provides
interface ThemeContextType {
  theme: "light" | "dark";
  toggleTheme: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

// 2. Create context with a DEFAULT value (used when no Provider is above)
const ThemeContext = createContext<ThemeContextType | null>(null);

// 3. Custom hook — easier to use, better error messages, encapsulates the null check
function useTheme(): ThemeContextType {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return ctx;
}

// 4. Provider component — wraps part of the tree that needs this context
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // Memoize the context value to avoid unnecessary re-renders
  const value = useMemo(
    () => ({
      theme,
      toggleTheme: () => setTheme(prev => prev === "light" ? "dark" : "light"),
      setTheme,
    }),
    [theme]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// 5. Usage anywhere in the tree
function ThemeButton() {
  const { theme, toggleTheme } = useTheme(); // no prop drilling needed!

  return (
    <button onClick={toggleTheme}>
      Current: {theme}
    </button>
  );
}

// 6. Setup at the app root
function App() {
  return (
    <ThemeProvider>
      {/* All children can use useTheme() */}
      <Header />
      <Main />
      <Footer />
    </ThemeProvider>
  );
}
```

### Full Auth Context Pattern

```tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check auth on mount
  useEffect(() => {
    async function checkAuth() {
      try {
        const response = await fetch("/api/auth/me");
        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      } catch {
        // Not authenticated
      } finally {
        setIsLoading(false);
      }
    }
    checkAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error("Login failed");
    const userData = await response.json();
    setUser(userData);
  }, []);

  const logout = useCallback(async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    const response = await fetch("/api/auth/me");
    if (response.ok) {
      const userData = await response.json();
      setUser(userData);
    }
  }, []);

  const value = useMemo(
    () => ({
      user,
      isLoading,
      isAuthenticated: user !== null,
      login,
      logout,
      refreshUser,
    }),
    [user, isLoading, login, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

// Usage
function ProtectedPage() {
  const { user, isLoading, isAuthenticated, logout } = useAuth();

  if (isLoading) return <Spinner />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return (
    <div>
      <h1>Welcome, {user!.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### Context Performance — Avoiding Unnecessary Re-Renders

```tsx
// Problem: ALL consumers re-render when context value changes
// Even if they only use part of the context

// Solution 1: Split context into smaller contexts
const UserContext = createContext<User | null>(null);
const ThemeContext = createContext<"light" | "dark">("light");
const NotificationsContext = createContext<Notification[]>([]);
// Components subscribe only to what they need

// Solution 2: Separate state from dispatch (common with useReducer)
type State = { theme: string; count: number };
type Action = { type: "SET_THEME"; value: string } | { type: "INCREMENT" };

const StateContext = createContext<State | null>(null);
const DispatchContext = createContext<React.Dispatch<Action> | null>(null);

// Components that only dispatch don't re-render on state change!
function IncrementButton() {
  const dispatch = useContext(DispatchContext)!;
  // This component WON'T re-render when state.theme changes
  return <button onClick={() => dispatch({ type: "INCREMENT" })}>+</button>;
}

// Solution 3: Use selector pattern with useSyncExternalStore or Zustand
```

---

## 13. Custom Hooks — Patterns & Best Practices

Custom hooks extract reusable stateful logic from components into functions.

### Rules of Hooks

```
1. ONLY call hooks at the TOP LEVEL of a function (not inside loops, conditions, or nested functions)
   - React relies on the ORDER of hook calls to maintain state
   
2. ONLY call hooks inside React FUNCTION COMPONENTS or other CUSTOM HOOKS

Hooks start with 'use' by convention (so linters can enforce the rules)
```

### Building Custom Hooks

```tsx
// Custom hook for data fetching
function useFetch<T>(url: string): {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
} {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [version, setVersion] = useState(0); // trigger for refetch

  useEffect(() => {
    if (!url) return;

    let cancelled = false;
    const controller = new AbortController();

    setLoading(true);
    setError(null);

    fetch(url, { signal: controller.signal })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        return res.json() as Promise<T>;
      })
      .then(data => {
        if (!cancelled) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled && err.name !== "AbortError") {
          setError(err instanceof Error ? err : new Error(String(err)));
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [url, version]);

  const refetch = useCallback(() => setVersion(v => v + 1), []);

  return { data, loading, error, refetch };
}

// Usage
function UserProfile({ id }: { id: string }) {
  const { data: user, loading, error, refetch } = useFetch<User>(`/api/users/${id}`);
  if (loading) return <Spinner />;
  if (error) return <button onClick={refetch}>Retry: {error.message}</button>;
  return user ? <UserCard user={user} /> : null;
}

// Custom hook for local storage
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    setStoredValue(prev => {
      const newValue = value instanceof Function ? value(prev) : value;
      try {
        window.localStorage.setItem(key, JSON.stringify(newValue));
      } catch (e) {
        console.warn("Failed to save to localStorage:", e);
      }
      return newValue;
    });
  }, [key]);

  return [storedValue, setValue];
}

// Custom hook for debouncing
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Custom hook for window size
function useWindowSize(): { width: number; height: number } {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return size;
}

// Custom hook for form field
function useField(initialValue: string = "") {
  const [value, setValue] = useState(initialValue);
  const [touched, setTouched] = useState(false);

  return {
    value,
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value),
    onBlur: () => setTouched(true),
    touched,
    reset: () => { setValue(initialValue); setTouched(false); },
  };
}

// Usage:
const nameField = useField("");
<input {...nameField} />
```

---

## 14. React 18 & 19 — New Hooks & Concurrent Features

### useTransition (React 18)

```tsx
import { useState, useTransition } from "react";

function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [isPending, startTransition] = useTransition();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const value = e.target.value;
    setQuery(value); // URGENT — update immediately

    startTransition(() => {
      // NON-URGENT — React can pause/interrupt this
      // The UI remains responsive while this is computing
      setResults(filterResults(value));
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending ? (
        <div className="opacity-50">Updating...</div>
      ) : (
        <ResultList results={results} />
      )}
    </>
  );
}
```

### useDeferredValue (React 18)

```tsx
import { useDeferredValue } from "react";

function SearchResults({ query }: { query: string }) {
  // Deferred version lags behind — keeps showing old results while new ones compute
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(
    () => filterResults(deferredQuery), // expensive computation
    [deferredQuery]
  );

  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>  {/* dim while stale */}
      {results.map(r => <ResultItem key={r.id} result={r} />)}
    </div>
  );
}
```

### useId (React 18)

```tsx
import { useId } from "react";

// Generates stable, unique IDs that work in SSR (server-generated id matches client)
function FormField({ label, type = "text" }: { label: string; type?: string }) {
  const id = useId(); // generates something like ":r0:", ":r1:", etc.

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} type={type} />
    </div>
  );
}
// Safe to render multiple instances — each gets a unique ID
<FormField label="Name" />
<FormField label="Email" type="email" />
```

### useSyncExternalStore (React 18)

```tsx
import { useSyncExternalStore } from "react";

// For subscribing to external stores (not React state)
// Used internally by Redux, Zustand, etc.

// Example: subscribing to browser online/offline status
function useOnlineStatus(): boolean {
  return useSyncExternalStore(
    (callback) => {
      // Subscribe
      window.addEventListener("online", callback);
      window.addEventListener("offline", callback);
      // Return unsubscribe function
      return () => {
        window.removeEventListener("online", callback);
        window.removeEventListener("offline", callback);
      };
    },
    () => navigator.onLine,     // getSnapshot (client)
    () => true                   // getServerSnapshot (SSR — assume online)
  );
}

function OnlineIndicator() {
  const isOnline = useOnlineStatus();
  return <span>{isOnline ? "🟢 Online" : "🔴 Offline"}</span>;
}
```

### useActionState (React 19 / Next.js 14+)

```tsx
import { useActionState } from "react";

// For Server Actions with loading state and error handling
type FormState = {
  errors?: Record<string, string[]>;
  message?: string;
} | null;

async function submitForm(prevState: FormState, formData: FormData): Promise<FormState> {
  // This is a Server Action
  "use server";
  const name = formData.get("name") as string;
  if (!name || name.length < 2) {
    return { errors: { name: ["Name must be at least 2 characters"] } };
  }
  await saveToDatabase({ name });
  return { message: "Saved successfully!" };
}

function MyForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="name" />
      {state?.errors?.name && (
        <p className="error">{state.errors.name[0]}</p>
      )}
      {state?.message && <p className="success">{state.message}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

### useOptimistic (React 19)

```tsx
import { useOptimistic, useTransition } from "react";

function LikeButton({ post }: { post: Post }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    post.likes,
    (state: number, increment: number) => state + increment
  );

  async function handleLike() {
    addOptimisticLike(1); // immediately update UI
    try {
      await likePost(post.id); // async server call
    } catch {
      // If it fails, React automatically reverts to the real value
    }
  }

  return (
    <button onClick={handleLike}>
      ❤️ {optimisticLikes} {/* shows +1 immediately, reverts on error */}
    </button>
  );
}
```

---

## 15. Component Patterns

### Higher-Order Components (HOC)

```tsx
// A HOC is a function that takes a component and returns an enhanced component
function withAuth<T extends object>(
  WrappedComponent: React.ComponentType<T>
): React.ComponentType<T> {
  return function WithAuthComponent(props: T) {
    const { user, isLoading } = useAuth();

    if (isLoading) return <FullPageSpinner />;
    if (!user) return <Navigate to="/login" />;

    return <WrappedComponent {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
// ProtectedDashboard has the same props as Dashboard, plus auth protection

// HOC with extra props injection
function withLogger<T extends object>(
  WrappedComponent: React.ComponentType<T>,
  componentName: string
): React.ComponentType<T> {
  return function LoggedComponent(props: T) {
    useEffect(() => {
      console.log(`${componentName} mounted`);
      return () => console.log(`${componentName} unmounted`);
    }, []);
    return <WrappedComponent {...props} />;
  };
}
```

### Polymorphic Components

```tsx
// A component that can render as different HTML elements or other components
type AsProp<C extends React.ElementType> = { as?: C };

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

type PolymorphicRef<C extends React.ElementType> = React.ComponentPropsWithRef<C>["ref"];

// Simple version (commonly sufficient):
type TextProps<T extends React.ElementType = "p"> = {
  as?: T;
  size?: "sm" | "md" | "lg";
  weight?: "normal" | "bold";
  children: React.ReactNode;
} & Omit<React.ComponentPropsWithoutRef<T>, "as" | "size" | "weight">;

function Text<T extends React.ElementType = "p">({
  as,
  size = "md",
  weight = "normal",
  children,
  className,
  ...rest
}: TextProps<T>) {
  const Component = as ?? "p";
  return (
    <Component
      className={`text-${size} font-${weight} ${className ?? ""}`}
      {...rest}
    >
      {children}
    </Component>
  );
}

// Usage:
<Text>Regular paragraph</Text>
<Text as="h1" size="lg" weight="bold">Heading</Text>
<Text as="span" className="text-gray-500">Small text</Text>
<Text as={Link} href="/about" size="sm">Link styled as Text</Text>
```

---

## 16. Performance Optimization

### Understanding React Rendering

```
A component re-renders when:
  1. Its state changes (useState, useReducer)
  2. Its parent re-renders (and it's not memoized)
  3. Its context value changes (if it uses useContext)

Re-rendering is NOT the same as DOM update:
  Re-render = React calls your function again
  DOM update = React actually changes the real DOM
  React is smart about DOM updates (only changes what's different)
  So most re-renders are fast and harmless

When to actually optimize:
  - Rendering large lists (100+ items)
  - Components with expensive calculations
  - Frequent updates (scroll, mouse move, real-time data)
  - Profiler shows a component is a bottleneck
```

### React.memo — Skip Re-renders

```tsx
// Component re-renders ONLY when props change (shallow comparison)
const ExpensiveChart = React.memo(function ExpensiveChart({
  data,
  width,
  height
}: ChartProps) {
  // This is expensive — only run when data/width/height actually change
  const processed = processData(data); // imagine this is slow
  return <canvas>{/* chart */}</canvas>;
});

// Custom comparison function
const UserRow = React.memo(
  function UserRow({ user, onSelect }: { user: User; onSelect: (id: string) => void }) {
    return (
      <tr onClick={() => onSelect(user.id)}>
        <td>{user.name}</td>
        <td>{user.email}</td>
      </tr>
    );
  },
  // Custom equality — only re-render if these specific fields change
  (prevProps, nextProps) =>
    prevProps.user.id === nextProps.user.id &&
    prevProps.user.name === nextProps.user.name &&
    prevProps.user.email === nextProps.user.email
    // Note: onSelect is NOT compared — use useCallback to keep it stable
);
```

### Virtualized Lists

```tsx
// For VERY long lists — only render what's visible
import { FixedSizeList as List } from "react-window";

function VirtualizedUserList({ users }: { users: User[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}> {/* style contains position/height for virtualization */}
      <UserRow user={users[index]} />
    </div>
  );

  return (
    <List
      height={600}        // visible height
      itemCount={users.length}
      itemSize={60}       // height of each row
      width="100%"
    >
      {Row}
    </List>
  );
}
// Instead of rendering 10,000 <UserRow> components, renders ~10 at a time
```

### Code Splitting & Lazy Loading

```tsx
import { lazy, Suspense } from "react";

// Lazy loading — only download when needed
const HeavyDashboard = lazy(() => import("./HeavyDashboard"));
const ChartLibrary = lazy(() => import("./ChartLibrary"));
const AdminPanel = lazy(() =>
  import("./AdminPanel").then(module => ({
    default: module.AdminPanel // for named exports
  }))
);

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      {/* HeavyDashboard's code is downloaded only when this renders */}
      <HeavyDashboard />
    </Suspense>
  );
}

// Route-based splitting — most common pattern
function AppRouter() {
  return (
    <Router>
      <Suspense fallback={<FullPageLoader />}>
        <Routes>
          <Route path="/" element={<HomePage />} /> {/* not lazy — load immediately */}
          <Route path="/dashboard" element={<lazy(() => import("./pages/Dashboard"))()}  />}
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Suspense>
    </Router>
  );
}
```

---

## 17. Forms in React

### Controlled vs Uncontrolled Components

```tsx
// CONTROLLED — React state is the source of truth
function ControlledForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    console.log({ name, email }); // always has latest value
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}                               // controlled by React state
        onChange={e => setName(e.target.value)}   // update state on change
      />
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
}

// UNCONTROLLED — DOM is the source of truth
function UncontrolledForm() {
  const formRef = useRef<HTMLFormElement>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const formData = new FormData(formRef.current!);
    const data = Object.fromEntries(formData); // { name: "...", email: "..." }
    console.log(data);
  }

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <input name="name" defaultValue="" />    {/* defaultValue, not value */}
      <input name="email" type="email" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Form Validation

```tsx
interface FormState {
  values: { name: string; email: string; password: string };
  errors: { name?: string; email?: string; password?: string };
  touched: { name: boolean; email: boolean; password: boolean };
  isSubmitting: boolean;
}

function RegisterForm() {
  const [state, setState] = useState<FormState>({
    values: { name: "", email: "", password: "" },
    errors: {},
    touched: { name: false, email: false, password: false },
    isSubmitting: false,
  });

  function validate(values: FormState["values"]): FormState["errors"] {
    const errors: FormState["errors"] = {};

    if (!values.name || values.name.length < 2) {
      errors.name = "Name must be at least 2 characters";
    }
    if (!values.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
      errors.email = "Please enter a valid email";
    }
    if (!values.password || values.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    return errors;
  }

  function handleChange(field: keyof FormState["values"]) {
    return (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValues = { ...state.values, [field]: e.target.value };
      setState(prev => ({
        ...prev,
        values: newValues,
        errors: validate(newValues), // validate on every change
      }));
    };
  }

  function handleBlur(field: keyof FormState["touched"]) {
    return () => {
      setState(prev => ({
        ...prev,
        touched: { ...prev.touched, [field]: true },
      }));
    };
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errors = validate(state.values);
    if (Object.keys(errors).length > 0) {
      setState(prev => ({
        ...prev,
        errors,
        touched: { name: true, email: true, password: true }, // show all errors
      }));
      return;
    }

    setState(prev => ({ ...prev, isSubmitting: true }));
    try {
      await registerUser(state.values);
      // redirect to dashboard
    } catch (err) {
      setState(prev => ({
        ...prev,
        isSubmitting: false,
        errors: { email: "This email is already registered" }
      }));
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          value={state.values.name}
          onChange={handleChange("name")}
          onBlur={handleBlur("name")}
          placeholder="Full Name"
        />
        {state.touched.name && state.errors.name && (
          <span className="error">{state.errors.name}</span>
        )}
      </div>
      {/* ... email and password fields similarly ... */}
      <button type="submit" disabled={state.isSubmitting}>
        {state.isSubmitting ? "Creating account..." : "Register"}
      </button>
    </form>
  );
}
```

---

## 18. Error Boundaries

Error boundaries are **class components** that catch JavaScript errors in their subtree and show fallback UI instead of crashing the whole app.

```tsx
import { Component, ErrorInfo } from "react";

interface ErrorBoundaryProps {
  fallback?: React.ReactNode;
  onError?: (error: Error, info: ErrorInfo) => void;
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    // Called when a child throws — update state to show fallback
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // Called after getDerivedStateFromError — good place to log to an error service
    console.error("Error caught by boundary:", error, info.componentStack);
    this.props.onError?.(error, info);
    // Send to Sentry, Datadog, etc.:
    // Sentry.captureException(error, { extra: { componentStack: info.componentStack } });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={this.handleReset}>Try Again</button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage — wrap sections that might throw
function App() {
  return (
    <ErrorBoundary
      onError={(error) => logToMonitoring(error)}
      fallback={<div>Critical error — please refresh</div>}
    >
      <Header />
      <ErrorBoundary fallback={<div>Chart failed to load</div>}>
        <ExpensiveChart /> {/* isolated — error here won't affect Header */}
      </ErrorBoundary>
      <Footer />
    </ErrorBoundary>
  );
}

// Error boundaries do NOT catch:
// - Async errors (inside setTimeout, fetch callbacks)
// - Server-side rendering errors
// - Errors in the error boundary itself
// - Event handler errors (use try/catch there)
```

---

## 19. Portals & Advanced DOM Control

```tsx
import { createPortal } from "react-dom";

// Portals render children into a DIFFERENT DOM node than the parent
// Useful for: modals, tooltips, dropdown menus (need to escape overflow/z-index)

function Modal({ isOpen, onClose, children }: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) {
  if (!isOpen) return null;

  return createPortal(
    // This JSX renders into document.body (or any element you choose)
    // Even though Modal is INSIDE your component tree
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body  // target container in the real DOM
  );
}

// Events still bubble through the React component tree (not the DOM tree)
// This means event handling works naturally even though the DOM position changed
```

---

## 20. State Management — Beyond useState

### Zustand (Modern, Lightweight State Management)

```tsx
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) => set({
        user,
        token,
        isAuthenticated: true,
      }),

      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false,
      }),
    }),
    {
      name: "auth-storage",   // localStorage key
      partialize: (state) => ({ token: state.token }), // only persist token
    }
  )
);

// Usage — automatically subscribes to changes
function UserMenu() {
  const { user, logout } = useAuthStore();

  if (!user) return null;
  return (
    <div>
      <span>{user.name}</span>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

// Select only what you need (performance optimization)
const userName = useAuthStore(state => state.user?.name);
const isAdmin = useAuthStore(state => state.user?.role === "admin");
```

---

## 21. Data Fetching Patterns

### TanStack Query (React Query)

```tsx
import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

// Setup
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,  // 5 minutes — data considered fresh
      gcTime: 10 * 60 * 1000,     // 10 minutes — cache kept for
      retry: 3,                    // retry failed requests 3 times
      refetchOnWindowFocus: true,  // refetch when user returns to tab
    },
  },
});

// Fetching data
function UserList() {
  const {
    data: users,
    isLoading,
    isError,
    error,
    isFetching,    // true when refetching in background
    refetch,
  } = useQuery({
    queryKey: ["users"],          // cache key — unique identifier
    queryFn: () => fetch("/api/users").then(r => r.json()) as Promise<User[]>,
    staleTime: 1000 * 60,        // override default for this query
  });

  if (isLoading) return <Spinner />;
  if (isError) return <div>Error: {(error as Error).message}</div>;

  return (
    <>
      {isFetching && <small>Updating...</small>} {/* background refetch indicator */}
      <ul>
        {users?.map(user => <UserRow key={user.id} user={user} />)}
      </ul>
    </>
  );
}

// Dependent queries
function UserPosts({ userId }: { userId: string | null }) {
  const { data: posts } = useQuery({
    queryKey: ["posts", userId],
    queryFn: () => fetch(`/api/users/${userId}/posts`).then(r => r.json()),
    enabled: !!userId,  // only fetch when userId is truthy
  });
  return <PostList posts={posts ?? []} />;
}

// Mutations — for creating/updating/deleting
function CreateUserForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newUser: CreateUserDto) =>
      fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
      }).then(r => r.json()) as Promise<User>,

    onSuccess: (newUser) => {
      // Update cache optimistically
      queryClient.setQueryData<User[]>(["users"], (old) =>
        old ? [...old, newUser] : [newUser]
      );
      // Or invalidate to trigger a refetch:
      // queryClient.invalidateQueries({ queryKey: ["users"] });
    },

    onError: (error) => {
      console.error("Failed to create user:", error);
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      mutation.mutate({ name: "Alice", email: "alice@example.com" });
    }}>
      {/* form fields */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create User"}
      </button>
      {mutation.isError && <p>Error: {mutation.error.message}</p>}
    </form>
  );
}
```

---

## 22. Testing React Components

```tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";

// Testing philosophy: test behavior (what users see and do), not implementation
// Query by accessibility (role, label, text) — more resilient to refactoring

describe("LoginForm", () => {
  const mockLogin = vi.fn();

  beforeEach(() => {
    mockLogin.mockClear();
  });

  it("renders email and password inputs", () => {
    render(<LoginForm onLogin={mockLogin} />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /log in/i })).toBeInTheDocument();
  });

  it("calls onLogin with credentials on submit", async () => {
    const user = userEvent.setup();
    render(<LoginForm onLogin={mockLogin} />);

    await user.type(screen.getByLabelText(/email/i), "alice@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /log in/i }));

    expect(mockLogin).toHaveBeenCalledWith({
      email: "alice@example.com",
      password: "password123",
    });
  });

  it("shows validation error for invalid email", async () => {
    const user = userEvent.setup();
    render(<LoginForm onLogin={mockLogin} />);

    await user.type(screen.getByLabelText(/email/i), "not-an-email");
    await user.click(screen.getByRole("button", { name: /log in/i }));

    expect(screen.getByText(/valid email/i)).toBeInTheDocument();
    expect(mockLogin).not.toHaveBeenCalled();
  });

  it("shows loading state while submitting", async () => {
    const user = userEvent.setup();
    // Login that takes a while
    mockLogin.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)));
    render(<LoginForm onLogin={mockLogin} />);

    await user.type(screen.getByLabelText(/email/i), "alice@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /log in/i }));

    expect(screen.getByRole("button", { name: /logging in/i })).toBeDisabled();
  });
});

// Test with providers (React Query, Auth Context, etc.)
function createTestWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </QueryClientProvider>
    );
  };
}

it("displays user data after fetching", async () => {
  vi.spyOn(global, "fetch").mockResolvedValueOnce(
    new Response(JSON.stringify({ id: "1", name: "Alice" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })
  );

  render(<UserProfile id="1" />, { wrapper: createTestWrapper() });

  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });
});
```

---

## 23. What is Next.js?

Next.js is a **React framework** built by Vercel that adds production-ready features:

```
Next.js adds to React:
  ✅ File-based routing — folders and files define URL routes
  ✅ Server-Side Rendering (SSR) — render on server per request
  ✅ Static Site Generation (SSG) — render at build time
  ✅ Incremental Static Regeneration (ISR) — static pages that auto-update
  ✅ Server Components — components that render ONLY on the server (zero client JS)
  ✅ Server Actions — async functions that run on the server, called from client
  ✅ API Routes — backend endpoints inside your Next.js app
  ✅ Streaming — send HTML chunks progressively (faster perceived load time)
  ✅ Image optimization — automatic WebP conversion, lazy loading, blur placeholder
  ✅ Font optimization — automatic self-hosting, zero layout shift
  ✅ Code splitting — automatic per-route bundling
  ✅ TypeScript — first-class support, zero configuration needed
  ✅ Middleware — intercept requests at the edge

Two Routers:
  Pages Router — legacy (pages/ directory), still maintained
  App Router — modern (app/ directory), Server Components, recommended for new projects
```

---

## 24. Next.js App Router — Architecture

### Directory Structure

```
my-app/
├── app/                      ← App Router — all routes live here
│   ├── layout.tsx            ← Root layout (wraps entire app)
│   ├── page.tsx              ← Route: /
│   ├── loading.tsx           ← Loading UI for this segment
│   ├── error.tsx             ← Error UI for this segment
│   ├── not-found.tsx         ← 404 page
│   ├── globals.css
│   │
│   ├── dashboard/
│   │   ├── layout.tsx        ← Layout for /dashboard/* routes
│   │   ├── page.tsx          ← Route: /dashboard
│   │   └── analytics/
│   │       └── page.tsx      ← Route: /dashboard/analytics
│   │
│   ├── blog/
│   │   ├── page.tsx          ← Route: /blog
│   │   └── [slug]/           ← Dynamic segment
│   │       └── page.tsx      ← Route: /blog/:slug
│   │
│   ├── (marketing)/          ← Route group — groups WITHOUT affecting URL
│   │   ├── about/
│   │   │   └── page.tsx      ← Route: /about (not /marketing/about)
│   │   └── contact/
│   │       └── page.tsx      ← Route: /contact
│   │
│   └── api/
│       └── users/
│           └── route.ts      ← API route: GET/POST /api/users
│
├── components/               ← Shared components
├── lib/                      ← Utilities, DB clients, etc.
├── public/                   ← Static files (images, fonts)
└── next.config.ts            ← Next.js configuration
```

### Special File Names

| File | Purpose |
|------|---------|
| `page.tsx` | The UI for a route — makes the route publicly accessible |
| `layout.tsx` | Shared UI that wraps pages — persists across navigation |
| `template.tsx` | Like layout but creates new instance on every navigation |
| `loading.tsx` | Suspense fallback for the route segment |
| `error.tsx` | Error boundary for the route segment (Client Component) |
| `not-found.tsx` | Rendered when `notFound()` is called or 404 |
| `route.ts` | API endpoint (no UI) |
| `middleware.ts` | Runs before requests (in root, not inside app/) |
| `default.tsx` | Fallback for parallel routes |

---

## 25. Server Components vs Client Components

This is the most important Next.js App Router concept.

### Server Components (Default)

```tsx
// ANY component in the app/ directory is a Server Component by default
// Server Components run ONLY on the server — the user's browser never receives the component code

// app/users/page.tsx
async function UsersPage() {
  // DIRECTLY access databases — no API layer needed!
  const users = await db.query("SELECT * FROM users LIMIT 50");
  // This code runs on the server — 'db' is never in the browser bundle

  // Fetch from internal APIs — no CORS, no auth headers needed
  const config = await getConfig(); // reads from filesystem, env vars, etc.

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name} — {user.email}</li>
        ))}
      </ul>
    </div>
  );
}

// What you CAN do in Server Components:
// ✅ async/await directly in component
// ✅ Access server-only resources (DB, filesystem, secrets)
// ✅ Import server-only packages (they're not in the client bundle)
// ✅ Reduce client JavaScript (no component code sent to browser)
// ✅ Access request data (cookies, headers)

// What you CANNOT do in Server Components:
// ❌ Use useState, useEffect, or any hooks
// ❌ Add event handlers (onClick, onChange, etc.)
// ❌ Use browser APIs (window, document, localStorage)
// ❌ Use React Context
```

### Client Components

```tsx
"use client"; // This directive marks the component as a Client Component

// Client Components are the traditional React components you're used to
// They run in the browser (and also on the server for SSR/hydration)

import { useState, useEffect } from "react";

export function Counter() {
  const [count, setCount] = useState(0); // hooks ✅

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button> {/* event handlers ✅ */}
    </div>
  );
}

// The "use client" directive:
// - Marks a boundary between server and client code
// - All IMPORTS of this component will also be client components
// - You don't need "use client" on every component — just the ones that
//   need interactivity or browser APIs
```

### Composing Server and Client Components

```tsx
// Server Component — fetches data, renders mostly static UI
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await db.products.findById(params.id); // server-only DB access

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>${product.price}</p>

      {/* Pass data DOWN to client component — this crosses the boundary */}
      <AddToCartButton productId={product.id} price={product.price} />
    </div>
  );
}

// "use client" — handles user interaction
"use client";
function AddToCartButton({ productId, price }: { productId: string; price: number }) {
  const [added, setAdded] = useState(false);

  async function handleAddToCart() {
    await addToCart(productId);
    setAdded(true);
  }

  return (
    <button onClick={handleAddToCart} disabled={added}>
      {added ? "Added to Cart ✓" : `Add to Cart — $${price}`}
    </button>
  );
}

// RULE: Server Components CAN be passed as props/children to Client Components
// But you CANNOT import a Server Component FROM a Client Component

// Pattern: "lifting" server data
async function ServerParent() {
  const data = await fetchExpensiveData();
  return (
    <ClientWrapper>
      <ServerChild data={data} /> {/* Server Component as child of Client Component */}
    </ClientWrapper>
  );
}

// This works because ServerChild is rendered on the server BEFORE ClientWrapper runs
```

---

## 26. Routing in the App Router

### Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: { slug: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function BlogPost({ params, searchParams }: PageProps) {
  const post = await getPost(params.slug);
  if (!post) notFound(); // triggers not-found.tsx

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// Generate static params at build time (for SSG)
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map(post => ({ slug: post.slug }));
}

// app/shop/[...categories]/page.tsx — catch-all routes
// Matches: /shop/electronics, /shop/electronics/phones, /shop/a/b/c
interface CatchAllProps {
  params: { categories: string[] }; // array of all segments
}

// app/shop/[[...categories]]/page.tsx — optional catch-all
// Also matches: /shop (categories would be undefined)
```

### Navigation

```tsx
import Link from "next/link";
import { useRouter, usePathname, useSearchParams } from "next/navigation";

// Declarative navigation — prefetches on hover
<Link href="/about">About</Link>
<Link href={`/users/${user.id}`}>User Profile</Link>
<Link href={{ pathname: "/blog", query: { page: 2 } }}>Next Page</Link>
// With replace (no history entry):
<Link href="/login" replace>Login</Link>
// Scroll to top:
<Link href="/page" scroll={false}>Stay here</Link>

// Programmatic navigation (in Client Components)
function SearchButton() {
  const router = useRouter();
  const pathname = usePathname(); // current path: "/dashboard"
  const searchParams = useSearchParams(); // URLSearchParams object

  function handleSearch(query: string) {
    const params = new URLSearchParams(searchParams);
    params.set("q", query);
    router.push(`/search?${params.toString()}`);
    // router.replace() — replace current history entry
    // router.back() — go back
    // router.forward() — go forward
    // router.refresh() — refresh current route (re-fetch server data)
    // router.prefetch("/heavy-page") — manually prefetch
  }
}
```

### Parallel Routes & Intercepting Routes

```tsx
// Parallel routes — show two pages at once
// app/layout.tsx
export default function Layout({
  children,
  modal,        // @modal slot
  sidebar,      // @sidebar slot
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
  sidebar: React.ReactNode;
}) {
  return (
    <div className="layout">
      <aside>{sidebar}</aside>
      <main>{children}</main>
      {modal}  {/* conditionally shown modal */}
    </div>
  );
}

// app/@modal/photos/[id]/page.tsx — intercepting route
// Shows photo in a modal when navigating from the gallery
// Shows photo on its own page when navigating directly or on refresh
```

---

## 27. Layouts, Templates & Special Files

### Root Layout (Required)

```tsx
// app/layout.tsx — must export a default function with html and body
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: { default: "My App", template: "%s | My App" },
  description: "My awesome app",
  metadataBase: new URL("https://myapp.com"),
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://myapp.com",
    siteName: "My App",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>  {/* QueryClient, Theme, Auth providers */}
          {children}
        </Providers>
      </body>
    </html>
  );
}
```

### Nested Layouts

```tsx
// app/dashboard/layout.tsx — wraps all /dashboard/* routes
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      <DashboardSidebar />  {/* this sidebar persists across all dashboard pages */}
      <main className="dashboard-content">
        {children}
      </main>
    </div>
  );
}

// Layout nesting order:
// Root Layout (app/layout.tsx)
//   └── Dashboard Layout (app/dashboard/layout.tsx)
//         └── page.tsx content

// IMPORTANT: Layouts do NOT re-render on navigation between their children
// DashboardSidebar stays mounted when going from /dashboard to /dashboard/analytics
```

### Loading UI (Suspense Integration)

```tsx
// app/dashboard/loading.tsx — automatically wrapped in Suspense
export default function DashboardLoading() {
  return (
    <div className="dashboard-skeleton">
      <div className="skeleton-header" />
      <div className="skeleton-grid">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="skeleton-card" />
        ))}
      </div>
    </div>
  );
}
// Next.js wraps the page.tsx in <Suspense fallback={<DashboardLoading />}>
// So the layout renders immediately, loading UI shows while page data fetches
```

### Error Handling

```tsx
// app/dashboard/error.tsx — Error Boundary for this segment
"use client"; // Error components must be Client Components

import { useEffect } from "react";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }; // digest = server error ID for logging
  reset: () => void;                  // retry — re-renders the error boundary
}) {
  useEffect(() => {
    // Log to error tracking service
    console.error(error);
    Sentry?.captureException(error, { extra: { digest: error.digest } });
  }, [error]);

  return (
    <div className="error-page">
      <h2>Something went wrong in the dashboard</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

---

## 28. Data Fetching in Next.js

### Server Component Data Fetching

```tsx
// app/users/page.tsx — Server Component
// fetch() is extended by Next.js to support caching

export default async function UsersPage() {
  // Cached fetch — data cached indefinitely until invalidated
  const users = await fetch("https://api.example.com/users", {
    cache: "force-cache", // default in Next.js 13-14
  }).then(r => r.json());

  // No-store — always fetch fresh data (like getServerSideProps)
  const liveData = await fetch("https://api.example.com/live", {
    cache: "no-store",
  }).then(r => r.json());

  // Revalidate every N seconds (ISR-style)
  const semiStale = await fetch("https://api.example.com/data", {
    next: { revalidate: 60 }, // fresh for 60 seconds
  }).then(r => r.json());

  // Tag-based revalidation
  const tagged = await fetch("https://api.example.com/products", {
    next: { tags: ["products"] }, // can invalidate with revalidateTag("products")
  }).then(r => r.json());

  return <UserList users={users} />;
}
```

### Parallel Data Fetching

```tsx
// Sequential (slow — 1000ms + 500ms = 1500ms total)
async function Sequential() {
  const user = await fetchUser();      // 1000ms
  const posts = await fetchPosts();    // 500ms more
  return <div>{/* ... */}</div>;
}

// Parallel (fast — max(1000ms, 500ms) = 1000ms total)
async function Parallel() {
  const [user, posts] = await Promise.all([
    fetchUser(),    // starts immediately
    fetchPosts(),   // starts immediately too
  ]);
  return <div>{/* ... */}</div>;
}

// Streaming with Suspense — start rendering parts immediately
async function StreamingPage() {
  const user = await fetchUser(); // fast — load immediately

  return (
    <div>
      <UserHeader user={user} />  {/* renders immediately */}

      <Suspense fallback={<PostsSkeleton />}>
        <SlowPosts userId={user.id} />  {/* streams in when ready */}
      </Suspense>

      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics userId={user.id} />  {/* streams in when ready */}
      </Suspense>
    </div>
  );
}
```

### generateMetadata — Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";

interface Props {
  params: { slug: string };
}

// Can be async — fetches data for metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  if (!post) return { title: "Post Not Found" };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage, width: 1200, height: 630 }],
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
    },
  };
}

export default async function BlogPost({ params }: Props) {
  const post = await getPost(params.slug);
  // ...
}
```

---

## 29. Caching in Next.js

Next.js 15 has a sophisticated caching system:

```
Four layers of caching:

1. Request Memoization (per request)
   - Automatically deduplicates fetch() calls with same URL within one render
   - Two different components fetching the same URL → one actual HTTP request

2. Data Cache (persistent)
   - fetch() results stored on the server
   - Persists across requests and deployments (until invalidated)
   - Controlled by: cache: 'force-cache', cache: 'no-store', next.revalidate

3. Full Route Cache (persistent)
   - Complete rendered HTML + RSC payload stored for static routes
   - Revalidated on: revalidatePath(), revalidateTag(), time interval

4. Router Cache (client-side)
   - Client-side cache of visited routes and prefetched routes
   - Persists for the session
   - Cleared on: router.refresh(), location change

Cache invalidation:
  revalidatePath("/users")       — invalidate specific path
  revalidatePath("/", "layout") — invalidate layout (affects all pages using it)
  revalidateTag("users")         — invalidate all fetches tagged with "users"
  cookies().set(...)             — opt out of cache
  headers()                      — opt out of cache
```

```tsx
// On-demand revalidation from Server Actions
"use server";
import { revalidatePath, revalidateTag } from "next/cache";

export async function updateUser(userId: string, data: UpdateUserDto) {
  await db.users.update({ where: { id: userId }, data });

  revalidatePath(`/users/${userId}`); // invalidate this user's page
  revalidatePath("/users");           // invalidate the users list page
  revalidateTag("users");             // invalidate all fetches tagged "users"
}
```

---

## 30. Server Actions

Server Actions are async functions that run on the **server**, callable from client components.

```tsx
// DEFINING Server Actions
// Method 1: "use server" directive at function level (in Server Components)
async function ServerPage() {
  async function createUser(formData: FormData) {
    "use server"; // marks this function as a Server Action
    const name = formData.get("name") as string;
    await db.users.create({ data: { name } });
    revalidatePath("/users");
  }

  return (
    <form action={createUser}> {/* directly use Server Action as form action */}
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  );
}

// Method 2: Dedicated actions file (recommended for organization)
// lib/actions/users.ts
"use server"; // applies to ALL exports in this file

import { z } from "zod";
import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";

const CreateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  role: z.enum(["admin", "user"]).default("user"),
});

type ActionState = {
  success: boolean;
  errors?: Record<string, string[]>;
  message?: string;
};

export async function createUser(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  // Validate input
  const parsed = CreateUserSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    role: formData.get("role"),
  });

  if (!parsed.success) {
    return {
      success: false,
      errors: parsed.error.flatten().fieldErrors,
    };
  }

  try {
    // Server-side operations — DB access, auth checks, etc.
    const authCookie = cookies().get("session")?.value;
    if (!authCookie) redirect("/login"); // server-side redirect

    await db.users.create({ data: parsed.data });
    revalidatePath("/users");
    revalidateTag("users");

    return { success: true, message: "User created successfully" };
  } catch (error) {
    if (error instanceof Error && error.message.includes("duplicate")) {
      return {
        success: false,
        errors: { email: ["This email is already registered"] },
      };
    }
    throw error; // re-throw unexpected errors — caught by error.tsx
  }
}

export async function deleteUser(userId: string): Promise<void> {
  await db.users.delete({ where: { id: userId } });
  revalidatePath("/users");
}

// USING Server Actions in Client Components
"use client";

import { useActionState } from "react";
import { createUser } from "@/lib/actions/users";

function CreateUserForm() {
  const [state, action, isPending] = useActionState(createUser, null);

  return (
    <form action={action}>
      <input name="name" disabled={isPending} />
      {state?.errors?.name && <p className="error">{state.errors.name[0]}</p>}

      <input name="email" type="email" disabled={isPending} />
      {state?.errors?.email && <p className="error">{state.errors.email[0]}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create User"}
      </button>

      {state?.success && <p className="success">{state.message}</p>}
    </form>
  );
}

// Calling Server Actions from event handlers (not forms)
"use client";
function DeleteButton({ userId }: { userId: string }) {
  const [isPending, startTransition] = useTransition();

  return (
    <button
      onClick={() => {
        startTransition(async () => {
          await deleteUser(userId); // Server Action called from event handler
        });
      }}
      disabled={isPending}
    >
      {isPending ? "Deleting..." : "Delete"}
    </button>
  );
}
```

---

## 31. API Routes (Route Handlers)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

export const dynamic = "force-dynamic"; // opt out of static rendering
export const runtime = "nodejs";        // or "edge" for Vercel Edge

// GET /api/users
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get("page") ?? "1");
    const limit = parseInt(searchParams.get("limit") ?? "20");
    const search = searchParams.get("search") ?? "";

    const users = await db.users.findMany({
      skip: (page - 1) * limit,
      take: limit,
      where: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
    });

    const total = await db.users.count({
      where: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
    });

    return NextResponse.json({ users, total, page, limit });
  } catch (error) {
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

// POST /api/users
const CreateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  role: z.enum(["admin", "user"]).default("user"),
});

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const token = request.headers.get("Authorization")?.replace("Bearer ", "");
    if (!token) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    const session = await verifyToken(token);
    if (!session) return NextResponse.json({ error: "Invalid token" }, { status: 401 });

    // Validate request body
    const body = await request.json();
    const parsed = CreateUserSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { error: "Validation failed", details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    // Create user
    const user = await db.users.create({ data: parsed.data });
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

// app/api/users/[id]/route.ts — dynamic route handler
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.users.findUnique({ where: { id: params.id } });
  if (!user) return NextResponse.json({ error: "Not found" }, { status: 404 });
  return NextResponse.json(user);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  const user = await db.users.update({ where: { id: params.id }, data: body });
  return NextResponse.json(user);
}

export async function DELETE(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.users.delete({ where: { id: params.id } });
  return new NextResponse(null, { status: 204 });
}
```

---

## 32. Middleware

Middleware runs BEFORE a request is completed — it's the right place for:
- Authentication checks
- Redirects and rewrites
- Locale detection
- A/B testing
- Request logging

```tsx
// middleware.ts — must be at the root of the project (not inside app/)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check auth for protected routes
  if (pathname.startsWith("/dashboard") || pathname.startsWith("/api/protected")) {
    const token = request.cookies.get("session")?.value;

    if (!token) {
      // Redirect to login
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }

    // Verify token (simple check — for complex validation use edge-compatible JWT library)
    const session = parseToken(token);
    if (!session || session.expiresAt < Date.now()) {
      const response = NextResponse.redirect(new URL("/login", request.url));
      response.cookies.delete("session"); // clear invalid cookie
      return response;
    }

    // Inject user info into headers for downstream use
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set("x-user-id", session.userId);
    requestHeaders.set("x-user-role", session.role);

    return NextResponse.next({ request: { headers: requestHeaders } });
  }

  // Locale detection
  const locale = request.headers.get("accept-language")?.split(",")[0]?.split("-")[0] ?? "en";
  if (locale === "ar" && !pathname.startsWith("/ar")) {
    return NextResponse.redirect(new URL(`/ar${pathname}`, request.url));
  }

  return NextResponse.next();
}

// Config — which paths middleware runs on
export const config = {
  matcher: [
    // Match all except static files and _next
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:jpg|jpeg|gif|png|svg|ico)).*)",
  ],
};
```

---

## 33. Image, Font & Script Optimization

```tsx
// Image optimization
import Image from "next/image";

// Local image — automatically gets width/height
import profilePic from "@/public/profile.jpg";
<Image src={profilePic} alt="Profile" />

// Remote image — must provide dimensions
<Image
  src="https://cdn.example.com/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  priority            // load immediately (above the fold)
  quality={80}        // 1-100, default 75
  placeholder="blur"  // show blur while loading
  blurDataURL="data:image/..."  // base64 blur placeholder
/>

// Fill mode — fills parent container
<div style={{ position: "relative", width: "100%", height: "400px" }}>
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    style={{ objectFit: "cover" }}
    sizes="(max-width: 768px) 100vw, 50vw"  // for responsive optimization
  />
</div>

// Font optimization
import { Inter, Roboto_Mono } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",          // show fallback font until Inter loads
  variable: "--font-inter", // CSS variable for Tailwind
});

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  variable: "--font-roboto-mono",
});

// app/layout.tsx
<html className={`${inter.variable} ${robotoMono.variable}`}>
  <body className={inter.className}>

// Script optimization
import Script from "next/script";

// Strategy options:
<Script src="https://analytics.com/script.js" strategy="beforeInteractive" />
// beforeInteractive: loads before page becomes interactive (for critical scripts)
<Script src="https://widget.com/embed.js" strategy="afterInteractive" />
// afterInteractive: loads after hydration (default for most scripts)
<Script src="https://ads.com/script.js" strategy="lazyOnload" />
// lazyOnload: loads during browser idle time
```

---

## 34. Authentication Patterns

### With NextAuth.js (Auth.js v5)

```tsx
// auth.ts — configuration
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Credentials from "next-auth/providers/credentials";
import { db } from "@/lib/db";
import { verifyPassword } from "@/lib/crypto";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    GitHub,
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials.password) return null;
        const user = await db.users.findUnique({
          where: { email: credentials.email as string }
        });
        if (!user) return null;
        const isValid = await verifyPassword(credentials.password as string, user.passwordHash);
        if (!isValid) return null;
        return { id: user.id, name: user.name, email: user.email, role: user.role };
      }
    })
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = (user as any).role;
      return token;
    },
    session({ session, token }) {
      session.user.role = token.role as string;
      return session;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
});

// app/api/auth/[...nextauth]/route.ts
export { handlers as GET, handlers as POST } from "@/auth";

// Using in Server Components
const session = await auth();
if (!session?.user) redirect("/login");
console.log(session.user.name);

// Using in Client Components
import { useSession, signIn, signOut } from "next-auth/react";
const { data: session, status } = useSession();
if (status === "loading") return <Spinner />;
if (!session) return <button onClick={() => signIn()}>Login</button>;
```

---

## 35. Streaming & Suspense in Next.js

```tsx
// Streaming sends HTML in chunks as it becomes available
// Users see content sooner instead of waiting for all data

// app/page.tsx — enable streaming with multiple Suspense boundaries
import { Suspense } from "react";

export default function HomePage() {
  return (
    <main>
      {/* Renders immediately — no async data */}
      <Hero />

      {/* Streams in when TopProducts query completes */}
      <Suspense fallback={<ProductsSkeleton count={4} />}>
        <TopProducts />
      </Suspense>

      {/* Streams in when UserRecommendations query completes */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <UserRecommendations />
      </Suspense>

      {/* Streams in last — most expensive query */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <RecentReviews />
      </Suspense>
    </main>
  );
}

// Server Components with async data
async function TopProducts() {
  const products = await db.products.findMany({
    orderBy: { sales: "desc" },
    take: 4,
  });
  return <ProductGrid products={products} />;
}

// The browser receives and renders:
// 1. Immediately: HTML with Hero + Skeletons for everything else
// 2. When TopProducts resolves: product grid HTML replaces skeleton
// 3. When UserRecommendations resolves: recommendations replace skeleton
// 4. When RecentReviews resolves: reviews replace skeleton
// All in a single HTTP connection — no waterfalls!
```

---

## 36. Deploying Next.js

```bash
# Build
npm run build   # creates .next/ directory with optimized output

# Output modes in next.config.ts:
# default: hybrid — each page uses best rendering strategy
# standalone: self-contained Node.js server for Docker
# export: pure static output (no server features)

# next.config.ts
const config: NextConfig = {
  output: "standalone",  // for Docker deployment
  
  images: {
    domains: ["cdn.example.com"],
    remotePatterns: [
      { protocol: "https", hostname: "*.cloudfront.net" }
    ],
  },
  
  // Redirect old URLs
  async redirects() {
    return [
      { source: "/old-path", destination: "/new-path", permanent: true },
    ];
  },
  
  // Headers
  async headers() {
    return [
      {
        source: "/api/:path*",
        headers: [
          { key: "Cache-Control", value: "no-store" },
        ],
      },
    ];
  },
};
```

```dockerfile
# Dockerfile for Next.js standalone
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Quick Reference: React Hooks

| Hook | Purpose |
|------|---------|
| `useState` | Local state — triggers re-render on change |
| `useEffect` | Side effects — after render |
| `useRef` | Mutable ref / DOM access — no re-render |
| `useMemo` | Cache expensive computed value |
| `useCallback` | Cache function reference |
| `useReducer` | Complex state with actions |
| `useContext` | Read context value |
| `useId` | Stable unique ID (SSR-safe) |
| `useTransition` | Mark state updates as non-urgent |
| `useDeferredValue` | Defer a value to show old content while updating |
| `useSyncExternalStore` | Subscribe to external store |
| `useActionState` | Manage Server Action state (React 19) |
| `useOptimistic` | Optimistic UI updates (React 19) |
| `useFormStatus` | Track form submission status (React 19) |

## Quick Reference: Next.js App Router

| Feature | How |
|---------|-----|
| Page route | `app/path/page.tsx` |
| Dynamic route | `app/[param]/page.tsx` |
| Layout | `app/path/layout.tsx` |
| Loading UI | `app/path/loading.tsx` |
| Error UI | `app/path/error.tsx` (Client Component) |
| Not found | `app/path/not-found.tsx` |
| API endpoint | `app/api/path/route.ts` |
| Server Action | `"use server"` directive |
| Client Component | `"use client"` directive |
| Middleware | `middleware.ts` at root |
| Metadata | `export const metadata` or `generateMetadata()` |
| Static params | `export async function generateStaticParams()` |
| Cache invalidation | `revalidatePath()` or `revalidateTag()` |

---

*This guide covers React from first principles through advanced patterns and the complete Next.js App Router. The next file covers oRPC, PostgreSQL, and Drizzle ORM.*
