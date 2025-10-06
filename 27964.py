# 백준 27964 콰트로치즈피자

import sys
input = sys.stdin.readline
n = int(input())
cheese = input().split()

result = set()
for c in cheese:
    if c.endswith('Cheese'):
        result.add(c)
# 처음 4일 때만 체크해서 4이상의 치즈가 있을 때 틀림 -> 4 이상으로 변경
if len(result) >= 4:
    print('yummy')
else:
    print('sad')