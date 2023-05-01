Title: 【Leetcode题解】Biweekly Contest 102 双周赛题目解析
Slug: biweekly-102
Date: 2023-04-16 15:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Biweekly Contest 102 | 2639. Find the Width of Columns of a Grid 查询网格图中每一列的宽度 | 2640. Find the Score of All Prefixes of an Array 一个数组所有前缀的分数 | 2641. Cousins in Binary Tree II 使子数组元素和相等 | 2642. Design Graph With Shortest Path Calculator 设计可以求最短路径的图类 | Solution to contest problems 赛题讲解 ｜ Prefix Sum 前缀和 | BFS 广度优先搜索 | Dijkstra's Algorithm 狄克斯特拉算法 | Floyd-Warshall's Algorithm 算法 | Bianry Tree Traversal 二叉树的遍历


又是两周一次双周赛环节。本次的题目涉及前缀和，二叉树和图。整体知识覆盖面积较广。难度属于手速场中比较均衡的那种。第三题需要一定的代码量，打字速度慢的同学可能会稍微吃一点亏。而最后一题则是标准的模板图题，又是喜闻乐见的狄克斯特拉。接下来让我们一起看看题目的解析。

## 题目列表
- [Easy - 2639. Find the Width of Columns of a Grid](https://leetcode.com/problems/find-the-width-of-columns-of-a-grid/)
- [Medium - 2640. Find the Score of All Prefixes of an Array](https://leetcode.com/problems/find-the-score-of-all-prefixes-of-an-array/)
- [Medium - 2641. Cousins in Binary Tree II](https://leetcode.com/problems/cousins-in-binary-tree-ii/)
- [Hard - 2642. Design Graph With Shortest Path Calculator](https://leetcode.com/problems/design-graph-with-shortest-path-calculator/)

## 2639. Find the Width of Columns of a Grid 查询网格图中每一列的宽度

遍历每一列找到最大值。转换的话，直接转化为`str`求长度即可，如果用`log10`的话需要考虑一些边界情况，如负数，`0`或者刚好是`10`的次方。

### 代码

```python
from math import log10, ceil

class Solution:
    def findColumnWidth(self, grid: List[List[int]]) -> List[int]:
        result = []
        for j in range(len(grid[0])):
            m = 0
            for i in range(len(grid)):
                m = max(m, len(str(grid[i][j])))
            result.append(m)
        return result
```

## 2640. Find the Score of All Prefixes of an Array 一个数组所有前缀的分数

这里会需要构建一个前缀和的数组，使用的时候直接通过前缀和数组按照题目的要求构建`conver`数组。最后再求一下累加和。

### 代码

```python
class Solution:
    def findPrefixScore(self, nums: List[int]) -> List[int]:
        prefix = [0]
        for v in nums:
            prefix.append(max(prefix[-1], v))
        prefix = prefix[1:]
        # print(prefix)
        
        conver = []
        for i, v in enumerate(nums):
            conver.append(v + prefix[i])
        
        # print(conver)
        
        from itertools import accumulate
        
        return list(accumulate(conver))
```

## 2641. Cousins in Binary Tree II 二叉树的堂兄弟节点 II

给定一个简单二叉树，需要将每个节点的值替换为所有他的堂兄节点（Cousin node）值的和。

> 如果两个节点在树中有相同的深度且它们的父节点不同，那么它们互为堂兄弟 。

先简单看个例子
```
Example 1
Input: [5,4,9,1,10,null,7]
Output: [0,0,0,7,7,null,11]
Explanation:
depth = 1: [[5]] => [0]
depth = 2: [[4,9]] => [0]
depth = 3: [[1, 10], [7]] => [7, 11]
```

在这个例子中，我们可以看到在深度一样的情况下，我们可以把父节点相同的子节点归并起来并求和，并将子节点的值替换为每一个深度的和减去它自身。我们分三步走

1. 遍历整个二叉树，求每一个父节点左右节点的和，并根据深度归并父节点。
2. 遍历每一层，求每个父节点下子节点替换为堂兄弟的值。即当前一层所有子节点的和减去当前父节点的左右节点的和。
3. 便利整个二叉树，根据当前节点的父节点找到对应的和并替换，返回结果。

此外，第二步其实跟[238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)比较相似，只不过累加和不需要处理乘积的边界条件。

### 代码

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def replaceValueInTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        parent_sum = defaultdict(int)
        parent_depth = defaultdict(set)
        
        def traverse(root, parent, depth):
            if root is None:
                return
            parent_sum[parent] += root.val
            parent_depth[depth].add(parent)
            
            traverse(root.left, root, depth + 1)
            traverse(root.right, root, depth + 1)
        
        traverse(root, None, 0)
        
        # print(parent_sum)
        # print(parent_depth)
        
        parent_result = dict()
        for key in sorted(parent_depth.keys()):
            parents = parent_depth[key]
            psum = [parent_sum[p] for p in parents]
            total = sum(psum)
            psum_result = [total - ps for ps in psum]
            for i, p in enumerate(parents):
                parent_result[p] = psum_result[i]
        
        def traverse2(root, parent):
            if root is None:
                return
            root.val = parent_result[parent]
            traverse2(root.left, root)
            traverse2(root.right, root)
        
        traverse2(root, None)
        return root
```

## 2642. Design Graph With Shortest Path Calculator 设计可以求最短路径的图类

给定一个有向有权图，设计一个数据结构以支持如下操作：

- `Graph(int n, int[][] edges)` 初始化整个图
- `addEdge(int[] edge)` 添加一条边到图中
- `int shortestPath(int node1, int node2)` 查询两个点之间最短权重

此外，所有的边不会重复；不会存在环和自我循环；`addEdge`和`shortestPath`两个方法最多各调用`100`次。

这道题目是一道经典图的题目。虽然求图的最短距离有很多种做法，但是这里会有一个问题就是我们的边是会有更新的，所以我们应该使用一些缓存友好的方法。即每次查询最短距离的时候可以以较少的操作拿到。对于这道题来说，使用`Floyd Warshall`和`Dijkstra`两种做法会更方便一点，这里我会分享两种解法。

`Floyd Warshall`的解法相对比较暴力，我们有一个$O(n^3)$的主循环。我们先初始化$adj$，一个$n^2$的距离矩阵，并将所有值设置为`inf`。其中，$adj[i][i] = 0$；对于每一条边$(i, j, w)$，$adj[i][j] = w$。在`addEdge`更新的时候，我们运行一个$O(n^2)$的循环，若路径`u->v`可以经过`i->j`且路径更小，我们就更新$adj[u][v]$。

`Dijkstra`的解法是在每个shortestPath调用的时候，直接用类似BFS的解法。但是同样利用了一个`adj`矩阵，使算法可以走捷径直接计算最短距离。

### 代码

Floyd Warshall算法

```python
from typing import List

class Graph:

    def __init__(self, n: int, edges: List[List[int]]):
        self.adj_matrix = [[float('inf') if i != j else 0 for j in range(n)] for i in range(n)]
        self.n = n
        self.modified = False
        for edge in edges:
            self.addEdge(edge)
        self._floyd_warshall()

    def addEdge(self, edge: List[int]) -> None:
        from_node, to_node, edge_cost = edge
        if self.adj_matrix[from_node][to_node] > edge_cost:
            self.adj_matrix[from_node][to_node] = edge_cost
            self.modified = True

    def _floyd_warshall(self):
        if not self.modified:
            return
        self.modified = False
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.adj_matrix[i][j] = min(self.adj_matrix[i][j], self.adj_matrix[i][k] + self.adj_matrix[k][j])

    def shortestPath(self, node1: int, node2: int) -> int:
        self._floyd_warshall()
        cost = self.adj_matrix[node1][node2]
        return cost if cost != float('inf') else -1
```

Dijkstra算法

```python
from heapq import heappush, heappop

class Graph:
    def __init__(self, n: int, edges: List[List[int]]):
        self.n = n
        self.adjList = [[] for _ in range(n)]
        for edge in edges:
            self.adjList[edge[0]].append((edge[1], edge[2]))

    def addEdge(self, edge: List[int]):
        self.adjList[edge[0]].append((edge[1], edge[2]))

    def shortestPath(self, node1: int, node2: int) -> int:
        dist = self._dijkstra(self.n, node1)
        return dist[node2]

    def _dijkstra(self, N: int, S: int) -> List[int]:
        pq = [(0, S)]
        dist = [-1] * N
        dist[S] = 0
        while pq:
            d, x = heappop(pq)
            if d > dist[x]:
                continue
            for nx, nd in self.adjList[x]:
                if dist[nx] != -1 and dist[nx] <= d + nd:
                    continue
                dist[nx] = d + nd
                heappush(pq, (dist[nx], nx))
        return dist
```

## 小结

对于这次双周赛来说，能够快速判断题目所需要的算法是非常有必要的。此外还需要有一定的问题分解能力，把问题分解成较小子问题一一求解。当然这点对于任何问题都非常有效。那么我们下期再见。

如果你想变得更强的话，可以做做

- [Easy - 993. Cousins in Binary Tree](https://leetcode.com/problems/cousins-in-binary-tree/)
- [Medium - 1161. Maximum Level Sum of a Binary Tree](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/)
- [Medium - 2070. Most Beautiful Item for Each Query](https://leetcode.com/problems/most-beautiful-item-for-each-query/)
- [Medium - 1786. Number of Restricted Paths From First to Last Node](https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/)
- [Hard - 2608. Shortest Cycle in a Graph](https://leetcode.com/problems/shortest-cycle-in-a-graph/)（[双周赛101第四题 我的解法]({filename}/leetcode/biweekly-101.md)）