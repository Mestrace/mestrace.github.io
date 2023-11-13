Title: Weekly Contest 371 周赛题目解析
Slug: weekly-371
Date: 2023-11-13 22:00
Category: Leetcode
Tags: Contest
Summary: 2023-11 Leetcode Weekly Contest 371 第 371 场力扣周赛 | 2932. Maximum Strong Pair XOR I 找出强数对的最大异或值 I | 2933. High-Access Employees 高访问员工 | 2934. Minimum Operations to Maximize Last Elements in Arrays 最大化数组末位元素的最少操作次数 | 2935. Maximum Strong Pair XOR II 找出强数对的最大异或值 II | Solution to contest problems 赛题讲解 | Trie 前缀树 | Greedy 贪心算法

[Weekly Contest 371](https://leetcode.com/contest/weekly-contest-371/)

[第 371 场周赛](https://leetcode.cn/contest/weekly-contest-371/)

两周没做了，复健一下。

## 题目列表

- [2932. Maximum Strong Pair XOR I 找出强数对的最大异或值 I](https://leetcode.com/problems/maximum-strong-pair-xor-i/)
- [2933. High-Access Employees 高访问员工](https://leetcode.com/problems/high-access-employees/)
- [2934. Minimum Operations to Maximize Last Elements in Arrays 最大化数组末位元素的最少操作次数](https://leetcode.com/problems/minimum-operations-to-maximize-last-elements-in-arrays/)
- [2935. Maximum Strong Pair XOR II 找出强数对的最大异或值 II](https://leetcode.com/problems/maximum-strong-pair-xor-ii/)

## 2932. Maximum Strong Pair XOR I 找出强数对的最大异或值 I

给定整数列表`nums`，找到满足`|x - y| <= min(x, y)`的数字对的异或值，并返回最大的异或值。

按照题意模拟即可。

```python
class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        result = 0
        for i in nums:
            for j in nums:
                if abs(i - j) <= min(i, j):
                    result = max(result, i ^ j)
        
        return result
```

## 2933. High-Access Employees 高访问员工

给定一个**24小时内**的员工访问日志`access_times`，其中`access_times[i][0]`为员工姓名，`access_times[i][1]`为四位数字代表的时间，如`00:32 => 0032`，`22:30 => 2230`等。我们定义高访问权限员工为在一个小时的时间窗口内（左闭右开）连续访问超过三次以上，找到所有高访问权限员工的名字。

这道题比较坑的是没说明白员工访问日志的顺序。要注意的是，这个员工访问数据只是一个24小时时间窗口内的，但是他发生的时间是可以重新排列的。因此首先我们要对这个数组进行排序。接着我们就采用常规的窗口方法来计算。对于每位员工，维护一个当前访问时间的窗口，窗口内的时间不能超过一小时。若新添加的时间超过一小时，应该将窗口内的数据弹出直到重新满足一小时时间窗口条件为止。此外，要考虑`12:30`跟`00:01`也能凑成一组的情况，我们可以在遍历的时候遍历两遍，在第二遍的时候给所有时间加上一个24小时的偏移量，这样就规避了这种不好计算的情况。

```python
class Solution:
    def findHighAccessEmployees(self, access_times: List[List[str]]) -> List[str]:
        access_times.sort()
                
        last_access = defaultdict(lambda : deque())
        
        high_access = set()
        
        for i, (name, time) in enumerate(access_times * 2):
            # ignore
            if name in high_access:
                continue

            time = (i // len(access_times)) * 2400 + int(time)
            # print(i, i // len(access_times), len(access_times), name, time)
            
            if not last_access[name]:
                last_access[name].append(time)
                continue
            
            while last_access[name] and last_access[name][0] + 100 <= time:
                last_access[name].popleft()
            
            last_access[name].append(time)
            if len(last_access[name]) >= 3:
                high_access.add(name)
        
        return list(high_access)
```

## 2934. Minimum Operations to Maximize Last Elements in Arrays 最大化数组末位元素的最少操作次数

给定两个数组`nums1`和`nums2`，我们可以选定任意下标`i`来讲`nums1[i]`和`nums2[i]`对调。问最少操作几次能够使得`nums1[-1]`和`nums2[-1]`分别为`nums1`和`nums2`中最大的元素。

这道题可以采取贪心的方式来做。遍历每一个元素下表`i`，若已经满足最大值条件，我们就不处理，否则的话我们尝试对调元素看下是否能够使得条件满足。当然这里隐含了一个条件是`nums1`和`nums2`的末尾元素是固定的，但是题目是允许我们对两个元素进行对调的，因此我们将两个末尾元素对调一次之后再跑一次同样的贪心算法，并比较最大值。这个算法的时间复杂度是`O(n)`。可以看到，下面的算法有一些可以做常数优化的地方，在周赛中没有来得及做。

```python
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        def check(nums1, nums2):
            result = 0
            mval = max(nums1[-1], nums2[-1])

            for i in range(n - 1):
                # no need swap
                if nums1[i] <= nums1[-1] and nums2[i] <= nums2[-1]:
                    continue
                
                nums1[i], nums2[i] = nums2[i], nums1[i]
                result += 1
                # swap performed check
                if nums1[i] <= nums1[-1] and nums2[i] <= nums2[-1]:
                    continue
                
                # impossible
                return int(1e9 + 7)
            return result
        
        result1 = check(list(nums1), list(nums2))
        nums1[-1], nums2[-1] = nums2[-1], nums1[-1]
        result2 = check(list(nums1), list(nums2)) + 1
        
        result = min(result1, result2)
        
        if result >= n:
            return -1
        
        return result
```

## 2935. Maximum Strong Pair XOR II 找出强数对的最大异或值 II

这道题的题干与第一题一样，只是数据范围变大了，这里就不再赘述了。

接着我们考虑强数对`|x - y| <= min(x, y)`的性质。因为我们只要找到数对，而不要求数字的先后顺序，因此我们总可以对数组进行排序处理。在排序之后，对于每个遍历到的`y`，我们考虑用什么`x`来使得上面的数组成立。升序排列后，已知`y`且`y > x`，强数对性质可以化简为`y - x <= x`进而推导出`2 * x >= y`。因此我们需要排除较小的`x`。若我们想要拿到最大的异或值，我们需要`1`交替出现。举个例子，`0b0010 ^ 0b1101 = 0b1111`。因此，我们可以把数字变换成二进制形式之后储存在一个前缀树中。当我们需要匹配最大异或值时，我们就遍历整个树。对于每一个二进制位，我们贪心的拿相反的比特去拼凑较大的异或值。当我们需要移除数字时，前缀树也可以方便地进行移除。因此这个算法的时间复杂度`O(n log n)`加上前缀树操作的`O(k * n)`。注意，我们的前缀树使用了32位的深度，实际上用20位的深度就已经超过题目要求的数据范围了，这里是一个可以优化的地方。


```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_number = False

class BinaryTrie:
    def __init__(self):
        self.root = TrieNode()

    def _get_binary_representation(self, number):
        return bin(number)[2:].zfill(32)

    def add(self, number):
        node = self.root
        for bit in self._get_binary_representation(number):
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.is_end_of_number = True

    def remove(self, number):
        def _remove(node, binary_number, depth):
            if depth == len(binary_number):
                if node.is_end_of_number:
                    node.is_end_of_number = False
                    return len(node.children) == 0
                return False
            bit = binary_number[depth]
            if bit not in node.children or not _remove(node.children[bit], binary_number, depth + 1):
                return False
            del node.children[bit]
            return len(node.children) == 0

        return _remove(self.root, self._get_binary_representation(number), 0)

    def maxXor(self, number):
        binary_number = self._get_binary_representation(number)
        node = self.root
        xor_number = ''
        for bit in binary_number:
            toggle_bit = '1' if bit == '0' else '0'
            if toggle_bit in node.children:
                xor_number += '1'
                node = node.children[toggle_bit]
            else:
                xor_number += '0'
                node = node.children[bit]
        return int(xor_number, 2)

class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        nums.sort()

        t = BinaryTrie()

        result = 0
        left = 0
        for right in range(len(nums)):
            t.add(nums[right])

            while nums[left] * 2 < nums[right]:
                t.remove(nums[left])
                left += 1
            
            result = max(result, t.maxXor(nums[right]))
        
        return result
```