# 백준 2506 점수계산
n = int(input())
score = list(map(int, input().split()))
sum = 0
s = 0
for i in range(n):
    if score[i] == 0:
        s = 0
    else:
        s += 1
    sum += s
print(sum)