# 백준 14235 크리스마스 선물 

import heapq

# 최대값을 빠르게 뽑아내기 위해서 heapq 사용
# 파이썬 기본은 최소힙이므로 최대힙으로 구현하기 위해 넣을 때 -, 뺄 때 -적용 
n = int(input())

heap = []
for i in range(n):
    kids = input().split()
    if int(kids[0]) == 0:
        if heap:
            print(-heapq.heappop(heap))
        else:
            print(-1)
    else:
        for kid in kids[1:]:
            heapq.heappush(heap, -int(kid))
