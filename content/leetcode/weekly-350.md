Title: Weekly Contest 350 周赛题目解析
Slug: weekly-350
Date: 2023-06-18 23:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-06 Leetcode Weekly Contest 350 第 350 场力扣周赛 | 2739. Total Distance Traveled 总行驶距离 | 2740. Find the Value of the Partition 找出分区值 | 2741. Special Permutations 特别的排列 | 2742. Painting the Walls 给墙壁刷油漆 | Solution to contest problems 赛题讲解 | Weighted Graph 有权图

[Weekly Contest 350](https://leetcode.com/contest/weekly-contest-350/)

[第 350 场周赛](https://leetcode.cn/contest/weekly-contest-350/)

## 题目列表

- [2739. Total Distance Traveled 总行驶距离](https://leetcode.com/problems/total-distance-traveled/)
- [2740. Find the Value of the Partition 找出分区值](https://leetcode.com/problems/find-the-value-of-the-partition/)
- [2741. Special Permutations 特别的排列](https://leetcode.com/problems/special-permutations/)
- [2742. Painting the Walls 给墙壁刷油漆](https://leetcode.com/problems/painting-the-walls/)

## 2739. Total Distance Traveled 总行驶距离

根据题意模拟即可。这里直接尝试用光`mainTank`里面的油，并把`additionalTank`里的油尽可能多的放到`mainTank`里面来。

```python
class Solution:
    def distanceTraveled(self, mainTank: int, additionalTank: int) -> int:
        total_distance = 0
        while mainTank > 0:
            # if the main tank has less than 5 liters, use up all the fuel in the main tank
            if mainTank < 5:
                total_distance += mainTank * 10
                mainTank = 0
            else:
                consumed = mainTank // 5 * 5
                total_distance += consumed * 10

                mainTank -= consumed

                if additionalTank:
                    refueled = min(additionalTank, consumed // 5)
                    mainTank += refueled
                    additionalTank -= refueled
        
        return total_distance
```

## 2740. Find the Value of the Partition 找出分区值

无论如何我们都能找到一种排序后的分法使得分区值最小，因此排序之后找最小的差值即可。

```python
class Solution:
    def findValueOfPartition(self, nums: List[int]) -> int:
        nums.sort()
        
        return min(nums[i] - nums[i - 1] for i in range(1, len(nums)))
```

## 2741. Special Permutations 特别的排列


若一个数组列表中对于每个`i`，`nums[i] % nums[i + 1] == 0`或者`nums[i + 1] % nums[i] == 0`这两个条件有任一成立，这个数组就是一个特殊数组。

给定一个数组`nums`，求这个数组里特别排列（Permutation）的个数。


先尝试一下暴力解法。我们用常规的方式遍历每一种可能的排列并检查。但题目最多有`14!`种可能组合，显然暴力解法无效。

```python
class Solution:
    def specialPerm(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # Sort the array in ascending order.
        nums.sort()

        def is_special(nums):
            n = len(nums)
            for i in range(n - 1):
                if nums[i] % nums[i+1] != 0 and nums[i+1] % nums[i] != 0:
                    return False
            return True

        
        def permute(l, r):
            if l == r:
                return int(is_special(nums))
            result = 0
            for i in range(l, r):
                nums[l], nums[i] = nums[i], nums[l]
                result += permute(l+1, r)
                nums[l], nums[i] = nums[i], nums[l]  # backtrack
            return result
        
        return permute(0, len(nums))
```

在朴素解法中，我们每一次都需要递归到再回溯，因此耗时非常长。如果我们能够记忆化一些中间结果，就能减少我们的耗时。

我们考虑一种基于bitmask和dp的算法。首先bitmask的每一位对应`nums`数组中的元素。若第`i`位被设置为`1`，则表明第`i`个数被包含在当前排列中。我们用一个二维`dp`数组来表示一些中间的计算结果，其中第一个维度是`bitmask`，第二个维度是上一个添加进当前排列中的元素索引。

我们遍历所有的`bitmask`来考虑不同的元素组合。对于每一个`bitmask`，我们遍历所有的位置，尝试包含未被包含的元素`j`到当前的排列里面，藉此更新新包含进来的元素的dp值，即包含`bitmask`所表示的元素，且最后一个添加的是`j`位置的元素的特殊排列个数。

这个解法用Python会超时，所以改为用Go写。

```go
const MOD = int(1e9 + 7)

func specialPerm(nums []int) int {
	n := len(nums)

    div := make([][]int, n)
    for i := range nums {
        for j := 0; j < i; j++ {
            if nums[i] % nums[j] == 0 || nums[j] % nums[i] == 0 {
                div[i] = append(div[i], j)
                div[j] = append(div[j], i)
            }
        }
    }

	// initialize dp
	dp := make([][]int, 1<<n)
	for i := range dp {
		dp[i] = make([]int, n)
	}

	for i := 0; i < n; i++ {
		dp[1<<i][i] = 1
	}

	for mask := 0; mask < (1 << n); mask++ {
		for i := 0; i < n; i++ {
			if (mask & (1 << i)) == 0 {
				continue
			}
			for _, j := range div[i] {
				if (mask & (1 << j)) > 0 {
					continue
				}
                dp[mask|(1<<j)][j] += dp[mask][i]
                dp[mask|(1<<j)][j] %= MOD
			}
		}
	}

	res := 0
	for _, val := range dp[(1<<n)-1] {
		res += val
		res %= MOD
	}
	return res
}
```

## 2742. Painting the Walls 给墙壁刷油漆

给定粉刷每个墙壁的`cost`和`time`，你有两个工人：付费工人粉刷第`i`面墙壁时候会花费`cost[i]`和`time[i]`；免费工人可以在`1`个单位时间内粉刷任意墙壁，但是他只能够在付费工人工作的时候工作。你需要找到粉刷`n`个墙壁的最短花费。

这道题乍一看是个二维的`dp`，需要同时考虑花费和时间的维度。我们需要让付费工人尽可能的做花费少但是时间长的工作。与此同时让免费工人做花费多的工作。这压根就没法做啊！

不过仔细观察题目发现，利用免费工人的特性，我们实际上是可以把时间这个维度优化掉的。我们可以用一个`dp`数组来表示，`dp[i]`表示在第`i`个墙壁之前，最少需要花费多少钱。我们发现，我们只需要考虑第`i`个墙壁。我们有两种选择：1）不动这个墙壁，等免费工人后面粉刷；2）让付费工人粉刷当前墙壁，同时扣除`time[i] - 1`个没粉刷的墙壁让免费工人粉刷。

```python
class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:

        from functools import cache
        @cache
        def solve(i, wall):
            if wall <= 0:
                return 0
            
            if i >= len(cost):
                return inf

            notTake = solve(i + 1, wall)
            take = cost[i] + solve(i + 1, wall - time[i] - 1)
            return min(take, notTake)
        
        return solve(0, len(cost))
```
