Title: Weekly Contest 399 周赛题目解析
Slug: weekly-399
Date: 2024-06-17 13:11
Category: Leetcode
Tags: Contest
Summary: 2024-06 Leetcode Weekly Contest 399 第 399 场力扣周赛 | Solution to contest problems 赛题讲解

[Weekly Contest 399](https://leetcode.com/contest/weekly-contest-399/)

[第 399 场周赛](https://leetcode.cn/contest/weekly-contest-399/)


## 题目列表

- [3162. Find the Number of Good Pairs I 优质数对的总数 I](https://leetcode.com/problems/find-the-number-of-good-pairs-i/description/)
- [3163. String Compression III 压缩字符串 III](https://leetcode.com/problems/string-compression-iii/)
- [3164. Find the Number of Good Pairs II 优质数对的总数 II](https://leetcode.com/problems/find-the-number-of-good-pairs-ii/)
- [3165. Maximum Sum of Subsequence With Non-adjacent Elements 不包含相邻元素的子序列的最大和](https://leetcode.com/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/description/)


## 3162. Find the Number of Good Pairs I 优质数对的总数 I

给定数组`nums1`和`nums2`和整数`k`，定义好数对为`(i,j)`使得`nums1[i]`整除`nums2[j] * k`，找到所有好数对的数量。

由于取值范围较小，我们直接`O(n^2)`暴力计算即可。

```python
class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        result = 0
        for i in nums1:
            for j in nums2:
                if i % (j * k) == 0:
                    result += 1
        
        return result
```

## 3163. String Compression III 压缩字符串 III

定义压缩算法为将最多`9`个连续字符压缩为数字前缀与字母后缀的字符串，给定字符`word`，将其进行压缩并返回最终的压缩字符串。

按照题意模拟即可。

```python
class Solution:
    def compressedString(self, word: str) -> str:
        ns = []
        
        c = None
        cnt = 0
        
        def append_reset():
            nonlocal c
            nonlocal cnt
            if c != None:
                ns.append(str(cnt))
                ns.append(c)
            c = None
            cnt = 0
        
        for w in word:
            if c == None or w == c:
                c = w
                cnt += 1
                if cnt == 9:
                    append_reset()
            elif w != c:
                append_reset()
                c = w
                cnt = 1
        append_reset()
        
        return ''.join(ns)
```

## 3164. Find the Number of Good Pairs II 优质数对的总数 II

第三题题目与第一题一样，只是数据范围增加，因此不多赘述。

若`nums1[i]`可以被`nums2[j] * k`整除，那么`nums2[j] * k`一定是`nums[i]`的一个因数。在数据范围内，我们可以在常数范围内求得`nums1`的因数。此题的解法呼之欲出。即我们对于球的`nums1`中每一个数求所有的因数，再用`nums2[j] * k`进行搜索即可。

```python
import math

def find_factors(n):
    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return factors


class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        # find all prime factors?
        d = defaultdict(int)
        for n in nums1:
            for f in find_factors(n):
                d[f] += 1
        
        result = 0
        for n in nums2:
            result += d[n * k]
        return result
```

## 3165. Maximum Sum of Subsequence With Non-adjacent Elements 不包含相邻元素的子序列的最大和

这题暂时不会做了，之后补充吧。