# 백준 1427 소트인사이드
n = input()
result = []
for i in range(len(n)):
    result.append(n[i])

result.sort(reverse=True)
print(''.join(result))