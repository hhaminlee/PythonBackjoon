# 백준 13975 파일 합치기 3
import sys
import heapq
input = sys.stdin.readline

t = int(input())
result = 0
for i in range(t):
    file_data = []
    result = []
    k = int(input())
    file_data = list(map(int, input().split()))
    heapq.heapify(file_data)
    while len(file_data) > 1:
        a = heapq.heappop(file_data)
        b = heapq.heappop(file_data)
        heapq.heappush(file_data, a+b)
        result.append(a+b)
    print(sum(result))