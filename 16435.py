n, l = list(map(int, input().split()))
h = list(map(int, input().split()))
sorted_h = sorted(h)
result = l

for i in range(n):
    if result >= sorted_h[i]:
        result += 1

print(result)