n = int(input())
score = [int(input()) for _ in range(n)]

max_score = score[len(score)-1]
result = 0
for i in range(n-2, -1, -1):
    if score[i] >= max_score:
        result += score[i] - max_score + 1
        sub = score[i] - max_score + 1
        max_score = score[i] - sub
    else:
        max_score = score[i]

print(result)