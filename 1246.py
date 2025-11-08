# 백준 1246 온라인 판매

n, m = map(int, input().split())
eggs = sorted([int(input()) for _ in range(m)], reverse=True)

result = 0
i = 0
cnt = 0
for egg in eggs:
    i += 1
    temp = egg * i
    if result < temp:
        result = temp
        cnt = egg
    if n == i:
        break
print(cnt, result)