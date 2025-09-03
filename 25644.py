import sys
input = sys.stdin.readline

n = int(input())
stocks = list(map(int, input().split()))
best = 0
min_price = stocks[0]
for i in stocks[1:]:
    if i - min_price > best:
        best = i - min_price
    if i < min_price: # 미래를 알 필요는 없으므로, 현재까지 중 최소를 찾음
        min_price = i
print(best if best else 0)