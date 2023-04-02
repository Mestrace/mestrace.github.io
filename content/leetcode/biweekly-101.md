Title: 【Leetcode题解】Biweekly Contest 101 双周赛题目解析
Slug: biweekly-101
Date: 2023-04-02
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Biweekly Contest 101 | 2605. Form Smallest Number From Two Digit Arrays 从两个数字数组里生成最小数字 | 2606. Find the Substring With Maximum Cost 找到最大开销的子字符串 | 2607. Make K-Subarray Sums Equal 使子数组元素和相等 | 2608. Shortest Cycle in a Graph 图中的最短环 | My solution 我的题目解析


这次双周赛难度不大，侮辱性极强。第三题和第四题完全是对调的难度，尽管一个是`Medium`一个是`Hard`。真的搞不懂出题人的思路了（<span title="你知道的太多了" class="heimu">他想让我死</span>）。

## 题目列表

- [Easy - 2605. Form Smallest Number From Two Digit Arrays](https://leetcode.com/problems/form-smallest-number-from-two-digit-arrays/)
- [Medium - 2606. Find the Substring With Maximum Cost](https://leetcode.com/problems/find-the-substring-with-maximum-cost/)
- [Medium - 2607. Make K-Subarray Sums Equal](https://leetcode.com/problems/make-k-subarray-sums-equal/)
- [Hard - 2608. Shortest Cycle in a Graph](https://leetcode.com/problems/shortest-cycle-in-a-graph/)


## 2606. Find the Substring With Maximum Cost 从两个数字数组里生成最小数字

第一题的要点：如果同一个数字在两个数组里都出现的话，那么这个数字必定最小；否则的话我们就看两个数组里最小的两个数字是否能组成最小的数。

### 代码

```python
class Solution:
    def minNumber(self, nums1: List[int], nums2: List[int]) -> int:
        nums1.sort()
        nums2.sort()
        
        nums3 = set(nums1).intersection(nums2)
        
        if nums3:
            return min(nums3)
        
        return min(nums1[0] * 10 + nums2[0], nums2[0] * 10 + nums1[0])
```

## 2606. Find the Substring With Maximum Cost 找到最大开销的子字符串

输入字符串`s`, `chars`和数组`vals`，其中`vals[i]`是`chars[i]`字母的分数。如果字母没有包含在`chars`里面，那么就按照他的`ascii`里的顺序来决定分数，比如`a = 1`，`b = 2`…… 最终，我们找到一个子字符串的组合使得分数最大。

这题其实是[53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)的变种，因为我们可以简单的根据三个入参转换为一个`nums`数组，这样我们的问题就是要求找到最大的子数组了。有两个需要注意的点：第一是对于负数的处理，第二是也可以取空集，这样分数就为0。这道题的解法主要是以[Kadine's Algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem#Kadane's_algorithm)来展开。这个解法有一些贪心的意味在里面。我们先来看个例子。

```
Example 1 
Input: [-1,-4,-5,4,1,2,-3]
Output: 7
```

这个例子里面我们很明显药跳过前面三个负数，从`4`开始取。那么我们只取正的子数组是不是就可以了呢？

```
Example 2
Input: [-1,1000,-5,4,1,2,-3]
Output: 1002
```

这个例子里面，我们又可以从`1000`，并且包含`-5`。当我们有一个绝对大的数字的时候，我们是可以选择性的囊括一些负数以期望获得更大的值的。无论如何，我们期望的是尽可能的囊括正数使得整个最大。

### 代码

```python
import string

class Solution:
    def maximumCostSubstring(self, s: str, chars: str, vals: List[int]) -> int:
        v = {chars[i] : vals[i] for i in range(len(chars))}
        for l in string.ascii_lowercase:
            if l in v:
                continue
            v[l] = int(ord(l)- ord('a') + 1)
        
        # print(v)
        
        nums = []
        for c in s:
            nums.append(v[c])
        
        curr = nums[0]
        result = nums[0]
        
        for i in range(1, len(nums)):
            num = nums[i]
            curr = max(num, curr + num)
            result = max(result, curr)
        
        return max(result, 0)
```

## 2607. Make K-Subarray Sums Equal 使子数组元素和相等

给定一个数字`arr`，可以对任意数字进行加减`1`的操作。我们期望找到最少次数的操作使得每个连续子数组的和都相等。此外，这个数组是循环的，也就是说我们数子数组的时候，数到末尾边界了的话需要从头开始继续算。

这题应该算是本次双周赛最难的题目了。我一开始的思路就是分case处理。有这么几种case

- 若`arr`的长度可以整除`k`，`arr`可以尽可能被调整为以`k`为单位循环的数组。
- 否则的话，就需要把所有的数字都变成相同的，而变为相同的最小情况是变为数组的中位数。

但是这样还是会有一些情况缺失。如下面这个例子

```
Example
Input: arr = [7,3,10,6,7,3,10,6], k = 6
Output: 12
```

在这个例子里面，有`8`个元素，而`k = 6`这样子的话。可以看到，第一个和第二子数组，`arr[0:6] = [7,...,3]`和`arr[1:7] = [3,...10]`，少了一个`7`多了一个`10`，因此这里`arr[0] = 7`和`arr[6] = 10`是要对齐的。而再挪动一位，我们需要把`arr[1] = 3`和`arr[7] = 6`进行对齐，`arr[2] = arr[8 % 8 = 0]`进行对齐，`arr[3] = arr[9 % 8 = 1]`。这样的话，我们需要变成一致的元素索引为`[0, 2, 4, 6]`和`[1, 3, 5, 7]`。这两个组里的元素需要变成一致的才可以。

```
Example
Input: arr = [7,3,10,6], k = 3
Output: 8
```

再来看一个例子，在这个例子里面，我们以同样的方法去检查哪些元素需要归成一组。因为`arr`长度为`4`而我们需要每`3`个都相等，因此我们没什么选择，只能把所有元素都归到同一组里面，即把整个组都变成`6`。

到这里的话，我们的思路大概就清晰了。我们通过上面这种方式把元素分组，然后每个组里的元素需要相等才可以。当然，你可以通过左右指针去做这件事情，但是这里我分享一个更高效的解法。实际上，我们能分的组数其实就是数组长度和`k`的最大公约数`gcd(len(arr), k)`。这样我们就可以利用这个循环数组的性质去找到最小的子集，使得我们的结果符合条件。

### 代码

```python
from collections import defaultdict
from math import gcd

class Solution:
    def makeSubKSumEqual(self, arr: List[int], k: int) -> int:
        
        k = gcd(k, len(arr))
        
        m = [[] for i in range(k)]
        
        
        for i, v in enumerate(arr):
            m[i % k].append(v)
        
        result = 0
        for a in m:
            a.sort()
            
            mid = a[len(a) // 2]
            
            for v in a:
                result += abs(v - mid)
        
        print(m)
        
        return result
```

## 2608. Shortest Cycle in a Graph 图中的最短环

给定一个无向图，我们需要找到里面最短的环。当然还有一些其他的条件，如每个点最多只有一条边，不过要解决这个问题的话都用不太上。

这道题实际上是相当标准的`bfs`做法。我们从任意点`i`出发，用一个queue来保存，并用一个列表来存某一个节点到`i`的距离。如果我们发现两个点都可以到达`i`的话，那么我们就找到了一个最短环。

### 代码

```python
from collections import deque

class Solution:
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]

        for i, j in edges:
            g[i].append(j)
            g[j].append(i)

        def root(i):
            dis = [inf] * n

            dis[i] = 0
            
            q = deque()

            q.append(i)

            while q:
                i = q.popleft()

                for j in g[i]:
                    if dis[j] == inf:
                        dis[j] = 1 + dis[i]
                        q.append(j)
                    elif dis[i] <= dis[j]:
                        return dis[i] + dis[j] + 1
            return inf
        
        result = inf
        for i in range(n):
            result = min(result, root(i))
        
        if result == inf:
            return -1
        return result
```


## 小结

总体来讲，这次第三题还是需要一点巧妙的思路的，题型也是不常见到的那种。

如果你想变得更强的话，可以看看

- [Directed Graph - Princeton COS 226 Spring 2007](https://www.cs.princeton.edu/courses/archive/spr07/cos226/lectures/20DirectedGraphs.pdf)里讨论了一下有向图的循环检测。
- [Graph Shortest Paths: Dijkstra and Bellman-Ford - UMD CMSC 451](https://www.cs.umd.edu/class/fall2017/cmsc451-0101/Lects/lect05-graph-shortest-path.pdf)里探讨了对于加权图的解决方法，如Dijstra和Bellman Ford。


如果你想变得更强的话，可以做做

- [Medium - 53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/)
- [Medium - 189. Rotate Array](https://leetcode.com/problems/rotate-array/)
- [Medium - 684. Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- [Hard - 2360. Longest Cycle in a Graph](https://leetcode.com/problems/longest-cycle-in-a-graph/)
- [Hard - 2493. Divide Nodes Into the Maximum Number of Groups](https://leetcode.com/problems/divide-nodes-into-the-maximum-number-of-groups/)