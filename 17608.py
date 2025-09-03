import sys
input = sys.stdin.readline

n = int(input())

sticks = [int(input()) for _ in range(n)]
sticks = sticks[::-1]

sum = 1
seek = sticks[0]
for stick in sticks:
    if stick > seek:
        sum += 1
        seek = stick

print(sum)