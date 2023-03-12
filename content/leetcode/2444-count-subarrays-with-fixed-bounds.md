Title: 【Leetcode题解】2444. Count Subarrays With Fixed Bound
Slug: 2444-count-subarrays-with-fixed-bounds
Date: 2023-03-04
Category: Leetcode
Tags: Contest, Subarray

今天闲的无聊，找点事情做，来写一下[2444. Count Subarrays With Fixed Bound](https://leetcode.com/problems/count-subarrays-with-fixed-bounds/)的题解。

## 题目

You are given an integer array `nums` and two integers `minK` and `maxK`.

A **fixed-bound subarray** of `nums` is a subarray that satisfies the following conditions:

- The **minimum** value in the subarray is equal to `minK`.
- The **maximum** value in the subarray is equal to `maxK`.
Return the number of fixed-bound subarrays.

A subarray is a contiguous part of an array.

给定一个数字列表和一个最大值和一个最小值，找到所有区间满足最大值和最小值分别等于给定值的子数组的数量。

## 分析

这道题是2022.10.16的[周赛](https://leetcode.com/contest/weekly-contest-315/)题目。当时尝试用暴力dp的方式去解。思路是说用放宽约束条件的方式，去计算一个区间`[i,j]`内是否都是在`[minK, maxK]`内的数字，然后数一遍。果不其然TLE了。但今天不是周赛，我们有充足的时间去思考，别有太大压力。做这类数连续子数组类型的题目，首先看数据量。这道题数据量`10^5`，也就意味着我们要在`O(n)`的方式去解决，否则一定超时。因此，头脑里冒出来的第一个方式一定是双指针。

先解决核心问题。假设我们已经知道怎么移动指针，并找到了满足条件的区间`[i,j]`。也就是说`[i,j]`区间的最大值等于`maxK`，最小值等于`minK`。那么我们要怎么计算这个区间内的子数组数量呢？这就可以引导我们去找到另外两个变量，我们要知道区间`[i,j]`内的区间`[k,l]`，使得`nums[k]`和`nums[l]`分别等于最大值和最小值（或反过来）。这样的话我们就找到了我们需要的变量。

那么如何计算子数组的数量呢？我们先来看几个例子。

先来个基础的例子
```
Input: nums = [2,6], minK = 2, maxK = 6
Output: 1
```
我们尝试往里面加一个元素
```
Input: nums = [3,2,6], minK = 2, maxK = 6
Output: 2
Explanation: 
[2,6]
[3,2,6]
```
多加两个元素，我们有
```
Input: nums = [3,2,6,4,5], minK = 2, maxK = 6
Output: 6
Explanation: 
[2,6]
[3,2,6]
[2,6,4]
[3,2,6,4]
[2,6,4,5]
[3,2,6,4,5]
```
再增加一点难度，假设我们在区间内有多个符合条件的区间，这时候怎么办呢。
```
Input: nums = [3,2,6,4,2], minK = 2, maxK = 6
Output: 7
Explanation: 
Starting from [2,6]
[2,6]
[3,2,6]
[2,6,4]
[3,2,6,4]
Starting from [6,4,2]
[6,4,2]
[2,6,4,2]
[3,2,6,4,2]
```

因此，我们来总结一下规律。先说下我们已知的变量：`[i,j]`为整个区间，`[k,l]`为使得`nums[k]`和`nums[l]`分别等于最大值和最小值（或反过来)的区间，`nums[x]`为我们当前看到的这个元素。

1. 如果在`minK <= nums[x] <= maxK`，之前已经找到了区间`[k,l]`，那么能和`x`组成的子数组数量为`k - i + 1`。
    
    可以参照上面第四个例子。当我们看到`4`的时候，我们可以组成`[2,6,4]`和`[3,2,6,4]`。当我们看到最后一个`2`的时候，前面有`[3,2,6]`可以组成3个子数组。
1. 在规律1的基础上，当`nums[x] == minK or maxK`的时候，我们需要更新区间`[k,l]`。

到这里这道题的核心部分已经解决了，那么我们来看看如何移动指针。假设我们有指针`[left, right]`，

1. 我们持续移动右指针`right`，就像刚刚我们移动`x`变量。
1. 之前我们假设的是我们已经能够找到区间`[i,j]`。所以我们在看到不符合条件的`x`使得`nums[x] < minK or nums[x] > maxK`之前，`i`都是保持不变的，因此这就是我们的左指针`left`。
1. 当我们找到不符合区间条件位置的`nums[right]`的时候，我们就需要把之前的所有东西废弃掉，重新开始新一轮的匹配。
    
    举个简单的例子我们可以想象这个数组为`nums = ...[i_1, j_1]...[i_2, j_2]...`，这样的话当我们移动到`...`里不符合条件的`nums[right]`的时候，我们就不能用刚刚的规则继续匹配了。

到这里，我们就把所有需要理解的逻辑都捋顺了。

## 代码

```python3
class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        left = -1
        lastmin = -1
        lastmax = -1

        result = 0

        for right in range(len(nums)):
            if nums[right] < minK or nums[right] > maxK:
                left = right
                lastmin = -1
                lastmax = -1
                continue
            
            if nums[right] == minK:
                lastmin = right
            if nums[right] == maxK:
                lastmax = right
            
            if lastmin != -1 and lastmax != -1:
                result += max(0, min(lastmin, lastmax) - left)
        return result
```

这里跟上述逻辑有略微不一样的是，我们每次把不符合条件的地方当作`left`开始的地方，这样逻辑更加简洁。