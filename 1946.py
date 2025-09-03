import sys
input = sys.stdin.readline

t = int(input())
for i in range(t):
    n = int(input())
    pair_test = []
    cnt = 1
    for j in range(n):
        pair_test.append(list(map(int, input().split())))
    sorted_pair = sorted(pair_test, key=lambda x: x[0])
    min_pair = sorted_pair[0][1]
    for k in range(n):
        if sorted_pair[k][1] < min_pair:
            min_pair = sorted_pair[k][1]
            cnt += 1
    print(cnt)