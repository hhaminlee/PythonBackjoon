# 백준 1911 흙길 보수하기
import math

n, l = map(int, input().split())

water_list = []
covered = 0
result = 0
for i in range(n):
    start, end = map(int, input().split())
    water_list.append((start, end))

water_list.sort(key=lambda x: x[0])

for start, end in water_list:
    curr = max(start, covered) # 시작값 or 이전 값 중 최고값
    if curr >= end: # 이미 덮여있다면 넘어감
        continue
    length = end - curr # 해당 웅덩이의 길이
    need = math.ceil(length / l) # 필요한 널빤지 갯수
    result += need # 널빤지 갯수 계속 더해나감
    covered = curr + need * l # 널빤지로 덮은 후 최대값 계산(덮여있는 구간 중 최대)

print(result)