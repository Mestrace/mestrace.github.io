Title: 【Leetcode题解】2589. Minimum Time to Complete All Tasks
Slug: 2589-minimum-time-to-complete-all-tasks
Date: 2023-03-12
Category: Leetcode
Tags: Contest, Scheduling
Summary: 2023-03 Weekly Contest 336 Leetcode 2589 Minimum Time to Complete All Tasks My Solution 我的解题思路


## 题目

给定一个列表的`tasks`，其中每个`task[i] = [start, end, duration]`需要在`[start, end]`中任意时间运行完成，并且最终需要运行`duration`秒。

此外，我们的机器可以并行运行任意数量的`task[i]`，可以随时开始或者停止，不运行的时候就需要关闭。我们需要找到这台机器能并行完成这些任务的最短时间。

## 分析

这道题是2023.03.12的[周赛Weekly Contest 336](https://leetcode.com/contest/weekly-contest-336/)第四题（[原题链接](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/description/)）。挺可惜的，我因为看错题目了，没做出来。我一开始以为是需要在连续区间运行的，直接开了个2000个元素的开始梭backtracking with memorization。各位看题一定要仔细看……

不扯犊子了，直接进入主题。对于这种涉及到调度的问题，一个经验法则就是先看看能不能用排序和贪心做。对于这种类型的题目，搜索空间通常非常的大。比如给定一个任务`task[i] = [1,2000,1]`直接干到`O(n^2)`，所以不是非常可取。那么既然决定了用贪心，我们就要考虑怎么贪才能满足我们的最小条件。对于这道题，我们期望是在区间内，任务能够尽可能的跟其他任务并行，因为题目并没有限制机器并行的任务个数。此外，假如我们拿到了一个任务，但是他前面没有其他任务可以并行，我们需要尽可能晚地运行这个任务，才能让后面的任务跟他一起并行。此外，排序怎么拍也决定了我们执行贪心的顺序，也正是这道题目的难点。我先放在前面，这道题我们应该根据结束时间升序。一个比较直白的解释是，结束时间较早的任务需要先运行才可以确定后面的任务要怎么并行。我们来看一个例子，

```
Input: [[8,19,1],[3,20,1],[1,20,2],[6,13,3]]
Sort based on end: [[6, 13, 3], [8, 19, 1], [3, 20, 1], [1, 20, 2]]
Sort based on start: [[1, 20, 2], [3, 20, 1], [6, 13, 3], [8, 19, 1]]
```

我们以任务 [1,20,2] 和 [6,13,3] 为例，当我们执行一个任务时，我们并不知道后续任务的处理方式，因此可能得到非最优解。但是，如果我们按照结束时间的先后顺序来执行任务，那么当我们处理一个任务时，我们已经知道在它之后不会再有比它更早结束的任务，因此我们可以放心地使用贪心算法进行处理。

## 题解


```python
class Solution:
    def findMinimumTime(self, tasks: List[List[int]]) -> int:
        line = [False] * 2001

        tasks = sorted(tasks, key=lambda t: t[1])

        for start, end, duration in tasks:
            duration -= sum(line[start:end + 1])
            if duration <= 0:
                continue
            for i in range(end, -1, -1):
                # print(i, duration, line[i])
                if duration == 0:
                    break
                if line[i]:
                    continue
                duration -= 1
                line[i] = True

        
        return sum(line)
```

## 总结

这道题个人感觉并不是特别难，但最重要的应该是在周赛的那种压力下能不能想到这个思路。各位继续加油吧。

这次周赛的其他题目

1. [Easy - 2586. Count the Number of Vowel Strings in Range](https://leetcode.com/problems/count-the-number-of-vowel-strings-in-range/) （手速题）
1. [Medium - 2587. Rearrange Array to Maximize Prefix Score](https://leetcode.com/problems/rearrange-array-to-maximize-prefix-score/) （手速题）
1. [Medium - 2588. Count the Number of Beautiful Subarrays](https://leetcode.com/problems/count-the-number-of-beautiful-subarrays/) （[我的题解]({filename}/leetcode/2588-count-the-number-of-beautiful-subarrays.md)）

如果你想变得更强的话，可以做做

1. [1834. Single-Threaded CPU](https://leetcode.com/problems/single-threaded-cpu/)
1. [2365. Task Scheduler II](https://leetcode.com/problems/task-scheduler-ii)
1. [1462. Course Schedule IV](https://leetcode.com/problems/course-schedule-iv/)
1. [1229. Meeting Scheduler](https://leetcode.com/problems/meeting-scheduler/)
