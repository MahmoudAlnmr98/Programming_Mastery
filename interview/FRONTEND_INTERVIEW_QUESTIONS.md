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

---

This covers frontend interview questions from beginner to advanced level.

