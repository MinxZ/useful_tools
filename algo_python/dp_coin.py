class Solution:
    # with base case and no solution skip 
    # def coinChange(self, coins, amount: int):
    #     def dp(n):
    #         # base case
    #         if n == 0: return 0
    #         if n < 0 : return -1
    #         res = float('inf')
    #         for coin in coins:
    #             sub = dp(n-coin)
    #             # sub problem without solution: continue
    #             if sub == -1: continue
    #             res = min(res, 1+sub)
    #         return res if res != float('inf') else -1
    #     return dp(amount)

    # with memory
    def coinChange(self, coins, amount: int):
        memo = dict()
        def dp(n):
            if n in memo:
                return memo[n]
            # base case
            if n == 0: return 0
            if n < 0 : return -1
            res = float('inf')
            for coin in coins:
                sub = dp(n-coin)
                # need to first compute the sub problem, -1 come from dp(-1), n < 0 or res == inf which means sub of sub is n < 0, dp(1) 
                # sub problem without solution: continue
                if sub == -1: continue
                res = min(res, 1+sub)
            memo[n] = res if res != float('inf') else -1
            return memo[n]
        return dp(amount)

    # dp table
    def coinChange(self, coins, amount: int):
        dp = [float('inf') for i in range(amount+1)]
        dp[0] = 0
        for n in range(1,amount+1):
            for coin in coins:
                if n - coin < 0: continue
                dp[n] = min(dp[n], 1+dp[n-coin])
        return dp[amount] if dp[amount] != float('inf') else -1
