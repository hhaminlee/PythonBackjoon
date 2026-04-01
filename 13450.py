# 백준 13450 László Babai

# 정점이 3개인 방향 없는 그래프 2개가 주어지고, 두개가 같은지 판단하기
# 정점의 이름(번호)는 상관없고, 간선의 수만 같으면 동형이 됨.


n = int(input())
for i in range(n):
    m = int(input())
    a_edge, b_edge = 0, 0
    a, b = [[] for _ in range(3)], [[] for _ in range(3)]
    for j in range(m):
        x, y = list(map(int, input().split()))
        a[x-1] = y
        a_edge += 1
    l = int(input())
    for k in range(l):
        x, y = list(map(int, input().split()))
        b[x-1] = y
        b_edge += 1
    print('yes' if a_edge == b_edge else 'no')