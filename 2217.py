# 백준 2217 로프
n = int(input())
lopes = [int(input()) for _ in range(n)]
lopes.sort()

# 해당 인덱스부터 끝까지 더한 값들을 리스트에 저장
# 가장 큰 값을 출력
result = []
for i in range(n):
    result.append(lopes[i]*(n-i))
print(max(result))