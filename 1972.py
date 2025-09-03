while True:
    words = input().strip()
    if words == '*':
        break
    n = len(words)
    is_surprising = True

    for i in range(1, n):
        pairs = []
        for j in range(n - i):
            pairs.append(words[j] + words[j+i])
        if len(pairs) != len(set(pairs)):
            print(f"{words} is NOT surprising.")
            is_surprising = False
            break

    if is_surprising:
        print(f"{words} is surprising.")
