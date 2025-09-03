import sys
input = sys.stdin.readline

# 중복값의 갯수 구하기

n = int(input())
a = []
mat = list(map(int, input().split()))
count_dict = {}

for item in mat:
    if item in count_dict:
        count_dict[item] += 1
    else:
        count_dict[item] = 1

print(max(count_dict.values()))