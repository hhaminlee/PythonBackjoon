n, l = map(int, input().split())
leaks = sorted(list(map(int, input().split())))
cnt = 0
end = -2000
for i in leaks:
    if i + 0.5 <= end:
        continue
    cnt += 1 
    end = i-0.5 + l
print(cnt)