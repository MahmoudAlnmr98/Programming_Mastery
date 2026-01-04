# Frontend Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. Explain the difference between HTML, CSS, and JavaScript.

**Answer:**
- **HTML**: Structure and content (markup language)
- **CSS**: Styling and presentation
- **JavaScript**: Behavior and interactivity

### 2. Explain CSS Box Model.

**Answer:**
Box model defines how elements are sized and spaced.

**Components:**
- **Content**: Actual content
- **Padding**: Space inside border
- **Border**: Border around padding
- **Margin**: Space outside border

```css
.box {
    width: 200px;        /* Content width */
    padding: 20px;       /* Inside space */
    border: 5px solid;   /* Border */
    margin: 10px;        /* Outside space */
    box-sizing: border-box; /* Include padding/border in width */
}
```

### 3. Explain CSS Flexbox.

**Answer:**
Flexbox provides efficient layout for one-dimensional layouts.

```css
.container {
    display: flex;
    flex-direction: row;      /* row, column */
    justify-content: center;   /* Main axis alignment */
    align-items: center;      /* Cross axis alignment */
    flex-wrap: wrap;          /* Wrap items */
}

.item {
    flex: 1;                 /* Grow and shrink */
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 0;
}
```

### 4. Explain CSS Grid.

**Answer:**
Grid provides two-dimensional layout system.

```css
.container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: auto;
    gap: 20px;
}

.item {
    grid-column: 1 / 3;  /* Span columns */
    grid-row: 1;        /* Row position */
}
```

### 5. Explain responsive design.

**Answer:**
Responsive design adapts to different screen sizes.

**Techniques:**
- **Media Queries**: Different styles for different screen sizes
- **Flexible Units**: %, em, rem, vw, vh
- **Flexbox/Grid**: Flexible layouts
- **Mobile-First**: Design for mobile first

```css
/* Mobile-first */
.container {
    width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        width: 750px;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        width: 1200px;
    }
}
```

### 6. Explain DOM manipulation.

**Answer:**
DOM (Document Object Model) represents HTML as tree structure.

```javascript
// Select elements
const element = document.getElementById('id');
const elements = document.querySelectorAll('.class');

// Modify content
element.textContent = 'New text';
element.innerHTML = '<strong>HTML</strong>';

// Modify attributes
element.setAttribute('id', 'newId');
element.className = 'new-class';

// Create elements
const div = document.createElement('div');
div.textContent = 'Hello';
document.body.appendChild(div);
```

### 7. Explain event delegation.

**Answer:**
Event delegation uses event bubbling to handle events on parent.

```javascript
// Instead of adding listener to each child
document.querySelectorAll('.button').forEach(btn => {
    btn.addEventListener('click', handleClick);
});

// Use event delegation
document.addEventListener('click', (e) => {
    if (e.target.matches('.button')) {
        handleClick(e);
    }
});
```

### 8. Explain CORS (Cross-Origin Resource Sharing).

**Answer:**
CORS allows web pages to request resources from different origin.

**Same-Origin Policy:**
- Same protocol, domain, port
- Blocks cross-origin requests

**CORS Headers:**
```javascript
// Server response
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Content-Type
```

---

## Intermediate Level

### 9. Explain Web Performance Optimization.

**Answer:**
**Techniques:**
1. **Minification**: Reduce file size
2. **Compression**: Gzip/Brotli
3. **Caching**: Browser cache, CDN
4. **Lazy Loading**: Load resources on demand
5. **Code Splitting**: Split code into chunks
6. **Image Optimization**: WebP, lazy loading
7. **Critical CSS**: Inline above-the-fold CSS

### 10. Explain Web Accessibility (a11y).

**Answer:**
Making web accessible to people with disabilities.

**Principles:**
- **Perceivable**: Information presentable to users
- **Operable**: Interface components operable
- **Understandable**: Information understandable
- **Robust**: Content interpretable by assistive technologies

**Best Practices:**
```html
<!-- Semantic HTML -->
<nav>
    <ul>
        <li><a href="/">Home</a></li>
    </ul>
</nav>

<!-- ARIA attributes -->
<button aria-label="Close dialog">×</button>

<!-- Alt text for images -->
<img src="image.jpg" alt="Description of image">

<!-- Keyboard navigation -->
<button tabindex="0">Click me</button>
```

### 11. Explain Progressive Web Apps (PWA).

