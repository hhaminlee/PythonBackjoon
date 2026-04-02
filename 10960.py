# 백준 10960 Calvinball championship, again 1

# 연결되어있는 리스트들은 사이가 좋지 않은 리스트
# 사이가 좋지 않은 요소들을 격리한 최소 리스트 출력

n, m = list(map(int, input().split()))

hate_list = [set() for _ in range(n)]
for i in range(m):
    x, y = list(map(int, input().split()))
    hate_list[x-1].add(y)
    hate_list[y-1].add(x)
    order = sorted(range(n), key=lambda x: -len(hate_list[x]))

color = [0] * n
for i in order:
    used = {color[j-1] for j in hate_list[i]}
    c = 1
    while c in used:
        c += 1
    color[i] = c
print(color)