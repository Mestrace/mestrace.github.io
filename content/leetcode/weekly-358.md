Title: Weekly Contest 358 周赛题目解析
Slug: weekly-358
Date: 2023-08-30 00:38:00
Category: Leetcode
Tags: Contest
Summary: 2023-08 Leetcode Weekly Contest 358 第 358 场力扣周赛 | 2815. Max Pair Sum in an Array 数组中的最大数对和 | 2816. Double a Number Represented as a Linked List 翻倍以链表形式表示的数字 | 2817. Minimum Absolute Difference Between Elements With Constraint 限制条件下元素之间的最小绝对差 | 2818. Apply Operations to Maximize Score 操作使得分最大 | Solution to contest problems 赛题讲解

[Weekly Contest 358](https://leetcode.com/contest/weekly-contest-358/)

[第 358 场周赛](https://leetcode.cn/contest/weekly-contest-358/)

## 题目列表

- [2815. Max Pair Sum in an Array 数组中的最大数对和](https://leetcode.com/problems/max-pair-sum-in-an-array/)
- [2816. Double a Number Represented as a Linked List 翻倍以链表形式表示的数字](https://leetcode.com/problems/double-a-number-represented-as-a-linked-list/)
- [2817. Minimum Absolute Difference Between Elements With Constraint 限制条件下元素之间的最小绝对差](https://leetcode.com/problems/minimum-absolute-difference-between-elements-with-constraint/)
- [2818. Apply Operations to Maximize Score 操作使得分最大](https://leetcode.com/problems/apply-operations-to-maximize-score/)

## 2815. Max Pair Sum in an Array 数组中的最大数对和

按照题意模拟即可。

```python
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        e = defaultdict(list)
        
        for n in nums:
            d = max(str(n))
            
            e[d].append(n)
        
        result = -1
        for l in e.values():
            if len(l) <= 1:
                continue
            l.sort()
            
            result = max(result, sum(l[-2:]))
        
        return result
```

## 2816. Double a Number Represented as a Linked List 翻倍以链表形式表示的数字

给定一个链表表示的数字`n`，返回同样用链表表示的`n * 2`。

如果设计过加法器的同学应该知道公式`d = (a + b + cin) % z`且`cout = (a + b + cin) // z`，从低位到高位两位两位相加，把前一个的`cout`变成下一位的`cin`。

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def doubleIt(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        def recur(node):
            if node is None:
                return 0, None
            cin, rest = recur(node.next)
            
            val = node.val * 2 + cin
            
            node.next = rest
            
            node.val = val % 10
            
            return val // 10, node
        
        cout, head = recur(head)
        
        while cout > 0:
            head = ListNode(cout % 10, head)
            cout = cout // 10
        
        return head
```

## 2817. Minimum Absolute Difference Between Elements With Constraint 限制条件下元素之间的最小绝对差

给定一个数字列表`nums`和一个整数`x`，在将任意两个数字`num[i]`和`nums[j]`两两配对之后，找到满足`abs(i - j) >= x`且最小的`abs(nums[i] - nums[j])`值。

先思考一个朴素的解法，对于每一个`nums[i]`，我们都遍历区间`[i + x, len(nums) - 1]`的`nums[j]`。这样我们的时间复杂为`O(n^2)`。

```python
class Solution:
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        n = len(nums)
        min_diff = float('inf')
        
        for i in range(n):
            for j in range(i + x, n):
                diff = abs(nums[i] - nums[j])
                min_diff = min(min_diff, diff)
        
        return min_diff
```

我们可以从问题的性质入手降低`O(n^2)`的时间复杂度。首先，从上面的算法中，我们可以明确地知道，对于一个`nums[i]`，所有可能的候选的数字都在区间`[i + x, len(nums) - 1]`中。对于我们的绝对值`abs`来说，不能太大也不能太小，刚好是中间的那个数最好。因此我们可以考虑排序。排序完成之后使用二分法找中间的数字即可。此外，我们是顺序便利的，因此对于前面已经排好序的数组来说，我们可以很容易添加一个新的数字进去。这里我们采用树形结构实现的排序结构，则每次插入为`O(log(n))`。

```python
from sortedcontainers import SortedList

class Solution:
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        s = SortedList()

        result = int(1e9 + 1)
        for i in range(len(nums) - 1, -1, -1):
            s.add(nums[i])

            l = i - x
            if l < 0:
                break

            idx1 = s.bisect_right(nums[l]) - 1
            if idx1 >= 0 and idx1 < len(s):
                result = min(result, abs(nums[l] - s[idx1]))
            idx2 = s.bisect_right(nums[l])
            if idx2 < len(s):
                result = min(result, abs(nums[l] - s[idx2]))
            
            # print(nums[l], s, idx1, idx2)
            
        return result
```

## 2818. Apply Operations to Maximize Score 操作使得分最大

给定一个长度为`n`的正整数列表`nums`和一个整数`k`，一开始你的分数为`1`，你需要通过一系列操作来最大化你的分数。你可以使用以下操作最多`k`次：在一个从未选择过的区间`[l:r]`中，选择其中质因数最多的元素`x`（最大化的**质因数分数**），并把你的分数翻`x`倍。求你最多可以获得多少分。

对于这种结构的记分，我们很快就可以观察出，每次取最大的元素肯定是最优的。这就构成了贪心算法的基础：`我们可以通过做出局部最优来构造全局最优`。但首先，我们要解决几个问题：

1. 给定任意一个元素，我们需要知道这个元素能够被使用多少次。
1. 给定任意一个元素，我们需要知道这个元素的质因数分数，即这个元素有多少个质因数。
1. 给定任意一个元素，我们需要知道这个元素的幂与先前分数相乘，再模`1e9+7`的结果。

第一个问题我们如何理解呢？这里题目描述的可能会比较有歧义，因此我们在这里再解释一下。题目的意思是说任意索引`[l:r]`的组合都可以被使用一次，而不是当前区间只能被使用一次。假设我有`b,c,a,d,e`，且`a`是质因数分数最大的数字，那么`a`可以被使用的次数就是`a`可以被包含在内的子数组的数量总和，这里是`9`种组合。一个朴素的方法是给当前元素，顺序遍历左边和右边的质因数分数值，直到当前元素的质因数分数不是最大为止。

第二个问题稍微比较简单。由于我们处理的是`1e5`以下的数字，因此我们只需要准备一个质数表就可以了。质数表需要多大呢，这里我直接给答案：因为`313 * 313 = 97969`，所以我们只需要准备`2`到`313`之间的`65`个质数就可以了，接着用朴素的方法算出来，并做记忆化保存，因为我们会多次重复计算。

第三个问题就更简单了。二分即可。即`p^n = (p * p) ^ (n / 2)`。

那么我们直接就可以来看一下代码实现。

```python
from functools import cache

class Solution:
    mod = 1000000007
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
            127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
            193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
            269, 271, 277, 281, 283, 293, 307, 311, 313]
    
    @cache
    def prime_score(self, n):
        score = 0
        val = n
        for i in range(65):
            if n >= self.primes[i] and val % self.primes[i] == 0:
                score += 1
                while val % self.primes[i] == 0:
                    val //= self.primes[i]
        return score + (val > 1)

    def mod_pow(self, x, y, m):
        if y == 0:
            return 1
        p = self.mod_pow(x, y // 2, m) % m
        p = (p * p) % m
        return p * x % m if y % 2 else p

    def maximumScore(self, nums: List[int], k: int) -> int:
        idx = list(range(len(nums)))
        idx.sort(key = lambda i: nums[i])
        result = 1
        while idx and k > 0:
            i = idx.pop()

            left = 0
            for j in range(i - 1, -1, -1):
                if self.prime_score(nums[i]) <= self.prime_score(nums[j]):
                    break
                left += 1
            
            right = 0
            for j in range(i + 1, len(nums)):
                if self.prime_score(nums[i]) < self.prime_score(nums[j]):
                    break
                right += 1
            
            take = min(k, (left + 1) * (right + 1))

            result = (result * self.mod_pow(nums[i], take, self.mod)) % self.mod
            
            k -= take
        
        return result
```

啪的一下，很快嘛！等一下，怎么TLE了！我的算法啊……

最耗时的部分应该很明显了，计算左边和右边的元素个数的循环就是。这样让我们的时间复杂度去到了`O(n^2)`。然而，我们可以采取一些优化措施来改进这一点。看起来，预先计算左右两侧的元素个数是一个可行的优化方法。在这个优化过程中，我们将会利用两个关键特性：1）题目中规定区间内的质因数分数最多不会超过`7`，2）我们只关心离当前元素最近的元素。

假设我们想要确定在当前位置左侧有多少个连续元素的质因数分数较小，我们首先计算那些具有较高质因数分数的左侧元素中最大元素的索引。然后，我们将这个最大索引从当前位置的索引中减去，从而得到了我们所需的连续元素数量。通过这个方法，我们可以逐步地叠加计算每个新元素所贡献的数量。需要注意的是，因为质因数分数仅为`[1,7]`，所以这个计算操作的时间复杂度为`O(n)`。对于右侧我们也使用相同的方式，只是遍历的时候变为从右到左遍历。

```python
class Solution:
    # same as above

    def maximumScore(self, nums, k):
        res = 1
        sz = len(nums)
        ids = list(range(sz))
        l = [-1] * sz
        r = [sz] * sz
        score_l = [-1] * 8
        score_r = [sz] * 8

        for i in range(sz):
            score = self.prime_score(nums[i])
            l[i] = max(score_l[score:])
            score_l[score] = i

        for i in range(sz - 1, -1, -1):
            score = self.prime_score(nums[i])
            r[i] = min(score_r[score + 1:])
            score_r[score] = i

        ids.sort(key=lambda i: nums[i])
        while ids and k > 0:
            i = ids.pop()
            take = min(k, (i - l[i]) * (r[i] - i))
            res = res * self.mod_pow(nums[i], take, self.mod) % self.mod
            k -= take

        return res
```
