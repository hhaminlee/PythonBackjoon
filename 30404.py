import sys
input = sys.stdin.readline

n, k = map(int, input().split())
duck = list(map(int, input().split()))

interval = [(duck[i], duck[i] + k) for i in range(n)]
interval.sort(key=lambda x: x[1]) # x+k 기준 정렬

clap = -1
result = 0
for start, end in interval:
    if start > clap:  # 현재 박수치는 시간보다 시작 시간이 더 크면 박수 칠 수 있음
        result += 1
        clap = end  # 박수치는 시간 갱신

print(result)