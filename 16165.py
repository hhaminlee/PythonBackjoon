# 백준 16165 걸그룹 마스터 준석이

import sys
input = sys.stdin.readline

n, m = map(int, input().split())

group = {}
for _ in range(n):
    a = input()
    b = int(input())
    group[a] = [input() for _ in range(b)]
# 그룹명을 key로, 멤버들을 value로 구별하여 저장

for _ in range(m):
    a = input()
    b = int(input())
    if b == 0:
        print('\n'.join(sorted(group[a])))
    else:
        # value로 key 찾기
        key = [k for k, v in group.items() if a in v][0]
        print(key)