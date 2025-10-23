# 백준 5218 알파벳 거리

n = int(input())

for i in range(n):
    dist = []
    a, b = input().split()
    for j in range(len(a)):
        if ord(a[j]) - ord(b[j]) <= 0:
            dist.append(ord(b[j]) - ord(a[j]))
        else:
            dist.append(26 - (ord(a[j]) - ord(b[j])))
    print(f"Distances: {' '.join(map(str, dist))}")
