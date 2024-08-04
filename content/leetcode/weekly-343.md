Title: 【Leetcode题解】Weekly Contest 343 周赛题目解析
Slug: weekly-343
Date: 2023-05-04 22:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Weekly Contest 343 第 343 场力扣周赛 | 2660. Determine the Winner of a Bowling Game 保龄球游戏的获胜者 | 2661. First Completely Painted Row or Column 找出叠涂元素 | 2663. Lexicographically Smallest Beautiful String 字典序最小的美丽字符串 | 2663. Lexicographically Smallest Beautiful String 字典序最小的美丽字符串 | Solution to contest problems 赛题讲解 | Dijkstra's Algorithm 狄克斯特拉算法 | Lexicographic order 字典序


[Weekly Contest 343](https://leetcode.com/contest/weekly-contest-343/)

[第 343 场周赛](https://leetcode.cn/contest/weekly-contest-343/)

这场比赛的题目都是阅读理解型的，一不小心漏掉条件就小甲虫了。就像是本来是防止机器人的验证码把人给梗住了的感觉，很难形容。不吐槽了，接着来看看题目吧。

## 题目列表

- [Easy - 2660. Determine the Winner of a Bowling Game](https://leetcode.com/problems/determine-the-winner-of-a-bowling-game/)
- [Medium - 2661. First Completely Painted Row or Column](https://leetcode.com/problems/first-completely-painted-row-or-column/)
- [Medium - 2662. Minimum Cost of a Path With Special Roads](https://leetcode.com/problems/minimum-cost-of-a-path-with-special-roads/)
- [Hard - 2663. Lexicographically Smallest Beautiful String](https://leetcode.com/problems/lexicographically-smallest-beautiful-string/)

## 2660. Determine the Winner of a Bowling Game 保龄球游戏的获胜者

按照题意模拟即可。隐藏条件有点多，不认真读题的话容易出小甲虫。

```python3
class Solution:
    def isWinner(self, player1: List[int], player2: List[int]) -> int:
        def score(pl):
            s = sum(pl)
            add = 0
            for v in pl:
                if add > 0:
                    s += v
                    add -= 1
                if v == 10:
                    add = 2 
            return s
        s1 = score(player1)
        s2 = score(player2)
        print(s1, s2)
        if s1 == s2:
            return 0
        elif s1 > s2:
            return 1
        return 2
```

## 2661. First Completely Painted Row or Column 找出叠涂元素

先考虑朴素的方法，即每涂一个格子检查一下行和列是否完整了。考虑到`10^5`的约束条件，这样会超时。但我们还是可以联想到通过计数的方法来判断。试想一个`m x n`的矩阵，第`i`行总共有`n`个元素，第`j`列总共有`m`个元素。这里我们直接分别用长度为`m`和`n`的列表来储存是否被涂满了。

```python3
class Solution:
    def firstCompleteIndex(self, arr: List[int], mat: List[List[int]]) -> int:
        ridx = dict()
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                ridx[mat[i][j]] = (i, j)
        
        row_painted = [0] * len(mat)
        col_painted = [0] * len(mat[0])
        
        for idx, v in enumerate(arr):
            i, j = ridx[v]
            row_painted[i] += 1
            col_painted[j] += 1
            if row_painted[i] == len(mat[0]) or col_painted[j] == len(mat):
                return idx
        
        return len(arr)
```

## 2662. Minimum Cost of a Path With Special Roads 前往目标的最小代价

在一个二维空间内，给定开始点`start`，和结束点`target`，和一系列单向的特殊道路`specialRoads`，要求求出开始点到结束点的最小代价。在这个空间内，任意路径的代价为曼哈顿距离`|y2 - y1| + |x2 - x2|`，也可以经由特殊路径`(x1, y1) -> (x2, y2)`，则代价是`d`。

这道题题目描述的不太清晰，导致好多人都以为特殊道路是双向的。空间大小也没有限定，但是我们也可以推出，要么直接是开始点到结束点的曼哈顿距离，或者是经由任意条特殊道路到达的。因此我们考虑Dijkstra算法。给定当前点`p`和`start -> p`的距离，若我们可以路过特殊道路`s1 -> s2`到达`s2`，且总距离小于当前记录的小于`start -> s2`的距离，那么就可以更新`start -> s2`的距离了。最后把所有的点进行比对求得最短距离。


```python
class Solution:
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        from heapq import heappush, heappop
        def euclid(p1, p2):
            return abs(p2[1] - p1[1]) + abs(p2[0] - p1[0])
        
        # filter roads that are not useful
        specialRoads = [v for v in specialRoads if euclid((v[0], v[1]), (v[2], v[3])) > v[4]]

        start = tuple(start)
        target = tuple(target)

        dist = {start: 0}

        heap = [(0, start)]

        while len(heap) > 0:
            d, p = heappop(heap)
            for x1, y1, x2, y2, cost in specialRoads:
                n1, n2 = (x1, y1), (x2, y2)
                if dist.get(n2, inf) > d + euclid(p, n1) + cost:
                    dist[n2] = d + euclid(p, n1) + cost
                    heappush(heap, (dist[n2], n2))
            # print(heap)
        
        result = euclid(start, target)
        for x1, y1, x2, y2, cost in specialRoads:
            n2 = (x2, y2)
            result = min(result, dist.get(n2, inf) + euclid(n2, target))
        return result
```

## 2663. Lexicographically Smallest Beautiful String 字典序最小的美丽字符串

如果一个字符串只包含了小写字母中的前`k`个字母，且其中任意大于2的子字符串不是回文，那么我们说这是一个美丽字符串。给定一个美丽字符串`s`和参数`k`，找到以字典序刚好比`s`大的下一个美丽字符串。若这样的字符串不存在的话，返回空。

看到题目的时候我的内心是懵逼的。但是其实仔细思考下来其实比较简单的。这里参考了李哥的做法给大家做一个解释。首先，由题目可以推出简化的条件。美丽字符串里面不能有回文，即连续的三个字母里面不能有重复，否则的话一定形成回文。此外要求字典序尽量小，实际上就是`a,b,c`三个字母循环一定可以拿到最小的。这样的话，我们就可以通过贪心的方式，从末尾往前看，若我们能刚好把一个位置上的字母加一且这个字母与前两个位置的字母不重复的话，我们在用`a,b,c`填充这个索引后面的所有字符。


```python3
class Solution:
    def smallestBeautifulString(self, s: str, k: int) -> str:
        a = [ord(c) - ord('a') for c in s]

        i = len(a) - 1

        while i >= 0:
            a[i] += 1
            if a[i] == k:
                i -= 1
                continue
            if a[i] not in a[max(i - 2, 0):i]:
                for j in range(i + 1, len(a)):
                    a[j] = min({0, 1, 2} - set(a[max(0, j - 2):j]))
                return ''.join(chr(ord('a') + c) for c in a)
        
        return ''
```