# 백준 1138 한 줄로 서기
n = int(input())

height = list(map(int, input().split()))
result = []
for i in range(n, 0, -1):
    result.insert(height[i-1], i)

print(*result)