# 백준 11286 절대값 힙
# 해결 방법: heapq 모듈 사용
# 문제 요약: 1. 배열에 정수 x (x ≠ 0)를 넣는다. 2. 배열에서 절댓값이 가장 작은 값을 출력하고, 그 값을 배열에서 제거한다. 절댓값이 가장 작은 값이 여러개일 때는, 가장 작은 수를 출력하고, 그 값을 배열에서 제거한다.
# 처음 접근: 최소힙을 두개 만들어서 음수, 양수값을 저장하도록 만듬
# 시행착오: 음수, 양수 힙을 따로 관리하는 것보다 (절댓값, 실제값) 튜플을 하나의 힙에 넣는 것이 더 간단하다는 것을 알게 됨
# 배운점: 튜플로 힙에 넣어서 우선순위 관리하는 법

import sys
import heapq
input = sys.stdin.readline

n = int(input())
heap = []

for _ in range(n):
    x = int(input())
    if x != 0:
        heapq.heappush(heap, (abs(x),x))
    else:
        if heap:
            print(heapq.heappop(heap)[1])
        else:
            print(0)