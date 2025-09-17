import heapq
n = int(input())
heap = []
cnt = 0

n_list = [int(input()) for _ in range(n)]
dasom = n_list[0]
for i in n_list[1:]:
    heapq.heappush(heap, -i)

if n > 1:
    while dasom <= -heap[0]:
        heapq.heappush(heap, heapq.heappop(heap)+1)
        dasom += 1
        cnt += 1
print(cnt)

# gpt 코드
# import heapq

# n = int(input())
# votes = [int(input()) for _ in range(n)]

# dasom, others = votes[0], votes[1:]
# heap = [-x for x in others]  # 최대 힙
# heapq.heapify(heap)

# cnt = 0
# while heap and dasom <= -heap[0]:
#     max_val = -heapq.heapreplace(heap, heap[0] + 1)  # 최댓값 -1 해서 다시 push
#     dasom += 1
#     cnt += 1

# print(cnt)
