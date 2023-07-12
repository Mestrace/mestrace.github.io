Title: Weekly Contest 352 周赛题目解析
Slug: weekly-352
Date: 2023-07-13 01:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 352 第 352 场力扣周赛 | 2760. Longest Even Odd Subarray With Threshold 最长奇偶子数组 | 2761. Prime Pairs With Target Sum 和等于目标值的质数对 | 2762. Continuous Subarrays 不间断子数组 | 2763. Sum of Imbalance Numbers of All Subarrays 所有子数组中不平衡数字之和 | Solution to contest problems 赛题讲解 | 双指针 Two Pointer

[Weekly Contest 352](https://leetcode.com/contest/weekly-contest-352/)

[第 352 场周赛](https://leetcode.cn/contest/weekly-contest-352/)

手持双指针在线对殴！

## 题目列表

- [2760. Longest Even Odd Subarray With Threshold 最长奇偶子数组](https://leetcode.com/problems/longest-even-odd-subarray-with-threshold/)
- [2761. Prime Pairs With Target Sum 和等于目标值的质数对](https://leetcode.com/problems/prime-pairs-with-target-sum/)
- [2762. Continuous Subarrays 不间断子数组](https://leetcode.com/problems/continuous-subarrays/)
- [2763. Sum of Imbalance Numbers of All Subarrays 所有子数组中不平衡数字之和](https://leetcode.com/problems/sum-of-imbalance-numbers-of-all-subarrays/)

## 2760. Longest Even Odd Subarray With Threshold 最长奇偶子数组

暴力算就完事了。

```python
class Solution:
    def longestAlternatingSubarray(self, nums: List[int], threshold: int) -> int:
        longest_length = 0
        l = 0
        while l < len(nums):
            if nums[l] % 2 == 0 and nums[l] <= threshold:
                r = l
                while r < len(nums) - 1 and nums[r] % 2 != nums[r + 1] % 2 and nums[r + 1] <= threshold:
                    r += 1
                longest_length = max(longest_length, r - l + 1)
            l += 1
        return longest_length
```

## 2761. Prime Pairs With Target Sum 和等于目标值的质数对

给定正整数`n`，找出所有和为`n`的质数对`(x, y)`。返回结果需要按照`x`排列，且不存在重复（如`(a, b)`和`(b, a)`）只能算一对。

考虑到`n`可能会很大，我们需要预先算出`n`以下所有的质数。直接祭出[Sievie of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)。接着左右指针进行计算就行。

说实话，这道题的代码量其实还不小，如果没有模版的话会浪费很多时间。

```python
class Solution:
    def sieve_of_eratosthenes(self):
        sieve = [0, 0] + [1] * (self.MAX_N - 1)
        for x in range(2, int(self.MAX_N**0.5) + 1):
            if sieve[x]:
                for u in range(x*x, self.MAX_N + 1, x):
                    sieve[u] = 0
        return [num for num in range(2, self.MAX_N + 1) if sieve[num]]

    def findPrimePairs(self, n: int):
        self.MAX_N = n + 1
        self.primes = self.sieve_of_eratosthenes()

        primes = [prime for prime in self.primes if prime <= n]
        pairs = []
        left, right = 0, len(primes) - 1
        while left <= right:
            if primes[left] + primes[right] == n:
                pairs.append([primes[left], primes[right]])
                left += 1
                right -= 1
            elif primes[left] + primes[right] < n:
                left += 1
            else:
                right -= 1
        return pairs
```

## 2762. Continuous Subarrays 不间断子数组

给定整数数组`nums`，若其中任意子数组`nums[i:j]`中，所有数字两两之差的绝对值小于`2`，我们说`nums[i:j]`是一个不间断子字数组。问给定`nums`中有多少个连续字数组。

显而易见的，我们可以观察到其中的子问题为，若`nums[i:j]`已经是一个不间断子数组，我们添加一个新的数`nums[j + 1]`时，只需要判断`nums[j + 1]`跟`min(nums[i:j])`和`max(nums[i:j])`的差值。我们考虑用两个单调数组来分别处理最小和最大值，且用双指针来圈定当前包含的数组，则每次可得的子数组就可以通过双指针的区间来计算。

```python
from collections import deque

class Solution:
    def continuousSubarrays(self, nums: List[int]) -> int:
        start = 0
        end = 0
        totalSubarrays = 0
        maxDeque = deque()
        minDeque = deque()

        while end < len(nums):
            # Update the deques for the new element
            while maxDeque and nums[maxDeque[-1]] < nums[end]:
                maxDeque.pop()
            while minDeque and nums[minDeque[-1]] > nums[end]:
                minDeque.pop()

            maxDeque.append(end)
            minDeque.append(end)

            # If the difference between maxValue and minValue is more than 2
            # then move the start pointer forward
            while nums[maxDeque[0]] - nums[minDeque[0]] > 2:
                start += 1
                if maxDeque[0] < start:
                    maxDeque.popleft()
                if minDeque[0] < start:
                    minDeque.popleft()
            
            # Add the number of subarrays ending at 'end' to the total
            totalSubarrays += end - start + 1
            
            # Move to the next element
            end += 1
            
        return totalSubarrays
```

## 2763. Sum of Imbalance Numbers of All Subarrays 所有子数组中不平衡数字之和

给定一个数组`nums`，定义不平衡数字为`nums`排序后前后差值`> 1`的个数，求`nums`所有连续子数组的不平衡数字的和。

这道题很容易可以得出一个朴素的解法，即`O(n^2)`遍历每个连续子数组并排序，再遍历排序后的子数组求的不平衡数字，则时间复杂度最坏是`O(n^3)`。在这个基础上，我们来进行简化。外层`O(n^2)`的便利难以避免，那么我们看看排序这一步可不可以省略，即利用之前的计算结果来增量计算下一步。

给定一个排序数组`sorted(nums[i:j])`，我们添加`nums[j + 1]`时，不外乎几种情况

- `nums[j + 1]`已经出现在前面的数组里面了，因此不会对不平衡数字产生影响。
- `nums[j + 1] + 1` 或 `nums[j + 1] - 1`已经出现在前面的数组里面了，因此添加`nums[j + 1]`会使得不平衡数字减少`1`。
- 若`nums[i:j]`为空，添加一个数字不平衡数字还是`0`。
- 非以上两种情况，且已经有数字时，添加`nums[j + 1]`会使得不平衡数字增加`1`。

这样，我们就有我们的算法了，直接看实现吧。

```python
class Solution:
    def sumImbalanceNumbers(self, nums: List[int]) -> int:
        n = len(nums)

        result = 0

        for i in range(n):
            s = set()
            curr = 0
            for x in nums[i:]:
                if x in s:
                    pass
                elif (x - 1) in s and (x + 1) in s:
                    curr -= 1
                elif (x - 1 not in s) and (x + 1 not in s) and s:
                    curr += 1
                s.add(x)
                result += curr
            
        return result
```
