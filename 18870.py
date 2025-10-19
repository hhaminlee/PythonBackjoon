# 백준 18870 좌표 압축
import sys
input = sys.stdin.readline

n = int(input())
x_list = list(map(int, input().split()))

sorted_list = sorted(set(x_list))
enum_list = {num: idx for idx, num in enumerate(sorted_list)}

result = [enum_list[x] for x in x_list]

print(*result)