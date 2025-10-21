# 백준 16916 부분 문자열
# pypy로 했을 경우 시간초과 -> python3로 제출해서 성공
import sys
input = sys.stdin.readline

a = input().rstrip() 
b = input().rstrip()

print(1 if b in a else 0)