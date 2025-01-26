Title: Weekly Contest 410 周赛题目解析
Slug: weekly-410
Date: 2024-12-29 12:00
Category: Leetcode
Tags: Contest
Summary: 2024-08 Leetcode Weekly Contest 410 第 410 场力扣周赛 | Solution to contest problems 赛题讲解 | 3248. Snake in Matrix 矩阵中的蛇 | 3249. Count the Number of Good Nodes 统计好节点的数目 | 3250. Find the Count of Monotonic Pairs I 单调数组对的数目 I | 3251. Find the Count of Monotonic Pairs II 单调数组对的数目 II


[Weekly Contest 410](https://leetcode.com/contest/weekly-contest-410/)

[第 410 场周赛](https://leetcode.cn/contest/weekly-contest-410/)


## 题目列表

- [3248. Snake in Matrix 矩阵中的蛇](https://leetcode.com/problems/snake-in-matrix/description/)
- [3249. Count the Number of Good Nodes 统计好节点的数目](https://leetcode.com/problems/count-the-number-of-good-nodes/description/)
- [3250. Find the Count of Monotonic Pairs I 单调数组对的数目 I](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-i/description/)
- [3251. Find the Count of Monotonic Pairs II 单调数组对的数目 II](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-ii/description/)


## 3248. Snake in Matrix 矩阵中的蛇

给定方形矩阵`n`，和一系列上下左右的命令，一条蛇从矩阵左上角序号为`0`的格子出发，问最终到达序号为几的格子。

根据题意求解即可。格子的索引可以用2D矩阵的`i * n + j`来求得。

```python
DIR = [0, 1, 0, -1]
CDM = ["RIGHT", "DOWN", "LEFT", "UP"]

class Solution:
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        i = 0
        j = 0

        for cm in commands:
            idx = CDM.index(cm)
            i = i + DIR[idx]
            j = j + DIR[(idx + 1) % 4]
        
        return i * n + j
```

## 3249. Count the Number of Good Nodes 统计好节点的数目

给定一棵无向的树中所有的边的列表`edges`，此树总以节点`0`作为根。若一个节点的所有子树的大小都相同，我们称这个节点为一个好节点。问此树中有多少个好节点。注意，叶子节点也算一个好节点。

非常标准的DFS题目，求出所有子树的大小逐一比对即可。

```python
class Solution:
    def countGoodNodes(self, edges: List[List[int]]) -> int:
        g = defaultdict(list)

        for i, j in edges:
            g[i].append(j)
            g[j].append(i)
        
        result = 0

        def dfs(i, p):
            nonlocal result
            szs = []
            for j in g[i]:
                if j == p:
                    continue
                szs.append(dfs(j, i))
            
            if all(sz == szs[0] for sz in szs):
                # print(f"node {i}")
                result += 1
            return sum(szs) + 1
        
        dfs(0, -1)

        return result
```

## 3250. Find the Count of Monotonic Pairs I 单调数组对的数目 I

给定长度为`n`正整数列表`nums`，若存在长度为`n`的单调非递减和单调非递增的两个数对`arr1`和`arr2`使得`arr1[1] + arr2[i] = nums[i]`对于每一个`i`都成立，问有多少个这样的单调数组对。需要对于结果取模。s

首先，从数据范围可以观察到，`1 <= nums[i] <= 50`，因此如果使用`dp`的话，这里可以给我们一个相对较小的时间复杂度。

为了处理问题，我们设`dp[i][j]`为以`nums[i]`为起点，满足`arr1`单调递增，`arr2`单调递减的数对的个数，其中`arr1[i] = j`。

关键在于从右向左遍历，利用已计算的结果更新当前状态。具体来说，对于每个`nums[i]`，计算其可以与后续组合的所有`j`值，递推公式为：

- `dp[i][j]`等于当前可行解的累计值，如果`j`满足差值条件，还需要累加后续的组合。
- 利用`nums[i]`与`nums[i - 1]`之间的最大差值`diff`来控制`arr1`和`arr2`的增减趋势。

将所有可能的情况累积至`dp[0][0]`即可得解。


```python
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        dp = [[0] * 51 for _ in range(n + 1)]

        dp[n] = [1] * 51

        for i in range(n - 1, -1, -1):
            diff = max(0, nums[i] - nums[i - 1]) if i > 0 else 0
            for j in range(50, -1, -1):
                if j + 1 <= 50:
                    dp[i][j] = dp[i][j + 1]
                if j + diff <= nums[i]:
                    dp[i][j] = (dp[i][j] + dp[i + 1][j + diff]) % MOD
        
        return dp[0][0]
```

## 3251. Find the Count of Monotonic Pairs II 单调数组对的数目 II

本题与C题[3250. Find the Count of Monotonic Pairs I 单调数组对的数目 I](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-i/description/)题面相同，但是数据范围变成了`1 <= nums[i] <= 1000`，意味着之前的dp构造方式不再适用。

我们可以观察到，在C题的dp中，每次dp的结果依赖于`diff`，即`dp[i][j] = (dp[i][j] + dp[i + 1][j + diff])`这个部分。因此我们总需要维护之前计算的二维数组。


我们如何简化状态转移？首先，我们回顾`dp[i][j]`的来源：

1. `dp[i][j]`中`dp[i - 1][j - d]`的部分来源于前一层，即`nums[i - 1]`到`nums[i]`之间的差异`d`。这表明每一层的状态更新只依赖上一层。
2. `dp[i][j]`的第二部分是`dp[i][j - 1]`，它表示当前层`j`之前所有可能状态的累积和。这部分表明，通过累积前缀和，我们可以用线性的方式计算当前层的状态。

基于这两点观察，我们发现：

- 实际上，每一层的状态只与上一层相关，因此我们可以用两个一维数组来表示当前层和上一层的状态，避免存储整个二维数组。  
- 我们可以利用累积前缀和，快速计算当前层的状态转移。累积和的思想在转移公式中表现为`dp2[j] = dp2[j - 1] + dp[j - d]`。


```python
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        m = max(nums) + 1

        dp = [1] * m
        dp2 = [0] * m

        for i in range(n - 1, -1, -1):
            diff = max(0, nums[i] - nums[i - 1]) if i > 0 else 0
        
            for j in range(m):
                dp2[j] = 0

            for j in range(nums[i], -1, -1):
                if j + 1 < m:
                    dp2[j] = dp2[j + 1]
                if j + diff <= nums[i]:
                    dp2[j] = (dp2[j] + dp[j + diff]) % MOD
            
            dp, dp2 = dp2, dp

        return dp[0]
```