import sys
input = sys.stdin.readline

d,c,r = map(int, input().split())
c_list = [int(input()) for _ in range(c)]
r_list = [int(input()) for _ in range(r)]

i = j = 0
while True:
    if i < c and d - c_list[i] >= 0:
        d -= c_list[i]
        i += 1
    elif j < r:
        d += r_list[j]
        j += 1
    else:
        break
print(i+j)