# 백준 5426 비밀 편지

import math

# 0,0 -> 0,5
# 0,1 -> 1(y위치),4(len - 기존 y 위치)
# 0,2 -> 2,3

n = int(input())
before = [input().strip() for _ in range(n)]

for b in before:
    length = int(math.sqrt(len(b)))
    after = []
    temp = []
    for i in range(len(b)):
        temp.append(b[i])
        if (i+1) % length == 0:
            after.append(temp)
            temp = []
    after_result = [list(x) for x in zip(*after)]
    print(''.join(elem for row in after_result[::-1] for elem in row))
    
