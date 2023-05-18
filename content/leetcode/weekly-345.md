Title: Weekly Contest 345 周赛题目解析
Slug: weekly-345
Date: 2023-05-18 22:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-05 Leetcode Weekly Contest 345 第 345 场力扣周赛 | 2682. Find the Losers of the Circular Game 找出转圈游戏输家 | 2683. Neighboring Bitwise XOR 相邻值的按位异或 | 2684. Maximum Number of Moves in a Grid 矩阵中移动的最大次数 | 2685. Count the Number of Complete Components 统计完全连通分量的数量 | Solution to contest problems 赛题讲解 | 异或 XOR | 

[Weekly Contest 345](https://leetcode.com/contest/weekly-contest-345/)

[第 345 场周赛](https://leetcode.cn/contest/weekly-contest-345/)


“认真读题，作风优良，能打胜仗。” 
<p align="right"> ---- 我说的 </p>

宿醉着也能全AC的手速题有什么好写的！虽然这么说着，但还是口嫌体正地写了解析。但说实话，现在这题目长度堪比托福阅读题了，是College Board又裁员了吗？

## 题目列表

- [2682. Find the Losers of the Circular Game](https://leetcode.com/problems/find-the-losers-of-the-circular-game/solutions/)
- [2683. Neighboring Bitwise XOR](https://leetcode.com/problems/neighboring-bitwise-xor/)
- [2684. Maximum Number of Moves in a Grid](https://leetcode.com/problems/maximum-number-of-moves-in-a-grid/)
- [2685. Count the Number of Complete Components](https://leetcode.com/problems/count-the-number-of-complete-components/)

## 2682. Find the Losers of the Circular Game 找出转圈游戏输家

按照题意模拟即可。

```python
class Solution:
    def circularGameLosers(self, n: int, k: int) -> List[int]:
        idx = [0] * n
        idx[0] = 1
        v = k % n
        add = 2 * k
        
        while idx[v] == 0:
            idx[v] += 1
            v = (v + add) % n
            add = (add + k) % n
        
        result = []
        for i, v in enumerate(idx):
            if v == 0: result.append(i + 1)
        
        return result
```

## 2683. Neighboring Bitwise XOR 相邻值的按位异或

一个二进制数组列表`original`通过一个变换形成了新的数组`derived`。这个变换是使得`derived[i] = original[i] ^ original[i + 1]`，边界case的时候循环回`0`。给定`derived`数组，求他是否能被某个`original`变换得到。

根据真值表我们可以知道，若`derived[i - 1] = 1`的话，那么`original[i - 1] != original[i]`；否则两者相等。此外，二进制有两种可能，所以我们两种都尝试一下恢复原数组，并检查原数组`original`是否能够变换回`derived`即可。


```python
class Solution:
    def doesValidArrayExist(self, derived: List[int]) -> bool:
        n = len(derived)
        def check(original):
            for i in range(n):
                if derived[i - 1] == 1:
                    original[i] = 1 ^ original[i - 1]
                else:
                    original[i] = original[i - 1]
            # print(derived, original)
            for i in range(n):
                if original[i - 1] ^ original[i] != derived[i - 1]:
                    return False
            return True
        
        return check([0] * n) or check([1] * n)
```

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

如果你非拉着我让我给你个oneliner的话，我也不能说无可奉告对吧。

当我们知道`derived[i] = original[i] ^ original[i + 1]`的时候，那么`derived[0] ^ derived[1] ^ ... = 0`。而因为我们只有二进制，所以可以转换为数1的个数是否为偶数个即可。

```python
class Solution:
    def doesValidArrayExist(self, derived: List[int]) -> bool:
        return sum(derived) % 2 == 0
```

## 2684. Maximum Number of Moves in a Grid 矩阵中移动的最大次数

给定一个`m x n`的矩阵`grid`。你总在第一列出发，并从`i,j`移动到`i-1,j+1`,`i,j+1`和`i+1,j+1`中的任意一点 ---- 只要这个点里面的点数严格大于当前点的点数，要求最远能走几步。

DP可破。初始化原矩阵大小的DP矩阵。其中`DP[i][j]`是从任意一点开始到`i,j`这个点能走的最大格子数。那么，状态转移方程为`DP[i][j] = 1 + max(DP[i - 1][j - 1], DP[i][j - 1], DP[i + 1][j - 1])`。有三种条件需要跳过不计算：1）不合法，2）左边=0，意味着没有路径到当前点，3）左边的数字小于当前点。

```python
class Solution:
    def maxMoves(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        
        dp = [[0] * n for _ in range(m)]
        for i in range(m):
            dp[i][0] = 1
        
        check = lambda p,q: p >= 0 and q >= 0 and p < m and q < n
        
        for j in range(n):
            for i in range(m):
                for d in [-1, 0, 1]:
                    ni = i - d
                    nj = j - 1
                    if not check(ni, nj):
                        continue
                    if dp[ni][nj] == 0:
                        continue
                    if grid[ni][nj] >= grid[i][j]:
                        continue
                    dp[i][j] = max(dp[i][j], 1 + dp[ni][nj])
        
        # print(dp)
        return max(max(dp[i]) for i in range(m)) - 1
```

## 2685. Count the Number of Complete Components 统计完全连通分量的数量

给定一个无向图，要求这个图里面的完全联通分量的个数。连通分量即无向图中存在的每一个最大联通的子顶点集合。而完全连通分量指的是一个连通分量中每个顶点都有一条边与其他顶点相连。

从任意顶点开始，我们通过DFS遍历所有边直到不能再走为止。这样我们就能找到当前顶点关联的连通分量。而为了判断这个连通分量是否为完全连通分量，我们可以遍历里面所有的顶点，确认每个顶点都与这个连通分量其他任意顶点相连。直接判断当前顶点的边的数量是否等于顶点数量减一即可。

当然，用并查集也是一样的方法，这里就不展开了。

```python
class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        visited = [False] * n
        
        g = [set() for _ in range(n)]
        
        for u, v in edges:
            g[u].add(v)
            g[v].add(u)
        
        def dfs(i):
            visited[i] = True
            result = {i}
            for j in g[i]:
                if visited[j]:
                    continue
                result.update(dfs(j))
            return result
        
        result = 0
        for i in range(n):
            if visited[i]:
                continue
            nodes = dfs(i)
            m = len(nodes)
            
            if all(len(g[node]) == m - 1 for node in nodes):
                result += 1
        
        return result
```