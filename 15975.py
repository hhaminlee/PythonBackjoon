# 백준 15975 화살표 그리기
import sys
from collections import defaultdict
input = sys.stdin.readline

n = int(input())
a = []
sum_a = 0
for _ in range(n):
    x, y = map(int, input().split())
    a.append((x, y))
a.sort(key=lambda x: (x[1], x[0]), reverse=True)

# 리스트로 그룹화
grouped = defaultdict(list)
for i in a:
    grouped[i[1]].append(i)

# 그룹화된 리스트에서 중복되는 것들만 추출
result = [t for t in grouped.values() if len(t) > 1]

# 중간에 있는 값은 양옆을 확인
# 첫값, 마지막 값은 바로 오른쪽만 확인하여 넣기
if result:
    for i in range(len(result)):
        sum_a += result[i][0][0] - result[i][1][0]
        sum_a += result[i][-2][0] - result[i][-1][0]
        for j in range(1, len(result[i])-1):
            sum_a += min(result[i][j][0] - result[i][j + 1][0], abs(result[i][j-1][0] - result[i][j][0]))
print(sum_a)


# gpt code
# import sys
# from collections import defaultdict
# input = sys.stdin.readline

# n = int(input())
# a = [tuple(map(int, input().split())) for _ in range(n)]

# # y 기준 내림차순, x 기준 내림차순 정렬
# a.sort(key=lambda x: (x[1], x[0]), reverse=True)

# # y 기준 그룹화
# grouped = defaultdict(list)
# for x, y in a:
#     grouped[y].append(x)  # x만 저장하면 됨

# sum_a = 0
# for x_list in grouped.values():
#     if len(x_list) <= 1:
#         continue

#     # 첫 번째와 마지막은 고정
#     sum_a += abs(x_list[0] - x_list[1])
#     sum_a += abs(x_list[-2] - x_list[-1])

#     # 중간 부분은 인접값 중 최소 차
#     for i in range(1, len(x_list) - 1):
#         left = abs(x_list[i] - x_list[i - 1])
#         right = abs(x_list[i] - x_list[i + 1])
#         sum_a += min(left, right)

# print(sum_a)
