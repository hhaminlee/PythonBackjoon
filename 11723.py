# 백준 11723 집합
import sys
input = sys.stdin.readline

n = int(input())
s = set()
result = []
for i in range(n):
    command = list(input().split())
    if len(command) != 1:
        match command[0]:
            case 'add':
                s.add(command[1])
            case 'remove':
                if command[1] in s:
                    s.remove(command[1])
            case 'check':
                if command[1] in s:
                    print(1)
                else: 
                    print(0)
            case 'toggle':
                if command[1] in s:
                    s.remove(command[1])
                else:
                    s.add(command[1])
    else:
        match command[0]:
            case 'all':
                s = {str(i) for i in range(1, 21)}
            case 'empty':
                s = set()