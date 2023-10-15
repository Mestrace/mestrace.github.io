Title: Weekly Contest 366 周赛题目解析
Slug: weekly-366
Date: 2023-10-09
Category: Leetcode
Tags: Contest
Summary: 2023-10 Leetcode Weekly Contest 366 第 366 场力扣周赛 | 2894. Divisible and Non-divisible Sums Difference 分类求和并作差 | 2895. Minimum Processing Time 最小处理时间 | 2896. Apply Operations to Make Two Strings Equal 执行操作使两个字符串相等 | 2897. Apply Operations on Array to Maximize Sum of Squares 对数组执行操作使平方和最大 | Solution to contest problems 赛题讲解

[Weekly Contest 366](https://leetcode.com/contest/weekly-contest-366/)

[第 366 场周赛](https://leetcode.cn/contest/weekly-contest-366/)


## 题目列表

- [2894. Divisible and Non-divisible Sums Difference 分类求和并作差](https://leetcode.com/problems/divisible-and-non-divisible-sums-difference/)
- [2895. Minimum Processing Time 最小处理时间](https://leetcode.com/problems/minimum-processing-time/)
- [2896. Apply Operations to Make Two Strings Equal 执行操作使两个字符串相等](https://leetcode.com/problems/apply-operations-to-make-two-strings-equal/)
- [2897. Apply Operations on Array to Maximize Sum of Squares 对数组执行操作使平方和最大](https://leetcode.com/problems/apply-operations-on-array-to-maximize-sum-of-squares/description/)

## 2894. Divisible and Non-divisible Sums Difference 分类求和并作差

按照题意模拟即可。

```python
class Solution:
    def differenceOfSums(self, n: int, m: int) -> int:
        s1 = 0
        for i in range(1, n + 1):
            if i % m != 0:
                s1 += i
        s2 = n * (n + 1) // 2 - s1
        
        return s1 - s2
```

## 2895. Minimum Processing Time 最小处理时间

这道题题目描述太差劲了。有两个要点：

- 每个核心最多只能处理4个任务。
- 题目要求的是处理器被分配的任务中最大能够处理完的时间，而不是最长多久能处理完。

因此，将处理器时间与任务时长分别排序后，让最早的处理器处理接下来最长的四个任务即可获得答案。

这道题如果是要求最长多久能处理完的话，就是一道标准的scheduling题目，用堆Heap即可求得最优解。

```python
class Solution:
    def minProcessingTime(self, processorTime: List[int], tasks: List[int]) -> int:
        proc = sorted(processorTime)
        tasks = sorted(tasks, reverse=True)
        result = 0
        
        for i, p in enumerate(proc):
            for j in range(i * 4, i * 4 + 4):
                result = max(result, p + tasks[j])
        
        return result
```

## 2896. Apply Operations to Make Two Strings Equal 执行操作使两个字符串相等

给定两个长度为`n`的**二进制**字符串`s1`和`s2`和正整数`x`。你可以对字符串执行两种操作：

1. 把`s1[i]`和`s1[i + 1]`两位都进行反转，这个操作的消耗为`1`。
2. 把`s1[i]`和`s2[j]`两位都进行反转，这个操作的消耗为`x`。

你需要通过有限次的操作使得`s1`和`s2`最终相等，并找到最小的消耗。若完全无法使两个字符串相等的话，则返回`-1`。

什么时候两个字符串完全无法相等？答案是当两个字符串不想等的位数为奇数的时候。为什么会这样呢，我们转换下思路思考一下。

首先假设我们有两个二进制数字，将他们进行位运算`xor`之后，我们得到了数字`b`。那么，上面的问题就可以转换成我们通过两种操作要使`b = 0`的最小操作数。则我们可以分别讨论以上两个操作对于`b`来说的情况。我们分别讨论题目中描述的两种操作对于`b`的影响。

首先是第一种：

1. 若`b[i] = 1`且`b[i + 1] = 0`，则我们可以以消耗`1`的代价使`b[i] = 0`，`b[i + 1] = 1`。即把`b[i]`向右边位移一位。
1. 若`b[i] = 1`且`b[i + 1] = 1`，则我们可以以消耗`1`的代价使得`b[i]`和`b[i + 1]`的代价使得`b[i]`和`b[i + 1]`都为`0`。
1. 结合以上两点，若`b[i:j+1] = 1000...0001`，则我们可以以`j - i`的代价使得`b[i]`和`b[j]`变为`0`。

那么我们再来看看第二个操作对于`b`有什么影响：

1. 若`b[i] = 1`且`b[j] = 1`，则我们可以以消耗`x`的代价使得`b[i]`和`b[j]`都变为`0`。

因此我们说，当`b`中存在偶数个`1`的时候才有办法在有限次数内使得两个字符串`s1`和`s2`相等。

从上面的分析中，我们可以看到，我们可以把这个问题分解成一些子问题进行求解。因为前述的操作中，存在一定的局部性。举个例子，当`b = 1001001001`，若我们使用第一种操作，最优解为将`(0, 3)`和`(6, 9)`进行消去，而不是`(0, 9)`和`(6, 3)`。此外，当我们要消去中间`z > x`位的时候，如`b = 1000..[z]..0001`，使用第二种操作会更优。因此，这道题我们可以使用动态规划dp进行求解。其中，`dp[i]`为`b[i:]`的最优解，且我们只需要考虑`b[i] = 1`的情况。

当`i`为奇数的时候，对于这道题的定义来说`dp[i]`是未定义的。因此，我们将第二个条件松弛一下。原来的定义是我们可以选择`b[i] = 1`和`b[j] = 1`两个点，以`x`的代价将两者置为`0`。松弛后的条件为，我们可以选择任意的一个点`b[i] = 1`，以`x / 2`（浮点数）的代价将这个点置为`0`。这样子，我们就可以定义`dp[i]`了。我们直接进行分类讨论`dp[i]`：

- `i = n`，`dp[i] = 0`
- `i = n - 1`，`dp[i] = x / 2`
- `0 < i < n - 1`，`dp[i] = min(dp[i + 1] + x / 2, dp[i + 2] + dist)`，其中`dist`为当前点`b[i] = 1`和上一个点`b[j] = 1`之间的距离`dist = j - i`。

且慢，我们忽略了一个要点。我们怎么确保最后不会出现奇数次的`x / 2`呢？考虑我们只有偶数个的`b[i] = 1`的情况，我们会使用`m`次操作一，和`n`次操作二。很明显可得，因为第一种操作只会消去两个，剩余的元素只能用偶数个第二种操作消去。这里就不再延伸了，感兴趣的同学可以自己使用`n = 4`的情况去推演一下。

```python
class Solution:
    def minOperations(self, s1: str, s2: str, x: int) -> int:
        diffs = [i for i in range(len(s1)) if s1[i] != s2[i]]

        if len(diffs) % 2 == 1:
            return -1
        if len(diffs) == 0:
            return 0
        # print(diffs)
        dp = [float("inf") for _ in range(len(diffs) + 1)]
        dp[-1] = 0
        dp[-2] = 0
        for idx in range(len(diffs) - 2, -1, -1):
            dp[idx] = min(
                dp[idx + 1] + x, 
                dp[idx + 2] + diffs[idx + 1] - diffs[idx],
            )
            # print(dp)
        return int(dp[0])
```


## 2897. Apply Operations on Array to Maximize Sum of Squares 对数组执行操作使平方和最大


给定一个数组列表`nums`和整数`k`，你可以对数组中的数字`nums[i]`和`nums[j]`做如下操作，使`nums[i] = nums[i] AND nums[j]`和`nums[j] = nums[i] OR nums[j]`。你可以重复这个操作任意次数。最终，你需要选择`k`个数字，并找到他们的平方和。要求求出最大的平方和结果。

先复习一下位运算

|`x`|`y`|`x&y`|`x|y`|
|:-:|:-:|:---:|:---:|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

虽然爱会消失，但是比特不会。我们可以看到，只有当`(x, y) = (1, 0)`的时候，结果才会改变。因此，只要我们执行这个操作无限次，我们会重组这个数字无限次，使得所有比特位都排好序。

```python
class Solution:
    def maxSum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        idx = [0] * 32
        lst = [0] * n

        for x in nums:
            for i in range(32):
                if x >> i & 1:
                    lst[idx[i]] += 1 << i
                    idx[i] += 1
        
        result = 0
        mod = int(1e9 + 7)

        for i in range(k):
            result += lst[i] * lst[i]
            result %= mod
        
        return result
```