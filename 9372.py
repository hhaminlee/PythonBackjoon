# 백준 9372 상근이의 여행
t = int(input())

# 모든 국가가 연결되어있다는 것이 보장되어있고,
# 가장 적은 종류의 비행기 수만 구하면 되므로
# 국가 수 - 1 이 정답.

for i in range(t):
    n, m = list(map(int, input().split()))
    for j in range(m):
        a, b = list(map(int, input().split()))
    print(n-1)