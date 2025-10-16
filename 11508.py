# 백준 11508 2+1 세일
# 처음에는 오름차순으로 정렬하면서 풀었는데, 반례가 생겨 거꾸로 정렬후 풀이 완료

n = int(input())

product = sorted([int(input()) for _ in range(n)], reverse=True)

# 3개씩 묶음으로 저장
sum_product = [product[i:i+3] for i in range(0, n, 3)]

result = 0
for i in range(len(sum_product)):
    # 3개일 경우에만 2+1을 적용할 수 있으므로
    if len(sum_product[i]) == 3:
        result += sum(sum_product[i]) - min(sum_product[i])
    else:
        result += sum(sum_product[i])
print(result)