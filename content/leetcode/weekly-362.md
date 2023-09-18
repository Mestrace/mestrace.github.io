Title: Weekly Contest 362 周赛题目解析
Slug: weekly-362
Date: 2023-09-17
Category: Leetcode
Tags: Contest
Summary: 2023-09 Leetcode Weekly Contest 362 第 362 场力扣周赛 | 2848. Points That Intersect With Cars 与车相交的点 | 2849. Determine if a Cell Is Reachable at a Given Time 判断能否在给定时间到达单元格 | 2850. Minimum Moves to Spread Stones Over Grid 将石头分散到网格图的最少移动次数 | 2851. String Transformation 字符串转换 | Solution to contest problems 赛题讲解

[Weekly Contest 362](https://leetcode.com/contest/weekly-contest-362/)

[第 362 场周赛](https://leetcode.cn/contest/weekly-contest-362/)

求锤得锤，终于得到了一个超级无敌Hard的第四题。此外，这次周赛其他题目的出题水准也相当高。<span title="你知道的太多了" class="heimu">第一题终于不是“按照题意模拟即可”就结束了。</span>

## 题目列表

- [2848. Points That Intersect With Cars 与车相交的点](https://leetcode.com/problems/points-that-intersect-with-cars/)
- [2849. Determine if a Cell Is Reachable at a Given Time 判断能否在给定时间到达单元格](https://leetcode.com/problems/determine-if-a-cell-is-reachable-at-a-given-time/)
- [2850. Minimum Moves to Spread Stones Over Grid 将石头分散到网格图的最少移动次数](https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/description/)
- [2851. String Transformation 字符串转换](https://leetcode.com/problems/string-transformation/)

## 2848. Points That Intersect With Cars 与车相交的点

合并相交的区间直到不能合并为止，则点的数量为`end - start + 1`。排序后遍历以进行合并。

```python
class Solution:
    def numberOfPoints(self, nums: List[List[int]]) -> int:
        nums.sort()
        s1, e1 = nums[0]
        result = 0
        for s2, e2 in nums[1:]:
            # print(s1, e1, s2, e2)
            if s2 <= e1:
                e1 = max(e1, e2)
            else:
                result += e1 - s1 + 1
                s1, e1 = s2, e2
        else:
            result += e1 - s1 + 1
        
        return result
```

## 2849. Determine if a Cell Is Reachable at a Given Time 判断能否在给定时间到达单元格

给定网格内的开始坐标`(sx, sy)`和结束坐标`(fx, fy)`，每一秒必须向四周的`8`个方向移动一格，问能否在给定时间`t`内从开始坐标到达结束坐标。

这道题隐含的条件是网格的大小是无限大，可以随意移动，因此只要从开始坐标到达结束坐标的的最短距离`t_min` 满足`t_min <= t`，就都可以到达。这里我们求最短距离的方式是`t_min = d + v`，其中`d`对角线移动的距离，`v`为直线移动的距离。这个比较好理解，我们从开始坐标，通过对角线移动，要么移动到`x`相同，要么移动到`y`相同，这样之后才可以直线移动到结束坐标。

但是，有一种特殊情况是当开始坐标和结束坐标是一样的时候，只移动一格一定无法到达，因为每一次都必须移动。

```python
class Solution:
    def isReachableAtTime(self, sx: int, sy: int, fx: int, fy: int, t: int) -> bool:
        # if self, need to move more than 1 to get back to self
        if sx == fx and sy == fy:
            return t != 1
        
        d = min(abs(fx - sx), abs(fy - sy))
        
        v = max(abs(fx - sx), abs(fy - sy)) - d
        
        return d + v <= t
```

## 2850. Minimum Moves to Spread Stones Over Grid 将石头分散到网格图的最少移动次数

`3 x 3`的矩阵中总共有`9`颗石子，其中有的点没有石子，有的点有多个石子。在每次只能移动一颗石子的情况下，问最少共需要多少步才可以使得每一个格子都恰好有一颗石子。

首先我们可以观察到，这道题无法使用贪心算法来求解。为什么这么说呢，请看下面的例子
```
Example:
Input: grid = [[1, 2, 0], [0, 1, 2], [1, 1, 1]]
```

这个例子的最优解法是`(0, 1) -> (1, 0)`和`(1, 2) -> (0, 2)`。但考虑到`(0, 1)`和`(1, 2)`的多余石子跟`(0, 2)`的空位距离相同，我们无法判断哪个是更优的。因此使用贪心算法很可能会走到次优解。

此外，移动石子这个过程相当于改变了整个棋盘的状态，动态规划也难以处理这样的场景。考虑到问题空间较小，我们直接使用暴力的backtracking来解决这个问题。

```python
class Solution:
    def minimumMoves(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        empty = []
        excess = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    empty.append((i, j))
                elif grid[i][j] > 1:
                    excess.append((i, j))
        
        def check(idx):
            if idx >= len(empty):
                return 0
            i, j = empty[idx]
            result = 1e9
            for x, y in excess:
                if grid[x][y] == 1:
                    continue
                grid[x][y] -= 1
                result = min(result, abs(x - i) + abs(y - j) + check(idx + 1))
                grid[x][y] += 1
            return result
    
        return check(0)
```

## 2851. String Transformation 字符串转换

有长度为`n`的字符串`s`和`t`，在每次操作中，你可以把`s`转换为任意`s[:i] + s[i:]`（`0 < i < n`）。问恰好转换`k`次之后，存在多少种转换方式使得转换后的`s`刚好与`t`一样。

这道题直接给了`2 <= n <= 5 * 10^5`和`1 <= k <= 10^15`，因此常规的dp铁定是用不了了，直接原地弃赛就可以了。

话虽这么说，我们还是可以通过常规的dp来帮助我们思考的。首先我们可以知道，倘若存在某种转换方式的话，`t`一定是`s`的某个旋转字符串。那么我们可以用数组下标的形式来表达`s`的旋转次数，即`s_i = s[:i] + s[i:]`。因此，我们可以用二维dp来表示可以转换的次数
```
Example
Input: s = "abcd", t = "cdab"
S_0 = [0, 0, 1, 0]
S_1 = [1, 1, 0, 1]
S_2 = [2, 2, 3, 2]
S_3 = [7, 7, 6, 7]
```

`S_0`表示移动`0`的时候各个旋转字符串`s_i`是否等于`t`。我们可以看到只有`s_2 = "cd" + "ab"`刚好为`t`，因此`S_0 = [0, 0, 1, 0]`。那么接下来当我们移动一次的时候，因为必须任意移动`0 < i < n`，`s_2`无法移动到其他的相等状态，而`s_0`，`s_1`和`s_3`都可以通过移动变成`s_2`或者`t`。其他`S_k`状态也用同样的方式，即初始的等价状态只能移动到其他状态，而其他状态可以移动到初始的等价状态。因此实际上整个状态表中我们只有这两种值。

我们可以把整个行为总结一下。假设存在`p`个`i`使得`s_i`刚好等于`t`，则有其他`q = n - p`个`i`使得`s_i`不为`t`。令$F_i$和$G_i$分别为第$i$次操作等价状态和非等价状态的值，则我们有以下的递归形式
$$
\begin{align}
F_i &= F_{i - 1} \times (p - 1) + G_{i - 1} \times q \\
G_i &= F_{i - 1} \times p + G_{i - 1} \times (q - 1)
\end{align}
$$

我们分别来讨论解释一下上面的两个递归方程

* $F_i$表示某一个旋转字符串`s'`在初始状态下刚好等于`t`的等价状态时，操作`i`次可以仍然等价的形式。
    
    * $F_{i - 1} \times (p - 1)$ 表明在从上一步的某个其他等价字符串`s''`变换一次也能得到`s'`（或者`t`），但不包含`s'`自身，因此存在`p - 1`种可能性。
    * $G_{i - 1} \times q$ 表明从上一步的非等价字符串`s'''`变换一次得到`s'`（或者`t`），因此存在`q`种可能性

* $G_j$ 则可以以同样的方式推导。

但是这样的解法是`O(k)`的，考虑到`k`的取值范围，我们需要使用更高阶的方法：矩阵快速幂。矩阵快速幂在很多地方都讨论过了，这里不多赘述。[这篇文章](https://hezhaojiang.github.io/post/2020/41da3a83/)在对我理解矩阵快速幂的应用场景时十分有效，推荐各位同学看下。

把上面的公式转换为矩阵形式，我们有
$$
\begin{bmatrix}
F_i \\
G_i
\end{bmatrix}
=
\mathbf{M}
\cdot
\begin{bmatrix}
F_{i - 1} \\
G_{i - 1}
\end{bmatrix}
$$
其中，
$$
\mathbf{M} = \begin{bmatrix}
p - 1 & q \\
p & q - 1
\end{bmatrix}
$$
而我们要计算的$F_k$和$G_k$则可以表示成
$$
\begin{bmatrix}
F_k \\
G_k
\end{bmatrix}
=
\mathbf{M}^k
\cdot
\begin{bmatrix}
F_0 \\
G_0
\end{bmatrix}
$$

```python
MOD = int(1e9 + 7)
class Solution:
    def numberOfWays(self, s: str, t: str, k: int) -> int:
        def find(s, t, n):
            idx = 0
            while idx != -1:
                idx = s.find(t, idx)
                if idx != -1:
                    if idx >= n:
                        break
                    yield idx
                    idx += 1

        def matrix_multiply(a, b):
            n = len(a)
            m = len(b[0])
            p = len(b)
            c = [[0 for _ in range(m)] for _ in range(n)]
            for i in range(n):
                for j in range(m):
                    for k in range(p):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= MOD

            return c

        def matrix_power(a, b):
            n = len(a)
            m = len(a[0])
            y = [[0 for _ in range(m)] for _ in range(n)]
            for i in range(n):
                y[i][i] = 1

            while b:
                if b & 1:
                    y = matrix_multiply(y, a)
                a = matrix_multiply(a, a)
                b >>= 1

            return y

        n = len(s)
        lst = list(find(s + s, t, n))
        p = len(list(i for i in lst if i < n))
        q = n - p
        # print(p, q)
        mat = [[p - 1, q], [p, q - 1]]
        # print(mat)
        mat = matrix_power(mat, k)

        # print(mat)

        if lst and lst[0] == 0:
            return mat[0][0]
        return mat[1][0]
```

到这里，就结束了这道题……了吗？还是图森破。都说了是8分的最后一题，那么简单就让你AC了岂不是很没面子？果然，直接出了TLE。看来还是我们的`find`方法太慢了，基本上等同于暴力计算。看来只能祭出KMP大法了。

KMP (Knuth-Morris-Pratt) 是一个令人闻之丧胆的话题，但是实际上它的原理并不难。我们要清楚，暴力搜索的缺点就在于完全不同的字串还是会进行搜索，特别是当存在前缀匹配但后缀不匹配的情况。而KMP就在这点上针对性的做了一些优化。KMP主要由两部分组成：

* 预处理步骤主要计算了前缀的匹配。对于每个模式字符串的子串，都会计算出这个子串的最长的相同的前缀和后缀的长度。
* 搜索步骤中利用了前面的前缀匹配，当在文本字符串中遇到不匹配的字符时，我们可以利用前缀函数跳过一些无需再次检查的字符。

直接上代码吧。

```python
        ...
        def compute_prefix_function(pattern):
            """
            This function computes the prefix function for the KMP algorithm.
            """
            prefix_function = [0] * len(pattern)
            j = 0

            for i in range(1, len(pattern)):
                while j > 0 and pattern[i] != pattern[j]:
                    j = prefix_function[j-1]
                if pattern[i] == pattern[j]:
                    j += 1
                prefix_function[i] = j

            return prefix_function

        def kmp_search(text, pattern):
            """
            This function searches for all occurrences of the pattern in the text using the KMP algorithm.
            """
            prefix_function = compute_prefix_function(pattern)
            j = 0
            result = []

            for i in range(len(text)):
                while j > 0 and text[i] != pattern[j]:
                    j = prefix_function[j-1]
                if text[i] == pattern[j]:
                    j += 1
                if j == len(pattern):
                    result.append(i - (j - 1))
                    j = prefix_function[j-1]

            return result

        ...
        lst = list(find(s + s, t, n))
        p = len(list(i for i in lst if i < n))
        ...
```

除了KMP之外，这道题还可以利用其他的方法，诸如Rabin-Karp (Rolling Hash)或者Z-Algorithm。感兴趣的同学就自己去研究吧。