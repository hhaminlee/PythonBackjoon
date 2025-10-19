# 백준 2751 수 정렬하기 2
import sys
input = sys.stdin.readline

n = int(input())
a = [int(input()) for _ in range(n)]
a.sort()

for i in a:
    print(i)