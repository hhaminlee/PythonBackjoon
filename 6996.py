# 백준 6996 애너그램

n = int(input())
for i in range(n):
    a, b = input().split()
    sorted_a = sorted(a)
    sorted_b = sorted(b)
    if sorted_a == sorted_b:
        print(f"{a} & {b} are anagrams.")
    else:
        print(f"{a} & {b} are NOT anagrams.")