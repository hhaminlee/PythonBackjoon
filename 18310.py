n = int(input())
home = list(map(int, input().split()))

home.sort()

if n % 2 == 0:
    mid = home[n//2 - 1]
else:
    mid = home[n//2]

print(mid)