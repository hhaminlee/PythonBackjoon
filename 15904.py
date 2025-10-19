# 백준 15904 UCPC는 무엇의 약자일까?
words = input()

target = "UCPC"  
target_index = 0 

for char in words:
    if target_index < len(target) and char == target[target_index]:
        target_index += 1 # 일치하면 다음 문자를 찾기 위해 인덱스를 1 증가

if target_index == len(target):
    print("I love UCPC")
else:
    print("I hate UCPC")