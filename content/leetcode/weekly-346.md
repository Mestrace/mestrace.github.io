Title: Weekly Contest 346 周赛题目解析
Slug: weekly-346
Date: 2023-05-21 22:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-05 Leetcode Weekly Contest 346 第 346 场力扣周赛 | 2696. Minimum String Length After Removing Substrings 删除子串后的字符串最小长度 | 2697. Lexicographically Smallest Palindrome 字典序最小回文串 | 2698. Find the Punishment Number of an Integer 求一个整数的惩罚数 | 2699. Modify Graph Edge Weights 修改图中的边权 | Solution to contest problems 赛题讲解 | Weighted Graph 有权图

[Weekly Contest 346](https://leetcode.com/contest/weekly-contest-346/)

[第 346 场周赛](https://leetcode.cn/contest/weekly-contest-346/)

前三题比较手速，最后一题虽然难但也是可以理解的程度。随便写写

## 题目列表

- [2696. Minimum String Length After Removing Substrings](https://leetcode.com/problems/minimum-string-length-after-removing-substrings/)
- [2697. Lexicographically Smallest Palindrome](https://leetcode.com/problems/lexicographically-smallest-palindrome/)
- [2698. Find the Punishment Number of an Integer](https://leetcode.com/problems/find-the-punishment-number-of-an-integer/)
- [2699. Modify Graph Edge Weights](https://leetcode.com/problems/modify-graph-edge-weights/)

## 2696. Minimum String Length After Removing Substrings 删除子串后的字符串最小长度

给定一个纯大写字母列表，删除其中所有的`AB`和`CD`，并返回最终结果的长度。要注意的是，`AABB`应该全部删掉。

用stack进行模拟，每次最后两个词是否为`AB`或者`CD`，若是的话就进行pop。

```python
class Solution:
    def minLength(self, s: str) -> int:
        stack = []  # Use a stack to keep track of the remaining characters after removing substrings

        for char in s:
            if char == 'B' and stack and stack[-1] == 'A':
                stack.pop() 
            elif char == 'D' and stack and stack[-1] == 'C':
                stack.pop()
            else:
                stack.append(char)  # Push any other character onto the stack

        return len(stack)  # Return the length of the resulting string
```

## 2697. Lexicographically Smallest Palindrome 字典序最小回文串

给定一个字符串`s`，每次操能改变其中的一个字母为任意小写字母。要求让这个字符串变为回文字符串，并要求操作次数最小。若存在多个解的话，需要返回字典序最小的那个。

这题最简单的方式是贪心进行求解。比较头尾两个字母，若这两个字母一样，则不需要变化。若这两个字母不一样，应该变化为较小的那个，这样才会在操作次数较少的情况下变为字典序最小。这里我们只需要看前半部分，并实时计算后半部分对应的索引即可。若为奇数长度的话，还需要加上正中间那个字符。

```python
class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        n = len(s)
        palindrome = []
        for i in range(n // 2):
            if s[i] == s[n - 1 - i]:
                palindrome.append(s[i])
            else:
                palindrome.append(min(s[i], s[n - 1 - i]))
        
        return ''.join(palindrome) + (s[n // 2] if n % 2 != 0 else '') + ''.join(palindrome[::-1])
```

## 2698. Find the Punishment Number of an Integer 求一个整数的惩罚数

一个数字`n`的惩罚数定义为所有满足条件的数字的平方和。条件为：1）`0 < i <= n`，2）`i * i`的被分割为多个子串后的数字表示之和等于`i`。给定这个数字`n`，求惩罚数。

我们可以用一个朴素的backtrack方式来求惩罚数，每次取`n`位形成新的数字相加，并递归后面的数字。

```python
def is_valid_partition(num_str, target):
    if len(num_str) == 0:
        return target == 0

    for i in range(1, len(num_str) + 1):
        current_num = int(num_str[:i])
        if current_num > target:
            return False
        if is_valid_partition(num_str[i:], target - current_num):
            return True

    return False

result = []
for i in range(1001):
    if is_valid_partition(str(i * i), i):
        result.append(i)
print(f"[{','.join(map(str, result))}]")
```

可以观察到，满足条件的数字都是一样的，因此我们可以先计算好然后直接进行打表。

```python
NUM = [0,1,9,10,36,45,55,82,91,99,100,235,297,369,370,379,414,657,675,703,756,792,909,918,945,964,990,991,999,1000]

from bisect import bisect_right

class Solution:
    
    def punishmentNumber(self, n: int) -> int:
        
        idx = bisect_right(NUM, n)
        
        return sum(i * i for i in NUM[:idx])
```

## 2699. Modify Graph Edge Weights 修改图中的边权

给定一个无向有权图，其中有一些边的权重为`-1`，剩余边的权重都为正整数。给定开始结束点`source`和`destination`，要求将所有`-1`边的权重更新为某个正整数，使得图中`source`和`destination`的最短路径权重为`target`。最终输出更新后的图的所有的边。

这道题只要求最短路径权重，加上最多只有100个点，因此我们用floyd-warshall去简化我们的思路，初始时间复杂度为$O(n^3)$。一个最朴素的思想就是，我们基于正常边构建一个相邻距离矩阵之后，依次把每条非法`-1`边加入图中。加入的顺序与最终结果无关。若存在`A - B - C - D`三条非法边组成的最短路径，我们总可以让前两条边的权重为`1`，最后一条边的权重为`target - 2`。此外，每次加入一条新的边之后，我们要以$O(n^2)$的复杂度更新距离矩阵。

不过，这个方法用Python是会TLE的，用Cpp是可以AC的，classic leetcode。

```python
LARGE = int(1e9 + 1)

class Solution:
    def modifiedGraphEdges(self, n: int, edges: List[List[int]], source: int, destination: int, target: int) -> List[List[int]]:

        # Initialize distance matrix with infinity
        dist_matrix = [[float('inf')]*101 for _ in range(101)]

        # Distance from a node to itself is 0
        for i in range(n):
            dist_matrix[i][i] = 0

        # Fill in initial distances
        negatives = []
        for i, (a, b, w) in enumerate(edges):
            if w == -1:
                negatives.append(i)
                continue
            dist_matrix[a][b] = w
            dist_matrix[b][a] = w 

        # Apply Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # If going through node k makes the path from i to j shorter, update the path
                    if dist_matrix[i][k] + dist_matrix[k][j] < dist_matrix[i][j]:
                        dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
        
        if dist_matrix[source][destination] < target:
            return []
        
        for nid in negatives:
            a,b, _ = edges[nid]
            # if we already achieved the target
            if dist_matrix[source][destination] == target:
                edges[nid][2] = LARGE
                continue
            
            pass_ab = 1 + dist_matrix[source][a] + dist_matrix[destination][b]
            pass_ba = 1 + dist_matrix[source][b] + dist_matrix[destination][a]
            
            if pass_ab <= target:
                w = target - pass_ab + 1
            elif pass_ba <= target:
                w = target - pass_ba + 1
            else:
                w = 1

            # Update the shortest paths for all pairs using the new edge
            for i in range(n):
                for j in range(n):
                    dist_matrix[i][j] = min(dist_matrix[i][j], dist_matrix[i][a] + w + dist_matrix[b][j], dist_matrix[i][b] + w + dist_matrix[a][j])
            edges[nid][2] = w

        # impossible
        if dist_matrix[source][destination] != target:
            return []

        return edges        
```