**Answer:**
PWAs provide app-like experience in browser.

**Features:**
- **Service Worker**: Offline functionality, background sync
- **Web App Manifest**: App metadata
- **Responsive**: Works on all devices
- **Installable**: Can be installed

```javascript
// Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then(cache => {
            return cache.addAll(['/', '/index.html']);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
```

### 12. Explain CSS Preprocessors (SASS/LESS).

**Answer:**
Preprocessors extend CSS with variables, nesting, mixins.

**SASS Example:**
```scss
// Variables
$primary-color: #3498db;
$font-size: 16px;

// Nesting
.nav {
    ul {
        margin: 0;
        padding: 0;
        li {
            display: inline-block;
        }
    }
}

// Mixins
@mixin border-radius($radius) {
    border-radius: $radius;
}

.button {
    @include border-radius(5px);
}
```

### 13. Explain build tools (Webpack, Vite).

**Answer:**
**Webpack:**
- Bundles modules
- Code splitting
- Loaders for different file types
- Plugins for optimization

**Vite:**
- Fast development server
- ES modules in development
- Rollup for production
- Faster than Webpack

### 14. Explain state management in frontend.

**Answer:**
**Local State:**
- Component-level state (useState)

**Global State:**
- Context API (React)
- Redux, Zustand, Jotai
- Vuex (Vue)

**Server State:**
- React Query, SWR
- Apollo Client (GraphQL)

---

## Advanced Level

### 15. Explain micro-frontends.

**Answer:**
Architecture where frontend is composed of independent applications.

**Approaches:**
- **Build-time**: Compile together
- **Run-time**: Load independently
- **iframe**: Isolated applications
- **Web Components**: Custom elements

### 16. Explain WebAssembly (WASM).

**Answer:**
Binary format for running code in browser.

**Use Cases:**
- Performance-critical code
- Existing C/C++ codebases
- Image/video processing
- Games

### 17. Explain frontend security.

**Answer:**
**XSS Prevention:**
- Escape user input
- Use textContent instead of innerHTML
- Content Security Policy (CSP)

**CSRF Prevention:**
- CSRF tokens
- SameSite cookies

**Input Validation:**
- Validate on client and server
- Sanitize inputs

### 18. Explain Web Components.

**Answer:**
Web Components are reusable custom HTML elements.

**Components:**
- **Custom Elements**: Define new HTML elements
- **Shadow DOM**: Encapsulated DOM
- **HTML Templates**: Reusable markup
- **ES Modules**: Component loading

```javascript
class MyComponent extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({mode: 'open'});
        shadow.innerHTML = `
            <style>
                :host { display: block; }
            </style>
            <div>Hello from Web Component</div>
        `;
    }
}

customElements.define('my-component', MyComponent);
```

### 19. Explain CSS-in-JS solutions.

**Answer:**
CSS-in-JS allows writing CSS in JavaScript.

**Libraries:**
- **Styled Components**: CSS with template literals
- **Emotion**: CSS-in-JS with performance
- **JSS**: JavaScript Style Sheets

**Example (Styled Components):**
```javascript
import styled from 'styled-components';

const Button = styled.button`
    background: ${props => props.primary ? 'blue' : 'gray'};
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
`;

<Button primary>Click me</Button>
```

**Benefits:**
- Scoped styles
- Dynamic styling
- No class name conflicts
- Better component encapsulation

### 20. Explain Server-Sent Events (SSE).

**Answer:**
SSE allows server to push data to client.

```javascript
// Client
const eventSource = new EventSource('/events');

eventSource.onmessage = (event) => {
    console.log('Data:', event.data);
};

eventSource.onerror = (error) => {
    console.error('Error:', error);
};

// Server (Node.js)
app.get('/events', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    
    setInterval(() => {
        res.write(`data: ${JSON.stringify({time: Date.now()})}\n\n`);
    }, 1000);
});
```

### 21. Explain CSS Custom Properties (CSS Variables).

**Answer:**
CSS variables allow dynamic values.

```css
:root {
    --primary-color: #3498db;
    --spacing: 20px;
}

.button {
    background: var(--primary-color);
    padding: var(--spacing);
}

/* Override in component */
.dark-theme {
    --primary-color: #2c3e50;
}
```

