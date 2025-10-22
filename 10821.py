# 백준 10821 정수의 개수

n = input().split(',')

cnt = 0
for num in n:
    if num.isdigit():
        cnt += 1
print(cnt)