# 백준 1105 팔
l, r = input().split()
min_count = float('inf')
for i in range(int(l), int(r)+1):
    s = str(i).count('8')
    if s == 0:
        print(0)
        break
    if s < min_count:
        min_count = s
else:
    print(0 if min_count == float('inf') else min_count)

# for-else문, break가 실행되지 않았을 때 else문 실행