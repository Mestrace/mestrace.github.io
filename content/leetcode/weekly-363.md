Title: Weekly Contest 363 周赛题目解析
Slug: weekly-363
Date: 2023-09-23
Category: Leetcode
Tags: Contest
Summary: 2023-09 Leetcode Weekly Contest 363 第 363 场力扣周赛 | 2859. Sum of Values at Indices With K Set Bits 计算 K 置位下标对应元素的和 | 2860. Happy Students 让所有学生保持开心的分组方法数 | 2861. Maximum Number of Alloys 最大合金数 | 2862. Maximum Element-Sum of a Complete Subset of Indices 完全子集的最大元素和 | Solution to contest problems 赛题讲解

[Weekly Contest 363](https://leetcode.com/contest/weekly-contest-363/)

[第 363 场周赛](https://leetcode.cn/contest/weekly-contest-363/)


## 题目列表

- [2859. Sum of Values at Indices With K Set Bits 计算 K 置位下标对应元素的和](https://leetcode.com/problems/sum-of-values-at-indices-with-k-set-bits/)
- [2860. Happy Students 让所有学生保持开心的分组方法数](https://leetcode.com/problems/happy-students/)
- [2861. Maximum Number of Alloys 最大合金数](https://leetcode.com/problems/maximum-number-of-alloys/)
- [2862. Maximum Element-Sum of a Complete Subset of Indices 完全子集的最大元素和](https://leetcode.com/problems/string-transformation/)

## 2859. Sum of Values at Indices With K Set Bits 计算 K 置位下标对应元素的和

按照题意，直接使用`bin`转换或者使用位运算都可以。

```python
class Solution:
    def sumIndicesWithKSetBits(self, nums: List[int], k: int) -> int:
        result = 0
        for i, n in enumerate(nums):
            b = bin(i)[2:]
            c = 0
            for d in b:
                if d == '1':
                    c += 1
                if c > k:
                    break
            # print(n, b, c)
            if c == k:
                result += n
        return result
```

## 2860. Happy Students 让所有学生保持开心的分组方法数

给定`n`位学生，每个学生都有一个开心分数，老师需要把在学生中挑选一组学生。让一个学生开心有两种条件：若一位学生被选中，且选中的总人数大于这个学生的开心分数；或学生未被选中，且选中的总人数小于这个学生的开心分数。问有多少种选择学生的方法使得所有人都开心。

因为我们不关心选中学生的索引，因此直接排序，则存在三种情况：

* 若选择`k = 0`位学生，则需要满足`k < nums[0]`才能让所有学生开心。
* 若选择`1 <= k < n`位学生，则需要满足`nums[k - 1] < k < nums[k]`才能让所有学生开心。
* 若选择`k = n`为学生，则需要满足`nums[n - 1] < k`才能让所有学生开心。

因此，有了条件之后就可以直接开写，不过要注意中间的条件，小心越界。

```python
# [0, 2, 3, 3, 6, 6, 7, 7]
#  1  2  3  4  5  6  7  8
class Solution:
    def countWays(self, nums: List[int]) -> int:
        nums.sort()
        # print(nums)
        result = int(nums[0] > 0)
        # print(0, result)
        for selected in range(1, len(nums)):
            if selected > nums[selected - 1] and selected < nums[selected]:
                result += 1
            # print(selected, result)
        else:
            if len(nums) > nums[-1]:
                result += 1
            # print(len(nums), result)
        
        return result
```

## 2861. Maximum Number of Alloys 最大合金数

在一家合金加工厂，我们用`n`种原料制造一种合金。总共有`k`台机器可以用，但是每台机器制造同一种合金的所需原料数量不一致，因此我们有`composition[i] = [c_1, c_2, ..., c_n]`代表了第`i`台机器所需原料。此外，我们还有`stock = [s_1, s_2, ..., s_n]`代表了当前的材料库存，`cost = [v_1, v_2, ..., v_n]`代表了额外购买每种材料的价格，以及`budget`代表我们的花费预算。我们要从`k`台机器中选出一台能在`budget`内生产最多合金产品的机器，并输出最多生产多少台产品。

题目真的是又臭又长。刚看到的时候还以为是一道背包（Knapsack）问题。仔细一看，只需要选择一台机器。因此，我们的问题就变成了在给定`budget`之内求出每台机器最多能生产多少合金产品。从性质可以观察出，我们可以顺序判断机器`i`是否可以生产`num`个产品。通过`num`，我们可以轻松计算出需要多少个`j`个材料。若库存足够，则不需要花钱；反之则需要以`v_j`的价格购买`c_i_j - s_j`个产品，并借此来判断预算是否足够。假设我们知道我们计划生产多少个产品`num`，我们就可以快速判断，且这个判断是连续的：如果我们能够生产`num`个产品，那么我们一定能生产`num - 1`个产品；如果我们不能在给定预算内生产`num`个产品，我们一定不能生产`num + 1`个产品。因此，这道题可以通过二分的方式求解。二分是一个相对成熟的模版，这里就不展开说了。我们只需要遍历每一台机器，通过二分法找到最大可以生产多少个合金，最后输出最大值。

```python
class Solution:
    def maxNumberOfAlloys(self, n: int, k: int, budget: int, composition: List[List[int]], stock: List[int], cost: List[int]) -> int:
        # check if machine i can create num alloys within budget
        def check_machine(i, num):
            # amount
            spent = 0
            for j in range(n):
                will_consume = composition[i][j] * num
                
                if will_consume <= stock[j]:
                    continue
                    
                spent += (will_consume - stock[j]) * cost[j]
                
                if spent > budget:
                    break
            return spent <= budget
        
        # max alloys
        result = 0
        
        for machine_id in range(k):
            left = 0
            right = int(1e9)
            
            while left <= right:
                mid = left + (right - left) // 2
                
                if check_machine(machine_id, mid):
                    result = max(result, mid)
                    left = mid + 1
                else:
                    right = mid - 1
            
            # result = max(result, left)
            # print("machine", machine_id, left, right)
        return result
```

## 2862. Maximum Element-Sum of a Complete Subset of Indices 完全子集的最大元素和

定义一个完全集为其中所有的元素每对两两相乘的乘积都为平方数字。给定一个长度为`n`的一维数组`nums`，我们想要找到这个数组的索引集合`{1,..,n}`中的完全子集中数值和最大的一个，并返回数值和。

什么意思呢？给定`nums = [5,6,7,8]`, 索引集合`{1,4}`是一个完全集，因为`1 * 4 = 4 = 2^2` 则对应的数值和为`nums[0] + nums[3] = 5 + 8 = 13`。

再多看几个例子吧。我们可以观察到以下几种情况

* 任何平方数与`1`组成的集合都是完全集，如`{1, 4}`，`{1, 9, 16}`。
* 质因数组成部分可以重组为两个平方数的，如`{3, 27}`，`{6, 24, 54}`。

看起来似乎不是非常困难。考虑到问题给了`10^4`的数组长度，我们需要考虑一些简单的办法。先来回忆一下我们是如何对任意自然数`n`做质因数分解的。可以从除数`v = 2`开始遍历，直到除数`v^2 > n`为止。以下是一段例程：
```python
while n > 1 and v * v <= n:
    while n % v == 0:
        factors.append(v)
        n //= v
    v += 1
```

那么，质因数分解的这个例子对我们有什么帮助呢？在上面的例子中，我们可以看到，任何平方数两两相乘都能组成平方集合，而非平方数，我们可以改写成为一个或多个平方数乘一个非平方数。取前面的例子，我们进行一下分解
```
index = {6, 24, 54}
6 = 6 * 1
24 = 3 * 2 * 2 * 2 = 6 * (2 ^ 2)
54 = 2 * 3 * 3 * 3 = 6 * (3 ^ 2)
Then
6 * 24 = (6 ^ 2) * (2 ^ 2) = 12 ^ 2
6 * 54 = (6 ^ 2) * (3 ^ 2) = 18 ^ 2
24 * 54 = (6 ^ 2) * (2 ^ 2) * (3 ^ 2) = 36 ^ 2
```

到这里我们就找出了他的规律。我们可以对于任意一个索引进行**平方数分解**以求的它的非平方数基。而非平方数基的两个数字相乘则可以可以成为一个平方数。

```python
class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        count = Counter()
        for i in range(len(nums)):
            x, v = i + 1, 2
            while x >= v * v:
                while x % (v * v) == 0:
                    x //= v * v
                v += 1
            count[x] += nums[i]
        return max(count.values())
```