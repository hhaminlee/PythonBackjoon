import sys
input = sys.stdin.readline

a = []
n = int(input())
for _ in range(n):
    x, y = input().split()
    x = int(x)
    a.append((x, y))

# 나이를 기준으로 정렬하되, 나이가 같으면 입력받은 순으로
sorted_items = sorted(a, key=lambda x: x[0])
for i in range(n):
    print(sorted_items[i][0], sorted_items[i][1])