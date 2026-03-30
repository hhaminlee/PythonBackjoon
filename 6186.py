# 백준 6186 Best Grass

# 풀이 묶음이 되는 모든 부분을 세기 -> dfs로 구현
def dfs(visited, x, y, grid):
    visited.add((x, y))
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if (nx, ny) not in visited and grid[nx][ny] == '#':
                dfs(visited, nx, ny, grid)

n, m = list(map(int, input().split()))
visited = set()
grass = []
count = 0
for i in range(n):
    tmp = input()
    grass.append(tmp)

for i in range(n):
    for j in range(m):
        # 이미 방문한 칸 / 갈 수 없는 칸 제외 -> 조금 더 빠르게 탐색
        if (i, j) not in visited and grass[i][j] == '#':
            dfs(visited, i, j, grass)
            count += 1

print(count)