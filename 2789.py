sentence = input()
cam = ['C', 'A' ,'M', 'B', 'R', 'I', 'D', 'G', 'E']
result = []
for i in sentence:
    if i not in cam:
        result.append(i)

print(''.join(result))