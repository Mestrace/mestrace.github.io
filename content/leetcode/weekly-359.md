Title: Weekly Contest 359 周赛题目解析
Slug: weekly-359
Date: 2023-08-31
Category: Leetcode
Tags: Contest
Summary: 2023-08 Leetcode Weekly Contest 359 第 359 场力扣周赛 | 2815. Max Pair Sum in an Array 数组中的最大数对和 | 2816. Double a Number Represented as a Linked List 翻倍以链表形式表示的数字 | 2817. Minimum Absolute Difference Between Elements With Constraint 限制条件下元素之间的最小绝对差 | 2818. Apply Operations to Maximize Score 操作使得分最大 | Solution to contest problems 赛题讲解

[Weekly Contest 359](https://leetcode.com/contest/weekly-contest-359/)

[第 359 场周赛](https://leetcode.cn/contest/weekly-contest-359/)

## 题目列表

- [2828. Check if a String Is an Acronym of Words 判别首字母缩略词](https://leetcode.com/problems/check-if-a-string-is-an-acronym-of-words/)
- [2829. Determine the Minimum Sum of a k-avoiding Array k-avoiding 数组的最小总和](https://leetcode.com/problems/determine-the-minimum-sum-of-a-k-avoiding-array/)
- [2830. Maximize the Profit as the Salesman 销售利润最大化](https://leetcode.com/problems/maximize-the-profit-as-the-salesman/)
- [2831. Find the Longest Equal Subarray 找出最长等值子数组](https://leetcode.com/problems/find-the-longest-equal-subarray/)

## 2828. Check if a String Is an Acronym of Words 判别首字母缩略词

按照题意模拟即可。

```python
class Solution:
    def isAcronym(self, words: List[str], s: str) -> bool:
        d = "".join([w[0] for w in words])
        
        return d == s
```

## 2829. Determine the Minimum Sum of a k-avoiding Array k-avoiding 数组的最小总和

给定两个整数`n`和`k`，要求求出长度为`n`且没有任意一对元素的和为`k`的数组的最小的和是多少。

反向的`2sum`，用一个hashset维护已经有的数字来确保不存在和为`k`的对。

```python
class Solution:
    def minimumSum(self, n: int, k: int) -> int:
        s = set()
        
        for i in range(1, 2 * max(k, n)):
            if len(s) == n:
                break
            if (k - i) not in s:
                s.add(i)
        # print(s)
        return sum(s)
```

## 2830. Maximize the Profit as the Salesman 销售利润最大化

给定一个正整数`n`代表`[0,n-1]`个房子，给定一个列表的`offers`，其中每个`offers[i] = [start, end, gold]`代表着第`i`位买家要买的房子区间`[start, end]`和他愿意支付的价格`gold`，你需要找到最多能获得多少钱。

这是一道时间窗口的题目，具体体现在他的排他性上。假如买家`i`以`gold`价格购买了`[start, end]`的房子，那么其他买家就不能购买了。我们首先应该想到按照开始时间排序，因为只有邻近的`offer`才会互相干涉。在我们看到每一个`offer`时，我们的决策是是否选择这个`offer`

1. 选择这个offer并获得对应的收益，移动到下一个可能的offer
2. 跳过这个offer以期望后面的offer能获得更大的收益。

这里我们自然而然的想到了`dp`，因为我们不可避免的需要对很多重复的子问题求解。此外，移动到下一个offer时我们还可以利用上面的排他性，使用二分法快速跳到下一个可能的offer。

```python
class Solution:
    def maximizeTheProfit(self, n: int, offers: List[List[int]]) -> int:
        offers.sort(key=lambda x: x[0])  # Sort the offers based on the start index
        
        from functools import cache
        
        # Create a list of offer start indices for binary search
        offer_start_indices = [offer[0] for offer in offers]
        
        @cache
        def dp(o):
            if o >= len(offers):
                return 0
            
            start, end, gold = offers[o]
            
            # Binary search to find the next valid offer index
            next_offer_idx = bisect_right(offer_start_indices, end)
            
            # Case 1: Do not consider the current offer, move to the next offer
            result = dp(o + 1)
            
            # Case 2: Consider the current offer if it's within the range of houses
            result = max(result, gold + dp(next_offer_idx))
            
            return result
        
        return dp(0)
```

## 2831. Find the Longest Equal Subarray 找出最长等值子数组

给定一个正整数数组`nums`和正整数`k`，你最多可以在`nums`中删除`k`个数字，要求求出最长能够形成的连续相同数字。

光看前面的描述，这个问题还是蛮唬人的，但是实际上并没有那么难。我们先来解决一个简化版的问题。若我们知道我们要通过在`nums`中删除至多`k`个元素来构造所有元素都是`e`的子数组，这道问题就变得相当的容易。我们只需要维护左右指针表示我们当前囊括的元素，及中间有多少个删除的非`e`的元素。我们持续移动右指针，直到中间删除的元素大于`k`，这时候我们移动左边来恢复一些删除元素。怎么样，非常简单吧。

那么，我们怎么从原题构造这道简单的双指针题目呢？假如我们能够分个类的话，我们就有我们要尝试构造的元素`e`的列表了。所以我们可以遍历整个`nums`，并按照值分类储存每个元素的索引。此外，还有一个简单的优化点是基于索引区间来保存元素，这样在重复元素较多的情况下可以尽可能地减少空间利用。


```python
class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        e = defaultdict(list)
        
        for i, n in enumerate(nums):
            if e[n] and e[n][-1][-1] == i:
                e[n][-1][-1] = i + 1
            else:
                e[n].append([i, i + 1])

        
        result = 0
        
        for element, ranges in e.items():
            # print(element, ranges)
            left = 0
            sz = 0 # size of elements
            gap = 0 # current gap
            for right in range(len(ranges)):
                sz += ranges[right][1] - ranges[right][0]
                if right > 0:
                    gap += ranges[right][0] - ranges[right - 1][1]
                
                while left < right and gap > k:
                    sz -= ranges[left][1] - ranges[left][0]
                    gap -= ranges[left + 1][0] - ranges[left][1]
                    left += 1
                
                # print(left, right, sz, gap)
                
                result = max(result, sz)
        
        return result
```