Title: Weekly Contest 393 周赛题目解析
Slug: weekly-393
Date: 2024-03-31 22:00
Category: Leetcode
Tags: Contest
Status: draft
Summary: 2024-03 Leetcode Weekly Contest 393 第 393 场力扣周赛 | 3105. Longest Strictly Increasing or Strictly Decreasing Subarray 最长的严格递增或递减子数组 | 3106. Lexicographically Smallest String After Operations With Constraint 满足距离约束且字典序最小的字符串 | 3107. Minimum Operations to Make Median of Array Equal to K 使数组中位数等于 K 的最少操作数 | 3108. Minimum Cost Walk in Weighted Graph 带权图里旅途的最小代价 | Solution to contest problems 赛题讲解 | Dual Pointer 双指针 | Union Find 并查集

[Weekly Contest 393](https://leetcode.com/contest/weekly-contest-393/)

[第 393 场周赛](https://leetcode.cn/contest/weekly-contest-393/)

## 题目列表

- [3105. Longest Strictly Increasing or Strictly Decreasing Subarray 最长的严格递增或递减子数组](https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/)
- [3106. Lexicographically Smallest String After Operations With Constraint 满足距离约束且字典序最小的字符串](https://leetcode.com/problems/lexicographically-smallest-string-after-operations-with-constraint/description/)
- [3107. Minimum Operations to Make Median of Array Equal to K 使数组中位数等于 K 的最少操作数](https://leetcode.com/problems/minimum-operations-to-make-median-of-array-equal-to-k/)
- [3108. Minimum Cost Walk in Weighted Graph 带权图里旅途的最小代价](https://leetcode.com/problems/minimum-cost-walk-in-weighted-graph/)

## 3105. Longest Strictly Increasing or Strictly Decreasing Subarray 最长的严格递增或递减子数组

按照题意模拟，分别从左到右从右到左使用双指针即可。

```python
class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        left = 0
        
        result = 1
        for right in range(1, len(nums)):
            if nums[right] <= nums[right - 1]:
                left = right
            result = max(result, right - left + 1)
        
        left = 0
        for right in range(1, len(nums)):
            if nums[right] >= nums[right - 1]:
                left = right
            result = max(result, right - left + 1)
        
        return result
```

## 3106. Lexicographically Smallest String After Operations With Constraint 满足距离约束且字典序最小的字符串

给定小写字符串`s`，你可以对字符串中的任意一位进行加减`1`操作，使其变换成另一个字母。与此同时，变换的时候遵循循环排列，如`z + 1 => a`或`a - 1 => z`。在限定操作`k`次的情况下，求可以变换得到的字典序最小的字符串。

看到字典序最小，我们可以马上考虑使用贪心的方法：肯定是优先把左边的字母变成更小的字母收益更大。给定字母`c`和剩余操作次数`k`，我们有：

1. 当满足`(c + n) % 26 == 'a'`，且`n <= k`时，我们可以把字母`c`往高位变换直至变成`'a'`。
1. 当`c - n == 'a'`，且`n <= k`时，我们可以把字母`c`往低位变换直至变成`'a'`。
1. 字母`c`也可以同时满足以上两个条件，则我们取尽量小的`n`。
1. 否则的话，我们只能最多向低位变换`k`次。

按照这样的逻辑，我们从左到右每次只处理一个字母，直至无法处理为止。

```python
def smallest_achivable(c, k):
    if c == 'a' or k == 0:
        return c, 0

    d = ord(c) - ord('a')

    if d + k >= 26 and d - k < 0:
        return 'a', min(26 - d, d)
    elif d + k >= 26:
        return 'a', 26 - d
    elif d - k < 0:
        return 'a', d

    return chr(d - k + ord('a')), k


class Solution:
    def getSmallestString(self, s: str, k: int) -> str:
        
        ns = []
        
        for c in s:
            nc, deduct = smallest_achivable(c, k)
            k -= deduct
            ns.append(nc)
        
        return ''.join(ns)
```

## 3107. Minimum Operations to Make Median of Array Equal to K 使数组中位数等于 K 的最少操作数

给定正整数数组`nums`和正整数`k`，可以将数组中任意数字加一或减一。求将数组的中位数变成`k`的最小操作次数。

这题的中位数定义为 `nums[n // 2]`，无需考虑偶数个数字时的场景。

将数组排序后，分成左右两边。左边的数字必小于等于`k`，右边的数字必大于等于`k`，因此操作次数为违反此规则的数字与`k`的差值的绝对值的和。

```python
class Solution:
    def minOperationsToMakeMedianK(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        midIndex = n // 2
        operations = 0

        for i in range(midIndex, -1, -1):
            if nums[i] > k:
                operations += (nums[i] - k)
            else:
                break
        for i in range(midIndex, n):
            if nums[i] < k:
                operations += (k - nums[i])
            else:
                break

        return operations
```

## 3072. Distribute Elements Into Two Arrays II 将元素分配到两个数组中 II

给定有权图`edges = [[u_i, v_i, w_i]...]`。若某条`u -> v`的路径经过了一系列边，则此路径的代价为经过的边的所有权重的按位与（Bitwise AND），且你可以经过同一条边无数次。给定一系列查询`query = [[p_i, q_i]...]`，返回每个查询的最短代价。

我们知道按位与操作的真值表只有当两位同时为`1`的时候才可以得到`1`，题目也告诉我们可以经过同一条边无数次，因此我们不需要考虑具体的路径，只需要暴力的经过尽可能多的边，就可以得到较小的代价。

我们可以采用并查集Union Find来支持此类查询。我们知道，并查集可以快速的找到图中的两个点是否连接。与此同时，在合并（Union）操作的时候，我们可以顺便进行按位与来计算两个合并节点的代价。

```python
class UF:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.min_cost = {i: (1 << 31) - 1 for i in range(size)}

    def find(self, x: int) -> int:
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int, weight: int):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            self.parent[rootX] = rootY
        self.min_cost[rootY] = self.min_cost[rootY] & self.min_cost[rootX] & weight
        self.min_cost[rootX] = self.min_cost[rootY]
        self.min_cost[x] = self.min_cost[rootY]


class Solution:
    def minimumCost(self, n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
        uf = UF(n)

        for u, v, w in edges:
            uf.union(u, v, w)

        answer = []
        for s, t in query:
            if s == t:
                answer.append(0)
            elif uf.find(s) == uf.find(t):
                answer.append(uf.min_cost[uf.find(s)])
            else:
                answer.append(-1)

        return answer
```