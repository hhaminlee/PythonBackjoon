import sys
input = sys.stdin.readline

n = int(input())
a = []

# strip으로 공백 제거 후 입력받기
a = [input().strip() for _ in range(n)]

a = list(set(a))
sorted_items = sorted(a, key=lambda x: (len(x), x))

for i in sorted_items:
    print(i)