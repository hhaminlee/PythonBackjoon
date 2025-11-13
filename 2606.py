# 백준 2606 바이러스
def dfs(graph, v, visited):
    visited[v] = True
    global count
    count += 1
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)
count = 0
computer = int(input())
pair = int(input())

graph = [[] for _ in range(computer+1)]

for _ in range(pair):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

visited = [False] * (computer+1)
dfs(graph, 1, visited)

print(count-1)