# DSA Mastery Guide — NeetCode 150 Focus
> Every pattern, every data structure, every algorithm explained from first principles with theory, diagrams, complexity analysis, and full solutions to the core NeetCode 150 problems.

---

## Table of Contents

### Part I — Foundations
1. [How to Think About Problems](#chapter-1-how-to-think-about-problems)
2. [Complexity Analysis — Big O](#chapter-2-complexity-analysis--big-o)
3. [Memory Model — Stack, Heap, Pointers](#chapter-3-memory-model)

### Part II — Linear Structures
4. [Arrays & Hashing](#chapter-4-arrays--hashing)
5. [Two Pointers](#chapter-5-two-pointers)
6. [Sliding Window](#chapter-6-sliding-window)
7. [Stack](#chapter-7-stack)
8. [Linked List](#chapter-8-linked-list)

### Part III — Non-Linear Structures
9. [Binary Search](#chapter-9-binary-search)
10. [Trees](#chapter-10-trees)
11. [Tries](#chapter-11-tries)
12. [Heap / Priority Queue](#chapter-12-heap--priority-queue)
13. [Backtracking](#chapter-13-backtracking)

### Part IV — Graphs
14. [Graph Theory & Representations](#chapter-14-graph-theory--representations)
15. [Graph BFS & DFS](#chapter-15-graph-bfs--dfs)
16. [Advanced Graphs](#chapter-16-advanced-graphs)

### Part V — Dynamic Programming
17. [1-D Dynamic Programming](#chapter-17-1-d-dynamic-programming)
18. [2-D Dynamic Programming](#chapter-18-2-d-dynamic-programming)
19. [Greedy Algorithms](#chapter-19-greedy-algorithms)
20. [Intervals](#chapter-20-intervals)
21. [Bit Manipulation](#chapter-21-bit-manipulation)
22. [Math & Geometry](#chapter-22-math--geometry)

---

# PART I — FOUNDATIONS

---

## Chapter 1: How to Think About Problems

### 1.1 The Problem-Solving Framework

Before writing a single line of code, follow this process every time:

```
1. UNDERSTAND
   - Read the problem at least twice
   - Identify: inputs, outputs, constraints
   - Ask: what are edge cases? (empty, one element, all same, negatives, overflow)
   - Ask: is input sorted? unsorted? unique? duplicates allowed?

2. EXAMPLES
   - Work through 2-3 examples by hand on paper
   - Use a tiny example first (n=3, not n=1000)
   - Try an edge case: empty input, single element, all same

3. BRUTE FORCE
   - Write the naive solution first — even O(n³) is fine at this stage
   - Correctness before optimization
   - This builds intuition for WHY a better solution exists

4. OPTIMIZE
   - Look for repeated work in the brute force
   - Ask: what data structure gives O(1) lookup? → HashMap
   - Ask: is there a pattern in how indices move? → Two Pointers / Sliding Window
   - Ask: can I precompute something? → Prefix Sum / Sorted Order

5. CODE
   - Write clean code with clear variable names
   - Handle edge cases first (empty input → return early)
   - Don't optimize prematurely

6. VERIFY
   - Trace through your examples manually
   - Check edge cases
   - Count operations mentally to confirm complexity
```

### 1.2 Recognizing Patterns

The key insight for NeetCode 150: **most problems fit ~15 patterns**. Once you recognize the pattern, the solution follows.

```
Input Type          → Pattern to Consider
──────────────────────────────────────────────────────────
Sorted array        → Two Pointers, Binary Search
Subarray/substring  → Sliding Window
Count/find pair     → HashMap
Tree                → DFS (recursion), BFS (queue)
Grid                → BFS (shortest), DFS (all paths)
Permutations/subsets→ Backtracking
Optimal subproblem  → Dynamic Programming
Intervals           → Sort + Greedy
Frequency           → HashMap or Heap
Top K               → Heap (Priority Queue)
String matching     → Trie
Connectivity        → Union-Find or DFS
Shortest path       → BFS (unweighted), Dijkstra (weighted)
```

---

## Chapter 2: Complexity Analysis — Big O

### 2.1 What Big O Measures

Big O describes how the **runtime** (or space usage) grows as the **input size n grows toward infinity**. It's about the *trend*, not exact values.

```
T(n) = 5n² + 3n + 100
        ↑      ↑    ↑
     dominant  lower  constant
     term      order  offset

Big O: O(n²) — we keep only the dominant term, drop constants
```

### 2.2 The Complexity Ladder

```
Complexity   | n=10  | n=100    | n=10,000       | Verdict
─────────────┼───────┼──────────┼────────────────┼──────────
O(1)         |    1  |       1  |              1 | ✅ Perfect
O(log n)     |    3  |       7  |             14 | ✅ Excellent
O(n)         |   10  |     100  |         10,000 | ✅ Good
O(n log n)   |   33  |     664  |        132,877 | ✅ Acceptable
O(n²)        |  100  |  10,000  |    100,000,000 | ⚠️ Slow for large n
O(2ⁿ)        | 1024  |  ~10³⁰  |    astronomical | ❌ Only for tiny n
O(n!)        |3.6M   |  ~10¹⁵⁷  |    impossible  | ❌ Never for n>15
```

### 2.3 Calculating Complexity — Rules

```python
# Rule 1: Drop constants
for i in range(n):
    print(i)          # O(n)
for i in range(n):
    print(i)          # O(n)
# Total: O(2n) = O(n)

# Rule 2: Drop lower-order terms
for i in range(n):          # O(n)
    for j in range(n):      # O(n)
        pass                # O(n²)
for i in range(n):          # + O(n)
    pass
# Total: O(n² + n) = O(n²)

# Rule 3: Nested loops multiply
for i in range(n):
    for j in range(n):       # n × n = n²
        for k in range(n):   # n² × n = n³
            pass             # O(n³)

# Rule 4: Sequential operations add
for i in range(n):   pass   # O(n)
for i in range(m):   pass   # O(m)
# Total: O(n + m)

# Rule 5: Recursion — draw the recursion tree
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
# Each call spawns 2 children; tree depth = n
# Total nodes = 2^0 + 2^1 + ... + 2^n = 2^(n+1) - 1 = O(2^n)
```

### 2.4 Space Complexity

```python
# O(1) space — fixed extra memory regardless of n
def sum_array(arr):
    total = 0          # 1 variable
    for x in arr:
        total += x
    return total

# O(n) space — extra memory proportional to n
def copy_array(arr):
    result = []
    for x in arr:
        result.append(x)   # n elements stored
    return result

# O(n) space — recursion call stack depth = n
def factorial(n):
    if n == 0: return 1
    return n * factorial(n - 1)   # n frames on call stack simultaneously

# O(log n) space — binary search recursion depth = log n
def bin_search(arr, lo, hi, target):
    if lo > hi: return -1
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    if arr[mid] < target: return bin_search(arr, mid+1, hi, target)
    return bin_search(arr, lo, mid-1, target)
```

### 2.5 Common Data Structure Complexities

```
Data Structure      | Access | Search | Insert | Delete | Space
────────────────────┼────────┼────────┼────────┼────────┼──────
Array               |  O(1)  |  O(n)  |  O(n)  |  O(n)  | O(n)
Sorted Array        |  O(1)  | O(logn)|  O(n)  |  O(n)  | O(n)
Linked List         |  O(n)  |  O(n)  |  O(1)* |  O(1)* | O(n)
Stack (array)       |  O(n)  |  O(n)  |  O(1)  |  O(1)  | O(n)
Queue (deque)       |  O(n)  |  O(n)  |  O(1)  |  O(1)  | O(n)
Hash Table          |   —    |  O(1)† |  O(1)† |  O(1)† | O(n)
BST (balanced)      |  O(logn)| O(logn)| O(logn)| O(logn)| O(n)
Heap                |  O(1)‡ |  O(n)  | O(logn)| O(logn)| O(n)
Trie                |   —    | O(m)   | O(m)   | O(m)   | O(n·m)

* at known position  † average case  ‡ peek only (min/max)
m = key length
```

---

## Chapter 3: Memory Model

### 3.1 How Arrays Work in Memory

```
arr = [3, 1, 4, 1, 5, 9]

Memory address: 1000  1004  1008  1012  1016  1020
                 [3]   [1]   [4]   [1]   [5]   [9]
                  ↑
              arr[0]

arr[i] address = base_address + i × element_size
arr[3] address = 1000 + 3 × 4 = 1012   → value: 1

This is why random access is O(1):
arithmetic to compute the address, then ONE memory read
```

### 3.2 How Hash Tables Work

A HashMap achieves O(1) average get/put through hashing:

```
key → hash(key) → hash(key) % capacity → bucket index

"Alice" → hash("Alice") = 5318008 → 5318008 % 16 = 8 → bucket[8]

Without collision:
  put("Alice", 90):  bucket[8] = ("Alice", 90)
  get("Alice"):      hash → 8 → return bucket[8].value = 90

With collision (two keys hash to same bucket):
  Method 1: Chaining — each bucket is a linked list
  Method 2: Open addressing — probe for next empty bucket

Load factor = n / capacity (n = stored items)
Python dict resizes when load factor > 0.67
Java HashMap resizes when load factor > 0.75
Resize doubles capacity → O(n) work but amortized O(1)
```

### 3.3 Pointer Arithmetic (Linked Lists)

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None   # None = null pointer

# Building: 1 → 2 → 3 → None
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.next = n2
n2.next = n3

# Traversal — follow .next until None
cur = n1
while cur:
    print(cur.val)
    cur = cur.next    # advance pointer

# Key insight: cur = cur.next moves the POINTER, not the node
# The node n1 still exists; we just don't have a local variable pointing to it
```

---

# PART II — LINEAR STRUCTURES

---

## Chapter 4: Arrays & Hashing

### 4.1 The Core Idea

Arrays + HashMaps together solve a huge class of problems. The pattern:
- **Brute force**: nested loops → O(n²)
- **Optimization**: store things you've seen in a HashMap → O(n)

Every time you think "for each element, I need to check all other elements" — ask: "can I store something in a HashMap and look it up in O(1)?"

### 4.2 Prefix Sums — Precomputation

```
Problem: Given array, answer many range sum queries [i, j].
Naive: scan [i..j] each time → O(n) per query
Prefix sum: precompute → O(1) per query

prefix[0] = 0
prefix[k] = arr[0] + arr[1] + ... + arr[k-1]
range_sum(i, j) = prefix[j+1] - prefix[i]

Example: arr = [2, 4, 1, 3, 5]
prefix = [0, 2, 6, 7, 10, 15]
sum(1,3) = prefix[4] - prefix[1] = 10 - 2 = 8  ✓ (4+1+3=8)
```

```python
def build_prefix(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, i, j):
    return prefix[j+1] - prefix[i]
```

### NeetCode Problem: Contains Duplicate

**Problem:** Given integer array, return true if any value appears at least twice.

```
Brute force: for each pair (i,j), check if arr[i]==arr[j] → O(n²)
Better: store seen values in a set → O(n) time, O(n) space
Even better for space: sort first → O(n log n) time, O(1) space
```

```python
# Solution 1: HashSet — O(n) time, O(n) space
def containsDuplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False

# Solution 2: One-liner
def containsDuplicate(nums):
    return len(nums) != len(set(nums))
```

### NeetCode Problem: Valid Anagram

**Problem:** Given two strings s and t, return true if t is an anagram of s.

```
Key insight: two strings are anagrams iff they have identical character frequencies.

"anagram" → {a:3, n:1, g:1, r:1, m:1}
"nagaram" → {n:1, a:3, g:1, r:1, m:1}   ← same map
```

```python
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        if c not in count or count[c] == 0:
            return False
        count[c] -= 1
    return True

# Pythonic version:
from collections import Counter
def isAnagram(s, t):
    return Counter(s) == Counter(t)
```

### NeetCode Problem: Two Sum

**Problem:** Given integer array and target, return indices of two numbers that add to target.

```
Brute force: for every pair (i,j) check if arr[i]+arr[j]==target → O(n²)

Insight: if arr[i] + arr[j] == target, then arr[j] = target - arr[i]
As we scan: for each arr[i], look up (target - arr[i]) in a HashMap.
Store {value → index} as we go.

Example: nums=[2,7,11,15], target=9
i=0: need 9-2=7. Not in map. Store {2:0}
i=1: need 9-7=2. Found 2 at index 0! Return [0,1]
```

```python
def twoSum(nums, target):
    seen = {}  # value → index
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []
```

### NeetCode Problem: Group Anagrams

**Problem:** Given array of strings, group anagrams together.

```
Key insight: sort each string → anagrams become identical keys.
"eat" → "aet", "tea" → "aet", "tan" → "ant", "nat" → "ant", "bat" → "abt"

HashMap: sorted_str → [original strings]
```

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))   # "eat" → ('a','e','t')
        groups[key].append(s)
    return list(groups.values())

# Alternative: use character count as key (no sorting, O(n·k))
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
```

### NeetCode Problem: Top K Frequent Elements

**Problem:** Given integer array and k, return k most frequent elements.

```
Step 1: count frequencies with HashMap
Step 2: find top k — use a heap or bucket sort

Bucket sort insight: max frequency ≤ n (length of array)
Create buckets: bucket[freq] = [elements with that frequency]
Scan buckets from high frequency to low, collect k elements.
```

```python
def topKFrequent(nums, k):
    # Count frequencies: O(n)
    count = {}
    for n in nums:
        count[n] = count.get(n, 0) + 1

    # Bucket sort by frequency: O(n)
    freq = [[] for _ in range(len(nums) + 1)]
    for num, cnt in count.items():
        freq[cnt].append(num)

    # Collect top k from highest frequency: O(n)
    result = []
    for i in range(len(freq) - 1, 0, -1):
        for n in freq[i]:
            result.append(n)
            if len(result) == k:
                return result
```

### NeetCode Problem: Product of Array Except Self

**Problem:** Return array output where output[i] = product of all nums except nums[i]. No division allowed.

```
Key insight: output[i] = (product of everything LEFT of i) × (product of everything RIGHT of i)

Two passes:
Pass 1 (left to right):  prefix[i] = product of arr[0..i-1]
Pass 2 (right to left):  suffix[i] = product of arr[i+1..n-1]

output[i] = prefix[i] × suffix[i]

Example: nums = [1, 2, 3, 4]
Prefix:  [1, 1, 2, 6]      prefix[0]=1, prefix[1]=1, prefix[2]=1*2=2, prefix[3]=2*3=6
Suffix:  [24,12, 4, 1]
Output:  [1*24, 1*12, 2*4, 6*1] = [24, 12, 8, 6]  ✓
```

```python
def productExceptSelf(nums):
    n = len(nums)
    output = [1] * n

    # Pass 1: store prefix products in output
    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    # Pass 2: multiply by suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output
# Time: O(n), Space: O(1) extra (output array doesn't count)
```

### NeetCode Problem: Longest Consecutive Sequence

**Problem:** Given unsorted array, find length of longest consecutive sequence. Must be O(n).

```
Naive: sort → O(n log n)
O(n) insight: only START counting from a sequence's first element.
A number n is the START of a sequence if (n-1) is NOT in the set.

For each start, count forward: n, n+1, n+2, ...

nums = [100, 4, 200, 1, 3, 2]
Set = {100, 4, 200, 1, 3, 2}

1 → (1-1=0 not in set) → start! count: 1→2→3→4 = 4
2 → (2-1=1 in set) → skip
3 → skip, 4 → skip, 100 → start, length 1. 200 → start, length 1.
Answer: 4
```

```python
def longestConsecutive(nums):
    num_set = set(nums)
    best = 0

    for n in num_set:
        if (n - 1) not in num_set:  # only start from sequence start
            length = 1
            while (n + length) in num_set:
                length += 1
            best = max(best, length)

    return best
# Time: O(n) — each number visited at most twice (once in outer loop, once counted)
```

### NeetCode Problem: Encode and Decode Strings

**Problem:** Design encode/decode for a list of strings (for network transmission).

```
Challenge: strings can contain any character including delimiters.
Solution: length-prefix encoding — prepend the length + a separator.

encode(["neet","code","love","you"])
→ "4#neet4#code4#love3#you"

decode: read until '#', parse length, read that many chars
```

```python
def encode(strs):
    return ''.join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    result = []
    i = 0
    while i < len(s):
        j = s.index('#', i)
        length = int(s[i:j])
        result.append(s[j+1 : j+1+length])
        i = j + 1 + length
    return result
```

### NeetCode Problem: Valid Sudoku

**Problem:** Determine if a 9×9 board is valid (no repeats in rows, cols, 3×3 boxes).

```
Key insight: track three sets of constraints:
  - For each row: seen digits
  - For each column: seen digits  
  - For each 3×3 box: seen digits

Box index trick: box = (row//3, col//3)
  row=0..2, col=0..2 → box (0,0)
  row=0..2, col=3..5 → box (0,1)
  etc.
```

```python
def isValidSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]  # 9 boxes indexed 0-8

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue

            box_idx = (r // 3) * 3 + (c // 3)

            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False

            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)

    return True
```

---

## Chapter 5: Two Pointers

### 5.1 The Pattern

Two pointers work when the array/string has some **ordered property** you can exploit to eliminate possibilities without checking all pairs.

```
Classic setup: sorted array, find pair summing to target.
Brute force: O(n²) — check every pair.

Two pointers:
  left = 0, right = n-1
  if arr[left] + arr[right] == target → found
  if arr[left] + arr[right] < target  → need bigger sum → left++
  if arr[left] + arr[right] > target  → need smaller sum → right--

Why it works: when we move left++, we permanently discard arr[left] with EVERY right ≥ current right.
We know none of those pairs work. So we never check them — correct AND efficient.
```

```
Variants:
  ① Same-direction: slow and fast pointer (e.g., remove duplicates)
  ② Opposite-direction: converging (e.g., two sum sorted, trapping rain)
  ③ Three pointers: outer loop + inner two pointers (3Sum)
```

### NeetCode Problem: Valid Palindrome

**Problem:** Given string, return true if palindrome after removing non-alphanumeric and lowercasing.

```
Two pointers converge from outside in:
left → ← right
Skip non-alphanumeric. Compare.
```

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1

    return True
```

### NeetCode Problem: Two Sum II (sorted input)

**Problem:** Given sorted array, return 1-indexed positions of two numbers summing to target.

```python
def twoSum(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        elif s < target:
            left += 1
        else:
            right -= 1
```

### NeetCode Problem: 3Sum

**Problem:** Find all unique triplets summing to zero.

```
Fix one element (nums[i]), then two-pointer on the rest.
Sort first → enables two-pointer AND easy duplicate skipping.

nums = [-4,-1,-1,0,1,2]

For i=0 (nums[i]=-4): find pair summing to 4 in [-1,-1,0,1,2]
  left=1(-1), right=5(2): sum=-1+2=1 < 4, left++
  left=2(-1), right=5(2): sum=-1+2=1 < 4, left++
  left=3(0),  right=5(2): sum=0+2=2 < 4, left++
  left=4(1),  right=5(2): sum=1+2=3 < 4, left++
  → no pair found

For i=1 (nums[i]=-1): find pair summing to 1 in [0,1,2]
  Actually: left=2(-1), right=5(2): sum=(-1)+2=1 == 1 → add [-1,-1,2]
  Skip duplicates: left=3(0), right=4(1): sum=1 == 1 → add [-1,0,1]
```

```python
def threeSum(nums):
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        # Skip duplicate values for the fixed element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates on both ends
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1

    return result
```

### NeetCode Problem: Container With Most Water

**Problem:** n vertical lines at positions 0..n-1 with heights. Find two lines that hold the most water.

```
water = min(height[left], height[right]) × (right - left)

Key insight: to maximize water, we want both height and width.
Width decreases as we move inward. So we should only move inward
if it might increase height enough to compensate.

The shorter line limits the water. Moving the shorter-line pointer
inward MIGHT find a taller line → might increase water.
Moving the taller-line pointer inward NEVER increases water
(width decreases and height can only be limited by shorter line).

→ Always move the pointer with the shorter line.
```

```python
def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water
```

### NeetCode Problem: Trapping Rain Water

**Problem:** Given height array, compute total water trapped.

```
For each position i: water[i] = max(0, min(maxLeft[i], maxRight[i]) - height[i])
where maxLeft[i] = max height to the left, maxRight[i] = max height to the right.

Two-pointer O(n) space O(1):
The water at position i is determined by the minimum of maxLeft and maxRight.
If maxLeft < maxRight: water[left] = maxLeft - height[left]
  (we don't need to know exact maxRight — it's at least maxRight which is > maxLeft)
Move the left pointer.

heights = [0,1,0,2,1,0,1,3,2,1,2,1]

  maxLeft=0, maxRight=1→3→2→...
  Process left side when maxLeft < maxRight
```

```python
def trap(height):
    left, right = 0, len(height) - 1
    max_left = max_right = 0
    water = 0

    while left < right:
        if max_left <= max_right:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                water += max_right - height[right]
            right -= 1

    return water
```

---

## Chapter 6: Sliding Window

### 6.1 The Pattern

A **window** is a contiguous subarray/substring. The window slides by expanding the right end and shrinking the left end.

```
Types:
  ① Fixed size window: window stays exactly size k
  ② Variable size window: window expands/shrinks based on condition

Template (variable):
  left = 0
  for right in range(n):
      add nums[right] to window
      while window is INVALID:
          remove nums[left] from window
          left += 1
      update answer (window is now valid and as large as possible)

The key: each element is added and removed at most once → O(n) total.
```

### NeetCode Problem: Best Time to Buy and Sell Stock

**Problem:** Find max profit from single buy+sell. Must buy before sell.

```
Sliding window where left = buy day, right = sell day.
If price[right] < price[left]: we found a better buy day → move left to right.
Otherwise: update max profit.
```

```python
def maxProfit(prices):
    left = 0   # buy pointer
    max_profit = 0

    for right in range(1, len(prices)):
        if prices[right] < prices[left]:
            left = right            # better buy price found
        else:
            profit = prices[right] - prices[left]
            max_profit = max(max_profit, profit)

    return max_profit
```

### NeetCode Problem: Longest Substring Without Repeating Characters

**Problem:** Find length of longest substring without duplicate characters.

```
Sliding window with a set to track characters in current window.
When we see a duplicate: shrink from left until duplicate is removed.

"abcabcbb"
right=0: add 'a' → {a}, len=1
right=1: add 'b' → {a,b}, len=2
right=2: add 'c' → {a,b,c}, len=3
right=3: 'a' in set → remove left='a' → {b,c} → add 'a' → {b,c,a}, len=3
right=4: 'b' in set → remove left='b' → {c,a} → add 'b' → {c,a,b}, len=3
...
```

```python
def lengthOfLongestSubstring(s):
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

### NeetCode Problem: Longest Repeating Character Replacement

**Problem:** Replace at most k characters in string. Find longest substring with all same char.

```
Key insight: for a window of length L with most_frequent character appearing f times,
we need L - f replacements. Valid window iff L - f ≤ k.

Rearranged: L ≤ f + k

We want to maximize L. Track max_freq (maximum frequency of any char seen so far).
When (right - left + 1) - max_freq > k: shrink from left.

Note: we never decrease max_freq even when left shrinks.
This is fine because we want the MAXIMUM window ever seen.
```

```python
def characterReplacement(s, k):
    count = {}
    left = 0
    max_freq = 0
    result = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])

        # Window length - max frequency = chars to replace
        window_len = right - left + 1
        if window_len - max_freq > k:
            count[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result
```

### NeetCode Problem: Permutation in String

**Problem:** Return true if s2 contains a permutation of s1.

```
Fixed-size sliding window of length len(s1) across s2.
Window is valid iff frequency counts match.

Maintain: count of chars needed (s1 count minus what's in window).
Track 'have' = number of chars whose count is satisfied.
Valid when have == need.

Optimization: instead of comparing entire frequency arrays each step,
maintain 'have' and 'need' counters.
```

```python
def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False

    count_s1 = [0] * 26
    window  = [0] * 26

    for c in s1:
        count_s1[ord(c) - ord('a')] += 1

    have = need = 0
    for i in range(26):
        if count_s1[i] > 0:
            need += 1

    left = 0
    for right in range(len(s2)):
        c = ord(s2[right]) - ord('a')
        window[c] += 1
        if window[c] == count_s1[c]:
            have += 1

        if right - left + 1 > len(s1):
            lc = ord(s2[left]) - ord('a')
            if window[lc] == count_s1[lc]:
                have -= 1
            window[lc] -= 1
            left += 1

        if have == need:
            return True

    return False
```

### NeetCode Problem: Minimum Window Substring

**Problem:** Find minimum window in s that contains all characters of t.

```
Variable sliding window.
Expand right to include all chars of t ('have' == 'need').
Then shrink left to minimize while still valid.
Track minimum valid window seen.
```

```python
from collections import Counter

def minWindow(s, t):
    if not t: return ""

    need = Counter(t)          # chars needed and their counts
    have = {}
    formed = 0                 # chars whose count is fully satisfied
    required = len(need)       # distinct chars in t

    left = 0
    best = float('inf'), 0, 0  # (length, left, right)

    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1

        while formed == required:
            # Update best window
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)

            # Shrink from left
            lc = s[left]
            have[lc] -= 1
            if lc in need and have[lc] < need[lc]:
                formed -= 1
            left += 1

    return "" if best[0] == float('inf') else s[best[1]: best[2]+1]
```

### NeetCode Problem: Sliding Window Maximum

**Problem:** Given array and window size k, return max of each window.

```
Naive: O(n·k) — scan each window.
Optimal: O(n) using a monotonic deque.

Monotonic decreasing deque: stores INDICES, front = index of current max.
For each new element:
  1. Remove from front if outside window (deque[0] < i-k+1)
  2. Remove from back while back's value ≤ current (they can never be max)
  3. Add current index to back
  4. Front of deque = max of current window

Deque maintains DECREASING order of values → front is always max.
```

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()  # indices, front = largest value's index
    result = []

    for i, n in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be the max)
        while dq and nums[dq[-1]] < n:
            dq.pop()

        dq.append(i)

        # Window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Chapter 7: Stack

### 7.1 The Pattern

A stack (LIFO) is the right tool when:
- You need to process things in **reverse order** of arrival
- You need to match/validate **nested structures** (parentheses, brackets)
- You need the **nearest previous/next larger/smaller element** → Monotonic Stack

### Monotonic Stack — The Key Insight

```
"Next Greater Element" — for each element, find the next one to its right that's larger.

Brute force: O(n²) — scan right for each element.

Monotonic stack: O(n)
Maintain a stack of "waiting" elements — elements that haven't found their NGE yet.
When we process num[i]:
  - Pop all elements from stack that are SMALLER than num[i]
    → num[i] is their Next Greater Element
  - Push num[i] onto stack

Example: [2, 1, 5, 6, 2, 3]
i=0: stack=[], push 2. stack=[2]
i=1: 1 < 2, push. stack=[2,1]
i=2: 5 > 1, pop 1 (NGE=5). 5 > 2, pop 2 (NGE=5). push 5. stack=[5]
i=3: 6 > 5, pop 5 (NGE=6). push 6. stack=[6]
i=4: 2 < 6, push. stack=[6,2]
i=5: 3 > 2, pop 2 (NGE=3). 3 < 6, push. stack=[6,3]
End: remaining [6,3] → no NGE → -1

Result: [5,5,6,-1,3,-1]
```

### NeetCode Problem: Valid Parentheses

**Problem:** Given string of `()[]{}`, determine if input is valid.

```python
def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for c in s:
        if c in '([{':
            stack.append(c)
        else:
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()

    return len(stack) == 0
```

### NeetCode Problem: Min Stack

**Problem:** Stack supporting push, pop, top, and getMin in O(1).

```
Key insight: maintain a parallel stack of minimums.
min_stack[i] = minimum of all elements at indices 0..i.

On push(val): push to main stack; push min(val, min_stack[-1]) to min stack.
On pop(): pop both stacks.
getMin(): peek min stack.
```

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # min_stack[i] = min of stack[0..i]

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```

### NeetCode Problem: Evaluate Reverse Polish Notation

**Problem:** Evaluate expression in RPN: `["2","1","+","3","*"]` → ((2+1)*3) = 9.

```
RPN eliminates need for parentheses. Use stack:
- Number → push
- Operator → pop two, apply, push result

["2","1","+","3","*"]
"2" → stack=[2]
"1" → stack=[2,1]
"+" → pop 1,2 → 3 → stack=[3]
"3" → stack=[3,3]
"*" → pop 3,3 → 9 → stack=[9]
Return 9
```

```python
def evalRPN(tokens):
    stack = []
    ops = {'+', '-', '*', '/'}

    for token in tokens:
        if token not in ops:
            stack.append(int(token))
        else:
            b = stack.pop()  # second operand
            a = stack.pop()  # first operand
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            else: stack.append(int(a / b))  # truncate toward zero

    return stack[0]
```

### NeetCode Problem: Generate Parentheses

**Problem:** Generate all valid combinations of n pairs of parentheses.

```
Backtracking with a stack to track current string.
Rules:
  - Add '(' if open_count < n
  - Add ')' if close_count < open_count
  - Base case: when len(current) == 2*n, add to result

n=2: 
  "(("  → "(()": close "(())" → valid!
                → "((" → cannot add more '(' (open=2=n), must add ')': "(())"
       → "()" → "()(": → "()()" valid!
```

```python
def generateParenthesis(n):
    result = []

    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result
```

### NeetCode Problem: Daily Temperatures

**Problem:** For each day, how many days until a warmer temperature? 

```
Classic "next greater element" with monotonic stack.
Stack stores INDICES of temperatures waiting for their warmer day.
```

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # indices waiting for warmer day

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)

    return result  # remaining indices in stack → default 0 (no warmer day)
```

### NeetCode Problem: Car Fleet

**Problem:** n cars drive to target. car[i] = (position, speed). How many fleets arrive?

```
Key insight: a faster car behind a slower car catches up → they form a fleet.
Sort by position (descending). Use a stack.

Time for car i to reach target: time[i] = (target - pos[i]) / speed[i]

Process from closest to target to farthest.
If current car arrives faster than car in front → it catches up → same fleet (pop).
Wait... actually simpler:
  Stack stores arrival times of distinct fleets.
  If current car arrives <= stack top (the fleet ahead arrives later),
    current car catches up → merge (don't push).
  If current car arrives > stack top → separate fleet (push).
```

```python
def carFleet(target, position, speed):
    # Sort by position descending (closest to target first)
    cars = sorted(zip(position, speed), key=lambda x: -x[0])
    stack = []  # arrival times of fleets

    for pos, spd in cars:
        time = (target - pos) / spd
        # If this car arrives before or at same time as car ahead,
        # it catches up → joins that fleet → don't add to stack
        if not stack or time > stack[-1]:
            stack.append(time)

    return len(stack)
```

### NeetCode Problem: Largest Rectangle in Histogram

**Problem:** Find area of largest rectangle in histogram.

```
Key insight: for each bar, the maximum rectangle extending left and right
is bounded by the first shorter bar on each side.

Monotonic stack (increasing): when we encounter a bar shorter than stack top,
we can calculate the rectangle for the stack top (it can't extend further right).

Height: height of popped bar
Width: current_index - stack[-1] - 1 (or current_index if stack is empty)

heights = [2,1,5,6,2,3]

i=0: stack=[], push (0,2). stack=[(0,2)]
i=1: h=1 < h=2. Pop (0,2): area=2*(1-(-1)-1)=2*1=2? 

Better to store just indices and compute:

stack stores indices of bars in increasing height order.
When popping bar at index j:
  width = i - stack[-1] - 1  (distance between current and new top)
  if stack empty: width = i
  area = heights[j] * width
```

```python
def largestRectangleArea(heights):
    stack = []  # indices, increasing heights
    max_area = 0
    heights = heights + [0]  # sentinel 0 at end forces all bars to be processed

    for i, h in enumerate(heights):
        start = i  # left boundary of the rectangle being formed
        while stack and heights[stack[-1]] > h:
            j = stack.pop()
            width = i - (stack[-1] if stack else -1) - 1
            max_area = max(max_area, heights[j] * width)
            start = j  # rectangle can extend to where j's bar started
        stack.append(i)  # push current index (representing height h)

    return max_area
```

---

## Chapter 8: Linked List

### 8.1 Core Techniques

```
1. Dummy head node — eliminates edge cases for head modifications
2. Two-pointer (slow/fast) — cycle detection, find middle
3. Reverse — iterative pointer manipulation
4. Merge — combine two sorted lists
```

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### NeetCode Problem: Reverse Linked List

**Problem:** Reverse a singly linked list.

```
Iterative:
1 → 2 → 3 → 4 → 5 → None
↑prev=None, ↑cur

Step 1: save cur.next, point cur.next to prev, advance prev and cur
prev=None, cur=1: next=2, 1.next=None, prev=1, cur=2
prev=1,    cur=2: next=3, 2.next=1,    prev=2, cur=3
...
Result: None ← 1 ← 2 ← 3 ← 4 ← 5, prev=5 (new head)
```

```python
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev  # new head

# Recursive version
def reverseList(head):
    if not head or not head.next:
        return head
    new_head = reverseList(head.next)  # reverse rest
    head.next.next = head              # point next node back to head
    head.next = None                   # remove forward link
    return new_head
```

### NeetCode Problem: Merge Two Sorted Lists

**Problem:** Merge two sorted linked lists into one sorted list.

```
Dummy head eliminates the "which list is the new head" edge case.
```

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)
    curr = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next

    curr.next = list1 or list2  # attach remaining non-empty list
    return dummy.next
```

### NeetCode Problem: Reorder List

**Problem:** Reorder L0→L1→…→Ln to L0→Ln→L1→Ln-1→…

```
Three steps:
1. Find middle (slow/fast pointers)
2. Reverse second half
3. Merge two halves

1→2→3→4→5
Step 1: mid=3 → split: [1→2→3] and [4→5]
Step 2: reverse second: [5→4]
Step 3: merge: 1→5→2→4→3
```

```python
def reorderList(head):
    if not head or not head.next:
        return

    # Step 1: Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None  # cut list at middle

    # Step 2: Reverse second half
    prev = None
    curr = second
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev

    # Step 3: Merge
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2
```

### NeetCode Problem: Remove Nth Node From End

**Problem:** Remove the nth node from end of list.

```
Two-pointer trick: advance fast pointer n steps first.
Then move both slow and fast together.
When fast reaches the end, slow is at the node BEFORE the target.

Example: 1→2→3→4→5, n=2 (remove 4th from start = 2nd from end)
fast advances 2 steps: fast=3
move both: slow=1→2→3, fast=3→4→5
fast hits end: slow=3 (node before 4)
slow.next = slow.next.next → remove 4
```

```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy

    # Advance fast by n+1 (so slow stops at node BEFORE target)
    for _ in range(n + 1):
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next
```

### NeetCode Problem: Copy List with Random Pointer

**Problem:** Deep copy linked list where each node has `next` and `random` pointer.

```
Challenge: when copying node i, its random might point to node j that hasn't been created yet.

Two-pass with HashMap:
  Pass 1: create copy of every node, store old→new in map
  Pass 2: set next and random pointers using the map
```

```python
def copyRandomList(head):
    if not head: return None

    old_to_new = {}

    # Pass 1: create all nodes
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # Pass 2: set pointers
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next

    return old_to_new[head]
```

### NeetCode Problem: Add Two Numbers

**Problem:** Two non-empty linked lists represent two non-negative integers (digits in reverse). Return sum as linked list.

```
342 + 465 = 807
[2→4→3] + [5→6→4] = [7→0→8]

Simulate addition digit by digit with carry.
```

```python
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)

        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next
```

### NeetCode Problem: Linked List Cycle

**Problem:** Determine if linked list has a cycle.

```
Floyd's Cycle Detection (Tortoise and Hare):
  slow moves 1 step, fast moves 2 steps per iteration.
  If cycle exists: fast gains 1 step on slow per iteration
  → they will eventually meet inside the cycle.
  If no cycle: fast reaches None.

Why they meet: when slow enters cycle, fast is somewhere in it.
Distance fast must close = some value k. Fast closes 1 per step → they meet in k steps.
```

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start (for "Linked List Cycle II"):
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Phase 2: move one pointer to head, advance both one step
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow  # cycle start
    return None
```

### NeetCode Problem: Find the Duplicate Number

**Problem:** Array of n+1 integers in range [1,n]. One number repeats. Find it. No extra space.

```
Treat array as linked list: index → value = next node.
nums[i] = j means there's an edge from i to j.
Duplicate number = cycle start (two indices point to same value).

Apply Floyd's cycle detection!
Phase 1: find meeting point.
Phase 2: find cycle start.
```

```python
def findDuplicate(nums):
    slow = fast = 0
    # Phase 1: find intersection point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: find cycle start
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

### NeetCode Problem: LRU Cache

**Problem:** Implement LRU Cache with O(1) get and put.

```
Data structure: HashMap + Doubly Linked List

HashMap: key → node (O(1) access)
DLL: nodes in order of recency (head=LRU, tail=MRU)

get(key): move node to tail (most recently used)
put(key, val): 
  - if key exists: update value, move to tail
  - if key new: add node at tail
  - if over capacity: remove head (LRU)

Dummy head and tail simplify insertion/removal edge cases.
```

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}           # key → node
        self.head = Node()        # dummy LRU (least recently used)
        self.tail = Node()        # dummy MRU (most recently used)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_tail(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._insert_at_tail(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_at_tail(node)
        if len(self.cache) > self.cap:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]
```

### NeetCode Problem: Merge K Sorted Lists

**Problem:** Merge k sorted linked lists into one sorted linked list.

```
Approach 1: Divide & Conquer (like merge sort)
  Pair up lists, merge pairs, repeat until 1 list.
  k lists, each of length n → O(n·k·log k)

Approach 2: Min-Heap
  Push first node of each list into min-heap.
  Pop minimum → add to result → push popped node's next.
  O(n·k·log k) same complexity but simpler to reason about.
```

```python
import heapq

def mergeKLists(lists):
    dummy = ListNode(0)
    curr = dummy
    heap = []

    # Push (value, index, node) — index breaks ties
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

### NeetCode Problem: Reverse Nodes in k-Group

**Problem:** Reverse nodes of list k at a time.

```
1→2→3→4→5, k=2 → 2→1→4→3→5

For each group:
1. Check if k nodes remain (if not, leave as is)
2. Reverse those k nodes
3. Connect to previous group and next group

Use dummy head. Track: prev_tail (end of already-processed part)
and group_start (start of current group).

After reversing a group:
  prev_tail.next = group_end (new start of reversed group)
  group_start.next = next_group_start
  prev_tail = group_start (it's now the tail of the reversed group)
```

```python
def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    prev_group_tail = dummy

    while True:
        # Check if k nodes remain
        kth = prev_group_tail
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        group_start = prev_group_tail.next
        next_group_start = kth.next

        # Reverse k nodes
        prev, curr = next_group_start, group_start
        for _ in range(k):
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Connect to surrounding groups
        prev_group_tail.next = kth        # kth is now the group's new head
        group_start.next = next_group_start  # group_start is now the tail
        prev_group_tail = group_start

    return dummy.next
```

---

# PART III — NON-LINEAR STRUCTURES

---

## Chapter 9: Binary Search

### 9.1 The Pattern — Thinking in Halves

Binary search works on any **monotone predicate**: a condition that is False for all inputs below some threshold and True for all inputs above (or vice versa). You're not just searching sorted arrays — you're searching the answer space.

```
Template: Find the FIRST position where condition(x) is True.

lo, hi = smallest_possible, largest_possible
while lo < hi:
    mid = lo + (hi - lo) // 2   # avoid overflow; prefer this over (lo+hi)//2
    if condition(mid):
        hi = mid                 # mid might be the answer; don't exclude it
    else:
        lo = mid + 1             # mid definitely not the answer
return lo                        # lo == hi == answer

Variant: Find the LAST position where condition(x) is True.
while lo < hi:
    mid = lo + (hi - lo + 1) // 2  # +1 to avoid infinite loop when lo+1==hi
    if condition(mid):
        lo = mid
    else:
        hi = mid - 1
return lo
```

### 9.2 Common Binary Search Bugs

```python
# Bug 1: Wrong boundary — off by one
# Wrong: while lo <= hi → might miss convergence case
# Right: while lo < hi (for left/right boundary templates)
# For "find exact": while lo <= hi works fine

# Bug 2: Infinite loop
mid = (lo + hi) // 2
if condition(mid): lo = mid   # if lo+1==hi, mid==lo, lo never changes!
# Fix: mid = lo + (hi - lo + 1) // 2  when updating lo=mid

# Bug 3: Integer overflow (mainly in C++/Java)
mid = (lo + hi) // 2          # Python has arbitrary precision, fine
mid = lo + (hi - lo) // 2     # C++/Java safe: no overflow
```

### NeetCode Problem: Binary Search

**Problem:** Search sorted array for target. Return index or -1.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### NeetCode Problem: Search a 2D Matrix

**Problem:** m×n matrix where each row is sorted and first element of each row > last element of previous row. Search for target.

```
Treat matrix as a sorted 1D array of length m*n.
Map 1D index to 2D: row = idx // n, col = idx % n
```

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

### NeetCode Problem: Koko Eating Bananas

**Problem:** Koko must eat all bananas in h hours. Piles of bananas. What is minimum eating speed k?

```
Binary search on ANSWER.
Condition: can Koko eat everything at speed k in ≤ h hours?
  Total hours = sum(ceil(pile/k) for pile in piles)
  = sum((pile + k - 1) // k)

Monotone: if she CAN eat at speed k, she CAN eat at speed k+1.
Find minimum k where condition is True.
lo = 1 (minimum speed)
hi = max(piles) (eat the biggest pile in 1 hour)
```

```python
import math

def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)

    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum(math.ceil(p / mid) for p in piles)
        if hours <= h:
            hi = mid    # mid might be optimal, don't exclude
        else:
            lo = mid + 1

    return lo
```

### NeetCode Problem: Find Minimum in Rotated Sorted Array

**Problem:** Array was sorted then rotated. Find minimum. O(log n).

```
Normal sorted: [1,2,3,4,5]     → min at index 0
Rotated:       [4,5,6,7,0,1,2] → min somewhere in the middle

Key observation: minimum is at the start of the "unsorted" portion.
If nums[mid] > nums[right]: min is in RIGHT half (mid is in larger portion)
If nums[mid] < nums[right]: min is in LEFT half including mid (mid might be min)

[4,5,6,7,0,1,2], lo=0, hi=6
  mid=3, nums[3]=7 > nums[6]=2 → min in right: lo=4
  lo=4,hi=6, mid=5, nums[5]=1 < nums[6]=2 → min in left incl mid: hi=5
  lo=4,hi=5, mid=4, nums[4]=0 < nums[5]=1 → hi=4
  lo=hi=4, return nums[4]=0 ✓
```

```python
def findMin(nums):
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1   # min is in right half
        else:
            hi = mid       # mid might be the min

    return nums[lo]
```

### NeetCode Problem: Search in Rotated Sorted Array

**Problem:** Find target in rotated sorted array (no duplicates).

```
One half is always sorted. Determine which half, then decide which to search.

If nums[lo] <= nums[mid]: left half is sorted.
  If target in [nums[lo], nums[mid]]: search left.
  Else: search right.
Else: right half is sorted.
  If target in [nums[mid], nums[hi]]: search right.
  Else: search left.
```

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1
```

### NeetCode Problem: Time Based Key-Value Store

**Problem:** Set key with timestamp; get key at latest timestamp ≤ given t.

```python
from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)  # key → [(timestamp, value)]

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))
        # Timestamps always increase per key — list is always sorted

    def get(self, key, timestamp):
        pairs = self.store[key]
        # Binary search: find rightmost timestamp ≤ given timestamp
        lo, hi = 0, len(pairs) - 1
        result = ""
        while lo <= hi:
            mid = (lo + hi) // 2
            if pairs[mid][0] <= timestamp:
                result = pairs[mid][1]
                lo = mid + 1
            else:
                hi = mid - 1
        return result
```

### NeetCode Problem: Median of Two Sorted Arrays

**Problem:** Find median of two sorted arrays. Must be O(log(m+n)).

```
This is hard. Key insight: binary search on the PARTITION POINT.

Total elements: m + n. Left half should have (m+n)//2 elements.
Partition array1 at i: elements[0..i-1] in left, elements[i..m-1] in right.
Partition array2 at j: (m+n)//2 - i elements from array2 in left.

Valid partition: max(left1, left2) ≤ min(right1, right2)

Binary search on i (smaller array). Adjust based on:
  max_left1 > min_right2: i too large → hi = i - 1
  max_left2 > min_right1: i too small → lo = i + 1
  otherwise: valid → compute median
```

```python
def findMedianSortedArrays(nums1, nums2):
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A  # ensure A is smaller
    m, n = len(A), len(B)
    total = m + n
    half = total // 2

    lo, hi = 0, m
    while True:
        i = (lo + hi) // 2       # partition point in A
        j = half - i              # partition point in B

        # Values around partition (use -inf/+inf for boundaries)
        A_left  = A[i-1] if i > 0 else float('-inf')
        A_right = A[i]   if i < m else float('inf')
        B_left  = B[j-1] if j > 0 else float('-inf')
        B_right = B[j]   if j < n else float('inf')

        if A_left <= B_right and B_left <= A_right:
            # Valid partition found
            if total % 2:
                return min(A_right, B_right)  # odd total: lower middle
            return (max(A_left, B_left) + min(A_right, B_right)) / 2
        elif A_left > B_right:
            hi = i - 1
        else:
            lo = i + 1
```

---

## Chapter 10: Trees

### 10.1 The Foundation — Recursive Thinking

Almost every tree problem is solved with recursion. The key: **define what your function returns, and trust the recursion**.

```
Pattern: f(node) = combine(f(node.left), f(node.right), node.val)

For each recursive function, ask:
  What do I return? (depth, sum, is-valid, list of nodes, etc.)
  What is the base case? (node is None → return 0/True/[]/None)
  How do I combine left and right results?
```

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Traversals — DFS

```python
# Inorder: Left → Node → Right
# → produces sorted output for BST
def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Preorder: Node → Left → Right
# → used to clone/serialize tree
def preorder(root):
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Postorder: Left → Right → Node
# → used to delete tree, evaluate expressions
def postorder(root):
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# Iterative inorder (interview-friendly, no recursion)
def inorder_iterative(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:             # go as far left as possible
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()      # process node
        result.append(curr.val)
        curr = curr.right       # move to right subtree
    return result
```

### BFS — Level Order Traversal

```python
from collections import deque

def levelOrder(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):   # process exactly one level
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### NeetCode Problem: Invert Binary Tree

**Problem:** Invert (mirror) a binary tree.

```
Recursive: swap left and right children, then invert each subtree.
```

```python
def invertTree(root):
    if not root: return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

### NeetCode Problem: Maximum Depth of Binary Tree

```python
def maxDepth(root):
    if not root: return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

# Iterative BFS
def maxDepth(root):
    if not root: return 0
    depth = 0
    queue = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
    return depth
```

### NeetCode Problem: Diameter of Binary Tree

**Problem:** Length of longest path between any two nodes (may not pass through root).

```
For each node, the diameter through that node = leftDepth + rightDepth.
Compute depth bottom-up, update global max diameter.
```

```python
def diameterOfBinaryTree(root):
    self_diameter = [0]  # use list to modify in closure

    def depth(node):
        if not node: return 0
        left  = depth(node.left)
        right = depth(node.right)
        self_diameter[0] = max(self_diameter[0], left + right)
        return 1 + max(left, right)

    depth(root)
    return self_diameter[0]
```

### NeetCode Problem: Balanced Binary Tree

**Problem:** Determine if tree is height-balanced (depth of subtrees differ by ≤ 1 at every node).

```
Single DFS: return -1 if unbalanced, else return height.
-1 propagates upward.
```

```python
def isBalanced(root):
    def height(node):
        if not node: return 0
        lh = height(node.left)
        rh = height(node.right)
        if lh == -1 or rh == -1 or abs(lh - rh) > 1:
            return -1   # unbalanced signal
        return 1 + max(lh, rh)

    return height(root) != -1
```

### NeetCode Problem: Same Tree

```python
def isSameTree(p, q):
    if not p and not q: return True
    if not p or not q: return False
    if p.val != q.val: return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### NeetCode Problem: Subtree of Another Tree

**Problem:** Is tree s a subtree of tree t?

```
At each node of t, check if the subtree rooted there equals s.
```

```python
def isSubtree(root, subRoot):
    if not root: return False
    if isSameTree(root, subRoot): return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
```

### NeetCode Problem: Lowest Common Ancestor of BST

**Problem:** Find LCA of nodes p and q in a BST.

```
BST property: left subtree < node < right subtree.
LCA = first node where p and q are on different sides (or one equals node).

If both p,q < node → LCA in left subtree.
If both p,q > node → LCA in right subtree.
Else → current node is LCA.
```

```python
def lowestCommonAncestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

### NeetCode Problem: Binary Tree Level Order Traversal

```python
def levelOrder(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### NeetCode Problem: Binary Tree Right Side View

**Problem:** Return values of rightmost nodes at each level.

```
Level order traversal; take the last element of each level.
```

```python
def rightSideView(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        for i in range(len(queue)):
            node = queue.popleft()
            if i == len(queue):  # last node of this level (after popleft, queue shrank)
                result.append(node.val)  # this doesn't work...

# Correct:
def rightSideView(root):
    result = []
    queue = deque([root]) if root else deque()
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                result.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
    return result
```

### NeetCode Problem: Count Good Nodes in Binary Tree

**Problem:** Node x is "good" if no node on path from root to x has value > x.

```
DFS, pass max value seen so far on the path.
Node is good if node.val >= max_so_far.
```

```python
def goodNodes(root):
    def dfs(node, max_so_far):
        if not node: return 0
        good = 1 if node.val >= max_so_far else 0
        new_max = max(max_so_far, node.val)
        return good + dfs(node.left, new_max) + dfs(node.right, new_max)

    return dfs(root, float('-inf'))
```

### NeetCode Problem: Validate Binary Search Tree

**Problem:** Validate BST (each node must satisfy strict bounds from ancestors).

```
DFS with bounds: each node must be in (lower, upper) exclusive.
Root: (-∞, +∞)
Left child: (lower, node.val)
Right child: (node.val, upper)
```

```python
def isValidBST(root):
    def validate(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return (validate(node.left, lo, node.val) and
                validate(node.right, node.val, hi))

    return validate(root, float('-inf'), float('inf'))
```

### NeetCode Problem: Kth Smallest Element in BST

**Problem:** Find kth smallest element in BST.

```
Inorder traversal gives elements in sorted order.
Return kth element.
```

```python
def kthSmallest(root, k):
    stack = []
    curr = root
    count = 0
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right
```

### NeetCode Problem: Construct Binary Tree from Preorder and Inorder Traversal

**Problem:** Reconstruct binary tree from preorder and inorder arrays.

```
Key insight:
  Preorder: first element is the ROOT.
  Inorder: root's position splits array into LEFT and RIGHT subtrees.

preorder = [3,9,20,15,7]
inorder  = [9,3,15,20,7]

Root = 3 (preorder[0])
In inorder: 3 is at index 1 → left has 1 node, right has 2 nodes.
Left: preorder[1:2]=[9], inorder[:1]=[9]  → subtree rooted at 9
Right: preorder[2:]=[20,15,7], inorder[2:]=[15,20,7] → subtree rooted at 20
```

```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)

    root.left  = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:],  inorder[mid+1:])
    return root

# Optimized with HashMap for O(1) index lookup:
def buildTree(preorder, inorder):
    idx_map = {val: i for i, val in enumerate(inorder)}
    self_pre_idx = [0]

    def build(lo, hi):
        if lo > hi: return None
        val = preorder[self_pre_idx[0]]
        self_pre_idx[0] += 1
        node = TreeNode(val)
        mid = idx_map[val]
        node.left  = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)
```

### NeetCode Problem: Binary Tree Maximum Path Sum

**Problem:** Find maximum sum of any path in the tree (path can start and end at any nodes).

```
For each node, compute:
  gain_from_left  = max(0, maxGain(left))   # take left if positive
  gain_from_right = max(0, maxGain(right))  # take right if positive
  path through node = node.val + gain_from_left + gain_from_right
  Update global max with this value.
  Return node.val + max(gain_from_left, gain_from_right) for parent's use
  (a path going "up" can only choose one direction)
```

```python
def maxPathSum(root):
    max_sum = [float('-inf')]

    def max_gain(node):
        if not node: return 0
        left_gain  = max(0, max_gain(node.left))
        right_gain = max(0, max_gain(node.right))
        # Path through this node
        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)
        # Return best single-direction gain to parent
        return node.val + max(left_gain, right_gain)

    max_gain(root)
    return max_sum[0]
```

### NeetCode Problem: Serialize and Deserialize Binary Tree

**Problem:** Encode tree to string and decode back.

```
Preorder DFS with null markers.
Serialize: preorder, write "N" for null.
Deserialize: read preorder, build tree recursively.
```

```python
def serialize(root):
    result = []
    def dfs(node):
        if not node:
            result.append('N')
            return
        result.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ','.join(result)

def deserialize(data):
    vals = iter(data.split(','))
    def dfs():
        val = next(vals)
        if val == 'N': return None
        node = TreeNode(int(val))
        node.left  = dfs()
        node.right = dfs()
        return node
    return dfs()
```

---

## Chapter 11: Tries

### 11.1 What is a Trie and Why Use It

A **Trie** (prefix tree) stores strings as paths from root to leaf. Each edge represents one character.

```
Storing: ["apple", "app", "api", "banana"]

         root
        /    \
       a      b
       |      |
       p      a
      / \     |
     p   i    n
     |   |    |
     l   (end) a
     |        |
     e        n
     |        |
   (end)      a
             (end)

Key operations:
  insert(word): walk path, create nodes as needed, mark end
  search(word): walk path, return True if end marker at last node
  startsWith(prefix): walk path, return True if prefix exists
  
Why trie instead of HashSet?
  1. Prefix queries: "find all words starting with 'ap'" — O(k) where k=prefix length
  2. Autocomplete: immediately obvious from trie structure
  3. Space-efficient when many words share prefixes
```

```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char → TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
```

### NeetCode Problem: Design Add and Search Words Data Structure

**Problem:** Add words; search where '.' matches any character.

```
DFS with backtracking when '.' is encountered.
```

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return node.is_end
            c = word[i]
            if c == '.':
                # Try all children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                if c not in node.children:
                    return False
                return dfs(node.children[c], i + 1)

        return dfs(self.root, 0)
```

### NeetCode Problem: Word Search II

**Problem:** Given board of characters and list of words, find all words that can be formed by adjacent cells (no reuse).

```
Approach: Build trie from words. DFS from each cell, follow trie.
When we reach a trie node with is_end, we found a word.
Prune: if current char not in trie node's children → stop DFS.
Optimization: remove found words from trie to avoid duplicates.
```

```python
def findWords(board, words):
    root = TrieNode()
    for word in words:
        node = root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.word = word   # store word at end node
        node.is_end = True

    ROWS, COLS = len(board), len(board[0])
    result = set()

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]
        if next_node.is_end:
            result.add(next_node.word)

        board[r][c] = '#'   # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = ch    # restore

    for r in range(ROWS):
        for c in range(COLS):
            dfs(r, c, root)

    return list(result)
```

---

## Chapter 12: Heap / Priority Queue

### 12.1 Heap Theory

A **binary heap** is a complete binary tree satisfying the heap property:
- **Min-heap**: parent ≤ both children (root = minimum element)
- **Max-heap**: parent ≥ both children (root = maximum element)

```
Heap operations:
  push(x): add at end, bubble up (swap with parent if violates property)
  pop(): remove root, put last element at root, bubble down
  peek(): return root without removing

  push: O(log n) — bubble up at most height=log n levels
  pop:  O(log n) — bubble down
  peek: O(1)     — just look at root

Python heapq is a MIN-HEAP.
For max-heap: negate values → push(-x), -pop()
```

```python
import heapq

# Min-heap operations
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
print(heap[0])           # peek: 1 (minimum)
print(heapq.heappop(heap))  # pop: 1

# Max-heap: negate values
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
max_val = -heapq.heappop(max_heap)  # 5

# Heapify: O(n) — more efficient than n individual pushes
nums = [3, 1, 4, 1, 5, 9]
heapq.heapify(nums)  # in-place
```

### 12.2 When to Use a Heap

```
Top K elements         → heap of size K
K-th largest/smallest  → heap
Merge K sorted lists   → heap
Continuous median      → two heaps (max-heap left, min-heap right)
Dijkstra               → min-heap
```

### NeetCode Problem: Kth Largest Element in a Stream

**Problem:** Design class that finds kth largest element in stream.

```
Maintain min-heap of size k.
The k-th largest = heap[0] (minimum of the k largest elements seen).
When new element arrives: push, then pop if size > k.
```

```python
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

### NeetCode Problem: Last Stone Weight

**Problem:** Pick heaviest two stones, smash them. Repeat. Return final weight (or 0).

```
Use max-heap. Each round: pop two heaviest, smash, push remainder if nonzero.
```

```python
def lastStoneWeight(stones):
    heap = [-s for s in stones]  # max-heap via negation
    heapq.heapify(heap)

    while len(heap) > 1:
        a = -heapq.heappop(heap)  # heaviest
        b = -heapq.heappop(heap)  # second heaviest
        if a != b:
            heapq.heappush(heap, -(a - b))

    return -heap[0] if heap else 0
```

### NeetCode Problem: K Closest Points to Origin

**Problem:** Return k closest points to origin from list of points.

```
Option 1: Sort by distance — O(n log n)
Option 2: Max-heap of size k — O(n log k)
  Maintain heap of k closest points.
  For each new point: if closer than heap max, replace.
Option 3: Quickselect — O(n) average (not needed for interview)
```

```python
def kClosest(points, k):
    # Max-heap of size k (negate distances for max-heap behavior)
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)  # negate for max-heap
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```

### NeetCode Problem: Kth Largest Element in an Array

**Problem:** Find kth largest without full sorting.

```
Min-heap of size k:
  Maintain the k largest elements seen so far.
  Heap root = k-th largest.

Or: partial sort with heapq.nlargest (O(n log k))
```

```python
def findKthLargest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

# One-liner: heapq.nlargest(k, nums)[-1]
```

### NeetCode Problem: Task Scheduler

**Problem:** CPU schedule tasks with cooldown n between same tasks. Minimum intervals needed.

```
Greedy: always execute most frequent remaining task.
Use max-heap + queue for cooling tasks.

Each round (CPU cycle):
  1. Pop most frequent task from heap, execute it.
  2. Add to cooldown queue: (next_available_time, count-1).
  3. When cooldown expires, push back to heap.
  4. If heap empty and queue not empty: idle.
```

```python
from collections import Counter, deque

def leastInterval(tasks, n):
    count = Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)

    time = 0
    cooldown_q = deque()  # (available_at_time, remaining_count)

    while max_heap or cooldown_q:
        time += 1

        if max_heap:
            remaining = heapq.heappop(max_heap) + 1  # increment (negated, so decrement)
            if remaining < 0:
                cooldown_q.append((time + n, remaining))
        else:
            # Idle: skip to when first task becomes available
            if cooldown_q:
                time = cooldown_q[0][0] - 1  # will be +1 at start of next iteration

        # Check cooldown expiry
        if cooldown_q and cooldown_q[0][0] == time:
            _, remaining = cooldown_q.popleft()
            heapq.heappush(max_heap, remaining)

    return time
```

### NeetCode Problem: Design Twitter

**Problem:** Implement Twitter with postTweet, getNewsFeed (10 most recent), follow, unfollow.

```
Each user has a list of tweets with timestamps.
getNewsFeed: merge k sorted lists (user's own tweets + followees' tweets)
→ use a min-heap to get 10 most recent.
```

```python
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)       # userId → [(time, tweetId)]
        self.following = defaultdict(set)     # userId → {followeeId}

    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId):
        # Gather tweets from user and followees
        heap = []
        sources = [userId] + list(self.following[userId])

        for uid in sources:
            tweets = self.tweets[uid]
            if tweets:
                # Start with the most recent tweet
                idx = len(tweets) - 1
                t, tweet_id = tweets[idx]
                heapq.heappush(heap, (-t, tweet_id, uid, idx - 1))

        result = []
        while heap and len(result) < 10:
            neg_t, tweet_id, uid, next_idx = heapq.heappop(heap)
            result.append(tweet_id)
            if next_idx >= 0:
                t, tid = self.tweets[uid][next_idx]
                heapq.heappush(heap, (-t, tid, uid, next_idx - 1))

        return result

    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

### NeetCode Problem: Find Median from Data Stream

**Problem:** Continuously find median of a growing data stream.

```
Two heaps: max-heap (left half) and min-heap (right half).
Invariant:
  max_heap stores lower half, min_heap stores upper half.
  |max_heap| == |min_heap| or |max_heap| == |min_heap| + 1

  median = max_heap[0] if odd total
         = (max_heap[0] + min_heap[0]) / 2 if even

Add number:
  1. Push to max_heap (may violate "lower half" invariant)
  2. Rebalance: if max_heap top > min_heap top, move max_heap top to min_heap
  3. Size balance: if min_heap has more, move min_heap top to max_heap
```

```python
class MedianFinder:
    def __init__(self):
        self.max_heap = []  # lower half (negated for max-heap)
        self.min_heap = []  # upper half (min-heap)

    def addNum(self, num):
        heapq.heappush(self.max_heap, -num)

        # Ensure max_heap top ≤ min_heap top
        if self.min_heap and -self.max_heap[0] > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        # Balance sizes: max_heap can have at most 1 more
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2
```

---

## Chapter 13: Backtracking

### 13.1 The Pattern — Exhaustive Search with Pruning

Backtracking explores all possible solutions by building a solution incrementally. When a partial solution can't lead to a valid complete solution, **backtrack** (undo the last choice) and try a different path.

```
def backtrack(state, choices):
    if is_complete(state):
        add state to results
        return
    for choice in choices:
        if is_valid(state, choice):
            make_choice(state, choice)      # modify state
            backtrack(state, next_choices)  # recurse
            undo_choice(state, choice)      # restore state (backtrack)

Time complexity: typically O(branching_factor ^ depth) — exponential
But pruning can make it much faster in practice.
```

### NeetCode Problem: Subsets

**Problem:** Return all subsets (power set) of distinct integers.

```
Decision tree: for each element, include or exclude.
n elements → 2^n subsets.

At each level, two choices: include or skip current element.
```

```python
def subsets(nums):
    result = []

    def backtrack(start, current):
        result.append(current[:])  # add copy of current subset
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()          # backtrack

    backtrack(0, [])
    return result
```

### NeetCode Problem: Combination Sum

**Problem:** Find all combinations summing to target. Can reuse elements.

```
Key: can reuse elements (so don't advance start index when recursing).
Prune: if current sum > target, stop.
```

```python
def combinationSum(candidates, target):
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        if remaining < 0:
            return

        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])  # i (not i+1) = reuse
            current.pop()

    backtrack(0, [], target)
    return result
```

### NeetCode Problem: Combination Sum II

**Problem:** Candidates have duplicates. Each candidate used once. No duplicate combinations.

```
Sort first. Skip duplicate candidates at the same recursion level.
(Can use same element in child levels, but not sibling levels.)
```

```python
def combinationSum2(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            # Skip duplicates at the SAME recursion level
            if i > start and candidates[i] == candidates[i-1]:
                continue
            current.append(candidates[i])
            backtrack(i + 1, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result
```

### NeetCode Problem: Permutations

**Problem:** Return all permutations of distinct integers.

```
Unlike combinations, ORDER matters.
At each step, choose any unused element.
Track used elements with a set or boolean array.
```

```python
def permute(nums):
    result = []

    def backtrack(current, used):
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i, n in enumerate(nums):
            if used[i]: continue
            used[i] = True
            current.append(n)
            backtrack(current, used)
            current.pop()
            used[i] = False

    backtrack([], [False] * len(nums))
    return result

# Cleaner version using set:
def permute(nums):
    result = []
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    backtrack([], nums)
    return result
```

### NeetCode Problem: Subsets II

**Problem:** Array may contain duplicates. Return all distinct subsets.

```
Sort + skip duplicates at same level.
```

```python
def subsetsWithDup(nums):
    nums.sort()
    result = []

    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue  # skip duplicate at same level
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### NeetCode Problem: Word Search

**Problem:** Find if word exists in grid of characters. Can use adjacent cells, no reuse.

```
DFS backtracking: explore from each starting cell.
Mark cell as visited during DFS (e.g., replace with '#').
Restore when backtracking.
```

```python
def exist(board, word):
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word): return True
        if (r < 0 or r >= ROWS or c < 0 or c >= COLS or
                board[r][c] != word[idx]):
            return False

        board[r][c] = '#'  # mark visited
        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        board[r][c] = word[idx]  # restore
        return found

    for r in range(ROWS):
        for c in range(COLS):
            if dfs(r, c, 0):
                return True
    return False
```

### NeetCode Problem: Palindrome Partitioning

**Problem:** Partition string so every substring is a palindrome. Return all such partitions.

```
At each position, try every valid palindrome starting here.
If it's a palindrome, recurse on the rest.
```

```python
def partition(s):
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start + 1, len(s) + 1):
            substr = s[start:end]
            if is_palindrome(substr):
                current.append(substr)
                backtrack(end, current)
                current.pop()

    backtrack(0, [])
    return result
```

### NeetCode Problem: Letter Combinations of a Phone Number

**Problem:** Return all possible letter combinations from phone digits.

```python
def letterCombinations(digits):
    if not digits: return []

    phone = {'2':'abc','3':'def','4':'ghi','5':'jkl',
             '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []

    def backtrack(idx, current):
        if idx == len(digits):
            result.append(''.join(current))
            return
        for c in phone[digits[idx]]:
            current.append(c)
            backtrack(idx + 1, current)
            current.pop()

    backtrack(0, [])
    return result
```

### NeetCode Problem: N-Queens

**Problem:** Place n queens on n×n chessboard. No two queens attack each other.

```
Queens attack same row, column, or diagonal.
Place one queen per row. Track:
  - cols: set of used columns
  - posDiag: set of (r+c) — same positive diagonal
  - negDiag: set of (r-c) — same negative diagonal
```

```python
def solveNQueens(n):
    cols = set()
    pos_diag = set()  # r + c
    neg_diag = set()  # r - c
    board = []
    result = []

    def backtrack(r):
        if r == n:
            result.append([''.join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r+c) in pos_diag or (r-c) in neg_diag:
                continue
            cols.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board.append(['Q' if i == c else '.' for i in range(n)])
            backtrack(r + 1)
            cols.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board.pop()

    backtrack(0)
    return result
```

---

# PART IV — GRAPHS

---

## Chapter 14: Graph Theory & Representations

### 14.1 Graph Fundamentals

```
A graph G = (V, E): V = vertices (nodes), E = edges (connections)

Types:
  Undirected: edges have no direction (A—B means A↔B)
  Directed (Digraph): edges have direction (A→B ≠ B→A)
  Weighted: edges have values (distances, costs)
  Unweighted: all edges equal

Properties:
  Connected: path exists between every pair of vertices
  Cyclic: contains at least one cycle
  Acyclic: no cycles (trees are connected acyclic graphs)
  DAG: Directed Acyclic Graph (topological sort applies here)

Special graphs:
  Tree: connected acyclic undirected graph (n nodes, n-1 edges)
  Forest: collection of trees
  Bipartite: can 2-color vertices so no edge connects same-color vertices
```

### 14.2 Representations

```python
# ① Adjacency List — most common for sparse graphs
# Space: O(V + E)  Access edge (u,v): O(degree(u))
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 4],
    3: [1],
    4: [2]
}

# From edge list:
from collections import defaultdict
def build_graph(n, edges, directed=False):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph

# ② Adjacency Matrix — for dense graphs or when O(1) edge query needed
# Space: O(V²)   Access edge (u,v): O(1)
matrix = [[0]*n for _ in range(n)]
matrix[0][1] = 1  # edge 0→1

# ③ Edge List — simplest, good for Kruskal's algorithm
edges = [(0,1), (0,2), (1,3), (2,4)]
```

---

## Chapter 15: Graph BFS & DFS

### 15.1 DFS — Depth-First Search

```
DFS explores as deep as possible before backtracking.
Uses: connected components, cycle detection, topological sort, DFS tree

Time: O(V + E)  Space: O(V) for visited + O(V) call stack
```

```python
# DFS — recursive
def dfs(graph, node, visited):
    if node in visited: return
    visited.add(node)
    print(node)
    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)

# DFS — iterative (using explicit stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node)
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### 15.2 BFS — Breadth-First Search

```
BFS explores level by level.
Uses: shortest path (unweighted), connected components, bipartite check

Time: O(V + E)  Space: O(V) for visited + queue

KEY PROPERTY: BFS gives SHORTEST PATH in unweighted graphs.
Why? Level k = all nodes exactly k steps from source.
We reach each node for the first time via the shortest path.
```

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# BFS with distance tracking
def bfs_distance(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist
```

### NeetCode Problem: Number of Islands

**Problem:** Count connected components of '1' in grid.

```
For each unvisited '1': BFS/DFS to mark the entire island as visited, increment count.
```

```python
def numIslands(grid):
    if not grid: return 0
    ROWS, COLS = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if (r < 0 or r >= ROWS or c < 0 or c >= COLS or grid[r][c] != '1'):
            return
        grid[r][c] = '0'   # mark visited by sinking the island
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == '1':
                dfs(r, c)
                islands += 1

    return islands
```

### NeetCode Problem: Max Area of Island

**Problem:** Return maximum area of island.

```python
def maxAreaOfIsland(grid):
    ROWS, COLS = len(grid), len(grid[0])

    def dfs(r, c):
        if (r < 0 or r >= ROWS or c < 0 or c >= COLS or grid[r][c] == 0):
            return 0
        grid[r][c] = 0
        return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)

    return max(dfs(r, c)
               for r in range(ROWS)
               for c in range(COLS)
               if grid[r][c] == 1)
```

### NeetCode Problem: Clone Graph

**Problem:** Deep clone a connected undirected graph.

```python
def cloneGraph(node):
    if not node: return None
    old_to_new = {}

    def dfs(node):
        if node in old_to_new:
            return old_to_new[node]
        clone = Node(node.val)
        old_to_new[node] = clone
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        return clone

    return dfs(node)
```

### NeetCode Problem: Walls and Gates

**Problem:** Grid with -1 (wall), 0 (gate), INF (empty room). Fill each room with distance to nearest gate.

```
Multi-source BFS from ALL gates simultaneously.
This is more efficient than BFS from each room individually.
The first time BFS reaches a room = shortest distance to any gate.
```

```python
def wallsAndGates(rooms):
    ROWS, COLS = len(rooms), len(rooms[0])
    INF = float('inf')
    queue = deque()

    # Start BFS from all gates
    for r in range(ROWS):
        for c in range(COLS):
            if rooms[r][c] == 0:
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

### NeetCode Problem: Rotting Oranges

**Problem:** Grid: 0=empty, 1=fresh, 2=rotten. Each minute, rotten oranges infect adjacent fresh. Minutes until all rotten (-1 if impossible).

```
Multi-source BFS from all initially rotten oranges.
```

```python
def orangesRotting(grid):
    ROWS, COLS = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    time = 0

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh += 1

    while queue and fresh > 0:
        r, c, t = queue.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                time = t + 1
                queue.append((nr, nc, t+1))

    return time if fresh == 0 else -1
```

### NeetCode Problem: Pacific Atlantic Water Flow

**Problem:** Water can flow to adjacent cells with ≤ height. Which cells can flow to both Pacific (top/left) and Atlantic (bottom/right)?

```
Reverse thinking: instead of "can water flow from (r,c) to ocean",
ask "which cells can be reached FROM the ocean going uphill?"

BFS/DFS from Pacific border cells (height constraint reversed: go to >= height).
BFS/DFS from Atlantic border cells.
Intersection = answer.
```

```python
def pacificAtlantic(heights):
    ROWS, COLS = len(heights), len(heights[0])

    def bfs(starts):
        visited = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r+dr, c+dc
                if (0 <= nr < ROWS and 0 <= nc < COLS and
                        (nr,nc) not in visited and
                        heights[nr][nc] >= heights[r][c]):
                    visited.add((nr,nc))
                    queue.append((nr,nc))
        return visited

    pacific_starts = [(0,c) for c in range(COLS)] + [(r,0) for r in range(ROWS)]
    atlantic_starts = [(ROWS-1,c) for c in range(COLS)] + [(r,COLS-1) for r in range(ROWS)]

    pacific  = bfs(pacific_starts)
    atlantic = bfs(atlantic_starts)

    return list(pacific & atlantic)
```

### NeetCode Problem: Surrounded Regions

**Problem:** 4-connected regions of 'O' captured by 'X' — except those on border. Flip captured 'O' to 'X'.

```
Reverse: mark all 'O' connected to border as safe (change to 'T').
Flip remaining 'O' (captured) to 'X'.
Restore 'T' back to 'O'.
```

```python
def solve(board):
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= ROWS or c < 0 or c >= COLS or board[r][c] != 'O': return
        board[r][c] = 'T'
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)

    # Mark safe 'O' (connected to border)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 'O' and (r in [0, ROWS-1] or c in [0, COLS-1]):
                dfs(r, c)

    # Flip: 'O' → 'X' (captured), 'T' → 'O' (safe)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 'O':   board[r][c] = 'X'
            elif board[r][c] == 'T': board[r][c] = 'O'
```

### NeetCode Problem: Course Schedule (Cycle Detection)

**Problem:** n courses, prerequisites pairs. Can you finish all courses?

```
Model as directed graph. Can finish all courses iff graph has NO CYCLE.
A cycle means circular dependency → impossible.

DFS cycle detection:
  For each node, DFS and track "currently in recursion stack" (visiting) and "fully processed" (visited).
  If DFS reaches a node that is "visiting" → cycle detected.
```

```python
def canFinish(numCourses, prerequisites):
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    # 0=unvisited, 1=visiting (in current DFS path), 2=done (safe)
    state = [0] * numCourses

    def has_cycle(node):
        if state[node] == 1: return True   # back edge → cycle
        if state[node] == 2: return False  # already processed, safe

        state[node] = 1  # mark as visiting
        for neighbor in graph[node]:
            if has_cycle(neighbor): return True
        state[node] = 2  # mark as done
        return False

    return not any(has_cycle(i) for i in range(numCourses))
```

### NeetCode Problem: Course Schedule II (Topological Sort)

**Problem:** Return valid course order (topological sort).

```
Topological sort: linear ordering of vertices such that for every directed edge u→v,
u appears before v.
Only possible if graph is a DAG (no cycles).

Approach: DFS post-order = reverse topological order
(add node to result AFTER all its dependencies are processed)
```

```python
def findOrder(numCourses, prerequisites):
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    state = [0] * numCourses
    order = []

    def dfs(node):
        if state[node] == 1: return False   # cycle
        if state[node] == 2: return True    # already processed
        state[node] = 1
        for neighbor in graph[node]:
            if not dfs(neighbor): return False
        state[node] = 2
        order.append(node)  # post-order: add after processing all dependencies
        return True

    for i in range(numCourses):
        if not dfs(i): return []

    return order[::-1]  # reverse post-order = topological order

# Alternative: Kahn's Algorithm (BFS-based topological sort)
def findOrder_kahn(numCourses, prerequisites):
    in_degree = [0] * numCourses
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == numCourses else []
```

---

## Chapter 16: Advanced Graphs

### NeetCode Problem: Redundant Connection

**Problem:** Find the edge that creates a cycle in an undirected graph.

```
Union-Find (Disjoint Set Union): Efficiently tracks connected components.

union(u, v): merge components of u and v.
find(u): return representative of u's component.

If two nodes already have same representative → adding edge creates cycle → this is the redundant edge.
```

```python
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))
    rank   = [0] * (len(edges) + 1)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  # path compression
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False   # already connected → redundant edge
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px             # union by rank
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]
```

### NeetCode Problem: Number of Connected Components in Undirected Graph

```python
def countComponents(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return 0
        parent[px] = py
        return 1

    return n - sum(union(u, v) for u, v in edges)
```

### NeetCode Problem: Graph Valid Tree

**Problem:** Given n nodes and edges, determine if they form a valid tree.

```
A tree is a connected graph with n-1 edges (and therefore no cycles).
Conditions:
  1. len(edges) == n - 1  (else definitely not a tree)
  2. All nodes connected (one component)
```

```python
def validTree(n, edges):
    if len(edges) != n - 1: return False

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    def dfs(node):
        if node in visited: return
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor)

    dfs(0)
    return len(visited) == n
```

### NeetCode Problem: Network Delay Time (Dijkstra)

**Problem:** Weighted directed graph. Send signal from k. Time until all nodes receive signal? (shortest path from k to all nodes)

```
Dijkstra's Algorithm: shortest path from source in weighted graph (non-negative weights).
Uses min-heap: always process nearest unvisited node.

Time: O((V + E) log V)

Algorithm:
  dist[k] = 0; all others = infinity
  Push (0, k) to heap
  While heap not empty:
    Pop (dist, node) — cheapest unvisited
    If visited: skip
    Mark visited
    For each neighbor:
      If dist + weight < dist[neighbor]:
        Update dist[neighbor]
        Push to heap
```

```python
def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n+1)}
    dist[k] = 0
    heap = [(0, k)]   # (distance, node)

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]: continue  # stale entry

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1
```

### NeetCode Problem: Swim in Rising Water

**Problem:** Grid where cell value = elevation. Rain rises: at time t, you can swim where elevation ≤ t. Min time to swim from top-left to bottom-right.

```
Binary search on time + BFS check? Or Dijkstra!
Treat elevation as "edge weight". Find path from (0,0) to (n-1,n-1) minimizing maximum elevation.
Dijkstra: dist[node] = minimum possible time (max elevation on path from start).
```

```python
def swimInWater(grid):
    n = len(grid)
    dist = [[float('inf')] * n for _ in range(n)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]

    while heap:
        t, r, c = heapq.heappop(heap)
        if t > dist[r][c]: continue
        if r == n-1 and c == n-1: return t

        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n:
                new_t = max(t, grid[nr][nc])  # time = max elevation on path
                if new_t < dist[nr][nc]:
                    dist[nr][nc] = new_t
                    heapq.heappush(heap, (new_t, nr, nc))
```

### NeetCode Problem: Alien Dictionary

**Problem:** Given sorted list of words from alien language, find order of alien alphabet.

```
Build directed graph: if word1[i] != word2[i], then word1[i] → word2[i] in alphabetical order.
Topological sort gives the alphabet order.
Edge case: if word1 is a prefix of word2 but comes AFTER → invalid.
```

```python
def alienOrder(words):
    # Initialize with all unique characters
    adj = {c: set() for word in words for c in word}

    # Build edges from adjacent pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # invalid: longer word comes first

        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break

    # Topological sort (DFS)
    state = {}  # 'visiting', 'visited'
    result = []

    def dfs(char):
        if char in state:
            return state[char] == 'visited'  # False if still visiting = cycle
        state[char] = 'visiting'
        for neighbor in adj[char]:
            if not dfs(neighbor): return False
        state[char] = 'visited'
        result.append(char)
        return True

    for c in adj:
        if not dfs(c): return ""

    return ''.join(reversed(result))
```

### NeetCode Problem: Cheapest Flights Within K Stops (Bellman-Ford)

**Problem:** Cheapest flight from src to dst with at most k stops.

```
Bellman-Ford: relax all edges repeatedly. Useful when:
  - Negative weights (Dijkstra doesn't work)
  - Bounded number of hops (exactly this problem)

Standard Bellman-Ford relaxes n-1 times.
For "at most k stops" (k+1 edges): relax k+1 times.

Important: use a copy of prices at start of each iteration
to prevent using edges from same iteration (violates hop count).
```

```python
def findCheapestPrice(n, flights, src, dst, k):
    prices = [float('inf')] * n
    prices[src] = 0

    for _ in range(k + 1):  # k stops = k+1 edges
        temp = prices.copy()
        for u, v, w in flights:
            if prices[u] != float('inf') and prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp

    return prices[dst] if prices[dst] != float('inf') else -1
```

### NeetCode Problem: Min Cost to Connect All Points (Prim's / Kruskal's)

**Problem:** Points on 2D plane. Connect all with minimum total Manhattan distance (MST).

```
Minimum Spanning Tree (MST): connect all vertices with minimum total edge weight.

Prim's Algorithm: grows MST one vertex at a time.
  Start from any vertex. Maintain min-heap of (cost, vertex).
  Always add cheapest connection to unvisited vertex.
  O((V+E) log V)
```

```python
def minCostConnectPoints(points):
    n = len(points)
    visited = set()
    heap = [(0, 0)]  # (cost, point_index)
    total = 0

    while len(visited) < n:
        cost, i = heapq.heappop(heap)
        if i in visited: continue
        visited.add(i)
        total += cost

        for j in range(n):
            if j not in visited:
                dist = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
                heapq.heappush(heap, (dist, j))

    return total
```

---

# PART V — DYNAMIC PROGRAMMING

---

## Chapter 17: 1-D Dynamic Programming

### 17.1 DP Philosophy

DP solves problems by:
1. Breaking them into **overlapping subproblems**
2. Solving each subproblem **once** and **caching** the result
3. Building the answer from **bottom up** (tabulation) or **top down** (memoization)

```
Ask: "Can this problem be expressed as f(n) = combine(f(n-1), f(n-2), ...)"?

Two approaches:
  Top-down (memoization): recursive, cache results
  Bottom-up (tabulation): iterative, fill table from base cases up

Top-down is often easier to think about.
Bottom-up is often more space-efficient (no call stack).
```

### NeetCode Problem: Climbing Stairs

**Problem:** n stairs. Can climb 1 or 2 steps. How many ways?

```
f(n) = ways to reach step n
f(1) = 1, f(2) = 2
f(n) = f(n-1) + f(n-2)   ← Fibonacci!
(either come from step n-1 with a 1-step, or from step n-2 with a 2-step)
```

```python
def climbStairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n+1):
        a, b = b, a + b
    return b
```

### NeetCode Problem: Min Cost Climbing Stairs

**Problem:** cost[i] = cost to step on stair i. Can step on 1 or 2 stairs. Min cost to reach top.

```
dp[i] = min cost to reach step i
dp[i] = cost[i] + min(dp[i-1], dp[i-2])
Base: dp[0] = cost[0], dp[1] = cost[1]
Answer: min(dp[n-1], dp[n-2]) (can start from 0 or 1)
```

```python
def minCostClimbingStairs(cost):
    n = len(cost)
    dp = [0] * (n + 1)   # dp[i] = min cost to reach step i
    # dp[0] = dp[1] = 0 (can start from either)
    for i in range(2, n + 1):
        dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])
    return dp[n]
```

### NeetCode Problem: House Robber

**Problem:** Rob houses in a row. Can't rob adjacent houses. Max money.

```
dp[i] = max money from first i houses
dp[i] = max(dp[i-1],           # skip house i
            dp[i-2] + nums[i]) # rob house i + best from i-2
```

```python
def rob(nums):
    if len(nums) == 1: return nums[0]
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2, prev1 = prev1, curr
    return prev1
```

### NeetCode Problem: House Robber II (Circular)

**Problem:** Same but houses are in a circle (first and last adjacent).

```
Can't rob both house 0 and house n-1.
Two cases: rob houses [0..n-2] OR rob houses [1..n-1].
Take max of both.
```

```python
def rob(nums):
    if len(nums) == 1: return nums[0]

    def rob_linear(houses):
        prev2 = prev1 = 0
        for h in houses:
            prev2, prev1 = prev1, max(prev1, prev2 + h)
        return prev1

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

### NeetCode Problem: Longest Palindromic Substring

**Problem:** Find longest substring that is a palindrome.

```
Expand around center:
For each center (character or gap between characters):
  Expand outward while characters match.
  Track longest palindrome found.

O(n²) time, O(1) space.
```

```python
def longestPalindrome(s):
    result = ""

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]

    for i in range(len(s)):
        odd  = expand(i, i)       # odd-length palindrome
        even = expand(i, i+1)     # even-length palindrome
        if len(odd)  > len(result): result = odd
        if len(even) > len(result): result = even

    return result
```

### NeetCode Problem: Palindromic Substrings

**Problem:** Count palindromic substrings.

```python
def countSubstrings(s):
    count = 0

    def expand(left, right):
        nonlocal count
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    for i in range(len(s)):
        expand(i, i)      # odd
        expand(i, i+1)    # even

    return count
```

### NeetCode Problem: Decode Ways

**Problem:** '1'→'A', ..., '26'→'Z'. Count ways to decode a numeric string.

```
dp[i] = number of ways to decode s[0..i-1]
dp[0] = 1 (empty string = 1 way)
dp[1] = 0 if s[0]=='0' else 1

For each i from 2 to n:
  one_digit = s[i-1]
  two_digit = s[i-2:i]
  
  if one_digit != '0': dp[i] += dp[i-1]   (decode single digit)
  if '10' <= two_digit <= '26': dp[i] += dp[i-2]  (decode two digits)
```

```python
def numDecodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0 if s[0] == '0' else 1

    for i in range(2, n + 1):
        one = s[i-1]
        two = s[i-2:i]
        if one != '0':
            dp[i] += dp[i-1]
        if '10' <= two <= '26':
            dp[i] += dp[i-2]

    return dp[n]
```

### NeetCode Problem: Coin Change

**Problem:** Coins of given denominations. Minimum coins to make amount.

```
dp[i] = minimum coins to make amount i
dp[0] = 0
dp[i] = min(dp[i - coin] + 1) for all valid coins

Bottom-up: fill dp[1] through dp[amount].
```

```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### NeetCode Problem: Maximum Product Subarray

**Problem:** Find contiguous subarray with largest product.

```
Trick: track both max AND min products at each position.
Why? A very negative number times a very negative number = large positive.
So min product might become max product when multiplied by a negative.

dp_max[i] = max product ending at i
dp_min[i] = min product ending at i
dp_max[i] = max(nums[i], dp_max[i-1]*nums[i], dp_min[i-1]*nums[i])
dp_min[i] = min(nums[i], dp_max[i-1]*nums[i], dp_min[i-1]*nums[i])
```

```python
def maxProduct(nums):
    result = max(nums)
    cur_max = cur_min = 1

    for n in nums:
        if n == 0:
            cur_max = cur_min = 1
            continue
        temp = cur_max * n
        cur_max = max(n, temp, cur_min * n)
        cur_min = min(n, temp, cur_min * n)
        result = max(result, cur_max)

    return result
```

### NeetCode Problem: Word Break

**Problem:** Can string s be segmented using words from dictionary?

```
dp[i] = can s[0..i-1] be segmented?
dp[0] = True (empty string)
dp[i] = any(dp[j] and s[j:i] in word_set for j in range(i))
```

```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

### NeetCode Problem: Longest Increasing Subsequence (LIS)

**Problem:** Find length of longest strictly increasing subsequence.

```
dp[i] = length of LIS ending at index i
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])
Answer = max(dp)
Time: O(n²)

O(n log n) solution: patience sorting / binary search
Maintain array `tails` where tails[i] = smallest tail of LIS of length i+1.
Binary search to find where current element fits.
```

```python
# O(n²) DP
def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n) patience sorting
def lengthOfLIS(nums):
    tails = []  # tails[i] = smallest tail of LIS of length i+1
    for n in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < n: lo = mid + 1
            else:              hi = mid
        if lo == len(tails): tails.append(n)
        else:                 tails[lo] = n
    return len(tails)
```

---

## Chapter 18: 2-D Dynamic Programming

### NeetCode Problem: Unique Paths

**Problem:** Robot at top-left of m×n grid. Can only move right or down. Count paths to bottom-right.

```
dp[r][c] = number of paths to reach (r,c)
dp[r][c] = dp[r-1][c] + dp[r][c-1]
Base: dp[0][c] = 1 (top row), dp[r][0] = 1 (left column)
```

```python
def uniquePaths(m, n):
    dp = [[1]*n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[m-1][n-1]
```

### NeetCode Problem: Longest Common Subsequence (LCS)

**Problem:** Find length of longest common subsequence of two strings.

```
dp[i][j] = LCS of s1[0..i-1] and s2[0..j-1]
if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
else:                   dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Example: "abcde" and "ace"
     ""  a  c  e
  "" [0, 0, 0, 0]
  a  [0, 1, 1, 1]
  b  [0, 1, 1, 1]
  c  [0, 1, 2, 2]
  d  [0, 1, 2, 2]
  e  [0, 1, 2, 3]  → LCS = 3
```

```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

### NeetCode Problem: Best Time to Buy and Sell Stock with Cooldown

**Problem:** Can buy/sell repeatedly but must have cooldown of 1 day after selling.

```
States at each day:
  holding: have a stock
  sold:    just sold today (next day must be cooldown)
  cooldown: in cooldown (or never bought)

Transitions:
  holding[i]  = max(holding[i-1], cooldown[i-1] - prices[i])
  sold[i]     = holding[i-1] + prices[i]
  cooldown[i] = max(cooldown[i-1], sold[i-1])
```

```python
def maxProfit(prices):
    holding = float('-inf')  # can't hold without buying
    sold = 0
    cooldown = 0

    for price in prices:
        prev_holding = holding
        holding  = max(holding, cooldown - price)
        cooldown = max(cooldown, sold)
        sold     = prev_holding + price

    return max(sold, cooldown)
```

### NeetCode Problem: Coin Change II

**Problem:** Count ways to make amount using coins (unlimited use, combinations not permutations).

```
dp[i][j] = ways to make amount j using first i coin types
dp[i][j] = dp[i-1][j]                  # don't use coin i
          + dp[i][j - coins[i-1]]       # use coin i (can reuse → dp[i] not dp[i-1])
```

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1  # 1 way to make amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### NeetCode Problem: Target Sum

**Problem:** Assign + or - to each num. Count ways to reach target.

```
Backtracking: O(2^n) — try all assignments.

DP: reduce to subset sum.
  Nums assigned +: sum = P
  Nums assigned -: sum = S - P
  P - (S - P) = target → 2P = target + S → P = (target + S) / 2
  Find number of subsets summing to (target + S) / 2.

dp[j] = number of subsets with sum j
```

```python
def findTargetSumWays(nums, target):
    total = sum(nums)
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0

    subset_sum = (total + target) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for num in nums:
        for j in range(subset_sum, num - 1, -1):  # reverse to avoid reuse
            dp[j] += dp[j - num]

    return dp[subset_sum]
```

### NeetCode Problem: Interleaving String

**Problem:** Is s3 an interleaving of s1 and s2?

```
dp[i][j] = can s3[0..i+j-1] be formed by interleaving s1[0..i-1] and s2[0..j-1]

dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1])  # take from s1
           OR
           (dp[i][j-1] and s2[j-1]==s3[i+j-1])  # take from s2
```

```python
def isInterleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    if m + n != len(s3): return False

    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True

    for i in range(1, m+1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
    for j in range(1, n+1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = ((dp[i-1][j] and s1[i-1] == s3[i+j-1]) or
                        (dp[i][j-1] and s2[j-1] == s3[i+j-1]))

    return dp[m][n]
```

### NeetCode Problem: Edit Distance

**Problem:** Minimum operations (insert, delete, replace) to convert word1 to word2.

```
dp[i][j] = min edits to convert word1[0..i-1] to word2[0..j-1]

If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]   (chars match, no op needed)
Else:
  dp[i][j] = 1 + min(
    dp[i-1][j-1],   # replace
    dp[i-1][j],     # delete from word1
    dp[i][j-1]      # insert into word1
  )
```

```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1): dp[i][0] = i  # delete all of word1
    for j in range(n+1): dp[0][j] = j  # insert all of word2

    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

### NeetCode Problem: Distinct Subsequences

**Problem:** Count distinct subsequences of s that equal t.

```
dp[i][j] = number of distinct subseqs of s[0..i-1] that equal t[0..j-1]

If s[i-1] == t[j-1]:
  dp[i][j] = dp[i-1][j-1]    # include s[i-1] to match t[j-1]
           + dp[i-1][j]       # skip s[i-1], find t[0..j-1] in s[0..i-2]
Else:
  dp[i][j] = dp[i-1][j]      # must skip s[i-1]
```

```python
def numDistinct(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = 1  # empty t: always 1 way

    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = dp[i-1][j]
            if s[i-1] == t[j-1]:
                dp[i][j] += dp[i-1][j-1]

    return dp[m][n]
```

### NeetCode Problem: Burst Balloons

**Problem:** Array of balloons. Burst balloon i: get nums[i-1]*nums[i]*nums[i+1] coins. Maximize coins.

```
Key insight: instead of thinking about which to burst FIRST,
think about which to burst LAST.

dp[left][right] = max coins from bursting all balloons between left and right (exclusive).
If balloon k is the LAST burst in [left..right]:
  dp[left][right] = max(nums[left]*nums[k]*nums[right] + dp[left][k] + dp[k][right])
  for k in range(left+1, right)

Add boundary balloons with value 1 on both ends.
```

```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]

    # Fill by length of interval
    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(dp[left][right],
                    nums[left]*nums[k]*nums[right] + dp[left][k] + dp[k][right])

    return dp[0][n-1]
```

### NeetCode Problem: Regular Expression Matching

**Problem:** Implement '.' (matches any single char) and '*' (matches 0+ of preceding).

```
dp[i][j] = does pattern p[0..j-1] match text s[0..i-1]?

If p[j-1] == s[i-1] or p[j-1] == '.':
  dp[i][j] = dp[i-1][j-1]   (chars match, advance both)

If p[j-1] == '*':
  dp[i][j] = dp[i][j-2]     (use '*' as 0 occurrences)
  If p[j-2] == s[i-1] or p[j-2] == '.':
    dp[i][j] |= dp[i-1][j]  (match one more char with '*')
```

```python
def isMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True

    # Empty string matching patterns like a* or a*b* or a*b*c*
    for j in range(1, n+1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]  # 0 occurrences
                if p[j-2] == s[i-1] or p[j-2] == '.':
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == s[i-1] or p[j-1] == '.':
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

---

## Chapter 19: Greedy Algorithms

### 19.1 The Greedy Approach

Make the locally optimal choice at each step. Works when the problem has **optimal substructure** and **greedy choice property** — a global optimum can be reached through locally optimal choices.

### NeetCode Problem: Jump Game

**Problem:** Can you reach the last index? nums[i] = max jump from position i.

```
Greedy: track the furthest position we can reach.
At each position, update max_reach. If we ever reach a position > max_reach → stuck.
```

```python
def canJump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach: return False
        max_reach = max(max_reach, i + jump)
    return True
```

### NeetCode Problem: Jump Game II

**Problem:** Minimum jumps to reach last index.

```
Greedy BFS: track current range reachable in current number of jumps,
and farthest reachable in next jump.
When we exhaust current range: take a jump, extend to farthest.
```

```python
def jump(nums):
    jumps = 0
    cur_end = 0    # farthest we can reach with current number of jumps
    farthest = 0   # farthest we can reach with one more jump

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:   # exhausted current jump range
            jumps += 1
            cur_end = farthest

    return jumps
```

### NeetCode Problem: Gas Station

**Problem:** Circular route. gas[i]=gas at station i, cost[i]=gas to drive to next. Find start station or -1.

```
Observation 1: If total gas >= total cost, solution exists.
Observation 2: If we run out of gas at station k starting from 0,
  no station between 0 and k can be the start (they all run out even sooner).
  So next candidate is k+1.
```

```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost): return -1

    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0

    return start
```

### NeetCode Problem: Hand of Straights

**Problem:** Can cards be grouped into groups of groupSize consecutive cards?

```
Greedy: always form a group starting from the smallest available card.
Count frequencies. For each smallest unique value, form a group.
```

```python
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize != 0: return False

    count = Counter(hand)
    min_heap = list(count.keys())
    heapq.heapify(min_heap)

    while min_heap:
        start = min_heap[0]
        for i in range(start, start + groupSize):
            if count[i] == 0: return False
            count[i] -= 1
            if count[i] == 0:
                if min_heap[0] != i: return False
                heapq.heappop(min_heap)

    return True
```

---

## Chapter 20: Intervals

### NeetCode Problem: Insert Interval

**Problem:** Insert a new interval into sorted non-overlapping intervals. Merge if needed.

```
Three phases:
1. Add all intervals that end before newInterval starts (no overlap)
2. Merge all overlapping intervals with newInterval
3. Add all remaining intervals
```

```python
def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: intervals that end before newInterval starts
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)

    # Phase 3: remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

### NeetCode Problem: Merge Intervals

**Problem:** Merge all overlapping intervals.

```
Sort by start time. Then merge greedily.
```

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= result[-1][1]:                    # overlap
            result[-1][1] = max(result[-1][1], end)  # extend
        else:
            result.append([start, end])

    return result
```

### NeetCode Problem: Non-Overlapping Intervals

**Problem:** Remove minimum intervals to make remaining non-overlapping.

```
Greedy: sort by END time. At each step, greedily keep the interval that ends earliest.
If current interval overlaps with last kept: remove current (increment removed count).
```

```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by end time
    removed = 0
    prev_end = float('-inf')

    for start, end in intervals:
        if start >= prev_end:
            prev_end = end   # keep this interval
        else:
            removed += 1     # remove this interval (it overlaps and ends later)

    return removed
```

### NeetCode Problem: Meeting Rooms

**Problem:** Can a person attend all meetings?

```python
def canAttendMeetings(intervals):
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True
```

### NeetCode Problem: Meeting Rooms II

**Problem:** Minimum number of conference rooms needed.

```
Sort by start. Use min-heap tracking end times of ongoing meetings.
For each meeting: if heap top (earliest ending) ends before this starts → reuse room.
Else: need a new room.
```

```python
def minMeetingRooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []  # end times of ongoing meetings

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)  # reuse room
        else:
            heapq.heappush(heap, end)     # new room

    return len(heap)
```

---

## Chapter 21: Bit Manipulation

### 21.1 Bitwise Operations Reference

```
n & 1       → check if n is odd (last bit)
n & (n-1)   → clear lowest set bit
n & (-n)    → isolate lowest set bit
n | (1<<k)  → set bit k
n ^ (1<<k)  → flip bit k
n >> 1      → divide by 2
n << 1      → multiply by 2
n ^ n = 0   → XOR with itself = 0
n ^ 0 = n   → XOR with 0 = n
XOR is commutative and associative
```

### NeetCode Problem: Number of 1 Bits (Hamming Weight)

```python
def hammingWeight(n):
    count = 0
    while n:
        n &= n - 1   # clear the lowest set bit
        count += 1
    return count
```

### NeetCode Problem: Counting Bits

**Problem:** For every number 0..n, count 1-bits.

```
dp[i] = dp[i >> 1] + (i & 1)
i >> 1 = i divided by 2 (same bits except the last)
i & 1  = value of last bit
```

```python
def countBits(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### NeetCode Problem: Reverse Bits

```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

### NeetCode Problem: Missing Number

**Problem:** Array 0..n with one missing. Find it.

```
XOR approach: XOR all indices and all values.
Pairs cancel out: x^x=0. Unpaired = missing number.

Or math: expected_sum - actual_sum.
```

```python
def missingNumber(nums):
    xor = 0
    for i, n in enumerate(nums):
        xor ^= i ^ n
    return xor ^ len(nums)

# Math version
def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

### NeetCode Problem: Sum of Two Integers (No + or -)

**Problem:** Calculate sum without + or - operators.

```
Bit addition without carry: a ^ b
Carry bits: (a & b) << 1
Repeat until no carry.
```

```python
def getSum(a, b):
    mask = 0xFFFFFFFF  # 32-bit mask for handling overflow in Python
    while b & mask:
        a, b = a ^ b, (a & b) << 1
    return a if b == 0 else a & mask  # handle potential overflow
```

### NeetCode Problem: Single Number

**Problem:** Every element appears twice except one. Find it.

```
XOR: all pairs cancel. Single number remains.
```

```python
def singleNumber(nums):
    result = 0
    for n in nums:
        result ^= n
    return result
```

---

## Chapter 22: Math & Geometry

### NeetCode Problem: Rotate Image

**Problem:** Rotate n×n matrix 90 degrees clockwise in-place.

```
Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
Step 2: Reverse each row

    1 2 3       1 4 7       7 4 1
    4 5 6  →T→  2 5 8  →R→  8 5 2
    7 8 9       3 6 9       9 6 3
```

```python
def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse each row
    for row in matrix:
        row.reverse()
```

### NeetCode Problem: Spiral Matrix

**Problem:** Return elements of matrix in spiral order.

```
Maintain four boundaries: top, bottom, left, right.
Traverse: right → down → left → up, shrinking boundaries each time.
```

```python
def spiralOrder(matrix):
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right+1):     result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom+1):     result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left-1, -1): result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top-1, -1): result.append(matrix[r][left])
            left += 1

    return result
```

### NeetCode Problem: Set Matrix Zeroes

**Problem:** If matrix[i][j]==0, set entire row i and column j to 0. In-place.

```
Two passes:
Pass 1: record which rows and cols contain 0 (using first row and col as markers).
Pass 2: set zeros based on markers.
Handle first row and col separately.
```

```python
def setZeroes(matrix):
    ROWS, COLS = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(COLS))
    first_col_zero = any(matrix[r][0] == 0 for r in range(ROWS))

    # Use first row/col as markers
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    # Zero out based on markers
    for r in range(1, ROWS):
        for c in range(1, COLS):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if first_row_zero:
        for c in range(COLS): matrix[0][c] = 0
    if first_col_zero:
        for r in range(ROWS): matrix[r][0] = 0
```

### NeetCode Problem: Happy Number

**Problem:** A number is happy if repeatedly replacing it with sum of squares of digits eventually reaches 1.

```
Cycle detection: use Floyd's or a set.
```

```python
def isHappy(n):
    def digit_square_sum(x):
        total = 0
        while x:
            total += (x % 10) ** 2
            x //= 10
        return total

    seen = set()
    while n != 1:
        n = digit_square_sum(n)
        if n in seen: return False
        seen.add(n)
    return True
```

### NeetCode Problem: Plus One

```python
def plusOne(digits):
    for i in range(len(digits)-1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits
```

### NeetCode Problem: Pow(x, n)

**Problem:** Implement pow(x, n) efficiently.

```
Fast exponentiation: x^n = x^(n//2) * x^(n//2) [* x if n is odd]
O(log n) instead of O(n).
```

```python
def myPow(x, n):
    if n < 0:
        x, n = 1/x, -n

    result = 1.0
    while n:
        if n & 1:         # n is odd
            result *= x
        x *= x            # square x
        n >>= 1           # n //= 2
    return result
```

### NeetCode Problem: Multiply Strings

**Problem:** Multiply two non-negative integers represented as strings.

```
Simulate long multiplication.
num1[i] * num2[j] contributes to positions i+j and i+j+1 in result.
```

```python
def multiply(num1, num2):
    if num1 == "0" or num2 == "0": return "0"
    m, n = len(num1), len(num2)
    pos = [0] * (m + n)

    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            mul = (ord(num1[i])-ord('0')) * (ord(num2[j])-ord('0'))
            p1, p2 = i+j, i+j+1
            total = mul + pos[p2]
            pos[p2] = total % 10
            pos[p1] += total // 10

    result = ''.join(str(d) for d in pos).lstrip('0')
    return result or "0"
```

---

## Appendix: NeetCode 150 Problem Index

### Arrays & Hashing
| Problem | Pattern | Difficulty |
|---------|---------|------------|
| Contains Duplicate | Set | Easy |
| Valid Anagram | Frequency Count | Easy |
| Two Sum | HashMap | Easy |
| Group Anagrams | HashMap + Sorting | Medium |
| Top K Frequent Elements | Bucket Sort / Heap | Medium |
| Product of Array Except Self | Prefix + Suffix | Medium |
| Valid Sudoku | HashSet | Medium |
| Encode and Decode Strings | Length Prefix | Medium |
| Longest Consecutive Sequence | Set | Medium |

### Two Pointers
| Valid Palindrome | Two Pointer | Easy |
| Two Sum II | Two Pointer | Medium |
| 3Sum | Sort + Two Pointer | Medium |
| Container With Most Water | Two Pointer | Medium |
| Trapping Rain Water | Two Pointer / Stack | Hard |

### Sliding Window
| Best Time to Buy/Sell Stock | Sliding Window | Easy |
| Longest Substring No Repeat | Sliding Window + Set | Medium |
| Longest Repeating Char Replace | Sliding Window | Medium |
| Permutation in String | Fixed Window | Medium |
| Minimum Window Substring | Variable Window | Hard |
| Sliding Window Maximum | Monotonic Deque | Hard |

### Stack
| Valid Parentheses | Stack | Easy |
| Min Stack | Stack | Medium |
| Evaluate RPN | Stack | Medium |
| Generate Parentheses | Backtracking | Medium |
| Daily Temperatures | Monotonic Stack | Medium |
| Car Fleet | Monotonic Stack | Medium |
| Largest Rectangle in Histogram | Monotonic Stack | Hard |

### Binary Search
| Binary Search | Binary Search | Easy |
| Search 2D Matrix | Binary Search | Medium |
| Koko Eating Bananas | Binary Search on Answer | Medium |
| Find Min in Rotated Sorted Array | Binary Search | Medium |
| Search in Rotated Sorted Array | Binary Search | Medium |
| Time Based Key-Value Store | Binary Search | Medium |
| Median of Two Sorted Arrays | Binary Search | Hard |

### Linked List
| Reverse Linked List | Pointer Reversal | Easy |
| Merge Two Sorted Lists | Merge | Easy |
| Linked List Cycle | Floyd's | Easy |
| Reorder List | Find Mid + Reverse + Merge | Medium |
| Remove Nth Node From End | Two Pointer | Medium |
| Copy List w/ Random Pointer | HashMap | Medium |
| Add Two Numbers | Simulation | Medium |
| Find The Duplicate Number | Floyd's | Medium |
| LRU Cache | HashMap + DLL | Medium |
| Merge K Sorted Lists | Heap | Hard |
| Reverse Nodes in K-Group | Simulation | Hard |

### Trees
| Invert Binary Tree | DFS | Easy |
| Maximum Depth | DFS | Easy |
| Diameter | DFS | Easy |
| Balanced Binary Tree | DFS | Easy |
| Same Tree | DFS | Easy |
| Subtree of Another Tree | DFS | Easy |
| LCA of BST | BST Property | Medium |
| Level Order Traversal | BFS | Medium |
| Right Side View | BFS | Medium |
| Count Good Nodes | DFS | Medium |
| Validate BST | DFS with bounds | Medium |
| Kth Smallest in BST | Inorder | Medium |
| Construct from Preorder+Inorder | Recursion | Medium |
| Max Path Sum | DFS Post-order | Hard |
| Serialize and Deserialize | DFS | Hard |

### Graphs
| Number of Islands | DFS/BFS | Medium |
| Clone Graph | DFS | Medium |
| Pacific Atlantic | Multi-source BFS | Medium |
| Course Schedule | Cycle Detection | Medium |
| Course Schedule II | Topological Sort | Medium |
| Surrounded Regions | DFS from border | Medium |
| Rotting Oranges | Multi-source BFS | Medium |
| Walls and Gates | Multi-source BFS | Medium |
| Max Area of Island | DFS | Medium |
| Number of Connected Components | Union-Find | Medium |
| Graph Valid Tree | DFS/Union-Find | Medium |
| Redundant Connection | Union-Find | Medium |
| Word Ladder | BFS | Hard |
| Alien Dictionary | Topological Sort | Hard |
| Network Delay Time | Dijkstra | Medium |
| Cheapest Flights w/ K Stops | Bellman-Ford | Medium |
| Min Cost Connect All Points | Prim's MST | Medium |
| Swim in Rising Water | Dijkstra | Hard |

### Dynamic Programming
| Climbing Stairs | DP | Easy |
| Min Cost Climbing Stairs | DP | Easy |
| House Robber | DP | Medium |
| House Robber II | DP | Medium |
| Longest Palindromic Substring | Expand Around Center | Medium |
| Palindromic Substrings | Expand Around Center | Medium |
| Decode Ways | DP | Medium |
| Coin Change | DP | Medium |
| Maximum Product Subarray | DP | Medium |
| Word Break | DP | Medium |
| LIS | DP / Binary Search | Medium |
| Partition Equal Subset Sum | 0/1 Knapsack | Medium |
| Unique Paths | 2D DP | Medium |
| Longest Common Subsequence | 2D DP | Medium |
| Best Time to Buy/Sell with Cooldown | State Machine DP | Medium |
| Coin Change II | 2D DP (Unbounded Knapsack) | Medium |
| Target Sum | DP / Subset Sum | Medium |
| Interleaving String | 2D DP | Medium |
| Edit Distance | 2D DP | Hard |
| Distinct Subsequences | 2D DP | Hard |
| Burst Balloons | Interval DP | Hard |
| Regular Expression Matching | 2D DP | Hard |

### Greedy & Intervals
| Jump Game | Greedy | Medium |
| Jump Game II | Greedy BFS | Medium |
| Gas Station | Greedy | Medium |
| Insert Interval | Simulation | Medium |
| Merge Intervals | Sort + Greedy | Medium |
| Non-Overlapping Intervals | Sort by end + Greedy | Medium |

### Bit Manipulation
| Number of 1 Bits | Bit Trick | Easy |
| Counting Bits | DP + Bits | Easy |
| Reverse Bits | Bit Manipulation | Easy |
| Missing Number | XOR / Math | Easy |
| Single Number | XOR | Easy |
| Sum of Two Integers | Bit Addition | Medium |

### Math
| Rotate Image | Transpose + Reverse | Medium |
| Spiral Matrix | Boundary Simulation | Medium |
| Set Matrix Zeroes | In-place Marking | Medium |
| Happy Number | Cycle Detection | Easy |
| Plus One | Array Manipulation | Easy |
| Pow(x,n) | Fast Exponentiation | Medium |
| Multiply Strings | Long Multiplication | Medium |

---

## Pattern Cheat Sheet

```
Subarray/Substring problem  → Sliding Window or Prefix Sum
Count pairs                 → HashMap (complement lookup)
Sorted array + pair/triplet → Two Pointers
Nested brackets             → Stack
Next greater/smaller        → Monotonic Stack
Find Kth / top K            → Heap
Prefix/suffix optimization  → Prefix Arrays
Tree problems               → DFS recursion or BFS with queue
Shortest path (unweighted)  → BFS
Shortest path (weighted +)  → Dijkstra (heap)
Shortest path (neg weights) → Bellman-Ford
All shortest paths          → Floyd-Warshall
Cycle in directed graph     → DFS with 3 states (unvisited/visiting/done)
Connectivity / grouping     → Union-Find or DFS
Topological order           → DFS post-order or Kahn's BFS
Exhaustive combinations     → Backtracking
Optimal choice at each step → Greedy (prove it's safe first)
Overlapping subproblems     → Dynamic Programming
  1D recurrence             → 1D DP array
  2D string/grid            → 2D DP table
  Tree recurrence           → DFS returning values
String prefix/search        → Trie
Answer is in a range        → Binary search on answer
```
