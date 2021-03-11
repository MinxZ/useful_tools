class Solution:
    # memory 
    def lengthOfLIS(self, nums) -> int:
        memo = {}
        memo[0] = 1
        N = len(nums)
        def dp(i):
            res = 1
            if i in memo:
                return memo[i]
            for j in range(i):
                if nums[j] < nums[i]:
                    res = max(res, 1+dp(j))
            memo[i] = res
            return memo[i]
        return max([dp(i) for i in range(N)])
    # dp table 
    def lengthOfLIS(self, nums) -> int:
        dp = [1 for i in nums]
        N = len(nums)
        for i in range(N):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], 1+dp[j])
        return max(dp)
    # binary search 
    def lengthOfLIS(self, nums) -> int:
        stack = []
        def find_index(num):
            l, r = 0, len(stack)
            while l != r:
                mid = l + r >> 1
                if num <= stack[mid]:
                    r = mid 
                else:
                    l = mid + 1

            return r
        for num in nums:
            if not stack or num > stack[-1]:
                stack.append(num)
            else:
                position = find_index(num)
                stack[position] = num

        return len(stack)
        