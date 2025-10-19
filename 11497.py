# 백준 11497 통나무 건너뛰기
t = int(input())

# 중앙에서부터 작은 값들 오른쪽, 왼쪽에 넣기
for i in range(t):
    n = int(input())
    sub_list = []
    result = -1
    l = list(map(int, input().split()))
    l.sort(reverse=True)
    for j in range(0, len(l)-1, 2):
        sub_list.append(l[j])
        sub_list.insert(0, l[j+1])
    # 길이가 홀수일 경우 값 하나가 안들어가서 넣어주기
    if len(l) % 2 != 0:
        sub_list.insert(0, l[len(l)-1])

    for k in range(len(sub_list) - 1):
        if result < abs(sub_list[k] - sub_list[k+1]):
            result = abs(sub_list[k] - sub_list[k+1])
    # 첫번째랑 마지막 값도 비교
    if result < abs(sub_list[0] - sub_list[len(sub_list) - 1]):
        result = abs(sub_list[0] - sub_list[len(sub_list) - 1])
    print(result)

# gpt 코드
# import sys
# input = sys.stdin.readline

# t = int(input())
# for _ in range(t):
#     n = int(input())
#     a = sorted(map(int, input().split()))
#     # 원형 배치: 짝수 인덱스는 그대로, 홀수 인덱스는 뒤집어서 이어붙이기
#     b = a[::2] + a[1::2][::-1]
#     # 원형이므로 마지막과 첫 번째도 비교
#     ans = max(abs(b[i] - b[(i + 1) % n]) for i in range(n))
#     print(ans)
