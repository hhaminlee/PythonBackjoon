# 백준 2204 도비의 영어공부
# 해결 방법: 
# 문제 요약: 
# 처음 접근: 
# 시행착오: 
# 배운점: 

import sys
input = sys.stdin.readline
while True:
    a = int(input())
    if a == 0:
        break
    word_list = [input().strip() for _ in range(a)]
    word_list.sort(key=lambda x: x.lower())
    print(word_list[0])
