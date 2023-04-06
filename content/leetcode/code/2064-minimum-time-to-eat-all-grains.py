class Solution:
    def minimumTime(self, hens: List[int], grains: List[int]) -> int:
        def check(t):
            idx = 0
            for h in hens:
                move = t
                # if there are grains left of h
                # need to eat left
                if grains[idx] < h:
                    left_cost = h - grains[idx]
                    if left_cost > t:
                        return False
                    # move left and back to original position
                    # move right then move back to left
                    # whichever way is further
                    move = max(0, t - 2 * left_cost, (t - left_cost) // 2)
                    
                if h + move >= grains[idx]:
                    idx = bisect_right(grains, h + move, lo = idx)
                    if idx == len(grains):
                        return True
            return False
        
        hens.sort()
        grains.sort()
        l = 0
        r = 2 * (max(grains[-1], hens[-1]) - min(grains[0], hens[0]))
        while l < r:
            mid = (l + r) // 2
            if check(mid):
                r = mid
            else:
                l = mid + 1
        return l