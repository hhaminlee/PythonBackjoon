# 백준 4458 첫 글자를 대문자로

import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    a = input()
    a = a[0].upper()+a[1:]
    print(a)