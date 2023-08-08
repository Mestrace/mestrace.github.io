Title: Weekly Contest 356 周赛题目解析
Slug: weekly-356
Date: 2023-08-08 23:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 356 第 356 场力扣周赛 | 2798. Number of Employees Who Met the Target 满足目标工作时长的员工数目 | 2799. Count Complete Subarrays in an Array 统计完全子数组的数目 | 2800. Shortest String That Contains Three Strings 包含三个字符串的最短字符串 | 2801. Count Stepping Numbers in Range 统计范围内的步进数字数目 | Solution to contest problems 赛题讲解 | Digit DP 数位DP

[Weekly Contest 356](https://leetcode.com/contest/weekly-contest-356/)

[第 356 场周赛](https://leetcode.cn/contest/weekly-contest-356/)

## 题目列表

- [2798. Number of Employees Who Met the Target 满足目标工作时长的员工数目](https://leetcode.com/problems/number-of-employees-who-met-the-target/)
- [2799. Count Complete Subarrays in an Array 统计完全子数组的数目](https://leetcode.com/problems/count-complete-subarrays-in-an-array/)
- [2800. Shortest String That Contains Three Strings 包含三个字符串的最短字符串](https://leetcode.com/problems/shortest-string-that-contains-three-strings/)
- [2801. Count Stepping Numbers in Range 统计范围内的步进数字数目](https://leetcode.com/problems/count-stepping-numbers-in-range/)

## 2798. Number of Employees Who Met the Target 满足目标工作时长的员工数目

按照题意模拟即可。

```python
class Solution:
    def numberOfEmployeesWhoMetTarget(self, hours: List[int], target: int) -> int:
        result = 0
        for h in hours:
            if h >= target:
                result += 1
        return result
```

## 2799. Count Complete Subarrays in an Array 统计完全子数组的数目

给定正整数`nums`，若`nums`中的任意连续子数组中唯一元素的数量等于`nums`中唯一元素的数量，我们称这个子数组为完全子数组。求所有完全子数组的数量。

题目比较好理解，就是要小心暴力解法吃虫，比如我的第一个解法实际上是`O(n^3)`

```python
class Solution:
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        c = Counter(nums)
        result = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                k = Counter(nums[i:j])
                if k.keys() == c.keys():
                    result += 1
        
        return result
```

真正通过的解法为`O(n^2)`

```python
class Solution:
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        c = Counter(nums)
        result = 0
        for i in range(len(nums)):
            k = Counter()
            for j in range(i, len(nums)):
                k[nums[j]] += 1
                if len(k) == len(c):
                    result += 1
                
        
        return result
```

## 2800. Shortest String That Contains Three Strings 包含三个字符串的最短字符串

给定三个字符串`a`，`b`和`c`，需要找到长度最小且字典序最小的字符串使得这三个字符串都为结果字符串的子串。

首先我们知道，最长的结果为这三个字符串连续拼接之后最小的那个，总共有6种组合。我们来看一个例子
```
Input: a = "abc", b = "bca", c = "aaa"
Explanation:
a + b + c = "abcbcaaaa"
a + c + b = "abcaaabca"
b + a + c = "bcaabcaaa"
b + c + a = "bcaaaaabc"
c + a + b = "aaaabcbca"
c + b + a = "aaabcaabc"
```

不难得出，如果我们能够找到前后两个字符相邻的公共子串，我们就可以把这些结果进行简化。如`a + b + c = "a(bc)(a)aa"`。虽然没有办法严谨的证明，但是这已经是我们能找到的最优的结果了。即，给定这三个字符串，我们尝试把三个字符串拼接在一起，并合并前后两个字符串的子串。因为我们只有六种组合结果，我们可以暴力进行计算。

```python
class Solution:
    def minimumString(self, a: str, b: str, c: str) -> str:
        def findOverlap(a: str, b: str) -> str:
            if b in a:
                return a
            for i in range(min(len(a), len(b)), 0, -1):
                prefix = b[:i]
                if a[-len(prefix):] == prefix:
                    return a + b[i:]
            return a + b
        
        def combineStrings(a: str, b: str, c: str) -> str:
            return findOverlap(findOverlap(a, b), c)
        
        return min(
            combineStrings(a, b, c),
            combineStrings(a, c, b),
            combineStrings(b, a, c),
            combineStrings(b, c, a),
            combineStrings(c, a, b),
            combineStrings(c, b, a),
            key=lambda x: (len(x), x)
        )
```

## 2801. Count Stepping Numbers in Range 统计范围内的步进数字数目

给定两个正整数`low`和`high`，我们需要找到在`[low, high]`区间内所有的步进数字的数量。若一个数字所有相邻数位的绝对差值都为`1`，那么我们称这个数字为步进数字。举个例子，`9876`就是一个步进数字，而`8341`则不是。

先来考虑一种朴素的方法，即我们遍历`[0, high]`所有的数字，然后筛选出`> low`的数字。我们的逻辑也比较简单

* 若当前数字最后一位大于`0`，我们可以增加一位数使得新添加的这一位刚好是前一位数字减去`1`。
* 若当前数字最后一位小于`9`，我们可以增加一位数使得新添加的这一位刚好是前一位数字加上`1`。
* 若当前数字在`[low, high]`之间，则更新数量。

```python
class Solution:
    def countSteppingNumbers(self, low: str, high: str) -> int:
        MOD = 10**9 + 7
        
        from functools import lru_cache
        @lru_cache(maxsize=1000000)
        def count_stepping_numbers_util(low, high, curr_num):
            if curr_num > int(high):
                return 0

            count = 0
            if curr_num >= int(low):
                count += 1

            last_digit = curr_num % 10

            if last_digit > 0:
                count += count_stepping_numbers_util(low, high, curr_num * 10 + last_digit - 1)
            if last_digit < 9:
                count += count_stepping_numbers_util(low, high, curr_num * 10 + last_digit + 1)

            return count

        count = 0
        for i in range(1, 10):
            count += count_stepping_numbers_util(low, high, i)

        return count % MOD
```

尝试运行一下，这个解法很快就会在一个较大的输入上TLE。因此我们考虑用其他的方法。既然是使用数字递归的方式不行，我们考虑减少一下我们的状态数量，直接从每一个数位下手，这个技巧也被称之为**数位DP**。

数位DP着重于解决一类问题：给定区间`[low, high]`，要求计算每一个数位满足特定条件的数字的数量。给定输入数字`n`，定义动态规划方程为`f(i, tight, last_digit, leading_zero)`以求构造第`i`位的合法方案书，其中每个维度的含义为

* `i` 表示构造第`i`个数位，取值区间为`[0, max_digits]`，只会受到输入的最大数位长度的限制。
* `tight` 表示当前是否受到了`n`的约束，布尔值。因为我们要构造的数据的第`i`位不能超过输入的数字`n`的同样位数，所以在构造每一位数字时需要考虑是否受到约束。
* `last_digit` 表示上一位数字的值。
* `leading_zero` 表示当前已经确定的前缀数字是否含有前导零。

通过这样的动态规划方程，我们可以逐位计算满足条件的数字的数量。具体的状态转移方程根据题目条件的不同而有所调整。

在数位DP的状态转移过程中，我们需要考虑以下几种情况：

1. **当`i`到最大数位长度时**： 如果此时的数字满足特定条件，我们可以将方案数加一。
1. **当`tight = true`时**： 这意味着我们的构造受到了输入数字n的限制，因此在当前位上的数字不能大于 n 对应位上的数字。我们可以将当前位的数字从 0 遍历到 n 的对应位的数字，然后根据约束递归计算下一位。举个例子，`n = 123`，`i = 2`，`tigit = True`表明前面两位已经取了`12`，则第三位只能取`[0,3]`之间的数字。
1. **当 tight 为 false 时**： 在这种情况下，我们可以将当前位的数字从 0 遍历到 9，因为没有约束。我们同样根据递归计算下一位。还是同样的例子，`n = 123`，`i = 2`，`tigit = False`表明前两位比`12`要小，如`10`等，则第三位可以任意取`[0,9]`。
1. **根据题目的条件进行状态转移**： 这一步是数位DP的核心，根据题目中给定的条件，我们需要根据当前位的数字确定下一位数字。题目已经描述的很清楚了，这里就不再赘述了。
1. **处理前导零**： 若前缀都为`0`的话，当前位数可以为`0`，或`[1,9]`。依旧是同样的例子，`n = 123`，`i = 1`，`leading_zero = True`表明第一位是`0`，我们只需要构造`000 - 099`之间的数字。

到这里，我们的递归关系已经理清了。这里直接给答案吧。

```python
MOD = int(1e9 + 7)
class Solution:

    def _count(self, n):
        from functools import cache
        @cache
        def dp(i, tight, lastDigit, leadingZero):
            if i == len(n):
                return 1
            maxDigit = int(n[i]) if tight else 9
            result = 0
            for d in range(maxDigit + 1):
                nextTight = tight and d == maxDigit
                nextLeadingZero = leadingZero and d == 0
                if nextLeadingZero:
                    result = (result + dp(i + 1, nextTight, lastDigit, nextLeadingZero)) % MOD
                elif lastDigit == -1 or abs(lastDigit - d) == 1:
                    result = (result + dp(i + 1, nextTight, d, nextLeadingZero)) % MOD
            return result
        
        return dp(0, True, -1, True)

    def countSteppingNumbers(self, low: str, high: str) -> int:
        return (self._count(high) - self._count(str(int(low) - 1)) + MOD) % MOD
```

以下这两篇文章让我更好的理解了数位DP，感兴趣的同学可以看下。

- [USACO Guide - Digit DP](https://usaco.guide/gold/digit-dp?lang=cpp)
- [CodeForces - flash_7's blog - Digit DP](https://codeforces.com/blog/entry/53960)
