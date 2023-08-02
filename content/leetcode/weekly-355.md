Title: Weekly Contest 355 周赛题目解析
Slug: weekly-355
Date: 2023-08-02 21:00:00
Category: Leetcode
Tags: Contest
Summary: 2023-07 Leetcode Weekly Contest 355 第 355 场力扣周赛 | 2788. Split Strings by Separator 按分隔符拆分字符串 | 2789. Largest Element in an Array after Merge Operations 合并后数组中的最大元素 | 2790. Maximum Number of Groups With Increasing Length 长度递增组的最大数目 | 2791. Count Paths That Can Form a Palindrome in a Tree 树中可以形成回文的路径数 | Solution to contest problems 赛题讲解 | Palindome 回文

[Weekly Contest 355](https://leetcode.com/contest/weekly-contest-355/)

[第 355 场周赛](https://leetcode.cn/contest/weekly-contest-355/)

后两题真是怪的不像话。。。

## 题目列表

- [2788. Split Strings by Separator 按分隔符拆分字符串](https://leetcode.com/problems/split-strings-by-separator/)
- [2789. Largest Element in an Array after Merge Operations 合并后数组中的最大元素](https://leetcode.com/problems/largest-element-in-an-array-after-merge-operations/)
- [2790. Maximum Number of Groups With Increasing Length 长度递增组的最大数目](https://leetcode.com/problems/maximum-number-of-groups-with-increasing-length/)
- [2791. Count Paths That Can Form a Palindrome in a Tree 树中可以形成回文的路径数](https://leetcode.com/problems/count-paths-that-can-form-a-palindrome-in-a-tree/description/)

## 2788. Split Strings by Separator 按分隔符拆分字符串

按照题意模拟即可。

```python
class Solution:
    def splitWordsBySeparator(self, words: List[str], separator: str) -> List[str]:
        result = []
        for w in words:
            s = w.split(separator)
            # print(s)
            for v in s:
                if len(v) > 0:
                    result.append(v)
        return result
```

## 2789. Largest Element in an Array after Merge Operations 合并后数组中的最大元素

给定`nums`数组，若`nums[i] <= nums[i + 1]`，你可以移除`nums[i]`并使`nums[i + 1] += nums[i]`。求完全合并之后数组中数字的最大值。

我们可以从右到左进行合并，这样我们当前的值总是期望的最大值，若左边值比较小，就可以继续加，否则从左边值开始继续往左加。

```python
class Solution:
    def maxArrayValue(self, nums: List[int]) -> int:
        for i in range(len(nums) - 1, 0, -1):
            if nums[i] >= nums[i - 1]:
                nums[i - 1] = nums[i] + nums[i - 1]
        return max(nums)
```

## 2790. Maximum Number of Groups With Increasing Length 长度递增组的最大数目

给定一个长度为`n`的整数数组`usageLimits`，其中每一个数字`usageLimits[i]`代表了`i`的最大使用频率。我们需要用`[0,n-1]`的数组来组成不同的数字组，其中每个数字组都是唯一的数字，且所有数字组中每个数字`i`被使用的次数不超过`usageLimits[i]`。此外，我们形成的数字组在除了满足其他的条件外，每个新的数字组的长度一定要大于所有之前的数字组的长度。最终要求我们计算最多能形成多少个组。

首先，我们先来考虑一种朴素的解法。我们每次都从频率最大数字开始构造，这样我们才能尽可能满足每个数组里面数字是唯一的。我们首先对于频率进行排序，接着构造数字组：第一个数字组包含频率最高的一个，第二个数字组包含频率最高的前两个，以此类推。一直贪心的使用频率最高的数字，直到我们无法再组成新的数字组为止。因为我们并不关心每个数字组里的具体组成数字，可以直接使用频率进行替代即可。这里我们使用一个堆来找最大的数值。

```python
class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        from heapq import heapify, heappush, heappop

        h = [-x for x in usageLimits]
        heapify(h)

        sz = 0
        while sz <= len(h):
            y = []

            for i in range(sz):
                v = -heappop(h)
                if v > 1:
                    y.append(v - 1)
            
            for v in y:
                heappush(h, -v)
            sz += 1
        
        return sz - 1
```

对于这个算法，我们有一个`O(n^2)`的循环，每个循环要执行`log(n)`的`pop`和`push`操作，因此这个算法的时间复杂度为`O(n^2 log(n))`。对于这道题`10^5`次方的输入长度，这样的解法是一定会超时的。那么，有没有更好的解法呢？我们先来看一个例子

```
Example 1
Input: [1,2,3,4]
Output: 4
Explanation:
Iteration 1 - [1]: [0]
Iteration 2 - [1,2]: [0,1], [1]
Iteration 3 - [1,2,3]: [0,1,2], [1,2], [2]
Iteration 4 - [1,2,3,4]: [0,1,2,3], [1,2,3], [2,3], [3]
```

我们使用这种逐步添加每一个数字的频率来表示每一步的演变。在这里，我们构造了一个完美的例子，即刚好使用完所有的数字。我们可以看到，给定这个数字列表，我们最多能够用`n * (n + 1)`个数字来形成`n`个数字组。再来看一个复杂点的例子。

```
Example 2
Input: [1, 1, 1, 10, 12]
Output:
Explanation:
Iteration 1 - [1]: [0]
Iteration 2 - [1,1]: [0]
Iteration 3 - [1,1,1]: [1,2], [0]
Iteration 4 - [1,1,1,10]: [1,2,3], [0,3], [3]
Iteration 5 - [1,1,1,10,12]: [1,2,3,4], [0,3,4], [3,4], [4]
```

在第二轮的时候，我们添加了一个`1`，但是因为不满足长度条件，不能形成新的数字组。而在第四轮的时候，我们添加了十个`3`，但是因为不满足唯一条件，我们只用到了三个`3`。

有的同学可能会说了，你用到的例子的频率都是已经排好序的了呀，要是测试用例给了个没排序的怎么办呢？我来解释一下，这里用到的例子都是用于方便展示的，实际上哪个频率对应哪个数字并不管见，因此我们总可以对于数组进行排序以构造类似的场景。

那么我们来描述一下我们的算法。首先我们维护两个数字：`total`代表当前看到的频率和，`count`代表我们当前有多少个数字组。我们首先对于频率数组进行排序，并进行循环，每次累加当前看到的频率到`total`，则我们有两种情况：

1. 若`total < (count * (count + 1)) / 2`的话，代表说新加进来的数字没法组成新的数据组
2. 若`total >= (count * (count + 1)) / 2`的话，代表新加进来的数字至少是上一次的数据组的个数 + 1，可以给每个数据组分配一个，因此`count += 1`。


```python
class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        usageLimits.sort()

        total, count = 0, 1
        for i in range(len(usageLimits)):
            total += usageLimits[i]
            if total >= (count * (count + 1)) // 2:
                count += 1
        
        return count - 1
```

## 2791. Count Paths That Can Form a Palindrome in a Tree 树中可以形成回文的路径数

以父节点的形式给定一棵树`parent`，其中`0`为根节点，其他节点`i`与`parent[i]`连接。这棵树中每条边代表了一个字母，以字符串`s`的形式给出。其中，`s[0]`可以忽略，`s[1]`则为`1 - parent[1]`的节点代表的字母，以此类推。问这颗树中存在多少路径的字母可以重新组合成回文串。

来回顾一下回文串的性质：一个字符串`s`中最多存在一种奇数个的字符，而其他字符全是偶数个，我们则说这个`s`可以被重新组合成回文字符串，如`aa`，`aba`。这道题没有要求我们求出实际的回文字符串，因而可以用这个性质进行化简。我们只需要关注每个字符的个数是奇数还是偶数即可。考虑到本题只会出现`26`个小写字母，我们可以用一个整形数字`bitmask`来储存路径上的字符是奇数还是偶数。

<p align="center">
  <img src="{static}/images/confused.jpeg" />
</p>

在这个树中，给定两个节点`u`和`v`，我们可以这样思考来求出上述描述中的`mask`
```
freq(u - v) = freq(root - u) + freq(root - v) - 2 * freq(root - lca(u, v))
```
其中，`lca`代表的是最近公共祖先。由于只有奇数个数的字母才会对结果有影响，所以后面的`2 * freq(root - lca(u, v))`可以直接被忽略。因此，这样我们就能很容易求出上面的奇数`mask`，直接使用`dfs`把每一条路径上的字母`xor`当前的`mask`即可。

在我们有了每一条路径的`mask`之后，我们可以来思考如何数存在的回文路径。假设当前`mask`代表了`root - u`路径，另一条路径`root - v`上的`mask'`需要满足以下条件才可以跟`root - u`组成符合条件的回文路径：

1. `mask' = mask`，即两条路径上奇数个的字符完全抵消。一种特例就是另一条路径上的字符完全相等。
2. `mask' = mask ^ a`，即两条路径上奇数个的字符完全抵消，且`mask'`存在一个`a`可以放在中间，
3. `mask' = mask ^ b`
4. `mask' = mask ^ c`
5. ... 以此类推

这样，我们就可以用类似 [2sum](https://leetcode.com/problems/two-sum/) 的方式顺序求之前的路径数量和了。

```python
class Solution:
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        from functools import cache
        @cache
        def dp(i):
            if i == 0:
                return 0
            
            return dp(parent[i]) ^ (1 << (ord(s[i]) - ord('a')))

        count = Counter()

        result = 0

        for i in range(len(parent)):
            v = dp(i)
            # mirrored part + 
            result += count[v] + sum(count[v ^ (1 << j)] for j in range(26))
            count[v] += 1
            # print(i, v, count, result)

        return result
```
