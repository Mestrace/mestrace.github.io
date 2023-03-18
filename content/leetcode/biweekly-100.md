Title: 【Leetcode题解】Biweekly Contest 100 双周赛题目解析
Slug: biweekly-100
Date: 2023-03-18
Category: Leetcode
Tags: Contest
Summary: 2023-03 Leetcode Biweekly Contest 100 | 2591. Distribute Money to Maximum Children | 2592. Maximize Greatness of an Array | 2593. Find Score of an Array After Marking All Elements | 2594. Minimum Time to Repair Cars | My solution 我的题目解析


最近双周赛的难度都比较适中。今天的[Biweekly Contest 100](https://leetcode.com/contest/biweekly-contest-100/)尤其离谱。第四题竟然是Medium。第一题由于题目太过拗口竟然出现了10%的提交AC率。恰逢这周GPT-4发布，我一开始还担心会不会是机器人大战。但是我多虑了，在每一题都做了反GPT处理，直接扔进去只会给你一个离谱到姥姥家的结果 ---- 出题人，真有你的。当然这也可能是为什么第一题题目那么难读的原因，心疼卡在那里提交了很多次的同学们。

没发挥好的同学们也不要气馁，我们一起过一下这次双周赛。

## 题目列表

- [Easy - 2591. Distribute Money to Maximum Children](https://leetcode.com/problems/distribute-money-to-maximum-children/)
- [Medium - 2592. Maximize Greatness of an Array](https://leetcode.com/problems/maximize-greatness-of-an-array/)
- [Medium - 2593. Find Score of an Array After Marking All Elements](https://leetcode.com/problems/find-score-of-an-array-after-marking-all-elements/)
- [Medium - 2594. Minimum Time to Repair Cars](https://leetcode.com/problems/minimum-time-to-repair-cars/)

## 2591. Distribute Money to Maximum Children 给小朋友分最多的钱

给定`money`金钱数量(in dollar)和`children`小朋友数量，根据下列规则，把钱分给这些小朋友

1. 所有钱都必须分配出去，不能有剩余。
1. 每个人至少有`1`美元
1. 没有人拿到`4`美元

我们需要找到一种分配方式使得所有小朋友中拿到刚好`8`美元的小朋友数量最多。如果这样的分配方法不存在的话，返回`-1`

### 分析

快速阅览题目，可以简单给出几个规则

- 不能分配的情况：当`money = 4, child = 1`的时候，违反规则。但是在其他部分的时候，我们总是可以分配，因为我们可以通过给其他人分配去避免。第一个例子就是这种情况，虽然`[8,8,4]`可以拿到最多的`8`，但是违背了规则，所以挪一下变成`[8,9,3]`就可以了。
- `money < child * 8`的情况：期望尽量的拿到更多的`8`，但是要避免让最后一个人拿到`4`
- `money == child * 8`的情况：就刚好所有小孩都拿到了`8`。
- `money > child * 8`的情况：`child - 1`能拿到`8`，因为我们把剩下的美元都给了最后一个人。

### 代码

```python
class Solution:
    def distMoney(self, money: int, children: int) -> int:
        # at least somebody will receive less than 1 dollar
        if money < children:
            return -1
        # if someone gets 4
        if children == 1 and money == 4:
            return -1
        
        # everyone gets at least 1
        money -= children
        rc = children
        
        for c in range(children - 1):
            if money < 7:
                break
            money -= 7
            rc -= 1
       
        if rc == 1 and money == 3:
            return children - rc - 1
        elif rc == 1 and money == 7:
            return children
        return children - rc
```


## 2592. Maximize Greatness of an Array 最伟大的数组

给定一个数组`nums`，我们可以有任意种方式把里面的元素重新排列为一个新的数组`perm`。题目定义了个Greateness，就是`perm[i] > nums[i]`的元素个数。我们需要找到一种可能的`perm`使得这个greateness最大，并返回这个值。

### 分析

因为我们想要尽可能的匹配更多，所以对于每个`nums[i]`我们都要尝试找到刚好比他大的数字。一开始想的是，排序之后移位一个对比。但是这样并找不到最优解。那么只能谈心的去拿了。排序之后直接对比，如果匹配上就丢弃这个元素，并匹配下一个。

### 代码

这里用了最大堆去匹配，当然也可以排序，这个就交给读者自己处理了。

```python
from heapq import heapify, heappop

class Solution:
    def maximizeGreatness(self, nums: List[int]) -> int:
        perm = [-n for n in nums]
        nums = list(perm)
        
        heapify(nums)
        heapify(perm)
        
        # pop the max since it is not possible to match anyway
        heappop(nums)
        
        result = 0
        sz = len(nums)
        for _ in range(sz):
            p = -perm[0]
            n = -heappop(nums)
            if p > n:
                result += 1
                heappop(perm)
        
        return result
```

## 2593. Find Score of an Array After Marking All Elements 标记所有元素来算分

给定一个数组`nums`，一开始我们有分数`score = 0`, 并且我们要对数组进行如下操作

- 选取并**标记**未被标记的最小的元素`i`，如果有多个元素一样，则选择数组下标最小的。
- 增加分数`score += nums[i]`
- **标记**`i`左右两边的元素（如果存在的话）
- 重复直到所有元素都被标记

### 分析

直接排序之后按照题目描述进行模拟就可以。

### 代码

这里我们直接把数组下标根据原数组里的元素大小进行排序，并定义**标记**为`nums[i] == -1`。

```python
class Solution:
    def findScore(self, nums: List[int]) -> int:
        # sort idx based on the smallest one
        idx = list(range(len(nums)))
        idx.sort(key = lambda i: nums[i])
        
        # print(idx)
        
        score = 0
        for i in idx:
            # marked
            if nums[i] == -1:
                continue
            score += nums[i]
            nums[i] = -1
            if i - 1 >= 0:
                nums[i - 1] = -1
            if i + 1 < len(nums):
                nums[i + 1] = -1
        
        return score
```


## 2594. Minimum Time to Repair Cars 找到最短的修车时间

我们有一个列表的修车师傅，其中他们修车的参数`rank`是一个列表。假如我让师傅`i`去修`x`辆车，那么他修这么些车所需要的时间为`rank[i] * x^2`分钟。我们还有`cars`辆车。我们需要找到最少需要多少时间去修好所有车。每个师傅可以并行的修所有分配给他们的车。

### 分析

这题乍一看是个二次优化，写成优化的形式就是
```text
minimize x^T * rank * x 
s.t. I * x = cars (summation of x equals cars)
```
当然可以用数值方式求解，但是题目里肯定不会要求这样，因此我们想想别的办法。

对于这个题目，我们可以观察到，题目要求的结果最小的分钟数`minute`，如果我们给了比他多的时间永远都可以修成功，而比他少的时间永远都不可以修完所有车。即`minute`刚好是可以修和不可以修的分界线。我们当然可以遍历从`0`到正无穷，每个时间都检查下是否能够修。但是更简便的方法是二分搜索，题目也刚好符合这个结构。

那么我们需要知道怎么检测是否可以修。给定一个分钟数`minutes`，我们想知道是否可以修。这里我们贪心的把所有车都给rank小的人去修，直到我们没有车可以修为止。这样就可以尽量快的检测了。

### 代码


```python
from math import sqrt

class Solution:
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # print("===")
        ranks.sort()
        
        def canRepair(minutes):
            total_fixed = 0
            for i, rank in enumerate(ranks):
                # print(minutes, i, rank, "fixed", int(sqrt(minutes / rank)))
                total_fixed += int(sqrt(minutes / rank))
                if total_fixed >= cars:
                    return True
            
            return False
        
        # print(canRepair(16))
        
        left = 0
        right = (ranks[-1] + 1) * cars * cars
        
        while left < right:
            mid = left + (right - left) // 2
            
            if canRepair(mid):
                right = mid
            else:
                left = mid + 1
        
        return right
```

## 小结

如果你想变得更强的话，可以做做

1. [Easy - 2558. Take Gifts From the Richest Pile](https://leetcode.com/problems/take-gifts-from-the-richest-pile/description/)
1. [Medium - 1387. Sort Integers by The Power Value](https://leetcode.com/problems/sort-integers-by-the-power-value/submissions/)
1. [Medium - 875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/)
1. [Medium - 2410. Maximum Matching of Players With Trainers](https://leetcode.com/problems/maximum-matching-of-players-with-trainers/)
1. [Hard - 2589. Minimum Time to Complete All Tasks](https://leetcode.com/problems/minimum-time-to-complete-all-tasks/) （[我的题解]({filename}/leetcode/2589-minimum-time-to-complete-all-tasks.md)）


