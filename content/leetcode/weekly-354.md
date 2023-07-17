Title: Weekly Contest 354 周赛题目解析
Slug: weekly-354
Date: 2023-07-18 01:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 354 第 354 场力扣周赛 | 2778. Sum of Squares of Special Elements 特殊元素平方和 | 2779. Maximum Beauty of an Array After Applying Operation 数组的最大美丽值 | 2780. Minimum Index of a Valid Split 合法分割的最小下标 | 2781. Length of the Longest Valid Substring 最长合法子字符串的长度 | Solution to contest problems 赛题讲解 | 字典树 Trie 

[Weekly Contest 354](https://leetcode.com/contest/weekly-contest-354/)

[第 354 场周赛](https://leetcode.cn/contest/weekly-contest-354/)

题目描述又不讲人话了。最后一题在寓教于乐的路上越走越远了，难度不高但是技巧不少。

## 题目列表

- [2778. Sum of Squares of Special Elements 特殊元素平方和](https://leetcode.com/problems/sum-of-squares-of-special-elements/)
- [2779. Maximum Beauty of an Array After Applying Operation 数组的最大美丽值](https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/)
- [2780. Minimum Index of a Valid Split 合法分割的最小下标](https://leetcode.com/problems/minimum-index-of-a-valid-split/)
- [2781. Length of the Longest Valid Substring 最长合法子字符串的长度](https://leetcode.com/problems/length-of-the-longest-valid-substring/description/)

## 2778. Sum of Squares of Special Elements 特殊元素平方和

按照题意模拟即可。

```python
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        result = 0
        for i in range(1, len(nums) + 1):
            if len(nums) % (i) == 0:
                result += nums[i - 1] * nums[i - 1]
        
        return result
```

## 2779. Maximum Beauty of an Array After Applying Operation 数组的最大美丽值

给定数字列表`nums`和非负整数`k`，我们可以把`nums`每个位置的数字`nums[i]`替换成`[nums[i] - k, nums[i] + k]`区间的任意数字，每个数字智能执行一次这个操作。求最终达到的所有数字都相同的子数组的长度（不要求连续子数组）。

题目的描述有点让人困惑。实际上不要求连续子数组这个条件只是个陷阱，这意味着我们可以重新排列整个数组。因此直接排序后左右搜索上下界，在上下界之间的数字就可以变成同一个数字。

```python
class Solution:
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        from bisect import bisect_left, bisect_right
        nums.sort()
        result = 1
        for v in range(max(nums) + 1):
            lb = bisect_left(nums, v - k)
            ub = bisect_right(nums, v + k)
            
            # print(lb, ub)
            
            result = max(result, ub - lb)
        
        return result
```

## 2780. Minimum Index of a Valid Split 合法分割的最小下标

给定一个数组`arr`，其中总会存在一个主要元素(dominant)`m`。主要元素的定义为`m`的出现频率`freq(m) * 2 > len(arr)`。我们需要把这个数组分割成左右两个数组，且左右数组的主要元素仍然为`m`，并返回最小的分割点`i`。若没法进行分割的话，返回`-1`。

难度不高，直接算左右两边的主要元素，并根据定义判断，遍历所有的点即可。

```python
from typing import List
from collections import Counter

class Solution:
    def minimumIndex(self, nums: List[int]) -> int:
        counter = Counter(nums)
        
        dominant_element = max(counter, key=counter.get)
        
        print("dominant", dominant_element)
        
        # Iterate over the array, keep track of cumulative count and look for valid split index
        left_count = 0
        for i in range(len(nums)):
            if nums[i] == dominant_element:
                left_count += 1
                
            right_count = counter[dominant_element] - left_count
            
            # Check if the split is valid
            # print(left_count, i + 1, right_count, len(nums) - i - 1)
            if left_count * 2 > (i + 1) and right_count * 2 > (len(nums) - i - 1) and right_count > 0:
                return i
            
        return -1
```

## 2781. Length of the Longest Valid Substring 最长合法子字符串的长度

给定一个字符串`word`和一个列表的字符串`forbidden`，其中`forbidden`代表的是禁止出现的短语，要求`word`里不包含禁止出现的短语的最长连续子串的长度。为了让大家轻松一点，题目还设定了只会出现小写字母。此外，禁止词列表里的长度也不会超过10。

首先对于匹配连续子串的题目，除了复杂得要了命的Knuth-Morris-Pratt（KMP）算法之外，我们首先应该想到的就是Trie。而且这道题刚好符合字典树Trie的性质。如果存在多个禁止词的前缀是一样的话，我们就不必每个都存，只要存相同前缀就可以了。

首先来回顾一下Trie的性质：

1. Trie是一个多叉树，其中每一个节点都代表一个字符，最终形成一个字典，可以让我们快速匹配某个字符串是否存在。
2. 在遍历的时候，每次移动一个字符，我们都匹配当前字符是否在当前子树的子节点里面，若是则移动，否则这个词就不存在。

接着我们来看看怎么解决这个问题。对于子串来说，最好就是用双指针去找。那么我们就要考虑如何移动两个指针。通常情况下，右指针持续向右移动。在这一题里面，还需要推动Trie中的节点指针往下走进行匹配。左节点的移动就比较困难了，分为两种情况：若右指针移动后匹配到了禁止词，那么就需要移动到右指针 + 1的位置；否则的话，左指针不用移动。我们用一个例子来演示一下

```text
Example 1
Input: word = "cba", forbidden = ["cb"]
Output: 2
Explanation:
trie: "c" -> "b"
left = 0, right = 0, 
    current_word = "c", trie_pointer = "c"
    => current_size = 1
left = 0, right = 1, 
    current_word = "cb", trie_pointer = "b",
    => left = 1
left = 1, right = 1
    current_word = "b", trie_pointer = None
    => current_size = 1
left = 1, right = 2
    current_word = "ba", trie_pointer = None
    => current_size = 2
```

这样就能解决问题了吗？我们再来看一个例子。

```text
Example 2
Input: word = "bcbab", forbidden = ["cba", "bcbc"]
Output: 3
```

如果用我们上面讲的算法来看，我们的`trie_pointer`会沿着`"bcbc"`这条路径走，但是发现没有，因此会输出`5`。但是实际上，中间有一个`"cba"`也是禁止词被放过去了。因此，我们要考虑是不是能够把所有中间的指针都存进去，即当我们匹配的时候，我们会尝试推动一个列表的`trie_poiner`指针，而不是只考虑当前的。还是上面那个例子

```
Example 2 Cont.
Explanation
left = 0, right = 0
    trie_pointer_1 = "b"
left = 0, right = 1:
    trie_pointer_1 = "bc"
    trie_pointer_2 = "c"
left = 0, right = 2:
    trie_pointer_1 = "bcb"
    trie_pointer_2 = "cb"
    trie_pointer_3 = "b"
left = 0, right = 3:
    trie_pointer_1 = "bcba" => unmatched
    trie_pointer_2 = "cba" => matched, move left = 1
    trie_pointer_3 = "ba"
    trie_pointer_4 = "a"
Omitted...
```
可以看到，我们维护`[left, right]`之间开始的子字符串匹配到的Trie指针`trie_pointer_*`，每次都尝试推进所有的指针并检查是否匹配。这样就解决了第一版算法会因为提前匹配了别的禁止词而漏掉中间禁止词的问题。考虑到我们只有26个字母和长度为10的禁止词，储存所有的中间指针可以视为常数项，因此这个算法是ok的，我们来尝试实现一下。


```python
class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        TERM = '#' # terminator
        trie = dict()
        
        def build_trie(t, s):
            node = t
            for c in s:
                if c not in node:
                    node[c] = dict()
                node = node[c]
            # the forbidden word terminates here
            if TERM not in node:
                node[TERM] = TERM
        
        for f in forbidden:
            build_trie(trie, f)
        # print(trie)
        q = deque()

        left = 0
        right = 0
        result = 0
        while right < len(word):
            char = word[right]
            if char in trie:
                q.append((trie, right))

            sz = len(q)
            for _ in range(sz):
                node, start = q.popleft()
                if char in node:
                    node = node[char]
                    if TERM in node:
                        # print("found", word[left:right + 1], word[start:right + 1])
                        left = start + 1
                        right = start
                        q.clear() # empty the deque
                        break
                    else:
                        q.append((node, start))
            # print(q)

            result = max(result, right - left + 1)
            right += 1
        
        return result
```

对于Trie不熟悉的同学们，以下资料可能会有用

- [JHU - Tries and suffix tries - Ben Langmead](https://www.cs.jhu.edu/~langmea/resources/lecture_notes/tries_and_suffix_tries.pdf)
- [Medium - 208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)
- [Codeforces - How to represent a trie in a 2D array? - maximaxi](https://codeforces.com/blog/entry/50357) 普通的Trie基本上会使用数组指针或者哈希表来存子节点，这样内存访问较为离散，空间上不是特别理想，因此存在对于这种情况的优化，使用三数组或者双数组来进行存储。