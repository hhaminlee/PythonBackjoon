import sys
input = sys.stdin.readline

N, K = map(int, input().split())
a = list(map(int, input().split()))

a.sort()
print(a[K-1])