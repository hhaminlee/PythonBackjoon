# 백준 7795 먹을 것인가 먹힐 것인가
# 해결 방법: A, B 리스트를 입력받은 후 정렬하여 앞에서부터 비교하면서 A의 원소가 클 때 count 증가
# 문제 요약: 두 생명체 A와 B의 크기가 주어졌을 때, A의 크기가 B보다 큰 쌍이 몇 개나 있는지 구하는 프로그램을 작성하시오.
# 처음 접근: 정렬 후 이중 for문으로 비교
# 시행착오: 이중 for문으로 했을 때 시간초과 발생 
# 배운점: python3 말고 pypy3로 시간초과 해결 / 투포인터로 해결, b[j] < x 인경우 계속 j를 증가시키면서 탐색

import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = sorted(list(map(int, input().split())))
    b = sorted(list(map(int, input().split())))
    count = 0
    j = 0
    for x in a:
        while j < m and b[j] < x:
            j += 1
        count += j
    print(count)
