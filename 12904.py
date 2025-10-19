# 백준 12904 A와 B
# s -> t로 가는걸 생각하지 말고 거꾸로 계산하는게 더 쉬움

s = input()
t = input()

result = 0
while len(t) > 1:
    if t[len(t)-1] == 'A':
        t = t[:-1]
    elif t[len(t)-1] == 'B':
        t = t[:-1]
        t = t[::-1]
    if s == t:
        result = 1  
        break
print(result)