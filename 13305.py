import sys
input = sys.stdin.readline 

n = int(input())
bridge = list(map(int, input().split()))
oil = list(map(int, input().split()))

# 최소값이 나올 때마다 갱신
# 갱신이 안되면 이전 값으로 곱하며 진행
min_oil = oil[0]
total_price = 0
for i in range(n - 1):
    if min_oil > oil[i]:
        min_oil = oil[i]
    total_price += min_oil * bridge[i]

print(total_price)