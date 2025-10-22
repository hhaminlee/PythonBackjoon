# 백준 15905 스텔라(STELLA)가 치킨을 선물했어요
import sys
input = sys.stdin.readline
n = int(input())

result = []
for i in range(n):
    a, b = map(int, input().split())
    result.append((a, b))

# 1. 푼 문제 많은 순서대로, 2. 페널티는 적은 순서대로 정렬
result.sort(key=lambda x: (-x[0], x[1]))

# 다섯번째 순위를 저장
five = result[4]
cnt = 0

# 반복문을 돌아가면서 다섯번째 순위의 푼 문제와 같은 사람을 찾아 cnt 증가
for prize in result[5:]:
    if prize[0] == five[0]:
        cnt += 1

print(cnt) 