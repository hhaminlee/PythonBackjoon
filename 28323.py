import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

b = []
if n == 1:
    print(1)
else:
    for i in range(len(a)-1):
        if (a[i] + a[i+1]) % 2 == 1:
            b.append(a[i])
    print(len(b) + 1) # 시작구간이 항상 포함되지 않기 때문에