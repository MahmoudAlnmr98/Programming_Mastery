# Next.js Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. What is Next.js? Explain its key features.

**Answer:**
Next.js is a React framework for production with built-in optimizations.

**Key Features:**
- **Server-Side Rendering (SSR)**: Render pages on server
- **Static Site Generation (SSG)**: Pre-render pages at build time
- **API Routes**: Build API endpoints
- **File-based Routing**: Automatic routing from file structure
- **Image Optimization**: Automatic image optimization
- **Code Splitting**: Automatic code splitting
- **TypeScript Support**: Built-in TypeScript support

### 2. Explain the difference between SSR, SSG, and CSR.

**Answer:**
- **SSR (Server-Side Rendering)**: Render on server for each request
  - `getServerSideProps`
  - Fresh data on each request
  - Slower initial load

- **SSG (Static Site Generation)**: Pre-render at build time
  - `getStaticProps`
  - Fast, can be cached by CDN
  - Data may be stale

- **CSR (Client-Side Rendering)**: Render in browser
  - Traditional React
  - Slower initial load
  - Better interactivity

### 3. Explain Next.js routing.

**Answer:**
Next.js uses file-based routing.

```javascript
// pages/index.js → /
// pages/about.js → /about
// pages/blog/[id].js → /blog/:id
// pages/blog/[...slug].js → /blog/* (catch-all)
// pages/blog/[[...slug]].js → /blog/* (optional catch-all)
```

**Dynamic Routes:**
```javascript
// pages/posts/[id].js
import { useRouter } from 'next/router';

export default function Post() {
    const router = useRouter();
    const { id } = router.query;
    return <div>Post {id}</div>;
}
```

### 4. Explain `getStaticProps` and `getStaticPaths`.

**Answer:**
**getStaticProps**: Fetch data at build time
```javascript
export async function getStaticProps(context) {
    const data = await fetchData();
    return {
        props: { data },
        revalidate: 60 // ISR: revalidate every 60 seconds
    };
}
```

**getStaticPaths**: Define which paths to pre-render
```javascript
export async function getStaticPaths() {
    const paths = await getAllPostIds();
    return {
        paths: paths.map(id => ({ params: { id } })),
        fallback: false // or 'blocking' or true
    };
}
```

### 5. Explain `getServerSideProps`.

**Answer:**
Fetch data on each request (SSR).

```javascript
export async function getServerSideProps(context) {
    const { params, req, res, query } = context;
    const data = await fetchData(params.id);
    
    return {
        props: { data }
    };
}
```

**Use Cases:**
- Data changes frequently
- User-specific data
- Need request headers/cookies

### 6. Explain API Routes in Next.js.

**Answer:**
API routes are serverless functions.

```javascript
// pages/api/users.js
export default function handler(req, res) {
    if (req.method === 'GET') {
        res.status(200).json({ users: [] });
    } else if (req.method === 'POST') {
        const user = createUser(req.body);
        res.status(201).json(user);
    }
}
```

**Dynamic API Routes:**
```javascript
// pages/api/users/[id].js
export default function handler(req, res) {
    const { id } = req.query;
    // Handle request
}
```

### 7. Explain Image Optimization in Next.js.

**Answer:**
Next.js automatically optimizes images.

```javascript
import Image from 'next/image';

<Image
    src="/image.jpg"
    alt="Description"
    width={500}
    height={300}
    priority // Load immediately
    placeholder="blur"
/>
```

**Benefits:**
- Automatic format optimization (WebP)
- Lazy loading
- Responsive images
- Prevents layout shift

### 8. Explain Next.js Link component.

**Answer:**
Link component provides client-side navigation.

```javascript
import Link from 'next/link';

<Link href="/about">
    <a>About</a>
</Link>

// With dynamic route
<Link href="/posts/[id]" as="/posts/123">
    <a>Post</a>
</Link>

// Prefetch (default: true)
<Link href="/about" prefetch={false}>
    <a>About</a>
</Link>
```

---

## Intermediate Level

### 9. Explain Incremental Static Regeneration (ISR).

**Answer:**
ISR allows updating static pages without rebuilding.

