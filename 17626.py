n = int(input())
result = 0
dp = [0, 1]
for i in range(2, n+1):
    min_v = 5
    j = 1
    while j**2 <= i:
        min_v = min(min_v, dp[i-j**2]) 
        # dp[i-j**2]의 값은 이전 상태 최소값
        # 여기에 j**2를 추가했으니까 +1
        j += 1
    dp.append(min_v + 1)
print(dp[n])