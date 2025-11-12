# 백준 11645 I’ve Been Everywhere, Man

n = int(input())

for i in range(n):
    a = int(input())
    result = set()
    for j in range(a):
        word = input()
        result.add(word)
    print(len(result))