Title: Weekly Contest 353 周赛题目解析
Slug: weekly-353
Date: 2023-07-15 12:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 353 第 353 场力扣周赛 | 2769. Find the Maximum Achievable Number 找出最大的可达成数字 | 2770. Maximum Number of Jumps to Reach the Last Index 达到末尾下标所需的最大跳跃次数 | 2771. Longest Non-decreasing Subarray From Two Arrays 构造最长非递减子数组 | 2772. Apply Operations to Make All Array Elements Equal to Zero 使数组中的所有元素都等于零 | Solution to contest problems 赛题讲解 | 动态规划 Dynamic Programming | 线段树 Segment Tree | 差分数组 Difference Array

[Weekly Contest 353](https://leetcode.com/contest/weekly-contest-353/)

[第 353 场周赛](https://leetcode.cn/contest/weekly-contest-353/)

经典手速场但最后一题是Medium。

## 题目列表

- [2769. Find the Maximum Achievable Number 找出最大的可达成数字](https://leetcode.com/problems/find-the-maximum-achievable-number/)
- [2770. Maximum Number of Jumps to Reach the Last Index 达到末尾下标所需的最大跳跃次数](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/)
- [2771. Longest Non-decreasing Subarray From Two Arrays 构造最长非递减子数组](https://leetcode.com/problems/longest-non-decreasing-subarray-from-two-arrays/)
- [2772. Apply Operations to Make All Array Elements Equal to Zero 使数组中的所有元素都等于零](https://leetcode.com/problems/apply-operations-to-make-all-array-elements-equal-to-zero/)

## 2769. Find the Maximum Achievable Number 找出最大的可达成数字

想题十分钟，做题两秒钟。

```python
class Solution:
    def theMaximumAchievableX(self, num: int, t: int) -> int:
        return num + 2 * t
```

## 2770. Maximum Number of Jumps to Reach the Last Index 达到末尾下标所需的最大跳跃次数

给定数字列表`nums`和目标数字`target`，如`i < j`且`abs(nums[j] - nums[j]) <= target`，则可以从`i`移动到`j`，问从索引`0`开始最多需要跳跃多少次能到达数组末尾`n - 1`。

先`O(n^2)`构图，再dp求最大。

```python
class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        g = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(nums[i] - nums[j]) > target:
                    continue
                g[i].append(j)
        
        # print(g)
        
        from functools import cache
        
        @cache
        def dp(i):
            if i == len(nums) - 1:
                return 0
            
            result = -1
            for nei in g[i]:
                nxt = dp(nei)
                if nxt == -1:
                    continue
                result = max(result, 1 + nxt)
            return result
            
        
        return dp(0)
```

## 2771. Longest Non-decreasing Subarray From Two Arrays 构造最长非递减子数组

给定同样长度的整数数组`nums1`和`nums2`，需要从`nums1`和`nums2`每个位置`i`挑选其中一个数字构造`nums3`。问在最优选择下`nums3`的最长连续非递减序列的长度。

题目出现了”最优选择“，我们应该第一时间想到DP。先思考一个最简单的形式，若`nums3[:i]`已经是最优选择了，此时我们要添加一个数字`x`，则我们只需要判断`nums3[i]`跟`x`的大小，就可以判断是否可以添加。接着我们考虑，若只基于`nums1`里的数字将`nums2`里的数字替换进去，那么在每个`nums1[i]`我们需要判断`nums1[i - 1]`和`nums2[i - 1]`的大小，并选择其中一个添加到我们的队列里来。将这种情况扩展到`nums2`里来，就形成了我们的答案。

```python
class Solution:
    def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        dp = [[1]*2 for _ in range(n)]
        
        result = 1
        
        for i in range(1, n):
            # check for nums1[i]
            if nums1[i] >= nums1[i-1]:
                dp[i][0] = max(dp[i][0], dp[i-1][0] + 1)
            if nums1[i] >= nums2[i-1]:
                dp[i][0] = max(dp[i][0], dp[i-1][1] + 1)
            # check for nums2[i]
            if nums2[i] >= nums1[i-1]:
                dp[i][1] = max(dp[i][1], dp[i-1][0] + 1)
            if nums2[i] >= nums2[i-1]:
                dp[i][1] = max(dp[i][1], dp[i-1][1] + 1)

            result = max(result, dp[i][0], dp[i][1])

            
        # print(dp)
        return result
```

## 2772. Apply Operations to Make All Array Elements Equal to Zero 使数组中的所有元素都等于零

给定一个数组`nums`和正整数`k`，在每次操作中，你可以选择`nums`内任意长度为`k`的连续字数组并将他们所有的值减去`1`。你可以操作任意多次这个操作，问是否可以将`nums`内的所有数字都变成`0`。

不说废话，先来一个暴力解法。首先可以很直观的看出来，我们只要贪心的遍历整个数组所有长度为`k`的连续子数组，并将每个子数组里的元素减去第一个元素的值，就可以得到答案。那么，我们的答案看起来是这样子的：

```python
class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        for i in range(n):
            if nums[i] > 0:
                # Check if there are enough elements to form a subarray of size k
                if i + k > n:
                    break
                v = nums[i]
                # Decrease nums[i] from every element in the subarray of size k
                for j in range(i, i+k):
                    nums[j] -= v
                    if nums[j] < 0:
                        return False
        return all(num == 0 for num in nums)
```

考虑到`10^5`的元素数量，而我们的算法的时间复杂度是`O(n*k)`，这样肯定是会TLE的。

外层的循环肯定不能少，因为我们要贪心遍历整个数组。但是我们能不能从内部循环减去`k`的地方下手呢？联系到数据结构的性质，我们需要找到一个数据结构能够小于`O(k)`的时间复杂度里将数组区间内的数字减少某个值。这里我们展示一个使用惰性求值的线段树的做法。

首先我们知道，线段树有三个组成部分：

1. `build`构建树：需要开一个`4 * n`的数组来储存线段树。线段树本身是一个二叉树结构，其中`n`个元素是数组的原值，会被放在线段树的叶子节点，其他节点则是左右子树的和。这样做之后，根节点就会是数组的和。
2. `update`更新树：我们从树的根节点开始递归，更新每个节点的值。这里我们是把选定区间内每个元素的值都减去`v`，因此，在每个节点我们都减去当前节点代表的区间元素个数`p * v`。
3. `query`查询树：这里我们查询每个数组`i`的值，即沿着线段树的节点走到叶子节点，并返回叶子节点的值。

聪明的同学可能会说了：`update`和`query`反而增加了时间复杂度啊！这个怎么能算作优化呢？先别急，我们从性质考虑。我们知道，朴素解法中，对于每个元素的减法我们是立即求值的，也就是每减去一个数字，我们就要用`O(k)`的时间遍历一遍。但是实际上，我们可能很久之后才会用到，所以我们可以利用线段树的性质来稍做更改来进行惰性求值。

1. `build`构建树：开辟一个`4 * n`的数组来储存每个节点惰性减去的值。即`lazy[i]`为`tree[i]`所代表的区间里面每一个元素要减去的值。
2. `update`更新树：若对应长度能够覆盖更新范围，我们就只递归到当前节点。怎么理解呢？我们分类讨论：
    1. 若当前区间刚好等于我们要更新的区间，那么我们就不需要接着往下更新了，不需要每次都更新到叶子节点。
    2. 若当前区域跟我们的区间有重叠部分，那么就二分递归，直到递归到情况`1`为止。
    3. 若没有重叠部分，则不需要更新，直接返回。
3. `query`查询树：这里我们就把惰性更新的值真正应用到每个节点上面，并且下推到左右节点的惰性更新里面，直到我们下推到叶子节点为止。

这里只是高屋建瓴的讨论了一下线段树的本质，实际上还有很多变种，在各种题目里面都需要做相应的修改，这里就不一一讨论了，感兴趣的同学可以参阅：

- [OI Wiki - 线段树 - 线段树的区间修改与懒惰标记](https://oi-wiki.org/ds/seg/#线段树的区间修改与懒惰标记)
- [CP Algorithms - Segment Tree - Range updates (Lazy Propagation)](https://cp-algorithms.com/data_structures/segment_tree.html#range-updates-lazy-propagation)


```python
class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        sg = SegmentTree(n)
        sg.build(0, 0, n - 1, nums)
        total_sum = sg.query(0, 0, n - 1, 0, n - 1)
        if total_sum % k != 0:
            return False
        
        for i in range(n):
            curr = sg.query(0, 0, n - 1, i, i)
            if curr < 0:
                return False
            if curr == 0:
                continue
            if i + k - 1 <= n - 1:
                sg.update(0, 0, n - 1, i, i + k - 1, -curr)
            else:
                if curr != 0:
                    return False
        
        return True

class SegmentTree:
    def __init__(self, n):
        self.seg = [0] * (4 * n + 1)
        self.lazy = [0] * (4 * n + 1)

    def build(self, idx, low, high, arr):
        if low == high:
            self.seg[idx] = arr[low]
            return

        mid = low + (high - low) // 2
        self.build(2 * idx + 1, low, mid, arr)
        self.build(2 * idx + 2, mid + 1, high, arr)
        self.seg[idx] = self.seg[2 * idx + 1] + self.seg[2 * idx + 2]

    def update(self, idx, low, high, l, r, val):
        # Lazy propagation
        if self.lazy[idx] != 0:
            self.seg[idx] += (high - low + 1) * self.lazy[idx]
            if low != high:
                self.lazy[2 * idx + 1] += self.lazy[idx]
                self.lazy[2 * idx + 2] += self.lazy[idx]
            self.lazy[idx] = 0

        # No overlap
        if l > high or r < low:
            return

        # Complete overlap
        if low >= l and high <= r:
            self.seg[idx] += (high - low + 1) * val
            if low != high:
                self.lazy[2 * idx + 1] += val
                self.lazy[2 * idx + 2] += val
            return

        # Partial overlap
        mid = low + (high - low) // 2
        self.update(2 * idx + 1, low, mid, l, r, val)
        self.update(2 * idx + 2, mid + 1, high, l, r, val)
        self.seg[idx] = self.seg[2 * idx + 1] + self.seg[2 * idx + 2]

    def query(self, idx, low, high, l, r):
        # Lazy propagation
        if self.lazy[idx] != 0:
            self.seg[idx] += (high - low + 1) * self.lazy[idx]
            if low != high:
                self.lazy[2 * idx + 1] += self.lazy[idx]
                self.lazy[2 * idx + 2] += self.lazy[idx]
            self.lazy[idx] = 0

        # No overlap
        if high < l or low > r:
            return 0

        # Complete overlap
        if low >= l and high <= r:
            return self.seg[idx]

        # Partial overlap
        mid = low + (high - low) // 2
        left = self.query(2 * idx + 1, low, mid, l, r)
        right = self.query(2 * idx + 2, mid + 1, high, l, r)

        return left + right
```

**你以为到这里就结束了？**

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

观摩线段树的解法，似乎区间求和的部分基本没有用到，我们能不能省略掉啊？

这里我们直接用一个差分数组Difference Array的技巧来储存之前的更新值。看一个差分数组的例子
```
Example: 
nums = [8,5,9,6,1]
diff = [0,0,0,0,0]
subtract 2 from nums[1,4]
diff = [0,2,0,0,-2]
actual_diff = [0,2,2,2,-2]
```
这里`diff`就是我们的差分数组，且我们可以通过差分数组前一个值推出后一个应该减去的值。

差分数组在挤到简单的题目中都有应用，可以看看下面的题目

- [Medium - 370. Range Addition](https://leetcode.com/problems/range-addition/)
- [Easy - 598. Range Addition II](https://leetcode.com/problems/range-addition-ii/)
- [Medium - 2718. Sum of Matrix After Queries](https://leetcode.com/problems/sum-of-matrix-after-queries/)

```python
class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        d = [0] * (n + 1)
        
        for i in range(n):
            if i > 0:
                d[i] += d[i - 1]
            
            diff = nums[i] - d[i]
            if diff < 0:
                return False
            
            if i + k > n:
                if diff != 0:
                    return False
                else:
                    continue
            
            d[i] += diff
            d[i + k] -= diff
            # print(diff, n, d)
        
        return True
```
