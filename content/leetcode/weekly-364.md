Title: Weekly Contest 364 周赛题目解析
Slug: weekly-364
Date: 2023-10-01
Category: Leetcode
Tags: Contest
Summary: 2023-09 Leetcode Weekly Contest 364 第 364 场力扣周赛 | 2864. Maximum Odd Binary Number 最大二进制奇数 | 2865. Beautiful Towers I 美丽塔 I | 2866. Beautiful Towers II 美丽塔 II | 2867. Count Valid Paths in a Tree 统计树中的合法路径数目 | Solution to contest problems 赛题讲解

[Weekly Contest 364](https://leetcode.com/contest/weekly-contest-364/)

[第 364 场周赛](https://leetcode.cn/contest/weekly-contest-364/)


## 题目列表

- [2864. Maximum Odd Binary Number 最大二进制奇数](https://leetcode.com/problems/maximum-odd-binary-number/)
- [2865. Beautiful Towers I 美丽塔 I](https://leetcode.com/problems/beautiful-towers-i/)
- [2866. Beautiful Towers II 美丽塔 II](https://leetcode.com/problems/beautiful-towers-ii/)
- [2867. Count Valid Paths in a Tree 统计树中的合法路径数目](https://leetcode.com/problems/count-valid-paths-in-a-tree/)

## 2864. Maximum Odd Binary Number 最大二进制奇数

<span title="你知道的太多了" class="heimu">找1</span>

```python
class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        c = Counter(s)
        
        return (c['1'] - 1) * '1' + (c['0']) * '0' + '1'
```

## 2865. Beautiful Towers I 美丽塔 I

你需要构建一个塔的列表使得所有塔满足以下两个约束条件

- 位置`i`的塔的高度不能超过`maxHeight[i]`。
- 所有的塔构成一个**山形**，即两边的塔不能高过中间的塔。

最终，你需要返回最大的高度总和。

看到`1 <= n <= 10^3`的数量级，直接暴力做就可以。我们选定一个位置`i`，以它最高高度`maxHeight[i]`为基准，分别计算并累加左右两边更矮的塔的高度，以求得当前的高度综合。我们对于每一个点`i`都重复这个动作以求得最终结果。搞掂！

```python
class Solution:
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        n = len(maxHeights)
        result = 0
        
        for peak in range(n):
            # print("peak", peak)
            peak_result = maxHeights[peak]
            # print("left")
            last_height = maxHeights[peak]
            for left in range(peak - 1, -1, -1):
                last_height = min(maxHeights[left], last_height)
                peak_result += last_height
                # print("left", left, last_height)
            
            # print("right")
            last_height = maxHeights[peak]
            for right in range(peak + 1, n):
                last_height = min(maxHeights[right], last_height)
                peak_result += last_height
                # print("right", right, last_height)
            
            # print("peak", peak, peak_result)
            result = max(result, peak_result)
        
        return result
```

## 2866. Beautiful Towers II 美丽塔 II

这题干跟上一道题[2865. Beautiful Towers I 美丽塔 I](https://leetcode.com/problems/beautiful-towers-i/)一毛一样，唯一的区别就是数据范围变为了`1 <= n <= 10^5`。说实话，就这个小小的区别就让这道题变成了这场周赛最难的一题，我是没想到的。

从上一题可以看出来，每一次我们选择`i`为最高点`peak = maxHeights[i]`的时候，我们都计算左边和右边限制高度为`peak`所形成的山峰总高度。这个过程中，我们做了很多的重复计算，我们需要针对这一点进行优化。那么，我们怎么计算左边（或右边）的山峰高度，使得前面的计算结果可以被重复利用呢？我们先从左边开始算起。

我们知道，对于左边已有的部分`[:i]`，我们的总高度是被`maxHeights[i]`限制的。当我们想要添加一个`maxHeights[i + 1]`的时候，会出现两种情况：

1. `maxHeights[i + 1] >= maxHeights[i]`，这种情况我们直接累加到总高度即可。
2. `maxHeights[i + 1] < maxHeights[i]`，我们需要持续移除高于`maxHeights[i + 1]`的山峰，直到满足第一个条件为止。此时，所有在左边高于`maxHeights[i + 1]`的山峰的高度最高只能为`maxHeights[i + 1]`。

那么，这是不是就意味着我们需要记录前面所有山峰的长度呢？非也非也，我们可以通过乘数来表示。仔细思考一下，若一个区间`maxHeights[i:j]`都被`maxHeights[j + 1]`限制，那么这个区间的高度就可以直接用`(j - i + 1)`区间中间的元素个数与`maxHeights[j + 1]`相乘计算出来。还有，别忘了最左（或最右）的边界情况！

这样子，是不是和单调栈的概念十分相似了！我们左到右遍历每一个索引，其中单调栈中只储存限制区间的索引，即`maxHeights[stack[-2]:stack[-1]]`中的每一个元素都被`maxHeights[stack-1]`限制。右边的算法也同理。

```python
class Solution:
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        # monotonic stack from the left to keep track
        # of the heights to the left
        stack = []
        total = 0
        left_sum = [0 for _ in maxHeights]
        for i in range(len(maxHeights)):
            while stack and maxHeights[stack[-1]] > maxHeights[i]:
                j = stack.pop()
                if stack:
                    multiplier = j - stack[-1]
                else:
                    multiplier = j + 1
                
                total -= maxHeights[j] * multiplier
            
            if stack:
                multiplier = i - stack[-1]
            else:
                multiplier = i + 1
            
            total += maxHeights[i] * multiplier
            left_sum[i] = total
            stack.append(i)
        
        # monotonic stack to compute the right side
        stack = []
        total = 0
        result = 0
        for i in range(len(maxHeights) - 1, -1, -1):
            while stack and maxHeights[stack[-1]] > maxHeights[i]:
                j = stack.pop()
                if stack:
                    multiplier = stack[-1] - j
                else:
                    multiplier = len(maxHeights) - j

                total -= maxHeights[j] * multiplier

            if stack:
                multiplier = stack[-1] - i
            else:
                multiplier = len(maxHeights) - i
            
            total += maxHeights[i] * multiplier
            # left_sum is inclusive of maxHeights[i], need to subtract from
            result = max(result, total + left_sum[i] - maxHeights[i])
            stack.append(i)
        
        return result
```

## 2867. Count Valid Paths in a Tree 统计树中的合法路径数目

给定一个边列表`edges`定义的树，其中`edges[i] = [u, v]`定义了树中连通的一条边。定义树中两个节点的合法路径的条件为这条路径上的节点序号有且只有一个是质数。求这棵树中的合法路径数量。

在这棵树中，质数集合把非质数集合切分成多个子树。我们通过广度优先搜索遍历所有非质数，并将他们分成不相交的组 $\mathbb{G} = {G_1, G_2,...}$，这个分割使得每两组质数 $G_i$ 和 $G_j$ 所形成的路径中必有至少一个质数。

接下来我们考虑计算。在构建上面的组的同时，我们也可以构建质数与组之间的连接。当我们知道一个质数$p$与多个组相连的时候，可以形成的两种路径为组里的每个元素与这个质数直接相连形成的路径，或组与组之间两两配对跨越这个质数所形成的路径。

接下来就是如何计算质数了。这里要求`10^5`，不能用打表的方式计算，我们直接用线性的`Sieve`算法计算。我在前面几期也讲过一些计算质数相关的题目，感兴趣的读者可以参考：

- 朴素：[Weekly Contest 340]({filename}/leetcode/weekly-340.md)
- Sievie：[Weekly Contest 352]({filename}/leetcode/weekly-352.md)
- 打表：
    - [2584. Split the Array to Make Coprime Products]({filename}/leetcode/2584-split-the-array-to-make-coprime-products.md)
    - [Weekly Contest 338]({filename}/leetcode/weekly-338.md)
    - [Weekly Contest 358]({filename}/leetcode/weekly-358.md)

```python
class Solution:
    def sieve_of_eratosthenes(self):
        sieve = [0, 0] + [1] * (self.MAX_N - 1)
        for x in range(2, int(self.MAX_N**0.5) + 1):
            if sieve[x]:
                for u in range(x*x, self.MAX_N + 1, x):
                    sieve[u] = 0
        return {num for num in range(2, self.MAX_N + 1) if sieve[num]}

    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        self.MAX_N = n + 1
        self.primes = self.sieve_of_eratosthenes()

        prime_groups = [-1] * (n + 1)
        prime_connections = defaultdict(set)

        # adj
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        
        # bfs on non-prime number
        def bfs(group, i):
            nonlocal prime_groups
            nonlocal prime_connections
            q = deque([i])
            prime_groups[i] = group

            while q:
                e = q.pop()
                for nei in adj[e]:
                    if nei in self.primes:
                        prime_connections[nei].add(group)
                        continue
                    if prime_groups[nei] != -1:
                        # safe guard
                        assert prime_groups[nei] == group
                        continue
                    prime_groups[nei] = group
                    q.append(nei)
        
        group_id = 1000
        for i in range(1, n + 1):
            if prime_groups[i] != -1:
                continue
            if i in self.primes:
                continue
            bfs(group_id, i)
            group_id += 1

        group_counter = Counter(prime_groups)
        # print(prime_groups)
        # print(group_counter)
        # print(prime_connections)

        result = 0

        for p, groups in prime_connections.items():
            for g in groups:
                result += group_counter[g]

            while groups:
                g1 = groups.pop()
                for g2 in groups:
                    result += group_counter[g1] * group_counter[g2]
            result %= int(1e9 + 7)
        
        return result
```

等下，还没完。啪的一下，就TLE了，问题到底出在哪里！

一通debug之后，我发现我的问题出在最后计算组的数量上。我这个朴素遍历法最终会有`O(n^2)`的时间复杂度。一通优化之后，成功AC。

```python
        ...
        for p, groups in prime_connections.items():
            prev = 1
            for g in groups:
                result += prev * group_counter[g]
                prev += group_counter[g]
        return result
```