# 백준 9255 The Friend of My Enemy is My Enemy

t = int(input())


for i in range(t):
    n, m = list(map(int, input().split()))
    # list로 구현 -> 양방향 리스트로 중복 발생
    # set으로 중복 제거 구현
    set_x = [set() for _ in range(n)]
    for j in range(m):
        a, b = list(map(int, input().split()))
        set_x[a-1].add(b)
        set_x[b-1].add(a)
    enemy = int(input())
    print(f'Data Set {i+1}:')
    if set_x[enemy-1]:
        print(*sorted(set_x[enemy-1]))
        print()
    else:
        # enemy와 연결이 안되어있는 경우 띄어쓰기를 한번 더 포함해야하기에 '\n' 추가
        print('\n')