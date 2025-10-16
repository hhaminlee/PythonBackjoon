# 백준 15819 너의 핸들은

import sys
input = sys.stdin.readline

n, i = map(int, input().split())

handle = sorted([input().strip() for _ in range(n)])
print(handle[i-1])