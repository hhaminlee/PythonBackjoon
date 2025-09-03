n = int(input())
balloon = list(map(int, input().split()))
balloon_with_index = list(enumerate(balloon, start=1))
index = 0
result = []
while balloon_with_index:
    num, val = balloon_with_index.pop(index)
    result.append(num)    

    if not balloon_with_index:
        break

    if val > 0:
        index = (index + val - 1) % len(balloon_with_index)
    else:
        index = (index + val) % len(balloon_with_index)

print(*result)