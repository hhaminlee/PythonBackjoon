# 백준 1758 알바생 강호
# 해결 방법: 내림차순 정렬 이후 그리디로 계산
# 문제 요약: 스타박스 앞에 있는 사람의 수 N과, 각 사람이 주려고 생각하는 팁이 주어질 때, 손님의 순서를 적절히 바꿨을 때, 강호가 받을 수 잇는 팁의 최댓값을 구하는 프로그램을 작성하시오.
# 처음 접근: 내림차순 정렬, 이후에 그리디로 팁을 계산

n = int(input())
tips = [int(input()) for _ in range(n)]
tips.sort(reverse=True)

result = 0
for i in range(n):
    result += max(0, tips[i] - i)

print(result)