# 백준 14469 소가 길을 건너간 이유 3
import sys
input = sys.stdin.readline

n = int(input())
list_ab = [tuple(map(int, input().split())) for _ in range(n)]
list_ab.sort(key=lambda x: x[0])

result = 0
for idx, (a, b) in enumerate(list_ab):
    result = max(result, a) + b
print(result)