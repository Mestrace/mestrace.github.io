Title: 【Leetcode题解】2551. Put Marbles in Bags
Slug: 2551-put-marbles-in-bags
Date: 2025-03-31
Category: Leetcode
Summary: Leetcode Hard 2551. Put Marbles in Bags 将珠子放入背包中 | Greedy

[2551. Put Marbles in Bags](https://leetcode.com/problems/put-marbles-in-bags/description/?envType=daily-question&envId=2025-03-31)

[2551. 将珠子放入背包中](https://leetcode.cn/problems/put-marbles-in-bags/description/)

首先我们来看看这个问题，这道题目 首先提供给我们一个弹珠列表`weights`，`weights[i]`代表了弹珠`i`的重量。要求我们将每个弹珠分配到`k`个袋子中，并满足如下条件：

1. 每个袋子必须有一粒弹珠。
2. 每个袋子中包含的弹珠是弹珠列表中的一个连续子数组。即

满足这个条件的袋子的得分为此袋子代表的连续子数组的第一个和最后一个弹珠的 怎么理解呢？如果当前袋子包含`weights[i:j+1]`，那么当前袋子的得分为`weights[i] + weights[j]`。求**最大化**和**最小化**得分之差。

按照题目的意思，若我们将弹珠分配到`k`个袋子中，那么实际上我们是在这个数组中放下`k-1`分割点，才能将这个数组分为`k`个子数组。

考虑一个例子：若`weights = [a, b, c, d, e, f, g], k = 3`，考虑两种分法：
```
P = [a, b], [c, d], [e, f, g]
Q = [a, b, c], [d, e], [f, g]
```
那么这两种方法各自的得分为`score(P) = (a + b) + (c + d) + (e + g)`，`score(Q) = (a + c) + (d + e) + (f + g)`。 在以上的式子中，我们使用的方式是按照题目的定义，将每个子数组的头和尾两个数字加起来用括号进行划分。 我们可以观察到在任何一种分法里面，数组的头元素和尾元素永远存在。 那么当我们实际在求结果要求的两种分法的差的时候，数组的头元素和尾元素都是消掉的，对最终的数字影响不计。令`score'(P) = score(P) - a - g`和`score'(Q) = score(Q) - a - g`，我们可以得到`score'(P) = b + c + d + e`以及`score'(Q) = c + d + e + f`。 那么，可知`score'`的定义为最终得分为每个分割点左右两边的元素之和，且两种分法之差为`score'(P) - score'(Q)`。

若`weights`有`w`个元素，我们有`w - 1`个可选的分割点。 我们将这些分割点都求出来并进行排序，就可以拿到令得分最大和最小的分割点了。

```python
class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        w = [weights[i] + weights[i + 1] for i in range(len(weights) - 1)]

        w.sort()

        return sum(w[len(w) - k + 1:]) - sum(w[0:k-1])
```
