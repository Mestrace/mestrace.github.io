Title: Weekly Contest 397 周赛题目解析
Slug: weekly-397
Date: 2024-06-11 10:35
Category: Leetcode
Tags: Contest
Summary: 2024-05 Leetcode Weekly Contest 397 第 397 场力扣周赛 | Solution to contest problems 赛题讲解 | 3146. Permutation Difference between Two Strings 两个字符串的排列差 | 3147. Taking Maximum Energy From the Mystic Dungeon 从魔法师身上吸取的最大能量 | 3148. Maximum Difference Score in a Grid 矩阵中的最大得分 | 3149. Find the Minimum Cost Array Permutation 找出分数最低的排列

[Weekly Contest 397](https://leetcode.com/contest/weekly-contest-397/)

[第 397 场周赛](https://leetcode.cn/contest/weekly-contest-397/)

## 题目列表

- [3146. Permutation Difference between Two Strings 两个字符串的排列差](https://leetcode.com/problems/permutation-difference-between-two-strings/description/)
- [3147. Taking Maximum Energy From the Mystic Dungeon 从魔法师身上吸取的最大能量](https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/description/)
- [3148. Maximum Difference Score in a Grid 矩阵中的最大得分](https://leetcode.com/problems/maximum-difference-score-in-a-grid/description/)
- [3149. Find the Minimum Cost Array Permutation 找出分数最低的排列](https://leetcode.com/problems/find-the-minimum-cost-array-permutation/description/)

## 3146. Permutation Difference between Two Strings 两个字符串的排列差

按照题意模拟即可。题目里提到了每个字母最多出现一次，因此可以用字典存储。

```python
class Solution:
    def findPermutationDifference(self, s: str, t: str) -> int:
        idx = dict()
        
        for i,c in enumerate(s):
            idx[c] = i
        
        result = 0
        for j,c in enumerate(t):
            result += abs(j - idx[c])
        
        return result
```

## 3147. Taking Maximum Energy From the Mystic Dungeon 从魔法师身上吸取的最大能量

在地牢中有一列魔法师，他们每个人都有整数魔法值$energy_i$。当你走到魔法师的位置时，你的魔法值会增加或者减少$energy_i$。每次移动时，你必须从`i`移动到接下来第`k`个魔法师的位置，也就是`i + k`，直到你无法再移动为止。假设你可以从任意`i`开始进行移动操作，求你最多能获得的魔法值。

这题我们可以很明显的看出其中的递推关系，即位置`i`的结果取决于`i + k`的结果。因此我们可以直接用动态规划求解。

```python
class Solution:
    def maximumEnergy(self, energy: List[int], k: int) -> int:
        
        from functools import cache
        
        @cache
        def dp(i):
            if i >= len(energy):
                return 0
            return energy[i] + dp(i + k)
        
        return max(dp(j) for j in range(len(energy)))
```

## 3148. Maximum Difference Score in a Grid 矩阵中的最大得分

给定一个`m x n`的正整数矩阵，你可以从任意一点`(x, y)`向右平移到同一行的另一个点`(x, y')`，或者向下平移到同一列的任意一个点`(x', y)`。令旧点在矩阵中的值为`c1`，新点的值为`c2`，则每次移动你获得`c2 - c1`的分数。你可以从任意一点开始，至少进行一次移动后，求你能获得的最大分数。

假设我们从`c1 -> c2 -> c3`进行了三次合法移动，那么我们的分数为`(c2 - c1) + (c3 - c2)`，最终可得`c3 - c1`。我们得到的结论是，分数只与起点与终点的值有关，而与中间的路径分数无关。利用这一点，我们大大简化我们的计算。首先我们利用dp的方式，求出在点`(x, y)`右边和下面所形成的长方形矩阵中最大的值，那么点`(x, y)`所能取得的最大分数就是这两个数之间的差值。

```python
class Solution:
    def maxScore(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        MIN_NUM = -(1e9 + 7)
        MAX_NUM = 1e9 + 7
        
        dp = [[0] * n for _ in range(m)]
        
        dp[-1][-1] = MIN_NUM
        
        for i in reversed(range(m - 1)):
            dp[i][-1] = max(grid[i + 1][-1], dp[i + 1][-1])
        
        for j in reversed(range(n - 1)):
            dp[-1][j] = max(grid[-1][j + 1], dp[-1][j + 1])
        
        for i in reversed(range(m - 1)):
            for j in reversed(range(n - 1)):
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1], grid[i + 1][j], grid[i][j + 1])
        
        # print(dp)
        
        result = MIN_NUM
        for i in range(m):
            for j in range(n):
                result = max(result, dp[i][j] - grid[i][j])
        
        return result
```

## 3149. Find the Minimum Cost Array Permutation 找出分数最低的排列

`nums`和`perm`都是一个长度为n的对于`[0,n-1]`数字的排列。对于给定的一个`nums`，一个`perm`的分数定义为
```
score(perm) = |perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + ... + |perm[n - 1] - nums[perm[0]]|
```

求使得分数最小的`perm`。若存在多个`perm`，返回字典序最小的。

我们可以敏锐地注意到，分数的表达式是一个循环的形式，因此对于任意给定的排列`perm`，我们将其数据循环移动任意次，分数也不会改变。为了验证这一猜想，我们来用一下表达式。令

$perm = [perm[0], perm[1], perm[2], ..., perm[n-1]]$

位移一次之后我们有

$perm' = [perm[1], perm[2], ..., perm[n-1], perm[0]]$

则新的分数为

$$score(perm') = |perm[1] - nums[perm[2]]| + |perm[2] - nums[perm[3]]| + ... + |perm[n-1] - nums[perm[0]]| + |perm[0] - nums[perm[1]]|$$

实际上只是把 $score(perm)$ 进行了一次位移。考虑到本体要求字典序最小的，我们总可以把`0`移动到起始点让其最小。接下来我们用代码验证一下这个猜想。首先我给出一个暴力计算分数的函数`score`。

```python
def score(nums, perm):
    n = len(nums)
    total_score = 0
    
    for i in range(n):
        if i == n - 1:
            diff = abs(perm[i] - nums[perm[0]])
        else:
            diff = abs(perm[i] - nums[perm[i + 1]])
        
        total_score += diff
    
    return total_score
```

为了更直观地展示，我给出一个打印表达式的方法`score_string`
```python
def score_string(nums, perm):
    n = len(nums)
    score_parts = []
    
    for i in range(n):
        if i == n - 1:
            diff = abs(perm[i] - nums[perm[0]])
            score_part = f"|{perm[i]} - {nums[perm[0]]}|"
        else:
            diff = abs(perm[i] - nums[perm[i + 1]])
            score_part = f"|{perm[i]} - {nums[perm[i + 1]]}|"
        
        score_parts.append(score_part)
    
    score_string = " + ".join(score_parts)
    return f"{score_string}"
```

然后，我们就可以遍历所有排列来看他们的分数是什么
```python
def print_all_scores(nums):
    slist = []
    
    for perm in permutations(nums):
        slist.append((score(nums, perm), score_string(nums, perm), perm))
    
    slist.sort()
        
    for s, ss, perm in slist:
        print(f"perm {perm} yields {s}, score = {ss}")
```

```python
In [1]: print_all_scores([1, 0, 2])
perm (0, 1, 2) yields 2, score = |0 - 0| + |1 - 2| + |2 - 1|
perm (1, 2, 0) yields 2, score = |1 - 2| + |2 - 1| + |0 - 0|
perm (2, 0, 1) yields 2, score = |2 - 1| + |0 - 0| + |1 - 2|
perm (0, 2, 1) yields 4, score = |0 - 2| + |2 - 0| + |1 - 1|
perm (1, 0, 2) yields 4, score = |1 - 1| + |0 - 2| + |2 - 0|
perm (2, 1, 0) yields 4, score = |2 - 0| + |1 - 1| + |0 - 2|
In [2]: print_all_scores([0,1,3,2])
perm (0, 1, 3, 2) yields 4, score = |0 - 1| + |1 - 2| + |3 - 3| + |2 - 0|
perm (0, 3, 2, 1) yields 4, score = |0 - 2| + |3 - 3| + |2 - 1| + |1 - 0|
perm (1, 0, 3, 2) yields 4, score = |1 - 0| + |0 - 2| + |3 - 3| + |2 - 1|
perm (1, 3, 2, 0) yields 4, score = |1 - 2| + |3 - 3| + |2 - 0| + |0 - 1|
perm (2, 0, 1, 3) yields 4, score = |2 - 0| + |0 - 1| + |1 - 2| + |3 - 3|
perm (2, 1, 0, 3) yields 4, score = |2 - 1| + |1 - 0| + |0 - 2| + |3 - 3|
perm (3, 2, 0, 1) yields 4, score = |3 - 3| + |2 - 0| + |0 - 1| + |1 - 2|
perm (3, 2, 1, 0) yields 4, score = |3 - 3| + |2 - 1| + |1 - 0| + |0 - 2|
perm (0, 1, 2, 3) yields 6, score = |0 - 1| + |1 - 3| + |2 - 2| + |3 - 0|
perm (0, 2, 3, 1) yields 6, score = |0 - 3| + |2 - 2| + |3 - 1| + |1 - 0|
perm (1, 0, 2, 3) yields 6, score = |1 - 0| + |0 - 3| + |2 - 2| + |3 - 1|
perm (1, 2, 3, 0) yields 6, score = |1 - 3| + |2 - 2| + |3 - 0| + |0 - 1|
perm (2, 3, 0, 1) yields 6, score = |2 - 2| + |3 - 0| + |0 - 1| + |1 - 3|
perm (2, 3, 1, 0) yields 6, score = |2 - 2| + |3 - 1| + |1 - 0| + |0 - 3|
perm (3, 0, 1, 2) yields 6, score = |3 - 0| + |0 - 1| + |1 - 3| + |2 - 2|
perm (3, 1, 0, 2) yields 6, score = |3 - 1| + |1 - 0| + |0 - 3| + |2 - 2|
perm (0, 3, 1, 2) yields 8, score = |0 - 2| + |3 - 1| + |1 - 3| + |2 - 0|
perm (0, 2, 1, 3) yields 8, score = |0 - 3| + |2 - 1| + |1 - 2| + |3 - 0|
perm (1, 3, 0, 2) yields 8, score = |1 - 2| + |3 - 0| + |0 - 3| + |2 - 1|
perm (1, 2, 0, 3) yields 8, score = |1 - 3| + |2 - 0| + |0 - 2| + |3 - 1|
perm (2, 0, 3, 1) yields 8, score = |2 - 0| + |0 - 2| + |3 - 1| + |1 - 3|
perm (2, 1, 3, 0) yields 8, score = |2 - 1| + |1 - 2| + |3 - 0| + |0 - 3|
perm (3, 0, 2, 1) yields 8, score = |3 - 0| + |0 - 3| + |2 - 1| + |1 - 2|
perm (3, 1, 2, 0) yields 8, score = |3 - 1| + |1 - 3| + |2 - 0| + |0 - 2|
```

对于这一题，我们采用dfs进行搜索。我们还可以观察到，数组长度最多为`14`，因此我们可以使用bit mask的方式来标记已经走过的状态。那么这一题就可以转换成通过记忆化的方式进行搜索。但是要注意的是，我们在搜索完成最小的结果之后，之后要重新构建整个路径。因此对于每一个产生更新的点位，我们不仅要记忆它的最大分数，还要记忆他下一步跳的点位是什么。

此外，题目中还提到了对于字典序的要求。我们可以看到在`[0,1,3,2]`这个例子中，从零开始的有两种最小结果`(0, 1, 3, 2)`和`(0, 3, 2, 1)`。我们在dfs遍历状态的时候，优先从更小的数字中搜索，这样就可以无心插柳柳成荫地规避掉这个问题了。

```python

INT_MAX = int(1e9 + 7)
class Solution:
    def findPermutation(self, nums: List[int]) -> List[int]:

        n = len(nums)
        dp = [[-1] * 16384 for _ in range(14)]
        val = [[0] * 16384 for _ in range(14)]

        def dfs(mask, p):
            if bin(mask).count('1') == n:
                return abs(p - nums[0])
            
            if dp[p][mask] >= 0:
                return dp[p][mask]
            
            dp[p][mask] = INT_MAX

            for i in range(1, n):
                if (mask & (1 << i)) == 0:
                    result_n = abs(p - nums[i]) + dfs(mask + (1 << i), i)
                    if result_n < dp[p][mask]:
                        dp[p][mask] = result_n
                        val[p][mask] = i
            
            return dp[p][mask]
        
        dfs(1, 0)

        mask = 1
        result = [0]
        while bin(mask).count('1') < n:
            result.append(val[result[-1]][mask])
            mask += (1 << result[-1])
        
        return result
```