# 백준 4963 섬의 개수

# 땅이고
# 이전에 방문한 적이 없으면
# → DFS/BFS 시작
# → 섬 개수 +1

# DFS/BFS는 8방향 모두 검사해 연결된 땅을 한 번에 모두 방문 처리
# 모든 칸을 스캔할 때까지 반복

def dfs(x, y):
    visited[x][y] = True
    for i in range(8):
        nx = x + dx[i]
        ny = y + dy[i]
        # 격자 바깥으로 빠져나가지 않는 범위안에서 8개 좌표 계산
        if 0 <= nx < m and 0 <= ny < n:
            # 방문하지 않았거나 섬인 경우 dfs
            if not visited[nx][ny] and ls[nx][ny] == 1:
                dfs(nx, ny)

    
while True:
    n, m = map(int, input().split())
    if n == m == 0:
        break
    
    ls = []
    for i in range(m):
        ls.append(list(map(int, input().split())))
    visited = [[False] * n for _ in range(m)]
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1,  0,  1, -1, 1, -1, 0, 1]
    count = 0

    for i in range(m):
        for j in range(n):
            if ls[i][j] == 1 and not visited[i][j]:
                dfs(i, j)
                count += 1
    print(count)