class Solution:
    def minimizeMax(self, nums: List[int], p: int) -> int:
        def check(m):
            k = 0
            i = 1
            while i < len(nums) and k < p:
                # print(i, nums[i], nums[i - 1])
                if nums[i] - nums[i - 1] <= m:
                    k += 1
                    i += 1
                i += 1
            return k >= p

        nums.sort()

        left = 0
        right = nums[-1] - nums[0] + 1

        while left < right:
            mid = left + (right - left) // 2
            
            if check(mid):
                right = mid
            else:
                left = mid + 1
        return left