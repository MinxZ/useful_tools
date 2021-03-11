class Solution:
    def findLongestChain(self, pairs) -> int:
        pairs.sort(key=lambda x: x[1])
        cur = float('-inf')
        res = 0
        for p in pairs:
            if cur < p[0]:
                cur = p[1]
                res += 1
        return res
