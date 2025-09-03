import sys
input = sys.stdin.readline

n = int(input())
conf = []
cnt = 0
before_end = -1
for i in range(n):
    start, end = map(int, input().split())
    conf.append((start, end))

sorted_conf = sorted(conf, key=lambda x: (x[1], x[0]))

for start, end in sorted_conf:
    if before_end <= start:
        before_end = end
        cnt += 1
        
print(cnt)