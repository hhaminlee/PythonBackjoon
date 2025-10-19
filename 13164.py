# 백준 13164 행복 유치원
import heapq

n, k = map(int, input().split())
t_shirt = list(map(int, input().split()))
result = 0

heap = []
for i in range(len(t_shirt)-1):
    heapq.heappush(heap, abs(t_shirt[i] - t_shirt[i+1]))

while len(heap) != k-1:
    result += heapq.heappop(heap)

print(result)