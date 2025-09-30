# 백준 9076 점수 집계
# 해결 방법: 
# 문제 요약: 
# 처음 접근: 
# 시행착오: 
# 배운점: 

import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    score_list = list(map(int, input().split()))
    score_list.sort()
    if score_list[3] - score_list[1] >= 4:
        print("KIN")
    else:
        print(sum(score_list[1:4]))