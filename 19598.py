import heapq
import sys
input = sys.stdin.readline

n = int(input())

conf = []
heap = []
for i in range(n):
    start, end = map(int, input().split())
    conf.append((start, end))
sorted_conf = sorted(conf, key=lambda x: x[0])

before_end = -1
for start, end in sorted_conf:
    # heap[0]은 가장 작은 값
    if heap and heap[0] <= start:
        heapq.heappop(heap)
    heapq.heappush(heap, end)
print(len(heap))