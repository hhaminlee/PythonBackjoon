# 백준 9536 여우는 어떻게 울지?
t = int(input())

# t를 무시하고 코드를 짜서 한번 틀림 -> 이후 for문 추가, 해결
for i in range(t):
    # 모든 동물이 말하는 것을 담는 리스트
    fox_say = input().strip().split()
    # 동물별 울음소리를 저장하기 위한 딕셔너리
    animals = {}
    while True:
        animal = input().strip()
        # what does the fox say?가 나올 때까지 입력 받기
        if animal == 'what does the fox say?':
            break
        # goes기준 앞 뒤 자르기
        animals[animal.split(' goes ')[0]] = animal.split(' goes ')[1]

    # 해당하는 요소들을 모두 제거하기 위해 while v in fox_say를 돌면서 remove
    # *를 통해 리스트에서 꺼내 출력
    for k, v in animals.items():
        while v in fox_say:
            fox_say.remove(v)
    print(*fox_say)