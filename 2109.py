# 백준 2109 순회강연
import heapq

n = int(input())
money_list = [tuple(map(int, input().split())) for _ in range(n)]
heap = []

money_list.sort(key=lambda x: x[1])
i = 1
for p, d in money_list:
    heapq.heappush(heap, p)
    if len(heap) > d:
        heapq.heappop(heap)
print(sum(heap))