def time(h, m, s, d):
    s += d
    if s >= 60:
        m += s // 60
        s %= 60
    if m >= 60:
        h += m // 60
        m %= 60
    h %= 24
    return h, m, s

current = list(map(int, input().split()))
d = int(input())

result = time(current[0], current[1], current[2], d)

print(f"{result[0]} {result[1]} {result[2]}")