# 백준 2303 숫자 게임

# 조합 사용을 위한 import
from itertools import combinations
n = int(input())
num_list = []
for i in range(n):
    max_num = 0
    tmp = map(int, input().split())
    # 3개를 뽑는 모든 경우의 수 찾기
    for i in combinations(tmp, 3):
        if (sum(i)%10) >= max_num:
            max_num = sum(i)%10
    num_list.append(max_num)

answer = -1
max_num = 0
for i in range(len(num_list)):
    # 최대값을 찾는데, 같으면 큰 번호 출력해야하므로 크거나 같은 것 탐색
    if num_list[i] >= max_num:
        max_num = num_list[i]
        answer = i+1
print(answer)