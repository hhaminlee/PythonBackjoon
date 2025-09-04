words = input()

result = ''
for ch in words:
    if ch == 'U' or ch == 'C' or ch == 'P':
        result += (ch)

if 'UCPC' in result:
    print("I love UCPC")
else:
    print("I hate UCPC")