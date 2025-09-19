# 3273 두 수의 합
n = int(input())
a_list = list(map(int, input().split()))
x = int(input())

a_list.sort()

# 투포인터 코드
cnt = 0
left, right = 0, n-1
while left < right:
    s = a_list[left] + a_list[right]
    # 같을 때에는 사이를 좁혀가면서 다시 확인함
    if s == x:
        cnt += 1
        left += 1
        right -= 1
    # 만약 x값이 더 클경우는 작은 값의 인덱스를 증가시켜 근사값으로
    elif s < x:
        left += 1
    # s값이 더 크면 큰값의 인덱스를 줄임
    else:
        right -= 1
print(cnt)
