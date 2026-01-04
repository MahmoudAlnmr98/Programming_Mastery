# Problem Solving & Algorithms Interview Questions

## Table of Contents
- [Beginner Level](#beginner-level)
- [Intermediate Level](#intermediate-level)
- [Advanced Level](#advanced-level)

---

## Beginner Level

### 1. Two Sum Problem

**Problem:** Given an array of integers and a target sum, find two numbers that add up to target.

**Solution:**
```javascript
// Time: O(n), Space: O(n)
function twoSum(nums, target) {
    const map = new Map();
    
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        map.set(nums[i], i);
    }
    return [];
}

// Example
twoSum([2, 7, 11, 15], 9); // [0, 1]
```

### 2. Reverse a String

**Problem:** Reverse a string.

**Solution:**
```javascript
// Method 1: Built-in
function reverse(str) {
    return str.split('').reverse().join('');
}

// Method 2: Loop
function reverse(str) {
    let reversed = '';
    for (let i = str.length - 1; i >= 0; i--) {
        reversed += str[i];
    }
    return reversed;
}

// Method 3: Recursion
function reverse(str) {
    if (str.length <= 1) return str;
    return reverse(str.slice(1)) + str[0];
}
```

### 3. Check if String is Palindrome

**Problem:** Check if string reads same forwards and backwards.

**Solution:**
```javascript
function isPalindrome(str) {
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    return cleaned === cleaned.split('').reverse().join('');
}

// Two pointers
function isPalindrome(str) {
    let left = 0;
    let right = str.length - 1;
    
    while (left < right) {
        if (str[left] !== str[right]) return false;
        left++;
        right--;
    }
    return true;
}
```

### 4. Find Maximum in Array

**Problem:** Find maximum element in array.

**Solution:**
```javascript
// Built-in
function findMax(arr) {
    return Math.max(...arr);
}

// Loop
function findMax(arr) {
    let max = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

// Reduce
function findMax(arr) {
    return arr.reduce((max, num) => num > max ? num : max, arr[0]);
}
```

### 5. Factorial

**Problem:** Calculate factorial of n.

**Solution:**
```javascript
// Iterative
function factorial(n) {
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Recursive
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

### 6. Fibonacci Sequence

**Problem:** Generate Fibonacci sequence.

**Solution:**
```javascript
// Recursive (inefficient)
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Iterative (efficient)
function fibonacci(n) {
    if (n <= 1) return n;
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        [a, b] = [b, a + b];
    }
    return b;
}

// Memoized
function fibonacci(n, memo = {}) {
    if (n in memo) return memo[n];
    if (n <= 1) return n;
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
    return memo[n];
}
```

### 7. Remove Duplicates from Array

**Problem:** Remove duplicate elements from array.

**Solution:**
```javascript
// Using Set
function removeDuplicates(arr) {
    return [...new Set(arr)];
}

// Using filter
function removeDuplicates(arr) {
    return arr.filter((item, index) => arr.indexOf(item) === index);
}

// Using reduce
function removeDuplicates(arr) {
    return arr.reduce((acc, item) => {
        if (!acc.includes(item)) acc.push(item);
        return acc;
    }, []);
}
```

### 8. Count Characters in String

**Problem:** Count frequency of each character in string.

**Solution:**
```javascript
function countChars(str) {
    const count = {};
    for (let char of str) {
        count[char] = (count[char] || 0) + 1;
    }
    return count;
}

// Using reduce
function countChars(str) {
    return str.split('').reduce((acc, char) => {
        acc[char] = (acc[char] || 0) + 1;
        return acc;
    }, {});
}
```

---

## Intermediate Level

### 9. Valid Parentheses

**Problem:** Check if parentheses are valid.

**Solution:**
```javascript
function isValid(s) {
    const stack = [];
    const map = {
        ')': '(',
        '}': '{',
        ']': '['
    };
    
    for (let char of s) {
        if (char in map) {
            if (stack.length === 0 || stack.pop() !== map[char]) {
                return false;
            }
        } else {
            stack.push(char);
        }
    }
    return stack.length === 0;
}
```

### 10. Merge Two Sorted Arrays

**Problem:** Merge two sorted arrays into one sorted array.

**Solution:**
```javascript
function mergeSorted(arr1, arr2) {
    const merged = [];
    let i = 0, j = 0;
    
    while (i < arr1.length && j < arr2.length) {
        if (arr1[i] < arr2[j]) {
            merged.push(arr1[i++]);
        } else {
            merged.push(arr2[j++]);
        }
    }
    
    while (i < arr1.length) merged.push(arr1[i++]);
    while (j < arr2.length) merged.push(arr2[j++]);
    
    return merged;
}
```

### 11. Binary Search

**Problem:** Search for element in sorted array.

**Solution:**
```javascript
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        
        if (arr[mid] === target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    
    return -1;
}
```

### 12. Longest Common Prefix

**Problem:** Find longest common prefix among array of strings.

**Solution:**
```javascript
function longestCommonPrefix(strs) {
    if (strs.length === 0) return '';
    
    let prefix = strs[0];
    
    for (let i = 1; i < strs.length; i++) {
        while (strs[i].indexOf(prefix) !== 0) {
            prefix = prefix.slice(0, -1);
            if (prefix === '') return '';
        }
    }
    
    return prefix;
}
```

### 13. Reverse Linked List

**Problem:** Reverse a linked list.

**Solution:**
```javascript
// Iterative
function reverseList(head) {
    let prev = null;
    let current = head;
    
    while (current !== null) {
        const next = current.next;
        current.next = prev;
        prev = current;
        current = next;
    }
    
    return prev;
}

// Recursive
function reverseList(head) {
    if (head === null || head.next === null) return head;
    
    const reversed = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    
    return reversed;
}
```

### 14. Contains Duplicate

**Problem:** Check if array contains duplicates.

**Solution:**
```javascript
// Using Set
function containsDuplicate(nums) {
    return new Set(nums).size !== nums.length;
}

// Using Map
function containsDuplicate(nums) {
    const seen = new Map();
    for (let num of nums) {
        if (seen.has(num)) return true;
        seen.set(num, true);
    }
    return false;
}
```

### 15. Best Time to Buy and Sell Stock

**Problem:** Find maximum profit from buying and selling stock.

**Solution:**
```javascript
function maxProfit(prices) {
    let minPrice = Infinity;
    let maxProfit = 0;
    
    for (let price of prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    
    return maxProfit;
}
```

### 16. Valid Anagram

**Problem:** Check if two strings are anagrams.

**Solution:**
```javascript
function isAnagram(s, t) {
    if (s.length !== t.length) return false;
    
    const count = {};
    
    for (let char of s) {
        count[char] = (count[char] || 0) + 1;
    }
    
    for (let char of t) {
        if (!count[char]) return false;
        count[char]--;
    }
    
    return true;
}

// Using sort
function isAnagram(s, t) {
    return s.split('').sort().join('') === t.split('').sort().join('');
}
```

### 17. Group Anagrams

**Problem:** Group strings that are anagrams.

**Solution:**
```javascript
function groupAnagrams(strs) {
    const map = new Map();
    
    for (let str of strs) {
        const key = str.split('').sort().join('');
        if (!map.has(key)) {
            map.set(key, []);
        }
        map.get(key).push(str);
    }
    
    return Array.from(map.values());
}
```

### 18. Maximum Subarray (Kadane's Algorithm)

**Problem:** Find maximum sum of contiguous subarray.

**Solution:**
```javascript
function maxSubArray(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
}
```

### 19. Product of Array Except Self

**Problem:** Return array where each element is product of all other elements.

**Solution:**
```javascript
function productExceptSelf(nums) {
    const result = [];
    let product = 1;
    
    // Left products
    for (let i = 0; i < nums.length; i++) {
        result[i] = product;
        product *= nums[i];
    }
    
    product = 1;
    // Right products
    for (let i = nums.length - 1; i >= 0; i--) {
        result[i] *= product;
        product *= nums[i];
    }
    
    return result;
}
```

### 20. Three Sum

**Problem:** Find all unique triplets that sum to zero.

**Solution:**
```javascript
function threeSum(nums) {
    nums.sort((a, b) => a - b);
    const result = [];
    
    for (let i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        
        let left = i + 1;
        let right = nums.length - 1;
        
        while (left < right) {
            const sum = nums[i] + nums[left] + nums[right];
            
            if (sum === 0) {
                result.push([nums[i], nums[left], nums[right]]);
                while (left < right && nums[left] === nums[left + 1]) left++;
                while (left < right && nums[right] === nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return result;
}
```

---

## Advanced Level

### 21. Merge K Sorted Lists

**Problem:** Merge k sorted linked lists.

**Solution:**
```javascript
function mergeKLists(lists) {
    if (lists.length === 0) return null;
    
    while (lists.length > 1) {
        const merged = [];
        for (let i = 0; i < lists.length; i += 2) {
            const l1 = lists[i];
            const l2 = i + 1 < lists.length ? lists[i + 1] : null;
            merged.push(mergeTwoLists(l1, l2));
        }
        lists = merged;
    }
    
    return lists[0];
}

function mergeTwoLists(l1, l2) {
    const dummy = new ListNode(0);
    let current = dummy;
    
    while (l1 && l2) {
        if (l1.val < l2.val) {
            current.next = l1;
            l1 = l1.next;
        } else {
            current.next = l2;
            l2 = l2.next;
        }
        current = current.next;
    }
    
    current.next = l1 || l2;
    return dummy.next;
}
```

### 22. Longest Palindromic Substring

**Problem:** Find longest palindromic substring.

**Solution:**
```javascript
function longestPalindrome(s) {
    let start = 0;
    let maxLen = 0;
    
    function expandAroundCenter(left, right) {
        while (left >= 0 && right < s.length && s[left] === s[right]) {
            left--;
            right++;
        }
        return right - left - 1;
    }
    
    for (let i = 0; i < s.length; i++) {
        const len1 = expandAroundCenter(i, i); // Odd length
        const len2 = expandAroundCenter(i, i + 1); // Even length
        const len = Math.max(len1, len2);
        
        if (len > maxLen) {
            maxLen = len;
            start = i - Math.floor((len - 1) / 2);
        }
    }
    
    return s.substring(start, start + maxLen);
}
```

### 23. Trapping Rain Water

**Problem:** Calculate trapped rainwater.

**Solution:**
```javascript
function trap(height) {
    let left = 0;
    let right = height.length - 1;
    let leftMax = 0;
    let rightMax = 0;
    let water = 0;
    
    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= leftMax) {
                leftMax = height[left];
            } else {
                water += leftMax - height[left];
            }
            left++;
        } else {
            if (height[right] >= rightMax) {
                rightMax = height[right];
            } else {
                water += rightMax - height[right];
            }
            right--;
        }
    }
    
    return water;
}
```

### 24. Word Ladder

**Problem:** Find shortest transformation sequence between two words.

**Solution:**
```javascript
function ladderLength(beginWord, endWord, wordList) {
    const wordSet = new Set(wordList);
    if (!wordSet.has(endWord)) return 0;
    
    const queue = [[beginWord, 1]];
    const visited = new Set([beginWord]);
    
    while (queue.length > 0) {
        const [word, level] = queue.shift();
        
        if (word === endWord) return level;
        
        for (let i = 0; i < word.length; i++) {
            for (let c = 97; c <= 122; c++) {
                const newWord = word.slice(0, i) + String.fromCharCode(c) + word.slice(i + 1);
                
                if (wordSet.has(newWord) && !visited.has(newWord)) {
                    visited.add(newWord);
                    queue.push([newWord, level + 1]);
                }
            }
        }
    }
    
    return 0;
}
```

### 25. Serialize and Deserialize Binary Tree

**Problem:** Convert binary tree to string and back.

**Solution:**
```javascript
function serialize(root) {
    const result = [];
    
    function dfs(node) {
        if (!node) {
            result.push('null');
            return;
        }
        result.push(node.val.toString());
        dfs(node.left);
        dfs(node.right);
    }
    
    dfs(root);
    return result.join(',');
}

function deserialize(data) {
    const values = data.split(',');
    let index = 0;
    
    function dfs() {
        if (values[index] === 'null') {
            index++;
            return null;
        }
        
        const node = new TreeNode(parseInt(values[index++]));
        node.left = dfs();
        node.right = dfs();
        return node;
    }
    
    return dfs();
}
```

### 26. Longest Substring Without Repeating Characters

**Problem:** Find length of longest substring without repeating characters.

**Solution:**
```javascript
function lengthOfLongestSubstring(s) {
    const map = new Map();
    let maxLen = 0;
    let start = 0;
    
    for (let end = 0; end < s.length; end++) {
        if (map.has(s[end])) {
            start = Math.max(start, map.get(s[end]) + 1);
        }
        map.set(s[end], end);
        maxLen = Math.max(maxLen, end - start + 1);
    }
    
    return maxLen;
}
```

### 27. Container With Most Water

**Problem:** Find two lines that form container with most water.

**Solution:**
```javascript
function maxArea(height) {
    let left = 0;
    let right = height.length - 1;
    let maxArea = 0;
    
    while (left < right) {
        const area = Math.min(height[left], height[right]) * (right - left);
        maxArea = Math.max(maxArea, area);
        
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    
    return maxArea;
}
```

### 28. Climbing Stairs

**Problem:** Count ways to climb n stairs (1 or 2 steps at a time).

**Solution:**
```javascript
// Dynamic Programming
function climbStairs(n) {
    if (n <= 2) return n;
    
    let first = 1;
    let second = 2;
    
    for (let i = 3; i <= n; i++) {
        const third = first + second;
        first = second;
        second = third;
    }
    
    return second;
}
```

### 29. House Robber

**Problem:** Maximum money that can be robbed without robbing adjacent houses.

**Solution:**
```javascript
function rob(nums) {
    if (nums.length === 0) return 0;
    if (nums.length === 1) return nums[0];
    
    let prev2 = nums[0];
    let prev1 = Math.max(nums[0], nums[1]);
    
    for (let i = 2; i < nums.length; i++) {
        const current = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = current;
    }
    
    return prev1;
}
```

### 30. Generate Parentheses

**Problem:** Generate all valid combinations of n pairs of parentheses.

**Solution:**
```javascript
function generateParenthesis(n) {
    const result = [];
    
    function backtrack(current, open, close) {
        if (current.length === n * 2) {
            result.push(current);
            return;
        }
        
        if (open < n) {
            backtrack(current + '(', open + 1, close);
        }
        
        if (close < open) {
            backtrack(current + ')', open, close + 1);
        }
    }
    
    backtrack('', 0, 0);
    return result;
}
```

### 31. Merge Intervals

**Problem:** Merge overlapping intervals.

**Solution:**
```javascript
function merge(intervals) {
    if (intervals.length <= 1) return intervals;
    
    intervals.sort((a, b) => a[0] - b[0]);
    const merged = [intervals[0]];
    
    for (let i = 1; i < intervals.length; i++) {
        const current = intervals[i];
        const last = merged[merged.length - 1];
        
        if (current[0] <= last[1]) {
            last[1] = Math.max(last[1], current[1]);
        } else {
            merged.push(current);
        }
    }
    
    return merged;
}
```

### 32. Rotate Array

**Problem:** Rotate array to right by k steps.

**Solution:**
```javascript
function rotate(nums, k) {
    k = k % nums.length;
    
    // Reverse entire array
    reverse(nums, 0, nums.length - 1);
    // Reverse first k elements
    reverse(nums, 0, k - 1);
    // Reverse remaining elements
    reverse(nums, k, nums.length - 1);
}

function reverse(nums, start, end) {
    while (start < end) {
        [nums[start], nums[end]] = [nums[end], nums[start]];
        start++;
        end--;
    }
}
```

### 33. Find Minimum in Rotated Sorted Array

**Problem:** Find minimum element in rotated sorted array.

**Solution:**
```javascript
function findMin(nums) {
    let left = 0;
    let right = nums.length - 1;
    
    while (left < right) {
        const mid = Math.floor((left + right) / 2);
        
        if (nums[mid] > nums[right]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    return nums[left];
}
```

### 34. Word Break

**Problem:** Check if string can be segmented into dictionary words.

**Solution:**
```javascript
function wordBreak(s, wordDict) {
    const wordSet = new Set(wordDict);
    const dp = new Array(s.length + 1).fill(false);
    dp[0] = true;
    
    for (let i = 1; i <= s.length; i++) {
        for (let j = 0; j < i; j++) {
            if (dp[j] && wordSet.has(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
        }
    }
    
    return dp[s.length];
}
```

### 35. Coin Change

**Problem:** Find minimum coins needed to make amount.

**Solution:**
```javascript
function coinChange(coins, amount) {
    const dp = new Array(amount + 1).fill(Infinity);
    dp[0] = 0;
    
    for (let i = 1; i <= amount; i++) {
        for (const coin of coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    return dp[amount] === Infinity ? -1 : dp[amount];
}
```

### 36. Implement Stack using Array.

**Problem:** Implement stack data structure.

**Solution:**
```javascript
class Stack {
    constructor() {
        this.items = [];
    }
    
    push(element) {
        this.items.push(element);
    }
    
    pop() {
        if (this.isEmpty()) return null;
        return this.items.pop();
    }
    
    peek() {
        return this.items[this.items.length - 1];
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
    
    size() {
        return this.items.length;
    }
}
```

### 37. Implement Queue using Array.

**Problem:** Implement queue data structure.

**Solution:**
```javascript
class Queue {
    constructor() {
        this.items = [];
    }
    
    enqueue(element) {
        this.items.push(element);
    }
    
    dequeue() {
        if (this.isEmpty()) return null;
        return this.items.shift();
    }
    
    front() {
        return this.items[0];
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
    
    size() {
        return this.items.length;
    }
}
```

### 38. Implement Binary Search Tree.

**Problem:** Implement BST with insert, search, delete.

**Solution:**
```javascript
class TreeNode {
    constructor(val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}

class BST {
    constructor() {
        this.root = null;
    }
    
    insert(val) {
        this.root = this._insert(this.root, val);
    }
    
    _insert(node, val) {
        if (!node) return new TreeNode(val);
        if (val < node.val) {
            node.left = this._insert(node.left, val);
        } else {
            node.right = this._insert(node.right, val);
        }
        return node;
    }
    
    search(val) {
        return this._search(this.root, val);
    }
    
    _search(node, val) {
        if (!node || node.val === val) return node;
        if (val < node.val) return this._search(node.left, val);
        return this._search(node.right, val);
    }
}
```

### 39. Implement Linked List.

**Problem:** Implement singly linked list.

**Solution:**
```javascript
class ListNode {
    constructor(val) {
        this.val = val;
        this.next = null;
    }
}

class LinkedList {
    constructor() {
        this.head = null;
        this.size = 0;
    }
    
    add(val) {
        const node = new ListNode(val);
        if (!this.head) {
            this.head = node;
        } else {
            let current = this.head;
            while (current.next) {
                current = current.next;
            }
            current.next = node;
        }
        this.size++;
    }
    
    remove(val) {
        if (!this.head) return false;
        if (this.head.val === val) {
            this.head = this.head.next;
            this.size--;
            return true;
        }
        let current = this.head;
        while (current.next) {
            if (current.next.val === val) {
                current.next = current.next.next;
                this.size--;
                return true;
            }
            current = current.next;
        }
        return false;
    }
}
```

### 40. Implement Hash Table.

**Problem:** Implement hash table with collision handling.

**Solution:**
```javascript
class HashTable {
    constructor(size = 10) {
        this.buckets = new Array(size).fill(null).map(() => []);
        this.size = size;
    }
    
    hash(key) {
        let hash = 0;
        for (let i = 0; i < key.length; i++) {
            hash = (hash + key.charCodeAt(i)) % this.size;
        }
        return hash;
    }
    
    set(key, value) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const existing = bucket.find(item => item[0] === key);
        if (existing) {
            existing[1] = value;
        } else {
            bucket.push([key, value]);
        }
    }
    
    get(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const item = bucket.find(item => item[0] === key);
        return item ? item[1] : undefined;
    }
    
    delete(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const itemIndex = bucket.findIndex(item => item[0] === key);
        if (itemIndex !== -1) {
            bucket.splice(itemIndex, 1);
            return true;
        }
        return false;
    }
}
```

---

## Common Patterns

### Two Pointers
- Used for sorted arrays
- Examples: Two Sum, Three Sum, Container With Most Water

### Sliding Window
- Used for subarray/substring problems
- Examples: Longest Substring Without Repeating Characters, Minimum Window Substring

### Hash Map/Set
- Used for lookups and frequency counting
- Examples: Two Sum, Group Anagrams, Contains Duplicate

### Stack
- Used for matching problems
- Examples: Valid Parentheses, Daily Temperatures

### Dynamic Programming
- Used for optimization problems
- Examples: Climbing Stairs, House Robber, Longest Increasing Subsequence

### Greedy
- Used for optimization with local choices
- Examples: Best Time to Buy Stock, Jump Game

### Backtracking
- Used for generating all solutions
- Examples: N-Queens, Generate Parentheses, Combination Sum

### 41. Longest Palindromic Substring

**Problem:** Find the longest palindromic substring in a string.

**Solution:**
```javascript
// Time: O(n^2), Space: O(1)
function longestPalindrome(s) {
    let start = 0, maxLen = 0;
    
    function expandAroundCenter(left, right) {
        while (left >= 0 && right < s.length && s[left] === s[right]) {
            left--;
            right++;
        }
        return right - left - 1;
    }
    
    for (let i = 0; i < s.length; i++) {
        const len1 = expandAroundCenter(i, i); // Odd length
        const len2 = expandAroundCenter(i, i + 1); // Even length
        const len = Math.max(len1, len2);
        
        if (len > maxLen) {
            maxLen = len;
            start = i - Math.floor((len - 1) / 2);
        }
    }
    
    return s.substring(start, start + maxLen);
}

// Example
longestPalindrome("babad"); // "bab" or "aba"
```

### 42. Container With Most Water

**Problem:** Find two lines that together with x-axis forms container with most water.

**Solution:**
```javascript
// Time: O(n), Space: O(1)
function maxArea(height) {
    let left = 0, right = height.length - 1;
    let maxArea = 0;
    
    while (left < right) {
        const area = Math.min(height[left], height[right]) * (right - left);
        maxArea = Math.max(maxArea, area);
        
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    
    return maxArea;
}

// Example
maxArea([1,8,6,2,5,4,8,3,7]); // 49
```

### 43. Three Sum

**Problem:** Find all unique triplets that sum to zero.

**Solution:**
```javascript
// Time: O(n^2), Space: O(1)
function threeSum(nums) {
    nums.sort((a, b) => a - b);
    const result = [];
    
    for (let i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        
        let left = i + 1, right = nums.length - 1;
        
        while (left < right) {
            const sum = nums[i] + nums[left] + nums[right];
            
            if (sum === 0) {
                result.push([nums[i], nums[left], nums[right]]);
                while (left < right && nums[left] === nums[left + 1]) left++;
                while (left < right && nums[right] === nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    
    return result;
}

// Example
threeSum([-1,0,1,2,-1,-4]); // [[-1,-1,2],[-1,0,1]]
```

### 44. Merge Intervals

**Problem:** Merge overlapping intervals.

**Solution:**
```javascript
// Time: O(n log n), Space: O(n)
function merge(intervals) {
    if (intervals.length <= 1) return intervals;
    
    intervals.sort((a, b) => a[0] - b[0]);
    const merged = [intervals[0]];
    
    for (let i = 1; i < intervals.length; i++) {
        const current = intervals[i];
        const last = merged[merged.length - 1];
        
        if (current[0] <= last[1]) {
            last[1] = Math.max(last[1], current[1]);
        } else {
            merged.push(current);
        }
    }
    
    return merged;
}

// Example
merge([[1,3],[2,6],[8,10],[15,18]]); // [[1,6],[8,10],[15,18]]
```

### 45. Best Time to Buy and Sell Stock

**Problem:** Find maximum profit from buying and selling stock once.

**Solution:**
```javascript
// Time: O(n), Space: O(1)
function maxProfit(prices) {
    let minPrice = Infinity;
    let maxProfit = 0;
    
    for (let price of prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    
    return maxProfit;
}

// Example
maxProfit([7,1,5,3,6,4]); // 5 (buy at 1, sell at 6)
```

### 46. Climbing Stairs

**Problem:** Count ways to climb n stairs (1 or 2 steps at a time).

**Solution:**
```javascript
// Time: O(n), Space: O(1)
function climbStairs(n) {
    if (n <= 2) return n;
    
    let first = 1, second = 2;
    
    for (let i = 3; i <= n; i++) {
        const third = first + second;
        first = second;
        second = third;
    }
    
    return second;
}

// Example
climbStairs(5); // 8
```

### 47. House Robber

**Problem:** Maximum money that can be robbed without robbing adjacent houses.

**Solution:**
```javascript
// Time: O(n), Space: O(1)
function rob(nums) {
    if (nums.length === 0) return 0;
    if (nums.length === 1) return nums[0];
    
    let prev2 = 0, prev1 = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        const current = Math.max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = current;
    }
    
    return prev1;
}

// Example
rob([2,7,9,3,1]); // 12 (rob houses 0, 2, 4)
```

### 48. Valid Parentheses

**Problem:** Check if parentheses are valid.

**Solution:**
```javascript
// Time: O(n), Space: O(n)
function isValid(s) {
    const stack = [];
    const map = {
        ')': '(',
        '}': '{',
        ']': '['
    };
    
    for (let char of s) {
        if (char === '(' || char === '{' || char === '[') {
            stack.push(char);
        } else {
            if (stack.length === 0 || stack.pop() !== map[char]) {
                return false;
            }
        }
    }
    
    return stack.length === 0;
}

// Example
isValid("()[]{}"); // true
isValid("([)]"); // false
```

### 49. Generate Parentheses

**Problem:** Generate all valid parentheses combinations with n pairs.

**Solution:**
```javascript
// Time: O(4^n / sqrt(n)), Space: O(n)
function generateParenthesis(n) {
    const result = [];
    
    function backtrack(current, open, close) {
        if (current.length === 2 * n) {
            result.push(current);
            return;
        }
        
        if (open < n) {
            backtrack(current + '(', open + 1, close);
        }
        
        if (close < open) {
            backtrack(current + ')', open, close + 1);
        }
    }
    
    backtrack('', 0, 0);
    return result;
}

// Example
generateParenthesis(3); // ["((()))","(()())","(())()","()(())","()()()"]
```

### 50. Letter Combinations of Phone Number

**Problem:** Generate all letter combinations from phone number digits.

**Solution:**
```javascript
// Time: O(4^n), Space: O(n)
function letterCombinations(digits) {
    if (digits.length === 0) return [];
    
    const map = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    };
    
    const result = [];
    
    function backtrack(index, current) {
        if (index === digits.length) {
            result.push(current);
            return;
        }
        
        const letters = map[digits[index]];
        for (let letter of letters) {
            backtrack(index + 1, current + letter);
        }
    }
    
    backtrack(0, '');
    return result;
}

// Example
letterCombinations("23"); // ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

### 51. Combination Sum

**Problem:** Find all unique combinations that sum to target (can reuse numbers).

**Solution:**
```javascript
// Time: O(2^n), Space: O(target)
function combinationSum(candidates, target) {
    const result = [];
    
    function backtrack(start, current, sum) {
        if (sum === target) {
            result.push([...current]);
            return;
        }
        
        if (sum > target) return;
        
        for (let i = start; i < candidates.length; i++) {
            current.push(candidates[i]);
            backtrack(i, current, sum + candidates[i]);
            current.pop();
        }
    }
    
    backtrack(0, [], 0);
    return result;
}

// Example
combinationSum([2,3,6,7], 7); // [[2,2,3],[7]]
```

### 52. Permutations

**Problem:** Generate all permutations of array.

**Solution:**
```javascript
// Time: O(n! * n), Space: O(n)
function permute(nums) {
    const result = [];
    
    function backtrack(current) {
        if (current.length === nums.length) {
            result.push([...current]);
            return;
        }
        
        for (let num of nums) {
            if (!current.includes(num)) {
                current.push(num);
                backtrack(current);
                current.pop();
            }
        }
    }
    
    backtrack([]);
    return result;
}

// Example
permute([1,2,3]); // [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### 53. Subsets

**Problem:** Generate all subsets of array.

**Solution:**
```javascript
// Time: O(2^n), Space: O(n)
function subsets(nums) {
    const result = [];
    
    function backtrack(start, current) {
        result.push([...current]);
        
        for (let i = start; i < nums.length; i++) {
            current.push(nums[i]);
            backtrack(i + 1, current);
            current.pop();
        }
    }
    
    backtrack(0, []);
    return result;
}

// Example
subsets([1,2,3]); // [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

### 54. Word Search

**Problem:** Check if word exists in 2D board (adjacent cells).

**Solution:**
```javascript
// Time: O(m * n * 4^L), Space: O(L)
function exist(board, word) {
    const rows = board.length;
    const cols = board[0].length;
    
    function dfs(row, col, index) {
        if (index === word.length) return true;
        if (row < 0 || row >= rows || col < 0 || col >= cols) return false;
        if (board[row][col] !== word[index]) return false;
        
        const temp = board[row][col];
        board[row][col] = '#'; // Mark as visited
        
        const found = dfs(row + 1, col, index + 1) ||
                     dfs(row - 1, col, index + 1) ||
                     dfs(row, col + 1, index + 1) ||
                     dfs(row, col - 1, index + 1);
        
        board[row][col] = temp; // Restore
        return found;
    }
    
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (dfs(i, j, 0)) return true;
        }
    }
    
    return false;
}
```

### 55. Number of Islands

**Problem:** Count number of islands (connected '1's) in 2D grid.

**Solution:**
```javascript
// Time: O(m * n), Space: O(m * n)
function numIslands(grid) {
    if (!grid || grid.length === 0) return 0;
    
    const rows = grid.length;
    const cols = grid[0].length;
    let count = 0;
    
    function dfs(row, col) {
        if (row < 0 || row >= rows || col < 0 || col >= cols) return;
        if (grid[row][col] === '0') return;
        
        grid[row][col] = '0'; // Mark as visited
        
        dfs(row + 1, col);
        dfs(row - 1, col);
        dfs(row, col + 1);
        dfs(row, col - 1);
    }
    
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (grid[i][j] === '1') {
                count++;
                dfs(i, j);
            }
        }
    }
    
    return count;
}
```

### 56. Course Schedule

**Problem:** Check if all courses can be finished (detect cycle in graph).

**Solution:**
```javascript
// Time: O(V + E), Space: O(V)
function canFinish(numCourses, prerequisites) {
    const graph = Array(numCourses).fill(0).map(() => []);
    const visited = Array(numCourses).fill(0); // 0: unvisited, 1: visiting, 2: visited
    
    for (let [course, prereq] of prerequisites) {
        graph[prereq].push(course);
    }
    
    function hasCycle(course) {
        if (visited[course] === 1) return true; // Cycle detected
        if (visited[course] === 2) return false; // Already processed
        
        visited[course] = 1; // Mark as visiting
        
        for (let next of graph[course]) {
            if (hasCycle(next)) return true;
        }
        
        visited[course] = 2; // Mark as visited
        return false;
    }
    
    for (let i = 0; i < numCourses; i++) {
        if (hasCycle(i)) return false;
    }
    
    return true;
}
```

### 57. Longest Increasing Subsequence

**Problem:** Find length of longest increasing subsequence.

**Solution:**
```javascript
// Time: O(n log n), Space: O(n)
function lengthOfLIS(nums) {
    const tails = [];
    
    for (let num of nums) {
        let left = 0, right = tails.length;
        
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (tails[mid] < num) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        if (left === tails.length) {
            tails.push(num);
        } else {
            tails[left] = num;
        }
    }
    
    return tails.length;
}

// Example
lengthOfLIS([10,9,2,5,3,7,101,18]); // 4
```

### 58. Coin Change

**Problem:** Find minimum coins needed to make amount.

**Solution:**
```javascript
// Time: O(amount * coins), Space: O(amount)
function coinChange(coins, amount) {
    const dp = Array(amount + 1).fill(Infinity);
    dp[0] = 0;
    
    for (let i = 1; i <= amount; i++) {
        for (let coin of coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    return dp[amount] === Infinity ? -1 : dp[amount];
}

// Example
coinChange([1,2,5], 11); // 3 (5 + 5 + 1)
```

### 59. Edit Distance

**Problem:** Find minimum operations to convert word1 to word2.

**Solution:**
```javascript
// Time: O(m * n), Space: O(m * n)
function minDistance(word1, word2) {
    const m = word1.length;
    const n = word2.length;
    const dp = Array(m + 1).fill(0).map(() => Array(n + 1).fill(0));
    
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (word1[i - 1] === word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + Math.min(
                    dp[i - 1][j],     // Delete
                    dp[i][j - 1],     // Insert
                    dp[i - 1][j - 1]  // Replace
                );
            }
        }
    }
    
    return dp[m][n];
}
```

### 60. Maximum Subarray (Kadane's Algorithm)

**Problem:** Find maximum sum of contiguous subarray.

**Solution:**
```javascript
// Time: O(n), Space: O(1)
function maxSubArray(nums) {
    let maxSum = nums[0];
    let currentSum = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    
    return maxSum;
}

// Example
maxSubArray([-2,1,-3,4,-1,2,1,-5,4]); // 6 ([4,-1,2,1])
```

---

This covers problem-solving and algorithm questions from beginner to advanced level with solutions and explanations.

