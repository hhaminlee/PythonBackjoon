# 백준 16212 정열적인 정렬
# 해결 방법: 파이썬 내장함수 sort사용
# 문제 요약: 수열이 주어졌을 때, 오름차순으로 정렬해서 출력
# 처음 접근: 파이썬 내장함수 sort사용
# 시행착오: join 함수 관련 사용법
# 배운점: join시에 str로 바꿔줘야함

import sys
input = sys.stdin.readline

n = int(input())
n_list = list(map(int, input().split()))
print(' '.join(map(str, sorted(n_list))))