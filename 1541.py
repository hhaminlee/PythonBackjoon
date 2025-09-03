import sys
input = sys.stdin.readline

result = 0
operation = input().strip()
if '-' in operation:
    sub_list = operation.split('-')
else:
    sub_list = [operation] # 리스트안에 문자열을 넣어줘야 에러가 발생하지 않음

sum_list = []
for i in range(len(sub_list)):
    if '+' in sub_list[i]:
        sum_list.append(sum(map(int, sub_list[i].split('+'))))
    else:
        sum_list.append(int(sub_list[i]))

result = sum_list[0]
for j in range(1, len(sum_list)):
    result -= sum_list[j]
print(result)
