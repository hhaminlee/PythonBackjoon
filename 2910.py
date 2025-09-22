from collections import Counter

n, c = map(int, input().split())
a = list(map(int, input().split()))

counter = Counter(a)

# most_common은 기본적으로 빈도수 정렬이지만, 등장 순서를 보장함
for num, freq in counter.most_common():
    print((str(num) + ' ') * freq, end='')