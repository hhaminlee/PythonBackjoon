n = int(input())
cup = input()

cnt = 0
for i in range(n):
    if cup[i] == 'S':
        cnt += 1
    elif cup[i] == 'L':
        cnt += 0.5 
cnt += 1
print(min(int(cnt), len(cup)))