Title: 【Leetcode题解】Weekly Contest 341 周赛题目解析
Slug: weekly-341
Date: 2023-04-19 21:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-04 Leetcode Weekly Contest 341 第 341 场力扣周赛 | 2643. Row With Maximum Ones 一最多的行 | 2644. Find the Maximum Divisibility Score 找出可整除性得分最大的整数 | 2645. Minimum Additions to Make Valid String 构造有效字符串的最少插入数 | 2646. Minimize the Total Price of the Trips 最小化旅行的价格总和 | Solution to contest problems 赛题讲解 | 状态机 State Machine | 树 Tree | Depth First Search | 最近公共祖先 Lowest Common Ancestor

[Weekly Contest 341](https://leetcode.com/contest/weekly-contest-341/)

[第 341 场力扣周赛](https://leetcode.cn/contest/weekly-contest-341/)

这次的周赛跟双周赛还是一样的味道。以三道手速题开头，并以一道图题结尾，但是数据范围都给的较小（<span title="你知道的太多了" class="heimu">谁让你们总是吐槽TLE</span>）。此外，某些OIer还在评论区叫嚣应该把最后一题数据量从`50`加到`1e5`。这里我严正谴责这些朋友们，要给我们这些普通人一点希望才行啊。好了不多说废话了，来看看这周的题目。

## 题目列表

- [Easy - 2643. Row With Maximum Ones](https://leetcode.com/problems/row-with-maximum-ones/)
- [Easy - 2644. Find the Maximum Divisibility Score](https://leetcode.com/problems/find-the-maximum-divisibility-score/)
- [Medium - 2645. Minimum Additions to Make Valid String](https://leetcode.com/problems/minimum-additions-to-make-valid-string/)
- [Hard - 2646. Minimize the Total Price of the Trips](https://leetcode.com/problems/minimize-the-total-price-of-the-trips/)

## 2643. Row With Maximum Ones 一最多的行

顺序遍历，取和即可。

### 代码

```python
class Solution:
    def rowAndMaximumOnes(self, mat: List[List[int]]) -> List[int]:
        total_ones = 0
        result_index = 0

        for i, row in enumerate(mat):
            ones_count = sum(row)
            if ones_count > total_ones:
                total_ones = ones_count
                result_index = i

        return [result_index, total_ones]
```

## 2644. Find the Maximum Divisibility Score 找出可整除性得分最大的整数

顺序遍历divisor，对于每一个divisor通过整除nums计算分数，并找到最大的即可。注意条件里还有要求若分数相同，取最小的divisor。

### 代码

```python
class Solution:
    def maxDivScore(self, nums: List[int], divisors: List[int]) -> int:
        max_score = -1
        max_divisor = 0

        for divisor in divisors:
            score = 0
            for num in nums:
                if num % divisor == 0:
                    score += 1

            if score > max_score or (score == max_score and divisor < max_divisor):
                max_score = score
                max_divisor = divisor

        return max_divisor
```

## 2645. Minimum Additions to Make Valid String 构造有效字符串的最少插入数

给定一个只有`a`,`b`,`c`三个字母的字符串，可以往里面插入任意次数的这三个字母，使得生成的字符串为`abc`三个字符串联任意次数。求最小的插入数量。

我们发现需要通过上一个字母和当前字母判断是否需要插入。这里我们贪心的读取并判断是否需要插入，按照题意进行模拟即可。

### 代码

这题其实完全用不到deque，只要用一个数字去确保索引就可以了。

```python
class Solution:
    def addMinimum(self, word: str) -> int:
        q = deque()
        
        result = 0
        
        all_letters = ['a', 'b', 'c']
        def add_until(l):
            nonlocal result
            while all_letters[(len(q)) % len(all_letters)] != l:
                q.append(all_letters[len(q) % len(all_letters)])
                result += 1
        
        for letter in word:
            if letter == 'a':
                if q and q[-1] != 'c':
                    add_until('a')
            elif letter == 'b':
                if not q or q[-1] != 'a':
                    add_until('b')
            elif letter == 'c':
                if not q or q[-1] != 'b':
                    add_until('c')
            q.append(letter)
            # print(q)
        
        if q[-1] != 'c':
            add_until('a')

        
        return result
```

## 2646. Minimize the Total Price of the Trips 最小化旅行的价格总和

给定一个有`n`个节点的树，一个列表`price`代表经过某一个节点的代价，一个`trips`列表，其中每一个`trips[i] = [a, b]`代表从树中的节点`a`到节点`b`的旅行。此外，在所有旅行开始之前，你有一次减少旅行代价的机会。你可以任意挑选一个集合的节点，且这些节点不相邻，并将他们的代价减半。找出一种一种方法，使得所有路径的代价和最小，并返回总的代价。

这道题题目有一定的复杂性。抛开减半的条件不谈，如果要求路径和，我们可以用dfs的方式去遍历整个图。而正是这个减半的条件，让整个问题都复杂了不少。

题目要求找到一个集合的不相邻节点。这里可能会有一个误区。很多同学（<span title="你知道的太多了" class="heimu">譬如我</span>）会联想到，对于一个树来说，最多被分为两个不相邻的节点集合。这个说法没有错，但是这里我们并不是要取全部的节点，所以可以有任意多种组合去取这个减半集合。

实际上，我们观察到，题目要求的最小路径代价和不仅与节点的价格相关，而且跟经过节点的次数也相关。这里也可以顺势联想到，最小化路径和即最大化减半可以减少的代价和。这样我们就把问题转化成两部分。第一部分是求出所有路经总和。像前面所说，用DFS直接遍历即可。此外，要最大化减半代价和。首先在前面的DFS中我们可以顺势找到经过某一个节点的次数。接着我们可以用DP的方式来求解。对于这道题来说，无非就两个点：

- 若相邻节点被减半了，那么当前节点不能被减半，则不能为我们的最大化减半代价和做贡献。
- 若所有相邻节点都没被减半，那么当前节点可以被囊括进减半集合，也可以不被囊括。

这样我们就用文字描述出了我们的状态转移方程。接着就可以进入代码环节了。

顺带一提，这道题跟[337. House Robber III](https://leetcode.com/problems/house-robber-iii/)和[1372. Longest ZigZag Path in a Binary Tree
](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/)有一些共性，可以去看看。

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

虽然对于这道题来说，数据范围较小，可以用DFS暴力解决。但是有更优雅的方式进行处理。不难看出，对于这个无根树，我们可以选定任意节点为根。基于这一点，我们把这个问题转化为求[最近公共祖先](https://oi-wiki.org/graph/lca/)的问题，可以利用一些更高阶的（<span title="你知道的太多了" class="heimu">我也不会的</span>）技巧，如[Tarjan算法](https://www.cnblogs.com/wkfvawl/p/9415280.html)离线求出所有结点的最近公共祖先。并利用这一点把整条路径上的代价都归并到祖先上。剩余求总路径和最大化代价的方式是一样的。这里我就交给读者去自行学习了。


### 代码

```python
class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        counter = Counter()
        total_cost = 0

        def dfs(node, parent, end):
            nonlocal total_cost

            counter[node] += 1
            total_cost += price[node]

            if node == end:
                return True

            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if dfs(neighbor, node, end):
                    return True
            
            counter[node] -= 1
            total_cost -= price[node]
            return False
        
        for start, end in trips:
            dfs(start, -1, end)
        
        @cache
        def dp(node, parent, can_reduce):
            result = 0

            if can_reduce:
                result = (price[node] // 2) * counter[node]

            for neighbor in graph[node]:
                if neighbor == parent:
                    continue

                if can_reduce:
                    result += dp(neighbor, node, False)
                else:
                    result += max(dp(neighbor, node, False), dp(neighbor, node, True))
            
            return result
        
        reduce = 0
        for i in range(n):
            reduce = max(reduce, dp(i, -1, True), dp(i, -1, False))
        
        return total_cost - reduce
```

## 小结

前三题还是非常手速的。我上去直接做了第三题，结果吃了点小亏。然后第四题又卡住了。树的题目还是非常考验思路的，如[周赛338中的收集树中金币]({filename}/leetcode/weekly-338.md)对于无根树的剪枝就比较巧妙。总之还是继续努力吧。

如果你想要变得更强的话，可以做做

- [Medium - 1339. Maximum Product of Splitted Binary Tree](https://leetcode.com/problems/maximum-product-of-splitted-binary-tree/)
- [Medium - 2477. Minimum Fuel Cost to Report to the Capital](https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/)
- [Hard - 124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/submissions/)
- [Hard - 2246. Longest Path With Different Adjacent Characters](https://leetcode.com/problems/longest-path-with-different-adjacent-characters/description/)