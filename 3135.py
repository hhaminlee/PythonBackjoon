a, b = map(int, input().split())
n = int(input())
hz_list = [int(input()) for _ in range(n)]
hz_list.sort()

count = []
count.append(abs(b-a))
for i in range(n):
    count.append(abs(hz_list[i]-b)+1)
print(min(count))