```javascript
export async function getStaticProps() {
    const data = await fetchData();
    return {
        props: { data },
        revalidate: 60 // Revalidate every 60 seconds
    };
}
```

**How it works:**
1. Page generated at build time
2. After revalidate time, next request triggers regeneration
3. New page served to subsequent requests

### 10. Explain middleware in Next.js.

**Answer:**
Middleware runs before request is completed.

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
    // Redirect
    if (request.nextUrl.pathname === '/old') {
        return NextResponse.redirect(new URL('/new', request.url));
    }
    
    // Rewrite
    if (request.nextUrl.pathname === '/api') {
        return NextResponse.rewrite(new URL('/api/proxy', request.url));
    }
    
    // Add headers
    const response = NextResponse.next();
    response.headers.set('x-custom-header', 'value');
    return response;
}

export const config = {
    matcher: '/about/:path*',
};
```

### 11. Explain Next.js App Router (App Directory).

**Answer:**
New routing system in Next.js 13+.

```javascript
// app/layout.js - Root layout
export default function RootLayout({ children }) {
    return (
        <html>
            <body>{children}</body>
        </html>
    );
}

// app/page.js - Home page
export default function Home() {
    return <div>Home</div>;
}

// app/about/page.js - About page
export default function About() {
    return <div>About</div>;
}
```

**Server Components:**
```javascript
// app/components/ServerComponent.js
// Runs on server, no 'use client'
export default async function ServerComponent() {
    const data = await fetchData();
    return <div>{data}</div>;
}
```

**Client Components:**
```javascript
'use client';

import { useState } from 'react';

export default function ClientComponent() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### 12. Explain data fetching in Next.js App Router.

**Answer:**
**Server Components:**
```javascript
// app/posts/page.js
async function getPosts() {
    const res = await fetch('https://api.example.com/posts');
    return res.json();
}

export default async function Posts() {
    const posts = await getPosts();
    return (
        <ul>
            {posts.map(post => (
                <li key={post.id}>{post.title}</li>
            ))}
        </ul>
    );
}
```

**Loading States:**
```javascript
// app/posts/loading.js
export default function Loading() {
    return <div>Loading...</div>;
}
```

**Error Handling:**
```javascript
// app/posts/error.js
'use client';

export default function Error({ error, reset }) {
    return (
        <div>
            <h2>Something went wrong!</h2>
            <button onClick={() => reset()}>Try again</button>
        </div>
    );
}
```

### 13. Explain Next.js optimization features.

**Answer:**
**1. Automatic Code Splitting:**
- Each page is automatically code-split
- Only loads code needed for that page

**2. Font Optimization:**
```javascript
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });
```

**3. Script Optimization:**
```javascript
import Script from 'next/script';

<Script
    src="https://example.com/script.js"
    strategy="lazyOnload"
/>
```

**4. Bundle Analysis:**
```bash
npm install @next/bundle-analyzer
```

### 14. Explain Next.js environment variables.

**Answer:**
```javascript
// .env.local
DATABASE_URL=postgres://...
API_KEY=secret

// Access in code
const dbUrl = process.env.DATABASE_URL;

// Public variables (exposed to browser)
NEXT_PUBLIC_API_URL=https://api.example.com
```

**Loading Order:**
1. `.env`
2. `.env.local`
3. `.env.development` / `.env.production`
4. `.env.development.local` / `.env.production.local`

### 15. Explain Next.js deployment.

**Answer:**
**Vercel (Recommended):**
```bash
npm install -g vercel
vercel
```

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

**Static Export:**
```javascript
// next.config.js
module.exports = {
    output: 'export',
};
```

---

## Advanced Level

### 16. Explain Next.js caching strategies.

**Answer:**
**Request Memoization:**
```javascript
// Same fetch in same request is deduplicated
async function getData() {
    const res = await fetch('https://api.example.com/data');
    return res.json();
}
```

**Data Cache:**
```javascript
// Cached by default
fetch('https://api.example.com/data');

// Revalidate
fetch('https://api.example.com/data', {
    next: { revalidate: 60 }
});

// No cache
fetch('https://api.example.com/data', {
    cache: 'no-store'
});
```

