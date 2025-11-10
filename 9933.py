# 백준 9933 민균이의 비밀번호

n = int(input())
password = [input().strip() for _ in range(n)]

for p in password:
    if p[::-1] in password:
        mid = p[int(len(p)/2)]
        len_p = len(p)
        break

print(len_p, mid)