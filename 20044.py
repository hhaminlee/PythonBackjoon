# 백준 20044 Project Teams
# 해결 방법: 
# 문제 요약: 
# 처음 접근: 
# 시행착오: 
# 배운점: 

import sys
input = sys.stdin.readline

n = int(input())

sum_list = []
score = list(map(int, input().split()))
score.sort()

for i in range(n):
    sum_list.append(score[i] + score[-i-1])
print(min(sum_list))