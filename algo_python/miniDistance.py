import numpy as np
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        memo = {}
        def dp(i, j):
            if (i, j) in memo: 
                return memo[(i,j)]
            if i == -1: return j+1
            if j == -1: return i+1
            if word1[i] == word2[j]:
                memo[(i,j)] = dp(i-1, j-1)
            else:
                memo[(i,j)] = min(dp(i-1, j)+1,  # delete
                           dp(i, j-1)+1,  # insert
                           dp(i-1, j-1)+1   # replace
                           )

            return memo[(i,j)]  
        return dp(len(word1)-1, len(word2)-1)
    
    def minDistance(self, word1, word2):
        """Dynamic programming solution"""
        m = len(word1)
        n = len(word2)
        table = [[0] * (n + 1) for _ in range(m + 1)]
        table2 = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            table[i][0] = i
        for j in range(n + 1):
            table[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    table[i][j] = table[i - 1][j - 1]
                    table2[i][j] = 0
                else:
                    table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
                    table2[i][j] = np.argmin([table[i - 1][j - 1], table[i - 1][j], table[i][j - 1]])+1
        print(table2)
        print(table)
        return table[-1][-1]

# replace 1
# delete 2
# insert 3

[[0, 0, 0, 0], 
[0, 1, 1, 1], 
[0, 1, 0, 3], 
[0, 0, 2, 1], 
[0, 2, 1, 0], 
[0, 2, 1, 2]]

[[0, 1, 2, 3], 
[1, 1, 2, 3], 
[2, 2, 1, 2], 
[3, 2, 2, 2], 
[4, 3, 3, 2], 
[5, 4, 4, 3]]