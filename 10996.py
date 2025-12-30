# 백준 10996 별 찍기 - 21
n = int(input())
for i in range(n):
    for j in range(2):
        for k in range(n):
            if j % 2 == 0:
                if k % 2 == 0:
                    print('*', end='')
                else:
                    print(' ', end='')
            else:
                if k % 2 != 0:
                    print('*', end='')
                else:
                    print(' ', end='')
        print()