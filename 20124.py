# 백준 20124 모르고리즘 회장님 추천 받습니다

n = int(input())

next_list = [input().split() for _ in range(n)]
sorted_list = sorted(next_list, key=lambda x: (-int(x[1]), x[0]))

print(sorted_list[0][0])