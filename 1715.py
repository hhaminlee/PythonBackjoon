# 백준 1715 카드 정렬하기
import sys
import heapq
input = sys.stdin.readline

n = int(input())
cards = [int(input().strip()) for _ in range(n)]

heapq.heapify(cards)
# heap = []
sum = 0
if n >= 2:
    while len(cards) > 1:
        n1 = heapq.heappop(cards)
        n2 = heapq.heappop(cards)
        heapq.heappush(cards, n1+n2)
        sum += n1 + n2
print(sum)