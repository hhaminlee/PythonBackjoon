# 방향이 다르면 갯수만큼
# 방향이 같으면 //2 만큼

perfect = []
i = 1

while True:
    s = input()
    if '-' in s:
        break
    stack = []
    for ch in s:
        if ch == '{':
            stack.append('{')
        else:
            if stack and stack[-1] == '{':
                stack.pop()
            else:
                stack.append('}')
    m = len(stack)
    o = stack.count('{')
    result = m//2 + (o%2)
    print(f"{i}. {result}")
    i += 1