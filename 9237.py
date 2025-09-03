n = int(input())
trees = list(map(int, input().split()))
trees.sort(reverse=True)

max_day = -1
for i in range(len(trees)):
    trees[i] += i
    if trees[i] + 1 > max_day:
        max_day = trees[i] + 1
    
print(max_day + 1)
    