import sys
input = sys.stdin.readline
n = int(input())
exp_list = [int(input()) for _ in range(n)] 
exp_list.sort()

sum = 0
for i in range(n):
    sum += abs((i+1) - exp_list[i])
print(sum)