**JavaScript Access:**
```javascript
// Get
const color = getComputedStyle(document.documentElement)
    .getPropertyValue('--primary-color');

// Set
document.documentElement.style.setProperty('--primary-color', '#e74c3c');
```

### 22. Explain Intersection Observer API.

**Answer:**
Intersection Observer detects when elements enter/exit viewport.

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.5,  // Trigger when 50% visible
    rootMargin: '50px'
});

observer.observe(document.querySelector('.element'));
```

**Use Cases:**
- Lazy loading images
- Infinite scroll
- Animations on scroll
- Analytics tracking

### 23. Explain Web Workers in detail.

**Answer:**
Web Workers run JavaScript in background threads.

**Dedicated Worker:**
```javascript
// main.js
const worker = new Worker('worker.js');
worker.postMessage({data: 'Hello'});
worker.onmessage = (e) => {
    console.log('Result:', e.data);
};

// worker.js
self.onmessage = (e) => {
    const result = processData(e.data);
    self.postMessage(result);
};
```

**Shared Worker:**
```javascript
// Multiple scripts can share
const worker = new SharedWorker('shared-worker.js');
worker.port.postMessage('Hello');
worker.port.onmessage = (e) => {
    console.log(e.data);
};
```

**Limitations:**
- No DOM access
- No window object
- Communication via messages only

### 24. Explain IndexedDB.

**Answer:**
IndexedDB is browser database for large data storage.

```javascript
// Open database
const request = indexedDB.open('MyDB', 1);

request.onupgradeneeded = (event) => {
    const db = event.target.result;
    const store = db.createObjectStore('users', {keyPath: 'id'});
    store.createIndex('name', 'name', {unique: false});
};

request.onsuccess = (event) => {
    const db = event.target.result;
    
    // Add data
    const transaction = db.transaction(['users'], 'readwrite');
    const store = transaction.objectStore('users');
    store.add({id: 1, name: 'John'});
    
    // Get data
    const getRequest = store.get(1);
    getRequest.onsuccess = () => {
        console.log(getRequest.result);
    };
};
```

### 25. Explain WebRTC basics.

**Answer:**
WebRTC enables peer-to-peer communication.

**Components:**
- **MediaStream**: Audio/video streams
- **RTCPeerConnection**: Peer connection
- **RTCDataChannel**: Data transfer

```javascript
// Get user media
navigator.mediaDevices.getUserMedia({video: true, audio: true})
    .then(stream => {
        videoElement.srcObject = stream;
    });

// Create peer connection
const pc = new RTCPeerConnection();
pc.onicecandidate = (event) => {
    if (event.candidate) {
        // Send candidate to peer
    }
};

pc.ontrack = (event) => {
    remoteVideo.srcObject = event.streams[0];
};
```

### 26. Explain browser rendering pipeline and optimization.

**Answer:**
**Rendering Pipeline:**
1. **Parse HTML** → DOM tree
2. **Parse CSS** → CSSOM tree
3. **Combine** → Render tree
4. **Layout** → Calculate positions
5. **Paint** → Fill pixels
6. **Composite** → Layer composition

**Optimization:**
```javascript
// Use requestAnimationFrame for animations
function animate() {
    // Animation code
    requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// Use transform/opacity (compositor-only properties)
// Bad: Changes layout
element.style.left = '100px';

// Good: Only composite
element.style.transform = 'translateX(100px)';

// Debounce scroll/resize handlers
const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

window.addEventListener('scroll', debounce(handleScroll, 100));
```

**Critical Rendering Path:**
- Minimize render-blocking resources
- Inline critical CSS
- Defer non-critical JavaScript
- Optimize images

### 27. Explain Service Workers and offline functionality.

**Answer:**
Service Workers enable offline functionality and background processing.

**Registration:**
```javascript
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(registration => {
            console.log('SW registered:', registration);
        })
        .catch(error => {
            console.log('SW registration failed:', error);
        });
}
```

**Service Worker:**
```javascript
// sw.js
const CACHE_NAME = 'v1';
const urlsToCache = [
    '/',
    '/styles.css',
    '/script.js'
];

