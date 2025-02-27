Title: Weekly Contest 388 周赛题目解析
Slug: weekly-388
Date: 2024-03-12 22:00
Category: Leetcode
Tags: Contest
Status: draft
Summary: 2024-03 Leetcode Weekly Contest 388 第 388 场力扣周赛 | 3069. Distribute Elements Into Two Arrays I 将元素分配到两个数组中 I | 3070. Count Submatrices with Top-Left Element and Sum Less Than k 元素和小于等于 k 的子矩阵的数目 | 3071. Minimum Operations to Write the Letter Y on a Grid 在矩阵上写出字母 Y 所需的最少操作次数 | 3072. Distribute Elements Into Two Arrays II 将元素分配到两个数组中 II | Solution to contest problems 赛题讲解

[Weekly Contest 388](https://leetcode.com/contest/weekly-contest-388/)

[第 388 场周赛](https://leetcode.cn/contest/weekly-contest-388/)


## 题目列表

- [3074. Apple Redistribution into Boxes 重新分装苹果](https://leetcode.com/problems/apple-redistribution-into-boxes/description/)
- [3075. Maximize Happiness of Selected Children 幸福值最大化的选择方案](https://leetcode.com/problems/maximize-happiness-of-selected-children/description/)
- [3076. Shortest Uncommon Substring in an Array 数组中的最短非公共子字符串](https://leetcode.com/problems/shortest-uncommon-substring-in-an-array/description/)
- [3077. Maximum Strength of K Disjoint Subarrays K 个不相交子数组的最大能量值](https://leetcode.com/problems/maximum-strength-of-k-disjoint-subarrays/)

## 3074. Apple Redistribution into Boxes 重新分装苹果

按照题意模拟即可。

```python
class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        capacity.sort(reverse=True)
        
        total = sum(apple)
        
        i = 0
        while total > 0:
            total -= capacity[i]
            i += 1
        
        return i 
```

## 3075. Maximize Happiness of Selected Children 幸福值最大化的选择方案

排序后依次求和即可。要注意的是，这里最小值不为负数，因此有个`max`。

```python
class Solution:
    def maximumHappinessSum(self, happiness: List[int], k: int) -> int:
        happiness.sort(reverse=True)
        
        
        for i in range(k):
            happiness[i] = max(happiness[i] - i, 0)
        
        return sum(happiness[:k])
```

## 3076. Shortest Uncommon Substring in an Array 数组中的最短非公共子字符串

给定长度为`n`的非空字符串数组`arr`。对于每个字符串`arr[i]`，找到其中最短的连续子字符串，使得这个子字符串不在除`arr[i]`以外的其他字符串。若所有都存在，则答案为空。要求返回长度为`n`的字符串数组`answer`。

由于最多只有100个字符串，每个字符串长度为20，最多也就`(20 * 19 // 2) * 100 = 19000`个子字符串，因此直接遍历求出每个子字符串的可能性，并与其他比对即可。这里用了`set`来减少时间复杂度。

```python
class Solution:
    def shortestSubstrings(self, arr: List[str]) -> List[str]:
        substrings = []
        
        for s in arr:
            ss = set()
            for l in range(1, len(s)+1):
                for i in range(l):
                    ss.add(s[i:l])
            substrings.append(ss)
        # print(substrings)
        result = []
        for i, ss in enumerate(substrings):
            
            candidates = set(ss)
            
            for j in range(len(substrings)):
                if i == j:
                    continue
                candidates -= substrings[j]
                if not candidates:
                    break
            
            if not candidates:
                result.append("")
                continue
            
            candidates = sorted(list(candidates), key = lambda x: (len(x), x))
            result.append(candidates[0])
        
        return result
```

当然，这道题也可以使用Trie来做。

```python
class TrieNode:
    def __init__(self):
        self.c = {}  # children
        self.wi = set()  # word index

    def add(self, c, idx):
        if c not in self.c:
            self.c[c] = TrieNode()
        node = self.c[c]
        node.wi.add(idx)

        return node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, idx):
        for i in range(len(word)):
            node = self.root
            for j in range(i, len(word)):
                node = node.add(word[j], idx)

        # print(self.root.c)

    def find(self, word):
        result = len(word) + 1
        left = -1
        right = -1

        for i in range(len(word)):
            node = self.root
            for j in range(i, len(word)):
                node = node.c[word[j]]
                if len(node.wi) == 1 and ((j - i + 1) < result or ((j - i + 1) == result and word[i:j+1] < word[left:right+1])):
                    result = (j - i + 1)
                    left = i
                    right = j

        if left == -1:
            return ""

        return word[left:right+1]


class Solution:
    def shortestSubstrings(self, arr: List[str]) -> List[str]:
        trie = Trie()
        for i, s in enumerate(arr):
            trie.insert(s, i)

        result = []
        for s in arr:
            result.append(trie.find(s))

        return result
```


## 3077. Maximum Strength of K Disjoint Subarrays K 个不相交子数组的最大能量值




```python
```