# 백준 11660 구간 합 구하기 5

n, m = map(int, input().split())
mat = [list(map(int, input().split())) for _ in range(n)]

s = [[0]*(n+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, n+1):
        s[i][j] = mat[i-1][j-1] + s[i-1][j] + s[i][j-1] - s[i-1][j-1]

for i in range(m):
    result = 0
    a, b, c, d = map(int, input().split())
    result += s[a-1][b-1] + s[c][d] - s[a-1][d] - s[c][b-1]
    print(result)