// Install
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Fetch
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version or fetch
                return response || fetch(event.request);
            })
    );
});
```

**Cache Strategies:**
- **Cache First**: Check cache, then network
- **Network First**: Try network, fallback to cache
- **Stale While Revalidate**: Return cache, update in background

### 28. Explain Web Vitals and performance metrics.

**Answer:**
Web Vitals are key user experience metrics.

**Core Web Vitals:**
1. **LCP (Largest Contentful Paint)**: < 2.5s
   - Time to render largest content
2. **FID (First Input Delay)**: < 100ms
   - Time from first interaction to response
3. **CLS (Cumulative Layout Shift)**: < 0.1
   - Visual stability measure

**Measuring:**
```javascript
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);

// Or with analytics
function sendToAnalytics(metric) {
    // Send to analytics service
    analytics.track('web-vital', {
        name: metric.name,
        value: metric.value,
        id: metric.id
    });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
```

**Other Metrics:**
- **TTFB (Time to First Byte)**: < 800ms
- **FCP (First Contentful Paint)**: < 1.8s
- **TBT (Total Blocking Time)**: < 200ms

### 29. Explain frontend build tools comparison (Webpack vs Vite vs Parcel).

**Answer:**
**Webpack:**
- Mature, extensive ecosystem
- Complex configuration
- Slower dev server
- Bundle-based

**Vite:**
- Fast HMR (Hot Module Replacement)
- Native ES modules
- Simple configuration
- Faster builds

**Parcel:**
- Zero configuration
- Fast builds
- Built-in optimizations
- Less flexible

**Comparison:**
```javascript
// Webpack config
module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            { test: /\.js$/, use: 'babel-loader' }
        ]
    }
};

// Vite config (simpler)
export default {
    build: {
        outDir: 'dist'
    }
};
```

### 30. Explain frontend state management patterns.

**Answer:**
**Local State:**
```javascript
const [count, setCount] = useState(0);
```

**Context API:**
```javascript
const ThemeContext = createContext();

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}
```

**Redux Pattern:**
```javascript
// Actions
const increment = () => ({ type: 'INCREMENT' });

// Reducer
const counter = (state = 0, action) => {
    switch (action.type) {
        case 'INCREMENT':
            return state + 1;
        default:
            return state;
    }
};

// Store
const store = createStore(counter);
```

**Zustand (Lightweight):**
```javascript
import create from 'zustand';

const useStore = create(set => ({
    count: 0,
    increment: () => set(state => ({ count: state.count + 1 }))
}));
```

### 31. Explain CSS Specificity in detail.

**Answer:**
Specificity determines which CSS rule applies when multiple rules target same element.

**Specificity Calculation:**
- Inline styles: 1000
- IDs: 100
- Classes, attributes, pseudo-classes: 10
- Elements, pseudo-elements: 1

**Examples:**
```css
/* Specificity: 1 */
div { color: red; }

/* Specificity: 10 */
.container { color: blue; }

/* Specificity: 11 */
div.container { color: green; }

/* Specificity: 100 */
#header { color: yellow; }

/* Specificity: 110 */
#header .container { color: purple; }

/* Specificity: 1000 */
<div style="color: orange;"> /* Inline */
```

**Important:**
```css
/* !important overrides everything */
div { color: red !important; }
```

### 32. Explain CSS BEM Methodology.

**Answer:**
BEM (Block Element Modifier) naming convention.

**Structure:**
- Block: Standalone component
- Element: Part of block
- Modifier: Variation of block/element

**Example:**
```css
/* Block */
.button { }

/* Element */
.button__icon { }
.button__text { }

/* Modifier */
.button--primary { }
.button--large { }
.button--disabled { }
```

**HTML:**
```html
<button class="button button--primary button--large">
    <span class="button__icon">✓</span>
    <span class="button__text">Submit</span>
</button>
```

### 33. Explain CSS Custom Properties (Variables).

**Answer:**
CSS variables for reusable values.

```css
:root {
    --primary-color: #007bff;
    --font-size: 16px;
    --spacing: 1rem;
}

.element {
    color: var(--primary-color);
    font-size: var(--font-size);
    margin: var(--spacing);
}

