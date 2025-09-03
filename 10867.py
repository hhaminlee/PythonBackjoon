import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
a = list(set(a))  # 중복 제거

a.sort()  # 정렬
print(" ".join(map(str, a)))

# gpt 코드
# import sys
# print(" ".join(map(str, sorted(set(map(int, sys.stdin.readline().split()))))))
