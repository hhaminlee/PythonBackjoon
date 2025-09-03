import sys
input = sys.stdin.readline 
n, l, r = map(int, input().split())
a = list(map(int, input().split()))
sorted_mid = sorted(a[l-1:r])
result = a[:l-1] + sorted_mid + a[r:]

# 빌트인 함수인 all 이용해서 구현하기
# 주어진 모든 요소가 True 인지 확인하고 True를 반환해줌
is_sorted = all(result[i] <= result[i+1] for i in range(len(result) - 1))
if is_sorted:
    print(1)
else:
    print(0)

# gpt 코드
# import sys
# input = sys.stdin.readline

# n, l, r = map(int, input().split())
# a = list(map(int, input().split()))

# # L~R 구간만 정렬해서 전체 수열 재구성
# a[l-1:r] = sorted(a[l-1:r])

# # 단조 증가인지 체크
# print(1 if all(a[i] < a[i+1] for i in range(n - 1)) else 0)