/* With fallback */
.element {
    color: var(--primary-color, #000);
}

/* Scoped variables */
.component {
    --local-color: red;
    color: var(--local-color);
}
```

**JavaScript:**
```javascript
// Get
const color = getComputedStyle(document.documentElement)
    .getPropertyValue('--primary-color');

// Set
document.documentElement.style.setProperty('--primary-color', '#ff0000');
```

### 34. Explain CSS Animations vs Transitions.

**Answer:**
**Transitions:**
```css
.element {
    transition: property duration timing-function delay;
    transition: width 0.3s ease-in-out;
}

.element:hover {
    width: 200px;
}
```

**Animations:**
```css
@keyframes slide {
    from { transform: translateX(0); }
    to { transform: translateX(100px); }
}

.element {
    animation: slide 1s ease-in-out infinite;
    animation-name: slide;
    animation-duration: 1s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
}
```

**Differences:**
- **Transitions**: Simple property changes, triggered by state
- **Animations**: Complex sequences, can loop, more control

### 35. Explain CSS Grid vs Flexbox.

**Answer:**
**Flexbox (1D):**
```css
.container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
```

**Grid (2D):**
```css
.container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: auto;
    gap: 20px;
}
```

**When to use:**
- **Flexbox**: 1D layouts, component alignment
- **Grid**: 2D layouts, page structure

### 36. Explain Web Accessibility (a11y).

**Answer:**
Making web accessible to people with disabilities.

**Semantic HTML:**
```html
<!-- Bad -->
<div onclick="...">Click me</div>

<!-- Good -->
<button>Click me</button>
```

**ARIA Attributes:**
```html
<button aria-label="Close dialog">×</button>
<div role="alert" aria-live="polite">Error message</div>
```

**Keyboard Navigation:**
```css
/* Focus styles */
button:focus {
    outline: 2px solid blue;
}
```

**Alt Text:**
```html
<img src="photo.jpg" alt="Description of image">
```

### 37. Explain Progressive Web Apps (PWA).

**Answer:**
Web apps that work like native apps.

**Service Worker:**
```javascript
// Register
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
}

// sw.js
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll(['/index.html', '/style.css']);
        })
    );
});
```

**Manifest:**
```json
{
    "name": "My App",
    "short_name": "App",
    "start_url": "/",
    "display": "standalone",
    "icons": [...]
}
```

**Features:**
- Offline support
- Installable
- Push notifications
- Background sync

### 38. Explain Web Performance Optimization.

**Answer:**
**Techniques:**
1. **Minification**: Reduce file size
2. **Compression**: Gzip/Brotli
3. **Caching**: Browser cache, CDN
4. **Lazy Loading**: Load on demand
5. **Code Splitting**: Split bundles
6. **Image Optimization**: WebP, lazy load
7. **Critical CSS**: Inline above fold

**Lazy Loading:**
```html
<img src="image.jpg" loading="lazy" alt="...">
```

**Code Splitting:**
```javascript
const Component = lazy(() => import('./Component'));
```

### 39. Explain Cross-Origin Resource Sharing (CORS).

**Answer:**
CORS allows cross-origin requests.

**Server Response:**
```javascript
// Express.js
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});
```

**Preflight Request:**
```javascript
// Browser sends OPTIONS request first
// Server responds with allowed methods/headers
```

**CORS Errors:**
- Missing CORS headers
- Credentials not allowed
- Method not allowed

### 40. Explain Web Security Best Practices.

**Answer:**
**1. HTTPS:**
- Encrypt data in transit
- SSL/TLS certificates

**2. Content Security Policy (CSP):**
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

**3. XSS Prevention:**
```javascript
// Sanitize user input
function sanitize(input) {
    return input.replace(/<script>/g, '');
}
```

**4. CSRF Protection:**
```javascript
// CSRF tokens
const token = generateCSRFToken();
```

**5. Input Validation:**
- Validate on client and server
- Sanitize inputs
- Use parameterized queries

### 41. Explain CSS Selectors and their specificity.

**Answer:**
**Selector Types:**
```css
/* Element */
div { }

/* Class */
.container { }

/* ID */
#header { }

/* Attribute */
[type="text"] { }

/* Pseudo-class */
:hover { }

/* Pseudo-element */
::before { }

/* Descendant */
div p { }

/* Child */
div > p { }

/* Adjacent sibling */
div + p { }

