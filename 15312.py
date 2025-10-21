# 백준 15312 이름 궁합

alpha = [3, 2, 1, 2, 3, 3, 2, 3, 3, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1]
name1 = input()
name2 = input()

n1 = [alpha[ord(c) - ord('A')] for c in name1]
n2 = [alpha[ord(c) - ord('A')] for c in name2]


name = []
for i in range(len(n1)):
    name.append(n1[i])
    name.append(n2[i])

while len(name) > 2:
    tmp = []
    for i in range(len(name) - 1):
        tmp.append((name[i] + name[i + 1]) % 10)
    name = tmp

print(f"{name[0]}{name[1]}")