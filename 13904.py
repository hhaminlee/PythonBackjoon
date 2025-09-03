# heap에 넣고 넘치면 가장 작은 걸 빼는 식으로 진행
# 큰 값이 들어오면 그 값이 그대로 남아있고, 작은 값이 들어오면 바로 빠져나감
import heapq
n = int(input())

heap = []
result = 0
score = [tuple(map(int, input().split())) for _ in range(n)]

sorted_score = sorted(score, key=lambda x: x[0])
for d, w in sorted_score:
    heapq.heappush(heap, w)
    if len(heap) > d:
        heapq.heappop(heap)
print(sum(heap))