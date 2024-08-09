Title: Weekly Contest 407 周赛题目解析
Slug: weekly-407
Date: 2024-08-08 13:11
Category: Leetcode
Tags: Contest
Summary: 2024-07 Leetcode Weekly Contest 407 第 407 场力扣周赛 | Solution to contest problems 赛题讲解

[Weekly Contest 407](https://leetcode.com/contest/weekly-contest-407/)

[第 407 场周赛](https://leetcode.cn/contest/weekly-contest-407/)


## 题目列表

- [3226. Number of Bit Changes to Make Two Integers Equal 使两个整数相等的位更改次数](https://leetcode.com/problems/number-of-bit-changes-to-make-two-integers-equal/)
- [3227. Vowels Game in a String 字符串元音游戏](https://leetcode.com/problems/vowels-game-in-a-string/)
- [3228. Maximum Number of Operations to Move Ones to the End 将 1 移动到末尾的最大操作次数](https://leetcode.com/problems/maximum-number-of-operations-to-move-ones-to-the-end/)
- [3229. Minimum Operations to Make Array Equal to Target 使数组等于目标数组所需的最少操作次数](https://leetcode.com/problems/minimum-operations-to-make-array-equal-to-target/)


## 3226. Number of Bit Changes to Make Two Integers Equal 使两个整数相等的位更改次数

给定两个整数`n`和`k`，你可以把`n`的任意一位从`1`变到`0`，问将`n`变为`k`的最小变换次数是多少。如果无法变换，则返回`-1`。

比较基础的位运算题目，先看区间为`10^6`，直接用位移判断是否相等或者可以变换。

```python
class Solution:
    def minChanges(self, n: int, k: int) -> int:
        def bitof(v, i):
            return ((v >> i) & 1)

        result = 0
        for i in range(32):
            nb = bitof(n, i)
            kb = bitof(k, i)

            if nb == kb:
                continue
            elif nb == 1 and kb == 0:
                result += 1
            else:
                return -1
        
        return result
```

## 3227. Vowels Game in a String 字符串元音游戏

爱丽丝和鲍勃正在玩一个游戏，给定一个小写字母字符串`s`，爱丽丝每回合可以从`s`中移除奇数个原音，鲍勃则可以移除偶数个元音。两人轮流进行回合，直到元音字符皆被移除，此时最后一个移除的人获得胜利。若两人都以最优的方式进行游戏，要求返回一个布尔值表明爱丽丝是否会赢。爱丽丝永远先进行游戏。

这里我们可以看出，只要`s`中至少有一个元音，爱丽丝永远可以进行移除最大的奇数个数，此时剩余元音个数要么为`0`要么为`1`，鲍勃无法进行移除，因此算输。直接数元音个数，然后进行简单判断即可。 

```python
class Solution:
    def doesAliceWin(self, s: str) -> bool:
        VOWELS = list('aeiou')

        vowel_count = sum(int(c in VOWELS) for c in s)

        print(vowel_count)

        if vowel_count == 0:
            return False
        
        return True
```

## 3228. Maximum Number of Operations to Move Ones to the End 将 1 移动到末尾的最大操作次数

给定二进制字符串`s`，你可以将`s[i] = 1`与右边的`s[i + 1] = 0`进行交换。你可以进行这个操作任意多次，问至多可以进行多少次操作。

这题的关键点要求最大次数。先来思考一下，如果我们要移动最少次数，那么我们肯定会选择优先移动靠右的元素，这样子一次操作的话，左边的元素会跳过更多的`0`直接来到右边。因此，反向思考的话，我们可以得出，一点一点的从左边开始将元素往右边移动，是求最大次数的关键。

当然，我们肯定不能一个一个的去看，这样时间复杂度较慢。我们倾向于一次处理一排`1`。这一题的设计刚好如此。假设`s[0:i]`之间有`k`个元素，且位置`i`之前所有的`1`都已经移动到了最佳位置，当`s[i + 1] == 0`时，我们最大可以移动`k`次。基于动态规划的思想，我们可以令`dp[i]` 为索引 `s[0:i]`包含的`1`移动到最佳位置的最大次数，则我们可以基于前面的结果，以及当前`1`的数量，来快速计算最大需要多少次的操作。

```python
class Solution:
    def maxOperations(self, s: str) -> int:
        ipos = [idx for idx in range(len(s)) if s[idx] == '1']

        if len(ipos) == 0:
            return 0

        if ipos[-1] != len(s) - 1:
            ipos.append(len(s))

        memo = [0] * len(ipos)

        for i in range(1, len(ipos)):
            if ipos[i] - 1 == ipos[i - 1]:
                memo[i] = memo[i - 1]
            else:
                memo[i] = memo[i - 1] + i
            
            # print(i, memo[i])

        return memo[-1]
```

## 3229. Minimum Operations to Make Array Equal to Target 使数组等于目标数组所需的最少操作次数

给两个定数组`nums`和`target`，在单次操作中，你可以将任意`nums`中的连续子数组的所有数字增加或者减少`1`。你可以操作任意多次，使得`nums`恰好为`target`，问最少需要需要多少次。

当然要从两个数组之间的区别开始。令数组`diff`为`target`和`nums`中元素两两相减之差，我们就能找到可以连续操作的最长的子数组，并且批量对他们进行操作。但这样真的解决了问题吗？当你遇到`diff = [-1, 2, -2]`的时候应该怎么抉择呢？程序可不会做这样的抉择。

实际上，这道题的性质与总变差（total variation）有关。先来看一个简单的例子。我们有`nums = [1, 3, 3, 2, 3, 3]`和`target = [4, 4, 4, 4, 4, 4]`，则两者的差值为`diff = [3, 1, 1, 2, 1, 1]`。为了方便进行计算，我们在两端加上`0`，则有`diff_new = [0, 3, 1, 1, 2, 1, 1, 0]`。将`diff_new`中的前后元素进行差分，我们有`var = [3, -2, 0, 1, -1, 0, -1]`。其中的正值相加，则是这道题的答案`4`。

当我们计算出一个序列的差分数组后，再进一步计算相邻元素之间的差异，其中正差值代表了每次转换时所需的增加量。将这些正差值相加，实际上就是计算了从原始数组转换为目标数组时，最少需要多少次操作。这个和反映了在转换过程中所需要的最小“工作量”。


```python
class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        n = len(nums)
        incr, decr, ops = 0, 0, 0

        for i in range(n):
            diff = target[i] - nums[i]

            if diff > 0:
                if incr < diff:
                    ops += diff - incr
                    # print(f"{i}: diff is {diff}, incr is {incr}, additional {diff - incr} ops needed.")
                incr = diff
                decr = 0
            elif diff < 0:
                if diff < decr:
                    ops += decr - diff
                    # print(f"{i}: diff is {diff}, decr is {decr}, additional {diff - decr} ops needed.")

                decr = diff
                incr = 0
            else:
                incr = decr = 0

        return ops
```

另一种方式是求全变差的绝对值总和之后除以`2`。

```python
class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:

        diffs = [0] + list(map(sub, target, nums)) + [0]

        return sum(abs(x-y) for x, y in pairwise(diffs))//2
```

