# 백준 14720 우유 축제
# 딸기 -> 초코 -> 바나나 -> 딸기
# 0 -> 1 -> 2 -> 0

n = int(input())
milk = list(map(int, input().split()))

result = 0
drink = 0

for i in milk:
    if i == drink:
        result += 1
        drink = (drink+1)%3 # 다음 순서로 이동

print(result)