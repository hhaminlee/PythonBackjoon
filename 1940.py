# 백준 1940 주몽
# 해결 방법: 투 포인터 (정렬 후 양끝에서 좁혀오기)
# 처음 접근: 이중 for문 O(n^2) 고려
# 시행착오: 시간 복잡도 고민 후 투 포인터로 전환
# 깨달음/배운점: 두 수의 합 → 정렬+투 포인터가 정석

n = int(input())
m = int(input())
num_list = list(map(int, input().split()))
num_list.sort()
left = 0
right = n-1
cnt = 0
# 정렬 먼저 하고, 투포인터로 정리
# right가 left보다 클 때만 반복
while left < right:
    # 합이 같을 경우 범위를 좁혀가며 cnt 증가
    if num_list[left] + num_list[right] == m:
        cnt += 1
        left += 1
        right -= 1
    # 합이 작은 경우 left(작은값) 인덱스만 증가
    elif num_list[left] + num_list[right] < m:
        left += 1
    # 합이 큰 경우 right(큰값) 인덱스만 감소
    else:
        right -= 1
print(cnt)