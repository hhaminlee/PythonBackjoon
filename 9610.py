n = int(input())

q1 = 0
q2 = 0 
q3 = 0
q4 = 0
on_axis = 0
for _ in range(n):
    x, y = map(int, input().split())
    if x > 0:
        if y > 0:
            q1 += 1
        elif y < 0:
            q4 += 1
        else:
            on_axis += 1
    elif x < 0:
        if y > 0:
            q2 += 1
        elif y < 0:
            q3 += 1
        else:
            on_axis += 1
    else:
        if x == 0 or y == 0:
            on_axis += 1
print(f"Q1: {q1}\nQ2: {q2}\nQ3: {q3}\nQ4: {q4}\nAXIS: {on_axis}")