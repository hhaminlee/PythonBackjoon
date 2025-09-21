import heapq

heap = []
n = int(input())
for _ in range(n):
    for i in list(map(int, input().split())):
        heapq.heappush(heap, i)
        if len(heap) > n:
            heapq.heappop(heap)

print(heapq.heappop(heap))