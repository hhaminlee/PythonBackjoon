k = int(input())

for i in range(1, k + 1):
    max_gap = 0
    a = list(map(int, input().split()))
    max_score = max(a[1:])
    min_score = min(a[1:])
    b = sorted(a[1:], reverse=True)
    for j in range(1, a[0]):
        if(b[j-1]-b[j] > max_gap):
            max_gap = b[j-1] - b[j]
    print(f"Class {i}")
    print(f"Max {max_score}, Min {min_score}, Largest gap {max_gap}")