# 백준 2776 암기왕
# 해결 방법: 파이썬 in 사용
# 문제 요약: 수첩 쌍 갯수 입력 받은 뒤 수첩1, 수첩2 입력 -> 수첩1에 있는 내용이 수첩 2에 있으면 1 없으면 0
# 처음 접근: note1 sort 이후 in 사용 -> 시간초과
# 시행착오: note1을 set으로 변경 -> 시간초과 해결
# 배운점: list, set, dict 에서 in 사용시에 발생하는 시간 복잡도의 차이

import sys
input = sys.stdin.readline
        
t = int(input())
for _ in range(t):
    n = int(input())
    note1 = set(map(int, input().split()))
    m = int(input())
    note2 = list(map(int, input().split()))
    for note in note2:
        if note in note1:
            print(1)
        else:
            print(0)