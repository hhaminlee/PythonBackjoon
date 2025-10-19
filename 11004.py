# 백준 11004 K번째 수
import sys
input = sys.stdin.readline

N, K = map(int, input().split())
a = list(map(int, input().split()))

a.sort()
print(a[K-1])