# 백준 1919 애너그램 만들기
a = sorted(input())
b = sorted(input())
cnt = 0

if len(a) > len(b):
    for ch in a:
        if ch in b:
            b.remove(ch)
            cnt += 1
else:
    for ch in b:
        if ch in a:
            a.remove(ch)
            cnt += 1
print(len(a) + len(b) - cnt)