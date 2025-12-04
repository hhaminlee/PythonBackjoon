# 백준 5555 반지

target = input()
n = int(input())
ring = [input() for _ in range(n)]

count = 0
for i in range(len(ring)):
    ring[i] *= 2
    if target in ring[i]:
        count += 1
print(count)