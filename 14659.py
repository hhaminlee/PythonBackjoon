# 백준 14659 한조서열정리하고옴ㅋㅋ
import sys
input = sys.stdin.readline

n = int(input())
mountains = list(map(int, input().split()))
best = []

for i in range(n):
    sum = 0
    for j in range(i+1, n):
        if mountains[i] < mountains[j]:
            break
        else:
            sum += 1
    best.append(sum)

print(max(best))