**Full Route Cache:**
- Static pages are cached
- Can be invalidated with `revalidatePath`

### 17. Explain Next.js internationalization (i18n).

**Answer:**
```javascript
// next.config.js
module.exports = {
    i18n: {
        locales: ['en', 'fr', 'es'],
        defaultLocale: 'en',
    },
};

// Usage
import { useRouter } from 'next/router';

const router = useRouter();
const { locale, locales, defaultLocale } = router;
```

### 18. Explain Next.js authentication patterns.

**Answer:**
**NextAuth.js:**
```javascript
// pages/api/auth/[...nextauth].js
import NextAuth from 'next-auth';

export default NextAuth({
    providers: [
        // Configure providers
    ],
});
```

**Middleware Protection:**
```javascript
// middleware.js
export function middleware(request) {
    if (!request.cookies.get('token')) {
        return NextResponse.redirect(new URL('/login', request.url));
    }
}
```

### 19. Explain Next.js performance monitoring.

**Answer:**
**Web Vitals:**
```javascript
// pages/_app.js
export function reportWebVitals(metric) {
    console.log(metric);
    // Send to analytics
}
```

**Custom Analytics:**
```javascript
import { Analytics } from '@vercel/analytics/react';

export default function App() {
    return (
        <>
            <Component />
            <Analytics />
        </>
    );
}
```

### 20. Explain Next.js testing strategies.

**Answer:**
**Jest + React Testing Library:**
```javascript
import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

test('renders home page', () => {
    render(<Home />);
    expect(screen.getByText('Welcome')).toBeInTheDocument();
});
```

**E2E Testing with Playwright:**
```javascript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h1')).toContainText('Welcome');
});
```

### 21. Explain Next.js Image component optimization.

**Answer:**
Next.js Image component provides automatic optimization.

```javascript
import Image from 'next/image';

<Image
    src="/image.jpg"
    alt="Description"
    width={500}
    height={300}
    quality={90}
    priority={false}
    placeholder="blur"
    blurDataURL="data:image/jpeg;base64,..."
    sizes="(max-width: 768px) 100vw, 50vw"
/>
```

**Features:**
- Automatic format optimization (WebP, AVIF)
- Responsive images
- Lazy loading
- Prevents layout shift

### 22. Explain Next.js middleware advanced usage.

**Answer:**
Middleware can handle complex routing and authentication.

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
    // A/B testing
    const variant = request.cookies.get('variant') || 'A';
    
    // Feature flags
    if (request.nextUrl.pathname.startsWith('/beta')) {
        const hasAccess = checkBetaAccess(request);
        if (!hasAccess) {
            return NextResponse.redirect(new URL('/', request.url));
        }
    }
    
    // Request modification
    const response = NextResponse.next();
    response.headers.set('x-custom-header', 'value');
    return response;
}
```

### 23. Explain Next.js static export and deployment.

**Answer:**
**Static Export:**
```javascript
// next.config.js
module.exports = {
    output: 'export',
    images: {
        unoptimized: true
    }
};
```

**Deployment Options:**
- **Vercel**: Optimized for Next.js
- **Netlify**: Static site hosting
- **AWS Amplify**: Full-stack deployment
- **Docker**: Containerized deployment

### 24. Explain Next.js internationalization (i18n) routing.

**Answer:**
```javascript
// next.config.js
module.exports = {
    i18n: {
        locales: ['en', 'fr', 'es'],
        defaultLocale: 'en',
        localeDetection: false
    }
};

// Usage
import { useRouter } from 'next/router';

const router = useRouter();
const { locale, locales, defaultLocale } = router;

// Change locale
router.push('/', '/', { locale: 'fr' });
```

### 25. Explain Next.js error boundaries and error handling.

**Answer:**
**Error Boundary (Pages Router):**
```javascript
// _error.js
function Error({ statusCode }) {
    return (
        <p>
            {statusCode
                ? `An error ${statusCode} occurred on server`
                : 'An error occurred on client'}
        </p>
    );
}
```

**Error Handling (App Router):**
```javascript
// app/error.js
'use client';

