Title: 【Leetcode题解】2588. Count the Number of Beautiful Subarrays
Slug: 2588-count-the-number-of-beautiful-subarrays
Date: 2023-03-12
Category: Leetcode
Tags: Subarray
Summary: 2023-03 Weekly Contest 336 Leetcode 2588 Count the Number of Beautiful Subarrays 我的解题思路

每周都被周赛折磨，真是痛苦。早上刚打完周赛，趁着记忆还热乎，赶紧来写一下这题的题解。

## 题目

给定一个列表的数字`nums`, 要求求出指定符合条件的子数组数量。子数组`nums[i:j]`要满足一定条件才可以。首先我们定义一个动作，消去子数组里任意两个数的第`k`个bit（当然这两个数的`k bit`都要为`1`）。将以上动作执行无限次数之后可以子数组全部是`0`，那么我们就说子数组`nums[i:j]`为满足条件的子数组。


## 分析

这道题是2023.03.12的[周赛Weekly Contest 336](https://leetcode.com/contest/weekly-contest-336/)第三题。我一开始想的是否可以用双指针做，但是仔细想想这道题不大对劲。我们用双指针是因为找双指针指向的区域其实是一个子问题，解决了这个子问题就可以通过很简单的方式方式判断下一个问题`[left, right + 1]`是否符合[ref]双指针解法的子数组题，可以移步[【Leetcode题解】2444. Count Subarrays With Fixed Bound]({filename}/leetcode/2444-count-subarrays-with-fixed-bounds.md) [/ref]。但这一题并不能用这个方法解。我们先来看个例子

```text
Input: [4,3,1,2,4]
Output: 2
Explanation
[3] not ok
[3,1] not ok
[3,1,2] ok
[3,1,2,4] not ok
[4,3,1,2,4] ok
```

上面这个例子中我们可以看到，`[3,1,2]`和`[3,1,2,4]`并没有直接联系，因此我们不太好用双指针来解决这个问题。

那么能不能从问题本身的性质解决呢？先转换一下问题，如果我们要按照题目条件将一个子数组都变为0，意味着这个子数组的bit count每一个都要是偶数。
```text
[3,1,2]
3 = 0b11
2 = 0b10
1 = 0b01
=> {0: 2, 1: 2}
```

```text
[4,3,1,2,4]
4 = 0b100 
4 = 0b100
=> {0: 2, 1: 2, 2: 2}
```

那么，如果我们想要知道一个子数组是否满足条件，我们只需要检查他们每一比特的数量是否都为偶数；如果是的话，就可以消除了；否则的话，这个子数组就不满足条件。再往前推一步，我们并不需要知道他的count，只需要知道是否存在奇数个；如果是偶数个那就直接消掉归0就好了。*看到这里，是否觉得有点眼熟？*

<p align="center">
  <img src="{static}/images/cong-tian-er-jiang.jpg" />
</p>

对了，就是位运算里面的XOR异或操作。先简单回顾一下XOR。
```
Input  Output
A  B  A XOR B
0  0     0
0  1     1
1  0     1
1  1     0
```
基于异或操作的真值表，前人总结出来了几个性质

1. 交换律（commutative）（这个不用我多解释吧）
1. 结合律（associative）：即`(A XOR B) XOR C == A XOR (B XOR C)`
1. 单位元（Identity element）: 对于任何数X，都有`X XOR X = 0`，`X XOR 0 = x`
1. 自反性（self-inverse）：`A XOR B XOR B = A xor 0 = A`

做过[287. Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)的朋友肯定不会对这陌生。这道题目里面，我们把重复的数据都XOR一遍，剩下的那个数字就是我们要找的答案。

回到我们的2588。结合了位运算，我们可以知道：如果`XOR(nums[i:j]) == 0`，那么我们就说他是一个符合条件的子数组。想要得到这个结果的话，我们可以每次都循环XOR每一个数；或者，如果我们更聪明一点，根据上面的性质，我们有
```
  XOR(nums[i:j])
= XOR(nums[i:j]) XOR (XOR(nums[0:i]) XOR XOR(nums[0:i])) (identity element)
= XOR(nums[0:i]) XOR XOR(nums[0:j]) (associative)

which implies XOR(nums[0:i]) == XOR(nums[0:j]) (identity element)
```

根据这以上的性质，我们可以转换为`XOR(nums[0:i]) == XOR(nums[0:j])`。*看到这里，是否觉得有点眼熟？*

<p align="center">
  <img src="{static}/images/cong-tian-er-jiang.jpg" />
</p>

对了，就是可恶的prefix sum……哦不对，应该是prefix xor。所以啊，不要小瞧基础题目啊。

那么现在我们有一个异或`prefix`了。给定一个位置`j`，我们怎么找出`i < j`且`prefix[i] == prefix[j]`（我们要找的子数组）呢？ 把`[0:j)`扫过去的话是`O(n^2)`的复杂度，未免有点naive。如果我们能够把`j`之前所有的值的数都记一下……等一下，*看到这里，是否觉得有点眼熟？*

<p align="center">
  <img src="{static}/images/cong-tian-er-jiang.jpg" />
</p>

这！@#¥不就是[1. Two Sum](https://leetcode.com/problems/two-sum/)吗？用一个hashmap把之前出现的次数都记一下。假设前面有`k`个`i`的候选，其中每一个`i`都可以和我们当前的`j`组成一个符合条件的子数组结果，那么我们就把结果加上`k`，问题解决！


## 解法

这里要注意的是，一开始初始化prefix的时候我放了一个0，因为如果是`[0,i)`是空集的话，任意的`j`也可以组成一个符合条件的子数组`[0,j]`。其他的就跟我们上面说的差不多，直接梭就行。

```python
from collections import defaultdict

class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        prefix = [0]
        for i in nums:
            prefix.append(prefix[-1] ^ i)
        
        # print(prefix)
        
        m = defaultdict(lambda: 0)
        result = 0
        
        for n in prefix:
            result += m[n]
            m[n] += 1
        return result
```

## 小结

今天周赛的这一题可谓是结合了几个关键的基础知识所研发出来的新题，我称之为眼熟题。遇到这种眼熟题也没有办法，打铁还需自身硬，各位继续加油。

若果你想变得更强的话，可以做做

1. [1486. XOR Operation in an Array](https://leetcode.com/problems/xor-operation-in-an-array/)
1. [2527. Find Xor-Beauty of Array](https://leetcode.com/problems/find-xor-beauty-of-array/)
1. [2425. Bitwise XOR of All Pairings](https://leetcode.com/problems/bitwise-xor-of-all-pairings/)
1. [1707. Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)

-----