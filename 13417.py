# 백준 13417 카드 문자열
# 해결 방법: 그리디, 리스트 사용
# 문제 요약: N장의 카드에 적혀있는 알파벳의 처음 순서가 주어질 때, 태욱이가 만들 수 있는 카드 문자열 중 사전 순으로 가장 빠른 문자열을 출력하는 프로그램을 작성하시오.
# 처음 접근: 계속 문자열을 붙여가면서 맨 앞의 문자열보다 작거나 같을 때에는 insert, 맨 뒤의 문자열 보다 크거나 같을 때에는 append를 사용해서 문자열 완성
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    result = []
    alpha = list(input().split())
    result.append(alpha[0])
    for ch in alpha[1:]:
        if ch > result[-1]:
            result.append(ch)
        elif ch <= result[0]:
            result.insert(0, ch)
        else:
            result.append(ch)
    print(''.join(result))