export default function Error({ error, reset }) {
    return (
        <div>
            <h2>Something went wrong!</h2>
            <button onClick={() => reset()}>Try again</button>
        </div>
    );
}
```

### 26. Explain Next.js API routes best practices.

**Answer:**
API routes provide backend functionality.

**Basic Route:**
```javascript
// pages/api/users.js
export default function handler(req, res) {
    if (req.method === 'GET') {
        res.status(200).json({ users: [] });
    } else {
        res.setHeader('Allow', ['GET']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
```

**Dynamic Routes:**
```javascript
// pages/api/users/[id].js
export default function handler(req, res) {
    const { id } = req.query;
    
    if (req.method === 'GET') {
        res.status(200).json({ id, name: 'User' });
    }
}
```

**Best Practices:**
- Validate input
- Handle errors properly
- Use proper HTTP methods
- Set appropriate headers
- Implement authentication
- Rate limiting

**Example:**
```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100
});

export default async function handler(req, res) {
    await limiter(req, res);
    
    try {
        const data = await fetchData();
        res.status(200).json(data);
    } catch (error) {
        res.status(500).json({ error: 'Internal Server Error' });
    }
}
```

### 27. Explain Next.js middleware and edge functions.

**Answer:**
Middleware runs before request completes.

**Middleware:**
```javascript
// middleware.js
export function middleware(request) {
    // Redirect
    if (request.nextUrl.pathname === '/old') {
        return NextResponse.redirect(new URL('/new', request.url));
    }
    
    // Add headers
    const response = NextResponse.next();
    response.headers.set('x-custom-header', 'value');
    return response;
}

// Matcher
export const config = {
    matcher: '/about/:path*',
};
```

**Edge Functions:**
```javascript
// pages/api/edge.js
export const config = {
    runtime: 'edge',
};

export default function handler(req) {
    return new Response('Hello from Edge!', {
        headers: { 'content-type': 'text/plain' },
    });
}
```

**Use Cases:**
- Authentication
- Redirects
- A/B testing
- Geolocation
- Request modification

### 28. Explain Next.js optimization techniques.

**Answer:**
**Image Optimization:**
```jsx
import Image from 'next/image';

<Image
    src="/image.jpg"
    width={500}
    height={300}
    alt="Description"
    priority // Load immediately
    placeholder="blur"
    blurDataURL="..."
/>
```

**Font Optimization:**
```javascript
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function Layout({ children }) {
    return (
        <div className={inter.className}>
            {children}
        </div>
    );
}
```

**Script Optimization:**
```jsx
import Script from 'next/script';

<Script
    src="https://example.com/script.js"
    strategy="lazyOnload"
    onLoad={() => console.log('Loaded')}
/>
```

**Bundle Analysis:**
```bash
npm install @next/bundle-analyzer
```

### 29. Explain Next.js deployment strategies.

**Answer:**
**Vercel (Recommended):**
```bash
vercel
```

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

**Static Export:**
```javascript
// next.config.js
module.exports = {
    output: 'export',
    images: {
        unoptimized: true
    }
};
```

**Environment Variables:**
```javascript
// .env.local
DATABASE_URL=...
NEXT_PUBLIC_API_URL=...

// Usage
const dbUrl = process.env.DATABASE_URL;
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### 30. Explain Next.js testing strategies.

**Answer:**
**Unit Testing:**
```javascript
import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

test('renders homepage', () => {
    render(<Home />);
    expect(screen.getByText('Welcome')).toBeInTheDocument();
});
```

**API Route Testing:**
```javascript
import { createMocks } from 'node-mocks-http';
import handler from '../pages/api/users';

test('GET /api/users', async () => {
    const { req, res } = createMocks({
        method: 'GET'
    });
    
    await handler(req, res);
    expect(res._getStatusCode()).toBe(200);
});
```

**E2E Testing:**
```javascript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page).toHaveTitle(/Next.js/);
});
```

---

This covers Next.js interview questions from beginner to advanced level with detailed explanations and code examples.

