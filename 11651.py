# 백준 11651 좌표 정렬하기 2
import sys
input = sys.stdin.readline

n = int(input())
a = []
for _ in range(n):
    x, y = map(int, input().split())
    # 튜플 형식으로 저장해서 x,y 쌍으로 저장하기
    a.append((x, y))

# y값을 기준으로 하되, 같으면 x값을 기준으로 정렬하기
sorted_items = sorted(a, key=lambda x: (x[1], x[0]))
for i in range(n):
    print(sorted_items[i][0], sorted_items[i][1])