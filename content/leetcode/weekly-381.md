Title: Weekly Contest 381 周赛题目解析
Slug: weekly-381
Date: 2024-01-31 23:30
Category: Leetcode
Tags: Contest
Summary: 2024-01 Leetcode Weekly Contest 381 第 381 场力扣周赛 | 3014. Minimum Number of Pushes to Type Word I 输入单词需要的最少按键次数 I | 3015. Count the Number of Houses at a Certain Distance I 按距离统计房屋对数目 I | 3016. Minimum Number of Pushes to Type Word II 输入单词需要的最少按键次数 II | 3017. Count the Number of Houses at a Certain Distance II 按距离统计房屋对数目 II | Solution to contest problems 赛题讲解

[Weekly Contest 381](https://leetcode.com/contest/weekly-contest-381/)

[第 381 场周赛](https://leetcode.cn/contest/weekly-contest-381/)

拷贝忍者再次出现，他使用了两次拷贝，将4题的周赛变成了两题！

这篇文章拖更了两周，倒不是因为我懒，而是第四题想要解释清楚其实是有一些困难的。

## 题目列表

- [3014. Minimum Number of Pushes to Type Word I 输入单词需要的最少按键次数 I](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-i/description/)
- [3015. Count the Number of Houses at a Certain Distance I 按距离统计房屋对数目 I](https://leetcode.com/problems/count-the-number-of-houses-at-a-certain-distance-i/description/)
- [3016. Minimum Number of Pushes to Type Word II 输入单词需要的最少按键次数 II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/)
- [3017. Count the Number of Houses at a Certain Distance II 按距离统计房屋对数目 II](https://leetcode.com/problems/count-the-number-of-houses-at-a-certain-distance-ii/description/)

## 3014. Minimum Number of Pushes to Type Word I 输入单词需要的最少按键次数 I

给定九宫格数字键盘，要求重组每个数字对应的字母，使得新组成的键盘能以最短的按键次数打出给丁的词`word`，并返回这个次数。

首先我们知道，九宫格键盘是`2-9`的键位，除`7`和`9`对应4个字母之外，其他键都只对应三个字母。因为要求以最少的按键次数打出`word`，我们可以以贪心的方式，让出现频率最高的字母占据每个键的最外面的字母。这时候就是`heap`出场的时刻了。

```python
def key_count(a):
    if a == 7 or a == 9:
        return 4
    return 3

class Solution:
    def minimumPushes(self, word: str) -> int:
        word_cnt = [(k, v) for k, v in Counter(word).items()]
        
        word_cnt.sort(reverse=True, key = lambda x: x[1])
        
        from heapq import heapify, heappush, heappop
        
        key_cnt = [(1, i) for i in range(2, 10)]
        
        heapify(key_cnt)
        
        result = 0
        
        for w, wc in word_cnt:
            kc, k = heappop(key_cnt)
            
            # print(f"{w} mapped to {k} with press {kc}, total cost: {wc * kc}")
            
            result += wc * kc
            
            if kc + 1 > key_count(k):
                continue
            heappush(key_cnt, (kc + 1, k))
        
        return result
```

## 3015. Count the Number of Houses at a Certain Distance I 按距离统计房屋对数目 I

给定`n`栋房子，每栋房子都与左右两边的房子直接相连。此外，还有两栋房子`(x, y)`有直接相邻的捷径。对于每两栋房子，计算出他们最短距离之后，要求每个距离下有多少对房子直接相连。这里有两个要点：

1. `x`可能等于`y`
2. `(a, b)`和`(b, a)`被视作不同的房子对。即每对房子应该被计算两次。

这里我们来看一个例子
```
Example:
Input: n = 5, x = 2, y = 4
Output: [10,8,2,0,0]
```

* 当距离`k = 1`，除了相邻的房子之外，还有一对`(2, 4)`直接相连，因此返回`(4 + 1) * 2 = 10`
* 当距离`k = 2`，隔一个的房子总共有3组，但是有一组`(2, 4)`直接相连需要排除；此外，通过捷径，我们还可以走`1 -> 2 -> 4`和`2 -> 4 -> 5`。因此总共是`4`组，返回`8`。
* 当距离`k = 3`，隔两个的房子总共有2组，但是他们实际上都可以通过捷径，因此无法参与计算；只通过捷径计算的话，剩余最后一组`1 -> 2 -> 4 -> 5`。因此返回`2`。
* 当距离`k = 4`和`k = 5`时，没有两组房子的最短距离刚好为`k`，因此都返回`0`。

我们知道，对于`n`个顶点，两两相连总共有`(n - 1) * n / 2`种组合（不算正反向）。这里我们可以看到，返回结果的数组刚好是`10`组乘以`2`的正反向。

看到数值范围为`100`，我们可以直接暴力计算。

```python
class Solution:
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        result = [0] * n
        
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i == j:
                    continue
                
                
                dist = min(abs(i - j), abs(i - x) + 1 + abs(j - y), abs(i - y) + 1 + abs(j - x))
                
                # print(f"dist {i}, {j}: {dist}")
                
                result[dist - 1] += 1
        
        return result
```

## 3016. Minimum Number of Pushes to Type Word II 输入单词需要的最少按键次数 II

与第一题[3014. Minimum Number of Pushes to Type Word I 输入单词需要的最少按键次数 I](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-i/description/)的解法一样，此处略。

## 3017. Count the Number of Houses at a Certain Distance II 按距离统计房屋对数目 II

与第二题[3015. Count the Number of Houses at a Certain Distance I 按距离统计房屋对数目 I](https://leetcode.com/problems/count-the-number-of-houses-at-a-certain-distance-i/description/)的题目是一样的，但是数据范围有变化，我们无法直接暴力求解。

首先，我们尝试简化一下问题。我们首先可以把所有的房子分成左，中，右三组。中间组代表在`[x, y]`之间的所有房子，而左和右就很好理解了，分别为`[1, x)`和`(y, n]`。那么，我们就可以对这个问题进行分组讨论了。

首先我们考虑在中间形成的环上的房子。在任意距离`k`下，每栋房子都可以镜像对应到另一栋房子。一个极端情况是当房子个数为偶数个时且距离`k = l / 2`时，房子只能被分为一半的组数。

其次我们考虑在两边形成的线段上的房子。在考虑到`x <-> y`形成的捷径之后，实际上我们有一条更短的直线。不过要注意的是，我们应该排除刚好在环上的房子所形成的对。


讨论线段到环上的结构配对的这个情况较为复杂。因此我们在代码部分之后再予以讨论。


```python
class Solution:
    
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        def pairwise_add(l1, l2):
            return [v1 + v2 for v1, v2 in zip(l1, l2)]
        
        result = [0] * n
        if x > y:
            x, y = y, x
        

        result = pairwise_add(result, _cycle(n, x, y))
        result = pairwise_add(result, _line(n, x, y))
        result = pairwise_add(result, _line_cycle(n, x, y))
        
        return result
    
def _cycle(n, x, y):
    result = [0] * n
    cycle = y - x + 1
    halfCycle = (cycle - 1) // 2
    # cycle
    for i in range(0, halfCycle):
        result[i] = cycle * 2
    if cycle % 2 == 0:
        result[halfCycle] = cycle
    return result

def _line(n, x, y):
    result = [0] * n
    left = x - 1
    right = n - y

    line = left + right + 1 + (x != y)
    for i in range(1, line):
        result[i - 1] += (line - i) * 2
    # print(result)
    if x != y:
        # exclude the shortcut itself
        result[0] -= 2
        # for every other pair, exclude the pair with cycle
        for l in (left, right):
            for i in range(1, l + 1):
                result[i] -= 2
    return result

def _line_cycle(n, x, y):
    result = [0] * n
    cycle = y - x + 1
    halfCycle = (cycle - 1) // 2

    left = x - 1
    right = n - y

    for l in (left, right):
        for i in range(1, l + halfCycle):
            # print(l, halfCycle, i, l + halfCycle - i)
            result[i] += 4 * min(l, halfCycle, i, l + halfCycle - i)
        # if the cycle is even, every node in the 
        if cycle % 2 == 0:
            for i in range(1, l + 1):
                result[i + halfCycle] += 2
    return result
```

接下来我们讨论线段到环上的结构配对，即`_line_cycle`方法中的`4 * min(l, halfCycle, i, l + halfCycle - i)`的含义。

首先，对于线段上的每一个房子，在同一个长度`k`下，总有两个环上的房子能以`k`的最短距离连接。因此，每存在这样的情形，我们会增加4个房子对。


接着，让我们探讨`min`函数中的各个参数的含义。实际上，在每个距离`k`中，线段到环上的房子对数都有以下条件限制。

* 线段长度(`l`)：它代表了在不同距离k上可能的最大房子对数量。当我们从线段上的一个房子出发，向环上的房子寻找配对时，线段长度限制了我们能够选择的最大距离。
* 半环长度(`halfCycle`)：这个值决定了在环上可能形成配对的最大数量。想象一下，当我们从线段的一个端点出发，沿着环行进时，我们最远只能到达环的对面中点，这就是半环长度限制了我们在不超过整个环长度的情况下，能够形成的配对数量。
* 起始长度(`i`)：它限制了在较短距离时可能的房子对数量。在距离k小于线段上房子的位置i时，我们最多只能形成i对房子。
* 末尾长度(`l + halfCycle - i`)：这个值限制了在较长距离时可能的房子对数量。当距离k大于线段上房子的位置i时，我们需要考虑从线段另一端出发，沿着环行进到达该房子的可能性。这个长度考虑了从线段的一端到另一端，再加上半环长度的总距离。

此外，当环长度为偶数时，两两配对时会多出来一组，因此我们需要加上这一组。

针对这一题，我还写了一些测试，代码放出来供大家参考。

```python
from typing import List, Callable
import unittest
from dataclasses import dataclass

# 暴力解法
def countOfPairs(n: int, x: int, y: int) -> List[int]:
    assert 1 <= x
    assert y <= n
    
    result = [0] * n

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                continue


            dist = min(abs(i - j), abs(i - x) + 1 + abs(j - y), abs(i - y) + 1 + abs(j - x))

            # print(f"dist {i}, {j}: {dist}")

            result[dist - 1] += 1

    return result


@dataclass
class Data:
    n: int
    x: int
    y: int
    func: Callable[[int, int, int], List]
    expected: List

line_data = []
line_data.append(
    Data(
        6, 1, 1, _line, countOfPairs(6, 1, 1)
    )
)

cycle_data = []
cycle_data.append(
    Data(7, 1, 7, _cycle, countOfPairs(7, 1, 7))
)

line_cycle_data = []

countOfPairs2 = Solution().countOfPairs
count_of_pair_data = []
count_of_pair_data.append(
    Data(7, 2, 5, countOfPairs2, countOfPairs(7, 2, 5))
)
count_of_pair_data.append(
    Data(13, 6, 8, countOfPairs2, countOfPairs(13, 6, 8))
)

class TestCases(unittest.TestCase):
    def test_line(self):
        for d in line_data:
            self.assertListEqual(d.func(d.n, d.x, d.y), d.expected, f"Testcase: {d}")
    
    def test_cycle(self):
        for d in cycle_data:
            self.assertListEqual(d.func(d.n, d.x, d.y), d.expected, f"Testcase: {d}")
    
    def test_line_cycle(self):
        for d in line_cycle_data:
            self.assertListEqual(d.func(d.n, d.x, d.y), d.expected, f"Testcase: {d}")

    def test_count_of_pairs(self):
        for d in count_of_pair_data:
            self.assertListEqual(d.func(d.n, d.x, d.y), d.expected, f"Testcase: {d}")

        
        
unittest.main(argv=[''], verbosity=2, exit=False)
```


