# 백준 5988 홀수일까 짝수일까
n = int(input())

for _ in range(n):
    a = int(input())
    if a % 2 == 0:
        print("even")
    else:
        print("odd")