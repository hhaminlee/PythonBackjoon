def dfs(x, y):
    visited[x][y] = True
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        # 격자 바깥으로 빠져나가지 않는 범위안에서 4개 좌표 계산
        if 0 <= nx < n and 0 <= ny < n:
            # 방문하지 않았거나 연결되어 있는 경우 dfs
            if not visited[nx][ny] and ls[nx][ny] == 1:
                dfs(nx, ny)

    
n = int(input())

ls = []
for i in range(n):
    s = input()
    ls.append([int(ch) for ch in s])
visited = [[False] * n for _ in range(n)]
dx = [1, 1, -1, -1]
dy = [1, -1, -1, 1]
count = 0

print(ls)
for i in range(n):
    for j in range(n):
        if ls[i][j] == 1 and not visited[i][j]:
            dfs(i, j)
            count += 1
print(count)