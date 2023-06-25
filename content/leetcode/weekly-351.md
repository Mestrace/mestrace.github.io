Title: Weekly Contest 351 周赛题目解析
Slug: weekly-351
Date: 2023-06-25 14:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-06 Leetcode Weekly Contest 351 第 351 场力扣周赛 | 2748. Number of Beautiful Pairs 美丽下标对的数目 | 2749. Minimum Operations to Make the Integer Zero 得到整数零需要执行的最少操作数 | 2750. Ways to Split Array Into Good Subarrays 将数组划分成若干好子数组的方式 | 2751. Robot Collisions 机器人碰撞 | Solution to contest problems 赛题讲解

[Weekly Contest 351](https://leetcode.com/contest/weekly-contest-351/)

[第 351 场周赛](https://leetcode.cn/contest/weekly-contest-351/)

欢迎来到“谁卡在第二题谁是大冤种”杯代码竞赛。

## 题目列表

- [2748. Number of Beautiful Pairs 美丽下标对的数目](https://leetcode.com/problems/number-of-beautiful-pairs/)
- [2749. Minimum Operations to Make the Integer Zero 得到整数零需要执行的最少操作数](https://leetcode.com/problems/minimum-operations-to-make-the-integer-zero/)
- [2750. Ways to Split Array Into Good Subarrays 将数组划分成若干好子数组的方式](https://leetcode.com/problems/ways-to-split-array-into-good-subarrays/)
- [2751. Robot Collisions 机器人碰撞](https://leetcode.com/problems/robot-collisions/)

## 2748. Number of Beautiful Pairs 美丽下标对的数目

这里直接用最暴力的方式遍历，并按照题意进行模拟。

```python
class Solution:
    def countBeautifulPairs(self, nums: List[int]) -> int:
        def gcd(a, b):
            if b == 0:
                return a
            return gcd(b, a % b)

        count = 0
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                first_digit = int(str(nums[i])[0])
                last_digit = int(str(nums[j])[-1])
                if gcd(first_digit, last_digit) == 1:
                    # print(i, j)
                    count += 1

        return count
```

## 2749. Minimum Operations to Make the Integer Zero 得到整数零需要执行的最少操作数

给定两个整数`nums1`和`nums2`，你可以对这`nums1`进行如下操作：选取`[0, 60]`之间的任意整数`i`，并将`nums1`减去`2^i + nums2`。求能够使`nums1`变为`0`的最小操作数量。

这道题我感觉是这次周赛里面最难的题目了。看到题目的时候完全没有思路。但我们也尝试做做看。

首先我们知道，如果只是减去`2^i`的话，那么最小操作次数就是`nums1`二进制表示的`1`的个数。因为增加了个`nums2`的的关系，我们尝试每次都减去`nums2`，并记录`i`的个数，最后查看`nums1`中`1`的个数是否等于`i`。当然这道题目不会这么简单，这个算法会在第一个例子中就失败。
```
Example 1:
Input: num1 = 3, num2 = -2
Output: 3
Explanation:
i = 1: 3 - (-2) = 5 = 0b101
i = 2: 5 - (-2) = 7 = 0b111
i = 3: 7 - (-2) = 9 = 0b1001 = 0b100 + 0b100 + 0b1
```

这里我们可以看到，虽然`9`里面只有两个`1`，但是`0b1000`可以通过两个`0b100`凑出来，因此最少是`3`次。也就是说，最终我们要找到`i >= ones(num1)`的场景。当然到这里还不能万事大吉，因为我们有一个特殊case：当`num1 = 1`且`i > 1`的时候，我们并没有办法凑出来。把这个综合一下，即当`num1 < i`的时候，我们无法拼凑了。

```python
class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        def count_one(num):
            result = 0
            while num:
                if num % 2 == 1:
                    result += 1
                num = num >> 1
            
            return result
        
        i = 0
        while count_one(num1) > i:
            num1 -= num2
            i += 1
            if num1 <= 0:
                return -1
        # print(num1, count_one(num1), i)
        if num1 >= i:
            return i
        return -1
```

## 2750. Ways to Split Array Into Good Subarrays 将数组划分成若干好子数组的方式

给定一个`01`数组`nums`，存在某种分割方式使得分割后的每个连续子数组都只有一个`1`，求有多少种分割方式。

这道题相对比较简单一点，我们直接考虑用DP来做。根据题目描述，我们可以从左到右持续的选择我们当前的子数组包含的元素或在此处分割，因此可以列出三种不同的条件：

- 当前面都是`0`的时候，我们要找到下一个`1`作为他的分割。
- 当前是`0`，且前面存在`1`的时候，我们既可以在此处分割，也可以选择把当前的`0`包含在当前子数组中。
- 当前是`1`，且前面存在`1`的时候，我们只能在此处分割。

最终当我们用完所有元素之后，若最后一个子数组也包含`1`的话，那么我们就说这是一个合法的分割，否则就是不合法的分割。

```python
class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        mod = int(1e9 + 7)
        n = len(nums)
        from functools import cache
        
        @cache
        def dp(i, one):
            # print(i, one)
            # base case
            if i == len(nums):
                return int(one)
            
            if nums[i] == 1:
                return dp(i + 1, True) % mod
            elif nums[i] == 0:
                # split here or not
                if one:
                    return (dp(i + 1, True) + dp(i + 1, False)) % mod
                else:
                    return (dp(i + 1, False)) % mod
        
        return dp(0, False) % mod
```

## 2751. Robot Collisions 机器人碰撞

给定一个列表的机器人，每个机器人有三个属性`(position, health, direction)`，分别为他们当前在一维坐标轴上的起始位置，当前血量，和前进方向(`L`左 / `R`右)。所有机器人同时以匀速从他们的起始位置沿既定方向出发。当两个机器人在同一位置时发生碰撞，则存在两种情况：若两个机器人血量相等，则两个机器人都损坏并被移除；否则血量较小的机器人被移除，而血量较大的机器人的血量减一。要求输出不再发生碰撞之后，剩余机器人的血量。

模拟题。首先对于所有机器人根据位置排序，然后我们知道当两个机器人一个往右一个往左的时候，才会发生碰撞。因此我们直接对于这种情况进行模拟，根据位置排序好后，使用一个队列记录往右前进的机器人。若遇到向左的机器人，则进行碰撞结果的计算，并最终输出结果。

提交的时候`print`没去掉还吃了一个Output Limit Exceeded的甲虫，气死。

```python
class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        # Combine positions, healths, and directions into list of robots
        robots = sorted(zip(positions, healths, directions, range(len(positions))))
        
        # print("===\n", robots)
        result = [-1] * len(positions)
        
        queue = deque()
        
        for pos, health, dire, idx in robots:
            # there is no robots to the left of this robot, therefore survive
            if dire == 'L' and not queue:
                result[idx] = health
                continue
            # moving left and there exist robot moving right
            elif dire == 'L':
                while health != -1 and queue:
                    # the right bot
                    pos2, health2, dire2, idx2 = queue.pop()
                    if health == health2:
                        health = -1
                        break
                    elif health > health2:
                        # removed the right bot
                        health -= 1
                    else:
                        # add the bot moving right back to the queue
                        queue.append((pos2, health2 - 1, dire2, idx2))
                        health = -1
                # moving left and removed all bots moving right
                if health != -1:
                    result[idx] = health
            elif dire == 'R':
                queue.append((pos, health, dire, idx))
                continue
            
            # print(queue)
        for _, health, _, idx in queue:
            result[idx] = health
        
        rresult = []
        for h in result:
            if h == -1:
                continue
            rresult.append(h)
        
        return rresult
```
