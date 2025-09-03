from collections import deque
import sys
input = sys.stdin.readline

def bfs(graph, start_node):
    visited = [0] * (len(graph))
    need_visited = deque()
    cnt = 1
    
    need_visited.append(start_node)
    visited[start_node] = cnt
    
    while need_visited:
        node = need_visited.popleft()  
        for nxt in graph[node]:
            if visited[nxt] == 0:  # 아직 방문 안 했다면
                cnt += 1
                visited[nxt] = cnt
                need_visited.append(nxt)

    return visited

n, m, start_node = map(int, input().split())
graph = [[] for _ in range(n+1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for v in range(1, n+1):
    graph[v].sort()
bfs_result = bfs(graph, start_node)
print(' '.join(map(str, bfs_result[1:])))
