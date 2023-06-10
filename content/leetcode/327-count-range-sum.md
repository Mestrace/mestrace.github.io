Title: 327. Count of Range Sum 区间和的个数
Slug: 327-count-of-range-sum
Date: 2023-06-10
Category: Leetcode
Summary: Leetcode Medium 327. Count of Range Sum 区间和的个数 | Binary Search 二分搜索 | Divide and Conquer 分治算法 | Merge Sort 归并排序

[327. Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/description/)

给定一个数字列表`nums`，一个包含范围`[lower, upper]`，求`nums`里面任意`[i, j]`区间元素和在上述范围之内的区间个数。

首先我们可以给出一个朴素的解法。给定索引`i < j`，我们可以通过前缀和求得`sums[i:j] = prefix[j] - prefix[i]`，这样就可以判定是否满足上述条件。

```python
class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        prefix_sum = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]
        
        count = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums) + 1):
                if lower <= prefix_sum[j] - prefix_sum[i] <= upper:
                    count += 1
        return count
```

通过朴素解法，我们可以观察到，这道题的核心问题就是解决给定`prefix[j]`，数出满足`lower <= prefix[j] - prefix[i] <= upper`的`i`的数量。而原数组的顺序并不重要，我们只需要前缀数组排序后的顺序就可以了。这里我们考虑用二分法去优化。依然是按照朴素解法里面遍历每一个前缀元素，但这里我们把已经遍历过的元素放进排序数组里面；对于每一个新的元素，我们使用二分法尝试找已经遍历过的排序数组里面是否由符合区间的数值。

``` python
import bisect

class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        prefix_sums = [0]
        for num in nums:
            prefix_sums.append(prefix_sums[-1] + num)

        count = 0
        sorted_list = [0]

        for x in prefix_sums[1:]:
            left = bisect.bisect_left(sorted_list, x - upper)
            right = bisect.bisect_right(sorted_list, x - lower)
            count += right - left
            bisect.insort(sorted_list, x)

        return count
```

在上面的解法中，我们简单使用了一个列表加上`bisect.insort`去处理插入。读者可以自行选择更好的数据结构，如任意二分搜索树或者B树来代替列表。

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>

除此之外，我们还有一个更好的解法。我们可以利用Divide and Conquer分治的思想，将数组划分为两个子数组，分别对两个子数组进行递归处理，然后再合并两个子数组的答案。更具体地说，我们可以先对数组进行排序，然后将数组划分为两个子数组，分别是`[left, mid]`和`[mid + 1, right]`。对于每个子数组，我们可以递归地计算出其范围和的答案，然后再合并两个子数组的答案。当然，这个算法可能有点难以理解，我尝试尽量清晰地讲明白。

对于分治算法来说，我们在写的时候不可能命令式地在头脑中执行这个算法，而是得先做一些假设，假设递归之后的结果，再来写当前的逻辑。在每一步递归完成之后，我们可以假设`prefix[left:mid]`和`prefix[mid + 1:right]`为已排序的两部分。此外，这两个子数组内部的和也已经求出。紧接着就需要基于这两部分计算我们要求的区间范围和的个数，即开始元素在左半部分，结束元素在右半部分。因此，我们遍历每一个左半部分的元素`prefix[i]`，尝试找到右边中元素的区间`[j, k]`使得`lower <= prefix[j] - prefix[i] <= prefix[k] - prefix[i] <= upper`。当我们找到这样一个区间`[j, k]`时，我们就将`j`和`k`之间的区间个数累加到结果中。最后，我们合并排好序的两部分即可。这一段递归分治实质上就是归并排序Merge Sort的思想。在下列代码中，只是为了简化概念的展示，我用了Python内置的`sorted`处理归并，读者可以自行实现`merge`方法，此处不多赘述。

```python
class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        prefix = [0] * (len(nums) + 1)
        for i in range(1, len(prefix)):
            prefix[i] = nums[i - 1] + prefix[i - 1]
        
        def mergesort(left, right):
            if left >= right:
                return 0
            
            mid = left + (right - left) // 2

            count = mergesort(left, mid) + mergesort(mid + 1, right)

            j = mid + 1
            k = mid + 1

            for i in range(left, mid + 1):
                while k <= right and prefix[k] - prefix[i] < lower:
                    k += 1
                while j <= right and prefix[j] - prefix[i] <= upper:
                    j += 1
                count += j - k
            
            prefix[left: right + 1] = sorted(prefix[left: right + 1])
            return count
        
        return mergesort(0, len(prefix) - 1)
```

类似的分治题目也可以看看

- [Medium - 912. Sort an Array](https://leetcode.com/problems/sort-an-array/description/)
- [Hard - 493. Reverse Pairs](https://leetcode.com/problems/reverse-pairs/)
- [Hard - 315. Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/)
- [Hard - 1885. Count Pairs in Two Arrays](https://leetcode.com/problems/count-pairs-in-two-arrays/description/)