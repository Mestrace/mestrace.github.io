Title: Weekly Contest 344 周赛题目解析
Slug: weekly-344
Date: 2023-05-08 22:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-05 Leetcode Weekly Contest 344 第 344 场力扣周赛 | 2670. Find the Distinct Difference Array 找出不同元素数目差数组 | 2671. Frequency Tracker 频率跟踪器 | 2672. Number of Adjacent Elements With the Same Color 有相同颜色的相邻元素数目 | 2663. Lexicographically Smallest Beautiful String 字典序最小的美丽字符串 | Solution to contest problems 赛题讲解 | Dijkstra's Algorithm 狄克斯特拉算法 | Lexicographic order 字典序

[Weekly Contest 344](https://leetcode.com/contest/weekly-contest-344/)

[第 344 场周赛](https://leetcode.cn/contest/weekly-contest-344/)

相比上周难得蛋疼，这周算是福利局。每道题都包含了一些实用小技巧，需要认真读题。

## 题目列表

- [Easy - 2670. Find the Distinct Difference Array](https://leetcode.com/problems/find-the-distinct-difference-array/)
- [Medium - 2671. Frequency Tracker](https://leetcode.com/problems/frequency-tracker/)
- [Medium - 2672. Number of Adjacent Elements With the Same Color](https://leetcode.com/problems/number-of-adjacent-elements-with-the-same-color/)
- [Medium - 2673. Make Costs of Paths Equal in a Binary Tree](https://leetcode.com/problems/make-costs-of-paths-equal-in-a-binary-tree/)

## 2670. Find the Distinct Difference Array 找出不同元素数目差数组

前缀和后缀和的twist，用一个set来取唯一元素。

```python
class Solution:
    def distinctDifferenceArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        left = [0] * len(nums)
        counter = set()
        for i, v in enumerate(nums):
            counter.add(v)
            left[i] = len(counter)
        
        right = [0] * len(nums)
        counter = set()
        for i in range(n - 2, -1, -1):
            counter.add(nums[i + 1])
            right[i] = len(counter)

        # print(right, left)

        result = [left[i] - right[i] for i in range(n)]

        return result
```
## 2671. Frequency Tracker 频率跟踪器

周赛比较少出现设计数据结构的题目。这道题还比较新奇。要求我们设计一个数据结构，可以支持添加一个数，删除一个数，和检查是否存在出现`frequency`次数的数字。这里我们直接用两个`map`来存即可。

```python
class FrequencyTracker:

    def __init__(self):
        self.counter = defaultdict(int)
        self.freq = defaultdict(set)

    def add(self, number: int) -> None:
        o = self.counter[number]
        self.counter[number] += 1
        if o > 0:
            self.freq[o].remove(number)
        self.freq[o + 1].add(number)
        

    def deleteOne(self, number: int) -> None:
        o = self.counter[number]
        if o == 0:
            return
        self.counter[number] -= 1
        self.freq[o].remove(number)
        if o - 1 > 0:
            self.freq[o - 1].add(number)
        

    def hasFrequency(self, frequency: int) -> bool:
        if frequency <= 0:
            return 0
        return len(self.freq[frequency]) > 0
```

## 2672. Number of Adjacent Elements With the Same Color 有相同颜色的相邻元素数目

初始的时候你有一个长度为`n`的`nums`数字列表，且里面颜色都为`0`，没有上色。给定一个查询列表`queries`，其中每一个为`[index, color]`。对于每一个`queries`，你要把`nums[index]`变成`color`的颜色，并求目前整个数组中相邻且相同的颜色的对数。注意审题。。。

先来简单看个例子
```
Input: n = 4, queries = [[0,2],[1,2],[3,1],[1,1],[2,1]]
Output: [0,1,1,0,2]
Explanation:
[0,0,0,0,0]
q = [0,2]
[2,0,0,0,0] => 0
q = [1,2]
[2,2,0,0,0] => 1
q = [3,1]
[2,2,0,1,0] => 1
q = [1,1]
[2,1,0,1,0] => 0
q = [2,1]
[2,1,1,1,0] => 2
```
这里我们发现，每次改`index`的颜色的时候，结果的变化只跟左右两边的颜色有关。因此直接给出`O(n)`模拟解法。

```python
class Solution:
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        nums, c = [0] * n, 0

        result = []

        for index, color in queries:
            prev = nums[index - 1] if index > 0 else 0
            next = nums[index + 1] if index < n - 1 else 0

            if nums[index] and nums[index] == prev:
                c -= 1
            if nums[index] and nums[index] == next:
                c -= 1
            
            nums[index] = color

            if nums[index] == prev:
                c += 1
            if nums[index] == next:
                c += 1
            result.append(c)
        
        return result
```

## 2673. Make Costs of Paths Equal in a Binary Tree 使二叉树所有路径值相等的最小代价

给定一棵以数组表示的完美二叉树，你可以对任意一个元素加一操作任意次。要求最少多少次操作使得每一条从根节点到叶子节点的路径的路径和都相等。

这里我们利用二叉树的性质可以推出，若当前所有路径和都相等，那么左右子树的路路径和也一定相等。下推到叶子节点可得，对于叶子节点的父节点，左右两个叶子节点一定相等。因此我们可以递归来做。

```python
class Solution:
    def minIncrements(self, n: int, cost: List[int]) -> int:
        result = 0
        def mini(i):
            if i - 1 >= len(cost):
                return 0
            
            left = mini(i * 2)
            right = mini(i * 2 + 1)

            diff = abs(left - right)
            
            nonlocal result
            result += diff

            # if diff > 0:
            #     print(i, left, right, diff)

            return cost[i - 1] + (left + right + diff) // 2
        
        mini(1)

        return result
```