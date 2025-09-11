import sys
input = sys.stdin.readline

n = int(input())
drinks = list(map(int, input().split()))
drinks.sort()
result = 0
while len(drinks) >= 2:
    drinks[len(drinks)-1] = ((drinks[0] / 2) + drinks[len(drinks)-1])
    drinks.pop(0)
print(sum(drinks))