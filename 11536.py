# 백준 11536 줄세우기

n = int(input())
names = [input() for _ in range(n)]

inc_names = sorted(names)
dec_names = sorted(names, reverse=True)

inc_flag = 1
dec_flag = 1
for i in range(len(names)):
    if names[i] != inc_names[i]:
        inc_flag = 0
    if names[i] != dec_names[i]:
        dec_flag = 0
if inc_flag == 1:
    print("INCREASING")
elif dec_flag == 1:
    print("DECREASING")
else:
    print("NEITHER")