Title: 解决Foobar挑战（三）
Slug: foobar-iv
Category: MISC
Date: 2023-05-13 19:00:00
Modified: 2023-10-09 22:00
Tags: Google Foobar
Summary: 接上回书，我们来到了Foobar挑战的第四层，题目越来越困难了。这篇文章给出了Foobar Level 4 的两道题 Running with Bunnies 和 Distract the Trainers 的解题思路和python代码。这一层要求我们掌握图相关的算法，包括Dijkstra，Floyd-Warshall，以及二分图和网络流算法，如匈牙利算法和Hopcroft-Karp算法。

Foobar系列已经全部完成了，你可以通过以下目录访问！

- [解决Foobar挑战（一）]({filename}/articles/11-foobar-challenge-ii.md)
- [解决Foobar挑战（二）]({filename}/articles/12-foobar-challenge-iii.md)
- 解决Foobar挑战（三）
- [解决Foobar挑战（四）- 终篇]({filename}/articles/16-google-foobar-v.md)

接上回书，我们来到了Foobar挑战的第四层。题目越来越困难了。

## Running with Bunnies

<details markdown="1">
  <summary>题目</summary>
You and the bunny workers need to get out of this collapsing death trap of a space station -- and fast! Unfortunately, some of the bunnies have been weakened by their long work shifts and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave -- you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
```
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
```
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

```
Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit
```
With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the solution is [1, 2].

Test cases
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

```
Input: solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output: [0, 1]
```
```
Input: solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output: [1, 2]
```
</details>

刚拿到题目的时候我是一脸懵逼的。描述实在太抽象了以至于人类难以理解。但是总而言之，在反复观摩了两天之后，我终于明白了题目的意思。给定一个`n x n`的距离矩阵`times`，其中位置`0`是起始点，位置`n-1`是出口，而位置`1,2...n-2`是每只兔子的位置。在给定时间`time_limit`内，要求你营救尽可能多的兔子（即到达兔子所在的位置），并在时间耗尽之前到达出口，最后输出你营救兔子的顺序。此外，还有一点是从一个位置跳到另一个位置的时候，消耗可能为负数，即走这条路的话时间反而会增加。在存在负数边的这个前提之下，剩余时间也可以短暂变为负数，只要保证到达出口的时候为非负数，出口就会重新打开。

……好的，理解完题目之后，还是一脸懵逼。不过，至少理解了他是个图的题目。但是跟正常套路图题目不一样的地方有两点。首先它要求的是尽可能多的营救兔子，而不是什么最短路径，因此我们可以排除狄克斯特拉这种算法。其次，他还要求出营救的顺序，因此我们在考虑算法的时候也需要想到营救兔子的顺序可能会影响结果的可能性。不过，要注意的是，他要求的是**营救兔子的顺序**，而不是到达每个点的**路径顺序**。在走的过程中，你仍然可以重复经过有兔子的地方。在捋清楚这两点之后，我决定用backtrack试一下。此外，因为路径顺序无关，我们考虑用Floyd Warshall来储存最短距离矩阵，这样就避免了处理路径的麻烦问题。

首先基于Floyd Warshall在$O(n^3)$时间内求出每个点到每个点的最短距离。接着backtracking的核心逻辑就比较暴力了，我们尝试每一种营救兔子的解决方案，当我们每次到达终点的时候，我们都尝试更新营救的兔子列表。这里我们允许剩余时间暂时为负数，只有最终结果的时候才检查剩余时间是否大于等于零。还有一个化简条件可以应用。即当节点`i`到自身的消耗为负数时，我们总可以凑到很多时间去救所有兔子，因此这里可以直接返回所有兔子的ID。

```python
def floyd_warshall(times):
    n = len(times)
    dist = [list(t) for t in times] # list.copy
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


result = None

def solution(times, times_limit):
    # reset
    # I hate python2 foobar should consider use python3
    global result
    result = []
    
    # computes the shortest distance by floyd warshall
    dist = floyd_warshall(times)
    
    # if there are negative cycle, we can always hit
    # it to add more time and save all bunnies
    for i in range(len(times)):
        if dist[i][i] < 0:
            return [i for i in range(len(times) - 2)]
    
    def bt(dist, time_limit, i, visited, bunnies):
        # only for python3
        # nonlocal result
        
        if time_limit < -1000:
            return
        
        global result
        if i == len(dist) - 1:
            if time_limit >= 0 and len(bunnies) > len(result):
                result = list(bunnies) # list.copy
            return

        if visited[i]:
            return
        visited[i] = True
        bunnies.append(i - 1)

        for j in range(0, len(dist)):
            if i == j:
                continue
            bt(dist, time_limit - dist[i][j], j, visited, bunnies)
        
        bunnies.pop()
        visited[i] = False
    
    visited = [False] * len(times)
    visited[0] = True
    # try each bunny as starting point
    for i in range(1, len(dist) - 1):
        bt(dist, times_limit - dist[0][i], i, visited, [])
    
    return sorted(result)
```


