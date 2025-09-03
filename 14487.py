n = int(input())
island = list(map(int, input().split()))
island.sort()
print(sum(island[:n-1]))