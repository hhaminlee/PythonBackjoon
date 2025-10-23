# 백준 5586 JOI와 IOI

name = input()
count_j = 0
count_i = 0

for i in range(len(name) - 2):
    if 'JOI' in name[i:i+3]:
        count_j += 1
    if 'IOI' in name[i:i+3]:
        count_i += 1
print(f"{count_j}\n{count_i}")