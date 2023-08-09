Title: Weekly Contest 357 周赛题目解析
Slug: weekly-357
Date: 2023-08-09 20:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 357 第 357 场力扣周赛 | 2810. Faulty Keyboard 故障键盘 | 2811. Check if it is Possible to Split Array 判断是否能拆分数组 | 2812. Find the Safest Path in a Grid 找出最安全路径 | 2813. Maximum Elegance of a K-Length Subsequence 子序列最大优雅度 | Solution to contest problems 赛题讲解 ｜ Dijkstra 迪科斯特拉算法 | Greedy 贪心算法

[Weekly Contest 357](https://leetcode.com/contest/weekly-contest-357/)

[第 357 场周赛](https://leetcode.cn/contest/weekly-contest-357/)

## 题目列表

- [2810. Faulty Keyboard 故障键盘](https://leetcode.com/problems/faulty-keyboard/)
- [2811. Check if it is Possible to Split Array 判断是否能拆分数组](https://leetcode.com/problems/check-if-it-is-possible-to-split-array/)
- [2812. Find the Safest Path in a Grid 找出最安全路径](https://leetcode.com/problems/find-the-safest-path-in-a-grid/)
- [2813. Maximum Elegance of a K-Length Subsequence 子序列最大优雅度](https://leetcode.com/problems/maximum-elegance-of-a-k-length-subsequence/)

## 2810. Faulty Keyboard 故障键盘

按照题意模拟即可。

```python
class Solution:
    def finalString(self, s: str) -> str:
        v = ''
        
        for c in s:
            if c == 'i':
                v = v[::-1]
            else:
                v += c
        
        return v
```

## 2811. Check if it is Possible to Split Array 判断是否能拆分数组

给定一个长度为`n`的数组`nums`，和一个整数`m`，你需要尝试通过一系列的拆分，每次把这个数组（或拆分后的子数组）拆分成两个新的子数组，直到不可再分。最终，你需要判断是否可以完全拆分（即每个子数组只有一个元素）。对于一个子数组进行拆分需要满足一定的条件：若拆分后的两个新子数组满足下列条件中的任一的，称之为合法的拆分

* 子数组长度为`1`，或
* 子数组元素总和大于等于`m`

最终需要返回`True`/`False`表明是否可以通过一系列合法拆分把数组变成单个元素。

这道题坑就坑在他的题目描述又长又臭，但是又很误导。比如是否可以把“长度为`n`的数组拆分成`n`个长度为`1`的子数组”。仔细看看，其实我们要关注的其实是是否可以分割的过程，即当中间某一步不可以执行的时候，需要返回`False`。

这里我们直接用DP来处理：

* 若子数组`nums[i:j]`没有元素，返回`False`
* 若子数组`nums[i:j]`有一个元素，返回`True`
* 若子数组`nums[i:j]`的和比`m`小，返回`False`
* 否则，尝试每一种分割方式

这里因为涉及到子数组求和，我们使用Prefix Sum来进行处理，即`sum(nums[i:j]) = prefix[j] - prefix[i]`。

还需要注意一个边界情况，当输入的子数组`nums`的长度为`1`或者`2`时，直接返回`True`即可。

```python
class Solution:
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        if len(nums) < 3:
            return True
        from itertools import accumulate
        prefix = [0] + list(accumulate(nums))
        
        from functools import cache
        @cache
        def bt(i, j):
            if i >= j:
                return False
            if i + 1 == j:
                return True
            elif prefix[j] - prefix[i] < m:
                # print(i, j, sum(nums[i:j]), prefix[j] - prefix[i])
                return False
            
            for idx in range(i, j):
                if bt(i, idx) and bt(idx, j):
                    return True
            
            return False
        
        return bt(0, len(nums))
```

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

实际上，一个隐秘的规律是：当数组中存在两个相邻元素的和大于`m`时，这样的分割就可以成功。并且这个是充分必要条件，因此我们直接检查即可。

```python
class Solution:
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        if len(nums) <= 2:
            return True
        for i in range(len(nums) - 1):
            if nums[i] + nums[i + 1] >= m:
                return True
        return False
```

## 2812. Find the Safest Path in a Grid 找出最安全路径

给定一个`n x n`的2D矩阵`grid`，其中`grid[r][c] = 0`代表空格，`grid[r][c] = 1`代表敌人。定义格子`(r,c)`的安全系数为这个格子离他当前敌人最近的曼哈顿距离，则一条路径的安全系数为路径上所有格子中最小的安全距离。要求出从`(0,0)`出发到达`(n-1,n-1)`最大安全系数的路径。

听上去很简单嘛。我直接正手一个Dijkstra。使用一个heap来维护当前到达的点，并优先走安全系数较大的点…… 我怎么知道每一个点的安全系数呢？有了，就用从每个敌人点出发的BFS吧！等一下，好像时间有点不够……

这道题最坑的地方在于，你要连续使用两个（类）BFS的方法去分别处理每个点的安全系数和最大安全系数的路径。如果平时对于BFS不熟练的话，要么就写不完，要么就会在某个地方卡壳出错，浪费掉大量的时间。

总之，回到我们的方法，分为两步走

1. 先使用BFS，从每一个敌人点出发，求出地图上每个点的安全系数
2. 再使用Dijkstra，从`(0,0)`出发，经由较大的点路径前往`(n-1,n-1)`。最终算的最大的安全系数。


```python
DIR = [1, 0, -1, 0, 1]

class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        
        def check(i, j):
            return i >= 0 and j >= 0 and i < m and j < n
        
        def computeSafenessMatrix():
            q = deque()
            mat = []
            for i in range(m):
                mat.append([-1] * n)
                for j in range(n):
                    if grid[i][j] == 1:
                        mat[i][j] = 0
                        q.append((i, j, 0))

            while q:
                x, y, d = q.popleft()
                
                for i in range(4):
                    nx = x + DIR[i]
                    ny = y + DIR[i + 1]
                    
                    # invalid
                    if not check(nx, ny):
                        continue
                    # visited
                    elif mat[nx][ny] != -1:
                        continue
                    mat[nx][ny] = d + 1        
                    q.append((nx, ny, d + 1))
                
            return mat
        
        safeness = computeSafenessMatrix()
        # print(safeness)
        
        # max queue
        from heapq import heappush, heappop
        q = []
        heappush(q, (-safeness[0][0], 0, 0))
        grid[0][0] = -1
        
        while q:
            ms, x, y = heappop(q)
            s = -ms
            
            if x == m - 1 and y == n - 1:
                return s
            
            for i in range(4):
                nx = x + DIR[i]
                ny = y + DIR[i + 1]

                # invalid
                if not check(nx, ny):
                    continue
                if grid[nx][ny] == -1:
                    continue
                grid[nx][ny] = -1
                
                heappush(q, (-min(safeness[nx][ny], s), nx, ny))
                
        return -1
```

## 2813. Maximum Elegance of a K-Length Subsequence 子序列最大优雅度

给定一个列表的`items`和整数`k`，其中每个`items[i]`包含了两个整数，`profit_i`代表了当前物品的价值，`category`是当前物品的类别。在`items`中选定`k`个物品组成的子序列的优雅度定义为`total_profit + distict_categories^2`，总价值加上独特类别个数的次方。要求任意长度为`k`的子序列所能组成的最大的优雅度。

直接看题目限制，`1 <= items.length == n <= 10^5`，`1 <= profit_i <= 10^9`可以推断出来这道题大概率要`O(n^2)`以下才可以，如果用`DP`的话大概率超时。又是个优化题，看看可不可以用贪心的方法入手。

显而易见，如果我们的优化目标只有`total_profit`的话，我们只需要排序后取前`k`个就可以了。考虑到`distinct_categories^2`大概率对于影响不大，我们排序后，可以优先取`total_profit`较高的，然后尝试把接下来的物品逐个替换上去，看看能不能对于独特类别这一项有帮助。

要注意的是，题目虽然要求的是子序列，但是没有要求连续的，因此实际上等价于随便取就好。搞不明白这题有什么难的……

```python
class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items = sorted(items, key=lambda v: -v[0])
        result = 0
        curr = 0
        array = []
        seen = set()
        for i, (profit, category) in enumerate(items):
            if i < k:
                if c in seen:
                    array.append(profit)
                curr += profit
            elif c not in seen:
                if not A:
                    break
                curr += profit - a.pop()
            seen.add(c)
            result = max(result, curr + len(seen) * len(seen))
        
        return result
```
