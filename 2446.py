# 백준 2446 별 찍기 - 9
n = int(input())
for i in range(n):
    print(" " * i, end='')
    print("*" * (2*(n-i)-1))
for i in range(n-1, 0, -1):
    print(" " * (i-1), end='')
    print("*" * (2*(n-i)+1))
    
