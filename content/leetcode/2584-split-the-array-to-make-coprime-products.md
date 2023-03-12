Title: 【Leetcode题解】2584. Split the Array to Make Coprime Products
Slug: 2584-split-the-array-to-make-coprime-products
Date: 2023-03-08
Category: Leetcode
Tags: Leetcode

又闲的无聊，找点事情做，来写一下[2584. Split the Array to Make Coprime Products](https://leetcode.com/problems/split-the-array-to-make-coprime-products/)的题解。

## 题目

You are given a 0-indexed integer array `nums` of length `n`.

A split at an index i where `0 <= i <= n - 2` is called valid if the product of the first `i + 1` elements and the product of the remaining elements are coprime.

For example, if `nums = [2, 3, 3]`, then a split at the index `i = 0` is valid because `2` and `9` are coprime, while a split at the index `i = 1` is not valid because `6` and `3` are not coprime. A split at the index `i = 2` is not valid because `i == n - 1`.
Return the smallest index `i` at which the array can be split validly or `-1` if there is no such split.

Two values `val1` and `val2` are coprime if `gcd(val1, val2) == 1` where `gcd(val1, val2)` is the greatest common divisor of `val1` and `val2`.

给一个列表的数字，把这个列表分为两半，使得两边的乘积互质(coprime)。当然啦，要找那个使得左边最小的。

## 分析

这道题是2023.03.05的[周赛](https://leetcode.com/contest/weekly-contest-335/)第三题。刚看到题目的时候我心想：“呵，简单！prefix sum(product)可破。”现在想想自己还是图样图森破了。首先要注意的是那个乘积，一看到n个数需要乘起来就需要立马联想到数字越界的问题。对于Python的盲目相信让我冲昏了头脑，用了各种魔改的prefix sum去试。比如先把数字预处理一遍，去除他们的乘数。当然事实证明我并没有办法解决这个问题。

我第二个思路是图的思路。因为我们要把这个数组分为两个集合。如果两个数`gcd(a,b) != 1`的话那么他们必定在同一个集合里面。那么，我们要先用`gcd`构建他们的图…… 诶等一下，如果我要把每两个数字对比一遍找`gcd`的话，时间复杂度好像是`O(n^2)`…… 当然，你肯定猜到结局了，愚蠢的我用了这个方法且TLE了。

最后，我光荣的成为了一名两题选手 ：）

不说伤心事儿了。解决这题，首先需要注意的就是互质的性质。对于互质的两个数`a`和`b`来说，`b`的所有质因数都不是`a`的因数。我们知道，每一个正整数都可以表示成一些质数的乘积。
进一步思考，如果我们能够对每个数字进行质数分解，那么对于左右两边进行质数分解之后，就可以通过对比两遍的质数来检查两边是否互质了。

当然这样还不够，因为找一个给定数字的质数也是一个不小的活儿。这里随便偷一段代码。
```Python
import math
 
# A function to print all prime factors of
# a given number n
def prime_factors(n):
    # Print the number of two's that divide n
    while n % 2 == 0:
        print 2,
        n = n / 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3,int(math.sqrt(n))+1,2):

        # while i divides n , print i and divide n
        while n % i== 0:
            print i,
            n = n / i
             
    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        print n
```
可以看到，这个naive的方法是这么计算的：给定数字`n`，循环[[2,√n]次去除这个数，如果能整除就说明n是这个数字的一个质因数，直到这个数字为1为止。因为我们的值域是`1 <= nums[i] <= 10^6`，所以每个数字要循环`10^3`次。哎，不得行不得行…… 等下，如果我们知道取值范围的话，那么直接打表不就好了！

```Python
def prime_factors(n):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    factors = []
    i = 0
    while i < len(primes) and primes[i] * primes[i] <= n:
        if n % primes[i] == 0:
            factors.append(primes[i])
            n //= primes[i]
        else:
            i += 1
    if n > 1:
        factors.append(n)
    return factors
```

这里我们直接搞个小于1000的质数表。然后一直尝试整除这些质数就好。这样就把我们的复杂度大大降低了。当然这个算法对于超过1000的质数也是有用的，因为最后如果n还是不为1的话，那么剩下那个数还是他的质因数。因为我们知道取值范围不可能出现超过两个 > 1000的指数，以最接近1000的两个为例，`1009 * 1013 = 1,022,117`，而`1009 * 991 = 999,919`。这个算法能保证在这个情况下我们是安全的。

那么剩下的就简单了。回到我们的算法，从左到右，每次比较左右两边的质因数的交集就可以解决了。

## 解法

贴上剩余部分的代码。我们维护`left`和`right`两边的prime然后算交集。每次循环我们都给`left`的质数数上，`right`的质数扣掉，再比较他们两个的`key`的交集就可以了。

```Python
from collections import defaultdict

class Solution:
    def findValidSplit(self, nums: List[int]) -> int:
        left = defaultdict(int)
        right = defaultdict(int)
        
        def inc(m, l):
            for n in l:
                m[n] += 1
            
        def dec(m, l):
            for n in l:
                m[n] -= 1
                if m[n] == 0:
                    del m[n]


        inc(left, prime_factors(nums[0]))
        for i in range(1, len(nums)):
            inc(right, prime_factors(nums[i]))
        
        # print(left)
        # print(right)
        
        i = 0
        while i < len(nums) - 1:
            # print(left, right)
            if not (left.keys() & right.keys()):
                return i
            dec(right, prime_factors(nums[i + 1]))
            inc(left, prime_factors(nums[i + 1]))
            i += 1
        
        return -1
```

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>


如果你看到这里了，再告诉你一点加强版的方案。

实际上，left是一直在增加没有减少，所以我们也不需要维护left的count了，直接一个set然后每次取并集就可以了。这样可以减少一点内存消耗和一丢丢时间复杂度。


<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

实际上我们把大部分数字的质因数都求了两遍，因此如果我们能消耗一些内存把每个数字的质因数都保存下来的话，这样就会把常数部分的时间减少一半以上。

用Python的朋友一定熟悉我们的好朋友`functools.cache`。直接给我们的`prime_factors`方法带上小帽子，实测有接近50%的速度提升（2801ms vs. 5300ms），而代价则是5MB的内存消耗（21.2MB vs. 16.2MB）。


<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

在这个方法里面，我们已经遍历了每一个数字的质因数。所以我们还是可以用类似图的方式去找。对于每一个质因数，如果我们知道他最早和最晚出现在数组的哪一个位置，那么我们就可以通过这样的方式去把这个数组一分为二了。
```
Input: nums = [4,7,8,15,3,5]
Output: 2
Explanation:
  [4,7,8,15,3,5]
2  -----|
3       |----
5       |------
7    -  |
```
在上面这个例子里面，横线为每个质因数的区间，而竖线就是他的分界线。我们可以追着这个索引找到最左边的分界线，就是我们的结果了。想要参考代码的可以看看[v神的题解](https://leetcode.com/problems/split-the-array-to-make-coprime-products/solutions/3258070/prime-intervals-vs-count-primes/?orderBy=most_votes)，这里就不多赘述了。

又及：这个做法其实跟一天前的[双周赛](https://leetcode.com/contest/biweekly-contest-99)的第三题[2580. Count Ways to Group Overlapping Ranges](https://leetcode.com/problems/count-ways-to-group-overlapping-ranges/description/)的思路非常相似了。难怪讨论区里的人都说周赛和双周赛的出题人是同一个呢……

## 拓展

如果你想变得更强的话，可以延伸看看

1. [Primes and GCD](https://www.cs.sfu.ca/~ggbaker/zju/math/primes.html)
1. [欧拉函数](https://maochong.xin/posts/euler_totient.html)
1. [理解黎曼猜想（二）两个自然数互质的概率是多少？|袁岚峰](https://zhuanlan.zhihu.com/p/47978393)
