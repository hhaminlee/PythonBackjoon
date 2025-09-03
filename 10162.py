n = int(input())

a = [300, 60, 10]
result = []
for i in a:
    result.append(n // i)
    n %= i

if n != 0:
    print(-1)
else:
    print(*result)