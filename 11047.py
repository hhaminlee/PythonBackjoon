import sys
input = sys.stdin.readline

n, k = map(int, input().split())
coins = [int(input()) for _ in range(n)]
coins.sort(reverse=True)
sum = 0
for i in coins:
    sum += k // i
    k %= i

print(sum)