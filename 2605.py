# 백준 2605 줄세우기

import sys
input = sys.stdin.readline

n = int(input())
line = list(map(int, input().split()))

result = []
for i in range(n):
    # 현재 result의 길이에서 각 수를 빼줘서 위치 조정
    result.insert(len(result) - line[i], i+1)
print(*result)