import sys
import heapq
input = sys.stdin.readline

n = int(input())
conf = []
cnt = 0
before_end = min_interval = -1
for i in range(n):
    start, end = map(int, input().split())
    conf.append((start, end))

sorted_conf = sorted(conf, key=lambda x: x[0])
heap = []
for start, end in sorted_conf:
    # 힙에 요소가 존재하는데, 그 end가 start보다 느릴경우 pop -> 회의 시간이 연결되면 pop
    # 그게 아니면 계속 push 
    if heap and heap[0] <= start:
        heapq.heappop(heap)
    heapq.heappush(heap, end)
# 힙에 남아있는 건 연결되지 않은 회의실의 갯수
print(len(heap))