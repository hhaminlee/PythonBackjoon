n = int(input())
sum = 0 
change = 1000 - n

change_list = [500, 100, 50, 10, 5, 1]
for i in change_list:
    sum += change // i # 몫: 동전의 갯수
    change %= i # 나머지: 잔돈

print(sum)