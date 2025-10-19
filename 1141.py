# 백준 1141 접두사
# 해당 원소가 접두사일때 +1 후 1인 것들만 더해서 결과 출력
# 연관이 없는 것들만 더한 값이 부분집합의 최대 크기이기 때문에

n = int(input())
word_list = list(set(input().strip() for _ in range(n))) # 중복값이 들어오면 제대로 잡지 못함

word_list.sort(key=len, reverse=True)

result_list = [0] * len(word_list)
for i in range(len(word_list)):
    for j in range(len(word_list)):
        if i != j and word_list[j].startswith(word_list[i]):
            result_list[i] += 1
cnt = 0
print(sum(1 for i in range(len(word_list)) if result_list[i] == 0))