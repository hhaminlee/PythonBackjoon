import sys
input = sys.stdin.readline
d = {}
n = int(input())
for _ in range(n):
    student = list(map(int, input().split()))
    d[student[0]] = student[1:]

# result를 딕셔너리가 가지고 있는 리스트로 변환
result = list(d.items())
for i in range(4):
    sorted_students = sorted(result, key=lambda x: (-x[1][i], x[0]))

    # 가장 높은 점수를 가진 학생
    aa = sorted_students[0][0]

    print(aa, end=' ')
    # 뽑힌 학생은 result에서 제거
    result = [x for x in result if x[0] != aa]

