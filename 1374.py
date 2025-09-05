import heapq
import sys
input = sys.stdin.readline
n = int(input())

lec_list = []
before_end = -1
cnt = 0
for i in range(n):
    x, a, b = map(int, input().split())
    lec_list.append((a,b))

sorted_list = sorted(lec_list, key=lambda x: x[0])
heap = []

for start, end in sorted_list:
    # heap의 0번째 요소는 가장 빨리 끝나는 강의의 끝나는 시간
    if heap and heap[0] <= start:
        heapq.heappop(heap)
    heapq.heappush(heap, end)
print(len(heap))