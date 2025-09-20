import heapq
n, m = map(int, input().split())
heap = list(map(int, input().split()))

heapq.heapify(heap)
for i in range(m):
    s = heapq.heappop(heap) + heapq.heappop(heap)
    heapq.heappush(heap, s)
    heapq.heappush(heap, s)
print(sum(heap))