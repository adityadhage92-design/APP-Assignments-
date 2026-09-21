def knapsack_bottom_up(weights, values, capacity):
    n = len(weights)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def knapsack_top_down(weights, values, capacity):
    memo = {}

    def solve(i, w):
        if i < 0 or w == 0:
            return 0

        if (i, w) in memo:
            return memo[(i, w)]

        if weights[i] > w:
            result = solve(i - 1, w)
        else:
            result = max(
                solve(i - 1, w),
                values[i] + solve(i - 1, w - weights[i])
            )

        memo[(i, w)] = result
        return result

    return solve(len(weights) - 1, capacity)


weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

print("Bottom-Up Maximum Value:",
      knapsack_bottom_up(weights, values, capacity))

print("Top-Down Maximum Value:",
      knapsack_top_down(weights, values, capacity))
