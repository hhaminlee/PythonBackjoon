# 백준 5397 키로거
# 단일 리스트로 구현해보려고 했으나 시간초과
# 왼쪽, 오른쪽 나누어 넣고 나중에 오른쪽 리스트를 거꾸로 붙이는 식으로 구현
from sys import stdin
input = stdin.readline

n = int(input())
for _ in range(n):
    left, right = [], []
    for ch in input().strip():
        if ch == '<' and left:
            right.append(left.pop())
        elif ch == '>' and right:
            left.append(right.pop())
        elif ch == '-' and left:
            left.pop()
        elif ch.isalnum():
            left.append(ch)
    print(''.join(left + right[::-1]))
