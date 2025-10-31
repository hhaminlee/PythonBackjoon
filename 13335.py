# 백준 13335 트럭

# n: 트럭의 갯수, w: 다리의 길이, l: 다리의 최대하중
n, w, l = map(int, input().split())
truck = list(map(int, input().split()))

i = 0
result = 0
bridge = [0] * w
while True:
    # 앞으로 한칸 이동
    bridge.pop(0)
    if i < n:
        # 만약 더 들어갈 수 있다면 append(truck[i])
        if sum(bridge) + truck[i] <= l:
            bridge.append(truck[i])
            i += 1
        else:
            # 들어갈 수 없으면 append(0)
            bridge.append(0)
    # 로직이 다 끝났을 때만 result += 1
    result += 1
    # 다리가 다 비면 종료
    if not bridge:
        break

print(result)