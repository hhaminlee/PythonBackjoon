# 백준 15969 행복
n = int(input())
students = list(map(int, input().split()))
print(max(students) - min(students))