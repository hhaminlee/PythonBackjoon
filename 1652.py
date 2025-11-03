# 백준 1652 누울 자리를 찾아라
n = int(input())
lay_list = [input() for _ in range(n)]

cnt_row = 0
cnt_col = 0

for row in lay_list:
    cnt = 0
    for cell in row.split('X'):  # X로 끊기
        if len(cell) >= 2:       # 두 칸 이상 비었으면 누울 수 있음
            cnt += 1
    cnt_row += cnt

flipped = [''.join(col) for col in zip(*lay_list)]  

for col in flipped:
    cnt = 0
    for cell in col.split('X'):
        if len(cell) >= 2:
            cnt += 1
    cnt_col += cnt

print(cnt_row, cnt_col)
