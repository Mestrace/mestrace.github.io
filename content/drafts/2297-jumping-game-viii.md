Title: 2297. Jump Game VIII 跳跃游戏 VIII
Slug: 2297-jumping-game-viii
Date: 2023-05-24
Status: draft
Category: Leetcode
Summary: Leetcode Medium 2297. Jump Game VIII 跳跃游戏 VIII | Monotonic Stack 单调栈

[2297. Jump Game VIII](https://leetcode.com/problems/jump-game-viii/description/)

这道题是经典的跳跃游戏系列。给定一个列表的数组`nums`，需要从初始位置`0`移动到最后一个元素。可以从`i`跳跃到之后的元素`j`，当且仅当满足下列任一条件：

- `nums[i] <= nums[j]`且对于`(i, j)`之间的每一个`k`，`nums[k] < nums[i]`
- `nums[i] > nums[j]`且对于`(i, j)`之间的每一个`k`，`nums[k] >= nums[i]`

此外，还会给定一个`cost`数组，其中每个`cost[i]`为移动到第`i`个元素的成本。要求找到到达最后一个元素的最小成本。

幸好，这道题只考察向前的情况，不会有倒着走的情况。那么，我们可以简单列出状态转移方程为`f(i) = min(cost(i) + f(j))`，其中`i > j`且`i`和`j`中间的每一个元素都满足上面的条件。最朴素的方法就是，当我们在`i`的时候，顺序往回看以确定哪条规则满足我们的需求，并尝试每一个更大 / 更小的元素以更新我们的结果。由这个最大/最小的性质，我们可以联想到用单调栈去快速这个大小关系，并减少我们的搜索空间。

在维护单调栈的过程中，我们知道，我们要维护栈中的元素的顺序，使得其保持单调递增或递减。