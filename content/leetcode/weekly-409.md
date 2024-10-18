Title: Weekly Contest 409 周赛题目解析
Slug: weekly-409
Date: 2024-10-18 12:00
Category: Leetcode
Tags: Contest
Summary: 2024-08 Leetcode Weekly Contest 409 第 409 场力扣周赛 | Solution to contest problems 赛题讲解 | 3242. Design Neighbor Sum Service 设计相邻元素求和服务 | 3243. Shortest Distance After Road Addition Queries I 新增道路查询后的最短距离 I | 3244. Shortest Distance After Road Addition Queries II 新增道路查询后的最短距离 II | 3245. Alternating Groups III 交替组 III

[Weekly Contest 409](https://leetcode.com/contest/weekly-contest-409/)

[第 409 场周赛](https://leetcode.cn/contest/weekly-contest-409/)


## 题目列表

- [3242. Design Neighbor Sum Service 设计相邻元素求和服务](https://leetcode.com/problems/design-neighbor-sum-service/description/)
- [3243. Shortest Distance After Road Addition Queries I 新增道路查询后的最短距离 I](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/description/)
- [3244. Shortest Distance After Road Addition Queries II 新增道路查询后的最短距离 II](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-ii/description/)
- [3245. Alternating Groups III 交替组 III](https://leetcode.com/problems/alternating-groups-iii/description/)


## 3242. Design Neighbor Sum Service 设计相邻元素求和服务

给定一个`n x n`的矩阵，其中包含`[0, n^2 - 1]`区间的每一个数字，设计一个类`neighborSum`，存在两个方法：`adjacentSum(value)`返回值为`value`的数字的邻接格子的数字之和；`diagonalSum(value)` 返回值为 `value`的格子的邻接对角线格子的数字之和。

由于区间刚好等于格子数量，因此可以认定矩阵中每一个数字都是独特的。为了最快的效率，我们直接在`__init__`的时候，就将所有的结果预先计算好即可。题目并不复杂，只是代码量稍微大一点点。

```python
ADIR = [0, -1, 0, 1, 0]
# 1 1, 1 -1, -1 1, -1 -1
DDIR = [1, -1, -1, 1, 1]

class neighborSum:

    def __init__(self, grid: List[List[int]]):
        self.m = len(grid)
        self.n = len(grid[0])

        adj = [[0] * self.n for _ in range(self.m)]
        dig = [[0] * self.n for _ in range(self.m)]
        vmap = dict()
        for i in range(self.m):
            for j in range(self.n):
                adj[i][j] = self.asum(grid, i, j)
                dig[i][j] = self.dsum(grid, i, j)
                vmap[grid[i][j]] = (i, j)
        
        self.adj = adj
        self.dig = dig
        self.vmap = vmap

    def adjacentSum(self, value: int) -> int:
        i, j = self.vmap[value]
        return self.adj[i][j]

    def diagonalSum(self, value: int) -> int:
        i, j = self.vmap[value]
        return self.dig[i][j]
    
    def asum(self, grid, i, j):
        result = 0
        for k in range(4):
            ni = i + ADIR[k]
            nj = j + ADIR[k + 1]
            if not self.is_valid(ni, nj):
                continue
            result += grid[ni][nj]
        return result
    
    def dsum(self, grid, i, j):
        result = 0
        for k in range(4):
            ni = i + DDIR[k]
            nj = j + DDIR[k + 1]
            if not self.is_valid(ni, nj):
                continue
            result += grid[ni][nj]

        return result
    
    def is_valid(self, i, j):
        return i >= 0 and i < self.m and j >= 0 and j < self.n
        esult
```

## 3243. Shortest Distance After Road Addition Queries I 新增道路查询后的最短距离 I

假设有`n`个城市，且两个相邻城市`i`与`i+1`纵有无向道路连接。给定一个列表的请求`queries`，其中每个请求包含`[u,v]`，在每次请求之后，城市`u`和`v`都会新增一条无向道路，问在每次查询之后，城市`0`到城市`n - 1`的距离，返回一个长度与`queries`长度相同的列表。

这题数据量小，直接用bfs即可。这里有一点小小的改变，由于在处理图的时候，通常对于无向边，我们需要在两个节点的邻接表中都放上对向节点，但是由于我们本身探索的就是`[0, n - 1]`，所以我们只做从数字小的到数字大的边，这样才能保证我们算法不提前探索一些点。不过，有一个疑问是，是否存在向反方向的点走更快的场景？这个问题就留给读者自己探索吧。

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        # Initialize graph with the initial roads
        graph = defaultdict(list)
        for i in range(n - 1):
            graph[i].append(i + 1)
        
        results = []
        
        def bfs(start: int, end: int) -> int:
            queue = deque([start])
            distances = {start: 0}
            
            while queue:
                node = queue.popleft()
                if node == end:
                    return distances[node]
                
                for neighbor in graph[node]:
                    if neighbor not in distances:
                        distances[neighbor] = distances[node] + 1
                        queue.append(neighbor)
            
            return -1
        
        # Process each query
        for ui, vi in queries:
            if ui > vi:
                ui, vi = vi, ui
            graph[ui].append(vi)
            shortest_path = bfs(0, n - 1)
            results.append(shortest_path)
        
        return results
```

## 3244. Shortest Distance After Road Addition Queries II 新增道路查询后的最短距离 II

此题题目与上一题 [3243. Shortest Distance After Road Addition Queries I 新增道路查询后的最短距离 I](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/description/) 一样，因此不多赘述了。

由于数据范围变大，我们无法在给定的时间内用bfs求解了，因此需要考虑其他办法。上一题我们给出了一个断言：对于这道题来说，因为相邻节点总有路径相连，因此我们无法通过反向的路径`[i, i-1]`来节省时间。因此这就给我们一个思路，即如果说两个点之间已有捷径相连，那么我们就可以不再考虑走任何这个捷径跨越的点。在经过这样的更改之后，我们的图总是一个从小到大连接的图；每次新增捷径，我们都可以删去，且此路径从头到尾的长度恰好为图里面节点的个数减一。为了快速找到要删除的路径，我们可以想象图为一个已排序列表，通过二分法来删去区间内所有元素。

这里我们利用了SortedList这个基于树的结构，来快速进行更改。我们通过二分法找到需要删除的区间，直接调用方法移除即可。

```python
from typing import List

class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        from sortedcontainers import SortedList
        def remove_range(sl, start, end):
            # Find the index of the first element greater than start
            start_index = sl.bisect_right(start) + 1
            # Find the index of the first element greater than end
            end_index = sl.bisect_right(end)

            if start_index <= end_index:
                # Remove elements in the range (start, end)
                del sl[start_index:end_index]

        
        sl = SortedList(range(n))

        for start, end in queries:
            remove_range(sl, start, end)
            # print(sl)
            yield len(sl) - 1
```

## 3245. Alternating Groups III 交替组 III

一些红蓝方块连续排列成环形（circular list），给定矩阵`color`代表其中每个方块是红色还是蓝色。给定一个列表的请求 `queries`，存在两种请求：第一种请求的形式为 `queries[i] = [1， size_i]` 需要查询指定长度的交替组的数量；第二种请求的形式为 `queries[i] = [2, index_i, color_i]` 需要改变指定索引`i`的元素颜色。从左到右处理所有请求，以列表的形式返回所有第一种查询的结果。交替组的定义为颜色交替且连续的一组方块。

遇到这种棘手的题目，我们先来思考一下暴力的解法。当处理类型为`2`的查询时，我们可以直接改变颜色；当处理类型为`1`的查询时，我们暴力的使用双指针来统计。要注意的是，我们处理的交替组是环形，因此在越界时候需要取模。

```python
class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        answer = []

        def count_alternating_groups(size):
            result = 0
            left = 0
            for right in range(n + size - 1):
                if left == right:
                    continue
                while right - left + 1 > size:
                    left += 1
                
                if colors[right % n] == colors[(right - 1) % n]:
                    left = right
                elif right - left + 1 == size:
                    result += 1
                    # print(f"\t counting: {left, right}")

            return result
        
        for query in queries:
            # print("handling", query, colors)
            if query[0] == 1:
                size = query[1]
                answer.append(count_alternating_groups(size))
            elif query[0] == 2:
                index = query[1]
                color = query[2]
                colors[index] = color
        
        return answer
```

这个算法的时间复杂度为`O(q * n)`，因为我们每次都要遍历整个数组来处理类型为`1`的查询。易得，进一步优化的方案当然是在处理类型为`2`的查询时，做额外的缓存。

如果我们能够知道组的长度，那么我们就能很快处理类型为`1`的查询。假设我们知道有`1`个长度为`2`的组，`2`个长度为`4`的组，和`1`个长度为`5`的组，那么也许他们长这样
```
RB BRBR RBRB BRBRB
-- ==== ---- =====
2  4    4    5
```
贼这种情况下，我们只储存最大的组的长度，因此我们可以看到每个组都不重叠。如果我们要查询长度为`4`的组，那么我们的结果为`4 = 1 + 1 + 2`，因为长度为`5`的组其实包含了两个长度为`4`的组。

在这种情况下，我们需要每次在处理类型为`2`的查询的时候，更新每个最大组的长度。显然，若更新的颜色与原来的颜色相同，我们可以忽略，因此我们只考虑不一样的情况。先来考虑一下一些基本情形。
```
colors = RBB
query = [2,2,R]
groups = {1: 1, 2: 1}
```
显然，我们在当前情形下，我们并无法直接更新`group`里储存的计数，因为我们没有任何关于索引为`2`前后的组的信息。因此，我们引入一个新的计数 `breaks`，储存所有组起始点的索引。对于上面的例子，我们有
```
colors = RBB
query = [2,2,R]
breaks = {0, 2}
```
其中，`break`里的每一个值代表了从当前点开始形成的组。给定任意一个点，我们总可以在`breaks`里面搜索他所属的组，以及他所属的组的相邻的组。在上面的例子中，我们可以查询到更新的索引`2`属于`2`这个组。他的前面是`0`这个组，且`0`这个组的长度为`2`，起始颜色为`R`，通过起始颜色和长度，我们可以推断出结束颜色为`B`。当我们更新相邻的`2`这个组的时候，我们可以把`2`也囊括进去。同理可得，当我们左右都有的时候
```
colors = RBBBR
query = [2,2,R]
breaks = {0, 2, 3}
groups = {1:1, 2:2}
```
当我们完成这个查询的时候，我们的结果应该是
```
colors = RBRBR
breaks = {0}
groups = {5:1}
```

别忘了，我们还需要处理删除的场景。还是上面那个例子
```
colors = RBRBR
query = [2,3,R]
breaks = {0}
groups = {5:1}
```
那么我们应该更新成
```
colors = RBRRR
breaks = {0, 3, 4}
groups = {1:2, 3:1}
```
其他的基本情形就不一一列举了。

注意到，这里我们对于`breaks`和`group`仅限于两种查询，一个是点查，一个是区域查询。因此我们可以灵活地采用基于树形结构的字典和集合。


```python
from sortedcontainers import SortedSet, SortedDict


class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)

        breaks = SortedSet()
        groups = SortedDict({2 * n: 1})

        def add(d: int, n: int) -> None:
            d = d % n
            if d > 2:
                groups[d] = groups[d] + 1 if d in groups else 1

        def erase(d: int, n: int) -> None:
            d = d % n
            if d > 2:
                groups[d] = groups[d] - 1 if d in groups else 1
                if groups[d] == 0:
                    del groups[d]

        def insert(i: int, n: int) -> None:
            if not breaks:
                groups.clear()
                groups[n] = 1
            elif len(breaks) == 1:
                j = breaks[0]
                groups.clear()
                groups[abs(i - j)] = 1
                groups[n - abs(i - j)] = groups[n - abs(i - j)] + \
                    1 if n - abs(i - j) in groups else 1
            else:
                idx = breaks.bisect_right(i)
                it3 = breaks[idx] if idx < len(breaks) else breaks[0]
                it1 = breaks[idx-1] if idx > 0 else breaks[-1]
                erase((it3 - it1) % n, n)
                add((it3 - i) % n, n)
                add((i - it1) % n, n)
            breaks.add(i)

        def remove(i: int, n: int) -> None:
            if len(breaks) == 1:
                groups.clear()
                groups[2 * n] = 1
            elif len(breaks) == 2:
                groups.clear()
                groups[n] = 1
            else:
                idx = breaks.index(i)
                it1 = breaks[idx-1] if idx > 0 else breaks[-1]
                it3 = breaks[idx+1] if idx < len(breaks)-1 else breaks[0]
                erase((i - it1) % n, n)
                erase((it3 - i) % n, n)
                add((it3 - it1) % n, n)
            breaks.remove(i)

        for i in range(n):
            if colors[i] == colors[(i + 1) % n]:
                insert(i, n)

        res = []
        for q in queries:
            if q[0] == 1:
                count = sum(v * (k - q[1] + 1)
                            for k, v in groups.items() if k >= q[1])
                res.append(min(n, count))
            elif colors[q[1]] != q[2]:
                idx = breaks.bisect_left(q[1])
                if idx < len(breaks) and breaks[idx] == q[1]:
                    remove(q[1], n)
                else:
                    insert(q[1], n)
                pi = (q[1] - 1) % n
                if colors[q[1]] != colors[pi]:
                    insert(pi, n)
                else:
                    remove(pi, n)
                colors[q[1]] = q[2]

        return res
```