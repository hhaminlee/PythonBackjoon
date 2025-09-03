from collections import deque, defaultdict

def bfs_dist(graph, start, n):
    dist = [-1] * (n + 1)   # 거리: -1 = 미방문
    dq = deque([start])
    dist[start] = 0

    while dq:
        node = dq.popleft()
        for nxt in graph[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1
                dq.append(nxt)
    return dist

n = int(input().strip())
x, y = map(int, input().split())
m = int(input().strip())

graph = defaultdict(list)
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for v in range(1, n + 1):
    graph[v].sort()

dist = bfs_dist(graph, y, n)   # y에서 출발해 모든 노드까지의 촌수
print(dist[x])                 # x까지의 촌수(없으면 -1이 찍힘)
