n = int(input())
m = int(input())
num_list = list(map(int, input().split()))
num_list.sort()
left = 0
right = n-1
cnt = 0
while left < right:
    if num_list[left] + num_list[right] == m:
        cnt += 1
        left += 1
        right -= 1
    elif num_list[left] + num_list[right] < m:
        left += 1
    else:
        right -= 1
print(cnt)