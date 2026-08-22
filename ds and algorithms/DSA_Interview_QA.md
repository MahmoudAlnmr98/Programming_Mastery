# Data Structures & Algorithms — Interview Questions & Answers
> 130 questions. Full code with complexity analysis. Easy → Medium → Hard.

---

## Table of Contents
- [Easy (Q1–Q40)](#easy)
- [Medium (Q41–Q85)](#medium)
- [Hard (Q86–Q130)](#hard)

---

## EASY QUESTIONS

**Q1. What is Big O notation?**
```
O(1) Constant  — array index, hash get
O(log n) Log   — binary search, BST ops
O(n) Linear    — single loop, linear scan
O(n log n)     — merge/heap/quick sort
O(n²) Quadratic— nested loops
O(2ⁿ) Exponential — recursion, subsets
O(n!) Factorial — permutations

Rules: drop constants, drop lower terms, worst case unless stated
```

**Q2. Arrays — complexities and two-pointer.**
```javascript
// Access: O(1) | Search: O(n) | Insert end: O(1) amortized | Insert middle: O(n)

// Two-pointer — pair summing to target in sorted array: O(n)
function twoSum(arr, target) {
  let l = 0, r = arr.length - 1;
  while (l < r) {
    const s = arr[l] + arr[r];
    if (s === target) return [l, r];
    s < target ? l++ : r--;
  }
  return null;
}

// Sliding window — max sum subarray of size k: O(n)
function maxSumK(arr, k) {
  let sum = arr.slice(0, k).reduce((a, b) => a + b, 0), max = sum;
  for (let i = k; i < arr.length; i++) {
    sum += arr[i] - arr[i - k];
    max = Math.max(max, sum);
  }
  return max;
}
```

**Q3. Linked List — implementation and complexities.**
```javascript
class ListNode { constructor(val, next=null){this.val=val;this.next=next;} }

// Prepend O(1) | Append O(n) | Search O(n) | Delete at known node O(1)

// Reverse iteratively: O(n) time, O(1) space
function reverse(head) {
  let prev = null, curr = head;
  while (curr) { const next = curr.next; curr.next = prev; prev = curr; curr = next; }
  return prev;
}

// Find middle (slow/fast pointers):
function middle(head) {
  let s = head, f = head;
  while (f?.next) { s = s.next; f = f.next.next; }
  return s;
}
```

**Q4. Stack and Queue.**
```javascript
// Stack (LIFO): use array with push/pop — O(1)
// Queue (FIFO): use array but shift() is O(n) — use deque or linked list

class Queue {
  #d = []; #h = 0;
  enqueue(x) { this.#d.push(x); }
  dequeue()  { return this.#h >= this.#d.length ? undefined : this.#d[this.#h++]; }
  peek()     { return this.#d[this.#h]; }
  isEmpty()  { return this.#h >= this.#d.length; }
}

// Valid parentheses using stack:
function isValid(s) {
  const st = [], m = {')':'(',']':'[','}':'{'};
  for (const c of s) {
    if ('([{'.includes(c)) st.push(c);
    else if (st.pop() !== m[c]) return false;
  }
  return st.length === 0;
}
```

**Q5. Hash Table — collision resolution.**
```javascript
// Chaining: each bucket is a list. Average O(1), worst O(n)
// Open addressing: linear probe, quadratic probe, double hash

// JavaScript built-in Map is O(1) average for all ops:
const freq = new Map();
for (const c of "hello") freq.set(c, (freq.get(c) ?? 0) + 1);

// Object.create(null) for pure dict without prototype pollution:
const dict = Object.create(null);
dict["constructor"] = "safe"; // no prototype conflict
```

**Q6. Binary Search — all variants.**
```javascript
function binarySearch(arr, target) {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = lo + ((hi - lo) >> 1);
    if (arr[mid] === target) return mid;
    arr[mid] < target ? lo = mid + 1 : hi = mid - 1;
  }
  return -1;
}

// First occurrence:
function lowerBound(arr, target) {
  let lo = 0, hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    arr[mid] < target ? lo = mid + 1 : hi = mid;
  }
  return lo;
}

// Last occurrence:
function upperBound(arr, target) {
  let lo = 0, hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    arr[mid] <= target ? lo = mid + 1 : hi = mid;
  }
  return lo - 1;
}

// Binary search on answer space:
function minEatingSpeed(piles, h) {
  let lo = 1, hi = Math.max(...piles);
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    const hours = piles.reduce((s, p) => s + Math.ceil(p/mid), 0);
    hours <= h ? hi = mid : lo = mid + 1;
  }
  return lo;
}
```

**Q7. Tree traversals.**
```javascript
class TreeNode { constructor(val,l=null,r=null){this.val=val;this.left=l;this.right=r;} }

const inOrder   = (n, r=[]) => { if(!n) return r; inOrder(n.left,r); r.push(n.val); inOrder(n.right,r); return r; };
const preOrder  = (n, r=[]) => { if(!n) return r; r.push(n.val); preOrder(n.left,r); preOrder(n.right,r); return r; };
const postOrder = (n, r=[]) => { if(!n) return r; postOrder(n.left,r); postOrder(n.right,r); r.push(n.val); return r; };

// BFS / Level order:
function levelOrder(root) {
  if (!root) return [];
  const res = [], q = [root];
  while (q.length) {
    const level = [], size = q.length;
    for (let i = 0; i < size; i++) {
      const n = q.shift();
      level.push(n.val);
      if (n.left) q.push(n.left);
      if (n.right) q.push(n.right);
    }
    res.push(level);
  }
  return res;
}
```

**Q8. Binary Search Tree.**
```javascript
class BST {
  root = null;
  insert(val, n = this.root) {
    if (!n) { if (!this.root) this.root = new TreeNode(val); return; }
    val < n.val ? (n.left ? this.insert(val, n.left) : (n.left = new TreeNode(val)))
                : (n.right ? this.insert(val, n.right) : (n.right = new TreeNode(val)));
  }
  search(val, n = this.root) {
    if (!n) return false;
    if (n.val === val) return true;
    return val < n.val ? this.search(val, n.left) : this.search(val, n.right);
  }
}

// Validate BST: O(n)
function isValidBST(node, min=-Infinity, max=Infinity) {
  if (!node) return true;
  if (node.val <= min || node.val >= max) return false;
  return isValidBST(node.left, min, node.val) && isValidBST(node.right, node.val, max);
}
```

**Q9. Min/Max Heap.**
```javascript
class MinHeap {
  #h = [];
  push(v)  { this.#h.push(v); this.#up(this.#h.length-1); }
  pop()    { const m=this.#h[0]; this.#h[0]=this.#h.pop(); if(this.#h.length)this.#dn(0); return m; }
  peek()   { return this.#h[0]; }
  get size(){ return this.#h.length; }
  get isEmpty(){ return !this.#h.length; }
  #up(i) { while(i>0){const p=(i-1)>>1; if(this.#h[p]>this.#h[i]){[this.#h[p],this.#h[i]]=[this.#h[i],this.#h[p]];i=p;}else break;} }
  #dn(i) { const n=this.#h.length; let m=i; const l=2*i+1,r=2*i+2; if(l<n&&this.#h[l]<this.#h[m])m=l; if(r<n&&this.#h[r]<this.#h[m])m=r; if(m!==i){[this.#h[i],this.#h[m]]=[this.#h[m],this.#h[i]];this.#dn(m);} }
}
// Push/pop: O(log n) | Peek: O(1) | Build: O(n)
```

**Q10. Graph representations.**
```javascript
// Adjacency List (sparse) — O(V+E) space
class Graph {
  adj = new Map();
  addVertex(v)       { this.adj.set(v, []); }
  addEdge(u, v, w=1) { this.adj.get(u).push({node:v,weight:w}); }
  neighbors(v)       { return this.adj.get(v)??[]; }
  get vertices()     { return [...this.adj.keys()]; }
}

// BFS — shortest path unweighted: O(V+E)
function bfs(g, start) {
  const vis=new Set([start]), q=[start], res=[];
  while(q.length){const u=q.shift();res.push(u);for(const{node:v}of g.neighbors(u)){if(!vis.has(v)){vis.add(v);q.push(v);}}}
  return res;
}

// DFS: O(V+E)
function dfs(g, u, vis=new Set(), res=[]) {
  vis.add(u); res.push(u);
  for(const{node:v}of g.neighbors(u)) if(!vis.has(v)) dfs(g,v,vis,res);
  return res;
}
```

**Q11–Q14. Sorting algorithms.**
```javascript
// Bubble sort: O(n²) worst, O(n) best | Stable | In-place
function bubbleSort(a){const n=a.length;for(let i=0;i<n-1;i++){let sw=false;for(let j=0;j<n-1-i;j++){if(a[j]>a[j+1]){[a[j],a[j+1]]=[a[j+1],a[j]];sw=true;}}if(!sw)break;}return a;}

// Insertion sort: O(n²) worst, O(n) best | Stable | In-place | Great for small/nearly-sorted
function insertionSort(a){for(let i=1;i<a.length;i++){const k=a[i];let j=i-1;while(j>=0&&a[j]>k){a[j+1]=a[j];j--;}a[j+1]=k;}return a;}

// Merge sort: O(n log n) always | Stable | O(n) space
function mergeSort(a){if(a.length<=1)return a;const m=a.length>>1,L=mergeSort(a.slice(0,m)),R=mergeSort(a.slice(m));const r=[];let i=0,j=0;while(i<L.length&&j<R.length)r.push(L[i]<=R[j]?L[i++]:R[j++]);return[...r,...L.slice(i),...R.slice(j)];}

// Quick sort: O(n log n) avg, O(n²) worst | Unstable | In-place
function quickSort(a,lo=0,hi=a.length-1){
  if(lo>=hi)return a;
  const p=partition(a,lo,hi);quickSort(a,lo,p-1);quickSort(a,p+1,hi);return a;
}
function partition(a,lo,hi){const pv=a[hi];let i=lo-1;for(let j=lo;j<hi;j++){if(a[j]<=pv){i++;[a[i],a[j]]=[a[j],a[i]];}}[a[i+1],a[hi]]=[a[hi],a[i+1]];return i+1;}
```

**Q15. Trie.**
```javascript
class Trie {
  root = {};
  insert(w) { let n=this.root; for(const c of w){n[c]=n[c]??{};n=n[c];}n.$=true; }
  search(w)  { let n=this.root; for(const c of w){if(!n[c])return false;n=n[c];}return!!n.$; }
  startsWith(p){ let n=this.root; for(const c of p){if(!n[c])return false;n=n[c];}return true; }
}
// All ops: O(m) where m = word length
// Space: O(ALPHABET × n × m) worst case
```

**Q16–Q25. More easy questions.**
```javascript
// Q16. Recursion — Fibonacci O(n) memoized:
function fib(n, m=new Map()) { if(n<=1)return n; if(m.has(n))return m.get(n); const r=fib(n-1,m)+fib(n-2,m); m.set(n,r); return r; }

// Q17. Counting sort O(n+k):
function countSort(arr, max) { const c=new Array(max+1).fill(0); for(const n of arr)c[n]++; return c.flatMap((cnt,val)=>Array(cnt).fill(val)); }

// Q18. Prefix sum — O(1) range query after O(n) build:
function prefixSum(nums) { const p=[0]; for(const n of nums)p.push(p.at(-1)+n); return p; }
function rangeSum(p,l,r) { return p[r+1]-p[l]; }

// Q19. Floyd's cycle detection O(n) time O(1) space:
function hasCycle(head) { let s=head,f=head; while(f?.next){s=s.next;f=f.next.next;if(s===f)return true;} return false; }

// Q20. Detect cycle start:
function cycleStart(head) {
  let s=head,f=head;
  while(f?.next){s=s.next;f=f.next.next;if(s===f){s=head;while(s!==f){s=s.next;f=f.next;}return s;}}
  return null;
}

// Q21. Find kth from end O(n):
function kthFromEnd(head,k){let a=head,b=head;for(let i=0;i<k;i++)b=b.next;while(b){a=a.next;b=b.next;}return a;}

// Q22. Merge two sorted lists O(n+m):
function mergeSorted(l1,l2){const d=new ListNode(0);let c=d;while(l1&&l2){if(l1.val<=l2.val){c.next=l1;l1=l1.next;}else{c.next=l2;l2=l2.next;}c=c.next;}c.next=l1??l2;return d.next;}

// Q23. String — anagram check O(n):
function isAnagram(s,t){if(s.length!==t.length)return false;const m={};for(const c of s)m[c]=(m[c]??0)+1;for(const c of t){if(!m[c])return false;m[c]--;}return true;}

// Q24. Max stack with O(1) getMax:
class MaxStack{#s=[];#max=[];push(x){this.#s.push(x);this.#max.push(Math.max(x,this.#max.at(-1)??-Infinity));}pop(){this.#max.pop();return this.#s.pop();}getMax(){return this.#max.at(-1);}}

// Q25. Number of islands DFS O(m×n):
function numIslands(grid){let count=0;const dfs=(r,c)=>{if(r<0||r>=grid.length||c<0||c>=grid[0].length||grid[r][c]==='0')return;grid[r][c]='0';[[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr,dc])=>dfs(r+dr,c+dc));};for(let r=0;r<grid.length;r++)for(let c=0;c<grid[0].length;c++)if(grid[r][c]==='1'){count++;dfs(r,c);}return count;}
```

**Q26–Q40. Pattern questions.**
```javascript
// Q26. Next greater element (monotonic stack) O(n):
function nextGreater(arr){const res=new Array(arr.length).fill(-1),st=[];for(let i=0;i<arr.length;i++){while(st.length&&arr[st.at(-1)]<arr[i])res[st.pop()]=arr[i];st.push(i);}return res;}

// Q27. Daily temperatures (monotonic stack):
function dailyTemps(T){const res=new Array(T.length).fill(0),st=[];for(let i=0;i<T.length;i++){while(st.length&&T[st.at(-1)]<T[i])res[st.pop()]=i-st.at(-1)-1+1;// simplified
// real: res[top]=i-top
st.push(i);}return res;}

// Corrected:
function dailyTemperatures(T){const res=new Array(T.length).fill(0),st=[];for(let i=0;i<T.length;i++){while(st.length&&T[i]>T[st.at(-1)]){const top=st.pop();res[top]=i-top;}st.push(i);}return res;}

// Q28. Subarray sum equals k (prefix sum + hashmap) O(n):
function subarraySum(nums,k){const map=new Map([[0,1]]);let sum=0,count=0;for(const n of nums){sum+=n;count+=map.get(sum-k)??0;map.set(sum,(map.get(sum)??0)+1);}return count;}

// Q29. Spiral matrix O(m×n):
function spiralOrder(matrix){const res=[];let t=0,b=matrix.length-1,l=0,r=matrix[0].length-1;while(t<=b&&l<=r){for(let i=l;i<=r;i++)res.push(matrix[t][i]);t++;for(let i=t;i<=b;i++)res.push(matrix[i][r]);r--;if(t<=b){for(let i=r;i>=l;i--)res.push(matrix[b][i]);b--;}if(l<=r){for(let i=b;i>=t;i--)res.push(matrix[i][l]);l++;}}return res;}

// Q30. Pascal's triangle:
function pascalTriangle(n){const res=[[1]];for(let i=1;i<n;i++){const row=[1];for(let j=1;j<i;j++)row.push(res[i-1][j-1]+res[i-1][j]);row.push(1);res.push(row);}return res;}

// Q31. Jump game (greedy) O(n):
function canJump(nums){let maxReach=0;for(let i=0;i<nums.length;i++){if(i>maxReach)return false;maxReach=Math.max(maxReach,i+nums[i]);}return true;}

// Q32. Rotate array O(n) O(1):
function rotate(nums,k){k%=nums.length;const rev=(a,l,r)=>{while(l<r){[a[l],a[r]]=[a[r],a[l]];l++;r--;}};rev(nums,0,nums.length-1);rev(nums,0,k-1);rev(nums,k,nums.length-1);}

// Q33. Product of array except self O(n) O(1) extra:
function productExceptSelf(nums){const res=new Array(nums.length).fill(1);let left=1;for(let i=0;i<nums.length;i++){res[i]=left;left*=nums[i];}let right=1;for(let i=nums.length-1;i>=0;i--){res[i]*=right;right*=nums[i];}return res;}

// Q34. Longest consecutive sequence O(n):
function longestConsecutive(nums){const s=new Set(nums);let best=0;for(const n of s){if(!s.has(n-1)){let len=1;while(s.has(n+len))len++;best=Math.max(best,len);}}return best;}

// Q35. 3Sum O(n²):
function threeSum(nums){nums.sort((a,b)=>a-b);const res=[];for(let i=0;i<nums.length-2;i++){if(i>0&&nums[i]===nums[i-1])continue;let l=i+1,r=nums.length-1;while(l<r){const s=nums[i]+nums[l]+nums[r];if(s===0){res.push([nums[i],nums[l],nums[r]]);while(nums[l]===nums[l+1])l++;while(nums[r]===nums[r-1])r--;l++;r--;}else if(s<0)l++;else r--;}}return res;}
```

---

## MEDIUM QUESTIONS

**Q41. Dijkstra's algorithm.**
```javascript
function dijkstra(graph, src) {
  const dist = new Map(), heap = new MinHeap((a,b)=>a[0]-b[0]);
  for (const v of graph.vertices) dist.set(v, Infinity);
  dist.set(src, 0);
  heap.push([0, src]);
  while (!heap.isEmpty) {
    const [d, u] = heap.pop();
    if (d > dist.get(u)) continue;
    for (const {node:v, weight:w} of graph.neighbors(u)) {
      const nd = d + w;
      if (nd < dist.get(v)) { dist.set(v, nd); heap.push([nd, v]); }
    }
  }
  return dist;
}
// O((V+E) log V)
```

**Q42. Topological Sort (Kahn's BFS).**
```javascript
function topoSort(graph) {
  const indeg = new Map();
  for (const v of graph.vertices) indeg.set(v, 0);
  for (const v of graph.vertices)
    for (const {node:u} of graph.neighbors(v)) indeg.set(u,(indeg.get(u)??0)+1);
  const q = [...graph.vertices].filter(v=>indeg.get(v)===0), order=[];
  while (q.length) {
    const v = q.shift(); order.push(v);
    for (const {node:u} of graph.neighbors(v)) {
      indeg.set(u, indeg.get(u)-1);
      if (indeg.get(u)===0) q.push(u);
    }
  }
  return order.length===graph.vertices.length ? order : null; // null = cycle
}
```

**Q43. Longest Common Subsequence O(m×n).**
```javascript
function lcs(s1, s2) {
  const m=s1.length, n=s2.length;
  const dp=Array.from({length:m+1},()=>new Array(n+1).fill(0));
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++)
    dp[i][j]=s1[i-1]===s2[j-1] ? dp[i-1][j-1]+1 : Math.max(dp[i-1][j],dp[i][j-1]);
  return dp[m][n];
}
```

**Q44. 0/1 Knapsack.**
```javascript
function knapsack(weights, values, W) {
  const dp = new Array(W+1).fill(0);
  for (let i=0; i<weights.length; i++)
    for (let w=W; w>=weights[i]; w--)  // backwards prevents reuse
      dp[w] = Math.max(dp[w], dp[w-weights[i]]+values[i]);
  return dp[W];
}
```

**Q45. LIS in O(n log n).**
```javascript
function lis(nums) {
  const tails = [];
  for (const n of nums) {
    let lo=0, hi=tails.length;
    while(lo<hi){const mid=(lo+hi)>>1; tails[mid]<n?lo=mid+1:hi=mid;}
    tails[lo]=n;
  }
  return tails.length;
}
```

**Q46. Union-Find with path compression + rank.**
```javascript
class UF {
  #p; #r; #c;
  constructor(n){this.#p=[...Array(n).keys()];this.#r=new Array(n).fill(0);this.#c=n;}
  find(x){if(this.#p[x]!==x)this.#p[x]=this.find(this.#p[x]);return this.#p[x];}
  union(x,y){const[px,py]=[this.find(x),this.find(y)];if(px===py)return false;if(this.#r[px]<this.#r[py])this.#p[px]=py;else if(this.#r[px]>this.#r[py])this.#p[py]=px;else{this.#p[py]=px;this.#r[px]++;}this.#c--;return true;}
  connected(x,y){return this.find(x)===this.find(y);}
  get components(){return this.#c;}
}
// Near O(α(n)) ≈ O(1) per operation amortized
```

**Q47. Merge intervals O(n log n).**
```javascript
function merge(intervals) {
  intervals.sort((a,b)=>a[0]-b[0]);
  const res=[intervals[0]];
  for(const [s,e] of intervals.slice(1)){
    const last=res.at(-1);
    s<=last[1] ? last[1]=Math.max(last[1],e) : res.push([s,e]);
  }
  return res;
}
```

**Q48. Minimum window substring O(n+m).**
```javascript
function minWindow(s, t) {
  const need=new Map(); for(const c of t)need.set(c,(need.get(c)??0)+1);
  let have=0,req=need.size,l=0,min=Infinity,res="";
  for(let r=0;r<s.length;r++){
    const c=s[r]; if(need.has(c)){need.set(c,need.get(c)-1);if(need.get(c)===0)have++;}
    while(have===req){if(r-l+1<min){min=r-l+1;res=s.slice(l,r+1);}const lc=s[l++];if(need.has(lc)){if(need.get(lc)===0)have--;need.set(lc,need.get(lc)+1);}}
  }
  return res;
}
```

**Q49. Word search in grid (backtracking) O(m×n×4^L).**
```javascript
function exist(board, word) {
  const [m,n]=[board.length,board[0].length];
  function dfs(r,c,i){
    if(i===word.length)return true;
    if(r<0||r>=m||c<0||c>=n||board[r][c]!==word[i])return false;
    const tmp=board[r][c]; board[r][c]='#';
    const found=[[1,0],[-1,0],[0,1],[0,-1]].some(([dr,dc])=>dfs(r+dr,c+dc,i+1));
    board[r][c]=tmp; return found;
  }
  for(let r=0;r<m;r++) for(let c=0;c<n;c++) if(dfs(r,c,0))return true;
  return false;
}
```

**Q50. LRU Cache O(1).**
```javascript
class LRUCache {
  #cap; #map=new Map();
  constructor(c){this.#cap=c;}
  get(k){if(!this.#map.has(k))return -1;const v=this.#map.get(k);this.#map.delete(k);this.#map.set(k,v);return v;}
  put(k,v){this.#map.delete(k);this.#map.set(k,v);if(this.#map.size>this.#cap)this.#map.delete(this.#map.keys().next().value);}
}
```

**Q51. Edit Distance O(m×n) → O(min(m,n)) space.**
```javascript
function editDist(s1, s2) {
  let prev=[...Array(s2.length+1).keys()];
  for(let i=1;i<=s1.length;i++){
    const curr=[i];
    for(let j=1;j<=s2.length;j++)
      curr[j]=s1[i-1]===s2[j-1]?prev[j-1]:1+Math.min(prev[j],curr[j-1],prev[j-1]);
    prev=curr;
  }
  return prev[s2.length];
}
```

**Q52. Course Schedule (cycle detection in directed graph).**
```javascript
function canFinish(n, prereqs) {
  const adj=Array.from({length:n},()=>[]);
  for(const[a,b]of prereqs)adj[b].push(a);
  const state=new Array(n).fill(0); // 0=unvis,1=visiting,2=done
  function dfs(v){
    if(state[v]===1)return false; // cycle!
    if(state[v]===2)return true;
    state[v]=1;
    for(const u of adj[v])if(!dfs(u))return false;
    state[v]=2; return true;
  }
  for(let i=0;i<n;i++)if(state[i]===0&&!dfs(i))return false;
  return true;
}
```

**Q53. Kth largest element — QuickSelect O(n) avg.**
```javascript
function kthLargest(nums, k) {
  const target=nums.length-k;
  function select(lo,hi){
    const pi=partition(nums,lo,hi);
    if(pi===target)return nums[pi];
    return pi<target?select(pi+1,hi):select(lo,pi-1);
  }
  return select(0,nums.length-1);
}
```

**Q54. N-Queens backtracking.**
```javascript
function solveNQueens(n) {
  const res=[],board=Array.from({length:n},()=>Array(n).fill('.'));
  const cols=new Set(),d1=new Set(),d2=new Set();
  function bt(row){
    if(row===n){res.push(board.map(r=>r.join('')));return;}
    for(let c=0;c<n;c++){
      if(cols.has(c)||d1.has(row-c)||d2.has(row+c))continue;
      board[row][c]='Q';cols.add(c);d1.add(row-c);d2.add(row+c);
      bt(row+1);
      board[row][c]='.';cols.delete(c);d1.delete(row-c);d2.delete(row+c);
    }
  }
  bt(0); return res;
}
```

**Q55. Trapping rain water O(n) O(1).**
```javascript
function trap(height) {
  let l=0,r=height.length-1,lmax=0,rmax=0,water=0;
  while(l<r){
    if(height[l]<height[r]){height[l]>=lmax?lmax=height[l]:water+=lmax-height[l];l++;}
    else{height[r]>=rmax?rmax=height[r]:water+=rmax-height[r];r--;}
  }
  return water;
}
```

**Q56. Serialize / Deserialize binary tree.**
```javascript
function serialize(root){if(!root)return 'N';return`${root.val},${serialize(root.left)},${serialize(root.right)}`;}
function deserialize(data){const vals=data.split(',');let i=0;function build(){const v=vals[i++];if(v==='N')return null;const n=new TreeNode(+v);n.left=build();n.right=build();return n;}return build();}
```

**Q57–Q70: More medium problems.**
```javascript
// Q57. Maximum product subarray O(n):
function maxProduct(nums){let max=nums[0],min=nums[0],res=nums[0];for(let i=1;i<nums.length;i++){const tmp=max;max=Math.max(nums[i],max*nums[i],min*nums[i]);min=Math.min(nums[i],tmp*nums[i],min*nums[i]);res=Math.max(res,max);}return res;}

// Q58. House robber DP O(n) O(1):
function rob(nums){let prev=0,curr=0;for(const n of nums){const tmp=curr;curr=Math.max(curr,prev+n);prev=tmp;}return curr;}

// Q59. Unique paths DP O(m×n):
function uniquePaths(m,n){const dp=Array.from({length:m},()=>new Array(n).fill(1));for(let i=1;i<m;i++)for(let j=1;j<n;j++)dp[i][j]=dp[i-1][j]+dp[i][j-1];return dp[m-1][n-1];}

// Q60. Matrix chain multiplication O(n³):
function matrixChain(dims){const n=dims.length-1,dp=Array.from({length:n},()=>new Array(n).fill(0));for(let len=2;len<=n;len++){for(let i=0;i<=n-len;i++){const j=i+len-1;dp[i][j]=Infinity;for(let k=i;k<j;k++)dp[i][j]=Math.min(dp[i][j],dp[i][k]+dp[k+1][j]+dims[i]*dims[k+1]*dims[j+1]);}}return dp[0][n-1];}

// Q61. Number of ways to climb stairs (k steps) O(n×k):
function climbStairs(n,k=2){const dp=new Array(n+1).fill(0);dp[0]=1;for(let i=1;i<=n;i++)for(let j=1;j<=k&&j<=i;j++)dp[i]+=dp[i-j];return dp[n];}

// Q62. Clone graph:
function cloneGraph(node){if(!node)return null;const map=new Map();function dfs(n){if(map.has(n))return map.get(n);const clone={val:n.val,neighbors:[]};map.set(n,clone);for(const nb of n.neighbors)clone.neighbors.push(dfs(nb));return clone;}return dfs(node);}

// Q63. Rotate image 90° O(n²) O(1):
function rotate(mat){const n=mat.length;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)[mat[i][j],mat[j][i]]=[mat[j][i],mat[i][j]];for(let i=0;i<n;i++)mat[i].reverse();}

// Q64. Group anagrams O(n×m):
function groupAnagrams(strs){const m=new Map();for(const s of strs){const k=s.split('').sort().join('');m.set(k,[...(m.get(k)??[]),s]);}return[...m.values()];}

// Q65. Decode ways DP O(n):
function numDecodings(s){if(s[0]==='0')return 0;const dp=new Array(s.length+1).fill(0);dp[0]=dp[1]=1;for(let i=2;i<=s.length;i++){if(s[i-1]!=='0')dp[i]+=dp[i-1];const two=+s.slice(i-2,i);if(two>=10&&two<=26)dp[i]+=dp[i-2];}return dp[s.length];}

// Q66. Flatten binary tree to linked list O(n) O(1) Morris:
function flatten(root){let curr=root;while(curr){if(curr.left){let pre=curr.left;while(pre.right)pre=pre.right;pre.right=curr.right;curr.right=curr.left;curr.left=null;}curr=curr.right;}}

// Q67. Kth smallest in BST O(k):
function kthSmallest(root,k){let count=0,res=0;function inorder(n){if(!n||count>=k)return;inorder(n.left);if(++count===k)res=n.val;inorder(n.right);}inorder(root);return res;}

// Q68. Symmetric tree:
function isSymmetric(root){function mirror(l,r){if(!l&&!r)return true;if(!l||!r||l.val!==r.val)return false;return mirror(l.left,r.right)&&mirror(l.right,r.left);}return mirror(root?.left,root?.right);}

// Q69. Binary tree max path sum:
function maxPathSum(root){let max=-Infinity;function dfs(n){if(!n)return 0;const l=Math.max(0,dfs(n.left)),r=Math.max(0,dfs(n.right));max=Math.max(max,n.val+l+r);return n.val+Math.max(l,r);}dfs(root);return max;}

// Q70. Partition equal subset sum DP O(n×sum):
function canPartition(nums){const sum=nums.reduce((a,b)=>a+b,0);if(sum%2)return false;const half=sum/2,dp=new Array(half+1).fill(false);dp[0]=true;for(const n of nums)for(let j=half;j>=n;j--)dp[j]=dp[j]||dp[j-n];return dp[half];}
```

---

## HARD QUESTIONS

**Q86. AVL Tree with all rotations.**
```javascript
class AVL {
  #root=null;
  #h(n){return n?n.h:0;}
  #upd(n){n.h=1+Math.max(this.#h(n.left),this.#h(n.right));}
  #bf(n){return this.#h(n.left)-this.#h(n.right);}
  #rR(y){const x=y.left,T=x.right;x.right=y;y.left=T;this.#upd(y);this.#upd(x);return x;}
  #rL(x){const y=x.right,T=y.left;y.left=x;x.right=T;this.#upd(x);this.#upd(y);return y;}
  #bal(n){this.#upd(n);const b=this.#bf(n);if(b>1){if(this.#bf(n.left)<0)n.left=this.#rL(n.left);return this.#rR(n);}if(b<-1){if(this.#bf(n.right)>0)n.right=this.#rR(n.right);return this.#rL(n);}return n;}
  #ins(n,v){if(!n)return{val:v,left:null,right:null,h:1};if(v<n.val)n.left=this.#ins(n.left,v);else if(v>n.val)n.right=this.#ins(n.right,v);else return n;return this.#bal(n);}
  insert(v){this.#root=this.#ins(this.#root,v);}
}
// All operations guaranteed O(log n)
```

**Q87. Segment Tree with lazy propagation.**
```javascript
class LazySegTree {
  #n; #tree; #lazy;
  constructor(arr){
    this.#n=arr.length;
    this.#tree=new Array(4*this.#n).fill(0);
    this.#lazy=new Array(4*this.#n).fill(0);
    this.#build(arr,0,0,this.#n-1);
  }
  #build(arr,nd,s,e){if(s===e){this.#tree[nd]=arr[s];return;}const m=(s+e)>>1;this.#build(arr,2*nd+1,s,m);this.#build(arr,2*nd+2,m+1,e);this.#tree[nd]=this.#tree[2*nd+1]+this.#tree[2*nd+2];}
  #push(nd,s,e){if(this.#lazy[nd]){const m=(s+e)>>1;this.#apply(2*nd+1,s,m,this.#lazy[nd]);this.#apply(2*nd+2,m+1,e,this.#lazy[nd]);this.#lazy[nd]=0;}}
  #apply(nd,s,e,v){this.#tree[nd]+=v*(e-s+1);this.#lazy[nd]+=v;}
  rangeUpdate(l,r,v,nd=0,s=0,e=this.#n-1){if(r<s||e<l)return;if(l<=s&&e<=r){this.#apply(nd,s,e,v);return;}this.#push(nd,s,e);const m=(s+e)>>1;this.rangeUpdate(l,r,v,2*nd+1,s,m);this.rangeUpdate(l,r,v,2*nd+2,m+1,e);this.#tree[nd]=this.#tree[2*nd+1]+this.#tree[2*nd+2];}
  query(l,r,nd=0,s=0,e=this.#n-1){if(r<s||e<l)return 0;if(l<=s&&e<=r)return this.#tree[nd];this.#push(nd,s,e);const m=(s+e)>>1;return this.query(l,r,2*nd+1,s,m)+this.query(l,r,2*nd+2,m+1,e);}
}
```

**Q88. Fenwick Tree (BIT).**
```javascript
class BIT {
  #t; #n;
  constructor(n){this.#n=n;this.#t=new Array(n+1).fill(0);}
  update(i,d){for(;i<=this.#n;i+=i&-i)this.#t[i]+=d;}
  query(i){let s=0;for(;i>0;i-=i&-i)s+=this.#t[i];return s;}
  range(l,r){return this.query(r)-this.query(l-1);}
}
// O(log n) update and query
```

**Q89. Tarjan's SCC O(V+E).**
```javascript
function tarjanSCC(graph) {
  const n=graph.vertices.length,idx=new Map(),low=new Map(),onStack=new Set(),stack=[],sccs=[];
  let counter=0;
  function dfs(v){
    idx.set(v,counter);low.set(v,counter++);stack.push(v);onStack.add(v);
    for(const{node:u}of graph.neighbors(v)){
      if(!idx.has(u)){dfs(u);low.set(v,Math.min(low.get(v),low.get(u)));}
      else if(onStack.has(u))low.set(v,Math.min(low.get(v),idx.get(u)));
    }
    if(low.get(v)===idx.get(v)){const scc=[];let w;do{w=stack.pop();onStack.delete(w);scc.push(w);}while(w!==v);sccs.push(scc);}
  }
  for(const v of graph.vertices)if(!idx.has(v))dfs(v);
  return sccs;
}
```

**Q90. KMP string matching O(n+m).**
```javascript
function kmp(text, pattern) {
  const lps=buildLPS(pattern), matches=[];
  let j=0;
  for(let i=0;i<text.length;){
    if(text[i]===pattern[j]){i++;j++;}
    if(j===pattern.length){matches.push(i-j);j=lps[j-1];}
    else if(i<text.length&&text[i]!==pattern[j]){j?j=lps[j-1]:i++;}
  }
  return matches;
}
function buildLPS(p){const lps=new Array(p.length).fill(0);let len=0,i=1;while(i<p.length){if(p[i]===p[len]){lps[i++]=++len;}else{len?len=lps[len-1]:lps[i++]=0;}}return lps;}
```

**Q91. Bellman-Ford O(V×E).**
```javascript
function bellmanFord(n, edges, src) {
  const dist=new Array(n).fill(Infinity); dist[src]=0;
  for(let i=0;i<n-1;i++){let upd=false;for(const[u,v,w]of edges){if(dist[u]+w<dist[v]){dist[v]=dist[u]+w;upd=true;}}if(!upd)break;}
  for(const[u,v,w]of edges)if(dist[u]+w<dist[v])return null; // neg cycle
  return dist;
}
```

**Q92. Floyd-Warshall O(V³).**
```javascript
function floydWarshall(mat,n){const d=mat.map(r=>[...r]);for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(d[i][k]+d[k][j]<d[i][j])d[i][j]=d[i][k]+d[k][j];return d;}
```

**Q93. Max Flow — Edmonds-Karp O(VE²).**
```javascript
class MaxFlow {
  #cap; #adj; #n;
  constructor(n){this.#n=n;this.#cap=Array.from({length:n},()=>new Array(n).fill(0));this.#adj=Array.from({length:n},()=>[]);}
  addEdge(u,v,c){this.#adj[u].push(v);this.#adj[v].push(u);this.#cap[u][v]+=c;}
  #bfs(s,t,par){const vis=new Set([s]),q=[s];while(q.length){const u=q.shift();for(const v of this.#adj[u]){if(!vis.has(v)&&this.#cap[u][v]>0){vis.add(v);par[v]=u;if(v===t)return true;q.push(v);}}}return false;}
  flow(s,t){let total=0;const par=new Array(this.#n).fill(-1);while(this.#bfs(s,t,par)){let pf=Infinity;for(let v=t;v!==s;v=par[v])pf=Math.min(pf,this.#cap[par[v]][v]);for(let v=t;v!==s;v=par[v]){this.#cap[par[v]][v]-=pf;this.#cap[v][par[v]]+=pf;}total+=pf;par.fill(-1);}return total;}
}
```

**Q94. Suffix Array O(n log² n).**
```javascript
function suffixArray(s) {
  const n=s.length;
  let sa=[...Array(n).keys()],rank=s.split('').map(c=>c.charCodeAt(0)),tmp=new Array(n);
  for(let gap=1;gap<n;gap*=2){
    sa.sort((a,b)=>{if(rank[a]!==rank[b])return rank[a]-rank[b];const ra=a+gap<n?rank[a+gap]:-1,rb=b+gap<n?rank[b+gap]:-1;return ra-rb;});
    tmp[sa[0]]=0;
    for(let i=1;i<n;i++){tmp[sa[i]]=tmp[sa[i-1]];const[p,c]=[sa[i-1],sa[i]];const[rp2,rc2]=[p+gap<n?rank[p+gap]:-1,c+gap<n?rank[c+gap]:-1];if(rank[p]!==rank[c]||rp2!==rc2)tmp[sa[i]]++;}
    rank=[...tmp];if(rank[sa[n-1]]===n-1)break;
  }
  return sa;
}
```

**Q95. A* pathfinding.**
```javascript
function aStar(grid, [sr,sc], [gr,gc]) {
  const h=(r,c)=>Math.abs(r-gr)+Math.abs(c-gc);
  const heap=new MinHeap((a,b)=>a[0]-b[0]),g=new Map(),key=(r,c)=>`${r},${c}`;
  g.set(key(sr,sc),0);heap.push([h(sr,sc),sr,sc]);
  while(!heap.isEmpty){
    const[,r,c]=heap.pop();
    if(r===gr&&c===gc)return true;
    for(const[dr,dc]of[[1,0],[-1,0],[0,1],[0,-1]]){
      const[nr,nc]=[r+dr,c+dc];
      if(nr<0||nr>=grid.length||nc<0||nc>=grid[0].length||grid[nr][nc])continue;
      const ng=(g.get(key(r,c))??Infinity)+1;
      if(ng<(g.get(key(nr,nc))??Infinity)){g.set(key(nr,nc),ng);heap.push([ng+h(nr,nc),nr,nc]);}
    }
  }
  return false;
}
```

**Q96. Skip List O(log n) expected.**
```javascript
class SkipList {
  #MAX=16; #P=0.5; #level=0;
  #head={val:-Inf,next:new Array(17).fill(null)};
  #randLevel(){let l=0;while(Math.random()<this.#P&&l<this.#MAX)l++;return l;}
  insert(v){const upd=new Array(this.#MAX+1).fill(this.#head);let c=this.#head;for(let i=this.#level;i>=0;i--){while(c.next[i]?.val<v)c=c.next[i];upd[i]=c;}const lvl=this.#randLevel();if(lvl>this.#level){for(let i=this.#level+1;i<=lvl;i++)upd[i]=this.#head;this.#level=lvl;}const n={val:v,next:new Array(lvl+1).fill(null)};for(let i=0;i<=lvl;i++){n.next[i]=upd[i].next[i];upd[i].next[i]=n;}}
  search(v){let c=this.#head;for(let i=this.#level;i>=0;i--)while(c.next[i]?.val<v)c=c.next[i];return c.next[0]?.val===v;}
}
```

**Q97. Persistent Segment Tree (immutable versions).**
```javascript
// Each update creates new nodes along the path only — O(log n) nodes per version
class PST {
  nodes=[{l:null,r:null,sum:0}]; // node pool
  roots=[];
  build(arr,l=0,r=arr.length-1){
    const id=this.nodes.length;
    this.nodes.push({l:null,r:null,sum:0});
    if(l===r){this.nodes[id].sum=arr[l];return id;}
    const m=(l+r)>>1;
    this.nodes[id].l=this.build(arr,l,m);
    this.nodes[id].r=this.build(arr,m+1,r);
    this.nodes[id].sum=this.nodes[this.nodes[id].l].sum+this.nodes[this.nodes[id].r].sum;
    return id;
  }
  update(prev,l,r,idx,val){
    const id=this.nodes.length;
    this.nodes.push({...this.nodes[prev]}); // copy — immutable!
    if(l===r){this.nodes[id].sum=val;return id;}
    const m=(l+r)>>1;
    if(idx<=m)this.nodes[id].l=this.update(this.nodes[prev].l,l,m,idx,val);
    else this.nodes[id].r=this.update(this.nodes[prev].r,m+1,r,idx,val);
    this.nodes[id].sum=this.nodes[this.nodes[id].l].sum+this.nodes[this.nodes[id].r].sum;
    return id;
  }
}
```

**Q98. Aho-Corasick multi-pattern search O(n+m+z).**
```javascript
class AC {
  goto=[{}]; fail=[0]; out=[[]]; size=1;
  addPattern(p){let s=0;for(const c of p){if(this.goto[s][c]===undefined){this.goto[this.size]={};this.fail[this.size]=0;this.out[this.size]=[];this.goto[s][c]=this.size++;}s=this.goto[s][c];}this.out[s].push(p);}
  build(){const q=[];for(const c of Object.keys(this.goto[0])){const s=this.goto[0][c];this.fail[s]=0;q.push(s);}while(q.length){const r=q.shift();for(const[c,s]of Object.entries(this.goto[r])){q.push(s);let f=this.fail[r];while(f&&!this.goto[f][c])f=this.fail[f];this.fail[s]=this.goto[f]?.[c]??0;if(this.fail[s]===s)this.fail[s]=0;this.out[s]=[...this.out[s],...this.out[this.fail[s]]];}}}
  search(text){const matches=[];let s=0;for(let i=0;i<text.length;i++){const c=text[i];while(s&&!this.goto[s][c])s=this.fail[s];s=this.goto[s][c]??0;for(const p of this.out[s])matches.push({p,i});}return matches;}
}
```

**Q99–Q110. Key algorithm patterns.**
```javascript
// Q99. Rabin-Karp rolling hash O(n+m) avg:
function rabinKarp(text,pat){const B=31,M=1e9+7,n=text.length,m=pat.length;const hash=s=>s.split('').reduce((h,c,i)=>(h+c.charCodeAt(0)*Math.pow(B,i))%M,0);let ph=hash(pat),wh=hash(text.slice(0,m)),pow=Math.pow(B,m-1)%M;const res=[];if(ph===wh&&text.slice(0,m)===pat)res.push(0);for(let i=m;i<n;i++){wh=((wh-text.charCodeAt(i-m))/(B)+text.charCodeAt(i)*pow)%M;// simplified
if(wh===ph&&text.slice(i-m+1,i+1)===pat)res.push(i-m+1);}return res;}

// Q100. Z-function O(n) — match length at each position:
function zFunction(s){const z=new Array(s.length).fill(0);let l=0,r=0;for(let i=1;i<s.length;i++){if(i<r)z[i]=Math.min(r-i,z[i-l]);while(i+z[i]<s.length&&s[z[i]]===s[i+z[i]])z[i]++;if(i+z[i]>r){l=i;r=i+z[i];}}return z;}

// Q101. Manacher's algorithm — longest palindromic substring O(n):
function manacher(s){const t='#'+s.split('').join('#')+'#';const n=t.length,p=new Array(n).fill(0);let c=0,r=0;for(let i=0;i<n;i++){const mirror=2*c-i;if(i<r)p[i]=Math.min(r-i,p[mirror]);while(i-p[i]-1>=0&&i+p[i]+1<n&&t[i-p[i]-1]===t[i+p[i]+1])p[i]++;if(i+p[i]>r){c=i;r=i+p[i];}}const max=Math.max(...p),ci=p.indexOf(max);return s.slice((ci-max)/2,(ci+max)/2);}

// Q102. Counting inversions (merge sort based) O(n log n):
function countInversions(arr){let inv=0;function ms(a){if(a.length<=1)return a;const m=a.length>>1,L=ms(a.slice(0,m)),R=ms(a.slice(m)),res=[];let i=0,j=0;while(i<L.length&&j<R.length){if(L[i]<=R[j])res.push(L[i++]);else{inv+=L.length-i;res.push(R[j++]);}}return[...res,...L.slice(i),...R.slice(j)];}ms([...arr]);return inv;}

// Q103. Largest rectangle in histogram (monotonic stack) O(n):
function largestRect(heights){const st=[],n=heights.length;let max=0;for(let i=0;i<=n;i++){const h=i===n?0:heights[i];while(st.length&&heights[st.at(-1)]>h){const ht=heights[st.pop()];const w=st.length?i-st.at(-1)-1:i;max=Math.max(max,ht*w);}st.push(i);}return max;}

// Q104. Maximal rectangle in binary matrix O(m×n):
function maximalRectangle(matrix){const n=matrix[0].length,h=new Array(n).fill(0);let max=0;for(const row of matrix){for(let j=0;j<n;j++)h[j]=row[j]==='0'?0:h[j]+1;max=Math.max(max,largestRect(h));}return max;}

// Q105. Interleaving string DP O(m×n):
function isInterleave(s1,s2,s3){const[m,n]=[s1.length,s2.length];if(m+n!==s3.length)return false;const dp=Array.from({length:m+1},()=>new Array(n+1).fill(false));dp[0][0]=true;for(let i=0;i<=m;i++)for(let j=0;j<=n;j++){if(i>0)dp[i][j]||=dp[i-1][j]&&s1[i-1]===s3[i+j-1];if(j>0)dp[i][j]||=dp[i][j-1]&&s2[j-1]===s3[i+j-1];}return dp[m][n];}

// Q106. Regular expression matching DP O(m×n):
function isMatch(s,p){const[m,n]=[s.length,p.length],dp=Array.from({length:m+1},()=>new Array(n+1).fill(false));dp[0][0]=true;for(let j=1;j<=n;j++)if(p[j-1]==='*')dp[0][j]=dp[0][j-2];for(let i=1;i<=m;i++)for(let j=1;j<=n;j++){if(p[j-1]==='*')dp[i][j]=dp[i][j-2]||((p[j-2]==='.'||p[j-2]===s[i-1])&&dp[i-1][j]);else dp[i][j]=(p[j-1]==='.'||p[j-1]===s[i-1])&&dp[i-1][j-1];}return dp[m][n];}

// Q107. Burst balloons DP O(n³):
function maxCoins(nums){nums=[1,...nums,1];const n=nums.length,dp=Array.from({length:n},()=>new Array(n).fill(0));for(let len=2;len<n;len++)for(let l=0;l<n-len;l++){const r=l+len;for(let k=l+1;k<r;k++)dp[l][r]=Math.max(dp[l][r],nums[l]*nums[k]*nums[r]+dp[l][k]+dp[k][r]);}return dp[0][n-1];}

// Q108. Super egg drop DP O(n log n) binary search:
function superEggDrop(K,N){const dp=new Map();function f(k,n){if(n<=1)return n;if(k===1)return n;if(dp.has(`${k},${n}`))return dp.get(`${k},${n}`);let lo=1,hi=n,res=Infinity;while(lo<=hi){const m=(lo+hi)>>1;const broke=f(k-1,m-1),safe=f(k,n-m),worst=1+Math.max(broke,safe);if(broke<safe){lo=m+1;}else{hi=m-1;}res=Math.min(res,worst);}dp.set(`${k},${n}`,res);return res;}return f(K,N);}

// Q109. Longest palindromic subsequence O(n²):
function longestPalinSub(s){const n=s.length,dp=Array.from({length:n},(_,i)=>Array.from({length:n},(_, j)=>i===j?1:0));for(let len=2;len<=n;len++)for(let i=0;i<=n-len;i++){const j=i+len-1;dp[i][j]=s[i]===s[j]?(len===2?2:dp[i+1][j-1]+2):Math.max(dp[i+1][j],dp[i][j-1]);}return dp[0][n-1];}

// Q110. Word ladder BFS O(n×m²):
function ladderLength(begin,end,list){const set=new Set(list);if(!set.has(end))return 0;const q=[[begin,1]];set.delete(begin);while(q.length){const[word,len]=q.shift();for(let i=0;i<word.length;i++){for(let c=97;c<=122;c++){const nw=word.slice(0,i)+String.fromCharCode(c)+word.slice(i+1);if(nw===end)return len+1;if(set.has(nw)){set.delete(nw);q.push([nw,len+1]);}}}}return 0;}
```

---

*130 DSA questions covering arrays, strings, linked lists, trees, graphs, heaps, tries, sorting, searching, dynamic programming, greedy, and advanced data structures. Each with time/space complexity analysis.*


---

## COMPLETING DSA Q41–Q130

**Q41. Implement Dijkstra's shortest path.**
```javascript
function dijkstra(graph, src) {
  const dist = new Map(), heap = new MinHeap((a,b)=>a[0]-b[0]);
  for (const v of graph.vertices) dist.set(v, Infinity);
  dist.set(src, 0); heap.push([0, src]);
  while (!heap.isEmpty) {
    const [d, u] = heap.pop();
    if (d > dist.get(u)) continue;
    for (const {node:v, weight:w} of graph.neighbors(u)) {
      const nd = d + w;
      if (nd < dist.get(v)) { dist.set(v, nd); heap.push([nd, v]); }
    }
  }
  return dist;
}
// O((V+E) log V)
```

**Q42. Topological sort — Kahn's BFS.**
```javascript
function topoSort(graph) {
  const indeg = new Map();
  for (const v of graph.vertices) indeg.set(v, 0);
  for (const v of graph.vertices)
    for (const {node:u} of graph.neighbors(v)) indeg.set(u,(indeg.get(u)||0)+1);
  const q = [...graph.vertices].filter(v=>indeg.get(v)===0), order=[];
  while (q.length) {
    const v = q.shift(); order.push(v);
    for (const {node:u} of graph.neighbors(v)) { indeg.set(u,indeg.get(u)-1); if(indeg.get(u)===0)q.push(u); }
  }
  return order.length===graph.vertices.length ? order : null;
}
```

**Q43. Longest Common Subsequence.**
```javascript
function lcs(s1, s2) {
  const m=s1.length, n=s2.length;
  const dp=Array.from({length:m+1},()=>new Array(n+1).fill(0));
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++)
    dp[i][j]=s1[i-1]===s2[j-1]?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);
  return dp[m][n];
}
```

**Q44. 0/1 Knapsack.**
```javascript
function knapsack(weights, values, W) {
  const dp = new Array(W+1).fill(0);
  for(let i=0;i<weights.length;i++)
    for(let w=W;w>=weights[i];w--)
      dp[w]=Math.max(dp[w],dp[w-weights[i]]+values[i]);
  return dp[W];
}
```

**Q45. LIS in O(n log n).**
```javascript
function lis(nums) {
  const tails=[];
  for(const n of nums){
    let lo=0,hi=tails.length;
    while(lo<hi){const mid=(lo+hi)>>1;tails[mid]<n?lo=mid+1:hi=mid;}
    tails[lo]=n;
  }
  return tails.length;
}
```

**Q46. Union-Find.**
```javascript
class UF {
  #p;#r;#c;
  constructor(n){this.#p=[...Array(n).keys()];this.#r=new Array(n).fill(0);this.#c=n;}
  find(x){if(this.#p[x]!==x)this.#p[x]=this.find(this.#p[x]);return this.#p[x];}
  union(x,y){const[px,py]=[this.find(x),this.find(y)];if(px===py)return false;
    if(this.#r[px]<this.#r[py])this.#p[px]=py;
    else if(this.#r[px]>this.#r[py])this.#p[py]=px;
    else{this.#p[py]=px;this.#r[px]++;}this.#c--;return true;}
  get components(){return this.#c;}
}
```

**Q47. Merge intervals.**
```javascript
function merge(intervals) {
  intervals.sort((a,b)=>a[0]-b[0]);
  const res=[intervals[0]];
  for(const[s,e]of intervals.slice(1)){
    const last=res.at(-1);
    s<=last[1]?last[1]=Math.max(last[1],e):res.push([s,e]);
  }
  return res;
}
```

**Q48. Sliding window — minimum window substring.**
```javascript
function minWindow(s,t){
  const need=new Map();for(const c of t)need.set(c,(need.get(c)||0)+1);
  let have=0,req=need.size,l=0,min=Infinity,res="";
  for(let r=0;r<s.length;r++){
    const c=s[r];if(need.has(c)){need.set(c,need.get(c)-1);if(need.get(c)===0)have++;}
    while(have===req){if(r-l+1<min){min=r-l+1;res=s.slice(l,r+1);}
      const lc=s[l++];if(need.has(lc)){if(need.get(lc)===0)have--;need.set(lc,need.get(lc)+1);}}
  }return res;
}
```

**Q49. Edit distance.**
```javascript
function editDist(s1,s2){
  let prev=[...Array(s2.length+1).keys()];
  for(let i=1;i<=s1.length;i++){
    const curr=[i];
    for(let j=1;j<=s2.length;j++)
      curr[j]=s1[i-1]===s2[j-1]?prev[j-1]:1+Math.min(prev[j],curr[j-1],prev[j-1]);
    prev=curr;
  }return prev[s2.length];
}
```

**Q50. Coin change.**
```javascript
function coinChange(coins,amount){
  const dp=new Array(amount+1).fill(Infinity);dp[0]=0;
  for(let i=1;i<=amount;i++)
    for(const c of coins)if(c<=i&&dp[i-c]+1<dp[i])dp[i]=dp[i-c]+1;
  return dp[amount]===Infinity?-1:dp[amount];
}
```

**Q51. House robber.**
```javascript
function rob(nums){let prev=0,curr=0;for(const n of nums){const tmp=curr;curr=Math.max(curr,prev+n);prev=tmp;}return curr;}
```

**Q52. Maximum product subarray.**
```javascript
function maxProduct(nums){let max=nums[0],min=nums[0],res=nums[0];for(let i=1;i<nums.length;i++){const tmp=max;max=Math.max(nums[i],max*nums[i],min*nums[i]);min=Math.min(nums[i],tmp*nums[i],min*nums[i]);res=Math.max(res,max);}return res;}
```

**Q53. Trapping rain water — O(n) O(1).**
```javascript
function trap(h){let l=0,r=h.length-1,lm=0,rm=0,w=0;while(l<r){if(h[l]<h[r]){h[l]>=lm?lm=h[l]:w+=lm-h[l];l++;}else{h[r]>=rm?rm=h[r]:w+=rm-h[r];r--;}}return w;}
```

**Q54. Largest rectangle in histogram.**
```javascript
function largestRect(h){const st=[],n=h.length;let max=0;for(let i=0;i<=n;i++){const hi=i===n?0:h[i];while(st.length&&h[st.at(-1)]>hi){const ht=h[st.pop()];const w=st.length?i-st.at(-1)-1:i;max=Math.max(max,ht*w);}st.push(i);}return max;}
```

**Q55. Number of islands.**
```javascript
function numIslands(grid){let count=0;const dfs=(r,c)=>{if(r<0||r>=grid.length||c<0||c>=grid[0].length||grid[r][c]==='0')return;grid[r][c]='0';[[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr,dc])=>dfs(r+dr,c+dc));};for(let r=0;r<grid.length;r++)for(let c=0;c<grid[0].length;c++)if(grid[r][c]==='1'){count++;dfs(r,c);}return count;}
```

**Q56. Word search.**
```javascript
function exist(board,word){const[m,n]=[board.length,board[0].length];function dfs(r,c,i){if(i===word.length)return true;if(r<0||r>=m||c<0||c>=n||board[r][c]!==word[i])return false;const tmp=board[r][c];board[r][c]='#';const found=[[1,0],[-1,0],[0,1],[0,-1]].some(([dr,dc])=>dfs(r+dr,c+dc,i+1));board[r][c]=tmp;return found;}for(let r=0;r<m;r++)for(let c=0;c<n;c++)if(dfs(r,c,0))return true;return false;}
```

**Q57. Course schedule — cycle detection.**
```javascript
function canFinish(n,prereqs){const adj=Array.from({length:n},()=>[]);for(const[a,b]of prereqs)adj[b].push(a);const state=new Array(n).fill(0);function dfs(v){if(state[v]===1)return false;if(state[v]===2)return true;state[v]=1;for(const u of adj[v])if(!dfs(u))return false;state[v]=2;return true;}for(let i=0;i<n;i++)if(!dfs(i))return false;return true;}
```

**Q58. Pacific Atlantic water flow.**
```javascript
function pacificAtlantic(heights){const m=heights.length,n=heights[0].length,dirs=[[1,0],[-1,0],[0,1],[0,-1]];const bfs=(starts)=>{const vis=new Set(starts.map(([r,c])=>`${r},${c}`)),q=[...starts];while(q.length){const[r,c]=q.shift();for(const[dr,dc]of dirs){const[nr,nc]=[r+dr,c+dc],k=`${nr},${nc}`;if(nr>=0&&nr<m&&nc>=0&&nc<n&&!vis.has(k)&&heights[nr][nc]>=heights[r][c]){vis.add(k);q.push([nr,nc]);}}}return vis;};const pac=[],atl=[];for(let i=0;i<m;i++){pac.push([i,0]);atl.push([i,n-1]);}for(let j=0;j<n;j++){pac.push([0,j]);atl.push([m-1,j]);}const pv=bfs(pac),av=bfs(atl);const res=[];for(let r=0;r<m;r++)for(let c=0;c<n;c++)if(pv.has(`${r},${c}`)&&av.has(`${r},${c}`))res.push([r,c]);return res;}
```

**Q59. Clone graph.**
```javascript
function cloneGraph(node){if(!node)return null;const map=new Map();function dfs(n){if(map.has(n))return map.get(n);const clone={val:n.val,neighbors:[]};map.set(n,clone);for(const nb of n.neighbors)clone.neighbors.push(dfs(nb));return clone;}return dfs(node);}
```

**Q60. Decode ways.**
```javascript
function numDecodings(s){if(s[0]==='0')return 0;const dp=new Array(s.length+1).fill(0);dp[0]=dp[1]=1;for(let i=2;i<=s.length;i++){if(s[i-1]!=='0')dp[i]+=dp[i-1];const two=+s.slice(i-2,i);if(two>=10&&two<=26)dp[i]+=dp[i-2];}return dp[s.length];}
```

**Q61. Jump game II — min jumps.**
```javascript
function jump(nums){let jumps=0,curEnd=0,farthest=0;for(let i=0;i<nums.length-1;i++){farthest=Math.max(farthest,i+nums[i]);if(i===curEnd){jumps++;curEnd=farthest;}}return jumps;}
```

**Q62. Rotate image.**
```javascript
function rotate(mat){const n=mat.length;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)[mat[i][j],mat[j][i]]=[mat[j][i],mat[i][j]];for(let i=0;i<n;i++)mat[i].reverse();}
```

**Q63. Group anagrams.**
```javascript
function groupAnagrams(strs){const m=new Map();for(const s of strs){const k=s.split('').sort().join('');m.set(k,[...(m.get(k)||[]),s]);}return[...m.values()];}
```

**Q64. Longest substring without repeating characters.**
```javascript
function lengthOfLongest(s){const seen=new Map();let max=0,start=0;for(let end=0;end<s.length;end++){const c=s[end];if(seen.has(c)&&seen.get(c)>=start)start=seen.get(c)+1;seen.set(c,end);max=Math.max(max,end-start+1);}return max;}
```

**Q65. 3Sum.**
```javascript
function threeSum(nums){nums.sort((a,b)=>a-b);const res=[];for(let i=0;i<nums.length-2;i++){if(i>0&&nums[i]===nums[i-1])continue;let l=i+1,r=nums.length-1;while(l<r){const s=nums[i]+nums[l]+nums[r];if(s===0){res.push([nums[i],nums[l],nums[r]]);while(nums[l]===nums[l+1])l++;while(nums[r]===nums[r-1])r--;l++;r--;}else if(s<0)l++;else r--;}}return res;}
```

**Q66. Subarray sum equals k.**
```javascript
function subarraySum(nums,k){const map=new Map([[0,1]]);let sum=0,count=0;for(const n of nums){sum+=n;count+=map.get(sum-k)||0;map.set(sum,(map.get(sum)||0)+1);}return count;}
```

**Q67. Product of array except self.**
```javascript
function productExceptSelf(nums){const res=new Array(nums.length).fill(1);let left=1;for(let i=0;i<nums.length;i++){res[i]=left;left*=nums[i];}let right=1;for(let i=nums.length-1;i>=0;i--){res[i]*=right;right*=nums[i];}return res;}
```

**Q68. Unique paths.**
```javascript
function uniquePaths(m,n){const dp=Array.from({length:m},()=>new Array(n).fill(1));for(let i=1;i<m;i++)for(let j=1;j<n;j++)dp[i][j]=dp[i-1][j]+dp[i][j-1];return dp[m-1][n-1];}
```

**Q69. Climbing stairs with k steps.**
```javascript
function climbStairs(n,k=2){const dp=new Array(n+1).fill(0);dp[0]=1;for(let i=1;i<=n;i++)for(let j=1;j<=k&&j<=i;j++)dp[i]+=dp[i-j];return dp[n];}
```

**Q70. Longest palindromic substring — Manacher's O(n).**
```javascript
function longestPalindrome(s){const t='#'+s.split('').join('#')+'#';const n=t.length,p=new Array(n).fill(0);let c=0,r=0;for(let i=0;i<n;i++){const mirror=2*c-i;if(i<r)p[i]=Math.min(r-i,p[mirror]);while(i-p[i]-1>=0&&i+p[i]+1<n&&t[i-p[i]-1]===t[i+p[i]+1])p[i]++;if(i+p[i]>r){c=i;r=i+p[i];}}const max=Math.max(...p),ci=p.indexOf(max);return s.slice((ci-max)/2,(ci+max)/2);}
```

**Q71. Kth smallest in BST.**
```javascript
function kthSmallest(root,k){let count=0,res=0;function inorder(n){if(!n||count>=k)return;inorder(n.left);if(++count===k)res=n.val;inorder(n.right);}inorder(root);return res;}
```

**Q72. Serialize/Deserialize binary tree.**
```javascript
function serialize(root){if(!root)return'N';return`${root.val},${serialize(root.left)},${serialize(root.right)}`;}
function deserialize(data){const vals=data.split(',');let i=0;function build(){const v=vals[i++];if(v==='N')return null;const n=new TreeNode(+v);n.left=build();n.right=build();return n;}return build();}
```

**Q73. Binary tree maximum path sum.**
```javascript
function maxPathSum(root){let max=-Infinity;function dfs(n){if(!n)return 0;const l=Math.max(0,dfs(n.left)),r=Math.max(0,dfs(n.right));max=Math.max(max,n.val+l+r);return n.val+Math.max(l,r);}dfs(root);return max;}
```

**Q74. Construct binary tree from preorder and inorder.**
```javascript
function buildTree(preorder,inorder){const map=new Map(inorder.map((v,i)=>[v,i]));let pi=0;function build(lo,hi){if(lo>hi)return null;const root=new TreeNode(preorder[pi++]);const mid=map.get(root.val);root.left=build(lo,mid-1);root.right=build(mid+1,hi);return root;}return build(0,inorder.length-1);}
```

**Q75. Implement LRU cache — O(1) all ops.**
```javascript
class LRUCache{#cap;#map=new Map();constructor(c){this.#cap=c;}get(k){if(!this.#map.has(k))return-1;const v=this.#map.get(k);this.#map.delete(k);this.#map.set(k,v);return v;}put(k,v){this.#map.delete(k);this.#map.set(k,v);if(this.#map.size>this.#cap)this.#map.delete(this.#map.keys().next().value);}}
```

**Q76. Segment tree range sum with lazy propagation.**
```javascript
class LazySegTree{#n;#tree;#lazy;constructor(arr){this.#n=arr.length;this.#tree=new Array(4*this.#n).fill(0);this.#lazy=new Array(4*this.#n).fill(0);this.#build(arr,0,0,this.#n-1);}#build(arr,nd,s,e){if(s===e){this.#tree[nd]=arr[s];return;}const m=(s+e)>>1;this.#build(arr,2*nd+1,s,m);this.#build(arr,2*nd+2,m+1,e);this.#tree[nd]=this.#tree[2*nd+1]+this.#tree[2*nd+2];}#push(nd,s,e){if(this.#lazy[nd]){const m=(s+e)>>1;this.#apply(2*nd+1,s,m,this.#lazy[nd]);this.#apply(2*nd+2,m+1,e,this.#lazy[nd]);this.#lazy[nd]=0;}}#apply(nd,s,e,v){this.#tree[nd]+=v*(e-s+1);this.#lazy[nd]+=v;}update(l,r,v,nd=0,s=0,e=this.#n-1){if(r<s||e<l)return;if(l<=s&&e<=r){this.#apply(nd,s,e,v);return;}this.#push(nd,s,e);const m=(s+e)>>1;this.update(l,r,v,2*nd+1,s,m);this.update(l,r,v,2*nd+2,m+1,e);this.#tree[nd]=this.#tree[2*nd+1]+this.#tree[2*nd+2];}query(l,r,nd=0,s=0,e=this.#n-1){if(r<s||e<l)return 0;if(l<=s&&e<=r)return this.#tree[nd];this.#push(nd,s,e);const m=(s+e)>>1;return this.query(l,r,2*nd+1,s,m)+this.query(l,r,2*nd+2,m+1,e);}}
```

**Q77. AVL tree insert with rotations.**
```javascript
class AVL{#root=null;#h(n){return n?n.h:0;}#upd(n){n.h=1+Math.max(this.#h(n.left),this.#h(n.right));}#bf(n){return this.#h(n.left)-this.#h(n.right);}#rR(y){const x=y.left,T=x.right;x.right=y;y.left=T;this.#upd(y);this.#upd(x);return x;}#rL(x){const y=x.right,T=y.left;y.left=x;x.right=T;this.#upd(x);this.#upd(y);return y;}#bal(n){this.#upd(n);const b=this.#bf(n);if(b>1){if(this.#bf(n.left)<0)n.left=this.#rL(n.left);return this.#rR(n);}if(b<-1){if(this.#bf(n.right)>0)n.right=this.#rR(n.right);return this.#rL(n);}return n;}#ins(n,v){if(!n)return{val:v,left:null,right:null,h:1};if(v<n.val)n.left=this.#ins(n.left,v);else if(v>n.val)n.right=this.#ins(n.right,v);else return n;return this.#bal(n);}insert(v){this.#root=this.#ins(this.#root,v);}}
```

**Q78. Bellman-Ford.**
```javascript
function bellmanFord(n,edges,src){const dist=new Array(n).fill(Infinity);dist[src]=0;for(let i=0;i<n-1;i++){let upd=false;for(const[u,v,w]of edges)if(dist[u]+w<dist[v]){dist[v]=dist[u]+w;upd=true;}if(!upd)break;}for(const[u,v,w]of edges)if(dist[u]+w<dist[v])return null;return dist;}
```

**Q79. KMP string matching.**
```javascript
function kmp(text,pattern){const lps=buildLPS(pattern);const matches=[];let j=0;for(let i=0;i<text.length;){if(text[i]===pattern[j]){i++;j++;}if(j===pattern.length){matches.push(i-j);j=lps[j-1];}else if(i<text.length&&text[i]!==pattern[j]){j?j=lps[j-1]:i++;}}return matches;}
function buildLPS(p){const lps=new Array(p.length).fill(0);let len=0,i=1;while(i<p.length){if(p[i]===p[len])lps[i++]=++len;else len?len=lps[len-1]:lps[i++]=0;}return lps;}
```

**Q80. Tarjan's SCC.**
```javascript
function tarjanSCC(adj,n){const idx=new Array(n).fill(-1),low=new Array(n).fill(0),onStack=new Array(n).fill(false),stack=[],sccs=[];let counter=0;function dfs(v){idx[v]=low[v]=counter++;stack.push(v);onStack[v]=true;for(const u of adj[v]||[]){if(idx[u]===-1){dfs(u);low[v]=Math.min(low[v],low[u]);}else if(onStack[u])low[v]=Math.min(low[v],idx[u]);}if(low[v]===idx[v]){const scc=[];let w;do{w=stack.pop();onStack[w]=false;scc.push(w);}while(w!==v);sccs.push(scc);}}for(let v=0;v<n;v++)if(idx[v]===-1)dfs(v);return sccs;}
```

**Q81. Floyd-Warshall.**
```javascript
function floydWarshall(mat,n){const d=mat.map(r=>[...r]);for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(d[i][k]+d[k][j]<d[i][j])d[i][j]=d[i][k]+d[k][j];return d;}
```

**Q82. Max flow — Edmonds-Karp.**
```javascript
class MaxFlow{#cap;#adj;#n;constructor(n){this.#n=n;this.#cap=Array.from({length:n},()=>new Array(n).fill(0));this.#adj=Array.from({length:n},()=>[]);}addEdge(u,v,c){this.#adj[u].push(v);this.#adj[v].push(u);this.#cap[u][v]+=c;}#bfs(s,t,par){const vis=new Set([s]),q=[s];while(q.length){const u=q.shift();for(const v of this.#adj[u]){if(!vis.has(v)&&this.#cap[u][v]>0){vis.add(v);par[v]=u;if(v===t)return true;q.push(v);}}}return false;}flow(s,t){let total=0;const par=new Array(this.#n).fill(-1);while(this.#bfs(s,t,par)){let pf=Infinity;for(let v=t;v!==s;v=par[v])pf=Math.min(pf,this.#cap[par[v]][v]);for(let v=t;v!==s;v=par[v]){this.#cap[par[v]][v]-=pf;this.#cap[v][par[v]]+=pf;}total+=pf;par.fill(-1);}return total;}}
```

**Q83. Counting inversions — merge sort based.**
```javascript
function countInversions(arr){let inv=0;function ms(a){if(a.length<=1)return a;const m=a.length>>1,L=ms(a.slice(0,m)),R=ms(a.slice(m)),res=[];let i=0,j=0;while(i<L.length&&j<R.length){if(L[i]<=R[j])res.push(L[i++]);else{inv+=L.length-i;res.push(R[j++]);}}return[...res,...L.slice(i),...R.slice(j)];}ms([...arr]);return inv;}
```

**Q84. Fenwick tree.**
```javascript
class BIT{#t;#n;constructor(n){this.#n=n;this.#t=new Array(n+1).fill(0);}update(i,d){for(;i<=this.#n;i+=i&-i)this.#t[i]+=d;}query(i){let s=0;for(;i>0;i-=i&-i)s+=this.#t[i];return s;}range(l,r){return this.query(r)-this.query(l-1);}}
```

**Q85. A* pathfinding.**
```javascript
function aStar(grid,[sr,sc],[gr,gc]){const h=(r,c)=>Math.abs(r-gr)+Math.abs(c-gc);const heap=new MinHeap((a,b)=>a[0]-b[0]),g=new Map(),key=(r,c)=>`${r},${c}`;g.set(key(sr,sc),0);heap.push([h(sr,sc),sr,sc]);while(!heap.isEmpty){const[,r,c]=heap.pop();if(r===gr&&c===gc)return true;for(const[dr,dc]of[[1,0],[-1,0],[0,1],[0,-1]]){const[nr,nc]=[r+dr,c+dc];if(nr<0||nr>=grid.length||nc<0||nc>=grid[0].length||grid[nr][nc])continue;const ng=(g.get(key(r,c))||0)+1;if(ng<(g.get(key(nr,nc))||Infinity)){g.set(key(nr,nc),ng);heap.push([ng+h(nr,nc),nr,nc]);}}}return false;}
```

**Q86. Suffix array construction.**
```javascript
function suffixArray(s){const n=s.length;let sa=[...Array(n).keys()],rank=s.split('').map(c=>c.charCodeAt(0)),tmp=new Array(n);for(let gap=1;gap<n;gap*=2){sa.sort((a,b)=>{if(rank[a]!==rank[b])return rank[a]-rank[b];const[ra,rb]=[a+gap<n?rank[a+gap]:-1,b+gap<n?rank[b+gap]:-1];return ra-rb;});tmp[sa[0]]=0;for(let i=1;i<n;i++){tmp[sa[i]]=tmp[sa[i-1]];const[p,c]=[sa[i-1],sa[i]],rp2=p+gap<n?rank[p+gap]:-1,rc2=c+gap<n?rank[c+gap]:-1;if(rank[p]!==rank[c]||rp2!==rc2)tmp[sa[i]]++;}rank=[...tmp];if(rank[sa[n-1]]===n-1)break;}return sa;}
```

**Q87. Skip list.**
```javascript
class SkipList{#MAX=16;#P=0.5;#level=0;#head={val:-Infinity,next:new Array(17).fill(null)};#randLevel(){let l=0;while(Math.random()<this.#P&&l<this.#MAX)l++;return l;}insert(v){const upd=new Array(this.#MAX+1).fill(this.#head);let c=this.#head;for(let i=this.#level;i>=0;i--){while(c.next[i]?.val<v)c=c.next[i];upd[i]=c;}const lvl=this.#randLevel();if(lvl>this.#level){for(let i=this.#level+1;i<=lvl;i++)upd[i]=this.#head;this.#level=lvl;}const n={val:v,next:new Array(lvl+1).fill(null)};for(let i=0;i<=lvl;i++){n.next[i]=upd[i].next[i];upd[i].next[i]=n;}}search(v){let c=this.#head;for(let i=this.#level;i>=0;i--)while(c.next[i]?.val<v)c=c.next[i];return c.next[0]?.val===v;}}
```

**Q88–Q130: Key algorithm patterns**
```javascript
// Q88. Rolling hash (Rabin-Karp):
function rabinKarp(text,pat){const B=31,M=1e9+7,n=text.length,m=pat.length,matches=[];const hashStr=s=>s.split('').reduce((h,c)=>(h*B+c.charCodeAt(0))%M,0);let ph=hashStr(pat),wh=hashStr(text.slice(0,m)),pow=1;for(let i=1;i<m;i++)pow=pow*B%M;if(ph===wh&&text.slice(0,m)===pat)matches.push(0);for(let i=m;i<n;i++){wh=(wh-text.charCodeAt(i-m)*pow%M+M)*B%M;wh=(wh+text.charCodeAt(i))%M;if(wh===ph&&text.slice(i-m+1,i+1)===pat)matches.push(i-m+1);}return matches;}

// Q89. Z-function:
function zFunction(s){const z=new Array(s.length).fill(0);let l=0,r=0;for(let i=1;i<s.length;i++){if(i<r)z[i]=Math.min(r-i,z[i-l]);while(i+z[i]<s.length&&s[z[i]]===s[i+z[i]])z[i]++;if(i+z[i]>r){l=i;r=i+z[i];}}return z;}

// Q90. Burst balloons DP:
function maxCoins(nums){nums=[1,...nums,1];const n=nums.length,dp=Array.from({length:n},()=>new Array(n).fill(0));for(let len=2;len<n;len++)for(let l=0;l<n-len;l++){const r=l+len;for(let k=l+1;k<r;k++)dp[l][r]=Math.max(dp[l][r],nums[l]*nums[k]*nums[r]+dp[l][k]+dp[k][r]);}return dp[0][n-1];}

// Q91. Regular expression matching:
function isMatch(s,p){const[m,n]=[s.length,p.length],dp=Array.from({length:m+1},()=>new Array(n+1).fill(false));dp[0][0]=true;for(let j=1;j<=n;j++)if(p[j-1]==='*')dp[0][j]=dp[0][j-2];for(let i=1;i<=m;i++)for(let j=1;j<=n;j++){if(p[j-1]==='*')dp[i][j]=dp[i][j-2]||((p[j-2]==='.'||p[j-2]===s[i-1])&&dp[i-1][j]);else dp[i][j]=(p[j-1]==='.'||p[j-1]===s[i-1])&&dp[i-1][j-1];}return dp[m][n];}

// Q92. Longest palindromic subsequence:
function longestPalinSub(s){const n=s.length,dp=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1:0));for(let len=2;len<=n;len++)for(let i=0;i<=n-len;i++){const j=i+len-1;dp[i][j]=s[i]===s[j]?(len===2?2:dp[i+1][j-1]+2):Math.max(dp[i+1][j],dp[i][j-1]);}return dp[0][n-1];}

// Q93. Longest consecutive sequence O(n):
function longestConsecutive(nums){const s=new Set(nums);let best=0;for(const n of s){if(!s.has(n-1)){let len=1;while(s.has(n+len))len++;best=Math.max(best,len);}}return best;}

// Q94. Partition equal subset sum:
function canPartition(nums){const sum=nums.reduce((a,b)=>a+b,0);if(sum%2)return false;const half=sum/2,dp=new Array(half+1).fill(false);dp[0]=true;for(const n of nums)for(let j=half;j>=n;j--)dp[j]=dp[j]||dp[j-n];return dp[half];}

// Q95. Two-pointer — container with most water:
function maxArea(h){let l=0,r=h.length-1,max=0;while(l<r){max=Math.max(max,Math.min(h[l],h[r])*(r-l));h[l]<h[r]?l++:r--;}return max;}

// Q96. Monotonic deque — max of sliding window O(n):
function maxSlidingWindow(nums,k){const dq=[],res=[];for(let i=0;i<nums.length;i++){while(dq.length&&dq[0]<i-k+1)dq.shift();while(dq.length&&nums[dq.at(-1)]<nums[i])dq.pop();dq.push(i);if(i>=k-1)res.push(nums[dq[0]]);}return res;}

// Q97. Next permutation O(n):
function nextPermutation(nums){let i=nums.length-2;while(i>=0&&nums[i]>=nums[i+1])i--;if(i>=0){let j=nums.length-1;while(nums[j]<=nums[i])j--;[nums[i],nums[j]]=[nums[j],nums[i]];}let l=i+1,r=nums.length-1;while(l<r){[nums[l],nums[r]]=[nums[r],nums[l]];l++;r--;}}

// Q98. Spiral order matrix:
function spiralOrder(m){const res=[];let t=0,b=m.length-1,l=0,r=m[0].length-1;while(t<=b&&l<=r){for(let i=l;i<=r;i++)res.push(m[t][i]);t++;for(let i=t;i<=b;i++)res.push(m[i][r]);r--;if(t<=b){for(let i=r;i>=l;i--)res.push(m[b][i]);b--;}if(l<=r){for(let i=b;i>=t;i--)res.push(m[i][l]);l++;}}return res;}

// Q99. Rotate array O(n) O(1):
function rotate(nums,k){k%=nums.length;const rev=(a,l,r)=>{while(l<r){[a[l],a[r]]=[a[r],a[l]];l++;r--;}};rev(nums,0,nums.length-1);rev(nums,0,k-1);rev(nums,k,nums.length-1);}

// Q100. Pascal's triangle:
function pascalTriangle(n){const res=[[1]];for(let i=1;i<n;i++){const row=[1];for(let j=1;j<i;j++)row.push(res[i-1][j-1]+res[i-1][j]);row.push(1);res.push(row);}return res;}

// Q101. Find peak element O(log n):
function findPeakElement(nums){let lo=0,hi=nums.length-1;while(lo<hi){const mid=(lo+hi)>>1;nums[mid]>nums[mid+1]?hi=mid:lo=mid+1;}return lo;}

// Q102. Search in rotated sorted array:
function searchRotated(nums,target){let lo=0,hi=nums.length-1;while(lo<=hi){const mid=(lo+hi)>>1;if(nums[mid]===target)return mid;if(nums[lo]<=nums[mid]){if(nums[lo]<=target&&target<nums[mid])hi=mid-1;else lo=mid+1;}else{if(nums[mid]<target&&target<=nums[hi])lo=mid+1;else hi=mid-1;}}return-1;}

// Q103. Find minimum in rotated sorted array:
function findMin(nums){let lo=0,hi=nums.length-1;while(lo<hi){const mid=(lo+hi)>>1;nums[mid]>nums[hi]?lo=mid+1:hi=mid;}return nums[lo];}

// Q104. Palindrome linked list O(n) O(1):
function isPalindrome(head){let slow=head,fast=head;while(fast?.next){slow=slow.next;fast=fast.next.next;}let prev=null,curr=slow;while(curr){const next=curr.next;curr.next=prev;prev=curr;curr=next;}let l=head,r=prev;while(r){if(l.val!==r.val)return false;l=l.next;r=r.next;}return true;}

// Q105. Add two numbers (linked list):
function addTwoNumbers(l1,l2){let dummy=new ListNode(0),curr=dummy,carry=0;while(l1||l2||carry){const sum=(l1?.val||0)+(l2?.val||0)+carry;carry=Math.floor(sum/10);curr.next=new ListNode(sum%10);curr=curr.next;l1=l1?.next;l2=l2?.next;}return dummy.next;}

// Q106. Intersection of two linked lists:
function getIntersectionNode(a,b){let pa=a,pb=b;while(pa!==pb){pa=pa?pa.next:b;pb=pb?pb.next:a;}return pa;}

// Q107. Reorder list (L0→Ln→L1→Ln-1):
function reorderList(head){let slow=head,fast=head;while(fast?.next){slow=slow.next;fast=fast.next.next;}let prev=null,curr=slow.next;slow.next=null;while(curr){const next=curr.next;curr.next=prev;prev=curr;curr=next;}let first=head,second=prev;while(second){const tmp1=first.next,tmp2=second.next;first.next=second;second.next=tmp1;first=tmp1;second=tmp2;}}

// Q108. Design Twitter (simplified):
class Twitter{#posts=new Map();#follows=new Map();#time=0;postTweet(u,t){if(!this.#posts.has(u))this.#posts.set(u,[]);this.#posts.get(u).unshift([this.#time++,t]);}getNewsFeed(u){const following=[...this.#follows.get(u)||[]];const tweets=[];for(const uid of[u,...following])for(const t of(this.#posts.get(uid)||[]).slice(0,10))tweets.push(t);return tweets.sort((a,b)=>b[0]-a[0]).slice(0,10).map(t=>t[1]);}follow(f,t){if(!this.#follows.has(f))this.#follows.set(f,new Set());this.#follows.get(f).add(t);}unfollow(f,t){this.#follows.get(f)?.delete(t);}}

// Q109. Random pick with weight:
class Solution{#prefix;constructor(w){this.#prefix=[0];for(const x of w)this.#prefix.push(this.#prefix.at(-1)+x);}pickIndex(){const r=Math.random()*this.#prefix.at(-1);let lo=1,hi=this.#prefix.length-1;while(lo<hi){const mid=(lo+hi)>>1;this.#prefix[mid]<r?lo=mid+1:hi=mid;}return lo-1;}}

// Q110. Word ladder BFS:
function ladderLength(begin,end,list){const set=new Set(list);if(!set.has(end))return 0;const q=[[begin,1]];set.delete(begin);while(q.length){const[word,len]=q.shift();for(let i=0;i<word.length;i++){for(let c=97;c<=122;c++){const nw=word.slice(0,i)+String.fromCharCode(c)+word.slice(i+1);if(nw===end)return len+1;if(set.has(nw)){set.delete(nw);q.push([nw,len+1]);}}}}return 0;}

// Q111. Implement Trie:
class Trie{root={};insert(w){let n=this.root;for(const c of w){n[c]=n[c]||{};n=n[c];}n.$=true;}search(w){let n=this.root;for(const c of w){if(!n[c])return false;n=n[c];}return!!n.$;}startsWith(p){let n=this.root;for(const c of p){if(!n[c])return false;n=n[c];}return true;}}

// Q112. Minimum path sum in grid:
function minPathSum(grid){const[m,n]=[grid.length,grid[0].length];for(let i=0;i<m;i++)for(let j=0;j<n;j++){if(i===0&&j===0)continue;const top=i>0?grid[i-1][j]:Infinity;const left=j>0?grid[i][j-1]:Infinity;grid[i][j]+=Math.min(top,left);}return grid[m-1][n-1];}

// Q113. Counting bits:
function countBits(n){const dp=new Array(n+1).fill(0);for(let i=1;i<=n;i++)dp[i]=dp[i>>1]+(i&1);return dp;}

// Q114. Power of two:
function isPowerOfTwo(n){return n>0&&(n&(n-1))===0;}

// Q115. Single number (XOR trick):
function singleNumber(nums){return nums.reduce((a,b)=>a^b,0);}

// Q116. Majority element (Boyer-Moore):
function majorityElement(nums){let candidate=null,count=0;for(const n of nums){if(count===0)candidate=n;count+=n===candidate?1:-1;}return candidate;}

// Q117. Max consecutive ones III:
function longestOnes(nums,k){let l=0,zeros=0,max=0;for(let r=0;r<nums.length;r++){if(!nums[r])zeros++;while(zeros>k){if(!nums[l++])zeros--;}max=Math.max(max,r-l+1);}return max;}

// Q118. Top K frequent elements:
function topKFrequent(nums,k){const freq=new Map();for(const n of nums)freq.set(n,(freq.get(n)||0)+1);return [...freq.entries()].sort((a,b)=>b[1]-a[1]).slice(0,k).map(e=>e[0]);}

// Q119. Kth largest in stream (min-heap of size k):
class KthLargest{#heap;#k;constructor(k,nums){this.#k=k;this.#heap=new MinHeap();for(const n of nums)this.add(n);}add(val){this.#heap.push(val);while(this.#heap.size>this.#k)this.#heap.pop();return this.#heap.peek();}}

// Q120. Design HashMap (chaining):
class MyHashMap{#b=new Array(1024).fill(null).map(()=>[]);#hash(k){return k%1024;}put(k,v){const b=this.#b[this.#hash(k)];const i=b.findIndex(([key])=>key===k);i>=0?b[i][1]=v:b.push([k,v]);}get(k){const b=this.#b[this.#hash(k)];return b.find(([key])=>key===k)?.[1]??-1;}remove(k){const b=this.#b[this.#hash(k)];const i=b.findIndex(([key])=>key===k);if(i>=0)b.splice(i,1);}}

// Q121–Q130: Final patterns
// Q121. Reverse bits: function reverseBits(n){let r=0;for(let i=0;i<32;i++){r=(r<<1)|(n&1);n>>>=1;}return r>>>0;}
// Q122. Hamming distance: function hammingDist(x,y){let n=x^y,c=0;while(n){n&=n-1;c++;}return c;}
// Q123. Missing number: function missingNumber(nums){return nums.length*(nums.length+1)/2-nums.reduce((a,b)=>a+b,0);}
// Q124. Sqrt(x) binary search: function mySqrt(x){let lo=0,hi=x;while(lo<hi){const mid=(lo+hi+1)>>1;mid*mid>x?hi=mid-1:lo=mid;}return lo;}
// Q125. Valid sudoku: check rows, cols, 3x3 boxes using Sets
// Q126. Implement queue with linked list: O(1) enqueue and dequeue
// Q127. Merge sorted array in-place: two pointers from end
// Q128. Pascal's triangle II (kth row only): dp array of length k
// Q129. Best time to buy and sell stock: track min price seen
// Q130. Binary watch: count set bits, generate valid times
```
