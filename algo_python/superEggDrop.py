class Solution:
    def superEggDrop(self, K, N):
        dp = [[0] * (K+1) for i in range(N+1)]
        for m in range(1, N+1):
            for k in range(1, K+1):
                dp[m][k] = 1 + dp[m-1][k-1] + dp[m-1][k]
            if dp[m][k] >= N: return m
    def superEggDrop(self, K, N):
        memo = {}
        def dp(k, n):
            if (k, n) in memo:
                return memo[(k, n)]
            if k == 1: return n
            if n == 0: return 0
            res = float('inf')
            lo, hi = 1, n
            while lo <= hi:
                i = (lo+hi)//2
                incres = dp(k-1, i-1) 
                decres = dp(k, n-i) 
                if decres < incres:
                    hi = i-1
                    res = min(res, 1+incres)
                else:
                    lo = i+1
                    res = min(res, 1+decres)
            memo[(k, n)] = res
            return res
        return dp(K, N)
