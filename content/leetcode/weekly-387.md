Title: Weekly Contest 387 周赛题目解析
Slug: weekly-387
Date: 2024-03-03 22:00
Category: Leetcode
Tags: Contest
Summary: 2024-03 Leetcode Weekly Contest 387 第 387 场力扣周赛 | 3069. Distribute Elements Into Two Arrays I 将元素分配到两个数组中 I | 3070. Count Submatrices with Top-Left Element and Sum Less Than k 元素和小于等于 k 的子矩阵的数目 | 3071. Minimum Operations to Write the Letter Y on a Grid 在矩阵上写出字母 Y 所需的最少操作次数 | 3072. Distribute Elements Into Two Arrays II 将元素分配到两个数组中 II | Solution to contest problems 赛题讲解

[Weekly Contest 387](https://leetcode.com/contest/weekly-contest-387/)

[第 387 场周赛](https://leetcode.cn/contest/weekly-contest-387/)

复健第一周。题目不难，都属于是代码量较大，但是需要一点时间debug的题目。要是面试题跟今天的题目一样简单就好了。

## 题目列表

- [3069. Distribute Elements Into Two Arrays I 将元素分配到两个数组中 I](https://leetcode.com/problems/distribute-elements-into-two-arrays-i/description/)
- [3070. Count Submatrices with Top-Left Element and Sum Less Than k 元素和小于等于 k 的子矩阵的数目](https://leetcode.com/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/description/)
- [3071. Minimum Operations to Write the Letter Y on a Grid 在矩阵上写出字母 Y 所需的最少操作次数](https://leetcode.com/problems/minimum-operations-to-write-the-letter-y-on-a-grid/description/)
- [3072. Distribute Elements Into Two Arrays II 将元素分配到两个数组中 II](https://leetcode.com/problems/distribute-elements-into-two-arrays-ii/description/)

## 3069. Distribute Elements Into Two Arrays I 将元素分配到两个数组中 I

按照题义模拟，将数组分为两个数组即可。

```python
class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        arr1 = [nums[0]]
        arr2 = [nums[1]]
        
        for i in range(2, len(nums)):
            if arr1[-1] > arr2[-1]:
                arr1.append(nums[i])
            else:
                arr2.append(nums[i])
        return arr1 + arr2
```

## 3070. Count Submatrices with Top-Left Element and Sum Less Than k 元素和小于等于 k 的子矩阵的数目

前缀和，再统计大于`k`的个数即可。

```python
class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        dp = [[-1] * len(grid[0]) for _ in range(len(grid))]
        
        dp[0][0] = grid[0][0]
        
        if dp[0][0] > k:
            return 0
        
        for i in range(1, len(grid)):
            dp[i][0] = dp[i - 1][0] + grid[i][0]
            
        for j in range(1, len(grid[0])):
            dp[0][j] = dp[0][j - 1] + grid[0][j]
        
        for i in range(1, len(grid)):
            for j in range(1, len(grid[0])):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] + grid[i][j] - dp[i - 1][j - 1]
        
        result = 0
        for i in range(len(grid)):
            # print(i, dp[i])
            for j in range(len(grid[0])):
                if dp[i][j] <= k:
                    result += 1
        
        return result
```

## 3071. Minimum Operations to Write the Letter Y on a Grid 在矩阵上写出字母 Y 所需的最少操作次数

给定一个只有`0，1, 2`的`n x n`矩阵，需要在矩阵中画一个`Y`的形状，即从左上角，右下角和底部最中间相交都是同样的数字，且其他部分都为一样的另一个数字。你可以任意转换其中任意一个格子的数字。问最少转换次数。

由于都是线性的，直接模拟将`Y`上面的数字转换为`v`，而非`Y`的数字转换为`w`即可。

```python
class Solution:
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        counter = [0] * 3
        m = len(grid)
        
        for i in range(m):
            for j in range(m):
                counter[grid[i][j]] += 1
        
        # print("init", counter)
        # try write Y using v
        def check_y(v):
            # check Ys that are not v
            local_counter = list(counter) # copy
            
            result = 0
            
            # left diag
            for i in range(0, m // 2):
                if grid[i][i] != v:
                    result += 1
                local_counter[grid[i][i]] -= 1
            
            # right diag
            for i in range(0, m // 2):
                if grid[i][m - i - 1] != v:
                    result += 1
                local_counter[grid[i][m - i - 1]] -= 1
            
            # bot
            for i in range(m // 2, m):
                if grid[i][m // 2] != v:
                    result += 1
                local_counter[grid[i][m // 2]] -= 1
            
            # print(v, "result:", result)
            # print(v, local_counter)
            
            fresult = 1e9 + 7
            
            for w in range(3):
                if v == w:
                    continue
                fresult = min(fresult, result + local_counter[w] + local_counter[v])
            return fresult
        
        return min(check_y(v) for v in range(3))
```

## 3072. Distribute Elements Into Two Arrays II 将元素分配到两个数组中 II

这道题与第一题有点相似。都是将一个数组基于规则分配到两个不同的数组中。而本题的规则是比较`arr1`和`arr2`中大于当前数字`nums[i]`的个数。因此我们考虑使用一些排序的数据结构，比如AVL树和红黑树。这里可以直接使用科技`sortedcontainers`，直接按照题义模拟即可。

```python
class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        from sortedcontainers import SortedList
        
        orig1 = [nums[0]]
        orig2 = [nums[1]]
        arr1 = SortedList([nums[0]])
        arr2 = SortedList([nums[1]])
        
        for i in range(2, len(nums)):
            n = nums[i]
            
            idx1 = len(arr1) - arr1.bisect_right(n)
            idx2 = len(arr2) - arr2.bisect_right(n)
            
            if idx1 > idx2:
                arr1.add(n)
                orig1.append(n)
            elif idx1 < idx2:
                arr2.add(n)
                orig2.append(n)
            elif len(arr1) > len(arr2):
                arr2.add(n)
                orig2.append(n)
            else:
                arr1.add(n)
                orig1.append(n)
        
        return orig1 + orig2
```