/* General sibling */
div ~ p { }
```

**Specificity Order:**
1. Inline styles (1000)
2. IDs (100)
3. Classes, attributes, pseudo-classes (10)
4. Elements, pseudo-elements (1)

### 42. Explain CSS Position Property.

**Answer:**
**Static (Default):**
```css
.element {
    position: static; /* Normal flow */
}
```

**Relative:**
```css
.element {
    position: relative;
    top: 10px; /* Offset from normal position */
    left: 20px;
}
```

**Absolute:**
```css
.element {
    position: absolute;
    top: 0;
    right: 0; /* Relative to nearest positioned ancestor */
}
```

**Fixed:**
```css
.element {
    position: fixed;
    top: 0; /* Relative to viewport */
}
```

**Sticky:**
```css
.element {
    position: sticky;
    top: 0; /* Sticks when scrolling */
}
```

### 43. Explain CSS Display Property.

**Answer:**
**Block:**
```css
.element {
    display: block; /* Full width, new line */
}
```

**Inline:**
```css
.element {
    display: inline; /* Width of content, no new line */
}
```

**Inline-Block:**
```css
.element {
    display: inline-block; /* Inline but can set width/height */
}
```

**None:**
```css
.element {
    display: none; /* Removed from layout */
}
```

**Flex:**
```css
.element {
    display: flex; /* Flexbox layout */
}
```

**Grid:**
```css
.element {
    display: grid; /* Grid layout */
}
```

### 44. Explain CSS Z-Index and Stacking Context.

**Answer:**
**Z-Index:**
```css
.element1 {
    z-index: 1; /* Higher value = on top */
}

.element2 {
    z-index: 2; /* Above element1 */
}
```

**Stacking Context:**
- Created by: positioned elements with z-index, opacity < 1, transform, etc.
- Each context has its own stacking order

```css
.parent {
    position: relative;
    z-index: 1; /* Creates stacking context */
}

.child {
    z-index: 999; /* Only within parent's context */
}
```

### 45. Explain CSS Media Queries.

**Answer:**
**Basic:**
```css
@media (max-width: 768px) {
    .container {
        width: 100%;
    }
}
```

**Multiple Conditions:**
```css
@media (min-width: 768px) and (max-width: 1024px) {
    .container {
        width: 750px;
    }
}
```

**Orientation:**
```css
@media (orientation: landscape) {
    .container {
        flex-direction: row;
    }
}
```

**Print:**
```css
@media print {
    .no-print {
        display: none;
    }
}
```

### 46. Explain HTML5 Semantic Elements.

**Answer:**
**Semantic Elements:**
```html
<header>Header content</header>
<nav>Navigation</nav>
<main>Main content</main>
<article>Independent content</article>
<section>Section of content</section>
<aside>Sidebar content</aside>
<footer>Footer content</footer>
```

**Benefits:**
- Better SEO
- Accessibility
- Code readability
- Screen readers

### 47. Explain HTML Forms and Input Types.

**Answer:**
**Input Types:**
```html
<input type="text" />
<input type="email" />
<input type="password" />
<input type="number" />
<input type="date" />
<input type="checkbox" />
<input type="radio" />
<input type="file" />
<input type="range" />
<input type="color" />
```

**Form Validation:**
```html
<form>
    <input type="email" required />
    <input type="number" min="0" max="100" />
    <input type="text" pattern="[A-Za-z]{3}" />
    <button type="submit">Submit</button>
</form>
```

### 48. Explain CSS Preprocessors (SASS/SCSS).

**Answer:**
**Variables:**
```scss
$primary-color: #007bff;
$font-size: 16px;

.button {
    color: $primary-color;
    font-size: $font-size;
}
```

**Nesting:**
```scss
.nav {
    ul {
        list-style: none;
        li {
            display: inline-block;
        }
    }
}
```

**Mixins:**
```scss
@mixin flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.container {
    @include flex-center;
}
```

### 49. Explain CSS Architecture (OOCSS, SMACSS, BEM).

**Answer:**
**OOCSS (Object-Oriented CSS):**
- Separate structure from skin
- Separate container from content

**SMACSS (Scalable and Modular Architecture):**
- Base, Layout, Module, State, Theme

**BEM (Block Element Modifier):**
```css
.block { }
.block__element { }
.block--modifier { }
```

### 50. Explain Browser Rendering Process.

**Answer:**
**Steps:**
1. **Parse HTML**: Build DOM tree
2. **Parse CSS**: Build CSSOM tree
3. **Render Tree**: Combine DOM + CSSOM
4. **Layout**: Calculate positions (reflow)
5. **Paint**: Fill pixels
6. **Composite**: Layer composition

**Optimization:**
- Minimize reflows/repaints
- Use transform/opacity for animations
- Avoid layout thrashing

---

This covers frontend interview questions from beginner to advanced level with comprehensive coverage.

