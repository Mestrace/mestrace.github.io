Title: 【Leetcode题解】Biweekly Contest 103 双周赛题目解析
Slug: biweekly-103
Date: 2023-05-01 23:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Biweekly Contest 103 | 2656. Maximum Sum With Exactly K Elements K 个元素的最大和 | 2657. Find the Prefix Common Array of Two Arrays 找到两个数组的前缀公共数组 | 2658. Maximum Number of Fish in a Grid 网格图中鱼的最大数目 | 2659. Make Array Empty 将数组清空 | Solution to contest problems 赛题讲解 | DFS 深度优先搜索


[Biweekly Contest 103](https://leetcode.com/contest/biweekly-contest-103/)

[第 103 场双周赛](https://leetcode.cn/contest/biweekly-contest-103/)

前三题手速做完，最后一题想破头，已经成为了周赛的新常态了（大佬们除外）。第三题海王捞鱼题的难度还标错了，标准的DFS被标成了Hard，赛后又悄咪咪地变成了Medium。然后第四题看着人畜无害但是由于数据量的缘故收割了大量用户，不通过率高达`90.9%`。

## 题目列表

- [Easy - 2656. Maximum Sum With Exactly K Elements K 个元素的最大和](https://leetcode.com/problems/maximum-sum-with-exactly-k-elements/description/)
- [Medium - 2657. Find the Prefix Common Array of Two Arrays 找到两个数组的前缀公共数组](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays/)
- [Medium - 2658. Maximum Number of Fish in a Grid 网格图中鱼的最大数目](https://leetcode.com/problems/maximum-number-of-fish-in-a-grid/)
- [Hard - 2659. Make Array Empty 将数组清空](https://leetcode.com/problems/make-array-empty/)


## 2656. Maximum Sum With Exactly K Elements K 个元素的最大和

找到最大的元素，并加上`sum([0,1,...,k-1])`即可。

### 代码
```python
class Solution:
    def maximizeSum(self, nums: List[int], k: int) -> int:
        v = max(nums)
        
        return v * k + int((k - 1) * k / 2)
```

## 2657. Find the Prefix Common Array of Two Arrays 找到两个数组的前缀公共数组

题目给出的数据范围是`[0,50]`，因此用两个数组桶分别保存`A`和`B`里面数字出现频率。每次循环两个数组桶比对出现的前缀数量即可。

### 代码
```python
class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        va = [0] * 51
        vb = [0] * 51
        
        
        result = [0] * len(A)
        for i in range(len(A)):
            va[A[i]] += 1
            vb[B[i]] += 1
            
            for j in range(51):
                result[i] += min(va[j], vb[j])
        
        return result
```

## 2658. Maximum Number of Fish in a Grid 网格图中鱼的最大数目

标准的DFS题目。

### 代码
```python
class Solution:
    def findMaxFish(self, grid: List[List[int]]) -> int:
        DIR = [1, 0, -1, 0]
        
        def dfs(x, y):
            if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
                return 0
            if grid[x][y] == 0:
                return 0
            
            result = grid[x][y]
            grid[x][y] = 0
            
            for i in range(4):
                nx = x + DIR[i - 1]
                ny = y + DIR[i]
                
                result += dfs(nx, ny)
            
            return result
        
        result = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 0:
                    continue
                result = max(result, dfs(i, j))
        
        return result
```

## 2659. Make Array Empty 将数组清空

给定一个数组`nums`，其中每个数字都是唯一的。你可以对数组进行如下操作：1）若数组首个元素是当前的最小元素，则移除首个元素，2）否则把第一个元素移动到末尾。重复这个操作直到数组清空。问需要多少次操作才可以清空数组。

先思考一个朴素的方法。显然我们可以从小到大保存排序结果，并按照操作进行模拟。这样的时间复杂度的最坏情况为$O(n^2)$。给定的条件为`1 <= nums.length <= 10^5`，朴素解法肯定会超时。现在来思考，如果我们顺序遍历每个元素，我们有没有办法通过当前的条件来直接推断某个元素需要多少次才可以移除呢？先来看几个例子
```
Example 1
Input: nums = [3,4,-1]
Output: 5
Explanation:
-1: need to move 3, 4, then remove, ops = 3
3: remove, ops = 1
4: remove, ops = 1
```

```
Example 2
Input: nums = [1,2,4,3]
Output: 5
Explanation:
1: remove, ops = 1
2: remove, ops = 1
3: move 4, then remove, ops = 2
4: remove
```

在这两个例子中，我们看到，当我们需要移除第`i`个元素时，此时这个元素为最小的，则操作次数为这个元素前面的元素数量减去已经移除的元素数量，即在这个元素之前小于这个元素的。此外，另一个发现就是若第`i`个元素前面存在更大的元素时，这个元素永远会在`i`前面。再来看些更复杂的例子

```
Example 3
Input: nums = [5, 1, 4, 3, 2]
Output: 11
Explanation
1: move 5, remove, ops = 2
[4, 3, 2, 5]
2: move 4, 3, then remove, ops = 3
[5, 4, 3]
3 & 4 & 5: ops = 3 + 2 + 1 = 6
```

```
Example 4
Input: nums = [5, 1, 4, 3, 6, 2]
Output: 15
Explanation:
1: move 5, remove, ops = 2
[4, 3, 6, 2, 5]
2: move 4, 3, 6, remove, ops = 4
[5, 4, 3, 6]
3: move 5, 4, remove, ops = 3
[6, 5, 4]
4, 5, 6: ops = 3 + 2 + 1 = 6
```

这两个更复杂的例子中，我们可以更清晰直观的看到，移除第`i + 1`小的元素的操作次数与第`i`小和第`i + 1`小的元素中比`i + 1`大的元素数量相关。在例子4中，我们可以看到，`1`和`2`之间符合条件的元素为`[4,3,6]`。此外我们找的时候应该往左看，并且循环绕回末尾。如同样是例子4中，我们可以看到，`2`和`3`符合条件的元素为`[4,5]`。

如果到这里没问题的话，我们就可以来构造我们的算法了。首先我们需要知道原`nums`里索引的映射关系，然后再按照`nums`里的大小挨个移除每个索引。根据我们上面的推导，当我们移除第`i`小的元素时，需要考虑他与前一个元素之间的元素数量，因此有两种情况

- 当 $idx_{i - 1} < idx_{i}$ 时，需要计算 $nums[idx_{i - 1}:idx_i]$ 中大于 $nums[idx_i]$ 的元素个数。这可以通过计算总元素数量 $idx_{i} - idx_{i - 1}$ 减去已经移除的元素中数组下标区间**在** $[idx_{i - 1}, idx_{i}]$ 的元素数量。
- 当 $idx_{i - 1} > idx_{i}$，需要计算 $nums[:idx_i]$ 和 $nums[idx_{i - 1}:]$ 这两个区间中大于 $nums[idx_i]$ 的元素个数。这里可以通过计算总元素数量 $n - (idx_{i - 1} - idx_i)$ 减去已经移除的元素中数组下标区间**不在** $[idx_{i}, idx_{i - 1}]$的数量。

这里解释的比较拗口，读者们可以自行看代码进行理解。

这里我们看到，两个条件都要求给定两个索引，我们要找到这两个索引之间元素的数量。因此我们考虑使用排序结构去维护已经被移除的元素的索引。然后就可以通过二分搜索查找元素数量了。

### 代码
```python
from sortedcontainers import SortedList

class Solution:
    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        n = len(nums)
        
        # Get a list of indices sorted by their corresponding values in nums
        sorted_indices = sorted(list(range(n)), key=lambda x: nums[x])
        
        sorted_list = SortedList()
        
        # Calculate the initial result
        result = sorted_indices[0] + 1
        sorted_list.add(sorted_indices[0])
        
        for i in range(n - 1):
            current_index = sorted_indices[i]
            next_index = sorted_indices[i + 1]
            
            if current_index < next_index:
                left = sorted_list.bisect_left(current_index)
                right = sorted_list.bisect_left(next_index)
                
                result += (next_index - current_index) - (right - left - 1)
                
            else:
                left = sorted_list.bisect_left(next_index)
                right = sorted_list.bisect_left(current_index)
                
                result += n - (current_index - next_index) - (len(sorted_list) - 1 - (right - left))
            
            sorted_list.add(next_index)
        
        return result
```

## 小结

前三题手速提其实没什么可以分析的。第四题几乎很难被分类到某个具体的模板，需要理解题目意思之后观察才能快速AC。观察非常重要。

如果你想变得更强的话，可以做做

- [Easy - 118. Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/description/)
- [Medium - 2606. Find the Substring With Maximum Cost](https://leetcode.com/problems/find-the-substring-with-maximum-cost/description/) （双周赛101 [我的题解]({filename}/leetcode/biweekly-101.md)）
- [Hard - 2551. Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags/description/)