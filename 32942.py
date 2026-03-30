# 백준 32942 그래프와 그래프

# 연결되어있는 모든 노드 탐색하기 > 브루트포스로 구현
# 최대 10 * 10, 이중 for문으로 괜찮을 거라고 생각

a_list = [[] for _ in range(10)]
a, b, c = list(map(int, input().split()))
for i in range(1, 11):
    for j in range(1, 11):
        if a != 0 or b != 0:
            if i * a + j * b == c:
                a_list[i-1].append(j)

# print(a_list)
for i in range(10):
    if a_list[i]:
        print(*a_list[i])
    else:
        print(0)