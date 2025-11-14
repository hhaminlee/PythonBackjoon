# 백준 11724 연결 요소의 개수

def dfs(v, visited, graph):
    visited[v] = True
    for i in graph[v]:
        if not visited[i]:
            dfs(i, visited, graph)

n, m = map(int, input().split())
cc = [[] for _ in range(n+1)]

for _ in range(m):
    a, b = map(int, input().split())
    # 무방향 그래프 양쪽으로 append 해주어서 만들기
    cc[a].append(b)
    cc[b].append(a)
visited = [False] * (n+1)

count = 0
# 요소에 방문하고 연결된 것들을 계속 찾아나감
for i in range(1, n+1):
    if not visited[i]:
        dfs(i, visited, cc)
        count += 1

print(count)