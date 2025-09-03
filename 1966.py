n = int(input())
aa =[]
for i in range(n):
    result = 0
    m, important = map(int, input().split())
    # 한줄 입력을 받은 후 인덱스까지 쌍으로 넣어주기
    q = [(i, x) for i, x in enumerate(map(int, input().split()))]

    while True:
        now = q.pop(0)  # 맨 앞 요소 꺼냄

        # 만약 중요도 최댓값이라면 출력 처리
        if not q or now[1] >= max(x[1] for x in q):
            result += 1
            if now[0] == important:  # 목표 문서면 출력
                print(result)
                break
        else:
            q.append(now)  # 중요도 낮으면 맨 뒤로 보냄