Title: 【Leetcode题解】2599. Make the Prefix Sum Non-negative
Slug: 2599-make-the-prefix-sum-non-negative
Date: 2023-03-23
Category: Leetcode
Summary: Leetcode 2599 Make the Prefix Sum Non-negative My Solution 我的解题思路。这道题主要用贪心算法(greedy)和最小堆(min-heap)结合起来去求解。

## 题目

[题目链接](https://leetcode.com/problems/make-the-prefix-sum-non-negative/)

给定数组`nums`，允许把这个数组里任意的数字移动到数组最后，我们能够把这个操作进行任意次，使得这个数组的前缀和（prefix sum）都为非负整数。找到最少的操作次数。此外，给定的测试样例一定存在解。

## 分析

初看到的时候，我也没有什么特别好的思路，所以就从例子入手去看看。
```text
Input: nums = [3, -5, -4, 7]
Output: 2
Explanation:
Prefix sums
0 - [3, -2, -6, 1]
1 - [3, -1, 6, 1] (Move -5 to the back)
2 - [3, 10, 5, 1] (Move -4 to the back)
```

上面那个例子我们可以看到，当我们移动第`i`个数字到数组末尾的时候，前缀和里面`[i, n - 1]`区间都会发生变化。此外，我们还可以观察到，要求最少的移动次数的话，非负整数是不需要移动的，只有负数会影响我们的结果。而且，维护一个前缀和来求解的话时间复杂度有点高，所以这个思路暂时不采纳。

那么，另一个思路就来了。我们可以贪心的把数字移动到末尾，仅当我们发现当前前缀加上当前数字小于0的时候。伪代码大概长这样
```text
prefix = 0
for n in range nums:
    if prefix + n < 0:
        move n to the back
        continue
    prefix += n
```
这样的方法虽然是能求出解的，但并不是最优的。让我们来看一个例子
```
Input: nums = [6, -6, -3, -3, 1]
Output: 1
```
在这个例子中，我们发现我们的算法会吞掉这个`-6`，但是把两个`-3`移到末尾去。所以显而易见的，如果能移动的话，我们要尽可能的移动更小的负数，而不是像上面那段伪代码一样，只有当`prefix + n`小于0的时候才移动。那么到这里，答案基本就呼之欲出了。

## 代码

我们用了一个最小堆min-heap来包括当前看到的所有的负数，每当我们发现当前前缀和已经小于0的时候，我们就把最小的那个负数移动到末尾去。

```python
from heapq import heappush, heappop

class Solution:
    def makePrefSumNonNegative(self, nums: List[int]) -> int:
        result = 0
        prefix = 0
        h = []

        for n in nums:
            prefix += n
            if n > 0:
                continue
            heappush(h, n)
            if prefix < 0:
                result += 1
                neg = heappop(h)
                prefix -= neg
        
        return result
```

## 总结

这道题整体难度不算很高，但是设计的挺巧妙，还是需要一些推导过程才能做出来。

如果你想变得更强的话，可以做做

1. [Medium - 1642. Furthest Building You Can Reach](https://leetcode.com/problems/furthest-building-you-can-reach/)
1. [Medium - 2512. Reward Top K Students](https://leetcode.com/problems/reward-top-k-students/)
1. [Medium - 2462. Total Cost to Hire K Workers](https://leetcode.com/problems/total-cost-to-hire-k-workers/)
1. [Hard - 2551. Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags/)