# 백준 27160 할리갈리

n = int(input())
card = {'STRAWBERRY': 0, 'BANANA':0, 'LIME':0, 'PLUM':0}

for i in range(n):
    name, cnt = input().split()
    card[name] += int(cnt)

result = 'NO'
for name, cnt in card.items():
    if cnt == 5:
        result = 'YES'

print(result)