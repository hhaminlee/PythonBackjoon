import sys
input = sys.stdin.readline

park_sum = 0
n = int(input())
a = list(map(int, input().split()))

a.sort(reverse = True)

if n % 2 == 0:
    for i in range(n // 2):
        park_sum += a[i]
else:
    for i in range(n // 2 + 1):
        park_sum += a[i]

print(sum(a) - park_sum, park_sum)

# gpt 코드
# import sys
# input = sys.stdin.readline

# n = int(input())
# a = sorted(map(int, input().split()), reverse=True)

# half = n // 2 + n % 2  # 홀수일 때는 하나 더
# park_sum = sum(a[:half])
# other_sum = sum(a[half:])

# print(other_sum, park_sum)