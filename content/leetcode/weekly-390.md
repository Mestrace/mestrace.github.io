Title: Weekly Contest 390 周赛题目解析
Slug: weekly-390
Date: 2024-03-24 22:00
Category: Leetcode
Tags: Contest
Summary: 2024-03 Leetcode Weekly Contest 390 第 390 场力扣周赛 | 3090. Maximum Length Substring With Two Occurrences 每个字符最多出现两次的最长子字符串 | 3091. Apply Operations to Make Sum of Array Greater Than or Equal to k 执行操作使数据元素之和大于等于 K | 3092. Most Frequent IDs 最高频率的 ID | 3093. Longest Common Suffix Queries 最长公共后缀查询 | Solution to contest problems 赛题讲解 | Trie 前缀树

[Weekly Contest 390](https://leetcode.com/contest/weekly-contest-390/)

[第 390 场周赛](https://leetcode.cn/contest/weekly-contest-390/)

## 题目列表

- [3090. Maximum Length Substring With Two Occurrences 每个字符最多出现两次的最长子字符串](https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/)
- [3091. Apply Operations to Make Sum of Array Greater Than or Equal to k 执行操作使数据元素之和大于等于 K](https://leetcode.com/problems/apply-operations-to-make-sum-of-array-greater-than-or-equal-to-k/)
- [3092. Most Frequent IDs 最高频率的 ID](https://leetcode.com/problems/most-frequent-ids/)
- [3093. Longest Common Suffix Queries 最长公共后缀查询](https://leetcode.com/problems/longest-common-suffix-queries/)

## 3090. Maximum Length Substring With Two Occurrences 每个字符最多出现两次的最长子字符串

使用双指针排除掉出现次数大于`2`的字母即可。

```python
class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        left = 0
        
        result = 0
        m = defaultdict(int)
        
        for right in range(len(s)):
            m[s[right]] += 1
            while left < right and m[s[right]] > 2:
                m[s[left]] -= 1
                left += 1
            result = max(result, right - left + 1)

        return result
```

## 3091. Apply Operations to Make Sum of Array Greater Than or Equal to k 执行操作使数据元素之和大于等于 K

假设有初始数组`nums = [1]`，你可以将数组中的某个数字加一或者减一，也可以将其复制一份并添加到数组末尾。问最少需要操作多少次使得`nums`的和大于给定值`k`。

显然，复制是更快的选项。不难看出，我们总可以先将初始数字加`n`次之后，复制`m`次，最终使得结果大于或者等于`k`。因此直接暴力计算。

```python
class Solution:
    def minOperations(self, k: int) -> int:
        # only the max element matters right?
        result = k - 1
        
        curr = 1
        
        while curr - 1 < result:
            if k % curr != 0:
                result = min(result, (curr - 1) + k // curr)
            else:
                result = min(result, (curr - 1) + k // curr - 1)
            curr += 1
        
        return result
```

通过对上面的方法进行分析，我们可以得出结论是，最快的方式是加到`sqrt(k)`然后再进行复制，因此我们有以下解法。

```python
class Solution:
    def minOperations(self, k: int) -> int:
        from math import ceil, sqrt
        m = ceil(sqrt(k))
        return m - 1 + (k - 1) // m
```

## 3092. Most Frequent IDs 最高频率的 ID

给定长度为`n`的数组`nums`和`freq`，其中每一对`nums[i], freq[i]`表示在`i`时刻ID为`nums[i]`的纪录出现次数的变化（可能为加或者减）。返回一个数组使得这个数组第`i`个值为在时刻`i`出现频率最高的ID。

我们需要变化的进行统计数组中出现频率最高的数组，因此我们考虑用一个排序的数据结构解决问题。有了这个数组，本题的其他部分就是对于逻辑的模拟。这里我们直接采用了SortedDict的排序树状哈希表来处理。

```python
class Solution:
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        from sortedcontainers import SortedDict
        
        f = defaultdict(int)
        d = SortedDict()
        
        n = len(nums)
        result = []
        for i in range(n):
            old_freq = f[nums[i]]
            f[nums[i]] += freq[i]
            new_freq = f[nums[i]]
            
            if old_freq > 0:
                d[old_freq] -= 1
                if d[old_freq] == 0:
                    del d[old_freq]
            
            if new_freq > 0:
                if new_freq not in d:
                    d[new_freq] = 1
                else:
                    d[new_freq] += 1
            
            if not d:
                result.append(0)
            else:
                result.append(d.peekitem(-1)[0])
        
        return result
```

## 3093. Longest Common Suffix Queries 最长公共后缀查询

用Trie一把梭就可以AC。

```python
class TrieNode:
    def __init__(self, c, idx):
        self.char = c
        self.children = {}
        self.index = idx

class Solution:
    def stringIndices(self, wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:        
        trie = TrieNode("*", 0)
        # Build the trie with wordsContainer
        for i, word in enumerate(wordsContainer):
            current = trie
            if len(word) < len(wordsContainer[current.index]) :
                current.index = i
            
            for char in word[::-1]:
                if char not in current.children:
                    current.children[char] = TrieNode(char, i)
                current = current.children[char]
                
                if len(word) < len(wordsContainer[current.index]):
                    current.index = i

        ans = []
        for query in wordsQuery:
            current = trie
            for i, char in enumerate(query[::-1]):
                if char not in current.children:
                    break  # No common suffix found, move to next query
                current = current.children[char]
            
            # print(current.char, current.index)
            ans.append(current.index)

        return ans
```