Title: 【Leetcode题解】Weekly Contest 337 周赛题目解析
Slug: weekly-337
Date: 2023-03-19
Category: Leetcode
Tags: Contest
Summary: 2023-03 Leetcode Weekly Contest 337 | 2595. Number of Even and Odd Bits | 2596. Check Knight Tour Configuration | 2597. The Number of Beautiful Subsets | 2598. Smallest Missing Non-negative Integer After Operations | My solution 我的题目解析


今天的周赛[Weekly Contest 337](https://leetcode.com/contest/weekly-contest-337/)难度也比较适中。而且令我没想到的是最后一题竟然是Medium。个人在做的时候感觉第三题比第四题的思考过程要难得多，可能是我个人的错觉。此外，跟之前一天的双周赛[Biweekly Contest 100](https://leetcode.com/contest/biweekly-contest-100/)（[我的题解]({filename}/leetcode/biweekly-100.md)）一样，题目也做了反GPT处理。出题人花了20买的这个GPT会员可真值，让无数英雄折腰啊。好了，不说废话了，看看今天的题目吧。

## 题目列表

1. [Easy - 2595. Number of Even and Odd Bits](https://leetcode.com/problems/number-of-even-and-odd-bits/)
1. [Medium - 2596. Check Knight Tour Configuration](https://leetcode.com/problems/check-knight-tour-configuration/)
1. [Medium - 2597. The Number of Beautiful Subsets](https://leetcode.com/problems/the-number-of-beautiful-subsets/)
1. [Medium - 2598. Smallest Missing Non-negative Integer After Operations](https://leetcode.com/problems/smallest-missing-non-negative-integer-after-operations/)

## 2595. Number of Even and Odd Bits 奇数和偶数比特位的数量

一个正整数n，统计这个正整数里面的even bit和odd bit数量。比如`17 = 0b10001`，奇数bit为0，偶数bit为第`0`和`4` bit。

### 分析

无论如何，要把一个数转换为他的比特表示才能做。常规方法肯定是直接位运算用`n & 1ek` 取第`k`位的比特值。这里为了手速，直接变成`string`并倒着遍历。

### 代码
```python
class Solution:
    def evenOddBit(self, n: int) -> List[int]:
        s = "{0:b}".format(n)
        
        # print(s)
        even = 0
        odd = 0
        for i in range(len(s)):
            idx = len(s) - 1 - i
            if s[idx] != '1':
                continue
            if i % 2 == 0:
                even += 1
            else:
                odd += 1
        return [even, odd]
```

## 2596. Check Knight Tour Configuration 棋盘设置是否正确

给定一个`n x n`矩阵，矩阵里一定有`[0, n*n-1]`的每个数字。这里每个数字代表棋子走的顺序。比如`[0,0] = 0` 和 `[1,1] = 1`就是说棋子会从`[0,0] -> [1,1]`。而我们的棋子是个马 (knight)，只能走日字。

> 国际象棋中的马（Knight）是一种走法比较特殊的棋子，它每次走动可以横跨2格并且向垂直或水平方向移动1格，或者横跨1格并且向垂直或水平方向移动2格。马的行走轨迹形状类似于“日”字。
> 
> 如果当前位置为(x, y)，那么它可以移动到以下8个位置中的任意一个：
> 
> (x + 2, y + 1)
> 
> (x + 2, y - 1)
> 
> (x - 2, y + 1)
> 
> (x - 2, y - 1)
> 
> (x + 1, y + 2)
> 
> (x + 1, y - 2)
> 
> (x - 1, y + 2)
> 
> (x - 1, y - 2)
> 
> ---- by chatgpt

给定这个棋盘，我们判断从`[0,n*n - 1]`的每一步是否合法。<u>棋子从[0,0]开始</u>。

### 分析

我们可以遍历整个棋盘，并反向把第`k`步映射到`[i,j]`上。然后我们遍历`[0, n*n-1]`去确认`k-1`到`k`步是否合法。判断走法也相对简单，`[x1,y1] -> [x2,y2]`是合法的一步，当且仅当（iff），`x1 - x2`的绝对值和`y1 - y2`的绝对值分别为`2`和`1` 或者`1`和`2`。

需要注意这题比较坑的点是<u>棋子从[0,0]开始</u>这个条件也是作为一个测试用例的，不是定义给定的棋盘的！如果你想我一样眼神不好，肯定会在这里卡很久。

### 代码
```python
class Solution:
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        
        n = len(grid)
        sz = n * n
        
        mapp = dict()
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                mapp[v] = [i, j]
        
        
        curr = mapp[0] # start with zero
        
        if curr != [0,0]:
            return False
        
        for step in range(1, sz):
            nxt = mapp[step]
            
            # print(step, curr, nxt,  ((abs(curr[0] - nxt[0]) == 1 and abs(curr[1] - nxt[1]) == 2)
            # or (abs(curr[0] - nxt[0]) == 2 and abs(curr[1] - nxt[1]) == 1)))
            
            if ((abs(curr[0] - nxt[0]) == 1 and abs(curr[1] - nxt[1]) == 2)
            or (abs(curr[0] - nxt[0]) == 2 and abs(curr[1] - nxt[1]) == 1)):
                curr = nxt
                continue
            
            return False

        return True
```

## 2597. The Number of Beautiful Subsets 美丽非空子集的个数 

给定一个数组`nums`和正整数`k`，我们定义`nums`的一个子集`subs`是一个美丽子集，如果`subs`里所有元素两两配对的差值都不等于`k`。我们需要求出这种子数组的总数。

限制条件：

- 1 <= nums.length <= 20
- 1 <= nums[i], k <= 1000

### 分析

首先，我们知道一个数组的非空子集有`2^n-1`个。如果暴力做的话很快就会命中时间上界，所以这种题目看题要仔细。我们注意到数组长度最多为`20`，那么`2^20`的递归次数，还是有暴力的空间的。只是在一些特殊case上处理下。

这里我们采用bt暴力求解，每次我们包含`nums[i:]`的时候，我们遍历整个数组并每次都尝试包含其中的数`j`，同时我们维护一个列表是无法包含的数字去排除掉一些其中的数字。

一个需要处理的特殊case：数组里如果没有任何等差 = k的序列，那么所有的非空子集就是答案。


### 代码
```python
class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        nums.sort()
        
        m = defaultdict(set)
        
        sz = len(nums)
        
        for i in range(sz):
            for j in range(i + 1, sz):
                if nums[j] - nums[i] == k:
                    m[nums[i]].add(nums[j])
                    m[nums[j]].add(nums[i])
        if len(m) == 0:
            return pow(2, sz) - 1
        
        result = 0
        def bt(i, cant):
            nonlocal result
            result += 1
            for j in range(i, len(nums)):
                if nums[j] in cant:
                    continue
                    
                cant_nums = m[nums[j]]
                
                cant.extend(cant_nums)
                bt(j + 1, cant)
                
                for cn in cant_nums:
                    cant.remove(cn)
        bt(0, [])
        return result - 1
```
## 2598. Smallest Missing Non-negative Integer After Operations 找到数组中最小缺失的整数

给定一个数组`nums`和一个整数`value`，我们定义变换为：将其中一个数字`k`加上或者减去`value`。我们可以对数组中的任意数字做任意次数的变换，形成一个新的数组。对于这个变换后数组来说，我们想要找到他的`MEX`（minimum excluded）：
> 一个数组的MEX（最小排除值）是指其中最小的未出现的非负整数。
> 
> ---- by chatgpt

用人话讲就是从`0`开始累加找，找到最小的那个不存在于这个数组里的数。

### 分析

一看到加减某个数，我们应该很快联想到取模这个操作。取模的性质为若`x + n * value = b`，则`x % value = b % value`。因此，如果我们想确认`k`是否能被数组里的`nums[i]`得到，我们应该找`k % value == nums[i] % value`的数字。这样的话，我们就做贪心的匹配就好了，从`k = 0`开始，我们一个个确认否能通过变换得到`k`；如果能通过变换得到，那么就把数组里的对应的数移除；如果不行的话，那个数就是答案。

与此同时，我们也发现参数定义是`1 <= nums.length, value <= 10^5`。所以极端情况下，结果就是`10^5 + 1`。

### 代码
```python
class Solution:
    def findSmallestInteger(self, nums: List[int], value: int) -> int:
        mapp = defaultdict(int)
        for n in nums:
            mapp[n % value] += 1
        
        for i in range(int(1e5 + 1)):
            modi = i % value
            if mapp[modi] == 0:
                return i
            mapp[modi] -= 1
        
        return int(1e5 + 1)
```

## 小结

如果你想变得更强的话，可以做做

1. [Easy - 1295. Find Numbers with Even Number of Digits](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/)
1. [Easy - 268. Missing Number](https://leetcode.com/problems/missing-number/)
1. [Medium - 1197. Minimum Knight Moves](https://leetcode.com/problems/minimum-knight-moves/)
1. [Medium - 688. Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/)
1. [Medium - 1718. Construct the Lexicographically Largest Valid Sequence](https://leetcode.com/problems/construct-the-lexicographically-largest-valid-sequence/)
1. [Hard - 41. First Missing Positive](https://leetcode.com/problems/first-missing-positive/)