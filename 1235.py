# 백준 1235 학생 번호

def suffix_length(a, b):
    # cnt = 0으로 했을 경우 가장 처음 같을 때 0이 반환 -> 1로 변경
    cnt = 1
    # 뒤에서부터 하나씩 비교
    for x, y in zip(reversed(a), reversed(b)):
        if x == y:
            cnt += 1
        else:
            break
    return cnt

n = int(input())
num = [input().strip() for _ in range(n)]

max_suffix = 1
# 이중 반복문을 돌면서 모든 경우의 접미사 비교
for i in range(n):
    for j in range(i+1, n):
        max_suffix = max(max_suffix, suffix_length(num[i], num[j]))

print(max_suffix)
