Title: 【Leetcode题解】Weekly Contest 338 周赛题目解析
Slug: weekly-338
Date: 2023-03-27
Category: Leetcode
Tags: Contest
Summary: 2023-03 Leetcode Weekly Contest 338 | 2600. K Items With the Maximum Sum K 件物品的最大和 | 2601. Prime Subtraction Operation 质数减法运算 | 2602. Minimum Operations to Make All Array Elements Equal 使数组元素全部相等的最少操作次数 | 2603. Collect Coins in a Tree 收集树中金币| My solution 我的题目解析

这次的周赛我鸽子了，结果就刚好错过了大闹剧：Leetcode全球站崩了，有的小伙伴们20分钟才能开始做题。估计这次分数会作废吧。这次的题目难度稍微比前几周的题目要难一些，主要是结合了多个知识。如果不熟练的话，就比较容易出错。此外，例如第二题和第三题，也有很多恶心的边缘条件需要一些技巧才能解决。

## 题目列表


1. [Easy - 2600. K Items With the Maximum Sum](https://leetcode.com/problems/k-items-with-the-maximum-sum/)
1. [Medium - 2601. Prime Subtraction Operation](https://leetcode.com/problems/prime-subtraction-operation/)
1. [Medium - 2602. Minimum Operations to Make All Array Elements Equal](https://leetcode.com/problems/minimum-operations-to-make-all-array-elements-equal/)
1. [Hard - 2603. Collect Coins in a Tree](https://leetcode.com/problems/collect-coins-in-a-tree/)


## 2600. K Items With the Maximum Sum K 件物品的最大和

第一题相当trival，贪心的尽可能的统计最多的1和0即可。

### 代码
```python
class Solution:
    def kItemsWithMaximumSum(self, numOnes: int, numZeros: int, numNegOnes: int, k: int) -> int:
        if numOnes >= k:
            return k
        
        if numOnes + numZeros >= k:
            return numOnes
        
        return numOnes - (k - numOnes - numZeros)
```

## 2601. Prime Subtraction Operation 质数减法运算

给定一个`nums`列表，我们可以对这个数组进行一项操作任意多次。这项操作为：选定数组其中的数字`nums[i]`，并将`nums[i]`减去任意一个小于`nums[i]`的质数。我们至多只能对每个`nums[i]`进行一次这样的操作。我们想要知道，对于数组进行任意次数的操作之后，`nums`是否可以变成一个严格递增的数组。

这道题还是类似贪心的思路。如果我们要让数组变成严格递增的话，我们要把其中的每一个数字变得尽可能的小。小到让这个数字刚好大于之前的那个数字。这样我们才有可能拼出来一个符合题目描述的严格递增数组。

题目的数据范围显示`1 <= nums[i] <= 1000`，为了简洁，我们这里直接打一个1000以内质数的表。题目要求我们构造一个严格递增的数组，可以采用局部的方式去解决，定义为对于所有`i`，`nums[i - 1] < nums[i]`。因此我们只需要检查局部的大小即可。

根据上面我们的分析，在`i`的时候，我们要找到一个质数`primes[j]`，使得`nums[i] - primes[j] < nums[i - 1]`。这里我们分两步解决，第一步先找到刚好小于`nums[i]`的质数，第二步再找另一个质数使得我们上述条件成立。然后我们就重复这个过程。如果我们能够让每个数字都满足刚刚的局部条件的话，我们就说我们可以通过题目要求的条件找到一个严格递增的数组；如果我们在之间完全找不到一个质数是的`nums[i] - primes[j] < nums[i-1]`的话，那么我们就说这个数组无法通过条件检测。

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

如果你想要你的算法跑得更快的话，也可以用二分的方式去扫对应的质数。

### 代码

```python
from bisect import bisect_left

class Solution:
    def primeSubOperation(self, nums: List[int]) -> bool:
        primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009]

        largest = 0

        def find_prime(x, right):
            for i in range(right, -1, -1):
                if x - primes[i] > largest:
                    return i, True
            return right, False


        for i, n in enumerate(nums):
            right = bisect_left(primes, n)

            print(i, n, right)

            if right > 0:
                loc, found = find_prime(n, right)
                # print("\t", found, primes[loc], largest, nums[i])
                if found:
                    nums[i] -= primes[loc]
            largest = nums[i]

            if i > 0 and nums[i - 1] >= nums[i]:
                return False

        return True

```

## 2602. Minimum Operations to Make All Array Elements Equal 使数组元素全部相等的最少操作次数

给定一个数组`num`和一个数组`queries`，我们想要知道要多少个`+1/-1`操作才能使`nums`里每一个数字都和`queries[i[i]`相等。题目也说了，每次查询后数组`nums`都会被重置为其原始状态。

先从最简单的方法开始：我们可以循环查询这个数组，去看`nums[i]`和`q`的差异，并将它们汇总起来。既然我们要进行汇总的话，是不是有更好的方式可以求解呢？

给定一个查询`q`我们可以把数组`nums`分为左右两半部分，其中左边部分`< q`，右边部分`>= q`。这样的话，我们需要对左边所有的数字使用`+1`操作，右边所有的数字使用`-1`操作才能得到满足条件的数组。这样是不是看起来有点像`prefix sum`了。

对于这道题来说，我们可以先将`nums`进行排序，在先求一个`prefix`和`suffix`前缀和和后缀和。对于索引`i`来说，`prefix[i] = sum(nums[:i])` 和 `suffix[i] = sum(nums[i:])`。所以每一个`q`的答案就是`q * i - prefix[i]`和`suffix[i] - q * (n - i)`的和。

而怎么找到`i`呢？我们刚刚不是把`nums`排序了嘛。要找到`nums[i] < q`的话，二分一下就好了。

### 代码

```python
from bisect import bisect_left

class Solution:
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()

        prefix = [0] * (len(nums) + 1)
        prefix[1] = nums[0]
        for i in range(1, len(nums)):
            prefix[i + 1] = prefix[i] + nums[i]
        
        suffix = [0] * (len(nums) + 1)
        suffix[-2] = nums[-1]
        for i in range(len(nums) - 2, -1, -1):
            suffix[i] = suffix[i + 1] + nums[i]
        
        # print(prefix)
        # print(suffix)

        result = [0] * len(queries)

        for i, q in enumerate(queries):
            idx = bisect_left(nums, q)
            # print(nums[:idx], q*idx, prefix[idx])
            # print(nums[idx:], q * (len(nums) - idx), suffix[idx])
            result[i] = (q * idx - prefix[idx]) + (suffix[idx] - q * (len(nums) - idx))
        
        return result
```

## 2603. Collect Coins in a Tree 收集树中金币| My solution 我的题目解析

给定一个无向，无根的树（undirected, unrooted tree）（其实就是一个DAG），其中有一些节点散落着一些硬逼。我们能收集两步以内的硬币。问最少需要几步才能收集所有硬币。起始点可以选择任意节点。

坦白讲，第四题我看到的时候也没什么思路。借鉴了[@ye15的解法](https://leetcode.com/problems/collect-coins-in-a-tree/solutions/3342036/c-java-python3-trim-the-tree/)才明白里面的玄机。

这道题目的解决方法相当巧妙。可以将树分为三部分：无硬币的子树、有硬币的节点和有硬币的子树。

第一步，将无硬币的子树剪枝。我们想要在最短步数内收集硬币的话，我们必不能走到一个没有硬币的子树里面去。

第二步，从有硬币的叶子节点开始，将有硬币的子树向上剪枝两层层，同时收集被剪掉的叶子节点。这步操作直接与题目中要求的能够在2步内收集硬币的限制相关。

最后，剩下的边组成了必须通过的边，如果路径上还有硬币，我们也可以一起收集。

### 代码

```python
class Solution:
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)
        tree = defaultdict(set)
        for u, v in edges:
            tree[u].add(v)
            tree[v].add(u)
        
        print(tree)

        leaf = deque()
        for u in range(n):
            while len(tree[u]) == 1 and not coins[u]:
                v = tree[u].pop()
                tree[v].remove(u)
                u = v
            if len(tree[u]) == 1:
                leaf.append(u)
        
        print(leaf)
        print(tree)

        for _ in range(2):
            for _ in range(len(leaf)):
                u = leaf.popleft()
                if tree[u]:
                    v = tree[u].pop()
                    tree[v].remove(u)
                    if len(tree[v]) == 1:
                        leaf.append(v)
            print(leaf)
            print(tree)

        return sum(len(tree[u]) for u in range(n))
```

## 小结

这次的题目难度较高，此外场外因素也限制了大多数人的发挥，没做好的同学也不要气馁，我们下周再见。

如果你想变得更强的话，可以做做

1. [Medium - 2584. Split the Array to Make Coprime Products](https://leetcode.com/problems/split-the-array-to-make-coprime-products/)（[我的题解]({filename}/leetcode/2584-split-the-array-to-make-coprime-products.md)）
1. [Medium - 2587. Rearrange Array to Maximize Prefix Score](https://leetcode.com/problems/rearrange-array-to-maximize-prefix-score/)
1. [Medium - 462. Minimum Moves to Equal Array Elements II](https://leetcode.com/problems/minimum-moves-to-equal-array-elements-ii/)
1. [Medium - 834. Sum of Distances in Tree](https://leetcode.com/problems/sum-of-distances-in-tree/)