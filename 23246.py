# 딕셔너리를 통해서 정렬 기준을 정하고 정렬하기
# 첫번째 기준은 곱의 크기, 두번째 기준은 합의 크기, 세번째 기준은 키의 크기
# 낮을 수록 우선순위가 높음
n = int(input())
d={}

for i in range(n):
    k, v1, v2, v3 = map(int, input().split())
    d[k] = (v1 * v2 * v3, v1 + v2 + v3)

sorted_items = sorted(d.items(), key=lambda x: (x[1][0], x[1][1], x[0]))

print(' '.join(str(sorted_items[i][0]) for i in range(3)))