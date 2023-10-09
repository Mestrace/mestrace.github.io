Title: Weekly Contest 365 周赛题目解析
Slug: weekly-365
Date: 2023-10-05
Category: Leetcode
Tags: Contest
Summary: 2023-10 Leetcode Weekly Contest 365 第 365 场力扣周赛 | 2873. Maximum Value of an Ordered Triplet I 有序三元组中的最大值 I | 2874. Maximum Value of an Ordered Triplet II 有序三元组中的最大值 II | 2875. Minimum Size Subarray in Infinite Array 无限数组的最短子数组 | 2876. Count Visited Nodes in a Directed Graph 有向图访问计数 | Solution to contest problems 赛题讲解

[Weekly Contest 365](https://leetcode.com/contest/weekly-contest-365/)

[第 365 场周赛](https://leetcode.cn/contest/weekly-contest-365/)


## 题目列表

- [2873. Maximum Value of an Ordered Triplet I 有序三元组中的最大值 I](https://leetcode.com/problems/maximum-odd-binary-number/)
- [2874. Maximum Value of an Ordered Triplet II 有序三元组中的最大值 II](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-ii/)
- [2875. Minimum Size Subarray in Infinite Array 无限数组的最短子数组](https://leetcode.com/problems/minimum-size-subarray-in-infinite-array/)
- [2876. Count Visited Nodes in a Directed Graph 有向图访问计数](https://leetcode.com/problems/string-transformation/)

## 2873. Maximum Value of an Ordered Triplet I 有序三元组中的最大值 I

按照题意模拟即可。$O(n^3)。

```python
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        result = 0
        for i in range(0, len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    result = max(result, (nums[i] - nums[j]) * nums[k])
        return result
```

## 2874. Maximum Value of an Ordered Triplet II 有序三元组中的最大值 II

这道题跟上一题一样，只不过数据范围变成了`3 <= nums.length <= 10^5`，因此我们只能考虑一遍过的做法。

实际上，我们可以观察到，我们要用`i < j < k`之间最大的`nums[i] - nums[j]`。因此我们基于`k`进行循环，并分别保存当前遇到的最大的`nums[i]`和`nums[i] - nums[j]`。

```python
class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        maxab = 0
        maxa = 0
        result = 0

        for n in nums:
            result = max(result, maxab * n)
            maxab = max(maxab, maxa - n)
            maxa = max(maxa, n)
        
        return result
```

## 2875. Minimum Size Subarray in Infinite Array 无限数组的最短子数组

数组`nums`是一个无限循环数组`infinite_nums`循环的部分，要求找到最短的连续子数组使得子数组的和等于`target`。若此子数组不存在，则返回`-1`。

令数组`nums`的总和为`total = sum(nums)`，拼接`nums`两次之后的数组`nums2 = nums + nums`，则我们有`target = total * k + sum(nums2[i:j])`。我们可以很方便的推算`k = target // total`，则我们要找到`[i, j]`使得`sum(nums2[i:j]) = target % total`，同时使得`[i, j]`长度最小。为了快速计算任意`nums2`的区间综合，我们可以使用前缀和。定义`nums2`的前缀和数组为`prefix`，对于每一个`prefix[i]`，为了找到`prefix[j]`，既可以用便利的方式（当然会超时），也可以利用前缀和升序的性质，直接进行二分搜索找`prefix[j] = target % total + prefix[i]`。最终，我们可以在`O(nlog n)`的时间内找到结果。

```python
from typing import List
from bisect import bisect_left

class Solution:
    def minSizeSubarray(self, nums: List[int], target: int) -> int:
        n = len(nums)
        total = sum(nums)
        nums = nums + nums
        
        prefix = [0] * len(nums)
        prefix[0] = nums[0]
        for i in range(1, len(nums)):
            prefix[i] = prefix[i - 1] + nums[i]

        result = float('inf')
        
        for i in range(n):
            times = target // total
            rest = target % total
            
            # Binary search to find smallest j such that prefix[j] - prefix[i] >= rest.
            j = bisect_left(prefix, rest + prefix[i], i)
            
            # Check if we found a valid subarray and update our answer.
            if j < len(prefix) and times * total + prefix[j] - prefix[i] == target:
                result = min(result, j - i + times * n)

        return result if result != float('inf') else -1
```

## 2876. Count Visited Nodes in a Directed Graph 有向图访问计数

给定一个边列表`edges`定义的有向图，其中每一个`edges[i]`代表`i -> edges[i]`的一条边。你需要从每个节点`i`出发进行遍历直到你遇到一个已经经过的点位置，并数每一个节点`i`会经过多少个节点。

由题目可知，这个有向图中至少存在一个环。若存在多个环的话，则两个环是分别的两个图，也可以说是连通分量（Connected Components）。一看到这种题目就想到Cycle detection中的龟兔赛跑算法，但实际上在这里并不能够，因为我们还是要数有多少个的。

对于这道题，我们还是采用分而治之的手法。首先，对于环节点，我们可以直接沿着环走一圈来确定这个连通分量中的这个环的长度，则环中所有的节点的计数都为这个环的长度。其次，对于非环节点，我们可以把他们放进一个栈里面，直到我们找到一个已经有长度的节点为止。这个有计数和的节点既可能是一个环节点，也可能是一个前面已经计数的非环节点。接着我们就以栈的顺序累加计数即可。这样我们就确保了前面的计数结果可以重复利用，有一种动态规划的思想在里面。

如何区分环节点和非环节点呢？这里我们可以通过入度（Indegree）的方式来判断。在一个环中，节点的入度`indegree >= 1`。因此我们总可以从初始入度为`0`的节点开始，移除这个节点出发的所有边。我们重复这个过程直到没有入度为`0`的节点位置，通过这样的方式我们就可以区分环节点和非环节点了。进一步延伸，如果我们给每次移除的节点加上序号，我们还可以得到用来拓扑排序的Kahn算法。


```python
class Solution:
    def countVisitedNodes(self, edges: List[int]) -> List[int]:
        n = len(edges)
        # initial indegree
        degree = Counter(edges)
        kahn = set()
        queue = deque()

        # initial points in queue
        for x in range(n):
            if degree[x] == 0:
                queue.append(x)
        
        # Kahn's algorithm by popping outward edges of 0 indegree nodes
        while queue:
            x = queue.popleft()
            kahn.add(x)
            x = edges[x]
            degree[x] -= 1
            if degree[x] == 0:
                queue.append(x)
            
        result = [0] * n

        # for cycle nodes: iterate to find cycle length and nodes
        for x in set(range(n)) - kahn:
            if result[x] != 0:
                continue
            vals = []
            while not vals or x != vals[0]:
                vals.append(x)
                x = edges[x]
            for x in vals:
                result[x] = len(vals)
        
        # for non-cycle nodes: stack and +1 for each node in path
        for x in kahn:
            stack = []
            while result[x] == 0:
                stack.append(x)
                x = edges[x]
            while stack:
                result[stack[-1]] = 1 + result[x]
                x = stack.pop()
        return result
```