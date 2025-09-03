from collections import deque, defaultdict

def dfs(graph, start_node):
    ## deque 패키지 불러오기
    
    visited = []
    need_visited = deque()
    
    ##시작 노드 설정해주기
    need_visited.append(start_node)
    
    ## 방문이 필요한 리스트가 아직 존재한다면
    while need_visited:
        ## 시작 노드를 지정하고
        node = need_visited.pop()

        ##만약 방문한 리스트에 없다면
        if node not in visited:

            ## 방문 리스트에 노드를 추가
            visited.append(node)
            ## 인접 노드들을 방문 예정 리스트에 추가
            need_visited.extend(reversed(graph[node]))
                
    return visited
    
def bfs(graph, start_node):
    visited = []
    need_visited = deque()
    
    need_visited.append(start_node)
    
    while need_visited:
        node = need_visited.popleft()  
        if node not in visited:
            visited.append(node)
            need_visited.extend(graph[node])
            
    return visited

n, m, start_node = map(int, input().split())
graph = defaultdict(list)
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for v in range(1, n+1):
    graph[v].sort()

dfs_result = dfs(graph, start_node)
bfs_result = bfs(graph, start_node)

print(' '.join(map(str, dfs_result)))
print(' '.join(map(str, bfs_result)))