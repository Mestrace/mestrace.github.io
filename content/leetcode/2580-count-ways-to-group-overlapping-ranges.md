Title: 【Leetcode题解】2580. Count Ways to Group Overlapping Ranges
Slug: 2580-count-ways-to-group-overlapping-ranges
Date: 2023-03-14
Category: Leetcode
Tags: Contest, Math
Summary: 2023-03 - Biweekly Contest 99 - Leetcode 2580 Count Ways to Group Overlapping Ranges - 计算重叠范围的分组方式 - 我的解法，思路和方法

## 题目

给定一个列表的`ranges`，其中`range[i] = [start, end]`包含了一个区间的开始和结束。我们想要把这个区间分为两个部分，且两个部分里面的每一对`range[i]`和`range[j]`没有相交的部分。

题目要求我们找到有多少种分为两个部分的方法，且因为数量非常大，需要模`1e9 + 7`。

## 分析

这道题是2023.03.04的[双周赛 Biweekly Contest 99](https://leetcode.com/contest/biweekly-contest-99/)第三题（[原题链接](https://leetcode.com/contest/biweekly-contest-99/problems/count-ways-to-group-overlapping-ranges/)）。这一题的大致思路是这样：找到并合并相交的区间，最终知道不相交的区间后，计算有多少种分组方式。

找到相交区间的题目已经很多了，包括这种经典的区间相交，还有经典的会议室系列。这类型题目的一个共性就是需要先对入参的时间进行排序。原理也比较好理解，如果你想要知道某个区间是否相交，最好的方式就是查看他临近的事件，而较远的事件就无需关注。对于这道题来说，我们只是要尽可能的合并相交的区间，没有什么太复杂的性质。所以我们先根据开始时间升序排序即可。排序之后，我们就可以遍历整个区间一个一个看是否相交并进行合并。

假设我们已经有了一个列表的不相交的区间，我们怎么算有多少种分组方式呢。在这个时候我选择的是画一些例子来找规律。
```text
Input: [1,2]
Output: 2
Explanation:
[1,2] & empty
empty & [1,2]
```
```text
Input: [[1,2], [3,4]]
Outpu: 4
Explanation:
[1,2] [3,4] & empty
[1,2] & [3,4]
[3,4] & [1,2]
empty & [1,2] [3,4]
```

```text
Input: [[1,2],[3,4],[5,6]]
Output: 8
```

在这里的时候似乎我们看到了这么一个规律，我们知道有`n`组的数量之后，结果永远都是`2^n`。此外，我们还可以确定的事，我们只需要知道不相交区间的个数就可以知道，而不需要具体的知道怎么相交。我们用数学方式去验证一下。首先我们只需要管左边有什么元素，因为右边有什么元素可根据左边来确定。
```text
Left elements
0: empty set = 1
1: n choose 1 = n
2: n choose 2
3: n choose 3
until
n : n choose n = 1
```
而我们可以观察到，这个正好和数学上的二项式展开的形式非常相似。我们再来看看杨辉三角（或者帕斯卡三角，Pascal's Triangle）。我们会发现其实这个问题的解就是每一横行求和！

```python
0:									1								
1:								1		1							
2:							1		2		1						
3:						1		3		3		1					
4:					1		4		6		4		1				
5:				1		5		10		10		5		1			
6:			1		6		15		20		15		6		1		
7:		1 		7 		21		35		35		21		7 		1 	
8:	1 		8 		28		56		70		56		28		8 		1
```

总而言之，非常巧妙的我们可以通过观察的方式得出二次幂就是这个题目的答案的这个结论。具体的证明和推倒就留给读者了。


## 解法

不多废话，直接上解法。这道题基本上就跟我们讲的一样，先进行排序，求出相交个数`groups`之后，直接用二次幂公式进行计算。

这里用二次幂公式的一个小机器。之前的周赛中是二次幂取模之后减去一个数求结果[ref][2550. Count Collisions of Monkeys on a Polygon](https://leetcode.com/problems/count-collisions-of-monkeys-on-a-polygon/description/)[/ref]，但是直接`pow`取模会直接导致算出负数的结果，因此这样算可以避免`((2^(n-1) % MOD) * 2 - m) % MOD` 。

```python3
MOD = int(1e9 + 7)

class Solution:
    def countWays(self, ranges: List[List[int]]) -> int:
        def isOverlap(a, b):
            return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]
        
        def overlap(a, b):
            return [min(a[0], b[0]), max(a[1], b[1])]
        
        ranges = sorted(ranges)
        
        # print(ranges)
        
        curr = ranges[0]
        groups = 0
        for i in range(1, len(ranges)):
            if isOverlap(curr, ranges[i]):
                curr = overlap(curr, ranges[i])
                continue
            groups += 1
            curr = ranges[i]
        
        # last group
        groups += 1
        
        # print("groups", groups)
        
        
        return (pow(2, groups - 1) % MOD) * 2 % MOD
```

而对于是用别的语言的同学来说，则需要自己手动实现带取模的二次幂方法，简单来说就是递归求`2^(n - 1)`，在半途中就需要取模。这里简单贴一个我写的版本。
```python3
MOD = int(1e9 + 7)

def power(n):
    if n == 1:
        return 2
    t = power(n / 2)
    t = (t * t) % MOD
    if n % 2 == 1:
        return (t * 2) % MOD
    return t
```

## 总结

这道题思路比较简单，但是难点在于把二项式分解和取模的部分跟这道题结合起来。大家一起努力吧。

如果你想变得更强的话，可以做做

1. [Easy - 252. Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)
1. [Medium - 435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
1. [Medium - 1621. Number of Sets of K Non-Overlapping Line Segments](https://leetcode.com/problems/number-of-sets-of-k-non-overlapping-line-segments/)
1. [Medium - 1229. Meeting Scheduler](https://leetcode.com/problems/meeting-scheduler/)
1. [Hard - 2402. Meeting Rooms III](https://leetcode.com/problems/meeting-rooms-iii/)

还可以延伸看看

1. [Proof By Induction of the Summation of n choose k](https://math.stackexchange.com/questions/519832/proving-by-induction-that-sum-k-0nn-choose-k-2n) 这个summation的数学证明。
1. [Wikipedia - Binomial Coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient)

-----