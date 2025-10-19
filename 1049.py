# 백준 1049 기타줄
# 전부 낱개 / 패키지 / 패키지 + 낱개
# 답은 min으로 세개 중 고르기
import math
n, m = map(int, input().split())

pack_min = 2000
each_min = 2000
for i in range(m):
    pack, each = map(int, input().split())
    if pack_min > pack:
        pack_min = pack
    if each_min > each:
        each_min = each
    
all_each = n * each_min
k = n // 6 # 필요한 패키지 수
r = n % 6 # 필요한 낱개 수
each_pack = k * pack_min + r * each_min
all_pack = math.ceil(n/6) * pack_min
print(min(all_each, all_pack, each_pack))
    