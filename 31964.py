import sys
input = sys.stdin.readline

n = int(input())
xn = list(map(int, input().split()))
tn = list(map(int, input().split()))
dict = dict(zip(xn, tn))

pos = 0 # 트럭의 위치
t = 0 # 현재 시간

dict = sorted(dict.items(), key=lambda x: x[0], reverse=True)
# x[0] 은 집의 위치, x[1] 은 내놓는 시간

for i in range(n):
    travel = abs(pos - dict[i][0])
    t += travel
    if t < dict[i][1]:
        t = dict[i][1]
    pos = dict[i][0]
t += pos
print(t)