a, b = map(int, input().split())
result = -1
while b > 0:
    if b % 2 == 0:
        b //= 2
        result += 1
    elif b % 10 == 1:
        b //= 10
        result += 1
    else:
        break
    if b == a:
        break
print(result+2 if b == a else -1)