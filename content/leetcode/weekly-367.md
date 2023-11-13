Title: Weekly Contest 367 周赛题目解析
Slug: weekly-367
Date: 2023-10-15
Category: Leetcode
Tags: Contest
Summary: 2023-10 Leetcode Weekly Contest 367 第 367 场力扣周赛 | 2903. Find Indices With Index and Value Difference I 找出满足差值条件的下标 I | 2904. Shortest and Lexicographically Smallest Beautiful String 最短且字典序最小的美丽子字符串 | 2905. Find Indices With Index and Value Difference II 找出满足差值条件的下标 II | 2906. Construct Product Matrix 构造乘积矩阵 | Solution to contest problems 赛题讲解

[Weekly Contest 367](https://leetcode.com/contest/weekly-contest-367/)

[第 367 场周赛](https://leetcode.cn/contest/weekly-contest-367/)


## 题目列表

- [2903. Find Indices With Index and Value Difference I 找出满足差值条件的下标 I](https://leetcode.com/problems/find-indices-with-index-and-value-difference-i/)
- [2904. Shortest and Lexicographically Smallest Beautiful String 最短且字典序最小的美丽子字符串](https://leetcode.com/problems/shortest-and-lexicographically-smallest-beautiful-string/)
- [2905. Find Indices With Index and Value Difference II 找出满足差值条件的下标 II](https://leetcode.com/problems/find-indices-with-index-and-value-difference-ii/)
- [2906. Construct Product Matrix 构造乘积矩阵](https://leetcode.com/problems/construct-product-matrix/)

## 2903. Find Indices With Index and Value Difference I 找出满足差值条件的下标 I

给定一个整数数组`nums`，区间差值`indexDifference`，和数值差值`valueDifference`，要求找到任意一对`[i, j]`满足`abs(i - j) >= indexDifference`和`abs(nums[i] - nums[j]) >= valueDifference`两个条件。

按照题意模拟即可。

```python
class Solution:
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        n = len(nums)
        
        for i in range(n):
            for j in range(i + indexDifference, n):
                if abs(nums[i] - nums[j]) >= valueDifference:
                    return [i, j]
        
        return [-1, -1]
```

## 2904. Shortest and Lexicographically Smallest Beautiful String 最短且字典序最小的美丽子字符串

给定二进制字符串`s`和正整数`k`，要求找到字典序最短的子串使得子串中`1`的数量刚好等于`k`。

双指针记录`1`的个数。注意这里比较字典序时只有长度相等的能直接比较。

```python
class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        result = None
        
        n = len(s)
        left = 0
        cnt = 0
        for right in range(n):
            while left < right and (cnt >= k or s[left] == '0'):
                cnt -= int(s[left] == '1')
                left += 1
                
            if s[right] == '1':
                cnt += 1
            
            # print(s[left:right + 1], cnt)
            if cnt == k:
                if not result or (right - left + 1) < len(result) or ((right - left + 1) == len(result) and result > s[left:right + 1]):
                    result = s[left:right + 1]
        if not result:
            return ""
        return result
```

## 2905. Find Indices With Index and Value Difference II 找出满足差值条件的下标 II

题干跟第一题[2903. Find Indices With Index and Value Difference I 找出满足差值条件的下标 I](https://leetcode.com/problems/find-indices-with-index-and-value-difference-i/)题目一样，只是数据范围变成了`1 <= n == nums.length <= 10^5`。

每个`nums[i]`只能考虑`nums[0:i - indexDifference + 1]`里的数字进行配对。考虑到`abs(nums[i] - nums[j]) >= valueDifference`，可能会出现两种情况`nums[j] >= nums[i] + valueDifference`或者`nums[j] <= nums[i] - valueDifference`。因此我们可以考虑对于`nums[0:i - indexDifference + 1]`中的数字进行排序后二分查找。

```python
class Solution:
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        from sortedcontainers import SortedDict
        n = len(nums)
        
        d = SortedDict()
        
        for i in range(indexDifference, n):
            v = nums[i - indexDifference]
            if v not in d:
                d[v] = i - indexDifference
                
            # print("===", i, nums[i])
            target = nums[i] + valueDifference
            idx = d.bisect_left(target)
            # print(d.keys(), target, idx)
            if idx < len(d) and abs(d.peekitem(idx)[0] - nums[i]) >= valueDifference:
                return [d.peekitem(idx)[1], i]
            
            target = nums[i] - valueDifference
            idx = d.bisect_left(target)
            # print(d.keys(), target, idx)
            if idx < len(d) and abs(d.peekitem(idx)[0] - nums[i]) >= valueDifference:
                return [d.peekitem(idx)[1], i]
            if idx > 0 and abs(d.peekitem(idx - 1)[0] - nums[i]) >= valueDifference:
                return [d.peekitem(idx - 1)[1], i]

        return [-1, -1]
```

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

实际上，我们只需要关注`nums[0:i - indexDifference + 1]`中间的最大值和最小值就可以了，这样我们的算法时间复杂度可以减少为`O(n)`。

```python
class Solution:
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        n = len(nums)
        maxi = 0
        mini = 0
        for i in range(indexDifference, n):
            if nums[i - indexDifference] < nums[mini]:
                mini = i - indexDifference
            if nums[i - indexDifference] > nums[maxi]:
                maxi = i - indexDifference
            
            if nums[i] - nums[mini] >= valueDifference:
                return [mini, i]
            if nums[maxi] - nums[i] >= valueDifference:
                return [maxi, i]
        
        return [-1, -1]
```

## 2906. Construct Product Matrix 构造乘积矩阵

给定二维矩阵`grid`，构造新的矩阵使得矩阵中的每一个元素为除自身外原矩阵元素的乘积。

将矩阵打平之后，这道题跟[238. Product of Array Except Self 除自身以外数组的乘积](https://leetcode.com/problems/product-of-array-except-self/)的做法几乎一样。


```python
class Solution:
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        m, n = len(grid), len(grid[0])

        prefix = [1] * (m * n + 1)

        for i in range(m):
            for j in range(n):
                prefix[i * n + j + 1] = (prefix[i * n + j] * grid[i][j]) % 12345
        
        prefix.pop()

        suffix = [1] * (m * n + 1)

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                suffix[i * n + j] = (suffix[i * n + j + 1] * grid[i][j]) % 12345
        
        suffix.pop(0)

        # print(prefix, suffix)

        for k in range(m * n):
            i = k // n
            j = k % n
            grid[i][j] = (prefix[k] * suffix[k]) % 12345
        
        return grid
```

顺便拓展一个同余运算（modular arithmetic）的知识点。存在整数`x`使得 $ax = 1 \mod p$，可以通过模反元素（modulo multiplicative inverse）来计算`x`的值。

若`p`为质数，则可以直接使用Python内建函数`pow`（需要`python >= 3.8`）
```python
>>> pow(38, -1, mod=97)
23
>>> 23 * 38 % 97 == 1
True
```

否则的话，可以使用

```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def inverse_modulo(a, m):
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

>>> inverse_modulo(23, 97)
38
>>> 23 * 38 % 97 == 1
True
>>> inverse_modulo(23, 12345)
2147
>>> 23 * 2147 % 12345 == 1
True
```

但是要注意的是，因为`12345`不是质数，且`12345`与`129`不是同余（gcd必须为`1`），因此无法计算模反元素。

```python
>>> inverse_modulo(129, 12345)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in inverse_modulo
Exception: Modular inverse does not exist
>>> g, _, _ = extended_gcd(12345, 129)
>>> 12345 % g == 129 % g == 0, f"gcd = {g}"
(True, 'gcd = 3')
```