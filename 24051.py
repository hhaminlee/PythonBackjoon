# 백준 24051 알고리즘 수업 - 삽입 정렬 1
import sys
input = sys.stdin.readline

N, K = map(int, input().split())
a = list(map(int, input().split()))
result = -1
def insertion_sort(a):
    global result, save
    save = 0
    for i in range(1, N):
        loc = i - 1
        newItem = a[i]

        while (0 <= loc and newItem < a[loc]):
            a[loc + 1] = a[loc]
            loc -= 1
            save += 1
            if save == K:
                result = a[loc + 1]
                return
        if (loc + 1 != i):
            a[loc + 1] = newItem
            save += 1
            if save == K:
                result = newItem
                return
    return
insertion_sort(a)
print(result)