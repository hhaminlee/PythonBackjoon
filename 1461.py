# 백준 1461 도서관
n, m = map(int, input().split())
books = list(map(int, input().split()))
books.sort()

minus_list = []
plus_list = []
result = 0
for book in books:
    if book < 0:
        minus_list.append(book)
    else:
        plus_list.append(book)

# 음수리스트는 가장 작은 것부터 m개 묶기
# 양수리스트는 가장 큰 것부터 m개 묶기
if not minus_list:
    max_dist = max(plus_list)
elif not plus_list:
    max_dist = abs(min(minus_list))
else:
    max_dist = max(abs(min(minus_list)), max(plus_list))
i = 0
while i < len(minus_list):
    curr = minus_list[i]          # 증가 전에 현재 값 확보

    if max_dist == -curr:
        result -= curr            # 최장거리면 편도(한 번만)
    else:
        result -= curr * 2        # 그 외엔 왕복(두 번)

    i += m

j = 0
plus_list.sort(reverse=True)
while j < len(plus_list):
    curr = plus_list[j]          # 증가 전에 현재 값 확보

    if max_dist == curr:
        result += curr            # 최장거리면 편도(한 번만)
    else:
        result += curr * 2        # 그 외엔 왕복(두 번)

    j += m
print(result)