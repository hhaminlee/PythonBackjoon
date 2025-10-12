# 백준 2841 외계인의 기타연주

import sys
input = sys.stdin.readline

n, p = map(int, input().split())

cnt = 0
# 6개의 줄을 담고 있는 리스트, 스택으로 사용
stacks = [[] for _ in range(7)]
for _ in range(n):
    a, b = map(int, input().split())

    # 비어있지 않을 때 가장 위에 있는 숫자가 b보다 작을 경우
    if not stacks[a] or stacks[a][-1] < b:
        stacks[a].append(b)
        cnt += 1
    # 가장 위에 있는 숫자가 b보다 클 경우 - 스택에 들어있는 것들을 빼고 넣어야함
    elif stacks[a][-1] > b:
        # 작아질 때까지 빼고, 
        while stacks[a] and stacks[a][-1] > b:
            stacks[a].pop()
            cnt += 1
        # 스택이 비어있는지 확인 후 입력받은 b와 스택의 가장 위에 있는 수가 만약 같지 않다면 다시 넣어줌
        if not stacks[a] or stacks[a][-1] != b:
            stacks[a].append(b)
            cnt += 1
print(cnt)