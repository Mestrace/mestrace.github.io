Title: 【Leetcode题解】2604. Minimum Time to Eat All Grains
Slug: 2604-minimum-time-to-eat-all-grains
Date: 2023-04-07
Category: Leetcode
Summary: Leetcode Hard 2604 Minimum Time to Eat All Grains My Solution 我的解题思路。


今日闲来无事，简单做一下[2604. Minimum Time to Eat All Grains](https://leetcode.com/problems/minimum-time-to-eat-all-grains/)

题目首先给定两个数字列表`hens`和`grains`。`hens`代表鸡的位置，`grains`代表饲料的位置。每只鸡可以吃掉无限的饲料；在位置`i`的鸡可以立即吃掉当前位置的饲料。但如果鸡的位置不等于饲料的位置的话，鸡可以移动过去吃饲料，且每秒移动速度是`1`。所有的鸡可以同时移动且互相独立。假定所有鸡都按照最优方法移动的话，我们需要找到最短时间使得所有饲料都可以被吃掉。

这道题我第一个思路是先找到一些比较小的子问题，来进行求解。显然，这道题有两个最小的子问题，即有`1`只鸡和多个饲料，或者多只鸡和`1`个饲料的例子。

```
Example 1
Input: hens = [6], grains = [2, 8]
Output: 8
Explanation:
One way to move
hens 0 move 6 -> 8 => 2s
hens 0 move 8 -> 2 => 6s
Another way to move
hens 0 move 6 -> 2 => 4s
hens 0 move 2 -> 8 => 6s
```

上面我们可以看到，如果一只鸡旁边有两个饲料的话，需要优先吃距离最短的，这样才能使得整体距离最小。

```
Example 2
Input: hens = [1, 10], grains = [7]
Output: 3
Explanation:
One way to move
hens 0 move 1 -> 7 => 6s
Another way to move
hens 1 move 10 -> 7 => 3s
```

第二个例子也是要用相同的方法，即我们试着让离饲料最近的鸡去吃就能拿到最优解。

这里我们只讨论了限制最大的两种情况。当我们有多只鸡和多个grain的情况的时候就不太好办了。思路到这里就断了。那么，我们能不能把时间这个变量固定住，再检查是否能在固定时间内完成我们的条件呢？我们要求的是最短的时间`T = t`。简单推理下可知，且当`T < t`的时候都无法完成，`T > t`的时候都可以完成。当然一个一个时间点查看肯定会超时，这里我们采用二分来找。

那么剩下的问题就是怎么判断在给定时间`T`里面判断是否可以吃到全部的饲料了。这里优先考虑对`hens`和`grains`进行排序，我们再一个个进行匹配。给定一只鸡的位置`h`和时间`t`，我们想要找到离他最近的饲料并标记这些饲料被他吃掉了。我们从小到大开始循环，我们有这么两条条规则

1. 如果有饲料`g`在`h`左边的话，必须要吃掉。
2. 剩余时间需要尽量向右移动吃右边的饲料。

但是我们发现，在规则1中，如果右边的饲料比左边更近的话，先移动到左边不一定最优，就如同上面的例子1中，我们先吃左边的比先吃右边的耗时更久。因此，我们进一步展开规则为

1. 左边有饲料`g`的情况下，我们先移动`h`到左边，然后回到`g`，可以移动到最右边的距离为`t - 2 * (h - g)`
1. 左边有饲料`g`的情况下，我们先移动`h`到右边，最后回到`g`，可以移动到最右边的距离为`(t - (h - g)) / 2`。
1. 左边没有饲料的情况下，可以移动到最右边的距离为`t`。

<p align="center">
  <img src="{static}/images/leetcode-2604/fig-1.png" />
  <img src="{static}/images/leetcode-2604/fig-2.png" />
  <img src="{static}/images/leetcode-2604/fig-3.png" />
</p>


## 代码

```python
{!content/leetcode/code/2064-minimum-time-to-eat-all-grains.py!}
```