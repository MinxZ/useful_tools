class Solution:
    # simple 
    # def fib(self, N: int) -> int:
    #     def dp(n):
    #         if n == 0:
    #             return 0
    #         if n == 1:
    #             return 1
    #         return dp(n-1) + dp(n-2)
    #     return dp(N)

    # memory 
    def fib(self, N: int) -> int:
        memo = dict()
        memo[0] = 0
        memo[1] = 1
        def dp(n):
            if n in memo:
                return memo[n]
            else:
                memo[n] = dp(n-1) + dp(n-2)
            return memo[n]
        return dp(N)

    # dp table
    def fib(self, N: int) -> int:
        if N == 0:
            return 0
        dp = [0 for i in range(N+1)]
        dp[1] = 1
        for i in range(2,N+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[N]
    # def fib(self, N):
    #     dp = {}
    #     dp[0] = 0
    #     dp[1] = 1
    #     for i in range(2, N+1):
    #         dp[i] = dp[i-1] + dp[i-2]
    #     return dp[N]

    # state compress
    def fib(self, N: int) -> int:
        prev, curr = 0, 1
        for n in range(N):
            prev, curr = curr, prev+ curr
        return prev
