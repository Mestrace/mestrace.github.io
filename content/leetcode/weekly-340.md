Title: 【Leetcode题解】Weekly Contest 340 周赛题目解析
Slug: weekly-340
Date: 2023-04-09 22:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Weekly Contest 340 第 340 场力扣周赛 | 2614. Prime In Diagonal 对角线上的质数 | 2615. Sum of Distances 等值距离和 | 2616. Minimize the Maximum Difference of Pairs 最小化数对的最大差值 | 2617. Minimum Number of Visited Cells in a Grid 网格图中最少访问的格子数 | Solution to contest problems 赛题讲解 ｜ Prefix Sum 前缀和 | Binary Search 二分搜索 ｜ BFS 广度优先搜索

[Weekly Contest 340](https://leetcode.com/contest/weekly-contest-340/)

[第 340 场周赛](https://leetcode.cn/contest/weekly-contest-340)

## 题目列表

- [2614. Prime In Diagonal](https://leetcode.com/problems/prime-in-diagonal/)
- [2615. Sum of Distances](https://leetcode.com/problems/sum-of-distances/)
- [2616. Minimize the Maximum Difference of Pairs](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/)
- [2617. Minimum Number of Visited Cells in a Grid](https://leetcode.com/problems/minimum-number-of-visited-cells-in-a-grid/)

## 2614. Prime In Diagonal 对角线上的质数

按照题意进行模拟即可。这里我们采用了一个朴素的便利方法进行求质数的操作，时间复杂度为$O(\sqrt(n))$。最后再按照题意检查对角线。

### 代码

```python
def isprime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

class Solution:
    def diagonalPrime(self, nums: List[List[int]]) -> int:
        result = 0
        for i in range(len(nums)):
            if isprime(nums[i][i]):
                result = max(result, nums[i][i])
            if isprime(nums[i][len(nums) - i - 1]):
                result = max(result, nums[i][len(nums) - i - 1])
        return result
```

## 2615. Sum of Distances 等值距离和

给定一个数组`nums`，需要返回一个结果数组`arr`。其中`arr[i]`的值需要这样求得：对于每一个满足`i != j`且`nums[i] == nums[j]`的索引`j`，求`i`对于每一个`j`的绝对值`abs(i  - j)` 的总和。

首先我们的第一反应应该是遍历`nums`并把值相同的索引归并成列表，然后再对每一个索引列表做上述的计算操作。给定一个索引列表`idxs`，我们可以用最简单遍历的方式去求上述结果要求的值，但这样最坏情况下的时间复杂度为$O(n^2)$。

```text
Example 1
Input: [1, 5, 8, 9]
Output:
1: 3 + 6 + 7 - 3 * 1 =>  19
5: (5 - 1) + (8 + 9 - 5 * 2)= 11
8: (8 * 2 - 1 - 5) + (9 - 8) = 11
9: 9 * 3 - 1 - 5 - 8 = 13
```

这里从例子中我们可以看到，上述的操作我们可以分为两部分，并且其中都包括对于`idxs`一个连续部分求和的操作。、假设对于索引`i`在`idxs`的位置为`k`，那么左边部分的结果就是`left = i * k - sum(idxs[:k])`，右边部分的结果为`right = sum(idxs[k + 1:]) - i * (len(idxs) - k)`。我们有两个求和操作，因此考虑用前缀和去求解。至于对于找到`i`在`idxs`的位置`k`，因为我们构建的时候顺序遍历数组找到的`idx`是顺序的，我们可以直接用二分搜索。

### 代码

```python
def prefixsum(l):
    prefix = [0] * (len(l) + 1)
    for i, n in enumerate(l):
        prefix[i + 1] = prefix[i] + n
    return prefix

class Solution:
    def distance(self, nums: List[int]) -> List[int]:
        d = defaultdict(list)
        for i, n in enumerate(nums):
            d[n].append(i)
        
        prefix = {n : prefixsum(l) for n, l in d.items()}

        result = [0] * len(nums)

        for i, n in enumerate(nums):
            idx = bisect_left(d[n], i)

            # print(i, n, d[n], idx, prefix[n], prefix[n][idx - 1])
            left = i * idx - prefix[n][idx]
            right = (prefix[n][-1] - prefix[n][idx]) - i * (len(d[n]) - idx)

            # print("\t", left, right)
            result[i] += left + right
        return result
```

## 2616. Minimize the Maximum Difference of Pairs 最小化数对的最大差值

给定一个数组`nums`和数字`p`，我们要在数组中匹配`p`对数使得所有对的差值的绝对值最小化。返回这`p`对数中最大的。此外，要注意每个数字只能使用一次。

对于给定的数组，我们可以对数组排序，那么前后两个数肯定是最小的。乍一看有点像是直接使用贪心的进行匹配，但是贪心并不能匹配到最优解。我们看一个例子。

```text
Example 1
Input: arr = [1, 5, 5, 7], p = 2
Output: 1
```
如果我们贪心匹配的话可能会得到`[5,5],[1,7] => 6`的差值，但实际最优解是`[1,5], [5,7] => 4`。此外，`p`的这个限制也比较困难，因为每个数字只能使用一次。如果我们能把最大值固定下来，是不是更好找呢？假设我们有一个固定的`m`最大值，我们可以通过贪心的判断`nums[i] - nums[j] < m`，从而判断是否将这部分数组囊括到最多`p`对数值里面。有了这个快速判断的方法，我们可以进一步使用二分搜索去寻找这个`m`。


### 代码

```python
{!content/leetcode/code/2616-minimize-the-maximum-difference-of-pairs.py!}
```


## 2617. Minimum Number of Visited Cells in a Grid 网格图中最少访问的格子数

给定一个`m x n`的矩阵`grid`，一开始出生点为左上角`(0,0)`。在每一个点`(i, j)`，我们可以向下或者向右走，可走到的格子跟`grid[i][j]`的值相关，

- 向右走：`(i, k)`且`j < k <= grid[i][j] + j`
- 向下走：`(k, j)`且`i < k <= grid[i][j] + i`

要求找到最少需要经过多少个格子才能走到右下角`(m - 1, n - 1)`。

这道题乍一看是简单的BFS或者DP，因为子问题组成了后续问题的答案。但我们不得不解决的一个问题是，我们不得不遍历`[j, min(grid[i][j] + j, n)]`或者`[i, min(grid[i][j] + i, m)]`个点去更新状态。这样的话总共时间复杂度为$O(m * n * (m + n))$，不可避免会TLE。因此我们想想能不能优化`O(m + n)`这一项。因为我们只要求最少的格子，使用BFS的方式，若`i -> k`先于`j -> k`出现的话，那么`i -> k`这一步的结果一定优于`j -> k`。这里可以类比一个无权重的图，先走到的那个步数一定最小。那么我们在找`j`的下一步的时候，其实是不用考虑之前已经经过的点`k`的。此外，我们也可以观察到，给定当前的行或者列，我们都是取连续的一段数作为我们下一个目标，因此我们这里使用维护sortedlist作为当前未被遍历到的行或者列，可以在$O(log(n))$时间找到连续的区间。剩下的就跟普通的BFS一样了。

### 代码

```python
from sortedcontainers import SortedList

class Solution:
    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        s0 = [SortedList(range(n)) for _ in range(m)]
        s1 = [SortedList(range(m)) for _ in range(n)]

        q = deque([(0, 0, 1)])

        while q:
            i, j, steps = q.popleft()

            if (i, j) == (m - 1, n -1):
                return steps
            
            for k in list(s0[i].irange(j + 1, min(j + grid[i][j], n - 1))):
                q.append((i, k, steps + 1))
                s0[i].remove(k)
                s1[k].remove(i)
            
            for k in list(s1[j].irange(i + 1, min(i + grid[i][j], m - 1))):
                q.append((k, j, steps + 1))
                s1[j].remove(k)
                s0[k].remove(j)
        return -1
```

## 小结

如果你想变得更强的话，可以做做

- [Easy - 1200. Minimum Absolute Difference](https://leetcode.com/problems/minimum-absolute-difference/)
- [Medium - 2602. Minimum Operations to Make All Array Elements Equal](https://leetcode.com/problems/minimum-operations-to-make-all-array-elements-equal/)（[Weekly Contest 338 我的解法]({filename}/leetcode/weekly-338.md)）
- [Medium - 1509. Minimum Difference Between Largest and Smallest Value in Three Moves](https://leetcode.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/)
- [Medium - Jumping Game](https://leetcode.com/problems/jump-game/)
- [Medium - 2594. Minimum Time to Repair Cars](https://leetcode.com/problems/minimum-time-to-repair-cars/)（[Biweekly Contest 100 我的解法]({filename}/leetcode/biweekly-100.md)）
- [Hard - 2604. Minimum Time to Eat All Grains](https://leetcode.com/problems/minimum-time-to-eat-all-grains/)（[我的解法]({filename}/leetcode/2604-minimum-time-to-eat-all-grains.md)）