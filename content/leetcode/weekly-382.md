Title: Weekly Contest 382 周赛题目解析
Slug: weekly-382
Date: 2024-02-06 22:00
Category: Leetcode
Tags: Contest
Summary: 2024-01 Leetcode Weekly Contest 382 第 382 场力扣周赛 | 3019. Number of Changing Keys 按键变更的次数 | 3020. Find the Maximum Number of Elements in Subset 子集中元素的最大数量 | 3021. Alice and Bob Playing Flower Game Alice 和 Bob 玩鲜花游戏 | 3022. Minimize OR of Remaining Elements Using Operations 给定操作次数内使剩余元素的或值最小 | Solution to contest problems 赛题讲解

[Weekly Contest 382](https://leetcode.com/contest/weekly-contest-382/)

[第 382 场周赛](https://leetcode.cn/contest/weekly-contest-382/)

本周没有锐评。

## 题目列表

- [3019. Number of Changing Keys 按键变更的次数](https://leetcode.com/problems/number-of-changing-keys/description/)
- [3020. Find the Maximum Number of Elements in Subset 子集中元素的最大数量](https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/description/)
- [3021. Alice and Bob Playing Flower Game Alice 和 Bob 玩鲜花游戏](https://leetcode.com/problems/alice-and-bob-playing-flower-game/description/)
- [3022. Minimize OR of Remaining Elements Using Operations 给定操作次数内使剩余元素的或值最小](https://leetcode.com/problems/minimize-or-of-remaining-elements-using-operations/)

## 3019. Number of Changing Keys 按键变更的次数

给定一个包含大小写字母的字符串，问不考虑大小写的情况，需要更换多少次键才可以打出来。

直接都转换成大写或者小写，然后数有多少变化

```python
class Solution:
    def countKeyChanges(self, s: str) -> int:
        s = s.lower()
        result = 0
        for i in range(1, len(s)):
            if s[i - 1] != s[i]:
                result += 1
        
        return result
```

## 3020. Find the Maximum Number of Elements in Subset 子集中元素的最大数量

给定一个列表的数字，从中选择一个子集，使得这个子集可以被排列成`[x, x^2, x^4, ..., x^k/2, x^k, x^k/2, ..., x^4, x^2, x]`的一个山形数组。问这个数组中能组成的最长的山形数组的长度。

显然，这个问题存在一些动态规划的性质。我们定义`dp(x)`为我们的动态规划方程，则我们有

* 若`x`不是一个平方数，则结果为`0`。
* 若`x`是一个平方数，且`x^0.5`至少有两次，则结果为`2 + dp(x^0.5)`。
* 若`x`是一个平方数，但`x^0.5`小于两次，则不进行递归了。

最后结果需要加上`x`本身的`1`次。


```python
class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        from math import sqrt, isqrt
        
        cnt = Counter(nums)
        nums.sort()
        
        def is_square(i):
            return i == isqrt(i) ** 2
        
        from functools import cache
        
        @cache
        def dp(n):
            if n == 1:
                return cnt[1]
            if cnt[n] < 2:
                return 0
            return 2 + (dp(isqrt(n)) if is_square(n) else 0)

        
        result = 1
        for n in nums:
            if n == 1:
                result = max(result, cnt[1] if cnt[1] % 2 == 1 else cnt[1] - 1)
            elif is_square(n):
                result = max(result, 1 + dp(isqrt(n)))
                
        return result
```

## 3021. Alice and Bob Playing Flower Game Alice 和 Bob 玩鲜花游戏

假设Alice和Bob站在原点，左边有`x`朵花，右边有`y`朵花。每个回合由Alice先Bob后，选择一个方向并从这个方向取走一朵花。当一名玩家取走最后一朵花时，这名玩家获得胜利。给定`m`和`n`使得 $x \in [1, n]$，$y \in [1, m]$，问有多少种`(x, y)`的组合方式使得Alice能够赢得这场比赛。

简单推理可知，因为Alice先开始，因此当`x + y`为奇数时，Alice会胜利。而所有组合中，刚好`tot // 2`的情况为奇数。

```python
class Solution:
    def flowerGame(self, n: int, m: int) -> int:
        tot = n * m
        
        return tot // 2
```

## 3022. Minimize OR of Remaining Elements Using Operations 给定操作次数内使剩余元素的或值最小

给定长度为`n`的数组`nums`和整数`k`。每次操作，你可以选择数组中的任意两个连续数字，并对他们进行按位与(bitwise AND)操作。在进行至多`k`次操作之后，问将所有数字按位或(bitwise OR)的最小结果是多少。

针对这类位运算的题目，大多数情况来说，我们需要通过遍历每一个比特位来减少时间复杂度。基于这一点，我们可以思考按位与的性质。我们知道，若要使得最终结果最小，我们需要尽可能将每个数字的最高有效位消去。

先来考虑一个最简单的场景。若`k = n - 1`，即我们可以把所有数字都进行按位与。因此，对于每一列比特位来说，只要其中有一个`0`，最终结果中这一位就是`0`；若其中一列所有数字都为`1`，则最终结果中这一位只能是`1`。这里我们可以推导出，若某一列中的`1`的数量大于`k`，则这一列无法通过按位与消减成为`0`。

接着引入一个更复杂的场景，若`k = n - 2`，即我们只能用按位与消去`n - 1`个数字。那么，我们如何排除这个数字呢？这里我们考虑用已经有的结果进行排除。若当前数字的最后`j`位与我们期望的结果按位或仍然等于期望的结果，我们称这个数不影响结果。因此不计算在内。使用这种方法，我们就可以扫描出影响结果和不影响结果的数字，并最终筛选这一位。若这一位中影响结果的数字数量大于`k`，则我们无法消去，否则则可以消去。

```python
class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        
        n = len(nums)
        result = 0

        for j in range(31, -1, -1):
            print(j, result)
            cnt = 0
            cur = (1 << 31) - 1

            target = result | ((1 << j) - 1)
            # print("target:", format(target, "032b"))

            for i in nums:
                # print("\t", i, cur, cur & i)
                cur &= i
                if ((cur | target)) == target:
                    cnt += 1
                    cur = (1 << 31) - 1

            # add back if not possible to do it 
            # within k merges
            if n - cnt > k:
                result |= (1 << j)
            # print("final:", result)
        
        return result
```