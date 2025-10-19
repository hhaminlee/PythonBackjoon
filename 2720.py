# 백준 2720 세탁소 사장 동혁
t = int(input())

change_list = [25, 10, 5, 1]

for _ in range(t):
    change = int(input())
    q = change // 25
    change %= 25

    d = change // 10
    change %= 10

    n = change // 5
    change %= 5

    p = change // 1
    change %= 1
    print(q, d, n, p)