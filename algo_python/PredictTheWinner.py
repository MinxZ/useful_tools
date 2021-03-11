class Solution:
    def PredictTheWinner(self, piles) -> bool:
        if len(piles) == 1:
            return True
        n = len(piles)
        dp = [[[0, 0] for i in range(n)] for i in range(n)]

        for i in range(n):
            dp[i][i][0] = piles[i]

        for l in range(2, n+1):
            for i in range(n-l+1):
                j = i+l-1

                left = piles[i] + dp[i+1][j][1]
                right = piles[j] + dp[i][j-1][1]

                if left > right:
                    dp[i][j][0] = left
                    dp[i][j][1] = dp[i+1][j][0]
                else:
                    dp[i][j][0] = right
                    dp[i][j][1] = dp[i][j-1][0]
        res = dp[0][n-1]
        win = res[0] - res[1] >= 0
        return win
