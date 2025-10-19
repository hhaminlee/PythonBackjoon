# 백준 1817 짐 챙기는 숌
n, m = map(int, input().split())
result = [0] * n
idx = 0 # 담긴 상자의 인덱스
i = 0 # 현재 확인 상자의 인덱스

if n != 0:
    box = list(map(int, input().split()))
    if max(box) <= m:
        while i < n:
            if result[idx] + box[i] <= m:
                result[idx] += box[i]
                i += 1
            else:
                idx += 1
count = len([x for x in result if x != 0])
print(count)