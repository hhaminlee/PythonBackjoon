# 백준 28417 스케이트보드

import sys
input = sys.stdin.readline

n = int(input())
result = []
for i in range(n):
    a = list(map(int, input().split()))
    b = max(a[:2])
    c = sorted(a[2:])
    result.append(b + sum(c[-2:]))
print(max(result))