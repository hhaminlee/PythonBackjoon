isbn = input()

result = 0
weight = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
m = int(isbn[len(isbn) - 1])
for i in range(len(isbn) - 1):
    if isbn[i] != '*':
        result += int(isbn[i]) * weight[i]
    else:
        check_weight = weight[i]

for i in range(10):
    check_digit = (check_weight * i + result) % 10
    check_digit = 0 if check_digit == 0 else 10 - check_digit
    if check_digit == m:
        print(i)