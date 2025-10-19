# 백준 11328 Strfry
n = int(input())

for _ in range(n):
    a, b = input().split()
    # sort는 str에 없으므로 sorted를 사용해야됨
    sorted_a = sorted(a)
    sorted_b = sorted(b)
    if sorted_a == sorted_b:
        print("Possible")
    else:
        print("Impossible")