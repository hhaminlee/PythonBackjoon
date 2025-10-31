# 백준 1969 DNA

# 반복문을 돌면서 각 자릿수마다 가장 많이 출력된 것이 자리의 답
# 만약 나온 순서가 같다면 사전순 정렬
n, m = map(int, input().split())
dna = [input().strip() for _ in range(n)]

result = []
cnt = 0
for i in range(m):
    # 딕셔너리 형태로 알파벳 갯수 카운트
    count = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for j in range(n):
        count[dna[j][i]] += 1
    # 제일 많이 나온 알파벳부터 정렬, 만약 같으면 알파벳 순서대로
    max_base = max(count, key=lambda x: (count[x], -ord(x)))
    result.append(max_base)

# 결과값과 각 자릿수 별 다른 부분 카운트
for i in range(n):
    for j in range(m):
        if dna[i][j] != result[j]:
            cnt += 1

print(''.join(result))
print(cnt)