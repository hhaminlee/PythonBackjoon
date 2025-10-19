# 백준 11652 카드
import sys
from collections import Counter
input = sys.stdin.readline

n = int(input())
int_list = [int(input()) for _ in range(n)]
count_d = Counter(int_list)

# items안에 들어있는 것들을 기준으로 정렬
# 첫번째 조건은 빈도수가 많을 수록
# 두번째 조건은 값이 작을수록
sorted_result = sorted(count_d.items(), key=lambda x: (-x[1], x[0]))
print(sorted_result[0][0])
