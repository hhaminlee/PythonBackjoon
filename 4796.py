# LPV 순으로 입력, 
# L: l일동안만 사용가능 p: 연속하는 일수 v: 휴가 기간
# 몫은 2, 나머지는 4
i = 1
while 1:
    l, p, v = map(int, input().split())
    if l == 0 and p == 0 and v == 0:
        break
    result = (v // p) * l + min(v % p, l)
    print(f"Case {i}: {result}")
    i += 1