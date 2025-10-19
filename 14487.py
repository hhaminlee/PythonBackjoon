# 백준 14487 욱제는 효도쟁이야!!
n = int(input())
island = list(map(int, input().split()))
island.sort()
print(sum(island[:n-1]))