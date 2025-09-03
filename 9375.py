from collections import Counter

n = int(input())

for i in range(n):
    result = 1
    d = {}
    m = int(input())
    for j in range(m):
        key, val = input().split()
        d[key] = val
    counter = Counter(d.values())
    # 독립적으로 선택되기 때문에 전체 조합은 곱의 법칙으로 구함
    for v in counter.values():
        result *= (v + 1)
    # 아무것도 안입는 경우 제외
    print(result-1)