## Distract the Trainers

<details markdown="1">
  <summary>题目</summary>
The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

Test cases

Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.
```
Input: solution.solution([1, 7, 3, 21, 13, 19])
Output: 0
```
```
Input: solution.solution(1,1)
Output: 2
```
</details>

给定一个列表`banana_list`，代表每一个trainer拥有的香蕉个数。如果你将两个trainer匹配在一起，那么他们就会用香蕉来打赌。若两个trainer分别有`A`和`B`个香蕉，且`A < B`，那么一局游戏之后他们的香蕉个数分别为`2A`和`B - A`。他们会一直玩这个游戏，直到`A = B`才会停下来 ---- 或者永远不会停下来，陷入一个死循环。我们需需要根据他们的香蕉数量尽可能地匹配使得陷入死循环的trainer最多，且每个trainer最多匹配一次。

一个立即需要解决的问题就是，什么样的数字对才可以形成题目描述的死循环呢？简单模拟下可知，只有两个数字之和为二次幂才可以形成。此外，`A`和`B`的数字大小也不重要，把他们通过`gcd`最大公因数化简之后的结果仍然等于原来的结果。如`1 4`和`2 8`都会循环，`1 3`和`2 6`都会终止。

接下来需要解决的是如何进行匹配的问题。最终需要配对的这个性质使得这个题目看起来有点像二分图的最大匹配，即给定一个图，我们要求找到最多的边，且这些边没有共同的节点。到这里这道题的考点才明晰起来。首先我们来介绍两个概念：

- 交替路 Alternating path：从一个未匹配点出发，依次经过非匹配边、匹配边、非匹配边…形成的路径叫交替路。
- 增广路 Augmenting path：从一个未匹配点出发，走交替路，如果途径另一个未匹配点（不包含出发点），则这条交替路称为增广路。
当我们找到一条增广路时，我们只要把增广路中间的匹配边和非匹配边的身份交换即可，这样不会破坏匹配的性质，且会将匹配的边的长度增加`1`。而对于我们的情况来说，只要能够判断从某个点开始是否形成增广路，即可知道这个点是否可以被包括进匹配对里。

对于这道题来说，若两个trainer能形成死循环，则我们说这两个trainer之间有一条边相连。这样的话可以在`O(n^2)`时间生成图。接着我们对于整个图中的每个点开始贪心匹配增广路。从点`A`开始，若点`A`的邻居`B`没有被匹配过，那么`A`和`B`就可以被匹配；若`B`已经匹配了`C`，那么就将`A`和`B`匹配，并递归匹配`C`。

```python
from collections import defaultdict

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def is_infinite_loop(x, y):
    total = x + y
    g = gcd(x, y)
    total //= g

    return (total & (total - 1)) != 0

def solution(banana_list):
    n = len(banana_list)
    graph = defaultdict(list)

    for i in range(n):
        for j in range(i+1, n):
            if is_infinite_loop(banana_list[i], banana_list[j]):
                graph[i].append(j)
                graph[j].append(i)
    
    def bpm(u, matched, visited):
        for v in graph[u]:
            if visited[v]:
                continue
            visited[v] = True
            if matched[v] == -1 or bpm(matched[v], matched, visited):
                matched[v] = u
                return True
        return False
    
    matched = [-1] * n
    
    result = 0
    for i in range(n):
        visited = [False] * n
        if bpm(i, matched, visited):
            result += 1
        print(i, matched)
    
    # print(matched)
    
    if result % 2 == 1:
        result -= 1
    return n - result
```

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

上面这个解法中，使用的方法其实是简化版本的Hopcroft-Karp算法。有差异的地方是，Hopcroft-Karp算法会输出所有的边，而这道题只需要判断点是否属于一个增广路。对于Hopcroft-Karp算法来说，首先会使用BFS从每个未匹配的点开始寻找增广路径。然后利用与此解法类似的DFS算法对于每条增广路径进行增广，以寻找最大匹配。

## 小结

相比起前一层来说，第四层显著花费了我更多的时间在寻找相关的算法上面。好在时间给的非常充裕，每道题都有360个小时的完成时间。此外，还进一步拓展了我对于图算法的知识边界。

在我研究第二题的过程中，这些资料对我有很大的帮助，你也可以看看：

- [最大流求解 & 增广路定理](https://zhuanlan.zhihu.com/p/391388290)
- [Columbia IEOR 8100  Matching Algorithms for Bipartite Graphs](http://www.columbia.edu/~cs2035/courses/ieor8100.F12/lec4.pdf)