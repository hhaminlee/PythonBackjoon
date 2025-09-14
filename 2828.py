n, m = map(int, input().split())
j = int(input())

left = 1
right = m
total_move = 0
for _ in range(j):
    apple = int(input())
    if left <= apple <= right:
        continue

    elif apple < left:
        move = left - apple
        total_move += move
        left = apple
        right = left + (m - 1)

    else:
        move = apple - right
        total_move += move
        right = apple
        left = right - (m - 1)
print(total_move)