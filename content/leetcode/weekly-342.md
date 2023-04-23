Title: 【Leetcode题解】Weekly Contest 342 周赛题目解析
Slug: weekly-342
Date: 2023-04-23 17:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Weekly Contest 342 第 342 场力扣周赛 | 2651. Calculate Delayed Arrival Time 计算列车到站时间 | 2652. Sum Multiples 倍数求和 | 2653. Sliding Subarray Beauty 滑动子数组的美丽值 | 2654. Minimum Number of Operations to Make All Array Elements Equal to 1 使数组所有元素变成 1 的最少操作次数 | Solution to contest problems 赛题讲解 | 快速选择 Quickselect | DFS | 最大公约数 Greatest Common Divisor

[Weekly Contest 342](https://leetcode.com/contest/weekly-contest-342/)

[第 342 场力扣周赛](https://leetcode.cn/contest/weekly-contest-342/)

前两周难的一比，今天却又来一个手速摆烂场。有点看不懂这个操作。最后一题可以总结为<span title="你知道的太多了" class="heimu">找 1</span>。

## 题目列表

- [Easy - 2651. Calculate Delayed Arrival Time](https://leetcode.com/problems/calculate-delayed-arrival-time/)
- [Easy - 2652. Sum Multiples](https://leetcode.com/problems/sum-multiples/)
- [Medium - 2653. Sliding Subarray Beauty](https://leetcode.com/problems/sliding-subarray-beauty/)
- [Medium - 2654. Minimum Number of Operations to Make All Array Elements Equal to 1](https://leetcode.com/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/)


## 2651. Calculate Delayed Arrival Time 计算列车到站时间

根据题意，暴力模拟即可。

### 代码

```python
class Solution:
    def findDelayedArrivalTime(self, arrivalTime: int, delayedTime: int) -> int:
        return (arrivalTime + delayedTime) % 24
```

## 2652. Sum Multiples 倍数求和

根据题意，暴力模拟即可。

但是这道题确实有一个数学解法。首先，我们可以用等差数列求出所有小于`n`且倍数为`3`，`5`和`7`的数字的和。但是简单相加起来会重复算一些元素，根据[容斥原理（inclusion-exclusion principle）](https://zh.wikipedia.org/zh-sg/%E6%8E%92%E5%AE%B9%E5%8E%9F%E7%90%86)，我们可以排除重复计算的元素。令$g(n, a)$为包含`x <= n`且`x`为`a`的倍数的所有`x`的集合，则本题的答案为
$$
f(n, \{3,5,7\}) = g(n, \{3\}) + g(n, \{5\}) + g(n, \{7\}) - g(n, \{3, 5\}) - g(n, \{3, 7\}) - g(n, \{5, 7\}) + g(n, \{3,5,7\})
$$

### 代码

```python
class Solution:
    def sumOfMultiples(self, n: int) -> int:
        result = 0
        for i in range(1, n + 1):
            if i % 3 == 0 or i % 5 == 0 or i % 7 == 0:
                result += i
        
        return result
```

## 2653. Sliding Subarray Beauty 滑动子数组的美丽值

给定一个数组`nums`，找到这个数组的每一个长度为`k`的子数组的美丽值。子数组的美丽值定义为子数组里包含的数字中第`k`小的负数；若子数组第`k`大的数字不为负数，则为`0`。

根据题意进行模拟，我们知道我们要用一个数据结构维护`nums`里某个长度为`k`的子数组里面的数字。此外我们还要能快速有效的找到这个数组里第`k`大的数字。因为数据范围较小，实际上用列表存然后顺序遍历也是可以AC的。但在这里我们考虑用`B`树来处理，插入，查找和删除都是`O(log(k))`。

### 代码

```python
class Solution:
    def getSubarrayBeauty(self, nums: List[int], k: int, x: int) -> List[int]:
        from sortedcontainers import SortedList
        result = [0] * (len(nums) - k + 1)
        window = SortedList()
        
        for i in range(len(nums)):
            if len(window) == k:
                window.remove(nums[i - k])
            window.add(nums[i])
                        
            if len(window) == k and window[x - 1] < 0:
                # print(i, window, window[x - 1])
                result[i - k + 1] = window[x - 1]
        
        return result
```

## 2654. Minimum Number of Operations to Make All Array Elements Equal to 1 使数组所有元素变成 1 的最少操作次数

给定一个只包含正整数的数组`nums`，你可以对立面任意索引`i`求`gcd(nums[i], nums[i + 1])`并将`nums[i]`或`nums[i + 1]`替换为前面求的最大公约数。找到最少的操作次数使得数组的所有元素都变成`1`。

我们知道，所有数字和`1`的最大公约数都是`1`。因此只要数组里存在至少一个`1`，最少操作次数就为`1`。此外，若两个正整数互质的话，他们的最大公约数就是`1`。这里我们分两步走：首先构造第一个`1`的出现，则可知剩下的非`1`数字都可以跟这个`1`抵消，进而求出结果。

那么怎么构造第一个`1`的出现呢。我们可以考虑用`DFS`。<span title="你知道的太多了" class="heimu">没想到吧，这也可以D。</span> 无论如何，我们对数组里的每一个数字，循环迭代两两求最大公约数，总能够收敛到一个结果。若在中间我们找到一个`1`的话，那么我们就可以通过`x`步找到一个`1`。

### 代码

```python
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        
        def find():
            steps = 0
            q = list(nums)
            while q:
                qq = []
                for i in range(len(q) - 1):
                    curr = gcd(q[i], q[i + 1])
                    if curr == 1:
                        return steps
                    
                    qq.append(curr)
                
                q = qq
                steps += 1
            return -1
        
        steps = find()
        
        if steps == -1:
            return -1
        
        return steps + len(nums) - sum([i == 1 for i in nums])
```

## 小结

如果你想变强的话，可以做做

- [Hard - 1521. Find a Value of a Mysterious Function Closest to Target](https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/)
