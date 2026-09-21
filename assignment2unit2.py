def lcs(X, Y):
    m = len(X)
    n = len(Y)

    dp = [["" for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + X[i - 1]
            else:
                if len(dp[i - 1][j]) >= len(dp[i][j - 1]):
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i][j - 1]

    return dp[m][n]


X = input("Enter first sequence: ")
Y = input("Enter second sequence: ")

result = lcs(X, Y)

print("Longest Common Subsequence:", result)
print("Length:", len(result))
