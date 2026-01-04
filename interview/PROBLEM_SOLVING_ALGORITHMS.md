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

---

This covers problem-solving and algorithm questions from beginner to advanced level with solutions and explanations.

