# 백준 1977 완전제곱수
import math
a = int(input())
b = int(input())
sum = 0
minimum = []
for i in range(a, b+1):
    if(math.sqrt(i) == int(math.sqrt(i))):
        sum += i
        minimum.append(i)

if(sum == 0):
    print(-1)
else:
    print(sum)
    print(minimum[0])